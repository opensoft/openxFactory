# ideation-dashboard Specification

## Purpose
The fixture capability. Eight scenarios on one requirement, which is the shape
issue #329's instance had.

## Requirements

### Requirement: Composed views are read-only with a repository jump
A composed view SHALL be read-only. It SHALL offer a jump to the owning
repository, and the jump SHALL name that repository in the spelling
`openxFactory` uses.

The selector MUST show exactly the available catalog entries and their
data-handling badges.

- every loaded editor MUST remain usable while a composed view is open
- a composed view MUST NOT offer a gate verb

**CORRECTED 2026-08-25 ON BRETT'S RULING — this note is one unit. It carries
two sentences and neither means anything apart from the other.**

#### Scenario: Gate verbs hide on a composed view
- **WHEN** a composed view is open
- **THEN** every gate verb MUST be hidden
- **AND** the jump MUST remain available
- **AND** the selector MUST stay read-only

#### Scenario: The menu offers a routing rule
- **WHEN** the menu opens
- **THEN** a routing rule MUST be offered

#### Scenario: A fourth provider verb is proposed
- **WHEN** a fourth provider verb is proposed
- **THEN** the run MUST refuse it

#### Scenario: The jump names its repository
- **WHEN** the jump is rendered
- **THEN** it MUST name the owning repository

#### Scenario: A read-only view refuses an edit
- **WHEN** an edit is attempted
- **THEN** the view MUST refuse it

#### Scenario: The badge set is complete
- **WHEN** the selector renders
- **THEN** every data-handling badge MUST appear

#### Scenario: A stale composed view refreshes
- **WHEN** the source moves
- **THEN** the view MUST refresh

#### Scenario: An empty composed view says so
- **WHEN** no tile resolves
- **THEN** the view MUST say so
