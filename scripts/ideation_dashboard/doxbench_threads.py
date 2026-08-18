"""Per-document doxBench session THREADS — the sidecar file format and the
persistence seams around it (add-doxbench-editing-phase-b, design §4, tasks §9).

Every loaded document carries one thread: a sidecar file on the session's own
branch, inside the session worktree, holding a STRUCTURED STATE HEADER above the
conversation that produced it. This module owns exactly four things, and
deliberately nothing else:

  1. THE FORMAT — the frontmatter, the six commitment classes of the state
     header, and the per-turn transcript lines, with a total ``parse_thread``
     that refuses anything it cannot round-trip byte for byte
     (``render_thread`` → ``parse_thread`` → ``render_thread`` is identity).
  2. COMPACTION — layer two of the three-layer compression stack. Lossy BY
     DESIGN over the transcript, and a DEFECT over the header's commitments, so
     a compaction that would drop one RAISES rather than returns.
  3. THE PERSISTENCE SEAM — the sidecar path rule, the path set that must ride
     the document's own Save so a thread and the text it discusses cannot land
     through separate commits, and ONE write route: the injected ``HumanGate``.
  4. THE DECLARED POSTURES — promotion exclusion (a thread is conversation
     scaffolding, never promoted by default), and the degraded posture that
     threads exist only where branch sessions exist.

WHAT IS NOT HERE, and why each absence is a decision:

  * No harness, model, or provider contact of any kind. The §11 slice bridges
    the harness and it is GATED behind tasks §3's verify list; what this module
    offers it is an INTERFACE (``ThreadMirror``) and nothing more.
  * No knowledge service and no packet assembler (§10). This module answers
    "what does a thread look like and where does it live", not "what does a
    turn get to see".
  * No share-session verb (§12). It declares the promotion posture §12 reads,
    and holds no path off the machine at all.
  * No commit. ``branch_session.commit_gate_action`` already commits a DECLARED
    path set as exactly ONE commit; this module hands it the paths
    (``thread_commit_paths``) and never grows a second commit path beside it.

AUTHORITY, stated because the file states it too: a thread state header is a
SUMMARY. It is non-authoritative by construction and regenerable from the
transcript it summarizes, both spelled INTO the file so nothing downstream has
to infer that a summary is not truth. It never becomes truth by being compacted,
carried into a packet, or written into a record that claims authority.

Stdlib only, and no I/O of its own: rendering and parsing are pure, and the one
write goes through the caller's human gate. A companion test greps this module
for every write and store spelling it must not contain.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:  # pragma: no cover - typing only; never a runtime import,
    # because this module performs no filesystem work of its own (see the
    # negative-space test): the one write is the injected gate's.
    from pathlib import Path

# ---------------------------------------------------------------------------
# the declared file identity (design §4.1)
# ---------------------------------------------------------------------------

SCHEMA_VERSION = 1
THREAD_KIND = "doxbench-document-thread"

# Written INTO the file, not inferred from where it sits: a reader that finds a
# thread anywhere — a packet, a diff, a fetched branch — reads its standing off
# the file itself (design §4.1, "so nothing downstream has to infer that a
# summary is not truth"). They are fields with exactly one legal value each
# rather than free strings, so a thread claiming authority cannot be
# CONSTRUCTED, never mind written.
NON_AUTHORITATIVE = "non_authoritative"
REGENERABLE_FROM_TRANSCRIPT = "transcript"

FRONTMATTER_FENCE = "---"
KEY_SCHEMA_VERSION = "schema_version"
KEY_KIND = "kind"
KEY_DOCUMENT = "document"
KEY_SCOPE = "scope"
KEY_AUTHORITY = "authority"
KEY_REGENERABLE_FROM = "regenerable_from"

# The DECLARED key order. Order is part of the format, not a preference: a
# byte-identical round trip is what makes the sidecar diffable and the parse
# total, and a reader that may reorder keys is a reader two writers will
# disagree with.
FRONTMATTER_KEY_ORDER: tuple[str, ...] = (
    KEY_SCHEMA_VERSION,
    KEY_KIND,
    KEY_DOCUMENT,
    KEY_SCOPE,
    KEY_AUTHORITY,
    KEY_REGENERABLE_FROM,
)

SCOPE_FIELD_ORDER: tuple[str, ...] = ("repository", "tile_kind", "tile_id")

# ---------------------------------------------------------------------------
# the state header's SIX commitment classes (design §4.1, delta requirement
# "Each loaded document carries a session thread with a structured state header")
# ---------------------------------------------------------------------------

STATE_SECTION = "## Thread state"
TRANSCRIPT_SECTION = "## Transcript"
SECTION_PREFIX = "## "

ACTIVE_GOAL_LABEL = "Active goal:"
ACCEPTED_FACTS_LABEL = "Accepted facts:"
OPEN_QUESTIONS_LABEL = "Open questions:"
DECISIONS_LABEL = "Decisions in thread:"
EVIDENCE_REFS_LABEL = "Evidence refs:"
PENDING_ACTIONS_LABEL = "Pending actions:"

# The five LIST classes, in the order they render. `Active goal:` is the sixth
# commitment class and renders first as a single line, so it is not in this
# tuple; `COMMITMENT_CLASSES` below names all six for the compaction check.
LIST_LABEL_ORDER: tuple[str, ...] = (
    ACCEPTED_FACTS_LABEL,
    OPEN_QUESTIONS_LABEL,
    DECISIONS_LABEL,
    EVIDENCE_REFS_LABEL,
    PENDING_ACTIONS_LABEL,
)

ITEM_PREFIX = "  - "
EVIDENCE_OPEN = " [evidence: "
EVIDENCE_CLOSE = "]"
# An em dash with spaces, exactly as the design sketch spells it: a decision
# without a stated basis is the thing this format exists to prevent, so the
# separator is required and the basis is non-empty.
DECISION_BASIS_SEPARATOR = " — "

TURN_HEADER_PREFIX = "### turn "
TURN_FIELD_SEPARATOR = " · "
TURN_BOUND_PREFIX = "bound: "
HUMAN_LABEL = "human:"
ASSISTANT_LABEL = "assistant:"

# A transcript body is prose, so it may span lines — but it may not open a line
# with any of the structural sentinels, or the file would parse as a different
# thread than the one that was rendered. Refused, never escaped: escaping would
# make the sidecar unreadable to the human it is written for.
BODY_FORBIDDEN_LINE_PREFIXES: tuple[str, ...] = (
    HUMAN_LABEL,
    ASSISTANT_LABEL,
    TURN_HEADER_PREFIX,
    SECTION_PREFIX,
    FRONTMATTER_FENCE,
)

# ---------------------------------------------------------------------------
# WHERE A THREAD LIVES (task 9.1)
#
# Threads are SESSION WORKING MEMORY, not corpus material, and the prefix says
# so out loud: they sit in the dashboard's own artifact tree beside the gate
# records and the intents (`ideation/dashboard/…`, gate_console.DEFAULT_RECORDS_DIR
# / intent_apply_lane.DEFAULT_INTENTS_DIR), never under `ideation/staging/` or
# `ideation/brainstorm/` where the corpus lives and where a lifecycle `Status:`
# header would be expected of them. Two consequences are the reason for the
# choice rather than side effects of it:
#
#   * a corpus lens, a doc-health sweep, or a reader browsing staging never
#     meets half-formed conversation as though it were material; and
#   * the tree is TRACKED, unlike `ideation/workbench/` (gitignored, FR-012),
#     because a thread MUST be able to ride its document's commit (task 9.2) —
#     an ignored sidecar could not.
# ---------------------------------------------------------------------------

THREAD_PREFIX = "ideation/dashboard/session-threads/"
THREAD_SUFFIX = ".thread.md"


# ---------------------------------------------------------------------------
# refusals — every one named, nothing silently coerced
# ---------------------------------------------------------------------------


class ThreadError(ValueError):
    """Base class for every thread-shaped refusal in this module. Derives from
    ``ValueError`` so a caller that already treats malformed input as a value
    error keeps working, and so every subclass here is catchable as one class."""


class ThreadFormatRefused(ThreadError):
    """The thread text, or a value offered for one, is not the DECLARED format:
    a malformed frontmatter line, a missing or misordered section, an unknown
    label, a multi-line value where one line is the format, or a body line that
    opens with a structural sentinel. Carries the structural reason and never
    the surrounding conversation."""


class ThreadKindRefused(ThreadError):
    """The file declares a different ``kind``. Refused rather than sniffed: a
    parser that guesses at kind is a parser that will one day read a gate record
    as a thread."""


class ThreadVersionRefused(ThreadError):
    """The file declares a ``schema_version`` this module does not implement.
    Refused rather than best-effort parsed — a partially understood thread is
    exactly the artifact whose commitments would go missing quietly."""


class ThreadPathRefused(ThreadError):
    """A document path cannot be turned into a sidecar path: it is absolute,
    traversal-shaped, not normalized, spelled with a backslash, blank, or is
    itself already a thread. The rule is deterministic and reversible, so a path
    it cannot represent is a refusal rather than a coercion."""


class ThreadCompactionRefused(ThreadError):
    """A compaction would drop a commitment from the state header. Layer two of
    the compression stack is lossy over the TRANSCRIPT and a DEFECT over the
    header, so the defect is a raise here rather than a note in a review."""


class ThreadCapabilityAbsent(ThreadError):
    """Threads were asked for where branch sessions do not exist — the hosted
    plane, or a plane with no gate capability. Absence is DECLARED and reported,
    never degraded into a thread written somewhere else."""

    def __init__(self, cause: str) -> None:
        self.cause = cause
        super().__init__(f"{THREAD_CAPABILITY_ABSENT_REASON} — {cause}")


class ThreadMirrorFailed(ThreadError):
    """An injected ``ThreadMirror`` raised. The appended thread rides on
    ``.thread`` BECAUSE the sidecar is the record: a harness that fails may not
    cost the human a turn, so the caller still has the exact thread to write."""

    def __init__(self, thread: "DocumentThread", cause: BaseException) -> None:
        self.thread = thread
        self.cause = cause
        super().__init__(
            "the thread mirror refused or failed; the sidecar remains the "
            "record and the appended turn is carried on `.thread` — a mirror "
            f"is downstream of the record, never in front of it ({cause})"
        )


# ---------------------------------------------------------------------------
# value validators — one place, so every refusal reads the same
# ---------------------------------------------------------------------------


def _single_line(value: object, *, field: str) -> str:
    """A frontmatter value, a commitment item, or a turn field: exactly one line,
    already stripped. Not stripped FOR the caller — a value that needed stripping
    would not round-trip, and a format that silently rewrites what it was given
    cannot be diffed against what the human wrote."""

    if not isinstance(value, str):
        raise ThreadFormatRefused(f"{field} must be a string")
    if value != value.strip():
        raise ThreadFormatRefused(
            f"{field} carries leading or trailing whitespace; a thread value is "
            "stored exactly as given and is never stripped for the caller")
    if "\n" in value or "\r" in value:
        raise ThreadFormatRefused(
            f"{field} spans lines; this value is a single line by format")
    return value


def _non_empty_single_line(value: object, *, field: str) -> str:
    text = _single_line(value, field=field)
    if not text:
        raise ThreadFormatRefused(f"{field} must not be blank")
    return text


def _validated_body(value: object, *, field: str) -> str:
    """A transcript body: prose that MAY span lines, must not be blank, must
    carry no blank line (a blank line is the turn-block separator), and must open
    no line with a structural sentinel."""

    if not isinstance(value, str):
        raise ThreadFormatRefused(f"{field} must be a string")
    if "\r" in value:
        raise ThreadFormatRefused(
            f"{field} carries a carriage return; a thread file is LF-only")
    if value != value.strip():
        raise ThreadFormatRefused(
            f"{field} carries leading or trailing whitespace; a body is stored "
            "exactly as given")
    if not value:
        raise ThreadFormatRefused(
            f"{field} must not be blank; a turn with no text is not a turn")
    for line in value.split("\n"):
        if not line.strip():
            raise ThreadFormatRefused(
                f"{field} contains a blank line, which is the transcript's own "
                "turn separator; a body is one block of prose")
        for sentinel in BODY_FORBIDDEN_LINE_PREFIXES:
            if line.startswith(sentinel):
                raise ThreadFormatRefused(
                    f"{field} opens a line with {sentinel!r}, a structural "
                    "sentinel; such a body would parse back as a different "
                    "thread than the one rendered")
    return value


def _validated_document_path(value: object, *, field: str = "document") -> str:
    """The ONE document-path rule, used by the path helpers AND by
    ``DocumentThread`` construction, so a thread cannot exist for a path no
    sidecar path can be derived from."""

    # A value that is not one non-empty line is refused AS A PATH refusal, not as
    # a generic format one: the caller asked for a sidecar path and the answer is
    # that this document cannot have one.
    try:
        path = _non_empty_single_line(value, field=field)
    except ThreadFormatRefused as error:
        raise ThreadPathRefused(f"refusing {value!r} as a {field}: {error}") from error
    if "\\" in path:
        raise ThreadPathRefused(
            f"refusing {path!r}: a document path is repository-relative POSIX; a "
            "backslash is not normalized here, because normalizing it would "
            "break the reversibility the sidecar path rule promises")
    if path.startswith("/"):
        raise ThreadPathRefused(
            f"refusing {path!r}: a document path is repository-relative, and an "
            "absolute path names a tree this rule cannot place")
    segments = path.split("/")
    if any(segment in ("", ".", "..") for segment in segments):
        raise ThreadPathRefused(
            f"refusing {path!r}: a document path is normalized and traversal-free "
            "— an empty, `.`, or `..` segment is refused rather than resolved")
    if path.startswith(THREAD_PREFIX) or path.endswith(THREAD_SUFFIX):
        raise ThreadPathRefused(
            f"refusing {path!r}: this is already a thread sidecar, and a thread "
            "of a thread is a second conversation store, not a document")
    return path


# ---------------------------------------------------------------------------
# the shapes
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class ThreadScope:
    """The tile the thread belongs to — the same triple every doxBench surface
    scopes by, so a thread found on a fetched branch says which tile of which
    repository it is working memory for."""

    repository: str
    tile_kind: str
    tile_id: str

    def __post_init__(self) -> None:
        for field in SCOPE_FIELD_ORDER:
            value = _non_empty_single_line(getattr(self, field),
                                           field=f"scope.{field}")
            # The scope renders as a FLOW mapping on one line, so a value
            # carrying the mapping's own punctuation could not be read back.
            # Refused, because a repository or tile id containing `,` `:` `{` or
            # `}` is a naming problem, not a quoting problem.
            for forbidden in (",", ":", "{", "}"):
                if forbidden in value:
                    raise ThreadFormatRefused(
                        f"scope.{field} contains {forbidden!r}, which the "
                        "one-line scope mapping reserves")


@dataclasses.dataclass(frozen=True, slots=True)
class AcceptedFact:
    """One accepted fact, with the OPTIONAL evidence ref the design sketch
    attaches to it. Evidence is part of the fact rather than a parallel list
    entry, so compaction cannot keep the fact and lose what backs it."""

    text: str
    evidence: str | None = None

    def __post_init__(self) -> None:
        text = _non_empty_single_line(self.text, field="accepted fact")
        if EVIDENCE_OPEN.strip() in text:
            raise ThreadFormatRefused(
                f"an accepted fact may not contain {EVIDENCE_OPEN.strip()!r}: "
                "the evidence ref is a declared field, not prose inside the fact")
        if self.evidence is not None:
            evidence = _non_empty_single_line(self.evidence,
                                              field="fact evidence ref")
            if EVIDENCE_CLOSE in evidence:
                raise ThreadFormatRefused(
                    f"an evidence ref may not contain {EVIDENCE_CLOSE!r}, which "
                    "closes the rendered ref")

    def render(self) -> str:
        if self.evidence is None:
            return self.text
        return f"{self.text}{EVIDENCE_OPEN}{self.evidence}{EVIDENCE_CLOSE}"


@dataclasses.dataclass(frozen=True, slots=True)
class ThreadDecision:
    """One decision made in the thread, and the BASIS it was made on. The basis
    is required: an unexplained decision is the artifact this whole layer exists
    to keep out of the corpus."""

    decision: str
    basis: str

    def __post_init__(self) -> None:
        decision = _non_empty_single_line(self.decision, field="decision")
        basis = _non_empty_single_line(self.basis, field="decision basis")
        for value, field in ((decision, "decision"), (basis, "decision basis")):
            if DECISION_BASIS_SEPARATOR in value:
                raise ThreadFormatRefused(
                    f"{field} contains {DECISION_BASIS_SEPARATOR!r}, the "
                    "separator between a decision and its basis")

    def render(self) -> str:
        return f"{self.decision}{DECISION_BASIS_SEPARATOR}{self.basis}"


@dataclasses.dataclass(frozen=True, slots=True)
class ThreadState:
    """The state header's six commitment classes. Empty is legal for every one
    of them — a thread that has established nothing yet says so — and the labels
    render either way, so the header's shape does not depend on how far the
    conversation got."""

    active_goal: str = ""
    accepted_facts: tuple[AcceptedFact, ...] = ()
    open_questions: tuple[str, ...] = ()
    decisions: tuple[ThreadDecision, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    pending_actions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.active_goal:
            _non_empty_single_line(self.active_goal, field="active goal")
        else:
            _single_line(self.active_goal, field="active goal")
        for label, values, expected in (
                (ACCEPTED_FACTS_LABEL, self.accepted_facts, AcceptedFact),
                (DECISIONS_LABEL, self.decisions, ThreadDecision)):
            if not isinstance(values, tuple):
                raise ThreadFormatRefused(f"{label} must be a tuple")
            for value in values:
                if not isinstance(value, expected):
                    raise ThreadFormatRefused(
                        f"{label} holds {expected.__name__} values")
        for label, values in ((OPEN_QUESTIONS_LABEL, self.open_questions),
                              (EVIDENCE_REFS_LABEL, self.evidence_refs),
                              (PENDING_ACTIONS_LABEL, self.pending_actions)):
            if not isinstance(values, tuple):
                raise ThreadFormatRefused(f"{label} must be a tuple")
            for value in values:
                _non_empty_single_line(value, field=label.rstrip(":"))


@dataclasses.dataclass(frozen=True, slots=True)
class ThreadTurn:
    """One transcript turn. The header line names the MODEL that answered and
    the BOUND BUFFER the turn was bound to, because that is the same pair the
    released chat-turn envelope carries (design §4.1) — the sidecar and the wire
    then agree by construction rather than by two conventions that drift."""

    turn_id: str
    model: str
    bound_buffer_key: str
    human: str
    assistant: str

    def __post_init__(self) -> None:
        for field in ("turn_id", "model", "bound_buffer_key"):
            value = _non_empty_single_line(getattr(self, field), field=field)
            if TURN_FIELD_SEPARATOR in value:
                raise ThreadFormatRefused(
                    f"{field} contains {TURN_FIELD_SEPARATOR!r}, the turn "
                    "header's own field separator")
        _validated_body(self.human, field="human turn body")
        _validated_body(self.assistant, field="assistant turn body")

    def render(self) -> str:
        return (
            f"{TURN_HEADER_PREFIX}{self.turn_id}{TURN_FIELD_SEPARATOR}"
            f"{self.model}{TURN_FIELD_SEPARATOR}"
            f"{TURN_BOUND_PREFIX}{self.bound_buffer_key}\n"
            f"{HUMAN_LABEL} {self.human}\n"
            f"{ASSISTANT_LABEL} {self.assistant}\n"
        )


@dataclasses.dataclass(frozen=True, slots=True)
class DocumentThread:
    """One document's thread: the file identity, the tile scope, the state
    header, and the transcript.

    ``authority`` and ``regenerable_from`` are FIELDS with exactly one legal
    value each rather than constants the renderer adds, so the refusal lands
    where the claim is made: a caller that tries to construct an authoritative
    thread fails at construction, and a file that CLAIMS authority fails at
    parse."""

    document: str
    scope: ThreadScope
    state: ThreadState = dataclasses.field(default_factory=ThreadState)
    turns: tuple[ThreadTurn, ...] = ()
    schema_version: int = SCHEMA_VERSION
    authority: str = NON_AUTHORITATIVE
    regenerable_from: str = REGENERABLE_FROM_TRANSCRIPT

    def __post_init__(self) -> None:
        _validated_document_path(self.document)
        if not isinstance(self.scope, ThreadScope):
            raise ThreadFormatRefused("scope must be a ThreadScope")
        if not isinstance(self.state, ThreadState):
            raise ThreadFormatRefused("state must be a ThreadState")
        if not isinstance(self.turns, tuple) or any(
                not isinstance(turn, ThreadTurn) for turn in self.turns):
            raise ThreadFormatRefused("turns must be a tuple of ThreadTurn")
        seen: set[str] = set()
        for turn in self.turns:
            if turn.turn_id in seen:
                raise ThreadFormatRefused(
                    f"turn id {turn.turn_id!r} appears twice; a turn id "
                    "identifies a turn, so a repeat is a lost turn")
            seen.add(turn.turn_id)
        if self.schema_version != SCHEMA_VERSION:
            raise ThreadVersionRefused(
                f"this module writes schema_version {SCHEMA_VERSION}; "
                f"{self.schema_version!r} is another format")
        if self.authority != NON_AUTHORITATIVE:
            raise ThreadFormatRefused(
                f"a thread's authority is {NON_AUTHORITATIVE!r} by construction: "
                "a summary does not become truth by declaring itself one")
        if self.regenerable_from != REGENERABLE_FROM_TRANSCRIPT:
            raise ThreadFormatRefused(
                f"a thread is regenerable from {REGENERABLE_FROM_TRANSCRIPT!r}; "
                "no other origin is a thread state header")


# ---------------------------------------------------------------------------
# rendering
# ---------------------------------------------------------------------------


def _render_scope(scope: ThreadScope) -> str:
    fields = ", ".join(f"{name}: {getattr(scope, name)}"
                       for name in SCOPE_FIELD_ORDER)
    return f"{{ {fields} }}"


def _render_frontmatter(thread: DocumentThread) -> str:
    values = {
        KEY_SCHEMA_VERSION: str(thread.schema_version),
        KEY_KIND: THREAD_KIND,
        KEY_DOCUMENT: thread.document,
        KEY_SCOPE: _render_scope(thread.scope),
        KEY_AUTHORITY: thread.authority,
        KEY_REGENERABLE_FROM: thread.regenerable_from,
    }
    lines = [FRONTMATTER_FENCE]
    lines.extend(f"{key}: {values[key]}" for key in FRONTMATTER_KEY_ORDER)
    lines.append(FRONTMATTER_FENCE)
    return "".join(f"{line}\n" for line in lines)


def _state_items(state: ThreadState, label: str) -> tuple[str, ...]:
    if label == ACCEPTED_FACTS_LABEL:
        return tuple(fact.render() for fact in state.accepted_facts)
    if label == OPEN_QUESTIONS_LABEL:
        return tuple(state.open_questions)
    if label == DECISIONS_LABEL:
        return tuple(decision.render() for decision in state.decisions)
    if label == EVIDENCE_REFS_LABEL:
        return tuple(state.evidence_refs)
    if label == PENDING_ACTIONS_LABEL:
        return tuple(state.pending_actions)
    raise ThreadFormatRefused(f"unknown state label {label!r}")


def render_state_header(thread: DocumentThread) -> str:
    """JUST the header: the frontmatter plus the ``## Thread state`` block, with
    NO transcript text.

    This is the packet-carryable unit (design §4.1): the assembler carries the
    SELECTED document's thread in full and the OTHER loaded documents' headers
    only, so the header has to be extractable without the conversation. It
    carries the frontmatter with it deliberately — a header travelling without
    its ``authority``/``regenerable_from`` declaration is the exact artifact a
    downstream reader would have to guess about."""

    lines = [f"{STATE_SECTION}", ""]
    goal = thread.state.active_goal
    lines.append(f"{ACTIVE_GOAL_LABEL} {goal}" if goal else ACTIVE_GOAL_LABEL)
    for label in LIST_LABEL_ORDER:
        lines.append(label)
        lines.extend(f"{ITEM_PREFIX}{item}"
                     for item in _state_items(thread.state, label))
    body = "".join(f"{line}\n" for line in lines)
    # The header ends with the blank line that separates it from the transcript
    # section, so `render_thread` is exactly header + transcript and a companion
    # test can assert the prefix relation rather than trusting this comment.
    return f"{_render_frontmatter(thread)}\n{body}\n"


def render_thread(thread: DocumentThread) -> str:
    """The whole sidecar, header ABOVE transcript (design §4.1): a reader —
    human or assembler — gets the commitments without reading the conversation."""

    if not isinstance(thread, DocumentThread):
        raise ThreadFormatRefused("render_thread renders a DocumentThread")
    rendered = f"{render_state_header(thread)}{TRANSCRIPT_SECTION}\n"
    if not thread.turns:
        return rendered
    blocks = "\n".join(turn.render() for turn in thread.turns)
    return f"{rendered}\n{blocks}"


# ---------------------------------------------------------------------------
# parsing — total, and every refusal named
# ---------------------------------------------------------------------------


def _parse_scope(raw: str) -> ThreadScope:
    text = raw.strip()
    if not (text.startswith("{") and text.endswith("}")):
        raise ThreadFormatRefused(
            "the scope is a one-line flow mapping "
            f"`{{ {', '.join(name + ': <value>' for name in SCOPE_FIELD_ORDER)} }}`")
    inner = text[1:-1].strip()
    parts = [part.strip() for part in inner.split(",")]
    if len(parts) != len(SCOPE_FIELD_ORDER):
        raise ThreadFormatRefused(
            f"the scope declares exactly {len(SCOPE_FIELD_ORDER)} fields "
            f"({', '.join(SCOPE_FIELD_ORDER)})")
    values: dict[str, str] = {}
    for part, expected in zip(parts, SCOPE_FIELD_ORDER):
        name, sep, value = part.partition(": ")
        if not sep or name != expected:
            raise ThreadFormatRefused(
                f"scope field {part!r} is not `{expected}: <value>`; the field "
                "order is part of the format")
        values[expected] = value.strip()
    return ThreadScope(**values)


def _parse_frontmatter(lines: list[str]) -> tuple[dict[str, str], int]:
    if not lines or lines[0] != FRONTMATTER_FENCE:
        raise ThreadFormatRefused(
            f"a thread file opens with the {FRONTMATTER_FENCE!r} frontmatter fence")
    index = 1
    order: list[str] = []
    values: dict[str, str] = {}
    while index < len(lines) and lines[index] != FRONTMATTER_FENCE:
        key, sep, raw = lines[index].partition(": ")
        if not sep or not key or key != key.strip():
            raise ThreadFormatRefused(
                f"frontmatter line {lines[index]!r} is not `<key>: <value>`")
        if key in values:
            raise ThreadFormatRefused(
                f"frontmatter key {key!r} appears twice; which one is meant is "
                "not something a parser may decide")
        order.append(key)
        values[key] = raw
        index += 1
    if index >= len(lines):
        raise ThreadFormatRefused(
            f"the frontmatter is not closed by a {FRONTMATTER_FENCE!r} fence")
    # kind and version FIRST, with their own refusals: what this file claims to
    # be is decided before anything else in it is trusted.
    kind = values.get(KEY_KIND)
    if kind != THREAD_KIND:
        raise ThreadKindRefused(
            f"this file declares kind {kind!r}; a thread sidecar declares "
            f"{THREAD_KIND!r}")
    declared_version = values.get(KEY_SCHEMA_VERSION, "")
    if declared_version.strip() != str(SCHEMA_VERSION):
        raise ThreadVersionRefused(
            f"this file declares schema_version {declared_version.strip()!r}; "
            f"this module implements {SCHEMA_VERSION} and refuses rather than "
            "reading a format it does not know")
    missing = [key for key in FRONTMATTER_KEY_ORDER if key not in values]
    unknown = [key for key in order if key not in FRONTMATTER_KEY_ORDER]
    if missing or unknown:
        raise ThreadFormatRefused(
            f"the frontmatter declares exactly {list(FRONTMATTER_KEY_ORDER)}; "
            f"missing={missing} unknown={unknown}")
    if tuple(order) != FRONTMATTER_KEY_ORDER:
        raise ThreadFormatRefused(
            f"the frontmatter key order is part of the format "
            f"({list(FRONTMATTER_KEY_ORDER)}); this file orders them {order}")
    return values, index + 1


def _parse_state(state_lines: list[str]) -> ThreadState:
    if not state_lines:
        raise ThreadFormatRefused(
            f"the {STATE_SECTION!r} section declares its six commitment classes; "
            "an empty section declares nothing")
    first = state_lines[0]
    if first == ACTIVE_GOAL_LABEL:
        active_goal = ""
    elif first.startswith(f"{ACTIVE_GOAL_LABEL} "):
        active_goal = first[len(ACTIVE_GOAL_LABEL) + 1:]
    else:
        raise ThreadFormatRefused(
            f"the state header opens with {ACTIVE_GOAL_LABEL!r}; this file opens "
            f"with {first!r}")
    index = 1
    collected: dict[str, list[str]] = {}
    for label in LIST_LABEL_ORDER:
        if index >= len(state_lines) or state_lines[index] != label:
            found = state_lines[index] if index < len(state_lines) else None
            raise ThreadFormatRefused(
                f"the state header declares {label!r} here; found {found!r}. The "
                f"six commitment classes are declared in a fixed order "
                f"({[ACTIVE_GOAL_LABEL, *LIST_LABEL_ORDER]}) so a reader knows "
                "what is missing rather than guessing")
        index += 1
        items: list[str] = []
        while index < len(state_lines) and state_lines[index].startswith(ITEM_PREFIX):
            items.append(state_lines[index][len(ITEM_PREFIX):])
            index += 1
        collected[label] = items
    if index != len(state_lines):
        raise ThreadFormatRefused(
            f"the state header carries an unrecognized line "
            f"{state_lines[index]!r} after its declared classes")
    facts: list[AcceptedFact] = []
    for item in collected[ACCEPTED_FACTS_LABEL]:
        if item.endswith(EVIDENCE_CLOSE) and EVIDENCE_OPEN in item:
            text, _, evidence = item.rpartition(EVIDENCE_OPEN)
            facts.append(AcceptedFact(text, evidence[:-len(EVIDENCE_CLOSE)]))
        else:
            facts.append(AcceptedFact(item))
    decisions: list[ThreadDecision] = []
    for item in collected[DECISIONS_LABEL]:
        decision, sep, basis = item.partition(DECISION_BASIS_SEPARATOR)
        if not sep:
            raise ThreadFormatRefused(
                f"decision {item!r} states no basis; the format is "
                f"`<decision>{DECISION_BASIS_SEPARATOR}<basis>` and a decision "
                "with no basis is the thing this header exists to prevent")
        decisions.append(ThreadDecision(decision, basis))
    return ThreadState(
        active_goal=active_goal,
        accepted_facts=tuple(facts),
        open_questions=tuple(collected[OPEN_QUESTIONS_LABEL]),
        decisions=tuple(decisions),
        evidence_refs=tuple(collected[EVIDENCE_REFS_LABEL]),
        pending_actions=tuple(collected[PENDING_ACTIONS_LABEL]),
    )


def _parse_turn(block: list[str]) -> ThreadTurn:
    header = block[0]
    if not header.startswith(TURN_HEADER_PREFIX):
        raise ThreadFormatRefused(
            f"a transcript turn opens with {TURN_HEADER_PREFIX!r}; found "
            f"{header!r}")
    fields = header[len(TURN_HEADER_PREFIX):].split(TURN_FIELD_SEPARATOR)
    if len(fields) != 3:
        raise ThreadFormatRefused(
            f"a turn header is `{TURN_HEADER_PREFIX}<id>{TURN_FIELD_SEPARATOR}"
            f"<model>{TURN_FIELD_SEPARATOR}{TURN_BOUND_PREFIX}<buffer key>` — "
            "the model and the bound buffer are not optional, because the "
            "released envelope carries the same pair")
    turn_id, model, bound = fields
    if not bound.startswith(TURN_BOUND_PREFIX):
        raise ThreadFormatRefused(
            f"the turn header's third field is {TURN_BOUND_PREFIX!r} plus the "
            f"bound buffer key; found {bound!r}")
    bodies: dict[str, list[str]] = {}
    current: str | None = None
    for line in block[1:]:
        matched = None
        for label in (HUMAN_LABEL, ASSISTANT_LABEL):
            if line == label or line.startswith(f"{label} "):
                matched = label
                break
        if matched is not None:
            if matched in bodies:
                raise ThreadFormatRefused(
                    f"turn {turn_id!r} declares {matched!r} twice")
            bodies[matched] = [line[len(matched) + 1:]] if line != matched else [""]
            current = matched
            continue
        if current is None:
            raise ThreadFormatRefused(
                f"turn {turn_id!r} carries the line {line!r} before any "
                f"{HUMAN_LABEL!r} body")
        bodies[current].append(line)
    for label in (HUMAN_LABEL, ASSISTANT_LABEL):
        if label not in bodies:
            raise ThreadFormatRefused(
                f"turn {turn_id!r} declares no {label!r} body; a turn is the pair")
    return ThreadTurn(
        turn_id=turn_id, model=model,
        bound_buffer_key=bound[len(TURN_BOUND_PREFIX):],
        human="\n".join(bodies[HUMAN_LABEL]),
        assistant="\n".join(bodies[ASSISTANT_LABEL]),
    )


def parse_thread(text: str) -> DocumentThread:
    """Read a rendered sidecar back. TOTAL by refusal: anything this parser
    cannot reproduce byte for byte is refused with the structural reason, so
    ``render_thread(parse_thread(render_thread(t)))`` is identity and a thread
    on disk is never half-understood."""

    if not isinstance(text, str):
        raise ThreadFormatRefused("a thread file is text")
    if "\r" in text:
        raise ThreadFormatRefused(
            "a thread file is LF-only; a CR would make the same thread hash and "
            "diff differently on two machines")
    if not text.endswith("\n"):
        raise ThreadFormatRefused("a thread file ends with a newline")
    lines = text.split("\n")[:-1]
    values, index = _parse_frontmatter(lines)
    if index >= len(lines) or lines[index] != "":
        raise ThreadFormatRefused(
            "the frontmatter is followed by one blank line")
    index += 1
    if index >= len(lines) or lines[index] != STATE_SECTION:
        raise ThreadFormatRefused(
            f"the {STATE_SECTION!r} section is required and sits ABOVE the "
            f"transcript, so a reader gets the commitments without reading the "
            "conversation")
    index += 1
    if index >= len(lines) or lines[index] != "":
        raise ThreadFormatRefused(
            f"the {STATE_SECTION!r} heading is followed by one blank line")
    index += 1
    state_lines: list[str] = []
    while index < len(lines) and lines[index] != "":
        state_lines.append(lines[index])
        index += 1
    state = _parse_state(state_lines)
    if index >= len(lines):
        raise ThreadFormatRefused(
            f"the {TRANSCRIPT_SECTION!r} section is required; a thread with no "
            "turns still declares it (a state header alone is not a thread)")
    index += 1  # the blank line closing the state block
    if index >= len(lines) or lines[index] != TRANSCRIPT_SECTION:
        found = lines[index] if index < len(lines) else None
        raise ThreadFormatRefused(
            f"the {TRANSCRIPT_SECTION!r} section follows the state header; found "
            f"{found!r}")
    index += 1
    turns: list[ThreadTurn] = []
    if index < len(lines):
        if lines[index] != "":
            raise ThreadFormatRefused(
                f"the {TRANSCRIPT_SECTION!r} heading is followed by one blank "
                "line before the first turn")
        index += 1
        block: list[str] = []
        for line in lines[index:]:
            if line == "":
                if not block:
                    raise ThreadFormatRefused(
                        "the transcript carries an empty turn block; turns are "
                        "separated by exactly one blank line")
                turns.append(_parse_turn(block))
                block = []
                continue
            block.append(line)
        if not block:
            raise ThreadFormatRefused(
                "the transcript ends with a blank line; a turn block is the last "
                "thing in the file")
        turns.append(_parse_turn(block))
    return DocumentThread(
        document=values[KEY_DOCUMENT],
        scope=_parse_scope(values[KEY_SCOPE]),
        state=state,
        turns=tuple(turns),
        schema_version=int(values[KEY_SCHEMA_VERSION].strip()),
        authority=values[KEY_AUTHORITY].strip(),
        regenerable_from=values[KEY_REGENERABLE_FROM].strip(),
    )


# ---------------------------------------------------------------------------
# the sidecar path rule (task 9.1)
# ---------------------------------------------------------------------------


def thread_path_for(document_path: str) -> str:
    """The ONE sidecar path for a document, deterministic and reversible.

    The document's own repository-relative path is MIRRORED under the thread
    prefix and given the thread suffix. Mirroring rather than flattening is the
    whole point: two documents named `README.md` in two folders keep two
    distinct threads, which a basename-keyed rule would silently merge — and
    merging two conversations is the worst failure this file format has."""

    return f"{THREAD_PREFIX}{_validated_document_path(document_path)}{THREAD_SUFFIX}"


def thread_document_for(thread_path: str) -> str:
    """The inverse of ``thread_path_for``. Reversible on purpose: a session
    holding a set of sidecars can say which document each one belongs to without
    reading it, and the reader of a diff can too."""

    try:
        path = _non_empty_single_line(thread_path, field="thread path")
    except ThreadFormatRefused as error:
        raise ThreadPathRefused(
            f"refusing {thread_path!r} as a thread path: {error}") from error
    if not path.startswith(THREAD_PREFIX):
        raise ThreadPathRefused(
            f"refusing {path!r}: every thread sidecar lives under "
            f"{THREAD_PREFIX!r}; a path outside it is not a thread")
    if not path.endswith(THREAD_SUFFIX):
        raise ThreadPathRefused(
            f"refusing {path!r}: every thread sidecar ends with "
            f"{THREAD_SUFFIX!r}")
    inner = path[len(THREAD_PREFIX):-len(THREAD_SUFFIX)]
    # Validated as a DOCUMENT path, so a traversal-shaped sidecar name cannot be
    # unwound into an escape either.
    return _validated_document_path(inner, field="thread document")


def thread_commit_paths(document_path: str) -> tuple[str, ...]:
    """The sidecar path(s) that MUST ride this document's Save (task 9.2).

    ``branch_session.commit_gate_action`` already commits a DECLARED path set as
    exactly ONE commit on the session branch; a Save adds these paths to the
    ``documents`` set it declares, and the thread then cannot land through a
    different commit than the text it discusses. That is the ratified
    one-commit-per-gate-action rule APPLIED to a second artifact, not relaxed for
    it — which is why this function returns paths and performs no commit of its
    own.

    Plural in shape although it is one file today, so a later sidecar (a
    compaction record, an offload artifact) joins the Save by being returned here
    rather than by changing every caller's call shape."""

    return (thread_path_for(document_path),)


# ---------------------------------------------------------------------------
# compaction — LAYER TWO of the three-layer compression stack
# ---------------------------------------------------------------------------

# Layer one is SELECTION (the knowledge service, lossless by reference); layer
# three is MECHANICAL REVERSIBLE COMPRESSION at the model boundary. Layer two —
# this function — is SEMANTIC COMPACTION into the state header: lossy BY DESIGN,
# human-reviewable, promotion-gated, non-authoritative and regenerable. No layer
# does another's work, and this one never claims to be lossless.
#
# "Lossy by design" is scoped exactly: it is lossy over the TRANSCRIPT, and a
# DEFECT over the header. So the defect is spelled as a REFUSAL rather than a
# comment — a compaction whose result loses a commitment raises instead of
# returning, because a review that has to notice a missing open question is a
# review that will one day not notice.

COMMITMENT_CLASSES: tuple[str, ...] = (
    "active goal",
    "accepted fact",
    "open question",
    "decision",
    "evidence ref",
    "pending action",
)


def _refuse_lost_commitment(class_label: str, item: object) -> None:
    raise ThreadCompactionRefused(
        f"compaction dropped the {class_label} {item!r}: layer two is lossy over "
        "the TRANSCRIPT and preserves the header's commitments — dropping an "
        "open question, a decision, an accepted fact, an evidence ref, or a "
        "pending action is a DEFECT, while dropping prose that restates them is "
        "the point")


def _refuse_lost_commitments(before: ThreadState, after: ThreadState) -> None:
    # The active goal is the header's sixth commitment class. The delta
    # enumerates the five list classes explicitly; losing the goal is the same
    # class of defect, and REWORDING it is a decision a human makes through a
    # lifecycle verb, not something a compaction may do on its own — so the goal
    # must survive verbatim.
    if before.active_goal and after.active_goal != before.active_goal:
        _refuse_lost_commitment("active goal", before.active_goal)
    for fact in before.accepted_facts:
        if fact not in after.accepted_facts:
            _refuse_lost_commitment("accepted fact", fact.render())
    for question in before.open_questions:
        if question not in after.open_questions:
            _refuse_lost_commitment("open question", question)
    for decision in before.decisions:
        if decision not in after.decisions:
            _refuse_lost_commitment("decision", decision.render())
    for ref in before.evidence_refs:
        if ref not in after.evidence_refs:
            _refuse_lost_commitment("evidence ref", ref)
    for action in before.pending_actions:
        if action not in after.pending_actions:
            _refuse_lost_commitment("pending action", action)


def compact_thread(thread: DocumentThread, *, keep_turns: int,
                   state: ThreadState | None = None) -> DocumentThread:
    """Compact a thread to stay inside its bounds: keep the last ``keep_turns``
    transcript turns, and take ``state`` as the compacted header when a caller
    supplies one.

    ``state`` is passed IN rather than derived here because summarizing is a
    model's job and verifying is this module's: whatever produced the compacted
    header, every commitment the old header carried must still be in the new one
    or the compaction is refused. The result stays ``non_authoritative`` and
    ``regenerable_from: transcript`` — structurally, since those are the only
    values ``DocumentThread`` accepts, and a compacted summary is exactly the
    artifact someone would otherwise be tempted to cite."""

    if not isinstance(thread, DocumentThread):
        raise ThreadFormatRefused("compact_thread compacts a DocumentThread")
    if isinstance(keep_turns, bool) or not isinstance(keep_turns, int):
        raise ThreadFormatRefused("keep_turns must be a non-negative integer")
    if keep_turns < 0:
        raise ThreadFormatRefused(
            "keep_turns must be non-negative; a negative bound is not a bound")
    if state is not None and not isinstance(state, ThreadState):
        raise ThreadFormatRefused("state must be a ThreadState")
    compacted_state = thread.state if state is None else state
    _refuse_lost_commitments(thread.state, compacted_state)
    retained = thread.turns[-keep_turns:] if keep_turns else ()
    return dataclasses.replace(thread, state=compacted_state, turns=retained)


# ---------------------------------------------------------------------------
# the persistence seam — ONE write route (task 9.1/9.2)
# ---------------------------------------------------------------------------


def write_thread(gate: object, thread: DocumentThread) -> "Path":
    """Write the sidecar through the injected ``HumanGate``.

    ``gate.write_gate_artifact`` is the route, and NOT
    ``gate.rewrite_session_document``, for two reasons read off ``boundary.py``:

      * ``rewrite_session_document`` refuses a target that does not ALREADY
        EXIST ("bringing a document into existence stays the create-only create
        path"), so it could never write a thread's FIRST turn — every thread
        begins as a file nothing has made yet; and
      * it deliberately does not consult the boundary's declared output
        allowlist, whereas ``write_gate_artifact`` → ``write_output`` →
        ``permit_output`` does. A thread is the surface's own artifact, like a
        gate record, so it SHOULD be allowlist-governed — which is exactly why
        task 9.5 puts ``THREAD_PREFIX`` in the doxBench save gate's declared
        allowlist rather than routing around the allowlist here.

    The sidecar lands inside the SESSION WORKTREE and never in the served
    checkout because the gate handed in is rooted at the worktree AND declares
    it (``gate_routes.first_edit_gate_factory``), an equality that module's own
    test already pins. This function therefore checks that a session worktree is
    DECLARED at all — the condition that says "this is a session gate" — and
    does not re-derive the root equality, because a second copy of a pinned rule
    is how two copies drift."""

    if not isinstance(thread, DocumentThread):
        raise ThreadFormatRefused("write_thread writes a DocumentThread")
    writer = getattr(gate, "write_gate_artifact", None)
    if not callable(writer):
        raise ThreadCapabilityAbsent(
            "the object handed in is not a human gate — a thread is written "
            "only through the gate's own artifact write")
    if getattr(gate, "session_root", None) is None:
        raise ThreadCapabilityAbsent(
            "the gate declares no session worktree, and a thread lives only on "
            "a session branch")
    return writer(thread_path_for(thread.document), render_thread(thread))


# ---------------------------------------------------------------------------
# promotion exclusion (task 9.4, design §4.2)
# ---------------------------------------------------------------------------

PROMOTION_EXCLUSION_REASON = (
    "threads are conversation scaffolding, not corpus material: a session pull "
    "request does NOT promote them by default, carrying them requires an "
    "explicit human opt-in, and a finding leaves a thread only through an "
    "existing lifecycle verb — an idea note, a fragment, or a disposition on "
    "the topic, with provenance"
)


def promotion_excluded_prefixes() -> tuple[str, ...]:
    """The prefixes a session pull request excludes from promotion BY DEFAULT.

    The consumer is the share-session / pull-request verb (tasks.md §12), which
    reads this rather than restating the prefix, so "threads are excluded" has
    one spelling. A reviewer reading a pull request of documents should not have
    to read the conversations that produced them unless someone CHOSE to include
    them, and raw chat becoming durable truth by default is the failure this
    exclusion exists to prevent.

    There is no automatic promotion path in this module, and no second decision
    store anywhere near it: a finding becomes durable by someone creating a new
    object through an existing lifecycle verb, with provenance. A companion test
    asserts that absence against this module's own source, because an absence
    nobody checks is an absence that grows a helper."""

    return (THREAD_PREFIX,)


# ---------------------------------------------------------------------------
# the MIRRORING INTERFACE the GATED harness slice consumes
# (TODO(add-doxbench-editing-phase-b tasks.md §11): that slice implements
# `ThreadMirror` in the local harness bridge — the adapter for the existing
# three-member model port — and injects it as `mirror=`. It is BLOCKED on
# tasks.md §3's verify list, so nothing here talks to a harness, starts a
# process, or knows a harness protocol; this is the whole seam it gets.)
#
# THE SPLIT-BRAIN PROHIBITION, stated where the seam is: the sidecar files are
# THE RECORD. A harness's native memory MUST NOT hold the thread. Where a
# harness-local memory exists at all it holds non-authoritative material only,
# is ranked LAST by the source hierarchy, and is never consulted as governed
# truth — two stores claiming to be the same thread is a split brain, and the
# sidecar wins by contract rather than by convention.
# ---------------------------------------------------------------------------

# The mirror's WHOLE operation set, declared as data so a test can assert on it
# and a second verb cannot arrive quietly — the shape the pull-request port's own
# `PORT_OPERATIONS` declaration established on this surface.
MIRROR_OPERATIONS: tuple[str, ...] = ("mirror_turn",)


@runtime_checkable
class ThreadMirror(Protocol):
    """ONE method: hand a turn that is ALREADY in the sidecar to the harness.

    It returns nothing, and that is the contract: a mirror is told what the
    record says, and can neither answer with a turn nor amend one. Anything a
    mirror would want to add to a thread has to go through this module's own
    append, so the record cannot be written from two places."""

    def mirror_turn(self, thread: "DocumentThread", turn: "ThreadTurn") -> None: ...


def mirror_turn(thread: DocumentThread, turn: ThreadTurn, *,
                mirror: ThreadMirror | None = None) -> DocumentThread:
    """Append ``turn`` to the sidecar thread and, when a mirror is injected, hand
    it the same turn.

    Order is the contract: the append is computed FIRST and completely, and the
    mirror is consulted afterwards on the resulting thread — the sidecar is the
    record, so nothing downstream of it may decide what the record says. With
    ``mirror=None`` the function is FULLY functional, because a thread must not
    depend on a harness existing: the editor-only posture (design §3.4) keeps
    buffers, the loaded set, Save, and threads-on-disk usable with no model port
    at all."""

    if not isinstance(thread, DocumentThread):
        raise ThreadFormatRefused("mirror_turn appends to a DocumentThread")
    if not isinstance(turn, ThreadTurn):
        raise ThreadFormatRefused("mirror_turn appends a ThreadTurn")
    appended = dataclasses.replace(thread, turns=thread.turns + (turn,))
    if mirror is None:
        return appended
    handler = getattr(mirror, MIRROR_OPERATIONS[0], None)
    if not callable(handler):
        raise ThreadFormatRefused(
            f"a thread mirror implements exactly {list(MIRROR_OPERATIONS)}; the "
            "object injected implements none of it")
    try:
        handler(appended, turn)
    except BaseException as error:  # the mirror's failure is not the thread's
        raise ThreadMirrorFailed(appended, error) from error
    return appended


# ---------------------------------------------------------------------------
# degraded postures (design §3.4) — threads exist only where sessions exist
# ---------------------------------------------------------------------------

HOSTED_PLANE = "hosted"
LOCAL_PLANE = "local"
PLANES: tuple[str, ...] = (LOCAL_PLANE, HOSTED_PLANE)

# The FIXED reason a route reports. One text, because the two absent cases are
# one posture: a thread is session working memory on an unmerged branch, so
# where there is no branch session there is nothing for a thread to be.
THREAD_CAPABILITY_ABSENT_REASON = (
    "threads exist only where branch sessions exist: a thread is session "
    "working memory on an unmerged branch, so where no branch session can be "
    "opened, no thread is created, written, or offered"
)
HOSTED_PLANE_CAUSE = "this is the hosted plane, which opens no branch session"
NO_GATE_CAPABILITY_CAUSE = (
    "this plane declares no gate capability, so no session verb is reachable "
    "and the thread affordance renders as a copyable descriptor instead")


def require_thread_capability(*, plane: str, gate_capability: bool) -> None:
    """The refusal a thread route calls FIRST. Returns ``None`` where threads
    exist, and raises ``ThreadCapabilityAbsent`` naming which absence applies.

    Both absent cases are DECLARED rather than discovered: the hosted plane and
    a plane with no gate capability. Neither degrades into a thread written
    somewhere else, because "somewhere else" is the served checkout."""

    if plane not in PLANES:
        raise ThreadFormatRefused(
            f"plane must be one of {list(PLANES)}; {plane!r} is not a plane this "
            "surface serves, and guessing which one was meant is how a hosted "
            "plane ends up treated as a local one")
    if not isinstance(gate_capability, bool):
        raise ThreadFormatRefused(
            "gate_capability is a declared boolean; a truthy value of another "
            "type is not a declaration")
    if plane == HOSTED_PLANE:
        raise ThreadCapabilityAbsent(HOSTED_PLANE_CAUSE)
    if not gate_capability:
        raise ThreadCapabilityAbsent(NO_GATE_CAPABILITY_CAUSE)
    return None


def thread_capability_absence(*, plane: str, gate_capability: bool) -> str | None:
    """The same decision as a REPORTABLE string for a surface that renders the
    absence instead of raising on it (the copyable-descriptor posture). ``None``
    means threads are available."""

    try:
        require_thread_capability(plane=plane, gate_capability=gate_capability)
    except ThreadCapabilityAbsent as absent:
        return str(absent)
    return None


def thread_paths_in(paths: Sequence[str]) -> tuple[str, ...]:
    """The subset of ``paths`` that are thread sidecars, in the order given.

    Offered so the §12 verb can answer "which of this session's changed paths
    are threads" from the SAME prefix rule the write uses, instead of matching
    the prefix again itself."""

    return tuple(path for path in paths
                 if isinstance(path, str) and path.startswith(THREAD_PREFIX)
                 and path.endswith(THREAD_SUFFIX))
