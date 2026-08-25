#!/usr/bin/env python3
"""Project xFactory document lifecycle states into NotebookLM books.

Reference implementation of the openxFactory `lifecycle-notebook-projection`
capability (docs/lifecycle-notebook-projection.md). Book definitions, title
prefixes, charter text, and chat framing below are contract conformance —
change them only through an OpenSpec delta to that capability.

Scans the xFactory workspace for governance docs carrying the controlled
Status taxonomy (openxFactory/docs/document-lifecycle.md) and reconciles
the NotebookLM books so membership is always derived, never curated:

  ideation-<repo>  <- Status: brainstorm, staged (ONE book per governed repo;
                      split-ideation-book-per-repo, after the shared book hit
                      the 300-source cap 2026-08-10)
  drafts           <- Status: draft
  canon            <- Status: ratified, standard  (+ promoted openspec/specs)

Books are resolved by NOTEBOOK TITLE (the provider's truth). The alias
family (xf-ideation-<repo-slug>, xf-drafts, xf-canon) is a machine-local
operator convenience: re-registered idempotently per run, never fatal when
absent — a second host or CI runner carries no alias store.

Statuses record, superseded, and retired are excluded by design. Source
titles carry a "[status]" prefix so citations self-declare authority
(L1 notebook synthesis per docs/notebooklm-source-workspaces.md).

Usage:
  python3 sync-notebooklm-books.py <workspace-root> [--apply] [--book NAME]
  python3 sync-notebooklm-books.py <workspace-root> --import-exports NOTEBOOK [--apply]
  python3 sync-notebooklm-books.py <workspace-root> --import-new-sources NOTEBOOK --target-path PATH [--apply]
  python3 sync-notebooklm-books.py <workspace-root> --session-ref BRANCH [--session-repository REPO] [--session-retire] [--apply]
  python3 sync-notebooklm-books.py <workspace-root> --session-sweep [--apply]

Dry-run by default; --apply performs adds/deletes via the nlm CLI.
Import modes are also dry-run by default. The --import-new-sources mode imports
all non-seed sources in an analysis notebook to the brainstorm, staging, or
active proposal supporting-documents folder that owns the notebook. Converting
a note to a source, adding a web source, or adding any other NotebookLM source
makes it eligible for import.
State manifest: <workspace-root>/.claude/nlm-sync-manifest.json

The default (book-sync) mode also runs the ideation-dashboard workbench
orphan sweep (`workbench_orphan_sweep` below): --apply deletes `xf-wb-*`
scratch notebooks no live workbench manifest binds; the dry run prints the
plan. Only `xf-wb-*` titles are ever candidates — the lifecycle books above
can never be swept.

The --session-ref mode is the fourth family: ONE
`xf-session-<repository>-<branch>` notebook per LIVE branch session
(007-workbench-branch-sessions, FR-036-FR-040), created / re-synced / retired
from that session's WORKTREE. It is deliberately independent of everything
above: the lifecycle books stay MAIN-ONLY (a session worktree lives in
`<repo>-worktrees/`, outside every book's walk — the exclusion is never
relaxed), the session leaves no manifest for the sweep to trip over, and the
`xf-session-` namespace is disjoint from the swept `xf-wb-` one. See
`session_source_set` / `sync_session_notebook` below.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

STATIC_BOOKS = {
    "drafts": {"alias": "xf-drafts", "title": "xFactory — Working Drafts",
               "statuses": {"draft"}},
    "canon": {"alias": "xf-canon", "title": "xFactory — Canon",
              "statuses": {"ratified", "standard"}},
}
# Legacy name kept for external iterators (tests, sweep wiring): the SHARED
# books. The per-repo ideation family is derived at scan time; its aliases
# all carry IDEATION_ALIAS_PREFIX.
BOOKS = STATIC_BOOKS

IDEATION_STATUSES = {"brainstorm", "staged"}
IDEATION_KEY_PREFIX = "ideation-"
IDEATION_ALIAS_PREFIX = "xf-ideation-"
IDEATION_TITLE_PREFIX = "xFactory Ideation — "

# NotebookLM's per-notebook source cap (plan-dependent platform property;
# contract surface per the projection capability's capacity guard — recorded
# in docs/lifecycle-notebook-projection.md). The 2026-08-10 incident: the
# shared ideation book reached it mid-run and every later add died.
NOTEBOOK_SOURCE_CAP = 300

# A single argv string on Linux caps at MAX_ARG_STRLEN (131072 bytes), so a
# governance doc that large cannot ride `--text` — proven live 2026-08-10 by
# the promoted ideation-dashboard spec (Errno 7 killed the canon book). An
# oversized doc uploads as a temp file and is renamed to its contract title
# (the CLI titles a --file source by FILENAME and ignores --title).
MAX_TEXT_ARG_BYTES = 100_000
SOURCE_ID_ECHO_RE = re.compile(r"Source ID:\s*(\S+)")
# Headroom (in sources, not percent: lead time is what matters and it must
# not scale away) at or below which the guard warns and names the owed
# split delta for a book with no successor split defined.
CAP_WARN_HEADROOM = 30


@dataclass(frozen=True)
class BookSpec:
    """One lifecycle book's identity: manifest/report key, provider title
    (the resolution key), and machine-local alias (convenience only)."""
    key: str
    alias: str
    title: str


def ideation_spec(repo: str) -> BookSpec:
    slug = repo.lower()
    return BookSpec(key=f"{IDEATION_KEY_PREFIX}{slug}",
                    alias=f"{IDEATION_ALIAS_PREFIX}{slug}",
                    title=f"{IDEATION_TITLE_PREFIX}{repo}")


def static_spec(book: str) -> BookSpec:
    cfg = STATIC_BOOKS[book]
    return BookSpec(key=book, alias=cfg["alias"], title=cfg["title"])

# Added to every book regardless of status so chat can ground ideas
# against the running system's shape.
GROUNDING = [
    "openxFactory/docs/document-lifecycle.md",
    "openxFactory/docs/terminology-and-repo-topology.md",
    "openxFactory/docs/architecture.md",
]

CHARTER_TITLE = "00 [charter] Read me first"
HYBRID_CHARTER_TITLE = "00 [hybrid charter] Read me first"
CHARTER = """This notebook is a derived projection of the xFactory governance
document lifecycle (see source: [grounding] openxFactory: document-lifecycle).
It is maintained by scripts/sync-notebooklm-books.py in openxFactory; do not
hand-curate sources — membership follows each document's Status header.

Title prefixes declare epistemic weight:
  [brainstorm] non-normative ideas; may contradict the running system freely
  [staged]     organized fragments heading toward an OpenSpec proposal
  [draft]      normative intent, not yet ratified
  [ratified]   backed by an approved OpenSpec change
  [standard]   promoted canon — the running system's authority
  [spec]       promoted OpenSpec capability spec — the running system's authority
  [grounding]  context docs duplicated into every book

Per xFactory policy (openxFactory/docs/notebooklm-source-workspaces.md), all
output of this notebook is L1 notebook synthesis: it may raise claims but
never decides policy, memory, or workflow. Ideas here sit ON TOP OF a running
system; only [standard]/[spec] sources describe that system authoritatively."""

CHAT_PROMPT = (
    "Sources titled [brainstorm] or [staged] are non-normative ideas layered "
    "on top of a running system. Sources titled [standard], [spec], or "
    "[ratified] describe the system as governed today; [draft] is intended "
    "but unratified. Never present an idea as current behavior. In every "
    "answer, state whether each claim comes from the running system or from "
    "a proposal, and describe conflicts as 'proposed change from current', "
    "not as fact."
)

STATUS_RE = re.compile(r"^Status: (brainstorm|staged|draft|ratified|standard|superseded|retired|record)\s*$", re.M)
# tests/ excluded: fixture corpora carry deliberate-violation statuses
# (fake ratified/standard docs) that must never project into the books.
SKIP_PARTS = {".git", "node_modules", "installs", "__pycache__", "tests"}
EXPORT_RE = re.compile(r"^\[export:(brainstorm|staged)\]\s+(.+?)\s*$")
SOURCE_ID_RE = re.compile(r"^NotebookLM source id:\s*(\S+)\s*$", re.M)
MANAGED_SOURCE_PREFIXES = (
    "[brainstorm]",
    "[staged]",
    "[draft]",
    "[ratified]",
    "[standard]",
    "[spec]",
    "[grounding]",
)


@dataclass(frozen=True)
class ExportTarget:
    status: str
    repo: str
    topic: str
    title: str
    source_title: str


@dataclass(frozen=True)
class ExportPlan:
    source_id: str
    source_title: str
    status: str
    repo: str
    topic: str
    title: str
    path: Path
    already_imported: bool = False


@dataclass(frozen=True)
class ImportTarget:
    status: str
    repo: str
    topic: str
    path: Path


def nlm(*args: str, parse: bool = True):
    assert_still_bound()
    res = subprocess.run(["nlm", *args], capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"nlm {' '.join(args[:3])}...: {res.stderr.strip()[:300]}")
    if not parse:
        return res.stdout
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        return res.stdout


def slug_part(value: str) -> str:
    """Single path segment from untrusted notebook-title text: no slashes,
    no dot sequences — a hostile title must not traverse the workspace."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "untitled"


def parse_export_title(title: str, default_repo: str = "openxFactory") -> ExportTarget | None:
    """Parse [export:*] source titles created by converted NotebookLM notes.

    Supported forms:
      [export:brainstorm] openxFactory: topic - idea title
      [export:staged] doc-health-checks - idea title
      [export:brainstorm] openxFactory: topic
    """
    m = EXPORT_RE.match(title)
    if not m:
        return None
    status, rest = m.groups()
    repo = default_repo
    if ":" in rest:
        maybe_repo, rest = rest.split(":", 1)
        repo = maybe_repo.strip() or default_repo
        rest = rest.strip()
    if not re.fullmatch(r"[A-Za-z0-9-]+", repo):
        return None  # repo names never contain path syntax; drop the source
    if " - " in rest:
        topic, idea_title = rest.split(" - ", 1)
    else:
        topic, idea_title = rest, rest
    topic = slug_part(topic)
    idea_title = idea_title.strip() or topic
    return ExportTarget(status=status, repo=repo, topic=topic,
                        title=idea_title, source_title=title)


def repo_path(root: Path, repo: str) -> Path:
    direct = root / repo
    if direct.exists() or repo == "openxFactory":
        return direct
    nested = root / "xFactories" / repo
    return nested


def session_repository_of(parts: tuple[str, ...]) -> str | None:
    """The REPOSITORY a path inside a session worktree belongs to, or None.

    A session worktree lives at `<repo>-worktrees/sessions/<flattened-branch>/`
    (research R7), so the container's own name carries the repository. Without
    this, an FR-041 import into a session worktree would stamp
    `Repository context: <repo>-worktrees` — a repository that does not exist —
    into the header contract it is required to apply unchanged."""
    head = list(parts[1:] if parts and parts[0] == "xFactories" else parts)
    if len(head) < 2 or not head[0].endswith(SESSION_CONTAINER_SUFFIX):
        return None
    if head[1] != "sessions":
        return None
    return head[0][:-len(SESSION_CONTAINER_SUFFIX)] or None


def target_from_path(root: Path, target_path: str) -> ImportTarget:
    raw = Path(target_path)
    path = raw if raw.is_absolute() else root / raw
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("--target-path must stay inside the workspace") from exc
    parts = rel.parts
    repo = parts[0] if parts[0] != "xFactories" else parts[1]
    # A branch-session worktree target keeps the SESSION's repository name
    # (FR-041): the header contract is applied verbatim, which means its
    # `Repository context:` must name a real repository, not a container.
    repo = session_repository_of(parts) or repo
    if "ideation" in parts:
        idx = parts.index("ideation")
        if (idx + 2 >= len(parts)
                or parts[idx + 1] not in {"brainstorm", "staging"}):
            raise ValueError(
                "--target-path must name an ideation brainstorm/staging topic"
            )
        status = "brainstorm" if parts[idx + 1] == "brainstorm" else "staged"
        return ImportTarget(
            status=status, repo=repo, topic=parts[idx + 2], path=path.resolve()
        )

    try:
        idx = parts.index("openspec")
    except ValueError as exc:
        raise ValueError(
            "--target-path must name ideation or active proposal support"
        ) from exc
    tail = parts[idx:]
    if (len(tail) != 4 or tail[1] != "changes" or tail[2] == "archive"
            or tail[3] != "supporting-docs"):
        raise ValueError(
            "--target-path must name openspec/changes/<change>/supporting-docs"
        )
    change = root.joinpath(*parts[:idx + 3])
    if not (change / "proposal.md").is_file():
        raise ValueError("--target-path must belong to an active OpenSpec change")
    if not (path / "manifest.yaml").is_file():
        raise ValueError("proposal supporting-docs target must have manifest.yaml")
    return ImportTarget(
        status="draft", repo=repo, topic=tail[2], path=path.resolve()
    )


def export_destination(root: Path, target: ExportTarget, imported_on: str) -> Path:
    base = repo_path(root, target.repo)
    area = "brainstorm" if target.status == "brainstorm" else "staging"
    return base / "ideation" / area / target.topic / f"notebooklm-ideas-{imported_on}.md"


def imported_source_ids(root: Path, extra_roots: Sequence[Path] = ()) -> set[str]:
    """Every NotebookLM source id already imported anywhere in the workspace —
    the idempotency key (a re-run imports nothing).

    `extra_roots` covers a destination OUTSIDE the two family roots: an FR-041
    session import lands inside `<repo>-worktrees/`, which neither `openxFactory`
    nor `xFactories` contains, so without the target's own directory in scope the
    dedupe would silently stop working exactly where a session re-syncs most."""
    ids: set[str] = set()
    bases = [root / rel for rel in ("openxFactory", "xFactories")]
    bases.extend(Path(extra) for extra in extra_roots)
    for base in bases:
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if "ideation" not in path.parts and "supporting-docs" not in path.parts:
                continue
            ids.update(SOURCE_ID_RE.findall(path.read_text(errors="replace")))
    return ids


def export_plan(root: Path, notebook: str, imported_on: str) -> list[ExportPlan]:
    sources = list_sources(notebook)
    seen = imported_source_ids(root)
    planned: list[ExportPlan] = []
    for source in sources:
        sid = source.get("id") or source.get("source_id")
        title = source.get("title", "")
        target = parse_export_title(title)
        if not sid or target is None:
            continue
        planned.append(ExportPlan(
            source_id=sid,
            source_title=title,
            status=target.status,
            repo=target.repo,
            topic=target.topic,
            title=target.title,
            path=export_destination(root, target, imported_on),
            already_imported=sid in seen,
        ))
    return planned


def list_sources(notebook: str) -> list[dict]:
    sources = nlm("source", "list", notebook, "--json")
    if isinstance(sources, dict):
        sources = sources.get("sources", [])
    if isinstance(sources, str):
        return []
    return sources


def is_seed_source(title: str) -> bool:
    """Whether a notebook source is one THIS TOOLING put there, and therefore not
    importable back out.

    The third clause closes an unbounded self-amplification loop (PR #49 review
    finding 12, measured at 788 -> 2120 -> 4784 -> 10112 bytes over four rounds).
    A projected SESSION or reference-set source's title is `<path>  #<hash>`
    (`workbench.managed_source_title`), which matches neither charter title nor a
    `[status]` prefix — so the import planned the notebook's OWN projected output,
    wrote it into the worktree as a `Status: staged` governed document, which
    `workbench.session_documents` then included, which re-projected under a NEW
    source id, which the source-id dedupe therefore could not stop. The predicate
    was a DENYLIST of seed titles; the fix is to recognise everything this tooling
    itself projected, which `parse_managed_source_title` already does."""
    parse_managed_source_title = _dashboard_module(
        "workbench").parse_managed_source_title

    if title in {CHARTER_TITLE, HYBRID_CHARTER_TITLE}:
        return True
    if title.startswith(MANAGED_SOURCE_PREFIXES):
        return True
    return parse_managed_source_title(title) is not None


def new_source_plan(root: Path, notebook: str, target: ImportTarget,
                    imported_on: str) -> list[ExportPlan]:
    sources = list_sources(notebook)
    # the target's own folder is always in dedupe scope, which is what makes a
    # session-worktree destination idempotent too (FR-041)
    seen = imported_source_ids(root, extra_roots=(target.path,))
    planned: list[ExportPlan] = []
    for source in sources:
        sid = source.get("id") or source.get("source_id")
        title = source.get("title", "")
        if not sid or is_seed_source(title):
            continue
        planned.append(ExportPlan(
            source_id=sid,
            source_title=title,
            status=target.status,
            repo=target.repo,
            topic=target.topic,
            title=title.strip() or sid,
            path=target.path / f"notebooklm-ideas-{imported_on}.md",
            already_imported=sid in seen,
        ))
    return planned


def display_path(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def imported_file_header(plan: ExportPlan, notebook: str) -> str:
    origin = (
        "NotebookLM source imported from the analysis notebook. Notes enter "
        "this path only after a human converts them to sources; web, file, "
        "Drive, and other added sources enter as sources directly."
    )
    return (
        f"# NotebookLM Ideas: {plan.topic}\n\n"
        f"Status: {plan.status}\n"
        "Kind: reference\n"
        f"Repository context: {plan.repo}\n"
        f"Source workspace: {notebook}\n"
        "Authority: L1 notebook synthesis\n"
        f"Origin: {origin}\n\n"
        "These notes are imported evidence and idea material. They do not "
        "decide policy, memory, release scope, or OpenSpec approval.\n"
    )


def render_imported_entry(plan: ExportPlan, notebook: str, content: str) -> str:
    body = content.strip()
    return (
        f"\n## {plan.title}\n\n"
        f"NotebookLM source id: {plan.source_id}\n"
        f"NotebookLM source title: {plan.source_title}\n"
        f"Source workspace: {notebook}\n\n"
        f"{body}\n"
    )


def source_content_text(raw: str) -> str:
    """Return source text from raw CLI output, tolerating JSON wrappers."""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    value = payload.get("value") if isinstance(payload, dict) else None
    if isinstance(value, dict) and isinstance(value.get("content"), str):
        return value["content"]
    if isinstance(payload, dict) and isinstance(payload.get("content"), str):
        return payload["content"]
    return raw


def append_import(root: Path, plan: ExportPlan, notebook: str, content: str) -> None:
    """Write an imported entry, refusing any destination that resolves
    outside the workspace (titles are untrusted notebook content)."""
    resolved = plan.path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise SystemExit(f"refusing to write outside workspace: {plan.path}")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    if not resolved.exists():
        resolved.write_text(imported_file_header(plan, notebook), encoding="utf-8")
    with resolved.open("a", encoding="utf-8") as fh:
        fh.write(render_imported_entry(plan, notebook, content))


def import_exported_sources(root: Path, notebook: str, apply: bool, imported_on: str) -> int:
    planned = export_plan(root, notebook, imported_on)
    if not planned:
        print(f"[exports] no [export:*] sources found in {notebook}")
        return 0
    count = 0
    for plan in planned:
        if plan.already_imported:
            print(f"[exports] SKIP {plan.source_title} (already imported)")
            continue
        print(f"[exports] ADD  {plan.source_title} -> {display_path(plan.path, root)}")
        count += 1
        if not apply:
            continue
        content = source_content_text(
            nlm("source", "content", plan.source_id, parse=False)
        )
        append_import(root, plan, notebook, content)
    return count


def import_new_sources(root: Path, notebook: str, target_path: str, apply: bool,
                       imported_on: str) -> int:
    target = target_from_path(root, target_path)
    # The notebook and the destination must be the SAME session, or neither may be
    # one (FR-041; PR #49 review finding 12). Checked BEFORE anything is planned,
    # so a mis-targeted session import writes nothing at all.
    session = bind_session_import(root, notebook, target)
    planned = new_source_plan(root, notebook, target, imported_on)
    if not planned:
        print(f"[sources] no new importable sources found in {notebook}")
        return 0
    count = 0
    written: list[Path] = []
    for plan in planned:
        if plan.already_imported:
            print(f"[sources] SKIP {plan.source_title} (already imported)")
            continue
        print(f"[sources] ADD  {plan.source_title} -> {display_path(plan.path, root)}")
        count += 1
        if not apply:
            continue
        content = source_content_text(
            nlm("source", "content", plan.source_id, parse=False)
        )
        append_import(root, plan, notebook, content)
        written.append(plan.path.resolve())
    if session is not None and written:
        commit_session_import(session, written, notebook=notebook)
    return count


def commit_session_import(session: SessionTarget, written: Sequence[Path], *,
                          notebook: str) -> str | None:
    """LAND the imported file on the session branch (FR-041).

    FR-041 says the import "MUST write into the origin folder INSIDE the session
    worktree AND LAND ON THE SESSION BRANCH", and it never landed: the file stayed
    UNTRACKED. That is not a harmless difference. The file carries `Status:
    staged` under a governed root, so `workbench.session_documents` includes it
    immediately — it projects into the notebook and into the session's panels as
    live governed material — while BOTH endings run `git worktree remove --force`,
    which deletes untracked files outright. On a MERGE the returned evidence never
    reaches `main`; on an ABANDON it is erased silently. Measured during the PR #49
    adjudication.

    It goes through the GOVERNED commit path and no other: `SessionGit`, whose
    staging is explicit-path only, whose `commit(only=…)` binds the commit to
    exactly the files this import wrote, and under `worktree_action_lock` so it
    cannot interleave with a gate action's stage → commit transaction (FR-006,
    SC-003). It writes NO gate-action record: an out-of-band human import is not a
    gate action, the schema has no verb for it, and a record naming one would
    attest to something that did not happen. The commit message names the notebook
    so the provenance is on the branch as well as in the file's header.

    A commit that cannot be made is REPORTED, never fatal — the bytes are already
    in the worktree and telling the human they are uncommitted is strictly better
    than losing the import.

    WHERE it lands is asked before it lands (PR #49 review finding 5, wave 2). The
    binding this call carries was resolved by `bind_session_import` BEFORE the
    sources were fetched, and every fetch is a network round trip, so the window
    between the binding and this commit is arbitrarily longer than a gate action's.
    A human's `git checkout` inside the worktree during it sent the commit onto
    whatever branch the directory then held while this function printed `COMMITTED
    on <session branch>` — reproduced: the sha was reachable only from
    `somebody-elses-branch` and the session branch had not moved. So the joint
    signal is verified inside the lock this already claims, using the same
    `assert_git_holds_branch` the gate action uses; a drift is a `SessionRefused`,
    which lands in the report below, so the import still never loses the bytes."""
    bs = _dashboard_module("branch_session")
    sg = _dashboard_module("session_git")
    worktree = Path(session.worktree)
    # the SERVED root the guard is built around is the CHECKOUT, never the
    # container: a `SessionGit` rooted at `sessions/` would classify the worktree
    # itself as the served checkout and refuse the stage outright (FR-004)
    git = sg.SessionGit(session.checkout or worktree.parents[2])
    relatives = sorted({p.relative_to(worktree).as_posix() for p in written})
    try:
        with git.worktree_action_lock(worktree,
                                      action=f"notebooklm import from {notebook}"):
            bs.assert_git_holds_branch(
                git, worktree, session.branch,
                during=f"the notebooklm import from {notebook}")
            git.stage(worktree, relatives)
            sha = git.commit(
                worktree,
                f"notebooklm import: {', '.join(relatives)}\n\n"
                f"Source-Notebook: {notebook}\n",
                only=relatives)
    except Exception as exc:  # noqa: BLE001 - reported; the bytes are already there
        print(f"[session] NOT COMMITTED on {session.branch}: {exc} — the imported "
              f"file is in {worktree} but UNTRACKED, and both endings remove that "
              f"worktree with `--force`. Commit it before the session ends "
              "(FR-041)")
        return None
    print(f"[session] COMMITTED on {session.branch}: {sha} ({', '.join(relatives)})")
    return sha


def in_nested_checkout(f: Path, basep: Path) -> bool:
    """True when f sits inside a git working copy nested below basep.

    Worktree checkouts and embedded clones carry a .git entry at their
    root; their documents must never project (duplicate or unmerged
    sources) — see the lifecycle-notebook-projection corpus scan scope.
    """
    for parent in f.parents:
        if parent == basep:
            return False
        if (parent / ".git").exists():
            return True
    return False


def pinned_factory_paths(root: Path) -> list[str]:
    """xFactories/<repo> paths pinned in .gitmodules — the only dirs scan()
    and the sweep may treat as repos. Transient siblings (review-lane copies
    like OpsxFactory-review-<sha>.<tmp>, worktree containers) polluted the
    canon book on 2026-07-14; pin-state is the authoritative filter. Falls
    back to the old suffix heuristic when .gitmodules is absent."""
    gm = root / ".gitmodules"
    if gm.is_file():
        pins = re.findall(r"^\s*path\s*=\s*(xFactories/\S+)\s*$",
                          gm.read_text(), re.M)
        if pins:
            return sorted(p for p in pins if (root / p).is_dir())
    factories = root / "xFactories"
    if not factories.is_dir():
        # a workspace with no factory checkouts at all (a lone openxFactory
        # clone, a scratch root): no pins, not an error
        return []
    return [str(p.relative_to(root))
            for p in sorted(factories.iterdir())
            if p.is_dir() and not p.name.endswith(SESSION_CONTAINER_SUFFIX)]


# A source title is the projection's IDENTITY KEY: scan() derives a set keyed
# by document PATH and sync_book() reconciles it against a live book BY TITLE,
# holding each title at one source. A derivation that is not injective
# therefore DISPLACES documents silently — four MedxFactory staging topics
# shared one source until 2026-08-25. The statuses below are the ones that
# actually reach a book; a `record`, `superseded` or `retired` document is
# scanned and projected by nothing, so it is outside the uniqueness scope and
# must not qualify anyone else's title.
PROJECTED_STATUSES = IDEATION_STATUSES | {
    s for cfg in STATIC_BOOKS.values() for s in cfg["statuses"]}

# The `[spec]` and `[grounding]` families are DELIBERATELY outside the
# uniqueness scope (add-projection-title-uniqueness § 2.2), not filtered out by
# accident: `[spec]` is keyed by a promoted capability's DIRECTORY name and
# `[grounding]` by a fixed three-document set, so neither is derived from a
# file stem and neither can collide with one. Measurement on 2026-08-25 showed
# that folding them in over-qualified one `drafts` title for no reason.
STEM_SCOPE_EXCLUDES = ("[spec]", "[grounding]")

# `README` floors at its parent directory — the title today's rule already
# produces for every README, so the amendment never SHORTENS an existing
# title. It is a MINIMUM and not a special case: a README still ambiguous two
# segments deep keeps qualifying like any other document.
README_FLOOR_SEGMENTS = 2


def title_segments(rel: Path) -> tuple[str, ...]:
    """A document's path as title segments, outermost first.

    The repository DIRECTORY is the outermost segment, so a repository-root
    `README.md` floors at `<repo>/README` — byte for byte the title the old
    `f.parent.name` rule produced. `xFactories/` is a container, not a path
    component of the repository, so it never appears.
    """
    parts = rel.parts[1:] if rel.parts[0] == "xFactories" else rel.parts
    return (*parts[:-1], Path(parts[-1]).stem)


def derive_stems(documents: Sequence[tuple[str, str, tuple[str, ...]]]
                 ) -> dict[str, str]:
    """Resolve every projected document's title stem. Returns {relpath: stem}.

    `documents` is (relpath, repository, segments) over the documents that
    actually project. A stem is the SHORTEST path suffix that no other
    projected document OF THE SAME REPOSITORY shares
    (docs/lifecycle-notebook-projection.md § 2). The scope is the repository's
    whole projected set rather than one book or one status, so a document is
    never retitled because a same-stem sibling's `Status:` header moved.

    The result is injective per repository, and therefore per book: two
    documents can only stop at the same suffix string if they stopped at the
    same DEPTH, and at that depth neither would have found the suffix
    unshared. A document that never finds an unshared suffix falls back to its
    whole segment path, which is unique by construction.
    """
    by_repo: dict[str, list[tuple[str, tuple[str, ...]]]] = {}
    for rel, repo, segs in documents:
        by_repo.setdefault(repo, []).append((rel, segs))
    stems: dict[str, str] = {}
    for docs in by_repo.values():
        # how many documents of this repository share each suffix, per depth
        counts: dict[int, dict[str, int]] = {}
        for _rel, segs in docs:
            for k in range(1, len(segs) + 1):
                level = counts.setdefault(k, {})
                suffix = "/".join(segs[-k:])
                level[suffix] = level.get(suffix, 0) + 1
        for rel, segs in docs:
            floor = (README_FLOOR_SEGMENTS
                     if segs[-1].lower() == "readme" else 1)
            stems[rel] = "/".join(segs)  # whole path: distinct by construction
            for k in range(min(floor, len(segs)), len(segs) + 1):
                suffix = "/".join(segs[-k:])
                if counts[k][suffix] == 1:
                    stems[rel] = suffix
                    break
    return stems


def scan(root: Path) -> tuple[dict[str, dict[str, str]], dict[str, BookSpec]]:
    """Return ({book_key: {relpath: title}}, {book_key: BookSpec}) desired state.

    Ideation membership is per-repository and STATUS-DERIVED ONLY: an
    ideation book (and therefore its lazy creation) exists exactly when its
    repo has at least one brainstorm/staged document — charter and grounding
    are seeds added to books that exist, never membership that creates one
    (split-ideation-book-per-repo).

    TWO PASSES, in this order, because uniqueness is a property of the
    FINISHED set while the walk visits one repository at a time: collect each
    projected document's segments, then resolve every title at once
    (add-projection-title-uniqueness § 2.1)."""
    desired: dict[str, dict[str, str]] = {b: {} for b in STATIC_BOOKS}
    specs: dict[str, BookSpec] = {b: static_spec(b) for b in STATIC_BOOKS}
    found: list[tuple[str, str, str, tuple[str, ...]]] = []
    for base in ["openxFactory", *pinned_factory_paths(root)]:
        basep = root / base
        for f in sorted(basep.rglob("*.md")):
            rel = f.relative_to(root)
            if SKIP_PARTS.intersection(rel.parts) or "openspec" in rel.parts:
                continue
            if in_nested_checkout(f, basep):
                continue
            m = STATUS_RE.search(f.read_text(errors="replace")[:2000])
            if not m:
                continue
            status = m.group(1)
            if status not in PROJECTED_STATUSES:
                continue  # scanned, projected by no book, out of scope
            repo = rel.parts[0] if rel.parts[0] != "xFactories" else rel.parts[1]
            found.append((str(rel), repo, status, title_segments(rel)))
    stems = derive_stems([(rel, repo, segs) for rel, repo, _st, segs in found])
    for rel, repo, status, _segs in found:
        title = f"[{status}] {repo}: {stems[rel]}"
        if status in IDEATION_STATUSES:
            spec = ideation_spec(repo)
            specs.setdefault(spec.key, spec)
            desired.setdefault(spec.key, {})[rel] = title
        for book, cfg in STATIC_BOOKS.items():
            if status in cfg["statuses"]:
                desired[book][rel] = title
    # promoted specs -> canon
    for f in sorted((root / "openxFactory/openspec/specs").glob("*/spec.md")):
        rel = f.relative_to(root)
        desired["canon"][str(rel)] = f"[spec] openxFactory: {f.parent.name}"
    # grounding set -> every book that exists by membership
    for g in GROUNDING:
        stem = Path(g).stem
        for book in desired:
            desired[book][g] = f"[grounding] openxFactory: {stem}"
    return desired, specs


def list_notebooks() -> list[dict]:
    rows = nlm("notebook", "list", "--json")
    if isinstance(rows, dict):
        rows = rows.get("notebooks", [])
    if isinstance(rows, str):
        return []
    return [r for r in rows if isinstance(r, dict)]


def _ensure_alias(spec: BookSpec, notebook_id: str) -> None:
    """Idempotent, NEVER fatal: aliases live in a per-machine CLI store, so a
    host that lacks one must gain it quietly, and a host that cannot set one
    must not lose the run over a convenience."""
    try:
        nlm("alias", "set", spec.alias, notebook_id, parse=False)
    except Exception as exc:  # noqa: BLE001
        print(f"[{spec.key}] NOTICE alias {spec.alias!r} not registered "
              f"(non-fatal: {exc})")


def ensure_workspace_record(root: Path, spec: BookSpec, notebook_id: str) -> None:
    """Write the book's external_source_workspace record at creation — its
    provider id does not exist until the notebook does
    (split-ideation-book-per-repo; model: docs/notebooklm-source-workspaces.md §6)."""
    path = root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
    record_id = f"workspace-xfactory-lifecycle-{spec.key}"
    if not path.is_file():
        print(f"[{spec.key}] NOTICE workspace registry missing at {path}; "
              f"record {record_id} not written")
        return
    text = path.read_text(encoding="utf-8")
    if f"id: {record_id}" in text:
        if notebook_id not in text:
            print(f"[{spec.key}] NOTICE workspace record {record_id} exists "
                  f"with a DIFFERENT provider_notebook_id — reconcile by hand")
        return
    created = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    repo = spec.title.removeprefix(IDEATION_TITLE_PREFIX)
    block = (
        f"  - kind: external_source_workspace\n"
        f"    schema_version: 1\n"
        f"    id: {record_id}\n"
        f"    provider: notebooklm\n"
        f"    provider_notebook_id: {notebook_id}\n"
        f"    owner_layer: domain_hermes\n"
        f"    scope:\n"
        f"      domain_id: xfactory\n"
        f"      client_id: null\n"
        f"      customer_id: null\n"
        f"    purpose: derived projection of brainstorm and staged governance docs ({repo})\n"
        f"    default_authority_level: L1_notebook_synthesis\n"
        f"    created_at: \"{created}\"\n"
        f"    managed_by: openxFactory/scripts/sync-notebooklm-books.py\n"
    )
    path.write_text(text.rstrip("\n") + "\n" + block, encoding="utf-8")
    print(f"[{spec.key}] workspace record {record_id} -> "
          f"{path.relative_to(root)} (commit it with the migration evidence)")


def resolve_or_create_book(root: Path, spec: BookSpec, apply: bool,
                           notebooks: list[dict] | None = None,
                           *, bind_alias: bool = True
                           ) -> tuple[str | None, bool]:
    """Resolve a book to its notebook id BY TITLE; lazily create it in apply
    mode. Returns (notebook_id | None, fully_ok). A dry run over a missing
    book reports the pending creation (verb CREATE — deliberately not
    ADD/DEL/UPD) and returns (None, True): the diff then runs against an
    empty listing so the pending adds are visible drift."""
    rows = notebooks if notebooks is not None else list_notebooks()
    by_title = {r.get("title"): r.get("id") for r in rows if r.get("id")}
    nid = by_title.get(spec.title)
    if nid:
        # `bind_alias=False` is the READ-ONLY caller's contract. The alias store
        # is a single flat, PROFILE-INDEPENDENT file, so registering here is a
        # write with cross-account consequences — a parity proof that repoints
        # xf-canon is not a proof, it is a migration nobody asked for.
        if bind_alias:
            _ensure_alias(spec, nid)
        return nid, True
    if not apply:
        print(f"[{spec.key}] CREATE {spec.title} (book missing; created on --apply)")
        return None, True
    # The one create form both CLI generations speak: NO --json (nlm 0.5.26
    # rejects it on create — live drift 2026-08-04, see
    # ideation_dashboard/workbench.py _create_titled); the id comes from a
    # fresh title listing, never from the create's echo.
    nlm("notebook", "create", spec.title, parse=False)
    time.sleep(2)
    fresh = {r.get("title"): r.get("id") for r in list_notebooks() if r.get("id")}
    nid = fresh.get(spec.title)
    if not nid:
        raise RuntimeError(
            f"created notebook {spec.title!r} but a fresh listing does not "
            f"resolve it by title")
    print(f"[{spec.key}] CREATED {spec.title} ({nid})")
    ok = True
    _ensure_alias(spec, nid)
    # Contract surface at creation (split-ideation-book-per-repo): tags keep
    # the book inside cross-tag query scope; framing is the capability's
    # Authority-framing requirement. A failure is REPORTED and fails the run
    # (nonzero), never silent — an unframed or untagged book is
    # non-conformant, not merely imperfect.
    try:
        nlm("tag", "add", nid, "--tags", "xfactory,lifecycle", parse=False)
    except Exception as exc:  # noqa: BLE001
        ok = False
        print(f"[{spec.key}] FAILED tagging {spec.title!r}: {exc}")
    try:
        nlm("chat", "configure", nid, "--goal", "custom", "--prompt",
            CHAT_PROMPT, parse=False)
    except Exception as exc:  # noqa: BLE001
        ok = False
        print(f"[{spec.key}] FAILED chat framing for {spec.title!r}: {exc}")
    ensure_workspace_record(root, spec, nid)
    time.sleep(2)
    return nid, ok


def _add_with_one_retry(*args: str) -> str:
    """One retry after a pause: the provider intermittently 500s behind an
    EMPTY CLI error (live-proven twice on 2026-08-10 — the cap incident's
    signature and a mid-canon transient). A transient must not kill a book;
    a real failure still raises on the second attempt."""
    try:
        return nlm(*args, parse=False)
    except RuntimeError as exc:
        print(f"    retrying once after: {exc}")
        time.sleep(10)
        return nlm(*args, parse=False)


def add_text_source(handle: str, text: str, title: str) -> None:
    """Add one text source, riding a temp file + rename when the content is
    too large for a single argv string (see MAX_TEXT_ARG_BYTES)."""
    if len(text.encode("utf-8", "replace")) <= MAX_TEXT_ARG_BYTES:
        _add_with_one_retry("source", "add", handle, "--text", text,
                            "--title", title)
        return
    fd, tmp = tempfile.mkstemp(suffix=".md", prefix="xf-sync-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        out = _add_with_one_retry("source", "add", handle, "--file", tmp)
        m = SOURCE_ID_ECHO_RE.search(out or "")
        if not m:
            raise RuntimeError(
                f"oversized source {title!r} uploaded but the CLI echoed no "
                f"source id to rename — rename it to the contract title by hand")
        time.sleep(2)
        nlm("source", "rename", m.group(1), title, "--notebook", handle,
            parse=False)
    finally:
        os.unlink(tmp)


def sync_book(root: Path, spec: BookSpec, desired: dict[str, str],
              manifest: dict, apply: bool, *,
              notebooks: list[dict] | None = None) -> tuple[bool, bool]:
    """Reconcile ONE book. Returns (ok, overflowed).

    The book is resolved by title and addressed by notebook id; the capacity
    guard runs before any mutation (split-ideation-book-per-repo): projected
    occupancy counts the desired managed set + the charter + every unmanaged
    source the reconciliation deliberately preserves."""
    key = spec.key
    nid, ok = resolve_or_create_book(root, spec, apply, notebooks)
    handle = nid if nid else spec.title  # dry-run over a missing book
    existing = nlm("source", "list", nid, "--json") if nid else []
    if isinstance(existing, str):
        existing = []
    by_title: dict[str, list[str]] = {}
    unmanaged = 0
    for s in existing:
        if not s.get("id"):
            continue
        title = s.get("title", "")
        by_title.setdefault(title, []).append(s["id"])
        if not (title.startswith("[") or title == CHARTER_TITLE):
            unmanaged += 1
    mf = manifest.setdefault(key, {})

    # ---- capacity guard (before any mutation) ----
    overflowed = False
    projected = len(desired) + 1 + unmanaged  # members + charter + unmanaged
    headroom = NOTEBOOK_SOURCE_CAP - projected
    if projected > NOTEBOOK_SOURCE_CAP:
        overflowed = True
        allowed = max(0, NOTEBOOK_SOURCE_CAP - 1 - unmanaged)
        items = sorted(desired.items())
        for rel, title in items[allowed:]:
            print(f"[{key}] EXCESS {title} (occupancy {projected} exceeds "
                  f"cap {NOTEBOOK_SOURCE_CAP}; cannot project)")
        desired = dict(items[:allowed])
        print(f"[{key}] OVER CAP: projecting the deterministic in-cap prefix "
              f"({allowed} of {len(items)} members; charter + {unmanaged} "
              f"unmanaged occupy the rest)")
    elif headroom <= CAP_WARN_HEADROOM:
        print(f"[{key}] WARN headroom {headroom}: occupancy {projected} of "
              f"cap {NOTEBOOK_SOURCE_CAP}. No successor split is defined for "
              f"this book — the owed remedy is an OpenSpec delta to "
              f"lifecycle-notebook-projection defining its split")

    # charter
    if CHARTER_TITLE not in by_title:
        print(f"[{key}] ADD  {CHARTER_TITLE}")
        if apply and nid:
            nlm("source", "add", handle, "--text", CHARTER, "--title", CHARTER_TITLE, parse=False)
            time.sleep(2)

    wanted_titles = set(desired.values()) | {CHARTER_TITLE}
    # deletions: our managed prefixes only; unwanted titles lose every copy,
    # wanted-but-duplicated titles keep one
    for title, sids in by_title.items():
        managed = title.startswith("[") or title == CHARTER_TITLE
        if not managed:
            continue
        doomed = sids if title not in wanted_titles else sids[1:]
        for sid in doomed:
            print(f"[{key}] DEL  {title}")
            if apply:
                nlm("source", "delete", sid, "--confirm", parse=False)
                time.sleep(2)

    # adds and content updates
    for rel, title in sorted(desired.items()):
        text = (root / rel).read_text(errors="replace")
        digest = hashlib.sha256(text.encode()).hexdigest()[:16]
        prev = mf.get(rel)
        if title in by_title and prev and prev.get("hash") == digest:
            continue
        if title in by_title and (not prev or prev.get("hash") != digest):
            print(f"[{key}] UPD  {title}")
            if apply:
                nlm("source", "delete", by_title[title][0], "--confirm", parse=False)
                time.sleep(2)
        elif title not in by_title:
            print(f"[{key}] ADD  {title}")
        if apply:
            add_text_source(handle, text, title)
            time.sleep(2)
        mf[rel] = {"hash": digest, "title": title}
    return ok, overflowed


# Workbench orphan sweep (openxFactory add-ideation-dashboard, task 4.1
# wiring of the wave-6 note at ideation_dashboard.workbench.orphan_sweep).
# v1 dashboard scope: workbench manifests are gitignored session state under
# the pinned openxFactory checkout, so that is the one live-binding root the
# sweep consults. Manifests found under any OTHER family checkout make the
# sweep skip (never risk deleting a notebook a live manifest still binds).
V1_WORKBENCH_DIR = "openxFactory/ideation/workbench/"


def _out_of_scope_workbench_dirs(root: Path) -> list[Path]:
    """Workbench dirs OUTSIDE the v1 openxFactory sweep scope that could carry
    live manifests: the aggregation root's own and each xFactories/<repo>'s
    (worktree containers excluded, matching scan())."""
    dirs = [root / "ideation" / "workbench"]
    if (root / "xFactories").is_dir():
        for rel in pinned_factory_paths(root):
            dirs.append(root / rel / "ideation" / "workbench")
    return [d for d in dirs if d.is_dir()]


def workbench_orphan_sweep(root: Path, apply: bool, adapter=None) -> None:
    """Sweep orphaned `xf-wb-*` scratch notebooks after a lifecycle sync.

    Calls `ideation_dashboard.workbench.orphan_sweep` over the aggregation
    root with a real NotebookAdapter: a deleted workbench manifest means its
    bound scratch notebook is removed on the next `--apply` run. Without
    `--apply` this only PRINTS the sweep plan (verbs SWEEP/KEEP — deliberately
    not ADD/DEL/UPD, which doc-health's notebook-projection-drift family
    counts as pending projection operations).

    Safety, by construction: candidates come solely from
    `NotebookAdapter.list_scratch_result()`, which filters titles on the `xf-wb-`
    prefix — the lifecycle books (xf-ideation-<repo>/xf-drafts/xf-canon) and
    every other notebook are not candidates and can never be swept. Degrades
    gracefully: an unavailable nlm, an import failure, out-of-scope manifests, or
    a notebook list that could not be READ all SKIP with a notice, never raise —
    and a list that could not be read is never reported as an account with
    nothing in it, on either the dry-run or the `--apply` half (PR #49 review
    finding 13)."""
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    try:
        from ideation_dashboard import workbench as wb
    except Exception as exc:  # sweep is additive; never break the sync
        print(f"[workbench] orphan sweep SKIPPED (ideation_dashboard "
              f"unavailable: {exc})")
        return
    root = Path(root).resolve()
    adapter = adapter or wb.NotebookAdapter()
    if not adapter.available():
        print("[workbench] orphan sweep SKIPPED (nlm unavailable)")
        return
    strays = [d for d in _out_of_scope_workbench_dirs(root)
              if any(d.glob("*.workbench.yaml"))]
    if strays:
        rels = ", ".join(str(d.relative_to(root)) for d in strays)
        print(f"[workbench] orphan sweep SKIPPED (manifests outside the v1 "
              f"openxFactory scope: {rels}; extend the sweep scope before "
              "enabling)")
        return
    if not apply:
        live = wb.live_notebook_aliases(root, workbench_dir=V1_WORKBENCH_DIR)
        pending = 0
        # AN ERRORED LISTING IS NOT AN EMPTY ONE (PR #49 review finding 13's
        # residual, wave 2). `list_scratch()` collapses a failed `nlm notebook
        # list` into `[]`, so the DRY RUN over an unreadable account printed
        # absolutely nothing and read as "no orphans pending" — the same
        # absence-of-evidence the finding was filed about, on the one read-only
        # path the wave-1 fix's four callers did not cover. `--apply` already says
        # it (`workbench.orphan_sweep` gates on `NotebookListing.ok`), so the two
        # halves of one command now agree.
        listing = adapter.list_scratch_result()
        if not listing.ok:
            print(f"[workbench] orphan sweep plan UNAVAILABLE (the notebook list "
                  f"could not be read, so nothing is known about orphans — this "
                  f"is NOT an empty account: {listing.detail})")
            return
        for nb in listing.rows:
            title = wb._notebook_title(nb)
            if not title:
                continue
            if title in live:
                print(f"[workbench] KEEP  {title} (bound by a live manifest)")
            else:
                pending += 1
                print(f"[workbench] SWEEP {title} (orphan; removed on --apply)")
        if pending:
            print(f"[workbench] dry-run: {pending} orphan(s) pending; "
                  "re-run with --apply to sweep")
        return
    result = wb.orphan_sweep(root, adapter, workbench_dir=V1_WORKBENCH_DIR)
    if result.skipped:
        print(f"[workbench] orphan sweep SKIPPED ({result.detail})")
        return
    print(f"[workbench] {result.detail}; "
          f"deleted={result.deleted or []} kept={result.kept or []}")


# --------------------------------------------------------------------------
# BRANCH-SESSION notebooks (007-workbench-branch-sessions T073; FR-036-FR-040)
#
# A fourth notebook family beside the lifecycle books and the swept
# `xf-wb-*` reference sets: ONE `xf-session-<repository>-<branch>` notebook per
# live branch session, synced FROM that session's WORKTREE.
#
# Three properties this mode must never lose:
#
#   * the books stay MAIN-ONLY (FR-039). `scan()`'s worktree exclusion is NOT
#     relaxed for them — a session worktree lives in `<repo>-worktrees/`, which
#     is neither `openxFactory` nor a pinned `xFactories/<repo>`, so it is
#     outside every book's walk by construction and this mode reads it through a
#     SEPARATE source set (`session_source_set`).
#   * a session leaves NO manifest (D10). The notebook itself is the diff store
#     (title + content hash, via `workbench.project_documents`), so nothing here
#     writes into `ideation/workbench/` — a per-session manifest directory would
#     trip `_out_of_scope_workbench_dirs` and SILENTLY DISABLE the orphan sweep
#     (research R8's trap).
#   * the namespaces stay disjoint (FR-038, D11). `xf-session-` aliases come from
#     `branch_session.notebook_alias` and are never re-spelled here; the sweep
#     only ever sees `xf-wb-*`.
#
# Output verbs are SYNC / RETIRE / KEEP / SKIPPED — deliberately not ADD/DEL/UPD,
# which doc-health's notebook-projection-drift family counts as pending
# LIFECYCLE-BOOK projection operations (same reasoning as the sweep's verbs).
# --------------------------------------------------------------------------

SESSION_CONTAINER_SUFFIX = "-worktrees"


class SessionNotebookRefused(SystemExit):
    """A session notebook operation that cannot be performed honestly: no live
    worktree for the branch, or a branch live in more than one repository. A
    `SystemExit` subclass so the CLI exits non-zero with the reason verbatim."""


@dataclass(frozen=True)
class SessionTarget:
    """The (repository, branch) session a notebook belongs to, plus the worktree
    its sources come from, the CHECKOUT that owns that worktree, and the alias
    derived from the pair.

    `checkout` is carried rather than re-derived from the worktree path: it is the
    SERVED root `SessionGit` guards against (FR-004), and inferring it by walking
    up out of `<repo>-worktrees/sessions/<flattened>` would be a second spelling of
    a layout the dashboard already owns."""
    repository: str
    branch: str
    worktree: Path
    alias: str
    checkout: Path | None = None


@dataclass(frozen=True)
class SessionSync:
    """What one session-notebook run did (or planned, when `applied` is False)."""
    target: SessionTarget
    documents: tuple[str, ...] = ()
    applied: bool = False
    retired: bool = False
    skipped: bool = False
    detail: str = ""

    @property
    def alias(self) -> str:
        return self.target.alias

    @property
    def repository(self) -> str:
        return self.target.repository

    @property
    def branch(self) -> str:
        return self.target.branch

    @property
    def worktree(self) -> Path:
        return self.target.worktree


def _dashboard_module(name: str):
    """Import one `ideation_dashboard` module, with `scripts/` on the path — the
    same lazy pattern `workbench_orphan_sweep` uses."""
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from importlib import import_module

    return import_module(f"ideation_dashboard.{name}")


def session_repositories(root: Path) -> list[tuple[str, Path]]:
    """(repository, checkout) pairs a session worktree can belong to: the
    openxFactory checkout plus every PINNED factory — deliberately the same repo
    set `scan()` walks, so the books and the sessions agree on what a repository
    is (and neither treats a worktree container as one)."""
    pairs = [("openxFactory", root / "openxFactory")]
    for rel in pinned_factory_paths(root):
        pairs.append((Path(rel).name, root / rel))
    return [(name, path) for name, path in pairs if path.is_dir()]


def live_session_targets(root: Path, branch: str,
                         repository: str | None = None) -> list[SessionTarget]:
    """Every LIVE session on `branch`, across the repository set.

    LIVENESS IS THE JOINT SIGNAL, not a directory (PR #49 review finding 12).
    This used to test `worktree.is_dir()` and nothing else, so against crash
    residue whose git association had been pruned AND whose branch had been
    deleted it still returned a target — and then drove notebook create /
    re-sync / RETIRE against a session that did not exist. Handed the identical
    directory, `branch_session.bootstrap_sessions` answered `live=()` and
    reported it stale: two liveness answers for one input, and the divergent one was the
    one holding the `nlm` credential. `branch_session.live_session_worktree` is
    the bootstrap's own per-branch rule — git must list the directory as a
    worktree ON THIS BRANCH, the branch must exist, and no ending marker may say
    the session is over (FR-008, FR-021, D10).

    THE CONTAINER QUESTION got the sweep's own fix (F3, migration evidence
    2026-08-24): a session's container is `<checkout>-worktrees/sessions/`,
    keyed on the checkout the session was OPENED from, and sessions are
    routinely opened from a FEATURE worktree. Asking only each repository's
    canonical checkout derived one path and never saw those sessions —
    `--session-ref` refused two LIVE draft/* branches while `--session-sweep`
    (which enumerates every worktree) saw both, leaving their notebooks hosted
    on the account being abandoned. So this enumeration is complete the same
    way the sweep's is: every worktree git lists for the repository is asked,
    each as a potential container owner, through the SAME joint signal. An
    unreadable worktree list still degrades to the canonical root alone —
    safe here because this mode only ever REFUSES when it finds nothing; it
    has no retire arm."""
    bs = _dashboard_module("branch_session")
    sg = _dashboard_module("session_git")
    root = Path(root).resolve()
    found: list[SessionTarget] = []
    for name, checkout in session_repositories(root):
        if repository and name != repository:
            continue
        roots: list[Path] = [Path(checkout)]
        try:
            for record in sg.SessionGit(checkout).worktree_records():
                candidate = Path(record.path)
                if candidate not in roots:
                    roots.append(candidate)
        except Exception:  # noqa: BLE001 - a tree with no git has no sessions
            pass
        for checkout_root in roots:
            try:
                worktree = bs.live_session_worktree(sg.SessionGit(checkout_root),
                                                    checkout_root, branch)
            except Exception:  # noqa: BLE001 - a tree with no git has no sessions
                worktree = None
            if worktree is not None:
                found.append(SessionTarget(repository=name, branch=branch,
                                           worktree=worktree,
                                           alias=bs.notebook_alias(name, branch),
                                           checkout=checkout))
    return found


def resolve_session_target(root: Path, branch: str,
                           repository: str | None = None) -> SessionTarget:
    """Resolve `branch` to the ONE live session worktree it names.

    The worktree path and the alias are both the dashboard's own derivations
    (`branch_session.worktree_path` / `notebook_alias`) — never re-spelled here,
    which is what keeps this mode and the session lifecycle from disagreeing
    about which notebook belongs to which branch (FR-037, D11).

    A branch with no live worktree is REFUSED rather than invented: a session
    notebook exists only while its session does, and liveness is the JOINT
    worktree+branch signal (see `live_session_targets`). A branch live in two
    repositories is refused NAMING BOTH — the alias is keyed on (repository,
    branch) precisely because that case is real (spec C9) — and
    `--session-repository` is the tie-break."""
    found = live_session_targets(root, branch, repository)
    if not found:
        named = f" in repository {repository!r}" if repository else ""
        raise SessionNotebookRefused(
            f"[session] no live session worktree for branch {branch!r}{named} "
            f"under {Path(root).resolve()}: a session notebook is bound to a LIVE "
            "session, and liveness is the JOINT worktree+branch signal — a "
            "directory alone is crash residue or an ended session, never a "
            "session (FR-036, FR-008, D10). Nothing here creates, re-syncs, or "
            "retires it")
    if len(found) > 1:
        names = ", ".join(t.repository for t in found)
        paths = ", ".join(str(t.worktree) for t in found)
        if len({t.repository for t in found}) > 1:
            advice = (f"; a session notebook alias is keyed on "
                      "(repository, branch) (FR-037, spec C9), so name one "
                      "with --session-repository")
        else:
            advice = ("; the same branch is live under more than one session "
                      "container IN this repository, which no alias can "
                      "disambiguate — end or clean up all but one before "
                      "addressing its notebook")
        raise SessionNotebookRefused(
            f"[session] branch {branch!r} names a live session in more than "
            f"one place ({names}: {paths}){advice}")
    return found[0]


def session_target_for_alias(root: Path, notebook: str) -> SessionTarget | None:
    """The LIVE session whose notebook alias IS `notebook`, or None when the
    argument is not a session alias at all (PR #49 review finding 12).

    Resolved FORWARD — every live session's own `notebook_alias(repository,
    branch)` is computed and compared — rather than by inverting the alias, which
    is lossy (FR-037's transform strips `draft/` and lowercases). A collision
    between two live sessions is REFUSED naming both instead of silently picking
    one: two sessions sharing an alias is the FR-037 hazard, and an import that
    guessed between them would write one session's notebook into the other's
    worktree."""
    bs = _dashboard_module("branch_session")
    sg = _dashboard_module("session_git")
    alias = str(notebook or "").strip()
    if not alias.startswith(bs.NOTEBOOK_PREFIX):
        return None
    root = Path(root).resolve()
    matches: list[SessionTarget] = []
    for name, checkout in session_repositories(root):
        # git's own worktree records, then the SAME joint-signal predicate the
        # bootstrap applies per directory. Deliberately not the bootstrap itself:
        # this is a READ, and the bootstrap registers entries and can regenerate
        # session snapshots — side effects an import must not have merely to work
        # out which notebook it was handed.
        try:
            git = sg.SessionGit(checkout)
            records = git.worktree_records()
        except Exception:  # noqa: BLE001 - a tree with no git has no sessions
            continue
        for record in records:
            branch = record.branch
            if not branch or bs.notebook_alias(name, branch) != alias:
                continue
            worktree = bs.live_session_worktree(git, checkout, branch)
            if worktree is not None:
                matches.append(SessionTarget(
                    repository=name, branch=branch, worktree=worktree,
                    alias=alias, checkout=checkout))
    if len(matches) > 1:
        names = ", ".join(f"{t.repository}@{t.branch}" for t in matches)
        raise SessionNotebookRefused(
            f"[session] the notebook alias {alias!r} resolves to MORE THAN ONE "
            f"live session ({names}); FR-037 says two live sessions can never "
            "share an alias, so this is a collision and an import cannot choose "
            "between them — end one of the sessions first")
    if not matches:
        raise SessionNotebookRefused(
            f"[session] {alias!r} is an `xf-session-*` notebook but no LIVE branch "
            f"session under {root} owns it: liveness is the JOINT worktree+branch "
            "signal (FR-008, D10), so a session whose worktree is gone, whose "
            "branch is gone, or whose ending left residue owns nothing. An import "
            "into a dead session's directory would write governed content nothing "
            "can ever merge")
    return matches[0]


def bind_session_import(root: Path, notebook: str, target: ImportTarget
                        ) -> SessionTarget | None:
    """Refuse an import whose notebook and destination are not the SAME session
    (FR-041; PR #49 review finding 12).

    `import_new_sources` took the notebook alias and `--target-path` as two
    INDEPENDENT human-typed strings and cross-checked nothing: `target_from_path`
    validated only workspace containment plus an ideation/supporting-docs shape.
    Pointing a session alias at the ORDINARY import spelling — one path segment
    shorter, the single most likely human slip — landed an unmerged session's
    notebook synthesis in the SERVED MAIN checkout (breaching FR-004's "no session
    operation may move the served checkout" and FR-039's main-only books, since
    `scan()` then picks the file up as a lifecycle-book source); pointing it at
    ANOTHER session's worktree wrote session A's content onto session B's branch.

    Both directions are refused. A session notebook requires a destination inside
    THAT session's worktree; a session-worktree destination requires the session's
    OWN notebook. Returns the bound target, or None when neither side is a
    session (the ordinary main-side import, untouched)."""
    session = session_target_for_alias(root, notebook)
    inside = _session_worktree_of(root, target.path)
    if session is None:
        if inside is None:
            return None
        raise SessionNotebookRefused(
            f"[session] --target-path resolves inside the session worktree "
            f"{inside} but {notebook!r} is not that session's notebook: a session "
            f"worktree holds ONE session's unmerged work, and importing another "
            f"notebook's sources into it would put content nobody projected from "
            f"this branch onto this branch (FR-041). Use "
            f"{_dashboard_module('branch_session').NOTEBOOK_PREFIX}… for this "
            "session, or a target outside the worktree")
    if inside is None or Path(inside).resolve() != Path(session.worktree).resolve():
        raise SessionNotebookRefused(
            f"[session] {notebook!r} is the notebook of the live session on "
            f"{session.branch!r}, whose worktree is {session.worktree} — but "
            f"--target-path resolves to {target.path}, which is not inside it. "
            "FR-041 requires a session import to write into the origin folder "
            "INSIDE the session worktree: a target outside it puts one session's "
            "unmerged synthesis into the served checkout (FR-004) or into another "
            "session's branch. Nothing was written")
    return session


def _session_worktree_of(root: Path, path: Path) -> Path | None:
    """The session worktree `path` sits inside, or None. Derived from the
    dashboard's own container layout (`<repo>-worktrees/sessions/<flattened>`),
    never re-spelled."""
    bs = _dashboard_module("branch_session")
    resolved = Path(path).resolve()
    for _name, checkout in session_repositories(Path(root).resolve()):
        sessions = bs.sessions_root(checkout)
        try:
            if sessions.resolve() not in resolved.parents:
                continue
        except OSError:                              # pragma: no cover - defensive
            continue
        relative = resolved.relative_to(sessions.resolve())
        return sessions / relative.parts[0]
    return None


def session_source_set(target: SessionTarget) -> list[tuple[str, str]]:
    """The session notebook's desired sources, read FROM the worktree. Delegates
    to `workbench.session_documents` so create-at-open (the dashboard) and this
    re-sync project exactly ONE membership rule."""
    wb = _dashboard_module("workbench")
    return wb.session_documents(target.worktree, repository=target.repository)


def sync_session_notebook(root: Path, branch: str, apply: bool = False, *,
                          repository: str | None = None, adapter=None,
                          retire: bool = False) -> SessionSync:
    """Create / re-sync / retire ONE `xf-session-*` notebook (FR-036, FR-040).

    Dry-run by default like every other mode here: without `--apply` this only
    PRINTS the plan. Degrades rather than raising on an absent `nlm` — a notebook
    is never what a session depends on (FR-042)."""
    target = resolve_session_target(root, branch, repository)
    wb = _dashboard_module("workbench")
    adapter = adapter if adapter is not None else wb.NotebookAdapter()
    rel = display_path(target.worktree, Path(root).resolve())
    if not adapter.available():
        print(f"[session] {target.alias} SKIPPED (nlm unavailable)")
        return SessionSync(target=target, skipped=True,
                           detail="nlm unavailable — notebook action skipped, "
                                  "not blocked")
    if retire:
        print(f"[session] RETIRE {target.alias} (the session is over; the "
              "notebook is not re-pointed at main)")
        if not apply:
            print("[session] dry-run: re-run with --apply to retire")
            return SessionSync(target=target, detail="retire planned")
        result = adapter.retire(target.alias)
        print(f"[session] {target.alias}: {result.detail}")
        return SessionSync(target=target, applied=True,
                           retired=bool(result.ok and not result.skipped),
                           skipped=bool(result.skipped), detail=result.detail)

    documents = session_source_set(target)
    paths = tuple(path for path, _text in documents)
    print(f"[session] SYNC {target.alias} <- {len(paths)} worktree source(s) "
          f"({rel})")
    for path in paths:
        print(f"[session]   source {path}")
    # ---- capacity guard (before any mutation) ----
    # This route is deliberately unbounded (workbench finding 21: the
    # human-waiting terminal completes what a bounded gate-route creation
    # deferred), so nothing downstream would stop a session whose derived
    # corpus outgrew the provider's per-notebook cap — adds would fail past
    # the cap mid-flight, the shared Ideation book's 2026-08-10 death. The
    # books' guard therefore applies here too: refuse before ANY mutation,
    # name the excess and the remedy.
    if len(paths) > NOTEBOOK_SOURCE_CAP:
        print(f"[session] {target.alias} REFUSED: {len(paths)} desired sources "
              f"exceed the provider's {NOTEBOOK_SOURCE_CAP}-source per-notebook "
              f"cap by {len(paths) - NOTEBOOK_SOURCE_CAP}. Applying would die "
              "mid-run; scope the session membership rule down or split the "
              "projection first (see split-ideation-book-per-repo). Nothing "
              "was created, added, or retired.")
        return SessionSync(target=target, documents=paths, skipped=True,
                           detail=f"{len(paths)} desired sources exceed the "
                                  f"{NOTEBOOK_SOURCE_CAP}-source provider cap")
    if not apply:
        print("[session] dry-run: re-run with --apply to sync")
        return SessionSync(target=target, documents=paths,
                           detail="sync planned")
    result = wb.project_documents(adapter, target.alias, documents)
    print(f"[session] {target.alias}: {result.detail}")
    return SessionSync(target=target, documents=paths, applied=True,
                       skipped=bool(result.skipped), detail=result.detail)


# ---------------------------------------------------------------------------
# SESSION-NAMESPACE RECONCILIATION (add-session-notebook-reconciliation)
#
# A session notebook is bound to a LIVE session, and the two governed endings
# retire it. Sessions also end a THIRD way: a probe or a crash-residue cleanup
# removes a worktree and a branch directly, no abandon runs, and the notebook
# survives on an account shared across the family. `--session-ref
# --session-retire` cannot clean that up — it resolves liveness first and refuses
# a dead branch, correctly, because that refusal is what stops this script
# inventing a session and retiring a LIVE one's notebook. So the dead case gets
# its own door, and it establishes death differently: not from a caller's
# assertion about one branch, but from no live session anywhere claiming the
# notebook.
# ---------------------------------------------------------------------------

# The session namespace's prefix, spelled ONCE and taken from the module that
# owns it rather than re-typed: `workbench.SESSION_NOTEBOOK_PREFIX` is what the
# adapter's own listing and prefix guards use.
SESSION_ALIAS_PREFIX = "xf-session-"

SESSION_LIVE = "live"
SESSION_DEAD = "dead"
SESSION_FOREIGN = "out-of-scope"


class SessionSweepRefused(RuntimeError):
    """The reconciliation refused: it could not account for every repository."""


def live_session_aliases(root: Path, adapter_repositories=None
                         ) -> tuple[set[str], list[str]]:
    """`(aliases, errors)` — every LIVE session's own notebook alias across this
    workspace's session repositories.

    FORWARD ONLY. `notebook_alias` is injective but NOT invertible: the readable
    half strips `draft/` and lowercases, and the key half is a digest. So a
    notebook title can never be resolved back to a `(repository, branch)` pair,
    and the only sound comparison is to compute what every live session's alias
    WOULD be and look for the title in that set.

    Errors are returned beside the aliases because the caller must fail closed on
    them: a repository this run could not enumerate yields fewer aliases, and
    fewer aliases is indistinguishable from sessions having ended."""
    bs = _dashboard_module("branch_session")
    sg = _dashboard_module("session_git")
    aliases: set[str] = set()
    errors: list[str] = []
    for name, checkout in (adapter_repositories
                           if adapter_repositories is not None
                           else session_repositories(root)):
        # EVERY WORKTREE OF THE REPOSITORY, not just its canonical checkout.
        # Caught by the live dry run this change owed, and it was the dangerous
        # direction: a session's container is `<checkout>-worktrees/sessions/`,
        # keyed on the checkout it was OPENED from, and sessions are routinely
        # opened from a FEATURE worktree. Asking only the canonical checkout
        # found no sessions there — a legitimate answer for that checkout, so
        # fail-closed never fired — and the run declared two LIVE sessions dead,
        # both holding unmerged work. `git worktree list` from the canonical
        # checkout knows every linked worktree (they share one git dir), so the
        # enumeration is completable; failing to read it is an ERROR, not an
        # answer.
        roots: list[Path] = [Path(checkout)]
        try:
            for record in sg.SessionGit(checkout).worktree_records():
                path = Path(record.path)
                if path not in roots:
                    roots.append(path)
        except Exception as exc:  # noqa: BLE001 - unreadable worktree list
            errors.append(f"{name}: could not enumerate worktrees: {exc}")
            continue
        for checkout_root in roots:
            try:
                branches, listing_errors = bs.live_session_branches_of(
                    sg.SessionGit(checkout_root), checkout_root)
            except Exception as exc:  # noqa: BLE001 - a tree with no git is an ERROR here
                # …and NOT a checkout with no sessions. `live_session_targets`
                # may treat a failure as "no target" because it is asked about
                # one named branch; a sweep asked "which are live" must never
                # read a failure as an answer.
                errors.append(f"{name} [{checkout_root}]: {exc}")
                continue
            for detail in listing_errors:
                errors.append(f"{name} [{checkout_root}]: {detail}")
            for branch in branches:
                try:
                    aliases.add(bs.notebook_alias(name, branch))
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{name} {branch}: {exc}")
    return aliases, errors


def session_repository_slugs(pairs) -> list[str]:
    """The lowercased repository segment each in-scope alias must open with.

    Derived from the SAME repository set the sessions and the books agree on, so
    a notebook belonging to another workspace's repositories is recognisable
    without this run guessing at title structure."""
    return [str(name).lower() for name, _checkout in pairs]


def classify_session_notebooks(titles, live_aliases, slugs
                               ) -> list[tuple[str, str]]:
    """`[(title, verdict)]` over `xf-session-` titles — pure, node of the sweep.

    Three verdicts and no fourth: `live` (the title IS a live session's alias),
    `out-of-scope` (its repository segment is not one this workspace carries, so
    it is another workspace's session and not this run's to judge), and `dead`.

    Scope is tested by PREFIX (`xf-session-<slug>-`), never by splitting the
    title on `-`: repository names and flattened branches both contain hyphens,
    so any parse would be ambiguous exactly where being wrong deletes someone
    else's notebook. A title that is not a session title at all is not
    classified — it never enters this function's answer."""
    prefixes = [f"{SESSION_ALIAS_PREFIX}{slug}-" for slug in slugs]
    out: list[tuple[str, str]] = []
    for title in titles:
        name = str(title or "")
        if not name.startswith(SESSION_ALIAS_PREFIX):
            continue
        if name in live_aliases:
            out.append((name, SESSION_LIVE))
        elif any(name.startswith(p) for p in prefixes):
            out.append((name, SESSION_DEAD))
        else:
            out.append((name, SESSION_FOREIGN))
    return out


def session_notebook_sweep(root: Path, apply: bool, adapter=None) -> int:
    """Reconcile the `xf-session-` namespace against live sessions.

    Returns a process exit code: 0 when the account and the workspace agree (or
    a report ran), nonzero when the run REFUSED. Refusal, never a partial act, is
    the whole posture — see `live_session_aliases`."""
    root = Path(root).resolve()
    pairs = session_repositories(root)
    aliases, errors = live_session_aliases(root, pairs)
    if errors:
        print("[session-sweep] REFUSED: this run could not account for every "
              "session repository, and a repository it cannot enumerate looks "
              "exactly like one whose sessions have ended. Nothing was retired.")
        for detail in errors:
            print(f"[session-sweep]   unaccounted: {detail}")
        return 1
    if adapter is None:
        wb = _dashboard_module("workbench")
        adapter = wb.NotebookAdapter()
    listing = adapter.list_sessions_result()
    if not listing.ok:
        print("[session-sweep] REFUSED: the notebook list could not be read, so "
              "nothing is known about session notebooks — this is NOT an empty "
              f"account: {listing.detail}")
        return 1
    wb = _dashboard_module("workbench")
    rows = {}
    for nb in listing.rows:
        title = wb._notebook_title(nb)
        if title:
            rows[title] = nb
    verdicts = classify_session_notebooks(rows, aliases,
                                          session_repository_slugs(pairs))
    dead = [t for t, v in verdicts if v == SESSION_DEAD]
    for title, verdict in verdicts:
        if verdict == SESSION_LIVE:
            print(f"[session-sweep] KEEP   {title} (a live session claims it)")
        elif verdict == SESSION_FOREIGN:
            print(f"[session-sweep] SKIP   {title} (names a repository this "
                  "workspace does not carry)")
        else:
            count = _session_source_count(rows[title])
            discards = "" if count is None else f"; retiring discards {count} source(s)"
            print(f"[session-sweep] {'RETIRE' if apply else 'DEAD  '} {title} "
                  f"(no live session claims it{discards})")
    if not dead:
        print(f"[session-sweep] {len(aliases)} live session(s); no orphans")
        return 0
    if not apply:
        print(f"[session-sweep] dry-run: {len(dead)} orphan(s) pending; "
              "re-run with --apply to retire")
        return 0
    if not hasattr(adapter, "retire"):
        print("[session-sweep] REFUSED: this adapter exposes no session `retire` "
              "operation, and a scratch delete is not interchangeable with it "
              "(no session-prefix guard). Nothing was retired.")
        return 1
    failures = 0
    for title in dead:
        # `retire` — the SAME operation both governed endings take, with its own
        # session-prefix guard. The title is the ACCOUNT'S own, taken from the
        # listing rather than built here, which is the property
        # `retire_session_notebook`'s key-derived title provides for a live
        # session: this run can only name notebooks that exist and that no live
        # session claims.
        result = adapter.retire(title)
        ok = getattr(result, "ok", False)
        print(f"[session-sweep] {'retired' if ok else 'FAILED '} {title}: "
              f"{getattr(result, 'detail', '')}")
        if not ok:
            failures += 1
    return 1 if failures else 0


def _session_source_count(row) -> int | None:
    """The notebook's source count when the listing carries one — reported so a
    retirement that would discard hand-added sources is visible BEFORE it runs."""
    if isinstance(row, dict):
        for key in ("source_count", "sources", "sourceCount"):
            value = row.get(key)
            if isinstance(value, int):
                return value
    return None


# --------------------------- the declared hosting identity ---------------------------
# add-notebook-projection-identity (ratified 2026-08-23). WHICH Google account
# the projection is created in is contract conformance, not a property of
# whoever ran `nlm login` first.

HOSTING_REL = "openxFactory/examples/notebook-projection-hosting.yaml"
_HOSTING_SCALARS = ("case", "account", "account_type", "domain",
                    "nlm_profile")
_HOSTING_MIGRATION_SCALARS = ("state", "from_account", "from_nlm_profile")


NLM_CONFIG = Path.home() / ".notebooklm-mcp-cli" / "config.toml"
# Set once the run is bound; re-asserted before EVERY CLI invocation, because
# the CLI's profile selection is process-global and any other terminal can
# `nlm login switch` mid-run. A single check before a 40-minute apply binds
# nothing.
_BOUND_PROFILE: str | None = None
_CONFIG_CACHE: tuple[tuple[int, int], str | None] | None = None


def configured_nlm_profile(path: Path | None = None) -> str | None:
    """`auth.default_profile` as it stands ON DISK right now.

    Read from the config FILE rather than by shelling out: this runs before
    every invocation, so it must cost a stat, not a subprocess. The parse is
    cached on (mtime_ns, size) and redone only when the file actually moves.
    """
    global _CONFIG_CACHE
    path = path or NLM_CONFIG
    try:
        stat = path.stat()
    except OSError:
        return None
    stamp = (stat.st_mtime_ns, stat.st_size)
    if _CONFIG_CACHE is not None and _CONFIG_CACHE[0] == stamp:
        return _CONFIG_CACHE[1]
    profile = None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    section = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            continue
        if section == "auth":
            key, sep, value = line.partition("=")
            if sep and key.strip() == "default_profile":
                profile = value.strip().strip('"').strip("'") or None
                break
    _CONFIG_CACHE = (stamp, profile)
    return profile


def profile_account(profile: str, home: Path | None = None) -> str | None:
    """The Google address the CLI recorded for `profile`, when it has one.

    Corrects a claim this change shipped with: the CLI DOES store an email, in
    `profiles/<name>/metadata.json`. It is populated by a recent login and left
    null by an older one, so a None here means UNKNOWN — not "no such thing" —
    and an unknown address is reported rather than treated as a mismatch.
    """
    base = home or (Path.home() / ".notebooklm-mcp-cli")
    path = base / "profiles" / profile / "metadata.json"
    try:
        meta = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    email = meta.get("email") if isinstance(meta, dict) else None
    return email.strip() or None if isinstance(email, str) else None


def bind_profile(profile: str | None) -> None:
    """Pin the run to `profile`; None releases the pin (undeclared installs)."""
    global _BOUND_PROFILE
    _BOUND_PROFILE = profile


def assert_still_bound() -> None:
    """Refuse the invocation if the CLI's profile drifted out from under us.

    The window this closes is real and was found in review: another terminal
    running `nlm login switch` after the run's opening check would silently
    redirect every later add and delete into a different Google account. The
    declaration exists to make that impossible, so the run dies here rather
    than writing one more source into an account nobody declared.
    """
    if _BOUND_PROFILE is None:
        return
    active = configured_nlm_profile()
    if active == _BOUND_PROFILE:
        return
    raise SystemExit(
        f"hosting: the CLI's active profile changed mid-run — bound to "
        f"{_BOUND_PROFILE!r}, now {active!r}. Refusing every further "
        f"invocation: the remaining work would land in an account this "
        f"install has not declared. Re-bind with "
        f"`nlm login switch {_BOUND_PROFILE}` and re-run; the sync is "
        f"idempotent, so a resumed run is a no-op over what finished.")


def read_hosting_declaration(root: Path) -> dict[str, str] | None:
    """The install's declared hosting identity, or None when undeclared.

    Deliberately a NARROW SCALAR READER rather than a YAML parse: this script
    carries no YAML dependency (the workspace registry beside it is handled as
    text for the same reason), and the full shape — required fields, the
    two-case vocabulary, the roster's key — is enforced by
    `scripts/validate-notebook-projection-hosting.py`. Only the `hosting:`
    block's own scalars and its `migration:` sub-block are read here, which is
    all the sync needs to bind a run to an account.
    """
    path = root / HOSTING_REL
    if not path.is_file():
        return None          # genuinely undeclared: the only undeclared case
    found: dict[str, str] = {}
    in_hosting = in_migration = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            in_hosting = line.strip() == "hosting:"
            in_migration = False
            continue
        if not in_hosting:
            continue
        key, sep, value = line.strip().partition(":")
        value = value.strip().strip('"').strip("'")
        if indent == 2:
            in_migration = (key == "migration" and not value)
            if sep and key in _HOSTING_SCALARS:
                found[key] = value
        elif indent == 4 and in_migration and key in _HOSTING_MIGRATION_SCALARS:
            found[f"migration_{key}"] = value
    # An EXISTING file always yields a dict — empty when this narrow reader
    # could not make sense of it (flow style, other indentation, tabs).
    # Returning None there would route a present-but-unparsed declaration into
    # the UNDECLARED branch: the sync would bind nothing and run unbound for the
    # whole job while the full validator passed the very same file. Fail closed.
    return found


def active_nlm_profile(runner=None) -> str | None:
    """The profile the CLI will actually use, or None when it cannot be read.

    The CLI selects a profile PROCESS-GLOBALLY, through `auth.default_profile`:
    of the verbs this sync issues (`notebook`, `source`, `alias`, `tag`,
    `chat`), NONE accepts a per-invocation `--profile`, so the binding is
    VERIFIED rather than passed. Only the newer `share` and `login` verbs take
    the flag.
    """
    if runner is None:
        # ONE source of truth in production: the same config file
        # `assert_still_bound()` re-reads before every invocation. Two readers
        # of one fact can disagree, and this one gates the other.
        return configured_nlm_profile()
    try:
        out = runner("config", "get", "auth.default_profile", parse=False)
    except Exception:  # noqa: BLE001 - an unreadable profile is "unknown"
        return None
    if not isinstance(out, str):
        return None
    return out.strip() or None


# The account shapes a Google USER account never has. A projection host must be
# one: NotebookLM has no API and a service principal cannot drive its consumer
# web UI, so such a declaration could never work.
_NON_USER_MARKERS = (".iam.gserviceaccount.com", ".gserviceaccount.com")


_MIGRATION_STATES = (None, "", "pending", "complete")


def _refuse_unusable_declaration(declared: dict[str, str]) -> None:
    """Enforce the declaration rules that must hold ON THE OPERATIONAL PATH.

    `scripts/validate-notebook-projection-hosting.py` checks the whole record,
    including the roster — but review found it was invoked by nothing the sync
    runs, so a declaration naming a consumer or service account would have been
    accepted by an ordinary `--apply`. These few rules are therefore enforced
    here too, inline and dependency-free; the validator remains the authority
    on the parts a sync never reads.
    """
    if not declared:
        raise SystemExit(
            f"hosting: {HOSTING_REL} EXISTS but no declaration could be read "
            f"from it. The sync reads the `hosting:` block's own two-space "
            f"scalars; flow style, other indentation or tabs parse as valid "
            f"YAML for the validator and as nothing here. Refusing rather than "
            f"running unbound — an unreadable declaration is not an absent "
            f"one. Re-indent it to match "
            f"examples/notebook-projection-hosting.yaml.")
    case = declared.get("case")
    account = declared.get("account", "")
    state = declared.get("migration_state")
    if state not in _MIGRATION_STATES:
        raise SystemExit(
            f"hosting: migration.state is {state!r}; it is 'pending', "
            f"'complete', or absent. An unrecognized state would otherwise "
            f"bind the run to the DECLARED profile while the books are still "
            f"in the previous account — a premature migration under --apply.")
    if state == "pending" and not declared.get("migration_from_nlm_profile"):
        raise SystemExit(
            f"hosting: a PENDING migration must name "
            f"migration.from_nlm_profile — the sync binds there until the "
            f"books move, and cannot bind to a profile nobody named.")
    if not declared.get("nlm_profile"):
        raise SystemExit(
            f"hosting: {HOSTING_REL} names no top-level nlm_profile. It is "
            f"required in every state: it is what the run binds to once a "
            f"migration completes.")
    if case not in ("operator_hosted", "self_hosted"):
        raise SystemExit(
            f"hosting: {HOSTING_REL} declares case {case!r}; an install "
            f"declares exactly one of operator_hosted or self_hosted")
    if "@" not in account:
        raise SystemExit(
            f"hosting: {HOSTING_REL} names no usable account address")
    if any(marker in account for marker in _NON_USER_MARKERS):
        raise SystemExit(
            f"hosting: {account} is a service account. The hosting identity "
            f"MUST be a Google USER account — NotebookLM has no API and a "
            f"service account cannot drive its consumer web UI, so this "
            f"declaration could never work")
    if case != "operator_hosted":
        return
    if declared.get("account_type") != "google_workspace_user":
        raise SystemExit(
            f"hosting: {account} is declared operator-hosted but its "
            f"account_type is {declared.get('account_type')!r}. The "
            f"operator-hosted case requires a google_workspace_user: a "
            f"consumer account keeps a personal recovery path and no admin "
            f"console, which is what this case exists to remove")
    domain = declared.get("domain", "")
    if not domain:
        raise SystemExit(
            f"hosting: an operator-hosted declaration must name the domain "
            f"the operating party administers")
    if not account.lower().endswith("@" + domain.lower()):
        raise SystemExit(
            f"hosting: {account} is not in the declared domain {domain} — "
            f"the operating party must administer the account it declares")


def enforce_hosting_profile(root: Path, *, runner=None) -> dict[str, str] | None:
    """Bind this run to the declared hosting identity, or refuse to run.

    Returns the declaration when the run may proceed, None when the install has
    not declared. Exits when an install HAS declared and the CLI is pointed
    somewhere else: writing a governed projection into an account nobody
    declared is precisely the failure this capability exists to retire, so the
    run fails rather than falling back to the default profile.

    While a declared migration is PENDING the run binds to the account that
    still HOLDS the books (`migration.from_nlm_profile`) and says so, because a
    declaration is not a migration — flipping the binding before the books move
    would break every sync rather than move anything.

    WHAT IS VERIFIED. The profile NAME always, and the ACCOUNT ADDRESS whenever
    the CLI recorded one: `profiles/<name>/metadata.json` carries an `email`,
    populated by a recent login and left null by an older one. A null is
    reported as unknown rather than treated as a match — this change originally
    claimed the CLI stored no email at all, which review disproved.
    """
    declared = read_hosting_declaration(root)
    if declared is None:
        bind_profile(None)
        print("hosting: NO DECLARED HOSTING IDENTITY. This install does not "
              "meet the declared-hosting requirement — a transition state, not "
              "a third legitimate case. Running under the CLI's default "
              "profile; this projection is not governed by a declared account.")
        return None

    _refuse_unusable_declaration(declared)
    account = declared.get("account") or "<unnamed>"
    case = declared.get("case") or "<unstated>"
    target = declared.get("nlm_profile")
    pending = declared.get("migration_state") == "pending"
    profile = declared.get("migration_from_nlm_profile") if pending else target
    holder = declared.get("migration_from_account", "the previous account") if pending else account

    active = active_nlm_profile(runner)
    if active is None:
        raise SystemExit(
            f"hosting: cannot read the CLI's active profile, so this run "
            f"cannot prove which account it would write to. Refusing rather "
            f"than guessing.")
    if active != profile:
        raise SystemExit(
            f"hosting: expected the {profile!r} profile but the CLI's active "
            f"profile is {active!r}. Refusing: a run that cannot prove which "
            f"account it writes to is the failure this declaration exists to "
            f"retire.\n"
            f"  switch it with:   nlm login switch {profile}\n"
            f"  first time:       nlm login --profile {profile}")

    # The profile NAME proves which store is used; the address it recorded, if
    # it recorded one, proves WHICH ACCOUNT that store holds. Check it when
    # available — a name can point anywhere after a re-login.
    expected = holder if pending else account
    signed_in = profile_account(profile)
    if signed_in and expected and signed_in.lower() != expected.lower():
        raise SystemExit(
            f"hosting: profile {profile!r} is signed in as {signed_in}, but "
            f"this install expects {expected}. Refusing: the profile name "
            f"matches and the ACCOUNT does not, which is exactly the mix-up a "
            f"declared identity exists to catch.\n"
            f"  re-authenticate with:  nlm login --profile {profile}  "
            f"(as {expected})")
    if signed_in is None:
        print(f"hosting: profile {profile!r} records no account address "
              f"(an older login leaves it null) — the binding is verified by "
              f"profile NAME only; confirm with `nlm notebook list` that it "
              f"shows {expected}.")

    bind_profile(profile)
    if pending:
        print(f"hosting: MIGRATION PENDING. Declared {case} {account}, but the "
              f"books still live in {holder} under profile {profile!r} "
              f"(verified active). This run reconciles them THERE. See "
              f"docs/notebook-projection-migration-runbook.md.")
    else:
        print(f"hosting: {case} — {account} "
              f"(nlm profile {profile!r}, verified active)")
    return declared


def parity_report(root: Path, *, book: str | None = None,
                  notebooks: list[dict] | None = None) -> int:
    """Prove parity of the live books against THE CORPUS SCAN.

    The scan is the reference on purpose: after a hosting migration the legacy
    books are the artifact whose fidelity is in question, so proving the new
    account against them proves nothing. Reports per-book DOCUMENT-level
    membership plus a union reconciliation, and never mutates — including the
    ALIAS STORE, a single flat file shared across profiles, so registering an
    alias is a cross-account write rather than a local convenience. Returns 0
    when every book in scope matches with nothing pending, 1 otherwise.

    Membership is proven at the DOCUMENT level, not at the title level
    (add-projection-title-uniqueness). Comparing a set of derived titles
    against a set of live titles CANNOT SEE a document that never received a
    title of its own: a collapse leaves the two sets equal, which is why this
    mode reported OK on three books that were missing five documents between
    them. Set equality alone is therefore no longer parity — a derived title
    carrying more than one document is a FAILURE that names them.
    """
    desired, specs = scan(root)
    if book and book not in desired:
        print(f"parity: {book!r} is not a book this scan derives; available: "
              f"{', '.join(sorted(desired))}")
        return 1
    if notebooks is None:
        notebooks = list_notebooks()

    derived_union: set[str] = set()
    live_union: set[str] = set()
    mismatched: list[str] = []

    for key, items in sorted(desired.items()):
        if book and key != book:
            continue
        derived = set(items.values())
        derived_union |= derived
        # DOCUMENT-level check, run on the corpus alone: a title carrying more
        # than one document is a book that cannot hold them all, whatever the
        # provider says.
        carried: dict[str, list[str]] = {}
        for rel, title in items.items():
            carried.setdefault(title, []).append(rel)
        collapsed = {t: sorted(rels) for t, rels in carried.items()
                     if len(rels) > 1}
        if collapsed:
            displaced = sum(len(rels) - 1 for rels in collapsed.values())
            print(f"[{key}] PARITY FAIL: {len(collapsed)} derived title(s) "
                  f"carry more than one document — {len(items)} documents "
                  f"derive only {len(derived)} titles, so {displaced} "
                  f"cannot hold a source of their own")
            for title, rels in sorted(collapsed.items())[:5]:
                print(f"[{key}]   COLLAPSED {title}")
                for rel in rels:
                    print(f"[{key}]     {rel}")
        nid, _ok = resolve_or_create_book(root, specs[key], False, notebooks,
                                          bind_alias=False)
        if nid is None:
            print(f"[{key}] PARITY FAIL: no live notebook titled "
                  f"{specs[key].title!r} ({len(derived)} derived members)")
            mismatched.append(key)
            continue
        rows = nlm("source", "list", nid, "--json")
        rows = rows if isinstance(rows, list) else []
        # managed members are the bracket-titled ones; the charter and any
        # hand-added source are deliberately preserved and not parity subjects
        live = {r.get("title", "") for r in rows
                if str(r.get("title", "")).startswith("[")}
        live_union |= live
        missing, extra = sorted(derived - live), sorted(live - derived)
        if not missing and not extra and not collapsed:
            print(f"[{key}] PARITY OK: {len(items)} documents in "
                  f"{len(derived)} titles match")
            continue
        mismatched.append(key)
        if missing or extra:
            print(f"[{key}] PARITY FAIL: {len(missing)} missing, {len(extra)} "
                  f"extra (derived {len(derived)}, live {len(live)})")
            for title in missing[:5]:
                print(f"[{key}]   MISSING {title}")
            for title in extra[:5]:
                print(f"[{key}]   EXTRA   {title}")

    print(f"parity union: {len(derived_union)} derived titles, "
          f"{len(live_union)} live managed titles, "
          f"{len(derived_union - live_union)} unprojected, "
          f"{len(live_union - derived_union)} unaccounted")
    if mismatched:
        print(f"parity: FAILED for {len(mismatched)} book(s): "
              f"{', '.join(mismatched)} — pending changes remain")
        return 1
    print("parity: PROVEN — every book in scope matches the corpus scan, "
          "0 pending ADD/DEL/UPD")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--parity", action="store_true",
                    help="prove the live books against the CORPUS SCAN "
                         "(per-book title-set equality + a union "
                         "reconciliation); reports, never mutates")
    ap.add_argument("--book", help="sync one book only (a scan-derived key: "
                                   "drafts, canon, or ideation-<repo-slug>)")
    ap.add_argument("--session-ref", metavar="BRANCH",
                    help="create/re-sync the xf-session-* notebook of the live "
                         "branch session on BRANCH, from its worktree")
    ap.add_argument("--session-repository", metavar="REPOSITORY",
                    help="tie-break for --session-ref when the same branch is "
                         "live in more than one repository")
    ap.add_argument("--session-retire", action="store_true",
                    help="with --session-ref: RETIRE the session notebook "
                         "(the session has ended)")
    ap.add_argument("--session-sweep", action="store_true",
                    help="RECONCILE the xf-session-* namespace against live "
                         "sessions: report every session notebook no live "
                         "session claims, and with --apply retire them "
                         "(the door for a session torn down without an abandon)")
    ap.add_argument("--import-exports", metavar="NOTEBOOK",
                    help="import [export:brainstorm]/[export:staged] sources from a hybrid notebook")
    ap.add_argument("--import-new-sources", metavar="NOTEBOOK",
                    help="import all non-seed sources from an analysis notebook")
    ap.add_argument("--target-path",
                    help="origin brainstorm/staging/proposal-support folder for --import-new-sources")
    ap.add_argument("--import-date",
                    default=datetime.now(timezone.utc).date().isoformat(),
                    help="date stamp for imported idea files (YYYY-MM-DD)")
    args = ap.parse_args()

    # Bind the run to the declared hosting identity BEFORE any branch that
    # reaches the CLI — session notebooks and imports are created in the same
    # account as the lifecycle books, so they are bound by the same rule. A run
    # that cannot prove which account it writes to must not write at all.
    enforce_hosting_profile(args.root)

    if args.parity:
        raise SystemExit(parity_report(args.root, book=args.book))

    if args.session_sweep:
        # RECONCILIATION, not a targeted operation. Mutually exclusive with
        # --session-ref by construction: one names a branch it requires to be
        # LIVE, the other starts from titles it cannot invert and asks the
        # workspace which sessions live. Answering both in one run would mean
        # holding two liveness questions at once.
        if args.session_ref:
            ap.error("--session-sweep reconciles the whole session namespace and "
                     "--session-ref names one branch; run them separately")
        raise SystemExit(session_notebook_sweep(args.root, args.apply))
    if args.session_ref:
        # A SESSION run is only ever about one session's notebook: it never syncs
        # a lifecycle book and never runs the orphan sweep, because neither has
        # anything to do with one branch's worktree.
        sync_session_notebook(args.root, args.session_ref, args.apply,
                              repository=args.session_repository,
                              retire=args.session_retire)
        return
    if args.session_retire or args.session_repository:
        ap.error("--session-retire / --session-repository require --session-ref")

    if args.import_exports:
        imported_on = datetime.fromisoformat(args.import_date).date().isoformat()
        import_exported_sources(args.root, args.import_exports, args.apply, imported_on)
        return
    if args.import_new_sources:
        if not args.target_path:
            ap.error("--target-path is required with --import-new-sources")
        imported_on = datetime.fromisoformat(args.import_date).date().isoformat()
        import_new_sources(args.root, args.import_new_sources, args.target_path,
                           args.apply, imported_on)
        return

    manifest_path = args.root / ".claude/nlm-sync-manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    if manifest.pop("ideation", None) is not None:
        print("manifest: dropped the retired shared-ideation key "
              "(split-ideation-book-per-repo)")
    desired, specs = scan(args.root)
    if args.book and args.book not in desired:
        ap.error(f"--book {args.book!r} is not a book this scan derives; "
                 f"available: {', '.join(sorted(desired))}")

    def flush_manifest() -> None:
        # per BOOK, not per run: an interrupted migration must resume as a
        # no-op over the books it finished, never as delete+re-add of
        # everything (split-ideation-book-per-repo)
        manifest_path.parent.mkdir(exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=1))

    notebooks = None
    failures: list[str] = []
    overflows: list[str] = []
    for book, items in desired.items():
        if args.book and book != args.book:
            continue
        print(f"== {book}: {len(items)} desired sources ==")
        try:
            if notebooks is None:
                notebooks = list_notebooks()
            ok, overflowed = sync_book(args.root, specs[book], items, manifest,
                                       args.apply, notebooks=notebooks)
        except Exception as exc:  # noqa: BLE001 - contained per book
            failures.append(book)
            print(f"[{book}] FAILED ({exc}); continuing with the remaining books")
            notebooks = None  # the cached listing may be at fault; refetch
            if args.apply:
                flush_manifest()
            continue
        if overflowed:
            overflows.append(book)
        if not ok:
            failures.append(book)
        if args.apply:
            flush_manifest()
    if args.apply:
        flush_manifest()
        print(f"manifest -> {manifest_path}")

    # Workbench orphan sweep rides the same run (dry-run prints the plan;
    # --apply deletes). Additive: it must never break the lifecycle sync.
    try:
        workbench_orphan_sweep(args.root, args.apply)
    except Exception as exc:
        print(f"[workbench] orphan sweep SKIPPED (unexpected error: {exc})")

    if failures or overflows:
        parts = []
        if overflows:
            parts.append(f"over-cap: {', '.join(overflows)}")
        if failures:
            parts.append(f"failed: {', '.join(failures)}")
        raise SystemExit(f"[sync] nonzero — {'; '.join(parts)} (every other "
                         f"book completed)")


if __name__ == "__main__":
    main()
