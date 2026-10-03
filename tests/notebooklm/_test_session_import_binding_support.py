"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import unittest
from collections.abc import Mapping, Sequence
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TypedDict
from unittest.mock import patch

from notebooklm_sync.models import SessionNotebookRefused
from notebooklm_sync.nlm_client import JsonValue, ProviderResult
from opendox import branch_session as bs
from opendox import workbench as wb

from tests.notebooklm._session_test_support import (
    STAGED_DOC,
    NlmCall,
    fixture,
    import_binding_sync,
)


class SourceRow(TypedDict):
    id: str
    title: str


sync = import_binding_sync()


class SessionImportBindingTests(unittest.TestCase):
    """PR #49 review finding 12 — the session source-return import is BOUND to
    the exact live session, lands through the governed commit path, cannot feed
    itself, and never reads a directory alone as liveness.

    Every test here was written against the pre-fix script and fails on it. No
    real `nlm`: `sync.nlm` is patched at every call site, and
    `tests/hermeticity.py` makes the binary unreachable besides (FR-043)."""

    def _nlm(
        self,
        sources: Sequence[SourceRow],
        contents: Mapping[str, str] | None = None,
    ) -> NlmCall:
        contents = contents or {}

        def fake_nlm(*args: str, parse: bool = True) -> ProviderResult:
            del parse
            if args[:2] == ("source", "list"):
                listed: list[JsonValue] = [
                    {"id": source["id"], "title": source["title"]} for source in sources
                ]
                return listed
            if args[:2] == ("source", "content"):
                return contents.get(args[2], "Session note body.")
            raise AssertionError(args)

        return fake_nlm

    def _import(
        self,
        root: Path,
        notebook: str,
        target_arg: str,
        sources: Sequence[SourceRow],
        contents: Mapping[str, str] | None = None,
    ) -> int:
        with patch.object(sync, "nlm", self._nlm(sources, contents)):
            return sync.import_new_sources(
                root, notebook, target_arg, True, "2026-07-26"
            )

    def scenario_a_session_notebook_cannot_import_into_the_served_checkout(self) -> None:
        """The single most likely human slip: the ORDINARY import spelling, one
        path segment shorter than quickstart step 7's. It landed an unmerged
        session's notebook synthesis in the SERVED MAIN checkout — which FR-004
        forbids any session operation from touching, and which `scan()` then picks
        up as a lifecycle-book source, breaching FR-039's main-only rule."""
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, _worktree = fixture.session_world(root)
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")

            with self.assertRaises(SessionNotebookRefused) as caught:
                _ = self._import(
                    root,
                    alias,
                    "openxFactory/ideation/staging/demo-topic",
                    [{"id": "src-note", "title": "A converted note"}],
                )

            self.assertIn("not inside it", str(caught.exception))
            self.assertFalse(
                (
                    checkout
                    / "ideation/staging/demo-topic"
                    / "notebooklm-ideas-2026-07-26.md"
                ).exists()
            )
            self.assertEqual(fixture.git(checkout, "status", "--porcelain"), "")

    def scenario_a_session_notebook_cannot_import_into_another_sessions_worktree(
        self,
    ) -> None:
        """Session A's notebook pointed at session B's worktree wrote A's content
        onto B's branch, carrying A's `Source workspace:` header."""
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, _a = fixture.session_world(root)
            other = fixture.add_worktree(checkout, "draft/other-topic")
            _ = (other / STAGED_DOC).write_text(
                fixture.doc("other body"), encoding="utf-8"
            )
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            target_arg = str((other / "ideation/staging/demo-topic").relative_to(root))

            with self.assertRaises(SessionNotebookRefused):
                _ = self._import(
                    root,
                    alias,
                    target_arg,
                    [{"id": "src-note", "title": "A converted note"}],
                )

            self.assertEqual(
                list(
                    (other / "ideation/staging/demo-topic").glob(
                        "notebooklm-ideas-*.md"
                    )
                ),
                [],
            )

    def scenario_a_non_session_notebook_cannot_import_into_a_session_worktree(self) -> None:
        """The symmetric refusal: a session worktree holds ONE session's unmerged
        work, so another notebook's sources may not be written onto its branch."""
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = fixture.session_world(root)
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root)
            )

            with self.assertRaises(SessionNotebookRefused) as caught:
                _ = self._import(
                    root,
                    "xf-ideation",
                    target_arg,
                    [{"id": "src-note", "title": "A converted note"}],
                )

            self.assertIn("is not that session's notebook", str(caught.exception))

    def scenario_a_dead_sessions_directory_is_not_a_live_session(self) -> None:
        """`resolve_session_target` tested `worktree.is_dir()` and NOTHING else,
        so against crash residue — the git association pruned AND the branch
        deleted — it returned a target and drove create / re-sync / RETIRE against
        a session that did not exist. `bootstrap_sessions`, handed the identical
        directory, answered `live=()` and reported it stale (FR-008, D10)."""
        with TemporaryDirectory() as td:
            root = Path(td)
            checkout, worktree = fixture.session_world(
                root, branch="draft/residue-topic"
            )
            _ = fixture.git(checkout, "worktree", "remove", "--force", str(worktree))
            _ = fixture.git(checkout, "branch", "-D", "draft/residue-topic")
            worktree.mkdir(parents=True)
            (worktree / "ideation/staging/demo-topic").mkdir(parents=True)

            with self.assertRaises(SessionNotebookRefused) as caught:
                sync.resolve_session_target(root, "draft/residue-topic")
            self.assertIn("JOINT worktree+branch signal", str(caught.exception))

            # and the two liveness answers now AGREE
            registry = fixture.dashboard_registry()
            report = bs.bootstrap_sessions(
                registry, repository="openxFactory", checkout_root=checkout
            )
            self.assertEqual(report.branches, ())

    def scenario_the_import_cannot_feed_itself(self) -> None:
        """Unbounded self-amplification, measured at 788 -> 2120 -> 4784 -> 10112
        bytes over four rounds. A projected source's title is `<path>  #<hash>`,
        which matched neither charter title nor a `[status]` prefix, so the import
        planned the notebook's OWN projected output; the imported file then became
        a governed document, re-projected under a NEW source id, and the
        source-id dedupe could not stop it by construction."""
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = fixture.session_world(root)
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root)
            )
            projected = wb.managed_source_title(
                "ideation/staging/demo-topic/notebooklm-ideas-2026-07-26.md",
                "already imported body",
            )

            count = self._import(
                root, alias, target_arg, [{"id": "src-self", "title": projected}]
            )

            self.assertEqual(count, 0)
            self.assertTrue(sync.is_seed_source(projected))
            self.assertEqual(
                list(
                    (worktree / "ideation/staging/demo-topic").glob(
                        "notebooklm-ideas-*.md"
                    )
                ),
                [],
            )

    def scenario_a_draft_only_outline_source_still_imports_and_commits(self) -> None:
        """The positive control the refusals must not swallow: an ordinary human
        source — here a draft-only outline with no managed title at all — still
        imports into the bound session worktree and still LANDS on the branch."""
        with TemporaryDirectory() as td:
            root = Path(td)
            _checkout, worktree = fixture.session_world(root)
            alias = bs.notebook_alias("openxFactory", "draft/demo-topic")
            target_arg = str(
                (worktree / "ideation/staging/demo-topic").relative_to(root)
            )

            count = self._import(
                root,
                alias,
                target_arg,
                [{"id": "src-outline", "title": "Outline: the draft-only shape"}],
                {"src-outline": "- one\n- two\n"},
            )

            self.assertEqual(count, 1)
            landed = (
                worktree
                / "ideation/staging/demo-topic"
                / "notebooklm-ideas-2026-07-26.md"
            )
            self.assertTrue(landed.is_file())
            self.assertNotIn(
                "notebooklm-ideas", fixture.git(worktree, "status", "--porcelain")
            )
            self.assertIn(
                "Source-Notebook: " + alias,
                fixture.git(worktree, "log", "-1", "--format=%B"),
            )
