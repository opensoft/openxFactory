from __future__ import annotations

import json
import unittest

from tests.notebooklm._test_sync_oversized_adoption_support import (
    DIFFERENT,
    DIFFERENT_2,
    FAR,
    HANDLE,
    PROJECTED,
    TITLE,
    TRANSFORMED,
    FakeBook,
    driving,
    sync,
)


class OversizedAdoptionTests(unittest.TestCase):
    """Hole (a): a bounded fallback for the class the strict digest can never
    match — and a LOUD STOP where the old code uploaded another duplicate."""

    def test_a_verbatim_stray_is_still_adopted_by_the_STRICT_digest(self) -> None:
        """The strict digest stays the FIRST gate. Nothing about the fallback
        may weaken the case that already worked."""
        book = FakeBook((("stray1", "xf-sync-deadbeef.md", PROJECTED),))
        with driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertEqual(
            book.adds(), [], "the stray IS this document; adding again duplicates it"
        )
        self.assertEqual(book.title_of("stray1"), TITLE)
        self.assertIn("by strict digest", out.getvalue())

    def test_a_provider_transformed_stray_is_adopted_by_the_NORMALIZED_digest(
        self,
    ) -> None:
        """Issue #462 hole (a), the live class.

        The provider returned 281,645 bytes for a 279,235-byte document, so the
        strict digest could never match and every run added another copy. Within
        the byte tolerance and unique on the normalized digest, the stray is
        adopted and nothing is uploaded.
        """
        self.assertNotEqual(
            sync.content_digest(PROJECTED), sync.content_digest(TRANSFORMED)
        )
        delta = abs(len(TRANSFORMED.encode()) - len(PROJECTED.encode()))
        self.assertGreater(delta, 0, "the transformed body must differ in bytes")
        self.assertLessEqual(delta, sync.ADOPTION_LENGTH_TOLERANCE_BYTES)
        book = FakeBook((("stray1", "xf-sync-deadbeef.md", TRANSFORMED),))
        with driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertEqual(
            book.adds(), [], "the stray is this document as the provider stores it"
        )
        self.assertEqual(book.title_of("stray1"), TITLE)
        text = out.getvalue()
        self.assertIn("by normalized digest", text)
        self.assertIn(f"{len(TRANSFORMED.encode())}B", text)
        self.assertIn(f"{len(PROJECTED.encode())}B", text)

    def test_one_within_tolerance_NON_MATCHING_stray_STOPS_without_uploading(
        self,
    ) -> None:
        """The compounding path, closed.

        A stray that is the right size but not this document is the state in
        which uploading again is exactly what produced four copies of one
        document. The run stops loudly and names the hand adoption instead.
        """
        book = FakeBook((("stray1", "xf-sync-deadbeef.md", DIFFERENT),))
        with (
            driving(book) as (_out, _sleeps),
            self.assertRaises(RuntimeError) as caught,
        ):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        msg = str(caught.exception)
        self.assertEqual(
            book.adds(), [], "STOP means stop — no fresh duplicate may be uploaded"
        )
        self.assertEqual(
            book.renames(), [], "an unmatched stray must not be adopted either"
        )
        self.assertIn("stray1", msg)
        self.assertIn(f"{len(DIFFERENT.encode())}B", msg)
        self.assertIn(f"{len(PROJECTED.encode())}B", msg)
        self.assertIn("nlm source rename", msg)
        self.assertIn("fully-ingested", msg)
        self.assertIn("Do NOT re-run", msg)

    def test_TWO_within_tolerance_strays_report_BOTH_and_adopt_neither(self) -> None:
        """Ambiguity is not a licence to guess — nor to add a third copy."""
        book = FakeBook(
            (
                ("strayA", "xf-sync-aaaa.md", DIFFERENT),
                ("strayB", "xf-sync-bbbb.md", DIFFERENT_2),
            )
        )
        with (
            driving(book) as (_out, _sleeps),
            self.assertRaises(RuntimeError) as caught,
        ):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        msg = str(caught.exception)
        self.assertIn("strayA", msg)
        self.assertIn("strayB", msg)
        self.assertEqual(book.adds(), [])
        self.assertEqual(book.renames(), [])
        self.assertEqual(sorted(book.titles()), ["xf-sync-aaaa.md", "xf-sync-bbbb.md"])

    def test_a_stray_FAR_outside_the_tolerance_falls_through_to_a_normal_add(
        self,
    ) -> None:
        """With nothing plausibly this document, there is nothing to compound
        and nothing to decide: the pre-existing behaviour, unchanged."""
        book = FakeBook((("other", "xf-sync-unrelated.md", FAR),))
        with driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        adds = book.adds()
        self.assertEqual(len(adds), 1)
        self.assertIn("--file", adds[0])
        self.assertEqual(
            book.title_of("other"),
            "xf-sync-unrelated.md",
            "an unrelated stray is left exactly as it was",
        )
        self.assertEqual(book.title_of("upload1"), TITLE)
        self.assertIn("uploaded as upload1", out.getvalue())

    def test_no_strays_at_all_falls_through_to_a_normal_add(self) -> None:
        book = FakeBook()
        with driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertEqual(len(book.adds()), 1)
        self.assertEqual(book.title_of("upload1"), TITLE)
        self.assertIn("renamed on attempt 1", out.getvalue())

    def test_the_normalized_digest_folds_only_defensible_transformations(self) -> None:
        """Each normalization is named in the docstring and each is tested; a
        changed WORD is still a different document."""
        base = "alpha\nbeta café\n"
        self.assertEqual(
            sync.normalized_digest(base),
            sync.normalized_digest("alpha\r\nbeta café\r\n"),
        )
        self.assertEqual(
            sync.normalized_digest(base),
            sync.normalized_digest("alpha   \nbeta café\t\n"),
        )
        self.assertEqual(
            sync.normalized_digest(base), sync.normalized_digest(base + "\n\n\n")
        )
        self.assertEqual(
            sync.normalized_digest(base), sync.normalized_digest("alpha\nbeta café\n")
        )
        self.assertEqual(
            sync.normalized_digest(base),
            sync.normalized_digest(json.dumps({"value": {"content": base}})),
        )
        self.assertNotEqual(
            sync.normalized_digest(base), sync.normalized_digest("alpha\nbeta tea\n")
        )
