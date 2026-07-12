"""Portable fail-closed semantics for artifacts, approvals, and trace evidence.

These checks deliberately do not claim database isolation or transactional
authorization. PostgreSQL conformance owns those enforcement guarantees; this
module validates immutable portable records and their exact cross-record
bindings before they can become candidate evidence.

``validate_evidence_document`` is the fail-closed public orchestration boundary
and runs the complete T045 authority validator once before dispatch. The
lower-level helpers remain composable pure checks and assume that boundary has
already accepted their authority document.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime

from scripts.hermes_runtime_validation.semantics.authority import (
    validate_active_principal,
    validate_authority_document,
)

Finding = dict[str, str]


def _finding(code: str, path: str, message: str) -> Finding:
    return {
        "code": code,
        "severity": "error",
        "case_id": "",
        "path": path,
        "message": message,
    }


def _sorted(findings: Sequence[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda item: (
            item["path"],
            item["code"],
            item["message"],
        ),
    )


def _time(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _scope_tuple(scope: Mapping[str, object] | None) -> tuple[str, ...] | None:
    if not isinstance(scope, Mapping):
        return None
    kind = scope.get("scope_kind")
    values = [kind, scope.get("installation_id")]
    if kind in {"stack", "layer"}:
        values.append(scope.get("stack_id"))
    if kind == "layer":
        values.append(scope.get("layer_id"))
    if any(not isinstance(value, str) or not value for value in values):
        return None
    return tuple(str(value) for value in values)


def _resource_scope(resource: Mapping[str, object]) -> dict[str, object]:
    return {
        "scope_kind": "layer",
        "installation_id": resource.get("installation_id"),
        "stack_id": resource.get("stack_id"),
        "layer_id": resource.get("layer_id"),
    }


def _resource_key(resource: Mapping[str, object]) -> tuple[object, ...]:
    return (
        resource.get("installation_id"),
        resource.get("stack_id"),
        resource.get("layer_id"),
        resource.get("resource_type"),
        resource.get("resource_id"),
    )


def _principal_ref(value: object) -> tuple[tuple[str, ...], str, str] | None:
    if not isinstance(value, Mapping):
        return None
    scope = _scope_tuple(
        value.get("scope") if isinstance(value.get("scope"), Mapping) else None
    )
    principal_id = value.get("principal_id")
    digest = value.get("record_digest")
    if (
        scope is None
        or not isinstance(principal_id, str)
        or not isinstance(digest, str)
    ):
        return None
    return scope, principal_id, digest


def _grant_ref(value: object) -> tuple[str, str, str] | None:
    if not isinstance(value, Mapping):
        return None
    installation_id = value.get("installation_id")
    grant_id = value.get("grant_id")
    digest = value.get("record_digest")
    if not all(isinstance(item, str) for item in (installation_id, grant_id, digest)):
        return None
    return str(installation_id), str(grant_id), str(digest)


def _binding_ref(value: object) -> tuple[str, str, str] | None:
    if not isinstance(value, Mapping):
        return None
    installation_id = value.get("installation_id")
    binding_id = value.get("binding_id")
    digest = value.get("record_digest")
    if not all(isinstance(item, str) for item in (installation_id, binding_id, digest)):
        return None
    return str(installation_id), str(binding_id), str(digest)


def _operation_ref(value: object) -> tuple[str, str, str] | None:
    if not isinstance(value, Mapping):
        return None
    installation_id = value.get("installation_id")
    operation_id = value.get("operation_id")
    digest = value.get("record_digest")
    if not all(
        isinstance(item, str) for item in (installation_id, operation_id, digest)
    ):
        return None
    return str(installation_id), str(operation_id), str(digest)


def _items(document: Mapping[str, object], key: str) -> list[Mapping[str, object]]:
    values = document.get(key)
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        return []
    return [value for value in values if isinstance(value, Mapping)]


def validate_artifact_record(record: Mapping[str, object]) -> list[Finding]:
    """Validate cross-field artifact storage identity."""

    digest = record.get("content_digest")
    installation_id = record.get("installation_id")
    layer_id = record.get("layer_id")
    expected = None
    if all(isinstance(value, str) for value in (digest, installation_id, layer_id)):
        expected = (
            f"{installation_id}/{layer_id}/sha256/"
            f"{str(digest).removeprefix('sha256:')}"
        )
    if expected is None or record.get("storage_key") != expected:
        return [
            _finding(
                "HGR-ARTIFACT-STORAGE-KEY",
                "storage_key",
                "artifact storage key must be derived from owning scope and content digest",
            )
        ]
    return []


def validate_artifact_body(
    record: Mapping[str, object],
    body: bytes | None,
    *,
    stage: str,
) -> list[Finding]:
    """Reverify finalized body bytes at admission, approval, or execution."""

    if stage not in {"admission", "approval", "execution"}:
        return [
            _finding(
                "HGR-ARTIFACT-GATE-UNKNOWN",
                "stage",
                f"unknown artifact verification stage {stage!r}",
            )
        ]
    if body is None:
        return [
            _finding(
                "HGR-ARTIFACT-BODY-MISSING",
                f"{stage}.body",
                f"artifact body is unavailable at {stage}",
            )
        ]

    actual_digest = "sha256:" + hashlib.sha256(body).hexdigest()
    if record.get("content_digest") != actual_digest:
        return [
            _finding(
                "HGR-ARTIFACT-DIGEST-MISMATCH",
                f"{stage}.content_digest",
                f"artifact body digest does not match at {stage}",
            )
        ]
    if record.get("byte_size") != len(body):
        return [
            _finding(
                "HGR-ARTIFACT-SIZE-MISMATCH",
                f"{stage}.byte_size",
                f"artifact body size does not match at {stage}",
            )
        ]
    return []


def validate_artifact_immutability(
    original: Mapping[str, object], candidate: Mapping[str, object]
) -> list[Finding]:
    if original != candidate:
        return [
            _finding(
                "HGR-ARTIFACT-IMMUTABLE",
                "artifact_record",
                "artifact records are wholly immutable",
            )
        ]
    return []


def validate_artifact_lifecycle_append_only(
    original: Sequence[Mapping[str, object]],
    candidate: Sequence[Mapping[str, object]],
) -> list[Finding]:
    if len(candidate) < len(original):
        return [
            _finding(
                "HGR-ARTIFACT-LIFECYCLE-DELETE",
                "artifact_lifecycle_events",
                "existing artifact lifecycle events cannot be deleted",
            )
        ]
    if list(candidate[: len(original)]) != list(original):
        return [
            _finding(
                "HGR-ARTIFACT-LIFECYCLE-IMMUTABLE",
                "artifact_lifecycle_events",
                "existing artifact lifecycle events cannot be rewritten",
            )
        ]
    return []


def admit_artifact_access(
    request_scope: Mapping[str, object],
    artifact_scope: Mapping[str, object] | None,
    body_lookup: Callable[[], bytes],
) -> dict[str, object]:
    """Apply scope admission before body lookup and return one anti-oracle shape."""

    if artifact_scope is None or _scope_tuple(request_scope) != _scope_tuple(
        artifact_scope
    ):
        return {
            "allowed": False,
            "status": 404,
            "code": "HGR-ARTIFACT-NOT-AVAILABLE",
            "body": None,
        }
    return {
        "allowed": True,
        "status": 200,
        "code": "HGR-ARTIFACT-AVAILABLE",
        "body": body_lookup(),
    }


def _grant_matches(
    authority_document: Mapping[str, object],
    *,
    grant_ref: object,
    principal_ref: object,
    scope: Mapping[str, object],
    action: str,
    resource_constraint: Mapping[str, object],
    evaluation_time: str,
) -> bool:
    at = _time(evaluation_time)
    exact_grant_ref = _grant_ref(grant_ref)
    exact_principal_ref = _principal_ref(principal_ref)
    if at is None or exact_grant_ref is None or exact_principal_ref is None:
        return False
    if validate_active_principal(
        principal_ref,
        authority_document,
        evaluation_time=evaluation_time,
    ):
        return False

    for grant in _items(authority_document, "authority_grants"):
        if (
            (
                grant.get("installation_id"),
                grant.get("grant_id"),
                grant.get("record_digest"),
            )
            != exact_grant_ref
            or _principal_ref(grant.get("principal_ref")) != exact_principal_ref
            or _scope_tuple(
                grant.get("scope") if isinstance(grant.get("scope"), Mapping) else None
            )
            != _scope_tuple(scope)
            or grant.get("action") != action
            or grant.get("resource_constraint") != resource_constraint
        ):
            continue
        starts = _time(grant.get("starts_at"))
        expires = _time(grant.get("expires_at"))
        if starts is None or expires is None or not (starts <= at < expires):
            continue
        if any(
            _grant_ref(revocation.get("grant_ref")) == exact_grant_ref
            and (effective := _time(revocation.get("effective_at"))) is not None
            and effective <= at
            for revocation in _items(authority_document, "grant_revocations")
        ):
            continue
        return True
    return False


def _principal_matches_selector(
    principal_ref: object,
    selector: Mapping[str, object],
    authority_document: Mapping[str, object],
) -> bool:
    exact_ref = _principal_ref(principal_ref)
    if exact_ref is None:
        return False
    principal = next(
        (
            candidate
            for candidate in _items(authority_document, "principals")
            if _principal_ref(
                {
                    "scope": candidate.get("scope"),
                    "principal_id": candidate.get("principal_id"),
                    "record_digest": candidate.get("record_digest"),
                }
            )
            == exact_ref
        ),
        None,
    )
    if principal is None:
        return False
    principal_id = exact_ref[1]
    return (
        principal_id in (selector.get("principal_ids") or [])
        or principal.get("principal_type") in (selector.get("principal_types") or [])
        or (
            principal.get("principal_type") == "group"
            and principal_id in (selector.get("group_principal_ids") or [])
        )
    )


def _approval_resource(
    record: Mapping[str, object], resource_type: str
) -> dict[str, object] | None:
    owning_scope = record.get("owning_scope")
    if not isinstance(owning_scope, Mapping) or _scope_tuple(owning_scope) is None:
        return None
    identifier_key = (
        "request_id" if resource_type == "approval_request" else "decision_id"
    )
    digest_key = (
        "request_digest" if resource_type == "approval_request" else "decision_digest"
    )
    return {
        "installation_id": owning_scope.get("installation_id"),
        "stack_id": owning_scope.get("stack_id"),
        "layer_id": owning_scope.get("layer_id"),
        "resource_type": resource_type,
        "resource_id": record.get(identifier_key),
        "digest": record.get(digest_key),
    }


def _approval_result(state: str, authorizes: bool, findings: Sequence[Finding]) -> dict:
    return {
        "state": state,
        "authorizes": authorizes,
        "findings": _sorted(findings),
    }


def _authority_gate_result(
    findings: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    normalized = [
        {
            "code": str(finding.get("code", "HGR-AUTHORITY-INVALID")),
            "severity": str(finding.get("severity", "error")),
            "case_id": "",
            "path": str(finding.get("path", "authority_document")),
            "message": str(finding.get("message", "authority validation failed")),
        }
        for finding in findings
    ]
    return _approval_result("invalid", False, normalized)


def validate_evidence_document(document: Mapping[str, object]) -> dict[str, object]:
    """Fail closed at the T046 boundary before evaluating governed evidence.

    This is the canonical orchestration entrypoint. It validates the complete
    T045 authority document exactly once, returns those authority findings
    unchanged in meaning, and only then dispatches to the low-level pure
    artifact, approval, or trace checks.
    """

    authority_document = document.get("authority_document")
    evaluation_time = document.get("evaluation_time")
    payload = document.get("input")
    if (
        not isinstance(authority_document, Mapping)
        or not isinstance(evaluation_time, str)
        or not isinstance(payload, Mapping)
    ):
        return _authority_gate_result(
            [
                _finding(
                    "HGR-EVIDENCE-DOCUMENT",
                    "$",
                    "authority_document, evaluation_time, and input mappings are required",
                )
            ]
        )

    authority_findings = validate_authority_document(
        authority_document,
        evaluation_time=evaluation_time,
    )
    if authority_findings:
        return _authority_gate_result(authority_findings)

    operation = document.get("operation")
    if operation == "evaluate_approval":
        request = payload.get("request")
        policy = payload.get("policy")
        decisions = payload.get("decisions")
        supersessions = payload.get("supersessions", [])
        target = payload.get("target")
        if (
            not isinstance(request, Mapping)
            or not isinstance(policy, Mapping)
            or not isinstance(decisions, Sequence)
            or isinstance(decisions, (str, bytes))
            or not isinstance(supersessions, Sequence)
            or isinstance(supersessions, (str, bytes))
            or any(not isinstance(item, Mapping) for item in decisions)
            or any(not isinstance(item, Mapping) for item in supersessions)
            or not isinstance(target, Mapping)
        ):
            return _authority_gate_result(
                [
                    _finding(
                        "HGR-EVIDENCE-DOCUMENT",
                        "input",
                        "approval evidence input is incomplete",
                    )
                ]
            )
        return evaluate_approval(
            request,
            policy,
            [item for item in decisions if isinstance(item, Mapping)],
            supersessions=[item for item in supersessions if isinstance(item, Mapping)],
            authority_document=authority_document,
            target=target,
            evaluation_time=evaluation_time,
        )
    if operation == "validate_trace_edge":
        edge = payload.get("edge")
        if not isinstance(edge, Mapping):
            return _authority_gate_result(
                [
                    _finding(
                        "HGR-EVIDENCE-DOCUMENT",
                        "input.edge",
                        "trace evidence requires one edge",
                    )
                ]
            )
        findings = validate_trace_edge(
            edge,
            authority_document=authority_document,
            evaluation_time=evaluation_time,
        )
        return _approval_result("valid" if not findings else "invalid", False, findings)
    if operation == "validate_artifact_body":
        record = payload.get("record")
        stage = payload.get("stage")
        body_utf8 = payload.get("body_utf8")
        if (
            not isinstance(record, Mapping)
            or not isinstance(stage, str)
            or not isinstance(body_utf8, str)
        ):
            return _authority_gate_result(
                [
                    _finding(
                        "HGR-EVIDENCE-DOCUMENT",
                        "input",
                        "artifact evidence requires record, stage, and body_utf8",
                    )
                ]
            )
        findings = [
            *validate_artifact_record(record),
            *validate_artifact_body(record, body_utf8.encode("utf-8"), stage=stage),
        ]
        artifact_scope = _resource_scope(record)
        artifact_resource = {
            "installation_id": record.get("installation_id"),
            "stack_id": record.get("stack_id"),
            "layer_id": record.get("layer_id"),
            "resource_type": "artifact",
            "resource_id": record.get("artifact_id"),
            "digest": record.get("content_digest"),
        }
        created_at = record.get("created_at")
        if not isinstance(created_at, str) or not _grant_matches(
            authority_document,
            grant_ref=record.get("producer_grant_ref"),
            principal_ref=record.get("producer_principal_ref"),
            scope=artifact_scope,
            action="create_artifact",
            resource_constraint=artifact_resource,
            evaluation_time=created_at,
        ):
            findings.append(
                _finding(
                    "HGR-ARTIFACT-PRODUCER-AUTHORITY",
                    "input.record.producer_grant_ref",
                    "artifact producer lacks exact create-artifact authority",
                )
            )
        return _approval_result("valid" if not findings else "invalid", False, findings)
    return _authority_gate_result(
        [
            _finding(
                "HGR-EVIDENCE-OPERATION",
                "operation",
                "unsupported evidence operation",
            )
        ]
    )


def evaluate_approval(
    request: Mapping[str, object],
    policy: Mapping[str, object],
    decisions: Sequence[Mapping[str, object]],
    *,
    supersessions: Sequence[Mapping[str, object]] = (),
    authority_document: Mapping[str, object],
    target: Mapping[str, object] | None,
    evaluation_time: str,
) -> dict:
    """Evaluate one immutable request under its exact pinned policy."""

    policy_pin = request.get("decision_policy_pin")
    pin_digest = policy_pin.get("digest") if isinstance(policy_pin, Mapping) else None
    if (
        request.get("decision_policy_id") != policy.get("policy_id")
        or request.get("decision_policy_digest") != policy.get("policy_digest")
        or pin_digest != policy.get("policy_digest")
        or _scope_tuple(
            request.get("authority_scope")
            if isinstance(request.get("authority_scope"), Mapping)
            else None
        )
        != _scope_tuple(
            policy.get("authority_scope")
            if isinstance(policy.get("authority_scope"), Mapping)
            else None
        )
    ):
        return _approval_result(
            "invalid",
            False,
            [
                _finding(
                    "HGR-APPROVAL-POLICY-MISMATCH",
                    "decision_policy",
                    "request does not bind the exact policy ID, digest, pin, and scope",
                )
            ],
        )

    request_target = request.get("target")
    request_owning_scope = request.get("owning_scope")
    if (
        not isinstance(request_target, Mapping)
        or not isinstance(request_owning_scope, Mapping)
        or _scope_tuple(request_owning_scope)
        != _scope_tuple(_resource_scope(request_target))
        or target is None
        or request_target != target
    ):
        return _approval_result(
            "invalid",
            False,
            [
                _finding(
                    "HGR-APPROVAL-TARGET-DRIFT",
                    "target",
                    "current target coordinates or digest differ from the approval request",
                )
            ],
        )

    authority_scope = request.get("authority_scope")
    request_created_at = request.get("created_at")
    if (
        not isinstance(authority_scope, Mapping)
        or not isinstance(request_created_at, str)
        or not _grant_matches(
            authority_document,
            grant_ref=request.get("requester_grant_ref"),
            principal_ref=request.get("requester_principal_ref"),
            scope=authority_scope,
            action="request_approval",
            resource_constraint=request_target,
            evaluation_time=request_created_at,
        )
        or not _grant_matches(
            authority_document,
            grant_ref=request.get("requester_grant_ref"),
            principal_ref=request.get("requester_principal_ref"),
            scope=authority_scope,
            action="request_approval",
            resource_constraint=request_target,
            evaluation_time=evaluation_time,
        )
    ):
        return _approval_result(
            "invalid",
            False,
            [
                _finding(
                    "HGR-APPROVAL-REQUESTER-AUTHORITY",
                    "requester_grant",
                    "requester lacks the exact active request authority",
                )
            ],
        )

    at = _time(evaluation_time)
    expires = _time(request.get("expires_at"))
    if at is None or expires is None or at >= expires:
        return _approval_result(
            "expired",
            False,
            [
                _finding(
                    "HGR-APPROVAL-EXPIRED",
                    "expires_at",
                    "approval request is expired at evaluation time",
                )
            ],
        )

    raw_policy_supersession = [
        item
        for item in (policy.get("supersession_authorities") or [])
        if isinstance(item, Mapping) and isinstance(item.get("event_type"), str)
    ]
    policy_supersession = {
        item.get("event_type"): item for item in raw_policy_supersession
    }
    if len(policy_supersession) != len(raw_policy_supersession):
        return _approval_result(
            "invalid",
            False,
            [
                _finding(
                    "HGR-APPROVAL-POLICY-SUPERSESSION",
                    "policy.supersession_authorities",
                    "decision policy contains duplicate supersession event authorities",
                )
            ],
        )
    decision_by_id = {
        item.get("decision_id"): item
        for item in decisions
        if isinstance(item.get("decision_id"), str)
    }
    effective_request_events: list[str] = []
    superseded_decision_ids: set[str] = set()
    for event in supersessions:
        event_type = event.get("event_type")
        target_kind = event.get("target_kind")
        if target_kind == "request":
            exact_target = event.get("target_id") == request.get(
                "request_id"
            ) and event.get("target_digest") == request.get("request_digest")
        elif target_kind == "decision":
            decision = decision_by_id.get(event.get("target_id"))
            exact_target = bool(
                decision
                and event.get("target_digest") == decision.get("decision_digest")
            )
        else:
            exact_target = False
        issuer_selector = policy_supersession.get(event_type)
        event_scope = event.get("authority_scope")
        event_time = event.get("effective_at")
        if target_kind == "request":
            supersession_resource = _approval_resource(request, "approval_request")
        elif target_kind == "decision" and decision is not None:
            supersession_resource = _approval_resource(decision, "approval_decision")
        else:
            supersession_resource = None
        if (
            not exact_target
            or not isinstance(issuer_selector, Mapping)
            or not _principal_matches_selector(
                event.get("issuer_principal_ref"),
                issuer_selector,
                authority_document,
            )
            or not isinstance(event_scope, Mapping)
            or _scope_tuple(event_scope) != _scope_tuple(authority_scope)
            or event.get("owning_scope") != request.get("owning_scope")
            or supersession_resource is None
            or not isinstance(event_time, str)
            or not _grant_matches(
                authority_document,
                grant_ref=event.get("issuer_grant_ref"),
                principal_ref=event.get("issuer_principal_ref"),
                scope=event_scope,
                action="supersede_approval",
                resource_constraint=supersession_resource,
                evaluation_time=event_time,
            )
        ):
            return _approval_result(
                "invalid",
                False,
                [
                    _finding(
                        "HGR-APPROVAL-SUPERSESSION-AUTHORITY",
                        "supersessions",
                        "supersession lacks exact target, principal selector, scope, or active issuer grant",
                    )
                ],
            )
        if _time(event_time) is not None and _time(event_time) <= at:
            if target_kind == "request":
                effective_request_events.append(str(event_type))
            else:
                superseded_decision_ids.add(str(event.get("target_id")))

    if effective_request_events:
        precedence = {"expired": 0, "cancelled": 1, "revoked": 2}
        state = max(effective_request_events, key=lambda item: precedence[item])
        return _approval_result(state, False, [])

    raw_selectors = [
        item
        for item in (policy.get("reviewer_selectors") or [])
        if isinstance(item, Mapping) and isinstance(item.get("selector_id"), str)
    ]
    selectors = {item.get("selector_id"): item for item in raw_selectors}
    if len(selectors) != len(raw_selectors):
        return _approval_result(
            "invalid",
            False,
            [
                _finding(
                    "HGR-APPROVAL-POLICY-SELECTOR",
                    "policy.reviewer_selectors",
                    "decision policy contains duplicate reviewer selector IDs",
                )
            ],
        )
    requested_selectors = set(request.get("reviewer_selector_ids") or [])
    if not requested_selectors or requested_selectors != set(selectors):
        return _approval_result(
            "invalid",
            False,
            [
                _finding(
                    "HGR-APPROVAL-REVIEWER-SELECTOR",
                    "reviewer_selector_ids",
                    "request contains an unknown or empty reviewer selector set",
                )
            ],
        )

    approved_by_selector: dict[str, set[str]] = {
        str(selector): set() for selector in requested_selectors
    }
    has_approve = False
    has_reject = False
    for decision in decisions:
        exact_request = (
            decision.get("request_id") == request.get("request_id")
            and decision.get("request_digest") == request.get("request_digest")
            and decision.get("owning_scope") == request.get("owning_scope")
            and decision.get("target") == request_target
            and decision.get("requested_action") == request.get("requested_action")
            and decision.get("authority_scope") == authority_scope
            and decision.get("decision_policy_id") == request.get("decision_policy_id")
            and decision.get("decision_policy_digest")
            == request.get("decision_policy_digest")
        )
        if not exact_request:
            return _approval_result(
                "invalid",
                False,
                [
                    _finding(
                        "HGR-APPROVAL-DECISION-TARGET",
                        "decisions",
                        "decision does not repeat the exact request target, action, scope, and policy",
                    )
                ],
            )
        decided_at = _time(decision.get("decided_at"))
        created_at = _time(request.get("created_at"))
        if (
            decided_at is None
            or created_at is None
            or decided_at < created_at
            or decided_at >= expires
            or decided_at > at
        ):
            return _approval_result(
                "invalid",
                False,
                [
                    _finding(
                        "HGR-APPROVAL-DECISION-TIME",
                        "decisions.decided_at",
                        "decision time must be within the request window and no later than evaluation",
                    )
                ],
            )
        selector_id = decision.get("reviewer_selector_id")
        selector = selectors.get(selector_id)
        if selector_id not in requested_selectors or selector is None:
            return _approval_result(
                "invalid",
                False,
                [
                    _finding(
                        "HGR-APPROVAL-REVIEWER-SELECTOR",
                        "decisions.reviewer_selector_id",
                        "decision reviewer does not match a requested policy selector",
                    )
                ],
            )
        principal_ref = decision.get("actual_reviewer_principal_ref")
        if not _principal_matches_selector(
            principal_ref,
            selector,
            authority_document,
        ):
            return _approval_result(
                "invalid",
                False,
                [
                    _finding(
                        "HGR-APPROVAL-REVIEWER-SELECTOR",
                        "decisions.actual_reviewer_principal_ref",
                        "actual reviewer is outside the policy's closed principal selector",
                    )
                ],
            )
        request_resource = _approval_resource(request, "approval_request")
        if not _grant_matches(
            authority_document,
            grant_ref=decision.get("reviewer_grant_ref"),
            principal_ref=principal_ref,
            scope=authority_scope,
            action="decide_approval",
            resource_constraint=request_resource or {},
            evaluation_time=str(decision.get("decided_at", "")),
        ) or not _grant_matches(
            authority_document,
            grant_ref=decision.get("reviewer_grant_ref"),
            principal_ref=principal_ref,
            scope=authority_scope,
            action="decide_approval",
            resource_constraint=request_resource or {},
            evaluation_time=evaluation_time,
        ):
            return _approval_result(
                "invalid",
                False,
                [
                    _finding(
                        "HGR-APPROVAL-REVIEWER-AUTHORITY",
                        "decisions.reviewer_grant",
                        "actual reviewer lacks exact active decision authority",
                    )
                ],
            )
        exact_principal = _principal_ref(principal_ref)
        principal = exact_principal[1] if exact_principal is not None else ""
        if decision.get("decision_id") in superseded_decision_ids:
            continue
        if decision.get("decision") == "approve":
            has_approve = True
            approved_by_selector[str(selector_id)].add(principal)
        elif decision.get("decision") == "reject":
            has_reject = True

    if has_approve and has_reject:
        if policy.get("conflict_resolution") == "reject_overrides":
            return _approval_result("rejected", False, [])
        return _approval_result(
            "contested",
            False,
            [
                _finding(
                    "HGR-APPROVAL-CONTESTED",
                    "decisions",
                    "conflicting terminal decisions are non-authorizing under this policy",
                )
            ],
        )
    if has_reject:
        return _approval_result("rejected", False, [])

    if policy.get("aggregation") == "minimum_approvals":
        approved_count = len(set().union(*approved_by_selector.values()))
        satisfied = approved_count >= int(policy.get("minimum_approvals", 0))
    else:
        satisfied = all(
            len(approved_by_selector.get(str(selector_id), set()))
            >= int(selectors[selector_id].get("minimum_count", 0))
            for selector_id in requested_selectors
        )
    if not satisfied:
        return _approval_result(
            "pending",
            False,
            [
                _finding(
                    "HGR-APPROVAL-INSUFFICIENT",
                    "decisions",
                    "approval aggregation requirements are not satisfied",
                )
            ],
        )
    return _approval_result("approved", True, [])


def validate_approval_immutability(
    original: Mapping[str, object], candidate: Mapping[str, object]
) -> list[Finding]:
    if original != candidate:
        return [
            _finding(
                "HGR-APPROVAL-IMMUTABLE",
                "approval_record",
                "approval requests, policies, decisions, and supersessions are immutable",
            )
        ]
    return []


def _lookup_by_id(
    values: Sequence[Mapping[str, object]], key: str, identifier: str
) -> Mapping[str, object] | None:
    return next(
        (value for value in values if value.get(key) == identifier),
        None,
    )


def validate_trace_edge(
    edge: Mapping[str, object],
    *,
    authority_document: Mapping[str, object],
    evaluation_time: str,
) -> list[Finding]:
    """Validate endpoint digests and exact cross-layer authority evidence."""

    source = edge.get("source")
    target = edge.get("target")
    if not isinstance(source, Mapping) or not isinstance(target, Mapping):
        return [
            _finding(
                "HGR-TRACE-ENDPOINT-MISSING",
                "source|target",
                "trace endpoints must be exact content resource references",
            )
        ]
    resources = {}
    for item in _items(authority_document, "resources"):
        resource = item.get("resource_ref")
        if not isinstance(resource, Mapping):
            resource = item
        resources[_resource_key(resource)] = resource
    for name, endpoint in (("source", source), ("target", target)):
        actual = resources.get(_resource_key(endpoint))
        if actual is None:
            return [
                _finding(
                    "HGR-TRACE-ENDPOINT-MISSING",
                    name,
                    f"trace {name} endpoint does not resolve",
                )
            ]
        if actual.get("digest") != endpoint.get("digest"):
            return [
                _finding(
                    "HGR-TRACE-ENDPOINT-DIGEST",
                    f"{name}.digest",
                    f"trace {name} digest does not match the immutable resource",
                )
            ]

    cross_layer = _scope_tuple(_resource_scope(source)) != _scope_tuple(
        _resource_scope(target)
    )
    authority = edge.get("cross_layer_authority")
    if not cross_layer:
        if authority is not None:
            return [
                _finding(
                    "HGR-TRACE-UNRELATED-AUTHORITY",
                    "cross_layer_authority",
                    "same-layer traces cannot claim unrelated cross-layer authority",
                )
            ]
        return []
    if not isinstance(authority, Mapping):
        return [
            _finding(
                "HGR-TRACE-AUTHORITY-REQUIRED",
                "cross_layer_authority",
                "cross-layer trace requires operation, binding, and grant evidence",
            )
        ]

    operation_ref = _operation_ref(authority.get("operation_authorization_ref"))
    binding_ref = _binding_ref(authority.get("binding_ref"))
    grant_refs = [
        ref
        for ref in (_grant_ref(value) for value in (authority.get("grant_refs") or []))
        if ref is not None
    ]
    if operation_ref is None or binding_ref is None or not grant_refs:
        return [
            _finding(
                "HGR-TRACE-AUTHORITY-REQUIRED",
                "cross_layer_authority",
                "cross-layer trace authority references are incomplete",
            )
        ]

    operation = _lookup_by_id(
        _items(authority_document, "operation_authorizations"),
        "operation_id",
        operation_ref[1],
    )
    expected_operation_grants = [
        ref
        for ref in (
            _grant_ref(operation.get("source_grant_ref")) if operation else None,
            (
                _grant_ref(operation.get("target_acceptance_grant_ref"))
                if operation
                else None
            ),
        )
        if ref is not None
    ]
    authorized_at = _time(operation.get("authorized_at")) if operation else None
    created_at = _time(edge.get("created_at"))
    evaluated_at = _time(evaluation_time)
    if (
        operation is None
        or operation.get("record_digest") != operation_ref[2]
        or operation_ref[0] != source.get("installation_id")
        or operation.get("source_scope") != _resource_scope(source)
        or operation.get("target_scope") != _resource_scope(target)
        or operation.get("source_resource") != source
        or operation.get("target_resource") != target
        or operation.get("target_result") != target
        or operation.get("action") != edge.get("relation")
        or _binding_ref(operation.get("binding_ref")) != binding_ref
        or sorted(expected_operation_grants) != sorted(grant_refs)
        or operation.get("actor_principal_ref") != edge.get("creator_principal_ref")
        or _grant_ref(operation.get("source_grant_ref"))
        != _grant_ref(edge.get("creator_grant_ref"))
        or authorized_at is None
        or created_at is None
        or evaluated_at is None
        or not (authorized_at <= created_at <= evaluated_at)
    ):
        return [
            _finding(
                "HGR-TRACE-OPERATION-AUTHORIZATION",
                "cross_layer_authority.operation_authorization_ref",
                "operation authorization does not bind the exact endpoints, binding, and grants",
            )
        ]

    binding = _lookup_by_id(
        _items(authority_document, "cross_layer_bindings"),
        "binding_id",
        binding_ref[1],
    )
    if (
        binding is None
        or binding.get("record_digest") != binding_ref[2]
        or binding_ref[0] != source.get("installation_id")
        or binding.get("source_scope") != _resource_scope(source)
        or binding.get("target_scope") != _resource_scope(target)
        or binding.get("source_resource") != source
        or binding.get("target_resource") != target
        or binding.get("action") != edge.get("relation")
    ):
        return [
            _finding(
                "HGR-TRACE-BINDING",
                "cross_layer_authority.binding_ref",
                "binding does not match the exact trace endpoints and relation",
            )
        ]

    grants = _items(authority_document, "authority_grants")
    if any(
        not any(
            (
                grant.get("installation_id"),
                grant.get("grant_id"),
                grant.get("record_digest"),
            )
            == grant_ref
            for grant in grants
        )
        for grant_ref in grant_refs
    ):
        return [
            _finding(
                "HGR-TRACE-GRANT",
                "cross_layer_authority.grant_refs",
                "trace cites an unknown or digest-mismatched authority grant",
            )
        ]
    return []


def validate_trace_immutability(
    original: Mapping[str, object], candidate: Mapping[str, object]
) -> list[Finding]:
    if original != candidate:
        return [
            _finding(
                "HGR-TRACE-IMMUTABLE",
                "trace_edge",
                "trace edges are append-only and immutable",
            )
        ]
    return []
