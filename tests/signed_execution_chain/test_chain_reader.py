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
import re
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
    """Coverage is the UNION of the packaged corpora: tranche one's reference
    chain carries the four original kinds and the ratification leaf types, and
    the tranche-two corpus carries the seven kinds and seven leaf types
    add-chain-attestation added. Neither corpus alone covers the enumeration,
    and neither is asked to."""
    records = [record
               for prefix, positives_dir, _ in reader.CORPORA
               for record in reader.positive_records(positives_dir, prefix)]
    kinds = {doc["kind"] for _, doc in records}
    # The tranche-two corpus also CARRIES the three consumed trust-anchor kinds
    # (anchor record, certificate record, issuance evidence) so a reader can
    # resolve every reference the bindings make; they are add-trust-anchor's
    # shapes, not this family's, and are the only kinds admitted beyond the
    # family's own enumeration.
    consumed = {"xfactory_trust_anchor", "xfactory_certificate_record",
                "xfactory_certificate_issuance_evidence"}
    assert kinds - consumed == set(reader.KIND_TO_SCHEMA)
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
              for _, _, negatives_dir in reader.CORPORA
              for path in sorted(negatives_dir.glob("*.yaml"))}
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


def test_a_key_id_two_wallets_claim_differently_is_ambiguous_not_last_seen(
        registry_and_docs, carried):
    """Codex's P1 on `aedfd8ce`, and the property is about ITERATION ORDER.

    The scope-wide key map was built with `dict.update`, so whichever carried
    wallet was read last silently won an identifier both claimed. This test
    presents the SAME two wallets in BOTH orders: an ambiguous identifier must be
    refused either way, because a verification result that depends on which
    record was read first is not a verification result.

    The `AMBIGUOUS_KEY` marker is what makes it order-independent — dropping the
    ambiguity would let a second wallet resolve an identifier the first had
    already made unanswerable."""
    reference = {"key_id": "key-shared-0001", "did": "did:key:zAAA"}
    other = {"key_id": "key-shared-0001", "did": "did:key:zBBB"}
    restated = {"key_id": "key-shared-0001", "did": "did:key:zAAA"}

    for first, second in ((reference, other), (other, reference)):
        merged: dict = {}
        reader.merge_declared_keys(merged, {"key_reference": first})
        reader.merge_declared_keys(merged, {"key_reference": second})
        assert merged["key-shared-0001"] is reader.AMBIGUOUS_KEY

    # A restatement of the SAME public half is not an ambiguity: the rejection
    # must not reject a wallet that declares one key twice identically.
    merged = {}
    reader.merge_declared_keys(merged, {"key_reference": reference,
                                        "keys": [restated]})
    assert merged["key-shared-0001"] is not reader.AMBIGUOUS_KEY

    # And an ambiguity INSIDE one wallet survives a second wallet's declaration.
    merged = {}
    reader.merge_declared_keys(merged, {"key_reference": reference,
                                        "keys": [other]})
    reader.merge_declared_keys(merged, {"key_reference": restated})
    assert merged["key-shared-0001"] is reader.AMBIGUOUS_KEY


def test_the_presentation_reference_must_name_the_record_it_carries(
        registry_and_docs, carried):
    """Codex's sharpest P1 on `aedfd8ce`: the per-act uniqueness rule keyed on
    `presentation.exercise_ref`, which is replaceable WITHOUT touching the
    exercise it names.

    Carrying the already-consumed exercise verbatim and changing only that outer
    reference produced different signed bytes, a different chain identity, and a
    uniqueness key the map had never seen — so the consumed exercise was
    replayable past the rule written to prevent it.

    BOTH halves of the repair are asserted, because either alone leaves a hole:
    the reference must AGREE with the carried record, and uniqueness must be keyed
    on the CARRIED identifier so it does not depend on that agreement check having
    run."""
    import copy

    records = copy.deepcopy(reader.positive_records())
    for _, doc in records:
        if doc["kind"] == "xfactory_signed_execution_chain_inception":
            doc["signed_ratification"]["presentation"]["exercise_ref"] = \
                "exr-a-fresh-label"
    codes = reader.codes_of(_validate(records, registry_and_docs, carried).errors)
    assert "continuity_broken" in codes

    # The uniqueness key itself: two inceptions carrying ONE exercise record,
    # under two different outer labels, are one act presented twice.
    doubled = copy.deepcopy(reader.positive_records())
    clone = None
    for _, doc in doubled:
        if doc["kind"] == "xfactory_signed_execution_chain_inception":
            clone = copy.deepcopy(doc)
    clone["inception_id"] = "inc-replayed"
    clone["chain_identity"]["value"] = "sha256:" + "cd" * 32
    clone["signed_ratification"]["presentation"]["exercise_ref"] = "exr-other-label"
    codes = reader.codes_of(
        _validate(doubled + [("replay", clone)], registry_and_docs,
                  carried).errors)
    assert "per_act_value_reused" in codes, (
        "uniqueness must key on the carried exercise identifier, which both "
        "inceptions share, and not on the outer label they differ in")


def test_every_reference_that_could_move_independently_is_compared(
        registry_and_docs, carried):
    """ROUND TWO'S SHAPE, SWEPT FOR RATHER THAN WAITED FOR.

    Both of round two's P1s were a REFERENCE and its REFERENT able to move
    independently — two facts that look like one fact. A capability whose whole
    subject is binding one record to another should expect that everywhere, so
    every remaining pair of the shape is compared, and this test pins that each
    comparison RUNS rather than merely existing.

    The custody pair is the load-bearing one. `add-trust-anchor`'s ratified rule
    is that declared custody BOUNDS WHAT A SIGNATURE EVIDENCES: a key readable by
    the host that uses it evidences that the HOST acted, which is exactly what a
    ratification may not stand on. An exercise free to record a stronger custody
    model than its wallet declares would let a `holder_readable` key evidence a
    human act, and requirement 8's narrowing rests on that being impossible."""
    import copy

    mutations = {
        "grant": ("presentation", "grant_ref", "grant-somebody-elses"),
        "attributed wallet": ("attribution", "wallet_ref", "wal-somebody-elses"),
        "attributed holder": ("attribution", "holder_ref", "person:somebody.else"),
        "custody model in force":
            ("exercise", "custody_model_in_force", "holder_readable"),
    }
    for what, (where, member, value) in mutations.items():
        records = copy.deepcopy(reader.positive_records())
        for _, doc in records:
            if doc["kind"] != "xfactory_signed_execution_chain_inception":
                continue
            presentation = doc["signed_ratification"]["presentation"]
            if where == "presentation":
                presentation["exercise"][member] = value
            elif where == "attribution":
                presentation["exercise"]["attribution"][member] = value
            else:
                presentation["exercise"][member] = value
        lines = reader.lines_for(
            _validate(records, registry_and_docs, carried).errors,
            "continuity_broken")
        assert any(what in line for line in lines), (what, lines)


def test_a_chain_whose_own_verdict_is_absent_from_the_log_is_refused(
        registry_and_docs, carried):
    """The FOURTH governed leaf type (Codex, P1 on `eb1241fc`), and the omission
    was fresh evidence of the same class one round after the missing-act fix: that
    fix required the ratification and traveling-contract leaves and still never
    required this one.

    Pinned here rather than by a packaged fixture for the same reason the
    deleted-genesis case is: a fixture is ADDED to the corpus and cannot take a
    leaf away.

    IT IS NOT A CHICKEN-AND-EGG, and the packaged corpus is the proof — a producer
    writes the verdict leaf it expects and this reader holds it to the reader's own
    walk, so requiring the leaf demands no trust in the producer and deadlocks no
    first landing. The second assertion is that half: the corpus's own
    producer-written verdict is accepted."""
    without = [(label, doc) for label, doc in reader.positive_records()
               if not (doc["kind"] == "xfactory_signed_execution_chain_log_leaf"
                       and doc.get("leaf_type") == "gate_verdict")]
    lines = reader.lines_for(
        _validate(without, registry_and_docs, carried).errors, "act_unproven")
    assert any("gate-verdict leaf" in line for line in lines), lines
    assert _validate(reader.positive_records(), registry_and_docs,
                     carried).errors == []


def test_a_signature_has_exactly_one_canonical_spelling(registry_and_docs,
                                                        carried):
    """Codex's P2 on `eb1241fc`. For 64 bytes the final base64url character carries
    two data bits and a decoder ignores the other four, so fifteen other spellings
    of one signature decode to the same bytes, verify identically, and match the
    schema's 86-character pattern.

    A record admitting sixteen textual forms of one signature admits sixteen
    distinct signed ratifications BY DIGEST — and the chain identity is a digest
    over those bytes."""
    import base64

    canonical_text = None
    for _, doc in reader.positive_records():
        if doc["kind"] == "xfactory_signed_execution_chain_inception":
            canonical_text = doc["ratification_signature"]["signature"]
    assert canonical_text is not None
    raw = base64.urlsafe_b64decode(canonical_text + "==")
    assert reader.decode_signature(canonical_text) == raw

    variants = 0
    for char in ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                 "0123456789-_"):
        candidate = canonical_text[:-1] + char
        if candidate == canonical_text:
            continue
        try:
            same = base64.urlsafe_b64decode(candidate + "==") == raw
        except Exception:  # noqa: BLE001
            continue
        if same:
            variants += 1
            assert reader.decode_signature(candidate) is None, candidate
    assert variants >= 1, (
        "the test proves nothing unless a non-canonical spelling of these exact "
        "bytes actually exists")


def test_a_log_whose_genesis_prefix_was_deleted_is_refused(registry_and_docs,
                                                           carried):
    """LEAVES ARE APPENDED AND NEVER REMOVED, and a check that cannot see a
    removal is not checking it.

    Found by Codex as a P1 on `0d0f277d`. The first reader walked consecutive
    PAIRS: the lowest retained leaf had no predecessor in scope, so its carried
    digest went unchecked, and a store that deleted a prefix presented a set in
    which every surviving pair linked correctly and every `tree_size` still
    agreed with its own index. THIS CASE CANNOT BE PROBED BY A PACKAGED FIXTURE —
    a fixture is ADDED to the corpus and cannot take leaf 0 away — so it is
    pinned here, where the scope is built rather than composed."""
    records = [(label, doc) for label, doc in reader.positive_records()
               if doc["kind"] != "xfactory_signed_execution_chain_log_leaf"
               or doc["leaf_index"] != 0]
    leaves = [doc for _, doc in records
              if doc["kind"] == "xfactory_signed_execution_chain_log_leaf"]
    assert [doc["leaf_index"] for doc in leaves] == [1, 2, 3], (
        "the fixture is leaves 1-3 with the genesis leaf deleted")
    lines = reader.lines_for(
        _validate(records, registry_and_docs, carried).errors,
        "leaf_hash_link_broken")
    assert any("begins at leaf 1" in line and "genesis" in line for line in lines), \
        lines
    assert any("compared against nothing" in line for line in lines), (
        "the surviving lowest leaf's carried predecessor digest must be reported "
        "as unverifiable rather than silently skipped — an unverifiable link is "
        "not a verified one")


def test_the_eight_check_list_is_closed_by_shape(registry_and_docs, carried):
    """Copilot's finding on `0d0f277d`, and the repair is the SHAPE rather than
    the reader.

    `uniqueItems` compares whole ITEMS, so two entries naming the same check with
    different outcomes were distinct objects and both validated: a verdict could
    record one check twice, omit another, carry eight items and be schema-valid
    beside prose calling the list closed and ordered. Each position now carries
    its own `const`, so a duplicate, an omission AND a reordering are all
    unrepresentable — which a reader-side rule would not have achieved."""
    import copy

    for mutate in ("duplicate", "reorder"):
        records = copy.deepcopy(reader.positive_records())
        for _, doc in records:
            if doc["kind"] != "xfactory_signed_execution_chain_log_leaf" \
                    or doc.get("leaf_type") != "gate_verdict":
                continue
            checks = doc["verdict"]["checks"]
            if mutate == "duplicate":
                checks[7] = dict(checks[5])
            else:
                checks[0], checks[1] = checks[1], checks[0]
        codes = reader.codes_of(_validate(records, registry_and_docs,
                                         carried).errors)
        assert "schema" in codes, mutate


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


# THE SWEEP'S SCOPE, IN BOTH DIRECTIONS. The whole-tree sweep collected only this
# family's OWN kinds until the § 5.8 canary build found it (openxFactory #579,
# fixed in #566): the three CONSUMED `add-trust-anchor` kinds every tier-2
# signature resolves against were dropped, so a VALID tranche-two chain placed in
# the tree drew 53 refusals — 49 `forged_attestation_identity` and 4
# `controller_anchor_not_held` — because the records that discharge the
# composition could never reach the scope that resolves them.
#
# THE TWO HALVES ARE ONE FIX AND ARE TESTED AS TWO. Admitting the kinds without
# generalizing the packaged-corpus exclusion sweeps `contracts/trust-anchor/`'s
# own deliberately-invalid negatives as LIVE records — measured, before the
# exclusion landed, as two `carried-vocabulary` refusals on a clean tree. The
# second half is already guarded by the whole-tree test above (it goes red
# without the exclusion, over the trust-anchor negatives this repository tracks);
# the tests below hold both halves HERMETICALLY, so they still stand if either
# family's packaged corpus moves — along with the four properties the bot bench
# on #566 found the sweep owed: a non-string `kind` skipped rather than crashing,
# a duplicate consumed identity refused rather than resolved by file order, an
# exclusion that cannot be evaded by placement, and an ambiguous scope refused
# without being walked.
#
# ONE FIXTURE, TWO PATHS, OPPOSITE OUTCOMES is the whole statement: the same
# bytes are adjudicated at a live path and excluded under a packaged `examples/`
# tree.
CONSUMED_FIXTURE = (
    REPO_ROOT / "contracts" / "trust-anchor" / "examples" / "negative"
    / "anchor-shortfall-cited-with-no-claim-moment.yaml")


def _swept(tmp_path, relative_path, registry_and_docs, carried):
    """Run the sweep over a tree holding ONE consumed-kind record at
    `relative_path`, plus one document of a kind this reader owns nothing of."""
    target = tmp_path / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(CONSUMED_FIXTURE.read_text(encoding="utf-8"),
                      encoding="utf-8")
    (tmp_path / "unrelated.yaml").write_text(
        "schema_version: 1\nkind: something_this_reader_does_not_own\n",
        encoding="utf-8")
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    return findings


def test_the_sweep_collects_and_adjudicates_the_consumed_trust_anchor_kinds(
        tmp_path, registry_and_docs, carried):
    """A consumed record at a LIVE path is in scope, and held to the vocabulary
    that owns it. Counting it is not enough — a kind admitted to the count and
    never adjudicated is the vacuous pass in miniature — so the fixture used is
    one `add-trust-anchor` itself packages as invalid, and the refusal proves the
    record was really read."""
    findings = _swept(tmp_path, "governance/anchor-under-adjudication.yaml",
                      registry_and_docs, carried)
    assert reader.codes_of(findings.errors) == {"carried-vocabulary"}
    assert len(findings.errors) == 1
    assert "1 artifact(s) checked" in findings.notes[0]
    # The kind this reader owns nothing of is still skipped and still counted.
    assert "1 skipped" in findings.notes[0]


def test_the_sweep_excludes_the_consumed_familys_own_packaged_examples(
        tmp_path, registry_and_docs, carried):
    """THE SAME BYTES under trust-anchor's packaged `examples/` tree draw
    NOTHING. A negative fixture is invalid ON PURPOSE and its own family's layer
    1 already asserts exactly how; re-adjudicating it here would make every
    checkout that vendors either family refuse on sight."""
    findings = _swept(
        tmp_path,
        "contracts/trust-anchor/examples/negative/anchor-shortfall.yaml",
        registry_and_docs, carried)
    assert findings.errors == []
    assert "0 artifact(s) checked" in findings.notes[0]


def test_the_sweeps_skipped_count_does_not_misreport_why(
        tmp_path, registry_and_docs, carried):
    """The note the operator reads when diagnosing a skip must name the scope the
    sweep actually has. It said "not a signed-execution-chain kind" while the
    sweep also admits the consumed vocabulary, which would send a reader looking
    for the wrong cause."""
    findings = _swept(tmp_path, "governance/anchor-under-adjudication.yaml",
                      registry_and_docs, carried)
    note = findings.notes[0]
    assert "not a signed-execution-chain kind" not in note
    assert "CONSUMED trust-anchor kinds" in note
    assert "BOTH families' packaged examples/ excluded" in note


def test_a_kind_that_is_not_a_string_is_skipped_and_never_crashes_the_sweep(
        tmp_path, registry_and_docs, carried):
    """A sweep reads ARBITRARY YAML, and `{"a": 1} in some_dict` RAISES rather
    than returning False. `kind: [a, b]` in one unrelated file took the whole
    scan down with a `TypeError` and discarded every other file's findings — a
    required gate felled by a document it does not even own. Found by Copilot on
    #566."""
    (tmp_path / "list-kind.yaml").write_text(
        "schema_version: 1\nkind: [a, b]\n", encoding="utf-8")
    (tmp_path / "mapping-kind.yaml").write_text(
        "schema_version: 1\nkind: {a: 1}\n", encoding="utf-8")
    (tmp_path / "numeric-kind.yaml").write_text(
        "schema_version: 1\nkind: 7\n", encoding="utf-8")
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    assert findings.errors == []
    assert "0 artifact(s) checked, 3 skipped" in findings.notes[0]


def test_two_consumed_records_sharing_an_id_are_ambiguous_not_last_seen(
        tmp_path, registry_and_docs, carried):
    """AN AMBIGUOUS CONSUMED SET IS REFUSED, NEVER RESOLVED BY FILE ORDER.

    The view that resolves consumed records keeps the LAST document it saw, so
    in an arbitrary checkout two certificates sharing an id would let
    lexicographic file order decide which fingerprint a tier-2 signature is
    compared against. `add-trust-anchor`'s own reader refuses this as
    `record-id-duplicate` on every copy; this reader already refuses a key id two
    wallets claim differently rather than taking the last one seen. Found by
    Codex on #566, where admitting the consumed kinds to the sweep is what made
    an UNCURATED consumed set reachable at all."""
    source = [d for d in yaml.safe_load_all(
        (EXAMPLES / "tranche-two" / "consumed-trust-anchor-records.example.yaml")
        .read_text(encoding="utf-8")) if d]
    certificate = next(d for d in source
                       if d.get("kind") == "xfactory_certificate_record")
    for name in ("a-first.yaml", "z-last.yaml"):
        (tmp_path / name).write_text(yaml.safe_dump(certificate, sort_keys=False),
                                     encoding="utf-8")
    findings = reader.Findings()
    registry, docs = registry_and_docs
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    assert "consumed-record-id-duplicate" in reader.codes_of(findings.errors)
    # REFUSED ON EVERY COPY, so the finding names both files rather than
    # whichever one file order happened to leave standing.
    duplicate = next(line for line in findings.errors
                     if "consumed-record-id-duplicate" in line)
    assert "a-first.yaml" in duplicate and "z-last.yaml" in duplicate
    # One copy alone is not ambiguous, and is not refused.
    (tmp_path / "z-last.yaml").unlink()
    findings = reader.Findings()
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    assert "consumed-record-id-duplicate" not in reader.codes_of(findings.errors)

    # AND THE OTHER LAYER-2 ENTRY POINT IS COVERED TOO, because `repo_scan()`
    # serves an explicitly named single file as well as a directory sweep, and one
    # file can carry a whole multi-document stream. The docstring says so, so it is
    # held to it rather than believed.
    one_file = tmp_path / "stream.yaml"
    one_file.write_text(yaml.safe_dump_all([certificate, certificate],
                                           sort_keys=False), encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, one_file, registry, docs, carried)
    assert "consumed-record-id-duplicate" in reader.codes_of(findings.errors)


def test_an_ambiguous_scope_is_not_walked_at_all(tmp_path, registry_and_docs,
                                                 carried):
    """FAIL CLOSED, DO NOT WALK. Refusing the duplicate and then walking anyway
    would leave every rule resolving through the identifiers just declared
    ambiguous, so the secondary findings would themselves depend on file order —
    the defect reported and then committed one line later. Found by Copilot on
    #566, in the review body rather than on a thread.

    The tree here would draw a `carried-vocabulary` refusal on its own, from a
    trust-anchor fixture invalid against the shape that owns it. Under an
    ambiguous set that finding is not reported, because the reading that produced
    it is not a reading anyone should act on."""
    registry, docs = registry_and_docs
    invalid = CONSUMED_FIXTURE.read_text(encoding="utf-8")
    (tmp_path / "invalid.yaml").write_text(invalid, encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    assert reader.codes_of(findings.errors) == {"carried-vocabulary"}, (
        "the baseline for this test is that the tree refuses on its own")

    source = [d for d in yaml.safe_load_all(
        (EXAMPLES / "tranche-two" / "consumed-trust-anchor-records.example.yaml")
        .read_text(encoding="utf-8")) if d]
    certificate = next(d for d in source
                       if d.get("kind") == "xfactory_certificate_record")
    for name in ("a-first.yaml", "z-last.yaml"):
        (tmp_path / name).write_text(yaml.safe_dump(certificate, sort_keys=False),
                                     encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    assert reader.codes_of(findings.errors) == {"consumed-record-id-duplicate"}, (
        "an ambiguous scope must be refused as unevaluable, not walked to "
        "produce order-dependent secondary findings")
    assert "NOT RUN" in next(line for line in findings.errors
                             if "consumed-record-id-duplicate" in line), (
        "the refusal must SAY the walk did not run, or a reader takes the "
        "absence of further findings for their absence in the tree")


def test_the_exclusion_ignores_components_above_the_scanned_tree(
        tmp_path, registry_and_docs, carried):
    """THE CHECKOUT'S OWN LOCATION MUST NOT SWITCH A REQUIRED GATE OFF.

    `main()` resolves the scan path, so every swept file's components include the
    directories a runner happened to put the checkout under. Matching the
    excluded sequence over that whole absolute path made the ENTIRE sweep
    skippable from outside the repository: a tree at
    `<anything>/contracts/<family>/examples/<checkout>` gave every file in it the
    sequence by inheritance, and the sweep reported `0 artifact(s) checked, 0
    skipped` over a live malformed record — never seen, no refusal, gate green.
    That is worse than the in-tree placement evasion below, because it needs no
    fabricated path inside the repository and takes out every file at once.
    Found by Codex on #566.

    Measured before the repair, for BOTH family names. The neutral-ancestor case
    is asserted first so the test cannot pass by the fixture simply being inert.
    """
    registry, docs = registry_and_docs
    invalid = CONSUMED_FIXTURE.read_text(encoding="utf-8")

    def swept_under(ancestor: str):
        root = tmp_path / ancestor / "domain-repo"
        record = root / "governance" / "live-and-malformed.yaml"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(invalid, encoding="utf-8")
        findings = reader.Findings()
        # RESOLVED, exactly as `main()` hands it over — an unresolved relative
        # path would not carry the ancestors this test is about.
        reader.repo_scan(findings, root.resolve(), registry, docs, carried)
        return findings

    baseline = swept_under("work")
    assert "1 artifact(s) checked" in baseline.notes[0]
    assert reader.codes_of(baseline.errors) == {"carried-vocabulary"}, (
        "the baseline for this test is that the record refuses at a live path")

    for family in ("trust-anchor", "signed-execution-chain"):
        findings = swept_under(f"work/contracts/{family}/examples")
        assert "1 artifact(s) checked" in findings.notes[0], (
            f"a checkout parked under contracts/{family}/examples had its whole "
            f"sweep excluded by its own location: {findings.notes[0]}")
        assert reader.codes_of(findings.errors) == {"carried-vocabulary"}

    # AND THE VENDORED CORPUS INSIDE THE TREE IS STILL EXCLUDED — the property
    # relativizing must not cost, since a domain repo scans a COPY.
    vendored = tmp_path / "consumer"
    for family in ("trust-anchor", "signed-execution-chain"):
        target = (vendored / "vendor" / "openxFactory" / "contracts" / family
                  / "examples" / "negative" / "fixture.yaml")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(invalid, encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, vendored.resolve(), registry, docs, carried)
    assert findings.errors == []
    assert "0 artifact(s) checked" in findings.notes[0]


def test_skip_dir_names_ignore_components_above_the_scanned_tree(
        tmp_path, registry_and_docs, carried):
    """THE SAME PLACEMENT EVASION, ONE CHECK EARLIER THAN THE ONE ABOVE.

    `SKIP_DIR_NAMES` was matched over the ABSOLUTE path too, so a checkout
    parked under a `.venv/`, `node_modules/`, `.git/` or `__pycache__/`
    ANCESTOR gave every file in it one of those names by inheritance and
    switched the whole sweep off, before `under_packaged_examples()` is ever
    reached — the same checkout-location evasion closed two commits ago, on
    the check that runs immediately after this one. Found by Copilot on #566.

    The ancestor case is asserted first so the test cannot pass by the fixture
    simply being inert; the in-tree control then proves relativizing did not
    cost the property SKIP_DIR_NAMES exists for.
    """
    registry, docs = registry_and_docs
    invalid = CONSUMED_FIXTURE.read_text(encoding="utf-8")

    def swept_under(ancestor: str):
        root = tmp_path / ancestor / "domain-repo"
        record = root / "governance" / "live-and-malformed.yaml"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(invalid, encoding="utf-8")
        findings = reader.Findings()
        # RESOLVED, exactly as `main()` hands it over — an unresolved relative
        # path would not carry the ancestor this test is about.
        reader.repo_scan(findings, root.resolve(), registry, docs, carried)
        return findings

    for skip_name in sorted(reader.SKIP_DIR_NAMES):
        findings = swept_under(skip_name)
        assert "1 artifact(s) checked" in findings.notes[0], (
            f"a checkout parked under a {skip_name}/ ancestor had its whole "
            f"sweep excluded by its own location: {findings.notes[0]}")
        assert reader.codes_of(findings.errors) == {"carried-vocabulary"}

    # AND A SKIP-NAMED DIRECTORY INSIDE THE TREE IS STILL EXCLUDED — the
    # property relativizing must not cost, since a real checkout does carry a
    # `.venv/` or `node_modules/` of its own.
    root = tmp_path / "consumer"
    record = root / ".venv" / "vendor-lib" / "fixture.yaml"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(invalid, encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, root.resolve(), registry, docs, carried)
    assert findings.errors == []
    assert "0 artifact(s) checked" in findings.notes[0]


def test_an_unadjudicated_scope_is_never_reported_as_checked(
        tmp_path, registry_and_docs, carried):
    """THE NOTE MUST NOT CALL A SCOPE "CHECKED" THAT NO RULE WAS APPLIED TO.

    Under an ambiguous consumed set the walk does not run — the test above pins
    that — but the operator-facing note still counted the collected documents as
    `N artifact(s) checked`. A reader who trusts that count takes the absence of
    further findings for a clean reading of those records, which is the vacuous
    pass in miniature and the exact confusion the walk was skipped to avoid.
    Found by Copilot on #566.

    ZERO is the honest count, the collected size is still reported, and the
    gate's own anti-vacuity grep — which asks for `N artifact(s) checked` — is
    satisfied by the truthful zero rather than being fooled by a false N."""
    registry, docs = registry_and_docs
    source = [d for d in yaml.safe_load_all(
        (EXAMPLES / "tranche-two" / "consumed-trust-anchor-records.example.yaml")
        .read_text(encoding="utf-8")) if d]
    certificate = next(d for d in source
                       if d.get("kind") == "xfactory_certificate_record")
    for name in ("a-first.yaml", "z-last.yaml"):
        (tmp_path / name).write_text(yaml.safe_dump(certificate, sort_keys=False),
                                     encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    note = findings.notes[0]
    assert reader.codes_of(findings.errors) == {"consumed-record-id-duplicate"}, (
        "the baseline for this test is an ambiguous, unwalked scope")
    assert "2 artifact(s) checked" not in note, (
        "the note reported an unadjudicated scope as checked: " + note)
    assert "0 artifact(s) checked" in note
    assert "2 collected and then NOT ADJUDICATED" in note
    assert "THE CHAIN WALK OVER THIS SCOPE WAS NOT RUN" in note

    # THE GATE'S OWN GREP still matches, so the ambiguous run fails on its
    # refusal and not on a misdiagnosed "the sweep did not run".
    assert re.match(r"^note  repo scan \(.*\): [0-9]+ artifact\(s\) checked",
                    note), (
        "the gate's anti-vacuity step greps this exact shape; an ambiguous run "
        "must fail on its refusal, not on a misdiagnosed 'sweep did not run'")


def test_the_corpus_exclusion_is_not_evadable_by_placement(
        tmp_path, registry_and_docs, carried):
    """THE EXCLUSION IS A PACKAGED-CORPUS EXCLUSION, NOT A KEYWORD FILTER.

    It cannot be anchored to this checkout's paths — a domain repo vendors
    openxFactory and scans a COPY — so it matches path COMPONENTS. Asking only
    whether the words appear ANYWHERE made the required gate evadable by
    placement: a chain record parked under any path carrying both `examples` and
    a family name was dropped from the sweep and drew no finding. Found by Codex
    on #566. Requiring the components ADJACENT keeps every vendored copy
    excluded and admits the paths that merely mention them."""
    registry, docs = registry_and_docs
    consumed = CONSUMED_FIXTURE.read_text(encoding="utf-8")
    evasive = [
        "governance/trust-anchor/live/examples/invalid.yaml",
        "governance/signed-execution-chain/live/examples/invalid.yaml",
        "somewhere/examples/deep/trust-anchor/invalid.yaml",
        # THE SECOND ROUND'S PATHS, which mere ADJACENCY of `<family>/examples`
        # still dropped — the shape the packaged corpus does NOT occupy, because
        # it lives under `contracts/`. Copilot found the first repair
        # insufficient on exactly these.
        "governance/trust-anchor/examples/invalid.yaml",
        "governance/signed-execution-chain/examples/invalid.yaml",
    ]
    # DISTINCT IDENTITIES, because three copies of one record are an AMBIGUOUS
    # scope and the reader refuses that without walking — the fail-closed rule
    # below. This test is about placement, so it gives each copy its own id and
    # leaves ambiguity to the test that owns it.
    for index, relative_path in enumerate(evasive):
        record = yaml.safe_load(consumed)
        record["anchor_id"] = f"anchor:evasive-{index}"
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(yaml.safe_dump(record, sort_keys=False),
                          encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, tmp_path, registry, docs, carried)
    assert f"{len(evasive)} artifact(s) checked" in findings.notes[0], (
        "a record the reader owns was dropped from the sweep by where it sits")
    assert len(findings.errors) >= len(evasive)

    # AND THE VENDORED PACKAGED CORPUS IS STILL EXCLUDED, at a prefix that is not
    # this checkout's — the property the component test exists to keep.
    vendored = tmp_path / "vendor"
    for family in ("trust-anchor", "signed-execution-chain"):
        target = (vendored / "openxFactory" / "contracts" / family / "examples"
                  / "negative" / "fixture.yaml")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(consumed, encoding="utf-8")
    findings = reader.Findings()
    reader.repo_scan(findings, vendored, registry, docs, carried)
    assert findings.errors == []
    assert "0 artifact(s) checked" in findings.notes[0]


def test_the_reader_no_longer_says_the_capability_confers_nothing(
        registry_and_docs, carried):
    """Requirement 9 is about this capability's own standing, and the reader
    states it where it runs rather than only in the declaration. THIS TEST USED TO
    ASSERT THE WARNING WAS THERE, and it was there for as long as the standing it
    reports was the true one. Task 4.5 was performed on 2026-08-31 — org ruleset
    21957695 requires `signed-execution-chain-gate` on `main` — and task 4.6 saw
    the refusal reach a real pull request (canary #549, run 33455808456), so the
    packaged declaration records `is_required_in_ruleset: true` and the warning
    stops firing. That is the point at which these records begin to confer
    anything at all, and the assertion is inverted rather than deleted so the
    reader cannot go quiet for the OTHER reason — a declaration still recording
    the reader unrequired, which the test below still holds it to."""
    findings = _validate(reader.positive_records(), registry_and_docs, carried)
    assert not any("reader-not-required" in line for line in findings.warnings)


def test_a_declaration_recording_the_reader_unrequired_still_warns(
        registry_and_docs, carried):
    """The rule is not retired by the ruleset act — it is the rule that made the
    act legible in the first place, and a realization that is NOT gated (a domain
    repository consuming this family, or this one if the ruleset were ever
    dropped) must still be told so on every run."""
    import copy

    records = copy.deepcopy(reader.positive_records())
    for _, doc in records:
        if doc["kind"] == \
                "xfactory_signed_execution_chain_conformance_declaration":
            doc["realization"]["reader_required_check"][
                "is_required_in_ruleset"] = False
    findings = _validate(records, registry_and_docs, carried)
    assert any("reader-not-required" in line for line in findings.warnings)


def test_a_declaration_recording_sec_r9_satisfied_while_unrequired_is_refused(
        registry_and_docs, carried):
    """The pairing above is not decoration: a declaration may record the reader as
    unrequired, and it may NOT then record the obligation as satisfied. Where no
    such check exists the requirement is UNMET, not partially met.

    THE MUTATION NOW HAS TO SET THE READER UNREQUIRED TOO, because the packaged
    declaration no longer is: SEC-R9 `satisfied` is the CORRECT record since
    2026-08-31, and this refusal is about the pairing, never about the word."""
    import copy

    records = copy.deepcopy(reader.positive_records())
    for _, doc in records:
        if doc["kind"] == \
                "xfactory_signed_execution_chain_conformance_declaration":
            doc["realization"]["reader_required_check"][
                "is_required_in_ruleset"] = False
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


def test_the_obligation_set_is_the_eighteen_requirements_of_the_deltas():
    """The delta is the authority for the count. Tranche one's nine ADDED
    requirements over 45 scenarios, then add-chain-attestation's NINE ADDED over
    108 (ratified 2026-09-01 at 6d7ef17b): eighteen obligations, in the deltas'
    own order, and a declaration naming any tranche-two obligation is closed
    over all eighteen."""
    schema = yaml.safe_load(
        (REPO_ROOT / "contracts" / "signed-execution-chain" /
         "conformance-declaration.schema.yaml").read_text(encoding="utf-8"))
    declared = schema["properties"]["obligations"]["items"]["properties"][
        "obligation"]["enum"]
    assert declared == reader.OBLIGATIONS
    assert len(declared) == 18
    # A tranche-one-only declaration carries nine entries and stays valid — the
    # shipped bundle's instance is not refused by this extension — while a
    # declaration naming any tranche-two obligation is closed over all eighteen
    # by the reader's coverage rule.
    assert schema["properties"]["obligations"]["minItems"] == 9
    assert schema["properties"]["obligations"]["maxItems"] == 18
