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
from ideation_dashboard import snapshot_registry as registry_mod  # noqa: E402

DEFAULT_HOST = "127.0.0.1"
SNAPSHOT_ROUTE = "/snapshot.json"
SNAPSHOT_INDEX_ROUTE = "/snapshot-index.json"
SOURCE_PREFIX = "/source/"
CAPABILITIES_ROUTE = "/capabilities"
ACTIONS_NOTEBOOK_ROUTE = "/actions/notebook"
ACTIONS_REFRESH_ROUTE = "/actions/refresh"
ACTIONS_EDIT_ROUTE = "/actions/edit"
ACTIONS_GATE_PREFIX = "/actions/gate/"
# T050/T051 (change 010-doxbench-editor-chat): the two doxBench HTTP routes.
# See the section banner above `_handle_workbench_model_catalog` for the
# judgement calls their handlers make.
WORKBENCH_MODEL_CATALOG_ROUTE = "/workbench/model-catalog"
ACTIONS_WORKBENCH_CHAT_TURN_ROUTE = "/actions/workbench/chat-turn"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})
JSON_CTYPE = "application/json; charset=utf-8"
JSON_OBJECT_BODY_REQUIRED = "a JSON object body is required"
_MAX_BODY_BYTES = 65_536  # a tile-action body is tiny; cap it to refuse a flood
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
# for every route that already exists — R7 explicitly rejects widening it,
# because that would weaken every unrelated action and lose measured limit
# errors. The doxBench chat-turn route declares this bound for ITSELF, sized
# to plan.md's Constraints total (1,048,576 UTF-8 bytes).
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
}


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
    if code == DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED and limit is not None:
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
                               limit: dict | None = None) -> dict:
    """The RELEASED `workbench-chat-turn-failure` envelope for `code` — a PURE
    module-level function, testable with no handler and no server.

    Keys are the released allowlist: `schema_version`, `kind`,
    `client_turn_id`, `error`, `message`, and — ONLY for
    `request_limit_exceeded` — the `limit` block, REBUILT from exactly three
    named fields exactly as `doxbench_error_body` rebuilds it, so nothing
    request-derived can splice a key into a response. The message is the same
    fixed module-level constant the pre-release shape used; only the envelope
    changed."""
    _, message = DOXBENCH_ERROR_CATALOG[code]
    body: dict = {
        "schema_version": DOXBENCH_WIRE_SCHEMA_VERSION,
        "kind": DOXBENCH_CHAT_TURN_FAILURE_KIND,
        "client_turn_id": str(client_turn_id),
        "error": code,
        "message": message,
    }
    if code == DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED and limit is not None:
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

    def _doxbench_validators(self):
        """The RELEASED per-kind schema validators for this request, or None.

        Resolved through the INJECTED `schema_validator_factory` seam, bound
        exactly like `model_port_factory`, so no test and no non-console plane
        depends on a pinned openxFactory checkout being present. Resolution is
        PER REQUEST, not cached: the pinned loader re-verifies digests, the
        checkout's own manifest, and `stack.yaml`'s declared ref every time, so
        a checkout that drifts mid-run stops being trusted at the next request
        rather than at the next restart.

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

    def _refuse_turn(self, validators, code, turn_id, *, limit=None) -> None:
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
        because idempotency is keyed on what the caller actually sent."""
        status = doxbench_error_status(code)
        if turn_id is not None:
            body = doxbench_turn_failure_body(code, turn_id, limit=limit)
            if self._doxbench_wire_conforms(
                    validators, DOXBENCH_CHAT_TURN_FAILURE_KIND, body):
                self._send_json(status, body)
                return
        self._send_json(status, doxbench_error_body(code, limit=limit))

    @staticmethod
    def _parse_workbench_chat_turn_body(payload):
        """Structural, known-field extraction for `POST /actions/workbench/
        chat-turn` (T051). Returns a tuple of coerced fields, or `None` on
        ANY structural violation: a missing/wrong-typed field, a blank-or-
        whitespace-only `message`, or a buffer list that is not exactly one
        `outline` plus one `document`. Runs AFTER the released-schema gate, so
        unknown extra keys are already refused by the CLOSED released envelope
        rather than ignored here -- this parser no longer needs to decide that
        question and deliberately still does not: it coerces the known fields
        the chain needs. NEVER re-implements
        `doxbench_turns.TurnBuffer`/`TranscriptTurn`'s own validation --
        this only checks JSON *shape*, then hands the coerced values to
        those constructors."""
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

        active_document_path = payload.get("active_document_path")
        if active_document_path is not None and not isinstance(active_document_path, str):
            return None

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
        if not isinstance(buffers_raw, list) or len(buffers_raw) != 2:
            return None
        turn_buffers = []
        kinds_seen = []
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
            kinds_seen.append(kind)
            turn_buffers.append(doxbench_turns.TurnBuffer(
                kind=kind, repository=repository, path=path, base_ref=base_ref,
                base_revision=base_revision, base_hash=base_hash,
                content_hash=content_hash, content=content, dirty=dirty))
        if sorted(kinds_seen) != ["document", "outline"]:
            return None

        return (client_turn_id, scope_fields, active_document_path, working_subject,
                message, model_id, last_assistant_turn_id, transcript_turns, turn_buffers)

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
        if not self._doxbench_wire_conforms(
                validators, DOXBENCH_CHAT_TURN_KIND, payload):
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST, turn_id)
            return

        fields = self._parse_workbench_chat_turn_body(payload)
        if fields is None:
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST, turn_id)
            return
        (client_turn_id, scope_fields, active_document_path, working_subject, message,
         model_id, _last_assistant_turn_id, transcript_turns, turn_buffers) = fields

        from ideation_dashboard import doxbench_hash
        from ideation_dashboard import doxbench_model
        from ideation_dashboard import doxbench_scope
        from ideation_dashboard import doxbench_turns

        key = doxbench_scope.ScopeKey(repository=scope_fields["repository"],
                                      ref=scope_fields["ref"],
                                      tile_kind=scope_fields["tile_kind"],
                                      tile_id=scope_fields["tile_id"])
        outline_buf = next((b for b in turn_buffers if b.kind == "outline"), None)
        document_buf = next((b for b in turn_buffers if b.kind == "document"), None)

        # ---- step 5: scope, all from SERVER truth ----
        projection = None
        scope_refused = False
        try:
            entry = self.source.registry.resolve(key.repository, key.ref)
            if entry is None or entry.source_root is None:
                scope_refused = True
            else:
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
                    doxbench_turns.revalidate_scope(
                        projection=projection, request_scope=key,
                        active_document_path=active_document_path,
                        outline_path=outline_buf.path if outline_buf else None,
                        document_path=document_buf.path if document_buf else None,
                    )
        except (doxbench_turns.TurnScopeError, doxbench_scope.ScopeConfinementError,
                ValueError, OSError):
            scope_refused = True

        if scope_refused:
            self._refuse_turn(validators, DOXBENCH_ERR_TURN_SCOPE_REFUSED,
                              turn_id)
            return

        # ---- step 6: exact identity ----
        try:
            outline, document = doxbench_turns.require_outline_and_document(turn_buffers)
        except doxbench_turns.TurnBufferKindError:
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id)
            return

        try:
            doxbench_turns.verify_buffer_identity(outline)
            doxbench_turns.verify_buffer_identity(document)
        except doxbench_turns.TurnIdentityMismatchError:
            self._refuse_turn(validators, DOXBENCH_ERR_CONTENT_IDENTITY_MISMATCH,
                              turn_id)
            return
        except doxbench_turns.TurnLimitError as exc:
            self._refuse_turn(validators, DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
                              turn_id, limit=exc.as_public_dict())
            return

        # ---- step 7: model ----
        port = self._workbench_model_port()
        if port is None:
            self._refuse_turn(validators,
                              DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE,
                              turn_id)
            return
        try:
            catalog = port.catalog()
        except Exception:  # noqa: BLE001 - never let a provider-shaped exception reach the wire
            self._refuse_turn(validators, DOXBENCH_ERR_CATALOG_UNAVAILABLE,
                              turn_id)
            return
        if not isinstance(catalog, doxbench_model.ModelCatalog):
            self._refuse_turn(validators, DOXBENCH_ERR_CATALOG_UNAVAILABLE,
                              turn_id)
            return
        model_entry = catalog.selectable_entry_for(model_id)
        if model_entry is None:
            self._refuse_turn(validators, DOXBENCH_ERR_MODEL_UNAVAILABLE,
                              turn_id)
            return

        effective_input_limit = doxbench_model.effective_limit_bytes(
            server_maximum=doxbench_model.SERVER_MAX_INPUT_LIMIT_BYTES,
            entry_limit=model_entry.input_limit_bytes)
        effective_output_limit = doxbench_model.effective_limit_bytes(
            server_maximum=doxbench_model.SERVER_MAX_OUTPUT_LIMIT_BYTES,
            entry_limit=model_entry.output_limit_bytes)

        outline_bytes = doxbench_hash.utf8_size(outline.content)
        document_bytes = doxbench_hash.utf8_size(document.content)
        message_bytes = doxbench_hash.utf8_size(message)
        working_subject_bytes = doxbench_hash.utf8_size(working_subject)
        transcript_byte_total = doxbench_turns.transcript_bytes(transcript_turns)

        try:
            doxbench_turns.validate_working_subject(working_subject)
            doxbench_turns.validate_message(message)
            doxbench_turns.validate_transcript(transcript_turns)
            doxbench_turns.validate_request_body_bytes(
                outline_bytes=outline_bytes, document_bytes=document_bytes,
                message_bytes=message_bytes, working_subject_bytes=working_subject_bytes,
                transcript_bytes=transcript_byte_total)
        except doxbench_turns.TurnLimitError as exc:
            self._refuse_turn(validators, DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
                              turn_id, limit=exc.as_public_dict())
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
                       "maximum": effective_input_limit})
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
                for buf in turn_buffers
            ],
        }
        digest = doxbench_hash.sha256_hex(
            json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False))

        record = self.turn_store.snapshot(key, client_turn_id)
        if record is not None:
            if record.state == doxbench_turns.TURN_STATE_IN_FLIGHT:
                code = (DOXBENCH_ERR_TURN_IN_FLIGHT if record.request_digest == digest
                       else DOXBENCH_ERR_TURN_ID_CONFLICT)
                self._refuse_turn(validators, code, turn_id)
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
                              turn_id)
            return

        try:
            lease = self.turn_store.reserve(key, client_turn_id, digest)
        except doxbench_turns.TurnInFlightError:
            self._refuse_turn(validators, DOXBENCH_ERR_TURN_IN_FLIGHT,
                              turn_id)
            return
        except doxbench_turns.TurnConflictError:
            self._refuse_turn(validators, DOXBENCH_ERR_TURN_ID_CONFLICT,
                              turn_id)
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
        prompt_envelope = None
        try:
            prompt_envelope = doxbench_turns.build_prompt_envelope(
                projection=projection, request_scope=key,
                active_document_path=active_document_path,
                model_id=model_id, model_data_handling=model_entry.data_handling,
                model_input_limit_bytes=effective_input_limit,
                model_output_limit_bytes=effective_output_limit,
                working_subject=working_subject, transcript=tuple(transcript_turns),
                buffers=(outline, document), message=message)
        except doxbench_turns.TurnScopeError:
            outcome_code = DOXBENCH_ERR_TURN_SCOPE_REFUSED
        except doxbench_turns.TurnIdentityMismatchError:
            outcome_code = DOXBENCH_ERR_CONTENT_IDENTITY_MISMATCH
        except doxbench_turns.TurnBufferKindError:
            outcome_code = DOXBENCH_ERR_INVALID_TURN_REQUEST

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
            permitted_targets = (
                doxbench_turns.PROPOSAL_TARGETS if active_document_path is not None
                else ("outline",))

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
                port, prompt_envelope, model_entry, _typed_response_validator)
            if isinstance(outcome, doxbench_model.TurnDispatchSuccess):
                # `assistant_turn_id` derivation is this slice's judgement
                # call: the released schema bounds it (1..128) without naming
                # a scheme, so it is derived from the turn's own canonical
                # request digest -- deterministic, request-unforgeable, and
                # carrying no provider or content material.
                success_body = doxbench_turn_success_body(
                    client_turn_id=client_turn_id,
                    assistant_turn_id="assistant-" + digest[:56],
                    model_id=model_id,
                    observed_hashes={
                        "outline": prompt_envelope.observed_hashes.outline.hex,
                        "document": prompt_envelope.observed_hashes.document.hex,
                    },
                    assistant_prose=outcome.assistant_prose,
                    proposals=outcome.proposals)
                if self._doxbench_wire_conforms(
                        validators, DOXBENCH_CHAT_TURN_SUCCESS_KIND, success_body):
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
                                          turn_id)
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
        body = (doxbench_turn_failure_body(outcome_code, turn_id)
                if turn_id is not None else doxbench_error_body(outcome_code))
        if not self._doxbench_wire_conforms(
                validators, DOXBENCH_CHAT_TURN_FAILURE_KIND, body):
            body = doxbench_error_body(outcome_code)
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
        if path == CAPABILITIES_ROUTE:
            # The loopback console token is process-launch authority. Never
            # disclose it to a DNS-rebinding Host, even though the connection
            # itself arrived on the loopback socket.
            if self.console_token and not self._trusted_console_host():
                self._send_json(403, {"ok": False, "error": "invalid_host",
                                      "message": "the request Host is not this "
                                                 "loopback console"})
                return True
            self._serve_bytes(json.dumps(self.capabilities).encode("utf-8"),
                              JSON_CTYPE, head_only)
            return True
        if path == WORKBENCH_MODEL_CATALOG_ROUTE:
            self._handle_workbench_model_catalog(head_only)
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
        if length <= 0 or length > _MAX_BODY_BYTES:
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
            "maximum": max_bytes})` — a MEASURED verdict (FR-017), unlike this
            class's OTHER reader, whose bare `None` is exactly what research
            R7 says a global cap loses;
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
            # Drain at most max_bytes + 1 bytes — enough to know the body is
            # over the bound, never enough to buffer an unbounded flood no
            # matter how large the declared length lies.
            try:
                self.rfile.read(max_bytes + 1)
            except OSError:
                pass
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
    tests."""
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
