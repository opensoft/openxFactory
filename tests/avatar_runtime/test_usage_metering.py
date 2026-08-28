"""Asynchronous per-tenant metering and threshold alerting (task 6.1.4).

Four claims are proved here: the metering is ASYNCHRONOUS (statically — the
dispatch path does not import it); the counters are per-tenant and aggregated
off the closed session records; the ruled 50/80 marks are evaluated for both
the $150-per-tenant and the $750-project figures and routed to the channel each
ruling gives them; and the alert act is the doc-health `gh issue create`
pattern, one issue per run, superseding the prior by a STRICTLY OLDER date.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from xfactory.avatar_runtime import metering
from xfactory.avatar_runtime.spend import KillReason, SessionSpendRecord
from xfactory.avatar_runtime.values import OutcomeCode

from _support import make_request

PKG = Path(__file__).resolve().parents[2] / "xfactory" / "avatar_runtime"

#: §7.10: TENANT = COHORT MEMBER, and the cohort has exactly two members.
COHORT_01 = "COHORT-01"
COHORT_02 = "COHORT-02"

HOLDER = "Brett Heap"
RUNBOOK = "docs/sops/avatar-internal-live-kill-switch.md"


def _record(tenant, session_id, usd_cents, *, reason=KillReason.NON_CEILING_TERMINAL):
    return SessionSpendRecord(
        session_id=session_id,
        tenant_ref=tenant,
        attempt_ref=f"req-{session_id}",
        billable_units=usd_cents,
        usd_cents=usd_cents,
        outcome=OutcomeCode.CONNECTED,
        reason=reason,
        cost_triggered=reason in (
            KillReason.COST_CEILING_EXCEEDED, KillReason.COST_UNCOUNTABLE
        ),
        countable=True,
        opened_at=0,
        closed_at=10,
    )


# --- asynchronous by construction ------------------------------------------ #
def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add(node.module or "")
            names.update(a.name for a in node.names)
    return names


@pytest.mark.parametrize("module", ["broker.py", "runtime.py"])
def test_the_dispatch_path_does_not_import_metering(module):
    """Metering cannot run in the dispatch path of a module that cannot see it."""
    assert "metering" not in _imported_modules(PKG / module)


def test_metering_does_not_reach_back_into_the_session_machinery():
    # The meter's only input is a list of closed spend records; it holds no
    # reference to a session, lease, grant or provider.
    imported = _imported_modules(PKG / "metering.py")
    for forbidden in ("broker", "runtime", "control", "session", "ports", "grant_cache"):
        assert forbidden not in imported
    assert ".spend" in imported or "spend" in imported


def test_a_dispatch_run_produces_records_but_no_crossings(runtime):
    for n in range(3):
        runtime.preflight(make_request(f"r{n}", session_id=f"s{n}"))
        runtime.complete_leg(f"s{n}")
    # The journal filled synchronously; nothing was metered until asked.
    assert len(runtime.spend.records) == 3
    usages = metering.aggregate_tenants(runtime.spend.records)
    assert metering.evaluate_thresholds(usages) == []


# --- per-tenant aggregation ------------------------------------------------ #
def test_counters_are_per_tenant_and_the_tenant_count_is_counted():
    records = [
        _record(COHORT_01, "s1", 4_000),
        _record(COHORT_01, "s2", 3_500),
        _record(COHORT_02, "s3", 1_000),
    ]
    usages = metering.aggregate_tenants(records)
    assert set(usages) == {COHORT_01, COHORT_02}
    assert usages[COHORT_01].usd_cents == 7_500
    assert usages[COHORT_01].session_count == 2
    assert usages[COHORT_02].usd_cents == 1_000

    project = metering.aggregate_project(usages)
    assert project.tenant_count == metering.RULED_TENANT_COUNT == 2
    assert project.usd_cents == 8_500


def test_a_malformed_record_is_skipped_rather_than_killing_the_run():
    class Foreign:
        tenant_ref = COHORT_01
        billable_units = "many"
        usd_cents = None

    usages = metering.aggregate_tenants([Foreign(), _record(COHORT_02, "s", 100)])
    assert set(usages) == {COHORT_02}


def test_records_are_aggregated_off_a_real_runtime_journal(runtime):
    from xfactory.avatar_runtime import spend as spend_mod

    runtime.preflight(make_request("r1", session_id="s1", tenant=COHORT_01))
    runtime.attribute_spend("s1", spend_mod.SESSION_BILLABLE_UNIT_CEILING)
    runtime.enforce_session_ceilings("s1")

    usages = metering.aggregate_tenants(runtime.spend.records)
    assert usages[COHORT_01].usd_cents == 300
    assert usages[COHORT_01].cost_triggered_kills == 1


# --- the ruled marks and their channels ------------------------------------ #
def test_the_ruled_figures_are_the_ruled_figures():
    assert metering.TENANT_MONTHLY_BUDGET_USD_CENTS == 15_000  # $150
    assert metering.PROJECT_MONTHLY_CAP_USD_CENTS == 75_000  # $750
    assert metering.THRESHOLD_MARKS_PCT == (50, 80, 100)


@pytest.mark.parametrize(
    "usd_cents,marks",
    [
        (7_499, []),
        (7_500, [50]),        # 50% of $150
        (12_000, [50, 80]),   # 80% of $150
        (15_000, [50, 80, 100]),
    ],
)
def test_tenant_marks_are_evaluated_at_fifty_eighty_and_the_budget(usd_cents, marks):
    usages = metering.aggregate_tenants([_record(COHORT_01, "s", usd_cents)])
    crossings = metering.evaluate_thresholds(usages)
    tenant = [c for c in crossings if c.subject_kind == "tenant"]
    assert [c.mark_pct for c in tenant] == marks


@pytest.mark.parametrize(
    "usd_cents,marks",
    [
        (37_499, []),
        (37_500, [50]),   # $375
        (60_000, [50, 80]),  # $600
        (75_000, [50, 80, 100]),
    ],
)
def test_project_marks_are_evaluated_at_fifty_eighty_and_the_cap(usd_cents, marks):
    # Split across both tenants so the project total is the sum, not one tenant.
    half = usd_cents // 2
    usages = metering.aggregate_tenants(
        [_record(COHORT_01, "s1", half), _record(COHORT_02, "s2", usd_cents - half)]
    )
    crossings = metering.evaluate_thresholds(usages)
    project = [c for c in crossings if c.subject_kind == "provider_project"]
    assert [c.mark_pct for c in project] == marks


def test_each_mark_routes_to_the_channel_its_ruling_gives_it():
    usages = metering.aggregate_tenants(
        [_record(COHORT_01, "s1", 40_000), _record(COHORT_02, "s2", 40_000)]
    )
    routed = {
        (c.subject_kind, c.mark_pct): c.channel
        for c in metering.evaluate_thresholds(usages)
    }
    # The provider's own native notifications carry the project sub-marks...
    assert routed[("provider_project", 50)] is metering.AlertChannel.PROVIDER_NATIVE_BUDGET_NOTIFICATION
    assert routed[("provider_project", 80)] is metering.AlertChannel.PROVIDER_NATIVE_BUDGET_NOTIFICATION
    # ... and the per-tenant crossing of $150 is the gh-issue path.
    assert routed[("tenant", 100)] is metering.AlertChannel.GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN
    # ... while the tenant sub-marks are metered and recorded, not paged: §7.4
    # rules the gh-issue channel at the budget itself, and paging at 50% would
    # be a trigger nobody ratified.
    assert routed[("tenant", 50)] is metering.AlertChannel.METERED_RECORDED_ONLY
    assert routed[("tenant", 80)] is metering.AlertChannel.METERED_RECORDED_ONLY


def test_the_provider_side_channels_are_recorded_as_install_side_not_emitted():
    usages = metering.aggregate_tenants([_record(COHORT_01, "s", 40_000)])
    project_crossings = [
        c for c in metering.evaluate_thresholds(usages) if c.subject_kind == "provider_project"
    ]
    assert project_crossings and all(not c.built_here for c in project_crossings)
    assert metering.INSTALL_SIDE_CHANNELS == frozenset(
        {
            metering.AlertChannel.PROVIDER_NATIVE_BUDGET_NOTIFICATION,
            metering.AlertChannel.PROVIDER_PROJECT_HARD_CAP,
        }
    )


# --- the alert act, on the doc-health pattern ------------------------------ #
def test_a_tenant_crossing_produces_one_issue_per_run():
    usages = metering.aggregate_tenants([_record(COHORT_01, "s", 15_000)])
    _, _, crossings, alert = metering.meter(
        [_record(COHORT_01, "s", 15_000)],
        "2026-08-27",
        recipient=HOLDER,
        runbook_ref=RUNBOOK,
    )
    assert alert is not None
    assert alert.title == "avatar internal-live metering 2026-08-27"
    assert alert.recipient == HOLDER and alert.runbook_ref == RUNBOOK
    assert HOLDER in alert.body() and RUNBOOK in alert.body()
    assert "metered_and_alerted" not in alert.body()
    assert "no per-tenant hard stop exists" in alert.body()
    assert usages[COHORT_01].usd_cents == 15_000
    assert any(c.mark_pct == 100 for c in crossings)


def test_any_cost_triggered_session_kill_alerts_on_its_own():
    kill = _record(COHORT_02, "s9", 300, reason=KillReason.COST_CEILING_EXCEEDED)
    _, _, _, alert = metering.meter(
        [kill], "2026-08-27", recipient=HOLDER, runbook_ref=RUNBOOK
    )
    assert alert is not None
    assert "cost_ceiling_exceeded" in alert.body()
    assert "s9" in alert.body()


def test_a_quiet_run_files_no_issue():
    _, _, _, alert = metering.meter(
        [_record(COHORT_01, "s", 100)],
        "2026-08-27",
        recipient=HOLDER,
        runbook_ref=RUNBOOK,
    )
    assert alert is None


def test_supersede_closes_only_a_strictly_older_issue():
    _, _, _, alert = metering.meter(
        [_record(COHORT_01, "s", 15_000)],
        "2026-08-27",
        recipient=HOLDER,
        runbook_ref=RUNBOOK,
    )
    assert alert.supersedes("avatar internal-live metering 2026-08-26") is True
    # Never this run's own issue — the doc-health strict-older rule verbatim.
    assert alert.supersedes("avatar internal-live metering 2026-08-27") is False
    assert alert.supersedes("avatar internal-live metering 2026-08-28") is False
    # And never an unrelated issue that merely mentions the words.
    assert alert.supersedes("doc-health regressions 2026-08-26") is False
    assert alert.supersedes("avatar internal-live metering follow-up") is False


def test_an_alert_with_no_named_recipient_is_refused():
    """§7.4's whole condition: the person who learns about the spend can stop it."""
    records = [_record(COHORT_01, "s", 15_000)]
    for missing in ("", "   "):
        with pytest.raises(metering.AlertRecipientUnresolved):
            metering.meter(records, "2026-08-27", recipient=missing, runbook_ref=RUNBOOK)
    with pytest.raises(metering.AlertRecipientUnresolved):
        metering.meter(records, "2026-08-27", recipient=HOLDER, runbook_ref="")


def test_the_recipient_is_never_hard_coded_in_the_runtime_package():
    """The holder's name lives in the policy, and in exactly one place."""
    for path in sorted(PKG.rglob("*.py")):
        assert "Brett Heap" not in path.read_text(), path


def test_a_bad_run_date_is_refused():
    with pytest.raises(ValueError):
        metering.meter(
            [_record(COHORT_01, "s", 15_000)],
            "27-08-2026",
            recipient=HOLDER,
            runbook_ref=RUNBOOK,
        )
