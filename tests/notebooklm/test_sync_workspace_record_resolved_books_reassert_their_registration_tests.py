from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar

from notebooklm_sync.models import BookSpec

from tests.notebooklm._test_sync_workspace_record_support import (
    NEW_ID,
    OTHER_ID,
    active_records,
    sync,
    write_registry,
)


class ResolvedBooksReassertTheirRegistrationTests(unittest.TestCase):
    """The FOUND path re-asserts too, which is where a migration lands.

    A hosting move re-derives the books; the run that CREATES them writes the
    replacement, but every run after that merely RESOLVES them by title. If the
    found path did not check, a registry left stale by a partial or skipped
    migration would never converge — the failure the issue was filed to prevent.
    """

    DRAFTS: ClassVar[BookSpec] = sync.static_spec("drafts")

    def _resolve(
        self, root: Path, apply: bool, notebooks: list[dict[str, str]] | None = None
    ) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            _nid, ok = sync.resolve_or_create_book(
                root,
                self.DRAFTS,
                apply,
                notebooks
                if notebooks is not None
                else [{"id": NEW_ID, "title": self.DRAFTS.title}],
                bind_alias=False,
            )
        self.assertTrue(ok)
        return out.getvalue()

    def test_two_notebooks_under_one_title_leave_the_record_alone(self) -> None:
        """An arbitrary resolution must not become a governed write.

        `by_title` keeps whichever row the provider returned LAST, so a
        duplicate title resolves to an arbitrary notebook. Projecting into one
        is a pre-existing hazard; re-pointing the record at it would overwrite
        an already-correct registration and flap it as ordering changes.
        """
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            before = path.read_text(encoding="utf-8")
            text = self._resolve(
                root,
                apply=True,
                notebooks=[
                    {"id": NEW_ID, "title": self.DRAFTS.title},
                    {"id": OTHER_ID, "title": self.DRAFTS.title},
                ],
            )
            after = path.read_text(encoding="utf-8")
        self.assertEqual(
            before, after, "an ambiguous title is what hand reconciliation is for"
        )
        self.assertIn("NOTICE", text)
        self.assertIn(NEW_ID, text)
        self.assertIn(OTHER_ID, text)
        self.assertNotIn("REPLACED", text)

    def test_a_read_only_resolve_plans_the_replacement_without_writing(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            before = path.read_text(encoding="utf-8")
            text = self._resolve(root, apply=False)
            after = path.read_text(encoding="utf-8")
        self.assertEqual(
            before,
            after,
            "--parity resolves with apply=False: a proof that changes the thing it measures is not a proof",
        )
        self.assertIn("REPLACE", text)

    def test_an_apply_resolve_re_points_the_stale_record(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            path = write_registry(root)
            _ = self._resolve(root, apply=True)
            written = path.read_text(encoding="utf-8")
        drafts = [
            r
            for r in active_records(written)
            if r.get("id") == "workspace-xfactory-lifecycle-drafts"
        ]
        self.assertEqual(len(drafts), 1)
        self.assertEqual(drafts[0]["provider_notebook_id"], NEW_ID)
