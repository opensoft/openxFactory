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
plan. Only `xf-wb-*` titles are ever candidates — the three lifecycle books
above can never be swept.

The --session-ref mode is the fourth family: ONE
`xf-session-<repository>-<branch>` notebook per LIVE branch session
(007-workbench-branch-sessions, FR-036-FR-040), created / re-synced / retired
from that session's WORKTREE. It is deliberately independent of everything
above: the three books stay MAIN-ONLY (a session worktree lives in
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


def scan(root: Path) -> tuple[dict[str, dict[str, str]], dict[str, BookSpec]]:
    """Return ({book_key: {relpath: title}}, {book_key: BookSpec}) desired state.

    Ideation membership is per-repository and STATUS-DERIVED ONLY: an
    ideation book (and therefore its lazy creation) exists exactly when its
    repo has at least one brainstorm/staged document — charter and grounding
    are seeds added to books that exist, never membership that creates one
    (split-ideation-book-per-repo)."""
    desired: dict[str, dict[str, str]] = {b: {} for b in STATIC_BOOKS}
    specs: dict[str, BookSpec] = {b: static_spec(b) for b in STATIC_BOOKS}
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
            repo = rel.parts[0] if rel.parts[0] != "xFactories" else rel.parts[1]
            # ambiguous stems take their parent dir (docs/lifecycle-notebook-projection.md §2)
            stem = f"{f.parent.name}/{f.stem}" if f.stem.lower() == "readme" else f.stem
            title = f"[{status}] {repo}: {stem}"
            if status in IDEATION_STATUSES:
                spec = ideation_spec(repo)
                specs.setdefault(spec.key, spec)
                desired.setdefault(spec.key, {})[str(rel)] = title
            for book, cfg in STATIC_BOOKS.items():
                if status in cfg["statuses"]:
                    desired[book][str(rel)] = title
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
                           notebooks: list[dict] | None = None
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
# A fourth notebook family beside the three lifecycle books and the swept
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
    directory, `branch_session.bootstrap_sessions` answered `live=()` and reported
    it stale: two liveness answers for one input, and the divergent one was the
    one holding the `nlm` credential. `branch_session.live_session_worktree` is
    the bootstrap's own per-branch rule — git must list the directory as a
    worktree ON THIS BRANCH, the branch must exist, and no ending marker may say
    the session is over (FR-008, FR-021, D10)."""
    bs = _dashboard_module("branch_session")
    sg = _dashboard_module("session_git")
    root = Path(root).resolve()
    found: list[SessionTarget] = []
    for name, checkout in session_repositories(root):
        if repository and name != repository:
            continue
        try:
            worktree = bs.live_session_worktree(sg.SessionGit(checkout), checkout,
                                                branch)
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
        raise SessionNotebookRefused(
            f"[session] branch {branch!r} names a live session in more than one "
            f"repository ({names}); a session notebook alias is keyed on "
            "(repository, branch) (FR-037, spec C9), so name one with "
            "--session-repository")
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
    if not apply:
        print("[session] dry-run: re-run with --apply to sync")
        return SessionSync(target=target, documents=paths,
                           detail="sync planned")
    result = wb.project_documents(adapter, target.alias, documents)
    print(f"[session] {target.alias}: {result.detail}")
    return SessionSync(target=target, documents=paths, applied=True,
                       skipped=bool(result.skipped), detail=result.detail)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--apply", action="store_true")
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
