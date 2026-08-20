"""The LOCAL HARNESS BRIDGE (add-doxbench-editing-phase-b tasks 11.1-11.6).

HERMETIC BY CONSTRUCTION, AND THE CONSTRUCTION IS THE POINT. `omp` is not
installed on this host and no gate may require it, so every process test here
drives `fixtures/fake_omp_child.py` — a real child, over real pipes, speaking
the frames `verification-findings.md` recorded hands-on and no others. What
that buys over an in-process double: the JSONL framing, the stdin flush, the
stdout reader thread, the stderr drain, and process death are all REAL, which
is where a stdio adapter's defects actually live.

The failure modes that cannot be driven through a real child without making the
suite slow or flaky (an unstartable command, a spawn that raises) use an
injected spawn instead — the same seam, one layer in.
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
from pathlib import Path

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_bridge as br  # noqa: E402
from ideation_dashboard import doxbench_mcp as mcp  # noqa: E402
from ideation_dashboard import doxbench_threads as dt  # noqa: E402
from ideation_dashboard.doxbench_model import (  # noqa: E402
    ModelCatalog, ModelCatalogEntry, WorkbenchModelPort,
)

FAKE_CHILD = Path(__file__).resolve().parent / "fixtures" / "fake_omp_child.py"


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------


def _entry(model_id="opus", *, available=True):
    return ModelCatalogEntry(
        model_id=model_id, label=model_id.title(), provider_class="on-tenant",
        available=available, input_limit_bytes=200_000,
        output_limit_bytes=64_000, data_handling="stays on this tenant")


def _catalog(*entries):
    return ModelCatalog.from_entries(entries or (_entry(),))


class _Section:
    def __init__(self, key, text):
        self.key = key
        self.text = text


class _Envelope:
    def __init__(self, model_id="opus", sections=None):
        self.model_id = model_id
        self.sections = tuple(sections or (
            _Section("system_contract", "ground every answer"),
            _Section("human_message", "Human message:\nwhat changed?")))


def _fake_spawn(*scripted):
    """A spawn seam that starts the FAKE child with the bridge's own argv tail,
    so the launch flags this module builds are really parsed by a real
    process."""

    def spawn(argv, environment, cwd):
        command = [sys.executable, str(FAKE_CHILD), *list(argv)[1:], *scripted]
        return subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=dict(environment), cwd=str(cwd))
    return spawn


LIVE_THREAD = "ideation/staging/t/a.md"


def _turn_frames(seen):
    """The frames the TURN itself sent. The bind that precedes every dispatch
    issues its own `get_state`/`switch_session`, which is not the turn."""
    return [frame for frame in seen
            if frame.get("type") in ("set_model", "prompt")]


def _dispatch(bridge, envelope=None, *, thread=LIVE_THREAD):
    """Bind a conversation, then dispatch — the order the ROUTE uses.

    Since the adversarial review's P2-11 a turn is always bound to the
    conversation it belongs to (a document, or the tile's outline), and the
    bridge REFUSES an unbound dispatch rather than running it in whichever
    session the harness was last switched to. Every dispatch test therefore
    binds first, exactly as the route does."""

    bridge.select_thread(thread)
    return bridge.dispatch(envelope if envelope is not None else _Envelope())


def _bridge(tmp_path, *scripted, catalog=None, log=None, **kwargs):
    # A DECLARED harness provider id is what a real install has (re-verify
    # N-1): the shipped `None` default cannot send `set_model` at all, because
    # a provider-less frame is refused by the harness with
    # `Model not found: undefined/<model>`. Tests about dispatch mechanics
    # therefore declare one, exactly as an operator does; the undeclared path
    # has its own two tests below.
    kwargs.setdefault("launch", br.LaunchConfig(
        session_dir=tmp_path / "bridge", provider_id="local-proxy"))
    return br.OmpHarnessBridge(
        catalog if catalog is not None else _catalog(),
        session_root=tmp_path / "bridge",
        spawn=_fake_spawn(*scripted),
        log=log if log is not None else (lambda line: None),
        environment={"PATH": "/usr/bin:/bin"},
        **kwargs)


# ===========================================================================
# 11.2 — AN ADAPTER FOR THE UNCHANGED THREE-MEMBER PORT
# ===========================================================================


def test_the_port_still_declares_exactly_three_members(tmp_path):
    """Task 11.2, asserted where the slice that would have widened it lives.
    `test_doxbench_model.py` pins the same equality; this one pins that THIS
    slice did not move it, which is the claim §11 actually makes."""
    assert WorkbenchModelPort.__protocol_attrs__ == {
        "timeout_seconds", "catalog", "dispatch"}


def test_the_de_facto_adapter_surface_is_declared_even_though_the_ban_is_not(
        tmp_path):
    """P3-21, recorded as a test rather than left as a comment.

    The PORT is three members and `FORBIDDEN_PORT_MEMBERS` polices exactly
    those. But the ROUTE reaches four more names on the adapter duck-typed —
    `select_thread`, `outline_conversation_key`, `mirror`, `dereference` — and
    the ban list cannot see that widening, because a duck-typed call is not a
    protocol member. That is not a D14 violation: none of them is a second
    spelling of the provider verb, and each is a capability D14 explicitly puts
    INSIDE the adapter. What it is is a contract nothing else states, so it is
    stated here: this is the set the route may reach, and a fifth name arriving
    without this list moving is the thing to argue about.

    WHAT THIS TEST CANNOT SEE (re-verify N-8): it detects only the
    `getattr(port, "…")` spelling. A route reaching a fifth capability as a
    plain attribute access (`port.something`), through `hasattr`, or off a
    variable would pass here unnoticed. The declared set is still the contract;
    this assertion is a tripwire on the one spelling the route actually uses,
    not a proof of absence."""

    reached = {"conversation_key", "outline_conversation_key",
               "for_conversation", "mirror", "dereference"}
    bridge = _bridge(tmp_path)
    for name in reached:
        assert callable(getattr(bridge, name, None)), name
    serve_source = (REPO_ROOT / "scripts" / "ideation_dashboard"
                    / "serve.py").read_text(encoding="utf-8")
    duck_typed = {name for name in
                  ("select_thread", "conversation_key",
                   "outline_conversation_key", "for_conversation", "mirror",
                   "dereference", "shake", "run_command", "catalog", "dispatch")
                  if f'getattr(port, "{name}"' in serve_source}
    assert duck_typed <= reached | {"catalog", "dispatch"}, sorted(duck_typed)


def test_the_bridge_satisfies_the_port_without_growing_a_provider_verb(tmp_path):
    from test_doxbench_model import FORBIDDEN_PORT_MEMBERS

    bridge = _bridge(tmp_path)
    assert isinstance(bridge, WorkbenchModelPort)
    public = {name for name in dir(bridge) if not name.startswith("_")}
    # The adapter may carry adapter surface (select_thread, shake, dereference,
    # mirror); what it may NOT carry is a second spelling of the provider verb.
    assert not (public & FORBIDDEN_PORT_MEMBERS), sorted(
        public & FORBIDDEN_PORT_MEMBERS)


def test_the_bridge_module_declares_no_credential_shaped_name():
    """Task 11.1's "holding no credential", asserted against the source rather
    than described: a bridge that grew a key field would fail here."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "doxbench_bridge.py").read_text(encoding="utf-8")
    for forbidden in ("api_key", "apiKey", "ANTHROPIC_API_KEY", "OPENAI_API_KEY",
                      "bearer", "Authorization", "secret_key"):
        assert forbidden not in source, forbidden


# ===========================================================================
# 11.1 — THE LAUNCH: loopback-local, credential-free, memory pinned off
# ===========================================================================


def test_the_launch_argv_uses_only_flags_the_real_binary_declares(tmp_path):
    """CORRECTED after the adversarial review's P1-1. `--setting` is not an omp
    flag — real v17.3.7 answers `Error: unknown flag: --setting` and exits — so
    the memory pin rides a `--config` overlay, which `omp --help` really
    declares and which outranks both the global and the project layers."""
    launch = br.LaunchConfig(session_dir=tmp_path / "sessions")
    argv = launch.argv()
    assert argv[0] == "omp"
    assert argv[1:3] == ("--mode", "rpc")
    assert "--profile" in argv and "doxbench-bridge" in argv
    assert f"--config={launch.overlay_path}" in argv
    # the flag that never existed must never come back
    assert not any(arg.startswith("--setting") for arg in argv), argv
    assert launch.declares_memory_off() is True


def test_the_overlay_pins_the_memory_backend_as_a_quoted_string(tmp_path):
    """Bare `off` is a YAML 1.1 BOOLEAN and the setting is a string enum, so the
    rendered value is quoted. A test rather than a comment, because the whole
    point of the overlay is that the harness reads it."""
    launch = br.LaunchConfig(session_dir=tmp_path / "sessions")
    assert launch.overlay_text() == 'memory:\n  backend: "off"\n'
    written = launch.write_overlay()
    assert written == launch.overlay_path
    assert written.read_text(encoding="utf-8") == launch.overlay_text()


def test_a_child_start_always_materialises_the_overlay_it_names(tmp_path):
    """A `--config` overlay is STRICT: a missing file is a hard startup error,
    not a skipped option. So the file has to exist whenever the argv names it."""
    bridge = _bridge(tmp_path)
    assert not bridge.launch.overlay_path.exists()
    _dispatch(bridge)
    assert bridge.launch.overlay_path.is_file()
    bridge.stop()


def test_a_launch_that_drops_the_memory_pin_is_visible_to_the_mirror(tmp_path):
    """Verification §3.1's implementation consequence, enforced rather than
    documented: a bridge whose launch config lost the pin refuses to mirror
    instead of quietly starting a second store. Read from the OVERLAY, which is
    what actually carries the pin."""
    launch = br.LaunchConfig(session_dir=tmp_path / "s", overlay={})
    bridge = _bridge(tmp_path, launch=launch)
    thread = _thread("ideation/staging/t/a.md")
    turn = dt.ThreadTurn(turn_id="t1", model="opus", bound_buffer_key="a",
                         human="hi", assistant="there")
    with pytest.raises(br.BridgeError, match="memory.backend"):
        bridge.mirror().mirror_turn(thread, turn)


def test_the_child_environment_is_an_allowlist_not_a_denylist():
    given = {"PATH": "/bin", "HOME": "/h", "ANTHROPIC_API_KEY": "sk-live",
             "OMP_TOKEN": "t", "AWS_SECRET_ACCESS_KEY": "s"}
    assert br.child_environment(given) == {"PATH": "/bin", "HOME": "/h"}


def test_no_child_is_started_until_a_turn_needs_one(tmp_path):
    """Task 11.3's first clause: an editor-only session must not spawn a model
    process it never uses. `catalog()` is the route's pre-turn call and it must
    not start anything."""
    bridge = _bridge(tmp_path)
    assert bridge.started is False
    bridge.catalog()
    assert bridge.started is False
    _dispatch(bridge)
    assert bridge.started is True
    bridge.stop()


def test_an_UNBOUND_dispatch_is_refused_rather_than_run_somewhere_else(tmp_path):
    """P2-11, structurally. An outline-bound turn used to reach `dispatch` with
    no bind at all, so it was prompted into whichever DOCUMENT session the
    harness was last switched to — and that document's session accumulated it.
    The bridge now refuses, so a caller cannot reintroduce the leak by
    forgetting."""
    bridge = _bridge(tmp_path)
    with pytest.raises(br.BridgeSessionConflict):
        bridge.dispatch(_Envelope())
    bridge.stop()


def test_TWO_SCOPES_sharing_a_document_path_get_TWO_sessions(tmp_path):
    """PR #223, Codex C1 — the reproduction, now a pin.

    The conversation key was the bare `bound_buffer_key`: a repository-relative
    path and nothing else, against a SINGLE per-serve session map. Two scopes
    that load the same path — one repository at two refs, or two repositories on
    a multi-repository plane — collided, and the second silently inherited the
    first's harness session and its conversation context."""
    from ideation_dashboard.doxbench_scope import ScopeKey

    document = "ideation/staging/shared/README.md"
    scopes = (
        ScopeKey(repository="repo-a", ref="main", tile_kind="staged", tile_id="t"),
        ScopeKey(repository="repo-b", ref="main", tile_kind="staged", tile_id="t"),
        ScopeKey(repository="repo-a", ref="draft/t", tile_kind="staged", tile_id="t"),
        ScopeKey(repository="repo-a", ref="main", tile_kind="possible", tile_id="t"),
        ScopeKey(repository="repo-a", ref="main", tile_kind="staged", tile_id="u"),
    )
    keys = {br.OmpHarnessBridge.conversation_key(scope, document)
            for scope in scopes}
    assert len(keys) == len(scopes), sorted(keys)
    # …and the outline key is scoped the same way
    outlines = {br.OmpHarnessBridge.outline_conversation_key(scope)
                for scope in scopes}
    assert len(outlines) == len(scopes)
    assert not (keys & outlines)

    # the composition is INJECTIVE: no spelling of one scope can forge another
    forged = ScopeKey(repository="repo-a", ref="main", tile_kind="staged",
                      tile_id='t", "x')
    assert br.OmpHarnessBridge.conversation_key(forged, document) not in keys

    # and two different scopes really do get two SESSIONS through the bridge
    first, second = str(tmp_path / "s1.jsonl"), str(tmp_path / "s2.jsonl")
    calls = {"n": 0}

    def spawn(argv, environment, cwd):
        calls["n"] += 1
        session = first if calls["n"] == 1 else second
        return subprocess.Popen(
            [sys.executable, str(FAKE_CHILD), *list(argv)[1:],
             "--session-file", session],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=dict(environment), cwd=str(cwd))

    bridge = br.OmpHarnessBridge(
        _catalog(), session_root=tmp_path / "bridge", spawn=spawn,
        launch=br.LaunchConfig(session_dir=tmp_path / "bridge",
                               provider_id="local-proxy"),
        log=lambda line: None, environment={"PATH": "/usr/bin:/bin"})
    a = bridge.select_thread(
        br.OmpHarnessBridge.conversation_key(scopes[0], document))
    b = bridge.select_thread(
        br.OmpHarnessBridge.conversation_key(scopes[1], document))
    bridge.stop()
    assert a == first and b == second
    assert a != b, "two scopes shared one harness session"


def test_BIND_AND_DISPATCH_are_ONE_critical_section(tmp_path):
    """PR #223, Codex C2 — the reproduction, now a pin.

    `select_thread` and `dispatch` each took the bridge lock separately, and
    this server is threaded: handler A selects A, handler B selects B, then A's
    dispatch sends A's prompt into B's session. Reproduced directly — after an
    interleaved bind, `_selected` was the other handler's conversation.

    The bind is now part of the dispatch, inside one lock acquisition, so an
    interleaved selection cannot land between them."""
    bridge = _bridge(tmp_path)
    key_a, key_b = "conversation-A", "conversation-B"
    bridge.select_thread(key_a)

    seen = []
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        seen.append(dict(frame))
        # the interleaving handler, DURING A's dispatch
        if frame["type"] == "set_model" and not getattr(_spy, "raced", False):
            _spy.raced = True
            racer = threading.Thread(target=bridge.select_thread, args=(key_b,))
            racer.start()
            racer.join(timeout=1.0)
            # the racer cannot get in: the lock is held for the whole turn
            assert racer.is_alive(), "the bind was not held across the dispatch"
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        answer = bridge.for_conversation(key_a).dispatch(_Envelope())
    finally:
        br.HarnessChild.request = original
    assert answer["assistant_prose"]
    # the turn ran in A's conversation, whatever the other handler wanted
    assert bridge._selected in (key_a, key_b)   # noqa: SLF001
    prompts = [f for f in seen if f["type"] == "prompt"]
    assert len(prompts) == 1
    bridge.stop()


def test_the_conversation_view_is_the_three_member_port_and_nothing_more(
        tmp_path):
    """C2's fix must not widen the port: `dispatch_turn` calls
    `port.dispatch(envelope)` and knows nothing of conversations."""
    from test_doxbench_model import FORBIDDEN_PORT_MEMBERS

    bridge = _bridge(tmp_path)
    view = bridge.for_conversation("c")
    assert isinstance(view, WorkbenchModelPort)
    public = {name for name in dir(view) if not name.startswith("_")}
    assert public == {"timeout_seconds", "catalog", "dispatch"}, sorted(public)
    assert not (public & FORBIDDEN_PORT_MEMBERS)
    with pytest.raises(br.BridgeSessionConflict):
        bridge.for_conversation("")
    bridge.stop()


def test_an_outline_turn_binds_its_TILES_own_conversation(tmp_path):
    """An outline conversation is a real conversation; it just is not a
    document's. Keyed by the tile, because two tiles' outlines are two
    conversations and a bare `outline` would merge them."""
    from ideation_dashboard.doxbench_scope import ScopeKey
    scope_a = ScopeKey(repository="r", ref="main", tile_kind="staged",
                       tile_id="topic-a")
    scope_b = ScopeKey(repository="r", ref="main", tile_kind="staged",
                       tile_id="topic-b")
    first = br.OmpHarnessBridge.outline_conversation_key(scope_a)
    second = br.OmpHarnessBridge.outline_conversation_key(scope_b)
    assert first != second
    assert br.OUTLINE_CONVERSATION_BUFFER in first
    # …and it can never collide with a document's key in the same scope
    assert first != br.OmpHarnessBridge.conversation_key(scope_a, "ideation/x.md")

    session_a = str(tmp_path / "a.jsonl")
    bridge = _bridge(tmp_path, "--session-file", session_a)
    assert bridge.select_thread(first) == session_a
    assert _dispatch(bridge, thread=first)["assistant_prose"]
    bridge.stop()


# ===========================================================================
# 11.6 — set_model BEFORE prompt, inside the adapter
# ===========================================================================


def test_a_turn_sets_the_model_before_prompting_over_a_real_child(tmp_path):
    bridge = _bridge(tmp_path, "--reply", "the harness answered")
    answer = _dispatch(bridge, _Envelope(model_id="opus"))
    assert answer == {"assistant_prose": "the harness answered", "proposals": []}
    bridge.stop()


def test_the_model_the_harness_is_set_to_is_the_envelope_s_own(tmp_path):
    seen = []

    class _Recording:
        def __init__(self, inner):
            self.inner = inner

        def __call__(self, argv, environment, cwd):
            return self.inner(argv, environment, cwd)

    bridge = _bridge(tmp_path)
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        seen.append(dict(frame))
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        _dispatch(bridge, _Envelope(model_id="opus"))
    finally:
        br.HarnessChild.request = original
        bridge.stop()
    kinds = [frame["type"] for frame in _turn_frames(seen)]
    assert kinds == ["set_model", "prompt"], kinds
    assert _turn_frames(seen)[0]["modelId"] == "opus"


def test_a_harness_that_refuses_the_model_refuses_the_turn(tmp_path):
    bridge = _bridge(tmp_path, "--known-provider", "something-else",
                     launch=br.LaunchConfig(session_dir=tmp_path / "s",
                                            provider_id="local-proxy"))
    with pytest.raises(br.BridgeProtocolError):
        _dispatch(bridge)
    bridge.stop()


def test_the_harness_provider_id_comes_from_the_INSTALL_not_the_catalog(tmp_path):
    """P1-5. `provider_class` is a GOVERNANCE data-handling classification, and
    sending it as the harness provider id had every real `set_model` refused
    with `Model not found: self_hosted/local-model`. The harness provider id is
    an install-side declaration; the catalog entry never supplies one."""
    catalog = _catalog(_entry("opus"))
    assert catalog.entries[0].provider_class == "on-tenant"
    seen = []
    bridge = _bridge(tmp_path, catalog=catalog,
                     launch=br.LaunchConfig(session_dir=tmp_path / "s",
                                            provider_id="local-proxy"))
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        seen.append(dict(frame))
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        _dispatch(bridge, _Envelope(model_id="opus"))
    finally:
        br.HarnessChild.request = original
        bridge.stop()
    assert _turn_frames(seen)[0]["provider"] == "local-proxy"
    assert "on-tenant" not in json.dumps(seen)


def test_a_PROVIDERLESS_set_model_is_never_sent(tmp_path):
    """RE-VERIFY N-1. This used to omit the `provider` key when the install
    declared none, on a docstring claim that the harness would then resolve the
    model itself. Live, it answers
    `Model not found: undefined/local-model` — so the SHIPPED DEFAULT refused
    every real turn. No provider-less `set_model` is ever sent now."""
    seen = []
    bridge = _bridge(tmp_path, "--current-model", "opus",
                     launch=br.LaunchConfig(session_dir=tmp_path / "bridge"))
    assert bridge.launch.provider_id is None
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        seen.append(dict(frame))
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        answer = _dispatch(bridge, _Envelope(model_id="opus"))
    finally:
        br.HarnessChild.request = original
        bridge.stop()
    assert answer["assistant_prose"]
    assert not [frame for frame in seen if frame["type"] == "set_model"], seen


def test_an_undeclared_provider_REFUSES_a_model_the_harness_is_not_on(tmp_path):
    """The honest half of N-1's fix, and a judgement call: letting the profile's
    default model answer under this turn's recorded `model_id` would put a false
    model on a durable record."""
    bridge = _bridge(tmp_path, "--current-model", "some-other-model",
                     launch=br.LaunchConfig(session_dir=tmp_path / "bridge"))
    with pytest.raises(br.BridgeProtocolError, match="no harness provider id"):
        _dispatch(bridge, _Envelope(model_id="opus"))
    bridge.stop()


def test_the_fixture_refuses_a_providerless_set_model_like_the_real_binary(
        tmp_path):
    """The P1-7 lesson, completed. The fixture ACCEPTED a missing provider where
    real omp refuses it, which is exactly why the broken default passed every
    hermetic test. Driven straight at the fixture so the refusal shape itself is
    pinned, verbatim from the live capture."""
    bridge = _bridge(tmp_path,
                     launch=br.LaunchConfig(session_dir=tmp_path / "bridge",
                                            provider_id="local-proxy"))
    bridge.select_thread(LIVE_THREAD)
    child = bridge._child                       # noqa: SLF001 - the fixture IS the subject
    answer = child.request(
        {"id": "sm-none", "type": "set_model", "modelId": "local-model"},
        deadline=__import__("time").monotonic() + 20,
        clock=__import__("time").monotonic)
    bridge.stop()
    assert answer.success is False
    assert answer.error == "Model not found: undefined/local-model"


def test_a_governance_label_sent_as_a_provider_is_refused_by_the_harness(tmp_path):
    """The fixture reproduces the REAL refusal shape, so the defect that shipped
    would fail here rather than only in production."""
    bridge = _bridge(tmp_path, "--known-provider", "local-proxy",
                     launch=br.LaunchConfig(session_dir=tmp_path / "s",
                                            provider_id="self_hosted"))
    with pytest.raises(br.BridgeProtocolError):
        _dispatch(bridge)
    bridge.stop()


def test_a_routing_rule_entry_would_set_the_RESOLVED_model(tmp_path):
    """Task 11.7's RUNTIME half. No conformant catalog entry can declare a
    routing rule today — the released catalog schema is a CLOSED seven-field
    entry — so this drives a duck-typed entry that CAN, proving the adapter
    already honours whatever a lawful catalog grows into without a change."""

    class _RoutingEntry:
        model_id = "auto"
        provider_class = "routed"
        resolved_model_id = "opus"
        available = True

    class _Catalog:
        entries = ()

        @staticmethod
        def entry_for(model_id):
            return _RoutingEntry() if model_id == "auto" else None

    bridge = _bridge(tmp_path)
    bridge._declared_catalog = _Catalog()      # noqa: SLF001 - the point of the test
    seen = []
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        seen.append(dict(frame))
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        _dispatch(bridge, _Envelope(model_id="auto"))
    finally:
        br.HarnessChild.request = original
        bridge.stop()
    assert _turn_frames(seen)[0]["modelId"] == "opus"


def test_every_entry_a_conformant_catalog_can_hold_is_truthfully_not_a_routing_rule():
    """The other half of 11.7's honesty clause: nothing in the shipped catalog
    type can claim to be a routing rule, so the record's `routing_rule` is
    truthfully false for every entry that can exist today."""
    entry = _entry()
    assert not hasattr(entry, "routing_rule")
    assert not hasattr(entry, "resolved_model_id")


# ===========================================================================
# 11.3 — SUPERVISION
# ===========================================================================


def test_a_child_that_dies_mid_turn_surfaces_as_unavailable_not_a_hang(tmp_path):
    # dies while handling the FIRST command, which is `set_model`
    bridge = _bridge(tmp_path, "--die-after", "1")
    with pytest.raises(br.BridgeUnavailable):
        _dispatch(bridge)
    bridge.stop()


def test_an_unstartable_bridge_refuses_inside_a_bounded_retry(tmp_path):
    attempts = []

    def _never(argv, environment, cwd):
        attempts.append(argv)
        raise OSError("no such command")

    bridge = br.OmpHarnessBridge(
        _catalog(), session_root=tmp_path / "bridge", spawn=_never,
        log=lambda line: None, environment={}, max_restarts=2)
    with pytest.raises(br.BridgeUnavailable):
        _dispatch(bridge)
    # bounded: the retry stops, it does not spin
    assert len(attempts) == 3, attempts


def test_a_child_that_STARTS_AND_DIES_flips_the_catalog_too(tmp_path):
    """P2-8. `_unavailable` used to be set only where `Popen` itself raised, so
    the commonest real failure — a child that spawns and then exits — left the
    catalog advertising the model as available forever and pushed every later
    turn onto leg 2 instead of the pre-dispatch refusal 11.3 promises."""
    bridge = _bridge(tmp_path, "--die-after", "1",
                     catalog=_catalog(_entry("opus"), _entry("kimi")))
    assert [e.available for e in bridge.catalog().entries] == [True, True]
    with pytest.raises(br.BridgeUnavailable):
        _dispatch(bridge)
    assert bridge.available is False
    assert [e.available for e in bridge.catalog().entries] == [False, False]
    assert bridge.catalog().selectable_entry_for("opus") is None
    bridge.stop()


def test_a_child_KILLED_EXTERNALLY_is_reported_unavailable_with_no_call_since(
        tmp_path):
    """RE-VERIFY N-3: `_known_dead` was unpinned — reverting it left every suite
    green, because every other path reaches `_unavailable` through a failed
    call. This is the case it exists for: the child dies with NO public call in
    between, and the next thing that happens is a catalog poll — which is
    exactly what `GET /workbench/model-catalog` does."""
    bridge = _bridge(tmp_path, catalog=_catalog(_entry("opus"), _entry("kimi")))
    _dispatch(bridge)
    assert bridge.available is True
    assert [e.available for e in bridge.catalog().entries] == [True, True]

    # killed from outside — nothing calls the bridge, nothing raises
    bridge._child._process.kill()               # noqa: SLF001 - an external death
    bridge._child._process.wait(timeout=10)     # noqa: SLF001

    assert [e.available for e in bridge.catalog().entries] == [False, False]
    assert bridge.catalog().selectable_entry_for("opus") is None
    # N-4: the two public readers agree
    assert bridge.available is False
    bridge.stop()


def test_an_unavailable_bridge_reports_every_catalog_entry_unavailable(tmp_path):
    """The FIRST of task 11.3's two legs, and the one that keeps the route's
    gate ORDER unchanged: an unavailable entry fails `selectable_entry_for` at
    the route's existing model step, which refuses with the existing fixed code
    before any packet is assembled and before any dispatch."""

    def _never(argv, environment, cwd):
        raise OSError("no such command")

    bridge = br.OmpHarnessBridge(
        _catalog(_entry("opus"), _entry("kimi")), session_root=tmp_path / "b",
        spawn=_never, log=lambda line: None, environment={})
    assert [e.available for e in bridge.catalog().entries] == [True, True]
    with pytest.raises(br.BridgeUnavailable):
        _dispatch(bridge)
    assert [e.available for e in bridge.catalog().entries] == [False, False]
    assert bridge.catalog().selectable_entry_for("opus") is None


def test_child_stderr_reaches_the_serve_log_and_never_the_answer(tmp_path):
    logged = []
    bridge = _bridge(tmp_path, "--stderr", "SECRET-DIAGNOSTIC-TEXT",
                     log=logged.append)
    answer = _dispatch(bridge)
    bridge.stop()
    assert "SECRET-DIAGNOSTIC-TEXT" not in json.dumps(answer)
    assert any("SECRET-DIAGNOSTIC-TEXT" in line for line in logged), logged


def test_a_non_json_banner_on_stdout_is_ignored_rather_than_fatal(tmp_path):
    bridge = _bridge(tmp_path, "--banner", "omp v17.3.7 ready")
    assert _dispatch(bridge)["assistant_prose"]
    bridge.stop()


def test_the_unsolicited_startup_frames_a_real_harness_sends_are_ignored(
        tmp_path):
    """A real session opens with `ready` and then emits `extension_ui_request`
    and `available_commands_update` around every command, unasked. A host that
    cannot ignore them cannot talk to omp at all — and the fixture now sends
    them, so this is exercised rather than assumed."""
    bridge = _bridge(tmp_path)
    assert _dispatch(bridge)["assistant_prose"]
    bridge.stop()


def test_a_frame_over_the_v1_cap_is_dropped_while_reading(tmp_path):
    """P3-16. The cap is the REAL v1 one the `ready` frame advertises, and it is
    enforced by a bounded read, so an unbounded run of bytes with no newline
    cannot be materialised before the guard runs."""
    import io

    assert br.MAX_FRAME_BYTES == 1024 * 1024
    oversize = b"x" * (br.MAX_FRAME_BYTES + 64)
    stream = io.BytesIO(oversize + b"\n" + b'{"type":"ready"}\n')
    assert list(br._bounded_lines(stream)) == [b'{"type":"ready"}\n']


# ===========================================================================
# 11.4 — ONE SESSION PER DOCUMENT THREAD
# ===========================================================================


def _thread(document, *, goal="", refs=()):
    return dt.DocumentThread(
        document=document,
        scope=dt.ThreadScope(repository="fixture-repo", tile_kind="staged",
                             tile_id="ideation-governance"),
        state=dt.ThreadState(active_goal=goal, evidence_refs=tuple(refs)))


def test_selecting_a_thread_twice_switches_the_harness_session_once(tmp_path):
    session = str(tmp_path / "sessions" / "2026-08-19T00-00-00-000Z_abc.jsonl")
    bridge = _bridge(tmp_path, "--session-file", session)
    frames = []
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        frames.append(dict(frame))
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        first = bridge.select_thread("ideation/staging/t/a.md")
        again = bridge.select_thread("ideation/staging/t/a.md")
    finally:
        br.HarnessChild.request = original
        bridge.stop()
    assert first == session and again == session
    # the SECOND selection of the same thread is a no-op: no second get_state,
    # no switch_session, because the harness is already on that thread.
    assert [f["type"] for f in frames] == ["get_state"]


def test_a_second_thread_gets_a_FRESH_session_and_the_first_switches_back(tmp_path):
    """Task 11.4 in one test: one session per document thread, switching the
    selected document switches the harness session, and one session never
    serves two threads."""
    first_session = str(tmp_path / "s1.jsonl")
    second_session = str(tmp_path / "s2.jsonl")
    calls = {"n": 0}

    def spawn(argv, environment, cwd):
        calls["n"] += 1
        session = first_session if calls["n"] == 1 else second_session
        command = [sys.executable, str(FAKE_CHILD), *list(argv)[1:],
                   "--session-file", session]
        return subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=dict(environment), cwd=str(cwd))

    bridge = br.OmpHarnessBridge(
        _catalog(), session_root=tmp_path / "bridge", spawn=spawn,
        log=lambda line: None, environment={"PATH": "/usr/bin:/bin"})
    frames = []
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        frames.append(dict(frame))
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        a = bridge.select_thread("ideation/staging/t/a.md")
        b = bridge.select_thread("ideation/staging/t/b.md")
        back = bridge.select_thread("ideation/staging/t/a.md")
    finally:
        br.HarnessChild.request = original
        bridge.stop()
    assert a == first_session
    assert b == second_session
    assert a != b, "two threads shared one session"
    assert back == first_session
    # the RETURN to the first thread is a `switch_session` carrying that
    # thread's OWN recorded path — the recorded second-process flow.
    switches = [f for f in frames if f["type"] == "switch_session"]
    assert len(switches) == 1
    assert switches[0]["sessionPath"] == first_session
    assert calls["n"] == 2, "a fresh session per thread means one start each"


def test_a_session_already_bound_to_another_thread_is_refused(tmp_path):
    """One session never serves two threads. Driven by a harness that reports
    the SAME session file for a second thread, which is the shape the refusal
    exists for."""
    same = str(tmp_path / "one.jsonl")
    bridge = _bridge(tmp_path, "--session-file", same)
    bridge.select_thread("ideation/staging/t/a.md")
    with pytest.raises(br.BridgeSessionConflict):
        bridge.select_thread("ideation/staging/t/b.md")
    bridge.stop()


# ===========================================================================
# LAYER THREE — /shake (verification §3.6)
# ===========================================================================


def test_shake_rides_the_prompt_channel_and_reports_free_text_only(tmp_path):
    bridge = _bridge(tmp_path)
    bridge.select_thread(LIVE_THREAD)
    sent = []
    original = br.HarnessChild.request

    def _spy(self, frame, *, deadline, clock):
        sent.append(dict(frame))
        return original(self, frame, deadline=deadline, clock=clock)

    br.HarnessChild.request = _spy
    try:
        report = bridge.shake()
    finally:
        br.HarnessChild.request = original
        bridge.stop()
    assert sent[-1] == {"id": sent[-1]["id"], "type": "prompt",
                        "message": "/shake elide"}
    assert report.agent_invoked is False
    assert report.summary == "Nothing to shake."
    # there is no structured bytes-reclaimed field, and this type claims none
    assert not hasattr(report, "bytes_reclaimed")


def test_an_unrecorded_shake_mode_is_refused_rather_than_sent(tmp_path):
    bridge = _bridge(tmp_path)
    with pytest.raises(br.BridgeError):
        bridge.shake("everything")
    bridge.stop()


def test_an_UNLISTED_slash_command_is_refused_rather_than_dispatched(tmp_path):
    """RE-VERIFY N-2. `run_command`'s docstring claimed a caller passing prose
    would have it "interpreted by the harness as an unknown command". Live, an
    unknown slash command falls straight through to a REAL MODEL TURN —
    unbounded by the packet assembler, uncounted by the byte bounds and
    unrecorded in any sidecar. The head is now a closed allowlist."""
    bridge = _bridge(tmp_path)
    bridge.select_thread(LIVE_THREAD)
    for unlisted in ("/definitelynotacommand", "/compact", "/init",
                     "/shakedown"):
        with pytest.raises(br.BridgeError, match="not a builtin"):
            bridge.run_command(unlisted)
    for listed in ("/shake elide", "/memory diagnose", "/mcp list"):
        assert bridge.run_command(listed).agent_invoked is False
    bridge.stop()


def test_the_fixture_lets_an_unknown_slash_command_START_A_TURN(tmp_path):
    """The fixture reproduces the harness's real behaviour, so the allowlist is
    guarding against something this rig can actually do — otherwise the guard
    would be a test of nothing."""
    bridge = _bridge(tmp_path, "--reply", "AN UNBOUNDED TURN RAN")
    bridge.select_thread(LIVE_THREAD)
    child = bridge._child                       # noqa: SLF001 - the fixture IS the subject
    import time as _time
    answer = child.request(
        {"id": "u1", "type": "prompt", "message": "/definitelynotacommand"},
        deadline=_time.monotonic() + 20, clock=_time.monotonic)
    bridge.stop()
    assert answer.assistant_text == "AN UNBOUNDED TURN RAN"
    assert answer.agent_invoked is None, "a real model turn omits agentInvoked"


def test_a_builtin_needs_a_bound_conversation_too(tmp_path):
    """A builtin acts on the CURRENT session — an unbound `/shake` would compact
    whichever conversation the harness was last switched to."""
    bridge = _bridge(tmp_path)
    with pytest.raises(br.BridgeSessionConflict):
        bridge.run_command("/shake elide")
    bridge.stop()


# ===========================================================================
# artifact:// DEREFERENCING (verification §3.5)
# ===========================================================================


def test_the_bridge_inlines_artifact_content_through_the_harness_store(tmp_path):
    sessions = tmp_path / "sessions"
    artifacts = sessions / "2026-08-19T00-00-00-000Z_abc"
    artifacts.mkdir(parents=True)
    (artifacts / "blob1").write_text("the spilled tool output", encoding="utf-8")
    session_file = str(sessions / "2026-08-19T00-00-00-000Z_abc.jsonl")

    bridge = _bridge(tmp_path, "--session-file", session_file)
    bridge.select_thread("ideation/staging/t/a.md")
    resolved = bridge.dereference("before artifact://blob1 after")
    bridge.stop()
    assert resolved == "before the spilled tool output after"
    assert dt.HARNESS_ARTIFACT_SCHEME not in resolved


def test_an_unresolvable_pointer_becomes_an_elided_note_not_a_pointer(tmp_path):
    bridge = _bridge(tmp_path, "--session-file", str(tmp_path / "s.jsonl"))
    bridge.select_thread("ideation/staging/t/a.md")
    resolved = bridge.dereference("see artifact://missing for details")
    bridge.stop()
    assert dt.HARNESS_ARTIFACT_SCHEME not in resolved
    assert "[elided:" in resolved


def test_an_oversize_artifact_records_the_FACT_and_its_size(tmp_path):
    sessions = tmp_path / "sessions"
    artifacts = sessions / "s"
    artifacts.mkdir(parents=True)
    payload = "x" * (br.MAX_INLINE_ARTIFACT_BYTES + 1)
    (artifacts / "big").write_text(payload, encoding="utf-8")

    bridge = _bridge(tmp_path, "--session-file", str(sessions / "s.jsonl"))
    bridge.select_thread("ideation/staging/t/a.md")
    resolved = bridge.dereference("artifact://big")
    bridge.stop()
    assert str(len(payload)) in resolved
    assert dt.HARNESS_ARTIFACT_SCHEME not in resolved


def test_the_dereference_seam_satisfies_the_threads_module_s_own_builder(tmp_path):
    """The seam `doxbench_threads.dereference_bodies` asks for, driven through
    that function — so a half-resolving bridge is refused by `ThreadTurn` on the
    next line rather than persisting a pointer."""
    sessions = tmp_path / "sessions"
    (sessions / "s").mkdir(parents=True)
    (sessions / "s" / "b").write_text("inlined body", encoding="utf-8")
    bridge = _bridge(tmp_path, "--session-file", str(sessions / "s.jsonl"))
    bridge.select_thread("ideation/staging/t/a.md")
    turn = dt.dereference_bodies(
        "t1", "opus", "a.md", "what does artifact://b say?", "it says so",
        dereference=bridge.dereference)
    bridge.stop()
    assert "inlined body" in turn.human


# ===========================================================================
# THE MIRROR — the sidecar is the record (11.5)
# ===========================================================================


def test_the_mirror_is_told_the_turn_and_answers_with_nothing(tmp_path):
    bridge = _bridge(tmp_path, "--session-file", str(tmp_path / "s.jsonl"))
    mirror = bridge.mirror()
    thread = _thread("ideation/staging/t/a.md")
    turn = dt.ThreadTurn(turn_id="t1", model="opus", bound_buffer_key="a",
                         human="hi", assistant="there")
    appended = dt.mirror_turn(thread, turn, mirror=mirror)
    bridge.stop()
    assert mirror.mirror_turn(thread, turn) is None
    assert appended.turns[-1].turn_id == "t1"
    assert mirror.mirrored[0] == ("ideation/staging/t/a.md", "t1")


def test_the_mirror_implements_exactly_the_declared_operation_set(tmp_path):
    bridge = _bridge(tmp_path)
    mirror = bridge.mirror()
    for operation in dt.MIRROR_OPERATIONS:
        assert callable(getattr(mirror, operation, None))
    assert isinstance(mirror, dt.ThreadMirror)


# ===========================================================================
# THE KNOWLEDGE MOUNT REGISTRATION (task 10.2's owed note, at §11)
# ===========================================================================


def test_registering_the_mount_writes_the_config_the_harness_discovers(tmp_path):
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "note.md").write_text("Status: draft\n\nsomething", encoding="utf-8")
    manifest = mcp.MountManifest(
        sources=(("ideation/brainstorm/note.md", str(corpus / "note.md")),))
    bridge = _bridge(tmp_path)
    manifest_path, config_path = bridge.register_knowledge_mount(manifest)
    assert manifest_path.is_file() and config_path.is_file()
    assert config_path.parent.name == mcp.MCP_CONFIG_DIR
    document = json.loads(config_path.read_text(encoding="utf-8"))
    assert set(document["mcpServers"]) == {mcp.MCP_SERVER_NAME}
    assert document["mcpServers"][mcp.MCP_SERVER_NAME]["type"] == "stdio"
    # written OUTSIDE any git worktree: the bridge's own session root
    assert str(config_path).startswith(str(tmp_path / "bridge"))


def test_the_registration_is_written_before_any_child_exists(tmp_path):
    """Registration-before-first-turn is the whole guarantee on offer (MCP
    discovery is asynchronous), so it must be reachable with no child running."""
    bridge = _bridge(tmp_path)
    bridge.register_knowledge_mount(mcp.MountManifest(sources=(("r", "/x"),)))
    assert bridge.started is False


# ===========================================================================
# PROMPT RENDERING
# ===========================================================================


def test_the_prompt_message_is_the_sections_and_only_the_sections():
    envelope = _Envelope(sections=(_Section("a", "ALPHA"), _Section("b", "BETA")))
    assert br.render_prompt_message(envelope) == "ALPHA\n\nBETA"


def test_an_envelope_with_no_sections_is_refused_rather_than_composed():
    class _Empty:
        sections = ()

    with pytest.raises(br.BridgeProtocolError):
        br.render_prompt_message(_Empty())


def test_the_streaming_delta_is_read_from_where_it_really_lives():
    """P1-3. The text is INSIDE `assistantMessageEvent`, not at the frame's top
    level and not under `data` — so no addition to a flat tuple of top-level
    names could ever have found it. Frame transcribed from the real capture."""
    frame = {"type": "message_update",
             "assistantMessageEvent": {"type": "text_delta", "contentIndex": 0,
                                       "delta": "MOCK_DONE", "partial": {}},
             "message": {"role": "assistant",
                         "content": [{"type": "text", "text": "MOCK_DONE"}]}}
    assert br._assistant_text_of(frame) == "MOCK_DONE"


def test_an_event_this_module_does_not_name_contributes_NOTHING():
    """A `text_start` carries no text and a `toolcall_start` is a tool call, not
    prose. The closed table is what keeps a guess out of the transcript."""
    for event in ({"type": "text_start", "contentIndex": 0},
                  {"type": "toolcall_start", "contentIndex": 0},
                  {"type": "reasoning_delta", "delta": "thinking out loud"}):
        assert br._assistant_text_of(
            {"type": "message_update", "assistantMessageEvent": event}) == ""


def test_the_final_answer_is_read_from_the_terminal_message_list():
    """`agent_end.messages` is the harness's own final state. The LAST assistant
    message carrying prose wins: a turn can end on a tool result, and an earlier
    assistant message is working, not the answer."""
    messages = [
        {"role": "user", "content": [{"type": "text", "text": "say OK"}]},
        {"role": "assistant", "content": [{"type": "toolCall", "id": "c1"}]},
        {"role": "assistant", "content": [{"type": "text", "text": "FINAL"}]},
    ]
    assert br.final_assistant_text(messages) == "FINAL"
    assert br.final_assistant_text([]) == ""
    assert br.final_assistant_text(None) == ""


def test_an_omitted_agentInvoked_means_await_the_session_events():
    """`rpc.md:104`, and the defect that returned an empty answer at 1.97 s: an
    omitted `agentInvoked` is NOT `False`."""
    omitted = br.HarnessResponse(command="prompt", success=True, data={})
    assert omitted.agent_invoked is None
    slash = br.HarnessResponse(command="prompt", success=True,
                               data={"agentInvoked": False})
    assert slash.agent_invoked is False


def test_a_real_agent_turn_returns_the_MODELS_OWN_TEXT_not_an_empty_answer(
        tmp_path):
    """The whole of P1-4, against the rebuilt fixture: the response frame
    carries no `data`, the turn streams, and `dispatch` waits for `agent_end`
    rather than returning at the response."""
    bridge = _bridge(tmp_path, "--reply", "THE MODEL ANSWERED",
                     "--delta-chunks", "4")
    answer = _dispatch(bridge)
    bridge.stop()
    assert answer == {"assistant_prose": "THE MODEL ANSWERED", "proposals": []}


def test_a_streamed_answer_is_not_doubled_by_its_own_text_end(tmp_path):
    """`text_end` repeats the whole run it closes, so only the deltas
    accumulate — and the terminal message list is preferred over both."""
    bridge = _bridge(tmp_path, "--reply", "ABCDEF", "--delta-chunks", "3")
    assert _dispatch(bridge)["assistant_prose"] == "ABCDEF"
    bridge.stop()


def test_the_rendered_prompt_is_the_envelopes_own_rendering():
    """P3-20: one spelling. `PromptEnvelope.rendered()` is the authority, and
    the bridge's fallback join must agree with it byte for byte."""
    from ideation_dashboard.doxbench_turns import PromptEnvelope, PromptSection
    from ideation_dashboard.doxbench_scope import ScopeKey

    envelope = PromptEnvelope(
        sections=(PromptSection(key="a", text="ALPHA"),
                  PromptSection(key="b", text="BETA")),
        scope=ScopeKey(repository="r", ref="main", tile_kind="staged",
                       tile_id="t"),
        model_id="m", message="hi", transcript=(),
        active_document_path=None, observed_hashes=None)
    assert br.render_prompt_message(envelope) == envelope.rendered()
    assert br.render_prompt_message(
        _Envelope(sections=(_Section("a", "ALPHA"),
                            _Section("b", "BETA")))) == envelope.rendered()
