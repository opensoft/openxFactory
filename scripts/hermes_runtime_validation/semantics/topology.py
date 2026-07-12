"""Pure topology, lifecycle, tombstone, and provisioning semantics."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence

CANONICAL_ROLES = ("customer", "client", "domain")
SUPPORTED_ISOLATION_SCOPES = frozenset(
    {
        "per_customer_subject",
        "per_tenant",
        "per_client",
        "per_customer",
        "per_patient",
        "per_campaign",
        "per_project",
        "per_ledger",
        "shared_with_review",
    }
)

TOPOLOGY_TRANSITIONS = {
    "installing": frozenset({"configured"}),
    "configured": frozenset({"operational", "retired"}),
    "operational": frozenset({"suspended", "retired"}),
    "suspended": frozenset({"operational", "retired"}),
    "retired": frozenset(),
}
LAYER_TRANSITIONS = {
    "provisioning": frozenset({"active", "failed", "retired"}),
    "active": frozenset({"suspended", "failed", "retired"}),
    "suspended": frozenset({"active", "failed", "retired"}),
    "failed": frozenset({"provisioning", "retired"}),
    "retired": frozenset(),
}


def _finding(code: str, path: str, message: str) -> dict[str, str]:
    return {
        "code": code,
        "severity": "error",
        "path": path,
        "message": message,
    }


def _sorted(findings: Iterable[Mapping[str, object]]) -> list[dict[str, str]]:
    return sorted(
        (dict(item) for item in findings),
        key=lambda item: (
            str(item.get("path", "")),
            str(item.get("code", "")),
            str(item.get("message", "")),
        ),
    )


def _subject_key(subject: object) -> tuple[str, str, str, str] | None:
    if not isinstance(subject, Mapping):
        return None
    fields = ("kind", "issuer", "namespace", "ref")
    if not all(isinstance(subject.get(field), str) for field in fields):
        return None
    return tuple(str(subject[field]) for field in fields)  # type: ignore[return-value]


def validate_static_templates(
    templates: Sequence[Mapping[str, object]],
    *,
    isolation_scopes: Sequence[str] = (),
) -> list[dict[str, str]]:
    """Enforce one canonical template per role and the compatibility vocabulary."""

    findings: list[dict[str, str]] = []
    counts = Counter(str(template.get("role", "")) for template in templates)
    for role in CANONICAL_ROLES:
        if counts[role] > 1:
            findings.append(
                _finding(
                    "HCS-STATIC-ROLE-DUPLICATE",
                    "role_templates",
                    f"canonical role {role} is declared {counts[role]} times",
                )
            )
        elif counts[role] == 0:
            findings.append(
                _finding(
                    "HCS-STATIC-ROLE-MISSING",
                    "role_templates",
                    f"canonical role {role} is not declared",
                )
            )
    unknown = sorted(set(isolation_scopes) - SUPPORTED_ISOLATION_SCOPES)
    if unknown:
        findings.append(
            _finding(
                "HCS-STATIC-ISOLATION-UNKNOWN",
                "isolation_scopes",
                f"unknown isolation scope(s): {', '.join(unknown)}",
            )
        )
    return _sorted(findings)


def _duplicate_values(
    layers: Sequence[Mapping[str, object]],
    field: str,
    code: str,
) -> list[dict[str, str]]:
    values = [layer.get(field) for layer in layers if layer.get(field) is not None]
    duplicates = sorted(
        str(value) for value, count in Counter(map(str, values)).items() if count > 1
    )
    return [
        _finding(code, f"layer_registrations.{field}", f"identity is reused: {value}")
        for value in duplicates
    ]


def validate_topology(
    document: Mapping[str, object],
    *,
    tombstones: Sequence[Mapping[str, object]] = (),
) -> list[dict[str, str]]:
    """Validate neutral runtime cardinality and lifetime-unique layer identity."""

    findings: list[dict[str, str]] = []
    root_installation_id = str(document.get("installation_id", ""))
    root_stack_id = str(document.get("stack_id", ""))

    installation_registration = document.get("installation_registration")
    if isinstance(installation_registration, Mapping) and str(
        installation_registration.get("installation_id", "")
    ) != root_installation_id:
        findings.append(
            _finding(
                "HCS-TOPOLOGY-INSTALLATION-SCOPE-MISMATCH",
                "installation_registration.installation_id",
                "installation registration must belong to the topology installation",
            )
        )
    stack_registration = document.get("stack_registration")
    if isinstance(stack_registration, Mapping):
        if str(stack_registration.get("installation_id", "")) != root_installation_id:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-INSTALLATION-SCOPE-MISMATCH",
                    "stack_registration.installation_id",
                    "stack registration must belong to the topology installation",
                )
            )
        if str(stack_registration.get("stack_id", "")) != root_stack_id:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-STACK-SCOPE-MISMATCH",
                    "stack_registration.stack_id",
                    "stack registration must be the topology's single stack",
                )
            )

    templates = document.get("role_templates", []) or []
    if isinstance(templates, list):
        findings.extend(validate_static_templates(templates))
    layers = document.get("layer_registrations", []) or []
    if not isinstance(layers, list):
        return [_finding("HCS-TOPOLOGY-LAYERS-TYPE", "layer_registrations", "list required")]
    typed_layers = [layer for layer in layers if isinstance(layer, Mapping)]

    declared_template_roles = {
        str(template.get("role", ""))
        for template in templates
        if isinstance(template, Mapping)
    }
    for index, layer in enumerate(typed_layers):
        if str(layer.get("installation_id", "")) != root_installation_id:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-INSTALLATION-SCOPE-MISMATCH",
                    f"layer_registrations[{index}].installation_id",
                    "layer registration must belong to the topology installation",
                )
            )
        if str(layer.get("stack_id", "")) != root_stack_id:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-STACK-SCOPE-MISMATCH",
                    f"layer_registrations[{index}].stack_id",
                    "layer registration must belong to the topology's single stack",
                )
            )
        role = str(layer.get("role", ""))
        template_role = str(layer.get("template_role", ""))
        if template_role not in declared_template_roles:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TEMPLATE-UNDECLARED",
                    f"layer_registrations[{index}].template_role",
                    f"template role {template_role!r} is not declared",
                )
            )
        elif template_role != role:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TEMPLATE-ROLE-MISMATCH",
                    f"layer_registrations[{index}].template_role",
                    "runtime role must exactly match its declared static template role",
                )
            )

    projections = document.get("lifecycle_projections", []) or []
    typed_projections = (
        [item for item in projections if isinstance(item, Mapping)]
        if isinstance(projections, list)
        else []
    )
    projection_by_key: dict[tuple[str, str, str, str], Mapping[str, object]] = {}
    projection_states = {
        "installation": frozenset(TOPOLOGY_TRANSITIONS),
        "stack": frozenset(TOPOLOGY_TRANSITIONS),
        "layer": frozenset(LAYER_TRANSITIONS),
    }
    registered_layer_scopes = {
        (
            str(layer.get("installation_id", "")),
            str(layer.get("stack_id", "")),
            str(layer.get("layer_id", "")),
        )
        for layer in typed_layers
    }
    for index, projection in enumerate(typed_projections):
        entity_kind = str(projection.get("entity_kind", ""))
        installation_id = str(projection.get("installation_id", ""))
        stack_id = str(projection.get("stack_id", ""))
        layer_id = str(projection.get("layer_id", ""))
        key = (entity_kind, installation_id, stack_id, layer_id)
        if key in projection_by_key:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PROJECTION-DUPLICATE",
                    f"lifecycle_projections[{index}]",
                    "one lifecycle projection is allowed per exact entity scope",
                )
            )
        else:
            projection_by_key[key] = projection
        if str(projection.get("state", "")) not in projection_states.get(
            entity_kind, frozenset()
        ):
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PROJECTION-STATE",
                    f"lifecycle_projections[{index}].state",
                    "projection state is not valid for its entity kind",
                )
            )
        if installation_id != root_installation_id:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-INSTALLATION-SCOPE-MISMATCH",
                    f"lifecycle_projections[{index}].installation_id",
                    "lifecycle projection must belong to the topology installation",
                )
            )
        if entity_kind in {"stack", "layer"} and stack_id != root_stack_id:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-STACK-SCOPE-MISMATCH",
                    f"lifecycle_projections[{index}].stack_id",
                    "lifecycle projection must belong to the topology's single stack",
                )
            )
        if (
            entity_kind == "layer"
            and (installation_id, stack_id, layer_id)
            not in registered_layer_scopes
        ):
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PROJECTION-ORPHAN",
                    f"lifecycle_projections[{index}]",
                    "layer projection requires one exact immutable registration",
                )
            )

    def layer_state(layer: Mapping[str, object]) -> str:
        key = (
            "layer",
            str(layer.get("installation_id", "")),
            str(layer.get("stack_id", "")),
            str(layer.get("layer_id", "")),
        )
        projection = projection_by_key.get(key)
        if projection is None:
            return ""
        return str(projection.get("state", ""))

    for index, layer in enumerate(typed_layers):
        if not layer_state(layer):
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PROJECTION-MISSING",
                    f"layer_registrations[{index}]",
                    "layer registration requires one exact lifecycle projection",
                )
            )

    installation_projection = projection_by_key.get(
        ("installation", root_installation_id, "", "")
    )
    stack_projection = projection_by_key.get(
        ("stack", root_installation_id, root_stack_id, "")
    )
    state = str(document.get("derived_topology_state", ""))
    for projection, path in (
        (installation_projection, "installation"),
        (stack_projection, "stack"),
    ):
        if projection is None:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PROJECTION-MISSING",
                    f"lifecycle_projections.{path}",
                    f"{path} requires one exact lifecycle projection",
                )
            )
        elif str(projection.get("state", "")) != state:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-STATE-PROJECTION-DRIFT",
                    f"lifecycle_projections.{path}.state",
                    "topology state must reconcile to installation and stack projections",
                )
            )

    role_layers = {
        role: [layer for layer in typed_layers if layer.get("role") == role]
        for role in CANONICAL_ROLES
    }
    if state == "installing":
        for role in ("client", "domain"):
            if len(role_layers[role]) > 1:
                findings.append(
                    _finding(
                        f"HCS-TOPOLOGY-{role.upper()}-CARDINALITY",
                        "layer_registrations",
                        f"installing topology allows at most one lifetime {role} registration",
                    )
                )
        if role_layers["customer"]:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-INSTALLING-CUSTOMER-FORBIDDEN",
                    "layer_registrations",
                    "installing topology cannot register a Customer layer",
                )
            )
    elif state in {"configured", "operational"}:
        for role in ("client", "domain"):
            registrations = role_layers[role]
            if len(registrations) != 1 or layer_state(registrations[0]) != "active":
                findings.append(
                    _finding(
                        f"HCS-TOPOLOGY-{role.upper()}-CARDINALITY",
                        "layer_registrations",
                        f"{state} topology requires exactly one lifetime, active {role} registration",
                    )
                )
        if state == "operational":
            active_customers = [
                layer
                for layer in role_layers["customer"]
                if layer_state(layer) == "active"
            ]
            if not active_customers:
                findings.append(
                    _finding(
                        "HCS-TOPOLOGY-CUSTOMER-MIN",
                        "layer_registrations",
                        "operational topology requires at least one active Customer layer",
                    )
                )
    elif state == "suspended":
        for role in ("client", "domain"):
            registrations = role_layers[role]
            if (
                len(registrations) != 1
                or layer_state(registrations[0]) == "retired"
            ):
                findings.append(
                    _finding(
                        f"HCS-TOPOLOGY-{role.upper()}-CARDINALITY",
                        "layer_registrations",
                        f"suspended topology preserves exactly one lifetime {role} registration",
                    )
                )
        if not role_layers["customer"]:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-SUSPENDED-CUSTOMER-PRESERVATION",
                    "layer_registrations",
                    "suspended topology must preserve its Customer registrations",
                )
            )
    elif state == "retired":
        if any(len(role_layers[role]) != 1 for role in ("client", "domain")):
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-RETIREMENT-PRESERVATION",
                    "layer_registrations",
                    "retired topology must preserve its Client and Domain registrations",
                )
            )
        if any(layer_state(layer) != "retired" for layer in typed_layers):
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-RETIREMENT-INCOMPLETE",
                    "layer_registrations",
                    "retired topology requires every layer to be retired",
                )
            )
    else:
        findings.append(
            _finding(
                "HCS-TOPOLOGY-STATE-UNKNOWN",
                "derived_topology_state",
                f"unknown topology state {state!r}",
            )
        )

    findings.extend(
        _duplicate_values(
            typed_layers,
            "registration_id",
            "HCS-TOPOLOGY-REGISTRATION-ID-REUSE",
        )
    )
    findings.extend(
        _duplicate_values(typed_layers, "layer_id", "HCS-TOPOLOGY-LAYER-ID-REUSE")
    )
    findings.extend(
        _duplicate_values(
            typed_layers,
            "policy_namespace",
            "HCS-TOPOLOGY-POLICY-NAMESPACE-REUSE",
        )
    )
    subject_keys = [
        key
        for key in (_subject_key(layer.get("customer_subject")) for layer in typed_layers)
        if key is not None
    ]
    if any(count > 1 for count in Counter(subject_keys).values()):
        findings.append(
            _finding(
                "HCS-TOPOLOGY-SUBJECT-REUSE",
                "layer_registrations.customer_subject",
                "Customer subject tuple is reused",
            )
        )

    for index, layer in enumerate(typed_layers):
        role = layer.get("role")
        subject_present = layer.get("customer_subject") is not None
        if role == "customer" and not subject_present:
            findings.append(
                _finding(
                    "HCS-SUBJECT-REQUIRED",
                    f"layer_registrations[{index}].customer_subject",
                    "Customer layers require a customer_subject",
                )
            )
        elif role == "extension" and subject_present:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-EXTENSION-CUSTOMER-EVASION",
                    f"layer_registrations[{index}].customer_subject",
                    "extension layer cannot represent a Customer subject",
                )
            )
        elif role in {"client", "domain"} and subject_present:
            findings.append(
                _finding(
                    "HCS-SUBJECT-FORBIDDEN",
                    f"layer_registrations[{index}].customer_subject",
                    f"{role} layer cannot carry a customer_subject",
                )
            )

    indexed_tombstones = document.get("retired_layer_tombstones", []) or []
    effective_tombstones = [
        item
        for item in (*indexed_tombstones, *tombstones)
        if isinstance(item, Mapping)
    ] if isinstance(indexed_tombstones, list) else [
        item for item in tombstones if isinstance(item, Mapping)
    ]
    tombstone_layer_ids = {str(item.get("layer_id")) for item in effective_tombstones}
    tombstone_namespaces = {
        str(item.get("policy_namespace")) for item in effective_tombstones
    }
    tombstone_subjects = {
        key
        for key in (
            _subject_key(item.get("customer_subject"))
            for item in effective_tombstones
        )
        if key is not None
    }
    tombstones_by_layer: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for item in effective_tombstones:
        tombstones_by_layer[str(item.get("layer_id", ""))].append(item)
    for layer_id, matches in sorted(tombstones_by_layer.items()):
        if len(matches) > 1:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TOMBSTONE-DUPLICATE",
                    "retired_layer_tombstones",
                    f"retired layer {layer_id!r} has multiple tombstones",
                )
            )
    registered_layer_ids = {
        str(layer.get("layer_id", "")) for layer in typed_layers
    }
    registered_policy_namespaces = {
        str(layer.get("policy_namespace", "")) for layer in typed_layers
    }
    registered_subjects = {
        key
        for key in (
            _subject_key(layer.get("customer_subject")) for layer in typed_layers
        )
        if key is not None
    }
    for layer_id, matches in sorted(tombstones_by_layer.items()):
        tombstone = matches[0]
        preserves_known_identity = (
            layer_id in registered_layer_ids
            or str(tombstone.get("policy_namespace", ""))
            in registered_policy_namespaces
            or _subject_key(tombstone.get("customer_subject"))
            in registered_subjects
        )
        if not preserves_known_identity:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TOMBSTONE-ORPHAN",
                    f"retired_layer_tombstones.{layer_id}",
                    "retirement tombstone requires a preserved layer registration",
                )
            )
    for layer in typed_layers:
        if layer_state(layer) != "retired":
            continue
        layer_id = str(layer.get("layer_id", ""))
        matches = tombstones_by_layer.get(layer_id, [])
        if not matches:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TOMBSTONE-MISSING",
                    f"layer_registrations.{layer_id}",
                    "retired layer must preserve one durable identity tombstone",
                )
            )
            continue
        tombstone = matches[0]
        projection = projection_by_key.get(
            (
                "layer",
                str(layer.get("installation_id", "")),
                str(layer.get("stack_id", "")),
                layer_id,
            )
        )
        mismatch = (
            tombstone.get("policy_namespace") != layer.get("policy_namespace")
            or tombstone.get("customer_subject") != layer.get("customer_subject")
            or projection is None
            or tombstone.get("retired_event_id")
            != projection.get("latest_event_id")
            or tombstone.get("retired_event_digest")
            != projection.get("latest_event_digest")
        )
        if mismatch:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TOMBSTONE-MISMATCH",
                    f"retired_layer_tombstones.{layer_id}",
                    "tombstone must exactly bind the retired registration and terminal event",
                )
            )
    live_layers = [layer for layer in typed_layers if layer_state(layer) != "retired"]
    if any(str(layer.get("layer_id")) in tombstone_layer_ids for layer in live_layers):
        findings.append(
            _finding(
                "HCS-TOPOLOGY-LAYER-ID-REUSE",
                "layer_registrations.layer_id",
                "layer_id is preserved by a retirement tombstone",
            )
        )
    if any(
        str(layer.get("policy_namespace")) in tombstone_namespaces
        for layer in live_layers
    ):
        findings.append(
            _finding(
                "HCS-TOPOLOGY-POLICY-NAMESPACE-REUSE",
                "layer_registrations.policy_namespace",
                "policy namespace is preserved by a retirement tombstone",
            )
        )
    if any(
        _subject_key(layer.get("customer_subject")) in tombstone_subjects
        for layer in live_layers
        if layer.get("customer_subject") is not None
    ):
        findings.append(
            _finding(
                "HCS-TOPOLOGY-SUBJECT-REUSE",
                "layer_registrations.customer_subject",
                "Customer subject tuple is preserved by a retirement tombstone",
            )
        )

    return _sorted(findings)


def validate_provisioning_requests(
    requests: Sequence[Mapping[str, object]],
    *,
    layer_registrations: Sequence[Mapping[str, object]] | None = None,
) -> list[dict[str, str]]:
    """Make an exact idempotency key converge onto one registered Customer."""

    findings: list[dict[str, str]] = []
    by_key: dict[str, Mapping[str, object]] = {}
    conflicted: set[str] = set()
    for index, request in enumerate(requests):
        key = request.get("idempotency_key")
        if not isinstance(key, str) or not key:
            findings.append(
                _finding(
                    "HCS-PROVISION-IDEMPOTENCY-KEY-REQUIRED",
                    f"provisioning_requests[{index}].idempotency_key",
                    "non-empty idempotency key required",
                )
            )
            continue
        previous = by_key.setdefault(key, request)
        if previous != request and key not in conflicted:
            conflicted.add(key)
            findings.append(
                _finding(
                    "HCS-PROVISION-IDEMPOTENCY-CONFLICT",
                    f"provisioning_requests[{index}]",
                    f"idempotency key {key!r} was reused with another subject or result",
                )
            )
    if layer_registrations is not None:
        for key, request in sorted(by_key.items()):
            if key in conflicted:
                # The conflict is the authoritative primary reason. Its competing
                # results are not independently evaluated as realized outcomes.
                continue
            matches = [
                layer
                for layer in layer_registrations
                if layer.get("role") == "customer"
                and layer.get("layer_id") == request.get("layer_id")
                and layer.get("registration_id")
                == request.get("lifecycle_record_id")
                and layer.get("customer_subject")
                == request.get("customer_subject")
            ]
            if len(matches) != 1:
                findings.append(
                    _finding(
                        "HCS-PROVISION-RESULT-UNBOUND",
                        f"provisioning_requests.{key}",
                        "non-conflicted provisioning result must bind exactly one "
                        "Customer registration, registration ID, and subject",
                    )
                )
    return _sorted(findings)


def validate_new_job_admission(
    document: Mapping[str, object],
) -> list[dict[str, str]]:
    """Reject a new governed job while topology lifecycle forbids new work."""

    state = str(document.get("derived_topology_state", ""))
    if state in {"suspended", "retired"}:
        return [
            _finding(
                "HCS-TOPOLOGY-NEW-JOB-FORBIDDEN",
                "derived_topology_state",
                f"topology state {state!r} does not admit new governed jobs",
            )
        ]
    return []


def validate_lifecycle_transition(
    entity_kind: str,
    from_state: str,
    to_state: str,
) -> list[dict[str, str]]:
    """Validate one closed state-machine edge without mutating history."""

    graph = LAYER_TRANSITIONS if entity_kind == "layer" else TOPOLOGY_TRANSITIONS
    if entity_kind not in {"installation", "stack", "layer"}:
        return [
            _finding(
                "HCS-LIFECYCLE-ENTITY-KIND",
                "entity_kind",
                f"unknown lifecycle entity kind {entity_kind!r}",
            )
        ]
    if from_state == "retired" and to_state != "retired":
        return [
            _finding(
                "HCS-LIFECYCLE-RETIRED-TERMINAL",
                "to_state",
                "retired is terminal",
            )
        ]
    if to_state not in graph.get(from_state, frozenset()):
        return [
            _finding(
                "HCS-LIFECYCLE-TRANSITION",
                "to_state",
                f"invalid {entity_kind} transition {from_state!r} -> {to_state!r}",
            )
        ]
    return []


def _registration_id(entity_kind: str, registration: Mapping[str, object]) -> str:
    key = {
        "installation": "installation_id",
        "stack": "stack_id",
        "layer": "layer_id",
    }[entity_kind]
    return str(registration.get("registration_id") or registration.get(key) or "")


def _projection_scope(
    entity_kind: str,
    registration: Mapping[str, object],
) -> dict[str, object]:
    keys = {
        "installation": ("installation_id",),
        "stack": ("installation_id", "stack_id"),
        "layer": ("installation_id", "stack_id", "layer_id"),
    }[entity_kind]
    return {
        "entity_kind": entity_kind,
        **{key: registration[key] for key in keys if key in registration},
    }


def _lifecycle_scope_keys(entity_kind: str) -> tuple[str, ...]:
    return {
        "installation": ("installation_id",),
        "stack": ("installation_id", "stack_id"),
        "layer": ("installation_id", "stack_id", "layer_id"),
    }[entity_kind]


def derive_lifecycle_projection(
    entity_kind: str,
    registration: Mapping[str, object],
    events: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    """Derive the non-authoritative current-state cache from immutable history."""

    projection = _projection_scope(entity_kind, registration)
    if events:
        latest = events[-1]
        state = latest.get("to_state")
        projection.update(
            {
                "latest_event_id": latest.get("event_id"),
                "latest_event_digest": latest.get("event_digest"),
                "state": state,
                "terminal_time": latest.get("occurred_at") if state == "retired" else None,
            }
        )
    else:
        projection.update(
            {
                "latest_event_id": None,
                "latest_event_digest": None,
                "state": registration.get("initial_lifecycle_state"),
                "terminal_time": None,
            }
        )
    return projection


def validate_lifecycle_history(
    entity_kind: str,
    registration: Mapping[str, object],
    events: Sequence[Mapping[str, object]],
    projection: Mapping[str, object] | None,
) -> list[dict[str, str]]:
    """Validate one linear predecessor chain and reconcile any cache projection."""

    findings: list[dict[str, str]] = []
    if entity_kind not in {"installation", "stack", "layer"}:
        return validate_lifecycle_transition(entity_kind, "", "")
    registration_kind = registration.get("entity_kind")
    if registration_kind is not None and registration_kind != entity_kind:
        findings.append(
            _finding(
                "HCS-LIFECYCLE-ENTITY-KIND",
                "registration.entity_kind",
                "registration entity_kind must match the lifecycle contract",
            )
        )
    event_ids = [str(event.get("event_id", "")) for event in events]
    for event_id, count in Counter(event_ids).items():
        if not event_id or count > 1:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-EVENT-ID-DUPLICATE",
                    "events.event_id",
                    f"event_id must be non-empty and unique: {event_id!r}",
                )
            )

    successors: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    scope_keys = _lifecycle_scope_keys(entity_kind)
    for index, event in enumerate(events):
        for scope_key in scope_keys:
            if event.get(scope_key) != registration.get(scope_key):
                findings.append(
                    _finding(
                        "HCS-LIFECYCLE-SCOPE-MISMATCH",
                        f"events[{index}].{scope_key}",
                        f"event {scope_key} must match its immutable registration",
                    )
                )
        predecessor = event.get("predecessor_ref")
        if isinstance(predecessor, Mapping):
            key = (str(predecessor.get("id", "")), str(predecessor.get("digest", "")))
        else:
            key = ("", "")
        successors[key].append(event)
    for key, candidates in successors.items():
        if len(candidates) > 1:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PREDECESSOR-FORK",
                    "events.predecessor_ref",
                    f"predecessor {key[0]!r}/{key[1]!r} has multiple successors",
                )
            )

    expected = (
        _registration_id(entity_kind, registration),
        str(registration.get("registration_digest", "")),
    )
    current_state = str(registration.get("initial_lifecycle_state", ""))
    ordered: list[Mapping[str, object]] = []
    visited: set[str] = set()
    while len(ordered) < len(events):
        candidates = successors.get(expected, [])
        if not candidates:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PREDECESSOR-MISMATCH",
                    "events.predecessor_ref",
                    f"no successor references expected predecessor {expected[0]!r}",
                )
            )
            break
        event = sorted(candidates, key=lambda item: str(item.get("event_id", "")))[0]
        event_id = str(event.get("event_id", ""))
        if event_id in visited:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PREDECESSOR-CYCLE",
                    "events.predecessor_ref",
                    f"event cycle includes {event_id!r}",
                )
            )
            break
        visited.add(event_id)
        ordered.append(event)
        predecessor = event.get("predecessor_ref")
        expected_predecessor_kind = "registration" if len(ordered) == 1 else "event"
        actual_predecessor_kind = (
            str(predecessor.get("kind", ""))
            if isinstance(predecessor, Mapping)
            else ""
        )
        if actual_predecessor_kind != expected_predecessor_kind:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PREDECESSOR-KIND",
                    f"events.{event_id}.predecessor_ref.kind",
                    f"expected predecessor kind {expected_predecessor_kind!r}",
                )
            )
        if str(event.get("from_state", "")) != current_state:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-FROM-STATE",
                    f"events.{event_id}.from_state",
                    f"event starts at {event.get('from_state')!r}, expected {current_state!r}",
                )
            )
        findings.extend(
            validate_lifecycle_transition(
                entity_kind,
                str(event.get("from_state", "")),
                str(event.get("to_state", "")),
            )
        )
        current_state = str(event.get("to_state", ""))
        expected = (event_id, str(event.get("event_digest", "")))

    if len(ordered) != len(events) and not any(
        item["code"] == "HCS-LIFECYCLE-PREDECESSOR-MISMATCH" for item in findings
    ):
        findings.append(
            _finding(
                "HCS-LIFECYCLE-PREDECESSOR-MISMATCH",
                "events.predecessor_ref",
                "not every lifecycle event is reachable from the registration",
            )
        )
    if projection is not None and not findings:
        derived = derive_lifecycle_projection(entity_kind, registration, ordered)
        if dict(projection) != derived:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PROJECTION-DRIFT",
                    "projection",
                    "current-state projection does not match the immutable event chain",
                )
            )
    elif projection is not None and events:
        derived = derive_lifecycle_projection(entity_kind, registration, ordered or events)
        if dict(projection) != derived:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-PROJECTION-DRIFT",
                    "projection",
                    "current-state projection does not match the immutable event chain",
                )
            )
    return _sorted(findings)


def validate_append_only_history(
    original_registration: Mapping[str, object],
    original_events: Sequence[Mapping[str, object]],
    candidate_registration: Mapping[str, object],
    candidate_events: Sequence[Mapping[str, object]],
) -> list[dict[str, str]]:
    """Reject registration/event rewrites while permitting a valid successor append."""

    findings: list[dict[str, str]] = []
    if dict(original_registration) != dict(candidate_registration):
        findings.append(
            _finding(
                "HCS-LIFECYCLE-REGISTRATION-IMMUTABLE",
                "registration",
                "identity registration is immutable",
            )
        )
    candidate_by_id = {
        str(event.get("event_id", "")): event for event in candidate_events
    }
    for original in original_events:
        event_id = str(original.get("event_id", ""))
        candidate = candidate_by_id.get(event_id)
        if candidate is None:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-EVENT-DELETE",
                    f"events.{event_id}",
                    "existing lifecycle event was deleted",
                )
            )
        elif dict(candidate) != dict(original):
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-EVENT-UPDATE",
                    f"events.{event_id}",
                    "existing lifecycle event was modified",
                )
            )
    entity_kind = str(candidate_registration.get("entity_kind", "layer"))
    findings.extend(
        validate_lifecycle_history(
            entity_kind,
            candidate_registration,
            candidate_events,
            None,
        )
    )
    return _sorted(findings)


def validate_topology_document(
    document: Mapping[str, object],
) -> list[dict[str, str]]:
    """Run the complete portable topology/lifecycle/provisioning semantic slice.

    Structural validation remains the responsibility of the offline schema
    registry. This orchestration prevents callers from validating cardinality
    while accidentally omitting the authoritative lifecycle histories,
    projection reconciliation, or provisioning idempotency checks.
    """

    findings: list[dict[str, str]] = list(validate_topology(document))
    raw_projections = document.get("lifecycle_projections", []) or []
    projections = (
        [item for item in raw_projections if isinstance(item, Mapping)]
        if isinstance(raw_projections, list)
        else []
    )

    def exact_projection(
        entity_kind: str,
        registration: Mapping[str, object],
    ) -> Mapping[str, object] | None:
        scope_keys = _lifecycle_scope_keys(entity_kind)
        matches = [
            projection
            for projection in projections
            if projection.get("entity_kind") == entity_kind
            and all(projection.get(key) == registration.get(key) for key in scope_keys)
        ]
        return matches[0] if len(matches) == 1 else None

    histories: list[
        tuple[str, Mapping[str, object], Sequence[Mapping[str, object]]]
    ] = []
    installation_registration = document.get("installation_registration")
    installation_events = document.get("installation_lifecycle_events", []) or []
    if isinstance(installation_registration, Mapping) and isinstance(
        installation_events, list
    ):
        histories.append(
            (
                "installation",
                installation_registration,
                [item for item in installation_events if isinstance(item, Mapping)],
            )
        )

    stack_registration = document.get("stack_registration")
    stack_events = document.get("stack_lifecycle_events", []) or []
    if isinstance(stack_registration, Mapping) and isinstance(stack_events, list):
        histories.append(
            (
                "stack",
                stack_registration,
                [item for item in stack_events if isinstance(item, Mapping)],
            )
        )

    raw_layer_events = document.get("layer_lifecycle_events", []) or []
    layer_events = (
        [item for item in raw_layer_events if isinstance(item, Mapping)]
        if isinstance(raw_layer_events, list)
        else []
    )
    raw_layers = document.get("layer_registrations", []) or []
    layers = (
        [item for item in raw_layers if isinstance(item, Mapping)]
        if isinstance(raw_layers, list)
        else []
    )
    registered_layer_scopes = {
        (
            registration.get("installation_id"),
            registration.get("stack_id"),
            registration.get("layer_id"),
        )
        for registration in layers
    }
    for index, event in enumerate(layer_events):
        event_scope = (
            event.get("installation_id"),
            event.get("stack_id"),
            event.get("layer_id"),
        )
        if event_scope not in registered_layer_scopes:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-EVENT-ORPHAN",
                    f"layer_lifecycle_events[{index}]",
                    "layer event must name one exact immutable registration scope",
                )
            )
    if isinstance(raw_layers, list):
        for registration in layers:
            events = [
                event
                for event in layer_events
                if all(
                    event.get(key) == registration.get(key)
                    for key in ("installation_id", "stack_id", "layer_id")
                )
            ]
            histories.append(("layer", registration, events))

    for entity_kind, registration, events in histories:
        findings.extend(
            validate_lifecycle_history(
                entity_kind,
                registration,
                events,
                exact_projection(entity_kind, registration),
            )
        )

    raw_requests = document.get("provisioning_requests", []) or []
    if isinstance(raw_requests, list):
        findings.extend(
            validate_provisioning_requests(
                [item for item in raw_requests if isinstance(item, Mapping)],
                layer_registrations=layers,
            )
        )
    return _sorted(findings)


def _mapping_sequence(
    document: Mapping[str, object],
    key: str,
) -> list[Mapping[str, object]]:
    raw = document.get(key, []) or []
    if not isinstance(raw, list):
        return []
    return [item for item in raw if isinstance(item, Mapping)]


def _layer_history(
    document: Mapping[str, object],
    registration: Mapping[str, object],
) -> list[Mapping[str, object]]:
    return [
        event
        for event in _mapping_sequence(document, "layer_lifecycle_events")
        if all(
            event.get(key) == registration.get(key)
            for key in ("installation_id", "stack_id", "layer_id")
        )
    ]


def validate_append_only_topology(
    original: Mapping[str, object],
    candidate: Mapping[str, object],
) -> list[dict[str, str]]:
    """Validate one topology replacement against its complete prior snapshot.

    Registrations, lifecycle events, and tombstones are immutable evidence.
    Projections may advance only because ``validate_topology_document`` proves
    that they exactly reconcile to an append-only candidate history.
    """

    findings: list[dict[str, str]] = list(validate_topology_document(candidate))

    for scope_key in ("installation_id", "stack_id"):
        if original.get(scope_key) != candidate.get(scope_key):
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-SCOPE-IMMUTABLE",
                    scope_key,
                    f"topology {scope_key} is immutable",
                )
            )

    for entity_kind, registration_key, event_key in (
        (
            "installation",
            "installation_registration",
            "installation_lifecycle_events",
        ),
        ("stack", "stack_registration", "stack_lifecycle_events"),
    ):
        original_registration = original.get(registration_key)
        candidate_registration = candidate.get(registration_key)
        if not isinstance(original_registration, Mapping):
            continue
        if not isinstance(candidate_registration, Mapping):
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-REGISTRATION-DELETE",
                    registration_key,
                    f"immutable {entity_kind} registration was deleted",
                )
            )
            continue
        findings.extend(
            validate_append_only_history(
                original_registration,
                _mapping_sequence(original, event_key),
                candidate_registration,
                _mapping_sequence(candidate, event_key),
            )
        )

    original_layers = _mapping_sequence(original, "layer_registrations")
    candidate_layers = _mapping_sequence(candidate, "layer_registrations")
    candidate_layers_by_registration: dict[
        str, list[Mapping[str, object]]
    ] = defaultdict(list)
    for registration in candidate_layers:
        candidate_layers_by_registration[
            str(registration.get("registration_id", ""))
        ].append(registration)

    for original_registration in original_layers:
        registration_id = str(original_registration.get("registration_id", ""))
        matches = candidate_layers_by_registration.get(registration_id, [])
        if not matches:
            findings.append(
                _finding(
                    "HCS-LIFECYCLE-REGISTRATION-DELETE",
                    f"layer_registrations.{registration_id}",
                    "immutable layer registration was deleted",
                )
            )
            continue
        if len(matches) > 1:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-REGISTRATION-ID-REUSE",
                    f"layer_registrations.{registration_id}",
                    "layer registration ID must identify exactly one registration",
                )
            )
        candidate_registration = matches[0]
        findings.extend(
            validate_append_only_history(
                original_registration,
                _layer_history(original, original_registration),
                candidate_registration,
                _layer_history(candidate, candidate_registration),
            )
        )

    candidate_tombstones: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for tombstone in _mapping_sequence(candidate, "retired_layer_tombstones"):
        candidate_tombstones[str(tombstone.get("layer_id", ""))].append(tombstone)
    for original_tombstone in _mapping_sequence(
        original, "retired_layer_tombstones"
    ):
        layer_id = str(original_tombstone.get("layer_id", ""))
        matches = candidate_tombstones.get(layer_id, [])
        if not matches:
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TOMBSTONE-DELETE",
                    f"retired_layer_tombstones.{layer_id}",
                    "durable retirement tombstone was deleted",
                )
            )
        elif dict(matches[0]) != dict(original_tombstone):
            findings.append(
                _finding(
                    "HCS-TOPOLOGY-TOMBSTONE-UPDATE",
                    f"retired_layer_tombstones.{layer_id}",
                    "durable retirement tombstone was modified",
                )
            )

    return _sorted(findings)
