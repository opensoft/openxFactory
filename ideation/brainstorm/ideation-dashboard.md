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

---

## v2 — bug register and direction (2026-07-14, post-realization review)

v1 realized (`add-ideation-dashboard`, 25/27 tasks, deployed at
https://ideation-dashboard.xforge.us) and immediately taught us where it is
wrong. This section is the raw v2 input: Brett's direction decisions, a
four-lane adversarial review of the realized system (governance record,
lane/deploy pipeline, frontend, plus a live reproduction of the production
lane failure), and the v1 build track's own candid deferral record. Being
brainstorm-stage, items may contradict; nothing here is normative.

### Direction decisions (Brett, 2026-07-14)

- **Hybrid backend, explicit seam.** One UI over an explicit backend API
  seam with two interchangeable implementations: a local backend (reads the
  operator's clones directly, serves at localhost) and a served backend
  (server-side workspace on xForge). v1's worst deployment bugs trace to
  never naming this seam: a loopback-only dev server (`serve.py` says "NOT a
  backend service") silently became the only thing that could serve
  `/snapshot.json` and the `/source/<path>` viewer, so the static xForge
  deploy shipped with both presumed-broken.
- **Repo discovery with a configurable allowlist.** The tool's entry point
  becomes a repo picker: enumerate candidate repos from (a) a scan of a
  configured local workspace root and (b) the user's GitHub orgs via `gh`,
  filtered through an explicit allowlist config of orgs/repos the tool may
  see. Merge into one list with per-repo cloned/not-cloned status.
- **No more implicit local-clone assumption.** v1 assumes the corpus is
  already cloned at a fixed relative path. v2 must make the workspace root
  explicit configuration, verify the expected repos are actually cloned,
  and offer clone-on-demand into the workspace root.

### Bug register (evidenced; grouping mine)

**A. Data pipeline emptiness — the funnel's middle is fiction.**

1. The possibles pipeline is entirely empty in production: `register.py`
   reads `ideation/cross-reference.yaml`, which has never existed in
   openxFactory (`possibles: []`, 0 across the live snapshot). Everything
   downstream of it is dead: staged→proposal flow edges never draw,
   `origin_staging_id` is always null, funnel possibles column is a bare
   em-dash everywhere except nothing.
2. Cluster readiness-heat and conflict-flag UI are dead bindings: the views
   read `c.readiness`/`c.conflict_flags`; the generator emits neither
   (0/82 clusters). Upstream-gated on `add-ideation-cross-reference-readiness`,
   which has not landed — the same sibling change blocks open tasks 1.1 and
   3.5 and the lens's queue-submission half. One dependency, four gaps.
3. Ratification line never renders despite 27 archived changes: the
   generator requires a `Ratified by:` header inside `proposal.md`; 0/35
   changes carry one there (ratification lives in the ratified DOCS, not
   proposals). Wrong derivation source.
4. "Add as cluster" in the keyword lens is a stub: it records
   `PENDING_PROPOSAL_REF` and shows a note; no queue entry, no submission.
   A user who clicks it reasonably believes they proposed something.
5. Canvas draft provenance is reconstructed best-effort (the snapshot
   projection deliberately drops the register's provenance field) rather
   than carried through.

**B. The lane and deployment pipeline silently rots.**

6. **stage:null DoS (live-reproduced).** The production lane failure
   ("snapshot rejected by the pinned validator: 4 error(s)") reproduces
   exactly: two `docs/sops/` files lacking `Status:` headers made the
   generator emit `stage: null`, the schema rejected the snapshot, and the
   whole lane skipped. One unheadered doc anywhere in the corpus blocks the
   entire dashboard refresh. This is the same presence-vs-value defect
   class the v1 merge-gate review fixed in agent-capture — it recurred in
   the generator. The generator must degrade per-document (bucket as
   "unheadered", surface as a finding), never invalidate the snapshot.
7. **The lane discards its own diagnosis.** `LaneOutcome` carries only
   "4 error(s)"; the candidate file and validator stdout are deleted on
   skip. Operators cannot learn WHICH four errors without re-running the
   generator by hand against the same pins.
8. **Stale-success status.** The committed
   `health/ideation-dashboard/lane-status.json` still says `result: ok`
   from an older green run while every later run that day failed — failed
   lanes never commit, and the nightly's same-day-report gate skips the
   entire `git add health/` for later runs, silently discarding fresh lane
   output (this same-day discard pattern also affects every other health/
   subsystem on reruns).
9. **No refresh path at all for the deployed site.** The Dockerfile COPYs
   the snapshot into the image ("refreshing it means rebuilding this
   image"); there is no scheduled rebuild/rollout. The live site froze at
   its deploy-time snapshot (already 14+ commits behind within five hours).
10. **Nightly-only regeneration by design** (R14) compounds 9: even with a
    refresh pipeline, the live site could show ~24h-stale governance state
    with no staleness indicator beyond the (mis-worded, divergence-only)
    banner. Needs an always-visible "generated at T, N commits behind"
    stamp.
11. The nightly's report commit was blocked for days by the org ruleset
    (GH013, fixed 2026-07-14 via app bypass) — the lane inherited every
    doc-health pipeline outage invisibly.

**C. Frontend/UX.**

12. **No scrollbars (Brett).** Overflowing panels/lists are unscrollable —
    fixed-viewport layout failure across views.
13. **No search, no filter, no sort, anywhere.** 108 doc cards, 82 cluster
    cards, 27 realized cards; only ordering is a static path sort.
14. The funnel is not funnel-shaped: all 108 governed docs pour into
    column 1 (only 21 are ideation sources; 87 are general corpus docs),
    and only 19 docs carry Topics at all. Corpus health and ideation
    pipeline need to be distinct surfaces, or the source column needs
    scoping.
15. 68/82 topic clusters are single-member with raw ids as names
    (`_titleize` is the identity function); cards read like "AVC-09".
16. Doc-list "other" group header renders twice (grouping compares only
    against the previous item while iterating a path sort).
17. Duplicate roll-up bars on funnel and board tabs (mounted globally AND
    per-view).
18. Stats tile mislabels: "active ideation docs" counts only
    stage==brainstorm (2), invisible-ing 55 draft + 19 staged docs; the
    board likewise hides 87 docs that fit no column.
19. a11y: explorer dialog has no focus trap/initial focus/aria-labelledby;
    tabs lack the ARIA roving-focus pattern; override reasons collected via
    blocking `window.prompt`.
20. Hygiene: incomplete `esc()` (no `'`) in older views vs textContent in
    newer ones; six near-duplicate helper copies; dead `STAGE_CLASS`
    constant; markdown viewer still fetches external `![img](url)` images
    (network egress decision never made).

**D. Local-clone / serving assumptions (Brett's #2, corroborated).**

21. Corrected after live probes (2026-07-14): the deployed image bakes
    the snapshot next to the renderer and serves it fine (deploy evidence
    shows served == committed byte-identical), and the whole site sits
    behind nginx Basic Auth by design. What IS dead on the live site is
    only the `/source/<path>` doc viewer — the container deliberately
    ships `--checkout-root /srv/empty` (static-only v1), so D15's
    read-only viewer 404s in production. The v2 seam should give the
    served backend a real checkout (or proxy) for `/source`.
22. Gate-console copy-paste commands hardcode
    `python3 scripts/ideation_dashboard/cli.py ... --repo-root .` — the
    script lives in codexFactory but acts on openxFactory; no single
    working directory satisfies both as printed.
23. The deployed host has no repo-in-pod mechanism (4.2 deferral), so
    D15's read-only viewer never worked on the live site.

**E. Governance/process debt.**

24. Change unarchived at 25/27; the five dashboard schemas are not yet in
    `contracts/manifest.yaml`/CHANGELOG (deferred to the archive gate);
    task 1.1's schema reconciliation against the sibling change never done.
25. Gate-console trust gaps accepted as v1 risks: unauthenticated
    `--actor`, records-tree-trust ratification (forgeable), un-confined
    `edit_apply` document path. Fine for v1; must be scheduled, not
    ambient.
26. Deployment target deviates from the ratified wording (Nextest QA
    cluster, not the named OS-AKS-QA) — documented, unreconciled.
27. Test suites can't run in one pytest invocation (conftest collision
    between ideation-dashboard and doc-health suites).
28. AI-assist surfaces prominent in the ratified design (suggestion tray,
    derive-possibles, inferred tag strength) are wholly absent from v1 —
    fine as scoping, but v2 should either build or formally de-scope them.

### v2 concept sketch

- **Repo-aware entry.** Allowlist config (schema-versioned, likely an
  extension of `project-register.yaml`: orgs, repos, workspace root) →
  picker listing allowlisted repos with cloned/not-cloned/behind status →
  clone-on-demand → per-repo or cross-repo dashboard. The multi-repo
  roll-up the grouping model already supports becomes real (load N
  snapshots, aggregate the five DomainxFactories + openxFactory).
- **Backend seam.** One small API: `GET /snapshots/<repo>`,
  `GET /source/<repo>/<path>`, `POST /actions/<queue>` (gate/lens
  submissions). Local impl: FS + `gh`. Served impl: workspace service with
  scheduled snapshot refresh + image-free delivery (serve the committed
  snapshot at request time; kill the bake-into-image model).
- **Fix the funnel before decorating it:** ideation-scoped source column;
  possibles from a real index (land the sibling change, or adapt the DTN
  candidate register as an interim possibles source); human cluster names +
  singleton collapse; stage-to-stage conversion counts.
- **Resilience defaults:** per-document degradation in the generator
  (never whole-snapshot rejection for content defects); lane status carries
  the validator detail + run id + commits-behind; loud CI check when the
  committed snapshot falls >N hours/commits behind; always-visible
  staleness stamp in the UI.
- **Table stakes sweep:** scrollbars/virtualized lists, global search +
  filters + sort, single roll-up control, empty-states that explain WHY
  ("cross-reference index not yet landed"), a11y pass, unified DOM-safety
  helpers.

### Tile → NotebookLM (Brett, 2026-07-14)

Every cluster, proposal, and staging-topic tile gets an "Open in
NotebookLM" action that fires up a notebook loaded with exactly that
tile's doc set. The pieces mostly exist; v1 shipped the engine without
the button:

- **Already promoted**: the lifecycle projection (three stage books) and
  the hybrid per-set notebook pattern — a notebook for one staging
  topic's or proposal's supporting-docs set, WITH the governed return
  path (human-converted NotebookLM notes re-enter ideation as
  Status-tagged files via `--import-exports`/`--import-new-sources`;
  `add-lifecycle-notebook-hybrid-imports` is merged and archived — the
  aggregation CLAUDE.md note that it awaits ratification is stale).
- **Already coded, unwired**: `ideation_dashboard/workbench.py`'s
  `NotebookAdapter` creates/deletes `xf-wb-<slug>` notebooks for any
  reference set (cluster-seeded, ad-hoc, recipe-seeded), binds the alias
  in the gitignored workbench manifest, orphan-sweeps unbound notebooks,
  and degrades gracefully when `nlm` is unavailable. No cli.py/serve.py/
  web view calls it today.
- **CLI surface sufficient**: `nlm notebook create`, `nlm source add
  --text/--file`, `nlm notebook get <id> --json` → shareable URL.

v2 shape: the tile action calls the backend seam
(`POST /actions/notebook {tile_kind, tile_id}`); the LOCAL backend wires
it to the existing `NotebookAdapter` (create-or-rebind `xf-wb-<slug>`,
add the tile's docs as titled text sources, return the notebook URL, UI
opens it in a new tab). The SERVED backend cannot hold `nlm` browser
auth (~20-min operator sessions in `~/.notebooklm-mcp-cli/`), so it
either deep-links notebooks pre-provisioned by an authenticated nightly
lane (stage books today; optionally one notebook per staging topic,
automating the hybrid pattern) or hides the action — making this the
poster-child capability for the local/served seam. The return path
closes the loop: read in the dashboard → interrogate in NotebookLM →
notes come back as governed ideation input.

Additional OQs: notebook lifetime for tile notebooks (default: keep the
existing orphan-sweep discipline — a notebook lives while its workbench
manifest binds it); source refresh on re-click (default: diff by title
+ content hash like the lifecycle sync manifest does); whether proposal
tiles load only supporting-docs or also the proposal/design/tasks files
(default: all of the change dir minus review records).

### Open questions (defaults proposed)

- **Allowlist config home**: extend `project-register.yaml` vs a new
  `dashboard-workspace.yaml`? Default: extend project-register (it already
  models repo→project→group and its group layer is an empty stub waiting
  for exactly this).
- **Interim possibles source**: wait for
  `add-ideation-cross-reference-readiness` vs adapt the DTN candidate
  register now? Update while drafting this section: that sibling change went
  ACTIVE the same evening (W1 index-contract keystone a7aac77, W2 validator
  + living index acbc98f, 2026-07-14 ~17:30-17:52, another session's track)
  — so the default flips to: wait for the real index, no interim DTN
  adapter; v2's possibles wiring should target the landing contract and
  reconcile dashboard task 1.1 against its final wording.
- **Served-backend write actions**: does the hosted instance accept gate
  actions at all, or stay read-only with actions local-only until the
  gate-console trust gaps (25) are hardened? Default: served = read-only;
  actions only through the local backend until authn lands.
- **Snapshot-per-repo vs one aggregate snapshot**: default per-repo
  snapshots + a thin index; the aggregate view composes client-side.

### Triage ledger (2026-07-15, post-redeploy reevaluation)

Live site redeployed 2026-07-14 evening (served snapshot byte-identical to
b4b0d65: 116 docs, 89 clusters, source_revision 0fcf01ae, resilient-lane
fields live). Strict per-bug triage against codexFactory 426c972 +
openxFactory 0fbea59:

- **FIXED (4):** 6, 7, 8 (PR #9 — per-document degradation, diagnosis
  retention, same-day commit; all verified in code), 11 (GH013 app bypass).
- **Corrected/moot (1):** 21 (register text already amended; the residual
  real defect is the dead `/source` viewer = 23).
- **Partial/in-progress (3):** 1 — the premise flipped:
  `ideation/cross-reference.yaml` NOW EXISTS (sibling W1/W2), but as an
  all-unscored bootstrap with the `possibles_register` section deliberately
  absent, and the dashboard's adapter reads a key the bootstrap doesn't
  carry — so possibles is still 0 and every downstream edge still dead;
  the funnel middle now has a CONTRACT but no DATA. 10 — lane-status
  gained run_id/generated_at (PR #9) but no commits-behind field and no
  UI staleness stamp. 24 — task 1.1's schema reconciliation discharged;
  manifest registration + archive still pending (sibling at 15/16).
- **OPEN (20):** 2-5, 9, 12-20, 22-23, 25-28 — the entire frontend sweep
  (web/ is byte-untouched since v1), the refresh pipeline, funnel scoping,
  gate-console hardening, and the AI-assist build-or-descope decision.

Numerically the render got worse with real data: 93/116 docs (80%) are
topic-less orphan cards in column 1; 70/89 clusters are singletons; 0/36
changes show ratification. The bootstrap index carries human topic names
('Avatar Client') that the snapshot clusters don't consume — a cheap win
waiting. What turns the funnel middle ON is the sibling's remaining
substance (possibles_register population + the scoring worker) plus
generator wiring against the landed schema — v2's data spine should be
scoped to consume exactly that landed contract.

## v2 Exit

Same two-repo split as v1: an openxFactory delta (allowlist/workspace
config schema, snapshot index contract, per-document degradation rules,
lane-status enrichment) paired with a codexFactory delta (backend seam +
local/served implementations, repo picker, funnel scoping, frontend sweep).
Bugs 6-8 (stage:null DoS, discarded diagnosis, stale-success status) are
small, severable fixes that should not wait for v2 scoping.
