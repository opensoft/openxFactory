"""`scripts/validate-signed-execution-chain.py` — the NAMED READER, adjudicated.

The reader's own self-test already proves the packaged corpus valid and every
negative fixture invalid for its intended reason. What this module adds is the
part a self-test cannot check about itself:

  * that the corpus is not vacuous — the positives really are a whole chain, and
    the negatives really are single-fault variants of it;
  * that EVERY closed refusal code has a packaged probe, checked here as well as
    inside the reader, so a code added without a fixture fails a REQUIRED check
    rather than only the tool that declares it;
  * that the carried-vocabulary path REFUSES a carried block the shipped shape
    would reject, which is the check the gate's
    `--require-pinned-wallet-vocabulary` flag exists to keep from degrading; and
  * that the exit codes and the notes the gate greps for are what the gate greps
    for.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate-signed-execution-chain.py"
EXAMPLES = REPO_ROOT / "contracts" / "signed-execution-chain" / "examples"
NEGATIVES = EXAMPLES / "negative"


def _load_reader():
    """The reader's filename carries a dash, so it is loaded by path. It is
    registered in `sys.modules` BEFORE execution because `@dataclass` resolves
    annotations through `sys.modules[cls.__module__]`, and a module that is not
    there yet fails at class-definition time rather than at first use."""
    spec = importlib.util.spec_from_file_location(
        "validate_signed_execution_chain", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reader = _load_reader()


@pytest.fixture(scope="module")
def registry_and_docs():
    return reader.build_registry()


@pytest.fixture(scope="module")
def carried():
    findings = reader.Findings()
    return reader.load_carried_schemas(findings, required=False)


def _validate(records, registry_and_docs, carried):
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.validate_scope(findings, records, registry, docs, carried)
    return findings


def test_the_packaged_corpus_is_one_whole_chain(registry_and_docs, carried):
    """Not merely "each file is well formed": the positives must compose into a
    chain that passes all EIGHT checks, or every negative below is measured
    against a baseline that was already broken."""
    findings = _validate(reader.positive_records(), registry_and_docs, carried)
    assert findings.errors == []


def test_the_corpus_covers_all_four_kinds_and_every_leaf_type(registry_and_docs,
                                                              carried):
    records = reader.positive_records()
    kinds = {doc["kind"] for _, doc in records}
    assert kinds == set(reader.KIND_TO_SCHEMA)
    leaf_types = {doc["leaf_type"] for _, doc in records
                  if doc["kind"] == "xfactory_signed_execution_chain_log_leaf"}
    assert leaf_types == set(reader.LEAF_TYPES), (
        "every act this capability governs writes a leaf, so every leaf type has "
        "a packaged example or one of them is a shape nobody has ever produced")


def test_every_closed_refusal_code_has_a_packaged_probe():
    """The reader enforces this too. It is repeated here because THIS module runs
    inside the required `pytest-suite` job: a refusal code added without a
    fixture must fail a required check, not only the tool that declares it."""
    probed = {reader.expected_failure(path)[0]
              for path in sorted(NEGATIVES.glob("*.yaml"))}
    assert reader.REFUSAL_CODES <= probed, sorted(reader.REFUSAL_CODES - probed)


def test_the_leaf_schema_enumerates_exactly_the_readers_refusal_codes():
    """One enumeration, two places it has to be true: the shape a verdict records
    and the set the reader can emit. A code in one and not the other is a refusal
    that cannot be written down, or a record that can claim a refusal nothing
    produces."""
    schema = yaml.safe_load(
        (REPO_ROOT / "contracts" / "signed-execution-chain" /
         "transparency-log-leaf.schema.yaml").read_text(encoding="utf-8"))
    declared = schema["properties"]["verdict"]["properties"]["refusal"][
        "properties"]["code"]["enum"]
    assert set(declared) == set(reader.REFUSAL_CODES)
    assert len(declared) == len(set(declared))


def test_every_negative_fixture_is_a_single_named_fault(registry_and_docs, carried):
    """Each fixture must fail for the code it declares, and the base corpus is
    the scope it is measured in. A fixture that passes cleanly, or that fails
    only for some other reason, is a fixture testing nothing."""
    base = reader.positive_records()
    for path in sorted(NEGATIVES.glob("*.yaml")):
        code, detail = reader.expected_failure(path)
        findings = _validate(base + reader.labelled("negative", path),
                             registry_and_docs, carried)
        codes = reader.codes_of(findings.errors)
        assert findings.errors, f"{path.name}: validated cleanly"
        assert code in codes, f"{path.name}: expected {code!r}, got {sorted(codes)}"
        if detail:
            assert any(detail in line
                       for line in reader.lines_for(findings.errors, code)), \
                f"{path.name}: {code!r} fired but not for {detail!r}"


def test_a_traveling_contract_is_checkable_from_the_artifact_alone(
        registry_and_docs, carried):
    """Requirement 5's claim, executed: ONE traveling contract, no registry, no
    log, no other record in scope.

    Two things must both hold. Its INTERNAL consistency is established — the
    carried signature verifies against the wallet the artifact itself carries,
    and the carried chain identity recomputes from the carried signed
    ratification — so neither `ratification_signature_invalid` nor
    `digest_construction_mismatch` fires. And that establishes consistency ONLY:
    the questions that need the store still REFUSE, because an unresolvable
    external lookup never converts into permission."""
    alone = [(label, doc) for label, doc in reader.positive_records()
             if doc["kind"] == "xfactory_signed_execution_chain_traveling_contract"]
    assert len(alone) == 1
    codes = reader.codes_of(_validate(alone, registry_and_docs, carried).errors)
    assert "ratification_signature_invalid" not in codes
    assert "digest_construction_mismatch" not in codes
    assert "orphan_chain_identity" in codes, (
        "with no inception in reach the chain resolves to no signed ratification, "
        "and the reader refuses rather than reading self-consistency as permission")


def test_a_traveling_contract_carrying_a_bad_signature_is_refused_on_its_own(
        registry_and_docs, carried):
    """The point-of-use check is not the inception check reached by another
    route. A traveling contract whose CARRIED signature is over other bytes must
    be refused when it is the only artifact in reach — otherwise the reader would
    be establishing the signature through a record a point-of-use checker does
    not have."""
    import copy

    alone = [(label, copy.deepcopy(doc)) for label, doc in reader.positive_records()
             if doc["kind"] == "xfactory_signed_execution_chain_traveling_contract"]
    signature = alone[0][1]["ratification_signature"]["signature"]
    mutated = ("B" if signature[0] != "B" else "C") + signature[1:]
    alone[0][1]["ratification_signature"]["signature"] = mutated
    codes = reader.codes_of(_validate(alone, registry_and_docs, carried).errors)
    assert "ratification_signature_invalid" in codes


def test_a_carried_block_the_shipped_shape_rejects_is_refused(registry_and_docs,
                                                              carried):
    """THE CARRIED RECORD IS THE SHIPPED RECORD, and this is the check that makes
    that more than a claim.

    The mutation adds a member the shipped exercise schema does not admit — it
    closes `additionalProperties` — so a reader holding carried blocks to the
    PINNED shape refuses it and a reader checking only the members this
    capability restricts does not. The assertion is conditional on the pinned
    vocabulary being reachable rather than skipped: in the required `pytest-suite`
    job the `openXwallet` gitlink is initialized, so the first branch is the one
    that runs in CI, and the second branch asserts the honest fallback a
    developer checkout gets."""
    import copy

    records = copy.deepcopy(reader.positive_records())
    for _, doc in records:
        if doc["kind"] == "xfactory_signed_execution_chain_inception":
            doc["signed_ratification"]["presentation"]["exercise"][
                "smuggled_member"] = "not a member of the shipped record"
    findings = _validate(records, registry_and_docs, carried)
    if "exercise" in carried:
        assert "carried-vocabulary" in reader.codes_of(findings.errors)
    else:
        assert findings.errors == [], (
            "with no pinned vocabulary reachable the reader falls back to the "
            "members this capability restricts, and says so in a note")


def test_requiring_an_unreachable_pinned_vocabulary_is_a_refusal(monkeypatch):
    """The gate passes `--require-pinned-wallet-vocabulary` precisely so a run
    that cannot reach the pin REFUSES instead of validating less than it claims.
    A check that silently checks less is the vacuous pass this repository has
    already had to close once, for the wallet intake register."""
    monkeypatch.setattr(reader, "PINNED_WALLET_DIR",
                        REPO_ROOT / "no" / "such" / "directory")
    strict = reader.Findings()
    reader.load_carried_schemas(strict, required=True)
    assert "pinned-wallet-vocabulary-unavailable" in reader.codes_of(strict.errors)

    lenient = reader.Findings()
    reader.load_carried_schemas(lenient, required=False)
    assert lenient.errors == []
    assert any("openXwallet" in line for line in lenient.notes)


def test_the_reader_exits_zero_on_the_corpus_and_the_tree(capsys):
    """The two invocations the gate makes, and the notes the gate greps for. A
    note the gate reads and the reader stopped emitting is a green check that
    proves nothing."""
    assert reader.main.__module__ == "validate_signed_execution_chain"
    argv = sys.argv
    try:
        sys.argv = ["validate-signed-execution-chain.py", str(REPO_ROOT),
                    "--require-pinned-wallet-vocabulary"] \
            if (REPO_ROOT / "openXwallet" / "contracts" / "openxwallet").is_dir() \
            else ["validate-signed-execution-chain.py", str(REPO_ROOT)]
        assert reader.main() == 0
    finally:
        sys.argv = argv
    out = capsys.readouterr().out
    assert "self-test:" in out
    assert "closed refusal codes red-proven" in out
    assert "repo scan (" in out and "artifact(s) checked" in out


def test_the_reader_says_the_capability_confers_nothing_yet(registry_and_docs,
                                                            carried):
    """Requirement 9 is about this capability's own standing, and the reader
    states it where it runs rather than only in the declaration. When the gate
    becomes a required check the packaged declaration flips to
    `is_required_in_ruleset: true` and this warning goes away — which is the
    point at which the records begin to confer anything at all."""
    findings = _validate(reader.positive_records(), registry_and_docs, carried)
    assert any("reader-not-required" in line for line in findings.warnings)


def test_a_declaration_recording_sec_r9_satisfied_while_unrequired_is_refused(
        registry_and_docs, carried):
    """The pairing above is not decoration: a declaration may record the reader as
    unrequired, and it may NOT then record the obligation as satisfied. Where no
    such check exists the requirement is UNMET, not partially met."""
    import copy

    records = copy.deepcopy(reader.positive_records())
    for _, doc in records:
        if doc["kind"] == \
                "xfactory_signed_execution_chain_conformance_declaration":
            for entry in doc["obligations"]:
                if entry["obligation"] == "SEC-R9":
                    entry["satisfaction"] = "satisfied"
                    entry.pop("declared_residual", None)
    findings = _validate(records, registry_and_docs, carried)
    assert any("SEC-R9" in line for line in
               reader.lines_for(findings.errors, "residual_not_declared"))


def test_the_declaration_is_closed_over_the_nine_obligations_in_both_directions(
        registry_and_docs, carried):
    """An obligation with no entry is refused, and so is an entry naming an
    obligation this capability does not have. A declaration that can quietly omit
    one is how a silent gap gets recorded as conformance."""
    import copy

    records = copy.deepcopy(reader.positive_records())
    for _, doc in records:
        if doc["kind"] == \
                "xfactory_signed_execution_chain_conformance_declaration":
            for entry in doc["obligations"]:
                if entry["obligation"] == "SEC-R5":
                    entry["obligation"] = "SEC-R2"
    findings = _validate(records, registry_and_docs, carried)
    lines = reader.lines_for(findings.errors, "residual_not_declared")
    assert any("SEC-R5 is declared 0 times" in line for line in lines)
    assert any("SEC-R2 is declared 2 times" in line for line in lines)


def test_the_obligation_set_is_the_nine_requirements_of_the_delta():
    """Nine ADDED requirements, nine obligations. The delta is the authority for
    the count, and the ratification record states it: NINE ADDED requirements
    over 45 scenarios."""
    schema = yaml.safe_load(
        (REPO_ROOT / "contracts" / "signed-execution-chain" /
         "conformance-declaration.schema.yaml").read_text(encoding="utf-8"))
    declared = schema["properties"]["obligations"]["items"]["properties"][
        "obligation"]["enum"]
    assert declared == reader.OBLIGATIONS
    assert len(declared) == 9
    assert schema["properties"]["obligations"]["minItems"] == 9
    assert schema["properties"]["obligations"]["maxItems"] == 9
