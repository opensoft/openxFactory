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
