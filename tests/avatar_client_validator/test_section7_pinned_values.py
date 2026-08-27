"""Positive + fail-closed negative coverage for the §7 authoring inputs ruled
2026-08-27 on ``qualify-avatar-live-voice``, as enforced by
``scripts/validate-avatar-client.py``:

* ``_check_section_7_values`` — §7.6's canary exit criteria and the §7.2 trip
  points ROLLBACK-B and ROLLBACK-C consume (called from
  ``check_canary_rollback_policy``).
* ``check_latency_sample_minimum`` — §7.5, feeding §5.2.
* ``check_broker_credential_binding`` — §7.1 and §7.3, task 6.1.1's custody
  pair.

EVERY NEGATIVE IS A MUTATION OF THE REAL ARTIFACT, not of a synthetic stand-in.
The real files are copied into a tmp tree, one field is moved, and the check is
run against that tree with the module-level ``AVC`` monkeypatched to it. That
shape buys two things a hand-written fixture does not: the positive case proves
the SHIPPED artifacts pass, and each negative proves the check would have
noticed the specific edit it names — rather than proving a fixture written to
fail does fail, which is a much weaker claim.

The validator is a hyphenated script, so it is loaded by file path with
``importlib``, the same way the sibling tests in this directory do it.
"""

from __future__ import annotations

import copy
import importlib.util
import shutil
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

import pytest
import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ENTRYPOINT = REPOSITORY_ROOT / "scripts" / "validate-avatar-client.py"
REAL_AVC = REPOSITORY_ROOT / "contracts" / "avatar-client"


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_avatar_client", ENTRYPOINT)
    assert spec and spec.loader, f"cannot load validator at {ENTRYPOINT}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()

# The four artifacts the §7 checks read. `acceptance-map.yaml` is copied too:
# the sample-minimum check compares its declared cell set against the SLO's
# gated axes, and the custody checks resolve `acceptance_map_refs` against it.
COPIED = (
    "acceptance-map.yaml",
    "canary-cohort-and-rollback-policy.yaml",
    "latency-sample-minimum.yaml",
    "broker-server-key-binding.template.yaml",
    "broker-server-key-rotation-policy.yaml",
)


def _codes(findings) -> list[str]:
    return [line.split("]")[0].split("[")[1] for line in findings.errors]


def _messages(findings) -> str:
    return "\n".join(findings.errors)


def _tree(tmp_path: Path) -> Path:
    avc = tmp_path / "avatar-client"
    avc.mkdir()
    for name in COPIED:
        shutil.copy2(REAL_AVC / name, avc / name)
    return avc


def _rewrite(avc: Path, name: str, mutate: Callable[[dict], Any]) -> None:
    doc = yaml.safe_load((avc / name).read_text())
    mutate(doc)
    (avc / name).write_text(yaml.safe_dump(doc, sort_keys=False))


def _run(monkeypatch, avc: Path, check: str):
    """Run one §7 check against a tmp artifact tree."""
    monkeypatch.setattr(VALIDATOR, "AVC", avc)
    findings = VALIDATOR.Findings()
    if check == "policy":
        VALIDATOR.check_canary_rollback_policy(findings)
    elif check == "samples":
        VALIDATOR.check_latency_sample_minimum(findings)
    else:
        VALIDATOR.check_broker_credential_binding(findings)
    return findings


# ---------------------------------------------------------------------------
# The positive: the artifacts as shipped.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("check", ["policy", "samples", "binding"])
def test_shipped_artifacts_pass(tmp_path, monkeypatch, check):
    findings = _run(monkeypatch, _tree(tmp_path), check)
    assert findings.errors == [], _messages(findings)


# ---------------------------------------------------------------------------
# §7.6 — the canary exit criteria, and §7.2's trip points.
# ---------------------------------------------------------------------------

def _exit(doc: dict) -> dict:
    return doc["canary_exit_criteria"]


def _rollback(doc: dict, cid: str) -> dict:
    return next(c for c in doc["rollback_policy"]["classes"] if c["id"] == cid)


POLICY_MUTATIONS = {
    # The regression the artifact's own former statement warned about: values
    # held open "so that a canary cannot be declared successful against
    # criteria invented after the fact", quietly reopened.
    "status_back_to_unset":
        lambda d: _exit(d).__setitem__("status", "unset"),
    "criteria_block_deleted":
        lambda d: d.pop("canary_exit_criteria"),
    "soak_shortened":
        lambda d: _exit(d)["soak_duration"].__setitem__("consecutive_calendar_days", 7),
    "distinct_day_floor_dropped":
        lambda d: _exit(d)["soak_duration"].__setitem__("sessions_on_distinct_days_min", 1),
    "session_count_halved":
        lambda d: _exit(d)["minimum_session_count"].__setitem__("completed_sessions", 100),
    "cohort_02_floor_removed":
        lambda d: _exit(d)["minimum_session_count"]["sub_floors"].pop(
            "cohort_02_domain_sandbox_min"),
    "per_class_floor_moved":
        lambda d: _exit(d)["minimum_session_count"]["sub_floors"].__setitem__(
            "per_evaluation_scenario_class_min", 1),
    "overall_rate_loosened":
        lambda d: _exit(d)["tolerated_error_rate"].__setitem__(
            "abnormal_rate_overall_max_pct", 10),
    "abnormal_definition_dropped":
        lambda d: _exit(d)["tolerated_error_rate"].pop("abnormal_definition"),
    "rehearsal_criterion_dropped":
        lambda d: _exit(d).__setitem__(
            "additional_criteria",
            [a for a in _exit(d)["additional_criteria"]
             if a["id"] != "EXIT-ROLLBACK-B-REHEARSED"]),
    "trip_points_deleted":
        lambda d: _rollback(d, "ROLLBACK-B").pop("trigger_thresholds"),
    "trigger_without_a_trip_point":
        lambda d: _rollback(d, "ROLLBACK-B")["triggers"].append("elevated_cost_condition"),
    "trip_point_with_no_trigger":
        lambda d: _rollback(d, "ROLLBACK-B")["trigger_thresholds"].__setitem__(
            "elevated_cost_condition", {"note": "orphan"}),
    "session_duration_ceiling_moved":
        lambda d: _rollback(d, "ROLLBACK-B")["trigger_thresholds"][
            "elevated_quota_condition"].__setitem__("per_session_duration_seconds_max", 3600),
    "session_spend_ceiling_moved":
        lambda d: _rollback(d, "ROLLBACK-B")["trigger_thresholds"][
            "elevated_quota_condition"].__setitem__("per_session_billable_units_max", 5000),
    "project_cap_moved":
        lambda d: _rollback(d, "ROLLBACK-B")["trigger_thresholds"][
            "elevated_quota_condition"].__setitem__("provider_project_monthly_cap_usd", 5000),
    "uncountable_fails_open":
        lambda d: _rollback(d, "ROLLBACK-B")["trigger_thresholds"][
            "elevated_quota_condition"].__setitem__("uncountable_is", "permitted"),
    "per_tenant_budget_moved":
        lambda d: _rollback(d, "ROLLBACK-C")["trigger_signals"][
            "cost_concern"].__setitem__("per_tenant_monthly_budget_usd", 5000),
    # Recording the metered-only per-tenant budget as a hard stop would be
    # FALSE: Fork 1 Option C defers the durable counter (task 6.1.5).
    "metered_budget_claimed_hard":
        lambda d: _rollback(d, "ROLLBACK-C")["trigger_signals"][
            "cost_concern"].__setitem__("hard_stop_exists", True),
    # The `budget_envelopes: {}` failure this org has already had flagged.
    "budget_left_without_a_reader":
        lambda d: _rollback(d, "ROLLBACK-C")["trigger_signals"]["cost_concern"].pop(
            "alert_reader"),
}


@pytest.mark.parametrize("name", sorted(POLICY_MUTATIONS))
def test_canary_policy_section_7_mutations_are_caught(tmp_path, monkeypatch, name):
    avc = _tree(tmp_path)
    _rewrite(avc, "canary-cohort-and-rollback-policy.yaml", POLICY_MUTATIONS[name])
    findings = _run(monkeypatch, avc, "policy")
    assert findings.errors, f"mutation {name!r} produced no finding"
    assert set(_codes(findings)) == {"canary-policy"}, _messages(findings)


def test_error_rate_drift_between_exit_criterion_and_auto_blocker(tmp_path, monkeypatch):
    """The coupling the ruling names: the canary's trailing-window tolerated
    error rate and ROLLBACK-B's `elevated_error_rate` are ONE number. Moved on
    one side only, the canary could pass its exit criterion while its
    auto-blocker was tripping."""
    avc = _tree(tmp_path)
    _rewrite(avc, "canary-cohort-and-rollback-policy.yaml",
             lambda d: _exit(d)["tolerated_error_rate"].__setitem__(
                 "abnormal_rate_trailing_window_max_pct", 12))
    findings = _run(monkeypatch, avc, "policy")
    joined = _messages(findings)
    assert "disagrees with" in joined, joined
    assert set(_codes(findings)) == {"canary-policy"}


def test_error_rate_moved_consistently_still_fails_the_ruling(tmp_path, monkeypatch):
    """Moving BOTH sides keeps them agreeing with each other and still fails,
    because each is compared to the ruled value as well as to the other. A
    consistency rule alone would let an operator relax the ring by editing two
    lines instead of one."""
    def mutate(d):
        _exit(d)["tolerated_error_rate"]["abnormal_rate_trailing_window_max_pct"] = 12
        _rollback(d, "ROLLBACK-B")["trigger_thresholds"]["elevated_error_rate"][
            "abnormal_rate_trailing_window_max_pct"] = 12

    avc = _tree(tmp_path)
    _rewrite(avc, "canary-cohort-and-rollback-policy.yaml", mutate)
    findings = _run(monkeypatch, avc, "policy")
    joined = _messages(findings)
    assert "disagrees with" not in joined, joined
    assert findings.errors, "a consistently-relaxed ring passed"


# ---------------------------------------------------------------------------
# §7.5 — the minimum sample count per gated cell.
# ---------------------------------------------------------------------------

SAMPLE_MUTATIONS = {
    "minimum_halved":
        lambda d: d["minimum"].__setitem__("n_min", 50),
    "declared_after_measuring":
        lambda d: d["declaration"].__setitem__("declared_before_measuring", False),
    "declaration_undated":
        lambda d: d["declaration"].pop("declared_on"),
    "short_cell_allowed_to_gate":
        lambda d: d["under_minimum"].__setitem__("effect", "gated"),
    "run_spread_collapsed":
        lambda d: d["spread"].__setitem__("distinct_runs_min", 1),
    "day_spread_collapsed":
        lambda d: d["spread"].__setitem__("distinct_days_min", 1),
    "p99_floor_moved":
        lambda d: d["p99_posture"].__setitem__("gate_sample_floor", 100),
    "p99_promoted_to_a_gate":
        lambda d: d["p99_posture"].__setitem__("stays_recorded_not_gated", False),
    # A minimum declared over a cell set the SLO does not gate is a minimum for
    # nothing — it reads as rigor and leaves every gated cell without a floor.
    "platforms_diverge_from_the_slo":
        lambda d: d["minimum"].__setitem__("gated_platforms", ["linux_ci"]),
    "percentiles_diverge_from_the_slo":
        lambda d: d["minimum"].__setitem__("gated_percentiles", ["p99"]),
    "intervals_diverge_from_the_slo":
        lambda d: d["minimum"].__setitem__("gated_intervals", ["teardown_to_terminal_ms"]),
    "network_class_diverges_from_the_slo":
        lambda d: d["minimum"].__setitem__("gated_network_class", "degraded"),
    "cell_count_left_behind":
        lambda d: d["minimum"].__setitem__("cells", 6),
    "wrong_kind":
        lambda d: d.__setitem__("kind", "avatar-client-acceptance-map"),
    "unresolvable_map_reference":
        lambda d: d.__setitem__("acceptance_map_refs", ["ALV-999"]),
}


@pytest.mark.parametrize("name", sorted(SAMPLE_MUTATIONS))
def test_sample_minimum_mutations_are_caught(tmp_path, monkeypatch, name):
    avc = _tree(tmp_path)
    _rewrite(avc, "latency-sample-minimum.yaml", SAMPLE_MUTATIONS[name])
    findings = _run(monkeypatch, avc, "samples")
    assert findings.errors, f"mutation {name!r} produced no finding"
    assert set(_codes(findings)) == {"sample-minimum"}, _messages(findings)


def test_absent_sample_minimum_fails_closed(tmp_path, monkeypatch):
    """An undeclared minimum is exactly the state §5.2 exists to prevent, so
    absence is the defect and not a deferral."""
    avc = _tree(tmp_path)
    (avc / "latency-sample-minimum.yaml").unlink()
    findings = _run(monkeypatch, avc, "samples")
    assert _codes(findings) == ["sample-minimum"]
    assert "DECLARED BEFORE MEASURING" in _messages(findings)


# ---------------------------------------------------------------------------
# §7.1 and §7.3 — the broker server-key custody pair (task 6.1.1).
# ---------------------------------------------------------------------------

def _binding(doc: dict) -> dict:
    return doc["credential_bindings"]["avatar_broker_openai_internal_live"]


BINDING_MUTATIONS = {
    # THE FAILURE THIS CHECK EXISTS FOR: someone with the install's values in
    # front of them fills in the two placeholders, because they look empty.
    "vault_product_filled_in":
        lambda d: _binding(d).__setitem__("provider", "azure_key_vault"),
    "vault_instance_filled_in":
        lambda d: _binding(d).__setitem__("vault", "kv-opensoft-xfactory-qa"),
    # Prose is where such a paste survives review, so values are walked, not
    # just the fields expected to carry one.
    "vault_named_in_prose":
        lambda d: d.__setitem__("source", "resolved from AWS Secrets Manager at call time"),
    "raw_secret_pasted_as_the_reference":
        lambda d: _binding(d).__setitem__("secret_ref", "sk-proj-EXAMPLENOTAREALKEY"),
    "reference_renamed_to_the_f0_lab_key":
        lambda d: _binding(d).__setitem__("secret_ref", "openai-realtime-f0-lab"),
    "owner_dropped":
        lambda d: _binding(d).pop("owner"),
    "vault_field_dropped":
        lambda d: _binding(d).pop("vault"),
    "rotation_label_changed":
        lambda d: _binding(d).__setitem__("rotation_policy", "unmanaged"),
    "second_credential_shares_the_record":
        lambda d: d["credential_bindings"].__setitem__(
            "avatar_broker_openai_pilot",
            {"provider": "<p>", "vault": "<v>", "secret_ref": "other",
             "owner": "opensoft-platform", "rotation_policy": "operator_managed"}),
    "binding_renamed":
        lambda d: d.__setitem__("credential_bindings", {"something_else": _binding(d)}),
    "resolved_by_someone_other_than_the_broker":
        lambda d: d["resolution"].__setitem__("resolved_by", "client"),
    "materialized_persistently":
        lambda d: d["resolution"].__setitem__("materialization", "host_state"),
    "wrong_kind":
        lambda d: d.__setitem__("kind", "avatar-client-acceptance-map"),
}


@pytest.mark.parametrize("name", sorted(BINDING_MUTATIONS))
def test_binding_mutations_are_caught(tmp_path, monkeypatch, name):
    avc = _tree(tmp_path)
    _rewrite(avc, "broker-server-key-binding.template.yaml", BINDING_MUTATIONS[name])
    findings = _run(monkeypatch, avc, "binding")
    assert findings.errors, f"mutation {name!r} produced no finding"
    assert set(_codes(findings)) == {"broker-credential"}, _messages(findings)


ROTATION_MUTATIONS = {
    "cadence_removed":
        lambda d: d["rotation_policy"]["credential_overrides"][
            "avatar_broker_openai_internal_live"].pop("max_key_age_days"),
    "cadence_moved":
        lambda d: d["rotation_policy"]["credential_overrides"][
            "avatar_broker_openai_internal_live"].__setitem__("max_key_age_days", 365),
    # Narrowing the inherited list silently drops the SOP's compromise path,
    # which rides `suspected_exposure`.
    "global_triggers_narrowed":
        lambda d: d["rotation_policy"].__setitem__(
            "require_rotation_on", ["client_offboarding"]),
    "added_triggers_changed":
        lambda d: d["rotation_policy"]["credential_overrides"][
            "avatar_broker_openai_internal_live"].__setitem__(
                "additional_require_rotation_on", ["canary_cohort_change"]),
    # A cadence keyed to a credential no binding declares governs nothing.
    "override_keyed_to_another_credential":
        lambda d: d["rotation_policy"].__setitem__(
            "credential_overrides",
            {"some_other_credential": d["rotation_policy"]["credential_overrides"][
                "avatar_broker_openai_internal_live"]}),
    "binding_pointer_drifts":
        lambda d: d.__setitem__("binds_credential_binding", "some_other_credential"),
    "rotation_record_permits_the_value":
        lambda d: d["rotation_policy"]["rotation_record"].__setitem__(
            "forbidden_fields", []),
    "vault_named_in_prose":
        lambda d: d.__setitem__("source", "the 1Password enterprise vault"),
    "wrong_kind":
        lambda d: d.__setitem__("kind", "xfactory_credential_binding_template"),
}


@pytest.mark.parametrize("name", sorted(ROTATION_MUTATIONS))
def test_rotation_policy_mutations_are_caught(tmp_path, monkeypatch, name):
    avc = _tree(tmp_path)
    _rewrite(avc, "broker-server-key-rotation-policy.yaml", ROTATION_MUTATIONS[name])
    findings = _run(monkeypatch, avc, "binding")
    assert findings.errors, f"mutation {name!r} produced no finding"
    assert set(_codes(findings)) == {"broker-credential"}, _messages(findings)


@pytest.mark.parametrize("victim", ["broker-server-key-binding.template.yaml",
                                    "broker-server-key-rotation-policy.yaml"])
def test_absent_custody_artifact_fails_closed(tmp_path, monkeypatch, victim):
    """The binding is the ring's ONLY deployment source — F0's mode-600 local
    file and its age-escrow copy are explicitly not one — and the cadence has
    no other home, because the published binding shape types `rotation_policy`
    as a string."""
    avc = _tree(tmp_path)
    (avc / victim).unlink()
    findings = _run(monkeypatch, avc, "binding")
    assert _codes(findings) == ["broker-credential"], _messages(findings)
    assert "fail closed" in _messages(findings)


def test_placeholder_check_accepts_only_the_bracketed_form(tmp_path, monkeypatch):
    """A blank is not a placeholder: an empty `provider` reads as "not yet
    decided" to a human and as a missing required field to the schema, so it is
    reported as absent rather than passing the vault-product rule by having no
    product in it."""
    avc = _tree(tmp_path)
    _rewrite(avc, "broker-server-key-binding.template.yaml",
             lambda d: _binding(d).__setitem__("provider", ""))
    findings = _run(monkeypatch, avc, "binding")
    assert "`provider` missing" in _messages(findings)


def test_mutations_are_applied_to_a_copy_not_the_repository():
    """Guard for this file's own method: the mutations above edit a tmp copy,
    so a run of this suite must leave the shipped artifacts byte-identical."""
    before = {name: (REAL_AVC / name).read_bytes() for name in COPIED}
    after = {name: (REAL_AVC / name).read_bytes() for name in COPIED}
    assert before == after
    assert all(copy.copy(v) == v for v in before.values())
