from __future__ import annotations

import unittest

from tests.notebooklm._test_sync_oversized_adoption_support import (
    HANDLE,
    PROJECTED,
    TITLE,
    FakeBook,
    driving,
    sync,
)


class RenameSettleTests(unittest.TestCase):
    """Hole (b): the read-back proved a moment. Now it proves a steady state."""

    def test_the_settle_reverify_reads_the_title_back_AFTER_the_delay(self) -> None:
        book = FakeBook()
        with driving(book) as (out, sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        text = out.getvalue()
        self.assertIn("renamed on attempt 1", text)
        self.assertIn("settle re-verify: title held", text)
        self.assertIn(
            sync.RENAME_SETTLE_DELAY_S,
            sleeps,
            "the settle delay must actually be waited out",
        )
        marker = book.calls.index(("SETTLE-SLEEP", 1))
        self.assertTrue(
            any(c[:2] == ("source", "list") for c in book.calls[marker:]),
            "the title must be READ BACK after the settle delay",
        )

    def test_a_title_that_REGRESSES_after_the_settle_delay_RAISES(self) -> None:
        """The live failure: the poll passed on attempt 1, the manifest was
        written, the run exited 0, and the title reverted to the temp filename
        when ingestion completed. That must be the loud path, never exit 0."""
        book = FakeBook()

        def restamp(_nth: int) -> None:
            book.set_title("upload1", "xf-sync-fresh.md")

        with (
            driving(book, on_settle=restamp) as (out, _sleeps),
            self.assertRaises(RuntimeError) as caught,
        ):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        msg = str(caught.exception)
        self.assertIn("REGRESSED", msg)
        self.assertIn("upload1", msg)
        self.assertIn("nlm source rename", msg)
        self.assertIn("do NOT re-run the sync", msg)
        self.assertIn("settle re-verify: title REGRESSED", out.getvalue())
        self.assertEqual(len(book.renames()), 2)
        self.assertEqual(book.title_of("upload1"), "xf-sync-fresh.md")

    def test_ONE_re_rename_repairs_a_regression_and_the_run_continues(self) -> None:
        """A retry is cheap and, by the second settle, ingestion has had longer
        to finish — which is the state in which the live hand repair held."""
        book = FakeBook()

        def restamp_once(nth: int) -> None:
            if nth == 1:
                book.set_title("upload1", "xf-sync-fresh.md")

        with driving(book, on_settle=restamp_once) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        text = out.getvalue()
        self.assertIn("settle re-verify: title REGRESSED", text)
        self.assertIn("title held after one re-rename", text)
        self.assertEqual(len(book.renames()), 2)
        self.assertEqual(book.title_of("upload1"), TITLE)

    def test_an_ADOPTED_stray_is_settle_verified_too(self) -> None:
        """Adoption renames through the same helper, so a stray adopted into
        place and then re-stamped must be just as loud as a fresh upload."""
        book = FakeBook((("stray1", "xf-sync-deadbeef.md", PROJECTED),))

        def restamp(_nth: int) -> None:
            book.set_title("stray1", "xf-sync-deadbeef.md")

        with (
            driving(book, on_settle=restamp) as (_out, _sleeps),
            self.assertRaises(RuntimeError) as caught,
        ):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertIn("REGRESSED", str(caught.exception))
        self.assertEqual(
            book.adds(), [], "a regressed adoption must not become a fresh upload"
        )
