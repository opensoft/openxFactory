code_surface: openxFactory
target_release: implemented
Status: ratified
Ratified: 2026-07-13 — record: the archive act, commit `f64c4c0` "Archive avatar-first UI standard (004); relocate its acceptance map (4/5 done)", which applied this change's spec delta into `openspec/specs/avatar-first-ui/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "archives align-avatar-first-ui-standard to archive/2026-07-13-* (avatar-first-ui promoted to openspec/specs/)". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The current avatar-first guidance predates the AVC result union, authoritative
media-authorization barrier, orthogonal runtime state, and neutral consent
purposes. Updating that guidance is a standards-and-validation change, not the
same implementation unit as building contracts, running a live API experiment,
or coding a broker.

This change aligns the reusable UI standard and domain profile carrier while
leaving Flutter implementation to `implement-avatar-client-lab`. It can proceed
in parallel against `avatar-client-parallel-v1` and performs a final read-only
cross-check against the released kernel registries.

## What Changes

- Update `docs/avatar-first-ui-standard.md` around four authoritative runtime
  axes and client-local `conversation | work | review` presentation modes.
- Define Customer Hermes as avatar-first, Client Hermes as hybrid, and Domain
  Hermes as conventional-first with an avatar analyst/copilot, subject to
  domain risk and accessibility overrides.
- Align the registered avatar-first profile schema with runtime compatibility,
  outcome/fallback slots, media-authorization pending state, speech-gate and
  interaction-mode selection, readiness/heartbeat/lease ceilings, consent
  purpose mappings, persona catalog references, retention overlays, and
  accessibility baselines.
- Update the shared template and validated examples for customer avatar-first,
  client hybrid, domain conventional-first, and confirmation-before-action
  experiences.
- Extend `scripts/validate-avatar-first-ui.py` to check the promoted states,
  safe outcome rendering, controls, fallbacks, authority boundaries, purpose
  mappings, persona references, accessibility fields, and closed defaults.
- Publish deterministic UI fixture shapes and evidence mappings without
  creating Flutter widgets, provider adapters, or a live client.
- Consume, but do not edit, the kernel's capability, outcome, consent-purpose,
  and state registries. Parallel implementation does not edit shared release
  metadata; the final UI profile-schema release rebases and updates it
  atomically after the kernel release.

## Capabilities

### New Capabilities

- `avatar-first-ui`: Defines the adaptive avatar shell, Hermes-layer defaults,
  standard controls and fallbacks, persona/disclosure duties, accessibility,
  safe rendering, workflow handoff boundary, and deterministic UI acceptance.

## Impact

- **openxFactory UI surface:** `docs/avatar-first-ui-standard.md`,
  `contracts/schemas/avatar-first-ui-profile.schema.yaml`,
  `templates/ui/avatar-first.yaml`, `examples/avatar-first-ui/`, and
  `scripts/validate-avatar-first-ui.py`.
- **Contract kernel:** read-only registry dependency; this change never edits
  `contracts/avatar-client/`. Manifest, changelog, and contract README changes
  occur only in this proposal's serialized final release.
- **Flutter client:** implementation remains in `implement-avatar-client-lab`,
  which must prove the standard with widget, accessibility, and golden evidence.
- **DomainxFactories:** later provide profiles and mappings. This change does
  not modify any DomainxFactory repository.
- **Workflow console:** existing workflow-visualization ownership remains
  unchanged; no second canvas or web console is built.
- **Compatibility:** existing static profiles remain valid; new runtime fields
  are additive or have explicit closed defaults.
