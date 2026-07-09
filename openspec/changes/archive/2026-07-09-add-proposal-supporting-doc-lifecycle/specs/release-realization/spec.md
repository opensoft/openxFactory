## ADDED Requirements

### Requirement: Proposal support archive gate
An OpenSpec change with proposal supporting documents SHALL NOT archive until
all accepted normative claims have been represented in its proposal, design, or
spec delta; any proposal hybrid has completed its final source import; strict
validation passes; and the supporting folder has been converted into a
deterministic bundle with a readable, verifiable manifest. Packaging SHALL wrap
the normal OpenSpec archive operation rather than replace spec promotion.

#### Scenario: Supporting material contains uncaptured accepted claims
- **WHEN** accepted normative content exists only in `supporting-docs/`
- **THEN** the change MUST remain active until that content is represented in the proposal, design, or spec delta

#### Scenario: Archive preflight succeeds
- **WHEN** implementation and repository tests pass, strict OpenSpec validation passes, final source returns complete, and the support bundle verifies
- **THEN** the normal OpenSpec archive operation MAY run
- **AND** canonical spec promotion MUST proceed unchanged
