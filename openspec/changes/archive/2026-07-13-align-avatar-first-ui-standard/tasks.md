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

## Bookkeeping annotation — archived with all 8 boxes open (2026-08-22, `archive-register-rulings`)

No box is ticked here and no task text above is altered. This section records
what the archive evidence actually shows, because this ledger and this change's
README row disagree with no reconciliation on the record — the anomaly
enumerated as C6 in `docs/archive-record-discrepancies.md`, ruled on 2026-08-22
by Brett (in-session, multiple-choice round) to be annotated rather than
force-ticked. Ticking eight boxes from inferred evidence would be authoring, not
correcting.

**What the ledger says.** Eight boxes across three sections — the standard and
profile schema (§1), the template and examples (§2), validation and handoff
(§3) — and every one of them is open. It archived that way on 2026-07-13 in
`f64c4c0` ("Archive avatar-first UI standard (004); relocate its acceptance map
(4/5 done)"), whose message reports the gates green ("004 --mode realization,
97 runtime tests, openspec --all --strict (25 passed)") and says nothing about
the open boxes.

**What the README row claims.** "avatar-first UI standard, domain profile
carrier, template, examples, and offline realization validator; realized as
`contract-v1.8` … archived 2026-07-13."

**Where the realization evidence actually lives — not in this ledger.** The
claim is backed, and the boxes are the only thing missing:

- `contract-v1.8` is a real annotated tag: `81fceae`, 2026-07-13, "Realize
  avatar-first UI standard: contract-v1.8 (004 T030-T035)", with its
  `contracts/CHANGELOG.md` section "contract-v1.8 — 2026-07-13 (additive;
  avatar-first UI profile-schema alignment)".
- The capability was promoted: `openspec/specs/avatar-first-ui/spec.md`.
- Every artifact §1–§3 name is on disk: `docs/avatar-first-ui-standard.md`,
  `contracts/schemas/avatar-first-ui-profile.schema.yaml` (registered in
  `contracts/manifest.yaml`), `templates/ui/`, `examples/avatar-first-ui/`
  (including the acceptance map relocated there at realization so the validator
  survives this directory's archiving), and
  `scripts/validate-avatar-first-ui.py`.
- **The ticking happened elsewhere.** The execution ledger for this work was
  the Speckit feature `specs/004-avatar-first-ui/tasks.md`, which stands at 37
  of 37 tasks done, 0 open. That is where the work was tracked; it was never
  mirrored back into these eight boxes.

So the gap is bookkeeping, not evidence: the realization is locatable and
verified, and this ledger simply stopped being the instrument that recorded it.
