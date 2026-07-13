# Cluster Combining GUI — Brainstorm

Status: brainstorm
Kind: architecture
Summary: GUI concepts that make the funnel's generative zone (docs → clusters → possibles) an active working surface instead of a rendering — a cluster canvas with an evidence board and gap prompts, a possible composer with option-set comparison, drag/lasso combining gestures, topic-chip faceting, and pending-review AI suggestion trays — all inside the dashboard's non-mutating / human-edit / agent-create-only boundary.
Topics: ideation-dashboard, workbench, possibles-register, gui-design, ideation-tooling, doc-management, doc-workflow
Repository context: openxFactory (feeds the ideation-dashboard staged topic)
Captured: 2026-07-13
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
