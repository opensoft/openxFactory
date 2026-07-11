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
ERR_FIXTURE_EXPECT = "AFUV-FIXTURE-EXPECT"
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


SAFE_RENDER_MODES = {"plain_text", "narrow_sanitized"}
UNSAFE_TEXT_MARKERS = ("<script", "<iframe", "<img", "javascript:", "data:text/html", "onerror=", "vbscript:")
SECRET_MARKERS = ("token=", "secret", "apikey", "api_key", "bearer", "password", "key=", "@")


def _looks_secret(value: str) -> bool:
    low = value.lower()
    return any(marker in low for marker in SECRET_MARKERS)


def _has_unsafe_text(node: Any) -> bool:
    if isinstance(node, str):
        low = node.lower()
        return any(marker in low for marker in UNSAFE_TEXT_MARKERS)
    if isinstance(node, dict):
        return any(_has_unsafe_text(v) for v in node.values())
    if isinstance(node, list):
        return any(_has_unsafe_text(v) for v in node)
    return False


def check_profile(candidate: dict[str, Any], ctx: str, baseline: dict[str, Any],
                  errors: list[str]) -> None:
    """Enforce the nine rule classes over a profile candidate's AVC blocks.

    Omitted optional blocks are valid (fail-closed). Positive profiles emit no
    errors; each negative fixture triggers exactly one enforced rule.
    """
    if not isinstance(candidate, dict):
        return

    # 1) Presentation must not author an authoritative axis transition (FR-001/016)
    ab = candidate.get("authority_boundaries", {})
    pres = candidate.get("presentation", {})
    if ab.get("avatar_is_presentation_only") is False or (
            isinstance(pres, dict) and pres.get("authors_authoritative_state")):
        emit(errors, ERR_AUTHORITY_TRANSITION,
             f"{ctx}: presentation must not author an authoritative axis transition")

    # 2) Selected timing within kernel-owned ceilings (FR-013/026)
    timing = candidate.get("timing")
    if isinstance(timing, dict):
        tb = baseline["timing"]
        r = timing.get("readiness_ms")
        if isinstance(r, int) and (r < tb["readiness_ms"]["min"] or r > tb["readiness_ms"]["max"]):
            emit(errors, ERR_TIMING_OUT_OF_RANGE,
                 f"{ctx}: readiness_ms {r} outside kernel ceiling "
                 f"[{tb['readiness_ms']['min']},{tb['readiness_ms']['max']}]")
        h = timing.get("heartbeat_ms")
        if isinstance(h, int) and (h < tb["heartbeat_ms"]["min"] or h > tb["heartbeat_ms"]["max"]):
            emit(errors, ERR_TIMING_OUT_OF_RANGE,
                 f"{ctx}: heartbeat_ms {h} outside kernel ceiling "
                 f"[{tb['heartbeat_ms']['min']},{tb['heartbeat_ms']['max']}]")
        lease = timing.get("lease_ms")
        if isinstance(lease, int) and lease > tb["lease_ms"]["max"]:
            emit(errors, ERR_TIMING_OUT_OF_RANGE,
                 f"{ctx}: lease_ms {lease} exceeds kernel ceiling {tb['lease_ms']['max']}")

    # 3) Required-control fallback (FR-007)
    for control in candidate.get("standard_controls", []) or []:
        if isinstance(control, dict) and control.get("required") is False and not control.get("fallback"):
            emit(errors, ERR_CONTROL_FALLBACK_MISSING,
                 f"{ctx}: control {control.get('id')} is not required but declares no fallback")

    # 4) Persona reference resolvable + non-secret locator (FR-011)
    pr = candidate.get("persona_reference")
    if isinstance(pr, dict):
        if not pr.get("persona_id") or pr.get("version") in (None, ""):
            emit(errors, ERR_PERSONA_UNRESOLVED,
                 f"{ctx}: persona_reference must carry a resolvable persona_id and version")
        locator = pr.get("catalog_locator")
        if isinstance(locator, str) and _looks_secret(locator):
            emit(errors, ERR_PERSONA_UNRESOLVED,
                 f"{ctx}: persona catalog_locator must be non-secret")

    # 5) Reserved/forbidden interaction mode or speech gate needs a fallback (FR-015)
    im = candidate.get("interaction_mode", {})
    if isinstance(im, dict) and im.get("value") in baseline["interaction_modes_reserved"] and not im.get("fallback"):
        emit(errors, ERR_MODE_RESERVED,
             f"{ctx}: reserved interaction mode {im.get('value')} requires a text/handoff fallback")
    sg = candidate.get("speech_gate", {})
    if isinstance(sg, dict) and sg.get("value") in baseline["speech_gates_reserved"] and not sg.get("fallback"):
        emit(errors, ERR_MODE_RESERVED,
             f"{ctx}: reserved speech gate {sg.get('value')} requires a text/handoff fallback")

    # 6) Safe rendering of untrusted content (FR-012)
    rendering = candidate.get("rendering")
    if isinstance(rendering, dict):
        mode = rendering.get("mode")
        if mode is not None and mode not in SAFE_RENDER_MODES:
            emit(errors, ERR_UNSAFE_RENDER,
                 f"{ctx}: rendering.mode {mode!r} must be one of {sorted(SAFE_RENDER_MODES)}")
    if _has_unsafe_text(candidate):
        emit(errors, ERR_UNSAFE_RENDER, f"{ctx}: unsafe markup or URI scheme found in rendered text")

    # 7) Consent-purpose mappings reference neutral IDs (FR-014)
    for mapping in candidate.get("consent_purpose_mappings", []) or []:
        if isinstance(mapping, dict):
            ref = mapping.get("purpose_ref")
            if ref not in baseline["consent_purposes"]:
                emit(errors, ERR_PURPOSE_INVALID,
                     f"{ctx}: consent purpose_ref {ref!r} is not a neutral consent-purpose ID")

    # 8) Held answer never rendered active (FR-008/009)
    media = candidate.get("media")
    if isinstance(media, dict):
        held = media.get("held_answer_state")
        if held is not None and held not in ("connecting", "pending"):
            emit(errors, ERR_HELD_ANSWER_ACTIVE,
                 f"{ctx}: held_answer_state {held!r} must be connecting|pending, never active")

    # 9) Retention overlay references resolve; no inline policy (FR-027)
    ro = candidate.get("retention_overlay")
    if isinstance(ro, dict):
        refs = ro.get("policy_refs")
        if refs is not None and (not refs or any((not isinstance(x, str) or not x.strip()) for x in refs)):
            emit(errors, ERR_RETENTION_UNRESOLVED,
                 f"{ctx}: retention_overlay policy_refs must be non-empty resolvable IDs")
        for forbidden in ("duration_days", "duration", "policy_text", "consent_evidence"):
            if forbidden in ro:
                emit(errors, ERR_RETENTION_UNRESOLVED,
                     f"{ctx}: retention_overlay must not carry inline {forbidden}")


def check_closed_defaults(errors: list[str]) -> None:
    """SC-004 — confirm the schema's new-field defaults are closed (fail-closed)."""
    data = load_yaml(SCHEMA_PATH)
    props = data.get("properties", {})
    expected = {
        ("presentation", "surface_default"): "conversation",
        ("media", "held_answer_state"): "connecting",
        ("interaction_mode", "value"): "provider_vad",
        ("speech_gate", "value"): "confirmation_before_action",
    }
    for (block, field), closed in expected.items():
        default = props.get(block, {}).get("properties", {}).get(field, {}).get("default")
        if default != closed:
            emit(errors, ERR_SCHEMA_SHAPE,
                 f"{rel(SCHEMA_PATH)} {block}.{field} default {default!r} must be closed default {closed!r}")
    acc = props.get("accessibility_baseline", {}).get("properties", {})
    for cap in ACCESSIBILITY_CAPABILITIES:
        if acc.get(cap, {}).get("default") is not False:
            emit(errors, ERR_SCHEMA_SHAPE,
                 f"{rel(SCHEMA_PATH)} accessibility_baseline.{cap} must default to false (closed)")


def check_fixture_meta(fixture: dict[str, Any], path: Path, errors: list[str]) -> None:
    if fixture.get("schema_version") is None or fixture.get("kind") != "xfactory_avatar_first_ui_fixture":
        emit(errors, ERR_SCHEMA_SHAPE,
             f"{rel(path)} fixture must carry schema_version and kind: xfactory_avatar_first_ui_fixture")
    if not fixture.get("fixture_id"):
        emit(errors, ERR_SCHEMA_SHAPE, f"{rel(path)} fixture missing fixture_id")


def validate_fixtures(errors: list[str], baseline: dict[str, Any]) -> None:
    """Compatibility fixtures validate clean; each negative fixture fails exactly
    its declared primary rule (Q6 + retention disposition)."""
    neg_dir = FIXTURES_DIR / "negative"
    for path in sorted(neg_dir.glob("*.yaml")) if neg_dir.is_dir() else []:
        fixture = load_yaml(path)
        check_fixture_meta(fixture, path, errors)
        expect = fixture.get("expect_error")
        candidate = fixture.get("candidate", {})
        local: list[str] = []
        check_profile(candidate, rel(path), baseline, local)
        fired = {line.split(" ", 1)[0] for line in local}
        enforced_fired = fired & set(ENFORCED_RULE_IDS)
        if expect not in fired:
            emit(errors, ERR_FIXTURE_EXPECT,
                 f"{rel(path)} expected {expect} but validator fired {sorted(fired) or 'nothing'}")
        elif enforced_fired != {expect}:
            emit(errors, ERR_FIXTURE_EXPECT,
                 f"{rel(path)} must fail exactly one primary rule {expect}, but fired {sorted(enforced_fired)}")

    comp_dir = FIXTURES_DIR / "compatibility"
    for path in sorted(comp_dir.glob("*.yaml")) if comp_dir.is_dir() else []:
        fixture = load_yaml(path)
        check_fixture_meta(fixture, path, errors)
        candidate = fixture.get("candidate", {})
        local = []
        check_profile(candidate, rel(path), baseline, local)
        if local:
            emit(errors, ERR_PARITY_EXAMPLE,
                 f"{rel(path)} compatibility fixture must validate clean, but fired "
                 f"{sorted({line.split(' ', 1)[0] for line in local})}")


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
    check_closed_defaults(errors)
    validate_template(errors)
    validate_examples(errors, baseline)
    validate_fixtures(errors, baseline)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print(f"OK xFactory avatar-first UI standard surface [mode={args.mode}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
