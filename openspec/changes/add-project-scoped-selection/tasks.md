# Tasks: add-project-scoped-selection

## 1. Contracts

- [x] 1.1 Extend `gate-intent.schema.yaml` additively: `create-project` in
      the verb enum; `project_id` on `target`; conditional `create-project →
      target.project_id`. Header note naming this change as the growth
      source; no `contract_schema_version` bump.
- [x] 1.2 Extend `gate-action-record.schema.yaml` the same way, including
      the `artifacts contains workflow-job` companion conditional.
- [x] 1.3 Schema conformance tests: one valid intent and one valid record
      for `create-project`; a record missing its workflow-job companion
      rejected; a record without `target.project_id` rejected.
- [ ] 1.4 Contract registration at the next additive bundle cut per
      `docs/contract-versioning-policy.md`.

## 2. Engine + routes

- [x] 2.1 `gate_console.py`: `ACTION_CREATE_PROJECT`;
      `build_gate_action_record` grows `project_id`.
- [x] 2.2 `kickoff.py`: `create_project()` — human-only; id slugged from the
      name and collision-refused against the register projection; member
      repositories validated against the snapshot-index roster; single-parent
      refusal for a repository already in a project; duplicate refusal via
      the shared (verb, target) index (`COMMISSION_TARGET_KEY` gains
      `create-project → project_id`); `workflow-job` descriptor (workflow
      `project-register-edit`, payload name + repositories) + gate-action
      record; NO register mutation.
- [x] 2.3 `gate_routes.py`: `EXECUTING_VERBS` gains `create-project`, with
      the structured-refusal response discipline.
- [x] 2.4 `cli.py`: `gate create-project <name> --repo <id> [--repo <id>…]`
      (`--note`); GateConsole delegate mirroring the other commissions.

## 3. Selector surface

- [x] 3.1 Project picker in the repo selector: projects listed from the
      register projection; selecting one narrows the roster to member
      repositories; "(ungrouped)" repositories keep today's behaviour.
- [x] 3.2 Create-project affordance under the gate capability with the
      commission form (name + member checkboxes from the roster); refusals
      render textContent-only; the affordance retires for the session once
      commissioned.
- [x] 3.3 Pure-model tests: picker narrowing, gate off, already-commissioned,
      member-set validation surface.

## 4. Verification

- [x] 4.1 Engine + route tests green: accept path, absent member repository,
      single-parent refusal, id collision, duplicate commission, agent-path
      rejection, register untouched by commission.
- [x] 4.2 Live browser check: picker narrows the roster against the split
      register (D7 content); create-project renders under the gate capability
      and not with it off; zero page errors.
      (Verified 2026-08-06, headless Chromium against two loopback serves of
      this checkout with the D7-split register discovered one level up. Gate
      ON: the picker lists the four role projects from
      `/project-register.json`, core-scoping and clearing behave, the
      `+ project` affordance renders, and — every published repository being
      owned post-split — the form honestly reports no candidates with submit
      disabled; a wire probe returned the engine's single-parent refusal
      naming `openxFactory (in 'core')`. Gate OFF: the picker stays (selection
      is read-only) and the affordance is absent. Zero console errors,
      uncaught page errors, and >=400 responses on both drives. Multi-repo
      narrowing is pinned by the node model tests, the local serve having a
      single-entry roster.)
- [ ] 4.3 First real commission by Brett recorded end-to-end and fulfilled
      into `project-register.yaml` (descriptor delivered, register edit
      validated + landed in the aggregation repo).

## 5. Multi-parent membership (design D-d, Brett's 2026-08-06 ruling)

- [x] 5.1 Contracts: register schema prose rules rewritten (repository
      membership multi-parent; project→group stays single-parent); snapshot
      schema gains the additive `projects` list beside the singular PRIMARY
      `project`; register validator drops `project-multi-parent-repo`.
- [x] 5.2 Adapter + generator: `ProjectRegisterAdapter.projects_of()` (full
      membership, register order, primary first); the generator stamps
      `projects` beside `project`/`project_group`.
- [x] 5.3 Engine + surface: the create-project single-parent guard dropped
      (an owned member is legal; roster guard unchanged); the affordance
      offers ALL roster repositories as candidates.
- [x] 5.4 Tests: owned-member acceptance (engine + wire), adapter
      primary/full-list resolution, validator no longer errs on shared
      membership; suites green.
- [x] 5.5 Register content: MedxFactory joins `medx-clinical` while staying
      in `domains` (aggregation-repo edit — the ruling's first beneficiary).
