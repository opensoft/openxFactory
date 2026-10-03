from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar

from notebooklm_sync.models import BookSpec

from tests.notebooklm._test_sync_workspace_record_support import (
    LEGACY_ID,
    NEW_ID,
    OTHER_ID,
    active_records,
    run_record,
    sync,
    write_registry,
)


class WorkspaceRecordReplacementTests(unittest.TestCase):
    """The replace path: the record is RE-POINTED, never duplicated."""

    DRAFTS: ClassVar[BookSpec] = sync.static_spec("drafts")

    def test_a_plan_run_prints_the_replacement_and_writes_nothing(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            before = path.read_text(encoding="utf-8")
            text = run_record(root, self.DRAFTS, NEW_ID, apply=False)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(
            before, after, "a plan run that re-points the registry is not a plan"
        )
        self.assertIn("REPLACE", text)
        self.assertIn(LEGACY_ID, text)
        self.assertIn(NEW_ID, text)
        self.assertIn("workspace-xfactory-lifecycle-drafts", text)
        for verb in (" ADD ", " DEL ", " UPD "):
            self.assertNotIn(verb, text)

    def test_apply_leaves_exactly_one_active_record_holding_the_new_id(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            text = run_record(root, self.DRAFTS, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        records = active_records(written)
        drafts = [
            r for r in records if r.get("id") == "workspace-xfactory-lifecycle-drafts"
        ]
        self.assertEqual(
            len(drafts),
            1,
            "exactly one active record per live book: a replacement appends nothing",
        )
        self.assertEqual(drafts[0]["provider_notebook_id"], NEW_ID)
        self.assertNotIn(
            LEGACY_ID,
            written,
            "the legacy provider notebook is what gets retired; the record must not keep pointing at it",
        )
        self.assertIn("REPLACED", text)
        self.assertIn(LEGACY_ID, text)
        self.assertIn(NEW_ID, text)

    def test_every_other_field_and_every_comment_survives_the_replacement(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            before = path.read_text(encoding="utf-8").splitlines()
            _ = run_record(root, self.DRAFTS, NEW_ID, apply=True)
            after = path.read_text(encoding="utf-8").splitlines()
        changed = [(b, a) for b, a in zip(before, after) if b != a]
        self.assertEqual(
            len(before), len(after), "the replacement rewrites one line in place"
        )
        self.assertEqual(
            changed,
            [
                (
                    f"    provider_notebook_id: {LEGACY_ID}",
                    f"    provider_notebook_id: {NEW_ID}",
                )
            ],
            "only provider_notebook_id moves — created_at and the rest are the record's own history, and the header comments carry the migration record",
        )

    def test_a_record_with_a_different_key_is_untouched(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            _ = run_record(root, self.DRAFTS, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        opsx = [
            r
            for r in active_records(written)
            if r.get("id") == "workspace-xfactory-lifecycle-ideation-opsxfactory"
        ]
        self.assertEqual(len(opsx), 1)
        self.assertEqual(
            opsx[0]["provider_notebook_id"],
            OTHER_ID,
            "another book's registration is not this book's to move",
        )

    def test_a_prefix_id_does_not_reach_the_longer_record(self) -> None:
        """`…-ideation` must not rewrite `…-ideation-opsxfactory`.

        The retired shared Ideation book's id is a strict prefix of every
        per-repo one, and it survives in the registry as a commented block. A
        substring test finds both; a whole-line test finds neither, which is
        the correct answer — there is no ACTIVE record under that id.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            retired = sync.BookSpec(
                key="ideation", alias="xf-ideation", title="xFactory — Ideation"
            )
            text = run_record(root, retired, NEW_ID, apply=True)
            written = path.read_text(encoding="utf-8")
        opsx = [
            r
            for r in active_records(written)
            if r.get("id") == "workspace-xfactory-lifecycle-ideation-opsxfactory"
        ]
        self.assertEqual(opsx[0]["provider_notebook_id"], OTHER_ID)
        self.assertIn(
            "#     provider_notebook_id: 27b1880b-6974-4cfe-a76f-4318f6021608", written
        )
        self.assertIn(
            "workspace record workspace-xfactory-lifecycle-ideation ->",
            text,
            "no active record under that id: it is REGISTERED, not treated as a replacement",
        )
