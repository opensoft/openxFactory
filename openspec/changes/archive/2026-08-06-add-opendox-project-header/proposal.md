---
code_surface: openxFactory (gate-intent / gate-action-record additive `edit-project` extension; dashboard runtime — kickoff.py edit_project + route + CLI + GateConsole delegate; web header redesign: brand, project dropdown, repo filter popover + manage mode; tests)
target_release: allocated at realization (next additive contract bundle, per docs/contract-versioning-policy.md)
Status: ratified
Ratified by: Brett's "ratify both and realize them in order" on 2026-08-06, with the header design round (topic D12–D15) carried as decided
Amended: 2026-08-07 by Brett's queued-edits ruling (topic D18) — the edit-project single-flight guard is dropped in favour of queued commissions validated against pending-applied state; see tasks §6
---

# Proposal: add-opendox-project-header

## Why

Brett's header design round (2026-08-06, topic decisions D12–D15): the
header grew by accretion — brand, repo chip, project picker, repo select,
"+ project", regenerate — and reads as noise ("this is confusing for the
user"). The redesign makes the PROJECT the header's organizing idea: you
are always in a project, the project decides which repositories are in
play, and membership is editable from the same control.

## What Changes

- RENAME the dashboard "Opensoft openDox" (D12): the brand line and page
  title; the repo chip retires (the freshness header already names
  `repo @ ref`).
- REPLACE the picker cluster with the PROJECT DROPDOWN (D13): first line
  "New Project" (opens the existing create-commission form, rehomed),
  then the register's projects. Default: last-used (session-stored),
  falling back to the first register project. Pending create-project
  commissions keep their non-selectable "(commissioned — pending
  fulfilment)" entries.
- REPLACE the repo select with the REPO FILTER (D14): a filter icon
  opening a popover listing the current project's member repositories;
  selecting one makes it the active served repository (the ratified
  reload-per-switch posture). An "All repositories" line renders on top,
  disabled with a coming-merged-view note until
  `add-project-merged-projection` lands, then it selects the project's
  derived aggregate.
- ADD gate verb `edit-project` (D15): a commission on the create-project
  mechanic — the filter popover's manage mode offers a checkbox per
  register repository; applying records a `project-register-edit`
  workflow-job carrying `add`/`remove` member lists plus an `edit-project`
  gate-action record. Guards: human gate, project existence, roster
  membership for additions, the at-least-one-member floor for removals,
  duplicate via the shared (verb, target) index. The register is edited
  only by the fulfilment; pending membership changes badge in the popover
  until it lands.
- EXTEND `gate-intent.schema.yaml` / `gate-action-record.schema.yaml`
  additively: `edit-project` in the enums, `project_id` target (already
  present), workflow-job companion. Registration at the next additive
  bundle cut.

## Non-Goals

- The merged view itself (`add-project-merged-projection`, awaiting
  ratification) — this change only reserves its "All repositories" line.
- Project deletion or rename verbs; group affordances (D4 stands).
- Any register write from the dashboard (D2 stands: commissions only).

## Impact

- Contracts: one additive verb; no `contract_schema_version` bump.
- Dashboard runtime: one new commission verb on the existing shared
  index; the header restructure is view-only.
- The old `#repopick` select and "+ project" button retire; the picker's
  scoping semantics (exit 1) are unchanged underneath.
