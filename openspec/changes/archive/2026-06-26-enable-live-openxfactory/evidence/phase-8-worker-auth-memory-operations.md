# Phase 8 Evidence: CloudPC Worker, Auth, Memory, And Operations Readiness

Change: `enable-live-openxfactory-factory`
Phase: 8
Date: 2026-06-26
Decision: PASS FOR LOCAL/DRY-RUN OPERATIONS READINESS

## Scope Verified

This phase verified the worker/runtime operations layer around the live factory:

- CloudPC worker pack shape
- worker lane capacity and preflight
- subscription-auth profile rules
- Plan A credential restore/onboarding
- no committed secrets
- agentmemory worker-local memory
- GBrain/Honcho memory-helper documentation
- operations backup/rebuild/upgrade smoke path

## Commands Run

From `opensoft/Omnigent-Install`:

```bash
./scripts/smoke-cloudpc-deployment-plan.sh
./scripts/smoke-worker-lane-config.sh
./scripts/smoke-phase8-scaleout.sh
./scripts/smoke-phase9-operations.sh
./scripts/smoke-no-committed-secrets.sh
./scripts/smoke-agentmemory.sh
./scripts/smoke-plan-a-credential-install.sh
python3 scripts/validate_cloudpc_deployment_plan.py
python3 scripts/validate_phase9_operations.py
python3 scripts/validate_plan_a_credential_install.py
```

Results:

```text
OK CloudPC deployment plan
OK worker lane config
OK worker preflight
OK Phase 8 scale-out contracts
OK Phase 8 scale-out smoke
OK Phase 9 operations contracts
OK Phase 9 operations smoke
OK no committed secrets smoke
agentmemory smoke passed
OK Plan A credential install
OK Plan A credential install smoke
```

## Worker Model Coverage

| Worker concern | Result | Evidence |
|---|---:|---|
| CloudPC shape is 8 vCPU / 32 GB / 500 GB | PASS | CloudPC deployment validator |
| Coder worker pack supports lightweight concurrency | PASS | Phase 8 scale-out smoke |
| Tester/integration lanes are capacity-limited separately | PASS | worker lane config smoke |
| Worker health/preflight is reportable | PASS | worker preflight and lane config smokes |
| Unsafe overscheduling is rejected or queued | PASS | Phase 8 scale-out smoke |

## Auth And Secret Restore Coverage

| Requirement | Result | Evidence |
|---|---:|---|
| Coders use subscription auth profiles, not API keys | PASS | worker preflight and no-secret smokes |
| `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` are not committed | PASS | no committed secrets smoke |
| Key Vault restore shape is documented | PASS | Plan A credential install validator |
| Portable and per-node fallback modes are documented | PASS | credential onboarding docs and validator |
| Live auth probes are optional and explicit | PASS | operations smoke skips unless `RUN_AUTH_PROBES=1` |

## Memory Helper Coverage

| Helper | Runtime role | Canonical boundary |
|---|---|---|
| `agentmemory` | Omnigent worker-local coding/session memory | context only; not canonical truth |
| `GBrain` | Hermes group/project coordination memory | summaries and coordination context only |
| `Honcho` | Hermes profile/conversation continuity memory | relationship/profile context only |

Canonical truth remains:

- Git
- OpenSpec
- Spec Kit artifacts
- GitHub PRs
- Hermes approvals
- Merge reports

Memory promotion to project truth requires an approval/event/artifact trail.

## Operations / DR Coverage

The operations smoke covers:

- agentmemory dry-run backup
- Hermes database dry-run backup
- backup manifest creation
- worker rebuild prerequisite checks
- upgrade preflight
- no-secret scan

## Known Caveat

Live Claude/Codex auth probes were not forced in this slice. The operation smoke reports:

```text
auth probes skipped; set RUN_AUTH_PROBES=1 to probe Claude/Codex
```

That is intentional for repeatable CI/local proof. A real CloudPC onboarding run must set `RUN_AUTH_PROBES=1` after the subscription auth profile is restored.
