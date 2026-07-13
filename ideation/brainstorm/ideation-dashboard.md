# Ideation Area Dashboard — Brainstorm

Status: staged
Kind: architecture
Summary: Proposes a read-only, generated dashboard GUI whose centerpiece is a
realization funnel — each topic cluster's enumerated *possible* feats, which
of them staging *picked*, and where each pick went — layered over a pipeline
board, lineage, readiness, and health views projected from the headers and
indexes that already exist, plus a non-mutating "workbench" for assembling
temp doc sets (cluster-seeded or ad-hoc) and pointing NotebookLM, readiness
scoring, and doc-health at them — complementing (not duplicating) the
NotebookLM semantic interrogation surface.
Topics: ideation-dashboard, workflow-visualization, ideation-cross-reference, doc-health, notebooklm-projection, lifecycle-projection, doc-management, doc-workflow
Repository context: openxFactory (contract-level, cross-factory topic)
Captured: 2026-07-12
Organized: 2026-07-12 into the ideation-dashboard staged topic and promoted
the same day into
[add-ideation-dashboard](../../openspec/changes/add-ideation-dashboard/proposal.md)
(ratified) — all open questions carry decisions in that packet's decision
record; Brett confirmed R1–R14 unchanged, decided D7–D9 (authoring
authority) in a follow-on session, and ratified the proposal on 2026-07-12.
The change stays active until realization evidence lands (code surface
declared), then archives.
Participants: Brett Heap, Claude (design session)

## Problem

The family already has a *semantic* surface over ideation content: the
NotebookLM projection (`xf-ideation` / `xf-drafts` / `xf-canon`) supports
interrogation, mind maps, and audio overviews of what the documents *say*.
Nothing renders what the documents *are*: which topics exist at which
lifecycle stage, what is heading where, what is ready, what is blocked, what
is stale. That governance state exists today — but scattered:

- `Status:` / `Kind:` / `Summary:` / `Topics:` headers on every brainstorm doc
- `ideation/staging/INDEX.md` rows (delta, files, readiness, exit)
- `ideation/README.md` active/organized lists and promoted-proposal pointers
- OpenSpec active changes and the dated archive
- nightly doc-health and corpus-share reports
- (once landed) the ideation-cross-reference readiness index with per-topic
  three-tier scores

Assembling "where is everything and what state is it in" means reading five
or six files and holding the join in your head. A newcomer — or Brett after a
week away — has no single glanceable picture of the ideation area.

## Design sketch

### Principle: a projection, never a source of truth

Same stance as the NotebookLM projection and every Omni worker in the family
(`document-cataloger`, `ideation-organizer`): the dashboard is **generated
from** the headers and indexes the validators already parse, holds **no state
of its own**, and is **non-mutating** over source docs. If the dashboard
disagrees with the repo, the dashboard is wrong and gets regenerated. v1 is
strictly read-only; any future interactivity is bounded below.

### Data layer

A generator (sibling of the doc-health checker, plausibly the same nightly
lane) scans `ideation/` + `openspec/changes/` and emits one machine-readable
snapshot — e.g. `ideation/dashboard/dashboard.json` — containing per doc:
stage, kind, summary, topics, captured/organized dates, organized-destination
links and their lifecycle words; per staged topic: the INDEX row (delta,
files, readiness, exit); per change: proposal status, `code_surface`,
`target_release`. Once the ideation-cross-reference index lands, its per-topic
three-tier scores and conflict flags join the snapshot. Renderers only ever
read the snapshot, so the scrape logic lives in exactly one place.

### The realization funnel: possibles and picks

The conceptual core (added in session, 2026-07-12). A cross-referenced topic
cluster is a **many-possibles object**: one body of brainstorm material can
plausibly spawn several distinct feats. Staging is a **selection event**: the
organize gate picks *one feat or a small, clearly defined set* out of those
possibles and gives the pick identity (staging ID, target capabilities, delta
types). The dashboard must therefore render three distinct populations per
topic cluster, not one:

1. **Possibles** — the enumerated candidate feats a cluster could become.
   States: `latent` (enumerated, unpicked), `picked` (selected into a staged
   topic, with the staging ID as citation), `rejected` / `superseded`
   (deliberately not pursued, with a reason). A latent possible is backlog,
   not failure — visible inventory for a later staging pass.
2. **Picks** — which possibles the organize gate selected, and the staged
   topic each landed in. The edge possible→staged-topic is the pick record.
3. **Realizations** — where each pick went next: OpenSpec change, feat
   decomposition, release evidence (the release-realization flow's two-axis
   model already tracks this tail end).

The family already has a worked precedent for exactly this shape: the
**domain-neutralization candidate register** (12 enumerated candidates,
DTN-001/002/003/004/013 `adopted`) is a possibles register for one specific
promotion case — a list of candidates, each with an adoption status and
identity. The funnel generalizes that register shape to feat extraction from
any topic cluster. Real worked examples the funnel would render today:

- `doc-health-pipeline` brainstorm → picked into **three** staged topics
  (prose-tagging, doc-health-checks, semantic-health-sweep), all since
  promoted — one cluster, a clearly defined set of three picks.
- The avatar staged packet → split into **four** approved changes (contract
  kernel, feasibility, reference runtime, UI standard) — one pick refined
  into a bounded set at the proposal gate.
- `domain-to-neutral-promotion` brainstorm → promotion process doc + the DTN
  register + promotion-refinements staged topic.

**Cluster↔possible links are many-to-many** (decided in session, 2026-07-12):
a single brainstorm doc carries several `Topics:`, so one doc feeds several
clusters, and one possible can be claimed by more than one cluster — this
very dashboard possible is claimed by both `ideation-governance` and
`workflow-visualization`. The funnel therefore draws explicit edges between
the cluster and possible columns rather than nesting possibles under a
single cluster row; per-cluster tallies count *links*, not cards, so a
shared possible appears in every claiming cluster's count.

### Workbench: user-assembled temp sets (added in session, 2026-07-12)

The dashboard gains one bounded interaction: the user can **assemble a
temporary working set of docs** — a "workbench" (Brett's term: temp staging;
naming note below) — and point tools at it. Two assembly paths:

1. **Cluster-seeded**: click a topic-cluster card and its member docs
   pre-populate a workbench — the machine's grouping as a starting point.
2. **Ad-hoc**: multi-select docs from the doc list directly, ignoring the
   clusters — because *the user may see a pattern the index does not*. An
   ad-hoc set that matches no machine cluster is not just a convenience; it
   is **signal that the tagging/clustering missed something**, and the
   workbench should be able to propose it back to the cross-reference index
   as a candidate topic (evidence-backed recommendation, `pending_review` —
   the same contract the organizer and cataloger already use).

A workbench is a **reference set, never copies or moves** — source docs are
untouched, so the non-mutating discipline survives intact. The only artifact
written is the workbench manifest itself. Tools that take a set:

- **Project to a scratch NotebookLM notebook** (`xf-wb-<name>`-style, via the
  existing nlm CLI + sync-script pattern) for interrogation, mind maps, audio
  — and, once the hybrid-imports change ratifies, notes taken there flow back
  through the governed return path.
- **Score readiness on demand** — run the three-tier panel over just this set
  instead of waiting for the nightly lane.
- **Run doc-health scoped to the set.**
- **Draft an organize-gate action** — pre-fill a `staging/<topic>/` packet
  skeleton from the set for a human to review and commit; the gate itself
  stays manual.

**Naming caution**: "temp staging" collides with the governed lifecycle word
`staged` and the `ideation/staging/` area — a doc must never appear to be
staged because it sits in a scratch set. Recommend a collision-free word
(workbench / tray / assembly) in the eventual contract, whatever the UI label
says.

**The gap this exposes**: nothing today records the possibles that were *not*
picked. `Target capabilities:` on a staged doc records the pick; the unpicked
candidates evaporate into prose (or a reader's memory). The dashboard can
only render what is declared, so the funnel view forces a small upstream
contract addition — a possibles register per topic cluster (candidate home:
the ideation-cross-reference index, whose three-tier reviewers are already
reading every cluster and are naturally positioned to enumerate what it could
become; alternatives in open questions).

### Rendering candidates (adopted-stack exploration order)

The MIT-vetted stack from `adopt-workflow-visualization-stack` applies
directly — no new library survey needed:

1. **Mermaid markdown dashboard** — a generated `DASHBOARD.md` with a
   pipeline flowchart (counts per stage), per-topic state diagrams, and
   tables. Zero new dependencies, renders on GitHub, diffable, could commit
   alongside `staging/INDEX.md`. Cheapest possible v0.
2. **Static single-file HTML board** — the "simple GUI": one self-contained
   HTML file (inline CSS/JS, reads the embedded or adjacent JSON snapshot)
   showing a kanban-style board, columns = lifecycle stages, cards = topics.
   No server, opens from the filesystem, publishable by CI if wanted.
3. **Cytoscape.js topic-cluster graph** — second view once the board exists:
   nodes = docs, edges = shared `Topics:` tags and explicit `Organized:` /
   staging-exit links. This is the governance complement to NotebookLM's
   content mind map.
4. **React Flow** — only if editable/interactive views are ever authorized.

### View catalogue

- **Realization funnel** (primary): six columns — *source docs → topic
  cluster → possibles → staged picks → proposals → realized* — with explicit
  edges drawn between all columns. Doc→cluster edges come from each doc's
  `Topics:` header and cluster→possible edges from the possibles register;
  both hops are many-to-many (see above), so columns are independent stacks
  and hover-tracing a card highlights its full upstream/downstream thread.
  **Decided 2026-07-12: docs-first six-column is the default view**; the
  five-column clusters-first layout remains as a "collapse docs" mode for
  when the doc count makes the leading column noisy. Both render from the
  same snapshot. Possibles render in three visual states: latent (hollow/grey, the
  backlog), picked (filled, edge to its staged topic labelled with the
  staging ID), rejected/superseded (struck, reason on hover). The eye should
  read three things instantly: how much latent potential a cluster still
  holds (hollow count), how disciplined the pick was (few, clearly bounded
  edges), and how far each pick has travelled right-ward. A cluster with many
  hollow possibles and high readiness scores is the "someone should stage
  this" signal made visible.
- **Pipeline board**: brainstorm → staged → active proposal →
  archived/ratified columns; cards show title, kind, one-line summary,
  topics, readiness badge, age — plus a **possibles badge** (`3 possibles ·
  1 picked`) tying the board back to the funnel. This is the "simple GUI"
  ask; the funnel is the same data pivoted from stage-centric to
  topic-centric.
- **Topic cluster graph**: which docs share subjects across stages — the
  visual twin of the cross-reference index.
- **Lineage / flow view**: where ideas went — brainstorm doc → staged topic →
  change → archive, drawn from `Organized:` headers and INDEX exit notes; a
  Sankey-ish traceability picture, and a visual detector for the stale-link
  defect the `Organized:` format exists to catch. (The funnel is the
  forward-looking version of this; lineage is the historical record.)
- **Readiness heat strip**: per-topic three-tier scores, min-score gate
  highlighted, wide-spread conflicts flagged (consumes the cross-reference
  index verbatim). Readiness naturally annotates the funnel's cluster column.
- **Health overlay**: doc-health findings on cards (contested vs
  auto-fixable), missing headers, stale statuses.
- **Corpus stats strip**: counts per stage, canon share and its trend
  (watching the nightly series, not day deltas).
- **Staleness view**: captured-date age for brainstorms that never organized
  and latent possibles that never got picked.

### Complement, not competitor, to NotebookLM

Clean division: NotebookLM answers *"what do these documents say?"*
(interrogation, mind maps, synthesis over content). The dashboard answers
*"what documents exist, in what state, heading where?"* (governance,
lifecycle, traceability). Neither renders the other redundant; the dashboard
could even deep-link a topic card to its NotebookLM notebook query.

### Interactivity boundary (revised in session, 2026-07-12)

The line is no longer "read-only" but **"non-mutating over source docs, and
never executes a gate."** In scope: selecting and assembling reference sets
(the workbench), launching analysis tools over a set, and *drafting* gate
artifacts (a pre-filled staging packet skeleton, a proposed topic tag for the
index) that a human reviews and commits. Out of scope, permanently: moving,
editing, promoting, or deleting any source doc, and executing any stage
transition — a workbench matures into a staged topic only through the normal
human organize gate, which the workbench merely pre-fills.

## Relationship to existing designs

- `ideation-cross-reference-readiness` (staged, decided): the dashboard's
  richest data feed — readiness scores, topic clusters, conflict flags. Open
  architectural choice: is the dashboard that capability's rendering layer,
  or a separate capability consuming its index?
- `adopt-workflow-visualization-stack` (adopted): supplies the license-vetted
  rendering libraries and the Mermaid-first exploration order; reuse, do not
  re-survey.
- `doc-health` (promoted): the nightly pipeline **already runs today**
  (codexFactory checker, nightly reports, corpus-share series) — the dashboard
  adds no new scheduler, only a new lane in the existing nightly run, beside
  the deterministic checks, the semantic sweep, and the readiness-scoring
  lane once `add-ideation-cross-reference-readiness` lands.
- `document-cataloging` (active, unimplemented): future tag source of truth
  for clustering, same bootstrap posture as the readiness index — headers now,
  catalog tags folded in later.
- `lifecycle-notebook-projection` (promoted): the sibling projection; the
  dashboard follows its derived-artifact discipline (regenerate, never edit).

## Open questions

(Kept as design history — every question below now has a decision or a
drafted recommendation in the
[staged topic's decision record](../staging/ideation-dashboard/ideation-dashboard.md).)

- **Possibles register home**: where are a cluster's candidate feats
  declared? Candidates: (a) the ideation-cross-reference index — its
  three-tier reviewers already read every cluster and can enumerate
  possibles alongside scores; (b) a `Possible feats:` header/section on
  brainstorm docs, author-declared at capture time; (c) a standalone
  register file per the DTN-register pattern. These compose — e.g. authors
  seed (b), the index reviewers consolidate into (a).
- **Possible states and transitions**: is `latent / picked / rejected /
  superseded` the right state set, and does a rejection require a recorded
  reason the way contested doc-health findings require a disposition?
- **Pick citation strictness**: must a pick edge cite the staging ID (and
  later the change ID), mirroring the origin-contract discipline, or is a
  link enough?
- **Backfill**: retroactively enumerate possibles for already-organized
  brainstorms (doc-health-pipeline, domain-to-neutral-promotion, avatar),
  or funnel-render only what declares possibles going forward?
- **Workbench naming**: pick the contract word ("workbench" recommended;
  "temp staging" collides with the `staged` lifecycle status and the
  `ideation/staging/` area).
- **Workbench persistence**: browser-local only (ephemeral, zero repo
  footprint), gitignored scratch manifests under e.g. `ideation/workbench/`,
  or committed manifests so a set is shareable and auditable across
  sessions/people?
- **Scratch notebook lifecycle**: are `xf-wb-*` notebooks auto-deleted when
  their workbench is discarded, or kept until explicitly cleaned (they are
  derived artifacts, so regenerate-don't-edit applies either way)?
- **Ad-hoc-set feedback contract**: does a human-assembled set that matches
  no cluster flow to the cross-reference index as a full organizer-style
  evidence-backed recommendation, or as a lighter "suggested topic" note?
- **Scope**: openxFactory's ideation area only, or every DomainxFactory's
  `ideation/` too, with a family-wide roll-up view in the aggregation repo?
- **Capability home**: its own capability, a rendering deliverable inside
  `add-ideation-cross-reference-readiness`, or a new doc-health lane?
- **Delivery form**: committed generated artifacts (like `staging/INDEX.md`),
  a CI-published static page, a local `scripts/` command that opens the HTML,
  or some combination?
- **Change coverage**: ideation/ only, or also active OpenSpec changes and the
  archive so the whole pipeline is one picture? (The lineage view argues for
  the latter.)
- **v0 cut**: Mermaid `DASHBOARD.md` first (zero deps, ships this week) then
  the HTML board, or straight to the HTML board since the JSON snapshot is
  needed either way?
- **Snapshot contract**: is `dashboard.json` a promoted, schema-versioned
  contract (kind + schema_version like every other YAML/JSON surface), or an
  internal artifact of the generator?
- **Regeneration trigger**: nightly with doc-health, on every ideation commit,
  or on demand only?

## Exit

Organize into a staged topic once the open questions have recommendations.
Likely exits as an openxFactory contract change defining the dashboard
snapshot schema and projection discipline, paired with a codexFactory delta
implementing the generator and renderers — the same two-repo split as
`ideation-routing`, `document-cataloging`, and the staged readiness index;
alternatively folded into `add-ideation-cross-reference-readiness` as its
rendering layer if that proposal is still unopened when this matures.
