import copy
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("private_connectivity", ROOT / "scripts/validate-private-connectivity.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)
NOW = datetime(2026, 11, 10, tzinfo=timezone.utc)
REF = "git:" + "a" * 40 + ":synthetic/evidence.json"


def ready():
    context = {"installation_id": "factory-a", "customer_id": "tenant-a", "environment": "test"}
    access = {"sources": ["workload-a"], "destinations": ["private-a"], "ports": [443], "protocol": "tcp"}
    approval = {
        **context, "network_ref": "network-a", "endpoint": "https://control.synthetic.invalid", "status": "active",
        "expires_at": "2026-11-11T00:00:00Z", "scope": copy.deepcopy(access), "ref": REF,
    }
    binding = {
        "schema_version": 1, "kind": "xfactory_connectivity_binding",
        **context, "operator_mode": "managed", "endpoint": "https://control.synthetic.invalid",
        "network_ref": "network-a", "state": "ready", "access": access, "routes": [],
        "approval": approval,
        "enrollment": {"network_ref": "network-a", "authorized": True, "credential_ref": "vault://synthetic/enrollment", "ref": REF},
        "policy": {"network_ref": "network-a", "revision": REF, "verified": True, "scope": copy.deepcopy(access), "ref": REF},
        "verification": {"allowed": True, "denied": True, "policy_revision": REF, "ref": REF},
    }
    return {"installation": context, "private_connectivity": binding}


def test_unbound_and_customer_operated_compatibility():
    assert VALIDATOR.validate({"old_runtime_field": {"old": True}}, NOW) == []
    assert VALIDATOR.validate({"private_connectivity": None}, NOW) == []
    manifest = ready()
    manifest["private_connectivity"]["operator_mode"] = "customer_operated"
    assert VALIDATOR.validate(manifest, NOW) == []


def test_ready_declaration_and_reordered_scope():
    manifest = ready()
    for access in (manifest["private_connectivity"]["access"],
                   manifest["private_connectivity"]["approval"]["scope"],
                   manifest["private_connectivity"]["policy"]["scope"]):
        access["ports"] = [443, 8443]
    manifest["private_connectivity"]["policy"]["scope"]["ports"].reverse()
    assert VALIDATOR.validate(manifest, NOW) == []


def test_mismatched_binding_scope():
    for field in ("customer_id", "environment", "installation_id"):
        manifest = ready()
        manifest["installation"][field] = "other"
        assert VALIDATOR.validate(manifest, NOW) == ["binding-context-mismatch"]


def test_approval_identity_authority_and_expiry():
    for field, value in (("network_ref", "other"), ("customer_id", "other"),
                         ("environment", "prod"), ("status", "revoked"),
                         ("status", "expired"), ("expires_at", "2026-11-09T00:00:00Z")):
        manifest = ready()
        manifest["private_connectivity"]["approval"][field] = value
        assert VALIDATOR.validate(manifest, NOW) == ["approval-unavailable"]


def test_access_cannot_exceed_approval_or_policy():
    for source in ("approval", "policy"):
        manifest = ready()
        manifest["private_connectivity"][source]["scope"]["ports"] = [22]
        assert VALIDATOR.validate(manifest, NOW)


def test_separate_route_approval():
    manifest = ready()
    binding = manifest["private_connectivity"]
    binding["routes"] = ["192.0.2.0/24"]
    assert VALIDATOR.validate(manifest, NOW) == ["route-approval-unavailable"]
    binding["route_approval"] = {**copy.deepcopy(binding["approval"]), "routes": list(binding["routes"])}
    assert VALIDATOR.validate(manifest, NOW) == []
    binding["route_approval"]["routes"] = ["198.51.100.0/24"]
    assert VALIDATOR.validate(manifest, NOW) == ["route-approval-unavailable"]


def test_ready_requires_enrollment_and_effective_policy():
    for field in ("enrollment", "policy", "verification"):
        manifest = ready()
        del manifest["private_connectivity"][field]
        assert VALIDATOR.validate(manifest, NOW)
    manifest = ready()
    manifest["private_connectivity"]["verification"]["denied"] = False
    assert VALIDATOR.validate(manifest, NOW) == ["binding-shape-invalid"]


def test_enrollment_and_policy_must_match_current_network():
    for field in ("enrollment", "policy"):
        manifest = ready()
        manifest["private_connectivity"][field]["network_ref"] = "other"
        assert VALIDATOR.validate(manifest, NOW)


def test_nonready_states_remain_representable():
    for state in ("requested", "unready", "revoked"):
        manifest = ready()
        manifest["private_connectivity"]["state"] = state
        for field in ("approval", "enrollment", "policy", "verification"):
            del manifest["private_connectivity"][field]
        assert VALIDATOR.validate(manifest, NOW) == []


def test_raw_credential_or_unknown_field_is_rejected():
    for field, value in (("password", "fixture-value"), ("operator_mode", "unrecognized")):
        manifest = ready()
        manifest["private_connectivity"][field] = value
        assert VALIDATOR.validate(manifest, NOW) == ["binding-shape-invalid"]
    manifest = ready()
    manifest["private_connectivity"]["enrollment"]["credential_ref"] = "fixture-raw-token"
    assert VALIDATOR.validate(manifest, NOW) == ["binding-shape-invalid"]


def test_invalid_endpoint():
    for endpoint in ("http://host.invalid", "https://user:pass@host.invalid", "https://host.invalid?token=value",
                     "https://host.invalid:bad", "https://host.invalid/a", "https://host.invalid\n"):
        manifest = ready()
        manifest["private_connectivity"]["endpoint"] = endpoint
        assert VALIDATOR.validate(manifest, NOW) == ["endpoint-invalid"]


def test_cli_failure_redacts_input(tmp_path, capsys):
    path = tmp_path / "input.json"
    manifest = ready()
    manifest["private_connectivity"]["password"] = "sensitive-fixture-value"
    path.write_text(json.dumps(manifest))
    assert VALIDATOR.main([str(path), "--now", "2026-11-10T00:00:00Z"]) == 1
    assert "sensitive-fixture-value" not in capsys.readouterr().err
    path.write_text('{"private_connectivity":null,"private_connectivity":null}')
    assert VALIDATOR.main([str(path)]) == 2


def test_other_valid_https_endpoint_cannot_reuse_existing_approval():
    for state in ("approved", "enrolled", "ready"):
        manifest = ready()
        manifest["private_connectivity"]["state"] = state
        manifest["private_connectivity"]["endpoint"] = "https://other-control.synthetic.invalid"
        assert VALIDATOR.validate(manifest, NOW) == ["approval-unavailable"]
