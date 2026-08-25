# crystallization-decision Specification

## Purpose
TBD - created by archiving change add-crystallizer-contracts. Update Purpose after archive.
## Requirements
### Requirement: Decisions Are The Only Path To Spend
A `crystallization_decision` record SHALL be the only mechanism by which a
crystallization candidate leads to any build, budget consumption, or
capability creation; a decision consumes exactly one open pattern-ledger
candidate, and a funded outcome is valid only inside the tenant's
crystallization budget and clearance envelope (auto-clear under the
envelope, liaison approval above it).

#### Scenario: A candidate without a decision spends nothing

- **WHEN** a `crystallization_candidate` is open and no funded decision
  references it
- **THEN** no `crystallization_build` job for its family is admissible

#### Scenario: Funding requires the budget surface

- **WHEN** a decision's funded outcome lacks a tenant budget or clearance
  reference
- **THEN** the decision is invalid and MUST be rejected

### Requirement: Ceilings Resolve Before Valuation
A decision SHALL resolve the family's rung ceiling before any valuation,
SHALL carry valuation rows only for rungs at or below that ceiling, and
SHALL select a funded rung only from those valued rows — the queue never
carries phantom ROI from ineligible rungs.

#### Scenario: A ceiling bounds the valuation

- **WHEN** the family's task category carries a declared ceiling of L3
- **THEN** the decision's valuation rows MUST NOT include L4, L5, or L6
- **AND** a funded rung above L3 is invalid

#### Scenario: The ceiling is recorded with its source

- **WHEN** a decision is evaluated
- **THEN** it MUST record the resolved ceiling and whether it came from a
  domain overlay declaration or the neutral default

### Requirement: Valuation Discounts Like An Investor
Each valuation row SHALL carry an AI-price deflation factor and a
pattern-survival factor applied to projected savings, and SHALL carry
non-token value terms (latency, determinism, auditability, compliance,
offline) as first-class inputs that may alone justify funding.

#### Scenario: Undiscounted savings are rejected

- **WHEN** a valuation row omits the deflation or survival factor
- **THEN** the decision is invalid and MUST be rejected

#### Scenario: Non-token value can carry a decision

- **WHEN** projected token savings alone do not clear the funding guard
  but declared non-token value (for example a gate that must be
  deterministic) is recorded as decisive
- **THEN** a funded outcome is valid with the non-token rationale recorded

### Requirement: Decisions Select A Shape
A funded decision SHALL fix a target rung from the frozen vocabulary, a
budget cap, an abort rule with declared behavior, and the proof obligations
the built capability must discharge — never a bare build/don't-build
boolean.

#### Scenario: A funded decision is complete

- **WHEN** a decision's outcome is `funded`
- **THEN** it MUST carry rung, budget cap, abort rule, and proof
  obligations
- **AND** a funded decision missing any of the four is invalid

### Requirement: Declined Candidates Are Recorded
A decision SHALL record a declined candidate as a `not_yet` outcome
carrying reasons and re-nomination conditions; a quiet drop is
nonconformant, and not-yet records are calibration evidence like funded
ones.

#### Scenario: A decline carries its conditions

- **WHEN** a decision's outcome is `not_yet`
- **THEN** it MUST carry at least one reason and a re-nomination condition
- **AND** it MUST NOT carry funded fields (rung, budget cap)

### Requirement: The Decision Ladder Matures With Evidence
Tenants SHALL start on decision-ladder rungs 1–2 (human judgment over an
evidence packet; count-threshold nomination with human clearance), and a
rung-3 expected-value decision SHALL be valid only when it references
calibration evidence (scored forecasts and estimate actuals) supporting
its model.

#### Scenario: An EV decision without calibration is rejected

- **WHEN** a decision declares decision-ladder rung 3 and references no
  scored forecasts or estimate actuals
- **THEN** the decision is invalid and MUST be rejected

### Requirement: The Rung Vocabulary Is Frozen
The `automation_rung` vocabulary SHALL be the controlled enum L0–L6 (cold
solve; recall-assisted solve; memoized result; frozen playbook; specialist
executors; code with AI edges; pure code), carried by decisions,
capability bindings, and dispatch records; a funded decision SHALL select
from L2–L6, since L0/L1 are the status quo and equal a `not_yet` outcome.

#### Scenario: An unknown rung is rejected

- **WHEN** any crystallization record carries a rung outside L0–L6
- **THEN** the record is invalid and MUST be rejected

#### Scenario: Funding the status quo is a decline

- **WHEN** evaluation concludes the family should stay at L0 or L1
- **THEN** the decision outcome MUST be `not_yet` with the conclusion as
  its reason, never a funded L0/L1

