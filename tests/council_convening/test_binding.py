"""T050 — producer identity bound to verified workflow claims (feature 035,
Phase 5, PR-5).

Data-model E10 (the producer workflow binding and its fourteen-step order),
under Brett Heap's rulings of 2026-10-08:

* OPEN-2, "Consumer's runtime config (Recommended)": the concrete binding lives
  in the consumer's governed runtime configuration; this family ships the
  schema, a `.template.yaml` stub that is never accepted as live, the
  derivation from `repository-identity.yaml`, and the corpus.
* OPEN-3, "History + unchanged rule file (Recommended)", and its follow-ups:
  2, "job_workflow_ref's repo (Recommended)": the producer repository is the
  repository `job_workflow_ref` names, and a permitted workflow outside the
  governed repository is `workflow_revision_ungoverned`;
  3, "At or after the frozen rev (Recommended)": a seat job's `job_workflow_sha`
  on the governed history at or after the frozen revision is accepted, and one
  before it or off that history is `workflow_revision_ungoverned`.
* The closed `workflow_revision_rule`: `equals_governed_revision` for
  `commission`, `on_governed_history_since_revision` for `seat_execution`, and
  any other pairing `binding_malformed`.
* R7-M1: vectors adjudicate against the frozen identity fixture, never the live
  `contracts/policies/repository-identity.yaml`.

Brett Heap's 025 ruling (A), 2026-10-09, "Per-seat environments (Recommended)",
is consumer-side; this file CHECKS that E10 expresses it (one binding per seat,
a per-seat environment in the `sub`) and designs nothing for it.

The module under test is imported as `scripts.council_convening.binding`, never
under a bare name (see this package's `__init__.py`). The corpus and generator
modules are imported inside the tests that need them, so the binding cases run
on their own.
"""

from __future__ import annotations

import copy
import json
import shutil

import pytest
import yaml

import estate_inventory
from scripts.council_convening import binding
from scripts.council_convening.records import Refused

from .binding_fixtures import (
    AUDIENCE,
    BINDING_SCHEMA,
    BINDING_TEMPLATE,
    BINDING_VECTORS,
    CALLER,
    CALLER_ID,
    CALLER_OWNER_ID,
    COMMISSION_WORKFLOW,
    EARLIER_REVISION,
    ENTERPRISE_ISSUER,
    EVALUATION_EPOCH,
    EVALUATION_TIME,
    GOVERNED,
    GOVERNED_CASE_VARIANT,
    GOVERNED_FORMER,
    GOVERNED_FORMER_CASE_VARIANT,
    IDENTITY_FIXTURE,
    ISSUER,
    LATER_REVISION,
    LIVE_IDENTITY_MAP,
    OFF_HISTORY,
    PENDING_CURRENT,
    PENDING_FORMER,
    REPO_ROOT,
    REVISION,
    SEAT_WORKFLOW,
    SHARED_DEFINITIONS,
    claims_for,
    commission_binding,
    fixture_text,
    governed,
    identity,
    admission_binding,
    admission_workflow,
    identity_oracle,
    malformed_row_text,
    seat_binding,
    seat_environment,
    seat_history,
    seat_subject,
    with_passing_binding,
    write_identity_map,
)

PHASE_5_CODES = (
    "binding_malformed",
    "claims_unverified",
    "claims_expired",
    "issuer_mismatch",
    "audience_mismatch",
    "binding_wildcard",
    "repository_identity_unavailable",
    "repository_identity_former",
    "repository_identity_mismatch",
    "subject_template_mismatch",
    "subject_workflow_conflation",
    "workflow_not_permitted",
    "workflow_revision_ungoverned",
)


@pytest.fixture
def map_root(tmp_path):
    """A temporary root holding the frozen fixture's map text."""
    return write_identity_map(tmp_path / "map-root")


def refusal(callable_, *args, **kwargs) -> str:
    with pytest.raises(Refused) as caught:
        callable_(*args, **kwargs)
    return caught.value.code


def run(b: dict, root, *, operation: str = "commission", claims: dict | None = None,
        verified: bool = True, gov: dict | None = None, history: dict | None = None,
        evaluation_time: str = EVALUATION_TIME):
    """E10 steps 1 to 14 over `b`, with claims matching `b` unless given."""
    return binding.check_binding(
        b,
        operation=operation,
        identity=identity(claims_for(b) if claims is None else claims,
                          verified=verified),
        governed=governed() if gov is None else gov,
        governed_history=seat_history() if history is None else history,
        evaluation_time=evaluation_time,
        identity_root=root,
    )


def code_of(b: dict, root, **kwargs) -> str | None:
    try:
        run(b, root, **kwargs)
    except Refused as refused:
        return refused.code
    return None


def seat_run(b: dict, root, *, workflow_sha: str = LATER_REVISION, **kwargs):
    kwargs.setdefault("claims", claims_for(b, workflow_sha=workflow_sha))
    return code_of(b, root, operation="seat_execution", **kwargs)


# =========================================================================
# The E10 shape: the schema, its closed enumerations and the template stub.
# =========================================================================


@pytest.fixture(scope="module")
def schema_doc():
    return yaml.safe_load(BINDING_SCHEMA.read_text(encoding="utf-8"))


def test_the_schema_carries_the_house_header(schema_doc):
    assert schema_doc["schema_version"] == 1
    assert schema_doc["kind"] == "openxfactory-council-convening-contract-schema"
    assert schema_doc["name"] == "xfactory_council_producer_binding"
    assert schema_doc["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema_doc["$id"] == (
        "https://xforge.us/schemas/openxfactory/council-convening/v1/"
        "producer-binding.schema.yaml")
    assert schema_doc["contract_schema_version"] == 1
    for member in ("contract_id", "title", "description"):
        assert isinstance(schema_doc[member], str) and schema_doc[member]


def _objects(node):
    """Every object-typed subschema in `node`, at any depth."""
    if isinstance(node, dict):
        if node.get("type") == "object" or "properties" in node:
            yield node
        for value in node.values():
            yield from _objects(value)
    elif isinstance(node, list):
        for value in node:
            yield from _objects(value)


def test_every_object_in_the_schema_is_closed(schema_doc):
    objects = list(_objects(schema_doc))
    assert objects
    for node in objects:
        if "properties" in node and node.get("type") == "object":
            assert node.get("additionalProperties") is False, node


def test_the_record_members_are_exactly_e10s(schema_doc):
    assert set(schema_doc["properties"]) == {
        "schema_version", "kind", "protocol", "binding_id", "principal_kind",
        "issuer", "audience", "caller_repository", "repository_id",
        "subject_claim_keys", "subject_template", "permitted_workflows",
        "broker", "instantiation_stub"}
    assert set(schema_doc["required"]) == set(schema_doc["properties"]) - {
        "instantiation_stub"}


def _rule_pairs(schema_doc) -> set[tuple[str, str]]:
    entry = schema_doc["$defs"]["permitted_workflow"]
    pairs = set()
    for branch in entry["oneOf"]:
        props = branch["properties"]
        pairs.add((props["operation"]["const"],
                   props["workflow_revision_rule"]["const"]))
    return pairs


def test_the_workflow_revision_rule_is_the_ruled_closed_enumeration(schema_doc):
    # OPEN-3 and follow-up 3: two values, one per operation, and no other.
    assert _rule_pairs(schema_doc) == {
        ("commission", "equals_governed_revision"),
        ("seat_execution", "on_governed_history_since_revision"),
    }
    assert binding.WORKFLOW_REVISION_RULES == {
        "commission": "equals_governed_revision",
        "seat_execution": "on_governed_history_since_revision",
    }


@pytest.mark.parametrize("operation, rule", [
    ("commission", "on_governed_history_since_revision"),
    ("seat_execution", "equals_governed_revision"),
    ("commission", "at_or_after_governed_revision"),
    ("deploy", "equals_governed_revision"),
])
def test_any_other_pairing_is_binding_malformed(map_root, operation, rule):
    b = commission_binding()
    b["permitted_workflows"][0].update(operation=operation,
                                       workflow_revision_rule=rule)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "binding_malformed")


def test_a_commission_entry_paired_with_the_seat_rule_is_binding_malformed(map_root):
    # R4-H1: the seat rule is never a commission job's rule.
    b = commission_binding()
    b["permitted_workflows"][0]["workflow_revision_rule"] = (
        "on_governed_history_since_revision")
    assert code_of(b, map_root) == "binding_malformed"


def test_the_subject_claim_keys_are_the_closed_set_from_githubs_oidc_reference(
        schema_doc):
    keys = schema_doc["properties"]["subject_claim_keys"]
    enum = keys["items"]["enum"]
    assert tuple(enum) == binding.SUBJECT_CLAIM_KEYS
    assert len(set(enum)) == len(enum)
    # The two subject-customization keys, and the claims E10's own rules and
    # the per-seat subject read.
    for key in ("repo", "context", "environment", "job_workflow_ref",
                "repository", "repository_id", "repository_owner"):
        assert key in enum
    # No standard JWT claim is a subject element.
    for key in ("iss", "aud", "sub", "exp", "nbf", "iat", "jti"):
        assert key not in enum
    assert keys["uniqueItems"] is True and keys["minItems"] == 1
    assert "https://docs.github.com/" in keys["description"]


def test_a_live_binding_satisfies_the_schema():
    assert binding.schema_errors(commission_binding()) == []
    assert binding.schema_errors(seat_binding()) == []


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda b: b.update(extra=1), id="unknown member"),
    pytest.param(lambda b: b.pop("broker"), id="missing broker"),
    pytest.param(lambda b: b.update(principal_kind="governed_broker_job"),
                 id="broker principal kind"),
    pytest.param(lambda b: b.update(principal_kind="robot"),
                 id="unknown principal kind"),
    pytest.param(lambda b: b.update(protocol="xfactory-council-seat-return/v1"),
                 id="legacy protocol"),
    pytest.param(lambda b: b.update(binding_id="bad id"), id="binding id grammar"),
    pytest.param(lambda b: b.update(caller_repository="xFactory"),
                 id="caller repository grammar"),
    pytest.param(lambda b: b.update(repository_id=0), id="repository id zero"),
    pytest.param(lambda b: b.update(repository_id=True), id="repository id boolean"),
    pytest.param(lambda b: b.update(repository_id="424242"),
                 id="repository id string"),
    pytest.param(lambda b: b.update(audience=""), id="empty audience"),
    pytest.param(lambda b: b.update(audience="a" * 257), id="audience above 256"),
    pytest.param(lambda b: b.update(subject_claim_keys=[]), id="no claim keys"),
    pytest.param(lambda b: b.update(subject_claim_keys=["repo", "repo"]),
                 id="repeated claim key"),
    pytest.param(lambda b: b.update(subject_claim_keys=["repo", "sha_256"]),
                 id="unknown claim key"),
    pytest.param(lambda b: b.update(permitted_workflows=[]), id="no workflows"),
    pytest.param(lambda b: b.update(permitted_workflows=(
        b["permitted_workflows"] * 9)), id="nine workflows"),
    pytest.param(lambda b: b["permitted_workflows"][0].update(extra=1),
                 id="unknown workflow member"),
    pytest.param(lambda b: b["broker"].update(capability_verified="yes"),
                 id="broker flag not boolean"),
    pytest.param(lambda b: b["broker"].pop("evidence_ref"),
                 id="broker evidence missing"),
    pytest.param(lambda b: b.update(schema_version=2), id="schema version"),
])
def test_a_shape_defect_is_binding_malformed(map_root, mutate):
    b = commission_binding()
    mutate(b)
    assert binding.schema_errors(b)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "binding_malformed")


def test_a_non_mapping_binding_is_binding_malformed(map_root):
    assert refusal(binding.check_offline, ["not", "a", "binding"],
                   identity_root=map_root) == "binding_malformed"


@pytest.fixture(scope="module")
def template_doc():
    return yaml.safe_load(BINDING_TEMPLATE.read_text(encoding="utf-8"))


def test_the_template_is_a_stub_with_no_live_value(template_doc):
    assert template_doc["schema_version"] == 1
    assert template_doc["kind"] == "xfactory_council_producer_binding"
    assert template_doc["instantiation_stub"] is True
    # No live audience, subject template or repository id (T053).
    assert template_doc["repository_id"] is None
    for member in ("audience", "subject_template", "caller_repository",
                   "binding_id"):
        value = template_doc[member]
        assert value.startswith("<") and value.endswith(">"), member
    assert template_doc["broker"]["capability_verified"] is False
    assert template_doc["broker"]["evidence_ref"] is None
    assert [(e["operation"], e["workflow_revision_rule"])
            for e in template_doc["permitted_workflows"]] == [
        ("commission", "equals_governed_revision")]


def test_the_stub_vector_is_the_shipped_template(template_doc):
    path = BINDING_VECTORS / "bind-stub-presented-as-live-refuse.json"
    vector = json.loads(path.read_text(encoding="utf-8"))
    assert vector["inputs"]["binding"] == template_doc
    assert vector["expected"]["refusal"] == "binding_malformed"


def test_the_template_has_the_stub_shape_and_is_never_accepted_as_live(
        template_doc, map_root):
    assert binding.schema_errors(template_doc) == []
    assert refusal(binding.check_offline, template_doc,
                   identity_root=map_root) == "binding_malformed"


def test_a_live_binding_marked_as_a_stub_is_never_accepted(map_root):
    b = commission_binding(instantiation_stub=True)
    assert code_of(b, map_root) == "binding_malformed"


def test_the_stub_marker_is_const_true(map_root):
    b = commission_binding(instantiation_stub=False)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "binding_malformed")


def test_the_phase_5_codes_extend_the_closed_refusal_vocabulary():
    doc = yaml.safe_load(SHARED_DEFINITIONS.read_text(encoding="utf-8"))
    enum = doc["$defs"]["refusal_code"]["enum"]
    assert set(PHASE_5_CODES) <= set(enum)
    assert binding.PHASE_5_REFUSAL_CODES == PHASE_5_CODES
    # Introduced in Phase 4, where their first triggers are (R5-M2).
    assert "binding_unresolved" not in binding.PHASE_5_REFUSAL_CODES
    assert "broker_capability_insufficient" not in binding.PHASE_5_REFUSAL_CODES


# =========================================================================
# Positives, including the estate's calling pattern and the per-seat subject.
# =========================================================================


def test_the_estates_calling_pattern_is_accepted(map_root):
    # A caller repository running the governed repository's reusable workflow at
    # `governed.revision` (OPEN-3; follow-up 2; N2).
    assert CALLER != GOVERNED
    assert code_of(commission_binding(), map_root) is None


def test_the_check_returns_the_matched_permitted_workflow(map_root):
    entry = run(commission_binding(), map_root)
    assert entry == {
        "operation": "commission",
        "job_workflow_ref": COMMISSION_WORKFLOW,
        "workflow_revision_rule": "equals_governed_revision",
    }


def test_a_per_seat_environment_subject_is_accepted(map_root):
    # Brett Heap's 025 ruling (A), "Per-seat environments (Recommended)":
    # GitHub's `repo:<owner>/<repo>:environment:<name>` form.
    b = seat_binding("alpha")
    assert b["subject_template"] == (
        f"repo:{CALLER}:environment:{seat_environment('alpha')}")
    assert seat_run(b, map_root) is None


def test_one_binding_per_seat_is_expressible(map_root):
    # 025 ruling (A): one producer binding per seat, told apart by the seat's
    # environment in `sub`, with the binding id as `principal_ref`.
    alpha, beta = seat_binding("alpha"), seat_binding("beta")
    assert alpha["binding_id"] != beta["binding_id"]
    assert seat_run(alpha, map_root) is None
    assert seat_run(beta, map_root) is None
    # Each seat's token passes only its own seat's binding.
    beta_token = claims_for(beta, workflow_sha=LATER_REVISION)
    assert seat_run(alpha, map_root, claims=beta_token) == (
        "subject_template_mismatch")


def test_a_customized_template_carrying_the_environment_is_accepted(map_root):
    # GitHub's documented `repo`, `context`, `job_workflow_ref` customization,
    # with the per-seat environment as the context.
    b = seat_binding(
        subject_claim_keys=["repo", "context", "job_workflow_ref"],
        subject_template=(f"{seat_subject('alpha')}:job_workflow_ref:"
                          f"{SEAT_WORKFLOW}"))
    assert seat_run(b, map_root) is None


def test_a_template_customized_with_job_workflow_ref_and_repository_id_is_accepted(
        map_root):
    # I6: the strongest reusable-workflow binding is legal.
    b = seat_binding(
        subject_claim_keys=["repository_id", "environment", "job_workflow_ref"],
        subject_template=(f"repository_id:{CALLER_ID}:environment:"
                          f"{seat_environment('alpha')}:job_workflow_ref:"
                          f"{SEAT_WORKFLOW}"))
    assert seat_run(b, map_root) is None


def test_githubs_immutable_repo_segment_is_parsed(map_root):
    # GitHub's immutable subject format, `repo:OWNER@OWNER-ID/REPO@REPO-ID:...`,
    # used by repositories created, renamed or transferred after 2026-07-15.
    owner, name = CALLER.split("/")
    b = seat_binding(subject_template=(
        f"repo:{owner}@{CALLER_OWNER_ID}/{name}@{CALLER_ID}:environment:"
        f"{seat_environment('alpha')}"))
    assert seat_run(b, map_root) is None


def test_an_immutable_repo_segment_with_another_repository_id_is_refused(map_root):
    owner, name = CALLER.split("/")
    b = seat_binding(subject_template=(
        f"repo:{owner}@{CALLER_OWNER_ID}/{name}@{CALLER_ID + 1}:environment:"
        f"{seat_environment('alpha')}"))
    assert seat_run(b, map_root) == "subject_template_mismatch"


def test_an_unverified_broker_is_accepted_at_binding_and_recorded(map_root):
    # D4: it parks activation (E12, Phase 6); binding records it and refuses
    # nothing (R5-L10).
    b = commission_binding(broker={"broker_ref": "corpus-broker",
                                   "capability_verified": False,
                                   "evidence_ref": None})
    assert code_of(b, map_root) is None


@pytest.mark.parametrize("issuer", [ISSUER, ENTERPRISE_ISSUER])
def test_the_standard_and_the_enterprise_issuer_are_accepted(map_root, issuer):
    assert code_of(commission_binding(issuer=issuer), map_root) is None


# =========================================================================
# The offline half, steps 1 to 6.
# =========================================================================


@pytest.mark.parametrize("member, value", [
    ("audience", "*"),
    ("audience", "council-*"),
    ("subject_template", f"repo:{CALLER}:*"),
    ("subject_template", "*"),
    ("issuer", ISSUER + "/*"),
])
def test_a_wildcard_is_binding_wildcard(map_root, member, value):
    b = commission_binding(**{member: value})
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "binding_wildcard")


def test_a_wildcard_in_a_permitted_workflow_is_binding_wildcard(map_root):
    b = commission_binding()
    b["permitted_workflows"][0]["job_workflow_ref"] = (
        f"{GOVERNED}/.github/workflows/*.yml@refs/heads/main")
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "binding_wildcard")


@pytest.mark.parametrize("issuer", [
    "https://token.actions.githubusercontent.com/",
    "http://token.actions.githubusercontent.com",
    "https://token.actions.githubusercontent.com.evil.example",
    "https://token.actions.githubusercontent.com/octocat-inc/extra",
    "https://token.actions.githubusercontent.com/Octocat-Inc",
    "https://token.actions.githubusercontent.com/-octocat",
    "https://token.actions.githubusercontent.com/octocat-",
    "https://evil.example",
    "https://token.actions.githubusercontent.com\n",
    "",
])
def test_any_other_issuer_is_issuer_mismatch(map_root, issuer):
    b = commission_binding(issuer=issuer)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "issuer_mismatch")


# --- step 4: the identity map, read through `load_transfers` ---------------------


def test_an_absent_map_is_repository_identity_unavailable(tmp_path):
    # `load_transfers` alone returns an empty map for an absent file.
    root = tmp_path / "empty-root"
    root.mkdir()
    assert estate_inventory.load_transfers(root) == ({}, ())
    assert refusal(binding.check_offline, commission_binding(),
                   identity_root=root) == "repository_identity_unavailable"


def test_an_unreadable_map_is_repository_identity_unavailable(tmp_path):
    # `load_transfers` alone returns an empty map for undecodable bytes.
    root = tmp_path / "unreadable-root"
    path = root / LIVE_IDENTITY_MAP
    path.parent.mkdir(parents=True)
    path.write_bytes(b"\xff\xfe\x00not utf-8")
    assert estate_inventory.load_transfers(root) == ({}, ())
    assert refusal(binding.check_offline, commission_binding(),
                   identity_root=root) == "repository_identity_unavailable"


def test_a_map_with_a_malformed_row_is_repository_identity_unavailable(tmp_path):
    root = write_identity_map(tmp_path / "malformed-root", malformed_row_text())
    resolved, malformed = estate_inventory.load_transfers(root)
    assert malformed
    assert refusal(binding.check_offline, commission_binding(),
                   identity_root=root) == "repository_identity_unavailable"


@pytest.mark.parametrize("text", [
    pytest.param("schema_version: 1\nkind: repository_identity\ntransfers: [\n",
                 id="does not parse"),
    pytest.param("- just\n- a list\n", id="not a mapping"),
    pytest.param("schema_version: 1\nkind: repository_identity\n",
                 id="no transfers list"),
    pytest.param("schema_version: 1\nkind: something_else\ntransfers: []\n",
                 id="another kind"),
    pytest.param("schema_version: 1\nkind: repository_identity\n"
                 "transfers:\n  - just a string\n", id="a row that is no mapping"),
    pytest.param("", id="empty"),
])
def test_a_map_that_is_not_well_formed_is_repository_identity_unavailable(
        tmp_path, text):
    root = write_identity_map(tmp_path / "bad-root", text)
    assert refusal(binding.check_offline, commission_binding(),
                   identity_root=root) == "repository_identity_unavailable"


def test_a_well_formed_map_with_no_transfer_rows_is_valid(tmp_path):
    root = write_identity_map(
        tmp_path / "no-rows",
        "schema_version: 1\nkind: repository_identity\ntransfers: []\n")
    assert code_of(commission_binding(), root) is None


def test_the_former_spellings_come_from_load_transfers(map_root, monkeypatch):
    # No second transfer map: a spelling is former exactly when `load_transfers`
    # resolves it.
    calls = []
    real = estate_inventory.load_transfers

    def spy(root):
        calls.append(root)
        return {"opensoft/xFactory": "elsewhere/xFactory"}, ()

    monkeypatch.setattr(estate_inventory, "load_transfers", spy)
    assert refusal(binding.check_offline, commission_binding(),
                   identity_root=map_root) == "repository_identity_former"
    assert calls == [map_root]
    monkeypatch.setattr(estate_inventory, "load_transfers", real)
    binding.check_offline(commission_binding(), identity_root=map_root)


def test_the_identity_map_derivation(map_root):
    identity_map = binding.load_identity_map(map_root)
    assert identity_map.is_former(GOVERNED_FORMER)
    assert not identity_map.is_former(GOVERNED)
    # A non-canonical case variant of a listed spelling, either side.
    assert identity_map.is_former(GOVERNED_CASE_VARIANT)
    assert identity_map.is_former(GOVERNED_FORMER_CASE_VARIANT)
    assert identity_map.is_former("CODEXFACTORY/CODEXFACTORY")
    # A spelling the map does not list is current.
    assert not identity_map.is_former(CALLER)
    # The pending row's former is still the only address (pending_row_rule).
    assert not identity_map.is_former(PENDING_FORMER)
    assert not identity_map.is_former(PENDING_CURRENT)


@pytest.mark.parametrize("caller", [
    GOVERNED_FORMER, GOVERNED_CASE_VARIANT, GOVERNED_FORMER_CASE_VARIANT])
def test_a_former_or_case_variant_caller_is_repository_identity_former(
        map_root, caller):
    b = commission_binding(caller_repository=caller,
                           subject_template=f"repo:{caller}:ref:refs/heads/main")
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "repository_identity_former")


def test_an_unlisted_caller_is_taken_as_current(map_root):
    b = commission_binding(caller_repository=PENDING_FORMER,
                           subject_template=f"repo:{PENDING_FORMER}:ref:refs/heads/main")
    assert code_of(b, map_root) is None


@pytest.mark.parametrize("spelling", [GOVERNED_FORMER, GOVERNED_CASE_VARIANT])
def test_a_former_spelling_in_a_permitted_workflow_is_repository_identity_former(
        map_root, spelling):
    # R3-L9: the one transferred repository is the one in `job_workflow_ref`.
    b = commission_binding()
    b["permitted_workflows"][0]["job_workflow_ref"] = COMMISSION_WORKFLOW.replace(
        GOVERNED, spelling, 1)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "repository_identity_former")


# --- steps 5 and 6: the subject template ---------------------------------------


@pytest.mark.parametrize("template", [COMMISSION_WORKFLOW, SEAT_WORKFLOW])
def test_a_bare_workflow_reference_as_the_template_is_conflation(map_root, template):
    # R3-H1: it runs before the parse check, which would also refuse it.
    assert binding.is_bare_workflow_reference(template)
    assert binding.parse_subject(template, ["repo", "context"]) is None
    b = commission_binding(subject_template=template)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "subject_workflow_conflation")


def test_a_template_carrying_the_job_workflow_ref_key_is_no_conflation(map_root):
    template = f"job_workflow_ref:{COMMISSION_WORKFLOW}"
    assert not binding.is_bare_workflow_reference(template)


@pytest.mark.parametrize("keys, template", [
    pytest.param(["repo", "context"], f"repo:{CALLER}",
                 id="context missing"),
    pytest.param(["repo", "context"], f"repo:{CALLER}:environment",
                 id="environment without a name"),
    pytest.param(["repo", "context"], f"repo:{CALLER}:branch:main",
                 id="unknown context"),
    pytest.param(["repo", "context"], f"repo:{CALLER}:pull_request:extra",
                 id="trailing element"),
    pytest.param(["repo", "context"], "repo::ref:refs/heads/main",
                 id="empty repository"),
    pytest.param(["repo", "context"], "repo:xFactory:ref:refs/heads/main",
                 id="repository without owner"),
    pytest.param(["context", "repo"], f"repo:{CALLER}:ref:refs/heads/main",
                 id="keys in another order"),
    pytest.param(["repo", "context", "job_workflow_ref"],
                 f"repo:{CALLER}:ref:refs/heads/main", id="a key with no element"),
    pytest.param(["repository_id", "context"],
                 "repository_id:42x:ref:refs/heads/main", id="repository id not decimal"),
    pytest.param(["repo", "context"], f"repo:{CALLER}:ref:refs/heads/main\n",
                 id="trailing newline"),
    pytest.param(["repo", "context"], f"repo:{CALLER}:environment:a\u0007b",
                 id="control character"),
    pytest.param(["job_workflow_ref"], f"job_workflow_ref:{COMMISSION_WORKFLOW}",
                 id="no repository element"),
])
def test_a_template_that_does_not_parse_is_subject_template_mismatch(
        map_root, keys, template):
    b = commission_binding(subject_claim_keys=keys, subject_template=template)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "subject_template_mismatch")


@pytest.mark.parametrize("keys, template", [
    pytest.param(["repo", "context"], "repo:opensoft/otherRepo:ref:refs/heads/main",
                 id="repo names another repository"),
    pytest.param(["repository", "context"],
                 "repository:opensoft/otherRepo:ref:refs/heads/main",
                 id="repository names another repository"),
    pytest.param(["repository_id", "context"],
                 f"repository_id:{CALLER_ID + 1}:ref:refs/heads/main",
                 id="repository id names another repository"),
    pytest.param(["repo", "context"], "repo:opensoft/xfactory:ref:refs/heads/main",
                 id="repo spelled in another case"),
])
def test_a_template_naming_another_repository_is_subject_template_mismatch(
        map_root, keys, template):
    b = commission_binding(subject_claim_keys=keys, subject_template=template)
    assert refusal(binding.check_offline, b, identity_root=map_root) == (
        "subject_template_mismatch")


@pytest.mark.parametrize("keys, template, elements", [
    (["repo", "context"], f"repo:{CALLER}:ref:refs/heads/main",
     (("repo", CALLER), ("context", "ref:refs/heads/main"))),
    (["repo", "context"], f"repo:{CALLER}:pull_request",
     (("repo", CALLER), ("context", "pull_request"))),
    (["repo", "context"], f"repo:{CALLER}:environment:Production%3AV1",
     (("repo", CALLER), ("context", "environment:Production%3AV1"))),
    (["repository_owner", "repository_visibility", "repo"],
     f"repository_owner:opensoft:repository_visibility:private:repo:{CALLER}",
     (("repository_owner", "opensoft"), ("repository_visibility", "private"),
      ("repo", CALLER))),
])
def test_the_subject_grammar_parses_githubs_documented_forms(keys, template, elements):
    # A `:` inside a value is written `%3A` in GitHub's `sub`, so `:` separates.
    assert binding.parse_subject(template, keys) == elements


# =========================================================================
# The claim half, steps 7 to 14.
# =========================================================================


def test_decoded_only_claims_are_claims_unverified(map_root):
    assert code_of(commission_binding(), map_root, verified=False) == (
        "claims_unverified")


@pytest.mark.parametrize("overrides", [
    pytest.param({"exp": EVALUATION_EPOCH}, id="exp at the instant"),
    pytest.param({"exp": EVALUATION_EPOCH - 1}, id="exp before the instant"),
    pytest.param({"nbf": EVALUATION_EPOCH + 1}, id="nbf after the instant"),
    pytest.param({"exp": None}, id="exp absent"),
    pytest.param({"exp": "1791504300"}, id="exp not an integer"),
    pytest.param({"exp": True}, id="exp a boolean"),
    pytest.param({"nbf": "1791503940"}, id="nbf not an integer"),
])
def test_a_token_outside_its_validity_window_is_claims_expired(map_root, overrides):
    b = commission_binding()
    claims = claims_for(b)
    for key, value in overrides.items():
        if value is None:
            del claims[key]
        else:
            claims[key] = value
    assert code_of(b, map_root, claims=claims) == "claims_expired"


def test_nbf_at_the_instant_is_inside_the_window(map_root):
    b = commission_binding()
    assert code_of(b, map_root, claims=claims_for(b, nbf=EVALUATION_EPOCH)) is None


def test_an_absent_nbf_sets_no_lower_bound(map_root):
    b = commission_binding()
    claims = claims_for(b)
    del claims["nbf"]
    assert code_of(b, map_root, claims=claims) is None


@pytest.mark.parametrize("claim, value, code", [
    ("iss", ENTERPRISE_ISSUER, "issuer_mismatch"),
    ("iss", None, "issuer_mismatch"),
    ("aud", AUDIENCE + "-other", "audience_mismatch"),
    ("aud", [AUDIENCE], "audience_mismatch"),
    ("aud", None, "audience_mismatch"),
    ("sub", f"repo:{CALLER}:ref:refs/heads/other", "subject_template_mismatch"),
    ("sub", None, "subject_template_mismatch"),
    ("repository", "opensoft/otherRepo", "repository_identity_mismatch"),
    ("repository", "opensoft/xfactory", "repository_identity_mismatch"),
    ("repository", None, "repository_identity_mismatch"),
    ("repository_id", str(CALLER_ID + 1), "repository_identity_mismatch"),
    ("repository_id", CALLER_ID, "repository_identity_mismatch"),
    ("repository_id", None, "repository_identity_mismatch"),
])
def test_a_verified_claim_that_differs_from_the_binding_is_refused(
        map_root, claim, value, code):
    # R3-H2: D3's "the consumer verifies signed issuer/audience/expiry".
    b = commission_binding()
    claims = claims_for(b)
    if value is None:
        del claims[claim]
    else:
        claims[claim] = value
    assert code_of(b, map_root, claims=claims) == code


def test_an_unlisted_workflow_is_workflow_not_permitted(map_root):
    b = commission_binding()
    other = f"{GOVERNED}/.github/workflows/corpus-other.yml@refs/heads/main"
    assert code_of(b, map_root, claims=claims_for(b, job_workflow_ref=other)) == (
        "workflow_not_permitted")


def test_a_sub_naming_a_permitted_workflow_does_not_permit_it(map_root):
    # N15: permitted workflows are matched against the verified
    # `job_workflow_ref`, never against `sub`.
    b = commission_binding(
        subject_claim_keys=["repo", "context", "job_workflow_ref"],
        subject_template=(f"repo:{CALLER}:ref:refs/heads/main:job_workflow_ref:"
                          f"{COMMISSION_WORKFLOW}"))
    other = f"{GOVERNED}/.github/workflows/corpus-other.yml@refs/heads/main"
    claims = claims_for(b, job_workflow_ref=other)
    assert COMMISSION_WORKFLOW in claims["sub"]
    assert code_of(b, map_root, claims=claims) == "workflow_not_permitted"


def test_a_workflow_permitted_for_the_other_operation_is_not_permitted(map_root):
    b = commission_binding()
    claims = claims_for(b, workflow_sha=LATER_REVISION)
    assert code_of(b, map_root, operation="seat_execution", claims=claims) == (
        "workflow_not_permitted")


def test_an_absent_job_workflow_ref_is_workflow_not_permitted(map_root):
    b = commission_binding()
    claims = claims_for(b)
    del claims["job_workflow_ref"]
    assert code_of(b, map_root, claims=claims) == "workflow_not_permitted"


# --- step 14: the commission rule (OPEN-3; follow-up 2) -------------------------


def test_an_unequal_commission_workflow_sha_is_workflow_revision_ungoverned(map_root):
    b = commission_binding()
    for sha in (LATER_REVISION, EARLIER_REVISION, OFF_HISTORY):
        assert code_of(b, map_root, claims=claims_for(b, workflow_sha=sha)) == (
            "workflow_revision_ungoverned"), sha


def test_a_permitted_workflow_outside_the_governed_repository_is_ungoverned(
        map_root):
    # Follow-up 2, "job_workflow_ref's repo (Recommended)": the producer
    # repository is `job_workflow_ref`'s, and a permitted workflow outside the
    # governed repository fails closed, even at the governed revision.
    outside = f"{CALLER}/.github/workflows/corpus-commission.yml@refs/heads/main"
    b = commission_binding()
    b["permitted_workflows"][0]["job_workflow_ref"] = outside
    assert code_of(b, map_root, claims=claims_for(b)) == (
        "workflow_revision_ungoverned")


def test_the_commission_rule_reads_the_records_governed_member(map_root):
    b = commission_binding()
    claims = claims_for(b, workflow_sha=LATER_REVISION)
    assert code_of(b, map_root, claims=claims,
                   gov=governed(revision=LATER_REVISION)) is None


@pytest.mark.parametrize("sha", ["4" * 39, "4" * 40 + "\n", "A" * 40, None])
def test_a_job_workflow_sha_that_is_no_full_commit_is_ungoverned(map_root, sha):
    b = commission_binding()
    claims = claims_for(b)
    if sha is None:
        del claims["job_workflow_sha"]
    else:
        claims["job_workflow_sha"] = sha
    assert code_of(b, map_root, claims=claims) == "workflow_revision_ungoverned"


# --- step 14: the seat rule (follow-up 3) --------------------------------------


@pytest.mark.parametrize("sha", [REVISION, LATER_REVISION])
def test_a_seat_sha_at_or_after_the_frozen_revision_is_accepted(map_root, sha):
    assert seat_run(seat_binding(), map_root, workflow_sha=sha) is None


@pytest.mark.parametrize("sha", [EARLIER_REVISION, OFF_HISTORY, "8" * 40])
def test_a_seat_sha_before_the_frozen_revision_or_off_history_is_ungoverned(
        map_root, sha):
    # "8" * 40 is a commit the governed history does not know at all.
    assert seat_run(seat_binding(), map_root, workflow_sha=sha) == (
        "workflow_revision_ungoverned")


def test_a_seat_workflow_outside_the_frozen_governed_repository_is_ungoverned(
        map_root):
    outside = f"{CALLER}/.github/workflows/corpus-seat.yml@refs/heads/main"
    b = seat_binding()
    b["permitted_workflows"][0]["job_workflow_ref"] = outside
    history = seat_history(repository=CALLER)
    assert seat_run(b, map_root, history=history) == "workflow_revision_ungoverned"


def test_the_seat_rule_never_reads_equality(map_root):
    # A later revision is accepted for a seat and refused for a commission job.
    seat, commission = seat_binding(), commission_binding()
    assert seat_run(seat, map_root, workflow_sha=LATER_REVISION) is None
    assert code_of(commission, map_root,
                   claims=claims_for(commission, workflow_sha=LATER_REVISION)) == (
        "workflow_revision_ungoverned")


# =========================================================================
# The E10 order: each adjacent pair of steps pinned by a two-defect binding.
# =========================================================================


def _stub(b):
    b["instantiation_stub"] = True


def _wildcard(b):
    b["audience"] = "*"


def _issuer(b):
    b["issuer"] = "https://evil.example"


def _former(b):
    b["caller_repository"] = GOVERNED_FORMER


def _conflation(b):
    b["subject_template"] = COMMISSION_WORKFLOW


def _unparseable(b):
    b["subject_template"] = f"repo:{CALLER}"


# Step 5 before step 6 needs no pair: a bare workflow reference is itself a
# template that does not parse (R3-H1), which
# `test_a_bare_workflow_reference_as_the_template_is_conflation` pins.
@pytest.mark.parametrize("first, second, code", [
    (_stub, _wildcard, "binding_malformed"),
    (_wildcard, _issuer, "binding_wildcard"),
    (_issuer, _former, "issuer_mismatch"),
    (_former, _conflation, "repository_identity_former"),
])
def test_the_offline_order(map_root, first, second, code):
    b = commission_binding()
    second(b)
    first(b)
    assert refusal(binding.check_offline, b, identity_root=map_root) == code


def test_an_unavailable_map_precedes_a_former_spelling(tmp_path):
    root = tmp_path / "no-map"
    root.mkdir()
    b = commission_binding()
    _former(b)
    assert refusal(binding.check_offline, b, identity_root=root) == (
        "repository_identity_unavailable")


def test_the_offline_half_precedes_the_claims(map_root):
    # Step 6 before step 7: an unparseable template and decoded-only claims.
    b = commission_binding()
    _unparseable(b)
    assert code_of(b, map_root, verified=False) == "subject_template_mismatch"


def _claims_case(**overrides):
    b = commission_binding()
    claims = claims_for(b, **{k: v for k, v in overrides.items()
                              if k in ("workflow_sha", "job_workflow_ref")})
    claims.update({k: v for k, v in overrides.items()
                   if k not in ("workflow_sha", "job_workflow_ref")})
    return b, claims


OTHER_WORKFLOW = f"{GOVERNED}/.github/workflows/corpus-other.yml@refs/heads/main"


@pytest.mark.parametrize("overrides, verified, code", [
    ({"exp": EVALUATION_EPOCH - 1}, False, "claims_unverified"),
    ({"exp": EVALUATION_EPOCH - 1, "iss": ENTERPRISE_ISSUER}, True,
     "claims_expired"),
    ({"iss": ENTERPRISE_ISSUER, "aud": "other"}, True, "issuer_mismatch"),
    ({"aud": "other", "sub": f"repo:{CALLER}:pull_request"}, True,
     "audience_mismatch"),
    ({"sub": f"repo:{CALLER}:pull_request", "repository": "opensoft/otherRepo"},
     True, "subject_template_mismatch"),
    ({"repository": "opensoft/otherRepo", "job_workflow_ref": OTHER_WORKFLOW},
     True, "repository_identity_mismatch"),
    ({"job_workflow_ref": OTHER_WORKFLOW, "workflow_sha": LATER_REVISION}, True,
     "workflow_not_permitted"),
])
def test_the_claim_order(map_root, overrides, verified, code):
    b, claims = _claims_case(**overrides)
    assert code_of(b, map_root, claims=claims, verified=verified) == code


# =========================================================================
# The two halves as separate entry points (E2 steps A1 and A4).
# =========================================================================


def test_steps_1_to_13_do_not_read_the_governed_member(map_root):
    # A1 runs before E2 step 5 has checked `governed`, so it must not read it.
    b = commission_binding()
    binding.check_offline(b, identity_root=map_root)
    entry = binding.check_claims(
        b, operation="commission", identity=identity(claims_for(b)),
        evaluation_time=EVALUATION_TIME)
    assert entry["job_workflow_ref"] == COMMISSION_WORKFLOW


def test_step_14_alone_applies_the_matched_rule(map_root):
    b = commission_binding()
    claims = claims_for(b, workflow_sha=LATER_REVISION)
    entry = b["permitted_workflows"][0]
    assert refusal(binding.check_workflow_revision, entry,
                   identity=identity(claims), governed=governed(),
                   governed_history=None) == "workflow_revision_ungoverned"
    binding.check_workflow_revision(
        entry, identity=identity(claims_for(b)), governed=governed(),
        governed_history=None)


def test_the_offline_and_claim_rules_are_named_for_check():
    # `check` runs steps 1 to 6 and reports each claim rule as not offline
    # checkable (contracts/validator-cli.md).
    assert binding.OFFLINE_STEPS == (
        "binding_malformed", "binding_wildcard", "issuer_mismatch",
        "repository_identity_unavailable", "repository_identity_former",
        "subject_workflow_conflation", "subject_template_mismatch")
    assert binding.CLAIM_RULES == (
        "claims_unverified", "claims_expired", "issuer_mismatch",
        "audience_mismatch", "subject_template_mismatch",
        "repository_identity_mismatch", "workflow_not_permitted",
        "workflow_revision_ungoverned")


def test_a_refusal_never_echoes_a_value(map_root):
    secret_looking = "council-" + "x" * 40
    b = commission_binding(audience=secret_looking)
    with pytest.raises(Refused) as caught:
        run(b, map_root, claims=claims_for(commission_binding()))
    assert caught.value.code == "audience_mismatch"
    assert secret_looking not in str(caught.value)


# =========================================================================
# The `repository_identity` oracle and the frozen identity fixture (R7-M1).
# =========================================================================


@pytest.mark.parametrize("state", ["absent", "unreadable"])
def test_the_oracle_states_materialize_under_a_temporary_root(tmp_path, state):
    root = binding.materialize_identity(identity_oracle(state), tmp_path / "r")
    assert refusal(binding.load_identity_map, root) == (
        "repository_identity_unavailable")
    path = root / LIVE_IDENTITY_MAP
    assert path.exists() is (state == "unreadable")


def test_the_text_state_materializes_the_exact_text(tmp_path):
    root = binding.materialize_identity(identity_oracle("text"), tmp_path / "r")
    assert (root / LIVE_IDENTITY_MAP).read_text(encoding="utf-8") == fixture_text()
    assert binding.load_identity_map(root).is_former(GOVERNED_FORMER)


@pytest.mark.parametrize("oracle", [
    {}, {"state": "text"}, {"state": "text", "text": 7}, {"state": "gone"},
    {"state": "absent", "text": "x"}, None])
def test_a_malformed_oracle_is_a_harness_error(tmp_path, oracle):
    with pytest.raises(ValueError):
        binding.materialize_identity(oracle, tmp_path / "r")


def test_the_fixture_is_corpus_owned_and_carries_one_complete_and_one_pending_row():
    doc = json.loads(IDENTITY_FIXTURE.read_text(encoding="utf-8"))
    assert set(doc) == {"schema_version", "kind", "name", "text"}
    assert doc["schema_version"] == 1
    assert doc["kind"] == "openxfactory-council-convening-conformance-fixture"
    assert doc["name"] == "repository-identity"
    rows = yaml.safe_load(doc["text"])["transfers"]
    assert [row["transfer_state"] for row in rows] == ["complete", "pending"]
    assert (rows[0]["former"], rows[0]["current"]) == (GOVERNED_FORMER, GOVERNED)


def test_the_fixtures_complete_row_is_codexfactorys_row_in_the_live_map():
    # As the live map records it when the fixture is authored. A later edit of
    # the live map moves nothing here (R7-M1); this pins the authoring only.
    live = yaml.safe_load((REPO_ROOT / LIVE_IDENTITY_MAP).read_text(encoding="utf-8"))
    pairs = {(row["former"], row["current"]) for row in live["transfers"]}
    assert (GOVERNED_FORMER, GOVERNED) in pairs


def test_the_fixture_is_in_the_deterministic_json_form():
    raw = IDENTITY_FIXTURE.read_bytes()
    doc = json.loads(raw)
    assert raw == (json.dumps(doc, sort_keys=True, indent=2, ensure_ascii=True)
                   + "\n").encode("ascii")


# =========================================================================
# The `binding` vectors (T051), adjudicated through the module.
# =========================================================================


def _binding_vectors():
    return [(path, json.loads(path.read_text(encoding="utf-8")))
            for path in sorted(BINDING_VECTORS.glob("*.json"))]


def test_the_binding_area_exists_with_vectors():
    assert len(_binding_vectors()) >= 40


def test_every_binding_vector_is_well_formed():
    for path, vector in _binding_vectors():
        assert vector["case_id"] == path.stem
        assert vector["area"] == "binding" and vector["boundary"] == "binding"
        # Consumer-side: a binding vector carries a verified commission or seat
        # token, which only the consumer verifies (R4-M2).
        assert vector["applies_to"] == ["consumer"], path.name
        assert "FR-009" in vector["requirement_ids"]
        assert vector["evaluation_time"] == EVALUATION_TIME
        assert set(vector["inputs"]) <= {"binding", "operation", "governed"}
        assert vector["inputs"]["operation"] in ("commission", "seat_execution")
        assert "repository_identity" in vector["environment"], path.name
        assert vector["expected"]["outcome"] in ("accept", "refuse")
        assert vector["expected"]["findings"] == []
        assert vector["expected"]["derived_origin"] == "hand"
        raw = path.read_bytes()
        assert raw == (json.dumps(vector, sort_keys=True, indent=2,
                                  ensure_ascii=True) + "\n").encode("ascii")


def test_every_map_reading_vector_carries_the_fixtures_text():
    # Except the malformed-row probe of `repository_identity_unavailable`.
    text = fixture_text()
    for path, vector in _binding_vectors():
        oracle = vector["environment"]["repository_identity"]
        if oracle["state"] == "text" and (
                vector["expected"]["refusal"] != "repository_identity_unavailable"):
            assert oracle["text"] == text, path.name


def test_the_three_unavailable_probes_exist():
    states = {
        (v["environment"]["repository_identity"]["state"],
         v["environment"]["repository_identity"].get("text") == malformed_row_text())
        for _, v in _binding_vectors()
        if v["expected"]["refusal"] == "repository_identity_unavailable"}
    assert states == {("absent", False), ("text", True), ("unreadable", False)}


def test_every_phase_5_code_is_probed_by_a_binding_vector():
    probed = {v["expected"]["refusal"] for _, v in _binding_vectors()}
    assert set(PHASE_5_CODES) <= probed
    assert probed - {None} <= set(PHASE_5_CODES)


def test_the_per_seat_environment_subject_is_an_accepted_vector():
    accepted = [v for _, v in _binding_vectors()
                if v["expected"]["outcome"] == "accept"
                and v["inputs"]["operation"] == "seat_execution"]
    assert any(":environment:" in v["inputs"]["binding"]["subject_template"]
               for v in accepted)


@pytest.mark.parametrize("path", sorted(BINDING_VECTORS.glob("*.json")),
                         ids=lambda p: p.stem)
def test_each_binding_vector_adjudicates(path):
    vector = json.loads(path.read_text(encoding="utf-8"))
    outcome, code = binding.evaluate_vector(vector)
    assert (outcome, code) == (vector["expected"]["outcome"],
                               vector["expected"]["refusal"])


def test_a_vector_is_adjudicated_against_the_map_it_carries(monkeypatch, tmp_path):
    # R7-M1: the live map is never read. Point the repository root's map at a
    # text that would make the former spelling current, and nothing moves.
    vectors = [v for _, v in _binding_vectors()
               if v["expected"]["refusal"] == "repository_identity_former"]
    assert vectors
    real = estate_inventory.load_transfers
    seen = []

    def spy(root):
        seen.append(root.resolve())
        return real(root)

    monkeypatch.setattr(estate_inventory, "load_transfers", spy)
    for vector in vectors:
        assert binding.evaluate_vector(vector) == (
            "refuse", "repository_identity_former")
    assert seen and REPO_ROOT.resolve() not in seen


# =========================================================================
# The corpus index rules this phase adds (T055), failing first (R7-L1).
# =========================================================================


def test_a_binding_vector_without_the_identity_oracle_is_refused(family_tree):
    from scripts.council_convening import corpus, generate

    conformance = family_tree / "contracts" / "council-convening" / "conformance"
    path = sorted((conformance / "vectors" / "binding").glob("*.json"))[0]
    vector = json.loads(path.read_text(encoding="utf-8"))
    del vector["environment"]["repository_identity"]
    path.write_bytes(corpus.dump_json(vector))
    generate.generate(family_tree)
    codes = [f.code for f in corpus.check_corpus(family_tree).findings]
    assert "council-convening-vector-identity-map-missing" in codes


def test_the_identity_map_rule_covers_every_boundary_that_reads_the_map():
    # conformance-corpus § Environment oracles: `binding`, `registration`, and
    # `admission` from Phase 5, where binding runs as E2 steps A1 and A4.
    from scripts.council_convening import corpus

    assert set(corpus.IDENTITY_MAP_BOUNDARIES) == {"binding", "registration", "admission"}


def test_an_admission_vector_without_the_identity_oracle_is_refused(family_tree):
    from scripts.council_convening import corpus, generate

    conformance = family_tree / "contracts" / "council-convening" / "conformance"
    path = conformance / "vectors" / "resolution" / f"{ADMISSION_BASE}.json"
    vector = json.loads(path.read_text(encoding="utf-8"))
    del vector["environment"]["repository_identity"]
    path.write_bytes(corpus.dump_json(vector))
    generate.generate(family_tree)
    codes = [f.code for f in corpus.check_corpus(family_tree).findings]
    assert "council-convening-vector-identity-map-missing" in codes


def test_the_fixture_is_an_index_fixtures_row_with_a_matching_digest():
    import hashlib

    index = json.loads((IDENTITY_FIXTURE.parents[1] / "index.json").read_text(
        encoding="utf-8"))
    assert index["fixtures"] == [{
        "name": "repository-identity",
        "path": "fixtures/repository-identity.json",
        "sha256": "sha256:" + hashlib.sha256(IDENTITY_FIXTURE.read_bytes()).hexdigest(),
    }]


def test_an_unindexed_fixture_is_an_index_closure_finding(family_tree):
    from scripts.council_convening import corpus

    fixtures = family_tree / "contracts" / "council-convening" / "conformance" / "fixtures"
    shutil.copy2(fixtures / "repository-identity.json", fixtures / "zz-extra.json")
    codes = [f.code for f in corpus.check_corpus(family_tree).findings]
    assert "council-convening-index-closure" in codes


def test_a_moved_fixture_byte_is_an_index_digest_finding(family_tree):
    from scripts.council_convening import corpus

    path = (family_tree / "contracts" / "council-convening" / "conformance"
            / "fixtures" / "repository-identity.json")
    path.write_bytes(path.read_bytes().replace(b"pending", b"pendinG", 1))
    codes = [f.code for f in corpus.check_corpus(family_tree).findings]
    assert "council-convening-index-digest" in codes


def test_a_vector_text_that_drifts_from_the_fixture_is_generator_drift(family_tree):
    from scripts.council_convening import corpus, generate

    conformance = family_tree / "contracts" / "council-convening" / "conformance"
    path = conformance / "vectors" / "binding" / "bind-commission-accept.json"
    vector = json.loads(path.read_text(encoding="utf-8"))
    vector["environment"]["repository_identity"]["text"] += "# drift\n"
    path.write_bytes(corpus.dump_json(vector))
    drift = generate.check(family_tree)
    assert any("bind-commission-accept" in line for line in drift)


@pytest.mark.parametrize("live_map", ["removed", "edited"])
def test_generate_check_never_reads_the_live_map(family_tree, live_map):
    # R7-M1: the generator reads the identity fixture, never
    # `contracts/policies/repository-identity.yaml`. In a temporary copy of the
    # tree the live map is removed, or edited so that the former spelling
    # would be current, and `generate --check` still passes unchanged.
    from scripts.council_convening import corpus, generate

    target = family_tree / LIVE_IDENTITY_MAP
    if live_map == "edited":
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            "schema_version: 1\nkind: repository_identity\ntransfers: []\n",
            encoding="utf-8")
    else:
        assert not target.exists()
    assert generate.check(family_tree) == []
    assert [f.code for f in corpus.check_corpus(family_tree).findings] == []


# =========================================================================
# The binding inside admission: E10 steps 1 to 13 as E2 step A1, after shape,
# and step 14 as E2 step A4, after step 5 has checked `governed` (T055; T051;
# R3-M4; R4-M1; R4-H2). Failing first.
# =========================================================================

RESOLUTION_VECTORS = BINDING_VECTORS.parent / "resolution"
ADMISSION_BASE = "admission-accept-conditional-seat-not-held"

#: Phase 2's twelve admission vectors, re-authored to carry a passing binding.
#: Their outcomes do not move.
PHASE_2_ADMISSION = {
    "admission-accept-conditional-seat-not-held": None,
    "admission-accept-unrelated-file-changed-at-tip": None,
    "admission-refuse-candidate-not-resolved": "candidate_mismatch",
    "admission-refuse-head-moved-after-submission": "candidate_head_moved",
    "admission-refuse-head-unavailable": "candidate_head_unavailable",
    "admission-refuse-order-digest-before-superseded": "rule_digest_mismatch",
    "admission-refuse-order-superseded-before-council": "rule_superseded",
    "admission-refuse-order-superseded-source-before-later-source": "rule_superseded",
    "admission-refuse-rule-superseded-council-profile": "rule_superseded",
    "admission-refuse-rule-superseded-listing": "rule_superseded",
    "admission-refuse-rule-superseded-rule-file": "rule_superseded",
    "admission-refuse-rule-superseded-source-deleted-at-tip": "rule_superseded",
}

#: The admission vectors this phase adds: the binding's own refusals at
#: admission, and the interleaved order.
PHASE_5_ADMISSION = {
    "admission-refuse-binding-claims-unverified": "claims_unverified",
    "admission-refuse-binding-identity-map-absent": "repository_identity_unavailable",
    "admission-refuse-binding-seat-token-for-commission": "workflow_not_permitted",
    "admission-refuse-binding-stub-presented-as-live": "binding_malformed",
    "admission-refuse-workflow-revision-not-the-governed-revision":
        "workflow_revision_ungoverned",
    "admission-refuse-workflow-outside-the-governed-repository":
        "workflow_revision_ungoverned",
    # A1 runs after shape (step 2), and before secrets and the candidate.
    "admission-refuse-order-shape-before-binding": "convening_malformed",
    "admission-refuse-order-binding-before-secret": "audience_mismatch",
    "admission-refuse-order-binding-before-candidate": "claims_expired",
    # A4 runs after every step-5 check, and before step 6.
    "admission-refuse-order-candidate-before-workflow-revision": "candidate_mismatch",
    "admission-refuse-order-mutable-revision-before-workflow-revision":
        "mutable_rule_reference",
    "admission-refuse-order-former-governed-spelling-before-workflow-revision":
        "rule_unauthorized",
    "admission-refuse-order-superseded-before-workflow-revision": "rule_superseded",
    "admission-refuse-order-workflow-revision-before-council":
        "workflow_revision_ungoverned",
}


def _raw(case_id):
    return json.loads((RESOLUTION_VECTORS / f"{case_id}.json").read_text(encoding="utf-8"))


def _joined(vector):
    from scripts.council_convening import corpus

    vector = copy.deepcopy(vector)
    vector["inputs"] = corpus.join_parts(vector["inputs"])
    vector["environment"] = corpus.join_parts(vector.get("environment", {}))
    return vector


def _admission(case_id=ADMISSION_BASE):
    return _joined(_raw(case_id))


def _adjudicate(vector):
    from scripts.council_convening import resolution

    got = resolution.adjudicate(vector)
    return got["outcome"], got["refusal"]


def _all_admission_vectors(role="record"):
    """Every admission vector in one input role: `record`, the commission record
    in the E2 order, where A1 and A4 run; or `snapshot`, the E4 half, which
    judges no binding."""
    out = []
    for path in sorted(BINDING_VECTORS.parent.glob("*/*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw["boundary"] == "admission" and role in raw["inputs"]:
            out.append((raw["case_id"], raw))
    return out


def test_every_admission_vector_carries_a_binding_and_the_commission_operation():
    vectors = _all_admission_vectors()
    assert len(vectors) >= len(PHASE_2_ADMISSION) + len(PHASE_5_ADMISSION)
    for case_id, raw in vectors:
        assert "binding" in raw["inputs"], case_id
        assert raw["inputs"]["operation"] == "commission", case_id
        assert "identity" in raw["environment"], case_id
        if raw["expected"]["refusal"] != "repository_identity_unavailable":
            assert raw["environment"]["repository_identity"] == identity_oracle(), case_id


@pytest.mark.parametrize("case_id", sorted(PHASE_2_ADMISSION))
def test_the_re_authored_phase_2_admission_vectors_keep_their_outcomes(case_id):
    raw = _raw(case_id)
    code = PHASE_2_ADMISSION[case_id]
    expected = ("accept", None) if code is None else ("refuse", code)
    assert (raw["expected"]["outcome"], raw["expected"]["refusal"]) == expected
    assert _adjudicate(_joined(raw)) == expected


@pytest.mark.parametrize("case_id", sorted(PHASE_5_ADMISSION))
def test_each_phase_5_admission_vector_pins_its_code(case_id):
    raw = _raw(case_id)
    assert raw["boundary"] == "admission" and raw["applies_to"] == ["consumer"]
    assert raw["area"] == "resolution"
    assert "FR-009" in raw["requirement_ids"]
    assert raw["expected"]["derived_origin"] == "hand"
    assert (raw["expected"]["outcome"], raw["expected"]["refusal"]) == (
        "refuse", PHASE_5_ADMISSION[case_id])
    assert _adjudicate(_joined(raw)) == ("refuse", PHASE_5_ADMISSION[case_id])


def test_admission_without_a_binding_is_a_harness_error():
    from scripts.council_convening import resolution

    vector = _admission()
    del vector["inputs"]["binding"]
    with pytest.raises(resolution.HarnessError):
        resolution.adjudicate(vector)


@pytest.mark.parametrize("operation", ["seat_execution", None, "Commission"])
def test_admission_judges_only_the_commission_jobs_token(operation):
    from scripts.council_convening import resolution

    vector = _admission()
    vector["inputs"]["operation"] = operation
    with pytest.raises(resolution.HarnessError):
        resolution.adjudicate(vector)


def test_a_commission_vector_carrying_a_binding_is_a_harness_error():
    from scripts.council_convening import resolution

    vector = _joined(_raw("commission-accept-conditional-seat-not-held"))
    vector["inputs"]["binding"] = admission_binding()
    with pytest.raises(resolution.HarnessError):
        resolution.adjudicate(vector)


def test_a_shared_commission_vector_reaches_the_consumer_without_a_binding():
    # conformance-corpus § How each side runs a shared vector: a shared vector
    # carries no binding, so the consumer runs it without A1 and A4. It carries
    # no `identity` oracle, so a consumer run that read one would be a harness
    # error, not this pass.
    shared = []
    for path in sorted(RESOLUTION_VECTORS.glob("commission-*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw["applies_to"] == ["producer", "consumer"]:
            assert "binding" not in raw["inputs"], raw["case_id"]
            assert "identity" not in raw.get("environment", {}), raw["case_id"]
            shared.append(raw)
    assert shared
    raw = next(r for r in shared if r["expected"]["outcome"] == "accept")
    assert _adjudicate(_joined(raw)) == ("accept", None)


def test_resolve_takes_the_binding_at_admission_and_refuses_it_at_commission(tmp_path):
    from scripts.council_convening import resolution

    vector = _admission()
    record = vector["inputs"]["record"]
    root = write_identity_map(tmp_path / "root")
    with pytest.raises(resolution.HarnessError):
        resolution.resolve(record, boundary="admission",
                           selected_protocol=vector["inputs"]["selected_protocol"],
                           oracles=resolution.VectorOracles(vector["environment"]))
    result = resolution.resolve(
        record, boundary="admission",
        selected_protocol=vector["inputs"]["selected_protocol"],
        oracles=resolution.VectorOracles(vector["environment"]),
        binding=vector["inputs"]["binding"], identity_root=root,
        evaluation_time=vector["evaluation_time"])
    assert result.required_seats == vector["expected"]["derived"]["required_seats"]
    commission = _joined(_raw("commission-accept-conditional-seat-not-held"))
    with pytest.raises(resolution.HarnessError):
        resolution.resolve(
            commission["inputs"]["record"], boundary="commission",
            selected_protocol=commission["inputs"]["selected_protocol"],
            oracles=resolution.VectorOracles(commission["environment"]),
            expected_candidate=commission["inputs"]["expected_candidate"],
            binding=admission_binding(), identity_root=root,
            evaluation_time=commission["evaluation_time"])


def test_a1_reads_the_verified_claims_before_step_3_and_only_them(tmp_path):
    # Data-model E2 step 3: the admission steps before it consult oracles only by
    # grammar-checked identifiers, and A1 reads the verified claims.
    from scripts.council_convening import resolution

    vector = _admission("admission-refuse-order-binding-before-secret")
    oracles = resolution.VectorOracles(vector["environment"])
    with pytest.raises(Refused) as refused:
        resolution.resolve(
            vector["inputs"]["record"], boundary="admission",
            selected_protocol=vector["inputs"]["selected_protocol"], oracles=oracles,
            binding=vector["inputs"]["binding"],
            identity_root=write_identity_map(tmp_path / "root"),
            evaluation_time=vector["evaluation_time"])
    assert refused.value.code == "audience_mismatch"
    assert oracles.reads == [("identity", None)]


@pytest.mark.parametrize("case_id, code", [
    ("admission-refuse-order-candidate-before-workflow-revision", "candidate_mismatch"),
    ("admission-refuse-order-mutable-revision-before-workflow-revision",
     "mutable_rule_reference"),
    ("admission-refuse-order-former-governed-spelling-before-workflow-revision",
     "rule_unauthorized"),
    ("admission-refuse-order-superseded-before-workflow-revision", "rule_superseded"),
])
def test_a4_reads_the_governed_member_only_after_step_5_checked_it(case_id, code):
    # R4-H2: a mutable revision, and a governed repository the allowlist does not
    # name, are refused by step 5 under their own codes, never by step 14. Each
    # of these vectors carries BOTH defects: step 14 alone, on the vector's own
    # token and record, refuses.
    vector = _admission(case_id)
    assert _adjudicate(vector) == ("refuse", code)
    entry = vector["inputs"]["binding"]["permitted_workflows"][0]
    with pytest.raises(Refused) as refused:
        binding.check_workflow_revision(
            entry, identity=vector["environment"]["identity"],
            governed=vector["inputs"]["record"]["required_seats_provenance"]["governed"],
            governed_history=None)
    assert refused.value.code == "workflow_revision_ungoverned"


def test_admission_reads_the_map_each_vector_carries_never_the_live_one(monkeypatch):
    real = estate_inventory.load_transfers
    seen = []

    def spy(root):
        seen.append(root.resolve())
        return real(root)

    monkeypatch.setattr(estate_inventory, "load_transfers", spy)
    for _, raw in _all_admission_vectors():
        expected = raw["expected"]
        assert _adjudicate(_joined(raw)) == (expected["outcome"], expected["refusal"])
    assert seen and REPO_ROOT.resolve() not in seen


def test_the_seat_workflow_is_not_permitted_for_the_commission_token():
    vector = _admission("admission-refuse-binding-seat-token-for-commission")
    claims = vector["environment"]["identity"]["claims"]
    assert claims["job_workflow_ref"] != admission_workflow()
    assert _adjudicate(vector) == ("refuse", "workflow_not_permitted")


def test_with_passing_binding_passes_a1_and_a4_on_the_base_record():
    raw = _raw(ADMISSION_BASE)
    for member in ("binding", "operation"):
        raw["inputs"].pop(member, None)
    for member in ("identity", "repository_identity"):
        raw["environment"].pop(member, None)
    vector = _joined(with_passing_binding(raw))
    assert _adjudicate(vector) == ("accept", None)


ASSIGNMENT_VECTORS = BINDING_VECTORS.parent / "assignment"

#: Phase 3's twelve retry-identity vectors (E2 step A3), re-authored to carry a
#: passing binding. Their outcomes do not move.
PHASE_3_RETRY = {
    "asg-retry-conflict-packet-refs-refuse": "convening_conflict",
    "asg-retry-conflict-pull-number-only-refuse": "convening_conflict",
    "asg-retry-conflict-subject-path-only-refuse": "convening_conflict",
    "asg-retry-identical-after-head-moved-accept": None,
    "asg-retry-identical-after-tip-moved-accept": None,
    "asg-retry-identical-not-pre-empted-by-once-per-pin-accept": None,
    "asg-retry-identical-returns-snapshot-accept": None,
    "asg-retry-order-conflict-before-head-moved-refuse": "convening_conflict",
    "asg-retry-order-conflict-before-secret-refuse": "convening_conflict",
    "asg-retry-order-shape-before-conflict-refuse": "convening_malformed",
    "asg-retry-other-council-same-pin-not-conflict-accept": None,
    "asg-retry-same-council-other-pin-not-conflict-accept": None,
}

#: A1 before A3: a token that fails binding never reaches retry identity, so an
#: identical retry does not return the snapshot and a conflicting one is not
#: `convening_conflict` (T051).
PHASE_5_RETRY_ORDER = {
    "asg-retry-order-binding-before-identical-retry-refuse": "claims_expired",
    "asg-retry-order-binding-before-conflict-refuse": "audience_mismatch",
}


def _assignment_raw(case_id):
    return json.loads((ASSIGNMENT_VECTORS / f"{case_id}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case_id", sorted(PHASE_3_RETRY))
def test_the_re_authored_phase_3_retry_vectors_keep_their_outcomes(case_id):
    raw = _assignment_raw(case_id)
    assert "binding" in raw["inputs"] and raw["inputs"]["operation"] == "commission"
    code = PHASE_3_RETRY[case_id]
    expected = ("accept", None) if code is None else ("refuse", code)
    assert (raw["expected"]["outcome"], raw["expected"]["refusal"]) == expected
    assert _adjudicate(_joined(raw)) == expected


@pytest.mark.parametrize("case_id", sorted(PHASE_5_RETRY_ORDER))
def test_a1_runs_before_retry_identity(case_id):
    raw = _assignment_raw(case_id)
    assert raw["boundary"] == "admission" and raw["applies_to"] == ["consumer"]
    assert raw["area"] == "assignment" and "FR-009" in raw["requirement_ids"]
    assert raw["environment"]["issued"]["live_snapshots"], case_id
    assert (raw["expected"]["outcome"], raw["expected"]["refusal"]) == (
        "refuse", PHASE_5_RETRY_ORDER[case_id])
    assert "convening_id" not in raw["expected"]["derived"]
    assert _adjudicate(_joined(raw)) == ("refuse", PHASE_5_RETRY_ORDER[case_id])


def test_the_identical_retry_with_a_passing_token_returns_the_snapshot():
    # The control for A1 before A3: the same vector with the token restored
    # returns the live snapshot's id.
    from scripts.council_convening import resolution

    vector = _joined(_assignment_raw("asg-retry-order-binding-before-identical-retry-refuse"))
    accepted = _joined(_assignment_raw("asg-retry-identical-returns-snapshot-accept"))
    vector["environment"]["identity"] = accepted["environment"]["identity"]
    got = resolution.adjudicate(vector)
    assert got["outcome"] == "accept"
    assert got["derived"]["convening_id"] == accepted["expected"]["derived"]["convening_id"]


def test_the_snapshot_half_reads_no_binding_and_no_map():
    # Data-model E4's order judges a snapshot, never the commission job's token.
    from scripts.council_convening import corpus

    snapshots = _all_admission_vectors(role="snapshot")
    assert snapshots
    for case_id, raw in snapshots:
        assert "binding" not in raw["inputs"], case_id
        assert "repository_identity" not in raw.get("environment", {}), case_id
        assert not corpus.reads_identity_map(raw), case_id
    for _, raw in _all_admission_vectors():
        assert corpus.reads_identity_map(raw)


# =========================================================================
# The independent review of 52a80130, cff00ac5 and c46d981e (lane
# codeXfactory-1): one MEDIUM and five LOW findings, each pinned here first.
# =========================================================================


def test_the_coverage_floor_carries_fr_009():
    # MEDIUM: without FR-009 in the floor, deleting every binding vector's
    # citation would not fail the gate.
    from scripts.council_convening import generate

    assert "FR-009" in generate.COVERAGE_FLOOR
    index = json.loads((BINDING_VECTORS.parents[1] / "index.json").read_text(
        encoding="utf-8"))
    assert "FR-009" in index["coverage_floor"]


def test_uncited_fr_009_fails_the_corpus(family_tree):
    from scripts.council_convening import corpus, generate

    vectors = family_tree / "contracts" / "council-convening" / "conformance" / "vectors"
    stripped = 0
    for path in sorted(vectors.glob("*/*.json")):
        vector = json.loads(path.read_text(encoding="utf-8"))
        if "FR-009" in vector["requirement_ids"]:
            vector["requirement_ids"] = [r for r in vector["requirement_ids"]
                                         if r != "FR-009"] or ["FR-001"]
            path.write_bytes(corpus.dump_json(vector))
            stripped += 1
    assert stripped
    generate.generate(family_tree)
    codes = [f.code for f in corpus.check_corpus(family_tree).findings]
    assert "council-convening-requirement-without-probe" in codes


#: LOW 1: a branch name may carry `@` (git forbids only `@{` and a lone `@`).
AT_BRANCH_REF = f"{GOVERNED}/.github/workflows/corpus-commission.yml@refs/heads/rel@2"
FORMER_AT_BRANCH_REF = (
    f"{GOVERNED_FORMER}/.github/workflows/council-lane-reusable.yml@refs/heads/rel@2")


def test_a_ref_carrying_an_at_sign_parses():
    parsed = binding.parse_workflow_ref(AT_BRANCH_REF)
    assert parsed is not None
    assert (parsed.repository, parsed.ref) == (GOVERNED, "refs/heads/rel@2")


@pytest.mark.parametrize("ref", [
    FORMER_AT_BRANCH_REF,
    # Not a workflow reference at all: its first two segments still name the
    # former spelling, and step 4 judges every permitted ref by them.
    f"{GOVERNED_FORMER}/workflows/corpus-commission.yml",
    f"{GOVERNED_FORMER_CASE_VARIANT}/.github/workflows/x.yml@refs/heads/a@b",
])
def test_step_4_judges_every_permitted_ref_by_its_first_two_segments(map_root, ref):
    b = commission_binding(permitted_workflows=[{
        "operation": "commission", "job_workflow_ref": ref,
        "workflow_revision_rule": "equals_governed_revision"}])
    assert code_of(b, map_root) == "repository_identity_former"


def test_a_commission_workflow_on_an_at_branch_is_accepted(map_root):
    b = commission_binding(permitted_workflows=[{
        "operation": "commission", "job_workflow_ref": AT_BRANCH_REF,
        "workflow_revision_rule": "equals_governed_revision"}])
    entry = binding.check_binding(
        b, operation="commission",
        identity=identity(claims_for(b, job_workflow_ref=AT_BRANCH_REF)),
        governed=governed(), evaluation_time=EVALUATION_TIME, identity_root=map_root)
    assert entry["job_workflow_ref"] == AT_BRANCH_REF


@pytest.mark.parametrize("spelling, former", [
    # LOW 2, the literal E10 reading: a non-canonical case variant of ANY listed
    # spelling, the pending row's included, is refused.
    ("opensoft/examplefactory", True),
    ("OpenSoft/ExampleFactory", True),
    ("exampleorg/ExampleFactory", True),
    ("ExampleOrg/examplefactory", True),
    # The pending row's spellings themselves stay as they were: its `former` is
    # still the only address (`pending_row_rule`).
    (PENDING_FORMER, False),
    (PENDING_CURRENT, False),
])
def test_a_case_variant_of_a_pending_spelling_is_former(map_root, spelling, former):
    assert binding.load_identity_map(map_root).is_former(spelling) is former


def test_a_caller_spelled_as_a_pending_case_variant_is_refused(map_root):
    b = commission_binding(caller_repository="opensoft/examplefactory",
                           subject_template="repo:opensoft/examplefactory:ref:refs/heads/main")
    assert code_of(b, map_root) == "repository_identity_former"


def _bind_vector(name):
    return json.loads((BINDING_VECTORS / f"{name}.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("oracle", ["identity", "governed_history"])
def test_a_binding_vector_missing_an_oracle_it_reads_is_a_harness_error(oracle):
    # LOW 3: as at admission, a missing oracle is never a refusal.
    from scripts.council_convening import classification, corpus, records

    name = ("bind-commission-accept" if oracle == "identity"
            else "bind-seat-per-seat-environment-accept")
    vector = _bind_vector(name)
    assert oracle in vector["environment"]
    del vector["environment"][oracle]
    with pytest.raises(ValueError):
        binding.evaluate_vector(vector)
    with pytest.raises(corpus.VectorInputError):
        corpus.HANDLERS["binding"].handler(
            vector, corpus.Context(records.load_schemas(), classification.load_registry()))


def test_an_offline_refusal_needs_no_identity_oracle():
    # The oracle is required where it is READ: a binding refused at steps 1 to 6
    # never reaches the claims.
    vector = _bind_vector("bind-subject-wildcard-refuse")
    del vector["environment"]["identity"]
    assert binding.evaluate_vector(vector) == ("refuse", "binding_wildcard")


def test_the_template_permits_one_operation():
    # Info: a stub permitting both operations would carry the seat entry into a
    # commission binding, or the commission entry into a seat's (025 (A)).
    doc = yaml.safe_load(BINDING_TEMPLATE.read_text(encoding="utf-8"))
    assert [e["operation"] for e in doc["permitted_workflows"]] == ["commission"]
    text = BINDING_TEMPLATE.read_text(encoding="utf-8")
    assert "seat_execution" in text and "on_governed_history_since_revision" in text


def test_the_claim_keys_description_names_the_claims_supported_only_members():
    # Reading 2: `sha` and `ref_protected` are in GitHub's `claims_supported`
    # but not in its claims table, so they are not members.
    doc = yaml.safe_load(BINDING_SCHEMA.read_text(encoding="utf-8"))
    prop = doc["properties"]["subject_claim_keys"]
    assert "claims_supported" in prop["description"]
    assert "`sha`" in prop["description"] and "`ref_protected`" in prop["description"]
    assert "sha" not in prop["items"]["enum"]
    assert "ref_protected" not in prop["items"]["enum"]


def test_the_review_round_vectors_pin_their_codes():
    expected = {
        "bind-permitted-ref-at-branch-former-refuse": "repository_identity_former",
        "bind-permitted-ref-unparsed-former-refuse": "repository_identity_former",
        "bind-commission-at-branch-accept": None,
        "bind-caller-pending-case-variant-refuse": "repository_identity_former",
        "bind-workflow-pending-current-case-variant-refuse": "repository_identity_former",
    }
    for name, code in expected.items():
        vector = _bind_vector(name)
        assert "FR-009" in vector["requirement_ids"], name
        want = ("accept", None) if code is None else ("refuse", code)
        assert (vector["expected"]["outcome"], vector["expected"]["refusal"]) == want, name
        assert binding.evaluate_vector(vector) == want, name
