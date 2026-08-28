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
import subprocess
from pathlib import Path

import pytest

from conftest import FakeGit  # noqa: F401  (sys.path side effect)

from doc_health import ERROR, INFO, Skip
from doc_health.corpus import RealGit
from doc_health.families import FAMILIES, FAMILY_RESOLUTION
from doc_health.release_inventory import (
    EDITORIAL, FAMILY, check_repo, inventory_path_for, parse_declared_bundle,
    parse_inventory,
)

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
