"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tests.notebooklm.typed_sync_contracts import load_typed_sync

sync = load_typed_sync()


class NotebookLmSourceImportBoundaryTests(unittest.TestCase):
    def scenario_hostile_export_titles_cannot_traverse_the_workspace(self) -> None:
        # topic with path syntax is flattened to a single safe segment
        target = sync.parse_export_title("[export:staged] a/../../../../etc/cron.d - x")
        if target is None:
            raise AssertionError("hostile staged route did not parse")
        self.assertNotIn("/", target.topic)
        self.assertNotIn("..", target.topic)
        # repo with path syntax drops the source entirely
        self.assertIsNone(
            sync.parse_export_title("[export:brainstorm] ../evil: topic - x")
        )

    def scenario_scan_excludes_worktree_containers_and_nested_checkouts(self) -> None:
        doc = "Status: staged\n"
        with TemporaryDirectory() as td:
            root = Path(td)
            governed = root / "xFactories/RealFactory"
            (governed / "docs").mkdir(parents=True)
            (governed / ".git").mkdir()
            _ = (governed / "docs/real-doc.md").write_text("# Real\n\n" + doc)
            (root / "openxFactory").mkdir()

            # feature-branch worktree container beside the governed repos
            wt = root / "xFactories/OpsxFactory-worktrees/002-branch"
            (wt / "docs").mkdir(parents=True)
            _ = (wt / ".git").write_text("gitdir: elsewhere\n")
            _ = (wt / "docs/branch-doc.md").write_text("# Branch\n\n" + doc)

            # embedded clone nested inside a governed repo
            nested = governed / "vendor/clone"
            (nested / "docs").mkdir(parents=True)
            (nested / ".git").mkdir()
            _ = (nested / "docs/clone-doc.md").write_text("# Clone\n\n" + doc)

            desired, specs = sync.scan(root)

            ideation = desired["ideation-realfactory"]
            self.assertEqual(
                specs["ideation-realfactory"].title, "xFactory Ideation — RealFactory"
            )
            self.assertIn("xFactories/RealFactory/docs/real-doc.md", ideation)
            # the worktree container spawned NO ideation book of its own
            self.assertNotIn("ideation-opsxfactory-worktrees", desired)
            polluted = [
                path
                for book in desired.values()
                for path in book
                if "worktrees" in path or "vendor/clone" in path
            ]
            self.assertEqual(polluted, [])
            repos = {
                title.split("] ", 1)[1].split(":", 1)[0]
                for book in desired.values()
                for title in book.values()
                if "] " in title and ":" in title
            }
            self.assertNotIn("OpsxFactory-worktrees", repos)

    def scenario_append_import_refuses_paths_outside_workspace(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td) / "workspace"
            root.mkdir()
            plan = sync.ExportPlan(
                source_id="s",
                source_title="t",
                status="staged",
                repo="openxFactory",
                topic="x",
                title="x",
                path=root / ".." / "escape.md",
            )
            with self.assertRaises(SystemExit):
                sync.append_import(root, plan, "book", "content")
            self.assertFalse((Path(td) / "escape.md").exists())
