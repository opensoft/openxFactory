from __future__ import annotations

from collections.abc import Mapping


CURRENT_PUBLICATION_IDS = frozenset({"itil5", "sfia", "apqc_pcf"})
CURRENT_PUBLICATION_FIELDS = (
    "current_version",
    "source_url",
    "verified_on",
    "confidence",
)
OVERRIDE_FIELDS = (
    "status",
    "decision",
    "approved_by",
    "approved_on",
    "rationale",
    "conflicting_source",
    "legal_review",
)


def _mapping(value: object) -> Mapping[str, object] | None:
    if isinstance(value, Mapping):
        return value
    return None


def registry_errors(document: object) -> list[str]:
    root = _mapping(document)
    if root is None:
        return ["registry: document must be a mapping"]

    bodies = root.get("bodies")
    if not isinstance(bodies, list):
        return ["registry.bodies: must be a list"]

    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, raw_body in enumerate(bodies):
        body = _mapping(raw_body)
        if body is None:
            errors.append(f"registry.bodies[{index}]: must be a mapping")
            continue
        body_id = body.get("id")
        if not isinstance(body_id, str) or not body_id:
            errors.append(f"registry.bodies[{index}].id: required")
            continue
        if body_id in seen_ids:
            errors.append(f"registry.bodies[{index}].id: duplicate '{body_id}'")
        seen_ids.add(body_id)

        if body_id in CURRENT_PUBLICATION_IDS:
            for field in CURRENT_PUBLICATION_FIELDS:
                if not body.get(field):
                    errors.append(
                        f"registry.bodies.{body_id}.{field}: required for current publication"
                    )

        override = _mapping(body.get("operator_override"))
        if override is None and body.get("operator_override") is not None:
            errors.append(
                f"registry.bodies.{body_id}.operator_override: must be a mapping"
            )
            continue
        if override is None:
            continue
        for field in OVERRIDE_FIELDS:
            if not override.get(field):
                errors.append(
                    f"registry.bodies.{body_id}.operator_override.{field}: required"
                )
        if override.get("status") != "unverified":
            errors.append(
                f"registry.bodies.{body_id}.operator_override.status: must be unverified"
            )
        if (
            override.get("decision") == "permit_product_configuration"
            and body.get("redistribution_permitted_in_product_config") != "yes"
        ):
            errors.append(
                f"registry.bodies.{body_id}.redistribution_permitted_in_product_config: "
                "must be yes for the recorded operator override"
            )
    return errors
