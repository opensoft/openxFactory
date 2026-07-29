# document-lifecycle Specification

## Purpose

Define the canonical lifecycle, controlled status taxonomy, ideation
convention, explicit-delta rule with its prose tagging markers, and
promotion-process binding for governance documents across openxFactory and
every DomainxFactory.
## Requirements
### Requirement: Canonical document lifecycle states
Governance documents across `openxFactory` and every DomainxFactory SHALL move
through one canonical lifecycle: `captured`, `organized`, `proposed`,
`ratified`, `implemented`, `promoted`, `adopted`, with `superseded` and
`retired` as terminal transitions and `rejected` or `deferred` as exits from
any pre-promoted state. Every transition SHALL be a deliberate, reviewable
step, never an implicit copy or a silent status edit.

#### Scenario: New governance thinking is recorded
- **WHEN** free-form design thinking, discussion output, or exploratory prose is added to a repository
- **THEN** it MUST enter the lifecycle at `captured` inside that repository's `ideation/brainstorm/` area
- **AND** it MUST NOT be treated as policy by any consumer

#### Scenario: A document changes lifecycle state
- **WHEN** a document moves between lifecycle states
- **THEN** the transition MUST be visible in review history (a commit moving it through an ideation gate, or an OpenSpec change)
- **AND** the document's status header MUST be updated in the same change

#### Scenario: A concept is rejected or deferred
- **WHEN** a captured, organized, or proposed concept is decided against or parked
- **THEN** its status MUST record `rejected` or `deferred` with the reason
- **AND** the artifact MUST be retained (not deleted) while any other document references it

### Requirement: Controlled document status taxonomy
Every governance document SHALL carry a `Status:` header drawn from the
controlled taxonomy: `brainstorm`, `staged`, `draft`, `ratified`, `standard`,
`superseded`, `retired`, `record`. Document genre SHALL NOT be encoded in the
status value; an optional `Kind:` header carries genre.

#### Scenario: A document claims standard authority
- **WHEN** a document's header declares `standard` status or its prose claims to be a shared xFactory standard
- **THEN** a promoted OpenSpec spec or canonical contract MUST back the claim
- **AND** absent such backing the document MUST carry `draft` or lower status

#### Scenario: A generated artifact is stored
- **WHEN** a simulation report, generated runbook, audit output, or other evidence artifact is committed
- **THEN** it MUST carry `record` status
- **AND** it MUST be excluded from prose-to-spec conversion and contradiction checks

#### Scenario: A document is superseded
- **WHEN** a later artifact replaces a document's content
- **THEN** the replaced document MUST move to `superseded` status naming its successor, or be deleted with the successor recording provenance

### Requirement: Ideation work area convention
Each repository that authors governance documents SHALL host its pre-proposal
pipeline in `ideation/brainstorm/` (non-normative capture) and
`ideation/staging/` (organized fragments). Content in `ideation/brainstorm/`
MAY contradict promoted specs; that area is the only place where
contradiction is sanctioned.

#### Scenario: Brainstorm content is organized
- **WHEN** brainstorm material is selected for progression
- **THEN** it MUST be organized into `ideation/staging/` or a candidate register with identified targets and deduplicated claims
- **AND** the brainstorm source MUST be marked `staged` (or note what was extracted) rather than silently duplicated

#### Scenario: Staged content becomes a proposal
- **WHEN** a staged topic is ready for ratification
- **THEN** an OpenSpec change MUST be created carrying the spec deltas
- **AND** the staged material MUST reference that change

#### Scenario: Cross-factory topic is captured
- **WHEN** ideation concerns the neutral layer or multiple DomainxFactories
- **THEN** it MUST be captured in `openxFactory`'s ideation area rather than a single domain repository

### Requirement: Explicit delta rule
Documents SHALL express any change to, contradiction of, or restatement of
promoted policy outside `ideation/brainstorm/` as an explicit change from
current state: an OpenSpec change proposal, or prose carrying the canonical
supersedes marker
`<!-- xspec:supersedes spec=<capability>/<requirement-slug> change=<change-id> -->`
naming the affected spec requirement. Prose designated for conversion to a
spec or contract SHALL be selected with the canonical block-level candidate
marker `<!-- xspec:candidate target=<capability> -->` ...
`<!-- /xspec:candidate -->`; candidacy is block-level only and no document
lifecycle status value expresses conversion candidacy. Accidental
restatement of promoted policy in differing words SHALL be treated as a
defect.

#### Scenario: Prose contradicts a promoted spec
- **WHEN** a document outside `ideation/brainstorm/` asserts behavior that conflicts with a promoted spec requirement
- **THEN** the document MUST either carry an `xspec:supersedes` marker naming that requirement (gaining a `change=` id once the OpenSpec change exists), or be corrected
- **AND** health tooling MUST report unmarked contradictions as findings

#### Scenario: Prose is tagged for conversion
- **WHEN** an author designates prose as needing conversion to a spec or contract
- **THEN** the designation MUST be an `xspec:candidate` block fence pair around the passage, naming the target capability
- **AND** only prose inside well-formed candidate blocks is queued for conversion
- **AND** the document's `Status:` header MUST NOT be used to express candidacy (no `spec-candidate` status exists)

#### Scenario: A staged fragment enters the queue
- **WHEN** a fragment lives in `ideation/staging/<topic>/` with a header declaring target capability and delta type
- **THEN** it is queued structurally by that header
- **AND** it MUST NOT require inline `xspec:` markers to be queued

### Requirement: Promotion process binding
Domain-to-neutral concept promotion and neutral-to-domain devolution SHALL
follow the documented promotion process, including candidate registration
with evidence, classification and scoring, OpenSpec ratification, and the
adoption steps (consumer re-pin, overlay replacement, local-copy retirement).
Register statuses SHALL be defined in terms of the canonical lifecycle
states. Neutralization drafts SHALL be produced by codexFactory
doc-engineering execution and approved by the originating domain's Hermes;
promotion provenance SHALL be machine-readable via optional `promoted_from`
and `specializes` declarations on the domain stack contract; and until a
promotion's re-pin gate completes, the domain-local copy SHALL remain
authoritative, with the register entry's status as the tiebreaker.

#### Scenario: A promotion is implemented
- **WHEN** a promoted neutral artifact merges into `openxFactory`
- **THEN** the promotion is not complete until each consuming DomainxFactory re-pins, replaces its local copy with a reference plus thin overlay, and the register entry reaches `adopted`
- **AND** a surviving domain-local near-duplicate MUST be reported as a health finding

#### Scenario: A neutral artifact proves domain-specific
- **WHEN** a neutral artifact is found to encode single-domain authority or vocabulary
- **THEN** a devolution MUST run the same lifecycle in reverse through an OpenSpec change, with the owning DomainxFactory adopting the content

#### Scenario: A neutralization draft is produced
- **WHEN** a promotion candidate is selected for drafting
- **THEN** codexFactory doc-engineering workers MAY produce the neutralization draft in openxFactory staging
- **AND** the originating domain's Hermes MUST review and approve the surrendered meaning before the OpenSpec change ratifies

#### Scenario: A promoted contract declares provenance
- **WHEN** a neutral artifact originates from a domain repo, or a domain overlay refines a neutral artifact
- **THEN** the consuming `stack.yaml` MAY declare `promoted_from` (origin repo and artifact) or `specializes` (refined neutral artifact)
- **AND** health tooling MUST verify that register entries at `adopted` status have resolvable provenance declarations where present

#### Scenario: A concept exists in both tiers mid-promotion
- **WHEN** a concept exists simultaneously in a domain repo and in openxFactory staging or an active change
- **THEN** consumers MUST treat the domain-local copy as authoritative until the re-pin gate completes
- **AND** the candidate register entry's status is the authoritative statement of promotion progress

### Requirement: Prose tagging marker hygiene
All `xspec:` markers SHALL be machine-checkable contract surface: every
occurrence of the literal string `xspec:` in governance Markdown MUST parse
against the canonical grammar (`xspec:candidate` open fence,
`/xspec:candidate` close fence, `xspec:supersedes` inline marker, with
space-separated unquoted `key=value` attributes), every marker target MUST
resolve, and candidate blocks MUST be properly fenced — no nesting, no
crossing of Markdown heading boundaries, and no unmatched open or close
fence. Deterministic health tooling SHALL report violations as findings.

#### Scenario: A marker is malformed or unknown
- **WHEN** the string `xspec:` occurs in a governance document but does not parse as a canonical `xspec:candidate`, `/xspec:candidate`, or `xspec:supersedes` marker
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A marker target does not resolve
- **WHEN** a marker names a `target=<capability>` or `spec=<capability>/<requirement-slug>` that does not exist under `openspec/specs/` or in an active change's spec deltas
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A candidate block is structurally invalid
- **WHEN** an `xspec:candidate` block nests inside another candidate block, spans a Markdown heading, or lacks a matching open or close fence
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A supersedes marker never acquires a change id
- **WHEN** an `xspec:supersedes` marker persists without a `change=` attribute beyond the doc-health aging threshold
- **THEN** the health pass MUST report it as an aging finding rather than accepting it as a permanent state

### Requirement: Proposal-owned supporting documents
When staged material crosses the proposal gate, the selected source documents SHALL
move from `ideation/staging/<topic>/` into
`openspec/changes/<change-id>/supporting-docs/`. The active change SHALL own a
machine-readable manifest recording the original staging path, source revision,
transition date, selected files and hashes, optional NotebookLM workspace
provenance, and any material remaining staged. Proposed prose SHALL carry
`Status: draft` and name the change; immutable evidence SHALL carry
`Status: record`.

#### Scenario: A complete staged topic becomes a proposal
- **WHEN** every file in a staged topic is selected for an OpenSpec change
- **THEN** the files MUST move into that change's `supporting-docs/` folder
- **AND** the empty staging topic MUST be removed so it no longer appears in the organized-work queue

#### Scenario: Part of a staged topic becomes a proposal
- **WHEN** only some staged files or fragments are selected for a change
- **THEN** only the selected material MUST move into the change's `supporting-docs/` folder
- **AND** the manifest MUST identify material remaining in staging

#### Scenario: Supporting material is non-normative evidence
- **WHEN** a generated report, imported source, or other immutable evidence supports a proposal
- **THEN** it MUST retain `Status: record` rather than becoming draft policy

### Requirement: Supporting-document archive retention
Before an OpenSpec change with supporting documents archives, its supporting folder SHALL
be packaged into a deterministic compressed bundle beside the
archived change and a readable manifest SHALL remain outside the bundle with
the bundle and per-file hashes. Historical bundles MUST NOT be stored under
canonical `openspec/specs/`.

#### Scenario: A supported change archives
- **WHEN** an active change with `supporting-docs/` reaches its archive gate
- **THEN** the archived change MUST contain `supporting-docs.tar.gz` and `supporting-docs.manifest.yaml`
- **AND** the uncompressed active supporting folder MUST no longer remain

#### Scenario: A bundle is placed with canonical specs
- **WHEN** a supporting-document archive is found under `openspec/specs/`
- **THEN** lifecycle validation MUST reject it as misplaced historical material

### Requirement: Possible feats declaration
A brainstorm document that enumerates candidate feats SHALL declare them in
a `Possible feats:` section, seeded by the author at capture, so unpicked
possibles are durable backlog rather than evaporating prose. Each declared
possible carries a register state — `latent`, `picked`, `rejected`, or
`superseded` — governed by the `ideation-cross-reference` register
contract; the canonical consolidated register is the cross-reference index,
and no third standalone register file exists. Legacy documents without the
section are valid and MUST NOT have possibles fabricated for them; only the
designated worked examples are backfilled as renderer fixtures.

#### Scenario: A new brainstorm is captured
- **WHEN** an author captures a brainstorm that names things the topic could become
- **THEN** those candidates are seeded in a `Possible feats:` section at capture

#### Scenario: A possible is picked at the organize gate
- **WHEN** staging picks a declared possible
- **THEN** its state becomes `picked` citing the staged topic's staging ID
- **AND** the citation inherits the change ID when the topic crosses the proposal gate

#### Scenario: A legacy document has no section
- **WHEN** a document written before this requirement carries no `Possible feats:` section
- **THEN** lifecycle validation MUST NOT report it and no history is fabricated

