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

## Release cut (section 5) — contract-v1.12 (2026-07-15)

Cut on branch `task/adopt-v112-release` (worktree
`openxFactory-worktrees/adopt-release`, base main @ `58fc401`).

- **5.1 collision re-check (before manifest edits).** `git status -sb` =
  `## task/adopt-v112-release` (clean, own branch only); `git log --oneline -6 --
  contracts examples` = this change's two landing commits (`fc42511`, `43c5a73`)
  atop the ideation cross-reference/routing work and `a010288` (v1.11 inventory) —
  all ancestors of HEAD; `openspec list` active changes (`add-ideation-dashboard`,
  `add-cross-factory-ideation-routing`, `add-ideation-cross-reference-readiness`,
  etc.) touch only `contracts/schemas/ideation-*` + `scripts/` paths held in the
  README "Contracts Pending Realization" area — none touch `contracts/avatar-client`,
  `contracts/avatar-client-lab`, or `examples/avatar-first-ui`. No collision.

- **Manifest members added: 23.** (a) 2 client-lab artifacts —
  `avatar-client-lab-avatar-state-derivation-table` (derivation table `.yaml`),
  `avatar-client-lab-capability-scenario-register`; (b) 20 adopted deterministic
  fixtures (P7 intake ×5, P8 takeover/recovery ×4, P11 interrupted/handoff ×2,
  P12/P13 media.states + control_degraded ×9); (c) 1 successor register
  `avatar-client-evidence-register-implement-avatar-client-lab`. Manifest now
  carries 68 contract entries, 53 with a per-file sha256.
  **`.md`-membership decision: NOT members.** `avatar-state-derivation-table.md`,
  `avatar-client-lab/README.md`, and `client-acceptance-map.yaml` are deliberately
  excluded — the manifest registers only machine-readable YAML per the v1.7 kernel
  and v1.11 document-cataloging precedent (neither registered a `.md`/adoption-guide
  doc), the proposal's Impact counts this change as "+2 artifacts" (the two `.yaml`),
  and tasks.md 5.1 names "the two client-lab artifacts"; `client-acceptance-map.yaml`
  is `implement-avatar-client-lab`'s artifact (governed by `check_client_lab_acceptance_map`,
  not manifest-membership) and neither `--require-realization` nor the impact notes
  demand it here. The prose `.md`/map are governed by the changelog + fail-closed
  validators instead.

- **Byte-identity sweep (5.2): 53 members verified, 0 mismatches.** All 30
  pre-existing recorded-sha256 members — `avatar-first-ui-profile` (v1.8), the 23
  avatar-client kernel members (v1.7), and the 6 document-cataloging schemas
  (v1.11) — recompute byte-identical to their manifest sha256; the 23 newly-added
  members match their computed digests. Confirms the additive-only invariant
  (no released v1.7/v1.8/v1.11 path changed).

- **Gate tail lines (5.3), all from the worktree HEAD:**
  - `validate-avatar-client.py` → `0 error(s), 0 warning(s)`
  - `--strict` → `0 error(s), 0 warning(s)`
  - `--require-realization` → `0 error(s), 0 warning(s)` (now PASSES: the successor
    register is manifest-listed, so `check_digests` no longer emits `digest-missing`;
    pre-registration it failed with exactly that one error)
  - `validate-avatar-first-ui.py` (baseline) → `OK ... [mode=baseline]`
  - `--mode realization` → `OK ... [mode=realization]`
  - `pytest tests/avatar_client_validator/ -q` → `60 passed`
  - `compileall scripts/` → exit 0 (clean)
  - `openspec validate adopt-avatar-client-lab-candidates --strict` → valid;
    `--all --strict` → 28 passed, 0 failed

- **Digest inventory: YES.** `contracts/releases/contract-v1.12.digests.yaml` built
  by `scripts/validate-contract-release.py build --tag contract-v1.12` (release: pass;
  179 entries). It refreshes the closed hermes-runtime release surface + the
  `manifest.yaml` / `CHANGELOG.md` / `README.md` auxiliaries; diff vs
  `contract-v1.11.digests.yaml` = only `bundle_tag` and those three auxiliary
  digests (the hermes-runtime family is byte-identical). The avatar-client-lab
  surface is outside this closure and is content-addressed via `manifest.yaml`.

- **DEFERRED TAG (deviation from 5.2 text).** No git tag created or pushed. The
  annotated `contract-v1.12` tag is applied by the coordinator on the main merge
  commit after review — a tag on this branch commit would point at the wrong
  object. Manifest `contract_bundle_version`, `CHANGELOG.md`, and the digest
  inventory are all cut and internally consistent; only the tag object is pending.
