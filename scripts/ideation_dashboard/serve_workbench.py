"""The openDox column of the dashboard serve: the doxBench workbench routes
(`split-opendox-two-layer-product` § 2.4, PR 2 of 4).

The model catalog, the model-intake surface and its two acts, the chat turn, the
per-document distilled abstract and the thread read — the routes design § D2
assigns to openDox — lifted out of `serve.py` UNCHANGED, byte for byte, as a
mixin `DashboardHandler` composes.

THEY ARE STILL FIXED CORE ROUTES. Nothing here is registered through the route
extension point: `_route()` and `do_POST()` dispatch to these handlers by the
same names, in the same order, as before the move (which
`tests/ideation-dashboard/test_extension_point_parity.py` pins arm by arm). The
extension point is for the columns openDox does NOT keep; these it does.

WHY A MIXIN AND NOT MODULE-LEVEL FUNCTIONS REBOUND ONTO THE CLASS. The block
carries three `@staticmethod`s and two `@classmethod`s, and the suites call
several members unbound off the class (`handler._workbench_model_port(handler)`,
`DashboardHandler._doxbench_invalid_turn_message(...)`). Inheritance keeps every
one of those spellings working, and per-test overrides
(`handler._indexed_sources = …`) keep resolving through the MRO. Rebinding plain
functions would have silently dropped `cls` from the classmethods.

EVERY GATING CALL IS UNCHANGED, and that is the load-bearing property. These
methods reach `self._not_the_human_console()`, `self._send_json`,
`self._serve_bytes`, `self._read_json_body`, `self._read_bounded_json_body` and
the injected class attributes (`loopback`, `capabilities`, `actor`,
`checkout_root`, `source`, `model_port_factory`, `schema_validator_factory`,
`turn_store`, `abstract_store`, `packet_assembler`, `usage_meter`,
`knowledge_declaration`) by name on the LIVE handler, exactly as they did when
they sat in `serve.py`. A mixin cannot bypass a gate its own class defines.

INVOCATION (design D12): `serve.py` runs BOTH as a script and as a module, so
this module uses ABSOLUTE `ideation_dashboard.*` imports, never `from . import`.
"""

from __future__ import annotations

import json
import sys
import threading
import time
import urllib.parse
from pathlib import Path

from ideation_dashboard import doxbench_abstract_store
from ideation_dashboard import doxbench_knowledge
from ideation_dashboard import doxbench_packet
from ideation_dashboard import doxbench_threads
from ideation_dashboard import snapshot_registry as registry_mod
from ideation_dashboard.serve_wire import (
    DOXBENCH_ABSTRACT_REFUSED_PROSE_BYTES,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_BYTES,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_DISTILLABLE,
    DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_ELIGIBLE,
    DOXBENCH_CHAT_TURN_V2_FAILURE_KIND,
    DOXBENCH_CHAT_TURN_V2_KIND,
    DOXBENCH_CHAT_TURN_V2_SUCCESS_KIND,
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
    DOXBENCH_MAX_REQUEST_BYTES,
    DOXBENCH_MODEL_CATALOG_KIND,
    JSON_CTYPE,
    JSON_OBJECT_BODY_REQUIRED,
    NO_LIVE_SESSION_CAUSE,
    NO_RESOLVED_ACTOR_CAUSE,
    _ABSTRACT_REASON_NOT_DISTILLABLE,
    _ABSTRACT_REASON_NOT_ELIGIBLE,
    _ABSTRACT_REASON_NO_DECLARED_BASE,
    _ABSTRACT_REASON_SUBJECT_BYTES,
    _CredentialStream,
    _DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT,
    _MAX_BODY_BYTES,
    _abstract_reason_prose_bytes,
    _drain_refused_body,
    _no_dereference,
    _sidecar_text,
    _thread_absence_body,
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
    mint_ledger_snapshot,
    provider_retry_fact,
)


class WorkbenchRoutes:
    """The doxBench workbench half of `DashboardHandler`.

    Declared as a mixin rather than a standalone class because every method here
    is a request handler on the live handler instance: it reads `self.path`,
    `self.headers` and `self.rfile` from `BaseHTTPRequestHandler` and answers
    through the core's own send/refuse primitives. It is never instantiated on
    its own, and it deliberately declares no `__init__`.
    """

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
        reports only presence/absence. Its CONSUMERS call it: the catalog
        handler reads `catalog()`, and the turn route reaches `dispatch`
        through `_deadline_bound_dispatch` -> `doxbench_model.dispatch_turn`
        below. (This docstring used to say "no route below calls it -- the
        dispatch arm is T051's"; T051's dispatch arm landed and the sentence
        was false from that day. Corrected by
        add-doxbench-distilled-abstract task 2.4.)

        THE RESOLVED PORT IS NOT NECESSARILY A FRESH ONE. Where the declared
        adapter is stateful -- the harness bridge the entrypoints declare holds
        per-document-thread sessions -- the factory returns ONE instance for
        the life of the process and this accessor hands back that same object
        on every request. Nothing here may assume a per-request adapter."""
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

    @staticmethod
    def _doxbench_violation_beside_the_buffers_floor(validators, kind: str,
                                                     instance) -> bool:
        """True when the released schema faults `instance` for ANYTHING other
        than the `buffers` array's own `minItems` floor.

        This is the guard that keeps a cause-naming refusal from sending a human
        round a loop. Naming the missing document is only useful if loading one
        is ENOUGH; where a blank message, a bad hash, or an unknown key is also
        wrong, fixing the buffer set would just earn a second refusal, so the
        caller falls back to the catch-all -- which is true of all of them.

        Conservative in both failure directions: no validator for the kind, or a
        validator that throws, means no verdict, and no verdict is treated as
        "something else may be wrong" rather than as permission to be specific.
        An EMPTY error list is False -- nothing else is wrong -- which is what
        lets the delegated validator's own statement of the floor name the same
        cause on a plane whose schema did not catch it first.

        WHAT IT READS, AND WHAT IT REFUSES TO READ. Only `validator` (a schema
        KEYWORD, `minItems`) and `absolute_path` (the INSTANCE location,
        `buffers`). Never `error.message` -- that is the field
        `_doxbench_wire_conforms` discards for cause, because a jsonschema
        message can quote instance content. Nothing read here reaches the wire in
        any case: the verdict only chooses between two fixed module-level
        strings.

        STREAMED, and stopping at the first disqualifying error (Copilot review,
        PR #255). The answer is a bare "is there one?", so materializing every
        violation of a large invalid request only to scan it was work and memory
        spent on a question already settled by error number one.

        The pass `_doxbench_wire_conforms` already made is deliberately NOT
        reused. Carrying its errors out would mean that seam returning them, and
        its whole posture is that it discards them precisely so a jsonschema
        message -- which can quote instance content -- has nowhere to leak to.
        Two cheap iterations on an already-failing request is the better trade
        against widening that seam's contract."""
        validator = validators.get(kind) if isinstance(validators, dict) else None
        if validator is None:
            return True
        try:
            for error in validator.iter_errors(instance):
                if (error.validator != "minItems"
                        or list(error.absolute_path) != ["buffers"]):
                    return True
        except Exception:  # noqa: BLE001 - a broken validator names no cause
            return True
        return False

    @staticmethod
    def _doxbench_turn_is_outline_only(payload) -> bool:
        """True when the request's buffer set is exactly one buffer and that
        buffer is the reserved outline -- the state a human reaches by unloading
        the last document.

        The floor is also short with ZERO buffers, and with one buffer that is a
        document and no outline. Neither is the outline-only state, and telling
        either of them that the turn 'carries no document beside the outline'
        would state something false about a set that has no outline in it. Those
        keep the catalog's generic message, which is true of both."""
        buffers = payload.get("buffers") if isinstance(payload, dict) else None
        if not isinstance(buffers, list) or len(buffers) != 1:
            return False
        only = buffers[0]
        return isinstance(only, dict) and only.get("kind") == "outline"

    @classmethod
    def _doxbench_invalid_turn_message(cls, validators, kind: str, payload):
        """Which fixed message an `invalid_turn_request` refusal of a request's
        SHAPE carries: the cause-naming one when the buffer set is outline-only
        and nothing else is wrong, else `None` for the catalog's generic message.

        Both conditions are required, and each rules out a different way of
        lying: the first that the message describes the set the caller actually
        sent, the second that acting on it is enough to make the turn sendable.

        Asked at BOTH shape gates, because the floor has TWO statements and
        either can be the one that fires. The released schema's `minItems: 2`
        answers first wherever the real release is bound, and the delegated
        validator's outline-plus-document pairing rule answers where a validator
        that does not express the floor let the request through. The CAUSE is a
        fact about the request, not about which gate noticed it, so both name it
        the same way rather than one of them staying mute."""
        if not cls._doxbench_turn_is_outline_only(payload):
            return None
        if cls._doxbench_violation_beside_the_buffers_floor(
                validators, kind, payload):
            return None
        return _DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT

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
    # A PROVIDER IS REACHED FROM HERE, THROUGH THE PORT AND NOWHERE ELSE.
    # This banner used to say "NO PROVIDER IS EVER CONTACTED FROM THIS SLICE
    # ... no code below calls it -- until T051's dispatch arm lands"; that arm
    # landed, `_deadline_bound_dispatch` calls `doxbench_model.dispatch_turn`
    # with the resolved port, and the sentence has been false since. Corrected
    # by add-doxbench-distilled-abstract task 2.4 rather than left to the next
    # reader to disbelieve.
    #
    # WHAT REMAINS TRUE, and is the claim that always mattered: the ONLY route
    # to a provider below is the injected `WorkbenchModelPort` and its three
    # declared members. No provider SDK import, no provider env-var read, no
    # credential, no raw endpoint and no secret name appears anywhere in this
    # file -- per-turn model selection, harness session handling and any
    # adapter-internal routing all happen INSIDE an adapter, and a fourth
    # provider verb is refused (`FORBIDDEN_PORT_MEMBERS`).

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

    # =====================================================================
    # THE MODEL INTAKE SURFACE (add-doxchat-model-intake §2/§3)
    # =====================================================================
    #
    # THE ONE QUESTION THIS BLOCK EXISTS TO ANSWER: when a human types a
    # provider key into a control on this console, WHERE DOES THAT STRING GO?
    #
    # It goes to the declared broker and nowhere else, and the shape of the
    # route is what makes that structural rather than careful:
    #
    #   * the FACTS ride the query string — the binding id, the label, the
    #     provider, the endpoint, the dialect, the authentication kind — exactly
    #     as they ride the broker's own declared FLAGS, where a fact belongs;
    #   * the BODY is the credential and NOTHING ELSE. It is never parsed, never
    #     decoded into a value this process holds, never assigned to a variable
    #     that outlives the request, and never echoed: it is STREAMED, in chunks,
    #     from this connection's read handle into the broker's standard input,
    #     through `doxbench_provider.hand_off_credential`, whose signature takes
    #     an open handle and refuses to take a value. That signature is the
    #     enforcement — a caller CANNOT pass a credential value to it, so no
    #     caller is holding one either.
    #
    # WHAT COMES BACK is the broker's `reference`, which is the only thing that
    # then lives in a binding, in a file, in a log, or in a review. THE GREP TEST
    # (tasks.md 2.4) is what makes that claim measurable rather than asserted.
    #
    # BOTH ACTS ARE GATED ON THE SAME `session` LOCAL-HUMAN VERDICT the model
    # catalog already reuses (loopback + real checkout + resolved actor), plus
    # the console-presence test, and an agent invocation is refused AND REPORTED
    # like every other gate action. Reusing the gate is deliberate: enrolling a
    # provider and approving one are exactly the kind of action that capability
    # already exists to fence.

    def _workbench_declaration_store(self):
        """The intake DECLARATIONS store for the served checkout, or None.

        Absence is a POSTURE and never an error, mirroring
        `_workbench_model_port`'s own discipline: a plane that fails the reused
        `session` gate, or has no real checkout to hold a settings document, has
        no intake surface — which is the honest answer for a plane that may not
        run a turn either.

        The accessor never READS the document. It hands back a store; the
        callers below decide what to ask it, so a route that only wants to know
        whether intake is offered pays for exactly that question."""
        if not self.capabilities.get("actions", {}).get("session"):
            return None
        if not self.checkout_root:
            return None
        try:
            from ideation_dashboard import doxbench_intake
            return doxbench_intake.DeclarationStore(
                doxbench_intake.declarations_path(Path(self.checkout_root)))
        except Exception:  # noqa: BLE001 - absence is a capability verdict
            return None

    def _intake_console_refusal(self) -> str | None:
        """The fixed refusal CODE this request earns on an intake route, or
        None when it is the local human console.

        ONE gate for all three routes, in the same order the catalog route runs
        its two clauses, so a surface, an act and an approval can never disagree
        about who may reach them."""
        if not (self.loopback
                and self.capabilities.get("actions", {}).get("session")
                and self.actor):
            return DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE
        console_refusal = self._not_the_human_console()
        if console_refusal is not None:
            # REJECT AND REPORT (FR-019): the reason is for the SERVER LOG, and
            # the wire gets the fixed sentence. An agent that reached for the
            # credential surface is exactly the event an operator should be able
            # to find afterwards.
            sys.stderr.write(
                "[workbench/model-intake] agent_invocation refused: "
                f"{console_refusal}\n")
            return DOXBENCH_ERR_CONSOLE_REQUIRED
        return None

    def _intake_refusal(self, code: str, reason: str) -> None:
        """One STATED refusal: the fixed catalog body plus a `reason` drawn from
        `doxbench_intake`'s own module constants.

        The `reason` is never the broker's words, never the provider's, never an
        exception's text and never anything the request carried — the same
        discipline `_thread_absence_body` keeps, and the same discipline
        `doxbench_provider` keeps on its side of the broker seam."""
        body = doxbench_error_body(code)
        body["reason"] = reason
        self._send_json(doxbench_error_status(code), body)

    def _handle_workbench_model_intake_surface(self, head_only: bool) -> None:
        """`GET`/`HEAD /workbench/model-intake` — WHETHER THE FLOW CAN BE OPENED.

        This route is what makes the selector's intake affordance honest. The
        ratified sequencing requirement says the affordance SHALL NOT be released
        ahead of the flow it opens — "an option that names an action and then does
        nothing, or opens a surface that cannot complete, is worse than an absent
        option" — and a browser cannot know whether a broker is declared. So it
        asks, and it renders the affordance only when this route says `offered`.

        `offered` is FALSE, with the fixed reason, when this install declares no
        credential broker. That is the flow REFUSING RATHER THAN DEGRADING: a
        wizard that collected a key with nowhere governed to put it would have to
        hold it somewhere, and every somewhere available to this dashboard is a
        place the standing rule forbids.

        The `auth_kinds` block is read from `doxbench_binding.AUTH_KINDS` through
        `doxbench_intake.auth_kind_disclosure()` and is served rather than
        hard-coded in the page ON PURPOSE: the workspace's absolute views clause
        keeps every credential-shaped spelling out of every browser module, so a
        page that named the kinds itself would carry exactly the vocabulary that
        clause forbids. The browser renders the label and submits the kind
        verbatim."""
        refusal = self._intake_console_refusal()
        if refusal is not None:
            self._send_json(doxbench_error_status(refusal),
                            doxbench_error_body(refusal))
            return
        from ideation_dashboard import doxbench_intake
        store = self._workbench_declaration_store()
        if store is None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        try:
            disclosure = store.read_back()
        except doxbench_intake.IntakeRefused:
            # An unreadable settings document is NOT "no broker": it is a
            # document this console cannot answer about, and offering enrolment
            # on top of one would be offering to write into a file it could not
            # read first.
            disclosure = None
        offered = bool(disclosure and disclosure.get("broker"))
        from ideation_dashboard import doxbench_binding
        envelope: dict = {
            "kind": "workbench-model-intake",
            "offered": offered,
            "auth_kinds": doxbench_intake.auth_kind_disclosure() if offered
                          else [],
            # THE DIALECT VOCABULARY IS SERVED, NOT SPELLED IN THE PAGE, for the
            # same reason the authentication kinds are: it is a CLOSED
            # vocabulary the binding record owns and validates, and a browser
            # that hard-coded it would be a second place to keep it in step. An
            # unknown grammar is refused when the operator DECLARES the binding
            # — earlier than a mint, and earlier than a paid call — so the
            # surface offers exactly what will be accepted.
            "dialects": list(doxbench_binding.DIALECTS) if offered else [],
            "declarations": (disclosure or {}).get("declarations", []),
        }
        if not offered:
            envelope["reason"] = doxbench_intake.NO_BROKER_NOTICE
        self._serve_bytes(json.dumps(envelope).encode("utf-8"), JSON_CTYPE,
                          head_only)

    #: The largest credential this route will carry. A BOUND, not a policy: an
    #: unbounded read of a connection is a way to spend this process's memory by
    #: posting to it, and no provider credential in existence is this long. It is
    #: deliberately far below `_MAX_BODY_BYTES` — a key is not a document.
    MAX_CREDENTIAL_BYTES = 8192

    #: The declared facts an intake act carries on its query string. CLOSED: a
    #: parameter this tuple does not name is refused rather than ignored, so no
    #: caller can smuggle a field the binding shape does not have — and a
    #: credential can never arrive as one, because a query string is a thing
    #: proxies and access logs record.
    INTAKE_QUERY_FIELDS: tuple[str, ...] = (
        "binding", "label", "provider", "endpoint", "dialect", "kind")

    def _handle_workbench_model_intake(self) -> None:
        """`POST /actions/workbench/model-intake` — THE ACT THAT CARRIES A
        CREDENTIAL.

        Reads the declared facts off the query string, builds the binding they
        describe, streams THE WHOLE BODY into the declared broker's `intake`, and
        keeps ONLY the reference it returns. Then it writes two records: the
        binding (which names the broker and the reference and has no field a
        secret could occupy) and a PENDING declaration (which says a human has
        not approved this model yet).

        NOTHING here holds the credential. `hand_off_credential` takes an open
        handle, `_CredentialStream` moves bytes from this connection to the
        child's pipe in chunks, and no local, no return value, no log line and no
        exception in this method has ever been the value.

        THE OAUTH KIND IS OFFERED AND NOT SIMULATED. It takes the same path with
        an EMPTY source, because the declared broker's own surface is the
        authorization flow (Brett's OQ-2 ruling) and this dashboard may not be
        the party that receives a provider's tokens. A broker that declares the
        flow takes custody and answers with a reference, and this route stores it
        exactly as it stores an enrolled key's. A broker that does NOT — which is
        every broker declared today — refuses, and the human is told so in this
        repository's own fixed sentence. No redirect is invented, no field that
        would take token material is presented, and no dance is faked."""
        import io

        refusal = self._intake_console_refusal()
        if refusal is not None:
            self._send_json(doxbench_error_status(refusal),
                            doxbench_error_body(refusal))
            return
        from ideation_dashboard import doxbench_binding
        from ideation_dashboard import doxbench_intake
        from ideation_dashboard import doxbench_provider
        store = self._workbench_declaration_store()
        if store is None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except (TypeError, ValueError):
            length = -1
        declared = self._intake_query_facts()
        if declared is None:
            # DRAIN BEFORE ANSWERING, on the same reasoning the bounded JSON
            # reader drains: refusing with every byte unread closes the socket on
            # a client still mid-body, and the kernel's reset can destroy the
            # queued refusal before the client reads it. The bytes are read and
            # DISCARDED — never parsed, never assembled, never looked at.
            if length > 0:
                _drain_refused_body(self.rfile, length)
            self._send_error_or_intake(DOXBENCH_ERR_INVALID_INTAKE_REQUEST)
            return
        if length < 0 or length > self.MAX_CREDENTIAL_BYTES:
            if length > 0:
                _drain_refused_body(self.rfile, length)
            self._send_error_or_intake(DOXBENCH_ERR_INVALID_INTAKE_REQUEST)
            return
        if (length <= 0
                and declared["kind"] == doxbench_binding.AUTH_KIND_API_KEY):
            # AN EMPTY BODY IS NOT A CREDENTIAL (PR #401 review). The api_key
            # kind's whole body IS the secret, so a request declaring
            # `Content-Length: 0` — or declaring no length at all, which this
            # route reads as zero — has declared that it is enrolling nothing.
            # Handing that to the broker would ask a custodian to take custody
            # of an empty value and would come back with a reference naming it,
            # and the binding and the PENDING declaration written afterwards
            # would then say a credential exists where none does. That is worse
            # than a refusal, because the records are the only thing anyone
            # afterwards can read.
            #
            # REFUSED HERE, WITH THE LENGTH'S OWN KIN, and not one line later:
            # this is a malformed request rather than a posture the server
            # declines, so it earns the 400 shape the closed query vocabulary
            # and the over-bound length already earn — no new failure code, and
            # the broker child is never spawned. Nothing is drained because
            # nothing was declared.
            #
            # `api_key` ONLY, deliberately. The oauth kind is SUPPOSED to send
            # an empty body: the dashboard may not be the party that receives a
            # provider's tokens (OQ-2), so that intake reaches the broker with
            # an empty source on purpose and is refused — or not — by the
            # broker's own declared flow rather than by this check.
            self._send_error_or_intake(DOXBENCH_ERR_INVALID_INTAKE_REQUEST)
            return
        try:
            broker = store.broker()
        except doxbench_intake.IntakeRefused as error:
            self._intake_refusal(DOXBENCH_ERR_INTAKE_REFUSED, str(error))
            return
        if broker is None:
            # NO FIELD THAT WOULD ACCEPT A SECRET WAS EVER PRESENTED, because
            # the surface route already answered `offered: false`. A caller that
            # posted anyway gets the same sentence, and the body it sent is
            # drained and dropped unread rather than parsed.
            if length > 0:
                _drain_refused_body(self.rfile, length)
            self._intake_refusal(DOXBENCH_ERR_INTAKE_REFUSED,
                                 doxbench_intake.NO_BROKER_NOTICE)
            return
        try:
            binding = doxbench_binding.ModelProviderBinding(
                id=declared["binding"],
                label=declared["label"],
                provider=declared["provider"],
                # A PLACEHOLDER UNTIL THE BROKER ANSWERS. The record that
                # reaches the store below carries the reference the broker
                # returned; this value exists only so the invocation can be
                # built, and it is replaced before anything is written.
                credential_ref="pending-broker-intake",
                auth_kind=declared["kind"],
                approved_by=str(self.actor),
                endpoint=declared["endpoint"],
                dialect=declared["dialect"],
                broker_argv=broker.argv)
        except doxbench_binding.BindingRefused as error:
            if length > 0:
                _drain_refused_body(self.rfile, length)
            self._intake_refusal(DOXBENCH_ERR_INVALID_INTAKE_REQUEST,
                                 str(error))
            return
        accepts_secret = (
            declared["kind"] == doxbench_binding.AUTH_KIND_API_KEY)
        source = (_CredentialStream(self.rfile, length)
                  if accepts_secret else io.StringIO(""))
        if not accepts_secret and length > 0:
            # A KIND THAT TAKES NO SECRET IS SENT NONE, and anything that
            # arrived anyway is dropped unread at the descriptor rather than
            # forwarded. The broker refuses an oauth intake before reading its
            # standard input at all, so forwarding would have been forwarding a
            # value nobody was going to read into a process that would not store
            # it — and reading it here to discard it would make this process hold
            # a credential for no reason at all.
            _drain_refused_body(self.rfile, length)
        try:
            reference = doxbench_provider.hand_off_credential(binding, source)
        except doxbench_provider.BrokerRefused as error:
            # THE BROKER'S OWN WORDS NEVER REACH HERE: `BrokerRefused` carries
            # one of `doxbench_provider.FIXED_DIAGNOSTICS` and nothing else, and
            # the oauth kind is additionally given this repository's own sentence
            # about what it means when a broker declines to open an authorization
            # flow.
            reason = (doxbench_intake.OAUTH_UNAVAILABLE_NOTICE
                      if not accepts_secret else str(error))
            self._intake_refusal(DOXBENCH_ERR_INTAKE_REFUSED, reason)
            return
        except Exception:  # noqa: BLE001 - no broker-shaped exception on the wire
            self._intake_refusal(DOXBENCH_ERR_INTAKE_REFUSED,
                                 doxbench_provider.DIAG_BROKER_UNREACHABLE)
            return
        import dataclasses as _dataclasses
        stored = _dataclasses.replace(binding, credential_ref=reference)
        bindings = doxbench_binding.BindingStore(
            doxbench_binding.bindings_path(Path(self.checkout_root)))
        try:
            bindings.add(stored)
            declaration = store.propose(doxbench_intake.ModelDeclaration(
                binding_id=stored.id,
                status=doxbench_intake.STATUS_PENDING,
                install_posture=doxbench_intake.POSTURE_SINGLE_OPERATOR,
                proposed_by=str(self.actor),
                proposed_at=doxbench_intake.stamp()))
        except (doxbench_binding.BindingRefused,
                doxbench_intake.IntakeRefused) as error:
            self._intake_refusal(DOXBENCH_ERR_INTAKE_REFUSED, str(error))
            return
        # THE ANSWER CARRIES THE BINDING'S READ-BACK AND THE DECLARATION'S, both
        # of which are safe to read, log and commit precisely because they name a
        # secret they do not contain. The pending sentence is the one the human
        # most needs: completing this flow did NOT make a model available.
        self._send_json(200, {
            "ok": True,
            "kind": "workbench-model-intake-result",
            "binding": stored.as_read_back(),
            "declaration": declaration.as_read_back(),
            "availability": doxbench_intake.PENDING_NOTICE,
        })

    def _intake_query_facts(self):
        """The declared facts off this request's query string, or None.

        CLOSED: every member of `INTAKE_QUERY_FIELDS` must be present exactly
        once and non-blank, and a parameter outside the tuple refuses the whole
        request rather than being ignored — a caller that believed it had
        declared something must never have it silently dropped, and a credential
        must never be accepted as a query parameter under any spelling."""
        raw = urllib.parse.parse_qs(
            urllib.parse.urlsplit(self.path).query, keep_blank_values=True)
        if set(raw) != set(self.INTAKE_QUERY_FIELDS):
            return None
        facts = {}
        for field in self.INTAKE_QUERY_FIELDS:
            values = raw[field]
            if len(values) != 1 or not str(values[0]).strip():
                return None
            facts[field] = str(values[0]).strip()
        return facts

    def _send_error_or_intake(self, code: str) -> None:
        self._send_json(doxbench_error_status(code), doxbench_error_body(code))

    def _handle_workbench_model_approval(self) -> None:
        """`POST /actions/workbench/model-approval` — THE RECORDED HUMAN ACT.

        Completing an intake produced a PROPOSED declaration; this is the second
        decision, and keeping the two apart is the whole of §3. If completing the
        flow had set `available`, then supplying a payment credential would have
        been the same act as approving a provider to process governed corpus
        material — and the placeholder the human is looking at says "approved
        model", so the word is already making a promise.

        THE RECORD IS WRITTEN BEFORE THE SETTINGS DOCUMENT MOVES. A crash between
        the two leaves an audit record for an approval that did not take effect,
        which is readable and recoverable; the other order would leave an
        available model no record accounts for, which is the state this act
        exists to make impossible.

        AGENT INVOCATION REFUSES AND IS REPORTED, exactly as every other gate
        action refuses one — through the shared `_intake_console_refusal` above,
        which writes the reason to the server log and puts the fixed sentence on
        the wire."""
        refusal = self._intake_console_refusal()
        if refusal is not None:
            self._send_json(doxbench_error_status(refusal),
                            doxbench_error_body(refusal))
            return
        from ideation_dashboard import doxbench_intake
        from ideation_dashboard import gate_console
        store = self._workbench_declaration_store()
        if store is None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        payload = self._read_json_body()
        if not isinstance(payload, dict):
            self._send_error_or_intake(DOXBENCH_ERR_INVALID_INTAKE_REQUEST)
            return
        binding_id = payload.get("binding")
        if not isinstance(binding_id, str) or not binding_id.strip():
            self._send_error_or_intake(DOXBENCH_ERR_INVALID_INTAKE_REQUEST)
            return
        binding_id = binding_id.strip()
        try:
            declaration = store.get(binding_id)
        except doxbench_intake.IntakeRefused as error:
            self._intake_refusal(DOXBENCH_ERR_APPROVAL_REFUSED, str(error))
            return
        if declaration is None or declaration.status != doxbench_intake.STATUS_PENDING:
            self._intake_refusal(
                DOXBENCH_ERR_APPROVAL_REFUSED,
                "no declaration is pending under that name on this install; "
                "there is nothing here to approve")
            return
        binding = self._approval_binding(binding_id)
        if binding is None:
            self._intake_refusal(
                DOXBENCH_ERR_APPROVAL_REFUSED,
                "the declaration names a binding this checkout does not "
                "declare; approving a model whose broker invocation is gone "
                "would record an authority over nothing")
            return
        import dataclasses as _dataclasses
        at = doxbench_intake.stamp()
        approved = _dataclasses.replace(
            declaration,
            status=doxbench_intake.STATUS_APPROVED,
            issued_by=binding.approved_by,
            approved_by=str(self.actor),
            expires_at=doxbench_intake.approval_expiry(),
            audit_ref=binding.credential_ref)
        record = gate_console.build_gate_action_record(
            actor=str(self.actor),
            action=doxbench_intake.GATE_ACTION_APPROVE_MODEL,
            at=at,
            model_declaration=binding_id,
            model_approval=approved.approval_block(),
            provenance=gate_console.HTTP_CONSOLE_TOKEN,
            artifacts=[{"kind": "other",
                        "reference": doxbench_intake.declarations_path(
                            Path(self.checkout_root)).relative_to(
                                Path(self.checkout_root)).as_posix()}])
        try:
            gate_console.validate_gate_action_record(record)
            human = gate_console.HumanGate(
                Path(self.checkout_root),
                [gate_console.DEFAULT_RECORDS_DIR],
                human_actor=str(self.actor))
            gate_console.write_gate_action_record(
                human, gate_console.DEFAULT_RECORDS_DIR, record)
            store.approve(
                binding_id,
                issued_by=approved.issued_by,
                approved_by=approved.approved_by,
                expires_at=approved.expires_at,
                audit_ref=approved.audit_ref,
                consent_ref=approved.consent_ref)
        except (gate_console.GateRefused, doxbench_intake.IntakeRefused,
                OSError) as error:
            self._intake_refusal(DOXBENCH_ERR_APPROVAL_REFUSED, str(error))
            return
        self._send_json(200, {
            "ok": True,
            "kind": "workbench-model-approval-result",
            "declaration": approved.as_read_back(),
            "availability": doxbench_intake.APPROVAL_NOTICE,
        })

    def _approval_binding(self, binding_id: str):
        """The binding a pending declaration names, or None. Read through the
        ONE store both entrypoints read, so an approval cannot be recorded
        against a binding the port would never resolve."""
        from ideation_dashboard import doxbench_binding
        try:
            return doxbench_binding.BindingStore(
                doxbench_binding.bindings_path(Path(self.checkout_root))
            ).get(binding_id)
        except doxbench_binding.BindingRefused:
            return None

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
                     failure_kind=DOXBENCH_CHAT_TURN_V2_FAILURE_KIND,
                     message=None) -> None:
        """Emit one chat-turn refusal in the correct envelope.

        With a wire-valid `turn_id` this is the RELEASED
        `workbench-chat-turn-v2-failure` envelope, SELF-VALIDATED against the
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

        `failure_kind` NAMES the envelope the refusal is answered in. Until
        contract-v3.0 two families were served, it followed the family the
        request arrived in, and it defaulted to the v1 envelope -- which is what
        a request that never named a recognizable family got. One family is
        served now, and an unrecognized kind is REFUSED in it rather than
        coerced into a family that no longer exists; the default moved with the
        removal (retire-doxbench-chat-turn-v1).

        THE PRE-IDENTITY FALLBACK BELOW IS UNCHANGED BY THAT REMOVAL, and
        deliberately so. It is the correct answer for a request carrying no
        wire-valid identity, and it is what lets the redesigned unknown-kind
        refusal REQUIRE a `client_turn_id` without inventing one: `failure_v2`
        makes that field mandatory, and no server may fabricate a correlation
        key for a turn it never accepted.

        `message` names the CAUSE inside an otherwise unchanged refusal, and is a
        fixed module-level constant or nothing (see `doxbench_turn_failure_body`).
        It rides only the RELEASED envelope: the pre-identity fallback below keeps
        the catalog message unconditionally. That is not a gap. The fallback is
        taken when the turn id is not wire-valid, and a turn id the released
        schema rejects is itself a second schema violation -- so no caller whose
        message depends on the violation being the SOLE one can reach it."""
        status = doxbench_error_status(code)
        if turn_id is not None:
            body = doxbench_turn_failure_body(code, turn_id, limit=limit,
                                              kind=failure_kind, message=message)
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
        # WHICH KIND THIS TURN NAMED (contract-v3.0,
        # retire-doxbench-chat-turn-v1). One family is served, so this is no
        # longer a choice BETWEEN families: it is the surviving request kind or
        # it is nothing.
        #
        # THE FALLBACK IS REDESIGNED, NOT DELETED. Until contract-v3.0 an
        # unrecognized or absent `kind` was COERCED into the deprecated v1
        # family, on the stated reason that "a request that never named a family
        # it could be answered in gets the posture it would have got before this
        # release". That reason died with v1: after the removal the old default
        # would select a parser and an envelope builder that no longer exist,
        # turning an unrecognized kind into a server FAULT rather than a
        # refusal. So the arm refuses instead, in the SURVIVING family, with an
        # explicit code -- and a retired v1 kind takes exactly this path,
        # because after the removal a retired kind and a kind that never existed
        # are the same fact about the wire.
        #
        # The refusal deliberately does NOT tell a client that the kind it sent
        # used to work. The surviving contract has no vocabulary for "removed at
        # a major", and inventing one to soften a refusal would put migration
        # guidance on the wire instead of in the changelog, where a consumer
        # upgrading across the major actually reads it.
        #
        # `_refuse_turn` below keeps its own SECOND layer, untouched: with no
        # wire-valid `client_turn_id` this refusal leaves the contract envelope
        # and answers in `doxbench_error_body`'s fixed pre-identity shape,
        # because `failure_v2` REQUIRES a `client_turn_id` and no server may
        # invent one to reach a contract envelope.
        request_kind = (payload.get("kind")
                        if isinstance(payload.get("kind"), str) else None)
        validators = self._doxbench_validators()
        if validators is None:
            # No readable contract, so no validated turn is possible. Fail
            # closed on the fixed pre-identity shape: this is a PLANE-level
            # verdict, not a defect in the caller's request, so it must not be
            # reported as one.
            #
            # HOISTED ABOVE THE KIND CHECK at contract-v3.0, because the
            # unrecognized-kind refusal below is itself SELF-VALIDATED against
            # the released schema and so cannot be built without validators.
            # The precedence is unchanged and deliberate: a plane-level verdict
            # outranks any defect in the caller's request.
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        if request_kind != DOXBENCH_CHAT_TURN_V2_KIND:
            self._refuse_turn(validators, DOXBENCH_ERR_UNRECOGNIZED_TURN_KIND,
                              turn_id,
                              failure_kind=DOXBENCH_CHAT_TURN_V2_FAILURE_KIND)
            return
        failure_kind = DOXBENCH_CHAT_TURN_V2_FAILURE_KIND
        parse_body = self._parse_workbench_chat_turn_v2_body
        if not self._doxbench_wire_conforms(validators, request_kind, payload):
            # The verdict is already taken; this only asks WHICH violation, so
            # the one a human can reach by hand -- unloading the set down to the
            # outline -- is answered with a sentence naming the missing document
            # instead of the catch-all. Same code, same status, same key set;
            # every other violation still gets the catalog's message, because
            # `_doxbench_invalid_turn_message` returns None for all of them.
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind,
                              message=self._doxbench_invalid_turn_message(
                                  validators, request_kind, payload))
            return

        fields = parse_body(payload)
        if fields is None:
            # The floor's OTHER statement (`require_outline_and_documents`). It
            # is unreachable for this cause wherever the real release is bound --
            # `minItems: 2` refuses an outline-only set above -- but a plane
            # whose validator does not express the floor lands here instead, and
            # the same act deserves the same sentence either way.
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind,
                              message=self._doxbench_invalid_turn_message(
                                  validators, request_kind, payload))
            return
        client_turn_id = fields["client_turn_id"]
        scope_fields = fields["scope_fields"]
        # The v1 envelope's own field, absent from the widened one by
        # construction. Read as an OPTIONAL member so the widened lane has
        # nothing to read it from -- the point of the release, not an oversight.
        #
        # ALWAYS `None` SINCE contract-v3.0, and DELIBERATELY still read. The v1
        # parser that could return it is gone with its family, so this is now a
        # constant. It is not deleted because it is a member of the idempotency
        # digest's canonical form below: dropping a key from that form changes
        # the digest of every turn, which would strand every record already in a
        # turn store behind a key nothing recomputes. A retirement that promises
        # to touch nothing in the surviving family does not get to invalidate
        # its stored answers on the way past. Retiring the key is a turn-store
        # migration, not a schema removal, and it is not this change's.
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
                    # binding arrives from the parser as `bound_buffer` and is
                    # never derived here from an adjacent field, which is the
                    # mis-derivation Phase A's review killed. (Until
                    # contract-v3.0 the deprecated envelope declared it as
                    # `active_document_path` instead, and a v1 turn that
                    # declared nothing passed `None`, on which the module's own
                    # rule refused a path-backed document rather than guessing.
                    # One lane is left and it always declares.)
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
            # The pairing rule is the floor's THIRD statement, and the one that
            # actually fires for an outline-only widened turn on a plane whose
            # validator did not express `minItems: 2`. Every other way to fail
            # the pairing -- two outlines, a reserved-key claim, a document with
            # no outline -- is not an outline-only set, so the chooser returns
            # None for all of them and they keep the catch-all.
            self._refuse_turn(validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                              turn_id, failure_kind=failure_kind,
                              message=self._doxbench_invalid_turn_message(
                                  validators, request_kind, payload))
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
        # the canonical form. `active_document_path` stays exactly where it was
        # so digests are unchanged; it was the v1 lane's declared binding, and
        # since contract-v3.0 it is a constant `None` here (see the read site).
        # KEEPING A CONSTANT KEY IS THE POINT: removing it would move every
        # digest and orphan every stored turn record.
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
        # THE POSTURE THE TURN RAN UNDER (contract-v1.40, task 10.7), derived
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
            # THE MINT LEDGER, BEFORE AND AFTER (task 3.6). Read around the
            # dispatch so the turn record can state a mid-turn re-mint and the
            # paid retry it bought — the fact Brett's 2026-08-26 ruling requires
            # to be VISIBLE, which until now existed only in three places the
            # browser cannot read. Duck-typed and optional: an adapter with no
            # ledger contributes nothing and nothing about its turns changes.
            mint_ledger_before = mint_ledger_snapshot(turn_port)
            outcome = self._deadline_bound_dispatch(
                turn_port, prompt_envelope, model_entry,
                _typed_response_validator)
            provider_retry = provider_retry_fact(
                mint_ledger_before, mint_ledger_snapshot(turn_port))
            if provider_retry is not None:
                # SAID ON THE CONSOLE TOO. The port already prints its own fixed
                # notice; this line names the TURN, so an operator reading the
                # log can join the paid retry to the conversation that bought it
                # without reading the browser at all.
                sys.stderr.write(
                    "[workbench/chat-turn] the provider token was re-minted "
                    "mid-turn and the turn was retried once (one further paid "
                    f"call) for client turn {client_turn_id}\n")
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
                # THE RECORD. One success envelope is built, unconditionally:
                # until contract-v3.0 this was an if/else over `success_kind`,
                # with a v1 arm building the deprecated two-key envelope. The
                # v1 arm and its two RECORDED limitations left with the family
                # (retire-doxbench-chat-turn-v1); `success_kind` is now the one
                # served kind by construction, so a branch on it would test a
                # condition that cannot be false.
                #
                # It says what the turn was about
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
                # AND SINCE contract-v1.40 (task 10.7) the record STATES the
                # posture its context was assembled under. Derived above,
                # beside the packet, by the same one-place discipline: the
                # values are the PACKET's own, so the record and the packet's
                # own declaration cannot disagree.
                # THE BUILDER'S REFUSALS ARE ON THE ROUTE'S 400 SHAPE, and
                # this `try` is what makes that true (issue #263 review,
                # P2-2). The builder gained refusals when its `str()`
                # coercions went, and this call sits OUTSIDE the packet
                # boundary's `try` several hundred lines up — so an escaping
                # `PacketError` would have been a 500 with a traceback,
                # while the comment in the builder claimed both refusals
                # stayed on one shape. AST-confirmed uncovered before this.
                #
                # Mapped to the SAME fixed `invalid_turn_request` the packet
                # boundary maps every other structural `PacketError` to,
                # rather than a new code: one function, one refusal shape,
                # and the recorded 400-vs-500 tension stays exactly one
                # tension instead of becoming two.
                try:
                    success_body = doxbench_turn_v2_success_body(
                        client_turn_id=client_turn_id,
                        assistant_turn_id="assistant-" + digest[:56],
                        model_id=selected_model["resolved_model_id"],
                        requested_model_id=selected_model[
                            "requested_model_id"],
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
                        # task 3.6: the re-mint and its paid retry, on the
                        # record the human actually reads. Two named scalars
                        # rather than the derived dict, so the builder
                        # rebuilds the closed block itself.
                        provider_retried=provider_retry is not None,
                        provider_retry_audit_ref=(
                            provider_retry.get("audit_ref")
                            if provider_retry else None),
                        assistant_prose=outcome.assistant_prose,
                        proposals=outcome.proposals)
                except doxbench_packet.PacketError:
                    self._refuse_turn(
                        validators, DOXBENCH_ERR_INVALID_TURN_REQUEST,
                        turn_id, failure_kind=failure_kind)
                    return
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

    # ---- the distilled abstract (add-doxbench-distilled-abstract §5) -------
    #
    # THE SECOND MODEL CONSUMER, and it reaches the provider through the SAME
    # seam under the SAME gate: `_workbench_model_port`, the three declared port
    # members, and `_deadline_bound_dispatch` -> `doxbench_model.dispatch_turn`.
    # No fourth provider verb, no second provider path, and nothing smuggled
    # through the chat-turn envelope -- what differs is the REQUEST, which is
    # assembled by `doxbench_turns.build_abstract_envelope` and carries exactly
    # one subject document with no packet, no second buffer, no transcript and
    # no human message.

    @staticmethod
    def _parse_document_abstract_body(payload):
        """The abstract request's known fields, or None.

        The shape is CLOSED and checked here rather than by a released schema,
        because no openxFactory schema declares an abstract request: an unknown
        key is REFUSED rather than ignored. That matters for exactly the keys a
        chat-shaped client would send by habit -- `buffers`, `transcript`,
        `context_packet`, `message` -- because silently dropping one would be the
        smuggling `build_abstract_envelope` exists to refuse, discovered later
        and by nobody.

        The subject path is checked for SHAPE only (repository-relative POSIX,
        no traversal segment): a path that is not one is a MALFORMED request, not
        an ineligible subject, and answering it with the eligibility refusal
        would echo a traversal string back as though it named a document.

        `refresh` is the EXPLICIT REFRESH INTENT the RE-GENERATE control issues
        (packet review, Codex on PR #352). It is OPTIONAL — absent means no
        intent, which is what every selection, mount and tile re-entry sends —
        and it is a BOOLEAN and not a truthy value: `1` and `"true"` are
        malformed, because a request that meant to spend a model call should say
        so in the type the shape declares. Adding it does not open the shape: an
        unknown key is still refused, and that is asserted."""
        known = {"scope", "subject_path", "model_id"}
        if not known <= set(payload) or set(payload) - known - {"refresh"}:
            return None
        refresh = payload.get("refresh", False)
        if not isinstance(refresh, bool):
            return None
        scope = payload.get("scope")
        if not isinstance(scope, dict):
            return None
        if set(scope) != {"repository", "ref", "tile_kind", "tile_id"}:
            return None
        if any(not isinstance(value, str) or not value.strip()
               for value in scope.values()):
            return None
        subject_path = payload.get("subject_path")
        model_id = payload.get("model_id")
        for value in (subject_path, model_id):
            if not isinstance(value, str) or not value.strip():
                return None
        if (subject_path.startswith("/") or "\\" in subject_path
                or "\x00" in subject_path
                or any(segment in ("", ".", "..")
                       for segment in subject_path.split("/"))):
            return None
        return {"scope": scope, "subject_path": subject_path,
                "model_id": model_id, "refresh": refresh}

    def _refuse_abstract(self, code, reason, *, subject_path,
                         subject_digest=None, caption_state=None,
                         wait_bound_seconds=None) -> None:
        """Send one STATED abstract refusal: a declared class, a reason the
        region renders, a caption state, and no prose."""
        body = doxbench_abstract_refusal_body(
            code, reason, subject_path=subject_path,
            subject_digest=subject_digest,
            wait_bound_seconds=wait_bound_seconds,
            **({} if caption_state is None else {"caption_state": caption_state}))
        self._send_json(doxbench_abstract_refusal_status(code), body)

    def _handle_workbench_document_abstract(self) -> None:
        """`POST /actions/workbench/document-abstract` (§5, design D1).

        Every step refuses before the next, and before any disclosure or
        dispatch, in the same load-bearing order the chat-turn handler uses:
        plane, console, body bound, request shape, scope, ELIGIBILITY, the
        subject's saved bytes, the verification base, the model, the assembled
        request, the store, the conversation this generation is bound to, and
        only then a provider."""
        from ideation_dashboard import doxbench_hash
        from ideation_dashboard import doxbench_model
        from ideation_dashboard import doxbench_scope
        from ideation_dashboard import doxbench_turns

        # ---- step 1: the plane. The SAME three-part verdict the catalog and
        # chat-turn routes sit behind -- a loopback human console, a real
        # checkout, a resolved actor -- read through the `session` capability
        # those two already reuse, AND the `gate` capability ruling 7.7 names:
        # where the gate capability is absent the generation control is ABSENT,
        # so a request for one is refused rather than served. `capability_verdict`
        # derives both keys from one `local_human` value today, so naming both is
        # a statement of the rule rather than a second gate; a plane that ever
        # separates them refuses generation and keeps every already-generated
        # abstract readable, which is exactly what 7.7 requires.
        actions = self.capabilities.get("actions", {})
        if not (self.loopback and actions.get("session") and actions.get("gate")
                and self.actor):
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        console_refusal = self._not_the_human_console()
        if console_refusal is not None:
            sys.stderr.write("[actions/workbench/document-abstract] "
                             f"agent_invocation refused: {console_refusal}\n")
            self._send_json(doxbench_error_status(DOXBENCH_ERR_CONSOLE_REQUIRED),
                            doxbench_error_body(DOXBENCH_ERR_CONSOLE_REQUIRED))
            return

        # ---- step 2: the body bound. The TINY pre-existing cap, declared for
        # this route by name: an abstract request carries a scope, a path, a
        # model id and one optional boolean, and never a buffer, so the chat
        # route's 1 MiB bound would be a bound this route has no use for.
        payload, refusal = self._read_bounded_json_body(
            _MAX_BODY_BYTES, "request_body_bytes")
        if refusal is not None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED),
                doxbench_error_body(DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
                                    limit=refusal))
            return
        if payload is None:
            self._send_json(400, {"ok": False, "error": "invalid_body",
                                  "message": JSON_OBJECT_BODY_REQUIRED})
            return

        # ---- step 3: the request shape ----
        fields = self._parse_document_abstract_body(payload)
        if fields is None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_INVALID_ABSTRACT_REQUEST),
                doxbench_error_body(DOXBENCH_ERR_INVALID_ABSTRACT_REQUEST))
            return
        subject_path = fields["subject_path"]
        model_id = fields["model_id"]
        refresh = fields["refresh"]
        key = doxbench_scope.ScopeKey(**fields["scope"])

        # ---- step 4: scope, all from SERVER truth ----
        projection = None
        source_root = None
        snapshot = None
        scope_refused = False
        try:
            entry = self.source.registry.resolve(key.repository, key.ref)
            if entry is None or entry.source_root is None:
                scope_refused = True
            else:
                source_root = Path(entry.source_root)
                snapshot = json.loads(entry.read_bytes())
                created_paths = doxbench_scope.session_created_paths_for_scope(
                    self.source.registry, key, repository=entry.repository,
                    ref=entry.ref, source_root=source_root)
                projection = doxbench_scope.resolve_scope(
                    snapshot, key, source_root=source_root,
                    created_paths=created_paths)
                if projection is None:
                    scope_refused = True
        except (doxbench_scope.ScopeConfinementError, ValueError, OSError):
            scope_refused = True
        if scope_refused:
            # The same fail-closed refusal the chat route gives, so no response
            # is an oracle about which repositories, refs or tiles exist.
            self._send_json(doxbench_error_status(DOXBENCH_ERR_TURN_SCOPE_REFUSED),
                            doxbench_error_body(DOXBENCH_ERR_TURN_SCOPE_REFUSED))
            return

        # ---- step 5: ELIGIBILITY (ruling 7(a)), before any disclosure ----
        # `revalidate_scope` is the ONE authority for "in scope AND editable"
        # (`doxbench_turns._require_in_scope_and_editable`), reached here with no
        # buffers and no declared binding -- which is precisely what an abstract
        # request carries. The `editable_paths` membership is ALSO read directly,
        # because that is the ruled set and the reason the region can state
        # honestly that no distillation is available for a readable-but-not-
        # editable document. A realization MUST NOT widen the disclosure set to
        # reach a subject; widening to `context_paths` is ruling 7(b), a named
        # follow-on with its own delta.
        try:
            doxbench_turns.revalidate_scope(
                projection=projection, request_scope=key,
                bound_buffer_key=None, buffer_keys=(), paths=(subject_path,))
            eligible = subject_path in projection.editable_paths
        except doxbench_turns.TurnScopeError:
            eligible = False
        if not eligible:
            self._refuse_abstract(
                DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_ELIGIBLE,
                _ABSTRACT_REASON_NOT_ELIGIBLE, subject_path=subject_path)
            return

        # ---- step 6: the SUBJECT'S OWN SAVED BYTES ----
        # The served checkout's file, read through `/source`'s own lens, and
        # never a browser buffer: an unsaved buffer's text must not leave the
        # browser, and this route carries no field it could arrive in.
        resolved = registry_mod.resolve_within(source_root, subject_path)
        if resolved is None or not resolved.is_file():
            self._send_json(doxbench_error_status(DOXBENCH_ERR_TURN_SCOPE_REFUSED),
                            doxbench_error_body(DOXBENCH_ERR_TURN_SCOPE_REFUSED))
            return
        try:
            content = doxbench_hash.served_text(resolved.read_bytes())
        except (OSError, UnicodeDecodeError, ValueError):
            self._send_json(doxbench_error_status(DOXBENCH_ERR_TURN_SCOPE_REFUSED),
                            doxbench_error_body(DOXBENCH_ERR_TURN_SCOPE_REFUSED))
            return
        try:
            digest = doxbench_knowledge.document_content_digest(content)
        except doxbench_knowledge.AbstractFormatRefused:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE))
            return

        # ---- step 7: the VERIFICATION BASE, and the refusal it decides ----
        declared_topics, declared_lands = doxbench_declared_fields(
            snapshot, subject_path)
        if not declared_topics and not declared_lands:
            self._refuse_abstract(
                doxbench_knowledge.ABSTRACT_REFUSED_NO_DECLARED_BASE,
                _ABSTRACT_REASON_NO_DECLARED_BASE,
                subject_path=subject_path, subject_digest=digest)
            return

        # ---- step 8: the model ----
        port = self._workbench_model_port()
        if port is None or not callable(getattr(port, "dispatch", None)):
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE))
            return
        try:
            catalog = port.catalog()
        except Exception:  # noqa: BLE001 - never let a provider-shaped exception reach the wire
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_CATALOG_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_CATALOG_UNAVAILABLE))
            return
        if not isinstance(catalog, doxbench_model.ModelCatalog):
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_CATALOG_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_CATALOG_UNAVAILABLE))
            return
        model_entry = catalog.selectable_entry_for(model_id)
        if model_entry is None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_MODEL_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_MODEL_UNAVAILABLE))
            return
        # THE MODEL THAT WILL ACTUALLY ANSWER, resolved through the SAME one
        # function the chat route's wire record and thread sidecar read, so the
        # three cannot drift into three answers. For a plain entry it is the
        # requested id; for an `auto` routing entry it is the model the rule
        # resolves to. Resolved HERE, once, because both consumers below need
        # exactly this value: the STORE KEY and the artifact's recorded
        # provenance are the same three facts, and a route that resolved twice
        # could key by one and record the other.
        resolved_model_id = doxbench_selected_model(
            model_entry)["resolved_model_id"]
        # THE ADAPTER'S OWN DECLARED BOUND, which the region states as the wait
        # it expects. Never `MAX_ADAPTER_TIMEOUT_SECONDS`: that is the validated
        # CEILING, and a region showing 120s while the adapter declared 60s would
        # be lying in the safe direction and still lying.
        try:
            wait_bound = doxbench_model.validated_timeout_seconds(
                port.timeout_seconds)
        except doxbench_model.AdapterTimeoutError:
            wait_bound = None

        # ---- step 9: the assembled request ----
        # `build_abstract_envelope` is the ONE authority for what an abstract
        # request may carry. It is handed the digest this route keyed its store
        # by, and it REFUSES if that is not the digest of the bytes about to be
        # sent -- so the pair the response echoes can never be a false statement
        # about which content was distilled.
        try:
            envelope = doxbench_turns.build_abstract_envelope(
                subject_path, content, model_id=model_id,
                declared_topics=declared_topics,
                declared_destinations=declared_lands,
                declared_digest=digest)
        except doxbench_turns.TurnLimitError:
            self._refuse_abstract(
                DOXBENCH_ABSTRACT_REFUSED_SUBJECT_BYTES,
                _ABSTRACT_REASON_SUBJECT_BYTES,
                subject_path=subject_path, subject_digest=digest,
                wait_bound_seconds=wait_bound)
            return
        except doxbench_turns.AbstractPacketRefusedError:
            # Unreachable by construction -- this route hands the assembler no
            # packet parameter at all -- and mapped anyway, because the one
            # refusal that must never become a dead handler is the one nobody
            # expected. A server-side assembly failure, not a caller's defect.
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE))
            return
        except doxbench_turns.AbstractRequestError:
            # The subject itself: an empty document has nothing to distil, and a
            # declared field that is not one line would forge a header. Both are
            # renderable states of the DOCUMENT, so both are stated refusals
            # rather than errors.
            self._refuse_abstract(
                DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_DISTILLABLE,
                _ABSTRACT_REASON_NOT_DISTILLABLE,
                subject_path=subject_path, subject_digest=digest,
                wait_bound_seconds=wait_bound)
            return
        except doxbench_turns.TurnIdentityMismatchError:
            # The route computed the digest from the very bytes it passed, so a
            # mismatch here is this server contradicting itself. Refuse; never
            # reconcile, and never send a pair that would be a lie.
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE))
            return

        # ---- step 10: the store. It is a PRECONDITION, not an assumption
        # (adversarial review 2026-08-25, N8). `build_server` always binds one
        # and `None` reaches here only from a hand-constructed handler -- which
        # is exactly what `schema_validator_factory` says too, and that seam
        # REFUSES rather than trusting the invariant. Without this leg an absent
        # store was an `AttributeError` on `None` mid-request: the connection
        # dropped with no stated verdict, after the model had been resolved and
        # the subject's bytes read. Fail closed, before any dispatch.
        if self.abstract_store is None:
            self._send_json(
                doxbench_error_status(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE),
                doxbench_error_body(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE))
            return

        # ONE in-flight generation per key, an
        # identical key replayed with no second dispatch, and a changed digest a
        # NEW KEY rather than a conflict (the key is `(scope, path, digest)`). A
        # concurrent request for the same key ATTACHES here rather than
        # dispatching a second time -- which is also the "regenerating" state the
        # renderer shows, so ruling 3(b) needs no machinery of its own.
        #
        # THE WHOLE SCOPE IS IN THE KEY (adversarial review 2026-08-25, S3).
        # `(path, digest)` alone is one question per document only INSIDE one
        # scope, and this handler serves every repository its registry resolves
        # and every ref of each -- so two scopes holding identical bytes at one
        # path shared an entry, and the `previous` base below crossed between
        # them.
        #
        # THE RESOLVED MODEL ID IS IN THE KEY (packet review, Codex on PR #352).
        # This surface lets a human change the selected model while the document
        # stands still, so on a `(scope, path, digest)` key that second request
        # is IDENTICAL by construction: the first model's prose replayed while
        # the artifact recorded the model the reader had just picked, which is
        # an artifact lying about its own provenance. It is the RESOLVED id and
        # never the requested one -- an `auto` routing entry keys on the model
        # that answered, for the same reason a turn records that model.
        #
        # AND THE REQUEST CARRIES AN EXPLICIT REFRESH INTENT. A regeneration
        # against unchanged content and an unchanged model has an identical key
        # by construction, so plain identical-key replay made the RE-GENERATE
        # control the delta requires INERT except by the accident of eviction.
        # `refresh` invalidates the completed entry, dispatches, and replaces
        # it; unset -- every selection, mount and tile re-entry -- it replays as
        # before. The store's one-in-flight arm is unconditional in both modes,
        # so an impatient double-click still spends ONE model call.
        store_key = doxbench_abstract_store.AbstractKey(
            repository=key.repository, ref=key.ref,
            subject_path=subject_path, content_digest=digest,
            resolved_model_id=resolved_model_id)
        lease = self.abstract_store.reserve(store_key, refresh=refresh)
        if not lease.should_dispatch:
            outcome = lease.result
            self._send_json(outcome["status"], outcome["body"])
            return
        # THE ANSWER A REFRESH JUST INVALIDATED, kept as this generation's
        # PREVIOUS verification base. The ratified rule makes a previously
        # generated abstract an ADDITIONAL base "where one exists", and
        # RE-GENERATE is the one path where one always exists -- invalidating it
        # out of the replay index and out of the verifier's reach in the same
        # breath would verify the regenerate path against a strictly weaker base
        # than every other path.
        invalidated_abstract = lease.invalidated_abstract

        answered = False
        try:
            # ---- step 11: THE ABSTRACT'S OWN CONVERSATION, bound AS PART OF
            # the dispatch (adversarial review 2026-08-25, B1; the chat route's
            # own pattern at `_handle_workbench_chat_turn`). `for_conversation`
            # returns a per-turn VIEW, and the adapter binds and prompts inside
            # ONE lock acquisition -- so under this threading server no other
            # handler can move the selection in between.
            #
            # Duck-typed exactly as `dispatch` is: an adapter that offers
            # `for_conversation` binds and prompts atomically, and one that does
            # not is a catalog-only or sessionless adapter and is unchanged. A
            # BINDING FAILURE IS NOT A TURN -- dispatching anyway would ground
            # this distillation in another conversation's session, so it refuses
            # with the same fixed, redacted `model_failed` the chat route uses
            # and nothing is dispatched. The key is released by the `finally`
            # below, so the re-generate control can try again.
            turn_port = port
            if callable(getattr(port, "for_conversation", None)):
                try:
                    turn_port = port.for_conversation(
                        doxbench_abstract_conversation_key(key, subject_path))
                except Exception:  # noqa: BLE001 - never let an adapter's text reach the wire
                    sys.stderr.write(
                        "[actions/workbench/document-abstract] the harness "
                        "bridge could not bind this abstract's own "
                        "conversation; the generation is refused rather than "
                        "prompted inside another conversation's session\n")
                    self._send_json(
                        doxbench_error_status(DOXBENCH_ERR_MODEL_FAILED),
                        doxbench_error_body(DOXBENCH_ERR_MODEL_FAILED))
                    return
                if turn_port is None:
                    # A port that RETURNS None rather than raising is the same
                    # non-binding as an exception -- dispatching would hand
                    # `None` to `_deadline_bound_dispatch`, which reads
                    # `port.timeout_seconds` unconditionally and drops the
                    # connection on an `AttributeError` with no stated
                    # verdict. Refuse the same fixed, redacted `model_failed`
                    # the raising branch above uses; the key is released by
                    # the `finally` below, so the re-generate control can try
                    # again.
                    sys.stderr.write(
                        "[actions/workbench/document-abstract] the harness "
                        "bridge returned no conversation for this abstract; "
                        "the generation is refused rather than dispatched "
                        "with no bound session\n")
                    self._send_json(
                        doxbench_error_status(DOXBENCH_ERR_MODEL_FAILED),
                        doxbench_error_body(DOXBENCH_ERR_MODEL_FAILED))
                    return

            # ---- step 12: dispatch, under the adapter's OWN deadline ----
            # `proposal_validator` is deliberately None: an abstract request is
            # not a conversation and can accept no typed proposal, so a
            # proposal-bearing answer fails closed inside `dispatch_turn`.
            outcome = self._deadline_bound_dispatch(
                turn_port, envelope, model_entry, None)
            if not isinstance(outcome, doxbench_model.TurnDispatchSuccess):
                self._send_json(doxbench_error_status(outcome.error),
                                doxbench_error_body(outcome.error))
                return

            # ---- step 13: the response bound, then VERIFICATION ----
            try:
                prose = doxbench_turns.validate_abstract_prose(
                    outcome.assistant_prose)
            except doxbench_turns.TurnLimitError as over_long:
                self._refuse_abstract(
                    DOXBENCH_ABSTRACT_REFUSED_PROSE_BYTES,
                    _abstract_reason_prose_bytes(over_long.measured,
                                                 over_long.maximum),
                    subject_path=subject_path, subject_digest=digest,
                    wait_bound_seconds=wait_bound)
                return

            # EVERY repository path the request actually carried: the subject's
            # own, plus the paths the subject's OWN SAVED CONTENT names. The
            # verifier refuses an answer naming a path its request did not carry
            # -- which is what refuses the wrong-document and leaked-neighbour
            # answers -- and a document that links to its neighbours would
            # otherwise make every faithful quotation of its own links a
            # refusal. Derived with the verifier's OWN path rule rather than a
            # second one here (`verify_document_abstract`'s docstring names this
            # derivation as the route's job), then filtered to the shapes that
            # module accepts, so a link the rule finds but the validator refuses
            # cannot turn a readable document into a 500.
            #
            # AND INTERSECTED WITH THE READER'S OWN DISCLOSURE SET (adversarial
            # review 2026-08-25, S2). A corpus document is ATTACKER-AUTHORABLE
            # material -- anyone who can land a file writes its bytes -- so an
            # unbounded derivation let a document PRE-AUTHORIZE any name it
            # liked: write `ideation/elsewhere/secret.md` into a subject and an
            # answer naming that document stopped being a leaked neighbour. The
            # carried set is therefore bounded by what this reader may see in
            # this scope, `editable_paths | context_paths` -- the projection's
            # own two sets, computed from server truth. `context_paths` and not
            # `editable_paths` alone, because a link to a READABLE neighbour is
            # a faithful quotation; the ELIGIBILITY rule (ruling 7(a), step 5)
            # is the one that stays `editable_paths`, and this is not that rule.
            # The subject's own path is always carried.
            disclosed = frozenset(projection.editable_paths) | frozenset(
                projection.context_paths)
            carried = [subject_path]
            for candidate in doxbench_knowledge.named_repository_paths(content):
                if (candidate.startswith("/") or "\\" in candidate
                        or any(segment in ("", ".", "..")
                               for segment in candidate.split("/"))):
                    continue
                if candidate not in disclosed:
                    continue
                carried.append(candidate)

            generation = self.abstract_store.next_generation()
            try:
                verdict = doxbench_knowledge.verify_document_abstract(
                    prose,
                    subject_path=subject_path,
                    subject_digest=digest,
                    model_id=resolved_model_id,
                    declared_topics=declared_topics,
                    declared_destinations=declared_lands,
                    request_paths=tuple(carried),
                    subject_title=envelope.subject_title,
                    # The PREVIOUS abstract for this document IN THIS SCOPE AND
                    # UNDER THIS MODEL, under whatever digest it was generated
                    # from: the ratified rule makes it an ADDITIONAL base, never
                    # the only one. On the ORDINARY path it can never be this
                    # key's own -- a cached answer for those exact bytes and
                    # that exact model was replayed above, before any
                    # verification ran -- so what is offered is the answer from
                    # before the last edit, which is precisely the base the rule
                    # is about. On the REFRESH path it IS this key's own,
                    # invalidated moments ago and handed back on the lease
                    # rather than dropped (and the same model by construction,
                    # because the model is in the key).
                    #
                    # NARROWED BY THE RESOLVED MODEL (ruled 2026-08-26,
                    # SHOULD-FIX 6). The base can only TIGHTEN, so offering
                    # another model's answer made a FIRST generation under model
                    # B defend model A's coverage: a reader who switched model
                    # and pressed GENERATE was refused `previous-coverage-
                    # dropped` about an answer this model had never produced,
                    # and every retry met the same live base and the same
                    # refusal. Two models can distil one document differently
                    # without either being wrong, which is exactly what that
                    # reader was choosing between.
                    # `latest_for_path` keeps its model-agnostic form for
                    # the reader-facing "what abstract does this document have
                    # at all"; the VERIFICATION BASE is this narrower question.
                    previous=(invalidated_abstract
                              if invalidated_abstract is not None
                              else self.abstract_store.latest_for_path(
                                  repository=key.repository, ref=key.ref,
                                  subject_path=subject_path,
                                  resolved_model_id=resolved_model_id)),
                    generation=generation)
            except doxbench_knowledge.AbstractFormatRefused:
                self._send_json(
                    doxbench_error_status(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE),
                    doxbench_error_body(DOXBENCH_ERR_ABSTRACT_UNAVAILABLE))
                return
            if isinstance(verdict, doxbench_knowledge.AbstractRefused):
                # A verification failure renders NOTHING, and is never silently
                # downgraded to rendering the unverified text: the refused prose
                # does not leave the verifier, and this body has no field it
                # could ride in. It is also NOT cached -- the `finally` below
                # releases the key -- so the re-generate control can try again
                # against unchanged content.
                self._refuse_abstract(
                    verdict.code, verdict.reason,
                    subject_path=verdict.subject_path, subject_digest=digest,
                    caption_state=verdict.caption_state,
                    wait_bound_seconds=wait_bound)
                return

            body = doxbench_abstract_success_body(
                verdict, wait_bound_seconds=wait_bound)
            try:
                self.abstract_store.complete(
                    store_key, {"status": 200, "body": body},
                    size_bytes=len(json.dumps(body).encode("utf-8")),
                    abstract=verdict)
                answered = True
            except doxbench_abstract_store.AbstractStoreError:
                # Bookkeeping failed; the verdict was still reached and
                # self-consistent, so it is answered. A store-side refusal must
                # never turn a decided answer into a dropped connection.
                pass
            self._send_json(200, body)
        finally:
            if not answered:
                # A refusal is not an answer, so the key goes back to being
                # unknown rather than caching a refusal for these bytes forever.
                self.abstract_store.release(store_key)

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
