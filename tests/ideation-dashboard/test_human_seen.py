"""US7 human-seen-cluster submission tests (T028; change 3.5).

The T028 blocker cleared 2026-07-14 (add-ideation-cross-reference-readiness
realized the pending_review intake contract in
ideation-cross-reference.schema.yaml). These tests exercise the submission path
in `human_seen.py` against the REAL fixture snapshot and the REAL pinned
cross-reference validator:

  * a complete submission builds a `topic_entry` with `origin: human-seen`, the
    full organizer evidence contract, and `pending_review` disposition — and
    validates CLEAN against the pinned `validate-ideation-cross-reference.py`;
  * a submission lacking ANY required evidence field (proposer / revision /
    section / passage hash / rationale) is REFUSED before persistence — no queue
    entry is written (spec scenario "A submission lacks evidence");
  * a malformed passage hash / abbreviated revision / out-of-range confidence is
    refused too (the contract FORMATS, caught before a write, not after);
  * the queue entry lands under the gitignored ideation/workbench/ prefix (never
    the generated index) with the expected intake shape;
  * members carry the snapshot's `stage`, and a member absent from the snapshot
    is refused (its stage cannot be resolved without fabrication).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit

from ideation_dashboard import human_seen as hs
from opendox import lens
from opendox import workbench as wb
from opendox.boundary import OutputBoundary
from openxdox.generator import generate_snapshot

XREF_VALIDATOR = hs.find_cross_reference_validator(REPO_ROOT)
NOW = "2026-07-14T08:00:00Z"

GOOD_HASH = "b0f04c299263dd2496c601fbbd812d645ebade162c5a9aa15e8fe8b7a656bc7a"


def _snapshot():
    return generate_snapshot(BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


def _boundary(root: Path, *extra: str) -> OutputBoundary:
    return OutputBoundary(root, [wb.WORKBENCH_DIR, *extra])


def _workbench(snap):
    return lens.build_workbench_from_recipe(
        "fixture-repo", "Governance lens", ["ideation-governance"], [], snap, now=NOW)


def _submission(**over):
    fields = {
        "proposer": "brett",
        "repository": "fixture-repo",
        "path": "ideation/brainstorm/dtn-register.md",
        "revision": PINNED_REVISION,
        "section": "Notes",
        "passage_sha256": GOOD_HASH,
        "rationale": "Two governance notes describe the same cluster; grouping for review.",
        "confidence": 0.6,
        "alternatives": ["Fold into an existing governance cluster instead."],
    }
    fields.update(over)
    return hs.HumanSeenSubmission(**fields)


# ----------------------------------------------------------------------------
# a complete submission — pending_review intake, validated by the real schema
# ----------------------------------------------------------------------------

def test_intake_carries_origin_human_seen_and_full_evidence_contract(tmp_path):
    snap = _snapshot()
    w = _workbench(snap)
    res = hs.submit_from_workbench(w, snap, _submission(), _boundary(tmp_path), now=NOW)
    entry = res.index["topic_entries"][0]
    assert res.index["kind"] == "ideation-cross-reference"
    assert entry["origin"] == "human-seen"
    hseen = entry["human_seen"]
    assert hseen["proposer"] == "brett"
    assert hseen["disposition"] == "pending_review"
    ev = hseen["evidence"]
    # the full ORGANIZER evidence contract (not the lighter cataloger pin).
    assert set(ev["source_ref"]) == {"repository", "path", "revision", "section", "passage_sha256"}
    assert ev["source_ref"]["revision"] == PINNED_REVISION
    assert ev["source_ref"]["passage_sha256"] == GOOD_HASH
    assert ev["rationale"]
    assert ev["confidence"] == pytest.approx(0.6)
    assert isinstance(ev["alternatives"], list)
    assert ev["disposition"] == "pending_review"          # never a verdict
    # the defining topics come from the recipe's checked keywords.
    assert entry["topics"] == ["ideation-governance"]
    assert entry["tag_sources"] == ["topics-header"]
    # the recipe is offered as rationale (change 3.10).
    assert "keyword lens" in hseen["recipe_reference"]


def test_members_carry_the_snapshot_stage(tmp_path):
    snap = _snapshot()
    w = _workbench(snap)
    res = hs.submit_from_workbench(w, snap, _submission(), _boundary(tmp_path), now=NOW)
    members = res.index["topic_entries"][0]["members"]
    assert members  # the governance recipe matches several docs
    stages = {d["id"]: d["stage"] for d in snap["documents"]}
    for m in members:
        assert m["stage"] == stages[m["document"]]         # verbatim from the snapshot
        assert "ideation-governance" in m["matched_tags"]  # the matched defining topic


@pytest.mark.skipif(XREF_VALIDATOR is None, reason="pinned cross-reference validator not reachable")
def test_submission_validates_clean_on_the_pinned_cross_reference_schema(tmp_path):
    snap = _snapshot()
    w = _workbench(snap)
    # validate=True re-checks the written entry with the pinned validator; a
    # failure would raise SubmissionInvalid here.
    res = hs.submit_from_workbench(w, snap, _submission(), _boundary(tmp_path),
                                   now=NOW, validate=True, validator=XREF_VALIDATOR)
    assert res.path.is_file()
    proc = subprocess.run(
        [sys.executable, str(XREF_VALIDATOR), str(res.path),
         "--repo", str(XREF_VALIDATOR.resolve().parents[1])],
        capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr


# ----------------------------------------------------------------------------
# queue location — gitignored workbench prefix, never the generated index
# ----------------------------------------------------------------------------

def test_queue_entry_lands_under_the_gitignored_workbench_prefix(tmp_path):
    snap = _snapshot()
    w = _workbench(snap)
    res = hs.submit_from_workbench(w, snap, _submission(), _boundary(tmp_path), now=NOW)
    assert res.relpath.startswith("ideation/workbench/cross-reference-queue/")
    assert res.relpath.startswith(hs.QUEUE_DIR)
    # it is NOT the generated source-of-truth index.
    assert "ideation/cross-reference.yaml" not in res.relpath
    # the only file written is the queue entry (submit_from_workbench writes no manifest).
    assert [p for p in tmp_path.rglob("*") if p.is_file()] == [res.path]


# ----------------------------------------------------------------------------
# refusal before persistence — the "A submission lacks evidence" scenario
# ----------------------------------------------------------------------------

@pytest.mark.parametrize("field", ["proposer", "revision", "section", "passage_sha256", "rationale"])
def test_missing_required_evidence_field_refused_before_persistence(tmp_path, field):
    snap = _snapshot()
    w = _workbench(snap)
    boundary = _boundary(tmp_path)
    sub = _submission(**{field: ""})
    with pytest.raises(hs.SubmissionRefused):
        hs.submit_from_workbench(w, snap, sub, boundary, now=NOW)
    # nothing was written — the refusal precedes any queue write.
    assert not [p for p in tmp_path.rglob("*") if p.is_file()]


def test_malformed_passage_hash_and_revision_refused():
    bad_hash = _submission(passage_sha256="not-a-hash")
    bad_revision = _submission(revision="abc123")  # abbreviated, not full
    with pytest.raises(hs.SubmissionRefused):
        hs.require_complete_evidence(bad_hash)
    with pytest.raises(hs.SubmissionRefused):
        hs.require_complete_evidence(bad_revision)


def test_confidence_out_of_range_refused():
    too_high = _submission(confidence=1.5)
    too_low = _submission(confidence=-0.1)
    with pytest.raises(hs.SubmissionRefused):
        hs.require_complete_evidence(too_high)
    with pytest.raises(hs.SubmissionRefused):
        hs.require_complete_evidence(too_low)


def test_alternatives_with_empty_or_non_string_entries_refused():
    # `alternatives` items are non-empty strings (contract minLength 1); an empty,
    # blank, or non-string entry is refused BEFORE persistence, never serialized
    # into the queue (the validate=False default otherwise lets contents through).
    empty_entry = _submission(alternatives=[""])
    blank_entry = _submission(alternatives=["   "])
    numeric_entry = _submission(alternatives=[123])
    for bad in (empty_entry, blank_entry, numeric_entry):
        with pytest.raises(hs.SubmissionRefused):
            hs.require_complete_evidence(bad)


def test_ad_hoc_submission_derives_topics_from_member_docs(tmp_path):
    # US7 ad-hoc scenario: a set with seed.kind ad-hoc and NO recipe.checked. The
    # defining topics fall back to the UNION of the member documents' declared
    # topics from the snapshot (previously this yielded no topics and was wrongly
    # refused as topic-less).
    snap = _snapshot()
    w = wb.Workbench.create("fixture-repo", "Ad-hoc governance set",
                            seed=wb.SEED_ADHOC, now=NOW)
    w.add_member("ideation/brainstorm/dtn-register.md", wb.VIA_MANUAL_INCLUDE,
                 reason="hand-picked", now=NOW)
    w.add_member("ideation/brainstorm/doc-health-checks.md", wb.VIA_MANUAL_INCLUDE,
                 reason="hand-picked", now=NOW)
    res = hs.submit_from_workbench(w, snap, _submission(), _boundary(tmp_path), now=NOW)
    entry = res.index["topic_entries"][0]
    assert entry["origin"] == "human-seen"
    assert entry["human_seen"]["disposition"] == "pending_review"
    # dtn-register -> {dtn, ideation-governance}; doc-health-checks -> {doc-health,
    # ideation-governance}; the sorted union defines the ad-hoc cluster's topics.
    assert entry["topics"] == ["doc-health", "dtn", "ideation-governance"]


def test_snapshot_evidence_revision_mismatch_refused_before_persistence(tmp_path):
    # The envelope's generation.source_revision and the evidence source_ref.revision
    # are ONE determinism anchor; a submission citing a DIFFERENT (well-formed)
    # revision than the workbench snapshot is refused before any write.
    snap = _snapshot()  # generated at PINNED_REVISION
    w = _workbench(snap)
    boundary = _boundary(tmp_path)
    other_revision = "0123456789abcdef0123456789abcdef01234567"  # 40-hex, != PINNED
    sub = _submission(revision=other_revision)
    with pytest.raises(hs.SubmissionRefused):
        hs.submit_from_workbench(w, snap, sub, boundary, now=NOW)
    assert not [p for p in tmp_path.rglob("*") if p.is_file()]


def test_complete_evidence_with_empty_alternatives_is_accepted(tmp_path):
    # `alternatives` is a REQUIRED but possibly-empty array (organizer contract).
    snap = _snapshot()
    w = _workbench(snap)
    res = hs.submit_from_workbench(w, snap, _submission(alternatives=[]), _boundary(tmp_path), now=NOW)
    assert res.index["topic_entries"][0]["human_seen"]["evidence"]["alternatives"] == []


def test_member_absent_from_snapshot_is_refused(tmp_path):
    snap = _snapshot()
    w = _workbench(snap)
    # a workbench member the snapshot does not carry — its stage is unresolvable.
    w.add_member("ideation/brainstorm/ghost.md", wb.VIA_MANUAL_INCLUDE,
                 reason="not in the corpus", now=NOW)
    boundary = _boundary(tmp_path)
    sub = _submission()
    with pytest.raises(hs.SubmissionRefused):
        hs.submit_from_workbench(w, snap, sub, boundary, now=NOW)
    assert not [p for p in tmp_path.rglob("*") if p.is_file()]
