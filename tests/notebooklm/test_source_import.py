"""Focused behavioral tests extracted from the NotebookLM sync suite."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from notebooklm_sync.nlm_client import ProviderResult

from tests.notebooklm.typed_sync_contracts import load_typed_sync

sync = load_typed_sync()


class NotebookLmSourceImportTests(unittest.TestCase):
    def test_parse_export_title_still_supports_explicit_route(self):
        target = sync.parse_export_title(
            "[export:brainstorm] openxFactory: openspec-speckit-release-flow - "
            + "release branch concern"
        )
        if target is None:
            raise AssertionError("explicit brainstorm route did not parse")
        self.assertEqual(target.status, "brainstorm")
        self.assertEqual(target.repo, "openxFactory")
        self.assertEqual(target.topic, "openspec-speckit-release-flow")
        self.assertEqual(target.title, "release branch concern")

        staged = sync.parse_export_title(
            "[export:staged] doc-health-checks - notebook drift issue"
        )
        if staged is None:
            raise AssertionError("explicit staged route did not parse")
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

            def fake_nlm(*args: str, parse: bool = True) -> ProviderResult:
                del parse
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
            content_calls: list[str] = []

            def fake_nlm(*args: str, parse: bool = True) -> ProviderResult:
                del parse
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
            _ = (change / "proposal.md").write_text("## Why\n")
            _ = (target / "manifest.yaml").write_text(
                '{"format_version": 1, "files": []}\n'
            )

            def fake_nlm(*args: str, parse: bool = True) -> ProviderResult:
                del parse
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
                root
                / "openxFactory/openspec/changes/archive/2026-07-09-change-a/supporting-docs"
            )
            archived.mkdir(parents=True)
            with self.assertRaises(ValueError):
                _ = sync.target_from_path(root, str(archived.relative_to(root)))
            missing = (
                "openxFactory/openspec/changes/change-b/supporting-docs"
            )
            with self.assertRaises(ValueError):
                _ = sync.target_from_path(root, missing)

    def test_hostile_export_titles_cannot_traverse_the_workspace(self):
        # topic with path syntax is flattened to a single safe segment
        target = sync.parse_export_title(
            "[export:staged] a/../../../../etc/cron.d - x")
        if target is None:
            raise AssertionError("hostile staged route did not parse")
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
