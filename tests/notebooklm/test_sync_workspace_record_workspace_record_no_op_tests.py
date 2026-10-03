from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar

from notebooklm_sync.models import BookSpec

from tests.notebooklm._test_sync_workspace_record_support import (
    LEGACY_ID,
    NEW_ID,
    REGISTRY,
    active_records,
    run_record,
    sync,
    write_registry,
)


class WorkspaceRecordNoOpTests(unittest.TestCase):
    """The paths that must stay exactly as they were."""

    DRAFTS: ClassVar[BookSpec] = sync.static_spec("drafts")

    def test_the_same_id_already_registered_is_a_silent_no_op(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            before = path.read_text(encoding="utf-8")
            plan = run_record(root, self.DRAFTS, LEGACY_ID, apply=False)
            applied = run_record(root, self.DRAFTS, LEGACY_ID, apply=True)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(before, after)
        self.assertEqual(plan, "")
        self.assertEqual(
            applied,
            "",
            "a book already registered under the id it has is not an operation and must not read as one",
        )

    def test_a_missing_registry_is_a_notice_and_not_a_crash(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            text = run_record(root, self.DRAFTS, NEW_ID, apply=True)
            self.assertFalse(
                (root / REGISTRY).exists(),
                "a missing registry is reported, never conjured",
            )
        self.assertIn("NOTICE", text)
        self.assertIn("workspace registry missing", text)

    def test_a_record_without_a_provider_id_line_stays_hand_reconciled(self) -> None:
        """The one case that genuinely cannot be replaced.

        Appending a second record would break the one-record invariant, so the
        function reports instead of guessing.
        """
        malformed = "workspaces:\n  - kind: external_source_workspace\n    schema_version: 1\n    id: workspace-xfactory-lifecycle-drafts\n    provider: notebooklm\n"
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root, malformed)
            text = run_record(root, self.DRAFTS, NEW_ID, apply=True)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(after, malformed)
        self.assertIn("reconcile by hand", text)

    def test_an_unregistered_book_is_registered_and_planned_first(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root, "workspaces:\n")
            plan = run_record(root, self.DRAFTS, NEW_ID, apply=False)
            self.assertEqual(path.read_text(encoding="utf-8"), "workspaces:\n")
            _ = run_record(root, self.DRAFTS, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        self.assertIn("REGISTER", plan)
        self.assertIn(NEW_ID, plan)
        records = active_records(written)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "workspace-xfactory-lifecycle-drafts")
        self.assertEqual(records[0]["provider_notebook_id"], NEW_ID)
