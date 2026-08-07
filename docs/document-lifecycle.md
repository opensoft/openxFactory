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
| `ratified` | ratified / implemented | Backed by an approved OpenSpec change; header names it |
| `standard` | promoted | Backed by a promoted spec or canonical contract; the only status allowed to claim shared-standard authority |
| `superseded` | superseded | Kept for provenance; header names the successor |
| `retired` | retired | Withdrawn; header names the reason or decision record |
| `record` | out of band | Immutable evidence artifact (generated reports, simulations, audits); excluded from prose-to-spec conversion and contradiction checks |

An optional `Kind:` header carries genre, from the recommended vocabulary:
`architecture | plan | process | runbook | report | register | template |
reference`.

## Status Claim Rules

- No document may claim `standard` status — in its header or its prose —
  unless a promoted OpenSpec spec or canonical contract backs the claim.
- A `ratified` header names the approving OpenSpec change
  (`Ratified by: <change>`).
- A `superseded` header names the successor artifact.
- Generated evidence (simulation output, runbook transcripts, audit reports)
  is always `record`, regardless of how normative its content sounds.

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
  their headers (target capability + delta type) and need no inline
  markers.

## Gates In Practice

- `captured -> organized`: brainstorm material is selected, deduplicated, and
  targeted into `ideation/staging/` or a candidate register; the source is
  marked accordingly.
- `organized -> proposed`: an OpenSpec change is created carrying the spec
  deltas; selected staged material moves with Git history into
  `openspec/changes/<change-id>/supporting-docs/`. Proposed prose becomes
  `draft`; immutable evidence stays `record`.
- **Origin at the proposal gate** (the promoted `document-lifecycle` proposal
  origin requirements — referenced here, never restated): every proposal
  declares exactly ONE origin in its `.openspec.yaml`, fixed at creation and
  immutable for the life of the change. `scripts/proposal-support.py
  transition` writes the `staged` origin automatically (durable id from the
  topic's `Staging ID:` header, path as the historical transition source)
  and repeats it in the support manifest; a deliberate exception uses
  `scripts/proposal-support.py declare-adhoc <change> --reason --approved-by
  --approved-on` — ad-hoc is an explicit approved exception, never a default,
  and never a substitute when organized source material exists. Strict
  per-change verification (`proposal-support.py verify <change>`) and the
  archive gate reject missing, malformed, dual-kind, or manifest-disagreeing
  origins; the nightly `proposal-origin` doc-health family (the fifteenth)
  reports drift — including post-ratification mutation, a `contested`
  finding — across active and archived proposals.
- `proposed -> ratified -> implemented`: standard OpenSpec flow.
- `implemented -> promoted`: the change archives and its requirements live
  under canonical specs; affected docs may claim `standard`. Before archive,
  proposal support is packaged as `supporting-docs.tar.gz` beside the archived
  change with a readable checksum manifest. Historical bundles never live
  under canonical `openspec/specs/`.
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
