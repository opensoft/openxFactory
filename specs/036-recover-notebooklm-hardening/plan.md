# Implementation Plan: Recover NotebookLM hardening

**Branch**: `036-recover-notebooklm-hardening` | **Date**: 2026-10-03 | **Spec**: [spec.md](spec.md)

## Summary

Recover the original typed package and focused tests, then reconcile every
current-main change against the common base before enabling the scoped gate.
Keep the wrapper's public path and patchable seams. Validate the union of
current and historical scenarios, not just a historical count.

## Technical Context

**Language/Version**: Python 3.12 in py-bench.
**Primary Dependencies**: stdlib, existing nlm CLI, existing lazy dashboard adapters.
**Storage**: existing JSON manifest, workspace Markdown and Git.
**Testing**: hermetic pytest and guarded unittest; Ruff, basedpyright and the original programming checker.
**Target Platform**: existing Linux CLI/container workflow.
**Project Type**: repository tooling CLI.
**Performance Goals**: preserve current provider command ordering and bounded polling.
**Constraints**: no live provider acts; no type suppressions or new runtime dependency; below 250 pure lines per scoped module.
**Scale/Scope**: wrapper, notebooklm_sync package, NotebookLM tests and scoped quality command/configuration.

## Constitution Check

- OpenSpec hardening scope authorized by the accepted recovery plan; one Speckit ledger.
- No contract/runtime surface, release allocation or immutable tag changes.
- Committed paths remain portable and documentation indexed.
- Baseline collection has 108 tests; historical snapshot had 129. Preserve scenario union.
- Affected OpenSpec change must validate. Repository-wide strict validation has a pre-existing add-chain-attestation failure; no push until it is corrected or the user explicitly grants an exception. This is an outstanding publication gate, not a claimed pass.
- No old ref/worktree deletion until reviewed replacement lands and bundle restoration is proved.

## Project Structure

Feature artifacts live in `specs/036-recover-notebooklm-hardening/`.
Production is `scripts/sync-notebooklm-books.py`, `scripts/notebooklm_sync/`
and `scripts/check-notebooklm-sync-quality.py`. Tests live in
`tests/notebooklm/`, with non-collectable typed support modules.

**Structure Decision**: retain the old package's acyclic models/provider/corpus,
projection/hosting/import, session, facade, CLI direction. Add focused modules
for newer readiness/adoption, root-product discovery, title naming and hosting
path resolution where needed. Keep lazy dashboard adapters and wrapper seams.

## Execution

1. Record current behavioral/quality baseline and restore the original checker.
2. Recover old modules and tests in the isolated feature.
3. Port each newer main change with its tests, resolving state/adapter seams.
4. Enforce size, typing, lint and checker rules without suppressions.
5. Validate discovery, hermetic behavior and CLI probes; record exact evidence.
6. Publish only after the outstanding gate resolves, request exact-head Codex
   review, resolve findings and land; then remove old ref/worktree.
