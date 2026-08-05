"""doxBench grounded chat-turn prompt envelope, boundary arithmetic, and the
bounded idempotency store (010-doxbench-editor-chat T047 and T048;
data-model.md Sections 1/3/4/7/8; contracts/chat-turn.md; research.md
R4/R5/R8; plan.md Constraints).

This module implements both the request-side envelope/boundary surface
(T047) and the store slice (T048) together. It owns:

* an internal, schema-agnostic prompt envelope assembly
  (``build_prompt_envelope``) that renders exactly nine deterministic
  sections from a scope projection, a pair of working buffers, a bounded
  transcript, and a new human message;
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
from collections.abc import Callable, Sequence
from pathlib import PurePosixPath

from ideation_dashboard.doxbench_hash import (
    MAX_BUFFER_BYTES,
    ContentIdentity,
    content_identity,
    sha256_hex,
    utf8_size,
)
from ideation_dashboard.doxbench_model import (
    SERVER_MAX_INPUT_LIMIT_BYTES,
    SERVER_MAX_OUTPUT_LIMIT_BYTES,
)
from ideation_dashboard.doxbench_scope import ScopeKey, ScopeProjection

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

PROMPT_SECTION_ORDER: tuple[str, ...] = (
    "system_contract",
    "model_data_handling",
    "scope_metadata",
    "working_subject",
    "transcript",
    "outline_buffer",
    "document_buffer",
    "human_message",
    "response_instruction",
)

SYSTEM_CONTRACT_TEXT = (
    "You are the doxBench editor-chat assistant. Ground every answer "
    "strictly in the outline and document buffers, the scope metadata, and "
    "the transcript shown below. Never invent facts about the repository "
    "or the selected model, and never claim access to material outside the "
    "sections provided in this prompt."
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
    buffer and one document buffer."""


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
    its original name-equality shape."""

    ref: str
    revision: str
    text_of: Callable[[str], str | None]


@dataclasses.dataclass(frozen=True, slots=True)
class TranscriptTurn:
    """One prior turn in the bounded transcript. ``role`` is a free-form,
    non-empty label (for example a human or an assistant turn); ``text`` is
    carried exactly, never summarized or truncated."""

    role: str
    text: str


@dataclasses.dataclass(frozen=True, slots=True)
class PromptSection:
    """One of the nine sections a prompt envelope assembles, in the exact
    order ``PROMPT_SECTION_ORDER`` declares."""

    key: str
    text: str


@dataclasses.dataclass(frozen=True, slots=True)
class ObservedHashes:
    """The recomputed content identities observed for the outline and the
    document buffer at assembly time -- never a cached value from an
    earlier turn (FR-016)."""

    outline: ContentIdentity
    document: ContentIdentity


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
    document_bytes: int,
    message_bytes: int,
    working_subject_bytes: int,
    transcript_bytes: int,
) -> None:
    measured = (
        outline_bytes + document_bytes + message_bytes + working_subject_bytes + transcript_bytes
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
    active_document_path: str | None,
    outline_path: str | None,
    document_path: str | None,
) -> None:
    """Independently revalidate a turn's scope binding against a projection
    a scope authority already produced. Refuses (``TurnScopeError``) unless:
    the request scope equals the projection's own active binding; the
    active document path equals the supplied document path; and every
    non-``None`` path among ``outline_path``/``document_path`` is both
    in-scope (``projection.context_paths``) and editable
    (``projection.editable_paths``) -- a readable-but-not-editable path is
    always refused before any disclosure. A ``None`` document path (a
    buffer not yet created) is exempt from the in-scope/editable checks.
    Every refusal here leaks no projection or buffer content."""
    if request_scope != projection.key:
        raise TurnScopeError("request scope does not match the projection's active binding")
    if active_document_path != document_path:
        raise TurnScopeError("active document path does not match the supplied document path")
    for path in (outline_path, document_path):
        if path is None:
            continue
        _require_in_scope_and_editable(path, projection)


# ---------------------------------------------------------------------------
# buffer-kind requirement
# ---------------------------------------------------------------------------


def require_outline_and_document(buffers) -> tuple[TurnBuffer, TurnBuffer]:
    """Require exactly one outline buffer and one document buffer, in any
    order. Refuses (``TurnBufferKindError``) on a missing, duplicated, or
    unexpected buffer kind."""
    outline: TurnBuffer | None = None
    document: TurnBuffer | None = None
    for buffer in buffers:
        if buffer.kind == "outline":
            if outline is not None:
                raise TurnBufferKindError("more than one outline buffer was supplied")
            outline = buffer
        elif buffer.kind == "document":
            if document is not None:
                raise TurnBufferKindError("more than one document buffer was supplied")
            document = buffer
        else:
            raise TurnBufferKindError("unexpected buffer kind")
    if outline is None or document is None:
        raise TurnBufferKindError(
            "exactly one outline buffer and one document buffer are required"
        )
    return outline, document


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
    detection is made precise, not weakened. ``base_ref`` keeps its meaning
    (provenance: where these base bytes came from) and is never rewritten
    here or anywhere else. Never echoes the buffer's path, repository,
    ref, or content."""
    if buffer.path != expected_path or buffer.repository != request_scope.repository:
        raise TurnScopeError(
            "working buffer is not bound to the validated scope projection"
        )
    if buffer.base_ref == request_scope.ref:
        return
    if (
        session_base is not None
        and buffer.base_ref == session_base.ref
        and buffer.base_revision == session_base.revision
        and buffer.base_hash == _session_text_identity(session_base, expected_path)
    ):
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
) -> PromptEnvelope:
    """Assemble the deterministic, nine-section prompt envelope for one
    chat turn. Order of operations is load-bearing: scope and editable
    revalidation runs first, then the buffer-kind requirement, then the
    buffer-binding check (each buffer's path/repository/base_ref against
    the validated projection and request scope -- widened for a session
    scope by ``session_base`` to accept a buffer based on the session's
    own recorded base, T104 R-12), then exact identity verification for
    each buffer, and only then is any section text assembled -- so a
    scope, binding, or identity refusal never discloses a partial
    envelope or buffer content."""
    revalidate_scope(
        projection=projection,
        request_scope=request_scope,
        active_document_path=active_document_path,
        outline_path=projection.outline_path,
        document_path=active_document_path,
    )
    outline, document = require_outline_and_document(buffers)
    _require_buffer_binding(outline, projection.outline_path, request_scope,
                            session_base)
    _require_buffer_binding(document, active_document_path, request_scope,
                            session_base)
    outline_identity = verify_buffer_identity(outline)
    document_identity = verify_buffer_identity(document)

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
        _buffer_section("outline_buffer", outline),
        _buffer_section("document_buffer", document),
        _human_message_section(message),
        PromptSection(key="response_instruction", text=RESPONSE_INSTRUCTION_TEXT),
    )

    return PromptEnvelope(
        sections=sections,
        scope=request_scope,
        model_id=model_id,
        message=message,
        transcript=tuple(transcript),
        active_document_path=active_document_path,
        observed_hashes=ObservedHashes(outline=outline_identity, document=document_identity),
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
# {target, base_hash, summary, content}, 0-2 proposals, unique targets).
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
MAX_RESPONSE_PROPOSALS = 2
PROPOSAL_TARGETS: tuple[str, ...] = ("outline", "document")
_PROPOSAL_FIELDS = frozenset({"target", "base_hash", "summary", "content"})


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
    """The whole validated typed response: bounded prose plus 0-2 validated
    proposals with unique targets."""

    assistant_prose: str
    proposals: tuple[TypedProposal, ...]


def validate_assistant_response(
    raw,
    *,
    observed: ObservedHashes,
    permitted_targets: Sequence[str] = PROPOSAL_TARGETS,
) -> ValidatedAssistantResponse:
    """Validate a provider's typed response strictly against the released
    contract, refusing with ``TurnResponseError`` on the FIRST defect.

    ``permitted_targets`` narrows the enum for ONE turn. It exists for the
    outline-only turn (G-1): when the request declares no active document
    (``active_document_path`` is null — legal from contract-v1.28, mirroring
    the already-nullable ``buffer_state.path``), the document buffer is backed
    by no path at all, so a document-targeted proposal would be a rewrite of a
    document that does not exist. The feature's own contract
    (``specs/010-doxbench-editor-chat/contracts/chat-turn.md``) and FR-026/
    FR-027 are silent on that case; the NARROWEST reading is taken and
    recorded — such a turn is chat grounded on the tile's context with NO
    document-targeted proposal — and it fails closed here rather than
    producing an Apply the buffer layer would have to refuse later. The
    default is the full enum, so every turn that DOES name a document is
    unchanged.

    Order: structural shape -> per-proposal field/bound checks (closed
    four-field surface; target enum; 64-lowercase-hex base; summary 1..500
    characters; content <= ``MAX_PROPOSAL_BYTES`` UTF-8 bytes — the plan
    bound, stricter than the schema's transport ceiling) -> duplicate-target
    -> base identity versus ``observed`` -> the SPANNING total
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
    proposals = raw["proposals"]
    if len(proposals) > MAX_RESPONSE_PROPOSALS:
        raise TurnResponseError("too many proposals")
    validated: list[TypedProposal] = []
    seen_targets: set[str] = set()
    total_bytes = prose_bytes
    for item in proposals:
        if not isinstance(item, dict) or set(item) != _PROPOSAL_FIELDS:
            raise TurnResponseError("proposal shape is invalid")
        target = item["target"]
        if target not in PROPOSAL_TARGETS:
            raise TurnResponseError("proposal target is unknown")
        if target not in permitted_targets:
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
        shown = observed.outline if target == "outline" else observed.document
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
