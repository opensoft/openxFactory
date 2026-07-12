# doc-health Delta: Ideation Readiness Lane

## ADDED Requirements

### Requirement: Ideation readiness lane
The doc-health capability SHALL include an ideation readiness lane: a
bounded, non-mutating worker pass — following the same execution split and
bounded-worker pattern as the agentic semantic sweep and the
document-cataloger and ideation-organizer lanes — that maintains the
promoted `ideation-cross-reference` index and emits `ideation-readiness`
findings, including the extension-fit citation finding when a fit note
cites only an archived change folder rather than a promoted spec or
capability. Lane output SHALL be recommendations with `pending_review`
disposition, resolution class `contested`, and severity at most `warning`;
the lane MUST NOT block merges and MUST NOT open regression issues in v1.
The strict index validator runs in the existing per-repo validator
preflight; this lane adds no deterministic check family.

#### Scenario: The nightly lane executes
- **WHEN** the readiness lane runs in the nightly workflow
- **THEN** it runs after the deterministic pass against the same inventory snapshot
- **AND** the dated report links the updated index and its evidence artifacts

#### Scenario: An archive-pointer-only fit note is found
- **WHEN** a topic entry's extension-fit note cites only an archived change folder
- **THEN** the lane MUST emit an `ideation-readiness` finding naming the entry and the citation requirement

#### Scenario: The lane is skipped
- **WHEN** the readiness worker is unavailable or fails
- **THEN** the run MUST record the lane as skipped and the deterministic results MUST land unaffected
- **AND** a prior finding absent only because the lane did not run MUST NOT be treated as resolved

#### Scenario: Lane output fails its contract
- **WHEN** worker output does not satisfy the promoted evidence contract or index schema
- **THEN** the output MUST be rejected before persistence and the rejection reported in the run

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement fifteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, and proposal origin. Every check in
this pass MUST be deterministic — identical inputs produce identical findings,
with no model calls; semantic analysis and readiness scoring belong to the
agentic semantic sweep and the separate document-cataloger,
ideation-organizer, and ideation-readiness lanes their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** a family or reference check that cannot run (for example notebook drift without credentials or an unavailable external checkout) MUST be reported as skipped, never silently omitted

#### Scenario: Lifecycle conformance checks fire
- **WHEN** a governance document violates a `document-lifecycle` rule — a free-form or missing `Status:` value, an unbacked `standard` claim, a dangling `Ratified by:` reference, a `superseded` doc without a successor, a `brainstorm` doc outside `ideation/brainstorm/`, a `staged` doc that is outside `ideation/staging/` and is not a candidate register (`Kind: register`), or a content edit to a `record` doc after capture
- **THEN** the run MUST emit a finding naming the check family, the repo, the path, and the violated rule

#### Scenario: A register carries staged status
- **WHEN** a candidate register (`Kind: register`) carries `Status: staged` outside `ideation/staging/`
- **THEN** location conformance MUST NOT emit a finding — registers are a promoted organized-state home per the `document-lifecycle` capability

#### Scenario: Drift checks fire
- **WHEN** a submodule pin lags its remote main, a contract copy diverges from its canonical source, or the lifecycle notebook projection dry-run reports nonzero add/update/delete operations
- **THEN** the run MUST emit a drift finding identifying what diverged and from which source of truth

#### Scenario: Catalog conformance checks fire
- **WHEN** governed-document coverage, catalog identity, freshness, taxonomy, provenance, override standing, or record immutability violates the promoted catalog contract
- **THEN** the run MUST emit a `document-catalog` finding with the violated requirement and evidence

#### Scenario: Routing conformance checks fire
- **WHEN** a routed idea, claim, destination, proposal manifest, repository ID or gitlink, or aggregation placement violates the promoted routing contract
- **THEN** the run MUST emit an `ideation-routing` finding with the violated requirement and evidence

#### Scenario: Origin conformance checks fire
- **WHEN** a proposal packet, support manifest, or staging-header linkage violates the promoted origin contract
- **THEN** the run MUST emit a `proposal-origin` finding with the violated requirement and evidence
