"""THREADS, THROUGH THE REAL SERVE (add-doxbench-editing-phase-b tasks 7.2,
9.2, 9.5, 11.4, 11.5).

Everything §10 shipped as a SEAM and honestly marked "route unwired" is wired
here, and this file is where the wiring is proven: the packet carries the
selected document's thread, every answered turn is mirrored back into that
document's sidecar, the sidecar rides its document's Save as ONE commit, and the
thread route serves it to the selector.

WHY A REAL SERVE. Each of these is a WIRING claim — "the route supplies the
threads", "the route writes the record", "the 409 arm is reachable" — and every
one of them passes trivially against a stubbed assembler. The harness is
IMPORTED from `test_doxbench_routes` for the reason that file's own siblings
record: a second harness is a second set of behaviours to keep in step.

THE ONE SEAM THESE TESTS OVERRIDE, and why it is honest to: which directory is
this scope's SESSION WORKTREE (`_session_worktree_for`). Building a live git
session inside the routes harness would test the registry's session bookkeeping,
which `test_session_*` already owns, and would tell us nothing more about the
thread wiring. Everything above that one answer — packet assembly, the budget
arithmetic, the mirror, the gate, the write allowlist, the HTTP envelope — is
the real thing. The SAVE half (task 9.2) is proven separately at the bottom of
this file against a REAL git session, where it belongs.
"""

from __future__ import annotations

import contextlib
import json
import urllib.parse
from pathlib import Path

import pytest

from conftest import BASE_REPO, REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
from ideation_dashboard import doxbench_packet as pk  # noqa: E402
from ideation_dashboard import doxbench_threads as dt  # noqa: E402
from ideation_dashboard import serve as serve_mod  # noqa: E402

from test_doxbench_routes import (  # noqa: E402
    DOC_ALPHA, DOC_ZULU, OUTLINE_PATH, _buf, _capabilities, _catalog,
    _console_headers, _handler_class, _port, _request, _serving,
    _snapshot_with_editable, _turn_v2,
)

CHAT_ROUTE = serve_mod.ACTIONS_WORKBENCH_CHAT_TURN_ROUTE
THREAD_ROUTE = serve_mod.WORKBENCH_THREAD_ROUTE
SCOPE = {"repository": "fixture-repo", "ref": "main",
         "tile_kind": "staged", "tile_id": "ideation-governance"}


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------


def _thread_for(document, *, goal="close the acceptance boundary",
                refs=(), turns=()):
    return dt.DocumentThread(
        document=document,
        scope=dt.ThreadScope(repository="fixture-repo", tile_kind="staged",
                             tile_id="ideation-governance"),
        state=dt.ThreadState(active_goal=goal, evidence_refs=tuple(refs)),
        turns=tuple(turns))


def _seed_sidecar(worktree: Path, thread: dt.DocumentThread) -> Path:
    """Write a sidecar into the worktree the way a previous turn would have —
    through the module's own render, at the module's own path."""
    target = worktree / dt.thread_path_for(thread.document)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dt.render_thread(thread), encoding="utf-8")
    return target


@contextlib.contextmanager
def _thread_serving(tmp_path, *, worktree, port=None, **kwargs):
    """A real serve whose scope has a session worktree."""
    snapshot = kwargs.pop("snapshot", None) or _snapshot_with_editable(
        DOC_ALPHA, DOC_ZULU)
    fake = port if port is not None else _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                  snapshot=snapshot, **kwargs) as (httpd, host, prt):
        handler = _handler_class(httpd)
        handler._session_worktree_for = (          # noqa: SLF001 - the one seam
            lambda self, key, _root=worktree: Path(_root))
        yield httpd, host, prt, fake


def _turn_bound_to(document, *, content="# Alpha\n\nalpha body", **over):
    body = _turn_v2(bound_buffer=document, buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\noutline body"),
        _buf("document", document, content),
    ])
    body.update(over)
    return body


def _post(host, prt, body, path=CHAT_ROUTE):
    caps = _capabilities(host, prt)
    status, payload, _headers, _raw = _request(
        host, prt, "POST", path, body=body, headers=_console_headers(caps))
    return status, payload


def _get(host, prt, path):
    caps = _capabilities(host, prt)
    status, payload, _headers, _raw = _request(
        host, prt, "GET", path, headers={
            "X-XF-Console-Token": caps["console_token"]})
    return status, payload


def _sections(port):
    assert len(port.dispatched) == 1, port.calls
    return {section.key: section.text for section in port.dispatched[0].sections}


# ===========================================================================
# THE READ SIDE — the packet finally carries threads (task 10.3's §11 seam)
# ===========================================================================


def test_the_packet_carries_the_selected_document_s_thread_in_full(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    _seed_sidecar(worktree, _thread_for(DOC_ALPHA, goal="SENTINEL-THREAD-GOAL"))
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, port):
        status, payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200, payload
    sections = _sections(port)
    assert pk.PACKET_SECTION_SELECTED_THREAD in sections
    assert "SENTINEL-THREAD-GOAL" in sections[pk.PACKET_SECTION_SELECTED_THREAD]


def test_another_loaded_document_carries_its_STATE_HEADER_only(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    _seed_sidecar(worktree, _thread_for(DOC_ALPHA, goal="ALPHA-GOAL"))
    _seed_sidecar(worktree, _thread_for(
        DOC_ZULU, goal="ZULU-GOAL",
        turns=[dt.ThreadTurn(turn_id="z1", model="model-a",
                             bound_buffer_key=DOC_ZULU,
                             human="ZULU-TRANSCRIPT-QUESTION",
                             assistant="ZULU-TRANSCRIPT-ANSWER")]))
    body = _turn_v2(bound_buffer=DOC_ALPHA, buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\noutline body"),
        _buf("document", DOC_ALPHA, "# Alpha\n\nalpha body"),
        _buf("document", DOC_ZULU, "# Zulu\n\nzulu body"),
    ])
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, port):
        status, payload = _post(host, prt, body)
    assert status == 200, payload
    sections = _sections(port)
    header = sections[pk.THREAD_STATE_SECTION_PREFIX + DOC_ZULU]
    assert "ZULU-GOAL" in header
    # the OTHER thread's TRANSCRIPT is not carried — the header is, and only it
    assert "ZULU-TRANSCRIPT-ANSWER" not in json.dumps(sections)


def test_a_loaded_document_with_no_sidecar_is_DECLARED_absent(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, port):
        status, _payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200
    declaration = _sections(port)[pk.PACKET_SECTION_DECLARATION]
    assert "no thread exists yet for:" in declaration
    assert DOC_ALPHA in declaration


def test_an_unreadable_sidecar_is_absent_rather_than_half_parsed(tmp_path):
    """An invented or half-parsed thread would be a claim that a conversation
    happened, so a sidecar that is not one reads exactly like no sidecar."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    target = worktree / dt.thread_path_for(DOC_ALPHA)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("this is not a thread file", encoding="utf-8")
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, port):
        status, _payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200
    declaration = _sections(port)[pk.PACKET_SECTION_DECLARATION]
    assert "no thread exists yet for:" in declaration


# ===========================================================================
# SIGNAL_THREAD_STATE FINALLY FIRES (the third declared retrieval signal)
# ===========================================================================


def test_the_thread_state_retrieval_signal_fires_on_a_route_assembled_packet(
        tmp_path, monkeypatch):
    """The local-hybrid profile DECLARES three retrieval signals and the shipped
    serve produced only two: threads were always `{}` at the route, so the
    thread-state signal could never fire on anything but a unit test. Spied at
    the BACKEND, with the whole real route above it, so what is asserted is that
    the signal reaches the provider — not that a helper computes one."""

    assert kn.SIGNAL_THREAD_STATE in kn.LOCAL_EMBEDDED_PROFILE.signals
    seen = {}
    original = kn.LocalHybridBackend.retrieve

    def _spy(self, query, *, confined_to, limit, thread_signals=frozenset()):
        seen["thread_signals"] = frozenset(thread_signals)
        return original(self, query, confined_to=confined_to, limit=limit,
                        thread_signals=thread_signals)

    monkeypatch.setattr(kn.LocalHybridBackend, "retrieve", _spy)

    worktree = tmp_path / "worktree"
    worktree.mkdir()
    _seed_sidecar(worktree, _thread_for(
        DOC_ALPHA, refs=("ideation/brainstorm/dtn-register.md",)))
    with _thread_serving(tmp_path, worktree=worktree,
                         knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                         ) as (_httpd, host, prt, _port):
        status, payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200, payload
    assert seen["thread_signals"] == frozenset(
        {"ideation/brainstorm/dtn-register.md"}), seen


def test_with_no_thread_the_signal_is_empty_rather_than_invented(tmp_path,
                                                                 monkeypatch):
    seen = {}
    original = kn.LocalHybridBackend.retrieve

    def _spy(self, query, *, confined_to, limit, thread_signals=frozenset()):
        seen["thread_signals"] = frozenset(thread_signals)
        return original(self, query, confined_to=confined_to, limit=limit,
                        thread_signals=thread_signals)

    monkeypatch.setattr(kn.LocalHybridBackend, "retrieve", _spy)
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree,
                         knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                         ) as (_httpd, host, prt, _port):
        assert _post(host, prt, _turn_bound_to(DOC_ALPHA))[0] == 200
    assert seen["thread_signals"] == frozenset()


# ===========================================================================
# THE 409 ARM, REACHABLE AT THE ROUTE (no injected assembler)
# ===========================================================================


def test_threads_alone_over_the_budget_refuse_at_the_REAL_route(tmp_path):
    """The bounds rail's refusal arm, driven end to end through the shipped
    assembler for the first time.

    Until this slice the route supplied NO threads, so the only thing that could
    exceed the packet's bound was evidence — which the fit selects away rather
    than refusing — and the 409 could be reached only by injecting an assembler
    that put a thread in. Now the route reads the session's own sidecar, so a
    thread bigger than what the model's declared ceiling leaves is refused with
    the measured dimension named, and the refusal is actionable: compaction is
    layer two and it exists for exactly this."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    _seed_sidecar(worktree, _thread_for(
        DOC_ALPHA,
        turns=[dt.ThreadTurn(turn_id=f"t{n}", model="model-a",
                             bound_buffer_key=DOC_ALPHA,
                             human="q" * 400, assistant="a" * 400)
               for n in range(40)]))
    narrow = _port(_catalog(input_limit_bytes=48_000))
    with _thread_serving(tmp_path, worktree=worktree,
                         port=narrow) as (_httpd, host, prt, port):
        status, payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 409, payload
    assert payload["error"] == serve_mod.DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED
    assert payload["limit"]["dimension"] == "context_packet_bytes"
    assert port.calls.count("dispatch") == 0
    # the refusal names a bound, never the thread's content
    assert "q" * 400 not in json.dumps(payload)


def test_the_same_thread_inside_a_generous_ceiling_still_answers(tmp_path):
    """The 409's own control: the refusal is about the BOUND, not about threads
    being present, so the identical sidecar under a wide ceiling is a 200."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    _seed_sidecar(worktree, _thread_for(
        DOC_ALPHA,
        turns=[dt.ThreadTurn(turn_id=f"t{n}", model="model-a",
                             bound_buffer_key=DOC_ALPHA,
                             human="q" * 400, assistant="a" * 400)
               for n in range(40)]))
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200, payload


# ===========================================================================
# THE WRITE SIDE — every turn is mirrored into the sidecar (tasks 9.2, 11.5)
# ===========================================================================


def _commit_paths(worktree, revision):
    """The paths one commit carries, read from real git."""
    import subprocess
    out = subprocess.run(
        ["git", "-C", str(worktree), "show", "--name-only",
         "--pretty=format:", revision],
        check=True, capture_output=True, text=True).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def _read_sidecar(worktree, document):
    target = worktree / dt.thread_path_for(document)
    return dt.parse_thread(target.read_text(encoding="utf-8"))


def test_an_answered_turn_is_mirrored_into_the_selected_document_s_sidecar(
        tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200, payload
    thread = _read_sidecar(worktree, DOC_ALPHA)
    assert len(thread.turns) == 1
    turn = thread.turns[0]
    assert turn.bound_buffer_key == DOC_ALPHA
    assert turn.model == "model-a"
    assert turn.assistant == "fake grounded answer"
    # the RECORD is non-authoritative and says so in the file
    assert thread.authority == dt.NON_AUTHORITATIVE
    assert thread.regenerable_from == dt.REGENERABLE_FROM_TRANSCRIPT


def test_a_second_turn_appends_rather_than_replacing(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        assert _post(host, prt, _turn_bound_to(DOC_ALPHA))[0] == 200
        assert _post(host, prt, _turn_bound_to(
            DOC_ALPHA, client_turn_id="turn-v2-0002",
            message="a second question entirely"))[0] == 200
    thread = _read_sidecar(worktree, DOC_ALPHA)
    assert len(thread.turns) == 2
    assert thread.turns[0].turn_id != thread.turns[1].turn_id


def test_the_sidecar_is_LF_only_even_when_the_wire_carried_CRLF(tmp_path):
    """The sidecar format refuses a carriage return absolutely, and the wire
    carries whatever a browser and a provider produced — so the mirror
    normalises at the one place a turn becomes a record."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    class _CrlfPort:
        timeout_seconds = 30.0
        calls: list = []
        dispatched: list = []

        def __init__(self):
            self.calls = []
            self.dispatched = []

        def catalog(self):
            self.calls.append("catalog")
            return _catalog()

        def dispatch(self, prompt_envelope):
            self.calls.append("dispatch")
            self.dispatched.append(prompt_envelope)
            return {"assistant_prose": "line one\r\nline two\r\n",
                    "proposals": []}

    with _thread_serving(tmp_path, worktree=worktree,
                         port=_CrlfPort()) as (_httpd, host, prt, _p):
        status, payload = _post(host, prt, _turn_bound_to(
            DOC_ALPHA, message="a question\r\nwith a carriage return"))
    assert status == 200, payload
    raw = (worktree / dt.thread_path_for(DOC_ALPHA)).read_text(encoding="utf-8")
    assert "\r" not in raw
    thread = dt.parse_thread(raw)
    assert thread.turns[0].assistant == "line one\nline two"


def test_an_OUTLINE_bound_turn_writes_no_thread(tmp_path):
    """A thread belongs to a DOCUMENT. The outline buffer is the tile's, not a
    document's, so a turn bound to it records no sidecar rather than inventing
    one for a path no document owns."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload = _post(host, prt, _turn_v2(bound_buffer="outline"))
    assert status == 200, payload
    assert not (worktree / dt.THREAD_PREFIX).exists()


def test_a_record_that_cannot_be_written_never_changes_the_wire_outcome(
        tmp_path):
    """THE JUDGEMENT CALL, PINNED. The provider has already answered by the time
    the record is written and there is no released refusal code for "the record
    could not be written", so the answer still ships and the failure goes to the
    serve's own log. What must NOT happen is a dropped connection, a changed
    status, or a diagnostic on the wire."""
    # A worktree that is a FILE: every write under it fails, which is the
    # cheapest real "the record could not be written" this route can be handed.
    unwritable = tmp_path / "not-a-worktree"
    unwritable.write_text("this is a file, not a worktree", encoding="utf-8")
    with _thread_serving(tmp_path, worktree=unwritable) as (_httpd, host, prt, _p):
        status, payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200, payload
    assert payload["kind"] == "workbench-chat-turn-v2-success"
    assert unwritable.is_file()
    assert unwritable.read_text(encoding="utf-8").startswith("this is a file")


def test_a_body_still_carrying_a_harness_pointer_is_refused_not_persisted(
        tmp_path):
    """Task 3.5's fail-closed half at the route: a serve with NO bridge supplies
    a dereference seam that resolves nothing, so an `artifact://` body is
    refused by `ThreadTurn` and the sidecar records nothing rather than an
    unresolvable pointer. The turn itself still answers."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    class _PointerPort:
        timeout_seconds = 30.0

        def __init__(self):
            self.calls = []
            self.dispatched = []

        def catalog(self):
            self.calls.append("catalog")
            return _catalog()

        def dispatch(self, prompt_envelope):
            self.calls.append("dispatch")
            self.dispatched.append(prompt_envelope)
            return {"assistant_prose": "see artifact://spilled-blob",
                    "proposals": []}

    with _thread_serving(tmp_path, worktree=worktree,
                         port=_PointerPort()) as (_httpd, host, prt, _p):
        status, _payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == 200
    assert not (worktree / dt.thread_path_for(DOC_ALPHA)).exists()


# ===========================================================================
# ONE HARNESS SESSION PER DOCUMENT THREAD, AT THE ROUTE (task 11.4 / 7.2)
# ===========================================================================


def test_the_route_binds_the_selected_document_s_thread_before_dispatching(
        tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    class _BindingPort:
        timeout_seconds = 30.0

        def __init__(self):
            self.calls = []
            self.dispatched = []
            self.bound = []

        def catalog(self):
            self.calls.append("catalog")
            return _catalog()

        def select_thread(self, key):
            self.calls.append("select_thread")
            self.bound.append(key)

        def dispatch(self, prompt_envelope):
            self.calls.append("dispatch")
            self.dispatched.append(prompt_envelope)
            return {"assistant_prose": "bound", "proposals": []}

    port = _BindingPort()
    with _thread_serving(tmp_path, worktree=worktree,
                         port=port) as (_httpd, host, prt, _p):
        assert _post(host, prt, _turn_bound_to(DOC_ALPHA))[0] == 200
    assert port.bound == [DOC_ALPHA]
    assert port.calls.index("select_thread") < port.calls.index("dispatch")


def test_an_OUTLINE_turn_binds_its_tiles_own_conversation_not_a_document(
        tmp_path):
    """P2-11. The bind used to be gated on `bound_buffer_key in document_keys`,
    so an outline turn never bound at all and was dispatched into whichever
    DOCUMENT session the harness was last switched to — contaminating that
    document's harness context, which is the second store design §5.2 keeps
    apart. Every turn binds now, and an outline turn binds under its tile."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    class _BindingPort:
        timeout_seconds = 30.0

        def __init__(self):
            self.calls = []
            self.dispatched = []
            self.bound = []

        def catalog(self):
            return _catalog()

        @staticmethod
        def outline_conversation_key(tile_kind, tile_id):
            from ideation_dashboard import doxbench_bridge as br
            return br.OmpHarnessBridge.outline_conversation_key(
                tile_kind, tile_id)

        def select_thread(self, key):
            self.bound.append(key)

        def dispatch(self, prompt_envelope):
            self.calls.append("dispatch")
            self.dispatched.append(prompt_envelope)
            return {"assistant_prose": "outline answer", "proposals": []}

    port = _BindingPort()
    # A document turn first, so the harness is left bound to a DOCUMENT — the
    # precondition that made the leak reachable.
    with _thread_serving(tmp_path, worktree=worktree,
                         port=port) as (_httpd, host, prt, _p):
        assert _post(host, prt, _turn_bound_to(DOC_ALPHA))[0] == 200
        assert _post(host, prt, dict(_turn_v2(bound_buffer="outline"),
                                     client_turn_id="turn-outline"))[0] == 200
    assert port.bound[0] == DOC_ALPHA
    assert port.bound[1] == "outline::staged/ideation-governance"
    assert port.bound[1] != DOC_ALPHA
    # …and the OUTLINE turn wrote no sidecar of its own: a thread belongs to a
    # DOCUMENT (judgement call 15 — true of the sidecar, and now true of the
    # harness session too). The only sidecar is the document turn's.
    written = sorted(str(path.relative_to(worktree))
                     for path in (worktree / dt.THREAD_PREFIX).rglob("*")
                     if path.is_file())
    assert written == [dt.thread_path_for(DOC_ALPHA)], written


def test_a_bridge_that_cannot_bind_the_thread_refuses_rather_than_grounding_it_elsewhere(
        tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    class _RefusingPort:
        timeout_seconds = 30.0

        def __init__(self):
            self.calls = []
            self.dispatched = []

        def catalog(self):
            self.calls.append("catalog")
            return _catalog()

        def select_thread(self, key):
            raise RuntimeError("SECRET-BRIDGE-DIAGNOSTIC")

        def dispatch(self, prompt_envelope):
            self.calls.append("dispatch")
            self.dispatched.append(prompt_envelope)
            return {"assistant_prose": "should never happen", "proposals": []}

    port = _RefusingPort()
    with _thread_serving(tmp_path, worktree=worktree,
                         port=port) as (_httpd, host, prt, _p):
        status, payload = _post(host, prt, _turn_bound_to(DOC_ALPHA))
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_MODEL_FAILED)
    assert payload["error"] == serve_mod.DOXBENCH_ERR_MODEL_FAILED
    assert "SECRET-BRIDGE-DIAGNOSTIC" not in json.dumps(payload)
    assert port.calls.count("dispatch") == 0


# ===========================================================================
# THE THREAD ROUTE (task 9.5)
# ===========================================================================


def _thread_query(document, **over):
    fields = dict(SCOPE, document=document)
    fields.update(over)
    return THREAD_ROUTE + "?" + urllib.parse.urlencode(fields)


def test_the_thread_route_answers_the_document_s_own_turns(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    _seed_sidecar(worktree, _thread_for(
        DOC_ALPHA, goal="ROUTE-GOAL",
        turns=[dt.ThreadTurn(turn_id="t1", model="model-a",
                             bound_buffer_key=DOC_ALPHA,
                             human="what next?", assistant="this next")]))
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload = _get(host, prt, _thread_query(DOC_ALPHA))
    assert status == 200, payload
    assert payload["present"] is True
    assert payload["turns"] == [{"turn_id": "t1", "model": "model-a",
                                 "bound_buffer_key": DOC_ALPHA,
                                 "human": "what next?",
                                 "assistant": "this next"}]
    assert "ROUTE-GOAL" in payload["state_header"]
    assert payload["authority"] == dt.NON_AUTHORITATIVE


def test_a_document_with_no_thread_answers_an_HONEST_empty_one(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload = _get(host, prt, _thread_query(DOC_ALPHA))
    assert status == 200
    assert payload["present"] is False
    assert payload["turns"] == []


def test_the_thread_route_is_absent_without_the_gate_capability(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (httpd, host, prt, _p):
        handler = _handler_class(httpd)
        caps = json.loads(json.dumps(handler.capabilities))
        caps["actions"]["session"] = False
        handler.capabilities = caps
        status, payload, _h, _r = _request(host, prt, "GET",
                                           _thread_query(DOC_ALPHA))
    assert status == 403
    assert payload["error"] == serve_mod.DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE
    assert dt.NO_GATE_CAPABILITY_CAUSE in payload["cause"]
    assert payload["reason"] == dt.THREAD_CAPABILITY_ABSENT_REASON


def test_the_thread_route_fails_closed_on_an_unresolved_actor(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (httpd, host, prt, _p):
        _handler_class(httpd).actor = None
        status, payload, _h, _r = _request(host, prt, "GET",
                                           _thread_query(DOC_ALPHA))
    assert status == 403
    assert payload["error"] == serve_mod.DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE


def test_the_thread_route_is_absent_on_the_hosted_plane(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (httpd, host, prt, _p):
        _handler_class(httpd).loopback = False
        status, payload, _h, _r = _request(host, prt, "GET",
                                           _thread_query(DOC_ALPHA))
    assert status == 403
    assert dt.HOSTED_PLANE_CAUSE in payload["cause"]


def test_a_scope_with_no_live_session_gets_its_OWN_cause(tmp_path):
    """P3-19. This branch used to answer the no-gate-capability cause — a true
    sentence about a DIFFERENT situation, since the plane has the capability
    here and the scope simply has no open session. The cause stays generic, so
    the route is still no oracle for which refs or tiles exist."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (httpd, host, prt, _p):
        _handler_class(httpd)._session_worktree_for = (   # noqa: SLF001
            lambda self, key: None)
        status, payload = _get(host, prt, _thread_query(DOC_ALPHA))
    assert status == 403
    assert payload["error"] == serve_mod.DOXBENCH_ERR_THREAD_CAPABILITY_UNAVAILABLE
    assert payload["cause"] == serve_mod.NO_LIVE_SESSION_CAUSE
    assert payload["cause"] != dt.NO_GATE_CAPABILITY_CAUSE
    # no oracle: neither the ref nor the tile id is echoed
    assert "ideation-governance" not in json.dumps(payload)
    assert DOC_ALPHA not in json.dumps(payload)


def test_the_thread_route_refuses_a_non_console_caller(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload, _h, _r = _request(host, prt, "GET",
                                           _thread_query(DOC_ALPHA))
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert payload["error"] == serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED


def test_the_thread_route_refuses_an_incomplete_query(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload = _get(host, prt, THREAD_ROUTE + "?document=x")
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST)


def test_the_thread_route_cannot_read_outside_the_worktree(tmp_path):
    outside = tmp_path / "outside.md"
    outside.write_text("not yours", encoding="utf-8")
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        status, payload = _get(host, prt, _thread_query("../outside.md"))
    assert status == 200
    assert payload["present"] is False


def test_the_thread_route_writes_nothing(tmp_path):
    """A thread is written by a TURN, through the Save gate. This route is a
    read, and there is no second write route anywhere near it."""
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    before = sorted(p.name for p in tmp_path.rglob("*"))
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        _get(host, prt, _thread_query(DOC_ALPHA))
    assert not (worktree / dt.THREAD_PREFIX).exists()
    assert "POST" not in serve_mod.WORKBENCH_THREAD_ROUTE
    del before


def test_the_thread_route_is_not_a_POST_surface(tmp_path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    with _thread_serving(tmp_path, worktree=worktree) as (_httpd, host, prt, _p):
        caps = _capabilities(host, prt)
        status, payload, _h, _r = _request(
            host, prt, "POST", THREAD_ROUTE, body={},
            headers=_console_headers(caps))
    assert status != 200
    assert payload is None or payload.get("error") != "ok"


# ===========================================================================
# NOTHING PUSHES IMPLICITLY (§12's negative, asserted where the writes are)
# ===========================================================================


def test_no_thread_write_path_reaches_a_push(tmp_path):
    """A turn writes a record and a Save commits it; neither may push, and
    nothing scheduled may either. Asserted against the SOURCE of every place
    this slice touched, because an absence nobody checks is an absence that
    grows a helper."""
    for module in ("serve.py", "doxbench_threads.py", "doxbench_bridge.py",
                   "doxbench_mcp.py"):
        source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                  / module).read_text(encoding="utf-8")
        for forbidden in (".push(", "open_or_update(", "git push"):
            assert forbidden not in source, (module, forbidden)


# ===========================================================================
# THE SCAFFOLD RESERVE (task 11.5, re-measured against the thread shape)
# ===========================================================================


def test_the_reserve_defaults_reproduce_the_pre_slice_number():
    assert pk.packet_scaffold_reserve() == pk.PROMPT_SCAFFOLD_RESERVE_BYTES
    assert pk.packet_budget_for(input_limit_bytes=1_000, request_bytes=900) == 0


def test_the_reserve_grows_with_the_shape_the_turn_will_render():
    one = pk.packet_scaffold_reserve(thread_refs=("a" * 40,))
    two = pk.packet_scaffold_reserve(thread_refs=("a" * 40, "b" * 40))
    assert two - one == pk.PER_SOURCE_SCAFFOLD_BYTES + pk.REF_RENDERINGS * 40
    slots = pk.packet_scaffold_reserve(evidence_slots=6)
    assert slots - pk.PROMPT_SCAFFOLD_RESERVE_BYTES == 6 * (
        pk.PER_SOURCE_SCAFFOLD_BYTES
        + pk.REF_RENDERINGS * pk.OBSERVED_REF_BYTES)


def test_the_reserve_covers_the_two_shapes_the_obligation_MEASURED():
    """§11.5's own numbers: 24 thread-state sections plus 6 evidence refs at
    120 characters spent 19,745 bytes of uncounted overhead, and the packet's
    own 48-source bound spent 31,211. Both must now be COVERED."""
    thirty = pk.packet_scaffold_reserve(
        thread_refs=tuple("x" * 120 for _ in range(24)), evidence_slots=6)
    assert thirty - pk.PROMPT_SCAFFOLD_RESERVE_BYTES >= 19_745
    full = pk.packet_scaffold_reserve(
        thread_refs=tuple("x" * 120 for _ in range(pk.MAX_PACKET_SOURCES)))
    assert full - pk.PROMPT_SCAFFOLD_RESERVE_BYTES >= 31_211


def test_the_widest_labels_are_the_ones_the_renderer_actually_produces():
    """The per-source constant is derived from the WIDEST label each slot can
    take; a wider one would make the reserve too small, so each is pinned
    against the helper that produces it."""
    source = pk.PacketSource(ref="r", kind=pk.SOURCE_EVIDENCE, text="",
                             status=None, compression_exempt=True)
    assert pk._status_label(source) == pk.WIDEST_STATUS_LABEL
    assert pk._exemption_label(source) == pk.WIDEST_EXEMPTION_LABEL
    assert pk.WIDEST_KIND_LABEL in pk.SOURCE_KINDS
    assert all(len(kind) <= len(pk.WIDEST_KIND_LABEL) for kind in pk.SOURCE_KINDS)


def test_the_rendered_prompt_stays_inside_the_ceiling_WITH_threads(tmp_path):
    """THE RE-MEASUREMENT §11.5's obligation asks for, at the route: render a
    real turn at a narrowed catalog ceiling with a thread mirrored and evidence
    carried, sum `utf8_size(section.text)` across the assembled envelope, and
    compare it to the entry's effective input limit.

    The pre-slice flat reserve is what this would have caught: it charged
    nothing for the thread sections, so a turn near its ceiling was accepted and
    then dispatched a prompt over it."""
    from ideation_dashboard.doxbench_hash import utf8_size

    worktree = tmp_path / "worktree"
    worktree.mkdir()
    _seed_sidecar(worktree, _thread_for(
        DOC_ALPHA,
        turns=[dt.ThreadTurn(turn_id=f"t{n}", model="model-a",
                             bound_buffer_key=DOC_ALPHA,
                             human="q" * 200, assistant="a" * 200)
               for n in range(5)]))
    _seed_sidecar(worktree, _thread_for(DOC_ZULU, goal="z" * 200))
    body = _turn_v2(bound_buffer=DOC_ALPHA, buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\noutline body"),
        _buf("document", DOC_ALPHA, "# Alpha\n\nalpha body"),
        _buf("document", DOC_ZULU, "# Zulu\n\nzulu body"),
    ])
    for ceiling in (60_000, 120_000, 400_000):
        narrow = _port(_catalog(input_limit_bytes=ceiling))
        with _thread_serving(tmp_path, worktree=worktree, port=narrow,
                             knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                             ) as (_httpd, host, prt, port):
            status, payload = _post(host, prt, dict(
                body, client_turn_id=f"turn-ceiling-{ceiling}"))
        assert status == 200, (ceiling, payload)
        envelope = port.dispatched[0]
        rendered = sum(utf8_size(section.text) for section in envelope.sections)
        assert rendered <= ceiling, (ceiling, rendered)
        # and the thread really is in there, or this measures nothing
        assert any(section.key == pk.PACKET_SECTION_SELECTED_THREAD
                   for section in envelope.sections), ceiling


def test_the_FLAT_reserve_really_was_too_small_for_the_shape_this_slice_makes(
        tmp_path):
    """THE OBLIGATION'S OWN SHAPE, MEASURED THROUGH THE REAL ROUTE: 24 loaded
    documents, each with a thread, plus the evidence slots a turn reserves.

    What is measured is the SCAFFOLDING — the rendered prompt minus the packet's
    own source bytes and minus the request bytes the route already measured —
    which is exactly what the reserve exists to cover. Two things are asserted,
    and the pair is the whole §11.5 argument:

      * the scaffolding this shape really spends EXCEEDS the flat 16,384 the
        pre-slice reserve subtracted, so the old arithmetic would have accepted
        a turn at its ceiling and then dispatched a prompt past it;
      * it fits inside the reserve the route now computes from the turn's own
        refs, so the new arithmetic covers what it charges for."""
    from ideation_dashboard.doxbench_hash import utf8_size

    worktree = tmp_path / "worktree"
    worktree.mkdir()
    documents = [f"ideation/staging/ideation-governance/loaded-{n:02d}.md"
                 for n in range(24)]
    for document in documents:
        _seed_sidecar(worktree, _thread_for(document, goal="g" * 40))
    buffers = [_buf("outline", OUTLINE_PATH, "# Outline\n\noutline body")]
    buffers += [_buf("document", document, f"# Doc {n}\n\nbody {n}")
                for n, document in enumerate(documents)]
    body = _turn_v2(bound_buffer=documents[0], buffers=buffers)
    wide = _port(_catalog(input_limit_bytes=1_000_000))
    with _thread_serving(tmp_path, worktree=worktree, port=wide,
                         snapshot=_snapshot_with_editable(*documents),
                         knowledge_declaration=kn.SELF_HOSTED_LOCAL_EMBEDDED
                         ) as (_httpd, host, prt, port):
        status, payload = _post(host, prt, body)
    assert status == 200, payload
    envelope = port.dispatched[0]
    rendered = sum(utf8_size(section.text) for section in envelope.sections)
    request_bytes = sum(utf8_size(buffer["content"]) for buffer in buffers)
    request_bytes += utf8_size(body["message"])
    request_bytes += utf8_size(body["working_subject"])
    packet_sections = [
        section for section in envelope.sections
        if section.key == pk.PACKET_SECTION_SELECTED_THREAD
        or section.key.startswith(pk.THREAD_STATE_SECTION_PREFIX)
        or section.key.startswith(pk.EVIDENCE_SECTION_PREFIX)]
    assert len(packet_sections) >= 24, len(packet_sections)
    # what the packet's OWN bound already accounts for
    carried_bytes = utf8_size(dt.render_thread(
        _thread_for(documents[0], goal="g" * 40)))
    carried_bytes += sum(
        utf8_size(dt.render_state_header(_thread_for(document, goal="g" * 40)))
        for document in documents[1:])
    scaffolding = rendered - request_bytes - carried_bytes
    assert scaffolding > pk.PROMPT_SCAFFOLD_RESERVE_BYTES, (
        "this shape no longer breaches the flat reserve, so the measurement "
        f"proves nothing: {scaffolding}")
    charged = pk.packet_scaffold_reserve(
        thread_refs=tuple(documents),
        evidence_slots=pk.DEFAULT_EVIDENCE_LIMIT)
    assert scaffolding <= charged, (scaffolding, charged)


# ===========================================================================
# THE SAVE COMMITS THE THREAD WITH ITS DOCUMENT (task 9.2) — REAL git
# ===========================================================================


def test_a_dirty_sidecar_rides_its_document_s_Save_as_ONE_commit(scratch_repo):
    """Task 9.2, against a REAL git session: `commit_gate_action` is untouched,
    and the thread joins the DECLARED path set the Save already commits — so a
    thread and the document text it discusses cannot land in separate commits.
    """
    from ideation_dashboard import branch_session as bs
    from ideation_dashboard import gate_routes as gr
    from ideation_dashboard import session_git as sg
    from ideation_dashboard import snapshot_registry as reg
    from ideation_dashboard.generator import generate_snapshot
    from session_fixtures import GATE_RECORDS_PREFIX

    repo = scratch_repo
    snapshot_path = repo.root.parent / "main-snapshot.json"
    snapshot_path.write_text(
        json.dumps(generate_snapshot(repo.root, repo.repository)),
        encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        snapshot_path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    git = sg.SessionGit(repo.root)
    tile = bs.Tile(bs.STAGED_TOPIC, repo.topic_id)
    document = f"ideation/staging/{repo.topic_id}/detail.md"

    first = gr.execute_first_edit(
        git=git, session_registry=registry, repository=repo.repository,
        tile=tile, document=document, content="# Detail\n\nfirst\n",
        actor="brett", checkout_root=repo.root,
        records_dir=GATE_RECORDS_PREFIX, at="2026-08-19T09:00:00Z")
    worktree = Path(registry.resolve(repo.repository, first["ref"]).source_root)

    # A turn happened: the sidecar is written through the SAME gate the Save
    # builds, which is the only gate on this surface whose allowlist carries the
    # thread prefix.
    gate = gr.first_edit_gate_factory("brett", GATE_RECORDS_PREFIX)(worktree)
    thread = dt.DocumentThread(
        document=document,
        scope=dt.ThreadScope(repository=repo.repository, tile_kind="staged",
                             tile_id=repo.topic_id),
        turns=(dt.ThreadTurn(turn_id="t1", model="model-a",
                             bound_buffer_key=document,
                             human="what next?", assistant="this next"),))
    dt.write_thread(gate, thread)
    sidecar = dt.thread_path_for(document)
    assert sidecar in set(git.dirty_paths(worktree))

    from ideation_dashboard import doxbench_hash as dh
    second = gr.execute_first_edit(
        git=git, session_registry=registry, repository=repo.repository,
        tile=tile, document=document, content="# Detail\n\nsecond\n",
        actor="brett", checkout_root=repo.root,
        base_hash=dh.content_identity("# Detail\n\nfirst\n").hex,
        records_dir=GATE_RECORDS_PREFIX, at="2026-08-19T09:05:00Z")

    landed = _commit_paths(worktree, second["commit"])
    assert document in landed
    assert sidecar in landed, landed
    # ONE commit, not two: the record, the document and the thread together
    assert second["commit"] != first["commit"]
    assert sidecar not in set(git.dirty_paths(worktree))


def test_a_Save_with_no_thread_written_commits_exactly_what_it_always_did(
        scratch_repo):
    """The seam is inert where no turn has written a sidecar: declaring a path
    that is not dirty would refuse every Save on a tile whose thread had not
    moved, so the filter is load-bearing rather than an optimisation."""
    from ideation_dashboard import branch_session as bs
    from ideation_dashboard import gate_routes as gr
    from ideation_dashboard import session_git as sg
    from ideation_dashboard import snapshot_registry as reg
    from ideation_dashboard.generator import generate_snapshot
    from session_fixtures import GATE_RECORDS_PREFIX

    repo = scratch_repo
    snapshot_path = repo.root.parent / "main-snapshot.json"
    snapshot_path.write_text(
        json.dumps(generate_snapshot(repo.root, repo.repository)),
        encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        snapshot_path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    git = sg.SessionGit(repo.root)
    tile = bs.Tile(bs.STAGED_TOPIC, repo.topic_id)
    document = f"ideation/staging/{repo.topic_id}/detail.md"

    first = gr.execute_first_edit(
        git=git, session_registry=registry, repository=repo.repository,
        tile=tile, document=document, content="# Detail\n\nfirst\n",
        actor="brett", checkout_root=repo.root,
        records_dir=GATE_RECORDS_PREFIX, at="2026-08-19T09:00:00Z")
    worktree = Path(registry.resolve(repo.repository, first["ref"]).source_root)
    landed = _commit_paths(worktree, first["commit"])
    assert document in landed
    assert not any(path.startswith(dt.THREAD_PREFIX) for path in landed), landed


# ===========================================================================
# THE REAL `_session_worktree_for` (P2-10) — the one method no test executed
# ===========================================================================


class _RegistryOnly(serve_mod.DashboardHandler):
    """A handler that is NOTHING but its registry.

    Subclassed rather than duck-typed so the method under test is the REAL one
    with its REAL collaborators — `__init__` is bypassed because a
    `BaseHTTPRequestHandler` constructor serves a request, and this test is
    about one method's own logic."""

    def __init__(self, registry):          # noqa: D107 - deliberately no super()
        self.source = type("S", (), {"registry": registry})()


def _real_worktree_for(registry, key):
    return _RegistryOnly(registry)._session_worktree_for(key)


def _open_a_real_session(repo):
    from ideation_dashboard import branch_session as bs
    from ideation_dashboard import gate_routes as gr
    from ideation_dashboard import session_git as sg
    from ideation_dashboard import snapshot_registry as reg
    from ideation_dashboard.generator import generate_snapshot
    from session_fixtures import GATE_RECORDS_PREFIX

    snapshot_path = repo.root.parent / "main-snapshot.json"
    snapshot_path.write_text(
        json.dumps(generate_snapshot(repo.root, repo.repository)),
        encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        snapshot_path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    outcome = gr.execute_first_edit(
        git=sg.SessionGit(repo.root), session_registry=registry,
        repository=repo.repository, tile=bs.Tile(bs.STAGED_TOPIC, repo.topic_id),
        document=f"ideation/staging/{repo.topic_id}/detail.md",
        content="# Detail\n\nfirst\n", actor="brett",
        checkout_root=repo.root, records_dir=GATE_RECORDS_PREFIX,
        at="2026-08-19T09:00:00Z")
    return registry, outcome["ref"]


def test_the_REAL_session_worktree_method_finds_a_live_session(scratch_repo):
    """P2-10. Every route test overrides this method, so nothing executed its
    body — and its body gated on two fields `snapshot_registry` documents as
    ADVISORY and "never the reason a session fails". It now asks the liveness
    authority the Save path itself trusts, and this drives the real thing
    against a real git session."""
    from ideation_dashboard.doxbench_scope import ScopeKey

    registry, ref = _open_a_real_session(scratch_repo)
    key = ScopeKey(repository=scratch_repo.repository, ref=ref,
                   tile_kind="staged", tile_id=scratch_repo.topic_id)
    worktree = _real_worktree_for(registry, key)
    assert worktree is not None, "a live session must have a thread worktree"
    assert Path(worktree).is_dir()
    assert Path(worktree) == Path(
        registry.resolve(scratch_repo.repository, ref).source_root)


def test_the_ADVISORY_markers_are_no_longer_the_predicate(scratch_repo):
    """The regression this fix exists for: a bootstrap-reconstructed entry
    carries neither `session_tile` nor `session_base`, and the old predicate
    silently lost every record on it. Liveness is unchanged by clearing them."""
    from ideation_dashboard.doxbench_scope import ScopeKey

    registry, ref = _open_a_real_session(scratch_repo)
    entry = registry.resolve(scratch_repo.repository, ref)
    entry.session_tile = None
    entry.session_base = None
    entry.session_base_aliases = ()
    key = ScopeKey(repository=scratch_repo.repository, ref=ref,
                   tile_kind="staged", tile_id=scratch_repo.topic_id)
    assert _real_worktree_for(registry, key) is not None, (
        "a bootstrap-reconstructed session still holds threads")


def test_the_liveness_question_has_ONE_spelling_and_it_normalises_refs(
        scratch_repo):
    """RE-VERIFY N-6. `serve.py` had grown a second copy of this question and
    the two had already diverged — this one is the safer reading, and it is the
    only one now. The comparison goes through
    `snapshot_registry.normalize_ref`, exactly as every other registry consumer
    does, so a ref carrying stray whitespace resolves rather than silently
    failing to match. (It does NOT strip `refs/heads/` — an earlier draft of
    this note claimed it did, and that was wrong.)"""
    from ideation_dashboard import doxbench_scope
    from ideation_dashboard.doxbench_scope import ScopeKey

    registry, ref = _open_a_real_session(scratch_repo)
    key = ScopeKey(repository=scratch_repo.repository, ref=ref,
                   tile_kind="staged", tile_id=scratch_repo.topic_id)
    assert doxbench_scope.is_live_session_ref(
        registry, key, repository=scratch_repo.repository, ref=ref) is True
    # the SAME branch, spelled with stray whitespace
    assert doxbench_scope.is_live_session_ref(
        registry, key, repository=scratch_repo.repository,
        ref=f"  {ref}  ") is True
    # …and a genuinely different spelling is still not this session
    assert doxbench_scope.is_live_session_ref(
        registry, key, repository=scratch_repo.repository,
        ref=f"refs/heads/{ref}") is False
    # and serve.py's method is that function, not a copy of it
    serve_source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                    / "serve.py").read_text(encoding="utf-8")
    assert "doxbench_scope.is_live_session_ref(" in serve_source
    assert "live_session_branches(" not in serve_source, (
        "serve.py must ASK the shared question, not re-derive it (a prose "
        "mention of the authority is fine; a call is a second copy)")


def test_a_ref_that_is_not_a_live_session_branch_has_no_worktree(scratch_repo):
    """The fail-closed half still holds: `main` is not a session."""
    from ideation_dashboard.doxbench_scope import ScopeKey
    from ideation_dashboard import snapshot_registry as reg

    registry, _ref = _open_a_real_session(scratch_repo)
    key = ScopeKey(repository=scratch_repo.repository, ref=reg.DEFAULT_REF,
                   tile_kind="staged", tile_id=scratch_repo.topic_id)
    assert _real_worktree_for(registry, key) is None


def test_another_tiles_session_is_not_this_tiles_worktree(scratch_repo):
    """Liveness is asked over THIS tile's branch family, so one tile's session
    never answers another tile's thread question."""
    from ideation_dashboard.doxbench_scope import ScopeKey

    registry, ref = _open_a_real_session(scratch_repo)
    key = ScopeKey(repository=scratch_repo.repository, ref=ref,
                   tile_kind="staged", tile_id="some-other-topic")
    assert _real_worktree_for(registry, key) is None


def test_the_thread_prefix_is_declared_on_exactly_one_gate():
    """The widening is as narrow as the task allows: ONE prefix, ONE gate."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "gate_routes.py").read_text(encoding="utf-8")
    assert source.count("doxbench_threads.THREAD_PREFIX") == 1
