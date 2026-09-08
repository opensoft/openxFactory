"""The openXdox column of the dashboard serve: the executing gate routes
(`split-opendox-two-layer-product` § 2.4, PR 3 of 4).

The gate console's HTTP door — design § D3's "gate console and verbs" cluster,
the LOOP openXdox owns — lifted out of `serve.py` UNCHANGED, byte for byte, on
the same reasoning `serve_workbench.py` and `serve_project.py` give: a mixin
`DashboardHandler` composes, so `self.loopback`, `self.capabilities`,
`self.actor`, `self._not_the_human_console()`, `self._session_registry()`,
`self._session_repository()` and every other gating primitive still resolve
through the MRO to the ONE core implementation.

THIN GLUE, NOT A REWRITE. The verb logic never lived here: `gate_console.py` and
`gate_routes.py` hold it, and this handler imports them FUNCTION-LOCALLY, exactly
as it did in `serve.py` (the literal `from ideation_dashboard import gate_routes`
is asserted to be in the serve surface by `test_repo_selector.py`). What moved is
the door — three refusals, one body read, one dispatch, one 500 log.

THE FIRST ROUTE THAT ARRIVES THROUGH THE SEAM. Unlike PR 2's columns, this one is
NOT a fixed core arm any more: `do_POST` no longer branches on
`ACTIONS_GATE_PREFIX`, and the prefix is contributed as a `RouteBinding` instead
(`GateRoutesExtension` below, assembled in `profile_openxfactory.py`). The
dispatch is `getattr(self, "_handle_gate_action")(remainder)` against the LIVE
handler, so the refusals below are reached by construction rather than by an
author's memory — which is the whole safety argument the seam makes
(`route_extension.py`'s own docstring, and `corpus-adapter-seam` requirement 4's
"no privileged route" one level up).

INVOCATION (design D12): `serve.py` runs BOTH as a script and as a module, so
this module uses ABSOLUTE `ideation_dashboard.*` imports, never `from . import`,
and self-inserts `scripts/` on the import path for the bare `route_extension`
import the same way `serve.py` and `snapshot_registry.py` do.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:  # plain-script parity with serve.py (D12)
    sys.path.insert(0, str(_SCRIPTS_DIR))

import route_extension  # noqa: E402

from ideation_dashboard.serve_wire import (  # noqa: E402
    AGENT_INVOCATION_REFUSAL,
    DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
    DOXBENCH_MAX_REQUEST_BYTES,
    JSON_OBJECT_BODY_REQUIRED,
    doxbench_error_body,
    doxbench_error_status,
)

#: The gate console's route PREFIX — `/actions/gate/<verb>`. Moved here with the
#: handler it addresses, and re-imported by name into `serve.py` so
#: `serve.ACTIONS_GATE_PREFIX` still resolves for every reader that had it.
ACTIONS_GATE_PREFIX = "/actions/gate/"


class GateRoutes:
    """The gate-verb door, mixed into `DashboardHandler`.

    Every `self.<name>` below resolves to `serve.py`'s own core implementation
    through the MRO — that is what makes a contributed route reach the same
    loopback verdict, the same capability dict, the same console test and the
    same session seams a fixed core arm reaches.
    """

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


class GateRoutesExtension:
    """openXdox's route contribution: the gate-verb prefix, and nothing else.

    Conforms to `route_extension.RouteExtension` STRUCTURALLY (the protocol is
    `runtime_checkable`), so nothing about this class is imported by the core it
    contributes to — the direction that lets the § 3 carve take this file whole.
    """

    def routes(self) -> tuple[route_extension.RouteBinding, ...]:
        return (
            # The prefix arm `do_POST` used to carry verbatim: the same pattern,
            # the same `path[len(ACTIONS_GATE_PREFIX):]` remainder (computed once
            # in `RouteBinding.remainder` now), the same handler.
            route_extension.RouteBinding("POST", ACTIONS_GATE_PREFIX, True,
                                         "_handle_gate_action"),
        )
