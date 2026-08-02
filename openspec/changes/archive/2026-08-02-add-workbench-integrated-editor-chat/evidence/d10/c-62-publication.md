# Step C — Deliberate hosted-refresh reproduction (`add-dashboard-repo-selector` 6.2)

Status: record · 2026-07-31 session

## The chain (no image rebake anywhere)

| Stage | Evidence |
|---|---|
| Distinct document (not Step B's unmerged creation) | `docs/d10-hosted-refresh-marker.md` |
| Ordinary governed landing | openxFactory PR #46, squash-merged `ae3f9c76292bd2810e7533ea7b6cba4487ad9ff9` (admin merge under Brett's live "merge it" authorization; no CI configured on that path) |
| Aggregation pointer-sync | xFactory `main` commit `2bf51fd` (openxFactory gitlink → `ae3f9c7`), staged via `update-index --cacheinfo` in an isolated worktree — shared-checkout state untouched |
| Publication lane dispatch | `workflow_dispatch` run `30672928437` on `doc-health-nightly.yml` (the P3 binding); prepare/finalize green; the singleton artifact worker executed and pushed the publication |
| Rolling publication | branch `doc-health/nightly` commit `6b6af30`; PR opensoft/xFactory#65 squash-merged `41c702aa7bc6adcaa0d249fbb8fd09843ce2fd2d`; health-only paths verified before merge |
| Published data source | index: 11 entries, openxFactory `@ main = ae3f9c76292b`; marker present in `openxFactory-snapshot.json` |
| Hosted refresh observation (Brett, live) | "I see the marker doc on the hosted dashboard after refresh in openxFactory" |
| Image digest before | `sha256:b602380e…` (`c-62-image-before.txt`, 08:16Z) |
| Image digest after | `sha256:b602380e…` — IDENTICAL (`c-62-image-after.txt`, 23:44Z; pod spot-reschedule within the same ReplicaSet noted, zero restarts) |

## Clause verdict

- Document landed on `main`, publication dispatched, hosted refresh clicked,
  document found: TRUE (human observation, deliberate reproduction of the
  motivating incident).
- No image rebake anywhere in the sequence: TRUE (identical immutable
  digest before/after; the only cluster event was a spot-pool pod
  reschedule).
- Selector sweep: see `c-62-selector-sweep.md`.
- Pass/Fail: Brett's sign-off cell; the mechanics all passed.
