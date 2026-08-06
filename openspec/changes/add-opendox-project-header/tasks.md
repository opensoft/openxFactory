# Tasks: add-opendox-project-header

## 1. Contracts

- [ ] 1.1 Extend `gate-intent.schema.yaml` additively: `edit-project` in the
      verb enum; conditional `edit-project → target.project_id` (the field
      exists since create-project). Header note naming this change.
- [ ] 1.2 Extend `gate-action-record.schema.yaml` the same way, including
      the workflow-job companion conditional.
- [ ] 1.3 Conformance tests: valid intent + record for `edit-project`;
      missing companion rejected; missing `project_id` rejected.
- [ ] 1.4 Contract registration at the next additive bundle cut (rides with
      create-project's 1.4).

## 2. Engine + routes

- [ ] 2.1 `kickoff.py`: `edit_project()` — human-only; guards in the ruled
      order (project existence, additions in the roster∪register universe,
      removals currently members, at-least-one-member floor, duplicate via
      the shared index); descriptor payload `add`/`remove` (either may be
      empty, not both); NO register mutation. `COMMISSION_TARGET_KEY`
      already maps `project_id`.
- [ ] 2.2 `gate_routes.py`: `EXECUTING_VERBS` gains `edit-project` with the
      structured-refusal discipline; `cli.py`: `gate edit-project
      <project-id> [--add <repo>…] [--remove <repo>…] (--note)`; GateConsole
      delegate.

## 3. Header redesign

- [ ] 3.1 Brand: "Opensoft openDox" in the brand line and `<title>`; the
      repo chip retires.
- [ ] 3.2 Project dropdown (D13): "New Project" first (opens the rehomed
      create form, restoring the previous selection), then the projects,
      pending entries preserved; default = stored scope else first project.
- [ ] 3.3 Repo filter (D14): icon + popover of the current project's
      members; single-select stores the key and reloads; active repository
      highlighted; unavailable members say why; "All repositories" first,
      disabled with the merged-view note (armed by
      add-project-merged-projection when it lands).
- [ ] 3.4 Manage mode (D15): checkbox per register repository seeded from
      membership; apply diffs into an edit-project commission; pending
      membership changes badge until fulfilment; refusals textContent-only.
- [ ] 3.5 Model tests: dropdown rows/default resolution, filter rows,
      manage-mode diffing, pending badges; engine + wire tests for
      edit-project's guards and accept path.

## 4. Verification

- [ ] 4.1 Full suites green; strict validation green.
- [ ] 4.2 Live browser check: the renamed header, dropdown default and New
      Project flow, filter single-select switching, manage mode
      commissioning (accept + refusal), gate-off degrade (dropdown + filter
      render read-only, New Project and manage mode absent); zero page
      errors.
- [ ] 4.3 First real edit-project commission by Brett, fulfilled into the
      aggregation register.
