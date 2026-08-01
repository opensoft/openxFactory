# Tasks: add-propose-verb

## 1. Contracts (openxFactory)

- [x] 1.1 Extend `gate-intent.schema.yaml`: `propose` in the verb enum,
      `topic_id` on target, conditional `propose → target.topic_id`.
- [x] 1.2 Extend `gate-action-record.schema.yaml`: `propose` in the action
      enum, `topic_id` on target, conditionals `propose → target.topic_id`
      and `propose → artifacts contains workflow-job`.
- [x] 1.3 Validate: schema validators + `openspec validate --all --strict`.

## 2. Engine (codexFactory)

- [x] 2.1 `kickoff.py`: `propose()` dispatch — human-only, staging-topic
      existence guard, duplicate-commission refusal, `workflow-job`
      descriptor (workflow `proposal-authoring`, `topic_id` target) +
      gate-action record.
- [x] 2.2 `gate_console.py`: `ACTION_PROPOSE`, `build_gate_action_record`
      grows `topic_id`; `GateConsole.propose` delegate.
- [x] 2.3 `cli.py`: `gate propose <topic-id>` (+ `--outline`, `--workflow`,
      `--note`).
- [x] 2.4 `gate_routes.py`: `propose` joins `EXECUTING_VERBS`; loopback
      route with the dispose-possible response discipline.

## 3. Dashboard affordance (codexFactory)

- [x] 3.1 Wheel: focused staged tile mounts a "▶ draft proposal" button in
      the badge rail under the same capability gate as the dispose tray;
      refusals land in the refusal panel; success decorates the tile
      (session-local overlay, snapshot untouched).

## 4. Verification

- [x] 4.1 Engine + route tests (accept, missing topic, duplicate
      commission, agent-path rejection) green.
- [x] 4.2 Live browser check on the local dashboard (button renders on a
      staged focus under gate capability, actor resolved; zero page errors).
- [x] 4.3 First real commission by Brett recorded end-to-end (descriptor +
      record in the checkout).
      PASSED 2026-08-01 (D10 combined pass Step E, Brett sign-off same
      day): `▶ draft proposal` on the merged, session-free, honestly-ready
      `consent-instrument-contract` (live health 0.925 / 0 blockers)
      commissioned workflow `proposal-authoring` — descriptor
      `ideation/dashboard/gate-records/consent-instrument-contract/propose-20260801T012134Z.workflow-job.yaml`
      and gate-action record
      `propose-20260801T012134Z.gate-action.yaml` (`actor: brettheap`),
      both landed on `main` by this governance commit (the verb records
      without committing — F10). The first click's FR-023 refusal over the
      then-live session is preserved as evidence of the guard working.
      The commissioned change is `add-consent-instrument` (DTN-016 exit).
      Evidence:
      `add-workbench-integrated-editor-chat/evidence/d10/e-43-commission.md`.
