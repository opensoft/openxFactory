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
upstream dependency. The aggregate's `.gitmodules` entry SHALL record the
ABSOLUTE `git@github.com:opensoft/MedxChart.git` remote — the form its sibling
submodules use — and SHALL NOT record a RELATIVE URL and SHALL NOT record a
host-absolute local path. A relative URL is refused for a measured reason and
not a stylistic one: it resolves against whatever URL cloned the SUPERPROJECT,
so on an HTTPS-cloned runner it becomes a plain `https://` URL that a `git@`-only
token rewrite never reaches.

#### Scenario: Aggregate submodules are inspected

- **WHEN** the xFactory superproject lists its submodules
- **THEN** `xFactories/MedxChart` is present
- **AND** `xFactories/openChart` is absent

#### Scenario: The aggregate resolves the MedxChart submodule URL

- **WHEN** the aggregate resolves its `xFactories/MedxChart` submodule URL
- **THEN** the URL is `git@github.com:opensoft/MedxChart.git`, containing neither a relative path nor a host-absolute local path
- **AND** the checked-out gitlink matches the MedxChart commit selected by the aggregate

#### Scenario: The aggregate is cloned over HTTPS by an automated runner

- **WHEN** a runner clones the superproject over HTTPS and initializes its submodules through a `git@`-only token rewrite
- **THEN** the MedxChart clone succeeds, because the recorded URL is already the `git@` form the rewrite reaches
- **AND** a relative `../MedxChart` URL is refused, having resolved to an unrewritable `https://` URL and killed every nightly from 2026-08-24 until `opensoft/xFactory` `386e7ee2` normalized it on 2026-08-25

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
