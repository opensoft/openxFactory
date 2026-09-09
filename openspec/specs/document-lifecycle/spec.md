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
`superseded`, `retired`, `record`, `projection`. Document genre SHALL NOT be encoded in the
status value; an optional `Kind:` header carries genre.

**The `projection` standing.** A document that a named generator RE-DERIVES IN PLACE from a declared source of truth SHALL carry `projection` rather than `record`. Being generated is not what makes a document a record; being CAPTURED ONCE is. The test SHALL be whether re-running the generator over the same path is the correct way to update the document: where it is, the document holds no captured state for immutability to protect, and each regeneration would otherwise be reported as a content edit to a record — making the correct act a finding. A `projection` document SHALL name its generator and its source, SHALL NOT be hand-edited, and SHALL NOT be treated as authoritative over the source it renders. A one-shot capture — a simulation report, an audit output, a dated run report, a byte-exact evidence snapshot — is NOT a projection and SHALL keep `record`; a second run of such a generator writes a different path rather than rewriting the same one.

**Ratification citation.** A `ratified` header SHALL name its ratification. A bare, uncited `Status: ratified` is a violation whatever else the document says, because the header asserts an approval the document does not point at. TWO citation spellings are sanctioned, and they are not interchangeable — each has a condition of use, and the condition is what decides which one is correct:

- `Ratified by: <change>` is the PRIMARY spelling and SHALL be used wherever an approving OpenSpec change exists to name. The named change IS the citation.
- `Ratified:` is the RECORD-CITING alternative and SHALL be used only where no approving OpenSpec change exists to name — an in-session ruling, a disposition, an `.openspec.yaml` approval pair, an archive or ratification commit, or another durable record. Reaching for the primary spelling in that situation would mean naming a change that does not exist.

A document SHALL carry exactly one ratification citation, in one of the two spellings. The count is ONE TOTAL across both spellings: a document MUST NOT carry one of each, and MUST NOT carry the same spelling twice. Two lines each claiming to name the ratification say nothing about which is current, whether or not they are spelled alike.

**The three-way floor on the record-citing form.** A `Ratified:` citation SHALL name at least one of three things: an approver, a date, or a resolvable record path. Naming none of the three is a finding, because such a line asserts a ratification nothing can be checked against — the bare uncited header's defect, differently spelled. The floor is deliberately a floor and not a fixed field set: the corpus's honest citations name different subsets (approver plus date plus a verbatim instruction; date plus a record pointer with no approver named; date alone where the record names no ratifier), and a rule demanding all three would force the invention of provenance the record does not carry, which is the failure mode this rule exists to prevent.

The floor SHALL apply to the `Ratified:` form only and SHALL NOT be applied to `Ratified by:`, whose named change is itself the resolvable record. A governed document whose `Ratified by:` line names its approving change and nothing else is correct as written and MUST NOT be reported.

A ratification citation is read in the document's lifecycle header, alongside the `Status:` header it justifies. Prose elsewhere in a document that begins with the same word — a section-level decision label, a sentence starting "Ratified together with…" — is body text and is NOT a ratification citation.

**Merged into `A generated artifact is captured once` by declare-generated-projection-status (2026-08-28):** `A generated artifact is stored`

#### Scenario: A document claims standard authority
- **WHEN** a document's header declares `standard` status or its prose claims to be a shared xFactory standard
- **THEN** a promoted OpenSpec spec or canonical contract MUST back the claim
- **AND** absent such backing the document MUST carry `draft` or lower status

#### Scenario: A generated artifact is captured once
- **WHEN** a simulation report, generated runbook, audit output, dated run report, or other evidence artifact is committed as a one-shot capture
- **THEN** it MUST carry `record` status
- **AND** it MUST be excluded from prose-to-spec conversion and contradiction checks

#### Scenario: A generated artifact is re-derived in place
- **WHEN** a document is deterministically re-rendered over the same path by a named generator from a declared source of truth
- **THEN** it MUST carry `projection` status rather than `record`
- **AND** regenerating it MUST NOT be reported as a content edit to a record, because re-derivation is the only correct way to update it
- **AND** it MUST be excluded from prose-to-spec conversion and contradiction checks, as a `record` is

#### Scenario: A generator emits the status it declares
- **WHEN** a generator writes a document this capability classifies as a projection
- **THEN** the generator MUST emit `Status: projection` itself
- **AND** a later regeneration MUST NOT reintroduce a status the classification has moved away from

#### Scenario: A document is superseded
- **WHEN** a later artifact replaces a document's content
- **THEN** the replaced document MUST move to `superseded` status naming its successor, or be deleted with the successor recording provenance

#### Scenario: An approving OpenSpec change exists
- **WHEN** a document carries `Status: ratified` and an approving OpenSpec change exists to name
- **THEN** it MUST cite that change with `Ratified by: <change>`
- **AND** the record-citing `Ratified:` spelling MUST NOT be used in its place

#### Scenario: A ratification has no approving OpenSpec change
- **WHEN** a document carries `Status: ratified` and no approving OpenSpec change exists — the ratification is an in-session ruling, a disposition, an `.openspec.yaml` approval pair, or another durable record
- **THEN** it MUST cite that record with `Ratified:` naming at least one of an approver, a date, or a resolvable record path
- **AND** the citation MUST NOT name a change that does not exist, and MUST NOT invent an approver, a date, or a record the evidence does not carry

#### Scenario: A record-citing ratification names nothing checkable
- **WHEN** a `Ratified:` citation names none of an approver, a date, or a resolvable record path
- **THEN** it MUST be reported as a finding
- **AND** a `Ratified by:` citation naming its approving change and nothing else MUST NOT be reported, because the named change is its record

#### Scenario: A ratified header carries no citation at all
- **WHEN** a document carries `Status: ratified` with neither a `Ratified by:` nor a `Ratified:` line in its lifecycle header
- **THEN** it MUST be reported as a finding
- **AND** body prose beginning with the word "Ratified" outside the lifecycle header MUST NOT be counted as the missing citation

#### Scenario: A ratified header carries more than one citation
- **WHEN** a document carries `Status: ratified` and its lifecycle header carries more than one ratification citation line — one in each spelling, or the same spelling twice
- **THEN** it MUST be reported as a finding, because two lines each claiming to name the ratification say nothing about which is current
- **AND** the violation MUST be reported on the count, not on the pair, so a second citation in the same spelling is the same finding as one of each — including where the first line alone would be correct

### Requirement: Ideation work area convention
Each repository that authors governance documents SHALL host its pre-proposal
pipeline in `ideation/brainstorm/` (non-normative capture) and
`ideation/staging/` (organized fragments). Content in `ideation/brainstorm/`
MAY contradict promoted specs; that area is the only place where contradiction
is sanctioned. Known-domain ideas SHALL be captured in their owning
DomainxFactory; clearly neutral or already cross-domain ideas SHALL be captured
in openxFactory; and genuinely unknown-owner ideas SHALL be captured as
independent items under
`openxFactory/ideation/brainstorm/inbox/<idea-id>/`. A domain-origin idea that
later crosses boundaries SHALL retain its original source while an openxFactory
routing hub is created under
`ideation/brainstorm/cross-domain/<idea-id>/`. The xFactory aggregation
repository MUST NOT host a general ideation backlog, and a monolithic tagged
inbox MUST NOT replace independently routable items.

#### Scenario: Brainstorm content is organized
- **WHEN** brainstorm material is selected for progression
- **THEN** it MUST be organized into `ideation/staging/` or a candidate register with identified targets and deduplicated claims
- **AND** the brainstorm source MUST be marked `staged` (or note what was extracted) rather than silently duplicated

#### Scenario: Staged content becomes a proposal
- **WHEN** a staged topic is ready for ratification
- **THEN** an OpenSpec change MUST be created carrying the spec deltas
- **AND** the staged material MUST reference that change

#### Scenario: Clearly neutral or cross-domain topic is captured
- **WHEN** ideation is known at capture to concern the neutral layer or multiple DomainxFactories
- **THEN** it MUST be captured in openxFactory's brainstorm area

#### Scenario: Ownership is genuinely unknown
- **WHEN** an idea's owner cannot yet be determined
- **THEN** it MUST be captured as an independent openxFactory inbox item without guessing an owner

#### Scenario: Domain-origin topic expands
- **WHEN** a DomainxFactory brainstorm later develops neutral or other-domain claims
- **THEN** its original domain source MUST remain in place as design history and authority for local meaning
- **AND** an openxFactory cross-domain routing hub MUST reference the source and coordinate extracted claims

#### Scenario: General backlog is placed in aggregation
- **WHEN** a general brainstorm area, unclassified inbox, or monolithic tagged backlog is created in the xFactory aggregation repository
- **THEN** lifecycle validation MUST reject the placement

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
provenance, and any material remaining staged. The manifest SHALL repeat
`origin.kind` and `origin.id` — and, for staged origins, `origin.path` — and
those values MUST match the change's `.openspec.yaml`. When selected material
derives from routed claims, the manifest SHALL additionally carry an
`ideation_provenance` entry for each source idea, naming the Idea ID, selected
Claim IDs, and a routing-record reference with canonical repository ID,
repository-relative path, and full committed revision. The Claim IDs SHALL
resolve in that pinned routing record. Unrelated proposals MUST NOT invent
ideation provenance. Proposed prose SHALL carry `Status: draft` and name the
change; immutable evidence SHALL carry `Status: record`.

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

#### Scenario: Manifest origin disagrees with the packet
- **WHEN** a support manifest's repeated origin fields differ from the change's `.openspec.yaml` declaration
- **THEN** strict proposal validation MUST fail

#### Scenario: Routed material enters a proposal
- **WHEN** staged material derived from routed claims crosses the proposal gate
- **THEN** its manifest MUST name every source Idea ID and selected Claim ID
- **AND** each routing-record repository, path, and full committed revision MUST resolve

#### Scenario: Proposal cites a missing routed claim
- **WHEN** proposal provenance names a Claim ID absent from its pinned routing record
- **THEN** strict proposal validation MUST fail

#### Scenario: Proposal omits a routing revision
- **WHEN** routed proposal provenance does not pin a full committed revision for the routing record
- **THEN** strict proposal validation MUST fail

#### Scenario: Proposal has no routed source
- **WHEN** a proposal did not derive from routed claims
- **THEN** its support manifest MUST remain valid without `ideation_provenance`

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

### Requirement: Canonical supporting-document mover
The canonical mover implementing the proposal-owned supporting-document and archive-retention requirements SHALL be owned by openxFactory as `scripts/proposal-support.py`.
It transitions selected staged material from `ideation/staging/<topic>/`
into an active change's `supporting-docs/` (status transitions, relative
link rewrites, a machine-readable manifest with per-file sha256 and source
snapshots), verifies the bundle, and packages the deterministic
`supporting-docs.tar.gz` + `supporting-docs.manifest.yaml` pair preserved
through OpenSpec archive. Doc-health family 5 (location conformance)
checks the artifacts it produces — with this adoption, producer and
checker live in the same repository.

#### Scenario: A staged doc cited by a proposal moves via the tool

- **WHEN** a staged topic's selected files transition into an active change through the tool
- **THEN** the files land under that change's `supporting-docs/` with statuses transitioned (`staged` becomes `draft` naming the change; `record` is retained), relative links rewritten to resolve from the new location, and a manifest recording origin path, source revision, transition date, selected files with hashes, and any material remaining staged
- **AND** the manifest verifies: each moved file's sha256 and source snapshot match, and a committed source revision's blob hashes reconcile

#### Scenario: Manifests survive archive

- **WHEN** a change with supporting documents reaches its archive gate
- **THEN** the tool packages the folder into a deterministic compressed bundle beside the archived change with a readable manifest carrying bundle and per-file hashes, and verification passes over the archived pair
- **AND** doc-health family 5 reports any checksum mismatch, incomplete archived support, or historical bundle misplaced under canonical `openspec/specs/`

### Requirement: Proposal origin declaration
Every OpenSpec change proposal SHALL declare exactly one origin in its
`.openspec.yaml`. The origin's IDENTITY — `kind`, `id`, and for a staged
origin `path` — is fixed when the proposal is created and unchanged for the
life of the change; that identity is what the support manifest repeats and
what a disagreement reports as post-ratification mutation. A `staged` origin
carries `kind: staged`, a durable
`id` of the form `<repo>:staging:<topic-slug>`, and a `path` naming the
original repository-relative staging folder; at the proposal transition the
staged folder MUST contain a document whose `Staging ID:` equals
`origin.id`. An `ad_hoc` origin carries `kind: ad_hoc`, a durable `id` of
the form `<repo>:adhoc:<date>-<sequence-or-slug>`, a required `reason`, and
EITHER approval provenance (`approved_by` and `approved_on`) OR drafting
provenance (`proposed_by` and `proposed_on`) — one of the two pairs in full,
never neither and never half of one. An APPROVED ad-hoc origin is an
explicit,
approved exception — it MUST NOT substitute for staging when organized
source material exists, and a proposal MUST NOT declare both origin kinds.
Durable ids remain valid after the staging folder moves, is compressed, or
is removed; `origin.path` is the historical record of the transition
source, not a live link.

**AN UNAPPROVED PROPOSAL SHALL BE EXPRESSIBLE.** An ad-hoc origin declaring
`proposed_by` and `proposed_on` in place of the approval pair declares
provenance WITHOUT asserting approval: a lawful state of the record, not a
defect awaiting one. The state exists because this corpus produces it
deliberately — a "scout and draft, do not implement" assignment is supposed
to yield a packet that exists, validates, and is not yet approved — and
because before it existed the only shapes available to such a packet were an
ad-hoc origin missing its required approval date, or no origin block at all.
Both were reported, so the only mechanical ways to clear the report were to
approve the change, delete the draft, or write an approval date nobody gave.
Inventing that date is the defect the approval fields exist to prevent, and a
rule whose only remedy is the defect it forbids is a rule that trains its
readers to disbelieve the checker.

**APPROVAL IS AN ADDITION, NEVER A REWRITE.** When an unapproved origin is
approved, the approval pair SHALL be added to the declared origin and the
identity SHALL NOT move: the durable id minted at drafting remains the
durable id after approval, so no manifest that repeats it comes to disagree
with the packet, and the addition MUST NOT be read as mutation of a fixed
origin. The drafting pair MAY remain beside the approval, and normally
should: it is the record of who drafted the proposal and when, which the
approval does not restate.

**APPROVAL SHALL APPEAR WHEN A STATUS CLAIMS IT.** A proposal whose own
`Status:` declares `ratified`, or any standing beyond it, SHALL carry
approval provenance in its origin. A proposal that declares such a standing
while its origin asserts no approval is a defect in the record, and its
lawful remedies are exactly two: record the approval provenance the status
claims, or return the proposal to a pre-ratification standing. Writing an
approval date the record does not carry is not a third remedy. The
unapproved state relaxes WHEN approval must be recorded; it does not relax
WHETHER a ratified proposal was approved, and it MUST NOT be entered to
quiet a check on a proposal that claims ratification.

#### Scenario: A staged proposal is created
- **WHEN** an OpenSpec change is created from a staged topic
- **THEN** its `.openspec.yaml` MUST declare `kind: staged` with the topic's durable id and original staging path
- **AND** the staged folder MUST contain, at transition, a document whose `Staging ID:` equals the declared id

#### Scenario: An ad-hoc proposal is created
- **WHEN** an OpenSpec change is deliberately created without a staging source, and its creation is approved
- **THEN** its `.openspec.yaml` MUST declare `kind: ad_hoc` with a durable id, the reason, the approving authority, and the approval date
- **AND** supporting evidence MAY still live under `supporting-docs/` but MUST NOT claim a fabricated staging source

#### Scenario: An unapproved proposal is drafted
- **WHEN** an OpenSpec change is deliberately created without a staging source and no approval act exists yet
- **THEN** its `.openspec.yaml` MUST declare `kind: ad_hoc` with a durable id, the reason, `proposed_by`, and `proposed_on`
- **AND** it MUST NOT carry an approval date no authority gave
- **AND** the origin MUST NOT be reported as incomplete for lacking the approval pair

#### Scenario: An unapproved origin is later approved
- **WHEN** an authority approves a proposal whose origin declared drafting provenance
- **THEN** `approved_by` and `approved_on` MUST be added to the declared origin
- **AND** `kind`, `id`, and `path` MUST remain exactly as declared at drafting
- **AND** the addition MUST NOT be reported as mutation of a fixed origin

#### Scenario: A proposal claims a ratification its origin does not carry
- **WHEN** a proposal's `Status:` declares `ratified` or beyond while its origin carries drafting provenance and no approval
- **THEN** health tooling MUST report it
- **AND** the remedy is to record the approval provenance or to return the proposal to a pre-ratification standing, never to invent an approval date

#### Scenario: The proposal gate rejects a malformed origin
- **WHEN** a proposal's origin is missing, declares an unknown kind, declares both kinds, carries a staged id or path that does not resolve before transition, disagrees with the staging header or support manifest, lacks ad-hoc reason, declares neither approval nor drafting provenance, or completes only half of the pair it declares
- **THEN** strict proposal validation MUST fail

#### Scenario: The staging folder later disappears
- **WHEN** a declared staged origin's topic folder moves, is compressed, or is removed after the proposal transition
- **THEN** the origin id and path remain unchanged as historical provenance and MUST NOT be rewritten to track the new location

### Requirement: The proposal gate records its authorship once per document, not once per attempt
When the promotion gate moves staged material into a change's supporting documents it records which change proposed that material on the document itself. That record SHALL be UPDATED where one already exists rather than added beside it, so a document that makes the round trip more than once carries exactly one such line naming the most recent attempt.

A document may legitimately reach proposal, be demoted, be worked, and reach proposal again — the round-trip guarantee exists precisely so that lap is normal. Appending a fresh authorship line each time turns a normal lap into visible cruft, and worse, into an ambiguous record: several lines each claiming to name the proposing change say nothing about which one is current.

The obligation sits on the gate that WRITES the line. The reverse transition MUST NOT be made to remove or rewrite it, because the reverse transition's own refresh is bounded to the round-trip provenance slots and the marked proposal-element sections and MUST leave every other byte of a live fragment unchanged; widening that boundary to tidy a header would trade a data-loss guarantee for neatness.

The reduction to one record SHALL apply to every such record the document carries outside a code fence, wherever it sits, and not only to the ones inside the document's header block — the requirement is that the document carry exactly one, and a stale record left standing in the body says the same ambiguous thing as one left standing in the header. A record inside a code fence is an EXAMPLE and MUST NOT be touched. Scope stated as measured rather than as an estimate: 0 documents in the corpus today carry a second such record or one outside their header block, so this clause governs the shape rather than clearing a backlog.

#### Scenario: A stale record sits outside the header block
- **WHEN** staged material carries a proposing-change record in its header block and another further down the document, outside any code fence
- **THEN** exactly one record MUST remain, naming the current change
- **AND** a record inside a code fence MUST be left unchanged

#### Scenario: A document reaches proposal for the second time
- **WHEN** staged material that already carries a proposing-change record is moved into a change's supporting documents
- **THEN** the existing record MUST be updated to name the current change
- **AND** the document MUST carry exactly one such record

#### Scenario: A document reaches proposal for the first time
- **WHEN** staged material carrying no proposing-change record is moved into a change's supporting documents
- **THEN** the record MUST be added

#### Scenario: The reverse transition returns a document carrying the record
- **WHEN** the reverse transition returns a document that carries a proposing-change record
- **THEN** it MUST NOT remove or rewrite that record
- **AND** the bounded-refresh guarantee over a live fragment MUST remain intact

### Requirement: Staged topic primary-fragment template
A staged topic's primary fragment SHALL follow a fixed template so that its live state is extractable by a reader or a parsing tool without opening the rest of the topic folder. The primary fragment is the file `primaryFragmentPath` already selects deterministically and path-only; this requirement adds no second candidate file and MUST NOT change that selection. Every other file in a topic folder stays free-form.

A conforming primary fragment SHALL carry three required sections — pre-document non-documented idea notes, conflicts, and open questions — in addition to its proposal-element sections. Each open question SHALL carry four sub-fields in this fixed order: Context, Recommended answer, Explanation, Disposition status. A question MUST NOT be recorded as a bare question: the template requires a recommendation and the reasoning for it even while the disposition itself remains open, so that an undecided question still carries a proposal to disagree with.

Sections beyond the required set MAY be added by either a human or an AI, and each added section SHALL carry an `Added-by:` line naming the person or agent and the date. Attribution is required because the document accumulates content nobody commissioned in advance.

The proposal-element sections SHALL be wrapped in the ratified `xspec:candidate` / `xspec:supersedes` prose-tagging marker grammar rather than a second addressing mechanism. That prose IS the candidate text an eventual OpenSpec change would carry, and the marker grammar already exists for exactly that content.

**Round-trip on demote.** When a topic that reached proposal is demoted back to staging — by the demote verb, or by a failed or reverted push — its proposal-element sections SHALL be refreshed to the ACTUAL text of the last attempted `proposal.md`, tagged with the change id and the dates raised and demoted, together with the demote reason. They MUST NOT be reset to their pre-proposal aspirational text. Nothing learned while the change was in flight may be lost by falling back to staging.

Conformance SHALL be REQUIRED for any topic staged after this requirement ratifies, and OPT-IN for topics staged before it — rewritten only when a topic is next actively touched. Doc-health SHALL report non-conformance of a pre-existing topic at warning tier as a nudge and MUST NOT treat it as a gate-blocking finding, because a mechanical rewrite of dormant, complete, or externally blocked topics produces busywork without advancing any live decision.

#### Scenario: A topic is staged after ratification
- **WHEN** a new staged topic's primary fragment is authored
- **THEN** it MUST carry the three required sections and the four-sub-field shape for every open question
- **AND** a bare question with no recommended answer MUST be rejected as non-conforming

#### Scenario: A proposal is demoted back to staging
- **WHEN** a topic that reached proposal is demoted
- **THEN** its proposal-element sections MUST carry the last attempted `proposal.md` text, the change id, the raised and demoted dates, and the demote reason
- **AND** they MUST NOT be reset to the pre-proposal text

#### Scenario: An AI adds a section
- **WHEN** a section beyond the required set is added by a human or an agent
- **THEN** it MUST carry an `Added-by:` identity and date

#### Scenario: A topic staged before ratification is untouched
- **WHEN** doc-health evaluates a pre-existing topic that does not conform
- **THEN** it MUST report at warning tier
- **AND** it MUST NOT block a gate on that finding

#### Scenario: The template would require a second selected file
- **WHEN** a proposed change would make a file other than the deterministically selected primary fragment the topic's outline
- **THEN** it MUST be rejected, because the one-path selection rule is preserved rather than extended

### Requirement: Proposal packets carry the lifecycle header
An OpenSpec change packet's `proposal.md`, and EVERY `review/` record under that packet, SHALL be governance documents for the purposes of the controlled status taxonomy and the ratification-citation rule.

Both carry a claim about the document's standing — a proposal says whether it
is `draft` or `ratified`; a review record says what standing its own finding
has, whether that is a ratification, a captured `record` of a review that
happened, or a superseded earlier round. A claim of standing is what the
taxonomy exists to make checkable, and a review record makes one whatever its
subject. The rest of the packet is deliberately NOT ruled here: `tasks.md`,
`design.md`, spec delta files, `supporting-docs/` and `evidence/` are working
files of the change rather than documents making a standing claim, and whether
they are governance documents is a separate question this capability leaves
open.

The two obligations this requirement creates are DIFFERENT in reach, and
conflating them would over-state the rule:

- The **taxonomy** obligation reaches every document named above. A
  `review/` record SHALL carry a `Status:` header drawn from the controlled
  taxonomy, within the lifecycle header window, whatever its subject. A
  review record that is not about a ratification most often carries
  `Status: record`, which is a conforming value and needs nothing further.
- The **ratification-citation** obligation reaches only those documents whose
  status IS `ratified`. A `review/` record carrying any other taxonomy value
  owes no citation, and demanding one of a `record` would be demanding
  provenance for a claim the document does not make.

A `review/` record whose status IS `ratified` and which names its ratifier and
decision date in its own vocabulary SHALL additionally carry a citation in one
of the two sanctioned spellings. Recording the same fact twice is the cost of
having one rule; inventing a third spelling for documents whose whole subject
is ratification would undo the single-rule result the two-spelling sanction
reached.

The pre-existing population SHALL be discharged rather than grandfathered:
this requirement defines NO contract date and NO reduced-severity legacy
class, so a packet carrying no `Status:` header is a current violation
whenever it was authored. Backfilling a header onto an archived packet is an
archived-record edit and takes the route archived-record edits take.

THAT ROUTE IS NOW STATED AND NOT ONLY NAMED. It is *An archived record is
edited only as a bookkeeping correction under a recorded ruling*, and a header
derived from the packet's own record is within that route's bookkeeping class;
it still takes the route's recorded ruling. Where the backfilled file is ALSO a pinned
target, *A change that edits a pinned target re-derives every dependent pin in
the same change* attaches as well and the backfill carries the re-derivation.
The two obligations are independent: clearing the first says nothing about the
second.

Deriving a header is nevertheless authoring, not correcting, and the rule is
bounded accordingly: a `Status:` value and, where that value is `ratified`,
its citation SHALL be derived from the packet's own record — its origin
declaration, its ratification or archive commit, its own task record, or the
index row that announced it. Where the record supports neither, the document
SHALL be reported by name, stating what its record does and does not carry,
and SHALL NOT be given a header the record does not support. A packet whose
own archive record states a decision against carrying a status value keeps
that decision; overturning it takes a ruling naming it, not a backfill pass.

#### Scenario: A proposal declares its standing
- **WHEN** a change packet's `proposal.md` is authored or amended
- **THEN** it MUST carry a `Status:` header drawn from the controlled taxonomy, within the lifecycle header window
- **AND** where that status is `ratified` it MUST carry exactly one ratification citation, in the spelling the citation's own condition of use selects

#### Scenario: A review record records a ratification
- **WHEN** a `review/` document under a change packet records that the change was ratified
- **THEN** it MUST carry `Status: ratified` and one ratification citation in a sanctioned spelling
- **AND** a `Ratifier:` or `Decision date:` header MAY accompany the citation but MUST NOT stand in place of it

#### Scenario: A review record is not about a ratification
- **WHEN** a `review/` document under a change packet records a finding, a disposition, a captured review round, or any other subject that is not the ratification of that change
- **THEN** it MUST still carry a `Status:` header drawn from the controlled taxonomy, within the lifecycle header window, because it is a governance document under this requirement whatever its subject
- **AND** it MUST NOT be required to carry a ratification citation, because the citation rule binds a `ratified` status and this document does not claim one

#### Scenario: A pre-existing packet carries no header
- **WHEN** a proposal packet authored at any date carries no `Status:` header
- **THEN** it MUST be reported as a current violation at full severity, because this requirement defines no contract date and no pre-contract legacy class
- **AND** the remedy MUST be a header derived from that packet's own record, not a reduced severity that leaves the claim unmade

#### Scenario: A record cannot support a derived header
- **WHEN** a packet's own record supports neither a `Status:` value nor, for a `ratified` value, a citation clearing the ratification floor
- **THEN** the document MUST be reported by name together with what its record does and does not carry
- **AND** a header the record does not support MUST NOT be written, because an invented provenance is a worse defect than the missing one it hides
- **AND** where the packet's archive record states a decision against carrying a status value, that decision stands until a ruling names it

#### Scenario: A packet working file carries no lifecycle header
- **WHEN** a change packet's `tasks.md`, `design.md`, spec delta, supporting document, or evidence file carries no `Status:` header
- **THEN** no finding is emitted under this requirement, because this requirement does not reach those files

#### Scenario: A header defect is discharged on an archived packet
- **WHEN** a missing or defective `Status:` header or ratification citation is repaired on a packet under `openspec/changes/archive/`
- **THEN** the repair MUST take the archived-record edit route — a ruling recorded before the edit, a bookkeeping note clearing the neutral minimum or the stricter form the repository's own convention requires, and nothing altered beyond the packet's own standing metadata
- **AND** where the edited file is a pinned target, every dependent pin MUST be re-derived and recorded in the same change
- **AND** a discharge that repairs the header and leaves a dependent pin naming bytes that no longer exist MUST be reported against the change that made it, a repair being incomplete while it holds a pin open

### Requirement: Ratified spec deltas reach the promoted specification
A ratified spec delta SHALL be applied to its promoted
`openspec/specs/<capability>/spec.md` when its change archives, and a
requirement it ADDED or MODIFIED — the requirement itself and every scenario
the delta states under it — SHALL be present in that promoted spec
thereafter; a requirement it REMOVED SHALL be absent.

This is the obligation the archive act has always carried and that nothing
stated. `openspec --strict` validates a delta's SHAPE, never its ARRIVAL, and
the four lifecycle families this capability governs read a packet's headers,
never its bodies — so a ratified requirement could archive and silently never
reach canon while every check reported the corpus healthy.
`docs/archive-record-discrepancies.md` records the instance under FU-DOM-CODEX:
codexFactory's archived `2026-08-08-activate-nightly-sweep-council-clearance`
ratified a MODIFIED requirement carrying six scenarios, the promoted
`merge-master-approval` spec carried the title with two, and the archive commit
never touched that file.

**Archiving a packet is presumed to be ratification of its deltas, and only an
explicit pre-ratification standing rebuts that.** The obligation attaches to
the archive act, so a packet is held to it unless its own `proposal.md`
declares a standing of `draft` or lower — `brainstorm`, `staged`, `draft` —
in which case its spec deltas are archived design evidence rather than
promoted canon and this requirement says nothing about them. A packet that
declares a ratified-or-later standing, declares nothing the taxonomy
recognizes, carries no `Status:` header, or carries no proposal at all is
held to the obligation: a record can disclaim ratification by saying so, and
not by leaving the question unanswered.

THE PRESUMPTION RUNS IN THE CONSERVATIVE DIRECTION. An unexamined ratified
delta is a governance gap that reports itself healthy; a wrongly examined one
is a reported finding that a `draft` header or a recorded disposition
retires. The first spelling of this rule ran the other way, and more than
fifty requirements across two repositories went unexamined for a decision
nobody took — one packet's ratification annotated in prose, three others
simply missing a header.

That is not a new marker invented for the rule: it is the header the corpus
already carries, and
`docs/archive-record-discrepancies.md` C5 is the case it reads.
`2026-06-26-enable-live-openxfactory` was archived with `--skip-specs`,
deliberately retaining four spec deltas as design evidence, and its 2026-08-23
supersession addendum backfilled exactly one line onto it to say so in this
capability's own vocabulary — `Status: draft`, "the honest value this folder
has always supported: never ratified".

**The authority for a requirement is the MOST RECENT archived delta that
touches it, and that one alone.** A ratified change may legitimately rewrite,
rename, or remove what an earlier ratified change stated, and canon carrying
the later text is canon being correct rather than canon drifting. Ordering is
by the archive folder's date; where two archived changes share a date, the
later ARCHIVE ACT is the later statement. A `RENAMED` block retires the title
it names, because `openspec archive` applies RENAMED before MODIFIED.

#### Scenario: A ratified delta never reaches canon
- **WHEN** an archived change carries a spec delta ADDING or MODIFYING a requirement, and its `proposal.md` declares a ratified-or-later standing, declares an unrecognized one, carries no `Status:` header, or does not exist
- **THEN** the promoted `openspec/specs/<capability>/spec.md` MUST carry that requirement by title, and MUST carry every scenario the delta states under it
- **AND** where it does not, health tooling MUST report the gap against the archived delta's own path, naming the promoted spec it failed to reach

#### Scenario: A ratified delta removes a requirement
- **WHEN** an archived ratified change carries a `## REMOVED Requirements` delta
- **THEN** the promoted spec MUST NOT carry that requirement thereafter
- **AND** a requirement still present after its ratified removal MUST be reported

#### Scenario: A deliberate non-promotion is recorded
- **WHEN** a change is archived without promoting its spec deltas, and its own `proposal.md` declares a standing of `draft` or lower
- **THEN** its deltas are archived design evidence and MUST NOT be reported as unpromoted
- **AND** the recorded status is what makes the non-promotion deliberate — a label, a title, or a claim in prose MUST NOT be read as one

#### Scenario: An archive says nothing about its own standing
- **WHEN** an archived change carries a spec delta and its `proposal.md` declares a ratified-or-later standing, declares an unrecognized one, carries no `Status:` header, or does not exist
- **THEN** its deltas MUST be held to this requirement, the archive act being presumed to be ratification
- **AND** an omitted header MUST NOT operate as a recorded non-promotion

#### Scenario: A later ratified change supersedes an earlier delta
- **WHEN** more than one archived ratified change carries a delta touching the same capability and requirement title
- **THEN** only the most recent one SHALL be checked against canon, ordered by archive date and, on a shared date, by the later archive act
- **AND** a requirement title retired by a later `RENAMED` block MUST NOT be reported as missing from canon

### Requirement: A ruling is discharged once
An archived change SHALL be the single discharge of the ruling it carries, and
an archived packet whose spec delta restates the requirement content another
archived packet already ratified SHALL name that packet's change id in its own
`proposal.md`.

This is the neighbour of "Ratified spec deltas reach the promoted
specification", and it is stated separately because the two failures are
invisible to each other. That requirement is unmet when canon is missing what
a ratified delta stated. THIS one is unmet when canon holds exactly what two
independent packets said it should hold — and no comparison against canon can
show it, because canon looks correct. `openspec --strict` validates each
packet's shape in isolation and has no view across packets; the lifecycle
families read headers, and two duplicate discharges both carry impeccable ones.

The instance on record is a NEAR MISS rather than a defect, and the twenty
minutes that made it one are the argument. openxFactory PR #317 and the landed
`2026-08-25-apply-branch-sessions-deltas` both restated the identical 2026-08-01
`add-workbench-branch-sessions` delta — the same git blob — from parallel
sessions. A human closed the second unmerged and recorded why: "One ruling, one
discharge: the landed packet is it."

**NAMING RECORDS LINEAGE, NOT AUTHORITY.** The remedy this corpus prescribes
for an unpromoted delta is a packet that restates the ratified text
BYTE-FAITHFULLY — any edit would be new normative content carried under an old
ratification — so a restatement is lawful and expected. What makes it
traceable, and distinguishes it from a second independent discharge, is that the
restating packet names the packet whose ruling it applies. Naming does not
confer the standing to restate; the ratification that does is the original's,
and a packet claiming standing it lacks is a ratification-citation defect
governed elsewhere in this capability. A packet that restates without naming is
reporting nothing about its own authority — it is leaving the record unable to
tell one ruling from two.

Restatement is judged on CONTENT, not resemblance: identical requirement
bodies, once trailing whitespace is set aside. Revising a requirement is not
restating it, and a rule loose enough to conflate the two would report the
ordinary case of a capability's requirement being rewritten by a later change.

A packet whose own `proposal.md` declares a standing of `draft` or lower is
outside this requirement for the same reason it is outside the promotion
obligation: it claimed no ratification, so it discharged no ruling.

#### Scenario: One ruling reaches the archive twice
- **WHEN** two archived packets carry spec deltas stating the same capability and requirement title with requirement bodies that differ only in trailing whitespace, and neither packet's `proposal.md` names the other's change id
- **THEN** health tooling MUST report the later packet's delta, naming the earlier packet it restates
- **AND** the remedy is to name the restated packet in the proposal or to withdraw the duplicate discharge

#### Scenario: A remedial packet applies a ratified delta
- **WHEN** a packet exists to apply an earlier packet's ratified but unpromoted delta, and restates that delta byte-faithfully
- **THEN** its `proposal.md` MUST name the earlier packet's change id
- **AND** a packet that does so MUST NOT be reported as a duplicate discharge
- **AND** naming the earlier packet MUST NOT be read as establishing that the restating packet had standing to restate

#### Scenario: Two packets independently remedy one gap
- **WHEN** two packets each restate a third packet's ratified delta and each names that third packet, and neither names the other
- **THEN** neither packet's pairing with the original MUST be reported
- **AND** the pairing the two remedials form MUST be reported, one gap having been discharged twice

#### Scenario: A later change revises a requirement
- **WHEN** a later archived change states a requirement title an earlier archived change also stated, with any difference in the requirement body beyond trailing whitespace
- **THEN** the later change is a revision and MUST NOT be reported as a duplicate discharge

### Requirement: A MODIFIED requirement block restates the requirement as canon currently states it
A `## MODIFIED Requirements` block SHALL restate its promoted requirement as
canon states it when the block is written or last amended — carrying every
scenario the requirement keeps and every body clause the change is not
deliberately changing — and any scenario or clause the change deliberately
deletes SHALL be declared by a reserved marker in the delta itself.

**OpenSpec's `MODIFIED` REPLACES a requirement wholesale; it does not merge.**
Whatever the block says is what canon says after the archive act, so a clause
or scenario the block does not restate is a clause or scenario the archive
deletes. Nothing in the gate set notices: `openspec validate --strict` checks a
delta's shape — the heading, the keyword on the first line, at least one
scenario — and never what promotion will do to the document being replaced.

**The defect is a function of time, not of care.** A block written correctly
against the canon of the day goes stale as canon moves under it, and it goes
stale silently, because nothing re-reads it. `add-doxchat-model-intake` was
written on 2026-08-21 against a pre-`02a71d6e` canon and was, on 2026-08-25,
holding the deletion of six body clauses, two scenarios and one reverted
scenario line (issue #351, corrected by PR #358).
`add-release-inventory-drift-check`, `add-promotion-fidelity-check` and
`add-duplicate-packet-check` each restated ONE of the eight scenarios of
`doc-health`'s "Deterministic check families" (issue #329). Every one of the
four was caught by a human, and one was caught only because a byte-for-byte
promotion verification was run by hand at the archive gate.

**Currency is owed continuously, not once at authoring.** The obligation
attaches to the block for as long as the change is active: a change whose
requirement moved in canon after the block was written SHALL bring the block
forward before it archives. This is what makes the rule enforceable at
authoring time rather than only at an archive gate, and it is the half that the
ordinary reading of "write a correct delta" misses.

**A deliberate deletion is legitimate, and it SHALL be declared by form rather
than by prose.** Removing a scenario or a clause is a normal governance act;
removing one by not mentioning it is not. The declaration SHALL be a reserved
marker paragraph inside the MODIFIED block, naming each deleted unit as a
CommonMark code span: `**Removed from canon by <change-id> (<YYYY-MM-DD>):**`
for a deletion, and
``**Merged into `<destination scenario title>` by <change-id> (<YYYY-MM-DD>):**``
where two scenarios legitimately become one — the destination being where the
superseded scenarios went rather than a unit the marker names. A unit that
itself contains backticks is fenced with a longer run of them, as CommonMark
provides. Naming a scenario title declares the bullets that scenario carried
removed with it — but only in a genuine removal, where the block adds no
scenario title canon does not already carry; where it adds one the shape is a
retitle, `Merged into` is the instrument, and the bullets must be carried or
named one at a time. A marker is not itself a unit anything later has to
restate. The marker is deliberately a NEW reserved form and NOT the corpus's
existing dated bold note, because every such note in
the corpus today records a caught near-miss and a restoration rather than a
deletion — one of them naming seven scenario titles in backticks as restored —
so a rule that read deletion out of prose would misread faithful restatements
as declarations of loss. A recorded disposition in the aggregation checkout's
`health/dispositions.yaml` is the fallback for a delta that is ratified and
cannot be re-authored; nothing else declares a deletion.

**Where two active changes write one requirement, `release-realization` already
governs the order and this requirement does not restate or widen it.** That
capability's "Ordered deltas and branch vocabulary" requires that a proposal
modifying a requirement already modified by an active RATIFIED change
references that change and declares its deltas relative to that change's
outcome; the reference is read as that change's id occurring as a whole token
in the declaring change's own `proposal.md`. This requirement adds only the
consequence for currency, in two parts. **The declaration IS the ordering.**
The change that declares itself relative to a sibling is the later writer —
there is nothing else to decide, and no date, folder name or commit timestamp
SHALL be consulted to decide it. And a block so declared is measured against
THAT sibling's outcome rather than against canon, so it carries the sibling's
additions as well as canon's. Exactly one of two active ratified writers
declares: neither declaring leaves the ordering unstated, which is reportable,
and both declaring states a cycle, which decides nothing.

#### Scenario: A block omits a scenario the requirement keeps
- **WHEN** an active change's `## MODIFIED Requirements` block restates a promoted requirement and does not restate a scenario that requirement currently carries
- **THEN** the block MUST be brought forward to carry that scenario, or the deletion MUST be declared by marker in the delta
- **AND** health tooling MUST report the omission against the active delta's own path, before the change archives

#### Scenario: Canon moves under a long-lived active change
- **WHEN** a requirement is amended in canon after an active change's MODIFIED block for it was written
- **THEN** the block MUST be brought forward before that change archives
- **AND** the passage of time MUST NOT be read as an excuse: the obligation attaches to the block for as long as the change is active

#### Scenario: A deletion is deliberate
- **WHEN** a change intends to delete a scenario or a body clause the promoted requirement carries
- **THEN** the delta MUST carry a reserved marker naming that unit as a code span
- **AND** a declared deletion MUST NOT be reported as a currency defect
- **AND** a marker naming a unit the block still carries MUST NOT be read as declaring anything

#### Scenario: Two active changes modify one requirement
- **WHEN** a proposal modifies a requirement that an active ratified change already modifies
- **THEN** the later proposal MUST reference the earlier change and declare its deltas relative to that change's outcome, exactly as `release-realization` requires and with no wider obligation added here
- **AND** that declaration MUST be what establishes which writer is later, no date, folder name or commit timestamp being consulted
- **AND** the declaring block MUST carry the earlier change's additions as well as canon's, because whichever archives last is the text canon keeps
- **AND** two such changes where neither declares MUST be reported, the ordering being unstated rather than merely unrecorded

#### Scenario: A MODIFIED block names a requirement canon does not carry
- **WHEN** a MODIFIED block names a capability and requirement title the promoted specification does not carry
- **THEN** the title MUST resolve to a requirement an active sibling change ADDS or RENAMES
- **AND** a title resolving to neither canon nor an active sibling MUST be reported, a block modifying nothing being a block whose promotion silently adds text nobody reviewed as an addition

### Requirement: A MODIFIED block over a requirement no promoted specification carries declares its basis by marker
A `## MODIFIED Requirements` block SHALL declare its basis by a reserved marker
inside that block where the requirement it names is one the promoted
specification does not carry and an active change ADDS or RENAMES to that
title, naming the change whose addition or rename the block is written over.

**THE SHAPE IS LAWFUL, AND IT IS THE DECLARATION THAT MAKES IT SO.** Modifying
a requirement a sibling is still adding — or still renaming a promoted
requirement into, the two basis forms being one basis on the same terms wherever
this corpus reads them — is a legitimate and frequent act in a
corpus where changes are long-lived: the successor arrives before the
predecessor archives, and asking it to wait would be asking governance to run at
the speed of the slowest packet. What is not lawful is doing it silently. The
obligation to order the two writers belongs to `release-realization` ("Ordered
deltas and branch vocabulary"), which this requirement neither restates nor
widens; the obligation this requirement adds is that the pairing be declared
where a reader and a checker can both find it, per requirement rather than per
packet.

**THE MARKER IS A THIRD RESERVED FORM, recognized by form and never by prose**,
taking its place beside the two this capability already defines and read under
the same rules: one paragraph inside the MODIFIED block, read after the same
whitespace normalization every other unit gets, and of marker form only where it
begins with the prefix COMPLETE. The form is
``**Modified over `<basis change-id>`'s addition by <change-id> (<YYYY-MM-DD>):**``
followed by ` — <reason>`. The basis change-id is written as a code span, as
every change-id this capability's markers name already is.

**THE ` — <reason>` TAIL IS REQUIRED FOR THE DECLARATION TO BE COMPLETE, AND A
MARKER WITHOUT IT IS DEFECTIVE RATHER THAN ABSENT.** The separator SHALL be
present and the reason after it SHALL be NONEMPTY, the reason being THE WHOLE
TAIL AFTER ` — ` and not merely what follows some code span inside it — this
form naming no units, there is nothing in the tail to measure it from behind.
A paragraph carrying the COMPLETE PREFIX with no
separator, or with a separator and nothing but whitespace after it, SHALL be
read as a marker OF THIS FORM whose declaration is DEFECTIVE, and SHALL be
reported as such. It is NOT a non-marker: recognition is the prefix and STOPS
THERE, deliberately and on the same reading the `by` identifier below already
has — a paragraph that fails a requirement of the form is a MARKER THAT FAILS
IT, and treating the missing tail as a failure to RECOGNIZE would drop the
paragraph to an ordinary body unit and leave the block described as carrying no
declaration at all, which is the absent-marker remedy handed to a block that
plainly carries one. And it is not silently complete either: a declaration this
requirement calls incomplete SHALL NOT promote as a complete one.

**THE TAIL IS REQUIRED OF THIS FORM ALONE, and the difference is the structural
one this requirement keeps returning to.** The two existing forms carry their
whole declaration in the UNITS THEY NAME — what was removed, or where it went —
so a reason there is prose added to a declaration already complete, and neither
form requires one. THIS FORM NAMES NO UNITS. Its prefix states a bare relation
between two documents and nothing more, so the reason is the only place the
declaration says WHY this text was written over that addition, and it is also
the ONLY CLAUSE the unratified disclosure stated below can be carried in. A
marker with no reason therefore discloses nothing and CAN disclose nothing: the
disclosure obligation is not vacuously satisfied by an absent clause and is not
waived by it — it is unreadable, and what such a marker's author must be told is
that the reason is missing rather than that a word is.

**THE WORD `addition` IN THAT PREFIX IS FIXED PROSE, NOT A CLAIM ABOUT THE
BASIS'S BLOCK KIND.** The form is recognized by a COMPLETE prefix, so its literal
text is a token a parser matches rather than a description a reader must verify;
it names the RELATION the marker declares — this block rests on what that change
writes into canon — and a basis that RENAMES a promoted requirement to the title
is declared by the same unchanged form. Spelling a second prefix for the rename
case would make one relation two shapes, two parse branches and two class-map
entries for one remedy, which is what this capability's reserved forms exist to
avoid.

**AT MOST ONE MARKER OF THIS FORM SHALL STAND IN ONE BLOCK — ONE PAIRING, ONE
DECLARATION.** This capability's other two reserved forms carry no such bound
and SHALL keep none, and the difference is the structural one this requirement
states below: they NAME UNITS, so their declarations ACCUMULATE — two `Removed from
canon by` markers declare two sets of removed units, both are read, and the
corpus's reading voids a marker per NAME rather than wholly — so a bound on
their count would be a bound on how many units one change may lawfully remove,
which no capability has ever asked for. This form names no units. It declares
ONE RELATION between two documents, so a second marker in one block does not add
to the first: it states a SECOND BASIS for one text, and a block resting on two
bases rests on neither, no reader being told which addition the text was written
over. A block carrying more than one marker of this form SHALL be reported, with
the same remedy a wrong basis has — withdraw every declaration but the one that
is true.

**THE `by` IDENTIFIER SHALL BE THE CHANGE THAT CARRIES THE BLOCK, and it is
VALIDATED rather than merely resolved.** The identifier written after `by` SHALL
EQUAL the id of the change whose delta carries the marker's block, on the reading
this capability's other two reserved forms already have: `Removed from canon by`
and ``Merged into `<title>` by`` name the change that PERFORMED the declared act,
and the change performing this declaration is the one writing the block. A marker
whose basis is right and whose `by` names an unrelated change is NOT a lesser
defect than a wrong basis — it is a FALSE PROVENANCE, sending every later reader
who follows the identifier to a packet that declared nothing, while the block
promotes looking declared. BOTH halves are therefore checked and a marker failing
either SHALL be reported: the obligation is stated HERE, where the form is
defined, and `doc-health` is where the reading of it is enforced, neither being a
substitute for the other.

**A PAIRED CONVERSION DOES NOT MOVE THE IDENTIFIER, and needs no exception to
this rule.** `release-realization` provides that a conversion of the block to
`## ADDED Requirements`, lawful only as a paired act, RETAINS this marker as
provenance. The block's FORM changes and its CARRIER does not — the converting
change is the same change that wrote the block — so the retained marker's `by`
identifier is still the carrying change's own id, and the retention stands
without narrowing or widening what this paragraph requires.

**THIS FORM NAMES NO UNITS, and that is the difference that matters.** The two
existing forms name units they declare removed; this one names a DOCUMENT PAIR
and declares nothing about carriage, because in this shape there is nothing to
compare — no promoted requirement exists to compare against. A marker of this
form SHALL NOT suppress any unit, SHALL NOT be read as naming any unit, and
SHALL NOT be reported under the rule that reports a marker naming a unit the
block still carries. Like every marker, it is NOT itself a carriage unit in
either direction, so no later block restates it and dropping it declares
nothing.

**THE PROPOSAL'S CROSS-REFERENCE IS STILL OWED AND IS NOT A SUBSTITUTE.**
`release-realization` requires the modifying proposal to reference the change it
is declared relative to, and that reference is a fact about the two CHANGES. The
marker is a fact about the two BLOCKS: a proposal may name a sibling for a dozen
reasons and may carry several MODIFIED blocks, so a change-level mention cannot
say which requirement rests on which sibling. Both are required and they are
different declarations.

**A BASIS THAT IS NOT RATIFIED SHALL BE DECLARED AS SUCH AND NOT AS CANON.**
`release-realization` owns the ordering obligation and this requirement neither
states nor widens it. Where the declared basis is a change that is not ratified,
the declaring block rests on text no authority has accepted; the marker is still
owed, the reason clause SHALL DISCLOSE that the basis is unratified, and the
modifying change SHALL NOT describe the requirement it modifies as settled.

**THE DISCLOSURE HAS A FORM, because an obligation only a reader can check is an
obligation nothing checks.** The reason clause discloses by CARRYING THE WORD
`unratified` — in prose or as a code span, this form naming no units either way
— read case-insensitively after the same whitespace normalization the marker
itself is read under. The sentence it sits in stays the author's to write, and
THAT A SENTENCE EXISTS AT ALL IS THE TAIL RULE'S OBLIGATION AND NOT THIS ONE'S:
a marker carrying no reason has already failed the form, and its defect is the
missing tail rather than a missing word — this disclosure is a reading OF a
reason clause and an absent clause is nothing to read. This
is the bargain every reserved form in this capability already strikes: the FORM
is what a checker reads and the PROSE is what a reader reads, and asking a
checker to decide whether a sentence discloses would be the prose rule this
whole marker design refuses. The obligation is stated HERE, where every reserved
marker in the corpus is defined; `doc-health` is where the reading of it is
enforced, and neither is a substitute for the other.

**AND THE DISCLOSURE WARNS THE READER; IT DOES NOT OPEN THE GATE.**
`release-realization`'s archive hold keys on the UNPROMOTED TITLE rather than on
the basis's standing, so it reaches an unratified basis on exactly the terms it
reaches a ratified one — the basis archives first, and where it is unratified it
ratifies and archives first. A marker carrying the word `unratified` has
therefore DISCHARGED THIS REQUIREMENT AND NOTHING ELSE. It SHALL NOT be read as
lifting that hold, as consenting to the modifying change's archive, or as making
the requirement it is declared over settled: a pairing may be perfectly declared
and still be unarchivable, those being two questions about one pairing answered
in two capabilities. Reading the disclosure the other way would make this
requirement's own discharge the escape from an obligation it does not state — a
marker form buying an archive act, which is the one thing no reserved form in
this capability has ever done.

#### Scenario: A block is written over a sibling's addition
- **WHEN** an active change's `## MODIFIED Requirements` block names a requirement the promoted specification does not carry, and an active change ADDS or RENAMES to that title
- **THEN** the block MUST carry a marker of the reserved `Modified over` form naming that change as a code span, and naming as its `by` identifier the change whose delta carries the block
- **AND** the change's own `proposal.md` MUST still reference that change as `release-realization` requires, the two declarations being about different things

#### Scenario: The marker names a change that does not add the requirement
- **WHEN** a `Modified over` marker names a change that neither ADDS nor RENAMES to the block's capability and requirement title
- **THEN** the declaration MUST be reported, a basis that does not exist being worse than an undeclared one because it stops the next reader looking

#### Scenario: The marker's `by` identifier names a change other than the carrier
- **WHEN** a `Modified over` marker names as basis a change that does ADD or RENAME to the block's capability and requirement title, and its `by` identifier is an id other than that of the change whose delta carries the block
- **THEN** the declaration MUST be reported, a marker naming the right basis under the wrong author being a false provenance rather than an incomplete declaration
- **AND** a marker whose `by` identifier IS the carrying change's own id MUST NOT be reported on that ground, the identifier being validated against the carrier rather than merely resolved
- **AND** a marker RETAINED as provenance through a paired conversion MUST NOT be reported on that ground either, the converting change being the change that carried the block

#### Scenario: A block carries two markers of this form
- **WHEN** one `## MODIFIED Requirements` block carries more than one paragraph of the reserved `Modified over` form
- **THEN** the block MUST be reported, one pairing admitting one declaration and a second marker stating a second basis for one text rather than adding to the first
- **AND** the remedy MUST be to withdraw every such marker but the one that is true, no reading of two bases making the block rest on either
- **AND** the two unit-naming forms MUST NOT be read as bounded by this rule, their declarations accumulating because each names its own units

#### Scenario: The marker carries the prefix and no reason
- **WHEN** a paragraph inside a `## MODIFIED Requirements` block carries the complete `Modified over` prefix and is not followed by ` — ` and a nonempty reason
- **THEN** the paragraph MUST still be read as a marker of this form, recognition ending at the prefix, and its declaration MUST be reported as defective rather than accepted
- **AND** it MUST NOT be read as a non-marker or as an ordinary body unit, a block whose declaration is defective being differently placed, and differently repaired, from one carrying no declaration at all
- **AND** a separator followed by nothing but whitespace MUST be treated as carrying no reason, an empty reason declaring exactly what an absent one does
- **AND** the disclosure this requirement asks of an unratified basis MUST NOT be read as satisfied by that absence, nor as waived by it, there being no clause to read it in
- **AND** the two unit-naming forms MUST NOT be read as acquiring this obligation, their declarations being complete in the units they name

#### Scenario: The marker is read as declaring a deletion
- **WHEN** a block carries a `Modified over` marker and omits a unit
- **THEN** the marker MUST NOT be read as declaring that omission, this form naming no units
- **AND** the marker MUST NOT itself be reported as a marker naming a unit the block still carries, that rule reaching only the forms that name units

#### Scenario: The declared basis is not ratified
- **WHEN** the change whose addition a block is written over carries a status other than `ratified`
- **THEN** the marker MUST still be carried and its reason clause MUST state that the basis is unratified, by carrying the word `unratified`
- **AND** a reason clause omitting that word MUST NOT be read as disclosing it however the rest of the sentence is worded, this disclosure being read by form like every other part of this marker
- **AND** the disclosure MUST NOT be read as lifting `release-realization`'s archive hold, which keys on the unpromoted title rather than on the basis's standing and reaches an unratified basis on the same terms — a block may be lawfully declared and still be unarchivable
- **AND** this requirement MUST NOT be read as stating that hold or as widening it, the marker being what a delta CARRIES and the order of the two archives being what `release-realization` owns

#### Scenario: One change both adds and modifies one requirement
- **WHEN** a single change carries both an `## ADDED Requirements` block and a `## MODIFIED Requirements` block for one capability and requirement title
- **THEN** the delta MUST be reported, a change modifying its own unpromoted addition having written two texts for one requirement where the second is simply the first
- **AND** a `Modified over` marker naming the change itself MUST NOT be read as curing it
- **AND** a change that RENAMES a promoted requirement to that title and modifies it in one delta MUST NOT be reported on this ground, that shape being the rename-and-amend one `doc-health`'s promoted resolution order resolves against canon under the OLD name (`openspec/specs/doc-health/spec.md:1568-1574`, with the scenario at `:1783-1786`), a `## RENAMED Requirements` block carrying a pair of titles rather than a second text

### Requirement: An archived record is edited only as a bookkeeping correction under a recorded ruling
A file under `openspec/changes/archive/` SHALL be edited ONLY as a
lifecycle-header or bookkeeping correction, under a ruling recorded BEFORE the
edit, and carrying a bookkeeping note; every other edit of an archived byte
SHALL be refused.

**THE NOTE HAS A NEUTRAL MINIMUM, BECAUSE THE PROMOTING REPOSITORY HAS NO
CONVENTION OF ITS OWN.** An earlier spelling of this requirement said "the
bookkeeping note the editing repository's own archived-packet convention already
requires", which is unsatisfiable where no such convention exists — and
openxFactory, the repository this capability is promoted in, HAS NONE. Only
OpsxFactory has written one down. A rule whose note obligation is delegated
entirely to local conventions is absent exactly where no local convention
exists, which would leave the loosest repository in the estate the one that
promoted the rule.

The minimum is therefore stated here: a DATED LINE in the edited file's OWN
lifecycle-header block — the block every governance document already carries
under *Controlled document status taxonomy* — of the form

`Edited (bookkeeping): <UTC date> by <change-id> — <edit class>`

A repository's own convention MAY be stricter and MUST NOT be absent;
OpsxFactory's note on the archived change's `tasks.md` is such a stricter form
and is unaffected. The note sits in the lifecycle header ON PURPOSE: that block
is the one part of an archived file this requirement already permits the edit to
touch, so recording the edit cannot itself become an edit the rule forbids.

**AN ARCHIVE IS NOT MERELY HISTORY, AND THAT IS WHY THIS RULE EXISTS.** Two
things in this corpus read archived bytes as CURRENT. *Ratified spec deltas
reach the promoted specification* makes "the MOST RECENT archived delta that
touches it, and that one alone" the authority for a promoted requirement — so
editing an archived delta edits the standard canon is checked against, with no
proposal, no review, and no ratification anywhere in the act. And archived
files are content-address TARGETS: consent instruments, evidence manifests and
digest inventories name them by locator and `sha256`, so an archived byte
moving silently breaks a pin somewhere else. An archived packet is a RECORD in
the taxonomy's own sense — captured once — and the whole value of a record is
that it says today what it said when it was captured.

**WHAT COUNTS AS BOOKKEEPING, AND WHAT DOES NOT.** A bookkeeping correction
adds or repairs the packet's OWN standing metadata and nothing the packet
ASSERTS: a `Status:` header or ratification citation derived from the packet's
own record; a corrected index row, path or cross-reference naming the packet; a
DATED AMENDMENT NOTE APPENDED BESIDE STALE TEXT THAT IS KEPT. It is NOT a spec
delta's requirement or scenario text, a task record or its tick state, a
decision, a measurement, a number, an evidence digest, or the deletion of any
of these. THE TEST IS WHETHER THE EDIT CHANGES WHAT THE ARCHIVED RECORD
ASSERTS, and it is deliberately a test of effect rather than a list of
filenames: `proposal.md` carries both classes, and a rule keyed to paths would
license a substantive rewrite inside a file the list called safe. Where the
edit does change an assertion, the route is a NEW change that supersedes, and
never an edit in place.

**THE RULING IS RECORDED BEFORE THE EDIT, AND THE NOTE IS NOT THE RULING.**
The recording SHALL name the ruler, the date, and the class of edit authorized,
and SHALL be resolvable — a ruling comment, a disposition, a review record, or
an approving change. A bookkeeping note written into the packet says WHAT was
changed; the ruling says THAT IT MAY BE. A convention satisfied by the note
alone authorizes every edit its author believed was bookkeeping, which is the
same thing as authorizing every edit.

**THE NARROW PERMISSION IS NOT A PRECAUTION — THE PERMISSIVE READING WAS TRIED
AND MEASURED.** OpsxFactory's `docs/packet-lifecycle-headers.md` § *Editing an
archived packet*, ratified 2026-08-24, permitted an archived-packet edit on a
bookkeeping note alone. On that same UTC day commit `57fd9fd2` ("Discharge all 55
lifecycle-header defects in the OpenSpec scan set", 63 files) wrote SIXTEEN
files under that repository's archive tree under it, inserting one `Ratified:`
line per target, and broke THREE executed consent instruments' `custody.sha256`
— one of them in a change directory that has never been archived, which is why
the class is pinned-target integrity and not archiving. It went thirteen days
unnoticed. Two packets in that repository had read `FR-072` as forbidding
archive writes; that was one feature's close-time fence, not a general rule, so
there was no general rule to break — the permissive convention was the whole of
the governance. This requirement is that general rule, stated estate-wide, and
its domain-realized twin is OpsxFactory's `govern-archived-record-edits`, which
states it over that repository's archive tree at the repository's own altitude.

**A REPOSITORY MAY BE STRICTER AND MAY NOT BE LOOSER.** A DomainxFactory's
local archived-packet convention SHALL be read as an ADDITION to this
requirement. A convention that permits an edit this requirement refuses is
superseded on that point by force of this rule, and remains in force for
everything it says that this rule does not reach.

#### Scenario: A lifecycle-header defect is discharged on an archived packet
- **WHEN** a change repairs a missing or defective `Status:` header or ratification citation on a file under `openspec/changes/archive/`
- **THEN** a ruling authorizing the class of edit MUST be recorded before the edit, naming ruler, date and class, and resolvable from the change
- **AND** the neutral minimum MUST be present — a dated `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line in the edited file's own lifecycle-header block — whatever else the editing repository requires
- **AND** a stricter local convention MAY require a further note and MUST NOT stand in place of the minimum, a local form ADDING to the minimum rather than substituting for it
- **AND** nothing beyond the packet's own standing metadata may be altered in the same act

#### Scenario: An edit would change what an archived record asserts
- **WHEN** a proposed edit to an archived file would change a requirement or scenario, a task record or its tick state, a decision, a measurement, a number, an evidence digest, or would delete any of these
- **THEN** the edit MUST be refused whatever file it sits in and however small it is
- **AND** the correction MUST take the form of a new change that supersedes the archived record, the archived bytes staying as captured

#### Scenario: An archived-packet edit carries a note and no ruling
- **WHEN** an archived file is edited under a local convention satisfied by a bookkeeping note alone, with no ruling recorded before the edit
- **THEN** the edit MUST be reported, the note recording WHAT changed and never THAT IT MAY
- **AND** the report MUST name the archived files the change wrote, so the scope of an unruled edit is visible rather than inferred

#### Scenario: The editing repository has no archived-packet convention
- **WHEN** an archived-record edit is made in a repository that has written no archived-packet convention of its own
- **THEN** the neutral minimum applies unchanged — a dated `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` line in the edited file's own lifecycle-header block
- **AND** the absence of a local convention MUST NOT be read as the absence of a note obligation

#### Scenario: A local convention is more permissive than this requirement
- **WHEN** a repository's own archived-packet convention permits an edit this requirement refuses
- **THEN** this requirement governs and the convention is superseded on that point
- **AND** the convention MUST be amended by a DATED AMENDMENT that keeps its stale text rather than by a rewrite, an archived-record rule that erased its own history being self-refuting

### Requirement: A change that edits a pinned target re-derives every dependent pin in the same change
A change that edits a PINNED TARGET SHALL re-derive every dependent pin and
SHALL RECORD the re-derivation in the SAME change, by the rule that pin's own
family declares. A PINNED TARGET is any file that an in-repo content-address pin
names, whether that file is ARCHIVED OR LIVE.

**THE REACH IS PINS, NOT THE ARCHIVE.** This requirement and its neighbour
above are stated separately because their failures are invisible to each other.
That one is unmet when an archived record is edited outside the bookkeeping
class. THIS one is unmet when a pin's target moves and the pin does not — and
the target need never have been archived. In the measured case one of the three
broken pins named a change directory that has never archived at all, so a rule
scoped to the archive tree would have left it broken while reporting itself
satisfied.

**THE OBLIGATION THIS REQUIREMENT CREATES IS THE RECORDING; THE DETECTION IS
THE GATES'.** Nothing here asks an author to notice a broken pin unaided, and a
rule that did would be a rule discharged by diligence. What this requires is
that a change which knows it is editing a pinned target carries the
re-derivation. Making an unrecorded edit VISIBLE is the work of running gates —
the pre-archive citation gate and the content-address integrity gate in
OpsxFactory are the first two — and a repository that has no such gate owes
this obligation exactly as much, with nothing but review to catch a breach.

**PER FAMILY, BY THE FAMILY'S OWN RULE, WHICH THE FAMILY MUST DECLARE.**
Re-derivation is not one act: a consent instrument's custody pin, an evidence
digest, a plan-acceptance desired-state reference and a contract-bundle digest
each re-derive differently and record differently. A family's rule SHALL be
declared either in the declaring repository's content-address register OR in
the neutral contract that owns the family — both homes are real and the
distinction is not cosmetic: the consent family's rule is a property of the
INSTRUMENT SCHEMA and lives in the contract wherever the instrument is held,
while a repository-local family's rule has no contract to live in. For consent
instruments the rule is the structured `custody_rederivations[]` entry proposed
by `add-consent-custody-rederivation-record`, which is a CONTRACT home;
OpsxFactory's `add-content-address-integrity-gate` proposes the estate's first
REGISTER home.

**A FAMILY THAT DECLARES NO RE-DERIVATION RULE HAS NOT EARNED A PIN — AND THE
CONSEQUENCE ARRIVES WITH THE DECLARATION, NOT WITH THIS REQUIREMENT.** Until a
family has declared its rule, an edit of that family's pinned target SHALL be
REPORTED — naming the family, the pinned target, and the register or contract
that owes the rule — and SHALL NOT be refused on that ground. It becomes a
REFUSAL for that family on the day that family declares, and thereafter an
ad-hoc re-derivation performed for the occasion is not accepted in place of the
declared rule, because "re-derive by whatever means" is a promise nobody can
check and nobody can repeat.

**THE TRANSITION IS NOT A SOFTENING; IT IS WHAT KEEPS THE RULE FROM FREEZING
THE ESTATE ON THE DAY IT LANDS.** Measured at this packet's authoring: NO
family anywhere in the estate has a declared re-derivation rule. The consent
family's is PROPOSED and not declared — the contract still reads
`contract_schema_version: 2`, the schema carries no `custody_rederivations`
property, and all 46 boxes of the proposing packet are unticked. The register
home does not exist at all: `models/content-address-families.yaml` is absent
from OpsxFactory's `main` AND from the branch that proposes it, where it is
task 2.1. A refuse-on-landing reading would therefore refuse EVERY pinned-target
edit in the estate from the moment this requirement is promoted — including the
routine lifecycle-header discharge that the neighbouring requirement and
*Proposal packets carry the lifecycle header* both require to be performed. A
rule whose first act is to forbid the corrective work it exists to govern is a
rule that will be worked around rather than followed.

**"IN THE SAME CHANGE" IS THE WHOLE OF IT.** A re-derivation deferred to a
successor is a broken pin with a promise attached, and the promise is not what
the pin's consumer reads. Where the dependent pin lives in another repository,
the same change SHALL record the owed consumer act by name, and the consumer's
re-pin is that repository's change — deferral ACROSS a boundary is legitimate
because the bytes are not in one tree; deferral WITHIN one is not.

**AN EDIT THAT CANNOT RE-DERIVE ITS DEPENDENTS MAY NOT LAND.** Where a
dependent pin cannot be re-derived — the target cannot be resolved through its
declared mapping, or the re-derivation does not verify — the correct outcome is
a REFUSAL naming what could not be derived, never an edit that lands with the
question open. Converting "cannot tell" into "fine" is precisely the state the
measured case sat in for thirteen days. **An UNDECLARED RULE is deliberately
NOT in that list**: it is not a failed re-derivation but an absent obligation,
it is the state of every family in the estate today, and it takes the REPORT
above rather than a refusal until that family declares.

#### Scenario: A pinned target's bytes change
- **WHEN** a change edits a file that an in-repo content-address pin names, whether that file is archived or live
- **THEN** every dependent pin MUST be re-derived and the re-derivation MUST be recorded in that same change, by the rule the pin's family declares
- **AND** a change that edits the target and moves no dependent pin MUST be reported against its own commit

#### Scenario: A pinned target's path changes
- **WHEN** a pinned target is moved or renamed and its bytes are unchanged
- **THEN** the dependent pin's locator MUST be re-derived in the same change and the record MUST say that the bytes did not change
- **AND** an unchanged digest MUST NOT be read as an unchanged pin, a locator being half of a content address

#### Scenario: A pin's family has not yet declared a re-derivation rule
- **WHEN** a change edits a pinned target whose family has declared no re-derivation rule, in either home
- **THEN** the edit MUST be REPORTED, naming the family, the pinned target, and the content-address register or neutral contract that owes the rule
- **AND** it MUST NOT be refused on that ground, an absent obligation being a different fact from a failed re-derivation
- **AND** the report MUST NOT be read as a re-derivation having been performed

#### Scenario: A family has declared its rule and an edit does not follow it
- **WHEN** a family has declared its re-derivation rule, in its register or in the neutral contract that owns it, and a change edits one of its pinned targets without following that rule
- **THEN** the edit MUST be refused
- **AND** an ad-hoc re-derivation performed for the occasion MUST NOT be accepted in place of the declared rule

#### Scenario: A dependent pin lives in another repository
- **WHEN** the pin depending on the edited target is held by a consuming repository
- **THEN** the editing change MUST record the owed consumer re-pin by name, repository and instrument
- **AND** the consumer's own change MUST carry the re-derivation, cross-boundary deferral being legitimate exactly because the bytes are not in one tree

#### Scenario: A dependent pin cannot be re-derived
- **WHEN** a dependent pin's target cannot be resolved, or the re-derivation does not verify
- **THEN** the change MUST be refused, naming the pin and what could not be derived
- **AND** the edit MUST NOT land on the reading that an underivable pin is an unaffected one
