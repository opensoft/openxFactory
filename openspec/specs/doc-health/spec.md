# doc-health Specification

## Purpose

Define the deterministic health-check contract for the factory family's
governance corpus: the check families, finding severities, the dated report
and ranked plan, the headline canon-share metric, and the ownership split
between contract, implementation, and the nightly runner.
## Requirements
### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement thirteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, and document catalog. Every check in this pass MUST be deterministic —
identical inputs produce identical findings, with no model calls; semantic
analysis and readiness scoring belong to the agentic semantic sweep and the
separate document-cataloger and ideation-readiness lanes their owning
capabilities define. Check families SHALL implement promoted spec wording;
staged ideation fragments are inputs to contracts, never check definitions.

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

### Requirement: Tag hygiene enforced by reference
The tag-hygiene check family SHALL enforce the canonical `xspec:` marker
grammar exactly as the `document-lifecycle` capability defines it, by
reference; this capability and its artifacts MUST NOT restate the grammar.
The family covers marker well-formedness, target and change-id resolution,
candidate fence structure, the code-fence and inline-code example
exclusion, the ban on doc-level candidacy status values, and supersedes
`change=` aging.

#### Scenario: A marker violates the grammar
- **WHEN** a live `xspec:` marker fails any rule of the grammar as defined by `document-lifecycle`
- **THEN** the run MUST emit a tag-hygiene finding citing the grammar's owning capability, not a locally restated rule

#### Scenario: The grammar evolves
- **WHEN** an OpenSpec change modifies the marker grammar in `document-lifecycle`
- **THEN** the tag-hygiene family follows it with no delta to this capability required

### Requirement: Health report contract
Each doc-health run SHALL produce a dated Markdown report committed at
`health/reports/YYYY-MM-DD.md` in the xFactory aggregation repo, carrying
`Status: record` and `Kind: report`, containing the headline metric (canon
share by words: ratified + standard + promoted specs over total governance
words), per-lifecycle-stage counts, per-family finding sections, and a
ranked plan in which every finding is a ready-to-stage work item stating
severity, repo, path, and suggested action.

#### Scenario: A report is produced
- **WHEN** a run completes
- **THEN** the report MUST be committed at the dated path with `Status: record` + `Kind: report`
- **AND** every finding MUST appear in the ranked plan as an actionable item, so report output feeds the ideation pipeline's input

#### Scenario: A run uses non-default configuration
- **WHEN** a run executes with any non-default threshold or scope
- **THEN** the report MUST state the deviation, so cross-run comparisons stay honest

### Requirement: Finding severity and regression handling
Every finding SHALL carry one severity from `critical` (governance
integrity broken), `error` (contract violation), `warning` (drift or
first-stage aging), or `info` (inventory and metrics); one resolution class
from `auto-fixable` (mechanical defect: malformed marker, broken link,
missing header, formatting) or `contested` (resolution would change a
deliberately-set state, arbitrate between rules, or reverse a prior gate
decision); and a regression — any `critical` or `error` finding not present
in the previous report, matched by check family and path — MUST open a
single issue per run in the aggregation repo listing the new findings.

#### Scenario: A new error-level finding appears
- **WHEN** a run emits a `critical` or `error` finding absent from the previous report
- **THEN** one issue for the run MUST be opened in the aggregation repo listing all such new findings

#### Scenario: Findings persist unchanged
- **WHEN** a finding present in the previous report recurs
- **THEN** it MUST appear in the report and plan but MUST NOT open or duplicate an issue

#### Scenario: A contested finding is resolved
- **WHEN** a finding classified `contested` stops appearing between consecutive reports
- **THEN** its resolution MUST cite an OpenSpec change or a recorded human disposition against the finding id
- **AND** a contested finding that disappears via a state or status change with no such citation MUST be emitted as a new `error` finding ("uncited resolution") naming the original finding

#### Scenario: A session works a report's plan
- **WHEN** a session resolves ranked-plan items from a report
- **THEN** it MAY apply `auto-fixable` items directly
- **AND** it MUST NOT apply state-changing edits for `contested` items — those are escalated for a change proposal or human disposition

#### Scenario: The headline metric declines
- **WHEN** canon share by words drops between runs
- **THEN** the decline is trend data in the report, not a regression — no issue is opened for it alone

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

### Requirement: Ownership and hosting split
The doc-health contract, report schema, and implementation SHALL all be owned by openxFactory
(checker scripts, report generator, and the reusable workflow move home
with the contract they follow); the nightly runner SHALL be hosted by the xFactory
aggregation repo as the only repo pinning every submodule; and content
authority SHALL stay with each owning factory — health tooling reports
and stages, it never approves or merges another factory's content.

#### Scenario: The pipeline changes shape

- **WHEN** a check family, report schema element, severity rule, or threshold default changes
- **THEN** the change MUST be an OpenSpec delta to this capability in openxFactory, and the in-repo implementation follows in the same change or a named successor

#### Scenario: A finding concerns a domain factory's content

- **WHEN** the ranked plan proposes work on a DomainxFactory's documents
- **THEN** the item enters that work as a staged proposal; approval remains with the owning factory's authority, and the health pipeline MUST NOT auto-apply content changes

#### Scenario: A neutral artifact cites the implementation

- **WHEN** a neutral schema, validator, or doc references a checker implementation file
- **THEN** the reference resolves inside openxFactory itself — a neutral artifact citing a domain-repo implementation path is a conformance defect of this capability

### Requirement: Proposal supporting-document integrity checks
The deterministic doc-health pass SHALL validate proposal supporting-document
lifecycle integrity. It SHALL report staged material that already cites an
active or archived proposal, active supporting-document folders with missing or
invalid manifests, `Status: staged` documents under active proposal support,
archive manifests whose bundle or file hashes do not verify, and supporting
bundles stored under canonical `openspec/specs/`.

#### Scenario: Proposed material remains in staging
- **WHEN** a staged document names an active or archived OpenSpec change as its exit or proposal
- **THEN** doc-health MUST report that document as stale staged state

#### Scenario: An active proposal lacks its manifest
- **WHEN** an active change contains `supporting-docs/` without a valid `manifest.yaml`
- **THEN** doc-health MUST report the incomplete proposal support record

#### Scenario: An archived bundle fails verification
- **WHEN** an archived change's readable supporting-document manifest does not match its bundle hash or bundled file hashes
- **THEN** doc-health MUST report an archive-integrity error

#### Scenario: A historical bundle is stored as canonical specification
- **WHEN** a compressed supporting-document bundle exists below `openspec/specs/`
- **THEN** doc-health MUST report a location-conformance error

### Requirement: Agentic semantic sweep
The doc-health capability SHALL include an agentic semantic sweep: a second
pass in which a model-driven worker reads the governance corpus and emits
findings in two semantic check families — `semantic-normative-prose`
(normative language such as "must", "owns", or "never" asserted in a
document that is not a promoted spec and carries no `xspec:` marker binding
it to one) and `semantic-contradiction` (prose whose meaning conflicts with
a promoted spec requirement). These families complement and never replace
the deterministic families.

#### Scenario: Untagged normative prose is found
- **WHEN** the sweep reads a non-spec document asserting an obligation with no `xspec:` marker binding it to a promoted requirement
- **THEN** the sweep MUST emit a `semantic-normative-prose` finding naming the repo, the path, and the passage

#### Scenario: A contradiction candidate is found
- **WHEN** the sweep judges a passage to conflict with a promoted spec requirement
- **THEN** the sweep MUST emit a `semantic-contradiction` finding naming the repo, the path, the passage, and the suspected conflicting requirement

### Requirement: Sweep execution split
The semantic sweep SHALL comprise two parts with distinct execution
authorities. Orchestration — inventory consumption, scope resolution,
worker invocation, findings merge, and report commit — is deterministic
runner code executing under the factory identity (a short-lived
installation token minted from the openxFactory GitHub App), exactly as the
deterministic pass runs today. Analysis — the model-driven judgment step —
executes only as the bounded worker defined by this capability and never
holds the factory identity.

#### Scenario: The nightly sweep executes
- **WHEN** the sweep runs in the nightly workflow
- **THEN** orchestration performs checkout, scope resolution, and the report commit under the factory identity
- **AND** the analysis step is invoked by orchestration and returns only its findings artifact

#### Scenario: Analysis authority is bounded
- **WHEN** the analysis step executes
- **THEN** it MUST NOT perform repository writes, report commits, or any orchestration action

### Requirement: Bounded analysis worker profile
The analysis worker SHALL execute under a bounded, read-only Omnigent
worker profile: no repository credentials in its environment (orchestration
provides a local read-only checkout), no credential grants beyond model API
access, no write path except its findings artifact, and a job envelope
conforming to the neutral job-envelope contract whose reference the report
records alongside the pinned model id and prompt-contract version. Analysis
output SHALL carry L1 authority.

The analysis workflow MAY receive a least-privilege, Actions-read GitHub job
token solely to transfer the self-contained input and findings artifacts, but
the model subprocess MUST NOT receive that token or any repository credential.
The model SHALL consume the corpus as untrusted stdin data with filesystem
tools and session persistence disabled, and its output SHALL satisfy the
versioned structured-output schema before findings-contract validation.
Before artifact download, the child workflow SHALL verify that its source run,
correlation, repository, workflow path, event, and source revision identify the
authorized nightly parent run at the same immutable revision.

Artifact-worker readiness SHALL be isolated from the general Hermes worker
registry. Its read and heartbeat routes SHALL require distinct bearer tokens;
the authenticated first heartbeat MAY create the readiness identity, and every
later heartbeat SHALL be a complete schema-versioned replacement with a
strictly newer observation time. Legacy worker registration or heartbeat
routes MUST NOT mutate the state used for artifact dispatch.

#### Scenario: An analysis run executes
- **WHEN** the analysis worker runs
- **THEN** its environment holds no repository credentials and no factory identity token
- **AND** the report records the job envelope reference, the model id, and the prompt-contract version used

#### Scenario: The analysis worker fails
- **WHEN** readiness is absent, the runner is offline or queued, the child exceeds its bounded wait, the analysis errors, or the model is unavailable
- **THEN** the run MUST record the sweep as skipped in the report and the deterministic results MUST land unaffected

#### Scenario: Self-hosted dispatch is enabled
- **WHEN** orchestration considers dispatching the analysis child
- **THEN** hosted readiness MUST observe an eligible online and idle runner plus a matching external heartbeat no older than five minutes
- **AND** exactly one runner in the restricted group MUST own the heartbeat's `host-*` dispatch label, and it MUST be the heartbeat-named runner
- **AND** the heartbeat MUST attest available capacity, eligible host class, worker and required profile versions, authorization boundaries, service/model health, and repository-credential absence
- **AND** hosted finalization MUST NOT depend on the self-hosted child job or fail because a readiness/result API is unavailable or malformed

#### Scenario: A readiness identity publishes its first or a later heartbeat
- **WHEN** the authenticated readiness heartbeat endpoint receives the first complete supported-schema snapshot for a worker id
- **THEN** it MUST create the isolated readiness identity without requiring legacy worker registration
- **WHEN** a later heartbeat is partial, uses an unsupported schema, or is not newer than the stored observation
- **THEN** Hermes MUST reject it without changing the prior readiness snapshot

#### Scenario: Analysis child is dispatched directly or with substituted input
- **WHEN** the source run, correlation, repository, workflow path, event, or source revision does not match the authorized nightly parent
- **THEN** the child MUST fail before downloading the corpus artifact

### Requirement: Semantic findings are proposals
Every semantic finding SHALL be a proposal, not a verdict: it carries the
document, the passage, the suspected conflicting requirement (for
contradiction findings), and a confidence note; it is always resolution
class `contested`, its severity is at most `warning`, and disposition
belongs to a human or a gate. Semantic findings MUST NOT block merges and
MUST NOT open regression issues in v1.

#### Scenario: A semantic finding enters the report
- **WHEN** a sweep run completes with findings
- **THEN** each finding MUST appear in the dated report's ranked plan as a candidate work item with its confidence note
- **AND** no finding of the semantic families carries severity `critical` or `error`

#### Scenario: A semantic finding is disposed
- **WHEN** a semantic finding stops appearing between consecutive reports
- **THEN** its resolution MUST cite an OpenSpec change or a recorded disposition, exactly as the contested-finding rule already requires

#### Scenario: The semantic sweep is unavailable
- **WHEN** a prior semantic finding is absent only because the current semantic sweep was skipped or unavailable
- **THEN** the prior finding MUST NOT be treated as resolved and MUST NOT generate an uncited-resolution error

### Requirement: Semantic finding disposition authority
Disposition authority for semantic findings SHALL follow content ownership:
a finding on a domain factory's own documents is disposed by that factory's
authority (its Domain Hermes); a finding implicating a neutral openxFactory
artifact, or a contradiction spanning repositories, is disposed at the
neutral repository's ratify gate. Client and Customer Hermes layers have no
disposition standing in v1 — their influence on the sweep is limited to
scope declarations.

#### Scenario: A finding concerns a domain factory's document
- **WHEN** a semantic finding names only documents owned by one domain factory
- **THEN** disposition belongs to that factory's authority and the ranked-plan item names it

#### Scenario: A finding implicates a neutral artifact
- **WHEN** a semantic finding names an openxFactory artifact or spans repositories
- **THEN** disposition belongs to the neutral repository's ratify gate and the ranked-plan item names it

#### Scenario: A layer without standing disposes a finding
- **WHEN** a disposition is recorded by an authority other than the finding's named disposer
- **THEN** the resolution is uncited under the contested-finding rule and the next run MUST emit the "uncited resolution" error finding

### Requirement: Sweep sequencing and snapshot consistency
The semantic sweep SHALL run after the deterministic pass and consume the
doc inventory that pass emits (paths, statuses, content hashes), so both
passes report against the same corpus snapshot; the changed-docs set for
incremental sweeps is derived from inventory hash diffs against the
previous report.

#### Scenario: A nightly run executes both passes
- **WHEN** the nightly run completes
- **THEN** the sweep's corpus is exactly the deterministic pass's inventory for that run
- **AND** the final report MUST verify that the prepared inventory matches the immutable checkout before merging worker findings

#### Scenario: The deterministic pass fails
- **WHEN** the deterministic pass fails before emitting an inventory
- **THEN** the sweep MUST NOT run against a stale inventory and MUST be reported as skipped

### Requirement: Hermes-layer sweep scope resolution
Sweep scope SHALL be Hermes-owned policy resolved deterministically by
orchestration: each Hermes layer overlay (customer, client, domain) MAY
declare a `doc_health.sweep_scope` value from the ordered set
`incremental` < `full-weekly` < `full-nightly`; the effective scope is the
deepest value declared across layers; when no layer declares one, the
default is `incremental` (nightly changed-docs sweep plus a weekly full
sweep). Every report MUST state the effective scope and, when a declaration
raised it above the default, the declaring layer.

#### Scenario: No layer declares a scope
- **WHEN** no Hermes layer overlay declares `doc_health.sweep_scope`
- **THEN** the sweep runs at `incremental` and the report states the default applied

#### Scenario: A layer declares a deeper scope
- **WHEN** any layer declares a scope deeper than the others or the default
- **THEN** the effective scope is that deepest declaration and the report names the declaring layer

#### Scenario: A layer declares a shallower scope
- **WHEN** a layer declares a scope shallower than another layer's declaration
- **THEN** the effective scope remains the deepest declaration — no layer can lower another's review level

### Requirement: Report-only to blocking promotion gate
The semantic sweep SHALL remain report-only until a future OpenSpec delta
promotes any semantic family to blocking, and such promotion MUST cite
precision evidence: at least seventy percent of dispositioned semantic
findings confirmed valid across at least twenty dispositions within a
rolling thirty-day window, measured from the recorded dispositions.

#### Scenario: Promotion is proposed without evidence
- **WHEN** a delta proposes making a semantic family blocking without the cited precision evidence
- **THEN** the proposal fails this capability's gate and the sweep stays report-only

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

### Requirement: Ideation dashboard snapshot lane
The nightly doc-health run SHALL include a deterministic ideation-dashboard
snapshot lane: after the deterministic pass, the generator defined by the
`ideation-dashboard` capability regenerates the snapshot and commits it
beside the dated reports. The lane is an output artifact of the run — like
the report itself — and adds no deterministic check family; strict snapshot
and workbench-manifest validation runs in the existing per-repo validator
preflight. A skipped or failed snapshot lane MUST be reported as skipped
and MUST NOT affect deterministic results.

#### Scenario: The nightly run completes
- **WHEN** the deterministic pass finishes
- **THEN** the snapshot lane regenerates and commits the snapshot beside the dated report
- **AND** the report links the committed snapshot

#### Scenario: The snapshot lane fails
- **WHEN** snapshot generation errors or is unavailable
- **THEN** the run records the lane as skipped and deterministic findings land unaffected

#### Scenario: A snapshot violates its schema
- **WHEN** a generated snapshot fails strict validation in the preflight
- **THEN** the run MUST report the validator failure rather than committing an invalid snapshot

### Requirement: Possibles derivation lane
The doc-health capability SHALL include a possibles-derivation lane: a bounded,
non-mutating worker pass — following the same execution split and bounded-worker
pattern as the agentic semantic sweep, the document-cataloger lane, and the
ideation-readiness lane — that derives candidate possibles from the promoted
`ideation-cross-reference` index and proposes `possibles_register` entries.

Lane output SHALL be recommendations with `pending_review` disposition,
resolution class `contested`, and severity at most `warning`; derived-but-
undisposed possibles SHALL appear in the report as their own section, excluded
from the Ranked Plan; the lane MUST NOT block merges, MUST NOT open regression
issues in v1, and SHALL add no deterministic check family — the strict register
validator that enforces derived-entry shape and one-way disposition runs in the
existing per-repo validator preflight (delegated to
`validate-ideation-dashboard-contracts.py`).

#### Scenario: The nightly lane executes
- **WHEN** the possibles-derivation lane runs in the nightly workflow
- **THEN** it runs after the deterministic pass against the same inventory/index snapshot
- **AND** the dated report links the updated index and its immutable derivation evidence

#### Scenario: Derived possibles are reported
- **WHEN** a run has undisposed derived possibles
- **THEN** the report MUST list them in their own section and MUST NOT rank them in the Ranked Plan

#### Scenario: The lane is skipped
- **WHEN** the derivation worker is unavailable or fails
- **THEN** the run MUST record the lane as skipped and the deterministic results MUST land unaffected
- **AND** prior derived possibles absent only because the lane did not run MUST NOT be treated as disposed

#### Scenario: Lane output fails its contract
- **WHEN** worker output does not satisfy the register evidence contract or the additive kernel shape
- **THEN** the output MUST be rejected before persistence and the rejection reported in the run

### Requirement: Ideation readiness lane
The doc-health capability SHALL include an ideation readiness lane: a
bounded, non-mutating worker pass — following the same execution split and
bounded-worker pattern as the agentic semantic sweep and the
document-cataloger lane — that maintains the
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

