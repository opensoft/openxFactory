"""The project-register-edit fulfilment LANE (add-register-edit-lane).

Automates "step 2" of the project commission loop (Brett's 2026-08-06
ruling: "we need an update button plus a job that watches"): dispatched
`project-register-edit` descriptors — recorded by the create-project and
edit-project gate verbs — are APPLIED to the aggregation-owned
`project-register.yaml`, validated against the pinned schema BEFORE the
write, stamped `delivered`, and the register file alone is committed and
pushed (explicit pathspec: the shared aggregation checkout routinely
carries other sessions' uncommitted work).

Fail-closed everywhere: a commission the live register can no longer
satisfy (the project vanished, a member conflict arose), a validation
failure, or a git failure leaves the descriptor `dispatched` and reports —
nothing is half-applied silently. Only RECORDED commissions are ever
applied, which is what keeps D2's boundary intact even when the serve runs
this code behind the header's apply button.

Three entrypoints, one core:
  * ``fulfil_once(repo_root)``    — one pass (the serve route calls this);
  * ``--watch --interval N``      — the polling job beside a serve;
  * plain CLI                     — one pass from a terminal.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import yaml

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:  # plain-script parity with serve.py (D12)
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ideation_dashboard.gate_console import DEFAULT_RECORDS_DIR  # noqa: E402
from ideation_dashboard.kickoff import (  # noqa: E402
    dispatched_commissions,
    discover_project_register,
)

DELIVERED_BY = "register-edit-lane"
#: The two verbs whose descriptors this lane consumes, applied oldest-first.
PROJECT_VERBS = ("create-project", "edit-project")
_VALIDATOR = _SCRIPTS_DIR.parent / "scripts" / "validate-ideation-dashboard-contracts.py"


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------
# surgical register edits — line-based, scoped to one project's block, so
# the register's curated comments survive (a yaml round-trip would not
# preserve them)
# --------------------------------------------------------------------------

def _project_block(lines: list[str], project_id: str) -> tuple[int, int] | None:
    """[start, end) line span of one project's entry under `projects:`."""
    start = None
    for i, line in enumerate(lines):
        if line.rstrip() == f"  - id: {project_id}":
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        stripped = lines[j]
        if stripped.startswith("  - id: ") or (
                stripped and not stripped.startswith((" ", "#", "\n"))):
            end = j
            break
    return start, end


def _member_lines(lines: list[str], start: int, end: int) -> list[int]:
    return [i for i in range(start, end)
            if lines[i].startswith("      - ")]


def apply_create(text: str, job: dict) -> tuple[str | None, str | None]:
    """Append the commissioned project; (new_text, None) or (None, reason)."""
    project_id = str(job.get("project_id") or "")
    if not project_id:
        return None, "descriptor carries no project_id"
    lines = text.splitlines(keepends=True)
    if _project_block(lines, project_id) is not None:
        return None, f"project {project_id!r} already exists in the register"
    members = [str(r) for r in (job.get("repositories") or [])]
    block = [f"  - id: {project_id}\n"]
    name = job.get("project_name")
    if name:
        block.append(f"    name: {name}\n")
    if members:
        block.append("    repositories:\n")
        block.extend(f"      - {m}\n" for m in members)
    else:
        # an empty project is legal (D17): created first, populated later
        block.append("    repositories: []\n")
    # insertion point: after the LAST project entry, before any
    # project_groups section or the trailing group-stub comment
    insert = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("project_groups:") or line.startswith("# No project groups"):
            insert = i
            break
    while insert > 0 and lines[insert - 1].strip() == "":
        insert -= 1
    return "".join(lines[:insert] + block + lines[insert:]), None


def apply_edit(text: str, job: dict) -> tuple[str | None, str | None]:
    """Apply add/remove member lists inside one project's block."""
    project_id = str(job.get("project_id") or "")
    lines = text.splitlines(keepends=True)
    span = _project_block(lines, project_id)
    if span is None:
        return None, f"project {project_id!r} is not in the register"
    start, end = span
    added = [str(r) for r in (job.get("add") or [])]
    removed = [str(r) for r in (job.get("remove") or [])]
    current = {lines[i].strip()[2:]: i for i in _member_lines(lines, start, end)}

    stale_add = [a for a in added if a in current]
    if stale_add:
        return None, "already a member: " + ", ".join(stale_add)
    stale_rm = [r for r in removed if r not in current]
    if stale_rm:
        return None, "not currently a member: " + ", ".join(stale_rm)

    drop = {current[r] for r in removed}
    out = [line for i, line in enumerate(lines) if i not in drop]

    if added:
        # re-locate after removals, then place additions at the block's end
        span = _project_block(out, project_id)
        start, end = span
        rep_line = None
        for i in range(start, end):
            if out[i].startswith("    repositories:"):
                rep_line = i
                break
        addition = [f"      - {a}\n" for a in added]
        if rep_line is None:
            out[end:end] = ["    repositories:\n"] + addition
        elif out[rep_line].strip() == "repositories: []":
            out[rep_line] = "    repositories:\n"
            out[rep_line + 1:rep_line + 1] = addition
        else:
            members = _member_lines(out, start, end)
            at = (members[-1] + 1) if members else rep_line + 1
            out[at:at] = addition
    return "".join(out), None


APPLIERS = {"create-project": apply_create, "edit-project": apply_edit}


# --------------------------------------------------------------------------
# the pass
# --------------------------------------------------------------------------

@dataclass
class LaneReport:
    register: str | None = None
    applied: list = field(default_factory=list)     # [(verb, project_id)]
    skipped: list = field(default_factory=list)     # [(verb, project_id, reason)]
    committed: str | None = None
    pushed: bool = False
    error: str | None = None

    def as_dict(self) -> dict:
        return {"register": self.register,
                "applied": [list(a) for a in self.applied],
                "skipped": [list(s) for s in self.skipped],
                "committed": self.committed, "pushed": self.pushed,
                "error": self.error}


def _pending(records_root: Path) -> list[tuple[str, str, Path, dict]]:
    """Every dispatched project-verb descriptor, oldest dispatch first."""
    rows = []
    for verb in PROJECT_VERBS:
        for pid, path in dispatched_commissions(records_root, verb).items():
            try:
                doc = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                continue
            if isinstance(doc, dict):
                rows.append((verb, pid, path, doc))
    rows.sort(key=lambda r: str(r[3].get("dispatched_at") or ""))
    return rows


def _validates(text: str, scratch: Path) -> tuple[bool, str]:
    scratch.write_text(text, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(_VALIDATOR), str(scratch)],
                          capture_output=True, text=True, timeout=120)
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


def _flip_delivered(path: Path, at: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "status: dispatched",
        f"status: delivered\ndelivered_at: '{at}'\ndelivered_by: {DELIVERED_BY}",
        1)
    path.write_text(text, encoding="utf-8")


def _git(register: Path, message: str, report: LaneReport) -> None:
    """Commit ONLY the register file and push, pull-rebase-retry once."""
    repo = register.parent
    name = register.name

    def run(*args):
        return subprocess.run(["git", "-C", str(repo), *args],
                              capture_output=True, text=True, timeout=180)

    if run("diff", "--quiet", "--", name).returncode == 0:
        return                                    # nothing to commit
    if run("add", "--", name).returncode != 0:
        report.error = "git add failed"
        return
    commit = run("commit", "-m", message, "--", name)
    if commit.returncode != 0:
        report.error = "git commit failed: " + commit.stderr.strip()[:200]
        return
    report.committed = run("rev-parse", "HEAD").stdout.strip()[:12]
    for _ in range(2):
        push = run("push")
        if push.returncode == 0:
            report.pushed = True
            return
        run("pull", "--rebase")
    report.error = "git push failed after rebase retry"


def fulfil_once(repo_root: Path | str, *, git: bool = True,
                delivered_by: str = DELIVERED_BY) -> LaneReport:
    """One lane pass. Descriptors flip ONLY after the register write lands
    (and, when git is on, only after the push) — a git failure leaves every
    consumed commission dispatched, per Brett's ruling."""
    report = LaneReport()
    root = Path(repo_root).resolve()
    register = discover_project_register(root)
    if register is None:
        report.error = "no project register reachable from the checkout"
        return report
    report.register = str(register)
    records_root = root / DEFAULT_RECORDS_DIR

    text = register.read_text(encoding="utf-8")
    consumed: list[tuple[str, str, Path]] = []
    scratch = register.parent / (register.name + ".lane-candidate")
    try:
        for verb, pid, path, job in _pending(records_root):
            new_text, reason = APPLIERS[verb](text, job)
            if new_text is None:
                report.skipped.append((verb, pid, reason))
                continue
            ok, msg = _validates(new_text, scratch)
            if not ok:
                report.skipped.append((verb, pid, "validation failed: " + msg[-200:]))
                continue
            text = new_text
            consumed.append((verb, pid, path))
    finally:
        scratch.unlink(missing_ok=True)

    if not consumed:
        return report
    register.write_text(text, encoding="utf-8")
    if git:
        ids = ", ".join(f"{v} {p}" for v, p, _ in consumed)
        _git(register, "Fulfil project-register commissions: " + ids
             + "\n\nApplied by the register-edit lane "
               "(openxFactory add-register-edit-lane); validated against "
               "the pinned schema.\n\n"
               "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>",
             report)
        if report.error:
            return report                        # descriptors stay dispatched
    at = _utcnow()
    for verb, pid, path in consumed:
        _flip_delivered(path, at)
        report.applied.append((verb, pid))
    return report


def watch(repo_root: Path | str, *, interval: float = 30.0,
          git: bool = True) -> None:  # pragma: no cover - thin loop over fulfil_once
    """The job that watches: fulfil, sleep, repeat. Ctrl-C to stop."""
    while True:
        report = fulfil_once(repo_root, git=git)
        for verb, pid in report.applied:
            print(f"applied  {verb} {pid}", flush=True)
        for verb, pid, reason in report.skipped:
            print(f"skipped  {verb} {pid}: {reason}", flush=True)
        if report.error:
            print(f"error    {report.error}", flush=True)
        time.sleep(interval)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True,
                        help="the served corpus checkout (records live here; "
                             "the register is discovered upward)")
    parser.add_argument("--watch", action="store_true",
                        help="poll instead of a single pass")
    parser.add_argument("--interval", type=float, default=30.0,
                        help="watch polling interval, seconds (default 30)")
    parser.add_argument("--no-git", action="store_true",
                        help="apply + flip only; leave commit/push to a human")
    args = parser.parse_args(argv)
    if args.watch:
        watch(args.repo_root, interval=args.interval, git=not args.no_git)
        return 0
    report = fulfil_once(args.repo_root, git=not args.no_git)
    for verb, pid in report.applied:
        print(f"applied  {verb} {pid}")
    for verb, pid, reason in report.skipped:
        print(f"skipped  {verb} {pid}: {reason}")
    if report.committed:
        print(f"committed {report.committed} (pushed={report.pushed})")
    if report.error:
        print(f"error: {report.error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
