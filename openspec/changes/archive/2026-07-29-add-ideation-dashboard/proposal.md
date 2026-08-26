code_surface: openxFactory, codexFactory, xFactory
target_release: implemented
Status: ratified
Ratified: 2026-07-29 — record: the archive act, commit `366f04f` "Archive add-ideation-dashboard: capability promoted, evidence green", which applied this change's spec delta into `openspec/specs/doc-health/spec.md`, `openspec/specs/document-lifecycle/spec.md`, `openspec/specs/ideation-cross-reference/spec.md`, `openspec/specs/ideation-dashboard/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records the promotion in words: "openspec archive 2026-07-29: promotes the ideation-dashboard capability (15 requirements), creates ideation-cross-reference (2), and grows doc-health and document-lifecycle by one each". Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".

## Why

The family has a semantic surface over ideation content (the NotebookLM
projection) but no surface over its governance state: which topics exist at
which lifecycle stage, what each brainstorm could still become, which
possibles the organize gate picked, and where each pick went. That state is
scattered across doc headers, the staging INDEX, README lists, and OpenSpec
folders. Two structural gaps surfaced in the 2026-07-12 design session:
candidate feats a cluster could spawn but has not yet ("possibles")
evaporate into prose, and nothing lets a human assemble an arbitrary doc set
and point tools at it when they see a pattern the machine clustering
missed. All design questions are decided: D1–D17 locked (D7–D9 authoring
authority; D10 project grouping; D11 two-zone funnel with the cluster
column as the working surface; D12 cluster canvas; D13 keyword lens; D14
drill-down folders; D15 read-only Markdown viewer; D16 human gate console,
superseding the blanket gate prohibition for human actors; D17 next-step
kickoff — D10 onward added 2026-07-13 by Brett), R1–R14 confirmed
unchanged by Brett on 2026-07-12. History: first proposed and ratified 2026-07-12; demoted to
staging 2026-07-13 for continued design (drafts iterated in the topic's
`openspec/` workspace per the draft-proposal convention); re-proposed
2026-07-13 with the reworked feature set. **Re-ratified by Brett on
2026-07-14** (D1–D17); active until realization evidence lands per the
release-realization flow. v1 is explicitly web-based: a static repo-tracked web
GUI served per Option C alongside the Hermes-stack surfaces on the internal
xForge host.

## What Changes

- Add the `ideation-dashboard` capability: a schema-versioned generated
  snapshot (`kind: ideation-dashboard-snapshot`) over `ideation/` plus
  active and archived changes, rendered by a static repo-tracked GUI whose
  primary view is the six-column docs-first realization funnel (docs →
  clusters → possibles → staged picks → proposals → realized, many-to-many
  on the left hops, tallies counting links), with pipeline board, doc list,
  lineage, readiness heat, health overlay, and stats views from the same
  snapshot.
- Add the workbench: user-assembled temporary reference sets
  (cluster-seeded or ad-hoc) with scratch-notebook (`xf-wb-*`), on-demand
  readiness, scoped doc-health, and draft-organize-gate actions; gitignored
  `ideation-workbench` manifests under `ideation/workbench/`; committed
  manifests disallowed; scratch notebooks deleted with their manifest via a
  sync orphan sweep.
- Bind the interactivity boundary as normative requirements, split by
  actor: the dashboard's automated machinery is non-mutating over existing
  source documents and never executes a gate; humans create and edit
  corpus docs through the dashboard (header-compliant scaffolded creation,
  select-to-edit opening the human's editor) and operate lifecycle gates
  through the gate console (D16); agents may create new corpus docs but
  never modify, delete, or gate; deleting a doc/source in a corpus-bound
  notebook removes it from that set only.
- Add drill-down navigation, the viewer, and the gate console (D14–D17):
  pipeline/funnel tiles open their underlying folders (staged topic docs;
  a change's proposal/design/tasks/specs/supporting-docs); any doc opens
  in a read-only Markdown viewer served pass-through from the pinned
  checkout; on proposal artifacts a human runs reject-to-staging (the
  mechanized reverse transition per the draft-proposal convention),
  AI-assisted or manual edit (AI revisions land as redlines only a human
  applies), or approve/ratify (recorded); after ratification the console
  offers the change's outlined next step as a recorded dispatch under the
  workflow-gate contract (Speckit realization in codexFactory; domain
  workflows such as MedxFactory diagnosis elsewhere).
- MODIFIED `document-lifecycle`: brainstorm docs seed candidate feats in a
  `Possible feats:` section at capture; no historical fabrication — only
  the worked examples backfill as renderer fixtures.
- MODIFIED `ideation-cross-reference` (declared relative to the active
  ratified `add-ideation-cross-reference-readiness` change per the
  ordered-deltas rule): the cross-reference index consolidates the
  canonical possibles register (states `latent / picked / rejected /
  superseded`, reason + citation on rejected/superseded, pick edges citing
  staging IDs), and human-seen clusters from ad-hoc workbench sets enter
  the same recommendation queue under the full evidence contract.
- MODIFIED `doc-health`: a deterministic nightly snapshot-generation lane
  committing the snapshot beside the dated reports; no new check family —
  strict snapshot/manifest validation runs in the per-repo validator
  preflight.
- Add the cluster canvas working surface (D11/D12): each cluster opens a
  per-cluster workspace — member docs strictly from `Topics:`-derived
  edges (downstream artifacts in a lineage strip, never as members), an
  evidence board whose pins carry section-reference + passage-hash
  provenance, gap prompts rendered as actionable slots, and a possibles
  rail with option sets (choosing one marks siblings superseded with the
  required reason + citation) plus a composer that drafts
  possibles-register entries for human commit.
- Add the keyword lens set-builder (D13): the controlled keyword
  vocabulary with doc counts and co-occurrence hints; a match-count
  bullseye (rings by matched-keyword count, sectored by matched subset)
  with an always-present flat matrix view; check-to-stratify /
  pin-to-require gestures; declared vs inferred tag strengths rendered
  distinctly; manual include/exclude overrides that require a recorded
  reason and are captured as evidence; and cluster-as-recipe persistence —
  the workbench manifest stores the query (checked, pinned, overrides) so
  a cluster re-runs as the corpus grows, and "add as cluster" creates a
  workbench set plus a human-seen proposal under the evidence contract.
- Add the project grouping hierarchy (D10): a schema-versioned
  `project-register` (neutral schema; instance owned by the
  aggregation/workspace layer) maps repositories → projects (a project is
  a set of repos) → project groups; the generator resolves the mapping
  into `project`/`project_group` snapshot fields and renderers offer
  repo/project/group roll-ups. Descriptive navigation only — no lifecycle
  or authority semantics; unregistered repositories render ungrouped.
- Delivery per the confirmed rows: local generate-and-open command plus the
  nightly lane; v0 is the HTML funnel/board grown from the staged mockup
  skeleton; nightly + on-demand regeneration only.

## Capabilities

### New Capabilities

- `ideation-dashboard`: Defines the snapshot projection contract, the
  realization funnel model, the cluster canvas working surface, the
  keyword lens set-builder with cluster-as-recipe persistence, the project
  grouping hierarchy (repos → projects → project groups via the project
  register), the workbench reference-set contract and persistence rules,
  the permanent interactivity boundary, per-actor authoring authority
  (human create/edit, agent create-only, notebook set-removal semantics),
  and delivery/regeneration.

### Modified Capabilities

- `document-lifecycle`: Adds the `Possible feats:` declaration to the
  brainstorm format.
- `ideation-cross-reference`: Adds possibles-register consolidation and
  human-seen-cluster intake; sequenced with
  `add-ideation-cross-reference-readiness`.
- `doc-health`: Adds the deterministic nightly snapshot lane.

## Impact

- **openxFactory:** snapshot and workbench manifest schemas, the possibles
  register contract, a strict index/snapshot validator in the preflight,
  and ideation guidance updates.
- **codexFactory:** the deterministic generator, the static renderers grown
  from the mockup skeleton, workbench actions wired to `nlm`/doc-health/
  readiness, the sync orphan sweep, and tests.
- **xFactory aggregation:** the nightly snapshot lane beside the doc-health
  reports.
- **Compatibility:** v1 covers openxFactory only; the snapshot schema's
  `repository` field makes DomainxFactory instances and an aggregation
  roll-up additive later. Existing source documents are never modified by
  the capability's automated machinery or by any agent; humans edit through
  their own editor via select-to-edit, and all lifecycle gates remain
  human-operated.
