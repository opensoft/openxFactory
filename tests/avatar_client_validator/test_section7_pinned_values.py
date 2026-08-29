"""Positive + fail-closed negative coverage for the §7 authoring inputs ruled
2026-08-27 on ``qualify-avatar-live-voice``, as enforced by
``scripts/validate-avatar-client.py``:

* ``_check_section_7_values`` — §7.6's canary exit criteria, the §7.2 trip
  points ROLLBACK-B and ROLLBACK-C consume, §7.7's named operator surface,
  §7.8's session-outcome tokens and §7.10's tenant definition (all called from
  ``check_canary_rollback_policy``).
* ``check_latency_sample_minimum`` — §7.5, feeding §5.2.
* ``check_broker_credential_binding`` — §7.1 and §7.3, task 6.1.1's custody
  pair.
* ``check_activation_checklist`` — §7.9's region, data-control and retention
  values, pinned on the checklist's condition 2.

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

# The artifacts the §7 checks read. `acceptance-map.yaml` is copied too: the
# sample-minimum check compares its declared cell set against the SLO's gated
# axes, and the custody and checklist checks resolve `acceptance_map_refs`
# against it. `registries/session-outcomes.registry.yaml` is copied because
# §7.8's rule is that no NEW outcome token is introduced, and the check
# resolves the declared tokens against that closed registry rather than against
# a list mirrored in the validator — so the registry has to be IN the tree, and
# mutating it is itself a case worth having.
COPIED = (
    "acceptance-map.yaml",
    "canary-cohort-and-rollback-policy.yaml",
    "internal-live-activation-checklist.yaml",
    "latency-sample-minimum.yaml",
    "broker-server-key-binding.template.yaml",
    "broker-server-key-rotation-policy.yaml",
    "registries/session-outcomes.registry.yaml",
)


# CAPTURED AT IMPORT TIME — during collection, before any test in this module
# has run — so that the end-of-session comparison has something to be a
# baseline OF. Reading the repository twice inside the guard instead would
# compare a mutated file to itself and agree.
_BASELINE_BYTES = {name: (REAL_AVC / name).read_bytes() for name in COPIED}


@pytest.fixture(scope="session", autouse=True)
def repository_artifacts_are_never_mutated():
    """THE ENFORCEMENT of this module's central safety property: every mutation
    here edits a copy under `tmp_path`, and none of them may reach the
    repository.

    It is a session-scoped teardown rather than a test so that it is
    ORDER-INDEPENDENT. As an ordinary test it would only catch a mutation made
    by a test that happened to run before it, which under a randomizing or
    parallel plugin is a coin flip; as a teardown it runs after everything, and
    a mutation made anywhere in the session is still there to be found.

    It compares against `_BASELINE_BYTES` — the bytes as of import — and not
    against a fresh read, for the reason spelled out in
    `test_the_repository_artifacts_match_their_import_time_bytes`."""
    yield
    drifted = sorted(name for name in COPIED
                     if (REAL_AVC / name).read_bytes() != _BASELINE_BYTES[name])
    assert not drifted, (
        f"shipped artifact(s) {drifted} were MUTATED during this session; the "
        f"mutations in this module must edit the tmp tree only. Restore with "
        f"`git checkout -- contracts/avatar-client/`")


def _codes(findings) -> list[str]:
    return [line.split("]")[0].split("[")[1] for line in findings.errors]


def _messages(findings) -> str:
    return "\n".join(findings.errors)


def _tree(tmp_path: Path) -> Path:
    avc = tmp_path / "avatar-client"
    avc.mkdir()
    for name in COPIED:
        target = avc / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REAL_AVC / name, target)
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
    elif check == "checklist":
        VALIDATOR.check_activation_checklist(findings)
    else:
        VALIDATOR.check_broker_credential_binding(findings)
    return findings


# ---------------------------------------------------------------------------
# The positive: the artifacts as shipped.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("check", ["policy", "samples", "binding", "checklist"])
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


def _surface(doc: dict) -> dict:
    return doc["rollback_policy"]["operator_surface"]


def _tokens(doc: dict) -> dict:
    return doc["rollback_policy"]["session_outcome_tokens"]


def _path(doc: dict, name: str) -> dict:
    return next(e for e in _tokens(doc)["bound"] if e["path"] == name)


def _tenant(doc: dict) -> dict:
    return doc["cohort"]["tenant_definition_ref"]


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
        lambda d: _exit(d)["minimum_session_count"].__setitem__("completed_sessions", 50),
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

    # ---- §7.7, the operator surface -------------------------------------
    # The state the block's own statement warned about: "a canary opened
    # without a named holder has an unfireable kill switch".
    "operator_surface_back_to_unnamed":
        lambda d: _surface(d).__setitem__("status", "unnamed"),
    "operator_surface_deleted":
        lambda d: d["rollback_policy"].pop("operator_surface"),
    "holder_replaced":
        lambda d: _surface(d).__setitem__("holder", "someone else"),
    # THE REGRESSION §7.4 WAS ALREADY HOLDING OPEN: a role in the holder
    # field reads as named and leaves the alert with no named recipient.
    "holder_recorded_as_a_role":
        lambda d: _surface(d).__setitem__("holder_kind", "role"),
    "holder_holds_only_one_switch":
        lambda d: _surface(d).__setitem__("holds", "profile_switch_only"),
    "mechanism_changed":
        lambda d: _surface(d).__setitem__("mechanism", "web_console"),
    # A REFERENCE TO A DOCUMENT NOBODY WROTE. The ruled mechanism IS the
    # runbook, so a dangling ref is the unfireable switch with a filename in
    # the field.
    "runbook_ref_dangles":
        lambda d: _surface(d).__setitem__(
            "mechanism_ref", "docs/sops/there-is-no-such-runbook.md"),
    "web_console_named_as_the_surface":
        lambda d: _surface(d).__setitem__("web_console_used", True),
    "rota_deferral_dropped":
        lambda d: _surface(d).pop("rota_deferred_to"),
    # Decoupling the two would un-close the gap §7.7 closed at both ends.
    "alert_target_decoupled_from_the_holder":
        lambda d: _surface(d).__setitem__("also_the_alert_page_target", False),
    # A third scope is a switch the runtime does not have: finer scopes are
    # DEFERRED with the features they would govern.
    "third_kill_switch_invented":
        lambda d: _surface(d)["switches"].append(
            {"id": "SWITCH-TENANT", "scope": "per_tenant",
             "modes": ["block_new", "revoke_active"]}),
    "switch_loses_its_revoke_mode":
        lambda d: _surface(d)["switches"][0].__setitem__("modes", ["block_new"]),

    # ---- §7.8, the session-outcome tokens --------------------------------
    "outcome_tokens_back_to_partially_bound":
        lambda d: _tokens(d).__setitem__("status", "partially_bound"),
    "outcome_token_block_deleted":
        lambda d: d["rollback_policy"].pop("session_outcome_tokens"),
    # A drained leg is `abandoned`; binding it to `revoked` would hide real
    # revocations among performance rollbacks.
    "drained_leg_bound_to_revoked":
        lambda d: _path(d, "drained_leg_after_block_new").__setitem__(
            "outcome", "revoked"),
    "force_terminated_leg_bound_to_abandoned":
        lambda d: _path(d, "force_terminated_leg").__setitem__(
            "outcome", "abandoned"),
    # The ruling's whole content is that no NEW token is introduced.
    "new_outcome_token_invented":
        lambda d: _path(d, "drained_leg_after_block_new").__setitem__(
            "outcome", "drained"),
    "new_token_permitted_as_an_alternative":
        lambda d: _path(d, "drained_leg_after_block_new").__setitem__(
            "also_permitted", ["settled"]),
    "new_token_claim_flipped":
        lambda d: _tokens(d).__setitem__("new_outcome_token_introduced", True),
    "a_bound_path_disappears":
        lambda d: _tokens(d).__setitem__(
            "bound", [e for e in _tokens(d)["bound"]
                      if e["path"] != "consent_or_lease_revocation"]),
    # The open state returning under a closed label.
    "unbound_path_returns":
        lambda d: _tokens(d).__setitem__(
            "unbound", [{"path": "force_terminated_leg",
                         "candidates": ["revoked", "abandoned"]}]),
    # THE TRUTHINESS TRAP, three ways. §7.8's claim is "nothing REMAINS
    # unbound" — an assertion, not the absence of a counter-example — so a
    # missing key and the falsy stand-ins must all refuse. A truthiness test
    # passed every one of these, which made deleting the field the easiest
    # possible way to satisfy the block's strongest sentence.
    "unbound_key_missing":
        lambda d: _tokens(d).pop("unbound"),
    "unbound_is_an_empty_string":
        lambda d: _tokens(d).__setitem__("unbound", ""),
    "unbound_is_a_mapping":
        lambda d: _tokens(d).__setitem__("unbound", {}),
    # THE POLICY POINTING ONE WAY WHILE THE RULE READS ANOTHER. `registry_ref`
    # was recorded and never checked, so the artifact could have nominated a
    # different vocabulary while the membership rule resolved the sanctioned
    # one — the document and its validator disagreeing in silence.
    "registry_ref_points_at_another_registry":
        lambda d: _tokens(d).__setitem__(
            "registry_ref", "registries/session-result-reasons.registry.yaml"),
    "registry_ref_dropped":
        lambda d: _tokens(d).pop("registry_ref"),
    # The same fact carried twice, moved on one side only.
    "class_outcome_drifts_from_the_block":
        lambda d: _rollback(d, "ROLLBACK-B").__setitem__(
            "session_outcome", "completed"),
    "class_outcome_path_drifts":
        lambda d: _rollback(d, "ROLLBACK-A").__setitem__(
            "session_outcome_path", "drained_leg_after_block_new"),
    "operator_class_names_a_single_token":
        lambda d: _rollback(d, "ROLLBACK-C").__setitem__(
            "session_outcome", "revoked"),

    # ---- §7.10, the tenant definition ------------------------------------
    "tenant_back_to_unset":
        lambda d: _tenant(d).__setitem__("status", "unset"),
    "tenant_definition_deleted":
        lambda d: d["cohort"].pop("tenant_definition_ref"),
    # Ruled as anything but a cohort member, §7.2's per-tenant figure needs
    # re-sizing against a new denominator.
    "tenant_ruled_wider_than_a_cohort_member":
        lambda d: _tenant(d).__setitem__("tenant_is", "domain_factory"),
    # The count that outlives the membership it summarises.
    "tenant_count_left_behind":
        lambda d: _tenant(d).__setitem__("tenant_count", 5),
    "tenant_ids_diverge_from_the_cohort":
        lambda d: _tenant(d).__setitem__("tenant_ids", ["COHORT-01"]),
    "sizing_invalidated_quietly":
        lambda d: _tenant(d).__setitem__("sizing_still_valid", False),
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


def test_outcome_token_absent_from_the_registry_is_caught(tmp_path, monkeypatch):
    """§7.8's rule resolves the declared tokens against the CLOSED REGISTRY, not
    against a list mirrored in the validator. Shrink the registry and the policy
    is suddenly naming a token that no longer exists — which a mirrored copy in
    the validator would have gone on agreeing with forever."""
    avc = _tree(tmp_path)
    _rewrite(avc, "registries/session-outcomes.registry.yaml",
             lambda d: d.__setitem__(
                 "members", [m for m in d["members"] if m["id"] != "abandoned"]))
    findings = _run(monkeypatch, avc, "policy")
    joined = _messages(findings)
    assert "closed `session-outcomes` registry" in joined, joined
    assert set(_codes(findings)) == {"canary-policy"}


def test_a_wrong_registry_ref_does_not_disable_the_membership_rule(
        tmp_path, monkeypatch):
    """The claim the fallback rests on, proven rather than asserted: pointing
    `registry_ref` somewhere else must NOT buy a weaker validation. Break the
    ref AND invent a token, and both findings land — the ref mismatch, and the
    invented token caught against the sanctioned registry the rule falls back
    to. Rewarding a broken reference by skipping the rule it names is the one
    outcome this must not have."""
    def mutate(d):
        _tokens(d)["registry_ref"] = "registries/session-result-reasons.registry.yaml"
        _path(d, "drained_leg_after_block_new")["outcome"] = "drained"

    avc = _tree(tmp_path)
    _rewrite(avc, "canary-cohort-and-rollback-policy.yaml", mutate)
    findings = _run(monkeypatch, avc, "policy")
    joined = _messages(findings)
    assert "!= the sanctioned" in joined, joined
    assert "closed `session-outcomes` registry" in joined, joined
    assert set(_codes(findings)) == {"canary-policy"}


def test_absent_outcome_registry_fails_closed(tmp_path, monkeypatch):
    """An unreadable vocabulary is reported, never silently skipped: a check
    that quietly passes when it cannot resolve its registry is not a check."""
    avc = _tree(tmp_path)
    (avc / "registries" / "session-outcomes.registry.yaml").unlink()
    findings = _run(monkeypatch, avc, "policy")
    assert "fail closed" in _messages(findings), _messages(findings)
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
# §7.9 — region, data-control classes and retention, pinned on the activation
# checklist's condition 2 (the condition that APPROVES those terms).
# ---------------------------------------------------------------------------

def _ruled_values(doc: dict) -> dict:
    return next(c for c in doc["conditions"] if c["number"] == 2)["ruled_values"]


CHECKLIST_MUTATIONS = {
    "ruled_values_deleted":
        lambda d: next(c for c in d["conditions"] if c["number"] == 2).pop(
            "ruled_values"),
    "status_back_to_unruled":
        lambda d: _ruled_values(d).__setitem__("status", "unset"),
    "region_moved":
        lambda d: _ruled_values(d)["region"].__setitem__(
            "declared_region", "eu_west_pinned"),
    # The ruling is the provider default DECLARED HONESTLY; dropping the
    # honesty flag is how a default quietly becomes a residency claim.
    "region_honesty_dropped":
        lambda d: _ruled_values(d)["region"].__setitem__("declare_honestly", False),
    # THE MUTATION THIS BLOCK EXISTS FOR: a retention class the kernel says
    # only a successor change may unreserve, admitted by a checklist edit.
    "audio_class_admitted":
        lambda d: _ruled_values(d)["data_control"]["classes_permitted"].append("audio"),
    "full_transcript_class_admitted":
        lambda d: _ruled_values(d)["data_control"]["classes_permitted"].append(
            "full_transcript"),
    "structured_record_class_dropped":
        lambda d: _ruled_values(d)["data_control"].__setitem__(
            "classes_permitted", ["ephemeral_presentation"]),
    "never_instantiated_list_narrowed":
        lambda d: _ruled_values(d)["data_control"].__setitem__(
            "classes_never_instantiated", ["audio"]),
    "reserved_classes_claimed_touched":
        lambda d: _ruled_values(d)["data_control"].__setitem__(
            "reserved_classes_untouched", False),
    # No schema field forbids a second-model shadow today; claiming the
    # guarantee is enforced would be the false claim task 6.2.4 refuses.
    "operational_guarantee_claimed_enforced":
        lambda d: _ruled_values(d)["data_control"].__setitem__(
            "enforcement", "schema_enforced"),
    "retention_window_moved":
        lambda d: _ruled_values(d)["retention"].__setitem__("window_days", 3650),
    "retention_scope_widened":
        lambda d: _ruled_values(d)["retention"].__setitem__(
            "applies_to", "all_canary_records"),
    # A duration with no reference is the inline retention the kernel's
    # reference-only split refuses.
    "retention_policy_reference_dropped":
        lambda d: _ruled_values(d)["retention"].pop("policy_ref"),
    "retention_ownership_moved_off_the_domain":
        lambda d: _ruled_values(d)["retention"].__setitem__("policy_owner", "kernel"),
}


@pytest.mark.parametrize("name", sorted(CHECKLIST_MUTATIONS))
def test_checklist_section_7_9_mutations_are_caught(tmp_path, monkeypatch, name):
    avc = _tree(tmp_path)
    _rewrite(avc, "internal-live-activation-checklist.yaml", CHECKLIST_MUTATIONS[name])
    findings = _run(monkeypatch, avc, "checklist")
    assert findings.errors, f"mutation {name!r} produced no finding"
    assert set(_codes(findings)) == {"activation-checklist"}, _messages(findings)


def test_section_7_9_values_moved_to_another_condition_are_not_found(
        tmp_path, monkeypatch):
    """The values are pinned on CONDITION 2 specifically — the hard-preflight
    condition that approves the regional, retention and data-control terms and
    already owns §7.9. Relocating the block onto a canary-time condition would
    move a blocker into the canary, so the check looks where the ruling put it
    and reports absence rather than hunting for the block anywhere it fits."""
    def mutate(d):
        two = next(c for c in d["conditions"] if c["number"] == 2)
        six = next(c for c in d["conditions"] if c["number"] == 6)
        six["ruled_values"] = two.pop("ruled_values")

    avc = _tree(tmp_path)
    _rewrite(avc, "internal-live-activation-checklist.yaml", mutate)
    findings = _run(monkeypatch, avc, "checklist")
    assert "no `ruled_values` block" in _messages(findings), _messages(findings)
    assert set(_codes(findings)) == {"activation-checklist"}


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
    # Same paste, different casing. The scan is case-insensitive precisely so
    # that the careless paste is caught alongside the tidy one.
    "raw_secret_pasted_in_another_casing":
        lambda d: _binding(d).__setitem__("secret_ref", "GHP_ExampleNotARealToken"),
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


@pytest.mark.parametrize("pasted", ["-----BEGIN RSA PRIVATE KEY-----",
                                    "-----begin rsa private key-----",
                                    "GHP_ExampleNotARealToken",
                                    "ghp_examplenotarealtoken",
                                    "AKIAEXAMPLENOTAREAL",
                                    "akiaexamplenotareal"])
def test_secret_markers_are_matched_regardless_of_casing(tmp_path, monkeypatch, pasted):
    """The vault-product scan normalizes and the secret scan must too, or the
    two halves of the same rule disagree about what a paste looks like."""
    avc = _tree(tmp_path)
    _rewrite(avc, "broker-server-key-binding.template.yaml",
             lambda d: d.__setitem__("source", f"held at {pasted}"))
    findings = _run(monkeypatch, avc, "binding")
    assert "raw secret marker" in _messages(findings), _messages(findings)
    assert set(_codes(findings)) == {"broker-credential"}


def test_secret_marker_scan_does_not_fire_on_ordinary_prose(tmp_path, monkeypatch):
    """The companion to the rule above, and the reason the secret markers are
    NOT squashed the way the product tokens are: squashing would reduce
    `-----begin` to `begin` and `gho_` to `gho`, and a scan that reports the
    words "beginning" and "ghost" as leaked credentials gets its findings
    dismissed wholesale."""
    avc = _tree(tmp_path)
    _rewrite(avc, "broker-server-key-binding.template.yaml",
             lambda d: d.__setitem__(
                 "source", "Beginning at the ghost of a prior rotation, "
                           "the record begins and the ghosts are gone"))
    findings = _run(monkeypatch, avc, "binding")
    assert findings.errors == [], _messages(findings)


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


def test_the_repository_artifacts_match_their_import_time_bytes():
    """Guard for this file's own method: every mutation above edits a tmp copy,
    so the shipped artifacts must be byte-identical to what they were before
    this module's tests began.

    THE BASELINE IS `_BASELINE_BYTES`, CAPTURED AT IMPORT TIME. An earlier
    version of this guard read the repository twice inside the test body and
    compared those two reads to each other, which is not a guard at all: two
    back-to-back reads of a mutated file agree with each other perfectly, so it
    would have passed on exactly the damage it was written to catch.

    This test is the readable statement of the invariant; the enforcement is
    `repository_artifacts_are_never_mutated` below, which runs at session
    teardown and therefore holds no matter what order the tests execute in."""
    drifted = sorted(name for name in COPIED
                     if (REAL_AVC / name).read_bytes() != _BASELINE_BYTES[name])
    assert not drifted, (
        f"shipped artifact(s) {drifted} differ from their import-time bytes; a "
        f"mutation escaped the tmp tree and edited the repository")
