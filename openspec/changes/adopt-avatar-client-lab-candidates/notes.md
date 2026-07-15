# Notes: adopt-avatar-client-lab-candidates

Status: record

## Preflight (task 1, 2026-07-15)

- **1.1 Source commit**: `3a8fbd5` verified an ancestor of codexFactory
  `origin/main` — the `002-avatar-client-lab` feature merged via PR #16,
  merge commit `ae78da4` (2026-07-15T18:02Z). Candidate source path:
  `specs/002-avatar-client-lab/upstream-drafts/` at that commit (7/7
  panel-confirmed per its STATUS.md).
- **1.2 Baseline validation** (openxFactory main @ `3bb8685`, before any
  landing): `validate-avatar-client.py --strict` 0 errors / 0 warnings;
  `validate-avatar-first-ui.py` OK baseline; OK realization.
- **1.3 Collision check**: working tree clean (`## main...origin/main`);
  recent `contracts/` + `examples/` history is the landed cataloging /
  ideation-routing / cross-reference work plus the avatar-lab task merges
  (`da69dc8`, `50c10db`, `e8e5e26` all ancestors of HEAD); active changes
  (`openspec list`) touch no `contracts/` or `examples/avatar-first-ui/`
  paths. No collision.

## OQ ratifications (task 4.1)

Product-owner sign-off: **Brett, 2026-07-15**. Recorded verbatim-in-substance in
`contracts/avatar-client-lab/avatar-state-derivation-table.md` §8 "Ratifications"
(and applied consistently in the `.yaml` companion).

- **OQ-1 — RATIFIED WITH BINDING.** R2's handoff trigger binds to the
  `avatar-client-runtime` session-lifecycle transition registry ("Leased control
  channel and deterministic recovery"); standard §9's
  `handoff_requested`/`handoff_active` are kept as neutral projections signaled via
  `lifecycle_transition` on `session_lifecycle`. Proof path: landed
  `avatar-handoff-escalation` seed.
- **OQ-2 — RATIFIED WITH BINDING.** R4's `interrupted` binds to an authoritative
  control-channel stop/cancel (`response.cancel` / `output_audio_buffer.clear`) or
  a superseding authoritative turn. Proof path: landed
  `avatar-interrupted-barge-in` seed.
- **OQ-3 — RATIFIED AS-IS.** Clean terminals map to `listening`; forced by the
  closed six-state vocabulary (a seventh state would be a kernel vocabulary change,
  out of scope); revisit note recorded at R3.
- **OQ-4 — CONFIRMED.** The `.yaml` is the content-addressed vendored source gate
  (vi) tests against (P2-map pattern); manifest registration is the section-5
  release cut, not task 4 (`contracts/manifest.yaml` untouched here).
- **OQ-5 — REPLACED (D4 unsourced-mapping rule).** `governed_action_pending` maps
  to `listening`, NOT `thinking`; applied in both `.md` (§4.1, §5.2) and `.yaml`
  (`media_state_map`). Rationale: no released source grounds `thinking`; the
  pendency is surfaced by the action card + status strip (AFU-004 family), and
  `thinking` would falsely signal model activity during a governance wait.
- **OQ-6 — RATIFIED WITH SCOPING AMENDMENT.** The INV-2 fail-closed target is
  `blocked`, lawful via an explicit amendment: `blocked` derives ONLY from
  `control_lost`/`control_degraded` OR the INV-2 fail-closed condition, citing
  FR-018(b).
