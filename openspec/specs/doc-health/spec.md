# doc-health Specification

## Purpose

Define the deterministic health-check contract for the factory family's
governance corpus: the check families, finding severities, the dated report
and ranked plan, the headline canon-share metric, and the ownership split
between contract, implementation, and the nightly runner.
## Requirements
### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement nineteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, promotion fidelity, and release-inventory drift.
Every check in this pass
MUST be
deterministic — identical inputs produce identical findings, with no model
calls; semantic analysis belongs to the agentic semantic sweep and the separate
document-cataloger and ideation-organizer lanes their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions. The client
identity roster composition family SHALL cover only the CROSS-DOMAIN
concerns — assembling per-client fragments published by each domain and
reporting shared identity material or undeclared cross-domain reach —
because intra-repo roster conformance is a blocking domain gate rather than
an advisory report. Four of the nineteen — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
fifteen families and every corpus census, word count, canon-share figure,
shared-inventory entry, and catalog record SHALL be computed from the
governed corpus alone and MUST NOT move because the lifecycle scan set
exists. The promotion fidelity family reads archived spec DELTAS and promoted
SPECS — bodies rather than headers — and therefore takes neither the governed
corpus nor the lifecycle scan set as its document list; it moves no census,
word count, canon-share figure, inventory entry, or catalog record either. The
release-inventory drift family reads CONTRACT ARTIFACT BYTES — a release digest
inventory and the blobs it names — and likewise takes neither document list,
and it moves no census, word count, canon-share figure, inventory entry, or
catalog record.

**CORRECTED 2026-08-25 ON BRETT'S RULING — this block is now
SCENARIO-COMPLETE.** As first written it restated only ONE of this
requirement's scenarios. OpenSpec's `MODIFIED` REPLACES A REQUIREMENT
WHOLESALE rather than merging into it, so promoting that block would have
dropped the seven scenarios it did not restate — `Lifecycle conformance checks
fire`, `A register carries staged status`, `Drift checks fire`, `Catalog
conformance checks fire`, `Routing conformance checks fire`, `Origin
conformance checks fire`, and `Roster composition is checked across domains` —
silently, because the file-level scenario count would have stayed at 98: the
seven lost exactly offset the seven this change's ADDED requirement brings.
Caught by the byte-for-byte promotion verification at archive time, before
anything was committed. The seven are restored below VERBATIM from the promoted
spec; only the first scenario differs from canon, and it differs by TWO `AND`
bullets rather than one — only the second is this change's. The first names
`promotion fidelity`, and it is INHERITED: this delta was written on top of
`add-promotion-fidelity-check`'s text, on the assumption that the sibling would
land first. That assumption is why canon now says "nineteen check families"
while `promotion fidelity`'s own owning requirement is still inside that active
change, so the bullet's "as its owning requirement below defines" is a FORWARD
REFERENCE until the sibling archives, at which point it resolves on its own.
Recorded in issue #329 rather than papered over; it is an ordering dependency,
not a defect in either change.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** client identity roster composition MUST assemble the per-client roster fragments published by each pinned domain repository as its owning requirement in `client-identity-roster` defines
- **AND** promotion fidelity MUST compare each repository's archived spec deltas against its promoted specs as its owning requirement below defines
- **AND** release-inventory drift MUST compare each repository's declared bundle inventory against the blobs it names as its owning requirement below defines
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

### Requirement: Neutrality drift is scouted nightly
The doc-health pipeline SHALL include a neutrality-drift lane that reviews domain-factory content against the domain-neutral boundary on the nightly cadence: deterministic pre-filter signals (near-duplication of a neutral artifact, absence of domain vocabulary in a schema or script, cross-repo consumers, tooling absent from the domain's declared inventory) select candidates, and a model-driven scout under a versioned prompt contract judges the survivors and content changed since the lane's last run, returning structured candidates with neutrality evidence, counter-evidence, and domain-local exclusions.

#### Scenario: A neutral-shaped artifact appears in a domain repo

- **WHEN** a domain factory gains a schema, script, or process doc that another domain would need essentially unchanged
- **THEN** a nightly run within the lane's incremental window MUST surface it as a neutrality candidate with evidence and counter-evidence
- **AND** the scout's judgment MUST cite the file's own content, never only its location

#### Scenario: Scope is the domain factories

- **WHEN** the lane selects subjects
- **THEN** it reviews the pinned `xFactories/*` domain repos and MUST NOT review openxFactory, openAvatar, or the install realizations in v1

### Requirement: Candidates become staged proposals under human approval
The lane's findings SHALL be delivered as drafted DTN-register seed candidates (register row plus detail section in the register's own format) and ranked-plan items through the existing rolling health PR; a candidate advances only by Brett's approval of the seed, movement follows the domain-to-neutral promotion process, and the lane SHALL NOT edit any domain repo, open any move PR, or modify any contract.

#### Scenario: A candidate is proposed and approved

- **WHEN** the lane files a neutrality candidate
- **THEN** the rolling health PR carries the drafted register seed and the plan item
- **AND** only the human approval of that seed admits it to the register's lifecycle

#### Scenario: A rejected candidate stays rejected

- **WHEN** Brett dispositions a candidate as not-neutral or not-now
- **THEN** the disposition is recorded in the health dispositions register keyed by repo, path, and content digest
- **AND** the lane MUST NOT re-file the candidate while that content is unchanged

#### Scenario: Authority never transfers

- **WHEN** the lane finds even an unambiguous misplacement
- **THEN** it reports and stages only — content authority stays with the owning factory and every move lands through its own ratified change

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

### Requirement: The deterministic pass reads a document's lifecycle header by real lines
The deterministic pass SHALL locate a governed document's lifecycle header by counting the document's REAL lines — the three line endings CR, LF and CRLF — and MUST NOT count any other character as a line separator. The bounded header window is therefore a number of lines of the document rather than a number of fragments a wider splitting rule produced from it.

This SHALL hold for every reader of that header, so that the status a document carries and the status the pass reports are the same fact. A reader that splits more aggressively than the writer can fail to find a header the writer just wrote correctly, and then reports a document as lacking a status it plainly has — a FALSE finding, which costs more trust than a crash because it accuses a correct document and leaves the operator no recourse but to disbelieve the checker.

The line rule SHALL be shared with the writers of the same header rather than reimplemented per reader. Where the corpus cannot share an implementation across language boundaries, the divergence SHALL be held by an explicit agreement test rather than by convention.

#### Scenario: A header carrying an exotic separator is read
- **WHEN** the deterministic pass reads a governed document whose header region contains characters a wider splitting rule would treat as line breaks
- **THEN** the document's lifecycle status MUST be found if it is present within the header window counted in real lines
- **AND** the pass MUST NOT report the document as lacking a status it carries

#### Scenario: The header window is counted
- **WHEN** the deterministic pass applies its bounded header window to a document
- **THEN** the bound MUST count real lines of the document

#### Scenario: The reader and the writer are compared
- **WHEN** a lifecycle header is written by a governed action and then read by the deterministic pass
- **THEN** both MUST agree on where the document's lines begin and end

#### Scenario: The corpus is unchanged by the correction
- **WHEN** the deterministic pass runs over the governance corpus after this correction
- **THEN** its findings MUST be identical to the run before it
- **AND** any finding that does move MUST be explained rather than accepted, because a moved finding means a corpus document carries a separator the prior measurement did not see

### Requirement: Governed corpus membership and the lifecycle scan set
The doc-health capability SHALL declare two document sets and SHALL keep them distinct.

The **governed corpus** is the set of Markdown documents under the governed
roots `contracts/`, `docs/`, `examples/`, `ideation/` and `templates/` of each
repository in scope, excluding `installs/`, `tests/`, `node_modules/`,
`__pycache__/` and any nested git working copy. It is the sole input to the
per-stage census, the governance and canon word totals, the canon-share
headline, the shared inventory, and the document catalog. `openspec/` is NOT
a governed root: promoted specs join the inventory as promoted specs and are
counted toward canon, and no other document under `openspec/` enters the
governed corpus.

The **lifecycle scan set** is a separately declared set of paths carrying
lifecycle headers outside the governed corpus. It SHALL be declared as an
explicit path pattern set rather than as a directory, and it SHALL comprise
each change packet's `proposal.md` and EVERY `review/` record under
`openspec/changes/`, whether or not that record's subject is a ratification.
A document in the lifecycle scan set is subject to the `document-lifecycle`
status and ratification-citation rules and to no other family's rules; the
citation half of that pair binds only a document whose status is `ratified`,
so a `review/` record carrying another taxonomy value is checked for its
status and for nothing else.

The scan set SHALL NOT reach a document that is byte-exact evidence rather
than live prose. A path carrying a `supporting-docs`, `source-snapshots` or
`evidence` segment SHALL be excluded from the set even where it otherwise
matches a declared pattern, because a frozen record reported for the state it
preserves is a false finding.

Widening either set is a governed change: a promoted OpenSpec change SHALL
record the new membership together with the measured effect on finding
counts by family, on the canon-share headline, and on the existing test
suite, because a corpus measurement whose scope changes silently reports the
scope rather than the corpus.

#### Scenario: A proposal carries an uncited ratified header
- **WHEN** a document in the lifecycle scan set carries `Status: ratified` with no ratification citation in either sanctioned spelling
- **THEN** the run MUST emit a `ratified-provenance` finding against that document's path
- **AND** the finding MUST carry the same severity it would carry for a governed-corpus document, because the defect is the same defect

#### Scenario: A proposal's lifecycle header sits outside the header window
- **WHEN** a document in the lifecycle scan set carries its `Status:` header past the header window, so the header reads as absent
- **THEN** the run MUST emit a `status-validity` finding of missing status header
- **AND** the run MUST NOT rely on `ratified-provenance` to catch it, because a document whose status does not parse is not a `ratified` document to that family

#### Scenario: The lifecycle scan set does not move the corpus metrics
- **WHEN** a doc-health run executes with a non-empty lifecycle scan set
- **THEN** the per-stage counts, the governance and canon word totals, the canon-share headline, the shared inventory, and the catalog snapshot MUST be identical to a run with an empty lifecycle scan set over the same corpus
- **AND** only the four families that read the set MAY report additional findings

#### Scenario: A family outside the declared four is added later
- **WHEN** a check family not named as a reader of the lifecycle scan set executes
- **THEN** it MUST read the governed corpus alone
- **AND** an automated check MUST hold that boundary, so that a family added later does not acquire or lose the wider scope by accident

#### Scenario: A document is byte-exact evidence rather than live prose
- **WHEN** a change packet holds a byte-exact snapshot of a staged fragment, illustrative malformed markers, or other evidence whose content is fixed by what it records
- **THEN** it MUST NOT be in the lifecycle scan set, because reporting a frozen record for the state it preserves is a false finding

### Requirement: Release-inventory drift
The release-inventory drift family SHALL compare, for every repository in
scope that declares a contract bundle, each member of that bundle's release
digest inventory against the blob the repository carries at the checked commit,
and report where they differ.

THE COMPARISON SHALL COVER THE RECORDED `git_mode` AS WELL AS THE DIGEST. An
inventory entry records both, and a mode-only change — an executable bit set or
cleared on a validator — leaves the blob bytes and therefore the digest
identical. A family that compared digests alone would report a validator whose
executability had changed as MATCHING, which is the silent-drift class this
whole capability exists to close. The canonical verifier already distinguishes
them (`HGR-RELEASE-DIGEST-MISMATCH` and `HGR-RELEASE-MODE-MISMATCH`); this
family SHALL NOT be weaker than the verifier whose gap it exists to cover.

The obligation being checked belongs to `release-surface-integrity` ("The
declared bundle describes the release surface"), the capability this change
adds; this requirement defines only how doc-health checks it, in the same
by-reference relationship tag hygiene already has with `document-lifecycle`'s
marker grammar.

THE FAMILY SHALL SPLIT ITS FINDINGS IN TWO, because the two states are
different facts and reporting them alike would make the common one hide the
serious one. NON-EDITORIAL drift — any member other than the changelog, the
manifest and the README — SHALL be reported at `error`, because a normative
contract's bytes moved while the repository went on declaring a bundle that
describes different bytes. EDITORIAL drift — those three members and nothing
else — SHALL be reported at `info`, because it is the expected bounded state
between cuts and the next cut re-baselines it. Both verdicts are Brett's ruling
of 2026-08-24: `info` rather than `warning`, so a condition nobody should act on
does not hold a permanent yellow row in every report.

DIGESTS SHALL BE COMPUTED OVER RAW BYTES, never over decoded text. The
inventory's own identity rule is the SHA-256 of raw Git blob bytes and names
text canonicalization as an invalid digest source, so a family that read the
blob as text would compute a different number and report drift that does not
exist on any file whose bytes are not pure ASCII.

THE FAMILY SHALL NOT BE CLASSIFIED `contested`, and the reason is structural
rather than a taste call. Both of its findings are RESOLVED BY A RELEASE CUT,
which is exactly the act that makes them vanish between reports — and a
`contested` finding that vanishes without citing a change or a disposition
against its finding id is re-emitted as an `error` under the uncited-resolution
rule. Classifying this family `contested` would therefore turn every correctly
performed release cut into a new error, which is an enforcement channel
arriving through the back door on precisely the runs that prove the family
working. Severity and resolution class are one later decision, taken together
by ruling.

The family SHALL be reported as skipped, never silently omitted, where a
repository declares no bundle at all, or where version control cannot answer —
an unavailable git dependency, or a commit that does not resolve. THE SKIP IS
RESERVED FOR "THE QUESTION COULD NOT BE ASKED": a declared bundle whose
inventory file is ABSENT is an ANSWER — an invalid release declaration — and is
reported at `error`, exactly as the scenarios below require, and a member absent
at the commit is drift rather than a skip.

**A SECOND CORRECTION, 2026-08-25, SAME DEFECT FAMILY (PR #331, Copilot).** The
sentence above once said the family is SKIPPED where "the declared bundle's
inventory file is absent" — a stale survivor from before the proposal round's
tightening, which decided that case is an `error`. The scenarios below and the
shipped code had said `error` since; only the summary sentence lagged, and
promotion faithfully copied the inconsistency into canon. Corrected so the prose
states what the scenarios decided. THIS CHANGES NO DECISION: the scenarios
govern, the code already implements them, and the sentence is aligned to both
rather than either being altered.

#### Scenario: A non-editorial member has drifted
- **WHEN** a member other than the changelog, the manifest or the README differs from the digest the declared bundle's inventory records
- **THEN** the family MUST emit an `error` finding naming that member and the declared bundle
- **AND** the action MUST name a release cut through the bundle realization order, never a hand-edit of the inventory

#### Scenario: Only editorial members have drifted
- **WHEN** the only differing members are the changelog, the manifest and the README
- **THEN** the family MUST emit `info` findings only, and the run MUST NOT redden under a gate set to `error` or `critical`

#### Scenario: The tree matches the declared bundle exactly
- **WHEN** every inventory member matches its recorded digest
- **THEN** the family MUST emit no finding

#### Scenario: A repository declares no bundle
- **WHEN** a repository in scope carries no declared contract bundle at all
- **THEN** the family MUST report a skip naming the reason, never an empty pass

#### Scenario: A declared bundle has no inventory
- **WHEN** a repository DECLARES a bundle and that bundle's inventory file is absent
- **THEN** the family MUST emit an `error`, never a skip — a declaration naming an inventory that does not exist is an INVALID RELEASE DECLARATION, not an absent capability, and it is what a mistyped bundle name or a half-created release looks like
- **AND** the canonical verifier already reports this condition as `HGR-RELEASE-INVENTORY-MISSING` rather than declining to answer

#### Scenario: An inventory member is absent at the commit
- **WHEN** a member the declared bundle's inventory names does not exist at the checked commit
- **THEN** the family MUST report it as NON-EDITORIAL DRIFT at `error`, never as a skip — a deleted normative member is the strongest form of the drift this family exists to catch, and a skip would make deletion indistinguishable from unavailability
- **AND** this MUST hold even where the underlying blob read degrades to a null result, so the family MUST distinguish "this path is absent at this commit" from "version control could not be consulted"

#### Scenario: Version control cannot answer at all
- **WHEN** the git dependency is unavailable, or the checked commit itself cannot be resolved
- **THEN** the family MUST report a skip rather than fall back to working-tree bytes, because an uncommitted edit is not drift from the declared bundle
- **AND** the skip MUST NOT be used for any per-member absence, which the scenario above governs

### Requirement: Promotion fidelity of archived spec deltas
The promotion fidelity family SHALL compare every archived spec delta against
the promoted specification it was ratified to reach, and report a finding
where the delta's requirement did not arrive — reporting against the archived
delta's own path and naming the promoted spec it failed to reach.

The obligation being checked belongs to `document-lifecycle` ("Ratified spec
deltas reach the promoted specification"); this requirement defines only how
doc-health checks it, in the same by-reference relationship tag hygiene already
has with that capability's marker grammar.

The family SHALL implement three resolution rules, each of which exists to
prevent a specific false positive rather than to narrow the check:

- **Latest writer wins.** For a given capability and requirement title, only
  the MOST RECENT archived delta touching it is authoritative. Ordering is by
  the archive folder's `YYYY-MM-DD` prefix; a folder carrying no such prefix
  never outranks one that does. Where two archived changes share a date, the
  tie SHALL be broken by the packets' archive-commit order, falling back —
  only where version-control history cannot answer — to folder name ascending,
  and then to statement order within one delta file.
- **A `RENAMED` block retires the title it names.** `openspec archive` applies
  RENAMED before MODIFIED, so a later rename legitimately removes an earlier
  delta's title from canon and MUST NOT be reported as a missing requirement.
- **Archiving is presumed to be ratification, and only an explicit
  pre-ratification standing exempts a delta.** An archived packet's deltas
  SHALL be checked unless its own `proposal.md` carries a `Status:` whose
  declared standing is `draft` or lower in this corpus's taxonomy
  (`brainstorm`, `staged`, `draft`); a packet carrying a ratified-or-later
  standing, an unrecognized value, no `Status:` header, or no `proposal.md`
  at all SHALL be checked. The declared standing is the header value's leading
  token, read the same way in both directions, so an annotated ratification
  (`Status: ratified (approved at ...)`) declares `ratified` for the same
  reason an annotated `draft` declares `draft`. The status SHALL be read
  through the same lifecycle header reader every other family uses, never
  through a second one; a missing or invalid header is the status-validity
  family's finding to report, not this one's.

A recorded disposition in the aggregation checkout's `health/dispositions.yaml`
— an entry naming this family with a `cite`, optionally narrowed to one
requirement — SHALL suppress the findings it names. Nothing else suppresses:
a label, a title, or a claim in prose is not a disposition.

**This family SHALL be enforcing, in both halves of what that means.** Every
finding it emits SHALL carry `error` severity, so a run configured to fail on
`error` fails on a ratified delta that never reached canon; and the family
SHALL be classified `contested`, so a finding that stops being reported
without a recorded citation becomes an `error` under this capability's
uncited-resolution rule. The two SHALL move together and MUST NOT be taken
apart: severity alone gates the family without the disposition discipline
that makes a disappearing finding accountable, and the contested class alone
gates it through `uncited-resolution` under a family name that does not say
what happened.

The family SHIPPED ADVISORY and was flipped by ruling, which is the sequence
this requirement records rather than a history it has replaced. At launch
every finding carried `warning` and the family was deliberately unclassified,
because no run had yet measured what the domain factories' archives would say
and a `contested` advisory family would have gated through the back door on
the first finding anyone fixed. The flip SHALL be taken as one decision by
ruling, never as a judgement call inside an implementation, and SHALL follow
the discharge of the standing population rather than precede it — a gate that
goes red on the commit introducing it teaches everyone to route around the
gate.

#### Scenario: A ratified delta did not reach canon
- **WHEN** the authoritative archived delta for a capability and requirement ADDED or MODIFIED it, and the promoted `openspec/specs/<capability>/spec.md` lacks that requirement title, or lacks a scenario title the delta states under it
- **THEN** the run MUST emit an `error` finding against the archived delta's path, naming the requirement, the promoted spec, and each absent scenario
- **AND** the finding MUST cause a run configured `--fail-on error` to fail, and MUST NOT cause a run configured `--fail-on critical` to fail
- **AND** the finding MUST carry the `contested` resolution class

#### Scenario: A ratified removal did not reach canon
- **WHEN** the authoritative archived delta REMOVED a requirement and the promoted spec still carries it
- **THEN** the run MUST emit an `error` finding naming the requirement and the promoted spec that still carries it

#### Scenario: A capability was never promoted at all
- **WHEN** an authoritative archived delta ADDED or MODIFIED a requirement for a capability with no promoted spec file
- **THEN** the run MUST report the requirement against the delta's path, stating that the capability has no promoted spec

#### Scenario: An earlier delta was superseded
- **WHEN** a later archived ratified change rewrote, renamed, or removed what an earlier archived delta stated
- **THEN** only the later delta MUST be checked, and the earlier one MUST NOT produce a finding

#### Scenario: A deliberate non-promotion was recorded
- **WHEN** an archived packet's own `proposal.md` declares a standing of `draft` or lower
- **THEN** its spec deltas MUST NOT be checked for arrival in canon
- **AND** an annotation after the standing MUST NOT change what it declares

#### Scenario: An archived packet declares no pre-ratification standing
- **WHEN** an archived packet's `proposal.md` declares a ratified-or-later standing, declares a standing the taxonomy does not recognize, carries no `Status:` header, or is absent altogether
- **THEN** its spec deltas MUST be checked for arrival in canon, archiving being presumed to be ratification
- **AND** the missing or invalid header itself MUST be left to the status validity family rather than reported here

### Requirement: The promotion fidelity measurement basis is declared
A doc-health run SHALL compare archived deltas against the checked-out tree by
default — the same tree every other check family measures — and MAY be
configured to compare them against each repository's own live `main` instead.
That option SHALL apply to the promotion fidelity family alone; no other
family's inputs change because it is set.

A run's report SHALL state which basis this family measured, in the family's
own report section, on every run and whether or not the family found anything.
Where a live basis is requested and a repository's live `main` cannot be read,
the run SHALL measure that repository from its checkout and SHALL name the
repository as having fallen back — a report that mixed the two bases without
saying which was which would invite a reader to act on a stale finding as a
current one.

The obligation being checked does not change with the basis. What changes is
which state of the repository the run is speaking about, and a reader can only
act on a finding if the report says which.

#### Scenario: A run declares the live basis
- **WHEN** a run is configured to measure this family against live `main`s
- **THEN** the promotion fidelity family MUST read each repository's archived deltas and promoted specs from that repository's own live `main`
- **AND** every other check family MUST measure the checked-out tree exactly as it does on a default run
- **AND** the report MUST state the basis, and the resolved `main` it read, in the promotion fidelity section

#### Scenario: A live main cannot be read
- **WHEN** the live basis is requested and a repository's live `main` is unavailable to the run
- **THEN** that repository MUST be measured from its checkout rather than skipped
- **AND** the report MUST name that repository as having fallen back to the checkout

#### Scenario: A run declares no basis
- **WHEN** a run is not configured with a basis
- **THEN** the family MUST measure the checked-out tree
- **AND** the report MUST say so in the family's section

#### Scenario: A finding is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an archived delta path, and a `cite`
- **THEN** findings on that path MUST be suppressed, or only the named requirement's finding where the entry carries a `requirement` key
- **AND** an entry without a `cite` MUST suppress nothing

#### Scenario: No repository in scope carries an archive
- **WHEN** no repository in the run's scope has an `openspec/changes/archive/` directory
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted

