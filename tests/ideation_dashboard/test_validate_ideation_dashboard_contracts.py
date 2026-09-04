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
    for kind in ("workbench-model-catalog", "workbench-chat-turn-v2",
                 "workbench-chat-turn-v2-success",
                 "workbench-chat-turn-v2-failure"):
        assert kind in vidc.KIND_TO_SCHEMA
    # …and the retired family routes to nothing (contract-v3.0,
    # retire-doxbench-chat-turn-v1). An instance declaring one of these kinds is
    # an UNKNOWN kind to this validator now, which is what makes the packaged
    # `workbench-chat-turn-unrecognized-kind` negative fail for its named reason.
    for retired in ("workbench-chat-turn", "workbench-chat-turn-success",
                    "workbench-chat-turn-failure"):
        assert retired not in vidc.KIND_TO_SCHEMA
    _registry, docs = registry_docs
    assert "xfactory-workbench-model-catalog.schema.yaml" in docs
    assert "xfactory-workbench-chat-turn.schema.yaml" in docs


# ---- 2.2: every packaged doxBench positive validates ------------------------

# The four v1 turn positives — `-unsaved-edits`, `-outline-only`,
# `-prose-only`, `-both-proposals` — left with their family at contract-v3.0
# (retire-doxbench-chat-turn-v1) and the surviving family's own instances stand
# in their place. Not a like-for-like swap: what each v1 file demonstrated is
# demonstrated here by whichever v2 instance carries the same claim (the loaded
# set for a request, the record for a success, and the two posture records this
# validator's redaction scan reaches), and there is nothing to migrate for the
# claims that were about v1's shape alone.
DOXBENCH_POSITIVES = (
    "workbench-model-catalog-empty.example.yaml",
    "workbench-model-catalog-local.example.yaml",
    "workbench-model-catalog-hosted-zero-retention.example.yaml",
    "workbench-chat-turn-v2-loaded-set.example.yaml",
    "workbench-chat-turn-v2-success.example.yaml",
    "workbench-chat-turn-v2-reduced-context.example.yaml",
    "workbench-chat-turn-v2-full-context.example.yaml",
    "workbench-chat-turn-v2-provider-retry.example.yaml",
)


@pytest.mark.parametrize("name", DOXBENCH_POSITIVES)
def test_doxbench_positive_examples_validate(vidc, registry_docs, name):
    f = _validate(vidc, registry_docs, name, _example(name))
    assert not f.errors, f.errors


# ---- 2.3: each negative fails for its intended reason -----------------------

# RE-EXPRESSED, NOT DROPPED, at contract-v3.0 (retire-doxbench-chat-turn-v1).
# Six of these refusal classes were only ever packaged against a v1 instance, so
# removing the family would have silently retired six negatives; each has a `-v2`
# fixture carrying the same defect in the surviving envelope, and the mapping
# below is what keeps the classes covered rather than merely renamed. The
# seventh row is NEW and belongs to the removal itself: a chat-turn `kind` this
# release does not serve.
NEGATIVES = {
    "workbench-model-catalog-exposed-credential.negative.yaml": "credential",
    "workbench-model-catalog-raw-endpoint.negative.yaml": "endpoint",
    "workbench-chat-turn-v2-unknown-model.negative.yaml": "unknown-model",
    "workbench-chat-turn-v2-hash-mismatch.negative.yaml": "hash",
    "workbench-chat-turn-v2-escaping-path.negative.yaml": "path",
    "workbench-chat-turn-v2-over-budget.negative.yaml": "budget",
    "workbench-chat-turn-v2-untyped-proposal.negative.yaml": "proposal",
    "workbench-chat-turn-v2-identity-subject.negative.yaml": "working_subject",
    "workbench-chat-turn-unrecognized-kind.negative.yaml": "unrecognized document",
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
    doc = _example("workbench-chat-turn-v2-loaded-set.example.yaml")
    bad = copy.deepcopy(doc)
    bad["buffers"][0]["content_hash"] = "0" * 64
    f = _validate(vidc, registry_docs, "mutated", bad)
    assert any("hash" in e for e in f.errors)


def test_over_budget_is_skipped_without_catalog_context(vidc, registry_docs):
    doc = yaml.safe_load((NEGATIVE /
        "workbench-chat-turn-v2-over-budget.negative.yaml").read_text(encoding="utf-8"))
    f = _validate(vidc, registry_docs, "no-ctx", doc, ctx=None)
    budget_errors = [e for e in f.errors if "budget" in e]
    assert not budget_errors, "budget must SKIP without catalog context"


def test_success_proposal_targets_must_be_unique(vidc, registry_docs):
    """RE-EXPRESSED on the surviving record at contract-v3.0
    (retire-doxbench-chat-turn-v1). It ran on the v1 `-both-proposals` example,
    which carried the only packaged two-proposal record; the surviving success
    instance carries one, so the second is CONSTRUCTED here from the first
    rather than read off a file. The rule under test is unchanged — two
    proposals may not name the same target — and the target is now a buffer key
    rather than v1's two-value enum, which is the only reason a duplicate has to
    be built by hand at all."""
    success = _example("workbench-chat-turn-v2-success.example.yaml")
    assert success.get("kind") == "workbench-chat-turn-v2-success"
    bad = copy.deepcopy(success)
    assert len(bad["proposals"]) == 1, bad["proposals"]
    bad["proposals"].append(copy.deepcopy(bad["proposals"][0]))
    f = _validate(vidc, registry_docs, "dup-target", bad)
    assert any("proposal" in e for e in f.errors), f.errors


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
    # …and it is SILENT again (contract-v3.0, retire-doxbench-chat-turn-v1).
    #
    # It reported `4 warning(s)` here for thirteen minors and one major: the four
    # packaged v1 chat-turn examples each raised one deprecation warning and were
    # each still ACCEPTED, which is the deprecating change class exactly. The
    # count was the pin, so a deprecation that stopped warning — or one that
    # started refusing — failed here.
    #
    # The count is STILL the pin, and it is now zero, which is a stronger
    # statement than dropping the assertion: nothing in the packaged corpus is
    # deprecated, and a release that deprecated something without packaging the
    # warning, or left a stale warning behind after removing its subject, fails
    # here exactly as a stopped warning used to.
    assert "0 warning(s)" in proc.stdout
    assert "is DEPRECATED" not in proc.stdout


def test_the_deprecation_reader_survives_its_only_subject(vidc, registry_docs):
    """Three tests stood here and pinned contract-v1.34's warn-do-not-refuse
    bargain from three angles: that a v1 instance warned and was still accepted,
    that the widened family did NOT carry the warning (or the signal would mean
    nothing), and that the list came from the schemas rather than from a copy
    inside the validator. The first two went with their subject at contract-v3.0
    (retire-doxbench-chat-turn-v1); the third is re-expressed here, because what
    it actually protects outlived the family it was written against.

    `deprecated_kinds` is GENERAL machinery, not v1 machinery: it reads whatever
    any loaded schema declares. The chat-turn v1 family was its only subject in
    the estate, so over the packaged schemas it now returns nothing — and that is
    the correct answer to the question rather than evidence the reader is dead.
    Deleting it because its only current subject went would have left the
    estate's next deprecation inert, which is the precise failure this whole
    retirement exists to correct: contract-v1.34 declared a removal target that
    contract-v2.0 shipped straight past, and the only thing that noticed was a
    warning nobody read."""
    _registry, docs = registry_docs
    assert vidc.deprecated_kinds(docs) == {}
    source = SCRIPT.read_text(encoding="utf-8")
    # The reader still reads. A second copy in the validator would be a second
    # authority that could disagree with the bytes consumers pin — and a hardcoded
    # list is exactly what an empty result invites somebody to add back.
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
    doc = _example("workbench-chat-turn-v2-loaded-set.example.yaml")
    rev = copy.deepcopy(doc)
    rev["buffers"] = list(reversed(rev["buffers"]))
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    a.write_text(yaml.safe_dump(doc), encoding="utf-8")
    b.write_text(yaml.safe_dump(rev), encoding="utf-8")
    f = vidc.Findings()
    vidc.check_turn_id_uniqueness(f, [a, b])
    assert not f.errors, f.errors


def test_a_turn_may_be_bound_to_the_outline_alone(vidc, registry_docs):
    """G-1 (codexFactory PR #63 re-verification, 2026-08-02): a tile whose ONLY
    editable path is its own primary fragment — which the canvas loads as the
    OUTLINE — has no separate document to name, and 16 of 21 real staged topics
    are that shape. v1 expressed that as a nullable `active_document_path`,
    MIRRORING `buffer_state.path`: still a required key, `null` when no document
    backs the buffer.

    RE-EXPRESSED at contract-v3.0 (retire-doxbench-chat-turn-v1). The surviving
    request has no such field, and does not need one — the binding is DECLARED,
    so a turn grounded on the outline alone simply names the reserved `outline`
    key. The G-1 shape is the same shape; what it costs to express went from a
    nullable field to nothing at all."""
    doc = copy.deepcopy(_example("workbench-chat-turn-v2-loaded-set.example.yaml"))
    doc["bound_buffer"] = "outline"
    ctx = vidc.catalog_model_ids_from(_example(
        "workbench-model-catalog-local.example.yaml"))
    f = _validate(vidc, registry_docs, "outline-bound", doc, ctx)
    assert not f.errors, f.errors


def test_a_binding_that_escapes_the_checkout_is_still_refused(vidc, registry_docs):
    """The other side of the same coin: a binding that names a PATH is confined
    exactly as any other path is. (This asserted the same rule about v1's
    `active_document_path` until contract-v3.0; the field moved, the confinement
    did not.)"""
    doc = copy.deepcopy(_example("workbench-chat-turn-v2-loaded-set.example.yaml"))
    doc["bound_buffer"] = "../outside/note.md"
    ctx = vidc.catalog_model_ids_from(_example(
        "workbench-model-catalog-local.example.yaml"))
    f = _validate(vidc, registry_docs, "escaping-binding", doc, ctx)
    assert any("path" in e or "bound" in e for e in f.errors), f.errors


def test_a_new_artifact_buffer_may_carry_a_null_path(vidc, registry_docs):
    """PR #45 Copilot blocker 4: a not-yet-created artifact has no path yet
    (the null-path -> create lifecycle, data-model §4); the buffer's path is
    nullable while every other identity field stays required."""
    doc = copy.deepcopy(_example("workbench-chat-turn-v2-loaded-set.example.yaml"))
    assert doc["buffers"][-1]["path"] is None
    ctx = vidc.catalog_model_ids_from(_example(
        "workbench-model-catalog-local.example.yaml"))
    f = _validate(vidc, registry_docs, "null-path", doc, ctx)
    assert not f.errors, f.errors


# ---- CODEX-3 (Codex review of PR #210): the validator refuses what the route
# refuses, per lane -------------------------------------------------------------
#
# TWO OF THE THREE TESTS HERE WERE THE V1 LANE'S and are deleted at
# contract-v3.0 (retire-doxbench-chat-turn-v1):
# `test_a_v1_document_at_the_outline_path_is_refused` and
# `test_a_v1_document_at_the_document_path_is_still_accepted`. Together they
# pinned that the validator's per-lane rule tracked the ROUTE's per-lane rule,
# which is the only way conformance means anything — and the asymmetry they
# recorded (the `outline` spelling refused, the `document` spelling accepted,
# CODEX-1) was a fact about the v1 envelope's single document. There is one lane
# now, so there is no per-lane pairing left to assert; what the surviving lane
# refuses is asserted below, and the validator's reserved SETS are still checked
# against the runtime's at the bottom of this file.

def test_a_v2_document_at_a_reserved_path_is_refused(vidc, registry_docs):
    """The certification gap Codex found: a widened instance whose document sits
    at path `document` validated CLEAN while the route always refuses it.

    The fixture shape matters — the outline plus exactly ONE document, so nothing
    else claims that key. A fixture carrying the unbacked slot too would fail on
    the duplicate-key rule and never reach this one, which is how the gap
    survived."""
    doc = _example("workbench-chat-turn-v2-loaded-set.example.yaml")
    doc = copy.deepcopy(doc)
    doc["buffers"] = [doc["buffers"][0], doc["buffers"][1]]
    doc["buffers"][1]["path"] = "document"
    doc["bound_buffer"] = "document"
    f = _validate(vidc, registry_docs, "v2-reserved-document", doc)
    assert any("reserved" in e for e in f.errors), f.errors


def test_the_validators_reserved_sets_agree_with_the_runtimes(vidc):
    """The validator RESTATES these sets rather than importing them, because it
    is published by exact commit and run against arbitrary target repositories —
    so the pairing has to be asserted somewhere, and this is that somewhere."""
    import sys
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from ideation_dashboard import doxbench_turns as turns
    assert set(vidc.V2_RESERVED_DOCUMENT_PATHS) == set(turns.RESERVED_BUFFER_KEYS)
    assert set(vidc.V1_RESERVED_DOCUMENT_PATHS) == set(turns.V1_RESERVED_BUFFER_KEYS)
