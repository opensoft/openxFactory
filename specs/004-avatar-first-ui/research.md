# Phase 0 Research — Avatar-First UI Standard Alignment

**Feature**: 004-avatar-first-ui | **Date**: 2026-07-11

All spec clarifications are resolved (see `spec.md` § Clarifications, Session
2026-07-11), so there are no open `NEEDS CLARIFICATION` items. This document
records the **design** decisions that translate the clarified requirements and
the current artifacts into concrete shapes for implementation. Each item is
Decision / Rationale / Alternatives considered.

## Current baseline (what exists today)

- `docs/avatar-first-ui-standard.md` (`Status: draft`): §1–14 cover core
  principle, ownership, shell regions, four channels, standard controls, persona
  contract, disclosure, tool boundary, 15 interaction states, implementation
  levels L0–L4, Hermes-layer defaults, domain-overlay requirements, traceability.
- `contracts/schemas/avatar-first-ui-profile.schema.yaml` (`schema_version: 1`,
  `name: avatar_first_ui_profile`): requires `profile`, `authority_boundaries`,
  `interaction_surface`, `channels`, `standard_controls`, `tool_boundaries`,
  `escalation`, `traceability`; an **embedded** `persona_catalog`.
- `templates/ui/avatar-first.yaml` (`kind: xfactory_avatar_first_ui_template`):
  authority boundaries, levels, Hermes guidance, regions, states, channels,
  15 controls, persona/tool/escalation/traceability defaults, overlay slots.
- `examples/avatar-first-ui/domain-overlays.example.yaml`
  (`kind: xfactory_avatar_first_ui_overlay_examples`): domain-instantiated
  overlays (Medx, codex, …) as `.example.yaml` stubs.
- `scripts/validate-avatar-first-ui.py`: PyYAML; checks schema `required`,
  template `kind`/presentation-only/channels/15 controls, and example shape.
- The schema is already registered in `contracts/manifest.yaml`
  (id `avatar-first-ui-profile`); `contracts/CHANGELOG.md`, `contracts/README.md`
  exist; the standard is already in the README doc index.

**Gap**: the baseline predates the AVC result union, the media-authorization
barrier, orthogonal runtime state, neutral consent purposes, content-addressed
compatibility, and structured accessibility. The decisions below close that gap
additively.

## D1 — Four authoritative axes vs client-local presentation modes

**Decision**: In the standard, model the four **authoritative** axes owned by
`avatar-client-runtime` — session lifecycle (broker), control health (lease),
media state (trusted-adapter observation under authority), workflow projection
(Hermes/workflow authority) — as read-only inputs, and model `conversation |
work | review` as **client-local presentation modes** that never author an axis.
In the schema, add a `presentation` block with a `surface_default` mode and a
`presentation_modes` enum; keep authoritative state out of the profile (it is
runtime-owned). Retain the existing 15 `session_states` list but document it as
mapping onto the authoritative axes, not replacing them.

**Rationale**: FR-001/FR-002 and Decision 2 of the change require axes and modes
to stay separate so presentation cannot fabricate transitions (Principle VII).
Keeping authoritative state runtime-owned keeps the profile a carrier, not an
authority.

**Alternatives**: Encode axis values inside the profile — rejected: it would
duplicate kernel/runtime authority and invite drift.

## D2 — Media-authorization / held-answer and AVC-02 outcome + fallback slots

**Decision**: Add a `media` block distinguishing permission, capture
authorized/pending, capture active, listening, speaking, control degraded/lost,
governed-action pending, and retention active; a held provider answer without a
matching `media_authorized` renders as `connecting|pending`. Add `outcome_slots`
and `fallback_slots`: outcomes reference kernel outcome-registry IDs and expose
only a localization-safe `message_key`, `retry_guidance`, and approved fallback
modes; provider error text is structurally excluded. Control-loss vs media-loss
is a documented distinction offering the runtime-defined stop/reconnect/handoff.

**Rationale**: FR-008/FR-009, Decision 5. Safe rendering and the authoritative
media barrier are the core safety properties; representing them as closed slots
lets the validator enforce "no raw provider text in widget state."

**Alternatives**: Free-form outcome strings — rejected: not machine-checkable and
leaks provider text.

## D3 — Interaction mode and speech gate

**Decision**: Add `interaction_mode` with `provider_vad` as the neutral default,
`server_vad` reserved (provider-native details live in a separate server
profile, not here), and `push_to_talk` reserved + disabled with a required
text/handoff fallback. Add a `speech_gate` selection. The validator rejects a
released profile that selects a reserved/forbidden mode without the fallback.

**Rationale**: FR-015, Decision 6. Keeps provider-native semantics out of the
neutral carrier while still letting a profile declare its gate.

**Alternatives**: Allow `server_vad` inline — rejected: pulls provider-native
detail into the neutral layer.

## D4 — Selected readiness / heartbeat / lease vs kernel-owned ceilings (Q4=A)

**Decision**: The profile carries only per-profile **selected** readiness,
heartbeat, and lease values (e.g. `timing.readiness`, `timing.heartbeat`,
`timing.lease`). The schema does **not** hardcode numeric ceilings. The validator
resolves ceilings read-only — from the frozen `avatar-client-parallel-v1`
baseline during development and the released state registry at realization — and
fails closed when a selected value exceeds, or a ceiling cannot be resolved.

**Rationale**: Q4=A, FR-013/FR-026, Principle VII. Ceilings are kernel-owned;
duplicating them would create drift the cross-check must catch.

**Alternatives**: Embed ceilings as neutral defaults (option B) — rejected:
duplicates kernel authority. Hybrid symbolic bounds (option C) — rejected as
unnecessary complexity given the read-only resolution already handles defaults.

## D5 — Content-addressed runtime compatibility (Q5=Custom)

**Decision**: `runtime_compatibility` records **exact content-addressed
coordinates**, never a loose released range. During parallel work: the exact
`avatar-client-parallel-v1` baseline identity + required baseline digests. At
realization: the released bundle tag, exact commit, and required
registry/interface-lock digests. The validator verifies every referenced
capability/outcome/consent-purpose/state ID against those exact bytes. No second
hand-maintained capability list is introduced — the profile's existing field
references already declare what it consumes.

**Rationale**: Q5 custom answer, FR-025/FR-021, Principle VI (consumers pin exact
commit + digests; a movable tag is not a pin).

**Alternatives**: Version pin/range only (option A) — rejected by the user: loose
ranges are not permitted for a released profile. Separate required-capability set
(option B/C) — rejected: redundant second list.

## D6 — Consent-purpose mappings

**Decision**: Add `consent_purpose_mappings` that reference the three neutral
consent-purpose IDs (resolved read-only from the kernel consent-purpose
registry) and MAY add stricter domain IDs. The block carries **no** consent
evidence and does not make the memory-gateway consent profile authoritative.

**Rationale**: FR-014, Decision 6. Keeps consent authority in Hermes/consent
layers; the UI only maps purposes.

**Alternatives**: Store consent state in the profile — rejected: authority
violation.

## D7 — Persona reference-only vs legacy embedded catalog (Q1=A) + compatibility

**Decision**: Introduce a `persona_reference` object carrying `persona_id`,
`version`, and an optional **non-secret** `catalog_locator`. The persona-catalog
schema and instances stay domain/kernel-owned and out of scope. An unresolved
persona reference fails closed to an approved fallback; the client never invents
persona data. For backward compatibility, the validator continues to **accept**
the legacy embedded `persona_catalog` shape (treated as deprecated), and a
compatibility fixture proves a legacy/static profile still validates. New and
updated examples use `persona_reference`.

**Rationale**: Q1=A, FR-011/FR-013, plus FR-016/SC-003 (existing static profiles
remain valid). Making the reference additive while keeping the legacy shape
accepted satisfies both reference-only intent and compatibility.

**Alternatives**: Hard-replace `persona_catalog` with the reference — rejected:
breaks existing profiles, violating the additive-compatibility requirement. Add a
neutral persona-catalog schema here (Q1 option B) — rejected by the user.

## D8 — Retention overlay references only (Q8=A)

**Decision**: `retention_overlay` carries references to externally owned
retention-policy IDs plus presentation flags/labels needed to show resolved
retention state. It carries no inline durations, legal policy, consent evidence,
or authority to change retention. An unresolved policy reference fails closed.

**Rationale**: Q8=A, FR-027. Keeps retention-policy authority in Hermes/consent
layers; the UI only displays resolved state.

**Alternatives**: Inline retention parameters (option B) — rejected: UI would own
policy that belongs elsewhere.

## D9 — Structured per-capability accessibility baseline (Q7=A)

**Decision**: Replace the flat `accessibility` object with a **structured**
per-capability declaration set: keyboard operation, stable/visible focus,
screen-reader announcements, captions, text-only mode, reduced motion, high
contrast, non-color cues, zoom/reflow, and pseudo-locale coverage — each with a
closed default and each individually validator-checkable. The standard separates
these declarable requirements from later platform qualification (Windows
qualification, web WCAG 2.2 AA audit/exception register, extra locales) owned by
named successors.

**Rationale**: Q7=A, FR-010/FR-028, AFU-005. Machine-checkable per-capability
fields map 1:1 to the standard's accessibility requirements.

**Alternatives**: Single baseline enum (option B) — rejected: gaps not
machine-checkable. Referenced baseline ID (option C) — rejected: needs a baseline
registry owner that does not exist.

## D10 — Negative-fixture rule classes and stable error/evidence IDs (Q6=A)

**Decision**: Enforce ≥1 negative fixture per rule class, each failing **one
primary** rule and carrying a stable error/evidence ID. Rule classes:

| Rule class | Stable error ID (proposed) |
|------------|----------------------------|
| Presentation-authored authoritative transition | `AFUV-AUTHORITY-TRANSITION` |
| Out-of-range readiness/heartbeat/lease | `AFUV-TIMING-OUT-OF-RANGE` |
| Missing required-control fallback | `AFUV-CONTROL-FALLBACK-MISSING` |
| Unknown/invalid persona reference | `AFUV-PERSONA-UNRESOLVED` |
| Reserved/forbidden mode selected | `AFUV-MODE-RESERVED` |
| Unsafe rendering / HTML or unsafe URI | `AFUV-UNSAFE-RENDER` |
| Missing/invalid consent-purpose mapping | `AFUV-PURPOSE-INVALID` |
| Held-answer rendered as active | `AFUV-HELD-ANSWER-ACTIVE` |

The validator emits `ERROR <error-id> <message>` for each rejected rule so error
IDs are stable evidence anchors. Final IDs are confirmed in
[contracts/validator-rules.md](./contracts/validator-rules.md).

**Rationale**: Q6=A, FR-019/FR-020/SC-002. Full rule coverage with stable IDs
gives the strongest, replayable acceptance evidence.

**Alternatives**: Per-requirement fixtures (option B) — rejected: may under-test
multiple rules per requirement. Representative subset (option C) — rejected:
weaker fixture-level evidence.

## D11 — Deterministic fixtures directory and determinism inputs (Q3=A)

**Decision**: Publish fixtures as versioned YAML/JSON under
`examples/avatar-first-ui/fixtures/` (subdirs `compatibility/` and `negative/`),
**separate** from the profile examples. Each fixture pins fixed
clock/ID/font/locale/platform inputs and canonical AVC command/event/snapshot
inputs, declares expected view-state/record shapes, and carries its AFU evidence
IDs. The validator checks fixtures; two identical runs yield equivalent shapes.
The concrete shape is defined in [contracts/fixture-shape.md](./contracts/fixture-shape.md).

**Rationale**: Q3=A, FR-023/SC-006. Separation keeps carrier profiles distinct
from test shapes and lets successors reuse the fixtures.

**Alternatives**: Embed shapes in the schema/examples (option B) — rejected:
conflates carrier and tests. Prose-only shapes (option C) — rejected: weaker
offline determinism evidence.

## D12 — Additive-with-closed-defaults compatibility and migration fixtures

**Decision**: Every new field is optional with an explicit closed (most
restrictive) default so an omitted field never opens behavior. Keep the current
top-level `required` set unchanged; new blocks are optional. Provide ≥1
compatibility fixture (a pre-alignment profile, including the legacy embedded
persona catalog) that still validates. Document the persona/timing/retention
migration path in the standard and `data-model.md`.

**Rationale**: FR-016/SC-003/SC-004, Principle VII. Guarantees existing profiles
remain valid while new fields fail closed.

**Alternatives**: Make new blocks required — rejected: breaks existing profiles.

## D13 — Validator baseline vs final-realization modes

**Decision**: The validator supports two modes: (a) **baseline** (default during
parallel work) resolving IDs/ceilings against the frozen
`avatar-client-parallel-v1` fixture data; (b) **final-realization** loading the
exact released kernel registries read-only and failing closed on any drift.
Mode selection is a plan-level execution detail (an explicit CLI flag such as
`--mode {baseline,realization}` defaulting to `baseline`, or an env var); the
default keeps offline parallel runs green. This detail is settled in the
implement phase and does not change spec requirements.

**Rationale**: FR-021, Decision 10. Offline parallel work must not depend on the
kernel release; realization must be exact and fail-closed.

**Alternatives**: Auto-detect released registries — rejected: implicit mode
switching is surprising in CI; an explicit flag is clearer.

## D14 — Serialized post-kernel release (deferred)

**Decision**: Treat the shared-metadata release as a distinct, deferred Phase 3
that runs only after the kernel release: rebase, allocate the next
`contract_bundle_version` at realization, update
`contracts/manifest.yaml`/`CHANGELOG.md`/`README.md` atomically for the
profile-schema revision, publish the annotated tag, and cross-check no
kernel/reference-runtime/F0/DomainxFactory/Flutter/deployment file changed.
During parallel work these files are **not** touched.

**Rationale**: Principle VI, change Decision 1 and Migration Plan, the team-lead
instruction. Avoids write conflicts with sibling changes on shared metadata.

**Alternatives**: Update manifest/changelog now — rejected: pre-reserving a
version and racing siblings violates Principle VI and the ownership boundary.

## Resolved unknowns

None outstanding. Deferred/out-of-scope by design (named successors): renderer,
Flutter state management, media/storage packages, native/web packaging
(`implement-avatar-client-lab`); formal accessibility qualification and domain
onboarding (`avatar-pilot-hardening`); the conventional web console and workflow
editor (workflow-visualization standard); domain profiles and mappings
(DomainxFactory repos).
