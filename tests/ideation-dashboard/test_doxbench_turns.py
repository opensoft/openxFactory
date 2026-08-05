"""Tests for the doxBench grounded chat-turn prompt envelope, boundary
arithmetic, and bounded idempotency store (010-doxbench-editor-chat
T040/T041/T042; data-model.md Sections 1/3/4/7/8; contracts/chat-turn.md;
research.md R4/R5/R8; plan.md Constraints).

T047/T048 implement this module (``ideation_dashboard.doxbench_turns``); the
suite below is fully green, including the regression tests pinning a
null-path buffer-disclosure defect (see the null-path buffer disclosure
section) that was fixed by rendering a fixed ``"Path: (not yet created)"``
placeholder header instead of disclosing the buffer unguarded. Three groups
below mirror the three task numbers exactly:

* T040 -- prompt envelope assembly (deterministic 9-section order), complete
  (never truncated/normalized) buffers, FR-014 working-state labels, and
  FR-013/FR-015/FR-016 exact-identity and scope-revalidation behavior.
* T041 -- content, transcript, message, output, and route-body boundary
  arithmetic (exact UTF-8 bytes, never code points), plus FR-017 redacted
  refusal shape.
* T042 -- the bounded, thread-safe, dedicated one-in-flight/idempotency store
  (the T048 store), including real ``threading`` concurrency proofs.

HARD BOUNDARIES enforced by sentinel tests at the bottom: no wire schema (no
quoted ``"schema_version"``/``"kind"`` literal -- the prompt/request
representation here is an internal, schema-agnostic Python shape only), no
response decoding (T041's output-side assertions are pure arithmetic
constants only), no routes/serve.py/browser coupling, and a hermetic,
stdlib-plus-doxbench-helpers-only module with no wall-clock LRU ordering.
"""

from __future__ import annotations

import copy
import dataclasses
import json
import threading

import pytest

from conftest import FIXTURES, REPO_ROOT

from ideation_dashboard.doxbench_hash import (
    ContentEncodingError,
    ContentIdentity,
    content_identity,
    sha256_hex,
    utf8_size,
)
from ideation_dashboard.doxbench_hash import MAX_BUFFER_BYTES as HASH_MAX_BUFFER_BYTES
from ideation_dashboard.doxbench_scope import ScopeKey, ScopeProjection, resolve_scope
from ideation_dashboard.doxbench_model import (
    SERVER_MAX_INPUT_LIMIT_BYTES,
    SERVER_MAX_OUTPUT_LIMIT_BYTES,
    ModelCatalogEntry,
    effective_limit_bytes,
)

from ideation_dashboard.doxbench_turns import (
    MAX_ASSISTANT_PROSE_BYTES,
    MAX_IDEMPOTENCY_BYTES,
    MAX_IDEMPOTENCY_ENTRIES,
    MAX_MESSAGE_BYTES,
    MAX_PROPOSAL_BYTES,
    MAX_REQUEST_BODY_BYTES,
    MAX_RESPONSE_TOTAL_BYTES,
    MAX_TRANSCRIPT_BYTES,
    MAX_TRANSCRIPT_TURNS,
    MAX_WORKING_SUBJECT_BYTES,
    PROMPT_SECTION_ORDER,
    RESPONSE_INSTRUCTION_TEXT,
    SYSTEM_CONTRACT_TEXT,
    TURN_STATE_COMPLETED,
    TURN_STATE_FAILED,
    TURN_STATE_IN_FLIGHT,
    WORKING_STATE_CLEAN_LABEL,
    WORKING_STATE_DIRTY_LABEL,
    ObservedHashes,
    PromptEnvelope,
    PromptSection,
    TranscriptTurn,
    TurnBlankMessageError,
    TurnBuffer,
    TurnBufferKindError,
    TurnConflictError,
    TurnError,
    TurnIdentityMismatchError,
    TurnLease,
    TurnLimitError,
    TurnRecord,
    TurnScopeError,
    TurnStore,
    build_prompt_envelope,
    require_outline_and_document,
    revalidate_scope,
    transcript_bytes,
    validate_message,
    validate_request_body_bytes,
    validate_transcript,
    validate_working_subject,
    verify_buffer_identity,
)
from ideation_dashboard import doxbench_turns

MODULE_PATH = REPO_ROOT / "scripts" / "ideation_dashboard" / "doxbench_turns.py"

REPOSITORY = "openxFactory"
REF = "draft/demo-topic"


# ---------------------------------------------------------------------------
# shared fixture builders
# ---------------------------------------------------------------------------


def _projection(
    key: ScopeKey,
    *,
    context_paths,
    editable_paths=(),
    outline_path=None,
) -> ScopeProjection:
    """A hand-built ScopeProjection. ScopeProjection has no __post_init__, so
    constructing it directly (rather than through resolve_scope) is safe and
    lets each test control exactly which paths are readable vs. editable --
    the task's own explicitly permitted shortcut for revalidation tests."""
    return ScopeProjection(
        key=key,
        title="Fixture Tile",
        keywords=(),
        source_revision="abc123",
        sections=(),
        context_paths=tuple(context_paths),
        editable_paths=tuple(editable_paths),
        outline_path=outline_path,
        active_document_candidates=tuple(context_paths),
    )


def _key(tile_id: str = "demo-topic", tile_kind: str = "staged") -> ScopeKey:
    return ScopeKey(repository=REPOSITORY, ref=REF, tile_kind=tile_kind, tile_id=tile_id)


OUTLINE_PATH = "ideation/staging/demo-topic/demo-topic.md"
DOCUMENT_PATH = "ideation/staging/demo-topic/note.md"


def _valid_projection(*, extra_context=()) -> ScopeProjection:
    return _projection(
        _key(),
        context_paths=(OUTLINE_PATH, DOCUMENT_PATH, *extra_context),
        editable_paths=(OUTLINE_PATH, DOCUMENT_PATH),
        outline_path=OUTLINE_PATH,
    )


def _buffer(
    kind: str,
    *,
    path: str | None,
    content: str,
    dirty: bool = False,
    content_hash: str | None = None,
    base_hash: str | None = None,
    repository: str = REPOSITORY,
    base_ref: str = REF,
    base_revision: str = "abc123",
) -> TurnBuffer:
    real_hex = content_identity(content).hex
    return TurnBuffer(
        kind=kind,
        repository=repository,
        path=path,
        base_ref=base_ref,
        base_revision=base_revision,
        base_hash=base_hash if base_hash is not None else real_hex,
        content_hash=content_hash if content_hash is not None else real_hex,
        content=content,
        dirty=dirty,
    )


OUTLINE_CONTENT = "# Demo topic\n\nOutline body.\n"
DOCUMENT_CONTENT = "# Note\n\nDocument body.\n"


def _valid_buffers(
    *,
    outline_content: str = OUTLINE_CONTENT,
    document_content: str = DOCUMENT_CONTENT,
    outline_dirty: bool = False,
    document_dirty: bool = False,
):
    return [
        _buffer("outline", path=OUTLINE_PATH, content=outline_content, dirty=outline_dirty),
        _buffer("document", path=DOCUMENT_PATH, content=document_content, dirty=document_dirty),
    ]


def _build_envelope(
    *,
    projection: ScopeProjection | None = None,
    request_scope: ScopeKey | None = None,
    active_document_path: str = DOCUMENT_PATH,
    model_id: str = "opaque-local-id",
    model_data_handling: str = "Processed in the approved tenant boundary",
    model_input_limit_bytes: int = 800_000,
    model_output_limit_bytes: int = 900_000,
    working_subject: str = "Clarify the acceptance boundary",
    transcript=(),
    buffers=None,
    message: str = "Which open question should we close next?",
    session_base=None,
) -> PromptEnvelope:
    return build_prompt_envelope(
        projection=projection if projection is not None else _valid_projection(),
        request_scope=request_scope if request_scope is not None else _key(),
        active_document_path=active_document_path,
        model_id=model_id,
        model_data_handling=model_data_handling,
        model_input_limit_bytes=model_input_limit_bytes,
        model_output_limit_bytes=model_output_limit_bytes,
        working_subject=working_subject,
        transcript=tuple(transcript),
        buffers=buffers if buffers is not None else _valid_buffers(),
        message=message,
        session_base=session_base,
    )


# ===========================================================================
# T040 -- prompt envelope, complete buffers, working-state labels, identities
# ===========================================================================


def test_prompt_section_order_is_the_nine_step_deterministic_sequence():
    assert PROMPT_SECTION_ORDER == (
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


def test_envelope_sections_are_assembled_in_the_exact_declared_order():
    envelope = _build_envelope()
    assert [section.key for section in envelope.sections] == list(PROMPT_SECTION_ORDER)
    assert all(isinstance(section, PromptSection) for section in envelope.sections)


def test_assembly_is_byte_for_byte_deterministic_for_identical_input():
    first = _build_envelope()
    second = _build_envelope()
    assert first.rendered().encode("utf-8") == second.rendered().encode("utf-8")
    assert [(s.key, s.text) for s in first.sections] == [(s.key, s.text) for s in second.sections]


def test_system_contract_and_response_instruction_are_the_fixed_constants():
    envelope = _build_envelope()
    system_section = envelope.sections[0]
    instruction_section = envelope.sections[-1]
    assert system_section.key == "system_contract"
    assert system_section.text == SYSTEM_CONTRACT_TEXT
    assert instruction_section.key == "response_instruction"
    assert instruction_section.text == RESPONSE_INSTRUCTION_TEXT


def test_model_data_handling_section_carries_the_selected_facts():
    envelope = _build_envelope(
        model_id="opaque-local-id",
        model_data_handling="Processed in the approved tenant boundary",
        model_input_limit_bytes=800_000,
        model_output_limit_bytes=900_000,
    )
    section = envelope.sections[1]
    assert section.key == "model_data_handling"
    assert "opaque-local-id" in section.text
    assert "Processed in the approved tenant boundary" in section.text
    assert "800000" in section.text or "800,000" in section.text
    assert "900000" in section.text or "900,000" in section.text


def test_scope_metadata_section_carries_repository_ref_and_tile():
    envelope = _build_envelope()
    section = envelope.sections[2]
    assert section.key == "scope_metadata"
    assert REPOSITORY in section.text
    assert REF in section.text
    assert "staged" in section.text
    assert "demo-topic" in section.text


def test_working_subject_section_carries_the_exact_text():
    envelope = _build_envelope(working_subject="Clarify the acceptance boundary")
    section = envelope.sections[3]
    assert section.key == "working_subject"
    assert "Clarify the acceptance boundary" in section.text


def test_human_message_section_carries_the_exact_new_message():
    envelope = _build_envelope(message="Which open question should we close next?")
    section = envelope.sections[7]
    assert section.key == "human_message"
    assert "Which open question should we close next?" in section.text


def test_exactly_one_outline_and_one_document_buffer_required():
    outline = _buffer("outline", path=OUTLINE_PATH, content=OUTLINE_CONTENT)
    document = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT)
    resolved_outline, resolved_document = require_outline_and_document([document, outline])
    assert resolved_outline is outline
    assert resolved_document is document


def test_missing_document_buffer_refuses():
    outline = _buffer("outline", path=OUTLINE_PATH, content=OUTLINE_CONTENT)
    with pytest.raises(TurnBufferKindError):
        require_outline_and_document([outline])


def test_missing_outline_buffer_refuses():
    document = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT)
    with pytest.raises(TurnBufferKindError):
        require_outline_and_document([document])


def test_empty_buffer_list_refuses():
    with pytest.raises(TurnBufferKindError):
        require_outline_and_document([])


def test_duplicate_kind_refuses():
    one = _buffer("outline", path=OUTLINE_PATH, content=OUTLINE_CONTENT)
    two = _buffer("outline", path=OUTLINE_PATH, content="different")
    document = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT)
    with pytest.raises(TurnBufferKindError):
        require_outline_and_document([one, two, document])


def test_extra_unexpected_kind_refuses():
    outline = _buffer("outline", path=OUTLINE_PATH, content=OUTLINE_CONTENT)
    document = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT)
    rogue = _buffer("comment", path="ideation/staging/demo-topic/scratch.md", content="x")
    with pytest.raises(TurnBufferKindError):
        require_outline_and_document([outline, document, rogue])


def test_build_prompt_envelope_refuses_the_same_way_on_bad_buffer_kinds():
    with pytest.raises(TurnBufferKindError):
        _build_envelope(buffers=[_buffer("outline", path=OUTLINE_PATH, content=OUTLINE_CONTENT)])


# --- complete, never-truncated buffers -------------------------------------


def test_full_outline_and_document_content_survive_exactly_in_their_sections():
    envelope = _build_envelope()
    outline_section = envelope.sections[5]
    document_section = envelope.sections[6]
    assert outline_section.key == "outline_buffer"
    assert document_section.key == "document_buffer"
    assert OUTLINE_CONTENT in outline_section.text
    assert DOCUMENT_CONTENT in document_section.text


def test_buffer_at_the_exact_400000_byte_boundary_is_accepted_and_survives_whole():
    marker = "BOUNDARY-MARKER-"
    padding = "A" * (HASH_MAX_BUFFER_BYTES - utf8_size(marker))
    content = marker + padding
    assert utf8_size(content) == HASH_MAX_BUFFER_BYTES == 400_000

    envelope = _build_envelope(buffers=_valid_buffers(document_content=content))
    document_section = envelope.sections[6]
    assert content in document_section.text
    assert marker in document_section.text


def test_crlf_content_is_preserved_exactly_no_newline_normalization():
    content = "Line1\r\nLine2\r\nLine3\r\n"
    envelope = _build_envelope(buffers=_valid_buffers(document_content=content))
    document_section = envelope.sections[6]
    assert content in document_section.text
    assert "Line1\r\nLine2" in document_section.text
    # a normalizer that rewrote CRLF to LF would break this exact substring
    assert "Line1\nLine2" not in document_section.text.replace("Line1\r\nLine2", "")


def test_combining_character_content_is_preserved_not_composed():
    combining = 'Café'  # "e" + COMBINING ACUTE ACCENT (U+0301), not the precomposed "e-acute"
    composed = 'Café'  # precomposed U+00E9 -- a different byte sequence entirely
    assert combining != composed
    content = f"marker-combining-{combining}-end"
    envelope = _build_envelope(buffers=_valid_buffers(document_content=content))
    document_section = envelope.sections[6]
    assert content in document_section.text
    assert combining in document_section.text
    # a normalizer that composed the accent would rewrite this exact substring
    # away, so its absence would only prove normalization happened silently.
    assert f"marker-combining-{composed}-end" not in document_section.text


def test_astral_plane_character_content_is_preserved_exactly():
    astral = "\U0001F600" * 5  # GRINNING FACE, outside the BMP
    content = f"marker-astral-{astral}-end"
    envelope = _build_envelope(buffers=_valid_buffers(document_content=content))
    document_section = envelope.sections[6]
    assert content in document_section.text
    assert astral in document_section.text


def test_transcript_is_bounded_but_never_selected_or_summarized():
    turns = tuple(TranscriptTurn(role="human", text=f"turn-{i}") for i in range(5))
    envelope = _build_envelope(transcript=turns)
    transcript_section = envelope.sections[4]
    assert transcript_section.key == "transcript"
    for turn in turns:
        assert turn.text in transcript_section.text


# --- FR-014 working-state labels -------------------------------------------


def test_dirty_buffer_carries_the_explicit_dirty_working_state_label():
    envelope = _build_envelope(buffers=_valid_buffers(document_dirty=True))
    document_section = envelope.sections[6]
    assert WORKING_STATE_DIRTY_LABEL in document_section.text
    assert WORKING_STATE_CLEAN_LABEL not in document_section.text


def test_clean_buffer_carries_the_explicit_clean_working_state_label():
    envelope = _build_envelope(buffers=_valid_buffers(document_dirty=False))
    document_section = envelope.sections[6]
    assert WORKING_STATE_CLEAN_LABEL in document_section.text
    assert WORKING_STATE_DIRTY_LABEL not in document_section.text


def test_outline_and_document_labels_are_independent_of_each_other():
    envelope = _build_envelope(buffers=_valid_buffers(outline_dirty=True, document_dirty=False))
    outline_section = envelope.sections[5]
    document_section = envelope.sections[6]
    assert WORKING_STATE_DIRTY_LABEL in outline_section.text
    assert WORKING_STATE_CLEAN_LABEL in document_section.text


def test_clean_and_dirty_labels_are_distinct_strings():
    assert WORKING_STATE_CLEAN_LABEL != WORKING_STATE_DIRTY_LABEL
    assert "GOVERNED" in WORKING_STATE_CLEAN_LABEL or "COMMITTED" in WORKING_STATE_CLEAN_LABEL
    assert "GOVERNED" not in WORKING_STATE_DIRTY_LABEL
    assert "COMMITTED" not in WORKING_STATE_DIRTY_LABEL


# --- FR-013 envelope carries the required fields ----------------------------


def test_envelope_exposes_fr013_required_fields():
    turns = (TranscriptTurn(role="human", text="earlier question"),)
    envelope = _build_envelope(
        transcript=turns,
        message="new message text",
        model_id="opaque-local-id",
    )
    assert envelope.scope == _key()
    assert envelope.model_id == "opaque-local-id"
    assert envelope.message == "new message text"
    assert envelope.transcript == turns
    assert envelope.active_document_path == DOCUMENT_PATH
    assert isinstance(envelope.observed_hashes, ObservedHashes)
    assert isinstance(envelope.observed_hashes.outline, ContentIdentity)
    assert isinstance(envelope.observed_hashes.document, ContentIdentity)


# --- exact identity recompute / mismatch refusal ----------------------------


def test_verify_buffer_identity_returns_the_recomputed_identity_and_is_64_lowercase_hex():
    buffer = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT)
    identity = verify_buffer_identity(buffer)
    assert identity.hex == content_identity(DOCUMENT_CONTENT).hex
    assert len(identity.hex) == 64
    assert identity.hex == identity.hex.lower()
    assert identity.algorithm == "sha256"


def test_content_hash_mismatch_refuses():
    buffer = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT, content_hash="0" * 64)
    with pytest.raises(TurnIdentityMismatchError):
        verify_buffer_identity(buffer)


def test_malformed_base_hash_refuses():
    buffer = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT, base_hash="not-a-hex-digest")
    with pytest.raises(TurnIdentityMismatchError):
        verify_buffer_identity(buffer)


def test_short_base_hash_refuses():
    buffer = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT, base_hash="abc123")
    with pytest.raises(TurnIdentityMismatchError):
        verify_buffer_identity(buffer)


def test_uppercase_base_hash_refuses_lowercase_only():
    buffer = _buffer(
        "document",
        path=DOCUMENT_PATH,
        content=DOCUMENT_CONTENT,
        base_hash=content_identity(DOCUMENT_CONTENT).hex.upper(),
    )
    with pytest.raises(TurnIdentityMismatchError):
        verify_buffer_identity(buffer)


def test_identity_mismatch_error_never_echoes_the_buffer_content():
    sentinel = "SENTINEL-LEAK-CHECK-CONTENT-XYZ"
    buffer = _buffer("document", path=DOCUMENT_PATH, content=sentinel, content_hash="0" * 64)
    with pytest.raises(TurnIdentityMismatchError) as raised:
        verify_buffer_identity(buffer)
    assert sentinel not in str(raised.value)


def test_lone_surrogate_buffer_content_raises_content_encoding_error_not_a_turn_error():
    """The SIBLING-EXCEPTION contract the route relies on (T104 F5-8).

    A lone UTF-16 surrogate in buffer content makes `utf8_size` inside
    `verify_buffer_identity` raise `doxbench_hash.ContentEncodingError` —
    which is a plain ValueError and deliberately NOT a `TurnError`, so an
    `except` written for the turn hierarchy does not catch it. serve.py's
    chat-turn route catches this class EXPLICITLY at every site that
    measures or hashes request text; this pin is what makes silently
    rehoming the exception under `TurnError` (which would change what those
    handlers catch) a visible contract change rather than a drive-by.
    Constructed directly rather than via `_buffer`, whose own
    `content_identity` call would trip the same error in the test process.
    The hashes are well-formed hex so the encoding refusal is proven to fire
    BEFORE any hash comparison could."""
    buffer = TurnBuffer(
        kind="document", repository=REPOSITORY, path=DOCUMENT_PATH,
        base_ref=REF, base_revision="abc123",
        base_hash="0" * 64, content_hash="0" * 64,
        content="broken \ud800 text", dirty=True)
    with pytest.raises(ContentEncodingError):
        verify_buffer_identity(buffer)
    assert not issubclass(ContentEncodingError, TurnError)
    assert issubclass(ContentEncodingError, ValueError)


def test_build_prompt_envelope_refuses_on_content_hash_mismatch_for_either_buffer():
    buffers = _valid_buffers()
    buffers[1] = _buffer(
        "document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT, content_hash="f" * 64
    )
    with pytest.raises(TurnIdentityMismatchError):
        _build_envelope(buffers=buffers)


# --- FR-015 scope revalidation ----------------------------------------------


def test_revalidate_scope_accepts_a_fully_matching_binding():
    projection = _valid_projection()
    revalidate_scope(
        projection=projection,
        request_scope=_key(),
        active_document_path=DOCUMENT_PATH,
        outline_path=OUTLINE_PATH,
        document_path=DOCUMENT_PATH,
    )


def test_revalidate_scope_refuses_when_request_scope_does_not_equal_the_active_binding():
    projection = _valid_projection()
    mismatched = ScopeKey(repository=REPOSITORY, ref=REF, tile_kind="staged", tile_id="other-topic")
    with pytest.raises(TurnScopeError):
        revalidate_scope(
            projection=projection,
            request_scope=mismatched,
            active_document_path=DOCUMENT_PATH,
            outline_path=OUTLINE_PATH,
            document_path=DOCUMENT_PATH,
        )


def test_revalidate_scope_refuses_when_active_document_path_does_not_match_document_buffer():
    projection = _valid_projection(extra_context=("ideation/staging/demo-topic/other.md",))
    with pytest.raises(TurnScopeError):
        revalidate_scope(
            projection=projection,
            request_scope=_key(),
            active_document_path="ideation/staging/demo-topic/other.md",
            outline_path=OUTLINE_PATH,
            document_path=DOCUMENT_PATH,
        )


def test_revalidate_scope_refuses_an_out_of_scope_document_path():
    projection = _projection(_key(), context_paths=(OUTLINE_PATH,), outline_path=OUTLINE_PATH)
    with pytest.raises(TurnScopeError):
        revalidate_scope(
            projection=projection,
            request_scope=_key(),
            active_document_path=DOCUMENT_PATH,
            outline_path=OUTLINE_PATH,
            document_path=DOCUMENT_PATH,
        )


def test_revalidate_scope_refuses_a_traversal_shaped_document_path():
    projection = _projection(_key(), context_paths=(OUTLINE_PATH,), outline_path=OUTLINE_PATH)
    with pytest.raises(TurnScopeError):
        revalidate_scope(
            projection=projection,
            request_scope=_key(),
            active_document_path="../../etc/passwd",
            outline_path=OUTLINE_PATH,
            document_path="../../etc/passwd",
        )


def test_revalidate_scope_refuses_an_out_of_scope_outline_path():
    projection = _projection(_key(), context_paths=(DOCUMENT_PATH,), outline_path=DOCUMENT_PATH)
    with pytest.raises(TurnScopeError):
        revalidate_scope(
            projection=projection,
            request_scope=_key(),
            active_document_path=DOCUMENT_PATH,
            outline_path="ideation/staging/demo-topic/not-the-outline.md",
            document_path=DOCUMENT_PATH,
        )


def test_readable_but_not_editable_document_path_is_refused_before_disclosure():
    # A cited/inherited path is readable (in context_paths) but never editable
    # merely because it is readable (data-model.md Section 2). FR-015
    # requires editable_paths membership before any content is disclosed, so
    # revalidate_scope must REFUSE a readable-but-not-editable document path.
    #
    # The sentinel is embedded IN the offending path itself (the only thing
    # revalidate_scope actually receives here) so the leak assertion below is
    # real: if a future refusal message ever echoed the rejected path, this
    # assertion would catch it. A sentinel defined but never threaded into
    # any argument the function receives can never fail -- see the Item B
    # audit note at the bottom of this module for every other place this
    # pattern was checked.
    sentinel = "SENTINEL-LEAK-CHECK-SCOPE-REFUSAL"
    cited_path = f"ideation/brainstorm/{sentinel}-a.md"
    projection = _projection(
        _key(),
        context_paths=(OUTLINE_PATH, cited_path),
        editable_paths=(OUTLINE_PATH,),
        outline_path=OUTLINE_PATH,
    )
    assert cited_path in projection.context_paths
    assert cited_path not in projection.editable_paths
    with pytest.raises(TurnScopeError) as raised:
        revalidate_scope(
            projection=projection,
            request_scope=_key(),
            active_document_path=cited_path,
            outline_path=OUTLINE_PATH,
            document_path=cited_path,
        )
    assert sentinel not in str(raised.value)
    assert cited_path not in str(raised.value)


def test_readable_but_not_editable_path_refuses_before_identity_verification_or_prompt_assembly():
    # Both a readable-but-not-editable document path AND a content-hash
    # mismatch are present at once. If TurnScopeError wins (not
    # TurnIdentityMismatchError), scope/editable revalidation ran first --
    # proving refusal happens before identity verification or any prompt
    # text is assembled (contracts/chat-turn.md pre-dispatch ordering,
    # FR-015).
    sentinel = "SENTINEL-LEAK-CHECK-BUFFER-CONTENT"
    cited_path = "ideation/brainstorm/a.md"
    projection = _projection(
        _key(),
        context_paths=(OUTLINE_PATH, cited_path),
        editable_paths=(OUTLINE_PATH,),
        outline_path=OUTLINE_PATH,
    )
    buffers = _valid_buffers()
    buffers[1] = _buffer(
        "document",
        path=cited_path,
        content=sentinel,
        content_hash="e" * 64,
    )
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(
            _build_envelope(
                projection=projection,
                active_document_path=cited_path,
                buffers=buffers,
            )
        )
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)


def test_scope_revalidation_uses_the_real_scope_authority_for_a_realistic_fixture(tmp_path):
    cases = json.loads((FIXTURES / "doxbench_scope_cases.json").read_text(encoding="utf-8"))
    snapshot = cases["snapshot"]
    key = ScopeKey(repository="fixture-repo", ref="main", tile_kind="staged", tile_id="topic-x")
    projection = resolve_scope(snapshot, key, source_root=tmp_path)
    assert projection is not None
    owned_path = "ideation/staging/topic-x/topic-x.md"
    non_owned_context_path = "ideation/brainstorm/b.md"
    assert owned_path in projection.editable_paths
    assert non_owned_context_path in projection.context_paths
    assert non_owned_context_path not in projection.editable_paths
    # Disclosure requires edit authority: the real, editable owned path
    # resolves fine.
    revalidate_scope(
        projection=projection,
        request_scope=key,
        active_document_path=owned_path,
        outline_path=projection.outline_path,
        document_path=owned_path,
    )
    # A real readable-but-not-editable path refuses.
    with pytest.raises(TurnScopeError):
        revalidate_scope(
            projection=projection,
            request_scope=key,
            active_document_path=non_owned_context_path,
            outline_path=projection.outline_path,
            document_path=non_owned_context_path,
        )
    # But a real out-of-scope path still refuses.
    with pytest.raises(TurnScopeError):
        revalidate_scope(
            projection=projection,
            request_scope=key,
            active_document_path="docs/not-in-scope.md",
            outline_path=projection.outline_path,
            document_path="docs/not-in-scope.md",
        )


# ---------------------------------------------------------------------------
# T104 F2 (PR #63 second review, P1 doxbench_scope.py:398): EVERY ADVERTISED
# CANDIDATE MUST SURVIVE THIS MODULE'S OWN GUARD
#
# The scope authority publishes `active_document_candidates` and this module
# decides which paths a turn may name. Both halves were tested -- separately.
# `test_doxbench_scope.py` asserted the published list; the tests above assert
# the guard; nothing JOINED them, so the suite stayed green while the two
# disagreed by construction: candidates were `context_paths` (everything
# readable) and the guard requires `context_paths` AND `editable_paths`.
# Executed against this repo's own fixture, that made every candidate on a
# cluster/possible tile and every non-owned candidate on a staged tile refuse.
#
# The join below is the guard: for EVERY fixture case, EVERY published
# candidate is fed to the real `revalidate_scope` alongside the projection's
# own `outline_path`. A candidate the turn guard refuses is not a candidate.
# ---------------------------------------------------------------------------

def _fixture_cases():
    return json.loads((FIXTURES / "doxbench_scope_cases.json").read_text(encoding="utf-8"))


def test_every_published_candidate_passes_the_real_turn_guard_on_every_fixture(tmp_path):
    """The two halves, joined over the real fixtures: the derivation's own
    output, fed to the guard's own function, tile by tile and path by path."""
    cases = _fixture_cases()
    snapshot = cases["snapshot"]
    checked = 0
    for case in cases["cases"]:
        key = ScopeKey(repository=case["repository"], ref=case["ref"],
                       tile_kind=case["tile_kind"], tile_id=case["tile_id"])
        projection = resolve_scope(snapshot, key, source_root=tmp_path,
                                   created_paths=case["created_paths"])
        if projection is None:
            continue
        for candidate in projection.active_document_candidates:
            checked += 1
            revalidate_scope(
                projection=projection,
                request_scope=key,
                active_document_path=candidate,
                outline_path=projection.outline_path,
                document_path=candidate,
            )
    assert checked, "no fixture case published a candidate to check"


def test_a_published_outline_path_always_passes_the_real_turn_guard(tmp_path):
    """The outline buffer rides EVERY turn on its tile (`build_prompt_envelope`
    passes `projection.outline_path` itself), so a published outline the guard
    refuses kills that tile's chat outright, whatever document is active. The
    `picked-possible` fixture case is exactly that: its outline was resolved
    from ANOTHER tile's staged folder, outside its own scope."""
    cases = _fixture_cases()
    snapshot = cases["snapshot"]
    for case in cases["cases"]:
        key = ScopeKey(repository=case["repository"], ref=case["ref"],
                       tile_kind=case["tile_kind"], tile_id=case["tile_id"])
        projection = resolve_scope(snapshot, key, source_root=tmp_path,
                                   created_paths=case["created_paths"])
        if projection is None or projection.outline_path is None:
            continue
        revalidate_scope(
            projection=projection,
            request_scope=key,
            active_document_path=None,
            outline_path=projection.outline_path,
            document_path=None,
        )


def test_no_candidate_is_ever_the_outline_buffers_own_path(tmp_path):
    """Aliasing guard (P1 staging-workbench-model.js:414): offering the outline
    as the active DOCUMENT gives the operator two independent working copies of
    one file -- two Save rows for one document, and the second one refused
    forever on a base the first just moved."""
    cases = _fixture_cases()
    snapshot = cases["snapshot"]
    for case in cases["cases"]:
        key = ScopeKey(repository=case["repository"], ref=case["ref"],
                       tile_kind=case["tile_kind"], tile_id=case["tile_id"])
        projection = resolve_scope(snapshot, key, source_root=tmp_path,
                                   created_paths=case["created_paths"])
        if projection is None or projection.outline_path is None:
            continue
        assert projection.outline_path not in projection.active_document_candidates


# ---------------------------------------------------------------------------
# G-1 (PR #63 re-verification, 2026-08-02): THE OUTLINE-ONLY TURN, joined from
# the real derivation to the real guard.
#
# 16 of 21 real staged topics have exactly ONE editable path — the topic's own
# primary fragment, which doxBench loads as the OUTLINE and which F2 therefore
# does not offer as a DOCUMENT. Those tiles have no document to name, so the
# turn declares `active_document_path: null` (legal from contract-v1.28,
# mirroring the already-nullable `buffer_state.path`). Everything below the
# wire must treat that as "no active document", never as a refusal.
# ---------------------------------------------------------------------------

def test_an_outline_only_turn_passes_the_real_guard_on_the_real_derivation(tmp_path):
    """derivation → guard, over the fixture case that IS the G-1 shape."""
    cases = _fixture_cases()
    case = next(c for c in cases["cases"] if c["name"] == "single-document-staged")
    key = ScopeKey(repository=case["repository"], ref=case["ref"],
                   tile_kind=case["tile_kind"], tile_id=case["tile_id"])
    projection = resolve_scope(cases["snapshot"], key, source_root=tmp_path,
                               created_paths=case["created_paths"])
    assert projection.active_document_candidates == ()
    assert projection.outline_path is not None
    # the turn a tile like this can actually send: no active document, and the
    # outline the projection published
    revalidate_scope(
        projection=projection,
        request_scope=key,
        active_document_path=None,
        outline_path=projection.outline_path,
        document_path=None,
    )


def test_an_outline_only_turn_assembles_a_full_prompt_envelope():
    """guard → envelope: a null active document binds a null-path document
    buffer (the same not-yet-created shape `buffer_state.path` already
    carries), and both buffers still reach the prompt COMPLETE (FR-013)."""
    projection = _valid_projection()
    buffers = _valid_buffers()
    buffers[1] = _buffer("document", path=None, content="drafting here\n")
    envelope = _build_envelope(
        projection=projection, active_document_path=None, buffers=buffers)
    text = "\n".join(section.text for section in envelope.sections)
    assert "drafting here" in text
    assert OUTLINE_CONTENT in text


def test_a_document_proposal_is_refused_on_a_turn_that_names_no_document():
    """The narrowest reading of a silent contract, recorded: an outline-only
    turn is chat grounded on the tile's context with NO document-targeted
    proposal. `specs/010-doxbench-editor-chat/contracts/chat-turn.md` and
    FR-026/FR-027 say only that a response MAY carry independently typed
    outline and document proposals with unique targets; neither says what a
    document proposal MEANS when the turn names no document. It would be a
    rewrite of a document that does not exist, so it fails closed here as a
    RESPONSE defect (the request was fine) rather than becoming an Apply the
    buffer layer would have to refuse later."""
    observed = doxbench_turns.ObservedHashes(
        outline=content_identity(OUTLINE_CONTENT),
        document=content_identity(DOCUMENT_CONTENT),
    )
    document_proposal = {
        "assistant_prose": "here", "proposals": [{
            "target": "document",
            "base_hash": content_identity(DOCUMENT_CONTENT).hex,
            "summary": "rewrite the document", "content": "# new\n"}]}
    with pytest.raises(doxbench_turns.TurnResponseError):
        doxbench_turns.validate_assistant_response(
            document_proposal, observed=observed, permitted_targets=("outline",))
    # the same response is accepted when the turn DID name a document
    accepted = doxbench_turns.validate_assistant_response(
        document_proposal, observed=observed)
    assert [p.target for p in accepted.proposals] == ["document"]


def test_an_outline_proposal_is_still_offered_on_an_outline_only_turn():
    observed = doxbench_turns.ObservedHashes(
        outline=content_identity(OUTLINE_CONTENT),
        document=content_identity(DOCUMENT_CONTENT),
    )
    validated = doxbench_turns.validate_assistant_response(
        {"assistant_prose": "here", "proposals": [{
            "target": "outline",
            "base_hash": content_identity(OUTLINE_CONTENT).hex,
            "summary": "tighten the outline", "content": "# tighter\n"}]},
        observed=observed, permitted_targets=("outline",))
    assert [p.target for p in validated.proposals] == ["outline"]


def test_null_not_yet_created_document_path_is_permitted():
    # data-model.md Section 4: a document path that is None (buffer not yet
    # created on disk) is not subject to editable-path membership and must
    # not be refused on that ground.
    projection = _valid_projection()
    revalidate_scope(
        projection=projection,
        request_scope=_key(),
        active_document_path=None,
        outline_path=OUTLINE_PATH,
        document_path=None,
    )


def test_scope_refusal_happens_before_identity_verification_is_ever_reached():
    # Both a scope violation AND a content-hash mismatch are present at once.
    # If TurnScopeError wins, scope revalidation ran first -- proving refusal
    # happens before any prompt text is assembled (contracts/chat-turn.md
    # pre-dispatch ordering, FR-015).
    bad_projection = _projection(_key(), context_paths=(OUTLINE_PATH,), outline_path=OUTLINE_PATH)
    buffers = _valid_buffers()
    buffers[1] = _buffer(
        "document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT, content_hash="e" * 64
    )
    with pytest.raises(TurnScopeError):
        _build_envelope(projection=bad_projection, buffers=buffers)


def test_scope_refusal_produces_no_partial_envelope():
    bad_projection = _projection(_key(), context_paths=(OUTLINE_PATH,), outline_path=OUTLINE_PATH)
    try:
        _build_envelope(projection=bad_projection)
    except TurnScopeError:
        pass
    else:
        pytest.fail("expected TurnScopeError")


# --- FR-015 buffer binding: the disclosed buffer must be bound to what was
# --- independently validated, never merely a self-consistent object --------

# build_prompt_envelope revalidates projection.outline_path and
# active_document_path (both caller-supplied arguments), then requires
# (``_require_buffer_binding``) that each buffer's own path/repository/
# base_ref equal exactly what was validated, before any identity check or
# section text is assembled. Regression: an earlier draft disclosed
# TurnBuffer.path/.content without ever checking this binding to the
# projection and request scope (FR-015), so a self-consistent buffer (its
# own hash matches its own content) claiming a wholly out-of-scope path, a
# foreign repository, or a foreign ref was disclosed unchecked; these tests
# pin the required refusal. Each test plants a unique sentinel as the
# buffer's content and asserts both that no envelope was produced and that
# the sentinel never appears in the refusal.


def test_outline_buffer_path_must_equal_the_validated_outline_path():
    sentinel = "SENTINEL-OUTLINE-BUFFER-PATH-BYPASS"
    buffers = _valid_buffers()
    buffers[0] = _buffer("outline", path="../../etc/passwd", content=sentinel)
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(_build_envelope(buffers=buffers))
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_document_buffer_path_must_equal_the_validated_active_document_path():
    sentinel = "SENTINEL-DOCUMENT-BUFFER-PATH-BYPASS"
    out_of_scope_path = "ideation/staging/demo-topic/out-of-scope-buffer-target.md"
    buffers = _valid_buffers()
    buffers[1] = _buffer("document", path=out_of_scope_path, content=sentinel)
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(
            _build_envelope(buffers=buffers, active_document_path=DOCUMENT_PATH)
        )
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_buffer_repository_must_equal_the_request_scope_repository():
    sentinel = "SENTINEL-DOCUMENT-BUFFER-REPOSITORY-BYPASS"
    buffers = _valid_buffers()
    buffers[1] = _buffer(
        "document", path=DOCUMENT_PATH, content=sentinel, repository="other-repo"
    )
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(_build_envelope(buffers=buffers))
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_buffer_base_ref_must_equal_the_request_scope_ref():
    sentinel = "SENTINEL-DOCUMENT-BUFFER-BASE-REF-BYPASS"
    buffers = _valid_buffers()
    buffers[1] = _buffer(
        "document", path=DOCUMENT_PATH, content=sentinel, base_ref="refs/heads/attacker"
    )
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(_build_envelope(buffers=buffers))
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_outline_buffer_repository_must_equal_the_request_scope_repository():
    # Item A requires all four mismatch cases for the outline buffer too,
    # "at minimum repository and path" -- path is covered above, this covers
    # repository.
    sentinel = "SENTINEL-OUTLINE-BUFFER-REPOSITORY-BYPASS"
    buffers = _valid_buffers()
    buffers[0] = _buffer(
        "outline", path=OUTLINE_PATH, content=sentinel, repository="other-repo"
    )
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(_build_envelope(buffers=buffers))
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_outline_buffer_base_ref_must_equal_the_request_scope_ref():
    # Cheap to add alongside the repository case above, covering the outline
    # buffer's base_ref mismatch as well.
    sentinel = "SENTINEL-OUTLINE-BUFFER-BASE-REF-BYPASS"
    buffers = _valid_buffers()
    buffers[0] = _buffer(
        "outline", path=OUTLINE_PATH, content=sentinel, base_ref="refs/heads/attacker"
    )
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(_build_envelope(buffers=buffers))
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_buffer_binding_refusal_precedes_identity_verification_and_prompt_assembly():
    # Combine an out-of-scope buffer path with a deliberately wrong
    # content_hash. TurnScopeError must win over TurnIdentityMismatchError,
    # proving the buffer-binding check runs before identity verification and
    # before any section text exists.
    sentinel = "SENTINEL-BUFFER-BINDING-PRECEDES-IDENTITY"
    out_of_scope_path = "ideation/staging/demo-topic/out-of-scope-buffer-target.md"
    buffers = _valid_buffers()
    buffers[1] = _buffer(
        "document",
        path=out_of_scope_path,
        content=sentinel,
        content_hash="e" * 64,
    )
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(
            _build_envelope(buffers=buffers, active_document_path=DOCUMENT_PATH)
        )
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


# --- R-12: a buffer based on the session's OWN base is correctly based ------
#
# The binding check used to compare ref NAMES by string equality, which
# conflates "same ref name" with "same base bytes": a session branch is
# created FROM the pre-session ref, so a buffer based on `main` at the moment
# of branching IS based on the session's base, and refusing it made every
# un-landed buffer permanently unable to ground a turn after a partial Save
# (T104 R-12). The reviewer's binding ruling (2026-08-02): accept the pairing
# when the buffer names the ref the session branched from AND its base
# revision equals the session's recorded base revision -- acceptance on the
# REVISION, never the name alone -- and continue to refuse once the session
# has DIVERGED past that base for the buffer's own document. `base_ref`
# keeps its meaning (provenance) and is never rewritten.


def _session_base(*, ref: str = "main", revision: str = "base-rev-1",
                  documents: dict | None = None,
                  alias_revisions: tuple = ()) -> doxbench_turns.SessionBase:
    """A SessionBase whose reader serves the session's CURRENT text for a
    path out of a plain dict -- the same duck the route builds from the
    session worktree, with no filesystem involved."""
    held = dict(documents or {})
    return doxbench_turns.SessionBase(
        ref=ref, revision=revision, text_of=lambda path: held.get(path),
        alias_revisions=tuple(alias_revisions))


def _pre_session_buffers(*, document_content: str = DOCUMENT_CONTENT,
                         base_revision: str = "base-rev-1",
                         base_ref: str = "main"):
    """The post-partial-Save shape: the outline LANDED (its base was adopted
    onto the session ref), the document did not -- it still declares the
    pre-session base, exactly as `rekeyDoxBenchState` deliberately leaves it."""
    return [
        _buffer("outline", path=OUTLINE_PATH, content=OUTLINE_CONTENT),
        _buffer("document", path=DOCUMENT_PATH, content=document_content,
                base_ref=base_ref, base_revision=base_revision),
    ]


def test_an_unsaved_buffer_based_on_the_sessions_own_base_grounds_a_turn():
    # The acceptance case the ruling requires: name = the ref the session
    # branched from, revision = the session's recorded base revision, and the
    # session has not moved this document past that base (its current text
    # still hashes to the buffer's declared base).
    envelope = _build_envelope(
        buffers=_pre_session_buffers(),
        session_base=_session_base(documents={DOCUMENT_PATH: DOCUMENT_CONTENT}),
    )
    assert envelope.sections[6].text.endswith(DOCUMENT_CONTENT)


def test_a_pre_session_buffer_is_refused_once_the_session_diverged_past_its_base():
    # The divergence case the ruling names: a landed gate action moved this
    # document on the session branch, so a buffer still claiming the
    # pre-session base may genuinely be stale -- the refusal is correct and
    # staleness detection is made precise, not weakened.
    sentinel = "SENTINEL-DIVERGED-SESSION-BASE"
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(_build_envelope(
            buffers=_pre_session_buffers(document_content=sentinel),
            session_base=_session_base(
                documents={DOCUMENT_PATH: "# Note\n\nRewritten in-session.\n"}),
        ))
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_a_buffer_declaring_the_serving_snapshots_revision_grounds_too():
    # W-4 (wave re-review): the CLIENT never receives a per-file revision --
    # its `base_revision` is the projection's `source_revision`, the checkout
    # HEAD at snapshot GENERATION time, while the session records the
    # merge-base at OPEN time. Any main movement between snapshot bake and
    # session open made those differ forever, silently reverting R-12 to the
    # refusal it closed. The OPEN now records the serving snapshot's revision
    # beside the merge-base as an accepted ALIAS; acceptance still demands
    # the name AND a listed revision AND the base bytes.
    envelope = _build_envelope(
        buffers=_pre_session_buffers(base_revision="snapshot-rev-at-open"),
        session_base=_session_base(
            documents={DOCUMENT_PATH: DOCUMENT_CONTENT},
            alias_revisions=("snapshot-rev-at-open",)),
    )
    assert envelope.sections[6].text.endswith(DOCUMENT_CONTENT)

    # an alias never relaxes the byte clause ...
    with pytest.raises(TurnScopeError):
        _build_envelope(
            buffers=_pre_session_buffers(
                document_content="SENTINEL-ALIAS-DIVERGED",
                base_revision="snapshot-rev-at-open"),
            session_base=_session_base(
                documents={DOCUMENT_PATH: "# moved in-session\n"},
                alias_revisions=("snapshot-rev-at-open",)),
        )
    # ... and an unlisted revision still refuses
    with pytest.raises(TurnScopeError):
        _build_envelope(
            buffers=_pre_session_buffers(base_revision="never-recorded"),
            session_base=_session_base(
                documents={DOCUMENT_PATH: DOCUMENT_CONTENT},
                alias_revisions=("snapshot-rev-at-open",)),
        )


def test_a_matching_ref_name_alone_never_grounds_a_pre_session_buffer():
    # Acceptance is on the REVISION: a buffer naming the branched-from ref at
    # some OTHER revision is exactly the conflation the ruling removes.
    envelopes_returned = []
    with pytest.raises(TurnScopeError):
        envelopes_returned.append(_build_envelope(
            buffers=_pre_session_buffers(base_revision="some-other-revision"),
            session_base=_session_base(documents={DOCUMENT_PATH: DOCUMENT_CONTENT}),
        ))
    assert envelopes_returned == []


def test_a_buffer_naming_a_ref_other_than_the_sessions_base_is_still_refused():
    envelopes_returned = []
    with pytest.raises(TurnScopeError):
        envelopes_returned.append(_build_envelope(
            buffers=_pre_session_buffers(base_ref="refs/heads/elsewhere"),
            session_base=_session_base(documents={DOCUMENT_PATH: DOCUMENT_CONTENT}),
        ))
    assert envelopes_returned == []


def test_without_a_recorded_session_base_the_binding_check_is_unchanged():
    # Degradation pin: a session whose base was never recorded (opened before
    # this wave, or a marker that could not be written) refuses the
    # pre-session pairing exactly as before -- honest, and never a crash.
    envelopes_returned = []
    with pytest.raises(TurnScopeError):
        envelopes_returned.append(_build_envelope(
            buffers=_pre_session_buffers(), session_base=None))
    assert envelopes_returned == []


def test_a_session_base_never_relaxes_the_path_or_repository_binding():
    # The session-base acceptance widens ONE comparison (the ref pairing);
    # the path and repository halves of FR-015 are untouched by it.
    sentinel = "SENTINEL-SESSION-BASE-PATH-BYPASS"
    buffers = _pre_session_buffers()
    buffers[1] = _buffer(
        "document", path="ideation/staging/demo-topic/other.md",
        content=sentinel, base_ref="main", base_revision="base-rev-1")
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(_build_envelope(
            buffers=buffers,
            session_base=_session_base(documents={
                "ideation/staging/demo-topic/other.md": sentinel}),
        ))
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)


def test_a_document_the_session_never_held_grounds_only_an_empty_base():
    # A path ABSENT from the session worktree has empty base bytes: a fresh
    # not-yet-written buffer (base identity of "") is accepted, and a buffer
    # claiming loaded bytes for a file the session does not hold is refused.
    fresh = _buffer("document", path=DOCUMENT_PATH, content="typed later",
                    base_hash=content_identity("").hex,
                    base_ref="main", base_revision="base-rev-1", dirty=True)
    buffers = [_buffer("outline", path=OUTLINE_PATH, content=OUTLINE_CONTENT), fresh]
    envelope = _build_envelope(buffers=buffers, session_base=_session_base())
    assert envelope.sections[6].text.endswith("typed later")

    claiming = _buffer("document", path=DOCUMENT_PATH, content=DOCUMENT_CONTENT,
                       base_ref="main", base_revision="base-rev-1")
    with pytest.raises(TurnScopeError):
        _build_envelope(buffers=[buffers[0], claiming],
                        session_base=_session_base())


# --- null-path buffer disclosure (data-model.md Section 4: `path` is "Null
# --- only for a not-yet-created buffer"; Section 2 permits `outline_path` to
# --- be null too) ------------------------------------------------------------
#
# Regression: `revalidate_scope` already exempted a `None` expected path
# from the in-scope/editable check, but an earlier draft of the
# section-assembly path did not render a `None` buffer path -- `_buffer_section`
# built its header with `"Path: " + buffer.path + ...`, which raised an
# unhandled, un-redacted `TypeError` the moment a disclosed buffer's `path`
# was `None`. These tests pin the required behavior: a null buffer path
# renders a fixed `"Path: (not yet created)"` placeholder instead of
# crashing, and a mismatch between the validated expected path and the
# buffer's own path (null vs. backed, either direction) still refuses via
# the existing equality-based buffer-binding check (`_require_buffer_binding`).


def test_document_buffer_with_a_null_path_is_disclosed_with_a_not_yet_created_header():
    buffers = _valid_buffers()
    buffers[1] = _buffer("document", path=None, content=DOCUMENT_CONTENT)
    envelope = _build_envelope(active_document_path=None, buffers=buffers)
    document_section = envelope.sections[6]
    assert document_section.key == "document_buffer"
    assert "Path: (not yet created)" in document_section.text
    assert DOCUMENT_CONTENT in document_section.text


def test_outline_buffer_with_a_null_path_is_disclosed_with_a_not_yet_created_header():
    projection = _projection(
        _key(),
        context_paths=(DOCUMENT_PATH,),
        editable_paths=(DOCUMENT_PATH,),
        outline_path=None,
    )
    buffers = _valid_buffers()
    buffers[0] = _buffer("outline", path=None, content=OUTLINE_CONTENT)
    envelope = _build_envelope(
        projection=projection, active_document_path=DOCUMENT_PATH, buffers=buffers
    )
    outline_section = envelope.sections[5]
    assert outline_section.key == "outline_buffer"
    assert "Path: (not yet created)" in outline_section.text
    assert OUTLINE_CONTENT in outline_section.text


def test_null_expected_path_with_a_backed_buffer_path_refuses():
    # active_document_path is None (no document buffer created yet) but the
    # document buffer itself smuggles in a real, out-of-scope path. The
    # existing equality-based buffer-binding check already refuses this:
    # `buffer.path != expected_path` is `"../../etc/passwd" != None`.
    sentinel = "SENTINEL-NULL-EXPECTED-BACKED-BUFFER-BYPASS"
    buffers = _valid_buffers()
    buffers[1] = _buffer("document", path="../../etc/passwd", content=sentinel)
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(
            _build_envelope(active_document_path=None, buffers=buffers)
        )
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_backed_expected_path_with_a_null_buffer_path_refuses():
    # active_document_path is a real, backed path but the document buffer
    # itself declares path=None. The same equality-based buffer-binding
    # check refuses this direction too: the backed path != None.
    sentinel = "SENTINEL-BACKED-EXPECTED-NULL-BUFFER-BYPASS"
    buffers = _valid_buffers()
    buffers[1] = _buffer("document", path=None, content=sentinel)
    envelopes_returned = []
    with pytest.raises(TurnScopeError) as raised:
        envelopes_returned.append(
            _build_envelope(active_document_path=DOCUMENT_PATH, buffers=buffers)
        )
    assert envelopes_returned == []
    assert sentinel not in str(raised.value)
    assert sentinel not in repr(raised.value)


def test_null_path_envelope_assembly_stays_byte_for_byte_deterministic():
    def _null_document_buffers():
        buffers = _valid_buffers()
        buffers[1] = _buffer("document", path=None, content=DOCUMENT_CONTENT)
        return buffers

    first = _build_envelope(active_document_path=None, buffers=_null_document_buffers())
    second = _build_envelope(active_document_path=None, buffers=_null_document_buffers())
    assert [(s.key, s.text) for s in first.sections] == [(s.key, s.text) for s in second.sections]
    assert first.rendered().encode("utf-8") == second.rendered().encode("utf-8")


# --- FR-016 fresh buffer state per turn -------------------------------------


def test_second_turn_after_an_intervening_edit_uses_the_new_content_never_a_cached_hash():
    first_envelope = _build_envelope(buffers=_valid_buffers(document_content=DOCUMENT_CONTENT))
    edited_content = DOCUMENT_CONTENT + "An added paragraph after editing.\n"
    second_envelope = _build_envelope(
        buffers=_valid_buffers(document_content=edited_content),
    )
    assert first_envelope.observed_hashes.document.hex == content_identity(DOCUMENT_CONTENT).hex
    assert second_envelope.observed_hashes.document.hex == content_identity(edited_content).hex
    assert first_envelope.observed_hashes.document.hex != second_envelope.observed_hashes.document.hex
    assert edited_content in second_envelope.sections[6].text
    assert DOCUMENT_CONTENT not in edited_content or edited_content in second_envelope.sections[6].text


# ===========================================================================
# T041 -- content, transcript, message, output, and route-body boundaries
# ===========================================================================


def test_working_subject_accepts_exactly_the_byte_maximum():
    text = "s" * MAX_WORKING_SUBJECT_BYTES
    assert utf8_size(text) == MAX_WORKING_SUBJECT_BYTES
    validate_working_subject(text)


def test_working_subject_refuses_one_byte_over_the_maximum():
    text = "s" * (MAX_WORKING_SUBJECT_BYTES + 1)
    with pytest.raises(TurnLimitError) as raised:
        validate_working_subject(text)
    assert raised.value.dimension == "working_subject_bytes"
    assert raised.value.measured == MAX_WORKING_SUBJECT_BYTES + 1
    assert raised.value.maximum == MAX_WORKING_SUBJECT_BYTES


def test_working_subject_multibyte_case_is_under_codepoints_but_over_bytes():
    # 300 code points, each 2 UTF-8 bytes -> 600 bytes > 512-byte maximum,
    # while 300 < 512 in raw code-point count -- proving bytes, not
    # characters, are measured.
    text = "é" * 300
    assert len(text) < MAX_WORKING_SUBJECT_BYTES
    assert utf8_size(text) > MAX_WORKING_SUBJECT_BYTES
    with pytest.raises(TurnLimitError):
        validate_working_subject(text)


def test_message_accepts_exactly_the_byte_maximum():
    text = "m" * MAX_MESSAGE_BYTES
    validate_message(text)


def test_message_refuses_one_byte_over_the_maximum():
    text = "m" * (MAX_MESSAGE_BYTES + 1)
    with pytest.raises(TurnLimitError) as raised:
        validate_message(text)
    assert raised.value.dimension == "message_bytes"
    assert raised.value.measured == MAX_MESSAGE_BYTES + 1
    assert raised.value.maximum == MAX_MESSAGE_BYTES


@pytest.mark.parametrize("blank", ["", "   ", "\t\n", "  "])
def test_message_refuses_blank_or_whitespace_only(blank):
    with pytest.raises(TurnBlankMessageError):
        validate_message(blank)


def test_message_multibyte_case_is_under_codepoints_but_over_bytes():
    text = "é" * 8500  # 8500 code points, 17000 bytes > 16384
    assert len(text) < MAX_MESSAGE_BYTES
    assert utf8_size(text) > MAX_MESSAGE_BYTES
    with pytest.raises(TurnLimitError):
        validate_message(text)


def test_transcript_accepts_exactly_twenty_turns_within_the_byte_budget():
    turns = tuple(TranscriptTurn(role="human", text="hi") for _ in range(MAX_TRANSCRIPT_TURNS))
    validate_transcript(turns)


def test_transcript_refuses_twenty_one_turns_even_when_tiny():
    turns = tuple(
        TranscriptTurn(role="human", text="hi") for _ in range(MAX_TRANSCRIPT_TURNS + 1)
    )
    with pytest.raises(TurnLimitError) as raised:
        validate_transcript(turns)
    assert raised.value.dimension == "transcript_turns"
    assert raised.value.measured == MAX_TRANSCRIPT_TURNS + 1
    assert raised.value.maximum == MAX_TRANSCRIPT_TURNS


def test_transcript_accepts_exactly_the_byte_maximum():
    turn = TranscriptTurn(role="human", text="t" * MAX_TRANSCRIPT_BYTES)
    validate_transcript((turn,))


def test_transcript_refuses_one_byte_over_the_maximum_independent_of_turn_count():
    turn = TranscriptTurn(role="human", text="t" * (MAX_TRANSCRIPT_BYTES + 1))
    with pytest.raises(TurnLimitError) as raised:
        validate_transcript((turn,))
    assert raised.value.dimension == "transcript_bytes"
    assert raised.value.measured == MAX_TRANSCRIPT_BYTES + 1
    assert raised.value.maximum == MAX_TRANSCRIPT_BYTES


def test_transcript_bytes_helper_sums_only_text_and_matches_utf8_size():
    turns = (TranscriptTurn(role="human", text="abc"), TranscriptTurn(role="assistant", text="de"))
    assert transcript_bytes(turns) == utf8_size("abc") + utf8_size("de")


def test_each_buffer_reuses_the_doxbench_hash_authority_boundary():
    at_max = "a" * HASH_MAX_BUFFER_BYTES
    buffer = _buffer("document", path=DOCUMENT_PATH, content=at_max)
    identity = verify_buffer_identity(buffer)
    assert identity.hex == content_identity(at_max).hex


def test_buffer_one_byte_over_the_maximum_refuses_with_the_contract_example_shape():
    sentinel = "SENTINEL-OVERSIZE-DOCUMENT-CONTENT"
    over = sentinel + "a" * (HASH_MAX_BUFFER_BYTES + 1 - utf8_size(sentinel))
    assert utf8_size(over) == HASH_MAX_BUFFER_BYTES + 1
    real_hex = "0" * 64  # any claim; size failure happens before hash comparison
    buffer = TurnBuffer(
        kind="document",
        repository=REPOSITORY,
        path=DOCUMENT_PATH,
        base_ref=REF,
        base_revision="abc123",
        base_hash=real_hex,
        content_hash=real_hex,
        content=over,
        dirty=True,
    )
    with pytest.raises(TurnLimitError) as raised:
        verify_buffer_identity(buffer)
    assert raised.value.dimension == "document_buffer_bytes"
    assert raised.value.measured == HASH_MAX_BUFFER_BYTES + 1
    assert raised.value.maximum == HASH_MAX_BUFFER_BYTES
    assert sentinel not in str(raised.value)


def test_outline_buffer_oversize_dimension_is_named_for_outline_not_document():
    over = "a" * (HASH_MAX_BUFFER_BYTES + 1)
    buffer = TurnBuffer(
        kind="outline",
        repository=REPOSITORY,
        path=OUTLINE_PATH,
        base_ref=REF,
        base_revision="abc123",
        base_hash="0" * 64,
        content_hash="0" * 64,
        content=over,
        dirty=True,
    )
    with pytest.raises(TurnLimitError) as raised:
        verify_buffer_identity(buffer)
    assert raised.value.dimension == "outline_buffer_bytes"


def test_route_body_arithmetic_accepts_every_field_simultaneously_at_its_own_maximum():
    # Even with every individual field at its own declared maximum, the sum
    # stays comfortably under the route-specific total -- proving the
    # aggregate check never falsely refuses a legitimate max-sized request.
    validate_request_body_bytes(
        outline_bytes=HASH_MAX_BUFFER_BYTES,
        document_bytes=HASH_MAX_BUFFER_BYTES,
        message_bytes=MAX_MESSAGE_BYTES,
        working_subject_bytes=MAX_WORKING_SUBJECT_BYTES,
        transcript_bytes=MAX_TRANSCRIPT_BYTES,
    )


def test_route_body_arithmetic_accepts_the_exact_total_maximum():
    validate_request_body_bytes(
        outline_bytes=MAX_REQUEST_BODY_BYTES,
        document_bytes=0,
        message_bytes=0,
        working_subject_bytes=0,
        transcript_bytes=0,
    )


def test_route_body_arithmetic_refuses_one_byte_over_the_total_maximum():
    with pytest.raises(TurnLimitError) as raised:
        validate_request_body_bytes(
            outline_bytes=MAX_REQUEST_BODY_BYTES + 1,
            document_bytes=0,
            message_bytes=0,
            working_subject_bytes=0,
            transcript_bytes=0,
        )
    assert raised.value.dimension == "request_body_bytes"
    assert raised.value.measured == MAX_REQUEST_BODY_BYTES + 1
    assert raised.value.maximum == MAX_REQUEST_BODY_BYTES


def test_route_body_arithmetic_refuses_a_synthetic_combination_over_the_maximum():
    with pytest.raises(TurnLimitError) as raised:
        validate_request_body_bytes(
            outline_bytes=700_000,
            document_bytes=700_000,
            message_bytes=0,
            working_subject_bytes=0,
            transcript_bytes=0,
        )
    assert raised.value.measured == 1_400_000
    assert raised.value.maximum == MAX_REQUEST_BODY_BYTES


# --- output-side constants only (no decoding, no dispatch) ------------------


def test_output_side_constants_match_plan_md_exactly():
    assert MAX_ASSISTANT_PROSE_BYTES == 65_536
    assert MAX_PROPOSAL_BYTES == 400_000
    assert MAX_RESPONSE_TOTAL_BYTES == 900_000


def test_request_and_response_totals_are_pinned_to_the_model_authority_no_drift():
    assert MAX_REQUEST_BODY_BYTES == SERVER_MAX_INPUT_LIMIT_BYTES == 1_048_576
    assert MAX_RESPONSE_TOTAL_BYTES == SERVER_MAX_OUTPUT_LIMIT_BYTES == 900_000


def test_effective_output_limit_reuses_the_model_catalog_stricter_of_arithmetic():
    strict_entry = ModelCatalogEntry(
        model_id="strict",
        label="Strict",
        provider_class="on-tenant",
        available=True,
        input_limit_bytes=800_000,
        output_limit_bytes=400_000,
        data_handling="Processed in the approved tenant boundary",
    )
    loose_entry = ModelCatalogEntry(
        model_id="loose",
        label="Loose",
        provider_class="on-tenant",
        available=True,
        input_limit_bytes=800_000,
        output_limit_bytes=SERVER_MAX_OUTPUT_LIMIT_BYTES,
        data_handling="Processed in the approved tenant boundary",
    )
    assert (
        effective_limit_bytes(
            server_maximum=MAX_RESPONSE_TOTAL_BYTES,
            entry_limit=strict_entry.output_limit_bytes,
        )
        == 400_000
    )
    assert (
        effective_limit_bytes(
            server_maximum=MAX_RESPONSE_TOTAL_BYTES,
            entry_limit=loose_entry.output_limit_bytes,
        )
        == MAX_RESPONSE_TOTAL_BYTES
    )


# --- FR-017 refusal shape and no-content-leak sentinels ---------------------


def test_turn_limit_error_public_dict_matches_the_contract_fixed_failure_shape():
    error = TurnLimitError("document_buffer_bytes", 400_123, 400_000)
    assert error.dimension == "document_buffer_bytes"
    assert error.measured == 400_123
    assert error.maximum == 400_000
    assert error.as_public_dict() == {
        "dimension": "document_buffer_bytes",
        "measured": 400_123,
        "maximum": 400_000,
    }


@pytest.mark.parametrize(
    "validator, oversize_kwargs",
    [
        (validate_working_subject, {}),
        (validate_message, {}),
    ],
)
def test_refusals_never_leak_a_planted_sentinel_from_oversized_text(validator, oversize_kwargs):
    del oversize_kwargs
    sentinel = "SENTINEL-LEAK-CHECK-BOUNDARY"
    limit = MAX_WORKING_SUBJECT_BYTES if validator is validate_working_subject else MAX_MESSAGE_BYTES
    over = sentinel + "a" * (limit + 1 - utf8_size(sentinel))
    with pytest.raises(TurnLimitError) as raised:
        validator(over)
    assert sentinel not in str(raised.value)
    assert sentinel not in str(raised.value.as_public_dict())


def test_transcript_refusal_never_leaks_planted_transcript_text():
    sentinel = "SENTINEL-LEAK-CHECK-TRANSCRIPT"
    turn = TranscriptTurn(role="human", text=sentinel + "a" * (MAX_TRANSCRIPT_BYTES + 1))
    with pytest.raises(TurnLimitError) as raised:
        validate_transcript((turn,))
    assert sentinel not in str(raised.value)
    assert sentinel not in str(raised.value.as_public_dict())


def test_turn_error_hierarchy_all_derive_from_turn_error_and_value_error():
    for cls in (
        TurnLimitError,
        TurnBlankMessageError,
        TurnBufferKindError,
        TurnIdentityMismatchError,
        TurnScopeError,
        TurnConflictError,
        doxbench_turns.TurnInFlightError,
    ):
        assert issubclass(cls, TurnError)
        assert issubclass(cls, ValueError)
    # FR-018's in-flight refusal is a TurnConflictError specialization so any
    # existing caller catching TurnConflictError still catches it.
    assert issubclass(doxbench_turns.TurnInFlightError, TurnConflictError)


# ===========================================================================
# T042 -- bounded idempotency / one-in-flight store (the T048 store)
# ===========================================================================


def _fresh_key(tile_id: str) -> ScopeKey:
    return ScopeKey(repository=REPOSITORY, ref=REF, tile_kind="staged", tile_id=tile_id)


def test_turn_record_shape_holds_no_content_only_a_digest_and_a_bounded_result():
    field_names = {f.name for f in dataclasses.fields(TurnRecord)}
    assert field_names == {
        "conversation_key",
        "client_turn_id",
        "request_digest",
        "state",
        "validated_result",
        "size_bytes",
        "last_access_order",
    }
    for forbidden in ("content", "buffer", "message", "prompt", "transcript"):
        assert forbidden not in field_names


def test_reserve_on_an_empty_store_creates_an_in_flight_entry_and_asks_to_dispatch():
    store = TurnStore()
    key = _fresh_key("t1")
    digest = sha256_hex("request-a")
    lease = store.reserve(key, "turn-1", digest)
    assert isinstance(lease, TurnLease)
    assert lease.should_dispatch is True
    assert lease.state == TURN_STATE_IN_FLIGHT
    record = store.snapshot(key, "turn-1")
    assert record.state == TURN_STATE_IN_FLIGHT
    assert record.request_digest == digest
    assert record.validated_result is None


def test_completed_identical_digest_replays_the_same_result_with_no_second_dispatch():
    store = TurnStore()
    key = _fresh_key("t2")
    digest = sha256_hex("request-b")
    dispatch_count = 0

    first_lease = store.reserve(key, "turn-1", digest)
    assert first_lease.should_dispatch is True
    dispatch_count += 1
    result = {"assistant_turn_id": "a-1", "marker": "RESULT-B"}
    store.complete(key, "turn-1", result, size_bytes=64)

    second_lease = store.reserve(key, "turn-1", digest)
    assert second_lease.should_dispatch is False
    assert second_lease.state == TURN_STATE_COMPLETED
    assert second_lease.result == result

    assert dispatch_count == 1


def test_failed_identical_digest_replays_the_same_failure_with_no_second_dispatch():
    store = TurnStore()
    key = _fresh_key("t3")
    digest = sha256_hex("request-c")

    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True
    failure = {"error": "request_limit_exceeded"}
    store.fail(key, "turn-1", failure, size_bytes=16)

    replay = store.reserve(key, "turn-1", digest)
    assert replay.should_dispatch is False
    assert replay.state == TURN_STATE_FAILED
    assert replay.result == failure


def test_different_digest_same_key_and_id_refuses_as_a_conflict_no_dispatch():
    store = TurnStore()
    key = _fresh_key("t4")
    first_digest = sha256_hex("request-d1")
    second_digest = sha256_hex("request-d2")

    lease = store.reserve(key, "turn-1", first_digest)
    assert lease.should_dispatch is True
    store.complete(key, "turn-1", {"assistant_turn_id": "a"}, size_bytes=8)

    with pytest.raises(TurnConflictError):
        store.reserve(key, "turn-1", second_digest)

    # the original completed entry is untouched by the refused conflict
    record = store.snapshot(key, "turn-1")
    assert record.request_digest == first_digest
    assert record.state == TURN_STATE_COMPLETED


def test_different_digest_against_an_in_flight_entry_also_refuses_immediately_without_blocking():
    store = TurnStore()
    key = _fresh_key("t5")
    first_digest = sha256_hex("request-e1")
    second_digest = sha256_hex("request-e2")

    lease = store.reserve(key, "turn-1", first_digest)
    assert lease.should_dispatch is True

    with pytest.raises(TurnConflictError):
        store.reserve(key, "turn-1", second_digest)

    record = store.snapshot(key, "turn-1")
    assert record.state == TURN_STATE_IN_FLIGHT
    assert record.request_digest == first_digest


def test_snapshot_of_an_unknown_key_or_id_is_none():
    store = TurnStore()
    assert store.snapshot(_fresh_key("nope"), "turn-1") is None


# --- real threading concurrency: single dispatch, attach/wait ---------------


def test_concurrent_reserve_on_the_same_key_dispatches_exactly_once_and_others_attach():
    store = TurnStore()
    key = _fresh_key("concurrent-same-key")
    digest = sha256_hex("shared-request")
    thread_count = 6

    barrier = threading.Barrier(thread_count)
    dispatch_registered = threading.Event()
    winner_may_complete = threading.Event()
    lock = threading.Lock()
    dispatch_count = 0
    returned = []
    shared_result = {"assistant_turn_id": "shared", "marker": "SHARED-RESULT"}

    def worker():
        nonlocal dispatch_count
        barrier.wait()
        lease = store.reserve(key, "turn-x", digest)
        if lease.should_dispatch:
            with lock:
                dispatch_count += 1
            dispatch_registered.set()
            winner_may_complete.wait(timeout=5)
            store.complete(key, "turn-x", shared_result, size_bytes=32)
        with lock:
            returned.append(lease)

    threads = [threading.Thread(target=worker) for _ in range(thread_count)]
    for thread in threads:
        thread.start()

    assert dispatch_registered.wait(timeout=5)
    # The winner has registered its dispatch but is deliberately blocked
    # before calling complete() -- so nobody (winner included) has appended
    # to `returned` yet. This is a structural guarantee, not a timing guess.
    with lock:
        assert returned == []

    winner_may_complete.set()
    for thread in threads:
        thread.join(timeout=5)
        assert not thread.is_alive()

    assert dispatch_count == 1
    assert len(returned) == thread_count
    for lease in returned:
        if not lease.should_dispatch:
            assert lease.state == TURN_STATE_COMPLETED
            assert lease.result == shared_result

    record = store.snapshot(key, "turn-x")
    assert record.state == TURN_STATE_COMPLETED
    assert record.validated_result == shared_result


def test_different_conversation_keys_proceed_concurrently_no_global_serialization():
    store = TurnStore()
    key_one = _fresh_key("independent-1")
    key_two = _fresh_key("independent-2")
    digest = sha256_hex("independent-request")

    holding = threading.Event()
    release = threading.Event()

    def slow_holder():
        lease = store.reserve(key_one, "turn-1", digest)
        assert lease.should_dispatch is True
        holding.set()
        # Simulate provider call time entirely OUTSIDE the store: no store
        # method is invoked here at all, proving no lock could be held.
        release.wait(timeout=5)
        store.complete(key_one, "turn-1", {"assistant_turn_id": "one"}, size_bytes=8)

    thread = threading.Thread(target=slow_holder)
    thread.start()
    assert holding.wait(timeout=5)

    # key_two's in-flight turn for key_one must not block a totally
    # independent key -- this must return immediately.
    other_lease = store.reserve(key_two, "turn-1", digest)
    assert other_lease.should_dispatch is True
    store.complete(key_two, "turn-1", {"assistant_turn_id": "two"}, size_bytes=8)

    release.set()
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_lock_is_not_held_across_the_simulated_provider_call():
    # Same mechanism as the key-independence test above, but the assertion is
    # framed around the specific research R8 requirement: the reservation
    # holder does its "call" without any reference to the store's lock, and a
    # second, unrelated reservation on a DIFFERENT key still proceeds while
    # the first caller's call is still "in progress".
    store = TurnStore()
    busy_key = _fresh_key("busy")
    idle_key = _fresh_key("idle")
    digest = sha256_hex("lock-not-held-request")
    call_in_progress = threading.Event()
    finish_call = threading.Event()
    progress_marks = []

    def busy_caller():
        lease = store.reserve(busy_key, "turn-1", digest)
        assert lease.should_dispatch is True
        call_in_progress.set()
        finish_call.wait(timeout=5)
        store.complete(busy_key, "turn-1", {"assistant_turn_id": "busy"}, size_bytes=8)

    thread = threading.Thread(target=busy_caller)
    thread.start()
    assert call_in_progress.wait(timeout=5)

    idle_lease = store.reserve(idle_key, "turn-1", digest)
    progress_marks.append("idle-reserved-while-busy-in-progress")
    assert idle_lease.should_dispatch is True
    store.complete(idle_key, "turn-1", {"assistant_turn_id": "idle"}, size_bytes=8)
    progress_marks.append("idle-completed-while-busy-in-progress")

    assert progress_marks == [
        "idle-reserved-while-busy-in-progress",
        "idle-completed-while-busy-in-progress",
    ]

    finish_call.set()
    thread.join(timeout=5)


def test_two_independent_store_instances_share_no_state():
    store_a = TurnStore()
    store_b = TurnStore()
    key = _fresh_key("shared-shape-different-store")
    digest = sha256_hex("cross-store-request")

    lease_a = store_a.reserve(key, "turn-1", digest)
    assert lease_a.should_dispatch is True

    # store_b has never seen this key/id: it must reserve fresh, independent
    # of store_a's unresolved in-flight entry for the identical key/id/digest.
    lease_b = store_b.reserve(key, "turn-1", digest)
    assert lease_b.should_dispatch is True

    store_a.complete(key, "turn-1", {"assistant_turn_id": "a"}, size_bytes=8)
    store_b.complete(key, "turn-1", {"assistant_turn_id": "b"}, size_bytes=8)

    assert store_a.snapshot(key, "turn-1").validated_result == {"assistant_turn_id": "a"}
    assert store_b.snapshot(key, "turn-1").validated_result == {"assistant_turn_id": "b"}


# --- bounded eviction --------------------------------------------------------


def test_completed_cache_is_bounded_to_64_entries_and_evicts_the_oldest():
    store = TurnStore()
    keys_and_ids = [(_fresh_key(f"evict-count-{i}"), f"turn-{i}") for i in range(MAX_IDEMPOTENCY_ENTRIES + 2)]
    for index, (key, turn_id) in enumerate(keys_and_ids):
        digest = sha256_hex(f"evict-count-request-{index}")
        lease = store.reserve(key, turn_id, digest)
        assert lease.should_dispatch is True
        store.complete(key, turn_id, {"marker": index}, size_bytes=1)

    first_key, first_id = keys_and_ids[0]
    second_key, second_id = keys_and_ids[1]
    last_key, last_id = keys_and_ids[-1]

    assert store.snapshot(first_key, first_id) is None
    assert store.snapshot(second_key, second_id) is None
    assert store.snapshot(last_key, last_id) is not None


def test_completed_cache_is_bounded_to_16_mebibytes_and_evicts_the_oldest():
    assert MAX_IDEMPOTENCY_BYTES == 16 * 1024 * 1024
    store = TurnStore()
    big = MAX_IDEMPOTENCY_BYTES // 3 + 1  # three entries exceed the byte bound
    keys_and_ids = [(_fresh_key(f"evict-bytes-{i}"), f"turn-{i}") for i in range(3)]
    for index, (key, turn_id) in enumerate(keys_and_ids):
        digest = sha256_hex(f"evict-bytes-request-{index}")
        lease = store.reserve(key, turn_id, digest)
        assert lease.should_dispatch is True
        store.complete(key, turn_id, {"marker": index}, size_bytes=big)

    first_key, first_id = keys_and_ids[0]
    last_key, last_id = keys_and_ids[-1]
    assert store.snapshot(first_key, first_id) is None
    assert store.snapshot(last_key, last_id) is not None


def test_touching_an_entry_updates_its_lru_order_and_protects_it_from_eviction():
    store = TurnStore()
    keys_and_ids = [(_fresh_key(f"lru-{i}"), f"turn-{i}") for i in range(MAX_IDEMPOTENCY_ENTRIES)]
    digests = {}
    for index, (key, turn_id) in enumerate(keys_and_ids):
        digest = sha256_hex(f"lru-request-{index}")
        digests[(key, turn_id)] = digest
        lease = store.reserve(key, turn_id, digest)
        assert lease.should_dispatch is True
        store.complete(key, turn_id, {"marker": index}, size_bytes=1)

    first_key, first_id = keys_and_ids[0]
    second_key, second_id = keys_and_ids[1]

    before = store.snapshot(first_key, first_id).last_access_order
    # Touch entry 0 by replaying its identical digest -- no dispatch, but it
    # must now look more-recently-used than entry 1.
    touch_lease = store.reserve(first_key, first_id, digests[(first_key, first_id)])
    assert touch_lease.should_dispatch is False
    after = store.snapshot(first_key, first_id).last_access_order
    assert after > before

    # One more completed entry pushes the store over its bound: the
    # least-recently-used surviving entry (now #1, since #0 was refreshed)
    # must be evicted, not #0.
    overflow_key = _fresh_key("lru-overflow")
    overflow_digest = sha256_hex("lru-overflow-request")
    overflow_lease = store.reserve(overflow_key, "turn-overflow", overflow_digest)
    assert overflow_lease.should_dispatch is True
    store.complete(overflow_key, "turn-overflow", {"marker": "overflow"}, size_bytes=1)

    assert store.snapshot(first_key, first_id) is not None
    assert store.snapshot(second_key, second_id) is None


def test_in_flight_entries_are_never_evicted_even_under_bound_pressure():
    store = TurnStore()
    in_flight_keys_and_ids = [
        (_fresh_key(f"never-evict-{i}"), f"turn-{i}") for i in range(MAX_IDEMPOTENCY_ENTRIES + 5)
    ]
    for index, (key, turn_id) in enumerate(in_flight_keys_and_ids):
        digest = sha256_hex(f"never-evict-request-{index}")
        lease = store.reserve(key, turn_id, digest)
        assert lease.should_dispatch is True
        # deliberately never completed: stays in_flight

    for key, turn_id in in_flight_keys_and_ids:
        record = store.snapshot(key, turn_id)
        assert record is not None
        assert record.state == TURN_STATE_IN_FLIGHT


def test_bounds_are_the_module_declared_constants():
    assert MAX_IDEMPOTENCY_ENTRIES == 64
    assert MAX_IDEMPOTENCY_BYTES == 16 * 1024 * 1024


# --- TurnStore finalization misuse paths (_finalize hardening) -------------
#
# _finalize validates every refusal condition (an unknown or already-
# resolved key, a negative size_bytes, or a size_bytes over the bound)
# BEFORE mutating any state, and stores a deep copy of the caller's result --
# never the caller's own object by reference. Regression: an earlier draft
# called `dataclasses.replace(previous, ...)` with `previous` possibly None,
# added size_bytes unconditionally with no upper bound, and stored the
# caller's result object by reference; these tests encode the adjudicated
# refusal/isolation semantics and pin the fix.


def test_finalizing_an_unknown_key_refuses_and_leaves_the_store_unchanged():
    store = TurnStore()
    key = _fresh_key("finalize-unknown")
    with pytest.raises(TurnConflictError):
        store.complete(key, "turn-x", {"marker": "should-not-apply"}, size_bytes=1)
    assert store.snapshot(key, "turn-x") is None


def test_double_finalization_refuses_and_never_double_counts_resolved_bytes():
    store = TurnStore()
    key = _fresh_key("finalize-double")
    digest = sha256_hex("double-finalize-request")
    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True
    first_result = {"assistant_turn_id": "first"}
    store.complete(key, "turn-1", first_result, size_bytes=1)

    with pytest.raises(TurnConflictError):
        store.complete(key, "turn-1", {"assistant_turn_id": "second"}, size_bytes=1)

    record = store.snapshot(key, "turn-1")
    assert record.validated_result == first_result
    assert record.size_bytes == 1

    # Behavioral proof the accounting only ever counted one contribution: add
    # exactly MAX_IDEMPOTENCY_ENTRIES - 1 more single-byte completed entries.
    # If the refused double-finalize had double-counted `key`'s bytes or
    # entry slot, this would already be over budget; instead the original
    # entry must still be the least-recently-used survivor.
    for index in range(MAX_IDEMPOTENCY_ENTRIES - 1):
        filler_key = _fresh_key(f"finalize-double-filler-{index}")
        filler_digest = sha256_hex(f"finalize-double-filler-request-{index}")
        filler_lease = store.reserve(filler_key, "turn-1", filler_digest)
        assert filler_lease.should_dispatch is True
        store.complete(filler_key, "turn-1", {"marker": index}, size_bytes=1)

    assert store.snapshot(key, "turn-1") is not None

    overflow_key = _fresh_key("finalize-double-overflow")
    overflow_digest = sha256_hex("finalize-double-overflow-request")
    overflow_lease = store.reserve(overflow_key, "turn-1", overflow_digest)
    assert overflow_lease.should_dispatch is True
    store.complete(overflow_key, "turn-1", {"marker": "overflow"}, size_bytes=1)

    # One more entry now pushes the count past the bound: the
    # least-recently-used entry -- the original `key`, never touched again
    # after its first completion -- must be the one evicted.
    assert store.snapshot(key, "turn-1") is None


def test_negative_size_bytes_at_finalization_refuses():
    store = TurnStore()
    key = _fresh_key("finalize-negative-size")
    digest = sha256_hex("finalize-negative-size-request")
    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True

    with pytest.raises(TurnLimitError) as raised:
        store.complete(key, "turn-1", {"marker": "x"}, size_bytes=-1)

    public = raised.value.as_public_dict()
    assert "dimension" in public
    assert "measured" in public
    assert "maximum" in public

    record = store.snapshot(key, "turn-1")
    assert record.state == TURN_STATE_IN_FLIGHT
    assert record.validated_result is None


def test_single_result_larger_than_the_byte_bound_refuses_at_finalization():
    store = TurnStore()
    key = _fresh_key("finalize-oversize-result")
    digest = sha256_hex("finalize-oversize-result-request")
    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True

    with pytest.raises(TurnLimitError) as raised:
        store.complete(key, "turn-1", {"marker": "x"}, size_bytes=MAX_IDEMPOTENCY_BYTES + 1)

    assert raised.value.maximum == MAX_IDEMPOTENCY_BYTES

    # Rather than being accepted and immediately self-evicted, the refusal
    # must leave the entry exactly as it was before the finalization attempt.
    record = store.snapshot(key, "turn-1")
    assert record is not None
    assert record.state == TURN_STATE_IN_FLIGHT


def test_completed_result_is_isolated_on_both_ingress_and_egress():
    store = TurnStore()
    key = _fresh_key("finalize-mutation-isolation")
    digest = sha256_hex("finalize-mutation-isolation-request")
    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True

    # 1. Reserve, then complete() with a mutable, nested validated result.
    # Keep both the original object (for the ingress mutation below) and an
    # independent deep snapshot of its original value (the ground truth every
    # later assertion in this test is compared against).
    mutable_result = {
        "assistant_turn_id": "a-1",
        "proposals": [{"text": "original"}],
        "prose": "original",
    }
    original_value = copy.deepcopy(mutable_result)
    store.complete(key, "turn-1", mutable_result, size_bytes=1)

    # 2. Ingress isolation: mutate the caller's original object -- including
    # a deep, nested mutation -- after complete() has already returned.
    mutable_result["prose"] = "MUTATED-VIA-CALLER"
    mutable_result["proposals"][0]["text"] = "MUTATED-VIA-CALLER"
    mutable_result["injected"] = "should-not-appear"

    # 3. Egress isolation via snapshot(): mutate the returned validated_result,
    # including a deep mutation of the nested list/dict.
    first_snapshot = store.snapshot(key, "turn-1")
    first_snapshot.validated_result["prose"] = "MUTATED-VIA-SNAPSHOT"
    first_snapshot.validated_result["proposals"][0]["text"] = "MUTATED-VIA-SNAPSHOT"

    # 4. Egress isolation via reserve() replay: the identical completed repeat
    # must not dispatch again, and its returned lease result is mutated too,
    # including a deep mutation.
    replay = store.reserve(key, "turn-1", digest)
    assert replay.should_dispatch is False
    replay.result["prose"] = "MUTATED-VIA-REPLAY"
    replay.result["proposals"][0]["text"] = "MUTATED-VIA-REPLAY"

    # 5. Re-snapshot and re-reserve: the stored validated result is
    # value-identical to the original finalized value from step 1 --
    # unaffected by all three mutations above (compared against the deep
    # snapshot of the original value, never against the mutated original).
    second_snapshot = store.snapshot(key, "turn-1")
    assert second_snapshot.validated_result == original_value

    second_replay = store.reserve(key, "turn-1", digest)
    assert second_replay.should_dispatch is False
    assert second_replay.result == original_value

    # 6. Identity distinctness: every hand-out is its own (deep) copy, never
    # the store's internal mutable object and never shared with any other
    # hand-out, at both the top level and the nested inner objects.
    assert first_snapshot.validated_result is not mutable_result
    assert first_snapshot.validated_result is not replay.result
    assert first_snapshot.validated_result is not second_snapshot.validated_result
    assert replay.result is not second_replay.result
    assert (
        first_snapshot.validated_result["proposals"][0]
        is not second_snapshot.validated_result["proposals"][0]
    )
    assert (
        replay.result["proposals"][0]
        is not second_replay.result["proposals"][0]
    )
    assert (
        first_snapshot.validated_result["proposals"][0]
        is not replay.result["proposals"][0]
    )


# --- FR-018: exactly one in-flight model turn per conversation key ---------
#
# spec.md FR-018 / data-model.md Section 5 / US2 acceptance scenario 3: at
# most one model turn may be in flight for a conversation key. TurnStore
# enforces this with a per-conversation-key guard (`_in_flight_by_key`), so
# a second, distinct client_turn_id for the same conversation_key is
# refused immediately with TurnInFlightError while a first turn for that key
# is still in flight. Regression: FR-018 requires exactly one in-flight turn
# per conversation key; an earlier draft keyed `_records` only by
# (conversation_key, client_turn_id) and allowed a second, distinct
# client_turn_id for the same conversation_key to dispatch concurrently with
# a first, still-in-flight turn; these tests pin the required per-key guard
# (FR-018). `doxbench_turns.TurnInFlightError` is
# referenced via the module object here (rather than added to the top-level
# import list) purely for locality with this historical block -- the class
# itself is fully defined in the module.


def test_a_second_turn_id_while_one_is_in_flight_for_the_same_conversation_refuses_dispatch():
    store = TurnStore()
    key = _fresh_key("in-flight-guard-same-key")
    digest_one = sha256_hex("in-flight-guard-request-1")
    digest_two = sha256_hex("in-flight-guard-request-2")

    first_lease = store.reserve(key, "turn-1", digest_one)
    assert first_lease.should_dispatch is True

    with pytest.raises(doxbench_turns.TurnInFlightError) as raised:
        store.reserve(key, "turn-2", digest_two)

    assert raised.value.in_flight_turn_id == "turn-1"
    message = str(raised.value)
    assert digest_one not in message
    assert digest_two not in message

    assert store.snapshot(key, "turn-2") is None
    still_first = store.snapshot(key, "turn-1")
    assert still_first.state == TURN_STATE_IN_FLIGHT
    assert still_first.request_digest == digest_one


def test_the_in_flight_refusal_is_immediate_and_never_blocks():
    store = TurnStore()
    key = _fresh_key("in-flight-guard-immediate")
    digest_one = sha256_hex("in-flight-immediate-request-1")
    digest_two = sha256_hex("in-flight-immediate-request-2")

    first_lease = store.reserve(key, "turn-1", digest_one)
    assert first_lease.should_dispatch is True

    outcome = {}

    def attempt_second():
        try:
            store.reserve(key, "turn-2", digest_two)
        except doxbench_turns.TurnInFlightError as exc:
            outcome["error"] = exc
        except BaseException as exc:  # pragma: no cover -- diagnostic only
            outcome["unexpected"] = exc

    thread = threading.Thread(target=attempt_second)
    thread.start()
    thread.join(timeout=2)

    assert not thread.is_alive()
    assert "unexpected" not in outcome
    assert "error" in outcome
    assert outcome["error"].in_flight_turn_id == "turn-1"
    # turn-1 is still unresolved -- proving the refusal above did not wait
    # for any finalization to occur.
    assert store.snapshot(key, "turn-1").state == TURN_STATE_IN_FLIGHT


def test_a_different_conversation_key_proceeds_while_another_key_has_an_in_flight_turn():
    store = TurnStore()
    key_one = _fresh_key("in-flight-guard-key-one")
    key_two = _fresh_key("in-flight-guard-key-two")
    digest = sha256_hex("in-flight-guard-cross-key-request")

    first_lease = store.reserve(key_one, "turn-1", digest)
    assert first_lease.should_dispatch is True

    other_lease = store.reserve(key_two, "turn-1", digest)
    assert other_lease.should_dispatch is True


def test_finalization_clears_the_in_flight_slot_so_the_next_turn_id_can_reserve():
    store = TurnStore()
    key = _fresh_key("in-flight-guard-clears-on-finalize")
    digest_one = sha256_hex("in-flight-guard-clear-request-1")
    digest_two = sha256_hex("in-flight-guard-clear-request-2")

    first_lease = store.reserve(key, "turn-1", digest_one)
    assert first_lease.should_dispatch is True
    store.complete(key, "turn-1", {"assistant_turn_id": "turn-1"}, size_bytes=1)

    second_lease = store.reserve(key, "turn-2", digest_two)
    assert second_lease.should_dispatch is True


def test_a_refused_finalization_can_be_retried_and_then_releases_the_in_flight_slot():
    # Recovery pin: a refused _finalize (e.g. a negative size_bytes) correctly
    # leaves the entry in-flight, which means the conversation key stays
    # occupied -- a different turn id is still refused -- until a valid
    # finalization lands, at which point the slot releases as usual. This
    # proves the refusal path and the FR-018 per-key guard compose correctly,
    # rather than the guard accidentally being left permanently stuck (or
    # accidentally released) by a refused finalization attempt.
    store = TurnStore()
    key = _fresh_key("in-flight-guard-refused-finalize-then-recovers")
    digest_one = sha256_hex("in-flight-guard-refused-finalize-request-1")
    digest_two = sha256_hex("in-flight-guard-refused-finalize-request-2")

    lease = store.reserve(key, "turn-1", digest_one)
    assert lease.should_dispatch is True

    with pytest.raises(TurnLimitError):
        store.complete(key, "turn-1", {"marker": "should-not-apply"}, size_bytes=-1)

    # The slot is still occupied by turn-1: a different turn id on the same
    # key is still refused.
    with pytest.raises(doxbench_turns.TurnInFlightError) as raised:
        store.reserve(key, "turn-2", digest_two)
    assert raised.value.in_flight_turn_id == "turn-1"

    # A VALID finalization for turn-1 now lands.
    store.complete(key, "turn-1", {"assistant_turn_id": "turn-1"}, size_bytes=1)
    record = store.snapshot(key, "turn-1")
    assert record.state == TURN_STATE_COMPLETED

    # The slot is released: a different turn id on the same key now
    # dispatches.
    second_lease = store.reserve(key, "turn-2", digest_two)
    assert second_lease.should_dispatch is True


def test_no_window_where_two_same_key_reservations_both_hold_dispatch_rights():
    store = TurnStore()
    key = _fresh_key("in-flight-guard-race")
    thread_count = 8
    barrier = threading.Barrier(thread_count)
    lock = threading.Lock()
    dispatch_winners = []
    refusals = []
    unexpected = []

    def worker(index):
        digest = sha256_hex(f"in-flight-guard-race-request-{index}")
        barrier.wait()
        try:
            lease = store.reserve(key, f"turn-{index}", digest)
        except doxbench_turns.TurnInFlightError as exc:
            with lock:
                refusals.append(exc)
            return
        except BaseException as exc:  # pragma: no cover -- diagnostic only
            with lock:
                unexpected.append(exc)
            return
        with lock:
            if lease.should_dispatch:
                dispatch_winners.append(f"turn-{index}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(thread_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
        assert not thread.is_alive()

    assert unexpected == []
    assert len(dispatch_winners) == 1
    assert len(refusals) == thread_count - 1
    for exc in refusals:
        assert exc.in_flight_turn_id == dispatch_winners[0]


# ---------------------------------------------------------------------------
# operator-escalated regression: the store's own lock must never be held
# across a caller's deep copy of a result payload (research R8; the class
# docstring's own "never held across a caller's...work" claim). Measured
# ~58ms of unrelated lock hold at three sites -- ingress in `_finalize`,
# egress in `snapshot`, egress in `reserve`'s replay branch -- all three
# previously called `copy.deepcopy` WHILE the lock was held. These tests pin
# the fix that moved every copy outside the lock. These tests are
# deterministic: no wall-clock timing assertions, no sleeps.
# ---------------------------------------------------------------------------


class _LockFreedomProbePayload:
    """A result payload whose ``__deepcopy__`` hook records whether the
    store's own lock was free at the moment ``copy.deepcopy`` touched it.

    ``threading.Lock`` is non-reentrant, so a non-blocking ``acquire()``
    called from inside this hook returns ``False`` if the lock is held by
    ANYONE -- including the very thread performing the copy -- and ``True``
    only if the lock is genuinely free. Reaching into ``store._lock`` here
    is deliberate: there is no public API that exposes lock state, and this
    is a narrowly-scoped, well-commented probe for exactly that discipline.
    """

    def __init__(self, store: TurnStore, observations: list) -> None:
        self._store = store
        self._observations = observations

    def __deepcopy__(self, memo):
        acquired = self._store._lock.acquire(blocking=False)
        if acquired:
            self._store._lock.release()
            self._observations.append("free")
        else:
            self._observations.append("HELD")
        clone = _LockFreedomProbePayload(self._store, self._observations)
        memo[id(self)] = clone
        return clone


def test_ingress_result_copy_happens_outside_the_store_lock():
    store = TurnStore()
    key = _fresh_key("lock-release-ingress")
    digest = sha256_hex("lock-release-ingress-request")
    observations: list = []

    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True

    store.complete(key, "turn-1", _LockFreedomProbePayload(store, observations), size_bytes=1)

    assert observations, "expected the ingress deep copy in _finalize to have run"
    assert "HELD" not in observations


def test_snapshot_egress_result_copy_happens_outside_the_store_lock():
    store = TurnStore()
    key = _fresh_key("lock-release-snapshot-egress")
    digest = sha256_hex("lock-release-snapshot-egress-request")
    observations: list = []

    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True
    store.complete(key, "turn-1", _LockFreedomProbePayload(store, observations), size_bytes=1)

    store.snapshot(key, "turn-1")

    assert observations, "expected the ingress and egress deep copies to have run"
    assert "HELD" not in observations


def test_replay_egress_result_copy_happens_outside_the_store_lock():
    store = TurnStore()
    key = _fresh_key("lock-release-replay-egress")
    digest = sha256_hex("lock-release-replay-egress-request")
    observations: list = []

    lease = store.reserve(key, "turn-1", digest)
    assert lease.should_dispatch is True
    store.complete(key, "turn-1", _LockFreedomProbePayload(store, observations), size_bytes=1)

    replay = store.reserve(key, "turn-1", digest)
    assert replay.should_dispatch is False

    assert observations, "expected the ingress and replay egress deep copies to have run"
    assert "HELD" not in observations


def test_a_blocked_result_copy_does_not_stall_an_unrelated_conversation_key():
    # Stronger interleave proof, beyond the deterministic free/HELD probes
    # above: a caller whose result payload takes a genuinely long time to
    # deep-copy must never stall a totally unrelated conversation key.
    #
    # The blocking payload's __deepcopy__ blocks on a threading.Event until
    # released. That blocking copy is triggered from its own worker thread
    # (`blocked_thread`, via `snapshot`), and -- critically for making this
    # test deadlock-proof -- the independent conversation-key cycle is ALSO
    # run on its own bounded worker thread (`idle_thread`) rather than
    # inline: if the fix is absent and the store's lock is genuinely held
    # for the whole blocked copy, `idle_thread`'s own `reserve()` call would
    # block indefinitely waiting for that same lock. Running it on a
    # separate thread lets this test bound the wait with `join(timeout=...)`
    # and then ASSERT on the recorded outcome, so an absent fix produces a
    # failed assertion -- never a frozen test process. The blocking event is
    # always released in a `finally`, so `blocked_thread` (and, once the lock
    # is free, `idle_thread`) can always eventually complete and be joined.
    store = TurnStore()
    blocking_key = _fresh_key("lock-release-interleave-blocking")
    idle_key = _fresh_key("lock-release-interleave-idle")
    digest = sha256_hex("lock-release-interleave-blocking-request")
    idle_digest = sha256_hex("lock-release-interleave-idle-request")

    copy_started = threading.Event()
    release_copy = threading.Event()
    block_enabled = [False]

    class _BlockingPayload:
        def __deepcopy__(self, memo):
            if block_enabled[0]:
                copy_started.set()
                release_copy.wait(timeout=5)
            clone = _BlockingPayload()
            memo[id(self)] = clone
            return clone

    lease = store.reserve(blocking_key, "turn-1", digest)
    assert lease.should_dispatch is True
    # Complete BEFORE arming the block, so this ingress copy of a
    # not-yet-armed payload never itself blocks.
    store.complete(blocking_key, "turn-1", _BlockingPayload(), size_bytes=1)
    block_enabled[0] = True

    blocked_outcome: dict = {}

    def blocked_worker():
        store.snapshot(blocking_key, "turn-1")
        blocked_outcome["finished"] = True

    blocked_thread = threading.Thread(target=blocked_worker)
    blocked_thread.start()

    idle_outcome: dict = {}

    def idle_worker():
        idle_lease = store.reserve(idle_key, "turn-1", idle_digest)
        idle_outcome["should_dispatch"] = idle_lease.should_dispatch
        if not idle_lease.should_dispatch:
            return
        store.complete(idle_key, "turn-1", {"assistant_turn_id": "idle"}, size_bytes=8)
        idle_snapshot = store.snapshot(idle_key, "turn-1")
        idle_outcome["result"] = idle_snapshot.validated_result if idle_snapshot else None

    idle_thread = threading.Thread(target=idle_worker)
    try:
        assert copy_started.wait(timeout=5), "the blocking copy never started"

        # While blocked_worker's copy is parked inside __deepcopy__, run a
        # full independent reserve/complete/snapshot cycle for a DIFFERENT
        # conversation key on its own bounded worker thread -- never inline
        # on this thread, so a still-held lock cannot hang the test itself.
        idle_thread.start()
        idle_thread.join(timeout=2)
        idle_outcome["thread_finished_while_blocked"] = not idle_thread.is_alive()
    finally:
        release_copy.set()

    blocked_thread.join(timeout=5)
    idle_thread.join(timeout=5)

    assert not blocked_thread.is_alive()
    assert blocked_outcome.get("finished") is True

    assert not idle_thread.is_alive()
    # The core proof: the unrelated key's full cycle finished WHILE the
    # blocking copy was still parked -- it was never stalled behind it.
    assert idle_outcome.get("thread_finished_while_blocked") is True
    assert idle_outcome.get("should_dispatch") is True
    assert idle_outcome.get("result") == {"assistant_turn_id": "idle"}


# ===========================================================================
# HARD BOUNDARY sentinels
# ===========================================================================


FORBIDDEN_SOURCE_SNIPPETS = (
    "import requests",
    "import httpx",
    "import socket",
    "import openai",
    "import anthropic",
    "boto3",
    "urllib",
    "subprocess",
    "os.environ",
    "os.getenv",
    "getenv(",
    "http://",
    "https://",
    "api_key",
    "apikey",
    "secret",
    "bearer",
    "jsonschema",
    "from ideation_dashboard.serve",
    "import serve",
)

FORBIDDEN_CLOCK_SNIPPETS = (
    "time.time(",
    "datetime.now(",
    "time.monotonic(",
    "perf_counter(",
    "utcnow(",
)


def test_module_source_contains_no_network_provider_serve_or_logging_markers():
    src = MODULE_PATH.read_text(encoding="utf-8")
    lowered = src.lower()
    for forbidden in FORBIDDEN_SOURCE_SNIPPETS:
        assert forbidden.lower() not in lowered, forbidden


def test_module_source_uses_no_wall_clock_ordering_for_lru():
    src = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in FORBIDDEN_CLOCK_SNIPPETS:
        assert forbidden not in src, forbidden


def test_no_quoted_wire_envelope_literals_in_source():
    # HARD BOUNDARY 1: the openxFactory xfactory-workbench-chat-turn schema is
    # UNRELEASED. This module's prompt/request representation is internal and
    # schema-agnostic: it must define no schema_version and no wire kind
    # literal anywhere in its source.
    src = MODULE_PATH.read_text(encoding="utf-8")
    for quoted in ('"schema_version"', "'schema_version'", '"kind"', "'kind'"):
        assert quoted not in src, quoted


def test_module_holds_no_bound_network_module_in_its_namespace():
    forbidden_names = ("requests", "httpx", "socket", "urllib", "subprocess", "os", "http")
    for name in forbidden_names:
        assert name not in vars(doxbench_turns), name


# ---------------------------------------------------------------------------
# T057/T061 (US3, red-first): strict typed assistant-response validation
# against the pinned released contract (typed_proposal: exactly
# {target, base_hash, summary, content}; 0-2 proposals; unique targets).
# Wrong-base at VALIDATION time is a RESPONSE-side defect (the model answered
# against content it was not shown) — distinct from client staleness at Apply
# time, which is a browser-model state and never a server error (R4).
# ---------------------------------------------------------------------------

_OBSERVED = doxbench_turns.ObservedHashes(
    outline=ContentIdentity(algorithm="sha256", hex="a" * 64),
    document=ContentIdentity(algorithm="sha256", hex="b" * 64),
)


def _proposal(**over):
    base = {"target": "outline", "base_hash": "a" * 64,
            "summary": "Tighten the outline", "content": "# New outline\n"}
    base.update(over)
    return base


def _raw(proposals=(), prose="grounded answer"):
    return {"assistant_prose": prose, "proposals": list(proposals)}


def test_a_prose_only_response_validates_with_no_proposals():
    validated = doxbench_turns.validate_assistant_response(
        _raw(), observed=_OBSERVED)
    assert validated.assistant_prose == "grounded answer"
    assert validated.proposals == ()


def test_one_and_two_target_responses_validate_and_freeze():
    one = doxbench_turns.validate_assistant_response(
        _raw([_proposal()]), observed=_OBSERVED)
    assert len(one.proposals) == 1
    assert one.proposals[0].target == "outline"
    assert one.proposals[0].base_hash == "a" * 64
    two = doxbench_turns.validate_assistant_response(
        _raw([_proposal(),
              _proposal(target="document", base_hash="b" * 64)]),
        observed=_OBSERVED)
    assert [p.target for p in two.proposals] == ["outline", "document"]
    with pytest.raises(Exception):
        two.proposals[0].content = "mutated"  # type: ignore[misc]


@pytest.mark.parametrize("bad,label", [
    ([_proposal(), _proposal()], "duplicate-target"),
    ([_proposal(target="sidebar", base_hash="a" * 64)], "unknown-target"),
    ([_proposal(base_hash="f" * 64)], "wrong-base"),
    ([_proposal(content="x" * 400_001)], "oversized-content"),
    ([_proposal(summary="")], "blank-summary"),
    ([_proposal(summary="s" * 501)], "oversized-summary"),
    ([{"target": "outline", "base_hash": "a" * 64,
       "summary": "no content key"}], "missing-field"),
    ([_proposal(extra="key")], "extra-field"),
    ([_proposal(), _proposal(target="document", base_hash="b" * 64),
      _proposal()], "three-proposals"),
    ("not-a-list", "proposals-not-a-list"),
], ids=lambda v: v if isinstance(v, str) else "")
def test_defective_typed_responses_are_refused(bad, label):
    with pytest.raises(doxbench_turns.TurnResponseError):
        doxbench_turns.validate_assistant_response(
            _raw(bad if isinstance(bad, list) else []) if isinstance(bad, list)
            else {"assistant_prose": "x", "proposals": bad},
            observed=_OBSERVED)


def test_the_total_response_bound_is_satisfied_by_construction_and_still_enforced():
    """The plan's 900,000-byte spanning total is UNREACHABLE while the
    stricter per-piece caps hold (65,536 + 2 x 400,000 = 865,536), so the
    largest legal response must validate — pinned here so a future cap
    raise that silently breaks the relationship fails this test — and the
    validator's own spanning check stays as belt-and-braces."""
    assert (doxbench_turns.MAX_ASSISTANT_PROSE_BYTES
            + 2 * doxbench_turns.MAX_PROPOSAL_BYTES
            <= doxbench_turns.MAX_RESPONSE_TOTAL_BYTES)
    largest = doxbench_turns.validate_assistant_response(
        _raw([_proposal(content="x" * 400_000),
              _proposal(target="document", base_hash="b" * 64,
                        content="y" * 400_000)],
             prose="p" * 65_536),
        observed=_OBSERVED)
    assert len(largest.proposals) == 2


def test_wrong_base_names_the_response_class_not_a_scope_or_identity_error():
    with pytest.raises(doxbench_turns.TurnResponseError):
        doxbench_turns.validate_assistant_response(
            _raw([_proposal(base_hash="c" * 64)]), observed=_OBSERVED)
