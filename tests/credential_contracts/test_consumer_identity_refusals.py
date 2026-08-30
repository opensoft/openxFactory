"""The consumer-identity refusals (add-binding-consumer-identity §2.3–§2.7).

A TEST PER CONDITION, EACH PROVING THE REFUSAL STANDS WHEN ONLY THAT CONDITION
IS MISSING — and then a mutation round proving each condition is load-bearing in
the code rather than merely present in it.

THE MUTATION ROUND'S CONTROL IS A BASELINE, NOT A NAME. Naming the killing test
fixes attribution; it does NOT detect ANCHOR-MISSING, where the named test fails
on the mutant because its fixture or assertion target is absent rather than
because the mutation was caught. So each mutant records BOTH halves: the named
check PASSES against unmutated code, and FAILS against the mutant. The mutant
population is an explicit count — NINE.
"""
from __future__ import annotations

import copy
import importlib.util
from itertools import combinations
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load():
    spec = importlib.util.spec_from_file_location(
        "credential_contracts_validator_refusals",
        ROOT / "scripts" / "validate-credential-contracts.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


V = _load()

REQUIREMENTS_DOC = "credentials/projection.requirements.yaml"
INDEX = {
    REQUIREMENTS_DOC: [
        {"id": "projection_sync_lane", "access_mode": "workload_identity"},
        {"id": "projection_editor_surface", "access_mode": "workload_identity"},
        {"id": "projection_report_builder", "access_mode": "workload_identity"},
        {"id": "intent_dispatch", "access_mode": "dispatch_only"},
        {"id": "corpus_content_write", "access_mode": "contents_write"},
    ],
}


def _binding(secret="one-operated-identity", **consumer):
    binding = {"provider": "azure_key_vault", "vault": "kv-example", "secret_ref": secret,
               "owner": "example-platform", "rotation_policy": "operator_managed"}
    if consumer:
        binding["consumer"] = consumer
    return binding


def _ref(requirement_id, document=REQUIREMENTS_DOC):
    return {"requirement_id": requirement_id, "requirements_document_ref": document}


def _conforming_pair():
    """The packaged POSITIVE's shape: two consuming systems, one operated
    identity, all six conditions satisfied."""
    return {
        "schema_version": 1,
        "kind": "xfactory_credential_binding_template",
        "client": {"id": "example-client"},
        "credential_bindings": {
            "projection_sync_lane": _binding(
                holder_ref="example:service-subject:projection-sync-lane",
                fetch_identity="example-sync-lane-workload-identity",
                requirement_ref=_ref("projection_sync_lane"),
                shared_credential_acknowledged=True),
            "projection_editor_surface": _binding(
                holder_ref="example:service-subject:projection-editor-surface",
                fetch_identity="example-editor-surface-workload-identity",
                requirement_ref=_ref("projection_editor_surface"),
                shared_credential_acknowledged=True),
        },
    }


def _findings(doc, index=None):
    return V._semantic_findings(doc, INDEX if index is None else index)


def _codes(doc, index=None):
    return sorted({f.split(":", 1)[0] for f in _findings(doc, index)})


# --------------------------- the lift, condition by condition ---------------------------

def test_the_conforming_pair_lifts():
    """The shape the predecessor had to DECLINE. If this ever stops lifting, the
    per-condition tests below stop meaning anything — they would all be passing
    on a refusal that was never available to lift."""
    assert _findings(_conforming_pair()) == []


def test_condition_1_a_pair_that_declares_nothing_is_refused():
    doc = _conforming_pair()
    for binding in doc["credential_bindings"].values():
        del binding["consumer"]
    assert _codes(doc) == ["shared-secret-identity"]


def test_condition_1_one_side_declaring_nothing_is_refused():
    doc = _conforming_pair()
    del doc["credential_bindings"]["projection_editor_surface"]["consumer"]
    assert _codes(doc) == ["shared-secret-identity"]


def test_condition_2_a_shared_holder_reference_is_refused():
    doc = _conforming_pair()
    doc["credential_bindings"]["projection_editor_surface"]["consumer"]["holder_ref"] = \
        "example:service-subject:projection-sync-lane"
    assert _codes(doc) == ["shared-secret-identity"]


def test_condition_3_a_shared_fetch_identity_is_refused_under_the_NAMED_fault():
    """Condition 3's failure is already refused by the default rule, so the new
    code adds no refusal — it adds a refusal that NAMES THE FAULT. A reader told
    about secret reuse would split the secret and keep the shared authority."""
    doc = _conforming_pair()
    doc["credential_bindings"]["projection_editor_surface"]["consumer"]["fetch_identity"] = \
        "example-sync-lane-workload-identity"
    assert _codes(doc) == ["shared-authority-identity"]


def test_condition_3_a_MISSING_fetch_identity_is_refused():
    """The lift's third condition has two arms and only one of them is reached
    HERE. Where both fetch identities are present and EQUAL while the holders
    differ, the named `shared-authority-identity` fault applies and REPLACES the
    default finding for that pair — one fault, one finding — so the arm the lift
    itself still owns is the one where an identity is missing or is not a
    string, and the per-system authority is therefore unproven rather than
    collapsed."""
    doc = _conforming_pair()
    del doc["credential_bindings"]["projection_editor_surface"]["consumer"]["fetch_identity"]
    findings = _findings(doc)
    assert _codes(doc) == ["shared-secret-identity"]
    assert "fetch_identity is missing" in findings[0]


def test_condition_4_a_one_sided_acknowledgment_is_refused():
    doc = _conforming_pair()
    del doc["credential_bindings"]["projection_editor_surface"]["consumer"][
        "shared_credential_acknowledged"]
    assert _codes(doc) == ["shared-secret-identity"]


def test_condition_4_a_false_valued_acknowledgment_is_refused():
    doc = _conforming_pair()
    doc["credential_bindings"]["projection_editor_surface"]["consumer"][
        "shared_credential_acknowledged"] = False
    assert _codes(doc) == ["shared-secret-identity"]


def _dispatch_and_content_pair():
    """An HONEST dispatch/content pair: each reference names its own map key, so
    condition six holds and only condition five can stand."""
    doc = _conforming_pair()
    bindings = doc["credential_bindings"]
    bindings["intent_dispatch"] = bindings.pop("projection_sync_lane")
    bindings["corpus_content_write"] = bindings.pop("projection_editor_surface")
    bindings["intent_dispatch"]["consumer"]["requirement_ref"] = _ref("intent_dispatch")
    bindings["corpus_content_write"]["consumer"]["requirement_ref"] = _ref("corpus_content_write")
    return doc


def test_condition_5_a_dispatch_and_content_pair_is_refused_however_declared():
    doc = _dispatch_and_content_pair()
    assert _codes(doc) == ["shared-secret-identity"]
    assert "access modes differ" in _findings(doc)[0]


def test_condition_5_two_dispatch_only_consumers_are_refused_by_a_DELIBERATE_over_refusal():
    """The exclusion over-refuses on purpose and the over-refusal is named rather
    than left to be discovered: two consumers of ONE dispatch-only credential are
    refused too, which nothing else in this capability forbids. The dispatch
    class is where serving-tier separation lives, the population of real
    two-consumer dispatch cases is currently zero, and a rule that refuses a
    shape nobody needs is cheaper to relax later than one that permits a shape
    nobody checked."""
    index = copy.deepcopy(INDEX)
    for record in index[REQUIREMENTS_DOC]:
        record["access_mode"] = "dispatch_only"
    assert _codes(_conforming_pair(), index) == ["shared-secret-identity"]


def test_condition_6_a_pair_pointing_at_a_requirement_neither_binding_is_is_refused():
    """L2, the execution that defeated the five-condition draft: both references
    aimed at one requirement so the access modes compare equal."""
    doc = _conforming_pair()
    for binding in doc["credential_bindings"].values():
        binding["consumer"]["requirement_ref"] = _ref("projection_sync_lane")
    assert _codes(doc) == ["shared-secret-identity"]
    assert "not its own map key" in _findings(doc)[0]


def test_the_packaged_serving_tier_negative_stays_refused_however_it_is_declared():
    """`dispatch-reuses-content-secret.yaml` is this capability's ONLY red proof
    of serving-tier separation, and the seat broke it with FOUR declarations and
    its shared secret untouched. It carries those four declarations now."""
    import yaml
    path = ROOT / "examples/credential-contracts/negative/dispatch-reuses-content-secret.yaml"
    doc = yaml.safe_load(path.read_text())
    consumers = [b["consumer"] for b in doc["credential_bindings"].values()]
    assert len({c["holder_ref"] for c in consumers}) == 2
    assert len({c["fetch_identity"] for c in consumers}) == 2
    assert all(c["shared_credential_acknowledged"] is True for c in consumers)
    assert doc["credential_bindings"]["intent_dispatch"]["secret_ref"] == \
        doc["credential_bindings"]["corpus_content_write"]["secret_ref"]
    assert _codes(doc, {"openxdox-dispatch.requirements.example.yaml": INDEX[REQUIREMENTS_DOC]}) \
        == ["shared-secret-identity"]


# --------------------------- the arity (§2.3a) ---------------------------

def _three_bindings():
    doc = _conforming_pair()
    doc["credential_bindings"]["projection_report_builder"] = _binding(
        holder_ref="example:service-subject:projection-report-builder",
        fetch_identity="example-editor-surface-workload-identity",
        requirement_ref=_ref("projection_report_builder"),
        shared_credential_acknowledged=True)
    return doc


def test_three_bindings_with_the_second_and_third_sharing_an_authority_are_refused():
    """The inherited predicate kept the FIRST binding per secret and compared
    later ones against it, so the pair (b, c) was NEVER examined and this record
    was accepted on both examined pairs."""
    assert _codes(_three_bindings()) == ["shared-authority-identity"]


def test_the_pairs_examined_are_every_pair_and_not_the_first_against_the_rest():
    doc = _three_bindings()
    findings = _findings(doc)
    assert len(findings) == 1
    assert "projection_editor_surface" in findings[0]
    assert "projection_report_builder" in findings[0]
    assert "projection_sync_lane" not in findings[0]


# --------------------------- the access mode (§2.3b) ---------------------------

@pytest.mark.parametrize("mode", [None, 7, "Workload_Identity", "not_a_mode"])
def test_an_unreadable_access_mode_makes_the_lift_UNAVAILABLE(mode):
    index = copy.deepcopy(INDEX)
    for record in index[REQUIREMENTS_DOC]:
        if mode is None:
            record.pop("access_mode", None)
        else:
            record["access_mode"] = mode
    assert _codes(_conforming_pair(), index) == ["shared-secret-identity"]


def test_two_ABSENT_access_modes_do_not_compare_equal_to_each_other():
    """`None == None` was one of three lifts a security seat drove through this
    field. Unreadable means UNAVAILABLE, never "equal, and not dispatch-only"."""
    index = copy.deepcopy(INDEX)
    for record in index[REQUIREMENTS_DOC]:
        record.pop("access_mode", None)
    findings = _findings(_conforming_pair(), index)
    assert findings and "unreadable makes the lift UNAVAILABLE" in findings[0]


def test_a_variant_spelling_does_not_compare_equal_to_itself():
    index = copy.deepcopy(INDEX)
    for record in index[REQUIREMENTS_DOC]:
        record["access_mode"] = "Dispatch_Only"
    assert _codes(_conforming_pair(), index) == ["shared-secret-identity"]


# --------------------------- resolution (§2.5) ---------------------------

def test_a_reference_resolving_to_nothing_is_reported_and_withholds_the_lift():
    doc = _conforming_pair()
    for binding in doc["credential_bindings"].values():
        binding["consumer"]["requirement_ref"] = _ref(
            binding["consumer"]["requirement_ref"]["requirement_id"], "credentials/absent.yaml")
    findings = _findings(doc)
    assert findings and "resolves to no requirement" in findings[0]


def test_a_reference_resolving_to_TWO_records_with_different_modes_is_reported():
    index = {REQUIREMENTS_DOC: INDEX[REQUIREMENTS_DOC] + [
        {"id": "projection_sync_lane", "access_mode": "delegated_api"}]}
    findings = _findings(_conforming_pair(), index)
    assert findings and "MORE THAN ONE requirement" in findings[0]


def test_the_ambiguity_is_never_resolved_by_picking_one():
    """The two matches may carry different access modes, so a rule whose outcome
    depends on which was found first is not a rule. Both orders must refuse."""
    extra = {"id": "projection_sync_lane", "access_mode": "delegated_api"}
    for index in ({REQUIREMENTS_DOC: INDEX[REQUIREMENTS_DOC] + [extra]},
                  {REQUIREMENTS_DOC: [extra] + INDEX[REQUIREMENTS_DOC]}):
        assert _codes(_conforming_pair(), index) == ["shared-secret-identity"]


@pytest.mark.parametrize("document", ["../elsewhere/requirements.yaml",
                                      "/etc/credentials/requirements.yaml",
                                      "OpsxFactory:credentials/requirements.yaml"])
def test_a_reference_that_escapes_the_tree_is_ungrammatical_and_withholds_the_lift(document):
    doc = _conforming_pair()
    for binding in doc["credential_bindings"].values():
        binding["consumer"]["requirement_ref"] = _ref(
            binding["consumer"]["requirement_ref"]["requirement_id"], document)
    findings = _findings(doc)
    assert findings and "absolute, escaping, or foreign-repository" in findings[0]


def test_a_reference_carrying_an_EXTRA_member_does_not_resolve():
    """PR #516, Copilot. The resolver documented "the two-member object" while
    checking only that the two were PRESENT, so a reference with a third key
    could resolve and satisfy the lift — accepting a shape the major's closed
    block refuses, and doing it on the exemption path where fail-closed matters
    most. Refusing to RESOLVE it refuses no record: it withholds an exemption,
    and the default refusal it leaves standing is the one that already stands."""
    doc = _conforming_pair()
    for binding in doc["credential_bindings"].values():
        binding["consumer"]["requirement_ref"]["custody_declared_in"] = "somewhere.yaml"
    findings = _findings(doc)
    assert findings and "is not a qualified reference" in findings[0]
    assert "consumer-member-grammar" in [c for c, _ in V._deprecation_warnings(doc)]


@pytest.mark.parametrize("record", [
    {"schema_version": 1, "kind": "xfactory_credential_binding_template",
     "client": {"id": "c"},
     "credential_bindings": {"r": {"provider": "p", "secret_ref": "s", "owner": "o",
                                   "rotation_policy": "rp",
                                   "consumer": {"holder_ref": "example:holder",
                                                "fetch_identity": "example-identity",
                                                "requirement_ref": {
                                                    "requirement_id": "r",
                                                    "requirements_document_ref": "r.yaml",
                                                    1: "an int key"}}}}},
    {"schema_version": 1, "kind": "xfactory_credential_binding_template",
     "client": {"id": "c"},
     "credential_bindings": {"r": {"provider": "p", "secret_ref": "s", "owner": "o",
                                   "rotation_policy": "rp",
                                   "consumer": {"holder_ref": "example:holder",
                                                "fetch_identity": "example-identity",
                                                2: "an int member"}}}},
    {"schema_version": 1, "kind": "xfactory_credential_requirements",
     "domain": {"id": "d"},
     "requirements": [{"id": "r", "purpose": "p", "access_mode": "workload_identity",
                       "requires_domain_approval": True, "requires_human_approval": False,
                       "max_grant_minutes": 60, "audit_required": True,
                       "issuance_preconditions": {"accepted_request_required": True,
                                                  3: True}}]},
], ids=["reference-key", "block-member", "issuance-precondition"])
def test_a_NON_STRING_KEY_is_reported_rather_than_raised(record):
    """PR #516, Codex round 2. The block is UNCONSTRAINED at this minor, so a
    record may hold a mapping whose keys are not all strings — YAML writes
    `1: extra` as an int key — and a bare `sorted()` over mixed types raises
    TypeError, aborting the WHOLE repository scan on a record this release
    promises stays valid and warned. A crash is not a verdict.

    The parametrisation is the SWEEP rather than the one line a bot pointed at:
    this validator sorts record-controlled keys in three places, and all three
    are driven here."""
    assert isinstance(V._deprecation_warnings(record), list)
    assert isinstance(V._semantic_findings(record, INDEX), list)


def test_an_overlong_document_reference_does_not_resolve():
    doc = _conforming_pair()
    overlong = "credentials/" + ("a" * 400) + ".yaml"
    for binding in doc["credential_bindings"].values():
        binding["consumer"]["requirement_ref"]["requirements_document_ref"] = overlong
    findings = _findings(doc)
    assert findings and "absolute, escaping, or foreign-repository" in findings[0]


def test_a_bare_requirement_id_does_not_satisfy_the_condition():
    doc = _conforming_pair()
    for binding in doc["credential_bindings"].values():
        binding["consumer"]["requirement_ref"] = \
            binding["consumer"]["requirement_ref"]["requirement_id"]
    findings = _findings(doc)
    assert findings and "is not a qualified reference" in findings[0]


def test_the_resolver_never_opens_a_path_taken_from_a_record(tmp_path, monkeypatch):
    """Resolution is a lookup against records the validator itself discovered.
    A record cannot steer it at a file of the record's choosing — so no file
    read happens at resolution time at all."""
    opened = []
    real_open = Path.open

    def spy(self, *args, **kwargs):
        opened.append(str(self))
        return real_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", spy)
    V.resolve_requirement(_ref("projection_sync_lane", "credentials/anything.yaml"), INDEX)
    assert opened == []


# --------------------------- the named fault (§2.4) ---------------------------

def test_the_authority_finding_is_not_scoped_to_a_shared_secret_reference():
    """Two different holders declaring one fetch identity is the collapse
    WHATEVER their secret references; scoping the finding to the proxy would
    leave it unreported when two spellings name one secret."""
    doc = _conforming_pair()
    bindings = doc["credential_bindings"]
    bindings["projection_editor_surface"]["secret_ref"] = "a-second-spelling-of-one-secret"
    bindings["projection_editor_surface"]["consumer"]["fetch_identity"] = \
        "example-sync-lane-workload-identity"
    assert _codes(doc) == ["shared-authority-identity"]


def test_one_holder_reusing_its_own_fetch_identity_reports_nothing():
    """A system legitimately authenticates as itself across the credentials it
    holds. The subtraction that matters was performed BEFORE widening the
    finding past the secret reference."""
    doc = _conforming_pair()
    bindings = doc["credential_bindings"]
    bindings["projection_editor_surface"]["secret_ref"] = "a-different-secret"
    bindings["projection_editor_surface"]["consumer"]["holder_ref"] = \
        bindings["projection_sync_lane"]["consumer"]["holder_ref"]
    bindings["projection_editor_surface"]["consumer"]["fetch_identity"] = \
        bindings["projection_sync_lane"]["consumer"]["fetch_identity"]
    assert _findings(doc) == []


def test_the_authority_finding_compares_only_GRAMMATICAL_identities():
    """PR #516, Codex P1. This is the one arm of this change that can raise a NEW
    error on a record carrying no shared secret, so it is the one place a
    malformed value could turn a deprecation into a refusal: two bindings whose
    consumers both carry `fetch_identity: ""` validate on the current major, and
    reading them as "the same identity" would refuse in a MINOR a shape the
    current major accepts. The malformed values are warned instead, and refused
    at the major with everything else."""
    doc = _conforming_pair()
    bindings = doc["credential_bindings"]
    bindings["projection_editor_surface"]["secret_ref"] = "a-different-secret"
    for name in bindings:
        bindings[name]["consumer"]["fetch_identity"] = ""
    assert _findings(doc) == []
    codes = [c for c, _ in V._deprecation_warnings(doc)]
    assert codes.count("consumer-member-grammar") == 2


def test_a_grammatical_shared_authority_is_still_refused():
    """The negative control: the guard above must cost the finding nothing on the
    values it exists to catch."""
    doc = _conforming_pair()
    bindings = doc["credential_bindings"]
    bindings["projection_editor_surface"]["secret_ref"] = "a-different-secret"
    bindings["projection_editor_surface"]["consumer"]["fetch_identity"] = \
        bindings["projection_sync_lane"]["consumer"]["fetch_identity"]
    assert _codes(doc) == ["shared-authority-identity"]


def test_the_named_fault_REPLACES_the_default_finding_rather_than_accompanying_it():
    """One fault SHALL produce one finding, or a reader repairing the named fault
    is left with a second refusal describing the same record."""
    doc = _conforming_pair()
    doc["credential_bindings"]["projection_editor_surface"]["consumer"]["fetch_identity"] = \
        "example-sync-lane-workload-identity"
    findings = _findings(doc)
    assert len(findings) == 1
    assert findings[0].startswith("shared-authority-identity")


def test_a_record_that_declares_no_consumer_is_refused_exactly_as_it_is_today():
    """Nothing that is refused today becomes accepted by silence: this change
    tightens before it lifts."""
    doc = _conforming_pair()
    for binding in doc["credential_bindings"].values():
        binding.pop("consumer")
    findings = _findings(doc)
    assert len(findings) == 1 and findings[0].startswith("shared-secret-identity")


# --------------------------- the screen (§2.6, openxFactory#506) ---------------------------

@pytest.mark.parametrize("value", [
    "-----BEGIN RSA PRIVATE KEY-----",
    "ghp_0123456789abcdefghijklmnopqrstuvwxyz",
    "github_pat_11ABCDEF0123456789exampleRawTokenNotAReference",
    "AKIAIOSFODNN7EXAMPLE",
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345",
    # openxFactory#506 — three families the marker list and the base64 screen
    # both missed while the screen's SCOPE was being widened to two new fields.
    "postgresql://user:hunter2@db.example.invalid/projection",
    "mongodb+srv://svc:s3cr3t@cluster.example.invalid/db",
    "password=hunter2",
    "Server=tcp:example;AccountKey=abc123;",
    "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJmaXh0dXJlIn0.",
])
def test_the_screen_recognises_a_raw_secret(value):
    assert V._looks_like_raw_secret(value)


@pytest.mark.parametrize("value", [
    "opsx:service-subject:aks-opensoft-qa",
    "example-sync-lane-workload-identity",
    "xf.sync.lane",                     # a dotted identifier is NOT a JWT
    "install_federated_workload_identity",
    "https://vault.example.invalid/secrets/one",   # a URI with no credentials
    "kv-opensoft-xfactory-qa",
])
def test_the_screen_admits_a_legitimate_identifier(value):
    """A screen that refused a dotted identifier or a plain URI would be worse
    than the gap it closes."""
    assert not V._looks_like_raw_secret(value)


def test_the_screen_reads_the_two_new_sinks_and_not_only_secret_ref():
    for field in ("holder_ref", "fetch_identity"):
        doc = _conforming_pair()
        doc["credential_bindings"]["projection_sync_lane"]["consumer"][field] = \
            "postgresql://user:hunter2@db.example.invalid/projection"
        assert any(f.startswith("baked-secret") and f"consumer.{field}" in f
                   for f in _findings(doc)), field


def test_the_screens_known_limit_is_recorded_rather_than_claimed_away():
    """`_B64ISH` requires 40 characters, so a 38-character alphanumeric secret
    passes even after the expansion. The screen catches shapes it recognises; it
    is not a secret detector, and a test that pretended otherwise would be the
    coverage claim the packet refuses to make."""
    thirty_eight = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9"
    assert len(thirty_eight) == 38
    assert not V._looks_like_raw_secret(thirty_eight)


# --------------------------- the mutation round (§2.7) ---------------------------
#
# NINE MUTANTS: six lift conditions, the every-pair arity, the unreadable
# access-mode arm, and the resolution-ambiguity arm.

def _blind_condition(condition):
    """The mutant: this condition no longer refuses anything."""
    real = V._lift_refusal_detail

    def mutant(first, second, index):
        found, reason = real(first, second, index)
        return (None, None) if found == condition else (found, reason)
    return "_lift_refusal_detail", mutant


def _first_against_rest():
    """The INHERITED shape: keep the first binding per secret and compare later
    ones against it, so the pair (b, c) is never examined."""
    def mutant(items, r):
        items = list(items)
        return [(items[0], other) for other in items[1:]] if items and r == 2 else \
            list(combinations(items, r))
    return "combinations", mutant


def _fail_open_access_mode():
    """The pre-repair reading: compare whatever the record holds. `str()` keeps
    the honest values honest and reproduces the two defeats exactly — two ABSENT
    modes compare equal to each other ("None" == "None") and a variant spelling
    compares equal to itself, both "equal, and not dispatch-only", both
    lifting."""
    return "_readable_access_mode", lambda record: str(record.get("access_mode"))


def _disambiguate_by_picking_one():
    """The rule with an opinion: on more than one match, take the first."""
    real = V.resolve_requirement

    def mutant(ref, index):
        status, record = real(ref, index)
        if status == "ambiguous":
            rid = ref["requirement_id"]
            doc = ref["requirements_document_ref"]
            return "ok", [r for r in index.get(doc, []) if r.get("id") == rid][0]
        return status, record
    return "resolve_requirement", mutant


def _absent_modes_everywhere():
    index = copy.deepcopy(INDEX)
    for record in index[REQUIREMENTS_DOC]:
        record.pop("access_mode", None)
    return index


def _ambiguous_index():
    return {REQUIREMENTS_DOC: INDEX[REQUIREMENTS_DOC]
            + [{"id": "projection_sync_lane", "access_mode": "delegated_api"}]}


def _pair_without(mutate):
    doc = _conforming_pair()
    mutate(doc["credential_bindings"])
    return doc


MUTANTS = {
    "c1-consumer-declared": (
        _blind_condition("c1-consumer-declared"),
        "test_condition_1_a_pair_that_declares_nothing_is_refused",
        lambda: _pair_without(lambda b: [x.pop("consumer") for x in b.values()]), None),
    "c2-holders-differ": (
        _blind_condition("c2-holders-differ"),
        "test_condition_2_a_shared_holder_reference_is_refused",
        lambda: _pair_without(lambda b: b["projection_editor_surface"]["consumer"].update(
            holder_ref="example:service-subject:projection-sync-lane")), None),
    "c3-fetch-identities-differ": (
        _blind_condition("c3-fetch-identities-differ"),
        "test_condition_3_a_MISSING_fetch_identity_is_refused",
        # The lift's own arm on condition 3. The EQUAL-identity arm is carried by
        # the named `shared-authority-identity` fault, which replaces the default
        # finding for that pair and is anchored by its own tests above.
        lambda: _pair_without(lambda b: b["projection_editor_surface"]["consumer"].pop(
            "fetch_identity")), None),
    "c4-both-acknowledge": (
        _blind_condition("c4-both-acknowledge"),
        "test_condition_4_a_one_sided_acknowledgment_is_refused",
        lambda: _pair_without(lambda b: b["projection_editor_surface"]["consumer"].pop(
            "shared_credential_acknowledged")), None),
    "c5-requirement-resolves": (
        _blind_condition("c5-requirement-resolves"),
        "test_condition_5_a_dispatch_and_content_pair_is_refused_however_declared",
        # the SAME construction the named test drives: the map keys move with the
        # references, so condition SIX holds and only condition five stands
        _dispatch_and_content_pair, None),
    "c6-reference-names-its-key": (
        _blind_condition("c6-reference-names-its-key"),
        "test_condition_6_a_pair_pointing_at_a_requirement_neither_binding_is_is_refused",
        lambda: _pair_without(lambda b: [x["consumer"].update(
            requirement_ref=_ref("projection_sync_lane")) for x in b.values()]), None),
    "every-pair-arity": (
        _first_against_rest(),
        "test_three_bindings_with_the_second_and_third_sharing_an_authority_are_refused",
        _three_bindings, None),
    "unreadable-access-mode": (
        _fail_open_access_mode(),
        "test_two_ABSENT_access_modes_do_not_compare_equal_to_each_other",
        _conforming_pair, _absent_modes_everywhere()),
    "resolution-ambiguity": (
        _disambiguate_by_picking_one(),
        "test_the_ambiguity_is_never_resolved_by_picking_one",
        _conforming_pair, _ambiguous_index()),
}


def test_the_mutant_population_is_an_explicit_count():
    assert len(MUTANTS) == 9
    assert set(V.LIFT_CONDITIONS) <= set(MUTANTS)


@pytest.mark.parametrize("mutant", sorted(MUTANTS))
def test_the_named_test_PASSES_against_unmutated_code(mutant):
    """THE ANCHOR CHECK. Without it, a named test that fails on the mutant
    because its fixture or assertion target is absent is indistinguishable from
    one that fails because the mutation was caught — ANCHOR-MISSING, which is
    not the same state as SURVIVED."""
    (_attribute, _replacement), _named, build, index = MUTANTS[mutant]
    assert _findings(build(), index) != [], f"{mutant}: the anchor fixture refuses nothing"


@pytest.mark.parametrize("mutant", sorted(MUTANTS))
def test_each_mutant_DIES(mutant, monkeypatch):
    (attribute, replacement), named, build, index = MUTANTS[mutant]
    assert named in globals(), f"{mutant} names a test that does not exist: {named}"
    monkeypatch.setattr(V, attribute, replacement)
    assert _findings(build(), index) == [], (
        f"{mutant} SURVIVED — the condition it removes changes no outcome, so the check "
        f"named {named} is passing on something other than that condition")
