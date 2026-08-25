"""Tests for NotebookLM lifecycle sync and source import helpers.

The `SessionNotebook*` classes at the bottom are Phase 8 of
007-workbench-branch-sessions (T067-T072): the `xf-session-*` notebook that
follows a branch session's WORKTREE. Every one of them drives a STUBBED `nlm`
runner — no test in this file may create a real notebook or invoke the real
`nlm` binary (FR-043).
"""

from __future__ import annotations

import contextlib
import functools
import importlib.util
import io
import itertools
import re
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"

spec = importlib.util.spec_from_file_location("sync_notebooklm_books", SCRIPT)
sync = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = sync
spec.loader.exec_module(sync)

sys.path.insert(0, str(REPO_ROOT / "scripts"))
# adopt-neutral-tooling-home tranche A: the session-notebook halves of this
# suite lean on the `ideation_dashboard` package (branch_session/session_git/
# workbench), which arrives with tranche B. Probed with find_spec because
# `tests/ideation_dashboard/` forms a same-named NAMESPACE package when
# `tests/` is on sys.path (see tests/hermeticity.py `runner_seams`).
# Self-healing: the skip disappears the moment the real package exists.
if importlib.util.find_spec("ideation_dashboard.branch_session") is None:
    raise unittest.SkipTest(
        "ideation_dashboard arrives with adopt-neutral-tooling-home tranche B")
from ideation_dashboard import branch_session as bs   # noqa: E402
from ideation_dashboard import session_git as sg      # noqa: E402
from ideation_dashboard import workbench as wb        # noqa: E402

# doc-health's notebook-projection-drift family counts `[book] ADD|DEL|UPD`
# lines as PENDING lifecycle-book projection operations
# (scripts/doc_health/families.py). Session-mode output must never match it, or a
# live session would read as unprojected canon drift.
SYNC_OP = re.compile(r"^\[[^\]]+\]\s+(ADD|DEL|UPD)\s")

LIFECYCLE_BOOKS = [
    {"id": "b1", "title": "xf-ideation"},
    {"id": "b2", "title": "xf-drafts"},
    {"id": "b3", "title": "xf-canon"},
]

STAGED_DOC = "ideation/staging/demo-topic/README.md"

# The session alias is DERIVED here, never re-spelled: FR-037's readable
# transform is only half of it, and the injective half is a digest of the
# (repository, branch) key (spec C11; PR #49 review finding 11). The exact
# literal derivation is pinned once, in
# `tests/ideation-dashboard/test_branch_session.py`.
SESSION_ALIAS = bs.notebook_alias("openxFactory", "draft/demo-topic")
CODEX_SESSION_ALIAS = bs.notebook_alias("codexFactory", "draft/demo-topic")


def _doc(body: str) -> str:
    return f"# Demo Topic\n\nStatus: staged\nKind: staging-packet\n\n{body}\n"


class FakeNlm:
    """Records every call; models the `nlm` verbs the notebook adapter uses.

    Injected as `NotebookAdapter(runner=...)`, so the REAL adapter code runs and
    the real CLI never does (FR-043). `quota` caps how many notebooks may exist —
    a create beyond it raises the way a full NotebookLM account does, which is
    D19's degradation input.
    """

    def __init__(self, notebooks=(), *, quota: int | None = None) -> None:
        self.calls: list[tuple] = []
        self.notebooks = [dict(nb) for nb in notebooks]
        self.sources: dict[str, list[dict]] = {nb["id"]: [] for nb in self.notebooks}
        self.quota = quota
        self._ids = itertools.count(1)

    # ---- the runner shape (`nlm(*args, parse=True)`) ----
    def __call__(self, *args, parse=True):
        self.calls.append(args)
        head = args[:2]
        if head == ("notebook", "list"):
            return list(self.notebooks)
        if head == ("notebook", "create"):
            title = args[2]
            if self.quota is not None and len(self.notebooks) >= self.quota:
                raise RuntimeError(
                    "nlm notebook create: the account's notebook limit is "
                    "reached (quota exhausted)")
            nb = {"id": f"nb{next(self._ids)}", "title": title}
            self.notebooks.append(nb)
            self.sources[nb["id"]] = []
            return nb
        if head == ("notebook", "delete"):
            self.notebooks = [n for n in self.notebooks if n.get("id") != args[2]]
            self.sources.pop(args[2], None)
            return ""
        if head == ("notebook", "get"):
            return {"id": args[2]}
        if head == ("source", "list"):
            return list(self.sources.get(args[2], []))
        if head == ("source", "add"):
            nid, text, title = args[2], args[4], args[6]
            row = {"id": f"src{next(self._ids)}", "title": title, "content": text}
            self.sources.setdefault(nid, []).append(row)
            return ""
        if head == ("source", "delete"):
            for nid, rows in self.sources.items():
                self.sources[nid] = [r for r in rows if r.get("id") != args[2]]
            return ""
        return {}

    # ---- reads the assertions use ----
    def titles(self) -> list[str]:
        return sorted(nb["title"] for nb in self.notebooks)

    def notebook(self, title: str) -> dict | None:
        return next((nb for nb in self.notebooks if nb.get("title") == title), None)

    def sources_of(self, title: str) -> list[dict]:
        nb = self.notebook(title)
        return list(self.sources.get(nb["id"], [])) if nb else []

    def added_contents(self) -> list[str]:
        return [c[4] for c in self.calls if c[:2] == ("source", "add")]

    def created_titles(self) -> list[str]:
        return [c[2] for c in self.calls if c[:2] == ("notebook", "create")]

    def deleted_ids(self) -> list[str]:
        return [c[2] for c in self.calls if c[:2] == ("notebook", "delete")]


def _boom(*args, **kwargs):
    raise AssertionError("the real nlm runner must never be called in tests")


def _git(cwd: Path, *args: str) -> str:
    done = subprocess.run(["git", *args], cwd=str(cwd), text=True,
                          capture_output=True, check=True)
    return done.stdout.strip()


def _init_repo(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "--initial-branch=main")
    _git(root, "config", "user.email", "harness@example.invalid")
    _git(root, "config", "user.name", "Notebook Harness")
    _git(root, "config", "commit.gpgsign", "false")


def _seed_checkout(checkout: Path, *, text: str) -> None:
    """A throwaway checkout on `main` carrying one staged fragment."""
    _init_repo(checkout)
    target = checkout / STAGED_DOC
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    _git(checkout, "add", "--", STAGED_DOC)
    _git(checkout, "commit", "-m", "Seed the scratch corpus")


def _add_worktree(checkout: Path, branch: str) -> Path:
    """A REAL session worktree at the derived container path — the same
    derivation `branch_session.worktree_path` gives the dashboard, so the sync
    script's discovery is tested against the real placement (FR-005, R7)."""
    path = bs.worktree_path(checkout, branch)
    path.parent.mkdir(parents=True, exist_ok=True)
    _git(checkout, "worktree", "add", "-b", branch, str(path), "main")
    return path


def _session_world(root: Path, *, repository: str = "openxFactory",
                   branch: str = "draft/demo-topic",
                   main_text: str = "main body",
                   worktree_text: str = "worktree body",
                   nested: bool = False) -> tuple[Path, Path]:
    """A workspace root holding one repo checkout plus one live session
    worktree whose staged fragment differs from `main`'s. Returns
    (checkout, worktree)."""
    checkout = root / ("xFactories/" + repository if nested else repository)
    _seed_checkout(checkout, text=_doc(main_text))
    worktree = _add_worktree(checkout, branch)
    (worktree / STAGED_DOC).write_text(_doc(worktree_text), encoding="utf-8")
    return checkout, worktree


class _FakeRegistry:
    """The registry API `branch_session` duck-types: get / register / keys /
    drop. Deliberately NOT a SnapshotRegistry — a session's liveness is the
    entry, and this test cares about the notebook, not the projection."""

    def __init__(self) -> None:
        self.entries: dict[tuple[str, str], object] = {}

    def get(self, repository, ref):
        return self.entries.get((str(repository), str(ref)))

    def register(self, entry):
        self.entries[(str(entry.repository), str(entry.ref))] = entry
        return entry

    def keys(self):
        return list(self.entries)

    def drop(self, repository, ref):
        self.entries.pop((str(repository), str(ref)), None)


class NotebookLmSourceImportTests(unittest.TestCase):
    def test_parse_export_title_still_supports_explicit_route(self):
        target = sync.parse_export_title(
            "[export:brainstorm] openxFactory: openspec-speckit-release-flow - "
            "release branch concern"
        )
        self.assertEqual(target.status, "brainstorm")
        self.assertEqual(target.repo, "openxFactory")
        self.assertEqual(target.topic, "openspec-speckit-release-flow")
        self.assertEqual(target.title, "release branch concern")

        staged = sync.parse_export_title(
            "[export:staged] doc-health-checks - notebook drift issue"
        )
        self.assertEqual(staged.status, "staged")
        self.assertEqual(staged.repo, "openxFactory")
        self.assertEqual(staged.topic, "doc-health-checks")

        self.assertIsNone(sync.parse_export_title(
            "[brainstorm] openxFactory: ordinary lifecycle source"
        ))
        self.assertIsNone(sync.parse_export_title(
            "converted source without export tag"
        ))

    def test_import_new_sources_dry_run_pulls_all_non_seed_sources(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "openxFactory/ideation/brainstorm/release-flow").mkdir(
                parents=True
            )

            def fake_nlm(*args, parse=True):
                self.assertEqual(args, ("source", "list", "hybrid-book", "--json"))
                return [
                    {
                        "id": "seed-charter",
                        "title": "00 [charter] Read me first",
                    },
                    {
                        "id": "seed-hybrid-charter",
                        "title": "00 [hybrid charter] Read me first",
                    },
                    {
                        "id": "seed-canon",
                        "title": "[spec] openxFactory: document-lifecycle",
                    },
                    {
                        "id": "note-source",
                        "title": "The codexFactory Governance Lifecycle and Sync Protocol",
                    },
                    {
                        "id": "web-source",
                        "title": "NotebookLM Help - Create and add notes",
                    },
                ]

            with patch.object(sync, "nlm", fake_nlm):
                count = sync.import_new_sources(
                    root,
                    "hybrid-book",
                    "openxFactory/ideation/brainstorm/release-flow",
                    apply=False,
                    imported_on="2026-07-09",
                )

            self.assertEqual(count, 2)
            self.assertEqual(list(root.rglob("notebooklm-ideas-2026-07-09.md")), [])

    def test_import_new_sources_writes_to_origin_folder_and_dedupes(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            target = "openxFactory/ideation/staging/doc-health-checks"
            (root / target).mkdir(parents=True)
            content_calls = []

            def fake_nlm(*args, parse=True):
                if args == ("source", "list", "hybrid-book", "--json"):
                    return {"sources": [
                        {
                            "id": "seed-grounding",
                            "title": "[grounding] openxFactory: document-lifecycle",
                        },
                        {
                            "id": "seed-hybrid-charter",
                            "title": "00 [hybrid charter] Read me first",
                        },
                        {
                            "source_id": "src-note",
                            "title": "Generated note title picked by NotebookLM",
                        },
                        {
                            "id": "src-web",
                            "title": "External web source title",
                        },
                    ]}
                if args == ("source", "content", "src-note"):
                    content_calls.append(args[-1])
                    return "Converted note body."
                if args == ("source", "content", "src-web"):
                    content_calls.append(args[-1])
                    return (
                        '{"value": {"content": "Added web source body.", '
                        '"source_type": "pasted_text"}}'
                    )
                raise AssertionError(args)

            with patch.object(sync, "nlm", fake_nlm):
                count = sync.import_new_sources(
                    root,
                    "hybrid-book",
                    target,
                    apply=True,
                    imported_on="2026-07-09",
                )

            self.assertEqual(count, 2)
            self.assertEqual(content_calls, ["src-note", "src-web"])

            imported = root / target / "notebooklm-ideas-2026-07-09.md"
            imported_text = imported.read_text()
            self.assertIn("Status: staged", imported_text)
            self.assertIn("Kind: reference", imported_text)
            self.assertIn("NotebookLM source id: src-note", imported_text)
            self.assertIn("NotebookLM source id: src-web", imported_text)
            self.assertIn("Authority: L1 notebook synthesis", imported_text)
            self.assertIn("Converted note body.", imported_text)
            self.assertIn("Added web source body.", imported_text)
            self.assertNotIn('"source_type"', imported_text)
            self.assertNotIn("seed-grounding", imported_text)
            self.assertNotIn("seed-hybrid-charter", imported_text)

            content_calls.clear()
            with patch.object(sync, "nlm", fake_nlm):
                again = sync.import_new_sources(
                    root,
                    "hybrid-book",
                    target,
                    apply=True,
                    imported_on="2026-07-09",
                )
            self.assertEqual(again, 0)
            self.assertEqual(content_calls, [])

    def test_proposal_origin_imports_as_draft_and_dedupes(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            change = root / "openxFactory/openspec/changes/change-a"
            target = change / "supporting-docs"
            target.mkdir(parents=True)
            (change / "proposal.md").write_text("## Why\n")
            (target / "manifest.yaml").write_text(
                '{"format_version": 1, "files": []}\n'
            )

            def fake_nlm(*args, parse=True):
                if args == ("source", "list", "proposal-book", "--json"):
                    return [{"id": "proposal-source", "title": "New proposal idea"}]
                if args == ("source", "content", "proposal-source"):
                    return "Proposal source body."
                raise AssertionError(args)

            target_arg = (
                "openxFactory/openspec/changes/change-a/supporting-docs"
            )
            with patch.object(sync, "nlm", fake_nlm):
                count = sync.import_new_sources(
                    root, "proposal-book", target_arg, True, "2026-07-09"
                )
            self.assertEqual(count, 1)
            imported = target / "notebooklm-ideas-2026-07-09.md"
            self.assertIn("Status: draft", imported.read_text())
            with patch.object(sync, "nlm", fake_nlm):
                self.assertEqual(sync.import_new_sources(
                    root, "proposal-book", target_arg, True, "2026-07-09"
                ), 0)

    def test_rejects_archived_or_missing_proposal_origin(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            archived = (
                root / "openxFactory/openspec/changes/archive/"
                "2026-07-09-change-a/supporting-docs"
            )
            archived.mkdir(parents=True)
            with self.assertRaises(ValueError):
                sync.target_from_path(root, str(archived.relative_to(root)))
            missing = (
                "openxFactory/openspec/changes/change-b/supporting-docs"
            )
            with self.assertRaises(ValueError):
                sync.target_from_path(root, missing)

    def test_hostile_export_titles_cannot_traverse_the_workspace(self):
        # topic with path syntax is flattened to a single safe segment
        target = sync.parse_export_title(
            "[export:staged] a/../../../../etc/cron.d - x")
        self.assertNotIn("/", target.topic)
        self.assertNotIn("..", target.topic)
        # repo with path syntax drops the source entirely
        self.assertIsNone(
            sync.parse_export_title("[export:brainstorm] ../evil: topic - x"))

    def test_scan_excludes_worktree_containers_and_nested_checkouts(self):
        doc = "Status: staged\n"
        with TemporaryDirectory() as td:
            root = Path(td)
            governed = root / "xFactories/RealFactory"
            (governed / "docs").mkdir(parents=True)
            (governed / ".git").mkdir()
            (governed / "docs/real-doc.md").write_text("# Real\n\n" + doc)
            (root / "openxFactory").mkdir()

            # feature-branch worktree container beside the governed repos
            wt = root / "xFactories/OpsxFactory-worktrees/002-branch"
            (wt / "docs").mkdir(parents=True)
            (wt / ".git").write_text("gitdir: elsewhere\n")
            (wt / "docs/branch-doc.md").write_text("# Branch\n\n" + doc)

            # embedded clone nested inside a governed repo
            nested = governed / "vendor/clone"
            (nested / "docs").mkdir(parents=True)
            (nested / ".git").mkdir()
            (nested / "docs/clone-doc.md").write_text("# Clone\n\n" + doc)

            desired, specs = sync.scan(root)

            ideation = desired["ideation-realfactory"]
            self.assertEqual(specs["ideation-realfactory"].title,
                             "xFactory Ideation — RealFactory")
            self.assertIn(
                "xFactories/RealFactory/docs/real-doc.md", ideation
            )
            # the worktree container spawned NO ideation book of its own
            self.assertNotIn("ideation-opsxfactory-worktrees", desired)
            polluted = [
                path for book in desired.values() for path in book
                if "worktrees" in path or "vendor/clone" in path
            ]
            self.assertEqual(polluted, [])
            repos = {
                title.split("] ", 1)[1].split(":", 1)[0]
                for book in desired.values() for title in book.values()
                if "] " in title and ":" in title
            }
            self.assertNotIn("OpsxFactory-worktrees", repos)

    def test_append_import_refuses_paths_outside_workspace(self):
        with TemporaryDirectory() as td:
            root = Path(td) / "workspace"
            root.mkdir()
            plan = sync.ExportPlan(
                source_id="s", source_title="t", status="staged",
                repo="openxFactory", topic="x", title="x",
                path=root / ".." / "escape.md")
            with self.assertRaises(SystemExit):
                sync.append_import(root, plan, "book", "content")
            self.assertFalse((Path(td) / "escape.md").exists())


# ==========================================================================
# Phase 8 — the SESSION notebook (T067-T072; FR-036-FR-043, D11, D16, D19)
# ==========================================================================


class SessionNotebookAliasTests(unittest.TestCase):
    """T067 — the alias is keyed on (repository, branch), asserted on the EXACT
    value, and the notebook's sources come from the WORKTREE."""

    def test_session_notebook_is_created_from_the_worktree_under_the_exact_alias(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = _session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)

            result = sync.sync_session_notebook(
                root, "draft/demo-topic", apply=True, adapter=adapter)

            # the EXACT expected value, not a pattern (FR-037, spec C9/C11) —
            # the ONE derivation, re-spelled nowhere
            self.assertEqual(result.alias, SESSION_ALIAS)
            self.assertEqual(result.repository, "openxFactory")
            self.assertEqual(Path(result.worktree), worktree)
            self.assertEqual(fake.created_titles(),
                             [SESSION_ALIAS])

            # the title carries NO xf-wb- reference-set prefix (FR-038, D11)
            self.assertFalse(result.alias.startswith(wb.NOTEBOOK_PREFIX))
            for title in fake.titles():
                self.assertNotIn("xf-wb-", title)

            # sources came from the WORKTREE, not from `main` (FR-036)
            contents = fake.added_contents()
            self.assertTrue(any("worktree body" in c for c in contents), contents)
            self.assertFalse(any("main body" in c for c in contents), contents)
            titles = [s["title"] for s in
                      fake.sources_of(SESSION_ALIAS)]
            self.assertTrue(any(t.startswith(STAGED_DOC) for t in titles), titles)
            self.assertEqual(result.documents, (STAGED_DOC,))

    def test_a_session_over_the_provider_source_cap_is_refused_before_any_mutation(self):
        """Step 5 of the 2026-08-24 hosting migration: the session resync route
        is deliberately unbounded (workbench finding 21 — the human-waiting
        route completes what the bounded gate-route creation deferred), so a
        session worktree whose derived corpus outgrew NotebookLM's per-notebook
        source cap would be applied as a dead run — adds failing past the cap
        mid-flight, exactly how the shared Ideation book died on 2026-08-10.
        The lifecycle books' capacity guard therefore applies here too: refuse
        BEFORE any mutation, name the excess, and leave every notebook
        untouched."""
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, _worktree = _session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)

            oversize = [(f"docs/doc-{n}.md", _doc(f"body {n}"))
                        for n in range(sync.NOTEBOOK_SOURCE_CAP + 1)]
            original = sync.session_source_set
            sync.session_source_set = lambda target: oversize
            try:
                result = sync.sync_session_notebook(
                    root, "draft/demo-topic", apply=True, adapter=adapter)
            finally:
                sync.session_source_set = original

            self.assertTrue(result.skipped, "over-cap is a refusal, not a sync")
            self.assertIn(str(sync.NOTEBOOK_SOURCE_CAP), result.detail or "")
            self.assertEqual(fake.created_titles(), [],
                             "nothing may be created when the plan cannot fit")

    def test_the_same_branch_in_a_second_repository_gets_a_different_alias(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _session_world(root, repository="openxFactory")
            _session_world(root, repository="codexFactory", nested=True,
                           main_text="factory main", worktree_text="factory work")

            # the same branch now lives in TWO repositories: resolving it without
            # naming one is ambiguous, and the refusal names both (spec C9)
            with self.assertRaises(sync.SessionNotebookRefused) as caught:
                sync.resolve_session_target(root, "draft/demo-topic")
            self.assertIn("openxFactory", str(caught.exception))
            self.assertIn("codexFactory", str(caught.exception))

            first = sync.resolve_session_target(root, "draft/demo-topic",
                                                repository="openxFactory")
            second = sync.resolve_session_target(root, "draft/demo-topic",
                                                 repository="codexFactory")
            self.assertEqual(first.alias, SESSION_ALIAS)
            self.assertEqual(second.alias, CODEX_SESSION_ALIAS)
            self.assertNotEqual(first.alias, second.alias)
            # and each alias is the ONE derivation, never re-spelled here
            for target in (first, second):
                self.assertEqual(target.alias,
                                 bs.notebook_alias(target.repository, target.branch))

    def test_a_branch_with_no_live_worktree_is_refused_not_invented(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _seed_checkout(root / "openxFactory", text=_doc("main body"))
            with self.assertRaises(sync.SessionNotebookRefused):
                sync.resolve_session_target(root, "draft/demo-topic")

    def test_the_transcribed_container_suffix_is_the_productions_own(self):
        """PR #49 second-review tail B3, the hygiene half. This script restates
        `branch_session.CONTAINER_SUFFIX` rather than importing it (it is a
        standalone hyphenated script), and the SIBLING transcription
        (`SESSION_NOTEBOOK_PREFIX`) has had a constant-equality pin since T068
        while this one had none — the FR-041 header assertions that cover it are
        `assertIn`/`assertNotIn`, which catch a drift only through a behaviour that
        happens to name a nested factory. One line closes the asymmetry, and it
        also covers the third literal (the pinned-factory-paths filter, which now
        reads the constant instead of repeating the string)."""
        self.assertEqual(sync.SESSION_CONTAINER_SUFFIX, bs.CONTAINER_SUFFIX)
        source = (Path(sync.__file__).read_text()
                  if getattr(sync, "__file__", None) else "")
        self.assertNotIn('endswith("-worktrees")', source,
                         "the suffix must be read from the constant, not retyped")

    def test_the_session_namespace_is_disjoint_from_the_swept_one(self):
        # D11: a session notebook titled xf-wb-* would be an orphan from birth.
        self.assertEqual(wb.SESSION_NOTEBOOK_PREFIX, bs.NOTEBOOK_PREFIX)
        self.assertFalse(bs.NOTEBOOK_PREFIX.startswith(wb.NOTEBOOK_PREFIX))
        self.assertFalse(wb.NOTEBOOK_PREFIX.startswith(bs.NOTEBOOK_PREFIX))
        for cfg in sync.BOOKS.values():
            self.assertFalse(cfg["alias"].startswith(bs.NOTEBOOK_PREFIX))
        # the per-repo ideation alias family is disjoint from BOTH reserved
        # namespaces too (split-ideation-book-per-repo)
        self.assertFalse(sync.IDEATION_ALIAS_PREFIX.startswith(bs.NOTEBOOK_PREFIX))
        self.assertFalse(sync.IDEATION_ALIAS_PREFIX.startswith(wb.NOTEBOOK_PREFIX))
        self.assertFalse(bs.NOTEBOOK_PREFIX.startswith(sync.IDEATION_ALIAS_PREFIX))
        self.assertFalse(wb.NOTEBOOK_PREFIX.startswith(sync.IDEATION_ALIAS_PREFIX))


class SessionNotebookSweepSafetyTests(unittest.TestCase):
    """T068 — the sweep leaves a live session notebook untouched (FR-038). This
    is the test that would have caught the original `xf-wb-<topic>` naming."""

    def _sweep(self, root, apply, adapter):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sync.workbench_orphan_sweep(root, apply, adapter=adapter)
        return buf.getvalue()

    def test_orphan_sweep_never_takes_a_live_session_notebook(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            fake = FakeNlm(LIFECYCLE_BOOKS + [
                {"id": "s1", "title": alias},
                {"id": "w1", "title": "xf-wb-orphan"},
            ])
            adapter = wb.NotebookAdapter(fake, available=True)

            # NO live workbench manifest binds anything: every xf-wb-* is an
            # orphan, and the session notebook is still not a candidate.
            out = self._sweep(root, True, adapter)

            self.assertEqual(fake.deleted_ids(), ["w1"])
            self.assertIn(alias, fake.titles())
            self.assertNotIn(alias, out)
            self.assertEqual(
                fake.titles(),
                ["xf-canon", "xf-drafts", "xf-ideation", alias])

    def test_the_dry_run_plan_never_names_a_session_notebook(self):
        with TemporaryDirectory() as td:
            alias = bs.notebook_alias("openxFactory", "cluster/cl-x")
            fake = FakeNlm([{"id": "s1", "title": alias},
                            {"id": "w1", "title": "xf-wb-orphan"}])
            adapter = wb.NotebookAdapter(fake, available=True)
            out = self._sweep(Path(td), False, adapter)
            self.assertIn("SWEEP xf-wb-orphan", out)
            self.assertNotIn(alias, out)
            self.assertEqual(fake.deleted_ids(), [])

    def test_the_dry_run_says_the_account_is_UNREADABLE_not_that_it_is_empty(self):
        """Finding 13's RESIDUAL, closed (wave 2): the one read-only path the
        wave-1 fix's four callers did not cover.

        The dry run listed candidates through `list_scratch()`, which collapses a
        failed `nlm notebook list` into `[]`, so over an unreadable account it
        printed ABSOLUTELY NOTHING and read as "no orphans pending" — while the
        SAME command with `--apply` correctly said the list could not be read. Two
        halves of one command disagreeing about whether the account is empty is
        exactly the absence-of-evidence the finding was filed about."""
        class Unreadable(FakeNlm):
            def __call__(self, *args, parse=True):
                if args[:2] == ("notebook", "list"):
                    raise RuntimeError("nlm notebook list: auth expired")
                return super().__call__(*args, parse=parse)

        with TemporaryDirectory() as td:
            fake = Unreadable([{"id": "w1", "title": "xf-wb-orphan"}])
            adapter = wb.NotebookAdapter(fake, available=True)

            dry = self._sweep(Path(td), False, adapter)
            applied = self._sweep(Path(td), True, adapter)

            self.assertIn("could not be read", dry)
            self.assertIn("NOT an empty account", dry)
            self.assertNotIn("orphan(s) pending", dry)
            self.assertNotIn("SWEEP", dry)
            # and the two halves agree, which is the property that was missing
            self.assertIn("could not be read", applied)
            self.assertEqual(fake.deleted_ids(), [])

    def test_a_session_leaves_no_manifest_that_could_disable_the_sweep(self):
        # research R8's trap: a per-session MANIFEST DIRECTORY would trip
        # `_out_of_scope_workbench_dirs` and silently skip the whole sweep.
        with TemporaryDirectory() as td:
            root = Path(td)
            _session_world(root)
            fake = FakeNlm([{"id": "w1", "title": "xf-wb-orphan"}])
            adapter = wb.NotebookAdapter(fake, available=True)
            sync.sync_session_notebook(root, "draft/demo-topic", apply=True,
                                       adapter=adapter)
            self.assertEqual(sync._out_of_scope_workbench_dirs(root), [])
            out = self._sweep(root, True, adapter)
            self.assertNotIn("SKIPPED", out)
            self.assertEqual(fake.deleted_ids(), ["w1"])


class SessionNotebookBookIsolationTests(unittest.TestCase):
    """T069 — NO lifecycle book ever contains a worktree-sourced document
    (FR-039), in addition to the existing `<repo>-worktrees/` exclusion."""

    def _assert_books_are_main_only(self, root, worktrees):
        desired, _specs = sync.scan(root)
        polluted = [path for book in desired.values() for path in book
                    if "-worktrees" in path or "sessions/" in path]
        self.assertEqual(polluted, [])
        for worktree in worktrees:
            rel = worktree.relative_to(root).as_posix()
            for book, items in desired.items():
                for path in items:
                    self.assertFalse(path.startswith(rel),
                                     f"{book} took a worktree source: {path}")
        repos = {title.split("] ", 1)[1].split(":", 1)[0]
                 for book in desired.values() for title in book.values()
                 if "] " in title and ":" in title}
        for repo in repos:
            self.assertFalse(repo.endswith("-worktrees"), repo)
        return desired

    def test_session_worktrees_are_outside_every_book_with_pins_present(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _, openx_wt = _session_world(root, repository="openxFactory")
            _, factory_wt = _session_world(root, repository="codexFactory",
                                           nested=True)
            (root / ".gitmodules").write_text(
                "[submodule \"codexFactory\"]\n"
                "\tpath = xFactories/codexFactory\n"
                "\turl = https://example.invalid/codexFactory.git\n",
                encoding="utf-8")
            self.assertEqual(sync.pinned_factory_paths(root),
                             ["xFactories/codexFactory"])
            desired = self._assert_books_are_main_only(root, [openx_wt, factory_wt])
            # the docs on `main` DO project — the exclusion is of the worktree,
            # not of the repository — and each repo's doc lands in ITS OWN
            # ideation book (split-ideation-book-per-repo)
            self.assertIn(f"openxFactory/{STAGED_DOC}",
                          desired["ideation-openxfactory"])
            self.assertIn(f"xFactories/codexFactory/{STAGED_DOC}",
                          desired["ideation-codexfactory"])
            self.assertNotIn(f"openxFactory/{STAGED_DOC}",
                             desired["ideation-codexfactory"])

    def test_session_worktrees_are_outside_every_book_without_pins(self):
        # the `.gitmodules`-absent fallback path of `pinned_factory_paths`
        with TemporaryDirectory() as td:
            root = Path(td)
            _, openx_wt = _session_world(root, repository="openxFactory")
            _, factory_wt = _session_world(root, repository="codexFactory",
                                           nested=True)
            self.assertNotIn("xFactories/codexFactory-worktrees",
                             sync.pinned_factory_paths(root))
            self._assert_books_are_main_only(root, [openx_wt, factory_wt])

    def test_a_session_source_set_and_a_book_share_no_document(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _, worktree = _session_world(root)
            target = sync.resolve_session_target(root, "draft/demo-topic")
            session_paths = {str(worktree.relative_to(root) / path)
                             for path, _text in sync.session_source_set(target)}
            book_paths = {path for book in sync.scan(root)[0].values() for path in book}
            self.assertTrue(session_paths)
            self.assertEqual(session_paths & book_paths, set())


class SessionNotebookRefreshTests(unittest.TestCase):
    """T070 — refresh re-syncs FROM the worktree; session end RETIRES the
    notebook and never re-points it at `main` (FR-036, FR-040, D16)."""

    def test_refresh_resyncs_from_the_worktree_without_recreating(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = _session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            alias = SESSION_ALIAS

            sync.sync_session_notebook(root, "draft/demo-topic", apply=True,
                                       adapter=adapter)
            first = fake.notebook(alias)["id"]
            self.assertEqual(len(fake.sources_of(alias)), 1)

            # an unchanged re-sync is a no-op (title + content hash diff)
            sync.sync_session_notebook(root, "draft/demo-topic", apply=True,
                                       adapter=adapter)
            self.assertEqual(fake.created_titles(), [alias])
            self.assertEqual(len(fake.added_contents()), 1)

            # the worktree moves on; the refresh follows IT
            (worktree / STAGED_DOC).write_text(_doc("second worktree body"),
                                               encoding="utf-8")
            sync.sync_session_notebook(root, "draft/demo-topic", apply=True,
                                       adapter=adapter)
            self.assertEqual(fake.notebook(alias)["id"], first)
            self.assertEqual(len(fake.sources_of(alias)), 1)
            self.assertIn("second worktree body",
                          fake.sources_of(alias)[0]["content"])
            self.assertFalse(any("main body" in c for c in fake.added_contents()))

    def test_the_dry_run_prints_a_plan_touches_nothing_and_is_not_book_drift(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                result = sync.sync_session_notebook(
                    root, "draft/demo-topic", apply=False, adapter=adapter)
            out = buf.getvalue()
            self.assertFalse(result.applied)
            self.assertEqual(fake.created_titles(), [])
            self.assertEqual(fake.added_contents(), [])
            self.assertIn(SESSION_ALIAS, out)
            for line in out.splitlines():
                self.assertIsNone(SYNC_OP.match(line), line)

    def test_session_end_retires_the_notebook_and_never_repoints_it_at_main(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            alias = SESSION_ALIAS
            sync.sync_session_notebook(root, "draft/demo-topic", apply=True,
                                       adapter=adapter)
            created = fake.notebook(alias)["id"]

            result = sync.sync_session_notebook(root, "draft/demo-topic",
                                                apply=True, adapter=adapter,
                                                retire=True)

            self.assertTrue(result.retired)
            self.assertEqual(fake.deleted_ids(), [created])
            self.assertIsNone(fake.notebook(alias))
            # RETIRED, never re-pointed at `main` (D16): nothing was created
            # again and no source was ever added from the served checkout
            self.assertEqual(fake.created_titles(), [alias])
            self.assertFalse(any("main body" in c for c in fake.added_contents()))
            # the lifecycle books are untouched by an ending
            self.assertEqual(fake.titles(), ["xf-canon", "xf-drafts", "xf-ideation"])

    def test_the_teardown_seam_retires_through_the_real_adapter(self):
        # `branch_session.retire_session_notebook` is what BOTH endings call
        # (FR-021); with the nlm-backed adapter injected it must really remove
        # the xf-session-* notebook, not report a benign no-op.
        with TemporaryDirectory() as td:
            root = Path(td)
            _session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            alias = SESSION_ALIAS
            sync.sync_session_notebook(root, "draft/demo-topic", apply=True,
                                       adapter=adapter)
            retired, detail = bs.retire_session_notebook(
                adapter, repository="openxFactory",
                branch="draft/demo-topic")
            self.assertTrue(retired, detail)
            self.assertIsNone(fake.notebook(alias))

    def test_retire_refuses_to_cross_into_the_reference_set_namespace(self):
        fake = FakeNlm([{"id": "w1", "title": "xf-wb-alpha"}])
        adapter = wb.NotebookAdapter(fake, available=True)
        with self.assertRaises(wb.WorkbenchError):
            adapter.retire("xf-wb-alpha")
        with self.assertRaises(wb.WorkbenchError):
            adapter.create_session("xf-wb-alpha")
        self.assertEqual(fake.deleted_ids(), [])


class SessionNotebookImportTests(unittest.TestCase):
    """T071 — a hybrid import lands in the origin folder INSIDE the worktree, on
    the branch, with the header contract and idempotency-by-source-id unchanged
    (FR-041)."""

    def test_an_import_lands_in_the_worktree_on_the_session_branch(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, worktree = _session_world(root)
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root))

            def fake_nlm(*args, parse=True):
                if args[:2] == ("source", "list"):
                    return [{"id": "src-note", "title": "A converted note"}]
                if args == ("source", "content", "src-note"):
                    return "Session note body."
                raise AssertionError(args)

            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            with patch.object(sync, "nlm", fake_nlm):
                count = sync.import_new_sources(root, alias, target_arg, True,
                                                "2026-07-26")
            self.assertEqual(count, 1)

            landed = worktree / "ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md"
            self.assertTrue(landed.is_file())
            # INSIDE the worktree, on the session BRANCH — never on `main`
            self.assertEqual(_git(worktree, "rev-parse", "--abbrev-ref", "HEAD"),
                             "draft/demo-topic")
            # LANDED, not merely written (FR-041, T071: "on the branch"). This
            # test used to pin the file as UNTRACKED, which locked in silent data
            # loss: it carries `Status: staged` under a governed root, so
            # `workbench.session_documents` includes it and it projects into the
            # notebook and the session's panels as live governed material — while
            # BOTH endings run `git worktree remove --force`, which deletes
            # untracked files outright (measured: PR #49 review finding 12).
            self.assertNotIn("notebooklm-ideas-2026-07-26.md",
                             _git(worktree, "status", "--porcelain"))
            self.assertIn("notebooklm-ideas-2026-07-26.md",
                          _git(worktree, "show", "--name-only", "--format=",
                               "HEAD"))
            self.assertIn("Source-Notebook: " + alias,
                          _git(worktree, "log", "-1", "--format=%B"))
            # …and the commit carries ONLY the imported file: the governed commit
            # path binds it (`commit --only`), so a neighbouring modification in
            # the same worktree cannot ride along
            self.assertEqual(
                _git(worktree, "show", "--name-only", "--format=", "HEAD").split(),
                ["ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md"])
            self.assertFalse(
                (checkout / "ideation/staging/demo-topic/"
                 "notebooklm-ideas-2026-07-26.md").exists())

            # the header contract, applied VERBATIM and unchanged
            text = landed.read_text()
            self.assertIn("Status: staged", text)
            self.assertIn("Kind: reference", text)
            self.assertIn("Repository context: openxFactory", text)
            self.assertNotIn("Repository context: openxFactory-worktrees", text)
            self.assertIn(f"Source workspace: {alias}", text)
            self.assertIn("Authority: L1 notebook synthesis", text)
            self.assertIn("NotebookLM source id: src-note", text)

            # idempotency BY SOURCE ID, unchanged: a re-run imports nothing
            with patch.object(sync, "nlm", fake_nlm):
                again = sync.import_new_sources(root, alias, target_arg, True,
                                                "2026-07-26")
            self.assertEqual(again, 0)
            self.assertEqual(text, landed.read_text())

    def test_an_import_refuses_a_worktree_that_drifted_during_the_fetch(self):
        """PR #49 review finding 5, wave 2 — the THIRD site that commits into a
        session worktree, and the one the wave's own contract line ("every consumer
        that is about to WRITE asks") did not cover.

        `bind_session_import` resolves the session BEFORE the sources are fetched,
        and each fetch is a network round trip, so the window between the binding
        and the commit is arbitrarily long — much longer than a gate action's. A
        human's `git checkout` inside the worktree during it used to send the
        imported file's commit onto whatever branch the directory then held, while
        the report attested `COMMITTED on draft/demo-topic`. The drift is injected
        INSIDE the fetch, which is exactly where it lands in production — a
        deterministic barrier, not a sleep."""
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, worktree = _session_world(root)
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root))
            before = _git(checkout, "rev-parse", "draft/demo-topic")

            def fake_nlm(*args, parse=True):
                if args[:2] == ("source", "list"):
                    return [{"id": "src-note", "title": "A converted note"}]
                if args == ("source", "content", "src-note"):
                    _git(worktree, "checkout", "-q", "-b",
                         "somebody-elses-branch")
                    return "Session note body."
                raise AssertionError(args)

            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            buf = io.StringIO()
            with patch.object(sync, "nlm", fake_nlm):
                with contextlib.redirect_stdout(buf):
                    count = sync.import_new_sources(root, alias, target_arg, True,
                                                    "2026-07-26")
            out = buf.getvalue()

            # the bytes are never lost: they were already written when the drift
            # was found, and the file stays in the worktree for the human
            self.assertEqual(count, 1)
            landed = (worktree
                      / "ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md")
            self.assertTrue(landed.is_file())
            # NOTHING was committed: not onto the drifted branch, and not onto the
            # session branch the report would otherwise have named
            self.assertEqual(_git(checkout, "rev-parse", "draft/demo-topic"), before)
            self.assertEqual(_git(worktree, "rev-parse", "somebody-elses-branch"),
                             before)
            # ... and the report says so, naming the branch git actually holds
            self.assertNotIn("[session] COMMITTED", out)
            self.assertIn("NOT COMMITTED", out)
            self.assertIn("somebody-elses-branch", out)
            self.assertIn("UNTRACKED", out)

    def test_a_nested_factory_session_import_keeps_the_repository_name(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = _session_world(root, repository="codexFactory",
                                                 nested=True)
            target = sync.target_from_path(
                root, str((worktree / "ideation/staging/demo-topic")
                          .relative_to(root)))
            self.assertEqual(target.repo, "codexFactory")
            self.assertEqual(target.status, "staged")
            self.assertEqual(target.topic, "demo-topic")


class SessionNotebookQuotaTests(unittest.TestCase):
    """T072 — an exhausted quota DEGRADES the session, never blocks it, and the
    notice is honest about whose limit was hit (FR-042, D19)."""

    def _open(self, root, adapter):
        """Open the session and then ATTACH its notebook — the two steps the
        gate action performs, in the order it performs them.

        The OPEN no longer creates the notebook (PR #49 review finding 3): a
        refused first create used to leave a real notebook on the shared account
        with no unwind, so the create is deferred to the first SUCCESSFUL commit
        and `attach_session_notebook` is that step. Everything asserted below —
        the degradation, the notice, the create-from-the-worktree — is unchanged;
        only WHEN it happens moved."""
        checkout = root / "openxFactory"
        _seed_checkout(checkout, text=_doc("main body"))
        git = sg.SessionGit(checkout)
        registry = _FakeRegistry()
        tile = bs.Tile("staged-topic", "demo-topic")
        session = bs.open_session(git, registry, repository="openxFactory",
                                  tile=tile, checkout_root=checkout,
                                  verb="create-document", notebook=adapter)
        # the open itself creates NOTHING on the account, whatever the adapter
        self.assertIsNone(session.notebook_notice)
        self.assertFalse(session.notebook_created)
        return bs.attach_session_notebook(session)

    def test_an_exhausted_quota_still_opens_the_session(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            # the fixture's lifecycle books already exist and the account
            # holds no more
            fake = FakeNlm(LIFECYCLE_BOOKS, quota=3)
            adapter = wb.NotebookAdapter(fake, available=True)

            session = self._open(root, adapter)

            self.assertTrue(session.opened)
            self.assertTrue(Path(session.worktree).is_dir())
            self.assertEqual(session.branch, "draft/demo-topic")
            self.assertEqual(session.notebook_alias,
                             SESSION_ALIAS)
            self.assertFalse(session.notebook_created)
            self.assertEqual(fake.titles(),
                             ["xf-canon", "xf-drafts", "xf-ideation"])

    def test_the_notice_speaks_of_concurrent_tiles_across_everyone(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            fake = FakeNlm(LIFECYCLE_BOOKS, quota=3)
            adapter = wb.NotebookAdapter(fake, available=True)

            session = self._open(root, adapter)

            notice = session.notebook_notice or ""
            lowered = notice.lower()
            self.assertIn("concurrent tiles across everyone", lowered)
            self.assertIn("shared", lowered)
            self.assertIn("xf-wb-", notice)
            self.assertIn("xf-session-", notice)
            # never phrased as this human's own doing (D19)
            for blame in ("your sessions", "sessions you", "too many",
                          "you opened", "your limit"):
                self.assertNotIn(blame, lowered, notice)
            # and it names the honest retry route (FR-040)
            self.assertIn("--session-ref draft/demo-topic", notice)

    def test_with_quota_room_the_session_opens_with_its_notebook(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)

            session = self._open(root, adapter)

            self.assertTrue(session.notebook_created)
            self.assertIsNone(session.notebook_notice)
            self.assertEqual(fake.created_titles(),
                             [SESSION_ALIAS])
            # created FROM the worktree the open just made
            self.assertTrue(any(
                "main body" in c for c in fake.added_contents()))

    def test_a_plane_with_no_adapter_creates_nothing_and_says_nothing(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            session = self._open(root, None)
            self.assertTrue(session.opened)
            self.assertFalse(session.notebook_created)
            self.assertIsNone(session.notebook_notice)


class SessionImportBindingTests(unittest.TestCase):
    """PR #49 review finding 12 — the session source-return import is BOUND to
    the exact live session, lands through the governed commit path, cannot feed
    itself, and never reads a directory alone as liveness.

    Every test here was written against the pre-fix script and fails on it. No
    real `nlm`: `sync.nlm` is patched at every call site, and
    `tests/hermeticity.py` makes the binary unreachable besides (FR-043)."""

    def _nlm(self, sources, contents=None):
        contents = contents or {}

        def fake_nlm(*args, parse=True):
            if args[:2] == ("source", "list"):
                return list(sources)
            if args[:2] == ("source", "content"):
                return contents.get(args[2], "Session note body.")
            raise AssertionError(args)

        return fake_nlm

    def _import(self, root, notebook, target_arg, sources, contents=None):
        with patch.object(sync, "nlm", self._nlm(sources, contents)):
            return sync.import_new_sources(root, notebook, target_arg, True,
                                           "2026-07-26")

    def test_a_session_notebook_cannot_import_into_the_served_checkout(self):
        """The single most likely human slip: the ORDINARY import spelling, one
        path segment shorter than quickstart step 7's. It landed an unmerged
        session's notebook synthesis in the SERVED MAIN checkout — which FR-004
        forbids any session operation from touching, and which `scan()` then picks
        up as a lifecycle-book source, breaching FR-039's main-only rule."""
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, _worktree = _session_world(root)
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")

            with self.assertRaises(sync.SessionNotebookRefused) as caught:
                self._import(root, alias, "openxFactory/ideation/staging/demo-topic",
                             [{"id": "src-note", "title": "A converted note"}])

            self.assertIn("not inside it", str(caught.exception))
            self.assertFalse(
                (checkout / "ideation/staging/demo-topic"
                 "/notebooklm-ideas-2026-07-26.md").exists())
            self.assertEqual(_git(checkout, "status", "--porcelain"), "")

    def test_a_session_notebook_cannot_import_into_another_sessions_worktree(self):
        """Session A's notebook pointed at session B's worktree wrote A's content
        onto B's branch, carrying A's `Source workspace:` header."""
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, _a = _session_world(root)
            other = _add_worktree(checkout, "draft/other-topic")
            (other / STAGED_DOC).write_text(_doc("other body"), encoding="utf-8")
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            target_arg = str(
                (other / "ideation/staging/demo-topic").relative_to(root))

            with self.assertRaises(sync.SessionNotebookRefused):
                self._import(root, alias, target_arg,
                             [{"id": "src-note", "title": "A converted note"}])

            self.assertEqual(
                list((other / "ideation/staging/demo-topic").glob(
                    "notebooklm-ideas-*.md")), [])

    def test_a_non_session_notebook_cannot_import_into_a_session_worktree(self):
        """The symmetric refusal: a session worktree holds ONE session's unmerged
        work, so another notebook's sources may not be written onto its branch."""
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = _session_world(root)
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root))

            with self.assertRaises(sync.SessionNotebookRefused) as caught:
                self._import(root, "xf-ideation", target_arg,
                             [{"id": "src-note", "title": "A converted note"}])

            self.assertIn("is not that session's notebook", str(caught.exception))

    def test_a_dead_sessions_directory_is_not_a_live_session(self):
        """`resolve_session_target` tested `worktree.is_dir()` and NOTHING else,
        so against crash residue — the git association pruned AND the branch
        deleted — it returned a target and drove create / re-sync / RETIRE against
        a session that did not exist. `bootstrap_sessions`, handed the identical
        directory, answered `live=()` and reported it stale (FR-008, D10)."""
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, worktree = _session_world(root, branch="draft/residue-topic")
            _git(checkout, "worktree", "remove", "--force", str(worktree))
            _git(checkout, "branch", "-D", "draft/residue-topic")
            worktree.mkdir(parents=True)
            (worktree / "ideation/staging/demo-topic").mkdir(parents=True)

            with self.assertRaises(sync.SessionNotebookRefused) as caught:
                sync.resolve_session_target(root, "draft/residue-topic")
            self.assertIn("JOINT worktree+branch signal", str(caught.exception))

            # and the two liveness answers now AGREE
            registry = _dashboard_registry()
            report = bs.bootstrap_sessions(registry, repository="openxFactory",
                                           checkout_root=checkout)
            self.assertEqual(report.branches, ())

    def test_the_import_cannot_feed_itself(self):
        """Unbounded self-amplification, measured at 788 -> 2120 -> 4784 -> 10112
        bytes over four rounds. A projected source's title is `<path>  #<hash>`,
        which matched neither charter title nor a `[status]` prefix, so the import
        planned the notebook's OWN projected output; the imported file then became
        a governed document, re-projected under a NEW source id, and the
        source-id dedupe could not stop it by construction."""
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = _session_world(root)
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root))
            projected = wb.managed_source_title(
                "ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md",
                "already imported body")

            count = self._import(root, alias, target_arg,
                                 [{"id": "src-self", "title": projected}])

            self.assertEqual(count, 0)
            self.assertTrue(sync.is_seed_source(projected))
            self.assertEqual(
                list((worktree / "ideation/staging/demo-topic").glob(
                    "notebooklm-ideas-*.md")), [])

    def test_a_draft_only_outline_source_still_imports_and_commits(self):
        """The positive control the refusals must not swallow: an ordinary human
        source — here a draft-only outline with no managed title at all — still
        imports into the bound session worktree and still LANDS on the branch."""
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = _session_world(root)
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root))

            count = self._import(
                root, alias, target_arg,
                [{"id": "src-outline", "title": "Outline: the draft-only shape"}],
                {"src-outline": "- one\n- two\n"})

            self.assertEqual(count, 1)
            landed = (worktree / "ideation/staging/demo-topic"
                      / "notebooklm-ideas-2026-07-26.md")
            self.assertTrue(landed.is_file())
            self.assertNotIn("notebooklm-ideas",
                             _git(worktree, "status", "--porcelain"))
            self.assertIn("Source-Notebook: " + alias,
                          _git(worktree, "log", "-1", "--format=%B"))


def _dashboard_registry():
    from ideation_dashboard.snapshot_registry import SnapshotRegistry

    return SnapshotRegistry()


class SplitIdeationBookTests(unittest.TestCase):
    """split-ideation-book-per-repo: per-repo routing, seeds-never-create,
    title resolution with alias re-registration, apply-gated lazy creation,
    and the capacity guard's occupancy math. All against a stubbed nlm —
    nothing here may touch the real CLI (FR-043)."""

    def _fake(self, notebooks, sources=None, create_ok=True):
        calls: list[tuple] = []
        state = {"notebooks": [dict(n) for n in notebooks],
                 "sources": {k: list(v) for k, v in (sources or {}).items()}}

        def fake(*args, parse=True):
            calls.append(args)
            head = args[:2]
            if head == ("notebook", "list"):
                return list(state["notebooks"])
            if head == ("notebook", "create"):
                if not create_ok:
                    raise RuntimeError("notebook quota exhausted")
                nb = {"id": f"nb{len(state['notebooks']) + 1}", "title": args[2]}
                state["notebooks"].append(nb)
                state["sources"].setdefault(nb["id"], [])
                return ""
            if head in {("alias", "set"), ("tag", "add"), ("chat", "configure"),
                        ("source", "delete"), ("source", "rename")}:
                return ""
            if head == ("source", "list"):
                return list(state["sources"].get(args[2], []))
            if head == ("source", "add"):
                nid = args[2]
                sid = f"s{len(state['sources'].setdefault(nid, [])) + 1}"
                if "--file" in args:
                    # the CLI titles a --file source by FILENAME and echoes the id
                    state["sources"][nid].append({"id": sid, "title": "upload.md"})
                    return f"Added source: upload.md\nSource ID: {sid}\n"
                state["sources"][nid].append({"id": sid, "title": args[6]})
                return ""
            raise AssertionError(f"unexpected nlm call: {args}")

        return fake, calls, state

    @staticmethod
    def _world(root: Path, brainstorms: int = 1) -> None:
        (root / "openxFactory/examples").mkdir(parents=True, exist_ok=True)
        (root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
         ).write_text("workspaces:\n", encoding="utf-8")
        for g in sync.GROUNDING:
            p = root / g
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# Grounding\n", encoding="utf-8")
        base = root / "openxFactory/ideation/brainstorm"
        base.mkdir(parents=True, exist_ok=True)
        for i in range(brainstorms):
            (base / f"idea-{i:02d}.md").write_text(
                f"# Idea {i}\n\nStatus: brainstorm\n", encoding="utf-8")

    def test_seeds_never_create_a_book(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "openxFactory/docs").mkdir(parents=True)
            (root / "openxFactory/docs/x.md").write_text(
                "# X\n\nStatus: draft\n", encoding="utf-8")
            desired, _specs = sync.scan(root)
            # grounding/charter seeding must not conjure an ideation book for
            # a repo with zero brainstorm/staged documents
            self.assertNotIn("ideation-openxfactory", desired)
            self.assertIn("drafts", desired)

    def test_dry_run_reports_pending_creation_and_mutates_nothing(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, _state = self._fake([])
            out = io.StringIO()
            with patch.object(sync, "nlm", fake), contextlib.redirect_stdout(out):
                ok, over = sync.sync_book(root, spec, desired[spec.key], {}, False)
            self.assertTrue(ok)
            self.assertFalse(over)
            self.assertIn("CREATE", out.getvalue())
            self.assertNotIn(("notebook", "create"), [c[:2] for c in calls])
            # the pending adds stay visible drift for doc-health
            self.assertIn("ADD", out.getvalue())

    def test_apply_creates_seeds_and_writes_the_workspace_record(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, state = self._fake([])
            out = io.StringIO()
            with patch.object(sync, "nlm", fake), \
                    patch.object(sync.time, "sleep", lambda _s: None), \
                    contextlib.redirect_stdout(out):
                ok, over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertTrue(ok)
            self.assertFalse(over)
            heads = [c[:2] for c in calls]
            for required in (("notebook", "create"), ("alias", "set"),
                             ("tag", "add"), ("chat", "configure")):
                self.assertIn(required, heads)
            record = (root / "openxFactory/examples/"
                             "lifecycle-notebook-workspaces.yaml").read_text()
            self.assertIn("workspace-xfactory-lifecycle-ideation-openxfactory",
                          record)
            self.assertIn(state["notebooks"][0]["id"], record)

    def test_missing_alias_resolves_by_title_and_reregisters(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            with patch.object(sync, "nlm", fake), \
                    patch.object(sync.time, "sleep", lambda _s: None), \
                    contextlib.redirect_stdout(io.StringIO()):
                sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertIn(("alias", "set", spec.alias, "nbX"), calls)
            self.assertNotIn(("notebook", "create"), [c[:2] for c in calls])
            adds = [c for c in calls if c[:2] == ("source", "add")]
            self.assertTrue(adds)
            # addressed by notebook id, never by alias
            self.assertTrue(all(c[2] == "nbX" for c in adds))

    def test_over_cap_projects_the_prefix_and_reports_the_exact_excess(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root, brainstorms=7)   # 7 members + 3 grounding = 10
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            unmanaged = [{"id": "hand1", "title": "my hand-added PDF"}]
            fake, calls, _state = self._fake(
                [{"id": "nbX", "title": spec.title}], sources={"nbX": unmanaged})
            out = io.StringIO()
            with patch.object(sync, "NOTEBOOK_SOURCE_CAP", 8), \
                    patch.object(sync, "nlm", fake), \
                    patch.object(sync.time, "sleep", lambda _s: None), \
                    contextlib.redirect_stdout(out):
                ok, over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            text = out.getvalue()
            self.assertTrue(over)
            # occupancy 10 members + 1 charter + 1 unmanaged = 12 over cap 8:
            # in-cap prefix is 8 - 1 charter - 1 unmanaged = 6 members
            self.assertEqual(text.count("EXCESS"), 4)
            adds = [c for c in calls if c[:2] == ("source", "add")
                    and c[6] != sync.CHARTER_TITLE]
            self.assertEqual(len(adds), 6)

    def test_oversized_source_rides_a_file_and_is_renamed_to_its_title(self):
        # Linux MAX_ARG_STRLEN killed the canon book live 2026-08-10: a doc
        # too large for one argv string must upload as a file and then be
        # renamed to the contract title (--title is ignored on --file).
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            big = root / "openxFactory/ideation/brainstorm/huge.md"
            big.write_text("# Huge\n\nStatus: brainstorm\n" + "x" * 500,
                           encoding="utf-8")
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            with patch.object(sync, "MAX_TEXT_ARG_BYTES", 200), \
                    patch.object(sync, "nlm", fake), \
                    patch.object(sync.time, "sleep", lambda _s: None), \
                    contextlib.redirect_stdout(io.StringIO()):
                ok, _over = sync.sync_book(root, spec, desired[spec.key], {}, True)
            self.assertTrue(ok)
            file_adds = [c for c in calls
                         if c[:2] == ("source", "add") and "--file" in c]
            renames = [c for c in calls if c[:2] == ("source", "rename")]
            self.assertEqual(len(file_adds), 1)
            self.assertEqual(len(renames), 1)
            self.assertEqual(renames[0][3],
                             "[brainstorm] openxFactory: huge")
            # the small docs still ride --text
            text_adds = [c for c in calls
                         if c[:2] == ("source", "add") and "--text" in c]
            self.assertTrue(text_adds)

    def test_low_headroom_warns_and_names_the_owed_delta(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root, brainstorms=7)   # 10 members + charter = 11
            desired, specs = sync.scan(root)
            spec = specs["ideation-openxfactory"]
            fake, _calls, _state = self._fake([{"id": "nbX", "title": spec.title}])
            out = io.StringIO()
            with patch.object(sync, "NOTEBOOK_SOURCE_CAP", 20), \
                    patch.object(sync, "nlm", fake), \
                    contextlib.redirect_stdout(out):
                ok, over = sync.sync_book(root, spec, desired[spec.key], {}, False)
            text = out.getvalue()
            self.assertFalse(over)
            self.assertIn("WARN headroom", text)
            self.assertIn("OpenSpec delta", text)


if __name__ == "__main__":
    unittest.main()


# ---------------------------------------------------------------------------
# SESSION-NAMESPACE RECONCILIATION (add-session-notebook-reconciliation)
#
# A session torn down without an abandon leaves its notebook alive on a SHARED
# account. `--session-ref --session-retire` cannot clean that up by design (it
# refuses a dead branch, which is what stops it retiring a LIVE session's
# notebook), so the dead case gets its own door and establishes death from the
# absence of any live claim instead of a caller's assertion.
#
# The dangerous direction is the only one worth most of this coverage: a run that
# knows LESS than it thinks retires a live session's work. Every test below that
# ends in "retires nothing" is about that.
# ---------------------------------------------------------------------------

class SessionSweepTests(unittest.TestCase):
    LIVE = "xf-session-openxfactory-alpha-kaaa"
    DEAD = "xf-session-openxfactory-beta-kbbb"
    FOREIGN = "xf-session-someoneelse-gamma-kccc"

    def _adapter(self, titles, *, ok=True, retire=True):
        """A recording adapter with exactly the two operations the sweep uses."""
        calls = []

        class Listing:
            def __init__(self, rows, ok, detail=""):
                self.rows, self.ok, self.detail = rows, ok, detail

        class Result:
            def __init__(self, ok, detail):
                self.ok, self.detail = ok, detail

        class Adapter:
            def list_sessions_result(self):
                calls.append(("list",))
                rows = [{"title": t, "source_count": 7} for t in titles]
                return Listing(rows if ok else [], ok,
                               "" if ok else "nlm notebook list failed")

        if retire:
            def _retire(self, alias):
                calls.append(("retire", alias))
                return Result(True, "retired")
            Adapter.retire = _retire
        return Adapter(), calls

    def _classify(self, titles, live, slugs):
        return dict(sync.classify_session_notebooks(titles, live, slugs))

    @contextlib.contextmanager
    def _workspace(self, live_aliases, errors=(), *, repositories=("openxFactory",)):
        """Drive the REAL sweep with its two inputs controlled at ONE seam.

        `session_repositories` feeds both halves — the live-alias walk and the
        in-scope slug list — so stubbing it keeps them consistent, which is
        exactly the property the sweep depends on."""
        original_repos = sync.session_repositories
        original_aliases = sync.live_session_aliases
        try:
            sync.session_repositories = lambda root: [
                (name, Path(root) / name) for name in repositories]
            sync.live_session_aliases = lambda root, pairs=None: (
                set(live_aliases), list(errors))
            with TemporaryDirectory() as tmp:
                yield Path(tmp)
        finally:
            sync.session_repositories = original_repos
            sync.live_session_aliases = original_aliases

    def test_the_classifier_answers_three_ways_and_ignores_non_sessions(self):
        verdicts = self._classify(
            [self.LIVE, self.DEAD, self.FOREIGN, "xf-wb-scratch", "xf-canon"],
            {self.LIVE}, ["openxfactory"])
        self.assertEqual(verdicts[self.LIVE], "live")
        self.assertEqual(verdicts[self.DEAD], "dead")
        self.assertEqual(verdicts[self.FOREIGN], "out-of-scope")
        # a title that is not a session title never enters the answer at all
        self.assertNotIn("xf-wb-scratch", verdicts)
        self.assertNotIn("xf-canon", verdicts)

    def test_scope_is_tested_by_prefix_not_by_splitting_on_hyphens(self):
        """Repository names and flattened branches BOTH contain hyphens, so any
        parse of the title is ambiguous exactly where being wrong retires
        someone else's notebook. `my-repo` must claim its own notebooks and
        must not claim `my`'s."""
        mine = "xf-session-my-repo-topic-kddd"
        theirs = "xf-session-my-other-topic-keee"
        verdicts = self._classify([mine, theirs], set(), ["my-repo"])
        self.assertEqual(verdicts[mine], "dead")
        self.assertEqual(verdicts[theirs], "out-of-scope")

    def test_a_live_alias_is_never_dead_however_lossy_the_transform(self):
        """The readable half of the alias strips `draft/` and lowercases, so the
        comparison must be against the FULL derived alias, forward. A branch
        whose name differs from its alias in both ways still matches."""
        alias = bs.notebook_alias("openxFactory", "draft/Mixed-Case-Topic")
        verdicts = self._classify([alias], {alias}, ["openxfactory"])
        self.assertEqual(verdicts[alias], "live")

    def test_an_unaccountable_repository_refuses_and_retires_nothing(self):
        """THE test. A repository the run cannot enumerate yields fewer live
        aliases, and fewer aliases is indistinguishable from sessions having
        ended — so the run must refuse rather than retire what it could not
        account for."""
        adapter, calls = self._adapter([self.LIVE, self.DEAD])
        with self._workspace(
                {self.LIVE},
                errors=["openxFactory: git worktree list failed"]) as root:
            code = sync.session_notebook_sweep(root, True, adapter)
        self.assertEqual(code, 1)
        self.assertEqual(calls, [], "nothing may be listed or retired on refusal")

    def test_an_unreadable_notebook_list_refuses_and_retires_nothing(self):
        """An errored listing is not an empty account — the same rule the
        workbench sweep already applies, on the session namespace."""
        adapter, calls = self._adapter([self.DEAD], ok=False)
        with self._workspace(set()) as root:
            code = sync.session_notebook_sweep(root, True, adapter)
        self.assertEqual(code, 1)
        self.assertEqual([c for c in calls if c[0] == "retire"], [])

    def test_the_report_is_the_default_and_retires_nothing(self):
        adapter, calls = self._adapter([self.LIVE, self.DEAD, self.FOREIGN])
        with self._workspace({self.LIVE}) as root:
            code = sync.session_notebook_sweep(root, False, adapter)
        self.assertEqual(code, 0)
        self.assertEqual([c for c in calls if c[0] == "retire"], [],
                         "a report must not retire")

    def test_apply_retires_exactly_the_dead_set(self):
        adapter, calls = self._adapter([self.LIVE, self.DEAD, self.FOREIGN])
        with self._workspace({self.LIVE}) as root:
            code = sync.session_notebook_sweep(root, True, adapter)
        self.assertEqual(code, 0)
        self.assertEqual([c[1] for c in calls if c[0] == "retire"],
                         [self.DEAD],
                         "the live one and the foreign one are both untouched")

    def test_an_adapter_without_retire_refuses_loudly(self):
        adapter, calls = self._adapter([self.DEAD], retire=False)
        with self._workspace(set()) as root:
            code = sync.session_notebook_sweep(root, True, adapter)
        self.assertEqual(code, 1)
        self.assertEqual([c for c in calls if c[0] == "retire"], [])

    def test_a_workspace_with_no_session_repositories_retires_nothing(self):
        """Found by writing the test above and worth keeping: with no session
        repositories in scope, EVERY session notebook is out of scope and the
        sweep retires nothing. That is the fail-safe direction — a workspace
        that carries none of the repositories a notebook could belong to has no
        standing to judge it, and pointing this mode at the wrong root must be
        inert rather than destructive."""
        adapter, calls = self._adapter([self.LIVE, self.DEAD, self.FOREIGN])
        with self._workspace(set(), repositories=()) as root:
            code = sync.session_notebook_sweep(root, True, adapter)
        self.assertEqual(code, 0)
        self.assertEqual([c for c in calls if c[0] == "retire"], [],
                         "no in-scope repository means no notebook is judged")

    def test_the_two_session_modes_are_mutually_exclusive(self):
        """One names a branch it requires to be LIVE; the other starts from
        titles it cannot invert. Answering both in one run would mean holding
        two liveness questions at once."""
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), ".", "--session-sweep",
             "--session-ref", "draft/x"],
            capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("run them separately", proc.stderr)

    def test_a_session_opened_from_a_feature_worktree_is_seen_as_live(self):
        """THE NEAR-MISS, 2026-08-10, caught by the live dry run this change
        owed and by nothing else.

        A session's container is `<checkout>-worktrees/sessions/`, keyed on the
        checkout it was OPENED from — and sessions are routinely opened from a
        FEATURE worktree, not from the repository's canonical checkout. The first
        implementation asked only the canonical checkout, found no sessions
        there, and reported two LIVE sessions (holding unmerged work) as dead.

        Fail-closed did not fire and could not: "no sessions in this checkout" is
        a legitimate answer, indistinguishable from "the sessions are in another
        worktree". The enumeration had to become complete instead — every
        worktree git lists for the repository — which is what this asserts, at
        the level where it broke: `live_session_aliases` over a real git
        repository with a real linked worktree that owns the session."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical = root / "openxFactory"
            canonical.mkdir()

            def git(*args, cwd=canonical):
                subprocess.run(["git", *args], cwd=cwd, check=True,
                               capture_output=True, text=True)

            git("init", "--initial-branch=main")
            git("config", "user.email", "h@example.invalid")
            git("config", "user.name", "Harness")
            git("config", "commit.gpgsign", "false")
            (canonical / "seed.md").write_text("# seed\n", encoding="utf-8")
            git("add", "seed.md")
            git("commit", "-m", "seed")

            # a FEATURE worktree of the same repository…
            feature = root / "openxFactory-worktrees" / "feature-x"
            git("worktree", "add", "-b", "feature-x", str(feature))
            # …and a SESSION worktree whose container belongs to THAT checkout
            session = bs.sessions_root(feature) / bs.flatten_branch("draft/topic")
            session.parent.mkdir(parents=True, exist_ok=True)
            git("worktree", "add", "-b", "draft/topic", str(session))

            aliases, errors = sync.live_session_aliases(
                root, [("openxFactory", canonical)])

        self.assertEqual(errors, [], "a readable workspace must produce no errors")
        self.assertIn(bs.notebook_alias("openxFactory", "draft/topic"), aliases,
                      "a session opened from a feature worktree is LIVE, and "
                      "asking only the canonical checkout would have called it "
                      "dead and retired its notebook")

    def test_session_ref_sees_a_session_opened_from_a_feature_worktree(self):
        """F3, migration evidence 2026-08-24: the single-branch path never got
        the sweep's every-worktree enumeration, so `--session-ref` refused the
        two LIVE draft/* sessions the sweep could see — their session notebooks
        stayed hosted on the account being abandoned, exactly what runbook
        step 5 warns about. Same harness as the sweep's near-miss test above,
        asserted at the level that broke: `live_session_targets` over a real
        repository whose session was opened from a feature worktree."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            canonical = root / "openxFactory"
            canonical.mkdir()

            def git(*args, cwd=canonical):
                subprocess.run(["git", *args], cwd=cwd, check=True,
                               capture_output=True, text=True)

            git("init", "--initial-branch=main")
            git("config", "user.email", "h@example.invalid")
            git("config", "user.name", "Harness")
            git("config", "commit.gpgsign", "false")
            (canonical / "seed.md").write_text("# seed\n", encoding="utf-8")
            git("add", "seed.md")
            git("commit", "-m", "seed")

            # a FEATURE worktree of the same repository…
            feature = root / "openxFactory-worktrees" / "feature-x"
            git("worktree", "add", "-b", "feature-x", str(feature))
            # …and a SESSION worktree whose container belongs to THAT checkout
            session = bs.sessions_root(feature) / bs.flatten_branch("draft/topic")
            session.parent.mkdir(parents=True, exist_ok=True)
            git("worktree", "add", "-b", "draft/topic", str(session))

            targets = sync.live_session_targets(
                root, "draft/topic", "openxFactory")

        self.assertEqual(len(targets), 1,
                         "the session opened from a feature worktree is LIVE; "
                         "deriving one path from the canonical container alone "
                         "refuses it and strands its notebook")
        self.assertEqual(targets[0].repository, "openxFactory")
        self.assertEqual(targets[0].branch, "draft/topic")


# --------------------------- the declared hosting identity ---------------------------
# add-notebook-projection-identity (ratified 2026-08-23): WHICH account the
# projection is written to is contract conformance, so a run that cannot prove
# it refuses rather than falling back.

HOSTING_DECLARED = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
  declared_at: "2026-08-23"
  declared_by: Brett Heap
share_out: []
"""

HOSTING_PENDING = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
  migration:
    state: pending
    from_account: brettheap@gmail.com
    from_nlm_profile: personal
share_out: []
"""


def _declare_hosting(root: Path, text: str) -> None:
    path = root / "openxFactory/examples/notebook-projection-hosting.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _profile_runner(active: str | None):
    """A runner answering only `config get auth.default_profile`."""
    def run(*args, parse=True):
        if args[:3] == ("config", "get", "auth.default_profile"):
            if active is None:
                raise RuntimeError("nlm config get: no configuration")
            return active
        return {}
    return run


class HostingDeclarationTests(unittest.TestCase):
    """The declaration is READ, and the run is BOUND to it or refused."""

    def test_undeclared_install_is_reported_as_a_transition_state_not_a_case(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = sync.enforce_hosting_profile(
                    root, runner=_profile_runner("personal"))
        self.assertIsNone(got, "an undeclared install has no declaration to return")
        self.assertIn("NO DECLARED HOSTING IDENTITY", out.getvalue())
        self.assertIn("transition state", out.getvalue(),
                      "undeclared must be reported as nonconforming, never as "
                      "a third legitimate case")

    def test_declared_profile_active_binds_the_run(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_DECLARED)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = sync.enforce_hosting_profile(
                    root, runner=_profile_runner("company"))
        self.assertEqual(got["account"], "xFactor001@opensoft.one")
        self.assertIn("verified active", out.getvalue())

    def test_a_run_pointed_at_another_account_refuses(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_DECLARED)
            with self.assertRaises(SystemExit) as caught:
                sync.enforce_hosting_profile(
                    root, runner=_profile_runner("personal"))
        message = str(caught.exception)
        self.assertIn("Refusing", message,
                      "writing a governed projection into an undeclared "
                      "account is the failure this capability retires")
        self.assertIn("nlm login switch company", message,
                      "the refusal must carry the exact remediation command")

    def test_an_unreadable_profile_refuses_rather_than_guessing(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_DECLARED)
            with self.assertRaises(SystemExit) as caught:
                sync.enforce_hosting_profile(
                    root, runner=_profile_runner(None))
        self.assertIn("cannot prove", str(caught.exception))

    def test_a_pending_migration_binds_to_the_account_that_holds_the_books(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_PENDING)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = sync.enforce_hosting_profile(
                    root, runner=_profile_runner("personal"))
        self.assertIsNotNone(got)
        self.assertIn("MIGRATION PENDING", out.getvalue())
        self.assertIn("brettheap@gmail.com", out.getvalue(),
                      "a declaration is not a migration: until the books move, "
                      "the run binds where they actually live")

    def test_a_pending_migration_still_refuses_a_third_account(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_PENDING)
            with self.assertRaises(SystemExit):
                sync.enforce_hosting_profile(
                    root, runner=_profile_runner("someone-else"))

    def test_the_reader_ignores_comments_and_nested_blocks(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, "# leading comment\n" + HOSTING_PENDING)
            got = sync.read_hosting_declaration(root)
        self.assertEqual(got["nlm_profile"], "company")
        self.assertEqual(got["migration_from_nlm_profile"], "personal")
        self.assertEqual(got["case"], "operator_hosted")


class ParityReportTests(unittest.TestCase):
    """Parity is proven against THE CORPUS SCAN, never against other books."""

    @staticmethod
    def _world(root: Path) -> None:
        (root / "openxFactory/examples").mkdir(parents=True, exist_ok=True)
        (root / "openxFactory/examples/lifecycle-notebook-workspaces.yaml"
         ).write_text("workspaces:\n", encoding="utf-8")
        for g in sync.GROUNDING:
            p = root / g
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# Grounding\n", encoding="utf-8")
        base = root / "openxFactory/ideation/brainstorm"
        base.mkdir(parents=True, exist_ok=True)
        (base / "idea-00.md").write_text("# Idea\n\nStatus: brainstorm\n",
                                         encoding="utf-8")

    def _run_parity(self, root: Path, fake) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            with patch.object(sync, "nlm", fake):
                code = sync.parity_report(root)
        return code, out.getvalue()

    def test_a_book_missing_a_derived_title_fails_parity(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            fake = FakeNlm([{"id": f"nb{i}", "title": specs[k].title}
                            for i, k in enumerate(sorted(desired))])
            code, text = self._run_parity(root, fake)
        self.assertEqual(code, 1, "an empty live book cannot be at parity with "
                                  "a scan that derives members")
        self.assertIn("PARITY FAIL", text)
        self.assertIn("MISSING", text)

    def test_matching_books_prove_parity_with_nothing_pending(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            fake = FakeNlm([{"id": f"nb{i}", "title": specs[k].title}
                            for i, k in enumerate(sorted(desired))])
            for i, key in enumerate(sorted(desired)):
                fake.sources[f"nb{i}"] = [
                    {"id": f"s{i}-{j}", "title": title}
                    for j, title in enumerate(sorted(desired[key].values()))]
            code, text = self._run_parity(root, fake)
        self.assertEqual(code, 0, text)
        self.assertIn("parity: PROVEN", text)
        self.assertIn("0 pending ADD/DEL/UPD", text)

    def test_parity_never_mutates(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, specs = sync.scan(root)
            fake = FakeNlm([{"id": f"nb{i}", "title": specs[k].title}
                            for i, k in enumerate(sorted(desired))])
            self._run_parity(root, fake)
            verbs = {call[:2] for call in fake.calls}
        # `alias set` belongs in this blocklist: the alias store is a single
        # flat file shared across profiles, so registering one during a parity
        # proof repoints xf-canon for every account on the host.
        for mutating in (("source", "add"), ("source", "delete"),
                         ("notebook", "create"), ("notebook", "delete"),
                         ("alias", "set"), ("alias", "delete")):
            self.assertNotIn(mutating, verbs,
                             "a parity proof that changes the thing it measures "
                             "is not a proof")

    def test_a_non_string_profile_answer_is_unknown_not_a_crash(self):
        """A runner that answers with anything but text means 'unknown'.

        The refusal path depends on this returning None rather than raising:
        an exception here would escape the guard instead of becoming the
        governed refusal.
        """
        for answer in ({}, [], None, 42):
            with self.subTest(answer=answer):
                self.assertIsNone(
                    sync.active_nlm_profile(lambda *a, parse=True: answer))


class ProfileBindingHoldsForTheWholeRunTests(unittest.TestCase):
    """The binding is re-asserted before EVERY invocation, not once.

    Found in review: profile selection is process-global, so another terminal
    running `nlm login switch` after the opening check would silently redirect
    every later add and delete into a different account — across a re-derivation
    that takes about forty minutes.
    """

    def tearDown(self):
        sync.bind_profile(None)
        sync._CONFIG_CACHE = None

    @staticmethod
    def _config(root: Path, profile: str) -> Path:
        path = root / "config.toml"
        path.write_text(f'[output]\nformat = "table"\n\n[auth]\n'
                        f'browser = "auto"\ndefault_profile = "{profile}"\n',
                        encoding="utf-8")
        return path

    def test_the_configured_profile_is_read_from_the_file(self):
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            self.assertEqual(sync.configured_nlm_profile(path), "company")

    def test_an_absent_config_is_unknown(self):
        with TemporaryDirectory() as td:
            self.assertIsNone(
                sync.configured_nlm_profile(Path(td) / "nope.toml"))

    def test_an_unbound_run_asserts_nothing(self):
        sync.bind_profile(None)
        sync.assert_still_bound()  # must not raise

    def test_a_profile_switched_mid_run_refuses_the_next_invocation(self):
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            with patch.object(sync, "NLM_CONFIG", path):
                sync.bind_profile("company")
                sync.assert_still_bound()          # still bound: no raise
                self._config(Path(td), "personal")  # another terminal switches
                sync._CONFIG_CACHE = None
                with self.assertRaises(SystemExit) as caught:
                    sync.assert_still_bound()
        message = str(caught.exception)
        self.assertIn("changed mid-run", message)
        self.assertIn("nlm login switch company", message)

    def test_the_cache_does_not_hide_a_switch(self):
        with TemporaryDirectory() as td:
            path = self._config(Path(td), "company")
            with patch.object(sync, "NLM_CONFIG", path):
                sync._CONFIG_CACHE = None
                sync.bind_profile("company")
                sync.assert_still_bound()
                # rewrite with a different size so the (mtime_ns, size) stamp
                # moves even inside one filesystem timestamp tick
                path.write_text('[auth]\ndefault_profile = "a-different-one"\n',
                                encoding="utf-8")
                with self.assertRaises(SystemExit):
                    sync.assert_still_bound()


class DeclarationIsEnforcedOnTheOperationalPathTests(unittest.TestCase):
    """The refusals must fire during an ordinary run, not only in the validator.

    Found in review: nothing the sync runs invoked the validator, so a
    declaration naming a consumer or service account would have been accepted
    by `--apply`.
    """

    def tearDown(self):
        sync.bind_profile(None)

    def _enforce(self, root: Path, text: str, active: str = "company"):
        _declare_hosting(root, text)
        return sync.enforce_hosting_profile(root, runner=_profile_runner(active))

    def test_a_service_account_is_refused_by_the_sync_itself(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "account: xFactor001@opensoft.one",
                "account: books@xf.iam.gserviceaccount.com").replace(
                "domain: opensoft.one", "domain: xf.iam.gserviceaccount.com")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("service account", str(caught.exception))

    def test_a_consumer_account_is_refused_for_the_operator_hosted_case(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace(
                "account_type: google_workspace_user",
                "account_type: consumer_google_account")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("google_workspace_user", str(caught.exception))

    def test_an_account_outside_the_declared_domain_is_refused(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace("domain: opensoft.one",
                                            "domain: elsewhere.example")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("not in the declared domain", str(caught.exception))

    def test_a_third_case_is_refused(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            text = HOSTING_DECLARED.replace("case: operator_hosted",
                                            "case: partly_hosted")
            with self.assertRaises(SystemExit) as caught:
                self._enforce(root, text)
        self.assertIn("exactly one of", str(caught.exception))

    def test_a_conforming_declaration_binds_the_run(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                got = self._enforce(root, HOSTING_DECLARED)
        self.assertEqual(got["account"], "xFactor001@opensoft.one")
        self.assertEqual(sync._BOUND_PROFILE, "company",
                         "a bound run must pin the profile it verified")

    def test_an_undeclared_install_releases_the_pin(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            sync.bind_profile("stale")
            with contextlib.redirect_stdout(io.StringIO()):
                sync.enforce_hosting_profile(
                    root, runner=_profile_runner("personal"))
        self.assertIsNone(sync._BOUND_PROFILE)

    def test_a_self_hosted_personal_declaration_is_accepted(self):
        text = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: self_hosted
  account: someone@gmail.com
  nlm_profile: personal
share_out: []
"""
        with TemporaryDirectory() as td:
            root = Path(td)
            with contextlib.redirect_stdout(io.StringIO()):
                got = self._enforce(root, text, active="personal")
        self.assertEqual(got["case"], "self_hosted",
                         "an individual's own account is a complete binding")

    def test_nlm_itself_reasserts_the_binding_before_running(self):
        """The wire, not just the check.

        `assert_still_bound()` is only worth anything if `nlm()` calls it: a
        drift detector nothing invokes is decoration. Asserted by driving the
        REAL `nlm()` with a drifted config and a stubbed subprocess, so the
        refusal must come from the binding rather than from the CLI.
        """
        with TemporaryDirectory() as td:
            path = Path(td) / "config.toml"
            path.write_text('[auth]\ndefault_profile = "someone-else"\n',
                            encoding="utf-8")
            ran = []
            with patch.object(sync, "NLM_CONFIG", path), \
                 patch.object(sync.subprocess, "run",
                              lambda *a, **k: ran.append(a)):
                sync._CONFIG_CACHE = None
                sync.bind_profile("company")
                with self.assertRaises(SystemExit) as caught:
                    sync.nlm("notebook", "list", "--json")
        self.assertIn("changed mid-run", str(caught.exception))
        self.assertEqual(ran, [], "the invocation must be refused BEFORE the "
                                  "subprocess, not after it has written")


class UnreadableDeclarationFailsClosedTests(unittest.TestCase):
    """A declaration the sync cannot read is NOT an absent one.

    Found in review: the narrow reader wants the `hosting:` block's own
    two-space scalars. Flow style, four-space indentation and tabs are all
    valid YAML — the validator passes them — and all yielded nothing here, so
    the run took the UNDECLARED branch, bound nothing, and left
    `assert_still_bound()` a no-op for the whole job.
    """

    def tearDown(self):
        sync.bind_profile(None)

    FLOW = ("schema_version: 1\nkind: notebook_projection_hosting\n"
            "hosting: {case: operator_hosted, account: x@opensoft.one, "
            "nlm_profile: company}\nshare_out: []\n")
    FOUR = ("schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n"
            "    case: operator_hosted\n    account: x@opensoft.one\n"
            "    nlm_profile: company\nshare_out: []\n")
    TABS = ("schema_version: 1\nkind: notebook_projection_hosting\nhosting:\n"
            "\tcase: operator_hosted\n\taccount: x@opensoft.one\n"
            "\tnlm_profile: company\nshare_out: []\n")

    def test_an_existing_file_always_yields_a_dict_never_none(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, self.FLOW)
            got = sync.read_hosting_declaration(root)
        self.assertEqual(got, {}, "present-but-unparsed must be distinguishable "
                                  "from absent")

    def test_an_absent_file_is_the_only_undeclared_case(self):
        with TemporaryDirectory() as td:
            self.assertIsNone(sync.read_hosting_declaration(Path(td)))

    def test_each_unreadable_shape_refuses_instead_of_running_unbound(self):
        for label, text in (("flow", self.FLOW), ("four-space", self.FOUR),
                            ("tabs", self.TABS)):
            with self.subTest(shape=label), TemporaryDirectory() as td:
                root = Path(td)
                _declare_hosting(root, text)
                with self.assertRaises(SystemExit) as caught:
                    sync.enforce_hosting_profile(
                        root, runner=_profile_runner("personal"))
                self.assertIn("no declaration could be read",
                              str(caught.exception))


class MigrationStateVocabularyTests(unittest.TestCase):
    """The sync owns the state vocabulary too — one rule, not two gates.

    Found in review: `state: in_progress` FAILED the validator and PASSED the
    sync, which then bound the DECLARED profile while the books were still in
    the previous account — a premature migration under `--apply`.
    """

    def tearDown(self):
        sync.bind_profile(None)

    BASE = """schema_version: 1
kind: notebook_projection_hosting
hosting:
  case: operator_hosted
  account: xFactor001@opensoft.one
  account_type: google_workspace_user
  domain: opensoft.one
  nlm_profile: company
  migration:
    state: {state}
    from_account: brettheap@gmail.com
    from_nlm_profile: personal
share_out: []
"""

    def _enforce(self, text: str, active: str):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, text)
            with contextlib.redirect_stdout(io.StringIO()):
                return sync.enforce_hosting_profile(
                    root, runner=_profile_runner(active))

    def test_an_unrecognized_state_is_refused(self):
        with self.assertRaises(SystemExit) as caught:
            self._enforce(self.BASE.format(state="in_progress"), "company")
        self.assertIn("migration.state", str(caught.exception))

    def test_pending_and_complete_are_both_accepted(self):
        self.assertIsNotNone(
            self._enforce(self.BASE.format(state="pending"), "personal"))
        self.assertIsNotNone(
            self._enforce(self.BASE.format(state="complete"), "company"))

    def test_a_pending_migration_without_a_from_profile_is_refused(self):
        text = self.BASE.format(state="pending").replace(
            "    from_nlm_profile: personal\n", "")
        with self.assertRaises(SystemExit) as caught:
            self._enforce(text, "personal")
        self.assertIn("from_nlm_profile", str(caught.exception))

    def test_the_top_level_profile_is_required_even_while_pending(self):
        text = self.BASE.format(state="pending").replace(
            "  nlm_profile: company\n", "")
        with self.assertRaises(SystemExit) as caught:
            self._enforce(text, "personal")
        self.assertIn("no top-level nlm_profile", str(caught.exception))


class ProfileAccountIsCheckedWhenTheCliRecordedOneTests(unittest.TestCase):
    """The CLI DOES store a profile's email — this change first claimed it did not.

    `profiles/<name>/metadata.json` carries `email`: populated by a recent
    login, left null by an older one. Null means UNKNOWN and is reported; a
    populated address that disagrees with the declaration is a refusal.
    """

    def tearDown(self):
        sync.bind_profile(None)

    @staticmethod
    def _home(root: Path, profile: str, email) -> Path:
        home = root / "cli-home"
        d = home / "profiles" / profile
        d.mkdir(parents=True)
        body = "null" if email is None else f'"{email}"'
        (d / "metadata.json").write_text('{"email": %s}' % body,
                                         encoding="utf-8")
        return home

    def test_a_recorded_address_is_read(self):
        with TemporaryDirectory() as td:
            home = self._home(Path(td), "company", "xFactor001@opensoft.one")
            self.assertEqual(sync.profile_account("company", home=home),
                             "xFactor001@opensoft.one")

    def test_a_null_address_is_unknown_not_empty_string(self):
        with TemporaryDirectory() as td:
            home = self._home(Path(td), "company", None)
            self.assertIsNone(sync.profile_account("company", home=home))

    def test_a_missing_profile_directory_is_unknown(self):
        with TemporaryDirectory() as td:
            self.assertIsNone(
                sync.profile_account("nope", home=Path(td) / "cli-home"))

    def test_the_right_profile_name_signed_in_as_the_wrong_account_refuses(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_DECLARED)
            home = self._home(root, "company", "someone-else@elsewhere.test")
            # the REAL reader, pointed at a synthetic CLI home
            real = functools.partial(sync.profile_account, home=home)
            with patch.object(sync, "profile_account", real):
                with self.assertRaises(SystemExit) as caught:
                    sync.enforce_hosting_profile(
                        root, runner=_profile_runner("company"))
        message = str(caught.exception)
        self.assertIn("signed in as someone-else@elsewhere.test", message)
        self.assertIn("nlm login --profile company", message)

    def test_an_unknown_address_is_reported_not_treated_as_a_mismatch(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            _declare_hosting(root, HOSTING_DECLARED)
            out = io.StringIO()
            with patch.object(sync, "profile_account", lambda *a, **k: None):
                with contextlib.redirect_stdout(out):
                    got = sync.enforce_hosting_profile(
                        root, runner=_profile_runner("company"))
        self.assertIsNotNone(got, "an older login that recorded no address must "
                                  "not block the run")
        self.assertIn("records no account address", out.getvalue())


# ---------------------------------------------------------------------------
# add-projection-title-uniqueness — the title derivation is INJECTIVE.
#
# A source title is the projection's identity key: `scan()` derives a set keyed
# by document PATH and `sync_book()` reconciles it against a live book BY
# TITLE, holding each title at one source. Until 2026-08-25 the derivation
# special-cased the literal filename `README` and let everything else fall
# through to a bare stem, so four MedxFactory staging topics shared one source
# while the manifest recorded four documents as synced.
# ---------------------------------------------------------------------------

# `design.md` § 6's enumeration, transcribed row for row:
# (book, relpath, status, title BEFORE this change, title AFTER).
# The apply that migrated the live books was diffed against this list, so a
# derivation change that moves any of these fourteen rows must move this
# constant too, in front of a reader.
TITLE_MIGRATION = [
    ("canon", "openxFactory/contracts/memory-gateway/README.md", "standard",
     "[standard] openxFactory: memory-gateway/README",
     "[standard] openxFactory: contracts/memory-gateway/README"),
    ("canon", "xFactories/LedgerxFactory/docs/company-provisioning.md",
     "ratified",
     "[ratified] LedgerxFactory: company-provisioning",
     "[ratified] LedgerxFactory: docs/company-provisioning"),
    ("drafts", "openxFactory/examples/memory-gateway/README.md", "draft",
     "[draft] openxFactory: memory-gateway/README",
     "[draft] openxFactory: examples/memory-gateway/README"),
    ("drafts",
     "openxFactory/specs/005-customer-subject-runtime/checklists/"
     "requirements.md", "draft",
     "[draft] openxFactory: requirements",
     "[draft] openxFactory: 005-customer-subject-runtime/checklists/"
     "requirements"),
    ("drafts",
     "openxFactory/specs/007-client-identity-roster/checklists/"
     "requirements.md", "draft",
     "[draft] openxFactory: requirements",
     "[draft] openxFactory: 007-client-identity-roster/checklists/"
     "requirements"),
    ("ideation-ledgerxfactory",
     "xFactories/LedgerxFactory/ideation/staging/company-provisioning/"
     "company-provisioning.md", "staged",
     "[staged] LedgerxFactory: company-provisioning",
     "[staged] LedgerxFactory: company-provisioning/company-provisioning"),
    ("ideation-medxfactory",
     "xFactories/MedxFactory/ideation/staging/root-truth-grounding/topic.md",
     "staged",
     "[staged] MedxFactory: topic",
     "[staged] MedxFactory: root-truth-grounding/topic"),
    ("ideation-medxfactory",
     "xFactories/MedxFactory/ideation/staging/root-truth-target-claims/"
     "topic.md", "staged",
     "[staged] MedxFactory: topic",
     "[staged] MedxFactory: root-truth-target-claims/topic"),
    ("ideation-medxfactory",
     "xFactories/MedxFactory/ideation/staging/terminology-normalization/"
     "topic.md", "staged",
     "[staged] MedxFactory: topic",
     "[staged] MedxFactory: terminology-normalization/topic"),
    ("ideation-medxfactory",
     "xFactories/MedxFactory/ideation/staging/treatment-plan-generation/"
     "topic.md", "staged",
     "[staged] MedxFactory: topic",
     "[staged] MedxFactory: treatment-plan-generation/topic"),
    ("ideation-openxfactory",
     "openxFactory/ideation/brainstorm/"
     "codexfactory-domain-hermes-content.md", "brainstorm",
     "[brainstorm] openxFactory: codexfactory-domain-hermes-content",
     "[brainstorm] openxFactory: brainstorm/"
     "codexfactory-domain-hermes-content"),
    ("ideation-openxfactory",
     "openxFactory/ideation/staging/codexfactory-domain-hermes-content/"
     "codexfactory-domain-hermes-content.md", "staged",
     "[staged] openxFactory: codexfactory-domain-hermes-content",
     "[staged] openxFactory: codexfactory-domain-hermes-content/"
     "codexfactory-domain-hermes-content"),
    ("ideation-opsxfactory",
     "xFactories/OpsxFactory/ideation/brainstorm/"
     "exchange-execution-bringup.md", "staged",
     "[staged] OpsxFactory: exchange-execution-bringup",
     "[staged] OpsxFactory: brainstorm/exchange-execution-bringup"),
    ("ideation-opsxfactory",
     "xFactories/OpsxFactory/ideation/staging/exchange-execution-bringup/"
     "exchange-execution-bringup.md", "staged",
     "[staged] OpsxFactory: exchange-execution-bringup",
     "[staged] OpsxFactory: exchange-execution-bringup/"
     "exchange-execution-bringup"),
]

# Documents that are NOT in the migration and must not move, each one a scope
# claim: a lone `topic.md` stays bare (the rule qualifies on collision, never
# pre-emptively), a unique README keeps its parent-directory floor, a
# repository-root README keeps the repository as its parent, a `record`
# document qualifies nobody because it projects nowhere, and a stem that
# matches a promoted capability name is not qualified by the `[spec]` family.
TITLE_UNMOVED = [
    ("xFactories/OpsxFactory/ideation/staging/opensoft-tenant-governance/"
     "topic.md", "staged", "[staged] OpsxFactory: topic"),
    ("xFactories/OpsxFactory/ideation/README.md", "ratified",
     "[ratified] OpsxFactory: ideation/README"),
    ("xFactories/OpsxFactory/README.md", "standard",
     "[standard] OpsxFactory: OpsxFactory/README"),
    ("openxFactory/docs/lifecycle-notebook-projection.md", "standard",
     "[standard] openxFactory: lifecycle-notebook-projection"),
]

# A `record` document is scanned and projected by no book, so it is outside the
# uniqueness scope: it must not push the standard document below into a
# qualifier it does not need.
RECORD_NAMESAKE = ("openxFactory/ideation/gate-records/"
                   "lifecycle-notebook-projection.md", "record")


def _legacy_stem(rel: str) -> str:
    """The derivation this change replaced, kept so the BEFORE column of
    TITLE_MIGRATION is produced rather than transcribed twice."""
    path = Path(rel)
    return (f"{path.parent.name}/{path.stem}"
            if path.stem.lower() == "readme" else path.stem)


def _bare_stem_derivation(documents):
    """Mutation (i): the pre-2026-08-25 derivation, with even the README floor
    removed. Nothing may pass under this."""
    return {rel: segs[-1] for rel, _repo, segs in documents}


def _one_level_derivation(documents):
    """Mutation (ii): candidate (b1), always `<parent>/<stem>`. Looks like a
    fix and leaves `checklists/requirements` colliding with itself — the
    platform-inert class in disguise, where the changed code yields an equal
    value."""
    return {rel: "/".join(segs[-2:]) for rel, _repo, segs in documents}


class TitleUniquenessTests(unittest.TestCase):
    """One projected document, one source — asserted over the derived set."""

    @staticmethod
    def _write(root: Path, rel: str, status: str) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {Path(rel).stem}\n\nStatus: {status}\n",
                        encoding="utf-8")

    @classmethod
    def _world(cls, root: Path) -> None:
        """The three real collision shapes plus the latent README pair, at
        their real paths (§ 3.1): four documents sharing a stem inside one
        directory family; two whose PARENT directories match as well; a pair
        split across two directory families; and a same-stem pair kept apart
        today only by a status difference."""
        (root / "openxFactory").mkdir(parents=True, exist_ok=True)
        for grounding in sync.GROUNDING:
            cls._write(root, grounding, "standard")
        for _book, rel, status, _before, _after in TITLE_MIGRATION:
            cls._write(root, rel, status)
        for rel, status, _title in TITLE_UNMOVED:
            cls._write(root, rel, status)
        cls._write(root, *RECORD_NAMESAKE)
        promoted = root / "openxFactory/openspec/specs/ideation-dashboard"
        promoted.mkdir(parents=True, exist_ok=True)
        (promoted / "spec.md").write_text("# Spec\n\nStatus: ratified\n",
                                          encoding="utf-8")

    @staticmethod
    def _documents(root: Path):
        """(relpath, repository, segments) for every projected document —
        the input `scan()` hands the derivation."""
        desired, _specs = sync.scan(root)
        rels = {rel for book in desired.values() for rel in book}
        out = []
        for rel in sorted(rels):
            parts = Path(rel).parts
            repo = parts[1] if parts[0] == "xFactories" else parts[0]
            out.append((rel, repo, sync.title_segments(Path(rel))))
        return out

    def test_the_fourteen_enumerated_titles_move_exactly_as_designed(self):
        """§ 3.1 — the migration is checked against a list, not trusted."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, _specs = sync.scan(root)
            for book, rel, status, before, after in TITLE_MIGRATION:
                self.assertEqual(f"[{status}] "
                                 f"{before.split(']', 1)[1].split(':', 1)[0].strip()}"
                                 f": {_legacy_stem(rel)}", before,
                                 f"the BEFORE column of {rel} is not what the "
                                 f"replaced derivation produced")
                self.assertIn(rel, desired[book], f"{rel} left book {book}")
                self.assertEqual(desired[book][rel], after,
                                 f"{rel} did not land on design.md § 6's title")
                self.assertNotEqual(desired[book][rel], before,
                                    f"{rel} was enumerated as a rename")

    def test_documents_outside_the_migration_keep_their_titles(self):
        """The rule qualifies on collision. Nothing else moves — including the
        five scope claims in TITLE_UNMOVED."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, _specs = sync.scan(root)
            titles = {rel: title
                      for book in desired.values()
                      for rel, title in book.items()}
            for rel, _status, expected in TITLE_UNMOVED:
                self.assertEqual(titles[rel], expected)

    def _assert_injective(self, desired) -> None:
        """§ 3.2 — the assertion whose absence let the class exist.

        Written over the DERIVED set, never over an expected-title table, so a
        future derivation cannot satisfy it by agreeing with itself. One
        method so the mutation check below runs THIS assertion rather than a
        paraphrase of it.
        """
        self.assertTrue(desired, "a fixture that derives nothing proves "
                                 "injectivity vacuously")
        for book, items in desired.items():
            self.assertEqual(
                len(set(items.values())), len(items),
                f"book {book} derives fewer titles than it has documents: "
                f"the shortfall is documents the book cannot hold")

    def test_every_book_derives_one_title_per_document(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            self._assert_injective(sync.scan(root)[0])

    def test_a_status_change_moves_no_other_title(self):
        """§ 3.3 — the repository-scope choice, pinned structurally.

        Under a (book, status) scope the two `memory-gateway/README`
        documents are qualified only while their statuses differ, so flipping
        one moves the other's title and this test reds. That is the point.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            before, _specs = sync.scan(root)
            before_titles = {rel: title
                             for book in before.values()
                             for rel, title in book.items()}
            moved = "openxFactory/examples/memory-gateway/README.md"
            self._write(root, moved, "standard")
            after, _specs = sync.scan(root)
            after_titles = {rel: title
                            for book in after.values()
                            for rel, title in book.items()}
            for rel, title in before_titles.items():
                if rel == moved:
                    continue
                self.assertEqual(after_titles.get(rel), title,
                                 f"{rel} was retitled by another document's "
                                 f"Status: header")
            self.assertEqual(after_titles[moved],
                             "[standard] openxFactory: examples/memory-gateway/"
                             "README",
                             "the moved document keeps its own qualifier; only "
                             "its status prefix changes")

    def test_a_unique_readme_still_carries_its_parent_directory(self):
        """§ 3.5 — the FLOOR. The amendment never SHORTENS a title, including
        for a repository-root README whose parent IS the repository."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, _specs = sync.scan(root)
            titles = {rel: title
                      for book in desired.values()
                      for rel, title in book.items()}
            for rel, title in titles.items():
                if Path(rel).stem.lower() != "readme":
                    continue
                stem = title.split(": ", 1)[1]
                self.assertGreaterEqual(
                    len(stem.split("/")), 2,
                    f"{rel} lost its parent-directory floor")
                self.assertEqual(stem.split("/")[-2:],
                                 _legacy_stem(rel).split("/"),
                                 f"{rel}'s floor is not the title the replaced "
                                 f"rule produced")

    def test_the_spec_and_grounding_families_are_outside_the_scope(self):
        """§ 2.2 — the exclusion is measured, not a convenience.

        `[spec]` is keyed by a promoted capability's DIRECTORY name and
        `[grounding]` by a fixed document set. Folding either into the
        uniqueness scope over-qualified a title for no reason.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            # a governance document whose stem is the promoted capability's
            # directory name: two families, one spelling, no collision
            self._write(root, "openxFactory/docs/ideation-dashboard.md",
                        "standard")
            desired, _specs = sync.scan(root)
            canon = desired["canon"]
            self.assertIn("[spec] openxFactory: ideation-dashboard",
                          canon.values())
            self.assertEqual(
                canon["openxFactory/docs/ideation-dashboard.md"],
                "[standard] openxFactory: ideation-dashboard",
                "a `[spec]` title must not qualify a `[status]` one")
            for family in sync.STEM_SCOPE_EXCLUDES:
                self.assertTrue(
                    any(t.startswith(family) for t in canon.values()),
                    f"the fixture must exercise the {family} family it "
                    f"claims to hold outside the scope")
            grounding = [t for book in desired.values() for t in book.values()
                         if t.startswith("[grounding]")]
            self.assertTrue(grounding)
            for title in grounding:
                self.assertNotIn("/", title.split(": ", 1)[1],
                                 "the grounding set is keyed by a fixed "
                                 "document list, never qualified")

    def test_a_record_document_qualifies_nobody(self):
        """The scope is the PROJECTED set. A `record` document reaches no book,
        so it cannot cost a projected namesake its bare stem."""
        rel, _status = RECORD_NAMESAKE
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            desired, _specs = sync.scan(root)
            placed = [book for book, items in desired.items() if rel in items]
            self.assertEqual(placed, [], "a record document projects nowhere")
            self.assertEqual(
                desired["canon"]["openxFactory/docs/"
                                 "lifecycle-notebook-projection.md"],
                "[standard] openxFactory: lifecycle-notebook-projection")

    def test_titles_are_derived_from_structure_not_from_a_rendered_path(self):
        """§ 3.6 (iii) — a `str(Path)` or separator substitution is inert on
        POSIX against a value-equality check, so assert the STRUCTURE."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            documents = self._documents(root)
            segments = dict((rel, segs) for rel, _repo, segs in documents)
            checklist = ("openxFactory/specs/005-customer-subject-runtime/"
                         "checklists/requirements.md")
            self.assertEqual(
                segments[checklist],
                ("openxFactory", "specs", "005-customer-subject-runtime",
                 "checklists", "requirements"))
            for rel, segs in segments.items():
                self.assertIsInstance(segs, tuple, f"{rel}")
                for part in segs:
                    self.assertIsInstance(part, str, f"{rel}")
                    self.assertNotIn("/", part, f"{rel}: a segment is a path")
                    self.assertNotIn("\\", part, f"{rel}: a segment is a path")
            stems = sync.derive_stems(documents)
            self.assertEqual(
                stems[checklist].split("/"),
                ["005-customer-subject-runtime", "checklists", "requirements"],
                "the qualifier is three segments deep because two segments "
                "still collide")

    def test_reverting_the_rule_to_a_bare_stem_reds_the_injectivity_check(self):
        """§ 3.6 (i) — an assertion that passes against the defective
        derivation is not the assertion."""
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            with patch.object(sync, "derive_stems", _bare_stem_derivation):
                desired, _specs = sync.scan(root)
            with self.assertRaises(AssertionError):
                self._assert_injective(desired)
            offenders = {book: len(items) - len(set(items.values()))
                         for book, items in desired.items()
                         if len(set(items.values())) != len(items)}
            self.assertEqual(
                sorted(offenders), ["drafts", "ideation-medxfactory",
                                    "ideation-opsxfactory"],
                "the fixture must reproduce the three real collisions when the "
                "rule is reverted")
            self.assertEqual(sum(offenders.values()), 5,
                             "five documents were displaced in the live books")

    def test_a_one_level_qualifier_leaves_the_checklists_pair_colliding(self):
        """§ 3.6 (ii) — candidate (b1) is eliminated on CORRECTNESS.

        Both checklist documents live in a directory named `checklists`, so
        `<parent>/<stem>` collides with itself. 572 renames and the defect
        survives; a one-level qualifier is a longer version of the same
        assumption, not a fix.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            self._world(root)
            with patch.object(sync, "derive_stems", _one_level_derivation):
                desired, _specs = sync.scan(root)
            drafts = desired["drafts"]
            self.assertNotEqual(
                len(set(drafts.values())), len(drafts),
                "a one-level qualifier must still collapse the checklist pair")
            self.assertEqual(
                drafts["openxFactory/specs/005-customer-subject-runtime/"
                       "checklists/requirements.md"],
                drafts["openxFactory/specs/007-client-identity-roster/"
                       "checklists/requirements.md"])
            # and the real rule does not
            desired, _specs = sync.scan(root)
            drafts = desired["drafts"]
            self.assertEqual(len(set(drafts.values())), len(drafts))


class ParityProvesDocumentsTests(unittest.TestCase):
    """§ 3.4 — the check that could not see the defect it existed to catch."""

    def _run_parity(self, root: Path, fake) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            with patch.object(sync, "nlm", fake):
                code = sync.parity_report(root)
        return code, out.getvalue()

    @staticmethod
    def _books_holding(root: Path, desired, specs):
        """A live account whose bracket-titled sources are EXACTLY the derived
        title set — the state the old parity called OK."""
        fake = FakeNlm([{"id": f"nb{i}", "title": specs[k].title}
                        for i, k in enumerate(sorted(desired))])
        for i, key in enumerate(sorted(desired)):
            fake.sources[f"nb{i}"] = [
                {"id": f"s{i}-{j}", "title": title}
                for j, title in enumerate(sorted(set(desired[key].values())))]
        return fake

    def test_a_collapsed_title_fails_parity_though_the_title_sets_are_equal(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            TitleUniquenessTests._world(root)
            with patch.object(sync, "derive_stems", _bare_stem_derivation):
                desired, specs = sync.scan(root)
                fake = self._books_holding(root, desired, specs)
                for key, items in desired.items():
                    self.assertEqual(
                        {r.get("title") for r in fake.sources_of(specs[key].title)},
                        set(items.values()),
                        "the fixture must put the live book at TITLE-set "
                        "equality, which is the state the old check passed")
                code, text = self._run_parity(root, fake)
        self.assertEqual(code, 1, "a book missing five documents is not at "
                                  "parity, however equal its title sets are")
        self.assertIn("carry more than one document", text)
        self.assertIn("COLLAPSED", text)
        self.assertIn("xFactories/MedxFactory/ideation/staging/"
                      "root-truth-grounding/topic.md", text)

    def test_the_injective_derivation_proves_parity_over_documents(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            TitleUniquenessTests._world(root)
            desired, specs = sync.scan(root)
            fake = self._books_holding(root, desired, specs)
            code, text = self._run_parity(root, fake)
        self.assertEqual(code, 0, text)
        self.assertIn("parity: PROVEN", text)
        self.assertIn("documents in", text)
        self.assertNotIn("COLLAPSED", text)
