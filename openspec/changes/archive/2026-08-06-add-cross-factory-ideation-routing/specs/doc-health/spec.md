# doc-health Delta: Ideation Routing

## ADDED Requirements

### Requirement: Ideation-routing checks enforced by reference
The `ideation-routing` deterministic check family SHALL enforce the promoted
`ideation-routing` and related `document-lifecycle` requirements by reference.
It SHALL validate routing schemas and controlled vocabulary; central Idea-ID
allocation; unique Idea-ID and Claim-ID definitions; paired-document identity;
one canonical routing record; legal transitions; destination-owner acceptance;
structured repository, path, and revision references; source and destination
resolution; staged Claim-ID pointers; proposal provenance; routed destinations
or explicit unresolved blockers; copied full routing records; routing aging;
and the absence of a general ideation backlog in the aggregation repository.

Duplicate detection SHALL distinguish canonical definitions from lightweight
references and SHALL ignore examples in Markdown code fences and inline code.
The family MAY auto-fix only safe mechanical defects permitted by existing
finding policy, such as path-separator normalization. It MUST NOT choose an
owner, split a claim, accept a destination, move a document, dispose an
organizer recommendation, or promote policy.

Repository resolution SHALL use reserved root ID `xFactory` plus exact
aggregation-relative `.gitmodules` paths and their gitlinks. The family SHALL
scan the governed openxFactory and DomainxFactory corpus, inspect the xFactory
root only for forbidden ideation placement and locator integrity, and resolve
referenced install/runtime paths without treating those repositories as
governance corpora. Strict organize/proposal mode SHALL materialize every
referenced pinned repository; a nightly unavailable external-path check SHALL
be reported as skipped rather than passed.

#### Scenario: Structural routing violation is found
- **WHEN** a routing record violates its promoted schema, vocabulary, transition, acceptance, identity, or reference contract
- **THEN** the run MUST emit an `ideation-routing` finding naming the repository, path, and owning requirement

#### Scenario: Ordinary document lacks routing metadata
- **WHEN** a document has not entered a routed lifecycle
- **THEN** the family MUST NOT emit a finding merely because it has no Idea ID or sidecar

#### Scenario: Unresolved claim has a blocker
- **WHEN** a claim remains `unresolved` and names an explicit blocker or blocking question
- **THEN** destination validation MUST accept that state while the record remains incomplete

#### Scenario: Duplicate-looking references occur
- **WHEN** one canonical Claim-ID definition has valid lightweight references or fenced examples elsewhere
- **THEN** the family MUST NOT report those references or examples as duplicate definitions

#### Scenario: Full routing record is copied
- **WHEN** a destination document contains the routing-record schema rather than lightweight provenance pointers
- **THEN** the family MUST emit a drift finding

#### Scenario: Safe path defect is found
- **WHEN** a structured reference differs only by a safely normalizable path separator
- **THEN** the finding MAY be classified `auto-fixable`

#### Scenario: Ownership decision is incomplete
- **WHEN** resolving a finding would require choosing an owner, accepting a destination, or splitting a claim
- **THEN** the finding MUST be `contested` and MUST NOT be auto-fixed

#### Scenario: External path is unavailable during nightly validation
- **WHEN** a pinned external repository needed only for reference resolution is not materialized
- **THEN** the path check MUST be reported as skipped
- **AND** strict organize or proposal validation MUST still require the path to resolve

#### Scenario: Routing contract evolves
- **WHEN** a later OpenSpec change modifies the promoted routing contract
- **THEN** the checker MUST follow the owning requirements by reference rather than a stale staged definition

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement fourteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, and ideation routing. Every check in this pass MUST be
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

### Requirement: Aging threshold defaults
The contract SHALL define default aging thresholds so reports are comparable
across runs: staged topics and `xspec:candidate` blocks untouched 30 days are
`warning` findings escalating to `error` at 90 days; an `xspec:supersedes`
marker without `change=` is `warning` at 14 days escalating to `error` at 45
days; `draft` documents have their age distribution reported always (`info`)
with a `warning` at 60 days without a lifecycle transition; after catalog
baseline, a document classification that remains `pending` for 30 days SHALL be
a `warning` and SHALL escalate to `error` at 90 days from its preserved
facet-level `state_since`; and routing records in `intake`, `triaging`, or
incomplete `split` state whose latest transition is 30 days old are `warning`
findings escalating to `error` at 90 days. `routed`, `rejected`, and explicitly
`deferred` routing records SHALL NOT age as unresolved work.

#### Scenario: An item crosses an aging threshold
- **WHEN** an item's untouched age crosses a threshold
- **THEN** the run MUST emit the finding at the threshold's severity
- **AND** crossing an escalation boundary produces a new `error` finding subject to the regression rule

#### Scenario: A draft lives long legitimately
- **WHEN** a `draft` document ages without transition
- **THEN** it MUST appear in age reporting and, past 60 days, as a `warning` ranked-plan item — never as `critical` or `error` on age alone

#### Scenario: Catalog classification remains pending
- **WHEN** a post-baseline catalog facet remains pending from the same `state_since` for 30 or 90 days
- **THEN** the run MUST emit a warning at 30 days and an error at 90 days

#### Scenario: Catalog pending threshold is overridden
- **WHEN** a run uses non-default catalog-pending thresholds
- **THEN** the report MUST disclose the configured thresholds

#### Scenario: Active routing work ages
- **WHEN** an `intake`, `triaging`, or incomplete `split` record's latest transition reaches 30 or 90 days
- **THEN** the run MUST emit a warning at 30 days and an error at 90 days

#### Scenario: Deferred routing is intentional
- **WHEN** a routing record is explicitly `deferred` with its reason recorded
- **THEN** it MUST NOT be reported as abandoned unresolved intake

#### Scenario: Routing threshold is overridden
- **WHEN** a run uses non-default routing-aging thresholds
- **THEN** the report MUST disclose the configured thresholds
