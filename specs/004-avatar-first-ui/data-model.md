# Phase 1 Data Model — Avatar-First UI Standard Alignment

**Feature**: 004-avatar-first-ui | **Date**: 2026-07-11

This is the logical data model for the **avatar-first UI profile** carrier and
its companion artifacts. It is technology-agnostic: the profile is a YAML
document validated offline; no runtime objects are created here. Fields are
grouped by block; each new block is **optional with a closed default** so
existing static profiles remain valid (D12). "Read-only kernel" means the value
references a kernel registry ID resolved by the validator, never authored here.

## Entity: Avatar-first UI profile (the domain overlay carrier)

Existing required top-level keys are unchanged: `profile`,
`authority_boundaries`, `interaction_surface`, `channels`, `standard_controls`,
`tool_boundaries`, `escalation`, `traceability`. The alignment adds the
**optional** blocks below.

| Block (new/updated) | Shape | Closed default when omitted | Rules (FR) |
|---------------------|-------|-----------------------------|------------|
| `runtime_compatibility` | Content-addressed coordinates (see entity below) | absent ⇒ profile treated as parallel-baseline-pinned; released profiles MUST carry it | FR-013, FR-025, FR-021 |
| `presentation` | `surface_default: conversation\|work\|review`; `presentation_modes: [conversation, work, review]` | `surface_default: conversation`; modes are client-local, never authoritative | FR-001, FR-002 |
| `media` | State flags (see entity) incl. `held_answer_state: connecting\|pending` | most-restrictive: capture inactive; held answer = `connecting` | FR-008, FR-009 |
| `outcome_slots` | List of `{outcome_ref (kernel outcome ID), message_key, retry_guidance, fallback_modes[]}` | empty ⇒ only kernel-registered outcomes renderable; no free text | FR-009, FR-012 |
| `fallback_slots` | Map: denial / terminal / missing-control / persona-unavailable / audio-unavailable ⇒ `{message_key, approved_modes[]}` | each unset slot ⇒ `text_or_handoff` (safe) | FR-007, FR-009 |
| `interaction_mode` | `provider_vad` (default) \| `server_vad` (reserved) \| `push_to_talk` (reserved, disabled) + `fallback` | `provider_vad`; reserved modes require `fallback: text\|handoff` | FR-015 |
| `speech_gate` | Selection referencing kernel-permitted gate | closed: gate disabled ⇒ text/handoff | FR-015 |
| `timing` | `{readiness, heartbeat, lease}` selected values | omitted ⇒ kernel-registry default (read-only); never opens beyond ceiling | FR-013, FR-026 |
| `consent_purpose_mappings` | List referencing the 3 neutral consent-purpose IDs (+ optional stricter domain IDs) | empty ⇒ no purpose asserted (fail-closed) | FR-014 |
| `persona_reference` | `{persona_id, version, catalog_locator?}` (see entity) | unresolved ⇒ approved fallback (fail-closed) | FR-011, FR-013 |
| `retention_overlay` | Retention-policy references + presentation flags/labels (see entity) | unresolved reference ⇒ fail-closed | FR-027 |
| `accessibility_baseline` | Structured per-capability declarations (see entity) | each capability defaults closed (declared-absent) | FR-010, FR-028 |
| `handoff` | `roles[]`, URL constraints (no token/subject/transcript/secret) | inherits template escalation defaults | FR-005, FR-006 |

**Legacy compatibility**: the pre-alignment embedded `persona_catalog` block
remains accepted (deprecated) so existing profiles validate; new/updated
examples use `persona_reference` (D7).

## Entity: Runtime compatibility

| Field | Meaning | Rule |
|-------|---------|------|
| `baseline_identity` | Exact `avatar-client-parallel-v1` baseline identity (parallel work) | exact string, no range (FR-025) |
| `baseline_digests` | Required baseline digests (per referenced registry/interface lock) | content-addressed |
| `released_tag` | Released contract bundle tag (realization only) | set at Phase 3 |
| `released_commit` | Exact release commit SHA | content-addressed pin (Principle VI) |
| `released_digests` | Required registry/interface-lock SHA-256 digests | validator verifies referenced IDs against these bytes |

No loose released version range; no separate hand-maintained capability list —
the profile's field references already declare consumed capabilities/outcomes/
states (D5).

## Entity: Persona reference

| Field | Meaning | Rule |
|-------|---------|------|
| `persona_id` | Stable persona ID in the domain/kernel-owned catalog | required |
| `version` | Persona version | required |
| `catalog_locator` | Optional **non-secret** locator for the owning catalog | optional; MUST NOT be a secret/URL with token |

Resolved persona exposes role, display name, required disclosure, supported
languages, lifecycle status (all catalog-owned, out of scope here). Unresolved ⇒
approved fallback; the client never invents persona data. Persona is fixed for a
logical session; a change ends the session and starts a new one (FR-011).

## Entity: Fallback slot

`{message_key, approved_modes[]}` where `approved_modes ⊆
{text, handoff, upgrade, retry_later}`. Used for denial, terminal outcome,
missing control, unavailable persona, unavailable audio. Never carries raw
provider text (FR-007, FR-009, FR-012).

## Entity: Consent purpose mapping

`{behavior, purpose_ref, domain_purpose_ref?}` where `purpose_ref` is one of the
three neutral consent-purpose IDs (read-only kernel) and `domain_purpose_ref` is
an optional stricter domain ID. Carries no consent evidence; does not make the
memory-gateway consent profile authoritative (FR-014).

## Entity: Retention overlay

| Field | Meaning | Rule |
|-------|---------|------|
| `policy_refs[]` | References to externally owned retention-policy IDs | unresolved ⇒ fail-closed |
| `display_flags` / `labels` | Presentation-only flags/labels to show resolved retention state | no inline durations/policy/consent evidence |

No authority to change retention (FR-027).

## Entity: Accessibility baseline (structured, per-capability)

Each capability is an individually validator-checkable field with a closed
default: `keyboard_operation`, `stable_focus`, `visible_focus`,
`screen_reader_announcements`, `captions`, `text_only_mode`, `reduced_motion`,
`high_contrast`, `non_color_cues`, `zoom_reflow`, `pseudo_locale_coverage`
(FR-010, FR-028). Distinguished from later platform qualification evidence owned
by named successors.

## Referenced (not owned) — authoritative runtime axes & kernel registries

- **Authoritative axes** (read-only from `avatar-client-runtime`): session
  lifecycle (broker), control health (lease), media state (trusted-adapter under
  authority), workflow projection (Hermes/workflow authority). The profile never
  authors these; presentation modes never conflate with them (FR-001).
- **Kernel registries** (read-only): capability, outcome, consent-purpose, and
  state registries. Consumed, never edited (FR-017, FR-021).

## Deterministic UI fixture (companion artifact)

Location `examples/avatar-first-ui/fixtures/`. Shape (see
[contracts/fixture-shape.md](./contracts/fixture-shape.md)):

| Field | Meaning |
|-------|---------|
| `fixture_id` | Stable ID |
| `evidence_ids[]` | The `AFU-*` scenario/requirement IDs the fixture attests (e.g. `AFU-001-S01`). The acceptance map's evidence IDs derive from these via its `evidence_id_template: TEST-{scenario_id}` (e.g. `TEST-AFU-001-S01`); the fixture declares the scenario ID and the evidence ID is template-derived. |
| `inputs` | Fixed clock, IDs, font, locale, platform capabilities |
| `canonical` | Canonical AVC command/event/snapshot inputs |
| `expected` | Expected view-state / record shapes |
| `expect_error` (negative only) | The single stable error/evidence ID this fixture must trigger |

Two identical runs ⇒ equivalent `expected` shapes and identical `evidence_ids`
(SC-006). Parity binding (AFUV-PARITY-ACCEPTANCE) resolves each fixture's
scenario `evidence_ids` against the acceptance map via `TEST-{scenario_id}`.

## Validator error / evidence ID catalog

Stable IDs the validator emits (`ERROR <id> <message>`), each tied to a rule
class and a negative fixture (D10; final list in
[contracts/validator-rules.md](./contracts/validator-rules.md)):
`AFUV-AUTHORITY-TRANSITION`, `AFUV-TIMING-OUT-OF-RANGE`,
`AFUV-CONTROL-FALLBACK-MISSING`, `AFUV-PERSONA-UNRESOLVED`, `AFUV-MODE-RESERVED`,
`AFUV-UNSAFE-RENDER`, `AFUV-PURPOSE-INVALID`, `AFUV-HELD-ANSWER-ACTIVE`,
`AFUV-RETENTION-UNRESOLVED` (nine enforced rule classes), plus
parity/structure IDs (`AFUV-PARITY-*`, `AFUV-SCHEMA-*`) and the
realization-drift ID `AFUV-RUNTIME-DRIFT` (`--mode realization`: released kernel
drift or a profile `runtime_compatibility` content-addressing failure).

## State note

The profile itself is static configuration and has no lifecycle state machine.
The runtime session states it describes (idle → … → archived) map onto the four
authoritative axes and are owned by the runtime, not authored by the profile.
