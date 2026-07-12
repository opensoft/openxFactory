"""FR-018 / SC-010: interface-impact always emitted; variances cite concrete ACR IDs."""
import pytest
from jsonschema.exceptions import ValidationError

from avatar_f0.evidence import build_interface_impact, validate_interface_impact


def test_empty_variances_on_clean_pass_is_valid():
    doc = build_interface_impact("map.yaml", "deadbeef", "a" * 64, [])
    validate_interface_impact(doc)
    assert doc["variances"] == []
    assert doc["kind"] == "avatar-f0-interface-impact"
    assert doc["acceptance_map"]["content_sha256"] == "a" * 64


def test_variance_with_concrete_acr_ids_validates():
    var = {
        "id": "VAR-001",
        "affected_acr_ids": ["ACR-003", "ACR-011"],
        "observed_behavior": "provider released answer before sideband verified",
        "evidence_refs": ["F0-A-01", "F0-A-ORDERING"],
        "severity": "high",
        "proposed_correction": "hold answer until sideband verified",
        "continuation": "blocked_pending_disposition",
    }
    doc = build_interface_impact("map.yaml", "c", "a" * 64, [var])
    validate_interface_impact(doc)


def test_placeholder_acr_id_is_rejected_by_schema():
    var = {
        "id": "VAR-001", "affected_acr_ids": ["ACR-TBD-01"],
        "observed_behavior": "x", "evidence_refs": ["F0-A-01"],
        "severity": "low", "proposed_correction": "y",
        "continuation": "continue_behind_closed_default",
    }
    with pytest.raises(ValidationError):
        validate_interface_impact(build_interface_impact("m", "c", "a" * 64, [var]))


def test_variance_requires_at_least_one_acr_id():
    var = {
        "id": "VAR-001", "affected_acr_ids": [],
        "observed_behavior": "x", "evidence_refs": ["F0-A-01"],
        "severity": "low", "proposed_correction": "y",
        "continuation": "continue_behind_closed_default",
    }
    with pytest.raises(ValidationError):
        validate_interface_impact(build_interface_impact("m", "c", "a" * 64, [var]))
