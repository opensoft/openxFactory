"""Pure immutable authority, trust-anchor, binding, and operation semantics.

The functions in this module deliberately consume plain mappings and a caller-
supplied time.  They perform no I/O and never consult ambient clock, network,
or mutable identity state, so the same contract bytes have the same meaning in
the portable validator and the PostgreSQL conformance lane.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Iterable, Mapping, Sequence

RECORD_DIGEST_PROFILE = "xfactory-canonical-json-v1"
PRINCIPAL_TRANSITIONS = {
    "provisioning": frozenset({"active", "retired"}),
    "active": frozenset({"suspended", "retired"}),
    "suspended": frozenset({"active", "retired"}),
    "retired": frozenset(),
}

_COLLECTION_IDS = {
    "principals": "principal_id",
    "principal_lifecycle_events": "event_id",
    "database_principal_bindings": "binding_id",
    "database_principal_binding_revocations": "revocation_id",
    "trust_anchors": "anchor_id",
    "trust_anchor_events": "event_id",
    "authority_grants": "grant_id",
    "grant_revocations": "revocation_id",
    "cross_layer_bindings": "binding_id",
    "binding_revocations": "revocation_id",
    "operation_authorizations": "operation_id",
}


def _finding(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": "error", "path": path, "message": message}


def _sorted(findings: Iterable[Mapping[str, object]]) -> list[dict[str, str]]:
    return sorted(
        (dict(item) for item in findings),
        key=lambda item: (
            str(item.get("path", "")),
            str(item.get("code", "")),
            str(item.get("message", "")),
        ),
    )


def _json_value(value: object, path: str = "$") -> None:
    if value is None or type(value) in {str, bool, int}:
        return
    if type(value) is float:
        raise ValueError(f"{path}: floating-point values are forbidden")
    if type(value) is list:
        for index, item in enumerate(value):
            _json_value(item, f"{path}[{index}]")
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise ValueError(f"{path}: mapping keys must be strings")
            _json_value(item, f"{path}.{key}")
        return
    raise ValueError(f"{path}: {type(value).__name__} is not a JSON value")


def canonical_record_digest(record: Mapping[str, object]) -> str:
    """Return the frozen ``xfactory-canonical-json-v1`` semantic digest.

    SHA-256 covers UTF-8 compact sorted-key JSON for the complete closed record
    with only that record's top-level ``record_digest`` member omitted.  Nested
    reference digests remain covered.  Floats and non-JSON values fail closed.
    """

    if not isinstance(record, Mapping):
        raise TypeError("record must be a mapping")
    payload = {key: value for key, value in record.items() if key != "record_digest"}
    _json_value(payload)
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _records(
    document: Mapping[str, object], collection: str
) -> list[Mapping[str, object]]:
    value = document.get(collection, []) or []
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _index(
    document: Mapping[str, object], collection: str
) -> dict[str, Mapping[str, object]]:
    id_field = _COLLECTION_IDS[collection]
    result: dict[str, Mapping[str, object]] = {}
    for record in _records(document, collection):
        identifier = record.get(id_field)
        if isinstance(identifier, str):
            result.setdefault(identifier, record)
    return result


def _parse_time(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError:
        return None
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        return None
    return parsed


def _at(document: Mapping[str, object], supplied: str | None) -> datetime | None:
    return _parse_time(
        supplied if supplied is not None else document.get("evaluation_time")
    )


def _scope_key(scope: object) -> tuple[str, str, str, str] | None:
    if not isinstance(scope, Mapping):
        return None
    return (
        str(scope.get("scope_kind", "")),
        str(scope.get("installation_id", "")),
        str(scope.get("stack_id", "")),
        str(scope.get("layer_id", "")),
    )


def _scope_contains(parent: object, child: object) -> bool:
    parent_key = _scope_key(parent)
    child_key = _scope_key(child)
    if parent_key is None or child_key is None or parent_key[1] != child_key[1]:
        return False
    parent_kind, _, parent_stack, parent_layer = parent_key
    child_kind, _, child_stack, child_layer = child_key
    if parent_kind == "installation":
        return child_kind in {"installation", "stack", "layer"}
    if parent_kind == "installation_admin":
        return child_kind == "installation_admin"
    if parent_kind == "stack":
        return child_kind in {"stack", "layer"} and parent_stack == child_stack
    return (
        parent_kind == child_kind == "layer"
        and parent_stack == child_stack
        and parent_layer == child_layer
    )


def _resource_in_scope(resource: object, scope: object) -> bool:
    if not isinstance(resource, Mapping):
        return False
    key = _scope_key(scope)
    if key is None or str(resource.get("installation_id", "")) != key[1]:
        return False
    if key[0] in {"installation", "installation_admin"}:
        return True
    if str(resource.get("stack_id", "")) != key[2]:
        return False
    return key[0] == "stack" or str(resource.get("layer_id", "")) == key[3]


def _same(value_a: object, value_b: object) -> bool:
    return value_a == value_b


def _ref_matches(
    reference: object,
    record: Mapping[str, object] | None,
    id_field: str,
    *,
    installation: bool = False,
) -> bool:
    if not isinstance(reference, Mapping) or record is None:
        return False
    reference_id = reference.get(id_field)
    if reference_id != record.get(id_field):
        return False
    if reference.get("record_digest") != record.get("record_digest"):
        return False
    return not installation or reference.get("installation_id") == record.get(
        "installation_id"
    )


def _principal_ref_matches(
    reference: object, principal: Mapping[str, object] | None
) -> bool:
    if not _ref_matches(reference, principal, "principal_id"):
        return False
    assert isinstance(reference, Mapping)
    return _same(reference.get("scope"), principal.get("scope") if principal else None)


def _record_findings(document: Mapping[str, object]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for collection, id_field in _COLLECTION_IDS.items():
        records = _records(document, collection)
        identifiers = [str(item.get(id_field, "")) for item in records]
        for duplicate, count in Counter(identifiers).items():
            if duplicate and count > 1:
                findings.append(
                    _finding(
                        "HGR-AUTHORITY-DUPLICATE-ID",
                        collection,
                        f"{id_field} {duplicate!r} occurs {count} times",
                    )
                )
        for index, record in enumerate(records):
            path = f"{collection}[{index}]"
            if record.get("record_digest_profile") != RECORD_DIGEST_PROFILE:
                findings.append(
                    _finding(
                        "HGR-AUTHORITY-DIGEST-PROFILE",
                        f"{path}.record_digest_profile",
                        f"{RECORD_DIGEST_PROFILE} is required",
                    )
                )
            try:
                expected = canonical_record_digest(record)
            except (TypeError, ValueError) as error:
                findings.append(
                    _finding("HGR-AUTHORITY-RECORD-DIGEST", path, str(error))
                )
                continue
            if record.get("record_digest") != expected:
                findings.append(
                    _finding(
                        "HGR-AUTHORITY-RECORD-DIGEST",
                        f"{path}.record_digest",
                        "record digest does not match semantic recomputation",
                    )
                )
    return findings


def _principal_events(
    document: Mapping[str, object], principal_id: str
) -> list[Mapping[str, object]]:
    result = []
    for event in _records(document, "principal_lifecycle_events"):
        reference = event.get("principal_ref")
        if (
            isinstance(reference, Mapping)
            and reference.get("principal_id") == principal_id
        ):
            result.append(event)
    return sorted(
        result,
        key=lambda item: (
            str(item.get("occurred_at", "")),
            str(item.get("event_id", "")),
        ),
    )


def _principal_state_at(
    document: Mapping[str, object], principal_id: str, at: datetime
) -> str | None:
    principal = _index(document, "principals").get(principal_id)
    if principal is None:
        return None
    state = str(principal.get("initial_lifecycle_state", "provisioning"))
    for event in _principal_events(document, principal_id):
        occurred = _parse_time(event.get("occurred_at"))
        if occurred is not None and occurred <= at and event.get("from_state") == state:
            state = str(event.get("to_state", ""))
    return state


def validate_active_principal(
    principal_ref: object,
    authority_document: Mapping[str, object],
    *,
    evaluation_time: str,
    path: str = "principal_ref",
) -> list[dict[str, str]]:
    """Require one exact principal reference to be active as-of a fixed time.

    This is the reusable governed-use boundary for operation, approval, and
    supersession semantics.  It intentionally does not use ambient current
    time and does not treat possession of a grant as lifecycle activation.
    """

    at = _parse_time(evaluation_time)
    if at is None:
        return [
            _finding(
                "HGR-PRINCIPAL-EVALUATION-TIME",
                path,
                "fixed RFC 3339 UTC principal evaluation time is required",
            )
        ]
    if not isinstance(principal_ref, Mapping):
        return [
            _finding(
                "HGR-PRINCIPAL-REFERENCE",
                path,
                "principal reference must be a closed mapping",
            )
        ]
    principal_id = str(principal_ref.get("principal_id", ""))
    principal = _index(authority_document, "principals").get(principal_id)
    if not _principal_ref_matches(principal_ref, principal):
        return [
            _finding(
                "HGR-PRINCIPAL-REFERENCE",
                path,
                "principal reference is unknown or not digest-and-scope exact",
            )
        ]
    state = _principal_state_at(authority_document, principal_id, at)
    if state != "active":
        return [
            _finding(
                "HGR-PRINCIPAL-INACTIVE",
                path,
                f"principal {principal_id!r} is {state or 'unknown'} as-of governed use",
            )
        ]
    return []


def _principal_lifecycle_findings(
    document: Mapping[str, object],
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    principals = _index(document, "principals")
    grants = _index(document, "authority_grants")
    for principal_id, principal in principals.items():
        state = str(principal.get("initial_lifecycle_state", ""))
        previous_kind = "registration"
        previous_id = principal_id
        previous_digest = principal.get("record_digest")
        for position, event in enumerate(_principal_events(document, principal_id)):
            path = f"principal_lifecycle_events[{position}]"
            if not _principal_ref_matches(event.get("principal_ref"), principal):
                findings.append(
                    _finding(
                        "HGR-PRINCIPAL-REFERENCE",
                        f"{path}.principal_ref",
                        "principal reference is not exact",
                    )
                )
            predecessor = event.get("predecessor_ref")
            expected = {
                "kind": previous_kind,
                "id": previous_id,
                "record_digest": previous_digest,
            }
            if predecessor != expected:
                findings.append(
                    _finding(
                        "HGR-PRINCIPAL-LIFECYCLE-PREDECESSOR",
                        f"{path}.predecessor_ref",
                        "principal lifecycle events must form one linear append-only chain",
                    )
                )
            from_state = str(event.get("from_state", ""))
            to_state = str(event.get("to_state", ""))
            if from_state != state or to_state not in PRINCIPAL_TRANSITIONS.get(
                state, frozenset()
            ):
                findings.append(
                    _finding(
                        "HGR-PRINCIPAL-LIFECYCLE-TRANSITION",
                        path,
                        f"transition {from_state!r} -> {to_state!r} is not valid from {state!r}",
                    )
                )
            else:
                state = to_state
            occurred = _parse_time(event.get("occurred_at"))
            grant_ref = event.get("authorizing_grant_ref")
            grant_id = (
                str(grant_ref.get("grant_id", ""))
                if isinstance(grant_ref, Mapping)
                else ""
            )
            grant = grants.get(grant_id)
            grant_ok, _ = _grant_status(
                document,
                grant_id,
                occurred or datetime.min.replace(tzinfo=timezone.utc),
            )
            if not (
                grant_ok
                and grant is not None
                and grant.get("action") == "transition_lifecycle"
                and _ref_matches(grant_ref, grant, "grant_id", installation=True)
                and _scope_contains(grant.get("scope"), principal.get("scope"))
            ):
                findings.append(
                    _finding(
                        "HGR-PRINCIPAL-LIFECYCLE-AUTHORITY",
                        f"{path}.authorizing_grant_ref",
                        "exact active transition_lifecycle authority is required",
                    )
                )
            previous_kind = "event"
            previous_id = str(event.get("event_id", ""))
            previous_digest = event.get("record_digest")
    for position, event in enumerate(_records(document, "principal_lifecycle_events")):
        reference = event.get("principal_ref")
        principal_id = (
            reference.get("principal_id") if isinstance(reference, Mapping) else None
        )
        if principal_id not in principals:
            findings.append(
                _finding(
                    "HGR-PRINCIPAL-REFERENCE",
                    f"principal_lifecycle_events[{position}].principal_ref",
                    "lifecycle event refers to an unknown principal",
                )
            )
    return findings


def _active_anchor_id(
    document: Mapping[str, object], at: datetime, *, stop_before: str | None = None
) -> str | None:
    anchors = _records(document, "trust_anchors")
    genesis = [item for item in anchors if item.get("anchor_kind") == "genesis"]
    if len(genesis) != 1:
        return None
    effective = _parse_time(genesis[0].get("effective_at"))
    active = (
        str(genesis[0].get("anchor_id"))
        if effective is not None and effective <= at
        else None
    )
    for event in sorted(
        _records(document, "trust_anchor_events"),
        key=lambda item: (
            str(item.get("effective_at", "")),
            str(item.get("event_id", "")),
        ),
    ):
        if event.get("event_id") == stop_before:
            break
        event_time = _parse_time(event.get("effective_at"))
        if event_time is None or event_time > at:
            continue
        predecessor = event.get("predecessor_anchor_ref")
        if (
            not isinstance(predecessor, Mapping)
            or predecessor.get("anchor_id") != active
        ):
            continue
        if event.get("event_type") == "rotate":
            successor = event.get("successor_anchor_ref")
            active = (
                str(successor.get("anchor_id"))
                if isinstance(successor, Mapping)
                else None
            )
        elif event.get("event_type") == "revoke":
            active = None
    return active


def _grant_status(
    document: Mapping[str, object],
    grant_id: str,
    at: datetime,
    *,
    stack: tuple[str, ...] = (),
    anchor_override: str | None = None,
    authorized_revocations: set[str] | None = None,
) -> tuple[bool, str | None]:
    grants = _index(document, "authority_grants")
    grant = grants.get(grant_id)
    if grant is None:
        return False, "HGR-GRANT-REFERENCE"
    if grant_id in stack:
        return False, (
            "HGR-GRANT-SELF-ISSUED"
            if stack and stack[-1] == grant_id
            else "HGR-GRANT-CYCLE"
        )
    starts = _parse_time(grant.get("starts_at"))
    expires = (
        _parse_time(grant.get("expires_at"))
        if grant.get("expires_at") is not None
        else None
    )
    if starts is None or at < starts or (expires is not None and at >= expires):
        return False, "HGR-GRANT-TIME"
    if authorized_revocations is None:
        authorized_revocations = _authorized_grant_revocation_ids(document, at)
    for revocation in _records(document, "grant_revocations"):
        reference = revocation.get("grant_ref")
        effective = _parse_time(revocation.get("effective_at"))
        if (
            str(revocation.get("revocation_id", "")) in authorized_revocations
            and isinstance(reference, Mapping)
            and reference.get("grant_id") == grant_id
            and effective is not None
            and effective <= at
        ):
            return False, "HGR-GRANT-REVOKED"
    if grant.get("grant_kind") == "root":
        root_reference = grant.get("root_anchor_ref")
        root_id = (
            root_reference.get("anchor_id")
            if isinstance(root_reference, Mapping)
            else None
        )
        root_anchor = _index(document, "trust_anchors").get(str(root_id))
        if not _ref_matches(
            root_reference, root_anchor, "anchor_id", installation=True
        ):
            return False, "HGR-GRANT-ANCHOR"
        expected_anchor = (
            anchor_override
            if anchor_override is not None
            else _active_anchor_id(document, at)
        )
        if root_id != expected_anchor:
            return False, "HGR-GRANT-ANCHOR"
        root_scope = _scope_key(grant.get("scope"))
        if root_scope is None or root_scope[0] != "installation":
            return False, "HGR-GRANT-ROOT-SCOPE"
        return True, None
    issuer_ref = grant.get("issuer_grant_ref")
    if not isinstance(issuer_ref, Mapping):
        return False, "HGR-GRANT-REFERENCE"
    issuer_id = str(issuer_ref.get("grant_id", ""))
    if issuer_id == grant_id:
        return False, "HGR-GRANT-SELF-ISSUED"
    issuer = grants.get(issuer_id)
    if not _ref_matches(issuer_ref, issuer, "grant_id", installation=True):
        return False, "HGR-GRANT-REFERENCE"
    issuer_ok, issuer_code = _grant_status(
        document,
        issuer_id,
        at,
        stack=stack + (grant_id,),
        anchor_override=anchor_override,
        authorized_revocations=authorized_revocations,
    )
    if not issuer_ok:
        return False, issuer_code
    if issuer is None or issuer.get("action") != "issue_grant":
        return False, "HGR-GRANT-ISSUER-ACTION"
    if not _scope_contains(issuer.get("scope"), grant.get("scope")):
        return False, "HGR-GRANT-SCOPE-WIDENING"
    return True, None


def _authorized_grant_revocation_ids(
    document: Mapping[str, object], at: datetime
) -> set[str]:
    authorized: set[str] = set()
    grants = _index(document, "authority_grants")
    principals = _index(document, "principals")
    for revocation in sorted(
        _records(document, "grant_revocations"),
        key=lambda item: (
            str(item.get("effective_at", "")),
            str(item.get("revocation_id", "")),
        ),
    ):
        effective = _parse_time(revocation.get("effective_at"))
        if effective is None or effective > at:
            continue
        issuer_ref = revocation.get("issuer_grant_ref")
        issuer_id = (
            str(issuer_ref.get("grant_id", ""))
            if isinstance(issuer_ref, Mapping)
            else ""
        )
        issuer = grants.get(issuer_id)
        target_ref = revocation.get("grant_ref")
        target_id = (
            str(target_ref.get("grant_id", ""))
            if isinstance(target_ref, Mapping)
            else ""
        )
        target = grants.get(target_id)
        principal_ref = revocation.get("issuer_principal_ref")
        principal_id = (
            principal_ref.get("principal_id")
            if isinstance(principal_ref, Mapping)
            else None
        )
        valid, _ = _grant_status(
            document,
            issuer_id,
            effective,
            authorized_revocations=set(authorized),
        )
        if (
            valid
            and issuer is not None
            and issuer.get("action") == "revoke_grant"
            and issuer.get("grant_kind") == "root"
            and _ref_matches(issuer_ref, issuer, "grant_id", installation=True)
            and _ref_matches(target_ref, target, "grant_id", installation=True)
            and _principal_ref_matches(principal_ref, principals.get(str(principal_id)))
            and _same(issuer.get("principal_ref"), principal_ref)
        ):
            authorized.add(str(revocation.get("revocation_id", "")))
    return authorized


def _anchor_findings(document: Mapping[str, object]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    anchors = _index(document, "trust_anchors")
    genesis = [
        item for item in anchors.values() if item.get("anchor_kind") == "genesis"
    ]
    if len(genesis) != 1:
        findings.append(
            _finding(
                "HGR-ANCHOR-GENESIS-CARDINALITY",
                "trust_anchors",
                "exactly one immutable genesis anchor is required",
            )
        )
        return findings
    active = str(genesis[0].get("anchor_id"))
    previous_kind = "registration"
    previous_id = active
    previous_digest = genesis[0].get("record_digest")
    principals = _index(document, "principals")
    grants = _index(document, "authority_grants")
    for position, event in enumerate(
        sorted(
            _records(document, "trust_anchor_events"),
            key=lambda item: (
                str(item.get("effective_at", "")),
                str(item.get("event_id", "")),
            ),
        )
    ):
        path = f"trust_anchor_events[{position}]"
        expected_predecessor = {
            "kind": previous_kind,
            "id": previous_id,
            "record_digest": previous_digest,
        }
        if event.get("predecessor_ref") != expected_predecessor:
            findings.append(
                _finding(
                    "HGR-ANCHOR-CHAIN",
                    f"{path}.predecessor_ref",
                    "anchor events must form one linear append-only chain",
                )
            )
        predecessor_ref = event.get("predecessor_anchor_ref")
        predecessor = (
            anchors.get(str(predecessor_ref.get("anchor_id", "")))
            if isinstance(predecessor_ref, Mapping)
            else None
        )
        if active is None or not _ref_matches(predecessor_ref, predecessor, "anchor_id", installation=True) or predecessor_ref.get("anchor_id") != active:  # type: ignore[union-attr]
            findings.append(
                _finding(
                    "HGR-ANCHOR-CHAIN",
                    f"{path}.predecessor_anchor_ref",
                    "event must consume the one active predecessor anchor",
                )
            )
        effective = _parse_time(event.get("effective_at"))
        grant_ref = event.get("authorizing_grant_ref")
        grant_id = (
            str(grant_ref.get("grant_id", "")) if isinstance(grant_ref, Mapping) else ""
        )
        grant = grants.get(grant_id)
        principal_ref = event.get("authorizing_principal_ref")
        principal_id = (
            principal_ref.get("principal_id")
            if isinstance(principal_ref, Mapping)
            else None
        )
        expected_action = (
            "rotate_trust_anchor"
            if event.get("event_type") == "rotate"
            else "revoke_trust_anchor"
        )
        grant_ok, _ = _grant_status(
            document,
            grant_id,
            effective or datetime.min.replace(tzinfo=timezone.utc),
            anchor_override=active,
            authorized_revocations=(
                _authorized_grant_revocation_ids(document, effective)
                if effective is not None
                else set()
            ),
        )
        if not (
            grant_ok
            and grant is not None
            and grant.get("grant_kind") == "root"
            and grant.get("action") == expected_action
            and _ref_matches(grant_ref, grant, "grant_id", installation=True)
            and _principal_ref_matches(principal_ref, principals.get(str(principal_id)))
            and _same(grant.get("principal_ref"), principal_ref)
        ):
            findings.append(
                _finding(
                    "HGR-ANCHOR-AUTHORITY",
                    f"{path}.authorizing_grant_ref",
                    f"current-root {expected_action} authority is required",
                )
            )
        if event.get("event_type") == "rotate":
            successor_ref = event.get("successor_anchor_ref")
            successor = (
                anchors.get(str(successor_ref.get("anchor_id", "")))
                if isinstance(successor_ref, Mapping)
                else None
            )
            if (
                not _ref_matches(
                    successor_ref, successor, "anchor_id", installation=True
                )
                or successor is None
                or successor.get("anchor_kind") != "rotated"
            ):
                findings.append(
                    _finding(
                        "HGR-ANCHOR-CHAIN",
                        f"{path}.successor_anchor_ref",
                        "rotation successor must be an exact immutable rotated anchor",
                    )
                )
            else:
                active = str(successor.get("anchor_id"))
        elif event.get("event_type") == "revoke":
            active = None
        previous_kind = "event"
        previous_id = str(event.get("event_id", ""))
        previous_digest = event.get("record_digest")
    return findings


def _grant_findings(document: Mapping[str, object]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    principals = _index(document, "principals")
    anchors = _index(document, "trust_anchors")
    grants = _index(document, "authority_grants")
    for position, grant in enumerate(_records(document, "authority_grants")):
        path = f"authority_grants[{position}]"
        principal_ref = grant.get("principal_ref")
        principal_id = (
            principal_ref.get("principal_id")
            if isinstance(principal_ref, Mapping)
            else None
        )
        if not _principal_ref_matches(principal_ref, principals.get(str(principal_id))):
            findings.append(
                _finding(
                    "HGR-GRANT-PRINCIPAL",
                    f"{path}.principal_ref",
                    "grant principal reference is not exact",
                )
            )
        issued = _parse_time(grant.get("issued_at"))
        if issued is None:
            findings.append(
                _finding(
                    "HGR-GRANT-TIME", f"{path}.issued_at", "valid issued_at is required"
                )
            )
            continue
        if grant.get("grant_kind") == "root":
            anchor_ref = grant.get("root_anchor_ref")
            anchor = (
                anchors.get(str(anchor_ref.get("anchor_id", "")))
                if isinstance(anchor_ref, Mapping)
                else None
            )
            if not _ref_matches(anchor_ref, anchor, "anchor_id", installation=True):
                findings.append(
                    _finding(
                        "HGR-GRANT-ANCHOR",
                        f"{path}.root_anchor_ref",
                        "root anchor reference is not exact",
                    )
                )
        valid, code = _grant_status(
            document,
            str(grant.get("grant_id", "")),
            issued,
            authorized_revocations=set(),
        )
        if not valid:
            findings.append(
                _finding(
                    code or "HGR-GRANT-INVALID",
                    path,
                    "grant chain is not valid at issuance",
                )
            )
        if not _resource_in_scope(grant.get("resource_constraint"), grant.get("scope")):
            findings.append(
                _finding(
                    "HGR-GRANT-RESOURCE",
                    f"{path}.resource_constraint",
                    "resource constraint escapes grant scope",
                )
            )
    evaluation = _at(document, None)
    if evaluation is not None:
        valid_revocations = _authorized_grant_revocation_ids(document, evaluation)
        for position, revocation in enumerate(_records(document, "grant_revocations")):
            if str(revocation.get("revocation_id", "")) not in valid_revocations:
                findings.append(
                    _finding(
                        "HGR-REVOCATION-AUTHORITY",
                        f"grant_revocations[{position}]",
                        "grant revocation requires exact current-root revoke_grant authority",
                    )
                )
    return findings


def _resource_known_draft(document: Mapping[str, object], reference: object) -> bool:
    if not isinstance(reference, Mapping):
        return False
    for resource in document.get("resources", []) or []:
        if not isinstance(resource, Mapping):
            continue
        candidate = resource.get("resource_ref")
        if (
            candidate == reference
            and resource.get("immutable") is True
            and resource.get("lifecycle_state") == "draft"
        ):
            return True
    return False


def _binding_revocation_ids(document: Mapping[str, object], at: datetime) -> set[str]:
    valid: set[str] = set()
    bindings = _index(document, "cross_layer_bindings")
    grants = _index(document, "authority_grants")
    principals = _index(document, "principals")
    grant_revocations = _authorized_grant_revocation_ids(document, at)
    for revocation in _records(document, "binding_revocations"):
        effective = _parse_time(revocation.get("effective_at"))
        if effective is None or effective > at:
            continue
        binding_ref = revocation.get("binding_ref")
        binding_id = (
            str(binding_ref.get("binding_id", ""))
            if isinstance(binding_ref, Mapping)
            else ""
        )
        binding = bindings.get(binding_id)
        source_grant_ref = revocation.get("source_grant_ref")
        source_grant_id = (
            str(source_grant_ref.get("grant_id", ""))
            if isinstance(source_grant_ref, Mapping)
            else ""
        )
        source_grant = grants.get(source_grant_id)
        target_grant_ref = revocation.get("target_acceptance_grant_ref")
        target_grant_id = (
            str(target_grant_ref.get("grant_id", ""))
            if isinstance(target_grant_ref, Mapping)
            else ""
        )
        target_grant = grants.get(target_grant_id)
        source_ok, _ = _grant_status(
            document,
            source_grant_id,
            effective,
            authorized_revocations=grant_revocations,
        )
        target_ok, _ = _grant_status(
            document,
            target_grant_id,
            effective,
            authorized_revocations=grant_revocations,
        )
        source_principal_ref = revocation.get("source_principal_ref")
        target_principal_ref = revocation.get("target_acceptance_principal_ref")
        source_pid = (
            source_principal_ref.get("principal_id")
            if isinstance(source_principal_ref, Mapping)
            else None
        )
        target_pid = (
            target_principal_ref.get("principal_id")
            if isinstance(target_principal_ref, Mapping)
            else None
        )
        if (
            _ref_matches(binding_ref, binding, "binding_id")
            and source_ok
            and source_grant is not None
            and source_grant.get("action") == "revoke_binding"
            and _ref_matches(
                source_grant_ref, source_grant, "grant_id", installation=True
            )
            and _principal_ref_matches(
                source_principal_ref, principals.get(str(source_pid))
            )
            and _same(source_grant.get("principal_ref"), source_principal_ref)
            and binding is not None
            and _same(source_grant.get("scope"), binding.get("source_scope"))
            and _same(
                source_grant.get("resource_constraint"), binding.get("source_resource")
            )
            and target_ok
            and target_grant is not None
            and target_grant.get("action") == "accept_cross_layer"
            and _ref_matches(
                target_grant_ref, target_grant, "grant_id", installation=True
            )
            and _principal_ref_matches(
                target_principal_ref, principals.get(str(target_pid))
            )
            and _same(target_grant.get("principal_ref"), target_principal_ref)
            and _same(target_grant.get("scope"), binding.get("target_scope"))
            and _same(
                target_grant.get("resource_constraint"), binding.get("target_resource")
            )
        ):
            valid.add(str(revocation.get("revocation_id", "")))
    return valid


def _binding_status(
    document: Mapping[str, object], binding_id: str, at: datetime
) -> tuple[bool, str | None]:
    binding = _index(document, "cross_layer_bindings").get(binding_id)
    if binding is None:
        return False, "HGR-BINDING-REFERENCE"
    starts = _parse_time(binding.get("starts_at"))
    expires = (
        _parse_time(binding.get("expires_at"))
        if binding.get("expires_at") is not None
        else None
    )
    if starts is None or at < starts or (expires is not None and at >= expires):
        return False, "HGR-BINDING-TIME"
    valid_revocations = _binding_revocation_ids(document, at)
    for revocation in _records(document, "binding_revocations"):
        reference = revocation.get("binding_ref")
        effective = _parse_time(revocation.get("effective_at"))
        if (
            str(revocation.get("revocation_id", "")) in valid_revocations
            and isinstance(reference, Mapping)
            and reference.get("binding_id") == binding_id
            and effective is not None
            and effective <= at
        ):
            return False, "HGR-BINDING-REVOKED"
    return True, None


def _binding_findings(
    document: Mapping[str, object], *, binding_id: str | None = None
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    grants = _index(document, "authority_grants")
    principals = _index(document, "principals")
    for position, binding in enumerate(_records(document, "cross_layer_bindings")):
        if binding_id is not None and binding.get("binding_id") != binding_id:
            continue
        path = f"cross_layer_bindings[{position}]"
        source_scope = binding.get("source_scope")
        target_scope = binding.get("target_scope")
        source_key = _scope_key(source_scope)
        target_key = _scope_key(target_scope)
        if (
            source_key is None
            or target_key is None
            or source_key[:3] != target_key[:3]
            or source_key[3] == target_key[3]
        ):
            findings.append(
                _finding(
                    "HGR-BINDING-DIRECTION",
                    path,
                    "binding must connect two distinct layers in one exact stack",
                )
            )
        if not _resource_in_scope(
            binding.get("source_resource"), source_scope
        ) or not _resource_in_scope(binding.get("target_resource"), target_scope):
            findings.append(
                _finding(
                    "HGR-BINDING-RESOURCE",
                    path,
                    "source and target resources must exactly belong to their declared layers",
                )
            )
        if not _resource_known_draft(document, binding.get("target_resource")):
            findings.append(
                _finding(
                    "HGR-BINDING-TARGET-UNKNOWN",
                    f"{path}.target_resource",
                    "target must be a pre-existing immutable draft ID and digest",
                )
            )
        created = _parse_time(binding.get("created_at"))
        if created is None:
            findings.append(
                _finding(
                    "HGR-BINDING-TIME",
                    f"{path}.created_at",
                    "valid created_at is required",
                )
            )
            continue
        created_at = str(binding.get("created_at", ""))
        findings.extend(
            validate_active_principal(
                binding.get("creator_principal_ref"),
                document,
                evaluation_time=created_at,
                path=f"{path}.creator_principal_ref",
            )
        )
        findings.extend(
            validate_active_principal(
                binding.get("target_acceptance_principal_ref"),
                document,
                evaluation_time=created_at,
                path=f"{path}.target_acceptance_principal_ref",
            )
        )
        grant_revocations = _authorized_grant_revocation_ids(document, created)
        creator_ref = binding.get("creator_grant_ref")
        creator_id = (
            str(creator_ref.get("grant_id", ""))
            if isinstance(creator_ref, Mapping)
            else ""
        )
        creator = grants.get(creator_id)
        creator_ok, _ = _grant_status(
            document, creator_id, created, authorized_revocations=grant_revocations
        )
        creator_principal_ref = binding.get("creator_principal_ref")
        creator_pid = (
            creator_principal_ref.get("principal_id")
            if isinstance(creator_principal_ref, Mapping)
            else None
        )
        if not (
            creator_ok
            and creator is not None
            and creator.get("action") == "create_binding"
            and _ref_matches(creator_ref, creator, "grant_id", installation=True)
            and _principal_ref_matches(
                creator_principal_ref, principals.get(str(creator_pid))
            )
            and _same(creator.get("principal_ref"), creator_principal_ref)
            and _same(creator.get("scope"), source_scope)
            and _same(
                creator.get("resource_constraint"), binding.get("source_resource")
            )
        ):
            findings.append(
                _finding(
                    "HGR-BINDING-AUTHORITY",
                    f"{path}.creator_grant_ref",
                    "exact active source create_binding authority is required",
                )
            )
        accept_ref = binding.get("target_acceptance_grant_ref")
        accept_id = (
            str(accept_ref.get("grant_id", ""))
            if isinstance(accept_ref, Mapping)
            else ""
        )
        accept = grants.get(accept_id)
        accept_ok, _ = _grant_status(
            document, accept_id, created, authorized_revocations=grant_revocations
        )
        accept_principal_ref = binding.get("target_acceptance_principal_ref")
        accept_pid = (
            accept_principal_ref.get("principal_id")
            if isinstance(accept_principal_ref, Mapping)
            else None
        )
        if not (
            accept_ok
            and accept is not None
            and accept.get("action") == "accept_cross_layer"
            and _ref_matches(accept_ref, accept, "grant_id", installation=True)
            and _principal_ref_matches(
                accept_principal_ref, principals.get(str(accept_pid))
            )
            and _same(accept.get("principal_ref"), accept_principal_ref)
            and _same(accept.get("scope"), target_scope)
            and _same(accept.get("resource_constraint"), binding.get("target_resource"))
        ):
            findings.append(
                _finding(
                    "HGR-BINDING-TARGET-ACCEPTANCE",
                    f"{path}.target_acceptance_grant_ref",
                    "exact active target acceptance is required",
                )
            )
    evaluation = _at(document, None)
    if evaluation is not None:
        valid_revocations = _binding_revocation_ids(document, evaluation)
        for position, revocation in enumerate(
            _records(document, "binding_revocations")
        ):
            reference = revocation.get("binding_ref")
            if binding_id is not None and (
                not isinstance(reference, Mapping)
                or reference.get("binding_id") != binding_id
            ):
                continue
            if str(revocation.get("revocation_id", "")) not in valid_revocations:
                findings.append(
                    _finding(
                        "HGR-BINDING-REVOCATION-AUTHORITY",
                        f"binding_revocations[{position}]",
                        "binding revocation requires exact source revoke_binding and target acceptance",
                    )
                )
    return findings


def _authorized_database_revocation_ids(
    document: Mapping[str, object], at: datetime
) -> set[str]:
    authorized: set[str] = set()
    bindings = _index(document, "database_principal_bindings")
    grants = _index(document, "authority_grants")
    principals = _index(document, "principals")
    grant_revocations = _authorized_grant_revocation_ids(document, at)
    for revocation in _records(document, "database_principal_binding_revocations"):
        effective = _parse_time(revocation.get("effective_at"))
        if effective is None or effective > at:
            continue
        binding_ref = revocation.get("binding_ref")
        binding_id = (
            str(binding_ref.get("binding_id", ""))
            if isinstance(binding_ref, Mapping)
            else ""
        )
        binding = bindings.get(binding_id)
        issuer_ref = revocation.get("issuer_grant_ref")
        issuer_id = (
            str(issuer_ref.get("grant_id", ""))
            if isinstance(issuer_ref, Mapping)
            else ""
        )
        issuer = grants.get(issuer_id)
        principal_ref = revocation.get("issuer_principal_ref")
        principal_id = (
            str(principal_ref.get("principal_id", ""))
            if isinstance(principal_ref, Mapping)
            else ""
        )
        issuer_ok, _ = _grant_status(
            document,
            issuer_id,
            effective,
            authorized_revocations=grant_revocations,
        )
        if (
            _ref_matches(binding_ref, binding, "binding_id")
            and isinstance(binding_ref, Mapping)
            and binding is not None
            and isinstance(binding.get("scope"), Mapping)
            and binding_ref.get("installation_id")
            == binding.get("scope", {}).get("installation_id")
            and issuer_ok
            and issuer is not None
            and issuer.get("action") == "revoke_grant"
            and issuer.get("grant_kind") == "root"
            and _ref_matches(issuer_ref, issuer, "grant_id", installation=True)
            and _principal_ref_matches(principal_ref, principals.get(principal_id))
            and _same(issuer.get("principal_ref"), principal_ref)
            and _same(revocation.get("scope"), binding.get("scope"))
            and _scope_contains(issuer.get("scope"), binding.get("scope"))
        ):
            authorized.add(str(revocation.get("revocation_id", "")))
    return authorized


def _database_binding_findings(
    document: Mapping[str, object], at: datetime
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    principals = _index(document, "principals")
    grants = _index(document, "authority_grants")
    revocations = _records(document, "database_principal_binding_revocations")
    valid_revocations = _authorized_database_revocation_ids(document, at)
    active_users: defaultdict[str, list[str]] = defaultdict(list)
    grant_revocations = _authorized_grant_revocation_ids(document, at)
    for position, binding in enumerate(
        _records(document, "database_principal_bindings")
    ):
        path = f"database_principal_bindings[{position}]"
        principal_ref = binding.get("principal_ref")
        principal_id = (
            str(principal_ref.get("principal_id", ""))
            if isinstance(principal_ref, Mapping)
            else ""
        )
        principal = principals.get(principal_id)
        grant_ref = binding.get("creator_grant_ref")
        grant_id = (
            str(grant_ref.get("grant_id", "")) if isinstance(grant_ref, Mapping) else ""
        )
        grant = grants.get(grant_id)
        grant_ok, _ = _grant_status(
            document, grant_id, at, authorized_revocations=grant_revocations
        )
        if not (
            _principal_ref_matches(principal_ref, principal)
            and grant_ok
            and grant is not None
            and grant.get("action") == "assume_scope"
            and _ref_matches(grant_ref, grant, "grant_id", installation=True)
            and _same(grant.get("principal_ref"), principal_ref)
            and _same(grant.get("scope"), binding.get("scope"))
        ):
            findings.append(
                _finding(
                    "HGR-DATABASE-BINDING-AUTHORITY",
                    path,
                    "database binding requires exact principal assume_scope authority",
                )
            )
        revoked = False
        for revocation in revocations:
            reference = revocation.get("binding_ref")
            effective = _parse_time(revocation.get("effective_at"))
            if (
                str(revocation.get("revocation_id", "")) in valid_revocations
                and isinstance(reference, Mapping)
                and reference.get("binding_id") == binding.get("binding_id")
                and effective is not None
                and effective <= at
            ):
                revoked = True
        bound = _parse_time(binding.get("bound_at"))
        if bound is not None and bound <= at and not revoked:
            active_users[str(binding.get("session_user", ""))].append(
                str(binding.get("binding_id", ""))
            )
            if _principal_state_at(document, principal_id, at) != "active":
                findings.append(
                    _finding(
                        "HGR-PRINCIPAL-INACTIVE",
                        f"{path}.principal_ref",
                        "database principal must be active as-of evaluation time",
                    )
                )
    for session_user, bindings in active_users.items():
        if session_user and len(bindings) > 1:
            findings.append(
                _finding(
                    "HGR-DATABASE-SESSION-USER-CONFLICT",
                    "database_principal_bindings",
                    f"session_user {session_user!r} has multiple active bindings",
                )
            )
    for position, revocation in enumerate(revocations):
        if str(revocation.get("revocation_id", "")) not in valid_revocations:
            findings.append(
                _finding(
                    "HGR-DATABASE-BINDING-REVOCATION-AUTHORITY",
                    f"database_principal_binding_revocations[{position}]",
                    "database binding revocation requires exact current-root revoke_grant authority",
                )
            )
    return findings


def validate_grant_authority(
    grant_id: str,
    authority_document: Mapping[str, object],
    *,
    evaluation_time: str,
) -> list[dict[str, str]]:
    """Validate that one exact grant is active as-of a caller-fixed time."""

    at = _parse_time(evaluation_time)
    if at is None:
        return [
            _finding(
                "HGR-GRANT-TIME",
                "evaluation_time",
                "fixed RFC 3339 UTC time is required",
            )
        ]
    anchor_findings = _anchor_findings(authority_document)
    if anchor_findings:
        return _sorted(anchor_findings)
    grant = _index(authority_document, "authority_grants").get(grant_id)
    if grant is None:
        return [
            _finding("HGR-GRANT-REFERENCE", "grant_id", f"unknown grant {grant_id!r}")
        ]
    principal_ref = grant.get("principal_ref")
    principal_id = (
        str(principal_ref.get("principal_id", ""))
        if isinstance(principal_ref, Mapping)
        else ""
    )
    if not _principal_ref_matches(
        principal_ref, _index(authority_document, "principals").get(principal_id)
    ):
        return [
            _finding(
                "HGR-GRANT-PRINCIPAL",
                "principal_ref",
                "grant principal reference is not exact",
            )
        ]
    if not _resource_in_scope(grant.get("resource_constraint"), grant.get("scope")):
        return [
            _finding(
                "HGR-GRANT-RESOURCE",
                "resource_constraint",
                "grant resource escapes its scope",
            )
        ]
    valid, code = _grant_status(authority_document, grant_id, at)
    if valid:
        return []
    return [
        _finding(
            code or "HGR-GRANT-INVALID", "grant_id", f"grant {grant_id!r} is not active"
        )
    ]


def validate_database_principal_binding(
    session_user: str,
    requested_scope: Mapping[str, object],
    authority_document: Mapping[str, object],
    *,
    evaluation_time: str,
) -> list[dict[str, str]]:
    """Resolve an authenticated ``session_user`` to one active exact scope."""

    at = _parse_time(evaluation_time)
    if at is None:
        return [
            _finding(
                "HGR-DATABASE-BINDING-TIME",
                "evaluation_time",
                "fixed RFC 3339 UTC time is required",
            )
        ]
    anchor_findings = _anchor_findings(authority_document)
    if anchor_findings:
        return _sorted(anchor_findings)
    candidates = [
        binding
        for binding in _records(authority_document, "database_principal_bindings")
        if binding.get("session_user") == session_user
        and binding.get("scope") == requested_scope
    ]
    valid_revocation_ids = _authorized_database_revocation_ids(authority_document, at)
    revoked_ids: set[str] = set()
    for revocation in _records(
        authority_document, "database_principal_binding_revocations"
    ):
        reference = revocation.get("binding_ref")
        effective = _parse_time(revocation.get("effective_at"))
        if (
            str(revocation.get("revocation_id", "")) in valid_revocation_ids
            and isinstance(reference, Mapping)
            and effective is not None
            and effective <= at
        ):
            revoked_ids.add(str(reference.get("binding_id", "")))
    active = [
        binding
        for binding in candidates
        if str(binding.get("binding_id", "")) not in revoked_ids
        and (
            _parse_time(binding.get("bound_at"))
            or datetime.max.replace(tzinfo=timezone.utc)
        )
        <= at
    ]
    if len(active) > 1:
        return [
            _finding(
                "HGR-DATABASE-SESSION-USER-CONFLICT",
                "session_user",
                "multiple active bindings resolve the same authenticated user and scope",
            )
        ]
    if not active:
        candidate_ids = {str(binding.get("binding_id", "")) for binding in candidates}
        code = (
            "HGR-DATABASE-BINDING-REVOKED"
            if candidate_ids & revoked_ids
            else "HGR-DATABASE-BINDING-INACTIVE"
        )
        return [
            _finding(
                code,
                "session_user",
                "no active exact database principal binding authorizes the requested scope",
            )
        ]
    binding = active[0]
    principal_ref = binding.get("principal_ref")
    principal_id = (
        str(principal_ref.get("principal_id", ""))
        if isinstance(principal_ref, Mapping)
        else ""
    )
    if _principal_state_at(authority_document, principal_id, at) != "active":
        return [
            _finding(
                "HGR-PRINCIPAL-INACTIVE",
                "principal_ref",
                "bound principal is not active",
            )
        ]
    grant_ref = binding.get("creator_grant_ref")
    grant_id = (
        str(grant_ref.get("grant_id", "")) if isinstance(grant_ref, Mapping) else ""
    )
    grant_findings = validate_grant_authority(
        grant_id, authority_document, evaluation_time=evaluation_time
    )
    if grant_findings:
        return grant_findings
    grant = _index(authority_document, "authority_grants").get(grant_id)
    if (
        grant is None
        or grant.get("action") != "assume_scope"
        or grant.get("scope") != requested_scope
    ):
        return [
            _finding(
                "HGR-DATABASE-BINDING-AUTHORITY",
                "creator_grant_ref",
                "exact assume_scope authority is required",
            )
        ]
    return []


def validate_operation_authorization(
    operation: Mapping[str, object],
    authority_document: Mapping[str, object],
    *,
    evaluation_time: str | None = None,
) -> list[dict[str, str]]:
    """Validate one operation against exact immutable authority as-of its time."""

    findings: list[dict[str, str]] = []
    at = _parse_time(
        evaluation_time
        if evaluation_time is not None
        else operation.get("authorized_at")
    )
    if at is None:
        return [
            _finding(
                "HGR-OPERATION-TIME",
                "authorized_at",
                "fixed RFC 3339 UTC authorization time is required",
            )
        ]
    bindings = _index(authority_document, "cross_layer_bindings")
    binding_ref = operation.get("binding_ref")
    binding_id = (
        str(binding_ref.get("binding_id", ""))
        if isinstance(binding_ref, Mapping)
        else ""
    )
    binding = bindings.get(binding_id)
    if not _ref_matches(binding_ref, binding, "binding_id"):
        return [
            _finding(
                "HGR-BINDING-REFERENCE",
                "binding_ref",
                "operation binding reference is not exact",
            )
        ]
    binding_ok, binding_code = _binding_status(authority_document, binding_id, at)
    if not binding_ok:
        findings.append(
            _finding(
                binding_code or "HGR-BINDING-INVALID",
                "binding_ref",
                "binding is not active at authorization time",
            )
        )
    assert binding is not None
    findings.extend(_binding_findings(authority_document, binding_id=binding_id))
    as_of = (
        evaluation_time
        if evaluation_time is not None
        else str(operation.get("authorized_at", ""))
    )
    findings.extend(
        validate_active_principal(
            operation.get("actor_principal_ref"),
            authority_document,
            evaluation_time=as_of,
            path="actor_principal_ref",
        )
    )
    findings.extend(
        validate_active_principal(
            binding.get("creator_principal_ref"),
            authority_document,
            evaluation_time=as_of,
            path="binding_ref.creator_principal_ref",
        )
    )
    findings.extend(
        validate_active_principal(
            binding.get("target_acceptance_principal_ref"),
            authority_document,
            evaluation_time=as_of,
            path="binding_ref.target_acceptance_principal_ref",
        )
    )
    exact_fields = (
        "source_scope",
        "target_scope",
        "source_resource",
        "target_resource",
        "action",
        "purpose",
    )
    if any(operation.get(field) != binding.get(field) for field in exact_fields):
        findings.append(
            _finding(
                "HGR-OPERATION-BINDING-MISMATCH",
                "binding_ref",
                "operation must exactly repeat binding direction, resources, action, and purpose",
            )
        )
    if operation.get("target_result") != binding.get("target_resource"):
        findings.append(
            _finding(
                "HGR-OPERATION-EVIDENCE-DRIFT",
                "target_result",
                "operation result must be the exact pre-accepted target ID and digest",
            )
        )
    grants = _index(authority_document, "authority_grants")
    principals = _index(authority_document, "principals")
    grant_revocations = _authorized_grant_revocation_ids(authority_document, at)
    source_ref = operation.get("source_grant_ref")
    source_id = (
        str(source_ref.get("grant_id", "")) if isinstance(source_ref, Mapping) else ""
    )
    source = grants.get(source_id)
    source_ok, _ = _grant_status(
        authority_document, source_id, at, authorized_revocations=grant_revocations
    )
    actor_ref = operation.get("actor_principal_ref")
    actor_id = (
        str(actor_ref.get("principal_id", "")) if isinstance(actor_ref, Mapping) else ""
    )
    if not (
        source_ok
        and source is not None
        and source.get("action") == operation.get("action")
        and _ref_matches(source_ref, source, "grant_id", installation=True)
        and _principal_ref_matches(actor_ref, principals.get(actor_id))
        and _same(source.get("principal_ref"), actor_ref)
        and _same(source.get("scope"), operation.get("source_scope"))
        and _same(source.get("resource_constraint"), operation.get("source_resource"))
    ):
        findings.append(
            _finding(
                "HGR-OPERATION-SOURCE-AUTHORITY",
                "source_grant_ref",
                "exact active source action authority is required",
            )
        )
    accept_ref = operation.get("target_acceptance_grant_ref")
    accept_id = (
        str(accept_ref.get("grant_id", "")) if isinstance(accept_ref, Mapping) else ""
    )
    accept = grants.get(accept_id)
    accept_ok, _ = _grant_status(
        authority_document, accept_id, at, authorized_revocations=grant_revocations
    )
    if not (
        accept_ok
        and accept is not None
        and accept.get("action") == "accept_cross_layer"
        and _ref_matches(accept_ref, accept, "grant_id", installation=True)
        and _same(accept.get("scope"), operation.get("target_scope"))
        and _same(accept.get("resource_constraint"), operation.get("target_resource"))
        and _same(
            accept.get("principal_ref"),
            binding.get("target_acceptance_principal_ref"),
        )
        and accept_ref == binding.get("target_acceptance_grant_ref")
    ):
        findings.append(
            _finding(
                "HGR-OPERATION-TARGET-AUTHORITY",
                "target_acceptance_grant_ref",
                "operation must retain exact active target acceptance",
            )
        )
    anchor_ref = operation.get("anchor_ref")
    anchor_id = (
        str(anchor_ref.get("anchor_id", "")) if isinstance(anchor_ref, Mapping) else ""
    )
    anchor = _index(authority_document, "trust_anchors").get(anchor_id)
    if not _ref_matches(
        anchor_ref, anchor, "anchor_id", installation=True
    ) or anchor_id != _active_anchor_id(authority_document, at):
        findings.append(
            _finding(
                "HGR-OPERATION-ANCHOR",
                "anchor_ref",
                "operation must cite the root active at its authorization time",
            )
        )
    findings.extend(_anchor_findings(authority_document))
    return _sorted(findings)


def validate_authority_document(
    document: Mapping[str, object], *, evaluation_time: str | None = None
) -> list[dict[str, str]]:
    """Validate one complete closed authority document deterministically."""

    findings: list[dict[str, str]] = []
    if not isinstance(document, Mapping):
        return [_finding("HGR-AUTHORITY-DOCUMENT-TYPE", "$", "mapping required")]
    at = _at(document, evaluation_time)
    if at is None:
        findings.append(
            _finding(
                "HGR-AUTHORITY-EVALUATION-TIME",
                "evaluation_time",
                "fixed RFC 3339 UTC evaluation time is required",
            )
        )
    findings.extend(_record_findings(document))
    findings.extend(_principal_lifecycle_findings(document))
    findings.extend(_anchor_findings(document))
    findings.extend(_grant_findings(document))
    findings.extend(_binding_findings(document))
    if at is not None:
        findings.extend(_database_binding_findings(document, at))
    for operation in _records(document, "operation_authorizations"):
        findings.extend(validate_operation_authorization(operation, document))
    return _sorted(findings)


def validate_append_only_authority(
    previous: Mapping[str, object], current: Mapping[str, object]
) -> list[dict[str, str]]:
    """Reject deletion, mutation, or reordering of immutable authority records."""

    findings: list[dict[str, str]] = []
    for collection, id_field in _COLLECTION_IDS.items():
        old = _records(previous, collection)
        new = _records(current, collection)
        new_by_id = {
            str(record.get(id_field, "")): record
            for record in new
            if isinstance(record.get(id_field), str)
        }
        for position, record in enumerate(old):
            identifier = str(record.get(id_field, ""))
            candidate = new_by_id.get(identifier)
            if candidate is None:
                findings.append(
                    _finding(
                        "HGR-AUTHORITY-RECORD-DELETE",
                        f"{collection}[{position}]",
                        f"immutable record {identifier!r} was deleted",
                    )
                )
            else:
                try:
                    changed = candidate != record or canonical_record_digest(
                        candidate
                    ) != canonical_record_digest(record)
                except (TypeError, ValueError):
                    changed = True
                if changed:
                    findings.append(
                        _finding(
                            "HGR-AUTHORITY-RECORD-UPDATE",
                            f"{collection}[{position}]",
                            f"immutable record {identifier!r} was changed",
                        )
                    )
        old_ids = [str(record.get(id_field, "")) for record in old]
        new_prefix = [str(record.get(id_field, "")) for record in new[: len(old)]]
        if new_prefix != old_ids:
            findings.append(
                _finding(
                    "HGR-AUTHORITY-RECORD-REORDER",
                    collection,
                    "existing authority records must remain an exact prefix",
                )
            )
    return _sorted(findings)
