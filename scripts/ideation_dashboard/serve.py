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
import secrets
import sys
import urllib.parse
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# The ROUTE EXTENSION POINT (`split-opendox-two-layer-product` § 2.4, design
# § D2). A neutral module at the top of `scripts/`, belonging to neither
# package and importing neither, for the same three reasons `output_boundary`
# and `corpus_adapter` sit there: both sides of the carve consume it, it travels
# with the carve, and it therefore imports nothing from here. Spelled as a bare
# top-level import for the same reason `boundary.py` spells `output_boundary`
# that way.
import route_extension  # noqa: E402

from ideation_dashboard import action_errors  # noqa: E402
from ideation_dashboard import doxbench_abstract_store  # noqa: E402
# The INSTALL-TIME model-provider declaration the two entrypoints make.
# Hoisted to module scope by add-doxbench-distilled-abstract §5: the graph is
# acyclic (`doxbench_install` -> `doxbench_bridge` -> `doxbench_mcp`/
# `doxbench_threads`/`doxbench_model`, none of which imports this module), and
# importing the declaration STARTS nothing -- the bridge is constructed lazily
# on the first resolution and its child only at the first turn that needs one.
# It used to be a function-scope import inside `serve()`, justified as "only an
# ENTRYPOINT has any business reading an install declaration"; that is a rule
# about who CALLS `model_port_factory`, which is still exactly one place, and
# a deferred import was never what enforced it.
from ideation_dashboard import doxbench_install  # noqa: E402
from ideation_dashboard import doxbench_knowledge  # noqa: E402
from ideation_dashboard import doxbench_packet  # noqa: E402
from ideation_dashboard import doxbench_telemetry  # noqa: E402
from ideation_dashboard import snapshot_registry as registry_mod  # noqa: E402
# THE BY-FUNCTION SPLIT (`split-opendox-two-layer-product` § 2.4, PRs 2 and 3
# of 4). The openDox column's routes live in `serve_workbench.py` (the doxBench
# workbench surface) and `serve_project.py` (projects, the notebook tile action,
# select-to-edit); openXdox's live in `serve_gate.py` (the gate console's door)
# and `serve_projection.py` (the snapshot, index and `/source` routes); this
# repository's OWN lane routes live in `serve_openxfactory_lanes.py` (RULING
# DQ-1). The wire vocabulary, the body bounds and the hosted-plane confinement
# this core AND every column read live in `serve_wire.py`. No column imports
# this module — the graph is a DAG, which is the whole reason the vocabulary
# moved out rather than staying here — and the columns are composed back onto
# `DashboardHandler` as MIXINS below.
#
# TWO REGISTRATION MODES, and the difference is the point of PR 3. PR 2's
# columns are still FIXED CORE ARMS of `_route`/`do_POST`, exactly as they were.
# PR 3's three are CONTRIBUTED: their arms have left the fixed tables and they
# arrive as `RouteBinding`s through the extension point, assembled in
# `profile_openxfactory.py` and dispatched BY NAME against the live handler —
# so they meet `self.loopback`, `self.capabilities` and the console test by
# construction rather than by their author's memory. One route deliberately
# straddles the two: `/snapshot.json`'s HANDLER moved to `serve_projection.py`
# with its neighbours while its ARM stayed core, because that arm tests
# `path == self.snapshot_route` — a per-server keyword `build_server` accepts,
# which a frozen `RouteBinding.pattern` cannot carry.
#
# EVERY MOVED MODULE-LEVEL NAME IS IMPORTED BACK BY NAME, so this module's
# namespace is what it always was: `serve.doxbench_error_body`,
# `serve.DOXBENCH_ERROR_CATALOG`, `serve.JSON_CTYPE`, `serve._launch_editor`,
# `serve.resolve_source_path`, `serve.hosted_index` and the rest all still
# resolve for every reader that already had them.
# That is what the `F401`s below declare: names imported to be RE-EXPORTED,
# not names this module happens not to use yet.
from ideation_dashboard import serve_gate  # noqa: E402
from ideation_dashboard import serve_openxfactory_lanes  # noqa: E402
from ideation_dashboard import serve_project  # noqa: E402
from ideation_dashboard import serve_projection  # noqa: E402
from ideation_dashboard import serve_workbench  # noqa: E402
from ideation_dashboard.serve_gate import (  # noqa: E402,F401
    ACTIONS_GATE_PREFIX,
)
from ideation_dashboard.serve_openxfactory_lanes import (  # noqa: E402,F401
    ACTIONS_APPLY_REGISTER_EDITS_ROUTE,
    ACTIONS_DTN_SEED_ROUTE,
    ACTIONS_REFRESH_ROUTE,
    ACTIONS_STAGING_SEED_ROUTE,
    COMMITTED_INTENTS_ROUTE,
)
from ideation_dashboard.serve_project import (  # noqa: E402,F401
    _edit_request_fields,
    _launch_editor,
    _listed_source_paths,
    _resolved_listed_edit_entry,
)
from ideation_dashboard.serve_projection import (  # noqa: E402,F401
    BARE_SOURCE_ROUTE,
    SNAPSHOT_INDEX_ROUTE,
    SOURCE_PREFIX,
    resolve_source_path,
)
from ideation_dashboard.serve_wire import (  # noqa: E402,F401
    AGENT_INVOCATION_REFUSAL,
    CONTEXT_REDUCED_REASON_MAX_LENGTH,
    HOSTED_SESSION_REFUSAL,
    DOXBENCH_ABSTRACT_CONVERSATION_KIND,
    DOXBENCH_ABSTRACT_REFUSAL_STATUS,
    DOXBENCH_ABSTRACT_REFUSED_PROSE_BYTES,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_BYTES,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_DISTILLABLE,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_ELIGIBLE,
    DOXBENCH_CHAT_TURN_V2_FAILURE_KIND,
    DOXBENCH_CHAT_TURN_V2_KIND,
    DOXBENCH_CHAT_TURN_V2_SUCCESS_KIND,
    DOXBENCH_ERROR_CATALOG,
    DOXBENCH_ERR_ABSTRACT_UNAVAILABLE,
    DOXBENCH_ERR_APPROVAL_REFUSED,
    DOXBENCH_ERR_CATALOG_UNAVAILABLE,
    DOXBENCH_ERR_CONSOLE_REQUIRED,
    DOXBENCH_ERR_CONTENT_IDENTITY_MISMATCH,
    DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED,
    DOXBENCH_ERR_CONTEXT_PACKET_INVALID,
    DOXBENCH_ERR_INTAKE_REFUSED,
    DOXBENCH_ERR_INVALID_ABSTRACT_REQUEST,
    DOXBENCH_ERR_INVALID_INTAKE_REQUEST,
    DOXBENCH_ERR_INVALID_TURN_REQUEST,
    DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE,
    DOXBENCH_ERR_MODEL_FAILED,
    DOXBENCH_ERR_MODEL_TIMEOUT,
    DOXBENCH_ERR_MODEL_UNAVAILABLE,
    DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
    DOXBENCH_ERR_RESPONSE_INVALID,
    DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE,
    DOXBENCH_ERR_TURN_ID_CONFLICT,
    DOXBENCH_ERR_TURN_IN_FLIGHT,
    DOXBENCH_ERR_TURN_SCOPE_REFUSED,
    DOXBENCH_ERR_UNRECOGNIZED_TURN_KIND,
    DOXBENCH_LIMIT_BEARING_CODES,
    DOXBENCH_MAX_REQUEST_BYTES,
    DOXBENCH_MODEL_CATALOG_KIND,
    DOXBENCH_WIRE_SCHEMA_VERSION,
    JSON_CTYPE,
    JSON_OBJECT_BODY_REQUIRED,
    NO_LIVE_SESSION_CAUSE,
    NO_RESOLVED_ACTOR_CAUSE,
    _ABSTRACT_REASON_NOT_DISTILLABLE,
    _ABSTRACT_REASON_NOT_ELIGIBLE,
    _ABSTRACT_REASON_NO_DECLARED_BASE,
    _ABSTRACT_REASON_SUBJECT_BYTES,
    _CredentialStream,
    _DOXBENCH_MSG_ABSTRACT_UNAVAILABLE,
    _DOXBENCH_MSG_APPROVAL_REFUSED,
    _DOXBENCH_MSG_CATALOG_UNAVAILABLE,
    _DOXBENCH_MSG_CONSOLE_REQUIRED,
    _DOXBENCH_MSG_CONTENT_IDENTITY_MISMATCH,
    _DOXBENCH_MSG_CONTEXT_PACKET_BOUND_EXCEEDED,
    _DOXBENCH_MSG_CONTEXT_PACKET_INVALID,
    _DOXBENCH_MSG_INTAKE_REFUSED,
    _DOXBENCH_MSG_INVALID_ABSTRACT_REQUEST,
    _DOXBENCH_MSG_INVALID_INTAKE_REQUEST,
    _DOXBENCH_MSG_INVALID_TURN_REQUEST,
    _DOXBENCH_MSG_MODEL_CAPABILITY_UNAVAILABLE,
    _DOXBENCH_MSG_MODEL_FAILED,
    _DOXBENCH_MSG_MODEL_TIMEOUT,
    _DOXBENCH_MSG_MODEL_UNAVAILABLE,
    _DOXBENCH_MSG_REQUEST_LIMIT_EXCEEDED,
    _DOXBENCH_MSG_RESPONSE_INVALID,
    _DOXBENCH_MSG_THREAD_CAPABILITY_UNAVAILABLE,
    _DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT,
    _DOXBENCH_MSG_TURN_ID_CONFLICT,
    _DOXBENCH_MSG_TURN_IN_FLIGHT,
    _DOXBENCH_MSG_TURN_SCOPE_REFUSED,
    _DOXBENCH_MSG_UNRECOGNIZED_TURN_KIND,
    _MAX_BODY_BYTES,
    _MAX_REFUSED_DRAIN_BYTES,
    _UNSET_VALIDATOR_FACTORY,
    _abstract_reason_prose_bytes,
    _drain_refused_body,
    _no_dereference,
    _sidecar_text,
    _thread_absence_body,
    default_doxbench_validators,
    doxbench_abstract_conversation_key,
    doxbench_abstract_refusal_body,
    doxbench_abstract_refusal_status,
    doxbench_abstract_success_body,
    doxbench_context_packet,
    doxbench_declared_fields,
    doxbench_error_body,
    doxbench_error_status,
    doxbench_selected_model,
    doxbench_turn_failure_body,
    doxbench_turn_v2_success_body,
    fresh_ledger_events,
    hosted_index,
    hosted_ref_refused,
    mint_ledger_snapshot,
    provider_retry_fact,
)

DEFAULT_HOST = "127.0.0.1"
SNAPSHOT_ROUTE = "/snapshot.json"
# add-project-scoped-selection: the register projection the selector's project
# picker reads. The snapshot INDEX is a locator and deliberately carries no
# grouping, so the register itself — aggregation-owned, discovered upward from
# the checkout — is served read-only here. Absent register (or the static
# image, which never serves this route) -> 404 -> the picker hides and the
# selector degrades to today's ungrouped roster.
PROJECT_REGISTER_ROUTE = "/project-register.json"
CAPABILITIES_ROUTE = "/capabilities"
ACTIONS_NOTEBOOK_ROUTE = "/actions/notebook"
ACTIONS_EDIT_ROUTE = "/actions/edit"
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
# add-doxbench-distilled-abstract §5 (design D1): the model-derived per-document
# distilled abstract's OWN route, deliberately NOT a scoped chat turn. The
# released turn envelope carries a bound buffer key, per-buffer observed hashes
# and a buffer-keyed proposal target that an abstract request has none of, and
# `dispatch_turn` would still demand a `{assistant_prose, proposals}` answer from
# a request that is not a conversation. The provider-boundary requirement says it
# in as many words -- a consumer whose request is not a conversation SHALL carry
# its own request shape and its own declared purpose -- so this is a second
# CONSUMER of the one model seam, never a second meaning for the chat route.
ACTIONS_WORKBENCH_DOCUMENT_ABSTRACT_ROUTE = "/actions/workbench/document-abstract"
# add-doxchat-model-intake §2/§3: the MODEL INTAKE surface and its two acts.
# Three routes and not one, because they answer three different questions and
# carry three different things.
#
#   * the SURFACE (a GET) discloses whether intake is offered at all, which
#     authentication kinds the declared broker can take, and which declarations
#     are still waiting on a human. It is what makes the selector's intake
#     affordance honest: the affordance is rendered only when this route says the
#     flow behind it can be opened AND completed;
#   * the INTAKE act (a POST) carries a CREDENTIAL, and so carries it in a way
#     nothing else on this server does — the facts ride the query string, where a
#     fact belongs, and the body is the credential and NOTHING ELSE, streamed
#     straight into the broker's standard input. See `_handle_workbench_model_intake`;
#   * the APPROVAL act (a POST) carries no credential at all: it names a
#     declaration and writes the gate-action record that makes it available.
#
# Console-internal local shapes, deliberately NOT released contract envelopes,
# exactly as `WORKBENCH_THREAD_ROUTE` is: no openxFactory schema declares an
# intake shape, and inventing a `schema_version` for one here would claim a
# release that was never cut. The governed artifacts are the ones that ARE
# released — the gate-action record the approval writes, and the settings
# documents the flow leaves behind.
WORKBENCH_MODEL_INTAKE_ROUTE = "/workbench/model-intake"
ACTIONS_WORKBENCH_MODEL_INTAKE_ROUTE = "/actions/workbench/model-intake"
ACTIONS_WORKBENCH_MODEL_APPROVAL_ROUTE = "/actions/workbench/model-approval"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})

_DEFAULT_CAPABILITIES = {"actions": {"notebook": False, "gate": False, "refresh": False,
                                    "session": False, "edit": False,
                                    "intent": False},
                         "actor": None, "refresh": {"binding": None, "loopback_only": True}}


# --------------------------- capability discovery (pure) ---------------------------

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
    a complete session.

    INTENT (add-ideation-intent-plane task 4.4, design D5) is the gate seam's
    OTHER binding, and it is the photographic negative of the gate leg: the
    SERVED plane emits intents, the loopback plane executes. D5 fixes the pair
    — "the LOCAL dashboard gets executing gate routes + the dispose tray FIRST
    ... and the identical tray then targets the intent API when hosted" — so
    exactly one of `gate` and `intent` is ever true, and a local session's
    `gate = local_human` verdict is unchanged by this key's existence.

    Three things it deliberately does NOT depend on, each for its own reason:

      * `hosted_actor`. That field is stamped PER REQUEST from the gateway
        header and is DISPLAY-ONLY: `add-dashboard-account-menu` Requirement 2
        says the header flips no capability verdict, and the `/capabilities`
        handler says the same in its own comment. Keying intent emission on it
        would make a display fact into an authorization input and would make
        the `actions` map differ between two requests to one server. The inbox
        is the identity authority: an unauthenticated POST gets its own 401
        there, which is a refusal the tray RENDERS rather than a capability the
        dashboard withholds.
      * `actor`. That is the LOCAL identity resolved from the checkout; a
        hosted plane has none by construction and must still emit.
      * `checkout_real`. Intent emission is a POST to another pod; it needs no
        corpus. (The committed-intent FEED does read the checkout, but a feed
        with nothing in it is an empty feed, not an absent capability.)

    So the predicate is the plane itself, and nothing else."""
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
            # THE HOSTED WRITE-REQUEST SEAM, and the only capability here that
            # is true OFF loopback. It grants no write: an intent is a REQUEST
            # the apply lane revalidates and may refuse (kernel schema: "an
            # intent is NEVER a write"), which is why it does not join the
            # account menu's WRITE_ACTIONS list either.
            "intent": not loopback,
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
    """The local action center's human identity. None (no identity) keeps gate
    actions unavailable — fail-closed, never a guessed actor.

    THE `--actor` TRUST GAP, on this surface. An explicit `--actor` used to WIN
    OUTRIGHT: whatever string the flag carried became the identity every
    gate-action record this serve wrote would name, checked against nothing. The
    override is now a CLAIM that must match the authenticated principal
    (`actor_identity`) — the gateway-verified user, a launcher-supplied
    principal, an explicit allowlist, or this checkout's own git identity, which
    is also the no-override default the function has always used. An override
    that cannot be authenticated resolves to None, which is this surface's
    fail-closed spelling: the plane comes up with gate actions OFF rather than
    with a fabricated identity attached to them."""
    from ideation_dashboard import actor_identity

    if override and str(override).strip():
        return actor_identity.authenticated_actor_or_none(
            override, checkout_root=checkout_root)
    return actor_identity.authenticated_actor_or_none(
        None, checkout_root=checkout_root)


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


def _head_of(checkout_root: Path, git=None) -> str | None:
    """Current git HEAD of the checkout, or None (degrades — never blocks
    serving)."""
    try:
        from doc_health.corpus import RealGit
        return (git or RealGit()).head_sha(Path(checkout_root))
    except Exception:
        return None


# --------------------------- request handler ---------------------------

class DashboardHandler(serve_workbench.WorkbenchRoutes,
                       serve_project.ProjectRoutes,
                       serve_gate.GateRoutes,
                       serve_projection.ProjectionRoutes,
                       serve_openxfactory_lanes.LaneRoutes,
                       http.server.SimpleHTTPRequestHandler):
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
    # The per-process DISTILLED-ABSTRACT cache (add-doxbench-distilled-abstract
    # §5.3, clarification N1). A SEPARATE instance with SEPARATE bounds, never
    # the chat ledger above: a scope holding more documents than the bound is
    # the ordinary case for abstracts, so a shared store would evict chat
    # idempotency records under ordinary abstract churn and a chat retry that
    # should replay would re-dispatch. None only in hand-constructed handlers;
    # `build_server` always binds a fresh one.
    abstract_store = None
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
    # The CONTRIBUTED routes this server was assembled with
    # (`split-opendox-two-layer-product` § 2.4), already flattened into one
    # consult order by `route_extension.collect_bindings`: the in-tree profile
    # (`profile_openxfactory.ROUTE_EXTENSIONS` — the gate console, the
    # projection routes, this repository's lane routes) plus whatever the
    # caller added. The fixed core arms below are consulted first and the
    # fallback after, so the ORDER a route is reached in is unchanged by where
    # it is registered. Bound by `build_server`; `()` in hand-constructed
    # handlers, which therefore serve the core arms alone — the same posture a
    # hand-constructed handler has always had for every seam `build_server`
    # binds (no adapter, no validators, no turn store).
    route_bindings: tuple = ()

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

    def _route(self, head_only: bool) -> bool:
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path == self.snapshot_route:
            self._serve_snapshot(head_only)
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
        if path == WORKBENCH_MODEL_INTAKE_ROUTE:
            self._handle_workbench_model_intake_surface(head_only)
            return True
        if path == WORKBENCH_THREAD_ROUTE:
            self._handle_workbench_thread(head_only)
            return True
        # ---- the CONTRIBUTED read routes (§ 2.4) ----
        # AFTER every fixed core arm and BEFORE the static fallback, which is
        # the placement that makes two things true at once: a contributed route
        # can never shadow a core one (the core arms have already returned), and
        # a path no binding claims still falls through to exactly the static
        # behaviour it falls through to today. Dispatch is BY NAME against
        # `self`, so a contributed route meets the same gating primitives — the
        # loopback verdict, the capability dict, the console-host check — that
        # every arm above meets.
        matched = route_extension.match(
            self.route_bindings, "HEAD" if head_only else "GET", path)
        if matched is not None:
            binding, remainder = matched
            handler = getattr(self, binding.handler)
            if binding.is_prefix:
                handler(remainder, head_only)
            else:
                handler(head_only)
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
        if path == ACTIONS_EDIT_ROUTE:
            self._handle_edit_action()
            return
        if path == ACTIONS_WORKBENCH_CHAT_TURN_ROUTE:
            self._handle_workbench_chat_turn()
            return
        if path == ACTIONS_WORKBENCH_DOCUMENT_ABSTRACT_ROUTE:
            self._handle_workbench_document_abstract()
            return
        if path == ACTIONS_WORKBENCH_MODEL_INTAKE_ROUTE:
            self._handle_workbench_model_intake()
            return
        if path == ACTIONS_WORKBENCH_MODEL_APPROVAL_ROUTE:
            self._handle_workbench_model_approval()
            return
        # ---- the CONTRIBUTED write routes (§ 2.4) ----
        # The read path's clause, with the write path's two call shapes and its
        # own fallback: an action no binding claims still answers
        # ERR_UNKNOWN_ACTION exactly as it does today. Same by-name dispatch
        # against `self`, so a contributed write route reaches the loopback and
        # capability gates by construction rather than by its author's memory.
        matched = route_extension.match(self.route_bindings, "POST", path)
        if matched is not None:
            binding, remainder = matched
            handler = getattr(self, binding.handler)
            if binding.is_prefix:
                handler(remainder)
            else:
                handler()
            return
        self._send_error_code(action_errors.ERR_UNKNOWN_ACTION)

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
    route_extensions: tuple = (),
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
    library default that quietly built one would defeat that.

    `route_extensions` is the ROUTE EXTENSION POINT
    (`split-opendox-two-layer-product` § 2.4, design § D2): the tuple of
    `route_extension.RouteExtension`s this server is ASSEMBLED with, each
    contributing routes the fixed core dispatch does not carry. `routes()` is
    called ONCE, here, and the flattened bindings are bound to the handler
    class; the extensions themselves are deliberately NOT retained, because an
    extension reachable from a request is an invitation to re-ask it per
    request, and a dispatch table that can change under traffic is not a
    dispatch table.

    THE IN-TREE PROFILE (`profile_openxfactory.ROUTE_EXTENSIONS`) is registered
    HERE, ahead of the caller's tuple, and is NOT passed in by `main()` — the
    same shape `build_parser` uses for `SUBCOMMAND_EXTENSIONS` (PR 4 of § 2.4).
    `build_server(...)` names the whole of THIS assembly's server, which is what
    all 31 in-tree test `build_server(...)` call sites across 27 test files
    already read it as, so the routes PR 3 moved out of the fixed tables are
    served by a caller who passes nothing — and by a
    caller who passes `route_extensions=()` explicitly, which is the same
    request spelled twice. `route_extensions` stays the seam for whatever a
    caller adds ON TOP; the default `()` therefore still means "add nothing".
    A SENTINEL (`None` -> profile, `()` -> none) was considered and refused: the
    only in-tree caller that passes the keyword at all passes `()` and would
    have silently lost `/snapshot-index.json`, `/source/` and every gate verb
    from the servers in the file that tests this very seam. This line is also
    the one the § 3 carve deletes rather than moves."""
    from ideation_dashboard import doxbench_turns
    # Imported HERE rather than at module scope, deliberately: the profile is a
    # WIRING input consulted once per build, and importing it at module scope
    # would pull every contributed column — and, once PR 4 lands, the CLI
    # column beside them — into the import graph of a module the container runs
    # as a plain script. `cli.py` names the same profile at module scope
    # because a parser is built from it at import time; a server is not.
    from ideation_dashboard import profile_openxfactory

    # FIRST, before a socket, a checkout read or a session bootstrap: a
    # malformed, duplicated or non-conforming binding refuses the BUILD, and it
    # costs nothing to find out before the expensive work starts. The profile's
    # own bindings go through the SAME collection — a collision between a
    # contributed route and one of this assembly's own is refused here too.
    route_bindings = route_extension.collect_bindings(
        tuple(profile_openxfactory.ROUTE_EXTENSIONS) + tuple(route_extensions))

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
        # ONE fresh abstract cache per served process, beside it and never it
        # (add-doxbench-distilled-abstract §5.3, N1). Two stores, two bounds:
        # abstract churn over a scope larger than the abstract bound evicts
        # abstracts and nothing else.
        "abstract_store": doxbench_abstract_store.AbstractStore(),
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
        # The contributed routes, already in consult order (§ 2.4). One more
        # injected class attribute, exactly like the seams above it.
        "route_bindings": route_bindings,
    })
    # A ROUTE THAT CANNOT BE SERVED MUST NOT START. Resolved against the bound
    # class — the object the dispatch will `getattr` on — so a binding naming a
    # handler this server does not have is a refused build rather than a stack
    # trace on the first live connection.
    route_extension.resolve_handlers(route_bindings, bound)
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
    # THE MODEL PROVIDER, declared by the same entrypoint discipline. This is
    # the STANDALONE SECONDARY PATH: the primary entrypoint is
    # `cli.cmd_generate_and_open`, which makes the identical declaration with
    # its own `--model-session-root` flag. Both are written out because a
    # declaration only one of them makes is a serve whose operator cannot tell
    # which install talks to a model — and `setdefault` keeps a caller's own
    # factory (a test, a harness) exactly as the two above do.
    #
    # The session root follows the SAME rule the CLI defaults to — beside the
    # served snapshot — so the two entrypoints cannot drift into writing harness
    # sessions in two different places.
    #
    # `doxbench_install` is imported at module scope (see the import block's own
    # note): the graph is acyclic and importing the declaration starts nothing.
    # What stays an ENTRYPOINT decision is this call -- the two entrypoints are
    # the only places that reach for the real declaration, and `build_server`
    # still never does it on a caller's behalf.
    #
    # SINCE add-model-provider-broker (ratified 2026-08-26) the declaration is
    # `declared_model_port_factory`, which reads the checkout's model-provider
    # BINDINGS and resolves the broker-backed port when one is declared. A
    # checkout declaring none resolves exactly the harness factory this line
    # used to name, so the unconfigured posture is unchanged byte for byte.
    # This file still names no provider endpoint, holds no credential and holds
    # no token: all three live in `doxbench_provider` and nowhere else, which
    # is the narrowed boundary the structural test enforces.
    build_kwargs.setdefault(
        "model_port_factory",
        doxbench_install.declared_model_port_factory(
            doxbench_install.session_root_beside(snapshot_path),
            checkout_root=checkout_root))
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
