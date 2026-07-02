# Merge Readiness Report

Feature: Live Factory Phase 8 Worker Auth Memory Operations Readiness
PR: #27
Decision: READY_WITH_WARNINGS

## Inputs Reviewed

- `openspec/changes/enable-live-openxfactory-factory/tasks.md`
- `openspec/changes/enable-live-openxfactory-factory/evidence/phase-8-worker-auth-memory-operations.md`
- CloudPC deployment and worker lane smoke output
- Phase 8 scale-out smoke output
- Phase 9 operations smoke output
- agentmemory smoke output
- Plan A credential install smoke output
- no-secret smoke output
- OpenSpec validation output

## Acceptance Criteria Coverage

| AC | Covered | Evidence | Notes |
|---|---:|---|---|
| CloudPC worker pack and lane capacity verified | Yes | CloudPC and worker lane smokes | Includes coder/tester capacity separation. |
| Subscription auth profile restore/onboarding avoids committed secrets | Yes | Plan A credential install and no-secret smokes | Live provider probes remain explicit. |
| Memory helpers are context, not canonical truth | Yes | memory docs and agentmemory smoke | GBrain/Honcho documented; agentmemory tested. |
| Operations and DR smoke sequence documented and runnable | Yes | Phase 9 operations smoke | Dry-run backups/rebuild/upgrade checks pass. |
| Live Claude/Codex provider auth probes executed | No | intentionally skipped | Warning only; set `RUN_AUTH_PROBES=1` for CloudPC onboarding. |

## Council Results

| Reviewer | Decision | Blocking |
|---|---|---:|
| Spec Traceability | Pass | No |
| Security | Pass | No |
| Tests | Pass | No |
| Architecture | Pass | No |
| Maintainability | Warn | No |
| Integration | Warn | No |

## Required Fixes

None for local/DRY-RUN operations readiness.

## Warnings

1. Live Claude/Codex auth probes were not forced in this local slice.
2. A real CloudPC onboarding run must enable `RUN_AUTH_PROBES=1` after Key Vault/profile restore.
