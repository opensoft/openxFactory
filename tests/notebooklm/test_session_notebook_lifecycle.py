"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ideation_dashboard import branch_session as bs
from ideation_dashboard import workbench as wb

from tests.notebooklm._sync_test_support import (
    CODEX_SESSION_ALIAS,
    LIFECYCLE_BOOKS,
    SESSION_ALIAS,
    STAGED_DOC,
    FakeNlm,
    HarnessFailure,
    _doc,
    _seed_checkout,
    _session_world,
    sync,
)


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
            with patch.object(sync, "session_source_set", lambda target: oversize):
                result = sync.sync_session_notebook(
                    root, "draft/demo-topic", apply=True, adapter=adapter)

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
        module_file = sync.__file__
        source = Path(module_file).read_text() if module_file is not None else ""
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
                    raise HarnessFailure("nlm notebook list: auth expired")
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
