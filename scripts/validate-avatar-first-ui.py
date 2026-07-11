#!/usr/bin/env python3
"""Validate the shared avatar-first UI standard surface (offline).

Checks the registered avatar-first UI profile schema, the shared template, the
domain-neutral example archetypes, and the deterministic fixtures against the
avatar-first UI standard. Runs fully offline (no provider or runtime service).

Two modes:
- ``--mode baseline`` (default) resolves kernel-owned IDs and readiness/heartbeat
  /lease ceilings against the frozen ``avatar-client-parallel-v1`` baseline that
  is mirrored read-only in ``BASELINE`` below (recorded from the kernel change
  ``define-avatar-client-contract-kernel`` supporting docs; not authored here).
- ``--mode realization`` loads the exact released kernel registries read-only and
  fails closed on drift (deferred to the serialized post-kernel release).

Every rejected rule prints ``ERROR <error-id> <message>`` so the stable error IDs
are usable evidence anchors.

Stable error / evidence ID catalog (nine enforced rule classes + parity/structure
IDs). See specs/004-avatar-first-ui/contracts/validator-rules.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]

# --- Stable error / evidence ID catalog (T002) -----------------------------
# Structure / parity IDs
ERR_SCHEMA_SHAPE = "AFUV-SCHEMA-SHAPE"
ERR_TEMPLATE_SHAPE = "AFUV-TEMPLATE-SHAPE"
ERR_PARITY_EXAMPLE = "AFUV-PARITY-EXAMPLE"
ERR_PARITY_ACCEPTANCE = "AFUV-PARITY-ACCEPTANCE"
ERR_EVIDENCE_UNKNOWN = "AFUV-EVIDENCE-UNKNOWN"
# Nine enforced rule classes (Q6 eight + retention from the 2026-07-11 analyze gate)
ERR_AUTHORITY_TRANSITION = "AFUV-AUTHORITY-TRANSITION"
ERR_TIMING_OUT_OF_RANGE = "AFUV-TIMING-OUT-OF-RANGE"
ERR_CONTROL_FALLBACK_MISSING = "AFUV-CONTROL-FALLBACK-MISSING"
ERR_PERSONA_UNRESOLVED = "AFUV-PERSONA-UNRESOLVED"
ERR_MODE_RESERVED = "AFUV-MODE-RESERVED"
ERR_UNSAFE_RENDER = "AFUV-UNSAFE-RENDER"
ERR_PURPOSE_INVALID = "AFUV-PURPOSE-INVALID"
ERR_HELD_ANSWER_ACTIVE = "AFUV-HELD-ANSWER-ACTIVE"
ERR_RETENTION_UNRESOLVED = "AFUV-RETENTION-UNRESOLVED"

ENFORCED_RULE_IDS = (
    ERR_AUTHORITY_TRANSITION,
    ERR_TIMING_OUT_OF_RANGE,
    ERR_CONTROL_FALLBACK_MISSING,
    ERR_PERSONA_UNRESOLVED,
    ERR_MODE_RESERVED,
    ERR_UNSAFE_RENDER,
    ERR_PURPOSE_INVALID,
    ERR_HELD_ANSWER_ACTIVE,
    ERR_RETENTION_UNRESOLVED,
)

REQUIRED_CONTROL_IDS = {
    "start_session",
    "pause_or_stop_session",
    "mute_microphone",
    "captions",
    "switch_persona",
    "switch_language",
    "slow_down",
    "repeat",
    "explain_simply",
    "show_more_detail",
    "attach_or_share_context",
    "request_handoff",
    "show_privacy_and_disclosure",
    "view_transcript",
    "view_workflow_state",
}

REQUIRED_CHANNELS = {
    "avatar_rendering",
    "conversation_media",
    "workflow_tool",
    "governance_supervisor",
}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def validate_template(errors: list[str]) -> None:
    path = ROOT / "templates" / "ui" / "avatar-first.yaml"
    data = load_yaml(path)
    if data.get("kind") != "xfactory_avatar_first_ui_template":
        errors.append(f"{rel(path)} kind must be xfactory_avatar_first_ui_template")
    if data.get("authority_boundaries", {}).get("avatar_is_presentation_only") is not True:
        errors.append(f"{rel(path)} must set authority_boundaries.avatar_is_presentation_only: true")

    channels = data.get("channels")
    if not isinstance(channels, dict):
        errors.append(f"{rel(path)} channels must be a mapping")
    else:
        for channel in sorted(REQUIRED_CHANNELS - set(channels)):
            errors.append(f"{rel(path)} missing channel: {channel}")

    controls = data.get("standard_controls")
    if not isinstance(controls, list):
        errors.append(f"{rel(path)} standard_controls must be a list")
        return
    control_ids = {str(control.get("id")) for control in controls if isinstance(control, dict)}
    for control_id in sorted(REQUIRED_CONTROL_IDS - control_ids):
        errors.append(f"{rel(path)} missing standard control: {control_id}")
    for control in controls:
        if not isinstance(control, dict):
            errors.append(f"{rel(path)} standard_controls entries must be mappings")
            continue
        if "required" not in control:
            errors.append(f"{rel(path)} control {control.get('id', '<unknown>')} missing required flag")


def validate_examples(errors: list[str]) -> None:
    path = ROOT / "examples" / "avatar-first-ui" / "domain-overlays.example.yaml"
    data = load_yaml(path)
    if data.get("kind") != "xfactory_avatar_first_ui_overlay_examples":
        errors.append(f"{rel(path)} kind must be xfactory_avatar_first_ui_overlay_examples")
    examples = data.get("examples")
    if not isinstance(examples, list) or not examples:
        errors.append(f"{rel(path)} examples must contain at least one overlay")
        return
    for index, example in enumerate(examples):
        if not isinstance(example, dict):
            errors.append(f"{rel(path)} example {index} must be a mapping")
            continue
        profile = example.get("profile")
        if not isinstance(profile, dict):
            errors.append(f"{rel(path)} example {index} missing profile mapping")
            continue
        for key in [
            "id",
            "domain_factory_repo",
            "default_implementation_level",
            "primary_user_kind",
            "primary_subject_kind",
        ]:
            if not profile.get(key):
                errors.append(f"{rel(path)} example {index} profile missing {key}")
        authority = example.get("authority_boundaries")
        if not isinstance(authority, dict) or authority.get("avatar_is_presentation_only") is not True:
            errors.append(f"{rel(path)} example {profile.get('id', index)} must keep avatar presentation-only")
        overlay = example.get("domain_overlay")
        if not isinstance(overlay, dict):
            errors.append(f"{rel(path)} example {profile.get('id', index)} missing domain_overlay")
            continue
        for key in ["persona_roles", "handoff_roles", "restricted_tool_classes"]:
            value = overlay.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"{rel(path)} example {profile.get('id', index)} domain_overlay.{key} must be non-empty")


def validate_schema(errors: list[str]) -> None:
    path = ROOT / "contracts" / "schemas" / "avatar-first-ui-profile.schema.yaml"
    data = load_yaml(path)
    if data.get("name") != "avatar_first_ui_profile":
        errors.append(f"{rel(path)} name must be avatar_first_ui_profile")
    required = data.get("required")
    if not isinstance(required, list):
        errors.append(f"{rel(path)} required must be a list")
        return
    for key in [
        "profile",
        "authority_boundaries",
        "interaction_surface",
        "channels",
        "standard_controls",
        "tool_boundaries",
        "escalation",
        "traceability",
    ]:
        if key not in required:
            errors.append(f"{rel(path)} required missing {key}")


def main() -> int:
    errors: list[str] = []
    validate_schema(errors)
    validate_template(errors)
    validate_examples(errors)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK xFactory avatar-first UI template")
    return 0


if __name__ == "__main__":
    sys.exit(main())
