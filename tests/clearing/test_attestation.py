"""The single-door attestation, and the three findings it must keep apart.

The ratified text spends more words on this distinction than on any other in the
capability, and for a measurable reason: conflating a DARK LANE with a WIDENING
would have made the estate's first attestation red over two lanes that cannot
reach the host at all, and a control that is red for a safe condition is a
control that gets muted.
"""

from __future__ import annotations

import copy

import yaml

from conftest import EXAMPLES, FAMILY_DIR, adjudicate

SCHEMA = yaml.safe_load(
    (FAMILY_DIR / "single-door-attestation.schema.yaml").read_text(encoding="utf-8"))
POSITIVE = yaml.safe_load(
    (EXAMPLES / "single-door-attestation.example.yaml").read_text(encoding="utf-8"))


def test_the_finding_classes_are_exactly_three() -> None:
    assert set(SCHEMA["$defs"]["finding"]["properties"]["finding_class"]["enum"]) == {
        "widening", "dark_lane", "convergence_not_yet_reached"}


def test_the_expected_set_is_a_per_group_member_with_no_estate_wide_twin() -> None:
    """"THE EXPECTED ALLOWLIST SHALL BE COMPUTED PER GROUP, not once for the
    estate."

    Checked structurally: `expected_allowlist` is required INSIDE a group, and
    there is no top-level member of that name for a record to fall back on.
    """
    group = SCHEMA["$defs"]["group_attestation"]
    assert "expected_allowlist" in group["required"]
    assert "expected_repositories" in group["required"]
    assert "expected_allowlist" not in SCHEMA["properties"]


def test_the_positive_carries_all_three_classes() -> None:
    """The corpus shows the estate's real state, not a clean one.

    A packaged attestation with no findings would document the shape and none of
    the reasoning: the three classes exist precisely because the estate has all
    three conditions at once.
    """
    classes = {finding["finding_class"]
               for group in POSITIVE["groups"]
               for finding in group["findings"]}
    assert classes == {"widening", "dark_lane", "convergence_not_yet_reached"}


def test_every_finding_names_its_group_and_its_expected_set() -> None:
    """A finding without a group could not be acted on, because the set it
    diverges from is a per-group value."""
    for group in POSITIVE["groups"]:
        for finding in group["findings"]:
            assert finding["runner_group"] == group["runner_group"]
            assert "expected_set" in finding
            assert finding["detail"]


def test_an_admitted_repository_other_than_the_clearing_one_is_a_widening() -> None:
    """The measured residual the ruling closes, carried in the corpus.

    `opensoft/codexFactory` is admitted to the artifact group. That is why run
    33381257642 could queue for eighteen hours at all — the group admitted the
    repository and allowlisted only xFactory paths — and the attestation reports
    it as a widening of the same class as an unexpected path.
    """
    artifact = next(g for g in POSITIVE["groups"]
                    if g["runner_group"] == "xfactory-artifact-workers")
    assert "opensoft/codexFactory" in artifact["observed_repositories"]
    assert artifact["expected_repositories"] == ["opensoft/xFactory"]
    repo_findings = [f for f in artifact["findings"]
                     if f["subject"] == "opensoft/codexFactory"]
    assert repo_findings and repo_findings[0]["finding_class"] == "widening"


def test_a_dark_lane_filed_as_a_widening_is_refused(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(POSITIVE)
    for group in doc["groups"]:
        for finding in group["findings"]:
            if finding["subject"] == "review-lane-worker.yml":
                finding["finding_class"] = "widening"
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-attestation-dark-lane-as-breach" in \
        reader.codes_of(findings.errors), findings.errors


def test_the_dark_lanes_are_the_two_measured_ones() -> None:
    """`review-lane-worker.yml` and `ideation-organizer-worker.yml` declare a
    group-5 job and hold no allowlist entry — measured 2026-09-01. They are
    ALREADY FAILING CLOSED, and their disposition is to be retired into an
    operation or removed, never to be filed as a breach."""
    artifact = next(g for g in POSITIVE["groups"]
                    if g["runner_group"] == "xfactory-artifact-workers")
    absent = {m["workflow"] for m in artifact["enumerated_members"]
              if m["declared_allowlist_status"] == "absent"}
    assert absent == {"review-lane-worker.yml", "ideation-organizer-worker.yml"}
    dark = {f["subject"] for f in artifact["findings"]
            if f["finding_class"] == "dark_lane"}
    assert dark == absent


def test_an_estate_wide_expected_set_is_refused(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(POSITIVE)
    shared = ["execution-lane-coding-worker.yml", "council-deliberation-worker.yml"]
    for group in doc["groups"]:
        group["expected_allowlist"] = list(shared)
        group["findings"] = []
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-attestation-expected-set-not-per-group" in \
        reader.codes_of(findings.errors), findings.errors


def test_the_absent_clearing_path_is_convergence_not_a_widening() -> None:
    """"CONVERGENCE IS A TERMINAL STATE, NOT AN ENTRY CONDITION ... That interval
    is a NOT-YET-CONVERGED state and SHALL NOT be reported as a single-door
    breach"."""
    for group in POSITIVE["groups"]:
        assert group["clearing_path_admitted"] is False
        classes = {f["finding_class"] for f in group["findings"]
                   if f["subject"] == POSITIVE["clearing_workflow_path"]}
        assert classes == {"convergence_not_yet_reached"}


def test_the_clearing_path_filed_as_a_widening_is_refused(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(POSITIVE)
    for group in doc["groups"]:
        for finding in group["findings"]:
            if finding["subject"] == doc["clearing_workflow_path"]:
                finding["finding_class"] = "widening"
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-attestation-dark-lane-as-breach" in \
        reader.codes_of(findings.errors), findings.errors


def test_the_completeness_claim_is_the_narrower_one_before_admission() -> None:
    assert POSITIVE["completeness_claim"]["strength"] == "narrower_pre_admission"


def test_claiming_full_completeness_before_admission_is_refused(
        reader, registry_and_docs, entries) -> None:
    doc = copy.deepcopy(POSITIVE)
    doc["completeness_claim"]["strength"] = "full_post_admission"
    findings = adjudicate(reader, registry_and_docs, entries, {}, doc)
    assert "clearing-attestation-overclaims-completeness" in \
        reader.codes_of(findings.errors), findings.errors


def test_the_residual_is_declared_in_the_record_itself() -> None:
    """"The RESIDUAL SHALL be declared rather than implied."

    Required as a field rather than left to a document beside the record,
    because a residual stated elsewhere is a residual a reader of the record does
    not see.
    """
    assert "residual_statement" in SCHEMA["required"]
    residual = POSITIVE["residual_statement"]
    assert "version control" in residual
    assert "OBSERVABLE" in residual
