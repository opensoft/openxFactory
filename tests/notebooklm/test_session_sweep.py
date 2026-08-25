"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import contextlib
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ideation_dashboard import branch_session as bs

from tests.notebooklm._sync_test_support import (
    SCRIPT,
    sync,
)


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

        class RetiringAdapter(Adapter):
            def retire(self, alias):
                calls.append(("retire", alias))
                return Result(True, "retired")

        return (RetiringAdapter() if retire else Adapter()), calls

    def _classify(self, titles, live, slugs):
        return dict(sync.classify_session_notebooks(titles, live, slugs))

    @contextlib.contextmanager
    def _workspace(self, live_aliases, errors=(), *, repositories=("openxFactory",)):
        """Drive the REAL sweep with its two inputs controlled at ONE seam.

        `session_repositories` feeds both halves — the live-alias walk and the
        in-scope slug list — so stubbing it keeps them consistent, which is
        exactly the property the sweep depends on."""
        with (
            patch.object(
                sync,
                "session_repositories",
                lambda root: [(name, Path(root) / name) for name in repositories],
            ),
            patch.object(
                sync,
                "live_session_aliases",
                lambda root, pairs=None: (set(live_aliases), list(errors)),
            ),TemporaryDirectory() as tmp
        ):
            yield Path(tmp)

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
            capture_output=True, text=True, check=False)
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
