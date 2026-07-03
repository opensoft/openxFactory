"""Reference xFactory Memory Gateway control-plane slice.

This module is intentionally small and service-ready: callers pass dictionaries
that mirror the canonical contracts, and responses are content-light records
that can later move behind a network API without changing the
``xfactory.memory.*`` operation surface.
"""

from __future__ import annotations

import datetime as dt
import fnmatch
import hashlib
import re
import uuid
from dataclasses import dataclass, field
from typing import Any


SECRET_RE = re.compile(
    r"-----BEGIN .*PRIVATE KEY-----|\b(password|passwd|secret|token)\s*[:=]"
    r"\s*['\"]?[A-Za-z0-9+/]{12,}|\bsk-[A-Za-z0-9]{20,}\b|"
    r"\bgh[pousr]_[A-Za-z0-9]{20,}\b|\bAKIA[0-9A-Z]{16}\b",
    re.IGNORECASE,
)


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.UTC).replace(microsecond=0)


def iso(ts: dt.datetime) -> str:
    return ts.isoformat().replace("+00:00", "Z")


def parse_iso(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def ref(prefix: str) -> str:
    return f"{prefix}:{uuid.uuid4().hex[:12]}"


def subject_hash(subject_refs: list[str]) -> str:
    joined = "|".join(sorted(subject_refs))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]


@dataclass
class GatewayResult:
    status: str
    request_id: str
    response_id: str = field(default_factory=lambda: ref("response"))
    denial_reason: str | None = None
    context_packet: dict[str, Any] | None = None
    expert_context_packet: dict[str, Any] | None = None
    provider_mapping_refs: list[str] = field(default_factory=list)
    usage_events: list[dict[str, Any]] = field(default_factory=list)
    audit_events: list[dict[str, Any]] = field(default_factory=list)
    review_tasks: list[dict[str, Any]] = field(default_factory=list)

    def as_response(self) -> dict[str, Any]:
        response: dict[str, Any] = {
            "id": self.response_id,
            "request_id": self.request_id,
            "status": self.status,
            "audit_refs": [event["id"] for event in self.audit_events],
        }
        if self.denial_reason:
            response["denial_reason"] = self.denial_reason
        if self.context_packet:
            response["context_packet_ref"] = self.context_packet["id"]
        if self.expert_context_packet:
            response["expert_context_packet_ref"] = self.expert_context_packet["id"]
        if self.provider_mapping_refs:
            response["provider_mapping_refs"] = self.provider_mapping_refs
        if self.usage_events:
            response["usage_refs"] = [event["id"] for event in self.usage_events]
        if self.review_tasks:
            response["review_task_refs"] = [task["id"] for task in self.review_tasks]
        return {"response": response}


class LocalFakeAdapter:
    """Deterministic in-memory adapter used by examples and validation."""

    def query_customer_context(self, request: dict[str, Any], grant: dict[str, Any]) -> dict[str, Any]:
        subject_refs = request.get("subject_refs") or []
        return {
            "current_state_snapshot_refs": [f"current-state:{subject_refs[0]}:demo"] if subject_refs else [],
            "memory_item_refs": [f"memory-item:{subject_refs[0]}:demo"] if subject_refs else [],
            "source_claim_refs": [f"source-claim:{subject_refs[0]}:demo"] if subject_refs else [],
            "trace_refs": [f"trace:{request.get('workflow_ref', 'workflow')}:demo"],
            "provider_refs": [f"provider:{grant['provider_id']}"],
        }

    def query_expert_context(self, request: dict[str, Any], grant: dict[str, Any]) -> dict[str, Any]:
        scopes = request.get("knowledge_scopes") or []
        return {
            "source_refs": [f"source:{scope}:demo" for scope in scopes],
            "provider_refs": [f"provider:{grant['provider_id']}"],
            "source_authority": {
                "minimum_level": request.get("min_source_authority", "source_backed"),
                "citations_required": True,
                "freshness_checked_at": iso(utcnow()),
            },
        }


class MemoryGateway:
    """Reference implementation for the M0 gateway slice."""

    def __init__(
        self,
        *,
        providers: dict[str, dict[str, Any]],
        bindings: list[dict[str, Any]],
        consent_profiles: dict[str, dict[str, Any]] | None = None,
        subject_safety_profiles: dict[str, dict[str, Any]] | None = None,
        break_glass_profiles: dict[str, dict[str, Any]] | None = None,
        gateway_available: bool = True,
        adapter: LocalFakeAdapter | None = None,
    ) -> None:
        self.providers = providers
        self.bindings = bindings
        self.consent_profiles = consent_profiles or {}
        self.subject_safety_profiles = subject_safety_profiles or {}
        self.break_glass_profiles = break_glass_profiles or {}
        self.gateway_available = gateway_available
        self.adapter = adapter or LocalFakeAdapter()
        self.packet_cache: dict[tuple[str, str], dict[str, Any]] = {}

    def context_packet(self, request: dict[str, Any]) -> GatewayResult:
        request_id = request.get("id", "<missing>")
        operation = request.get("operation", "xfactory.memory.context_packet")
        if operation != "xfactory.memory.context_packet":
            return self._deny(request, "unsupported_operation", provider_io=False)

        if not self.gateway_available:
            return self._handle_read_outage(request)

        caller_denial = self._verify_caller(request)
        if caller_denial:
            return caller_denial

        break_glass = self._maybe_break_glass(request)
        if break_glass:
            return break_glass

        if request.get("consumer_layer") == "domain_omnigent":
            return self._expert_context_packet(request)

        consent_denial = self._check_consent(request)
        if consent_denial:
            return consent_denial

        status, redaction_class, safety_denial = self._resolve_subject_safety(request)
        if safety_denial and status == "denied":
            return safety_denial

        binding_result = self._resolve_binding(request)
        if isinstance(binding_result, GatewayResult):
            return binding_result
        binding, grant = binding_result

        data = self.adapter.query_customer_context(request, grant)
        issued_at = utcnow()
        packet = {
            "id": ref("context-packet"),
            "issued_at": iso(issued_at),
            "expires_at": iso(issued_at + dt.timedelta(seconds=int(request.get("ttl_seconds", 900)))),
            "purpose": request["purpose"],
            "workflow_ref": request["workflow_ref"],
            "subject_refs": request.get("subject_refs", []),
            "consent_profile_ref": request.get("consent_profile_ref"),
            "subject_safety_profile_ref": request.get("subject_safety_profile_ref"),
            "redaction_class": redaction_class,
            **data,
        }
        audit = self._audit(request, status, provider_io=True, rail_results=["caller", "consent", "subject_safety", "provider_binding"])
        usage = self._usage(request, grant, latency_ms=0)
        result = GatewayResult(
            status=status,
            request_id=request_id,
            context_packet=packet,
            provider_mapping_refs=[ref("provider-mapping")],
            usage_events=[usage],
            audit_events=[audit],
        )
        self.packet_cache[(request["workflow_ref"], request["purpose"])] = packet
        return result

    def write(self, request: dict[str, Any]) -> GatewayResult:
        if not self.gateway_available:
            return self._deny(request, "gateway_unavailable", status="failed_closed", provider_io=False)
        caller_denial = self._verify_caller(request)
        if caller_denial:
            return caller_denial
        source_refs = request.get("payload", {}).get("source_refs") or request.get("source_refs")
        if not source_refs:
            return self._deny(request, "missing_source_refs", provider_io=False)
        if self._contains_secret(request.get("payload", {})):
            return self._deny(request, "secret_like_content", provider_io=False)
        binding_result = self._resolve_binding(request)
        if isinstance(binding_result, GatewayResult):
            return binding_result
        binding, grant = binding_result
        audit = self._audit(request, "allowed", provider_io=True, rail_results=["caller", "source_refs", "secret_scan", "provider_binding"])
        usage = self._usage(request, grant, latency_ms=0)
        return GatewayResult(
            status="allowed",
            request_id=request.get("id", "<missing>"),
            provider_mapping_refs=[ref("provider-mapping")],
            usage_events=[usage],
            audit_events=[audit],
        )

    def provider_health(self, request: dict[str, Any]) -> GatewayResult:
        caller_denial = self._verify_caller(request)
        if caller_denial:
            return caller_denial
        binding_result = self._resolve_binding(request)
        if isinstance(binding_result, GatewayResult):
            return binding_result
        _binding, grant = binding_result
        if not grant.get("read_only") and request.get("consumer_layer") == "xfactory":
            return self._deny(request, "provider_binding_denied", provider_io=False)
        audit = self._audit(request, "allowed", provider_io=True, rail_results=["caller", "diagnostic_binding"])
        return GatewayResult(status="allowed", request_id=request.get("id", "<missing>"), audit_events=[audit])

    def consume_context_packet(self, packet: dict[str, Any], *, purpose: str, now: dt.datetime | None = None) -> GatewayResult:
        now = now or utcnow()
        request = {
            "id": ref("consume"),
            "operation": "context_packet_consume",
            "caller": {"id": "consumer", "authenticated": True},
            "consumer_layer": "runtime",
            "purpose": purpose,
            "workflow_ref": packet.get("workflow_ref", "<unknown>"),
        }
        if parse_iso(packet["expires_at"]) <= now:
            return self._deny(request, "packet_expired", provider_io=False)
        if packet.get("purpose") != purpose:
            return self._deny(request, "packet_wrong_purpose", provider_io=False)
        audit = self._audit(request, "allowed", provider_io=False, rail_results=["packet_ttl", "packet_purpose"])
        return GatewayResult(status="allowed", request_id=request["id"], audit_events=[audit])

    def _expert_context_packet(self, request: dict[str, Any]) -> GatewayResult:
        if not request.get("expert_profile"):
            return self._deny(request, "missing_expert_profile", provider_io=False)
        provider = self.providers.get(request.get("provider_id", ""))
        source_policy = provider.get("source_authority", {}) if isinstance(provider, dict) else {}
        if source_policy.get("citations_required") and request.get("min_source_authority") == "below_threshold":
            return self._deny(request, "source_authority_below_threshold", provider_io=False)
        binding_result = self._resolve_binding(request)
        if isinstance(binding_result, GatewayResult):
            return binding_result
        binding, grant = binding_result
        issued_at = utcnow()
        data = self.adapter.query_expert_context(request, grant)
        packet = {
            "id": ref("expert-context"),
            "issued_at": iso(issued_at),
            "expires_at": iso(issued_at + dt.timedelta(seconds=int(request.get("ttl_seconds", 1200)))),
            "expert_profile": request["expert_profile"],
            "workflow_ref": request["workflow_ref"],
            "knowledge_scopes": request.get("knowledge_scopes", []),
            "allowed_uses": request.get("allowed_uses", [request["purpose"]]),
            "prohibited_uses": request.get("prohibited_uses", ["authoritative_db_mutation"]),
            **data,
        }
        audit = self._audit(request, "allowed", provider_io=True, rail_results=["caller", "expert_profile", "source_authority", "provider_binding"])
        usage = self._usage(request, grant, latency_ms=0)
        packet["audit_refs"] = [audit["id"]]
        packet["usage_refs"] = [usage["id"]]
        return GatewayResult(
            status="allowed",
            request_id=request.get("id", "<missing>"),
            expert_context_packet=packet,
            provider_mapping_refs=[ref("provider-mapping")],
            usage_events=[usage],
            audit_events=[audit],
        )

    def _maybe_break_glass(self, request: dict[str, Any]) -> GatewayResult | None:
        if not request.get("emergency_basis"):
            return None
        profile = self.break_glass_profiles.get(request.get("workflow_ref", ""))
        if not profile:
            return self._deny(request, "break_glass_not_declared", provider_io=False)
        caller_class = request.get("caller", {}).get("actor_class")
        if caller_class not in profile.get("allowed_actor_classes", []):
            return self._deny(request, "break_glass_not_declared", provider_io=False)
        if not self._scope_matches(request.get("subject_refs", []), profile.get("subject_scope", [])):
            return self._deny(request, "provider_binding_denied", provider_io=False)
        binding_result = self._resolve_binding(request)
        if isinstance(binding_result, GatewayResult):
            return binding_result
        _binding, grant = binding_result
        issued_at = utcnow()
        ttl = min(int(request.get("ttl_seconds", profile.get("max_ttl_seconds", 900))), int(profile.get("max_ttl_seconds", 900)))
        packet = {
            "id": ref("context-packet"),
            "issued_at": iso(issued_at),
            "expires_at": iso(issued_at + dt.timedelta(seconds=ttl)),
            "purpose": request["purpose"],
            "workflow_ref": request["workflow_ref"],
            "subject_refs": request.get("subject_refs", []),
            "redaction_class": profile.get("redaction_class", "emergency_minimal"),
            "minimal_packet_profile": profile.get("minimal_packet_profile", {}),
            "trace_refs": [ref("break-glass-trace")],
            "provider_refs": [f"provider:{grant['provider_id']}"],
        }
        review_task = {
            "id": ref("review-task"),
            "sla": profile.get("retrospective_review_sla"),
            "targets": profile.get("escalation_targets", []),
        }
        audit = self._audit(
            request,
            "allowed",
            provider_io=True,
            rail_results=["caller", "break_glass_profile", "subject_scope", "provider_binding", "ttl"],
            enhanced=True,
            review_task_ref=review_task["id"],
        )
        packet["audit_refs"] = [audit["id"]]
        return GatewayResult(
            status="allowed",
            request_id=request.get("id", "<missing>"),
            context_packet=packet,
            audit_events=[audit],
            review_tasks=[review_task],
        )

    def _handle_read_outage(self, request: dict[str, Any]) -> GatewayResult:
        key = (request.get("workflow_ref", ""), request.get("purpose", ""))
        cached = self.packet_cache.get(key)
        if cached and parse_iso(cached["expires_at"]) > utcnow():
            audit = self._audit(request, "degraded", provider_io=False, rail_results=["outage_cache"])
            return GatewayResult(status="degraded", request_id=request.get("id", "<missing>"), context_packet=cached, audit_events=[audit])
        return self._deny(request, "gateway_unavailable", provider_io=False)

    def _verify_caller(self, request: dict[str, Any]) -> GatewayResult | None:
        caller = request.get("caller")
        if not isinstance(caller, dict) or not caller.get("id") or caller.get("authenticated") is not True or not request.get("consumer_layer"):
            return self._deny(request, "unauthenticated_caller", provider_io=False)
        return None

    def _check_consent(self, request: dict[str, Any]) -> GatewayResult | None:
        consent_ref = request.get("consent_profile_ref")
        consent = self.consent_profiles.get(consent_ref or "")
        if not consent:
            return self._deny(request, "missing_consent", provider_io=False)
        if consent.get("status") != "active":
            return self._deny(request, "consent_withdrawn", provider_io=False)
        if request.get("purpose") not in consent.get("purposes", []):
            return self._deny(request, "missing_consent", provider_io=False)
        return None

    def _resolve_subject_safety(self, request: dict[str, Any]) -> tuple[str, str, GatewayResult | None]:
        profile = self.subject_safety_profiles.get(request.get("subject_safety_profile_ref", ""))
        if not profile:
            return "allowed", request.get("redaction_class", "standard"), None
        if profile.get("subject_category") == "minor" and profile.get("authority_mode") not in {"guardian", "delegated", "court_ordered"}:
            return "denied", profile.get("redaction_class", "minor_safe"), self._deny(request, "subject_safety_denied", provider_io=False)
        prohibited = set(profile.get("prohibited_uses", []))
        requested = set(request.get("requested_uses", []))
        if prohibited & requested:
            return "degraded", profile.get("redaction_class", "minor_safe"), None
        return "allowed", profile.get("redaction_class", request.get("redaction_class", "standard")), None

    def _resolve_binding(self, request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]] | GatewayResult:
        provider_id = request.get("provider_id")
        operation = request.get("operation")
        for binding in self.bindings:
            if binding.get("provider_id") != provider_id:
                continue
            if request.get("consumer_layer") not in binding.get("allowed_layers", []):
                continue
            if operation not in binding.get("allowed_operations", []):
                continue
            if request.get("client_ref") and request.get("client_ref") not in binding.get("allowed_clients", []):
                continue
            if not self._scope_matches(request.get("subject_refs", ["domain:medx"]), binding.get("allowed_subject_scopes", [])):
                continue
            grant_info = binding.get("grant", {})
            grant = {
                "id": ref("grant"),
                "provider_id": provider_id,
                "broker_ref": grant_info.get("broker_ref"),
                "ttl_seconds": grant_info.get("ttl_seconds", 300),
                "issued_to_gateway_only": grant_info.get("issued_to_gateway_only") is True,
                "read_only": grant_info.get("read_only", operation in {"xfactory.memory.query", "xfactory.memory.context_packet", "xfactory.memory.provider_health"}),
            }
            if not grant["issued_to_gateway_only"]:
                return self._deny(request, "provider_binding_denied", provider_io=False)
            return binding, grant
        return self._deny(request, "provider_binding_denied", provider_io=False)

    @staticmethod
    def _scope_matches(subject_refs: list[str], allowed_scopes: list[str]) -> bool:
        if not subject_refs:
            return True
        if "*" in allowed_scopes:
            return True
        return all(any(fnmatch.fnmatch(subject, pattern) for pattern in allowed_scopes) for subject in subject_refs)

    def _deny(self, request: dict[str, Any], reason: str, *, status: str = "denied", provider_io: bool) -> GatewayResult:
        audit = self._audit(request, status, provider_io=provider_io, rail_results=[reason], denial_reason=reason)
        return GatewayResult(status=status, request_id=request.get("id", "<missing>"), denial_reason=reason, audit_events=[audit])

    def _audit(
        self,
        request: dict[str, Any],
        decision: str,
        *,
        provider_io: bool,
        rail_results: list[str],
        denial_reason: str | None = None,
        enhanced: bool = False,
        review_task_ref: str | None = None,
    ) -> dict[str, Any]:
        consent = self.consent_profiles.get(request.get("consent_profile_ref", ""))
        event = {
            "id": ref("audit"),
            "at": iso(utcnow()),
            "operation": request.get("operation", "<unknown>"),
            "caller_ref": request.get("caller", {}).get("id", "<unknown>"),
            "consumer_layer": request.get("consumer_layer"),
            "decision": decision,
            "rail_results": [{"id": rail, "decision": decision} for rail in rail_results],
            "provider_io_attempted": provider_io,
            "enhanced": enhanced,
        }
        if denial_reason:
            event["denial_reason"] = denial_reason
        if consent:
            event["consent_profile_version"] = consent.get("version")
        if review_task_ref:
            event["review_task_ref"] = review_task_ref
        return event

    def _usage(self, request: dict[str, Any], grant: dict[str, Any], *, latency_ms: int) -> dict[str, Any]:
        return {
            "id": ref("usage"),
            "operation": request.get("operation"),
            "provider_role": self.providers.get(grant["provider_id"], {}).get("provider_role", "unknown"),
            "provider_id": grant["provider_id"],
            "client_ref": request.get("client_ref", "unknown"),
            "domain_ref": request.get("domain_ref", "unknown"),
            "workflow_ref": request.get("workflow_ref", "unknown"),
            "bill_to": request.get("bill_to", request.get("client_ref", "opensoft")),
            "usage_units": {"requests": 1},
            "latency_ms": latency_ms,
            "subject_ref_hash": subject_hash(request.get("subject_refs", [])),
        }

    def _contains_secret(self, value: Any) -> bool:
        if isinstance(value, dict):
            return any(self._contains_secret(v) for v in value.values())
        if isinstance(value, list):
            return any(self._contains_secret(v) for v in value)
        if isinstance(value, str):
            return bool(SECRET_RE.search(value))
        return False


def demo_gateway() -> MemoryGateway:
    """Return a deterministic gateway configured for validation smoke tests."""

    providers = {
        "gbrain_customer_memory_v1": {
            "provider_role": "customer_memory",
            "source_authority": {"citations_required": False},
        },
        "medx_root_truth_db_v1": {
            "provider_role": "root_truth_db",
            "source_authority": {"citations_required": True},
        },
    }
    bindings = [
        {
            "id": "opensoft_hosted_gbrain_medx_dev",
            "provider_id": "gbrain_customer_memory_v1",
            "allowed_layers": ["customer", "client"],
            "allowed_operations": ["xfactory.memory.query", "xfactory.memory.context_packet", "xfactory.memory.write"],
            "allowed_clients": ["client:medx-demo-clinic"],
            "allowed_subject_scopes": ["patient:demo-*"],
            "grant": {"broker_ref": "broker://opensoft/dev/memory", "ttl_seconds": 900, "issued_to_gateway_only": True},
        },
        {
            "id": "hybrid_medx_expert_knowledge",
            "provider_id": "medx_root_truth_db_v1",
            "allowed_layers": ["domain_omnigent"],
            "allowed_operations": ["xfactory.memory.context_packet", "xfactory.memory.query"],
            "allowed_clients": ["client:medx-demo-clinic"],
            "allowed_subject_scopes": ["domain:medx"],
            "grant": {"broker_ref": "broker://hybrid/medx/expert-knowledge", "ttl_seconds": 300, "issued_to_gateway_only": True},
        },
    ]
    consent_profiles = {
        "consent:patient-demo-001:v3": {
            "id": "consent:patient-demo-001",
            "version": "v3",
            "subject_ref": "patient:demo-001",
            "status": "active",
            "purposes": ["care_plan_review", "diagnostic_review"],
        }
    }
    subject_profiles = {
        "medx_adult_patient_standard": {
            "id": "medx_adult_patient_standard",
            "subject_category": "adult",
            "age_band": "adult",
            "authority_mode": "direct",
            "prohibited_uses": [],
            "redaction_class": "customer_private",
        },
        "medx_minor_patient_guardian": {
            "id": "medx_minor_patient_guardian",
            "subject_category": "minor",
            "age_band": "minor_13_to_15",
            "authority_mode": "guardian",
            "prohibited_uses": ["marketing_personalization", "autonomous_sensitive_disclosure"],
            "redaction_class": "minor_safe",
        },
    }
    break_glass_profiles = {
        "workflow:medx:emergency-clinical-escalation": {
            "id": "medx_emergency_clinical_escalation",
            "allowed_actor_classes": ["licensed_clinician", "emergency_supervisor"],
            "subject_scope": ["patient:demo-*"],
            "redaction_class": "emergency_minimal",
            "minimal_packet_profile": {"includes": ["active_allergies", "current_medications"]},
            "max_ttl_seconds": 900,
            "escalation_targets": ["review-council:medx-clinical-safety"],
            "retrospective_review_sla": "PT24H",
        }
    }
    return MemoryGateway(
        providers=providers,
        bindings=bindings,
        consent_profiles=consent_profiles,
        subject_safety_profiles=subject_profiles,
        break_glass_profiles=break_glass_profiles,
    )
