"""Every ruled value the wiring consumes is READ BACK from its contract.

None of §7's numbers were invented in the runtime package, and this file is
what makes that checkable rather than claimed: each constant is compared
against the artifact that rules it, so a drift in either direction — someone
editing the contract, or someone editing the mirror — fails here rather than
being discovered when the canary trips on the wrong number.

Sources:

* `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml` — the §7.2
  per-session ceilings and provider-project cap, the §7.2 per-tenant budget,
  the three-way rollback split with its triggers and revoke flags, §7.7's
  operator surface, §7.8's session-outcome tokens and §7.10's tenant count.
* `contracts/avatar-client/latency-sample-minimum.yaml` — §7.5's declared n.
* `contracts/avatar-client/acceptance-map.yaml` — ALV-SLO-001's materiality
  rule and its gated set.
* `contracts/avatar-client/registries/session-outcomes.registry.yaml` — the
  closed registry every declared token must be a member of.
* `contracts/avatar-client/usage-metering-and-alerting.yaml` — task 6.1.4's
  channel routing and its named install-side halves.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from xfactory.avatar_runtime import detection, metering, rollback, spend

AVC = Path(__file__).resolve().parents[2] / "contracts" / "avatar-client"


def _load(name: str) -> dict:
    return yaml.safe_load((AVC / name).read_text())


@pytest.fixture(scope="module")
def policy() -> dict:
    return _load("canary-cohort-and-rollback-policy.yaml")


@pytest.fixture(scope="module")
def classes(policy) -> dict:
    return {c["id"]: c for c in policy["rollback_policy"]["classes"]}


@pytest.fixture(scope="module")
def acceptance_map() -> dict:
    return _load("acceptance-map.yaml")


# --- §7.2, the per-session ceilings (task 6.1.3) ---------------------------- #
def test_session_ceilings_match_the_ruled_quota_condition(classes):
    quota = classes["ROLLBACK-B"]["trigger_thresholds"]["elevated_quota_condition"]
    assert spend.SESSION_DURATION_CEILING_SECONDS == quota["per_session_duration_seconds_max"]
    assert spend.SESSION_BILLABLE_UNIT_CEILING == quota["per_session_billable_units_max"]
    assert quota["billable_unit"] == "one_us_cent_of_provider_attributed_spend"
    assert spend.BILLABLE_UNIT_USD_CENTS == 1
    assert spend.SESSION_SPEND_CEILING_USD_CENTS == 300  # $3.00
    assert quota["uncountable_is"] == "exhausted"


def test_the_project_cap_matches_the_ruled_figure(classes):
    quota = classes["ROLLBACK-B"]["trigger_thresholds"]["elevated_quota_condition"]
    assert (
        metering.PROJECT_MONTHLY_CAP_USD_CENTS
        == quota["provider_project_monthly_cap_usd"] * 100
    )
    assert quota["provider_project_cap_enforcement"] == "hard_at_the_provider_project"


# --- §7.2/§7.4/§7.10, the per-tenant budget (task 6.1.4) ------------------- #
def test_the_per_tenant_budget_matches_the_ruled_cost_concern(classes):
    cost = classes["ROLLBACK-C"]["trigger_signals"]["cost_concern"]
    assert (
        metering.TENANT_MONTHLY_BUDGET_USD_CENTS
        == cost["per_tenant_monthly_budget_usd"] * 100
    )
    # Metered and alerted ONLY — no per-tenant hard stop exists at this ring.
    assert cost["enforcement"] == "metered_and_alerted_only"
    assert cost["hard_stop_exists"] is False
    assert cost["alert_reader"] == metering.AlertChannel.GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN.value
    assert cost["budget_subject"] == "cohort_member"


def test_the_tenant_count_matches_the_cohort(policy):
    tenant_def = policy["cohort"]["tenant_definition_ref"]
    assert metering.RULED_TENANT_COUNT == tenant_def["tenant_count"]
    assert tenant_def["tenant_count"] == len(policy["cohort"]["members"])
    assert tenant_def["tenant_is"] == "cohort_member"


def test_the_alert_recipient_and_runbook_resolve_through_the_policy(policy):
    surface = policy["rollback_policy"]["operator_surface"]
    assert surface["status"] == "named"
    assert surface["holder"] and surface["holder_kind"] == "named_person"
    assert surface["mechanism_ref"] == "docs/sops/avatar-internal-live-kill-switch.md"
    assert surface["also_the_alert_page_target"] is True
    # The metering alert can be built from those two values and nothing else.
    alert = metering.build_alert(
        "2026-08-27",
        [
            metering.ThresholdCrossing(
                "tenant", "COHORT-01", 100,
                metering.TENANT_MONTHLY_BUDGET_USD_CENTS,
                metering.TENANT_MONTHLY_BUDGET_USD_CENTS,
                metering.AlertChannel.GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN,
            )
        ],
        [],
        recipient=surface["holder"],
        runbook_ref=surface["mechanism_ref"],
    )
    assert alert is not None and alert.recipient == surface["holder"]


def test_the_metering_record_names_its_install_side_halves():
    record = _load("usage-metering-and-alerting.yaml")
    declared = {c["id"]: c for c in record["channels"]}
    for channel in metering.AlertChannel:
        assert channel.value in declared, channel
    for channel in metering.INSTALL_SIDE_CHANNELS:
        assert declared[channel.value]["built_in_this_repository"] is False
        assert declared[channel.value]["install_side_owner"]
    gh = declared[metering.AlertChannel.GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN.value]
    assert gh["built_in_this_repository"] is True
    assert gh["pattern_source"] == ".github/workflows/doc-health-reusable.yml"
    assert record["marks"]["percentages"] == list(metering.THRESHOLD_MARKS_PCT)


# --- §7.5 and ALV-SLO-001, the latency trip (task 6.3.3) ------------------- #
def test_the_declared_sample_minimum_matches_its_declaration():
    minimum = _load("latency-sample-minimum.yaml")["minimum"]
    assert detection.DECLARED_SAMPLE_MINIMUM == minimum["n_min"]
    assert set(detection.GATED_PERCENTILES) == set(minimum["gated_percentiles"])
    assert detection.GATED_INTERVALS == frozenset(minimum["gated_intervals"])
    assert detection.GATED_PLATFORMS == frozenset(minimum["gated_platforms"])
    assert detection.GATED_NETWORK_CLASS == minimum["gated_network_class"]


def test_under_the_minimum_is_recorded_not_gated():
    assert _load("latency-sample-minimum.yaml")["under_minimum"]["effect"] == (
        "recorded_not_gated"
    )


def test_the_materiality_rule_matches_alv_slo_001(acceptance_map):
    slo = acceptance_map["latency_slo"]
    assert slo["id"] == "ALV-SLO-001"
    assert slo["materiality"]["rule"] == "greater_of"
    assert detection.RELATIVE_THRESHOLD_PCT == slo["materiality"]["relative_threshold_pct"]
    assert detection.ABSOLUTE_THRESHOLD_MS == slo["materiality"]["absolute_threshold_ms"]
    assert detection.REFERENCE_CLASSIFICATION == slo["comparison_cell"]["reference_classification"]
    assert detection.ADAPTER_CLASSIFICATION == slo["comparison_cell"]["adapter_classification"]
    gated = slo["gated"]
    assert set(detection.GATED_PERCENTILES) == set(gated["percentiles"])
    assert detection.GATED_INTERVALS == frozenset(gated["intervals"])
    assert detection.GATED_PLATFORMS == frozenset(gated["platforms"])
    assert detection.GATED_NETWORK_CLASS == gated["network_class"]


# --- §6.3.2/§7.8, the split and its tokens (tasks 6.3.3-6.3.5) ------------- #
@pytest.mark.parametrize(
    "class_id,klass",
    [
        ("ROLLBACK-A", rollback.RollbackClass.A),
        ("ROLLBACK-B", rollback.RollbackClass.B),
        ("ROLLBACK-C", rollback.RollbackClass.C),
    ],
)
def test_each_class_mirrors_its_recorded_triggers_and_revoke_flag(
    classes, class_id, klass
):
    recorded = classes[class_id]
    assert rollback.CLASS_TRIGGERS[klass] == frozenset(recorded["triggers"])
    ruled = recorded["revoke_active_leases"]
    if ruled == "operator_selected":
        assert rollback.CLASS_REVOKES_ACTIVE[klass] is None
    else:
        assert rollback.CLASS_REVOKES_ACTIVE[klass] is ruled


def test_rollback_b_revoke_flag_is_false_in_both_places(classes):
    """The mutation `check_canary_rollback_policy` exists to catch."""
    assert classes["ROLLBACK-B"]["revoke_active_leases"] is False
    assert rollback.CLASS_REVOKES_ACTIVE[rollback.RollbackClass.B] is False


def test_session_outcome_tokens_match_seven_eight(policy, classes):
    bound = {b["path"]: b for b in policy["rollback_policy"]["session_outcome_tokens"]["bound"]}
    assert bound["force_terminated_leg"]["outcome"] == "revoked"
    assert bound["drained_leg_after_block_new"]["outcome"] == "abandoned"
    assert tuple(bound["drained_leg_after_block_new"]["also_permitted"]) == (
        rollback.DRAINED_LEG_ALSO_PERMITTED
    )
    assert rollback.CLASS_SESSION_OUTCOME[rollback.RollbackClass.A] == classes["ROLLBACK-A"]["session_outcome"]
    assert rollback.CLASS_SESSION_OUTCOME[rollback.RollbackClass.B] == classes["ROLLBACK-B"]["session_outcome"]
    assert rollback.CLASS_OUTCOME_PATH[rollback.RollbackClass.A] == classes["ROLLBACK-A"]["session_outcome_path"]
    assert rollback.CLASS_OUTCOME_PATH[rollback.RollbackClass.B] == classes["ROLLBACK-B"]["session_outcome_path"]
    assert policy["rollback_policy"]["session_outcome_tokens"]["new_outcome_token_introduced"] is False


def test_no_new_session_outcome_token_is_introduced():
    registry = yaml.safe_load(
        (AVC / "registries" / "session-outcomes.registry.yaml").read_text()
    )
    members = {m["id"] for m in registry["members"]}
    declared = {
        v for v in rollback.CLASS_SESSION_OUTCOME.values() if v is not None
    } | set(rollback.DRAINED_LEG_ALSO_PERMITTED)
    assert declared <= members
    # Every token the runtime can emit is a member too.
    from xfactory.avatar_runtime.values import AttemptStatus, OutcomeCode

    emitted = {
        rollback.session_outcome_token(status, outcome)
        for status in AttemptStatus
        for outcome in list(OutcomeCode) + [None]
    } - {None}
    assert emitted <= members


# --- §6.3.4 and the abort scope (tasks 6.3.4-6.3.5) ------------------------ #
def test_the_rollback_target_matches_the_policy(policy):
    target = policy["rollback_target"]
    assert target["target"] == "disable_voice_to_text_or_human_handoff"
    assert target["model_fallback_exists"] is rollback.MODEL_FALLBACK_EXISTS is False
    assert policy["candidate_profile"] == rollback.CANDIDATE_PROFILE


def test_the_offered_modes_are_released_fallback_mode_tokens():
    registry = yaml.safe_load(
        (AVC / "registries" / "fallback-modes.registry.yaml").read_text()
    )
    members = {m["id"] for m in registry["members"]}
    assert set(rollback.ROLLBACK_OFFERED_MODES) <= members


def test_the_abort_scope_ends_media_only(policy):
    scope = policy["abort_scope"]
    assert scope["ends"] == "media_plane_only"
    assert set(scope["survives"]) == {
        "authority_owned_workflow_projection",
        "policy_required_structured_records",
    }
    assert scope["proof_owner"] == "qualify-avatar-live-voice 6.3.5"


def test_this_change_still_owns_the_detection_wiring(classes):
    for class_id in ("ROLLBACK-A", "ROLLBACK-B"):
        assert classes[class_id]["detection_wiring_owner"] == (
            "qualify-avatar-live-voice 6.3.3"
        )
