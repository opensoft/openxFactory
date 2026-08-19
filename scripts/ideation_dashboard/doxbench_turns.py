"""doxBench grounded chat-turn prompt envelope, boundary arithmetic, and the
bounded idempotency store (010-doxbench-editor-chat T047 and T048;
data-model.md Sections 1/3/4/7/8; contracts/chat-turn.md; research.md
R4/R5/R8; plan.md Constraints).

This module implements both the request-side envelope/boundary surface
(T047) and the store slice (T048) together. It owns:

* an internal, schema-agnostic prompt envelope assembly
  (``build_prompt_envelope``) that renders the nine declared deterministic
  section GROUPS from a scope projection, a KEYED BUFFER SET (the reserved
  `outline` buffer plus one section per loaded document, in the declared
  order -- add-doxbench-editing-phase-b), a bounded transcript, and a new
  human message;
* the exact UTF-8 byte-count validators for every request-side dimension a
  turn must enforce before any provider dispatch is attempted;
* the redacted refusal shape (``TurnError`` and its subclasses) every
  boundary and identity check raises on failure; and
* ``TurnRecord``, ``TurnLease``, and ``TurnStore``: the bounded,
  thread-safe, per-instance one-in-flight/idempotency store a caller uses
  to reserve, finalize, and replay turns without ever dispatching a
  provider call twice for the same request.

Every validator here measures exact UTF-8 bytes, never Unicode code points,
and never truncates, normalizes, composes, or reflows caller-supplied text.
Content identity recomputation reuses the ``doxbench_hash`` authority; scope
and editable-path authority is never re-derived here, only revalidated
against the projection an independent scope authority already produced.

This module performs no response decoding, no provider dispatch, and no
failure-mapping of any kind; it computes response-side byte limits only as
declared constants. That logic is left to the caller that dispatches a
provider call and hands its result to ``TurnStore``.
"""

from __future__ import annotations

import copy
import dataclasses
import itertools
import threading
from collections.abc import Callable, Mapping, Sequence
from pathlib import PurePosixPath

from ideation_dashboard.doxbench_hash import (
    MAX_BUFFER_BYTES,
    ContentIdentity,
    content_identity,
    sha256_hex,
    utf8_size,
)
from ideation_dashboard import doxbench_packet
from ideation_dashboard.doxbench_model import (
    SERVER_MAX_INPUT_LIMIT_BYTES,
    SERVER_MAX_OUTPUT_LIMIT_BYTES,
)
from ideation_dashboard.doxbench_scope import ScopeKey, ScopeProjection
from ideation_dashboard.doxbench_telemetry import (
    OPERATION_CONTEXT_PACKET, PROVIDER_ROLE_RETRIEVAL, TurnUsage,
)

# ---------------------------------------------------------------------------
# request-side boundary constants (plan.md Constraints; contracts/chat-turn.md)
# ---------------------------------------------------------------------------

MAX_WORKING_SUBJECT_BYTES = 512
MAX_MESSAGE_BYTES = 16_384
MAX_TRANSCRIPT_TURNS = 20
MAX_TRANSCRIPT_BYTES = 64_000

# Pinned to the model authority's own route-specific constants so the two
# cannot drift apart (a companion test asserts the equality directly).
MAX_REQUEST_BODY_BYTES = SERVER_MAX_INPUT_LIMIT_BYTES

# ---------------------------------------------------------------------------
# response-side arithmetic constants only -- no decoding, no dispatch here
# ---------------------------------------------------------------------------

MAX_ASSISTANT_PROSE_BYTES = 65_536
MAX_PROPOSAL_BYTES = 400_000
MAX_RESPONSE_TOTAL_BYTES = SERVER_MAX_OUTPUT_LIMIT_BYTES

# ---------------------------------------------------------------------------
# deterministic prompt shape
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# BUFFER KEYS (add-doxbench-editing-phase-b, design D1)
#
# The turn's buffer set is KEYED, exactly as the browser's working state is:
# `outline` is permanently reserved, a document buffer's key is its own
# repository-relative PATH, and the reserved `document` key holds the ONE
# not-yet-created buffer of the create flow, which has no path to be keyed by.
# ---------------------------------------------------------------------------

OUTLINE_BUFFER_KEY = "outline"
UNBACKED_DOCUMENT_BUFFER_KEY = "document"

# The keys a DOCUMENT'S OWN PATH may not claim. The browser refuses such a load in
# its own vocabulary (`doxbench-state.js` `LOAD_REFUSED_RESERVED_KEY`, F12/N2);
# these are the same rule on the server, because a wire request is not obliged to
# have come from that browser.
#
# THE RULE IS PER LANE, and deliberately so (Codex review of PR #210, CODEX-1).
#
# `outline` is refused on EVERY lane. A document keyed there is filtered out of
# the document enumeration by `ordered_document_keys`, so it vanishes: its hash
# goes unverified, its bytes uncounted, and the v1 success builder indexes an
# empty list. Reproduced at a4a6f6e — the connection dropped with no response at
# all — so refusing it restores no promise, it closes a crash.
#
# `document` is refused only on the WIDENED lane. There it would shadow the ONE
# reserved unbacked slot, which may ride the same request beside it. On the v1
# lane no such ambiguity exists: that envelope carries exactly one document, its
# key IS `document` whether the path is null or literally "document", and a turn
# shaped that way WAS SERVED at a4a6f6e (reproduced: 200, dispatched). Refusing it
# would break the promise this release's additive class makes -- that a v1 client
# keeps being served -- for a collision that lane cannot have.
RESERVED_BUFFER_KEYS = frozenset({OUTLINE_BUFFER_KEY, UNBACKED_DOCUMENT_BUFFER_KEY})
V1_RESERVED_BUFFER_KEYS = frozenset({OUTLINE_BUFFER_KEY})

# The DECLARED deterministic document order (design D3 point 4). Spelled to
# match `web/views/doxbench-state.js`'s `DOCUMENT_KEY_ORDER_RULE` byte for byte,
# and sorted on UTF-16 code units rather than Python code points so the two
# runtimes agree on every key, including the astral characters where code-unit
# and code-point order diverge. A companion test asserts the two spellings.
DOCUMENT_KEY_ORDER_RULE = "ascending lexicographic by buffer key (UTF-16 code unit)"


def buffer_key_for(buffer: TurnBuffer) -> str:
    """The key a buffer belongs under. Never invented: the outline's key is
    reserved, a document's key IS its path, and a document with no path yet
    takes the one reserved unbacked slot."""
    if buffer.kind == OUTLINE_BUFFER_KEY:
        return OUTLINE_BUFFER_KEY
    if buffer.path is None:
        return UNBACKED_DOCUMENT_BUFFER_KEY
    return buffer.path


def ordered_document_keys(keys) -> tuple[str, ...]:
    return tuple(sorted(
        (key for key in keys if key != OUTLINE_BUFFER_KEY),
        key=lambda value: value.encode("utf-16-be", "surrogatepass"),
    ))


def ordered_buffer_keys(keys) -> tuple[str, ...]:
    """The outline first -- its commit is the session ancestry -- then every
    document in the declared order. The ONE place a buffer enumeration order is
    decided, because a prompt whose section order depends on dictionary
    iteration is a prompt no test can pin."""
    return (OUTLINE_BUFFER_KEY,) + ordered_document_keys(keys)


DOCUMENT_BUFFER_SECTION_PREFIX = "document_buffer:"

# The DECLARED section groups, in order. Three of them are GROUPS that expand to
# a per-item section list rather than to exactly one section
# (`prompt_section_keys`).
#
# `document_buffers` expands to one section per loaded document in the declared
# order. Phase A had a single `document_buffer` here because the set held
# exactly one document; the group name replaced it rather than a longer literal
# list, since the count is now the request's own.
#
# THE PACKET'S FOUR GROUPS (task 5.4's packet half, §10) sit between the
# transcript and the buffers, which is design §3.1 step 5's own order —
# "· thread (selected, full) · thread-state headers (others) · evidence (with
# refs) · outline buffer · document buffers ·" — with the packet's DECLARATION
# ahead of them, because a packet that states its purpose, its sources, its
# scope and its expiry has to state them somewhere a reader of the prompt can
# see, and that is also where a REDUCED posture is stated (§3.4).
#
# `transcript` keeps the position Phase A gave it. Step 5's list does not name
# it at all — it names the thread material that will eventually carry the same
# conversation — so moving it would be inventing an ordering the design does
# not state, while dropping it would drop a released input. It therefore stays
# adjacent to the thread sections it is the wire-carried counterpart of.
PROMPT_SECTION_ORDER: tuple[str, ...] = (
    "system_contract",
    "model_data_handling",
    "scope_metadata",
    "working_subject",
    "transcript",
    doxbench_packet.PACKET_SECTION_DECLARATION,
    doxbench_packet.PACKET_SECTION_SELECTED_THREAD,
    doxbench_packet.PACKET_SECTION_THREAD_STATES,
    doxbench_packet.PACKET_SECTION_EVIDENCE,
    "outline_buffer",
    "document_buffers",
    "human_message",
    "response_instruction",
)


def prompt_section_keys(document_keys, *, packet) -> tuple[str, ...]:
    """The CONCRETE section keys one request's envelope carries, in the declared
    order -- `PROMPT_SECTION_ORDER` with every GROUP expanded: one
    `document_buffer:<buffer key>` section per loaded document, and the packet's
    own groups expanded by the packet module (one `thread_state:<key>` per other
    loaded document that HAS a thread, one `evidence:<ref>` per selected
    evidence item).

    ``packet`` is REQUIRED and not defaulted, deliberately. Every turn carries a
    packet -- an absent knowledge service yields the DECLARED REDUCED packet,
    not the absence of one (§3.4) -- so a `None` default would invent a second
    prompt shape that no requirement sanctions. ``None`` is still accepted by
    the expansion because a caller may ask what a packet-less order would be;
    what it may not do is arrive by omission."""
    documents = ordered_document_keys(document_keys)
    keys: list[str] = []
    for group in PROMPT_SECTION_ORDER:
        if group == "document_buffers":
            keys.extend(DOCUMENT_BUFFER_SECTION_PREFIX + key for key in documents)
        elif group in doxbench_packet.PACKET_SECTION_GROUPS:
            keys.extend(doxbench_packet.expand_group(group, packet))
        else:
            keys.append(group)
    return tuple(keys)


# The SOURCE-RANKING HIERARCHY, stated rather than left to the model to infer
# (add-doxbench-editing-phase-b task 5.5; the delta's knowledge-service
# requirement). Ordered most authoritative first, and it names the LAST rank
# explicitly as non-authoritative because a harness's own memory claiming to be
# a thread is the split brain the contract forbids.
SOURCE_RANKING_TEXT = (
    "Rank the material below by authority, in this order, and never invert it: "
    "(1) ratified or standard canon; (2) accepted or staged facts; "
    "(3) promoted findings; (4) active thread state; and last, "
    "(5) any harness-local memory, which is NON-AUTHORITATIVE and must never be "
    "cited as governed truth. A summary, a thread-state header, an offloaded "
    "artifact, or a derived index is never authority: it becomes durable only by "
    "creating a new object through review."
)

SYSTEM_CONTRACT_TEXT = (
    "You are the doxBench editor-chat assistant. Ground every answer "
    "strictly in the outline and document buffers, the scope metadata, and "
    "the transcript shown below. Never invent facts about the repository "
    "or the selected model, and never claim access to material outside the "
    "sections provided in this prompt.\n"
    + SOURCE_RANKING_TEXT
)

RESPONSE_INSTRUCTION_TEXT = (
    "Respond with assistant prose that directly addresses the human "
    "message below. If a change to the outline or the document would help, "
    "describe it as an explicit proposal grounded in the buffers shown "
    "above; never apply a change silently."
)

WORKING_STATE_CLEAN_LABEL = "WORKING STATE: GOVERNED (matches the last saved content exactly)"
WORKING_STATE_DIRTY_LABEL = "WORKING STATE: UNSAVED EDITS (differs from the last saved content)"


# ---------------------------------------------------------------------------
# error hierarchy (FR-017 redacted refusal shape)
# ---------------------------------------------------------------------------


class TurnError(ValueError):
    """Base class for every doxBench turn-shaped refusal. Every subclass in
    this module derives from both ``TurnError`` and ``ValueError`` by
    construction, since ``TurnError`` itself derives from ``ValueError``."""


class TurnBlankMessageError(TurnError):
    """Raised when a human message is blank or contains only whitespace."""


class TurnBufferKindError(TurnError):
    """Raised when the supplied working buffers are not exactly one outline
    buffer plus one or more distinctly-keyed document buffers."""


class TurnConflictError(TurnError):
    """Raised by the store slice on a conflicting concurrent turn."""


class TurnInFlightError(TurnConflictError):
    """Raised (FR-018) when a different ``client_turn_id`` attempts to
    reserve while another turn for the same conversation key is already
    in flight. A specialization of ``TurnConflictError`` so any existing
    caller catching that class still catches this one. Carries only the
    existing in-flight turn id -- never a request digest or any content."""

    def __init__(self, in_flight_turn_id: str) -> None:
        self.in_flight_turn_id = in_flight_turn_id
        super().__init__(
            "another turn is already in flight for this conversation key"
        )


class TurnIdentityMismatchError(TurnError):
    """Raised when a buffer's declared content hash does not match its
    recomputed identity, or when a declared base hash is not a
    lowercase, 64-character hex digest. Never echoes buffer content."""


class TurnScopeError(TurnError):
    """Raised when a request scope, an active document path, an outline
    path, or a document path fails independent revalidation against a scope
    projection. Never echoes buffer or projection content."""


class TurnLimitError(TurnError):
    """Raised when a measured UTF-8 byte (or turn-count) dimension exceeds
    its declared maximum. Carries only the dimension name and the two
    integers involved -- never the text that was measured."""

    def __init__(self, dimension: str, measured: int, maximum: int) -> None:
        self.dimension = dimension
        self.measured = measured
        self.maximum = maximum
        if measured < maximum:
            message = (
                f"{dimension} measured {measured}, which is below the minimum of {maximum}"
            )
        else:
            message = f"{dimension} measured {measured}, which exceeds the maximum of {maximum}"
        super().__init__(message)

    def as_public_dict(self) -> dict[str, object]:
        return {
            "dimension": self.dimension,
            "measured": self.measured,
            "maximum": self.maximum,
        }


# ---------------------------------------------------------------------------
# immutable, redacted shapes
# ---------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class TurnBuffer:
    """One working buffer (an outline or a document) exactly as the browser
    holds it. No field here is validated at construction time -- a
    malformed base hash, a mismatched content hash, or an oversize body are
    all refused later, by ``verify_buffer_identity``, so that every refusal
    goes through one redacted path."""

    kind: str
    repository: str
    # ``None`` means a not-yet-created buffer (data-model.md Section 4); a
    # not-yet-created buffer's path is expected to equal ``None`` wherever
    # the scope/binding checks compare it.
    path: str | None
    base_ref: str
    base_revision: str
    base_hash: str
    content_hash: str
    content: str
    dirty: bool


@dataclasses.dataclass(frozen=True, slots=True)
class SessionBase:
    """The base a branch session was created FROM (T104 R-12 ruling,
    2026-08-02): the ref it branched off, the revision recorded at that
    branch point, and a reader for the session's CURRENT text of a
    validated in-scope path (``None`` when the session holds no such
    file). Derived by the caller from the session's registry entry and
    worktree -- never from anything the request supplied -- and absent
    (``None`` in ``build_prompt_envelope``) for a non-session scope or a
    session whose base was never recorded, where the binding check keeps
    its original name-equality shape.

    ``alias_revisions`` (W-4, wave re-review) are the OTHER spellings of
    the same base the OPEN recorded -- concretely, the serving snapshot's
    ``source_revision`` at open time, which is what a real client's
    ``base_revision`` actually carries (the browser never receives a
    per-file revision; it declares the projection's generation-time HEAD,
    while the branch point is the open-time HEAD). Without the alias, any
    main movement between snapshot bake and session open silently reverted
    R-12 to the refusal it closed. Aliases widen ONLY the revision
    comparison; the ref name and the base-bytes clauses are untouched."""

    ref: str
    revision: str
    text_of: Callable[[str], str | None]
    alias_revisions: tuple[str, ...] = ()


@dataclasses.dataclass(frozen=True, slots=True)
class TranscriptTurn:
    """One prior turn in the bounded transcript. ``role`` is a free-form,
    non-empty label (for example a human or an assistant turn); ``text`` is
    carried exactly, never summarized or truncated."""

    role: str
    text: str


@dataclasses.dataclass(frozen=True, slots=True)
class PromptSection:
    """One section a prompt envelope assembles, in the exact order
    ``prompt_section_keys`` declares from ``PROMPT_SECTION_ORDER``."""

    key: str
    text: str


@dataclasses.dataclass(frozen=True, slots=True)
class ObservedHashes:
    """The recomputed content identities observed for EVERY buffer in the
    request's own buffer set at assembly time, keyed by BUFFER KEY -- never a
    cached value from an earlier turn (FR-016).

    Phase A carried two named fields, `outline` and `document`, because the set
    held exactly those two buffers. add-doxbench-editing-phase-b keys them, so a
    turn carrying the outline plus four loaded documents states five identities
    and a reader can ask for any of them by key. `outline` survives as a
    PROPERTY, because that key is permanently reserved and every turn carries it;
    `document` does not, because it is now one possible key among N and an
    attribute named after one key would be a literal buffer name baked into a
    surface expressed over the set."""

    by_key: Mapping[str, ContentIdentity]

    @property
    def outline(self) -> ContentIdentity:
        return self.by_key[OUTLINE_BUFFER_KEY]

    def for_key(self, key: str) -> ContentIdentity:
        return self.by_key[key]

    def keys(self) -> tuple[str, ...]:
        return ordered_buffer_keys(self.by_key)

    def document_keys(self) -> tuple[str, ...]:
        return ordered_document_keys(self.by_key)

    def __contains__(self, key: object) -> bool:
        return key in self.by_key

    def __len__(self) -> int:
        return len(self.by_key)


@dataclasses.dataclass(frozen=True, slots=True)
class PromptEnvelope:
    """The assembled, deterministic prompt for one chat turn."""

    sections: tuple[PromptSection, ...]
    scope: ScopeKey
    model_id: str
    message: str
    transcript: tuple[TranscriptTurn, ...]
    active_document_path: str | None
    observed_hashes: ObservedHashes

    # NO ``bound_buffer_key`` FIELD, deliberately (adversarial review of PR #207,
    # F4). One was added here and removed again for the same reason Phase A's own
    # review killed its ancestor: a field on an internal envelope that nothing
    # serializes, persists or renders is unreadable, so it cannot discharge the
    # obligation to NAME the bound buffer in a turn's durable RECORD -- and
    # deriving it from ``active_document_path`` mis-states the binding exactly as
    # Phase A's review found, recording "bound to the document" for a human
    # working the outline with a document loaded.
    #
    # The declared binding is still CHECKED: ``build_prompt_envelope`` passes it
    # to ``revalidate_scope``, which refuses a binding naming no supplied buffer
    # before any provider call. What it is not is stored here as a claim no reader
    # can consult. It returns as a RECORD field when the widened co-resident
    # envelope family carries it on the wire (tasks.md §13), which is the only
    # place it can be read from.

    def rendered(self) -> str:
        """The full prompt text, sections joined in declared order. Byte-for-
        byte deterministic for identical construction input."""
        return "\n\n".join(section.text for section in self.sections)


# ---------------------------------------------------------------------------
# exact UTF-8 byte validators (never code points)
# ---------------------------------------------------------------------------


def validate_working_subject(text: str) -> None:
    measured = utf8_size(text)
    if measured > MAX_WORKING_SUBJECT_BYTES:
        raise TurnLimitError("working_subject_bytes", measured, MAX_WORKING_SUBJECT_BYTES)


def validate_message(text: str) -> None:
    if not text.strip():
        raise TurnBlankMessageError("the human message must not be blank or whitespace-only")
    measured = utf8_size(text)
    if measured > MAX_MESSAGE_BYTES:
        raise TurnLimitError("message_bytes", measured, MAX_MESSAGE_BYTES)


def transcript_bytes(transcript) -> int:
    """The sum of each turn's exact UTF-8 text size -- nothing else is
    measured (no role labels, no separators)."""
    return sum(utf8_size(turn.text) for turn in transcript)


def validate_transcript(transcript) -> None:
    count = len(transcript)
    if count > MAX_TRANSCRIPT_TURNS:
        raise TurnLimitError("transcript_turns", count, MAX_TRANSCRIPT_TURNS)
    measured = transcript_bytes(transcript)
    if measured > MAX_TRANSCRIPT_BYTES:
        raise TurnLimitError("transcript_bytes", measured, MAX_TRANSCRIPT_BYTES)


def validate_request_body_bytes(
    *,
    outline_bytes: int,
    document_bytes: int = 0,
    message_bytes: int,
    working_subject_bytes: int,
    transcript_bytes: int,
    document_buffer_bytes: Sequence[int] = (),
) -> None:
    """The whole request's measured UTF-8 total, against the fixed ceiling.

    ``document_bytes`` was the ONE document buffer Phase A allowed;
    ``document_buffer_bytes`` carries EVERY loaded document's measurement, and
    both are summed so a caller may pass either -- the released v1 wire supplies
    exactly one document and passes it as `document_bytes`, and a widened caller
    passes the whole set. Nothing is dropped or sampled: a bound that measured
    only some of the buffers it is bounding would be no bound at all."""
    measured = (
        outline_bytes + document_bytes + message_bytes + working_subject_bytes
        + transcript_bytes + sum(document_buffer_bytes)
    )
    if measured > MAX_REQUEST_BODY_BYTES:
        raise TurnLimitError("request_body_bytes", measured, MAX_REQUEST_BODY_BYTES)


# ---------------------------------------------------------------------------
# exact identity recompute
# ---------------------------------------------------------------------------

_LOWERCASE_HEX_DIGITS = frozenset("0123456789abcdef")


def _is_lowercase_hex64(value: object) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(character in _LOWERCASE_HEX_DIGITS for character in value)


def verify_buffer_identity(buffer: TurnBuffer) -> ContentIdentity:
    """Recompute a buffer's content identity via the hash authority and
    refuse on any mismatch. Refusals never echo buffer content."""
    measured = utf8_size(buffer.content)
    if measured > MAX_BUFFER_BYTES:
        raise TurnLimitError(f"{buffer.kind}_buffer_bytes", measured, MAX_BUFFER_BYTES)
    identity = content_identity(buffer.content, max_bytes=None)
    if identity.hex != buffer.content_hash:
        raise TurnIdentityMismatchError(
            "buffer content hash does not match its recomputed content identity"
        )
    if not _is_lowercase_hex64(buffer.base_hash):
        raise TurnIdentityMismatchError(
            "buffer base hash is not a lowercase, 64-character hex digest"
        )
    return identity


# ---------------------------------------------------------------------------
# scope revalidation (FR-015) -- never re-derives the scope authority
# ---------------------------------------------------------------------------


def _is_traversal_shaped(path: str) -> bool:
    if not isinstance(path, str) or not path:
        return True
    if path.startswith("/") or "\\" in path or "\x00" in path:
        return True
    return ".." in PurePosixPath(path).parts


def _require_in_scope_and_editable(path: str, projection: ScopeProjection) -> None:
    if _is_traversal_shaped(path):
        raise TurnScopeError("path is not a valid repository-relative path")
    if path not in projection.context_paths:
        raise TurnScopeError("path is not within the resolved scope")
    if path not in projection.editable_paths:
        raise TurnScopeError("path is readable but not editable")


def revalidate_scope(
    *,
    projection: ScopeProjection,
    request_scope: ScopeKey,
    bound_buffer_key: str | None,
    buffer_keys: Sequence[str],
    paths: Sequence[str | None],
) -> None:
    """Independently revalidate a turn's scope binding against a projection a
    scope authority already produced. Refuses (``TurnScopeError``) unless:

    * the request scope equals the projection's own active binding;
    * the request's DECLARED ``bound_buffer_key`` names one of the buffers the
      request actually supplied (``buffer_keys``) -- the same refusal discipline
      Phase A expressed as an equality between the active document path and the
      one document buffer's path, restated over a SET because the set is now the
      outline plus N loaded documents; and
    * every non-``None`` path in ``paths`` is both in-scope
      (``projection.context_paths``) and editable (``projection.editable_paths``)
      -- a readable-but-not-editable path is always refused before any
      disclosure. A ``None`` path (a buffer not yet created) is exempt.

    ``bound_buffer_key`` may be ``None`` ONLY where the caller's wire envelope
    carries no declared binding at all -- which is the case the released v1
    chat-turn envelope is in, and the gap this capability's own contract release
    (tasks.md §13) discharges. The binding is then NOT inferred from an adjacent
    field, because that is exactly the mis-derivation Phase A's review killed:
    instead the buffer set is required to hold no path-backed document, since a
    request that supplies a document it is working on and declares no binding is
    refusing to say what it is working on. Every refusal here leaks no projection
    or buffer content."""
    if request_scope != projection.key:
        raise TurnScopeError("request scope does not match the projection's active binding")
    keys = tuple(buffer_keys)
    if bound_buffer_key is None:
        if any(key not in (OUTLINE_BUFFER_KEY, UNBACKED_DOCUMENT_BUFFER_KEY)
               for key in keys):
            raise TurnScopeError(
                "a turn that declares no bound buffer must not supply a "
                "path-backed document buffer"
            )
    elif bound_buffer_key not in keys:
        raise TurnScopeError("the declared bound buffer names no supplied buffer")
    for path in paths:
        if path is None:
            continue
        _require_in_scope_and_editable(path, projection)


# ---------------------------------------------------------------------------
# buffer-set requirement (add-doxbench-editing-phase-b task 5.1)
# ---------------------------------------------------------------------------


def require_outline_and_documents(
    buffers, *, refused_paths: frozenset[str] = RESERVED_BUFFER_KEYS,
) -> tuple[TurnBuffer, dict[str, TurnBuffer]]:
    """Require exactly ONE outline buffer and ONE OR MORE document buffers, in
    any order, each keyed by its own path (or by the one reserved unbacked slot).
    Refuses (``TurnBufferKindError``) on a missing outline, a second outline, a
    duplicated document key -- the same document supplied twice, which is
    impossible in a well-formed keyed set and would make "which text did the
    model see" unanswerable -- or an unexpected kind.

    A document buffer whose own PATH claims one of ``refused_paths`` is refused
    here too, and that refusal is load-bearing rather than tidy (adversarial
    review of the §13 slice, F2). A repository-root file named exactly ``outline``
    derives the reserved outline key, which ``ordered_document_keys`` then filters
    OUT of the document enumeration -- so the buffer passed this requirement and
    every later step read a set that did not contain it: its declared content hash
    was never verified, its bytes were never counted against the request bound,
    and the released v1 success builder indexed an empty document list and died
    with the connection, stranding the turn's own store lease. Refusing it HERE
    puts the verdict before identity verification and before any port is
    consulted, which is where a malformed request belongs.

    ``refused_paths`` defaults to the WIDENED lane's set -- the fail-closed
    direction for any new caller -- and the v1 lane passes
    ``V1_RESERVED_BUFFER_KEYS``, which omits the ``document`` spelling because
    that lane cannot have the collision it guards (see those constants).

    Phase A's ``require_outline_and_document`` demanded exactly one of each and
    returned a pair. The ratified Phase B contract widens the set, so the
    requirement is restated over it and the return shape names the keys."""
    outline: TurnBuffer | None = None
    documents: dict[str, TurnBuffer] = {}
    for buffer in buffers:
        if buffer.kind == OUTLINE_BUFFER_KEY:
            if outline is not None:
                raise TurnBufferKindError("more than one outline buffer was supplied")
            outline = buffer
        elif buffer.kind == "document":
            if buffer.path in refused_paths:
                raise TurnBufferKindError(
                    "a document buffer's path claims a reserved buffer key")
            key = buffer_key_for(buffer)
            if key in documents:
                raise TurnBufferKindError("the same document buffer was supplied twice")
            documents[key] = buffer
        else:
            raise TurnBufferKindError("unexpected buffer kind")
    if outline is None or not documents:
        raise TurnBufferKindError(
            "exactly one outline buffer and at least one document buffer are required"
        )
    return outline, documents


# ---------------------------------------------------------------------------
# buffer-binding requirement (FR-015) -- refuses a buffer smuggled in under a
# path, repository, or ref other than what scope revalidation already
# approved. Runs after the buffer-kind requirement and before any identity
# verification or section assembly.
# ---------------------------------------------------------------------------


def _require_buffer_binding(
    buffer: TurnBuffer,
    expected_path: str | None,
    request_scope: ScopeKey,
    session_base: SessionBase | None = None,
) -> None:
    """Refuse (``TurnScopeError``) unless ``buffer`` is bound to exactly the
    session-declared path and the request scope's repository, and its base
    is one the scope can actually ground: the request scope's own ref, or --
    T104 R-12, reviewer ruling of 2026-08-02 -- the base the session
    branched FROM. Comparing ref NAMES alone conflated "same ref name" with
    "same base bytes": a buffer based on ``main`` at the moment of branching
    is correctly based, because its bytes ARE the session's base, and
    refusing it left every buffer a partial Save did not land permanently
    unable to ground a turn. Acceptance is on the REVISION, never the name
    alone, and it stays refused once the session has DIVERGED past that
    base for this buffer's own document -- the session's current text no
    longer hashes to the buffer's declared base identity -- so staleness
    detection is made precise, not weakened. "Diverged" is a CONTENT
    reading, RULED as such (reviewer, 2026-08-06, closing the wave
    re-review's interpretation question): a session that moved this
    document and moved it back byte-identically is accepted, because
    every acceptance is content-safe -- the buffer's base bytes provably
    equal the session's current text, so no stale envelope can result;
    history is not consulted. ``base_ref`` keeps its meaning
    (provenance: where these base bytes came from) and is never rewritten
    here or anywhere else. Never echoes the buffer's path, repository,
    ref, or content."""
    if buffer.path != expected_path or buffer.repository != request_scope.repository:
        raise TurnScopeError(
            "working buffer is not bound to the validated scope projection"
        )
    if buffer.base_ref == request_scope.ref:
        return
    if session_base is not None and buffer.base_ref == session_base.ref and (
        buffer.base_revision == session_base.revision
        or buffer.base_revision in session_base.alias_revisions
    ):
        # The byte clause fails CLOSED twice over: a reader failure yields
        # None, and None never equals a base identity -- including a direct
        # caller's base_hash=None (dataclass fields are unenforced), which
        # once satisfied None == None and grounded a buffer on the very
        # failure that should refuse it (wave re-review, R-12 machinery).
        identity = _session_text_identity(session_base, expected_path)
        if identity is not None and buffer.base_hash == identity:
            return
    raise TurnScopeError(
        "working buffer is not bound to the validated scope projection"
    )


def _session_text_identity(
    session_base: SessionBase, expected_path: str | None
) -> str | None:
    """The identity of the session's CURRENT base bytes for ``expected_path``
    -- what a correctly-based buffer's ``base_hash`` must equal. A path the
    session holds no file for (including a not-yet-created ``None`` path)
    has empty base bytes, so only a fresh, never-written buffer matches it.
    ``None`` (never a match) when the session's text cannot be read or
    hashed -- a refusal, not a crash, and never an echo."""
    try:
        text = session_base.text_of(expected_path) if expected_path is not None else None
        return sha256_hex(text if text is not None else "")
    except Exception:  # noqa: BLE001 - any reader failure must refuse, not crash
        return None


# ---------------------------------------------------------------------------
# section assembly helpers -- plain string formatting, no normalization
# ---------------------------------------------------------------------------


def _model_data_handling_section(
    *,
    model_id: str,
    model_data_handling: str,
    model_input_limit_bytes: int,
    model_output_limit_bytes: int,
) -> PromptSection:
    text = (
        "Selected model: " + model_id + "\n"
        "Data handling: " + model_data_handling + "\n"
        "Input limit (bytes): " + str(model_input_limit_bytes) + "\n"
        "Output limit (bytes): " + str(model_output_limit_bytes)
    )
    return PromptSection(key="model_data_handling", text=text)


def _scope_metadata_section(scope: ScopeKey) -> PromptSection:
    text = (
        "Repository: " + scope.repository + "\n"
        "Ref: " + scope.ref + "\n"
        "Tile kind: " + scope.tile_kind + "\n"
        "Tile id: " + scope.tile_id
    )
    return PromptSection(key="scope_metadata", text=text)


def _working_subject_section(working_subject: str) -> PromptSection:
    return PromptSection(key="working_subject", text="Working subject: " + working_subject)


def _transcript_section(transcript) -> PromptSection:
    turns = tuple(transcript)
    if not turns:
        text = "(no prior turns)"
    else:
        text = "\n".join(turn.role + ": " + turn.text for turn in turns)
    return PromptSection(key="transcript", text=text)


def _buffer_section(key: str, buffer: TurnBuffer) -> PromptSection:
    label = WORKING_STATE_DIRTY_LABEL if buffer.dirty else WORKING_STATE_CLEAN_LABEL
    path_text = "(not yet created)" if buffer.path is None else buffer.path
    header = "Path: " + path_text + "\n" + label + "\n---\n"
    return PromptSection(key=key, text=header + buffer.content)


def _human_message_section(message: str) -> PromptSection:
    return PromptSection(key="human_message", text="Human message:\n" + message)


# ---------------------------------------------------------------------------
# prompt envelope assembly (FR-013)
# ---------------------------------------------------------------------------


def build_prompt_envelope(
    *,
    projection: ScopeProjection,
    request_scope: ScopeKey,
    active_document_path: str | None,
    model_id: str,
    model_data_handling: str,
    model_input_limit_bytes: int,
    model_output_limit_bytes: int,
    working_subject: str,
    transcript: tuple[TranscriptTurn, ...],
    buffers,
    message: str,
    session_base: SessionBase | None = None,
    bound_buffer_key: str | None = None,
    refused_paths: frozenset[str] = RESERVED_BUFFER_KEYS,
    packet: "doxbench_packet.ContextPacket | None" = None,
    meter: object | None = None,
) -> PromptEnvelope:
    """Assemble the deterministic prompt envelope for one chat turn -- the nine
    declared section GROUPS, with one document-buffer section per loaded document
    in the declared order. Order of operations is load-bearing: scope and
    editable revalidation runs first, then the buffer-set requirement, then the
    buffer-binding check PER BUFFER (each buffer's path/repository/base_ref
    against the validated projection and request scope -- widened for a session
    scope by ``session_base`` to accept a buffer based on the session's own
    recorded base, T104 R-12), then exact identity verification for each buffer,
    and only then is any section text assembled -- so a scope, binding, or
    identity refusal never discloses a partial envelope or buffer content.

    ``bound_buffer_key`` is the request's own DECLARED binding, and it is a
    VALIDATION INPUT only: it is handed to ``revalidate_scope`` and never stored
    on the returned envelope (F4 -- an unreadable field cannot discharge the
    obligation to name the bound buffer in a durable record, and deriving one from
    an adjacent field mis-states it). ``None`` means the caller's wire envelope
    declares no binding, which the released v1 shape does not.

    A document buffer's expected path is ITS OWN key, not a single
    ``active_document_path``: the binding check was always per buffer, and
    widening the set means running it N times rather than relaxing it once. The
    reserved unbacked slot's expected path stays ``None``.
    """
    outline, documents = require_outline_and_documents(
        buffers, refused_paths=refused_paths)
    document_keys = ordered_document_keys(documents)
    revalidate_scope(
        projection=projection,
        request_scope=request_scope,
        bound_buffer_key=bound_buffer_key,
        buffer_keys=(OUTLINE_BUFFER_KEY,) + document_keys,
        paths=(projection.outline_path,)
        + tuple(documents[key].path for key in document_keys),
    )
    _require_buffer_binding(outline, projection.outline_path, request_scope,
                            session_base)
    for key in document_keys:
        # STATED PLAINLY (PR #207 review, F13): a document buffer's expected path
        # is its OWN key, which `require_outline_and_documents` established IS its
        # path -- so the path clause inside `_require_buffer_binding` is a
        # SELF-COMPARISON for documents and does no work. It is not pretended
        # otherwise, and it is not removed either: the function is one shape for
        # both buffer kinds, and the outline still passes a path it did not derive
        # from the buffer (`projection.outline_path`), where the clause is live.
        #
        # What confines a DOCUMENT is therefore two other things, both of which do
        # run: `_require_in_scope_and_editable`, which ran above for every supplied
        # path, and the base clauses here -- repository, ref name, and the T104
        # R-12 session-base widening with its byte-equality leg -- each applied per
        # buffer exactly as they were to the one document Phase A allowed. Phase A
        # additionally cross-checked the buffer's path against a single
        # server-declared `active_document_path`; no single such value exists once
        # the loaded set is the human's own choice, and the DECLARED binding that
        # replaces it is checked in `revalidate_scope` against the supplied keys.
        _require_buffer_binding(documents[key], documents[key].path, request_scope,
                                session_base)
    observed = {OUTLINE_BUFFER_KEY: verify_buffer_identity(outline)}
    for key in document_keys:
        observed[key] = verify_buffer_identity(documents[key])

    # THE PACKET (task 5.4's packet half, §10). Every turn carries one: a
    # caller that supplies none gets the DECLARED REDUCED packet rather than a
    # packet-less prompt, because "no knowledge service" is a POSTURE with a
    # stated reduction and not the absence of the pipeline. Its rails have
    # already run by the time it arrives here -- confinement and the
    # lifecycle-status exemption both happen inside the assembler, upstream of
    # every provider -- and the bounds refusal it can raise is a refusal of the
    # turn, never a truncation of it.
    if packet is None:
        packet = doxbench_packet.reduced_packet(
            projection=projection, scope=request_scope,
            selected_key=bound_buffer_key, loaded_keys=document_keys)

    sections = (
        PromptSection(key="system_contract", text=SYSTEM_CONTRACT_TEXT),
        _model_data_handling_section(
            model_id=model_id,
            model_data_handling=model_data_handling,
            model_input_limit_bytes=model_input_limit_bytes,
            model_output_limit_bytes=model_output_limit_bytes,
        ),
        _scope_metadata_section(request_scope),
        _working_subject_section(working_subject),
        _transcript_section(transcript),
        *(PromptSection(key=key, text=text)
          for key, text in doxbench_packet.packet_sections(packet)),
        _buffer_section("outline_buffer", outline),
        *(_buffer_section(DOCUMENT_BUFFER_SECTION_PREFIX + key, documents[key])
          for key in document_keys),
        _human_message_section(message),
        PromptSection(key="response_instruction", text=RESPONSE_INSTRUCTION_TEXT),
    )

    if meter is not None:
        # CONTENT-FREE metering, emitted where BOTH dimensions are real: the
        # packet's own byte count and the assembled prompt's. The dispatch
        # operation and any provider-reported token count belong to the slice
        # that dispatches (§11), which is why only one operation is emitted
        # here rather than a second one with a fabricated zero.
        meter.record(TurnUsage(
            operation=OPERATION_CONTEXT_PACKET,
            scope=request_scope,
            provider_role=PROVIDER_ROLE_RETRIEVAL,
            provider_id=packet.provider_id,
            packet_posture=packet.posture,
            source_count=len(packet.sources),
            exempt_source_count=packet.exempt_count,
            packet_bytes=packet.byte_count,
            prompt_bytes=sum(utf8_size(section.text) for section in sections),
        ))

    return PromptEnvelope(
        sections=sections,
        scope=request_scope,
        model_id=model_id,
        message=message,
        transcript=tuple(transcript),
        active_document_path=active_document_path,
        observed_hashes=ObservedHashes(by_key=dict(observed)),
    )


# ---------------------------------------------------------------------------
# bounded, thread-safe one-in-flight / idempotency store (FR-018 family)
# ---------------------------------------------------------------------------

MAX_IDEMPOTENCY_ENTRIES = 64
MAX_IDEMPOTENCY_BYTES = 16 * 1024 * 1024

TURN_STATE_COMPLETED = "completed"
TURN_STATE_FAILED = "failed"
TURN_STATE_IN_FLIGHT = "in_flight"


@dataclasses.dataclass(frozen=True, slots=True)
class TurnRecord:
    """One reserved-or-resolved turn entry. Holds no request content and no
    credential-bearing material -- only the scope-partitioned identity, a
    request digest, a state, and a bounded, already-validated result."""

    conversation_key: ScopeKey
    client_turn_id: str
    request_digest: str
    state: str
    validated_result: object | None
    size_bytes: int
    last_access_order: int


@dataclasses.dataclass(frozen=True, slots=True)
class TurnLease:
    """The outcome of a ``TurnStore.reserve`` call: whether the caller must
    dispatch a new provider call, the entry's current state, and -- for a
    replayed completion or failure -- the bounded result to hand back
    unchanged, with no second dispatch."""

    should_dispatch: bool
    state: str
    result: object | None


class TurnStore:
    """A bounded, thread-safe, per-instance one-in-flight/idempotency store.

    Entries are partitioned by conversation scope key plus ``client_turn_id``.
    A reservation for a brand-new key dispatches immediately. An identical
    digest against an in-flight entry attaches and waits (never dispatching
    twice); an identical digest against a completed or failed entry replays
    the stored result with no second dispatch. A different digest for the
    same key refuses immediately as a conflict, whether the existing entry is
    in-flight, completed, or failed -- it never blocks.

    The store's own lock is held only for the brief, in-memory bookkeeping
    each method performs; it is never held across a caller's or a provider's
    work, which always happens outside every store method call. Every
    ``copy.deepcopy`` of a ``validated_result`` runs outside the lock, but
    ingress and egress sit on opposite sides of the critical section:
    ingress (``_finalize``, via ``complete``/``fail``) deep-copies the
    caller's incoming result BEFORE the lock is ever acquired, then acquires
    the lock only to publish the already-made copy; egress (``snapshot``,
    and the replay branch of ``reserve``) captures a reference to the
    stored record UNDER the lock, releases the lock, and only then
    deep-copies it -- so an arbitrarily slow or blocking caller-supplied
    ``__deepcopy__`` can never stall an unrelated conversation key,
    whichever side of the lock it runs on. Waiting for an in-flight entry
    to resolve is done via a ``threading.Condition``, whose ``wait()``
    releases the underlying lock for the duration of the wait, so unrelated
    keys are never serialized behind it.

    Completed-or-failed entries are evicted least-recently-used once the
    store holds more than ``MAX_IDEMPOTENCY_ENTRIES`` of them or their
    combined ``size_bytes`` exceeds ``MAX_IDEMPOTENCY_BYTES``; in-flight
    entries are never evicted. Recency is tracked with a monotonically
    increasing integer counter guarded by the same lock -- never a
    timestamp -- so ordering is deterministic. Two ``TurnStore`` instances
    never share any state: every field below is set on ``self`` in
    ``__init__``.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._records: dict[tuple[ScopeKey, str], TurnRecord] = {}
        self._resolved_bytes_total = 0
        self._order_counter = itertools.count(1)
        # FR-018: at most one client_turn_id may be in flight per
        # conversation_key. Maps conversation_key -> the in-flight turn id.
        # Cleared (popped) the moment that turn id finalizes.
        self._in_flight_by_key: dict[ScopeKey, str] = {}

    def _next_order_locked(self) -> int:
        return next(self._order_counter)

    def reserve(
        self,
        conversation_key: ScopeKey,
        client_turn_id: str,
        request_digest: str,
    ) -> TurnLease:
        """Reserve (or attach to) the entry for ``conversation_key`` and
        ``client_turn_id``. Returns a lease telling the caller whether to
        dispatch a new provider call, waiting first if an identical-digest
        entry is currently in-flight. Raises ``TurnConflictError``
        immediately, with no wait, if a differing digest already occupies
        this key -- regardless of that entry's state. Raises
        ``TurnInFlightError`` immediately, with no wait and no new entry
        created, if a DIFFERENT ``client_turn_id`` is already in flight for
        the same ``conversation_key`` (FR-018) -- evaluated under the same
        lock as entry creation, so there is no race window between the
        check and the reservation."""
        entry_key = (conversation_key, client_turn_id)
        replayed_record: TurnRecord | None = None
        with self._condition:
            while True:
                record = self._records.get(entry_key)
                if record is None:
                    in_flight_turn_id = self._in_flight_by_key.get(conversation_key)
                    if in_flight_turn_id is not None and in_flight_turn_id != client_turn_id:
                        raise TurnInFlightError(in_flight_turn_id)
                    record = TurnRecord(
                        conversation_key=conversation_key,
                        client_turn_id=client_turn_id,
                        request_digest=request_digest,
                        state=TURN_STATE_IN_FLIGHT,
                        validated_result=None,
                        size_bytes=0,
                        last_access_order=self._next_order_locked(),
                    )
                    self._records[entry_key] = record
                    self._in_flight_by_key[conversation_key] = client_turn_id
                    return TurnLease(
                        should_dispatch=True, state=TURN_STATE_IN_FLIGHT, result=None
                    )
                if record.request_digest != request_digest:
                    raise TurnConflictError(
                        "a conflicting request digest is already reserved for this "
                        "conversation turn"
                    )
                if record.state == TURN_STATE_IN_FLIGHT:
                    self._condition.wait()
                    continue
                # Replay branch: do the lookup, digest-conflict check,
                # in-flight guard, and the LRU touch all under the lock, then
                # break out to deep-copy the captured result OUTSIDE the
                # lock. Safe because a finalized ``validated_result`` is
                # never mutated in place -- ingress deep-copies it once on
                # the way in, and ``TurnRecord`` is a frozen dataclass that
                # is only ever replaced wholesale, never edited -- so a
                # reference captured here stays valid after the lock is
                # released.
                replayed_record = self._touch_locked(entry_key, record)
                break
        assert replayed_record is not None
        return TurnLease(
            should_dispatch=False,
            state=replayed_record.state,
            result=copy.deepcopy(replayed_record.validated_result),
        )

    def _touch_locked(
        self, entry_key: tuple[ScopeKey, str], record: TurnRecord
    ) -> TurnRecord:
        touched = dataclasses.replace(record, last_access_order=self._next_order_locked())
        self._records[entry_key] = touched
        return touched

    def _finalize(
        self,
        conversation_key: ScopeKey,
        client_turn_id: str,
        state: str,
        result: object,
        size_bytes: int,
    ) -> None:
        """Resolve an in-flight entry. Validates every refusal condition
        BEFORE mutating any state, so a refused finalization leaves the
        store -- records, resolved-bytes accounting, and the in-flight
        guard -- byte-for-byte unchanged. The stored result is a deep copy
        of the caller's ``result`` (ingress isolation), never the caller's
        own object by reference.

        The cheap size-bounds check needs no lock and runs first; the
        (potentially expensive) deep copy of ``result`` also runs OUTSIDE
        the lock, before it is ever acquired. Only the in-memory bookkeeping
        -- state validation, publishing the already-made copy, resolved-byte
        accounting, and the in-flight guard -- happens under the lock. A
        refused finalization discards the unused copy and leaves the store
        byte-for-byte unchanged."""
        if size_bytes < 0:
            raise TurnLimitError("result_size_bytes", size_bytes, 0)
        if size_bytes > MAX_IDEMPOTENCY_BYTES:
            raise TurnLimitError("result_size_bytes", size_bytes, MAX_IDEMPOTENCY_BYTES)
        copied_result = copy.deepcopy(result)
        entry_key = (conversation_key, client_turn_id)
        with self._condition:
            previous = self._records.get(entry_key)
            if previous is None or previous.state != TURN_STATE_IN_FLIGHT:
                raise TurnConflictError(
                    "no in-flight turn exists to finalize for this conversation "
                    "key and turn id"
                )
            record = dataclasses.replace(
                previous,
                state=state,
                validated_result=copied_result,
                size_bytes=size_bytes,
                last_access_order=self._next_order_locked(),
            )
            self._records[entry_key] = record
            self._resolved_bytes_total += size_bytes
            if self._in_flight_by_key.get(conversation_key) == client_turn_id:
                del self._in_flight_by_key[conversation_key]
            self._enforce_bounds_locked()
            self._condition.notify_all()

    def complete(
        self,
        conversation_key: ScopeKey,
        client_turn_id: str,
        result: object,
        *,
        size_bytes: int,
    ) -> None:
        """Resolve the in-flight entry as completed with a validated,
        already-bounded ``result``, waking every attached waiter."""
        self._finalize(conversation_key, client_turn_id, TURN_STATE_COMPLETED, result, size_bytes)

    def fail(
        self,
        conversation_key: ScopeKey,
        client_turn_id: str,
        failure: object,
        *,
        size_bytes: int,
    ) -> None:
        """Resolve the in-flight entry as failed with a bounded failure
        payload, waking every attached waiter."""
        self._finalize(conversation_key, client_turn_id, TURN_STATE_FAILED, failure, size_bytes)

    def _enforce_bounds_locked(self) -> None:
        resolved_keys = [
            entry_key
            for entry_key, record in self._records.items()
            if record.state != TURN_STATE_IN_FLIGHT
        ]
        while resolved_keys and (
            len(resolved_keys) > MAX_IDEMPOTENCY_ENTRIES
            or self._resolved_bytes_total > MAX_IDEMPOTENCY_BYTES
        ):
            oldest_key = min(resolved_keys, key=lambda key: self._records[key].last_access_order)
            oldest_record = self._records.pop(oldest_key)
            self._resolved_bytes_total -= oldest_record.size_bytes
            resolved_keys.remove(oldest_key)

    def snapshot(self, conversation_key: ScopeKey, client_turn_id: str) -> TurnRecord | None:
        """Return the current record for this key, or ``None`` if unknown.
        A read-only peek: it never mutates recency order. The returned
        record's ``validated_result`` is a fresh deep copy (egress
        isolation) -- mutating it can never alter the stored value.

        Only the lookup happens under the lock; the deep copy runs OUTSIDE
        it, after the lock has been released. This is safe because a
        finalized ``validated_result`` is never mutated in place -- ingress
        deep-copies it once in ``_finalize`` and ``TurnRecord`` is a frozen
        dataclass that is only ever replaced wholesale, never edited -- so
        the reference captured under the lock is still valid to copy after
        release."""
        entry_key = (conversation_key, client_turn_id)
        with self._lock:
            record = self._records.get(entry_key)
        if record is None:
            return None
        return dataclasses.replace(record, validated_result=copy.deepcopy(record.validated_result))


# ---------------------------------------------------------------------------
# T061 (US3): strict typed assistant-response validation against the PINNED
# released contract (contract-v1.27 `typed_proposal`: exactly
# {target, base_hash, summary, content}, unique targets, and AT MOST ONE
# PROPOSAL PER SUPPLIED BUFFER -- `PROPOSAL_CAP_RULE`, which replaced the
# released schema's literal 0-2 when add-doxbench-editing-phase-b made the
# bound the request's own buffer count. The released v1 wire still carries
# exactly two buffers, so the effective bound there is still two.
# ---------------------------------------------------------------------------


class TurnResponseError(TurnError):
    """The assistant's typed response failed validation — malformed shape,
    unknown or duplicate target, summary/content bounds, the spanning total
    bound, or a base identity that does not match what the model was SHOWN
    (``ObservedHashes``). A wrong base here is a RESPONSE-side defect: the
    route maps this whole class to its fixed ``response_invalid`` refusal.
    Client-side staleness at Apply time is a browser-model state and never
    raises this (R4)."""


MAX_PROPOSAL_SUMMARY_CHARS = 500  # schema maxLength counts characters

# THE PROPOSAL CAP IS A RULE, NOT A NUMBER (add-doxbench-editing-phase-b task
# 5.3). Phase A's `MAX_RESPONSE_PROPOSALS = 2` was the literal buffer count of a
# two-buffer request. The ratified Phase B contract states the bound over the
# REQUEST'S OWN buffer count, so widening the loaded set cannot silently widen
# what one response may rewrite beyond what it was grounded on -- and cannot
# narrow it either, which a fixed 2 would have done the moment a third document
# was loaded.
PROPOSAL_CAP_RULE = (
    "at most one proposal per buffer the request supplied, so a response may "
    "never rewrite more buffers than it was shown"
)

_PROPOSAL_FIELDS = frozenset({"target", "base_hash", "summary", "content"})


def permitted_proposal_targets(observed: ObservedHashes) -> tuple[str, ...]:
    """The closed set of targets one response may name: exactly the BUFFER KEYS
    the request supplied and the model was therefore shown.

    Phase A's `PROPOSAL_TARGETS` was a fixed two-value enum, which is retired
    rather than lengthened: `outline` is the one reserved name and every other
    key is a path the request itself declared, so no module-level constant can
    know the set. Deriving it from the OBSERVED identities -- the same object the
    base-identity check reads -- makes "a target the request did not supply" and
    "a target whose shown identity we do not hold" the same refusal by
    construction, which is what makes an unroutable proposal impossible to guess
    at rather than merely unlikely."""
    return observed.keys()


@dataclasses.dataclass(frozen=True, slots=True)
class TypedProposal:
    """One validated, human-reviewable single-buffer replacement, bound to
    the content identity the model saw (FR-026..FR-029)."""

    target: str
    base_hash: str
    summary: str
    content: str


@dataclasses.dataclass(frozen=True, slots=True)
class ValidatedAssistantResponse:
    """The whole validated typed response: bounded prose plus validated proposals
    with unique targets, AT MOST ONE PER SUPPLIED BUFFER (``PROPOSAL_CAP_RULE``).

    The literal ``0-2`` this docstring used to state was the released v1 wire's own
    bound, which `add-doxbench-editing-phase-b` replaced with a bound expressed over
    the request's buffer count -- so a four-buffer request may carry four proposals
    and a two-buffer one still may not carry three. The v1 wire supplies exactly two
    buffers, so its effective bound is unchanged."""

    assistant_prose: str
    proposals: tuple[TypedProposal, ...]


def validate_assistant_response(
    raw,
    *,
    observed: ObservedHashes,
    permitted_targets: Sequence[str] | None = None,
) -> ValidatedAssistantResponse:
    """Validate a provider's typed response strictly against the released
    contract, refusing with ``TurnResponseError`` on the FIRST defect.

    ``permitted_targets`` defaults to the request's OWN buffer keys
    (``permitted_proposal_targets(observed)``) and may be NARROWED for one turn.
    It exists for the outline-only turn (G-1): when the request declares no
    active document (``active_document_path`` is null — legal from
    contract-v1.28, mirroring the already-nullable ``buffer_state.path``), the
    document buffer is backed by no path at all, so a document-targeted proposal
    would be a rewrite of a document that does not exist. The feature's own
    contract (``specs/010-doxbench-editor-chat/contracts/chat-turn.md``) and
    FR-026/FR-027 are silent on that case; the NARROWEST reading is taken and
    recorded — such a turn is chat grounded on the tile's context with NO
    document-targeted proposal — and it fails closed here rather than producing
    an Apply the buffer layer would have to refuse later. A supplied
    ``permitted_targets`` may only NARROW: a target it names that the request did
    not supply is refused, because a narrowing that admitted a buffer the model
    was never shown would be a widening wearing the wrong name.

    The PROPOSAL CAP is the request's buffer count, not a literal 2
    (``PROPOSAL_CAP_RULE``): at most one proposal per supplied buffer, which
    duplicate-target refusal already implies and which is stated as a bound so an
    over-long list refuses before any per-proposal work is done.

    Order: structural shape -> the count bound -> per-proposal field/bound checks
    (closed four-field surface; target among the supplied keys; 64-lowercase-hex
    base; summary 1..500 characters; content <= ``MAX_PROPOSAL_BYTES`` UTF-8
    bytes — the plan bound, stricter than the schema's transport ceiling) ->
    duplicate-target -> base identity versus ``observed`` -> the SPANNING total
    (prose + all proposal content <= ``MAX_RESPONSE_TOTAL_BYTES``). Prose is
    bounded by ``MAX_ASSISTANT_PROSE_BYTES`` exactly as the model layer
    already enforces; revalidating here keeps this function the single
    authority a route or store can trust on its own."""
    if (not isinstance(raw, dict)
            or set(raw) != {"assistant_prose", "proposals"}
            or not isinstance(raw.get("assistant_prose"), str)
            or not isinstance(raw.get("proposals"), list)):
        raise TurnResponseError("assistant response shape is invalid")
    prose = raw["assistant_prose"]
    prose_bytes = utf8_size(prose)
    if prose_bytes > MAX_ASSISTANT_PROSE_BYTES:
        raise TurnResponseError("assistant prose exceeds the permitted size")
    supplied = permitted_proposal_targets(observed)
    allowed = supplied if permitted_targets is None else tuple(
        target for target in permitted_targets if target in supplied)
    proposals = raw["proposals"]
    # THE CAP, expressed over the request's own buffer count.
    if len(proposals) > len(supplied):
        raise TurnResponseError("too many proposals")
    validated: list[TypedProposal] = []
    seen_targets: set[str] = set()
    total_bytes = prose_bytes
    for item in proposals:
        if not isinstance(item, dict) or set(item) != _PROPOSAL_FIELDS:
            raise TurnResponseError("proposal shape is invalid")
        target = item["target"]
        if not isinstance(target, str) or target not in supplied:
            raise TurnResponseError("proposal target is unknown")
        if target not in allowed:
            # G-1: this turn names no such buffer to rewrite (the outline-only
            # turn's document buffer is backed by no path). Refused as a
            # RESPONSE defect, never a scope refusal -- the request was fine.
            raise TurnResponseError("proposal target is not part of this turn")
        if target in seen_targets:
            raise TurnResponseError("proposal target is duplicated")
        seen_targets.add(target)
        base_hash = item["base_hash"]
        if not _is_lowercase_hex64(base_hash):
            raise TurnResponseError("proposal base identity is malformed")
        summary = item["summary"]
        if (not isinstance(summary, str) or not summary
                or len(summary) > MAX_PROPOSAL_SUMMARY_CHARS):
            raise TurnResponseError("proposal summary is out of bounds")
        content = item["content"]
        if not isinstance(content, str):
            raise TurnResponseError("proposal content must be a string")
        content_bytes = utf8_size(content)
        if content_bytes > MAX_PROPOSAL_BYTES:
            raise TurnResponseError("proposal content exceeds the permitted size")
        shown = observed.for_key(target)
        if base_hash != shown.hex:
            raise TurnResponseError(
                "proposal base identity does not match the shown content")
        total_bytes += content_bytes
        validated.append(TypedProposal(target=target, base_hash=base_hash,
                                       summary=summary, content=content))
    if total_bytes > MAX_RESPONSE_TOTAL_BYTES:
        raise TurnResponseError("the validated response exceeds the total bound")
    return ValidatedAssistantResponse(
        assistant_prose=prose, proposals=tuple(validated))
