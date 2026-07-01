#!/usr/bin/env python3
"""Validate the xFactory intake template starter catalog."""

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
TEMPLATE_DIR = ROOT / "templates" / "intake"

REQUIRED_TEMPLATE_KEYS = {
    "schema_version",
    "kind",
    "template",
    "taxonomy_defaults",
    "supported_profiles",
    "recommended_questions",
    "common_workflows",
    "credential_families",
    "adapter_families",
    "risk_defaults",
    "hermes_mixture_defaults",
    "runtime_binding_focus",
}

REQUIRED_TAXONOMY_KEYS = {
    "factory_type",
    "factory_subtype",
    "target_domain",
    "target_domain_subtype",
    "client_industry",
    "client_type",
    "customer_subject_type",
}

REQUIRED_SUBTYPE_KEYS = {
    "id",
    "label",
    "factory_subtype",
    "target_domain",
    "target_domain_subtype",
    "client_types",
    "customer_subject_types",
    "starter_workflows",
    "credential_families",
    "adapter_families",
    "high_risk_boundaries",
    "recommended_questions",
    "hermes_mixture_defaults",
    "runtime_binding_focus",
}

ALLOWED_MIX_MODES = {"panel_synthesis", "scored_vote", "deliberative_council"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def validate_template(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_yaml(path)
    missing = REQUIRED_TEMPLATE_KEYS - set(data)
    for key in sorted(missing):
        errors.append(f"{path.relative_to(ROOT)} missing top-level key: {key}")

    if data.get("kind") != "xfactory_intake_template":
        errors.append(f"{path.relative_to(ROOT)} kind must be xfactory_intake_template")

    template = data.get("template")
    if not isinstance(template, dict) or not template.get("id") or not template.get("recommended_factory_repo"):
        errors.append(f"{path.relative_to(ROOT)} template must include id and recommended_factory_repo")

    taxonomy = data.get("taxonomy_defaults")
    if not isinstance(taxonomy, dict):
        errors.append(f"{path.relative_to(ROOT)} taxonomy_defaults must be a mapping")
    else:
        for key in sorted(REQUIRED_TAXONOMY_KEYS - set(taxonomy)):
            errors.append(f"{path.relative_to(ROOT)} taxonomy_defaults missing: {key}")

    profiles = data.get("supported_profiles")
    if not isinstance(profiles, list) or not profiles:
        errors.append(f"{path.relative_to(ROOT)} supported_profiles must contain at least one profile")
    else:
        for profile in profiles:
            if not isinstance(profile, dict):
                errors.append(f"{path.relative_to(ROOT)} supported_profiles entries must be mappings")
                continue
            for key in [
                "id",
                "factory_subtype",
                "target_domain",
                "target_domain_subtype",
                "client_types",
                "customer_subject_types",
                "starter_workflows",
                "credential_families",
                "high_risk_boundaries",
            ]:
                if key not in profile:
                    errors.append(f"{path.relative_to(ROOT)} profile {profile.get('id', '<unknown>')} missing {key}")

    for workflow in data.get("common_workflows") or []:
        if not isinstance(workflow, dict):
            errors.append(f"{path.relative_to(ROOT)} common_workflows entries must be mappings")
            continue
        mode = workflow.get("required_mix_mode")
        if mode not in ALLOWED_MIX_MODES:
            errors.append(
                f"{path.relative_to(ROOT)} workflow {workflow.get('id', '<unknown>')} has invalid mix mode: {mode}"
            )

    credential_ids = set()
    for family in data.get("credential_families") or []:
        if isinstance(family, dict) and family.get("id"):
            credential_ids.add(str(family["id"]))
        else:
            errors.append(f"{path.relative_to(ROOT)} credential_families entries must include id")

    for profile in profiles if isinstance(profiles, list) else []:
        if not isinstance(profile, dict):
            continue
        for family_id in profile.get("credential_families") or []:
            if family_id not in credential_ids:
                errors.append(
                    f"{path.relative_to(ROOT)} profile {profile.get('id')} references unknown credential family: {family_id}"
                )

    return errors


def validate_subtype_catalog(index_entries: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    path = TEMPLATE_DIR / "subtypes" / "catalog.yaml"
    if not path.exists():
        return [f"{path.relative_to(ROOT)} missing"]

    data = load_yaml(path)
    if data.get("kind") != "xfactory_intake_subtype_catalog":
        errors.append(f"{path.relative_to(ROOT)} kind must be xfactory_intake_subtype_catalog")

    indexed_template_ids = {str(entry.get("id")) for entry in index_entries if isinstance(entry, dict)}
    catalog = data.get("catalog")
    if not isinstance(catalog, list):
        errors.append(f"{path.relative_to(ROOT)} catalog must be a list")
        return errors

    seen_template_ids: set[str] = set()
    seen_subtype_ids: set[str] = set()
    for group in catalog:
        if not isinstance(group, dict):
            errors.append(f"{path.relative_to(ROOT)} catalog entries must be mappings")
            continue
        template_id = str(group.get("template_id") or "")
        if not template_id:
            errors.append(f"{path.relative_to(ROOT)} catalog entry missing template_id")
            continue
        seen_template_ids.add(template_id)
        if template_id not in indexed_template_ids:
            errors.append(f"{path.relative_to(ROOT)} template_id not found in index: {template_id}")
        subtypes = group.get("subtypes")
        if not isinstance(subtypes, list):
            errors.append(f"{path.relative_to(ROOT)} {template_id} subtypes must be a list")
            continue
        if len(subtypes) != 10:
            errors.append(f"{path.relative_to(ROOT)} {template_id} must define exactly 10 subtypes, found {len(subtypes)}")
        for subtype in subtypes:
            if not isinstance(subtype, dict):
                errors.append(f"{path.relative_to(ROOT)} {template_id} subtype entries must be mappings")
                continue
            subtype_id = str(subtype.get("id") or "")
            if not subtype_id:
                errors.append(f"{path.relative_to(ROOT)} {template_id} subtype missing id")
                continue
            if subtype_id in seen_subtype_ids:
                errors.append(f"{path.relative_to(ROOT)} duplicate subtype id: {subtype_id}")
            seen_subtype_ids.add(subtype_id)
            for key in sorted(REQUIRED_SUBTYPE_KEYS - set(subtype)):
                errors.append(f"{path.relative_to(ROOT)} subtype {subtype_id} missing {key}")
            for key in [
                "client_types",
                "customer_subject_types",
                "starter_workflows",
                "credential_families",
                "adapter_families",
                "high_risk_boundaries",
                "recommended_questions",
                "runtime_binding_focus",
            ]:
                value = subtype.get(key)
                if not isinstance(value, list) or not value:
                    errors.append(f"{path.relative_to(ROOT)} subtype {subtype_id} {key} must be a non-empty list")
            mix_defaults = subtype.get("hermes_mixture_defaults")
            if not isinstance(mix_defaults, dict) or not mix_defaults:
                errors.append(f"{path.relative_to(ROOT)} subtype {subtype_id} hermes_mixture_defaults must be a mapping")
            else:
                for mix_name, mode in mix_defaults.items():
                    if mode not in ALLOWED_MIX_MODES:
                        errors.append(
                            f"{path.relative_to(ROOT)} subtype {subtype_id} mix {mix_name} has invalid mode: {mode}"
                        )

    missing_template_ids = indexed_template_ids - seen_template_ids
    for template_id in sorted(missing_template_ids):
        errors.append(f"{path.relative_to(ROOT)} missing subtype group for template: {template_id}")

    return errors


def main() -> int:
    errors: list[str] = []
    index = load_yaml(TEMPLATE_DIR / "index.yaml")
    entries = index.get("templates")
    if not isinstance(entries, list) or not entries:
        errors.append("templates/intake/index.yaml must contain templates")
    else:
        for entry in entries:
            if not isinstance(entry, dict) or not entry.get("file"):
                errors.append("templates/intake/index.yaml template entries must include file")
                continue
            path = TEMPLATE_DIR / str(entry["file"])
            if not path.exists():
                errors.append(f"templates/intake/index.yaml references missing file: {entry['file']}")
                continue
            errors.extend(validate_template(path))
        errors.extend(validate_subtype_catalog(entries))

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK xFactory intake templates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
