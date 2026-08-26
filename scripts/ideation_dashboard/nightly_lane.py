"""Nightly ideation-dashboard snapshot lane (openxFactory change
`add-ideation-dashboard`, task 4.1 — the xFactory aggregation nightly).

Runs AFTER the deterministic doc-health pass in the aggregation nightly
(the in-repo reusable `doc-health-reusable.yml` finalize job, called by the
aggregation repo's thin `doc-health-nightly.yml`) and refreshes the CURRENT
v1-scope snapshot — the pinned openxFactory checkout projected by the
deterministic generator — beside the dated doc-health reports:

    health/ideation-dashboard/<repository>-snapshot.json
        the current snapshot, overwritten nightly (delivery requirements
        R11/R14: one current artifact; history lives in git, not dated copies)
    health/ideation-dashboard/lane-status.json
        this run's outcome: ``ok``, or ``skipped`` with the reason
    health/ideation-dashboard/index.json          (``--repositories`` runs)
        the snapshot INDEX — the thin (repository, ref) locator the repository
        selector reads and a refresh re-fetches (openxFactory
        ``ideation-dashboard-snapshot-index``; add-dashboard-repo-selector task
        3.1). Only ``main`` snapshots ever enter it; the writer refuses any
        other ref (task 2.3)
    health/ideation-dashboard/index-status.json   (``--repositories`` runs)
        which repositories published into the index and which were skipped

PER-REPOSITORY ITERATION (add-dashboard-repo-selector). ``--repositories`` runs
the SAME generator once per registered repository and then writes the index.
This is a loop, not a redesign: the 2026-07-25 domain drive snapshot
MedxFactory, AdxFactory, and LedgerxFactory with the UNMODIFIED generator, so
neutrality was never the missing piece — the selector, the per-repository
snapshots, and the index were. The project register is the roster (design D9),
so adding a repository is a register edit plus a lane run: no code change and no
image change.

The lane itself STAGES AND COMMITS NOTHING: the nightly host's existing
"Commit report" step (``git add health/``) sweeps these files into the same
commit that lands the dated reports and inventories — exactly the reports'
emission pattern.

FAILURE SEMANTICS (task 4.1): any error — a missing checkout, an unresolvable
pin, a generator crash, a snapshot the pinned validator rejects — makes the
lane report SKIPPED (reason in ``lane-status.json`` and on stdout) and exit 0,
so the deterministic doc-health results are NEVER affected. A skipped run
leaves the previously committed snapshot in place (still the last good current
snapshot): the fresh render is written to a ``.candidate`` sibling and only
replaces the published file after the pinned validator accepts it.

DETERMINISM: the published SNAPSHOT is byte-identical per pin state —
``generation.source_revision`` is the pinned checkout's HEAD sha and the
generator derives any snapshot ``generated_at`` from that revision's commit
date, never the wall clock — so it only diffs when the pin/tree actually
changes. The lane-status artifact is diagnostic, not a projection: it
additionally carries a wall-clock ``generated_at`` and a ``run_id`` (the CI
run) so a rerun's status reflects the run that produced it. The same-day
commit step stages ``health/`` and commits only a real tree diff, so a
refreshed status is a wanted change and never a spurious one.

DIAGNOSIS RETENTION: when the pinned validator rejects the render, its per-error
output is captured into the status ``detail`` (capped) so the one-line reason is
not the whole record. Documents the generator had to exclude (missing/unparseable
Status header) are reported in ``excluded_documents`` on both the ok and skipped
outcomes — the dashboard is a projection and must degrade per-document rather
than be DoSed by a single unheadered doc.

Project grouping (D10): the aggregation root's ``project-register.yaml`` seed
instance is passed to the generator explicitly (the generator's own discovery
looks only under the scanned repo root, which is the openxFactory checkout,
not the aggregation root). A missing register is legal — the repository
renders ungrouped, per the register contract.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ideation_dashboard import register as register_mod  # noqa: E402
from ideation_dashboard import snapshot as snapshot_mod  # noqa: E402
from ideation_dashboard import snapshot_registry as registry_mod  # noqa: E402
from ideation_dashboard.boundary import OutputBoundary  # noqa: E402
from ideation_dashboard.generator import generate_snapshot  # noqa: E402

LANE = "ideation-dashboard-snapshot"
DEFAULT_CHECKOUT = "openxFactory"       # v1 scope: the pinned openxFactory checkout
DEFAULT_REPOSITORY = "openxFactory"     # canonical repository id in the snapshot
DEFAULT_OUT_DIR = "health/ideation-dashboard"
DEFAULT_REGISTER = "project-register.yaml"
STATUS_NAME = "lane-status.json"
INDEX_STATUS_NAME = "index-status.json"


@dataclass
class LaneOutcome:
    """One lane run's outcome. ``ok=False`` is always SKIPPED, never failed —
    the lane has no failure mode that propagates (main() returns 0 either way)."""
    ok: bool
    reason: str | None
    source_revision: str | None
    snapshot_path: Path | None
    status_path: Path | None

    def log_line(self) -> str:
        if self.ok:
            return (f"ideation-dashboard lane: OK {self.snapshot_path} "
                    f"(source_revision={self.source_revision})")
        return f"ideation-dashboard lane: SKIPPED — {self.reason}"


def _head_sha(repo: Path) -> str | None:
    """The pinned checkout's HEAD sha — the deterministic source_revision
    anchor. None on any failure (not a git checkout, git absent)."""
    try:
        proc = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True)
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def _now_iso() -> str:
    """This run's wall-clock stamp (UTC, seconds precision) for the diagnostic
    lane-status. Deliberately NOT part of the snapshot's determinism contract —
    it stamps the status artifact only."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_id() -> str | None:
    """The CI run id (``GITHUB_RUN_ID``) when running under Actions, else None —
    ties a committed status back to the run that produced it."""
    return os.environ.get("GITHUB_RUN_ID") or None


def _detail_lines(result, cap: int = 50) -> list[str]:
    """The pinned validator's own output, line by line (stdout then stderr,
    blank lines dropped, capped) — the per-error diagnosis that would otherwise
    be lost once the candidate is deleted. Only the one-line ``summary()``
    survives in ``reason``; this preserves every ``ERROR [...]`` line."""
    lines: list[str] = []
    for stream in (result.stdout, result.stderr):
        for line in (stream or "").splitlines():
            line = line.rstrip()
            if line:
                lines.append(line)
    return lines[:cap]


def _write_status(boundary: OutputBoundary, out_dir: Path, payload: dict) -> Path | None:
    """Write the lane-status artifact. Its own failure must never take the
    lane down (the log line still reports the outcome)."""
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    try:
        return boundary.write_output(out_dir / STATUS_NAME, text)
    except Exception:  # noqa: BLE001 — status is best-effort reporting
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            path = out_dir / STATUS_NAME
            path.write_text(text, encoding="utf-8")
            return path
        except OSError:
            return None


def run_lane(
    agg_root: Path | str,
    *,
    checkout: str = DEFAULT_CHECKOUT,
    repository: str = DEFAULT_REPOSITORY,
    out_dir: str = DEFAULT_OUT_DIR,
    register: str = DEFAULT_REGISTER,
    source_revision: str | None = None,
    validator: Path | None = None,
    strict: bool = False,
    generate=generate_snapshot,
) -> LaneOutcome:
    """Generate + validate + publish the current snapshot under the aggregation
    checkout. Never raises: every error path returns a SKIPPED outcome with the
    reason recorded in the status artifact. ``generate`` is injectable so tests
    can prove the failure-isolation semantics without breaking the real
    generator."""
    agg_root = Path(agg_root).resolve()
    out_abs = agg_root / out_dir
    snapshot_name = f"{repository}-snapshot.json"
    candidate_name = snapshot_name + ".candidate"
    boundary = OutputBoundary(out_abs, [snapshot_name, candidate_name, STATUS_NAME])
    candidate = out_abs / candidate_name

    # Documents the generator had to exclude (defective Status header); reported
    # on BOTH outcomes. Bound before `_skip` so the closure reads the same list
    # the generator appends to.
    excluded: list[dict[str, str]] = []

    def _status_payload(result: str, reason: str | None, rev: str | None,
                         detail: list[str] | None = None) -> dict:
        """The lane-status record. `kind` and the original fields are
        byte-compatible with prior runs; `detail`/`excluded_documents`/
        `generated_at`/`run_id` are additive (lane-status has no openxFactory
        schema — only snapshot/workbench/possibles-register/project-register/
        gate-action-record are contract-owned)."""
        return {
            "kind": "ideation-dashboard-lane-status",
            "lane": LANE,
            "result": result,
            "reason": reason,
            "repository": repository,
            "source_revision": rev,
            "snapshot": snapshot_name,
            "excluded_documents": list(excluded),
            "detail": list(detail or []),
            "generated_at": _now_iso(),
            "run_id": _run_id(),
        }

    def _skip(reason: str, rev: str | None = None,
              detail: list[str] | None = None) -> LaneOutcome:
        # A rejected/failed render is never published and never left behind.
        try:
            candidate.unlink(missing_ok=True)
        except OSError:
            pass
        status = _write_status(boundary, out_abs,
                               _status_payload("skipped", reason, rev, detail))
        return LaneOutcome(False, reason, rev, None, status)

    rev: str | None = None
    try:
        checkout_root = (agg_root / checkout).resolve()
        if not checkout_root.is_dir():
            return _skip(f"pinned checkout not found: {checkout}")

        rev = source_revision or _head_sha(checkout_root)
        if not rev:
            return _skip(f"cannot resolve HEAD of the pinned checkout {checkout!r} "
                         "(source_revision is the deterministic anchor)")

        register_path = agg_root / register
        register_source = register_path if register_path.is_file() else None

        snap = generate(checkout_root, repository, source_revision=rev,
                        project_register_source=register_source,
                        excluded_documents=excluded)
        snapshot_mod.write_snapshot(snap, candidate, boundary)

        pinned = validator or snapshot_mod.find_validator(agg_root)
        if pinned is None:
            return _skip("pinned openxFactory validator not found "
                         f"({snapshot_mod.VALIDATOR_RELPATH} under {agg_root})", rev)
        result = snapshot_mod.validate_snapshot(candidate, validator=pinned,
                                                strict=strict)
        if not result.available:
            # The lane still SKIPS, and that is the right call unchanged: this
            # publishes to a location others READ, so an unchecked snapshot must
            # not land there — exactly the judgement the `pinned is None` skip
            # above already makes. Only the DIAGNOSIS changes. Saying "snapshot
            # rejected" when the runner simply lacks the validator's libraries
            # sends whoever reads lane-status.json hunting a corpus defect that
            # does not exist, and the fix is on the HOST.
            return _skip("the pinned validator could NOT RUN, so this snapshot "
                         f"was never checked: {result.unavailable_reason} — "
                         f"remedy on the lane host: {snapshot_mod.DEPENDENCY_REMEDY}",
                         rev, detail=_detail_lines(result))
        if not result.ok:
            # Retain the validator's per-error diagnosis, not just the one-liner.
            return _skip("snapshot rejected by the pinned validator: "
                         f"{result.summary()}", rev, detail=_detail_lines(result))

        final = boundary.permit_output(out_abs / snapshot_name)
        candidate.replace(final)
        status = _write_status(boundary, out_abs,
                               _status_payload("ok", None, rev))
        return LaneOutcome(True, None, rev, final, status)
    except Exception as exc:  # noqa: BLE001 — task 4.1: any error is a SKIP
        return _skip(f"{type(exc).__name__}: {exc}", rev)


# --------------------------------------------------------------------------
# Per-repository iteration + the snapshot INDEX (add-dashboard-repo-selector
# task 3.1). The generator already took `--repository` + `--project-register`
# and needed ZERO changes to snapshot Medx/Adx/Ledgerx in the 2026-07-25 drive:
# what was missing is this LOOP and the thin locator it publishes.
# --------------------------------------------------------------------------

@dataclass
class MultiLaneOutcome:
    """One multi-repository publication run: each repository's own outcome plus
    the index that locates the snapshots that succeeded."""
    outcomes: list[LaneOutcome]
    index_path: Path | None
    status_path: Path | None

    @property
    def published(self) -> list[LaneOutcome]:
        return [o for o in self.outcomes if o.ok]

    def log_line(self) -> str:
        return (f"ideation-dashboard lane: {len(self.published)}/{len(self.outcomes)} "
                f"repository snapshot(s) published"
                + (f", index {self.index_path}" if self.index_path else ", NO index"))


def submodule_paths(agg_root: Path) -> dict[str, str]:
    """`.gitmodules` path per submodule BASENAME — the aggregation workspace's own
    statement of where each repository lives. The project register names repository
    IDS (which match those basenames); nothing here guesses a layout."""
    out: dict[str, str] = {}
    gitmodules = Path(agg_root) / ".gitmodules"
    try:
        text = gitmodules.read_text(encoding="utf-8")
    except OSError:
        return out
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("path"):
            continue
        _, _, value = stripped.partition("=")
        rel = value.strip()
        if rel:
            out.setdefault(Path(rel).name, rel)
    return out


def resolve_checkout(agg_root: Path, repository: str,
                     submodules: dict[str, str] | None = None) -> str | None:
    """The checkout path (relative to the aggregation root) for a repository id:
    the repository id used AS a path, then the `.gitmodules` basename map. None
    when nothing resolves — that repository is SKIPPED with a reason rather than
    guessed at."""
    subs = submodules if submodules is not None else submodule_paths(agg_root)
    direct = Path(agg_root) / repository
    if direct.is_dir():
        return repository
    rel = subs.get(Path(repository).name)
    if rel and (Path(agg_root) / rel).is_dir():
        return rel
    return None


def registered_repositories(agg_root: Path, register: str = DEFAULT_REGISTER) -> list[str]:
    """Every repository the project register declares, in authored order — THE
    roster (design D9). No second repository list exists anywhere: adding a
    repository to the dashboard is a register edit plus a lane run."""
    path = Path(agg_root) / register
    if not path.is_file():
        return []
    adapter = register_mod.ProjectRegisterAdapter(path)
    seen: list[str] = []
    for project in adapter.projects():
        for repo in project.get("repositories") or []:
            if isinstance(repo, str) and repo not in seen:
                seen.append(repo)
    return seen


def run_multi_lane(
    agg_root: Path | str,
    *,
    repositories: list[str] | None = None,
    out_dir: str = DEFAULT_OUT_DIR,
    register: str = DEFAULT_REGISTER,
    validator: Path | None = None,
    strict: bool = False,
    generate=generate_snapshot,
    index_name: str = registry_mod.DEFAULT_INDEX_NAME,
    aggregate_id: str | None = None,
    aggregate_members: list[str] | None = None,
    aggregate_display_name: str | None = None,
) -> MultiLaneOutcome:
    """Publish one snapshot per registered repository PLUS the index that locates
    them. Same failure semantics as the single-repository lane: a repository that
    cannot be scanned, generated, or validated is SKIPPED (its previously
    published snapshot stays in place and it simply does not enter this run's
    index), and the run never fails the nightly.

    Only `main` snapshots are ever published — the index write goes through
    `snapshot_registry.build_index(published=True)`, which refuses any other ref
    (task 2.3)."""
    agg_root = Path(agg_root).resolve()
    out_abs = agg_root / out_dir
    repos = repositories if repositories is not None else registered_repositories(agg_root, register)
    subs = submodule_paths(agg_root)

    outcomes: list[LaneOutcome] = []
    entries: list[registry_mod.SnapshotEntry] = []
    skipped: list[dict[str, str]] = []
    for repository in repos:
        checkout = resolve_checkout(agg_root, repository, subs)
        if checkout is None:
            outcomes.append(LaneOutcome(
                False, f"no checkout found for repository {repository!r}", None, None, None))
            skipped.append({"repository": repository, "reason": "checkout not found"})
            continue
        outcome = run_lane(agg_root, checkout=checkout, repository=repository,
                           out_dir=out_dir, register=register, validator=validator,
                           strict=strict, generate=generate)
        outcomes.append(outcome)
        if not outcome.ok or outcome.snapshot_path is None:
            skipped.append({"repository": repository, "reason": outcome.reason or "skipped"})
            continue
        entry = registry_mod.entry_from_snapshot_file(
            outcome.snapshot_path, repository=repository,
            ref=registry_mod.DEFAULT_REF, origin=registry_mod.ORIGIN_LOCAL)
        entry.location = Path(outcome.snapshot_path).name
        entries.append(entry)

    aggregates = []
    aggregate_entries = entries
    aggregate_is_complete = True
    if aggregate_members is not None:
        requested = list(dict.fromkeys(aggregate_members))
        by_repository = {entry.repository: entry for entry in entries}
        aggregate_entries = [by_repository[repository]
                             for repository in requested
                             if repository in by_repository]
        # A named program aggregate is fail-closed: publishing a partial member
        # set would make a missing proposal look like a complete program. The
        # per-repository index and skip status still publish normally.
        aggregate_is_complete = (len(aggregate_entries) == len(requested)
                                 and bool(requested))
    if aggregate_id and aggregate_entries and aggregate_is_complete:
        # The composed view is declared as member (repository, ref) pairs so a
        # composing renderer reads the index and the snapshots it names — never
        # a repository. Omitting aggregate_members preserves the original
        # all-published-repositories behavior.
        aggregates.append(registry_mod.Aggregate(
            id=aggregate_id,
            members=[entry.key for entry in aggregate_entries],
            display_name=(aggregate_display_name
                          or (f"{aggregate_id} (selected repositories)"
                              if aggregate_members is not None
                              else f"{aggregate_id} (all registered repositories)"))))

    index_path: Path | None = None
    reason: str | None = None
    if entries:
        boundary = OutputBoundary(out_abs, [index_name, INDEX_STATUS_NAME])
        try:
            document = registry_mod.build_index(entries, published=True, aggregates=aggregates)
            index_path = boundary.write_output(
                out_abs / index_name,
                json.dumps(document, indent=2, sort_keys=True) + "\n")
        # An index failure is a SKIP, never a nightly failure (the prose lives
        # here because a noqa directive may carry nothing but its codes — trailing
        # text makes the suppression itself malformed, python:S7632).
        except Exception as exc:  # noqa: BLE001
            reason = f"{type(exc).__name__}: {exc}"
    else:
        reason = "no repository snapshot was published"

    status_boundary = OutputBoundary(out_abs, [INDEX_STATUS_NAME])
    status = _write_index_status(status_boundary, out_abs, {
        "kind": "ideation-dashboard-index-status",
        "lane": LANE,
        "result": "ok" if index_path else "skipped",
        "reason": reason,
        "index": index_name if index_path else None,
        "published": [{"repository": e.repository, "ref": e.ref,
                       "source_revision": e.source_revision} for e in entries],
        "skipped": skipped,
        "generated_at": _now_iso(),
        "run_id": _run_id(),
    })
    return MultiLaneOutcome(outcomes, index_path, status)


def _write_index_status(boundary: OutputBoundary, out_dir: Path, payload: dict) -> Path | None:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    try:
        return boundary.write_output(out_dir / INDEX_STATUS_NAME, text)
    except Exception:  # noqa: BLE001 — status is best-effort reporting
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            path = out_dir / INDEX_STATUS_NAME
            path.write_text(text, encoding="utf-8")
            return path
        except OSError:
            return None


def main(argv: list[str] | None = None) -> None:
    """CLI entry. Void by contract: the lane NEVER fails the nightly, so there
    is no exit-status variation to return — every path (including a total
    failure, reported as SKIPPED) falls through and the process exits 0."""
    ap = argparse.ArgumentParser(
        prog="ideation-dashboard-nightly", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo-root", required=True,
                    help="the aggregation checkout root")
    ap.add_argument("--checkout", default=DEFAULT_CHECKOUT,
                    help=f"pinned checkout to scan, relative to the aggregation "
                         f"root (default: {DEFAULT_CHECKOUT})")
    ap.add_argument("--repository", default=DEFAULT_REPOSITORY,
                    help=f"canonical repository id for the snapshot "
                         f"(default: {DEFAULT_REPOSITORY})")
    ap.add_argument("--out-dir", default=DEFAULT_OUT_DIR,
                    help=f"lane output directory, relative to the aggregation "
                         f"root (default: {DEFAULT_OUT_DIR})")
    ap.add_argument("--register", default=DEFAULT_REGISTER,
                    help=f"project-register instance, relative to the "
                         f"aggregation root (default: {DEFAULT_REGISTER}; "
                         "missing is legal — the repository renders ungrouped)")
    ap.add_argument("--source-revision", default=None,
                    help="pin the source_revision anchor "
                         "(default: the pinned checkout's HEAD sha)")
    ap.add_argument("--validator", default=None,
                    help="pinned validator path (default: discovered as "
                         f"{snapshot_mod.VALIDATOR_RELPATH} under the "
                         "aggregation root)")
    ap.add_argument("--strict", action="store_true",
                    help="treat validator warnings as rejection")
    ap.add_argument("--repositories", default=None,
                    help="publish one snapshot per repository PLUS the snapshot "
                         "index (add-dashboard-repo-selector task 3.1): a comma-"
                         "separated list of repository ids, or `registered` for "
                         "every repository the project register declares. Omit "
                         "for the single-repository behaviour")
    ap.add_argument("--index", default=registry_mod.DEFAULT_INDEX_NAME,
                    help=f"index filename written beside the snapshots "
                         f"(default: {registry_mod.DEFAULT_INDEX_NAME})")
    ap.add_argument("--aggregate", default=None, metavar="ID",
                    help="also declare a composed cross-repository view with this "
                         "id (e.g. xFactory) whose members are the published "
                         "(repository, ref) pairs; omitted by default")
    ap.add_argument("--aggregate-members", default=None, metavar="REPOSITORIES",
                    help="optional comma-separated repository subset for "
                         "--aggregate; the aggregate is omitted unless every "
                         "named member publishes successfully")
    ap.add_argument("--aggregate-display-name", default=None, metavar="LABEL",
                    help="optional human-readable label for --aggregate")
    args = ap.parse_args(argv)

    if args.repositories:
        _run_multi(args)
        return
    try:
        outcome = run_lane(
            Path(args.repo_root), checkout=args.checkout,
            repository=args.repository, out_dir=args.out_dir,
            register=args.register, source_revision=args.source_revision,
            validator=Path(args.validator) if args.validator else None,
            strict=args.strict)
    except Exception as exc:  # noqa: BLE001 — belt-and-braces: never fail the nightly
        print(f"ideation-dashboard lane: SKIPPED — unhandled "
              f"{type(exc).__name__}: {exc}")
        return
    print(outcome.log_line())
    if outcome.status_path is not None:
        print(f"  status: {outcome.status_path}")


def _run_multi(args) -> None:
    """The per-repository publication run. Same void contract as `main`: every
    failure is a SKIP that never propagates."""
    repos = None
    if args.repositories.strip() != "registered":
        repos = [r.strip() for r in args.repositories.split(",") if r.strip()]
    aggregate_members = None
    if args.aggregate_members is not None:
        aggregate_members = [r.strip() for r in args.aggregate_members.split(",")
                             if r.strip()]
    try:
        outcome = run_multi_lane(
            Path(args.repo_root), repositories=repos, out_dir=args.out_dir,
            register=args.register,
            validator=Path(args.validator) if args.validator else None,
            strict=args.strict, index_name=args.index, aggregate_id=args.aggregate,
            aggregate_members=aggregate_members,
            aggregate_display_name=args.aggregate_display_name)
    except Exception as exc:  # noqa: BLE001 — never fail the nightly
        print(f"ideation-dashboard lane: SKIPPED — unhandled "
              f"{type(exc).__name__}: {exc}")
        return
    print(outcome.log_line())
    for one in outcome.outcomes:
        print(f"  {one.log_line()}")
    if outcome.status_path is not None:
        print(f"  index status: {outcome.status_path}")


if __name__ == "__main__":
    main()
