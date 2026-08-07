# ideation-dashboard Specification

## Purpose
TBD - created by archiving change add-ideation-dashboard. Update Purpose after archive.
## Requirements
### Requirement: Snapshot projection contract
The ideation dashboard SHALL be a generated projection, never a source of truth: a deterministic generator scans `ideation/` plus active and archived OpenSpec changes for ONE repository at ONE ref and emits one schema-versioned snapshot (`kind: ideation-dashboard-snapshot`, `schema_version`, and a `repository` field), and renderers SHALL read only snapshots, addressed by the (repository, ref) pair through the snapshot registry. When the dashboard disagrees with the repository, the dashboard is wrong and is regenerated. The generator SHALL be runnable for every registered repository, and the `repository` field plus the snapshot index are what make per-repository instances and an aggregate roll-up composable — no repository is privileged, and the earlier openxFactory-only scope is superseded.

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

#### Scenario: The generator runs for a second repository
- **WHEN** the generator is run against another registered repository
- **THEN** it MUST emit that repository's own snapshot under its own (repository, ref) address, with no change to any other repository's snapshot

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
The dashboard SHALL support a two-level grouping hierarchy over repositories — repositories belong to named projects (a project is a set of repositories) and projects belong to project groups — declared in one schema-versioned project register (`kind: project-register`, neutral schema, instance owned by the aggregation/workspace layer), resolved by the generator into `project` and `project_group` snapshot fields, and surfaced through the project-first header (the project dropdown and the repository filter) — the former header-level roll-up strip is retired (Brett's 2026-08-06 ruling), with the pure grouping model remaining available to any view wanting a roll-up. Repository membership SHALL be multi-parent: a repository MAY live in any number of projects (a project is a named view over repositories, not an owner), the snapshot's singular `project` field SHALL carry the PRIMARY project (the first project in register order declaring the repository, so grouped roll-ups render each repository under exactly one heading), and the snapshot SHALL additionally carry the full membership as an additive `projects` list whose first element is that primary. A project SHALL belong to at most one project group. Grouping is descriptive navigation only: it confers no lifecycle state or authority, and renderers read grouping from the snapshot, never from the register directly.

#### Scenario: A project spans several repositories
- **WHEN** the project register maps more than one repository to a project
- **THEN** the project roll-up MUST aggregate those repositories' snapshot entries under one project heading
- **AND** per-repository detail remains reachable beneath it

#### Scenario: A repository lives in several projects
- **WHEN** the register declares one repository under more than one project
- **THEN** the register is valid, the repository's snapshot carries the first-declaring project as `project` and every declaring project in `projects`
- **AND** project-scoped selection offers the repository under each of its projects

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
The dashboard SHALL be delivered as a local generate-and-open command plus a publication lane that regenerates each registered repository's snapshot and publishes the snapshots and the index to a declared data source beside the dated doc-health reports. The served plane SHALL bake the APPLICATION — the renderer and its assets — and fetch its DATA at runtime from that source, keeping a baked snapshot only as a first-boot and offline fallback; the serving host is provided by the runtime install layer, and the dashboard MUST NOT be served from a public endpoint because the snapshot projects internal governance state. Regeneration of a PUBLISHED snapshot is scheduled, on-demand, and manually dispatchable — still no per-commit regeneration. A SESSION-LOCAL snapshot at a non-`main` ref SHALL additionally be regenerated after every gate action in its session: it is never published, so its regeneration cadence is a property of one human's working loop rather than of the publication lane, and coupling the two would be the mistake in either direction. Dashboard artifacts remain generated: the served plane reads them, and neither the renderer nor a viewer ever hand-edits a snapshot or an index.

#### Scenario: An operator wants the current picture
- **WHEN** the local command runs
- **THEN** it regenerates the snapshot from the working tree and opens the renderer against it

#### Scenario: A team viewer opens the hosted dashboard
- **WHEN** a viewer opens the dashboard on the internal host
- **THEN** the host serves the baked application against the most recently fetched snapshot behind the existing access control, modifying neither

#### Scenario: A public endpoint is proposed
- **WHEN** any delivery path would serve the dashboard from a public, unauthenticated endpoint
- **THEN** it MUST be rejected — the snapshot projects internal governance state and is served only from an access-controlled internal host

#### Scenario: Only the application changes require a rebuild
- **WHEN** newly published data must be reflected on the served plane
- **THEN** an image rebuild MUST NOT be required — rebuilds are for application changes

#### Scenario: The publication lane is asked to regenerate per commit
- **WHEN** a commit lands on a repository's `main`
- **THEN** the publication lane MUST NOT regenerate per commit — published regeneration stays scheduled, on-demand, and dispatchable

#### Scenario: A session regenerates per gate action
- **WHEN** a gate action lands inside a branch session
- **THEN** that session's own non-`main` snapshot MUST be regenerated, and no published snapshot MUST be touched

#### Scenario: Backfill scope is exceeded
- **WHEN** generation would fabricate register history for documents outside the worked-example fixtures
- **THEN** it MUST NOT — legacy docs without `Possible feats:` sections simply carry no possibles

### Requirement: Staged-topic proposal commissioning
The gate console SHALL offer a human-only `propose` action on a staging topic that commissions proposal authoring as a recorded dispatch — a `workflow-job` descriptor naming the proposal-authoring workflow and targeting the topic's staging id, plus a gate-action record — without authoring anything itself; the commissioned authoring runs externally and lands as an ordinary OpenSpec change subject to the existing review and ratify gates. The console SHALL refuse a topic absent from the pinned checkout's staging area and SHALL refuse a duplicate commission while a dispatched `propose` job for the same topic remains undelivered. The console SHALL ALSO refuse `propose` while the topic's tile carries an UNRESOLVED branch session, and the refusal MUST name the session and the two resolutions available — merge its pull request, or abandon the session to discard it. Proposal is the end of the staging pipeline: commissioning it from a tile whose drafts are still scattered across an unmerged branch would propose from a state no reviewer can see, so the human SHALL clear the session first. A session is UNRESOLVED while its snapshot registry entry is live; a merged session and an abandoned session are both resolved, and a branch surviving an abandon MUST NOT block propose, because the abandon already recorded the human's decision to discard. An abandoned branch is retained as reviewable evidence only until the topic's PROPOSAL exists; once it does, that branch MAY be deleted, because the proposal has closed the topic off and the abandoned exploration no longer has a question to answer. The deletion SHALL remain a human-invoked cleanup rather than an automatic consequence of commissioning — `propose` dispatches authoring and the proposal lands externally, so the branch MUST NOT be destroyed on the strength of a commission that has not yet produced anything.

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

#### Scenario: A non-console path invokes propose
- **WHEN** any caller that cannot demonstrate it originates from the human console this serve started calls the propose action
- **THEN** the call MUST be rejected and reported, like every gate action
- **AND** a process running as the identified human, which can read that console's own token, is NOT distinguished here — that distinction requires the xForge-host identity work deferred under D22, and the residual is accepted by D23

#### Scenario: Propose is invoked with a live branch session on the tile
- **WHEN** propose is invoked for a topic whose tile holds a live branch session
- **THEN** the console MUST refuse and persist nothing, naming the session branch and offering both resolutions — merge the session's pull request, or abandon the session
- **AND** the refusal MUST clear once the session ends by either route, with no further action required of the human

#### Scenario: A previously abandoned session leaves a branch behind
- **WHEN** propose is invoked for a topic whose session was abandoned but whose pushed branch still exists
- **THEN** propose MUST proceed — the session is resolved, and the surviving branch is reviewable evidence rather than unresolved working state

#### Scenario: An abandoned branch outlives the proposal that closed its topic
- **WHEN** a topic's proposal exists and an abandoned session branch for that topic is still present
- **THEN** that branch MAY be deleted — the proposal has closed the topic off, so the abandoned exploration is no longer evidence anyone needs
- **AND** the deletion MUST be human-invoked, never an automatic consequence of the `propose` dispatch, whose commissioned authoring may not have produced a proposal yet

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

### Requirement: Repository selector over the registered roster
The dashboard SHALL offer a repository selector whose roster is the repositories the project register declares, and MUST NOT maintain a second repository list of its own. Selecting a repository SHALL switch the ACTIVE snapshot to that repository at the default ref, after which every view renders from that one snapshot exactly as it does today. A repository whose corpus populates only SOME funnel stations SHALL render the stations it has data for and MUST NOT be refused, hidden, or degraded as a whole: adoption of any ideation convention MUST NEVER be a precondition of being selectable, and a station with no data in the selected repository MUST render an explicit empty state naming what is absent rather than a blank region. A repository present in the snapshot index but absent from the register SHALL remain selectable and render ungrouped, as the grouping hierarchy already requires. A selection naming an aggregate view across repositories SHALL compose from the snapshot index and the per-repository snapshots it names, and MUST NOT scan any repository directly.

#### Scenario: A human switches repositories
- **WHEN** a human selects a different repository in the selector
- **THEN** every view MUST re-render from that repository's snapshot, addressed at the default ref
- **AND** the roster offered MUST be the project register's repositories, not a list maintained by the dashboard

#### Scenario: A sparse repository is selected
- **WHEN** the selected repository's snapshot populates only some funnel stations — for example an install repository carrying only OpenSpec changes
- **THEN** the populated stations MUST render and the unpopulated ones MUST show an explicit empty state
- **AND** the repository MUST NOT be refused or hidden for lacking a convention

#### Scenario: A repository is missing from the register
- **WHEN** the index names a repository the project register does not
- **THEN** it MUST still be selectable and render ungrouped, without failing the dashboard

#### Scenario: An aggregate selection is rendered
- **WHEN** a selection spans repositories rather than naming one
- **THEN** it MUST compose from the index and the snapshots it names
- **AND** MUST NOT read any repository working tree directly

### Requirement: Snapshot source keyed by repository and ref
Every snapshot the dashboard reads SHALL be addressed by the PAIR (repository, ref), and a request that names no ref MUST resolve to `main`. The serving layer SHALL keep ONE snapshot registry keyed by that pair, and every renderer, index entry, and refresh binding MUST address snapshots through it rather than through a path convention of its own. The seam MUST carry `ref` from the first release even while only `main` is exercised, so a later session-scoped or runtime-plane consumer binds to it without the interface being re-cut. The served plane SHALL exercise only `(repository, main)`: a snapshot generated for any other ref is session-local derived data, MUST NEVER be published to the data source, MUST NEVER appear in the index the served plane fetches, and MUST NEVER become a shared view — main remains the shared truth on every shared surface. Source confinement SHALL hold per registry entry, so reading a document through a (repository, ref) entry MUST NOT be able to escape that entry's own root.

#### Scenario: A caller names no ref
- **WHEN** any renderer, refresh binding, or command requests a snapshot for a repository without naming a ref
- **THEN** it MUST resolve to that repository's `main` snapshot
- **AND** an existing consumer that never names a ref MUST keep working unchanged

#### Scenario: Two refs of one repository are registered
- **WHEN** the registry holds entries for the same repository at two different refs
- **THEN** each MUST serve its own snapshot and its own source root, with no cross-contamination between them

#### Scenario: A non-main snapshot is offered for publication
- **WHEN** any path would publish a snapshot for a ref other than `main`, or enter one into the served plane's index
- **THEN** it MUST be refused — non-`main` snapshots are session-local derived data and never shared state

### Requirement: Snapshot index contract
The available snapshots SHALL be enumerated by a thin, schema-versioned snapshot INDEX artifact carrying one entry per available (repository, ref) with that entry's repository, ref, snapshot location, `source_revision`, and generated-at stamp. The index SHALL be declared by its OWN contract and MUST NOT be folded into the snapshot schema: an index describes a SET of snapshots while a snapshot describes one repository's corpus at one revision, so carrying sibling facts inside a snapshot would break the determinism property that the same working tree yields a byte-identical snapshot. Each (repository, ref) pair MUST be unique within one index. The index MUST carry no funnel, document, cluster, possible, or keyword data — it is a locator, not a projection. Renderers and refresh bindings SHALL discover available snapshots only through the index, and an index entry whose snapshot cannot be fetched MUST be reported as that repository being unavailable, leaving the active view unaffected.

#### Scenario: A repository becomes available
- **WHEN** the publication lane adds an entry to the index for a newly registered repository
- **THEN** the selector MUST offer that repository with no application change and no image rebuild

#### Scenario: An indexed snapshot cannot be fetched
- **WHEN** an index entry names a snapshot the serving side cannot retrieve
- **THEN** that repository MUST be reported unavailable and the currently active view MUST continue to render

#### Scenario: The index is asked to carry projection data
- **WHEN** a change would add document, cluster, possible, or keyword data to the index
- **THEN** it MUST be rejected — that data belongs to the snapshot the index locates

### Requirement: Runtime snapshot fetch with baked fallback and displayed freshness
The served dashboard SHALL fetch the index and the active snapshot at RUNTIME from a declared external data source, and the served image SHALL bake the APPLICATION rather than the data — an image rebuild MUST NOT be required to reflect newly published snapshots. The runtime fetch SHALL be performed by the SERVING side into the snapshot registry, and the browser bundle MUST continue to address only its own origin, preserving the bundle's existing no-external-network boundary. A snapshot MAY remain baked into the image as a FIRST-BOOT and OFFLINE fallback ONLY. Whenever the fallback is what renders, the surface MUST display a stale banner naming the fallback's generated-at, and it MUST NEVER degrade to fallback data silently. Every view SHALL display a freshness header naming the active repository and ref, the active snapshot's `source_revision` in short form, and its generated-at, so the question "is the document I just landed in this view" is answerable without reasoning about deployment times.

#### Scenario: The data source is reachable
- **WHEN** the served dashboard starts or refreshes with the data source reachable
- **THEN** it MUST render the fetched snapshot, not the baked one
- **AND** the freshness header MUST name the active repository and ref, the snapshot's short `source_revision`, and its generated-at

#### Scenario: The data source is unreachable
- **WHEN** the index or the active snapshot cannot be fetched
- **THEN** the baked snapshot MUST render as the fallback
- **AND** a stale banner MUST state that the fallback is in use and name its generated-at — the degradation MUST NOT be silent

#### Scenario: A newly published snapshot needs no rebuild
- **WHEN** the publication lane publishes a newer snapshot for the active repository
- **THEN** reflecting it MUST require no image rebuild and no rollout

#### Scenario: The browser is asked to reach the data source
- **WHEN** any realization would have the browser bundle fetch the external data source directly
- **THEN** it MUST be rejected — the serving side performs the fetch and the bundle stays same-origin

### Requirement: Refresh affordances on both planes
The dashboard SHALL offer a refresh affordance, bound per plane, that grants NO authority the surface does not already have. On the SERVED plane refresh MUST re-fetch the index and the active snapshot into the registry and re-render, and MUST write nothing beyond that derived cache — fetching fresher derived data is a read. On the LOCAL plane refresh MUST re-run the snapshot generator against the served checkout and re-render, reachable only on a loopback bind, writing ONLY the derived snapshot artifact and mutating no governed content, with no server restart required. Neither binding MUST be able to trigger an image build, a rollout, a publication to the data source, or any write to a repository's governed content, and a refusal MUST leave the previously rendered snapshot in place rather than blanking the view.

#### Scenario: A document lands and the hosted viewer refreshes
- **WHEN** a document is committed to a repository's `main`, the publication lane runs, and a viewer clicks refresh on the served dashboard
- **THEN** the newly published snapshot MUST be fetched and the document MUST appear
- **AND** no image rebuild MUST have occurred and no write authority MUST have been exercised by the served surface

#### Scenario: A local author regenerates
- **WHEN** an author commits in the served checkout and uses the local refresh
- **THEN** the generator MUST re-run against that checkout and the document MUST appear without restarting the server
- **AND** only the derived snapshot artifact MUST have been written

#### Scenario: Refresh is asked to rebuild the app
- **WHEN** any refresh binding would trigger an image build, a rollout, or a publication
- **THEN** it MUST be rejected — refresh reads derived data and never executes a final action

#### Scenario: A refresh fails
- **WHEN** a refresh cannot complete
- **THEN** the previously rendered snapshot MUST remain rendered and the failure MUST be reported inline

#### Scenario: Newer data is advertised passively
- **WHEN** the served plane's background index poll (Brett's 2026-07-26 OQ2 ruling: passive hint, ~5-minute cadence) observes an index entry fresher than the loaded snapshot for the active repository
- **THEN** a passive newer-data hint MUST show on the surface
- **AND** the surface MUST NOT auto-reload — the view changes only when the viewer invokes refresh

### Requirement: Dispatchable publication, never from the served surface
The snapshot publication lane SHALL be manually dispatchable in addition to its schedule, so that an off-cycle data refresh is a governed CI action a human or a session triggers with an attributable run. The served dashboard MUST NOT be able to trigger publication, an image build, or a rollout by any path: a serving surface dispatches recorded requests at most and never executes a final action. A recorded-dispatch verb that would commission a rebake from the dashboard SHALL be out of scope here and MUST arrive, if ever, as its own change at its own gate. Off-cycle dispatch MUST change nothing else about the lane — the same generator, the same per-repository snapshots, the same index, the same commit posture as the scheduled run.

#### Scenario: An off-cycle refresh is needed
- **WHEN** a document lands shortly after the scheduled publication run
- **THEN** a human or a session MUST be able to dispatch the publication lane manually
- **AND** the dispatched run MUST produce the same artifacts as a scheduled run

#### Scenario: The dashboard is asked to commission a rebake
- **WHEN** any affordance on the served dashboard would trigger a build, a rollout, or a publication
- **THEN** it MUST be refused — the pod holds no build or rollout authority, and such a verb is a separate change at its own gate

### Requirement: Branch session lifecycle
The workbench SHALL open a BRANCH SESSION on a topic-bearing tile the first time a gate write is performed against that tile, and the session's working state SHALL live on a git branch materialized as a git WORKTREE rather than in the served checkout. The session branch name SHALL be derived deterministically from the TILE's scope identity — `draft/<topic-folder>` for a staged topic, where `<topic-folder>` is the topic FOLDER name and a colon-qualified corpus staging id MUST be reduced to its final segment so the derived name is a legal git ref, and the scope's kind and id for a cluster or a possible — never from the actor, so two humans working the same tile join the SAME session rather than forking two. The served checkout MUST NEVER be switched, reset, stashed, or otherwise moved by any session operation: session writes reach the branch only through its own worktree, which dissolves the shared-checkout hazard by construction rather than by discipline. A branch session SHALL end in exactly one of two ways — its pull request MERGES, or a human explicitly ABANDONS it — and on either ending the worktree, the session's snapshot registry entry, and the session notebook SHALL be torn down and the main view refreshed. On a MERGE the session BRANCH SHALL ALSO be deleted: the work is saved on `main`, so the branch holds nothing the merge did not preserve, and a surviving branch would only contend for its own deterministic name when the tile is worked again. An abandon SHALL be a recorded human gate action carrying a reason, MUST end only the SESSION, and MUST NOT delete history that has already been pushed or close a pull request on the human's behalf — a pushed branch and its PR remain reviewable evidence, and an abandoned session is RESOLVED even though its branch may survive. When the first gate write lands on a tile whose PREVIOUS session was abandoned and whose branch survives, the workbench MUST NOT silently pick a name: it SHALL notify the human that an abandoned branch exists and SHALL offer exactly two continuations — RESUME that branch, which keeps its existing name and re-materializes a worktree over it so the abandoned work is picked back up, or start NEW, which opens a fresh session under the next session ORDINAL (`draft/<topic-folder>-2`, derived as the highest existing ordinal plus one). The choice SHALL be offered ONLY while no live session holds the tile; once either continuation has opened a session, every later writer JOINS it under the rule above, so the prompt can never fork one tile into two sessions. A BRANCH session is distinct from the workbench's UI-lifetime "workbench session" that scopes the checked-keyword selection: a branch session outlives page loads, spans actors, and is ended only by a merge or an abandon.

#### Scenario: The first gate write on a tile opens a session
- **WHEN** a human performs the first gate write against a topic-bearing tile that has no active branch session
- **THEN** a session branch named from that tile's scope identity MUST be created and materialized as a git worktree
- **AND** the write MUST land in that worktree, not in the served checkout

#### Scenario: A second human opens the same tile
- **WHEN** another human performs a gate write against a tile that already has an active branch session
- **THEN** they MUST join the EXISTING session on the same branch rather than opening a second session
- **AND** the branch name MUST NOT encode either actor

#### Scenario: A tile with an abandoned branch is worked again
- **WHEN** the first gate write lands on a tile whose previous session was abandoned and whose branch still exists
- **THEN** the workbench MUST NOT choose a branch silently — it MUST report the abandoned branch and offer RESUME or NEW
- **AND** RESUME MUST re-materialize a worktree over the EXISTING branch under its existing name, so the abandoned work is continued rather than orphaned
- **AND** NEW MUST open a session on the next ordinal, `draft/<topic-folder>-2`, computed as the highest existing ordinal plus one

#### Scenario: Two humans reach an abandoned tile at once
- **WHEN** a second human performs a gate write after another human's resume-or-new choice has already opened a session
- **THEN** they MUST join that session rather than being offered the choice again — the prompt appears only while no live session holds the tile

#### Scenario: The served checkout is asked to move
- **WHEN** any session operation would switch, reset, or stash the served checkout's branch
- **THEN** it MUST be refused — the served checkout stays on its own ref for the life of every session

#### Scenario: A session is abandoned
- **WHEN** a human abandons an active branch session
- **THEN** the worktree, the session's snapshot registry entry, and the session notebook MUST be torn down and the abandon MUST be recorded with a reason
- **AND** any already-pushed branch and its pull request MUST survive the abandon

#### Scenario: A session's pull request merges
- **WHEN** a session's pull request merges
- **THEN** the session MUST end: the worktree, the session registry entry, and the session notebook are torn down and the main view is refreshed
- **AND** the session branch MUST be deleted, since the merge has preserved everything it held

### Requirement: A tile that has moved to proposal refuses branch sessions
A branch session SHALL NOT open, and an abandoned branch SHALL NOT be resumed, on a tile that carries a LIVE PROPOSAL — either a dispatched `propose` workflow-job that has not yet delivered, or a proposal that already exists for the topic. Proposal is the end of the staging pipeline, and a tile is in exactly ONE of two modes: it is a staging work surface, or it is a proposal, never both at once. Editing a topic's staging documents underneath a proposal authored FROM them would leave the two disagreeing with no record of which version the reviewer read, and any such edit would merge into `main` beneath a proposal that never saw it. The refusal SHALL name the route back: `demote`, which returns the proposal to staging for continued design; once a tile has been demoted it accepts sessions again exactly as before. While a `propose` dispatch is still in flight there is no proposal yet to demote, so the refusal SHALL say so rather than naming a route the human cannot take — the tile is closed until its proposal lands. This rule is the mirror of the `propose` refusal on an unresolved session: together they make the two states mutually exclusive from both directions, so a tile can never be simultaneously worked and proposed.

#### Scenario: A gate write arrives on a tile whose proposal exists
- **WHEN** a human performs a gate write against a tile that carries an existing proposal
- **THEN** no session MUST be opened and nothing MUST be persisted
- **AND** the refusal MUST name `demote` as the route back to a workable staging tile

#### Scenario: A gate write arrives while proposal authoring is still in flight
- **WHEN** a human performs a gate write against a tile whose `propose` workflow-job is dispatched and undelivered
- **THEN** no session MUST be opened, and the refusal MUST state that the proposal has not landed yet, so there is nothing to demote and the tile is closed until it does

#### Scenario: A demoted tile is worked again
- **WHEN** a tile's proposal has been demoted back to staging and a human performs a gate write against it
- **THEN** a branch session MUST open normally, under the ordinary naming and resume-or-new rules

#### Scenario: An abandoned branch is resumed on a proposed tile
- **WHEN** a tile carries a live proposal and an abandoned session branch for that tile still exists
- **THEN** the resume-or-new choice MUST NOT be offered and the branch MUST NOT be resumed — the tile is a proposal, not a work surface

### Requirement: One commit per gate action inside a branch session
Every gate action performed inside a branch session SHALL produce exactly ONE commit on the session branch, carrying BOTH the documents that action wrote and the gate-action record that attests to it, and that record SHALL name the commit as a `commit`-kind artifact. A record and the artifact it attests to MUST NOT land through separate paths: riding the same commit is what keeps them inseparable, and it is why a session's audit trail FALLS OUT of version control instead of being reconstructed beside it. A gate verb whose effect reaches OUTSIDE the branch — a workflow dispatch that actually runs, a publication, an image build, or a rollout — MUST NOT be performed from inside a branch session, because it would act on state that is not yet governed; those verbs remain main-resident. A gate action whose artifacts are FILES is session-legal, and it becomes governed STATUS only when the session's pull request merges, exactly as the gates-happen-on-main rule requires of any unmerged transition.

#### Scenario: A gate action lands as one commit
- **WHEN** a human performs any file-producing gate action inside a branch session
- **THEN** exactly one commit MUST appear on the session branch carrying that action's documents and its gate-action record together
- **AND** the record MUST reference that commit as a `commit`-kind artifact

#### Scenario: A reviewer reads the session's audit trail
- **WHEN** a reviewer opens the session's pull request
- **THEN** the commit series MUST read as one commit per gate action, so the audit trail is the branch history itself and not a separate ledger

#### Scenario: A record is asked to travel without its document
- **WHEN** any realization would write a session gate-action record in a different commit from the documents it attests to
- **THEN** it MUST be rejected — the record and its artifact ride together

#### Scenario: An externally-dispatching verb is invoked in a session
- **WHEN** a gate verb that dispatches work outside the branch — a running workflow, a publication, a build, or a rollout — is invoked from inside a branch session
- **THEN** it MUST be refused and reported: unmerged state is exploration and MUST NOT commission external action

### Requirement: Session-scoped document editing verb
The gate console SHALL offer a human-only `edit-document` verb that is valid inside an active branch session and MAY also be invoked by local doxBench as the tile's FIRST save when it targets that tile's own editable material. On an eligible first save, the route SHALL atomically materialize or join the tile's branch session, verify the supplied base ref/revision/content hash against the selected source, rewrite the existing document only in the resulting session worktree, and commit the rewrite as that action's single commit with its gate-action record. If validation or rewriting fails, the attempted first save MUST persist no document, commit, gate record, live registry entry, or orphan worktree. Every other invocation that names no live session MUST refuse. The verb MUST refuse a target outside the session worktree or outside the tile's own editable material; inherited, cluster-neighbourhood, cited, and inbound-context documents remain read-only in this tile even though they exist inside the worktree. The verb SHALL rewrite an EXISTING document, MUST NOT create one (that stays `create-document`), and MUST NOT delete one by any path. No per-edit redline ceremony SHALL be required of an on-branch edit, because THE PULL REQUEST REVIEW IS THE GOVERNANCE — the ratified gates-happen-on-main rule already holds that an unmerged transition is exploration and not status, which makes an unmerged branch precisely the place where ordinary editing is legal. The gate console's `edit-apply` redline path and the human external-editor escape hatch SHALL REMAIN UNCHANGED for a MAIN-RESIDENT document outside integrated branch-backed authoring. The `create-document` verb SHALL keep its create-only semantics unchanged and, inside a branch session, SHALL write into the session worktree instead of the served checkout. The verb MUST be loopback-only, MUST fail closed on an unresolved actor, and MUST reject and report any invocation that cannot demonstrate it originates from the human console this serve started, like every gate action — a process running as the identified human, which can read that console's own token, is NOT distinguished at this layer (D23), and every accepted invocation's record MUST therefore name the surface it arrived on and how console presence was shown.

#### Scenario: A document is edited inside a session
- **WHEN** a human invokes `edit-document` on the tile's own document in an active session's worktree with the current base hash
- **THEN** the document MUST be rewritten in that worktree and committed as that action's single commit with its gate-action record
- **AND** no redline artifact MUST be required before the edit lands

#### Scenario: An existing document is the first save
- **WHEN** local doxBench invokes `edit-document` as the tile's first save against the current base ref, revision, and hash of the tile's own editable material
- **THEN** the route MUST materialize or join the tile's branch session and commit the rewrite only in that session worktree
- **AND** the served checkout MUST remain untouched

#### Scenario: First-save validation fails
- **WHEN** the integrated first save carries a stale base hash, illegal target, invalid content, or any other edit refusal
- **THEN** it MUST persist no document, commit, gate record, live registry entry, or orphan worktree

#### Scenario: Editing is attempted without a session by another path
- **WHEN** `edit-document` is invoked with no active branch session and is not an eligible integrated first save
- **THEN** it MUST refuse and persist nothing — main-resident editing stays the `edit-apply` or external-editor path

#### Scenario: An edit targets a path outside the worktree
- **WHEN** `edit-document` names a path that does not resolve inside the active session's worktree root
- **THEN** it MUST refuse and persist nothing

#### Scenario: An edit targets context owned by another scope
- **WHEN** the tile's edit names an inherited, cluster-neighbourhood, cited, inbound, or other context document that is not the tile's own editable material
- **THEN** it MUST refuse even when that path exists inside the session worktree

#### Scenario: A session edit is asked to delete
- **WHEN** `edit-document` is invoked in a way that would remove a document
- **THEN** it MUST refuse — the verb rewrites, and no session verb grants delete authority

#### Scenario: Creating inside a session
- **WHEN** `create-document` is invoked while a branch session is active on the tile
- **THEN** the document MUST be created in the session worktree with the create-only semantics unchanged, and committed as that action's single commit

#### Scenario: A non-console path invokes the edit verb
- **WHEN** any caller that cannot demonstrate it originates from the human console this serve started calls `edit-document`
- **THEN** the call MUST be rejected and reported
- **AND** a process running as the identified human, which can read that console's own token, is NOT distinguished here — that distinction requires the xForge-host identity work deferred under D22, and the residual is accepted by D23
- **AND** the record of any accepted call MUST carry the surface it arrived on and how console presence was shown, so an act performed this way is auditable rather than invisible

### Requirement: Session snapshot addressed by repository and session ref
A branch session's workbench panels SHALL read a snapshot addressed by the (repository, session-branch) pair through the EXISTING snapshot registry, generated from the session WORKTREE, and MUST NOT introduce an overlay, a diff layer, or any second projection path over the `main` snapshot. The session snapshot SHALL be regenerated after EVERY gate action in the session, so a document created or edited in the session appears in that session's bullseye, docs panel, and outline without a manual step. A session snapshot SHALL be derived, session-local data: it MUST NEVER be published to a data source, MUST NEVER be entered in a published index, and MUST NEVER become a shared view. The freshness header SHALL name the SESSION BRANCH as the active ref whenever a session snapshot is what renders, so a draft view can never be mistaken for `main`.

#### Scenario: A created document appears in the session's panels
- **WHEN** a human creates or edits a document through a gate verb inside a branch session
- **THEN** the session snapshot MUST be regenerated and the document MUST appear in that session's panels without a manual regeneration step

#### Scenario: The session view names its ref
- **WHEN** a session snapshot is what renders
- **THEN** the freshness header MUST name the session branch as the active ref alongside the snapshot's source revision and generated-at

#### Scenario: A session snapshot is offered for publication
- **WHEN** any path would publish a session snapshot or enter it in a published index
- **THEN** it MUST be refused — session snapshots are session-local derived data

#### Scenario: An overlay is proposed instead
- **WHEN** a realization would render session drafts by overlaying or diffing them onto the `main` snapshot
- **THEN** it MUST be rejected — the session reads its own snapshot through the (repository, ref) registry

### Requirement: Session-confined draft visibility
Branch-session drafts SHALL be visible ONLY inside the branch session that holds them, and every shared surface — the wheel, the funnel, the pipeline board, the hosted dashboard, and every published projection — SHALL keep rendering `main`. A shared surface that showed someone's unmerged drafts would silently redefine what the team's pipeline picture MEANS, which is the same failure the gates-happen-on-main rule forbids; this requirement is that rule applied to the workbench. Inside the session the drafts SHALL be visible to EVERY actor who joins that session, because the branch is named for the tile and the session is collaborative by design. A draft SHALL become visible on shared surfaces only by merging, after which the ordinary publication lane picks it up on its own schedule.

#### Scenario: A draft is invisible outside its session
- **WHEN** a human creates a document inside a branch session and another human looks at the wheel, the funnel, or the hosted dashboard
- **THEN** the document MUST NOT appear on any of those surfaces — they render `main`

#### Scenario: A collaborator joins the session
- **WHEN** a second human opens the same tile's active branch session
- **THEN** they MUST see the session's drafts, because the session is per-tile and collaborative

#### Scenario: A draft becomes shared
- **WHEN** the session's pull request merges
- **THEN** the documents MUST become visible on shared surfaces through the ordinary publication lane, with no special path

### Requirement: Branch-aware source resolution
Document reads inside a branch session SHALL resolve through the SAME read-only source pass-through the document viewer already uses, bound to the SESSION WORKTREE, and the resolution MUST be confined to that worktree's own root so a session read can never escape into another ref's source or into the served checkout. The outline panel and the read-only viewer SHALL render branch drafts through that route and MUST NOT gain a second read path. A read naming a path outside the active session's root MUST refuse rather than fall back to `main`, because a silent fallback would render a stale document under a draft heading. Outside a branch session the pass-through SHALL resolve against the served checkout exactly as it does today, unchanged.

#### Scenario: The outline panel renders a branch draft
- **WHEN** a human opens the `outline` panel inside an active branch session
- **THEN** the fragment MUST render from the session worktree through the read-only pass-through

#### Scenario: A session read escapes its root
- **WHEN** a session read names a path that does not resolve inside the session worktree's root
- **THEN** it MUST refuse, and MUST NOT fall back to the `main` copy of that path

#### Scenario: A read outside a session is unchanged
- **WHEN** a document is read with no active branch session
- **THEN** the pass-through MUST resolve against the served checkout exactly as before this change

### Requirement: Session save through the open-pr gate verb
The gate console SHALL offer a human-only `open-pr` verb that SAVES a branch session by pushing the session branch and opening a pull request into the EXISTING Merge-Master review ritual, recording the dispatch as a gate-action record that names the session branch and references the pull request as a `pull-request`-kind artifact. The verb SHALL create NO new approval path and grant NO authority: it MUST NOT merge, approve, self-review, or bypass any branch protection, and the merge remains the Merge Master's action under the existing ritual. The verb MUST NOT require ANY readiness signal to have fired — neither the blocking STAGED-TO-PROPOSAL readiness gate that refuses `propose` for a topic whose health status is not `ready`, nor the advisory readiness RECOMMENDATION gate of the cross-reference capability: a session pull request is exploration offered for review, and readiness guards PROPOSE, not SAVE. Naming both is deliberate, because they are different mechanisms and only one of them blocks: a rule that named only the advisory recommendation would forbid nothing and leave the blocking gate free to be wired to this verb. Requiring the blocking gate here would in fact DEADLOCK the surface — that gate scores the documents that live in the topic folder on the served checkout, a session's documents reach the served checkout only when its pull request merges, and so a topic worked from a new session could never become `ready` while the only route to `main` was the pull request the gate refused. Invoking the verb on a session that already has an open pull request SHALL update and report that pull request rather than opening a second one for the same branch. On merge the documents become governed content on `main`, the publication lane reflects them on its own schedule, and the session tears down as its lifecycle requires. The verb MUST be loopback-only, MUST fail closed on an unresolved actor, and MUST reject and report any invocation that cannot demonstrate it originates from the human console this serve started; a process running as the identified human is NOT distinguished at this layer (D23), and every accepted invocation's record MUST name the surface it arrived on and how console presence was shown. The identity the verb writes under SHALL follow the PLANE: on the LOCAL plane the push and the pull request SHALL be performed with the invoking engineer's OWN credential — their existing authenticated GitHub session, never a stored service identity, App installation token, or any other credential minted for the surface; on the HOSTED plane the verb MUST perform the remote write and open the pull request as the openxfactory domain App once that App exists, and MUST NOT use a personal credential there (D22).

#### Scenario: A session is saved
- **WHEN** a human invokes `open-pr` on an active branch session
- **THEN** the branch MUST be pushed, a pull request MUST be opened into the existing review ritual, and a gate-action record MUST name the branch and reference the pull request as a `pull-request`-kind artifact

#### Scenario: The save verb is asked to merge
- **WHEN** any path would have `open-pr` merge, approve, or bypass protection on its own pull request
- **THEN** it MUST be refused — saving hands work to the Merge-Master ritual and holds no approval authority

#### Scenario: A session without a passing readiness gate is saved
- **WHEN** a human invokes `open-pr` on a session whose topic is not `ready` under the staged-to-proposal readiness gate, or carries no fired readiness recommendation, or both
- **THEN** the save MUST proceed — a session pull request is exploration, and readiness is a precondition of proposing, not of saving
- **AND** no readiness signal of either kind MUST be consulted by the verb at all

#### Scenario: The verb is invoked twice
- **WHEN** `open-pr` is invoked on a session that already has an open pull request
- **THEN** it MUST update and report the existing pull request and MUST NOT open a second one for the same branch

#### Scenario: A saved session merges
- **WHEN** the session's pull request merges
- **THEN** the documents MUST be governed content on `main`, the session MUST tear down, and the main view MUST refresh

#### Scenario: The push identity follows the plane
- **WHEN** `open-pr` pushes a session branch from the local plane
- **THEN** the remote write MUST be performed under the invoking engineer's own credential, never a stored service identity
- **AND WHEN** `open-pr` runs on the hosted plane
- **THEN** the push and the pull request MUST use the openxfactory domain App, never a personal credential

### Requirement: Branch sessions are a local-plane capability
Branch sessions SHALL exist on the LOCAL plane only, and the hosted dashboard MUST expose NONE of this capability: no session, no branch-ref selection, no `edit-document`, no `open-pr`, no abandon, no worktree, and no non-`main` snapshot. A hosted session would have to apply writes the hosted surface holds no authority to make, so the capability MUST NOT be offered there before the intent plane's apply lane exists. The (repository, ref) seam SHALL be the binding point that makes a hosted session possible WITHOUT redesign the moment an apply lane can produce a ref, and until then the hosted plane SHALL exercise only `(repository, main)`. Where the gate capability is absent, every session affordance SHALL render as a COPYABLE CLI DESCRIPTOR and MUST NOT render as a live button, and no session write path MUST be reachable from the page.

#### Scenario: The hosted surface is asked for a session
- **WHEN** the dashboard renders on the hosted plane
- **THEN** no session affordance, branch-ref selection, or session verb MUST be present, and no non-`main` snapshot MUST be reachable

#### Scenario: A hosted request names a non-main ref
- **WHEN** a request on the hosted plane addresses a snapshot at any ref other than `main`
- **THEN** it MUST refuse — the hosted plane exercises only `(repository, main)`

#### Scenario: The gate capability is off
- **WHEN** the workbench renders on a surface without the gate capability
- **THEN** every session affordance MUST render as a copyable CLI descriptor and no session write MUST be reachable from the page

#### Scenario: A hosted session becomes possible
- **WHEN** the intent plane's apply lane can produce a ref for an applied intent
- **THEN** a hosted session MUST be reachable by binding that ref through the existing (repository, ref) seam, with no re-cutting of the snapshot source interface

### Requirement: doxBench scoped view
The dashboard SHALL provide doxBench as the named evolution of the staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — with three coordinated regions over that scope. A context region SHALL retain `docs` and `lens`: `docs` SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them; `lens` SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. An authoring canvas SHALL present exactly two primary tabs, `Outline` and `Document`: Outline SHALL load the topic's declared outline material when one exists — for a staged topic, the fragment's outline material — and Document SHALL load the active document selected from the scoped docs set; both SHALL provide browser-local editing plus live rendered Markdown preview on the local human console, while an absent outline remains an explicit empty/create state rather than fabricated content. A chat region SHALL contain Working subject, transcript, server-declared model selection, and composer, and SHALL ground turns on the current canvas buffers as specified by this change. doxBench's corpus write authority SHALL remain the human-only gate verbs `create-document`, `edit-document`, `open-pr`, and session abandon: buffer edits, chat turns, and AI Apply MUST write no corpus document, register entry, workbench manifest, snapshot, branch, or gate artifact; Save MAY materialize/join a branch session and invoke only create/edit as specified; no verb MAY delete a document; and no session write may touch the served checkout. With the gate/model capabilities absent or on the hosted plane, the context SHALL remain usable and doxBench SHALL render read-only outline/document content without reachable editing, chat, or write controls.

#### Scenario: doxBench opens on a cluster
- **WHEN** a human opens doxBench from a cluster tile
- **THEN** the view MUST scope to that cluster: `docs` lists exactly that cluster's snapshot document edges and `lens` is scoped to that cluster's declared topics
- **AND** the canvas MUST show an honest empty Outline state unless that scope declares outline material

#### Scenario: doxBench opens on a possible
- **WHEN** a human opens doxBench from a possible tile
- **THEN** `docs` MUST list the documents its recorded supporting evidence cites
- **AND** any documents inherited from its claiming clusters MUST appear in a separately labelled section, distinct from cited evidence

#### Scenario: doxBench opens on a staged topic
- **WHEN** a human opens doxBench from a staged-topic tile
- **THEN** `docs` MUST list the topic folder's corpus documents together with every document whose declared destination names that staging topic
- **AND** the member documents of the topic's linked clusters MUST appear in a separately labelled cluster-neighbourhood section, never conflated with the topic's own material
- **AND** the Outline canvas MUST load that fragment's outline material from the active repository/ref

#### Scenario: A document becomes active
- **WHEN** a human selects a row in the scoped docs context
- **THEN** the Document canvas MUST load that exact document and make Document the active authoring tab
- **AND** docs/lens context and chat state MUST remain available

#### Scenario: Cluster-neighbourhood documents stay out of health
- **WHEN** a staged topic's health or its readiness gate is computed
- **THEN** cluster-neighbourhood documents MUST contribute nothing — health and the gate stay derived from the topic FOLDER's own corpus documents only

#### Scenario: A docs row shows how far a document has come
- **WHEN** the docs context renders a document the snapshot scores
- **THEN** its bar and named signals MUST come from the snapshot's `completeness` object verbatim
- **AND** doxBench MUST NOT compute, adjust, or re-weight any signal

#### Scenario: The source pass-through is absent
- **WHEN** doxBench runs against a served static image with no `/source` route
- **THEN** the docs and lens context MUST still render from the snapshot
- **AND** the canvas MUST report unavailable source content inline and MUST NOT expose editing or chat

#### Scenario: A scope carries no outline
- **WHEN** the opened tile has no outline material
- **THEN** the Outline canvas MUST render an explicit empty state rather than fabricating or drafting one
- **AND** only a capable local human console MAY offer a create-backed outline buffer

#### Scenario: A human edits before a session exists
- **WHEN** a capable local human edits an outline or document buffer with no active branch session
- **THEN** the edit MUST remain browser-local and available to the next chat turn
- **AND** the served checkout and every shared surface MUST remain unchanged

#### Scenario: An existing document is saved
- **WHEN** a human saves an existing eligible buffer from doxBench
- **THEN** `edit-document` MUST persist it on the tile's branch session as that action's single commit
- **AND** the served checkout MUST remain untouched

#### Scenario: doxBench renders without gate or model capability
- **WHEN** doxBench runs on a surface where gate and model capabilities are absent
- **THEN** docs/lens and available source content MUST remain readable
- **AND** no editing, chat, Apply, Save, or other write-implying control MUST be reachable

#### Scenario: doxBench is used on a narrow viewport
- **WHEN** the three desktop regions cannot remain usable side by side
- **THEN** the same context, Outline/Document canvas, and chat regions MUST stack without losing state, labels, keyboard reachability, or focus order

### Requirement: doxBench surface identity
The dashboard SHALL name the integrated staging-workbench authoring surface **doxBench**, using that exact casing in visible product copy, navigation and heading text, accessible names, documentation, tests, and realization evidence. doxBench SHALL remain the named human-facing evolution of the existing `ideation-dashboard` staging workbench rather than a second capability. Existing technical identifiers — including `workbench-*` schemas, routes, module names, the `workbench-chat-turn` kind, `WorkbenchModelPort`, branch-session records, and persisted dashboard artifacts — MUST remain compatible and MUST NOT be renamed or rewritten solely to adopt the doxBench name.

#### Scenario: The integrated authoring surface is presented
- **WHEN** the dashboard exposes the integrated authoring surface
- **THEN** its visible heading and accessible surface name MUST use the exact name `doxBench`
- **AND** generic controls MAY retain descriptive workbench terminology where that terminology names an inherited technical concept

#### Scenario: Existing workbench artifacts are loaded
- **WHEN** doxBench consumes a pre-name snapshot, branch-session record, route, schema, or other `workbench-*` artifact
- **THEN** that artifact MUST remain valid and usable without migration
- **AND** no persisted identifier or artifact kind MUST be rewritten merely to carry the doxBench name

### Requirement: doxBench editor buffer contract
The local doxBench surface SHALL maintain exactly two explicit authoring buffers for its canvas — `outline` and `document` — and each buffer SHALL carry its kind, repository-relative path or `null` for a not-yet-created artifact, repository, base ref, base source revision, base content hash, current content hash, current text, and dirty state. The outline buffer SHALL be seeded from the opened scope's declared outline material when one exists and MUST NOT be fabricated from the active document's headings; the document buffer SHALL be seeded from the active document selected from the scoped document set or from the existing create-document flow. Editing either buffer MUST be a browser-local, reversible action that writes no corpus document, snapshot, register, workbench manifest, gate artifact, or branch until the human invokes Save. Save SHALL compare current and base hashes, persist a new path through `create-document` and an existing path through `edit-document`, preserve each verb's existing validation and authority boundary, and refresh/rebase each successfully saved buffer from the resulting session ref and source revision. Saving two dirty backed buffers SHALL invoke one existing gate action per changed document in deterministic outline-then-document order and MUST NOT invent a multi-document write verb, rewrite history, or hide partial success. Discard SHALL restore the last loaded/saved base content and MUST persist nothing.

#### Scenario: A human edits the outline before chatting
- **WHEN** a human changes the outline buffer without invoking Save
- **THEN** the canvas MUST show the outline as dirty
- **AND** no corpus file, branch, snapshot, register, manifest, or gate record MUST change

#### Scenario: A human selects a document
- **WHEN** a human selects a document from the scoped `docs` context
- **THEN** the `Document` buffer MUST load that exact document from the active repository/ref and record its source revision and content hash
- **AND** changing the selection with unsaved document edits MUST require the human to save or discard rather than silently replacing the buffer

#### Scenario: A scope has no outline
- **WHEN** the opened scope declares no outline material
- **THEN** the Outline tab MUST show an explicit empty state
- **AND** it MAY offer a new outline buffer whose first persistence uses `create-document`, but it MUST NOT fabricate or persist an outline merely by opening the tab

#### Scenario: One dirty buffer is saved
- **WHEN** the human invokes Save with exactly one backed buffer dirty
- **THEN** exactly one `create-document` or `edit-document` gate action MUST persist that buffer on the tile's branch session
- **AND** the successful response MUST become the buffer's new base ref, revision, content, and hash

#### Scenario: Both dirty buffers are saved
- **WHEN** the human invokes Save with both backed buffers dirty
- **THEN** the outline action MUST run before the document action and each changed document MUST produce its own existing gate-action commit
- **AND** no combined or hidden write verb MUST be introduced

#### Scenario: The second save action fails
- **WHEN** the outline save commits and the subsequent document save refuses
- **THEN** the UI MUST report the committed outline and refused document separately
- **AND** the outline buffer MUST advance to its committed base while the document buffer remains dirty
- **AND** the system MUST NOT amend, reset, or otherwise erase the committed outline action

#### Scenario: A human discards local edits
- **WHEN** the human invokes Discard on a dirty buffer
- **THEN** that buffer MUST return to its last loaded or saved base content
- **AND** no gate action or provider call MUST occur

### Requirement: Grounded doxBench chat turn
The local human-console doxBench surface SHALL offer a chat rail containing a `Working subject` field, transcript, server-declared model selector, and message composer. Each submitted turn SHALL use a versioned `workbench-chat-turn` request containing the repository/ref and tile scope, active document path, `working_subject`, new user message, bounded prior transcript, selected model id, a client-generated turn id, and the complete current outline and document buffer descriptors and text including their hashes. The server MUST independently resolve and confine the repository/ref, tile, outline path, and active document path before a provider call; MUST verify every declared content hash; and MUST record in the response the exact buffer hashes, model id, and turn id used. Unsaved buffer text SHALL be eligible turn input and MUST be labelled as working state rather than governed or committed content. The next turn SHALL use the buffer contents that exist when that next turn is submitted, including intervening human edits and locally applied AI proposals, rather than reusing a previous turn's text. The request/response schemas SHALL impose explicit byte, transcript-turn, and output bounds; an over-bound turn MUST refuse with the applicable measured limit and MUST NOT silently truncate, summarize, or omit either buffer. Exactly one turn MAY be in flight per browser conversation key. Within one server process, the client turn id SHALL be idempotent: a repeated completed id with identical input hashes SHALL return the recorded result without another provider dispatch, an in-flight repeat SHALL attach to or report that turn, and reuse with different content or hashes MUST refuse. A provider or response-validation failure MUST return a fixed redacted error, preserve both buffers, append no assistant proposal, and disclose no credential, raw provider response, prompt, document content, or unsaved text in logs or error details.

#### Scenario: A human edit feeds the next turn
- **WHEN** a human edits either buffer after one assistant response and submits another message
- **THEN** the new request MUST carry the edited current buffer text and hash
- **AND** the response MUST identify that hash as the content the model saw

#### Scenario: Unsaved edits are discussed
- **WHEN** a dirty buffer is included in a chat turn
- **THEN** the model MAY use that exact unsaved text
- **AND** neither the request nor response MUST represent the text as committed, governed, or present on `main`

#### Scenario: The route receives a mismatched path or hash
- **WHEN** a turn names a path outside the opened tile's allowed scope, a repository/ref other than the active binding, or a hash that does not match the supplied text
- **THEN** the route MUST refuse before any provider call
- **AND** no browser conversation state or corpus state MUST be persisted by the server

#### Scenario: A turn exceeds a declared limit
- **WHEN** the combined buffers, transcript, message, or requested output exceed the selected catalog entry's or route's limit
- **THEN** the route MUST refuse and name the exceeded dimension and limit
- **AND** it MUST NOT silently truncate or send a partial document to the provider

#### Scenario: A turn completes
- **WHEN** the provider returns a valid response for the exact request
- **THEN** the chat rail MUST append assistant prose and any typed proposals under one turn id
- **AND** focus, active canvas tab, editor selection, scroll position, and dirty state MUST remain usable

#### Scenario: A completed turn is retried
- **WHEN** the same client turn id is submitted again in the same server process with identical content and hashes
- **THEN** the recorded result MUST be returned without a second provider dispatch

#### Scenario: A turn id is reused for different content
- **WHEN** a client turn id is repeated with different buffer text, hashes, subject, message, or model
- **THEN** the server MUST refuse the idempotency conflict before any additional provider call

#### Scenario: A provider or response validation fails
- **WHEN** the provider call fails or its response violates the typed response schema
- **THEN** both editor buffers MUST remain byte-identical and no assistant proposal MUST be appended
- **AND** the UI MUST receive a fixed actionable failure while logs and response details reveal no credential, raw provider payload, prompt, document content, or unsaved text

### Requirement: doxBench model catalog and provider boundary
The dashboard backend SHALL expose a same-origin workbench model catalog whose entries carry a stable opaque model id, human label, provider class, input/output limits, availability, and a human-readable data-handling badge. The catalog MUST NOT expose a provider credential, raw secret, raw endpoint, secret environment-variable name, or provider request template, and the browser MUST NOT call any model provider directly. A chat turn SHALL accept only a model id present and available in the current catalog and SHALL resolve that id through a server-side injected model-provider port. Provider credentials MUST come only from the deployment's approved server-side credential mechanism and MUST NOT enter browser storage, a request body, response body, dashboard snapshot, chat transcript, log, gate record, git artifact, or exception detail. A hosted fallback MAY be offered only when the deployment explicitly enables it and its configured data-handling policy meets the catalog badge; otherwise the model MUST be unavailable. The model catalog and turn routes SHALL be offered only on a loopback human console with a real checkout, resolved actor, and demonstrated console presence; the hosted/read-only plane MUST offer neither route.

#### Scenario: The browser loads model choices
- **WHEN** local doxBench opens with one or more allowed providers configured
- **THEN** the selector MUST show exactly the available catalog entries and their data-handling badges
- **AND** no credential or raw provider endpoint MUST be present in the page or catalog response

#### Scenario: No model is configured
- **WHEN** the model catalog is empty
- **THEN** the chat rail MUST explain that no allowed model is configured
- **AND** the Outline and Document editors MUST remain usable

#### Scenario: An unknown model id is submitted
- **WHEN** a chat request names a model id absent from or unavailable in the current catalog
- **THEN** the server MUST refuse before any provider call

#### Scenario: A browser attempts a direct provider call
- **WHEN** the dashboard bundle or runtime would contact a model endpoint other than the same-origin workbench routes
- **THEN** the renderer boundary MUST fail validation and the call MUST NOT ship

#### Scenario: Hosted doxBench is opened
- **WHEN** doxBench runs on the hosted/read-only plane
- **THEN** the model catalog and turn capabilities MUST be absent
- **AND** no chat or editor control implying unavailable authority MUST be reachable

### Requirement: Typed AI proposals and stale-application protection
A workbench chat response MAY contain ordinary assistant prose and zero or more typed edit proposals, and each proposal SHALL name exactly one target (`outline` or `document`), carry complete proposed content, identify the target buffer's input `base_hash`, and include a human-readable summary. A provider response MUST NOT write, save, commit, create, delete, or apply any document by itself. The browser SHALL render Apply only for schema-valid typed proposals. Applying a proposal SHALL replace only the named browser buffer, mark it dirty, remain locally reversible, and MUST NOT invoke Save or any gate action. Immediately before Apply, the browser MUST recompute the target buffer hash and compare it with the proposal's `base_hash`; a mismatch MUST refuse as stale and offer inspection of current versus proposed content or a new turn, but MUST NOT silently merge or expose an authority-bypassing force-apply action. Chat prose without a typed proposal MUST NOT be inferred as replacement content.

#### Scenario: An AI proposes a document revision
- **WHEN** a valid response proposes document content against the current document hash
- **THEN** the human MAY apply it to the Document buffer
- **AND** the buffer MUST become dirty while the corpus and branch remain unchanged until Save

#### Scenario: A proposal targets both buffers
- **WHEN** one turn returns valid outline and document proposals
- **THEN** each proposal MUST have its own target and base hash
- **AND** the human MUST be able to apply or reject each independently

#### Scenario: Human work makes a proposal stale
- **WHEN** the human changes the target buffer after the turn was issued and then invokes Apply
- **THEN** Apply MUST refuse because the current hash differs from the proposal base hash
- **AND** the current human text MUST remain unchanged

#### Scenario: A provider returns prose that looks like a document
- **WHEN** assistant prose contains Markdown but no schema-valid typed proposal
- **THEN** the UI MUST render it as conversation only and MUST NOT offer or perform document replacement

#### Scenario: An applied proposal is saved
- **WHEN** the human reviews an applied proposal, optionally edits it, and invokes Save
- **THEN** persistence MUST occur only through the applicable existing create/edit gate action
- **AND** the saved gate record MUST attest to the human action, not claim that the provider held write authority

### Requirement: Browser-local doxBench conversation
doxBench SHALL keep `working_subject`, selected model id, and bounded transcript in browser `sessionStorage` keyed by repository, ref, tile kind, and tile id, and SHALL treat that state as ephemeral per-browser working context rather than a branch-session descriptor, shared conversation, snapshot field, corpus artifact, or governance record. The working subject SHALL default from the tile's title or summary, remain editable, and affect authoring focus only; it MUST NOT be interpreted or copied into any customer `subject_ref`, actor, patient, tenant, authority, credential, routing identity, or other identity-bearing subject field. A normal refresh in the same browser session MAY restore matching working state, but changing to a different repository/ref/tile key MUST NOT leak the prior state into the new scope. Ending a branch session by merge or abandon SHALL clear state for that session key.

#### Scenario: A page refresh restores the same conversation
- **WHEN** the page reloads in the same browser session on the identical repository/ref/tile key
- **THEN** the matching working subject, selected available model, and bounded transcript MAY be restored
- **AND** no server-side conversation store or corpus artifact MUST be required

#### Scenario: doxBench changes scope
- **WHEN** the active repository, ref, tile kind, or tile id changes
- **THEN** working state from the previous key MUST NOT appear in the new chat rail or buffers

#### Scenario: A session ends
- **WHEN** the branch session merges or is abandoned
- **THEN** browser working state keyed to that session ref MUST be cleared

#### Scenario: Working subject resembles an identity
- **WHEN** a human types a customer, patient, tenant, or other identity-shaped value into Working subject
- **THEN** the system MUST continue to treat it only as free-form prompt focus
- **AND** it MUST NOT bind, validate, route, or persist it as an identity subject

### Requirement: Executing demote from the wheel action row
The gate console SHALL expose `demote` as an executing dashboard verb — a loopback-gated executing route and an expanded-tile action-row button on the wheel column whose tiles carry a change id — under the same capability gate as the other executing verbs (real checkout, resolved actor, human gate), and the dashboard invocation SHALL produce exactly the engine's existing demotion artifacts: the transition manifest, the executable plan, the register-update note, and a `demote` gate-action record carrying the required `reason`. The dashboard invocation MUST NOT mutate the live corpus — the file moves remain the separate, human-run execution step of the same governed tooling — and the console SHALL refuse a missing `reason`, a target change absent from the snapshot, and any agent-invoked call, persisting nothing on refusal.

#### Scenario: A proposal is sent back from the action row
- **WHEN** a human activates demote on an expanded tile for a change under the gate capability
- **THEN** the transition manifest, executable plan, register-update note, and `demote` gate-action record are written through the human gate
- **AND** no document in the live corpus is moved or edited by the dashboard call

#### Scenario: An unreasoned demote is refused
- **WHEN** demote is invoked without a reason
- **THEN** the console MUST refuse with the reason requirement and persist nothing

#### Scenario: The execution half stays human-run
- **WHEN** a demote has been planned and recorded from the dashboard
- **THEN** the corpus transition happens only when a human runs the recorded executable plan

#### Scenario: An agent invokes demote
- **WHEN** any agent or automated path calls the demote action
- **THEN** the call MUST be rejected and reported, like every gate action

### Requirement: Accepted-possible promotion to staging
The gate console SHALL offer a human-only `promote-to-staging` action on a possible that commissions the organization of that possible into `ideation/staging/<topic>/` as a fragment — a `workflow-job` descriptor naming the staging-fragment authoring workflow and targeting the possible's register id (optionally carrying a proposed topic slug), plus a `promote-to-staging` gate-action record — and the console MUST NOT author the fragment or mutate the possibles register: the possible's `latent → picked` pick edge is recorded only when the commissioned fragment is delivered, never at commission time. Promotion SHALL presuppose an accepted disposition — the console MUST refuse a derived possible still `pending_review` (it must be disposed first), a `rejected` or `superseded` possible, an already-`picked` possible, and a register id absent from the pinned checkout — and MUST refuse a duplicate commission while a dispatched `promote-to-staging` job for the same possible remains undelivered.

#### Scenario: An accepted possible is commissioned into staging
- **WHEN** a human runs promote-to-staging on an accepted (`latent`) possible
- **THEN** a `workflow-job` descriptor (target `possible_id`) and a `promote-to-staging` gate-action record are written through the human gate
- **AND** the possibles register is unchanged — no pick edge, no state transition

#### Scenario: An undisposed derived possible is refused
- **WHEN** promote-to-staging is invoked on a derived possible whose machine disposition is still `pending_review`
- **THEN** the console MUST refuse, citing the missing human disposition, and persist nothing

#### Scenario: A rejected or already-picked possible is refused
- **WHEN** promote-to-staging is invoked on a `rejected`, `superseded`, or already-`picked` possible
- **THEN** the console MUST refuse with the entry's state as the reason

#### Scenario: A duplicate promotion is refused
- **WHEN** promote-to-staging is invoked for a possible that already carries a dispatched, undelivered `promote-to-staging` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch

### Requirement: Cluster-scoped possibles-derivation commissioning
The gate console SHALL offer a human-only `derive-possibles` action on a topic cluster that commissions a cluster-scoped run of the promoted possibles-derivation lane as a recorded dispatch — a `workflow-job` descriptor naming the `derive-possibles` workflow and carrying the cluster id, plus a `derive-possibles` gate-action record — without deriving anything itself and without altering that lane's contract: the commissioned run stays bounded and read-only, its candidates arrive `origin: ai-derived` with machine disposition `pending_review`, they merge into the register only through the lane's own concurrency-protected merge, and every verdict on them remains a human act on the dispose tray. The console SHALL refuse a cluster id absent from the snapshot's cluster set and SHALL refuse a duplicate commission while a dispatched `derive-possibles` job for the same cluster remains undelivered.

#### Scenario: A cluster is commissioned for derivation
- **WHEN** a human runs derive-possibles on a cluster tile under the gate capability
- **THEN** a `workflow-job` descriptor (workflow `derive-possibles`, target `cluster_id`) and a `derive-possibles` gate-action record are written through the human gate
- **AND** no register entry is created by the console itself

#### Scenario: The commissioned run auto-promotes nothing
- **WHEN** the commissioned cluster-scoped run delivers candidates
- **THEN** they enter as `pending_review` derived possibles awaiting human disposition, exactly as a nightly lane run's candidates do

#### Scenario: An unknown cluster is refused
- **WHEN** derive-possibles is invoked for a cluster id the snapshot does not carry
- **THEN** the console MUST refuse with the reason and persist nothing

#### Scenario: A duplicate derivation is refused
- **WHEN** derive-possibles is invoked for a cluster that already carries a dispatched, undelivered `derive-possibles` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch

### Requirement: Pre-verdict research brief commissioning
The gate console SHALL offer a human-only `research-brief` action on a possible that commissions an evidence brief for that possible BEFORE the human rules on it — sources, prior art, and overlap with existing capabilities and specs — as a recorded dispatch: a `workflow-job` descriptor naming the research-brief workflow and targeting the possible's register id, plus a `research-brief` gate-action record. The commissioned brief SHALL be delivered as staging-compatible material accompanying the possible, and it MUST NOT dispose the possible, edit its register entry, or add evidence to it autonomously; a brief SHALL NOT be a precondition for any disposition. The console SHALL refuse a register id absent from the pinned checkout and SHALL refuse a duplicate commission while a dispatched `research-brief` job for the same possible remains undelivered.

#### Scenario: A pending possible is researched before the verdict
- **WHEN** a human runs research-brief on a possible awaiting disposition
- **THEN** a `workflow-job` descriptor (target `possible_id`) and a `research-brief` gate-action record are written through the human gate
- **AND** the possible's disposition state is untouched

#### Scenario: The brief informs, it never decides
- **WHEN** a commissioned brief is delivered
- **THEN** it lands as staging-compatible material referencing the possible and the human still disposes on the gate console

#### Scenario: Disposition never waits on a brief
- **WHEN** a human disposes a possible for which no brief was ever commissioned
- **THEN** the disposition proceeds unaffected

#### Scenario: A duplicate brief is refused
- **WHEN** research-brief is invoked for a possible that already carries a dispatched, undelivered `research-brief` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch

### Requirement: Lens set-builder gate verbs
The gate console SHALL offer two human-only verbs that execute a keyword-lens plan through the existing tested engines as recorded dispatches, enforced at the route so the lens plan panel, the CLI, and a direct request are gated identically. `lens-save-recipe` SHALL execute a save-recipe plan verbatim: the `ideation-workbench` manifest is written through the workbench engine (gitignored, schema-validated at write, reasoned-override guard intact) together with a gate-action record. `lens-add-as-cluster` SHALL execute an add-as-cluster plan: the recipe-seeded manifest plus the `pending_review` human-seen submission into the cross-reference queue, with the full evidence contract enforced BEFORE persistence, together with a gate-action record; the generated cross-reference index MUST NOT be written — acceptance remains the disposing authority's governed act outside these verbs. Every refusal the engines already define SHALL surface as a route refusal that persists nothing: a reasonless override, a duplicate set name, a submission lacking evidence, a validation failure (reject-and-report, prior state intact). When the gate capability is live the lens plan panel SHALL offer an execute affordance posting the confirmed plan to the verb route; when it is absent the panel SHALL stay plan-only, exactly as the read-only posture renders today. Agent invocations MUST be rejected and reported, like every gate action.

#### Scenario: A save-recipe plan is executed
- **WHEN** a human confirms a save-recipe plan and executes it through the gate
- **THEN** the workbench manifest is written exactly as the plan displayed — recipe line, members, reasoned overrides — and a gate-action record is persisted
- **AND** the write is schema-validated before landing

#### Scenario: An add-as-cluster plan is executed
- **WHEN** a human confirms an add-as-cluster plan and executes it through the gate
- **THEN** the recipe-seeded manifest and a `pending_review` human-seen entry are persisted, and a gate-action record is written
- **AND** the generated cross-reference index is not modified

#### Scenario: The engine would refuse
- **WHEN** the plan carries a reasonless override, a duplicate set name, a submission lacking its evidence contract, or fails validation
- **THEN** the route MUST refuse with the engine's reason and persist nothing, leaving prior state intact

#### Scenario: The gate capability is off
- **WHEN** the lens renders on a surface without the gate capability
- **THEN** the plan panel MUST render the plan-only confirmation with no execute affordance

#### Scenario: An agent invokes a lens verb
- **WHEN** any agent or automated path calls either verb
- **THEN** the call MUST be rejected and reported, like every gate action

### Requirement: Register-edit fulfilment lane
The dashboard runtime SHALL provide a fulfilment lane for dispatched `project-register-edit` commissions that applies each recorded edit to the aggregation-owned project register, validates the result against the pinned schema BEFORE writing, stamps the descriptor `delivered` with when and by what, and then commits only the register file and pushes — refusing and reporting (descriptor left `dispatched`) whenever the live register can no longer satisfy the commission or the write cannot land. The lane SHALL be runnable once, as a watching job, and from a loopback-only human-gated serve route behind a header affordance that appears whenever pending commissions exist; only recorded commissions are ever applied.

#### Scenario: A pending commission is applied
- WHEN the lane runs with a dispatched create-project or edit-project descriptor whose edit the live register can satisfy
- THEN the register file gains exactly that edit, the pinned validator passes before the write, the descriptor flips to `delivered` with `delivered_at` and `delivered_by`, and the register commit carries only the register file

#### Scenario: A stale commission refuses and reports
- WHEN a descriptor's edit can no longer be satisfied (the project vanished, a member conflict arose) or validation fails
- THEN the register is unchanged, the descriptor stays `dispatched`, and the run's report names the commission and its reason

#### Scenario: The button applies on demand
- WHEN a human clicks the apply affordance on the loopback gate console
- THEN the serve runs the same lane code once and reports what was applied and what was skipped
- AND the affordance is absent off the gate capability and when nothing is pending

#### Scenario: The watcher fulfils unattended
- WHEN the lane runs in watch mode beside a serve
- THEN each polling tick fulfils whatever commissions have been recorded since the last, with the same validation and refusal semantics

### Requirement: Project creation is a recorded commission
The dashboard SHALL offer a `create-project` verb on the human gate console that records a `workflow-job` descriptor (workflow `project-register-edit`, carrying the proposed project id, display name, and member repository ids) plus a `create-project` gate-action record naming the human — and SHALL NOT write the project register itself: the register is aggregation-owned, and the fulfilment of the recorded commission is what applies the edit.

#### Scenario: A human creates a project
- WHEN a human on the loopback gate console commissions a project with a name and member repositories drawn from the selector roster
- THEN a `workflow-job` descriptor and a `create-project` gate-action record are written under the served checkout's records tree
- AND `project-register.yaml` is not modified by the dashboard

#### Scenario: A member repository is not in the roster
- WHEN a commissioned member repository id is absent from the snapshot-index roster
- THEN the commission is refused with the unknown id as the reason and nothing is persisted

#### Scenario: A repository joins a second project
- WHEN a commissioned member repository already belongs to a project in the register projection
- THEN the commission is accepted — repository membership is multi-parent, and a project is a named view over repositories, not an owner

#### Scenario: A duplicate commission is refused
- WHEN a project id already carries a dispatched, undelivered `project-register-edit` commission
- THEN a second `create-project` commission for that id is refused and the refusal names the blocking descriptor

#### Scenario: A commissioned project is visible as pending
- WHEN a `create-project` commission is dispatched and not yet delivered
- THEN the register projection reports it on a `pending` plane distinct from the register's projects, and the picker renders it as a clearly-marked, non-selectable pending entry
- AND the pending entry never scopes the roster and disappears in favour of the register's own entry once the fulfilment lands

### Requirement: Project-scoped repository selection
The repository selector SHALL offer a project picker listing the register's projects, and selecting a project SHALL narrow the selector roster to that project's member repositories while the active snapshot remains a single `(repository, ref)` key.

#### Scenario: A project scopes the roster
- WHEN a human selects a project in the picker
- THEN the repository selector lists only that project's member repositories
- AND choosing one serves that single repository's snapshot exactly as an unscoped selection would

#### Scenario: Unregistered repositories keep their standing
- WHEN a repository is absent from the project register
- THEN it renders ungrouped exactly as the register contract already specifies, and clearing the project selection restores the full roster

### Requirement: Local register authority is declared against the tenant catalog
The project register consumed by this capability SHALL be authoritative for the development plane only until a tenant project catalog exists; once a runtime catalog is authoritative for project-to-repository composition, the local register SHALL be treated as a derived, replaceable workstation cache and SHALL NOT override the catalog.

#### Scenario: The runtime twin lands
- WHEN a tenant project catalog becomes authoritative for project composition
- THEN the dashboard's register is consumed as a derived projection of it
- AND a local edit is not an override of the catalog

### Requirement: The openDox project-first header
The dashboard header SHALL brand as "Opensoft openDox" and SHALL organize repository navigation around the CURRENT PROJECT: a project dropdown whose first line is "New Project" (opening the create-project commission form) followed by the register's projects, defaulting to the viewer's last-used project when the register projection still names it and to the first register project otherwise — the viewer is always in a project. Repository selection SHALL be a filter scoped to the current project: a popover listing the project's member repositories where selecting one makes it the active served repository, with an "All repositories" line that is disabled (naming the merged view as pending) until the project merged view exists and thereafter selects the project's derived aggregate.

#### Scenario: The header renders project-first
- WHEN the dashboard loads with a register projection available
- THEN the brand reads "Opensoft openDox", the project dropdown shows "New Project" first and the register's projects after it
- AND the current project is the stored last-used project, else the first register project

#### Scenario: The filter switches the served repository
- WHEN a human selects a member repository in the current project's filter popover
- THEN that repository becomes the active served snapshot exactly as the repository selector contract already specifies

#### Scenario: All-repositories awaits the merged view
- WHEN the project merged view is not yet available
- THEN the filter's "All repositories" line renders disabled and names the merged view as pending
- AND once the merged view exists the line selects the project's derived aggregate

#### Scenario: The header degrades without a projection
- WHEN no register projection is served (a static image or no reachable register)
- THEN the project dropdown and filter do not render and the dashboard degrades exactly as the selector contract already specifies

### Requirement: Project membership editing is a recorded commission
The dashboard SHALL offer an `edit-project` verb on the human gate console — the filter popover working like the project dropdown (D16): its first line adds a repository to the current project from the known-repository candidates, each member row carries a visibility indicator on its left and a two-click removal control on its right — that records a `project-register-edit` workflow-job descriptor carrying the added and removed member lists plus an `edit-project` gate-action record, and SHALL NOT write the register itself. The commission SHALL be refused when the project does not exist in the register projection, when an addition is outside the roster-or-register repository universe, when a removal is not currently a member, or while the project carries an undelivered edit commission — removing the last member is legal, because a project MAY be empty (created first, populated later); pending membership changes SHALL render as clearly-marked overlay until the fulfilment lands the register edit.

#### Scenario: A repository is added and another removed
- WHEN a human commissions an addition from the filter's add line or a removal from a member row's armed removal control
- THEN one `edit-project` descriptor records the diff and one gate-action record names the human
- AND the register is unchanged until the commission's fulfilment applies the edit

#### Scenario: An empty project is legal
- WHEN a project is created with no member repositories, or an edit removes its last member
- THEN the commission is accepted — the project exists awaiting its next additions, and the register schema admits the empty set

#### Scenario: Pending membership renders as overlay
- WHEN an edit-project commission is dispatched and undelivered
- THEN the affected repositories badge as pending in the popover and the register projection's truth plane is unchanged

### Requirement: Project merged view
Selecting a project's all-repositories view SHALL render one composed snapshot spanning the project's member repositories, produced by the existing aggregate composition (per-repo namespaced ids, per-item repository badges, `composed_from` freshness) from an aggregate DERIVED from the project register — one aggregate per register project, members being the project's repositories the serving plane can resolve — with hand-declared aggregates continuing to work and winning any id collision.

#### Scenario: A project offers its all-repos view
- WHEN a project is scoped in the selector
- THEN the roster offers "all repositories in <project>" backed by the project's derived aggregate
- AND selecting it renders the composed snapshot through the existing views

#### Scenario: A commissioned project gains its merged view on fulfilment
- WHEN a create-project commission's fulfilment lands the register edit
- THEN the project's derived aggregate exists on the next index composition with no further authoring

#### Scenario: A member snapshot is unavailable
- WHEN a member repository's snapshot cannot be loaded
- THEN the composed view renders the remaining members and names the missing one, degrading and never refusing

### Requirement: Merged-view cluster union
The wheel and canvas SHALL render a composed snapshot's same-topic clusters as one merged tile whose membership lists each repository's contribution, grouping by the namespaced id's topic tail — while the composition itself SHALL keep its ratified per-repo namespacing, so edges stay uncorrupted and non-composed consumers are unaffected.

#### Scenario: The same topic exists in two member repositories
- WHEN two member repositories carry clusters for the same topic
- THEN the merged wheel renders ONE tile for that topic listing both repositories' contributions
- AND drilling in distinguishes each repository's cluster

#### Scenario: A single-repository snapshot renders unchanged
- WHEN the rendered snapshot is not composed
- THEN clusters render exactly as today through the same view path

### Requirement: Composed views are read-only with a repository jump
On a composed snapshot every gate-bearing affordance SHALL hide — a gate verb binds to one served checkout, and a composed view has none — and the expanded tile SHALL offer one navigation verb, "open in <repo>", which switches the active snapshot to that tile's member repository, where every verb works as on any single-repository view. Per-tile repository binding remains a successor change.

#### Scenario: Gate verbs hide on a composed view
- WHEN the rendered snapshot carries `generation.composed_from`
- THEN no gate-bearing affordance renders anywhere in the view

#### Scenario: A tile jumps to its repository
- WHEN a human invokes "open in <repo>" on a composed tile
- THEN the active snapshot switches to that tile's `(repository, ref)` and the page reloads with every verb available as today

