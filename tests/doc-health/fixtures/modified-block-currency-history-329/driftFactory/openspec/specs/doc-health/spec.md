# doc-health Specification

## Purpose
Canon as it stood on 2026-08-25, before add-release-inventory-drift-check
archived, carrying ONLY the requirement under test. Recovered verbatim at
d5f447e8 — see ../README.md.

## Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement seventeen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, and client
identity roster composition. Every check in this pass MUST be
deterministic — identical inputs produce identical findings, with no model
calls; semantic analysis belongs to the agentic semantic sweep and the separate
document-cataloger and ideation-organizer lanes their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions. The client
identity roster composition family SHALL cover only the CROSS-DOMAIN
concerns — assembling per-client fragments published by each domain and
reporting shared identity material or undeclared cross-domain reach —
because intra-repo roster conformance is a blocking domain gate rather than
an advisory report. Four of the seventeen — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
thirteen families and every corpus census, word count, canon-share figure,
shared-inventory entry, and catalog record SHALL be computed from the
governed corpus alone and MUST NOT move because the lifecycle scan set
exists.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** client identity roster composition MUST assemble the per-client roster fragments published by each pinned domain repository as its owning requirement in `client-identity-roster` defines
- **AND** status validity, standard backing, ratified provenance, and succession integrity MUST additionally read the declared lifecycle scan set, reporting a finding against the document's own path exactly as they do for a governed-corpus document
- **AND** a family or reference check that cannot run (for example notebook drift without credentials or an unavailable external checkout) MUST be reported as skipped, never silently omitted

#### Scenario: Lifecycle conformance checks fire
- **WHEN** a governance document violates a `document-lifecycle` rule — a free-form or missing `Status:` value, an unbacked `standard` claim, a `ratified` document whose lifecycle header carries no ratification citation in either sanctioned spelling, a dangling `Ratified by:` reference, a record-citing `Ratified:` line naming none of an approver, a date, or a resolvable record path, a `ratified` document whose lifecycle header carries more than one ratification citation (one of each spelling, or the same spelling twice), a `superseded` doc without a successor, a `brainstorm` doc outside `ideation/brainstorm/`, a `staged` doc that is outside `ideation/staging/` and is not a candidate register (`Kind: register`), or a content edit to a `record` doc after capture
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

#### Scenario: Roster composition is checked across domains
- **WHEN** two or more pinned domain repositories publish client identity roster fragments for the same client
- **THEN** the roster composition family assembles them and reports shared identity material or undeclared cross-domain reach
- **AND** intra-repo entry conformance is NOT reported here, because it fails the owning domain's gate instead

