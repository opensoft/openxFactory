"""Tests for scripts/validate-ideation-routing.py (add-cross-factory-ideation-routing,
change task 2.3; the validator/contract-tests half of task 2.4).

The script's own `main()` self-tests schema conformance over every packaged
example under `examples/ideation-routing/` on every invocation (see the
script's `check_examples`). This suite targets, one by one, the eight
deterministic checks task 2.3 enumerates — routing schema conformance,
central ID allocation, unique canonical definitions, paired-document
agreement, legal transitions, accepted destinations, structured repository
references, and prospective legacy compatibility — proving each both accepts
the shape it should and fires for the violation it is named for, plus the
documented GATES behavior end-to-end (subprocess): every valid example
passes, every negative example fails for its own reason.

No prior pytest precedent exists for the other `scripts/validate-*.py`
contract validators (they are invoked directly against a repo path); this
follows the two suites that do exist — `tests/document_catalog/` and
`tests/avatar_runtime/` — adapted for a hyphenated-filename script module via
`importlib`.
"""
from __future__ import annotations

import copy
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-ideation-routing.py"

# An explicit known-repository set + mode so unit tests are deterministic
# regardless of whether an aggregation .gitmodules ancestor happens to exist.
KNOWN = {
    "xFactory", "openxFactory",
    "xFactories/MedxFactory", "xFactories/OpsxFactory", "xFactories/codexFactory",
    "installs/cloudpc-install",
}
MODE = "gitmodules"


def _load_module():
    spec = importlib.util.spec_from_file_location("validate_ideation_routing", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


vir = _load_module()


class RecordingFindings:
    """A Findings-shaped recorder that also captures the check code, so tests
    can assert *which* check fired without string-matching the whole
    message."""

    def __init__(self) -> None:
        self.errors: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []
        self.notes: list[str] = []

    def error(self, code, msg):
        self.errors.append((code, msg))

    def warn(self, code, msg):
        self.warnings.append((code, msg))

    def note(self, msg):
        self.notes.append(msg)

    def error_codes(self):
        return {c for c, _ in self.errors}

    def warning_codes(self):
        return {c for c, _ in self.warnings}


# --------------------------- fixtures ---------------------------

def _txn(frm, to, at="2026-07-10T14:00:00Z"):
    return {"from": frm, "to": to, "actor_ref": "actor", "occurred_at": at, "evidence_refs": []}


def _intake_record() -> dict:
    """A minimal schema-valid intake record with one unresolved claim,
    mirroring routing-record-unknown-owner-intake.example.yaml."""
    return {
        "schema_version": 1,
        "kind": "xfactory_idea_routing_record",
        "idea_id": "XFI-2026-014",
        "title": "Unknown-owner intake",
        "scope": "unclassified",
        "routing_status": "intake",
        "sources": [{
            "repository": "openxFactory",
            "path": "ideation/brainstorm/inbox/XFI-2026-014/idea.md",
            "revision": "pending_capture",
            "context": "discussion",
            "passage_sha256": None,
        }],
        "deduplication_rationale": None,
        "domains_touched": [],
        "candidate_owners": [],
        "claims": [{
            "claim_id": "XFI-2026-014-C01",
            "summary": "Notify a capability when a cited document changes.",
            "source_ref": {"source_index": 0, "section": "problem", "passage_sha256": "2" * 64},
            "proposed_owner": None,
            "accepted_owner": None,
            "target_capability": None,
            "destination": None,
            "blocker": "Owner unknown; needs triage.",
            "dependencies": [],
            "domain_local_exclusions": [],
            "disposition": "unresolved",
            "rationale": "Captured before ownership is known.",
            "acceptance": None,
            "transitions": [_txn(None, "unresolved")],
        }],
        "transitions": [_txn(None, "intake")],
        "successors": [],
        "notes": None,
    }


def _routed_record() -> dict:
    """A schema-valid, fully routed record whose one claim carries complete
    destination-owner acceptance, mirroring
    routing-record-destination-acceptance.example.yaml."""
    return {
        "schema_version": 1,
        "kind": "xfactory_idea_routing_record",
        "idea_id": "XFI-2026-003",
        "title": "Routed liaison",
        "scope": "cross_domain",
        "routing_status": "routed",
        "sources": [{
            "repository": "xFactories/MedxFactory",
            "path": "ideation/brainstorm/omni-clinic-hosting.md",
            "revision": "7" * 40,
            "context": "document",
            "passage_sha256": "5" * 64,
        }],
        "deduplication_rationale": None,
        "domains_touched": ["MedxFactory"],
        "candidate_owners": ["openxFactory"],
        "claims": [{
            "claim_id": "XFI-2026-003-C01",
            "summary": "Neutral liaison skeleton.",
            "source_ref": {"source_index": 0, "section": "infra", "passage_sha256": "8" * 64},
            "proposed_owner": "openxFactory",
            "accepted_owner": "openxFactory",
            "target_capability": "client-infrastructure-liaison",
            "destination": {
                "repository": "openxFactory",
                "path": "ideation/staging/client-infrastructure-liaison/skeleton.md",
                "revision": "5" * 40,
            },
            "blocker": None,
            "dependencies": [],
            "domain_local_exclusions": [],
            "disposition": "routed",
            "rationale": "Reusable neutral skeleton accepted by openxFactory.",
            "acceptance": {
                "actor_ref": "openxFactory ratify authority",
                "accepted_at": "2026-07-12T16:00:00Z",
                "evidence_refs": [{
                    "repository": "openxFactory",
                    "path": "ideation/staging/client-infrastructure-liaison/note.md",
                    "revision": "c" * 40,
                }],
            },
            "transitions": [
                _txn(None, "unresolved"),
                _txn("unresolved", "proposed", "2026-07-11T10:00:00Z"),
                _txn("proposed", "routed", "2026-07-12T16:00:00Z"),
            ],
        }],
        "transitions": [
            _txn(None, "intake"),
            _txn("intake", "triaging", "2026-07-10T13:45:00Z"),
            _txn("triaging", "split", "2026-07-11T09:30:00Z"),
            _txn("split", "routed", "2026-07-12T16:30:00Z"),
        ],
        "successors": [],
        "notes": None,
    }


def _index(idea_id="XFI-2026-014", path="ideation/brainstorm/inbox/XFI-2026-014/routing.yaml") -> dict:
    return {
        "schema_version": 1,
        "kind": "xfactory_ideation_routing_index",
        "allocations": [{
            "idea_id": idea_id,
            "title": "t",
            "routing_record": {"repository": "openxFactory", "path": path},
            "allocated_at": "2026-07-13",
        }],
        "notes": None,
    }


def _dump_yaml(doc: dict) -> str:
    return yaml.safe_dump(doc, sort_keys=False)


# --------------------------- 1. routing schema conformance (GATES) ---------------------------

def test_gates_valid_examples_pass_and_negative_examples_fail():
    """Documented GATES behavior end-to-end: exit 0, 6 valid top-level + 2
    fragment files confirmed valid, 8 negative examples confirmed invalid."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert ("6 valid top-level example(s) + 2 fragment file(s) confirmed valid, "
            "8 negative example(s) confirmed invalid") in proc.stdout
    assert "0 error(s), 0 warning(s)" in proc.stdout


def test_all_valid_examples_validate_against_their_schema():
    registry, docs = vir.build_registry()
    checked = 0
    for path in sorted(vir.EXAMPLES_DIR.glob("*.example.yaml")):
        if path.name in vir.FRAGMENT_DEFS:
            continue
        doc = vir.load_yaml(path)
        schema_name = vir.KIND_TO_SCHEMA[doc["kind"]]
        errs = list(vir.doc_validator(schema_name, registry, docs).iter_errors(doc))
        assert not errs, f"{path.name} expected valid: {[e.message for e in errs]}"
        checked += 1
    assert checked == 6


def test_negative_examples_each_fail_for_their_own_reason():
    """Re-derive per-file fail directly through the loaded module so a negative
    fixture that silently validates cannot hide behind another's failure."""
    registry, docs = vir.build_registry()
    neg_dir = vir.EXAMPLES_DIR / "negative"
    files = sorted(neg_dir.glob("*.yaml"))
    assert len(files) == 8
    for path in files:
        doc = vir.load_yaml(path)
        if path.name in vir.NEGATIVE_FRAGMENT_DEFS:
            schema_name, def_name = vir.NEGATIVE_FRAGMENT_DEFS[path.name]
            validator = vir.def_validator(schema_name, def_name, registry)
        else:
            schema_name = vir.KIND_TO_SCHEMA[doc["kind"]]
            validator = vir.doc_validator(schema_name, registry, docs)
        errs = list(validator.iter_errors(doc))
        assert errs, f"{path.name} was expected to fail schema validation but validated cleanly"


def test_all_four_schemas_are_valid_draft2020_12():
    from jsonschema import Draft202012Validator
    _, docs = vir.build_registry()
    assert set(docs) == set(vir.SCHEMA_FILENAMES)
    for name, doc in docs.items():
        Draft202012Validator.check_schema(doc)  # raises on invalid


def test_fixtures_are_schema_valid():
    """The synthetic fixtures this suite exercises are themselves schema-valid,
    so a deterministic-check failure is never masked by a bad fixture."""
    registry, docs = vir.build_registry()
    v = vir.doc_validator("xfactory-idea-routing-record.schema.yaml", registry, docs)
    for rec in (_intake_record(), _routed_record()):
        assert not list(v.iter_errors(rec)), rec["idea_id"]
    vi = vir.doc_validator("xfactory-ideation-routing-index.schema.yaml", registry, docs)
    assert not list(vi.iter_errors(_index()))


# --------------------------- 2. central ID allocation + uniqueness ---------------------------

def test_central_allocation_accepts_allocated_idea():
    f = RecordingFindings()
    vir.check_central_allocation(f, [("r", _intake_record())], _index(), repo_root=None)
    assert not f.errors


def test_central_allocation_flags_unallocated_idea():
    f = RecordingFindings()
    vir.check_central_allocation(f, [("r", _intake_record())], _index(idea_id="XFI-2026-999"), repo_root=None)
    assert "idea-unallocated" in f.error_codes()


def test_central_allocation_flags_duplicate_allocation():
    idx = _index()
    idx["allocations"].append(copy.deepcopy(idx["allocations"][0]))
    f = RecordingFindings()
    vir.check_central_allocation(f, [("r", _intake_record())], idx, repo_root=None)
    assert "duplicate-idea-allocation" in f.error_codes()


def test_central_allocation_flags_dangling_openxfactory_pointer(tmp_path):
    """An index pointer into this checkout (repository openxFactory) that names
    no real file is dangling."""
    idx = _index(path="ideation/brainstorm/inbox/XFI-2026-014/routing.yaml")  # file not created
    f = RecordingFindings()
    vir.check_central_allocation(f, [], idx, repo_root=tmp_path)
    assert "allocation-dangling" in f.error_codes()


def test_central_allocation_resolves_existing_openxfactory_pointer(tmp_path):
    rec_path = tmp_path / "ideation" / "brainstorm" / "inbox" / "XFI-2026-014" / "routing.yaml"
    rec_path.parent.mkdir(parents=True)
    rec_path.write_text("placeholder")
    f = RecordingFindings()
    vir.check_central_allocation(f, [("r", _intake_record())], _index(), repo_root=tmp_path)
    assert not f.errors


# --------------------------- 3. unique canonical definitions ---------------------------

def test_one_canonical_accepts_distinct_ideas():
    f = RecordingFindings()
    vir.check_one_canonical(f, [("a", _intake_record()), ("b", _routed_record())])
    assert not f.errors


def test_one_canonical_rejects_two_records_for_one_idea():
    dup = copy.deepcopy(_intake_record())
    f = RecordingFindings()
    vir.check_one_canonical(f, [("a/routing.yaml", _intake_record()), ("b/routing.yaml", dup)])
    assert "duplicate-canonical-record" in f.error_codes()


def test_claim_ids_accepts_wellformed_prefix_and_unique():
    f = RecordingFindings()
    vir.check_claim_ids(f, "r", _intake_record())
    assert not f.errors


def test_claim_ids_rejects_wrong_prefix():
    rec = _intake_record()
    rec["claims"][0]["claim_id"] = "XFI-2026-999-C01"  # != record idea_id
    f = RecordingFindings()
    vir.check_claim_ids(f, "r", rec)
    assert "claim-id-prefix" in f.error_codes()


def test_claim_ids_rejects_intra_record_duplicate():
    rec = _routed_record()
    rec["claims"].append(copy.deepcopy(rec["claims"][0]))  # same claim_id twice
    f = RecordingFindings()
    vir.check_claim_ids(f, "r", rec)
    assert "duplicate-claim-id" in f.error_codes()


def test_corpus_claim_uniqueness_rejects_duplicate_across_records():
    a = _routed_record()
    b = copy.deepcopy(_routed_record())
    b["idea_id"] = "XFI-2026-050"  # different idea, but reuses the same claim id
    f = RecordingFindings()
    vir.check_corpus_claim_uniqueness(f, [("a", a), ("b", b)])
    assert "duplicate-claim-id" in f.error_codes()


# --------------------------- 4. paired-document agreement ---------------------------

def _write_record_dir(tmp_path, idea_dir: str, record: dict, paired: dict[str, str]):
    d = tmp_path / "ideation" / "brainstorm" / "inbox" / idea_dir
    d.mkdir(parents=True)
    rec_path = d / "routing.yaml"
    rec_path.write_text(_dump_yaml(record))
    for name, text in paired.items():
        (d / name).write_text(text)
    return rec_path


def test_paired_documents_accepts_matching_pair(tmp_path):
    rec = _intake_record()
    rec_path = _write_record_dir(tmp_path, "XFI-2026-014", rec, {"idea.md": "Idea ID: XFI-2026-014\n\nbody"})
    f = RecordingFindings()
    vir.check_paired_documents(f, tmp_path, rec_path, rec)
    assert not f.errors


def test_paired_documents_flags_directory_mismatch(tmp_path):
    rec = _intake_record()  # idea_id XFI-2026-014
    rec_path = _write_record_dir(tmp_path, "XFI-2026-999", rec, {"idea.md": "body"})
    f = RecordingFindings()
    vir.check_paired_documents(f, tmp_path, rec_path, rec)
    assert "pair-dir-mismatch" in f.error_codes()


def test_paired_documents_flags_missing_human_readable_doc(tmp_path):
    rec = _intake_record()
    rec_path = _write_record_dir(tmp_path, "XFI-2026-014", rec, {})  # no idea.md/routing-summary.md
    f = RecordingFindings()
    vir.check_paired_documents(f, tmp_path, rec_path, rec)
    assert "pair-missing-doc" in f.error_codes()


def test_paired_documents_flags_header_id_mismatch(tmp_path):
    rec = _intake_record()
    rec_path = _write_record_dir(tmp_path, "XFI-2026-014", rec, {"idea.md": "Idea ID: XFI-2026-777\n"})
    f = RecordingFindings()
    vir.check_paired_documents(f, tmp_path, rec_path, rec)
    assert "pair-id-mismatch" in f.error_codes()


def test_paired_documents_allows_doc_without_header_for_legacy(tmp_path):
    """A paired document that carries no `Idea ID:` header at all is not
    flagged — prospective/legacy compatibility."""
    rec = _intake_record()
    rec_path = _write_record_dir(tmp_path, "XFI-2026-014", rec, {"idea.md": "# just prose, no header\n"})
    f = RecordingFindings()
    vir.check_paired_documents(f, tmp_path, rec_path, rec)
    assert not f.errors


# --------------------------- 5. legal transitions (sequence level) ---------------------------

def test_transition_chains_accepts_valid_records():
    for rec in (_intake_record(), _routed_record()):
        f = RecordingFindings()
        vir.check_transition_chains(f, "r", rec)
        assert not f.errors, rec["idea_id"]


def test_transition_chains_rejects_noncontiguous_record_history():
    rec = _routed_record()
    # drop the intake->triaging edge so triaging->split no longer follows intake
    rec["transitions"] = [rec["transitions"][0], rec["transitions"][2], rec["transitions"][3]]
    f = RecordingFindings()
    vir.check_transition_chains(f, "r", rec)
    assert "transition-chain" in f.error_codes()


def test_transition_chains_rejects_terminal_state_mismatch():
    rec = _intake_record()
    rec["routing_status"] = "triaging"  # but history ends at intake
    f = RecordingFindings()
    vir.check_transition_chains(f, "r", rec)
    assert "transition-chain" in f.error_codes()


def test_transition_chains_rejects_nonnull_first_from():
    rec = _intake_record()
    rec["transitions"][0]["from"] = "intake"  # first from must be null
    f = RecordingFindings()
    vir.check_transition_chains(f, "r", rec)
    assert "transition-chain" in f.error_codes()


def test_claim_transition_chains_rejects_noncontiguous():
    rec = _routed_record()
    # remove unresolved->proposed so proposed->routed no longer follows unresolved
    c = rec["claims"][0]
    c["transitions"] = [c["transitions"][0], c["transitions"][2]]
    f = RecordingFindings()
    vir.check_transition_chains(f, "r", rec)
    assert "claim-transition-chain" in f.error_codes()


def test_claim_transition_chains_rejects_terminal_mismatch():
    rec = _routed_record()
    rec["claims"][0]["disposition"] = "deferred"  # history ends at routed
    f = RecordingFindings()
    vir.check_transition_chains(f, "r", rec)
    assert "claim-transition-chain" in f.error_codes()


# --------------------------- 6. accepted destinations ---------------------------

def test_accepted_destinations_accepts_complete_routed_claim():
    f = RecordingFindings()
    vir.check_accepted_destinations(f, "r", _routed_record(), KNOWN, MODE)
    assert not f.errors


def test_accepted_destinations_flags_missing_acceptance():
    rec = _routed_record()
    rec["claims"][0]["acceptance"] = None
    f = RecordingFindings()
    vir.check_accepted_destinations(f, "r", rec, KNOWN, MODE)
    assert "routed-acceptance" in f.error_codes()


def test_accepted_destinations_flags_empty_acceptance_evidence():
    rec = _routed_record()
    rec["claims"][0]["acceptance"]["evidence_refs"] = []
    f = RecordingFindings()
    vir.check_accepted_destinations(f, "r", rec, KNOWN, MODE)
    assert "routed-acceptance" in f.error_codes()


def test_accepted_destinations_flags_unknown_destination_repository():
    rec = _routed_record()
    rec["claims"][0]["destination"]["repository"] = "not-a-known-repo"
    f = RecordingFindings()
    vir.check_accepted_destinations(f, "r", rec, KNOWN, MODE)
    assert "routed-acceptance" in f.error_codes()


def test_accepted_destinations_ignores_unrouted_claims():
    f = RecordingFindings()
    vir.check_accepted_destinations(f, "r", _intake_record(), KNOWN, MODE)  # claim is unresolved
    assert not f.errors


# --------------------------- 7. structured repository references ---------------------------

def test_reference_resolution_accepts_known_repositories():
    f = RecordingFindings()
    vir.check_reference_resolution(f, "r", _routed_record(), KNOWN, MODE)
    assert not f.errors


def test_reference_resolution_flags_unknown_repository():
    rec = _intake_record()
    rec["sources"][0]["repository"] = "some-unknown-repo"
    f = RecordingFindings()
    vir.check_reference_resolution(f, "r", rec, KNOWN, MODE)
    assert "unknown-repository" in f.error_codes()


def test_reference_resolution_ignores_bare_owner_label_strings():
    """`proposed_owner`/`candidate_owners`/`accepted_owner` are free-form owner
    labels, not structured references, and must never be resolved as repos."""
    rec = _intake_record()
    rec["candidate_owners"] = ["OpsxFactory", "some free text owner"]
    rec["claims"][0]["proposed_owner"] = "a totally free-form authority label"
    f = RecordingFindings()
    vir.check_reference_resolution(f, "r", rec, KNOWN, MODE)
    assert not f.errors


def test_repository_unknown_reason_reserved_root_always_resolves():
    assert vir.repository_unknown_reason("xFactory", set(), "convention") is None
    assert vir.repository_unknown_reason("xFactory", set(), "gitmodules") is None


def test_repository_unknown_reason_convention_mode_shapes():
    assert vir.repository_unknown_reason("openxFactory", {"openxFactory", "xFactory"}, "convention") is None
    assert vir.repository_unknown_reason("xFactories/GhostFactory", {"openxFactory", "xFactory"}, "convention") is None
    assert vir.repository_unknown_reason("installs/whatever", {"openxFactory", "xFactory"}, "convention") is None
    assert vir.repository_unknown_reason("random", {"openxFactory", "xFactory"}, "convention") is not None


def test_repository_unknown_reason_gitmodules_mode_requires_membership():
    known = {"xFactory", "openxFactory", "xFactories/MedxFactory"}
    assert vir.repository_unknown_reason("xFactories/MedxFactory", known, "gitmodules") is None
    # a well-formed-but-absent domain path is rejected in exact-membership mode
    assert vir.repository_unknown_reason("xFactories/GhostFactory", known, "gitmodules") is not None


def test_resolve_known_repositories_finds_aggregation_gitmodules():
    """From this worktree, walk-up discovers the aggregation .gitmodules and
    resolves exactly; the openxFactory-internal .gitmodules (installs only) is
    correctly skipped."""
    known, mode, gm = vir.resolve_known_repositories(ROOT)
    if mode == "gitmodules":
        assert "xFactories/MedxFactory" in known
        assert "installs/cloudpc-install" in known
        assert gm is not None
    else:  # standalone clone: no aggregation ancestor
        assert known == {"openxFactory", "xFactory"}


def test_resolve_known_repositories_falls_back_to_convention(tmp_path):
    known, mode, gm = vir.resolve_known_repositories(tmp_path)
    assert mode == "convention"
    assert gm is None


# --------------------------- 8. prospective legacy compatibility ---------------------------

def test_ordinary_documents_without_sidecar_are_not_flagged(tmp_path):
    """An ideation tree with ordinary brainstorm prose and no routing.yaml (and
    an empty central index) produces no findings — routing is prospective."""
    (tmp_path / "ideation").mkdir()
    (tmp_path / "ideation" / "routing-index.yaml").write_text(
        _dump_yaml({"schema_version": 1, "kind": "xfactory_ideation_routing_index", "allocations": []})
    )
    bs = tmp_path / "ideation" / "brainstorm"
    bs.mkdir()
    (bs / "some-ordinary-idea.md").write_text("Status: brainstorm\nKind: idea\n\nplain prose, no routing.\n")
    registry, docs = vir.build_registry()
    f = RecordingFindings()
    vir.check_repo_tree(f, registry, docs, tmp_path, KNOWN, MODE)
    assert not f.errors, f.errors


# --------------------------- repo-tree integration (end to end) ---------------------------

def _write_corpus(tmp_path, record: dict, index: dict):
    (tmp_path / "ideation").mkdir()
    (tmp_path / "ideation" / "routing-index.yaml").write_text(_dump_yaml(index))
    d = tmp_path / "ideation" / "brainstorm" / "inbox" / record["idea_id"]
    d.mkdir(parents=True)
    (d / "routing.yaml").write_text(_dump_yaml(record))
    (d / "idea.md").write_text(f"Idea ID: {record['idea_id']}\n\nbody\n")


def test_repo_tree_end_to_end_clean_corpus(tmp_path):
    """A real synthetic corpus — central index + one allocated routing record
    with a matching paired idea.md — passes check_repo_tree end to end."""
    _write_corpus(tmp_path, _intake_record(), _index())
    registry, docs = vir.build_registry()
    f = RecordingFindings()
    vir.check_repo_tree(f, registry, docs, tmp_path, KNOWN, MODE)
    assert not f.errors, f.errors


def test_repo_tree_flags_unallocated_record_end_to_end(tmp_path):
    """A committed routing record whose Idea ID was never allocated in the
    central index fails check_repo_tree (central-allocation over the real
    corpus, not just a unit fixture)."""
    _write_corpus(tmp_path, _intake_record(), _index(idea_id="XFI-2026-500",
                                                     path="ideation/brainstorm/inbox/XFI-2026-500/routing.yaml"))
    registry, docs = vir.build_registry()
    f = RecordingFindings()
    vir.check_repo_tree(f, registry, docs, tmp_path, KNOWN, MODE)
    assert "idea-unallocated" in f.error_codes()


def test_repo_tree_flags_invalid_record_schema_end_to_end(tmp_path):
    bad = _intake_record()
    del bad["idea_id"]  # required by the record schema
    d = tmp_path / "ideation" / "brainstorm" / "inbox" / "XFI-2026-014"
    d.mkdir(parents=True)
    (d / "routing.yaml").write_text(_dump_yaml(bad))
    (d / "idea.md").write_text("Idea ID: XFI-2026-014\n\nbody\n")
    (tmp_path / "ideation" / "routing-index.yaml").write_text(_dump_yaml(_index()))
    registry, docs = vir.build_registry()
    f = RecordingFindings()
    vir.check_repo_tree(f, registry, docs, tmp_path, KNOWN, MODE)
    assert "record-invalid" in f.error_codes()


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
