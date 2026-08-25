## ADDED Requirements

### Requirement: MedxChart pins an independent openChart repository

MedxChart SHALL be a standalone Git repository whose composition boundary pins
the upstream openChart repository at an immutable commit through a nested
submodule and a committed provenance manifest. The pin MUST identify the
repository, revision, and source path without depending on a host-absolute
filesystem path.

#### Scenario: MedxChart is checked out

- **WHEN** a developer checks out MedxChart and initializes its submodules
- **THEN** the nested openChart checkout resolves to the recorded commit
- **AND** the provenance manifest identifies that same commit

#### Scenario: Upstream branch advances

- **WHEN** opensoft/openChart receives a new commit
- **THEN** the existing MedxChart checkout remains at its prior recorded commit
- **AND** no moving branch reference silently changes the composition

### Requirement: xFactory aggregates MedxChart instead of openChart

The xFactory aggregate SHALL track MedxChart at the Medx clinical submodule
boundary and SHALL NOT track a direct `xFactories/openChart` gitlink. The
aggregate's project register and repository documentation MUST identify
MedxChart as the Medx clinical component while preserving openChart as its
upstream dependency.

#### Scenario: Aggregate submodules are inspected

- **WHEN** the xFactory superproject lists its submodules
- **THEN** `xFactories/MedxChart` is present
- **AND** `xFactories/openChart` is absent

#### Scenario: Aggregate is cloned from a compatible workspace

- **WHEN** the aggregate resolves its relative MedxChart submodule URL
- **THEN** the URL does not contain a host-absolute local path
- **AND** the checked-out gitlink matches the MedxChart commit selected by the aggregate

### Requirement: Moving openChart preserves standalone use

The openChart repository SHALL remain independently usable after moving to the
workspace root. Its Git history, origin, tracked content, and standalone
contract MUST remain intact, and its local worktree documentation/configuration
MUST not retain a stale path to the former xFactory checkout.

#### Scenario: Standalone repository is inspected after the move

- **WHEN** openChart is opened from its new workspace-root location
- **THEN** its origin and current commit are unchanged
- **AND** its repository instructions still state that it operates without a
  MedxFactory checkout

#### Scenario: openChart worktree configuration is resolved

- **WHEN** the openChart Spec Kit worktree configuration is used from the new
  location
- **THEN** its configured worktree root resolves to a valid workspace-relative
  sibling location
