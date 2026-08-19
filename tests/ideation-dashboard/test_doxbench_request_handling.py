"""T024 (change 010-doxbench-editor-chat): route-specific 1 MiB request
handling, fixed doxBench error envelopes, and injected model-port
configuration in `serve.py` — a DELIBERATELY SCOPED slice, tested in
isolation from the routes that will eventually consume it.

This file never dispatches to a doxBench route. `GET /workbench/model-catalog`
and `POST /actions/workbench/chat-turn` landed later, under T050/T051, and are
covered by `test_doxbench_routes.py`; the T024 surface tested here stays
deliberately reachable-free, exercised at helper level only. It exercises:

  A. the new ROUTE-SPECIFIC bounded JSON body reader
     (`DashboardHandler._read_bounded_json_body`) directly, by calling it
     unbound over a small stand-in `self` carrying just `.headers`/`.rfile` —
     the same technique `test_session_snapshot.py` uses for
     `_session_pull_requests`/`_session_pull_requests` — and proves the
     EXISTING global `_MAX_BODY_BYTES` cap and an existing route's behaviour
     are untouched via a REAL ephemeral `ThreadingHTTPServer` over
     `serve_mod.build_server(...)`;
  B. the new pure, module-level doxBench fixed-error catalog and emitter
     (`DOXBENCH_ERROR_CATALOG` / `doxbench_error_body`), which need no server
     at all;
  C. the new `model_port_factory` injection seam on `build_server`/
     `DashboardHandler`, over a REAL server built by `build_server(...)`, with
     the handler class's own methods called directly (again mirroring
     `test_session_snapshot.py`'s `_session_pull_requests` idiom) so no test
     ever calls a method ON the injected port itself.

Follows the house style of `test_renderer.py` / `test_edit_action.py` /
`test_session_snapshot.py`: real ephemeral `ThreadingHTTPServer`s, injected
fakes, `from conftest import ...`.
"""

from __future__ import annotations

import http.client
import io
import json
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit

from ideation_dashboard import serve as serve_mod
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"


def _snapshot():
    return generate_snapshot(
        BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


# ============================================================================
# shared HTTP harness (mirrors test_edit_action.py's `_serving`/`_request`)
# ============================================================================

@contextmanager
def _serving(tmp_path, *, actor="brett", checkout_root=None,
            model_port_factory=None, snapshot=None):
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot or _snapshot()), encoding="utf-8")
    httpd = serve_mod.build_server(
        WEB,
        snap_path,
        checkout_root if checkout_root is not None else BASE_REPO,
        head=PINNED_REVISION,
        actor=actor,
        model_port_factory=model_port_factory,
    )
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
    """The bound `DashboardHandler` subclass a server was built with — the
    same unwrap `test_session_snapshot.py` uses, since `build_server` hands
    `ThreadingHTTPServer` a `functools.partial(bound, directory=...)`."""
    return getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)


def _request(host, port, method, path, *, body=None, headers=None):
    conn = http.client.HTTPConnection(host, port, timeout=5)
    raw = None if body is None else json.dumps(body)
    conn.request(method, path, body=raw, headers=headers or {})
    resp = conn.getresponse()
    payload = json.loads(resp.read().decode("utf-8") or "{}")
    conn.close()
    return resp.status, payload


def _capabilities(host, port):
    status, payload = _request(host, port, "GET", "/capabilities")
    assert status == 200
    return payload


def _console_headers(caps):
    return {
        "Content-Type": "application/json",
        "X-XF-Console-Token": caps["console_token"],
    }


# ============================================================================
# a stand-in `self` for the bounded reader — a plain object carrying only the
# two attributes `_read_bounded_json_body` touches, so every case below is a
# pure unit test with no socket, no server, and no route.
# ============================================================================

class _RecordingRFile(io.BytesIO):
    """Wraps `io.BytesIO` to record every `n` a caller asks `.read(n)` for, so
    a test can prove a lying `Content-Length` never drives an unbounded read."""

    def __init__(self, data: bytes) -> None:
        super().__init__(data)
        self.read_sizes: list[int] = []

    def read(self, size=-1):  # noqa: A003 - matches io.BytesIO.read's signature
        self.read_sizes.append(size)
        return super().read(size)


class _FakeRequest:
    """Everything `_read_bounded_json_body` reads from `self`: `.headers`
    (dict-like, `.get`) and `.rfile` (file-like, `.read`)."""

    def __init__(self, headers: dict, body: bytes) -> None:
        self.headers = headers
        self.rfile = _RecordingRFile(body)


def _bounded_call(headers, body, *, max_bytes, dimension="request_body_bytes"):
    fake = _FakeRequest(headers, body)
    payload, refusal = serve_mod.DashboardHandler._read_bounded_json_body(
        fake, max_bytes=max_bytes, dimension=dimension)
    return payload, refusal, fake


def _json_body_of_exact_bytes(target_bytes: int, filler: str = "x") -> bytes:
    """Build `{"a":"...filler..."}` as UTF-8 bytes of EXACTLY `target_bytes`.
    A single-byte ASCII filler makes byte count == character count (the plain
    boundary cases); a multi-byte `filler` (each unit contributing
    `len(filler.encode())` bytes) proves the boundary is measured on ENCODED
    BYTES, not decoded characters, because the resulting character count is a
    fraction of the byte count."""
    prefix = b'{"a":"'
    suffix = b'"}'
    filler_bytes = filler.encode("utf-8")
    overhead = len(prefix) + len(suffix)
    remaining = target_bytes - overhead
    assert remaining >= 0 and remaining % len(filler_bytes) == 0, (
        "target_bytes must be exactly reachable with whole filler units")
    body = prefix + (filler_bytes * (remaining // len(filler_bytes))) + suffix
    assert len(body) == target_bytes
    return body


def _headers_for(body: bytes) -> dict:
    return {"Content-Length": str(len(body))}


# ============================================================================
# A. the route-specific 1 MiB bounded reader
# ============================================================================

def test_doxbench_max_request_bytes_is_public_exact_and_not_the_global_cap():
    assert serve_mod.DOXBENCH_MAX_REQUEST_BYTES == 1_048_576
    assert serve_mod._MAX_BODY_BYTES == 65_536
    assert serve_mod.DOXBENCH_MAX_REQUEST_BYTES != serve_mod._MAX_BODY_BYTES


def test_existing_action_route_still_enforces_the_global_65kb_cap_unchanged(tmp_path):
    """Comparison point (hard boundary): T024 must not widen `_MAX_BODY_BYTES`
    or change `_read_json_body`'s behaviour for any EXISTING route. An
    over-65-KiB body to `/actions/edit` (already covered by
    test_edit_action.py) refuses exactly as it does today: 400 `invalid_body`,
    because `_read_json_body` returns bare `None` for ANY malformation,
    including "too large", and `_edit_request_fields(None)` reports the fixed
    `JSON_OBJECT_BODY_REQUIRED` message.

    (T104 F5-6 later carved out ONE gate verb — `first-edit`, the governed
    Save, whose body legitimately carries a full document — onto the widened
    route-specific reader; see section D below. That carve-out changes
    nothing this test pins: `/actions/edit` and every other verb keep the
    tiny global cap.)"""
    with _serving(tmp_path) as (httpd, host, port):
        caps = _capabilities(host, port)
        big_body = {
            "path": "ideation/staging/ideation-governance/README.md",
            "repository": "fixture-repo",
            "ref": "main",
            "padding": "x" * (serve_mod._MAX_BODY_BYTES + 1),
        }
        status, payload = _request(
            host, port, "POST", "/actions/edit", body=big_body,
            headers=_console_headers(caps))
    assert status == 400
    assert payload == {"ok": False, "error": "invalid_body",
                        "message": serve_mod.JSON_OBJECT_BODY_REQUIRED}


def test_the_tiny_reader_drains_an_over_cap_body_before_refusing():
    """T104 F5/F8 follow-through — the carried '65kb test' flake, closed at
    its root. `_read_json_body` used to return bare None for an over-cap body
    while leaving EVERY byte of it unread; the handler then wrote the 400 and
    closed a socket whose client was still mid-body, and the kernel's reset
    could destroy the queued refusal before the client read it — the refusal
    raced its own transport, intermittently, under load. The reader now
    DRAINS the refused body first: fully for anything a real client sends
    (bounded by the shared `_MAX_REFUSED_DRAIN_BYTES`, W-5/W-6), in small
    chunks so the drain never buffers what it refuses to parse."""
    body = b"x" * (serve_mod._MAX_BODY_BYTES + 200)
    fake = _FakeRequest(_headers_for(body), body)
    result = serve_mod.DashboardHandler._read_json_body(fake)
    assert result is None
    assert fake.rfile.read_sizes, "the over-cap body was left entirely unread"
    assert sum(fake.rfile.read_sizes) >= len(body), \
        "the drain stopped short of the declared body"
    assert all(n <= serve_mod._MAX_BODY_BYTES for n in fake.rfile.read_sizes), \
        "the drain buffered more per read than the cap it refused"
    # and the drain itself is bounded: a lying gigabyte Content-Length is
    # never read to completion
    liar = _FakeRequest({"Content-Length": str(10**9)}, b"x" * 1024)
    assert serve_mod.DashboardHandler._read_json_body(liar) is None
    assert sum(liar.rfile.read_sizes) <= serve_mod._MAX_REFUSED_DRAIN_BYTES


def test_the_bounded_reader_drains_a_refused_body_with_the_same_posture():
    """W-6 (wave re-review): the bounded reader used to pull only
    `max_bytes + 1` of an over-cap body and abandon the remainder on the
    socket — so on the chat-turn route AND on `first-edit` (the route the
    F5-6 carve-out had just widened) the measured 413 could still be
    destroyed by the close-with-unread reset. Both readers now share one
    drain: chunked, and bounded by `_MAX_REFUSED_DRAIN_BYTES` rather than a
    per-reader band."""
    declared = serve_mod.DOXBENCH_MAX_REQUEST_BYTES + 200_000
    body = b"x" * declared
    payload, refusal, fake = _bounded_call(
        _headers_for(body), body, max_bytes=serve_mod.DOXBENCH_MAX_REQUEST_BYTES)
    assert payload is None
    assert refusal == {"dimension": "request_body_bytes",
                       "measured": declared,
                       "maximum": serve_mod.DOXBENCH_MAX_REQUEST_BYTES}
    assert sum(fake.rfile.read_sizes) >= declared, \
        "the refused body was left partially unread on the socket"
    assert all(n <= serve_mod._MAX_BODY_BYTES for n in fake.rfile.read_sizes)
    # a lying declaration past the shared ceiling stays bounded
    liar = _FakeRequest({"Content-Length": str(10**9)}, b"x" * 1024)
    _p, _r = serve_mod.DashboardHandler._read_bounded_json_body(
        liar, max_bytes=serve_mod.DOXBENCH_MAX_REQUEST_BYTES,
        dimension="request_body_bytes")
    assert sum(liar.rfile.read_sizes) <= serve_mod._MAX_REFUSED_DRAIN_BYTES


def test_a_stalled_over_cap_body_is_bounded_by_the_socket_timeout(tmp_path):
    """W-5 (wave re-review): the drain without a socket timeout traded an
    instant 400 for an UNBOUNDED block — a client declaring an over-cap body
    and then going silent pinned a handler thread and its connection forever
    (no timeout existed anywhere on this server). `DashboardHandler.timeout`
    now bounds every socket read, so the stalled drain raises and the thread
    exits. Driven with a real server, a real half-sent body, and a shrunken
    timeout so the test proves the BOUND, not the default's exact value."""
    import socket as socket_mod
    import time as time_mod
    assert serve_mod.DashboardHandler.timeout is not None
    with _serving(tmp_path) as (httpd, host, port):
        handler = _handler_class(httpd)
        original = handler.timeout
        handler.timeout = 0.4
        try:
            caps = _capabilities(host, port)
            declared = serve_mod._MAX_BODY_BYTES + 10_000
            raw = socket_mod.create_connection((host, port), timeout=5)
            try:
                raw.sendall(
                    b"POST /actions/gate/ratify HTTP/1.1\r\n"
                    b"Host: local\r\n"
                    b"Content-Type: application/json\r\n"
                    + f"X-XF-Console-Token: {caps['console_token']}\r\n".encode()
                    + f"Content-Length: {declared}\r\n\r\n".encode()
                    + b"x" * 1024)  # ...and then silence
                started = time_mod.monotonic()
                raw.settimeout(10)
                answer = b""
                try:
                    while True:
                        got = raw.recv(4096)
                        if not got:
                            break
                        answer += got
                except OSError:
                    pass
                elapsed = time_mod.monotonic() - started
            finally:
                raw.close()
            # the connection ENDED promptly (refusal delivered or reset) —
            # never a thread parked in read() for the life of the process
            assert elapsed < 5, f"stalled body held the connection {elapsed:.1f}s"
        finally:
            handler.timeout = original


def test_bounded_reader_accepts_exactly_the_boundary_and_refuses_one_byte_over():
    at_max = _json_body_of_exact_bytes(serve_mod.DOXBENCH_MAX_REQUEST_BYTES)
    payload, refusal, _ = _bounded_call(
        _headers_for(at_max), at_max, max_bytes=serve_mod.DOXBENCH_MAX_REQUEST_BYTES)
    assert refusal is None
    assert payload == {"a": "x" * (len(at_max) - 8)}

    over_max = _json_body_of_exact_bytes(serve_mod.DOXBENCH_MAX_REQUEST_BYTES + 1)
    payload, refusal, _ = _bounded_call(
        _headers_for(over_max), over_max, max_bytes=serve_mod.DOXBENCH_MAX_REQUEST_BYTES)
    assert payload is None
    assert refusal == {
        "dimension": "request_body_bytes",
        "measured": serve_mod.DOXBENCH_MAX_REQUEST_BYTES + 1,
        "maximum": serve_mod.DOXBENCH_MAX_REQUEST_BYTES,
    }


def test_bounded_reader_is_parameterised_per_call_site_not_a_second_global():
    """Two DIFFERENT calls with two DIFFERENT `max_bytes` prove the bound is
    an explicit argument (what a future route declares for itself), not a
    second module-level constant standing in for `_MAX_BODY_BYTES`."""
    small_ok = _json_body_of_exact_bytes(20)
    payload, refusal, _ = _bounded_call(_headers_for(small_ok), small_ok, max_bytes=20)
    assert refusal is None and payload is not None

    small_over = _json_body_of_exact_bytes(21)
    payload, refusal, _ = _bounded_call(
        _headers_for(small_over), small_over, max_bytes=20, dimension="tiny_dimension")
    assert payload is None
    assert refusal == {"dimension": "tiny_dimension", "measured": 21, "maximum": 20}


def test_multibyte_utf8_body_is_measured_in_bytes_not_code_points():
    """A body whose CHARACTER count is well under the bound but whose BYTE
    count is one over it must be REFUSED — a character-counting bug would
    incorrectly accept it (research R4's exact-byte discipline applies to
    request bounds too, not only content identity)."""
    max_bytes = serve_mod.DOXBENCH_MAX_REQUEST_BYTES
    target_total = max_bytes + 1
    overhead = len(b'{"a":"') + len(b'"}')
    remaining = target_total - overhead  # bytes available for the filler content
    # (remaining - 1) is even: pack it as N two-byte 'e-acute' characters plus
    # one trailing ASCII byte, so the encoded content is EXACTLY `remaining`
    # bytes while its CHARACTER count (n + 1) is well under the byte bound.
    n = (remaining - 1) // 2
    content = ("é" * n) + "x"
    body = b'{"a":"' + content.encode("utf-8") + b'"}'
    assert len(body) == target_total
    assert len(content) < max_bytes  # character count well under the byte bound
    payload, refusal, _ = _bounded_call(_headers_for(body), body, max_bytes=max_bytes)
    assert payload is None
    assert refusal == {"dimension": "request_body_bytes",
                        "measured": target_total, "maximum": max_bytes}

    # And vice versa: a body composed ENTIRELY of multi-byte characters whose
    # BYTE count sits EXACTLY at the bound (character count a fraction of it)
    # is ACCEPTED — proving acceptance is also decided on bytes, not on the
    # (much smaller) character count.
    at_max_multibyte = _json_body_of_exact_bytes(max_bytes, filler="é")
    payload, refusal, _ = _bounded_call(
        _headers_for(at_max_multibyte), at_max_multibyte, max_bytes=max_bytes)
    assert refusal is None
    assert payload is not None


@pytest.mark.parametrize("headers,body", [
    ({}, b'{"a": 1}'),                                    # missing Content-Length
    ({"Content-Length": "not-a-number"}, b'{"a": 1}'),    # unparseable Content-Length
    ({"Content-Length": "-5"}, b'{"a": 1}'),               # negative Content-Length
])
def test_bounded_reader_refuses_missing_or_unparseable_length_without_measurement(
        headers, body):
    payload, refusal, fake = _bounded_call(headers, body, max_bytes=1024)
    assert payload is None
    assert refusal is None
    assert "SECRET" not in json.dumps({"payload": payload, "refusal": refusal})


def test_bounded_reader_refuses_a_short_read_without_measurement():
    declared_headers = {"Content-Length": "40"}
    actually_sent = b'{"a": "SECRET_PARTIAL_BODY"'  # fewer than 40 bytes, no closing brace
    payload, refusal, fake = _bounded_call(declared_headers, actually_sent, max_bytes=1024)
    assert payload is None
    assert refusal is None
    assert "SECRET_PARTIAL_BODY" not in json.dumps({"payload": payload, "refusal": refusal})


def test_bounded_reader_refuses_invalid_utf8_without_measurement():
    body = b'{"a": "\xff\xfe"}'
    payload, refusal, _ = _bounded_call(_headers_for(body), body, max_bytes=1024)
    assert payload is None
    assert refusal is None


def test_bounded_reader_refuses_non_json_without_measurement():
    body = b"not json at all, contains SECRET_TOKEN_TEXT"
    payload, refusal, _ = _bounded_call(_headers_for(body), body, max_bytes=1024)
    assert payload is None
    assert refusal is None
    assert "SECRET_TOKEN_TEXT" not in json.dumps({"payload": payload, "refusal": refusal})


@pytest.mark.parametrize("literal", [b"[1, 2, 3]", b'"just a string"', b"42", b"null", b"true"])
def test_bounded_reader_refuses_a_json_non_object_without_measurement(literal):
    payload, refusal, _ = _bounded_call(_headers_for(literal), literal, max_bytes=1024)
    assert payload is None
    assert refusal is None


def test_bounded_reader_never_echoes_request_bytes_in_any_refusal():
    """Every malformation case above, swept together: none of the refusal
    verdicts may contain any byte of the request that produced them."""
    secret = "REQUEST_DERIVED_SECRET_VALUE"
    cases = [
        ({}, secret.encode()),
        ({"Content-Length": "abc"}, secret.encode()),
        ({"Content-Length": "999"}, secret.encode()),  # short read
        ({"Content-Length": str(len(secret.encode()))}, b"\xff" + secret.encode()[:-1]),
        ({"Content-Length": str(len(secret.encode()))}, secret.encode()),  # non-JSON
    ]
    for headers, body in cases:
        payload, refusal, _ = _bounded_call(headers, body, max_bytes=1024)
        assert payload is None
        blob = json.dumps({"payload": payload, "refusal": refusal})
        assert secret not in blob


def test_lying_content_length_never_drives_an_unbounded_read():
    """A declared `Content-Length` far beyond both the bound and the actual
    bytes present must never cause a read attempt bigger than
    `max_bytes + 1` — the flood-protection half of "never trust a lying
    Content-Length" (R7)."""
    max_bytes = serve_mod.DOXBENCH_MAX_REQUEST_BYTES
    fake = _FakeRequest({"Content-Length": "5000000000"}, b"x" * 10)
    payload, refusal = serve_mod.DashboardHandler._read_bounded_json_body(
        fake, max_bytes=max_bytes, dimension="request_body_bytes")
    assert payload is None
    assert refusal == {"dimension": "request_body_bytes",
                        "measured": 5_000_000_000, "maximum": max_bytes}
    assert fake.rfile.read_sizes
    assert all(n <= max_bytes + 1 for n in fake.rfile.read_sizes)


# ============================================================================
# B. fixed doxBench error envelopes
# ============================================================================

# The FOUR codes T024 landed, each spelled VERBATIM in the planning contracts
# (contracts/model-catalog.md's fixed-failure table and contracts/chat-turn.md's
# fixed-failure example).
_PLANNING_CONTRACT_CODES = {
    "request_limit_exceeded",
    "model_capability_unavailable",
    "catalog_unavailable",
    "console_required",
}

# The ONE route-era code that is also spelled VERBATIM in the planning
# contracts (contracts/chat-turn.md, "Idempotency").
_ROUTE_VERBATIM_CODES = {
    "turn_id_conflict",
}

# The FIVE route-era spellings the planning contracts do NOT pin. Each answers
# a precondition contracts/chat-turn.md numbers but leaves unnamed, so the
# spelling and status are T050/T051 judgement calls recorded in that change's
# ledger. This set is deliberately CLOSED: a new code may not appear here
# without its own recorded grounding.
_ROUTE_JUDGEMENT_CALL_CODES = {
    "turn_in_flight",
    "turn_scope_refused",
    "content_identity_mismatch",
    "model_unavailable",
    "invalid_turn_request",
}

# PIN EVOLUTION (T051 dispatch arm). The THREE provider-outcome codes the
# dispatch arm can surface -- spelled by doxbench_model's CLOSED
# `DISPATCH_FAILURE_CODES` (whose fourth member, `model_unavailable`, was
# already grounded above) and asserted equal to it below, so the two
# spellings can never drift. Statuses are the arm's recorded judgement
# calls: 504 deadline, 502 adapter failure, 502 unvalidatable response.
_DISPATCH_OUTCOME_CODES = {
    "model_timeout",
    "model_failed",
    "response_invalid",
}

# PIN EVOLUTION (add-doxbench-editing-phase-b §10, and the adversarial review
# that required it). TWO packet-era spellings, each a recorded judgement call
# for a condition that has no code in the planning contracts because the
# planning contracts predate the bounded context packet:
#
#   * `context_packet_bound_exceeded` (409) replaces the misuse of
#     `request_limit_exceeded` for a bound the SERVER's own selection blew.
#     413 with "the request exceeds the allowed size for this route" was false
#     twice over — the request was a few hundred bytes, and the oversize was
#     server-selected evidence — and un-actionable, because it refused every
#     turn on that tile forever. Evidence is now fitted by selecting less, so
#     this code answers only the case the session's own THREADS exceed the
#     bound alone, which a human can act on by compacting the thread.
#   * `context_packet_invalid` (500) answers a packet that failed its own
#     purpose/scope/expiry revalidation twice, which no request the caller
#     could send would fix.
#
# The released failure envelope's `error` is a free-form pattern string, not an
# enum, so neither needed a contract change. This set stays CLOSED for the same
# reason the others do.
_PACKET_CODES = {
    "context_packet_invalid",
    "context_packet_bound_exceeded",
}

_ALL_DOXBENCH_CODES = (
    _PLANNING_CONTRACT_CODES | _ROUTE_VERBATIM_CODES
    | _ROUTE_JUDGEMENT_CALL_CODES | _DISPATCH_OUTCOME_CODES | _PACKET_CODES
)


def test_the_dispatch_outcome_codes_are_spelled_by_doxbench_models_closed_set():
    from ideation_dashboard import doxbench_model as model_mod
    assert (_DISPATCH_OUTCOME_CODES | {"model_unavailable"}
            == set(model_mod.DISPATCH_FAILURE_CODES))


def test_doxbench_error_catalog_has_exactly_the_grounded_code_set():
    """The catalog stays a CLOSED set. T024 pinned four verbatim planning-contract
    codes; T050/T051 added one further verbatim code and five recorded
    judgement-call spellings; the T051 dispatch arm added the three
    provider-outcome codes doxbench_model's own closed set spells. Anything
    else appearing here is an ungrounded invention and must fail this
    assertion."""
    assert set(serve_mod.DOXBENCH_ERROR_CATALOG) == _ALL_DOXBENCH_CODES
    for code, (status, message) in serve_mod.DOXBENCH_ERROR_CATALOG.items():
        assert isinstance(status, int)
        assert isinstance(message, str) and message


def test_the_four_t024_codes_are_still_spelled_verbatim_from_the_contracts():
    """T024's original guard, retained unchanged in substance: the four codes it
    landed are still present and still spelled exactly as the planning contracts
    spell them."""
    assert _PLANNING_CONTRACT_CODES <= set(serve_mod.DOXBENCH_ERROR_CATALOG)


def test_doxbench_error_messages_are_fixed_module_level_constants():
    catalog = serve_mod.DOXBENCH_ERROR_CATALOG
    assert catalog[serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED][1] is (
        serve_mod._DOXBENCH_MSG_REQUEST_LIMIT_EXCEEDED)
    assert catalog[serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE][1] is (
        serve_mod._DOXBENCH_MSG_MODEL_CAPABILITY_UNAVAILABLE)
    assert catalog[serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE][1] is (
        serve_mod._DOXBENCH_MSG_CATALOG_UNAVAILABLE)
    assert catalog[serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED][1] is (
        serve_mod._DOXBENCH_MSG_CONSOLE_REQUIRED)


def test_doxbench_error_body_keys_are_a_fixed_allowlist():
    for code in serve_mod.DOXBENCH_ERROR_CATALOG:
        body = serve_mod.doxbench_error_body(code)
        assert set(body) <= {"ok", "error", "message", "limit"}
        assert body["ok"] is False
        assert body["error"] == code
        assert body["message"] == serve_mod.DOXBENCH_ERROR_CATALOG[code][1]


def test_doxbench_error_body_never_carries_schema_version_or_kind():
    # Deliberate, recorded deferral: the schema-versioned envelope belongs to
    # the RELEASED openxFactory catalog/turn schemas (blocked on T005-T008,
    # T014, T021, and OpenSpec items 2.1/2.5) and is not this ad hoc surface's
    # to invent.
    for code in serve_mod.DOXBENCH_ERROR_CATALOG:
        body = serve_mod.doxbench_error_body(
            code, limit={"dimension": "x", "measured": 1, "maximum": 1})
        assert "schema_version" not in body
        assert "kind" not in body


def test_limit_block_carries_only_a_fixed_dimension_and_two_integers():
    body = serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
        limit={"dimension": "request_body_bytes", "measured": 999, "maximum": 500})
    assert body["limit"] == {"dimension": "request_body_bytes",
                              "measured": 999, "maximum": 500}
    assert set(body["limit"]) == {"dimension", "measured", "maximum"}
    assert isinstance(body["limit"]["dimension"], str)
    assert isinstance(body["limit"]["measured"], int)
    assert isinstance(body["limit"]["maximum"], int)


def test_only_the_limit_BEARING_codes_ever_carry_a_limit_block():
    """RE-PINNED (add-doxbench-editing-phase-b §10). The rule was never "one
    code"; it was "only a DIMENSION-BEARING refusal carries a dimension", and
    for a long time exactly one refusal was dimension-bearing. The packet's
    bound refusal is the second, and it names its measured dimension for the
    same reason the first does. The set is asserted to be exactly those two, so
    a third cannot appear unnoticed."""
    assert serve_mod.DOXBENCH_LIMIT_BEARING_CODES == {
        serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED,
        serve_mod.DOXBENCH_ERR_CONTEXT_PACKET_BOUND_EXCEEDED,
    }
    limit = {"dimension": "request_body_bytes", "measured": 1, "maximum": 1}
    for code in serve_mod.DOXBENCH_ERROR_CATALOG:
        body = serve_mod.doxbench_error_body(code, limit=limit)
        if code in serve_mod.DOXBENCH_LIMIT_BEARING_CODES:
            assert "limit" in body
        else:
            assert "limit" not in body


def test_limit_block_cannot_be_used_to_splice_extra_request_derived_fields():
    injected = {"dimension": "request_body_bytes", "measured": 1, "maximum": 1,
                "leaked_request_text": "SHOULD_NEVER_APPEAR"}
    body = serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED, limit=injected)
    assert set(body["limit"]) == {"dimension", "measured", "maximum"}
    assert "leaked_request_text" not in json.dumps(body)
    assert "SHOULD_NEVER_APPEAR" not in json.dumps(body)


def test_bounded_reader_refusal_composes_directly_with_the_emitter():
    """End-to-end (still no route): the reader's measured verdict feeds the
    emitter's `limit` argument without any reshaping at a call site."""
    max_bytes = 100
    body = _json_body_of_exact_bytes(max_bytes + 1)
    payload, refusal, _ = _bounded_call(
        _headers_for(body), body, max_bytes=max_bytes, dimension="request_body_bytes")
    assert payload is None
    envelope = serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED, limit=refusal)
    assert envelope == {
        "ok": False,
        "error": "request_limit_exceeded",
        "message": serve_mod._DOXBENCH_MSG_REQUEST_LIMIT_EXCEEDED,
        "limit": {"dimension": "request_body_bytes", "measured": max_bytes + 1,
                  "maximum": max_bytes},
    }


# ============================================================================
# C. injected model-port configuration
# ============================================================================

class _RecordingPort:
    """A fake `WorkbenchModelPort` stand-in that records every attribute
    lookup. T024's own seam is DUCK-TYPED and never reads an attribute or
    method on a declared port, so a plain recorder is all a test needs to prove
    nothing on the port is ever touched — deliberately independent of the
    `WorkbenchModelPort` protocol T020 later landed in `doxbench_model.py`."""

    def __init__(self) -> None:
        self.accessed: list[str] = []

    def __getattr__(self, name):
        self.accessed.append(name)
        return lambda *a, **k: None


def test_build_server_accepts_and_binds_model_port_factory(tmp_path):
    port = _RecordingPort()
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, port_num):
        handler = _handler_class(httpd)
        assert handler.model_port_factory is not None
        resolved = handler._workbench_model_port(handler)
    assert resolved is port
    assert port.accessed == []


def test_absent_model_port_factory_is_a_posture_not_an_error(tmp_path):
    """FR-025/SC-008/research R6: no declared factory means an honest
    empty-catalog / editor-only posture, and the server still builds and
    serves exactly as before — no new key on `/capabilities` either
    (regression guard lives in its own test below)."""
    with _serving(tmp_path) as (httpd, host, port):
        handler = _handler_class(httpd)
        assert handler.model_port_factory is None
        assert handler._workbench_model_port(handler) is None
        status, caps = _request(host, port, "GET", "/capabilities")
    assert status == 200
    assert "model" not in caps["actions"]
    assert "model" not in caps


def test_model_port_is_absent_without_a_resolved_actor(tmp_path, monkeypatch):
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *args, **kwargs: None)
    port = _RecordingPort()
    with _serving(tmp_path, actor=None, model_port_factory=lambda: port) as (httpd, host, p):
        handler = _handler_class(httpd)
        assert handler.capabilities["actions"]["session"] is False
        assert handler._workbench_model_port(handler) is None
    assert port.accessed == []


def test_model_port_is_absent_without_a_real_checkout(tmp_path):
    empty_checkout = tmp_path / "empty-checkout"
    empty_checkout.mkdir()
    port = _RecordingPort()
    with _serving(tmp_path, checkout_root=empty_checkout,
                 model_port_factory=lambda: port) as (httpd, host, p):
        handler = _handler_class(httpd)
        assert handler.capabilities["actions"]["session"] is False
        assert handler._workbench_model_port(handler) is None
    assert port.accessed == []


def test_model_port_is_absent_on_a_non_loopback_hosted_handler(tmp_path):
    """The route tests flip `handler.loopback`/`handler.capabilities` rather
    than binding `0.0.0.0` — the established pattern this file's siblings use
    (test_session_snapshot.py, test_repo_selector.py) — because the PLANE is
    what a hosted probe must refuse, not merely the advertised capability."""
    port = _RecordingPort()
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        handler = _handler_class(httpd)
        assert handler._workbench_model_port(handler) is port  # capable/local: sanity check

        class _Hosted(handler):
            capabilities = {"actions": {"session": False}}

        assert _Hosted._workbench_model_port(_Hosted) is None
    assert port.accessed == []


def test_model_port_factory_that_raises_yields_none_not_a_500(tmp_path):
    def _raise():
        raise RuntimeError("provider construction boom")

    with _serving(tmp_path, model_port_factory=_raise) as (httpd, host, port):
        handler = _handler_class(httpd)
        assert handler._workbench_model_port(handler) is None


def test_compute_capabilities_still_returns_its_exact_pre_existing_dict():
    """Regression guard (hard boundary): this slice adds NO key to
    `/capabilities` or `compute_capabilities` — the additive public `model`
    field belongs with the catalog route (T050). Pinned with the SAME exact
    dict literal test_notebook_action.py already asserts, so a stray key
    anywhere fails here too."""
    no_refresh = {"binding": None, "loopback_only": True}
    assert serve_mod.compute_capabilities(
        nlm_present=True, checkout_real=True, loopback=True) == {
        "actions": {"notebook": True, "gate": False, "refresh": False,
                    "session": False, "edit": False},
        "actor": None,
        "refresh": no_refresh,
    }
    assert serve_mod.compute_capabilities(
        nlm_present=True, checkout_real=True, loopback=True, actor="brett") == {
        "actions": {"notebook": True, "gate": True, "refresh": False,
                    "session": True, "edit": True},
        "actor": "brett",
        "refresh": no_refresh,
    }


# ============================================================================
# D. the first-edit Save body bound (T104 F5-6)
#
# The governed Save verb `first-edit` posts the document's FULL replacement
# text to `/actions/gate/first-edit`, and both sides declare the buffer bound
# at `doxbench_hash.MAX_BUFFER_BYTES` (400,000 UTF-8 bytes; doxbench-state.js
# `DOXBENCH_MAX_BUFFER_BYTES` agrees). Reading that body through the global
# 65,536-byte `_read_json_body` refused a perfectly legal ~70KB Save at the
# TRANSPORT — with the misleading "a JSON object body is required", because
# that reader collapses "too large" into the same bare `None` as any other
# malformation. The fix routes this ONE verb through the widened
# `_read_bounded_json_body` at `DOXBENCH_MAX_REQUEST_BYTES` (reused, not a
# new bound — see the comment at the branch in `_handle_gate_action`); every
# other gate verb keeps the tiny cap deliberately.
# ============================================================================

def _first_edit_body(content: str) -> dict:
    """A first-edit body that DELIBERATELY omits the required tile scope, so
    the verb refuses in `_edit_body`'s own shape check — a refusal that can
    only be produced AFTER the transport has read and parsed the whole body,
    and that never opens a session or touches git in the fixture checkout."""
    return {"document": "ideation/staging/ideation-governance/README.md",
            "content": content}


def test_a_70kb_first_edit_save_passes_the_transport_and_reaches_the_verb(tmp_path):
    """The declared-bound Save (F5-6's reproducer): ~70KB of replacement text
    is UNDER the buffer bound both sides declare, so the transport must admit
    it. The verb then refuses for its own (deliberately planted) reason — a
    message only `_edit_body` produces — proving the body was read, parsed,
    and inspected rather than dropped at the cap. What this asserts NOT to
    happen is the old failure: the bare transport `invalid_body` with the
    fixed `JSON_OBJECT_BODY_REQUIRED` message, or any oversize refusal."""
    assert 70_000 > serve_mod._MAX_BODY_BYTES  # the old cap refused this Save
    from ideation_dashboard import doxbench_hash
    assert 70_000 < doxbench_hash.MAX_BUFFER_BYTES  # both sides declare it legal
    with _serving(tmp_path) as (httpd, host, port):
        caps = _capabilities(host, port)
        status, payload = _request(
            host, port, "POST", "/actions/gate/first-edit",
            body=_first_edit_body("x" * 70_000),
            headers=_console_headers(caps))
    assert payload.get("error") != "request_limit_exceeded"
    assert payload.get("message") != serve_mod.JSON_OBJECT_BODY_REQUIRED
    # The refusal that proves arrival: _edit_body's own tile-scope shape check.
    assert status == 400
    assert "scope" in payload.get("message", "")


def test_an_over_cap_first_edit_body_gets_an_honest_measured_size_refusal(tmp_path):
    """A genuinely oversize Save must be refused as a SIZE problem — the fixed
    `request_limit_exceeded` with its measured limit block — never as "a JSON
    object body is required", which misdirects the caller into reshaping a
    body whose only defect is its byte count. The content carries a sentinel
    so the refusal is also proven not to echo request text."""
    sentinel = "FIRST-EDIT-OVERSIZE-SENTINEL-4c1d"
    content = sentinel + ("x" * serve_mod.DOXBENCH_MAX_REQUEST_BYTES)
    with _serving(tmp_path) as (httpd, host, port):
        caps = _capabilities(host, port)
        status, payload = _request(
            host, port, "POST", "/actions/gate/first-edit",
            body=_first_edit_body(content),
            headers=_console_headers(caps))
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED)
    assert payload["error"] == "request_limit_exceeded"
    assert payload["message"] == serve_mod._DOXBENCH_MSG_REQUEST_LIMIT_EXCEEDED
    assert payload["limit"]["dimension"] == "request_body_bytes"
    assert payload["limit"]["maximum"] == serve_mod.DOXBENCH_MAX_REQUEST_BYTES
    assert payload["limit"]["measured"] > serve_mod.DOXBENCH_MAX_REQUEST_BYTES
    assert sentinel not in json.dumps(payload)


def test_a_lone_surrogate_in_first_edit_content_refuses_400_not_500(tmp_path):
    """Wave re-review P3: JSON's `"\\ud800"` escape decodes to a Python str no
    file can hold — and nothing on the first-edit path encoded `content`
    before the boundary write, so the `UnicodeEncodeError` raised at
    `write_text` escaped the transaction's unwind and reached the operator as
    a 500 with a stderr traceback (reproduced against a scratch session repo:
    the raise site is `boundary.rewrite_session_document`). The verb now
    refuses it at its own body/shape layer, in the transaction's own
    vocabulary: 400 `invalid_body` with a FIXED sentence naming the
    unpaired-surrogate condition — never the text itself, and never a
    session opened for a Save that cannot be written."""
    from ideation_dashboard import gate_routes
    sentinel = "FIRST-EDIT-SURROGATE-SENTINEL-7e2a"
    body = {"scope_kind": "staged-topic", "scope_id": "ideation-governance",
            "document": "ideation/staging/ideation-governance/README.md",
            "content": "# Outline\n\nrewritten \ud800 " + sentinel}
    with _serving(tmp_path) as (httpd, host, port):
        caps = _capabilities(host, port)
        status, payload = _request(
            host, port, "POST", "/actions/gate/first-edit",
            body=body, headers=_console_headers(caps))
    assert status == 400, f"expected the shape-layer refusal, got {status}"
    assert payload["error"] == "invalid_body"
    assert payload["message"] == gate_routes.FIRST_EDIT_UNENCODABLE_CONTENT
    # the refusal names the CONDITION, never the content.
    assert sentinel not in json.dumps(payload)


def test_the_first_edit_cap_accommodates_the_declared_buffer_bound():
    """The cap is DERIVED, not minted: `DOXBENCH_MAX_REQUEST_BYTES` must keep
    admitting a full declared buffer (`doxbench_hash.MAX_BUFFER_BYTES`) plus
    JSON-escaping inflation and envelope overhead. If either constant moves so
    that a maximal legal Save no longer fits, this pin makes the collision a
    test failure instead of a rediscovered F5-6."""
    from ideation_dashboard import doxbench_hash
    assert serve_mod.DOXBENCH_MAX_REQUEST_BYTES > doxbench_hash.MAX_BUFFER_BYTES


@pytest.mark.parametrize("verb", [
    # Wave re-review P3: the pin used to cover `ratify` alone, so the
    # carve-out could silently widen to any OTHER verb without a test
    # noticing — `verb in ("first-edit", "create-document")` would have kept
    # this file green. One case per verb CLASS that reads a body on this
    # route and can be refused before its own logic runs:
    "ratify",              # pre-existing, non-session gate verb
    "create-document",     # session-OPENING verb
    "edit-document",       # session-WRITING verb
    "abandon-session",     # session-ENDING verb
])
def test_other_gate_verbs_keep_the_tiny_global_cap(tmp_path, verb):
    """The carve-out is ONE verb wide (`first-edit`). Every other gate verb —
    pre-existing or session-bearing — still reads through `_read_json_body`:
    an over-65-KiB body refuses with the bare transport `invalid_body`, exactly
    as before F5-6 — widening every verb would weaken unrelated actions for no
    declared payload (research R7's reasoning, unchanged).

    Each case is as cheap as the original ratify one: the transport refuses
    the over-cap body BEFORE `run_gate_action` dispatches, so no session, no
    git, and no verb logic ever runs — the console-token headers admit the
    request past the session-verb presence gate, and the very next step is
    the body read that refuses."""
    with _serving(tmp_path) as (httpd, host, port):
        caps = _capabilities(host, port)
        status, payload = _request(
            host, port, "POST", f"/actions/gate/{verb}",
            body={"padding": "x" * (serve_mod._MAX_BODY_BYTES + 1)},
            headers=_console_headers(caps))
    assert status == 400
    assert payload == {"ok": False, "error": "invalid_body",
                       "message": serve_mod.JSON_OBJECT_BODY_REQUIRED}
