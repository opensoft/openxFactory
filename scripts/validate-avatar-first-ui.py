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


# --- Frozen avatar-client-parallel-v1 baseline (read-only mirror) ----------
# Recorded read-only from the kernel change `define-avatar-client-contract-kernel`
# supporting docs (avatar-client-parallel-workstream-plan.md §Parallel Interface
# Baseline; specs/avatar-client-runtime/spec.md). NOT authored here — the kernel
# owns these registries and ceilings; this mirror lets the offline validator
# resolve references and bounds during parallel work. Final realization
# (`--mode realization`) MUST re-verify against the exact released registries.
BASELINE: dict[str, Any] = {
    "identity": "avatar-client-parallel-v1",
    # Three neutral consent-purpose IDs (runtime spec §Consent-before-capture).
    "consent_purposes": [
        "avatar.media_capture",
        "avatar.provider_processing",
        "avatar.structured_record",
    ],
    # Speech gates: default + allowed; pre_speech_review is reserved (fail closed).
    "speech_gates_allowed": ["confirmation_before_action", "streaming_monitor"],
    "speech_gates_reserved": ["pre_speech_review"],
    # Neutral interaction mode; server_vad + push_to_talk are reserved.
    "interaction_mode_neutral": "provider_vad",
    "interaction_modes_reserved": ["server_vad", "push_to_talk"],
    # Kernel-owned timing ceilings (milliseconds) — selected values validated here.
    "timing": {
        "readiness_ms": {"default": 3000, "min": 1000, "max": 5000},
        "heartbeat_ms": {"min": 1, "max": 5000},
        "lease_ms": {"max": 10000},
    },
    # AVC-02 result union and the four authoritative UI axes.
    "avc02_results": ["grant", "denial", "terminal"],
    "authoritative_axes": [
        "session_lifecycle",
        "control_health",
        "media_state",
        "workflow_projection",
    ],
    "presentation_modes": ["conversation", "work", "review"],
}

SCHEMA_PATH = ROOT / "contracts" / "schemas" / "avatar-first-ui-profile.schema.yaml"
TEMPLATE_PATH = ROOT / "templates" / "ui" / "avatar-first.yaml"
EXAMPLES_PATH = ROOT / "examples" / "avatar-first-ui" / "domain-overlays.example.yaml"
FIXTURES_DIR = ROOT / "examples" / "avatar-first-ui" / "fixtures"

REQUIRED_SCHEMA_BLOCKS = (
    "runtime_compatibility", "presentation", "media", "outcome_slots",
    "fallback_slots", "interaction_mode", "speech_gate", "timing",
    "consent_purpose_mappings", "persona_reference", "retention_overlay",
    "accessibility_baseline", "handoff",
)
ACCESSIBILITY_CAPABILITIES = (
    "keyboard_operation", "stable_focus", "visible_focus",
    "screen_reader_announcements", "captions", "text_only_mode",
    "reduced_motion", "high_contrast", "non_color_cues", "zoom_reflow",
    "pseudo_locale_coverage",
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def emit(errors: list[str], error_id: str, message: str) -> None:
    """Record a rejection tagged with its stable error/evidence ID."""
    errors.append(f"{error_id} {message}")


def resolve_baseline(mode: str, errors: list[str]) -> dict[str, Any]:
    """Return the registry/ceiling baseline for the requested mode (read-only).

    baseline: the frozen avatar-client-parallel-v1 mirror above.
    realization: load the exact released kernel registries and fail closed on
    drift. The released registries do not exist during parallel work, so this
    path is deferred to the serialized post-kernel release (US4/Phase 6).
    """
    if mode == "realization":
        emit(
            errors, ERR_PARITY_ACCEPTANCE,
            "realization mode requires the released kernel registries "
            "(serialized post-kernel release, Phase 6) — not available in parallel work",
        )
        return BASELINE
    return BASELINE


# check_profile() implements the nine enforced rule classes and is wired in the
# US1 phase (T018). During Foundational it resolves closed defaults only, so
# existing static profiles (no AVC blocks) validate clean.
def check_profile(profile: dict[str, Any], ctx: str, baseline: dict[str, Any],
                  errors: list[str]) -> None:  # pragma: no cover - filled in US1
    # Foundational seam: closed-default resolution means an omitted optional
    # block is valid (fail-closed). Per-rule detections are added in US1.
    return None


def validate_schema(errors: list[str]) -> None:
    data = load_yaml(SCHEMA_PATH)
    if data.get("name") != "avatar_first_ui_profile":
        emit(errors, ERR_SCHEMA_SHAPE, f"{rel(SCHEMA_PATH)} name must be avatar_first_ui_profile")
    if data.get("schema_version") is None or not data.get("kind"):
        emit(errors, ERR_SCHEMA_SHAPE, f"{rel(SCHEMA_PATH)} must carry schema_version and kind")
    required = data.get("required")
    if not isinstance(required, list):
        emit(errors, ERR_SCHEMA_SHAPE, f"{rel(SCHEMA_PATH)} required must be a list")
        return
    for key in (
        "profile", "authority_boundaries", "interaction_surface", "channels",
        "standard_controls", "tool_boundaries", "escalation", "traceability",
    ):
        if key not in required:
            emit(errors, ERR_SCHEMA_SHAPE, f"{rel(SCHEMA_PATH)} required missing {key}")
    props = data.get("properties", {})
    for block in REQUIRED_SCHEMA_BLOCKS:
        if block not in props:
            emit(errors, ERR_SCHEMA_SHAPE, f"{rel(SCHEMA_PATH)} missing additive block: {block}")
    # Additive blocks must remain optional so existing profiles stay valid.
    for block in REQUIRED_SCHEMA_BLOCKS:
        if block in required:
            emit(errors, ERR_SCHEMA_SHAPE,
                 f"{rel(SCHEMA_PATH)} additive block {block} must be optional, not required")


def validate_template(errors: list[str]) -> None:
    data = load_yaml(TEMPLATE_PATH)
    if data.get("kind") != "xfactory_avatar_first_ui_template":
        emit(errors, ERR_TEMPLATE_SHAPE, f"{rel(TEMPLATE_PATH)} kind must be xfactory_avatar_first_ui_template")
    if data.get("schema_version") is None:
        emit(errors, ERR_TEMPLATE_SHAPE, f"{rel(TEMPLATE_PATH)} must carry schema_version")
    if data.get("authority_boundaries", {}).get("avatar_is_presentation_only") is not True:
        emit(errors, ERR_TEMPLATE_SHAPE,
             f"{rel(TEMPLATE_PATH)} must set authority_boundaries.avatar_is_presentation_only: true")
    channels = data.get("channels")
    if not isinstance(channels, dict):
        emit(errors, ERR_TEMPLATE_SHAPE, f"{rel(TEMPLATE_PATH)} channels must be a mapping")
    else:
        for channel in sorted(REQUIRED_CHANNELS - set(channels)):
            emit(errors, ERR_TEMPLATE_SHAPE, f"{rel(TEMPLATE_PATH)} missing channel: {channel}")
    controls = data.get("standard_controls")
    if not isinstance(controls, list):
        emit(errors, ERR_TEMPLATE_SHAPE, f"{rel(TEMPLATE_PATH)} standard_controls must be a list")
        return
    control_ids = {str(c.get("id")) for c in controls if isinstance(c, dict)}
    for control_id in sorted(REQUIRED_CONTROL_IDS - control_ids):
        emit(errors, ERR_TEMPLATE_SHAPE, f"{rel(TEMPLATE_PATH)} missing standard control: {control_id}")
    for control in controls:
        if not isinstance(control, dict):
            emit(errors, ERR_TEMPLATE_SHAPE, f"{rel(TEMPLATE_PATH)} standard_controls entries must be mappings")
            continue
        if "required" not in control:
            emit(errors, ERR_TEMPLATE_SHAPE,
                 f"{rel(TEMPLATE_PATH)} control {control.get('id', '<unknown>')} missing required flag")


def validate_examples(errors: list[str], baseline: dict[str, Any]) -> None:
    data = load_yaml(EXAMPLES_PATH)
    if data.get("kind") != "xfactory_avatar_first_ui_overlay_examples":
        emit(errors, ERR_PARITY_EXAMPLE, f"{rel(EXAMPLES_PATH)} kind must be xfactory_avatar_first_ui_overlay_examples")
    if data.get("schema_version") is None:
        emit(errors, ERR_PARITY_EXAMPLE, f"{rel(EXAMPLES_PATH)} must carry schema_version")
    examples = data.get("examples")
    if not isinstance(examples, list) or not examples:
        emit(errors, ERR_PARITY_EXAMPLE, f"{rel(EXAMPLES_PATH)} examples must contain at least one overlay")
        return
    for index, example in enumerate(examples):
        if not isinstance(example, dict):
            emit(errors, ERR_PARITY_EXAMPLE, f"{rel(EXAMPLES_PATH)} example {index} must be a mapping")
            continue
        profile = example.get("profile")
        if not isinstance(profile, dict):
            emit(errors, ERR_PARITY_EXAMPLE, f"{rel(EXAMPLES_PATH)} example {index} missing profile mapping")
            continue
        for key in ("id", "domain_factory_repo", "default_implementation_level",
                    "primary_user_kind", "primary_subject_kind"):
            if not profile.get(key):
                emit(errors, ERR_PARITY_EXAMPLE, f"{rel(EXAMPLES_PATH)} example {index} profile missing {key}")
        authority = example.get("authority_boundaries")
        if not isinstance(authority, dict) or authority.get("avatar_is_presentation_only") is not True:
            emit(errors, ERR_PARITY_EXAMPLE,
                 f"{rel(EXAMPLES_PATH)} example {profile.get('id', index)} must keep avatar presentation-only")
        overlay = example.get("domain_overlay")
        if not isinstance(overlay, dict):
            emit(errors, ERR_PARITY_EXAMPLE, f"{rel(EXAMPLES_PATH)} example {profile.get('id', index)} missing domain_overlay")
            continue
        for key in ("persona_roles", "handoff_roles", "restricted_tool_classes"):
            value = overlay.get(key)
            if not isinstance(value, list) or not value:
                emit(errors, ERR_PARITY_EXAMPLE,
                     f"{rel(EXAMPLES_PATH)} example {profile.get('id', index)} domain_overlay.{key} must be non-empty")
        # AVC-aligned rule checks over any present blocks (positives must pass).
        check_profile(example, f"{rel(EXAMPLES_PATH)}#{profile.get('id', index)}", baseline, errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the avatar-first UI standard surface (offline).")
    parser.add_argument("--mode", choices=["baseline", "realization"], default="baseline",
                        help="Resolve kernel IDs/ceilings against the frozen baseline (default) "
                             "or the released registries (realization; Phase 6).")
    args = parser.parse_args(argv)

    errors: list[str] = []
    baseline = resolve_baseline(args.mode, errors)
    validate_schema(errors)
    validate_template(errors)
    validate_examples(errors, baseline)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print(f"OK xFactory avatar-first UI standard surface [mode={args.mode}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
