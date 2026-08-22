"""T043/T050 (change 010-doxbench-editor-chat): the doxBench HTTP ROUTE
surface in `serve.py`, tested end to end over a REAL ephemeral
`ThreadingHTTPServer`.

THIS IS TURN 1 OF 2. This file currently covers ONLY the T050 catalog route,
`GET /workbench/model-catalog` (and its shared-gate `HEAD` twin), against the
adjudicated behaviour recorded in `specs/010-doxbench-editor-chat/contracts/
model-catalog.md` and the T024 slice already landed in `serve.py`
(`DOXBENCH_ERROR_CATALOG`, `doxbench_error_body`/`doxbench_error_status`,
`_workbench_model_port`). The T051 chat-turn route
(`POST /actions/workbench/chat-turn`) is a SEPARATE follow-up turn of this
same file and is not written here.

These are RED tests: `serve_mod.WORKBENCH_MODEL_CATALOG_ROUTE` and the route
dispatch in `_route`/`do_GET`/`do_HEAD` do not exist yet in this checkout, so
every test below is expected to fail (most at collection, via the missing
module-level constant referenced immediately below) until the route is
implemented. `serve.py` is deliberately NOT modified by this file.

What this file deliberately does NOT assert, recording the same scoped
deferrals `test_doxbench_request_handling.py` and `test_doxbench_turns.py`
already record for their own slices:

* (SUPERSEDED 2026-07-30 by the released contract -- see the "injected
  released-schema validators" banner below.) This file used to record "NO
  `schema_version`/`kind` wire envelope" as a deliberate deferral while the two
  additive openxFactory schemas were unreleased. They are RELEASED and PINNED
  at contract-v1.27 (`d09d5820de5b63b9528f6baea884a6dccde9b158`), so both
  routes now emit the released envelopes and validate them before send;
* NO provider dispatch of any kind -- every port used below is an injected
  fake (`FakeWorkbenchModelPort` from `doxbench_model.py`, or a minimal
  duck-typed stand-in defined in this file); there is no real provider
  adapter anywhere in this suite;
* NO response DECODING beyond parsing the returned JSON object and comparing
  it to fixed expectations -- no markdown rendering, no content-identity
  hashing, nothing from `doxbench-state.js`/`app.js`.

Follows the house style of `test_doxbench_request_handling.py` /
`test_edit_action.py`: a real ephemeral `ThreadingHTTPServer` over
`serve_mod.build_server(...)`, injected fakes only, `from conftest import
...`, and refusal assertions built from the module's OWN error catalog
rather than hardcoded guesses at status/message text.
"""

from __future__ import annotations

import copy
import http.client
import json
import os
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest
import yaml

from conftest import BASE_REPO, PINNED_REVISION, REPO_ROOT, FakeGit

from jsonschema import Draft202012Validator

from ideation_dashboard import action_errors
from ideation_dashboard import branch_session
from ideation_dashboard import doxbench_contracts
from ideation_dashboard import doxbench_hash
from ideation_dashboard import doxbench_turns
from ideation_dashboard import gate_console
from ideation_dashboard import serve as serve_mod
from ideation_dashboard.doxbench_hash import content_identity
from ideation_dashboard.doxbench_model import (
    EMPTY_CATALOG,
    FakeWorkbenchModelPort,
    ModelCatalog,
    ModelCatalogEntry,
    PUBLIC_ENTRY_FIELDS,
    catalog_wire_envelope,
)
from ideation_dashboard.doxbench_scope import ScopeKey
from ideation_dashboard.generator import generate_snapshot

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"

# The route under test (T050). Referencing it at module scope is deliberate:
# it does not exist yet, so importing this file fails closed (an
# AttributeError at collection) rather than silently skipping every test.
ROUTE = serve_mod.WORKBENCH_MODEL_CATALOG_ROUTE


def _snapshot():
    return generate_snapshot(
        BASE_REPO, "fixture-repo", source_revision=PINNED_REVISION, git=FakeGit())


# ============================================================================
# injected released-schema validators (T024/T050/T051 wire clause)
#
# The routes validate every wire shape they emit -- and the chat request they
# accept -- against the RELEASED contract-v1.27 schemas, resolved through
# `doxbench_contracts`. That resolution reads a pinned openxFactory CHECKOUT,
# which a hermetic suite has no business depending on, so the validators are
# an INJECTED seam exactly like `model_port_factory`. Tests here supply
# hand-held fixture validators.
#
# The fixtures pin the ENVELOPE DISCRIMINATORS ONLY -- `schema_version`, the
# instance `kind`, the released required-key list, and closedness. They
# deliberately restate NO value-level rule (pattern, length, ceiling): those
# are the release's, and restating one in a fixture is the forking of contract
# authority `doxbench_contracts` exists to prevent (the same reasoning
# `test_doxbench_contracts.py`'s hermetic rung records). Conformance against
# the REAL released bytes is the env-gated integration rung at the bottom of
# this file, and every semantic rule beyond the shape belongs to the delegated
# openxFactory validator.
#
# Every `kind` literal comes from `doxbench_contracts`, never re-spelled here.
# ============================================================================

_FIXTURE_CATALOG_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "kind", "models"],
    "properties": {
        "schema_version": {"const": 1},
        "kind": {"const": doxbench_contracts.KIND_MODEL_CATALOG},
        "models": {"type": "array"},
    },
}

_FIXTURE_TURN_REQUEST_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "kind", "client_turn_id", "scope",
                 "active_document_path", "working_subject", "message", "model_id",
                 "last_assistant_turn_id", "transcript", "buffers"],
    "properties": {
        "schema_version": {"const": 1},
        "kind": {"const": doxbench_contracts.KIND_CHAT_TURN},
        # Value-level rules are the RELEASE's, not this fixture's; the keys are
        # declared only so the closed envelope admits them.
        "client_turn_id": {},
        "scope": {},
        "active_document_path": {},
        "working_subject": {},
        "message": {},
        "model_id": {},
        "last_assistant_turn_id": {},
        "transcript": {},
        "buffers": {},
    },
}

_FIXTURE_TURN_SUCCESS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "kind", "client_turn_id", "assistant_turn_id",
                 "model_id", "observed_hashes", "assistant_prose", "proposals"],
    "properties": {
        "schema_version": {"const": 1},
        "kind": {"const": doxbench_contracts.KIND_CHAT_TURN_SUCCESS},
        "client_turn_id": {}, "assistant_turn_id": {}, "model_id": {},
        "observed_hashes": {}, "assistant_prose": {}, "proposals": {},
    },
}

_FIXTURE_TURN_FAILURE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "kind", "client_turn_id", "error", "message"],
    "properties": {
        "schema_version": {"const": 1},
        "kind": {"const": doxbench_contracts.KIND_CHAT_TURN_FAILURE},
        "client_turn_id": {}, "error": {}, "message": {},
        "limit": {},
    },
}

# The CO-RESIDENT WIDENED family (contract-v1.34,
# add-doxbench-editing-phase-b §13), fixtured to the same depth and for the same
# reason: discriminators and closedness only. `bound_buffer` replaces
# `active_document_path` on the request -- the binding is DECLARED, not inferred
# from an adjacent field -- and the record gains that key plus the
# selected-model metadata.
_FIXTURE_TURN_V2_REQUEST_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "kind", "client_turn_id", "scope",
                 "bound_buffer", "working_subject", "message", "model_id",
                 "last_assistant_turn_id", "transcript", "buffers"],
    "properties": {
        "schema_version": {"const": 1},
        "kind": {"const": doxbench_contracts.KIND_CHAT_TURN_V2},
        "client_turn_id": {},
        "scope": {},
        "bound_buffer": {},
        "working_subject": {},
        "message": {},
        "model_id": {},
        "last_assistant_turn_id": {},
        "transcript": {},
        "buffers": {},
    },
}

_FIXTURE_TURN_V2_SUCCESS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "kind", "client_turn_id", "assistant_turn_id",
                 "model_id", "selected_model", "bound_buffer", "observed_hashes",
                 "assistant_prose", "proposals"],
    "properties": {
        "schema_version": {"const": 1},
        "kind": {"const": doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS},
        "client_turn_id": {}, "assistant_turn_id": {}, "model_id": {},
        "selected_model": {}, "bound_buffer": {},
        "observed_hashes": {}, "assistant_prose": {}, "proposals": {},
    },
}

_FIXTURE_TURN_V2_FAILURE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "kind", "client_turn_id", "error", "message"],
    "properties": {
        "schema_version": {"const": 1},
        "kind": {"const": doxbench_contracts.KIND_CHAT_TURN_V2_FAILURE},
        "client_turn_id": {}, "error": {}, "message": {},
        "limit": {},
    },
}

_FIXTURE_SCHEMAS = {
    doxbench_contracts.KIND_MODEL_CATALOG: _FIXTURE_CATALOG_SCHEMA,
    doxbench_contracts.KIND_CHAT_TURN: _FIXTURE_TURN_REQUEST_SCHEMA,
    doxbench_contracts.KIND_CHAT_TURN_SUCCESS: _FIXTURE_TURN_SUCCESS_SCHEMA,
    doxbench_contracts.KIND_CHAT_TURN_FAILURE: _FIXTURE_TURN_FAILURE_SCHEMA,
    doxbench_contracts.KIND_CHAT_TURN_V2: _FIXTURE_TURN_V2_REQUEST_SCHEMA,
    doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS: _FIXTURE_TURN_V2_SUCCESS_SCHEMA,
    doxbench_contracts.KIND_CHAT_TURN_V2_FAILURE: _FIXTURE_TURN_V2_FAILURE_SCHEMA,
}


def _fixture_validators():
    return {kind: Draft202012Validator(schema)
            for kind, schema in _FIXTURE_SCHEMAS.items()}


def _require_released_validators():
    """The REAL pinned release's validators, for the few tests whose SUBJECT is a
    value-level rule the fixture deliberately does not express.

    The fixture above is "discriminators and closedness only" -- `"buffers": {}`
    -- so a test of behavior the `minItems: 2` floor DEFINES would be testing the
    fixture's silence rather than the release's rule. These tests therefore bind
    the actual release, and SKIP where it cannot be read, which keeps the whole
    rest of the suite's no-checkout-required promise intact.

    Resolved ONCE in the test body rather than inside the injected factory: a
    `pytest.skip` raised on a serving thread would not skip anything."""
    try:
        return doxbench_contracts.validators(root=REPO_ROOT, repo_root=REPO_ROOT)
    except Exception as exc:  # noqa: BLE001 - any unreadable pin means skip
        pytest.skip(f"the pinned doxBench release is unreadable here: {exc}")


def _refusing_validators():
    """Validators that refuse EVERY instance -- the "the shape this route was
    about to send does not conform" input, so the fail-closed branch is proven
    against a real refusal rather than asserted in the abstract."""
    return {kind: Draft202012Validator({"not": {}}) for kind in _FIXTURE_SCHEMAS}


_EMPTY_CATALOG_ENVELOPE = {"schema_version": 1,
                           "kind": doxbench_contracts.KIND_MODEL_CATALOG,
                           "models": []}

# `_serving` injects fixture validators by default; this sentinel asks it to
# pass NOTHING, so `build_server`'s own default seam is what binds.
_UNSET = object()


# ============================================================================
# shared HTTP harness (mirrors test_doxbench_request_handling.py's own
# `_serving`/`_handler_class`/`_request`/`_capabilities`/`_console_headers`)
# ============================================================================

@contextmanager
def _serving(tmp_path, *, actor="brett", checkout_root=None,
            model_port_factory=None, snapshot=None,
            knowledge_declaration=None, packet_assembler=None,
            schema_validator_factory=_fixture_validators):
    """PIN EVOLUTION (T024/T050/T051 wire clause): the harness now injects
    released-schema validators, because the routes validate every wire shape
    they emit and the request they accept. The default is the hand-held
    fixture factory above, so this suite stays hermetic -- it must never
    depend on a pinned openxFactory checkout being present. Pass `_UNSET` to
    exercise `build_server`'s own default seam instead."""
    snap_path = tmp_path / "snapshot.json"
    snap_path.write_text(json.dumps(snapshot or _snapshot()), encoding="utf-8")
    extra = ({} if schema_validator_factory is _UNSET
             else {"schema_validator_factory": schema_validator_factory})
    httpd = serve_mod.build_server(
        WEB,
        snap_path,
        checkout_root if checkout_root is not None else BASE_REPO,
        head=PINNED_REVISION,
        actor=actor,
        model_port_factory=model_port_factory,
        # add-doxbench-editing-phase-b task 10.6: the INSTALL-TIME retrieval
        # backend declaration. `None` -- the default here and in
        # `build_server` -- is the declared reduced-packet posture, which is
        # what every pre-existing test in this file exercises unchanged.
        knowledge_declaration=knowledge_declaration,
        # The packet assembler is a COLLABORATOR of the turn route, injected
        # like every other one; `None` keeps `build_server`'s real default.
        packet_assembler=packet_assembler,
        **extra,
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
    """The bound `DashboardHandler` subclass a server was built with -- the
    same unwrap `test_doxbench_request_handling.py`/`test_session_snapshot.py`
    use, since `build_server` hands `ThreadingHTTPServer` a
    `functools.partial(bound, directory=...)`."""
    return getattr(httpd.RequestHandlerClass, "func", httpd.RequestHandlerClass)


def _request(host, port, method, path, *, body=None, headers=None):
    """Unlike the T024 file's 2-tuple twin, this also returns the response
    HEADERS (lower-cased, mirroring test_doxbench_transport.py's own
    `resp.getheaders()` idiom) and the RAW response bytes, since this route's
    JSON-media-type and zero-leakage assertions need both. `payload` is `None`
    on a non-JSON body (e.g. the static-file 404 page a near-miss path still
    falls through to) rather than raising."""
    conn = http.client.HTTPConnection(host, port, timeout=5)
    raw_request_body = None if body is None else json.dumps(body)
    conn.request(method, path, body=raw_request_body, headers=headers or {})
    resp = conn.getresponse()
    raw_response_body = resp.read()
    try:
        payload = json.loads(raw_response_body.decode("utf-8") or "{}")
    except ValueError:
        payload = None
    response_headers = {k.lower(): v for k, v in resp.getheaders()}
    conn.close()
    return resp.status, payload, response_headers, raw_response_body


def _capabilities(host, port):
    status, payload, _headers, _raw = _request(host, port, "GET", "/capabilities")
    assert status == 200
    return payload


def _console_headers(caps):
    return {
        "Content-Type": "application/json",
        "X-XF-Console-Token": caps["console_token"],
    }


# ============================================================================
# fixtures: catalogs, a "leaky" port, and a duck-typed bad-return port
# ============================================================================

def _two_entry_catalog() -> ModelCatalog:
    """One available entry, one unavailable -- order is significant to the
    order-preservation assertions below."""
    return ModelCatalog.from_entries([
        ModelCatalogEntry(
            model_id="model-a",
            label="Available Model A",
            provider_class="on-tenant",
            available=True,
            input_limit_bytes=800_000,
            output_limit_bytes=900_000,
            data_handling="Processed in the approved tenant boundary"),
        ModelCatalogEntry(
            model_id="model-b",
            label="Unavailable Model B",
            provider_class="off-tenant",
            available=False,
            input_limit_bytes=500_000,
            output_limit_bytes=400_000,
            data_handling="Processed off-tenant, disabled pending approval"),
    ])


# Sentinel strings that could only reach the wire from a credential, a raw
# endpoint, an environment-variable name, a request template, a
# provider-internal name, or a deployment resource name -- planted on a REAL
# injected port object (not asserted in the abstract) so the leakage tests
# below have a genuine input to prove absent.
_SENTINEL_CREDENTIAL = "sk-SENTINEL-CREDENTIAL-9f3a7c21"
_SENTINEL_ENDPOINT = "https://internal-provider.sentinel.example/v1/completions"
_SENTINEL_ENV_VAR_NAME = "SENTINEL_SECRET_PROVIDER_API_KEY"
_SENTINEL_REQUEST_TEMPLATE = '{"prompt": "{{SENTINEL_PROMPT_TEMPLATE}}", "max_tokens": 256}'
_SENTINEL_PROVIDER_INTERNAL_NAME = "sentinel-internal-model-v3-quantized-shard7"
_SENTINEL_DEPLOYMENT_RESOURCE = (
    "arn:aws:sentinel:us-east-1:123456789012:deployment/prod-sentinel-pool")
_SENTINEL_STACK_FRAME = (
    'Traceback (most recent call last): File "sentinel_provider_adapter.py", line 42')

_ATTRIBUTE_SENTINELS = (
    _SENTINEL_CREDENTIAL,
    _SENTINEL_ENDPOINT,
    _SENTINEL_ENV_VAR_NAME,
    _SENTINEL_REQUEST_TEMPLATE,
    _SENTINEL_PROVIDER_INTERNAL_NAME,
    _SENTINEL_DEPLOYMENT_RESOURCE,
)
_ERROR_SENTINELS = _ATTRIBUTE_SENTINELS + (_SENTINEL_STACK_FRAME,)


def _leaky_port(catalog: ModelCatalog) -> FakeWorkbenchModelPort:
    """A `FakeWorkbenchModelPort` carrying credential/endpoint/env-var/
    template/provider-internal/deployment-resource-shaped attributes in its
    OWN attribute space -- exactly what a real adapter might hold, never read
    by the route (research R6), planted only so the success-path leakage test
    has a real input rather than a strawman."""
    port = FakeWorkbenchModelPort(catalog)
    port.credential = _SENTINEL_CREDENTIAL
    port.endpoint = _SENTINEL_ENDPOINT
    port.env_var_name = _SENTINEL_ENV_VAR_NAME
    port.request_template = _SENTINEL_REQUEST_TEMPLATE
    port.provider_internal_name = _SENTINEL_PROVIDER_INTERNAL_NAME
    port.deployment_resource = _SENTINEL_DEPLOYMENT_RESOURCE
    return port


def _leaky_catalog_error() -> RuntimeError:
    """A `catalog_error` whose message reads like a real provider failure --
    endpoint, credential, env var, template, provider-internal name,
    deployment resource, AND a stack-trace-shaped line -- so the
    `catalog_unavailable` leakage test has a real seeded input too."""
    return RuntimeError(
        f"provider call to {_SENTINEL_ENDPOINT} failed using credential "
        f"{_SENTINEL_CREDENTIAL} (env {_SENTINEL_ENV_VAR_NAME}); "
        f"template={_SENTINEL_REQUEST_TEMPLATE}; "
        f"model={_SENTINEL_PROVIDER_INTERNAL_NAME}; "
        f"resource={_SENTINEL_DEPLOYMENT_RESOURCE}; {_SENTINEL_STACK_FRAME}")


class _BadPort:
    """A minimal duck-typed `WorkbenchModelPort` stand-in whose `catalog()`
    returns something that is NOT a `ModelCatalog` -- the "could not be
    assembled safely" half of `catalog_unavailable`
    (contracts/model-catalog.md), proven with a fake, never a real provider.
    Carries its own `calls` log, same discipline as `FakeWorkbenchModelPort`."""

    def __init__(self, bad_value) -> None:
        self._bad_value = bad_value
        self.calls: list[str] = []
        self.timeout_seconds = 30.0

    def catalog(self):
        self.calls.append("catalog")
        return self._bad_value


# ============================================================================
# T050: GET/HEAD /workbench/model-catalog
# ============================================================================

def test_route_constant_matches_the_planning_contract():
    assert serve_mod.WORKBENCH_MODEL_CATALOG_ROUTE == "/workbench/model-catalog"


# ---- exact method/path -----------------------------------------------------

def test_get_exact_path_is_routed_to_the_catalog_handler(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert headers["content-type"] == serve_mod.JSON_CTYPE
    assert "models" in payload and len(payload["models"]) == 2


def test_post_to_the_catalog_path_is_not_this_route(tmp_path):
    """A POST to the exact catalog path is NOT the T050 route -- it falls to
    `do_POST`'s existing unknown-action refusal. Read from
    `action_errors.ERROR_CATALOG`/`error_body` rather than hardcoding a
    guessed status/message, per the packet's explicit instruction."""
    with _serving(tmp_path) as (httpd, host, p):
        status, payload, _headers, _raw = _request(host, p, "POST", ROUTE, body={})
    expected_status, expected_message = action_errors.ERROR_CATALOG[
        action_errors.ERR_UNKNOWN_ACTION]
    assert status == expected_status
    assert payload == action_errors.error_body(action_errors.ERR_UNKNOWN_ACTION)
    assert payload["message"] == expected_message


def test_trailing_slash_is_not_this_route(tmp_path):
    with _serving(tmp_path) as (httpd, host, p):
        status, _payload, headers, _raw = _request(host, p, "GET", ROUTE + "/")
    assert status == 404
    assert headers["content-type"].startswith("text/html")


def test_pluralized_path_is_not_this_route(tmp_path):
    with _serving(tmp_path) as (httpd, host, p):
        status, _payload, headers, _raw = _request(host, p, "GET", ROUTE + "s")
    assert status == 404
    assert headers["content-type"].startswith("text/html")


def test_query_string_form_still_routes_through_the_same_handler(tmp_path):
    """`_route` strips query/fragment before comparing paths -- the query form
    of the exact route must still reach the SAME handler as the bare path."""
    port = FakeWorkbenchModelPort(EMPTY_CATALOG)
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, headers, _raw = _request(
            host, p, "GET", ROUTE + "?x=1", headers=_console_headers(caps))
    assert status == 200
    assert payload == _EMPTY_CATALOG_ENVELOPE
    assert headers["content-type"] == serve_mod.JSON_CTYPE
    assert port.calls == ["catalog"]


def test_head_is_gated_identically_to_get_and_returns_no_body(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, _payload, headers, raw = _request(
            host, p, "HEAD", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert raw == b""
    assert headers["content-type"] == serve_mod.JSON_CTYPE
    assert port.calls == ["catalog"]


def test_head_refusal_returns_no_body_too(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        status, _payload, headers, raw = _request(
            host, p, "HEAD", ROUTE, headers={"Content-Type": "application/json"})
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert raw == b""
    assert headers["content-type"] == serve_mod.JSON_CTYPE
    assert port.calls == []


# ---- JSON media type --------------------------------------------------------

def test_content_type_is_exact_json_ctype_on_success_and_on_refusals(tmp_path):
    # success
    with _serving(
            tmp_path,
            model_port_factory=lambda: FakeWorkbenchModelPort(EMPTY_CATALOG),
    ) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, _payload, headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert headers["content-type"] == serve_mod.JSON_CTYPE

    # refusal 1: console_required (missing token)
    with _serving(tmp_path) as (httpd, host, p):
        status, _payload, headers, _raw = _request(
            host, p, "GET", ROUTE, headers={"Content-Type": "application/json"})
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert headers["content-type"] == serve_mod.JSON_CTYPE

    # refusal 2: model_capability_unavailable (no real checkout)
    empty_checkout = tmp_path / "empty-checkout-ctype"
    empty_checkout.mkdir()
    with _serving(tmp_path, checkout_root=empty_checkout) as (httpd, host, p):
        status, _payload, headers, _raw = _request(host, p, "GET", ROUTE)
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert headers["content-type"] == serve_mod.JSON_CTYPE


# ---- console gate, with real evidence --------------------------------------

def test_console_gate_admits_the_real_console(tmp_path):
    port = FakeWorkbenchModelPort(EMPTY_CATALOG)
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        assert caps["console_token"]  # a real, non-empty minted token
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert payload == _EMPTY_CATALOG_ENVELOPE
    assert port.calls == ["catalog"]


def test_console_gate_refuses_missing_token(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        _capabilities(host, p)  # mints the token; this request just never sends it
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers={"Content-Type": "application/json"})
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert payload == serve_mod.doxbench_error_body(serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert port.calls == []


def test_console_gate_refuses_wrong_token(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        headers = _console_headers(caps)
        headers["X-XF-Console-Token"] = "definitely-not-the-real-token"
        status, payload, _headers, _raw = _request(host, p, "GET", ROUTE, headers=headers)
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert payload == serve_mod.doxbench_error_body(serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert port.calls == []


def test_console_gate_refuses_foreign_origin(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        headers = _console_headers(caps)
        headers["Origin"] = "https://evil.example"
        status, payload, _headers, _raw = _request(host, p, "GET", ROUTE, headers=headers)
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert payload == serve_mod.doxbench_error_body(serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert port.calls == []


def test_console_gate_refuses_host_not_naming_the_bound_port(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        headers = _console_headers(caps)
        headers["Host"] = "rebound.example"
        status, payload, _headers, _raw = _request(host, p, "GET", ROUTE, headers=headers)
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert payload == serve_mod.doxbench_error_body(serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED)
    assert port.calls == []


def test_console_gate_accepts_a_token_bearing_get_without_content_type(tmp_path):
    """PIN EVOLUTION (T098 finding fix; operator ruling (a), spec
    Clarifications 2026-07-31). This test previously pinned that a GET MUST
    declare `Content-Type: application/json` — the exact pin that MASKED the
    real-browser T098 failure, because the browser transport correctly sends
    no Content-Type on GET. The clause's purpose is non-simplicity, and the
    console-token header already forces a CORS preflight; header PRESENCE now
    satisfies that one clause while validity/Host/origin refuse unchanged
    (their pins follow below)."""
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        headers = {"X-XF-Console-Token": caps["console_token"]}  # no Content-Type
        status, payload, _headers, _raw = _request(host, p, "GET", ROUTE, headers=headers)
    assert status == 200
    assert len(payload["models"]) == 2
    assert port.calls == ["catalog"]


# ---- plane gate, checked BEFORE the console gate ---------------------------

def test_plane_gate_refuses_without_a_resolved_actor_before_the_console_gate(
        tmp_path, monkeypatch):
    """`resolve_actor` is forced to `None` (mirroring
    test_doxbench_request_handling.py's own
    `test_model_port_is_absent_without_a_resolved_actor`, since `BASE_REPO`'s
    real git config could otherwise resolve an actor even when the caller
    passes `actor=None`). No console-related header is sent AT ALL, yet the
    refusal is `model_capability_unavailable`, not `console_required` --
    proof the plane gate is consulted first."""
    monkeypatch.setattr(serve_mod, "resolve_actor", lambda *args, **kwargs: None)
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, actor=None,
                 model_port_factory=lambda: port) as (httpd, host, p):
        handler = _handler_class(httpd)
        assert handler.capabilities["actions"]["session"] is False
        status, payload, _headers, _raw = _request(host, p, "GET", ROUTE)
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert payload == serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert port.calls == []


def test_plane_gate_refuses_without_a_real_checkout_before_the_console_gate(tmp_path):
    """A non-real (empty) checkout also fails the `session` capability, and
    again the refusal is `model_capability_unavailable` even with no
    console-related header sent."""
    empty_checkout = tmp_path / "empty-checkout-plane"
    empty_checkout.mkdir()
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, checkout_root=empty_checkout,
                 model_port_factory=lambda: port) as (httpd, host, p):
        handler = _handler_class(httpd)
        assert handler.capabilities["actions"]["session"] is False
        status, payload, _headers, _raw = _request(host, p, "GET", ROUTE)
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert payload == serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE)
    assert port.calls == []


# ---- empty-catalog posture (FR-025/SC-008): a success, not an error -------

def test_absent_model_port_factory_yields_empty_catalog_success(tmp_path):
    with _serving(tmp_path) as (httpd, host, p):  # no model_port_factory at all
        handler = _handler_class(httpd)
        assert handler.model_port_factory is None
        caps = _capabilities(host, p)
        status, payload, headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert payload == _EMPTY_CATALOG_ENVELOPE
    assert headers["content-type"] == serve_mod.JSON_CTYPE


def test_empty_catalog_fake_port_yields_empty_catalog_success(tmp_path):
    port = FakeWorkbenchModelPort(EMPTY_CATALOG)
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert payload == _EMPTY_CATALOG_ENVELOPE
    assert port.calls == ["catalog"]


# ---- public-only descriptors: key-exact, order-preserving -----------------

def test_success_body_exposes_only_the_public_allowlist_fields_in_order(tmp_path):
    catalog = _two_entry_catalog()
    port = FakeWorkbenchModelPort(catalog)
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert set(payload) == {"schema_version", "kind", "models"}
    assert [entry["model_id"] for entry in payload["models"]] == ["model-a", "model-b"]
    for entry in payload["models"]:
        assert set(entry) == set(PUBLIC_ENTRY_FIELDS)
    assert payload == catalog_wire_envelope(catalog)
    assert port.calls == ["catalog"]


def test_success_body_carries_the_released_catalog_envelope(tmp_path):
    """PIN EVOLUTION (T024/T050 wire clause). This test previously asserted
    the ABSENCE of `schema_version`/`kind` -- the correct pin while the
    additive openxFactory catalog schema was unreleased (T005-T008, T014,
    T021). That schema is now RELEASED and PINNED (contract-v1.27,
    `d09d5820de5b63b9528f6baea884a6dccde9b158`), so the same test now pins the
    released envelope instead of its absence."""
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert payload["schema_version"] == 1
    assert payload["kind"] == doxbench_contracts.KIND_MODEL_CATALOG
    assert payload["kind"] == "workbench-model-catalog"


def test_catalog_success_body_is_validated_against_the_released_schema_before_send(tmp_path):
    """The console never serves an unvalidated wire shape: the enveloped
    response is checked against the injected released-schema validator BEFORE
    it goes out, and a validator that refuses the shape turns the success into
    the fixed `catalog_unavailable`."""
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port,
                 schema_validator_factory=_refusing_validators) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert payload == serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)


def test_catalog_route_refuses_fail_closed_when_the_pinned_checkout_is_unreachable(tmp_path):
    """An unreachable pinned checkout is NOT an implicit pass: with no
    validators the model route refuses the fixed `catalog_unavailable` rather
    than serving a shape nothing verified. The editor-only posture endures --
    the editor's own routes are untouched by this refusal."""
    def _unreachable():
        raise doxbench_contracts.ContractPinError("no openxFactory checkout is reachable")

    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port,
                 schema_validator_factory=_unreachable) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert payload == serve_mod.doxbench_error_body(
        serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    # Nothing about the missing checkout reaches the wire.
    assert set(payload) == {"ok", "error", "message"}


def test_the_default_validator_factory_resolves_the_pinned_checkout(tmp_path):
    """`build_server` defaults the seam to the pinned loader rather than to
    "no validation": an absent factory must not become an implicit pass."""
    with _serving(tmp_path, schema_validator_factory=_UNSET) as (httpd, host, p):
        handler = _handler_class(httpd)
        assert handler.schema_validator_factory is not None
        assert handler.schema_validator_factory is serve_mod.default_doxbench_validators


# ---- catalog_unavailable ----------------------------------------------------

def test_catalog_port_that_raises_yields_catalog_unavailable(tmp_path):
    port = FakeWorkbenchModelPort(catalog_error=RuntimeError("boom"))
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == serve_mod.doxbench_error_status(serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert payload == serve_mod.doxbench_error_body(serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert headers["content-type"] == serve_mod.JSON_CTYPE
    assert port.calls == ["catalog"]


def test_catalog_port_returning_a_non_catalog_yields_catalog_unavailable(tmp_path):
    port = _BadPort({"models": []})
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == serve_mod.doxbench_error_status(serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert payload == serve_mod.doxbench_error_body(serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert port.calls == ["catalog"]


# ---- zero leakage: real sentinels, threaded through real inputs -----------

def test_no_sentinel_leakage_on_success(tmp_path):
    port = _leaky_port(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, _payload, headers, raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    header_blob = " ".join(f"{k}:{v}" for k, v in headers.items())
    for sentinel in _ATTRIBUTE_SENTINELS:
        assert sentinel.encode("utf-8") not in raw
        assert sentinel not in header_blob
    assert port.calls == ["catalog"]


def test_no_sentinel_leakage_on_catalog_unavailable(tmp_path):
    port = FakeWorkbenchModelPort(catalog_error=_leaky_catalog_error())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, headers, raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == serve_mod.doxbench_error_status(serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    assert payload == serve_mod.doxbench_error_body(serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE)
    header_blob = " ".join(f"{k}:{v}" for k, v in headers.items())
    for sentinel in _ERROR_SENTINELS:
        assert sentinel.encode("utf-8") not in raw
        assert sentinel not in header_blob
    assert port.calls == ["catalog"]


# ---- refusal-body shape, across all three refusal codes -------------------

def test_refusal_bodies_carry_exactly_ok_error_message_with_fixed_messages(tmp_path):
    """Every refusal this route can produce -- `console_required`,
    `model_capability_unavailable`, `catalog_unavailable` -- carries EXACTLY
    `{"ok", "error", "message"}`, and `message` is the module's own fixed
    constant, never text composed from the request. Checked against three
    real refusals, not asserted in the abstract."""
    port_a = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port_a) as (httpd, host, p):
        status_a, payload_a, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers={"Content-Type": "application/json"})

    empty_checkout = tmp_path / "empty-checkout-shape"
    empty_checkout.mkdir()
    port_b = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, checkout_root=empty_checkout,
                 model_port_factory=lambda: port_b) as (httpd, host, p):
        status_b, payload_b, _headers, _raw = _request(host, p, "GET", ROUTE)

    port_c = FakeWorkbenchModelPort(catalog_error=RuntimeError("boom"))
    with _serving(tmp_path, model_port_factory=lambda: port_c) as (httpd, host, p):
        caps = _capabilities(host, p)
        status_c, payload_c, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))

    cases = (
        (status_a, payload_a, serve_mod.DOXBENCH_ERR_CONSOLE_REQUIRED),
        (status_b, payload_b, serve_mod.DOXBENCH_ERR_MODEL_CAPABILITY_UNAVAILABLE),
        (status_c, payload_c, serve_mod.DOXBENCH_ERR_CATALOG_UNAVAILABLE),
    )
    for status, payload, code in cases:
        assert status == serve_mod.doxbench_error_status(code)
        assert set(payload) == {"ok", "error", "message"}
        assert payload["ok"] is False
        assert payload["error"] == code
        assert payload["message"] == serve_mod.DOXBENCH_ERROR_CATALOG[code][1]


# ---- port-consultation discipline ------------------------------------------

def test_the_model_port_is_consulted_at_most_once_per_successful_request(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, _payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert port.calls == ["catalog"]


# ============================================================================
# T051: POST /actions/workbench/chat-turn
#
# NOTE on scope (SUPERSEDED 2026-07-30 by the released contract). This section
# used to record that UNKNOWN extra request keys were deliberately NOT
# rejected, and that no test asserted `schema_version`/`kind`, because
# exact-envelope validation was schema-gated on T005-T008/T014/T021 and "not
# this ad hoc route's to invent". The `xfactory-workbench-chat-turn` schema is
# RELEASED and PINNED at contract-v1.27
# (`d09d5820de5b63b9528f6baea884a6dccde9b158`), so the route now validates the
# request against the released CLOSED envelope before the precondition chain
# and emits the released failure envelope for every refusal that has a
# wire-valid turn identity. The precondition chain itself (steps 1-8) is
# unchanged, and DISPATCH IS STILL REFUSED (T049).
# ============================================================================

OUTLINE_PATH = "ideation/staging/ideation-governance/README.md"
READABLE_ONLY_PATH = "ideation/brainstorm/doc-health-checks.md"
CHAT_ROUTE = serve_mod.ACTIONS_WORKBENCH_CHAT_TURN_ROUTE

_S_OUTLINE = "SENTINEL-OUTLINE-BUFFER-TEXT-a91f"
_S_DOCUMENT = "SENTINEL-DOCUMENT-BUFFER-TEXT-b72e"
_S_SUBJECT = "SENTINEL-WORKING-SUBJECT-c53d"
_S_MESSAGE = "SENTINEL-HUMAN-MESSAGE-d14c"
_S_TRANSCRIPT = "SENTINEL-TRANSCRIPT-TEXT-e65b"
_TURN_SENTINELS = (_S_OUTLINE, _S_DOCUMENT, _S_SUBJECT, _S_MESSAGE, _S_TRANSCRIPT)

# The released failure envelope's exact key set for a non-limit refusal. Named
# once so the leakage assertions below pin the CLOSED shape rather than
# repeating a literal that could drift from `_assert_refusal`.
_RELEASED_FAILURE_KEYS = frozenset(
    {"schema_version", "kind", "client_turn_id", "error", "message"})


def _buf(kind, path, content, *, repository="fixture-repo", base_ref="main",
         base_revision=PINNED_REVISION, base_hash=None, content_hash=None, dirty=True):
    """One buffer envelope. Hashes are computed from `content` unless overridden."""
    digest = content_identity(content).hex
    return {"kind": kind, "repository": repository, "path": path,
            "base_ref": base_ref, "base_revision": base_revision,
            "base_hash": base_hash if base_hash is not None else digest,
            "content_hash": content_hash if content_hash is not None else digest,
            "content": content, "dirty": dirty}


def _turn(**over):
    """A structurally valid turn body whose document buffer is the
    not-yet-created (null path) carve-out, so the only in-scope editable path
    used is the outline README."""
    body = {
        # PIN EVOLUTION (T051 wire clause): the RELEASED request envelope is
        # closed and requires both discriminators, so the fixture carries them.
        # Every other field is unchanged, and no assertion below was relaxed.
        "schema_version": 1,
        "kind": doxbench_contracts.KIND_CHAT_TURN,
        "client_turn_id": "turn-0001",
        "scope": {"repository": "fixture-repo", "ref": "main",
                  "tile_kind": "staged", "tile_id": "ideation-governance"},
        "active_document_path": None,
        "working_subject": "Clarify the acceptance boundary " + _S_SUBJECT,
        "message": "Which open question should we close next? " + _S_MESSAGE,
        "model_id": "model-a",
        "last_assistant_turn_id": None,
        "transcript": [],
        "buffers": [
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ],
    }
    body.update(over)
    return body


def _catalog(*, model_id="model-a", available=True, input_limit_bytes=1_048_576):
    return ModelCatalog((ModelCatalogEntry(
        model_id=model_id, label="Approved authoring model",
        provider_class="on-tenant", available=available,
        input_limit_bytes=input_limit_bytes, output_limit_bytes=900_000,
        data_handling="Processed in the approved tenant boundary"),))


def _port(catalog=None):
    return FakeWorkbenchModelPort(catalog if catalog is not None else _catalog())


def _post_turn(tmp_path, body, *, port=None, headers=None, snapshot=None,
               knowledge_declaration=None, inspect_handler=None,
               packet_assembler=None, checkout_root=None,
               schema_validator_factory=_fixture_validators):
    """POST a turn as the real local console. Returns (status, payload, port).

    `inspect_handler` is called with the bound handler class while the server
    is still up, for a test that needs to read per-process state the response
    does not carry (the usage meter, task 10.8).

    `schema_validator_factory` defaults to the hermetic fixture, exactly as
    `_serving` does; the released-schema tests pass `_require_released_validators`
    output so a value-level rule can be exercised as the release states it."""
    fake = port if port is not None else _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake), snapshot=snapshot,
                  knowledge_declaration=knowledge_declaration,
                  packet_assembler=packet_assembler,
                  schema_validator_factory=schema_validator_factory,
                  checkout_root=checkout_root) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(host, prt, "POST", CHAT_ROUTE, body=body,
                                   headers=headers or _console_headers(caps))
        if inspect_handler is not None:
            inspect_handler(_handler_class(httpd))
    return status, payload, fake


def _assert_refusal(status, payload, code, message=None):
    """PIN EVOLUTION (T051 wire clause). Every refusal reached AFTER the turn
    identity has been read and found wire-valid now carries the RELEASED
    `workbench-chat-turn-failure` envelope, which is CLOSED and admits no `ok`
    key -- so the `ok is False` assertion this helper used to make is now the
    wrong pin, not a weakened one. The code and the fixed module-level message
    are asserted exactly as before, and the key set is asserted EXACTLY, so
    nothing can be added to a failure body unnoticed.

    `client_turn_id` is asserted present and in the released 1..128 bound
    rather than compared to a literal, because callers below use several turn
    ids; the exact ECHO is pinned by its own dedicated test.

    Refusals reached BEFORE the request validated -- the plane gate, the
    console gate, and the route-specific body bound -- keep the pre-existing
    fixed shape and are asserted by `_assert_preidentity_refusal`."""
    assert status == serve_mod.doxbench_error_status(code)
    expected = {"schema_version", "kind", "client_turn_id", "error", "message"}
    if code == serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED:
        expected.add("limit")
    assert set(payload) == expected
    assert payload["schema_version"] == 1
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_FAILURE
    assert isinstance(payload["client_turn_id"], str)
    assert 1 <= len(payload["client_turn_id"]) <= 128
    assert payload["error"] == code
    assert payload["message"] == _expected_refusal_message(code, message)


def _expected_refusal_message(code, message):
    """The message a refusal must carry: the catalog's, unless a caller names a
    different FIXED module-level constant.

    `None` is the default at every one of the ~30 call sites below, and that is
    the point of the parameter rather than a convenience: those call sites now
    assert positively that their violation still gets the GENERIC sentence, so
    the one cause-naming message added for the buffers floor cannot leak into
    any other refusal without failing here."""
    if message is None:
        return serve_mod.DOXBENCH_ERROR_CATALOG[code][1]
    return message


def _assert_v2_refusal(status, payload, code, message=None):
    """`_assert_refusal` for the WIDENED family (contract-v1.34). Identical in
    every clause but the `kind`: a refusal is answered in the family its request
    arrived in, and asserting the v1 kind on a v2 turn would pass only for a
    route that answered the wrong one."""
    assert status == serve_mod.doxbench_error_status(code)
    expected = {"schema_version", "kind", "client_turn_id", "error", "message"}
    if code == serve_mod.DOXBENCH_ERR_REQUEST_LIMIT_EXCEEDED:
        expected.add("limit")
    assert set(payload) == expected
    assert payload["schema_version"] == 1
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_V2_FAILURE
    assert isinstance(payload["client_turn_id"], str)
    assert 1 <= len(payload["client_turn_id"]) <= 128
    assert payload["error"] == code
    assert payload["message"] == _expected_refusal_message(code, message)


def _assert_preidentity_refusal(status, payload, code):
    """A refusal the released envelope CANNOT express: it requires a
    `client_turn_id`, and these refusals happen before any turn identity was
    read (or before one was found wire-valid). Fabricating an id would hand the
    browser a correlation key for a turn the server never accepted, so the
    route keeps `doxbench_error_body`'s pre-existing fixed shape -- same code,
    same fixed message, no invented identity."""
    assert status == serve_mod.doxbench_error_status(code)
    assert payload["ok"] is False
    assert payload["error"] == code
    assert payload["message"] == serve_mod.DOXBENCH_ERROR_CATALOG[code][1]
    assert "schema_version" not in payload
    assert "kind" not in payload
    assert "client_turn_id" not in payload


def _assert_no_sentinels(payload):
    blob = json.dumps(payload)
    for sentinel in _TURN_SENTINELS:
        assert sentinel not in blob


# ---- route identity ---------------------------------------------------------

def test_chat_route_constant_matches_the_planning_contract():
    assert CHAT_ROUTE == "/actions/workbench/chat-turn"


def test_get_on_the_chat_route_is_not_this_route(tmp_path):
    with _serving(tmp_path) as (httpd, host, port_num):
        status, _payload, headers, _raw = _request(host, port_num, "GET", CHAT_ROUTE)
    assert status == 404
    assert headers["content-type"].startswith("text/html")


def test_near_miss_chat_path_is_not_this_route(tmp_path):
    with _serving(tmp_path) as (httpd, host, port_num):
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE + "s", body=_turn())
    expected_status, expected_message = action_errors.ERROR_CATALOG[
        action_errors.ERR_UNKNOWN_ACTION]
    assert status == expected_status
    assert payload == action_errors.error_body(action_errors.ERR_UNKNOWN_ACTION)
    assert payload["message"] == expected_message


# ---- dispatch boundary (currently fixed at model_capability_unavailable) --

def test_valid_turn_reaches_the_dispatch_boundary_and_refuses_fixed(tmp_path):
    """PIN EVOLUTION (T051 dispatch arm; previous evolutions recorded the
    wire-clause and pre-arm postures). The arm HAS landed, so a fully valid
    turn through a dispatch-capable adapter now completes -- that path is
    pinned by test_a_valid_turn_with_a_dispatch_capable_port_returns_the_
    released_success. THIS test keeps its original purpose against the
    adapter shape that still cannot dispatch (`_CatalogOnlyPort`, the exact
    production posture until T099's approved adapter): the boundary refuses
    the SAME fixed code with the SAME released failure envelope,
    byte-preserved from the pre-arm assertions below."""
    status, payload, _fake_port = _post_turn(
        tmp_path, _turn(), port=_CatalogOnlyPort())
    _assert_refusal(status, payload, "model_capability_unavailable")
    assert "assistant_prose" not in payload
    assert "proposals" not in payload
    assert "observed_hashes" not in payload
    assert payload["kind"] == "workbench-chat-turn-failure"
    assert payload["kind"] != doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    _assert_no_sentinels(payload)


def test_the_released_failure_envelope_echoes_the_submitted_turn_id(tmp_path):
    # PIN EVOLUTION (T051 dispatch arm): catalog-only port keeps this a
    # FAILURE-envelope echo; the success envelope's echo is pinned by the
    # dispatch-capable success test.
    status, payload, _fake_port = _post_turn(
        tmp_path, _turn(client_turn_id="turn-echo-9137"),
        port=_CatalogOnlyPort())
    _assert_refusal(status, payload, "model_capability_unavailable")
    assert payload["client_turn_id"] == "turn-echo-9137"


# ---- released REQUEST validation, before the precondition chain ------------

def test_a_request_missing_the_released_discriminators_refuses_invalid_turn_request(tmp_path):
    body = _turn()
    del body["kind"]
    status, payload, fake = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    # Refused BEFORE scope, identity, model, or idempotency: the catalog was
    # never consulted, so nothing downstream of the schema gate ran.
    assert fake.calls == []


def test_a_request_with_the_wrong_schema_version_refuses_invalid_turn_request(tmp_path):
    status, payload, fake = _post_turn(tmp_path, _turn(schema_version=2))
    _assert_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_a_request_with_the_wrong_kind_refuses_invalid_turn_request(tmp_path):
    status, payload, fake = _post_turn(
        tmp_path, _turn(kind=doxbench_contracts.KIND_CHAT_TURN_SUCCESS))
    _assert_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_an_unknown_top_level_request_key_is_now_refused_as_a_schema_violation(tmp_path):
    """PIN EVOLUTION (T051 "exact schema"). The suite previously recorded that
    unknown extra keys were deliberately NOT rejected, because exact-envelope
    validation was schema-gated and "not this ad hoc route's to invent". The
    released request envelope is CLOSED (`additionalProperties: false`), so the
    release itself now supplies the rule the route was refusing to invent."""
    status, payload, fake = _post_turn(tmp_path, _turn(smuggled_key="anything"))
    _assert_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_a_schema_refusal_with_no_usable_turn_id_stays_on_the_fixed_shape(tmp_path):
    """`client_turn_id` itself is what is unusable, so NO released envelope can
    be built for the refusal that names it -- the envelope requires a string of
    1..128 characters, and inventing one would hand the browser a correlation
    key for a turn the server never accepted. A null id is the case both rungs
    agree on; the released 1..128 BOUND is exercised against the real validator
    in the integration rung, since a fixture that restated the bound would be
    restating a contract rule."""
    status, payload, fake = _post_turn(tmp_path, _turn(client_turn_id=None))
    _assert_preidentity_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_the_chat_route_refuses_fail_closed_when_the_pinned_checkout_is_unreachable(tmp_path):
    def _unreachable():
        raise doxbench_contracts.ContractPinError("no openxFactory checkout is reachable")

    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=_unreachable) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=_turn(), headers=_console_headers(caps))
    _assert_preidentity_refusal(status, payload, "model_capability_unavailable")
    assert fake.calls == []
    assert "checkout" not in json.dumps(payload)


def test_a_failure_envelope_that_cannot_be_validated_falls_back_to_the_fixed_shape(tmp_path):
    """Self-validation before send, on the FAILURE side too: with validators
    that refuse everything, the route can neither accept the request nor emit a
    released envelope for the refusal, so it sends the fixed shape rather than
    an envelope nothing verified."""
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=_refusing_validators) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=_turn(), headers=_console_headers(caps))
    _assert_preidentity_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_chat_refusal_carries_exact_json_media_type(tmp_path):
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        conn = http.client.HTTPConnection(host, port_num, timeout=5)
        conn.request("POST", CHAT_ROUTE, body=json.dumps(_turn()),
                     headers=_console_headers(caps))
        resp = conn.getresponse()
        resp.read()
        content_type = resp.getheader("Content-Type")
        conn.close()
    assert content_type == serve_mod.JSON_CTYPE


# ---- body bound (checked before turn-shape validation) ---------------------

def test_body_one_byte_over_the_route_bound_refuses_with_measured_limit(tmp_path):
    oversized = b"x" * (serve_mod.DOXBENCH_MAX_REQUEST_BYTES + 1)
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        conn = http.client.HTTPConnection(host, port_num, timeout=5)
        conn.request("POST", CHAT_ROUTE, body=oversized, headers=_console_headers(caps))
        resp = conn.getresponse()
        raw = resp.read()
        status = resp.status
        conn.close()
    payload = json.loads(raw.decode("utf-8"))
    # The body is refused UNREAD at the bound, so there is no turn identity to
    # put in a released envelope -- this refusal keeps the fixed shape and its
    # measured `limit` block (FR-017), which is where the numeric verdict lives
    # in BOTH shapes.
    _assert_preidentity_refusal(status, payload, "request_limit_exceeded")
    assert payload["limit"] == {
        "dimension": "request_body_bytes",
        "measured": 1_048_577,
        "maximum": 1_048_576,
    }


def test_malformed_json_body_refuses_invalid_body(tmp_path):
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        conn = http.client.HTTPConnection(host, port_num, timeout=5)
        conn.request("POST", CHAT_ROUTE, body=b"{not json", headers=_console_headers(caps))
        resp = conn.getresponse()
        raw = resp.read()
        status = resp.status
        conn.close()
    payload = json.loads(raw.decode("utf-8"))
    assert status == 400
    assert payload["error"] == "invalid_body"
    assert payload["message"] == serve_mod.JSON_OBJECT_BODY_REQUIRED


def test_non_object_json_body_refuses_invalid_body(tmp_path):
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        conn = http.client.HTTPConnection(host, port_num, timeout=5)
        conn.request("POST", CHAT_ROUTE, body=b"[1,2,3]", headers=_console_headers(caps))
        resp = conn.getresponse()
        raw = resp.read()
        status = resp.status
        conn.close()
    payload = json.loads(raw.decode("utf-8"))
    assert status == 400
    assert payload["error"] == "invalid_body"
    assert payload["message"] == serve_mod.JSON_OBJECT_BODY_REQUIRED


# ---- turn-shape validation ---------------------------------------------------

def test_blank_message_refuses_invalid_turn_request(tmp_path):
    status, payload, _fake_port = _post_turn(tmp_path, _turn(message="   "))
    _assert_refusal(status, payload, "invalid_turn_request")


def test_duplicate_buffer_kind_refuses_invalid_turn_request(tmp_path):
    body = _turn(buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("outline", OUTLINE_PATH, "# Outline again\n\n" + _S_OUTLINE),
    ])
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")


def test_missing_document_buffer_refuses_invalid_turn_request(tmp_path):
    """PIN EVOLUTION (Amendment 2 follow-up 1). The verdict is unchanged -- same
    400, same `invalid_turn_request`, same envelope and key set -- but the
    SENTENCE now names what this test's own name has always said is wrong. The
    v1 family declares the same `buffers` floor (`minItems: 2`) as the widened
    one, so the cause is identical here and it is answered identically; a
    deprecated family is still one a human can be refused by."""
    body = _turn(buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
    ])
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request",
                    serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT)


# ---- scope refusals -----------------------------------------------------------

def test_unknown_tile_id_refuses_turn_scope_refused(tmp_path):
    body = _turn(scope={"repository": "fixture-repo", "ref": "main",
                        "tile_kind": "staged", "tile_id": "no-such-tile"})
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "turn_scope_refused")


def test_readable_but_not_editable_document_path_refuses_turn_scope_refused(tmp_path):
    body = _turn(
        active_document_path=READABLE_ONLY_PATH,
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
            _buf("document", READABLE_ONLY_PATH, "# Doc\n\n" + _S_DOCUMENT),
        ],
    )
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "turn_scope_refused")
    _assert_no_sentinels(payload)


def test_traversal_shaped_outline_path_refuses_turn_scope_refused(tmp_path):
    body = _turn(
        active_document_path=None,
        buffers=[
            _buf("outline", "../secrets.md", "# Outline\n\n" + _S_OUTLINE),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ],
    )
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "turn_scope_refused")


def test_buffer_bound_to_a_foreign_repository_refuses_turn_scope_refused(tmp_path):
    body = _turn(
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE,
                 repository="other-repo"),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ],
    )
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "turn_scope_refused")


# ---- content-identity refusals -----------------------------------------------

def test_wrong_content_hash_refuses_content_identity_mismatch(tmp_path):
    body = _turn(
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE,
                 content_hash="0" * 64),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ],
    )
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "content_identity_mismatch")


def test_uppercase_base_hash_refuses_content_identity_mismatch(tmp_path):
    text = "# Outline\n\n" + _S_OUTLINE
    body = _turn(
        buffers=[
            _buf("outline", OUTLINE_PATH, text,
                 base_hash=content_identity(text).hex.upper()),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ],
    )
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "content_identity_mismatch")


# ---- lone-surrogate (encoding) refusals (T104 F5-8) --------------------------
#
# JSON's `"\ud800"` escape decodes to a Python str holding a LONE UTF-16
# surrogate — text that cannot be encoded to UTF-8, so it cannot be
# represented identically across runtimes. `doxbench_hash` refuses it with
# `ContentEncodingError`, a plain ValueError SIBLING of `doxbench_turns.
# TurnError` (pinned in test_doxbench_turns.py), so before the F5-8 fix no
# `except` on the route caught it: the handler died mid-request and the
# browser got a DROPPED CONNECTION instead of any HTTP envelope. The released
# schema accepts the escape (jsonschema checks structure, not encodability),
# so this is reachable from any conforming client. The route now refuses it
# as the fixed `invalid_turn_request` — such a request is malformed — and the
# refusal must be an HTTP envelope, never a killed handler. One test per
# field class the handler measures or hashes; each surrogate rides NEXT TO a
# sentinel so the no-echo sweep still proves refusals never quote request
# content.

_LONE_SURROGATE = "\ud800"


def _surrogate_buf(kind, path, content):
    """A buffer envelope whose content holds a lone surrogate. `_buf` cannot
    build this one: it hashes its content via `content_identity`, which would
    trip `ContentEncodingError` in the TEST process. The hashes here are
    well-formed 64-char lowercase hex that simply do not match — deliberately,
    to prove the route refuses on the ENCODING (invalid_turn_request) before
    it ever reaches a hash comparison (content_identity_mismatch)."""
    return {"kind": kind, "repository": "fixture-repo", "path": path,
            "base_ref": "main", "base_revision": PINNED_REVISION,
            "base_hash": "0" * 64, "content_hash": "0" * 64,
            "content": content, "dirty": True}


def test_lone_surrogate_in_buffer_content_refuses_invalid_turn_request(tmp_path):
    body = _turn(
        buffers=[
            _surrogate_buf("outline", OUTLINE_PATH,
                           "# Outline\n\n" + _LONE_SURROGATE + _S_OUTLINE),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ],
    )
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)


def test_lone_surrogate_in_message_refuses_invalid_turn_request(tmp_path):
    body = _turn(message="Which question next? " + _LONE_SURROGATE + _S_MESSAGE)
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)


def test_lone_surrogate_in_working_subject_refuses_invalid_turn_request(tmp_path):
    body = _turn(working_subject="Acceptance boundary " + _LONE_SURROGATE + _S_SUBJECT)
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)


def test_lone_surrogate_in_a_transcript_turn_refuses_invalid_turn_request(tmp_path):
    body = _turn(transcript=[
        {"role": "human",
         "content": "An earlier question " + _LONE_SURROGATE + _S_TRANSCRIPT}])
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)


def test_lone_surrogate_in_base_ref_refuses_invalid_turn_request(tmp_path):
    """W-1 (wave re-review): `base_ref` and `base_revision` are the two
    request fields that reach the CANONICAL DIGEST with no earlier gate —
    they are neither measured nor hashed at steps 6/7, and both are
    RELEASED-SCHEMA-VALID surrogate carriers (plain bounded strings). Before
    this fix, `sha256_hex(json.dumps(canonical, ensure_ascii=False))` raised
    out of the digest statement and the handler died with a dropped
    connection — the exact F5-8 failure mode, one site over."""
    buf = _buf("document", None, "# Document\n\n" + _S_DOCUMENT)
    buf["base_ref"] = "main" + _LONE_SURROGATE
    body = _turn(buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE), buf])
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)


def test_lone_surrogate_in_base_revision_refuses_invalid_turn_request(tmp_path):
    buf = _buf("document", None, "# Document\n\n" + _S_DOCUMENT)
    buf["base_revision"] = _LONE_SURROGATE
    body = _turn(buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE), buf])
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)


def test_lone_surrogate_in_a_transcript_role_refuses_invalid_turn_request(tmp_path):
    """Wave re-review P3: the transcript turn's ROLE is the remaining
    surrogate carrier this section had not pinned. It is a free-form string
    (`doxbench_turns.TranscriptTurn` — deliberately not an enum), it is NOT
    measured at step 7 (`transcript_bytes` counts turn TEXT only, no role
    labels), and it is not hashed at step 6 — so, like `base_ref` and
    `base_revision` above, it reaches the canonical idempotency digest with
    no earlier encodability gate and W-1's digest-site
    `ContentEncodingError` catch is the layer that answers (proven by
    scratch-mutating that catch to re-raise: this test then loses the
    connection while the transcript-CONTENT pin above still refuses at step
    7). The hermetic fixture validators pass it through on purpose — they
    pin envelope discriminators only, never value-level rules — so this pin
    exercises the deepest layer the suite reaches. Refusal, not a dropped
    connection."""
    body = _turn(transcript=[
        {"role": _LONE_SURROGATE,
         "content": "An earlier question " + _S_TRANSCRIPT}])
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)


# ---- model refusals ------------------------------------------------------------

def test_unknown_model_id_refuses_model_unavailable(tmp_path):
    status, payload, _fake_port = _post_turn(tmp_path, _turn(model_id="not-in-catalog"))
    _assert_refusal(status, payload, "model_unavailable")


def test_unavailable_model_entry_refuses_model_unavailable(tmp_path):
    port = _port(_catalog(available=False))
    status, payload, _fake_port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "model_unavailable")


def test_absent_model_port_refuses_model_capability_unavailable(tmp_path):
    with _serving(tmp_path, model_port_factory=None) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status, payload, "model_capability_unavailable")


# ---- byte-limit refusals, checked at/after the model step -------------------

def test_stricter_catalog_input_limit_refuses_a_request_the_server_constant_would_allow(tmp_path):
    port = _port(_catalog(input_limit_bytes=2_000))
    body = _turn(buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE + ("x" * 5_000)),
        _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
    ])
    status, payload, _fake_port = _post_turn(tmp_path, body, port=port)
    _assert_refusal(status, payload, "request_limit_exceeded")


def test_oversize_message_refuses_with_measured_byte_dimension(tmp_path):
    body = _turn(message="x" * 16_385)
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "request_limit_exceeded")
    assert payload["limit"]["dimension"] == "message_bytes"


def test_multibyte_message_over_byte_budget_but_under_code_point_count_refuses(tmp_path):
    message = "\U0001F600" * 6_000
    assert len(message) == 6_000
    assert len(message.encode("utf-8")) == 24_000
    body = _turn(message=message)
    status, payload, _fake_port = _post_turn(tmp_path, body)
    _assert_refusal(status, payload, "request_limit_exceeded")


# ---- refusals before the model step never consult the catalog ---------------

def test_refusals_before_the_model_step_never_consult_the_catalog(tmp_path):
    cases = (
        _turn(scope={"repository": "fixture-repo", "ref": "main",
                     "tile_kind": "staged", "tile_id": "no-such-tile"}),
        _turn(
            active_document_path=READABLE_ONLY_PATH,
            buffers=[
                _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
                _buf("document", READABLE_ONLY_PATH, "# Doc\n\n" + _S_DOCUMENT),
            ],
        ),
        _turn(buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE,
                 content_hash="0" * 64),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ]),
    )
    for body in cases:
        _status, _payload, fake_port = _post_turn(tmp_path, body)
        assert fake_port.calls == []


# ============================================================================
# T051 continued: turn-store lifecycle at the idempotency boundary (step 8)
#
# These tests pin `contracts/chat-turn.md`'s "### Turn-store lifecycle
# obligations (planning-contract, not wire parity)" -- obligation 1 (a
# refused finalization must not abandon the slot: the fixed
# `model_capability_unavailable` dispatch-boundary refusal still calls
# `turn_store.fail(...)`, freeing the conversation key for a later attempt)
# and obligation 2 (an in-flight attach is bounded AT THE ROUTE, via a peek-
# before-reserve, never an indefinite wait inside the store). As with the
# rest of this file, no test below asserts `schema_version`, `kind`, or any
# other contract-parity shape -- only the planning-contract lifecycle
# behaviour above.
# ============================================================================

KEY = ScopeKey(repository="fixture-repo", ref="main",
               tile_kind="staged", tile_id="ideation-governance")


def test_turn_store_is_bound_per_server_process(tmp_path):
    with _serving(tmp_path) as (httpd_a, _host_a, _port_a):
        store_a = _handler_class(httpd_a).turn_store
        assert isinstance(store_a, doxbench_turns.TurnStore)
    with _serving(tmp_path) as (httpd_b, _host_b, _port_b):
        store_b = _handler_class(httpd_b).turn_store
        assert isinstance(store_b, doxbench_turns.TurnStore)
    assert store_a is not store_b


def test_valid_turn_records_a_failed_entry_and_frees_the_conversation_slot(tmp_path):
    # PIN EVOLUTION (T051 dispatch arm): this test's purpose is the
    # refused-finalization obligation, so it keeps the catalog-only posture;
    # the COMPLETED lifecycle is pinned by the success-replay test.
    with _serving(tmp_path, model_port_factory=(lambda: _CatalogOnlyPort())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
        _assert_refusal(status, payload, "model_capability_unavailable")
        record = _handler_class(httpd).turn_store.snapshot(KEY, "turn-0001")
    assert record.state == doxbench_turns.TURN_STATE_FAILED


def test_a_second_distinct_turn_id_is_not_refused_after_a_valid_turn_completed(tmp_path):
    # PIN EVOLUTION (T051 dispatch arm): slot semantics are the purpose, and
    # they are dispatch-independent -- catalog-only posture preserved.
    with _serving(tmp_path, model_port_factory=(lambda: _CatalogOnlyPort())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        status1, payload1, _headers1, _raw1 = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
        _assert_refusal(status1, payload1, "model_capability_unavailable")

        status2, payload2, _headers2, _raw2 = _request(
            host, port_num, "POST", CHAT_ROUTE,
            body=_turn(client_turn_id="turn-0002"),
            headers=_console_headers(caps))
    assert payload2["error"] != "turn_in_flight"
    _assert_refusal(status2, payload2, "model_capability_unavailable")


def test_identical_repeat_replays_the_stored_fixed_failure(tmp_path):
    # PIN EVOLUTION (T051 dispatch arm): stored-FAILURE replay stays pinned
    # via the catalog-only posture; stored-SUCCESS replay has its own test.
    body = _turn()
    with _serving(tmp_path, model_port_factory=(lambda: _CatalogOnlyPort())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        status1, payload1, _headers1, raw1 = _request(
            host, port_num, "POST", CHAT_ROUTE, body=body,
            headers=_console_headers(caps))
        status2, payload2, _headers2, raw2 = _request(
            host, port_num, "POST", CHAT_ROUTE, body=body,
            headers=_console_headers(caps))
        record = _handler_class(httpd).turn_store.snapshot(KEY, "turn-0001")
    assert status1 == status2
    assert raw1 == raw2
    _assert_refusal(status1, payload1, "model_capability_unavailable")
    _assert_refusal(status2, payload2, "model_capability_unavailable")
    assert record.state == doxbench_turns.TURN_STATE_FAILED


def test_seeded_in_flight_same_turn_id_with_a_different_digest_refuses_turn_id_conflict(
        tmp_path):
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(KEY, "turn-0001", "a" * 64)
        caps = _capabilities(host, port_num)
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status, payload, "turn_id_conflict")


def test_seeded_in_flight_different_turn_id_refuses_turn_in_flight(tmp_path):
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(KEY, "other-turn", "b" * 64)
        caps = _capabilities(host, port_num)
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status, payload, "turn_in_flight")


def test_seeded_in_flight_same_digest_refuses_turn_in_flight_without_waiting(tmp_path):
    """The digest is learned from a first server's real refusal, then seeded
    into a SECOND server's store ahead of the identical POST -- the route's
    request digest is a deterministic function of the request body alone, so
    a digest learned on one server is valid to seed on another given the same
    body."""
    body = _turn()
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        _request(host, port_num, "POST", CHAT_ROUTE, body=body,
                  headers=_console_headers(caps))
        digest = _handler_class(httpd).turn_store.snapshot(KEY, "turn-0001").request_digest

    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd2, host2, port_num2):
        _handler_class(httpd2).turn_store.reserve(KEY, "turn-0001", digest)
        caps2 = _capabilities(host2, port_num2)
        status, payload, _headers, _raw = _request(
            host2, port_num2, "POST", CHAT_ROUTE, body=body,
            headers=_console_headers(caps2))
    _assert_refusal(status, payload, "turn_in_flight")


def test_an_in_flight_attach_returns_promptly_rather_than_hanging(tmp_path):
    """A regression to the store's untimed `wait()` must fail this test (via
    `socket.timeout`) rather than stall the whole suite -- the route peeks
    the store before ever reserving/waiting, so a response must ARRIVE well
    inside the connection's own 5s timeout."""
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(KEY, "turn-0001", "c" * 64)
        caps = _capabilities(host, port_num)
        conn = http.client.HTTPConnection(host, port_num, timeout=5)
        conn.request("POST", CHAT_ROUTE, body=json.dumps(_turn()),
                     headers=_console_headers(caps))
        resp = conn.getresponse()
        resp.read()
        status = resp.status
        conn.close()
    assert status == serve_mod.doxbench_error_status("turn_in_flight")


def test_a_conflicting_digest_against_a_resolved_entry_refuses_turn_id_conflict(tmp_path):
    # PIN EVOLUTION (T051 dispatch arm): a RESOLVED entry of either kind
    # must conflict on a drifted digest; catalog-only keeps leg one a
    # resolved FAILURE exactly as before.
    with _serving(tmp_path, model_port_factory=(lambda: _CatalogOnlyPort())) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        status1, payload1, _headers1, _raw1 = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
        _assert_refusal(status1, payload1, "model_capability_unavailable")

        status2, payload2, _headers2, _raw2 = _request(
            host, port_num, "POST", CHAT_ROUTE,
            body=_turn(message="a completely different question entirely"),
            headers=_console_headers(caps))
    _assert_refusal(status2, payload2, "turn_id_conflict")


def test_unrelated_conversation_keys_never_interfere(tmp_path):
    other_key = ScopeKey(repository="fixture-repo", ref="main",
                          tile_kind="staged", tile_id="keyword-lens")
    # PIN EVOLUTION (T051 dispatch arm): catalog-only posture preserved --
    # the purpose is key isolation, not the dispatch outcome.
    with _serving(tmp_path, model_port_factory=(lambda: _CatalogOnlyPort())) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(other_key, "other-turn", "d" * 64)
        caps = _capabilities(host, port_num)
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    assert payload["error"] != "turn_in_flight"
    _assert_refusal(status, payload, "model_capability_unavailable")


def test_no_idempotency_refusal_leaks_request_content(tmp_path):
    # conflict refusal: same turn id already resolved/in-flight with a
    # different digest
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(KEY, "turn-0001", "a" * 64)
        caps = _capabilities(host, port_num)
        status_a, payload_a, _headers_a, _raw_a = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status_a, payload_a, "turn_id_conflict")
    _assert_no_sentinels(payload_a)
    assert set(payload_a) == _RELEASED_FAILURE_KEYS

    # in-flight refusal: a DIFFERENT turn id already in flight for the key
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(KEY, "other-turn", "b" * 64)
        caps = _capabilities(host, port_num)
        status_b, payload_b, _headers_b, _raw_b = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status_b, payload_b, "turn_in_flight")
    _assert_no_sentinels(payload_b)
    assert set(payload_b) == _RELEASED_FAILURE_KEYS


def test_idempotency_refusals_do_not_dispatch_or_reconsult_after_the_peek(tmp_path):
    # conflict refusal
    port_a = _port()
    with _serving(tmp_path, model_port_factory=(lambda: port_a)) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(KEY, "turn-0001", "a" * 64)
        caps = _capabilities(host, port_num)
        status_a, payload_a, _headers_a, _raw_a = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status_a, payload_a, "turn_id_conflict")
    assert len(port_a.calls) <= 1
    assert all(call == "catalog" for call in port_a.calls)

    # in-flight refusal
    port_b = _port()
    with _serving(tmp_path, model_port_factory=(lambda: port_b)) as (httpd, host, port_num):
        _handler_class(httpd).turn_store.reserve(KEY, "other-turn", "b" * 64)
        caps = _capabilities(host, port_num)
        status_b, payload_b, _headers_b, _raw_b = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status_b, payload_b, "turn_in_flight")
    assert len(port_b.calls) <= 1
    assert all(call == "catalog" for call in port_b.calls)


# ============================================================================
# T104 F4 (PR #63 second review, P1 serve.py:1547): the LOST PEEK/RESERVE RACE
#
# The route peeks the store before reserving, and the comment above that peek
# used to claim the untimed store wait "is never entered". That claim held
# only for the SEQUENTIAL case the tests above cover: every one of them
# pre-seeds the store and then sends ONE request, so the peek always sees the
# seeded record and the reserve-side replay branch is never reached.
#
# `ThreadingHTTPServer` serves each connection on its own thread against ONE
# shared `TurnStore`, so two requests carrying the SAME `client_turn_id` can
# BOTH pass the peek before either reserves. The store answers that correctly
# -- the second caller attaches, waits, and gets a lease whose
# `should_dispatch` is False plus the first caller's stored result -- but the
# route discarded the lease, so the second caller dispatched the provider a
# SECOND time (FR-019 requires refusing before another dispatch) and then died
# on an uncaught `TurnConflictError` out of `complete()`, dropping the
# connection with no envelope written.
#
# The interleave is forced deterministically by holding the first two peeks at
# a barrier. The store below IS `doxbench_turns.TurnStore` -- the real reserve,
# the real wait, the real replay branch, the real `ScopeKey` -- with the
# barrier as its only seam, sitting AFTER the real `snapshot` has answered.
# ============================================================================


class _PeekBarrierStore(doxbench_turns.TurnStore):
    """The real store, with the first two `snapshot` peeks held at a barrier so
    both requests pass the route's peek fast-path before either reserves."""

    def __init__(self, parties: int = 2) -> None:
        super().__init__()
        self._peek_barrier = threading.Barrier(parties, timeout=20)
        self._peek_lock = threading.Lock()
        self._peeks = 0
        self.held = 0

    def snapshot(self, conversation_key, client_turn_id):
        record = super().snapshot(conversation_key, client_turn_id)
        with self._peek_lock:
            self._peeks += 1
            hold = self._peeks <= self._peek_barrier.parties
        if hold:
            self.held += 1
            try:
                self._peek_barrier.wait()
            except threading.BrokenBarrierError:  # pragma: no cover - safety net
                pass
        return record


def _concurrent_turns(host, port_num, caps, body, count=2):
    """Fire `count` identical POSTs from their own threads and collect what
    each one actually received -- including a DROPPED CONNECTION, which is the
    pre-fix outcome and must be reported as a result rather than as an error
    inside a worker thread."""
    results: list[dict] = [None] * count                      # type: ignore[list-item]

    def run(index):
        try:
            status, payload, _headers, raw = _request(
                host, port_num, "POST", CHAT_ROUTE, body=body,
                headers=_console_headers(caps))
            results[index] = {"status": status, "payload": payload, "raw": raw}
        except Exception as exc:  # noqa: BLE001 - the dropped connection IS the result
            results[index] = {"dropped": f"{type(exc).__name__}: {exc}"}

    threads = [threading.Thread(target=run, args=(i,)) for i in range(count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=30)
    assert all(not thread.is_alive() for thread in threads), "a request thread hung"
    return results


def test_two_concurrent_turns_on_one_turn_id_dispatch_once_and_replay_verbatim(tmp_path):
    """FR-019 under the REAL interleave: exactly ONE provider dispatch, and the
    loser of the reserve race replays the winner's stored result BYTE-IDENTICALLY
    instead of dispatching a second time. Neither caller may lose its connection."""
    fake = _port()
    body = _turn()
    with _serving(tmp_path, model_port_factory=(lambda: fake)) as (httpd, host, port_num):
        handler = _handler_class(httpd)
        store = _PeekBarrierStore()
        handler.turn_store = store
        caps = _capabilities(host, port_num)
        results = _concurrent_turns(host, port_num, caps, body)
        record = store.snapshot(KEY, "turn-0001")
    assert store.held == 2, "the peek barrier did not hold both requests"
    for result in results:
        assert "dropped" not in result, (
            f"a concurrent turn lost its connection: {result.get('dropped')}")
    assert [result["status"] for result in results] == [200, 200]
    assert results[0]["raw"] == results[1]["raw"], (
        "the replayed answer is not byte-identical to the stored one")
    assert fake.calls.count("dispatch") == 1, (
        "the provider was dispatched more than once for one client_turn_id "
        f"(calls: {fake.calls})")
    assert record.state == doxbench_turns.TURN_STATE_COMPLETED


class _ConflictingFinalizeStore(doxbench_turns.TurnStore):
    """The real store with ONE finalize arm forced to raise the conflict the
    route never handled -- the state a lost race leaves behind once another
    caller has already resolved this entry."""

    def __init__(self, *, arm: str) -> None:
        super().__init__()
        self._arm = arm

    def complete(self, conversation_key, client_turn_id, result, *, size_bytes):
        if self._arm == "complete":
            raise doxbench_turns.TurnConflictError(
                "no in-flight turn exists to finalize for this conversation "
                "key and turn id")
        return super().complete(conversation_key, client_turn_id, result,
                                size_bytes=size_bytes)

    def fail(self, conversation_key, client_turn_id, failure, *, size_bytes):
        if self._arm == "fail":
            raise doxbench_turns.TurnConflictError(
                "no in-flight turn exists to finalize for this conversation "
                "key and turn id")
        return super().fail(conversation_key, client_turn_id, failure,
                            size_bytes=size_bytes)


def test_a_conflicting_finalize_of_a_success_answers_a_released_failure_envelope(
        tmp_path):
    """A `TurnConflictError` raised by `complete()` must not kill the handler.
    The dispatched answer cannot be stored, so it cannot be replayed either --
    the caller gets the RELEASED conflict refusal, never a dropped connection
    and never a success the store does not hold."""
    with _serving(tmp_path, model_port_factory=(lambda: _port())) as (httpd, host, port_num):
        _handler_class(httpd).turn_store = _ConflictingFinalizeStore(arm="complete")
        caps = _capabilities(host, port_num)
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status, payload, "turn_id_conflict")
    assert set(payload) == _RELEASED_FAILURE_KEYS
    _assert_no_sentinels(payload)


def test_a_conflicting_finalize_of_a_refusal_still_answers_its_released_envelope(
        tmp_path):
    """The same on the failure arm: the verdict for THIS request was already
    computed and validated, so a store that refuses to record it still answers
    with it rather than dropping the connection."""
    with _serving(tmp_path, model_port_factory=(lambda: _CatalogOnlyPort())) as (
            httpd, host, port_num):
        _handler_class(httpd).turn_store = _ConflictingFinalizeStore(arm="fail")
        caps = _capabilities(host, port_num)
        status, payload, _headers, _raw = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
    _assert_refusal(status, payload, "model_capability_unavailable")
    assert set(payload) == _RELEASED_FAILURE_KEYS
    _assert_no_sentinels(payload)


# ============================================================================
# T107 / FR-043: a SESSION-CREATED document becomes chat-eligible, and the
# record that makes it so belongs to the SERVER
#
# Before T107 this route passed NO `created_paths` to the scope authority, so
# the created-in-session set was empty on every turn and a document the human
# had just created could never be the subject of one. The set is now derived
# from the session's OWN committed `create-document` gate-action records, read
# out of the session worktree the registry entry already points at.
#
# The forgery tests below are the CHK012 obligation stated as behaviour.
# PIN EVOLUTION (T051 "exact schema"): the obligation is now met TWICE OVER and
# the tests say so. It used to be met only by indifference -- the route ignored
# unknown extra request keys, so a request-declared created set changed
# NOTHING. The RELEASED request envelope is CLOSED, so such a request is now
# REFUSED outright (`invalid_turn_request`) before scope runs at all: strictly
# stronger than being ignored. Because a schema refusal would otherwise mask
# the scope-layer coverage, each forgery case below is split -- one request
# WITHOUT the forged keys, which must still be refused by SCOPE, and one WITH
# them, which must now be refused by the SCHEMA and never reach the port.
# ============================================================================

SESSION_TILE_ID = "ideation-governance"
SESSION_BRANCH = "draft/ideation-governance"
SESSION_CREATED_PATH = "ideation/brainstorm/created-in-this-sitting.md"
SESSION_UNRECORDED_PATH = "ideation/brainstorm/never-created-here.md"


def _session_worktree(tmp_path, *, documents=(SESSION_CREATED_PATH,),
                      branch=SESSION_BRANCH, present=True,
                      at="2026-07-30T12:00:00+00:00"):
    """A session WORKTREE holding exactly what a session `create-document` left
    behind: each created document, and the gate-action record naming it and the
    branch. Built through the real record builder and the real record path rule,
    so this cannot drift from what the gate route writes."""
    worktree = tmp_path / "sessions" / "draft-ideation-governance"
    worktree.mkdir(parents=True, exist_ok=True)
    for document in documents:
        record = gate_console.build_gate_action_record(
            actor="brett", action=gate_console.ACTION_CREATE_DOCUMENT, at=at,
            document=document,
            artifacts=[
                {"kind": gate_console.ART_DOCUMENT, "reference": document},
                branch_session.commit_artifact(branch_session.action_stamp(at)),
            ],
            ref=branch)
        rel = gate_console.gate_action_record_relpath(
            gate_console.DEFAULT_RECORDS_DIR, record["action"],
            gate_console.document_target_id(document), record["at"])
        record_path = worktree / rel
        record_path.parent.mkdir(parents=True, exist_ok=True)
        record_path.write_text(yaml.safe_dump(record, sort_keys=False),
                               encoding="utf-8")
        if present:
            created = worktree / document
            created.parent.mkdir(parents=True, exist_ok=True)
            created.write_text("Status: brainstorm\n\n# created\n",
                               encoding="utf-8")
    return worktree


def _register_session(httpd, tmp_path, worktree, *, branch=SESSION_BRANCH,
                      tile_id=SESSION_TILE_ID, session_base=None,
                      session_base_aliases=()):
    """Register the session's registry entry: liveness IS the entry (FR-008),
    and its `source_root` is the worktree (`branch_session.session_entry`).

    Nothing is opened, no git runs, and no request could have caused this -- it
    is the server-side fact the derivation reads. `session_base` is the
    `(base_ref, base_revision)` the OPEN would have recorded (T104 R-12),
    `session_base_aliases` its other recorded revision spellings (W-4);
    None/() is the pre-wave shape and the degradation posture."""
    registry = _handler_class(httpd).source.registry
    snap = Path(tmp_path) / f"session-snapshot-{branch.replace('/', '-')}.json"
    snap.write_text(json.dumps(_snapshot()), encoding="utf-8")
    entry = branch_session.session_entry(
        "fixture-repo", branch, worktree, snapshot_path=snap,
        tile=(branch_session.Tile(branch_session.STAGED_TOPIC, tile_id)
              if tile_id else None),
        session_base=session_base,
        session_base_aliases=tuple(session_base_aliases))
    registry.register(entry)
    return entry


def _session_turn(document=SESSION_CREATED_PATH, *, branch=SESSION_BRANCH, **over):
    """A structurally valid turn whose DOCUMENT buffer is `document`, bound to
    the session branch's scope."""
    body = _turn(
        scope={"repository": "fixture-repo", "ref": branch,
               "tile_kind": "staged", "tile_id": SESSION_TILE_ID},
        active_document_path=document,
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE,
                 base_ref=branch),
            _buf("document", document, "# Document\n\n" + _S_DOCUMENT,
                 base_ref=branch),
        ],
    )
    body.update(over)
    return body


def _post_session_turn(tmp_path, body, *, worktree, register=True, branch=SESSION_BRANCH,
                       tile_id=SESSION_TILE_ID, session_base=None,
                       session_base_aliases=()):
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake)) as (httpd, host, prt):
        if register:
            _register_session(httpd, tmp_path, worktree, branch=branch,
                              tile_id=tile_id, session_base=session_base,
                              session_base_aliases=session_base_aliases)
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=body,
            headers=_console_headers(caps))
    return status, payload, fake


# ---- the acceptance: the created document is now in scope AND editable ------

def test_a_session_created_document_passes_scope_revalidation(tmp_path):
    """It gets past step 5 and dies at the SAME fixed dispatch boundary a
    known-valid turn dies at (`test_valid_turn_reaches_the_dispatch_boundary_
    and_refuses_fixed`) -- provider dispatch is schema-gated and unchanged."""
    worktree = _session_worktree(tmp_path)
    # PIN EVOLUTION (T051 dispatch arm): "scope passed" used to be proven by
    # reaching the boundary's fixed refusal; the boundary now COMPLETES for
    # a dispatch-capable port, so the released success IS the proof -- a
    # strictly stronger assertion, not a relaxed one.
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(), worktree=worktree)
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    _assert_no_sentinels(payload)


def test_the_tiles_own_material_is_still_editable_inside_a_session(tmp_path):
    """The created path is ADDITIVE: it does not displace tile ownership."""
    worktree = _session_worktree(tmp_path)
    body = _session_turn(OUTLINE_PATH)
    # PIN EVOLUTION (T051 dispatch arm): completion replaces the old
    # boundary-refusal proxy as the in-scope proof.
    status, payload, _fake = _post_session_turn(tmp_path, body, worktree=worktree)
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS


def test_a_readable_only_document_is_still_refused_inside_a_session(tmp_path):
    """FR-043 widens NOTHING but the created set: context-only material stays
    readable-but-not-editable even on a live session's own branch."""
    worktree = _session_worktree(tmp_path)
    body = _session_turn(READABLE_ONLY_PATH)
    status, payload, _fake = _post_session_turn(tmp_path, body, worktree=worktree)
    _assert_refusal(status, payload, "turn_scope_refused")


# ---- the negatives: without the SERVER's record, nothing changed ------------

def test_a_session_with_no_created_record_still_refuses_the_document(tmp_path):
    """The live session exists; the record does not. Identical to pre-T107."""
    worktree = _session_worktree(tmp_path, documents=())
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(), worktree=worktree)
    _assert_refusal(status, payload, "turn_scope_refused")


def test_a_record_whose_document_is_absent_refuses_the_document(tmp_path):
    """A recorded path nobody can read is not chat-eligible."""
    worktree = _session_worktree(tmp_path, present=False)
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(), worktree=worktree)
    _assert_refusal(status, payload, "turn_scope_refused")


def test_a_created_document_without_a_live_registry_entry_is_refused(tmp_path):
    """The branch, the worktree and the record all exist; the registry does not
    know the session. Neither a branch nor a worktree proves liveness (D15)."""
    worktree = _session_worktree(tmp_path)
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(), worktree=worktree, register=False)
    _assert_refusal(status, payload, "turn_scope_refused")


def test_another_tiles_live_session_does_not_donate_its_created_document(tmp_path):
    """FR-002: the branch family is derived from the TILE. An entry recorded
    against a different tile is not this tile's session."""
    worktree = _session_worktree(tmp_path)
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(), worktree=worktree, tile_id="some-other-topic")
    _assert_refusal(status, payload, "turn_scope_refused")


def test_a_record_naming_another_branch_is_not_this_sessions_creation(tmp_path):
    worktree = _session_worktree(tmp_path, branch="draft/some-other-topic")
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(), worktree=worktree)
    _assert_refusal(status, payload, "turn_scope_refused")


# ---- T104 R-12 (reviewer ruling 2026-08-02): a buffer based on the session's
# ---- OWN recorded base grounds a turn; one the session diverged past does not.

def test_the_post_partial_save_turn_grounds_the_unlanded_buffer_on_the_session_base(tmp_path):
    """The R-12 acceptance, end to end: after a partial Save re-keys the scope
    to the session, a buffer the Save did NOT land still declares the
    pre-session base -- `rekeyDoxBenchState` deliberately keeps it
    byte-identical, base_ref included -- and that pairing now grounds a turn,
    because the buffer names the ref the session branched FROM at the
    session's own recorded base revision, and the session has not moved this
    document past that base. Provenance is preserved: nothing rewrote
    `base_ref`, the guard's comparison is what changed."""
    worktree = _session_worktree(tmp_path)
    base_text = (worktree / SESSION_CREATED_PATH).read_bytes().decode("utf-8")
    body = _session_turn()
    body["buffers"][1] = _buf(
        "document", SESSION_CREATED_PATH, base_text + "\nunsaved work\n",
        base_ref="main", base_revision="pre-session-rev-1",
        base_hash=content_identity(base_text).hex)
    status, payload, _fake = _post_session_turn(
        tmp_path, body, worktree=worktree,
        session_base=("main", "pre-session-rev-1"))
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    _assert_no_sentinels(payload)


def test_a_pre_session_buffer_is_refused_once_the_session_moved_the_document(tmp_path):
    """The ruling's divergence clause: a landed gate action advanced the
    session past its base FOR THIS DOCUMENT, so a buffer still claiming the
    pre-session base may genuinely be stale and the refusal is correct --
    staleness detection is made precise, never weakened. Without this the
    fix would read as "accept anything from main"."""
    worktree = _session_worktree(tmp_path)
    target = worktree / SESSION_CREATED_PATH
    base_text = target.read_bytes().decode("utf-8")
    target.write_text(base_text + "\nlanded by a later gate action\n",
                      encoding="utf-8")
    body = _session_turn()
    body["buffers"][1] = _buf(
        "document", SESSION_CREATED_PATH, base_text,
        base_ref="main", base_revision="pre-session-rev-1",
        base_hash=content_identity(base_text).hex, dirty=False)
    status, payload, _fake = _post_session_turn(
        tmp_path, body, worktree=worktree,
        session_base=("main", "pre-session-rev-1"))
    _assert_refusal(status, payload, "turn_scope_refused")
    _assert_no_sentinels(payload)


def test_the_post_partial_save_turn_grounds_on_the_snapshots_revision_alias(tmp_path):
    """W-4 (wave re-review): a REAL client's `base_revision` is the serving
    snapshot's generation-time revision, not the open-time merge-base — the
    browser never receives a per-file revision. Whenever main moved between
    snapshot bake and session open the two differed forever, and the R-12
    acceptance silently reverted to the refusal it closed (executed in the
    re-review). The OPEN records the snapshot's revision as an accepted
    ALIAS; the name and base-bytes clauses are untouched."""
    worktree = _session_worktree(tmp_path)
    base_text = (worktree / SESSION_CREATED_PATH).read_bytes().decode("utf-8")
    body = _session_turn()
    body["buffers"][1] = _buf(
        "document", SESSION_CREATED_PATH, base_text + "\nunsaved work\n",
        base_ref="main", base_revision="snapshot-rev-at-open",
        base_hash=content_identity(base_text).hex)
    status, payload, _fake = _post_session_turn(
        tmp_path, body, worktree=worktree,
        session_base=("main", "merge-base-at-open"),
        session_base_aliases=("snapshot-rev-at-open",))
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    _assert_no_sentinels(payload)


def test_a_crlf_bom_session_document_grounds_on_the_session_base(tmp_path):
    """W-7 (wave re-review): the R-12 reader at the route reads the session's
    current text through the SAME lens the client hashes (`served_text`:
    verbatim bytes, one leading BOM dropped, CR/CRLF intact) — and nothing
    pinned it: every R-12 fixture was LF-only, where `read_text`'s
    universal-newline collapse coincides with the served lens, so the reader
    could silently regress to `read_text` with the whole suite green
    (proven by the re-review's mutation round). This document makes the two
    lenses DISAGREE: under the regression the session identity hashes
    LF-collapsed BOM-bearing text, mismatches the declared base, and this
    correctly-based buffer is refused."""
    worktree = _session_worktree(tmp_path)
    raw = "﻿# Demo\r\n\r\nauthored on Windows.\r\n".encode("utf-8")
    (worktree / SESSION_CREATED_PATH).write_bytes(raw)
    base_text = doxbench_hash.served_text(raw)
    body = _session_turn()
    body["buffers"][1] = _buf(
        "document", SESSION_CREATED_PATH, base_text + "unsaved\r\n",
        base_ref="main", base_revision="pre-session-rev-1",
        base_hash=content_identity(base_text).hex)
    status, payload, _fake = _post_session_turn(
        tmp_path, body, worktree=worktree,
        session_base=("main", "pre-session-rev-1"))
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    _assert_no_sentinels(payload)


def test_a_document_moved_and_moved_back_grounds_again_the_content_ruling(tmp_path):
    """RULED (reviewer, 2026-08-06, closing the wave re-review's last open
    question): "diverged past that base" is a CONTENT reading. A session that
    moved this document and moved it BACK byte-identically accepts the
    pre-session buffer again — every acceptance is content-safe, since the
    buffer's base bytes provably equal the session's current text and no
    stale envelope can result; history is not consulted. This test is the
    ruling's executable record: the same worktree REFUSES while the document
    is moved (the divergence guard above) and grounds once it is restored."""
    worktree = _session_worktree(tmp_path)
    target = worktree / SESSION_CREATED_PATH
    original = target.read_bytes()
    body = _session_turn()
    body["buffers"][1] = _buf(
        "document", SESSION_CREATED_PATH, original.decode("utf-8"),
        base_ref="main", base_revision="pre-session-rev-1",
        base_hash=content_identity(original.decode("utf-8")).hex, dirty=False)

    target.write_bytes(original + b"moved by a landed gate action\n")
    status, payload, _fake = _post_session_turn(
        tmp_path, body, worktree=worktree,
        session_base=("main", "pre-session-rev-1"))
    _assert_refusal(status, payload, "turn_scope_refused")

    target.write_bytes(original)                     # ...and moved BACK
    status, payload, _fake = _post_session_turn(
        tmp_path, body, worktree=worktree,
        session_base=("main", "pre-session-rev-1"))
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    _assert_no_sentinels(payload)


def test_a_session_with_no_recorded_base_still_refuses_the_pre_session_pairing(tmp_path):
    """Degradation pin: an entry with no recorded base (opened before this
    wave, or a marker that could not be written) keeps the original
    name-equality binding -- honest refusal, never a crash."""
    worktree = _session_worktree(tmp_path)
    base_text = (worktree / SESSION_CREATED_PATH).read_bytes().decode("utf-8")
    body = _session_turn()
    body["buffers"][1] = _buf(
        "document", SESSION_CREATED_PATH, base_text,
        base_ref="main", base_revision="pre-session-rev-1",
        base_hash=content_identity(base_text).hex, dirty=False)
    status, payload, _fake = _post_session_turn(
        tmp_path, body, worktree=worktree)
    _assert_refusal(status, payload, "turn_scope_refused")
    _assert_no_sentinels(payload)


# ---- CHK012: the request cannot declare its own created set -----------------

def _forged(document):
    """Every plausible spelling a client could reach for, all at once: the
    top-level snake_case and camelCase names the server-side and browser-side
    overlays actually use, and a nested one inside the scope object."""
    return {
        "created_paths": [document],
        "createdDocuments": [document],
        "created_documents": [document],
        "scope": {"repository": "fixture-repo", "ref": SESSION_BRANCH,
                  "tile_kind": "staged", "tile_id": SESSION_TILE_ID,
                  "created_paths": [document], "createdDocuments": [document]},
    }


def test_a_request_cannot_declare_a_created_path_inside_a_live_session(tmp_path):
    """The session is live and HAS a created record -- for a different document.
    The request names its own and is refused: by SCOPE when the body is
    otherwise clean, and by the released SCHEMA when it carries the forged
    keys."""
    worktree = _session_worktree(tmp_path)
    status, payload, fake = _post_session_turn(
        tmp_path, _session_turn(SESSION_UNRECORDED_PATH), worktree=worktree)
    _assert_refusal(status, payload, "turn_scope_refused")
    _assert_no_sentinels(payload)

    body = _session_turn(SESSION_UNRECORDED_PATH,
                         **_forged(SESSION_UNRECORDED_PATH))
    status, payload, fake = _post_session_turn(tmp_path, body, worktree=worktree)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)
    assert fake.calls == []


def test_a_request_cannot_declare_a_created_path_with_no_session_at_all(tmp_path):
    """On `main` there is no session, so the created set is empty whatever the
    body says."""
    clean = _turn(
        active_document_path=READABLE_ONLY_PATH,
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
            _buf("document", READABLE_ONLY_PATH, "# Doc\n\n" + _S_DOCUMENT),
        ],
    )
    status, payload, _fake_port = _post_turn(tmp_path, clean)
    _assert_refusal(status, payload, "turn_scope_refused")
    _assert_no_sentinels(payload)

    forged = dict(clean, created_paths=[READABLE_ONLY_PATH],
                  createdDocuments=[READABLE_ONLY_PATH])
    status, payload, fake = _post_turn(tmp_path, forged)
    _assert_refusal(status, payload, "invalid_turn_request")
    _assert_no_sentinels(payload)
    assert fake.calls == []


def test_a_forged_created_path_cannot_escape_the_session_root(tmp_path):
    worktree = _session_worktree(tmp_path)
    for document in ("../../../etc/passwd", ".git/config",
                     "ideation/brainstorm/../../escape.md"):
        # Clean body: SCOPE refuses the traversal-shaped document path.
        status, payload, _fake = _post_session_turn(
            tmp_path, _session_turn(document), worktree=worktree)
        _assert_refusal(status, payload, "turn_scope_refused")
        # Same path, forged created-set keys: the released CLOSED envelope
        # refuses it before scope is consulted at all.
        body = _session_turn(document, **_forged(document))
        status, payload, fake = _post_session_turn(
            tmp_path, body, worktree=worktree)
        _assert_refusal(status, payload, "invalid_turn_request")
        assert fake.calls == []


def test_a_declared_created_path_does_not_survive_alongside_a_real_one(tmp_path):
    """The REAL created path still works in the same request that forges a
    second one -- the server's set is exactly its record, no more."""
    worktree = _session_worktree(tmp_path)
    # The REAL created path COMPLETES on a clean body (PIN EVOLUTION, T051
    # dispatch arm: was the boundary's fixed refusal)...
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(SESSION_CREATED_PATH), worktree=worktree)
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS

    # ...while the forged one is refused on a clean body by SCOPE...
    status, payload, _fake = _post_session_turn(
        tmp_path, _session_turn(SESSION_UNRECORDED_PATH), worktree=worktree)
    _assert_refusal(status, payload, "turn_scope_refused")

    # ...and mixing a real path with a forged declaration no longer buys the
    # caller anything at all: the whole request is refused by the SCHEMA, so
    # the declaration cannot even be evaluated, let alone honoured.
    for document in (SESSION_CREATED_PATH, SESSION_UNRECORDED_PATH):
        other = (SESSION_UNRECORDED_PATH if document == SESSION_CREATED_PATH
                 else SESSION_CREATED_PATH)
        body = _session_turn(document, **_forged(other))
        status, payload, fake = _post_session_turn(tmp_path, body, worktree=worktree)
        _assert_refusal(status, payload, "invalid_turn_request")
        assert fake.calls == []


# ============================================================================
# INTEGRATION RUNG: the routes against the REAL released contract-v1.27 bytes
#
# Env-gated on OPENXFACTORY_ROOT and skipping LOUDLY, exactly as
# test_doxbench_contracts.py's own integration rung does -- the hermetic rung
# above must never depend on a pinned openxFactory checkout being present, and
# this rung is the only place the released bytes are read. Run it with
#
#     OPENXFACTORY_ROOT=/workspace/projects/xFactory/openxFactory-worktrees/contract-v1.27
#
# The validators here are the REAL ones (digest-verified, manifest-checked,
# `stack.yaml`-parity-checked by `doxbench_contracts`), so what this rung proves
# is CONFORMANCE, not merely internal consistency. Every semantic rule the shape
# cannot express stays the delegated openxFactory validator's.
# ============================================================================

# Runs by DEFAULT from a publisher checkout: this suite is hosted inside
# openxFactory, so the released bytes are present and the rung has no reason to
# be opt-in. `OPENXFACTORY_ROOT` still selects a different checkout when one is
# wanted. While this was env-gated ONLY, the publisher-mode refusal that killed
# both model routes sat green here for a week — every one of these probes
# skipped, and the break surfaced as a runtime 500 instead
# (align-doxbench-contract-pin-to-publisher, 2026-08-10).
contracts_env = doxbench_contracts.OPENXFACTORY_ROOT_ENV
_RELEASED_ROOT = os.environ.get(contracts_env) or (
    str(doxbench_contracts.REPO_ROOT)
    if doxbench_contracts.is_publisher_checkout(doxbench_contracts.REPO_ROOT)
    else None)

released_only = pytest.mark.skipif(
    not _RELEASED_ROOT,
    reason=(f"set {contracts_env}=<checkout at {doxbench_contracts.CONTRACT_TAG}>, "
            f"or run from a publisher checkout, to run the released-contract "
            f"integration rung"),
)


@pytest.fixture(scope="module")
def released_validators():
    """The REAL per-kind validators, loaded ONCE for this module: the load
    verifies digests, manifest parity, and the declared `stack.yaml` ref, and
    there is nothing per-test about that verdict."""
    return doxbench_contracts.validators()


def _released_turn(**over):
    """A turn body that the RELEASED request schema accepts.

    Two deliberate departures from `_turn()`, both forced by the released
    envelope rather than chosen: `active_document_path` is a STRING (the release
    requires one -- see the nullability tripwire below), and the document buffer
    carries that same path, because `revalidate_scope` requires the two to be
    equal. The fixture tile's only editable document IS its README, so both
    buffers name it."""
    content = "# Outline\n\n" + _S_OUTLINE
    body = _turn(
        active_document_path=OUTLINE_PATH,
        buffers=[
            _buf("outline", OUTLINE_PATH, content),
            _buf("document", OUTLINE_PATH, content),
        ],
    )
    body.update(over)
    return body


@released_only
def test_the_default_validator_factory_loads_every_released_kind(released_validators):
    """RE-PINNED at contract-v1.34 (add-doxbench-editing-phase-b §13): the file
    now holds SIX turn envelopes, not three. The v1 kinds stay in the set
    deliberately -- they are DEPRECATED, not withdrawn, and a factory that
    stopped loading them would refuse exactly the clients the deprecation exists
    to keep working."""
    assert set(released_validators) == {
        doxbench_contracts.KIND_MODEL_CATALOG,
        doxbench_contracts.KIND_CHAT_TURN,
        doxbench_contracts.KIND_CHAT_TURN_SUCCESS,
        doxbench_contracts.KIND_CHAT_TURN_FAILURE,
        doxbench_contracts.KIND_CHAT_TURN_V2,
        doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS,
        doxbench_contracts.KIND_CHAT_TURN_V2_FAILURE,
    }
    # And `build_server`'s default seam is the very function that loads them.
    assert serve_mod.default_doxbench_validators() .keys() == released_validators.keys()


@released_only
def test_the_catalog_success_body_conforms_to_the_released_catalog_schema(
        tmp_path, released_validators):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port,
                 schema_validator_factory=doxbench_contracts.validators) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert doxbench_contracts.validate_instance(payload) == []
    assert payload["kind"] == doxbench_contracts.KIND_MODEL_CATALOG


@released_only
def test_the_empty_catalog_posture_conforms_to_the_released_catalog_schema(
        tmp_path, released_validators):
    with _serving(tmp_path,
                 schema_validator_factory=doxbench_contracts.validators) as (httpd, host, p):
        caps = _capabilities(host, p)
        status, payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers=_console_headers(caps))
    assert status == 200
    assert payload == _EMPTY_CATALOG_ENVELOPE
    assert doxbench_contracts.validate_instance(payload) == []


@released_only
def test_a_released_valid_turn_refuses_with_a_conformant_failure_envelope(
        tmp_path, released_validators):
    """A request the RELEASED schema accepts reaches the dispatch boundary and
    is refused there -- and the refusal is itself a conformant released
    `workbench-chat-turn-failure` instance. PIN EVOLUTION (T051 dispatch
    arm): the boundary refusal now requires the catalog-only adapter shape;
    the dispatch-capable success side has its own released-conformance
    test."""
    fake = _CatalogOnlyPort()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=doxbench_contracts.validators) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        body = _released_turn()
        assert doxbench_contracts.validate_instance(body) == []
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=body, headers=_console_headers(caps))
    _assert_refusal(status, payload, "model_capability_unavailable")
    assert doxbench_contracts.validate_instance(payload) == []
    _assert_no_sentinels(payload)


@released_only
def test_a_scope_refusal_conforms_to_the_released_failure_schema(
        tmp_path, released_validators):
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=doxbench_contracts.validators) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        body = _released_turn(scope={"repository": "fixture-repo", "ref": "main",
                                    "tile_kind": "staged", "tile_id": "no-such-tile"})
        assert doxbench_contracts.validate_instance(body) == []
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=body, headers=_console_headers(caps))
    _assert_refusal(status, payload, "turn_scope_refused")
    assert doxbench_contracts.validate_instance(payload) == []
    assert fake.calls == []


@released_only
def test_an_over_long_turn_id_is_refused_and_cannot_reach_a_released_envelope(
        tmp_path, released_validators):
    """The released bound on `client_turn_id` is 1..128. An id past it is
    refused by the request schema AND cannot appear in a failure envelope, so
    the refusal falls back to the fixed shape -- the fail-closed direction,
    proven against the real bound rather than a restated one."""
    body = _released_turn(client_turn_id="t" * 129)
    assert doxbench_contracts.validate_instance(body) != []
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=doxbench_contracts.validators) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=body, headers=_console_headers(caps))
    _assert_preidentity_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


@released_only
def test_an_unknown_top_level_key_is_refused_by_the_released_closed_envelope(
        tmp_path, released_validators):
    body = _released_turn(created_paths=[OUTLINE_PATH])
    assert doxbench_contracts.validate_instance(body) != []
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=doxbench_contracts.validators) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=body, headers=_console_headers(caps))
    _assert_refusal(status, payload, "invalid_turn_request")
    assert doxbench_contracts.validate_instance(payload) == []
    assert fake.calls == []


# ---- KNOWN CONTRACT GAP: a TRIPWIRE, not a ruling --------------------------

@released_only
def test_the_released_request_schema_accepts_a_null_active_document_path(
        tmp_path, released_validators):
    """FLIPPED at contract-v1.28 (2026-08-02) — the gap this tripwire guarded
    is closed.

    History: at contract-v1.27 `buffer_state.path` was nullable but
    `active_document_path` kept the non-nullable `confined_path`, so a turn
    about a not-yet-created document could not be expressed on the wire. This
    test asserted that REFUSAL so the gap could not be forgotten, and its
    docstring named the flip condition.

    The flip condition was met by finding G-1 (codexFactory PR #63
    re-verification, reviewer Brett Heap): measured on the real corpus, 16 of
    21 staged topics have exactly ONE editable path — the topic's own primary
    fragment, loaded as the OUTLINE — so requiring a non-null value made a
    legal turn impossible on ~76% of real topics. contract-v1.28 gives
    `active_document_path` the same nullability `buffer_state.path` has.

    As the original docstring predicted, the route needed NO change: it only
    ever delegated the verdict to the pinned schema. This test now asserts
    ACCEPTANCE of the null pairing — an outline-only turn is legal on the
    wire and reaches dispatch."""
    null_document = _turn()  # the hermetic default: null active path, null document path
    assert null_document["active_document_path"] is None
    errors = doxbench_contracts.validate_instance(null_document)
    assert not errors, (
        "contract-v1.28 makes active_document_path nullable; a null pairing "
        f"must validate: {errors}")

    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=doxbench_contracts.validators) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=null_document,
            headers=_console_headers(caps))
    # The turn now COMPLETES: the route only ever delegated the verdict to the
    # pinned schema, so widening the schema was the whole fix — exactly what
    # the pre-flip docstring predicted ("the route needs no change at all").
    assert status == 200, (status, payload)
    assert payload.get("kind") == "workbench-chat-turn-success", payload
    assert doxbench_contracts.validate_instance(payload) == []
    # The port IS consulted now: pre-flip this asserted `== []` because the
    # schema refused before dispatch could ever be reached.
    assert fake.calls == ["catalog", "dispatch"], fake.calls


# ============================================================================
# T051 dispatch arm: a dispatch-capable port now completes a fully valid turn
# with the RELEASED success envelope; every provider outcome maps through
# doxbench_model.dispatch_turn's fixed codes; a port WITHOUT a dispatch
# member keeps the refused-by-absence posture byte-identically. Production
# remains refused-by-absence: no real adapter exists in this repository
# (T099 is operator-gated), so the success path below is reachable only with
# an injected fake.
# ============================================================================


class _CatalogOnlyPort:
    """The pre-T049 adapter surface: `timeout_seconds` + `catalog()` and NO
    dispatch member. T049 widened the PROTOCOL and the fake, so the
    refused-by-absence posture needs this explicit catalog-only adapter to
    stay testable -- it is the exact shape a deployment without an approved
    dispatch adapter presents."""

    timeout_seconds = 30.0

    def __init__(self, catalog=None):
        self._catalog = catalog if catalog is not None else _catalog()
        self.calls = []

    def catalog(self):
        self.calls.append("catalog")
        return self._catalog


_RELEASED_SUCCESS_KEYS = {
    "schema_version", "kind", "client_turn_id", "assistant_turn_id",
    "model_id", "observed_hashes", "assistant_prose", "proposals",
}


def test_a_valid_turn_with_a_dispatch_capable_port_returns_the_released_success(tmp_path):
    status, payload, fake = _post_turn(tmp_path, _turn())
    assert status == 200
    assert set(payload) == _RELEASED_SUCCESS_KEYS
    assert payload["schema_version"] == 1
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    assert payload["client_turn_id"] == "turn-0001"
    assert payload["model_id"] == "model-a"
    assert payload["assistant_prose"] == "fake grounded answer"
    assert payload["proposals"] == []
    assert set(payload["observed_hashes"]) == {"outline", "document"}
    for value in payload["observed_hashes"].values():
        assert isinstance(value, str)
        assert len(value) == 64
        assert all(c in "0123456789abcdef" for c in value)
    assert isinstance(payload["assistant_turn_id"], str)
    assert 1 <= len(payload["assistant_turn_id"]) <= 128
    # Delegation-only: exactly ONE dispatch, and it is the LAST port touch --
    # every precondition (catalog consult included) ran before it.
    assert fake.calls.count("dispatch") == 1
    assert fake.calls[-1] == "dispatch"
    _assert_no_sentinels(payload)


# ---------------------------------------------------------------------------
# G-1 (PR #63 re-verification, 2026-08-02): THE OUTLINE-ONLY TURN, end to end
#
# The fixture tile IS the real-corpus majority shape — `resolve_scope` gives it
# exactly one editable path, its own README, which the canvas loads as the
# OUTLINE and which T104 F2 therefore does not offer as a DOCUMENT, so its
# candidate set is empty. Every `_turn()` in this file is consequently an
# outline-only turn: `active_document_path` is null and the document buffer
# carries the not-yet-created null path. These tests SAY that, so the chain
# derivation -> guard -> route is pinned as the G-1 acceptance case rather than
# passing by accident, and pin the proposal semantics such a turn carries.
# ---------------------------------------------------------------------------

def test_the_fixture_tile_is_the_single_document_shape_g1_measured(tmp_path):
    """The route's own snapshot, through the real scope authority."""
    from ideation_dashboard.doxbench_scope import resolve_scope
    projection = resolve_scope(_snapshot(), KEY, source_root=BASE_REPO)
    assert projection is not None
    assert projection.editable_paths == (OUTLINE_PATH,)
    assert projection.outline_path == OUTLINE_PATH
    assert projection.active_document_candidates == ()


def test_an_outline_only_turn_completes_end_to_end(tmp_path):
    """derivation -> guard -> route, with no document named anywhere: the turn
    is answered, not refused. This is the case that was impossible before
    contract-v1.28 made `active_document_path` nullable."""
    body = _turn()
    assert body["active_document_path"] is None
    assert body["buffers"][1]["path"] is None
    status, payload, fake = _post_turn(tmp_path, body)
    assert status == 200, payload
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    assert fake.calls.count("dispatch") == 1


def test_an_outline_only_turn_may_carry_an_outline_proposal(tmp_path):
    proposal = {"target": "outline", "base_hash": _outline_digest(),
                "summary": "Tighten the outline",
                "content": "# Outline rewritten\n"}
    port = FakeWorkbenchModelPort(_catalog(), dispatch_result={
        "assistant_prose": "here is a proposal", "proposals": [proposal]})
    status, payload, _port = _post_turn(tmp_path, _turn(), port=port)
    assert status == 200
    assert payload["proposals"] == [proposal]


def test_an_outline_only_turn_refuses_a_document_targeted_proposal(tmp_path):
    """The narrowest reading of a silent contract, recorded: a turn that names
    NO document carries no document-targeted proposal — it would be a rewrite
    of a document that does not exist. A RESPONSE defect (the request was
    fine), so it maps to the fixed `response_invalid`, and the same proposal is
    accepted on a turn that DOES name a document (pinned in
    test_doxbench_turns.py)."""
    document_content = "# Document\n\n" + _S_DOCUMENT
    proposal = {"target": "document",
                "base_hash": content_identity(document_content).hex,
                "summary": "Rewrite a document this turn never named",
                "content": "# Drift\n"}
    port = FakeWorkbenchModelPort(_catalog(), dispatch_result={
        "assistant_prose": "x", "proposals": [proposal]})
    status, payload, _port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "response_invalid")


# RE-ENABLED 2026-08-10 (align-doxbench-contract-pin-to-publisher). This was
# deferred behind "the pin advances to the bundle carrying the G-1 nullability
# amendment" while the pin named contract-v1.27; the amendment landed AT
# contract-v1.28 and the pin now names contract-v1.31, so the stated signal has
# fired. It went unnoticed because the released rung it belongs to was itself
# opt-in — a skip waiting on a signal nobody could observe. The assertion is
# unchanged, exactly as the deferral required.
@released_only
def test_the_outline_only_request_conforms_to_the_released_schema(
        tmp_path, released_validators):
    body = _turn()
    assert body["active_document_path"] is None
    assert doxbench_contracts.validate_instance(body) == []


def test_a_catalog_only_port_keeps_the_fixed_capability_refusal_byte_identically(tmp_path):
    """The refused-by-absence posture is UNCHANGED in shape and code: this is
    the tripwire that proves T051's arm dispatches only when an adapter
    actually declares the capability."""
    port = _CatalogOnlyPort()
    status, payload, port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "model_capability_unavailable")
    assert "dispatch" not in port.calls
    _assert_no_sentinels(payload)


def test_the_completed_success_is_stored_and_replayed_with_exactly_one_dispatch(tmp_path):
    body = _turn()
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake)) as (httpd, host, port_num):
        caps = _capabilities(host, port_num)
        status1, payload1, _headers1, raw1 = _request(
            host, port_num, "POST", CHAT_ROUTE, body=body,
            headers=_console_headers(caps))
        status2, payload2, _headers2, raw2 = _request(
            host, port_num, "POST", CHAT_ROUTE, body=body,
            headers=_console_headers(caps))
        record = _handler_class(httpd).turn_store.snapshot(KEY, "turn-0001")
    assert status1 == status2 == 200
    assert raw1 == raw2
    assert payload1["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    assert record.state == doxbench_turns.TURN_STATE_COMPLETED
    assert fake.calls.count("dispatch") == 1


def test_a_provider_exception_maps_to_model_failed_and_discloses_nothing(tmp_path):
    port = FakeWorkbenchModelPort(
        _catalog(), dispatch_error=RuntimeError("secret-key-material-9x7"))
    status, payload, port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "model_failed")
    assert "secret-key-material-9x7" not in json.dumps(payload)
    _assert_no_sentinels(payload)


def test_a_malformed_provider_payload_maps_to_response_invalid(tmp_path):
    port = FakeWorkbenchModelPort(
        _catalog(), dispatch_result={"unexpected": True})
    status, payload, port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "response_invalid")


def test_an_oversize_provider_payload_maps_to_response_invalid(tmp_path):
    port = FakeWorkbenchModelPort(
        _catalog(),
        dispatch_result={"assistant_prose": "a" * 65_537, "proposals": []})
    status, payload, port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "response_invalid")


def test_a_dispatch_failure_finalizes_the_slot_as_failed_and_frees_it(tmp_path):
    """The refused-finalization obligation holds for PROVIDER outcomes too:
    a model_failed turn frees the conversation slot for a fresh id."""
    with _serving(tmp_path, model_port_factory=(
            lambda: FakeWorkbenchModelPort(
                _catalog(), dispatch_error=RuntimeError("boom")))) as (
            httpd, host, port_num):
        caps = _capabilities(host, port_num)
        status1, payload1, _headers1, _raw1 = _request(
            host, port_num, "POST", CHAT_ROUTE, body=_turn(),
            headers=_console_headers(caps))
        record = _handler_class(httpd).turn_store.snapshot(KEY, "turn-0001")
        status2, payload2, _headers2, _raw2 = _request(
            host, port_num, "POST", CHAT_ROUTE,
            body=_turn(client_turn_id="turn-0002"),
            headers=_console_headers(caps))
    _assert_refusal(status1, payload1, "model_failed")
    assert record.state == doxbench_turns.TURN_STATE_FAILED
    assert payload2["error"] != "turn_in_flight"


def test_the_three_dispatch_outcome_codes_join_the_fixed_error_catalog():
    """Spelling parity with doxbench_model's closed dispatch-code set, plus
    this slice's own judgement-call statuses: 504 for the deadline outcome
    (gateway-timeout semantics), 502 for adapter failure and for an invalid
    provider response (bad-gateway semantics: the upstream answered
    unusably). Messages are fixed and module-level like every other entry."""
    catalog = serve_mod.DOXBENCH_ERROR_CATALOG
    from ideation_dashboard import doxbench_model as model_mod
    assert catalog[model_mod.DISPATCH_ERR_MODEL_TIMEOUT][0] == 504
    assert catalog[model_mod.DISPATCH_ERR_MODEL_FAILED][0] == 502
    assert catalog[model_mod.DISPATCH_ERR_RESPONSE_INVALID][0] == 502
    for code in (model_mod.DISPATCH_ERR_MODEL_TIMEOUT,
                 model_mod.DISPATCH_ERR_MODEL_FAILED,
                 model_mod.DISPATCH_ERR_RESPONSE_INVALID):
        message = catalog[code][1]
        assert isinstance(message, str) and message
        assert "{" not in message and "}" not in message


@released_only
def test_the_success_envelope_validates_against_the_released_schema(
        tmp_path, released_validators):
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                 schema_validator_factory=doxbench_contracts.validators) as (
            httpd, host, prt):
        caps = _capabilities(host, prt)
        body = _released_turn()
        assert doxbench_contracts.validate_instance(body) == []
        status, payload, _headers, _raw = _request(
            host, prt, "POST", CHAT_ROUTE, body=body,
            headers=_console_headers(caps))
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    assert doxbench_contracts.validate_instance(payload) == []


# ---------------------------------------------------------------------------
# T061 closure: the dispatch arm passes VALIDATED typed proposals through to
# the released success envelope; a defective proposal payload maps to the
# fixed response_invalid refusal. The validator is doxbench_turns'
# validate_assistant_response, bound to the request's own observed hashes.
# ---------------------------------------------------------------------------

def _outline_digest():
    return content_identity("# Outline\n\n" + _S_OUTLINE).hex


def test_a_validated_proposal_flows_into_the_released_success_envelope(tmp_path):
    proposal = {"target": "outline", "base_hash": _outline_digest(),
                "summary": "Tighten the outline",
                "content": "# Outline rewritten\n"}
    port = FakeWorkbenchModelPort(_catalog(), dispatch_result={
        "assistant_prose": "here is a proposal", "proposals": [proposal]})
    status, payload, _port = _post_turn(tmp_path, _turn(), port=port)
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    assert payload["proposals"] == [proposal]
    assert set(payload["proposals"][0]) == {
        "target", "base_hash", "summary", "content"}


def test_a_wrong_base_proposal_maps_to_response_invalid_at_the_route(tmp_path):
    proposal = {"target": "outline", "base_hash": "f" * 64,
                "summary": "Bound to content the model never saw",
                "content": "# Drift\n"}
    port = FakeWorkbenchModelPort(_catalog(), dispatch_result={
        "assistant_prose": "x", "proposals": [proposal]})
    status, payload, _port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "response_invalid")


def test_a_duplicate_target_proposal_payload_is_refused_at_the_route(tmp_path):
    proposal = {"target": "outline", "base_hash": _outline_digest(),
                "summary": "s", "content": "# A\n"}
    port = FakeWorkbenchModelPort(_catalog(), dispatch_result={
        "assistant_prose": "x", "proposals": [proposal, dict(proposal)]})
    status, payload, _port = _post_turn(tmp_path, _turn(), port=port)
    _assert_refusal(status, payload, "response_invalid")


# ---------------------------------------------------------------------------
# PR #63 review response (Codex P1, doxbench_model.py:535): the route's
# dispatch arm enforces the adapter deadline WHILE dispatch runs — a hung
# adapter yields the fixed model_timeout, frees the slot, and cannot pin the
# conversation for the process lifetime.
# ---------------------------------------------------------------------------

class _HangingPort:
    timeout_seconds = 0.2  # declared deadline: 200ms

    def __init__(self, catalog=None):
        self._catalog = catalog if catalog is not None else _catalog()
        self.calls = []
        self.release = threading.Event()

    def catalog(self):
        self.calls.append("catalog")
        return self._catalog

    def dispatch(self, prompt_envelope):
        self.calls.append("dispatch")
        # Hang far past the declared deadline unless released.
        self.release.wait(timeout=10.0)
        return {"assistant_prose": "too late", "proposals": []}


def test_a_hung_adapter_times_out_at_the_declared_deadline_and_frees_the_slot(tmp_path):
    port = _HangingPort()
    try:
        with _serving(tmp_path, model_port_factory=(lambda: port)) as (httpd, host, port_num):
            caps = _capabilities(host, port_num)
            status1, payload1, _h1, _r1 = _request(
                host, port_num, "POST", CHAT_ROUTE, body=_turn(),
                headers=_console_headers(caps))
            record = _handler_class(httpd).turn_store.snapshot(KEY, "turn-0001")
            status2, payload2, _h2, _r2 = _request(
                host, port_num, "POST", CHAT_ROUTE,
                body=_turn(client_turn_id="turn-0002"),
                headers=_console_headers(caps))
    finally:
        port.release.set()
    _assert_refusal(status1, payload1, "model_timeout")
    assert record.state == doxbench_turns.TURN_STATE_FAILED
    # The slot is FREE: a fresh id proceeds (also times out, but is not
    # refused turn_in_flight — the hung first turn did not pin the key).
    assert payload2["error"] != "turn_in_flight"


# ---------------------------------------------------------------------------
# T098 finding fix (operator ruling (a), spec Clarifications 2026-07-31): a
# console-token-BEARING GET is non-simple (the custom header forces a CORS
# preflight), so the gate accepts it without a JSON Content-Type. Validity,
# Host, and origin checks are unchanged.
# ---------------------------------------------------------------------------

def test_a_tokenless_untyped_request_keeps_the_simple_request_refusal(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        status, _payload, _headers, _raw = _request(
            host, p, "GET", ROUTE, headers={})
    assert status == 403


def test_a_wrong_token_bearing_get_still_refuses_on_validity(tmp_path):
    port = FakeWorkbenchModelPort(_two_entry_catalog())
    with _serving(tmp_path, model_port_factory=lambda: port) as (httpd, host, p):
        status, _payload, _headers, _raw = _request(
            host, p, "GET", ROUTE,
            headers={"X-XF-Console-Token": "forged-token-value"})
    assert status == 403


# ---------------------------------------------------------------------------
# THE WIDENED FAMILY ON THE ROUTE (contract-v1.34;
# add-doxbench-editing-phase-b tasks 13.1/13.4/13.5)
#
# The route serves BOTH released families and answers a turn in the family it
# arrived in. The v1 lane above is unchanged and stays exercised by every test
# in this module; these pin the widened one -- most importantly that the durable
# RECORD names the binding the REQUEST DECLARED, which is the F2 obligation
# Phase A deferred against exactly this release.
# ---------------------------------------------------------------------------

_RELEASED_V2_SUCCESS_KEYS = {
    "schema_version", "kind", "client_turn_id", "assistant_turn_id",
    "model_id", "selected_model", "bound_buffer", "observed_hashes",
    "assistant_prose", "proposals",
}


def _turn_v2(**over):
    """A widened turn over the same fixture tile: the outline plus the reserved
    not-yet-created document slot, with the binding DECLARED rather than implied
    by an active-document path (which this envelope does not carry)."""
    body = {
        "schema_version": 1,
        "kind": doxbench_contracts.KIND_CHAT_TURN_V2,
        "client_turn_id": "turn-v2-0001",
        "scope": {"repository": "fixture-repo", "ref": "main",
                  "tile_kind": "staged", "tile_id": "ideation-governance"},
        "bound_buffer": "outline",
        "working_subject": "Clarify the acceptance boundary " + _S_SUBJECT,
        "message": "Which open question should we close next? " + _S_MESSAGE,
        "model_id": "model-a",
        "last_assistant_turn_id": None,
        "transcript": [],
        "buffers": [
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
            _buf("document", None, "# Document\n\n" + _S_DOCUMENT),
        ],
    }
    body.update(over)
    return body


def test_a_widened_turn_returns_the_widened_record_naming_its_declared_binding(
        tmp_path):
    """THE F2 OBLIGATION, discharged and measured on the RECORD.

    The turn is bound to the OUTLINE while a document buffer rides beside it --
    precisely the case Phase A's review found mis-recorded, because the binding
    was derived from which document happened to be supplied. The record names
    what the request DECLARED."""
    status, payload, fake = _post_turn(tmp_path, _turn_v2())
    assert status == 200
    assert set(payload) == _RELEASED_V2_SUCCESS_KEYS
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS
    assert payload["client_turn_id"] == "turn-v2-0001"
    assert payload["bound_buffer"] == "outline"
    # Keyed by BUFFER KEY, one per buffer the turn carried.
    assert set(payload["observed_hashes"]) == {"outline", "document"}
    for value in payload["observed_hashes"].values():
        assert isinstance(value, str) and len(value) == 64
    # The selected-model metadata beside the model that answered.
    assert payload["model_id"] == "model-a"
    assert payload["selected_model"] == {
        "requested_model_id": "model-a",
        "routing_rule": False,
        "data_handling": "Processed in the approved tenant boundary",
    }
    assert fake.calls.count("dispatch") == 1
    assert fake.calls[-1] == "dispatch"
    _assert_no_sentinels(payload)


def test_a_widened_turn_bound_to_a_supplied_document_records_that_key(tmp_path):
    """The other binding, over the same buffer set: what changes in the record is
    the declared key and NOTHING else, which is what makes the record a statement
    about the conversation rather than about the buffer list."""
    status, payload, _fake = _post_turn(
        tmp_path, _turn_v2(client_turn_id="turn-v2-0002",
                           bound_buffer="document"))
    assert status == 200
    assert payload["bound_buffer"] == "document"
    assert set(payload["observed_hashes"]) == {"outline", "document"}


def test_a_widened_turn_whose_binding_names_no_supplied_buffer_is_refused(
        tmp_path):
    """The generalized active-path revalidation: refused BEFORE any provider
    call, and answered in the family the request arrived in."""
    status, payload, fake = _post_turn(
        tmp_path, _turn_v2(bound_buffer="ideation/staging/ideation-governance/"
                                        "never-supplied.md"))
    _assert_v2_refusal(status, payload, "turn_scope_refused")
    # Scope revalidation is step 5: no port member is consulted at all.
    assert fake.calls == []
    _assert_no_sentinels(payload)


def test_a_deprecated_v1_turn_is_still_served_in_its_own_family(tmp_path):
    """The deprecation's whole promise: the older shape keeps working, and it is
    answered in ITS envelope -- never in the widened one, which carries fields a
    v1 client has no reader for."""
    status, payload, _fake = _post_turn(tmp_path, _turn())
    assert status == 200
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    assert "bound_buffer" not in payload
    assert "selected_model" not in payload


@released_only
def test_both_families_conform_to_the_released_schema_on_the_wire(
        tmp_path, released_validators):
    """Requests and records from BOTH families validate against the released
    bytes -- the co-residence claim, executed rather than described."""
    v2_request = _turn_v2()
    assert doxbench_contracts.validate_instance(v2_request) == []
    assert doxbench_contracts.validate_instance(_turn()) == []
    status, payload, _fake = _post_turn(tmp_path, v2_request)
    assert status == 200
    assert doxbench_contracts.validate_instance(payload) == []
    status, payload, _fake = _post_turn(tmp_path, _turn())
    assert status == 200
    assert doxbench_contracts.validate_instance(payload) == []


# ---------------------------------------------------------------------------
# A SECOND FIXTURE TILE: the same staged topic, widened to hold MORE THAN ONE
# EDITABLE DOCUMENT (adversarial review of the §13 slice, F2 and F5).
#
# The default fixture tile is the G-1 single-document shape — `editable_paths ==
# (OUTLINE_PATH,)` — which is the right default and is pinned as such above. It
# also means every turn this module posts carries exactly one document buffer,
# so the widened lane's own arithmetic (the per-document identity loop, the
# per-document byte bound, an observed-hash map with three keys) was never
# actually driven, and a buffer whose path claims a RESERVED KEY was refused by
# scope confinement long before it could reach the requirement that must refuse
# it.
#
# The extra documents join the topic's OWN FILES rather than its inbound
# destinations, because only the topic's own section is `owned` and therefore
# editable — which is the scope authority's rule, read off it rather than
# assumed.
# ---------------------------------------------------------------------------

def _staged_document(path):
    return {
        "id": path, "path": path, "stage": "staged", "kind": "staging-packet",
        "summary": "fixture document for the widened-lane tests",
        "topics": ["ideation-governance"],
        "dates": {"captured": "2026-08-18"},
        "destinations": {"staged_topics": ["ideation-governance"]},
        "completeness": {
            "score": 0.6,
            "structure": {"value": 1.0, "count": 3},
            "length": {"value": 1.0, "count": 45},
            "open_markers": {"value": 1.0, "count": 0},
            "keyword_coverage": {"value": 1.0, "count": 1},
            "link_degree": {"value": 1.0, "count": 2},
        },
    }


def _snapshot_with_editable(*paths):
    """The fixture snapshot with `paths` added to the tile's OWN material, so the
    scope authority resolves each one as in-scope AND editable."""
    snapshot = copy.deepcopy(_snapshot())
    snapshot["documents"] = list(snapshot["documents"]) + [
        _staged_document(path) for path in paths]
    for topic in snapshot["staged_topics"]:
        if topic.get("staging_id") == "ideation-governance":
            topic["files"] = list(topic["files"]) + list(paths)
    return snapshot


DOC_ALPHA = "ideation/staging/ideation-governance/alpha.md"
DOC_ZULU = "ideation/staging/ideation-governance/zulu.md"


def test_the_widened_fixture_tile_really_is_editable_at_every_added_path():
    """The fixture's own precondition, through the real scope authority — so a
    test below that passes because a path was NOT editable cannot be mistaken for
    one that passes because the rule under test held."""
    from ideation_dashboard.doxbench_scope import resolve_scope
    projection = resolve_scope(
        _snapshot_with_editable("outline", "document", DOC_ALPHA, DOC_ZULU),
        KEY, source_root=BASE_REPO)
    assert projection is not None
    for path in ("outline", "document", DOC_ALPHA, DOC_ZULU):
        assert path in projection.editable_paths
        assert path in projection.context_paths
    # The outline buffer's own path is unmoved: the tile's primary fragment.
    assert projection.outline_path == OUTLINE_PATH


# ---------------------------------------------------------------------------
# F2 (adversarial review of the §13 slice): A DOCUMENT PATH THAT CLAIMS A
# RESERVED KEY IS REFUSED ON BOTH LANES, WITH AN ENVELOPE
#
# `buffer_key_for` maps a document buffer at path `outline` onto the reserved
# outline key; `ordered_document_keys` filters that key OUT of the document
# enumeration. So the buffer passed the kind requirement and then vanished:
# step 6 never verified its declared content hash, step 7 never counted its bytes
# against the request bound, and the released v1 success builder indexed an empty
# document list — an uncaught IndexError, a dropped connection with NO envelope
# at all, and a stranded turn-store lease. On the widened lane it survived as far
# as the provider and came back mislabelled as a response defect.
#
# The refusal now lands in `require_outline_and_documents`, before identity
# verification and before any port. These tests prove the ENVELOPE, because "the
# connection dropped" is exactly what a passing status assertion cannot tell from
# a refusal — and they run against the widened fixture tile, where the claimed
# path is genuinely in scope and editable, so scope confinement cannot answer
# first and hide the hole.
# ---------------------------------------------------------------------------

# The reviewer's own repro shape: an oversize buffer whose declared content_hash
# CANNOT match its text. If identity verification ever ran on it, the refusal
# would be `content_identity_mismatch`; `invalid_turn_request` is the proof that
# the malformed-request verdict is reached first, which is where it belongs.
_RESERVED_CLAIM_CONTENT = "R" * 5010
_RESERVED_CLAIM_HASH = "f" * 64

_RESERVED_SNAPSHOT_PATHS = ("outline", "document")


def test_a_v1_turn_whose_document_path_claims_the_outline_key_is_refused(tmp_path):
    """The v1 half of the reserved-key refusal. NARROWED to the `outline`
    spelling by Codex review CODEX-1: that one is a CRASH class on this lane —
    reproduced at a4a6f6e as a dropped connection with no response — while the
    `document` spelling was SERVED there and keeps being served (below)."""
    body = _turn(active_document_path="outline", buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("document", "outline", _RESERVED_CLAIM_CONTENT,
             content_hash=_RESERVED_CLAIM_HASH),
    ])
    status, payload, fake = _post_turn(
        tmp_path, body,
        snapshot=_snapshot_with_editable(*_RESERVED_SNAPSHOT_PATHS))
    assert payload is not None, (
        "the connection must carry an envelope, never drop: an IndexError here "
        "stranded the turn-store lease and told the browser nothing")
    _assert_refusal(status, payload, "invalid_turn_request")
    # The buffer-set requirement is step 6; the model port is step 7. A malformed
    # request must reach neither.
    assert fake.calls == []
    _assert_no_sentinels(payload)


def test_a_v1_turn_whose_document_path_is_literally_document_is_still_served(
        tmp_path):
    """CODEX-1, the promise this release makes: a v1 client keeps being served.

    A repository-root file named exactly `document` is a legal editable path, and
    a v1 turn carrying it was SERVED at a4a6f6e — reproduced in a worktree at that
    commit: HTTP 200, dispatched. The v1 envelope carries exactly ONE document
    whose key is `document` whether its path is null or literally "document", so
    that lane has no collision to guard; refusing it would have been a breaking
    change wearing an additive release's number."""
    body = _turn(active_document_path="document", buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("document", "document", "# Doc\n\n" + _S_DOCUMENT),
    ])
    status, payload, fake = _post_turn(
        tmp_path, body,
        snapshot=_snapshot_with_editable(*_RESERVED_SNAPSHOT_PATHS))
    assert status == 200, payload
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_SUCCESS
    assert set(payload["observed_hashes"]) == {"outline", "document"}
    assert fake.calls.count("dispatch") == 1


@pytest.mark.parametrize("reserved", ["outline", "document"])
def test_a_v2_turn_whose_document_path_claims_a_reserved_key_is_refused(
        tmp_path, reserved):
    body = _turn_v2(bound_buffer="outline", buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("document", reserved, _RESERVED_CLAIM_CONTENT,
             content_hash=_RESERVED_CLAIM_HASH),
    ])
    status, payload, fake = _post_turn(
        tmp_path, body,
        snapshot=_snapshot_with_editable(*_RESERVED_SNAPSHOT_PATHS))
    assert payload is not None
    _assert_v2_refusal(status, payload, "invalid_turn_request")
    # BOTH spellings stay refused on THIS lane (CODEX-1): the widened envelope
    # can carry the reserved unbacked slot beside a path-backed document, so a
    # document at path `document` would shadow it — the collision the v1 lane
    # cannot have.
    #
    # BEFORE the provider, and before the CATALOG: on this lane the buffer used
    # to survive to dispatch and come back as `response_invalid`, which named the
    # model for a defect in the request.
    assert fake.calls == []
    _assert_no_sentinels(payload)


def test_the_reserved_key_refusal_leaves_the_turn_slot_reusable(tmp_path):
    """The stranded-lease half of F2, measured rather than argued: a refused turn
    must leave its conversation slot usable, which it cannot do if the handler
    died mid-lease."""
    claimed = _turn_v2(bound_buffer="outline", buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("document", "outline", _RESERVED_CLAIM_CONTENT,
             content_hash=_RESERVED_CLAIM_HASH),
    ])
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                  snapshot=_snapshot_with_editable(*_RESERVED_SNAPSHOT_PATHS)
                  ) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        first_status, first_payload, _h, _r = _request(
            host, prt, "POST", CHAT_ROUTE, body=claimed,
            headers=_console_headers(caps))
        # …and a well-formed turn on the same conversation goes through after it.
        second_status, second_payload, _h2, _r2 = _request(
            host, prt, "POST", CHAT_ROUTE, body=_turn_v2(client_turn_id="turn-v2-9"),
            headers=_console_headers(caps))
    assert first_payload["error"] == "invalid_turn_request"
    assert first_status == serve_mod.doxbench_error_status(
        serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST)
    assert second_status == 200, second_payload
    assert second_payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS


# ---------------------------------------------------------------------------
# F5: THE WIDENED LANE, ACTUALLY WIDE — outline plus TWO path-backed documents
# ---------------------------------------------------------------------------

def test_a_widened_turn_carries_two_path_backed_documents_end_to_end(tmp_path):
    """Every widened-lane mechanism the single-document fixture could not reach:
    the per-document identity loop, the per-document byte bound, an
    `observed_hashes` map with THREE keys, and a `bound_buffer` naming a
    path-keyed document rather than a reserved one."""
    body = _turn_v2(
        client_turn_id="turn-v2-wide",
        bound_buffer=DOC_ZULU,
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
            _buf("document", DOC_ALPHA, "# Alpha\n\n" + _S_DOCUMENT),
            _buf("document", DOC_ZULU, "# Zulu\n\nsecond loaded document"),
        ])
    status, payload, fake = _post_turn(
        tmp_path, body, snapshot=_snapshot_with_editable(DOC_ALPHA, DOC_ZULU))
    assert status == 200, payload
    assert payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS
    assert payload["bound_buffer"] == DOC_ZULU
    assert set(payload["observed_hashes"]) == {"outline", DOC_ALPHA, DOC_ZULU}
    for value in payload["observed_hashes"].values():
        assert isinstance(value, str) and len(value) == 64
    # The identities are each buffer's OWN recomputed hash, not one repeated.
    assert len(set(payload["observed_hashes"].values())) == 3
    assert fake.calls.count("dispatch") == 1
    _assert_no_sentinels(payload)


def test_a_widened_turn_verifies_every_documents_identity_not_just_the_first(
        tmp_path):
    """The per-document loop, proven by moving the SECOND document's declared
    hash: a loop that verified only the first would answer 200 here."""
    body = _turn_v2(
        client_turn_id="turn-v2-wide-2",
        bound_buffer=DOC_ALPHA,
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
            _buf("document", DOC_ALPHA, "# Alpha\n\n" + _S_DOCUMENT),
            _buf("document", DOC_ZULU, "# Zulu\n\nsecond loaded document",
                 content_hash="a" * 64),
        ])
    status, payload, fake = _post_turn(
        tmp_path, body, snapshot=_snapshot_with_editable(DOC_ALPHA, DOC_ZULU))
    _assert_v2_refusal(status, payload, "content_identity_mismatch")
    # NO PORT TOUCH AT ALL, not merely no dispatch: exact identity is step 6 and
    # the model step is 7, so a loop that verified only the first document and
    # went on to consult the catalog would satisfy "no dispatch" while breaking
    # the gate order this test is named for.
    assert fake.calls == []
    _assert_no_sentinels(payload)


def test_the_request_byte_bound_counts_every_loaded_document(tmp_path):
    """The byte bound over the SET: two documents that each fit the selected
    model's ceiling but together do not must refuse with the MEASURED TOTAL.

    The ceiling is narrowed through the catalog entry rather than reached with
    megabytes, because the point is the arithmetic — a bound that measured only
    the first document would report roughly half this number and answer 200."""
    half = "z" * 12_000
    body = _turn_v2(
        client_turn_id="turn-v2-wide-3",
        bound_buffer=DOC_ALPHA,
        buffers=[
            _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
            _buf("document", DOC_ALPHA, half),
            _buf("document", DOC_ZULU, half),
        ])
    status, payload, fake = _post_turn(
        tmp_path, body, port=_port(_catalog(input_limit_bytes=20_000)),
        snapshot=_snapshot_with_editable(DOC_ALPHA, DOC_ZULU))
    _assert_v2_refusal(status, payload, "request_limit_exceeded")
    assert payload["limit"]["dimension"] == "request_body_bytes"
    assert payload["limit"]["maximum"] == 20_000
    assert payload["limit"]["measured"] >= 24_000, (
        "both documents must be counted, not the first")
    # This bound is the SELECTED ENTRY's, so the catalog is legitimately consulted
    # before it can be applied — the one pre-dispatch refusal in this section that
    # is NOT `fake.calls == []`, stated so nobody tightens it into a false pin.
    assert fake.calls == ["catalog"]


# ---------------------------------------------------------------------------
# F6: the selected-model metadata is DERIVED from the catalog entry, in one place
# ---------------------------------------------------------------------------

def test_the_selected_model_metadata_reads_the_catalog_entry(tmp_path):
    """`doxbench_selected_model` is the one place task 11.7 has to change. It
    reads the entry duck-typed and defaults honestly, so today's catalog — which
    declares no routing rule, because the model-catalog envelope has no field for
    one yet — produces the true statement rather than a literal."""
    entry = _catalog().entries[0]
    assert serve_mod.doxbench_selected_model(entry) == {
        "requested_model_id": "model-a",
        "routing_rule": False,
        "data_handling": "Processed in the approved tenant boundary",
        "resolved_model_id": "model-a",
    }


def test_a_routing_rule_entry_would_be_reported_as_one_without_touching_the_route():
    """The forward half, proven on a stand-in entry that declares the fields task
    11.7 will add: the route needs no change to report a routing rule and the
    model it resolved to. A record built from three literals could not.

    KEPT VERBATIM ACROSS THE contract-v1.38 RELEASE, deliberately. The release
    made those fields declarable on the real type (see the sibling below) and
    this route was not touched — so this test passing unchanged IS the evidence
    that the one-place derivation was written correctly the first time."""

    class _RoutingEntry:
        model_id = "auto"
        data_handling = "Routes to any approved model; badge of all of them"
        routing_rule = True
        resolved_model_id = "model-a"

    assert serve_mod.doxbench_selected_model(_RoutingEntry()) == {
        "requested_model_id": "auto",
        "routing_rule": True,
        "data_handling": "Routes to any approved model; badge of all of them",
        "resolved_model_id": "model-a",
    }


def test_a_CONFORMANT_routing_entry_is_reported_as_one_without_touching_the_route():
    """The same derivation on a REAL `ModelCatalogEntry` — the shape
    contract-v1.38 made constructible (task 11.7). `doxbench_selected_model` is
    byte-identical to what §13 shipped; what changed is that a lawful catalog
    can now hand it a routing rule."""
    entry = ModelCatalogEntry(
        model_id="auto", label="Automatic (routes by role)",
        provider_class="routing-rule", available=True,
        input_limit_bytes=2048, output_limit_bytes=8192,
        data_handling="Routes by role. / Processed in the approved tenant "
                      "boundary",
        routing_rule=True, routes_to=("model-a",), resolved_model_id="model-a")
    assert serve_mod.doxbench_selected_model(entry) == {
        "requested_model_id": "auto",
        "routing_rule": True,
        "data_handling": "Routes by role. / Processed in the approved tenant "
                         "boundary",
        "resolved_model_id": "model-a",
    }


# ---------------------------------------------------------------------------
# CODEX-2 (Codex review of PR #210): BUFFER ORDER IS NOT PART OF A TURN'S
# IDENTITY on the widened lane
# ---------------------------------------------------------------------------

def test_a_widened_turn_replays_when_its_buffers_arrive_reordered(tmp_path):
    """The released contract: "a repeated completed id with identical input
    hashes SHALL return the recorded result without another provider dispatch".

    A reordered buffer array carries identical hashes, but
    `json.dumps(sort_keys=True)` orders KEYS and never array members — so the
    retransmission digested differently and came back `turn_id_conflict`.
    Reproduced before the fix: second send 409. The canonical form now orders the
    buffers by BUFFER KEY."""
    buffers = [
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("document", DOC_ALPHA, "# Alpha\n\n" + _S_DOCUMENT),
        _buf("document", DOC_ZULU, "# Zulu\n\nsecond loaded document"),
    ]
    body = _turn_v2(client_turn_id="turn-v2-reorder", bound_buffer=DOC_ALPHA,
                    buffers=buffers)
    reordered = dict(body, buffers=[buffers[0], buffers[2], buffers[1]])
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                  snapshot=_snapshot_with_editable(DOC_ALPHA, DOC_ZULU)
                  ) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        first_status, first_payload, _h, _r = _request(
            host, prt, "POST", CHAT_ROUTE, body=body, headers=_console_headers(caps))
        second_status, second_payload, _h2, _r2 = _request(
            host, prt, "POST", CHAT_ROUTE, body=reordered,
            headers=_console_headers(caps))
    assert first_status == 200, first_payload
    assert second_status == 200, second_payload
    # BYTE-IDENTICAL replay, and exactly one provider dispatch for the two sends.
    assert second_payload == first_payload
    assert fake.calls.count("dispatch") == 1


def test_a_widened_turn_with_changed_content_still_conflicts(tmp_path):
    """The other side of the same rule, so the fix cannot have loosened
    idempotency into indifference: a repeat of the same id with DIFFERENT content
    is still the conflict it always was."""
    body = _turn_v2(client_turn_id="turn-v2-conflict", bound_buffer=DOC_ALPHA,
                    buffers=[
                        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
                        _buf("document", DOC_ALPHA, "# Alpha\n\n" + _S_DOCUMENT),
                    ])
    changed = dict(body, buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("document", DOC_ALPHA, "# Alpha\n\nEDITED SINCE"),
    ])
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake),
                  snapshot=_snapshot_with_editable(DOC_ALPHA, DOC_ZULU)
                  ) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        first_status, _p, _h, _r = _request(
            host, prt, "POST", CHAT_ROUTE, body=body, headers=_console_headers(caps))
        second_status, second_payload, _h2, _r2 = _request(
            host, prt, "POST", CHAT_ROUTE, body=changed,
            headers=_console_headers(caps))
    assert first_status == 200
    _assert_v2_refusal(second_status, second_payload, "turn_id_conflict")
    assert fake.calls.count("dispatch") == 1


def test_the_v1_canonical_form_is_untouched_by_the_reorder_fix(tmp_path):
    """The v1 lane keeps its recorded digests: its canonical form still carries
    the buffers in WIRE order, because changing it would make every turn already
    in a live store unreplayable.

    STATED HONESTLY (land-time note N6): that is a TRADE, not an impossibility.
    The closed v1 envelope fixes the buffer COUNT and their KINDS, NOT their
    array order — so a v1 client that retransmits the same turn with its two
    buffers swapped still gets the 409 this fix closes on the widened lane. The
    wart is knowingly retained, because a live break (every recorded digest) is
    worse than a latent one, and it dies with the lane at contract-v2.0."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard"
              / "serve.py").read_text(encoding="utf-8")
    assert "canonical_buffer_order = turn_buffers" in source
    assert 'if request_kind == DOXBENCH_CHAT_TURN_V2_KIND:\n' \
           '            canonical_buffer_order = sorted(' in source


# ===========================================================================
# AMENDMENT 2 FOLLOW-UP 1 — the buffers floor names its own cause.
#
# BRETT'S SCENARIO (2026-08-21, browser annotation round): unload the loaded set
# down to the outline and press Send. Amendment 2 RULED that this act stays
# reachable and refuses at send rather than being made unreachable, and the
# refusal was correct in class -- the released `buffers.minItems: 2` really is
# violated -- but its sentence was the catch-all "the turn request is malformed",
# which names nothing a human can act on. The actionable half sat in the
# selector's empty state a few pixels away.
#
# WHAT CHANGED, AND WHAT DID NOT. Only the `message` string, and only for this
# one violation. Same code, same 400, same envelope, same key set, and the
# released schemas are byte-untouched -- the failure envelope's `message` is
# free-form (`minLength: 1, maxLength: 500`), so no digest and no contract
# release is involved. The tests below pin both halves: that the sentence
# arrives where the cause is real, and that it CANNOT arrive anywhere else.
# ===========================================================================

_ONLY_OUTLINE = [_buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE)]


def test_a_v2_turn_unloaded_to_the_outline_alone_names_the_missing_document(
        tmp_path):
    """THE SCENARIO, driven end to end against the real route.

    The turn is well-formed in every other respect and bound to the outline, so
    nothing but the buffer set can be what the route objects to."""
    body = _turn_v2(bound_buffer="outline", buffers=list(_ONLY_OUTLINE))
    status, payload, fake = _post_turn(tmp_path, body)
    _assert_v2_refusal(status, payload, "invalid_turn_request",
                       serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT)
    # The schema gate is before scope, before identity, and before the model.
    assert fake.calls == []
    _assert_no_sentinels(payload)


def test_the_no_document_sentence_names_both_the_cause_and_the_remedy(tmp_path):
    """WHY the change was worth making at all. A refusal that names only a class
    leaves the human to guess; this one has to say what is missing AND what to do
    about it, in the surface's own vocabulary.

    The remedy is asserted against the selector's ratified empty-state note
    rather than a literal, so the two surfaces cannot drift into naming
    different remedies for one state."""
    empty_note = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
                  / "views" / "doxbench-chat.js").read_text(encoding="utf-8")
    assert "use a docs tile's load verb to work on one" in empty_note, (
        "precondition: the selector's ratified empty state still names the "
        "load verb as the remedy")
    sentence = serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT
    assert "no document" in sentence
    assert "use a docs tile's load verb to work on one" in sentence, (
        "the route must name the SAME remedy the selector names")
    assert 1 <= len(sentence) <= 500, "the released `message` bound"
    # Fixed, and composed from nothing the caller sent: the chooser returns THIS
    # object, so no formatting or interpolation can have happened on the way.
    assert serve_mod.DashboardHandler._doxbench_invalid_turn_message(
        {}, doxbench_contracts.KIND_CHAT_TURN_V2,
        {"buffers": [{"kind": "outline"}]}) is None, (
        "no validator means no verdict, and no verdict must not be specific")


def test_a_v2_turn_carrying_no_buffers_at_all_keeps_the_generic_message(
        tmp_path):
    """The floor is short here too, but the outline is missing as well -- so a
    sentence about there being 'no document beside the outline' would describe a
    set this request does not have. The catch-all is true of it; the specific one
    would not be."""
    body = _turn_v2(bound_buffer="outline", buffers=[])
    status, payload, fake = _post_turn(tmp_path, body)
    _assert_v2_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_a_v2_turn_carrying_only_a_document_keeps_the_generic_message(tmp_path):
    """The other way to be one buffer short: a document and NO outline. The
    outline is the permanently reserved buffer every turn carries, so this is a
    malformed request of a different kind, and it is not told that its document
    is missing."""
    body = _turn_v2(bound_buffer="document", buffers=[
        _buf("document", None, "# Document\n\n" + _S_DOCUMENT)])
    status, payload, fake = _post_turn(tmp_path, body)
    _assert_v2_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_the_released_floor_itself_names_the_cause(tmp_path):
    """The scenario against the RELEASE rather than the fixture: here it really is
    `buffers.minItems: 2` that refuses the turn, at the schema gate, before the
    delegated validator is reached at all. Same sentence from that gate as from
    the pairing rule, which is the point -- the cause is a fact about the
    request, not about which statement of the floor noticed it."""
    released = _require_released_validators()
    body = _turn_v2(bound_buffer="outline", buffers=list(_ONLY_OUTLINE))
    status, payload, fake = _post_turn(
        tmp_path, body, schema_validator_factory=lambda: dict(released))
    _assert_v2_refusal(status, payload, "invalid_turn_request",
                       serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT)
    assert fake.calls == []


def test_a_second_violation_beside_the_buffers_floor_keeps_the_generic_message(
        tmp_path):
    """THE HONESTY CONSTRAINT, and the reason the chooser demands that nothing
    else be wrong.

    This turn is outline-only AND carries a blank message. Loading a document
    would not make it sendable, so telling the human that loading one is the
    remedy would send them round a loop. The catch-all is the honest answer while
    more than one thing is wrong.

    Bound to the RELEASED validators deliberately: the guard is a statement about
    what the release faults, and the fixture -- which declares `"message": {}` as
    well as `"buffers": {}` -- cannot see the second violation to be guarded
    against, so under it this test would pass while proving nothing."""
    released = _require_released_validators()
    body = _turn_v2(bound_buffer="outline", buffers=list(_ONLY_OUTLINE),
                    message="")
    status, payload, fake = _post_turn(
        tmp_path, body, schema_validator_factory=lambda: dict(released))
    _assert_v2_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []


def test_the_remedy_the_no_document_refusal_names_actually_makes_it_sendable(
        tmp_path):
    """The claim measured rather than asserted: doing what the sentence says is
    ENOUGH. The same turn, refused with the cause named, is served once a
    document rides beside the outline -- which is what makes the remedy a remedy
    and not a guess."""
    refused_body = _turn_v2(bound_buffer="outline", buffers=list(_ONLY_OUTLINE))
    status, payload, _fake = _post_turn(tmp_path, refused_body)
    _assert_v2_refusal(status, payload, "invalid_turn_request",
                       serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT)

    loaded_body = _turn_v2(bound_buffer="outline", buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("document", None, "# Document\n\n" + _S_DOCUMENT)])
    ok_status, ok_payload, fake = _post_turn(tmp_path, loaded_body)
    assert ok_status == 200, ok_payload
    assert ok_payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS
    assert fake.calls.count("dispatch") == 1


def test_the_no_document_refusal_leaves_the_turn_slot_reusable(tmp_path):
    """A refusal must not strand the conversation's lease: the human's next act
    after reading the sentence is to load a document and send AGAIN, and that
    second turn has to be accepted rather than met with `turn_in_flight`."""
    refused = _turn_v2(bound_buffer="outline", buffers=list(_ONLY_OUTLINE),
                       client_turn_id="turn-v2-reuse")
    retried = _turn_v2(client_turn_id="turn-v2-reuse")
    fake = _port()
    with _serving(tmp_path, model_port_factory=(lambda: fake)) as (httpd, host, prt):
        caps = _capabilities(host, prt)
        first_status, first_payload, _h1, _r1 = _request(
            host, prt, "POST", CHAT_ROUTE, body=refused,
            headers=_console_headers(caps))
        second_status, second_payload, _h2, _r2 = _request(
            host, prt, "POST", CHAT_ROUTE, body=retried,
            headers=_console_headers(caps))
    _assert_v2_refusal(first_status, first_payload, "invalid_turn_request",
                       serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT)
    assert second_status == 200, second_payload
    assert second_payload["kind"] == doxbench_contracts.KIND_CHAT_TURN_V2_SUCCESS


def test_the_cause_naming_message_is_not_a_catalog_entry(tmp_path):
    """The catalog stays ONE fixed message per code, and `invalid_turn_request`'s
    entry is still the catch-all. The cause-naming sentence is an override the
    schema gate passes for one detected violation -- so every OTHER emitter of
    this code (the delegated validator, the later precondition legs) is
    untouched by construction, not by discipline."""
    catalog = serve_mod.DOXBENCH_ERROR_CATALOG
    assert (catalog[serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST][1]
            is serve_mod._DOXBENCH_MSG_INVALID_TURN_REQUEST)
    assert (serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT
            not in [message for _status, message in catalog.values()])
    # The pure body builder still defaults to the catalog, so nothing that does
    # not deliberately pass the override can emit the specific sentence.
    body = serve_mod.doxbench_turn_failure_body(
        serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST, "turn-1",
        kind=doxbench_contracts.KIND_CHAT_TURN_V2_FAILURE)
    assert body["message"] == serve_mod._DOXBENCH_MSG_INVALID_TURN_REQUEST


class _LeakyMessage:
    """A plausible future mistake: an object a caller passes as the override
    whose `__str__` carries the human's own prose.

    Deliberately shaped like the things that actually get passed by accident --
    an exception, a validation error, a response wrapper -- rather than a
    contrived sentinel, because those are what stringify to request content."""

    def __init__(self, leaked):
        self.leaked = leaked

    def __str__(self):
        return f"invalid buffer content: {self.leaked}"


@pytest.mark.parametrize("override", [
    _LeakyMessage("the human's unsent question"),
    b"the human's unsent question",
    ["the human's unsent question"],
    123,
    "",
], ids=["object", "bytes", "list", "int", "empty"])
def test_a_message_override_that_is_not_a_real_string_falls_back_to_the_catalog(
        override):
    """Copilot review (PR #255): the override is typed by CONTRACT, and now also
    by construction.

    The old `str(message)` would have coerced any of these, and the first case
    shows why that matters -- its `__str__` carries the caller's own text
    straight into a published refusal, which is exactly what the envelope's
    redaction posture exists to prevent. The fallback is the catalog string, and
    the leaked prose appears NOWHERE in the serialized body.

    The empty string is here for a different reason: not disclosure, but the
    released `minLength: 1`, which an empty override would violate."""
    body = serve_mod.doxbench_turn_failure_body(
        serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST, "turn-1",
        kind=doxbench_contracts.KIND_CHAT_TURN_V2_FAILURE, message=override)
    assert body["message"] == serve_mod._DOXBENCH_MSG_INVALID_TURN_REQUEST
    assert "the human's unsent question" not in json.dumps(body), (
        "a refusal must disclose nothing the caller sent")
    # Still a conformant envelope: the hardening must not cost the correlation
    # id, which is what a raise or a `minLength` violation would have done.
    assert set(body) == {"schema_version", "kind", "client_turn_id",
                         "error", "message"}
    assert body["client_turn_id"] == "turn-1"


def test_a_real_string_override_is_still_honoured_unchanged():
    """The negative half: the hardening rejects TYPES, not the feature. A genuine
    fixed constant still overrides, or the change above would have quietly
    reverted this branch's whole point."""
    body = serve_mod.doxbench_turn_failure_body(
        serve_mod.DOXBENCH_ERR_INVALID_TURN_REQUEST, "turn-1",
        kind=doxbench_contracts.KIND_CHAT_TURN_V2_FAILURE,
        message=serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT)
    assert body["message"] == serve_mod._DOXBENCH_MSG_TURN_HAS_NO_DOCUMENT


def test_the_delegated_validators_own_refusals_keep_the_generic_message(
        tmp_path):
    """The floor has TWO statements: the schema's `minItems: 2` and the server's
    own outline-plus-document pairing rule. Only the schema one can be the sole
    violation of the released envelope, so a turn that satisfies the count and
    fails the PAIRING (two outlines) is refused by the delegated validator, after
    the schema gate has already passed it -- and it gets the catch-all, because
    the cause-naming branch never ran."""
    body = _turn_v2(bound_buffer="outline", buffers=[
        _buf("outline", OUTLINE_PATH, "# Outline\n\n" + _S_OUTLINE),
        _buf("outline", OUTLINE_PATH, "# Outline again\n\n" + _S_OUTLINE)])
    status, payload, fake = _post_turn(tmp_path, body)
    _assert_v2_refusal(status, payload, "invalid_turn_request")
    assert fake.calls == []
