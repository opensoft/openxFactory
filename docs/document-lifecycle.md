# xFactory Document Lifecycle

Status: standard
Kind: process
Repository context: openxFactory
Backed by: [openspec/specs/document-lifecycle/spec.md](../openspec/specs/document-lifecycle/spec.md) (promoted from the archived add-document-lifecycle-vocabulary change)
Purpose: define the canonical lifecycle for governance documents, the
controlled `Status:` and `Kind:` header taxonomy, and the gates between
states, for openxFactory and every DomainxFactory.

## The Lifecycle Spine

Governance content moves through one canonical lifecycle:

```text
captured     free-form thinking exists (ideation/brainstorm/)
organized    pieces identified, deduped, targeted (ideation/staging/,
             candidate registers)
proposed     an OpenSpec change exists
             selected source material lives with that active change
ratified     the change is approved
implemented  the artifact (doc, schema, validator, template) is built
promoted     canonical — the contract/spec layer owns it
adopted      consumers re-pinned; local duplicates retired
superseded   replaced by a later delta, provenance retained
retired      withdrawn without replacement
```

`rejected` and `deferred` are exits from any pre-promoted state. Devolution
(neutral to domain) runs the same spine in reverse. Every transition is a
deliberate, reviewable step — a commit moving material through an ideation
gate, or an OpenSpec change — never an implicit copy or a silent status edit.

## Document Status Taxonomy

Every governance document carries a `Status:` header drawn from this
controlled list. Status is *state*, never genre.

| Status | Lifecycle state | Meaning |
| --- | --- | --- |
| `brainstorm` | captured | Non-normative; contradiction legal; lives in `ideation/brainstorm/` |
| `staged` | organized | Structured toward a proposal; not yet policy |
| `draft` | proposed (or awaiting proposal) | Normative intent, not yet ratified |
| `ratified` | ratified / implemented | Backed by an approved OpenSpec change, or by a durable ratification record where no such change exists; header names it |
| `standard` | promoted | Backed by a promoted spec or canonical contract; the only status allowed to claim shared-standard authority |
| `superseded` | superseded | Kept for provenance; header names the successor |
| `retired` | retired | Withdrawn; header names the reason or decision record |
| `record` | out of band | Immutable evidence artifact CAPTURED ONCE (simulation output, audit reports, dated run reports); excluded from prose-to-spec conversion and contradiction checks |
| `projection` | out of band | Deterministic RE-DERIVED rendering of a declared source of truth, rewritten in place by a named generator; never authoritative, never hand-edited, and not immutable — regenerating it is the correct act, not a violation |

An optional `Kind:` header carries genre, from the recommended vocabulary:
`architecture | plan | process | runbook | report | register | template |
reference`.

## Status Claim Rules

- No document may claim `standard` status — in its header or its prose —
  unless a promoted OpenSpec spec or canonical contract backs the claim.
- A `ratified` header names its ratification on exactly ONE citation line in
  the lifecycle header, written in one of two spellings — never two lines
  (not one of each spelling, and not the same spelling twice), and never
  none: a bare, uncited `Status: ratified` is a violation whatever else the
  document says, two lines each claiming to name the ratification say
  nothing about which is current, and prose elsewhere in the document that
  opens with the same word is body text, not a citation.
  - `Ratified by: <change>` is the primary spelling, required wherever an
    approving OpenSpec change exists to name. The named change is the
    citation; a line naming its change and nothing else is complete. It is
    also the only thing that completes this spelling: naming an approver and
    a date after `Ratified by:` instead of a change does not satisfy it.
  - `Ratified:` is the record-citing alternative, legal only where no
    approving OpenSpec change exists to name — an in-session ruling, a
    disposition, an `.openspec.yaml` approval pair, an archive or
    ratification commit, or another durable record. It names at least one of
    an approver, a date, or a resolvable record path. That floor applies to
    `Ratified:` alone and never reaches `Ratified by:`, whose named change is
    itself the record.
  - The recognized approver form is `by <Name>` — write it that way. A line
    that names its approver some other way (inside a record parenthetical,
    say) is not read as naming one, and must clear the floor on its date or
    its resolvable record path instead. Where it clears none of the three,
    add `by <Name>`; never invent a date or a record the evidence does not
    carry.
- A `superseded` header names the successor artifact.
- Generated evidence CAPTURED ONCE (simulation output, runbook transcripts,
  audit reports, dated run reports) is always `record`, regardless of how
  normative its content sounds.
- **Being generated is not what makes a document a `record`; being CAPTURED
  is.** A deterministic projection that a named generator rewrites in place
  from a declared source of truth carries `projection`, not `record`. The test
  is whether re-running the generator over the same path is the CORRECT act:
  for a projection it is the only way to update it, so there is no captured
  state for immutability to protect, and reporting each regeneration as a
  content edit to a record would make the correct act a critical finding. For
  a one-shot capture it is not — a dated report is written once and a second
  run writes a different path. A `projection` document declares its generator
  and its source, and is never hand-edited.
- An OpenSpec change packet's `proposal.md`, and every `review/` record under
  that packet — whatever that record's subject — are governance documents for
  these rules. Both make a claim about standing (a proposal says whether it is
  `draft` or `ratified`; a review record says what standing its own finding
  has, whether that is a ratification, a captured `record` of a review round,
  or a superseded earlier one), and a claim of standing is what the taxonomy
  exists to make checkable. Ratified by
  `govern-openspec-corpus-membership` (2026-08-23).
  - **The two obligations differ in reach, and only one reaches every review
    record.** The TAXONOMY rule reaches all of them: a `review/` record
    carries a `Status:` from the controlled taxonomy, in the header window,
    whatever it is about — most often `Status: record`, which is conforming
    and needs nothing further. The RATIFICATION-CITATION rule reaches only a
    document whose status IS `ratified`. A review record carrying any other
    taxonomy value owes no citation; demanding one would be demanding
    provenance for a claim the document does not make.
  - **The REST of the packet is not ruled.** `tasks.md`, `design.md`, the
    spec delta files, `supporting-docs/` and `evidence/` are working files of
    the change rather than documents making a standing claim, and no finding
    is emitted against them under these rules. Whether they are governance
    documents is a separate question, deliberately left open.
  - There is **no legacy class and no contract date**: a proposal carrying no
    `Status:` header is a current violation whenever it was authored. The
    remedy is a header DERIVED from that packet's own record — its origin
    declaration, its ratification or archive commit, its own task record, or
    the index row that announced it — not a reduced severity that leaves the
    claim unmade. Where the record supports neither a status nor, for
    `ratified`, a citation that clears the floor, report the document by name
    with what its record does and does not carry; an invented provenance is a
    worse defect than the missing one it hides.
  - A `ratified` `review/` record that states its ratifier and decision date
    in its own vocabulary — a `Ratifier:` or `Decision date:` header — still
    carries one of the two sanctioned citation spellings. Those headers
    **accompany** a citation and never stand in place of one: recording the
    same fact twice is the cost of having one rule, and a third spelling for
    the documents whose whole subject is ratification would undo it.
  - Byte-exact evidence is **not** in scope, by path: a document whose path
    carries a `supporting-docs`, `source-snapshots` or `evidence` segment is
    excluded even where its name would otherwise match, because reporting a
    frozen record for the state it preserves is a false finding.

## The Explicit Delta Rule

Outside `ideation/brainstorm/`, prose that changes, contradicts, or restates
promoted policy must be expressed as an explicit change from current state:
an OpenSpec change proposal, or an explicit supersedes marker naming the
affected spec requirement. Accidental restatement of promoted policy in
different words is a defect, and health tooling reports unmarked
contradictions as findings.

### Prose Tagging Markers

The machine-readable markers the rule and the conversion queue rely on use
one canonical grammar under the `xspec:` namespace, expressed as HTML
comments (concretized by the
[concretize-prose-tagging-syntax](../openspec/changes/archive/2026-07-09-concretize-prose-tagging-syntax/proposal.md)
change):

```text
<!-- xspec:candidate target=<capability> -->
...prose selected for conversion to a spec or contract...
<!-- /xspec:candidate -->

<!-- xspec:supersedes spec=<capability>/<requirement-slug> change=<change-id> -->
```

- `<capability>` is a spec capability id under `openspec/specs/` (or in an
  active change's `specs/` while the capability is pre-promotion);
  `<requirement-slug>` is the kebab-case requirement name, e.g.
  `document-lifecycle/explicit-delta-rule`.
- Candidacy is **block-level only**: no `Status:` value expresses
  conversion candidacy — a document's lifecycle status and its conversion
  queue stay orthogonal. Only prose inside well-formed candidate blocks is
  queued.
- Candidate blocks may not nest and may not span Markdown heading
  boundaries; every open fence has a matching close fence in the same
  section. A passage covering several sections gets one block per section.
- `change=` on a supersedes marker is included as soon as the OpenSpec
  change exists; a marker that never acquires one becomes an aging finding.
- Markers are contract surface: the literal string `xspec:` appears in
  governance Markdown only inside well-formed markers, so
  `grep -rn 'xspec:' --include='*.md'` is the complete inventory. Health
  tooling reports malformed markers, unresolved targets, and structural
  violations as findings.
- Staged fragments (`ideation/staging/<topic>/`) are queued structurally by
  their headers (target capability + delta type). They need no inline markers
  to be QUEUED — but a fragment conforming to the outline template below wraps
  its proposal-element sections in the same ratified `xspec:` grammar, because
  that prose IS the candidate text an eventual change would carry and the
  grammar already exists for exactly that content.

## The Staged-Topic Outline Template

Ratified by `add-staged-topic-outline-template` (2026-08-15). A staged topic's
primary fragment — the file `primaryFragmentPath` selects, path-only and never
content-sniffed — IS the topic's outline. There is no second "true" document
and no new selector: every other file in a topic folder stays free-form.

The outline is for BOTH human and AI consumption. Every section exists so a
reader, or a parsing tool, can extract the topic's live state without opening
the whole folder.

### Three required sections

A conforming fragment carries, in addition to its proposal-element sections:

1. **pre-document, non-documented idea notes** — the thinking that has not
   become a claim yet;
2. **conflicts** — what this topic contradicts, and what contradicts it;
3. **open questions** — where the most attention is spent, so it carries the
   most structure.

### Every open question carries four sub-fields, in this order

`Context`, `Recommended answer`, `Explanation`, `Disposition status`.

A question is never recorded bare. The template forces a recommendation and the
reasoning for it even while the disposition itself stays `open`, so an
undecided question still gives a reader something to disagree with rather than
a prompt to re-derive. A question missing any sub-field is reported by
doc-health's `staged-topic-template` family.

### Sections are extensible, with provenance

Either a human or an AI may add a section beyond the required set. Each added
section carries an `Added-by:` line naming the person or agent and the date,
because the document accumulates content nobody commissioned in advance and has
to stay attributable as it does.

An AI adding or patching a section does so through the ordinary `edit-document`
verb on the topic's branch session, scoped by the section it targets — its
heading, or its `xspec:candidate` fence where the section is a proposal-element
block. Section-scoped patching is a patch-TARGETING detail, not a different kind
of action, so it introduces no second write verb.

> Amended 2026-08-15. This first said `edit-apply`, following the topic's Q4.
> That verb is the gate console's main-resident redline path: it requires a
> change id and applies to change documents, so it cannot write a staged
> fragment on a session branch — and a topic that HAS an owning change has
> already moved its material out of staging, so the two states never coexist.
> `edit-document` is the session content verb the buffer contract already uses.
> The rule is unchanged; only the verb name was wrong.

### Round-trip on demote — the load-bearing rule

**A demoted topic does not reset to its aspirational text.** When a topic that
reached proposal is demoted back to staging — by the demote verb, or by a
failed or reverted push — its proposal-element sections are refreshed to the
ACTUAL text of the last attempted `proposal.md`, tagged with the change id, the
dates raised and demoted, and the demote reason.

This is testable, and that is the point of stating it here rather than leaving
it a convention: does a demoted fragment's `Last proposal attempt` slot carry
the prior change's real text. Nothing learned while a change was in flight may
be lost by falling back to staging.

### Conformance is opt-in for what already exists

REQUIRED for any topic staged after this ratified; OPT-IN for topics staged
before it, rewritten when the topic is next actively worked. doc-health reports
non-conformance at WARNING and never blocks a gate on it — a mechanical rewrite
of dormant, complete, or externally blocked topics produces busywork without
advancing a live decision. Obligation follows a topic's staging date, never its
last touch, so editing an opt-in topic for an unrelated reason does not
silently make it required.

### The skeleton

Copy-pasteable. Every bracketed `<…>` is a fill-in slot, and the marker
comments are the real ratified `xspec:` grammar rather than illustrative syntax
of their own — filling the slots produces a document the tag-hygiene family
accepts unchanged.

```markdown
# Staged: <short topic title>

Status: staged
Kind: <capability-proposal | architecture | staging-packet | ...>
Summary: <2-4 sentences, plain prose, no heading directly above it — this is
what the wheel's expanded tile shows verbatim, so write the topic's own
substance here, not a restatement of the title>
Topics: <comma-separated keyword tags>
Repository context: <which repo(s) own the target capability/capabilities;
who realizes the change>
Staging ID: openxFactory:staging:<topic-slug>
Captured: <YYYY-MM-DD>
Source: <who named this topic, when, and from what — a brainstorm doc, a
live session ruling, a cross-repo pointer>
Target capabilities: <ADDED|MODIFIED> `<capability>` (<one-line delta
summary>)[ and <ADDED|MODIFIED> `<capability-2>` (<one-line delta summary>)]

## Last proposal attempt (round-trip provenance)

<!-- Stays "none yet" until this topic first reaches proposal. On DEMOTE,
     replace every field below with the ACTUAL values from the demoted
     change — never re-blank them; that is the whole point of this slot. -->

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## Claims

<!-- Settled context the open questions below should NOT reopen. -->

- <a decided fact or ruling this topic treats as fixed>

## Why

<!-- xspec:candidate target=<target-capability-1> -->
<one paragraph: the problem, in the shape a proposal.md "## Why" section
would state it — the CURRENT possible-draft answer, not a placeholder>
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=<target-capability-1> -->
<one or more paragraphs: the CURRENT possible-draft shape of the change,
written the way a proposal.md "## What changes" section would read>
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=<target-capability-1> -->
- Affected specs: `<capability>` (ADDED|MODIFIED — <requirement area>)
- Affected code: <repo(s) / path(s)>
- <other blast-radius notes>
<!-- /xspec:candidate -->

## Idea notes (pre-document, non-documented)

<!-- Free-form thoughts that have not earned a claim, a question, or a
     proposal line yet. Anyone — human or agent — may append. -->

- <idea note text> — Added-by: <name or agent/model id> · <YYYY-MM-DD>

## Conflicts

<!-- Honest tensions this topic has NOT resolved: with another staged
     topic, with a promoted spec, with itself. A conflict names something
     currently INCONSISTENT, even when the reconciliation is "defer,
     noted" — it is not the same thing as an open question. -->

- <conflict text> — Added-by: <name or agent/model id> · <YYYY-MM-DD>

## Open questions

<!-- The section read most closely. Every question gets all four
     sub-fields below, in this order, even when the answer feels
     obvious — "obvious" is exactly when a wrong disposition ships
     silently. -->

### Q1. <question, as a single sentence>

Context: <what makes this undecided; what facts bear on it>
Recommended answer: <a position, stated plainly — not a survey of options>
Explanation: <why this is the recommended answer — the reasoning, not a
restatement of the recommendation>
Disposition status: open
Added-by: <name or agent/model id> · <YYYY-MM-DD>

## Exit

<one or two sentences: what crossing the proposal gate looks like for this
topic, and what must be true first (e.g. "every open question above carries
a disposition other than `open`"). Do not cite an existing change-id here —
doc-health's location-conformance family scans Exit-labeled lines for
exactly that, to catch a topic mistakenly claiming another change's exit as
its own.>
```

## Gates In Practice

- `captured -> organized`: brainstorm material is selected, deduplicated, and
  targeted into `ideation/staging/` or a candidate register; the source is
  marked accordingly.
- `organized -> proposed`: an OpenSpec change is created carrying the spec
  deltas; selected staged material moves with Git history into
  `openspec/changes/<change-id>/supporting-docs/`. Proposed prose becomes
  `draft`; immutable evidence stays `record`; a re-derived projection carries
  `projection`.
- **Origin at the proposal gate** (the promoted `document-lifecycle` proposal
  origin requirements — referenced here, never restated): every proposal
  declares exactly ONE origin in its `.openspec.yaml`, fixed at creation and
  immutable for the life of the change. `scripts/proposal-support.py
  transition` writes the `staged` origin automatically (durable id from the
  topic's `Staging ID:` header, path as the historical transition source)
  and repeats it in the support manifest; a deliberate exception uses
  `scripts/proposal-support.py declare-adhoc <change> --reason --approved-by
  --approved-on` — ad-hoc is an explicit approved exception, never a default,
  and never a substitute when organized source material exists. A packet
  DRAFTED BUT NOT YET APPROVED declares the same command's
  `--proposed-by --proposed-on` INSTEAD of the approval pair: an unapproved
  origin is a lawful state that reports nothing, approval is later ADDED to
  it without the identity moving, and a proposal whose `Status:` claims
  `ratified` or beyond over an unapproved origin is reported — approval
  appears when the status claims it, and an approval date is never invented
  to quiet a check. Strict
  per-change verification (`proposal-support.py verify <change>`) and the
  archive gate reject missing, malformed, dual-kind, or manifest-disagreeing
  origins, and an ad-hoc origin declaring neither provenance pair or half of
  one; the archive gate additionally compares the declaration against the one
  the packet carried at its RATIFYING COMMIT — the first commit whose
  `proposal.md` declares `Status: ratified` — and refuses the archive (exit 2,
  no bypass flag) when the origin block or the support manifest's repeated
  origin fields have moved since, when no such commit exists, or when the
  history holding that baseline cannot be read; the nightly `proposal-origin`
  doc-health family
  (the fifteenth) reports drift — including post-ratification mutation, a
  `contested` finding — across active and archived proposals.
- `proposed -> ratified -> implemented`: standard OpenSpec flow.
- `implemented -> promoted`: the change archives and its requirements live
  under canonical specs; affected docs may claim `standard`. Before archive,
  proposal support is packaged as `supporting-docs.tar.gz` beside the archived
  change with a readable checksum manifest. Historical bundles never live
  under canonical `openspec/specs/`. THE ARCHIVE DATE IS UTC:
  `proposal-support.py archive` derives it once as today in UTC, runs the
  pinned OpenSpec CLI with `TZ=UTC` (the CLI has no date option and names
  `openspec/changes/archive/<YYYY-MM-DD>-<change>/` from its own clock),
  refuses a `--date` that is not today in UTC, and refuses and reverts the
  move when the directory the CLI named carries any other day — so the
  bundle's `packaged_at`, the directory name and the ledger row's `moved_on`
  are one date.
- `promoted -> adopted`: consumers re-pin, replace local copies with
  references plus thin overlays, and retire duplicates — see the
  [Domain-To-Neutral Promotion Process](domain-to-neutral-promotion-process.md).

### Proposal Supporting Documents

`ideation/staging/` is a live queue, not permanent storage. At the proposal
gate, selected files move into the active OpenSpec change:

```text
ideation/staging/<topic>/
  -> openspec/changes/<change-id>/supporting-docs/
  -> openspec/changes/archive/<date>-<change-id>/supporting-docs.tar.gz
```

Each active support folder owns `manifest.yaml`, recording the source path,
source revision, transition date, selected files and hashes, optional
NotebookLM workspace, and any files deliberately left staged. A partial
promotion moves only selected files; the residual topic remains in staging.
When no material remains, the staging folder disappears.

The archived change keeps `supporting-docs.manifest.yaml` readable beside the
compressed bundle. Proposal, design, and spec artifacts must carry every
accepted normative claim before compression; the bundle is provenance, not
canonical policy.

## Catalog Tags Are Not Lifecycle State

The active `add-document-cataloging` change defines an external,
aggregation-hosted document catalog with controlled classification facets
(see its
[document-cataloging spec](../openspec/changes/add-document-cataloging/specs/document-cataloging/spec.md)
for the owned vocabulary, provenance, and disposition-authority rules). Those
facets are descriptive discovery metadata: they never set or infer this
document's `Status:`/`Kind:` header, never assign ownership or destination,
and never move a document through the lifecycle spine above. Once that
change promotes, its own capability continues to own those rules; this
section only draws the boundary for readers of this spine.

## Cross-Factory Ideation Routing

The active `add-cross-factory-ideation-routing` change extends the ideation
work area and proposal-supporting-document rules above: an unknown-owner
`openxFactory/ideation/brainstorm/inbox/<idea-id>/` capture point; a
cross-domain routing hub at `ideation/brainstorm/cross-domain/<idea-id>/`
that coordinates claims split out of a domain-origin idea without replacing
its source; and an `ideation_provenance` manifest entry (Idea ID, Claim IDs,
and a pinned routing-record reference) for proposals derived from routed
claims (see its
[ideation-routing spec](../openspec/changes/add-cross-factory-ideation-routing/specs/ideation-routing/spec.md)
and
[document-lifecycle spec delta](../openspec/changes/add-cross-factory-ideation-routing/specs/document-lifecycle/spec.md)
for the owned Idea/Claim ID, transition, and destination-acceptance rules).
Routing coordinates proposed ownership only; it never replaces this spine's
gates. Until that change promotes, the lifecycle spine above remains
authoritative and the xFactory aggregation repository still hosts no general
ideation backlog.

## Related Documents

- [Ideation Work Area](../ideation/README.md) — the captured/organized areas.
- [Domain-To-Neutral Promotion Process](domain-to-neutral-promotion-process.md)
  — cross-tier promotion and devolution mechanics.
- [Domain Neutralization Candidate Register](domain-neutralization-candidate-register.md)
  — per-concept register whose aliases map onto this spine.
- Migration mapping for pre-taxonomy `Status:` values:
  [design.md](../openspec/changes/archive/2026-07-09-add-document-lifecycle-vocabulary/design.md)
  of the ratifying change.
