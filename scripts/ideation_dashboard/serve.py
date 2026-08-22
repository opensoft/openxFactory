"""Local backend for the ideation dashboard (plan "serve.py"; change task 3.3;
T011 + v2 local/served seam). Still a thin `http.server` shim, still loopback-
only for every write — but now the explicit LOCAL backend of the v2 seam, so it
grew its first write route. It serves:

  1. the static `web/` bundle (the renderer), with SimpleHTTPRequestHandler's
     own traversal defense over that tree;
  2. the ACTIVE generated snapshot at `/snapshot.json`, and any registered
     snapshot at `/snapshot.json?repository=<id>&ref=<ref>` — every snapshot is
     addressed through the ONE (repository, ref) registry
     (`snapshot_registry.py`, add-dashboard-repo-selector task 2.1), with `ref`
     defaulting to `main`, so a query-less request is exactly today's behaviour;
  2b. `GET /snapshot-index.json` — the snapshot INDEX composed from that
     registry (the openxFactory `ideation-dashboard-snapshot-index` locator plus
     additive serving-side freshness fields). This is the ONLY roster the
     repository selector reads; when the route is absent the renderer degrades
     to the single baked snapshot, which is what the static image does;
  3. a READ-ONLY `/source/<repo-relative-path>` pass-through returning file
     bytes from the pinned checkout (D15), and its keyed form
     `/source/<repository>@<ref>/<repo-relative-path>` which reads through THAT
     registry entry's own root (per-entry confinement, task 2.2). GET-only,
     confined to that entry's root, and rejecting every path-traversal attempt
     (`..`, encoded `..`, absolute paths, symlink escapes) with 404;
  4. `GET /capabilities` — a JSON capability probe (`{"actions": {...}}`)
     computed ONCE at startup. The static served image (nginx) never serves this
     route, so the UI probes once at load and hides every action affordance when
     the route is absent/404 or a capability is false;
  5. `POST /actions/notebook` — the "Open in NotebookLM" tile action (the first
     write route). LOOPBACK-ONLY: refused with 403 on a non-loopback bind. It
     resolves a tile's doc set and projects it into an `xf-wb-*` scratch
     notebook via the workbench NotebookAdapter, returning the notebook URL.
     Every failure is a structured JSON `{"error": <catalog code>, "message":
     <fixed string>}` drawn from `action_errors.ERROR_CATALOG` — request-
     derived data never enters a response, there is never a traceback, and
     never a hang (the adapter carries a subprocess timeout).
  6. `POST /actions/refresh` — ONE refresh affordance with TWO plane bindings
     (design D7), the binding chosen by the plane rather than by the client:
       * SERVED (a data source is declared): re-fetch the index and the active
         snapshot into the in-process derived cache and report the new
         freshness. Strictly READ-ONLY — fetching fresher derived data is a
         read, it writes nothing anywhere, and it is reachable off-loopback
         because that is the hosted refresh;
       * LOCAL (no data source, a real checkout): re-run the generator against
         the served checkout for one (repository, ref) and rewrite ONLY that
         derived snapshot artifact, through the interactivity boundary, with NO
         server restart. LOOPBACK-ONLY, and UNGATED on the `open-workbench`
         precedent — the snapshot is derived data, regeneration mutates nothing
         governed, and a gate record per regeneration would be audit noise about
         a cache (design D7 / open question 3's recommendation, stated here
         rather than inherited).
     Neither binding can trigger an image build, a rollout, or a publication:
     a serving surface dispatches recorded requests and never executes a final
     action (D1). A failed refresh leaves the previously rendered snapshot in
     place and reports inline.
  7. `POST /actions/edit` — the human select-to-edit escape hatch. It is
     available only on the loopback human console with a real checkout and
     resolved actor, requires the per-serve console token, resolves the selected
     document through the active registry entry's own source root, proves that
     the selected path is listed in that entry's snapshot, and launches the
     human's editor without modifying the document.

The `notebook` capability is TRUE only on a loopback bind with `nlm` on PATH and
a real (non-empty) checkout root — modelling the seam: the served static image
cannot hold `nlm` browser auth, so the action degrades to hidden there.

The `session` capability (007-workbench-branch-sessions T083, FR-048) is TRUE only
on a loopback bind with a real checkout and a RESOLVED HUMAN ACTOR, and the HOSTED
plane additionally refuses any request naming a non-`main` ref
(`hosted_ref_refused`, which also RECORDS the arrival path a hosted session would
one day take). Both halves are one decision: the session's remote-write identity is
the invoking engineer's own `gh` authentication (FR-034, D22), a personal
credential a hosted plane must never hold, and the port that uses it
(`_session_pull_requests`) is declared under exactly this capability.

Every snapshot/source response carries the snapshot↔checkout divergence, derived
from the snapshot's `generation.source_revision` versus the checkout's current
git HEAD (`X-Snapshot-Divergence: aligned|diverged|unknown`), so a viewer can
warn when the working tree has moved past the projected revision — plus the
active entry's freshness (`X-Snapshot-Repository`, `X-Snapshot-Ref`,
`X-Snapshot-Origin`, `X-Snapshot-Generated-At`, `X-Snapshot-Stale`), the
transport half of the freshness header the renderer displays (design D11).

Security posture: binds LOOPBACK only by default (127.0.0.1); every write route
is loopback-gated; the source route is read-only and confined PER REGISTRY ENTRY
(an entry with no declared root serves no documents at all); the actions
validate their request body and confine every path through the read-side guard
before touching the filesystem.

INVOCATION (design D12). This module is runnable BOTH as a script
(`python3 scripts/ideation_dashboard/serve.py …`, which is what the served
container image does) AND as a module (`python3 -m ideation_dashboard.serve`).
It self-inserts `scripts/` on the import path and uses ABSOLUTE
`ideation_dashboard.*` imports for its route collaborators; the old relative
`from . import …` imports 500'd every POST route under plain-script invocation,
and this change adds a POST route rather than carrying that workaround into it.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import secrets
import subprocess
import sys
import threading
import time
import traceback
import urllib.parse
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from ideation_dashboard import action_errors  # noqa: E402
from ideation_dashboard import doxbench_knowledge  # noqa: E402
from ideation_dashboard import doxbench_packet  # noqa: E402
from ideation_dashboard import doxbench_telemetry  # noqa: E402
from ideation_dashboard import doxbench_threads  # noqa: E402
from ideation_dashboard import snapshot_registry as registry_mod  # noqa: E402

DEFAULT_HOST = "127.0.0.1"
SNAPSHOT_ROUTE = "/snapshot.json"
SNAPSHOT_INDEX_ROUTE = "/snapshot-index.json"
# add-project-scoped-selection: the register projection the selector's project
# picker reads. The snapshot INDEX is a locator and deliberately carries no
# grouping, so the register itself — aggregation-owned, discovered upward from
# the checkout — is served read-only here. Absent register (or the static
# image, which never serves this route) -> 404 -> the picker hides and the
# selector degrades to today's ungrouped roster.
PROJECT_REGISTER_ROUTE = "/project-register.json"
SOURCE_PREFIX = "/source/"
CAPABILITIES_ROUTE = "/capabilities"
ACTIONS_NOTEBOOK_ROUTE = "/actions/notebook"
ACTIONS_REFRESH_ROUTE = "/actions/refresh"
# add-register-edit-lane: the header's apply button — the serve runs the
# fulfilment lane once (Brett's ruling: the click is the deliberate human
# act; only RECORDED commissions are ever applied, so D2's boundary holds).
ACTIONS_APPLY_REGISTER_EDITS_ROUTE = "/actions/apply-register-edits"
# add-shared-identity-seeds: DRAFT a DTN candidate-register seed from a
# repository-lens region. Read-only by construction — it returns TEXT the
# human merges and never opens the register for writing — so it is loopback-
# gated like every local action but needs NO gate capability, which is also
# what lets it answer from a composed (read-only) view.
ACTIONS_DTN_SEED_ROUTE = "/actions/dtn-seed"
# The STAGING-QUEUE seed: the same seed-first, write-nothing contract for a
# set of documents the human selected in the lens matrix. It drafts the
# fragment `ideation/staging/<topic>/` expects; the human places it.
ACTIONS_STAGING_SEED_ROUTE = "/actions/staging-seed"
ACTIONS_EDIT_ROUTE = "/actions/edit"
ACTIONS_GATE_PREFIX = "/actions/gate/"
# T050/T051 (change 010-doxbench-editor-chat): the two doxBench HTTP routes.
# See the section banner above `_handle_workbench_model_catalog` for the
# judgement calls their handlers make.
WORKBENCH_MODEL_CATALOG_ROUTE = "/workbench/model-catalog"
# add-doxbench-editing-phase-b task 9.5: the THREAD read route. A console-
# internal surface, deliberately NOT a released contract envelope — no
# openxFactory schema declares a thread shape, and inventing a `schema_version`
# for one here would claim a release that was never cut. It carries the same
# unversioned local shape `/capabilities` does, and the sidecar file itself is
# the governed artifact.
WORKBENCH_THREAD_ROUTE = "/workbench/thread"
ACTIONS_WORKBENCH_CHAT_TURN_ROUTE = "/actions/workbench/chat-turn"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})
JSON_CTYPE = "application/json; charset=utf-8"
JSON_OBJECT_BODY_REQUIRED = "a JSON object body is required"
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
_DEFAULT_CAPABILITIES = {"actions": {"notebook": False, "gate": False, "refresh": False,
                                    "session": False, "edit": False},
                         "actor": None, "refresh": {"binding": None, "loopback_only": True}}


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
# `WorkbenchModelPort` and its typed catalog/fake now exist as T020's
# catalog-only core. `model_port_factory` below (and
# `_workbench_model_port`, on the handler class further down) remains
# DUCK-TYPED at the injection boundary; the catalog handler consumes
# `catalog()`, while the turn handler deliberately stops before provider
# dispatch because the port has no dispatch member yet.
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
DOXBENCH_CHAT_TURN_KIND = "workbench-chat-turn"
DOXBENCH_CHAT_TURN_SUCCESS_KIND = "workbench-chat-turn-success"
DOXBENCH_CHAT_TURN_FAILURE_KIND = "workbench-chat-turn-failure"
# The CO-RESIDENT WIDENED family (contract-v1.34, add-doxbench-editing-phase-b
# §13). Both families are served: the v1 kinds above are DEPRECATED, not
# withdrawn, and the route answers a request in the family it arrived in --
# answering a v1 turn in a v2 envelope would break exactly the client the
# deprecation exists to keep working, and answering a v2 turn in a deprecated
# one would emit a shape with no room for what that turn declared.
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
                               kind: str = DOXBENCH_CHAT_TURN_FAILURE_KIND) -> dict:
    """The RELEASED `workbench-chat-turn-failure` envelope for `code` — a PURE
    module-level function, testable with no handler and no server.

    Keys are the released allowlist: `schema_version`, `kind`,
    `client_turn_id`, `error`, `message`, and — ONLY for
    `request_limit_exceeded` — the `limit` block, REBUILT from exactly three
    named fields exactly as `doxbench_error_body` rebuilds it, so nothing
    request-derived can splice a key into a response. The message is the same
    fixed module-level constant the pre-release shape used; only the envelope
    changed.

    `kind` selects the FAMILY the refusal is answered in (contract-v1.34). The
    two failure envelopes are structurally identical -- a refusal discloses
    nothing whichever family it answers -- so the only thing that varies is which
    `kind` a caller is entitled to receive, and that is the family its request
    arrived in."""
    _, message = DOXBENCH_ERROR_CATALOG[code]
    body: dict = {
        "schema_version": DOXBENCH_WIRE_SCHEMA_VERSION,
        "kind": str(kind),
        "client_turn_id": str(client_turn_id),
        "error": code,
        "message": message,
    }
    if code in DOXBENCH_LIMIT_BEARING_CODES and limit is not None:
        body["limit"] = {
            "dimension": str(limit["dimension"]),
            "measured": int(limit["measured"]),
            "maximum": int(limit["maximum"]),
        }
    return body


def doxbench_turn_success_body(*, client_turn_id: str, assistant_turn_id: str,
                               model_id: str, observed_hashes: dict,
                               assistant_prose: str, proposals=()) -> dict:
    """The RELEASED `workbench-chat-turn-success` envelope (T051 dispatch
    arm) — a PURE module-level function, testable with no handler and no
    server, exactly like `doxbench_turn_failure_body`.

    Keys are the released allowlist and nothing else: `schema_version`,
    `kind`, `client_turn_id`, `assistant_turn_id`, `model_id`,
    `observed_hashes` (REBUILT from exactly the two named 64-hex strings, so
    nothing caller-derived can splice a key in), `assistant_prose`, and
    `proposals`. PIN EVOLUTION (T061, the loud widening the original
    docstring promised): the builder now takes 0-2 VALIDATED
    `doxbench_turns.TypedProposal` values and REBUILDS each into exactly the
    released four-field wire shape, so nothing provider-derived can splice a
    key in. The route still self-validates the built envelope against the
    released schema before storing or sending it; this builder is never the
    last word on conformance."""
    return {
        "schema_version": DOXBENCH_WIRE_SCHEMA_VERSION,
        "kind": DOXBENCH_CHAT_TURN_SUCCESS_KIND,
        "client_turn_id": str(client_turn_id),
        "assistant_turn_id": str(assistant_turn_id),
        "model_id": str(model_id),
        "observed_hashes": {
            "outline": str(observed_hashes["outline"]),
            "document": str(observed_hashes["document"]),
        },
        "assistant_prose": str(assistant_prose),
        "proposals": [
            {"target": str(p.target), "base_hash": str(p.base_hash),
             "summary": str(p.summary), "content": str(p.content)}
            for p in proposals
        ],
    }


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

    Its three CONSUMERS are now the v2 wire record, the thread sidecar's turn
    header, and nothing else. The deprecated v1 success envelope does NOT
    consult it: that envelope has room for exactly one model id and cannot state
    both facts, which is recorded as a v1 limitation rather than papered over."""
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


def doxbench_context_packet(packet) -> dict:
    """The ASSEMBLED CONTEXT's posture, as the widened record carries it since
    contract-v1.39 (task 10.7) — derived in ONE place, from the packet the turn
    ACTUALLY RAN UNDER, on `doxbench_selected_model`'s precedent one function up.

    The ratified sentence is *"Where the knowledge service is unavailable the
    turn SHALL degrade to a declared reduced packet … with the reduced posture
    STATED"*. Until v1.39 it was stated only INSIDE the packet, where no reader
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
    A test drives each refusal through that seam."""
    posture = getattr(packet, "posture", None)
    reason = getattr(packet, "reduced_reason", None)
    if posture == doxbench_packet.POSTURE_REDUCED:
        if not reason:
            raise doxbench_packet.PacketError(
                "a reduced packet STATES the reduced posture's reason; a "
                "record cannot carry a reduction nobody can read")
        return {"posture": posture, "reduced_reason": str(reason)}
    if posture == doxbench_packet.POSTURE_FULL:
        if reason:
            raise doxbench_packet.PacketError(
                "a full packet carries no reduction reason; a record cannot "
                "state both postures and let a reader pick")
        return {"posture": posture}
    raise doxbench_packet.PacketError(
        "a packet states its posture; a record cannot declare one the packet "
        "does not have")


def doxbench_turn_v2_success_body(*, client_turn_id: str, assistant_turn_id: str,
                                  model_id: str, requested_model_id: str,
                                  routing_rule: bool, data_handling: str,
                                  bound_buffer: str, observed_hashes: dict,
                                  assistant_prose: str, context_posture: str,
                                  context_reduced_reason: str | None = None,
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

    …and, SINCE contract-v1.39 (task 10.7), a fourth:

    * `context_packet` — the POSTURE the turn's bounded context packet was
      assembled under, plus the reduction's reason when there is one. Rebuilt
      here from two named scalars for the same reason `selected_model` is: a
      caller handing in a ready-made dict could splice a key past the builder,
      and this envelope is closed. The posture is a REQUIRED argument, so no v2
      record can be built that silently omits it — the WIRE key is optional
      (that is what makes v1.39 additive), but this producer always states it,
      and a full turn's record says `full` explicitly rather than by omission.
      Omission on the wire means "a producer older than v1.39", never "full".

    Like its v1 sibling this builder is never the last word on conformance: the
    route self-validates the built envelope against the released schema before it
    is stored or sent."""
    context_packet = {"posture": str(context_posture)}
    if context_reduced_reason is not None:
        context_packet["reduced_reason"] = str(context_reduced_reason)
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


# --------------------------- capability discovery (pure) ---------------------------

def _launch_editor(command: list[str], *, configured_editor: bool,
                   popen=subprocess.Popen):
    """Launch an edit command with the streams its invocation style requires.

    A configured ``$EDITOR`` may be a terminal program, so it must inherit the
    server's terminal and remain in its session.  The desktop-opener fallback
    has no interactive contract and is detached from the dashboard process.
    ``popen`` is injectable so tests never start either kind of program.
    """
    if configured_editor:
        return popen(command)
    return popen(
        command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, start_new_session=True)


def _listed_source_paths(entry) -> frozenset[str]:
    """Source paths the selected snapshot actually projects into the UI.

    The viewer can be reached from the corpus-wide document list, a staged-topic
    folder, or an active/archived change folder.  Root confinement alone is not
    enough for select-to-edit: without this projection check, a console-token
    holder could ask the route to open any existing file under the registered
    checkout, including one the dashboard never listed.
    """
    snapshot = entry.read_json() if entry is not None else None
    if not isinstance(snapshot, dict):
        return frozenset()

    paths: set[str] = set()
    for document in snapshot.get("documents") or []:
        if isinstance(document, dict) and isinstance(document.get("path"), str):
            paths.add(document["path"])
    for collection in ("staged_topics", "changes"):
        for item in snapshot.get(collection) or []:
            if not isinstance(item, dict):
                continue
            paths.update(path for path in (item.get("files") or [])
                         if isinstance(path, str))
    return frozenset(paths)


def _edit_request_fields(body) -> tuple[tuple[str, str, str] | None, str | None]:
    """Validate the select-to-edit wire body without touching the filesystem."""
    if not isinstance(body, dict):
        return None, JSON_OBJECT_BODY_REQUIRED
    path = body.get("path")
    repository = body.get("repository")
    ref = body.get("ref")
    if not all(isinstance(field, str) and field
               for field in (path, repository, ref)):
        return None, "path, repository, and ref must be non-empty strings"
    return (path, repository, ref), None


def _resolved_listed_edit_entry(source, path: str, repository: str | None,
                                ref: str | None):
    """Return the selected entry only when its projected file is editable."""
    registry = getattr(source, "registry", None) if source is not None else None
    if registry is None:
        return None
    entry = registry.resolve(repository, ref)
    target = registry.resolve_source(repository, ref, path)
    if (entry is None or entry.source_root is None or target is None
            or not target.is_file() or path not in _listed_source_paths(entry)):
        return None
    return entry


def compute_capabilities(*, nlm_present: bool, checkout_real: bool, loopback: bool,
                         actor: str | None = None,
                         refresh_binding: str | None = None) -> dict:
    """The startup capability verdict. The notebook action is available only on
    a loopback bind with `nlm` reachable and a real checkout — the served static
    image satisfies none of these, so the UI hides the affordance there. GATE
    actions (the local action center, add-ideation-intent-plane §3) require a
    loopback bind, a real checkout, AND a resolved human actor — the hosted
    image fails all three, so the tray/executing gate bar never renders there
    (the intent plane replaces this seam hosted-side in §4).

    REFRESH (add-dashboard-repo-selector, design D7) is ONE affordance with two
    bindings, and the capability reports WHICH binding this plane offers so the
    UI renders one button either way: `refetch` (a declared data source; a
    read, hence available off-loopback — that IS the hosted refresh) or
    `regenerate` (a real checkout; loopback-only, because it writes the derived
    snapshot). No binding means no affordance.

    SESSION (007-workbench-branch-sessions T083, FR-048) is stated SEPARATELY from
    the gate leg even though it currently shares the gate's three conditions, and
    that is deliberate on both counts:

      * the HOSTED dashboard must expose NONE of this capability, and a reader of
        `/capabilities` should not have to infer "no session" from "no gate". The
        renderer keys its session affordances on this key, so a plane that says
        `false` gets copyable CLI descriptors and no live control (FR-046).
      * the conditions are the gate's because a session write IS a gate write, and
        because the session's remote-write identity is the invoking engineer's OWN
        `gh` authentication (FR-034, D22) — a PERSONAL credential, which a hosted
        plane must never hold or borrow. Declaring the pull-request port and
        confining the hosted plane are therefore ONE decision (Phase 7 note 6).

    It is INDEPENDENT of `nlm`: a local plane with no notebook still has full
    sessions, because FR-042 already requires a session without its notebook to be
    a complete session."""
    binding = refresh_binding
    if binding == registry_mod.BINDING_REGENERATE and not (loopback and checkout_real):
        binding = None
    local_human = bool(actor and checkout_real and loopback)
    return {
        "actions": {
            "notebook": bool(nlm_present and checkout_real and loopback),
            "gate": local_human,
            "refresh": bool(binding),
            "session": local_human,
            "edit": local_human,
        },
        "actor": actor if (actor and checkout_real and loopback) else None,
        "refresh": {
            "binding": binding,
            # Only the writing binding is loopback-gated; the read-only re-fetch
            # must work on the served (0.0.0.0) bind behind the ingress.
            "loopback_only": binding != registry_mod.BINDING_REFETCH,
        },
    }


def _is_loopback(host: str) -> bool:
    return host in LOOPBACK_HOSTS


# --------------------------- the human console (FR-019) ---------------------------
#
# FR-019's THIRD clause — "reject and report any agent or automated invocation" —
# had no runtime realization on either public surface (PR #49 review finding 2).
# The first two clauses were enforced here before the body parse; the third was
# discharged only by in-process OBJECT TYPE (`gate_console.require_human_gate`
# refusing anything that is not a `HumanGate`), which no HTTP caller is ever
# asked about. The consequences were measured during the adjudication: a bare
# `http.client` POST tore a live session down with `200` and a gate-action record
# naming the HUMAN, and — worse — a CROSS-ORIGIN simple request from
# `https://evil.example` with `Content-Type: text/plain` did the same, so any page
# open in the engineer's browser could drive session verbs on the loopback plane.
#
# The realization is a HUMAN CONSOLE test, applied to the session verbs before the
# body is parsed, exactly where the other two clauses live:
#
#   1. a per-serve TOKEN, minted at start-up and published ONLY on
#      `/capabilities`. The served page reads it same-origin; a cross-origin page
#      cannot read a same-origin JSON response at all, so the drive-by class is
#      structurally out.
#   2. a same-origin `Origin`/`Referer` when the caller sends one, so a browser
#      that CAN reach the plane cannot borrow the human's session from another
#      site.
#   3. a JSON `Content-Type`, which a CSRF "simple request" is not allowed to set.
#
# What this HONESTLY does not do, stated so no reader over-reads it: a process
# already running as the engineer, on the engineer's own machine, can `GET
# /capabilities` and present the token. Hardening THAT is the xForge host's
# concern (the pre-existing ruling recorded at `cli.py`'s `_human_gate` and D22),
# not this local console's. What the check removes is every caller that cannot
# demonstrate it came from the console this serve started — which is the whole of
# the reachable attack surface the review reproduced.
CONSOLE_TOKEN_HEADER = "X-XF-Console-Token"
CONSOLE_TOKEN_FIELD = "console_token"
JSON_CONTENT_TYPE_PREFIX = "application/json"

AGENT_INVOCATION_REFUSAL = (
    "a session gate verb is human-only (FR-019) and this request does not come "
    "from the human console this serve started: it must be issued by the served "
    "page, same-origin, carrying this serve's console token")


def mint_console_token() -> str:
    """A fresh, unguessable per-serve console token. New on every start, so a
    token cannot outlive the console that minted it."""
    return secrets.token_urlsafe(32)


def loopback_authorities(port: int) -> frozenset[str]:
    """Normalized ``Host``/origin authorities for this loopback serve."""
    authorities = {
        f"[{host}]:{port}" if ":" in host else f"{host}:{port}"
        for host in LOOPBACK_HOSTS
    }
    if port == 80:
        authorities |= {
            f"[{host}]" if ":" in host else host
            for host in LOOPBACK_HOSTS
        }
    return frozenset(authorities)


# The refusal message every hosted non-`main` request gets, verbatim. Fixed text:
# nothing request-derived reaches the wire (the response discipline this module
# already keeps for the notebook action).
HOSTED_SESSION_REFUSAL = ("a ref other than 'main' is session-local data and is "
                          "not available on this plane")


def hosted_ref_refused(loopback: bool, ref: str | None) -> bool:
    """Whether a request naming `ref` must be REFUSED because this is the hosted
    plane (007-workbench-branch-sessions T083, FR-048).

    FR-048: "The hosted dashboard MUST expose NONE of this capability — no session,
    no branch-ref selection, no session verb, no worktree, no non-`main` snapshot —
    and a hosted request naming a non-`main` ref MUST refuse."

    The test is the BIND, not the advertised capability. A capability dict is a
    startup verdict a handler could in principle be constructed with by hand; the
    bind is what makes a plane hosted, and the confinement has to hold for any
    handler that is not on loopback. `None` / blank means `main` (the registry's own
    `normalize_ref` default), so every pre-existing ref-less request is untouched,
    and the LOCAL plane is untouched entirely — confining the hosted plane must not
    confine the plane this whole feature lives on.

    Why the hosted plane cannot simply have sessions: the session's remote-write
    identity is the invoking engineer's OWN `gh` authentication (FR-034, D22) — a
    personal credential, which a hosted plane must never hold or borrow — and the
    worktree a session reads through is a per-machine directory beside a real
    checkout, which a served image does not have (research R7).

    THE ARRIVAL PATH, RECORDED AND DELIBERATELY NOT BUILT (FR-048, chg 7.2). A
    hosted session becomes possible by binding the INTENT PLANE's apply-lane ref
    (openxFactory `add-ideation-intent-plane` §4) through the EXISTING
    (repository, ref) seam this function guards: the intent plane's lane already
    owns an identity that is not anybody's personal credential, and a lane ref is
    already a (repository, ref) pair, so the session would arrive as another row in
    the same registry — no new seam, no second write chokepoint, and the openxfactory
    App as the ruled hosted identity (D22). That binding is a SEPARATE change with
    its own gate: nothing in this module reaches for a lane, and this refusal is
    where the next reader will be standing when they ask why."""
    if loopback:
        return False
    return not registry_mod.is_publishable_ref(ref)


def hosted_index(document: dict) -> dict:
    """The snapshot INDEX as a hosted plane may project it (FR-048, PR #49 review
    finding 14): every non-`main` entry dropped, a non-`main` `active` dropped with
    them, and every non-`main` AGGREGATE MEMBER dropped too.

    `hosted_ref_refused` guards the routes that NAME a ref; the index names none,
    so it was outside that confinement entirely and published the branch names of
    unmerged work — the topic and cluster ids of work in progress — to anyone who
    could reach the bind. Pure, so the rule is testable on its own, and it reuses
    the SAME `is_publishable_ref` predicate the refusal does, so there is still
    one definition of "a ref a hosted plane may see".

    THE MEMBER PASS IS WAVE 2's. `entries` and `active` were projected and
    `aggregates[].members` was not, though `SnapshotRegistry.index_document` emits
    those members as `{repository, ref}` pairs — so an aggregate naming a session
    ref published `draft/<topic>` off-loopback with a 200 while `entries` was
    correctly main-only (reproduced by the wave-2 critic on a production-shaped
    hosted plane, and reproduced again here before the fix). Content stayed confined
    (`?ref=…` still 403), so what leaked is the topic id of unmerged work — the same
    class FR-048 exists to prevent. An aggregate whose members are ALL unpublishable
    is dropped whole rather than published empty: an aggregate is defined by the
    snapshots it composes, and one with no visible members is not a narrower view of
    itself, it is a name with nothing behind it (and a hosted plane composing it
    would find nothing to render)."""
    projected = dict(document)
    entries = [entry for entry in projected.get("entries") or []
               if registry_mod.is_publishable_ref(entry.get("ref"))]
    projected["entries"] = entries
    active = projected.get("active")
    if isinstance(active, dict) and not registry_mod.is_publishable_ref(active.get("ref")):
        projected.pop("active", None)
    if "aggregates" in projected:
        aggregates = []
        for aggregate in projected.get("aggregates") or []:
            if not isinstance(aggregate, dict):
                continue
            members = [member for member in aggregate.get("members") or []
                       if isinstance(member, dict)
                       and registry_mod.is_publishable_ref(member.get("ref"))]
            if not members:
                continue
            aggregates.append({**aggregate, "members": members})
        if aggregates:
            projected["aggregates"] = aggregates
        else:
            projected.pop("aggregates", None)
    return projected


def _checkout_real(checkout_root: Path | str) -> bool:
    """A real corpus checkout, not the served image's empty `/srv/empty` sentinel.

    "Real" means SCANNABLE AS A CORPUS (`corpus_root.corpus_scan_defect`) — the same
    predicate `cli.py`'s `--repo-root` guard uses, which is the same value under a
    second spelling (runbook §2). It used to mean merely "an existing, non-empty
    directory", which is what the sentinel fails; but that let a wrong-but-populated
    path (a home directory, a workspace root, a sibling repository) satisfy the
    condition that turns the local gate/session affordances ON — and those affordances
    WRITE INTO whatever tree this names. The docstring already promised a corpus;
    this makes the code keep the promise. The empty sentinel still fails it, so the
    hosted image is unchanged.

    `corpus_root` is a stdlib-plus-`doc_health.corpus` module for exactly this
    reason: this runs on every `build_server`, including the served image's, and
    reaching the predicate through `generator` would newly require PyYAML in a
    startup path that serves snapshots and scans nothing. Imported lazily, as this
    module does for every sibling."""
    from ideation_dashboard.corpus_root import corpus_scan_defect
    return corpus_scan_defect(checkout_root) is None


def resolve_actor(checkout_root: Path | str, override: str | None = None) -> str | None:
    """The local action center's human identity: an explicit ``--actor`` wins;
    otherwise the checkout's `git config user.name`. None (no identity) keeps
    gate actions unavailable — fail-closed, never a guessed actor."""
    if override and str(override).strip():
        return str(override).strip()
    import subprocess
    try:
        proc = subprocess.run(
            ["git", "-C", str(checkout_root), "config", "user.name"],
            capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    name = (proc.stdout or "").strip()
    return name or None


def real_notebook_adapter():
    """The REAL `nlm`-backed adapter — the ONE place a serve constructs one.

    Named, and supplied by the ENTRYPOINTS rather than defaulted inside
    `build_server` (PR #49 hardening item 1). `_make_adapter` used to fall back
    here whenever no factory was injected, so `build_server(...)` with no
    `adapter_factory` — which is how 10 of the 10 test call sites build a server —
    would reach the SHARED NotebookLM account the moment a session open or a
    notebook action succeeded on that server. Nothing fired only because no such
    test existed yet; the next one written would have, silently, because every
    adapter call site degrades on failure (FR-042) and therefore passes
    identically whether `nlm` is absent, failing, or succeeding.

    So the library default is ABSENCE and the two production entrypoints —
    `serve()` (which `main()` runs) and the CLI's `generate-and-open` — declare
    this factory explicitly. A caller that declares no adapter gets a plane with
    no notebook capability, which FR-042 already defines as a complete session."""
    from ideation_dashboard import workbench

    return workbench.NotebookAdapter()


def _probe_nlm(adapter_factory) -> bool:
    """Whether the DECLARED notebook adapter reports `nlm` available.

    No declared adapter is no capability: probing a real adapter a caller never
    asked for would advertise a `notebook` capability the server then could not
    honour without reaching a binary nobody declared (see
    `real_notebook_adapter`). A missing dependency or import is the same verdict."""
    if adapter_factory is None:
        return False
    try:
        return bool(adapter_factory().available())
    except Exception:  # noqa: BLE001
        # absence is a capability verdict, not an error
        return False


# --------------------------- divergence (pure) ---------------------------

def divergence(source_revision: str | None, head: str | None) -> dict[str, str | None]:
    """The snapshot↔checkout relationship. `unknown` when HEAD is undeterminable
    (e.g. no git); `aligned` when the checkout still sits on the projected
    revision; `diverged` when it has moved. Pure — unit-tested directly."""
    if not head:
        state = "unknown"
    elif source_revision and head == source_revision:
        state = "aligned"
    else:
        state = "diverged"
    return {"state": state, "source_revision": source_revision, "head": head}


# --------------------------- source-path containment (pure) ---------------------------

def resolve_source_path(checkout_root: Path, url_tail: str) -> Path | None:
    """Resolve a `/source/<tail>` request to an absolute file under
    `checkout_root`, or None to reject. Rejects absolute paths, NUL bytes, any
    escape of the root (via `..`, encoded `..`, or a symlink), and non-files.
    Percent-decoding happens BEFORE the containment check so `%2e%2e` cannot slip
    past.

    The containment check itself now lives in `snapshot_registry.resolve_within`
    so the SAME rule applies per registry entry (task 2.2); this stays the
    single-root entry point every existing caller and test uses."""
    return registry_mod.resolve_within(Path(checkout_root), url_tail)


def _head_of(checkout_root: Path, git=None) -> str | None:
    """Current git HEAD of the checkout, or None (degrades — never blocks
    serving)."""
    try:
        from doc_health.corpus import RealGit
        return (git or RealGit()).head_sha(Path(checkout_root))
    except Exception:
        return None


# --------------------------- request handler ---------------------------

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Static bundle + snapshot + read-only source pass-through. Bound
    subclasses set the class attributes below via `build_server`."""

    # W-5 (wave re-review): one stalled or lying client must never pin a
    # handler thread forever. `StreamRequestHandler.timeout` puts a socket
    # timeout on every read and write of the connection (setup() calls
    # settimeout), so a body that stops arriving — including mid-DRAIN of a
    # refused over-cap body, which without this blocked UNBOUNDEDLY — raises
    # OSError instead. The value bounds NETWORK SILENCE, never request
    # duration: a slow model dispatch performs no socket operation while it
    # waits, and a healthy local client is orders of magnitude faster.
    timeout = 30

    checkout_root: Path = Path(".")
    snapshot_path: Path = Path("snapshot.json")
    snapshot_route: str = SNAPSHOT_ROUTE
    source_revision: str | None = None
    head: str | None = None
    quiet: bool = True
    # The ONE (repository, ref) snapshot source: the registry every snapshot,
    # index, and refresh response is resolved through (task 2.1). None only in
    # hand-constructed handlers; `build_server` always supplies one.
    source = None
    # v2 seam: the startup capability verdict, whether the bind is loopback (the
    # write-route gate), and an injectable adapter factory (tests supply a fake).
    capabilities: dict = _DEFAULT_CAPABILITIES
    loopback: bool = True
    adapter_factory = None
    # The session's remote-write port supplier (T082). None means "build the real
    # `GhPullRequests` for this checkout"; a test injects its fake here.
    pull_request_factory = None
    # The doxBench `WorkbenchModelPort` supplier (T024, research R6). None means
    # NO model port at all — the honest empty-catalog/editor-only posture
    # (FR-025), not an error. The injection boundary stays DUCK-TYPED; see
    # `_workbench_model_port`.
    model_port_factory = None
    # The doxBench RELEASED-schema validator supplier (T024/T050/T051 wire
    # clause). Bound by `build_server` to `default_doxbench_validators` unless
    # a caller injects its own; None only in hand-constructed handlers, and a
    # None factory REFUSES both model routes, which is the fail-closed
    # direction (see `_doxbench_validators`).
    schema_validator_factory = None
    # The per-process doxBench turn-idempotency ledger (T050/T051). None only
    # in hand-constructed handlers; `build_server` always binds a fresh
    # `doxbench_turns.TurnStore()` here -- ONE store per served process, never
    # shared across servers (see `test_turn_store_is_bound_per_server_process`).
    turn_store = None
    # The doxBench STAGED-SET KNOWLEDGE SERVICE, declared at INSTALL time
    # (add-doxbench-editing-phase-b D11, task 10.6). None means NO knowledge
    # service, which is a declared POSTURE and not an error: the turn degrades
    # to the reduced packet with its reduction stated, the rails still run, and
    # the editors are untouched. NOTHING at runtime — no turn, no prompt, no
    # heuristic — may choose a backend, which is why this is a serve-level
    # declaration and why the route below only ever READS it.
    knowledge_declaration = None
    # The packet assembler this route reaches, bound by `build_server` to
    # `doxbench_packet.assemble_packet`. INJECTED for the same reason every
    # other collaborator on this route is (the model port, the notebook
    # adapter, the schema validators): the packet is now a collaborator, and
    # the leash it carries -- purpose, scope, expiry -- can only be exercised
    # end to end by a route that was handed one it must reject. Unlike the
    # capability seams, absence here is NOT a posture: the real assembler is
    # the default, because assembling a packet is the pipeline, not a
    # capability an install may decline.
    packet_assembler = staticmethod(doxbench_packet.assemble_packet)
    # The per-process content-free usage meter (task 10.8). None only in
    # hand-constructed handlers; one meter per served process, beside the turn
    # store and never shared across servers.
    usage_meter = None
    actor: str | None = None
    # The repository half of every session key this process serves, BOUND at
    # `build_server` to the served checkout's own repository (finding R2-11). None
    # only in hand-constructed handlers — see `_session_repository`, which is the
    # one reader and which never re-reads the mutable active entry when this is set.
    session_repository: str | None = None
    # The per-serve human-console token (FR-019's third clause). None on a plane
    # that has no session capability — and a None token REFUSES every session
    # verb, which is the fail-closed direction.
    console_token: str | None = None
    gate_index_validator = None  # test seam: injectable pinned-validator path
    gate_manifest_validator = None  # test seam: pinned workbench-manifest validator
    gate_xref_validator = None  # test seam: pinned cross-reference validator

    # keep the console quiet unless asked otherwise
    def log_message(self, fmt, *args):  # noqa: N802
        if not self.quiet:
            super().log_message(fmt, *args)

    def end_headers(self) -> None:  # noqa: N802
        # Every response is revalidated (`no-cache` = cached but checked, not
        # `no-store`): the bundle is rebuilt/redeployed in place under the
        # SAME urls (index.html/app.js/views/*), and browsers' heuristic
        # caching of those assets made a fresh deploy invisible until a hard
        # refresh. The snapshot route already fetches with cache: "no-store"
        # client-side; this closes the same gap for the static bundle.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def _divergence_headers(self, entry=None) -> None:
        state = divergence(self.source_revision, self.head)["state"]
        self.send_header("X-Snapshot-Source-Revision", str(self.source_revision or ""))
        self.send_header("X-Source-Head", str(self.head or ""))
        self.send_header("X-Snapshot-Divergence", state)
        # The transport half of the freshness header (design D11): which
        # (repository, ref) this response projects, where those bytes came from,
        # and whether they are the stale fallback.
        entry = entry if entry is not None else self._active_entry()
        # never NAME a session ref on a hosted response (FR-048, finding 14):
        # every route that would SERVE one already refuses, but `/capabilities`
        # and the static bundle also carry these headers, and the ref itself is
        # the topic id of unmerged work.
        if entry is not None and hosted_ref_refused(self.loopback,
                                                    getattr(entry, "ref", None)):
            entry = None
        if entry is not None:
            self.send_header("X-Snapshot-Repository", str(entry.repository))
            self.send_header("X-Snapshot-Ref", str(entry.ref))
            self.send_header("X-Snapshot-Origin", str(entry.origin))
            self.send_header("X-Snapshot-Generated-At", str(entry.generated_at or ""))
            self.send_header("X-Snapshot-Stale", "true" if entry.stale else "false")

    def _active_entry(self):
        return self.source.registry.active if self.source is not None else None

    # ---- the branch-session seam (007-workbench-branch-sessions T025) ----
    def _session_registry(self):
        """The registry a gate route keys session liveness on (FR-008), or None.

        None for a hand-constructed handler with no source: with nowhere to record
        liveness there can be no session, and `create-document` then takes its
        pre-session path unchanged rather than half-opening one."""
        return self.source.registry if self.source is not None else None

    def _session_notebook(self):
        """The notebook adapter a session's notebook is created and retired
        through (007-workbench-branch-sessions T074; FR-036, FR-021, D16), or None.

        Declared ONLY when the `notebook` capability is TRUE — a loopback bind, a
        real checkout, and `nlm` reachable (`compute_capabilities`) — so this is the
        same confinement decision the capability itself already made: a hosted
        plane never touches `nlm`, and a session on one simply has no notebook,
        which FR-042 already requires to be a complete session. Built through
        `_make_adapter`, which returns the DECLARED adapter and never falls back
        to the real `nlm`-backed one (PR #49 hardening item 1), so a server built
        with no `adapter_factory` — every test that does not inject a fake — has
        no notebook rather than a silent reach for the shared account (FR-043). An
        adapter that cannot be constructed is absence, not an error — the same
        verdict `_probe_nlm` reaches."""
        if not self.capabilities.get("actions", {}).get("notebook"):
            return None
        try:
            return self._make_adapter()
        except Exception:  # noqa: BLE001 - absence is a capability verdict
            return None

    def _session_pull_requests(self):
        """The `PullRequestPort` `open-pr` pushes and opens the pull request
        through (007-workbench-branch-sessions T082; FR-029, FR-034, D22), or None.

        Declared ONLY when the `session` capability is TRUE — a loopback bind, a
        real checkout, and a resolved human actor — because the identity this port
        writes with is the INVOKING ENGINEER'S OWN ambient `gh` authentication. It
        accepts no token, stores no credential, and has no hosted mode: that is
        exactly why declaring it here is the SAME decision as confining the hosted
        plane (`hosted_ref_refused`, FR-048). A hosted plane never gets one, and
        with none declared `open-pr` REFUSES naming the CLI parity command rather
        than inventing an identity.

        Built through `pull_request_factory` so a test injects `FakePullRequests`
        by the ONE seam and no test can reach a real `gh` or a network (quickstart
        step 6). A port that cannot be constructed is absence, not an error — the
        same verdict `_session_notebook` reaches."""
        if not self.capabilities.get("actions", {}).get("session"):
            return None
        try:
            if self.pull_request_factory is not None:
                return self.pull_request_factory()
            from ideation_dashboard.session_pr import GhPullRequests
            return GhPullRequests(Path(self.checkout_root))
        except Exception:  # noqa: BLE001 - absence is a capability verdict
            return None

    def _workbench_model_port(self):
        """The injected `WorkbenchModelPort` this server was declared with
        (T024, research R6), or None.

        GATED ON THE SAME local-human verdict the `session` capability already
        encodes (loopback + real checkout + resolved human actor) rather than
        a NEW capability key. `GET /workbench/model-catalog` now exposes the
        catalog on that gate; the additive public `/capabilities` model field
        remains deferred until the released contract is pinned. Reusing
        `session` is deliberate, not incidental: both gates protect the same
        thing, a loopback human console with a real checkout and a resolved
        actor, and provider dispatch is exactly the kind of action that
        capability already exists to fence.

        Absence — no declared factory, a plane that fails the reused gate, or
        a factory that raises — is a POSTURE (an honest empty-catalog /
        editor-only editor, FR-025, SC-008), not an error, mirroring
        `_session_pull_requests`/`_session_notebook`'s "absence is a
        capability verdict" discipline.

        This accessor itself never calls the port: it stays DUCK-TYPED and
        reports only presence/absence. The catalog handler is the one consumer
        of `catalog()`; the port PROTOCOL now declares `dispatch` (T049), but
        no route below calls it -- the dispatch arm is T051's, and the
        boundary refuses fixed until it lands."""
        if not self.capabilities.get("actions", {}).get("session"):
            return None
        if self.model_port_factory is None:
            return None
        try:
            return self.model_port_factory()
        except Exception:  # noqa: BLE001 - absence is a capability verdict
            return None

    # The largest corpus one tile's index is built from. A bound, not a
    # policy: a tile's staged set is a topic folder, and an index that grew
    # without one would be a way to spend a serve's memory by loading a tile.
    MAX_INDEXED_SOURCES = 200

    def _indexed_sources(self, projection):
        """This tile's staged set, as indexable sources.

        Read through `snapshot_registry.resolve_within` — the SINGLE
        containment authority `/source` already uses — rather than through a
        second path check of this route's own, because two confinement rules
        are how one of them drifts. A path that does not resolve, is not a
        file, or cannot be decoded is SKIPPED: an unreadable document is one
        the packet will not carry, never a reason to fail a turn.

        The bytes come from the SERVED CHECKOUT, which is what "the tile's
        staged set" means here: the corpus at the revision this tile projects.
        A session's own edits ride the turn as BUFFERS, verbatim and
        identity-verified, so nothing is read twice from two places.

        THE BOUND IS ON WHAT IS INDEXED, NOT ON WHAT IS ATTEMPTED (Codex review
        of PR #216, CODEX-C). Slicing `context_paths` before filtering let an
        unreadable entry consume index capacity, so a tile whose first entries
        were missing indexed FEWER than the bound and never even considered
        readable documents behind them — and the coverage sentence then blamed
        "the declared index bound" for omissions the bound had nothing to do
        with. Reproduced at a bound of 2 over three paths: one indexed.

        Returns the sources plus the refs that were UNREADABLE, so the packet
        can tell the two omission classes apart instead of merging them.
        """

        sources = []
        unreadable = []
        for ref in projection.context_paths:
            if len(sources) >= self.MAX_INDEXED_SOURCES:
                break
            resolved = registry_mod.resolve_within(self.checkout_root, ref)
            if resolved is None:
                unreadable.append(ref)
                continue
            try:
                text = resolved.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                unreadable.append(ref)
                continue
            sources.append(doxbench_knowledge.IndexedSource(ref=ref, text=text))
        return tuple(sources), tuple(unreadable)

    def _knowledge_service_and_coverage(self, projection):
        """The tool boundary over this install's DECLARED retrieval backend,
        indexed for this tile's confined corpus — or None.

        ABSENCE IS A POSTURE (design §3.4), exactly as it is for the model
        port: no declaration means no knowledge service, the packet assembler
        produces the DECLARED reduced packet with its reduction stated, and the
        editors are unaffected. A failure to index is the same posture rather
        than a turn failure, for the same reason.

        A FRESH backend per request, built from the install-time declaration.
        The declaration is process-wide; the INDEX is not, because this server
        is threaded and one tile's index must never be visible to another
        tile's turn. Nothing here consults the turn, the message, or the
        prompt: the declaration is the only input to which backend exists.

        COVERAGE, stated rather than left to silence (adversarial review, F6):
        the index has a DECLARED BOUND and the confinement does not, so a tile
        holding more documents than the bound has refs that are confined but
        were never indexed -- not retrievable this turn, and NOT "one retrieval
        call away" the way the packet's own lossless note would otherwise
        imply. The actual indexed count is returned beside the boundary so the
        packet can say so; an unreadable document counts as uncovered for the
        same reason.
        """

        declaration = getattr(self, "knowledge_declaration", None)
        if declaration is None:
            return None, None
        try:
            backend = doxbench_knowledge.build_backend(declaration)
            boundary = doxbench_knowledge.KnowledgeToolBoundary(backend)
            # ONLY CONFINED SOURCES ARE EVER INDEXED: `_indexed_sources` reads
            # `projection.context_paths`, which IS the tile's staged set and is
            # exactly what `confined_refs` computes the admissible set from, so
            # the index is a SUBSET of the confinement by construction rather
            # than by filtering afterwards (Codex review of PR #216, CODEX-A).
            sources, unreadable = self._indexed_sources(projection)
            boundary.reindex(sources)
        except Exception:  # noqa: BLE001 - absence is a capability verdict
            return None, None
        return boundary, doxbench_packet.CorpusCoverage(
            indexed=len(sources), unreadable=len(unreadable),
            total=len(projection.context_paths))

    # ------------------------------------------------------------------
    # THREADS (add-doxbench-editing-phase-b §9.2/§9.5/§11.5, design §4)
    #
    # THE SIDECAR IS THE RECORD. These helpers READ threads out of the session
    # worktree for the packet and WRITE one back after a turn settles, through
    # `doxbench_threads`' own single write route and the doxBench Save gate's
    # own declared allowlist. Nothing here parses, renders, or path-derives a
    # thread itself: every one of those rules has exactly one spelling, and it
    # is in `doxbench_threads`.
    # ------------------------------------------------------------------

    def _thread_plane(self) -> str:
        """Which plane this serve is, in `doxbench_threads`' own vocabulary. A
        non-loopback serve is the HOSTED plane, which opens no branch session
        and therefore has no threads (FR-048)."""
        return (doxbench_threads.LOCAL_PLANE if self.loopback
                else doxbench_threads.HOSTED_PLANE)

    def _thread_capability_absence(self) -> str | None:
        """`None` where threads exist, else the DECLARED cause. Fail-closed on
        an unresolved actor: a thread is a human's working memory on a session
        branch, and a session with no identified human is not one."""
        if not self.actor:
            return NO_RESOLVED_ACTOR_CAUSE
        try:
            doxbench_threads.require_thread_capability(
                plane=self._thread_plane(),
                gate_capability=bool(
                    self.capabilities.get("actions", {}).get("session")))
        except doxbench_threads.ThreadCapabilityAbsent as absent:
            # `.cause` and NOT `str(absent)` (CP1). The exception's text is
            # "<REASON> — <cause>", and the body carries the reason in its own
            # `reason` field — so returning the string embedded the reason
            # twice and made `cause` not a cause.
            return absent.cause
        return None

    def _session_worktree_for(self, key):
        """The SESSION WORKTREE this scope's threads live in, or None.

        A thread lives on the session branch inside the session worktree, so a
        scope that is not a live session entry has none — and that is an
        ABSENCE, not a failure: the packet then declares the thread absent
        rather than inventing an empty one.

        `source_root` IS the worktree for a session entry (the turn route
        already reads the session's own text through it).

        SESSION-NESS COMES FROM THE LIVENESS AUTHORITY, not from the registry's
        advisory markers — corrected 2026-08-19 after the adversarial review's
        P2-10. This used to gate on `session_tile or session_base`, and
        `snapshot_registry` documents BOTH as advisory: `session_tile` is "None
        on a bootstrap-reconstructed entry", and `session_base` "degrades to the
        original name-equality binding — advisory ... **and never the reason a
        session fails**". This made them exactly that, and the consequences were
        silent: a bootstrap-reconstructed entry with neither marker got `{}`
        threads, no mirrored record, and a 403 from the thread route, with
        nothing on the wire saying so.

        `branch_session.live_session_branches` is what the Save path itself
        trusts and what the turn route ALREADY reaches one step earlier through
        `doxbench_scope.session_created_paths_for_scope`. This route asks it
        through the SHARED `doxbench_scope.is_live_session_ref` rather than
        calling it again here (re-verify N-6). Asking it means a
        session this console can WRITE to is a session this console will RECORD
        into, which is the property that actually matters."""
        try:
            entry = self.source.registry.resolve(key.repository, key.ref)
        except Exception:  # noqa: BLE001 - an unresolvable scope has no threads
            return None
        if entry is None or entry.source_root is None:
            return None
        if not self._is_live_session_ref(key, entry):
            return None
        root = Path(entry.source_root)
        return root if root.is_dir() else None

    def _is_live_session_ref(self, key, entry) -> bool:
        """Whether `key.ref` is one of this tile's LIVE session branches.

        ONE spelling, in `doxbench_scope` beside the other consumer of the same
        question (re-verify N-6). This method had grown as a second copy and had
        already diverged from it — different ref comparison, different exception
        breadth — which is precisely how the two would have drifted apart on the
        next change to what counts as a live session."""
        from ideation_dashboard import doxbench_scope
        return doxbench_scope.is_live_session_ref(
            self.source.registry, key,
            repository=entry.repository or key.repository, ref=key.ref)

    def _read_thread(self, worktree, document: str):
        """One document's thread, or None where no sidecar exists or it cannot
        be read as one.

        An UNREADABLE sidecar is treated exactly as an absent one, and the
        reason is the packet's: an invented or half-parsed thread would be a
        claim that a conversation happened. Confinement is the same
        `resolve_within` authority `/source` uses, so a thread path cannot
        escape the worktree."""
        if worktree is None:
            return None
        try:
            relative = doxbench_threads.thread_path_for(document)
        except doxbench_threads.ThreadError:
            return None
        target = registry_mod.resolve_within(worktree, relative)
        if target is None or not target.is_file():
            return None
        try:
            return doxbench_threads.parse_thread(
                target.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, doxbench_threads.ThreadError):
            return None

    def _document_threads(self, key, document_keys) -> dict:
        """The thread mapping `assemble_packet` takes — the seam §10 left for
        §11 to fill (`tasks.md` 10.3's "Thread read side, and what waits on
        §11").

        Keyed by BUFFER KEY, so the packet's selected-thread and thread-state
        sections name the same keys the turn's buffers do. For every
        PATH-BACKED document buffer that key IS its path, which is also what the
        WRITE side keys by since PR #223's C3 — so a read and a write name one
        file. The one buffer where they differ is the reserved unbacked slot
        (key `document`, path None): the write side records no sidecar for it at
        all, so the read is always an honest absence rather than a lookup under
        a key nothing writes."""
        absent = self._thread_capability_absence()
        if absent is not None:
            return {}
        worktree = self._session_worktree_for(key)
        if worktree is None:
            return {}
        threads = {}
        for document in document_keys:
            thread = self._read_thread(worktree, document)
            if thread is not None:
                threads[document] = thread
        return threads

    def _thread_gate(self, worktree):
        """The doxBench Save gate, rooted at the session worktree and DECLARING
        it — the one gate on this surface whose allowlist carries the thread
        prefix (`gate_routes.first_edit_gate_factory`, task 9.5). Built through
        that factory rather than beside it, so the widening has one spelling."""
        from ideation_dashboard import gate_console
        from ideation_dashboard import gate_routes
        return gate_routes.first_edit_gate_factory(
            self.actor, gate_console.DEFAULT_RECORDS_DIR)(worktree)

    def _mirror_turn_into_sidecar(self, key, *, document: str, turn_id: str,
                                  model_id: str, bound_buffer_key: str,
                                  human: str, assistant: str, mirror=None,
                                  dereference=None) -> bool:
        """Append this turn to the selected document's sidecar and write it
        (tasks 9.2's write half, 11.5).

        Order is `doxbench_threads`': the append is computed FIRST and
        completely, and the mirror is consulted afterwards on the resulting
        thread — the sidecar is the record, so nothing downstream of it decides
        what the record says. `dereference` is the BRIDGE's seam; with none, a
        body carrying a harness pointer is refused by `ThreadTurn` rather than
        persisted, which is the fail-closed half of task 3.5's finding.

        RETURNS whether the record was written, and NEVER raises into the turn.
        THE JUDGEMENT CALL, STATED: the provider has already answered by the
        time this runs, and there is no released refusal code for "the record
        could not be written". Losing the human's answer to protect a record
        that failed for an environment reason is the worse trade, so the answer
        still ships and the failure goes to the serve's own log — where every
        other non-wire diagnostic on this surface goes. The next turn's packet
        then declares that document's thread ABSENT, honestly, rather than
        implying a conversation that was never recorded."""
        worktree = self._session_worktree_for(key)
        if worktree is None or self._thread_capability_absence() is not None:
            return False
        try:
            thread = self._read_thread(worktree, document)
            if thread is None:
                thread = doxbench_threads.DocumentThread(
                    document=document,
                    scope=doxbench_threads.ThreadScope(
                        repository=key.repository, tile_kind=key.tile_kind,
                        tile_id=key.tile_id))
            turn = doxbench_threads.dereference_bodies(
                turn_id, model_id, bound_buffer_key,
                _sidecar_text(human), _sidecar_text(assistant),
                dereference=dereference if callable(dereference)
                else _no_dereference)
            appended = doxbench_threads.mirror_turn(thread, turn, mirror=mirror)
            doxbench_threads.write_thread(self._thread_gate(worktree), appended)
            return True
        except doxbench_threads.ThreadMirrorFailed:
            # The MIRROR failed, not the record. The append is already computed
            # and the sidecar is what the record is, so the write still happens
            # — a harness that cannot be told is not a reason to lose the turn.
            sys.stderr.write(
                "[workbench/thread] the harness mirror refused a turn; the "
                "sidecar is still the record\n")
            return self._write_thread_after_mirror_failure(worktree, document,
                                                           key, turn_id,
                                                           model_id,
                                                           bound_buffer_key,
                                                           human, assistant,
                                                           dereference)
        except Exception:  # noqa: BLE001 - a record failure never kills a turn
            sys.stderr.write(
                "[workbench/thread] this turn could not be mirrored into its "
                "sidecar; the answer stands and the thread stays absent\n")
            return False

    def _write_thread_after_mirror_failure(self, worktree, document, key,
                                           turn_id, model_id,
                                           bound_buffer_key, human, assistant,
                                           dereference) -> bool:
        try:
            thread = self._read_thread(worktree, document)
            if thread is None:
                thread = doxbench_threads.DocumentThread(
                    document=document,
                    scope=doxbench_threads.ThreadScope(
                        repository=key.repository, tile_kind=key.tile_kind,
                        tile_id=key.tile_id))
            turn = doxbench_threads.dereference_bodies(
                turn_id, model_id, bound_buffer_key,
                _sidecar_text(human), _sidecar_text(assistant),
                dereference=dereference if callable(dereference)
                else _no_dereference)
            appended = doxbench_threads.mirror_turn(thread, turn, mirror=None)
            doxbench_threads.write_thread(self._thread_gate(worktree), appended)
            return True
        except Exception:  # noqa: BLE001 - same verdict as the caller's
            return False

    def _handle_workbench_thread(self, head_only: bool) -> None:
        """`GET`/`HEAD /workbench/thread` (task 9.5).

        LOOPBACK-ONLY, fail-closed on an unresolved actor, absent without the
        gate capability and on the hosted plane — the four clauses the task
        names, in that order, and answered by `doxbench_threads`' own
        capability rule rather than by a second copy of it here. The read is
        confined by `resolve_within`, the same containment authority `/source`
        uses.

        WHAT IT IS FOR: the loaded-document selector switches the transcript to
        the selected document's thread (task 7.2), and this is where the
        browser reads that thread from. It writes nothing: a thread is written
        by a TURN, through the Save gate, and there is no second write route."""

        if not self.loopback:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE),
                _thread_absence_body(doxbench_threads.HOSTED_PLANE_CAUSE))
            return
        absence = self._thread_capability_absence()
        if absence is not None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE),
                _thread_absence_body(absence))
            return
        console_refusal = self._not_the_human_console()
        if console_refusal is not None:
            sys.stderr.write(
                f"[workbench/thread] agent_invocation refused: {console_refusal}\n")
            self._send_json(doxbench_error_status(DOXBENCH_ERR_CONSOLE_REQUIRED),
                            doxbench_error_body(DOXBENCH_ERR_CONSOLE_REQUIRED))
            return
        query = urllib.parse.parse_qs(
            urllib.parse.urlsplit(self.path).query, keep_blank_values=False)

        def _one(name):
            values = query.get(name) or []
            return values[0] if len(values) == 1 else None

        fields = {name: _one(name) for name in
                  ("repository", "ref", "tile_kind", "tile_id", "document")}
        if any(value is None or not str(value).strip()
               for value in fields.values()):
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_INVALID_TURN_REQUEST),
                doxbench_error_body(DOXBENCH_ERR_INVALID_TURN_REQUEST))
            return
        from ideation_dashboard import doxbench_scope
        key = doxbench_scope.ScopeKey(
            repository=fields["repository"], ref=fields["ref"],
            tile_kind=fields["tile_kind"], tile_id=fields["tile_id"])
        worktree = self._session_worktree_for(key)
        if worktree is None:
            # No live session on this scope. A DISTINCT cause (adversarial
            # review P3-19): this used to answer the no-gate-capability cause,
            # which is a true sentence about a different situation — the plane
            # HAS the capability here, this scope simply has no open session.
            # The non-oracle reasoning is unchanged and is what keeps the cause
            # generic: it says "no session is open for this scope" and never
            # which refs or tiles exist.
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE),
                _thread_absence_body(NO_LIVE_SESSION_CAUSE))
            return
        thread = self._read_thread(worktree, fields["document"])
        body = {
            "ok": True,
            "document": fields["document"],
            "present": thread is not None,
            "authority": doxbench_threads.NON_AUTHORITATIVE,
            "regenerable_from": doxbench_threads.REGENERABLE_FROM_TRANSCRIPT,
            "turns": [] if thread is None else [
                {"turn_id": turn.turn_id, "model": turn.model,
                 "bound_buffer_key": turn.bound_buffer_key,
                 "human": turn.human, "assistant": turn.assistant}
                for turn in thread.turns],
            "state_header": ("" if thread is None
                             else doxbench_threads.render_state_header(thread)),
        }
        self._serve_bytes(json.dumps(body).encode("utf-8"), JSON_CTYPE,
                          head_only)

    def _doxbench_validators(self):
        """The RELEASED per-kind schema validators for this request, or None.

        Resolved through the INJECTED `schema_validator_factory` seam, bound
        exactly like `model_port_factory`, so no test and no non-console plane
        depends on a pinned openxFactory checkout being present. The factory
        runs PER REQUEST, and the pinned loader re-verifies digests, the
        checkout's own manifest, and `stack.yaml`'s declared ref every time, so
        a checkout that drifts mid-run stops being trusted at the next request
        rather than at the next restart. Since the T104 final-queue Q-2 ruling
        (2026-08-09) the loader amortizes only the parse/compile behind a
        digest-keyed cache — the byte verification itself is never skipped, so
        this comment's freshness claim survives the cache by construction.

        Unlike `_workbench_model_port`, absence here is NOT a posture: a route
        that cannot read the contract must refuse, because serving a shape
        nothing verified is exactly the failure this seam exists to prevent.
        Every exception is swallowed into None — a `ContractPinError`'s text
        names checkout paths and digests, and that never belongs on the wire or
        in a response — and the caller emits only a fixed catalog code."""
        factory = self.schema_validator_factory
        if factory is None:
            return None
        try:
            validators = factory()
        except Exception:  # noqa: BLE001 - a pin failure must not reach the wire
            return None
        if not isinstance(validators, dict):
            return None
        return validators

    @staticmethod
    def _doxbench_wire_conforms(validators, kind: str, instance) -> bool:
        """True only when `instance` structurally conforms to the RELEASED
        schema for `kind`. An absent validator for the kind is FALSE, never a
        pass: an unknown kind means no verdict, and no verdict is not consent.
        Validation errors are discarded rather than reported — the caller emits
        a fixed code, and a jsonschema message can quote instance content."""
        validator = validators.get(kind) if isinstance(validators, dict) else None
        if validator is None:
            return False
        try:
            return not any(True for _ in validator.iter_errors(instance))
        except Exception:  # noqa: BLE001 - a broken validator is not a pass
            return False

    # ------------------------------------------------------------------
    # T050/T051 route handlers (change 010-doxbench-editor-chat).
    #
    # `GET /workbench/model-catalog` (T050) and `POST
    # /actions/workbench/chat-turn` (T051) LAND here. Both share the
    # `session` local-human-console gate `_workbench_model_port` already
    # documents.
    #
    # Five of the six new `DOXBENCH_ERROR_CATALOG` codes are this slice's
    # OWN judgement calls, spelling and (except where the contract pins a
    # status) HTTP status alike -- `turn_id_conflict` is the one spelling
    # taken VERBATIM from `contracts/chat-turn.md` ("Idempotency": "Same
    # conversation + turn id + different digest -> 409 `turn_id_conflict`"),
    # status included; `turn_in_flight`,
    # `turn_scope_refused`, `content_identity_mismatch`, `model_unavailable`,
    # and `invalid_turn_request` fill a genuine gap in the planning packet,
    # which pins the BEHAVIOUR each must have (FR-017/FR-018, spec.md's
    # preconditions 3-7, and the stale-model edge case) without pinning a
    # code spelling or, for most of them, a status. See each constant's own
    # comment above `DOXBENCH_ERROR_CATALOG` for its specific citation.
    #
    # The wire envelopes below ARE the released `contract-v1.27` shapes
    # (`xfactory-workbench-model-catalog`, `xfactory-workbench-chat-turn`),
    # emitted and self-validated since the T020/T024/T050/T051 wire clauses
    # landed. (This banner previously recorded the pre-release
    # discriminator-free posture; the release retired it.)
    #
    # NO PROVIDER IS EVER CONTACTED FROM THIS SLICE: `WorkbenchModelPort`
    # now DECLARES `dispatch` (T049), but no code below calls it --
    # `_handle_workbench_chat_turn`'s dispatch boundary still refuses
    # `model_capability_unavailable` unconditionally after building (and
    # discarding) the prompt envelope, until T051's dispatch arm lands with
    # its own tests -- no provider SDK import, no provider env-var read, no
    # credential, no raw endpoint, no secret name, anywhere below.

    def _handle_workbench_model_catalog(self, head_only: bool) -> None:
        """`GET`/`HEAD /workbench/model-catalog` (T050). Dispatched from
        `_route` so both methods share one gate, mirroring how
        `CAPABILITIES_ROUTE` is handled."""
        if not (self.loopback and self.capabilities.get("actions", {}).get("session")
                and self.actor):
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        console_refusal = self._not_the_human_console()
        if console_refusal is not None:
            sys.stderr.write(
                f"[workbench/model-catalog] agent_invocation refused: {console_refusal}\n")
            self._send_json(doxbench_error_status(DOXBENCH_ERR_CONSOLE_REQUIRED),
                            doxbench_error_body(DOXBENCH_ERR_CONSOLE_REQUIRED))
            return
        # The RELEASED schema is resolved BEFORE the port is consulted: a plane
        # that cannot read the contract has no business asking an adapter for a
        # catalog it could not then verify.
        validators = self._doxbench_validators()
        if validators is None:
            self._send_json(doxbench_error_status(DOXBENCH_ERR_CATALOG_UNAVAILABLE),
                            doxbench_error_body(DOXBENCH_ERR_CATALOG_UNAVAILABLE))
            return
        from ideation_dashboard import doxbench_model
        if port := self._workbench_model_port():
            try:
                catalog = port.catalog()
            except Exception:  # noqa: BLE001 - never let a provider-shaped exception reach the wire
                self._send_json(doxbench_error_status(DOXBENCH_ERR_CATALOG_UNAVAILABLE),
                                doxbench_error_body(DOXBENCH_ERR_CATALOG_UNAVAILABLE))
                return
            if not isinstance(catalog, doxbench_model.ModelCatalog):
                self._send_json(doxbench_error_status(DOXBENCH_ERR_CATALOG_UNAVAILABLE),
                                doxbench_error_body(DOXBENCH_ERR_CATALOG_UNAVAILABLE))
                return
        else:
            # The honest empty-catalog / editor-only posture (FR-025, SC-008):
            # a SUCCESS, never an error. It travels the SAME enveloping and
            # validation path as a populated catalog — the released schema
            # declares an empty `models` array a success, so this posture is
            # contract-conformant rather than an exception to conformance.
            catalog = doxbench_model.EMPTY_CATALOG
        envelope = doxbench_model.catalog_wire_envelope(catalog)
        if not self._doxbench_wire_conforms(
                validators, DOXBENCH_MODEL_CATALOG_KIND, envelope):
            # Self-validation BEFORE send: the console never serves a wire
            # shape the released schema has not accepted, so a catalog that
            # cannot be represented conformantly becomes the fixed
            # "could not be assembled safely" refusal.
            self._send_json(doxbench_error_status(DOXBENCH_ERR_CATALOG_UNAVAILABLE),
                            doxbench_error_body(DOXBENCH_ERR_CATALOG_UNAVAILABLE))
            return
        self._serve_bytes(json.dumps(envelope).encode("utf-8"), JSON_CTYPE, head_only)

    @staticmethod
    def _wire_valid_turn_id(payload):
        """The submitted `client_turn_id` if it is usable in the RELEASED
        failure envelope (a string of 1..128 characters, the released bound),
        else None.

        Read straight off the raw payload, BEFORE schema validation, for one
        purpose: a failure the browser cannot correlate to its own turn is
        nearly useless to it, and most schema refusals have nothing to do with
        this field. Nothing else is trusted from the unvalidated payload, and a
        None result never becomes a fabricated id -- it selects the fixed
        pre-release shape instead."""
        if not isinstance(payload, dict):
            return None
        turn_id = payload.get("client_turn_id")
        if not isinstance(turn_id, str) or not (1 <= len(turn_id) <= 128):
            return None
        return turn_id

    def _refuse_turn(self, validators, code, turn_id, *, limit=None,
                     failure_kind=DOXBENCH_CHAT_TURN_FAILURE_KIND) -> None:
        """Emit one chat-turn refusal in the correct envelope.

        With a wire-valid `turn_id` this is the RELEASED
        `workbench-chat-turn-failure` envelope, SELF-VALIDATED against the
        released schema before it is sent; without one -- or if that envelope
        somehow fails its own validation -- it is `doxbench_error_body`'s fixed
        shape. The console never sends a wire shape the released schema has not
        accepted, and it never invents a turn identity to obtain one.

        Every caller passes `_wire_valid_turn_id`'s verdict, NOT the parsed
        `client_turn_id` the turn store is keyed on. The two hold the same
        string whenever the released schema accepted the request, and the
        distinction only bites when a validator is more permissive than the
        release: then the wire-valid verdict is None and this emits the fixed
        shape, rather than putting an out-of-bounds id in an envelope that
        claims released conformance. The turn STORE keeps using the parsed id,
        because idempotency is keyed on what the caller actually sent.

        `failure_kind` is the FAMILY the refusal is answered in (contract-v1.34).
        It follows the family the request arrived in and defaults to the v1
        envelope, which is what a request that never named a recognizable family
        still gets."""
        status = doxbench_error_status(code)
        if turn_id is not None:
            body = doxbench_turn_failure_body(code, turn_id, limit=limit,
                                              kind=failure_kind)
            if self._doxbench_wire_conforms(validators, failure_kind, body):
                self._send_json(status, body)
                return
        self._send_json(status, doxbench_error_body(code, limit=limit))

    @staticmethod
    def _parse_workbench_chat_turn_common(payload):
        """The fields BOTH released chat-turn families spell identically, coerced
        from one payload; `None` on any structural violation.

        Split out at contract-v1.34 so the two family parsers below differ in
        exactly what actually differs -- how the binding is DECLARED and how many
        buffers may ride -- rather than in a second copy of the eight fields that
        do not. Each family parser calls this, then adds its own half."""
        from ideation_dashboard import doxbench_turns

        if not isinstance(payload, dict):
            return None

        client_turn_id = payload.get("client_turn_id")
        if not isinstance(client_turn_id, str) or not client_turn_id:
            return None

        scope = payload.get("scope")
        if not isinstance(scope, dict):
            return None
        scope_fields = {}
        for name in ("repository", "ref", "tile_kind", "tile_id"):
            value = scope.get(name)
            if not isinstance(value, str):
                return None
            scope_fields[name] = value

        working_subject = payload.get("working_subject")
        if not isinstance(working_subject, str):
            return None

        message = payload.get("message")
        if not isinstance(message, str) or not message.strip():
            return None

        model_id = payload.get("model_id")
        if not isinstance(model_id, str) or not model_id:
            return None

        last_assistant_turn_id = payload.get("last_assistant_turn_id")
        if last_assistant_turn_id is not None and not isinstance(last_assistant_turn_id, str):
            return None

        transcript_raw = payload.get("transcript")
        if not isinstance(transcript_raw, list):
            return None
        transcript_turns = []
        for item in transcript_raw:
            if not isinstance(item, dict):
                return None
            role = item.get("role")
            # The RELEASED `transcript_turn` spells this field `content`; the
            # internal `doxbench_turns.TranscriptTurn` keeps its own `text`
            # attribute, so the mapping happens HERE, at the wire boundary,
            # rather than by renaming a validated domain type. Reading `text`
            # off the wire would now be unreachable anyway: the closed released
            # envelope refuses it before this parser runs.
            text = item.get("content")
            if not isinstance(role, str) or not isinstance(text, str):
                return None
            transcript_turns.append(doxbench_turns.TranscriptTurn(role=role, text=text))

        buffers_raw = payload.get("buffers")
        if not isinstance(buffers_raw, list) or not buffers_raw:
            return None
        turn_buffers = []
        for item in buffers_raw:
            if not isinstance(item, dict):
                return None
            kind = item.get("kind")
            repository = item.get("repository")
            path = item.get("path")
            base_ref = item.get("base_ref")
            base_revision = item.get("base_revision")
            base_hash = item.get("base_hash")
            content_hash = item.get("content_hash")
            content = item.get("content")
            dirty = item.get("dirty")
            if not isinstance(kind, str) or not isinstance(repository, str):
                return None
            if path is not None and not isinstance(path, str):
                return None
            if not all(isinstance(value, str) for value in
                       (base_ref, base_revision, base_hash, content_hash, content)):
                return None
            if not isinstance(dirty, bool):
                return None
            turn_buffers.append(doxbench_turns.TurnBuffer(
                kind=kind, repository=repository, path=path, base_ref=base_ref,
                base_revision=base_revision, base_hash=base_hash,
                content_hash=content_hash, content=content, dirty=dirty))

        return {
            "client_turn_id": client_turn_id,
            "scope_fields": scope_fields,
            "working_subject": working_subject,
            "message": message,
            "model_id": model_id,
            "last_assistant_turn_id": last_assistant_turn_id,
            "transcript_turns": transcript_turns,
            "turn_buffers": turn_buffers,
        }

    @classmethod
    def _parse_workbench_chat_turn_body(cls, payload):
        """Structural, known-field extraction for a RELEASED v1 `POST
        /actions/workbench/chat-turn` (T051). Returns the coerced-field record,
        or `None` on ANY structural violation: a missing/wrong-typed field, a
        blank-or-whitespace-only `message`, or a buffer list that is not exactly
        one `outline` plus one `document`. Runs AFTER the released-schema gate,
        so unknown extra keys are already refused by the CLOSED released envelope
        rather than ignored here -- this parser no longer needs to decide that
        question and deliberately still does not: it coerces the known fields
        the chain needs. NEVER re-implements
        `doxbench_turns.TurnBuffer`/`TranscriptTurn`'s own validation --
        this only checks JSON *shape*, then hands the coerced values to
        those constructors.

        THE V1 BINDING, unchanged and DEPRECATED with its family
        (contract-v1.34): this envelope declares an `active_document_path` and
        nothing else, so the binding it can express is that path -- reading its
        KEY off a declared path is a spelling change, not the inference Phase A's
        review killed. Where it is null the envelope declares NO binding at all,
        `None` says so, and `doxbench_turns.revalidate_scope`'s own rule then
        refuses a path-backed document rather than guessing."""
        from ideation_dashboard import doxbench_turns

        common = cls._parse_workbench_chat_turn_common(payload)
        if common is None:
            return None
        active_document_path = payload.get("active_document_path")
        if active_document_path is not None and not isinstance(active_document_path, str):
            return None
        buffers = common["turn_buffers"]
        if sorted(buffer.kind for buffer in buffers) != ["document", "outline"]:
            return None
        return {
            **common,
            "active_document_path": active_document_path,
            "bound_buffer_key": active_document_path,
            "failure_kind": DOXBENCH_CHAT_TURN_FAILURE_KIND,
            "success_kind": DOXBENCH_CHAT_TURN_SUCCESS_KIND,
        }

    @classmethod
    def _parse_workbench_chat_turn_v2_body(cls, payload):
        """The same extraction for the WIDENED family (contract-v1.34;
        add-doxbench-editing-phase-b §13). Two differences, and only two:

        * the binding is DECLARED as `bound_buffer` -- a buffer KEY, carried on
          the wire, which the scope revalidation below requires to name one of
          the buffers this same request supplied. There is no
          `active_document_path` in this envelope to infer it from, and the
          closed schema refuses one; the record therefore states the binding the
          human declared rather than one derived from which document happened to
          be supplied (design D17).
        * the buffer set is the outline plus ONE OR MORE documents rather than
          exactly one of each, keyed as `doxbench_turns` keys them.

        The pairing itself is not restated here: `require_outline_and_documents`
        is the authority and runs on this same list a few steps later."""
        common = cls._parse_workbench_chat_turn_common(payload)
        if common is None:
            return None
        bound_buffer = payload.get("bound_buffer")
        if not isinstance(bound_buffer, str) or not bound_buffer:
            return None
        return {
            **common,
            # DELIBERATELY ABSENT: this family carries no active document path,
            # so there is nothing here for any later step to read one from.
            "bound_buffer_key": bound_buffer,
            "failure_kind": DOXBENCH_CHAT_TURN_V2_FAILURE_KIND,
            "success_kind": DOXBENCH_CHAT_TURN_V2_SUCCESS_KIND,
        }

    def _handle_workbench_chat_turn(self) -> None:
        """`POST /actions/workbench/chat-turn` (T051). See the section
        banner above `_handle_workbench_model_catalog` for the judgement
        calls this handler makes. Every step below refuses before the next
        and before any disclosure or dispatch."""
        if not (self.loopback and self.capabilities.get("actions", {}).get("session")
                and self.actor):
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        console_refusal = self._not_the_human_console()
        if console_refusal is not None:
            sys.stderr.write(
                f"[actions/workbench/chat-turn] agent_invocation refused: {console_refusal}\n")
            self._send_json(doxbench_error_status(DOXBENCH_ERR_CONSOLE_REQUIRED),
                            doxbench_error_body(DOXBENCH_ERR_CONSOLE_REQUIRED))
            return

        payload, refusal = self._read_bounded_json_body(
            DOXBENCH_MAX_REQUEST_BYTES, "request_body_bytes")
        if refusal is not None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED),
                doxbench_error_body(DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED, limit=refusal))
            return
        if payload is None:
            # DELIBERATELY the pre-existing `invalid_body` spelling, NOT a
            # doxBench code: a body that is not a JSON object at all fails the
            # same way `/actions/edit` and `/actions/gate/*` already fail it,
            # with the same fixed module-level message. `DOXBENCH_ERROR_CATALOG`
            # is the closed set of doxBench-SPECIFIC codes, not the closed set
            # of codes this route can emit -- `invalid_turn_request` below is
            # for a well-formed JSON OBJECT that fails the released schema or
            # the known-field shape.
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": JSON_OBJECT_BODY_REQUIRED})
            return

        # ---- EXACT SCHEMA (T051), between the body bound (precondition 2) and
        # scope (precondition 3): the request is validated against the RELEASED
        # `workbench-chat-turn` envelope BEFORE the precondition chain, which is
        # otherwise unchanged. The turn id is read first, unvalidated, for one
        # purpose only -- so a refusal the browser can correlate is possible
        # (see `_wire_valid_turn_id`). ----
        turn_id = self._wire_valid_turn_id(payload)
        # WHICH FAMILY THIS TURN ARRIVED IN (contract-v1.34). Read off the raw
        # payload's own `kind`, which is the only thing that distinguishes the
        # two co-resident envelopes, exactly as the released file discriminates
        # them. An unrecognized kind is answered in the v1 failure family: a
        # request that never named a family it could be answered in gets the
        # posture it would have got before this release, and the schema gate
        # below refuses it in any case.
        request_kind = (payload.get("kind")
                        if isinstance(payload.get("kind"), str) else None)
        if request_kind == DOXBENCH_CHAT_TURN_V2_KIND:
            failure_kind = DOXBENCH_CHAT_TURN_V2_FAILURE_KIND
            parse_body = self._parse_workbench_chat_turn_v2_body
        else:
            request_kind = DOXBENCH_CHAT_TURN_KIND
            failure_kind = DOXBENCH_CHAT_TURN_FAILURE_KIND
            parse_body = self._parse_workbench_chat_turn_body
        validators = self._doxbench_validators()
        if validators is None:
            # No readable contract, so no validated turn is possible. Fail
            # closed on the fixed pre-identity shape: this is a PLANE-level
            # verdict, not a defect in the caller's request, so it must not be
            # reported as one.
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        if not self._doxbench_wire_conforms(validators, request_kind, payload):
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind)
            return

        fields = parse_body(payload)
        if fields is None:
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind)
            return
        client_turn_id = fields["client_turn_id"]
        scope_fields = fields["scope_fields"]
        # The v1 envelope's own field, absent from the widened one by
        # construction. Read as an OPTIONAL member so the widened lane has
        # nothing to read it from -- the point of the release, not an oversight.
        active_document_path = fields.get("active_document_path")
        bound_buffer_key = fields["bound_buffer_key"]
        success_kind = fields["success_kind"]
        working_subject = fields["working_subject"]
        message = fields["message"]
        model_id = fields["model_id"]
        transcript_turns = fields["transcript_turns"]
        turn_buffers = fields["turn_buffers"]

        from ideation_dashboard import doxbench_hash
        from ideation_dashboard import doxbench_model
        from ideation_dashboard import doxbench_scope
        from ideation_dashboard import doxbench_turns

        key = doxbench_scope.ScopeKey(repository=scope_fields["repository"],
                                      ref=scope_fields["ref"],
                                      tile_kind=scope_fields["tile_kind"],
                                      tile_id=scope_fields["tile_id"])
        # ---- step 5: scope, all from SERVER truth ----
        projection = None
        session_base = None
        scope_refused = False
        try:
            entry = self.source.registry.resolve(key.repository, key.ref)
            if entry is None or entry.source_root is None:
                scope_refused = True
            else:
                # THE SESSION'S OWN BASE (T104 R-12): what this scope's branch
                # was created from, recorded on the entry by the OPEN (or the
                # bootstrap) — never by anything the request carried. It widens
                # exactly one comparison in the binding check below: a buffer
                # still based on the pre-session ref grounds a turn IFF its
                # recorded base revision is the session's AND the session has
                # not moved that document past the base — read through the same
                # confinement and the same decoding lens as `/source` itself,
                # so both sides hash the same character sequence. Absent
                # (a non-session scope, an unrecorded base) the binding check
                # keeps its original name-equality shape.
                recorded_base = getattr(entry, "session_base", None)
                if recorded_base:
                    source_root = Path(entry.source_root)

                    def _session_text(rel, _root=source_root):
                        target = registry_mod.resolve_within(_root, rel)
                        if target is None or not target.is_file():
                            return None
                        return doxbench_hash.served_text(target.read_bytes())

                    session_base = doxbench_turns.SessionBase(
                        ref=str(recorded_base[0]),
                        revision=str(recorded_base[1]),
                        text_of=_session_text,
                        # W-4: the base's other recorded revision spellings —
                        # the serving snapshot's revision at open time, which
                        # is what a real client's base_revision carries.
                        alias_revisions=tuple(
                            str(a) for a in
                            (getattr(entry, "session_base_aliases", ()) or ())))
                snapshot = json.loads(entry.read_bytes())
                # THE CREATED-IN-SESSION RECORD (T107; FR-043, CHK012). Every
                # input is the ENTRY's — the repository, the ref and the worktree
                # the registry itself holds — and the request contributes only the
                # tile identity the branch family is derived from. The browser's
                # own created overlay (`swb-session.js createdDocuments`) is never
                # read here and is not a request field this route parses: a body
                # cannot add a path to this set. With no live session on the
                # scope's own branch family the answer is empty and this
                # projection is what it was before T107.
                created_paths = doxbench_scope.session_created_paths_for_scope(
                    self.source.registry, key,
                    repository=entry.repository, ref=entry.ref,
                    source_root=Path(entry.source_root))
                projection = doxbench_scope.resolve_scope(
                    snapshot, key, source_root=Path(entry.source_root),
                    created_paths=created_paths)
                if projection is None:
                    scope_refused = True
                else:
                    # add-doxbench-editing-phase-b: the pair became a SET, and
                    # §13 released the wire that can say so. The DECLARED
                    # binding arrives from the parser -- `bound_buffer` on the
                    # widened envelope, the declared `active_document_path` on
                    # the deprecated one -- and is never derived here from an
                    # adjacent field, which is the mis-derivation Phase A's
                    # review killed. A v1 turn that declares nothing passes
                    # `None`, and the module's own rule then refuses a
                    # path-backed document rather than guessing.
                    doxbench_turns.revalidate_scope(
                        projection=projection, request_scope=key,
                        bound_buffer_key=bound_buffer_key,
                        buffer_keys=tuple(
                            doxbench_turns.buffer_key_for(b) for b in turn_buffers),
                        paths=tuple(b.path for b in turn_buffers),
                    )
        except (doxbench_turns.TurnScopeError, doxbench_scope.ScopeConfinementError,
                ValueError, OSError):
            scope_refused = True

        if scope_refused:
            self._refuse_turn(validators, DOXBENCH_ERR_TURN_SCOPE_REFUSED,
                              turn_id, failure_kind=failure_kind)
            return

        # ---- step 6: exact identity ----
        # WHICH RESERVED PATHS THIS LANE REFUSES (Codex review of PR #210,
        # CODEX-1). `outline` on both -- a document keyed there vanishes from the
        # enumeration and killed the handler, reproduced at a4a6f6e. `document`
        # on the WIDENED lane only, where it would shadow the reserved unbacked
        # slot that may ride beside it; the v1 envelope carries exactly one
        # document, so it has no such collision, and a v1 turn shaped that way
        # was served at a4a6f6e. Refusing it here would break the additive class
        # this release claims.
        refused_paths = (doxbench_turns.RESERVED_BUFFER_KEYS
                         if request_kind == DOXBENCH_CHAT_TURN_V2_KIND
                         else doxbench_turns.V1_RESERVED_BUFFER_KEYS)
        try:
            outline, turn_documents = \
                doxbench_turns.require_outline_and_documents(
                    turn_buffers, refused_paths=refused_paths)
            # The DECLARED order, from the module that owns it. The v1 envelope
            # carries exactly one document so this list has one member there;
            # the widened one carries the loaded set, and every member of it is
            # verified below rather than the first.
            document_keys = doxbench_turns.ordered_document_keys(turn_documents)
        except doxbench_turns.TurnBufferKindError:
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind)
            return

        try:
            doxbench_turns.verify_buffer_identity(outline)
            for buffer_key in document_keys:
                doxbench_turns.verify_buffer_identity(turn_documents[buffer_key])
        except doxbench_hash.ContentEncodingError:
            # T104 F5-8: a lone UTF-16 surrogate in buffer content. JSON's
            # `"\ud800"` escape decodes to a str no runtime can encode to
            # UTF-8, so `utf8_size`/`content_identity` inside
            # `verify_buffer_identity` raise `ContentEncodingError` -- a plain
            # ValueError SIBLING of `TurnError`, which the two turn-shaped
            # clauses below therefore never caught: the handler died and the
            # browser got a dropped connection instead of any HTTP envelope.
            # The released schema accepts the escape (jsonschema checks
            # structure, not encodability), so this is reachable from any
            # conforming client. A request whose text cannot be represented
            # identically across runtimes is MALFORMED -- the fixed
            # `invalid_turn_request`, refused before any hash comparison.
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind)
            return
        except doxbench_turns.TurnIdentityMismatchError:
            self._refuse_turn(validators, DOXBENCH_ERR_CONTENT_IDENTITY_MISMATCH,
                              turn_id, failure_kind=failure_kind)
            return
        except doxbench_turns.TurnLimitError as exc:
            self._refuse_turn(validators, DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
                              turn_id, limit=exc.as_public_dict(),
                              failure_kind=failure_kind)
            return

        # ---- step 7: model ----
        port = self._workbench_model_port()
        if port is None:
            self._refuse_turn(validators,
                              DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE,
                              turn_id, failure_kind=failure_kind)
            return
        try:
            catalog = port.catalog()
        except Exception:  # noqa: BLE001 - never let a provider-shaped exception reach the wire
            self._refuse_turn(validators, DOXBENCH_ERR_CATALOG_UNAVAILABLE,
                              turn_id, failure_kind=failure_kind)
            return
        if not isinstance(catalog, doxbench_model.ModelCatalog):
            self._refuse_turn(validators, DOXBENCH_ERR_CATALOG_UNAVAILABLE,
                              turn_id, failure_kind=failure_kind)
            return
        model_entry = catalog.selectable_entry_for(model_id)
        if model_entry is None:
            self._refuse_turn(validators, DOXBENCH_ERR_MODEL_UNAVAILABLE,
                              turn_id, failure_kind=failure_kind)
            return

        effective_input_limit = doxbench_model.effective_limit_bytes(
            server_maximum=doxbench_model.SERVER_MAX_INPUT_LIMIT_BYTES,
            entry_limit=model_entry.input_limit_bytes)
        effective_output_limit = doxbench_model.effective_limit_bytes(
            server_maximum=doxbench_model.SERVER_MAX_OUTPUT_LIMIT_BYTES,
            entry_limit=model_entry.output_limit_bytes)

        # T104 F5-8: these measurements sat OUTSIDE any try, so a lone
        # surrogate in `message`, `working_subject`, or a transcript turn's
        # text raised `ContentEncodingError` straight through the handler (the
        # buffer sizes are re-measured here too, but a surrogate in buffer
        # content was already refused at step 6). Measured and validated under
        # ONE try so every field class gets the same fixed refusal.
        try:
            outline_bytes = doxbench_hash.utf8_size(outline.content)
            # EVERY loaded document is measured, not the first: a bound that
            # measured only some of the buffers it is bounding would be no bound
            # at all, and the widened envelope carries N of them.
            document_buffer_bytes = tuple(
                doxbench_hash.utf8_size(turn_documents[buffer_key].content)
                for buffer_key in document_keys)
            document_bytes = sum(document_buffer_bytes)
            message_bytes = doxbench_hash.utf8_size(message)
            working_subject_bytes = doxbench_hash.utf8_size(working_subject)
            transcript_byte_total = doxbench_turns.transcript_bytes(transcript_turns)
            doxbench_turns.validate_working_subject(working_subject)
            doxbench_turns.validate_message(message)
            doxbench_turns.validate_transcript(transcript_turns)
            doxbench_turns.validate_request_body_bytes(
                outline_bytes=outline_bytes,
                document_buffer_bytes=document_buffer_bytes,
                message_bytes=message_bytes, working_subject_bytes=working_subject_bytes,
                transcript_bytes=transcript_byte_total)
        except doxbench_hash.ContentEncodingError:
            # The same sibling-ValueError verdict as step 6's clause: text no
            # runtime can carry identically is a malformed request, answered
            # with an HTTP envelope rather than a killed handler.
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind)
            return
        except doxbench_turns.TurnLimitError as exc:
            self._refuse_turn(validators, DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
                              turn_id, limit=exc.as_public_dict(),
                              failure_kind=failure_kind)
            return

        # `validate_request_body_bytes` cannot accept a NARROWED ceiling (it
        # only ever checks the fixed `MAX_REQUEST_BODY_BYTES`), so a
        # stricter catalog entry's limit is enforced here, inline, against
        # the same measured total -- research R7's "the route's own bound",
        # applied per-model rather than per-route.
        request_total_bytes = (outline_bytes + document_bytes + message_bytes
                               + working_subject_bytes + transcript_byte_total)
        if request_total_bytes > effective_input_limit:
            self._refuse_turn(
                validators, DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED, turn_id,
                limit={"dimension": "request_body_bytes",
                       "measured": request_total_bytes,
                       "maximum": effective_input_limit},
                failure_kind=failure_kind)
            return

        # ---- step 8: idempotency, LAST precondition. PEEK FIRST so the
        # untimed store wait is not entered for a request that can be answered
        # from an already-resolved record (contracts/chat-turn.md obligation 2;
        # see test_an_in_flight_attach_returns_promptly_rather_than_hanging).
        #
        # T104 F4: the peek is a FAST PATH, never a guarantee. This server is a
        # `ThreadingHTTPServer` over ONE shared store, so two requests carrying
        # the same `client_turn_id` can both pass the peek before either
        # reserves; the loser of that race then attaches inside `reserve` and
        # comes back with a lease that says DO NOT DISPATCH. That lease is
        # bound and honoured below -- discarding it dispatched the provider a
        # second time (FR-019) and then died on an uncaught `TurnConflictError`
        # out of `complete()`, dropping the connection with no envelope. ----
        #
        # BUFFER ORDER IS NOT PART OF THE REQUEST'S IDENTITY -- on the widened
        # lane (Codex review of PR #210, CODEX-2). `json.dumps(sort_keys=True)`
        # orders KEYS, never array members, so a retransmission that merely
        # reordered the buffer array digested differently and came back
        # `turn_id_conflict` instead of the recorded result -- reproduced: the
        # same turn id with the same content and the same hashes, second send
        # 409. The released contract says a repeated id with identical input
        # hashes replays, and a reordered array carries identical hashes.
        #
        # Canonicalized by BUFFER KEY, in the same UTF-16 code-unit order the
        # rest of this family declares, so the two runtimes cannot disagree about
        # it either.
        #
        # The v1 lane's canonical form is DELIBERATELY untouched, and the reason
        # is a TRADE rather than an impossibility -- stated plainly because the
        # first spelling of this comment overclaimed. That envelope fixes the
        # buffer COUNT (exactly two) and their KINDS (one outline, one document);
        # it does NOT fix their ARRAY ORDER, so a v1 client that retransmits the
        # same turn with its two buffers swapped gets the same 409 this fix
        # closes on the widened lane. That wart is KNOWINGLY RETAINED: v1 digests
        # are already recorded in live stores, and changing the form would make
        # every turn in flight unreplayable -- a live break traded against a
        # latent one on a lane that is deprecated and dies at contract-v2.0.
        canonical_buffer_order = turn_buffers
        if request_kind == DOXBENCH_CHAT_TURN_V2_KIND:
            canonical_buffer_order = sorted(
                turn_buffers,
                key=lambda buf: doxbench_turns.buffer_key_for(buf).encode(
                    "utf-16-be", "surrogatepass"))
        # THE DECLARED BINDING IS PART OF THE REQUEST'S IDENTITY
        # (add-doxbench-editing-phase-b §13). Two widened turns that carry the
        # same buffers and the same message but are bound to DIFFERENT documents
        # are different requests, and a digest that could not tell them apart
        # would replay one turn's answer for the other -- so `bound_buffer` joins
        # the canonical form. The v1 lane's `active_document_path` stays exactly
        # where it was, so its digests are unchanged; on that lane the two fields
        # hold the same string anyway.
        canonical = {
            "repository": scope_fields["repository"], "ref": scope_fields["ref"],
            "tile_kind": scope_fields["tile_kind"], "tile_id": scope_fields["tile_id"],
            "active_document_path": active_document_path,
            "working_subject": working_subject, "message": message, "model_id": model_id,
            "transcript": [[turn.role, turn.text] for turn in transcript_turns],
            "buffers": [
                {"kind": buf.kind, "path": buf.path, "repository": buf.repository,
                 "base_ref": buf.base_ref, "base_revision": buf.base_revision,
                 "base_hash": buf.base_hash, "content_hash": buf.content_hash,
                 "dirty": buf.dirty}
                for buf in canonical_buffer_order
            ],
        }
        if request_kind == DOXBENCH_CHAT_TURN_V2_KIND:
            canonical["kind"] = request_kind
            canonical["bound_buffer"] = bound_buffer_key
        try:
            digest = doxbench_hash.sha256_hex(
                json.dumps(canonical, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False))
        except doxbench_hash.ContentEncodingError:
            # W-1 (wave re-review): `json.dumps(..., ensure_ascii=False)`
            # PASSES a lone surrogate through, so the raise happens here, at
            # the encode inside `sha256_hex` — and `base_ref`/`base_revision`
            # are the two request fields that reach this statement with no
            # earlier measurement or hash gate (both are released-schema-valid
            # surrogate carriers). Same fixed refusal as the other three
            # sites: malformed request, HTTP envelope, never a dead handler.
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind)
            return

        record = self.turn_store.snapshot(key, client_turn_id)
        if record is not None:
            if record.state == doxbench_turns.TURN_STATE_IN_FLIGHT:
                code = (DOXBENCH_ERR_TURN_IN_FLIGHT if record.request_digest == digest
                       else DOXBENCH_ERR_TURN_ID_CONFLICT)
                self._refuse_turn(validators, code, turn_id, failure_kind=failure_kind)
                return
            if record.request_digest == digest:
                # A resolved replay: the stored outcome is returned
                # VERBATIM, byte-identical, never recomputed -- and therefore
                # NOT re-validated. It was validated when it was finalized;
                # re-validating here would let a checkout that drifted after
                # the fact change a stored answer, which is exactly what
                # byte-identical replay forbids (contracts/chat-turn.md
                # "Idempotency").
                outcome = record.validated_result
                self._send_json(outcome["status"], outcome["body"])
                return
            self._refuse_turn(validators, DOXBENCH_ERR_TURN_ID_CONFLICT,
                              turn_id, failure_kind=failure_kind)
            return

        try:
            lease = self.turn_store.reserve(key, client_turn_id, digest)
        except doxbench_turns.TurnInFlightError:
            self._refuse_turn(validators, DOXBENCH_ERR_TURN_IN_FLIGHT,
                              turn_id, failure_kind=failure_kind)
            return
        except doxbench_turns.TurnConflictError:
            self._refuse_turn(validators, DOXBENCH_ERR_TURN_ID_CONFLICT,
                              turn_id, failure_kind=failure_kind)
            return

        if not lease.should_dispatch:
            # The peek/reserve race was LOST: another thread already holds (or
            # held) this exact turn, and the store has handed back ITS result.
            # Replayed VERBATIM, byte-identical, never recomputed and never
            # re-validated -- the same rule, and the same two lines, as the
            # peek path above.
            outcome = lease.result
            self._send_json(outcome["status"], outcome["body"])
            return

        # ---- step 9: dispatch boundary (T051 dispatch arm). ----
        # `build_prompt_envelope` is the ONE authority that re-runs scope,
        # buffer-kind, buffer-to-scope BINDING, and exact identity in the
        # pinned load-bearing order. Its result is bound ONLY for the
        # dispatch call below -- never logged, returned, or stored.
        #
        # The arm dispatches IFF the injected adapter actually declares the
        # capability (`callable(getattr(port, "dispatch", None))` -- a
        # DUCK-TYPED probe, never `isinstance`, so a catalog-only adapter
        # keeps working). Without it, the fixed
        # `model_capability_unavailable` refusal below stands byte-identical
        # to the pre-arm posture. That IS the production posture: no real
        # adapter exists in this repository, and none is implied -- the
        # approved deployment adapter is T099's operator-gated slice. Every
        # provider outcome maps through `doxbench_model.dispatch_turn`
        # (T049): fixed codes, fixed redacted diagnostics, injected
        # monotonic clock for the deadline.
        outcome_code = DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE
        outcome_limit = None
        prompt_envelope = None
        turn_port = None
        # THE POSTURE THE TURN RAN UNDER (contract-v1.39, task 10.7), derived
        # below beside the packet it describes and read again in the v2 arm.
        # Seeded to None so a path that never assembles a packet cannot leave a
        # stale posture in scope: only the success arm reads it, and that arm is
        # reachable only when `prompt_envelope` was built, which happens after
        # this is set.
        context_packet_record = None
        try:
            # ---- the PACKET, assembled BEFORE the prompt and before any
            # provider (§10.3). Its rails run inside the assembler: the
            # confinement is computed from the projection and HANDED to the
            # retrieval boundary rather than left for it to respect, and the
            # lifecycle-status exemption is applied from each item's own
            # `Status:` header. `_knowledge_service` returning None is the
            # DECLARED reduced posture, not a failure, so nothing here branches
            # on it -- the reduction is stated inside the packet.
            #
            # PROMOTED FINDINGS are an empty set today, and deliberately so: a
            # finding becomes a promoted one only when a human performs the
            # reviewed act that creates the target object, and that object is
            # then an ordinary document of the tile, which the tile's own
            # staged set already carries. There is no promoted-findings
            # register to read, and inventing one here would be the parallel
            # decision store the contract forbids.
            knowledge, coverage = self._knowledge_service_and_coverage(
                projection)

            # THE THREADS, at last (§11; the seam §10 shipped and could not
            # fill). `assemble_packet` carries the selected document's thread
            # IN FULL and every other loaded document's STATE HEADER, and it
            # declares by name each loaded document that has no sidecar — so
            # an absence is stated rather than inferred from silence. Read from
            # the SESSION WORKTREE, which is the only place a thread lives; a
            # scope with no live session answers `{}`, which is the same
            # honest absence the route had before this slice, now for a reason
            # instead of by omission.
            threads = self._document_threads(key, document_keys)

            def _new_packet():
                return self.packet_assembler(
                    projection=projection,
                    scope=key,
                    selected_key=bound_buffer_key,
                    loaded_keys=document_keys,
                    query=message,
                    threads=threads,
                    knowledge=knowledge,
                    corpus_coverage=coverage,
                    # THE PACKET'S BOUND COMPOSES WITH THE MODEL'S OWN INPUT
                    # LIMIT (Codex review of PR #216, CODEX-B). The request
                    # bytes were measured and accepted against
                    # `effective_input_limit` above, but the packet is appended
                    # AFTER that check, so a turn could be accepted and then
                    # dispatch a prompt past the model's declared capacity —
                    # failing at the provider instead of at a measured bound.
                    # The packet is FITTED to what the request left, rather
                    # than refused afterwards: refusing here would resurrect
                    # exactly the un-actionable-refusal class the fit removed.
                    max_packet_bytes=doxbench_packet.packet_budget_for(
                        input_limit_bytes=effective_input_limit,
                        request_bytes=request_total_bytes,
                        # §11.5's DISCHARGED obligation. The reserve is no
                        # longer flat: the prompt's rendered per-section
                        # scaffolding is charged from the refs THIS turn will
                        # carry — one section per thread, one per evidence slot
                        # — because a flat number could only ever be right for
                        # one section count, and the count is exactly what this
                        # slice changed.
                        thread_refs=tuple(threads),
                        evidence_slots=doxbench_packet.DEFAULT_EVIDENCE_LIMIT),
                    already_carried=(
                        () if projection.outline_path is None
                        else (projection.outline_path,)),
                )

            packet = _new_packet()
            try:
                doxbench_packet.require_valid(
                    packet,
                    purpose=doxbench_packet.PACKET_PURPOSE_CHAT_TURN,
                    scope=key, now=time.monotonic())
            except doxbench_packet.PacketRejected:
                # THE DELTA'S OWN SENTENCE, realized literally: a consuming
                # surface presented with a stale or foreign packet "MUST reject
                # it and REQUEST A NEW ONE". So the route asks the service for
                # a new packet exactly once; only a second failure is a refusal,
                # because a leash that could not be reissued is a server that
                # cannot bound its own context.
                packet = _new_packet()

            # DERIVED HERE, INSIDE THE PACKET BOUNDARY, and for the reason the
            # boundary exists: this reads the packet, so its refusals are packet
            # refusals and must land on the same fixed codes every other packet
            # refusal does. Derived from the packet the turn will actually run
            # under — after the one permitted re-request above, so a reissued
            # packet's posture is the one recorded, never the rejected packet's.
            context_packet_record = doxbench_context_packet(packet)

            prompt_envelope = doxbench_turns.build_prompt_envelope(
                packet=packet, meter=self.usage_meter,
                projection=projection, request_scope=key,
                active_document_path=active_document_path,
                model_id=model_id, model_data_handling=model_entry.data_handling,
                model_input_limit_bytes=effective_input_limit,
                model_output_limit_bytes=effective_output_limit,
                working_subject=working_subject, transcript=tuple(transcript_turns),
                buffers=turn_buffers, message=message,
                session_base=session_base,
                refused_paths=refused_paths,
                # The DECLARED binding, checked against the supplied buffer set
                # and NOT stored as a binding claim on the envelope (PR #207
                # review F4): an internal field nothing serializes cannot
                # discharge the obligation to name the bound buffer in a durable
                # RECORD. §13's widened family carries it on the wire, which is
                # the only place a reader can consult it, and the success body
                # below is where it lands.
                bound_buffer_key=bound_buffer_key)
        except doxbench_turns.TurnScopeError:
            outcome_code = DOXBENCH_ERR_TURN_SCOPE_REFUSED
        except doxbench_turns.TurnIdentityMismatchError:
            outcome_code = DOXBENCH_ERR_CONTENT_IDENTITY_MISMATCH
        except doxbench_turns.TurnBufferKindError:
            outcome_code = DOXBENCH_ERR_INVALID_TURN_REQUEST
        except doxbench_packet.PacketBoundExceeded as exc:
            # THE BOUNDS RAIL'S REFUSAL ARM, on the wire (task 10.3, F2).
            #
            # RE-MAPPED after the adversarial review. This used to answer
            # `request_limit_exceeded` (413, "the request exceeds the allowed
            # size for this route"), which was FALSE twice over: the request
            # was a few hundred bytes, and what exceeded the bound was context
            # the SERVER selected. Evidence is now fitted by selecting less, so
            # reaching here means the session's own THREADS exceed the bound
            # alone -- a 409 against the session's state, with the measured
            # dimension named and a message pointing at the act that fixes it.
            outcome_code = DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED
            outcome_limit = exc.limit
        except doxbench_packet.PacketRejected:
            # The re-requested packet was ALSO invalid. The server could not
            # bound its own context for this turn, which no request the caller
            # could send would fix -- so it is a 500 that says exactly that,
            # never a 4xx blaming the turn.
            outcome_code = DOXBENCH_ERR_CONTEXT_PACKET_INVALID
        except doxbench_packet.PacketError:
            # Any other packet refusal is a malformed turn, mapped to the same
            # fixed code every other structural refusal uses. Its text names
            # this module's own vocabulary and stays in this process.
            outcome_code = DOXBENCH_ERR_INVALID_TURN_REQUEST
        except doxbench_hash.ContentEncodingError:
            # T104 F5-8, the step-9 re-verification leg: `build_prompt_envelope`
            # re-runs exact identity, so it re-raises the same sibling
            # ValueError the pre-reserve legs above already refuse. With those
            # legs in place no surrogate should survive to here -- but this
            # boundary maps EVERY re-verification failure to a fixed code, and
            # leaving one class to kill the handler mid-lease (dropping the
            # connection AND stranding the reserved slot) is exactly the
            # defect. Same verdict as the earlier legs: `invalid_turn_request`.
            outcome_code = DOXBENCH_ERR_INVALID_TURN_REQUEST

        # ---- ONE HARNESS SESSION PER DOCUMENT THREAD (task 11.4, and the
        # server half of task 7.2's thread switch). The adapter is asked to
        # bind to the SELECTED document's thread BEFORE the turn is dispatched,
        # so switching the selected document switches the harness session and
        # one session never serves two threads. Duck-typed exactly as
        # `dispatch` is: an adapter without the method is a catalog-only or
        # sessionless one and keeps working unchanged.
        #
        # A BINDING FAILURE IS NOT A TURN. If the adapter cannot bind this
        # thread — a dead child, or a session already serving another thread —
        # dispatching anyway would ground the answer in another document's
        # conversation, so the turn refuses with the route's existing fixed,
        # redacted `model_failed` and nothing is dispatched.
        # The capability is now `for_conversation` (PR #223, C2): an adapter
        # that offers it binds and dispatches atomically, and one that does not
        # is a catalog-only or sessionless adapter, unchanged.
        if prompt_envelope is not None \
                and callable(getattr(port, "for_conversation", None)):
            # EVERY turn binds, including an outline-bound one (adversarial
            # review P2-11). The bind used to be gated on
            # `bound_buffer_key in document_keys`, so an outline turn was
            # dispatched into whichever DOCUMENT session the harness was last
            # switched to and contaminated that document's harness context. An
            # outline conversation is a real conversation; it just is not a
            # document's, so it binds under its own tile-scoped key.
            # THE WHOLE SCOPE IS IN THE KEY (PR #223, Codex C1). The bare
            # `bound_buffer_key` is a repository-relative path and nothing else,
            # so two scopes loading the SAME path — one repository at two refs,
            # or two repositories on a multi-repository plane — collided in the
            # bridge's single per-serve session map and the second silently
            # inherited the first's conversation.
            conversation_key = (
                (port.conversation_key(key, bound_buffer_key)
                 if bound_buffer_key in document_keys
                 else port.outline_conversation_key(key))
                if callable(getattr(port, "conversation_key", None)) else None)
            try:
                if conversation_key is None:
                    raise RuntimeError(
                        "this adapter declares no conversation key")
                # BOUND AS PART OF THE DISPATCH, not before it (Codex C2). The
                # bind used to be a separate call, and under this threading
                # server another handler could move the selection in between —
                # sending this turn's prompt into that handler's session. The
                # per-turn view binds and prompts inside ONE lock acquisition.
                turn_port = port.for_conversation(conversation_key)
            except Exception:  # noqa: BLE001 - never let an adapter's text reach the wire
                sys.stderr.write(
                    "[workbench/chat-turn] the harness bridge could not bind "
                    "this document's thread; the turn is refused rather than "
                    "grounded in another thread\n")
                prompt_envelope = None
                outcome_code = DOXBENCH_ERR_MODEL_FAILED

        # The conversation-bound view where the adapter offers one, the adapter
        # itself otherwise (a catalog-only or sessionless adapter is unchanged).
        turn_port = turn_port if turn_port is not None else port
        if prompt_envelope is not None and callable(getattr(port, "dispatch", None)):
            # T061: typed proposals validate against the hashes THIS request
            # was shown — wrong base is a response-side defect mapped to the
            # fixed response_invalid, never a scope or identity refusal.
            # G-1: an OUTLINE-ONLY turn (no active document — the request's
            # `active_document_path` is null, which contract-v1.28 makes legal
            # by mirroring the already-nullable `buffer_state.path`) names no
            # document buffer for a proposal to rewrite. The narrowest reading
            # of a silent contract, recorded in
            # `doxbench_turns.validate_assistant_response`: such a turn is
            # chat grounded on the tile's context, with NO document-targeted
            # proposal. Every turn that DOES name a document is unchanged.
            # The permitted set is the REQUEST'S OWN buffer keys
            # (add-doxbench-editing-phase-b task 5.3 retired the fixed enum);
            # G-1's narrowing is unchanged and is now expressed PER BUFFER,
            # which is the same rule stated over a set: a document buffer backed
            # by NO PATH names no document, so a proposal targeting it would be a
            # rewrite of a document that does not exist. On the v1 lane that is
            # exactly "active_document_path is null", because the one document
            # buffer is then the unbacked one; on the widened lane the unbacked
            # slot can ride beside real documents, and only IT is withheld.
            permitted_targets = tuple(
                buffer_key for buffer_key in
                (doxbench_turns.OUTLINE_BUFFER_KEY,) + tuple(document_keys)
                if buffer_key == doxbench_turns.OUTLINE_BUFFER_KEY
                or turn_documents[buffer_key].path is not None)

            def _typed_response_validator(raw):
                return doxbench_turns.validate_assistant_response(
                    raw, observed=prompt_envelope.observed_hashes,
                    permitted_targets=permitted_targets)
            # PR #63 review (Codex P1): the deadline is enforced WHILE
            # dispatch runs, not merely measured afterwards. The adapter call
            # runs on a worker thread and the route waits at most the
            # validated declared timeout; on overrun the fixed model_timeout
            # refusal finalizes the slot (freeing the conversation) and the
            # late result — if it ever arrives — is discarded unread by the
            # abandoned daemon thread. dispatch_turn's own post-hoc elapsed
            # check stays as the pure verdict for adapters that DO return.
            outcome = self._deadline_bound_dispatch(
                turn_port, prompt_envelope, model_entry,
                _typed_response_validator)
            if isinstance(outcome, doxbench_model.TurnDispatchSuccess):
                # `assistant_turn_id` derivation is this slice's judgement
                # call: the released schema bounds it (1..128) without naming
                # a scheme, so it is derived from the turn's own canonical
                # request digest -- deterministic, request-unforgeable, and
                # carrying no provider or content material.
                observed = prompt_envelope.observed_hashes
                # ---- THE SIDECAR IS THE RECORD (tasks 9.2, 11.5) ----
                # Every turn is mirrored into the SELECTED document's thread,
                # before the answer is stored or sent, through
                # `doxbench_threads`' one write route and the doxBench Save
                # gate's own declared allowlist. The turn id is the derived
                # `assistant_turn_id` rather than the caller's own
                # `client_turn_id`: the released schema bounds that field's
                # LENGTH and nothing else, so a client could spell one carrying
                # the sidecar's own turn-header separator, and a record cannot
                # take its identity from a string a caller chose freely.
                #
                # An OUTLINE-bound turn writes no thread: a thread belongs to a
                # DOCUMENT, and the outline buffer is the tile's, not a
                # document's.
                # THE SIDECAR IS THE DOCUMENT'S, SO IT COMES FROM THE
                # DOCUMENT'S PATH (PR #223, Codex C3). It used to be derived
                # from the buffer KEY, and the two differ for exactly one
                # buffer: the reserved unbacked slot, whose key is `document`
                # and whose path is None. A turn on it wrote
                # `session-threads/document.thread.md` — a sidecar for a
                # document that does not exist, which no Save can ever commit
                # (`thread_commit_paths` is called with the real path), and
                # which a later re-key strands while a second thread starts at
                # the document's own path.
                #
                # A buffer with NO path has no document, so it records no
                # thread — the same rule the outline already follows. The buffer
                # key stays in the turn's metadata, where it belongs.
                bound_document = (
                    turn_documents[bound_buffer_key].path
                    if bound_buffer_key in document_keys else None)
                # DERIVED ONCE, AND BEFORE THE SIDECAR — corrected 2026-08-21
                # (adversarial review of the §11.7 release, F3). This used to be
                # computed inside the v2 arm below, so the sidecar was handed the
                # REQUESTED id while the wire record carried the RESOLVED one:
                # for a routing rule the durable transcript on disk named `auto`
                # and no reader could learn which model answered. The ratified
                # THEN's own purpose clause is "so a transcript names the model
                # that actually answered", and the thread file IS a transcript.
                selected_model = doxbench_selected_model(model_entry)
                if bound_document is not None:
                    self._mirror_turn_into_sidecar(
                        key, document=bound_document,
                        turn_id="assistant-" + digest[:56],
                        model_id=selected_model["resolved_model_id"],
                        bound_buffer_key=bound_buffer_key,
                        human=message, assistant=outcome.assistant_prose,
                        mirror=getattr(port, "mirror", lambda: None)(),
                        dereference=getattr(port, "dereference", None))
                if success_kind == DOXBENCH_CHAT_TURN_V2_SUCCESS_KIND:
                    # THE RECORD, at last able to say what the turn was about
                    # (§13; design D17). It names the DECLARED bound buffer --
                    # carried from the request, never derived -- states every
                    # buffer's observed identity by key, and carries the
                    # selected-model metadata beside the model that answered.
                    #
                    # The selected-model metadata is DERIVED from the catalog
                    # entry, in one place (`doxbench_selected_model`), so
                    # contract-v1.38's routing-rule entry changed that function
                    # rather than three literals here. `selected_model` is
                    # computed ABOVE, before the sidecar, because the sidecar
                    # needs the resolved id too (F3).
                    #
                    # AND SINCE contract-v1.39 (task 10.7) the record STATES the
                    # posture its context was assembled under. Derived above,
                    # beside the packet, by the same one-place discipline: the
                    # values are the PACKET's own, so the record and the packet's
                    # own declaration cannot disagree.
                    success_body = doxbench_turn_v2_success_body(
                        client_turn_id=client_turn_id,
                        assistant_turn_id="assistant-" + digest[:56],
                        model_id=selected_model["resolved_model_id"],
                        requested_model_id=selected_model["requested_model_id"],
                        routing_rule=selected_model["routing_rule"],
                        data_handling=selected_model["data_handling"],
                        bound_buffer=bound_buffer_key,
                        observed_hashes={
                            buffer_key: observed.for_key(buffer_key).hex
                            for buffer_key in observed.keys()
                        },
                        context_posture=context_packet_record["posture"],
                        context_reduced_reason=context_packet_record.get(
                            "reduced_reason"),
                        assistant_prose=outcome.assistant_prose,
                        proposals=outcome.proposals)
                else:
                    # The DEPRECATED v1 success envelope has room for EXACTLY
                    # these two keys. The envelope's own identities are keyed by
                    # BUFFER KEY, so the one document's key is read rather than
                    # assumed; that lane still carries exactly one document,
                    # which the closed v1 request schema guarantees.
                    #
                    # A RECORDED v1 LIMITATION (contract-v1.38, review F3): this
                    # envelope has ONE `model_id` field and no `selected_model`,
                    # so on a routed turn it cannot state both the requested and
                    # the answering model. It carries the REQUESTED id, which is
                    # what every v1 consumer already reads and revalidates. The
                    # fix is the v2 envelope, which exists; widening a deprecated
                    # closed shape whose whole promise is byte-identical
                    # stability is the one thing contract-v1.34's deprecation
                    # forbids. The SIDECAR on this lane does name the answering
                    # model — it is written above, before this branch, and is not
                    # part of the v1 wire.
                    #
                    # A SECOND RECORDED v1 LIMITATION (contract-v1.39, task
                    # 10.7): this envelope has no `context_packet` either, so a
                    # v1 turn that ran on a REDUCED context cannot say so on the
                    # wire. The reduction is still stated where it always was —
                    # inside the assembled packet, in the prompt's own
                    # declaration section — and the v1 turn still SUCCEEDS,
                    # which is the ratified "MUST NOT make the editors unusable"
                    # half. What a v1 consumer cannot do is READ the posture; the
                    # migration path is the v2 envelope, and widening a
                    # deprecated closed shape is exactly what contract-v1.34's
                    # deprecation forbids.
                    document_key = document_keys[0]
                    success_body = doxbench_turn_success_body(
                        client_turn_id=client_turn_id,
                        assistant_turn_id="assistant-" + digest[:56],
                        model_id=model_id,
                        observed_hashes={
                            "outline": observed.outline.hex,
                            "document": observed.for_key(document_key).hex,
                        },
                        assistant_prose=outcome.assistant_prose,
                        proposals=outcome.proposals)
                if self._doxbench_wire_conforms(
                        validators, success_kind, success_body):
                    body_bytes = json.dumps(success_body).encode("utf-8")
                    # The stored result IS the sent result (byte-identical
                    # replay, contracts/chat-turn.md "Idempotency").
                    #
                    # T104 F4: a `TurnConflictError` here means this slot was
                    # resolved by somebody else while this dispatch ran, so
                    # this answer can NEVER be replayed. Sending it anyway
                    # would put a body on the wire that the store contradicts
                    # -- the caller gets the conflict refusal instead, and the
                    # handler stays alive to write it.
                    try:
                        self.turn_store.complete(
                            key, client_turn_id,
                            {"status": 200, "body": success_body},
                            size_bytes=len(body_bytes))
                    except doxbench_turns.TurnConflictError:
                        self._refuse_turn(validators,
                                          DOXBENCH_ERR_TURN_ID_CONFLICT,
                                          turn_id, failure_kind=failure_kind)
                        return
                    self._send_json(200, success_body)
                    return
                # FAIL CLOSED: a success the released schema refuses must
                # never ship -- it is provider output the validator could not
                # bless, the same class as any other unusable answer.
                outcome_code = DOXBENCH_ERR_RESPONSE_INVALID
            else:
                outcome_code = outcome.error

        status = doxbench_error_status(outcome_code)
        # The RELEASED failure envelope, self-validated before it is either
        # stored or sent: what the turn store retains for a byte-identical
        # replay must be the same validated shape this response carries, or a
        # replay would answer differently from the original.
        body = (doxbench_turn_failure_body(outcome_code, turn_id,
                                           limit=outcome_limit,
                                           kind=failure_kind)
                if turn_id is not None
                else doxbench_error_body(outcome_code, limit=outcome_limit))
        if not self._doxbench_wire_conforms(validators, failure_kind, body):
            body = doxbench_error_body(outcome_code, limit=outcome_limit)
        body_bytes = json.dumps(body).encode("utf-8")
        # Planning-contract obligation 1 (contracts/chat-turn.md): a refused
        # finalization must not abandon the slot -- `fail` frees the
        # conversation key for a later attempt even on this always-fixed
        # dispatch-boundary refusal.
        #
        # T104 F4: if the slot is already gone (another thread resolved it),
        # the bookkeeping cannot be done -- but this request's verdict was
        # computed and self-validated above, so it is still answered. A
        # store-side conflict must never turn a decided refusal into a dropped
        # connection.
        try:
            self.turn_store.fail(key, client_turn_id,
                                 {"status": status, "body": body},
                                 size_bytes=len(body_bytes))
        except doxbench_turns.TurnConflictError:
            pass
        self._send_json(status, body)

    def _deadline_bound_dispatch(self, port, prompt_envelope, model_entry,
                                 proposal_validator):
        """Run `doxbench_model.dispatch_turn` under the adapter's OWN declared
        deadline (PR #63 review, Codex P1). A hung adapter cannot pin the
        HTTP thread or the conversation slot: the worker is a daemon thread,
        the wait is bounded by the validated timeout plus a small fixed
        grace for the wrapper's bookkeeping, and an overrun returns the SAME
        fixed model_timeout outcome dispatch_turn itself would map. The late
        result is discarded unread (FR-020/FR-022)."""
        from ideation_dashboard import doxbench_model
        try:
            deadline = doxbench_model.validated_timeout_seconds(
                port.timeout_seconds)
        except doxbench_model.AdapterTimeoutError:
            # Misdeclared adapters keep dispatch_turn's own fixed mapping
            # (model_failed, no dispatch) — run it inline; nothing can hang
            # because the declared-timeout gate refuses before any dispatch.
            return doxbench_model.dispatch_turn(
                port, prompt_envelope, entry=model_entry, clock=time.monotonic,
                proposal_validator=proposal_validator)
        holder = {}

        def _run():
            try:
                holder["outcome"] = doxbench_model.dispatch_turn(
                    port, prompt_envelope, entry=model_entry,
                    clock=time.monotonic,
                    proposal_validator=proposal_validator)
            except Exception:
                # PR-stabilization R3: a worker-thread exception is an
                # ADAPTER FAILURE, not a timeout — misreporting it as 504
                # would replay the wrong verdict forever. Text dropped
                # unread (FR-020/FR-022).
                holder["raised"] = True

        worker = threading.Thread(target=_run, daemon=True)
        worker.start()
        worker.join(timeout=deadline + 0.25)
        if holder.get("raised"):
            return doxbench_model.TurnDispatchFailure(
                error=DOXBENCH_ERR_MODEL_FAILED,
                diagnostic="the provider failed and its details are withheld by design")
        if worker.is_alive() or "outcome" not in holder:
            return doxbench_model.TurnDispatchFailure(
                error=DOXBENCH_ERR_MODEL_TIMEOUT,
                diagnostic="the provider did not answer within the declared timeout")
        return holder["outcome"]

    def _session_repository(self):
        """The repository half of the `(repository, session-branch)` key.

        BOUND ONCE PER PROCESS, at `build_server`, to the SERVED checkout's own
        repository — the value `_bootstrap_session_entries` registered this
        process's live sessions under (PR #49 second-review finding R2-11).

        It used to be read from `registry.active` per request, and `active` is
        precisely what the HUMAN moves: on a `--local-index` plane one legitimate
        `POST /actions/refresh` naming ANOTHER repository promotes that entry
        (`_regenerate` does that for any publishable ref, correctly), and from then
        on every session verb was keyed on it. Reproduced end to end:
        `edit-document` answered 409 `repository_mismatch` claiming "this dashboard
        serves 'repoB'" about a served checkout that IS repoA, and `propose` —
        deliberately outside `refuse_foreign_repository`, being a main-resident
        verb — proceeded over an unmerged live session, which is the exact D15 /
        FR-023 hazard.

        A session lives in ONE tree: the served checkout. Which snapshot the human
        is looking at is a view, and a view cannot re-key a session. Two
        repositories can still carry the same tile id, so the repository half is
        still mandatory (FR-037, spec C9) — it is simply not a per-request read.

        The fallbacks below are for a handler built WITHOUT `build_server` (the
        hand-constructed handlers in tests), which has no session bootstrap either:
        the source's own baked repository first, and only then the active entry."""
        if self.session_repository:
            return str(self.session_repository)
        baked = getattr(self.source, "baked_repository", None) if self.source else None
        if baked:
            return str(baked)
        entry = self._active_entry()
        return str(entry.repository) if entry is not None else None

    def _query_key(self) -> tuple[str | None, str | None]:
        """The optional `?repository=&ref=` of a read route. Absent repository
        means the ACTIVE entry — which is what every pre-existing caller sends,
        so today's behaviour is unchanged."""
        query = urllib.parse.urlsplit(self.path).query
        params = urllib.parse.parse_qs(query)
        repository = (params.get("repository") or [None])[0]
        ref = (params.get("ref") or [None])[0]
        return repository, ref

    def _route(self, head_only: bool) -> bool:
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == self.snapshot_route:
            self._serve_snapshot(head_only)
            return True
        if path == SNAPSHOT_INDEX_ROUTE:
            self._serve_index(head_only)
            return True
        if path == PROJECT_REGISTER_ROUTE:
            self._serve_project_register(head_only)
            return True
        if path == CAPABILITIES_ROUTE:
            # The loopback console token is process-launch authority. Never
            # disclose it to a DNS-rebinding Host, even though the connection
            # itself arrived on the loopback socket.
            if self.console_token and not self._trusted_console_host():
                self._send_json(403, {"ok": False, "error": "invalid_host",
                                      "message": "the request Host is not this "
                                                 "loopback console"})
                return True
            # THE ONE REPOSITORY THIS SERVE CAN WRITE TO, reported from the
            # SAME authority a create is refused against (`_session_repository`
            # — a session lives in one tree, the served checkout), so the
            # capability and the refusal can never disagree. Resolved per
            # request rather than at startup, because the registry that answers
            # it is not populated when the capability dict is built.
            #
            # The browser used to have to GUESS this, and under a composed
            # project view it guessed the PROJECT id — not a repository at all,
            # and refused. A serve knows what it serves, so it says so.
            payload = dict(self.capabilities)
            writable = self._session_repository()
            if writable:
                payload["repository"] = str(writable)
            # THE HOSTED ACTOR (add-dashboard-account-menu), resolved PER REQUEST
            # beside `repository`, `None` when the header is absent. Read from the
            # gateway-stamped `X-Auth-Request-User` header; DISPLAY-ONLY — the
            # dox-auth gateway remains the identity authority (it strips any
            # client value before stamping its own), and the dashboard's trust in
            # this header rests entirely on the NetworkPolicy boundary that lets
            # only the gateway reach it. It feeds NO capability verdict and NO
            # route consults it to authorize: reading a stamped identity for
            # display does not make this credential-free surface a credential
            # holder or an auth authority (design D16 nuance).
            payload["hosted_actor"] = self.headers.get("X-Auth-Request-User") or None
            self._serve_bytes(json.dumps(payload).encode("utf-8"),
                              JSON_CTYPE, head_only)
            return True
        if path == WORKBENCH_MODEL_CATALOG_ROUTE:
            self._handle_workbench_model_catalog(head_only)
            return True
        if path == WORKBENCH_THREAD_ROUTE:
            self._handle_workbench_thread(head_only)
            return True
        if path.startswith(SOURCE_PREFIX):
            self._serve_source(path[len(SOURCE_PREFIX):], head_only)
            return True
        if path == "/source" or path == "/source/":  # no file named -> reject
            self.send_error(404, "no source path")
            return True
        return False

    def do_GET(self):  # noqa: N802
        if not self._route(head_only=False):
            super().do_GET()

    def do_HEAD(self):  # noqa: N802
        if not self._route(head_only=True):
            super().do_HEAD()

    # ---- write route (v2 seam): the loopback-only "Open in NotebookLM" action ----
    # RESPONSE DISCIPLINE: every error body is {"error": <catalog code>,
    # "message": <catalog fixed string>} — request-derived data (tile ids,
    # nlm stderr) NEVER enters a response; diagnostics go to the server log.
    def do_POST(self):  # noqa: N802
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == ACTIONS_NOTEBOOK_ROUTE:
            self._handle_notebook_action()
            return
        if path == ACTIONS_REFRESH_ROUTE:
            self._handle_refresh_action()
            return
        if path == ACTIONS_DTN_SEED_ROUTE:
            self._handle_dtn_seed()
            return
        if path == ACTIONS_STAGING_SEED_ROUTE:
            self._handle_staging_seed()
            return
        if path == ACTIONS_APPLY_REGISTER_EDITS_ROUTE:
            self._handle_apply_register_edits()
            return
        if path == ACTIONS_EDIT_ROUTE:
            self._handle_edit_action()
            return
        if path == ACTIONS_WORKBENCH_CHAT_TURN_ROUTE:
            self._handle_workbench_chat_turn()
            return
        if path.startswith(ACTIONS_GATE_PREFIX):
            self._handle_gate_action(path[len(ACTIONS_GATE_PREFIX):])
            return
        self._send_error_code(action_errors.ERR_UNKNOWN_ACTION)

    # ---- select-to-edit route (US8 T030; the dashboard itself writes nothing) ----
    def _handle_edit_action(self) -> None:
        """Launch the selected source file in the human's local editor.

        The route deliberately shares the human-console boundary with session
        verbs: loopback + real checkout + resolved actor + per-serve token. The
        target is resolved through the selected registry entry, so neither a
        traversal nor a repository/ref mismatch can fall back to another root.
        """
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "select-to-edit is loopback-only"})
            return
        if not self.capabilities.get("actions", {}).get("edit") or not self.actor:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "select-to-edit is unavailable "
                                             "(no resolved actor/checkout)"})
            return
        console_refusal = self._not_the_human_console()
        if console_refusal is not None:
            sys.stderr.write(
                f"[actions/edit] agent_invocation refused: {console_refusal}\n")
            self._send_json(403, {"ok": False, "error": "agent_invocation",
                                  "message": AGENT_INVOCATION_REFUSAL})
            return
        fields, body_error = _edit_request_fields(self._read_json_body())
        if fields is None:
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": body_error or JSON_OBJECT_BODY_REQUIRED})
            return
        path, repository, ref = fields

        entry = _resolved_listed_edit_entry(self.source, path, repository, ref)
        if entry is None:
            self._send_json(404, {"ok": False, "error": "document_unavailable",
                                  "message": "the selected document is unavailable"})
            return

        editor = os.environ.get("EDITOR")
        # Tests install a recorder on this server instance. Production preserves
        # the console for a configured terminal editor; only the desktop-opener
        # fallback is detached with its streams closed.
        launcher = getattr(self.server, "editor_launcher", None) or (
            lambda command: _launch_editor(
                command, configured_editor=bool(editor)))
        try:
            from ideation_dashboard import authoring
            argv = authoring.edit_command(entry.source_root, path, editor=editor)
            launcher(argv)
        # The wire response is fixed; full detail stays in the local server log.
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(
                f"[actions/edit] editor launch failed: {type(exc).__name__}: {exc}\n")
            self._send_json(500, {"ok": False, "error": "editor_launch_failed",
                                  "message": "the editor could not be opened; "
                                             "see the server log"})
            return
        self._send_json(200, {"ok": True, "path": path})

    # ---- refresh route (add-dashboard-repo-selector, design D7) ----
    def _handle_dtn_seed(self) -> None:
        """Draft a DTN candidate-register seed from a project's SHARED
        IDENTITIES (add-shared-identity-seeds): the identities two or more of
        the named member repositories carry, which is the promotion process's
        first candidate rule computed rather than eyeballed.

        WRITES NOTHING. The response is the register row + detail section as
        TEXT, in the register's own format and numbering, for a human to
        merge — the same seed-first discipline the neutrality-drift lane
        records. That is why this route asks for loopback but not the gate
        capability, and why it can answer while a composed, read-only view is
        on screen.

        The carriers are recomputed HERE from the serve's own composed view;
        the client names the project, the visible subset, and (optionally)
        the exact carrier COMBINATION a lens region stands for — never the
        evidence itself. `combination` is what keeps a seed honest to the
        region it was drafted from: a row reading "carried by 3" drafts those
        identities and no others."""
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "seed drafting is loopback-only"})
            return
        body = self._read_json_body()
        if body is None:
            return
        project = str(body.get("project_id") or "").strip()
        if not project:
            self._send_json(400, {"ok": False, "error": "bad_request",
                                  "message": "project_id is required"})
            return
        repositories = body.get("repositories")
        combination = body.get("combination")
        for name, value in (("repositories", repositories),
                            ("combination", combination)):
            if value is not None and not isinstance(value, list):
                self._send_json(400, {"ok": False, "error": "bad_request",
                                      "message": f"{name} must be a list"})
                return
        if self.source is None:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "no snapshot source on this plane"})
            return
        composed = self.source.compose_view(project)
        if composed is None:
            self._send_json(404, {"ok": False, "error": "unknown_project",
                                  "message": f"no composed view for {project!r}"})
            return

        import datetime
        from doc_health import shared_identity as si
        rows = si.shared_identities(composed.get("documents"),
                                    repositories=repositories,
                                    exactly=combination)
        if not rows:
            self._send_json(200, {
                "ok": False, "error": "nothing_shared",
                "message": "no document identity is carried by two or more of "
                           "the named repositories — there is no candidate to "
                           "draft, which is itself the honest answer"})
            return
        register = Path(self.checkout_root) / si.REGISTER_PATH
        try:
            register_text = register.read_text(encoding="utf-8")
        except OSError:
            register_text = ""       # no register reachable: number from zero
        draft = si.draft_seed(
            register_text, rows, project=project,
            as_of=datetime.date.today().isoformat())
        payload = draft.as_dict()
        payload["ok"] = True
        payload["register"] = si.REGISTER_PATH
        self._send_json(200, payload)

    def _handle_staging_seed(self) -> None:
        """Draft a STAGING-QUEUE fragment from the documents the human selected
        in the lens matrix (Brett, 2026-08-08: "I should have a checkbox on
        each one to generate the seed from checked").

        WRITES NOTHING, like the register seed beside it: the response is the
        fragment as TEXT plus the path it belongs at. That is why this route
        asks for loopback but not the gate capability, and why it can answer
        while a read-only composed view is on screen.

        The client names the DOCUMENTS; their terms and repositories are read
        HERE from the serve's own snapshot. A client that could supply the
        terms could draft a fragment claiming a convergence the corpus does
        not have, and the fragment's whole value is that its evidence is
        checkable against the tree.
        """
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "seed drafting is loopback-only"})
            return
        body = self._read_json_body()
        if body is None:
            return
        project = str(body.get("project_id") or "").strip()
        wanted = body.get("documents")
        if not isinstance(wanted, list) or not wanted:
            self._send_json(400, {"ok": False, "error": "bad_request",
                                  "message": "documents must be a non-empty list"})
            return
        if self.source is None:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "no snapshot source on this plane"})
            return

        # a composed project view when the plane has one, else the active
        # snapshot — the keyword lens runs on both, so the seed must too
        snapshot = self.source.compose_view(project) if project else None
        if snapshot is None:
            entry = self.source.registry.resolve(None)
            snapshot = entry.read_json() if entry is not None else None
        if not isinstance(snapshot, dict):
            self._send_json(404, {"ok": False, "error": "unknown_project",
                                  "message": "no snapshot to read the "
                                             "selected documents from"})
            return

        by_id = {}
        for doc in snapshot.get("documents") or []:
            if not isinstance(doc, dict):
                continue
            for key in (doc.get("id"), doc.get("path")):
                if key:
                    by_id.setdefault(str(key), doc)
        rows, missing = [], []
        for name in wanted:
            doc = by_id.get(str(name))
            if doc is None:
                missing.append(str(name))
            else:
                rows.append(doc)
        if missing:
            self._send_json(404, {
                "ok": False, "error": "unknown_document",
                "message": "not in this snapshot: " + ", ".join(missing[:5])})
            return

        import datetime
        from doc_health import staging_seed as ss
        existing = []
        staging_root = Path(self.checkout_root) / ss.STAGING_DIR
        try:
            existing = sorted(p.name for p in staging_root.iterdir() if p.is_dir())
        except OSError:
            existing = []       # no queue reachable: no collision to avoid
        draft = ss.draft_staging_seed(
            rows, project=project or (snapshot.get("repository") or "corpus"),
            as_of=datetime.date.today().isoformat(),
            repository=str(snapshot.get("repository") or "openxFactory"),
            existing=existing)
        payload = draft.as_dict()
        payload["ok"] = True
        payload["index"] = ss.STAGING_INDEX
        self._send_json(200, payload)

    def _handle_apply_register_edits(self) -> None:
        """Run the register-edit fulfilment lane once
        (add-register-edit-lane): apply every dispatched
        project-register-edit commission, validate, deliver, commit + push
        the register file alone. Loopback + gate-actor only — the same
        human-console boundary as the gate verbs — and only RECORDED
        commissions are ever applied."""
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "applying register edits is "
                                             "loopback-only"})
            return
        if not self.capabilities.get("actions", {}).get("gate") or not self.actor:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "applying register edits needs "
                                             "the human gate capability"})
            return
        from ideation_dashboard.register_edit_lane import fulfil_once
        try:
            report = fulfil_once(Path(self.checkout_root))
        except Exception as exc:  # noqa: BLE001 - a lane crash must answer, not hang
            self._send_json(500, {"ok": False, "error": "lane_failed",
                                  "message": str(exc)[:300]})
            return
        payload = report.as_dict()
        payload["ok"] = report.error is None
        self._send_json(200 if payload["ok"] else 409, payload)

    def _handle_refresh_action(self) -> None:
        """ONE affordance, TWO bindings, chosen by the PLANE and never by the
        client body (a client cannot ask a served plane to regenerate, nor a
        local plane to re-fetch). Fail-closed: no binding refuses before any body
        parse, and the writing binding refuses off-loopback.

        UNGATED by ruling (D7 / open question 3's recommendation, stated
        explicitly): the artifact is derived, regeneration mutates nothing
        governed, and no build, rollout, or publication path exists here (D1)."""
        binding = self.capabilities.get("refresh", {}).get("binding")
        if not binding or self.source is None:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "refresh is unavailable on this plane "
                                             "(no data source and no served checkout)"})
            return
        if binding != registry_mod.BINDING_REFETCH and not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "the regenerate binding is loopback-only"})
            return
        body = self._read_json_body()
        if body is None:
            body = {}  # a plain POST means "refresh the active snapshot"
        if not isinstance(body, dict):
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": JSON_OBJECT_BODY_REQUIRED})
            return
        repository = body.get("repository")
        ref = body.get("ref")
        if repository is not None and not isinstance(repository, str):
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": "repository must be a string"})
            return
        if ref is not None and not isinstance(ref, str):
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": "ref must be a string"})
            return
        # FR-048 again, on the one WRITE-ish route reachable off-loopback: the
        # read-only `refetch` binding is available on the hosted plane by design,
        # so a hosted client could otherwise ask it to refresh a session ref.
        # (`regenerate` has already refused above, being loopback-only.)
        if hosted_ref_refused(self.loopback, ref):
            self._send_json(403, {"ok": False, "error": "session_unavailable",
                                  "message": HOSTED_SESSION_REFUSAL})
            return
        self._run_refresh(repository, ref)

    def _run_refresh(self, repository: str | None, ref: str | None) -> None:
        """Run the binding. EVERY failure keeps the registry as it was, so the
        previously rendered snapshot stays renderable and the client reports the
        failure inline (spec scenario "A refresh fails")."""
        try:
            result = self.source.refresh(repository=repository, ref=ref)
        except registry_mod.PublicationRefused:
            self._send_json(403, {"ok": False, "error": "publication_refused",
                                  "message": "a non-main snapshot is never published"})
            return
        except registry_mod.DataSourceError as exc:
            sys.stderr.write(f"[actions/refresh] data source unreachable: {exc}\n")
            self._send_json(502, {"ok": False, "error": "source_unreachable",
                                  "message": "the data source could not be read; "
                                             "the previous snapshot is still shown"})
            return
        except ValueError as exc:
            sys.stderr.write(f"[actions/refresh] {exc}\n")
            self._send_json(404, {"ok": False, "error": "unknown_snapshot",
                                  "message": "no such (repository, ref) is registered"})
            return
        except Exception:  # noqa: BLE001 — never leak a traceback over the wire
            self._send_json(500, {"ok": False, "error": "action_failed",
                                  "message": "refresh failed; see the server log"})
            return
        # Keep the handler's own divergence anchor in step with the new active
        # snapshot, so a subsequent read reports the refreshed revision.
        active = self._active_entry()
        if active is not None:
            type(self).source_revision = active.source_revision
        self._send_json(200, {"ok": True, **result})

    # ---- the human-console test (FR-019's third clause) ----
    def _trusted_console_host(self) -> bool:
        """Whether ``Host`` names this server's bound loopback port."""
        raw = str(self.headers.get("Host") or "").strip().lower()
        return raw in loopback_authorities(int(self.server.server_address[1]))

    def _own_origin_authorities(self) -> set[str]:
        """The `host:port` spellings a request from THIS serve's own page can
        legitimately name. Derived from the bound port, never from the request's
        untrusted ``Host``, so DNS rebinding cannot define its own origin."""
        return set(loopback_authorities(int(self.server.server_address[1])))

    def _foreign_origin(self) -> bool:
        """Whether the caller declares an origin that is not this serve's own.
        A caller that declares NONE (a plain `curl`) is not exonerated here — the
        token check below is what refuses it; this closes the browser class."""
        for header in ("Origin", "Referer"):
            raw = str(self.headers.get(header) or "").strip()
            if not raw or raw == "null":
                continue
            parts = urllib.parse.urlsplit(raw)
            if (parts.netloc
                    and parts.netloc.lower() not in self._own_origin_authorities()):
                return True
        return False

    def _not_the_human_console(self) -> str | None:
        """Why this request is not the human console, or None when it is.

        The reason is for the SERVER LOG (FR-019 says reject AND report); the wire
        gets one fixed sentence, keeping this module's response discipline —
        request-derived data never reaches a response body."""
        expected = self.console_token
        if not expected:
            return "this plane minted no console token (no session capability)"
        if not self._trusted_console_host():
            return "the request Host does not name this loopback console"
        ctype = str(self.headers.get("Content-Type") or "")
        # T098 finding fix (operator ruling (a), spec Clarifications
        # 2026-07-31): the clause exists to prove the request is NOT a
        # cross-origin "simple request". A JSON Content-Type proves it — and
        # so does the PRESENCE of the custom console-token header, which
        # forces a CORS preflight on every browser. Presence satisfies only
        # THIS clause; the token's VALIDITY (compare_digest below), Host
        # trust, and foreign-origin checks refuse independently, unchanged.
        token_bearing = bool(str(self.headers.get(CONSOLE_TOKEN_HEADER) or ""))
        if not token_bearing and not ctype.split(";", 1)[0].strip().lower().startswith(
                JSON_CONTENT_TYPE_PREFIX):
            return "the request is not a JSON submission (a cross-origin simple request cannot be)"
        if self._foreign_origin():
            return "the request declares a foreign origin"
        presented = str(self.headers.get(CONSOLE_TOKEN_HEADER) or "")
        if not presented:
            return "no console token was presented"
        if not presented.isascii():
            # compare_digest raises on non-ASCII str (headers decode as
            # latin-1) — refuse fixed instead of dropping the connection.
            return "the console token is not a valid token"
        if not secrets.compare_digest(presented, expected):
            return "the console token does not match this serve's"
        return None

    # ---- executing gate routes (add-ideation-intent-plane §3, D5 local-first) ----
    def _handle_gate_action(self, verb: str) -> None:
        """Loopback-only human console verbs over the gate engine. Fail-closed:
        off-loopback, capability-off, and NON-CONSOLE callers all refuse before
        any body parse — the three clauses of FR-019, in that order, so the two
        older refusals keep the exact codes their tests pin."""
        if not self.loopback:
            self._send_json(403, {"ok": False, "error": "loopback_only",
                                  "message": "gate actions are loopback-only"})
            return
        if not self.capabilities.get("actions", {}).get("gate") or not self.actor:
            self._send_json(403, {"ok": False, "error": "action_unavailable",
                                  "message": "gate actions unavailable "
                                             "(no resolved actor/checkout)"})
            return
        from ideation_dashboard import gate_console
        from ideation_dashboard import gate_routes
        # The console-presence test, run ONCE for every verb — a pure read of this
        # request's own headers, with no side effect. It answers two questions that
        # used to be one:
        #
        #   (a) ENFORCEMENT — FR-019's third clause, on the verbs this feature
        #       added (the session verbs, whose side effects are a worktree, a
        #       branch, and a remote write with the engineer's own credential). The
        #       pre-existing verbs keep their pre-existing posture: widening the
        #       REFUSAL to them is a separate decision with its own compatibility
        #       surface, and is NOT smuggled in here.
        #   (b) PROVENANCE (D23; Brett's 2026-07-27 ruling item 3) — the fact this
        #       handler is the only place that knows: this action arrived on the
        #       HTTP surface, and its console presence was shown by THIS SERVE'S
        #       token. Observing it for every verb is what makes the record say
        #       which door the action came through, which is the whole point; it
        #       adds no refusal anywhere, so no pre-existing verb changes behaviour.
        #
        # A verb whose presence was not shown and is not enforced (a pre-existing
        # verb over a non-console call) gets NO provenance rather than a guessed
        # one: the vocabulary deliberately has no value meaning "not shown", and
        # inventing one here would be the invisible residual again in a new place.
        console_refusal = self._not_the_human_console()
        if verb in gate_routes.SESSION_BEARING_VERBS and console_refusal is not None:
            sys.stderr.write(
                f"[actions/gate] agent_invocation refused ({verb}): "
                f"{console_refusal}\n")
            self._send_json(403, {"ok": False, "error": "agent_invocation",
                                  "message": AGENT_INVOCATION_REFUSAL})
            return
        provenance = (gate_console.HTTP_CONSOLE_TOKEN
                      if console_refusal is None else None)
        # T104 F5-6: `first-edit` is the governed Save -- its body carries the
        # document's FULL replacement text, and both sides declare the buffer
        # bound at `doxbench_hash.MAX_BUFFER_BYTES` (400,000 UTF-8 bytes;
        # doxbench-state.js `DOXBENCH_MAX_BUFFER_BYTES` agrees). The global
        # `_MAX_BODY_BYTES` reader below (65,536 -- "a tile-action body is
        # tiny") therefore refused a legal ~70KB Save at the TRANSPORT, and
        # with the misleading "a JSON object body is required" because that
        # reader collapses "too large" into the same bare None as any other
        # malformation. This ONE verb -- branched on the URL-path verb, before
        # any body byte is read -- goes through the widened route-specific
        # reader instead. The cap REUSES `DOXBENCH_MAX_REQUEST_BYTES`
        # (1,048,576) rather than minting a new number: that constant is
        # already sized to carry a full declared buffer plus JSON-escaping
        # inflation and envelope overhead for the chat-turn route, and a Save
        # posts exactly that payload class (the derivation is pinned by
        # test_the_first_edit_cap_accommodates_the_declared_buffer_bound).
        # Every OTHER gate verb keeps the tiny cap deliberately: their bodies
        # ARE tiny, and widening them would weaken unrelated actions
        # (research R7's reasoning, unchanged).
        if verb == "first-edit":
            body, size_refusal = self._read_bounded_json_body(
                DOXBENCH_MAX_REQUEST_BYTES, "request_body_bytes")
            if size_refusal is not None:
                # The verdict for a genuinely oversize Save names the SIZE
                # problem (fixed message + limit block), never the "JSON
                # object body" misdirection. Wave re-review P3 honesty note:
                # the limit block's `measured` figure is the DECLARED
                # Content-Length — the reader refuses on the declaration and
                # drains without buffering, so the declaration is exactly
                # what this refusal is based on (see `_read_bounded_json_body`).
                self._send_json(
                    doxbench_error_status(DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED),
                    doxbench_error_body(DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
                                        limit=size_refusal))
                return
        else:
            body = self._read_json_body()
        if not isinstance(body, dict):
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": JSON_OBJECT_BODY_REQUIRED})
            return
        try:
            status, payload = gate_routes.run_gate_action(
                verb, body, checkout_root=Path(self.checkout_root),
                actor=self.actor,
                index_validator=self.gate_index_validator,
                snapshot_path=Path(self.snapshot_path),
                manifest_validator=self.gate_manifest_validator,
                xref_validator=self.gate_xref_validator,
                # BRANCH SESSIONS (007-workbench-branch-sessions T025, research
                # R1): `checkout_root` above is the SERVED root and stays that
                # way — no session operation may move it (FR-004). The gap R1
                # found was that the route had no other input, so it could not
                # tell which tree a write belonged to. These two close it: the
                # registry is where session LIVENESS lives (FR-008) and the
                # repository is the other half of its key. The route resolves the
                # session EXPLICITLY from them plus the body's tile scope — it
                # never assumes the active entry is the session, because the
                # active entry is whatever the human is LOOKING at.
                session_registry=self._session_registry(),
                repository=self._session_repository(),
                session_notebook=self._session_notebook(),
                # The remote-write port (T082): declared on this LOOPBACK plane and
                # nowhere else, because its identity is a personal credential
                # (FR-034, D22). Without it the workbench's save affordance could
                # not fire at all; with it on a hosted plane the whole confinement
                # would be void — which is why the same capability answers both.
                session_pull_requests=self._session_pull_requests(),
                # THE GATEWAY FACT (D23). Observed above from this request's own
                # headers and handed down; nothing below re-derives it, and no
                # request body can spell it — `run_gate_action` reads it from this
                # argument only, and the value is a `Provenance` type a body
                # could never be.
                provenance=provenance)
        except Exception as exc:  # noqa: BLE001 — never leak a traceback over the wire
            # THE LOG THE MESSAGE NAMES (T092 acceptance sweep, defect 3). This
            # clause used to send that message and write NOTHING anywhere: the
            # server log was byte-identical before and after three separate 500s,
            # so a human hitting any gate failure had no way at all to find out
            # what happened — and neither did the sweep, which had to reproduce
            # each one through the CLI to see a traceback. `http.server`'s own
            # request logging is suppressed by `log_message` above, so this is the
            # only place the fact can be recorded.
            #
            # The WIRE response is unchanged, deliberately and to the byte: the
            # fixed catalog message, no exception text, no request-derived value.
            # The traceback goes to stderr ONLY — the same channel and the same
            # `[actions/<route>] ` prefix the notebook route already uses (which is
            # what proved this a real gap rather than an environment artifact: in
            # the same run, the same log carried nlm's real reason verbatim).
            self._log_gate_failure(verb, exc)
            self._send_json(500, {"ok": False, "error": "action_failed",
                                  "message": "gate action failed; see the "
                                             "server log"})
            return
        self._send_json(status, payload)

    def _log_gate_failure(self, verb: str, exc: BaseException) -> None:
        """The unexpected-exception half of a gate 500, on the server's stderr.

        Three things, because each answers a different question the sweep had to
        answer by hand: WHICH verb (the wire response cannot say — it is one fixed
        message for every verb), WHAT kind of failure (an `OSError` from a
        derived path and a bug in a route are not the same incident), and the
        TRACEBACK. `verb` is a route-dispatch value from the fixed
        `EXECUTING_VERBS` set, not free request text; nothing else from the
        request reaches even this channel."""
        sys.stderr.write(
            f"[actions/gate] unexpected failure in {verb}: "
            f"{type(exc).__name__}: {exc}\n")
        traceback.print_exception(type(exc), exc, exc.__traceback__,
                                  file=sys.stderr)
        sys.stderr.flush()

    def _send_json(self, status: int, obj: dict) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", JSON_CTYPE)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_error_code(self, code: str) -> None:
        """One structured refusal: status + body both come from the fixed error
        catalog, so no request-derived value can reach the response."""
        status, _message = action_errors.ERROR_CATALOG[code]
        self._send_json(status, action_errors.error_body(code))

    def _read_json_body(self):
        """Parse a capped JSON request body, or None on any malformation. Never
        trusts Content-Length beyond the cap — a tile-action body is tiny."""
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except (TypeError, ValueError):
            return None
        if length <= 0:
            return None
        if length > _MAX_BODY_BYTES:
            # DRAIN the refused body before answering (T104 F5/F8 — the
            # carried "65kb test" flake, closed at its root). Refusing with
            # every byte unread closed the socket on a client still mid-body,
            # and the kernel's reset could destroy the queued 400 before the
            # client read it — the refusal raced its own transport.
            _drain_refused_body(self.rfile, length)
            return None
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (OSError, ValueError):  # UnicodeDecodeError is a ValueError
            return None


    def _read_bounded_json_body(self, max_bytes: int, dimension: str):
        """Route-specific bounded JSON body reader (T024, research R7).

        UNLIKE `_read_json_body` above — which stays EXACTLY as it is, at the
        existing 65,536-byte global cap, for every route that already exists
        — this reader is PARAMETERISED per call site. The doxBench chat-turn
        route passes its own `max_bytes` and a fixed `dimension` name for the
        measured-limit verdict FR-017 requires.

        Returns `(payload, refusal)`:
          * success -> `(<dict>, None)`;
          * OVER the bound -> `(None, {"dimension": dimension, "measured": N,
            "maximum": max_bytes})` — a quantified verdict (FR-017), unlike
            this class's OTHER reader, whose bare `None` is exactly what
            research R7 says a global cap loses. `N` here is the DECLARED
            Content-Length (the refusal's actual basis — see the over-bound
            branch), not a count of buffered bytes;
          * any OTHER malformation (missing/unparseable `Content-Length`, a
            short read, invalid UTF-8, non-JSON, or JSON that is not an
            object) -> `(None, None)` — no measurement to report, and NOTHING
            request-derived (no body text, no header value) is ever returned
            in either element.

        Measurement is EXACT BYTES, never decoded characters (research R4's
        exact-byte discipline applies to request bounds too: a multi-byte
        UTF-8 body can be over the byte bound while under a code-point count,
        and the reverse must never be mistaken for a refusal). A lying
        `Content-Length` is never trusted for the READ itself: at most
        `max_bytes + 1` bytes are ever pulled off the socket, however large a
        declared length claims, so a flood cannot buffer past the bound
        merely by declaring a bigger number."""
        try:
            declared = int(self.headers.get("Content-Length", "0"))
        except (TypeError, ValueError):
            return None, None
        if declared <= 0:
            return None, None
        if declared > max_bytes:
            # Drain the refused body (W-6: this reader used to pull only
            # max_bytes + 1 and abandon the remainder on the socket, so the
            # measured 413 could still be destroyed by the close-with-unread
            # reset — the same race the tiny reader's drain closes). Same
            # shared posture: chunked, bounded, and backed by the socket
            # timeout so a stalled sender raises instead of holding the
            # thread.
            #
            # Wave re-review P3 honesty note: the `measured` value below is
            # the DECLARED Content-Length, not a count of bytes read — an
            # over-cap body is refused on its declaration precisely so it is
            # never buffered to be counted. That is the honest basis of this
            # refusal: the caller declared more than the bound admits.
            _drain_refused_body(self.rfile, declared)
            return None, {"dimension": dimension, "measured": declared,
                          "maximum": max_bytes}
        try:
            raw = self.rfile.read(declared)
        except OSError:
            return None, None
        if len(raw) != declared:
            return None, None  # a short read: fewer bytes arrived than declared
        try:
            text = raw.decode("utf-8")
        except ValueError:  # UnicodeDecodeError is a ValueError
            return None, None
        try:
            payload = json.loads(text)
        except ValueError:
            return None, None
        if not isinstance(payload, dict):
            return None, None
        return payload, None

    def _make_adapter(self):
        """The notebook adapter this server was BUILT with, or None.

        There is no fallback to the real `nlm`-backed adapter here (PR #49
        hardening item 1): a server is handed its adapter by whoever built it, so
        an undeclared adapter is absence rather than an implicit reach for the
        shared NotebookLM account. `_probe_nlm` keeps the `notebook` capability in
        step with exactly this decision, so a route that checks the capability
        first can never arrive here holding None."""
        if self.adapter_factory is None:
            return None
        return self.adapter_factory()

    def _handle_notebook_action(self) -> None:
        if not self.loopback:
            self._send_error_code(action_errors.ERR_LOOPBACK_ONLY)
            return
        if not self.capabilities.get("actions", {}).get("notebook"):
            self._send_error_code(action_errors.ERR_ACTION_UNAVAILABLE)
            return
        body = self._read_json_body()
        if not isinstance(body, dict):
            self._send_error_code(action_errors.ERR_INVALID_BODY)
            return
        from ideation_dashboard import notebook_action
        self._run_notebook_action(notebook_action, body.get("tile_kind"), body.get("tile_id"))

    def _run_notebook_action(self, notebook_action, tile_kind, tile_id) -> None:
        try:
            snapshot = json.loads(Path(self.snapshot_path).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            self._send_error_code(notebook_action.ERR_SNAPSHOT_UNAVAILABLE)
            return
        adapter = self._make_adapter()
        if adapter is None:
            # unreachable while the capability agrees with the declaration
            # (`_probe_nlm`), and fail-closed if it ever does not
            self._send_error_code(notebook_action.ERR_ACTION_UNAVAILABLE)
            return
        try:
            result = notebook_action.run_notebook_action(
                tile_kind=tile_kind, tile_id=tile_id, snapshot=snapshot,
                checkout_root=Path(self.checkout_root), adapter=adapter)
        except notebook_action.NotebookActionError as exc:
            self._log_action_failure(exc.code, exc.log_detail)
            self._send_json(exc.status, exc.body())
            return
        except Exception:  # noqa: BLE001
            # never leak a traceback over the wire
            self._send_error_code(notebook_action.ERR_ACTION_FAILED)
            return
        self._send_json(200, result)

    def _log_action_failure(self, code: str, detail: str | None) -> None:
        """Server-side-only diagnostics for a refused/failed action — the wire
        carries only the fixed catalog message; the operator sees the detail."""
        if detail:
            sys.stderr.write(f"[actions/notebook] {code}: {detail}\n")

    # ---- snapshot ----
    def _read_snapshot(self) -> bytes | None:
        """The ACTIVE snapshot's bytes, through the registry when one is bound
        (the in-process derived cache included) and from the configured path
        otherwise."""
        entry = self._active_entry()
        if entry is not None:
            return entry.read_bytes()
        try:
            return Path(self.snapshot_path).read_bytes()
        except OSError:
            return None

    def _serve_snapshot(self, head_only: bool) -> None:
        """`/snapshot.json` — the active snapshot, or any registered
        (repository, ref) named by the query. An unknown pair is a 404; the
        active view the client already has stays untouched.

        On the HOSTED plane a non-`main` ref refuses before resolution (FR-048):
        the serving index legitimately advertises a live session row (FR-014), so
        without this a hosted request could name one."""
        repository, ref = self._query_key()
        if hosted_ref_refused(self.loopback, ref):
            self._send_json(403, {"ok": False, "error": "session_unavailable",
                                  "message": HOSTED_SESSION_REFUSAL})
            return
        if repository and self.source is not None:
            entry = self.source.registry.resolve(repository, ref)
            if entry is None:
                # An AGGREGATE id (declared, or register-derived per project —
                # add-project-merged-projection D11) composes at the default
                # ref only. Off-loopback, members at unpublishable refs are
                # dropped before composition (the hosted_index projection,
                # applied to content).
                composed = None
                if registry_mod.is_publishable_ref(ref):
                    composed = self.source.compose_view(
                        repository, publishable_only=not self.loopback)
                if composed is not None:
                    self._serve_bytes(json.dumps(composed).encode("utf-8"),
                                      JSON_CTYPE, head_only)
                    return
                self.send_error(404, "no such snapshot")
                return
            if self._hosted_entry_refused(entry):
                return
            self._serve_bytes(entry.read_bytes(), JSON_CTYPE, head_only, entry=entry)
            return
        if repository and self.source is None:
            self.send_error(404, "no such snapshot")
            return
        # THE REF-LESS HOLE (PR #49 review finding 14, composing with finding
        # 10b): a request that NAMES no ref resolves to the ACTIVE entry, and
        # `hosted_ref_refused` only ever inspected the ref a request named. A
        # non-`main` active entry would therefore have been served off-loopback
        # with no key in sight. The refusal now follows the RESOLVED entry.
        if self._hosted_entry_refused(self._active_entry()):
            return
        self._serve_bytes(self._read_snapshot(), JSON_CTYPE, head_only)

    def _hosted_entry_refused(self, entry) -> bool:
        """Refuse (and answer) when the entry a request RESOLVED to is
        session-local and this is the hosted plane. Returns whether it answered."""
        if entry is None or not hosted_ref_refused(self.loopback, getattr(entry, "ref", None)):
            return False
        self._send_json(403, {"ok": False, "error": "session_unavailable",
                              "message": HOSTED_SESSION_REFUSAL})
        return True

    def _serve_index(self, head_only: bool) -> None:
        """`/snapshot-index.json` — the roster the selector reads, composed from
        the registry. No registry (a hand-built handler) means no index, which
        is exactly how the renderer degrades to a single snapshot."""
        if self.source is None:
            self.send_error(404, "no snapshot index")
            return
        document = self.source.index_document()
        # belt AND braces on the hosted plane (FR-048, finding 14): the bootstrap
        # above admits no session rows off-loopback, and this projection would
        # drop them anyway — a handler constructed by hand, or a registry a future
        # route populates, cannot reopen the hole.
        if not self.loopback:
            document = hosted_index(document)
        body = json.dumps(document).encode("utf-8")
        self._serve_bytes(body, JSON_CTYPE, head_only)

    def _serve_project_register(self, head_only: bool) -> None:
        """`/project-register.json` — the register PROJECTION the project
        picker reads (add-project-scoped-selection). Read per request (the
        register is human-editable between requests), reduced to the
        navigation fields only, and 404 when no register is reachable — the
        picker hides and the selector renders today's ungrouped roster.

        TWO PLANES in one document (design D-e): `projects` is TRUTH (the
        register), `pending` is INTENT — dispatched, undelivered
        create-project commissions read from the same records scan the
        duplicate guard uses, so a fresh commission is visible as pending
        instead of looking like it did nothing. A pending id the register
        already carries is dropped: the register wins the moment the
        fulfilment lands, even before the descriptor's status flips."""
        import yaml
        from ideation_dashboard.gate_console import DEFAULT_RECORDS_DIR
        from ideation_dashboard.kickoff import (
            dispatched_commission_rows, dispatched_commissions,
            discover_project_register)
        source = discover_project_register(Path(self.checkout_root))
        register = None
        if source is not None:
            try:
                register = yaml.safe_load(source.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                register = None
        if not isinstance(register, dict):
            self.send_error(404, "no project register")
            return
        projects = [
            {"id": p.get("id"), "name": p.get("name") or p.get("id"),
             "repositories": [str(r) for r in (p.get("repositories") or [])]}
            for p in (register.get("projects") or [])
            if isinstance(p, dict) and p.get("id")
        ]
        real_ids = {p["id"] for p in projects}
        records_root = Path(self.checkout_root) / DEFAULT_RECORDS_DIR

        def _job(descriptor):
            try:
                doc = yaml.safe_load(descriptor.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError):
                doc = None
            return doc if isinstance(doc, dict) else {}

        pending = []
        for pid, descriptor in sorted(
                dispatched_commissions(records_root, "create-project").items()):
            if pid in real_ids:
                continue
            job = _job(descriptor)
            pending.append({
                "id": pid,
                "name": job.get("project_name") or pid,
                "repositories": [str(r) for r in (job.get("repositories") or [])],
                "dispatched_at": job.get("dispatched_at"),
            })
        # add-opendox-project-header (D15): dispatched, undelivered MEMBERSHIP
        # edits — the popover badges the affected rows until the fulfilment
        # lands. Same two-plane posture as `pending` above. EVERY queued edit
        # rides (edits queue, topic D18), oldest first — including edits on a
        # project that so far exists only as a pending creation, so the apply
        # affordance's count stays honest; an edit whose project is in
        # neither plane is dropped (nothing to badge).
        pending_ids = {p["id"] for p in pending}
        pending_edits = []
        for pid, _descriptor, job in dispatched_commission_rows(
                records_root, "edit-project"):
            if pid not in real_ids and pid not in pending_ids:
                continue
            pending_edits.append({
                "project_id": pid,
                "add": [str(r) for r in (job.get("add") or [])],
                "remove": [str(r) for r in (job.get("remove") or [])],
                "dispatched_at": job.get("dispatched_at"),
            })
        document = {
            "kind": "project-register-projection",
            "projects": projects,
            "pending": pending,
            "pending_edits": pending_edits,
        }
        self._serve_bytes(json.dumps(document).encode("utf-8"), JSON_CTYPE,
                          head_only)

    # ---- source pass-through ----
    def _keyed_source(self, tail: str):
        """Split an optional `<repository>@<ref>/` prefix off a `/source/` tail.
        The prefix is honoured ONLY when it names a REGISTERED pair, so a real
        file whose first path segment happens to contain `@` still resolves as a
        path. Returns (repository, ref, remaining tail).

        A SESSION ref CONTAINS a slash (`draft/<topic>`, `cluster/<id>`), so the
        key is not always one path segment: the split is tried at every separator,
        shortest prefix first, and the first candidate naming a REGISTERED pair
        wins. Registration remains the whole admission test — an unregistered pair
        falls through to the plain path exactly as before — so widening the split
        cannot make an unknown key addressable. Both spellings work: the browser
        percent-encodes the whole key (`repo%40draft%2Ftopic`, one segment) and the
        runbook's `curl` writes it plainly (`repo@draft/topic`, two)."""
        if self.source is None or "/" not in tail:
            return None, None, tail
        parts = tail.split("/")
        for cut in range(1, len(parts)):
            rest = "/".join(parts[cut:])
            if not rest:
                break
            parsed = registry_mod.parse_key_id(
                urllib.parse.unquote("/".join(parts[:cut])))
            if parsed is None:
                continue
            if self.source.registry.get(*parsed) is not None:
                return parsed[0], parsed[1], rest
        return None, None, tail

    def _serve_source(self, tail: str, head_only: bool) -> None:
        repository, ref, rest = self._keyed_source(tail)
        # the keyed form is the OTHER route that names a ref (FR-048): a hosted
        # plane serves no session worktree's bytes, keyed or not
        if hosted_ref_refused(self.loopback, ref):
            self._send_json(403, {"ok": False, "error": "session_unavailable",
                                  "message": HOSTED_SESSION_REFUSAL})
            return
        entry = None
        if self.source is not None:
            target = self.source.registry.resolve_source(repository, ref, rest)
            entry = self.source.registry.resolve(repository, ref)
            # the UNKEYED form resolves to the ACTIVE entry, which the query never
            # named — the same ref-less hole `_serve_snapshot` closes above
            if self._hosted_entry_refused(entry):
                return
        else:
            target = resolve_source_path(Path(self.checkout_root), rest)
        if target is None:
            self.send_response(404)
            self._divergence_headers(entry)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        try:
            body = target.read_bytes()
        except OSError:
            self.send_error(404, "unreadable source")
            return
        ctype = "text/markdown; charset=utf-8" if target.suffix == ".md" else "text/plain; charset=utf-8"
        self._serve_bytes(body, ctype, head_only, entry=entry)

    def _serve_bytes(self, body: bytes | None, ctype: str, head_only: bool,
                     entry=None) -> None:
        if body is None:
            self.send_error(404, "not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self._divergence_headers(entry)
        self.end_headers()
        if not head_only:
            # Serving file bytes IS this route's function (S5131 justification):
            # the snapshot path is server config (never request data) and every
            # /source path is root-confined by resolve_source_path before it is
            # read — a read-only pass-through, exactly like the stdlib static
            # handler this class extends.
            self.wfile.write(body)  # NOSONAR


# --------------------------- server construction ---------------------------

def served_repository(source) -> str | None:
    """The repository half of THIS PROCESS's session keys (finding R2-11).

    The SERVED CHECKOUT's own identity, not the view's: the baked/local snapshot's
    repository — which `SnapshotSource` reads out of the snapshot file itself when
    no `--repository` is given — because that is the snapshot generated FROM the
    served tree, and the served tree is the only tree a session can live in. The
    active entry is consulted ONLY when there is no baked snapshot at all, and even
    then it is read once, here, rather than per request.

    Public because it is a decision, not a detail: `_bootstrap_session_entries`
    registers the live sessions under this value and every gate dispatch is keyed
    on the same one, so the two cannot drift."""
    baked = getattr(source, "baked_repository", None)
    if baked:
        return str(baked)
    active = getattr(getattr(source, "registry", None), "active", None)
    return str(active.repository) if active is not None else None


def _bootstrap_session_entries(source, checkout_root: Path,
                               repository: str | None = None) -> None:
    """Re-derive THIS PROCESS's live branch-session entries at start-up
    (007-workbench-branch-sessions T033a; FR-008, D10, G13).

    `SnapshotRegistry._entries` is an in-process dict, so a fresh serve starts with
    no session entries at all: without this, a restart mid-session would 404 the
    session ref, the next gate write would open a SECOND session on the same tile,
    the resume-or-new prompt would re-fire, and `propose` would proceed over
    unmerged drafts — the exact D15 hazard. The re-derivation reads the worktree and
    its branch JOINTLY under the sessions container, which D10 already names as the
    session's derivation source, and each half-signal is reported stale for the
    human rather than adopted or cleaned up.

    `repository` is the SERVED checkout's own (`served_repository`) and is the same
    value every gate dispatch is keyed on (finding R2-11); it defaults to that
    resolution rather than to the active entry, which the human moves.

    Never fatal. A served tree with no git, no sessions container, or no resolvable
    repository simply has no sessions, and the dashboard comes up exactly as it did
    before sessions existed."""
    repository = repository or served_repository(source)
    if not repository:
        return
    from ideation_dashboard import branch_session as session_mod
    report = session_mod.bootstrap_sessions(
        source.registry, repository=repository,
        checkout_root=Path(checkout_root))
    for note in report.stale:
        sys.stderr.write(f"[sessions] stale ({note.kind}): {note.reason}\n")
    for message in report.errors:
        sys.stderr.write(f"[sessions] {message}\n")


def _read_source_revision(snapshot_path: Path) -> str | None:
    try:
        data = json.loads(Path(snapshot_path).read_text(encoding="utf-8"))
        return data.get("generation", {}).get("source_revision")
    except (OSError, ValueError, AttributeError):
        return None


def build_server(
    web_dir: Path | str,
    snapshot_path: Path | str,
    checkout_root: Path | str,
    *,
    host: str = DEFAULT_HOST,
    port: int = 0,
    head: str | None = None,
    snapshot_route: str = SNAPSHOT_ROUTE,
    git=None,
    quiet: bool = True,
    adapter_factory=None,
    pull_request_factory=None,
    model_port_factory=None,
    schema_validator_factory=_UNSET_VALIDATOR_FACTORY,
    actor: str | None = None,
    gate_index_validator=None,
    gate_manifest_validator=None,
    gate_xref_validator=None,
    repository: str | None = None,
    ref: str | None = None,
    data_source=None,
    index_name: str = registry_mod.DEFAULT_INDEX_NAME,
    source_roots: dict | None = None,
    local_index: Path | str | None = None,
    project_register: Path | str | None = None,
    peek_ttl_seconds: float = registry_mod.PEEK_TTL_SECONDS,
    snapshot_source=None,
    knowledge_declaration=None,
    packet_assembler=None,
) -> http.server.ThreadingHTTPServer:
    """Build (but do not start) the loopback server. `port=0` binds an ephemeral
    port (read it back from `httpd.server_address`). `head` is injectable so a
    divergence can be exercised without a git checkout. `adapter_factory` is the
    `NotebookAdapter` supplier and it is REQUIRED for a plane to have notebooks
    at all: unset means NO adapter, not "build the real one" (PR #49 hardening
    item 1 — see `real_notebook_adapter`, which the entrypoints declare). It also
    drives the startup `notebook` capability verdict, keeping capability and
    behaviour consistent. `pull_request_factory` is the same kind of seam for the
    session's
    `PullRequestPort` (T082): unset builds the real `GhPullRequests` for this
    checkout, which writes with the invoking engineer's own `gh` auth (FR-034,
    D22), and every test injects `FakePullRequests` through it so no test can
    reach a network. `model_port_factory` is the SAME kind of seam for the
    doxBench `WorkbenchModelPort` (T024, research R6): unset means NO model
    port at all — the honest empty-catalog/editor-only posture (FR-025), not
    an error — and it is gated on the reused `session` local-human verdict
    (see `_workbench_model_port`). The current catalog-only port is consumed
    by the catalog route; the turn route still stops before provider dispatch.

    The (repository, ref) SOURCE is built here and bootstrapped once: a declared
    `data_source` (the served plane) is tried first, then a `local_index` (the
    multi-repository local plane), and the `snapshot_path` argument always
    remains available as the baked/local fallback — so a server built exactly as
    every existing caller builds one serves exactly one `(repository, main)`
    entry and behaves as it always has. `snapshot_source` is injectable for
    tests.

    `knowledge_declaration` is the INSTALL-TIME declaration of the doxBench
    staged-set knowledge service's retrieval backend
    (add-doxbench-editing-phase-b D11): unset means NO knowledge service, which
    is the declared reduced-packet posture rather than an error, and the
    production entrypoint declares `SELF_HOSTED_LOCAL_EMBEDDED` explicitly —
    the same discipline `real_notebook_adapter` carries, and for the same
    reason: an operator must be able to read what their install talks to, and a
    library default that quietly built one would defeat that."""
    from ideation_dashboard import doxbench_turns

    web_dir = Path(web_dir).resolve()
    snapshot_path = Path(snapshot_path).resolve()
    checkout_root = Path(checkout_root).resolve()
    if head is None:
        head = _head_of(checkout_root, git)

    source = snapshot_source or registry_mod.SnapshotSource(
        baked_snapshot=snapshot_path,
        repository=repository,
        ref=ref,
        checkout_root=checkout_root,
        data_source=data_source,
        index_name=index_name,
        source_roots=source_roots,
        local_index=local_index,
        project_register=project_register,
        peek_ttl_seconds=peek_ttl_seconds,
    )
    source.bootstrap()
    loopback = _is_loopback(host)
    # the LIVE branch sessions of this checkout, re-derived for this process
    # (T033a) — before any route can be asked about a session ref.
    #
    # ADMISSION IS THE CONFINEMENT (PR #49 review finding 14). This ran
    # UNCONDITIONALLY and BEFORE the bind was even classified, so an engineer who
    # served a real checkout with `--host 0.0.0.0` admitted every live session
    # into the registry of a HOSTED plane — and `/snapshot-index.json` then
    # advertised the branch names of unmerged work, the selector offered a row
    # that could only ever 403, and the page printed the session's CLI verbs.
    # FR-048 says a hosted plane has NO session, so the cheapest and most
    # complete confinement is never to admit the rows: a filter can be forgotten
    # by the next route, an empty registry cannot.
    # ONE resolution of the session key's repository half, before the bootstrap
    # that registers under it and before any request can read it (finding R2-11).
    session_repository = served_repository(source)
    if loopback:
        _bootstrap_session_entries(source, checkout_root,
                                   repository=session_repository)
    active = source.registry.active
    source_revision = active.source_revision if active else _read_source_revision(snapshot_path)

    # gate actions need a HUMAN actor: explicit arg, else the checkout's git
    # user.name; unresolvable identity keeps the capability off (fail-closed).
    resolved_actor = resolve_actor(checkout_root, actor) if loopback else None
    capabilities = compute_capabilities(
        nlm_present=_probe_nlm(adapter_factory),
        checkout_real=_checkout_real(checkout_root),
        loopback=loopback,
        actor=resolved_actor,
        refresh_binding=source.refresh_binding,
    )
    # The human console's per-serve token (FR-019's third clause, review finding
    # 2). Minted only where session verbs exist at all, and published on
    # `/capabilities` — the one route the served page reads same-origin and no
    # cross-origin page can read.
    console_token = (mint_console_token()
                     if capabilities["actions"]["session"] else None)
    if console_token:
        capabilities[CONSOLE_TOKEN_FIELD] = console_token
    # THE ONE REPOSITORY THIS SERVE CAN WRITE TO. A plane reaching several
    # repositories serves them all for READING through per-entry source roots,
    # but exactly one of them is the checkout a gate verb writes into, and
    # `refuse_foreign_repository` refuses any create that names another —
    # correctly, because "cannot verify" is not "matches".
    #
    # The browser previously had to GUESS it, and under a composed project view
    # it guessed the PROJECT id, which is not a repository at all. A serve knows
    # what it serves, so it says so; the client stops inferring. Absent
    # (no writable checkout) means no create is possible, which is the honest
    # reading of a plane that cannot name one.


    bound = type("BoundDashboardHandler", (DashboardHandler,), {
        "checkout_root": checkout_root,
        "snapshot_path": snapshot_path,
        "snapshot_route": snapshot_route,
        "source_revision": source_revision,
        "head": head,
        "quiet": quiet,
        "capabilities": capabilities,
        "loopback": loopback,
        "adapter_factory": staticmethod(adapter_factory) if adapter_factory is not None else None,
        "pull_request_factory": (staticmethod(pull_request_factory)
                                if pull_request_factory is not None else None),
        "model_port_factory": (staticmethod(model_port_factory)
                              if model_port_factory is not None else None),
        # UNSET defaults to the pinned loader; an EXPLICIT None is a caller
        # saying "no validators", which refuses both model routes. The two are
        # distinguished deliberately: an absent argument must never become an
        # implicit "serve unvalidated".
        "schema_validator_factory": (
            staticmethod(default_doxbench_validators)
            if schema_validator_factory is _UNSET_VALIDATOR_FACTORY
            else (staticmethod(schema_validator_factory)
                  if schema_validator_factory is not None else None)),
        # ONE fresh turn-idempotency ledger per served process (T050/T051).
        "turn_store": doxbench_turns.TurnStore(),
        # The INSTALL-TIME retrieval-backend declaration (task 10.6). Bound
        # once, here, and READ by the route; the backend instance itself is
        # built per request from this declaration and from nothing else, so no
        # tile's derived index is ever visible to another tile's turn.
        "knowledge_declaration": knowledge_declaration,
        # The packet assembler, defaulted to the real one (see the class
        # attribute's own note on why absence is not a posture here).
        "packet_assembler": staticmethod(
            packet_assembler if packet_assembler is not None
            else doxbench_packet.assemble_packet),
        # ONE fresh content-free usage meter per served process (task 10.8).
        "usage_meter": doxbench_telemetry.UsageMeter(),
        "actor": resolved_actor,
        # the session key's repository half, for this whole process (R2-11)
        "session_repository": session_repository,
        "console_token": console_token,
        "gate_index_validator": gate_index_validator,
        "gate_manifest_validator": gate_manifest_validator,
        "gate_xref_validator": gate_xref_validator,
        "source": source,
    })
    factory = functools.partial(bound, directory=str(web_dir))
    return http.server.ThreadingHTTPServer((host, port), factory)


def server_url(httpd: http.server.ThreadingHTTPServer, path: str = "/") -> str:
    host, port = httpd.server_address[:2]
    if host in ("0.0.0.0", "", "::"):
        host = "127.0.0.1"
    # plain-HTTP by design (S5332): a loopback-only local dev server — TLS adds
    # nothing on 127.0.0.1; the scheme is composed so no insecure-URL literal
    # exists for a copy-paste into non-loopback code.
    scheme = "http"
    return f"{scheme}://{host}:{port}{path}"


def serve(
    web_dir: Path | str,
    snapshot_path: Path | str,
    checkout_root: Path | str,
    *,
    host: str = DEFAULT_HOST,
    port: int = 0,
    quiet: bool = False,
    actor: str | None = None,
    **build_kwargs,
) -> None:
    """Build and run forever (standalone use).

    THIS is where the real notebook adapter is declared (PR #49 hardening item
    1): `serve()` is an entrypoint a human runs, so it opts into `nlm` explicitly
    rather than letting `build_server` reach for it on every caller's behalf. A
    caller that passes its own `adapter_factory` (a test, a harness) keeps it."""
    build_kwargs.setdefault("adapter_factory", real_notebook_adapter)
    # The INSTALL-TIME retrieval-backend declaration, made by the ENTRYPOINT for
    # the same reason the notebook adapter is: an operator must be able to read
    # what their install talks to, and `build_server` reaching for one on every
    # caller's behalf would put that decision out of sight. This is the
    # self-hosted case of the ratified two-case principle; a tenant install
    # declares its own here instead.
    build_kwargs.setdefault("knowledge_declaration",
                            doxbench_knowledge.SELF_HOSTED_LOCAL_EMBEDDED)
    httpd = build_server(web_dir, snapshot_path, checkout_root, host=host,
                         port=port, quiet=quiet, actor=actor, **build_kwargs)
    print(f"serving ideation dashboard at {server_url(httpd, '/index.html')}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


def _source_roots_from_args(values) -> dict:
    """`--source-root repo[@ref]=PATH`, repeatable. Explicit by design: nothing
    guesses where another repository's checkout is, and an entry with no declared
    root serves no documents at all (fail-closed, task 2.2)."""
    roots: dict[str, str] = {}
    for raw in values or []:
        key, sep, path = str(raw).partition("=")
        if not sep or not key.strip() or not path.strip():
            raise SystemExit(f"--source-root expects repo[@ref]=PATH, got {raw!r}")
        roots[key.strip()] = path.strip()
    return roots


# The shape a correct invocation has, shown in the `--checkout-root` refusal.
# Placeholders only, for the same reason `cli._GENERATE_SHAPE` carries none: a real
# path in the message would re-create the confusion it is ending.
_SERVE_SHAPE = (
    "python3 scripts/ideation_dashboard/serve.py \\\n"
    "  --snapshot <the snapshot json to serve> \\\n"
    "  --checkout-root <path to the corpus checkout>"
)


def _refuse_impossible_checkout_root(value: Path | str) -> int:
    """Refuse a `--checkout-root` that CANNOT be a checkout; report one that
    merely is not a corpus. Returns the process exit status (0 = keep going).

    `--checkout-root` is `cli.py`'s `--repo-root` under a second spelling (runbook
    §2) and it had the same T092 hole in a different shape: a path from another
    filesystem namespace was accepted in silence, and the dashboard then came up
    looking fine with every checkout-bound affordance simply absent and `/source/`
    404ing. Nothing said why.

    The two cases are NOT the same, so they are not treated the same:

      * a path that does not exist, or is not a directory, can never be a served
        checkout in any configuration -> REFUSED here, before a socket is bound.
      * an existing directory that holds no corpus IS a supported configuration:
        the served image mounts the empty `/srv/empty` sentinel precisely so
        `_checkout_real` reports false and the write-bearing affordances stay off.
        So it serves, and says loudly what it will not be able to do — which on a
        LOCAL run is the same wrong path, diagnosed."""
    from ideation_dashboard.corpus_root import corpus_root_refusal, corpus_scan_defect
    path = Path(value)
    if not path.is_dir():
        print(corpus_root_refusal(value, flag="--checkout-root",
                                  shape=_SERVE_SHAPE), file=sys.stderr)
        return 1
    defect = corpus_scan_defect(value)
    if defect is not None:
        print(f"--checkout-root {path.resolve()} is not a corpus checkout: "
              f"{defect}", file=sys.stderr)
        print("  serving anyway — an empty directory is the hosted image's "
              "sentinel — with every affordance that needs a real checkout OFF: "
              "no gate actions, no branch sessions, no /source/ pass-through",
              file=sys.stderr)
        print("  on a LOCAL run this is a wrong --checkout-root: it must name the "
              "SERVED CHECKOUT, the corpus tree itself", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ideation-dashboard-serve", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--web-dir", default=str(Path(__file__).resolve().parent / "web"),
                        help="static bundle directory (default: the packaged web/)")
    parser.add_argument("--snapshot", required=True,
                        help="snapshot JSON served as the baked/local entry — the "
                             "FIRST-BOOT and OFFLINE fallback when a data source is "
                             "declared (design D6)")
    parser.add_argument("--checkout-root", required=True, help="pinned checkout root for /source/ pass-through")
    parser.add_argument("--host", default=DEFAULT_HOST, help="bind host (default: 127.0.0.1, loopback only)")
    parser.add_argument("--port", type=int, default=0, help="bind port (default: ephemeral)")
    parser.add_argument("--actor", default=None,
                        help="human identity for loopback gate actions "
                             "(default: the checkout's git user.name; "
                             "unresolvable keeps gate actions off)")
    parser.add_argument("--repository", default=None,
                        help="repository id of the baked/local snapshot "
                             "(default: the snapshot's own `repository` field)")
    parser.add_argument("--ref", default=registry_mod.DEFAULT_REF,
                        help=f"ref of the baked/local snapshot (default: "
                             f"{registry_mod.DEFAULT_REF}; the served plane only "
                             f"ever exercises {registry_mod.DEFAULT_REF})")
    parser.add_argument("--data-source-dir", default=None,
                        help="RUNTIME DATA SOURCE: a directory holding the published "
                             "index + per-repository snapshots (a mounted volume or a "
                             "checked-out publication tree)")
    parser.add_argument("--data-source-url", default=None,
                        help="RUNTIME DATA SOURCE: base URL of the published tree, read "
                             "SERVER-SIDE (the browser never reaches it). Brett's "
                             "2026-07-26 ruling on open question 1 is the aggregation "
                             "repo's raw files, which is what --data-source-github "
                             "composes")
    parser.add_argument("--data-source-github", default=None, metavar="OWNER/REPO",
                        help="RUNTIME DATA SOURCE (the RULED hosted binding): read the "
                             "published tree from this repository's raw files, i.e. "
                             "https://raw.githubusercontent.com/OWNER/REPO/<ref>/<path>/")
    parser.add_argument("--data-source-github-ref", default=registry_mod.DEFAULT_REF,
                        help=f"ref of the raw-file source (default: {registry_mod.DEFAULT_REF})")
    parser.add_argument("--data-source-path", default=registry_mod.DEFAULT_PUBLISH_PATH,
                        help=f"path of the published tree inside the source repository "
                             f"(default: {registry_mod.DEFAULT_PUBLISH_PATH})")
    parser.add_argument("--data-source-index", default=registry_mod.DEFAULT_INDEX_NAME,
                        help=f"index filename inside the data source (default: "
                             f"{registry_mod.DEFAULT_INDEX_NAME})")
    parser.add_argument("--data-source-peek-seconds", type=float,
                        default=registry_mod.PEEK_TTL_SECONDS,
                        help="how long the serving side caches its cheap INDEX peek "
                             "before answering a freshness poll from the source again "
                             f"(default: {int(registry_mod.PEEK_TTL_SECONDS)}s; the "
                             "browser polls every ~5 minutes, so N viewers cost the "
                             "source at most one index read per TTL)")
    parser.add_argument("--data-source-token-env", default=None, metavar="ENV_NAME",
                        help="NAME of an environment variable holding a READ-ONLY bearer "
                             "token for the data source (deploy-time config: never a "
                             "credential in a repository, never reachable from the "
                             "browser)")
    parser.add_argument("--source-root", action="append", default=None,
                        metavar="REPO[@REF]=PATH",
                        help="per-entry /source confinement root, repeatable; an entry "
                             "with no declared root serves no documents (fail-closed)")
    parser.add_argument("--local-index", default=None,
                        help="a LOCAL snapshot index (multi-repository local plane); "
                             "snapshot locations resolve relative to the index file")
    parser.add_argument("--project-register", default=None,
                        help="project-register instance passed to the generator on a "
                             "local regenerate (grouping resolution)")
    args = parser.parse_args(argv)
    rc = _refuse_impossible_checkout_root(args.checkout_root)
    if rc:
        return rc
    data_source = registry_mod.data_source_from_options(
        directory=args.data_source_dir,
        url=args.data_source_url or (registry_mod.github_raw_base_url(
            args.data_source_github, ref=args.data_source_github_ref,
            path=args.data_source_path) if args.data_source_github else None),
        token_env=args.data_source_token_env,
    )
    serve(args.web_dir, args.snapshot, args.checkout_root, host=args.host,
          port=args.port, actor=args.actor,
          repository=args.repository, ref=args.ref,
          data_source=data_source, index_name=args.data_source_index,
          source_roots=_source_roots_from_args(args.source_root),
          local_index=args.local_index,
          project_register=args.project_register,
          peek_ttl_seconds=args.data_source_peek_seconds)
    return 0


if __name__ == "__main__":
    sys.exit(main())
