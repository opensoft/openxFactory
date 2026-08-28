"""ASYNCHRONOUS per-tenant usage metering and threshold alerting (task 6.1.4).

ASYNCHRONOUS BY CONSTRUCTION, NOT BY PROMISE. Every function here is a pure
function over a list of :class:`~.spend.SessionSpendRecord` — the records a
session leaves behind when its ledger closes. Nothing in this module touches a
session, a lease, a grant or a provider, and NEITHER ``broker`` NOR ``runtime``
IMPORTS IT. That import direction is the proof, and
``tests/avatar_runtime/test_usage_metering.py`` asserts it statically with
``ast`` rather than trusting the docstring: a metering call cannot appear in
the dispatch path of a module that does not import metering.

THE SUBJECT. §7.10 ruled TENANT = COHORT MEMBER, and the cohort has exactly two
members (COHORT-01 the vendor organization's internal accounts, COHORT-02 the
one internally-staffed domain sandbox), so this job meters TWO tenants. The
count is derived from the records it is given, never asserted, for the same
reason the policy's own `tenant_count` is recomputed from `cohort.members`.

THE FIGURES (§7.2, ruled 2026-08-27):

* $150 per calendar month per tenant — METERED AND ALERTED ONLY. There is no
  per-tenant hard stop at this ring; Fork 1 Option C defers the durable
  synchronous counter (task 6.1.5), and recording $150 as hard would be false.
* $750 per calendar month for the provider project — HARD at the provider,
  with the provider's own native notifications at 50% ($375) and 80% ($600).

THE MARKS AND WHERE EACH ONE GOES. Both figures are evaluated at the ruled 50%
and 80% marks and at the full budget; what differs is which channel each
crossing reaches, and the routing is read off the rulings rather than chosen
here:

===================  =======  ==================================================
subject              mark     channel
===================  =======  ==================================================
provider project     50, 80   provider-native budget notification (INSTALL-SIDE)
provider project     100      provider-project hard cap (INSTALL-SIDE)
tenant               50, 80   metered, recorded only — no alert act is ruled
tenant               100      `gh issue create` on the doc-health pattern
cost-triggered kill  n/a      `gh issue create` on the doc-health pattern
===================  =======  ==================================================

The two tenant sub-budget marks are RECORDED AND NOT PAGED deliberately. §7.4
rules the gh-issue channel to fire "on a per-tenant metered crossing of
$150/month or any cost-triggered session kill", and firing at 50% as well
would be a trigger nobody ratified. They are still computed, because they are
the telemetry ROLLBACK-C's `cost_concern` judgment is read off, and a number
with no reader is the `budget_envelopes: {}` artifact this org has already been
bitten by.

THE INSTALL-SIDE HALF IS NAMED, NOT FAKED. The provider-native notifications
are provider-project configuration on the dedicated spend-capped project that
task 6.1.2 provisions and that does not exist yet. Nothing here emits them and
nothing here pretends to; they are recorded as the named install-side half in
``contracts/avatar-client/usage-metering-and-alerting.yaml``, and
:data:`INSTALL_SIDE_CHANNELS` is the machine-readable half of that statement.

THE RECIPIENT IS INJECTED, NEVER COPIED. §7.7 names a PERSON as the holder of
both kill switches and §7.4 makes that same person the alert's page target.
`canary-cohort-and-rollback-policy.yaml` `operator_surface.holder` is the ONE
place that name is written down, so :func:`build_alert` takes the recipient as
an argument and refuses to build an alert without one — see
:class:`AlertRecipientUnresolved`. ``scripts/avatar-metering-alert.py`` reads
it from the policy at run time. No literal copy of the name appears anywhere in
this package, in code or in prose — that is the drift §7.4 and §7.7 exist to
prevent, and ``test_usage_metering.py`` greps the whole package for it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional, Sequence

from .spend import SessionSpendRecord


# --------------------------------------------------------------------------- #
# The ruled budgets (§7.2) and marks
# --------------------------------------------------------------------------- #
#: $150 per calendar month, per tenant. Metered and alerted only.
TENANT_MONTHLY_BUDGET_USD_CENTS = 15_000

#: $750 per calendar month for the dedicated provider project. Hard at the
#: provider — this module observes it, the provider enforces it.
PROJECT_MONTHLY_CAP_USD_CENTS = 75_000

#: The ruled notification marks, plus the budget itself.
THRESHOLD_MARKS_PCT = (50, 80, 100)

#: The ruled tenant count, derived from §7.10's tenant = cohort member and the
#: cohort's two members. Recorded for a reader; every function recomputes the
#: observed count from its input rather than trusting this.
RULED_TENANT_COUNT = 2


class AlertChannel(Enum):
    """CLOSED registry of the channels §7.4 ruled. No channel is added here."""

    #: The provider project's own native budget notification. INSTALL-SIDE.
    PROVIDER_NATIVE_BUDGET_NOTIFICATION = "provider_native_budget_notification"
    #: The provider project's hard cap. INSTALL-SIDE; the ring's only
    #: per-tenant hard stop until task 6.1.5's durable counter lands.
    PROVIDER_PROJECT_HARD_CAP = "provider_project_hard_cap"
    #: `gh issue create` from the metering job, one issue per run,
    #: supersede-and-close the prior — the doc-health pattern verbatim.
    GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN = "gh_issue_on_the_doc_health_pattern"
    #: Computed and recorded; no alert act is ruled for it.
    METERED_RECORDED_ONLY = "metered_recorded_only"


#: Channels this repository does NOT build and does not pretend to emit. They
#: are provider-project configuration on the install task 6.1.2 provisions.
INSTALL_SIDE_CHANNELS = frozenset(
    {
        AlertChannel.PROVIDER_NATIVE_BUDGET_NOTIFICATION,
        AlertChannel.PROVIDER_PROJECT_HARD_CAP,
    }
)

#: The doc-health issue title shape, transposed. One issue per run; the prior
#: run's issue is superseded and closed by a STRICTLY-OLDER date comparison, so
#: the current run can never close its own issue.
ALERT_TITLE_PREFIX = "avatar internal-live metering"
ALERT_TITLE_PATTERN = r"^avatar internal-live metering (\d{4}-\d{2}-\d{2})$"
_RUN_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class AlertRecipientUnresolved(ValueError):
    """No named recipient could be resolved for a metering alert.

    Fails closed on the exact gap §7.4 and §7.7 were ruled to close. An alert
    with no named recipient and a kill switch with no named holder were
    recorded as one gap seen twice; a metering job that emitted an
    unaddressed issue would re-open it quietly.
    """


# --------------------------------------------------------------------------- #
# Aggregation — off the session records, and off nothing else
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class TenantUsage:
    tenant_ref: str
    session_count: int
    billable_units: int
    usd_cents: int
    cost_triggered_kills: int
    uncountable_sessions: int

    @property
    def budget_pct(self) -> int:
        """Whole percent of the ruled per-tenant budget, rounded DOWN.

        Rounding down is the conservative direction for a MARK: it never
        reports a crossing that has not happened.
        """
        return (self.usd_cents * 100) // TENANT_MONTHLY_BUDGET_USD_CENTS


@dataclass(frozen=True)
class ProjectUsage:
    tenant_count: int
    session_count: int
    usd_cents: int
    cost_triggered_kills: int

    @property
    def cap_pct(self) -> int:
        return (self.usd_cents * 100) // PROJECT_MONTHLY_CAP_USD_CENTS


@dataclass(frozen=True)
class ThresholdCrossing:
    subject_kind: str  # "tenant" | "provider_project"
    subject_ref: str
    mark_pct: int
    budget_usd_cents: int
    observed_usd_cents: int
    channel: AlertChannel

    @property
    def built_here(self) -> bool:
        """False for the halves that belong to the serving install."""
        return self.channel not in INSTALL_SIDE_CHANNELS

    def alert_line(self) -> str:
        return (
            f"- [{self.subject_kind}] {self.subject_ref} crossed {self.mark_pct}% "
            f"of {self.budget_usd_cents} usd_cents "
            f"(observed {self.observed_usd_cents}) -> {self.channel.value}"
        )


def aggregate_tenants(
    records: Iterable[SessionSpendRecord],
) -> dict[str, TenantUsage]:
    """Per-tenant counters, aggregated off the closed session spend records.

    A malformed or foreign object in the input is SKIPPED rather than crashing
    the job: a metering run that dies on one bad record delivers no alert at
    all, which is strictly worse than delivering the alert the good records
    justify. Skipped objects are simply absent from the result.
    """
    totals: dict[str, list[int]] = {}
    for rec in records:
        tenant = getattr(rec, "tenant_ref", None)
        units = getattr(rec, "billable_units", None)
        cents = getattr(rec, "usd_cents", None)
        if not isinstance(tenant, str) or not tenant:
            continue
        if not isinstance(units, int) or isinstance(units, bool) or units < 0:
            continue
        if not isinstance(cents, int) or isinstance(cents, bool) or cents < 0:
            continue
        slot = totals.setdefault(tenant, [0, 0, 0, 0, 0])
        slot[0] += 1
        slot[1] += units
        slot[2] += cents
        slot[3] += 1 if getattr(rec, "cost_triggered", False) else 0
        slot[4] += 0 if getattr(rec, "countable", True) else 1
    return {
        tenant: TenantUsage(
            tenant_ref=tenant,
            session_count=slot[0],
            billable_units=slot[1],
            usd_cents=slot[2],
            cost_triggered_kills=slot[3],
            uncountable_sessions=slot[4],
        )
        for tenant, slot in sorted(totals.items())
    }


def aggregate_project(usages: dict[str, TenantUsage]) -> ProjectUsage:
    """Ring-level totals. The tenant count is COUNTED, never assumed."""
    return ProjectUsage(
        tenant_count=len(usages),
        session_count=sum(u.session_count for u in usages.values()),
        usd_cents=sum(u.usd_cents for u in usages.values()),
        cost_triggered_kills=sum(u.cost_triggered_kills for u in usages.values()),
    )


def _tenant_channel(mark_pct: int) -> AlertChannel:
    # §7.4 rules the gh-issue channel at the metered crossing of the budget
    # itself. The sub-budget marks are computed and recorded; paging on one
    # would be a trigger nobody ratified.
    if mark_pct >= 100:
        return AlertChannel.GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN
    return AlertChannel.METERED_RECORDED_ONLY


def _project_channel(mark_pct: int) -> AlertChannel:
    if mark_pct >= 100:
        return AlertChannel.PROVIDER_PROJECT_HARD_CAP
    return AlertChannel.PROVIDER_NATIVE_BUDGET_NOTIFICATION


def evaluate_thresholds(
    usages: dict[str, TenantUsage], project: Optional[ProjectUsage] = None
) -> list[ThresholdCrossing]:
    """Every ruled mark crossed, for both budget subjects, in a stable order.

    A crossing is reported for a mark when the observed spend REACHES it, so a
    tenant at exactly $150.00 has crossed 100% — a budget that reports itself
    uncrossed at its own figure is a budget nobody is watching.
    """
    project = project if project is not None else aggregate_project(usages)
    out: list[ThresholdCrossing] = []
    for tenant_ref, usage in sorted(usages.items()):
        for mark in THRESHOLD_MARKS_PCT:
            if usage.usd_cents * 100 >= TENANT_MONTHLY_BUDGET_USD_CENTS * mark:
                out.append(
                    ThresholdCrossing(
                        subject_kind="tenant",
                        subject_ref=tenant_ref,
                        mark_pct=mark,
                        budget_usd_cents=TENANT_MONTHLY_BUDGET_USD_CENTS,
                        observed_usd_cents=usage.usd_cents,
                        channel=_tenant_channel(mark),
                    )
                )
    for mark in THRESHOLD_MARKS_PCT:
        if project.usd_cents * 100 >= PROJECT_MONTHLY_CAP_USD_CENTS * mark:
            out.append(
                ThresholdCrossing(
                    subject_kind="provider_project",
                    subject_ref="internal_live_provider_project",
                    mark_pct=mark,
                    budget_usd_cents=PROJECT_MONTHLY_CAP_USD_CENTS,
                    observed_usd_cents=project.usd_cents,
                    channel=_project_channel(mark),
                )
            )
    return out


# --------------------------------------------------------------------------- #
# The alert act — the gh-issue payload, on the doc-health pattern
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class MeteringAlert:
    """The payload a `gh issue create` step consumes. This package NEVER runs it.

    The runtime side of §7.4 is producing this value; invoking `gh` belongs to
    the metering job, exactly as the doc-health nightly's Python writes
    ``issue-body.md`` and a separate workflow step runs ``gh issue create
    --body-file``.
    """

    run_date: str
    title: str
    body_lines: tuple[str, ...]
    recipient: str
    runbook_ref: str
    supersede_title_pattern: str
    channel: AlertChannel

    def body(self) -> str:
        return "\n".join(self.body_lines) + "\n"

    def supersedes(self, other_title: str) -> bool:
        """True for a STRICTLY OLDER prior issue — never this run's own.

        The strict-older comparison is the doc-health rule verbatim; ISO dates
        compare correctly as strings, and equality is excluded so a run cannot
        close the issue it just opened.
        """
        match = re.match(self.supersede_title_pattern, other_title or "")
        return bool(match) and match.group(1) < self.run_date


def build_alert(
    run_date: str,
    crossings: Sequence[ThresholdCrossing],
    cost_kills: Sequence[SessionSpendRecord],
    *,
    recipient: str,
    runbook_ref: str,
) -> Optional[MeteringAlert]:
    """One alert per metering run, or None when nothing reached the channel.

    Raises :class:`AlertRecipientUnresolved` when the recipient or the runbook
    reference is missing. That is deliberate: §7.4's whole condition was that
    the person who learns about the spend is the person who can stop it, so an
    alert that cannot name either is refused rather than sent unaddressed.
    """
    if not isinstance(recipient, str) or not recipient.strip():
        raise AlertRecipientUnresolved(
            "no recipient resolved from rollback_policy.operator_surface.holder"
        )
    if not isinstance(runbook_ref, str) or not runbook_ref.strip():
        raise AlertRecipientUnresolved(
            "no runbook resolved from rollback_policy.operator_surface.mechanism_ref"
        )
    if not _RUN_DATE_RE.match(run_date or ""):
        raise ValueError(f"run_date must be an ISO calendar date, got {run_date!r}")

    paged = [c for c in crossings if c.channel is AlertChannel.GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN]
    kills = [k for k in cost_kills if getattr(k, "cost_triggered", False)]
    if not paged and not kills:
        return None

    lines: list[str] = [
        f"Metered per-tenant spend and cost-triggered session kills for {run_date}.",
        f"Escalation: {recipient} — runbook {runbook_ref}",
        "",
    ]
    if paged:
        lines.append("Per-tenant metered budget crossings:")
        lines.extend(c.alert_line() for c in paged)
        lines.append("")
    if kills:
        lines.append("Cost-triggered session kills:")
        lines.extend(
            f"- [{k.tenant_ref}] session {k.session_id} {k.reason.value} "
            f"units={k.billable_units} usd_cents={k.usd_cents} "
            f"outcome={k.outcome.value}"
            for k in kills
        )
        lines.append("")
    lines.append(
        "The per-tenant budget is METERED AND ALERTED ONLY: no per-tenant hard "
        "stop exists at this ring, and the provider-project cap is the only "
        "per-tenant hard stop until task 6.1.5's durable counter lands."
    )
    return MeteringAlert(
        run_date=run_date,
        title=f"{ALERT_TITLE_PREFIX} {run_date}",
        body_lines=tuple(lines),
        recipient=recipient,
        runbook_ref=runbook_ref,
        supersede_title_pattern=ALERT_TITLE_PATTERN,
        channel=AlertChannel.GH_ISSUE_ON_THE_DOC_HEALTH_PATTERN,
    )


def meter(
    records: Iterable[SessionSpendRecord],
    run_date: str,
    *,
    recipient: str,
    runbook_ref: str,
) -> tuple[dict[str, TenantUsage], ProjectUsage, list[ThresholdCrossing], Optional[MeteringAlert]]:
    """The whole metering run, as one pure function over closed session records."""
    materialized = list(records)
    usages = aggregate_tenants(materialized)
    project = aggregate_project(usages)
    crossings = evaluate_thresholds(usages, project)
    kills = [r for r in materialized if getattr(r, "cost_triggered", False)]
    alert = build_alert(
        run_date, crossings, kills, recipient=recipient, runbook_ref=runbook_ref
    )
    return usages, project, crossings, alert
