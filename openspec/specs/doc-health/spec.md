# doc-health Specification

## Purpose

Define the deterministic health-check contract for the factory family's
governance corpus: the check families, finding severities, the dated report
and ranked plan, the headline canon-share metric, and the ownership split
between contract, implementation, and the nightly runner.

## Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty-three check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, promotion fidelity, release-inventory drift,
duplicate packet, family enumeration, modified-block currency, and release-tag
publication.
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
an advisory report. Four of the twenty-three — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
nineteen families and every corpus census, word count, canon-share figure,
shared-inventory entry, and catalog record SHALL be computed from the
governed corpus alone and MUST NOT move because the lifecycle scan set
exists. The promotion fidelity family reads archived spec DELTAS and promoted
SPECS — bodies rather than headers — and therefore takes neither the governed
corpus nor the lifecycle scan set as its document list; it moves no census,
word count, canon-share figure, inventory entry, or catalog record either. The
release-inventory drift family reads CONTRACT ARTIFACT BYTES — a release digest
inventory and the blobs it names — and likewise takes neither document list,
and it moves no census, word count, canon-share figure, inventory entry, or
catalog record. The duplicate packet family reads archived spec deltas ONLY
AGAINST EACH OTHER — never against canon, which by construction cannot show
that a ruling was discharged twice — and takes neither document list and moves
none of those figures either. The family enumeration family reads THIS
REQUIREMENT and the code registry that satisfies it — a promoted spec and a
Python dict, neither of them a governed-corpus document — so it likewise takes
neither document list and moves none of those figures. The modified-block
currency family reads ACTIVE CHANGE DELTAS, the promoted SPECS they have not yet
replaced, and each active change's own `proposal.md` — the last read only to
resolve whether one active writer declares its deltas relative to another, which
`release-realization` governs — so it likewise takes neither the governed corpus
nor the lifecycle scan set as its document list, and it moves no census, word
count, canon-share figure, inventory entry, or catalog record either.
The release-tag publication family reads the DECLARED BUNDLE and the
repository's PUBLISHED TAG REFS — a manifest field and a set of git refs,
neither of them a governed-corpus document — so it likewise takes neither the
governed corpus nor the lifecycle scan set as its document list, and it moves no
census, word count, canon-share figure, inventory entry, or catalog record
either.

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

**THE ORDERING DEPENDENCY RESOLVED, 2026-08-25 — appended, with the paragraph
above left exactly as ratified.** `add-promotion-fidelity-check` archived
(`560e0bd5`), so two sentences above are now historical rather than current, and
they are corrected here rather than edited in place. First: the `promotion
fidelity` bullet's "as its owning requirement below defines" is no longer a
forward reference — that requirement is promoted canon, and the bullet resolves
against it. Second: this block no longer differs from canon by TWO `AND`
bullets. Canon absorbed the inherited one when the sibling archived, so exactly
ONE bullet here is new, and it is this change's own — `duplicate packet`.
Verified at this archive gate scenario-by-scenario: 8 of canon's 8 scenarios
restated, 7 byte-identical, and the eighth differing by that single bullet and
nothing else. This change is the third and last of the three siblings that each
restated this requirement, so the chain closes here — the enumeration reaches
twenty and no further active change is left holding a version of it.

**FOURTH RESTATEMENT, AND THE FIRST ONE A CHECK VERIFIED — appended
2026-08-25, with every paragraph above left exactly as promoted.** The three
notes above record three separate repairs of this one requirement, all three
caught by a human. This block is the fourth restatement of it, and it is the
first written under `add-family-enumeration-check`: its own delta half read
this block, resolved every name here against `families.FAMILIES`, and checked
all three numerals before the change could be committed. The enumeration
reaches twenty-one and the counts are derived rather than re-typed. That the
check policing this requirement had to restate this requirement to add itself
to it is deliberate, and it is the acceptance test — a wrong restatement here
could not have landed, because the thing it would corrupt was standing at the
gate.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** client identity roster composition MUST assemble the per-client roster fragments published by each pinned domain repository as its owning requirement in `client-identity-roster` defines
- **AND** promotion fidelity MUST compare each repository's archived spec deltas against its promoted specs as its owning requirement below defines
- **AND** release-inventory drift MUST compare each repository's declared bundle inventory against the blobs it names as its owning requirement below defines
- **AND** duplicate packet MUST compare each repository's archived spec deltas against each other as its owning requirement below defines
- **AND** family enumeration MUST verify this requirement's own family enumeration and counts against the code registry as its owning requirement below defines
- **AND** modified-block currency MUST compare each active change's `## MODIFIED Requirements` blocks against the promoted requirements they replace as its owning requirement below defines
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
ACTIVE proposal, active supporting-document folders with missing or
invalid manifests, `Status: staged` documents under active proposal support,
archive manifests whose bundle or file hashes do not verify, and supporting
bundles stored under canonical `openspec/specs/`.

A citation of an ARCHIVED change SHALL NOT raise the staged-material finding.
That finding's remedy is to move the material into the cited proposal's
supporting-docs folder, and an archived packet is closed: the move names an act
nobody can perform, so the finding would report a defect with no conforming
resolution. Archived-ness SHALL be read from the change tree rather than
presumed, and the union of active and archived ids that other families require
— a ratification citation may name an archived change, and must — SHALL remain
available to them unchanged.

#### Scenario: Proposed material remains in staging
- **WHEN** a staged document names an ACTIVE OpenSpec change as its exit or proposal
- **THEN** doc-health MUST report that document as stale staged state

#### Scenario: Staged material cites a change that has archived
- **WHEN** a staged document's only cited exit or proposal names a change that has archived
- **THEN** doc-health MUST NOT report that document as stale staged state
- **AND** the id MUST remain resolvable to the families that read the union of active and archived changes

#### Scenario: Staged material cites both an archived and an active change
- **WHEN** a staged document names both an archived change and an active one as its exits
- **THEN** doc-health MUST report the document against the ACTIVE change
- **AND** the finding MUST NOT name the archived change, whose supporting-docs folder cannot receive the material

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
support manifest; an ad-hoc origin lacking `reason`; an ad-hoc origin that
claims approval without the whole of the approval pair; an ad-hoc origin
that declares neither approval nor drafting provenance, and so declares no
provenance state at all; an ad-hoc origin whose declared drafting provenance
is incomplete; a proposal whose own declared status claims ratification or
beyond while its origin asserts no approval;
and mutation of an origin declaration after ratification. Backfilled
origins SHALL be validated against recorded migration provenance; the
family MUST NOT fabricate or infer staging history for changes that predate
the contract.

The family's finding classes are therefore SEVEN, named: `missing-origin`,
`malformed-origin`, `origin-mismatch`, `staged-origin-unresolvable`,
`adhoc-provenance-incomplete`, `drafting-provenance-incomplete`, and
`unapproved-origin-at-ratification`. The last two are added by
`add-drafted-proposal-origin` and are the two halves of one rule: an
unapproved draft is EXPRESSIBLE, and an approval APPEARS when a status claims
it.

**THE UNAPPROVED STATE PRODUCES NO FINDING, AND THAT IS THE POINT OF ADDING
IT.** Before it existed this family reported every drafted-but-unapproved
packet — an `ad_hoc` origin without `approved_on` was
`adhoc-provenance-incomplete`, a packet with no origin block at all was
`missing-origin`, and no third shape existed, so the only ways to clear the
finding were to approve the change, delete the draft, or invent an approval
date. The last is the defect this family exists to catch, and a rule whose
only mechanical remedy is the defect it forbids does not survive contact with
the repository's own workflow: a "scout and draft, do not implement"
assignment is SUPPOSED to yield a packet that exists, validates, and is not
yet approved.

`unapproved-origin-at-ratification` is `error` with resolution class
`contested`, and the class is argued rather than inherited: resolving the
finding either TRANSCRIBES an approval act that happened or WITHDRAWS a status
claim that should not have been made, and the third move — writing a date
nobody gave — is the defect. `drafting-provenance-incomplete` is mechanical:
a half-written pair is completed from the record of who drafted it.

The status the last class reads SHALL be the packet's own declared `Status:`,
read through the single lifecycle-header reader this contract already
requires, and the class SHALL fire only where the packet POSITIVELY declares
the unapproved state. Silence is not that state: an origin that merely omits
its approval has declared no provenance state and is reported as such, so a
packet cannot buy the lenient treatment by leaving fields out. Archival is
not a status claim either — an archived packet may lawfully declare a
pre-ratification standing, and this family MUST NOT read the fact of
archiving as the approval its origin does not carry.

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

#### Scenario: An unapproved draft declares its origin
- **WHEN** a proposal declaring a pre-ratification standing carries an ad-hoc origin with `reason`, `proposed_by`, and `proposed_on`, and no approval fields
- **THEN** the family MUST report nothing against that origin
- **AND** the absence of `approved_by` and `approved_on` MUST NOT be reported as incomplete provenance

#### Scenario: A declared status claims a ratification the origin does not carry
- **WHEN** a proposal's own `Status:` declares `ratified` or any standing beyond it while its origin carries drafting provenance and asserts no approval
- **THEN** the family MUST emit an `error` finding with resolution class `contested`, naming the declared status
- **AND** the finding MUST NOT be resolvable by writing an approval date the record does not carry

#### Scenario: Declared drafting provenance is incomplete
- **WHEN** an ad-hoc origin declares one of `proposed_by` or `proposed_on` and not the other, and asserts no approval
- **THEN** the family MUST emit an `error` finding naming the missing field as a drafting-provenance defect rather than as a missing approval

#### Scenario: An ad-hoc origin declares no provenance state
- **WHEN** an ad-hoc origin carries neither a complete approval pair nor any drafting field
- **THEN** the family MUST emit one `error` finding naming both lawful shapes rather than one finding per absent approval field

#### Scenario: A claimed approval is incomplete
- **WHEN** an ad-hoc origin carries one of `approved_by` or `approved_on` without the other
- **THEN** the family MUST report the missing field exactly as it did before the unapproved state existed

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

### Requirement: One ruling, one discharge, across archived packets
The duplicate packet family SHALL compare every archived spec delta against
every other archived spec delta in the same repository, and report where two
packets state the same capability and requirement title with content-identical
requirement bodies and neither packet's proposal names the other — reporting
against the later packet's own delta path and naming the earlier packet it
restates.

The obligation being checked belongs to `document-lifecycle` ("A ruling is
discharged once"); this requirement defines only how doc-health checks it, in
the same by-reference relationship promotion fidelity already has with that
capability's promotion obligation.

**This family answers a question the promotion fidelity family cannot.** That
family compares an archived delta to CANON, and where one ruling has been
discharged twice canon holds exactly what both packets said it should hold — so
it reports zero either way. The comparison that can see the class is between the
archived deltas themselves, which is why this is a separate family rather than
a wider reading of that one.

The family SHALL implement one identity rule and one exemption, and the
exemption is what keeps the lawful remedy legal:

- **Content identity, not resemblance.** Two archived packets state the same
  thing only where their requirement bodies are byte-identical after trailing
  whitespace — per-line trailing spaces and trailing blank lines — is
  normalized, and after no other normalization. The requirement's own heading
  line is not part of the body compared, because the title is compared through
  the family's title normalization already. A similarity or near-match rule
  MUST NOT be used: revising a requirement is not restating it, and a rule
  loose enough to conflate the two would report the ordinary case.
- **A recorded remedial lineage is exempt.** Where either packet's own
  `proposal.md` names the other's change id — in the bare change-id spelling or
  as the archived folder that carries it, matched as a whole token so that one
  change id occurring inside a longer one buys no exemption — the pair SHALL
  NOT be reported. Applying an already-ratified delta byte-faithfully is the
  prescribed remedy for a promotion gap, and naming the packet whose ruling is
  being applied is what makes the second statement traceable to the first.
  The naming records LINEAGE, not authority: it does not establish that the
  restating packet had standing to restate, which is the ratified provenance
  family's question, and this family MUST NOT be read as deciding it.
- **The pre-ratification and disposition exemptions are the existing ones.** A
  packet whose own `proposal.md` declares a standing of `draft` or lower
  discharged no ruling and SHALL NOT be paired, read through the same
  lifecycle header reader the promotion fidelity family uses rather than a
  second one. A recorded disposition in the aggregation checkout's
  `health/dispositions.yaml` naming THIS family, with a `cite`, optionally
  narrowed to one requirement, SHALL suppress the findings it names; an entry
  naming another family MUST NOT suppress this family's findings.

The comparison SHALL be pairwise within each identity: three packets stating
one requirement identically are three pairs, and a pair carrying a recorded
lineage says nothing about a pair that does not.

**This family SHALL measure the checked-out tree.** The live-`main` basis this
capability defines applies to the promotion fidelity family alone, and a report
that said otherwise while this family read a pin would mislead every reader of
its basis line.

**This family SHALL be enforcing, in both halves of what that means.** Every
finding it emits SHALL carry `error` severity, so a run configured to fail on
`error` fails on a ruling discharged twice; and the family SHALL be classified
`contested`, so a finding that stops being reported without a recorded citation
becomes an `error` under this capability's uncited-resolution rule. The two
SHALL move together and MUST NOT be taken apart: severity alone gates the
family without the discipline that makes a disappearing finding accountable,
and the contested class alone gates it through `uncited-resolution` under a
family name that does not say what happened.

The family SHIPPED ADVISORY and was flipped by ruling, which is the sequence
this requirement records rather than a history it has replaced. At launch every
finding carried `warning` and the family was deliberately unclassified, because
no run had yet measured what any archive outside this repository would say and
a `contested` advisory family would have gated through the back door on the
first duplicate anyone withdrew. The flip SHALL be taken as one decision by
ruling, never as a judgement call inside an implementation, and SHALL follow a
measurement showing the population it will gate is discharged rather than
precede it — a gate that goes red on the commit introducing it teaches everyone
to route around the gate. The measurement SHALL be taken on the basis this
family enforces on, which is the checked-out tree; a zero measured on some
other tree is a fact about that tree.

#### Scenario: Two packets discharge one ruling with no account of each other
- **WHEN** two archived packets state the same capability and requirement title with requirement bodies identical after trailing-whitespace normalization, and neither packet's `proposal.md` names the other's change id
- **THEN** the run MUST emit an `error` finding against the later packet's archived delta path, naming both packets, the requirement, the capability, and a digest of the restated block
- **AND** the finding MUST cause a run configured `--fail-on error` to fail, and MUST NOT cause a run configured `--fail-on critical` to fail
- **AND** the finding MUST carry the `contested` resolution class

#### Scenario: A remedial packet names the ruling it applies
- **WHEN** an archived packet restates another archived packet's ratified delta byte-faithfully and its own `proposal.md` names that packet's change id
- **THEN** the pair MUST NOT be reported
- **AND** the change id MUST be matched as a whole token, so that a packet naming only itself gains no exemption because another packet's id is a fragment of its own

#### Scenario: Two remedials of one ruling do not name each other
- **WHEN** two archived packets each restate a third packet's ratified delta and each names that third packet, but neither names the other
- **THEN** the two pairs involving the original MUST NOT be reported
- **AND** the pair the two remedials form MUST be reported

#### Scenario: A requirement is revised rather than restated
- **WHEN** a later archived packet states a requirement title an earlier packet also stated, with any difference in the requirement body beyond trailing whitespace
- **THEN** the pair MUST NOT be reported, a revision not being a second discharge

#### Scenario: A pre-ratification packet restates another
- **WHEN** two archived packets state identical requirement bodies and either one's `proposal.md` declares a standing of `draft` or lower
- **THEN** the pair MUST NOT be reported, a packet that claimed no ratification having discharged no ruling

#### Scenario: A finding is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an archived delta path, and a `cite`
- **THEN** findings on that path MUST be suppressed, or only the named requirement's finding where the entry carries a `requirement` key
- **AND** an entry naming a different family MUST suppress nothing here

#### Scenario: A reported duplicate stops being reported
- **WHEN** a finding this family reported in a previous report is absent from a later report, and the family actually ran in that later run
- **THEN** the disappearance MUST be reported under the uncited-resolution rule unless a citation records the governance act that closed it
- **AND** a run CONFIGURED not to execute this family MUST NOT have that family's absent findings read as resolved, a family that never ran having looked at nothing

#### Scenario: No repository in scope carries an archive
- **WHEN** no repository in the run's scope has an `openspec/changes/archive/` directory
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted

### Requirement: The readiness derivation proof resolves the repository under test
The readiness derivation proof SHALL resolve the repository under test before
any other checkout, and SHALL NEVER read a different checkout in its place
without saying so in the run's own output.

The proof is the verification that the readiness lane's cluster derivation
still reproduces the landed `ideation-cross-reference` index. It needs two
things from a checkout — the index and the corpus the index pins — and today
it finds them by walking UP from its own location to the first ancestor
holding a `openxFactory/ideation/cross-reference.yaml`. In the aggregation
workspace that walk always terminates on the one shared checkout beneath the
aggregation root, whatever repository the run was actually launched against.
Resolution order is therefore reversed here: the repository under test first,
any other checkout only as a declared fallback, and never silently.

An ancestor search or an environment override MAY serve as that fallback. When
one is used, the run MUST name the checkout it resolved and the reason the
fallback was taken, so that a proof about repository A is never reported as
though it were a proof about repository B. The same resolution order SHALL
govern every checkout the readiness surface reaches for — the index, the
corpus, and the pinned index validator the checker spawns — because a proof
that reads its subject from one checkout and its validator from another has
proved nothing about either.

#### Scenario: The proof runs from a worktree of the repository under test
- **WHEN** the proof runs from any working tree of a repository that itself carries `ideation/cross-reference.yaml`
- **THEN** it MUST read that repository's own index, corpus, and validator
- **AND** it MUST NOT resolve to a sibling checkout that happens to sit above it on the filesystem

#### Scenario: The repository under test cannot serve the proof
- **WHEN** the repository under test does not carry the index and a declared fallback checkout does
- **THEN** the run MUST record which checkout it resolved and why the fallback was taken
- **AND** the fallback MUST be reached only after the repository under test has been tried and found wanting

#### Scenario: No checkout can serve the proof
- **WHEN** neither the repository under test nor any declared fallback carries the index
- **THEN** the run MUST report the proof as not performed, naming that reason
- **AND** it MUST NOT report a pass

### Requirement: The derivation comparison reads committed index state
The derivation comparison SHALL read the landed index from committed state
rather than from a working tree, so that an uncommitted edit — in the
repository under test or in any other checkout on the machine — can neither
red nor green the verdict.

Both sides of the comparison are already revision-addressed on the corpus
side: the derived clusters are built from the corpus reconstructed at the
index's own `generation.source_revision`. The index side is not, and the
asymmetry is the defect. An index read from a working tree is whatever
somebody happens to be editing at that moment, which makes the verdict a
function of a concurrent session rather than of the repository's committed
content.

The comparison SHALL therefore name the committed revision it read the index
at, and SHALL read the corpus at the revision that index pins. A consequence
is stated rather than left implicit: an index edit under review is proved when
it is committed, not while it sits in a working tree. That is the intended
trade — a proof that changes its answer depending on who else is editing is
not a proof.

#### Scenario: Another session holds an uncommitted index edit
- **WHEN** a checkout on the machine carries an uncommitted change to `ideation/cross-reference.yaml`
- **THEN** the verdict MUST equal the verdict the same revision yields on a clean tree
- **AND** the run MUST NOT read that edit as the index under test

#### Scenario: The comparison assembles its two sides
- **WHEN** the comparison reads the index and the corpus
- **THEN** the index MUST be read at a named committed revision of the repository under test
- **AND** the corpus MUST be read at the revision that index itself pins

#### Scenario: The change under review edits the index
- **WHEN** a working tree carries an index edit that has not been committed
- **THEN** the proof MUST state that it read committed state and name the revision it read
- **AND** the edit MUST become subject to the proof once committed, rather than being proved from the working tree

### Requirement: An unreachable pinned revision fails the proof
An unreachable pinned `source_revision` SHALL fail the readiness derivation
proof whenever the repository under test is a complete clone, and SHALL be
reported as skipped only where the repository's history is genuinely truncated.

A pin the repository cannot resolve is not an environment inconvenience: it
means the index names a corpus state that no reader can reconstruct, so the
index's own provenance claim is unverifiable. Reporting that as a skip
converts a defect in the index into a silent absence of verification, and the
absence is invisible precisely because a skip looks like a healthy run.

The two conditions SHALL be distinguished by observation rather than by
supposition, and the reported reason SHALL name the condition observed. A
complete clone missing the object is a finding about the index; a truncated
history missing the object is a finding about the clone; and a reason that
guesses at the second while standing in the first is worse than no reason,
because it sends the reader to the wrong repair.

This obligation is on the verification, not on the nightly lane's findings:
the readiness lane's own output remains report-only under its owning
requirement, and nothing here makes a lane finding block a merge.

#### Scenario: The pin is unreachable in a complete clone
- **WHEN** the index pins a revision the repository under test cannot resolve, and that repository's history is not truncated
- **THEN** the proof MUST fail, naming the pinned revision and the index that carries it
- **AND** it MUST NOT be reported as a skip

#### Scenario: The clone is truncated
- **WHEN** the repository under test is shallow or its history is otherwise truncated, and the pinned revision lies outside the fetched history
- **THEN** the proof MAY be reported as skipped
- **AND** the reason MUST name the truncation actually observed rather than offering it as a conjecture

#### Scenario: The pin resolves
- **WHEN** the pinned revision resolves in the repository under test
- **THEN** the comparison MUST run and its result MUST be the verdict
- **AND** no resolution branch may return a skip in place of a comparison that could have been performed

### Requirement: The family enumeration is derived, not restated on trust
The doc-health suite SHALL verify that the family enumeration and the counts
stated by the "Deterministic check families" requirement agree exactly with the
code registry of families the suite actually runs, and report every divergence
naming precisely what diverged.

The requirement being checked is this capability's own, which is the point: it
NAMES every check family and COUNTS them three times in prose, and every new
family must restate that whole requirement to add itself. A requirement whose
text every new family must restate is a requirement every new family can
truncate. Three changes in three days truncated it, and all three were caught
by a human rather than by a check.

The registry SHALL be the mapping of family ids the suite iterates when it
runs, and it SHALL be the sole authority for which check families exist. The
reporting list that drives the report's per-family sections SHALL name exactly
the families the registry registers — no more, so that a section is never
promised for a family that does not run, and no fewer, so that a family's
findings are never counted in the headline and the ranked plan while rendering
under no section at all. The reporting list's ORDER is presentational and is
not constrained by this requirement.

**AMENDED 2026-08-25 ON BRETT'S RULING, before promotion.** As first written
this paragraph said the reporting list "is a separate declaration and is
allowed to be a subset", and the scenario below said a registered family absent
from it MUST NOT be reported. That was written from the state of the code rather
than from what the code should be, and it would have ratified a live defect:
two registered families, `staged-topic-template` and `proposal-origin`, were
absent from the list and between them carried 61 findings — three of them
ERRORS — with no section to render under. Brett ruled the drift fixed ("fix the
FAMILY_IDS drift"); the realization landed in the same change as this
amendment, and the equality is pinned by test rather than left to prose.

The verification SHALL cover BOTH the promoted requirement AND every ACTIVE
change delta that restates it:

- **A promoted enumeration** SHALL name exactly the registered families, each
  once, and its numerals SHALL be arithmetically true of that set: the stated
  total equals the number registered, a stated subset-of-total agrees with that
  total, and a stated remainder equals the total minus the stated subset.
- **An active change delta restating the requirement** SHALL carry the complete
  enumeration, consistent with the registry in its own tree. A change that
  registers a new family states that family in its delta, so the two are
  self-consistent before promotion and the incomplete restatement is reported
  at authoring time rather than at an archive gate.
- **The promoted requirement SHALL be exempt from the count comparison while
  an active delta restates it**, because a change that registers family N+1
  leaves canon stating N until it archives. Canon is pending there, not
  divergent, and the delta is what carries the obligation.
- Where more than one active delta restates the requirement, EACH SHALL be
  checked independently against the registry, because a `MODIFIED` requirement
  replaces its promoted counterpart wholesale and whichever change archives
  last is the one canon keeps.

A prose family name SHALL resolve to a registry id by a mechanical
normalization plus a declared alias set, and a name that resolves to no
registered family SHALL be reported rather than guessed at. The alias set
SHALL be minimal — an alias that is no longer needed is itself a defect.

**This family SHALL be advisory at launch.** Every finding it emits carries
`warning` severity, so it publishes into the report and the ranked plan without
failing any run configured to fail on `error` or `critical`, and it is
deliberately NOT classified `contested`, because a contested finding that
resolves without a citation becomes an `error` under this capability's
uncited-resolution rule — which would make the family gate-blocking through the
back door on the first divergence anyone corrected. Raising the severity and
adding the contested classification are ONE later decision taken together by
ruling, and SHALL follow a measurement of the population the gate would red
rather than precede it.

#### Scenario: The promoted enumeration omits a registered family
- **WHEN** no active change delta restates the requirement, and the promoted enumeration does not name a family the registry registers
- **THEN** the run MUST emit a `warning` finding against the promoted spec's path, naming the omitted families and the registered total
- **AND** the finding MUST NOT cause a run to fail under `--fail-on error` or `--fail-on critical`

#### Scenario: The promoted enumeration carries a stale numeral
- **WHEN** no active change delta restates the requirement, and the stated total differs from the number of registered families, or a stated remainder does not equal the stated total minus the stated subset
- **THEN** the run MUST emit a finding naming the stated numeral, the derived one, and which sentence carried it

#### Scenario: The promoted enumeration names an unregistered family
- **WHEN** the enumeration names a family that resolves to no registered family id
- **THEN** the run MUST report that name and the id it resolved to, rather than ignoring it or matching it approximately

#### Scenario: An active delta restates the requirement incompletely
- **WHEN** an active change's `doc-health` delta restates the requirement and its enumeration omits a registered family, names an unregistered one, or carries a numeral inconsistent with the registry in its own tree
- **THEN** the run MUST emit a finding against that delta's own path, so the incomplete restatement is reported before it can be promoted

#### Scenario: A change adds a family and canon has not moved yet
- **WHEN** an active change registers a new family and restates the requirement completely for its own tree, while the promoted requirement still states the previous total
- **THEN** the promoted requirement MUST NOT be reported, its statement being pending promotion rather than divergent
- **AND** the active delta MUST be reported if ITS restatement is incomplete

#### Scenario: Two active deltas both restate the requirement
- **WHEN** two or more active changes each restate the requirement
- **THEN** each delta MUST be checked independently against the registry, neither one excusing the other

#### Scenario: The reporting list promises a section for no family
- **WHEN** the reporting list names an id the registry does not register
- **THEN** the run MUST report it, a report section for a family that never runs being invisible to every other check
- **AND** a registered family ABSENT from the reporting list MUST also be reported, by the suite's own tests rather than as a run finding, both declarations being constants of one package

#### Scenario: No promoted doc-health specification is in scope
- **WHEN** no repository in the run's scope carries a promoted `doc-health` specification
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted

### Requirement: Derivation-pin reachability is verified across a declared artifact class
The doc-health suite SHALL verify derivation-pin reachability across every
committed artifact class that records a repo-local commit pin, rather than
across the cross-reference index alone, and the class SHALL be DECLARED and
checked rather than discovered afresh on each run.

The promoted obligation this extends already exists and covers exactly one
artifact: an unreachable pinned `source_revision` fails the readiness
derivation proof. That requirement is not restated here and nothing about it
moves. What it does not reach is every OTHER committed artifact in this
repository that records the same kind of pin — the derivation and readiness
evidence records under `health/`, gate records under `ideation/dashboard/`, and
any future artifact whose generator stamps a revision. The two live orphans in
this repository at authoring are both in that uncovered remainder, which is the
evidence that a per-artifact obligation does not generalize on its own.

THE DECLARED CLASS IS THE MECHANISM, and it is declared for the same reason the
family enumeration is derived rather than trusted: a scan that finds pin-carrying
artifacts by pattern will silently stop covering an artifact whose generator
renames its key, and a silent loss of coverage looks exactly like a clean run.
The verification SHALL therefore compare the declared class against what the
repository actually carries, and report a pin-carrying artifact that no declared
class member covers — naming the artifact and the key — rather than passing over
it. The declaration MUST distinguish repo-local commit pins from cross-repository
pins, because only the former are answerable against this repository's own refs.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, and the enumeration and its numerals in
the "Deterministic check families" requirement are deliberately untouched and
unrestated. Two reasons, and the first is about the check rather than about
convenience. Reachability is not deterministic in the sense that requirement
means: identical governance-corpus inputs produce different answers in a shallow
clone and a complete one, because the answer is a function of fetched history
rather than of the corpus. A check whose verdict moves with clone depth does not
belong in a pass whose defining property is that identical inputs produce
identical findings. Second, that requirement is the one requirement in this
capability that EVERY new family must restate in full, and a `MODIFIED` block
replaces its counterpart wholesale — so each family added puts canon's family
list at the mercy of archive order, and a requirement every new family must
restate is a requirement every new family can truncate. That hazard is not
hypothetical: three changes in three days truncated it, all three caught by a
human rather than by a check, and this capability now carries a promoted family
whose whole purpose is to catch the next one. A verification that needs no family
declines the hazard entirely rather than managing it.

The verification SHALL live where the existing pin obligation already lives —
the readiness proof surface and the per-repo validator preflight — and SHALL
report a pin unreachable in a complete clone as a failure while reporting a
truncated clone as a skip that names the truncation observed, by reference to the
promoted requirement that already states that split rather than by restating it.

THE REF SET CONSULTED IS `main` PLUS THE RETENTION NAMESPACE
`refs/retention/pins/<full-sha>`, and no more. A pin that neither reaches is
unreachable; a pin either reaches is conforming. The namespace is derivable from
the pin itself, so the verification computes the ref name rather than enumerating
a namespace, which is what keeps the check cheap and keeps a stray ref elsewhere
in the repository from silently greening a pin nobody can find.

#### Scenario: A pin-carrying artifact outside the index is orphaned
- **WHEN** a declared class member other than the cross-reference index carries a pin reachable from no ref, in a complete clone
- **THEN** the run MUST report it, naming the artifact, the pin key, and the pinned commit
- **AND** the report MUST NOT be limited to the cross-reference index because that is where the obligation was first stated

#### Scenario: An artifact carries a pin no declared class covers
- **WHEN** the repository carries a committed artifact recording a repo-local commit pin that no declared class member covers
- **THEN** the run MUST report the uncovered artifact and the key it carries, so the coverage gap is visible rather than invisible
- **AND** the run MUST NOT report the class as fully verified

#### Scenario: A declared member's pin is reachable but stale
- **WHEN** a declared class member pins an ancestor of `main` that is not its tip
- **THEN** no finding is emitted, because staleness between regenerations is legal under the owning capability's rule
- **AND** the verification MUST NOT convert an age comparison into a reachability finding

#### Scenario: The clone cannot answer the question
- **WHEN** the repository under test is shallow or its history is otherwise truncated
- **THEN** the run MUST report the verification as skipped, naming the truncation actually observed
- **AND** no deterministic check family is added, removed, or renumbered by this verification in any run configuration

### Requirement: Currency of an active change's MODIFIED requirement blocks
The modified-block currency family SHALL compare every active change's
`## MODIFIED Requirements` block against the requirement as the promoted
specification currently states it, and report what the block does not carry —
reporting against the active delta's own path, while the change can still be
edited.

The obligation being checked belongs to `document-lifecycle` ("A MODIFIED
requirement block restates the requirement as canon currently states it"); this
requirement defines only how doc-health checks it, in the same by-reference
relationship promotion fidelity and duplicate packet already have with that
capability's obligations.

**This family answers a question the promotion fidelity family cannot, and it
asks it at the only time the answer is cheap.** That family compares an
archived delta to canon, and after an archive act canon IS the delta — a block
that dropped seven scenarios and a canon that now lacks them agree perfectly,
so that family reports nothing. The comparison that can see the class is
between an active delta and the canon it has not yet replaced, which is a
different document pair read at a different moment, and is why this is a
separate family rather than a wider reading of that one. It is also why the
loss is invisible to counting: the file-level scenario count can stay flat
while a requirement goes from eight scenarios to one, because a change's own
ADDED requirement offsets what its MODIFIED block drops.

**The family SHALL read every active change regardless of its lifecycle
standing.** A `draft` packet's block is as capable of restating stale canon as
a `ratified` one, and a finding against a draft costs its author one line —
which is the cheapest moment to pay it, the scenario-title arm below now
carrying an `error` that reds any run configured to fail on it. This is a
reading rule for the check and is deliberately WIDER than the two-writers
obligation below, which `release-realization` scopes to an active RATIFIED
change and which this requirement does not widen.

The family SHALL implement three comparison arms over one document pair, and
SHALL report them as distinct finding classes so that a precise signal is never
buried in an editorial one:

- **Scenario-title completeness.** Every `#### Scenario:` title the promoted
  requirement carries SHALL appear as a scenario title in the block. This arm
  reports deletion at the granularity the defect occurs at, its inputs are
  short titled strings rather than prose, and it is the arm that carries this
  family's gate.
- **The carriage ledger.** Every body unit of the promoted requirement, and
  every scenario bullet it carries, SHALL be reported where the block does not
  carry it. Scenario bullets SHALL be compared against ALL bullets of ALL
  scenarios in the block, never scenario by scenario: a bullet carries the
  requirement's actual obligations, and pairing each bullet to the scenario
  that restates it would let a block retitle a scenario, declare the retitle,
  and drop the bullets underneath it unreported. This arm CANNOT distinguish a
  deliberate rewording from stale text and SHALL NOT be read as claiming it
  does; it is the list a reviewer reads to confirm that each divergence is one
  the change intended. It SHALL emit at most one finding per requirement,
  listing the units, rather than one finding per unit.
- **Title resolution and the two-writers rule.** A MODIFIED block whose
  capability and requirement title resolve to no promoted requirement SHALL be
  resolved in order: FIRST against the change's own `## RENAMED Requirements`
  block, and where that block renames a promoted requirement to this title the
  three arms above SHALL run against canon under the OLD name, a rename being a
  change of title rather than of the content a block must carry; THEN against a
  requirement an active sibling change ADDS or RENAMES. Where a title resolves
  to none of those, the block SHALL be reported. Where two active changes carry
  a MODIFIED block for ONE promoted requirement, ORDER IS BY DECLARATION AND
  NEVER BY DATE. `release-realization`'s "Ordered deltas and branch vocabulary"
  already requires the later proposal to reference the earlier change and
  declare its deltas relative to that change's outcome, so the change that
  makes that declaration IS the later writer and nothing else needs to decide
  it. The declaration SHALL be read as the sibling's change id occurring as a
  whole token in the declaring change's own `proposal.md` — the whole-token
  match the duplicate packet family already uses, so one change id occurring
  inside a longer one satisfies nothing. The declaring block SHALL be measured
  against the declared sibling's outcome rather than against canon, and the
  sibling's additions SHALL be present in it. EXACTLY ONE of two active
  RATIFIED writers SHALL declare: where neither does the run SHALL report the
  undeclared ordering against both blocks, and where both declare relative to
  each other the run SHALL report that too, mutual declaration deciding
  nothing. Where no declaration stands, each block SHALL be measured against
  canon, which is the only basis a reader can name. No folder name, commit
  timestamp, or `created:` date SHALL be consulted.

**A canon unit is CARRIED only by a block unit of the SAME KIND, matched in
full after whitespace normalization.** Normalization collapses runs of
whitespace to a single space and strips leading and trailing whitespace, so a
re-wrapped paragraph compares equal to the same paragraph wrapped differently;
no normalization beyond it applies. A canon body unit is carried only by a body
unit of the block, a canon scenario title only by a scenario title of the
block, and a canon scenario bullet only by a scenario bullet of the block.
**Matching MUST NOT be substring containment.** A block bullet that CONTAINS
canon's bullet has replaced it — which is precisely how issue #351's widened
line entered — and a containment rule would report nothing there. A similarity
or near-match rule MUST NOT be used either: it would accept a clause whose
meaning had been reversed, which is also on this class's record, and the
corpus has already ruled against resemblance as an identity test in the
duplicate packet family.

**The units of a requirement SHALL be derived mechanically, and the derivation
is normative.** Backticked spans SHALL be masked before any sentence split, so
that a period inside `.openspec.yaml` or `promotion_fidelity.py` never ends a
sentence. In the requirement BODY — everything above the first
`#### Scenario:` — each bullet line SHALL be one unit with its list marker
stripped; each dated bold note SHALL be one unit, undivided, a note being a
single editorial statement whose sentences mean nothing apart; and every other
paragraph SHALL be split into sentences at a period, question mark or
exclamation mark followed by whitespace or the end of the paragraph. In the
SCENARIOS, each `#### Scenario:` heading SHALL be one title unit and each
bullet line SHALL be one bullet unit. A paragraph of RESERVED MARKER form —
defined below — SHALL NOT be a unit of either kind, in canon or in a block.

**A deliberate deletion SHALL be declared by a RESERVED MARKER, recognized by
form and never by prose.** A marker is ONE PARAGRAPH inside the MODIFIED block,
read after the same whitespace normalization every other unit gets so that a
marker wrapped across several lines is still one marker, in one of exactly two
forms:

- `**Removed from canon by <change-id> (<YYYY-MM-DD>):**` followed by the
  deleted units, then ` — <reason>`.
- ``**Merged into `<destination scenario title>` by <change-id> (<YYYY-MM-DD>):**``
  followed by the superseded scenario titles — the form for two scenarios
  legitimately becoming one. The destination is written as a code span like
  every other title this marker carries, and in this one spelling everywhere.

**A paragraph is of MARKER FORM only where, after normalization, it BEGINS with
one of those two prefixes COMPLETE** — the bold run, a resolvable change-id, an
ISO date in parentheses, and the closing colon. A paragraph that merely quotes,
templates or describes a marker does not begin with one, and is an ordinary body
unit like any other prose. This anchor is load-bearing rather than pedantic:
this requirement's own text and `document-lifecycle`'s both set out the two
templates in prose, both promote into canon, and a looser test would read them
as markers and exempt them from carriage — the check quietly declining to check
the paragraphs that define it.

**Every unit a marker names, and the `Merged into` destination, SHALL be written
as a CommonMark code span, and a unit that itself contains backticks SHALL be
fenced with a longer run of them.** Roughly a third of this corpus's requirement
body units and a sixth of its scenario bullets contain a backtick, because they
cite things like `openxFactory` or `promotion_fidelity.py`; a single-backtick
span around such a unit ends at its first inner backtick and names a fragment,
so the marker would name something that is not a unit at all. CommonMark already
provides the longer fence and this rule adds nothing to it. The parser SHALL
extract the code spans following the colon, in order, per CommonMark, and THE
REASON SHALL BEGIN AT THE FIRST ` — ` SEPARATOR STANDING OUTSIDE EVERY CODE
SPAN: the units named are the spans that close before that separator, the reason
is everything after it, and a code span that falls inside the reason is prose
the reason quotes rather than a unit the marker names. Where no such separator
stands, every span names a unit and the marker carries no reason, which is what
the written-out `Merged into` example below is. The boundary is read the same
way in both forms, the `Merged into` destination being matched in the prefix and
the tail after the closing colon being parsed identically. Semicolons and dashes
inside a unit or inside a reason are therefore irrelevant, because extraction is
by code span and never by splitting on punctuation.

**The `Merged into` destination is NOT a named unit.** It states where the
superseded scenarios went, and it is present in the block by construction —
reading it as a named unit would make every valid merge marker report itself
under the rule below. Only the code spans after the colon name units.

A marker SHALL suppress only the units it names AND that are in fact absent from
the block. A MARKER SHALL ITSELF BE REPORTED ON ANY OF THREE GROUNDS, each of
them one finding at the `info` band this family's marker-defect class already
carries: it names a unit the block still carries; or a code span standing INSIDE
its reason matches EXACTLY a unit of the requirement's basis that the block does
not carry and that no marker declares removed, the boundary above reading that
span as prose rather than as a name, so that its author declared nothing about a
unit they plainly had in mind; or it names something matching no unit of the
requirement's basis and no unit of the block. Each of the three is a declaration
that does not describe the block, which is a declaration no reader can rely on,
and a report on the MARKER is what points an author at the paragraph they wrote
rather than at the unit it failed to declare. THE SECOND GROUND SHALL BE READ NARROWLY, on the exact match and never
on the span's position alone: a reason is prose and prose in this corpus quotes,
so a code span inside a reason matching no unit of the requirement is the NORMAL
FORM of a reason and SHALL NOT be reported. The second ground SHALL NOT withdraw
the carriage arms from the unit the span would have named — the scenario below
that keeps that unit subject to them stands unchanged — the report being added
BESIDE the carriage and never in place of it.

**A named scenario TITLE carries its bullets with it ONLY IN A GENUINE
REMOVAL.** Where a `Removed from canon` marker names a scenario title AND the
block adds no scenario title canon does not already carry, the bullets that
scenario carried in canon SHALL also be treated as declared removed — unless
they appear as bullets elsewhere in the block, in which case they are carried
and nothing is reported about them either way. Declaring a scenario genuinely
gone and then reporting its bullets forever would make the declaration useless
for the act it exists to declare.

**Where the block DOES add a scenario title canon does not carry, a
`Removed from canon` marker SHALL NOT suppress the removed title's bullets.**
That shape is a retitle, whatever the marker calls it, and treating it as a
removal reopens the defect the bullet arm exists to close: name the old title
removed, add a replacement carrying two of its four bullets, and two obligations
leave canon with nothing reported. The author's instrument for a retitle is
`Merged into`, whose bullets must be carried somewhere in the block or named
individually in a `Removed from canon` marker of their own. **A `Merged into`
marker names titles only**, so a bullet a merge makes redundant is a declared
removal, not a permanent editorial row — but it has to be declared as a bullet,
one at a time, which is exactly the deliberation the class deserves.

**A marker is NOT a carriage unit, in either direction.** A marker promotes into
canon with the requirement that carries it, and if it were a unit every later
block would have to restate every marker any predecessor ever wrote, forever.
The durable record of a deletion is the archived delta, which is where every
other archived governance act is read from.

Written out, the two forms are exactly:

```
**Removed from canon by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`; ``an adapter that reaches a hosted provider SHALL obtain its credential through the `openxFactory` broker lane`` — the affordance is now tile-bound and the credential clause moved to its own requirement
**Merged into `Tile-bound gate verbs hide on a composed view` by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`
```

**The marker is NEW, and the existing dated-note convention MUST NOT be reused
for it.** Every dated bold note in this corpus today records a caught near-miss
and a RESTORATION, never a deletion — and `doc-health`'s own "Deterministic
check families" carries one naming SEVEN of its eight scenario titles in
backticks as restored. A rule that read deletion out of prose would therefore
read a faithful restatement of that very requirement as declaring seven
scenarios deleted, on the requirement whose truncation is issue #329. Form,
not prose, is what makes the declaration falsifiable.

A recorded disposition in the aggregation checkout's `health/dispositions.yaml`
naming THIS family, with a `cite`, optionally narrowed to one requirement,
SHALL suppress the findings it names; an entry naming another family MUST NOT
suppress this family's findings. Nothing else suppresses.

**This family SHALL measure the checked-out tree.** The live-`main` basis this
capability defines applies to the promotion fidelity family alone, and it would
be actively wrong here: an active change lives on a branch, so a family reading
`main` would measure a delta `main` does not carry against canon the branch may
have moved.

**This family SHALL be ENFORCING IN ONE ARM AND CLASSIFIED `contested` WHOLE,
which is what the flip of 2026-08-31 left behind.** Every finding of the
scenario-title completeness arm — the arm that carries this family's gate —
SHALL carry `error` severity, so a run configured to fail on `error` fails on a
MODIFIED block that drops a scenario canon still carries; every other class the
family emits SHALL keep the band its own rule states, the title-resolution and
ordering arm at `warning` and the carriage ledger and the marker defects at
`info`, so no `--fail-on` configuration reds on those; and the family SHALL be
classified `contested`, so a finding of ANY of its classes is a contested
finding, and a session working a report's ranked plan SHALL NOT apply a
state-changing edit for one, escalating it to a change proposal or a recorded
disposition instead. THE DISAPPEARANCE THAT OWES A CITATION IS READ AT THE
GRAIN THE UNCITED-RESOLUTION RULE KEYS ON, WHICH IS `(family, repository,
path)` AND NOT THE CLASS: where this family stops reporting at a repository and
path the previous report carried, the resolution is uncited without a recorded
citation and SHALL be the `error` that rule defines; where a finding of ONE
class stops being reported while ANY other finding of this family is still
emitted at that same repository and path, the key never leaves the current
report and the rule does not fire — which the promoted *A
modified-block-currency finding its own class map cannot place is itself a
finding* already states of this family's key, and this requirement neither
widens nor narrows it. THE RESOLUTION TABLE HAS NO PER-CLASS GRAIN — it is
applied by finding FAMILY alone, one string every arm and every class of this
module shares — so the classification reaches every class the family emits, and
neither this requirement nor any other can hold one class out of it.

THE FAMILY SHIPPED ADVISORY IN BOTH HALVES AND WAS FLIPPED IN BOTH BY ONE
RULING, WHICH RAISED EXACTLY ONE SEVERITY ARM AND LEFT EVERY OTHER BAND WHERE
IT STOOD, which is the sequence this requirement records rather than a history
it has replaced. At launch every finding carried `warning` or `info` and the
family was deliberately absent from `FAMILY_RESOLUTION`, because no run had yet
measured what the governed repositories' active changes would say and a
`contested` advisory family would have gated through the back door on the first
block anyone corrected. The flip SHALL be taken as ONE decision by ruling,
never as a judgement call inside an implementation, and SHALL follow the
discharge of the standing population rather than precede it — a gate that goes
red on the commit introducing it teaches everyone to route around the gate. IT
WAS TAKEN THAT WAY: the ruling of 2026-08-27 was "MEASURE FIRST, THEN FLIP",
the nightly aggregation runs of 2026-08-30 and 2026-08-31 read the
scenario-title arm's population at ZERO across every governed repository, and
the flip was ordered on 2026-08-31 and landed as ONE COMMIT that raised the
scenario-title arm's severity constant to `error` and added the family's
`contested` row together (openxFactory issue #357, pull request #529). THE TWO
HALVES MOVE TOGETHER AND MUST NOT BE TAKEN APART: severity alone gates the
family without the disposition discipline that makes a disappearing finding
accountable, and the contested class alone gates it through
`uncited-resolution` under a family name that does not say what happened. **No
flip is proposed for the carriage ledger in this change**, whose population is
standing by construction — every legitimate MODIFIED block edits something — so
an editorial band is the honest launch state; a later flip remains available
and is a ruling like any other.

**AMENDED BY `amend-marker-reason-boundary` (2026-09-06).** Every paragraph and
every scenario above this note stands exactly as promoted, and the only change
this block makes to promoted text is to ONE body sentence: the one that told the
parser to measure a marker's reason from BEHIND, from its LAST code span. TWO
SCENARIOS ARE ADDED, at the END of the block, and they pin that sentence rather
than restate it — a normative rule no scenario exercises is a rule the next
author re-deriving this parser has nothing to test against. No promoted scenario
moves, is retitled or loses a bullet; no arm is removed, no severity changes, no
threshold moves, no disposition rule changes, and the set of trees over which
this family speaks is not altered by one line.

MEASURING THE REASON FROM BEHIND MAKES EVERY CODE SPAN AN AUTHOR WRITES INSIDE
IT A NAME. A reason is prose, and prose in this corpus quotes: the two markers
`doc-health`'s own *Release-tag publication* carries each name the `WHEN` bullet
they retire and then, in the reason that explains the retirement, quote the
words `WHEN` and `AND` as code spans — so the promoted parser reads THREE
declared-removed names where each author declared one, and reads the explanation
as no reason at all. Measured on this corpus on 2026-09-06, ACROSS THE PROMOTED
SPECIFICATIONS AND EVERY ACTIVE DELTA OTHER THAN THIS ONE — this block carries
an eighth marker, the one below, and a figure a reader is invited to re-derive
must name the tree it was taken on: SEVEN unit-naming markers, of which TWO are
misread this way and FIVE are unaffected; and of 17,566 derived units NONE
is literally `WHEN` or `AND`, and neither is any unit this block's own text
adds, so today every wrongly-derived name matches no
canon unit, suppresses nothing and is reported as nothing. **THE DEFECT IS
INERT AND IS NOT HARMLESS.** The names a marker derives are what it suppresses,
and the next author whose reason quotes a real unit — a scenario title, a clause
this corpus actually carries — declares that unit removed by mentioning it. The
boundary above puts the reason where its author put it, and its direction of
failure is the conservative one: a marker that separated its names with ` — `
would have the later ones read as reason, would suppress nothing with them, and
the units it meant to name would be REPORTED rather than silently dropped. No
marker in this corpus is written that way, which is what the seven were measured
to establish.

**AMENDED BY `amend-marker-defect-reporting` (2026-09-09).** Every paragraph
and every scenario above this note stands exactly as promoted —
`amend-marker-reason-boundary`'s own note and its narrative included — and the
only change this block makes to promoted text is to ONE body sentence: the one
that gave a marker exactly ONE reporting ground. TWO SCENARIOS ARE ADDED, at the
END of the block, one for each ground added, because a normative ground no
scenario exercises is a ground the next author re-deriving this class has nothing
to test against. No promoted scenario moves, is retitled or loses a bullet: the
reason-quotes scenario's third `AND`, which keeps the quoted unit subject to the
carriage arms, is carried word for word, this amendment adding a report about the
MARKER beside that carriage rather than replacing it. No arm is removed, no
severity moves, no threshold moves, no disposition rule changes, this family's
registration in the resolution table is untouched, and the set of trees over
which this family speaks is not altered by one line. AND
`amend-marker-reason-boundary`'S OWN `Removed from canon` MARKER IS DELIBERATELY
NOT RESTATED HERE, on this requirement's own rule that a marker is not a
carriage unit in either direction: restating it would declare a removal this
change did not perform, and its named unit — a sentence canon no longer carries
because that change removed it — matches no unit of the requirement or of this
block, which is the third ground above reporting this block for copying a
predecessor's declaration forward.

A MARKER IS A DECLARATION, AND UNTIL THIS AMENDMENT A DECLARATION THAT DESCRIBED
NOTHING WAS SILENT IN TWO WAYS. The first is as old as the family: a name
matching no unit of the requirement suppressed nothing and was reported as
nothing, which `add-modified-block-currency-check` recorded as a plausible later
ruling it had no standing to take, because this sentence gave a marker exactly
one reporting ground. The second is younger than the boundary:
`amend-marker-reason-boundary` correctly stopped reading a code span inside a
reason as a name, and an author who separates two NAMES with the separator
therefore declares only the first — the second is read as prose, suppresses
nothing, and the unit it meant to declare is REPORTED, which is the conservative
direction, but the marker that caused it is not, so its author is pointed at a
unit rather than at their own paragraph. THE SECOND GROUND IS NARROW BY DESIGN
AND THE MEASUREMENT IS WHY. Measured on this corpus on 2026-09-09, across every
promoted specification and every active delta OTHER THAN THIS ONE — this block
carries a marker of its own and a figure a reader is invited to re-derive must
name the tree it was taken on: SIXTEEN unit-naming markers, of which EIGHT quote
a code span inside their reason, every one of them a marker promoted into canon
and every quoted span reason-prose; and of those quoted spans, ZERO is a derived
unit of the document carrying it. So a ground written on the span's POSITION
would report eight legitimate markers the moment a MODIFIED block restated one
of them, and would grow with the corpus, while a ground written on an EXACT
MATCH against an uncarried unit is silent on all eight. THE POPULATION OF BOTH
NEW GROUNDS IS ZERO TODAY, and that is measured rather than hoped: of the active
MODIFIED blocks this family reads, TWO carry a unit-naming marker at all, both
of the `Merged into` form, each naming one unit that matches its resolved basis,
neither quoting a code span in a reason. A ground whose population is zero at
landing is a ground that reports the NEXT marker written, which is the only
moment at which either silence has ever cost anybody anything.

**AMENDED BY `amend-modified-block-currency-standing` (2026-09-10).** Every
paragraph and every scenario above this note stands exactly as promoted —
`amend-marker-reason-boundary`'s and `amend-marker-defect-reporting`'s own
notes and their narratives included — and the only promoted text this block
changes is what the flip of 2026-08-31 made untrue: ONE sentence of the
lifecycle-standing paragraph, TWO sentences of the *advisory at launch*
paragraph, and TWO bullets of the first scenario. ONE SCENARIO IS ADDED, at the
END of the block, because the resolution row reaches every class this family
emits and no scenario exercised that — stated at the `(family, repository,
path)` grain the uncited-resolution rule keys on, never at finding-class grain,
which is the grain that rule has always read and is not moved here. No arm is
added or removed, no threshold moves, no disposition rule changes, no parse and
no marker grammar moves, and the set of trees over which this family speaks is
not altered by one line. THIS BLOCK MOVES NO SEVERITY AND ADDS NO ROW: the
scenario-title arm's severity constant has read `error` and
`families.FAMILY_RESOLUTION` has carried `"modified-block-currency": CONTESTED`
since 2026-08-31, so this is promoted canon catching up with running code
rather than a new decision — the same catch-up the promoted *A
modified-block-currency finding its own class map cannot place is itself a
finding* performed for its own sentence on the day that flip landed. THE
SENTENCE ABOVE STATING THAT NO FLIP IS PROPOSED FOR THE CARRIAGE LEDGER IS
CARRIED UNCHANGED AND IS STILL TRUE: its "this change" names
`add-modified-block-currency-check`, which promoted this requirement, no flip
has been ruled for that arm since, and its band is `info` today. AND
`amend-marker-defect-reporting`'S OWN `Removed from canon` MARKER IS
DELIBERATELY NOT RESTATED HERE, on this requirement's own rule that a marker is
not a carriage unit in either direction: restating it would declare a removal
this change did not perform, and its named unit — a sentence canon no longer
carries because that change removed it — matches no unit of the requirement or
of this block, which is the third ground above reporting this block for copying
a predecessor's declaration forward.

**Removed from canon by amend-modified-block-currency-standing (2026-09-10):**
``**The family SHALL read every active change regardless of its lifecycle
standing.** A `draft` packet's block is as capable of restating stale canon as
a `ratified` one, the arms below are advisory, and a finding against a draft
costs its author one line.``; ``**This family SHALL be advisory at launch, in
both halves of what that means.** Every finding carries `warning` severity for
the scenario-completeness and title-resolution arms and `info` for the carriage
ledger, so no `--fail-on` configuration reds on it; and the family is
deliberately absent from `FAMILY_RESOLUTION`, so its findings are not
classified `contested` — a contested finding that resolves without a citation
becomes an `error` under this capability's uncited-resolution rule, which would
gate the family through the back door on the first block anyone corrected.``;
``Raising the scenario-completeness arm to `error` and adding the contested
classification are ONE later decision taken together by ruling, and SHALL
follow the discharge of the standing population rather than precede it.``;
``**THEN** the run MUST emit a `warning` finding against the active delta's own
path, naming each omitted scenario title and the promoted spec it was read
from``; ``**AND** the finding MUST NOT cause a run configured `--fail-on error`
or `--fail-on critical` to fail`` — the flip of 2026-08-31 (openxFactory issue
#357, pull request #529) took the scenario-title arm to error and added the
family's contested row, so each of these five units asserts a standing the
running checker has not had since that day: three say the arms are advisory and
the family unclassified, one says the raising is a decision still to be taken,
and two are the first scenario's assertion of the advisory band in bullet form.
Every one is REPLACED rather than dropped — the two paragraphs above state the
post-flip standing and the history that produced it, the lifecycle-standing
sentence is restated with its rationale corrected, and the two bullets are
replaced in place by three that mirror the promoted promotion fidelity and
duplicate packet scenarios. This reason carries no code span, so the marker
names exactly the five units listed before the separator.

#### Scenario: An active block drops a scenario the requirement keeps
- **WHEN** an active change's MODIFIED block restates a promoted requirement and omits a scenario title that requirement currently carries, with no marker naming it
- **THEN** the run MUST emit an `error` finding against the active delta's own path, naming each omitted scenario title and the promoted spec it was read from
- **AND** the finding MUST cause a run configured `--fail-on error` to fail, and MUST NOT cause a run configured `--fail-on critical` to fail
- **AND** the finding MUST carry the `contested` resolution class

#### Scenario: A deletion is declared by marker
- **WHEN** the MODIFIED block carries a `Removed from canon by` or `Merged into` marker naming a unit as a code span, and that unit is absent from the block
- **THEN** that unit MUST NOT be reported
- **AND** the suppression MUST extend to exactly the units named and to no others

#### Scenario: A genuinely removed scenario title carries its bullets with it
- **WHEN** a `Removed from canon` marker names a scenario title that is absent from the block, and the block adds NO scenario title the promoted requirement does not already carry
- **THEN** the bullets that scenario carried in canon MUST NOT be reported either, the title's removal declaring them
- **AND** a bullet of that scenario that DOES appear elsewhere in the block MUST be treated as carried

#### Scenario: A removal marker is used where the block adds a replacement scenario
- **WHEN** a `Removed from canon` marker names a scenario title AND the block adds a scenario title the promoted requirement does not carry
- **THEN** the removed title's bullets MUST NOT be suppressed by that marker, the shape being a retitle rather than a removal however it is labelled
- **AND** every such bullet the block does not carry somewhere MUST be reported, unless it is itself named in a `Removed from canon` marker as a bullet

#### Scenario: A marker names a unit the block still carries
- **WHEN** a marker names a scenario title or body unit that the block does in fact restate
- **THEN** the run MUST report the marker itself, a declaration that does not describe the block being unusable as evidence about it

#### Scenario: A block does not carry canon's body text or a scenario bullet
- **WHEN** an active MODIFIED block does not carry a body unit of the promoted requirement, or one of its scenario bullets, as a unit of the same kind after whitespace normalization
- **THEN** the run MUST emit one `info` finding for that requirement listing every uncarried unit
- **AND** the finding MUST NOT assert that the divergence is unintended, the arm having no means to distinguish a rewording from stale text

#### Scenario: A block retitles a scenario and drops its bullets
- **WHEN** a block replaces a scenario title with a new one, declares the replacement by marker, and does not carry every bullet the superseded scenario carried
- **THEN** the uncarried bullets MUST still be reported, the bullet comparison running across all bullets of the block rather than within the scenario that restates them

#### Scenario: Two active changes modify one requirement and one declares
- **WHEN** two or more active changes carry a MODIFIED block for the same capability and requirement title, and exactly one declares its deltas relative to another by naming that change as a whole token in its own `proposal.md`
- **THEN** the declaring change MUST be treated as the later writer, and its block MUST be measured against the declared sibling's outcome rather than against canon
- **AND** an addition the sibling's block makes that the declaring block does not carry MUST be reported against the declaring delta's path
- **AND** no folder name, commit timestamp, or `created:` date MUST be consulted to decide which writer is later

#### Scenario: Two active ratified changes modify one requirement and the ordering is undeclared
- **WHEN** two active ratified changes carry a MODIFIED block for one promoted requirement and neither names the other as `release-realization` requires
- **THEN** the run MUST report the undeclared ordering against both blocks, no reader being able to tell which text canon will keep
- **AND** where both declare relative to each other, the run MUST report that as well, mutual declaration deciding nothing
- **AND** each block MUST meanwhile be measured against canon, the only basis a reader can name while no declaration stands

#### Scenario: A change renames a requirement and modifies it in one delta
- **WHEN** a MODIFIED block names a title canon does not carry, and the change's own `## RENAMED Requirements` block renames a promoted requirement to that title
- **THEN** the block MUST NOT be reported as unresolved
- **AND** the three arms MUST compare it against the promoted requirement under its OLD name, a rename changing a title rather than the content the block must carry

#### Scenario: A MODIFIED title resolves to an active sibling's addition
- **WHEN** a MODIFIED block names a requirement canon does not carry, and an active sibling change ADDS or RENAMES that title
- **THEN** the block MUST NOT be reported as unresolved, the promoted requirement being pending rather than absent

#### Scenario: A MODIFIED title resolves to nothing at all
- **WHEN** a MODIFIED block names a capability and requirement title carried neither by the promoted spec, nor by the change's own `## RENAMED Requirements` block, nor by any active change's ADDED or RENAMED block
- **THEN** the run MUST emit a finding naming the unresolved title, a block modifying nothing being a block whose promotion adds text nobody reviewed as an addition

#### Scenario: A finding is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an active delta path, and a `cite`
- **THEN** findings on that path MUST be suppressed, or only the named requirement's findings where the entry carries a `requirement` key
- **AND** an entry without a `cite`, or an entry naming another family, MUST suppress nothing

#### Scenario: No repository in scope carries active changes
- **WHEN** no repository in the run's scope has an `openspec/changes/` directory the family can read
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted
- **AND** a scope that carries active changes but no `## MODIFIED Requirements` block among them MUST NOT be reported as skipped, the family having run and found nothing

#### Scenario: A marker's reason quotes a code span
- **WHEN** a unit-naming marker's tail carries a ` — ` separator standing outside every code span, and a code span falls after that separator
- **THEN** that span MUST NOT be read as a unit the marker names, a reason being prose that quotes rather than a declaration
- **AND** the units named MUST be exactly the spans that close before that separator, and the reason MUST be everything after it
- **AND** the units the span would have named MUST therefore remain subject to the carriage arms, an author who only mentioned a unit having declared nothing about it

#### Scenario: A marker's tail carries no separator outside a code span
- **WHEN** a unit-naming marker's tail carries no ` — ` separator standing outside every code span, a separator INSIDE a span being that unit's own bytes rather than a boundary
- **THEN** every code span after the closing colon MUST name a unit
- **AND** the marker MUST carry no reason, which is the form the written-out `Merged into` example above is in

#### Scenario: A marker's reason quotes a unit the block does not carry
- **WHEN** a code span standing after a unit-naming marker's reason separator, and not also named before it, matches a unit of the requirement's basis exactly, and neither the block nor any marker in it accounts for that unit
- **THEN** the run MUST report the marker itself in the `info` band, the span having been read as prose while the unit it had in mind went undeclared
- **AND** the unit MUST remain subject to the carriage arms, the report being added beside that carriage rather than in place of it
- **AND** a code span inside a reason that matches NO unit of the requirement's basis MUST NOT be reported, a reason being prose that quotes and this corpus's markers quoting one routinely

#### Scenario: A marker names something no unit matches
- **WHEN** a marker names a code span matching no unit of the requirement's basis and no unit of the block
- **THEN** the run MUST report the marker itself in the `info` band, a declaration about nothing being unusable as evidence about the block
- **AND** the name MUST suppress nothing, which is the reading this family has always taken and is unchanged by the report

#### Scenario: This family stops reporting a path without a citation
- **WHEN** this family emitted one or more findings — of ANY class, the `info` carriage ledger included — at a repository and delta path the previous report carried, the next report carries NO finding of this family at that repository and path, and no OpenSpec change or recorded disposition cites the resolution
- **THEN** the run MUST emit the uncited-resolution `error` this capability's contested-finding rule defines, the family's resolution row having no per-class grain to hold one class out of it
- **AND** a finding of ONE class that stops being reported while ANY other finding of this family is still emitted at that same repository and path MUST NOT raise that error, the rule keying on `(family, repository, path)` alone, so the key never leaves the current report
- **AND** the disappeared finding's own severity MUST NOT be read as moved by that classification, the resolution class and the severity being separate fields

### Requirement: A declared unrecoverable pin loss is discharged by a superseding record, never by deleting its declaration
A declared loss of a pinned commit SHALL stay declared and reported for as long
as the pin stands committed, and the verification SHALL treat that loss as
answered ONLY where a superseding record naming it is committed and readable —
never on the strength of the declaration having been removed.

WHY THIS NEEDS SAYING AT ALL, and why in this capability. The obligation to
issue a superseding record where a pinned object is unrecoverable is stated
where the pin obligation lives, and nothing here restates or moves it. What that
obligation does not say is what the VERIFICATION does afterwards, and the
verification is this capability's. Between the two there was exactly one route
from "this class carries a permanently lost pin" to "this class is fully
verified", and it ran through deleting the declaration. That route is a
silencing: it discards the measurement that established the loss, it makes the
next reader unable to tell a repository that never had the defect from one that
erased it, and it converts the one condition in this class that no code change
can repair into background noise. The route this requirement states instead is
that the governance act lands, the declaration CITES it, and the verification
goes and reads it.

THE LOSS IS NEVER SILENCED BY ITS DISCHARGE, and the two halves are separate
questions. "Is this pin reachable?" is answered LOST for ever: the object is
gone, no ref reaches it, and every run says so with the measurement that
established it. "Has the class been left with an unanswered obligation?" is
answered by whether the superseding record exists. A discharged loss therefore
still reports as a declared unrecoverable loss, still carries its measurement,
and is still re-measured — because the day such an object turns out to be
recoverable, retention becomes the route and the declaration is stale.

THE CITATION IS READ, NOT BELIEVED. A declaration naming a superseding record
SHALL be satisfied only by committed state at the revision under test: the
record present at the path the declaration names, and naming the pin it claims
to supersede. A citation of a record nobody committed, a record deleted after
the fact, or a stub that never mentions the lost object is a dangling citation,
and a dangling citation is worse than a blank one because it reads as
discharged.

THE DISPOSITION IS RECORDED WHERE THE REPORT IS PRODUCED. The standing report of
an unrecoverable loss is not a deterministic check-family finding and MUST NOT be
disposed as one: this verification registers no check family, emits no family
finding, and therefore offers no (family, repo, path) tuple for a finding
disposition to match. Its disposition SHALL be carried by the loss declaration
itself, citing the superseding record — the same place the measurement and the
outstanding act are already carried, so a reader who can see the report can see
its disposition without a second lookup that could drift from it.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, and the enumeration and its numerals in
the "Deterministic check families" requirement are deliberately untouched and
unrestated. The verification this governs adds none, for the reasons that
verification's own requirement states; a discharge mechanism inside it adds none
either, and a `MODIFIED` block over a requirement every new family must restate
in full is exactly the hazard this capability now carries a family to police.

#### Scenario: The superseding record has not landed
- **WHEN** a pin declared unrecoverable stands committed and no superseding record for it is committed
- **THEN** the verification MUST NOT report the class as fully verified, and MUST report the loss with the measurement that established it and the governance act still owed
- **AND** the run MUST NOT fail on that loss alone, because no code change repairs it and reddening every unrelated change on a standing governance obligation is enforcement arriving by the back door

#### Scenario: The superseding record lands
- **WHEN** a superseding record naming that pin is committed at the path the declaration cites
- **THEN** the verification MUST report the class as fully verified again if nothing else is outstanding, because the obligation that held it open has been met
- **AND** the loss MUST still be reported as a declared unrecoverable loss, with its measurement, in every run

#### Scenario: The declaration cites a record the repository does not carry
- **WHEN** a declaration names a superseding record that is not committed at the revision under test, or names one that does not mention the pin it claims to supersede
- **THEN** the loss MUST be treated as still awaiting its record, exactly as if nothing were cited
- **AND** the citation MUST NOT be accepted on the strength of being written, because a discharge nobody can read is not a discharge

#### Scenario: The declaration is deleted instead of discharged
- **WHEN** a change removes the declaration of an unrecoverable loss while the pin it describes still stands committed
- **THEN** the pin MUST be reported as an orphaned pin — a repairable defect that fails the run — rather than passing silently, so deletion cannot be used to obtain a clean report
- **AND** the measurement the declaration carried MUST NOT be treated as superseded by its own removal

### Requirement: A declared sentinel is verified as a legal non-pin, and an undeclared non-commit value is a defect
The pin verification SHALL classify a derivation-pin value that is not a commit
name into one of exactly two outcomes — a LEGAL NON-PIN where the value is
declared in the shared sentinel vocabulary, or a DEFECT where it is not — and
MUST NOT leave such a value unclassified.

SILENCE IS THE CURRENT ANSWER, AND SILENCE IS THE DEFECT. The verification finds
pins by matching a commit-shaped value against a declared key, so a key holding
anything else produces no site at all: it is not reachable, not orphaned, not
lost, and — this is the part that matters — not UNCOVERED either. The artifact
is swept, the key is declared, the file is a member of the class in good
standing, and the value is skipped. A run therefore reports a fully verified
class over an artifact whose central provenance claim nothing has read. That is
exactly the silent-coverage shape the declared class was built to end, arriving
through the value rather than through the key, and the declared class does not
close it because the class declares WHICH KEYS carry pins and never what a
non-commit value in one of them means.

THE LEGAL NON-PIN IS A FIFTH OUTCOME, NOT A PASS IN DISGUISE. It sits beside
reachable, orphaned, lost and uncovered rather than inside any of them, and the
distinctions are load-bearing in both directions. It is NOT reachable: there is
no commit, so no ref reaches it and reporting it as reachable would claim a
resolution nobody performed. It is NOT orphaned or lost: those verdicts say a
named commit cannot be found, and here no commit was ever named, so a repair
route — retention, re-derivation, a superseding record — would be offered for a
defect that does not exist. It is NOT uncovered: the key is declared and the
sweep did read the site, so reporting a coverage gap would send the next reader
to widen a declaration that is already correct. And a legal non-pin MUST NOT
hold full verification open, because the artifact is conforming: it made an
honest claim about content nobody can reconstruct, which is the outcome the
generator obligation asks for.

AN UNDECLARED NON-COMMIT VALUE IS REPORTED AS A DEFECT, naming the artifact, the
key and the value. Two things reach that branch and both are worth failing on: a
generator that invented a spelling nobody declared, and a value that is neither
a commit nor a sentinel — a truncated object name, a placeholder, an empty
string, a spelling drifted by one character from a declared member. The
verification cannot tell those apart and SHALL NOT try, because the remedy is
the same for all of them: declare the value or fix the generator. What it MUST
NOT do is guess that a value resembling a declared member was meant as that
member, since a near-miss spelling is precisely the condition under which every
consumer guarding on the exact string already fails.

THE DEFECT BRANCH SHALL NOT RED CONFORMING COMMITTED OUTPUT ON THE DAY IT IS
SWITCHED ON, and this is an obligation on the DECLARATION rather than a softening
of the check. Every non-commit spelling the corpus already carries under a
declared pin key SHALL be resolved before the defect branch runs: declared as a
member where it names a real condition, or corrected at its generator where it
does not. A verification that launches by reporting a lane's own committed output
as a defect teaches its readers that the finding is noise, and the first thing a
reader does with a noisy finding is to stop reading it. This is a seeding
obligation, not an amnesty: nothing here excuses a spelling from being resolved,
and a spelling nobody resolves is a defect the moment the branch runs.

THE COMMIT-SHAPED PATH IS UNTOUCHED. A value that is a commit name is verified
for reachability exactly as the promoted requirement states, and this
requirement neither restates nor modifies it. Nothing here converts a
reachability answer into a vocabulary answer, or the reverse.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, and the enumeration and its numerals in
the "Deterministic check families" requirement are deliberately untouched and
unrestated. This is a classification inside a verification that already declines
a family for reasons its own requirement states, and a `MODIFIED` block over a
requirement every new family must restate in full is a hazard this capability
now carries a family to police.

#### Scenario: A declared sentinel stands in a pin key
- **WHEN** a swept artifact carries, under a declared pin key, a value that the shared sentinel vocabulary declares
- **THEN** the verification MUST report it as a legal non-pin, naming the artifact, the key and the condition the sentinel states
- **AND** it MUST NOT be reported as reachable, orphaned, lost or uncovered, and MUST NOT hold full verification open

#### Scenario: An undeclared non-commit value stands in a pin key
- **WHEN** a swept artifact carries, under a declared pin key, a value that is neither a commit name nor a declared sentinel
- **THEN** the verification MUST report it as a defect, naming the artifact, the key and the value
- **AND** it MUST NOT be skipped, guessed at, or matched to the nearest declared member

#### Scenario: The value is a commit name
- **WHEN** a swept artifact carries a commit name under a declared pin key
- **THEN** the reachability verification proceeds exactly as before, and this classification changes neither its ref set nor its verdicts
- **AND** no sentinel outcome is emitted for it

#### Scenario: A spelling the corpus already carries is not yet declared
- **WHEN** the defect branch is switched on while committed output of an existing generator carries a non-commit spelling the vocabulary does not yet declare
- **THEN** that spelling MUST first be resolved — declared where it names a real condition, or corrected at its generator where it does not — so the branch does not launch by reporting conforming committed output as a defect
- **AND** the seeding obligation MUST NOT be read as an amnesty: an unresolved spelling is a defect the moment the branch runs

#### Scenario: A sentinel appears under a key no declared member covers
- **WHEN** a sentinel-valued key is carried by an artifact that no declared class member covers
- **THEN** the uncovered-artifact report MUST still fire on the key, because a coverage gap in the declaration is a separate finding from the value's classification
- **AND** the two findings MUST be reported separately rather than one being allowed to mask the other

### Requirement: The sentinel vocabulary is declared beside the pin class, and the declaration is itself checked over the same inventory
The shared sentinel vocabulary SHALL be DECLARED rather than discovered, in the
same place and the same form as the declared pin class it qualifies, and the
declaration SHALL be checked against what the repository actually carries rather
than trusted.

A DECLARATION THAT NOTHING CHECKS IS A SECOND PLACE FOR DRIFT TO HIDE. This
capability already learned that lesson twice — the check-family enumeration is
derived from the registry rather than restated on trust, and the pin class is
compared against the committed corpus so a renamed key surfaces as an uncovered
site rather than as silence. A vocabulary of honest non-pins earns the same
treatment for the same reason: its whole purpose is that one condition has one
spelling everywhere, and a list nobody measures against the corpus stops being
true the first time a generator writes a value the list does not carry.

THE CHECK RUNS IN BOTH DIRECTIONS, and each direction catches a different
failure. Corpus against declaration: a non-commit value standing in a declared
pin key that the vocabulary does not declare is reported, which is the branch
that catches a new generator inventing a spelling. Declaration against corpus: a
declared member that no committed artifact carries and no generator emits is
reported too, because a vocabulary that accumulates entries nobody writes
becomes a place where a reader looks up a value and finds a plausible-sounding
condition that never applied. Reporting a stale member is not deleting it — a
condition can be declared before its generator lands, in the same way the pin
class declares members whose first committed instance has not arrived yet — but
the state MUST be visible rather than assumed.

THE INVENTORY THE CHECK RUNS OVER IS THE PIN CLASS'S OWN, STATED EXPLICITLY.
The scope is every artifact the declared pin class already sweeps, under every
key that class declares, in the serializations it already reads. It is NOT
widened to files the class excludes, and the declared exclusions keep their
stated reasons and their stated trades: prose quotes sentinels exactly as it
quotes commit names, so a governance document narrating a dirty-tree derivation
is not itself making one. Naming the scope as the class's own inventory is what
keeps the two declarations answering for the same corpus — a vocabulary checked
over a wider or narrower set than the pins it qualifies would report gaps that
the pin class does not have, and miss gaps that it does.

AN ABSENT PIN KEY IS RECOGNIZED BY THE DECLARATION AND IS NOT A MEMBER OF IT.
The declaration SHALL name absence as a legacy state of the corpus — an artifact
that carries no pin key at all where the class expects one — so the state is
visible to a reader rather than falling outside both the pin path and the
sentinel path. It MUST NOT be declared as a vocabulary member, and an absent key
MUST NOT be filled in with a sentinel after the fact, because a sentinel asserts
which condition applied and absence records no condition at all. The two are
therefore reported differently and neither is converted into the other: a
recognized legacy absence is reported once and repaired never, where an
undeclared spelling is a defect with a remedy.

THE DECLARATION STATES A CONDITION PER MEMBER, and a member without one is
itself a defect. A sentinel whose meaning is not written down is a magic string,
and a reader who meets it in an artifact learns only that somebody chose not to
write a commit. Every member SHALL name the condition it stands for and whether
it is canonical for new output or a legacy spelling retained for committed
state.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, for the reasons the verification that
carries it already states, and the family enumeration and its numerals are
untouched and unrestated.

#### Scenario: A generator writes a spelling the vocabulary does not declare
- **WHEN** committed state carries a non-commit value under a declared pin key and the vocabulary declares no such member
- **THEN** the check MUST report it, naming the artifact, the key and the value, so the spelling is declared or the generator corrected
- **AND** the report MUST NOT be satisfied by the value being plainly readable to a human

#### Scenario: A declared member nothing carries
- **WHEN** the vocabulary declares a member that no committed artifact carries and no generator emits
- **THEN** the check MUST report the member as unused, so the declaration cannot silently accumulate conditions that never applied
- **AND** the report MUST NOT be treated as an instruction to delete a member whose generator has not landed yet

#### Scenario: A member is declared without its condition
- **WHEN** a vocabulary member is declared without stating the condition it stands for, or without stating whether it is canonical or legacy
- **THEN** the declaration MUST be reported as incomplete
- **AND** the member MUST NOT be accepted on the strength of its spelling being self-explanatory

#### Scenario: An artifact carries no pin key at all
- **WHEN** a swept artifact of a declared class member carries no pin key where the member declares one
- **THEN** the declaration MUST recognize the absence as a legacy state of the corpus and report it as such, distinctly from an undeclared spelling
- **AND** the absence MUST NOT be declared as a vocabulary member, nor filled in with a sentinel after the fact, because absence records no condition to assert

#### Scenario: The scope is questioned at the edge of the class
- **WHEN** a non-commit value stands under a pin-shaped key in a file the declared pin class excludes as a non-member
- **THEN** no sentinel finding is emitted for it, because the vocabulary check runs over the pin class's own inventory and inherits its declared exclusions with their stated reasons
- **AND** the exclusion MUST remain a declaration with a reason rather than becoming an unstated boundary of this check

### Requirement: A modified-block-currency finding its own class map cannot place is itself a finding
The modified-block-currency family SHALL emit ONE ADDITIONAL `warning` finding
per run for each DISTINCT SHAPE of rule text its own class map does not place,
naming how many of that run's findings carry that shape and, verbatim, the rule
text of the first of them in the family's own report order, and carrying that
first finding's repository and delta path. Where the map places every finding
the family emits, no such finding SHALL be emitted.

Two unplaced findings SHALL be treated as ONE SHAPE where their rule texts are
equal after EVERY FIELD THE ARM'S TEMPLATE INTERPOLATES has been replaced by a
fixed placeholder — quoted spans, runs of digits, repository-relative paths,
change identifiers, unit-kind lists, and any other value the arm substitutes
into its fixed prose — so that one shape is one template and one remedy.

The family SHALL derive that mask from its own arm templates: an arm's FIXED
PROSE is the shape and every value the arm interpolates into it is not, so the
rule cannot drift from the arms it describes.

The finding's action line SHALL name both remedies and where the first is
applied: "extend the class map in `scripts/doc_health/modified_block_currency.py`,
or fix the drifted rule text the finding names".

The finding SHALL itself be placed by the class map, in a FIFTH class of the
family's own registry carrying the `warning` band and that action line, so that
it is never counted by the residual it reports.

The pattern that places that class SHALL be anchored at the start of the rule
text, this finding carrying a quoted rule text that may itself begin in the shape
of an arm's.

The family's residual row SHALL continue to render whenever its count is
nonzero.

**THE FAMILY IS PRESENT IN `FAMILY_RESOLUTION`, AND THIS REQUIREMENT RECORDS
THAT ROW RATHER THAN CONTRADICTING IT.** `scripts/doc_health/families.py` reads
`"modified-block-currency": CONTESTED` as of `7f656980` (PR #529, 2026-08-31),
landed as the second half of `add-modified-block-currency-check` § 7.2's
reserved flip together with `_LAUNCH_SEVERITY`'s move to `error`. The absence
this requirement asserted was SPENT on that day, and it is superseded here so
that promoted canon states what the code does rather than the reverse — the
landing amended no specification, and this block is that catch-up rather than a
new decision. That table has NO PER-CLASS GRAIN: it is applied by finding FAMILY
alone, one string every arm and every class of this module shares, so neither
this requirement nor any other can hold one class of the family out of it, and
the finding this requirement defines is `contested` from that landing.

**THE PROTECTION THE ABSENCE BOUGHT IS NOT ENDANGERED BY A MAP EXTENSION, AND
NOTHING IS OWED FOR ONE.** What the absence was held for is that a finding
designed to stop being emitted must never become an uncited-resolution `error`
for having worked. Measured against the machinery rather than reasoned from the
shape of the rule, a map extension cannot raise that error at all:
`report.uncited_resolutions` keys a resolution on `(family, repository, path)` —
`Finding.match_key()`, which reads neither rule text nor severity — and this
finding is emitted with the FAMILY, REPOSITORY and PATH of the very finding it
names, `_drift_findings` in `scripts/doc_health/modified_block_currency.py`
constructing it from that finding's own `repo` and `path`. Extending the map
changes what `classify` PLACES and nothing that an arm EMITS, so the finding
this one named is still emitted, under that same key, on the next run. The key
therefore never leaves the current report, the rule's own `in current` test
skips it, and no error is raised. A protective clause that fires on no reachable
state protects nothing, and stating it would misdescribe the mechanism it claims
to guard.

**AND AN ACT THAT EXTENDS THE CLASS MAP SHALL NOT RECORD A DISPOSITION FOR THE
FINDING IT RECLASSIFIES.** Such an entry answers no disappearance; it causes
one. This family's dispositions are read BEFORE a block is resolved against
canon, at family, repository and path grain with an optional requirement
narrowing and NEVER at finding-class grain, so an entry recorded over the delta
path this finding carries suppresses the three comparison arms over that block —
including the finding that SURVIVED the extension, the one the map has merely
learned to name. **A MAP EXTENSION CLASSIFIES A DEFECT; IT DOES NOT FIX ONE.**
Recording a disposition for it would hide a live finding on every report until
the entry was retired — the exact failure the citation was imagined to prevent,
reached by the instrument imagined to prevent it.

**WHAT THE UNCITED-RESOLUTION RULE STILL REACHES IS UNCHANGED, AND IT IS NOT
RESTATED HERE.** Where some OTHER act makes this family emit nothing at all at a
`(repository, path)` the previous report carried — the block repaired, the delta
withdrawn — that IS a disappearance under the key the rule reads, and this
capability's promoted contested-finding rule applies to it on its own terms,
this family being present in `FAMILY_RESOLUTION`. This requirement adds nothing
to that rule and takes nothing from it. It records only that extending the class
map is not such an act, and that treating it as one is itself the defect.

This requirement adds no deterministic check family: the finding is emitted by
the modified-block-currency family under its own id, and the enumeration and its
numerals in the "Deterministic check families" requirement are untouched and
unrestated.

**Removed from canon by govern-sibling-added-modified-deltas (2026-08-31):** `` The family SHALL remain absent from `FAMILY_RESOLUTION`, so that a finding designed to stop being emitted as soon as the map is extended is never classified `contested` and its disappearance is never reported as an uncited resolution. ``; `` **AND** the disappearance MUST NOT be reported as an uncited resolution, the family being deliberately absent from `FAMILY_RESOLUTION` and its findings therefore never classified `contested` `` — the family joined the resolution table on 2026-08-31, at the landing PR #529 named above, so both units assert an absence that no longer holds; each is superseded in this same block, the sentence by the four paragraphs above and the bullet by the one that replaces it, and neither is dropped without replacement

#### Scenario: Every finding the family emits is placed by its map
- **WHEN** a run of the modified-block-currency family emits findings and the class map places every one of them
- **THEN** no additional finding MUST be emitted, the map and the arms agreeing being the state this requirement exists to leave alone
- **AND** the family's rendered class counts MUST still sum to the rows the report prints for it

#### Scenario: A rule text the class map does not place
- **WHEN** a run of the modified-block-currency family emits one or more findings whose rule text no pattern of its class map matches
- **THEN** the run MUST emit exactly one additional `warning` finding for each distinct shape among them, naming the number of that run's findings carrying that shape and, verbatim, the rule text of the first of them in the family's own report order
- **AND** each such finding MUST carry the repository and delta path of that first finding, and the action line this requirement states
- **AND** each such finding MUST itself be placed by the map into the fifth class, so that it is never counted by the residual it reports and the rendered counts still sum to the rows

#### Scenario: Two unplaced findings from one arm template
- **WHEN** two unplaced findings come from the SAME arm template and differ only in the values that template interpolates — a different quoted title, a different promoted-spec path, a different unit-kind list, different change identifiers
- **THEN** ONE additional finding MUST be emitted for both, naming the count two, one drifted arm template being one remedy
- **AND** two unplaced findings from DIFFERENT arm templates — differing in the fixed prose the mask leaves standing — MUST yield two additional findings, being two remedies

#### Scenario: The quoted rule text begins in the shape of an arm
- **WHEN** an unplaced rule text itself begins with the phrase an arm's rule texts begin with, and this finding quotes it
- **THEN** this finding MUST be placed in the fifth class and MUST NOT be placed under the class its quotation resembles
- **AND** the unplaced finding it names MUST still be counted by the residual row, the two being counted apart

#### Scenario: The warning is worked from the ranked plan
- **WHEN** a report is rendered for a run that emitted the additional finding
- **THEN** the finding MUST appear in the ranked plan as a ready-to-stage work item stating its severity, repository, path and action, on the same terms as every other finding
- **AND** the family's residual row MUST still render in the family's own report block, the row and the finding being two readings of one fact rather than alternatives

#### Scenario: The class map grows the pattern the drift named
- **WHEN** the class map is extended with a pattern that places the rule text the finding named, and the family is run again over the same tree
- **THEN** the additional finding MUST NOT be emitted, and the residual row MUST NOT render
- **AND** the disappearance MUST NOT be reported as an uncited resolution, and no citation and no disposition MUST be recorded for it — the finding this one named being still emitted at the same `(family, repository, path)` the uncited-resolution rule keys on, so the key never leaves the current report and the rule never fires

#### Scenario: The act that extends the class map records a disposition for the finding it reclassifies
- **WHEN** an act extends the class map so that a drifted rule text is placed, and that same act records an entry in `health/dispositions.yaml` naming this family, the repository and the delta path the additional finding carried
- **THEN** the entry MUST be refused, this requirement forbidding it: it answers no disappearance, the finding the additional one named still being emitted under the key the uncited-resolution rule reads
- **AND** the entry MUST be read as suppressing rather than resolving — dispositions of this family being read before a block resolves and carrying no finding-class grain, it silences the three comparison arms over that block, and with them the surviving finding the extension only classified, on every run until it is retired

#### Scenario: The family's resolution class is read from the table and not from this requirement
- **WHEN** a reader asks whether a finding of this class is classified `contested`
- **THEN** the answer MUST be read from `FAMILY_RESOLUTION`, which carries this family and has no per-class grain, and this requirement MUST NOT be read as holding this class out of it
- **AND** the row MUST be read as standing since `7f656980` (PR #529, 2026-08-31), the landing that added it without amending this specification, so that a reader of the code and a reader of canon are not told two different things

### Requirement: A pin site is built only from a value that is a whole object name
The pin verification SHALL create a derivation-pin site only where the matched
value is a WHOLE object name, and MUST NOT manufacture a pin from a prefix of a
longer hexadecimal run.

A PIN THE ARTIFACT DOES NOT CARRY IS THE ONE VALUE THIS VERIFICATION MUST NEVER
PRODUCE. Everything else the class reports is a reading of committed bytes: a
pin is reachable, orphaned, lost, uncovered, a legal non-pin or an undeclared
one, and in every case the value under judgment is the value the artifact
holds. A truncated prefix is not. It is a string the verification composed out
of the first forty characters of something longer, and every downstream verdict
about it is a verdict about a value nobody wrote — which is a worse failure than
any of the outcomes the class already names, because the reader cannot find the
subject of the finding by opening the file.

BOTH WAYS IT GOES WRONG ARE WORTH FAILING ON, and they fail in opposite
directions. The fabricated prefix is overwhelmingly likely to name no object at
all, so the run reports an ORPHANED PIN on an artifact whose recorded value is
intact — sending a reader to retention, to a superseding record, or to a
re-derivation, for a defect that does not exist. And it may instead COLLIDE: a
forty-character prefix that happens to name a real commit in this repository
reports as REACHABLE, and the verification then certifies a provenance claim it
never read. A check that can certify a claim it did not read is worse than a
check that abstains.

THE GUARD ALREADY EXISTS IN THE SAME MODULE AND WAS NOT CARRIED TO THE REGEXES
THAT BUILD SITES. The standalone-object-name scanner carries an explicit
hexadecimal boundary on both sides and a comment stating that a longer digest
would otherwise yield spurious pins. The obligation here is that EVERY
expression that builds a pin site carries the same boundary — the field forms,
the vocabulary sweep, and the prose members' own patterns alike. A guard stated
in one place and absent from the four that matter is not coverage; it is a
comment.

THE OBLIGATION IS ON THE VALUE, NOT ON A LIST OF LENGTHS. The rule is not "reject
sixty-four characters": it is that a value is a pin only if the WHOLE value is
an object name, so a forty-one-character run, a sixty-four-character digest and
a forty-hex token abutting further hexadecimal text are all refused by the same
rule rather than by an enumeration of the widths somebody thought of. And a
repository whose object names are a different width is accommodated by widening
what counts as an object name, never by loosening the boundary — the boundary is
what makes "whole" mean anything.

THE VALUE IS NOT DISCARDED, IT IS HANDED ON WHOLE. A value refused as a pin is
still a value standing under a declared pin key, and it therefore reaches the
non-commit classification exactly as any other non-commit value does, where the
promoted classification requirement already decides it — a legal non-pin where
the vocabulary declares it, a defect naming the artifact, the key and THE WHOLE
VALUE where it does not. Refusing to build the site is what makes that
classification the only reading of the value, rather than a second reading
racing a fabricated first one.

NOTHING ABOUT A CONFORMING PIN MOVES. A value that IS a whole object name builds
the same site it builds today, against the same declared class, the same key
set, the same serializations, the same ref set and the same verdicts. This
requirement changes what is REFUSED, and refuses nothing that was ever a pin.

THIS ADDS NO DETERMINISTIC CHECK FAMILY, for the reasons the verification that
carries it already states in its own promoted requirements, and the family
enumeration and its numerals are untouched and unrestated.

#### Scenario: A digest longer than an object name stands under a declared pin key
- **WHEN** a swept artifact carries, under a declared pin key, a hexadecimal value longer than a whole object name — a sixty-four-character digest, or any run of hexadecimal characters that does not end where an object name would
- **THEN** the verification MUST NOT build a pin site from any prefix of it, and MUST NOT report that prefix as reachable, orphaned, lost or retained
- **AND** the whole value MUST reach the non-commit classification unshortened, where an undeclared value is reported as a defect naming the artifact, the key and the value as written

#### Scenario: The fabricated prefix would have resolved
- **WHEN** the first forty characters of such a value happen to name an object this repository holds and a ref reaches
- **THEN** the verification MUST still refuse to build a site, because a coincidental resolution is not a reading of the artifact's claim
- **AND** it MUST NOT report the artifact's provenance claim as verified on the strength of an object the artifact does not name

#### Scenario: A whole object name is unaffected
- **WHEN** the value under a declared pin key is a whole object name — quoted or bare, in a mapping field, in compact serialization, or inside the sentence a prose class member declares its own pattern for
- **THEN** the site is built exactly as before, and the ref set consulted, the verdicts reached and the reported outcomes are unchanged
- **AND** no finding is introduced by this requirement for any value that was a pin before it

#### Scenario: The boundary is stated once and applied everywhere a site is built
- **WHEN** the module carries an expression that builds a pin site — a field form, a vocabulary sweep, or a class member's declared prose pattern
- **THEN** every such expression MUST carry the whole-object-name boundary, and a new one added later MUST carry it too
- **AND** a boundary present on the module's standalone scanner MUST NOT be read as covering the expressions that build sites, because the site builders are where a fabricated pin is produced

### Requirement: Release-tag publication
The release-tag-publication family SHALL report, for every repository in scope and for EVERY BUNDLE THAT REPOSITORY HAS CUT at or above the version where mandatory tag publication begins, whether that bundle has a published ANNOTATED tag, and whether that tag peels to a commit that declares the bundle.

EVERY CUT BUNDLE, NOT ONLY THE ONE CURRENTLY DECLARED — and this is the
difference between catching the recurrence and reading zero through it. A
bundle is legitimately silent while its declaring commit is the published tip.
Then the NEXT cut advances the manifest, and a family that read only the current
declaration would begin checking the new bundle and NEVER REVISIT the old one.
Run against the incident that motivated this family it would have reported
nothing at all: `contract-v2.3` untagged, `contract-v2.4` declared on top of it,
silence. The set of bundles a repository has cut SHALL be taken from its release
inventories, which are the machine-readable fact that a cut happened.

A SUPERSEDED BUNDLE IS NOT GRADED BY DISTANCE. The distance window exists for
the interval between declaring and tagging, and that interval ENDED for any
bundle the manifest has moved on from. An untagged superseded bundle is
therefore reported at `error` without grading, and its remedy is
retro-publication at the commit the policy's rule identifies — RETRO-PUBLISHED,
NOT RE-DATED, as the 2026-08-25 discharge did.

The obligation being checked belongs to `docs/contract-versioning-policy.md` —
"a bundle is not published until its tag exists", and "the tag SHALL point to
that realized commit". This requirement defines only how doc-health checks it,
in the same by-reference relationship `tag-hygiene` already has with
`document-lifecycle`'s marker grammar and `Release-inventory drift` has with
`release-surface-integrity`.

THE FAMILY SHALL BE DISTANCE-GRADED RATHER THAN IMMEDIATE, because the declaring
commit and the tag are two acts by two actors and the interval between them is
legitimate. A cut declares the bundle; the repository owner publishes the tag
afterwards. A family that fired the moment the manifest moved would redden every
correctly performed release, and a family nobody can leave green is a family
that gets configured away. Distance SHALL be measured in FIRST-PARENT COMMITS ON
PUBLISHED `main` since the earliest commit declaring the bundle, never in wall
time, because landings are what the policy's own retro-publication rule counts
and wall time punishes a quiet week.

THE THRESHOLD SHALL DEFAULT TO FIVE FIRST-PARENT LANDINGS, ruled by Brett Heap on
2026-08-31. It is a threshold default in the sense this capability already gives
that term, configurable in the same place the aging defaults are, and the ruled
number is what an unconfigured run uses. The calibration it answers to:
`contract-v2.3` sat untagged across six first-parent landings before a human
noticed it, so a threshold above five would have stayed silent through the
recurrence this family exists to catch.

THE TWO FAILURE STATES SHALL BE REPORTED IN DIFFERENT WORDS AND AT DIFFERENT
SEVERITIES. An ABSENT tag is an incomplete release — the common case, and the
one the window above exists to tolerate for a while. A tag that exists and peels
to a commit NOT declaring the bundle is a MISPLACED tag: it satisfies every
check that asks only whether a tag exists, it is what consumers will pin, and it
is worse than absence because it looks like completion. Reporting them alike
would let the common one hide the serious one.

THE FAMILY SHALL NOT FIRE BELOW THE ENFORCEMENT LINE. `contract-v1.0` through
`contract-v1.6` predate mandatory annotated tags and carry none by design, as
the changelog's own legacy baseline note records. A family that reported them
would emit seven permanent findings nobody may act on, which is how a report
teaches its readers to stop reading it.

A LIGHTWEIGHT TAG SHALL NOT SATISFY THE OBLIGATION. The policy requires an
ANNOTATED tag; a lightweight ref carries no tagger, no date and no message, and
accepting one would let the weaker object silently discharge the stronger
requirement.

The family SHALL be reported as skipped, never silently omitted, where a
repository declares no bundle at all, or where version control cannot answer —
an unavailable git dependency, tag refs that cannot be listed, or a declaring
commit that does not resolve. THE SKIP IS RESERVED FOR "THE QUESTION COULD NOT
BE ASKED": a declared bundle whose tag is simply absent is an ANSWER, and is
reported by the scenarios below rather than skipped.

THIS FAMILY DOES NOT PROVE THE TARGET IS THE EARLIEST DECLARING COMMIT, and the
residue is disclosed rather than hidden. The policy's target is "the EARLIEST
FIRST-PARENT COMMIT on published `main` that DECLARES the bundle and at which
`verify-commit` PASSES"; the second conjunct is a digest verification per
candidate and is out of scope here. A tag on a LATER declaring commit therefore
passes this family and remains a defect under the policy.

**AMENDED BY `declare-spent-bundle-state` (2026-09-02).** Every paragraph above
this note stands exactly as promoted; everything from here to the scenarios is
this change's addition, and among the scenarios exactly one `AND` bullet is
added, to *A bundle was cut, superseded, and never tagged*. Nothing else in this
requirement moves. **AND ONE PROMOTED PARAGRAPH IS QUALIFIED RATHER THAN
REPLACED, which is worth saying because its bytes are unchanged**: *A SUPERSEDED
BUNDLE IS NOT GRADED BY DISTANCE* still reads that an untagged superseded bundle
is *"reported at `error` without grading"*, and that remains exactly what such a
bundle reads as WHEREVER NO DECLARATION NAMES IT — which is every bundle in the
estate's history but one, and the default forever. The sentence is kept
byte-faithful rather than rewritten so that a reader arriving at it meets the
promoted rule and then its one exception, instead of a rewritten rule with no
trace of what it replaced.

A SUPERSEDED BUNDLE MAY BE DECLARED SPENT, AND A SPENT BUNDLE IS THE THIRD STATE
THIS FAMILY OTHERWISE LACKS. Between *published* and *owes a tag* sits a number
that was cut, was never publishable, and never will be. The action the
superseded finding prescribes — retro-publication at the commit the policy's
rule identifies — is UNPERFORMABLE for such a bundle, and a finding whose only
prescribed action cannot be taken by anyone is one a reader learns to skip,
which is how a report loses the readers the rest of it needs. The family SHALL
therefore recognize a SPENT state, and SHALL recognize it ONLY from an EXPLICIT
DECLARATION.

SILENCE IS NEVER A DECLARATION, AND THAT SENTENCE CARRIES THE WHOLE OF THIS
STATE'S FAIL-CLOSED CHARACTER. An untagged superseded bundle that no declaration
names SHALL be reported exactly as it is today, at `error` and in the same
words. A bundle MUST NOT become spent by being old, by being ignored, by being
inconvenient, or by any absence whatsoever. Every state below is entered by a
record that exists and is refused by a record that does not.

THREE OUTCOMES, NOT TWO, AND THE MIDDLE ONE IS NOT A REFUSAL — stated here
because a two-way reading of "accepted or refused" makes the ruled `warning`
band unreachable. A declaration is ACCEPTED (the `info`), REFUSED (an `error`,
and the superseded-and-never-published `error` stands alongside it because a bad
declaration must remove nothing), or PROVISIONAL: well formed in every element,
naming a LATER superseding bundle that is CUT but NOT YET PUBLISHED. A
PROVISIONAL declaration SHALL emit the `warning` and SHALL SUPPRESS the
superseded-and-never-published `error` for that bundle, reporting ONE finding
and not two. That is the ruled outcome — this case is a `warning` — and a
conforming family reporting both would be contradicting it. **NOTHING IS LOST BY
THE SUPPRESSION, AND THIS IS WHY THE BAND IS SAFE**: the successor is the bundle
the manifest now declares, so it is graded by the distance arm ON ITS OWN
ACCOUNT — `warning` inside its window, `error` past the threshold — so the
obligation has MOVED ONTO THE SUCCESSOR rather than been discharged, which is
exactly what the successor guard is for. The provisional band is bounded by that
grading and not by this state's patience.

THE DECLARATION SHALL BE READ FROM `contracts/CHANGELOG.md` AT THE PUBLISHED
TIP, and from nowhere else. Three facts pick that document and no other. It is
ON THE RELEASE SURFACE a consumer already pins — it is a member of every release
digest inventory — so the record travels with the bundle rather than sitting
beside it. It is one of the THREE EDITORIAL MEMBERS the versioning policy allows
to move between cuts, so a disposition can be recorded when the fact arises
rather than waiting for a bundle that may never be cut; every other release
member is one whose between-cuts edit is itself a defect. And the changelog is
ALREADY where this estate records supersessions — `contract-v2.3`'s disposition
sits in `contract-v2.4`'s entry and `contract-v2.6`'s sits in `contract-v3.0`'s
— so the state is given a machine-readable handle on a record the estate keeps
anyway, rather than a second record beside it.

THE DECLARATION SHALL NOT BE READ FROM `health/dispositions.yaml`, and the
reason is mechanical rather than a preference. That file SUPPRESSES findings
keyed by `(family, repo, path)`, and every finding this family raised BEFORE
this amendment lands on `contracts/manifest.yaml` — so a single entry on that
path would suppress EVERY absent-tag, misplaced-tag and lightweight-ref finding
this family could ever raise about that repository, including the next genuinely
abandoned bundle. That coarseness is the mechanism's, not this state's: it has
no way to name one bundle. (The findings THIS amendment adds land on per-bundle
inventories for the very same reason — see the path rule below — which is the
distinction the dispositions file cannot draw.) It lives at the AGGREGATION
ROOT, so it is
unreachable both by a consumer reading a pinned policy document and by a
`--single-repo` run, which is the scope this family's own self-gate uses. A
mechanism that cannot name one bundle, cannot be read by the consumer the
obligation protects, and is invisible to the gate that measures it is not the
smaller mechanism; it is the one that fails open.

THE DECLARING ACT IS THE SUPERSEDING BUNDLE'S OWN CHANGELOG ENTRY, and that
answers who may declare a bundle spent. A declaration SHALL be accepted only
where the changelog entry containing it is the entry of the bundle it names as
the superseding one. A bundle therefore cannot declare ITSELF spent, and no
document outside a release entry can declare anything spent: the act costs a
version number, is performed by a release cut, and is recorded on the surface
consumers pin. A family that accepted a repository's declaration about its own
number would be accepting *"I decided not to tag it"*, which is the state this
family exists to refuse.

THE DECLARATION SHALL TAKE ONE RESERVED SINGLE-LINE FORM, and the form is stated
here rather than left to an implementation because a deterministic family reading
free prose is a family whose behaviour nobody can predict from its
specification:

    **SPENT BUNDLE:** `<bundle>` — SUPERSEDED BY `<superseding bundle>` — CAUSE: <text> — RULED BY <author>, <YYYY-MM-DD> — MEASUREMENT: <citation>

That is the literal line, shown as a code block so that no delimiter of the
surrounding prose can be misread as part of it — a form quoted inside backticks
invites a reader to copy the backticks, which is a defect a specification can
avoid by not introducing it. The opener `**SPENT BUNDLE:**` is RESERVED: no other text in
`contracts/CHANGELOG.md` may begin a line with it, and a line beginning with it
that does not complete the form is a malformed declaration rather than prose to
be ignored. The form is a HANDLE ON THE RECORD AND NOT A SECOND RECORD — it is
written INSIDE the human disposition subsection the cut writes anyway, in the
pattern `document-lifecycle`'s reserved `Modified over` marker already sets, so
there is one record and one place it can be read from.

FOUR ELEMENTS ARE OWED AND EACH SHALL BE CHECKED FOR PRESENCE: the SUPERSEDING
BUNDLE, the CAUSE, the RULING that disposed it — its author and its date — and
the MEASUREMENT OF RECORD the cause cites. The family SHALL verify that each is
present and non-empty and SHALL verify the superseding bundle mechanically; it
does NOT and CANNOT verify that a cited ruling was really made, and that residue
is disclosed rather than hidden. What makes the state safe is not the family's
belief in the citation but the successor guard below, which cannot be satisfied
by writing anything.

THE SUCCESSOR GUARD IS WHAT MAKES THE STATE UNABUSABLE — RULED BY BRETT HEAP,
2026-09-02 — and it SHALL hold in both directions. A SPENT declaration SHALL be
quiet only where the superseding bundle it names has itself been CUT and has
itself been PUBLISHED: an annotated tag peeling to a commit that declares it. So
the only way to retire a number is to publish its replacement's tag, which is
the very act this family exists to compel; a repository that walks away from a
bundle by declaring it spent has merely moved the obligation onto the successor,
where the same check meets it again. Where the successor is cut but not yet
published the supersession is UNPROVEN and the family SHALL `warning` rather
than accept it; where the successor was never cut at all the declaration points
at nothing and the family SHALL `error`.

AND THE SUCCESSOR SHALL BE LATER THAN THE BUNDLE IT SUPERSEDES, which is the
half a "cut and published" test does not cover and which cannot be omitted. The
superseding bundle's `(major, minor)` SHALL be STRICTLY GREATER than the spent
bundle's, and a declaration naming a successor that is not SHALL be an `error`
that accepts nothing. Without it, the guard above is satisfiable by an ALREADY
PUBLISHED EARLIER BUNDLE — a declaration for `contract-v2.6` written into
`contract-v2.5`'s entry and naming `contract-v2.5`, which was cut, is published,
and carries a valid tag — so an untagged bundle would go quiet with NO
replacement published at all and the guard would have been walked around
backwards rather than broken. Found by Codex on PR #578 against the ratified
shape of this delta, and repaired in it rather than filed. The residue is
disclosed: version ordering is the CHEAP conjunct, and this family does not
prove that the successor actually CARRIES what the spent bundle was to have
carried. That claim lives in the declaration's CAUSE and MEASUREMENT, which are
read for presence and not for truth — the same disclosure this requirement
already makes about the earliest-declaring-commit conjunct.

A CORRECTLY DECLARED SPENT BUNDLE IS RECORDED, NOT SILENT — RULED BY BRETT HEAP,
2026-09-02, on an alternative that was put to him and declined. The family SHALL
emit exactly one `info` for it, naming the spent bundle, the bundle that
superseded it, and where the record is. It is recorded because a reader who
finds a release inventory with no matching tag is owed the answer in the report
rather than only in a changelog they may not read.

AND THE FINDING SHALL LAND ON THAT BUNDLE'S OWN RELEASE INVENTORY —
`contracts/releases/<bundle>.digests.yaml` — NOT on the manifest and NOT on the
changelog, because THE PATH IS THE FINDING'S IDENTITY. A finding's identity in
this capability is `(family, repository, path)`; every other finding of this
family lands on `contracts/manifest.yaml`, so a spent state landed there would
share an identity with every one of them and its disappearance would be masked
by any surviving sibling. The changelog is no better: two bundles legitimately
declared spent would share THAT path too, and removing one declaration while the
other stood would leave the shared identity present and the removal unreported.
The per-bundle inventory is the one path that is unique to the bundle BY
CONSTRUCTION — it is the artifact whose existence made the bundle enumerable in
the first place. Found by Codex on PR #578 against a `contracts/CHANGELOG.md`
path, and repaired rather than filed. The `info` SHALL be classed `contested`,
so that a spent state which stops being reported without a cited change is
re-raised: the way to make it stop is to delete that inventory or that
declaration, and *"never edit the manifest, the changelog or the inventory to
match the absence"* is the sentence this family already prescribes. Every OTHER
finding this state introduces SHALL land on the same per-bundle inventory, with
ONE exception that has no bundle to land on: a declaration naming a bundle this
repository never cut at all disposes nothing and SHALL be reported at `warning`
on `contracts/CHANGELOG.md`, because a mistyped bundle name leaves the real
bundle undeclared and still reported, and an orphan record that looks like a
disposition is worth a reader's attention.

The `info` MUST NOT be read as the tag obligation having been MET. It was not
met; it was EXTINGUISHED, by an owner act, at the cost of a version number, and
the record says which.

THE SPENT STATE REACHES THE ABSENT-TAG ARM AND NOTHING ELSE. It SHALL NOT quiet
a MISPLACED tag, SHALL NOT quiet a LIGHTWEIGHT ref, SHALL NOT quiet the
distance-graded findings on the bundle the manifest currently declares, and
SHALL NOT be accepted for that bundle at all. The state answers *"this number
will never be published"*; it does not answer *"whatever ref exists under this
name is acceptable"*, and a tag that exists and points wrongly is the condition
this family already calls worse than absence.

THE STATE SHALL NOT BE READ BACKWARDS. The five bundles the versioning policy
records under § *Untagged Bundles After Enforcement Began* are NOT retrofitted:
all five were publishable, all five were published, and all five carry annotated
tags on declaring commits, so none of them reaches this arm at all. Neither does
any bundle below the enforcement line. `contract-v2.6` is the first bundle of
this kind in the estate's history, and a state introduced for one instance must
not acquire a second by being applied to cases that were only late.

**AMENDED BY `add-release-tag-gate` (2026-09-04).** Every paragraph above this
note stands exactly as promoted and exactly as `declare-spent-bundle-state` left
it; everything from here to the scenarios is this change's addition, and SIX
scenarios are added after the ones above. Nothing else in this requirement
moves: no severity changes, no arm is removed, no threshold moves, no path
moves, and what the family READS over a tree is not altered by one line. **THIS
BLOCK DROPS NO UNIT OF CANON** — it restates the requirement in full and adds to
it — so no `Removed from canon by` and no `Merged into` marker is owed.

THE CONDITION SHALL BE REPORTED NIGHTLY AND ENFORCED AT THE CUT, AND THOSE ARE
TWO MOMENTS OF ONE OBLIGATION RATHER THAN TWO OBLIGATIONS. The family above is
the REPORT: it runs in the nightly doc-health lane over published `main`, at the
severities this requirement already sets, and a cut landed without its tag stays
visible there however it landed, including on an administrative bypass. The
ENFORCEMENT is a required status check on the pull request that changes the
release surface, and it asks the SAME FAMILY the SAME QUESTION about a different
tree. One family, one definition of "published", two moments — never a second
implementation, a second severity ladder, or a second notion of when a tag
counts.

THE ENFORCING MOMENT IS THE PULL REQUEST THAT TOUCHES THE RELEASE SURFACE, AND
NO OTHER PULL REQUEST. The release surface, for this purpose, is
`contracts/manifest.yaml` and the release inventories under
`contracts/releases/`. A pull request that changes neither SHALL be passed
without the family being consulted about it at all, and this is the point of the
arrangement rather than an optimisation: the tag is published by a second actor
AFTER the cut merges, so any enforcement that reached every pull request would
make one actor's pending act every other lane's merge blocker. **THAT IS NOT
HYPOTHETICAL AND THE MEASUREMENT IS WHY THIS PARAGRAPH EXISTS.** On 2026-09-03
`contract-v3.3` was declared at 22:27Z and tagged five and a half hours later,
and for that whole window every open pull request in the repository failed a
required check on that one fact.

THE CHECK SHALL BE REQUIRED AND SHALL THEREFORE REPORT ON EVERY PULL REQUEST,
deciding for itself rather than being filtered by path. A required status
context that does not report on some pull requests is expected forever and
blocks them, so the scope rule above SHALL be evaluated INSIDE the check and not
by the trigger that starts it.

THE BAR IS THE ONE THAT WAS ALREADY BEING ASSERTED, MOVED RATHER THAN WEAKENED:
no `error` and no `warning` from this family over the tree under judgment. A
`warning` refuses too. The distance window this requirement grants a fresh cut
is for LANDINGS THAT LEAVE THE RELEASE SURFACE ALONE; a pull request that
touches that surface again is asserting the surface is in order, and is answered
on that assertion.

THE BUNDLE THE PULL REQUEST ITSELF CUTS SHALL NOT BE REQUIRED TO CARRY A TAG,
AND THE OBLIGATION SHALL BE RECORDED INSTEAD. The tag cannot exist yet: under
the versioning policy's realization order the reviewed commit lands first and
the annotated tag is published afterwards at the commit that landed. A check
demanding it before the merge would be unsatisfiable by construction, and an
unsatisfiable gate is one that gets configured away. No new rule is needed for
this, which is the load-bearing part: the bundle a cutting pull request declares
has its declaring commit AS THE TIP of the tree under judgment, so the distance
arm above already emits nothing — the scenario *The declaring commit is still
the published tip* answers it, and it answers it in the same words for a merge
tree as for published `main`. WHAT THE CHECK ADDS IS THAT THE SILENCE IS
RECORDED RATHER THAN PASSED OVER: the outstanding tag SHALL be named in the
check's own report, so that a reader of the passing check is told what is still
owed and by whom.

WHERE THE QUESTION CANNOT BE ASKED, THE CHECK SHALL FAIL CLOSED, AND THIS IS
WHERE IT DIVERGES FROM THE NIGHTLY ON PURPOSE. The family reports a SKIP when
version control cannot answer, and the nightly is right to carry that skip as an
`info`: it reads an environment it does not control and a skip there is the
honest answer. The check is the ENFORCING moment for a tree that is about to
become the published one, so an unasked question SHALL NOT be a pass.

THE CONDITION SHALL NOT ALSO BE PINNED AS A ZERO-FINDINGS ASSERTION OVER THIS
REPOSITORY IN ITS OWN TEST SUITE, and the prohibition is deliberate rather than
incidental. A test asserting that the repository currently reads zero findings
of this family is a pin on a fact that a legitimate, in-progress release makes
false, held inside a suite that every pull request must pass — so it converts
one actor's pending act into every lane's failure, which is the defect this
amendment removes and which it MUST NOT be able to re-acquire by having the
assertion written back beside the moved one. **WHAT IS KEPT IS THE POSITIVE
CONTROL.** A probe that only ever reads zero cannot be told apart from a reader
that answers nothing, so the suite SHALL go on demonstrating, over a tree
constructed to be untagged, that this family can fire.

**AMENDED BY `amend-published-tip-unreadable-scenario` (2026-09-05).** Every
paragraph above this note stands exactly as promoted, and the ONLY change this
block makes is to the scenario *The manifest cannot be read at the published
tip*: its `WHEN` bullet is replaced and two `AND` bullets are added. No other
scenario moves, no severity changes, no arm is removed, no threshold moves, and
what the family READS over a tree is not altered by one line — this is CANON
CATCHING UP WITH THE CHECKER, not a change to the checker.

THE FAMILY SHALL NOT NAME A CAUSE IT HAS NOT ESTABLISHED. A per-path answer of
nothing carries two facts at once — an unfetched commit, and a commit this
checkout holds that simply has no manifest — and the promoted wording named the
first as the commonest without the family being able to tell them apart. It can
now: it asks whether the commit is present and attempts one bounded fetch where
it is not, and reports each fact in its own words. **THE MEASUREMENT THAT
SETTLED WHICH IS COMMONER RAN THE OTHER WAY** — on the aggregation nightly the
commit WAS fetched, the workflow's own fetch step having put all ten published
tips in the store, and nine of the ten governed repositories simply carry no
`contracts/manifest.yaml` at all (openxFactory #612, remedied by #646). A
parenthetical that misnames the common case sends every reader of the report to
look for a fetch defect that is not there, which is the cost this amendment
removes.

**Removed from canon by amend-published-tip-unreadable-scenario (2026-09-05):**
``**WHEN** the blob read for the manifest at the published tip answers nothing — the commonest cause being a checkout that has not fetched that commit`` — the
clause after the dash asserts which cause is commonest, and the measurement
above shows it is the other one; the unit is REPLACED rather than deleted, by
the `WHEN` that names both facts and the `AND` that requires the family to
establish which holds before it speaks. Nothing else in this requirement is
dropped.

**AMENDED BY `amend-unreadable-read-sibling-scenarios` (2026-09-05).** Every
paragraph and every scenario above this note stands exactly as promoted —
including the note and the marker `amend-published-tip-unreadable-scenario` left
here, which promote with the requirement and are carried, not restated — and the
ONLY change this block makes is to the scenario *The changelog cannot be read at
the published tip*: its `WHEN` bullet is replaced and two `AND` bullets are
added. No other scenario moves, no severity changes, no arm is removed, no
threshold moves, and the set of trees over which this family speaks is not
altered by one line.

THE SAME RULE, AT THE SECOND READ THAT ANSWERS NOTHING. The clause the note
above retired for the manifest read had been written a second time, word for
word, over `contracts/CHANGELOG.md`; the amendment that removed one left the
other standing, and said so before it landed. **THE TWO READS ARE NOT IN THE
SAME POSITION, AND THAT DIFFERENCE IS WHAT THIS AMENDMENT RECORDS RATHER THAN
COPIES OVER.** The changelog read has no presence probe of its own — it INHERITS
the manifest read's, and it inherits it COMPLETELY, because the manifest is read
AT THE SAME COMMIT and must have answered before this arm can be reached. A blob
cannot be read out of a commit the checkout does not hold, so by the time the
changelog answers nothing the unfetched fact is not merely the rarer one: IT IS
EXCLUDED, and the only fact left standing is a tip this checkout HOLDS at which
no readable `contracts/CHANGELOG.md` blob came back. Naming the other one is
therefore not a bad guess but a statement the family's own position already
contradicts — so the skip SHALL say WHICH FACT HOLDS and SHALL state the
presence, rather than leave a reader of the report to infer a fetch defect that
cannot be there. **AND IT SHALL CLAIM NO MORE THAN THE PRESENCE GIVES IT.** A
held commit licenses "no readable blob came back at this path"; it does not
license "the commit carries no such file", because a store that holds the commit
AND its trees can still fail to produce the blob. Reporting that as a clean
absence would be the same conflation pointed in a third direction.

**Removed from canon by amend-unreadable-read-sibling-scenarios (2026-09-05):**
``**WHEN** the blob read for `contracts/CHANGELOG.md` at the published tip answers nothing — the commonest cause being a checkout that has not fetched that commit`` — the
clause after the dash names one of two causes as the commonest, and at this read
the one it names is the one that cannot hold at all; the unit is REPLACED rather
than deleted, by the `WHEN` that names both facts and the `AND` that requires
the family to have established which of them holds before it speaks. Nothing
else in this requirement is dropped.

**AMENDED BY `amend-absent-changelog-is-an-answer` (2026-09-07).** Every
paragraph and every scenario above this note stands exactly as promoted —
including every amendment note and every `Removed from canon by` marker left
here by `declare-spent-bundle-state`, `add-release-tag-gate`,
`amend-published-tip-unreadable-scenario` and
`amend-unreadable-read-sibling-scenarios`, which promote with the requirement
and are carried, not restated — and the ONLY change this block makes
is to the scenario *The changelog cannot be read at the published tip*: its
`THEN` bullet and the `AND` bullet below it are REPLACED. No scenario is added,
removed or retitled, no other scenario's bullets move, no threshold moves, no
path moves, and the severity of every finding this family already emits is
unchanged. **AND "ENTRY" AND "PATH" NAME ONE TREE FACT, NOT TWO.** The promoted
`WHEN` above says *"the tree carries no such entry"* and the bullets this block
adds say the tree carries, or carries no such, *path*; both name the SAME
question asked of the same tree object — whether the tree at that commit holds
anything at `contracts/CHANGELOG.md` — and the word varies only because each
sentence reads better with one of them. Nothing turns on the difference, and
no reader should hunt for a distinction that is not there.

A TIP THIS CHECKOUT HOLDS AT WHICH NO DOCUMENT CAME BACK IS AN ANSWER, AND AN
ANSWER IS GRADED. The note above settled which of the two facts holds at this
read and had the family SAY it; it left the read a SKIP, and a skip returns
before the bundles are looked at. So the state the amendment had just proved to
be an answer — the commit is held, no readable `contracts/CHANGELOG.md` blob is
reachable at it, therefore NO SPENT DECLARATION EXISTS — went on being answered
as a question the family could not ask, and the bundles in scope went ungraded.
**MEASURED ON A SHIM, AND THE MEASUREMENT IS WHY THIS AMENDMENT EXISTS**: the
same repository, differing in one blob, answered with ONE skip where the
changelog was absent and ONE `error` naming an untagged bundle where the
changelog was EMPTY. A document that is not there and a document that says
nothing carry the SAME fact about declarations, and the family owes them the
same grading. What the absent read owes ON TOP is the RECORD — the fact is not
dropped when the skip goes, it is reported beside the grading at `info`, on
`contracts/CHANGELOG.md`, in the words the note above ratified and claiming no
more than the presence gives them.

**AND THE SKIP IS KEPT WHEREVER THE DOCUMENT'S OWN ABSENCE IS NOT ESTABLISHED.**
Where the commit is not held, the absence of a declaration is the absence of a
LOOK: the skip stands, in the words it already had. **AND THE NOTE ABOVE NAMED A
THIRD STATE, WHICH GRADING MAKES LOAD-BEARING FOR THE FIRST TIME.** A store that
holds the commit AND its trees can still fail to produce the blob, so a held
commit licenses *"no readable blob came back at this path"* and never *"the
commit carries no such file"* — and GRADING is a claim about the file. Reading a
damaged object store as an absent document would answer an EXTINGUISHED
obligation with an `error` telling an operator to publish a tag that cannot be
published, which is the #338 conflation pointed in a third direction and made
expensive. So the family SHALL consult the TREE at that commit, which answers for
a path whose blob this store cannot produce, and SHALL grade only where the tree
carries no such path; where it carries the path, and where the listing itself
cannot be performed, the skip stands and says which. **THE PRESENCE PROBE THE
NOTE ABOVE REQUIRED IS WHAT MAKES ANY OF THIS AVAILABLE** — a family that could
not tell an unfetched commit from a held one could not safely grade either.

**Removed from canon by amend-absent-changelog-is-an-answer (2026-09-07):**
``**THEN** the family MUST report a skip naming that read, and MUST NOT treat the absence of a declaration it could not look for as the absence of a declaration`` — a
skip is what this bullet requires and a skip returns before the bundles in scope
are graded, so at a HELD tip it made a fact the family had established suppress
the findings an empty document receives; the unit is REPLACED rather than
deleted, by a bullet that keeps the unfetched skip word for word and adds what a
held tip is owed instead. Nothing else in this requirement is dropped.

**Removed from canon by amend-absent-changelog-is-an-answer (2026-09-07):**
``**AND** where the commit IS held, the skip MUST SAY THAT and MUST state the presence — naming the held commit and the read that returned nothing at it, and NOT asserting a file absence the held commit does not establish — because a tip this checkout holds is an ANSWER rather than a read that failed, and reporting it in the unfetched case's words sends a reader to look for a fetch defect that does not exist`` — it
constrains the wording of a skip the ESTABLISHED-ABSENCE case no longer emits,
so leaving it standing would require a report this family has stopped making at
that read; the unit is REPLACED rather than deleted, by a bullet that carries its
narrowing verbatim — the presence stated, the file absence not asserted — onto
the record that takes the skip's place, and by a THEN that carries the same
narrowing onto the two skips a held tip still emits. Nothing else in this
requirement is dropped.

#### Scenario: The declaring commit is still the published tip
- **WHEN** a repository declares a bundle at or above the enforcement line, that bundle has no published annotated tag, and the earliest commit declaring it is still the tip of published `main`
- **THEN** the family MUST emit no finding, because the cut has only just landed and the owner's tag act legitimately follows it
- **AND** the family MUST NOT record this as a pass that discharges the obligation, which remains owed

#### Scenario: Landings have accumulated on an untagged declared bundle
- **WHEN** the bundle has no published annotated tag and further first-parent commits have landed on published `main` above the earliest commit declaring it, up to and including the configured threshold
- **THEN** the family MUST emit a `warning` naming the bundle, the declaring commit, and how many first-parent landings have accumulated
- **AND** the action MUST name publishing the annotated tag at the commit the policy's rule identifies, never editing the manifest, the changelog or the inventory to match the absence

#### Scenario: An untagged declared bundle passes the threshold
- **WHEN** the accumulated first-parent landings exceed the configured threshold
- **THEN** the family MUST emit an `error`, because a bundle being consumed while unpublished is the state the policy calls a breach rather than an exception
- **AND** the finding MUST say that the bundle is NOT PUBLISHED in the policy's own terms, so no reader infers from its presence in the manifest that it was released

#### Scenario: The declared bundle carries an annotated tag on a declaring commit
- **WHEN** the bundle has a published annotated tag and that tag peels to a commit whose manifest declares that same bundle
- **THEN** the family MUST emit no finding

#### Scenario: A tag exists but peels to a commit that does not declare the bundle
- **WHEN** the bundle has a published annotated tag and the commit it peels to does not declare that bundle
- **THEN** the family MUST emit an `error` in DIFFERENT WORDS from the absent-tag findings, naming it a MISPLACED tag and naming both the commit it peels to and the bundle that commit actually declares, if any
- **AND** this MUST NOT be graded by distance, because a misplaced tag is not a release in progress and no interval makes it correct

#### Scenario: The published tag is lightweight rather than annotated
- **WHEN** a ref of the bundle's tag name exists but is not an annotated tag object
- **THEN** the family MUST emit an `error` naming the ref as lightweight, never treat it as satisfying the obligation, and never report it in the absent-tag words

#### Scenario: A bundle below the enforcement line
- **WHEN** the declared bundle is below the version at which mandatory tag publication begins
- **THEN** the family MUST emit no finding, and MUST NOT report the legacy sequence's untagged bundles at any severity

#### Scenario: A bundle was cut, superseded, and never tagged
- **WHEN** a repository has a release inventory for a bundle at or above the enforcement line, that bundle has no published annotated tag, and the manifest now declares a different bundle
- **THEN** the family MUST emit an `error` naming the superseded bundle and the bundle that replaced it, and MUST NOT grade it by distance — the window it would be graded against closed when the next cut replaced it
- **AND** the action MUST name retro-publication at the commit the policy's rule identifies, never a re-dating and never an edit to the inventory
- **AND** this MUST hold wherever no accepted SPENT declaration names that bundle — silence, an absent changelog record, and a REFUSED declaration all leave this scenario in force, while a PROVISIONAL one (well formed, its later successor cut but not yet published) SUPPRESSES it in favour of its own `warning`, the successor being graded on its own account

#### Scenario: A superseded bundle is declared SPENT and its successor is published
- **WHEN** a bundle has a release inventory, has no published annotated tag, the manifest has moved on from it, `contracts/CHANGELOG.md` at the published tip carries exactly one SPENT declaration naming it — carrying the superseding bundle, the cause, the ruling's author and date, and the measurement of record — inside the changelog entry of that superseding bundle, and that superseding bundle has itself a published annotated tag peeling to a commit that declares it
- **AND** that superseding bundle's version is STRICTLY GREATER than the spent bundle's
- **THEN** the family MUST NOT emit the superseded-and-never-published `error`, and MUST instead emit exactly one `info` on `contracts/releases/<spent bundle>.digests.yaml` naming the spent bundle, the bundle that superseded it, and where the record is
- **AND** that `info` MUST be classed `contested`, so that its disappearance without a cited change is re-raised rather than read as a resolution — the state is permanent, and the only way it stops being reported is that the inventory or the declaration was removed
- **AND** the family MUST NOT record it as the tag obligation having been met, which it was not: it was extinguished by an owner act at the cost of a version number

#### Scenario: A SPENT declaration names a superseding bundle that is not itself published
- **WHEN** a SPENT declaration carries every element it owes and the superseding bundle it names has a release inventory but no published annotated tag
- **THEN** the family MUST emit a `warning` on `contracts/releases/<spent bundle>.digests.yaml` saying the supersession is UNPROVEN, because a bundle is not published until its tag exists and a successor that is not published cannot yet be shown to have carried anything forward
- **AND** the family MUST NOT emit the `info`, and MUST NOT ALSO emit the superseded-and-never-published `error` for that bundle — this state is PROVISIONAL rather than REFUSED, ONE finding is reported and not two, and reporting both would contradict the ruling that this case is a `warning`
- **AND** the family MUST NOT suppress the SUCCESSOR's own finding, which is raised on the successor's own account by the scenarios above and is what bounds this band: past the successor's threshold the estate carries an `error` again, on the bundle that owes the tag

#### Scenario: A SPENT declaration names a superseding bundle this repository never cut
- **WHEN** a SPENT declaration names as its superseding bundle a name for which the repository holds no release inventory
- **THEN** the family MUST emit an `error` on `contracts/releases/<spent bundle>.digests.yaml` saying the declaration names a bundle that was never cut, because retiring a number by pointing at one that does not exist is the abuse this state is most exposed to
- **AND** the superseded-and-never-published `error` on the spent bundle MUST also stand, so that a bad declaration removes nothing

#### Scenario: A SPENT declaration names a superseding bundle that is not later than the bundle it supersedes
- **WHEN** a SPENT declaration is well formed, and the superseding bundle it names is cut and carries a published annotated tag on a declaring commit, but its version is not STRICTLY GREATER than the spent bundle's — including the case of a declaration written into an earlier, already-published bundle's changelog entry and naming that earlier bundle
- **THEN** the family MUST emit an `error` and MUST accept nothing, because a tag that already existed before the spent bundle was cut is not a replacement for it, and a guard satisfied by an earlier release has been walked around backwards rather than met
- **AND** the superseded-and-never-published `error` on the spent bundle MUST also stand, so that no untagged bundle goes quiet without a LATER published one

#### Scenario: A SPENT declaration's SUBJECT is a bundle this repository never cut
- **WHEN** a SPENT declaration's SUBJECT — the bundle it declares spent — is a name for which the repository holds no release inventory
- **THEN** the family MUST emit a `warning` on `contracts/CHANGELOG.md` saying the declaration disposes nothing, this being the one finding of this state that has no per-bundle inventory to land on
- **AND** it MUST NOT be read as disposing any other bundle, because a mistyped subject leaves the real bundle undeclared — and that bundle is still reported by the scenarios above, which is the fail-closed behaviour a typo must not be able to defeat

#### Scenario: A SPENT declaration omits an element it owes
- **WHEN** a declaration of the reserved form is present and any of the superseding bundle, the cause, the ruling's author, the ruling's date or the measurement of record is absent or empty
- **THEN** the family MUST emit an `error` on `contracts/releases/<spent bundle>.digests.yaml` naming which element is missing, and MUST NOT accept the declaration
- **AND** it MUST NOT report that omission in the absent-tag words, because a malformed declaration is worse than none: it looks like a record

#### Scenario: A SPENT declaration sits outside its superseding bundle's own changelog entry
- **WHEN** a well-formed SPENT declaration names a superseding bundle other than the one whose changelog entry contains it, including a declaration written inside the spent bundle's own entry
- **THEN** the family MUST emit an `error` and MUST NOT accept it, because the act that spends a number is the LATER CUT that allocates its replacement
- **AND** a bundle that could declare itself spent could decline to be published, which is the whole of what this family refuses

#### Scenario: More than one SPENT declaration names the same bundle
- **WHEN** `contracts/CHANGELOG.md` carries two or more SPENT declarations naming one bundle
- **THEN** the family MUST emit an `error` and MUST accept none of them, because two records of one disposition is how they come to disagree

#### Scenario: Two different bundles are each declared SPENT
- **WHEN** two bundles are each named by their own accepted SPENT declaration, under their own superseding bundles
- **THEN** the family MUST emit ONE `info` per spent bundle, each on that bundle's OWN release inventory path, so the two findings carry DIFFERENT identities
- **AND** removing either declaration MUST re-raise that bundle's state on its own — a shared path would leave the surviving finding holding the identity, and the removal would be reported by nothing

#### Scenario: A SPENT declaration names the bundle the manifest currently declares
- **WHEN** a SPENT declaration names the bundle `contracts/manifest.yaml` declares at the published tip
- **THEN** the family MUST emit an `error` and MUST NOT accept it, because a repository declaring a bundle it also calls spent asserts two incompatible things about one number
- **AND** that bundle MUST continue to be graded by distance exactly as it is today

#### Scenario: A SPENT declaration does not quiet a misplaced or lightweight tag
- **WHEN** a bundle named by an accepted SPENT declaration nevertheless carries a published ref of its own name — annotated but peeling to a commit that declares something else, or lightweight
- **THEN** the family MUST report that ref exactly as it does today, at `error` and in the MISPLACED or LIGHTWEIGHT words
- **AND** the SPENT state MUST reach the ABSENT-tag arm and nothing else

#### Scenario: The changelog cannot be read at the published tip
- **WHEN** the blob read for `contracts/CHANGELOG.md` at the published tip answers nothing — ONE ANSWER STANDING FOR TWO DIFFERENT FACTS: the commit is not in this checkout's object store, or the commit IS held and NO READABLE `contracts/CHANGELOG.md` BLOB IS REACHABLE AT IT, whether because the tree carries no such entry or because the blob object itself is not in this store
- **AND** the family has ESTABLISHED WHICH OF THE TWO HOLDS before choosing the words it reports — here by INHERITANCE and completely, the manifest read at that SAME COMMIT having already answered, which a commit this checkout does not hold cannot do — rather than naming a cause it did not check
- **THEN** the family MUST NOT treat the absence of a declaration it COULD NOT LOOK FOR as the absence of a declaration, and MUST report a skip naming that read WHEREVER THE DOCUMENT'S OWN ABSENCE HAS NOT BEEN ESTABLISHED — the commit not held, or held with the tree at it carrying the path and no readable blob coming back for it, or the tree not listable at all — and MUST treat a declaration it DID look for, at a commit this checkout holds whose tree carries no such path, as ABSENT: the bundles in scope MUST be graded with NO declarations, exactly as they are graded where the changelog reads and declares nothing, rather than skipped past
- **AND** where the document's absence IS established, the fact MUST STILL BE RECORDED and MUST state the presence — naming the held commit, the read that returned nothing at it, and the tree listing that establishes the absence, NEVER asserting a file absence on the held commit alone, which does not establish it — but it MUST be recorded BESIDE the grading rather than INSTEAD of it, and at `info`, because a tip this checkout holds whose tree carries no such document is an ANSWER rather than a read that failed, and a family that answered it with a skip would withhold from it the very findings the same tip carrying an empty changelog receives
- **AND** this is the same conflation the manifest read already guards one document over: not fetched is not an answer, in either direction

#### Scenario: The bundles untagged before this state existed are not retrofitted
- **WHEN** the family reads the five bundles the versioning policy records under § Untagged Bundles After Enforcement Began
- **THEN** no finding about any of them changes, because all five were publishable and all five were published: they carry annotated tags on declaring commits and never reach this arm
- **AND** the SPENT state MUST NOT be read backwards onto them, nor onto any bundle below the enforcement line

#### Scenario: The manifest cannot be read at the published tip
- **WHEN** the blob read for the manifest at the published tip answers nothing — ONE ANSWER STANDING FOR TWO DIFFERENT FACTS: the commit is not in this checkout's object store, or the commit IS held and carries no manifest at all
- **AND** the family has ESTABLISHED WHICH OF THE TWO HOLDS before choosing the words it reports — asking whether the commit is present, and attempting ONE BOUNDED FETCH of exactly that commit where it is not — rather than naming a cause it did not check
- **THEN** the family MUST report a skip saying so, and MUST NOT report it as the repository declaring no bundle
- **AND** where the commit IS present and simply carries no manifest, the skip MUST say THAT instead and MUST state the presence, because a tip this checkout holds is an ANSWER rather than a read that failed, and reporting it in the unfetched case's words sends a reader to look for a fetch defect that does not exist
- **AND** the same MUST hold for the commit a tag peels to, so a tag pointing at an unfetched commit is never reported as a tag pointing at a commit that declares nothing — this is the conflation `verify_tag` is filed for at #338, and a family that repeated it would be reporting the benign case in the serious case's words

#### Scenario: A repository declares no bundle
- **WHEN** a repository in scope carries no declared contract bundle at all
- **THEN** the family MUST report a skip naming the reason, never an empty pass

#### Scenario: Version control cannot answer
- **WHEN** the git dependency is unavailable, the repository's tag refs cannot be listed, or the declaring commit cannot be resolved
- **THEN** the family MUST report a skip naming which of those it was, never a finding
- **AND** the family MUST NOT read a tag's existence from a local ref alone where the published refs could not be consulted, because an unpushed local tag is not a published tag

#### Scenario: A pull request that touches no release surface path while a bundle is untagged
- **WHEN** a bundle is declared and has no published annotated tag, and a pull request changes neither `contracts/manifest.yaml` nor any file under `contracts/releases/`
- **THEN** the cut-time check MUST report success on that pull request WITHOUT consulting the family about its tree, so that a pending tag act is never another lane's merge blocker
- **AND** the nightly report MUST go on carrying that bundle at the severity the scenarios above give it, the relief being to the pull request and never to the record

#### Scenario: A cutting pull request while an earlier bundle is still untagged
- **WHEN** a pull request changes the release surface and the tree it would produce carries a bundle that this requirement's scenarios above report at `error` or at `warning`
- **THEN** the cut-time check MUST fail, naming the bundle and the finding in the family's own words
- **AND** the failure MUST be carried by that pull request alone, because it is the one asserting that the release surface is in order

#### Scenario: A cutting pull request declares a bundle that cannot be tagged yet
- **WHEN** a pull request changes the release surface, the bundle it declares has no published annotated tag, and the commit declaring it is the tip of the tree under judgment
- **THEN** the cut-time check MUST report success, because the tag is published after the merge at the commit that landed and demanding it earlier would be unsatisfiable
- **AND** the check MUST RECORD the outstanding tag in its own report, naming the bundle, so that success is not read as the obligation having been discharged
- **AND** the nightly report MUST continue to report that bundle until the tag exists

#### Scenario: A cutting pull request moves the declaration onto a bundle that is already published
- **WHEN** a pull request changes the release surface, the bundle it declares differs from the one its base declares, and that bundle already has a published tag peeling to a commit OTHER than the tree under judgment
- **THEN** the cut-time check MUST fail, because a version number that has been published is never reused and a defective release is corrected by a superseding one
- **AND** a tag peeling to the tree under judgment itself MUST NOT be refused this way, that being the obligation met early rather than a number cut twice
- **AND** this reaches ONLY the MOVED declaration: where the base already declares the same bundle the check MUST NOT be read as covering the case, which the realization order's rebase-and-recheck step answers instead

#### Scenario: The cut-time check cannot ask the family's question
- **WHEN** a pull request changes the release surface and the family reports a skip over the tree under judgment — the published refs unlistable, a required blob unreadable, or a declaring commit unresolvable
- **THEN** the cut-time check MUST fail closed, naming the reason, because it is the enforcing moment and an unasked question is not a pass
- **AND** the nightly report MUST still be permitted to carry that same skip as an `info` with its reason, the two moments answering the same skip differently on purpose

#### Scenario: The repository's own test suite is asked what it asserts about this family
- **WHEN** the repository's test suite is read for assertions about this family over the repository itself
- **THEN** it MUST carry no assertion that the repository currently reads zero findings of this family
- **AND** it MUST still carry a positive control demonstrating, over a tree constructed to be untagged, that the family fires

### Requirement: A MODIFIED block over an active sibling's addition is evaluated for its pairing, not for its carriage
The modified-block-currency family SHALL evaluate every `## MODIFIED
Requirements` block whose title resolves to an active change's ADDED or RENAMED
requirement — the shape its resolver returns as `pending` — and SHALL report the
pairing where it is undeclared, misdeclared, self-referential, or declared over
a basis that is not ratified without the disclosure `document-lifecycle`
requires of the marker, placing every such block in EXACTLY ONE of those states,
instead of dropping the block before its checks run.

**NOTHING IS COMPARED, AND THAT RULING STANDS.** Synthesising a basis from the
sibling's ADDED text was ruled against on 2026-08-27 for a reason that has not
changed: it would measure a block against text no promoted requirement carries.
The three comparison arms this family's currency requirement defines therefore
do NOT run against such a block, and this requirement adds no fourth comparison
arm — it adds a check on the PAIRING, whose inputs are the delta's own marker
and the set of active additions, and which compares no requirement text at all.
What was wrong was never that the arms declined; it was that the block was
dropped before anything at all looked at it, so the arms' silence read as
clearance when it was uncomparability.

**THE CHECK SHALL REPORT EXACTLY FOUR STATES, be silent on the fifth, and PLACE
EVERY BLOCK IN EXACTLY ONE OF THEM.** The five are MUTUALLY EXCLUSIVE BY
DEFINITION rather than by convention: they are examined IN THE ORDER WRITTEN
BELOW, a block placed in one state is NOT examined for any state below it, and
each state's antecedent below carries the exclusion that order performs. One
block therefore yields at most one finding of this class, and the words a reader
is given are never a choice between two true descriptions of one defect.

**THE CLASSIFICATION READS THE BLOCK'S WHOLE MARKER SET, AND THE COUNT IS THE
FIRST THING IT READS OF IT.** The family's derivation preserves EVERY paragraph
of marker form a block carries, in document order, so "the marker" is a SET and
not a singular the check may pick a member from. `document-lifecycle` bounds
that set — AT MOST ONE marker of the `Modified over` form per block, one pairing
and one declaration — and the states below are predicates over the WHOLE set
rather than over a chosen member of it. The checks therefore run in this order:
the carrier's own addition; then the COUNT of pairing markers; then, for the
single marker a lawful block carries, its basis, then its `by` identifier, THEN
ITS REASON, then its disclosure.
**A BLOCK IS DECLARED AND RESOLVING, OR UNDISCLOSED, ONLY WHERE
EXACTLY ONE PAIRING MARKER STANDS AND IT PASSES EVERY CHECK ABOVE IT; OTHERWISE
THE BLOCK IS PLACED BY THE FIRST CHECK IT FAILS, IN THAT ORDER.** Without the
count the promise this requirement makes is not kept by the states themselves: a
block carrying one valid marker and one naming a change that adds nothing
satisfies MISDECLARED and DECLARED AND RESOLVING at once, and which of the two a
run reported would be settled by which marker an implementation happened to look
at — the same false provenance accepted or refused by an accident of iteration
order.

- **SELF-REFERENTIAL** — the change that carries the block ADDS the block's
  capability and requirement title in its OWN `## ADDED Requirements` block.
  Reported, and a marker naming the change itself MUST NOT clear it. **THIS STATE
  IS EXAMINED FIRST AND EXCLUDES THE OTHER FOUR**, because it is a fact about the
  DELTA and not about the marker: a self-referential block carrying no marker is
  reported here and NOT as UNDECLARED, and one carrying any marker at all is
  reported here and NOT as MISDECLARED. Its remedy is to withdraw one of the two
  blocks, which no marker supplies, so a second finding over the same block would
  offer a remedy that does not reach the defect. **THE CARRIER'S OWN RENAME TO
  THE TITLE IS NOT THIS STATE**, for the reason the paragraph below states.
- **UNDECLARED** — the block is NOT self-referential and carries no marker of the
  reserved `Modified over` form. Reported.
- **MISDECLARED** — the block is NOT self-referential, carries at least one
  marker of the reserved form, and the declaration is wrong in one of the FOUR
  ways a declaration of this form can be wrong. **FIRST, THE COUNT**: the block
  carries MORE THAN ONE such marker, `document-lifecycle` admitting one pairing
  and one declaration, and this ground is read BEFORE the other three so that a
  block carrying a good marker and a bad one is placed by a fact about the BLOCK
  rather than by which marker was examined. Otherwise the block carries EXACTLY
  ONE, and that one is wrong in one of the remaining THREE ways: EITHER the change
  it names AS BASIS is not an active change
  OTHER THAN THE CARRIER that ADDS or RENAMES to the block's capability and
  requirement title — it names a change that neither adds nor renames to that
  title, or it names the carrying change itself — OR its `by` identifier is not
  the change that carries the block — OR it CARRIES NO REASON, the ` — <reason>`
  tail `document-lifecycle` requires being absent, or present and empty, so that
  the declaration the marker makes is one that capability calls incomplete.
  **AND THOSE THREE ARE READ IN THAT ORDER — basis, then `by`, then reason** —
  the single marker's own fields taken in the order its form writes them, so
  that one finding names the field a repair actually touches and a marker wrong
  in two of them is repaired from the front. Reported, and reported apart from UNDECLARED
  in the finding's own words, because a wrong basis and an absent one have
  different remedies. **THE BASIS GROUND IS THE EXACT NEGATION of the silent state's
  basis clause**, so that narrowing SELF-REFERENTIAL to the carrier's own addition
  leaves no block outside all five states: a marker naming the carrier as its own
  basis is reported here wherever the carrier is not reported self-referential.
  **THE REMEDY IS SINGULAR PER GROUND AND THE FINDING SHALL SAY
  WHICH GROUND IT NAMES**: more than one marker is repaired by withdrawing every
  declaration but the true one, a wrong basis by naming the change that
  actually adds the requirement or renames to its title, a wrong `by` by writing
  the carrying change's own
  identifier, an absent reason by writing the one the form requires,
  and one finding naming two of them without saying which would leave
  its reader to guess which paragraph, or which word of one paragraph, to
  change.
- **UNDISCLOSED** — the block is NOT self-referential and carries EXACTLY ONE
  marker of the reserved form, and that marker is not misdeclared — naming as
  basis an active change, other than this one, that
  does add or rename to the title, carrying as its `by` identifier the change
  that carries the block, AND CARRYING A REASON — that basis change is NOT
  `ratified`, and the marker's
  reason clause does not carry the disclosure `document-lifecycle` requires of it.
  Reported, and reported apart from the other three: here the pairing is declared
  and the basis is real, and what is missing is the reader's warning that the text
  the block rests on has been accepted by no authority. **THE REASON'S PRESENCE
  IS THIS STATE'S PRECONDITION AND NOT ONE OF ITS TESTS**: a marker with no
  reason clause is placed MISDECLARED one check earlier, so this state never
  reads an absent clause and never hands a reader "write the word `unratified`"
  as the remedy for a marker with no sentence to write it into.
- **DECLARED AND RESOLVING** — the block is NOT self-referential and carries
  EXACTLY ONE marker of the reserved form, and that marker is neither misdeclared
  nor undisclosed: it names as basis an active
  change other than this one that does add or rename to the title, its `by`
  identifier is the change that carries the block, it carries the nonempty
  reason `document-lifecycle`'s form requires, and either that basis is
  `ratified` or the marker discloses that it is not. NO FINDING IS EMITTED.
  A correctly declared pair is the state this check exists to produce, and a
  standing row for it would be a permanent advisory nobody should act on.

**A CHANGE'S OWN RENAME TO THE TITLE IS THE RENAME-AND-AMEND SHAPE, NOT A
DEFECT, AND PROMOTED CANON ALREADY DECIDES IT.** The resolution order this family
runs under examines the CARRYING change's own `## RENAMED Requirements` block
BEFORE the set of titles active changes add or rename to, and where that block
renames a promoted requirement TO this title the three comparison arms SHALL run
against canon under the OLD name, "a rename being a change of title rather than
of the content a block must carry"
(`openspec/specs/doc-health/spec.md:1568-1574`), with the promoted scenario "A
change renames a requirement and modifies it in one delta" resting a MUST on that
reading (`:1783-1786`). That PRECEDENCE IS PRESERVED AHEAD OF THE EXAMINATION
ABOVE and is widened, narrowed and reordered in no way: a rename-and-amend block
resolves against canon under the old name and never reaches this check at all.
Defining self-reference to reach a carrier's own RENAME would therefore do one of
two wrong things and never a right one — report the supported shape as a defect
where it reached, and stand as unreachable words where the precedence held. The
state is defined by the carrier's own ADDITION because the defect is TWO TEXTS
FOR ONE REQUIREMENT: an `## ADDED Requirements` block carries the requirement's
text and a `## RENAMED Requirements` block carries a pair of titles, so only the
first can be the same text written twice. Where a carrier's own rename names a
`FROM:` title the promoted specification does NOT carry, that precedence does not
resolve and the block reaches this check like any other, to be placed by its
marker or by the absence of one; there is no self-reference in it, a title pair
being no second text.

**THE `by` IDENTIFIER IS COMPARED TO THE CARRIER, AND THE OBLIGATION THAT
COMPARISON ENFORCES IS NOT THIS CAPABILITY'S TO STATE.** `document-lifecycle`
defines the form and requires its `by` identifier to BE the change whose delta
carries the block; this family reads that identifier and compares it, exactly as
it reads the basis and resolves it. Checking the basis ALONE would leave a marker
naming the right predecessor under an unrelated author in DECLARED AND RESOLVING,
so a block would promote carrying FALSE PROVENANCE — a declaration that sends its
next reader to a packet which declared nothing, which is worse than the
undeclared state it wears the appearance of curing. The comparison belongs INSIDE
MISDECLARED rather than in a state of its own: the defect is one wrong marker
with one paragraph to repair, on the same terms as a wrong basis, and the number
of states this check reports stays FOUR.

**THE REASON IS HARVESTED IN RECOGNITION AND JUDGED IN CLASSIFICATION, AND THE
TWO STAY APART FOR THE REASON THE `by` IDENTIFIER'S DO.** `document-lifecycle`
recognizes this form by its COMPLETE PREFIX and requires a nonempty ` — <reason>`
tail after it; this family reads that tail off every recognized marker and
reports its absence, exactly as it reads the `by` identifier and compares it.
Making the tail a condition of RECOGNITION instead would drop a prefix-only
paragraph to an ordinary body unit, so the block would be reported UNDECLARED
and its author told to add a marker the block already carries — the absent-marker
remedy for a defective declaration. Reading the absence NOWHERE is the hole this
ground closes: a paragraph carrying that complete prefix and its closing colon
and nothing after it names a basis, carries the carrier's own `by`, and would
otherwise satisfy every remaining check and reach DECLARED AND RESOLVING, so a
declaration the form itself calls incomplete would promote as a complete one and
the block would look declared to every later reader while declaring nothing. The
check belongs INSIDE MISDECLARED on the same terms as the `by` comparison — one
wrong marker with one paragraph to repair, one band and one action — so it adds
a GROUND and not a state, and the number of states this check reports stays
FOUR.

**AND IT IS READ BEFORE THE DISCLOSURE, which is not an ordering preference but
the condition of the disclosure being readable at all.** The disclosure is A
WORD LOOKED FOR IN THE REASON CLAUSE, so a marker with no reason clause offers
it nothing to look in. Taken the other way round, an unratified basis under a
prefix-only marker would be reported UNDISCLOSED and its author told to write
`unratified` into a sentence that does not exist, while the identical marker
over a RATIFIED basis would pass in silence — one defect named two ways at two
titles, and at one of the two not named at all. Reading BOTH would be worse
again: two findings and two remedies for one missing tail, which the
exactly-one-state rule forbids. So the reason is read FOURTH and the disclosure
FIFTH, and a prefix-only marker is MISDECLARED on the reason ground whatever its
basis's standing is.

**THE FOURTH STATE, UNDISCLOSED, EXISTS BECAUSE THE OBLIGATION WOULD OTHERWISE
BE DECLARED IN ONE CAPABILITY AND ENFORCED IN NONE.** `document-lifecycle` requires the reason
clause of a marker naming an unratified basis to disclose that standing; without
this state a marker that names its basis and says nothing about its standing
falls into DECLARED AND RESOLVING and passes in silence, and the disclosure
becomes a rule with no reader. The state is a NARROWING of the silent one and
not a fifth thing to look for: its antecedent is the silent state's antecedent
plus two conditions, so it reaches ONLY a block whose pairing is otherwise in
good order, and it restates no defect the other three already name.

**THE DISCLOSURE IS READ AS A WORD AND NOT AS A SENTENCE.** The form belongs to
`document-lifecycle`, which defines the marker and reserves the word; this
family only looks in the reason clause for it. A reason that carries the word
and denies it in the same breath is past what any deterministic family can read,
and it is a defect of authorship its reviewers catch — the alternative, a
checker arbitrating whether a sentence discloses, is the prose rule this marker
design refuses everywhere else.

**A DISCLOSURE THAT OUTLIVES THE STATUS IT DISCLOSED IS NOT REPORTED.** The
marker is a dated statement about the moment it was written, so a basis that
ratifies afterwards ends the question rather than turning the marker into a
defect. Nothing obliges the modifying change to go back and strike the word, and
a stale disclosure SHALL NOT be read as a wrong one.

**AND THE SILENCE THAT FOLLOWS A DISCLOSURE IS SILENCE ABOUT A DECLARATION,
NEVER CLEARANCE FOR AN ARCHIVE.** `release-realization` holds the modifying
change's archive while the title is unpromoted, and that hold keys on the
UNPROMOTED TITLE rather than on the basis's standing — so it stands over EVERY
pending pairing this check passes in silence, the ratified-basis ones included.
The hold is therefore NOT a defect of this class, and keeping the
disclosed-unratified case alone actionable would mis-locate it twice: it would
leave the identical hold unreported over a ratified basis, so that one run's
silence meant two different things at two titles; and it would stand a permanent
advisory over a block that is in good order, whose only remedy — the basis's own
archive — belongs to another packet and another owner, which is the state the
silent state exists to refuse. **THE HOLD IS ENFORCED WHERE THE ACT IT FORBIDS IS
TAKEN**, at the modifying change's archive gate, and what that gate reads is THIS
FAMILY'S OWN RESOLUTION OF THE BLOCK: while the block resolves `pending` the
title is unpromoted and the gate is shut; when the basis archives the block
resolves against canon, the three comparison arms run, and the gate opens with
them. That is a mechanical fact this family already computes for every block, so
the obligation is falsifiable without a finding standing over a correctly
declared pairing — the class's action line carries the same half of the remedy,
hold the archive until the declared change promotes, and the collision class
below is the evidence a breach leaves behind. No arm, no class and no read is
added by this paragraph; it records which instrument enforces what.

**THE FINDINGS SHALL FORM ONE NEW FINDING CLASS of this family**, reported
against the active delta's own path like every other finding this family emits,
carrying the `warning` band and one action line stating every half of the
remedy: declare the basis by ONE marker and no more than one, name the carrying
change itself as that marker's `by` identifier, give that marker the reason its
form requires, disclose in that reason clause
where that basis is not ratified, and hold the archive until the declared change
promotes.
The class SHALL be registered in the family's own class registry with its own
identifier and label, and SHALL be placed by the family's class map; a finding
this new class emits that the map does not place is an unplaced finding like any
other and is reported by the class that reports those.

**ITS RULE TEXT SHALL BE RENDERED FROM A REGISTERED ARM TEMPLATE.** The family
derives its unplaced-finding mask from its own arm templates, so a rule text
built any other way would have no shape the mask can compute and would be
reported as drift on every run that emitted one. One template SHALL carry all
four reported states — MISDECLARED's four grounds included, they being one state
with one action that differ only in the same interpolated clause — distinguished
by that clause, because one template is one shape is one map entry: the four
states share a band and an action and differ only in why.

**THE BAND IS `warning`, AND THE CLASS IS `contested` BY A ROW THIS REQUIREMENT
DOES NOT ADD AND CANNOT DECLINE.** The band is the measure-then-flip posture
every family of this group launched under, and here it is also the only honest
one: the population this check reports is the corpus's existing four pairs, none
of which was authored under a rule that existed, and raising the band is one
later decision taken by ruling AFTER that standing population is discharged. The
RESOLUTION CLASS is not a second half of that choice. `FAMILY_RESOLUTION` already
carries this family, its table has no per-class grain, and this requirement adds
no row and can remove none — so a finding of this class is `contested` from its
first emit. The promoted sentence that once denied that row is superseded by
this change's `## MODIFIED Requirements` block below, so the classification is
one thing canon and code now say together rather than two things they say
apart.

**THE CLASS'S REMEDY IS THE MARKER, AND THE TWO ROUTES TO IT ARE ORDERED RATHER
THAN OFFERED.** A `contested` finding that stops being emitted owes a citation
under this capability's own uncited-resolution rule, so a class whose whole
design is that its findings are discharged SHALL NOT be introduced against a
population it could have declared first.

1. **SEQUENCING IS THE ROUTE.** Where a repository carries undeclared pairings at
   the moment this check is introduced, they SHALL be declared by marker BEFORE
   the check runs there, so that it launches at a population of zero. A finding
   never emitted never vanishes and owes no citation, so this route ends the
   question rather than answering it.
2. **THE CITATION IS THE EXCEPTION, IT CARRIES ITS OWN RETIREMENT, AND IT IS
   AVAILABLE ONLY WHERE THE ORDERING ARM HAS NOTHING IT COULD EMIT.** Where
   that sequencing is not available — a pairing arising after the check is
   running, or a population in a repository the introducing measurement did not
   reach — the act that ADDS the marker SHALL record the citation that resolution
   requires, on the same terms as every other `contested` finding of this family.
   A disposition SHALL NOT be recorded IN PLACE OF a marker. **AND THIS ROUTE
   SHALL NOT BE TAKEN AT ALL while any active change OTHER THAN the one whose
   delta carries the block, and whose declared standing is `ratified`, carries a
   `## MODIFIED Requirements` block for the same capability and requirement
   title.** In that state SEQUENCING IS THE ONLY ROUTE: the marker is written and
   no entry is recorded, and where the marker cannot yet be written the finding
   stands until it can.

   **THE BOUND IS READ OFF THE MECHANISM RATHER THAN CHOSEN.** This family's
   two-writers ordering arm is armed BY COUNT — it takes the active MODIFIED
   blocks over one capability and requirement title, keeps those whose carrying
   change is `ratified`, and returns nothing whatever below TWO of them. It runs
   BEFORE any block of that group is resolved against canon, it emits one finding
   PER RATIFIED BLOCK against that block's own delta path, and its findings are
   then filtered through THE SAME family/repository/path disposition read,
   narrowed by THE SAME requirement title. An entry recorded to answer a pairing
   finding on a block therefore reaches the ordering finding over that same block
   wherever one is emitted — and the ordering defect is a SEPARATE defect with a
   SEPARATE remedy, which would stay hidden for as long as the entry stood.

   **SO THE SENTENCE THIS ROUTE ONCE RESTED ON IS MADE TRUE BY CONSTRUCTION
   RATHER THAN ASSERTED.** That a citation "suppresses nothing" is not a property
   of the citation — the entry carries no finding-class grain and silences
   whatever shares its key — it is a property of the STATE it is recorded in. The
   bound admits the entry only where the ordering arm has NO SUBJECT at that
   title, so there is nothing of that class for it to hide; the pairing finding it
   answers is already answered by the marker landed in the same act; and the three
   comparison arms do not run over a pending block. The route suppresses nothing
   because it exists only where there is nothing to suppress.

   **THE BOUND IS ONE CASE WIDER THAN THE ARM'S ARMING CONDITION, DELIBERATELY.**
   The arm needs TWO ratified writers and this refuses the route at ONE OTHER, so
   it also refuses where the carrier's own change is not ratified and exactly one
   other ratified writer stands — a state in which the arm emits nothing today.
   The width is the point: standing is one header edit on the carrier's own
   proposal, and an entry recorded under the reading "my own change is not
   ratified, so the arm is silent" would begin suppressing the ordering class the
   moment that change was ratified, with no act anywhere to notice. A bound a
   later edit can invalidate while the entry stands is not a bound. For the same
   reason the bound reads the arm's SUBJECT and not its current emit: two ratified
   writers with exactly one declaration between them are the ordered pair the arm
   passes in silence, and one proposal edit withdrawing that declaration turns the
   silence into a finding the standing entry would then hide.

   **AND THE BOUND'S POPULATION IS ZERO ON THE AUTHORING TREE.** Measured with
   the family's own reader over this branch, this packet's own two MODIFIED
   blocks included: no capability-and-requirement title carries more than ONE
   active MODIFIED block at all, so none carries two ratified writers and the
   route is refused nowhere. Like the collision class, the bound costs nothing to
   land and is in place before its first instance rather than after it.

**A DISPOSITION RECORDED FOR A PAIRING SHALL BE SCOPED SO THAT IT CANNOT OUTLIVE
THE PAIRING IT ANSWERS, and the scope is dictated by the mechanism rather than
chosen.** This family reads its dispositions at FAMILY, REPOSITORY and PATH grain
with an optional REQUIREMENT narrowing, NEVER at finding-class grain, and it
reads them BEFORE a block is resolved against canon AND before the two-writers
ordering arm's findings are collected. An entry recorded to answer
a finding of this class therefore suppresses the three comparison arms over that
block as well — and goes on suppressing them after the declared basis archives
and the block becomes comparable, which is the one moment those arms exist for —
and, where the ordering arm has a subject at that title, the ordering finding
over that same block with them. A
remedy that ends by disabling the checks its own subject is finally eligible for
is not a remedy, and one that hides a live defect of another class the whole time
it stands is worse, so THREE obligations attach to the entry and all three are
part of it. The first is the AVAILABILITY bound route 2 states, which is what
keeps the ORDERING reading above empty; the other two are here:

- **GRAIN.** The entry SHALL name the REQUIREMENT and not the delta path alone,
  so that it reaches the one block it answers rather than every finding this
  family raises against a delta file that may carry several blocks.
- **RETIREMENT.** The entry SHALL be retired when the declared basis archives,
  that being the act after which it silences a comparison instead of answering a
  disappearance. **AND THE INTERVAL BEFORE THAT ACT IS EMPTY BY THE AVAILABILITY
  BOUND AND NOT BY THE PENDING STATE ALONE.** A pending block's three comparison
  arms do not run, so while the basis is unpromoted the entry silences nothing of
  theirs; the ordering arm is the exception, running before resolution and read
  through the same key, and route 2's bound is what makes that reading empty for
  as long as the entry stands. Without it this interval would carry one class of
  live finding the entry hid. The retirement is an obligation of THE ARCHIVING
  CHANGE — the
  act that promotes the requirement is the act that makes the arms able to read
  the block — and it is evidenced at that change's own archive gate. The
  MODIFYING change's archive gate SHALL confirm that no such entry stands over
  its block, a block whose carriage no arm has been allowed to read being exactly
  what that gate exists to refuse. The ORDER of the two archive acts stays
  `release-realization`'s obligation and is neither restated nor widened here;
  what this requirement adds is only the bound on an instrument this capability
  owns.

**THE CHECK READS EVERY ACTIVE CHANGE REGARDLESS OF LIFECYCLE STANDING**, as
this family's reading rule already provides, and this is deliberately wider than
the REFERENCE-AND-DECLARE half `release-realization` scopes to an active ratified
change — though not wider than that capability's ARCHIVE HOLD, which keys on the
unpromoted title and reaches a basis of any standing. A finding SHALL name the
declared or resolved basis change and, where that change is not ratified, SHALL
say so, so that a reader can see at a glance
whether an obligation or only an observation stands behind the row. **THE
BASIS'S OWN STANDING IS READ THE WAY THIS FAMILY ALREADY READS STANDING** —
through the one lifecycle-header reader its two-writers arm uses for
`release-realization`'s `ratified` scoping, never a private regex — so the fact
that qualifies a finding's wording and the fact the UNDISCLOSED state turns on
are one fact read once. A basis whose header declares no standing this reader
can resolve SHALL be treated as not ratified, the whole point of the disclosure
being to warn a reader about text no authority has been shown to accept, and a
standing nobody can read being no such showing.

#### Scenario: A block over a sibling's addition carries no marker
- **WHEN** an active change's MODIFIED block names a requirement the promoted specification does not carry, an active change ADDS or RENAMES to that title, the change carrying the block does not itself ADD that title, and the block carries no `Modified over` marker
- **THEN** the run MUST emit one `warning` finding against the active delta's own path, naming the requirement, the change whose addition it resolves to, and that no marker declares the pairing
- **AND** the three comparison arms MUST NOT run against that block, there being no promoted requirement to compare it to
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

#### Scenario: A block over a sibling's addition is correctly declared
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis an active change other than its own that ADDS or RENAMES to the block's capability and requirement title, that marker's `by` identifier is the change whose delta carries the block, that marker carries the nonempty reason its form requires, and the basis change is `ratified`
- **THEN** no finding MUST be emitted for that block, a declared pairing being the state this check exists to produce
- **AND** the reason's presence MUST be one of the conditions of that silence, an otherwise identical marker carrying the prefix alone being reported rather than passed

#### Scenario: The marker names a change that does not add the requirement
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis a change that neither ADDS nor RENAMES to its capability and requirement title, and the change carrying the block does not itself ADD that title
- **THEN** the run MUST emit a `warning` finding naming the change the marker names and stating that it adds no such requirement
- **AND** that finding MUST be worded apart from the undeclared case, a wrong basis and an absent one having different remedies
- **AND** a marker naming the CARRYING change itself as basis MUST be reported in this state wherever that change is not reported self-referential, a block's basis being a change other than the one that writes it

#### Scenario: The marker's `by` identifier is not the change carrying the block
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, whose basis DOES add or rename to the block's capability and requirement title, and whose `by` identifier is a change other than the one whose delta carries the block
- **THEN** the run MUST emit one `warning` finding in the misdeclared state, naming the identifier the marker carries and the change that carries the block, a right basis under a wrong author being a FALSE provenance rather than an incomplete one
- **AND** an otherwise identical marker whose `by` identifier IS the carrying change MUST NOT be reported on that ground, the identifier being validated against the carrier rather than merely resolved
- **AND** no undeclared finding MUST be emitted for that block alongside it, the marker being present and the states being exclusive

#### Scenario: A block carries two pairing markers
- **WHEN** such a block carries MORE THAN ONE paragraph of the reserved `Modified over` form — one of them naming a basis that does add the requirement and carrying as its `by` identifier the change that carries the block, the other naming a change that adds nothing
- **THEN** the run MUST emit exactly ONE `warning` finding for that block, in the misdeclared state and on the count ground, naming how many such markers the block carries
- **AND** the finding MUST NOT depend on which of the markers is examined, the count being read before any marker's basis or `by` identifier is
- **AND** an otherwise identical block carrying EXACTLY ONE valid marker MUST NOT be reported, this ground reaching a plurality of declarations and never a lawful single one

#### Scenario: The marker carries its prefix and no reason
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis an active change other than its own that ADDS or RENAMES to the title and carrying as its `by` identifier the change whose delta carries the block, the basis change is `ratified`, and that marker carries no ` — ` separator or carries one with nothing but whitespace after it
- **THEN** the run MUST emit one `warning` finding for that block in the misdeclared state, on the reason ground, stating that the marker carries no reason
- **AND** the block MUST NOT be placed in DECLARED AND RESOLVING, a declaration `document-lifecycle` calls incomplete not being one this check passes in silence
- **AND** the block MUST NOT be reported UNDECLARED, the paragraph being a recognized marker of this form whose declaration is defective rather than an absent one, and the remedy being to write the reason rather than to add a marker

#### Scenario: A prefix-only marker names an unratified basis
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker with a right basis and a right `by` identifier and no reason at all, and the basis change carries a status other than `ratified`
- **THEN** the run MUST emit exactly ONE finding for that block, in the misdeclared state and on the reason ground, the reason being read before the disclosure
- **AND** the block MUST NOT be reported UNDISCLOSED, that state reading a word in a reason clause and there being no clause to read it in, so that its remedy would name a word rather than the missing tail
- **AND** the finding MUST NOT depend on the basis's standing, the identical marker over a `ratified` basis being reported on the same ground

#### Scenario: A change modifies its own unpromoted addition
- **WHEN** one change carries both an ADDED and a MODIFIED block for one capability and requirement title
- **THEN** the run MUST emit a `warning` finding against that delta
- **AND** a `Modified over` marker naming that same change MUST NOT suppress it
- **AND** exactly ONE finding of this class MUST be emitted for that block, in the self-referential state, whether the block carries no marker, one, or several — that state being examined first and excluding the undeclared and misdeclared readings the same block would otherwise also satisfy

#### Scenario: The carrier renames the requirement and modifies it in one delta
- **WHEN** one change carries a `## RENAMED Requirements` block renaming a promoted requirement TO a title and a MODIFIED block for that same title
- **THEN** the block MUST NOT be reported in the self-referential state, nor in any other state of this class, the promoted resolution order resolving it against canon under the OLD name before this check is reached
- **AND** the three comparison arms MUST run against it under that old name, this requirement preserving that precedence rather than displacing it

#### Scenario: A block is declared over a basis no authority has accepted
- **WHEN** such a block carries EXACTLY ONE `Modified over` marker, naming as basis an active change other than its own that ADDS or RENAMES to the title, whose `by` identifier is the change whose delta carries the block, that marker CARRIES A REASON, that basis change carries a status other than `ratified`, and that reason clause does not carry the disclosure `document-lifecycle` requires
- **THEN** the run MUST emit one `warning` finding against the active delta's own path, naming the basis change and its declared standing and stating that the marker does not disclose it
- **AND** that finding MUST be worded apart from the undeclared and the misdeclared cases, a pairing declared over text no authority has accepted being a different defect from an absent basis or a wrong one
- **AND** a marker carrying no reason at all MUST be reported in the misdeclared state instead and never here, the reason being read before the disclosure and an absent clause being nothing for the disclosure to be read in

#### Scenario: The unratified basis is disclosed
- **WHEN** such a marker carries a reason, and that reason clause carries that disclosure or the change it names is `ratified`
- **THEN** no finding MUST be emitted for that block, the disclosure being the whole of what THIS CHECK asks of a declared pairing beyond the form's own reason
- **AND** a `ratified` basis MUST NOT be read as excusing the reason, a marker carrying the prefix alone being reported on the reason ground whatever its basis's standing
- **AND** that silence MUST NOT be read as archive clearance, `release-realization`'s hold standing over the block for as long as the title is unpromoted and keying on that title rather than on the basis's standing
- **AND** a disclosure MUST NOT be reported once the basis it discloses ratifies, the marker being a dated statement about the moment it was written

#### Scenario: A disclosed unratified pairing reaches the modifying change's archive gate
- **WHEN** a block this check passes in silence names a basis that is not ratified and whose marker discloses it, and the change carrying that block reaches its archive gate while the title is still unpromoted
- **THEN** this check MUST emit nothing for that block, its pairing being in good order, and that silence MUST NOT be read at the gate as clearance
- **AND** the fact the gate reads MUST be the block's own `pending` resolution — this family's, computed for every block — the title being unpromoted for exactly as long as the block resolves `pending`, and the hold that fact serves being `release-realization`'s obligation rather than this requirement's
- **AND** no finding of THIS class MUST be emitted for the held block, its remedy being the basis's ratification and archive rather than any edit to the block
- **AND** where that change archives regardless, the still-active basis's `## ADDED Requirements` block — or its `## RENAMED Requirements` block's `TO:` title — MUST be reported by the collision class on the next run, that being the mechanical evidence the breach leaves

#### Scenario: A declared basis archives
- **WHEN** the change a block is declared over archives and its addition reaches the promoted specification
- **THEN** the block MUST resolve against canon on the next run and the three comparison arms MUST run against it
- **AND** this check MUST emit nothing further for that block, its question having been answered by the promotion
- **AND** the modifying change's archive gate MUST open at that promotion and not before, whatever the basis's standing was while the block was pending

#### Scenario: The `Modified over` marker is not a carriage declaration
- **WHEN** a block carries a `Modified over` marker
- **THEN** that marker MUST NOT suppress any unit of any comparison, and MUST NOT be reported as a marker naming a unit the block still carries
- **AND** the marker paragraph MUST NOT be counted as a body unit of the block or of the requirement it promotes into

#### Scenario: A pairing finding is discharged by its marker
- **WHEN** a block this check reports gains a `Modified over` marker naming the change that adds its requirement, and the finding stops being emitted on the next run
- **THEN** the resolution MUST carry the citation this capability's uncited-resolution rule requires of a `contested` finding, recorded on the act that added the marker
- **AND** the citation MUST NOT be recorded IN PLACE OF the marker, a disposition standing in for the remedy being the state this class's band posture exists to avoid

#### Scenario: A finding of this class is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an active delta path, and a `cite`
- **THEN** findings of this class on that path MUST be suppressed on the same terms as this family's other findings, and the entry MUST be read as reaching the whole block rather than this class — the disposition is read before the block resolves and there is no finding-class grain for it to read
- **AND** the entry MUST name the requirement, an entry without that narrowing disposing every finding this family raises against a delta file that may carry several blocks
- **AND** an entry without a `cite`, or an entry naming another family, MUST suppress nothing

#### Scenario: A citation is recorded while a second ratified writer stands
- **WHEN** a pairing finding stands over a block, and an active change other than the one whose delta carries that block, whose declared standing is `ratified`, carries a `## MODIFIED Requirements` block for the same capability and requirement title
- **THEN** the citation route MUST be refused for that block and the pairing MUST be declared by marker with no entry recorded, an entry at this family's grain reaching the ordering finding over that title as well as the pairing one it answers
- **AND** the refusal MUST rest on the ordering arm having a SUBJECT at that title rather than on its having emitted, the declarations between two ratified writers being one proposal edit away from turning that arm's silence into a finding the standing entry would hide
- **AND** where no active change other than the carrier, whose declared standing is `ratified`, writes a MODIFIED block for that title any longer — that change having archived, or its standing having ceased to be `ratified` — the route MUST open, the arm having no subject there and nothing it could emit
- **AND** this bound MUST NOT be read as adding a finding class or a check to this family: it is an obligation on the act that records the entry, read from a state the family's own reader already computes

#### Scenario: The declared basis archives while a pairing disposition still stands
- **WHEN** the change a pairing disposition was recorded against archives, its addition reaches the promoted specification, and the entry still stands in `health/dispositions.yaml`
- **THEN** the entry MUST be retired by that archiving act, the block resolving against canon from that moment and the three comparison arms being the only reading of it there is
- **AND** the run's silence on that block MUST NOT be read as those arms clearing it, the disposition being read before the block resolves so that the silence is suppression rather than comparison
- **AND** the modifying change MUST NOT meet its own archive gate while the entry stands, a stale MODIFIED block deleting newly promoted clauses unreported being the defect those arms exist to report

### Requirement: An active block writing a title the promoted specification already carries is reported
The modified-block-currency family SHALL report every active change's `## ADDED
Requirements` block naming a capability and requirement title the promoted
specification already carries, AND every active change's `## RENAMED
Requirements` block whose `TO:` title the promoted specification already carries
for that capability, at `warning`, against that delta's own path.

**THIS IS THE ARCHIVE-ORDERING BACKSTOP, and it is the only direction in which
one can exist.** Where a MODIFIED-over-a-sibling's-basis pair archives in the
safe order the requirement enters canon first and every existing check resumes.
Where it archives in the unsafe order the modifying block promotes text nobody
reviewed as an addition or as a rename, and the surviving evidence is precisely
this: an active change still writing that title into canon — an ADDED block for
a title canon now carries, or a RENAMED block whose `TO:` title canon now
carries. Nothing in
the estate reads that shape. The family that compares an archived delta to canon
cannot, canon being the delta after the archive act; the family reading active
MODIFIED blocks reads ADDED and RENAMED blocks ONLY to build the pending set,
never against canon. Reading it here
costs one lookup against a promoted-requirement index this family already builds,
and one more pass over the rename pairs `resolve` already parses.

**THE RENAME'S COLLISION IS IN THE `TO:` HALF, AND THE DIRECTION IS THE WHOLE OF
WHAT MAKES THE CHECK READABLE.** A `## RENAMED Requirements` block names a
`FROM:` title and a `TO:` title. The `FROM:` half is expected to name a title
canon carries — that is what a rename renames — so reading THAT half would
report every lawful rename in the corpus. The collision shape is the `TO:` half:
a title canon ALREADY carries while an active change is still proposing to
rename something INTO it, which is the same surviving evidence an unpromoted
addition leaves, reached through the other basis form. Canon's own resolution
rule reads a rename BY ITS TARGET for exactly this reason — "where that block
renames a promoted requirement to this title"
(`openspec/specs/doc-health/spec.md:1568-1574`), with the scenario at
`:1783-1786` — so the half this class reads is the half canon already reads.

**A BASIS IS A BASIS EVERYWHERE OR NOWHERE.** `document-lifecycle`'s marker
requirement is owed where "an active change ADDS or RENAMES to that title", the
pairing check's misdeclared state accepts a basis that RENAMES to the title, and
`release-realization`'s ordering obligation reaches a requirement an active
change ADDS OR RENAMES TO — its reference-and-declare half at a ratified basis,
its archive hold at a basis of any standing. A backstop that read additions
alone would leave a rename-based pair with the declaration and the ordering rule both
reaching it and no mechanical evidence of a breach at all — the one hole this
requirement exists to close, left open for the one basis form that arrives less
often.

**THE CHECK IS NOT LIMITED TO THE PAIR THAT MOTIVATES IT.** An ADDED block, or a
rename's target, over a requirement canon already carries is a defect however it
arose — a stale packet, a duplicated title, an addition that should have been a
modification, a rename into a title that has since been added — and narrowing
the check to blocks that had a MODIFIED partner would decline to report the same
defect for a worse reason.

**THE FINDING SHALL BE ITS OWN CLASS**, registered and templated on the same
terms as every other class this family carries, and SHALL carry an action line
naming the two remedies: promote nothing further until the collision is
resolved, and — where the requirement genuinely already exists — convert the
addition to a modification declared against canon, or withdraw or re-target the
rename whose `TO:` title canon already carries. The band is `warning`; the
class is `contested` by the family's standing `FAMILY_RESOLUTION` row, which this
requirement neither adds nor can decline. Its exposure to the
uncited-resolution rule is smaller than the pairing class's and not absent: its
population is zero, so nothing is owed at launch, and a collision that stops
being reported has been resolved by a governance act with a change to cite.

**THE POPULATION IS ZERO ON THE AUTHORING TREE ACROSS BOTH BASIS FORMS, and that
is the argument for
building it now.** Measured: of the tree's active `## ADDED Requirements` blocks
none names a title the promoted specification already carries, and the tree
carries no active `## RENAMED Requirements` pair at all, so the widening to
renames costs a population of zero rather than a discharge. A check whose
standing population is empty costs nothing to
land, pins a state every reader already assumes, and is in place before the
first instance rather than after it — which for this shape matters more than
usual, because the first instance is an archive act that cannot be taken back.

#### Scenario: An active ADDED block names a requirement canon carries
- **WHEN** an active change's `## ADDED Requirements` block names a capability and requirement title the promoted specification already carries
- **THEN** the run MUST emit one `warning` finding against that delta's own path, naming the requirement and the promoted specification that carries it
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

#### Scenario: An active RENAMED block targets a title canon carries
- **WHEN** an active change's `## RENAMED Requirements` block names a `TO:` title the promoted specification already carries for that capability
- **THEN** the run MUST emit one `warning` finding against that delta's own path, on the same terms and in the same class as an ADDED block naming that title, a rename being a basis wherever an addition is
- **AND** the block's `FROM:` title MUST NOT be read for this class however it resolves, a rename's source being a title canon is expected to carry and reading it reporting every lawful rename

#### Scenario: The unsafe archive order is taken
- **WHEN** a change carrying a MODIFIED block over an active sibling's addition, or over an active sibling's rename to the title, archives before that sibling, so the requirement enters canon from the modifying block
- **THEN** the sibling's still-active block MUST be reported by this check on the next run — its `## ADDED Requirements` block, or its `## RENAMED Requirements` block's `TO:` title — the collision being the surviving evidence of the ordering breach
- **AND** the report MUST NOT be read as curing the breach, an archive act being outside what any health run can undo

#### Scenario: No active change writes a title canon carries
- **WHEN** every active `## ADDED Requirements` block names a title the promoted specification does not carry, and every active `## RENAMED Requirements` block names a `TO:` title it does not carry
- **THEN** this check MUST emit nothing, and its class MUST still render in the family's class block at a count of zero
