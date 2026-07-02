#!/usr/bin/env python3
"""Validate the xFactory installation spine and overlay examples."""

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
SPINE_PATH = ROOT / "templates" / "installation" / "openxfactory-installation-spine.yaml"
EXAMPLES_PATH = ROOT / "examples" / "installation" / "domain-overlay-examples.yaml"

REQUIRED_STAGE_IDS = [
    "install_scope",
    "domain_resolution",
    "source_access_consent",
    "source_inventory",
    "current_state_inference",
    "workflow_definition_packet",
    "user_validation_walkthrough",
    "best_practice_comparison",
    "migration_plan",
    "workflow_change_consent",
    "target_workflow_generation",
    "dry_run_cutover",
    "drift_monitoring",
]

ALLOWED_OPERATIONS = {"supplement", "replace", "constrain", "veto"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def validate_spine() -> list[str]:
    errors: list[str] = []
    data = load_yaml(SPINE_PATH)

    if data.get("kind") != "xfactory_open_installation_spine":
        errors.append(f"{rel(SPINE_PATH)} kind must be xfactory_open_installation_spine")

    for key in [
        "template",
        "layering",
        "nonreplaceable_controls",
        "overlay_operations",
        "stages",
        "artifact_families",
        "generic_product_service_defaults",
    ]:
        if key not in data:
            errors.append(f"{rel(SPINE_PATH)} missing top-level key: {key}")

    stages = data.get("stages")
    if not isinstance(stages, list):
        errors.append(f"{rel(SPINE_PATH)} stages must be a list")
        return errors

    seen_ids: list[str] = []
    for index, stage in enumerate(stages, start=1):
        if not isinstance(stage, dict):
            errors.append(f"{rel(SPINE_PATH)} stage {index} must be a mapping")
            continue
        stage_id = str(stage.get("id") or "")
        seen_ids.append(stage_id)
        if stage.get("sequence") != index:
            errors.append(f"{rel(SPINE_PATH)} stage {stage_id or index} sequence must be {index}")
        for key in [
            "openxfactory_responsibility",
            "allowed_overlay_operations",
            "required_artifacts",
            "validation_rules",
        ]:
            if key not in stage:
                errors.append(f"{rel(SPINE_PATH)} stage {stage_id or index} missing {key}")
        operations = stage.get("allowed_overlay_operations")
        if not isinstance(operations, list) or not operations:
            errors.append(f"{rel(SPINE_PATH)} stage {stage_id or index} must allow at least one overlay operation")
        else:
            for operation in operations:
                if operation not in ALLOWED_OPERATIONS:
                    errors.append(f"{rel(SPINE_PATH)} stage {stage_id} invalid operation: {operation}")

    if seen_ids != REQUIRED_STAGE_IDS:
        errors.append(f"{rel(SPINE_PATH)} stages must match required installation spine stage order")

    artifact_ids = {
        str(item.get("id"))
        for item in data.get("artifact_families") or []
        if isinstance(item, dict) and item.get("id")
    }
    for stage in stages:
        if not isinstance(stage, dict):
            continue
        for artifact_id in stage.get("required_artifacts") or []:
            if artifact_id not in artifact_ids:
                errors.append(f"{rel(SPINE_PATH)} stage {stage.get('id')} references unknown artifact: {artifact_id}")

    return errors


def validate_examples() -> list[str]:
    errors: list[str] = []
    data = load_yaml(EXAMPLES_PATH)

    if data.get("kind") != "xfactory_domain_installation_overlay_examples":
        errors.append(f"{rel(EXAMPLES_PATH)} kind must be xfactory_domain_installation_overlay_examples")

    examples = data.get("examples")
    if not isinstance(examples, list) or not examples:
        errors.append(f"{rel(EXAMPLES_PATH)} examples must contain at least one overlay")
        return errors

    required_top_level = {"overlay", "compatibility", "stage_overrides", "artifact_bindings", "validation"}
    for example in examples:
        if not isinstance(example, dict):
            errors.append(f"{rel(EXAMPLES_PATH)} example entries must be mappings")
            continue
        example_id = str(example.get("id") or "<unknown>")
        for key in sorted(required_top_level - set(example)):
            errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} missing {key}")

        compatibility = example.get("compatibility")
        if not isinstance(compatibility, dict):
            errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} compatibility must be a mapping")
        else:
            supported = compatibility.get("supported_stage_ids")
            if supported != REQUIRED_STAGE_IDS:
                errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} supported_stage_ids must match the spine")

        overrides = example.get("stage_overrides")
        if not isinstance(overrides, list) or not overrides:
            errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} must define stage_overrides")
            continue

        for override in overrides:
            if not isinstance(override, dict):
                errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} stage override must be a mapping")
                continue
            stage_id = str(override.get("stage_id") or "")
            operation = override.get("operation")
            if stage_id not in REQUIRED_STAGE_IDS:
                errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} unknown stage_id: {stage_id}")
            if operation not in ALLOWED_OPERATIONS:
                errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} invalid operation: {operation}")
            if not override.get("reason"):
                errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} override {stage_id} missing reason")
            if override.get("emits_openxfactory_artifacts") is not True:
                errors.append(
                    f"{rel(EXAMPLES_PATH)} example {example_id} override {stage_id} must emit openxFactory artifacts"
                )
            if operation == "replace" and not override.get("approval_rule_ref"):
                errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} replace override {stage_id} needs approval_rule_ref")
            if operation == "veto":
                if not override.get("blocking_condition"):
                    errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} veto override {stage_id} needs blocking_condition")
                if not override.get("resolution_path"):
                    errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} veto override {stage_id} needs resolution_path")

        validation = example.get("validation")
        if not isinstance(validation, dict):
            errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} validation must be a mapping")
        else:
            for key in [
                "nonreplaceable_controls_acknowledged",
                "stricter_rule_wins",
                "replacement_requires_same_artifact_family",
            ]:
                if validation.get(key) is not True:
                    errors.append(f"{rel(EXAMPLES_PATH)} example {example_id} validation.{key} must be true")

    return errors


def main() -> int:
    errors = validate_spine() + validate_examples()
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK xFactory installation templates")
    return 0


if __name__ == "__main__":
    sys.exit(main())

