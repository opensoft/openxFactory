"""add-doxbench-distilled-abstract §5: `POST /actions/workbench/document-abstract`.

RED FIRST. `serve_mod.ACTIONS_WORKBENCH_DOCUMENT_ABSTRACT_ROUTE` does not exist
in this checkout, so this module fails at COLLECTION (the module-level `ROUTE`
below) rather than silently skipping — the same fail-closed opening
`test_doxbench_routes.py` uses for its own route constant.

WHAT THIS FILE PINS (tasks 5.1, 5.2, 5.4, 5.6):

  * 5.1 — the SAME three-part verdict the catalog and turn routes sit behind: a
    non-loopback plane, a plane with no gate capability, a plane with no
    resolved actor, and a caller that is not the human console are each refused,
    and none of them reaches a provider;
  * 5.2 — a subject outside `projection.editable_paths` is refused with a STATED
    reason and reaches NO provider (ruling 7(a): disclosure requires edit
    authority, `doxbench_scope.py:390`, enforced at `doxbench_turns.py:585-591`);
  * 5.4 — abstract churn over a scope larger than the cache bound MUST NOT evict
    the chat surface's turn-idempotency records, asserted against the served
    process's own `TurnStore` contents;
  * 5.6 — the response ECHOES the subject path and content digest it was
    generated for, so a result resolving against a subject the pane no longer
    has selected can be discarded unrendered (design D6).

AND the verified-answer contract this route is the consumer of: the subject
bytes are the SERVED SAVED CONTENT (never a browser buffer), the answer is
bounded by `doxbench_turns.validate_abstract_prose` and then VERIFIED by
`doxbench_knowledge.verify_document_abstract`, and a refusal renders nothing —
the body carries a refusal class, a stated reason and a caption state, and NO
prose.

N5, and it is why this file defines its own seeded port: the house fake
(`FakeWorkbenchModelPort`) returns the constant "fake grounded answer", which
the verifier REFUSES (it names neither the subject nor any declared subject of
it). That refusal is itself pinned below; a SUCCESS path therefore needs a port
whose scripted answer names the subject and a declared topic, which is what
`_seeded_port` builds.

No test here reaches a real provider: every port is an injected fake, and the
one live-provider suite in this repository (`test_doxbench_bridge_live.py`)
skips unless a harness is explicitly declared.
"""

from __future__ import annotations

import copy
import http.client
import json
import threading
from contextlib import contextmanager

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit

from ideation_dashboard import doxbench_abstract_store as store_mod
from ideation_dashboard import doxbench_hash
from ideation_dashboard import doxbench_knowledge
from ideation_dashboard import doxbench_model
from ideation_dashboard import doxbench_turns
from ideation_dashboard import serve as serve_mod
from ideation_dashboard.doxbench_model import (
    FakeWorkbenchModelPort,
    ModelCatalog,
    ModelCatalogEntry,
)
from ideation_dashboard.doxbench_scope import ScopeKey
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"

# The route under test. Referenced at module scope deliberately: it does not
# exist yet, so this file fails closed at collection.
ROUTE = serve_mod.ACTIONS_WORKBENCH_DOCUMENT_ABSTRACT_ROUTE

SUBJECT_PATH = "ideation/staging/ideation-governance/README.md"
READABLE_ONLY_PATH = "ideation/brainstorm/doc-health-checks.md"
OUT_OF_SCOPE_PATH = "ideation/staging/other-topic/README.md"
SCOPE = {"repository": "fixture-repo", "ref": "main",
         "tile_kind": "staged", "tile_id": "ideation-governance"}

# An answer that satisfies BOTH verifier rules for this fixture subject: it
# names the subject by TITLE (`README.md`) and mentions the snapshot's declared
# topic/destination (`ideation-governance`), and it names no other repository
# path. Hand-seeded rather than generated, because the point of the success path
# is that a REAL verification passed, not that a fake was waved through.
GROUNDED_PROSE = (
    "README.md is the staged ideation-governance packet: it works through the "
    "ideation-area lifecycle and its work queue, and records that its possible "
    "is picked and inherits a change id at the proposal gate."
)


def _snapshot():
    return generate_snapshot(
        BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


def _saved_content(path=SUBJECT_PATH):
    """The SERVED SAVED bytes, read through the same lens `/source` serves them
    through — never `read_text`, whose newline translation hashes text no client
    ever saw (`doxbench_hash.served_text`)."""
    return doxbench_hash.served_text((BASE_REPO / path).read_bytes())


def _saved_digest(path=SUBJECT_PATH):
    return doxbench_knowledge.document_content_digest(_saved_content(path))


# ============================================================================
# harness (mirrors test_doxbench_routes.py's `_serving`/`_request`/`_capabilities`)
# ============================================================================

@contextmanager
def _serving(tmp_path, *, actor="brett", checkout_root=None,
             model_port_factory=None, snapshot=None):
    """A real ephemeral server. NO schema validators are injected: this route
    emits no RELEASED wire envelope — no openxFactory schema declares an
    abstract shape — so it carries the same unversioned console-internal shape
    `/capabilities` and the thread read route carry, and inventing a
    `schema_version` for one here would claim a release nobody cut."""
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot or _snapshot()), encoding="utf-8")
    httpd = serve_mod.build_server(
        WEB, snap_path,
        checkout_root if checkout_root is not None else BASE_REPO,
        head=PINNED_REVISION, actor=actor,
        model_port_factory=model_port_factory)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]
    try:
        yield httpd, host, port
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)


def _handler_class(httpd):
    return getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)


def _request(host, port, method, path, *, body=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=10)
    conn.request(method, path,
                 body=None if body is None else json.dumps(body),
                 headers=headers or {})
    resp = conn.getresponse()
    raw = resp.read()
    try:
        payload = json.loads(raw.decode("utf-8") or "{}")
    except ValueError:
        payload = None
    conn.close()
    return resp.status, payload, raw


def _capabilities(host, port):
    status, payload, _raw = _request(host, port, "GET", "/capabilities")
    assert status == 200
    return payload


def _console_headers(caps):
    return {"Content-Type": "application/json",
            "X-XF-Console-Token": caps["console_token"]}


def _catalog(*, model_id="model-a", available=True):
    return ModelCatalog((ModelCatalogEntry(
        model_id=model_id, label="Approved authoring model",
        provider_class="on-tenant", available=available,
        input_limit_bytes=1_048_576, output_limit_bytes=900_000,
        data_handling="Processed in the approved tenant boundary"),))


def _seeded_port(prose=GROUNDED_PROSE, *, catalog=None, timeout_seconds=30.0):
    """N5: a port whose scripted answer is hand-seeded prose that names the
    subject and a declared topic, so the SUCCESS path exercises a real
    verification pass rather than a fake the verifier would refuse."""
    return FakeWorkbenchModelPort(
        catalog if catalog is not None else _catalog(),
        timeout_seconds=timeout_seconds,
        dispatch_result={"assistant_prose": prose, "proposals": []})


class _ScriptedPort:
    """A port whose successive dispatches return successive scripted answers —
    the one thing `FakeWorkbenchModelPort` cannot do (its scripted result is a
    constant), and exactly what a "a refusal is not cached, so a later attempt
    really re-dispatches" pin needs."""

    def __init__(self, answers, *, catalog=None, timeout_seconds=30.0):
        self._answers = list(answers)
        self._catalog = catalog if catalog is not None else _catalog()
        self.timeout_seconds = timeout_seconds
        self.calls = []
        self.dispatched = []

    def catalog(self):
        self.calls.append("catalog")
        return self._catalog

    def dispatch(self, prompt_envelope):
        self.calls.append("dispatch")
        self.dispatched.append(prompt_envelope)
        prose = self._answers.pop(0) if self._answers else ""
        return {"assistant_prose": prose, "proposals": []}


def _body(**over):
    body = {"scope": dict(SCOPE), "subject_path": SUBJECT_PATH,
            "model_id": "model-a"}
    body.update(over)
    return body


def _post(tmp_path, body=None, *, port=None, headers=None, snapshot=None,
          checkout_root=None, actor="brett", before=None):
    """POST one abstract request as the real local console.

    `before` is called with (bound handler class, capabilities) while the server
    is still up — the seam the plane-verdict and store tests need, since a
    served process's own capability dict and its two stores are not reachable
    from a response body."""
    fake = port if port is not None else _seeded_port()
    with _serving(tmp_path, model_port_factory=(lambda: fake), snapshot=snapshot,
                  checkout_root=checkout_root, actor=actor) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        if before is not None:
            before(_handler_class(httpd), caps)
        status, payload, _raw = _request(
            host, prt, "POST", ROUTE,
            body=_body() if body is None else body,
            headers=_console_headers(caps) if headers is None else headers)
    return status, payload, fake


def _assert_fixed_refusal(status, payload, code):
    """A PLANE, TRANSPORT or PROVIDER verdict: the module's pre-existing fixed
    `{ok, error, message}` shape, with the catalog's own status and message."""
    assert status == serve_mod.doxbench_error_status(code)
    assert payload == serve_mod.doxbench_error_body(code)


def _assert_abstract_refusal(status, payload, refused, *, subject=SUBJECT_PATH):
    """A STATED refusal that renders nothing: a declared class, a reason, and a
    caption state — and NO prose anywhere in the body."""
    assert payload["ok"] is False
    assert payload["refused"] == refused
    assert isinstance(payload["reason"], str) and payload["reason"].strip()
    assert payload["caption_state"] in doxbench_knowledge.CAPTION_STATES
    assert payload["subject_path"] == subject
    assert "prose" not in payload
    assert set(payload) == {"ok", "refused", "reason", "caption_state",
                            "subject_path", "subject_digest",
                            "wait_bound_seconds"}
    assert status == store_expected_status(refused)


def store_expected_status(refused):
    return serve_mod.DOXBENCH_ABSTRACT_REFUSAL_STATUS[refused]


# ============================================================================
# 5.1 — the three-part verdict, and the console gate behind it
# ============================================================================

def test_the_route_is_refused_on_a_non_loopback_plane(tmp_path, monkeypatch):
    """The hosted/read-only plane MUST offer no model-consuming route
    (`spec.md`'s provider-boundary requirement). Refused before any provider."""
    monkeypatch.setattr(serve_mod, "_is_loopback", lambda host: False)
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, port=port, headers={})
    _assert_fixed_refusal(status, payload,
                          serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert fake.calls == []


def test_the_route_is_refused_with_no_gate_capability(tmp_path):
    """Task 7.7's server half: where the gate capability is absent the
    generation control is ABSENT, so the route refuses generation. The
    capability is flipped on the BOUND handler class after the token is minted,
    because `compute_capabilities` derives `gate` and `session` from one
    local-human verdict and cannot express this plane on its own."""
    port = _seeded_port()

    def _drop_gate(handler, _caps):
        actions = dict(handler.capabilities["actions"])
        actions["gate"] = False
        handler.capabilities = {**handler.capabilities, "actions": actions}

    status, payload, fake = _post(tmp_path, port=port, before=_drop_gate)
    _assert_fixed_refusal(status, payload,
                          serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert fake.calls == []


def test_the_route_is_refused_with_no_resolved_actor(tmp_path, monkeypatch):
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *args, **kwargs: None)
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, port=port, actor=None, headers={})
    _assert_fixed_refusal(status, payload,
                          serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert fake.calls == []


def test_the_route_is_refused_without_a_real_checkout(tmp_path):
    empty = tmp_path / "empty-checkout"
    empty.mkdir()
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, port=port, checkout_root=empty,
                                  headers={})
    _assert_fixed_refusal(status, payload,
                          serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert fake.calls == []


def test_the_route_is_refused_without_the_console_token(tmp_path):
    port = _seeded_port()
    status, payload, fake = _post(
        tmp_path, port=port, headers={"Content-Type": "application/json"})
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert fake.calls == []


def test_the_plane_gate_is_consulted_before_the_console_gate(tmp_path, monkeypatch):
    """The same ordering pin the catalog route carries: with no resolved actor
    and no console header at all, the refusal names the CAPABILITY, not the
    console."""
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *args, **kwargs: None)
    status, payload, fake = _post(tmp_path, actor=None, headers={})
    assert payload["error"] == serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE
    assert fake.calls == []


def test_the_route_is_refused_with_no_model_port_declared(tmp_path):
    """No entrypoint declared a port: an absent capability, never an error."""
    with _serving(tmp_path) as (httpd, host, prt):  # no model_port_factory
        caps = _capabilities(host, prt)
        status, payload, _raw = _request(host, prt, "POST", ROUTE, body=_body(),
                                         headers=_console_headers(caps))
    _assert_fixed_refusal(status, payload,
                          serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)


def test_a_get_is_not_a_route(tmp_path):
    """One POST route, declared once. A GET falls through to the static
    handler rather than answering an abstract."""
    with _serving(tmp_path) as (httpd, host, prt):
        status, _payload, _raw = _request(host, prt, "GET", ROUTE)
    assert status == 404


# ============================================================================
# 5.2 — eligibility (ruling 7(a)): editable_paths, and no provider reached
# ============================================================================

def test_a_readable_but_not_editable_subject_is_refused_before_any_provider(tmp_path):
    """Ruling 7(a). `editable_paths` is fed only from sections flagged `owned`
    (`doxbench_scope.py:356-358`), so a brainstorm document this tile can READ is
    not a subject it may distil, and the standing rule — disclosure requires edit
    authority (`doxbench_scope.py:390`) — refuses it before any disclosure."""
    port = _seeded_port()
    status, payload, fake = _post(
        tmp_path, _body(subject_path=READABLE_ONLY_PATH), port=port)
    _assert_abstract_refusal(
        status, payload,
        serve_mod.DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_ELIGIBLE,
        subject=READABLE_ONLY_PATH)
    assert fake.calls == []
    assert fake.dispatched == []
    # The refusal names no digest: the route never read the file, which is what
    # "reaches no provider and makes no disclosure" means at this boundary.
    assert payload["subject_digest"] is None


def test_a_subject_outside_the_scope_entirely_is_refused(tmp_path):
    port = _seeded_port()
    status, payload, fake = _post(
        tmp_path, _body(subject_path=OUT_OF_SCOPE_PATH), port=port)
    _assert_abstract_refusal(
        status, payload,
        serve_mod.DOXBENCH_ABSTRACT_REFUSED_SUBJECT_NOT_ELIGIBLE,
        subject=OUT_OF_SCOPE_PATH)
    assert fake.calls == []


def test_a_traversal_shaped_subject_is_refused(tmp_path):
    port = _seeded_port()
    status, payload, fake = _post(
        tmp_path, _body(subject_path="../../etc/passwd"), port=port)
    assert status in (400, 403)
    assert fake.calls == []
    assert "prose" not in payload


def test_a_foreign_scope_is_refused(tmp_path):
    port = _seeded_port()
    status, payload, fake = _post(
        tmp_path, _body(scope={**SCOPE, "repository": "another-repo"}), port=port)
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_TURN_SCOPE_REFUSED)
    assert fake.calls == []


def test_a_subject_with_no_declared_topics_or_destinations_is_refused_before_dispatch(
        tmp_path):
    """The verifier's base is the snapshot's declared topics and destinations,
    so a subject that declares NEITHER cannot be verified against anything the
    document itself declares — and a request that could only ever end in
    `no-declared-base` is refused BEFORE it spends a provider call."""
    snapshot = copy.deepcopy(_snapshot())
    for document in snapshot["documents"]:
        if document.get("path") == SUBJECT_PATH:
            document["topics"] = []
            document["destinations"] = {}
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, port=port, snapshot=snapshot)
    _assert_abstract_refusal(
        status, payload, doxbench_knowledge.ABSTRACT_REFUSED_NO_DECLARED_BASE)
    assert fake.dispatched == []


# ============================================================================
# the request shape
# ============================================================================

@pytest.mark.parametrize("body", [
    {},
    {"scope": dict(SCOPE)},
    {"scope": dict(SCOPE), "subject_path": SUBJECT_PATH},
    {"scope": dict(SCOPE), "subject_path": "", "model_id": "model-a"},
    {"scope": dict(SCOPE), "subject_path": SUBJECT_PATH, "model_id": ""},
    {"scope": {"repository": "fixture-repo"}, "subject_path": SUBJECT_PATH,
     "model_id": "model-a"},
    {"scope": dict(SCOPE), "subject_path": SUBJECT_PATH, "model_id": "model-a",
     "buffers": []},
    {"scope": dict(SCOPE), "subject_path": SUBJECT_PATH, "model_id": "model-a",
     "context_packet": {"purpose": "chat-turn"}},
])
def test_a_malformed_abstract_request_is_refused_before_any_provider(tmp_path, body):
    """The shape is CLOSED: an abstract request carries exactly a scope, a
    subject path and a model id. A `buffers` or `context_packet` key in
    particular is refused at the wire rather than ignored — this request carries
    no packet, no second buffer and no transcript, and a route that silently
    dropped one would be the smuggling the assembler exists to refuse."""
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, body, port=port)
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_INVALID_ABSTRACT_REQUEST)
    assert payload == serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_INVALID_ABSTRACT_REQUEST)
    assert fake.calls == []


def test_a_body_that_is_not_a_json_object_is_refused(tmp_path):
    port = _seeded_port()
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        conn = http.client.HTTPConnection(host, prt, timeout=10)
        conn.request("POST", ROUTE, body="[]", headers=_console_headers(caps))
        resp = conn.getresponse()
        payload = json.loads(resp.read().decode("utf-8"))
        status = resp.status
        conn.close()
    assert status == 400
    assert payload["ok"] is False
    assert port.calls == []


# ============================================================================
# the model gate
# ============================================================================

def test_a_model_id_absent_from_the_catalog_is_refused(tmp_path):
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, _body(model_id="model-z"), port=port)
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_MODEL_UNAVAILABLE)
    assert fake.dispatched == []


def test_an_unavailable_model_is_refused(tmp_path):
    port = _seeded_port(catalog=_catalog(available=False))
    status, payload, fake = _post(tmp_path, port=port)
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_MODEL_UNAVAILABLE)
    assert fake.dispatched == []


def test_a_catalog_that_raises_is_refused_without_leaking(tmp_path):
    port = FakeWorkbenchModelPort(_catalog(),
                                  catalog_error=RuntimeError("provider boom"))
    status, payload, fake = _post(tmp_path, port=port)
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert "boom" not in json.dumps(payload)


def test_a_provider_that_raises_is_the_fixed_model_failed_refusal(tmp_path):
    port = FakeWorkbenchModelPort(_catalog(),
                                  dispatch_error=RuntimeError("provider boom"))
    status, payload, fake = _post(tmp_path, port=port)
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_MODEL_FAILED)
    assert "boom" not in json.dumps(payload)


def test_a_malformed_provider_payload_is_the_fixed_response_invalid_refusal(tmp_path):
    port = FakeWorkbenchModelPort(_catalog(), dispatch_result={"nope": True})
    status, payload, fake = _post(tmp_path, port=port)
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_RESPONSE_INVALID)


def test_a_proposal_bearing_answer_is_refused(tmp_path):
    """An abstract request is not a conversation and cannot accept a typed
    proposal: nothing on this route may write into a buffer."""
    port = FakeWorkbenchModelPort(_catalog(), dispatch_result={
        "assistant_prose": GROUNDED_PROSE,
        "proposals": [{"target": "document", "base_hash": "0" * 64,
                       "summary": "rewrite", "content": "new"}]})
    status, payload, fake = _post(tmp_path, port=port)
    _assert_fixed_refusal(status, payload, serve_mod.DOXBENCH_ERR_RESPONSE_INVALID)


# ============================================================================
# the request the provider actually sees
# ============================================================================

def test_the_dispatched_envelope_carries_exactly_one_subject_and_no_packet(tmp_path):
    port = _seeded_port()
    status, _payload, fake = _post(tmp_path, port=port)
    assert status == 200
    assert len(fake.dispatched) == 1
    envelope = fake.dispatched[0]
    assert isinstance(envelope, doxbench_turns.AbstractEnvelope)
    assert envelope.subject_path == SUBJECT_PATH
    assert envelope.subject_digest == _saved_digest()
    assert tuple(section.key for section in envelope.sections) == \
        doxbench_turns.ABSTRACT_SECTION_ORDER
    rendered = envelope.rendered()
    # The SERVED SAVED bytes, and nothing else: no outline buffer, no second
    # document, no transcript, no human message.
    assert _saved_content() in rendered
    assert READABLE_ONLY_PATH not in rendered


def test_the_subject_bytes_are_the_served_saved_content(tmp_path):
    """The subject is the SAVED file — an unsaved buffer's text never leaves the
    browser, and there is no request field it could arrive in."""
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, port=port)
    assert status == 200
    assert payload["subject_digest"] == _saved_digest()
    assert fake.dispatched[0].subject_digest == _saved_digest()


# ============================================================================
# 5.6 — the response echoes the subject path and digest
# ============================================================================

def test_a_verified_abstract_echoes_its_subject_path_and_digest(tmp_path):
    port = _seeded_port()
    status, payload, fake = _post(tmp_path, port=port)
    assert status == 200
    assert payload["subject_path"] == SUBJECT_PATH
    assert payload["subject_digest"] == _saved_digest()
    assert payload["prose"] == GROUNDED_PROSE
    assert payload["model_id"] == "model-a"
    assert payload["caption_state"] == doxbench_knowledge.CAPTION_MODEL_DERIVED
    assert isinstance(payload["generation"], int) and payload["generation"] >= 0
    assert payload["ok"] is True
    assert set(payload) == {"ok", "subject_path", "subject_digest", "model_id",
                            "prose", "caption_state", "generation",
                            "wait_bound_seconds"}


def test_the_response_states_the_adapters_own_declared_bound(tmp_path):
    """Task 7.3's server half: the wait the region states is the ADAPTER'S OWN
    declared timeout, never `MAX_ADAPTER_TIMEOUT_SECONDS`, which is a validated
    ceiling and not a prediction."""
    port = _seeded_port(timeout_seconds=60.0)
    status, payload, _fake = _post(tmp_path, port=port)
    assert status == 200
    assert payload["wait_bound_seconds"] == 60.0
    assert payload["wait_bound_seconds"] != doxbench_model.MAX_ADAPTER_TIMEOUT_SECONDS


# ============================================================================
# verification: a refusal renders nothing
# ============================================================================

def test_the_house_fakes_constant_answer_is_refused_as_unverified(tmp_path):
    """N5, pinned rather than assumed: `FakeWorkbenchModelPort`'s default
    "fake grounded answer" names neither the subject nor a declared subject of
    it, so the verifier refuses it and the route renders nothing."""
    port = FakeWorkbenchModelPort(_catalog())
    status, payload, fake = _post(tmp_path, port=port)
    _assert_abstract_refusal(
        status, payload, doxbench_knowledge.ABSTRACT_REFUSED_SUBJECT_NOT_NAMED)
    assert "fake grounded answer" not in json.dumps(payload)
    assert fake.calls.count("dispatch") == 1


def test_an_answer_naming_a_foreign_path_is_refused(tmp_path):
    port = _seeded_port(
        GROUNDED_PROSE + " See also ideation/brainstorm/dtn-register.md.")
    status, payload, _fake = _post(tmp_path, port=port)
    _assert_abstract_refusal(
        status, payload, doxbench_knowledge.ABSTRACT_REFUSED_FOREIGN_PATH)
    # The reason NAMES the foreign path — that is the point of it: the reader
    # is told which path made the answer refusable. It renders no abstract.
    assert "dtn-register" in payload["reason"]


def test_an_answer_mentioning_no_declared_subject_is_refused(tmp_path):
    port = _seeded_port("README.md describes something, in general terms.")
    status, payload, _fake = _post(tmp_path, port=port)
    _assert_abstract_refusal(
        status, payload, doxbench_knowledge.ABSTRACT_REFUSED_COVERAGE)


def test_an_empty_answer_is_refused(tmp_path):
    port = _seeded_port("   ")
    status, payload, _fake = _post(tmp_path, port=port)
    _assert_abstract_refusal(
        status, payload, doxbench_knowledge.ABSTRACT_REFUSED_EMPTY)


def test_an_over_long_answer_is_refused_in_full_and_never_trimmed(tmp_path):
    """`validate_abstract_prose` refuses over `MAX_ABSTRACT_PROSE_BYTES`; text
    cut to fit the 280px region is text no model wrote and no verifier
    checked."""
    long_prose = GROUNDED_PROSE + (" the ideation-governance queue." *
                                   doxbench_turns.MAX_ABSTRACT_PROSE_BYTES)
    port = _seeded_port(long_prose)
    status, payload, _fake = _post(tmp_path, port=port)
    _assert_abstract_refusal(
        status, payload, serve_mod.DOXBENCH_ABSTRACT_REFUSED_PROSE_BYTES)
    assert long_prose[:40] not in json.dumps(payload)


# ============================================================================
# 5.3 at the route: one store per served process, keyed by (path, digest)
# ============================================================================

def test_the_served_process_binds_its_own_abstract_store(tmp_path):
    with _serving(tmp_path) as (httpd, host, prt):
        handler = _handler_class(httpd)
        assert isinstance(handler.abstract_store, store_mod.AbstractStore)
        assert handler.abstract_store is not handler.turn_store
    with _serving(tmp_path) as (other, host, prt):
        assert _handler_class(other).abstract_store is not handler.abstract_store


def test_an_identical_request_replays_without_a_second_dispatch(tmp_path):
    port = _seeded_port()
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        first = _request(host, prt, "POST", ROUTE, body=_body(),
                         headers=_console_headers(caps))
        second = _request(host, prt, "POST", ROUTE, body=_body(),
                          headers=_console_headers(caps))
    assert first[0] == second[0] == 200
    assert first[1] == second[1]          # byte-identical replay
    assert port.calls.count("dispatch") == 1


def test_a_refused_generation_is_not_cached(tmp_path):
    """A refusal is not an answer, so the key is FREED: the re-generate control
    must be able to try again against unchanged content."""
    port = _ScriptedPort(["fake grounded answer", GROUNDED_PROSE])
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        first_status, first, _raw = _request(host, prt, "POST", ROUTE, body=_body(),
                                             headers=_console_headers(caps))
        second_status, second, _raw = _request(host, prt, "POST", ROUTE, body=_body(),
                                               headers=_console_headers(caps))
    assert first["refused"] == doxbench_knowledge.ABSTRACT_REFUSED_SUBJECT_NOT_NAMED
    assert second_status == 200
    assert second["prose"] == GROUNDED_PROSE
    assert port.calls.count("dispatch") == 2


# ============================================================================
# 5.4 — abstract churn never evicts the chat turn store's records
# ============================================================================

def test_abstract_churn_never_evicts_the_served_processes_chat_records(tmp_path):
    """TASK 5.4 at the ROUTE, asserted against the chat `TurnStore`'s OWN
    contents: the served process's two stores are separate instances with
    separate bounds, so churning the abstract store past its bound — while the
    route itself is serving — leaves every chat idempotency record replayable."""
    port = _seeded_port()
    chat_key = ScopeKey(repository="fixture-repo", ref="main",
                        tile_kind="staged", tile_id="ideation-governance")
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        handler = _handler_class(httpd)

        handler.turn_store.reserve(chat_key, "turn-0001", "d" * 64)
        handler.turn_store.complete(chat_key, "turn-0001",
                                    {"status": 200, "body": {"turn": "kept"}},
                                    size_bytes=128)

        for index in range(store_mod.MAX_ABSTRACT_ENTRIES * 3):
            key = store_mod.AbstractKey(
                subject_path=f"ideation/staging/churn-{index:04d}/README.md",
                content_digest=f"{index:064d}")
            handler.abstract_store.reserve(key)
            handler.abstract_store.complete(
                key, {"status": 200, "body": {"n": index}}, size_bytes=256)

        status, payload, _raw = _request(host, prt, "POST", ROUTE, body=_body(),
                                         headers=_console_headers(caps))
        assert status == 200
        assert payload["subject_path"] == SUBJECT_PATH

        record = handler.turn_store.snapshot(chat_key, "turn-0001")
        assert record is not None, "abstract churn evicted a chat turn record"
        assert record.validated_result == {"status": 200, "body": {"turn": "kept"}}
        assert handler.turn_store.reserve(
            chat_key, "turn-0001", "d" * 64).should_dispatch is False


# ============================================================================
# the snapshot is untouched (§6's route-side statement)
# ============================================================================

def test_generating_an_abstract_writes_nothing(tmp_path):
    """No corpus document, no snapshot field, no gate artifact: the served
    checkout is byte-identical after a generation."""
    before = {path: path.read_bytes()
              for path in sorted(BASE_REPO.rglob("*")) if path.is_file()}
    status, _payload, _fake = _post(tmp_path)
    assert status == 200
    after = {path: path.read_bytes()
             for path in sorted(BASE_REPO.rglob("*")) if path.is_file()}
    assert before == after
