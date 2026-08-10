"""Tests for NotebookLM lifecycle sync and source import helpers.

The `SessionNotebook*` classes at the bottom are Phase 8 of
007-workbench-branch-sessions (T067-T072): the `xf-session-*` notebook that
follows a branch session's WORKTREE. Every one of them drives a STUBBED `nlm`
runner — no test in this file may create a real notebook or invoke the real
`nlm` binary (FR-043).
"""

from __future__ import annotations

import contextlib
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
            # the three lifecycle books are untouched by an ending
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
            # three books already exist and the account holds no more
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
