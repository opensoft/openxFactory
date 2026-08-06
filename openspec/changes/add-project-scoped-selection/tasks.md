# Tasks: add-project-scoped-selection

## 1. Contracts

- [ ] 1.1 Extend `gate-intent.schema.yaml` additively: `create-project` in
      the verb enum; `project_id` on `target`; conditional `create-project →
      target.project_id`. Header note naming this change as the growth
      source; no `contract_schema_version` bump.
- [ ] 1.2 Extend `gate-action-record.schema.yaml` the same way, including
      the `artifacts contains workflow-job` companion conditional.
- [ ] 1.3 Schema conformance tests: one valid intent and one valid record
      for `create-project`; a record missing its workflow-job companion
      rejected; a record without `target.project_id` rejected.
- [ ] 1.4 Contract registration at the next additive bundle cut per
      `docs/contract-versioning-policy.md`.

## 2. Engine + routes

- [ ] 2.1 `gate_console.py`: `ACTION_CREATE_PROJECT`;
      `build_gate_action_record` grows `project_id`.
- [ ] 2.2 `kickoff.py`: `create_project()` — human-only; id slugged from the
      name and collision-refused against the register projection; member
      repositories validated against the snapshot-index roster; single-parent
      refusal for a repository already in a project; duplicate refusal via
      the shared (verb, target) index (`COMMISSION_TARGET_KEY` gains
      `create-project → project_id`); `workflow-job` descriptor (workflow
      `project-register-edit`, payload name + repositories) + gate-action
      record; NO register mutation.
- [ ] 2.3 `gate_routes.py`: `EXECUTING_VERBS` gains `create-project`, with
      the structured-refusal response discipline.
- [ ] 2.4 `cli.py`: `gate create-project <name> --repo <id> [--repo <id>…]`
      (`--note`); GateConsole delegate mirroring the other commissions.

## 3. Selector surface

- [ ] 3.1 Project picker in the repo selector: projects listed from the
      register projection; selecting one narrows the roster to member
      repositories; "(ungrouped)" repositories keep today's behaviour.
- [ ] 3.2 Create-project affordance under the gate capability with the
      commission form (name + member checkboxes from the roster); refusals
      render textContent-only; the affordance retires for the session once
      commissioned.
- [ ] 3.3 Pure-model tests: picker narrowing, gate off, already-commissioned,
      member-set validation surface.

## 4. Verification

- [ ] 4.1 Engine + route tests green: accept path, absent member repository,
      single-parent refusal, id collision, duplicate commission, agent-path
      rejection, register untouched by commission.
- [ ] 4.2 Live browser check: picker narrows the roster against the split
      register (D7 content); create-project renders under the gate capability
      and not with it off; zero page errors.
- [ ] 4.3 First real commission by Brett recorded end-to-end and fulfilled
      into `project-register.yaml` (descriptor delivered, register edit
      validated + landed in the aggregation repo).
