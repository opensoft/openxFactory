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
#: nothing would go red. It is COPY TWO OF FIVE — the others are the validator's
#: constant, the register instance, the CI gate's literal member-count grep, and
#: the test in `test_clearing_gate_wiring.py` that pins that grep from a second
#: file. Do NOT import one from another; the independence is the control.
#:
#: `deliberation` joined on 2026-09-04 by `admit-deliberation-clearing-operation`
#: (ratified by Brett Heap, PR #645, merged `3cf917b7`) — register entry number
#: two.
RATIFIED = frozenset({"readiness-diagnostic", "deliberation"})


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


def test_the_registry_version_advanced_with_the_governed_addition() -> None:
    """The identity is a `const`; the VERSION is not, so it is on the author.

    A governed change to a CLOSED set that left the version at 1 would make two
    different registers indistinguishable by their own declaration — the
    identity test above only asserts `>= 1` and would pass over it in silence.
    Entry number two took it to 2 (`admit-deliberation-clearing-operation`, PR
    #645, merged `3cf917b7`), and the next governed addition takes it to 3.
    """
    assert INSTANCE["registry_version"] == 2, (
        "the shipped instance holds two ratified members; a governed change that "
        "moved the set and not the version publishes two different registers "
        "under one version number"
    )


def test_coding_is_refused_by_name(reader, registry_and_docs) -> None:
    """The next real later operation is the honest fixture for this refusal.

    The failure mode is never somebody adding an absurd operation. It is somebody
    adding a REASONABLE one — wanted, well-formed, and in the file rather than in
    a change.

    `coding` is that name now: `add-clearing-dispatch-boundary` design D11 names
    it as the next real later operation, and the estate already holds its lane
    and its grandfathered worker. `deliberation` held the role until 2026-09-04
    and vacated it by being RATIFIED, which is the only way to vacate it — and
    THE TEST'S NAME MOVED WITH ITS BODY, because a test whose name says one
    operation while its body builds another is the same defect as a fixture whose
    comment and bytes disagree.
    """
    doc = copy.deepcopy(INSTANCE)
    extra = copy.deepcopy(doc["operations"][0])
    extra["operation_id"] = "coding"
    doc["operations"].append(extra)
    findings = adjudicate(reader, registry_and_docs, {}, {}, doc, "probe")
    codes = reader.codes_of(findings.errors)
    assert "clearing-register-member-unratified" in codes, findings.errors
    assert any("coding" in line for line in findings.errors)
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


def test_entry_two_declares_every_ratified_fact() -> None:
    """The ENTRY-TWO twin, written out rather than parametrized.

    A test that only ever read `operations[0]` would pass over a malformed entry
    two in silence, which is the whole reason this exists as its own function.
    Every value below is fixed by the ratified requirement "deliberation is
    register entry number two and returns evidence only".
    """
    entry = next(e for e in INSTANCE["operations"]
                 if e["operation_id"] == "deliberation")
    assert entry["title"]
    assert entry["permitted_semantics"]["may"], "no permitted semantics declared"
    assert entry["permitted_semantics"]["may_not"], (
        "an entry that lists only permissions describes a capability; the "
        "ratified requirement asks for a BOUND"
    )
    constraints = entry["class_constraints"]
    assert constraints["checks_out_code"] is False
    assert constraints["writes"] is False
    assert constraints["may_reference_secrets"] is False
    assert constraints["token_scopes"] == ["actions:read"], (
        "EXACTLY the clearing side's own scoped, short-lived, READ-ONLY "
        "admission credential and nothing else. `metadata:read` is deliberately "
        "absent — on this provider it is the token's floor rather than a grant "
        "this entry makes — and adding it is an amendment to this entry by "
        "governed change, not a fix-up"
    )
    assert 1 <= constraints["timeout_minutes"] <= 1440, (
        "the ratified requirement says BOUNDED; a constraint with no "
        "representation cannot be checked"
    )
    assert entry["worker_profile"] == "council-deliberation-worker"
    assert entry["output_schema_ref"] == \
        "contracts/clearing/deliberation-return.schema.yaml", (
        "a return is validated against THIS value and never against a bundle's "
        "copy of it, and the declared schema is never a path a producing "
        "repository owns"
    )
    assert entry["data_handling"] == "internal-governance", (
        "STRICTER than entry one's `public_log_only`, which is what the register "
        "instance's own comment promised a bundle-carrying operation would "
        "declare"
    )
    assert entry["repository_affecting_output"] is False, (
        "the return is EVIDENCE. An entry that declared a repository effect "
        "would need a hosted finalizer, and giving it one is a change to this "
        "entry"
    )


def test_entry_two_declares_the_artifact_lane_and_only_the_artifact_lane() -> None:
    """ONE lane, and the four members are all literal.

    Entry one declares BOTH lanes, so no request can name a lane its operation
    does not permit. Entry two is the FIRST entry that permits one and refuses
    the other — which is what makes the refusal ground `lane_not_permitted`
    emittable at all, and why this entry admits it.
    """
    entry = next(e for e in INSTANCE["operations"]
                 if e["operation_id"] == "deliberation")
    lanes = {lane["lane_key"]: lane for lane in entry["lanes"]}
    assert set(lanes) == {"artifact"}, (
        "a coding-lane request for this operation is refused "
        "`clearing-lane-not-permitted` before any runner is selected; widening "
        "this list is a governed change to the entry"
    )
    assert lanes["artifact"]["runner_group"] == "xfactory-artifact-workers"
    assert lanes["artifact"]["dispatch_label"] == "host-rider-cpc-brett01"
    assert lanes["artifact"]["expected_runner"] == "xfactory-artifact-cpc-brett01"


def test_entry_one_is_not_widened_by_entry_twos_arrival() -> None:
    """The widening that is NOT happening, pinned so nobody performs it later.

    The ratified text says it in as many words: "THE EMPTY TOKEN-SCOPE LIST OF
    ENTRY NUMBER ONE IS NOT WIDENED BY THIS ENTRY AND SHALL NOT BE READ AS HAVING
    BEEN." Entry one's constraints bind entry one.
    """
    entry = next(e for e in INSTANCE["operations"]
                 if e["operation_id"] == "readiness-diagnostic")
    assert entry["class_constraints"]["token_scopes"] == []
    assert entry["data_handling"] == "public_log_only"
    assert {lane["lane_key"] for lane in entry["lanes"]} == {"coding", "artifact"}


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
