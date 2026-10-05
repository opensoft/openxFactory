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
image change. A register id resolves to a checkout some `.gitmodules` in the
workspace DECLARES, at any depth (`locate_checkout`), which is how the nested
product legs (`openDox-spec`, `openXdox-code`, ...) are reached; and a declared
directory that was never initialised is skipped as `submodule not initialised`,
never scanned (openxFactory #1208).

The lane itself STAGES AND COMMITS NOTHING: the nightly host's existing
"Commit report" step (``git add health/``) sweeps these files into the same
commit that lands the dated reports and inventories — exactly the reports'
emission pattern.

FAILURE SEMANTICS (task 4.1): any error — a missing checkout, a checkout that
is an uninitialised submodule directory (whose HEAD git would answer from the
enclosing repository), an unresolvable pin, a generator crash, a snapshot the
pinned validator rejects — makes the
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
import re
import subprocess
import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import TypedDict

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# § 5.2 SHED REACH (RULED (a) / RULED Q7, `#656`): the modules this file reads
# from `opendox.*` / `openxdox.*` below left openxFactory at the carve and are
# read from the two PINNED legs through the ONE resolver. See
# `scripts/carved_reach.py`.
from carved_reach import install as _install_carved_reach  # noqa: E402

_install_carved_reach()

from openxdox import register as register_mod  # noqa: E402
from openxdox import snapshot as snapshot_mod  # noqa: E402
from openxdox import snapshot_registry as registry_mod  # noqa: E402
from openxdox.generator import generate_snapshot  # noqa: E402
from output_boundary import OutputBoundary  # noqa: E402

LANE = "ideation-dashboard-snapshot"
DEFAULT_CHECKOUT = "openxFactory"       # v1 scope: the pinned openxFactory checkout
DEFAULT_REPOSITORY = "openxFactory"     # canonical repository id in the snapshot
DEFAULT_OUT_DIR = "health/ideation-dashboard"
DEFAULT_REGISTER = "project-register.yaml"
STATUS_NAME = "lane-status.json"
INDEX_STATUS_NAME = "index-status.json"
# `index-status.json` skip reasons for a repository that never reached
# `run_lane` (a `run_lane` skip records its own full reason instead).
SKIP_CHECKOUT_NOT_FOUND = "checkout not found"
SKIP_SUBMODULE_NOT_INITIALISED = "submodule not initialised"


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
    anchor. None on any failure (not a git checkout, git absent).

    It answers for WHATEVER work tree encloses `repo`, which is why
    `run_lane` asks `_borrowed_toplevel` first: git walks up out of a
    directory that has no checkout of its own."""
    try:
        proc = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                              capture_output=True, text=True)
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def _git_toplevel(path: Path) -> Path | None:
    """The top level of the work tree git finds for `path`, or None when git
    finds none (or is absent)."""
    try:
        proc = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True)
    except OSError:
        return None
    top = proc.stdout.strip() if proc.returncode == 0 else ""
    return Path(top).resolve() if top else None


def _borrowed_toplevel(checkout: Path) -> Path | None:
    """The ENCLOSING work tree whose HEAD a directory would borrow, when the
    directory has no git checkout of its own (openxFactory #1208).

    A declared submodule that was never initialised is an EMPTY directory
    inside the aggregation's own work tree. `git -C <it> rev-parse HEAD` walks
    up and answers the AGGREGATION's head, so a lane that trusted it would
    publish an empty snapshot under a revision that is not the repository's.
    A checkout is POPULATED when it has a `.git` entry of its own (a work
    tree's `.git` directory, or the gitfile a submodule checkout carries) or
    git resolves its top level to the directory itself; it then answers None.
    A directory in no work tree answers None too, because nothing is
    borrowed: if it is in no repository at all, its HEAD fails to resolve,
    which is the lane's existing skip; if it is in a repository that has no
    work tree there (a bare repository, or a path inside a `.git` directory),
    `_without_work_tree` refuses it, because its HEAD DOES resolve."""
    if (checkout / ".git").exists():
        return None
    top = _git_toplevel(checkout)
    if top is None or top == checkout.resolve():
        return None
    return top


def _without_work_tree(directory: Path) -> bool:
    """True when `directory` sits in a git REPOSITORY that has no work tree
    there: a bare repository, or a path inside a `.git` directory. git
    resolves `HEAD` in such a place, yet there are no files to snapshot, so
    it is never a populated checkout. A checkout is populated only when it
    has a `.git` entry of its own, or git resolves its top level to the
    directory itself, and a bare repository has neither (Copilot review,
    PR #1209)."""
    if (directory / ".git").exists():
        return False
    try:
        proc = subprocess.run(
            ["git", "-C", str(directory), "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True)
    except OSError:
        return False
    return proc.returncode == 0 and proc.stdout.strip() == "false"


def _enclosing_label(top: Path, agg_root: Path) -> str:
    """Where a borrowed HEAD would come from, said without an absolute path
    (lane-status.json is committed by the nightly)."""
    root = agg_root.resolve()
    if top == root:
        return "the aggregation root"
    try:
        return f"the enclosing repository {top.relative_to(root).as_posix()!r}"
    except ValueError:
        return "an enclosing repository outside the aggregation root"


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


def _pinned_validator() -> Path | None:
    """The default pinned validator: the openxdox product's OWN, made runnable.

    ASKED FROM THE MODULE, NEVER FROM THE AGGREGATION ROOT. This lane used to
    ask `snapshot.find_validator(agg_root)`, which walked up for
    `openxFactory/scripts/validate-ideation-dashboard-contracts.py`. The § 5.2
    shed (`cc4ae9d3`) deleted that file from this repository, so the walk
    already found nothing. From openXdox-code `e28930bf` on
    (split-opendox-two-layer-product § 8.9 residue (iii)), the locator also
    CONFINES: any start outside the product's own tree answers None. Called with
    no start, it answers the validator that ships beside the generator which
    rendered the snapshot, at the leg openxFactory pins.

    FOUND IS NOT RUNNABLE. Run in place from the code leg, the script reads no
    `contracts/` of its own and exits 2 before reading the snapshot, which
    `validate_snapshot` reports as could-not-run. So it is composed with the
    schemas the shed split from it by
    `doxbench_contracts._composed_validator`, as
    `delegated_semantic_validation` and the suite's `_shed_validator` already
    do. The composer returns any other path unchanged.
    """
    found = snapshot_mod.find_validator()
    if found is None:
        return None
    from ideation_dashboard import doxbench_contracts
    return doxbench_contracts._composed_validator(found)


def _pinned_validator_missing() -> str:
    """WHERE `_pinned_validator()` looked, for when it answers None.

    Spelled ONCE, for the two callers that must say it: this lane's skip, and
    the refresh lane's seal refusal, which resolves its validator through
    `_pinned_validator()` too (openxFactory #1158). One sentence in one place,
    so the two lanes cannot come to disagree about where the default is
    looked for.
    """
    root = snapshot_mod.product_root()
    return (f"{root / snapshot_mod.VALIDATOR_RELPATH} does not exist"
            if root is not None else
            "openxdox is not running from a source checkout, so it ships no "
            "validator")


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

        # The anchor is DERIVED from the checkout only when the caller pinned
        # none, and a derived anchor must be the checkout's OWN: an
        # uninitialised submodule directory would lend the enclosing
        # repository's HEAD to an empty snapshot (#1208). An explicit
        # `source_revision` is the caller's statement and borrows nothing.
        if not source_revision:
            borrowed = _borrowed_toplevel(checkout_root)
            if borrowed is not None:
                return _skip(
                    f"{SKIP_SUBMODULE_NOT_INITIALISED}: the pinned checkout "
                    f"{checkout!r} has no git checkout of its own, so its HEAD "
                    f"would be {_enclosing_label(borrowed, agg_root)}'s, not this "
                    "repository's revision")
            if _without_work_tree(checkout_root):
                return _skip(
                    f"{SKIP_SUBMODULE_NOT_INITIALISED}: the pinned checkout "
                    f"{checkout!r} is a git repository with no work tree (a bare "
                    "repository or a git directory), so it has no files to "
                    "snapshot")

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

        pinned = validator or _pinned_validator()
        if pinned is None:
            return _skip("pinned openxdox validator not found "
                         f"({_pinned_validator_missing()})", rev)
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


# A submodule key as git's own config parser prints it: the section and the
# variable name lowercased, the submodule NAME (which may contain dots) as
# declared.
_SUBMODULE_KEY = re.compile(r"^submodule\.(.+)\.(path|url)$", re.DOTALL)


def _gitmodules_entries(gitmodules: Path) -> list[tuple[str, str | None]]:
    """`(path, url)` per submodule one `.gitmodules` declares, in declared
    order, read by GIT'S OWN config parser (`git config --file <it>
    --no-includes --null --get-regexp`), never by a hand parser.

    Three review rounds on PR #1209 each found a way a hand parser drifted
    from git-config's grammar: a non-submodule section declaring a checkout,
    an unanchored header, and inline comments and quoting kept inside values,
    which made an initialised leg declared as `path = spec # product leg`
    resolve as missing. git's own reading settles every such question at
    once: section headers, comments, quoting, escapes and case are exactly
    git's, and `include.*` directives are not followed. A section git reads as
    a submodule is read the same way here, and every path it yields still
    passes the lane's containment and populated-checkout checks.

    A file that is missing, that git refuses (a bad config line, rc 128), or
    that declares no submodule (rc 1) declares nothing. That keeps one
    malformed `.gitmodules` in a pinned repository from aborting the whole
    run before `index-status.json` is written. Bytes that are not UTF-8 are
    carried through `surrogateescape`, so a path still names the directory
    git names."""
    if not gitmodules.is_file():
        return []
    try:
        proc = subprocess.run(
            ["git", "config", "--file", str(gitmodules), "--no-includes",
             "--null", "--get-regexp", r"^submodule\..*\.(path|url)$"],
            capture_output=True)
    except OSError:
        return []
    if proc.returncode != 0:
        return []
    order: list[str] = []
    found: dict[str, dict[str, str]] = {}
    for record in proc.stdout.split(b"\0"):
        key, sep, value = record.partition(b"\n")
        if not sep:
            continue  # a valueless (boolean) key, or the trailing empty record
        match = _SUBMODULE_KEY.match(key.decode("utf-8", "surrogateescape"))
        if match is None:
            continue
        name, var = match.groups()
        if name not in found:
            found[name] = {}
            order.append(name)
        # The last value wins, as git's own single-value read answers.
        found[name][var] = value.decode("utf-8", "surrogateescape")
    return [(found[n]["path"], found[n].get("url") or None)
            for n in order if found[n].get("path")]


def _repository_name(url: str | None) -> str | None:
    """The repository NAME a submodule URL declares: its last path segment,
    without `.git` (`git@github.com:opensoft/openDox-spec.git` ->
    `openDox-spec`). This is the name the project register uses for a leg
    whose checkout path is only `spec` or `code`."""
    if not url:
        return None
    tail = url.strip().rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
    if tail.endswith(".git"):
        tail = tail[:-4]
    return tail or None


def _declared_rel(base: str, path: str) -> str | None:
    """`path` declared by the `.gitmodules` at `base`, as a path relative to
    the aggregation root. None for a declaration that is absolute or climbs out
    of the repository declaring it: that is not a checkout this lane scans.

    Absolute means absolute on EITHER platform: a backslash, or a Windows
    drive or UNC anchor (`C:\\x`, `C:/x`, `\\\\srv\\share`), is refused too, because
    `PurePosixPath` does not see those as absolute and `root / rel` on Windows
    would then leave the aggregation root (Copilot review, PR #1209). git
    writes `.gitmodules` paths with forward slashes only, so nothing it
    declares is lost."""
    raw = path.strip()
    declared = PurePosixPath(raw)
    if (not raw or declared.is_absolute() or ".." in declared.parts
            or "\\" in raw or PureWindowsPath(raw).drive):
        return None
    joined = PurePosixPath(base) / declared if base else declared
    rel = joined.as_posix()
    return None if rel in ("", ".") else rel


def submodule_paths(agg_root: Path) -> dict[str, str]:
    """`.gitmodules` path per submodule BASENAME — the aggregation workspace's own
    statement of where each repository lives. The project register names repository
    IDS (which match those basenames); nothing here guesses a layout."""
    out: dict[str, str] = {}
    for path, _url in _gitmodules_entries(Path(agg_root) / ".gitmodules"):
        rel = path.strip()
        if rel:
            out.setdefault(Path(rel).name, rel)
    return out


def declared_checkouts(agg_root: Path) -> dict[str, list[str]]:
    """Every checkout the workspace DECLARES, at any depth, by the names a
    register id may use for it (openxFactory #1208).

    The aggregation root's `.gitmodules` is read first, then the `.gitmodules`
    of every POPULATED checkout it declares, and so on down (breadth first, so
    a shallower declaration is always the earlier candidate). Each declared
    checkout answers to its path BASENAME, as `submodule_paths` has always
    keyed it, AND to the repository NAME its URL declares. The second key is
    what reaches a nested product leg: openxFactory declares `openDox`, and
    openDox declares `spec` at `https://github.com/opensoft/openDox-spec.git`,
    so the register id `openDox-spec` is `openxFactory/openDox/spec`. Nothing
    here guesses a layout: every candidate is a path some `.gitmodules`
    declares, relative to the aggregation root, in the order found. A checkout
    that was never initialised is an empty directory with no `.gitmodules` to
    read, so the walk stops there on its own."""
    root = Path(agg_root)
    out: dict[str, list[str]] = {}
    queue: deque[str] = deque([""])  # "" is the aggregation root itself
    seen: set[Path] = set()
    while queue:
        base = queue.popleft()
        base_dir = root / base if base else root
        try:
            real = base_dir.resolve()
        except (OSError, RuntimeError):  # RuntimeError: a symlink loop
            continue
        if real in seen:
            continue
        seen.add(real)
        for path, url in _gitmodules_entries(base_dir / ".gitmodules"):
            rel = _declared_rel(base, path)
            if rel is None:
                continue
            for name in dict.fromkeys(n for n in (PurePosixPath(rel).name,
                                                  _repository_name(url)) if n):
                bucket = out.setdefault(name, [])
                if rel not in bucket:
                    bucket.append(rel)
            child = root / rel
            if ((child / ".gitmodules").is_file()
                    and _borrowed_toplevel(child) is None):
                queue.append(rel)
    return out


class _SkippedRepositoryBase(TypedDict):
    repository: str
    reason: str


class SkippedRepository(_SkippedRepositoryBase, total=False):
    """One `index-status.json` `skipped` entry. `repository` and `reason` are
    always present; `paths` (the declared directories that were found
    uninitialised) only when `reason` is `submodule not initialised`
    (Copilot review, PR #1209)."""
    paths: list[str]


@dataclass
class CheckoutLocation:
    """Where a repository id resolved. `path` is the populated checkout,
    relative to the aggregation root, or None. `uninitialised` lists the
    declared directories that exist but have no git checkout of their own, in
    the order they were tried — the evidence for a `submodule not initialised`
    skip."""
    path: str | None
    uninitialised: list[str]


def locate_checkout(agg_root: Path, repository: str,
                    submodules: dict[str, str] | None = None,
                    declared: dict[str, list[str]] | None = None) -> CheckoutLocation:
    """Resolve a repository id to its checkout, trying in order: the id used AS
    a path, the aggregation root's `.gitmodules` basename map, then every
    checkout the workspace declares at any depth (`declared_checkouts`). The
    FIRST candidate that is a directory and not an uninitialised submodule is
    the checkout. A candidate with no git checkout of its own is never used,
    because its HEAD is the enclosing repository's (#1208); it is recorded
    instead, so the skip can say which declared directories were empty.

    EVERY candidate passes the same containment `declared_checkouts` applies:
    an id or a root declaration that is absolute or climbs out with `..` is
    never tried, so no source can point the generator outside the
    aggregation root (Copilot review, PR #1209)."""
    root = Path(agg_root)
    name = Path(repository).name
    subs = submodules if submodules is not None else submodule_paths(root)
    decl = declared if declared is not None else declared_checkouts(root)
    candidates = [c for c in (_declared_rel("", repository),
                              _declared_rel("", subs[name]) if subs.get(name) else None)
                  if c is not None]
    candidates.extend(decl.get(name, []))
    uninitialised: list[str] = []
    for rel in dict.fromkeys(candidates):
        directory = root / rel
        if not directory.is_dir():
            continue
        if (_borrowed_toplevel(directory) is not None
                or _without_work_tree(directory)):
            uninitialised.append(rel)
            continue
        return CheckoutLocation(rel, uninitialised)
    return CheckoutLocation(None, uninitialised)


def resolve_checkout(agg_root: Path, repository: str,
                     submodules: dict[str, str] | None = None,
                     declared: dict[str, list[str]] | None = None) -> str | None:
    """The checkout path (relative to the aggregation root) for a repository
    id, as `locate_checkout` resolves it. None when nothing resolves — that
    repository is SKIPPED with a reason rather than guessed at."""
    return locate_checkout(agg_root, repository, submodules, declared).path


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
    declared = declared_checkouts(agg_root)

    outcomes: list[LaneOutcome] = []
    entries: list[registry_mod.SnapshotEntry] = []
    skipped: list[SkippedRepository] = []
    for repository in repos:
        located = locate_checkout(agg_root, repository, subs, declared)
        checkout = located.path
        if checkout is None and located.uninitialised:
            # Declared, but never checked out: no revision of its own exists
            # to snapshot, so nothing is published for it (#1208).
            outcomes.append(LaneOutcome(
                False, f"{SKIP_SUBMODULE_NOT_INITIALISED} for repository {repository!r}: "
                       f"{', '.join(located.uninitialised)} declared but not checked out",
                None, None, None))
            skipped.append({"repository": repository,
                            "reason": SKIP_SUBMODULE_NOT_INITIALISED,
                            "paths": list(located.uninitialised)})
            continue
        if checkout is None:
            outcomes.append(LaneOutcome(
                False, f"no checkout found for repository {repository!r}", None, None, None))
            skipped.append({"repository": repository, "reason": SKIP_CHECKOUT_NOT_FOUND})
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


def _pre_parse_output_location(argv: list[str] | None) -> argparse.Namespace:
    """A `--help`-agnostic peek at just the flags that decide WHERE a
    registration-failure status artifact belongs (`--repo-root`, `--out-dir`,
    `--repository`, `--repositories`), read BEFORE the real parser built
    inside `main()` runs. `add_help=False` and `parse_known_args` so this
    never recognizes `--help` and never raises on a flag it does not itself
    define — reintroducing a parser that could raise `SystemExit` ahead of
    registration is exactly the hazard the real parser's placement (after
    registration, in `main()`) exists to avoid
    (`test_an_engine_lane_registers_at_its_own_process_entry`). Never raises:
    a malformed argv falls back to the defaults (with no `--repo-root` to
    anchor a write, `_write_registration_failure_status` below is then a
    no-op) rather than letting a SKIP path raise."""
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--repo-root", default=None)
    pre.add_argument("--out-dir", default=DEFAULT_OUT_DIR)
    pre.add_argument("--repository", default=DEFAULT_REPOSITORY)
    pre.add_argument("--repositories", default=None)
    try:
        peeked, _ = pre.parse_known_args(argv)
    except SystemExit:
        return argparse.Namespace(repo_root=None, out_dir=DEFAULT_OUT_DIR,
                                  repository=DEFAULT_REPOSITORY, repositories=None)
    return peeked


def _write_registration_failure_status(args: argparse.Namespace, reason: str) -> None:
    """Record a process-start registration failure (`main()`, below) through
    the SAME status-writing path `run_lane()`/`run_multi_lane()` use for
    every other SKIP (Copilot review, PR #984, second round) — never only a
    print. `main()` runs this registration before either of those ever gets
    a chance to write anything, so nothing else will record the reason.
    Writes whichever artifact the requested mode would have produced:
    `index-status.json` for `--repositories`, `lane-status.json` otherwise —
    there is no per-repository outcome to report, since no repository was
    ever reached. Best-effort like the writers it calls: a failure here
    must not turn this SKIP into a raised exception. `args` is ordinarily
    `_pre_parse_output_location`'s peek (registration runs before the real
    parser — see `main()`), so `repo_root` may legitimately be `None`."""
    if args.repo_root is None:
        return
    agg_root = Path(args.repo_root).resolve()
    out_abs = agg_root / args.out_dir
    common = {"generated_at": _now_iso(), "run_id": _run_id()}
    if args.repositories:
        boundary = OutputBoundary(out_abs, [INDEX_STATUS_NAME])
        _write_index_status(boundary, out_abs, {
            "kind": "ideation-dashboard-index-status",
            "lane": LANE,
            "result": "skipped",
            "reason": reason,
            "index": None,
            "published": [],
            "skipped": [],
            **common,
        })
    else:
        boundary = OutputBoundary(out_abs, [STATUS_NAME])
        _write_status(boundary, out_abs, {
            "kind": "ideation-dashboard-lane-status",
            "lane": LANE,
            "result": "skipped",
            "reason": reason,
            "repository": args.repository,
            "source_revision": None,
            "snapshot": f"{args.repository}-snapshot.json",
            "excluded_documents": [],
            "detail": [],
            **common,
        })


def main(argv: list[str] | None = None) -> None:
    """CLI entry. Void by contract: the lane NEVER fails the nightly, so there
    is no exit-status variation to return — every path (including a total
    failure, reported as SKIPPED) falls through and the process exits 0."""
    # THE ONE PROCESS-START REGISTRATION (§ 4.3/§ 4.4, RULED ASK-2 option (2)
    # and RULING C2). `openxdox.generator.generate_snapshot()` — imported
    # above and called at :191 and :379 — resolves `domain_profile.current()`
    # while deriving
    # cluster lineage (`openxdox/generator.py`:339, :361).
    # A process that reaches the engine with nothing registered is REFUSED —
    # `openxdox.domain_profile.DomainProfileNotRegistered` — and this lane
    # reports every error as SKIPPED and exits 0 by contract, so the
    # refusal would be published as a green-looking skip rather than surfaced
    # (Copilot review, PR #984).
    #
    # HERE, IN `main()`, AND NOT AT MODULE SCOPE: a column that registered
    # while being imported could re-enter its own half-executed module, the
    # hazard `scripts/opendox_host.py` documents for
    # `ideation_dashboard/serve_openxfactory_lanes.py`. Called from the process
    # entry instead, which is what both production paths go through
    # (`scripts/ideation-dashboard-nightly.py` and
    # `python3 -m ideation_dashboard.nightly_lane`, the form
    # `scripts/reserve-dashboard.sh`:69 runs). Idempotent, so a caller that
    # already registered is not punished.
    #
    # BEFORE THE REAL PARSER BELOW, DELIBERATELY
    # (`test_an_engine_lane_registers_at_its_own_process_entry`): `--help` is
    # the cheapest argv that reaches `main()`, and it must still leave the
    # registry populated, which only holds if this runs before a parser that
    # defines `--help` gets a chance to raise `SystemExit(0)`. A registration
    # failure still has to honour this lane's FAILURE SEMANTICS (module
    # docstring) — the reason recorded in a status artifact, not only
    # printed (Copilot review, PR #984, second round) — so the except: below
    # reaches for `--repo-root`/`--out-dir`/`--repositories` through
    # `_pre_parse_output_location`'s OWN `add_help=False` parser instead of
    # the real one: it never recognizes `--help`, so it cannot reintroduce
    # the SystemExit-before-registration hazard this ordering exists to avoid.
    from opendox_host import register_openxfactory
    try:
        register_openxfactory()
    except Exception as exc:  # noqa: BLE001 — same SKIPPED contract as run_lane()
        # A missing leg, a malformed profile, or a registration conflict must
        # not escape `main()` uncaught (Copilot review, PR #984): this call
        # runs before `run_lane()`/`run_multi_lane()` ever get a chance to
        # write their own status artifact, and this function's own contract
        # (docstring above) is that EVERY error is a SKIP at exit 0, never a
        # nonzero exit — reported on stdout AND in the status artifact, same
        # as any other SKIP this lane can produce. There is no
        # `LaneOutcome`/`MultiLaneOutcome` to build around it, so
        # `_write_registration_failure_status` writes the artifact directly.
        reason = f"{type(exc).__name__}: {exc}"
        print(f"ideation-dashboard lane: SKIPPED — unhandled {reason}")
        _write_registration_failure_status(_pre_parse_output_location(argv), reason)
        return

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
                    help="pinned validator path (default: the pinned openxdox "
                         f"product's own {snapshot_mod.VALIDATOR_RELPATH}, "
                         "composed with its schemas)")
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
