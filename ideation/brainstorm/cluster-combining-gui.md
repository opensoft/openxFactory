# Cluster Combining GUI — Brainstorm

Status: staged
Kind: architecture
Summary: GUI concepts that make the funnel's generative zone (docs → clusters → possibles) an active working surface instead of a rendering — a cluster canvas with an evidence board and gap prompts, a possible composer with option-set comparison, drag/lasso combining gestures, topic-chip faceting, and pending-review AI suggestion trays — all inside the dashboard's non-mutating / human-edit / agent-create-only boundary.
Topics: ideation-dashboard, workbench, possibles-register, gui-design, ideation-tooling, doc-management, doc-workflow
Repository context: openxFactory (feeds the ideation-dashboard staged topic)
Captured: 2026-07-13
Organized: 2026-07-13 — the cluster canvas and keyword lens entered the
add-ideation-dashboard re-proposal as decisions D12/D13 with spec
requirements and tasks; kept as design history with the full option space
inline.
Origin: D11 follow-through session (Brett + Claude, 2026-07-13). Brett: the
first three funnel columns are where feats are made — "make tools to make
this combining process easy for the user."

Brainstorm — contradiction and half-formed options are legal here.

## The problem

Right of the pick, the funnel is one identity promoted through gates (D11);
the GUI's job there is honest state. Left of the pick — doc pool → clusters
→ possibles — is where many docs get organized around a feat area and the
feat's candidate shapes are derived and chosen. Today's GUI renders that
zone and collects doc sets (assemble button, doc-list checkboxes, tray) but
does not host the combining itself: seeing across docs, deriving options,
shaping one feat. Every tool below must respect the decided boundary: the
dashboard's machinery never mutates sources, humans create/edit through
scaffold + their own editor, agents create only into pending-review queues
(D5, D7–D9).

## Zone A — doc pool (column 1): make relatedness visible

- **Topic-chip faceting with co-occurrence counts.** Chips are clickable
  filters; combining chips shows intersections ("doc-health ∧
  ai-generation → 2 docs"). Chip algebra is the cheapest cluster-discovery
  tool because Topics: headers already exist.
- **Hover summaries** from `Summary:` headers — hold a corpus in your head
  without opening files.
- **Unclustered shelf.** Docs whose topics match no current cluster sit in
  a visible "raw material" band — an invitation, not a defect.
- **Drag-to-cluster membership gesture.** Dropping a doc on a cluster
  proposes membership; realized as a scaffolded `Topics:` edit opened in
  the human's editor (or a pending-review suggestion), never a silent
  write.
- **Similarity lens** (later): hover a doc → related docs stay lit. Topic
  overlap first; semantic similarity only as a human-reviewed assist.

## The keyword lens — bullseye set-builder (Zone A elaborated; Brett, 2026-07-13)

Brett's concept: a list of the corpus keywords/tags, each showing how many
docs reference it and the correlation strength per doc. Click a keyword →
see its docs with strengths. Check more keywords → the doc set grows, with
union AND intersection both visible: concentric circles where the outer
ring holds docs matching one checked keyword, each ring inward matches
more, and the innermost circle holds docs that check all the boxes; closer
to center = more relevant. Docs are clickable (view/edit) and carry a +/−
toggle for inclusion in the forming cluster; the included set becomes a
cluster fed to the rest of the boards.

Refinements from the session:

- **Bullseye beats Venn.** Ring index = match count scales past the 3-set
  Venn limit. Sector each ring by WHICH subset matched, so "these docs
  share A+B but lack C" is a visible wedge. Always pair with an
  UpSet-style matrix/list as the flat fallback view.
- **Two strengths, visually distinct.** Declared (keyword in the Topics:
  header — solid dot, binary today) vs inferred (cataloging classifier
  confidence 0–1 with pending/suggested/reviewed states — hollow dot).
  v1 rings are pure match count; strength gradients arrive with the
  cataloging change. A machine guess never renders as an author
  declaration.
- **Check = stratify, pin = require.** Checked keywords shape the rings;
  pinning one makes it a hard filter that collapses the lattice.
- **Next-keyword assist, deterministic.** Co-occurrence hints against the
  current selection: "adding credential-contracts pulls 2 docs into
  ring 2."
- **Overrides are evidence.** Manual + on a non-matching doc records a
  reason and emits a scaffolded Topics: edit (under-tagged doc) or a
  human-seen signal (missing vocabulary term); manual − on a matching doc
  is negative evidence (tag too broad / mis-tagged). Both feed the tag
  suggester and organizer queues. Never a silent set edit.
- **Clusters as recipes.** Save the query — checked, pinned, overrides +
  reasons — in the workbench manifest, not just the doc list. An
  intensional cluster stays live: re-running the recipe as the corpus
  grows surfaces "new candidates since last review." Durable promotion is
  the existing human-seen path into the cross-reference index (R8), with
  the recipe as rationale evidence.
- **Scale + boundary.** Rings aggregate into expandable count bubbles past
  ~30 docs; hover cards carry title/summary/chips; click previews, ✎
  launches the human's editor (D7); inclusion state lives only in the
  manifest.
- **Placement.** The lens is the cluster canvas's front door: keyword lens
  → forming set → open as canvas → compose possibles → pick. It absorbs
  the topic-chip faceting and similarity-lens bullets above.

## Zone B — cluster canvas (column 2): the war room

The headline concept: clicking into a cluster opens a focused workspace —
the funnel remains the overview; the canvas is where combining happens.

- **Layout:** member docs (with summaries) down one side; an **evidence
  board** in the middle; this cluster's possibles down the other side.
- **Evidence board.** Pin passages pulled from member docs. The cataloging
  contract already defines section reference + passage hash, so every
  pinned quote carries provenance; a possible built from pinned evidence
  cites its passages from birth.
- **Gap prompts, not gap stats.** "3 docs unclaimed by any possible"
  renders as an empty possible slot asking to be filled; "possible with no
  doc support" renders as a dangling claim needing evidence or deletion.
- **Merge/split gestures.** Select two clusters → "propose merge"; lasso a
  doc subset → "split as candidate cluster." Both land as pending-review
  entries in the organizer/human-seen queue (R8), not direct mutations.
- **Overlap strip.** Shared docs and shared possibles between clusters get
  a first-class lane (the violet shared case) — a feat wanted by two topic
  groupings is a strong signal, so show it, don't bury it in edge spaghetti.

## Zone C — possibles shaping (column 3): the feat takes shape

- **Possible composer.** A structured mini-form: name, one-line claim,
  evidence (dragged from member docs/board), option-set membership, state.
  Output is a drafted possibles-register entry for human commit — the
  registered shape (states, citations) made tactile.
- **Option sets.** Possibles that are alternative shapes of ONE feat group
  explicitly, with a compare strip: claim, evidence count, readiness
  signal, open questions side by side. Choosing one marks siblings
  `superseded` with the required reason + citation (R2) in a single
  gesture.
- **AI suggestion tray** (agent create-only). "Suggest possibles from this
  cluster" dispatches a bounded agent over member docs; candidates arrive
  pending-review with cited passages; the human drags accepted ones into
  the column. Integration point for the AI tag suggester and the
  generation-engine lanes named in the staged topic's integration map.
- **"What would this take?" preview.** On any possible, the seed-to-spec
  lane drafts a skeleton (scope in/out, claims, open questions) as a
  disposable preview; approving it becomes the draft-organize packet — the
  bridge from possible to staged pick.
- **Latent aging heat.** Old latent possibles warm in color — backlog that
  should be promoted or culled, mirroring staged-candidate-aging.

## Cross-cutting gestures

- The workbench tray grows two actions beyond notebook/readiness/health:
  **compose possible** (manual) and **derive possibles** (AI, pending
  review).
- **Provenance ribbons:** selecting a possible highlights back to exact
  passages, not just docs — the deep version of the funnel's thread trace.
- **Resumable sessions:** a combining session (doc set + board state)
  persists in the gitignored workbench manifest (R6) — close the tab,
  resume the war room.
- **Keyboard flow:** j/k to walk cards, space to add to set, p to pin —
  the combining loop without the mouse.

## Boundary fit

Every tool maps onto the decided authority model: canvas/board/faceting are
read-and-assemble (machinery, non-mutating); composer/scaffolds/Topics
edits are human create/edit via editor launch (D7); suggestion trays and
merge/split proposals are agent-create-only into pending-review queues
(D8/R8); nothing executes a gate (D5).

## Candidate v-next cut

Cluster canvas + gap prompts + possible composer + option sets — all
renderable from the snapshot plus the possibles register, no new AI
dependencies. The AI suggestion tray and seed-to-spec preview follow when
the generation-engine and organizer lanes land (see the staged topic's
integration-candidates map).

## Possible feats

- Keyword lens board: bullseye set-builder (match-count rings, subset
  sectors, strength dots) with UpSet-style matrix fallback and
  next-keyword co-occurrence assist.
- Cluster-as-recipe manifests: intensional cluster definitions (query +
  pins + overrides with reasons) that re-run as the corpus grows and
  surface new candidates.
- Override-evidence loop: +/− inclusion overrides emitting Topics-edit
  scaffolds, human-seen signals, and negative evidence to the tag
  suggester and organizer queues.
- Cluster canvas: per-cluster workspace with member docs, evidence board,
  and possibles rail.
- Possible composer + option-set compare over the possibles register.
- Gap-prompt rendering (unclaimed docs, unsupported possibles) as
  actionable empty slots.
- Topic-chip faceting with co-occurrence counts and an unclustered shelf.
- Drag-to-cluster membership gesture scaffolding Topics: edits.
- AI possible-suggestion tray (bounded agent, cited passages, pending
  review).
- Provenance ribbons from possibles to source passages.
- Merge/split cluster proposals into the organizer queue.

## Exit

Feeds `ideation/staging/ideation-dashboard/` (the D11 working surface):
selected concepts land in the topic's `openspec/` drafts as renderer and
workbench deltas; the mockup grows a cluster-canvas sketch when the cut is
chosen.
