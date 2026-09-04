"""The operation report: composed evidence, name-allowlisted, and verdict-free.

Three ratified properties, and each is checked in the way the requirement's own
reasoning demands rather than in the way a schema happens to allow.
"""

from __future__ import annotations

import copy

import yaml

from conftest import EXAMPLES, FAMILY_DIR, adjudicate

SCHEMA = yaml.safe_load(
    (FAMILY_DIR / "operation-report.schema.yaml").read_text(encoding="utf-8"))
REPORT = yaml.safe_load(
    (EXAMPLES / "operation-report-both-lanes.example.yaml").read_text(encoding="utf-8"))

#: The ratified NAME ALLOWLIST, held here independently of both the schema and
#: the validator. Three copies is deliberate for the same reason the register's
#: member set is held twice: a widening that edited only one place would widen
#: the test in the same motion.
ALLOWLIST = {
    "RUNNER_NAME", "RUNNER_OS", "RUNNER_ARCH", "RUNNER_TEMP", "COMPUTERNAME",
    "USERNAME", "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS",
    "GITHUB_WORKSPACE",
}


def test_the_report_is_one_composed_record_across_both_lanes() -> None:
    """"one report of record per dispatch across however many lanes were
    probed", with per-lane facts as a KEYED COLLECTION.

    What the requirement forbids is "a report that exists only as scattered log
    lines a reader must reassemble" — so the test is that ONE record carries BOTH
    lanes, not that two lane records exist.
    """
    assert set(REPORT["lanes"]) == {"coding", "artifact"}
    assert REPORT["dispatch_id"]
    assert SCHEMA["properties"]["lanes"]["type"] == "object", (
        "an array of fragments would make 'one composed report' "
        "indistinguishable from 'several reports in one file'"
    )


def test_the_environment_echo_is_the_ratified_name_allowlist() -> None:
    names = set(SCHEMA["$defs"]["lane_report"]["properties"]["environment"]
                ["propertyNames"]["enum"])
    assert names == ALLOWLIST
    for lane in REPORT["lanes"].values():
        assert set(lane["environment"]) <= ALLOWLIST


def test_an_unallowlisted_variable_is_refused_even_when_unset(
        reader, registry_and_docs, entries) -> None:
    """The NAME is refused, not the value.

    The hazard is not that this run leaked a secret. It is a shape that PERMITS
    the name, because the day the variable is set is the day the log is public
    and nobody re-reads the allowlist.
    """
    doc = copy.deepcopy(REPORT)
    doc["lanes"]["coding"]["environment"]["AZURE_CLIENT_SECRET"] = "<unset>"
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-report-environment-not-allowlisted" in \
        reader.codes_of(findings.errors), findings.errors


def test_each_lane_reports_declared_group_and_label() -> None:
    """"the group and label MUST be reported as DECLARED rather than as observed
    group membership" — and the member name is where that is carried."""
    lane_shape = SCHEMA["$defs"]["lane_report"]
    assert "declared" in lane_shape["required"]
    declared = lane_shape["properties"]["declared"]
    assert set(declared["required"]) == {
        "runner_group", "dispatch_label", "expected_runner"}
    for lane in REPORT["lanes"].values():
        assert lane["declared"]["runner_group"]
        assert lane["declared"]["dispatch_label"]
        assert not any("observed" in name for name in lane)


def test_an_observed_group_member_is_refused(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(REPORT)
    doc["lanes"]["artifact"]["observed_runner_group"] = "xfactory-artifact-workers"
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-report-lane-reported-as-observed" in \
        reader.codes_of(findings.errors), findings.errors


def test_the_report_carries_no_verdict(reader, registry_and_docs, entries) -> None:
    """The report is EVIDENCE produced BY passing through the boundary; the
    awaited infrastructure-readiness result is a DECISION consulted BEFORE
    dispatch, and a verdict field would quietly promote one into the other."""
    doc = copy.deepcopy(REPORT)
    doc["readiness_verdict"] = "ready"
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-report-carries-a-verdict" in \
        reader.codes_of(findings.errors), findings.errors


def test_a_nested_verdict_is_refused_too(reader, registry_and_docs, entries) -> None:
    """The scan is not top-level only.

    A verdict tucked inside a lane would be exactly as much of a decision as one
    at the root, and rather more likely to survive review.
    """
    doc = copy.deepcopy(REPORT)
    doc["lanes"]["coding"]["eligibility"] = "eligible"
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-report-carries-a-verdict" in \
        reader.codes_of(findings.errors), findings.errors


def test_runner_identity_is_a_two_valued_comparison() -> None:
    """"A runner identity that does not match the expected identity SHALL FAIL
    the operation with the observed identity named, rather than proceeding
    against an unexpected host." The record must be able to say MISMATCH."""
    identity = SCHEMA["$defs"]["lane_report"]["properties"]["runner"]["properties"]["identity"]
    assert set(identity["enum"]) == {"CONFIRMED", "MISMATCH"}


def test_the_compute_round_trip_records_both_digests() -> None:
    """"the fixed-input digest computed on the host differs from the fixed
    expected digest → the operation MUST fail WITH BOTH VALUES RECORDED."

    A shape carrying only the check result could not evidence what disagreed.
    """
    compute = SCHEMA["$defs"]["lane_report"]["properties"]["compute"]
    assert {"sha256", "expected_sha256"} <= set(compute["required"])
    for lane in REPORT["lanes"].values():
        assert lane["compute"]["sha256"] == lane["compute"]["expected_sha256"]
        assert lane["compute"]["sha256_check"] == "PASS"


def test_the_report_names_the_claimed_operation_separately() -> None:
    """`operation` is the CLEARED one and may be null; `operation_claimed` is
    what was asked for. A report carrying only one of them could present a
    refused claim as a cleared one."""
    assert "operation_claimed" in SCHEMA["required"]
    assert "operation" not in SCHEMA["required"]
    assert REPORT["operation"] == REPORT["operation_claimed"] == "readiness-diagnostic"


def test_the_output_schema_the_register_declares_is_this_one() -> None:
    """The register's `output_schema_ref` must actually point at this shape, or
    a return would be validated against a file nobody ships."""
    registry = yaml.safe_load(
        (FAMILY_DIR / "permitted-operations.registry.yaml").read_text(encoding="utf-8"))
    entry = registry["operations"][0]
    assert entry["output_schema_ref"] == "contracts/clearing/operation-report.schema.yaml"
    assert (FAMILY_DIR.parent.parent / entry["output_schema_ref"]).is_file()
