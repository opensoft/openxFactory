# doc-health Delta: Agentic Semantic Sweep

## ADDED Requirements

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

#### Scenario: An analysis run executes
- **WHEN** the analysis worker runs
- **THEN** its environment holds no repository credentials and no factory identity token
- **AND** the report records the job envelope reference, the model id, and the prompt-contract version used

#### Scenario: The analysis worker fails
- **WHEN** the analysis step errors or the model is unavailable
- **THEN** the run MUST record the sweep as skipped in the report and the deterministic results MUST land unaffected

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

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twelve check families
over the whole factory family's governance corpus: status validity,
standard backing, ratified provenance, succession integrity, location
conformance, record immutability, staged/candidate aging,
register-lifecycle consistency, tag hygiene, submodule pin drift,
contract-copy drift, and notebook projection drift. Every check in this
pass MUST be deterministic — identical inputs produce identical findings,
with no model calls; semantic analysis belongs exclusively to the agentic
semantic sweep pass this capability defines separately. Check families
SHALL implement promoted spec wording; staged ideation fragments are inputs
to contracts, never check definitions.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** a family that cannot run (e.g. notebook drift without credentials) MUST be reported as skipped, never silently omitted

#### Scenario: Lifecycle conformance checks fire
- **WHEN** a governance document violates a `document-lifecycle` rule — a free-form or missing `Status:` value, an unbacked `standard` claim, a dangling `Ratified by:` reference, a `superseded` doc without a successor, a `brainstorm` doc outside `ideation/brainstorm/`, a `staged` doc that is outside `ideation/staging/` and is not a candidate register (`Kind: register`), or a content edit to a `record` doc after capture
- **THEN** the run MUST emit a finding naming the check family, the repo, the path, and the violated rule

#### Scenario: A register carries staged status
- **WHEN** a candidate register (`Kind: register`) carries `Status: staged` outside `ideation/staging/`
- **THEN** location conformance MUST NOT emit a finding — registers are a promoted organized-state home per the `document-lifecycle` capability

#### Scenario: Drift checks fire
- **WHEN** a submodule pin lags its remote main, a contract copy diverges from its canonical source, or the lifecycle notebook projection dry-run reports nonzero add/update/delete operations
- **THEN** the run MUST emit a drift finding identifying what diverged and from which source of truth
