"""Security and contract tests for the one server-side provider boundary."""

from __future__ import annotations

import json
import http.client
from pathlib import Path
import sys
import threading
import uuid

import pytest

from ideation_dashboard import doxbench_model
from ideation_dashboard import doxbench_provider as provider
from ideation_dashboard import serve


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = REPO_ROOT / "scripts" / "ideation_dashboard"
WEB_ROOT = SCRIPTS_ROOT / "web"
BASE_REPO = REPO_ROOT / "tests" / "ideation-dashboard" / "fixtures" / "base-repo"


def _binding(**overrides):
    values = {
        "id": "local-provider",
        "label": "Local provider",
        "credential_ref": "ref-123",
        "auth_kind": "api_key",
        "broker_invocation": ("declared-broker", "mint"),
    }
    values.update(overrides)
    return provider.ModelProviderBinding(**values)


def _catalog():
    return doxbench_model.ModelCatalog.from_entries([
        doxbench_model.ModelCatalogEntry(
            model_id="model-a", label="Model A", provider_class="on-tenant",
            available=True, input_limit_bytes=100_000,
            output_limit_bytes=100_000, data_handling="on-tenant",
        )
    ])


def test_binding_shape_is_closed_and_has_no_secret_field():
    binding = _binding()
    assert tuple(binding.as_public_dict()) == provider.MODEL_PROVIDER_BINDING_FIELDS
    assert set(binding.as_public_dict()) == {
        "id", "label", "credential_ref", "auth_kind", "broker_invocation",
    }
    with pytest.raises(TypeError):
        provider.ModelProviderBinding(**{
            **binding.as_public_dict(), "secret": "must-not-fit"
        })


def test_credential_is_sent_on_stdin_and_only_reference_is_persisted(tmp_path):
    secret = "credential-sentinel-" + uuid.uuid4().hex
    seen = []

    def runner(argv, stdin, timeout):
        seen.append((argv, stdin, timeout))
        request = json.loads(stdin.decode("utf-8"))
        assert request["operation"] == "store_credential"
        assert request["credential"] == secret
        return b'{"credential_ref":"broker-ref-1"}'

    broker = provider.BrokerClient(runner=runner)
    ref = broker.store_credential(
        binding_id="local-provider", label="Local provider", auth_kind="api_key",
        broker_invocation=("declared-broker",), credential=secret)
    store = provider.ModelProviderBindingStore(tmp_path / "bindings.json")
    store.put(_binding(credential_ref=ref))

    persisted = (tmp_path / "bindings.json").read_text(encoding="utf-8")
    assert secret not in persisted
    assert ref in persisted
    response = json.dumps({"ok": True, "bindings": store.public_list()})
    assert secret not in response
    # The value is generated at runtime, so this can safely sweep the checkout
    # rather than accidentally finding the test's own source literal.
    for path in REPO_ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        assert secret.encode("utf-8") not in path.read_bytes(), str(path)
    assert seen[0][0] == ("declared-broker",)


def test_binding_store_round_trips_only_safe_records(tmp_path):
    path = tmp_path / "bindings.json"
    store = provider.ModelProviderBindingStore(path)
    store.put(_binding())
    loaded = provider.ModelProviderBindingStore(path)
    assert loaded.public_list() == store.public_list()
    assert "secret" not in path.read_text(encoding="utf-8").lower()


class _Broker:
    def __init__(self):
        self.mints = 0

    def mint(self, binding):
        self.mints += 1
        return provider.MintedCapability(
            token=f"memory-token-{self.mints}", expires_at=4_000_000_000,
            catalog_endpoint="http://127.0.0.1/catalog",
            completion_endpoint="http://127.0.0.1/complete",
            timeout_seconds=10,
        )


class _Provider:
    def catalog(self, capability):
        return _catalog()

    def dispatch(self, capability, prompt):
        return {"assistant_prose": "answer", "proposals": []}


def test_expired_capability_is_discarded_without_retry_then_next_call_mints():
    broker = _Broker()
    port = provider.BrokerBackedWorkbenchModelPort(
        _binding(), broker=broker, provider=_Provider())
    assert port.catalog() == _catalog()
    assert broker.mints == 1
    port._capability.expires_at = 0
    with pytest.raises(provider.ProviderTokenExpired):
        port.dispatch("opaque prompt")
    assert broker.mints == 1
    assert port.dispatch("opaque prompt") == {
        "assistant_prose": "answer", "proposals": []
    }
    assert broker.mints == 2


def test_broker_failure_has_no_provider_detail_in_the_exception():
    def runner(argv, stdin, timeout):
        raise RuntimeError("contains raw credential and provider endpoint")

    with pytest.raises(provider.BrokerError) as error:
        provider.BrokerClient(runner=runner).mint(_binding())
    assert str(error.value) == "broker invocation failed"


def test_provider_transport_markers_are_confined_to_the_named_module():
    """The provider boundary narrows to one module; it is not deleted."""
    allowed = SCRIPTS_ROOT / "doxbench_provider.py"
    markers = ("MintedCapability", "catalog_endpoint", "completion_endpoint")
    inspected = [
        path for path in SCRIPTS_ROOT.glob("*.py") if path != allowed
    ]
    inspected += list((SCRIPTS_ROOT / "web").rglob("*.js"))
    for path in inspected:
        source = path.read_text(encoding="utf-8")
        assert not any(marker in source for marker in markers), str(path)


def test_provider_port_outputs_never_include_its_minted_token():
    broker = _Broker()
    port = provider.BrokerBackedWorkbenchModelPort(
        _binding(), broker=broker, provider=_Provider())
    catalog = port.catalog()
    answer = port.dispatch({"prompt": "opaque"})
    wire = json.dumps({"catalog": catalog.as_public_dict(), "answer": answer})
    assert "memory-token-1" not in wire
    assert "memory-token-1" not in json.dumps(port.binding.as_public_dict())
    assert "memory-token-1" not in repr(port._capability)


def test_settings_route_hands_off_secret_and_supports_list_edit_remove(tmp_path):
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(json.dumps({
        "repository": "fixture-repo", "ref": "main",
        "generation": {"source_revision": "pin"},
        "documents": [], "clusters": [],
    }), encoding="utf-8")
    store = provider.ModelProviderBindingStore()
    httpd = serve.build_server(
        WEB_ROOT, snapshot, BASE_REPO, head="pin", actor="brett",
        model_provider_store=store,
    )
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    host, port = httpd.server_address[:2]

    def request(method, path, body=None, headers=None):
        connection = http.client.HTTPConnection(host, port, timeout=5)
        connection.request(
            method, path,
            body=None if body is None else json.dumps(body),
            headers=headers or {},
        )
        response = connection.getresponse()
        raw = response.read()
        connection.close()
        return response.status, json.loads(raw.decode("utf-8")), raw

    try:
        status, capabilities, _ = request("GET", "/capabilities")
        assert status == 200
        headers = {
            "Content-Type": "application/json",
            "X-XF-Console-Token": capabilities["console_token"],
        }
        secret = "route-secret-" + uuid.uuid4().hex
        broker_script = (
            "import json,sys; request=json.load(sys.stdin); "
            "print(json.dumps({'credential_ref':'route-ref'}))"
        )
        binding_request = {
            "operation": "upsert", "id": "route-provider", "label": "Route",
            "auth_kind": "api_key", "broker_invocation": [
                sys.executable, "-c", broker_script,
            ], "credential": secret,
        }
        status, payload, raw = request(
            "POST", "/settings/model-providers", binding_request, headers)
        assert status == 200
        assert secret.encode("utf-8") not in raw
        assert payload["bindings"][0]["credential_ref"] == "route-ref"
        assert secret not in json.dumps(store.public_list())

        status, payload, _ = request(
            "POST", "/settings/model-providers", {
                "operation": "upsert", "id": "route-provider",
                "label": "Edited", "credential_ref": "route-ref",
                "auth_kind": "api_key", "broker_invocation": ["declared"],
            }, headers)
        assert status == 200
        assert payload["bindings"][0]["label"] == "Edited"

        status, payload, _ = request(
            "POST", "/settings/model-providers",
            {"operation": "remove", "id": "route-provider"}, headers)
        assert status == 200
        assert payload["bindings"] == []
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=2)
