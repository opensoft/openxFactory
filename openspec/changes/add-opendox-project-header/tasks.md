# Tasks: add-opendox-project-header

## 1. Contracts

- [x] 1.1 Extend `gate-intent.schema.yaml` additively: `edit-project` in the
      verb enum; conditional `edit-project → target.project_id` (the field
      exists since create-project). Header note naming this change.
- [x] 1.2 Extend `gate-action-record.schema.yaml` the same way, including
      the workflow-job companion conditional.
- [x] 1.3 Conformance tests: valid intent + record for `edit-project`;
      missing companion rejected; missing `project_id` rejected.
- [ ] 1.4 Contract registration at the next additive bundle cut (rides with
      create-project's 1.4).

## 2. Engine + routes

- [x] 2.1 `kickoff.py`: `edit_project()` — human-only; guards in the ruled
      order (project existence, additions in the roster∪register universe,
      removals currently members, at-least-one-member floor, duplicate via
      the shared index); descriptor payload `add`/`remove` (either may be
      empty, not both); NO register mutation. `COMMISSION_TARGET_KEY`
      already maps `project_id`.
- [x] 2.2 `gate_routes.py`: `EXECUTING_VERBS` gains `edit-project` with the
      structured-refusal discipline; `cli.py`: `gate edit-project
      <project-id> [--add <repo>…] [--remove <repo>…] (--note)`; GateConsole
      delegate.

## 3. Header redesign

- [x] 3.1 Brand: "Opensoft openDox" in the brand line and `<title>`; the
      repo chip retires.
- [x] 3.2 Project dropdown (D13): "New Project" first (opens the rehomed
      create form, restoring the previous selection), then the projects,
      pending entries preserved; default = stored scope else first project.
- [x] 3.3 Repo filter (D14): icon + popover of the current project's
      members; single-select stores the key and reloads; active repository
      highlighted; unavailable members say why; "All repositories" first,
      disabled with the merged-view note (armed by
      add-project-merged-projection when it lands).
- [x] 3.4 Manage mode (D15): checkbox per register repository seeded from
      membership; apply diffs into an edit-project commission; pending
      membership changes badge until fulfilment; refusals textContent-only.
- [x] 3.5 Model tests: dropdown rows/default resolution, filter rows,
      manage-mode diffing, pending badges; engine + wire tests for
      edit-project's guards and accept path.

## 4. Verification

- [x] 4.1 Full suites green; strict validation green.
- [x] 4.2 Live browser check: the renamed header, dropdown default and New
      Project flow, filter single-select switching, manage mode
      commissioning (accept + refusal), gate-off degrade (dropdown + filter
      render read-only, New Project and manage mode absent); zero page
      errors.
      (Verified 2026-08-06, headless Chromium against gate-on + gate-off
      serves of this checkout: title + brand "Opensoft openDox", repo chip
      gone; the dropdown reads New Project… then the five register projects,
      defaulting to `core`; New Project opens the create form and restores
      the selection; the filter reads "⧩ Core Contracts" with the ARMED
      all-repos line (exit 2's derived aggregate), the member row, and
      manage members with membership-seeded checkboxes; switching projects
      re-renders the filter; gate-off disables New Project and drops manage.
      Zero console errors, page errors, and >=400 responses on both drives.
      The wire accept + refusal paths are pinned by test_edit_project.py's
      real-HTTP group.)
- [ ] 4.3 First real edit-project commission by Brett, fulfilled into the
      aggregation register.

## 5. The dropdown-like filter (design D-h / topic D16, Brett's 2026-08-06 annotation)

- [x] 5.1 Filter popover rework: "＋ add repository…" first (inline
      candidate select over roster∪register minus members; commissions a
      single-addition edit), per-row eyeball visibility indicator (active
      repo, or any member under the project's merged view), and a two-click
      trash control commissioning the single removal; manage mode retires.
- [x] 5.2 Model: `addableRepositories` + `repositoryVisible` (manageDiff
      retires with manage mode); node tests updated.
- [x] 5.3 Live browser check re-run on the reworked popover.
- [x] 5.4 Brett's 2026-08-06 follow-up annotations: the create form becomes
      a LABELED PANEL (heading, captioned name field and member list, a
      what-this-does note, "commission project"/"cancel"), and the add-repo
      flow becomes ONE self-closing dropdown (placeholder line = the
      affordance; choosing commissions and the select closes, like the
      project selector).
- [x] 5.5 The live check exposed that explicit `display:flex` on the
      popover/panel defeated the `hidden` attribute (the filter popover
      could never close); restated `[hidden] { display:none }` for both and
      verified full open/close cycles with zero page errors.
- [x] 5.6 Brett's 2026-08-06 second annotation round: the filter box names
      its content (single member -> the repository's name; several ->
      "N Repos"); theme + settings pin to the page's top-right as chrome;
      the header-level grouping roll-up strip retires (the project dropdown
      and filter are where grouping surfaces; the pure grouping model stays
      available) — the scoped-selection delta's grouping requirement
      restated accordingly. Live-checked: labels, corner placement, settings
      panel, no roll-up row, zero page errors.
- [x] 5.7 Brett's 2026-08-06 empty-project ruling ("I think it is better if
      we allow a project to exist without a repo defined"): the register
      schema admits an empty `repositories` set (the task-2.6 minItems rule
      reversed; the negative example converts to a positive one), the
      create-project non-empty guard and the edit-project last-member floor
      are dropped, the route accepts an absent/empty list, and the create
      panel marks members optional. A project is created first and gains
      members later through edit-project. Engine/wire/UI checks green.
