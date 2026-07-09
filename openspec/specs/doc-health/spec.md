# doc-health Specification

## Purpose

Define the deterministic health-check contract for the factory family's
governance corpus: the check families, finding severities, the dated report
and ranked plan, the headline canon-share metric, and the ownership split
between contract, implementation, and the nightly runner.
## Requirements
### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twelve check families
over the whole factory family's governance corpus: status validity,
standard backing, ratified provenance, succession integrity, location
conformance, record immutability, staged/candidate aging,
register-lifecycle consistency, tag hygiene, submodule pin drift,
contract-copy drift, and notebook projection drift. Every check MUST be
deterministic — identical inputs produce identical findings, with no model
calls; semantic sweeps are out of this capability's scope. Check families
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
The contract SHALL define default aging thresholds so reports are
comparable across runs: staged topics and `xspec:candidate` blocks
untouched 30 days are `warning` findings escalating to `error` at 90 days;
an `xspec:supersedes` marker without `change=` is `warning` at 14 days
escalating to `error` at 45 days; `draft` documents have their age
distribution reported always (`info`) with a `warning` at 60 days without a
lifecycle transition.

#### Scenario: An item crosses an aging threshold
- **WHEN** an item's untouched age crosses a threshold
- **THEN** the run MUST emit the finding at the threshold's severity
- **AND** crossing an escalation boundary produces a new `error` finding subject to the regression rule

#### Scenario: A draft lives long legitimately
- **WHEN** a `draft` document ages without transition
- **THEN** it MUST appear in age reporting and, past 60 days, as a `warning` ranked-plan item — never as `critical` or `error` on age alone

### Requirement: Ownership and hosting split
The doc-health contract and report schema SHALL be owned by openxFactory;
the implementation (checker scripts, report generator, reusable workflow)
SHALL be owned by codexFactory; the nightly runner SHALL be hosted by the
xFactory aggregation repo as the only repo pinning every submodule; and
content authority SHALL stay with each owning factory — health tooling
reports and stages, it never approves or merges another factory's content.

#### Scenario: The pipeline changes shape
- **WHEN** a check family, report schema element, severity rule, or threshold default changes
- **THEN** the change MUST be an OpenSpec delta to this capability in openxFactory, and the implementation follows it

#### Scenario: A finding concerns a domain factory's content
- **WHEN** the ranked plan proposes work on a DomainxFactory's documents
- **THEN** the item enters that work as a staged proposal; approval remains with the owning factory's authority, and the health pipeline MUST NOT auto-apply content changes

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
