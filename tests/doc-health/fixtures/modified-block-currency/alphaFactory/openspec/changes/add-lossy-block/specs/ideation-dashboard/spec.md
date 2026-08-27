# ideation-dashboard Specification Delta

## MODIFIED Requirements

### Requirement: Composed views are read-only with a repository jump
A composed view SHALL be read-only. It SHALL offer a jump to the owning
repository, and the jump SHALL name that repository in the spelling
`openxFactory` uses.

The selector MUST show exactly the available catalog entries and their
data-handling badges, and MUST show their provider lanes too.

The jump SHALL read `.openspec.yaml` for its repository name. It SHALL NOT
guess.

- a composed view MUST NOT offer a gate verb

#### Scenario: Gate verbs hide on a composed view
- **WHEN** a composed view is open
- **THEN** every gate verb MUST be hidden
- **AND** the jump MUST remain available
- **THEN** it MUST name the owning repository

## ADDED Requirements

### Requirement: A composed view carries a provider lane
A composed view SHALL carry a provider lane.

#### Scenario: The lane renders
- **WHEN** a composed view renders
- **THEN** the lane MUST appear

#### Scenario: The lane is read-only
- **WHEN** the lane renders
- **THEN** it MUST be read-only

#### Scenario: The lane names its provider
- **WHEN** the lane renders
- **THEN** it MUST name the provider

#### Scenario: The lane refuses an edit
- **WHEN** an edit is attempted
- **THEN** the lane MUST refuse it

#### Scenario: The lane hides with the view
- **WHEN** the view closes
- **THEN** the lane MUST hide

#### Scenario: An absent provider is reported
- **WHEN** no provider resolves
- **THEN** the lane MUST say so

#### Scenario: The lane refreshes with the view
- **WHEN** the view refreshes
- **THEN** the lane MUST refresh
