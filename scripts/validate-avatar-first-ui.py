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
import hashlib
import re
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
# Realization drift (--mode realization): released kernel diverged from the frozen
# baseline mirror, or a profile's runtime_compatibility fails content-addressing.
ERR_RUNTIME_DRIFT = "AFUV-RUNTIME-DRIFT"
ERR_EVIDENCE_UNKNOWN = "AFUV-EVIDENCE-UNKNOWN"
ERR_FIXTURE_EXPECT = "AFUV-FIXTURE-EXPECT"
ERR_ACCESSIBILITY_INVALID = "AFUV-ACCESSIBILITY-INVALID"
ERR_DETERMINISM_SHAPE = "AFUV-DETERMINISM-SHAPE"
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

# Released avatar-client (AVC) kernel files read read-only at --mode realization
# (FR-021/FR-025). The UI standard OWNS none of these; it verifies the frozen
# baseline mirror against them and fails closed on drift.
MANIFEST_PATH = ROOT / "contracts" / "manifest.yaml"
AVC_DIR = ROOT / "contracts" / "avatar-client"
RELEASED_INTERFACE_LOCK = AVC_DIR / "interface-lock.yaml"
RELEASED_SHARED_DEFS = AVC_DIR / "shared-definitions.schema.yaml"
RELEASED_AVC02 = AVC_DIR / "avc-02-session-result.schema.yaml"
RELEASED_AVC12 = AVC_DIR / "avc-12-state-snapshot.schema.yaml"
RELEASED_CONSENT = AVC_DIR / "registries" / "consent-purposes.registry.yaml"
RELEASED_IMODES = AVC_DIR / "registries" / "interaction-modes.registry.yaml"

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


def digest_file(path: Path) -> str:
    """sha256 over exact bytes — identical algorithm to validate-avatar-client.py."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_baseline(mode: str, errors: list[str]) -> dict[str, Any]:
    """Return the registry/ceiling baseline for the requested mode (read-only).

    baseline: the frozen avatar-client-parallel-v1 mirror above.
    realization: load the exact released kernel files read-only and VERIFY every
    frozen-baseline claim against their actual bytes, failing closed
    (AFUV-RUNTIME-DRIFT) on any divergence between the parallel mirror and the
    released IDs/ceilings. Returns the verified baseline (identical to BASELINE
    when there is no drift, so downstream per-profile verdicts are unchanged).
    """
    if mode == "realization":
        return _verify_released_baseline(errors)
    return BASELINE


def _load_released(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        emit(errors, ERR_RUNTIME_DRIFT,
             f"released kernel file not found: {rel(path)} (cannot verify baseline — fail closed)")
        return None
    return load_yaml(path)


def _verify_released_baseline(errors: list[str]) -> dict[str, Any]:
    """Verify the frozen BASELINE mirror against the released kernel bytes.

    This is a VERIFICATION pass, not an independent re-derivation: each frozen
    claim (IDs, ceilings, reserved/allowed sets) is asserted against the exact
    released files and any divergence fails closed. `timeouts_ms`,
    `closed_defaults`, and `result_kinds` live under the interface-lock `frozen`
    block (not the document root).
    """
    ilock = _load_released(RELEASED_INTERFACE_LOCK, errors)
    consent = _load_released(RELEASED_CONSENT, errors)
    imodes = _load_released(RELEASED_IMODES, errors)
    shared = _load_released(RELEASED_SHARED_DEFS, errors)
    avc02 = _load_released(RELEASED_AVC02, errors)
    avc12 = _load_released(RELEASED_AVC12, errors)
    if None in (ilock, consent, imodes, shared, avc02, avc12):
        return BASELINE  # a missing file already emitted drift → whole run fails closed

    defs = shared.get("$defs") or {}
    frozen = ilock.get("frozen") or {}
    closed = frozen.get("closed_defaults") or {}

    # identity <- interface_baseline (document root)
    if ilock.get("interface_baseline") != BASELINE["identity"]:
        emit(errors, ERR_RUNTIME_DRIFT,
             f"interface_baseline {ilock.get('interface_baseline')!r} != frozen {BASELINE['identity']!r}")

    # consent_purposes <- registry members[].id, cross-checked to shared-definitions enum
    reg_ids = [m.get("id") for m in (consent.get("members") or []) if isinstance(m, dict)]
    enum_ids = (defs.get("consent_purpose") or {}).get("enum") or []
    if sorted(reg_ids) != sorted(BASELINE["consent_purposes"]):  # set-equal (order is not semantic)
        emit(errors, ERR_RUNTIME_DRIFT,
             f"consent-purposes registry {sorted(reg_ids)} != frozen {sorted(BASELINE['consent_purposes'])}")
    if sorted(enum_ids) != sorted(BASELINE["consent_purposes"]):
        emit(errors, ERR_RUNTIME_DRIFT,
             f"shared-definitions consent_purpose enum {sorted(enum_ids)} != frozen "
             f"{sorted(BASELINE['consent_purposes'])}")

    # timing <- interface-lock frozen.timeouts_ms
    tmo = frozen.get("timeouts_ms") or {}
    mr, hb = tmo.get("media_readiness") or {}, tmo.get("heartbeat_interval") or {}
    lag = (tmo.get("lease_after_grant") or {}).get("max")
    lah = (tmo.get("lease_after_heartbeat") or {}).get("max")
    derived_timing = {
        "readiness_ms": {"default": mr.get("default"), "min": mr.get("min"), "max": mr.get("max")},
        "heartbeat_ms": {"min": hb.get("min"), "max": hb.get("max")},
        # Both released lease ceilings must equal the single mirrored ceiling; max()
        # would hide a tightening of one. When they diverge (or either changes), the
        # non-scalar value below != the mirror's {"max": 10000} and drift fires.
        "lease_ms": {"max": lag if lag == lah else {"lease_after_grant": lag, "lease_after_heartbeat": lah}},
    }
    if derived_timing != BASELINE["timing"]:
        emit(errors, ERR_RUNTIME_DRIFT,
             f"interface-lock frozen.timeouts_ms -> {derived_timing} != frozen timing {BASELINE['timing']}")

    # speech gates <- shared-definitions speech_gate enum + interface-lock frozen.closed_defaults
    gate_enum = (defs.get("speech_gate") or {}).get("enum") or []
    for gate in BASELINE["speech_gates_reserved"]:
        if gate not in gate_enum:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"reserved speech gate {gate!r} absent from released speech_gate enum {gate_enum}")
        if gate not in closed:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"reserved speech gate {gate!r} not marked reserved in interface-lock closed_defaults")
    for gate in BASELINE["speech_gates_allowed"]:
        if gate not in gate_enum:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"allowed speech gate {gate!r} absent from released speech_gate enum {gate_enum}")

    # interaction modes: neutral must be a released live mode; every reserved mode must NOT be live
    live = [m.get("id") for m in (imodes.get("members") or []) if isinstance(m, dict)]
    if BASELINE["interaction_mode_neutral"] not in live:
        emit(errors, ERR_RUNTIME_DRIFT,
             f"neutral interaction mode {BASELINE['interaction_mode_neutral']!r} not in released "
             f"interaction-modes registry {live}")
    for m in BASELINE["interaction_modes_reserved"]:
        if m in live:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"reserved interaction mode {m!r} is now a released live mode {live} "
                 f"(kernel promoted it; mirror is stale — fail closed)")
    # Set-equality cross-check: the released live modes must match the interface-lock
    # frozen declaration exactly (a new live mode, or a dropped one, is drift even if
    # neutral-in / reserved-out still holds).
    il_imodes = (frozen.get("registries") or {}).get("interaction-modes")
    if isinstance(il_imodes, list) and sorted(live) != sorted(il_imodes):
        emit(errors, ERR_RUNTIME_DRIFT,
             f"interaction-modes registry {sorted(live)} != interface-lock "
             f"frozen.registries.interaction-modes {sorted(il_imodes)}")

    # avc02_results <- interface-lock frozen.result_kinds
    if (frozen.get("result_kinds") or []) != BASELINE["avc02_results"]:
        emit(errors, ERR_RUNTIME_DRIFT,
             f"interface-lock result_kinds {frozen.get('result_kinds')} != frozen {BASELINE['avc02_results']}")

    # presentation_modes + authoritative_axes <- avc-12
    props12 = avc12.get("properties") or {}
    pm_enum = (props12.get("presentation_mode") or {}).get("enum") or []
    if sorted(pm_enum) != sorted(BASELINE["presentation_modes"]):
        emit(errors, ERR_RUNTIME_DRIFT,
             f"avc-12 presentation_mode enum {sorted(pm_enum)} != frozen {sorted(BASELINE['presentation_modes'])}")
    for axis in BASELINE["authoritative_axes"]:
        if axis not in props12:
            emit(errors, ERR_RUNTIME_DRIFT, f"authoritative axis {axis!r} absent from avc-12 properties")

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
    #    Fail closed on non-integer selected values: the schema declares these as
    #    `type: integer`, so a float/string/null (e.g. `6000.0` or `"6000"`) must
    #    NOT slip past the ceiling — it is rejected outright, not skipped. Absent
    #    keys are "not selected" and remain optional (block-level closed default).
    timing = candidate.get("timing")
    if isinstance(timing, dict):
        tb = baseline["timing"]
        for field in ("readiness_ms", "heartbeat_ms", "lease_ms"):
            if field not in timing:
                continue
            value = timing[field]
            if not isinstance(value, int) or isinstance(value, bool):
                emit(errors, ERR_TIMING_OUT_OF_RANGE,
                     f"{ctx}: {field} {value!r} must be an integer (selected value "
                     f"could not be resolved to a number — fail closed)")
                continue
            bounds = tb[field]
            low = bounds.get("min")
            high = bounds.get("max")
            if (low is not None and value < low) or (high is not None and value > high):
                lo_txt = low if low is not None else "-inf"
                emit(errors, ERR_TIMING_OUT_OF_RANGE,
                     f"{ctx}: {field} {value} outside kernel ceiling [{lo_txt},{high}]")

    # 3) Required-control fallback (FR-007)
    #    A control that is not explicitly `required: true` must declare a fallback.
    #    `required` is mandatory per schema; a control omitting it is treated as
    #    fail-closed (not-guaranteed-required) so a missing fallback is still caught.
    for control in candidate.get("standard_controls", []) or []:
        if isinstance(control, dict) and control.get("required") is not True and not control.get("fallback"):
            emit(errors, ERR_CONTROL_FALLBACK_MISSING,
                 f"{ctx}: control {control.get('id')} is not required: true and declares no fallback")

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

    # 10) Structured per-capability accessibility declarations (FR-010/020/028).
    #     When present the block must be a mapping of KNOWN capabilities to booleans;
    #     any unknown key or non-boolean value is malformed and fails closed. When
    #     the block (or a capability) is omitted it resolves to its schema closed
    #     default (false), which is valid — closed defaults need no declaration.
    ab_cap = candidate.get("accessibility_baseline")
    if ab_cap is not None:
        if not isinstance(ab_cap, dict):
            emit(errors, ERR_ACCESSIBILITY_INVALID,
                 f"{ctx}: accessibility_baseline must be a mapping of per-capability booleans")
        else:
            for cap, decl in ab_cap.items():
                if cap not in ACCESSIBILITY_CAPABILITIES:
                    emit(errors, ERR_ACCESSIBILITY_INVALID,
                         f"{ctx}: accessibility_baseline has unknown capability {cap!r}")
                elif not isinstance(decl, bool):
                    emit(errors, ERR_ACCESSIBILITY_INVALID,
                         f"{ctx}: accessibility_baseline.{cap} must be a boolean, got {decl!r}")


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
        elif expect in ENFORCED_RULE_IDS:
            # Enforced-rule-class negative: must fire exactly its one primary rule class.
            if enforced_fired != {expect}:
                emit(errors, ERR_FIXTURE_EXPECT,
                     f"{rel(path)} must fail exactly one primary rule {expect}, but fired {sorted(enforced_fired)}")
        elif enforced_fired:
            # Structural negative (e.g. accessibility/shape): must NOT trip an enforced rule class.
            emit(errors, ERR_FIXTURE_EXPECT,
                 f"{rel(path)} expected structural {expect} only, but also fired enforced {sorted(enforced_fired)}")

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


def verify_released_runtime_compatibility(errors: list[str]) -> None:
    """--mode realization (FR-021/FR-025): every released profile's
    runtime_compatibility must pin EXACT content-addressed coordinates over the
    FULL consumed kernel set. For each profile carrying released_* coordinates:
    require a full 40-hex commit (no tag-only pin), the interface-lock anchor,
    and set-completeness (every released schema/registry + interface-lock from
    the manifest must be pinned — so the AVC schema structural guards cannot
    relax silently); then triangulate each pinned entry
    declared digest == manifest per-file sha256 == actual sha256(read_bytes).
    Fail closed (AFUV-RUNTIME-DRIFT) on any missing/mismatched/omitted coordinate.

    Note: `released_tag` pins the consumed KERNEL bundle (contract-v1.7, from the
    interface-lock realized_stamp) — NOT this profile's own bundle version in
    contracts/manifest.yaml. Do not "fix" this to the manifest header.
    """
    manifest = load_yaml(MANIFEST_PATH)
    man_digest = {c.get("path"): c.get("sha256")
                  for c in (manifest.get("contracts") or []) if isinstance(c, dict)}
    ilock = load_yaml(RELEASED_INTERFACE_LOCK)
    kernel_tag = ((ilock.get("completion_states") or {}).get("realized_stamp") or {}).get(
        "contract_bundle_version")
    anchor = rel(RELEASED_INTERFACE_LOCK)

    data = load_yaml(EXAMPLES_PATH)
    for index, example in enumerate(data.get("examples") or []):
        if not isinstance(example, dict):
            continue
        rc = example.get("runtime_compatibility")
        if not isinstance(rc, dict):
            continue
        if not any(k in rc for k in ("released_tag", "released_commit", "released_digests")):
            continue  # parallel-baseline-pinned profile (baseline_identity only) — not a realization target
        ctx = f"{rel(EXAMPLES_PATH)}#{(example.get('profile') or {}).get('id', index)}"

        tag = rc.get("released_tag")
        if tag != kernel_tag:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"{ctx}: released_tag {tag!r} must equal the released kernel bundle "
                 f"{kernel_tag!r} (interface-lock realized_stamp)")
        commit = rc.get("released_commit")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit or ""):
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"{ctx}: released_commit must be a full 40-hex release commit SHA "
                 f"(no tag-only pin), got {commit!r}")
        digests = rc.get("released_digests")
        if not isinstance(digests, dict) or not digests:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"{ctx}: released_digests must be a non-empty map of released "
                 f"registry/interface-lock paths -> sha256")
            continue
        if anchor not in digests:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"{ctx}: released_digests must pin the interface-lock anchor {anchor}")
        # Set-completeness: released_digests MUST content-address the full consumed
        # kernel set (every schema/registry + interface-lock), derived from the
        # manifest so the required set cannot itself drift. Without this, the AVC
        # schema structural guards (avc-02 non_grant.not, avc-12 not-guards) would
        # never be content-addressed and could relax silently through this gate.
        required_paths = {
            p for p in man_digest
            if isinstance(p, str) and p.startswith("contracts/avatar-client/")
            and (p.endswith(".schema.yaml") or "/registries/" in p
                 or p.endswith("interface-lock.yaml"))
        }
        missing = sorted(required_paths - set(digests))
        if missing:
            emit(errors, ERR_RUNTIME_DRIFT,
                 f"{ctx}: released_digests omits content-addressed kernel files {missing} "
                 f"(set-completeness: every released schema/registry/interface-lock must be pinned)")
        for path_str, declared in digests.items():
            fpath = ROOT / path_str
            if not fpath.exists():
                emit(errors, ERR_RUNTIME_DRIFT,
                     f"{ctx}: released_digests path {path_str} does not exist (fail closed)")
                continue
            actual = digest_file(fpath)
            if declared != actual:
                emit(errors, ERR_RUNTIME_DRIFT,
                     f"{ctx}: released_digests[{path_str}] {declared!r} != actual sha256 {actual!r}")
            man = man_digest.get(path_str)
            if man is None:
                emit(errors, ERR_RUNTIME_DRIFT,
                     f"{ctx}: released_digests path {path_str} is not a manifest-pinned kernel file")
            elif man != actual:
                emit(errors, ERR_RUNTIME_DRIFT,
                     f"{ctx}: manifest sha256 for {path_str} ({man!r}) != actual {actual!r}")


ACCEPTANCE_MAP = (ROOT / "openspec" / "changes" / "align-avatar-first-ui-standard"
                  / "supporting-docs" / "avatar-first-ui-acceptance-map.yaml")


def load_acceptance_scenarios(errors: list[str]) -> set[str]:
    """Read the OpenSpec acceptance map read-only; assert 8 req / 25 scenarios."""
    if not ACCEPTANCE_MAP.exists():
        emit(errors, ERR_PARITY_ACCEPTANCE, f"{rel(ACCEPTANCE_MAP)} acceptance map not found")
        return set()
    data = load_yaml(ACCEPTANCE_MAP)
    reqs = data.get("requirements", []) or []
    scenarios = {s.get("id") for r in reqs for s in (r.get("scenarios") or [])}
    exp_r = data.get("expected_requirement_count")
    exp_s = data.get("expected_scenario_count")
    if exp_r is not None and len(reqs) != exp_r:
        emit(errors, ERR_PARITY_ACCEPTANCE,
             f"{rel(ACCEPTANCE_MAP)} requirement count {len(reqs)} != expected {exp_r}")
    if exp_s is not None and len(scenarios) != exp_s:
        emit(errors, ERR_PARITY_ACCEPTANCE,
             f"{rel(ACCEPTANCE_MAP)} scenario count {len(scenarios)} != expected {exp_s}")
    return scenarios


def validate_parity(errors: list[str]) -> None:
    """AFUV-PARITY-ACCEPTANCE — reverse parity: every fixture's scenario evidence_ids
    resolve against the acceptance map via evidence_id_template: TEST-{scenario_id}."""
    scenarios = load_acceptance_scenarios(errors)
    if not scenarios:
        return
    for path in sorted(FIXTURES_DIR.rglob("*.yaml")):
        fixture = load_yaml(path)
        for eid in fixture.get("evidence_ids", []) or []:
            if eid not in scenarios:
                emit(errors, ERR_EVIDENCE_UNKNOWN,
                     f"{rel(path)} evidence_id {eid} is not a scenario in the acceptance map "
                     f"(its evidence id would be TEST-{eid})")


def validate_forward_parity(errors: list[str]) -> None:
    """AFUV-PARITY-ACCEPTANCE — forward parity (FR-022/SC-008): every requirement and
    scenario declared in the acceptance map must be OWNED. Fail on any overclaimed item.

    An item is owned when it resolves to at least one of:
      - an owning fixture (a fixture whose `evidence_ids` reference one of its scenarios),
      - declared offline standard/examples/validator evidence
        (`evidence_types` containing `automated` or `manual`), or
      - a named successor change (`owner_changes` non-empty).
    A requirement (or scenario) declaring none of these is overclaimed and fails closed.
    """
    if not ACCEPTANCE_MAP.exists():
        return  # absence already reported by load_acceptance_scenarios
    data = load_yaml(ACCEPTANCE_MAP)
    reqs = data.get("requirements", []) or []
    fixture_scenarios: set[str] = set()
    for path in sorted(FIXTURES_DIR.rglob("*.yaml")):
        fixture = load_yaml(path)
        for eid in fixture.get("evidence_ids", []) or []:
            fixture_scenarios.add(eid)
    for req in reqs:
        rid = req.get("id")
        has_successor = bool(req.get("owner_changes"))
        offline_owned = bool(set(req.get("evidence_types") or []) & {"automated", "manual"})
        scenario_ids = [s.get("id") for s in (req.get("scenarios") or [])]
        fixture_owned = any(sid in fixture_scenarios for sid in scenario_ids)
        if not (has_successor or offline_owned or fixture_owned):
            emit(errors, ERR_PARITY_ACCEPTANCE,
                 f"{rel(ACCEPTANCE_MAP)} requirement {rid} is overclaimed: no owning fixture, "
                 f"declared offline evidence, or named successor change")
        for sid in scenario_ids:
            if sid not in fixture_scenarios and not (has_successor or offline_owned):
                emit(errors, ERR_PARITY_ACCEPTANCE,
                     f"{rel(ACCEPTANCE_MAP)} scenario {sid} is overclaimed: no owning fixture and "
                     f"requirement {rid} declares no offline evidence or named successor")


import re

_AFU_SCENARIO_RE = re.compile(r"^AFU-\d{3}-S\d{2}$")


def check_determinism(errors: list[str]) -> None:
    """SC-006 / FR-023 — assert the determinism-relevant STRUCTURE each deterministic
    fixture depends on, rather than re-parsing the same file twice.

    A deterministic UI acceptance replay is byte-stable only if the fixture pins
    every non-deterministic input (clock/ids/font/locale/platform), supplies the
    canonical AVC command/event/snapshot inputs it derives from, carries AFU
    evidence IDs, and declares a well-shaped `expected` view-state/record output.
    Any missing determinism anchor fails closed."""
    det_dir = FIXTURES_DIR / "deterministic"
    for path in sorted(det_dir.glob("*.yaml")) if det_dir.is_dir() else []:
        fixture = load_yaml(path)
        ctx = rel(path)

        # (b) Fixed non-deterministic inputs — no live clock/RNG/locale/platform.
        inputs = fixture.get("inputs")
        if not isinstance(inputs, dict):
            emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} deterministic fixture missing fixed `inputs` block")
        else:
            for key in ("clock", "font", "locale"):
                if not isinstance(inputs.get(key), str) or not inputs.get(key).strip():
                    emit(errors, ERR_DETERMINISM_SHAPE,
                         f"{ctx} inputs.{key} must be a fixed non-empty string (deterministic clock/font/locale)")
            ids = inputs.get("ids")
            if not isinstance(ids, dict):
                emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} inputs.ids must pin fixed session/workflow/persona IDs")
            else:
                for key in ("session_id", "workflow_id", "persona_id", "persona_version"):
                    if ids.get(key) in (None, ""):
                        emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} inputs.ids.{key} must be a fixed value")
            if not isinstance(inputs.get("platform_capabilities"), dict):
                emit(errors, ERR_DETERMINISM_SHAPE,
                     f"{ctx} inputs.platform_capabilities must be a fixed capability mapping")

        # (b) Canonical AVC command/event/snapshot inputs the expected shape derives from.
        canonical = fixture.get("canonical")
        if not isinstance(canonical, dict):
            emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} deterministic fixture missing canonical AVC inputs")
        else:
            if not isinstance(canonical.get("commands"), list) or not canonical.get("commands"):
                emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} canonical.commands must be a non-empty list")
            if not isinstance(canonical.get("events"), list) or not canonical.get("events"):
                emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} canonical.events must be a non-empty list")
            if not isinstance(canonical.get("snapshot"), dict):
                emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} canonical.snapshot must be a mapping")

        # (b) AFU evidence IDs anchoring the fixture to the acceptance map.
        evidence_ids = fixture.get("evidence_ids")
        if not isinstance(evidence_ids, list) or not evidence_ids or not all(
                isinstance(e, str) and _AFU_SCENARIO_RE.match(e) for e in evidence_ids):
            emit(errors, ERR_DETERMINISM_SHAPE,
                 f"{ctx} evidence_ids must be a non-empty list of AFU-<req>-S<nn> scenario IDs")

        # (a) `expected` output shape — required determinism-derived keys present/typed.
        expected = fixture.get("expected")
        if not isinstance(expected, dict):
            emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} deterministic fixture missing `expected` output shape")
            continue
        if not isinstance(expected.get("view_state"), dict) or not expected.get("view_state"):
            emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} expected.view_state must be a non-empty mapping")
        if not isinstance(expected.get("records"), list) or not expected.get("records"):
            emit(errors, ERR_DETERMINISM_SHAPE, f"{ctx} expected.records must be a non-empty list")


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
    validate_parity(errors)
    validate_forward_parity(errors)
    check_determinism(errors)
    if args.mode == "realization":
        verify_released_runtime_compatibility(errors)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print(f"OK xFactory avatar-first UI standard surface [mode={args.mode}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
