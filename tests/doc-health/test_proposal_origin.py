"""Fifteenth deterministic family (add-proposal-origin-contract task 4.4):
proposal-origin checks plus the proposal-support gate wiring.

Deterministic fixtures built under tmp_path; the required matrix from task
4.4: staged origin accepted and copied into the manifest; ad-hoc accepted
with complete provenance; missing origin rejected; both kinds rejected;
staged id/path/header mismatch rejected; active-to-archive identity
preserved (manifest disagreement is contested mutation evidence); the
archived bootstrap exception resolvable via the migration record; and
backfilled origins validated against migration evidence without fabricated
history (pre-contract legacy reports WARNING, never ERROR).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from doc_health import ERROR, WARNING, CONTESTED  # noqa: E402
from doc_health import proposal_origin as po  # noqa: E402

_SUPPORT_SPEC = importlib.util.spec_from_file_location(
    "proposal_support_gate", REPO_ROOT / "scripts" / "proposal-support.py")
support = importlib.util.module_from_spec(_SUPPORT_SPEC)
sys.modules[_SUPPORT_SPEC.name] = support
_SUPPORT_SPEC.loader.exec_module(support)


def _change(tmp_path, name, packet=None, manifest=None, archived=False):
    base = tmp_path / "openspec" / "changes"
    if archived:
        base = base / "archive"
    d = base / name
    d.mkdir(parents=True)
    (d / "proposal.md").write_text("# p\n")
    if packet is not None:
        (d / ".openspec.yaml").write_text(packet)
    if manifest is not None:
        if archived:
            (d / "supporting-docs.manifest.yaml").write_text(
                yaml.safe_dump(manifest))
        else:
            (d / "supporting-docs").mkdir()
            (d / "supporting-docs" / "manifest.yaml").write_text(
                yaml.safe_dump(manifest))
    return d


STAGED = """schema: spec-driven
created: 2026-08-10
origin:
  kind: staged
  id: repo:staging:topic-a
  path: ideation/staging/topic-a
"""

ADHOC = """schema: spec-driven
created: 2026-08-10
origin:
  kind: ad_hoc
  id: repo:adhoc:2026-08-10-topic
  reason: deliberate exception
  approved_by: Brett
  approved_on: 2026-08-10
"""


def test_staged_origin_accepted(tmp_path):
    d = _change(tmp_path, "add-a", STAGED,
                manifest={"origin": {"kind": "staged",
                                     "id": "repo:staging:topic-a",
                                     "path": "ideation/staging/topic-a"}})
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_adhoc_origin_accepted_with_provenance(tmp_path):
    d = _change(tmp_path, "add-b", ADHOC)
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_missing_origin_post_contract_is_error(tmp_path):
    d = _change(tmp_path, "add-c",
                "schema: spec-driven\ncreated: 2026-09-01\n")
    [f] = po.check_change("r", tmp_path, d, frozenset(), False)
    assert f.severity == ERROR and "no origin declaration" in f.rule
    # PIN (commissioned 2026-08-27, after `promotion_fidelity._ACTION` was
    # mutated and 85 tests stayed green — no doc-health family's action line
    # was pinned anywhere). An action line is operator guidance rendered in
    # every ranked-plan row; nothing else in this repository notices it
    # changing, so each family gets one verbatim pin in its own suite.
    assert f.action == (
        "declare `origin:` in .openspec.yaml (staged or ad_hoc per the "
        "document-lifecycle origin requirement)")


def test_missing_origin_pre_contract_is_warning(tmp_path):
    d = _change(tmp_path, "2026-07-01-add-old", None, archived=True)
    [f] = po.check_change("r", tmp_path, d, frozenset(), True)
    assert f.severity == WARNING and "pre-contract legacy" in f.rule


def test_both_kinds_rejected(tmp_path):
    packet = STAGED.replace("id: repo:staging:topic-a",
                            "id: repo:adhoc:2026-08-10-topic")
    d = _change(tmp_path, "add-d", packet)
    rules = [f.rule for f in po.check_change("r", tmp_path, d,
                                             frozenset(), False)]
    assert any("id and kind disagree" in r for r in rules)


def test_malformed_id_rejected(tmp_path):
    packet = STAGED.replace("repo:staging:topic-a", "not-a-durable-id")
    d = _change(tmp_path, "add-e", packet)
    rules = [f.rule for f in po.check_change("r", tmp_path, d,
                                             frozenset(), False)]
    assert any("malformed durable origin id" in r for r in rules)


def test_adhoc_incomplete_provenance_rejected(tmp_path):
    packet = ADHOC.replace("  approved_by: Brett\n", "")
    d = _change(tmp_path, "add-f", packet)
    rules = [f.rule for f in po.check_change("r", tmp_path, d,
                                             frozenset(), False)]
    assert any("lacks required `approved_by`" in r for r in rules)


def test_manifest_disagreement_is_contested_mutation(tmp_path):
    d = _change(tmp_path, "2026-08-10-add-g", STAGED,
                manifest={"origin": {"kind": "staged",
                                     "id": "repo:staging:OTHER",
                                     "path": "ideation/staging/topic-a"}},
                archived=True)
    findings = po.check_change("r", tmp_path, d, frozenset(), True)
    mism = [f for f in findings if "disagrees with the packet" in f.rule]
    assert mism and mism[0].resolution == CONTESTED
    assert "post-ratification mutation" in mism[0].rule


def test_staging_header_linkage_checked_for_active(tmp_path):
    folder = tmp_path / "ideation" / "staging" / "topic-a"
    folder.mkdir(parents=True)
    (folder / "topic-a.md").write_text("Staging ID: repo:staging:DIFFERENT\n")
    d = _change(tmp_path, "add-h", STAGED)
    rules = [f.rule for f in po.check_change("r", tmp_path, d,
                                             frozenset(), False)]
    assert any("no document carries `Staging ID:" in r for r in rules)


# BOTH SPELLINGS OF ONE RECORDED PATH. `str(PurePath)` wrote the second on a
# Windows checkout until PR #221 put the writer into POSIX, and fixing a writer
# cannot reach the records already on disk — so both must resolve here.
_SPELLINGS = ["ideation/staging/topic-a", "ideation\\staging\\topic-a"]


def _staged_packet(declared: str) -> str:
    return STAGED.replace("path: ideation/staging/topic-a",
                          f"path: {declared}")


@pytest.mark.parametrize("declared", _SPELLINGS)
def test_the_staging_header_check_runs_on_either_spelling(tmp_path, declared):
    """THE SILENT HALF, and the reason this is worth a test at all.

    A backslash-spelled origin path makes `Path(repo) / path` a directory that
    does not exist, so `_staging_header_matches` returns None and the linkage
    check SKIPS. Nothing is reported, nothing looks wrong, and a change whose
    staging folder really has lost its `Staging ID:` linkage sails through. A
    check that silently does not run is worse than one that fails."""
    folder = tmp_path / "ideation" / "staging" / "topic-a"
    folder.mkdir(parents=True)
    (folder / "topic-a.md").write_text("Staging ID: repo:staging:DIFFERENT\n")
    d = _change(tmp_path, "add-bs", _staged_packet(declared))
    rules = [f.rule for f in po.check_change("r", tmp_path, d,
                                             frozenset(), False)]
    assert any("no document carries `Staging ID:" in r for r in rules)


@pytest.mark.parametrize("declared", _SPELLINGS)
def test_intact_linkage_reports_nothing_on_either_spelling(tmp_path, declared):
    """Running is not the same as firing: the check must reach the folder AND
    come back clean when the linkage is intact."""
    folder = tmp_path / "ideation" / "staging" / "topic-a"
    folder.mkdir(parents=True)
    (folder / "topic-a.md").write_text("Staging ID: repo:staging:topic-a\n")
    d = _change(tmp_path, "add-bs-ok", _staged_packet(declared))
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


@pytest.mark.parametrize("declared", _SPELLINGS)
def test_a_vanished_staging_folder_stays_legal_history_either_way(
        tmp_path, declared):
    """The skip that is CORRECT stays a skip. A folder that disappeared after
    the transition is legal history, and tolerating the other spelling must not
    turn that silence into a finding — the normalization makes the check
    resolve, not the check accuse."""
    d = _change(tmp_path, "add-bs-gone", _staged_packet(declared))
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


@pytest.mark.parametrize("declared", _SPELLINGS)
def test_the_recorded_revision_check_resolves_either_spelling(
        tmp_path, declared):
    """THE LOUD HALF at the other site. `git ls-tree` matches no entry for a
    backslash-spelled path, so sound provenance reports as
    `staged origin path ... does not resolve at the recorded source revision`
    — a false ERROR against a folder that is present in the very commit
    named."""
    import subprocess
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    folder = tmp_path / "ideation" / "staging" / "topic-a"
    folder.mkdir(parents=True)
    (folder / "topic-a.md").write_text("Staging ID: repo:staging:topic-a\n")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "-c", "user.name=T", "-c",
         "user.email=t@example.invalid", "commit", "-qm", "fixture"],
        check=True)
    revision = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    d = _change(tmp_path, "add-bs-rev", _staged_packet(declared),
                manifest={"source_revision": revision,
                          "origin": {"kind": "staged",
                                     "id": "repo:staging:topic-a",
                                     "path": declared}})
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_vanished_staging_folder_is_legal_history(tmp_path):
    d = _change(tmp_path, "add-i", STAGED)
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_migrated_backfill_validated_not_reported(tmp_path):
    d = _change(tmp_path, "2026-07-01-add-old", ADHOC.replace(
        "repo:adhoc:2026-08-10-topic", "repo:adhoc:old-loose-grammar"),
        archived=True)
    migrated = frozenset({"2026-07-01-add-old"})
    assert po.check_change("r", tmp_path, d, migrated, True) == []


def test_migration_recorded_but_removed_is_contested(tmp_path):
    d = _change(tmp_path, "2026-07-01-add-old", None, archived=True)
    migrated = frozenset({"2026-07-01-add-old"})
    [f] = po.check_change("r", tmp_path, d, migrated, True)
    assert f.severity == ERROR and f.resolution == CONTESTED
    assert "removed after the fact" in f.rule


def test_unparseable_packet_is_distinct_finding(tmp_path):
    d = _change(tmp_path, "add-j",
                'origin:\n  reason: broken: colon\n')
    [f] = po.check_change("r", tmp_path, d, frozenset(), False)
    assert "does not parse" in f.rule


def test_migration_records_parsed_from_evidence(tmp_path):
    change = tmp_path / "openspec" / "changes" / \
        "add-proposal-origin-contract"
    change.mkdir(parents=True)
    (change / "migration-evidence.md").write_text(
        "**`archive/2026-07-09-add-x`** —\nclassification: `ad_hoc`. "
        "Applied.\n\n**`2026-07-10-add-y`** —\n")
    got = po.migration_records(tmp_path)
    assert got == frozenset({"2026-07-09-add-x", "2026-07-10-add-y"})


# --- the proposal-support gate wiring (tasks 2.2/2.3/4.3) -----------------


def test_gate_rejects_missing_origin_strict(tmp_path):
    d = _change(tmp_path, "add-k",
                "schema: spec-driven\ncreated: 2026-09-01\n")
    errors = support.origin_errors(tmp_path, d, strict=True)
    assert errors and "no origin declaration" in errors[0]
    assert support.origin_errors(tmp_path, d, strict=False) == []


def test_gate_checks_manifest_agreement(tmp_path):
    d = _change(tmp_path, "add-l", STAGED)
    manifest = {"origin": {"kind": "staged", "id": "repo:staging:topic-a",
                           "path": "ideation/staging/ELSEWHERE"}}
    errors = support.origin_errors(tmp_path, d, strict=False,
                                   manifest=manifest)
    assert errors and "immutable after ratification" in errors[0]


@pytest.mark.parametrize("declared", _SPELLINGS)
def test_the_gates_own_coherence_check_runs_on_either_spelling(
        tmp_path, declared):
    """`origin_errors`' strict arm has the SAME silent-skip failure as the
    family's linkage check, and PR #221 normalized it without a test. It joins
    the recorded path to the repo root and reads the folder's `Staging ID:`; a
    spelling it cannot resolve makes `staging_header_id` return None and the
    disagreement go unreported. Pinned here, on the funnel this module now
    states once."""
    folder = tmp_path / "ideation" / "staging" / "topic-a"
    folder.mkdir(parents=True)
    (folder / "topic-a.md").write_text(
        "# T\n\nStatus: staged\nStaging ID: repo:staging:DIFFERENT\n")
    d = _change(tmp_path, "add-bs-gate", _staged_packet(declared))
    errors = support.origin_errors(tmp_path, d, strict=True)
    assert any("does not equal the declared origin id" in e for e in errors)


def test_write_origin_block_refuses_overwrite(tmp_path):
    d = _change(tmp_path, "add-m", STAGED)
    with pytest.raises(support.SupportError):
        support.write_origin_block(
            d, {"kind": "staged", "id": "repo:staging:x",
                "path": "ideation/staging/x"}, "2026-08-10")


def test_write_origin_block_creates_and_parses(tmp_path):
    d = _change(tmp_path, "add-n", None)
    support.write_origin_block(
        d, {"kind": "ad_hoc", "id": "repo:adhoc:2026-08-10-n",
            "reason": "explicit exception", "approved_by": "Brett",
            "approved_on": "2026-08-10"}, "2026-08-10")
    packet = yaml.safe_load((d / ".openspec.yaml").read_text())
    assert packet["origin"]["kind"] == "ad_hoc"
    assert support.origin_errors(tmp_path, d, strict=True) == []


def test_transition_writes_origin_and_manifest_repeats_it(tmp_path):
    import subprocess
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    topic = tmp_path / "ideation" / "staging" / "topic-a"
    topic.mkdir(parents=True)
    (topic / "topic-a.md").write_text(
        "# Staged: Topic A\n\nStatus: staged\n"
        f"Staging ID: {tmp_path.name}:staging:topic-a\n\nbody\n")
    d = _change(tmp_path, "add-o", None)
    manifest = support.transition(
        tmp_path, "add-o", "ideation/staging/topic-a", [], None,
        "2026-08-10", False, True)
    assert manifest["origin"]["kind"] == "staged"
    assert manifest["origin"]["id"] == f"{tmp_path.name}:staging:topic-a"
    packet = yaml.safe_load((d / ".openspec.yaml").read_text())
    assert packet["origin"] == manifest["origin"]
    assert support.origin_errors(tmp_path, d, strict=True,
                                 manifest=manifest) == []
