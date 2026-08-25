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

**Ratification citation.** A `ratified` header SHALL name its ratification. A bare, uncited `Status: ratified` is a violation whatever else the document says, because the header asserts an approval the document does not point at. TWO citation spellings are sanctioned, and they are not interchangeable — each has a condition of use, and the condition is what decides which one is correct:

- `Ratified by: <change>` is the PRIMARY spelling and SHALL be used wherever an approving OpenSpec change exists to name. The named change IS the citation.
- `Ratified:` is the RECORD-CITING alternative and SHALL be used only where no approving OpenSpec change exists to name — an in-session ruling, a disposition, an `.openspec.yaml` approval pair, an archive or ratification commit, or another durable record. Reaching for the primary spelling in that situation would mean naming a change that does not exist.

A document SHALL carry exactly one ratification citation, in one of the two spellings. The count is ONE TOTAL across both spellings: a document MUST NOT carry one of each, and MUST NOT carry the same spelling twice. Two lines each claiming to name the ratification say nothing about which is current, whether or not they are spelled alike.

**The three-way floor on the record-citing form.** A `Ratified:` citation SHALL name at least one of three things: an approver, a date, or a resolvable record path. Naming none of the three is a finding, because such a line asserts a ratification nothing can be checked against — the bare uncited header's defect, differently spelled. The floor is deliberately a floor and not a fixed field set: the corpus's honest citations name different subsets (approver plus date plus a verbatim instruction; date plus a record pointer with no approver named; date alone where the record names no ratifier), and a rule demanding all three would force the invention of provenance the record does not carry, which is the failure mode this rule exists to prevent.

The floor SHALL apply to the `Ratified:` form only and SHALL NOT be applied to `Ratified by:`, whose named change is itself the resolvable record. A governed document whose `Ratified by:` line names its approving change and nothing else is correct as written and MUST NOT be reported.

A ratification citation is read in the document's lifecycle header, alongside the `Status:` header it justifies. Prose elsewhere in a document that begins with the same word — a section-level decision label, a sentence starting "Ratified together with…" — is body text and is NOT a ratification citation.

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
`.openspec.yaml`, fixed when the proposal is created and unchanged for the
life of the change. A `staged` origin carries `kind: staged`, a durable
`id` of the form `<repo>:staging:<topic-slug>`, and a `path` naming the
original repository-relative staging folder; at the proposal transition the
staged folder MUST contain a document whose `Staging ID:` equals
`origin.id`. An `ad_hoc` origin carries `kind: ad_hoc`, a durable `id` of
the form `<repo>:adhoc:<date>-<sequence-or-slug>`, and required `reason`,
`approved_by`, and `approved_on` fields. Ad-hoc status is an explicit,
approved exception — it MUST NOT substitute for staging when organized
source material exists, and a proposal MUST NOT declare both origin kinds.
Durable ids remain valid after the staging folder moves, is compressed, or
is removed; `origin.path` is the historical record of the transition
source, not a live link.

#### Scenario: A staged proposal is created
- **WHEN** an OpenSpec change is created from a staged topic
- **THEN** its `.openspec.yaml` MUST declare `kind: staged` with the topic's durable id and original staging path
- **AND** the staged folder MUST contain, at transition, a document whose `Staging ID:` equals the declared id

#### Scenario: An ad-hoc proposal is created
- **WHEN** an OpenSpec change is deliberately created without a staging source
- **THEN** its `.openspec.yaml` MUST declare `kind: ad_hoc` with a durable id, the reason, the approving authority, and the approval date
- **AND** supporting evidence MAY still live under `supporting-docs/` but MUST NOT claim a fabricated staging source

#### Scenario: The proposal gate rejects a malformed origin
- **WHEN** a proposal's origin is missing, declares an unknown kind, declares both kinds, carries a staged id or path that does not resolve before transition, disagrees with the staging header or support manifest, or lacks ad-hoc reason or approval provenance
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

