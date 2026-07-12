# ideation-dashboard Delta: Realization Funnel, Snapshot, Workbench

## ADDED Requirements

### Requirement: Snapshot projection contract
The ideation dashboard SHALL be a generated projection, never a source of
truth: a deterministic generator scans `ideation/` plus active and archived
OpenSpec changes and emits one schema-versioned snapshot
(`kind: ideation-dashboard-snapshot`, `schema_version`, and a `repository`
field), and renderers SHALL read only the snapshot. When the dashboard
disagrees with the repository, the dashboard is wrong and is regenerated.
v1 covers openxFactory only; the `repository` field keeps DomainxFactory
instances and an aggregation roll-up additive.

#### Scenario: The generator runs twice on the same tree
- **WHEN** the generator runs twice over an unchanged working tree
- **THEN** it MUST emit byte-identical snapshots

#### Scenario: A renderer needs data the snapshot lacks
- **WHEN** a view requires information not present in the snapshot
- **THEN** the snapshot schema is extended by delta and the generator populates it
- **AND** the renderer MUST NOT scan the repository directly

#### Scenario: The dashboard disagrees with the repository
- **WHEN** rendered state diverges from repo state
- **THEN** the resolution is regeneration — dashboard artifacts are never hand-edited

### Requirement: Realization funnel model
The dashboard's primary view SHALL be the six-column docs-first realization
funnel — source docs → topic clusters → possibles → staged picks →
proposals → realized — with explicit edges at every hop. Doc-to-cluster
edges derive from `Topics:` headers and cluster-to-possible edges from the
possibles register; both hops are many-to-many and per-cluster tallies
count links, not cards. A five-column collapsed-docs mode SHALL remain
available. Secondary views — pipeline board with possibles badges, doc
list, lineage, readiness heat, health overlay, and stats strip — render
from the same snapshot.

#### Scenario: One doc feeds several clusters
- **WHEN** a document's `Topics:` header names subjects belonging to different clusters
- **THEN** the funnel draws one edge per cluster and each cluster's tally counts the link

#### Scenario: One possible is claimed by several clusters
- **WHEN** more than one cluster claims the same possible
- **THEN** the possible appears once with an edge per claiming cluster

#### Scenario: Readiness scores exist for a cluster
- **WHEN** the cross-reference index carries tier scores or conflict flags for a topic
- **THEN** the readiness heat view MUST render them from the snapshot verbatim, without re-scoring

### Requirement: Workbench reference sets
The dashboard SHALL provide a workbench: user-assembled temporary reference
sets of documents, seeded from a cluster card or ad-hoc from the doc list,
with bounded actions — creating a scratch NotebookLM notebook
(`xf-wb-<name>`), on-demand readiness scoring, scoped doc-health, and a
draft-organize action that pre-fills a `staging/<topic>/` packet skeleton
for human review. Saved sets persist as gitignored schema-versioned
manifests (`kind: ideation-workbench`) under `ideation/workbench/`;
committed workbench manifests are disallowed. Scratch notebooks are derived
artifacts deleted with their manifest, and the notebook sync SHALL sweep
orphaned `xf-wb-*` notebooks. An ad-hoc set matching no machine cluster is
signal: it MAY be submitted to the cross-reference index as a human-seen
cluster under the full evidence contract.

#### Scenario: A workbench manifest is committed
- **WHEN** an `ideation-workbench` manifest appears in tracked repository content
- **THEN** validation MUST reject it — workbench sets must never become pseudo-staging

#### Scenario: A workbench manifest is deleted
- **WHEN** a saved set's manifest is removed
- **THEN** its bound `xf-wb-*` notebook is deleted by the orphan sweep rather than lingering

#### Scenario: The draft-organize action runs
- **WHEN** a user drafts an organize-gate packet from a reference set
- **THEN** the skeleton is written outside `ideation/staging/` for human review
- **AND** moving material into `ideation/staging/` remains a human gate action

### Requirement: Interactivity boundary
The dashboard and workbench SHALL be non-mutating over source documents and
SHALL never execute a lifecycle gate — permanently, not as a v1 limit. In
scope: assembling reference sets, launching analysis tools, and drafting
gate artifacts. Out of scope: editing, moving, promoting, or deleting
source documents, and executing any stage transition. Generator and
workbench actions MUST write only under their own declared output paths.

#### Scenario: A rendered card offers a stage transition
- **WHEN** any dashboard control would move a document between lifecycle stages
- **THEN** that control violates this capability — the strongest allowed concession is drafting the gate artifact for a human

#### Scenario: An action attempts a source write
- **WHEN** a generator or workbench action attempts to write outside its declared output paths
- **THEN** the write MUST be rejected and the attempt reported

### Requirement: Delivery and regeneration
The dashboard SHALL be delivered as a local generate-and-open command plus
a nightly lane that commits the snapshot beside the dated doc-health
reports, with the static renderer tracked in the repository and reading the
adjacent snapshot. Regeneration is nightly plus on-demand only — no
per-commit regeneration in v1. The v0 renderer is the HTML funnel/board
grown from the staged mockup skeleton; historical backfill is limited to
the worked-example fixtures.

#### Scenario: An operator wants the current picture
- **WHEN** the local command runs
- **THEN** it regenerates the snapshot from the working tree and opens the renderer against it

#### Scenario: Backfill scope is exceeded
- **WHEN** generation would fabricate register history for documents outside the worked-example fixtures
- **THEN** it MUST NOT — legacy docs without `Possible feats:` sections simply carry no possibles
