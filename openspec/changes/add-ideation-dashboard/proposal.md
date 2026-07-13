code_surface: openxFactory, codexFactory, xFactory
target_release: implemented

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
missed. All design questions are decided: D1–D10 locked (D7–D9, authoring
authority, added in a follow-on session; D10, the project grouping
hierarchy, added 2026-07-13 by Brett), R1–R14 confirmed unchanged by Brett
on 2026-07-12. **Ratified by Brett on 2026-07-12**; active until
realization evidence lands per the release-realization flow.

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
- Bind the permanent interactivity boundary as normative requirements,
  split by actor: the dashboard's automated machinery is non-mutating over
  existing source documents and never executes a gate; humans create and
  edit corpus docs through the dashboard (header-compliant scaffolded
  creation, select-to-edit opening the human's editor); agents may create
  new corpus docs but never modify or delete existing ones; deleting a
  doc/source in a corpus-bound notebook removes it from that set only.
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
  realization funnel model, the project grouping hierarchy
  (repos → projects → project groups via the project register), the
  workbench reference-set contract and persistence rules, the permanent
  interactivity boundary, per-actor authoring authority (human
  create/edit, agent create-only, notebook set-removal semantics), and
  delivery/regeneration.

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
