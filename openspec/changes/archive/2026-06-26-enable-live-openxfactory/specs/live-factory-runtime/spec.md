## ADDED Requirements

### Requirement: Live factory pilot flow
The system SHALL support a repeatable live pilot flow from approved OpenSpec
intent through Hermes, Omnigent, Spec Kit, branch work, PR admission, GitHub PR,
Merge Council, Merge Master, and GitHub final enforcement.

#### Scenario: Pilot starts from approved intent
- **WHEN** a live factory pilot feature is selected
- **THEN** it MUST have approved OpenSpec or Hermes change intent before
  Omnigent begins decomposition or Spec Kit work

#### Scenario: Pilot produces end-to-end evidence
- **WHEN** the live pilot reaches merge readiness
- **THEN** evidence MUST link OpenSpec intent, decomposition, Spec Kit artifacts,
  branch, checks, review, PR admission, GitHub PR, Merge Council, and Merge
  Master decision

### Requirement: Approval gates
The live runtime SHALL enforce Hermes approval gates before irreversible or
externally visible transitions.

#### Scenario: Worker reaches a gated transition
- **WHEN** Omnigent reaches Spec Kit entry, clarification answer application,
  implementation start, PR creation, or merge readiness
- **THEN** it MUST stop until Hermes records the required approval

#### Scenario: Approval is missing
- **WHEN** an approval is missing or rejected
- **THEN** Omnigent MUST NOT continue the gated transition

### Requirement: Pilot risk boundary
The initial live pilot SHALL be low-risk, small, and traceable.

#### Scenario: Pilot feature is selected
- **WHEN** a feature is chosen for the first live runtime pilot
- **THEN** it SHOULD target fewer than 3,000 changed lines and MUST remain below
  10,000 changed lines unless Hermes approves an explicit exception
