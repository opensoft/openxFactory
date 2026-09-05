# crystallization-dispatch Specification

## Purpose

Bound the runtime seam where an arriving instance either meets a
crystallized capability or goes to the AI path: one junction at job
admission, before any planner runs — fingerprint, registry lookup,
deterministic fence check, instance risk check, execution at the
capability's rung, post-conditions, emit with provenance — with any
invocation outside it a conformance violation. Keep the AI path permanently
intact as the resolution of every ambiguity: fences are deterministic
predicates a classifier may veto toward but never widen, only `pure` and
`idempotent` effect classes are admitted in this wave, a post-condition
breach is re-served and filed as drift rather than shipped, and every
fallback carries a cause from the controlled taxonomy and accumulates in its
family's frontier queue as evidence for widening. Meter the junction's own
decision overhead against a declared budget, hold the L2 result cache behind
the junction rather than beside it, and keep run records path-invariant so
provenance is the only difference an auditor sees between an AI-served and a
crystal-served run.
## Requirements
### Requirement: The Junction Is The Single Entry Before Planning
Dispatch SHALL sit at job admission, before any planner runs, as the only
entry to every crystallized capability — fingerprint → registry lookup →
deterministic fence check → instance risk check → execute at the
capability's rung → post-conditions → emit with provenance — and invoking
a crystallized capability outside the junction is a conformance
violation.

#### Scenario: No side door exists

- **WHEN** a workflow attempts to execute a registered capability without
  a dispatch record
- **THEN** the execution is nonconformant regardless of outcome

#### Scenario: The junction precedes planning

- **WHEN** an envelope arrives whose family has a serving capability and
  the instance passes fence and risk checks
- **THEN** the instance MUST be served without invoking the planner

### Requirement: Fences Are Deterministic And Ambiguity Falls To The AI Path
Fence evaluation SHALL be a deterministic predicate over envelope and
inputs, ambiguity SHALL resolve to the AI path, and an in-scope
classifier MAY veto toward fallback but MUST NOT extend execution beyond
the fence.

#### Scenario: A gray-zone instance falls back

- **WHEN** an instance cannot be deterministically shown inside the fence
- **THEN** it MUST route to the AI path with fallback cause `fence-miss`

#### Scenario: A classifier cannot widen the fence

- **WHEN** a classifier scores an out-of-fence instance as probably
  servable
- **THEN** the instance still routes to the AI path

### Requirement: Effect-Class Admission Is Enforced
The junction SHALL admit only capabilities whose declared effect class is
`pure` or `idempotent`; `compensable` and `irreversible` families are
fenced out until compensation contracts exist in a successor change.

#### Scenario: A compensable capability is not served

- **WHEN** a registered capability declares effect class `compensable`
- **THEN** every instance of its family routes to the AI path
- **AND** the dispatch record carries cause `risk-override`

### Requirement: Post-Conditions Always Run
Every crystallized output SHALL be evaluated against its spec's
post-conditions before it counts as done; a breach SHALL fall back to the
AI path AND file a drift signal on the capability's health surface.

#### Scenario: A breach is never silently served

- **WHEN** a crystallized output fails a post-condition
- **THEN** the instance MUST be re-served by the AI path
- **AND** the breach MUST appear in the capability's health signals

#### Scenario: Unevaluated post-conditions invalidate the record

- **WHEN** a dispatch record claims the crystallized path without an
  evaluated post-conditions block
- **THEN** the record is invalid and MUST be rejected

### Requirement: Fallbacks Carry Causes And Feed The Frontier
Every fallback SHALL be recorded with a cause from the controlled
taxonomy `no-family-match | fence-miss | execution-error |
postcondition-fail | risk-override | sentinel`, and fence-adjacent
fallbacks SHALL accumulate in the family's frontier queue as the evidence
for fence widening and re-crystallization.

#### Scenario: A causeless fallback is invalid

- **WHEN** a dispatch record shows the AI path for a family with a
  serving capability and carries no fallback cause
- **THEN** the record is invalid and MUST be rejected

### Requirement: Dispatch Overhead Is Budgeted And Metered
The junction's own decision cost SHALL carry a declared budget and be
metered per decision, so the economics of serving always include the cost
of deciding.

#### Scenario: Overhead is visible

- **WHEN** a dispatch decision completes
- **THEN** its record MUST carry the decision's time and credit overhead

### Requirement: The Result Cache Sits Behind The Junction
The L2 result cache SHALL be reachable only as a rung executed through
the junction; a cache lookup that can serve an instance outside dispatch
is a conformance violation.

#### Scenario: No cache side door

- **WHEN** a cached result would satisfy an arriving instance
- **THEN** it may be served only by a junction decision that records the
  L2 path with provenance

### Requirement: Run Records Are Path-Invariant
Run records SHALL have the same shape whether an instance was served by
the AI path or a crystallized capability, with provenance ("served by
capability@version at rung Ln") the only difference an auditor sees, and
the lineage chain run → capability → spec → corpus → episodes MUST
resolve without a seam.

#### Scenario: Audit shape does not fork

- **WHEN** an auditor compares an AI-served and a crystal-served run
  record of the same family
- **THEN** the records MUST differ only in their provenance and path
  fields

#### Scenario: Provenance is mandatory on served instances

- **WHEN** a dispatch record shows the crystallized path without a
  provenance line
- **THEN** the record is invalid and MUST be rejected

