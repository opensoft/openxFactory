"""Tests for the doxBench additions to
scripts/validate-ideation-dashboard-contracts.py
(add-workbench-integrated-editor-chat, change tasks 2.1-2.4).

The script's own `main()` self-tests every packaged example under
`examples/ideation-dashboard/` (see its `check_examples`). This suite targets
the doxBench contract family one clause at a time — the two schemas load into
the offline registry; every doxBench positive validates; each negative fails
for exactly the reason its filename declares; the request-buffer hash parity,
budget, unknown-model, duplicate-turn-id, proposal-target, and
failure-envelope rules fire and stay quiet correctly; and the pre-existing
dashboard/session artifacts remain valid so no pre-growth snapshot or gate
record is invalidated (task 2.4's compatibility clause).

Follows tests/ideation_routing's harness pattern (importlib module-load for a
hyphenated script + one subprocess end-to-end)."""
from __future__ import annotations

import copy
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validate-ideation-dashboard-contracts.py"
SCHEMAS = ROOT / "contracts" / "schemas"
EXAMPLES = ROOT / "examples" / "ideation-dashboard"
NEGATIVE = EXAMPLES / "negative"

CATALOG_SCHEMA = SCHEMAS / "xfactory-workbench-model-catalog.schema.yaml"
TURN_SCHEMA = SCHEMAS / "xfactory-workbench-chat-turn.schema.yaml"


def _load_module():
    spec = importlib.util.spec_from_file_location("vidc", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def vidc():
    return _load_module()


@pytest.fixture(scope="module")
def registry_docs(vidc):
    return vidc.build_registry()


def _validate(vidc, registry_docs, name, doc, ctx=None):
    registry, docs = registry_docs
    f = vidc.Findings()
    vidc.validate_instance(f, name, doc, registry, docs, set(), model_ctx=ctx)
    return f


def _example(name):
    return yaml.safe_load((EXAMPLES / name).read_text(encoding="utf-8"))


# ---- 2.1: the two schemas exist and join the family registry ---------------

def test_the_two_doxbench_schemas_exist_and_load(vidc, registry_docs):
    assert CATALOG_SCHEMA.is_file(), "task 2.1: catalog schema missing"
    assert TURN_SCHEMA.is_file(), "task 2.1: chat-turn schema missing"
    for kind in ("workbench-model-catalog", "workbench-chat-turn",
                 "workbench-chat-turn-success", "workbench-chat-turn-failure"):
        assert kind in vidc.KIND_TO_SCHEMA
    _registry, docs = registry_docs
    assert "xfactory-workbench-model-catalog.schema.yaml" in docs
    assert "xfactory-workbench-chat-turn.schema.yaml" in docs


# ---- 2.2: every packaged doxBench positive validates ------------------------

DOXBENCH_POSITIVES = (
    "workbench-model-catalog-empty.example.yaml",
    "workbench-model-catalog-local.example.yaml",
    "workbench-model-catalog-hosted-zero-retention.example.yaml",
    "workbench-chat-turn-unsaved-edits.example.yaml",
    "workbench-chat-turn-outline-only.example.yaml",
    "workbench-chat-turn-prose-only.example.yaml",
    "workbench-chat-turn-both-proposals.example.yaml",
)


@pytest.mark.parametrize("name", DOXBENCH_POSITIVES)
def test_doxbench_positive_examples_validate(vidc, registry_docs, name):
    f = _validate(vidc, registry_docs, name, _example(name))
    assert not f.errors, f.errors


# ---- 2.3: each negative fails for its intended reason -----------------------

NEGATIVES = {
    "workbench-model-catalog-exposed-credential.negative.yaml": "credential",
    "workbench-model-catalog-raw-endpoint.negative.yaml": "endpoint",
    "workbench-chat-turn-unknown-model.negative.yaml": "unknown-model",
    "workbench-chat-turn-hash-mismatch.negative.yaml": "hash",
    "workbench-chat-turn-escaping-path.negative.yaml": "path",
    "workbench-chat-turn-over-budget.negative.yaml": "budget",
    "workbench-chat-turn-untyped-proposal.negative.yaml": "proposal",
    "workbench-chat-turn-identity-subject.negative.yaml": "working_subject",
}


@pytest.mark.parametrize("name,needle", sorted(NEGATIVES.items()))
def test_each_negative_fails_for_its_named_reason(vidc, registry_docs, name, needle):
    doc = yaml.safe_load((NEGATIVE / name).read_text(encoding="utf-8"))
    ctx = vidc.catalog_model_ids_from(_example(
        "workbench-model-catalog-local.example.yaml"))
    f = _validate(vidc, registry_docs, name, doc, ctx)
    assert f.errors, f"{name}: expected invalid"
    assert any(needle in e for e in f.errors), (needle, f.errors)


def test_duplicate_turn_ids_with_different_content_are_refused(vidc):
    pair_dir = NEGATIVE / "duplicate-turn-pair"
    f = vidc.Findings()
    vidc.check_turn_id_uniqueness(f, sorted(pair_dir.glob("*.yaml")))
    assert any("duplicate-turn" in e for e in f.errors), f.errors


# ---- semantic rules: fire AND stay quiet correctly --------------------------

def test_request_hash_parity_rule_is_exact(vidc, registry_docs):
    doc = _example("workbench-chat-turn-unsaved-edits.example.yaml")
    bad = copy.deepcopy(doc)
    bad["buffers"][0]["content_hash"] = "0" * 64
    f = _validate(vidc, registry_docs, "mutated", bad)
    assert any("hash" in e for e in f.errors)


def test_over_budget_is_skipped_without_catalog_context(vidc, registry_docs):
    doc = yaml.safe_load((NEGATIVE /
        "workbench-chat-turn-over-budget.negative.yaml").read_text(encoding="utf-8"))
    f = _validate(vidc, registry_docs, "no-ctx", doc, ctx=None)
    budget_errors = [e for e in f.errors if "budget" in e]
    assert not budget_errors, "budget must SKIP without catalog context"


def test_success_proposal_targets_must_be_unique(vidc, registry_docs):
    doc = _example("workbench-chat-turn-both-proposals.example.yaml")
    # find the embedded success answer inside the example bundle
    success = doc if doc.get("kind") == "workbench-chat-turn-success" else None
    assert success is not None
    bad = copy.deepcopy(success)
    bad["proposals"][1]["target"] = bad["proposals"][0]["target"]
    f = _validate(vidc, registry_docs, "dup-target", bad)
    assert any("proposal" in e for e in f.errors)


# ---- 2.4: pre-growth artifacts remain valid (compatibility clause) ----------

def test_pre_existing_dashboard_examples_still_validate(vidc, registry_docs):
    for name in ("ideation-dashboard-snapshot.example.yaml",
                 "gate-action-record-edit-document.example.yaml"):
        f = _validate(vidc, registry_docs, name, _example(name))
        assert not f.errors, (name, f.errors)


def test_end_to_end_self_test_passes(tmp_path):
    # The sanctioned default invocation: packaged-example self-test (positives,
    # negatives, the duplicate-turn pair) plus the committed-manifest guard.
    # The explicit-REPO full-tree sweep is a different mode and trips
    # pre-existing unrelated YAML outside this contract family.
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=str(ROOT),
        capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "0 error(s)" in proc.stdout
    # …and it is NOT silent about the deprecated family (contract-v1.34): the
    # four packaged v1 chat-turn examples each raise one warning and are each
    # still ACCEPTED, which is the deprecating change class exactly — warn, do
    # not refuse. The count is the pin, so a deprecation that stopped warning
    # (or one that started refusing) fails here.
    assert "4 warning(s)" in proc.stdout
    assert proc.stdout.count("is DEPRECATED as of contract-v1.34") == 4


def test_a_deprecated_kind_warns_and_is_still_accepted(vidc, registry_docs):
    """The deprecating class, per instance: `docs/contract-versioning-policy.md`
    says the conformance validator "emits warnings but still accepts it". Before
    this, `deprecated_envelopes` was read by nothing, so the release could claim
    to start the clock the breaking path requires while every conforming v1
    instance validated in silence."""
    f = _validate(vidc, registry_docs, "v1-request",
                  _example("workbench-chat-turn-unsaved-edits.example.yaml"))
    assert not f.errors, f.errors
    assert any("is DEPRECATED" in w and "workbench-chat-turn" in w
               for w in f.warnings), f.warnings
    assert any("contract-v2.0" in w for w in f.warnings), (
        "the warning names the removal target, which is the half a consumer "
        "has to plan against")


def test_the_widened_family_is_not_warned_about(vidc, registry_docs):
    """The other half: the replacement must not carry the warning, or the signal
    means nothing."""
    f = _validate(vidc, registry_docs, "v2-request",
                  _example("workbench-chat-turn-v2-loaded-set.example.yaml"))
    assert not f.errors, f.errors
    assert not any("DEPRECATED" in w for w in f.warnings), f.warnings


def test_the_deprecated_list_is_read_from_the_schema_never_restated(vidc,
                                                                    registry_docs):
    """The validator carries no list of its own: it reads the schemas' declared
    `deprecated_envelopes`. A second copy here would be a second authority that
    could disagree with the bytes consumers pin."""
    _registry, docs = registry_docs
    declared = vidc.deprecated_kinds(docs)
    assert set(declared) == {"workbench-chat-turn",
                             "workbench-chat-turn-success",
                             "workbench-chat-turn-failure"}
    source = SCRIPT.read_text(encoding="utf-8")
    # The kinds appear as SCHEMA ROUTING entries, never as a deprecation list.
    assert "deprecated_envelopes" in source
    for spelling in ('"workbench-chat-turn": "contract-v1.34"',
                     "DEPRECATED_KINDS = "):
        assert spelling not in source


def test_websocket_endpoints_are_caught_by_the_spelling_scan(vidc, registry_docs):
    """Hardening (PR #45 review finding 2): the endpoint scan covers ws/wss
    alongside http/https — a streaming endpoint is as raw as a REST one."""
    doc = copy.deepcopy(_example("workbench-model-catalog-local.example.yaml"))
    doc["models"][0]["data_handling"] = "streams via wss://provider.internal/live"
    f = _validate(vidc, registry_docs, "wss-mutant", doc)
    assert any("endpoint" in e for e in f.errors), f.errors


def test_reversed_buffer_order_is_not_a_turn_id_conflict(vidc, tmp_path):
    """PR #45 Copilot blocker 3: the duplicate-turn sweep canonicalizes buffer
    order by kind before hashing — a retransmission that merely reorders
    [outline, document] is the SAME request, not an FR-019 conflict."""
    doc = _example("workbench-chat-turn-unsaved-edits.example.yaml")
    rev = copy.deepcopy(doc)
    rev["buffers"] = list(reversed(rev["buffers"]))
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    a.write_text(yaml.safe_dump(doc), encoding="utf-8")
    b.write_text(yaml.safe_dump(rev), encoding="utf-8")
    f = vidc.Findings()
    vidc.check_turn_id_uniqueness(f, [a, b])
    assert not f.errors, f.errors


def test_a_turn_may_carry_a_null_active_document_path(vidc, registry_docs):
    """G-1 (codexFactory PR #63 re-verification, 2026-08-02): a tile whose ONLY
    editable path is its own primary fragment — which the canvas loads as the
    OUTLINE — has no separate document to name, and 16 of 21 real staged topics
    are that shape. The request's `active_document_path` is therefore nullable,
    MIRRORING `buffer_state.path` exactly: still a required key, `null` when no
    document backs the buffer. Additive: every instance that names a path is
    unaffected, and confinement still judges only paths that exist."""
    doc = copy.deepcopy(_example("workbench-chat-turn-unsaved-edits.example.yaml"))
    doc["active_document_path"] = None
    doc["buffers"][1]["path"] = None
    ctx = vidc.catalog_model_ids_from(_example(
        "workbench-model-catalog-local.example.yaml"))
    f = _validate(vidc, registry_docs, "null-active-document", doc, ctx)
    assert not f.errors, f.errors


def test_an_escaping_active_document_path_is_still_refused(vidc, registry_docs):
    """The nullability above widens the shape by exactly one value. A path that
    EXISTS is judged exactly as before."""
    doc = copy.deepcopy(_example("workbench-chat-turn-unsaved-edits.example.yaml"))
    doc["active_document_path"] = "../outside/note.md"
    ctx = vidc.catalog_model_ids_from(_example(
        "workbench-model-catalog-local.example.yaml"))
    f = _validate(vidc, registry_docs, "escaping-active-document", doc, ctx)
    assert any("path" in e for e in f.errors), f.errors


def test_a_new_artifact_buffer_may_carry_a_null_path(vidc, registry_docs):
    """PR #45 Copilot blocker 4: a not-yet-created artifact has no path yet
    (the null-path -> create lifecycle, data-model §4); the buffer's path is
    nullable while every other identity field stays required."""
    doc = copy.deepcopy(_example("workbench-chat-turn-unsaved-edits.example.yaml"))
    doc["buffers"][1]["path"] = None
    ctx = vidc.catalog_model_ids_from(_example(
        "workbench-model-catalog-local.example.yaml"))
    f = _validate(vidc, registry_docs, "null-path", doc, ctx)
    assert not f.errors, f.errors
