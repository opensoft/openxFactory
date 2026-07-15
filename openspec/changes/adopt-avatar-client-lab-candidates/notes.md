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
