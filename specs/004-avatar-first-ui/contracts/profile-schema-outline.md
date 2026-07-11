# Contract: Avatar-First UI Profile Schema (additive outline)

**Target file**: `contracts/schemas/avatar-first-ui-profile.schema.yaml`
**Kind**: registered contract schema (already in `contracts/manifest.yaml`)
**Change type**: additive — existing top-level `required` set is unchanged; all
new blocks are optional with closed defaults so existing static profiles stay
valid (FR-016, SC-003).

This is a design reference for the implement phase, not the final schema. It
lists the blocks to add and the closed default / fail-closed rule for each.

## Unchanged (existing) required top-level keys

`profile`, `authority_boundaries`, `interaction_surface`, `channels`,
`standard_controls`, `tool_boundaries`, `escalation`, `traceability`. Continue to
carry `schema_version` and `name: avatar_first_ui_profile`.

## Added optional blocks (with closed defaults)

```text
runtime_compatibility:      # FR-013, FR-025, FR-021 — exact content-addressed coords
  baseline_identity: str    #   parallel work: exact avatar-client-parallel-v1 identity
  baseline_digests: {..}    #   required baseline digests (no loose range)
  released_tag: str?        #   realization only (Phase 3)
  released_commit: str?     #   exact commit SHA
  released_digests: {..}?   #   registry/interface-lock SHA-256 digests
  # default when omitted: parallel-baseline-pinned; a RELEASED profile MUST carry it

presentation:               # FR-001, FR-002
  surface_default: enum[conversation, work, review]   # default: conversation
  presentation_modes: [conversation, work, review]    # client-local only

media:                      # FR-008, FR-009
  states: [permission, capture_authorized, capture_pending, capture_active,
           listening, speaking, control_degraded, control_lost,
           governed_action_pending, retention_active]
  held_answer_state: enum[connecting, pending]        # default: connecting (never active)

outcome_slots:              # FR-009, FR-012 — reference kernel outcome IDs only
  - outcome_ref: str        #   kernel outcome-registry ID (read-only)
    message_key: str        #   localization-safe key (no provider text)
    retry_guidance: str
    fallback_modes: [text|handoff|upgrade|retry_later]

fallback_slots:             # FR-007, FR-009 — closed default: text_or_handoff
  denial: {message_key, approved_modes[]}
  terminal: {..}
  missing_control: {..}
  persona_unavailable: {..}
  audio_unavailable: {..}

interaction_mode:           # FR-015
  value: enum[provider_vad, server_vad(reserved), push_to_talk(reserved,disabled)]  # default provider_vad
  fallback: enum[text, handoff]   # REQUIRED when value is a reserved mode
speech_gate:
  value: str                # kernel-permitted gate; closed default = disabled -> text/handoff

timing:                     # FR-013, FR-026 — selected values only; ceilings kernel-owned
  readiness: <selected>     #   omitted -> kernel-registry default (read-only)
  heartbeat: <selected>
  lease: <selected>
  # validator fails closed if a value exceeds, or a ceiling cannot be resolved

consent_purpose_mappings:   # FR-014 — reference 3 neutral IDs (+ optional stricter domain IDs)
  - behavior: str
    purpose_ref: str        #   neutral consent-purpose ID (read-only kernel)
    domain_purpose_ref: str?
  # no consent evidence; not authoritative over memory-gateway consent profile

persona_reference:          # FR-011, FR-013 — reference-only (Q1=A)
  persona_id: str
  version: int|str
  catalog_locator: str?     #   optional NON-SECRET locator
  # unresolved -> approved fallback (fail-closed); never invent persona data

retention_overlay:          # FR-027 (Q8=A) — references only
  policy_refs: [str]        #   externally owned retention-policy IDs
  display_flags: {..}       #   presentation-only; no inline durations/policy/consent
  # unresolved policy ref -> fail-closed

accessibility_baseline:     # FR-010, FR-028 (Q7=A) — structured per-capability, closed defaults
  keyboard_operation: bool           # default: false (declared-absent = closed)
  stable_focus: bool
  visible_focus: bool
  screen_reader_announcements: bool
  captions: bool
  text_only_mode: bool
  reduced_motion: bool
  high_contrast: bool
  non_color_cues: bool
  zoom_reflow: bool
  pseudo_locale_coverage: bool
```

## Legacy compatibility (D7)

The pre-alignment embedded `persona_catalog` block remains **accepted**
(deprecated). A compatibility fixture proves a legacy profile still validates.
New/updated examples switch to `persona_reference`.

## Fail-closed summary (Principle VII)

Omitted optional field ⇒ most-restrictive value. Unresolvable persona / retention
/ ceiling / consent-purpose reference ⇒ validation failure with the matching
stable error ID (see [validator-rules.md](./validator-rules.md)). Reserved/forbidden
interaction mode without a fallback ⇒ failure. Presentation may never author an
authoritative axis.
