"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from notebooklm_sync.nlm_client import ProviderResult
from opendox import branch_session as bs
from opendox import session_git as sg
from opendox import workbench as wb

from tests.notebooklm._session_test_support import (
    LIFECYCLE_BOOKS,
    SESSION_ALIAS,
    FakeNlm,
    fixture,
    notebook_import_sync,
)

sync = notebook_import_sync()


class SessionNotebookImportTests(unittest.TestCase):
    """T071 — a hybrid import lands in the origin folder INSIDE the worktree, on
    the branch, with the header contract and idempotency-by-source-id unchanged
    (FR-041)."""

    def scenario_an_import_lands_in_the_worktree_on_the_session_branch(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, worktree = fixture.session_world(root)
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root)
            )

            def fake_nlm(*args: str, parse: bool = True) -> ProviderResult:
                del parse
                if args[:2] == ("source", "list"):
                    return [{"id": "src-note", "title": "A converted note"}]
                if args == ("source", "content", "src-note"):
                    return "Session note body."
                raise AssertionError(args)

            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            with patch.object(sync, "nlm", fake_nlm):
                count = sync.import_new_sources(
                    root, alias, target_arg, True, "2026-07-26"
                )
            self.assertEqual(count, 1)

            landed = (
                worktree / "ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md"
            )
            self.assertTrue(landed.is_file())
            # INSIDE the worktree, on the session BRANCH — never on `main`
            self.assertEqual(
                fixture.git(worktree, "rev-parse", "--abbrev-ref", "HEAD"),
                "draft/demo-topic",
            )
            # LANDED, not merely written (FR-041, T071: "on the branch"). This
            # test used to pin the file as UNTRACKED, which locked in silent data
            # loss: it carries `Status: staged` under a governed root, so
            # `workbench.session_documents` includes it and it projects into the
            # notebook and the session's panels as live governed material — while
            # BOTH endings run `git worktree remove --force`, which deletes
            # untracked files outright (measured: PR #49 review finding 12).
            self.assertNotIn(
                "notebooklm-ideas-2026-07-26.md",
                fixture.git(worktree, "status", "--porcelain"),
            )
            self.assertIn(
                "notebooklm-ideas-2026-07-26.md",
                fixture.git(worktree, "show", "--name-only", "--format=", "HEAD"),
            )
            self.assertIn(
                "Source-Notebook: " + alias,
                fixture.git(worktree, "log", "-1", "--format=%B"),
            )
            # …and the commit carries ONLY the imported file: the governed commit
            # path binds it (`commit --only`), so a neighbouring modification in
            # the same worktree cannot ride along
            self.assertEqual(
                fixture.git(
                    worktree, "show", "--name-only", "--format=", "HEAD"
                ).split(),
                ["ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md"],
            )
            self.assertFalse(
                (
                    checkout
                    / "ideation/staging/demo-topic"
                    / "notebooklm-ideas-2026-07-26.md"
                ).exists()
            )

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
                again = sync.import_new_sources(
                    root, alias, target_arg, True, "2026-07-26"
                )
            self.assertEqual(again, 0)
            self.assertEqual(text, landed.read_text())

    def scenario_an_import_refuses_a_worktree_that_drifted_during_the_fetch(self) -> None:
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
            checkout, worktree = fixture.session_world(root)
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root)
            )
            before = fixture.git(checkout, "rev-parse", "draft/demo-topic")

            def fake_nlm(*args: str, parse: bool = True) -> ProviderResult:
                del parse
                if args[:2] == ("source", "list"):
                    return [{"id": "src-note", "title": "A converted note"}]
                if args == ("source", "content", "src-note"):
                    _ = fixture.git(
                        worktree, "checkout", "-q", "-b", "somebody-elses-branch"
                    )
                    return "Session note body."
                raise AssertionError(args)

            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            buf = io.StringIO()
            with (
                patch.object(sync, "nlm", fake_nlm),
                contextlib.redirect_stdout(buf),
            ):
                count = sync.import_new_sources(
                    root, alias, target_arg, True, "2026-07-26"
                )
            out = buf.getvalue()

            # the bytes are never lost: they were already written when the drift
            # was found, and the file stays in the worktree for the human
            self.assertEqual(count, 1)
            landed = (
                worktree / "ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md"
            )
            self.assertTrue(landed.is_file())
            # NOTHING was committed: not onto the drifted branch, and not onto the
            # session branch the report would otherwise have named
            self.assertEqual(
                fixture.git(checkout, "rev-parse", "draft/demo-topic"), before
            )
            self.assertEqual(
                fixture.git(worktree, "rev-parse", "somebody-elses-branch"), before
            )
            # ... and the report says so, naming the branch git actually holds
            self.assertNotIn("[session] COMMITTED", out)
            self.assertIn("NOT COMMITTED", out)
            self.assertIn("somebody-elses-branch", out)
            self.assertIn("UNTRACKED", out)

    def scenario_a_nested_factory_session_import_keeps_the_repository_name(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = fixture.session_world(
                root, repository="codexFactory", nested=True
            )
            target = sync.target_from_path(
                root, str((worktree / "ideation/staging/demo-topic").relative_to(root))
            )
            self.assertEqual(target.repo, "codexFactory")
            self.assertEqual(target.status, "staged")
            self.assertEqual(target.topic, "demo-topic")


class SessionNotebookQuotaTests(unittest.TestCase):
    """T072 — an exhausted quota DEGRADES the session, never blocks it, and the
    notice is honest about whose limit was hit (FR-042, D19)."""

    def _open(self, root: Path, adapter: wb.NotebookAdapter | None) -> bs.SessionOpen:
        """Open the session and then ATTACH its notebook — the two steps the
        gate action performs, in the order it performs them.

        The OPEN no longer creates the notebook (PR #49 review finding 3): a
        refused first create used to leave a real notebook on the shared account
        with no unwind, so the create is deferred to the first SUCCESSFUL commit
        and `attach_session_notebook` is that step. Everything asserted below —
        the degradation, the notice, the create-from-the-worktree — is unchanged;
        only WHEN it happens moved."""
        checkout = root / "openxFactory"
        fixture.seed_checkout(checkout, text=fixture.doc("main body"))
        git = sg.SessionGit(checkout)
        registry = fixture.registry()
        tile = bs.Tile("staged-topic", "demo-topic")
        session = bs.open_session(
            git,
            registry,
            repository="openxFactory",
            tile=tile,
            checkout_root=checkout,
            verb="create-document",
            notebook=adapter,
        )
        # the open itself creates NOTHING on the account, whatever the adapter
        self.assertIsNone(session.notebook_notice)
        self.assertFalse(session.notebook_created)
        return bs.attach_session_notebook(session)

    def scenario_an_exhausted_quota_still_opens_the_session(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            # three books already exist and the account holds no more
            fake = FakeNlm(LIFECYCLE_BOOKS, quota=3)
            adapter = wb.NotebookAdapter(fake, available=True)

            session = self._open(root, adapter)

            self.assertTrue(session.opened)
            self.assertTrue(Path(session.worktree).is_dir())
            self.assertEqual(session.branch, "draft/demo-topic")
            self.assertEqual(session.notebook_alias, SESSION_ALIAS)
            self.assertFalse(session.notebook_created)
            self.assertEqual(fake.titles(), ["xf-canon", "xf-drafts", "xf-ideation"])

    def scenario_the_notice_speaks_of_concurrent_tiles_across_everyone(self) -> None:
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
            for blame in (
                "your sessions",
                "sessions you",
                "too many",
                "you opened",
                "your limit",
            ):
                self.assertNotIn(blame, lowered, notice)
            # and it names the honest retry route (FR-040)
            self.assertIn("--session-ref draft/demo-topic", notice)

    def scenario_with_quota_room_the_session_opens_with_its_notebook(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            fake = FakeNlm(LIFECYCLE_BOOKS)
            adapter = wb.NotebookAdapter(fake, available=True)

            session = self._open(root, adapter)

            self.assertTrue(session.notebook_created)
            self.assertIsNone(session.notebook_notice)
            self.assertEqual(fake.created_titles(), [SESSION_ALIAS])
            # created FROM the worktree the open just made
            self.assertTrue(any("main body" in c for c in fake.added_contents()))

    def scenario_a_plane_with_no_adapter_creates_nothing_and_says_nothing(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            session = self._open(root, None)
            self.assertTrue(session.opened)
            self.assertFalse(session.notebook_created)
            self.assertIsNone(session.notebook_notice)
