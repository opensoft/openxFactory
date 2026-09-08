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

`add-drafted-proposal-origin` (issue #318) adds the UNAPPROVED state and its
own matrix, in both directions: the lawful draft reports nothing, the same
packet at `Status: ratified` reports a `contested` ERROR, a half-declared
drafting pair is its own finding, an origin declaring neither state says so
once, and the approval pair is still required in full wherever approval is
claimed. The fixtures are `tmp_path` packets built by `_change` — this
family's own fixture idiom since it was written, because what it reads is
`.openspec.yaml` text and a `Status:` line rather than a corpus of governed
documents.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from doc_health import ERROR, WARNING, CONTESTED  # noqa: E402
from doc_health import proposal_origin as po  # noqa: E402
from doc_health.promotion_fidelity import (  # noqa: E402
    PRE_RATIFICATION, RATIFIED_OR_BEYOND)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from action_pins import assert_actions_pinned, harvest_static  # noqa: E402

_SUPPORT_SPEC = importlib.util.spec_from_file_location(
    "proposal_support_gate", REPO_ROOT / "scripts" / "proposal-support.py")
support = importlib.util.module_from_spec(_SUPPORT_SPEC)
sys.modules[_SUPPORT_SPEC.name] = support
_SUPPORT_SPEC.loader.exec_module(support)


def _change(tmp_path, name, packet=None, manifest=None, archived=False,
            status=None):
    """`status`, when given, writes the packet's own `Status:` header — the
    ONE input class 7 reads. Absent it the proposal carries no header at all,
    which is what every test written before `add-drafted-proposal-origin`
    assumed and what class 7 must stay silent on."""
    base = tmp_path / "openspec" / "changes"
    if archived:
        base = base / "archive"
    d = base / name
    d.mkdir(parents=True)
    (d / "proposal.md").write_text(
        "# p\n" if status is None else f"# p\n\nStatus: {status}\n")
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


# The UNAPPROVED state (`add-drafted-proposal-origin`): the same `ad_hoc`
# kind and the same durable id as `ADHOC` — that is the whole point, the
# identity does not move when the approval lands — with the drafting pair
# where the approval pair will go.
DRAFTED = """schema: spec-driven
created: 2026-08-10
origin:
  kind: ad_hoc
  id: repo:adhoc:2026-08-10-topic
  reason: drafted under a scout-and-draft assignment, not yet approved
  proposed_by: A Session
  proposed_on: 2026-08-10
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


# --- the UNAPPROVED state (add-drafted-proposal-origin, issue #318) -------
#
# THE STATE HAD NO LAWFUL SHAPE AT ALL before this change, which is why the
# matrix below is worth stating in full rather than as one happy-path
# assertion: an `ad_hoc` origin without `approved_on` was an error, no origin
# block was an error, and the only remaining moves were to approve the change,
# delete the draft, or invent a date — the last being the exact defect this
# family exists to catch.


def test_an_unapproved_draft_reports_nothing(tmp_path):
    """PROPERTY (a). The whole point of the change: expressible AND quiet."""
    d = _change(tmp_path, "add-draft", DRAFTED, status="draft")
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_an_unapproved_draft_with_no_status_header_reports_nothing(tmp_path):
    """A packet whose `Status:` is missing entirely is `fam_status_validity`'s
    finding, not this family's — and class 7 cannot read a claim that is not
    there, so it must not invent one."""
    d = _change(tmp_path, "add-draft-nostatus", DRAFTED)
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


@pytest.mark.parametrize("standing", sorted(PRE_RATIFICATION))
def test_the_state_is_lawful_at_every_pre_ratification_standing(
        tmp_path, standing):
    d = _change(tmp_path, f"add-draft-{standing}", DRAFTED, status=standing)
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


@pytest.mark.parametrize("standing", sorted(RATIFIED_OR_BEYOND))
def test_a_status_claiming_ratification_over_an_unapproved_origin_is_error(
        tmp_path, standing):
    """PROPERTY (b), over EVERY standing at or beyond ratification rather than
    over `ratified` alone — a packet that reached `standard` or `superseded`
    without its approval ever being recorded is the same defect one stage
    later, and keying on the single word `ratified` would let it through.

    `contested`, and the resolution class is the argued half: resolving this
    finding either TRANSCRIBES an approval act that happened or WITHDRAWS a
    status claim that should not have been made. Inventing the date is the
    third option, it is the defect, and a mechanical class would invite it."""
    d = _change(tmp_path, f"add-claim-{standing}", DRAFTED, status=standing)
    [f] = po.check_change("r", tmp_path, d, frozenset(), False)
    assert f.severity == ERROR and f.resolution == CONTESTED
    assert f"declares `Status: {standing}`" in f.rule
    assert "approval MUST appear when the status claims it" in f.rule


def test_an_approved_origin_at_ratified_status_reports_nothing(tmp_path):
    """The other direction of the same rule: approval PRESENT and a status
    claiming it is the ordinary lawful case, and it must stay quiet."""
    d = _change(tmp_path, "add-approved", ADHOC, status="ratified")
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_approval_arriving_beside_the_drafting_record_is_lawful(tmp_path):
    """APPROVAL IS AN ADDITION, NOT A REWRITE — the property the encoding was
    chosen for. The identity (`kind`, `id`) is byte-identical to the drafted
    packet's, so the support manifest that repeats it never comes to disagree,
    and the drafting record survives beside the approval rather than being
    deleted to make room for it."""
    packet = DRAFTED + "  approved_by: Brett\n  approved_on: 2026-09-03\n"
    d = _change(tmp_path, "add-approved-later", packet, status="ratified")
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_the_unapproved_state_is_declared_never_inferred_from_silence(
        tmp_path):
    """A packet cannot buy the lenient treatment by leaving fields out. An
    origin carrying only `reason` has declared NO provenance state, and at
    `Status: ratified` it gets the missing-provenance finding — never class
    7's, which reports on a state this packet never claimed."""
    packet = ADHOC.replace("  approved_by: Brett\n", "").replace(
        "  approved_on: 2026-08-10\n", "")
    d = _change(tmp_path, "add-silent", packet, status="ratified")
    [f] = po.check_change("r", tmp_path, d, frozenset(), False)
    assert f.severity == ERROR
    assert "declares no provenance state" in f.rule
    assert "approval MUST appear" not in f.rule


def test_an_origin_declaring_neither_state_says_so_once(tmp_path):
    """ONE finding, not one per absent field: nothing has been half-claimed,
    and the remedy is a single choice between two shapes."""
    packet = ADHOC.replace("  approved_by: Brett\n", "").replace(
        "  approved_on: 2026-08-10\n", "")
    d = _change(tmp_path, "add-neither", packet, status="draft")
    findings = po.check_change("r", tmp_path, d, frozenset(), False)
    assert len(findings) == 1
    assert findings[0].action == (
        "record the approval provenance the ad-hoc exception requires, or "
        "declare the unapproved state with `proposed_by` and `proposed_on`")


@pytest.mark.parametrize("missing", po.DRAFTING_FIELDS)
def test_a_half_declared_drafting_pair_is_its_own_finding(tmp_path, missing):
    packet = "".join(line for line in DRAFTED.splitlines(keepends=True)
                     if not line.strip().startswith(f"{missing}:"))
    d = _change(tmp_path, f"add-half-{missing}", packet, status="draft")
    [f] = po.check_change("r", tmp_path, d, frozenset(), False)
    assert f.severity == ERROR
    assert f"drafting origin lacks required `{missing}`" in f.rule


@pytest.mark.parametrize("missing", po.APPROVAL_FIELDS)
def test_a_claimed_approval_still_owes_the_whole_pair(tmp_path, missing):
    """PROPERTY (c). `approved_on` is required for an ad-hoc APPROVAL exactly
    as it was before this change, and so is `approved_by`: an origin that
    claims approval at all owes both, and the drafting state does not weaken
    that by a byte. Nothing already lawful changes shape."""
    packet = "".join(line for line in ADHOC.splitlines(keepends=True)
                     if not line.strip().startswith(f"{missing}:"))
    d = _change(tmp_path, f"add-partial-{missing}", packet, status="draft")
    rules = [f.rule for f in po.check_change("r", tmp_path, d,
                                             frozenset(), False)]
    assert [f"ad-hoc origin lacks required `{missing}`"] == rules


def test_a_drafting_origin_still_owes_its_reason(tmp_path):
    """The state relaxes the APPROVAL pair and nothing else. `reason` is the
    provenance half of an ad-hoc origin, and an unapproved draft has one."""
    packet = DRAFTED.replace(
        "  reason: drafted under a scout-and-draft assignment, "
        "not yet approved\n", "")
    d = _change(tmp_path, "add-draft-noreason", packet, status="draft")
    rules = [f.rule for f in po.check_change("r", tmp_path, d,
                                             frozenset(), False)]
    assert rules == ["ad-hoc origin lacks required `reason`"]


def test_a_staged_origin_at_ratified_status_owes_no_approval(tmp_path):
    """Class 7 is an AD-HOC rule. A staged origin's provenance is the staging
    topic and its transition record; it has never carried an approval pair and
    a ratified staged packet must not start being asked for one."""
    d = _change(tmp_path, "add-staged-ratified", STAGED, status="ratified")
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


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


def test_the_gate_accepts_an_unapproved_draft(tmp_path):
    """PROPERTY (a) AT THE GATE, and it is not decoration: a state the nightly
    family calls lawful while `proposal-support.py verify` rejects it is not a
    lawful state, it is a state with two answers."""
    d = _change(tmp_path, "add-draft-gate", DRAFTED)
    assert support.origin_errors(tmp_path, d, strict=True) == []


def test_the_gate_rejects_a_half_declared_drafting_pair(tmp_path):
    packet = DRAFTED.replace("  proposed_on: 2026-08-10\n", "")
    d = _change(tmp_path, "add-half-gate", packet)
    errors = support.origin_errors(tmp_path, d, strict=True)
    assert any("drafting origin lacks required `proposed_on`" in e
               for e in errors)


def test_the_gate_rejects_an_origin_declaring_neither_state(tmp_path):
    packet = ADHOC.replace("  approved_by: Brett\n", "").replace(
        "  approved_on: 2026-08-10\n", "")
    d = _change(tmp_path, "add-neither-gate", packet)
    errors = support.origin_errors(tmp_path, d, strict=True)
    assert any("declares no provenance state" in e for e in errors)


def test_the_gate_and_the_family_name_the_same_provenance_fields():
    """THE AGREEMENT TEST FOR A DELIBERATE DUPLICATION. The gate copies the
    two field pairs rather than importing them — `proposal-support.py` states
    why beside the copy: `doc_health.proposal_origin` depends on PyYAML and on
    two further package modules, so it fails the "nothing outside the standard
    library" test that earned `doc_health.pin_sentinels` its import, exactly
    as the two id grammars above it are copied for the same reason. A copied
    rule is held by a test or by nothing."""
    assert support.APPROVAL_FIELDS == po.APPROVAL_FIELDS
    assert support.DRAFTING_FIELDS == po.DRAFTING_FIELDS


def test_write_origin_block_writes_the_unapproved_state(tmp_path):
    """EVERY LAWFUL SHAPE HAS A PRODUCER. A state only hand-authorable is a
    state the repository's own writer disagrees with."""
    d = _change(tmp_path, "add-write-draft", None)
    support.write_origin_block(
        d, {"kind": "ad_hoc", "id": "repo:adhoc:2026-09-03-write-draft",
            "reason": "drafted, not approved", "proposed_by": "A Session",
            "proposed_on": "2026-09-03"}, "2026-09-03")
    packet = yaml.safe_load((d / ".openspec.yaml").read_text())
    # `str(...)`, because an unquoted ISO date loads as `datetime.date` — the
    # reason every presence test on these fields, in the family and in the
    # gate alike, goes through `str(value).strip()` rather than comparing to
    # a string or testing truthiness of a raw scalar.
    assert str(packet["origin"]["proposed_on"]) == "2026-09-03"
    assert "approved_on" not in packet["origin"]
    assert support.origin_errors(tmp_path, d, strict=True) == []
    assert po.check_change("r", tmp_path, d, frozenset(), False) == []


def test_write_origin_block_writes_both_pairs_when_both_are_given(tmp_path):
    d = _change(tmp_path, "add-write-both", None)
    support.write_origin_block(
        d, {"kind": "ad_hoc", "id": "repo:adhoc:2026-09-03-write-both",
            "reason": "drafted, then approved", "proposed_by": "A Session",
            "proposed_on": "2026-09-01", "approved_by": "Brett",
            "approved_on": "2026-09-03"}, "2026-09-01")
    origin = yaml.safe_load((d / ".openspec.yaml").read_text())["origin"]
    assert str(origin["proposed_on"]) == "2026-09-01"
    assert str(origin["approved_on"]) == "2026-09-03"


@pytest.mark.parametrize("half", ["proposed_by", "proposed_on",
                                  "approved_by", "approved_on"])
def test_write_origin_block_refuses_a_half_given_pair(tmp_path, half):
    """FOUND BY COPILOT ON PR #619, AND IT WAS A SILENT DROP. The writer wrote
    only pairs it found COMPLETE, so a caller handing it a full approval pair
    and a lone `proposed_by` got a block with the stray field discarded and no
    word said — a record that looks complete, produced by the writer whose own
    gate reports a half-declared pair as a defect. Refused now, in both
    directions and at either field of either pair."""
    origin = {"kind": "ad_hoc", "id": "repo:adhoc:2026-09-03-half",
              "reason": "one pair complete, the other half-given"}
    complete = ("proposed", "approved")[half.startswith("proposed")]
    origin[f"{complete}_by"] = "Someone"
    origin[f"{complete}_on"] = "2026-09-03"
    origin[half] = "a lone half"
    d = _change(tmp_path, f"add-write-half-{half}", None)
    with pytest.raises(support.SupportError) as raised:
        support.write_origin_block(d, origin, "2026-09-03")
    assert half in str(raised.value)
    assert not (d / ".openspec.yaml").is_file()


def test_write_origin_block_refuses_an_ad_hoc_origin_with_neither_pair(
        tmp_path):
    d = _change(tmp_path, "add-write-neither", None)
    with pytest.raises(support.SupportError):
        support.write_origin_block(
            d, {"kind": "ad_hoc", "id": "repo:adhoc:2026-09-03-x",
                "reason": "no provenance state at all"}, "2026-09-03")


def test_every_action_string_the_proposal_origin_family_can_emit_is_pinned_verbatim(
        tmp_path):
    """`fam_proposal_origin`'s `check_change` raises ELEVEN distinct action
    strings across its five finding classes (module docstring). `#448`
    (`cadc05ec`) pinned one (`test_missing_origin_post_contract_is_error`,
    above). Steward follow-up (Brett, 2026-08-28) widens that to the whole
    set, table-driven.

    ALL ELEVEN are pinned BEHAVIOURALLY, reusing this suite's own `_change`
    helper and `STAGED`/`ADHOC` packet constants exactly as the existing
    per-defect tests above use them — one small `tmp_path` change directory
    per finding class, `po.check_change(...)` called directly (its own
    signature, not through a `Context`/family-registry indirection, exactly
    as every other test in this file already calls it) and the resulting
    actions unioned. The git-backed `source_revision` check (class
    staged-origin-unresolvable, mismatch arm) needs a REAL git repository —
    a real `git init`/commit under its own `tmp_path`, following
    `test_the_recorded_revision_check_resolves_either_spelling`'s own
    precedent, but recording a revision whose tree does NOT contain the
    declared staging folder, so the check fires instead of resolving
    cleanly. No static fallback is needed.
    """
    behavioral = set()

    # missing origin (post-contract -> ERROR)
    d = _change(tmp_path, "pin-missing",
                "schema: spec-driven\ncreated: 2026-09-01\n")
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # unknown kind
    packet = STAGED.replace("kind: staged", "kind: bogus")
    d = _change(tmp_path, "pin-unknown-kind", packet)
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # both kinds declared (id says adhoc, kind says staged)
    packet = STAGED.replace("id: repo:staging:topic-a",
                           "id: repo:adhoc:2026-08-10-topic")
    d = _change(tmp_path, "pin-both-kinds", packet)
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # malformed durable id
    packet = STAGED.replace("repo:staging:topic-a", "not-a-durable-id")
    d = _change(tmp_path, "pin-malformed-id", packet)
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # ad-hoc incomplete provenance
    packet = ADHOC.replace("  approved_by: Brett\n", "")
    d = _change(tmp_path, "pin-adhoc-incomplete", packet)
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # manifest disagreement (archived, contested mutation)
    d = _change(tmp_path, "2026-08-10-pin-mismatch", STAGED,
                manifest={"origin": {"kind": "staged", "id": "repo:staging:OTHER",
                                     "path": "ideation/staging/topic-a"}},
                archived=True)
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), True)}

    # staged origin lacks `path`
    packet = STAGED.replace("  path: ideation/staging/topic-a\n", "")
    d = _change(tmp_path, "pin-no-path", packet)
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # staging-header linkage broken (active, folder still exists)
    folder = tmp_path / "ideation" / "staging" / "pin-linkage"
    folder.mkdir(parents=True)
    (folder / "pin-linkage.md").write_text(
        "Staging ID: repo:staging:DIFFERENT\n")
    packet = STAGED.replace("path: ideation/staging/topic-a",
                           "path: ideation/staging/pin-linkage")
    d = _change(tmp_path, "pin-bad-linkage", packet)
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # unparseable packet metadata
    d = _change(tmp_path, "pin-unparseable", "origin:\n  reason: broken: colon\n")
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    # migration-recorded backfill removed after the fact (contested)
    d = _change(tmp_path, "2026-07-01-pin-old", None, archived=True)
    migrated = frozenset({"2026-07-01-pin-old"})
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, migrated, True)}

    # staged origin path does not resolve at the recorded source revision
    # (its OWN real git repo, under a fresh tmp_path).
    git_root = tmp_path / "pin-git-mismatch"
    git_root.mkdir()
    (git_root / "unrelated.txt").write_text("nothing staged here\n")
    subprocess.run(["git", "init", "-q", str(git_root)], check=True)
    subprocess.run(["git", "-C", str(git_root), "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", str(git_root), "-c", "user.name=T", "-c",
         "user.email=t@example.invalid", "commit", "-qm", "fixture"],
        check=True)
    revision = subprocess.run(
        ["git", "-C", str(git_root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
    d = _change(git_root, "pin-git-mismatch", STAGED,
               manifest={"source_revision": revision,
                         "origin": {"kind": "staged",
                                    "id": "repo:staging:topic-a",
                                    "path": "ideation/staging/topic-a"}})
    behavioral |= {f.action for f in
                  po.check_change("r", git_root, d, frozenset(), False)}

    # add-drafted-proposal-origin's three classes: the half-declared drafting
    # pair, the origin declaring neither state, and the status claiming a
    # ratification its origin does not carry.
    packet = DRAFTED.replace("  proposed_on: 2026-08-10\n", "")
    d = _change(tmp_path, "pin-half-drafting", packet, status="draft")
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    packet = ADHOC.replace("  approved_by: Brett\n", "").replace(
        "  approved_on: 2026-08-10\n", "")
    d = _change(tmp_path, "pin-no-state", packet, status="draft")
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    d = _change(tmp_path, "pin-unapproved-ratified", DRAFTED,
                status="ratified")
    behavioral |= {f.action for f in
                  po.check_change("r", tmp_path, d, frozenset(), False)}

    behavioral = frozenset(behavioral)
    static = harvest_static(po)

    EXPECTED_ACTIONS = {
        "declare `origin:` in .openspec.yaml (staged or ad_hoc per the "
        "document-lifecycle origin requirement)",
        "declare kind: staged or kind: ad_hoc",
        "make the durable id match the declared kind",
        "use <repo>:staging:<topic-slug> or <repo>:adhoc:<date>-<slug>",
        "record the explicit approval provenance the ad-hoc exception "
        "requires",
        "reconcile the manifest against the declaration recorded at "
        "transition; resolving reverses a gate decision",
        "record the original staging folder path",
        "restore the staging-header linkage or record the folder's move",
        "repair the packet metadata (quote scalars containing ': '), "
        "preserving the declared origin text",
        "restore the origin block recorded in the migration evidence",
        "the recorded provenance must contain the staging folder; correct "
        "the manifest or the declaration",
        # add-drafted-proposal-origin (issue #318)
        "record the approval provenance the ad-hoc exception requires, or "
        "declare the unapproved state with `proposed_by` and `proposed_on`",
        "record both `proposed_by` and `proposed_on`, or the approval pair "
        "once an approval exists",
        "record the approval provenance the declared status claims, or "
        "return the proposal to `draft`; resolving it reverses a gate "
        "decision",
    }
    assert_actions_pinned(EXPECTED_ACTIONS, behavioral, static,
                          family="proposal-origin")
