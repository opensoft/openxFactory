"""The COMMITTED intent feed — the corpus half of the hosted intent plane
(`add-ideation-intent-plane` task 4.4, Brett Heap's ruling D-1 on
openxFactory #656).

RULING D-1, in one sentence: *the applied/refused feed is SERVED FROM THE
CORPUS* — the dashboard reads the intent files the apply lane already
committed under `ideation/dashboard/intents/`, read-only, beside the inbox's
live pending list. No new write path, and the serving pod stays
credential-free (design D16). This module is that read, and nothing else: it
walks a directory, parses what it finds, and hands back records. It opens
nothing, writes nothing, and reaches no network.

WHY IT PARSES YAML BY HAND (the one surprising thing here).

The hosted dashboard image is `python:3.12-slim` plus the repository's own
modules and NO pip dependencies — `containers/ideation-dashboard/Dockerfile`
in Omnigent-Install says so in as many words, and `corpus_root.py` already
carries the same constraint for the startup path ("importing the generator
there would newly require PyYAML in the served image's startup path"). PyYAML
is therefore NOT importable in the pod that has to answer this route, and the
committed intents are YAML. So the reader is stdlib-only.

It is not a YAML implementation and does not pretend to be. It reads exactly
ONE shape: `yaml.safe_dump(<flat mapping of scalars plus the two one-level
sub-mappings `target` and `args`>, sort_keys=False)` preceded by the lane's
`#` banner — which is the only shape `intent_apply_lane._write_intent` can
emit, because the document it dumps is rebuilt field by field from validated
values in `_terminal_intent`. Anything it cannot read confidently is SKIPPED,
never guessed at: a malformed file drops out of the feed rather than
poisoning it.

That is a real risk to take on, so it is discharged by test rather than by
assertion: `tests/ideation-dashboard/test_intent_feed.py` runs PyYAML — which
the TEST environment does have — as an oracle over a wide matrix of emitted
values (unicode, folded long lines, embedded quotes and colons and newlines,
number-like and bool-like strings) and requires this reader to agree with it
document for document, plus a round-trip over intents written by the REAL
apply lane. One runtime code path, one independent oracle.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

#: Where the apply lane commits intents. Deliberately RESTATED rather than
#: imported from `intent_apply_lane`, which imports PyYAML at module scope and
#: so cannot be imported by the serving pod at all. The two definitions are
#: held together by a test (`test_the_intents_dir_matches_the_apply_lane`) —
#: the same "one definition, guarded" posture `corpus_root.SCANNED_ROOTS`
#: takes toward `doc_health.corpus.GOVERNED_ROOTS`.
INTENTS_DIR = "ideation/dashboard/intents/"

#: The lane's filename suffix (`intent_relpath`).
INTENT_SUFFIX = ".gate-intent.yaml"

#: Only TERMINAL intents are ever committed: the lane writes `applied` or
#: `refused` and nothing else (its module docstring: "every refusal is
#: WRITTEN as a status: refused intent and committed"). A `pending` file
#: would mean the corpus disagrees with the lane, so it is not served.
TERMINAL_STATUSES = ("applied", "refused")

#: Mirrored from `intent_apply_lane.VERB_TARGET_KEY` (grow together; the same
#: test guards this pair).
VERB_TARGET_KEY = {
    "demote": "change_id",
    "edit-apply": "change_id",
    "ratify": "change_id",
    "kickoff": "change_id",
    "dispose-possible": "possible_id",
    "propose": "topic_id",
    "promote-to-staging": "possible_id",
    "derive-possibles": "cluster_id",
    "research-brief": "possible_id",
    "create-project": "project_id",
    "edit-project": "project_id",
}

#: Bounds. The feed is a read of an unbounded, append-only directory served to
#: an unauthenticated-to-this-pod browser, so every axis is capped: how many
#: files are opened per request, how big a file is read at all, and how many
#: records come back. A request past the cap gets `truncated: true` and says
#: so, rather than being silently short.
MAX_FILES = 2000
MAX_FILE_BYTES = 64 * 1024
DEFAULT_LIMIT = 200
MAX_LIMIT = 1000

_KEY_LINE = re.compile(r"^(?P<indent> *)(?P<key>[A-Za-z_][A-Za-z0-9_.-]*):"
                       r"(?: +(?P<value>.*))?$")
_HEX = "0123456789abcdefABCDEF"
_INT = re.compile(r"^[-+]?[0-9]+$")
_FLOAT = re.compile(r"^[-+]?(?:[0-9]*\.[0-9]+|[0-9]+\.[0-9]*)$")


# --------------------------------------------------------------------------
# the reader
# --------------------------------------------------------------------------

def _fold(chunks: list[str]) -> str:
    """YAML flow folding over the raw lines of ONE scalar: a single line break
    becomes a space, N consecutive breaks become N-1 literal newlines, the
    indentation of a continuation line is not content, and trailing whitespace
    is content ONLY on the last line (everywhere else a break follows it and
    strips it)."""
    if not chunks:
        return ""
    last = len(chunks) - 1
    norm = []
    for idx, raw in enumerate(chunks):
        piece = raw if idx == 0 else raw.lstrip(" \t")
        norm.append(piece if idx == last else piece.rstrip(" \t"))
    out = norm[0]
    blanks = 0
    for idx in range(1, len(norm)):
        piece = norm[idx]
        if piece == "" and idx != last:
            blanks += 1
            continue
        out += ("\n" * blanks) if blanks else " "
        out += piece
        blanks = 0
    return out


def _decode_double(body: str) -> str | None:
    """Decode the inside of a double-quoted YAML scalar. Handles exactly the
    escapes PyYAML's emitter produces (`\\\\`, `\\"`, `\\n`, `\\t`, `\\r`,
    `\\0`, `\\ `, `\\xNN`, `\\uNNNN`, `\\UNNNNNNNN`) plus the escaped line
    break it uses to fold a long line. Returns None on anything else — an
    unreadable value must skip its document, never become a wrong one."""
    simple = {"\\": "\\", '"': '"', "n": "\n", "t": "\t", "r": "\r",
              "0": "\0", "a": "\a", "b": "\b", "f": "\f", "v": "\v",
              "e": "\x1b", " ": " ", "/": "/", "N": "\x85", "_": "\xa0"}
    out: list[str] = []
    i = 0
    pending_break = False       # an UNescaped break: folds to one space
    blanks = 0
    while i < len(body):
        ch = body[i]
        if ch == "\n":
            # look ahead: consecutive breaks are literal newlines (N -> N-1)
            j = i
            while j < len(body) and body[j] in "\n":
                j += 1
                # a line that is only whitespace counts as a blank line
                k = j
                while k < len(body) and body[k] in " \t":
                    k += 1
                if k < len(body) and body[k] == "\n":
                    j = k
                else:
                    break
            breaks = body[i:j].count("\n")
            blanks = breaks - 1
            pending_break = True
            i = j
            # strip the continuation line's indentation
            while i < len(body) and body[i] in " \t":
                i += 1
            continue
        if pending_break:
            out.append("\n" * blanks if blanks else " ")
            pending_break = False
            blanks = 0
        if ch != "\\":
            out.append(ch)
            i += 1
            continue
        i += 1
        if i >= len(body):
            return None
        esc = body[i]
        if esc == "\n":                     # escaped break: removed entirely
            i += 1
            while i < len(body) and body[i] in " \t":
                i += 1
            pending_break = False
            blanks = 0
            continue
        if esc in simple:
            out.append(simple[esc])
            i += 1
            continue
        widths = {"x": 2, "u": 4, "U": 8}
        if esc in widths:
            width = widths[esc]
            hexes = body[i + 1:i + 1 + width]
            # `int(..., 16)` accepts underscores and surrounding whitespace,
            # neither of which is a YAML hex escape — check the digits first so
            # a malformed escape SKIPS rather than decoding to a wrong char.
            if len(hexes) != width or not all(c in _HEX for c in hexes):
                return None
            try:
                out.append(chr(int(hexes, 16)))
            except ValueError:
                return None
            i += 1 + width
            continue
        return None
    if pending_break:                      # a body ending on a folded break
        out.append("\n" * blanks if blanks else " ")
    return "".join(out)


def _decode_single(body: str) -> str:
    """Decode the inside of a single-quoted YAML scalar: `''` is a literal
    quote and line breaks fold exactly as a plain scalar's do."""
    folded = _fold(body.split("\n"))
    return folded.replace("''", "'")


def _resolve_plain(text: str):
    """The core YAML type resolution a plain scalar gets. Only the forms a
    committed intent can actually carry: `schema_version: 1` is an int, the
    empty flow collections the emitter uses for `args: {}`, and everything
    else the lane writes is a string.

    A plain scalar can never BEGIN with an indicator character — the emitter
    quotes any value that would (`'&amp start'`, `'*star'`, `'|pipe'`) — so a
    leading indicator means a real YAML construct this reader does not
    implement, and that is unreadable rather than text."""
    if text in ("{}", "[]"):
        return {} if text == "{}" else []
    if text[:1] in ("{", "[", "&", "*", "!", "|", ">", "%", "@", "`"):
        return _UNREADABLE
    if text in ("", "~", "null", "Null", "NULL"):
        return None
    if text in ("true", "True", "TRUE"):
        return True
    if text in ("false", "False", "FALSE"):
        return False
    if _INT.match(text):
        return int(text)
    if _FLOAT.match(text):
        return float(text)
    return text


def _scalar(first: str, lines: list[str], start: int, indent: int):
    """Read ONE scalar beginning with `first` on line `start - 1`, consuming
    the continuation lines that belong to it.

    Returns `(value, next_index)`, or `(_UNREADABLE, next_index)` when the
    value cannot be decoded confidently."""
    i = start
    if first[:1] in ('"', "'"):
        quote = first[0]
        raw = first
        # accumulate until the quote closes (an escaped quote does not close
        # a double-quoted scalar; a doubled one does not close a single).
        while not _closes(raw, quote):
            if i >= len(lines):
                return _UNREADABLE, i
            raw += "\n" + lines[i]
            i += 1
        body = raw[1:raw.rindex(quote)]
        trailing = raw[raw.rindex(quote) + 1:].strip()
        if trailing and not trailing.startswith("#"):
            return _UNREADABLE, i
        if quote == '"':
            decoded = _decode_double(body)
            return (_UNREADABLE if decoded is None else decoded), i
        return _decode_single(body), i
    # plain scalar: continuation lines are more-indented (or blank)
    chunks = [first]
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            chunks.append("")
            i += 1
            continue
        if len(line) - len(line.lstrip(" ")) <= indent:
            break
        chunks.append(line)
        i += 1
    while chunks and chunks[-1] == "":       # trailing blanks are not content
        chunks.pop()
        i -= 1
    return _resolve_plain(_fold(chunks).strip()), i


def _closes(raw: str, quote: str) -> bool:
    """Does `raw` contain a complete quoted scalar starting at its first
    character?"""
    i = 1
    while i < len(raw):
        ch = raw[i]
        if quote == '"':
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                return True
        else:
            if ch == "'":
                if raw[i + 1:i + 2] == "'":
                    i += 2
                    continue
                return True
        i += 1
    return False


class _Unreadable:
    def __repr__(self) -> str:      # pragma: no cover - debugging aid only
        return "<unreadable>"


_UNREADABLE = _Unreadable()


def parse_intent_document(text: str) -> dict | None:
    """Parse ONE committed `.gate-intent.yaml` into a mapping, or None when the
    document is not the shape the apply lane emits.

    Reads the top-level mapping plus its one-level sub-mappings (`target`,
    `args`). A sub-mapping member that is itself a collection is DROPPED — the
    feed's contract is the terminal fields, and `args` is decoration — but a
    top-level key that cannot be read at all fails the whole document."""
    lines = [line.rstrip("\r") for line in text.split("\n")]
    doc: dict = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#") or stripped == "---":
            i += 1
            continue
        if stripped == "...":
            break
        match = _KEY_LINE.match(line)
        if match is None or match.group("indent"):
            return None                       # not a top-level mapping key
        key = match.group("key")
        raw = (match.group("value") or "").strip()
        i += 1
        if raw and not raw.startswith("#"):
            value, i = _scalar(raw, lines, i, 0)
            if value is _UNREADABLE:
                return None
            doc[key] = value
            continue
        # a block: the indented lines that follow are a flat sub-mapping
        block: dict = {}
        last_key: str | None = None
        while i < len(lines):
            child = lines[i]
            if child.strip() == "":
                i += 1
                continue
            child_indent = len(child) - len(child.lstrip(" "))
            if child_indent == 0:
                break
            sub = _KEY_LINE.match(child)
            if sub is None:
                # A block sequence's `- item` lines sit at the PARENT key's own
                # indent, so they arrive here. `args` is decoration, not the
                # feed's contract, so an unreadable member is dropped and the
                # document survives — the terminal fields are all top-level.
                block.pop(last_key, None)
                i += 1
                continue
            last_key = sub.group("key")
            sub_raw = (sub.group("value") or "").strip()
            i += 1
            if not sub_raw or sub_raw.startswith("#"):
                # a nested collection: skip its body, drop the member
                while i < len(lines) and (
                        lines[i].strip() == ""
                        or len(lines[i]) - len(lines[i].lstrip(" ")) > child_indent):
                    i += 1
                continue
            value, i = _scalar(sub_raw, lines, i, child_indent)
            if value is _UNREADABLE:
                block.pop(last_key, None)
                continue
            block[last_key] = value
        doc[key] = block
    return doc or None


# --------------------------------------------------------------------------
# the feed record
# --------------------------------------------------------------------------

def target_id(verb, target) -> str | None:
    """The verb's ONE target id — the join key the browser decorates tiles by
    (`intent_apply_lane.canonical_target`, same rule)."""
    key = VERB_TARGET_KEY.get(verb)
    if key is None or not isinstance(target, dict):
        return None
    value = target.get(key)
    return value if isinstance(value, str) and value else None


def feed_record(doc, *, path: str | None = None) -> dict | None:
    """Normalize a parsed intent into the feed's wire record, or None when it
    is not a terminal `gate-intent` this feed may serve.

    Rebuilt field by field from validated values — never a copy of the parsed
    document — for the same reason `intent_apply_lane._terminal_intent` does
    it: a stray or junk key must not ride out to the client as if the lane had
    written it."""
    if not isinstance(doc, dict):
        return None
    if doc.get("kind") != "gate-intent" or doc.get("schema_version") != 1:
        return None
    status = doc.get("status")
    if status not in TERMINAL_STATUSES:
        return None
    verb = doc.get("verb")
    if verb not in VERB_TARGET_KEY:
        return None
    tid = target_id(verb, doc.get("target"))
    if tid is None:
        return None
    actor = doc.get("actor")
    if not isinstance(actor, str) or not actor.strip():
        return None
    args = doc.get("args")
    record = {
        "kind": "gate-intent",
        "schema_version": 1,
        "actor": actor,
        "verb": verb,
        "target": {VERB_TARGET_KEY[verb]: tid},
        "target_id": tid,
        "args": {k: v for k, v in (args or {}).items()
                 if isinstance(v, (str, int, float, bool))}
        if isinstance(args, dict) else {},
        "requested_at": _text(doc.get("requested_at")),
        "snapshot_rev_seen": _text(doc.get("snapshot_rev_seen")),
        "status": status,
        "idempotency_key": _text(doc.get("idempotency_key")),
        "source": "corpus",
    }
    if status == "refused":
        # A silent refusal is invalid (the delta's "A refused intent is
        # visible" scenario). A refused file with no reason is not served as a
        # reasonless refusal — it is skipped, and the file is the defect.
        reason = _text(doc.get("refusal_reason"))
        if not reason:
            return None
        record["refusal_reason"] = reason
    else:
        applied_record = _text(doc.get("applied_record"))
        if not applied_record:
            return None
        record["applied_record"] = applied_record
        applied_at = _text(doc.get("applied_at"))
        if applied_at:
            record["applied_at"] = applied_at
    if path:
        record["path"] = path
    return record


def _text(value) -> str:
    return value.strip() if isinstance(value, str) else ""


def _when(record: dict) -> datetime:
    """Newest-first ordering. RFC 3339 with mixed offsets and mixed precision
    does not sort lexically, so it is parsed; an unparseable stamp sorts
    oldest rather than failing the request."""
    raw = record.get("applied_at") or record.get("requested_at") or ""
    text = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


# --------------------------------------------------------------------------
# the directory walk
# --------------------------------------------------------------------------

def read_committed_intents(checkout_root, *, actor: str | None = None,
                           status: str | None = None,
                           target: str | None = None,
                           limit: int = DEFAULT_LIMIT,
                           intents_dir: str = INTENTS_DIR) -> dict:
    """The feed document for one request.

    Absent or empty directory -> an empty feed, never an error: a checkout
    with no intents yet is the ordinary first state, and the hosted overlay
    must render "nothing yet" rather than "the feed is broken"."""
    limit = max(1, min(int(limit or DEFAULT_LIMIT), MAX_LIMIT))
    base = Path(checkout_root) / intents_dir
    records: list[dict] = []
    scanned = 0
    skipped = 0
    truncated = False
    try:
        paths = sorted(base.rglob("*" + INTENT_SUFFIX)) if base.is_dir() else []
    except OSError:
        paths = []
    for path in paths:
        if scanned >= MAX_FILES:
            truncated = True
            break
        scanned += 1
        try:
            if path.stat().st_size > MAX_FILE_BYTES:
                skipped += 1
                continue
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            skipped += 1
            continue
        try:
            rel = path.relative_to(Path(checkout_root)).as_posix()
        except ValueError:                       # pragma: no cover - defensive
            rel = None
        record = feed_record(parse_intent_document(text), path=rel)
        if record is None:
            skipped += 1
            continue
        if actor and record["actor"] != actor:
            continue
        if status and record["status"] != status:
            continue
        if target and record["target_id"] != target:
            continue
        records.append(record)
    records.sort(key=_when, reverse=True)
    if len(records) > limit:
        records = records[:limit]
        truncated = True
    return {
        "kind": "committed-intent-feed",
        "intents": records,
        "truncated": truncated,
        "scanned": scanned,
        "skipped": skipped,
    }
