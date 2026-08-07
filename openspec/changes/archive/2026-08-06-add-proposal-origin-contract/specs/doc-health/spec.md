# doc-health Delta: Proposal Origin Contract

## ADDED Requirements

### Requirement: Proposal-origin checks enforced by reference
The `proposal-origin` deterministic check family SHALL enforce the promoted
origin requirements of `document-lifecycle` and `release-realization` by
reference. It SHALL report an active or archived proposal with no origin
declaration; an unknown or malformed origin kind or id; a staged origin
whose id, path, or staging-header linkage does not resolve against its
recorded provenance; a mismatch among staging header, proposal packet, and
support manifest; an ad-hoc origin lacking reason or approval provenance;
and mutation of an origin declaration after ratification. Backfilled
origins SHALL be validated against recorded migration provenance; the
family MUST NOT fabricate or infer staging history for changes that predate
the contract.

#### Scenario: A proposal lacks an origin declaration
- **WHEN** an active or archived proposal carries no origin declaration and no recorded migration exemption
- **THEN** the run MUST emit a `proposal-origin` finding naming the change and the violated requirement

#### Scenario: Origin declarations disagree
- **WHEN** the staging header, the `.openspec.yaml` declaration, and the support manifest do not agree on origin kind, id, or path
- **THEN** the run MUST emit a `proposal-origin` finding identifying each disagreeing record

#### Scenario: An origin was mutated after ratification
- **WHEN** an origin declaration differs from the declaration recorded at ratification
- **THEN** the run MUST emit an `error` finding with resolution class `contested` — resolving it reverses a gate decision

#### Scenario: A pre-contract change carries a backfilled origin
- **WHEN** an archived change's origin was backfilled by the recorded migration
- **THEN** the family MUST validate it against the migration provenance record and MUST NOT report it merely for having been declared late

#### Scenario: The origin contract evolves
- **WHEN** a later OpenSpec change modifies the promoted origin requirements
- **THEN** the family MUST follow the owning requirements by reference rather than a stale implementation copy

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement fifteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, and proposal origin. Every check in this pass MUST be
deterministic — identical inputs produce identical findings, with no model
calls; semantic analysis belongs to the agentic semantic sweep and the separate
document-cataloger and ideation-organizer lanes their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
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
