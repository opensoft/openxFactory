from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import jsonschema
import yaml

from .model import Finding, RecordDocument

SCHEMA_NAMES = {
    "veto_class_vocabulary": "veto-class-vocabulary.schema.yaml",
    "policy_allowance": "policy-allowance.schema.yaml",
    "policy_allowance_revocation": "policy-allowance-revocation.schema.yaml",
    "policy_allowance_registry": "policy-allowance-registry.schema.yaml",
    "compliance_decision": "compliance-decision.schema.yaml",
}


def schema_validators(
    family_dir: Path,
) -> dict[str, jsonschema.Draft202012Validator]:
    validators: dict[str, jsonschema.Draft202012Validator] = {}
    for kind, name in SCHEMA_NAMES.items():
        with (family_dir / name).open(encoding="utf-8") as stream:
            schema = yaml.safe_load(stream)
        if not isinstance(schema, dict):
            raise TypeError(f"{name} must contain a schema mapping")
        jsonschema.Draft202012Validator.check_schema(schema)
        validators[kind] = jsonschema.Draft202012Validator(
            schema,
            format_checker=jsonschema.FormatChecker(),
        )
    return validators


def schema_findings(
    document: RecordDocument,
    validators: dict[str, jsonschema.Draft202012Validator],
) -> list[Finding]:
    kind = document.data.get("kind")
    if not isinstance(kind, str) or kind not in validators:
        return [Finding("schema", str(document.path), "unknown record kind")]
    errors = sorted(
        validators[kind].iter_errors(document.data), key=lambda error: list(error.path)
    )
    return [
        Finding(
            "schema",
            str(document.path),
            f"{_safe_error_path(error.path)}: schema keyword {error.validator!s} failed",
        )
        for error in errors
    ]


def _safe_error_path(parts: Iterable[object]) -> str:
    rendered = ".".join(
        "[index]" if isinstance(part, int) else "[field]" for part in parts
    )
    return rendered or "<root>"
