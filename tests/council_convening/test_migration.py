"""T057: the matched migration (data-model E1 effects, E11 selection, E12 activation).

Phase 6 of feature 035, User Story 3 (FR-011, FR-012; D5). Four boundaries are
probed here, each through the corpus's own vector contract
(`corpus.adjudicate`), so a test reads exactly what a successor's adapter reads:

* `classification`, the E1 EFFECTS TABLE completed: every row, under each legacy
  registry status, by override. Phase 1 landed the `in_use` rows; Phase 6 lands
  `deprecated` (a route that also carries `legacy_protocol_deprecated`) and
  `historical_only` (a legacy selection is itself refused, in either mode).
* `historical`, the `--historical` row: a record is classified by its recorded
  protocol and never reinterpreted, at any status. A legacy record is routed; a
  replacement record goes on to the replacement rules.
* `selection`, E11 in its order: `selection_malformed`, `protocol_unknown`,
  admission eligibility and the `historical_only` refusal, the pair matched on
  all five members, then `rejected_without_fallback`.
* `activation`, E12 in its order: `activation_evidence_malformed`, each act's
  required members, the binding set and broker capability, the pair, then
  `historical_reinterpretation_refused`.

BRETT HEAP'S 025 RULING (A), "Per-seat environments (Recommended)", 2026-10-09T01:20:43Z:
one producer binding per council seat. So the consumer's configured binding set
is its commission binding plus one binding per seat, and an activation's
`binding_refs` lists every one of them. The binding-set cases below are written
with per-seat bindings, for both of the estate's councils as they stand.

TWO READINGS THE DATA MODEL LEAVES OPEN, encoded and disclosed in evidence.md
§ Phase 6:

* The backing rehearsal is compared with the activation on its provider and on
  the matched selection values OTHER THAN `mode`: a rehearsal runs its
  selections in `mode: rehearsal` and an activation in `mode: active`, so a
  comparison that included `mode` would refuse every activation.
* In a rollback, `producer` and `consumer` are the pair the rollback RESTORES,
  matched at step 4 (a paired rollback); `rollback.restored_producer` and
  `rollback.restored_consumer` are each side's restoration evidence.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
import yaml

from scripts.council_convening import classification, corpus, generate, migration, records

from .conftest import FAMILY_REL, INDEX, LEGACY, REPLACEMENT, load_validator, run_validator

assert migration  # imported for its handler registrations

SHA = "0123456789abcdef0123456789abcdef01234567"
OTHER_SHA = "89abcdef0123456789abcdef0123456789abcdef"
INDEX_SHA = "sha256:" + "cd" * 32
OTHER_INDEX_SHA = "sha256:" + "ef" * 32
#: Illustrative tags, never allocations: Release A is the deprecation minor
#: (Phase 7), Release B the removal major (Phase 8).
RELEASE_A = "contract-v4.1"
BUNDLE = "contract-v5.0"
RELEASE_A_SHA = "fedcba9876543210fedcba9876543210fedcba98"
RELEASE_A_INDEX = "sha256:" + "1a" * 32
FPR = "sha256:" + "ab" * 32
NOW = "2026-10-09T00:00:00Z"

FULL_FLOOR = [f"FR-{n:03d}" for n in range(1, 13)] + ["SC-001", "SC-002", "SC-003"]

PHASE_6_REFUSALS = [
    "selection_malformed",
    "pair_mismatched",
    "rejected_without_fallback",
    "replacement_not_admission_eligible",
    "activation_evidence_malformed",
    "activation_evidence_incomplete",
    "historical_reinterpretation_refused",
]

LEGACY_RECORD = {"protocol": LEGACY, "key_fingerprint": FPR, "signature": "sig"}
REPLACEMENT_RECORD = {"schema_version": 1, "kind": "xfactory_council_convening",
                      "protocol": REPLACEMENT, "council_id": "merge-readiness",
                      "subject_pin": SHA}

#: The estate's two councils as their governed documents stand at codexFactory
#: `48d0560e` (hermes/domain/review-councils/): merge-readiness's three standing
#: seats and its conditional tenant seat, and gate-rules's six.
MERGE_READINESS_SEATS = ["lead-quality", "lead-security", "lead-integration",
                         "company-policy-lead"]
GATE_RULES_SEATS = ["lead-architect", "lead-security", "lead-quality",
                    "company-policy-lead", "client-security-compliance-officer",
                    "intent_owner_role_slot"]


@pytest.fixture(scope="module")
def schemas():
    return records.load_schemas()


@pytest.fixture(scope="module")
def registry():
    return classification.load_registry()


@pytest.fixture(scope="module")
def context(schemas, registry):
    return corpus.Context(schemas, registry)


# --------------------------------------------------------------------------
# Builders.
# --------------------------------------------------------------------------

def _vector(boundary: str, inputs: dict, environment: dict | None = None) -> dict:
    vector = {"schema_version": 1, "kind": corpus.VECTOR_KIND, "case_id": "probe",
              "area": "migration", "boundary": boundary,
              "applies_to": ["producer", "consumer"], "requirement_ids": ["FR-011"],
              "evaluation_time": NOW, "inputs": inputs,
              "expected": {"outcome": "accept", "refusal": None, "findings": [],
                           "derived": {}, "derived_origin": "hand"}}
    if environment:
        vector["environment"] = environment
    return vector


def _run(context, boundary: str, inputs: dict, environment: dict | None = None):
    return corpus.adjudicate(_vector(boundary, inputs, environment), context)


def _verdict(outcome) -> tuple:
    return (outcome.outcome, outcome.refusal, tuple(outcome.findings))


def selection(side: str, mode: str = "rehearsal", protocol: str = REPLACEMENT,
              commit: str = SHA, bundle: str | None = None,
              index: str = INDEX_SHA) -> dict:
    """An E11 record."""
    return {"schema_version": 1, "kind": "xfactory_council_protocol_selection",
            "side": side, "mode": mode, "protocol": protocol,
            "provider_commit": commit, "provider_bundle": bundle,
            "corpus_index_sha256": index}


def pair(**members) -> tuple[dict, dict]:
    return selection("producer", **members), selection("consumer", **members)


def binding(binding_id: str, operation: str = "seat_execution",
            verified: bool = True, evidence: str | None = "broker-evidence-0001",
            environment: str | None = None) -> dict:
    """An E10 binding instance, one per seat environment under 025 ruling (A).

    The OIDC subject names the seat's GitHub environment, so each seat's
    binding is its own: the consumer maps environment to seat to binding.
    """
    environment = environment or binding_id
    rule = ("equals_governed_revision" if operation == "commission"
            else "on_governed_history_since_revision")
    workflow = ("council-lane-reusable.yml" if operation == "commission"
                else "council-seat-worker.yml")
    return {
        "schema_version": 1,
        "kind": "xfactory_council_producer_binding",
        "protocol": REPLACEMENT,
        "binding_id": binding_id,
        "principal_kind": "github_oidc_job",
        "issuer": "https://token.actions.githubusercontent.com",
        "audience": "council-convening-conformance",
        "caller_repository": "opensoft/xFactory",
        "repository_id": 700000001,
        "subject_claim_keys": ["repo", "context"],
        "subject_template": f"repo:opensoft/xFactory:environment:{environment}",
        "permitted_workflows": [{
            "operation": operation,
            "job_workflow_ref": f"codeXfactory/codexFactory/.github/workflows/{workflow}"
                                f"@refs/heads/main",
            "workflow_revision_rule": rule,
        }],
        "broker": {"broker_ref": "broker-0001", "capability_verified": verified,
                   "evidence_ref": evidence},
    }


def per_seat_bindings(*seat_lists: list[str]) -> list[dict]:
    """The configured set under 025 ruling (A): one commission binding per
    council, and one binding per seat of each council."""
    found = []
    for number, seats in enumerate(seat_lists, start=1):
        found.append(binding(f"council-{number}-commission", operation="commission"))
        found.extend(binding(f"council-{number}-seat-{seat}") for seat in seats)
    return found


PROVIDER = {"commit": SHA, "bundle": BUNDLE, "corpus_index_sha256": INDEX_SHA}
#: The pair a rollback after activation restores.
RESTORED = {"mode": "active", "protocol": LEGACY, "commit": RELEASE_A_SHA,
            "bundle": RELEASE_A, "index": RELEASE_A_INDEX}
OWNER_WORD = {"author": "Example Owner", "date": "2026-10-09T00:00:00Z",
              "verbatim": "an example owner word, for a conformance vector only",
              "cite": "conformance-vector-example"}
INTAKE = {"paused_at": "2026-10-08T23:00:00Z"}


def side(role: str, **selection_members) -> dict:
    repository = "opensoft/xFactory" if role == "producer" else "opensoft/xFactory-Hermes-Install"
    return {"repository": repository, "revision": OTHER_SHA,
            "selection": selection(role, **selection_members)}


def rehearsal_record(mode: str = "matched", outcome: str = "pass", provider=None,
                     **selection_members) -> dict:
    members = {"bundle": BUNDLE, **selection_members}
    record = {"schema_version": 1, "kind": "xfactory_council_activation_evidence",
              "act": "rehearsal", "recorded_at": "2026-10-08T23:30:00Z",
              "provider": provider or dict(PROVIDER),
              "producer": side("producer", **members),
              "consumer": side("consumer", **members),
              "rehearsal": {"mode": mode, "corpus_index_sha256": INDEX_SHA,
                            "outcome": outcome, "evidence_ref": "rehearsal-run-0001"}}
    if mode == "matched":
        record["intake"] = dict(INTAKE)
    return record


def rehearsal_text(record: dict) -> str:
    """The record's exact UTF-8 text, as `inputs.rehearsal` carries it."""
    return corpus.dump_json(record).decode("utf-8")


def ref_of(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def evidence(act: str, bindings: list[dict] | None = None, rehearsal: str | None = None,
             **overrides) -> dict:
    """A complete E12 record for `act`."""
    record = {"schema_version": 1, "kind": "xfactory_council_activation_evidence",
              "act": act, "recorded_at": "2026-10-09T00:00:00Z",
              "provider": dict(PROVIDER)}
    active = {"mode": "active", "bundle": BUNDLE}
    if act in ("pause", "switch", "activation", "rollback", "resume"):
        record["owner_word"] = dict(OWNER_WORD)
    if act in ("drain", "switch", "activation", "rollback"):
        record["intake"] = dict(INTAKE)
    if act == "drain":
        record["in_flight"] = {"disposition": "drained", "convening_ids": ["conv-0001"]}
    if act in ("switch", "activation", "rollback", "resume"):
        record["producer"] = side("producer", **active)
        record["consumer"] = side("consumer", **active)
    if act == "rehearsal":
        return {**rehearsal_record(), **overrides}
    if act in ("activation", "resume"):
        record["rehearsal_ref"] = ref_of(rehearsal) if rehearsal is not None else ref_of(
            rehearsal_text(rehearsal_record()))
        record["binding_refs"] = [b["binding_id"] for b in (bindings or [])]
    if act == "rollback":
        # Brett Heap, 2026-10-09T13:22:16Z, "Back to Release A pins (Recommended)":
        # both sides return to their Release A pins and reselect legacy there.
        record["provider"] = {"commit": RELEASE_A_SHA, "bundle": RELEASE_A,
                              "corpus_index_sha256": RELEASE_A_INDEX}
        record["producer"] = side("producer", **RESTORED)
        record["consumer"] = side("consumer", **RESTORED)
        record["rollback"] = {
            "restored_producer": {"verified_at": "2026-10-09T00:00:00Z",
                                  "evidence_ref": "restore-producer-0001"},
            "restored_consumer": {"verified_at": "2026-10-09T00:00:00Z",
                                  "evidence_ref": "restore-consumer-0001"},
            "new_records_retained": True,
            "new_records_protocol": REPLACEMENT,
        }
    record.update(overrides)
    return record


def activate(context, record: dict, bindings: list[dict] | None = None,
             rehearsal: str | None = None):
    inputs: dict = {"record": record}
    if record.get("act") in ("activation", "resume"):
        inputs["bindings"] = bindings if bindings is not None else per_seat_bindings(
            MERGE_READINESS_SEATS)
        inputs["rehearsal"] = (rehearsal if rehearsal is not None
                               else rehearsal_text(rehearsal_record()))
    return _run(context, "activation", inputs)


def activation_case(act: str = "activation", seats=(MERGE_READINESS_SEATS,), **overrides):
    """A complete activation or resume, with its per-seat bindings and its
    passing matched rehearsal, as `(record, bindings, rehearsal_text)`."""
    bindings = per_seat_bindings(*seats)
    text = rehearsal_text(rehearsal_record())
    return evidence(act, bindings=bindings, rehearsal=text, **overrides), bindings, text


# --------------------------------------------------------------------------
# E1: the effects table, every row, under each legacy status, by override.
# --------------------------------------------------------------------------

STATUSES = ("in_use", "deprecated", "historical_only")
ROUTED = ("legacy_protocol_routed",)
ROUTED_DEPRECATED = ("legacy_protocol_routed", "legacy_protocol_deprecated")

#: data-model E1: (selected protocol, legacy status, record) -> verdict.
EFFECTS = {
    **{(REPLACEMENT, status, "legacy"): ("refuse", "legacy_protocol_refused", ())
       for status in STATUSES},
    **{(REPLACEMENT, status, "replacement"): ("accept", None, ()) for status in STATUSES},
    (LEGACY, "in_use", "legacy"): ("route", None, ROUTED),
    (LEGACY, "in_use", "replacement"): ("refuse", "protocol_not_selected", ()),
    (LEGACY, "deprecated", "legacy"): ("route", None, ROUTED_DEPRECATED),
    (LEGACY, "deprecated", "replacement"): ("refuse", "protocol_not_selected", ()),
    (LEGACY, "historical_only", "legacy"): ("refuse", "legacy_protocol_refused", ()),
    (LEGACY, "historical_only", "replacement"): ("refuse", "legacy_protocol_refused", ()),
    **{(None, status, "legacy"): ("route", None, ROUTED) for status in STATUSES},
    **{(None, status, "replacement"): ("accept", None, ()) for status in STATUSES},
}

RECORDS = {"legacy": LEGACY_RECORD, "replacement": REPLACEMENT_RECORD}


@pytest.mark.parametrize("selected, status, kind", sorted(
    EFFECTS, key=lambda key: (str(key[0]), key[1], key[2])))
def test_every_row_of_the_effects_table_under_each_status(registry, selected, status, kind):
    outcome = classification.classify_and_select(RECORDS[kind], selected, registry,
                                                 {LEGACY: status})
    assert _verdict(outcome) == EFFECTS[(selected, status, kind)]
    if outcome.outcome != "refuse":
        assert outcome.derived == {"classification": kind}


@pytest.mark.parametrize("selected, status, kind", sorted(
    EFFECTS, key=lambda key: (str(key[0]), key[1], key[2])))
def test_the_effects_are_the_same_through_a_classification_vector(
        context, selected, status, kind):
    outcome = _run(context, "classification",
                   {"record": RECORDS[kind], "selected_protocol": selected},
                   {"registry_status": {LEGACY: status}})
    assert _verdict(outcome) == EFFECTS[(selected, status, kind)]


@pytest.mark.parametrize("status", STATUSES)
def test_only_a_legacy_selection_reads_the_legacy_status(registry, status):
    """The rows keyed by a replacement selection, or none, read no status, so
    their vectors' outcomes cannot move when a cut flips the registry."""
    for kind, record in RECORDS.items():
        legacy_selected = classification.classify_and_select(
            record, LEGACY, registry, {LEGACY: status})
        assert legacy_selected.status_read is True
        for selected in (REPLACEMENT, None):
            outcome = classification.classify_and_select(record, selected, registry,
                                                         {LEGACY: status})
            assert outcome.status_read is False, (kind, selected)


def test_a_deprecated_route_carries_both_findings_in_order(registry):
    outcome = classification.classify_and_select(LEGACY_RECORD, LEGACY, registry,
                                                 {LEGACY: "deprecated"})
    assert outcome.findings == ("legacy_protocol_routed", "legacy_protocol_deprecated")


def test_classification_still_runs_before_a_historical_only_selection_is_read(registry):
    outcome = classification.classify_and_select({"protocol": "xfc-resolved-council-2"},
                                                 LEGACY, registry,
                                                 {LEGACY: "historical_only"})
    assert _verdict(outcome) == ("refuse", "protocol_unknown", ())
    assert outcome.status_read is False


# --------------------------------------------------------------------------
# The `--historical` row: classified by the recorded protocol, never reinterpreted.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("status", STATUSES)
def test_historically_a_legacy_record_routes_at_every_status(context, status):
    outcome = _run(context, "historical", {"record": LEGACY_RECORD},
                   {"registry_status": {LEGACY: status}})
    assert _verdict(outcome) == ("route", None, ROUTED)
    assert outcome.derived == {"classification": "legacy"}


@pytest.mark.parametrize("statuses", [
    {LEGACY: "in_use", REPLACEMENT: "available"},
    {LEGACY: "deprecated", REPLACEMENT: "available"},
    {LEGACY: "historical_only", REPLACEMENT: "admission_eligible"},
])
def test_historically_a_replacement_record_goes_to_the_replacement_rules(context, statuses):
    outcome = _run(context, "historical", {"record": REPLACEMENT_RECORD},
                   {"registry_status": statuses})
    assert _verdict(outcome) == ("accept", None, ())
    assert outcome.derived == {"classification": "replacement"}


def test_historically_no_status_is_read(context):
    for record in RECORDS.values():
        outcome = _run(context, "historical", {"record": record})
        assert outcome.status_read is False
        assert getattr(outcome, "statuses_read", ()) == ()


@pytest.mark.parametrize("record, kind", [
    # Recorded as legacy, shaped like a replacement record: still legacy.
    ({"protocol": LEGACY, "required_seats": ["lead-quality"],
      "council_id": "merge-readiness"}, "legacy"),
    # Recorded as replacement, carrying every legacy shape: still replacement.
    ({"protocol": REPLACEMENT, "root_key_fingerprint": FPR,
      "council_convening": {"council_id": "c"},
      "signature": {"protocol": "xfactory-council-seat-return/v1"}}, "replacement"),
    # No protocol: the legacy seat result's own shape, its context string under
    # `signature.protocol` (codexFactory `council_seat_signing.py`): legacy.
    ({"seat": "lead-security", "signature": {"protocol": LEGACY, "key_fingerprint": FPR,
                                             "signature": "sig"}}, "legacy"),
    # No protocol, the roster-less convening block: legacy.
    ({"council_convening": {"council_id": "merge-readiness", "subject_pin": SHA,
                            "packet_refs": ["opensoft/openxFactory#1268"]}}, "legacy"),
])
def test_historically_the_recorded_protocol_decides_never_the_shape(context, record, kind):
    outcome = _run(context, "historical", {"record": record})
    assert outcome.derived == {"classification": kind}


def test_historically_an_unknown_protocol_is_refused(context):
    outcome = _run(context, "historical", {"record": {"protocol": "xfc-resolved-council-2"}})
    assert _verdict(outcome) == ("refuse", "protocol_unknown", ())


@pytest.mark.parametrize("inputs", [
    {"record": LEGACY_RECORD, "selected_protocol": None},
    {},
    {"record": "not an object"},
    {"record": {"schema_version": 1, "kind": "xfactory_council_protocol_selection"}},
])
def test_a_historical_vector_takes_exactly_one_record_that_classifies(context, inputs):
    with pytest.raises(corpus.VectorInputError):
        _run(context, "historical", inputs)


def test_check_historical_routes_a_legacy_record_with_exit_3(tmp_path):
    path = tmp_path / "legacy.json"
    path.write_text(json.dumps(LEGACY_RECORD) + "\n", encoding="utf-8")
    result = run_validator("check", "--historical", str(path), cwd=tmp_path)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "council-convening-legacy-protocol-routed" in result.stdout
    assert "ERROR [" not in result.stdout


# --------------------------------------------------------------------------
# `deprecated` in the CLI: a WARN beside the route, an ERROR under --strict.
# --------------------------------------------------------------------------

def _flip_registry(root: Path, legacy_status: str, replacement_status: str = "available"):
    path = root / FAMILY_REL / "protocol.registry.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    for entry in document["protocols"]:
        entry["status"] = (legacy_status if entry["protocol_id"] == LEGACY
                           else replacement_status)
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def _legacy_file(tmp_path: Path) -> Path:
    path = tmp_path / "legacy.json"
    path.write_text(json.dumps(LEGACY_RECORD) + "\n", encoding="utf-8")
    return path


def test_check_warns_beside_the_route_while_legacy_is_deprecated(family_tree, tmp_path, capsys,
                                                                  monkeypatch):
    monkeypatch.chdir(tmp_path)
    _flip_registry(family_tree, "deprecated")
    assert load_validator().main(["check", str(_legacy_file(tmp_path))],
                                 root=family_tree) == 3
    out = capsys.readouterr().out
    assert "council-convening-legacy-protocol-routed" in out
    assert "WARN  [council-convening-legacy-protocol-deprecated]" in out
    assert "ERROR [" not in out


@pytest.mark.parametrize("argv", [["--strict", "check"], ["check", "--strict"]])
def test_the_deprecated_warning_is_an_error_under_strict(family_tree, tmp_path, capsys, argv,
                                                          monkeypatch):
    monkeypatch.chdir(tmp_path)
    _flip_registry(family_tree, "deprecated")
    assert load_validator().main([*argv, str(_legacy_file(tmp_path))],
                                 root=family_tree) == 1
    assert "council-convening-legacy-protocol-deprecated" in capsys.readouterr().out


def test_no_deprecated_warning_while_legacy_is_in_use(tmp_path):
    result = run_validator("--strict", "check", str(_legacy_file(tmp_path)), cwd=tmp_path)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "legacy-protocol-deprecated" not in result.stdout


@pytest.mark.parametrize("status", ["deprecated", "historical_only"])
def test_check_historical_is_status_invariant(family_tree, tmp_path, capsys, status,
                                              monkeypatch):
    """A historical audit classifies and never reinterprets: it routes a legacy
    record at every status, with no deprecation finding, even under --strict."""
    monkeypatch.chdir(tmp_path)
    _flip_registry(family_tree, status, "admission_eligible"
                   if status == "historical_only" else "available")
    assert load_validator().main(["--strict", "check", "--historical",
                                  str(_legacy_file(tmp_path))], root=family_tree) == 3
    out = capsys.readouterr().out
    assert "legacy-protocol-deprecated" not in out and "ERROR [" not in out


# --------------------------------------------------------------------------
# E11: protocol selection, in its order.
# --------------------------------------------------------------------------

def select(context, producer, consumer, statuses=None, rejected_under=None,
           attempt=None):
    inputs = {"selection_producer": producer, "selection_consumer": consumer}
    if rejected_under is not None or attempt is not None:
        inputs["rejected_under"] = rejected_under
        inputs["selection_attempt"] = attempt
    environment = {"registry_status": statuses} if statuses else None
    return _run(context, "selection", inputs, environment)


def test_a_matched_rehearsal_pair_with_no_bundle_is_accepted(context):
    outcome = select(context, *pair())
    assert _verdict(outcome) == ("accept", None, ())
    assert outcome.derived == {}


def test_a_rehearsal_replacement_selection_reads_no_status(context):
    outcome = select(context, *pair(bundle=BUNDLE))
    assert outcome.outcome == "accept"
    assert outcome.status_read is False
    assert tuple(outcome.statuses_read) == ()


@pytest.mark.parametrize("producer_mode, consumer_mode", [("active", "active"),
                                                          ("active", "rehearsal"),
                                                          ("rehearsal", "active")])
def test_a_null_bundle_is_legal_only_in_rehearsal(context, producer_mode, consumer_mode):
    producer = selection("producer", mode=producer_mode)
    consumer = selection("consumer", mode=consumer_mode)
    outcome = select(context, producer, consumer,
                     {REPLACEMENT: "admission_eligible", LEGACY: "in_use"})
    assert _verdict(outcome) == ("refuse", "selection_malformed", ())


@pytest.mark.parametrize("mutate", [
    lambda s: s.update(unexpected="member"),
    lambda s: s.pop("corpus_index_sha256"),
    lambda s: s.pop("provider_bundle"),
    lambda s: s.update(kind="xfactory_council_protocol_selection_v2"),
    lambda s: s.update(schema_version=2),
    lambda s: s.update(mode="dormant"),
    lambda s: s.update(side="both"),
    lambda s: s.update(provider_commit=SHA[:12]),
    lambda s: s.update(provider_commit=SHA.upper()),
    lambda s: s.update(provider_bundle="v4.1"),
    lambda s: s.update(corpus_index_sha256="cd" * 32),
    lambda s: s.update(protocol=""),
    lambda s: s.update(protocol="xfc\nresolved"),
])
def test_a_selection_that_breaks_its_schema_is_malformed(context, mutate):
    producer, consumer = pair()
    mutate(producer)
    assert _verdict(select(context, producer, consumer)) == (
        "refuse", "selection_malformed", ())


def test_a_selection_presented_for_the_other_side_is_malformed(context):
    """The record handed in as the producer's names the consumer: no pair."""
    assert _verdict(select(context, selection("consumer"), selection("consumer"))) == (
        "refuse", "selection_malformed", ())
    assert _verdict(select(context, selection("producer"), selection("producer"))) == (
        "refuse", "selection_malformed", ())


def test_an_unregistered_protocol_is_unknown(context):
    producer, consumer = pair(protocol="xfc-resolved-council-2")
    assert _verdict(select(context, producer, consumer)) == ("refuse", "protocol_unknown", ())


@pytest.mark.parametrize("status, verdict", [
    ("available", ("refuse", "replacement_not_admission_eligible", ())),
    ("admission_eligible", ("accept", None, ())),
])
def test_an_active_replacement_selection_needs_admission_eligibility(context, status, verdict):
    outcome = select(context, *pair(mode="active", bundle=BUNDLE), {REPLACEMENT: status})
    assert _verdict(outcome) == verdict
    assert REPLACEMENT in outcome.statuses_read


def test_a_rehearsal_replacement_selection_is_legal_before_the_major(context):
    outcome = select(context, *pair(bundle=BUNDLE), {REPLACEMENT: "available"})
    assert _verdict(outcome) == ("accept", None, ())


@pytest.mark.parametrize("mode", ["rehearsal", "active"])
@pytest.mark.parametrize("status, verdict", [
    ("in_use", ("accept", None, ())),
    ("deprecated", ("accept", None, ())),
    ("historical_only", ("refuse", "legacy_protocol_refused", ())),
])
def test_a_legacy_selection_is_refused_in_either_mode_once_historical_only(
        context, mode, status, verdict):
    """N17: refused in either mode, not only when active."""
    outcome = select(context, *pair(mode=mode, protocol=LEGACY, bundle=BUNDLE),
                     {LEGACY: status})
    assert _verdict(outcome) == verdict
    assert LEGACY in outcome.statuses_read


@pytest.mark.parametrize("member, value", [
    ("mode", "active"),
    ("protocol", LEGACY),
    ("provider_commit", OTHER_SHA),
    ("provider_bundle", "contract-v4.2"),
    ("corpus_index_sha256", OTHER_INDEX_SHA),
])
def test_the_pair_is_matched_on_all_five_members(context, member, value):
    producer, consumer = pair(bundle=BUNDLE)
    consumer[member] = value
    statuses = {REPLACEMENT: "admission_eligible", LEGACY: "in_use"}
    assert _verdict(select(context, producer, consumer, statuses)) == (
        "refuse", "pair_mismatched", ())


def test_a_null_bundle_against_a_named_bundle_is_mismatched(context):
    producer, consumer = selection("producer"), selection("consumer", bundle=BUNDLE)
    assert _verdict(select(context, producer, consumer)) == (
        "refuse", "pair_mismatched", ())


# Multi-defect selections pin the order. Steps 1 to 3 run over every selection
# in the vector before the next step begins: the producer's, the consumer's,
# then the later attempt's.

def test_malformed_before_unknown_across_the_two_sides(context):
    producer = selection("producer", protocol="xfc-resolved-council-2")
    consumer = selection("consumer")
    consumer.pop("mode")
    assert _verdict(select(context, producer, consumer)) == (
        "refuse", "selection_malformed", ())


def test_unknown_before_eligibility(context):
    producer = selection("producer", mode="active", bundle=BUNDLE)
    consumer = selection("consumer", mode="active", bundle=BUNDLE,
                         protocol="xfc-resolved-council-2")
    assert _verdict(select(context, producer, consumer, {REPLACEMENT: "available"})) == (
        "refuse", "protocol_unknown", ())


def test_eligibility_before_the_pair(context):
    producer = selection("producer", mode="active", bundle=BUNDLE)
    consumer = selection("consumer", mode="rehearsal", bundle=BUNDLE)
    assert _verdict(select(context, producer, consumer, {REPLACEMENT: "available"})) == (
        "refuse", "replacement_not_admission_eligible", ())


def test_the_pair_before_the_fallback(context):
    producer, consumer = pair(bundle=BUNDLE)
    consumer["corpus_index_sha256"] = OTHER_INDEX_SHA
    outcome = select(context, producer, consumer, {LEGACY: "in_use"},
                     rejected_under=REPLACEMENT,
                     attempt=selection("consumer", protocol=LEGACY, bundle=BUNDLE))
    assert _verdict(outcome) == ("refuse", "pair_mismatched", ())


# rejected_without_fallback: a refusal under the selected protocol never selects
# another protocol.

def test_a_later_attempt_naming_another_protocol_is_refused(context):
    outcome = select(context, *pair(bundle=BUNDLE), {LEGACY: "in_use"},
                     rejected_under=REPLACEMENT,
                     attempt=selection("consumer", protocol=LEGACY, bundle=BUNDLE))
    assert _verdict(outcome) == ("refuse", "rejected_without_fallback", ())


def test_a_later_attempt_naming_the_same_protocol_is_no_fallback(context):
    outcome = select(context, *pair(bundle=BUNDLE), rejected_under=REPLACEMENT,
                     attempt=selection("consumer", bundle=BUNDLE))
    assert _verdict(outcome) == ("accept", None, ())


def test_a_fallback_from_legacy_to_the_replacement_is_refused_too(context):
    statuses = {LEGACY: "in_use"}
    outcome = select(context, *pair(mode="active", protocol=LEGACY, bundle=BUNDLE),
                     statuses, rejected_under=LEGACY,
                     attempt=selection("producer", bundle=BUNDLE))
    assert _verdict(outcome) == ("refuse", "rejected_without_fallback", ())


def test_the_attempt_is_itself_checked_first(context):
    attempt = selection("consumer", protocol=LEGACY, bundle=BUNDLE)
    attempt.pop("side")
    outcome = select(context, *pair(bundle=BUNDLE), rejected_under=REPLACEMENT,
                     attempt=attempt)
    assert _verdict(outcome) == ("refuse", "selection_malformed", ())


@pytest.mark.parametrize("inputs", [
    {"selection_producer": selection("producer")},
    {"selection_producer": selection("producer"), "selection_consumer": selection("consumer"),
     "rejected_under": REPLACEMENT},
    {"selection_producer": selection("producer"), "selection_consumer": selection("consumer"),
     "selection_attempt": selection("consumer")},
    {"selection_producer": selection("producer"), "selection_consumer": selection("consumer"),
     "rejected_under": "xfc-resolved-council-2", "selection_attempt": selection("consumer")},
    {"selection_producer": selection("producer"), "selection_consumer": selection("consumer"),
     "selected_protocol": None},
])
def test_a_selection_vector_takes_exactly_its_inputs(context, inputs):
    with pytest.raises(corpus.VectorInputError):
        _run(context, "selection", inputs)


def test_a_selection_vector_that_reads_a_status_without_its_override_is_flagged(family_tree):
    """U4 for the replacement's status: the corpus names the entry whose status
    the outcome read, not only the legacy entry."""
    conformance = family_tree / FAMILY_REL / "conformance"
    vector = _vector("selection", {"selection_producer": selection(
        "producer", mode="active", bundle=BUNDLE), "selection_consumer": selection(
        "consumer", mode="active", bundle=BUNDLE)}, {"registry_status": {LEGACY: "in_use"}})
    vector["case_id"] = "probe-replacement-status-read"
    vector["expected"].update(outcome="refuse", refusal="replacement_not_admission_eligible")
    path = conformance / "vectors" / "migration" / f"{vector['case_id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(corpus.dump_json(vector))
    generate.generate(family_tree)
    report = corpus.check_corpus(family_tree)
    missing = [f for f in report.findings
               if f.code == "council-convening-vector-registry-status-missing"]
    assert len(missing) == 1 and vector["case_id"] in missing[0].message


# --------------------------------------------------------------------------
# E12: activation evidence, per act, in the activation order.
# --------------------------------------------------------------------------

ACTS = ("pause", "drain", "switch", "rehearsal", "activation", "rollback", "resume")

#: Each act's required members (data-model E12), beside `act`, `schema_version`
#: and `kind`. A matched rehearsal also needs `intake`.
REQUIRED = {
    "pause": ["recorded_at", "provider", "owner_word"],
    "drain": ["recorded_at", "provider", "intake", "in_flight"],
    "switch": ["recorded_at", "provider", "owner_word", "intake", "producer", "consumer"],
    "rehearsal": ["recorded_at", "provider", "intake", "producer", "consumer", "rehearsal"],
    "activation": ["recorded_at", "provider", "owner_word", "intake", "producer",
                   "consumer", "rehearsal_ref", "binding_refs"],
    "rollback": ["recorded_at", "provider", "owner_word", "intake", "producer",
                 "consumer", "rollback"],
    "resume": ["recorded_at", "provider", "owner_word", "producer", "consumer",
               "rehearsal_ref", "binding_refs"],
}


def _case(context, act):
    if act in ("activation", "resume"):
        record, bindings, text = activation_case(act)
        return activate(context, record, bindings, text)
    return activate(context, evidence(act))


@pytest.mark.parametrize("act", ACTS)
def test_a_complete_record_of_each_act_is_accepted(context, act):
    assert _verdict(_case(context, act)) == ("accept", None, ())


def test_a_dormant_rehearsal_needs_no_intake(context):
    record = rehearsal_record(mode="dormant")
    assert "intake" not in record
    assert _verdict(activate(context, record)) == ("accept", None, ())


def test_no_activation_record_reads_a_registry_status(context):
    record, bindings, text = activation_case()
    outcome = activate(context, record, bindings, text)
    assert outcome.status_read is False and tuple(outcome.statuses_read) == ()


# Step 1: activation_evidence_malformed.

@pytest.mark.parametrize("mutate", [
    lambda r: r.update(unexpected="member"),
    lambda r: r.update(act="activate"),
    lambda r: r.pop("act"),
    lambda r: r.update(kind="xfactory_council_activation_evidence_v2"),
    lambda r: r.update(recorded_at="2026-10-09 00:00:00Z"),
    lambda r: r["provider"].update(commit="main"),
    lambda r: r["provider"].pop("corpus_index_sha256"),
    lambda r: r["owner_word"].pop("verbatim"),
    lambda r: r.update(binding_refs=[]),
    lambda r: r.update(binding_refs=["council-1-commission", "council-1-commission"]),
    lambda r: r.update(binding_refs=[f"b-{n}" for n in range(17)]),
    lambda r: r.update(rehearsal_ref="cd" * 32),
    lambda r: r["producer"]["selection"].update(side="consumer"),
    lambda r: r["consumer"]["selection"].update(provider_bundle=None),
    lambda r: r["producer"].update(revision="HEAD"),
])
def test_a_record_that_breaks_its_schema_is_malformed(context, mutate):
    record, bindings, text = activation_case()
    mutate(record)
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_malformed", ())


@pytest.mark.parametrize("member", ["broker", "broker_capability"])
def test_an_activation_record_carries_no_broker_state_of_its_own(context, member):
    """The broker's one source of truth is each binding's `broker` member."""
    record, bindings, text = activation_case()
    record[member] = {"broker_ref": "broker-0001", "capability_verified": True,
                      "evidence_ref": "broker-evidence-0001"}
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_malformed", ())


@pytest.mark.parametrize("act, foreign", [
    ("pause", "intake"), ("pause", "producer"), ("drain", "owner_word"),
    ("switch", "rehearsal_ref"), ("rehearsal", "owner_word"),
    ("activation", "in_flight"), ("activation", "rollback"),
    ("rollback", "binding_refs"), ("rollback", "rehearsal_ref"),
    ("resume", "intake"),
])
def test_a_member_foreign_to_the_act_is_malformed(context, act, foreign):
    source = {"intake": INTAKE, "producer": side("producer"), "owner_word": OWNER_WORD,
              "rehearsal_ref": INDEX_SHA, "in_flight": {"disposition": "drained",
                                                         "convening_ids": []},
              "rollback": {"new_records_retained": True}, "binding_refs": ["b-1"]}
    if act in ("activation", "resume"):
        record, bindings, text = activation_case(act)
    else:
        record, bindings, text = evidence(act), None, None
    record[foreign] = copy.deepcopy(source[foreign])
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_malformed", ())


# Step 2: activation_evidence_incomplete.

@pytest.mark.parametrize("act, member", [(act, member) for act in ACTS
                                         for member in REQUIRED[act]])
def test_each_acts_required_members(context, act, member):
    if act in ("activation", "resume"):
        record, bindings, text = activation_case(act)
    else:
        record, bindings, text = evidence(act), None, None
    del record[member]
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_incomplete", ())


@pytest.mark.parametrize("member", ["restored_producer", "restored_consumer",
                                    "new_records_retained", "new_records_protocol"])
def test_each_rollback_member_is_required(context, member):
    record = evidence("rollback")
    del record["rollback"][member]
    assert _verdict(activate(context, record)) == (
        "refuse", "activation_evidence_incomplete", ())


def test_a_rollback_that_drops_the_new_records_is_incomplete(context):
    record = evidence("rollback")
    record["rollback"]["new_records_retained"] = False
    assert _verdict(activate(context, record)) == (
        "refuse", "activation_evidence_incomplete", ())


def test_a_rollback_needs_no_binding_refs_and_no_rehearsal(context):
    record = evidence("rollback")
    assert "binding_refs" not in record and "rehearsal_ref" not in record
    assert _verdict(activate(context, record)) == ("accept", None, ())


# The backing rehearsal, found through rehearsal_ref in inputs.rehearsal.

@pytest.mark.parametrize("act", ["activation", "resume"])
def test_the_rehearsal_ref_is_the_hash_of_the_exact_text(context, act):
    record, bindings, text = activation_case(act)
    assert record["rehearsal_ref"] == ref_of(text)
    respaced = json.dumps(json.loads(text), indent=1, sort_keys=True) + "\n"
    assert json.loads(respaced) == json.loads(text) and respaced != text
    assert _verdict(activate(context, record, bindings, respaced)) == (
        "refuse", "activation_evidence_incomplete", ())


@pytest.mark.parametrize("rehearsal", [
    rehearsal_record(outcome="fail"),
    rehearsal_record(mode="dormant"),
    {**rehearsal_record(), "act": "switch"},
    rehearsal_record(provider={**PROVIDER, "commit": OTHER_SHA}),
    rehearsal_record(provider={**PROVIDER, "bundle": "contract-v4.2"}),
    rehearsal_record(provider={**PROVIDER, "corpus_index_sha256": OTHER_INDEX_SHA}),
    rehearsal_record(protocol=LEGACY),
    rehearsal_record(commit=OTHER_SHA),
    rehearsal_record(bundle=None),
    rehearsal_record(index=OTHER_INDEX_SHA),
])
def test_activation_needs_a_passing_matched_rehearsal_with_its_values(context, rehearsal):
    """A failed, dormant, or differently pinned rehearsal backs no activation
    (R4-M5): its provider and its matched selection values must be the
    activation's."""
    record, bindings, _ = activation_case()
    text = rehearsal_text(rehearsal)
    record["rehearsal_ref"] = ref_of(text)
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_incomplete", ())


def test_a_rehearsal_whose_own_pair_is_mismatched_backs_nothing(context):
    rehearsal = rehearsal_record()
    rehearsal["consumer"]["selection"]["corpus_index_sha256"] = OTHER_INDEX_SHA
    record, bindings, _ = activation_case()
    text = rehearsal_text(rehearsal)
    record["rehearsal_ref"] = ref_of(text)
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_incomplete", ())


@pytest.mark.parametrize("text", ["{not json\n", "[]\n", "null\n"])
def test_a_rehearsal_text_that_is_not_a_record_backs_nothing(context, text):
    record, bindings, _ = activation_case()
    record["rehearsal_ref"] = ref_of(text)
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_incomplete", ())


def test_the_rehearsal_runs_in_rehearsal_mode_and_the_activation_in_active(context):
    """The one matched value a rehearsal cannot share with its activation."""
    record, bindings, text = activation_case()
    assert record["producer"]["selection"]["mode"] == "active"
    assert json.loads(text)["producer"]["selection"]["mode"] == "rehearsal"
    assert _verdict(activate(context, record, bindings, text)) == ("accept", None, ())


# The binding set, under Brett Heap's 025 ruling (A): one binding per seat.

@pytest.mark.parametrize("seats", [
    (MERGE_READINESS_SEATS,),
    (GATE_RULES_SEATS,),
    (MERGE_READINESS_SEATS, GATE_RULES_SEATS),
], ids=["merge-readiness", "gate-rules", "both-councils"])
def test_a_per_seat_binding_set_listed_in_full_is_accepted(context, seats):
    record, bindings, text = activation_case(seats=seats)
    assert len(record["binding_refs"]) == len(bindings) == sum(1 + len(s) for s in seats)
    assert _verdict(activate(context, record, bindings, text)) == ("accept", None, ())


def test_the_binding_refs_compare_as_a_set(context):
    record, bindings, text = activation_case()
    record["binding_refs"] = list(reversed(record["binding_refs"]))
    assert _verdict(activate(context, record, bindings, text)) == ("accept", None, ())


@pytest.mark.parametrize("omitted", ["council-1-commission",
                                     "council-1-seat-company-policy-lead"])
def test_an_omitted_seat_binding_is_incomplete(context, omitted):
    record, bindings, text = activation_case()
    record["binding_refs"].remove(omitted)
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_incomplete", ())


def test_a_binding_the_consumer_does_not_configure_is_unresolved(context):
    record, bindings, text = activation_case()
    record["binding_refs"].append("council-1-seat-lead-architect")
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "binding_unresolved", ())


@pytest.mark.parametrize("verified, evidence_ref", [(False, "broker-evidence-0001"),
                                                    (True, None), (False, None)])
def test_one_unverified_seat_broker_parks_the_whole_activation(context, verified, evidence_ref):
    record, bindings, text = activation_case()
    seat = next(b for b in bindings if b["binding_id"] == "council-1-seat-lead-security")
    seat["broker"].update(capability_verified=verified, evidence_ref=evidence_ref)
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "broker_capability_insufficient", ())


@pytest.mark.parametrize("act", ["activation", "resume"])
def test_resume_is_held_to_the_binding_set_too(context, act):
    record, bindings, text = activation_case(act)
    bindings[0]["broker"]["capability_verified"] = False
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "broker_capability_insufficient", ())


def test_the_binding_refs_cap_holds_the_estate_and_refuses_a_seventeenth(context):
    """E12 bounds `binding_refs` at 16. Per-seat, the estate's two councils need
    12 (two commission bindings and ten seat bindings); a seventeenth binding is
    refused as malformed, so a council roster that outgrows the cap is a
    governed contract change, not a silent truncation."""
    assert len(per_seat_bindings(MERGE_READINESS_SEATS, GATE_RULES_SEATS)) == 12
    fifteen = [f"seat-{n:02d}" for n in range(15)]
    record, bindings, text = activation_case(seats=(fifteen,))
    assert len(bindings) == 16
    assert _verdict(activate(context, record, bindings, text)) == ("accept", None, ())
    record, bindings, text = activation_case(seats=(fifteen + ["seat-15"],))
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_malformed", ())


# Multi-defect activations pin the order.

def test_incomplete_before_unresolved(context):
    record, bindings, text = activation_case()
    record["binding_refs"].remove("council-1-seat-lead-quality")
    record["binding_refs"].append("council-9-seat-unknown")
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_incomplete", ())


def test_the_binding_refs_are_read_entry_by_entry_in_order(context):
    """Step 3 runs per entry: an unverified broker on the first entry is named
    before an unresolved later entry."""
    record, bindings, text = activation_case()
    first = record["binding_refs"][0]
    next(b for b in bindings if b["binding_id"] == first)["broker"]["evidence_ref"] = None
    record["binding_refs"].append("council-9-seat-unknown")
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "broker_capability_insufficient", ())
    record["binding_refs"] = ["council-9-seat-unknown", *record["binding_refs"][:-1]]
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "binding_unresolved", ())


def test_broker_capability_before_the_pair(context):
    record, bindings, text = activation_case()
    record["consumer"]["selection"]["mode"] = "rehearsal"
    bindings[1]["broker"]["capability_verified"] = False
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "broker_capability_insufficient", ())


# Step 4: pair_mismatched.

MATCHED_MEMBERS = ["mode", "protocol", "provider_commit", "provider_bundle",
                   "corpus_index_sha256"]


def _stray(record: dict, member: str) -> None:
    """Move the consumer's selection off the producer's on one matched member."""
    selected = record["consumer"]["selection"]
    selected[member] = {
        "mode": "active" if selected["mode"] == "rehearsal" else "rehearsal",
        "protocol": REPLACEMENT if selected["protocol"] == LEGACY else LEGACY,
        "provider_commit": OTHER_SHA,
        "provider_bundle": "contract-v4.2",
        "corpus_index_sha256": OTHER_INDEX_SHA,
    }[member]


@pytest.mark.parametrize("act", ["switch", "rehearsal", "rollback"])
@pytest.mark.parametrize("member", MATCHED_MEMBERS)
def test_the_two_sides_selections_must_match(context, act, member):
    record = evidence(act)
    _stray(record, member)
    assert _verdict(activate(context, record)) == ("refuse", "pair_mismatched", ())


@pytest.mark.parametrize("act", ["activation", "resume"])
def test_an_activation_pair_split_on_mode_is_mismatched(context, act):
    record, bindings, text = activation_case(act)
    _stray(record, "mode")
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "pair_mismatched", ())


@pytest.mark.parametrize("act", ["activation", "resume"])
@pytest.mark.parametrize("member", MATCHED_MEMBERS[1:])
def test_an_activation_side_that_strays_from_its_rehearsal_is_incomplete(
        context, act, member):
    """The backing rehearsal is itself a matched pair, so a side that differs
    from the other on any matched value but `mode` also differs from the
    rehearsal: step 2 names it, before the pair comparison of step 4."""
    record, bindings, text = activation_case(act)
    _stray(record, member)
    assert _verdict(activate(context, record, bindings, text)) == (
        "refuse", "activation_evidence_incomplete", ())


# The ruled rollback: back to the Release A pins, legacy reselected there.

def test_a_rollback_after_activation_restores_the_release_a_pins(context):
    record = evidence("rollback")
    for role in ("producer", "consumer"):
        restored = record[role]["selection"]
        assert (restored["protocol"], restored["mode"], restored["provider_commit"],
                restored["provider_bundle"]) == (LEGACY, "active", RELEASE_A_SHA, RELEASE_A)
    assert record["provider"]["commit"] == RELEASE_A_SHA
    assert _verdict(activate(context, record)) == ("accept", None, ())


@pytest.mark.parametrize("statuses, verdict", [
    ({LEGACY: "deprecated", REPLACEMENT: "available"}, ("accept", None, ())),
    ({LEGACY: "historical_only", REPLACEMENT: "admission_eligible"},
     ("refuse", "legacy_protocol_refused", ())),
], ids=["at-release-a", "past-the-major"])
def test_the_restored_legacy_pair_is_selectable_only_at_release_a(context, statuses, verdict):
    """The restored pair is judged as selections at the pin it names: at the
    Release A pin legacy is `deprecated` and selectable; at the removal major's
    pin or later it is `historical_only`, and the same pair is refused."""
    assert _verdict(select(context, *pair(**RESTORED), statuses)) == verdict


# Step 5: historical_reinterpretation_refused.

def test_retained_new_records_stay_under_the_replacement(context):
    record = evidence("rollback")
    record["rollback"]["new_records_protocol"] = LEGACY
    assert _verdict(activate(context, record)) == (
        "refuse", "historical_reinterpretation_refused", ())


def test_an_unknown_new_records_protocol_is_reinterpretation_too(context):
    record = evidence("rollback")
    record["rollback"]["new_records_protocol"] = "xfc-resolved-council-2"
    assert _verdict(activate(context, record)) == (
        "refuse", "historical_reinterpretation_refused", ())


def test_dropped_records_before_reinterpretation(context):
    record = evidence("rollback")
    record["rollback"].update(new_records_retained=False, new_records_protocol=LEGACY)
    assert _verdict(activate(context, record)) == (
        "refuse", "activation_evidence_incomplete", ())


def test_a_mismatched_restored_pair_before_reinterpretation(context):
    record = evidence("rollback")
    record["consumer"]["selection"]["provider_commit"] = OTHER_SHA
    record["rollback"]["new_records_protocol"] = LEGACY
    assert _verdict(activate(context, record)) == ("refuse", "pair_mismatched", ())


# The activation vector's inputs.

@pytest.mark.parametrize("act", ["activation", "resume"])
@pytest.mark.parametrize("drop", ["bindings", "rehearsal"])
def test_an_activation_vector_carries_its_bindings_and_rehearsal(context, act, drop):
    record, bindings, text = activation_case(act)
    inputs = {"record": record, "bindings": bindings, "rehearsal": text}
    del inputs[drop]
    with pytest.raises(corpus.VectorInputError):
        _run(context, "activation", inputs)


@pytest.mark.parametrize("act", ["pause", "rollback"])
def test_another_act_carries_neither(context, act):
    with pytest.raises(corpus.VectorInputError):
        _run(context, "activation", {"record": evidence(act), "bindings": [binding("b")]})


@pytest.mark.parametrize("mutate", [
    pytest.param(lambda bindings: bindings.append(copy.deepcopy(bindings[0])),
                 id="repeated-binding-id"),
    pytest.param(lambda bindings: bindings[0].pop("broker"), id="no-broker"),
    pytest.param(lambda bindings: bindings[0].update(instantiation_stub=True), id="stub"),
    pytest.param(lambda bindings: bindings.clear(), id="empty"),
    # From Phase 5 a configured binding is a whole E10 instance: each of these
    # fails producer-binding.schema.yaml, so the input is not a live binding.
    pytest.param(lambda bindings: bindings[0].pop("issuer"), id="no-issuer"),
    pytest.param(lambda bindings: bindings[0]["permitted_workflows"].clear(),
                 id="no-permitted-workflow"),
    pytest.param(lambda bindings: bindings[1]["permitted_workflows"][0].update(
        workflow_revision_rule="equals_governed_revision"), id="seat-paired-with-commission-rule"),
    pytest.param(lambda bindings: bindings[0].update(repository_id=0), id="repository-id-zero"),
    pytest.param(lambda bindings: bindings[0].update(notes="x"), id="unknown-member"),
])
def test_the_configured_binding_set_is_a_set_of_live_bindings(context, mutate):
    record, bindings, text = activation_case()
    mutate(bindings)
    with pytest.raises(corpus.VectorInputError):
        activate(context, record, bindings, text)


# --------------------------------------------------------------------------
# The corpus at the commit.
# --------------------------------------------------------------------------

def _index() -> dict:
    return json.loads(INDEX.read_text(encoding="utf-8"))


def _migration_rows() -> list[dict]:
    return [row for row in _index()["cases"] if row["area"] == "migration"]


def test_the_coverage_floor_is_full_at_phase_6():
    """R16 and T058: from Phase 6 the floor is the full FR-001 to FR-012 and
    SC-001 to SC-003, in that order, and every member is cited by a vector."""
    floor = _index()["coverage_floor"]
    assert floor == list(generate.COVERAGE_FLOOR) == FULL_FLOOR
    cited = {r for row in _index()["cases"] for r in row["requirement_ids"]}
    assert set(FULL_FLOOR) <= cited


def test_the_vocabulary_holds_the_phase_6_codes(schemas):
    refusals = schemas.enum("refusal_code")
    assert refusals[-len(PHASE_6_REFUSALS):] == PHASE_6_REFUSALS
    assert schemas.enum("finding_code") == ["legacy_protocol_routed",
                                            "legacy_protocol_deprecated"]


def test_the_migration_vectors_probe_every_phase_6_code():
    probed = {row["expected"]["refusal"] for row in _migration_rows()}
    assert set(PHASE_6_REFUSALS) <= probed
    assert {"binding_unresolved", "broker_capability_insufficient",
            "legacy_protocol_refused"} <= probed
    findings = {f for row in _migration_rows() for f in row["expected"]["findings"]}
    assert "legacy_protocol_deprecated" in findings


def test_the_migration_vectors_cover_every_boundary_and_act():
    rows = _migration_rows()
    assert {row["boundary"] for row in rows} == {"classification", "historical",
                                                 "selection", "activation"}
    acts = set()
    for row in rows:
        if row["boundary"] == "activation" and row["expected"]["outcome"] == "accept":
            vector = json.loads((INDEX.parent / row["path"]).read_text(encoding="utf-8"))
            acts.add(vector["inputs"]["record"]["act"])
    assert acts == set(ACTS)


def test_every_effects_row_has_a_migration_vector_under_each_status():
    cells = set()
    for row in _migration_rows():
        if row["boundary"] != "classification":
            continue
        vector = json.loads((INDEX.parent / row["path"]).read_text(encoding="utf-8"))
        status = vector["environment"]["registry_status"][LEGACY]
        kind = "legacy" if vector["inputs"]["record"].get("protocol") != REPLACEMENT \
            else "replacement"
        cells.add((vector["inputs"]["selected_protocol"], status, kind))
        assert (row["expected"]["outcome"], row["expected"]["refusal"],
                tuple(row["expected"]["findings"])) == EFFECTS[
                    (vector["inputs"]["selected_protocol"], status, kind)]
    assert cells == set(EFFECTS)


def test_activation_and_resume_vectors_are_the_consumers():
    """The consumer holds the configured binding set, so the vectors that read
    it apply to the consumer; every other migration vector is shared."""
    for row in _migration_rows():
        vector = json.loads((INDEX.parent / row["path"]).read_text(encoding="utf-8"))
        record = vector["inputs"].get("record")
        if row["boundary"] == "activation" and isinstance(record, dict) and \
                record.get("act") in ("activation", "resume"):
            assert row["applies_to"] == ["consumer"], row["case_id"]
        else:
            assert row["applies_to"] == ["producer", "consumer"], row["case_id"]


def test_every_configured_binding_passes_e10_offline(tmp_path):
    """The bindings an activation vector configures are bindings the `binding`
    boundary accepts offline: E10 steps 1 to 6 (Phase 5's `check_offline`),
    against the corpus's frozen identity map, never the live one. So an
    activation's refusal is always the activation order's, never a stray E10
    defect in its inputs."""
    from scripts.council_convening import binding as e10

    fixture = json.loads((INDEX.parent / "fixtures" / "repository-identity.json")
                         .read_text(encoding="utf-8"))
    root = e10.materialize_identity({"state": "text", "text": fixture["text"]}, tmp_path)
    checked = 0
    for row in _migration_rows():
        vector = json.loads((INDEX.parent / row["path"]).read_text(encoding="utf-8"))
        for configured in corpus.join_parts(vector["inputs"].get("bindings", [])):
            e10.check_offline(configured, identity_root=root)
            checked += 1
    # 36 activation and resume vectors carry a configured set: 212 bindings.
    assert checked == 212


def test_every_migration_vector_cites_fr_011_or_fr_012():
    for row in _migration_rows():
        assert {"FR-011", "FR-012"} & set(row["requirement_ids"]), row["case_id"]


def test_the_landed_corpus_adjudicates_with_no_findings():
    report = corpus.check_corpus()
    assert report.findings == []
    assert report.adjudicated == (report.vectors, report.vectors)
