"""The oversized-upload path of `sync-notebooklm-books.py`, issue #462.

#438 fixed the oversized rename twice over — a bounded poll instead of a fixed
`sleep(2)`, and stray ADOPTION instead of a duplicating re-run — and both halves
missed live on 2026-08-28, each doing exactly what it was written to do:

  (a) adoption compares the projected body against `nlm source content` on a
      STRICT digest, and the provider does not return large bodies verbatim: all
      four strays of the 279,235-byte `ideation-dashboard` spec came back as
      281,645 bytes. For that class the strict gate can never match, so the
      "safe" fall-through to a normal add minted a fresh duplicate every run;
  (b) the rename's read-back proves a MOMENT. Both applies passed the poll on
      attempt 1 and the title later regressed to the temp filename — apparently
      re-stamped when ingestion of the large body completed — so the run exited
      0 over a stranded source, with nothing in the transcript to say so.

Every test here drives a STUBBED `nlm`; no test in this file may reach the real
CLI or the provider (FR-043, and `tests/hermeticity.py` makes that structural).
Both sleeps — the poll interval and the new settle delay — are monkeypatched,
and the settle sleep is where the tests inject the provider's re-stamp, which is
the honest model of "ingestion completed while we waited".

It lives beside `test_sync_notebooklm_books.py` rather than inside it because
that file is 3,000 lines that several lanes edit at once.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import itertools
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"

# The script is not importable as a package (its name is hyphenated), so it is
# loaded by path — the same seam `test_sync_notebooklm_books.py` uses. REUSED
# when that module has already loaded it, so the suite holds ONE object and a
# `patch.object` here cannot be reading a different copy than the code under
# test is running from.
if "sync_notebooklm_books" in sys.modules:
    sync = sys.modules["sync_notebooklm_books"]
else:
    _spec = importlib.util.spec_from_file_location("sync_notebooklm_books", SCRIPT)
    sync = importlib.util.module_from_spec(_spec)
    assert _spec.loader is not None
    sys.modules[_spec.name] = sync
    _spec.loader.exec_module(sync)


TITLE = "[spec] openxFactory: ideation-dashboard"
HANDLE = "nbX"

# A body large enough to ride the oversized path under a patched
# MAX_TEXT_ARG_BYTES, with real line structure so the line-ending and
# trailing-whitespace normalizations have something to act on. The composed
# "é" gives NFC something to fold on the other side.
PROJECTED = "".join(
    f"line {n}: {'x' * 40} caf\u00e9\n" for n in range(200)   # e-acute COMPOSED
)

# What a provider that rewrites line endings, pads line ends, adds trailing
# blank lines and DECOMPOSES accents would hand back: DIFFERENT BYTES, same
# document. Length differs by ~1KB, well inside ADOPTION_LENGTH_TOLERANCE_BYTES.
# The escapes are spelled out because the two forms are indistinguishable on
# screen, and a reader must be able to see that this is not a no-op replace.
TRANSFORMED = (PROJECTED.replace("caf\u00e9", "cafe\u0301")   # NFC -> NFD
                        .replace("\n", "  \r\n") + "\n\n")

# Same length class, DIFFERENT DOCUMENT: proves length alone never adopts.
DIFFERENT = PROJECTED.replace("line 7:", "LINE 7:").replace("line 9:", "LINE 9:")
DIFFERENT_2 = PROJECTED.replace("line 3:", "LINE 3:")

# Far outside the tolerance — a genuinely unrelated stray.
FAR = PROJECTED + ("y" * 20_000)


class FakeBook:
    """One notebook, modelling the four verbs the oversized path speaks.

    `source list` / `source content` / `source add` / `source rename` and
    NOTHING else: an unmodelled verb raises, so a test cannot pass because the
    code took a route this double happens to tolerate.

    THE RENAME IS MODELLED AS A WRITE. #438's own review found a fake whose
    `source rename` returned `""` without recording anything, which would have
    made every rename look like it never took — a test double that ignores the
    write cannot verify it.
    """

    def __init__(self, strays: tuple[tuple[str, str, str], ...] = ()) -> None:
        self.sources = [{"id": sid, "title": title} for sid, title, _b in strays]
        self.bodies = {sid: body for sid, _t, body in strays}
        self.calls: list[tuple] = []
        self._ids = itertools.count(1)

    def __call__(self, *args, parse=True):
        self.calls.append(args)
        head = args[:2]
        if head == ("source", "list"):
            return [dict(r) for r in self.sources]
        if head == ("source", "content"):
            return self.bodies.get(args[2], "")
        if head == ("source", "add"):
            sid = f"upload{next(self._ids)}"
            # The CLI titles a `--file` source by FILENAME, which is the whole
            # reason the rename exists.
            self.sources.append({"id": sid, "title": "xf-sync-fresh.md"})
            return f"Added source: xf-sync-fresh.md\nSource ID: {sid}\n"
        if head == ("source", "rename"):
            for row in self.sources:
                if row["id"] == args[2]:
                    row["title"] = args[3]
            return ""
        raise AssertionError(f"unexpected nlm call: {args}")

    # ---- reads the assertions use ----
    def adds(self) -> list[tuple]:
        return [c for c in self.calls if c[:2] == ("source", "add")]

    def renames(self) -> list[tuple]:
        return [c for c in self.calls if c[:2] == ("source", "rename")]

    def titles(self) -> list[str]:
        return [r["title"] for r in self.sources]

    def title_of(self, source_id: str) -> str:
        return next((r["title"] for r in self.sources if r["id"] == source_id), "")

    def set_title(self, source_id: str, title: str) -> None:
        for row in self.sources:
            if row["id"] == source_id:
                row["title"] = title


def _sleeper(book: FakeBook | None = None, on_settle=None):
    """A no-op `time.sleep` that RECORDS, and optionally lets a test act during
    the settle window — the one place a provider's re-stamp can arrive.

    Also drops a marker into the call log so a test can assert the settle
    re-verify's read happened AFTER the delay, not merely that a delay happened.
    """
    sleeps: list[float] = []
    settles = itertools.count(1)

    def sleep(seconds):
        sleeps.append(seconds)
        if seconds == sync.RENAME_SETTLE_DELAY_S:
            nth = next(settles)
            if book is not None:
                book.calls.append(("SETTLE-SLEEP", nth))
            if on_settle is not None:
                on_settle(nth)

    return sleeps, sleep


@contextlib.contextmanager
def _driving(book: FakeBook, *, on_settle=None):
    """Run the oversized path against `book`, capturing stdout and sleeps."""
    sleeps, sleep = _sleeper(book, on_settle)
    out = io.StringIO()
    with patch.object(sync, "nlm", book), \
            patch.object(sync, "MAX_TEXT_ARG_BYTES", 200), \
            patch.object(sync.time, "sleep", sleep), \
            contextlib.redirect_stdout(out):
        yield out, sleeps


class OversizedAdoptionTests(unittest.TestCase):
    """Hole (a): a bounded fallback for the class the strict digest can never
    match — and a LOUD STOP where the old code uploaded another duplicate."""

    def test_a_verbatim_stray_is_still_adopted_by_the_STRICT_digest(self):
        """The strict digest stays the FIRST gate. Nothing about the fallback
        may weaken the case that already worked."""
        book = FakeBook((("stray1", "xf-sync-deadbeef.md", PROJECTED),))
        with _driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertEqual(book.adds(), [],
                         "the stray IS this document; adding again duplicates it")
        self.assertEqual(book.title_of("stray1"), TITLE)
        self.assertIn("by strict digest", out.getvalue())

    def test_a_provider_transformed_stray_is_adopted_by_the_NORMALIZED_digest(self):
        """Issue #462 hole (a), the live class.

        The provider returned 281,645 bytes for a 279,235-byte document, so the
        strict digest could never match and every run added another copy. Within
        the byte tolerance and unique on the normalized digest, the stray is
        adopted and nothing is uploaded.
        """
        # The strict gate really is failing here — otherwise this test would
        # pass without the fallback existing at all.
        self.assertNotEqual(sync._content_digest(PROJECTED),
                            sync._content_digest(TRANSFORMED))
        delta = abs(len(TRANSFORMED.encode()) - len(PROJECTED.encode()))
        self.assertGreater(delta, 0, "the transformed body must differ in bytes")
        self.assertLessEqual(delta, sync.ADOPTION_LENGTH_TOLERANCE_BYTES)

        book = FakeBook((("stray1", "xf-sync-deadbeef.md", TRANSFORMED),))
        with _driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertEqual(book.adds(), [],
                         "the stray is this document as the provider stores it")
        self.assertEqual(book.title_of("stray1"), TITLE)
        text = out.getvalue()
        self.assertIn("by normalized digest", text)
        # the transcript names both byte lengths, so the operator can see WHY
        # the strict gate did not fire
        self.assertIn(f"{len(TRANSFORMED.encode())}B", text)
        self.assertIn(f"{len(PROJECTED.encode())}B", text)

    def test_one_within_tolerance_NON_MATCHING_stray_STOPS_without_uploading(self):
        """The compounding path, closed.

        A stray that is the right size but not this document is the state in
        which uploading again is exactly what produced four copies of one
        document. The run stops loudly and names the hand adoption instead.
        """
        book = FakeBook((("stray1", "xf-sync-deadbeef.md", DIFFERENT),))
        with _driving(book) as (_out, _sleeps):
            with self.assertRaises(RuntimeError) as caught:
                sync.add_text_source(HANDLE, PROJECTED, TITLE)
        msg = str(caught.exception)
        self.assertEqual(book.adds(), [],
                         "STOP means stop — no fresh duplicate may be uploaded")
        self.assertEqual(book.renames(), [],
                         "an unmatched stray must not be adopted either")
        self.assertIn("stray1", msg)                      # names the stray
        self.assertIn(f"{len(DIFFERENT.encode())}B", msg)  # provider's length
        self.assertIn(f"{len(PROJECTED.encode())}B", msg)  # projected length
        self.assertIn("nlm source rename", msg)            # the hand adoption
        self.assertIn("fully-ingested", msg)
        self.assertIn("Do NOT re-run", msg)

    def test_TWO_within_tolerance_strays_report_BOTH_and_adopt_neither(self):
        """Ambiguity is not a licence to guess — nor to add a third copy."""
        book = FakeBook((("strayA", "xf-sync-aaaa.md", DIFFERENT),
                         ("strayB", "xf-sync-bbbb.md", DIFFERENT_2)))
        with _driving(book) as (_out, _sleeps):
            with self.assertRaises(RuntimeError) as caught:
                sync.add_text_source(HANDLE, PROJECTED, TITLE)
        msg = str(caught.exception)
        self.assertIn("strayA", msg)
        self.assertIn("strayB", msg)
        self.assertEqual(book.adds(), [])
        self.assertEqual(book.renames(), [])
        self.assertEqual(sorted(book.titles()),
                         ["xf-sync-aaaa.md", "xf-sync-bbbb.md"])

    def test_a_stray_FAR_outside_the_tolerance_falls_through_to_a_normal_add(self):
        """With nothing plausibly this document, there is nothing to compound
        and nothing to decide: the pre-existing behaviour, unchanged."""
        book = FakeBook((("other", "xf-sync-unrelated.md", FAR),))
        with _driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        adds = book.adds()
        self.assertEqual(len(adds), 1)
        self.assertIn("--file", adds[0])
        self.assertEqual(book.title_of("other"), "xf-sync-unrelated.md",
                         "an unrelated stray is left exactly as it was")
        self.assertEqual(book.title_of("upload1"), TITLE)
        self.assertIn("uploaded as upload1", out.getvalue())

    def test_no_strays_at_all_falls_through_to_a_normal_add(self):
        book = FakeBook()
        with _driving(book) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertEqual(len(book.adds()), 1)
        self.assertEqual(book.title_of("upload1"), TITLE)
        self.assertIn("renamed on attempt 1", out.getvalue())

    def test_the_normalized_digest_folds_only_defensible_transformations(self):
        """Each normalization is named in the docstring and each is tested; a
        changed WORD is still a different document."""
        base = "alpha\nbeta caf\u00e9\n"
        self.assertEqual(sync._normalized_digest(base),
                         sync._normalized_digest("alpha\r\nbeta caf\u00e9\r\n"))
        self.assertEqual(sync._normalized_digest(base),
                         sync._normalized_digest("alpha   \nbeta caf\u00e9\t\n"))
        self.assertEqual(sync._normalized_digest(base),
                         sync._normalized_digest(base + "\n\n\n"))
        self.assertEqual(sync._normalized_digest(base),           # NFD == NFC
                         sync._normalized_digest("alpha\nbeta cafe\u0301\n"))
        # the JSON envelope is unwrapped first, like the strict digest
        self.assertEqual(sync._normalized_digest(base),
                         sync._normalized_digest(
                             json.dumps({"value": {"content": base}})))
        self.assertNotEqual(sync._normalized_digest(base),
                            sync._normalized_digest("alpha\nbeta tea\n"))


class RenameSettleTests(unittest.TestCase):
    """Hole (b): the read-back proved a moment. Now it proves a steady state."""

    def test_the_settle_reverify_reads_the_title_back_AFTER_the_delay(self):
        book = FakeBook()
        with _driving(book) as (out, sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        text = out.getvalue()
        self.assertIn("renamed on attempt 1", text)
        self.assertIn("settle re-verify: title held", text)
        self.assertIn(sync.RENAME_SETTLE_DELAY_S, sleeps,
                      "the settle delay must actually be waited out")
        # the re-read happens AFTER the delay, which is the whole point: a read
        # before it would prove the same moment the poll already proved
        marker = book.calls.index(("SETTLE-SLEEP", 1))
        self.assertTrue(
            any(c[:2] == ("source", "list") for c in book.calls[marker:]),
            "the title must be READ BACK after the settle delay")

    def test_a_title_that_REGRESSES_after_the_settle_delay_RAISES(self):
        """The live failure: the poll passed on attempt 1, the manifest was
        written, the run exited 0, and the title reverted to the temp filename
        when ingestion completed. That must be the loud path, never exit 0."""
        book = FakeBook()

        def restamp(_nth):
            # the provider re-stamps the title when ingestion completes —
            # every time, including after the one re-rename
            book.set_title("upload1", "xf-sync-fresh.md")

        with _driving(book, on_settle=restamp) as (out, _sleeps):
            with self.assertRaises(RuntimeError) as caught:
                sync.add_text_source(HANDLE, PROJECTED, TITLE)
        msg = str(caught.exception)
        self.assertIn("REGRESSED", msg)
        self.assertIn("upload1", msg)
        self.assertIn("nlm source rename", msg)
        self.assertIn("do NOT re-run the sync", msg)
        self.assertIn("settle re-verify: title REGRESSED", out.getvalue())
        # BOUNDED: the original rename plus exactly one retry, never a loop
        self.assertEqual(len(book.renames()), 2)
        self.assertEqual(book.title_of("upload1"), "xf-sync-fresh.md")

    def test_ONE_re_rename_repairs_a_regression_and_the_run_continues(self):
        """A retry is cheap and, by the second settle, ingestion has had longer
        to finish — which is the state in which the live hand repair held."""
        book = FakeBook()

        def restamp_once(nth):
            if nth == 1:
                book.set_title("upload1", "xf-sync-fresh.md")

        with _driving(book, on_settle=restamp_once) as (out, _sleeps):
            sync.add_text_source(HANDLE, PROJECTED, TITLE)
        text = out.getvalue()
        self.assertIn("settle re-verify: title REGRESSED", text)
        self.assertIn("title held after one re-rename", text)
        self.assertEqual(len(book.renames()), 2)
        self.assertEqual(book.title_of("upload1"), TITLE)

    def test_an_ADOPTED_stray_is_settle_verified_too(self):
        """Adoption renames through the same helper, so a stray adopted into
        place and then re-stamped must be just as loud as a fresh upload."""
        book = FakeBook((("stray1", "xf-sync-deadbeef.md", PROJECTED),))

        def restamp(_nth):
            book.set_title("stray1", "xf-sync-deadbeef.md")

        with _driving(book, on_settle=restamp) as (_out, _sleeps):
            with self.assertRaises(RuntimeError) as caught:
                sync.add_text_source(HANDLE, PROJECTED, TITLE)
        self.assertIn("REGRESSED", str(caught.exception))
        self.assertEqual(book.adds(), [],
                         "a regressed adoption must not become a fresh upload")


if __name__ == "__main__":  # pragma: no cover - parity with the sibling suite
    unittest.main()
