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
import io
import itertools
from collections.abc import Callable, Generator
from pathlib import Path
from unittest.mock import patch

from notebooklm_sync.nlm_client import ProviderResult

from tests.notebooklm.typed_sync_contracts import load_typed_sync

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "sync-notebooklm-books.py"
sync = load_typed_sync()
TITLE = "[spec] openxFactory: ideation-dashboard"
HANDLE = "nbX"
PROJECTED = "".join(f"line {n}: {'x' * 40} café\n" for n in range(200))
TRANSFORMED = PROJECTED.replace("café", "café").replace("\n", "  \r\n") + "\n\n"
DIFFERENT = PROJECTED.replace("line 7:", "LINE 7:").replace("line 9:", "LINE 9:")
DIFFERENT_2 = PROJECTED.replace("line 3:", "LINE 3:")
FAR = PROJECTED + "y" * 20000


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
        self.sources: list[dict[str, str]] = [
            {"id": sid, "title": title} for sid, title, _b in strays
        ]
        self.bodies: dict[str, str] = {sid: body for sid, _t, body in strays}
        self.calls: list[tuple[str | int, ...]] = []
        self._ids: itertools.count[int] = itertools.count(1)

    def __call__(self, *args: str, parse: bool = True) -> ProviderResult:
        del parse
        self.calls.append(args)
        head = args[:2]
        if head == ("source", "list"):
            rows: ProviderResult = [dict(r) for r in self.sources]
            return rows
        if head == ("source", "content"):
            return self.bodies.get(args[2], "")
        if head == ("source", "add"):
            sid = f"upload{next(self._ids)}"
            self.sources.append({"id": sid, "title": "xf-sync-fresh.md"})
            return f"Added source: xf-sync-fresh.md\nSource ID: {sid}\n"
        if head == ("source", "rename"):
            for row in self.sources:
                if row["id"] == args[2]:
                    row["title"] = args[3]
            return ""
        raise AssertionError(f"unexpected nlm call: {args}")

    def adds(self) -> list[tuple[str | int, ...]]:
        return [c for c in self.calls if c[:2] == ("source", "add")]

    def renames(self) -> list[tuple[str | int, ...]]:
        return [c for c in self.calls if c[:2] == ("source", "rename")]

    def titles(self) -> list[str]:
        return [r["title"] for r in self.sources]

    def title_of(self, source_id: str) -> str:
        return next((r["title"] for r in self.sources if r["id"] == source_id), "")

    def set_title(self, source_id: str, title: str) -> None:
        for row in self.sources:
            if row["id"] == source_id:
                row["title"] = title


def sleeper(
    book: FakeBook | None = None, on_settle: Callable[[int], None] | None = None
) -> tuple[list[float], Callable[[float], None]]:
    """A no-op `time.sleep` that RECORDS, and optionally lets a test act during
    the settle window — the one place a provider's re-stamp can arrive.

    Also drops a marker into the call log so a test can assert the settle
    re-verify's read happened AFTER the delay, not merely that a delay happened.
    """
    sleeps: list[float] = []
    settles = itertools.count(1)

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        if seconds == sync.RENAME_SETTLE_DELAY_S:
            nth = next(settles)
            if book is not None:
                book.calls.append(("SETTLE-SLEEP", nth))
            if on_settle is not None:
                on_settle(nth)

    return (sleeps, sleep)


@contextlib.contextmanager
def driving(
    book: FakeBook, *, on_settle: Callable[[int], None] | None = None
) -> Generator[tuple[io.StringIO, list[float]], None, None]:
    """Run the oversized path against `book`, capturing stdout and sleeps."""
    sleeps, sleep = sleeper(book, on_settle)
    out = io.StringIO()
    with (
        patch.object(sync, "nlm", book),
        patch.object(sync, "MAX_TEXT_ARG_BYTES", 200),
        patch.object(sync.time, "sleep", sleep),
        contextlib.redirect_stdout(out),
    ):
        yield (out, sleeps)
