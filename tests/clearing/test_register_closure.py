"""The permitted-operations register is CLOSED, and closure shrinks but never grows.

The ratified requirement makes adding an operation a governed contract change
with a spec delta and a reviewer. JSON Schema cannot express that — it constrains
a document, not a decision — so the enforcement is the validator's frozen member
set, and THIS is the test that proves the refusal fires rather than merely
existing.

WHAT THE MECHANISM IS WORTH, said here as well as in the register: this file, the
validator and the register share a repository with the changes they police, so
one diff can edit every side. The refusal guarantees that an append cannot be
made SILENTLY. It is a tripwire backed by review of that diff, not an unforgeable
refusal, and describing it as one would be the overclaim the ratified
authoring-time guard requires be avoided.
"""

from __future__ import annotations

import copy

import yaml

from conftest import REGISTRY_INSTANCE, adjudicate

INSTANCE = yaml.safe_load(REGISTRY_INSTANCE.read_text(encoding="utf-8"))

#: The RATIFIED member set, held here as a frozen constant INDEPENDENTLY of the
#: validator's own. Two copies is deliberate: if the validator's set were the
#: only one, a diff that widened it would widen the test in the same motion and
#: nothing would go red.
RATIFIED = frozenset({"readiness-diagnostic"})


def test_the_shipped_instance_holds_exactly_the_ratified_set() -> None:
    members = {entry["operation_id"] for entry in INSTANCE["operations"]}
    assert members == RATIFIED, (
        f"the shipped register holds {sorted(members)}. Adding an operation is a "
        f"GOVERNED CONTRACT CHANGE with a spec delta and a reviewer — if this "
        f"assertion is failing because a member was added, the change that added "
        f"it is what needs a ratifier, not this line"
    )


def test_the_registry_declares_its_own_identity() -> None:
    assert INSTANCE["registry_id"] == "clearing-permitted-operations"
    assert INSTANCE["kind"] == "xfactory_clearing_permitted_operations_registry"
    assert INSTANCE["registry_version"] >= 1


def test_deliberation_is_refused_by_name(reader, registry_and_docs) -> None:
    """codexFactory #165's operation is the honest fixture for this refusal.

    The failure mode is never somebody adding an absurd operation. It is somebody
    adding a REASONABLE one — wanted, well-formed, and in the file rather than in
    a change.
    """
    doc = copy.deepcopy(INSTANCE)
    extra = copy.deepcopy(doc["operations"][0])
    extra["operation_id"] = "deliberation"
    doc["operations"].append(extra)
    findings = adjudicate(reader, registry_and_docs, {}, {}, doc, "probe")
    codes = reader.codes_of(findings.errors)
    assert "clearing-register-member-unratified" in codes, findings.errors
    assert any("deliberation" in line for line in findings.errors)
    assert any("GOVERNED CONTRACT CHANGE" in line for line in findings.errors)


def test_removing_a_member_does_not_refuse(reader, registry_and_docs) -> None:
    """CLOSURE SHRINKS. A retirement is lawful; an addition is not.

    The asymmetry matters: the ratified convergence model expects the estate's
    direct routes to retire into operations over time, and a rule that refused a
    shrinking set would fight the direction the contract wants to move in. The
    shipped instance has one member, so the shrunk case is the empty one — which
    the schema refuses by `minItems`, because a register with no members is not a
    closed set but an unrealized one. What this test asserts is that the CLOSURE
    rule stays silent about it: whatever refuses an empty register, it is not
    `clearing-register-member-unratified`.
    """
    doc = copy.deepcopy(INSTANCE)
    doc["operations"] = []
    findings = adjudicate(reader, registry_and_docs, {}, {}, doc, "probe")
    codes = reader.codes_of(findings.errors)
    assert "clearing-register-member-unratified" not in codes, findings.errors


def test_the_entry_declares_every_ratified_fact() -> None:
    """The ratified entry-declaration list, checked member by member.

    "Each entry SHALL declare its operation id, what the operation may do and
    what it may not, its class constraints (at minimum: whether it checks out
    code, whether it writes, whether it may reference secrets, and the token
    scopes its job carries), its required worker profile, the lanes — runner
    group and dispatch label — it may be dispatched to, its declared output
    schema, and whether it returns repository-affecting output."
    """
    entry = INSTANCE["operations"][0]
    assert entry["operation_id"] == "readiness-diagnostic"
    assert entry["permitted_semantics"]["may"], "no permitted semantics declared"
    assert entry["permitted_semantics"]["may_not"], (
        "an entry that lists only permissions describes a capability; the "
        "ratified requirement asks for a BOUND"
    )
    constraints = entry["class_constraints"]
    assert constraints["checks_out_code"] is False
    assert constraints["writes"] is False
    assert constraints["may_reference_secrets"] is False
    assert constraints["token_scopes"] == [], (
        "an EMPTY token-scope list is a stronger statement than the member's "
        "absence: the job token carries no scopes at all"
    )
    assert constraints["timeout_minutes"] >= 1
    assert entry["worker_profile"]
    assert entry["output_schema_ref"] == "contracts/clearing/operation-report.schema.yaml"
    assert entry["data_handling"]
    assert entry["repository_affecting_output"] is False, (
        "readiness-diagnostic returns EVIDENCE. An entry that declared a "
        "repository effect would need a hosted finalizer, which this slice "
        "deliberately does not ship"
    )


def test_both_ratified_lanes_are_declared_with_literal_group_and_label() -> None:
    """The GROUP is the boundary and the LABEL is the routing choice, and both
    are literal in the register so a request for a lane the entry does not permit
    is refusable BEFORE any runner is involved."""
    lanes = {lane["lane_key"]: lane for lane in INSTANCE["operations"][0]["lanes"]}
    assert set(lanes) == {"coding", "artifact"}
    assert lanes["coding"]["runner_group"] == "xfactory-execution-lane-workers"
    assert lanes["coding"]["dispatch_label"] == "host-coding-cpc-brett01"
    assert lanes["coding"]["expected_runner"] == "xfactory-coding-cpc-brett01"
    assert lanes["artifact"]["runner_group"] == "xfactory-artifact-workers"
    assert lanes["artifact"]["dispatch_label"] == "host-rider-cpc-brett01"
    assert lanes["artifact"]["expected_runner"] == "xfactory-artifact-cpc-brett01"


def test_a_read_only_entry_may_not_also_permit_writes(reader, registry_and_docs) -> None:
    doc = copy.deepcopy(INSTANCE)
    doc["operations"][0]["class_constraints"]["writes"] = True
    findings = adjudicate(reader, registry_and_docs, {}, {}, doc, "probe")
    assert "clearing-readonly-entry-claims-effect" in reader.codes_of(findings.errors), \
        findings.errors


def test_an_incomplete_entry_is_refused(reader, registry_and_docs) -> None:
    doc = copy.deepcopy(INSTANCE)
    doc["operations"][0].pop("worker_profile")
    findings = adjudicate(reader, registry_and_docs, {}, {}, doc, "probe")
    assert "clearing-register-entry-incomplete" in reader.codes_of(findings.errors), \
        findings.errors
