# ideation-dashboard Specification

## Purpose
TBD - created by archiving change add-ideation-dashboard. Update Purpose after archive.
## Requirements
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
The dashboard's automated machinery (generator, renderers, workbench actions) SHALL never execute a lifecycle gate and SHALL be non-mutating over existing source documents, writing only under declared output paths. Document mutation authority is split by actor: humans may create and edit corpus documents through the dashboard and may operate lifecycle gates through the gate console (see the gate-console requirement — D16, superseding the earlier blanket prohibition for human actors); agents may only create, never edit, delete, or gate. In scope for all actors: assembling reference sets, launching analysis tools, and drafting gate artifacts. Out of scope permanently: any gate executed by machinery or agents, and any stage transition that does not produce the governed transition artifacts and a recorded human action.

#### Scenario: Automated machinery attempts a stage transition
- **WHEN** the generator, a renderer, a scheduled lane, or any agent path would move a document or change between lifecycle stages
- **THEN** the attempt MUST be rejected and reported — gates are human console actions only

#### Scenario: An automated action attempts a source write
- **WHEN** the generator, a renderer, or a workbench action attempts to write outside its declared output paths
- **THEN** the write MUST be rejected and the attempt reported

### Requirement: Pipeline drill-down and document explorer
Pipeline-board and funnel tiles SHALL be openable as their underlying artifact folders: a staged-topic tile opens the topic folder listing its documents (including any `openspec/` draft workspace); a proposal tile opens the change folder listing proposal, design, tasks, spec deltas, and supporting documents; realized tiles open the archived change or promoted spec. From the explorer the user picks any document to open in the viewer.

#### Scenario: A staged tile is opened
- **WHEN** the user opens a staged-topic tile
- **THEN** the explorer lists the topic folder's documents with their headers (status, kind, summary)

#### Scenario: A proposal tile is opened
- **WHEN** the user opens a proposal tile
- **THEN** the explorer lists the change's proposal, design, tasks, spec deltas, and supporting documents, each openable in the viewer

### Requirement: Read-only document viewer
The dashboard SHALL render any explorer-selected document as read-only rendered Markdown via source pass-through: content is served read-only from the same pinned checkout the snapshot was generated from, so dashboard state stays snapshot-only while document content is always the source file; the viewer offers the select-to-edit escape hatch and, on gate-bearing artifacts, the gate console actions.

#### Scenario: A document is viewed
- **WHEN** the user opens a document from the explorer
- **THEN** it renders as read-only Markdown from the pinned checkout and the dashboard modifies nothing

#### Scenario: Snapshot and content disagree
- **WHEN** the pinned checkout has moved past the snapshot's revision
- **THEN** the viewer MUST surface the divergence and the resolution is snapshot regeneration

### Requirement: Human gate console
The dashboard SHALL offer gate actions on an opened proposal artifact, executable by a human only, each producing the same governed artifacts as the manual path plus a recorded action: (1) reject / move back to staging — the reverse transition returns the change's artifacts to the staging topic with the proposal documents continuing as draft ideas in the topic's `openspec/` workspace per the draft-proposal convention, registers and READMEs updated; (2) edit — the console lists the artifact's main concepts (requirements, decisions) and the human either picks one for an AI-drafted revision, delivered as a proposed redline that only a human may apply and commit, or opens the document in their own editor; (3) approve / ratify — the ratification is recorded on the proposal with the ratifier and date, and registers update. Agents SHALL be unable to invoke any gate action.

#### Scenario: A proposal is rejected back to staging
- **WHEN** a human runs the reject action on a proposal
- **THEN** the reverse transition executes via the governed tooling — artifacts return to the staging topic (drafts into its `openspec/` workspace), the staging INDEX and README records update, and a demotion record is written

#### Scenario: A concept is edited with AI assistance
- **WHEN** a human picks a listed concept for AI revision
- **THEN** the AI produces a proposed redline as a new review artifact and the source document changes only when a human applies and commits it

#### Scenario: A proposal is ratified from the console
- **WHEN** a human runs the approve action
- **THEN** the ratification record (ratifier, date) is written to the proposal and the registers update — identical artifacts to a manual ratification

#### Scenario: An agent invokes a gate action
- **WHEN** any agent or automated path calls a gate-console action
- **THEN** the call MUST be rejected and reported

### Requirement: Next-step kickoff
After ratification the console SHALL offer the change's outlined next step as a human-initiated, recorded dispatch under the promoted workflow-gate contract — commonly a Speckit realization workflow in the engineering factory, or a domain workflow in a DomainxFactory (for example a diagnosis workflow in MedxFactory); the dashboard dispatches and renders status, it never executes the workflow itself.

#### Scenario: A ratified change offers its next step
- **WHEN** a change is ratified and declares a realization outline
- **THEN** the console offers the outlined next step and a human-initiated dispatch creates a recorded, gated workflow job

#### Scenario: A non-ratified change is asked for kickoff
- **WHEN** kickoff is attempted on a change without a recorded ratification
- **THEN** the console MUST refuse — kickoff is downstream of the ratify gate

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

### Requirement: Staged-topic proposal commissioning
The gate console SHALL offer a human-only `propose` action on a staging topic that commissions proposal authoring as a recorded dispatch — a `workflow-job` descriptor naming the proposal-authoring workflow and targeting the topic's staging id, plus a gate-action record — without authoring anything itself; the commissioned authoring runs externally and lands as an ordinary OpenSpec change subject to the existing review and ratify gates. The console SHALL refuse a topic absent from the pinned checkout's staging area and SHALL refuse a duplicate commission while a dispatched `propose` job for the same topic remains undelivered.

#### Scenario: A staged tile is taken toward proposal
- **WHEN** a human runs the propose action on a staging topic
- **THEN** a `workflow-job` descriptor (workflow `proposal-authoring`, target `topic_id`) and a `propose` gate-action record are written through the human gate
- **AND** no proposal artifact is authored by the console itself

#### Scenario: A missing topic is refused
- **WHEN** propose is invoked for a topic id with no directory under the checkout's `ideation/staging/`
- **THEN** the console MUST refuse with the reason and persist nothing

#### Scenario: A duplicate commission is refused
- **WHEN** propose is invoked for a topic that already carries a dispatched, undelivered `propose` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch

#### Scenario: An agent invokes propose
- **WHEN** any agent or automated path calls the propose action
- **THEN** the call MUST be rejected and reported, like every gate action

### Requirement: Deterministic per-document completeness signal
The snapshot generator SHALL compute a per-document completeness signal at generation time and emit it as an additive `completeness` object on each `documents[]` entry — a `score` plus five named signals: `structure` (the fraction of the document's expected structural elements present, the expected set fixed per `Kind:` with a common fallback — H1 title, the governance header block, at least one section), `length` (body size normalized against a fixed saturation threshold, so padding past the threshold cannot outscore substance), `open_markers` (an INVERSE signal over open-question / TODO / TBD markers normalized against a fixed saturation count), `keyword_coverage` (the fraction of the document's declared `Topics:` subjects that resolve to the snapshot's keyword vocabulary), and `link_degree` (the document's snapshot edge degree — cluster document edges plus `destinations` staged topics, changes, and capabilities — normalized against a fixed saturation degree). Every signal SHALL be reported as a named normalized value beside the raw count that produced it, so a rendered bar is explainable. The computation MUST be deterministic and reproducible from the pinned tree alone: no model call, no wall clock, no network, no judgment input of any kind, with the `score` a fixed-weight combination of the normalized signals at a fixed decimal precision — the weights are contract constants in v1 (a tunable configuration would be a successor change, never a per-run input). The per-document signal SHALL stay out of judgment surfaces: it MUST NOT be an input to the readiness recommendation gate and MUST NOT produce a doc-health finding; its ONE sanctioned gate consumer is the staged-to-proposal readiness gate defined in this change, which consumes document scores only through the staged-topic health aggregate — no other gate verb, console guard, or lifecycle transition may consult it or refuse on it (Brett's 2026-07-25 ruling supersedes this change's earlier informational-only bound). Growth is additive — the field is optional, no existing snapshot is invalidated, and a renderer reading a pre-growth snapshot MUST degrade to showing no completeness rather than failing.

#### Scenario: The generator runs twice on the same tree
- **WHEN** the generator runs twice over an unchanged working tree
- **THEN** every document's `completeness` score and signals MUST be identical and the snapshot MUST stay byte-identical

#### Scenario: A document grows sections and links
- **WHEN** a document gains expected sections and gains edges (a new declared topic matching a cluster, or a new downstream destination) between two generations
- **THEN** its `structure` and `link_degree` signals MUST rise and its `score` MUST be strictly higher than the earlier generation's

#### Scenario: A stub scores low without becoming a defect
- **WHEN** a document carries only its headers, a short body, and standing TODO markers
- **THEN** it MUST score low on `structure`, `length`, and `open_markers`
- **AND** no doc-health finding, refusal, or lifecycle consequence MUST follow from the score

#### Scenario: A score is asked to gate an action
- **WHEN** any surface OTHER than the staged-to-proposal readiness gate — the readiness recommendation gate, another console verb's guard, or a lifecycle transition — would consult a completeness score to allow or refuse
- **THEN** it MUST NOT — the readiness gate consumes document scores only through the staged-topic health aggregate, and every other consumer treats completeness as information

#### Scenario: A signal would require judgment
- **WHEN** a proposed completeness signal cannot be computed from the pinned tree without model judgment
- **THEN** it MUST NOT enter v1 scoring — the signal set stays the five deterministic signals, and semantic assessment remains the agentic sweep's and the readiness panel's own capabilities

#### Scenario: A snapshot predates the field
- **WHEN** a renderer reads a snapshot generated before this growth landed
- **THEN** it MUST render the document list with no completeness bars and MUST NOT compute the signal itself

### Requirement: Staged-topic health signal
The snapshot generator SHALL compute a per-staged-topic health aggregate at generation time and emit it as an additive `health` object on each `staged_topics[]` entry, derived exclusively from the topic FOLDER's own corpus documents — documents that merely declare the topic as a destination are context, never health inputs. The object SHALL carry `standing_open_items` (the sum of the member documents' `open_markers` raw counts), `doc_score_min` and `doc_score_mean` (over the member documents' completeness scores, at the same fixed decimal precision), a `blockers` array of typed, explainable reasons (each standing-open-items document with its count; each document whose score falls below the ready threshold, with the score and the constant), and a derived `status`: `ready` when the blockers array is empty, `stub` when the folder carries no corpus documents, `developing` otherwise. The ready threshold is a contract constant in v1 (`READY_MIN_SCORE`, initial value 0.60 by Brett's 2026-07-25 ruling, calibrated at realization), pinned beside the completeness weights — never a per-run input. The computation MUST be deterministic and reproducible from the pinned tree alone, exactly as the per-document signal is. The aggregate SHALL NOT be a readiness judgment: it MUST NOT feed the readiness recommendation gate or re-score any readiness tier, and no cluster or possible gains any aggregate. Growth is additive — the field is optional and a pre-growth snapshot stays valid.

#### Scenario: A topic carries standing open questions
- **WHEN** any of the topic folder's corpus documents carries standing open-question / TODO markers
- **THEN** the topic's `status` MUST NOT be `ready`
- **AND** `blockers` MUST name each such document with its standing count

#### Scenario: A topic is worked to done
- **WHEN** every member document's standing open markers reach zero and every member document's score is at or above the ready threshold
- **THEN** the topic's `blockers` MUST be empty and its `status` MUST be `ready`

#### Scenario: A topic folder is a stub
- **WHEN** a staged topic's folder carries no corpus documents
- **THEN** its `status` MUST be `stub`

#### Scenario: Health is deterministic
- **WHEN** the generator runs twice over an unchanged working tree
- **THEN** every staged topic's `health` object MUST be identical and the snapshot MUST stay byte-identical

#### Scenario: Health is mistaken for readiness
- **WHEN** the readiness recommendation gate, a readiness tier, or any cluster/possible surface would consume the health aggregate
- **THEN** it MUST NOT — health is a structural doneness signal for staged topics, and the governed readiness judgment keeps its own authorities

### Requirement: Staging workbench scoped view
The dashboard SHALL provide a staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — presenting three tabbed panels over that one scope. The `docs` panel SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them. The `lens` panel SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `outline` panel SHALL render the topic's outline when one exists — for a staged topic, the fragment's outline material — read through the same read-only `/source` pass-through the document viewer uses, and MUST show an explicit empty state when the scope carries no outline. The workbench's ONLY write authority SHALL be the human-only `create-document` gate verb: it MUST write no register entry, no workbench manifest, and no gate artifact beyond that verb's own gate-action record; it MUST NOT modify or delete any existing document, in any panel, by any path; and outline EDITING remains out of scope. With the gate capability absent the workbench SHALL be read-only in every panel, as it is on the served static image.

#### Scenario: The workbench opens on a cluster
- **WHEN** a human opens the workbench from a cluster tile
- **THEN** the view scopes to that cluster: the `docs` panel lists exactly that cluster's snapshot document edges and the `lens` panel is scoped to that cluster's declared topics

#### Scenario: The workbench opens on a possible
- **WHEN** a human opens the workbench from a possible tile
- **THEN** the `docs` panel lists the documents its recorded supporting evidence cites
- **AND** any documents inherited from its claiming clusters appear in a separately labelled section, distinct from cited evidence

#### Scenario: The workbench opens on a staged topic
- **WHEN** a human opens the workbench from a staged-topic tile
- **THEN** the `docs` panel lists the topic folder's corpus documents together with every document whose declared destination names that staging topic
- **AND** the member documents of the topic's linked clusters appear in a separately labelled cluster-neighbourhood section, never conflated with the topic's own material
- **AND** the `outline` panel renders that fragment's outline material read-only

#### Scenario: Cluster-neighbourhood documents stay out of health
- **WHEN** a staged topic's health or its readiness gate is computed
- **THEN** cluster-neighbourhood documents contribute nothing — health and the gate stay derived from the topic FOLDER's own corpus documents only

#### Scenario: A docs row shows how far a document has come
- **WHEN** the `docs` panel renders a document the snapshot scores
- **THEN** its bar and named signals MUST come from the snapshot's `completeness` object verbatim
- **AND** the workbench MUST NOT compute, adjust, or re-weight any signal

#### Scenario: The source pass-through is absent
- **WHEN** the workbench runs against a served static image with no `/source` route
- **THEN** the `docs` and `lens` panels MUST still render from the snapshot
- **AND** the `outline` panel MUST report the missing pass-through inline and degrade, exactly as the document viewer does

#### Scenario: A scope carries no outline
- **WHEN** the opened tile has no outline material
- **THEN** the `outline` panel MUST render an explicit empty state rather than fabricating or drafting one

#### Scenario: The workbench is asked to modify an existing document
- **WHEN** any workbench panel would edit or delete an existing corpus document, or write a register entry, a workbench manifest, or any gate artifact other than the `create-document` verb's own gate-action record
- **THEN** the write MUST be rejected and reported — the workbench's only write is the create-only gated document creation, and every other write path arrives in a later change

#### Scenario: The workbench renders without the gate capability
- **WHEN** the workbench runs on a surface where the gate capability is absent
- **THEN** every panel MUST be read-only and no write MUST be reachable from the page

### Requirement: Workbench tile action
The wheel's expanded tile SHALL offer an `open workbench` action on the clusters, possibles, and staged wheels, mounted through the wheel's established per-wheel action-row extension point (one row in the pure action table plus one mounter entry, as `add-wheel-action-verbs` describes — not re-specified here), and the action SHALL carry NO gate capability requirement because it writes nothing: it is a read-only navigation verb like the existing read, lens, canvas, and landed verbs, offered whether or not the gate capability is live and therefore present on the deployed static image, where content-dependent panels degrade inline. The action SHALL open the workbench scoped to the tile it was activated from, and the wheels whose tiles are not topic-bearing SHALL NOT offer it.

#### Scenario: A topic-bearing tile offers the workbench
- **WHEN** a human expands a cluster, possible, or staged tile
- **THEN** the action row MUST include the workbench action
- **AND** activating it opens the workbench scoped to that tile

#### Scenario: The gate capability is off
- **WHEN** the loopback gate capability is unavailable
- **THEN** the workbench action MUST still be offered — it writes nothing and needs no gate

#### Scenario: A non-topic-bearing tile is expanded
- **WHEN** a human expands a document, active-change, or archived-change tile
- **THEN** the workbench action MUST NOT appear on that row

### Requirement: Staged-to-proposal readiness gate
The gate console's `propose` action SHALL refuse to commission proposal authoring for a staging topic whose health status is not `ready`, so a topic cannot move from staging toward proposal while open questions stand or its documents fall short of the ready threshold. The guard SHALL be enforced at the propose route itself, so every surface that reaches it — the staged tile's action, the CLI, a direct request — is gated identically, and it adds to (never replaces) the existing refusals for a missing topic and a duplicate commission. The check MUST be evaluated live against the pinned checkout at request time using the same deterministic scoring the generator uses — never against the served snapshot, which may be stale. A refusal SHALL cite the topic's blockers concretely (each document with standing open items and its count; each document below the threshold with its score and the constant) and SHALL persist nothing, exactly like the existing propose refusals. The gate consumes per-document completeness ONLY through the staged-topic health aggregate, and the action remains human-only as the commissioning requirement prescribes. The gate SHALL offer NO override in v1 (Brett's 2026-07-25 ruling): a blocker is cleared by closing it, and any future override would be a recorded gate action defined by a successor change, never a silent bypass.

#### Scenario: An override is attempted
- **WHEN** any parameter, header, or console affordance would bypass the readiness gate for a topic that is not `ready`
- **THEN** the console MUST refuse — v1 carries no override path, recorded or otherwise

#### Scenario: A topic with standing open questions is proposed
- **WHEN** a human runs propose on a staging topic whose folder documents carry standing open-question markers
- **THEN** the console MUST refuse, naming each document and its standing count, and persist nothing

#### Scenario: A topic with an underdone document is proposed
- **WHEN** a human runs propose on a topic whose every open question is closed but a member document's completeness score is below the ready threshold
- **THEN** the console MUST refuse, citing that document's score against the contract constant, and persist nothing

#### Scenario: A ready topic is proposed
- **WHEN** a human runs propose on a topic whose live-computed health is `ready`
- **THEN** the commission proceeds exactly as the staged-topic proposal commissioning requirement prescribes — descriptor plus gate-action record

#### Scenario: The snapshot and the checkout disagree
- **WHEN** the served snapshot shows a topic `ready` but the pinned checkout has since gained a standing open marker in that topic's folder
- **THEN** the live evaluation governs and the console MUST refuse, citing the marker the snapshot has not yet seen

### Requirement: Staged tile health display
The wheel's staged tiles SHALL surface the topic's health at two levels matching the tile interaction model: the FOCUSED (centred, first-click) tile face SHALL carry a compact health indicator showing the tri-state status, and the EXPANDED (second-click) tile SHALL render the full health block — status, standing open items with each document's count, the doc score minimum and mean, and the blockers list — VERBATIM from the snapshot's `health` object, never recomputing any value client-side. Resting drum faces SHALL stay unadorned. A renderer reading a pre-growth snapshot MUST show no indicator and no health block rather than computing the signal itself. The display never gates: allowing or refusing stays with the server-side readiness gate, whose refusal message is the authoritative account when the snapshot has drifted from the checkout.

#### Scenario: A staged tile is focused
- **WHEN** a human clicks a staged tile to centre it
- **THEN** the focused tile face MUST show the compact health indicator reflecting the snapshot's `status`

#### Scenario: A focused staged tile is expanded
- **WHEN** the human clicks the centred staged tile again
- **THEN** the expanded tile MUST render the full health block, including every blocker, verbatim from the snapshot

#### Scenario: The snapshot predates the health field
- **WHEN** the renderer reads a snapshot with no `health` object on a staged topic
- **THEN** the tile MUST render with no indicator and no health block, and MUST NOT compute health itself

#### Scenario: The display disagrees with the gate
- **WHEN** a tile shows `ready` from a stale snapshot but the live gate refuses the propose
- **THEN** the refusal's cited blockers are the authoritative account and the display MUST NOT suppress or restate the refusal

### Requirement: Workbench lens bullseye at tile scope
The staging workbench's `lens` panel SHALL render the match-count bullseye — the same rings-by-match-count, sectored-by-matched-subset, dotted geometry the keyword lens renders (rings index how many checked keywords a document matches, innermost = all) — at TILE SCOPE, above the always-present flat matrix, from the SAME scoped keyword-lens derivation the panel already performs. The bullseye MUST introduce no new analysis, no new score, and no new snapshot field: it renders the geometry the scoped derivation already returns, and each rail row's declared count stays the snapshot's corpus-wide number verbatim, labelled as such. The flat matrix SHALL remain always present and MUST NOT become a toggle-only alternate. There SHALL be exactly ONE bullseye renderer serving both the keyword-lens view and the workbench panel, so the two surfaces cannot drift. The human's checked-keyword selection SHALL persist across tab switches within one workbench session, and SHALL reset to the scope's seed when a different scope is opened or the workbench is closed.

#### Scenario: The workbench lens panel renders the bullseye
- **WHEN** a human opens the workbench's `lens` tab on any topic-bearing tile
- **THEN** the match-count bullseye MUST render at that tile's scope, above the flat matrix
- **AND** the flat matrix MUST still render, as the always-available view of the same membership

#### Scenario: The scoped bullseye introduces no new number
- **WHEN** the workbench bullseye renders
- **THEN** its rings, sectors, and dots MUST come from the existing scoped keyword-lens derivation
- **AND** no new snapshot field, score, or recount of the keyword vocabulary is introduced

#### Scenario: A checked selection survives a tab switch
- **WHEN** a human checks keywords in the workbench `lens` tab, visits `docs` or `outline`, and returns to `lens`
- **THEN** the checked selection MUST be exactly the one they left

#### Scenario: A new scope reseeds the selection
- **WHEN** the workbench is closed, or opened on a different tile
- **THEN** the checked selection MUST reset to that scope's seed keywords rather than carrying the previous scope's keywords forward

### Requirement: Gated document creation verb
The gate console SHALL offer a human-only `create-document` verb that brings a NEW ideation document into existence through the EXISTING tested authoring engine, enforced at the route so the workbench affordance, the CLI parity subcommand, and a direct request are gated identically. The verb SHALL accept an area, title, summary, topics, and optional repository context, kind, status, possible-feat seeds, and source citation, defaulting the repository context from the served snapshot's repository, and SHALL write the document through the authoring scaffold with its controlled header block (`Status`, `Kind`, `Summary`, `Topics`, `Repository context`, `Captured`) in the declared order. A created document's `Status:` SHALL default to `brainstorm` in EVERY area — the verb MUST NOT derive a lifecycle status from the area it writes into, because a document's tie to a staging packet is carried by its PLACEMENT inside that packet's folder and not by its status header, and a just-captured thought is `brainstorm` wherever it sits. A human-supplied status MUST be accepted only from the create-legal set (`brainstorm`, `staged`, `draft`), so no document can be born already approved. The write MUST be create-only: an EXISTING target refuses as a source-edit refusal and is never overwritten, and this verb grants NO edit or delete authority over any existing document. Every successful create SHALL persist a gate-action record naming the created document's repository-relative path in its target and referencing the created document as a `document`-kind artifact. The verb MUST be loopback-only and MUST fail closed on an unresolved actor, and any agent or automated invocation MUST be rejected and reported, like every gate action. The verb SHALL make no engine change beyond the status and source passthrough the header block requires: the header contract, the filename normalization, and every refusal are the authoring engine's, surfaced verbatim at the route.

#### Scenario: A human creates a document through the gate
- **WHEN** a human invokes `create-document` with an area, title, summary, and topics
- **THEN** a header-compliant document is written into that area with the controlled header block in the declared order
- **AND** a gate-action record is persisted naming the created document's repository-relative path and referencing it as a `document`-kind artifact

#### Scenario: A create into a staging topic folder
- **WHEN** a human creates a document with the area set to a staging topic folder and supplies no status
- **THEN** the document MUST be written with `Status: brainstorm`, exactly as a create into the brainstorm area is
- **AND** its membership of that staging packet MUST come from its placement in the topic folder, which is what the folder-scoped health and readiness derivations already read

#### Scenario: A create asks to be born approved
- **WHEN** a create supplies a status outside the create-legal set — `ratified`, `standard`, or any other promoted stage
- **THEN** the call MUST refuse and persist nothing

#### Scenario: The target already exists
- **WHEN** the verb targets a path that already holds a document
- **THEN** the call MUST refuse as a source-edit refusal, persist nothing, and leave the existing document byte-identical

#### Scenario: An agent invokes the verb
- **WHEN** any agent or automated path calls `create-document`
- **THEN** the call MUST be rejected and reported — document creation by an agent remains the separate agent-capture surface with its own header enforcement

#### Scenario: The gate capability is unavailable
- **WHEN** the verb is reached on a non-loopback bind, or with no resolved human actor
- **THEN** the route MUST refuse and persist nothing

#### Scenario: The CLI reaches the same law
- **WHEN** the parity subcommand invokes the verb
- **THEN** it MUST be gated identically to the browser affordance, drive the same engine, and produce the same gate-action record

### Requirement: Workbench creation affordances and seeding
The staging workbench SHALL offer the `create-document` verb from each of its three tabs, seeded from the material that tab is showing, and the seeded values SHALL remain editable before the create fires. On the `docs` tab the affordance SHALL be a button on the pane's actions row, seeding topics from the tile's keywords, repository context from the snapshot's repository, the area from the scope (a staged scope's own staging topic folder; the brainstorm area for a cluster or possible scope), and a source citation naming the workbench scope by kind and id. On the `lens` tab the affordance SHALL be a button on the forming-set pane AND an activation of ANY region of the bullseye — its matches-ALL centre zone or any ring SECTOR — all opening the SAME dialog with the same seeding rule and a source citation naming the recipe (the checked and pinned keywords) at the snapshot's source revision, so the membership that motivated the document re-derives from the record. The topics seed SHALL be the activated region's own matched keyword combination: the LIVE checked keyword set for the forming-set button and the centre zone, and that sector's matched SUBSET of the checked set for a ring sector — the bullseye is already sectored by which checked keywords a document matched, so a sector names a combination the human can act on without re-deriving it. Every activatable region MUST be keyboard-reachable and focusable on the same terms as the centre zone, and MUST NOT be the only path to the dialog. The bullseye renderer serving the keyword-lens view SHALL receive no activation handler, and with no handler supplied every region MUST be inert and the rendered output MUST be identical to the unactivatable bullseye. On the `outline` tab the affordance SHALL be offered for staged scopes ONLY, as a new fragment in that topic with the area set to the staging topic folder, and MUST be hidden for cluster and possible scopes, which have no topic folder to write into. When the gate capability is absent the affordances SHALL render as COPYABLE CLI DESCRIPTORS carrying the seeded values and MUST NOT render as live buttons, and no write MUST be reachable from the page. On a successful create the workbench SHALL open the created document in the read-only viewer. The workbench's posture indicator SHALL state `read-only` when the gate capability is off and the gate-bearing posture when the capabilities grant gate, and MUST NOT claim a posture the surface does not have.

#### Scenario: Creating from the docs tab
- **WHEN** a human uses the create affordance on the workbench `docs` tab
- **THEN** the dialog opens seeded with the tile's keywords as topics, the snapshot's repository as repository context, the scope-derived area, and a source citation naming the scope's kind and id
- **AND** every seeded value is editable before the create fires

#### Scenario: Creating from the centre ring
- **WHEN** a human clicks the bullseye's matches-ALL centre ring, or the forming-set pane's create button
- **THEN** the SAME create dialog opens, seeded with the LIVE checked keyword set as topics
- **AND** the source citation names the checked and pinned keywords at the snapshot's source revision

#### Scenario: Creating from a ring sector
- **WHEN** a human activates a ring SECTOR of the workbench bullseye, by click or by keyboard
- **THEN** the SAME create dialog opens, seeded with exactly that sector's matched keyword combination as topics — the subset of the checked set the sector represents, not the whole checked set
- **AND** every sector MUST be focusable and keyboard-activatable, on the same terms as the centre zone

#### Scenario: The bullseye outside the workbench stays inert
- **WHEN** the bullseye renders on the keyword-lens view, which supplies no activation handler
- **THEN** no region MUST be activatable or focusable, and the rendered output MUST be identical to the bullseye rendered before any create affordance existed

#### Scenario: The outline affordance is scope-bound
- **WHEN** the workbench `outline` tab renders for a cluster or a possible
- **THEN** the create affordance MUST be hidden — there is no staging topic folder to write a fragment into
- **AND** for a staged scope it MUST be offered, writing into that topic's folder

#### Scenario: The gate capability is off
- **WHEN** the workbench renders on a surface without the gate capability
- **THEN** every create affordance MUST render as a copyable CLI descriptor carrying the seeded values
- **AND** no live create button and no write path MUST be reachable from the page

#### Scenario: A create succeeds
- **WHEN** a create lands through the gate
- **THEN** the workbench MUST open the created document in the read-only viewer

#### Scenario: The posture indicator is honest
- **WHEN** the workbench renders with the gate capability granted
- **THEN** its posture indicator MUST state the gate-bearing posture rather than `read-only`
- **AND** with the gate capability absent it MUST state `read-only`

