"""The release-inventory drift family (add-release-inventory-drift-check).

The taxonomy under test is EXHAUSTIVE AND DISJOINT, and three of its five arms
were wrong in the change's first draft and tightened by review before any code
existed. Each arm gets its own test, and the two that were confused with each
other — a member ABSENT at the commit versus GIT UNAVAILABLE — are tested
against each other, because that confusion is the defect the tightening fixed.

  no bundle declared ............................. SKIP
  bundle declared, inventory file absent ......... ERROR
  member absent at the commit .................... ERROR (drift, not a skip)
  member digest or mode differs .................. ERROR / INFO by editorial set
  every member matches ........................... no finding
  git unavailable ................................ SKIP (and never per-member)

Every fixture here is SYNTHESIZED, including the `contract-v1.36` shape: the
change's own tasks require the forgot-to-bump case be reproduced hermetically
rather than by reaching for a commit that happens to exist in this clone's
history, because a test that depends on a real sha stops testing anything the
day someone prunes or rewrites it.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import time
from pathlib import Path

import pytest

from conftest import FakeGit  # noqa: F401  (sys.path side effect)

import carved_reach

from doc_health import ERROR, Finding, INFO, PartialSkip, Skip
from doc_health import corpus, release_inventory
from doc_health.corpus import RealGit
from doc_health.families import FAMILIES, FAMILY_RESOLUTION
from doc_health.release_inventory import (
    EDITORIAL, FAMILY, check_repo, inventory_path_for, parse_declared_bundle,
    parse_inventory,
)

from action_pins import assert_actions_pinned, harvest_static

REPO = "openxFactory"
BUNDLE = "contract-v1.40"
INV = inventory_path_for(BUNDLE)
MANIFEST = "contracts/manifest.yaml"


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _inventory(members) -> bytes:
    """An inventory document in the shape the schema fixes."""
    lines = ["schema_version: 1",
             "kind: openxfactory-contract-release-digest-inventory",
             f"bundle_tag: {BUNDLE}",
             "entries:"]
    for path, (data, mode) in members.items():
        lines += [f"- artifact_id: {path.replace('/', '-')}",
                  f"  path: {path}",
                  "  type: schema",
                  f"  git_mode: '{mode}'",
                  f"  digest: sha256:{_digest(data)}"]
    return ("\n".join(lines) + "\n").encode("utf-8")


def _world(members, *, declared=BUNDLE, drop_inventory=False,
           blob_overrides=None, mode_overrides=None, absent=(),
           git_unavailable=False):
    """A repository whose declared bundle is `declared` and whose inventory
    records `members`, with the tree optionally diverging from it."""
    blobs, modes = {}, {}
    for path, (data, mode) in members.items():
        if path in absent:
            continue
        blobs[(REPO, path)] = (blob_overrides or {}).get(path, data)
        modes[(REPO, path)] = (mode_overrides or {}).get(path, mode)
    if not drop_inventory:
        blobs[(REPO, inventory_path_for(declared))] = _inventory(members)
    # THE DECLARED MANIFEST IS WRITTEN LAST, deliberately: the manifest is also
    # an inventory MEMBER, so a member loop that ran afterwards would overwrite
    # the declaration this fixture exists to set. That ordering bug made the
    # `declared=` parameter silently inert on its first outing.
    blobs[(REPO, MANIFEST)] = (
        f"contract_bundle_version: {declared}\n".encode("utf-8"))
    modes.setdefault((REPO, MANIFEST), "100644")
    return FakeGit(blobs=blobs, modes=modes, git_unavailable=git_unavailable)


SCHEMA = "contracts/schemas/gate-action-record.schema.yaml"
CHANGELOG = "contracts/CHANGELOG.md"

BASE = {
    SCHEMA: (b"kind: gate-action-record\n", "100644"),
    CHANGELOG: (b"# changelog\n", "100644"),
    MANIFEST: (b"contract_bundle_version: contract-v1.40\n", "100644"),
}
# The manifest's recorded digest must agree with what `_world` writes for the
# default declaration, or every test would carry a spurious manifest finding.
assert BASE[MANIFEST][0] == b"contract_bundle_version: contract-v1.40\n"


def _run(git):
    return check_repo(REPO, Path(REPO), git)


def _sev(findings, severity):
    return [f for f in findings if f.severity == severity]


# ---------------------------------------------------------------- the parsers

def test_the_declared_bundle_is_read_from_the_manifest():
    assert parse_declared_bundle(
        "kind: x\ncontract_bundle_version: contract-v1.40\n") == BUNDLE
    assert parse_declared_bundle("kind: x\n") is None


def test_the_inventory_parser_reads_path_digest_and_mode():
    parsed = parse_inventory(_inventory(BASE).decode())
    assert set(parsed) == set(BASE)
    assert parsed[SCHEMA]["digest"] == _digest(BASE[SCHEMA][0])
    assert parsed[SCHEMA]["git_mode"] == "100644"


def test_a_member_never_inherits_the_previous_members_digest():
    """The path resets the accumulator, so a malformed run of keys cannot
    silently attach one member's digest to another."""
    doc = ("entries:\n"
           "- path: a.yaml\n"
           "  digest: sha256:" + "a" * 64 + "\n"
           "- path: b.yaml\n"          # no digest of its own
           "- path: c.yaml\n"
           "  digest: sha256:" + "c" * 64 + "\n")
    parsed = parse_inventory(doc)
    assert parsed["b.yaml"] == {}
    assert parsed["a.yaml"]["digest"] == "a" * 64
    assert parsed["c.yaml"]["digest"] == "c" * 64


# ------------------------------------------------------- the five taxonomy arms

def test_every_member_matching_reports_nothing():
    assert _run(_world(BASE)) == []


def test_no_bundle_declared_is_a_skip():
    git = FakeGit(blobs={(REPO, MANIFEST): b"kind: manifest\n"}, modes={})
    outcome = _run(git)
    assert isinstance(outcome, Skip)
    assert "declares no contract_bundle_version" in outcome.reason


def test_a_declared_bundle_with_no_inventory_is_an_ERROR_not_a_skip():
    """A declaration naming an inventory that does not exist is an INVALID
    RELEASE DECLARATION — what a mistyped bundle name or a half-created release
    looks like — not an absent capability. The canonical verifier reports the
    same condition as HGR-RELEASE-INVENTORY-MISSING rather than declining."""
    outcome = _run(_world(BASE, drop_inventory=True))
    assert not isinstance(outcome, Skip)
    assert len(_sev(outcome, ERROR)) == 1
    assert "has no release digest inventory" in outcome[0].rule


def test_a_MISTYPED_bundle_name_is_an_ERROR_even_though_a_real_inventory_exists():
    """The distinct half of that arm, and the reason it is worth its own test:
    a VALID inventory is present — for the bundle the repository really cut —
    and the manifest names a different one. Nothing is missing from the tree;
    the DECLARATION is wrong. A family that looked for "any inventory" rather
    than "the declared one's" would pass this."""
    git = _world(BASE)                      # a real contract-v1.40 inventory
    git.blobs[(REPO, MANIFEST)] = b"contract_bundle_version: contract-v9.99\n"
    outcome = _run(git)
    assert not isinstance(outcome, Skip)
    errors = _sev(outcome, ERROR)
    assert len(errors) == 1
    assert "contract-v9.99" in errors[0].rule
    assert "has no release digest inventory" in errors[0].rule
    assert errors[0].path == inventory_path_for("contract-v9.99")


def test_a_member_absent_at_the_commit_is_drift_not_a_skip():
    """A deleted normative member is the strongest form of the drift this
    family exists to catch. Reported as an error against that member's path."""
    outcome = _run(_world(BASE, absent=(SCHEMA,)))
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [SCHEMA]
    assert "absent at HEAD" in errors[0].rule


def test_git_unavailable_is_a_skip_and_names_no_member():
    outcome = _run(_world(BASE, git_unavailable=True))
    assert isinstance(outcome, Skip)
    assert "could not be consulted" in outcome.reason


def test_absence_and_unavailability_are_DIFFERENT_verdicts():
    """The distinction the review tightening exists for. Same family, same
    inputs but for one bit, and the verdicts must not converge — before the
    tightening both were drafted as skips, which made a deleted contract
    indistinguishable from a broken checkout."""
    deleted = _run(_world(BASE, absent=(SCHEMA,)))
    unavailable = _run(_world(BASE, git_unavailable=True))
    assert not isinstance(deleted, Skip)
    assert isinstance(unavailable, Skip)


# ------------------------------------------------------- the editorial split

def test_non_editorial_drift_is_an_error():
    outcome = _run(_world(BASE, blob_overrides={SCHEMA: b"changed\n"}))
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [SCHEMA]
    assert "cut a release" in errors[0].action
    assert "never hand-edit" in errors[0].action
    # VERBATIM PIN (commissioned 2026-08-27, after `promotion_fidelity._ACTION`
    # was mutated and 85 tests stayed green — no doc-health family's action
    # line was pinned anywhere VERBATIM; the two substring checks above do not
    # catch a mutation that preserves both phrases). An action line is
    # operator guidance rendered in every ranked-plan row; nothing else in
    # this repository notices it changing.
    assert errors[0].action == (
        "cut a release through the bundle realization order; never "
        "hand-edit an inventory or contract_bundle_version to make "
        "this comparison pass")


def test_editorial_drift_is_info_and_reddens_no_gate():
    outcome = _run(_world(BASE, blob_overrides={CHANGELOG: b"# changed\n"}))
    assert _sev(outcome, ERROR) == []
    infos = _sev(outcome, INFO)
    assert [f.path for f in infos] == [CHANGELOG]
    assert "expected between cuts" in infos[0].rule


def test_the_editorial_set_is_exactly_the_three_ruled_members():
    assert EDITORIAL == {
        "contracts/CHANGELOG.md",
        "contracts/manifest.yaml",
        "contracts/README.md",
    }


def test_the_two_bands_are_not_one_code_path():
    """Both drift at once: the editorial member must not be promoted to error
    by its neighbour, nor the normative one demoted by its."""
    outcome = _run(_world(BASE, blob_overrides={
        SCHEMA: b"changed\n", CHANGELOG: b"# changed\n"}))
    assert [f.path for f in _sev(outcome, ERROR)] == [SCHEMA]
    assert [f.path for f in _sev(outcome, INFO)] == [CHANGELOG]


# ------------------------------------------------------------------ git_mode

def test_a_mode_only_change_is_caught():
    """A chmod leaves the bytes and therefore the digest identical. Without the
    mode arm a validator could drift executable -> non-executable while the
    family reported matching (PR #319, Codex P2)."""
    outcome = _run(_world(BASE, mode_overrides={SCHEMA: "100755"}))
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [SCHEMA]
    assert "git_mode 100755" in errors[0].rule
    assert "100644" in errors[0].rule


def test_a_mode_only_change_on_an_editorial_member_stays_info():
    outcome = _run(_world(BASE, mode_overrides={CHANGELOG: "100755"}))
    assert _sev(outcome, ERROR) == []
    assert [f.path for f in _sev(outcome, INFO)] == [CHANGELOG]


# ------------------------------------------- the contract-v1.36 true positive

def test_the_forgot_to_bump_shape_reports_non_editorial_drift():
    """THE contract-v1.36 DEFECT, SYNTHESIZED. A cut edits a schema and the
    changelog and the manifest but leaves `contract_bundle_version` naming the
    PREVIOUS bundle, so the tree is measured against the wrong inventory. The
    changed schema surfaces as non-editorial drift, at the commit, before any
    tag exists — which is why this class needs no tag access and no second rule.

    Synthesized rather than pointed at `08c5aa9`: a test that depends on a real
    sha stops testing anything the day someone prunes or rewrites it."""
    previous = {
        SCHEMA: (b"kind: gate-action-record\n", "100644"),
        CHANGELOG: (b"# changelog\n", "100644"),
    }
    # the cut edited the schema and the changelog but did NOT advance the
    # declared bundle, so `previous`'s inventory is what it is checked against
    git = _world(previous, blob_overrides={
        SCHEMA: b"kind: gate-action-record\n# + share-session\n",
        CHANGELOG: b"# changelog\n## contract-v1.36\n"})
    outcome = _run(git)
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [SCHEMA], (
        "the forgot-to-bump case must surface as non-editorial drift on the "
        "schema the cut changed")
    assert [f.path for f in _sev(outcome, INFO)] == [CHANGELOG]


# ---------------------------------------------------- the raw-bytes guarantee

def test_the_raw_reader_returns_CRLF_BYTES_from_a_real_commit(tmp_path):
    """THE RAW-BYTES RULE, PINNED AGAINST A REAL GIT OBJECT.

    A non-ASCII fixture would NOT do this job and the change's tasks say so:
    `é` encodes and decodes through a UTF-8 text-mode round trip to identical
    bytes, so the obvious fixture passes with the very reader the rule forbids.
    A committed CRLF blob does distinguish them — Python's universal-newline
    text mode rewrites `\\r\\n` to `\\n`, so a text-mode read yields different
    bytes and a different SHA-256 than the blob holds.

    The assertion is on the READER DIRECTLY rather than on the family's verdict,
    so it fails on a text-mode reader instead of merely happening to agree."""
    repo = tmp_path / "repo"
    repo.mkdir()
    run = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True,
                                    capture_output=True)
    run("init", "-q")
    run("config", "user.email", "t@example.invalid")
    run("config", "user.name", "T")
    run("config", "core.autocrlf", "false")
    raw = b"alpha\r\nbeta\r\n"
    (repo / "crlf.txt").write_bytes(raw)
    run("add", "crlf.txt")
    run("commit", "-qm", "crlf")

    got = RealGit().blobs_at(repo, "HEAD", ["crlf.txt"])["crlf.txt"]
    assert got == raw, "the reader must return the blob's RAW bytes"
    assert b"\r\n" in got, "a text-mode read would have collapsed CRLF to LF"
    assert hashlib.sha256(got).hexdigest() != hashlib.sha256(
        raw.replace(b"\r\n", b"\n")).hexdigest(), (
        "the fixture must DISTINGUISH the two readings, or it proves nothing")


def test_the_real_reader_distinguishes_absence_from_failure(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True,
                                    capture_output=True)
    run("init", "-q")
    run("config", "user.email", "t@example.invalid")
    run("config", "user.name", "T")
    (repo / "there.txt").write_text("x\n")
    run("add", "there.txt")
    run("commit", "-qm", "one")

    got = RealGit().blobs_at(repo, "HEAD", ["there.txt", "gone.txt"])
    assert got["there.txt"] == b"x\n"
    assert got["gone.txt"] is None, "absence is data, not failure"
    assert RealGit().blobs_at(tmp_path / "not-a-repo", "HEAD", ["x"]) is None


def test_the_real_reader_reports_modes(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run = lambda *a: subprocess.run(["git", "-C", str(repo), *a], check=True,
                                    capture_output=True)
    run("init", "-q")
    run("config", "user.email", "t@example.invalid")
    run("config", "user.name", "T")
    (repo / "plain.sh").write_text("#!/bin/sh\n")
    (repo / "exec.sh").write_text("#!/bin/sh\n")
    (repo / "exec.sh").chmod(0o755)
    run("add", "plain.sh", "exec.sh")
    run("commit", "-qm", "modes")

    modes = RealGit().tree_modes(repo, "HEAD")
    assert modes["plain.sh"] == "100644"
    assert modes["exec.sh"] == "100755"


# ------------------------------------------------- the #1098 subprocess bound

def _blocking_git_shim(tmp_path: Path, sleep_seconds: int = 2) -> Path:
    """A `git` on PATH that just sleeps past any sane bound, to prove a slow
    real subprocess is stopped by `_GIT_TIMEOUT_SECONDS` and not merely by
    however long the shim itself takes to exit."""
    bin_dir = tmp_path / "fake-bin"
    bin_dir.mkdir()
    shim = bin_dir / "git"
    shim.write_text(f"#!/bin/sh\nsleep {sleep_seconds}\nexit 1\n")
    shim.chmod(0o755)
    return bin_dir


def test_run_hits_the_timeout_rather_than_hanging(tmp_path, monkeypatch):
    """#1098: `_run` (corpus.py's shared primitive for every OTHER RealGit
    reader) bound no `timeout=` at all, so a blocked promisor remote could
    hang rather than answer the `None` the class's own docstring documents
    for a git failure. `_GIT_TIMEOUT_SECONDS` is monkeypatched down so the
    test proves the BOUND fired, not merely that the shim eventually exited
    on its own well inside a slower bound."""
    bin_dir = _blocking_git_shim(tmp_path, sleep_seconds=2)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr(corpus, "_GIT_TIMEOUT_SECONDS", 0.2)

    start = time.monotonic()
    result = RealGit()._run(tmp_path, "log", "-1")
    elapsed = time.monotonic() - start

    assert result is None, (
        "a timed-out probe must answer the same None a failed git already "
        "does, so every existing caller's skip handling is unchanged")
    assert elapsed < 2.0, (
        f"took {elapsed:.2f}s -- bounded by the shim's own sleep rather "
        "than by _GIT_TIMEOUT_SECONDS, so the timeout is not really wired")


def test_blobs_at_hits_the_timeout_rather_than_hanging(tmp_path, monkeypatch):
    """Same gap, the batch `cat-file` reader: #1098 names it as `_run`'s
    twin, the file's only OTHER raw `subprocess.run` call site."""
    bin_dir = _blocking_git_shim(tmp_path, sleep_seconds=2)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setattr(corpus, "_GIT_TIMEOUT_SECONDS", 0.2)

    start = time.monotonic()
    result = RealGit().blobs_at(tmp_path, "HEAD", ["some/path.yaml"])
    elapsed = time.monotonic() - start

    assert result is None, (
        "a timed-out batch read must answer None, the same failed-read "
        "result blobs_at already gives on a bare OSError")
    assert elapsed < 2.0, f"took {elapsed:.2f}s -- the timeout did not bound the call"


def test_a_missing_git_binary_answers_none_not_a_crash(tmp_path, monkeypatch):
    """#1098's second, separate gap: `_run` had no `try`/`except` AT ALL, so
    an unrunnable git raised `FileNotFoundError` straight out of the reader
    instead of the `None` every OTHER git failure already answers with.
    `blobs_at`'s bare `except OSError` already caught this case before this
    fix; asserted again here so widening it to also catch
    `subprocess.TimeoutExpired` is shown NOT to have narrowed it."""
    empty_bin = tmp_path / "empty-bin"
    empty_bin.mkdir()
    monkeypatch.setenv("PATH", str(empty_bin))

    assert RealGit()._run(tmp_path, "log", "-1") is None
    assert RealGit().blobs_at(tmp_path, "HEAD", ["some/path.yaml"]) is None


# ------------------------------------------------------------- the wiring

def test_the_family_is_registered():
    assert FAMILY in FAMILIES


def test_the_family_is_ABSENT_from_family_resolution():
    """The structural reason, pinned rather than left as a comment: BOTH of
    this family's findings are resolved by a RELEASE CUT, which is exactly the
    act that makes them vanish between reports. A `contested` class would route
    every correctly performed cut through `report.uncited_resolutions` as a new
    ERROR — enforcement arriving through the back door on the runs that prove
    the family working."""
    assert FAMILY not in FAMILY_RESOLUTION


def test_findings_carry_the_default_resolution_class():
    outcome = _run(_world(BASE, blob_overrides={SCHEMA: b"changed\n"}))
    assert {f.resolution for f in outcome} == {"auto-fixable"}


def test_every_finding_names_the_cut_and_forbids_the_hand_edit():
    outcome = _run(_world(BASE, blob_overrides={
        SCHEMA: b"changed\n", CHANGELOG: b"# changed\n"}))
    for finding in outcome:
        assert "cut a release" in finding.action
        assert "never hand-edit" in finding.action


# ------------------------------------------------- the ratified-text fixes
#
# Two conformance gaps a review found against the RATIFIED delta, not against
# taste: the code disagreed with a scenario in one place and with a
# per-repository obligation in another. Both are pinned here.


def test_an_absent_EDITORIAL_member_is_an_error_too():
    """The ratified scenario is UNQUALIFIED — "a deleted normative member is
    the strongest form of the drift this family exists to catch" — and the
    editorial allowance is about members that legitimately MOVE between cuts,
    not ones that legitimately VANISH. A deleted `contracts/CHANGELOG.md` is
    not an expected steady state under any reading.

    The first version of the absence branch carried
    `ERROR if not editorial else INFO`, which contradicted both the scenario and
    the module's own docstring taxonomy."""
    outcome = _run(_world(BASE, absent=(CHANGELOG,)))
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [CHANGELOG]
    assert "absent at HEAD" in errors[0].rule
    assert _sev(outcome, INFO) == []


def test_absence_outranks_the_editorial_band_for_every_member():
    """Every editorial member EXCEPT the manifest, and the exception is not a
    gap: the manifest's absence means no bundle is DECLARED at all, which is
    the skip arm rather than the drift arm. There is no state in which a
    declared bundle's own manifest is missing from the tree it was read from."""
    testable = sorted((EDITORIAL & set(BASE)) - {MANIFEST})
    assert testable, "the fixture must carry at least one absentable member"
    for path in testable:
        outcome = _run(_world(BASE, absent=(path,)))
        assert [f.severity for f in outcome if f.path == path] == [ERROR], path


def test_a_skipped_repository_is_REPORTED_not_silently_omitted():
    """The ratified obligation is PER-REPOSITORY: a family that cannot run
    "MUST be reported as skipped, never silently omitted". The family-level
    Skip can only carry the all-skipped case, and in this factory the everyday
    state is mixed — most pinned repositories declare no bundle — so a design
    that only spoke up when EVERY repository skipped would be silent about most
    of them on every run."""
    from doc_health.release_inventory import fam_release_inventory_drift

    class Ctx:
        repo_paths = {"declaring": Path("declaring"), "silent": Path("silent")}
        git = None

    declaring = _world(BASE)
    ctx = Ctx()
    # one repo declares a bundle and matches; the other has no manifest at all
    ctx.git = FakeGit(
        blobs={(("declaring"), k[1]): v for k, v in declaring.blobs.items()},
        modes={(("declaring"), k[1]): v for k, v in declaring.modes.items()})
    out = fam_release_inventory_drift(ctx)
    assert not isinstance(out, Skip), "one repo was askable, so not a family skip"
    silent = [f for f in out if f.repo == "silent"]
    assert len(silent) == 1
    assert silent[0].severity == INFO
    assert "not checked" in silent[0].rule
    assert "declares no contract_bundle_version" in silent[0].rule or \
           "no contracts/manifest.yaml" in silent[0].rule


def test_all_repositories_skipping_is_still_a_family_skip():
    from doc_health.release_inventory import fam_release_inventory_drift

    class Ctx:
        repo_paths = {"a": Path("a"), "b": Path("b")}
        git = FakeGit(blobs={}, modes={})
    out = fam_release_inventory_drift(Ctx())
    assert isinstance(out, Skip)


def test_an_unresolvable_commit_is_not_reported_as_a_missing_manifest():
    """`cat-file --batch` answers `missing` both for an absent path at a good
    commit and for a spec whose COMMIT does not resolve, so the bare None
    cannot tell them apart. Reporting "no manifest" for an unresolvable commit
    sends a reader looking in the wrong place."""
    git = FakeGit(blobs={}, modes={}, git_unavailable=False)
    # blobs_at answers None-per-path (absence) but tree_modes answers None,
    # which is the signature of a commit that does not resolve
    git.tree_modes = lambda repo, commit: None
    outcome = check_repo(REPO, Path(REPO), git)
    assert isinstance(outcome, Skip)
    assert "does not resolve" in outcome.reason
    assert "no contracts/manifest.yaml" not in outcome.reason


def test_the_parser_refuses_a_digest_that_precedes_any_path():
    """The parser reads `path` before `digest` within an entry. That order is
    guaranteed by the WRITER (`release.build_release_inventory`), not by the
    schema — JSON Schema cannot constrain key order. So if a future writer
    changes it, this refuses loudly rather than mis-attributing a digest to the
    previous member."""
    with pytest.raises(ValueError, match="digest appears before any path"):
        parse_inventory("entries:\n  digest: sha256:" + "a" * 64 + "\n")


def test_the_never_tagged_bundle_scenario_is_STRUCTURAL_only():
    """Traceability note rather than a behavioural pin, said here because this
    is where a reader checks scenario coverage.

    The ratified scenario "The declared bundle was never tagged" is satisfied
    by CONSTRUCTION: nothing in this family reads a tag. `check_repo` resolves
    the inventory from `inventory_path_for(declared)` — a path in the tree —
    and no code path consults `git tag`, `ls-remote`, or a tag object. There is
    no behaviour to drive that could distinguish a tagged bundle from an
    untagged one, which is exactly what the scenario asks for."""
    import inspect

    from doc_health import release_inventory
    source = inspect.getsource(release_inventory)
    # Command tokens, not English words: the module's PROSE necessarily says
    # things like "the declared bundle describes the release surface", so a
    # bare `describe` substring matches the requirement's own name.
    for tagish in ('"ls-remote"', '"tag"', '"rev-list"', '"describe"',
                   '"for-each-ref"', "git tag"):
        assert tagish not in source, tagish


# ------------------------------------------- a malformed entry cannot pass
#
# THE FAIL-OPEN CLASS, closed (PR #324, Codex). Both comparisons were once
# written as `if recorded.get(field) and ...`, so an entry missing its `digest`
# skipped the byte check entirely — and if the mode still matched, the family
# reported the member CLEAN while its bytes had drifted. An inventory that
# cannot answer the question is not a matching inventory.


def _inventory_missing(field: str, path: str) -> bytes:
    """The BASE inventory with one field stripped from one entry."""
    doc = _inventory(BASE).decode()
    out, in_entry = [], False
    for line in doc.splitlines():
        if line.startswith("  path: "):
            in_entry = line == f"  path: {path}"
        if in_entry and line.strip().startswith(f"{field}:"):
            continue
        out.append(line)
    return ("\n".join(out) + "\n").encode()


def _world_missing(field, path, **kw):
    git = _world(BASE, **kw)
    git.blobs[(REPO, INV)] = _inventory_missing(field, path)
    return git


def test_an_entry_missing_its_digest_cannot_report_the_member_clean():
    """THE REPRODUCTION. Bytes drifted, mode still matching, digest absent —
    which reported CLEAN before the fix."""
    git = _world_missing("digest", SCHEMA,
                         blob_overrides={SCHEMA: b"DRIFTED BYTES\n"})
    outcome = _run(git)
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [SCHEMA]
    assert "missing digest" in errors[0].rule
    assert "cannot be checked at all" in errors[0].rule
    assert outcome != [], "a member whose bytes cannot be checked is not clean"


def test_an_entry_missing_its_git_mode_is_an_error_too():
    outcome = _run(_world_missing("git_mode", SCHEMA))
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [SCHEMA]
    assert "missing git_mode" in errors[0].rule


def test_a_malformed_entry_is_an_error_even_for_an_EDITORIAL_member():
    """Unconditional, for the same reason absence is: the editorial allowance
    is about members that legitimately MOVE between cuts, and says nothing
    about an entry that cannot be read."""
    outcome = _run(_world_missing("digest", CHANGELOG))
    errors = _sev(outcome, ERROR)
    assert [f.path for f in errors] == [CHANGELOG]
    assert _sev(outcome, INFO) == []


def test_a_malformed_entry_names_the_rebuild_not_a_release_cut():
    """The action differs from every other finding here on purpose: a broken
    inventory is repaired by rebuilding it, not by cutting a release over it."""
    outcome = _run(_world_missing("digest", SCHEMA))
    assert "validate-contract-release.py build" in outcome[0].action
    assert "cut a release" not in outcome[0].action


def test_a_well_formed_entry_is_still_compared_on_both_fields():
    """The fix must not have turned the comparisons off: with every field
    present, drift on each is still reported."""
    assert _sev(_run(_world(BASE, blob_overrides={SCHEMA: b"x\n"})), ERROR)
    assert _sev(_run(_world(BASE, mode_overrides={SCHEMA: "100755"})), ERROR)


def test_every_action_string_the_release_inventory_drift_family_can_emit_is_pinned_verbatim():
    """`release_inventory.check_repo`/`fam_release_inventory_drift` raise SIX
    distinct action strings. `#448` (`cadc05ec`) pinned one
    (`test_non_editorial_drift_is_an_error`, above — its VERBATIM pin, not
    the two substring checks beside it, which cannot catch a mutation that
    preserves both phrases). Steward follow-up (Brett, 2026-08-28) widens
    that to the whole set, table-driven.

    FIVE are pinned BEHAVIOURALLY, reusing this suite's own `_run`,
    `_world`, `_world_missing` and `BASE` fixture helpers exactly as the
    existing per-arm tests above use them, plus one `fam_release_inventory_drift`
    call (the family-level per-repository skip precedent,
    `test_a_skipped_repository_is_REPORTED_not_silently_omitted`) for the
    "no action" INFO action a bare `check_repo` call never reaches. THE SIXTH
    — the `info` action a CARRYING skip takes instead (`#1048` round 2), where
    the repository was PARTLY evaluated — is pinned STATICALLY: producing it
    behaviourally needs a repository whose pinned leg goes unreadable partway
    through its members, which is a real-git fixture rather than a `FakeGit`
    world. It is reached, and separately asserted, by
    `test_a_carrying_skip_is_reported_WITH_its_findings_not_instead_of_them`.
    """
    from doc_health.release_inventory import fam_release_inventory_drift

    behavioral = set()

    # non-editorial byte drift (also proves the VERBATIM _CUT_ACTION text)
    behavioral |= {f.action for f in
                  _run(_world(BASE, blob_overrides={SCHEMA: b"changed\n"}))}

    # declared bundle with no inventory
    behavioral |= {f.action for f in
                  _run(_world(BASE, drop_inventory=True))}

    # inventory names no members at all
    empty_inventory_git = _world(BASE)
    empty_inventory_git.blobs[(REPO, inventory_path_for(BUNDLE))] = (
        b"schema_version: 1\nentries:\n")
    behavioral |= {f.action for f in _run(empty_inventory_git)}

    # an inventory entry missing digest/git_mode cannot report the member clean
    behavioral |= {f.action for f in _run(_world_missing("digest", SCHEMA))}

    # the per-repository skip, reported as an INFO finding rather than
    # dropped — needs a SECOND, askable repository, or the family collapses
    # to an all-skip (test_all_repositories_skipping_is_still_a_family_skip
    # precedent) and never reaches the per-repository INFO finding at all.
    declaring = _world(BASE)
    class Ctx:
        repo_paths = {"declaring": Path("declaring"), "silent": Path("silent")}
        git = FakeGit(
            blobs={("declaring", k[1]): v for k, v in declaring.blobs.items()},
            modes={("declaring", k[1]): v for k, v in declaring.modes.items()})
    behavioral |= {f.action for f in fam_release_inventory_drift(Ctx())}

    behavioral = frozenset(behavioral)
    static = harvest_static(release_inventory)

    EXPECTED_ACTIONS = {
        "cut a release through the bundle realization order; never "
        "hand-edit an inventory or contract_bundle_version to make this "
        "comparison pass",
        "declare a bundle whose inventory exists, or create the inventory "
        "through the bundle realization order",
        "rebuild the inventory with scripts/validate-contract-release.py "
        "build",
        "rebuild the inventory with scripts/validate-contract-release.py "
        "build; an entry that cannot answer is not an entry that matches",
        "no action — this repository's release surface was not evaluated, "
        "and the reason is recorded rather than omitted",
        "no action on this line — the question it names could not be asked, "
        "and the members this repository HAD compared before it stand, with "
        "whatever they established reported beside it rather than discarded "
        "with it",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="release-inventory-drift")


# ----------------------------------------- a linked worktree reads the same
#
# WHY THESE USE REAL GIT AND A REAL SUBMODULE RATHER THAN `FakeGit` (`#1048`).
# The defect they pin is not in any code path a stubbed git reaches: it was in
# how `carved_reach` LOCATED the pinned leg's object store, and the difference
# between a checkout and a linked worktree of that checkout is a fact about
# git's own on-disk layout. `git worktree add` writes the superproject's tracked
# files and leaves every gitlink an EMPTY DIRECTORY, while the leg's objects
# stay in the superproject's common git directory under `modules/<name>`. A
# stub cannot have that shape, so a fixture built on one would pass against the
# broken reader and prove nothing.
#
# THE FIXTURE MIRRORS `openxdox_spec`, two submodule levels deep, rather than a
# one-level mount, because that is the shape the family actually reads:
# `openXdox/spec` is a submodule OF A SUBMODULE, so the second level's parent is
# itself a module store and not a working tree at all. A one-level fixture
# exercises half the walk and the wrong half.

BUNDLE_WT = "contract-v0.0-worktree-fixture"
MOVED = "contracts/moved.schema.yaml"
KEPT = "contracts/kept.yaml"
MOVED_BYTES = b"kind: moved-by-the-shed\n"
KEPT_BYTES = b"kind: never-moved\n"


def _git_in(repo: Path, *args: str) -> None:
    # `protocol.file.allow` because every remote here is a local path: git has
    # refused the file transport for submodules since CVE-2022-39253, and the
    # same opt-in is already how `tests/former_id_arrival` builds its fixtures.
    subprocess.run(["git", "-c", "protocol.file.allow=always", "-C", str(repo),
                    *args], check=True, capture_output=True)


def _new_repo(path: Path) -> Path:
    path.mkdir(parents=True)
    _git_in(path, "init", "-q", "-b", "main")
    _git_in(path, "config", "user.email", "t@example.invalid")
    _git_in(path, "config", "user.name", "T")
    # A PARTIAL CLONE OF THIS REPO IS A FIXTURE THE ROUND-2 ARMS NEED, and the
    # server side has to allow the filter or `--filter=tree:0` is answered with
    # a full pack. Harmless everywhere else: it changes nothing for a clone
    # that asks for no filter.
    _git_in(path, "config", "uploadpack.allowfilter", "true")
    return path


def _write_file(repo: Path, relpath: str, data: bytes) -> None:
    target = repo / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def _worktree_inventory(drifting=(), members=(KEPT, MOVED)) -> bytes:
    """Two members: one this repository still carries, and one the shed moved
    into the pinned leg BYTE FOR BYTE — so a reader that reaches the leg finds
    the digest matching and a reader that does not has an opinion to state.

    `drifting` records a WRONG digest for the members it names, which is how
    the carrying-skip arm below gets a repository that has established a
    finding BEFORE its leg stops being readable.

    `members` narrows the recorded set. Comparison runs in SORTED path order,
    so recording the moved member ALONE is how the round-3 arm gets a
    repository whose very first member is the unreadable one and which
    therefore evaluated nothing at all — the other side of the partly-evaluated
    distinction."""
    lines = ["schema_version: 1",
             "kind: openxfactory-contract-release-digest-inventory",
             f"bundle_tag: {BUNDLE_WT}",
             "entries:"]
    for path, data in ((KEPT, KEPT_BYTES), (MOVED, MOVED_BYTES)):
        if path not in members:
            continue
        recorded = _digest(data + b"drifted" if path in drifting else data)
        lines += [f"- artifact_id: {path.replace('/', '-')}",
                  f"  path: {path}",
                  "  type: schema",
                  "  git_mode: '100644'",
                  f"  digest: sha256:{recorded}"]
    return ("\n".join(lines) + "\n").encode("utf-8")


def _shed_fixture(tmp_path: Path, drifting=(), members=(KEPT, MOVED)) -> Path:
    """A superproject declaring a bundle whose inventory records a member that
    exists ONLY in a leg pinned two submodule levels down."""
    spec = _new_repo(tmp_path / "origin-spec")
    _write_file(spec, MOVED, MOVED_BYTES)
    _git_in(spec, "add", "-A")
    _git_in(spec, "commit", "-qm", "the leg carries the moved member")

    leg = _new_repo(tmp_path / "origin-leg")
    _git_in(leg, "submodule", "add", "-q", str(spec), "spec")
    _git_in(leg, "commit", "-qm", "the leg pins its spec submodule")

    root = _new_repo(tmp_path / "checkout")
    _write_file(root, KEPT, KEPT_BYTES)
    _write_file(root, MANIFEST, f"schema_version: 1\nkind: manifest\n"
                                f"contract_bundle_version: {BUNDLE_WT}\n"
                                .encode("utf-8"))
    _write_file(root, inventory_path_for(BUNDLE_WT),
                _worktree_inventory(drifting, members))
    _git_in(root, "submodule", "add", "-q", str(leg), "leg")
    _git_in(root, "submodule", "update", "--init", "--recursive", "-q")
    _git_in(root, "add", "-A")
    _git_in(root, "commit", "-qm", "declare the bundle and pin the leg")
    return root


def _point_carve_at(monkeypatch, root: Path) -> None:
    """`carved_reach` as it IS in the checkout being read, which is not a
    fiction: the module is imported from that checkout's own `scripts/`, so its
    `REPO_ROOT` really is whichever tree the run is reading — the worktree when
    the run is in the worktree."""
    monkeypatch.setattr(carved_reach, "REPO_ROOT", root)
    monkeypatch.setattr(carved_reach, "MOUNTS",
                        {"leg_spec": root / "leg" / "spec"})
    monkeypatch.setattr(carved_reach, "_rows", lambda: {
        MOVED: {"source_path": MOVED, "disposition": "moved_verbatim",
                "destination": "leg_spec", "destination_path": MOVED}})


def test_a_linked_worktree_reads_the_same_release_surface(tmp_path, monkeypatch):
    """ONE COMMIT, TWO CHECKOUTS, ONE VERDICT (`#1048`).

    Measured on the real repository before the fix: the checkout reported one
    error and a `git worktree add` of the SAME commit reported five — the four
    extra naming members that exist in neither tree, because they live in a leg
    the worktree was wrongly told it could not reach."""
    root = _shed_fixture(tmp_path)
    worktree = tmp_path / "worktree"
    _git_in(root, "worktree", "add", "--quiet", "--detach", str(worktree),
            "HEAD")
    assert not (worktree / "leg" / ".git").exists(), (
        "the fixture must reproduce the shape the defect needs: `git worktree "
        "add` leaves every gitlink an EMPTY directory")

    git = RealGit()
    _point_carve_at(monkeypatch, root)
    from_checkout = check_repo(REPO, root, git)
    _point_carve_at(monkeypatch, worktree)
    from_worktree = check_repo(REPO, worktree, git)

    assert from_checkout == [], (
        "the moved member is recorded byte for byte as the leg holds it, so a "
        "checkout that can read the leg reports no drift at all")
    assert from_worktree == from_checkout, (
        "the worktree reported "
        f"{[f.rule for f in from_worktree]} where its own checkout reported "
        f"{[f.rule for f in from_checkout]}")


def test_the_legs_object_store_is_found_through_gits_common_directory(tmp_path):
    """THE ROOT CAUSE, ASSERTED ON THE RESOLVER ITSELF rather than only on the
    family's verdict, so it fails on a working-tree test rather than merely
    happening to agree — the same reason the raw-bytes rule above is pinned on
    its reader."""
    root = _shed_fixture(tmp_path)
    worktree = tmp_path / "worktree"
    _git_in(root, "worktree", "add", "--quiet", "--detach", str(worktree),
            "HEAD")

    assert carved_reach._leg_object_store(root, "leg") == root / "leg", (
        "a checked-out submodule is still read from its working tree")
    store = carved_reach._leg_object_store(worktree, "leg")
    assert store == root / ".git" / "modules" / "leg", (
        "a linked worktree shares the SUPERPROJECT's copy of the leg")
    assert carved_reach._leg_object_store(store, "spec") == \
        store / "modules" / "spec", (
        "and past the first level the parent is a module store, not a "
        "working tree — which is the level `openXdox/spec` reads at")


def test_an_unreachable_leg_is_a_repository_skip_not_a_phantom_absence(
        tmp_path, monkeypatch):
    """THE SIXTH ARM, NOT THE THIRD (`#1048`).

    A side clone that never initialized the submodule cannot read the leg at
    all, and that is a fact about the checkout rather than about the release.
    Before the fix the refusal was swallowed and every moved member was reported
    ABSENT AT THE COMMIT — the family's most severe verdict, naming files a
    reader then cannot find in EITHER tree."""
    root = _shed_fixture(tmp_path)
    side_clone = tmp_path / "side-clone"
    subprocess.run(["git", "clone", "-q", str(root), str(side_clone)],
                   check=True, capture_output=True)
    assert list((side_clone / "leg").iterdir()) == [], (
        "the fixture must reproduce an UNINITIALIZED submodule")

    _point_carve_at(monkeypatch, side_clone)
    outcome = check_repo(REPO, side_clone, RealGit())

    assert isinstance(outcome, Skip), (
        "the question could not be asked, so the repository is skipped — "
        f"got {outcome!r}")
    assert "leg_spec" in outcome.reason and "cannot be read" in outcome.reason
    assert "git submodule update --init" in outcome.reason, (
        "the skip must carry the leg's own remedy, which is the whole reason "
        "it beats errors naming files that are in neither tree")


def test_a_store_without_the_pinned_commit_is_a_skip_not_a_phantom_absence(
        tmp_path, monkeypatch):
    """A STORE THAT EXISTS IS NOT YET A STORE THAT ANSWERS (Copilot on PR
    #1051, `carved_reach.py:718`).

    `_leg_object_store`'s `HEAD` test proves the DIRECTORY is a git directory
    and nothing about its contents. A shallow clone, an interrupted fetch, and
    a gitlink advanced past what the store was fetched at all leave the same
    shape: a real module store that simply does not carry the pinned commit.
    Without the probe the walk read `None` one layer lower — from the next
    level's `rev-parse`, or from the caller's own blob read at the last level —
    and the member was reported ABSENT AT THE COMMIT again, which is the single
    misattribution this whole path exists to prevent."""
    root = _shed_fixture(tmp_path)

    stranger = _new_repo(tmp_path / "stranger")
    _write_file(stranger, "unrelated.txt", b"a commit no leg store carries\n")
    _git_in(stranger, "add", "-A")
    _git_in(stranger, "commit", "-qm", "a commit the leg's store never fetched")
    unknown = subprocess.run(["git", "-C", str(stranger), "rev-parse", "HEAD"],
                             check=True, capture_output=True,
                             text=True).stdout.strip()
    # A gitlink may name a commit the recording repository does not have — that
    # is what a gitlink IS — so this is the shape itself, not a simulation.
    _git_in(root, "update-index", "--add", "--cacheinfo",
            f"160000,{unknown},leg")
    _git_in(root, "commit", "-qm", "pin the leg at a commit its store lacks")

    worktree = tmp_path / "worktree-incomplete"
    _git_in(root, "worktree", "add", "--quiet", "--detach", str(worktree),
            "HEAD")
    store = carved_reach._leg_object_store(worktree, "leg")
    assert store is not None and (store / "HEAD").is_file(), (
        "the fixture must reproduce a store that PASSES the directory test")
    assert not carved_reach._git_ok(store, "cat-file", "-e",
                                    f"{unknown}^{{commit}}"), (
        "...and that does NOT carry the commit the superproject pins it at, "
        "or this test proves nothing")

    _point_carve_at(monkeypatch, worktree)
    outcome = check_repo(REPO, worktree, RealGit())

    assert isinstance(outcome, Skip), (
        "a store that cannot answer for the pinned commit has learned nothing "
        f"about the member — got {outcome!r}")
    assert unknown in outcome.reason, "the skip must name the unreadable commit"
    assert "leg_spec" in outcome.reason, "and the leg it was pinned in"


# ------------------------------------- round 2: an unreadable leg is never an
#                                       absence, and never a discarded finding
#
# WHAT THESE ADD TO THE FOUR ABOVE (`#1048` round 2). Those pin the case where
# the leg's object store cannot be FOUND or does not carry the pinned COMMIT.
# Every read after that point still failed open: a `rev-parse <commit>:<segment>`
# that answered nothing was read as "no gitlink there", and the blob and mode
# reads in `release_inventory._shed_member` answered `(None, None)` and `{}` on
# failure. Each of those is a fact about the MACHINE reported as a fact about
# the RELEASE — the identical misattribution, one layer lower each time.
#
# MEASURED BEFORE THEY WERE WRITTEN, git 2.43.0, throwaway stores:
#
#   a path genuinely not in a tree ....... `rev-parse` exit 128, `ls-tree`
#                                          EXIT 0 AND NO OUTPUT
#   the commit's tree object missing ..... `rev-parse` exit 128 (a different
#                                          `fatal:`, the same empty stdout),
#                                          `ls-tree` exit 128; and
#                                          `cat-file -e <commit>^{commit}`
#                                          STILL EXIT 0, which is why round 1's
#                                          commit probe passes this through
#   a subtree missing below a good root .. `ls-tree` exit 1, while
#                                          `cat-file -e <commit>^{tree}` exits
#                                          0 — so the root-tree probe is not
#                                          the discriminator, and `ls-tree` is
#   a blob the store does not hold ....... `cat-file --batch` answers
#                                          `<spec> missing` WITH EXIT 0 where
#                                          nothing can fetch it, and FAILS
#                                          OUTRIGHT (exit 128) where a promisor
#                                          remote is configured and unreachable
#
# The fixtures below reproduce those shapes with real git rather than simulate
# them: a `--filter=tree:0` store really is a store with the commit and without
# its tree, and a `--filter=blob:none` store really is one whose trees list a
# member it cannot serve.


def _side_clone(tmp_path: Path, root: Path, name: str) -> Path:
    """A clone that initialized no submodule — a side checkout, a CI job, a
    fresh box — and therefore the place a DEGRADED leg store can be put where
    `_leg_object_store` will find it."""
    side = tmp_path / name
    subprocess.run(["git", "clone", "-q", str(root), str(side)],
                   check=True, capture_output=True)
    return side


def _store_clone(source: Path, target: Path, *filters: str) -> None:
    """Build a leg's OBJECT STORE at the path `_leg_object_store` computes.

    `--bare`, because a module store IS a git directory rather than a checkout,
    and `file://` because git says `--filter is ignored in local clones; use
    file:// instead` — a path-spelled source would silently hand back a
    COMPLETE store and the fixture would prove nothing."""
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--bare", *filters,
                    f"file://{source}", str(target)],
                   check=True, capture_output=True)


def _dead_promisor(store: Path) -> None:
    """Point the partial clone's promisor remote at nothing.

    A live promisor REPAIRS the fixture on first read — git fetches the missing
    object and the test passes against any reader. Pointed at nothing, the lazy
    fetch fails loudly, which is what an offline box, a deleted remote and a
    credential-less CI job all look like."""
    _git_in(store, "remote", "set-url", "origin",
            f"file://{store}-no-such-remote")


def _forget_promisor(store: Path) -> None:
    """Make the same store a plain one that is simply MISSING objects.

    The other half of the measurement: with no promisor to try, `cat-file
    --batch` answers `<spec> missing` and EXITS 0 — the answer an absent path
    gives, for an object the store cannot serve. That indistinguishability is
    the whole reason the tree is asked."""
    for key in ("extensions.partialclone", "remote.origin.promisor",
                "remote.origin.partialclonefilter"):
        subprocess.run(["git", "-C", str(store), "config", "--unset", key],
                       capture_output=True)  # exit 5 where the key is absent


def _leg_store_of(side: Path) -> Path:
    return side / ".git" / "modules" / "leg"


def _spec_store_of(side: Path) -> Path:
    return _leg_store_of(side) / "modules" / "spec"


def _gitlink(repo: Path, rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", f"{rev}:{path}"],
                          check=True, capture_output=True,
                          text=True).stdout.strip()


def test_the_tree_probe_separates_a_missing_entry_from_an_unreadable_tree(
        tmp_path):
    """THE DISCRIMINATOR ITSELF, asserted on `carved_reach` rather than only
    through the family's verdict — the same reason the object-store resolver is
    pinned above rather than left to be implied by a green run.

    `rev-parse <commit>:<segment>` returns nothing for BOTH facts, so this is
    the read that has to tell them apart."""
    root = _shed_fixture(tmp_path)
    side = _side_clone(tmp_path, root, "side")
    _store_clone(tmp_path / "origin-leg", _leg_store_of(side), "--filter=tree:0")
    _dead_promisor(_leg_store_of(side))
    pinned = _gitlink(side, "HEAD", "leg")

    assert carved_reach._tree_entry_absent(side, "HEAD", "no-such-path") == \
        (True, ""), ("a tree that can be read and carries no such entry is an "
                     "ANSWER — git exits 0 and prints nothing")
    assert carved_reach._git_ok(_leg_store_of(side), "cat-file", "-e",
                                f"{pinned}^{{commit}}"), (
        "the fixture must reproduce a store that carries the pinned COMMIT — "
        "round 1's probe passes here, which is why this case reaches the walk")
    assert carved_reach._git_object_id(_leg_store_of(side), pinned, "spec") \
        is None, ("...and whose TREE it cannot read, so the gitlink read "
                  "answers exactly what a missing entry answers")
    readable, said = carved_reach._tree_entry_absent(_leg_store_of(side),
                                                     pinned, "spec")
    assert readable is False, (
        "an unreadable tree is a FAILURE, never an absence — got a claim that "
        "the leg's own tree carries no `spec` entry")
    assert said, "and the refusal quotes what git actually said"


def test_a_tree_the_store_cannot_read_is_a_skip_not_an_absent_gitlink(
        tmp_path, monkeypatch):
    """A STORE WITH THE COMMIT AND WITHOUT ITS TREE (`#1048` round 2).

    A `--filter=tree:0` clone whose promisor is unreachable is exactly that,
    and it is not exotic: it is what a partial CI checkout of a leg leaves
    behind. `shed_commit_object` read the gitlink with `rev-parse
    <commit>:<segment>`, got nothing, and returned `None` — "this commit
    records no such leg" — so `_shed_member` answered `(None, None)` and the
    family reported the member ABSENT AT THE COMMIT: a deleted normative
    contract, announced on the strength of an object nobody fetched."""
    root = _shed_fixture(tmp_path)
    side = _side_clone(tmp_path, root, "side")
    _store_clone(tmp_path / "origin-leg", _leg_store_of(side), "--filter=tree:0")
    _dead_promisor(_leg_store_of(side))

    _point_carve_at(monkeypatch, side)
    outcome = check_repo(REPO, side, RealGit())

    assert isinstance(outcome, Skip), (
        "the leg's tree could not be read, so nothing was learned about the "
        f"member it holds — got {outcome!r}")
    assert "leg_spec" in outcome.reason, "the skip names the leg"
    assert "UNESTABLISHED" in outcome.reason, (
        "and says what is unestablished rather than asserting an absence")
    assert "git submodule update --init" in outcome.reason, (
        "and carries the leg's own remedy")


def test_a_leg_store_that_cannot_serve_the_blob_is_a_skip_not_an_absence(
        tmp_path, monkeypatch):
    """THE READ AFTER THE PROBE (`#1048` round 2).

    Everything `shed_commit_object` checks passes here: the store is found, it
    carries the pinned commit, and both levels of the walk resolve. The BLOB is
    what the store cannot serve — a `--filter=blob:none` leg with an unreachable
    promisor — and `git.blobs_at` answers `None` for it, which `_shed_member`
    turned into `(None, None)` and the family into ABSENT AT THE COMMIT."""
    root = _shed_fixture(tmp_path)
    side = _side_clone(tmp_path, root, "side")
    _store_clone(tmp_path / "origin-leg", _leg_store_of(side))
    _store_clone(tmp_path / "origin-spec", _spec_store_of(side),
                 "--filter=blob:none")
    _dead_promisor(_spec_store_of(side))

    assert RealGit().blobs_at(_spec_store_of(side),
                              _gitlink(_leg_store_of(side),
                                       _gitlink(side, "HEAD", "leg"), "spec"),
                              [MOVED]) is None, (
        "the fixture must reproduce a store whose blob read FAILS, or this "
        "test proves nothing")

    _point_carve_at(monkeypatch, side)
    outcome = check_repo(REPO, side, RealGit())

    assert isinstance(outcome, Skip), (
        f"git declined the read, so the member is unknown — got {outcome!r}")
    assert MOVED in outcome.reason and "could not be read" in outcome.reason
    assert "git submodule update --init" in outcome.reason


def test_a_leg_tree_that_lists_a_member_it_cannot_serve_is_a_skip(
        tmp_path, monkeypatch):
    """THE HARDER HALF OF THE SAME READ, and the reason the tree is consulted.

    With nothing to fetch from, `cat-file --batch` reports the unserveable blob
    as `<spec> missing` AND EXITS 0 — byte for byte what it reports for a path
    that is not in the tree at all. The result alone cannot tell a pruned store
    from a deleted member; the TREE can, because it lists what the commit
    names rather than what the store holds."""
    root = _shed_fixture(tmp_path)
    side = _side_clone(tmp_path, root, "side")
    _store_clone(tmp_path / "origin-leg", _leg_store_of(side))
    _store_clone(tmp_path / "origin-spec", _spec_store_of(side),
                 "--filter=blob:none")
    _forget_promisor(_spec_store_of(side))

    spec_commit = _gitlink(_leg_store_of(side),
                           _gitlink(side, "HEAD", "leg"), "spec")
    git = RealGit()
    assert git.blobs_at(_spec_store_of(side), spec_commit, [MOVED]) == \
        {MOVED: None}, (
        "the fixture must reproduce the INDISTINGUISHABLE shape: the batch "
        "read succeeds and answers `missing`, exactly as it would for a "
        "member the leg genuinely does not carry")
    assert MOVED in (git.ls_tree_paths(_spec_store_of(side), spec_commit,
                                       MOVED) or []), (
        "...while the tree at that commit LISTS the member, which is what "
        "makes this a read that FAILED rather than an absence")

    _point_carve_at(monkeypatch, side)
    outcome = check_repo(REPO, side, RealGit())

    assert isinstance(outcome, Skip), (
        f"a listed member with no readable blob is unknown — got {outcome!r}")
    assert "FAILED rather than an absent member" in outcome.reason


def test_a_member_a_READABLE_leg_does_not_carry_is_still_reported_absent(
        tmp_path, monkeypatch):
    """THE ANSWER STILL STANDS, which is what keeps the arms above from being
    a blanket amnesty.

    A leg that can be read and does not carry the member has ANSWERED, and the
    answer is the drift this family exists to catch: a recorded member that is
    in neither tree. Nothing about the refusals above may turn that into a
    skip, or the family would stop reporting the deletion of a moved member
    altogether."""
    root = _shed_fixture(tmp_path)
    _point_carve_at(monkeypatch, root)
    monkeypatch.setattr(carved_reach, "_rows", lambda: {
        MOVED: {"source_path": MOVED, "disposition": "moved_verbatim",
                "destination": "leg_spec",
                "destination_path": "contracts/never-arrived.yaml"}})

    outcome = check_repo(REPO, root, RealGit())

    assert not isinstance(outcome, Skip), (
        f"the leg answered; that is not a skip — got {outcome!r}")
    assert [f.rule for f in outcome] == [
        f"inventory member is absent at HEAD but recorded in {BUNDLE_WT!r}"], (
        "a readable leg that does not carry the member is the absence arm, "
        f"unchanged — got {[f.rule for f in outcome]}")
    assert outcome[0].severity == ERROR


def test_an_unreadable_leg_does_not_discard_the_members_already_compared(
        tmp_path, monkeypatch):
    """A LATE SKIP MUST NOT TAKE THE EARLIER FINDINGS WITH IT (`#1048` round 2,
    the `#766` carrying-skip precedent).

    Members are compared in sorted order, so `contracts/kept.yaml` is graded —
    and found drifted — before `contracts/moved.schema.yaml` sends the whole
    repository to a skip. A bare `Skip` there discards a real, established
    finding about a normative member BECAUSE A LATER MEMBER could not be
    looked up: a second verdict about the release read off the same fact about
    the machine."""
    root = _shed_fixture(tmp_path, drifting=(KEPT,))
    side = _side_clone(tmp_path, root, "side")
    assert list((side / "leg").iterdir()) == [], (
        "the fixture must reproduce an UNINITIALIZED leg")

    _point_carve_at(monkeypatch, side)
    outcome = check_repo(REPO, side, RealGit())

    assert isinstance(outcome, Skip), "the leg is unreadable, so: a skip"
    assert "leg_spec" in outcome.reason
    carried = list(getattr(outcome, "findings", ()))
    assert [(f.path, f.severity) for f in carried] == [(KEPT, ERROR)], (
        "the drift established BEFORE the unreadable member must ride out on "
        f"the skip — got {[(f.path, f.severity) for f in carried]}")
    assert "bytes differ from the digest" in carried[0].rule

    class Ctx:
        repo_paths = {REPO: side}
        git = RealGit()

    from doc_health.release_inventory import fam_release_inventory_drift
    family = fam_release_inventory_drift(Ctx())
    assert isinstance(family, Skip), (
        "one repository in scope and it skipped, so the family skips — the "
        "shape `--single-repo` and the cut-time gate both see")
    assert [f.path for f in getattr(family, "findings", ())] == [KEPT], (
        "and what that repository DID establish travels with it, which is "
        "what `runner.run_suite` reports beside the skip")


def test_a_carrying_skip_is_reported_WITH_its_findings_not_instead_of_them(
        monkeypatch):
    """THE MIXED RUN, where the family returns findings rather than a skip.

    The per-repository `info` row is the family's own promise that a skipped
    repository is "reported, not silently omitted"; a carrying skip makes that
    row's own text false if it still says the release surface WAS NOT
    EVALUATED, because part of it was — and the findings are printed right
    beside it. Asserted on `fam_` directly, with `check_repo` stubbed, because
    the branch is about what the FAMILY does with a partial skip rather than
    about how one is produced (the arms above prove that)."""
    from doc_health import PartialSkip
    from doc_health.release_inventory import fam_release_inventory_drift

    established = Finding(ERROR, FAMILY, "skipping", "contracts/a.yaml",
                          "bytes differ from the digest 'contract-v0.0' "
                          "records", "cut a release")
    outcomes = {"skipping": PartialSkip(FAMILY, "skipping: the leg is "
                                        "unreadable here", (established,)),
                "askable": []}
    monkeypatch.setattr(release_inventory, "check_repo",
                        lambda repo, path, git: outcomes[repo])

    class Ctx:
        repo_paths = {"askable": Path("askable"), "skipping": Path("skipping")}
        git = FakeGit()

    out = fam_release_inventory_drift(Ctx())

    assert established in out, (
        "the finding the skipping repository established is reported")
    notices = [f for f in out if f.rule.startswith("not checked:")]
    assert len(notices) == 1 and notices[0].severity == INFO
    assert "reported beside it rather than discarded with it" in \
        notices[0].action, (
        "and the notice says the repository was PARTLY evaluated, because "
        f"'not evaluated' would be false of it — got {notices[0].action!r}")


# -------------------------------------------- round 3: the probe asks about
#                                               the path the read asked about
#
# `git ls-tree` resolves its pathspec RELATIVE TO THE CURRENT PREFIX unless
# `--full-tree` is given; `git rev-parse <revision>:<path>` is relative to the
# ROOT of the tree always. `_tree_entry_absent` exists to say which of two
# facts a `rev-parse` that answered nothing carries, so under any non-empty
# prefix it was answering about a DIFFERENT path than the read it arbitrates —
# and its "exit 0 and no output" answer, the one shape it treats as git's
# unambiguous "no such entry", is exactly what a prefixed pathspec that matches
# nothing produces for an entry that IS there.


def test_the_tree_probe_answers_from_the_ROOT_of_the_tree_not_the_prefix(
        tmp_path):
    """THE PREFIX SHAPE, MEASURED ON A MODULE STORE (Copilot on PR #1051,
    `carved_reach.py:746`).

    A module store is where the walk reads every level past the first, and it
    is a git directory with a `core.worktree` of its own. Where that worktree
    resolves to a directory CONTAINING the store — a relocated superproject, a
    store reached through a path git computes a prefix for — `ls-tree` prepends
    that prefix to the pathspec and quietly matches nothing."""
    root = _shed_fixture(tmp_path)
    worktree = tmp_path / "worktree"
    _git_in(root, "worktree", "add", "--quiet", "--detach", str(worktree),
            "HEAD")
    store = carved_reach._leg_object_store(worktree, "leg")
    assert store == root / ".git" / "modules" / "leg"
    # The shape itself: a store whose own work tree contains it, which is what
    # makes git compute a prefix for the directory the reader points it at.
    _git_in(store, "config", "core.worktree", str(root))
    prefix = carved_reach._git_text(store, "rev-parse", "--show-prefix")
    assert prefix, ("the fixture must reproduce a NON-EMPTY prefix, or this "
                    "test proves nothing about prefix independence")

    pinned = _gitlink(worktree, "HEAD", "leg")
    old_form = carved_reach._git_run(store, "ls-tree", pinned, "--", "spec")
    assert old_form.returncode == 0 and not old_form.stdout.strip(), (
        "MEASURED: the prefix-relative form answers EXIT 0 AND NOTHING — git's "
        "own unambiguous 'this tree carries no such entry' — for the `spec` "
        "gitlink this very commit records, which is the phantom absence "
        "`_tree_entry_absent` exists to refuse")

    absent, said = carved_reach._tree_entry_absent(store, pinned, "spec")
    assert absent is False, (
        "the tree DOES carry `spec` at that commit, so the probe may not "
        f"report it absent — got ({absent!r}, {said!r})")
    assert carved_reach._tree_entry_absent(
        store, pinned, "no-such-entry") == (True, ""), (
        "...and a genuine absence read from the SAME prefixed store is still "
        "the answer it always was, which is what keeps this a fix rather than "
        "a blanket refusal")


def test_the_tree_probe_reads_a_segment_as_a_NAME_not_as_pathspec_magic(
        tmp_path):
    """`:(literal)` comes with `--full-tree` for the reason `content.py` pairs
    them. MEASURED, git 2.43.0: `ls-tree --full-tree HEAD -- :!leg` exits 128
    (`pathspec magic not supported by this command: 'exclude'`) while
    `:(literal):!leg` exits 0 — a segment whose name begins with `:` is read as
    MAGIC otherwise, and this probe would report git's parse refusal as the
    leg's tree being unreadable."""
    root = _shed_fixture(tmp_path)
    assert carved_reach._tree_entry_absent(root, "HEAD", ":!leg") == (True, ""), (
        "a segment spelled `:!leg` is a NAME this tree does not carry, which "
        "is an answer; parsed as exclusion magic git refuses outright and the "
        "probe reports an unreadable tree instead")


# ------------------------------------ round 3: evaluated is not established
#
# `check_repo` can stop being able to ask partway through a repository's
# members. What the members BEFORE that point established rides out on the skip
# (round 2) — but a member that was compared and MATCHED establishes nothing,
# and reading "was anything evaluated" off "was anything established" put the
# family's own `info` line over such a repository saying its release surface
# WAS NOT EVALUATED, when most of it had just been evaluated and found clean.


def test_members_that_MATCHED_before_the_unreadable_one_still_count_as_evaluated(
        tmp_path, monkeypatch):
    """THE ORDINARY CASE, and the one the wording was wrong for.

    `contracts/kept.yaml` sorts first, is in this repository's own tree, and
    its digest is recorded correctly — so it is compared, it matches, and it
    contributes NOTHING to carry before `contracts/moved.schema.yaml` sends the
    repository to a skip."""
    root = _shed_fixture(tmp_path)
    side = _side_clone(tmp_path, root, "side")
    _point_carve_at(monkeypatch, side)

    outcome = check_repo(REPO, side, RealGit())

    assert isinstance(outcome, PartialSkip), (
        "one member was compared before the leg went unreadable, so this is "
        f"the partial form even though it carries nothing — got {outcome!r}")
    assert getattr(outcome, "findings", ()) == (), (
        "and it carries nothing, which is the whole point: the evaluated "
        "member MATCHED")


def test_a_repository_whose_FIRST_member_is_unreadable_evaluated_nothing(
        tmp_path, monkeypatch):
    """THE OTHER SIDE, unchanged down to its type — a NEGATIVE CONTROL, and it
    passes against the reader this round replaces on purpose.

    An inventory recording the moved member ALONE makes the unreadable one the
    first thing compared, so nothing was evaluated and the plain `Skip` — and
    the wording that says the surface was not evaluated — is exactly right.
    Without this, `_skip` answering `PartialSkip` unconditionally would satisfy
    every other arm above."""
    root = _shed_fixture(tmp_path, members=(MOVED,))
    side = _side_clone(tmp_path, root, "side-first")
    _point_carve_at(monkeypatch, side)

    outcome = check_repo(REPO, side, RealGit())

    assert isinstance(outcome, Skip) and not isinstance(outcome, PartialSkip), (
        "nothing was asked of this repository at all, so the skip is the plain "
        f"one it has always been — got {type(outcome).__name__}")


def test_a_partly_evaluated_repository_is_not_reported_as_UNEVALUATED(
        monkeypatch):
    """THE LINE THE READER ACTUALLY SEES, asserted on `fam_` with `check_repo`
    stubbed — the same separation `test_a_carrying_skip_is_reported_WITH_its_
    findings_not_instead_of_them` makes, for the same reason: the branch under
    test is what the FAMILY does with a partial skip, and the two arms above
    prove how one is produced.

    A second, askable repository is required or the family collapses to an
    all-skip and never emits a per-repository row at all."""
    from doc_health.release_inventory import fam_release_inventory_drift

    def _rows_for(outcome):
        monkeypatch.setattr(release_inventory, "check_repo",
                            lambda repo, path, git: (
                                outcome if repo == "skipping" else []))

        class Ctx:
            repo_paths = {"askable": Path("askable"),
                          "skipping": Path("skipping")}
            git = FakeGit()

        return [f for f in fam_release_inventory_drift(Ctx())
                if f.rule.startswith("not checked:")]

    reason = "skipping: the leg is unreadable here"
    partly = _rows_for(PartialSkip(FAMILY, reason, ()))
    assert len(partly) == 1 and partly[0].severity == INFO
    assert partly[0].action == release_inventory._PARTLY_EVALUATED_ACTION, (
        "members were compared and merely matched, so 'was not evaluated' is "
        f"false of this repository — got {partly[0].action!r}")

    unevaluated = _rows_for(Skip(FAMILY, reason))
    assert len(unevaluated) == 1
    assert unevaluated[0].action == release_inventory._NOT_EVALUATED_ACTION, (
        "and a repository nothing was asked of still takes the wording it "
        f"always had — got {unevaluated[0].action!r}")


# ------------------------------------------- round 5: one leg, one tree read
#
# `_shed_member` ran the leg's full recursive `ls-tree` once per MOVED member
# (Copilot on PR #1051, `release_inventory.py:325`) — four times, for the
# normal openxFactory bundle, every one of them resolving to the SAME
# `(leg_repo, leg_commit)`. `check_repo` now creates one mode-map cache before
# its member loop and `_shed_member` consults it before calling
# `git.tree_modes` again.

def test_two_moved_members_on_one_leg_call_tree_modes_once(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Two inventory members resolving to ONE pinned leg must produce exactly
    ONE `tree_modes` call, counted through a `FakeGit` subclass that
    INSTRUMENTS the real method rather than replacing it — so this remains a
    test of the call count, not of a second, hand-rolled `tree_modes`.

    `carved_reach.shed_commit_object` is stubbed rather than driven through a
    real submodule fixture (the shape `test_a_linked_worktree_reads_the_same_
    release_surface` and its neighbours use above): what this test measures is
    `_shed_member`'s OWN call discipline once a leg is located, which is a
    property of `release_inventory.py` and not of `carved_reach`'s gitlink
    walk — the two are already tested separately, and conflating them here
    would make a failure of either look like a failure of both.
    """
    member_a = "contracts/schemas/moved-a.schema.yaml"
    member_b = "contracts/schemas/moved-b.schema.yaml"
    data_a, data_b = b"kind: moved-a\n", b"kind: moved-b\n"
    mode = "100644"

    repo_path = tmp_path / "checkout"
    repo_path.mkdir()
    monkeypatch.setattr(carved_reach, "REPO_ROOT", repo_path)

    leg_repo = tmp_path / "leg"
    leg_commit = "c" * 40
    leg_paths = {member_a: "a.schema.yaml", member_b: "b.schema.yaml"}

    def fake_shed_commit_object(commit: str, path: str):
        assert commit == "HEAD", commit
        return leg_repo, leg_commit, leg_paths[path]

    monkeypatch.setattr(carved_reach, "shed_commit_object",
                        fake_shed_commit_object)

    tree_modes_calls: list[tuple[Path, str]] = []

    class CountingGit(FakeGit):
        def tree_modes(self, repo: Path, commit: str):
            tree_modes_calls.append((repo, commit))
            return super().tree_modes(repo, commit)

    manifest_bytes = f"contract_bundle_version: {BUNDLE}\n".encode()
    members = {member_a: (data_a, mode), member_b: (data_b, mode),
              MANIFEST: (manifest_bytes, mode)}
    git = CountingGit(
        blobs={
            (leg_repo.name, "a.schema.yaml"): data_a,
            (leg_repo.name, "b.schema.yaml"): data_b,
            (repo_path.name, MANIFEST): manifest_bytes,
            (repo_path.name, INV): _inventory(members),
        },
        modes={
            (leg_repo.name, "a.schema.yaml"): mode,
            (leg_repo.name, "b.schema.yaml"): mode,
            (repo_path.name, MANIFEST): mode,
        })

    findings = check_repo(repo_path.name, repo_path, git)

    assert findings == [], findings
    leg_calls = [c for c in tree_modes_calls if c == (leg_repo, leg_commit)]
    assert len(leg_calls) == 1, (
        f"two members sharing one leg must produce ONE `tree_modes` call, "
        f"got {tree_modes_calls}")
