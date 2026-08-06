# ideation-dashboard

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

#### Scenario: The single-parent rule refuses a double membership
- WHEN a commissioned member repository already belongs to a project in the register projection
- THEN the commission is refused citing that project, because a repository belongs to at most one project

#### Scenario: A duplicate commission is refused
- WHEN a project id already carries a dispatched, undelivered `project-register-edit` commission
- THEN a second `create-project` commission for that id is refused and the refusal names the blocking descriptor

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
