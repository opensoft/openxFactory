"""Deterministic per-document completeness + staged-topic health scoring
(openxFactory `add-staging-workbench`, design D1/D2/D8; change tasks 2.1-2.4).

THE ONE SCORING MODULE. Two callers only: the generator (which emits
`documents[].completeness` and `staged_topics[].health` into the snapshot) and
the propose route's readiness guard (which recomputes ONE topic's health LIVE
from the pinned checkout at request time, design D9). One implementation, one
set of constants, so the rendered bar and the refusal message can never
disagree.

EVERY FUNCTION HERE IS PURE. No file read, no network, no clock, no model call,
no randomness, no module state — the module imports `re` and
`doc_health.lines.split_keepends` (itself pure: `re` and nothing else, no I/O)
and nothing beyond those two, which is the structural half of design D1's
guarantee: the score is a function of the pinned tree alone, so the same tree
yields a BYTE-IDENTICAL snapshot (the promoted spec's first scenario) and a
rising-score scenario is fixture-testable. Text and derived maps arrive as
ARGUMENTS from the generator, which has already loaded them.

`_Prepared.lines` is REAL lines (CR/LF/CRLF only), not `str.splitlines()`
pseudo-lines, since `align-status-reader-to-real-lines`'s wide ruling
(2026-08-19, finding F4): `_has_header` reads the SAME six lifecycle header
fields, in the SAME 15-line window, as `doc_health.corpus.parse_status`/
`parse_kind` and `authoring.missing_required_headers` — see this module's
`GOVERNANCE_HEADER_FIELDS`/`HEADER_WINDOW` comment — and a wider split here
than there is the exact divergence that change exists to close: a document
whose header carries an exotic separator could get `authoring` saying its
header block is COMPLETE (real lines) and `completeness` saying
`governance_header_block` is ABSENT (pseudo-lines), demonstrated. Converting
`_Prepared.lines` alone fixes every consumer coherently — `_headings`,
`_has_heading`, `_has_header`, the `h1_title`/`section` structural checks, and
`_open_question_items` all already treat `.lines` as an opaque `Sequence[str]`
of "the document's lines," so none of them needed to change.

The five signals are deliberately STRUCTURAL PROXIES, not an assessment of
quality (design D1 consequence): a well-formed empty argument scores well. The
judgment-shaped question ("is this topic ready?") belongs to the human clicking
propose after the gate clears, and cluster readiness keeps its own three-tier
authorities. The per-document score's ONE sanctioned gate consumer is the
staged-to-proposal readiness gate, and even it reads scores only through
`topic_health` — never a per-document score directly, never a doc-health
finding.

  * `structure` — the fraction of the document's EXPECTED structural elements
    present. The expected set is fixed per `Kind:` in ONE table
    (`STRUCTURE_ELEMENTS`) over ONE predicate table (`ELEMENT_CHECKS`), with the
    common fallback (H1 title, the governance header block, at least one
    section) as that table's `None` entry — never scattered through the checks.
  * `length` — body word count against a fixed saturation threshold, so padding
    past the threshold cannot outscore substance.
  * `open_markers` — an INVERSE signal: the STANDING open-item count against a
    fixed saturation count, subtracted from 1, so more standing items always
    scores LOWER. Standing items are the `TODO`/`TBD`/`FIXME`/`??` tokens plus
    unresolved open-question items (see `_open_question_items` for the two
    resolution conventions the corpus actually uses).
  * `keyword_coverage` — the fraction of the document's declared `Topics:`
    subjects that resolve to the snapshot's keyword vocabulary.
  * `link_degree` — the document's snapshot edge degree (cluster document edges
    plus `destinations` staged topics / changes / capabilities) against a fixed
    saturation degree.

Every signal is reported as `{"value": <normalized 0..1>, "count": <raw>}` — the
normalized value beside the raw measurement that produced it, so a rendered bar
is always explainable in the signal's own terms, and the `score` is
recomputable from the emitted values by anyone holding `WEIGHTS`.

The weights, the saturation constants, the decimal precision, and
`READY_MIN_SCORE` are v1 CONTRACT CONSTANTS (design D2): a per-run input would
make the same tree yield different snapshots, and a committed config would make
every score a function of two inputs instead of one. A tunable configuration is
a plausible successor (design open question 1) and would have to pin the weights
INTO the snapshot beside the scores.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from doc_health.lines import split_keepends

# --------------------------------------------------------------------------
# v1 contract constants (design D2 — fixed, never a per-run input)
# --------------------------------------------------------------------------

#: Decimal places every emitted `value`/`score`/mean carries. Fixed precision is
#: not cosmetic: it is what keeps the rendered JSON byte-identical across runs
#: and platforms (a raw IEEE weighted sum is not).
PRECISION = 4

#: The fixed-weight combination. Sums to exactly 1.0, so `score` is itself a
#: normalized 0..1 value. Order is the emission/spec order of the five signals.
WEIGHTS: dict[str, float] = {
    "structure": 0.30,
    "length": 0.15,
    "open_markers": 0.25,
    "keyword_coverage": 0.10,
    "link_degree": 0.20,
}
SIGNAL_NAMES: tuple[str, ...] = tuple(WEIGHTS)

#: Body words at which `length` saturates at 1.0.
LENGTH_SATURATION_WORDS = 400
#: Standing open items at which `open_markers` bottoms out at 0.0.
OPEN_MARKER_SATURATION = 5
#: Snapshot edge degree at which `link_degree` saturates at 1.0.
LINK_DEGREE_SATURATION = 6

#: The staged-to-proposal ready bar (design D8; Brett's 2026-07-25 ruling —
#: v1 starts at 0.60, calibrated on the real corpus at realization).
READY_MIN_SCORE = 0.60

#: `staged_topic.health.status` — DERIVED from the blockers, never scored
#: directly (design D8), so the gate and the tile icon can never disagree
#: about WHY.
STATUS_READY = "ready"
STATUS_DEVELOPING = "developing"
STATUS_STUB = "stub"

#: `blockers[].kind` — the two typed, explainable blocker classes.
BLOCKER_STANDING_OPEN_ITEMS = "standing_open_items"
BLOCKER_BELOW_READY_THRESHOLD = "below_ready_threshold"

#: The `destinations` reference lists that count toward `link_degree`.
DESTINATION_KEYS: tuple[str, ...] = ("capabilities", "changes", "staged_topics")

#: The governance header block, and the window it must live in. Both mirror the
#: shared header contract already enforced elsewhere in this package
#: (`authoring.REQUIRED_HEADER_FIELDS`, `doc_health.corpus.STATUS_SCAN_LINES`);
#: they are restated here — rather than imported — to keep this module's import
#: graph empty of anything that touches the filesystem, and a test cross-checks
#: the two definitions so they cannot drift. Since
#: `split-opendox-two-layer-product` § 2.3 the first of those two is the
#: CORPUS's own answer (`classify`) rather than a constant of the dashboard's,
#: so that cross-check now measures this restatement against the corpus
#: itself — which is why keeping this module filesystem-free costs nothing in
#: authority.
GOVERNANCE_HEADER_FIELDS: tuple[str, ...] = (
    "Status", "Kind", "Summary", "Topics", "Repository context", "Captured",
)
HEADER_WINDOW = 15


# --------------------------------------------------------------------------
# text shapes
# --------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
_ITEM_RE = re.compile(r"^(?:[-*+]|\d+[.)])\s+\S")
_HEADER_LINE_RE = re.compile(r"^[A-Z][A-Za-z][A-Za-z ]{0,38}:(?:\s|$)")

# Standing-item tokens. Scanned over the WHOLE document (a `Summary: TBD` is a
# standing item too), counted as occurrences, deliberately including any inside
# fenced code — a marker in an example is still a marker the author left behind.
_MARKER_TOKEN_RE = re.compile(r"\bTODO\b|\bTBD\b|\bFIXME\b|\?\?")

# Open-question sections and the TWO resolution conventions the real corpus
# uses (see `_open_question_items`).
_OPEN_QUESTION_HEADING_RE = re.compile(
    r"^(#{1,6})\s+.*\b(open\s+questions?|unresolved\s+questions?"
    r"|questions?\s+outstanding)\b",
    re.IGNORECASE)
_RESOLVED_HEADING_RE = re.compile(
    r"\b(resolved|answered|closed|decided|settled)\b", re.IGNORECASE)
_RESOLVED_ITEM_RE = re.compile(r"\b(RESOLVED|ANSWERED|CLOSED|DECIDED|SETTLED)\b")

# Structural-element heading patterns (used by ELEMENT_CHECKS below).
_CLAIMS_RE = re.compile(r"\bclaims?\b", re.IGNORECASE)
_TARGET_CAPABILITY_RE = re.compile(r"\btarget\s+capabilit(?:y|ies)\b", re.IGNORECASE)
_EXIT_RE = re.compile(r"\bexit\b", re.IGNORECASE)


class _Prepared:
    """One document's text, split ONCE (design "generator cost": the generator
    already holds the text; every signal is a linear pass over this)."""

    __slots__ = ("text", "lines", "body_words")

    def __init__(self, text: str) -> None:
        self.text = text
        # REAL lines (CR/LF/CRLF only), not `str.splitlines()` pseudo-lines —
        # see the module docstring. `.lines` stays a plain `list[str]` (the
        # body half of each `split_keepends` row; the ending is not needed by
        # any consumer here), so every existing reader of `.lines` keeps its
        # own signature and behavior unchanged.
        self.lines = [body for body, _ending in split_keepends(text)]
        self.body_words = _body_word_count(self.lines)


def _body_word_count(lines: Sequence[str]) -> int:
    """Words in the document BODY: the header block (the H1 title plus the
    `Name: value` governance lines inside the header window) is not body."""
    words = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            continue
        if i < HEADER_WINDOW and _HEADER_LINE_RE.match(line):
            continue
        words += len(line.split())
    return words


def _round(value: float) -> float:
    """The ONE rounding used for every emitted number (fixed precision)."""
    return round(float(value), PRECISION)


def _normalized(raw: int, saturation: int) -> float:
    if saturation <= 0:
        return 0.0
    return _round(min(raw / saturation, 1.0))


def _signal(value: float, count: int) -> dict[str, Any]:
    """The emitted signal shape: normalized value beside the raw count."""
    return {"value": _round(min(max(value, 0.0), 1.0)), "count": int(count)}


# --------------------------------------------------------------------------
# structural elements: ONE predicate table + ONE expected-set table
# --------------------------------------------------------------------------

def _headings(p: _Prepared) -> list[str]:
    return [line for line in p.lines if _HEADING_RE.match(line)]


def _has_heading(p: _Prepared, pattern: re.Pattern[str]) -> bool:
    return any(pattern.search(line) for line in _headings(p))


def _has_header(p: _Prepared, *names: str) -> bool:
    prefixes = tuple(name + ":" for name in names)
    return any(line.startswith(prefixes) and line.split(":", 1)[1].strip()
               for line in p.lines[:HEADER_WINDOW])


ELEMENT_CHECKS: dict[str, Any] = {
    # The common fallback's three elements.
    "h1_title": lambda p: any(line.startswith("# ") for line in p.lines),
    "governance_header_block": lambda p: all(
        _has_header(p, field) for field in GOVERNANCE_HEADER_FIELDS),
    "section": lambda p: any(line.startswith("## ") for line in p.lines),
    # Per-`Kind:` additions.
    "claims": lambda p: _has_heading(p, _CLAIMS_RE),
    "open_questions": lambda p: _has_heading(p, _OPEN_QUESTION_HEADING_RE),
    "target_capability": lambda p: (_has_heading(p, _TARGET_CAPABILITY_RE)
                                    or _has_header(p, "Target capability")),
    "exit_path": lambda p: (_has_heading(p, _EXIT_RE)
                            or _has_header(p, "Exit", "Exit path")),
}

_COMMON_ELEMENTS: tuple[str, ...] = ("h1_title", "governance_header_block", "section")
# The feat-spec shape a staging fragment declares (openxFactory
# `ideation/staging/INDEX.md`): target capability, delta type, claims, open
# questions, exit path.
_FEAT_SPEC_ELEMENTS: tuple[str, ...] = _COMMON_ELEMENTS + (
    "target_capability", "claims", "open_questions", "exit_path")

#: THE expected-structure table. `None` is the common fallback every unlisted
#: (or header-less) `Kind:` falls back to — declared here, once, so growing an
#: expectation is a table edit and never a scattered check.
STRUCTURE_ELEMENTS: dict[str | None, tuple[str, ...]] = {
    None: _COMMON_ELEMENTS,
    "staging-packet": _FEAT_SPEC_ELEMENTS,
    "staging-fragment": _FEAT_SPEC_ELEMENTS,
    "architecture": _COMMON_ELEMENTS + ("claims",),
}


def expected_elements(kind: str | None) -> tuple[str, ...]:
    """The expected structural element set for a `Kind:` value — the table's
    entry, else the common fallback."""
    key = kind.strip().lower() if isinstance(kind, str) and kind.strip() else None
    return STRUCTURE_ELEMENTS.get(key, STRUCTURE_ELEMENTS[None])


# --------------------------------------------------------------------------
# the five signals (public, independently callable, each pure)
# --------------------------------------------------------------------------

def structure(text: str, kind: str | None = None) -> dict[str, Any]:
    """Fraction of the document's expected structural elements present.
    `count` is the number present."""
    return _structure(_Prepared(text), kind)


def _structure(p: _Prepared, kind: str | None) -> dict[str, Any]:
    expected = expected_elements(kind)
    present = sum(1 for name in expected if ELEMENT_CHECKS[name](p))
    return _signal(present / len(expected) if expected else 0.0, present)


def length(text: str) -> dict[str, Any]:
    """Body word count against `LENGTH_SATURATION_WORDS`. `count` is the raw
    word count, so padding past the threshold is visible as a raw number while
    the normalized value stays 1.0."""
    return _length(_Prepared(text))


def _length(p: _Prepared) -> dict[str, Any]:
    return _signal(_normalized(p.body_words, LENGTH_SATURATION_WORDS), p.body_words)


def open_markers(text: str) -> dict[str, Any]:
    """INVERSE signal: `count` standing open items against
    `OPEN_MARKER_SATURATION`, subtracted from 1 — MORE standing items always
    yields a LOWER value."""
    return _open_markers(_Prepared(text))


def _open_markers(p: _Prepared) -> dict[str, Any]:
    count = _standing_open_items(p)
    return _signal(1.0 - _normalized(count, OPEN_MARKER_SATURATION), count)


def standing_open_items(text: str) -> int:
    """The raw standing-open-item count: `TODO`/`TBD`/`FIXME`/`??` tokens plus
    unresolved open-question items."""
    return _standing_open_items(_Prepared(text))


def _standing_open_items(p: _Prepared) -> int:
    return len(_MARKER_TOKEN_RE.findall(p.text)) + _open_question_items(p.lines)


def _open_question_items(lines: Sequence[str]) -> int:
    """Unresolved open-question items, counted section by section.

    TWO resolution conventions, both drawn from how the real corpus closes
    questions, and both deterministic:

      1. SECTION-level — the heading itself declares the resolution
         (`## Open questions — resolved 2026-07-14`). Matched
         case-insensitively, because that is how the corpus writes it; the whole
         section then contributes NOTHING.
      2. ITEM-level — an enumerated question carries an UPPERCASE resolution
         token (`RESOLVED by Brett's ruling`). Uppercase ONLY, deliberately: an
         open question's prose routinely contains the lowercase word
         ("an attestation resolved before answer-release"), and closing a
         question on that would make the gate lie.

    A section with no enumerated items counts as ONE standing item unless its
    text carries an uppercase resolution token.
    """
    total = 0
    i = 0
    n = len(lines)
    while i < n:
        m = _OPEN_QUESTION_HEADING_RE.match(lines[i])
        if not m:
            i += 1
            continue
        level = len(m.group(1))
        if _RESOLVED_HEADING_RE.search(lines[i]):  # convention 1
            i += 1
            continue
        j = i + 1
        while j < n:
            hm = _HEADING_RE.match(lines[j])
            if hm and len(hm.group(1)) <= level:
                break
            j += 1
        total += _unresolved_items(lines[i + 1:j])
        i = j
    return total


def _unresolved_items(section: Sequence[str]) -> int:
    starts = [k for k, line in enumerate(section) if _ITEM_RE.match(line)]
    if not starts:
        return 0 if _RESOLVED_ITEM_RE.search("\n".join(section)) else 1
    count = 0
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(section)
        if not _RESOLVED_ITEM_RE.search("\n".join(section[start:end])):
            count += 1
    return count


def keyword_coverage(topics: Sequence[str],
                     vocabulary: Iterable[str] = ()) -> dict[str, Any]:
    """Fraction of the document's DECLARED `Topics:` subjects that resolve to
    the snapshot's keyword vocabulary; `count` is the resolved count.

    A document declaring no topics scores 0.0 (it joins no vocabulary and earns
    no edges), never a vacuous 1.0. In a whole-corpus projection an INCLUDED
    document's own declared topics are in the vocabulary by construction (the
    vocabulary IS the union of declared topics), so this signal separates
    documents that declare and resolve topics from those that declare none — and
    it keeps its teeth for any narrower vocabulary a caller supplies."""
    return _keyword_coverage(topics, vocabulary)


def _keyword_coverage(topics: Sequence[str],
                      vocabulary: Iterable[str]) -> dict[str, Any]:
    declared = list(topics or ())
    vocab = set(vocabulary or ())
    resolved = sum(1 for t in declared if t in vocab)
    return _signal(resolved / len(declared) if declared else 0.0, resolved)


def link_degree(topics: Sequence[str],
                destinations: Mapping[str, Sequence[str]] | None = None,
                vocabulary: Iterable[str] = ()) -> dict[str, Any]:
    """The document's snapshot edge degree — one cluster edge per declared topic
    that resolves to a cluster, plus every `destinations` reference — against
    `LINK_DEGREE_SATURATION`. Reads the generator's own derived maps; it never
    rescans anything."""
    return _link_degree(topics, destinations, vocabulary)


def _link_degree(topics: Sequence[str],
                 destinations: Mapping[str, Sequence[str]] | None,
                 vocabulary: Iterable[str]) -> dict[str, Any]:
    vocab = set(vocabulary or ())
    degree = sum(1 for t in (topics or ()) if t in vocab)
    dest = destinations or {}
    for key in DESTINATION_KEYS:
        degree += len(dest.get(key) or ())
    return _signal(_normalized(degree, LINK_DEGREE_SATURATION), degree)


# --------------------------------------------------------------------------
# the per-document object
# --------------------------------------------------------------------------

def document_completeness(
    *,
    text: str,
    kind: str | None = None,
    topics: Sequence[str] = (),
    destinations: Mapping[str, Sequence[str]] | None = None,
    vocabulary: Iterable[str] = (),
) -> dict[str, Any]:
    """One document's `completeness` object: the `score` plus the five named
    signals, each a normalized value beside its raw count.

    `text` is the document body the generator already loaded; `kind`/`topics`/
    `destinations` are its projected entry fields; `vocabulary` is the
    snapshot's keyword vocabulary. Nothing is read from disk."""
    p = _Prepared(text)
    signals = {
        "structure": _structure(p, kind),
        "length": _length(p),
        "open_markers": _open_markers(p),
        "keyword_coverage": _keyword_coverage(topics, vocabulary),
        "link_degree": _link_degree(topics, destinations, vocabulary),
    }
    score = _round(sum(WEIGHTS[name] * signals[name]["value"]
                       for name in SIGNAL_NAMES))
    return {"score": min(max(score, 0.0), 1.0), **signals}


# --------------------------------------------------------------------------
# the staged-topic aggregate (design D8) — the ONE sanctioned aggregate
# --------------------------------------------------------------------------

def topic_health(member_docs: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """One staged topic's `health` object, from the topic FOLDER's own corpus
    documents ONLY.

    `member_docs` are projected `documents[]` entries (each carrying `id`/`path`
    and its `completeness` object) for the documents that LIVE in the topic
    folder. A document that merely declares the topic as a DESTINATION is
    inbound context and contributes nothing: its doneness is its own topic's
    business, and letting an unfinished upstream note hold a finished fragment
    hostage would make the gate capricious (design D8).

    `status` is DERIVED from the blockers — `ready` when there are none, `stub`
    when the folder carries no corpus documents, `developing` otherwise — so a
    red indicator is always explainable by named, countable reasons, and the
    gate's refusal and the tile's icon can never disagree about WHY."""
    docs = list(member_docs or ())
    standing_total = 0
    scores: list[float] = []
    standing_blockers: list[dict[str, Any]] = []
    threshold_blockers: list[dict[str, Any]] = []

    for entry in docs:
        doc_id = entry.get("id") or entry.get("path") or ""
        comp = entry.get("completeness") or {}
        raw = (comp.get("open_markers") or {}).get("count")
        markers = int(raw) if isinstance(raw, (int, float)) and not isinstance(raw, bool) else 0
        raw_score = comp.get("score")
        score = (_round(raw_score)
                 if isinstance(raw_score, (int, float)) and not isinstance(raw_score, bool)
                 else 0.0)
        standing_total += markers
        scores.append(score)
        if markers > 0:
            standing_blockers.append({
                "kind": BLOCKER_STANDING_OPEN_ITEMS,
                "document": doc_id,
                "count": markers,
            })
        if score < READY_MIN_SCORE:
            threshold_blockers.append({
                "kind": BLOCKER_BELOW_READY_THRESHOLD,
                "document": doc_id,
                "score": score,
                "threshold": READY_MIN_SCORE,
            })

    blockers = standing_blockers + threshold_blockers
    if not docs:
        status = STATUS_STUB
    elif not blockers:
        status = STATUS_READY
    else:
        status = STATUS_DEVELOPING
    return {
        "standing_open_items": standing_total,
        "doc_score_min": _round(min(scores)) if scores else 0.0,
        "doc_score_mean": _round(sum(scores) / len(scores)) if scores else 0.0,
        "blockers": blockers,
        "status": status,
    }


# --------------------------------------------------------------------------
# refusal wording (the gate's half of design D8's "explainable in one hover
# and one refusal message") — pure string rendering, no policy
# --------------------------------------------------------------------------

def blocker_sentence(blocker: Mapping[str, Any]) -> str:
    """One blocker as one concrete, actionable clause: the document plus its
    count, or the document plus its score against the contract constant."""
    document = blocker.get("document") or "<unnamed document>"
    if blocker.get("kind") == BLOCKER_STANDING_OPEN_ITEMS:
        count = blocker.get("count")
        item = "item" if count == 1 else "items"
        return f"{document} carries {count} standing open {item}"
    if blocker.get("kind") == BLOCKER_BELOW_READY_THRESHOLD:
        return (f"{document} scores {blocker.get('score')} below "
                f"READY_MIN_SCORE {blocker.get('threshold')}")
    return f"{document} is blocked ({blocker.get('kind')})"


def refusal_reason(health: Mapping[str, Any]) -> str:
    """Why this topic is not ready, in the blockers' own terms. A `stub` topic
    has no blockers to cite, so it states the one fact it has."""
    blockers = list(health.get("blockers") or ())
    if blockers:
        return "; ".join(blocker_sentence(b) for b in blockers)
    if health.get("status") == STATUS_STUB:
        return "the topic folder carries no corpus documents"
    return f"health status {health.get('status')!r}"
