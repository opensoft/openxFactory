# ideation-dashboard

## MODIFIED Requirements

### Requirement: Project grouping hierarchy
The dashboard SHALL support a two-level grouping hierarchy over repositories — repositories belong to named projects (a project is a set of repositories) and projects belong to project groups — declared in one schema-versioned project register (`kind: project-register`, neutral schema, instance owned by the aggregation/workspace layer), resolved by the generator into `project` and `project_group` snapshot fields, and surfaced through the project-first header (the project dropdown and the repository filter) — the former header-level roll-up strip is retired (Brett's 2026-08-06 ruling), with the pure grouping model remaining available to any view wanting a roll-up. Repository membership SHALL be multi-parent: a repository MAY live in any number of projects (a project is a named view over repositories, not an owner), the snapshot's singular `project` field SHALL carry the PRIMARY project (the first project in register order declaring the repository, so grouped roll-ups render each repository under exactly one heading), and the snapshot SHALL additionally carry the full membership as an additive `projects` list whose first element is that primary. A project SHALL belong to at most one project group. Grouping is descriptive navigation only: it confers no lifecycle state or authority, and renderers read grouping from the snapshot, never from the register directly.

#### Scenario: A project spans several repositories
- **WHEN** the project register maps more than one repository to a project
- **THEN** the project roll-up MUST aggregate those repositories' snapshot entries under one project heading
- **AND** per-repository detail remains reachable beneath it

#### Scenario: A repository lives in several projects
- **WHEN** the register declares one repository under more than one project
- **THEN** the register is valid, the repository's snapshot carries the first-declaring project as `project` and every declaring project in `projects`
- **AND** project-scoped selection offers the repository under each of its projects

#### Scenario: Projects roll up into a project group
- **WHEN** the register assigns projects to a project group
- **THEN** the group view MUST aggregate its member projects' tallies from the snapshot

#### Scenario: A repository is absent from the register
- **WHEN** a snapshot's `repository` has no register entry
- **THEN** it MUST render ungrouped (its own implicit project) without failing the dashboard

#### Scenario: The register changes
- **WHEN** the project register is edited
- **THEN** grouping updates only through snapshot regeneration — rendered grouping is never hand-edited

## ADDED Requirements

### Requirement: Project creation is a recorded commission
The dashboard SHALL offer a `create-project` verb on the human gate console that records a `workflow-job` descriptor (workflow `project-register-edit`, carrying the proposed project id, display name, and member repository ids) plus a `create-project` gate-action record naming the human — and SHALL NOT write the project register itself: the register is aggregation-owned, and the fulfilment of the recorded commission is what applies the edit.

#### Scenario: A human creates a project
- WHEN a human on the loopback gate console commissions a project with a name and member repositories drawn from the selector roster
- THEN a `workflow-job` descriptor and a `create-project` gate-action record are written under the served checkout's records tree
- AND `project-register.yaml` is not modified by the dashboard

#### Scenario: A member repository is not in the roster
- WHEN a commissioned member repository id is absent from the snapshot-index roster
- THEN the commission is refused with the unknown id as the reason and nothing is persisted

#### Scenario: A repository joins a second project
- WHEN a commissioned member repository already belongs to a project in the register projection
- THEN the commission is accepted — repository membership is multi-parent, and a project is a named view over repositories, not an owner

#### Scenario: A duplicate commission is refused
- WHEN a project id already carries a dispatched, undelivered `project-register-edit` commission
- THEN a second `create-project` commission for that id is refused and the refusal names the blocking descriptor

#### Scenario: A commissioned project is visible as pending
- WHEN a `create-project` commission is dispatched and not yet delivered
- THEN the register projection reports it on a `pending` plane distinct from the register's projects, and the picker renders it as a clearly-marked, non-selectable pending entry
- AND the pending entry never scopes the roster and disappears in favour of the register's own entry once the fulfilment lands

### Requirement: Project-scoped repository selection
The repository selector SHALL offer a project picker listing the register's projects, and selecting a project SHALL narrow the selector roster to that project's member repositories while the active snapshot remains a single `(repository, ref)` key.

#### Scenario: A project scopes the roster
- WHEN a human selects a project in the picker
- THEN the repository selector lists only that project's member repositories
- AND choosing one serves that single repository's snapshot exactly as an unscoped selection would

#### Scenario: Unregistered repositories keep their standing
- WHEN a repository is absent from the project register
- THEN it renders ungrouped exactly as the register contract already specifies, and clearing the project selection restores the full roster

### Requirement: Local register authority is declared against the tenant catalog
The project register consumed by this capability SHALL be authoritative for the development plane only until a tenant project catalog exists; once a runtime catalog is authoritative for project-to-repository composition, the local register SHALL be treated as a derived, replaceable workstation cache and SHALL NOT override the catalog.

#### Scenario: The runtime twin lands
- WHEN a tenant project catalog becomes authoritative for project composition
- THEN the dashboard's register is consumed as a derived projection of it
- AND a local edit is not an override of the catalog
