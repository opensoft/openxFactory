"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
import unittest
from collections.abc import Sequence
from pathlib import Path
from tempfile import TemporaryDirectory

from notebooklm_sync.corpus import DesiredState
from opendox import branch_session as bs
from opendox import workbench as wb

from tests.notebooklm._session_test_support import (
    LIFECYCLE_BOOKS,
    SESSION_ALIAS,
    STAGED_DOC,
    SYNC_OP,
    FakeNlm,
    SessionNamespaceAdapter,
    SessionNamespaceFacade,
    fixture,
    refresh_sync,
)

sync = refresh_sync()


class SessionNotebookBookIsolationTests(unittest.TestCase):
    """T069 — NO lifecycle book ever contains a worktree-sourced document
    (FR-039), in addition to the existing `<repo>-worktrees/` exclusion."""

    def _assert_books_are_main_only(
        self, root: Path, worktrees: Sequence[Path]
    ) -> DesiredState:
        desired, _specs = sync.scan(root)
        polluted = [
            path
            for book in desired.values()
            for path in book
            if "-worktrees" in path or "sessions/" in path
        ]
        self.assertEqual(polluted, [])
        for worktree in worktrees:
            rel = worktree.relative_to(root).as_posix()
            for book, items in desired.items():
                for path in items:
                    self.assertFalse(
                        path.startswith(rel), f"{book} took a worktree source: {path}"
                    )
        repos = {
            title.split("] ", 1)[1].split(":", 1)[0]
            for book in desired.values()
            for title in book.values()
            if "] " in title and ":" in title
        }
        for repo in repos:
            self.assertFalse(repo.endswith("-worktrees"), repo)
        return desired

    def scenario_session_worktrees_are_outside_every_book_with_pins_present(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _, openx_wt = fixture.session_world(root, repository="openxFactory")
            _, factory_wt = fixture.session_world(
                root, repository="codexFactory", nested=True
            )
            _ = (root / ".gitmodules").write_text(
                '[submodule "codexFactory"]\n'
                + "\tpath = xFactories/codexFactory\n"
                + "\turl = https://example.invalid/codexFactory.git\n",
                encoding="utf-8",
            )
            self.assertEqual(
                sync.pinned_factory_paths(root), ["xFactories/codexFactory"]
            )
            desired = self._assert_books_are_main_only(root, [openx_wt, factory_wt])
            # the docs on `main` DO project — the exclusion is of the worktree,
            # not of the repository — and each repo's doc lands in ITS OWN
            # ideation book (split-ideation-book-per-repo)
            self.assertIn(
                f"openxFactory/{STAGED_DOC}", desired["ideation-openxfactory"]
            )
            self.assertIn(
                f"xFactories/codexFactory/{STAGED_DOC}",
                desired["ideation-codexfactory"],
            )
            self.assertNotIn(
                f"openxFactory/{STAGED_DOC}", desired["ideation-codexfactory"]
            )

    def scenario_session_worktrees_are_outside_every_book_without_pins(self) -> None:
        # the `.gitmodules`-absent fallback path of `pinned_factory_paths`
        with TemporaryDirectory() as td:
            root = Path(td)
            _, openx_wt = fixture.session_world(root, repository="openxFactory")
            _, factory_wt = fixture.session_world(
                root, repository="codexFactory", nested=True
            )
            self.assertNotIn(
                "xFactories/codexFactory-worktrees", sync.pinned_factory_paths(root)
            )
            _ = self._assert_books_are_main_only(root, [openx_wt, factory_wt])

    def scenario_a_session_source_set_and_a_book_share_no_document(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _, worktree = fixture.session_world(root)
            target = sync.resolve_session_target(root, "draft/demo-topic")
            session_paths = {
                str(worktree.relative_to(root) / path)
                for path, _text in sync.session_source_set(target)
            }
            book_paths = {path for book in sync.scan(root)[0].values() for path in book}
            self.assertTrue(session_paths)
            self.assertEqual(session_paths & book_paths, set())


class SessionNotebookRefreshTests(unittest.TestCase):
    """T070 — refresh re-syncs FROM the worktree; session end RETIRES the
    notebook and never re-points it at `main` (FR-036, FR-040, D16)."""

    def scenario_refresh_resyncs_from_the_worktree_without_recreating(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = fixture.session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            alias = SESSION_ALIAS

            _ = sync.sync_session_notebook(
                root, "draft/demo-topic", apply=True, adapter=adapter
            )
            first = fake.notebook_id(alias)
            self.assertEqual(len(fake.sources_of(alias)), 1)

            # an unchanged re-sync is a no-op (title + content hash diff)
            _ = sync.sync_session_notebook(
                root, "draft/demo-topic", apply=True, adapter=adapter
            )
            self.assertEqual(fake.created_titles(), [alias])
            self.assertEqual(len(fake.added_contents()), 1)

            # the worktree moves on; the refresh follows IT
            _ = (worktree / STAGED_DOC).write_text(
                fixture.doc("second worktree body"), encoding="utf-8"
            )
            _ = sync.sync_session_notebook(
                root, "draft/demo-topic", apply=True, adapter=adapter
            )
            self.assertEqual(fake.notebook_id(alias), first)
            self.assertEqual(len(fake.sources_of(alias)), 1)
            self.assertIn("second worktree body", fake.sources_of(alias)[0]["content"])
            self.assertFalse(any("main body" in c for c in fake.added_contents()))

    def scenario_the_dry_run_prints_a_plan_touches_nothing_and_is_not_book_drift(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = fixture.session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                result = sync.sync_session_notebook(
                    root, "draft/demo-topic", apply=False, adapter=adapter
                )
            out = buf.getvalue()
            self.assertFalse(result.applied)
            self.assertEqual(fake.created_titles(), [])
            self.assertEqual(fake.added_contents(), [])
            self.assertIn(SESSION_ALIAS, out)
            for line in out.splitlines():
                self.assertIsNone(SYNC_OP.match(line), line)

    def scenario_session_end_retires_the_notebook_and_never_repoints_it_at_main(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = fixture.session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            alias = SESSION_ALIAS
            _ = sync.sync_session_notebook(
                root, "draft/demo-topic", apply=True, adapter=adapter
            )
            created = fake.notebook_id(alias)

            result = sync.sync_session_notebook(
                root, "draft/demo-topic", apply=True, adapter=adapter, retire=True
            )

            self.assertTrue(result.retired)
            self.assertEqual(fake.deleted_ids(), [created])
            self.assertIsNone(fake.notebook(alias))
            # RETIRED, never re-pointed at `main` (D16): nothing was created
            # again and no source was ever added from the served checkout
            self.assertEqual(fake.created_titles(), [alias])
            self.assertFalse(any("main body" in c for c in fake.added_contents()))
            # the three lifecycle books are untouched by an ending
            self.assertEqual(fake.titles(), ["xf-canon", "xf-drafts", "xf-ideation"])

    def scenario_the_teardown_seam_retires_through_the_real_adapter(self) -> None:
        # `branch_session.retire_session_notebook` is what BOTH endings call
        # (FR-021); with the nlm-backed adapter injected it must really remove
        # the xf-session-* notebook, not report a benign no-op.
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = fixture.session_world(root)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)
            alias = SESSION_ALIAS
            _ = sync.sync_session_notebook(
                root, "draft/demo-topic", apply=True, adapter=adapter
            )
            retired, detail = bs.retire_session_notebook(
                adapter, repository="openxFactory", branch="draft/demo-topic"
            )
            self.assertTrue(retired, detail)
            self.assertIsNone(fake.notebook(alias))

    def scenario_retire_refuses_to_cross_into_the_reference_set_namespace(self) -> None:
        fake = FakeNlm([{"id": "w1", "title": "xf-wb-alpha"}])
        adapter = wb.NotebookAdapter(fake, available=True)
        assert isinstance(adapter, SessionNamespaceAdapter)
        namespace_adapter = SessionNamespaceFacade(adapter)
        with self.assertRaises(wb.WorkbenchError):
            _ = namespace_adapter.retire("xf-wb-alpha")
        with self.assertRaises(wb.WorkbenchError):
            _ = namespace_adapter.create_session("xf-wb-alpha")
        self.assertEqual(fake.deleted_ids(), [])
