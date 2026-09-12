"""ONE DEFINITION OF A LINE FOR THE CARVE FLOOR (RULED Q-L8 (c)).

`docs/opendox-carve-manifest.yaml` declares 1422 EDIT LINES BY NUMBER, and two
tools read those numbers: `scripts/validate-carve-manifest.py` bounds them
against the blob at `carve_commit` (a declared line the file does not have
cannot be checked at the destination), and `scripts/verify-carve-arrival.py`
decides at the destination whether the arrived blob differs from the carve blob
ONLY on them. A number is a claim about a NUMBERING, so the two tools must
share one, and they did not.

THE DEFECT THIS FILE EXISTS TO CLOSE, measured by carve leg 3's author and
confirmed by its independent verifier (`opensoft/openxFactory#656`, 2026-09-10):
the validator counted `b"\\n"` on the raw bytes while the arrival verifier used
`str.splitlines()`, which ALSO breaks on `\\v`, `\\f`, `\\x1c`, `\\x1d`,
`\\x1e`, `\\x85`, `U+2028` and `U+2029`. Three rows of the landed manifest carry
`U+2028` inside a line, two of them `moved_with_declared_edit` rows to
`openxdox_code`:

  * `tests/ideation-dashboard/test_gate_console.py` — 3 occurrences, the first
    on `\\n`-line 795; the file is 2364 lines by `b"\\n"` and 2367 by
    `splitlines()`, so its declared lines 870, 1627, 1785, 1786 and 1810 named
    ONE line here and a different line there.
  * `tests/ideation-dashboard/test_round_trip.py` — 4 occurrences, the first on
    `\\n`-line 113; 734 lines against 738, so its declared line 728 diverged.

Six declared lines were therefore UNAPPLIABLE at the destination through no
fault of the leg: the verifier read line numbers the validator had never
issued. Leg 3 left all six among its 59 unapplied lines and reported the cause
rather than narrowing around it.

THE DEFINITION, and it is the one the manifest's authors already counted in:

    A LINE IS A `\\n`-TERMINATED RECORD OF THE RAW BYTES. Line N is the Nth
    such record, 1-based. A trailing `\\n` closes the last record and does not
    open another; empty content has no lines.

WHY THIS ONE AND NOT `splitlines()`. It is what the validator already did, what
`git diff`, `grep -n` and every editor show an operator, and what the manifest's
own line numbers were written from — proven per line rather than assumed: at
`b075fd91` each of those six numbers names exactly the `import rewrites` or
`path constants` text its row's note describes under THIS definition and names
unrelated text under `splitlines()`. The alternative would have meant
RE-DECLARING lines in the manifest so that a numbering no human tool shows
became the floor's, which is the wrong half to move.

`\\r` IS NOT A TERMINATOR HERE, and the `\\r` of a `\\r\\n` pair stays in the
record's content. That follows from the definition rather than being bolted
onto it — the record is the bytes BETWEEN the `\\n`s — and it is the stronger
reading: a CRLF/LF flip on a line becomes a change AT THAT LINE NUMBER, which
the arrival verifier can name and hold to the row's declaration, instead of
vanishing into "a change no line number can name". A lone `\\r` (an old Mac
line ending) opens no record, so a file written that way is ONE line to this
floor, exactly as it is one line to `git diff`.

THE ONE DIFFERENCE THE RECORDS CANNOT EXPRESS is a final newline gained or
lost: `b"a\\nb\\n"` and `b"a\\nb"` have the same records. The arrival verifier
keeps a refusal for that case — bytes differing while records do not — because
no line number can name it and it must not pass as "no changed line".

NEITHER TOOL RE-IMPLEMENTS THIS. Both import this module rather than carrying a
copy, and `tests/carve_manifest/test_carve_manifest.py` asserts by AST that
neither file splits lines by any other route — the drift this file exists to
end is not the kind a reader spots in review, because both spellings look
correct in isolation and disagree only on a corpus nobody reads by eye.
"""

from __future__ import annotations

# The floor's sentence, in one place, so `docs/opendox-cutover-runbook.md`
# § 2.1, both tools' refusals and the tests quote one string rather than four
# paraphrases that can drift the way the implementations did.
DEFINITION = ("a line is a `\\n`-terminated record of the raw bytes; line N is "
              "the Nth such record, 1-based, a trailing newline closes the "
              "last record without opening another, and `\\r` is content and "
              "not a terminator")

TEXT_ENCODING = "utf-8"
TEXT_ERRORS = "surrogateescape"


def records(content: bytes) -> list[bytes]:
    """The lines of `content`, as the raw bytes between the `\\n`s.

    Equal by construction to `content.count(b"\\n") + (0 if not content or
    content.endswith(b"\\n") else 1)` in LENGTH — the expression
    `validate-carve-manifest.py` carried inline before this module existed, and
    `tests/carve_manifest/test_carve_manifest.py` pins the equality over a
    corpus including every separator `splitlines()` would have added, so the
    refactor is provably numbering-preserving for the tool whose numbering the
    manifest was written in.
    """
    parts = content.split(b"\n")
    if parts and parts[-1] == b"":
        # A trailing `\n` CLOSES the last record; it does not open an empty
        # one. `b""` itself lands here too and is zero lines, which is what the
        # validator's `not content` guard said.
        parts.pop()
    return parts


def count(content: bytes) -> int:
    """How many lines `content` has — the upper bound a declared line must
    satisfy."""
    return len(records(content))


def text_records(content: bytes) -> list[str]:
    """`records()` decoded for `difflib` and for a unified-diff excerpt.

    `surrogateescape` because a carve blob is whatever git holds: the floor's
    question is which LINE changed, and a file that is not valid UTF-8 must
    still be answerable rather than raising `UnicodeDecodeError` out of a
    comparison. The decode is per record and after the split, so the split
    itself never depends on the encoding — which is half of why `splitlines()`
    was the wrong instrument: it made the answer depend on Unicode's opinion of
    what a line separator is.
    """
    return [record.decode(TEXT_ENCODING, TEXT_ERRORS)
            for record in records(content)]
