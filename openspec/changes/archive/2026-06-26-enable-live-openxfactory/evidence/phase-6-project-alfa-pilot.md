# Phase 6 Evidence: Project Alfa Live Pilot

Change: `enable-live-openxfactory-factory`
Phase: 6
Date: 2026-06-26
Decision: PASS FOR CONTROLLED LOCAL/REPLAY PILOT

## Pilot Target

Project: Project Alfa
Repository: `opensoft/project-alfa`
Pilot feature: `FEAT-000` / `FEAT-001` low-risk documentation or repo-diagnostics flow, depending on the replay fixture.

The pilot target remains intentionally low-risk:

- documentation/tooling-oriented behavior
- no production data migration
- no direct default-branch push
- no direct merge
- draft PR mode when external PR execution is enabled
- changed-line budget capped at 10,000 lines, with local pilot target below 3,000 lines

## Scope Proven

Phase 6 verified the controlled local/replay pilot path:

```text
Hermes service
  -> worker lane
  -> repo preparation checks
  -> feature decomposition
  -> Spec Kit stage artifacts
  -> implementation/branch evidence
  -> deterministic checks
  -> local branch review evidence
  -> Hermes PR admission gate
  -> GitHub draft PR plan/record fixture
  -> Merge Council fixture path
  -> traceability checks
```

This phase did not force an external live PR mutation. The dry-run/replay path exists so the stack can prove all internal gates before opening a real GitHub PR.

## Commands Run

From `opensoft/Omnigent-Install`:

```bash
./scripts/smoke-live-pilot.sh
./scripts/smoke-live-factory-replay.sh
./scripts/smoke-live-factory-six-workstream.sh
```

Results:

```text
OK live pilot contracts
OK no committed secrets smoke
OK live pilot smoke
OK PR admission contracts
OK Project Alfa feature decomposition packet
OK Spec Kit control fixtures
OK implementation worker contracts
OK no committed secrets smoke
OK live factory replay smoke
OK live factory six-workstream smoke
```

The six-workstream smoke also exercised these supporting lanes:

- non-doc pilot contracts
- non-doc stage gates
- non-doc PR admission evaluator
- non-doc Merge Council
- Hermes dispatch inbox
- worker lane config and preflight
- Phase 8 scale-out contracts/smoke
- Phase 9 operations contracts/smoke
- no-committed-secrets checks

## Required Artifacts Covered

| Artifact | Coverage |
|---|---|
| Decomposition packet | `smoke-live-factory-replay.sh`, six-workstream smoke |
| Spec Kit spec/plan/tasks/analyze artifacts | Spec Kit control smoke and live pilot fixtures |
| Clarification answer packet | Earlier Project Alfa clarify/approval smokes |
| Implementation evidence | implementation worker contracts and replay fixture |
| Deterministic check results | replay and six-workstream smoke outputs |
| Branch review findings | PR admission replay fixture |
| PR admission packet | PR admission replay and non-doc PR admission smoke |
| GitHub PR record | dry-run/draft PR fixture from live pilot smoke |
| Merge readiness report | non-doc Merge Council smoke and six-workstream smoke |
| Merge Master decision artifact | covered by later Phase 7/8 evidence |
| Traceability report | replay smoke checks feature/job/artifact/approval traceability edges |

## Acceptance Checks

| Requirement | Result | Evidence |
|---|---:|---|
| Traceability exists from feature to PR admission readiness | PASS | `smoke-live-factory-replay.sh` |
| No approval gate is bypassed | PASS | replay blocks continue before approval and only records PR-open artifact after approval |
| PR is not opened before PR admission | PASS | replay asserts `pr_opened` event absent before approval |
| Changed-line budget is enforced by policy | PASS | live pilot config validation caps at 10,000 changed lines |
| No committed secrets | PASS | `smoke-no-committed-secrets.sh` via live pilot and six-workstream smokes |

## Stop Conditions Checked

| Stop condition | Result |
|---|---|
| Missing live pilot contract | PASS |
| Missing decomposition packet | PASS |
| Missing Spec Kit control fixture | PASS |
| Missing implementation worker contract | PASS |
| PR opened before admission approval | PASS |
| Secret material appears in Git-tracked pilot files | PASS |

## Remaining Work

The controlled pilot path is ready for an operator-enabled external live run. Later phases still need to close:

- enforceable PR admission and Merge Council runtime proof
- Merge Master dry-run/human-review router proof
- CloudPC worker runtime packaging and auth restore
- memory helper integration and operations/DR closeout
