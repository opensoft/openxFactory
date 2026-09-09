"""The doxBench WIRE VOCABULARY and the shared transport bounds
(`split-opendox-two-layer-product` § 2.4, PR 2 of 4).

Lifted OUT of `serve.py` UNCHANGED, byte for byte, because the by-function split
needs somewhere for the names BOTH columns read to live. `serve.py`'s core
readers (`_read_json_body`, `_read_bounded_json_body`, `_not_the_human_console`)
and the openDox column's routes (`serve_workbench.py`, `serve_project.py`) reach
the same error catalog, the same fixed messages, the same envelope builders and
the same body bounds; had they stayed in `serve.py` the column modules would
have had to import `serve` while `serve` imported them, and an import cycle is
not a seam. The graph is a DAG instead:

    serve_wire  <-  serve_workbench  <-  serve
    serve_wire  <-  serve_project    <-  serve
    serve_wire  <-  serve

and `serve.py` imports every name back by an explicit `from … import`, so its
module namespace is exactly what it was — `serve.doxbench_error_body`,
`serve.DOXBENCH_ERROR_CATALOG`, `serve.JSON_CTYPE` and the rest all still
resolve, which is what lets the existing suites read them unchanged.

WHY THIS IS NOT THE openDox COLUMN. The catalog is genuinely SHARED: the gate
verb handler (openXdox's column, extracted in PR 3) answers on
`doxbench_error_body`/`doxbench_error_status` at `DOXBENCH_MAX_REQUEST_BYTES`,
and the core body readers carry `JSON_OBJECT_BODY_REQUIRED` and
`_MAX_BODY_BYTES`. Filing this vocabulary under `serve_workbench.py` would have
made the CORE depend on the openDox column, which is the carve backwards.

WIDENED BY PR 3 OF 4 for exactly the same reason this module exists, and
EMPTIED AGAIN by the pre-carve splits — read them together, because the
hosted-plane group this paragraph used to describe HAS NOW LEFT IN FULL. The
hosted-plane confinement — `HOSTED_SESSION_REFUSAL`, `hosted_ref_refused`,
`hosted_index` (FR-048) — ARRIVED here as a group, but the three names are not
read alike, and that is what eventually sent every one of them on. This
paragraph is now this module's HISTORY of them, and the record of where each
went and why:

- `hosted_index` went FIRST, by pre-carve split S-3 (§ 3.1 of this same
  change), into `serve_projection.py` beside its one in-tree reader
  `_serve_index` — an openXdox FR-048 index-confinement rule inside a module
  that goes WHOLE to openDox is a file the carve manifest cannot file under
  one column.
- `hosted_ref_refused` FOLLOWED IT, into the same module, beside it, by OQ-B
  re-plumb B-2 on Brett Heap's ruling of 2026-09-09 (`#656`, "rule B-2 (i')").
  It was read by the CORE (`_divergence_headers`, `serve.py`), by the openXdox
  projection column (`serve_projection.py`: the snapshot, index and `/source`
  routes) and by the openxFactory adapter column
  (`serve_openxfactory_lanes.py`: the refresh binding reachable off loopback)
  — and that LAST reader is what settled it. `serve_openxfactory_lanes.py`
  STAYS in openxFactory, so its import of a name defined here was an
  openxFactory to openDox edge, which RULING OQ-2 forbids after the carve. The
  predicate's one dependency, `snapshot_registry.is_publishable_ref`, is the
  openXdox column and was already imported by `serve_projection.py`, so the
  move costs no dependency and adds no edge, and three of its four call sites
  were already in the destination.
- `HOSTED_SESSION_REFUSAL` went in the SAME re-plumb, but the other way: a
  `str` literal carries no dependency, so it is neutral by construction and
  joined `JSON_CTYPE` and `JSON_OBJECT_BODY_REQUIRED` in the neutral
  `scripts/wire_messages.py` — where it is `not_moved`, reason
  `replicated_at_destination` (RULED OQ-A/OQ-C), rather than filed under any
  column at all. It is re-exported here, so it still resolves off this module.

So the group above names nothing this module DEFINES any more. Leaving any of
the three in `serve.py` would still have forced at least one column to import
`serve` while `serve` imported it, which is the cycle this module exists to
prevent — this module was the right first home for all three and the wrong
last one for each. `serve.py` takes `hosted_index` and `hosted_ref_refused`
from `serve_projection` and the three strings from this module's re-export, so
`serve.hosted_ref_refused`, `serve.hosted_index` and `serve.JSON_CTYPE` all
resolve exactly as they did for the suites that call them directly. What
remains here is this module's own stated remit: the shared wire vocabulary and
pure envelope builders over already-validated inputs, plus fixed refusal prose
BOTH columns read.

NOTHING HERE REACHES A PROVIDER, a socket or a filesystem: it is constants,
fixed refusal prose, pure envelope builders over already-validated inputs, and
two bounded readers over a request's own file handle.

INVOCATION (design D12): `serve.py` runs BOTH as a script and as a module, so
this module uses ABSOLUTE `ideation_dashboard.*` imports, never `from . import`.
"""

from __future__ import annotations

import json

from ideation_dashboard import doxbench_knowledge
from ideation_dashboard import doxbench_packet
from ideation_dashboard import doxbench_threads
# The family's NON-BLANK rule (issue #263), imported rather than
# restated: the type gate and this server boundary share one
# implementation so they cannot drift into two spellings of one rule.
from ideation_dashboard.doxbench_packet import states_something

# The three FIXED WIRE STRINGS moved OUT of this module to the neutral
# `scripts/wire_messages.py` (OQ-B re-plumb B-2, ruled on `#656`
# 2026-09-09): `serve_openxfactory_lanes.py` is openxFactory's own adapter
# column and STAYS, this module is openDox under design D3, and RULING OQ-2
# forbids that direction after the carve. A `str` literal carries no
# dependency, so all three are neutral by construction. Re-exported here —
# the SAME OBJECTS, not copies — so `serve_wire.JSON_CTYPE` and its two
# siblings keep resolving for every existing caller (`serve.py`,
# `serve_workbench.py`, `serve_project.py`, `serve_gate.py`,
# `serve_projection.py`, and the suites that read them off `serve`).
from wire_messages import (  # noqa: F401  (re-export)
    HOSTED_SESSION_REFUSAL,
    JSON_CTYPE,
    JSON_OBJECT_BODY_REQUIRED,
)

_MAX_BODY_BYTES = 65_536  # a tile-action body is tiny; cap it to refuse a flood

# W-5/W-6 (wave re-review): how much of a REFUSED body a reader will
# read-and-discard so the refusal survives its own transport. Sized past the
# largest body a real client can legally compose (a maximal 400,000-byte
# buffer JSON-escapes to under 2.5 MiB); a sender past this is a flood, and
# its connection closes with bytes unread. Shared by BOTH readers — the tiny
# global-cap reader and the route-specific bounded reader — so the
# refusal-races-its-own-transport fix has one posture, not a band.
_MAX_REFUSED_DRAIN_BYTES = 4 * 1024 * 1024


def _drain_refused_body(rfile, declared: int) -> None:
    """Read and DISCARD a refused body so the refusal survives its own
    transport (T104 F5/F8; wave re-review W-5/W-6). Chunked in cap-sized
    reads (never buffering what it refuses to parse) and bounded by
    `_MAX_REFUSED_DRAIN_BYTES` — beyond it the sender is a flood, not a
    client whose refusal needs to survive, and the connection closes with
    bytes unread. A read that stops arriving raises out of the socket
    timeout (`DashboardHandler.timeout`) rather than blocking forever: the
    drain without that bound traded an instant refusal for an unbounded
    block, which was strictly worse (W-5). Module-level over a bare file
    object so the request-shaped test doubles need nothing beyond `.rfile`.
    """
    remaining = min(declared, _MAX_REFUSED_DRAIN_BYTES)
    try:
        while remaining > 0:
            chunk = rfile.read(min(remaining, _MAX_BODY_BYTES))
            if not chunk:
                break
            remaining -= len(chunk)
    except OSError:
        return
class _CredentialStream:
    """A BOUNDED TEXT VIEW of an intake request's body, and nothing else
    (add-doxchat-model-intake task 2.2).

    THE WHOLE POINT IS WHAT IT DOES NOT DO. It never assembles the body, never
    returns it, never stores it and never logs it: it exposes exactly the one
    method `shutil.copyfileobj` calls — `read(size)` — so
    `doxbench_provider.hand_off_credential` can move the value in chunks from
    this connection's read handle into the broker's standard input. No variable
    in this process ever holds the whole credential, and this object holds only
    the chunk currently in flight, for exactly as long as the copy takes.

    IT DECODES INCREMENTALLY because the broker child is opened in text mode and
    a UTF-8 sequence can straddle a chunk boundary. A whole-body `.decode()`
    would have been simpler and would have materialised the value, which is the
    one thing this class exists not to do.

    IT IS BOUNDED BY THE DECLARED LENGTH, never by trust in it: it reads at most
    what `Content-Length` declared and stops, so a sender that declares less than
    it means cannot leave bytes on the socket for the next request to read, and
    one that declares more simply reaches end of stream. The route refuses a
    declaration past `MAX_CREDENTIAL_BYTES` before this object is ever built.

    `__repr__` DISCLOSES NOTHING, on the same reasoning the provider client's own
    redacting token repr uses: a traceback frame or a debugger that printed this
    object must not print what travelled through it — and it cannot, because it
    kept none of it.
    """

    __slots__ = ("_rfile", "_remaining", "_decoder")

    def __init__(self, rfile, declared: int) -> None:
        import codecs
        self._rfile = rfile
        self._remaining = max(0, int(declared))
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")

    def read(self, size: int = -1) -> str:
        if self._remaining <= 0:
            return self._decoder.decode(b"", True)
        want = self._remaining if size is None or size < 0 else min(
            size, self._remaining)
        chunk = self._rfile.read(want)
        if not chunk:
            self._remaining = 0
            return self._decoder.decode(b"", True)
        self._remaining -= len(chunk)
        return self._decoder.decode(chunk, self._remaining <= 0)

    def __repr__(self) -> str:
        return "_CredentialStream(<withheld>)"


# --------------------------- doxBench request handling ---------------------------
#
# T024 introduced the route-specific request bound, fixed error vocabulary,
# and injected model-port seam. T050/T051 now consume those foundations from
# the reachable catalog and chat-turn routes declared above.
#
# The wire envelope stays `schema_version`/`kind`-FREE, deliberately: the two
# additive openxFactory schemas (`xfactory-workbench-model-catalog`,
# `xfactory-workbench-chat-turn`) are not yet released — blocked on
# T005-T008, T014, T021, and OpenSpec items 2.1/2.5 (plan.md's "Contract
# Baseline and Merge Pin", research.md R13). This section reuses serve.py's
# EXISTING `{"ok": false, "error": <code>, "message": <fixed string>}`
# discipline only; the schema-versioned envelope arrives WITH the released
# contract, not before.
#
# `WorkbenchModelPort` declares THREE members -- the adapter-declared timeout,
# the catalog, and the single opaque dispatch -- and all three are consumed
# here. `model_port_factory` below (and `_workbench_model_port`, on the handler
# class further down) stays DUCK-TYPED at the injection boundary, so a
# catalog-only adapter still resolves and the dispatch arms probe for
# `dispatch` rather than asserting a type. (This paragraph used to describe
# T020's "catalog-only core" and say the turn handler "deliberately stops
# before provider dispatch because the port has no dispatch member yet". T051's
# dispatch arm landed and the sentence has been false since; corrected by
# add-doxbench-distilled-abstract §5 rather than left for the next reader to
# disbelieve.) The consumers are now TWO: the chat turn, and the per-document
# distilled abstract, which reaches the same seam through the same gate.
#
# Nothing here reaches a provider: no provider SDK import, no provider
# env-var read, no credential, no raw endpoint, no secret name.

# The ROUTE-SPECIFIC bound (research R7): NOT a second global cap.
# `_MAX_BODY_BYTES` above stays the EXISTING tiny 65,536-byte tile-action cap
# — R7 explicitly rejects widening IT, because that would weaken every
# unrelated action and lose measured limit errors. The doxBench chat-turn
# route declares this bound for ITSELF, sized to plan.md's Constraints total
# (1,048,576 UTF-8 bytes).
#
# T104 F5-6 UPDATE to that record: "every route that already exists keeps the
# tiny cap" is no longer quite the rule, because one already-existing verb was
# found to carry a declared LARGE payload. The gate verb `first-edit` (the
# governed Save) posts a document's full replacement text, whose bound both
# sides declare at `doxbench_hash.MAX_BUFFER_BYTES` (400,000) — over the tiny
# cap by design, so the transport refused a legal Save with a misleading
# message. That ONE verb now reads through `_read_bounded_json_body` at THIS
# same bound (see the branch in `_handle_gate_action` for the full record);
# every other pre-existing route keeps `_read_json_body` and the tiny cap,
# exactly as R7 decided.
DOXBENCH_MAX_REQUEST_BYTES = 1_048_576

# ---- released wire identifiers (T024/T050/T051 wire clause) ----
# The additive openxFactory schemas are RELEASED and PINNED at contract-v1.27
# (`d09d5820de5b63b9528f6baea884a6dccde9b158`), so the deferral this section
# used to record is discharged. `doxbench_contracts` is the AUTHORITY: it reads
# the released bytes, verifies their digests against the checkout's own
# manifest, and confirms `stack.yaml` still declares that ref. These literals
# exist only so the pure envelope builders below need no schema import, and the
# companion suite pins each one against `doxbench_contracts`'s released
# constant so a second spelling cannot drift. Conformance is never claimed from
# these constants: every wire shape is VALIDATED against the released schema
# before it is sent.
DOXBENCH_WIRE_SCHEMA_VERSION = 1
DOXBENCH_MODEL_CATALOG_KIND = "workbench-model-catalog"
# The ONE served chat-turn family (contract-v3.0,
# retire-doxbench-chat-turn-v1). Three v1 kind constants stood here --
# `workbench-chat-turn`, `-success` and `-failure` -- added at contract-v1.31,
# DEPRECATED at contract-v1.34 when the widened family arrived beside them, and
# removed at contract-v3.0 with the envelopes they named. Nothing in the estate
# emits them: the shipped client (`web/views/doxbench-chat.js`) is `-v2`-only,
# and the route now REFUSES an unrecognized kind rather than coercing it into a
# family that no longer exists (see `_handle_workbench_chat_turn`).
DOXBENCH_CHAT_TURN_V2_KIND = "workbench-chat-turn-v2"
DOXBENCH_CHAT_TURN_V2_SUCCESS_KIND = "workbench-chat-turn-v2-success"
DOXBENCH_CHAT_TURN_V2_FAILURE_KIND = "workbench-chat-turn-v2-failure"

# ---- fixed doxBench error catalog (mirrors action_errors.ERROR_CATALOG's shape) ----
# The closed code set combines spellings pinned verbatim by the planning
# contracts with route-level judgement calls documented beside their entries.
DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED = "request_limit_exceeded"
DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE = "model_capability_unavailable"
DOXBENCH_ERR_CATALOG_UNAVAILABLE = "catalog_unavailable"
DOXBENCH_ERR_CONSOLE_REQUIRED = "console_required"
# ---- T050/T051 additions. `turn_id_conflict` is VERBATIM from
# `contracts/chat-turn.md`; the other five are this slice's own judgement
# calls (spelling AND, where noted, HTTP status) -- the planning packet pins
# the BEHAVIOUR but leaves these six spellings/statuses unpinned. See the
# section banner above `_handle_workbench_model_catalog` for the full record.
DOXBENCH_ERR_TURN_ID_CONFLICT = "turn_id_conflict"
DOXBENCH_ERR_TURN_IN_FLIGHT = "turn_in_flight"
DOXBENCH_ERR_TURN_SCOPE_REFUSED = "turn_scope_refused"
DOXBENCH_ERR_CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
DOXBENCH_ERR_MODEL_UNAVAILABLE = "model_unavailable"
DOXBENCH_ERR_INVALID_TURN_REQUEST = "invalid_turn_request"
# add-doxbench-distilled-abstract §5, and the same class of judgement call: the
# abstract route's own malformed-request code. `invalid_turn_request` is not
# reusable for it, because its fixed message says "the turn request is
# malformed" and an abstract request is not a turn -- a refusal that misnames
# what the caller sent points the reader at the wrong contract.
DOXBENCH_ERR_INVALID_ABSTRACT_REQUEST = "invalid_abstract_request"
# The 500 for an abstract this server composed and could not then use -- the
# same class, and deliberately the same phrasing, as `catalog_unavailable`. No
# request the caller could send would fix it, so a 4xx would misdirect.
DOXBENCH_ERR_ABSTRACT_UNAVAILABLE = "abstract_unavailable"
# ---- T051 dispatch-arm additions. These three spell doxbench_model's
# CLOSED dispatch-code set (`DISPATCH_FAILURE_CODES`; its fourth member is
# `model_unavailable`, already above). doxbench_model is a deferred
# function-scope import in this module, so the spellings are restated as
# literals here and the companion route test pins the parity — same
# discipline as the CATALOG_WIRE_KIND restatement in doxbench_model.py.
DOXBENCH_ERR_MODEL_TIMEOUT = "model_timeout"
DOXBENCH_ERR_MODEL_FAILED = "model_failed"
DOXBENCH_ERR_RESPONSE_INVALID = "response_invalid"

# add-doxbench-editing-phase-b §10, and BOTH are judgement-call spellings this
# slice records rather than inherits. The released failure envelope's `error` is
# a free-form `^[a-z][a-z0-9_]{2,63}$` string, not an enum, so naming a
# server-side condition honestly needs no contract change — and reusing
# `request_limit_exceeded` for either of these would state something FALSE:
# that the CALLER's request was too large, when what exceeded a bound was
# context the server itself selected or the session's own threads.
DOXBENCH_ERR_CONTEXT_PACKET_INVALID = "context_packet_invalid"
DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED = "context_packet_bound_exceeded"

# add-doxbench-editing-phase-b §9.5, and the same class of judgement call: a
# thread is session working memory on an unmerged branch, so where no branch
# session can be opened there is nothing for a thread to be. Reusing
# `model_capability_unavailable` would state a different absence, and reusing
# `turn_scope_refused` would blame the scope for a capability verdict.
DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE = "thread_capability_unavailable"

# add-doxchat-model-intake §2/§3. THREE codes, and the split is the same class
# of judgement call the thread route's own code records.
#
#   * `intake_refused` is the flow REFUSING RATHER THAN DEGRADING: no broker is
#     declared, the broker would not take custody, or the declaration this
#     install already holds forbids the act. It is a STATED refusal — the body
#     carries a `reason` from `doxbench_intake`'s own fixed sentences, exactly as
#     the thread route's absence body carries a declared cause — because "the
#     wizard did not work" and "there is nowhere governed to put a credential"
#     are different facts with different remedies, and only one of them is
#     something the human can act on;
#   * `invalid_intake_request` is the request's own shape: a missing declared
#     fact, an unknown authentication kind, a body past the bound. 400, like
#     every other malformed-request refusal on this surface;
#   * `approval_refused` is the second act failing on its own terms — nothing
#     pending under that name, something already approved, a record that would
#     not validate. Kept separate from `intake_refused` because approving is a
#     different decision from enrolling, which is the whole point of §3.
#
# NONE of them ever carries the broker's words, the provider's words, or the
# supplied value. The `reason` is always one of this repository's own module
# constants.
DOXBENCH_ERR_INTAKE_REFUSED = "intake_refused"
DOXBENCH_ERR_INVALID_INTAKE_REQUEST = "invalid_intake_request"
DOXBENCH_ERR_APPROVAL_REFUSED = "approval_refused"

# retire-doxbench-chat-turn-v1 (contract-v3.0), and the answer to that packet's
# OQ-3, which deliberately left the token and the status to the realization.
#
# THE CODE THE REDESIGNED FALLBACK NEEDS. Until contract-v3.0 an unrecognized or
# absent chat-turn `kind` was coerced into the DEPRECATED v1 family and refused
# there. The family is gone, so the coercion is gone, and the refusal now
# answers in the surviving family -- which requires naming the condition.
#
# WHY NOT `invalid_turn_request`. That code's fixed message says "the turn
# request is malformed", which is a true sentence about a DIFFERENT failure: a
# request whose `kind` this release does not serve may be perfectly well formed
# in the family it names. Reusing it would tell a client to go looking for a
# shape error that is not there. The distinction is the same one
# `invalid_abstract_request` records against this code, for the same reason.
#
# WHY IT SAYS NOTHING ABOUT THE REMOVAL. A retired v1 kind and a kind that never
# existed reach this code identically, and the message does not distinguish
# them. The surviving contract has no vocabulary for "removed at a major", and
# inventing one to soften a refusal would put migration guidance on the wire
# instead of in the changelog, where a consumer upgrading across the major
# actually reads it.
#
# 400, the same status and the same class as every other
# malformed-or-unservable-request refusal on this surface. It is the caller's
# request that cannot be served, and a different request WOULD be served, which
# is what makes 4xx right.
#
# THE CONTRACT PERMITS IT WITHOUT WIDENING ANYTHING. `$defs/failure_v2`
# constrains `error` by the PATTERN `^[a-z][a-z0-9_]{2,63}$` and by no enum, and
# the delegated validator that judges a failure applies no code vocabulary
# either. The only CLOSED list is `DOXBENCH_ERROR_CATALOG` below -- which RAISES
# on an unregistered code -- so this constant and its catalog entry land in the
# same commit as the arm that answers it, or the refusal path faults instead of
# refusing.
DOXBENCH_ERR_UNRECOGNIZED_TURN_KIND = "unrecognized_turn_kind"

# Fixed, module-level messages: never composed from request data, exactly
# like `action_errors.ERROR_CATALOG`'s messages.
_DOXBENCH_MSG_REQUEST_LIMIT_EXCEEDED = "the request exceeds the allowed size for this route"
_DOXBENCH_MSG_MODEL_CAPABILITY_UNAVAILABLE = "this plane has no model capability"
_DOXBENCH_MSG_CATALOG_UNAVAILABLE = "the model catalog could not be assembled safely"
_DOXBENCH_MSG_CONSOLE_REQUIRED = "this route is available only from the local human console"
_DOXBENCH_MSG_TURN_ID_CONFLICT = "this turn id was already used for different request content"
_DOXBENCH_MSG_TURN_IN_FLIGHT = "a turn is already in flight for this conversation"
_DOXBENCH_MSG_TURN_SCOPE_REFUSED = "the requested scope could not be confirmed"
_DOXBENCH_MSG_CONTENT_IDENTITY_MISMATCH = "the submitted content does not match its declared identity"
_DOXBENCH_MSG_MODEL_UNAVAILABLE = "the requested model is not available"
_DOXBENCH_MSG_INVALID_TURN_REQUEST = "the turn request is malformed"
_DOXBENCH_MSG_INVALID_ABSTRACT_REQUEST = "the abstract request is malformed"
_DOXBENCH_MSG_ABSTRACT_UNAVAILABLE = (
    "the abstract request could not be assembled safely")
_DOXBENCH_MSG_MODEL_TIMEOUT = "the model did not answer within the declared timeout"
_DOXBENCH_MSG_MODEL_FAILED = "the model request failed"
_DOXBENCH_MSG_RESPONSE_INVALID = "the model response could not be validated"
_DOXBENCH_MSG_CONTEXT_PACKET_INVALID = (
    "the bounded context for this turn could not be confirmed")
_DOXBENCH_MSG_CONTEXT_PACKET_BOUND_EXCEEDED = (
    "this session's own thread material exceeds the bounded context a turn may "
    "carry; compacting the thread brings it back inside the bound")
# The THIRD declared cause for an absent thread, beside `doxbench_threads`'
# hosted-plane and no-gate-capability pair. It belongs here rather than there
# because it is a fact about THIS serve's session registry, not about the
# thread format — and it is deliberately generic: a cause naming the ref or the
# tile would make this route an oracle for which of them exist.
NO_LIVE_SESSION_CAUSE = (
    "no branch session is open for this scope, so there is no session worktree "
    "for a thread to live in")

# The FOURTH declared cause (PR #223, Copilot CP1). An unresolved actor used to
# borrow the no-gate-capability cause, which is a true sentence about a
# different situation — the plane HAS the capability, there is simply no
# identified human to attribute a gate action to. Exactly the class this
# slice's own P3-19 fixed for the no-live-session branch, missed one clause
# over.
NO_RESOLVED_ACTOR_CAUSE = (
    "this console resolved no human actor, and a thread is one human's working "
    "memory on a session branch — so there is nobody to attribute it to")

_DOXBENCH_MSG_THREAD_CAPABILITY_UNAVAILABLE = (
    "threads exist only where branch sessions exist")
_DOXBENCH_MSG_INTAKE_REFUSED = (
    "model intake refused and stored nothing")
_DOXBENCH_MSG_INVALID_INTAKE_REQUEST = (
    "the intake request does not declare what this flow needs")
_DOXBENCH_MSG_APPROVAL_REFUSED = (
    "the model approval refused and recorded nothing")
_DOXBENCH_MSG_UNRECOGNIZED_TURN_KIND = (
    "this route does not serve the chat-turn kind the request declared")

# THE ONE CAUSE-NAMING ALTERNATE, and deliberately NOT a catalog entry.
#
# `invalid_turn_request` answers every way a well-formed JSON object can fail the
# released envelope, so its catalog message has to hold for all of them and
# therefore says only that the request is malformed. True, and useless for the
# one violation a HUMAN reaches by hand: unloading the set down to the outline
# and sending, which trips `request`/`request_v2`.`buffers`' `minItems: 2` floor.
# The refusal was correct in class and named nothing actionable, while the
# actionable half sat a few pixels away in the selector's empty state
# (`LOADED_SELECTOR_EMPTY_NOTE`, web/views/doxbench-chat.js) -- recorded as a
# follow-up in add-doxbench-editing-phase-b's Amendment 2, which RULED that this
# act refuses at send, visibly, rather than being made unreachable. This message
# is the send-side half of that ruling, and it deliberately echoes the selector's
# own sentence so the two surfaces say the same thing about the same state.
#
# WHY A MESSAGE, AND NOT A CODE OR A FIELD. The code is unchanged because the
# CLASS is unchanged: the request really is malformed against the release. A
# `cause` key beside it -- the shape `thread_capability_unavailable` uses -- is
# not available here: both released failure envelopes are
# `additionalProperties: false` over exactly `{schema_version, kind,
# client_turn_id, error, message, limit}`, so a body carrying one would fail
# `_refuse_turn`'s own self-validation and fall back to the pre-identity shape.
# The released `message` is free-form (`type: string, minLength: 1,
# maxLength: 500` -- no `const`, no `enum`, no `pattern`), so saying something
# more useful in it costs no schema byte, hence no digest refresh in
# `doxbench_contracts.SCHEMA_DIGESTS` and no contract release.
#
# It stays a FIXED module-level constant composed from nothing the caller sent,
# exactly like every catalog message: the choice BETWEEN the two strings is made
# from the SHAPE of the violation, never from its content.
_DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT = (
    "the turn carries no document beside the outline — use a docs tile's load "
    "verb to work on one")

# code -> (HTTP status, fixed caller-safe message). `request_limit_exceeded`'s
# 413 (Payload Too Large) is this slice's own judgement call: the planning
# contracts do not pin an HTTP status for it the way model-catalog.md's table
# pins the other three (403/403/500).
DOXBENCH_ERROR_CATALOG: dict[str, tuple[int, str]] = {
    DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED: (413, _DOXBENCH_MSG_REQUEST_LIMIT_EXCEEDED),
    DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE: (403, _DOXBENCH_MSG_MODEL_CAPABILITY_UNAVAILABLE),
    DOXBENCH_ERR_CATALOG_UNAVAILABLE: (500, _DOXBENCH_MSG_CATALOG_UNAVAILABLE),
    DOXBENCH_ERR_CONSOLE_REQUIRED: (403, _DOXBENCH_MSG_CONSOLE_REQUIRED),
    # turn_id_conflict: 409, spelling VERBATIM in contracts/chat-turn.md.
    DOXBENCH_ERR_TURN_ID_CONFLICT: (409, _DOXBENCH_MSG_TURN_ID_CONFLICT),
    # turn_in_flight: judgement-call spelling; the BEHAVIOUR is mandated
    # (contract's "attach/wait or safe in-flight response", spec's "an
    # in-flight repeat SHALL attach to or report that turn", FR-018) but the
    # packet pins no code spelling or status for it.
    DOXBENCH_ERR_TURN_IN_FLIGHT: (409, _DOXBENCH_MSG_TURN_IN_FLIGHT),
    # turn_scope_refused: judgement-call spelling; covers the contract's
    # preconditions 3/4/5 as ONE fail-closed refusal so no response is an
    # oracle about which repositories, refs, tiles, or paths exist.
    DOXBENCH_ERR_TURN_SCOPE_REFUSED: (403, _DOXBENCH_MSG_TURN_SCOPE_REFUSED),
    # content_identity_mismatch: judgement-call spelling; precondition 6, the
    # stale-input class.
    DOXBENCH_ERR_CONTENT_IDENTITY_MISMATCH: (409, _DOXBENCH_MSG_CONTENT_IDENTITY_MISMATCH),
    # model_unavailable: judgement-call spelling; precondition 7 plus
    # spec.md's "a model becomes unavailable after selection but before
    # submission" edge case.
    DOXBENCH_ERR_MODEL_UNAVAILABLE: (409, _DOXBENCH_MSG_MODEL_UNAVAILABLE),
    # invalid_turn_request: judgement-call spelling; known-field shape and
    # blank message.
    DOXBENCH_ERR_INVALID_TURN_REQUEST: (400, _DOXBENCH_MSG_INVALID_TURN_REQUEST),
    # invalid_abstract_request: 400, this slice's own spelling and status,
    # mirroring the turn code above for the route beside it.
    DOXBENCH_ERR_INVALID_ABSTRACT_REQUEST: (
        400, _DOXBENCH_MSG_INVALID_ABSTRACT_REQUEST),
    DOXBENCH_ERR_ABSTRACT_UNAVAILABLE: (500, _DOXBENCH_MSG_ABSTRACT_UNAVAILABLE),
    # T051 dispatch outcomes (spellings from doxbench_model's closed set;
    # statuses are this slice's judgement calls): 504 for the deadline
    # outcome (gateway-timeout semantics), 502 for an adapter failure and
    # for provider output the validator refused (bad-gateway semantics: the
    # upstream answered, unusably). Fixed messages, like every entry above.
    DOXBENCH_ERR_MODEL_TIMEOUT: (504, _DOXBENCH_MSG_MODEL_TIMEOUT),
    DOXBENCH_ERR_MODEL_FAILED: (502, _DOXBENCH_MSG_MODEL_FAILED),
    DOXBENCH_ERR_RESPONSE_INVALID: (502, _DOXBENCH_MSG_RESPONSE_INVALID),
    # 500: the server produced a bounded context it could not then use. No
    # request the caller could send would fix it, so a 4xx would misdirect.
    DOXBENCH_ERR_CONTEXT_PACKET_INVALID: (
        500, _DOXBENCH_MSG_CONTEXT_PACKET_INVALID),
    # 409: the turn conflicts with the current state of the session's own
    # threads. Not 413 -- the REQUEST is not too large, the session's working
    # memory is -- and the caller CAN act on it, which is what makes 409 right:
    # compacting the thread is layer two, and it exists for exactly this.
    DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED: (
        409, _DOXBENCH_MSG_CONTEXT_PACKET_BOUND_EXCEEDED),
    # 403: a capability verdict, the same status and the same class as
    # `model_capability_unavailable`. The two DECLARED causes — the hosted
    # plane, and a plane with no gate capability — ride the body's `reason`
    # field, and both are fixed module-level strings from `doxbench_threads`.
    DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE: (
        403, _DOXBENCH_MSG_THREAD_CAPABILITY_UNAVAILABLE),
    # 409: the request was well-formed and the SERVER's declared posture refused
    # it — the same status `model_unavailable` carries for the same reason.
    DOXBENCH_ERR_INTAKE_REFUSED: (409, _DOXBENCH_MSG_INTAKE_REFUSED),
    DOXBENCH_ERR_INVALID_INTAKE_REQUEST: (
        400, _DOXBENCH_MSG_INVALID_INTAKE_REQUEST),
    DOXBENCH_ERR_APPROVAL_REFUSED: (409, _DOXBENCH_MSG_APPROVAL_REFUSED),
    # 400: the request named a chat-turn kind this release does not serve.
    # Registered HERE and not merely spelled above, because this catalog raises
    # on an unregistered code -- an unregistered unknown-kind code would fault
    # the refusal path rather than refuse (retire-doxbench-chat-turn-v1,
    # "The new code is not registered").
    DOXBENCH_ERR_UNRECOGNIZED_TURN_KIND: (
        400, _DOXBENCH_MSG_UNRECOGNIZED_TURN_KIND),
}

# The codes whose released envelope may carry the `limit` block. The released
# failure envelope allows `limit` on any code; this set is the SERVER's own
# rule about which refusals are dimension-bearing, kept in one place so the two
# body builders cannot disagree about it.
DOXBENCH_LIMIT_BEARING_CODES: frozenset[str] = frozenset({
    DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
    DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED,
})


# The sidecar format is LF-ONLY (`doxbench_threads._validated_body` refuses a
# carriage return), and the wire carries whatever the browser and the provider
# produced. Normalising HERE — at the one place a turn becomes a record — is
# what keeps a CRLF answer storable instead of refused, and it is a
# normalisation rather than an edit: the bytes the model returned still ride the
# response envelope unchanged.
def _sidecar_text(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def _no_dereference(value: str) -> str:
    """The dereference seam a serve with NO bridge supplies: it resolves
    nothing, so a body still carrying a harness pointer is refused by
    `ThreadTurn` rather than persisted. Fail-closed, which is task 3.5's own
    verdict — an unresolvable pointer in a shared sidecar is worse than an
    unrecorded turn."""
    return value


def _thread_absence_body(reason: str) -> dict:
    """The thread route's absence body: the FIXED catalog message, plus the
    DECLARED cause. Both are module-level constants — `doxbench_threads` owns
    the reason strings — so nothing request-derived reaches the wire."""
    body = doxbench_error_body(DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE)
    body["reason"] = doxbench_threads.THREAD_CAPABILITY_ABSENT_REASON
    body["cause"] = reason
    return body


def doxbench_error_body(code: str, *, limit: dict | None = None) -> dict:
    """The fixed doxBench wire body for `code` — a PURE module-level function,
    testable with no handler and no server. Keys are a fixed allowlist: `ok`,
    `error`, `message`, and — ONLY for `request_limit_exceeded` — a `limit`
    block REBUILT from exactly three named fields (`dimension` cast to `str`,
    `measured` and `maximum` cast to `int`), so nothing request-derived can
    ever splice an extra key into the response regardless of what a caller
    passes in `limit`. NO `schema_version`, NO `kind`: those are fields of the
    future RELEASED openxFactory schemas — the deliberate, recorded deferral
    the section banner above states."""
    _, message = DOXBENCH_ERROR_CATALOG[code]
    body: dict = {"ok": False, "error": code, "message": message}
    if code in DOXBENCH_LIMIT_BEARING_CODES and limit is not None:
        body["limit"] = {
            "dimension": str(limit["dimension"]),
            "measured": int(limit["measured"]),
            "maximum": int(limit["maximum"]),
        }
    return body


def doxbench_error_status(code: str) -> int:
    """The fixed HTTP status for `code` (companion to `doxbench_error_body`,
    mirroring `action_errors.ERROR_CATALOG`'s status half)."""
    return DOXBENCH_ERROR_CATALOG[code][0]


# ---- the distilled abstract's STATED refusals (add-doxbench-distilled-abstract
# §5; ratified: "A verification failure SHALL be a stated refusal that renders no
# abstract, and MUST NOT be silently downgraded to rendering the unverified
# text") ----
#
# A DIFFERENT KIND OF REFUSAL from the catalog above, and the difference is what
# a reader sees. The codes above are verdicts about the PLANE, the TRANSPORT or
# the PROVIDER, and each carries one fixed sentence because nothing
# request-derived may reach them. These are verdicts about THE ABSTRACT ITSELF:
# the region renders a stated reason IN PLACE OF a distillation, so the reason has
# to say which document and why, and it is rendered rather than logged.
#
# WHO OWNS WHICH CLASS. `doxbench_knowledge` owns the six VERIFICATION classes and
# composes their reasons -- it is the verifier, and a route restating its
# sentences would be a second spelling of one rule. This module adds only the
# classes the ROUTE itself decides, and their reasons are FIXED module-level
# strings composed from nothing the caller sent.
DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_ELIGIBLE = "subject-not-eligible"
DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_DISTILLABLE = "subject-not-distillable"
DOXBENCH_ABSTRACT_REFUSED_SUBJECT_BYTES = "subject-too-large"
DOXBENCH_ABSTRACT_REFUSED_PROSE_BYTES = "abstract-too-long"

# One statement covering BOTH ways a subject can fail eligibility -- outside this
# scope entirely, and inside it but readable-only -- and deliberately not an
# oracle about which: `editable_paths` is fed only from sections flagged `owned`
# (doxbench_scope.py:356-358), and the standing rule is that disclosure requires
# edit authority (doxbench_scope.py:390, enforced at doxbench_turns.py:585-591).
_ABSTRACT_REASON_NOT_ELIGIBLE = (
    "this document is not one of this scope's editable documents, and on this "
    "surface disclosure requires edit authority, so no distillation is "
    "available for it")
# Refused BEFORE dispatch rather than after: the verifier's coverage base is the
# snapshot's declared topics and destinations, so a subject declaring neither
# could only ever come back as `no-declared-base` -- and spending a provider call
# to learn that would be spending it on a question already answered.
_ABSTRACT_REASON_NO_DECLARED_BASE = (
    "the snapshot declares no topics and no destinations for this document, so "
    "subject-mention coverage has no base and a distilled abstract could not be "
    "verified against anything the document itself declares")
_ABSTRACT_REASON_NOT_DISTILLABLE = (
    "this document carries nothing to distil, so the region states the absence "
    "rather than asking a model to invent one")
_ABSTRACT_REASON_SUBJECT_BYTES = (
    "this document is larger than the byte bound one abstract request may "
    "carry, so no distillation is available for it")


def _abstract_reason_prose_bytes(measured: int, maximum: int) -> str:
    """The ONE abstract reason composed per refusal rather than fixed, and it
    NAMES BOTH NUMBERS.

    "Too long" is a verdict a reader cannot act on. The first real operator run
    (2026-08-26) refused a 2_018-byte answer against the 1_500-byte bound and
    the region could say only that something was over-long -- so nothing in the
    surface told the operator how far over, or what the bound even was, and the
    diagnosis had to be made from the server's own source.

    The two values spliced here are SERVER MEASUREMENTS: integers this process
    computed over the provider's answer, carried by `TurnLimitError`, which
    holds the dimension and the two numbers and never the text it measured. The
    section rule above -- composed from nothing the caller sent -- holds
    exactly: no caller field and no provider text reaches this string."""
    return (
        "the model answered with " + str(int(measured)) + " bytes of prose "
        "and this region renders at most " + str(int(maximum)) + ": an "
        "over-long answer is refused in full rather than trimmed into it, "
        "because text cut to fit is text no model wrote and no verifier "
        "checked")


# code -> HTTP status. The three 502s are the `response_invalid` class by another
# name -- the upstream answered, unusably -- and they are the statuses the chat
# route already gives that class. The two 409s say something different and truer:
# nothing the caller could resend would help, but the state of the DOCUMENT can
# change (an edit gives it declared fields, or brings it inside the bound) and
# then the same request succeeds. The 403 is a capability-shaped verdict about
# authority over this subject, the same status class as every other refusal on
# this surface that is about what the caller may reach.
DOXBENCH_ABSTRACT_REFUSAL_STATUS: dict[str, int] = {
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_ELIGIBLE: 403,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_DISTILLABLE: 409,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_BYTES: 409,
    DOXBENCH_ABSTRACT_REFUSED_PROSE_BYTES: 502,
    doxbench_knowledge.ABSTRACT_REFUSED_EMPTY: 502,
    doxbench_knowledge.ABSTRACT_REFUSED_NO_DECLARED_BASE: 409,
    doxbench_knowledge.ABSTRACT_REFUSED_FOREIGN_PATH: 502,
    doxbench_knowledge.ABSTRACT_REFUSED_SUBJECT_NOT_NAMED: 502,
    doxbench_knowledge.ABSTRACT_REFUSED_COVERAGE: 502,
    doxbench_knowledge.ABSTRACT_REFUSED_PREVIOUS_COVERAGE: 502,
}


def doxbench_abstract_refusal_body(code: str, reason: str, *, subject_path: str,
                                   subject_digest: str | None = None,
                                   caption_state: str = doxbench_knowledge.CAPTION_NOT_YET_GENERATED,
                                   wait_bound_seconds: float | None = None) -> dict:
    """The abstract route's STATED-refusal body -- a PURE module-level function,
    testable with no handler and no server.

    THE KEY SET IS FIXED AND CARRIES NO PROSE. That is structural rather than a
    rule someone must remember: a refusal renders nothing, so there is no field a
    downstream surface could silently downgrade the refused text into. The
    verifier gives the same guarantee at its own boundary -- `AbstractRefused`
    has no prose field -- and this shape keeps it on the wire.

    `subject_digest` is `None` where the route refused BEFORE reading the
    subject's saved bytes (an ineligible subject is refused before any
    disclosure), and `wait_bound_seconds` is `None` where it refused before
    resolving the adapter."""
    if code not in DOXBENCH_ABSTRACT_REFUSAL_STATUS:
        raise KeyError(code)
    return {"ok": False, "refused": code, "reason": reason,
            "caption_state": caption_state, "subject_path": subject_path,
            "subject_digest": subject_digest,
            "wait_bound_seconds": wait_bound_seconds}


def doxbench_abstract_refusal_status(code: str) -> int:
    """The fixed HTTP status for one stated abstract refusal (companion to
    `doxbench_abstract_refusal_body`)."""
    return DOXBENCH_ABSTRACT_REFUSAL_STATUS[code]


# THE KIND THE ABSTRACT'S OWN CONVERSATION IS COMPOSED UNDER, and it is
# deliberately NOT `doxbench_bridge.CONVERSATION_KEY_KIND`. A distillation is
# not a chat turn: it must not land in the chat's session (the envelope's claim
# is that the model was shown ONE subject and no other material), and the chat
# must not land in the abstract's either. Two kinds is what keeps the two apart
# no matter how the rest of the key is spelled.
DOXBENCH_ABSTRACT_CONVERSATION_KIND = "doxbench-abstract"


def doxbench_abstract_conversation_key(scope, subject_path: str) -> str:
    """The conversation ONE abstract generation binds its harness session under
    -- a PURE module-level function (adversarial review 2026-08-25, B1).

    WHY THE ABSTRACT BINDS AT ALL. `OmpHarnessBridge.dispatch` is
    `_dispatch_bound(None, ...)`: on a fresh process it REFUSES an unbound turn
    outright, and once any turn has bound a session it runs inside whichever
    conversation the harness was last switched to. The abstract route used to
    hand the raw port to `_deadline_bound_dispatch`, so on a real install the
    first generation of a session could only fail -- and every generation after a
    chat turn would have been prompted INSIDE that document's chat session,
    against design 5.2's one-session-per-thread rule and against this route's own
    envelope contract.

    WHY ITS OWN KEY RATHER THAN THE DOCUMENT THREAD'S. Reusing
    `conversation_key(scope, subject_path)` would fix the refusal and keep the
    contamination, in the other direction: the abstract prompt would join the
    document thread's conversation and every later chat turn on that document
    would carry it.

    COMPOSED AS JSON, for the reason `OmpHarnessBridge.conversation_key` states:
    a separator has to be a character no component can contain, and a repository
    name, a ref, a tile id and a document path can contain almost anything JSON
    escaping makes injective by construction. It is an internal session key and
    an error string, never a wire value."""

    return json.dumps([
        DOXBENCH_ABSTRACT_CONVERSATION_KIND,
        str(getattr(scope, "repository", "")),
        str(getattr(scope, "ref", "")),
        str(getattr(scope, "tile_kind", "")),
        str(getattr(scope, "tile_id", "")),
        str(subject_path),
    ], ensure_ascii=False)


def doxbench_abstract_success_body(abstract, *,
                                   wait_bound_seconds: float | None) -> dict:
    """The verified abstract's wire body -- a PURE module-level function.

    THE ECHO IS THE POINT (task 5.6, design D6). The body names the subject path
    and the content digest this abstract was generated FOR, so a result resolving
    against a subject the pane no longer has selected is discarded unrendered
    instead of painting itself over whatever the reader has since spun to, under
    a confident caption.

    `caption_state` comes from the artifact's own `caption_state_for`, never from
    a literal here: the five ruled captions are `doxbench_knowledge`'s
    vocabulary, and a sixth spelling in a third file is how five strings become
    six. `generation` is the store's own increasing counter and never a clock --
    `DocumentAbstract` refuses a clock reading in that field by construction.

    NO `schema_version`, NO `kind`: no released openxFactory schema declares an
    abstract shape, so this carries the same unversioned console-internal shape
    `/capabilities` and the thread read route carry. Inventing a `schema_version`
    here would claim a release nobody cut."""
    return {"ok": True,
            "subject_path": abstract.subject_path,
            "subject_digest": abstract.subject_digest,
            "model_id": abstract.model_id,
            "prose": abstract.prose,
            "caption_state": abstract.caption_state_for(
                current_digest=abstract.subject_digest),
            "generation": abstract.generation,
            "wait_bound_seconds": wait_bound_seconds}


def doxbench_declared_fields(snapshot, subject_path: str):
    """The SNAPSHOT'S OWN declared topics and destinations for one document, as
    `(topics, lands)` -- the abstract's verification base, and the two fields its
    prompt header states.

    The destinations object is FLATTENED here into the surface's own
    `kind: name` lands (`staging-workbench-model.js:1566-1571`) rather than
    passed through as a mapping. The assembler renders one line per declared
    value and refuses a non-string; the verifier accepts either shape. Flattening
    at the one place that reads the snapshot keeps the base the verifier checks
    and the header the model reads spelled identically, which is the whole point
    of the coverage rule.

    Anything that is not a one-line string is SKIPPED rather than rendered: a
    line break in a declared value would forge a header field, and the assembler
    refuses one -- so a malformed snapshot value must not be able to turn a
    readable document into a 500."""
    documents = snapshot.get("documents") if isinstance(snapshot, dict) else None
    document = None
    for raw in documents or ():
        if isinstance(raw, dict) and raw.get("path") == subject_path:
            document = raw
            break
    if document is None:
        return (), ()

    def _lines(values):
        return tuple(value for value in values
                     if isinstance(value, str) and value.strip()
                     and "\n" not in value and "\r" not in value)

    topics_raw = document.get("topics")
    topics = _lines(topics_raw if isinstance(topics_raw, list) else ())
    lands: list[str] = []
    destinations = document.get("destinations")
    if isinstance(destinations, dict):
        for kind, names in destinations.items():
            if not isinstance(kind, str):
                continue
            for name in (names if isinstance(names, list) else ()):
                if isinstance(name, str) and name.strip():
                    lands.append(kind + ": " + name)
    return topics, _lines(tuple(lands))


# ---- the RELEASED chat-turn failure envelope (T024/T051 wire clause) ----
#
# `contracts/model-catalog.md` keeps the CATALOG route's failures on the
# pre-existing `{ok, error, message}` shape — the release publishes no catalog
# failure envelope — while `xfactory-workbench-chat-turn.schema.yaml` DOES
# publish one, closed, requiring a `client_turn_id` of 1..128 characters and
# admitting no `ok` key at all. Two consequences, both deliberate:
#
#   * a chat failure emitted AFTER the request validated against the released
#     schema carries the released envelope (and therefore no `ok`), because at
#     that point the turn identity is known AND known to be in bounds; and
#   * a chat refusal emitted BEFORE that point — the plane gate, the console
#     gate, the route-specific body bound, a body that is not a JSON object,
#     and the schema refusal itself — keeps `doxbench_error_body`'s fixed
#     shape, because the released envelope has no representation for "a
#     failure with no validated turn identity" and fabricating a
#     `client_turn_id` would hand the browser a correlation key for a turn the
#     server never accepted. Refusing to invent one is the fail-closed
#     direction; the code and fixed message are identical either way.

def doxbench_turn_failure_body(code: str, client_turn_id: str, *,
                               limit: dict | None = None,
                               kind: str = DOXBENCH_CHAT_TURN_V2_FAILURE_KIND,
                               message: str | None = None) -> dict:
    """The RELEASED `workbench-chat-turn-v2-failure` envelope for `code` — a
    PURE module-level function, testable with no handler and no server.

    Keys are the released allowlist: `schema_version`, `kind`,
    `client_turn_id`, `error`, `message`, and — ONLY for
    `request_limit_exceeded` — the `limit` block, REBUILT from exactly three
    named fields exactly as `doxbench_error_body` rebuilds it, so nothing
    request-derived can splice a key into a response. The message defaults to the
    same fixed module-level constant the pre-release shape used; only the
    envelope changed.

    `kind` NAMES the failure envelope this refusal is answered in. It survives
    as a parameter, with the one served family as its default, rather than being
    inlined at contract-v3.0: the released `kind` is a value the CALLER of this
    pure builder states, and a builder that hard-coded it would have to be
    edited again the next time a second family is served. Until contract-v3.0 it
    selected BETWEEN two co-resident families and defaulted to the deprecated
    one; there is now one, and every caller reaches it through `_refuse_turn`.

    `message` overrides the catalog's message for THIS refusal. The contract on
    every caller is that it passes a FIXED module-level constant and never
    anything derived from the request -- the released `message` is free-form, but
    the redaction posture that keeps a refusal from being an oracle is a property
    of the callers, not of the schema. Today every caller reaches this through
    `_refuse_turn`, and all of them pass `_doxbench_invalid_turn_message`'s
    verdict -- one of exactly two module-level constants; see
    `_DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT` for the full record. `None` means the
    catalog's own message, so every other refusal is byte-identical to before.

    ENFORCED, not merely documented (Copilot review, PR #255). Only an actual
    `str` overrides; anything else falls back to the catalog string. The earlier
    `str(message)` would have coerced whatever it was handed, so a caller that
    one day passed an exception, a response object, or a validation error --
    every one of which stringifies to something that can carry request content --
    would have spliced that content into a published refusal while this docstring
    still claimed refusals disclose nothing. A type is a cheap thing to check and
    the posture is too expensive to lose to a future caller's slip.

    An EMPTY string falls back too. It is not a disclosure risk, but the released
    envelope requires `minLength: 1`, so letting it through would fail
    `_refuse_turn`'s self-validation and cost the refusal its `client_turn_id` --
    the browser's only means of correlating it. One more condition buys a
    correlatable refusal instead of an anonymous one.

    QUIET, like every neighbouring fail-closed seam: `_wire_valid_turn_id`
    answers a bad type with None and `_doxbench_wire_conforms` answers one with
    False, rather than raising. This is on the RESPONSE path of a refusal, where
    an exception would drop the connection and strand the turn's lease -- the
    exact failure `test_a_v1_turn_whose_document_path_claims_the_outline_key_is_refused`
    exists to forbid ("the connection must carry an envelope, never drop"). The
    caller still gets a true, conformant refusal; it just gets the general one."""
    _, catalog_message = DOXBENCH_ERROR_CATALOG[code]
    body: dict = {
        "schema_version": DOXBENCH_WIRE_SCHEMA_VERSION,
        "kind": str(kind),
        "client_turn_id": str(client_turn_id),
        "error": code,
        "message": (message if isinstance(message, str) and message
                    else catalog_message),
    }
    if code in DOXBENCH_LIMIT_BEARING_CODES and limit is not None:
        body["limit"] = {
            "dimension": str(limit["dimension"]),
            "measured": int(limit["measured"]),
            "maximum": int(limit["maximum"]),
        }
    return body


# The v1 success builder `doxbench_turn_success_body` stood here until
# contract-v3.0 (retire-doxbench-chat-turn-v1). It built the deprecated
# `workbench-chat-turn-success` envelope -- the two-key `observed_hashes`
# shape, an `enum` proposal target, no `selected_model`, no
# `context_packet`, no `provider_retry` -- and its two RECORDED v1
# limitations went with it. `doxbench_turn_success_v2_body` below is the
# one success builder, and the migration path the CHANGELOG names.


def doxbench_selected_model(model_entry) -> dict:
    """The SELECTED-MODEL metadata a widened record carries, derived from the
    catalog entry the turn resolved — in ONE place (adversarial review of the §13
    slice, F6).

    SINCE contract-v1.38 (task 11.7) a conformant catalog entry CAN declare
    itself a routing rule, and this function needed no change to report one:
    it reads the entry duck-typed and defaults honestly, so an entry declaring
    nothing still answers `routing_rule` false with the chosen model as the
    answering model. Being one function rather than three literals at the call
    site is what made that true — and it is also why the release's reviewer
    could find, in one place, that the SIDECAR was being handed the requested id
    while the wire record carried the resolved one (F3).

    Its CONSUMERS are now the v2 wire record, the thread sidecar's turn header,
    and -- since add-doxbench-distilled-abstract §5 -- the distilled abstract,
    which records the ANSWERING model on the artifact it verifies for exactly the
    reason the routing-rule scenario gives: a reader must be able to learn which
    model actually answered, and `auto` is not one. The deprecated v1 success
    envelope does NOT consult it: that envelope has room for exactly one model id
    and cannot state both facts, which is recorded as a v1 limitation rather than
    papered over."""
    requested = str(model_entry.model_id)
    routing_rule = bool(getattr(model_entry, "routing_rule", False))
    resolved = getattr(model_entry, "resolved_model_id", None)
    return {
        "requested_model_id": requested,
        "routing_rule": routing_rule,
        "data_handling": str(model_entry.data_handling),
        # The model that ANSWERS. Equal to the requested id until a routing-rule
        # entry resolves to something else, which is exactly when the two facts
        # stop being one fact.
        "resolved_model_id": str(resolved) if resolved else requested,
    }


# The released `context_packet.reduced_reason` ceiling, restated here as a
# literal because this module does not parse the schema per turn — the
# `MAX_ROUTING_TARGETS` precedent from contract-v1.38, and it is authoritative
# for the same reason: a test reads the bound out of the RELEASED BYTES and pins
# it equal, so the two cannot drift into two ceilings.
#
# THE UNIT IS CODE POINTS, exactly as JSON Schema's `maxLength` counts them, so
# this guard refuses precisely what the shape refuses and nothing more. A
# 500-code-point CJK reason is 1,500 UTF-8 bytes and is CONFORMANT; refusing it
# for its byte count would refuse a record the released contract accepts.
# (The shipped `REDUCED_*` constants are separately held to the stricter BYTE
# count by a test — a belt on authored text this repository controls, not a
# rule the wire imposes.)
CONTEXT_REDUCED_REASON_MAX_LENGTH = 500


def doxbench_context_packet(packet) -> dict:
    """The ASSEMBLED CONTEXT's posture, as the widened record carries it since
    contract-v1.40 (task 10.7) — derived in ONE place, from the packet the turn
    ACTUALLY RAN UNDER, on `doxbench_selected_model`'s precedent one function up.

    The ratified sentence is *"Where the knowledge service is unavailable the
    turn SHALL degrade to a declared reduced packet … with the reduced posture
    STATED"*. Until v1.40 it was stated only INSIDE the packet, where no reader
    of the record and no human on the surface could consult it. This is the one
    derivation that puts it on the wire, and it re-states the PACKET'S OWN
    values — never a re-derivation from "was there a knowledge service?", which
    would be a second authority that could disagree with the packet (the packet
    also reduces when a live backend REFUSES a retrieval, and only the packet
    knows which of the two happened).

    THE REASON IS CARRIED VERBATIM. `ContextPacket` already refuses a reduced
    packet with no reason and a full packet with one, so on the shipped path
    these refusals cannot fire — but the packet assembler is an INJECTED seam
    (`packet_assembler`), duck-typed like every other collaborator here, and a
    collaborator that handed back a packet declaring `full` beside a reduction
    would put a self-contradicting record on the wire and in the turn store.
    Refused as a `PacketError`, which the route's existing packet boundary maps
    to the fixed `invalid_turn_request` — fail-closed, never a guessed posture.
    A test drives each refusal through that seam.

    A RECORDED TENSION, not a resolved one (adversarial review S2). Every
    refusal in this function has a SERVER-AUTHORED cause — a collaborator that
    lied, or a reason constant this repository wrote too long — and none is
    fixable by any request a caller could send. The route's
    `context_packet_invalid` arm (500) exists for exactly that class and says so
    in as many words ("never a 4xx blaming the turn"), so `invalid_turn_request`
    (400) is arguably the wrong code for all four arms. They are kept on ONE
    code deliberately: one function, one refusal shape, and the four cases are
    unreachable in production (`ContextPacket` refuses three of them at
    construction and a test holds the constants under the fourth). Moving the
    whole function to the 500 arm is a follow-up, named here rather than
    smuggled into a fix pass that four tests already pin."""
    posture = getattr(packet, "posture", None)
    reason = getattr(packet, "reduced_reason", None)
    if posture == doxbench_packet.POSTURE_REDUCED:
        # A NON-EMPTY STRING, not merely something truthy (Codex review of
        # PR #256). `if not reason:` accepted any truthy value and `str(reason)`
        # then MANUFACTURED a reason out of it: `123` became `"123"`, a list
        # became `"['a', 'b']"`, and a bare `object()` became
        # `"<object object at 0x…>"` — a heap address, in a durable record, on
        # the degraded path. That is the same silent-normalisation class the
        # presence findings were: malformed collaborator output turned into a
        # conformant-LOOKING posture instead of a refusal. The released shape
        # says `type: string`, so this boundary says it too, and the reason is
        # carried VERBATIM rather than coerced.
        # NON-BLANK, not merely non-empty (issue #263). This read
        # `or not reason`, which is the released shape's `minLength: 1` — and
        # that bound counts CHARACTERS, so all nine recorded blank classes are
        # one character long and every one of them passed. `states_something`
        # is the family's rule, defined once in `doxbench_packet`; this
        # boundary IMPORTS it rather than restating it, so the type gate and
        # the server gate cannot drift into two spellings of one rule.
        if not states_something(reason):
            raise doxbench_packet.PacketError(
                "a reduced packet STATES the reduced posture's reason; a "
                "record cannot carry a reduction nobody can read")
        # THE RELEASED CEILING, ENFORCED WHERE THE REASON IS CARRIED
        # (adversarial review S2). Without this the only thing standing between
        # an over-long reason and the wire was the route's post-dispatch
        # self-validation, which the review reproduced: a 501-code-point reason
        # answered `response_invalid` (502) AFTER a provider dispatch had
        # already been paid for and the human's turn was already gone. Refusing
        # HERE is pre-dispatch, and it also covers a `REDUCED_*` constant added
        # later that nobody thought to hold to the bound.
        #
        # NOT TRUNCATED, ever: truncating a statement about a degradation is how
        # a degradation goes quiet, which is the failure this whole requirement
        # is written against.
        if len(reason) > CONTEXT_REDUCED_REASON_MAX_LENGTH:
            raise doxbench_packet.PacketError(
                "a reduction reason exceeds the released ceiling; the record "
                "refuses rather than truncating a statement about a "
                "degradation")
        return {"posture": posture, "reduced_reason": reason}
    if posture == doxbench_packet.POSTURE_FULL:
        # PRESENCE, NOT TRUTHINESS (Copilot review of PR #256, finding 1). This
        # arm used `if reason:`, so an EMPTY STRING passed it and the record was
        # emitted with the key omitted — a lying assembler handing
        # `{full, reduced_reason: ""}` was silently normalized instead of failing
        # closed. The released shape forbids the key's PRESENCE on a full posture
        # (`not: {required: [reduced_reason]}`), not its usefulness, so this
        # boundary has to mean the same thing the shape does.
        #
        # ASYMMETRIC WITH THE REDUCED ARM ABOVE, DELIBERATELY, and the shape is
        # asymmetric in exactly the same way: `reduced` REQUIRES a reason and
        # bounds it at `minLength: 1`, so a blank one is refused there for being
        # unusable; `full` refuses the field for being THERE. Do not "simplify"
        # these two into one predicate — they are two rules.
        if reason is not None:
            raise doxbench_packet.PacketError(
                "a full packet carries no reduction reason; a record cannot "
                "state both postures and let a reader pick")
        return {"posture": posture}
    raise doxbench_packet.PacketError(
        "a packet states its posture; a record cannot declare one the packet "
        "does not have")


def mint_ledger_snapshot(port) -> tuple:
    """A COPY of an adapter's mint ledger, or an empty tuple (task 3.6).

    DUCK-TYPED AND OPTIONAL, on purpose. `ledger` is not a port member and is not
    becoming one: the declared surface stays exactly the three members
    (`timeout_seconds`, `catalog`, `dispatch`), and an adapter that has no ledger
    — the local harness bridge, every test double, every future adapter — is not
    broken by this, it simply has no such fact to report. Absence is a posture
    here as it is everywhere else on this surface.

    A COPY rather than the list itself, because the server is a
    `ThreadingHTTPServer` and the port appends to that list from whichever thread
    is dispatching. A tuple taken now is a fact about now."""
    ledger = getattr(port, "ledger", None)
    if not isinstance(ledger, list):
        return ()
    return tuple(ledger)


def fresh_ledger_events(before: tuple, after: tuple) -> list:
    """The events APPENDED to a mint ledger between two snapshots.

    BY IDENTITY, NEVER BY EQUALITY, and PR #401's review found the reason.
    `doxbench_provider.MintEvent` is a FROZEN dataclass, so two DISTINCT events
    whose four fields coincide compare equal — and they coincide exactly when it
    matters most. A `paid_retry` event carries no `audit_ref` at all, so under a
    clock that returns the same value twice (a frozen test clock, a coarse
    timer, two turns inside one tick) the second turn's paid retry is
    field-for-field the first turn's. An `event not in before` test then filters
    it out as already-seen, `provider_retry_fact` answers None, and the second
    paid provider call that Brett's 2026-08-26 ruling requires to be VISIBLE is
    the one the human never sees. Identity cannot make that mistake: the port's
    `_record` constructs a fresh object per append, so no event object is ever
    two events.

    NOT POSITIONAL EITHER, which is the other obvious repair and is wrong here.
    THE LEDGER IS NOT STRICTLY APPEND-ONLY: it is append-only up to
    `doxbench_provider.MAX_LEDGER_EVENTS`, past which `_record` trims from the
    FRONT (`del self.ledger[:-MAX_LEDGER_EVENTS]`). A `ledger[before_len:]`
    slice reads NOTHING once the ledger sits at that bound — which is the state
    a long-lived console converges to, so the positional repair would fail in
    precisely the installs that dispatch the most turns. The invariant that
    actually holds is weaker and is enough: events are appended at the right and
    only ever dropped from the left, so an event present in `after` and absent
    from `before` was appended during the window, and one trimmed away is not in
    `after` to be counted twice.

    The `id()` set is safe here because `before` is a live tuple for this call's
    whole duration: nothing it holds can be collected, so no id can be recycled
    underneath the comparison."""
    if not before:
        return list(after)
    seen = {id(event) for event in before}
    return [event for event in after if id(event) not in seen]


def provider_retry_fact(before: tuple, after: tuple) -> dict | None:
    """THE MID-TURN RE-MINT, as the turn record states it (task 3.6), or None.

    Brett ruled on 2026-08-26 that when a minted token expires part-way through a
    turn the dashboard re-mints and retries ONCE, "with the re-mint and the paid
    retry VISIBLY RECORDED in the turn record" — because a second paid call the
    human cannot see is exactly the decision that ruling was made to avoid. The
    broker change built three real records of it (the port's content-free ledger,
    the console's stderr notice, and the broker's own audit trail correlated by
    `--retry-of`) and the BROWSER CAN READ NONE OF THEM. This function is how the
    fact crosses to the person paying for it.

    IT IS A DELTA, and the wording of the field it feeds is chosen to be true of
    a delta. The ledger is one object shared by every turn this process
    dispatches, and two conversations can dispatch concurrently, so what this
    measures is honestly "a re-mint and one further paid provider call happened
    WHILE THIS TURN WAS DISPATCHED" — not "this turn's own re-mint", which
    nothing short of a per-turn correlation the port does not carry could
    establish. On the single-operator loopback console this surface is gated to,
    with at most one turn in flight per conversation, the two coincide. The
    contract's own description says "while this turn was dispatched" for exactly
    this reason: a record that over-claimed would be worse than one that measures
    something slightly wider, and erring toward MORE visibility is the direction
    the ruling points.

    WHAT IT CARRIES: that it happened, that it happened at most once (the ruling's
    bound — a second expiry in one turn refuses instead of buying a third call,
    and that turn produces a failure envelope, not this one), and the re-mint's
    audit reference. Never the token, never a prefix of it, never the provider's
    words, never a status code. The audit reference is disclosable by
    construction: the broker's declaration records no token material against
    one."""
    from ideation_dashboard import doxbench_provider
    fresh = fresh_ledger_events(before, after)
    if not any(getattr(event, "reason", None) == doxbench_provider.REASON_PAID_RETRY
               for event in fresh):
        return None
    audit_ref = None
    for event in fresh:
        if getattr(event, "reason", None) == doxbench_provider.REASON_EXPIRY_REMINT:
            candidate = getattr(event, "audit_ref", None)
            if isinstance(candidate, str) and candidate.strip():
                audit_ref = candidate.strip()
    fact = {"retried": True, "at_most_once": True}
    if audit_ref is not None:
        fact["audit_ref"] = audit_ref
    return fact


def doxbench_turn_v2_success_body(*, client_turn_id: str, assistant_turn_id: str,
                                  model_id: str, requested_model_id: str,
                                  routing_rule: bool, data_handling: str,
                                  bound_buffer: str, observed_hashes: dict,
                                  assistant_prose: str, context_posture: str,
                                  context_reduced_reason: str | None = None,
                                  provider_retried: bool = False,
                                  provider_retry_audit_ref: str | None = None,
                                  proposals=()) -> dict:
    """The RELEASED `workbench-chat-turn-v2-success` envelope — the turn's
    durable RECORD (contract-v1.34; add-doxbench-editing-phase-b §13).

    Three things this envelope has room for that its predecessor did not, and
    each is REBUILT here from named values so nothing caller-derived can splice a
    key in:

    * `bound_buffer` — the binding the REQUEST DECLARED, carried through
      unchanged. Never derived from which document happened to be supplied: that
      derivation is the one Phase A's review killed, because it recorded "bound
      to the document" for a human working the outline with a document loaded.
    * `observed_hashes` keyed by BUFFER KEY, one per buffer the turn carried,
      rather than the two fixed names the v1 record could express.
    * `selected_model` — what the human CHOSE, beside `model_id`'s what
      ANSWERED. `routing_rule` is stated rather than inferred from the two ids
      being unequal, because "these differ" and "this entry is a routing rule"
      are different facts.

    …and, SINCE contract-v1.40 (task 10.7), a fourth:

    * `context_packet` — the POSTURE the turn's bounded context packet was
      assembled under, plus the reduction's reason when there is one. Rebuilt
      here from two named scalars for the same reason `selected_model` is: a
      caller handing in a ready-made dict could splice a key past the builder,
      and this envelope is closed. The posture is a REQUIRED argument, so no v2
      record can be built that silently omits it — the WIRE key is optional
      (that is what makes v1.40 additive), but this producer always states it,
      and a full turn's record says `full` explicitly rather than by omission.
      Omission on the wire means "a producer older than v1.40", never "full".

    Like its v1 sibling this builder is never the last word on conformance: the
    route self-validates the built envelope against the released schema before it
    is stored or sent."""
    # NO `str()` COERCION (issue #263, folded finding F5). This built
    # `{"posture": str(context_posture)}` and coerced the reason the same way,
    # which is the LAST coercion on the posture path — the others went when the
    # derivation stopped coercing, and this one was missed because its only
    # caller hands it values `doxbench_context_packet` has already validated.
    #
    # RESOLVED THE WAY THE DERIVATION RESOLVED ITS OWN, deliberately rather than
    # by inventing a second answer: REFUSE a non-string instead of manufacturing
    # one out of it. `str()` on a malformed value is how `<object object at
    # 0x…>` reaches a durable record — a heap address standing in for a posture.
    # The refusal is a `PacketError` on the same recorded 400-vs-500 tension the
    # derivation carries: the cause is server-authored and unreachable from any
    # request, and both refusals stay on ONE shape until that tension is
    # resolved for the whole path at once.
    if not isinstance(context_posture, str):
        raise doxbench_packet.PacketError(
            "a turn record states its context posture as the packet declared "
            "it; a coerced posture is a manufactured one")
    context_packet = {"posture": context_posture}
    if context_reduced_reason is not None:
        # TWO REFUSALS, NOT ONE (issue #263 review, P3-6). A non-string reason
        # and a blank one are different defects and had been folded into the
        # blank message, which told a reader "nobody can read this" about a
        # value that was never a string — the same manufactured-diagnosis class
        # the `str()` coercion was.
        if not isinstance(context_reduced_reason, str):
            raise doxbench_packet.PacketError(
                "a turn record carries the reduction's reason as the packet "
                "stated it; a coerced reason is a manufactured one")
        if not states_something(context_reduced_reason):
            raise doxbench_packet.PacketError(
                "a turn record carries the reduction's reason as the packet "
                "stated it; a reduction nobody can read is a silent "
                "degradation")
        context_packet["reduced_reason"] = context_reduced_reason
    # THE RE-MINT FACT (contract-v1.45, task 3.6). REBUILT here from two named
    # scalars, exactly as `context_packet` and `selected_model` are and for the
    # same reason: a caller handing in a ready-made dict could splice a key past
    # the builder, and this envelope is closed by `additionalProperties: false`.
    #
    # ABSENT WHEN IT DID NOT HAPPEN, never `retried: false`. The wire key is
    # optional — that is what makes contract-v1.45 additive — and a second,
    # weaker spelling of an absence that is already unambiguous is how a consumer
    # comes to read the wrong one.
    provider_retry = None
    if provider_retried:
        provider_retry = {"retried": True, "at_most_once": True}
        if provider_retry_audit_ref is not None:
            if not isinstance(provider_retry_audit_ref, str):
                raise doxbench_packet.PacketError(
                    "a turn record carries the re-mint's audit reference as the "
                    "broker stated it; a coerced reference is a manufactured "
                    "one")
            if not states_something(provider_retry_audit_ref):
                raise doxbench_packet.PacketError(
                    "a turn record carries the re-mint's audit reference as the "
                    "broker stated it; a reference nobody can read correlates "
                    "nothing")
            provider_retry["audit_ref"] = provider_retry_audit_ref
    return {
        "schema_version": DOXBENCH_WIRE_SCHEMA_VERSION,
        "kind": DOXBENCH_CHAT_TURN_V2_SUCCESS_KIND,
        "client_turn_id": str(client_turn_id),
        "assistant_turn_id": str(assistant_turn_id),
        "model_id": str(model_id),
        "selected_model": {
            "requested_model_id": str(requested_model_id),
            "routing_rule": bool(routing_rule),
            "data_handling": str(data_handling),
        },
        "context_packet": context_packet,
        **({"provider_retry": provider_retry} if provider_retry else {}),
        "bound_buffer": str(bound_buffer),
        "observed_hashes": {str(key): str(value)
                            for key, value in observed_hashes.items()},
        "assistant_prose": str(assistant_prose),
        "proposals": [
            {"target": str(p.target), "base_hash": str(p.base_hash),
             "summary": str(p.summary), "content": str(p.content)}
            for p in proposals
        ],
    }


# `build_server`'s sentinel for "the caller said nothing about validators".
# Distinct from None, which is a caller explicitly declaring NO validators.
_UNSET_VALIDATOR_FACTORY = object()


def default_doxbench_validators() -> dict:
    """Resolve the released doxBench schema validators from the PINNED
    openxFactory checkout (`doxbench_contracts.validators`).

    This is `build_server`'s default for the `schema_validator_factory` seam.
    It is a function, not an eager module-level load, so a server can be built
    on a plane with no checkout and simply refuse the two model routes rather
    than failing to start — and so the pin is re-verified per request rather
    than cached at import, which is what makes a mid-run repin observable.

    Raises whatever `doxbench_contracts` raises (`ContractPinError` on an
    unreachable checkout, an absent schema, a digest mismatch, a manifest
    disagreement, or a drifted `stack.yaml` ref). The caller
    (`_doxbench_validators`) turns any of those into a fail-closed route
    refusal: "I could not read the contract" is never an implicit pass."""
    from ideation_dashboard import doxbench_contracts
    return doxbench_contracts.validators()


AGENT_INVOCATION_REFUSAL = (
    "a session gate verb is human-only (FR-019) and this request does not come "
    "from the human console this serve started: it must be issued by the served "
    "page, same-origin, carrying this serve's console token")

