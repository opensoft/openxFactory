#!/usr/bin/env python3
"""Render the avatar internal-live metering alert (qualify-avatar-live-voice 6.1.4).

THE PYTHON HALF OF THE DOC-HEALTH PATTERN. The nightly doc-health job splits
its alert in two: a Python half that computes the findings and writes
``issue-body.md``, and a workflow step that runs ``gh issue create
--body-file``. This is the metering equivalent's Python half. It reads a
metering input file, aggregates per-tenant counters, evaluates the ruled
50/80/100 marks against the $40-per-tenant and $100-project figures, and
writes the issue body plus the title. IT NEVER INVOKES ``gh`` ITSELF, exactly
as ``dashboard-refresh-nightly.py`` and the doc-health checker never do.

THE RECIPIENT IS READ FROM THE POLICY, NEVER FROM A COPY.
``contracts/avatar-client/canary-cohort-and-rollback-policy.yaml``
``rollback_policy.operator_surface.holder`` is the one place the page target's
name is written down, and ``mechanism_ref`` beside it is the runbook the alert
escalates into. §7.7 made that holder the same person who holds both kill
switches, so reading both from one place is what keeps the alert's recipient
and the switch's holder from drifting apart. A missing value FAILS CLOSED:
this script exits non-zero rather than filing an unaddressed issue.

THE INPUT does not exist yet. Task 6.1.2 provisions the serving install and
its dedicated spend-capped provider project; until it lands there is no
metering job and no data for one, so no scheduled workflow is committed for
this script. Writing one that reads nothing would be a fabricated procedure —
the same call ``docs/sops/avatar-internal-live-kill-switch.md`` makes about
the concrete kill-switch command.

Input file (JSON), one object per CLOSED session, as produced by the serving
broker's spend journal:

    {"sessions": [
       {"session_id": "...", "tenant_ref": "COHORT-01", "attempt_ref": "...",
        "billable_units": 42, "usd_cents": 42, "outcome": "connected",
        "reason": "non_ceiling_terminal", "cost_triggered": false,
        "countable": true, "opened_at": 0, "closed_at": 120}
    ]}

Usage:
    python3 scripts/avatar-metering-alert.py --input run.json --run-date 2026-08-27
    python3 scripts/avatar-metering-alert.py --input run.json --run-date ... \\
        --body-file issue-body.md --print-gh-command

Exit codes: 0 an alert was rendered, 3 nothing crossed a paging threshold
(a quiet run files no issue), 2 a harness or fail-closed error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from xfactory.avatar_runtime import metering  # noqa: E402
from xfactory.avatar_runtime.spend import KillReason, SessionSpendRecord  # noqa: E402
from xfactory.avatar_runtime.values import OutcomeCode  # noqa: E402

POLICY = ROOT / "contracts" / "avatar-client" / "canary-cohort-and-rollback-policy.yaml"

QUIET_RUN = 3
HARNESS_ERROR = 2


class FailClosed(RuntimeError):
    """A value the alert cannot honestly be sent without."""


def _load_policy(policy_path: Path) -> dict:
    """Parse the recorded policy, NAMING the file when it does not parse.

    The same boundary `validate-avatar-client.py`'s `MalformedYAML` draws: a
    parser error is caught at the read and re-raised as this script's own
    fail-closed error carrying the file's identity, so an unreadable policy
    exits with the harness code and a sentence a human can act on rather than
    a `yaml.scanner.ScannerError` traceback. A policy that cannot be parsed is
    a policy whose named recipient cannot be read, which is exactly the
    condition §7.4 refuses to send an alert under.
    """
    try:
        text = policy_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise FailClosed(f"cannot read recorded policy {policy_path}: {exc}") from exc
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise FailClosed(
            f"recorded policy {policy_path} does not parse as YAML: {exc}"
        ) from exc
    if doc is None:
        raise FailClosed(f"recorded policy {policy_path} is empty")
    if not isinstance(doc, dict):
        raise FailClosed(
            f"recorded policy {policy_path} must be a mapping, "
            f"got {type(doc).__name__}"
        )
    return doc


def operator_surface(policy_path: Path = POLICY) -> tuple[str, str]:
    """Read the page target and its runbook from the recorded policy.

    Fails closed on an absent file, an unparseable one, an unnamed surface, or
    a missing mechanism reference. §7.4's condition was that the person who
    learns about the spend is the person who can stop it, so an alert that
    cannot name either is refused rather than sent unaddressed.
    """
    if not policy_path.is_file():
        raise FailClosed(f"recorded policy not found at {policy_path}")
    doc = _load_policy(policy_path)
    rollback_policy = doc.get("rollback_policy")
    if not isinstance(rollback_policy, dict):
        raise FailClosed(
            f"recorded policy {policy_path} carries no `rollback_policy` mapping"
        )
    surface = rollback_policy.get("operator_surface")
    if not isinstance(surface, dict):
        raise FailClosed(
            f"recorded policy {policy_path} carries no "
            f"`rollback_policy.operator_surface` mapping"
        )
    if surface.get("status") != "named":
        raise FailClosed(
            "rollback_policy.operator_surface.status is not 'named'; "
            "§7.7 requires a named holder before the canary opens"
        )
    holder = surface.get("holder")
    runbook = surface.get("mechanism_ref")
    if not holder or not runbook:
        raise FailClosed(
            "rollback_policy.operator_surface must carry both holder and mechanism_ref"
        )
    return str(holder), str(runbook)


def _record(raw: dict) -> SessionSpendRecord:
    return SessionSpendRecord(
        session_id=str(raw["session_id"]),
        tenant_ref=str(raw["tenant_ref"]),
        attempt_ref=str(raw.get("attempt_ref", "")),
        billable_units=int(raw["billable_units"]),
        usd_cents=int(raw["usd_cents"]),
        outcome=OutcomeCode(raw.get("outcome", "connected")),
        reason=KillReason(raw.get("reason", KillReason.NON_CEILING_TERMINAL.value)),
        cost_triggered=bool(raw.get("cost_triggered", False)),
        countable=bool(raw.get("countable", True)),
        opened_at=int(raw.get("opened_at", 0)),
        closed_at=int(raw.get("closed_at", 0)),
    )


def load_records(path: Path) -> list[SessionSpendRecord]:
    """Parse the metering input. A malformed session is skipped, not fatal.

    A metering run that dies on one bad session delivers no alert at all,
    which is strictly worse than delivering the alert the good sessions
    justify.
    """
    doc = json.loads(path.read_text(encoding="utf-8"))
    out: list[SessionSpendRecord] = []
    for raw in doc.get("sessions", []):
        try:
            out.append(_record(raw))
        except (KeyError, TypeError, ValueError) as exc:
            print(f"  skipped a malformed session record: {exc}", file=sys.stderr)
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path,
                        help="metering input JSON produced by the serving broker")
    parser.add_argument("--run-date", required=True,
                        help="ISO calendar date of this metering run")
    parser.add_argument("--body-file", type=Path, default=None,
                        help="write the issue body here (doc-health's issue-body.md)")
    parser.add_argument("--title-file", type=Path, default=None,
                        help="write the issue title here")
    parser.add_argument("--policy", type=Path, default=POLICY,
                        help="the recorded policy the recipient is read from")
    parser.add_argument("--print-gh-command", action="store_true",
                        help="print the `gh issue create` line the job step runs")
    parser.add_argument("--repo", default="opensoft/openxFactory",
                        help="repository the issue is filed against")
    args = parser.parse_args(argv)

    try:
        recipient, runbook = operator_surface(args.policy)
    except FailClosed as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return HARNESS_ERROR
    try:
        records = load_records(args.input)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL-CLOSED: cannot read metering input: {exc}", file=sys.stderr)
        return HARNESS_ERROR

    try:
        usages, project, crossings, alert = metering.meter(
            records, args.run_date, recipient=recipient, runbook_ref=runbook
        )
    except metering.AlertRecipientUnresolved as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return HARNESS_ERROR
    except ValueError as exc:
        print(f"FAIL-CLOSED: {exc}", file=sys.stderr)
        return HARNESS_ERROR

    print(
        f"avatar-metering-alert: {len(records)} closed sessions, "
        f"{project.tenant_count} tenant(s), {project.usd_cents} usd_cents, "
        f"{len(crossings)} threshold crossing(s)"
    )
    for tenant_ref, usage in sorted(usages.items()):
        print(f"  {tenant_ref}: {usage.usd_cents} usd_cents "
              f"({usage.budget_pct}% of budget), "
              f"{usage.cost_triggered_kills} cost-triggered kill(s)")
    for crossing in crossings:
        marker = "" if crossing.built_here else "  [install-side]"
        print(f"  {crossing.alert_line()}{marker}")

    if alert is None:
        print("No per-tenant crossing and no cost-triggered kill — no issue filed.")
        return QUIET_RUN

    if args.body_file is not None:
        args.body_file.write_text(alert.body(), encoding="utf-8")
        print(f"  issue body -> {args.body_file}")
    if args.title_file is not None:
        args.title_file.write_text(alert.title + "\n", encoding="utf-8")
    if args.print_gh_command:
        body = args.body_file or Path("issue-body.md")
        print(
            f'gh issue create --title "{alert.title}" '
            f'--body-file {body} --repo "{args.repo}"'
        )
    print(f"  title: {alert.title}")
    print(f"  supersedes prior issues matching: {alert.supersede_title_pattern}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
