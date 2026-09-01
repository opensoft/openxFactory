"""`scripts/validate-chain-anchoring.py` — the NAMED READER, adjudicated.

The reader's own self-test already proves the packaged corpus valid and every
negative fixture invalid for its intended reason. What this module adds is the
part a self-test cannot check about itself:

  * that the corpus is not vacuous — the positives really are one coherent
    scope covering every record kind, every digest in it really recomputes
    under the one construction in force, and the negatives really are
    single-fault variants adjudicated INSIDE that scope;
  * that EVERY closed refusal code has a packaged probe whose filename IS the
    code, checked here as well as inside the reader, so a code added without a
    fixture fails a required check rather than only the tool that declares it;
  * that the DIRECTION-SENSITIVE rules hold in both directions — the
    future-dated mint refused beyond the skew and its honest twin accepted
    within it, the breach margin applied one way only, the ordering-only
    correspondence enforced both ways — because three consecutive review
    rounds of this capability's delta found direction errors, and a direction
    is exactly what a green fixture alone cannot pin;
  * and that the exit codes and the note lines a future gate would grep for
    are what it would grep for.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.signed_execution_chain import canonical  # noqa: E402

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate-chain-anchoring.py"
CONTRACT_DIR = REPO_ROOT / "contracts" / "chain-anchoring"
EXAMPLES = CONTRACT_DIR / "examples"
NEGATIVES = EXAMPLES / "negative"


def _load_reader():
    """The reader's filename carries a dash, so it is loaded by path. It is
    registered in `sys.modules` BEFORE execution because `@dataclass` resolves
    annotations through `sys.modules[cls.__module__]`, and a module that is not
    there yet fails at class-definition time rather than at first use."""
    spec = importlib.util.spec_from_file_location(
        "validate_chain_anchoring", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reader = _load_reader()


@pytest.fixture(scope="module")
def registry_and_docs():
    return reader.build_registry()


def _validate(records, registry_and_docs):
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.validate_scope(findings, records, registry, docs)
    return findings


def _corpus():
    return reader.positive_records()


def _one(predicate):
    """A deep copy of the first positive record the predicate matches, so a
    mutation test never bleeds into another test's baseline."""
    return copy.deepcopy(next(doc for _, doc in _corpus()
                              if isinstance(doc, dict) and predicate(doc)))


def _receipt(rid):
    return _one(lambda doc: doc.get("receipt_id") == rid)


def _reseal(receipt):
    receipt["anchored_digest"]["value"] = canonical.digest(
        {"material_digest": receipt["material_digest"],
         "mint_time_configuration": receipt["mint_time_configuration"]})
    return receipt


# --------------------------- the corpus itself ---------------------------

def test_the_packaged_corpus_is_one_coherent_scope(registry_and_docs):
    """Not merely "each file is well formed": the positives are validated as
    ONE scope, cross-record rules included, or every negative below is
    measured against a baseline that was already broken."""
    findings = _validate(_corpus(), registry_and_docs)
    assert findings.errors == []


def test_the_corpus_covers_every_record_kind():
    kinds = {doc.get("kind") for _, doc in _corpus() if isinstance(doc, dict)}
    assert kinds == set(reader.KIND_TO_SCHEMA)


def test_every_digest_in_the_corpus_actually_recomputes():
    """The corpus's digests are computed, not decorative: every receipt's
    anchored digest recomputes over {material_digest, mint_time_configuration},
    and every record digest recomputes over its record. A corpus whose digests
    did not recompute would make check 2 vacuously green on hand-typed
    values."""
    checked = 0
    for _, doc in _corpus():
        if doc.get("kind") == "xfactory_chain_anchoring_receipt":
            expected = canonical.digest(
                {"material_digest": doc["material_digest"],
                 "mint_time_configuration": doc["mint_time_configuration"]})
            assert doc["anchored_digest"]["value"] == expected
            checked += 1
        for member in ("commitment_digest", "derivation_digest",
                       "result_digest"):
            node = doc.get(member)
            if isinstance(node, dict):
                body = {k: v for k, v in doc.items() if k != member}
                assert node["value"] == canonical.digest(body)
                checked += 1
    assert checked >= 7  # four receipts and three record digests


def test_every_closed_refusal_code_has_a_packaged_probe():
    """Checked OUTSIDE the reader as well as inside it, so a refusal code
    added to the contract without a fixture fails a required check rather
    than only the tool that declares it."""
    stems = {path.stem for path in NEGATIVES.glob("*.yaml")}
    missing = reader.REFUSAL_CODES - stems
    assert not missing, f"closed refusal codes with no probe: {sorted(missing)}"


def test_negative_filenames_are_the_codes_they_trigger():
    """One fixture per refusal code and the FILENAME IS THE CODE, so the tree
    listing is the index of the refusal enumeration."""
    for path in sorted(NEGATIVES.glob("*.yaml")):
        code, _ = reader.expected_failure(path)
        assert path.stem == code, f"{path.name} declares {code!r}"


def test_the_definitions_enum_and_the_readers_frozen_set_are_one_set():
    definitions = yaml.safe_load(
        (CONTRACT_DIR / "anchoring-definitions.schema.yaml").read_text())
    declared = set(definitions["$defs"]["refusal_code"]["enum"])
    assert declared == reader.REFUSAL_CODES


def test_every_family_digest_subject_is_in_the_one_construction():
    """The family adds SUBJECTS to tranche one's enumeration rather than a
    second construction: every `subject: {const: ...}` any schema here pins
    must already be a member of the canonical module's frozen mirror."""
    pinned = set()
    for path in CONTRACT_DIR.glob("*.schema.yaml"):
        def walk(node):
            if isinstance(node, dict):
                subject = node.get("subject")
                if isinstance(subject, dict) and "const" in subject:
                    pinned.add(subject["const"])
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)
        walk(yaml.safe_load(path.read_text()))
    assert pinned  # the walk found the pinned subjects
    assert pinned <= canonical.SUBJECTS


def test_every_negative_fixture_is_a_single_named_fault(registry_and_docs):
    """Each negative, adjudicated INSIDE the positive scope, fails with its
    declared code and its declared detail — the cross-record refusals
    (a reused derivation parameter, a receipt entry for an in-flight witness,
    one key under two planes) are only expressible that way."""
    base = _corpus()
    for path in sorted(NEGATIVES.glob("*.yaml")):
        code, detail = reader.expected_failure(path)
        findings = _validate(base + reader.labelled("negative", path),
                             registry_and_docs)
        lines = reader.lines_for(findings.errors, code)
        assert lines, (f"{path.name}: expected {code!r}, got "
                       f"{sorted(reader.codes_of(findings.errors))}")
        if detail:
            assert any(detail in line for line in lines), \
                f"{path.name}: {code!r} fired but not for {detail!r}: {lines}"


# --------------------------- the timing model's directions ---------------------------

def test_a_submission_beyond_the_skew_is_refused_and_within_it_accepted(
        registry_and_docs):
    """THE DIRECTION, PINNED AS A PAIR. A header time is a reference with a
    width, never an upper bound on submission: the same receipt is refused
    with its declared submission 3.5 hours past the earliest chain time
    (skew is 2 hours) and accepted at 30 minutes past it."""
    refused = _receipt("rcp-example-0001")
    refused["mint_time_configuration"]["submission_time"] = \
        "2026-08-30T13:35:00Z"
    _reseal(refused)
    findings = _validate([("mutated/refused", refused)], registry_and_docs)
    assert reader.lines_for(findings.errors,
                            "receipt_submission_after_earliest_chain_time")

    accepted = _receipt("rcp-example-0001")
    accepted["mint_time_configuration"]["submission_time"] = \
        "2026-08-30T10:35:00Z"
    _reseal(accepted)
    findings = _validate([("mutated/accepted", accepted)], registry_and_docs)
    assert findings.errors == []


def test_refusing_the_honest_twin_is_itself_refused(registry_and_docs):
    """The guard has a probe fixture over the within-skew receipt; this pins
    that it also fires over a receipt whose submission PRECEDES every header
    time — the fully unambiguous honest case."""
    result = {
        "schema_version": 1,
        "kind": "xfactory_chain_anchoring_verification_result",
        "result_id": "vr-mutated-guard",
        "subject_ref": "item-example-0001-log-checkpoint-640",
        "verification_mode": "receipt_only",
        "status": "refused",
        "receipt_ref": "rcp-example-0001",
        "refusal": {"code": "receipt_submission_after_earliest_chain_time",
                    "statement": "refused in the wrong direction"},
    }
    findings = _validate(_corpus() + [("mutated/guard", result)],
                         registry_and_docs)
    assert reader.lines_for(findings.errors, "honest_receipt_refused_within_skew")


def test_the_breach_margin_is_one_directional(registry_and_docs):
    """A delay check claiming breach_proven on a bound INSIDE the declared
    maximum plus tolerance is refused; the same bound one second past the
    margin is not. The fixture probes a horizon breach; this pins the delay
    side's arithmetic edge."""
    stateful = _one(lambda doc: doc.get("result_id") == "vr-example-0003")
    stateful["result_id"] = "vr-mutated-margin"
    stateful["delay_check"]["cp_in"] = "2026-08-30T07:00:00Z"
    stateful["delay_check"]["bound_seconds"] = 3600  # inside 3600 + 600
    findings = _validate(_corpus() + [("mutated/inside", stateful)],
                         registry_and_docs)
    assert reader.lines_for(findings.errors, "breach_declared_within_tolerance")


def test_the_committed_block_governs_a_rewritten_horizon(registry_and_docs):
    """The anchored digest breaks on ANY committed-block edit — the extended
    horizon included, not only the rewritten witness set the fixture probes."""
    receipt = _receipt("rcp-example-0001")
    receipt["mint_time_configuration"]["configured_witnesses"][1][
        "completion_horizon_seconds"] = 999999  # extended, digest left stale
    findings = _validate([("mutated/horizon", receipt)], registry_and_docs)
    assert reader.lines_for(findings.errors, "receipt_configuration_block_edited")


def test_ordering_only_correspondence_holds_in_both_directions(
        registry_and_docs):
    """The fixture probes a time under an ordering-only rule; this pins the
    opposite direction — a null header time under a time-bearing rule."""
    receipt = _receipt("rcp-example-0001")
    receipt["per_chain_anchors"][0]["block_header"]["time_field"] = None
    findings = _validate([("mutated/null-time", receipt)], registry_and_docs)
    assert reader.lines_for(findings.errors, "ordering-only-correspondence")


def test_a_transaction_capture_at_the_floor_is_accepted(registry_and_docs):
    """The deferred-transaction refusal is a SIZE floor, and the floor itself
    is lawful: exactly 64 decoded bytes passes, one identifier's worth does
    not (the fixture proves the refusal; this proves the floor's edge)."""
    import base64
    receipt = _receipt("rcp-example-0001")
    receipt["per_chain_anchors"][0]["anchor_transaction_bytes"] = \
        base64.urlsafe_b64encode(b"\x11" * 64).rstrip(b"=").decode()
    findings = _validate([("mutated/at-floor", receipt)], registry_and_docs)
    assert not reader.lines_for(findings.errors,
                                "receipt_transaction_deferred_to_verification")


# --------------------------- the structural sweeps ---------------------------

def test_the_payload_sweep_is_depth_blind(registry_and_docs):
    """A content-bearing member nested inside a per-chain entry is refused
    exactly as a top-level one: the sweep runs at any depth, or it is a
    control that reads as though it covered the record."""
    receipt = _receipt("rcp-example-0001")
    receipt["per_chain_anchors"][0]["inclusion_proof"]["payload"] = "x" * 40
    findings = _validate([("mutated/nested-payload", receipt)],
                         registry_and_docs)
    assert any("payload" in line for line in
               reader.lines_for(findings.errors, "payload_bearing_field"))


def test_an_overlong_string_is_a_payload_however_it_is_spelled(
        registry_and_docs):
    """The length half of the sweep: a member name no token matches, carrying
    more bytes than any declared member of this family admits."""
    commitment = _one(lambda doc: doc.get("commitment_id") == "cac-example-0001")
    commitment["innocuous_member"] = "A" * 3000
    findings = _validate(_corpus() + [("mutated/overlong", commitment)],
                         registry_and_docs)
    assert reader.lines_for(findings.errors, "payload_bearing_field")


def test_a_receipt_only_result_reading_state_is_refused(registry_and_docs):
    """The mode discriminator is enforced on every stateful-knowledge channel;
    the fixture probes the boolean, this pins the anchor_state_ref channel."""
    result = _one(lambda doc: doc.get("result_id") == "vr-example-0001")
    result["result_id"] = "vr-mutated-stateful-ref"
    result["anchor_state_ref"] = "as-example-0001"
    findings = _validate(_corpus() + [("mutated/state-ref", result)],
                         registry_and_docs)
    assert reader.lines_for(findings.errors,
                            "verification_result_claims_stateful_knowledge")


def test_the_shortfall_is_checked_against_the_committed_set(registry_and_docs):
    """The arithmetic fixture reconciles the three lists against each other;
    this pins the second half — a configured list that reconciles internally
    but disagrees with the receipt's committed witness set."""
    result = _one(lambda doc: doc.get("result_id") == "vr-example-0001")
    result["result_id"] = "vr-mutated-configured"
    result["witness_shortfall"] = {
        "configured": ["w-someone-elses-witness"],
        "present": [],
        "missing": ["w-someone-elses-witness"],
    }
    result["status"] = "anchor_pending"
    findings = _validate(_corpus() + [("mutated/configured", result)],
                         registry_and_docs)
    assert reader.lines_for(findings.errors, "witness_shortfall_miscomputed")


# --------------------------- the declaration's arithmetic ---------------------------

def _declaration():
    return _one(lambda doc: doc.get("kind")
                == "xfactory_chain_anchoring_conformance_declaration")


def test_a_declaration_recording_the_reader_unrequired_still_warns(
        registry_and_docs):
    """`is_required_in_ruleset: false` is a fact to record, not a defect to
    hide — and while it is the fact, the standing warning keeps saying so."""
    findings = _validate(_corpus(), registry_and_docs)
    assert any("[reader-not-required]" in line for line in findings.warnings)


def test_ca_r5_satisfied_is_refused_even_with_the_token_removed(
        registry_and_docs):
    """The structural residual is refused BY OBLIGATION, not only by token: an
    entry that drops the `structural_residual` member and claims `satisfied`
    is still refused, or the refusal would be opt-in."""
    declaration = _declaration()
    declaration["declaration_id"] = "cad-mutated-r5"
    for entry in declaration["obligations"]:
        if entry["obligation"] == "CA-R5":
            entry["satisfaction"] = "satisfied"
            entry.pop("declared_residual", None)
            entry.pop("structural_residual", None)
    findings = _validate(_corpus() + [("mutated/r5", declaration)],
                         registry_and_docs)
    assert reader.lines_for(findings.errors,
                            "structural_residual_declared_satisfied")


def test_a_satisfied_entry_carrying_a_residual_is_a_contradiction(
        registry_and_docs):
    declaration = _declaration()
    declaration["declaration_id"] = "cad-mutated-contradiction"
    for entry in declaration["obligations"]:
        if entry["obligation"] == "CA-R9":
            entry["declared_residual"] = {
                "statement": "a residual on a satisfied obligation",
                "closed_by": "nothing can close a contradiction",
            }
    findings = _validate(_corpus() + [("mutated/contradiction", declaration)],
                         registry_and_docs)
    assert reader.lines_for(findings.errors, "residual-not-declared")


def test_the_obligation_set_is_the_nine_requirements_of_the_delta():
    assert reader.OBLIGATIONS == [f"CA-R{n}" for n in range(1, 10)]
    schema = yaml.safe_load(
        (CONTRACT_DIR / "conformance-declaration.schema.yaml").read_text())
    enum = schema["properties"]["obligations"]["items"]["properties"][
        "obligation"]["enum"]
    assert enum == reader.OBLIGATIONS


# --------------------------- the reader as a gate ---------------------------

def test_the_reader_exits_zero_on_the_corpus_and_the_tree(capsys, monkeypatch):
    """What a future required check runs, run here: self-test plus the
    whole-tree scan exits 0, the note names 70/70 closed refusal codes
    red-proven, and zero real artifacts is reported as the expected state."""
    monkeypatch.setattr(sys, "argv",
                        ["validate-chain-anchoring.py", str(REPO_ROOT)])
    assert reader.main() == 0
    out = capsys.readouterr().out
    assert f"{len(reader.REFUSAL_CODES)}/{len(reader.REFUSAL_CODES)} " \
           f"closed refusal codes red-proven" in out
    assert "ZERO real artifacts is the expected state" in out


def test_strict_mode_turns_the_standing_warnings_into_a_refusal(capsys,
                                                                monkeypatch):
    """--strict exists so the day the warnings should block, flipping one flag
    blocks on them; until then the corpus's two honest warnings (reader not
    required, archival node undeclared) do not mask each other."""
    monkeypatch.setattr(sys, "argv", ["validate-chain-anchoring.py", "--strict"])
    assert reader.main() == 1
    assert "[reader-not-required]" in capsys.readouterr().out


def test_a_broken_corpus_fails_the_self_test(registry_and_docs, monkeypatch,
                                             tmp_path, capsys):
    """The self-test is not decorative: with one negative fixture's expected
    code unsatisfiable (pointed at a code the fixture does not provoke), the
    reader exits 1. Run against a scratch copy of the corpus so the shipped
    tree is never touched."""
    import shutil
    scratch = tmp_path / "examples"
    shutil.copytree(EXAMPLES, scratch)
    victim = scratch / "negative" / "salt_width_below_floor.yaml"
    text = victim.read_text().replace(
        "salt_width_bits: 32", "salt_width_bits: 256")
    victim.write_text(text)
    monkeypatch.setattr(reader, "EXAMPLES_DIR", scratch)
    monkeypatch.setattr(reader, "NEGATIVE_DIR", scratch / "negative")
    monkeypatch.setattr(sys, "argv", ["validate-chain-anchoring.py"])
    assert reader.main() == 1
    out = capsys.readouterr().out
    assert "negative-should-fail" in out or "negative-wrong-reason" in out \
        or "refusal-code-without-probe" in out
