---
code_surface: openxFactory (gate-intent / gate-action-record additive extension; dashboard runtime — kickoff.py create_project + shared commission index, gate_routes.py executing route, cli.py entrypoint, GateConsole delegate, selector project picker + scoped roster; tests)
target_release: allocated at realization (next additive contract bundle, per docs/contract-versioning-policy.md)
Status: draft
---

# Proposal: add-project-scoped-selection

## Why

The dashboard's project machinery is built and idle: `project-register.yaml`
declares `projects[].repositories[]`, the generator stamps
repository→project→group onto every snapshot, and the surface renders the
grouping toggles. What a human cannot do is MAKE a project or WORK inside
one. Brett named the gap 2026-08-02 ("lists existing projects and allows for
use to create new project … then allow the user to later select the project,
then a repo in that project or all repos in that project") and ruled the
design 2026-08-06 (staging topic `dashboard-project-scoping`, decisions
D1–D7, zero open questions).

This is EXIT 1 of the topic's three-change series (D6): the create-project
commission and project-scoped selection. The merged all-repos view (D1) is
exit 2 (`add-project-merged-projection`); per-tile repository binding (D3)
is exit 3 (`add-project-tile-repository-binding`). The register's by-role
content split (D7) rides the aggregation repo directly — content, not code.

## What Changes

- ADD gate-console verb `create-project`: a recorded COMMISSION on the
  propose mechanic (D2). The click records a `workflow-job` descriptor
  (workflow `project-register-edit`, target `project_id`, payload: project
  name + member repositories) plus a `create-project` gate-action record;
  the fulfilment applies the edit to the aggregation-owned
  `project-register.yaml`. The dashboard never writes across the repository
  boundary itself. Guards: human gate, member-repository existence against
  the snapshot index's roster, single-parent rule (a repository already in
  a project is refused, citing D7's schema reading), duplicate commission
  via the shared (verb, target) index.
- EXTEND `gate-intent.schema.yaml` and `gate-action-record.schema.yaml`
  additively: `create-project` in the verb/action enums; `project_id` on
  the target; the workflow-job companion conditional (the propose/kickoff
  pattern). No `contract_schema_version` bump.
- MODIFIED `ideation-dashboard`: the selector grows a PROJECT PICKER — the
  register's projects listed from the snapshot-index roster; selecting one
  narrows the repository selector to member repos (one `(repository, ref)`
  snapshot at a time, the honest interim until exit 2); a create-project
  affordance mounts under the gate capability and retires for the session
  once commissioned.
- DECLARE the authority split (D5): the local register is authoritative for
  the development plane ONLY until a tenant project catalog exists; it then
  becomes a derived, replaceable workstation cache per
  `tenant-project-catalog-and-workstation-cache` — never an override.

## Non-Goals

- The merged all-repos projection (exit 2) — until it lands, "all repos in
  a project" renders as the scoped roster, not a merged document.
- Per-tile repository binding and any gate operation outside the served
  checkout (exit 3) — tiles from non-served member repos stay exactly as
  the selector serves them today.
- Project edit/delete verbs, and any `project_groups` affordance (D4).
- The `project-register-edit` fulfilment lane: a terminal session fulfils
  dispatched commissions in the interim, exactly the posture `propose`,
  `kickoff`, and the wheel verbs shipped with.

## Impact

- Contracts: additive enum + target growth on gate-intent /
  gate-action-record; registration at the next additive bundle cut.
- Dashboard runtime: one new commission verb through the existing shared
  index and route discipline; the selector picker is snapshot-index-driven
  (no serving-plane change).
- The aggregation repo is impacted by CONTENT only (fulfilled register
  edits); no aggregation code.
