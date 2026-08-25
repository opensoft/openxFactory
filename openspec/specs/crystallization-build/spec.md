# crystallization-build Specification

## Purpose
TBD - created by archiving change add-crystallizer-contracts. Update Purpose after archive.
## Requirements
### Requirement: Specs Are Mined From Episodes
A `crystallization_spec` SHALL derive its requirements from the family's
episode corpus — invariants, parameters with observed ranges, branches
from divergent episodes, and counterexamples from failure-labeled episodes
— with every mined element citing episode references, and declared
evidence bounds (episode count, parameter ranges, time span) as part of
the spec.

#### Scenario: A spec cites its evidence

- **WHEN** a `crystallization_spec` is submitted to intake
- **THEN** every invariant, parameter, branch, and counterexample MUST
  carry at least one episode reference

#### Scenario: Happy paths alone are rejected

- **WHEN** a spec's mined content contains zero counterexamples
- **THEN** intake MUST reject it — a corpus without failure cases cannot
  define refusal behavior

### Requirement: The Acceptance Corpus Is The Operative Contract
The spec SHALL carry a digest-pinned acceptance corpus — curated episode
references, equivalence predicates declared per output type (never
byte-equality goldens for semantic outputs), and cassettes for
`record-replay` episodes — and the spec SHALL be regenerable: the same
corpus digest and miner version produce the same spec.

#### Scenario: A byte golden posing as a predicate is rejected

- **WHEN** an equivalence predicate for a prose output type declares
  byte equality
- **THEN** the spec is invalid and MUST be rejected

#### Scenario: Regeneration is deterministic

- **WHEN** the miner re-runs with an unchanged corpus digest and miner
  version
- **THEN** the resulting spec MUST be identical

### Requirement: The Scope Fence Is A Requirement Artifact
The spec SHALL include a deterministic scope-fence predicate over envelope
and inputs, derived conservatively from observed support, digest-pinned,
and consumed verbatim by dispatch — never runtime configuration invented
at deploy time; fence widening is a spec revision carrying fresh evidence.

#### Scenario: A spec without a fence fails intake

- **WHEN** a `crystallization_spec` lacks a scope-fence artifact
- **THEN** intake MUST reject it

#### Scenario: Widening requires evidence

- **WHEN** a fence revision claims inputs outside the corpus's observed
  support
- **THEN** the revision MUST cite fallback episodes covering the widened
  region or be rejected

### Requirement: Effect Class Is Declared At Spec Time
Every spec SHALL declare the capability's `effect_class` from the frozen
vocabulary `pure | idempotent | compensable | irreversible`; the class is
part of the capability's identity, consumed by dispatch admission
(successor change), and a missing or unknown class fails intake.

#### Scenario: Missing effect class fails intake

- **WHEN** a `crystallization_spec` omits `effect_class`
- **THEN** intake MUST reject it

### Requirement: Builds Are Ordinary Governed Jobs
A crystallization build SHALL run as a normal governed job
(`job_type: crystallization_build`) executed by codexFactory for every
consuming domain, with the consuming domain owning fitness gates and
domain review — no parallel build machinery exists, and build jobs are
themselves episodes in the pattern ledger.

#### Scenario: A non-engineering domain's pattern is built by codexFactory

- **WHEN** a MedxFactory family's funded decision produces a build job
- **THEN** codexFactory executes it under its normal lanes
- **AND** MedxFactory's fitness gate MUST pass before the artifact is
  accepted

### Requirement: Provenance Chains Without Gaps
Every built artifact SHALL carry a provenance manifest pinning episode
digests, corpus digest, spec identity and digest, builder identity and
version, and toolchain pins; maintenance SHALL be regeneration-first, and
a hand-patch is a gated exception that must fold back into spec or corpus
and re-derive.

#### Scenario: The chain resolves end to end

- **WHEN** an auditor starts from a built artifact's provenance manifest
- **THEN** capability → spec → corpus → episodes → original runs MUST
  resolve without a gap

#### Scenario: A hand-patch cannot persist

- **WHEN** an artifact's content no longer matches regeneration from its
  pinned spec and corpus
- **THEN** the mismatch is a finding, and the resolution MUST be a spec or
  corpus revision plus regeneration, never a silent re-pin

### Requirement: Dry-Run And Leak Scan Are Build Acceptance Criteria
A build SHALL NOT be accepted unless the artifact demonstrates a
dry-run/simulation mode and passes the generated-artifact data-leak scan —
no literal in the artifact may be traceable to a single tenant's episode
payloads.

#### Scenario: No dry-run, no acceptance

- **WHEN** a built artifact cannot execute in dry-run mode
- **THEN** the build fails acceptance regardless of corpus results

#### Scenario: A memorized tenant constant fails the scan

- **WHEN** the leak scan finds an artifact literal traceable to one
  tenant's episode payloads
- **THEN** the build fails acceptance and the finding is recorded

### Requirement: Builds Run Under Budget Caps With Declared Abort
Every build SHALL run under its decision's budget cap with declared abort
behavior — stop at the cap, persist partial work, return actuals for
calibration — and the artifact SHALL declare its packaging and residence
with a digest so registry pinning (successor change) has a stable target.

#### Scenario: An overrun aborts honestly

- **WHEN** a build reaches its decision's abort threshold
- **THEN** it MUST stop, persist partials, and return actuals
- **AND** continuation requires a new or amended funded decision

#### Scenario: Residence is declared

- **WHEN** a build is accepted
- **THEN** the artifact record MUST carry packaging, residence, and digest

