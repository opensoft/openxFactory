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

### Background notebook pre-provisioning (Brett, 2026-07-16 — v5 candidate)

Pre-create notebooks in the background for each STAGING folder so
launching NotebookLM from the dashboard is instant. The PR #15 machinery
makes this nearly free: create-or-rebind + content-hash sync is
idempotent, so the pre-provisioner is the same call looped over staging
topics; click-time then hits the existing no-op path (hashes match →
immediate URL return).

- **The policy (Brett, 2026-07-16): notebook permanence follows document
  lifecycle.** A click on a possible/cluster loads its notebook REALTIME
  (the PR #15 on-demand path — exploration is ephemeral, and on-demand
  latency is acceptable for it); a concept PROMOTED TO STAGING earns its
  own dedicated, pre-provisioned notebook (deliberation is persistent).
  Also quota-correct: 5 staging topics vs 89 clusters against
  NotebookLM's notebook limits.
- **Two warming triggers**: (a) serve.py startup — a background thread
  syncs staging notebooks while the operator looks at the funnel;
  warm-if-authenticated, silent skip on a stale nlm session; (b) the
  nightly lane on the authenticated host — the served-mode
  pre-provisioning posture above, enabling deep-links from the deployed
  site or a phone.
- **Lifecycle**: the pre-provisioner regenerates each topic's workbench
  manifest per run; a topic that exits staging stops being regenerated
  and the existing orphan sweep collects its notebook. No new lifecycle
  machinery.

**The four notebook types (Brett, 2026-07-16)** — and the set-first
discipline beneath them: **no notebook without a set, no set without a
manifest** (the orphan sweep keys on manifests; the four notebook types
ARE the four set types):

| # | Type | Set source | Lifetime |
|---|---|---|---|
| 1 | Stage books (ideation/drafts/canon) | `Status:` headers, automatic | permanent, synced |
| 2 | Staging-topic notebooks | staging folders, automatic | while the topic lives |
| 3 | Realtime tile notebooks | cluster/possible/proposal click | ephemeral, on demand |
| 4 | Ad-hoc workbench notebooks | user-assembled reference set | while its manifest lives |

Corrections to the naive model: users do NOT create clusters by
selecting docs — clusters derive from `Topics:` headers, and a `Status:`
header alone puts every governed doc into a stage book with zero user
action. The one true "select docs → notebook" path is type 4, the
keyword lens's assembled set — **and PR #15 did not wire the notebook
button onto it** (buttons landed on funnel/board/canvas cards only).
v5 item: "Open in NotebookLM" on the lens's assembled reference set —
the one surface where users literally hand-pick docs is currently the
one without the button.

### Doc-location and NotebookLM connectivity (Brett + discussion, 2026-07-15)

Design ground for the hybrid backend seam. The pivotal observation: **the
repo is already the database** — the nightly lane commits `snapshot.json`
into the aggregation repo and the governed docs ARE the repo, so "where do
the docs live" reduces to *who fetches from the repo, when*. Four models:

| | Local clone | Baked server copy (served mode today) | Live server workspace | Repo-direct (the Claude-Code-mobile parallel) |
|---|---|---|---|---|
| What | operator's checkouts | corpus frozen into the image | server keeps a pulling clone | UI fetches straight from GitHub (raw snapshot.json + contents API) |
| Freshness | as fresh as your pull | frozen at build (the staleness bug class) | minutes | always current |
| Doc viewer | yes | yes since v4, frozen | yes | yes (raw fetch) |
| Actions | full | none | partial (writes as PRs) | writes become PRs/issues via API — matches the rolling-PR delivery model |
| Ops burden | clone mgmt (v2 repo picker) | rebuild+redeploy per refresh | pod + sync loop + repo creds | near zero: static page + a token |
| Auth | your git | ingress Basic Auth | server-held repo creds | fine-grained PAT in browser, or a thin GitHub-App proxy (~the whole "served backend") |
| Mobile/anywhere | no | yes | yes | best |

Direction: **local clone stays the action-rich operator mode; repo-direct
is the served mode's destination; the baked image is a stopgap** we now
understand as such. Repo-direct dissolves three standing bug classes at
once (staleness, the missing refresh pipeline, the served doc viewer) at
the cost of one problem — private-repo credentials in a browser — solved
by a pasted fine-grained PAT (single-operator) or a tiny GitHub-App proxy
(team).

**NotebookLM connectivity, corrected:** consumer NotebookLM has NO
official public API. The `nlm` CLI (`notebooklm-mcp-cli`) is
session-automation: `nlm login` opens a browser and the Google session
(~20-minute lifetime) lands in `~/.notebooklm-mcp-cli/`; every call
replays that session against the web endpoints. The MCP flavor is the
same tool exposed as an MCP server — same auth underneath, not a second
channel. This is WHY the served backend cannot create notebooks: holding
a user's live Google session cookies server-side is structurally
unacceptable, not an engineering gap. The only true service-API path is
NotebookLM Enterprise (Google Cloud/Agentspace, IAM/service-account) —
worth a fresh capability check before ever betting on it (knowledge-
cutoff caveat recorded).

Three integration postures, per mode:
1. **Local (SHIPPED, v4 PR #15):** tile button → `nlm` under the
   operator's session; capability-gated, invisible elsewhere.
2. **Served/repo-direct, pragmatic:** no live creation — a nightly
   pre-provisioning lane on an already-authenticated host builds one
   notebook per staging topic/cluster and the UI deep-links. The Cloud PC
   artifact-worker host is the proven pattern for keeping interactive
   auth alive (it already does for claude); an `nlm` session there is the
   same shape.
3. **Served, someday:** Enterprise API with a service identity — only if
   multi-user demand justifies procurement.

Bonus from the mobile parallel: the USER'S browser is already logged into
Google, so deep-links into pre-provisioned notebooks work from any device
with zero credential machinery. Repo-direct UI + pre-provisioned
notebooks = a fully-current dashboard usable from a phone, NotebookLM one
tap away — no pod, no bake, no session juggling. This section supersedes
the earlier "Served-backend write actions" OQ default where they differ.

### v5 candidates (Brett's live v4 feedback, 2026-07-16)

v4 deployed and operator-tested on the hosted site. Six items, verbatim
intent preserved:

1. **Possibles column is blank — so generate possibles.** Confirmed
   data-level: the landed cross-reference index's possibles_register is
   deliberately absent (bootstrap), adapter correct since PR #12. Brett's
   direction: "it must be that we have possibilities — that is what we
   want our AI system to do, help think of possible connections." →
   the **derive-possibles worker lane**: a bounded Omnigent lane (same
   shape as the cataloger, same model-worker contract lessons) proposes
   candidate possibles into the register with `pending_review`
   disposition; humans dispose on the gate console. This was the ratified
   v1 design's deferred AI-assist surface — now the headline v5 data
   item.
2. **Carousel, not horizontal scroll.** The viewport must not scroll
   horizontally pixel-by-pixel: discrete column-by-column navigation with
   arrow buttons.
3. **Column visibility toggles.** An eye symbol in each column header to
   show/hide that column; hidden = header collapses to just the eye, no
   column data, remaining columns close in so the viewport focuses on
   what's visible. Brett: unsure the eye is right — think of alternative
   GUI elements for column on/off (icon-tray? checkbox legend? click the
   carousel dots? column header context menu?).
4. **THE WHEEL (funnel navigation paradigm).** Each column becomes a
   vertically spinning wheel (slot-reel / iOS-picker style). Hover over
   the column you want to adjust; the MOUSE WHEEL spins that tile-wheel;
   the selected item lands in the vertical CENTER position, magnified
   ~30-40% to show focus (click or wheel-align to select). Then the
   OTHER column wheels spin automatically to bring the items CONNECTED
   to the centered one into alignment in the viewport — selection in one
   column rotates the neighbors so its relations line up on the center
   row. (The funnel's existing trace machinery already computes the
   connection sets; the wheel is a re-render of trace as alignment.)
   Paradigm-level redesign — deserves a mockup round before code.
5. **Connection-count badges on tiles.** Every tile shows the NUMBER of
   items it links to per neighbor class (documents, topic clusters,
   possibles, active proposals, archived) — and each count is a link to
   a view that enlightens the user about those connections.
6. **Menu scrollbar bug.** The tab menu (realization / pipeline /
   cluster / keyword / doclist / lineage) shows an unneeded vertical
   scrollbar in that small area — remove (likely v4 shell fallout: a
   height constraint on the tab strip).

### THE WHEEL — locked interaction spec (Track C, Brett-approved 2026-07-16)

v5 candidate 4 graduated through two interactive prototype rounds (a
session-built mockup on the real `0fcf01ae` snapshot: 26 ideation docs,
89 clusters, 5 staged, 7 active, 29 archived, 137 indexed doc→cluster
edges; possibles synthesized and demo-marked since the register is
empty). Brett drove both rounds and locked the second: "the wheels are
great … this is good, lets lock this in." Spec below is LOCKED for the
v5+ realization; only the eye-vs-dock choice (candidate 3) stays open.

**Deck.** Six wheels in funnel order — documents → clusters → possibles
→ staged → active → archived — crossed by one horizontal brass FOCUS
LINE at viewport half-height. Discrete carousel (locks candidate 2):
arrow buttons / ←→ keys page column-by-column with scroll-snap; no
horizontal scrollbar, no pixel scrolling.

**Spin & focus.** Hover a wheel and the mouse wheel spins it in
whole-tile steps (↑/↓ likewise; clicking a tile centres it). Only the
FOCUSED wheel magnifies: its centred tile scales ~1.35 onto the focus
line and carries the per-class connection chips.

**Elastic alignment (the round-2 refinement that locked it).** When the
focused wheel seats on an item, each connected wheel takes a SOFT turn
that rests its linked tiles BALANCED around the centre line — group
centroid, nudged ±0.45 step if any tile would land dead-centre; a single
linked tile parks ~0.8 step off-centre. The other wheels are never
centred-and-magnified: a tile exactly on the line collapses its thread
into a flat connector, and magnification is reserved for focus. Linked
tiles get a teal edge only. Clicking a linked tile TRANSFERS focus —
that wheel centres + magnifies and the pull radiates from it instead.

> **The alignment MATH above is SUPERSEDED — Brett, 2026-08-21.** What a
> wheel does now depends on how many CONNECTING STRINGS it is showing
> (threads from the focused context to its own tiles — first-degree when
> it has any, else the dimmed second-degree set):
>
> 1. **No connecting string** — nothing to align on, so the wheel rotates
>    so its FILLED tiles are centred in the viewport: the group of real
>    tiles centred on the visible band, biased toward no tile in
>    particular. (Previously the wheel simply kept its position, which at
>    load is the first item on the line with the upper half of the band
>    blank filler.)
> 2. **Exactly one connecting string** — the connected tile rests NEAR
>    the centreline, deliberately NOT on it, at the named `ALIGN.near`
>    offset. That offset IS the ~0.8 step above: the single-tile park is
>    unchanged, it is now the canonical "near, not on" distance.
> 3. **Several connecting strings** — one of the connected tiles MAY sit
>    ON the centreline, and does: the one needing the smallest rotation
>    from the wheel's current position (lowest index breaks a tie). The
>    others stay visible where the geometry allows.
>
> Rule 3 is the inverse of the ±0.45 dead-centre nudge, so that nudge is
> REMOVED rather than scoped, and the group no longer rests on a centroid
> (nor on the span midpoint the 2026-07-23 delta had replaced it with).
> Everything else in this paragraph stands: pulled wheels are still never
> magnified, linked tiles still take a teal edge only, and clicking a
> linked tile still TRANSFERS focus. These rules govern AUTOMATIC
> alignment only — a human's own click still centres the clicked tile
> dead on the line.
>
> Realized in `scripts/ideation_dashboard/web/views/wheel-model.js`
> (`alignTarget` · `filledGroupCentre` · `centredChoice` · `ALIGN.near`),
> consumed by `wheel.js`'s single `alignFor` call site, pinned by
> `tests/ideation-dashboard/test_wheel_model.py`.
>
> Two earlier deltas to this paragraph, recorded here for the same
> reason: the group target became the linked SPAN MIDPOINT rather than
> the centroid (Brett, 2026-07-23 — now itself superseded by rule 3), and
> a wheel with MANY linked tiles REARRANGES rather than stacking them,
> seating the linked block in consecutive slots at the centre (Brett,
> 2026-07-24, `computeReorder`; extended 2026-07-25 to gather the
> second-degree tiles into the same block). Those two stand.

**Physics ("mass" + elastic connectors).** Wheels are spring–damper
systems: the user-driven wheel runs stiffness .020 / damping .84 (real
inertia, slight overshoot before seating); pulled wheels run .008 / .90
so they trail behind — the threads visibly drag them. The pull is LIVE:
as the driven wheel crosses each tile mid-spin, connected wheels
retarget continuously rather than jumping once at settle.
prefers-reduced-motion ⇒ instant snap, no springs.

**Threads.** SVG beziers from the focused centre tile to visible linked
tiles, class-coded: solid teal = indexed edge, dashed teal = inferred,
dashed brass = synthesized/demo. Because pulled tiles rest off-centre,
threads keep visible curvature at rest.

**Tiles & badges (locks candidate 5).** Every tile: two-line label,
class subline (stage / n files / n docs), total-degree pill. The focused
centred tile adds "n ⟨class⟩" chips per connected class; clicking a chip
pages the carousel to that column (expanding it if collapsed) and pulses
it — the chip is the "view that enlightens" entry point.

**Column hiding (candidate 3 — deliberately open).** The mockup ships
BOTH affordances sharing one state for A/B feel: a header eye collapsing
the column to a thin vertical rail, and dock chips along the bottom
edge. Brett picks after more driving; realization carries the survivor
(or both).

**Possibles honesty rule.** While `possibles_register` is empty the
wheel may show SYNTHESIZED possibles derived from real clusters/staged
topics — each dash-bordered, "demo"-tagged, threaded in dashed brass —
never visually confusable with indexed data. Placeholder until the
derive-possibles lane (v5 item 1) populates the register.

**Realization data contract.** The mockup inferred cross-class edges by
token overlap; the real wheel needs the snapshot (or server-side
derivation) to carry MATERIALIZED cross-class edges — cluster→staged,
staged→change (active/archived), possible→cluster/staged — plus
per-item degree counts, each edge carrying a class field
(indexed | inferred | synthesized) that drives thread styling. Exit:
same v2 two-repo split; the wheel lands as a new codexFactory
`web/views/wheel.js` view once the v5 Track A fixes settle.

### Hosted NotebookLM: service identity + native sharing + Keycloak (Brett, 2026-07-16)

The hosted site now has the DOCUMENTS (v4 bakes the checkout); the
blocker is Google identity. Two proposals, complementary:

**A. Org-owned NotebookLM account + native sharing.** The
pre-provisioning lane runs `nlm` as an org WORKSPACE identity (e.g.
xfactory-notebooks@ — Workspace, not consumer: shared personal accounts
are a Google ToS gray zone; Workspace gets admin controls). Notebooks are
created under the service identity and SHARED to individual users via
NotebookLM's native sharing — **the share list IS a grant list** (share =
grant, unshare = revoke, per-notebook scope): the first real openxWallet
grant implementation, enforced by Google's own ACLs, zero crypto on day
one. Users open shared notebooks in their OWN Google context — browser or
the iOS app via deep link.
STRUCK CLAUSE: embedding NotebookLM in the hosted page. Google apps
refuse framing, and proxying the service session would hand every hosted
user the whole service account's reach (cross-user leakage) — the hosted
page renders deep-links to the notebooks shared with YOU; the notebook
always opens in Google's own surface.
Operational risk to test: the ~20-minute nlm session means the service
account needs a maintained login on the authenticated host (Cloud PC
pattern: persistent browser profile, provisioning in batch windows).

**B. Keycloak — right tool, different job than stated.** Brokering
Google login yields the user's IDENTITY, never their NotebookLM session
(no OAuth scope drives NotebookLM). Keycloak's real jobs here: (1)
replace the hosted site's Basic Auth with SSO (connects to the existing
keycloak-identity-brokering brainstorm); (2) its Google-brokered identity
DRIVES option A's share lists — knowing the user's email, the lane shares
their notebooks and the dashboard renders THEIR links; (3) bridge IdP for
openxWallet while DIDs mature, and the identity that would map to
per-user NotebookLM Enterprise API calls if that path is ever procured.

**Synthesis:** Keycloak login → identity → service-provisioned notebooks
shared to that identity → deep-links in the hosted page → opens under the
user's own Google session anywhere (incl. iOS). Server never holds user
creds; service creds never leave the authenticated host; nothing
embedded.

### Custody tiers: git as the traceability plane (Brett + discussion, 2026-07-15)

Principle: **system of record ≠ traceability plane.** The EMR is where
medical records live; the client's books are where ledger data lives; you
cannot and should not force those into git. What the system requires is
the EVIDENCE plane: **every use of this tool requires a git repo, where
the inputs to a governed analysis are hash-locked at the moment of use.**
Source docs join under one of three custody tiers:

| Tier | Domains | What's in the repo |
|---|---|---|
| Repo-native | codex; most Ledgerx working papers | the docs themselves, fully versioned |
| External system-of-record | Medx (EMR), bank/ERP feeds | an evidence manifest: opaque locator + content hash + retrieval provenance (system, record id, as-of) — plus only policy-permitted derived extracts |
| Drive-hosted (OneDrive/GDrive) | ad-hoc client folders | treated as external sources — manifests + optionally mirrored copies |

The primitives already shipped as `contract-v1.11` (document-cataloging):
per-doc `content_hash` with source-freshness enforcement, the
opaque-locator kernel (reference a document without storing path or
content), the handling-gate kernel (`policy_blocked` unless authorized),
immutable `status: record` snapshots. The Medx and Ledgerx tiers are
configurations of that machinery, not new systems.

**Engagement model:** an audit or clinical analysis = a branch (or
engagement repo). Evidence manifests hash-lock every source at the
version analyzed → the NotebookLM notebook is loaded from exactly that
manifest → generated material commits alongside → the decision/opinion is
tagged. Verifiable later: THIS conclusion came from THESE bytes.

**Hard rules (Brett, 2026-07-15):**
1. **PHI never enters GitHub.** Tier-2 manifests carry hashes and opaque
   refs, never content. Because raw content-hashes of guessable records
   can leak by dictionary attack, protected-tier manifest hashes are
   salted/HMAC — extend the opaque-locator kernel's domain separation
   with an engagement-scoped key held OUTSIDE the repo.
2. **No PHI enters NotebookLM. Ever.** NotebookLM is Google-hosted,
   consumer session-auth, not a BAA-covered pipeline. Loading a notebook
   IS a dispatch across a custody boundary — the same handling-gate shape
   as the cataloger's dispatch gate.
3. **Sanitize before dispatch.** A sanitization process runs before any
   protected-tier doc reaches a notebook: strip/replace direct
   identifiers, with **salted deterministic pseudonymization** — PHI
   identifiers become HMAC-derived pseudonyms under an engagement-scoped
   salt, so "Patient A" stays consistent across the engagement's docs
   (the analysis still works) while being unlinkable outside it and
   reversible only by the key-holder inside the boundary. The evidence
   manifest records BOTH the original's salted hash reference and the
   sanitized derivative's plain hash — trail from opinion → sanitized
   inputs → (inside the boundary only) original records. This is the
   generalization of the cataloging contract's redacted-dispatch rule
   ("redacted dispatch MAY occur only when source policy explicitly
   authorizes the redacted derived view") into a reusable sanitizer
   worker — a natural bounded Omnigent lane, same shape as the cataloger.

Dashboard consequences: the v2 allowlist config gains a **custody profile
per repo/source** (native / manifest / drive-source); the repo picker
enforces "no repo, no workload"; the NotebookLM action consults the
handling gate + sanitizer before loading sources. Git-inside-a-Drive
folder is an anti-pattern (sync clients corrupt .git, race refs), not a
fourth tier — treat as tier 1 with a health warning if encountered.

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

### v4 candidates (Brett's live v3 feedback, 2026-07-15)

Bugs observed using the deployed v3 site, verbatim intent preserved:

1. **Lens fold-aware scrollbars**: keyword-lens columns must gain a
   scrollbar once they extend to within ~10% of the fold — cap columns at
   ~90vh with overflow-y auto so nothing approaches the bottom edge
   unscrolled.
2. **Mystery second scrollbar**: funnel/board/canvas/lens list menus show
   an extra right-side scrollbar of unclear purpose — likely a nested
   scroller introduced by the v3 sweep (roll-up body cap or `.scroller`
   wrapper) stacking against the page scrollbar. Consolidate to ONE
   scroll context per region; a scrollbar whose owner the user can't
   identify is a defect even when functional.
3. **Global layout contract**: on every screen, no column may run off the
   bottom of the viewport — all columns viewport-bounded with their own
   scrollbars, keeping every widget reachable within one screen height.
   This is a layout-system rule, not per-view CSS patches; v3 fixed
   instances, v4 should fix the contract.
4. **Live `/source` 404s** (e.g.
   `ideation/staging/avatar-pilot-hardening/avatar-pilot-hardening.md`):
   register #23 confirmed by the operator on the live site. Fix: bake the
   pinned openxFactory checkout into the image (the build context already
   contains it) and set `--checkout-root` accordingly — turning D15's
   read-only viewer ON in production. Owner surface: omnigent-install
   Dockerfile + deployment args; serve.py already supports it.
5. **Tile → NotebookLM pulled forward**: the operator cannot see how to
   start NotebookLM from a doc set — because the button was scoped out of
   v3. Promote the "Tile → NotebookLM" capability (see its section above:
   wire the existing NotebookAdapter through a local-backend action) into
   the next fix round rather than the next major version. Served-instance
   behavior per that section (deep-link pre-provisioned books or hide).

## v2 Exit

Same two-repo split as v1: an openxFactory delta (allowlist/workspace
config schema, snapshot index contract, per-document degradation rules,
lane-status enrichment) paired with a codexFactory delta (backend seam +
local/served implementations, repo picker, funnel scoping, frontend sweep).
Bugs 6-8 (stage:null DoS, discarded diagnosis, stale-success status) are
small, severable fixes that should not wait for v2 scoping.

## Domain drive + the runtime plane (2026-07-25)

Design session (Brett Heap, Claude) on the repo selector and where the
dashboard ultimately lives, followed by a live drive of the v1 dashboard
against three domain factories. This section records the decisions, the
one genuinely open fork, and what the drive showed.

### Decided 2026-07-25 (Brett)

1. **The runtime plane is the real goal.** The dashboard becomes a
   neutral xFactory capability that every DomainxFactory install ships: a
   running MedxFactory serves its own wheel over its tenant's domain ideas
   (e.g. patient-management ideas) held as governed content in that
   install's stack — not as repo files. The dev dashboard (this doc's v1/v2
   subject) is the dev instance of the same capability pointed at a
   filesystem corpus. Structurally this makes the snapshot generator's data
   source an adapter seam: filesystem-corpus adapter (dev) vs
   governed-content adapter (runtime); the neutral snapshot schema is what
   makes the seam possible.
2. **The two planes are separate systems.** In the dev dashboard, setting
   the selector to `xFactory` shows the dev-time code-and-ideas corpus of
   ALL the submodule repos — but it has no access to what a running
   install holds (a codexFactory dev dashboard never sees the installed
   MedxFactory's patient ideas). No plane-crossing data path exists.
3. **Per-repo snapshots + a thin index** (re-affirms the v2 sketch
   default): the lane generates one snapshot per registered repository;
   the selector switches snapshots; the aggregate view composes from the
   index/client side. `serve.py` grows per-repository snapshot routes and
   multi-root source confinement.
4. **Sparse wheels are honest.** A repo shows whatever stations it has
   data for; install repos with only `openspec/changes/` (hermes-install
   etc.) render active/archived and nothing else. No convention adoption
   is forced as a precondition of being selectable.

### Open fork (named, undecided)

One neutral dashboard living in openxFactory that handles all domains as
is, OR a neutral core with per-domain overrides in each DomainxFactory
(the digest-pinned overlay pattern the omnigent contract family uses).
Driving the unmodified dashboard in the domains is the deliberate
experiment to inform this split: whatever survives contact unchanged is
neutral core; whatever feels wrong per domain is an override point.

### Drive findings (2026-07-25)

The v1 dashboard (codexFactory `scripts/ideation_dashboard/`, current
wheel UI) was run unmodified against MedxFactory, AdxFactory, and
LedgerxFactory: per-repo snapshots generated with `--repository` +
`--project-register` pointed at the aggregation register, served as three
session-local loopback instances; no repo was touched.

1. **The generator is already repo-agnostic** — zero code changes to
   snapshot Medx (31 documents / 1 change), Adx (7 / 1), Ledgerx (9 / 3).
   Scan, snapshot schema, and wheel rendering all look like neutral core.
2. **The funnel's middle is empty in every domain**: clusters, possibles,
   and staged wheels feed from the ideation cross-reference index and
   staging conventions that today exist only in openxFactory. Either
   domains adopt those conventions (pure neutral core) or a domain
   override redefines what feeds those stations. This is the biggest
   neutral-vs-override pressure point found.
3. **Post-render validation skipped cross-repo** ("no reachable
   openxFactory checkout"): pinned-validator discovery assumes the
   codexFactory checkout layout. The neutral version needs explicit
   pinned-contract discovery, not positional.
4. **The vocabulary test is the point of the drive**: whether the six
   stations (documents → clusters → possibles → staged → active →
   archived) and the action verbs (propose, gate, notebook) are neutral or
   codex-specific is exactly what driving Medx/Adx/Ledgerx wheels should
   answer. Caution for drivers: gate-console verbs are LIVE against the
   selected checkout (they write gate-action records); drive the read
   surfaces freely, treat gate verbs as armed.

### Exit for this section

Dev-plane findings fold into the v2 exit above (same two-repo split; the
index contract and multi-root serving are already named there). The
runtime plane routes separately when scoped: an openxFactory
neutralization change defining the governed-content adapter seam and what
an "idea" is as install content, registered as a domain-neutralization
candidate.

Organized 2026-07-25 into the
[dashboard-repo-selector](../staging/dashboard-repo-selector/dashboard-repo-selector.md)
staging topic (decisions, open fork, drive findings, and both exits carried
there; this section stays as the brainstorm-side record).
