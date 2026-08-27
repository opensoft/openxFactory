# rewrap-cases Specification

## Purpose
SYNTHESIZED. A requirement whose every paragraph, bullet and scenario line a
block re-wraps while restating it completely.

## Requirements

### Requirement: A re-wrapped restatement is still a restatement
A composed view SHALL be read-only, and it SHALL offer a jump to the owning
repository in the spelling the aggregation uses.

The selector MUST show exactly the available catalog entries. It MUST NOT guess
at an entry the catalog does not carry.

- every loaded editor MUST remain usable while a composed view is open
- a composed view MUST NOT offer a gate verb

**CORRECTED 2026-08-27 ON A RULING — this note is one unit and it wraps.**

#### Scenario: The view opens
- **WHEN** a composed view is open
- **THEN** every gate verb MUST be hidden and the jump MUST remain available

#### Scenario: An edit is attempted
- **WHEN** an edit is attempted on a read-only composed view
- **THEN** the view MUST refuse it and MUST say why
