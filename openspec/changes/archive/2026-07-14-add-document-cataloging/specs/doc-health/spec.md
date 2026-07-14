# doc-health Delta: Document Catalog

## ADDED Requirements

### Requirement: Document-catalog checks enforced by reference
The `document-catalog` deterministic check family SHALL enforce the promoted
`document-cataloging` requirements by reference. It SHALL validate exact
inventory coverage after baseline; unique canonical or policy-opaque locators;
source revision and content-hash freshness; artifact type; schema, taxonomy,
and controlled-value validity; effective taxonomy digest and ordered inputs;
capability and topic resolution; classifier and prompt provenance; confidence
range; per-facet `state_since` and transition history; authorized override and
host-handling standing; pending aging; protected-input/output evidence shape;
immutable run paths; and exclusion of generated catalog records from recursive
discovery.

The family SHALL distinguish deterministic catalog integrity from semantic
classification judgment. It MUST NOT decide whether a domain, capability,
topic, role, or sensitivity signal is semantically correct; approve or reject
a recommendation; alter a source document; or convert a catalog tag into
routing state. Before the declared baseline completes, it SHALL report coverage
progress without emitting one missing-entry regression per legacy document.

#### Scenario: Catalog coverage is incomplete after baseline
- **WHEN** a complete inventory document has no matching entry in the run snapshot after baseline enforcement is enabled
- **THEN** the run MUST emit a `document-catalog` coverage finding naming the repository and path

#### Scenario: Catalog entry does not match inventory
- **WHEN** an entry's path, revision, or content hash differs from the shared inventory snapshot
- **THEN** the run MUST emit a stale-catalog finding and downstream consumers MUST ignore the entry

#### Scenario: Catalog value is structurally invalid
- **WHEN** a facet uses an unknown controlled value, unresolved effective topic or capability, invalid confidence, or incomplete provenance
- **THEN** the run MUST emit a schema or taxonomy finding

#### Scenario: Semantic classification is debatable
- **WHEN** a structurally valid suggested tag might be semantically wrong
- **THEN** the deterministic family MUST NOT judge or auto-fix it
- **AND** disposition MUST remain with the authority defined by `document-cataloging`

#### Scenario: Baseline is still running
- **WHEN** the first sharded catalog baseline is incomplete and disclosed as such
- **THEN** the report MUST state coverage progress without opening a separate regression for every uncataloged legacy document

#### Scenario: Cataloger worker is unavailable
- **WHEN** the semantic cataloger is skipped or fails
- **THEN** deterministic catalog validation and the mechanical snapshot MUST still complete
- **AND** selected semantic entries MUST remain visibly pending

#### Scenario: Catalog contract evolves
- **WHEN** a later OpenSpec change modifies catalog corpus, schema, taxonomy, or authority rules
- **THEN** the family MUST follow the owning requirements by reference rather than a stale implementation copy

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement thirteen check families
over the whole factory family's governance corpus: status validity,
standard backing, ratified provenance, succession integrity, location
conformance, record immutability, staged/candidate aging,
register-lifecycle consistency, tag hygiene, submodule pin drift,
contract-copy drift, notebook projection drift, and document catalog. Every
check in this pass MUST be deterministic — identical inputs produce identical
findings, with no model calls; semantic analysis belongs to the agentic
semantic sweep and separate document-cataloger lane their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** a family that cannot run (for example notebook drift without credentials) MUST be reported as skipped, never silently omitted

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

### Requirement: Aging threshold defaults
The contract SHALL define default aging thresholds so reports are comparable
across runs: staged topics and `xspec:candidate` blocks untouched 30 days are
`warning` findings escalating to `error` at 90 days; an `xspec:supersedes`
marker without `change=` is `warning` at 14 days escalating to `error` at 45
days; `draft` documents have their age distribution reported always (`info`)
with a `warning` at 60 days without a lifecycle transition; and, after catalog
baseline, a document classification that remains `pending` for 30 days SHALL be
a `warning` and SHALL escalate to `error` at 90 days from its preserved
facet-level `state_since`.

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
