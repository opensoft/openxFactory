"""Tests for scripts/validate-document-catalog.py (add-document-cataloging,
change task 2.3).

The script's own `main()` self-tests schema conformance over every packaged
example under `examples/document-cataloging/` on every invocation (see the
script's `check_examples`). This suite instead targets the cross-cutting
deterministic checks that JSON Schema alone cannot express — complete
coverage, unique identity, source freshness, review-binding freshness
against the owner override file, taxonomy resolution, override standing (on
the override file and on snapshot review blocks), immutable path layout,
and the disclosed baseline-mode exception — with small synthetic fixtures,
proving each one both accepts the shape it should and rejects the violation
it is named for. It also runs the packaged
script end-to-end (subprocess) to prove the documented GATES behavior: valid
examples pass, every negative example fails for its own reason.

No prior pytest precedent exists for the other `scripts/validate-*.py`
contract validators (they are invoked directly against a repo path, not
covered by a dedicated suite); this follows the one pytest convention that
does exist in this repo (`tests/avatar_runtime/`), adapted for a
hyphenated-filename script module via `importlib`.
"""
from __future__ import annotations

import copy
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-document-catalog.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("validate_document_catalog", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


vdc = _load_module()


class RecordingFindings:
    """A Findings-shaped recorder that also captures the check code, so
    tests can assert *which* check fired without string-matching the whole
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

def _base_snapshot() -> dict:
    """A minimal, schema-valid two-entry snapshot mirroring the shape of
    the shipped `document-catalog-snapshot-complete.example.yaml`."""
    return {
        "schema_version": 1,
        "kind": "xfactory_document_catalog",
        "status": "record",
        "run": {
            "run_id": "RUN-1",
            "repository": "xFactories/MedxFactory",
            "repository_revision": "a" * 40,
            "inventory_snapshot_id": "snap-1",
        },
        "taxonomy": {
            "digest": "1" * 64,
            "inputs": [
                {
                    "repository": "openxFactory",
                    "path": "contracts/document-tag-registry.yaml",
                    "content_sha256": "2" * 64,
                    "registry_version": "1",
                    "repository_revision": "b" * 40,
                    "registry_revision": "c" * 40,
                },
            ],
        },
        "entries": [
            {
                "repo": "xFactories/MedxFactory",
                "path": "docs/one.md",
                "status": "draft",
                "artifact_type": "governance_markdown",
                "revision": "a" * 40,
                "content_hash": "3" * 64,
                "snapshot_id": "snap-1",
            },
            {
                "repo": "xFactories/MedxFactory",
                "path": "docs/two.md",
                "status": "draft",
                "artifact_type": "governance_markdown",
                "revision": "a" * 40,
                "content_hash": "4" * 64,
                "snapshot_id": "snap-1",
            },
        ],
    }


def _reviewed_entry_snapshot(
    state: str = "reviewed",
    authority: str = "xFactories/MedxFactory authority (Domain Hermes)",
) -> dict:
    """_base_snapshot with a reviewed/overridden document_role facet (and
    its schema-required review block) on the first entry."""
    doc = _base_snapshot()
    doc["entries"][0]["facet_assignments"] = [
        {
            "facet": "document_role",
            "values": ["process"],
            "state": state,
            "state_since": "2026-07-13",
            "provenance": {
                "taxonomy_sha256": "1" * 64,
                "method": "classifier",
                "classifier_version": "1.0.0",
                "model": "xfactory-doc-cataloger-2026-06",
                "prompt_contract_version": 1,
                "confidence": 0.95,
                "section": "front-matter",
                "passage_sha256": "2" * 64,
                "evidence_refs": [],
            },
            "transitions": [
                {
                    "from": "suggested",
                    "to": state,
                    "occurred_at": "2026-07-13T09:00:00Z",
                    "evidence_refs": ["catalog/document-tag-overrides.yaml#entry-1"],
                },
            ],
            "review": {
                "decision": state,
                "authority": authority,
                "occurred_at": "2026-07-13T09:00:00Z",
                "rationale": "test disposition",
                "evidence_refs": ["catalog/document-tag-overrides.yaml#entry-1"],
            },
        },
    ]
    return doc


def _matching_overrides(source_content_hash: str = "3" * 64) -> dict:
    """An override file whose single entry targets _reviewed_entry_snapshot's
    first entry (docs/one.md, facet document_role); by default it binds that
    entry's current content_hash."""
    return {
        "schema_version": 1,
        "kind": "xfactory_document_tag_overrides",
        "overrides": [
            {
                "repo": "xFactories/MedxFactory",
                "path": "docs/one.md",
                "source_content_hash": source_content_hash,
                "facet": "document_role",
                "decision": "reviewed",
                "actor": "xFactories/MedxFactory authority (Domain Hermes)",
                "occurred_at": "2026-07-13T00:00:00Z",
                "rationale": "test",
                "evidence_refs": ["e1"],
            },
        ],
    }


# --------------------------- 1. schema conformance (GATES) ---------------------------

def test_gates_valid_examples_pass_and_negative_examples_fail():
    """The documented GATES behavior end-to-end: exit 0 over the packaged
    fixture set, with 9 top-level valid examples and 12 negative examples
    confirmed (the two fragment-kernel example files carry 2 items each,
    for the 12 valid fixture cases task 2.2 reports, plus the
    `document-catalog-reference-invalidation`/`snapshot-evidence-ref-
    extra-property` pair added for the `evidence_ref` mapping-form schema
    revision)."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=ROOT, capture_output=True, text=True, timeout=60,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "9 valid example(s) confirmed valid, 12 negative example(s) confirmed invalid" in proc.stdout
    assert "0 error(s), 0 warning(s)" in proc.stdout


def test_negative_examples_each_fail_for_a_reason_matching_their_filename():
    """Re-derive per-file pass/fail directly through the loaded module
    (rather than only the aggregate GATES count) so a negative fixture that
    silently validates cannot hide behind another fixture's failure."""
    registry, docs = vdc.build_registry()
    neg_dir = vdc.EXAMPLES_DIR / "negative"
    files = sorted(neg_dir.glob("*.yaml"))
    assert len(files) == 12
    for path in files:
        doc = vdc.load_yaml(path)
        if path.name in vdc.NEGATIVE_FRAGMENT_DEFS:
            schema_name, def_name = vdc.NEGATIVE_FRAGMENT_DEFS[path.name]
            validator = vdc.def_validator(schema_name, def_name, registry)
        else:
            schema_name = vdc.KIND_TO_SCHEMA[doc["kind"]]
            validator = vdc.doc_validator(schema_name, registry, docs)
        errs = list(validator.iter_errors(doc))
        assert errs, f"{path.name} was expected to fail schema validation but validated cleanly"


# --------------------------- 2. complete coverage ---------------------------

def test_complete_coverage_flags_missing_and_extra_against_inventory():
    doc = _base_snapshot()
    f = RecordingFindings()
    inventory = [
        {"repo": "xFactories/MedxFactory", "path": "docs/one.md"},
        {"repo": "xFactories/MedxFactory", "path": "docs/two.md"},
        {"repo": "xFactories/MedxFactory", "path": "docs/three.md"},  # missing from the snapshot
    ]
    vdc.check_complete_coverage(f, "t", doc, inventory, baseline=False)
    assert "coverage-missing" in f.error_codes()
    assert not f.warning_codes()


def test_complete_coverage_without_inventory_notes_and_does_not_error():
    doc = _base_snapshot()
    f = RecordingFindings()
    vdc.check_complete_coverage(f, "t", doc, inventory=None, baseline=False)
    assert not f.errors
    assert any("coverage cross-check skipped" in n for n in f.notes)


def test_complete_coverage_extra_entry_is_always_an_error_even_in_baseline():
    doc = _base_snapshot()
    f = RecordingFindings()
    inventory = [{"repo": "xFactories/MedxFactory", "path": "docs/one.md"}]  # docs/two.md is "extra"
    vdc.check_complete_coverage(f, "t", doc, inventory, baseline=True)
    assert "coverage-extra" in f.error_codes()


# --------------------------- 3. unique identity ---------------------------

def test_unique_identity_accepts_distinct_locators():
    doc = _base_snapshot()
    f = RecordingFindings()
    vdc.check_unique_identity(f, "t", doc)
    assert not f.errors


def test_unique_identity_rejects_duplicate_locator():
    doc = _base_snapshot()
    doc["entries"].append(copy.deepcopy(doc["entries"][0]))
    f = RecordingFindings()
    vdc.check_unique_identity(f, "t", doc)
    assert "duplicate-identity" in f.error_codes()


# --------------------------- 4. source freshness ---------------------------

def test_source_freshness_accepts_entries_matching_their_run():
    doc = _base_snapshot()
    f = RecordingFindings()
    vdc.check_source_freshness(f, "t", doc)
    assert not f.errors


def test_source_freshness_rejects_stale_revision():
    doc = _base_snapshot()
    doc["entries"][0]["revision"] = "9" * 40  # != run.repository_revision
    f = RecordingFindings()
    vdc.check_source_freshness(f, "t", doc)
    assert "stale-revision" in f.error_codes()


def test_source_freshness_rejects_stale_snapshot_id():
    doc = _base_snapshot()
    doc["entries"][0]["snapshot_id"] = "some-other-snapshot"
    f = RecordingFindings()
    vdc.check_source_freshness(f, "t", doc)
    assert "stale-snapshot" in f.error_codes()


# ------------------ 4b. review-binding freshness (override source hash) ------------------

def test_review_source_freshness_accepts_override_bound_to_current_hash():
    doc = _reviewed_entry_snapshot()
    f = RecordingFindings()
    vdc.check_review_source_freshness(f, "t", doc, _matching_overrides())
    assert not f.errors


def test_review_source_freshness_rejects_retained_standing_after_content_change():
    """spec scenario "Source content changes after review": the entry's
    content_hash moved past the override's bound source_content_hash while
    the facet silently stayed reviewed — must be rejected, never retained."""
    doc = _reviewed_entry_snapshot()
    doc["entries"][0]["content_hash"] = "5" * 64  # content changed after review
    f = RecordingFindings()
    vdc.check_review_source_freshness(f, "t", doc, _matching_overrides())
    assert "stale-review" in f.error_codes()


def test_review_source_freshness_allows_reclassified_entry_after_content_change():
    """The compliant half of the same scenario: after the content change the
    entry re-entered classification (state back to suggested), so the stale
    override alone is no violation."""
    doc = _base_snapshot()
    doc["entries"][0]["content_hash"] = "5" * 64
    doc["entries"][0]["facet_assignments"] = [
        {
            "facet": "document_role",
            "values": ["process"],
            "state": "suggested",
            "state_since": "2026-07-13",
            "transitions": [],
        },
    ]
    f = RecordingFindings()
    vdc.check_review_source_freshness(f, "t", doc, _matching_overrides())
    assert not f.errors


def test_review_source_freshness_discloses_unmatched_review_instead_of_guessing():
    """A reviewed facet with no matching override in the supplied file is
    disclosed as unverifiable (note), never silently accepted or fabricated
    into an error — the owning repo's own overrides pass holds that truth."""
    doc = _reviewed_entry_snapshot()
    f = RecordingFindings()
    vdc.check_review_source_freshness(f, "t", doc, overrides_doc=None)
    assert not f.errors
    assert any("no matching override" in n for n in f.notes)


# --------------------------- 5. taxonomy resolution ---------------------------

def test_taxonomy_registries_accepts_disjoint_namespaces():
    registries = {
        "neutral": {"namespaces": [{"id": "xfactory", "owner": "openxFactory"}], "tags": []},
        "domain": {"namespaces": [{"id": "medx", "owner": "xFactories/MedxFactory"}], "tags": []},
    }
    f = RecordingFindings()
    vdc.check_taxonomy_registries(f, registries)
    assert not f.errors


def test_taxonomy_registries_rejects_namespace_owner_collision():
    registries = {
        "neutral": {"namespaces": [{"id": "medx", "owner": "openxFactory"}], "tags": []},
        "domain": {"namespaces": [{"id": "medx", "owner": "xFactories/MedxFactory"}], "tags": []},
    }
    f = RecordingFindings()
    vdc.check_taxonomy_registries(f, registries)
    assert "namespace-collision" in f.error_codes()


def test_taxonomy_registries_rejects_tag_alias_collision_across_owners():
    registries = {
        "neutral": {
            "namespaces": [{"id": "xfactory", "owner": "openxFactory"}],
            "tags": [{"id": "xfactory.governance", "namespace": "xfactory", "aliases": ["shared.alias"]}],
        },
        "domain": {
            "namespaces": [{"id": "medx", "owner": "xFactories/MedxFactory"}],
            "tags": [{"id": "medx.ops", "namespace": "medx", "aliases": ["shared.alias"]}],
        },
    }
    f = RecordingFindings()
    vdc.check_taxonomy_registries(f, registries)
    assert "tag-collision" in f.error_codes()


def test_topic_tag_resolution_rejects_tag_absent_from_effective_registry():
    doc = _base_snapshot()
    doc["entries"][0]["facet_assignments"] = [
        {"facet": "topic_tags", "values": ["medx.unregistered"], "state": "suggested", "state_since": "2026-07-12"},
    ]
    registries = {
        "neutral": {"tags": [{"id": "xfactory.document-governance", "status": "active", "aliases": []}]},
    }
    f = RecordingFindings()
    vdc.check_topic_tag_resolution(f, "t", doc, registries)
    assert "topic-unresolved" in f.error_codes()


def test_topic_tag_resolution_accepts_active_registered_tag():
    doc = _base_snapshot()
    doc["entries"][0]["facet_assignments"] = [
        {"facet": "topic_tags", "values": ["xfactory.document-governance"], "state": "suggested", "state_since": "2026-07-12"},
    ]
    registries = {
        "neutral": {"tags": [{"id": "xfactory.document-governance", "status": "active", "aliases": []}]},
    }
    f = RecordingFindings()
    vdc.check_topic_tag_resolution(f, "t", doc, registries)
    assert not f.errors


def test_capability_resolution_accepts_known_openxfactory_capability():
    doc = _base_snapshot()
    doc["entries"][0]["facet_assignments"] = [
        {
            "facet": "capability_refs",
            "values": [{"repository": "openxFactory", "capability": "document-lifecycle"}],
            "state": "suggested",
            "state_since": "2026-07-12",
        },
    ]
    f = RecordingFindings()
    vdc.check_capability_resolution(f, "t", doc)
    assert not f.errors


def test_capability_resolution_rejects_unknown_openxfactory_capability():
    doc = _base_snapshot()
    doc["entries"][0]["facet_assignments"] = [
        {
            "facet": "capability_refs",
            "values": [{"repository": "openxFactory", "capability": "totally-invented-capability"}],
            "state": "suggested",
            "state_since": "2026-07-12",
        },
    ]
    f = RecordingFindings()
    vdc.check_capability_resolution(f, "t", doc)
    assert "capability-unresolved" in f.error_codes()


def test_taxonomy_digest_consistency_accepts_matching_inputs_and_digest():
    doc_a = _base_snapshot()
    doc_b = copy.deepcopy(doc_a)
    doc_b["run"]["run_id"] = "RUN-2"
    f = RecordingFindings()
    vdc.check_taxonomy_digest_consistency(f, [("a", doc_a), ("b", doc_b)])
    assert not f.errors


def test_taxonomy_digest_consistency_rejects_same_inputs_different_digest():
    doc_a = _base_snapshot()
    doc_b = copy.deepcopy(doc_a)
    doc_b["taxonomy"]["digest"] = "9" * 64  # inputs unchanged, digest changed -> inconsistent
    f = RecordingFindings()
    vdc.check_taxonomy_digest_consistency(f, [("a", doc_a), ("b", doc_b)])
    assert "taxonomy-digest-inconsistent" in f.error_codes()


def test_taxonomy_digest_consistency_ignores_unrelated_revision_changes():
    """Spec scenario "Registry repository changes elsewhere": a
    repository_revision/registry_revision-only change must not be treated
    as an inconsistency."""
    doc_a = _base_snapshot()
    doc_b = copy.deepcopy(doc_a)
    doc_b["taxonomy"]["inputs"][0]["repository_revision"] = "f" * 40
    doc_b["taxonomy"]["inputs"][0]["registry_revision"] = "f" * 40
    f = RecordingFindings()
    vdc.check_taxonomy_digest_consistency(f, [("a", doc_a), ("b", doc_b)])
    assert not f.errors


# --------------------------- 6. override standing ---------------------------

def test_override_standing_accepts_matching_domain_authority():
    doc = {
        "overrides": [
            {"repo": "xFactories/MedxFactory", "actor": "xFactories/MedxFactory authority (Domain Hermes)"},
        ],
    }
    f = RecordingFindings()
    vdc.check_override_standing(f, "t", doc)
    assert not f.errors


def test_override_standing_accepts_matching_neutral_authority():
    doc = {"overrides": [{"repo": "openxFactory", "actor": "openxFactory ratify authority"}]}
    f = RecordingFindings()
    vdc.check_override_standing(f, "t", doc)
    assert not f.errors


def test_override_standing_rejects_wrong_domain_actor():
    """spec scenario "Unauthorized override is supplied": an actor naming a
    different domain's authority has no standing over this repo."""
    doc = {
        "overrides": [
            {"repo": "xFactories/MedxFactory", "actor": "xFactories/OpsxFactory authority (Domain Hermes)"},
        ],
    }
    f = RecordingFindings()
    vdc.check_override_standing(f, "t", doc)
    assert "override-standing" in f.error_codes()


def test_override_standing_rejects_neutral_authority_on_domain_repo():
    doc = {
        "overrides": [
            {"repo": "xFactories/MedxFactory", "actor": "openxFactory ratify authority"},
        ],
    }
    f = RecordingFindings()
    vdc.check_override_standing(f, "t", doc)
    assert "override-standing" in f.error_codes()


def test_override_standing_rejects_domain_authority_on_neutral_repo():
    doc = {"overrides": [{"repo": "openxFactory", "actor": "xFactories/MedxFactory authority (Domain Hermes)"}]}
    f = RecordingFindings()
    vdc.check_override_standing(f, "t", doc)
    assert "override-standing" in f.error_codes()


# ------------------ 6b. override standing on snapshot review blocks ------------------

def test_snapshot_review_standing_accepts_owning_domain_authority():
    doc = _reviewed_entry_snapshot()
    f = RecordingFindings()
    vdc.check_snapshot_review_standing(f, "t", doc)
    assert not f.errors


def test_snapshot_review_standing_rejects_unauthorized_actor():
    """Review-finding repro: a committed snapshot whose review.authority is
    an arbitrary unauthorized string must fail standing (spec scenario
    "Unauthorized override is supplied", enforced on the merged artifact
    where reviewed/overridden state actually lives)."""
    doc = _reviewed_entry_snapshot(authority="random-unauthorized-actor")
    f = RecordingFindings()
    vdc.check_snapshot_review_standing(f, "t", doc)
    assert "override-standing" in f.error_codes()


def test_snapshot_review_standing_rejects_neutral_authority_on_domain_entry():
    doc = _reviewed_entry_snapshot(authority="openxFactory ratify authority")
    f = RecordingFindings()
    vdc.check_snapshot_review_standing(f, "t", doc)
    assert "override-standing" in f.error_codes()


def test_snapshot_review_standing_rejects_domain_authority_on_neutral_entry():
    doc = _reviewed_entry_snapshot()  # authority stays MedxFactory Domain Hermes
    doc["entries"][0]["repo"] = "openxFactory"
    f = RecordingFindings()
    vdc.check_snapshot_review_standing(f, "t", doc)
    assert "override-standing" in f.error_codes()


# --------------------------- 7. immutable path layout ---------------------------

def test_immutable_path_layout_accepts_conformant_snapshot_path(tmp_path):
    doc = _base_snapshot()
    doc["run"]["run_id"] = "RUN-1"
    doc["run"]["repository"] = "xFactories/MedxFactory"
    path = tmp_path / "health" / "document-catalog" / "runs" / "2026-07-13" / "RUN-1" / "xFactories" / "MedxFactory.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("placeholder")
    f = RecordingFindings()
    vdc.check_immutable_path_layout(f, tmp_path, path, doc, kind="snapshot")
    assert not f.errors


def test_immutable_path_layout_rejects_run_id_mismatch(tmp_path):
    doc = _base_snapshot()
    doc["run"]["run_id"] = "RUN-1"
    doc["run"]["repository"] = "xFactories/MedxFactory"
    path = tmp_path / "health" / "document-catalog" / "runs" / "2026-07-13" / "RUN-DIFFERENT" / "xFactories" / "MedxFactory.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("placeholder")
    f = RecordingFindings()
    vdc.check_immutable_path_layout(f, tmp_path, path, doc, kind="snapshot")
    assert "path-layout" in f.error_codes()


def test_immutable_path_layout_rejects_bad_date_segment(tmp_path):
    doc = _base_snapshot()
    doc["run"]["run_id"] = "RUN-1"
    doc["run"]["repository"] = "xFactories/MedxFactory"
    path = tmp_path / "health" / "document-catalog" / "runs" / "not-a-date" / "RUN-1" / "xFactories" / "MedxFactory.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("placeholder")
    f = RecordingFindings()
    vdc.check_immutable_path_layout(f, tmp_path, path, doc, kind="snapshot")
    assert "path-layout" in f.error_codes()


def test_immutable_path_layout_accepts_conformant_recommendation_path(tmp_path):
    doc = {"job_id": "CATJOB-2026-07-13-001"}
    path = tmp_path / "health" / "document-catalog" / "recommendations" / "2026-07-13" / "CATJOB-2026-07-13-001.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("placeholder")
    f = RecordingFindings()
    vdc.check_immutable_path_layout(f, tmp_path, path, doc, kind="recommendation")
    assert not f.errors


def test_immutable_path_layout_rejects_job_id_mismatch_in_recommendation_filename(tmp_path):
    doc = {"job_id": "CATJOB-2026-07-13-001"}
    path = tmp_path / "health" / "document-catalog" / "recommendations" / "2026-07-13" / "some-other-job.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("placeholder")
    f = RecordingFindings()
    vdc.check_immutable_path_layout(f, tmp_path, path, doc, kind="recommendation")
    assert "path-layout" in f.error_codes()


# --------------------------- 8. baseline-mode exceptions ---------------------------

def test_baseline_mode_downgrades_missing_coverage_to_warning():
    doc = _base_snapshot()
    f = RecordingFindings()
    inventory = [
        {"repo": "xFactories/MedxFactory", "path": "docs/one.md"},
        {"repo": "xFactories/MedxFactory", "path": "docs/two.md"},
        {"repo": "xFactories/MedxFactory", "path": "docs/three.md"},
    ]
    vdc.check_complete_coverage(f, "t", doc, inventory, baseline=True)
    assert not f.errors
    assert "coverage-missing" in f.warning_codes()


def test_non_baseline_mode_keeps_missing_coverage_as_error():
    doc = _base_snapshot()
    f = RecordingFindings()
    inventory = [
        {"repo": "xFactories/MedxFactory", "path": "docs/one.md"},
        {"repo": "xFactories/MedxFactory", "path": "docs/two.md"},
        {"repo": "xFactories/MedxFactory", "path": "docs/three.md"},
    ]
    vdc.check_complete_coverage(f, "t", doc, inventory, baseline=False)
    assert "coverage-missing" in f.error_codes()
    assert not f.warning_codes()


# --------------------------- repo-tree integration (end to end) ---------------------------

def _write_synthetic_repo_tree(tmp_path, snapshot_doc: dict) -> None:
    """A small synthetic repo tree: a neutral registry, an authorized
    override binding docs/one.md's content hash, and one snapshot at the
    conformant immutable path."""
    (tmp_path / "contracts").mkdir()
    (tmp_path / "contracts" / "document-tag-registry.yaml").write_text(
        "schema_version: 1\n"
        "kind: xfactory_document_tag_registry\n"
        "registry_version: 1\n"
        "namespaces:\n"
        "  - {id: xfactory, owner: openxFactory, description: neutral}\n"
        "tags:\n"
        "  - {id: xfactory.document-governance, namespace: xfactory, label: x, description: x, aliases: [], status: active}\n"
        "proposed_tags: []\n"
        "retired_tags: []\n"
    )
    (tmp_path / "catalog").mkdir()
    (tmp_path / "catalog" / "document-tag-overrides.yaml").write_text(_dump_yaml(_matching_overrides()))
    run_dir = tmp_path / "health" / "document-catalog" / "runs" / "2026-07-13" / "RUN-1" / "xFactories"
    run_dir.mkdir(parents=True)
    (run_dir / "MedxFactory.yaml").write_text(_dump_yaml(snapshot_doc))


def test_repo_tree_end_to_end_against_a_synthetic_repo(tmp_path):
    """Wires a small synthetic repo tree through check_repo_tree end to end:
    a registry pair, an authorized override, and one conformant snapshot
    whose reviewed facet is disposed by the owning authority against the
    current content hash, proving the real-artifact layer (not just the
    packaged examples)."""
    _write_synthetic_repo_tree(tmp_path, _reviewed_entry_snapshot())
    registry, docs = vdc.build_registry()
    f = RecordingFindings()
    vdc.check_repo_tree(f, registry, docs, tmp_path, baseline=False, inventory=None)
    assert not f.errors, f.errors


def test_repo_tree_rejects_unauthorized_review_and_stale_binding_in_snapshot(tmp_path):
    """Review-finding repro on the real-artifact layer: a committed
    `status: record` snapshot carrying an unauthorized review.authority AND
    a reviewed facet whose entry content_hash moved past the override's
    bound source_content_hash must fail check_repo_tree — it previously
    passed every check cleanly."""
    doc = _reviewed_entry_snapshot(authority="random-unauthorized-actor")
    doc["entries"][0]["content_hash"] = "5" * 64  # != override's bound "3"*64
    _write_synthetic_repo_tree(tmp_path, doc)
    registry, docs = vdc.build_registry()
    f = RecordingFindings()
    vdc.check_repo_tree(f, registry, docs, tmp_path, baseline=False, inventory=None)
    assert "override-standing" in f.error_codes()
    assert "stale-review" in f.error_codes()


def _dump_yaml(doc: dict) -> str:
    import yaml
    return yaml.safe_dump(doc, sort_keys=False)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
