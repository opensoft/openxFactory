# Conditional Lane Attribution

## Purpose

Keep the required repository lane-line check consistent with conditional lane membership while retaining validation of supplied declarations.

## ADDED Requirements

### Requirement: Lane attribution is conditional
The check SHALL accept a PR with no lane declaration. Sessions outside a lane SHALL need no invented lane, claim or enrollment. A lane-bound author MUST still declare its actual lane; absence alone SHALL NOT establish non-membership.

#### Scenario: Outside-lane PR has no declaration
- **WHEN** a human-authored PR has prose or an empty body without a lane declaration
- **THEN** lane-line succeeds without requiring a tag or register write

### Requirement: Supplied attribution remains strict
A supplied lane declaration MUST be unique, use the established `Lane: [A-Za-z0-9-]+` format with an optional parenthesized suffix, and occupy the first nonempty body line. Malformed, misplaced, or duplicate declarations MUST fail.

#### Scenario: Valid attribution
- **WHEN** the first nonempty line is a valid lane declaration and no second declaration exists
- **THEN** lane-line succeeds, including for CRLF and blank leading lines

#### Scenario: Malformed or misplaced attribution
- **WHEN** a declaration has no valid name, uses invalid characters or casing, occurs later in the body, or occurs more than once
- **THEN** lane-line fails with a useful declaration-format message

### Requirement: Preserve enforcement and input isolation
The workflow SHALL preserve its existing check identity, triggers, permissions and bot-exemption behavior. PR text MUST be treated as data through environment variables and MUST NOT be evaluated as shell code. No branch-protection or approval rule SHALL change.

#### Scenario: Body contains shell syntax
- **WHEN** ordinary PR prose contains command substitution or workflow-command-like text
- **THEN** that text is not executed or re-emitted as a workflow command

#### Scenario: Existing bot exemption
- **WHEN** the PR author matches this repository's existing bot exemption
- **THEN** the existing exemption and its check conclusion remain unchanged
