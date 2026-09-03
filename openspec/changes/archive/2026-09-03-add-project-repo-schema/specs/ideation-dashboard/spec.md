# ideation-dashboard Specification

## MODIFIED Requirements

### Requirement: Project grouping hierarchy
The dashboard SHALL support a two-level grouping hierarchy over repositories — repositories belong to named projects (a project is a set of repositories) and projects belong to project groups — declared in one schema-versioned project register (`kind: project-register`, neutral schema, instance owned by the aggregation/workspace layer), resolved by the generator into `project` and `project_group` snapshot fields, and surfaced through the project-first header (the project dropdown and the repository filter) — the former header-level roll-up strip is retired (Brett's 2026-08-06 ruling), with the pure grouping model remaining available to any view wanting a roll-up. Repository membership SHALL be multi-parent: a repository MAY live in any number of projects (a project is a named view over repositories, not an owner), the snapshot's singular `project` field SHALL carry the PRIMARY project (the first project in register order declaring the repository, so grouped roll-ups render each repository under exactly one heading), and the snapshot SHALL additionally carry the full membership as an additive `projects` list whose first element is that primary. A project SHALL belong to at most one project group. Grouping is descriptive navigation only: it confers no lifecycle state or authority, and renderers read grouping from the snapshot, never from the register directly.

**ADDED BY `add-project-repo-schema`, and additive in every direction.** The
register SHALL additionally carry an OPTIONAL per-project `schema` election, an
OPTIONAL per-project `reference` recording the document that election followed,
and an OPTIONAL per-project `repository_roles` list assigning each named
repository a `role` of `spec`, `code` or `assembly`. All three SHALL be optional
and additive: a project declaring none of them is legal, renders identically and
is reviewed identically, and `repositories` remains the single membership answer
every existing consumer reads — a repository named in `repository_roles` SHALL
also appear in that project's `repositories`, and at most one repository per
project SHALL carry `role: assembly`. Where an electing project carries its own
assembly-root manifest, the register row SHALL be DERIVABLE FROM that manifest
and the manifest is the SOURCE; the register stays descriptive and is never the
origin of the election. Register writes continue to reach the file only through
the recorded `project-register-edit` commission.

**THE EXISTING POSTURE GOVERNS THE NEW FIELDS UNCHANGED.** Neither `schema`, nor
`reference`, nor a `role` SHALL confer lifecycle state, authority, gate standing
or clearance eligibility over any repository, project or group it names, and a
consumer deriving any permission from one is DEFECTIVE. These are exactly the
fields a later consumer reads as permission, which is why the posture is restated
here rather than left to the sentence above it — and why it is restated a third
and fourth time, in the schema's own description and in the instance header.

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


#### Scenario: A project records a schema election and leg roles
- **WHEN** a register row declares `schema: project-repo-schema`, a `reference`, and a `repository_roles` list naming one assembly, one spec and one code repository
- **THEN** the row is valid and the election is machine-readable by the instrument that already names the group
- **AND** the election confers no lifecycle state, authority, gate standing or clearance eligibility over any repository it names

#### Scenario: A project declares neither field
- **WHEN** a register row carries no `schema`, no `reference` and no `repository_roles`
- **THEN** the row is valid, renders identically and is reviewed identically
- **AND** nothing is owed by a project that declined the schema

#### Scenario: A role names a repository the project does not list
- **WHEN** a `repository_roles` entry names a repository absent from that project's `repositories`
- **THEN** the register is refused, `repositories` being the single membership answer every existing consumer reads

#### Scenario: A project names two assembly roots
- **WHEN** a project assigns `role: assembly` to more than one repository
- **THEN** the register is refused, an electing project having exactly one per-project root

#### Scenario: A consumer reads authority out of a role
- **WHEN** a tool treats `role: spec` as evidence that spec authority lives in that repository
- **THEN** that consumer is defective and its reading MUST NOT be honoured
- **AND** the register has not thereby become a governance boundary, which the ratified prose forbids

#### Scenario: A row disagrees with the project's own manifest
- **WHEN** an electing project's assembly-root manifest and its register row disagree
- **THEN** the manifest is the source and the row is derivable from it
- **AND** the disagreement is reported as drift rather than silently reconciled
