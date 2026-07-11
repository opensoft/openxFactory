## 1. Standard And Profile

- [ ] 1.1 Update `docs/avatar-first-ui-standard.md` with the four authoritative axes, client-local presentation modes, Hermes-layer defaults, AVC-02 denial/terminal rendering, held-answer/media-authorization state, control-loss behavior, safe rendering, disclosure, handoff, and accessibility evidence boundaries.
- [ ] 1.2 Update `contracts/schemas/avatar-first-ui-profile.schema.yaml` with runtime compatibility, surface default, interaction and speech-gate selection, readiness default/range, heartbeat/lease ceilings, fallback slots, neutral consent-purpose mappings, persona catalog reference, retention overlay, accessibility baseline, and closed defaults while preserving existing-profile compatibility.

## 2. Template And Examples

- [ ] 2.1 Update `templates/ui/avatar-first.yaml` with stable regions, standard controls, authority sources, media/recording awareness, fallback behavior, handoff boundary, and reserved-feature defaults.
- [ ] 2.2 Update `examples/avatar-first-ui/` with validated customer avatar-first, client hybrid, domain conventional-first, and Ledgerx-style confirmation-before-action profiles plus compatibility and negative fixtures.

## 3. Validation And Handoff

- [ ] 3.1 Extend `scripts/validate-avatar-first-ui.py` for schema/template/example parity, state axes, safe outcomes, held-answer/media authorization, timeout and lease bounds, controls and fallbacks, purpose mappings, persona references, safe rendering, accessibility fields, and forbidden/reserved modes.
- [ ] 3.2 Map every `AFU-*` requirement and scenario to standard, validator, fixture, or named successor evidence. Keep Flutter widget, golden, platform-accessibility, and live-provider evidence explicitly successor-owned.
- [ ] 3.3 Consume accepted kernel variances by mapped fields, then pin and cross-check the exact released capability, outcome, consent-purpose, and state registries without modifying kernel files. Rebase to the latest bundle, allocate the next available version, update `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and `contracts/README.md` atomically for the profile-schema revision, and publish the matching annotated tag without pre-reserving a version.
- [ ] 3.4 Run strict target/all OpenSpec validation, avatar-first UI validation, compatibility/negative fixtures, acceptance-map parity, and `git diff --check`. Confirm that no canonical AVC, F0, reference-runtime, DomainxFactory, Flutter, or deployment file changed.
