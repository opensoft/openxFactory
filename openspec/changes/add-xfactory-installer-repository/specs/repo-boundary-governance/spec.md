## ADDED Requirements

### Requirement: Neutral installer repository integration
The top-level xFactory aggregation repository SHALL pin the independently
released neutral installer implementation repository at
`installs/xfactory-installer`. The pin MUST reference an exact validated commit,
and repository intent MUST document remote, visibility, ownership, compatibility,
update, and rollback behavior before the pin is treated as supported.

#### Scenario: Installer repository is first integrated
- **WHEN** `opensoft/xFactory-Installer` is added to the aggregation workspace
- **THEN** GitHub visibility MUST be private
- **AND** the parent MUST record the SSH remote and exact validated bootstrap commit
- **AND** a recursive submodule checkout MUST reproduce the repository boundary

#### Scenario: Installer pin is updated
- **WHEN** xFactory adopts a later installer release
- **THEN** the installer repository MUST pass its validation at the proposed commit
- **AND** the parent change MUST record compatibility and rollback evidence

#### Scenario: Installer integration is rolled back
- **WHEN** an installer pin is incompatible or its repository boundary is withdrawn
- **THEN** xFactory MUST restore the previous gitlink or remove the gitlink and `.gitmodules` entry in a dedicated reviewed change
- **AND** immutable repository release evidence MUST remain available
