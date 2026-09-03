"""The standards-body registry's own completeness and override rules.

A pure reader over an already-loaded document, plus the ONE loader that is safe
to load the registry with.

WHY THE LOADER IS HERE AND NOT LEFT TO `yaml.safe_load`. `safe_load` applies
LAST-DUPLICATE-KEY-WINS SILENTLY, and this registry met that defect on its first
day: the `sfia` entry carried `source_url` twice — the licensing page written
2026-08-09, then the SFIA 9 publication page added by this change — so the
parsed document held the publication URL and the licensing evidence was GONE,
while both lines sat visibly in the file for any human reading it. `registry_errors`
could not have caught it and no amount of checking after the parse can: by then
there is one key. Copilot found it on PR #593; the instance is repaired in the
YAML and the CLASS is closed here, by refusing at LOAD time.

The refusal is deliberately narrow — duplicate keys at any mapping level, and
nothing else. It is the same defect `scripts/frontmatter_strict.py` refuses for
proposal front matter and for the same reason, but it is NOT that module reused:
that loader carries a 65,536-byte ceiling and this registry is already ~77,000
bytes, so the shared thing is the rule rather than the code.

Deterministic: YAML/text reads only, no model calls, no writes, no network.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import yaml


class DuplicateRegistryKey(ValueError):
    """A registry mapping declares one key twice.

    Raised rather than reported as a finding because a finding is a statement
    ABOUT a document and this is a statement about whether the document can be
    read at all: the two values are already collapsed to one by the time any
    checker sees them, so the reader that returns a document at all would be
    returning the wrong one.
    """


class _NoDuplicatesLoader(yaml.SafeLoader):
    """`SafeLoader` that refuses a repeated key at ANY mapping level.

    Nesting cannot smuggle a duplicate past a top-level check — a duplicate
    inside `operator_override` discards a value exactly as well as one at the
    body's own level — so the refusal is done in `construct_mapping`, which
    every mapping in the document passes through.
    """


def _refuse_duplicate_keys(loader, node, deep=False):
    seen: set = set()
    for key_node, _value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in seen
        except TypeError:  # pragma: no cover - an unhashable key
            duplicate = False
        if duplicate:
            mark = key_node.start_mark
            raise DuplicateRegistryKey(
                f"duplicate key {key!r} at line {mark.line + 1}, column "
                f"{mark.column + 1} — the later value would silently replace "
                "the earlier one"
            )
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


_NoDuplicatesLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _refuse_duplicate_keys
)


def load_registry(path: str | Path):
    """Load the registry, refusing any document that declares a key twice.

    THE ONLY SUPPORTED WAY TO READ THIS FILE. A caller reaching for
    `yaml.safe_load` re-opens the class this module exists to close.
    """
    return yaml.load(Path(path).read_text(encoding="utf-8"), Loader=_NoDuplicatesLoader)


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
