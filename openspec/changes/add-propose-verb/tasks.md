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
- [ ] 4.2 Live browser check on the local dashboard (button renders on a
      staged focus; refusal panel carries engine reasons).
- [ ] 4.3 First real commission by Brett recorded end-to-end (descriptor +
      record in the checkout).
