# Phase 3 Evidence: Hermes Runtime Control Plane

Change: `enable-live-openxfactory-factory`
Phase: 3
Date: 2026-06-26
Decision: PASS

## Scope Verified

Phase 3 verified that the pilot Hermes control plane can persist and query the core runtime records needed by the live factory:

- jobs
- runs
- events
- artifacts
- approval requests
- approval decisions
- traceability edges
- worker registry records

The verified implementation lives in `opensoft/Omnigent-Install` commit `8bb179e`, pinned by `installs/omnigent-install`.

## Runtime Surface

The Hermes API exposes the pilot control-plane lifecycle through the Omnigent-facing endpoints:

| Capability | Endpoint shape |
|---|---|
| Create job | `POST /api/omnigent/jobs` |
| Query job/run state | `GET /api/omnigent/jobs/{job_id}` |
| Launch job | `POST /api/omnigent/jobs/{job_id}/launch` |
| Record event | `POST /api/omnigent/jobs/{job_id}/events` |
| Record artifact | `POST /api/omnigent/jobs/{job_id}/artifacts` |
| Request approval | `POST /api/omnigent/jobs/{job_id}/approval-requests` |
| Record approval | `POST /api/omnigent/jobs/{job_id}/approvals` |
| Continue approved job | `POST /api/omnigent/jobs/{job_id}/continue` |
| Record traceability edge | `POST /api/omnigent/jobs/{job_id}/traceability-edges` |
| Register/query workers | `POST /api/workers`, `GET /api/workers` |
| Worker heartbeat | `POST /api/workers/{worker_id}/heartbeat` |

Approval type values are persisted as data so the required live-factory gates can be represented without schema changes:

- `approve_feature_decomposition`
- `approve_speckit_entry`
- `apply_clarification_answers`
- `approve_implementation_start`
- `approve_pr_admission`
- `approve_merge_readiness`
- `merge_master_decision`

Specific stage semantics are verified in later slices; this phase verified the runtime control plane can store, query, and resolve approval records.

## Canonical Postgres Contract

The Hermes store initializes Postgres from the canonical SQL compatibility copy sourced from:

```text
openxFactory/contracts/schemas/hermes-operational-postgres.sql
```

The Omnigent install compatibility validator confirms the local copy and required contract inventory match the pinned `openxFactory` contract reference.

## Commands Run

From `opensoft/Omnigent-Install`:

```bash
python3 scripts/validate-openxfactory-contracts.py
./scripts/smoke-hermes-api.sh
./scripts/run-hermes-postgres-container-test.sh
git diff --check
```

Results:

```text
openxFactory contract compatibility OK: 229761c
OK Hermes API smoke
OK Hermes Postgres smoke
OK Hermes Postgres restart persistence
```

## Stop Conditions Checked

| Stop condition | Result |
|---|---|
| Job cannot be queried after creation | PASS |
| Run is missing from launched job | PASS |
| Event/artifact/approval/traceability records are not persisted | PASS |
| Approval continuation occurs before approval | PASS |
| Postgres schema fails to initialize | PASS |
| API restart loses persisted records | PASS |

## Remaining Work

Phase 3 does not claim the full live pilot is complete. The next slices still need to verify:

- worker event bridge behavior under direct Hermes API posting
- Spec Kit stage ownership and clarification routing
- real Project Alfa pilot artifacts
- PR admission, Merge Council, and Merge Master runtime behavior
- CloudPC worker packaging, auth restore, memory helpers, and DR
