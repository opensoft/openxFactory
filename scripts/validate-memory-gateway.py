#!/usr/bin/env python3
"""Validate xFactory Memory Gateway contracts, examples, fixtures, and smoke paths."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "contracts" / "memory-gateway"
EXAMPLE_DIR = ROOT / "examples" / "memory-gateway"

REQUIRED_CONTRACTS = {
    "README.md",
    "vocabularies.yaml",
    "consent-profile.schema.yaml",
    "gateway-request.schema.yaml",
    "gateway-response.schema.yaml",
    "provider-profile.schema.yaml",
    "provider-binding.schema.yaml",
    "provider-mapping.schema.yaml",
    "subject-safety-profile.schema.yaml",
    "context-packet.schema.yaml",
    "expert-context-packet.schema.yaml",
    "expert-knowledge-source.schema.yaml",
    "promotion-candidate.schema.yaml",
    "migration-manifest.schema.yaml",
    "usage-event.schema.yaml",
    "revocation.schema.yaml",
    "erasure.schema.yaml",
    "break-glass-profile.schema.yaml",
    "audit-event.schema.yaml",
    "memory-binding.schema.yaml",
}

REQUIRED_EXAMPLES = {
    "semantic-context-packet.example.yaml",
    "gbrain-provider-profile.yaml",
    "honcho-provider-profile.yaml",
    "agentmemory-provider-profile.yaml",
    "local-postgres-provider-profile.yaml",
    "expert-provider-profiles.yaml",
    "provider-mappings.example.yaml",
    "provider-bindings.example.yaml",
    "subject-safety.example.yaml",
    "hermes-memory-gateway-config.example.yaml",
    "xfactory-memory-tool-surface.example.yaml",
    "conformance-fixtures.yaml",
    "hermes-gbrain-context-packet-smoke.example.yaml",
    "provider-route-swap-smoke.example.yaml",
    "omnigent-expert-context-smoke.example.yaml",
    "domain-stack-memory-gateway.example.yaml",
    "medx-patient-context-packet.example.yaml",
    "opsx-managed-system-context-packet.example.yaml",
    "customer-memory-migration-manifest.example.yaml",
    "medx-omnigent-diagnostic-reviewer-context.example.yaml",
    "opsx-runbook-expert-context.example.yaml",
    "medx-break-glass.example.yaml",
    "memory-binding.example.yaml",
}

REQUIRED_FIXTURE_IDS = {
    "semantic_context_digest_mismatch_rejected",
    "semantic_context_unpinned_package_rejected",
    "semantic_context_retired_package_rejected",
    "semantic_context_cross_purpose_rejected",
    "semantic_context_tenant_binding_mismatch_rejected",
    "semantic_context_unrestricted_corpus_refused",
    "semantic_context_provider_replacement_stable",
    "semantic_inference_cannot_authorize",
    "read_denied_missing_consent",
    "read_denied_withdrawn_consent",
    "write_denied_missing_source_refs",
    "write_denied_secret_like_content",
    "promotion_denied_without_deidentification",
    "promotion_denied_without_required_review",
    "context_packet_created_with_trace",
    "provider_binding_denies_layer",
    "minor_denied_missing_guardian_authority",
    "minor_degrades_prohibited_personalization",
    "usage_event_emitted_for_context_packet",
    "budget_hard_limit_denies_expensive_operation",
    "migration_dual_write_routes_source_and_target",
    "provider_profile_missing_required_companion",
    "expert_context_packet_created",
    "expert_knowledge_denied_uncited",
    "expert_db_migration_shadow_read",
    "threat_overbroad_packet_request_denied",
    "threat_purpose_gaming_break_glass_denied",
    "threat_confused_deputy_denied",
    "threat_worker_bypass_denied_by_credential_absence",
    "threat_memory_laundering_denied",
    "threat_cross_tenant_namespace_residue_denied",
    "caller_identity_denied_unattributable",
    "diagnostic_credential_scope_read_only_non_production",
    "fail_mode_write_fail_closed_gateway_outage",
    "break_glass_minimal_packet",
    "packet_leash_ttl_expiry_reruns_rails",
    "packet_leash_cross_purpose_rejected",
    "erasure_provider_side_delete_with_confirmations",
    "erasure_denies_unsupported_policy_constrained_subject",
    "revocation_does_not_claim_erasure",
    "consent_rail_records_profile_version",
    "consent_change_is_audited",
    "consent_backing_store_swap_does_not_change_contract",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def require_files(root: Path, names: set[str], errors: list[str]) -> None:
    for name in sorted(names):
        path = root / name
        if not path.is_file():
            errors.append(f"{rel(path)} missing")


def validate_contracts(errors: list[str]) -> None:
    require_files(CONTRACT_DIR, REQUIRED_CONTRACTS, errors)
    vocab = load_yaml(CONTRACT_DIR / "vocabularies.yaml")
    vocabs = vocab.get("vocabularies", {})
    for key in [
        "gateway_operations",
        "canonical_ports",
        "provider_roles",
        "expert_provider_roles",
        "provider_support_levels",
        "binding_custody_modes",
        "subject_categories",
        "age_bands",
        "guardian_authority_modes",
        "rail_denial_reasons",
        "privacy_classes",
        "authority_levels",
        "billing_modes",
        "migration_modes",
        "knowledge_scopes",
        "promotion_statuses",
        "conformance_tiers",
        "fail_modes",
        "erasure_capability_levels",
        "redaction_classes",
    ]:
        if not isinstance(vocabs.get(key), list) or not vocabs[key]:
            errors.append(f"{rel(CONTRACT_DIR / 'vocabularies.yaml')} missing vocabulary {key}")
    for schema in sorted(CONTRACT_DIR.glob("*.schema.yaml")):
        data = load_yaml(schema)
        if data.get("schema_version") != 1:
            errors.append(f"{rel(schema)} schema_version must be 1")
        if not data.get("name") or data.get("type") != "object":
            errors.append(f"{rel(schema)} needs name and type: object")
        if not isinstance(data.get("required"), list) or not data["required"]:
            errors.append(f"{rel(schema)} required must be a non-empty list")


def validate_provider_profiles(errors: list[str]) -> None:
    for filename in [
        "gbrain-provider-profile.yaml",
        "honcho-provider-profile.yaml",
        "agentmemory-provider-profile.yaml",
        "local-postgres-provider-profile.yaml",
    ]:
        path = EXAMPLE_DIR / filename
        profile = load_yaml(path).get("provider_profile", {})
        for key in ["id", "provider_role", "adapter", "allowed_layers", "ports", "erasure"]:
            if not profile.get(key):
                errors.append(f"{rel(path)} provider_profile missing {key}")
        if "raw_credentials" not in profile.get("prohibited_content", []):
            if filename != "agentmemory-provider-profile.yaml":
                errors.append(f"{rel(path)} must prohibit raw_credentials")

    expert = load_yaml(EXAMPLE_DIR / "expert-provider-profiles.yaml")
    profiles = expert.get("provider_profiles", [])
    if len(profiles) < 6:
        errors.append(f"{rel(EXAMPLE_DIR / 'expert-provider-profiles.yaml')} needs six expert profiles")
    for profile in profiles:
        pid = profile.get("id", "<unknown>")
        if not profile.get("allowed_knowledge_scopes"):
            errors.append(f"expert provider {pid} missing allowed_knowledge_scopes")
        source = profile.get("source_authority")
        if not isinstance(source, dict):
            errors.append(f"expert provider {pid} missing source_authority")
            continue
        for key in ["minimum_level", "citations_required", "freshness_required"]:
            if key not in source:
                errors.append(f"expert provider {pid} source_authority missing {key}")


def validate_examples(errors: list[str]) -> None:
    require_files(EXAMPLE_DIR, REQUIRED_EXAMPLES, errors)
    bindings = load_yaml(EXAMPLE_DIR / "provider-bindings.example.yaml").get("provider_bindings", [])
    if not any(binding.get("grant", {}).get("issued_to_gateway_only") is True for binding in bindings):
        errors.append("provider bindings must include gateway-only grants")
    if not any(binding.get("grant", {}).get("read_only") is True for binding in bindings):
        errors.append("provider bindings must include read-only diagnostic binding")

    stack = load_yaml(EXAMPLE_DIR / "domain-stack-memory-gateway.example.yaml").get("memory_gateway", {})
    if stack.get("conformance_tier") != "M0":
        errors.append("domain stack example must declare M0 conformance")
    provider_ids = {provider.get("provider_id") for provider in stack.get("providers", [])}
    for binding in stack.get("bindings", []):
        if binding.get("provider_id") not in provider_ids:
            errors.append(f"domain stack binding {binding.get('binding_id')} references unknown provider")
    expert = stack.get("omnigent_expert_memory_gateway", {})
    for key in ["allowed_knowledge_scopes", "source_authority_minimum", "audit_required"]:
        if key not in expert:
            errors.append(f"domain stack omnigent_expert_memory_gateway missing {key}")

    break_glass = load_yaml(EXAMPLE_DIR / "medx-break-glass.example.yaml").get("break_glass_profile", {})
    for key in [
        "allowed_actor_classes",
        "subject_scope",
        "provider_binding_refs",
        "minimal_packet_profile",
        "max_ttl_seconds",
        "escalation_targets",
        "retrospective_review_sla",
    ]:
        if not break_glass.get(key):
            errors.append(f"medx break-glass example missing {key}")


def _binding_surface_violations(value: Any, path: str, errors: list[str], where: str) -> None:
    """A memory binding is rails input: any provider/credential surface fails."""
    forbidden = ("provider", "credential", "secret", "endpoint", "token")
    if isinstance(value, dict):
        for key, child in value.items():
            key_l = str(key).lower()
            if any(marker in key_l for marker in forbidden):
                errors.append(f"{where} memory binding carries a provider/credential surface: {path}.{key}")
            _binding_surface_violations(child, f"{path}.{key}", errors, where)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _binding_surface_violations(child, f"{path}[{index}]", errors, where)


def validate_memory_bindings(errors: list[str]) -> None:
    """Deterministic memory-binding checks the schema shape cannot express."""
    vocab = load_yaml(CONTRACT_DIR / "vocabularies.yaml").get("vocabularies", {})
    authority_levels = set(vocab.get("authority_levels") or [])
    example_path = EXAMPLE_DIR / "memory-binding.example.yaml"
    bindings = load_yaml(example_path).get("memory_bindings", [])
    if not bindings:
        errors.append(f"{rel(example_path)} carries no memory_bindings")
        return
    for binding in bindings:
        where = f"{rel(example_path)} ({binding.get('layer_role', '?')})"
        if binding.get("kind") != "hermes_memory_binding":
            errors.append(f"{where} kind must be hermes_memory_binding")
        if binding.get("derived_from") != "memory_boundary":
            errors.append(f"{where} derived_from must be memory_boundary")
        if not binding.get("vocabulary_bundle_tag"):
            errors.append(f"{where} missing vocabulary_bundle_tag")
        for scope in binding.get("scopes", []):
            promotion = scope.get("promotion")
            if promotion is None:
                continue
            if promotion.get("gateway") != "customer_memory_gateway":
                errors.append(f"{where} scope {scope.get('scope')} promotion gateway must be customer_memory_gateway")
            level = promotion.get("accepted_authority_level")
            if level is not None and level not in authority_levels:
                errors.append(f"{where} scope {scope.get('scope')} accepted_authority_level outside authority_levels: {level}")
        _binding_surface_violations(binding, "binding", errors, where)


SEMANTIC_AUTHORITY_KEYS = {
    "effect", "permission", "permissions", "grant", "grants", "credential",
    "credentials", "scope", "scopes", "route", "routing", "token", "secret",
    "binding", "approval",
}


def validate_semantic_context(errors: list[str]) -> None:
    """Semantic-context preflight (add-domain-ontology-layer, tasks 6.2/6.3):
    every example packet carrying a semantic_context block is checked the way
    the gateway must check it BEFORE provider I/O — exact ids and digests,
    published-or-deprecated package lifecycle (retired fails closed), purpose
    agreement with the packet (cross-purpose reuse is a new-packet event),
    and a non-empty bounded term subset. The block can never widen anything:
    an authority-named key inside it is a violation."""
    checked = 0
    for example in sorted(EXAMPLE_DIR.glob("*.example.yaml")):
        doc = load_yaml(example)
        for packet_key in ("context_packet", "expert_context_packet"):
            packet = doc.get(packet_key)
            if not isinstance(packet, dict):
                continue
            ctx = packet.get("semantic_context")
            if ctx is None:
                continue
            checked += 1
            where = f"{example.name}:{packet_key}"
            for key in ("semantic_context_id", "content_digest", "purpose",
                        "kernel_pin", "package_pin", "term_subset", "lifecycle"):
                if key not in ctx:
                    errors.append(f"{where} semantic_context missing {key}")
            import re as _re
            if not _re.match(r"^[a-f0-9]{64}$", str(ctx.get("content_digest", ""))):
                errors.append(f"{where} semantic_context content_digest is not a sha256")
            for pin_name in ("kernel_pin", "package_pin"):
                pin = ctx.get(pin_name) or {}
                if not _re.match(r"^[a-f0-9]{64}$", str(pin.get("package_digest", ""))):
                    errors.append(f"{where} {pin_name} lacks an exact digest; "
                                  "an unpinned package fails closed")
            if ctx.get("purpose") != packet.get("purpose"):
                errors.append(f"{where} semantic_context purpose differs from the packet "
                              "purpose; cross-purpose reuse requires a new packet")
            state = (ctx.get("lifecycle") or {}).get("package_lifecycle_state")
            if state not in ("published", "deprecated"):
                errors.append(f"{where} semantic_context package lifecycle {state!r} "
                              "rejected before provider I/O")
            if not ctx.get("term_subset"):
                errors.append(f"{where} semantic_context term_subset is empty; an "
                              "unrestricted ontology corpus is never issued")
            stack = [ctx]
            while stack:
                node = stack.pop()
                if isinstance(node, dict):
                    for k, v in node.items():
                        if k.lower() in SEMANTIC_AUTHORITY_KEYS:
                            errors.append(f"{where} semantic_context carries authority-named "
                                          f"key {k!r}; semantic context never grants")
                        stack.append(v)
                elif isinstance(node, list):
                    stack.extend(node)
    if checked == 0:
        errors.append("no example packet exercises semantic_context")


def validate_fixtures(errors: list[str]) -> None:
    data = load_yaml(EXAMPLE_DIR / "conformance-fixtures.yaml")
    fixtures = data.get("fixtures", [])
    ids = {fixture.get("id") for fixture in fixtures}
    for required_id in sorted(REQUIRED_FIXTURE_IDS - ids):
        errors.append(f"conformance fixture missing {required_id}")
    for fixture in fixtures:
        if "provider_io_attempted" not in fixture:
            errors.append(f"fixture {fixture.get('id')} missing provider_io_attempted")


def validate_runtime_smoke(errors: list[str]) -> None:
    sys.path.insert(0, str(ROOT))
    from xfactory.memory_gateway import demo_gateway, utcnow  # noqa: PLC0415

    gateway = demo_gateway()
    request = {
        "id": "smoke-customer-context",
        "operation": "xfactory.memory.context_packet",
        "caller": {"id": "hermes-role:care", "type": "hermes_role", "authenticated": True},
        "consumer_layer": "customer",
        "purpose": "care_plan_review",
        "workflow_ref": "workflow:medx:care-plan-review",
        "client_ref": "client:medx-demo-clinic",
        "subject_refs": ["patient:demo-001"],
        "provider_id": "gbrain_customer_memory_v1",
        "consent_profile_ref": "consent:patient-demo-001:v3",
        "subject_safety_profile_ref": "medx_adult_patient_standard",
    }
    customer = gateway.context_packet(request)
    if customer.status != "allowed" or not customer.context_packet:
        errors.append("runtime smoke: customer context packet should be allowed")

    denied = gateway.context_packet({**request, "id": "smoke-no-caller", "caller": {}})
    if denied.status != "denied" or denied.denial_reason != "unauthenticated_caller":
        errors.append("runtime smoke: unattributable caller should deny")

    write_denied = gateway.write({
        **request,
        "id": "smoke-write-missing-source",
        "operation": "xfactory.memory.write",
        "payload": {"content": "new memory"},
    })
    if write_denied.denial_reason != "missing_source_refs":
        errors.append("runtime smoke: write without source refs should deny")

    expert = gateway.context_packet({
        "id": "smoke-expert-context",
        "operation": "xfactory.memory.context_packet",
        "caller": {"id": "omnigent:diagnostic", "type": "omnigent_worker", "authenticated": True},
        "consumer_layer": "domain_omnigent",
        "purpose": "diagnostic_review",
        "workflow_ref": "workflow:medx:diagnostic-review",
        "client_ref": "client:medx-demo-clinic",
        "provider_id": "medx_root_truth_db_v1",
        "expert_profile": "expert://medx/diagnostic-reviewer",
        "knowledge_scopes": ["clinical_guideline"],
        "min_source_authority": "reviewed",
    })
    if expert.status != "allowed" or not expert.expert_context_packet:
        errors.append("runtime smoke: expert context packet should be allowed")

    if customer.context_packet:
        expired = {**customer.context_packet, "expires_at": "2026-01-01T00:00:00Z"}
        consume = gateway.consume_context_packet(expired, purpose="care_plan_review", now=utcnow())
        if consume.denial_reason != "packet_expired":
            errors.append("runtime smoke: expired packet should deny")
        wrong = gateway.consume_context_packet(customer.context_packet, purpose="other_purpose", now=utcnow())
        if wrong.denial_reason != "packet_wrong_purpose":
            errors.append("runtime smoke: wrong purpose should deny")

    break_glass = gateway.context_packet({
        **request,
        "id": "smoke-break-glass",
        "workflow_ref": "workflow:medx:emergency-clinical-escalation",
        "purpose": "emergency_clinical_escalation",
        "emergency_basis": "active emergency escalation",
        "caller": {
            "id": "clinician:demo",
            "type": "hermes_role",
            "authenticated": True,
            "actor_class": "licensed_clinician",
        },
    })
    if break_glass.status != "allowed" or not break_glass.review_tasks:
        errors.append("runtime smoke: break-glass should create review task")


def main() -> int:
    errors: list[str] = []
    validate_contracts(errors)
    validate_provider_profiles(errors)
    validate_examples(errors)
    validate_memory_bindings(errors)
    validate_semantic_context(errors)
    validate_fixtures(errors)
    validate_runtime_smoke(errors)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK xFactory Memory Gateway contracts, examples, fixtures, and runtime smoke")
    return 0


if __name__ == "__main__":
    sys.exit(main())
