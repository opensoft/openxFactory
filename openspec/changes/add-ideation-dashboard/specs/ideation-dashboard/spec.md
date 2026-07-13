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

### Requirement: Project grouping hierarchy
The dashboard SHALL support a two-level grouping hierarchy over repositories — repositories belong to named projects (a project is a set of repositories) and projects belong to project groups — declared in one schema-versioned project register (`kind: project-register`, neutral schema, instance owned by the aggregation/workspace layer), resolved by the generator into `project` and `project_group` snapshot fields, and rendered as repo/project/group roll-ups on the funnel, pipeline, and stats views. Grouping is descriptive navigation only: it confers no lifecycle state or authority, and renderers read grouping from the snapshot, never from the register directly.

#### Scenario: A project spans several repositories
- **WHEN** the project register maps more than one repository to a project
- **THEN** the project roll-up MUST aggregate those repositories' snapshot entries under one project heading
- **AND** per-repository detail remains reachable beneath it

#### Scenario: Projects roll up into a project group
- **WHEN** the register assigns projects to a project group
- **THEN** the group view MUST aggregate its member projects' tallies from the snapshot

#### Scenario: A repository is absent from the register
- **WHEN** a snapshot's `repository` has no register entry
- **THEN** it MUST render ungrouped (its own implicit project) without failing the dashboard

#### Scenario: The register changes
- **WHEN** the project register is edited
- **THEN** grouping updates only through snapshot regeneration — rendered grouping is never hand-edited

### Requirement: Cluster canvas working surface
Each cluster SHALL open a canvas working surface rendered from the snapshot: a member pane listing exactly the cluster's `Topics:`-derived document edges (downstream artifacts — staged picks, proposals, realizations — render in a lineage strip, never as members), an evidence board whose pinned passages carry section reference and passage hash, gap prompts rendered as actionable slots (member documents unclaimed by any possible; possibles without document support), and a possibles rail with option-set grouping and a composer that drafts possibles-register entries for human commit; canvas machinery mutates no source document and AI-derived suggestions enter only as pending-review items.

#### Scenario: Member pane derivation
- **WHEN** a cluster canvas opens
- **THEN** its member pane MUST contain exactly the snapshot's Topics-derived document edges for that cluster
- **AND** downstream artifacts appear only in the lineage strip

#### Scenario: A member document supports no possible
- **WHEN** a member document is unclaimed by any possible
- **THEN** the canvas MUST render an actionable gap prompt for it

#### Scenario: An option set resolves
- **WHEN** a human chooses one option from an option set
- **THEN** the sibling possibles' superseded transitions MUST be drafted with the required reason and citation for human commit

#### Scenario: A possible is composed
- **WHEN** the composer produces a possible
- **THEN** a possibles-register entry draft is created and nothing enters the register without a human commit

### Requirement: Keyword lens set-builder
The dashboard SHALL provide a keyword lens over the controlled keyword vocabulary: per-keyword document counts with deterministic co-occurrence hints; a match-count bullseye whose rings index how many checked keywords a document matches (innermost = all), sectored by matched subset, paired with an always-present flat matrix view of the same membership; check-to-stratify and pin-to-require gestures; declared tags rendered distinctly from inferred tags; manual include/exclude overrides that REQUIRE a recorded reason and are captured as evidence; and cluster-as-recipe persistence — the workbench manifest stores the query (checked, pinned, overrides with reasons) so the set re-runs as the corpus grows, and cluster submission follows the human-seen evidence path.

#### Scenario: Intersection and union are both visible
- **WHEN** k keywords are checked
- **THEN** documents matching all k MUST render in the innermost zone and every partial match renders in the ring for its match count, sectored by which subset matched

#### Scenario: The matrix fallback exists
- **WHEN** the lens renders
- **THEN** a flat matrix or list view of the same membership MUST be available

#### Scenario: A manual override is recorded
- **WHEN** a document is manually included or excluded from the forming set
- **THEN** a reason MUST be recorded and the override captured as evidence (a scaffolded Topics: edit, a human-seen signal, or negative evidence) — never a silent set edit

#### Scenario: A recipe re-runs after corpus growth
- **WHEN** a saved recipe re-runs after new documents enter the corpus
- **THEN** newly matching documents MUST surface as new candidates without altering recorded overrides

#### Scenario: The forming set becomes a cluster
- **WHEN** the user adds the forming set as a cluster
- **THEN** a workbench reference set is created and a human-seen cluster proposal enters the cross-reference queue citing the recipe as rationale

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
The dashboard SHALL never execute a lifecycle gate — permanently, not as a
v1 limit — and its automated machinery (generator, renderers, workbench
actions) SHALL be non-mutating over existing source documents, writing only
under declared output paths. Document mutation authority is split by actor:
humans may create and edit corpus documents through the dashboard, agents
may only create (see the authoring requirements below). In scope for all
actors: assembling reference sets, launching analysis tools, and drafting
gate artifacts. Out of scope for all actors: executing any stage
transition, and moving or promoting source documents outside the
human-operated gates.

#### Scenario: A rendered card offers a stage transition
- **WHEN** any dashboard control would move a document between lifecycle stages
- **THEN** that control violates this capability — the strongest allowed concession is drafting the gate artifact for a human

#### Scenario: An automated action attempts a source write
- **WHEN** the generator, a renderer, or a workbench action attempts to write outside its declared output paths
- **THEN** the write MUST be rejected and the attempt reported

### Requirement: Human document authoring
The dashboard SHALL be the human's authoring cockpit over the ideation
corpus: a create action that scaffolds a new header-compliant document
(H1, `Status:`, `Kind:`, `Summary:`, `Topics:`, `Repository context:`,
`Captured:` pre-filled) into the chosen ideation area and opens it for
editing, and a select-to-edit action on any listed document that opens the
document in the human's editor. The dashboard launches the edit; it never
rewrites document content itself. Human edits remain subject to the
existing lifecycle discipline — editing a promoted document through the
dashboard grants no exemption from prose-delta rules or doc-health checks.

#### Scenario: A human creates a new corpus doc from the UI
- **WHEN** a human uses the create action
- **THEN** a header-compliant skeleton is written into the chosen ideation area and opened for editing
- **AND** the document appears in the next snapshot

#### Scenario: A human selects a doc to edit
- **WHEN** a human uses select-to-edit on a listed document
- **THEN** the document opens in the human's editor and the dashboard itself modifies nothing

#### Scenario: A human edits a promoted document
- **WHEN** the edited document carries a promoted lifecycle status
- **THEN** doc-health and prose-delta rules apply to the edit exactly as if it were made outside the dashboard

### Requirement: Agent create-only capture
Agents SHALL be able to add new documents to the ideation corpus but SHALL
never modify or delete an existing document — no Hermes tier and no Omni
worker holds edit or delete authority over corpus content. Agent-created
documents carry the required ideation headers and enter the corpus as
ordinary capture.

#### Scenario: An agent captures a new document
- **WHEN** an agent submits a new document to the corpus
- **THEN** it is added as a new file with the required headers and appears in the next snapshot

#### Scenario: An agent attempts to modify or delete an existing document
- **WHEN** any agent attempts an edit or deletion of an existing corpus document
- **THEN** the attempt MUST be rejected and reported

### Requirement: Notebook set-removal semantics
Deleting a doc/source in any corpus-bound NotebookLM surface SHALL only
remove it from that notebook's set — never delete the underlying corpus
document. Creating and editing notes in those surfaces (lifecycle
projections and `xf-wb-*` scratch notebooks) is allowed; new notes return
to the corpus only as new documents through the governed hybrid-import
path.

#### Scenario: A source is deleted from a workbench notebook
- **WHEN** a user removes a doc/source from an `xf-wb-*` notebook
- **THEN** the workbench manifest drops the reference and the corpus document is untouched

#### Scenario: A source is deleted from a lifecycle projection notebook
- **WHEN** a user removes a source from a lifecycle notebook
- **THEN** the corpus document is untouched and the next projection sync restores the set from lifecycle state — removing a source is not a lifecycle exit

### Requirement: Delivery and regeneration
The dashboard SHALL be delivered as a local generate-and-open command plus
a nightly lane that commits the snapshot beside the dated doc-health
reports, with the static renderer tracked in the repository and reading the
adjacent snapshot. The committed renderer and snapshot SHALL additionally
be served from an access-controlled internal host that reads the committed
snapshot read-only; the serving host is provided by the runtime install
layer, and the dashboard MUST NOT be served from a public endpoint because
the snapshot projects internal governance state. Regeneration is nightly
plus on-demand only — no per-commit regeneration in v1. The v0 renderer is
the HTML funnel/board grown from the staged mockup skeleton; historical
backfill is limited to the worked-example fixtures.

#### Scenario: An operator wants the current picture
- **WHEN** the local command runs
- **THEN** it regenerates the snapshot from the working tree and opens the renderer against it

#### Scenario: A team viewer opens the hosted dashboard
- **WHEN** a viewer opens the dashboard on the internal host
- **THEN** the host serves the committed renderer against the nightly-committed snapshot behind the existing access control, modifying neither

#### Scenario: A public endpoint is proposed
- **WHEN** any delivery path would serve the dashboard from a public, unauthenticated endpoint
- **THEN** it MUST be rejected — the snapshot projects internal governance state and is served only from an access-controlled internal host

#### Scenario: Backfill scope is exceeded
- **WHEN** generation would fabricate register history for documents outside the worked-example fixtures
- **THEN** it MUST NOT — legacy docs without `Possible feats:` sections simply carry no possibles
