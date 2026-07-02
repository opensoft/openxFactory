# Phase 4 Evidence: Omnigent Worker Event Bridge

Change: `enable-live-openxfactory-factory`
Phase: 4
Date: 2026-06-26
Decision: PASS

## Scope Verified

Phase 4 verified that Omnigent worker execution can report structured runtime activity into Hermes through two compatible paths:

- direct worker event client posts when `HERMES_API_URL` and `HERMES_JOB_ID` are configured
- `HERMES_EVENT_JSON:` marker fallback for CLI/orchestrator output streams

The verified implementation lives in `opensoft/Omnigent-Install` commit `c53f190`, pinned by `installs/omnigent-install`.

## Required Event Coverage

The bridge supports and/or exercises the live-factory event vocabulary:

| Event | Coverage |
|---|---|
| `job_started` | Covered by Hermes launch/API smoke from Phase 3 |
| `stage_started` | Covered by direct worker event client smoke |
| `subagent_dispatched` | Covered by marker bridge smoke |
| `subagent_result_collected` | Covered by marker bridge smoke |
| `artifact_recorded` | Covered by direct client and marker bridge smokes |
| `approval_requested` | Covered by direct client and marker bridge smokes |
| `approval_recorded` | Covered by Hermes approval smoke from Phase 3 |
| `stage_completed` | Covered by stage/pilot worker scripts, verified in later phase slices |
| `job_completed` / `job_blocked` / `job_failed` | Covered by launch/store status model, verified in later phase slices |

## Durable IDs

The event bridge records the durable identifiers required by the runtime contract when applicable:

- `job_id`
- `run_id`
- `stage_id`
- `artifact_id`
- `approval_request_id`
- `bridge_key`
- `feature_id`
- `agent_id`

`bridge_key` is the idempotency key for both direct posts and marker replay.

## Commands Run

From `opensoft/Omnigent-Install`:

```bash
./scripts/smoke-hermes-event-client.sh
./scripts/smoke-hermes-event-bridge.sh
git diff --check
```

Results:

```text
OK Hermes event client smoke
OK Hermes event bridge smoke
```

## Acceptance Checks

| Requirement | Result | Evidence |
|---|---:|---|
| A no-write/direct worker run records events into Hermes | PASS | `smoke-hermes-event-client.sh` posts `stage_started` through Hermes API. |
| Duplicate `bridge_key` events are idempotent | PASS | Direct client repeats `stage_started_speckit_clarify`; only the first payload is retained. Marker bridge replays the full marker stream twice; event counts remain unchanged. |
| Missing Hermes API config no-ops safely | PASS | Direct client runs with `HERMES_API_URL` and `HERMES_JOB_ID` unset and exits successfully. |
| Marker fallback remains supported | PASS | `smoke-hermes-event-bridge.sh` replays `HERMES_EVENT_JSON:` markers and records events, artifact, approval request, and traceability. |
| Artifact and approval side effects are linked by traceability | PASS | Marker bridge smoke checks `artifact -> awaits -> approval_request`. |

## Remaining Work

Later phases still need to prove the event bridge inside the full live pilot flow:

- all Spec Kit stage events under canonical ownership
- PR admission stage completion and gate behavior
- Merge Council and Merge Master event sequences
- CloudPC worker heartbeat and capacity events
