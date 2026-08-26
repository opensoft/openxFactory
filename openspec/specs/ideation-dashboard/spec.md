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
The gate console SHALL offer a human-only `propose` action on a staging topic that commissions proposal authoring as a recorded dispatch — a `workflow-job` descriptor naming the proposal-authoring workflow and targeting the topic's staging id, plus a gate-action record — without authoring anything itself; the commissioned authoring runs externally and lands as an ordinary OpenSpec change subject to the existing review and ratify gates. The console SHALL refuse a topic absent from the pinned checkout's staging area and SHALL refuse a duplicate commission while a dispatched `propose` job for the same topic remains undelivered. The console SHALL ALSO refuse `propose` while the topic's tile carries an UNRESOLVED branch session, and the refusal MUST name the session and the two resolutions available — merge its pull request, or abandon the session to discard it. Proposal is the end of the staging pipeline: commissioning it from a tile whose drafts are still scattered across an unmerged branch would propose from a state no reviewer can see, so the human SHALL clear the session first. A session is UNRESOLVED while its snapshot registry entry is live; a merged session and an abandoned session are both resolved, and a branch surviving an abandon MUST NOT block propose, because the abandon already recorded the human's decision to discard.

An abandoned branch SHALL remain reviewable evidence until a human invokes cleanup with a durable RETENTION-RELEASE basis. The console SHALL accept an exact-tile active proposal, an archived change carrying that exact staged origin, or an executed demotion returning the proposal to that exact tile as machine-resolved preservation evidence. A demotion plan, proposal dispatch, missing change, missing worktree, missing tile, or non-live session state MUST NOT itself release retention. Demotion execution SHALL be proved by a durable execution receipt for new demotions; a pre-receipt demotion MAY be accepted only when the exact transition manifest and an exact returned-topic artifact jointly prove execution.

Where no machine-resolved preservation evidence exists, cleanup MAY proceed only through an explicit human retention release carrying a nonblank reason. This lane SHALL support staged-topic, cluster, possible, missing, renamed, and otherwise orphaned tile identities without inferring that absence is disposition. Every successful cleanup SHALL remain human-invoked, local-only, and non-automatic; SHALL verify the branch belongs to the supplied tile, the session is not live, no worktree is attached, and a durable `abandon-session` proof names the ref; and SHALL write a main-resident cleanup record naming the exact tile scope, pre-delete head, abandonment proof, retention-release evidence, and reason where explicitly supplied. A failed deletion MUST NOT leave a record claiming success.

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

#### Scenario: An active proposal preserves the abandoned exploration
- **WHEN** cleanup is invoked for an abandoned branch and an active change resolves to the exact staged-topic origin
- **THEN** the branch MAY be deleted after every ownership, liveness, worktree, and abandonment-proof check passes
- **AND** the cleanup record MUST name that active change as its retention-release evidence

#### Scenario: An archived proposal preserves the abandoned exploration
- **WHEN** cleanup is invoked for an abandoned branch and an archived change's own staged-origin metadata resolves to the exact topic
- **THEN** the archived change MUST release retention even though it is not a live proposal and no current pick edge survives
- **AND** the cleanup record MUST name the archived change and its origin evidence

#### Scenario: Historical evidence predates the abandonment
- **WHEN** matching active, archived, or demotion evidence was recorded before the session was abandoned
- **THEN** that historical evidence MUST NOT release retention for the newer abandoned work
- **AND** cleanup MUST require a fresh machine disposition or explicit human retention release

#### Scenario: The abandoned branch moved after abandonment
- **WHEN** the branch no longer points at the exact head recorded by `abandon-session`
- **THEN** machine-resolved retention evidence MUST NOT authorize deletion
- **AND** cleanup MUST preserve the moved ref until a new explicit human retention release names the current head

#### Scenario: An executed demotion preserves the abandoned exploration
- **WHEN** cleanup is invoked for an abandoned branch and a demotion execution receipt proves that the proposal returned to the exact staged topic
- **THEN** the executed demotion MUST release retention
- **AND** the cleanup record MUST name the demotion evidence and returned destination

#### Scenario: A legacy demotion is corroborated by returned artifacts
- **WHEN** a pre-receipt demotion has an exact transition manifest and an exact returned-topic artifact naming the same change and destination
- **THEN** their joint evidence MAY release retention
- **AND** neither artifact alone MUST be treated as execution proof

#### Scenario: A demotion was planned but not executed
- **WHEN** a transition manifest and plan exist but no execution receipt or exact returned-topic artifact proves execution
- **THEN** cleanup MUST NOT infer that the proposal was demoted
- **AND** the machine-evidence lane MUST refuse without deleting the branch

#### Scenario: Demotion execution is incomplete
- **WHEN** any planned source artifact is missing, any move is skipped, the source change remains, or a returned artifact does not occupy its exact planned destination
- **THEN** demotion MUST NOT emit an `executed` receipt
- **AND** cleanup MUST NOT treat the partial result as retention-release evidence

#### Scenario: The current tile is absent but exact disposition survives
- **WHEN** the supplied tile is absent from the current inventory but branch-family ownership, abandonment proof, and accepted retention-release evidence all resolve to its exact identity
- **THEN** current tile absence MUST NOT block cleanup
- **AND** absence MUST contribute no positive disposition evidence of its own

#### Scenario: A true orphan is explicitly released by a human
- **WHEN** no machine-resolved preservation evidence exists and a human invokes cleanup with a nonblank retention-release reason
- **THEN** cleanup MAY delete the abandoned local branch after all non-disposition preconditions pass
- **AND** it MUST first record the exact scope, pre-delete head, reason, and prior abandonment proof in the main-resident cleanup record

#### Scenario: A non-staged tile has no proposal lifecycle
- **WHEN** an abandoned cluster or possible branch is cleaned
- **THEN** it MUST use the explicit human retention-release lane rather than being permanently blocked on a proposal state that tile kind can never carry

#### Scenario: An orphan has neither disposition nor explicit release
- **WHEN** no accepted preservation evidence exists and no nonblank human retention-release reason is supplied
- **THEN** cleanup MUST refuse and delete nothing
- **AND** missing files, missing tiles, missing worktrees, and absent changes MUST NOT weaken that refusal

#### Scenario: Retention evidence names another tile
- **WHEN** active, archived, demoted, or operator-supplied evidence resolves to a different tile identity than the branch's supplied owner
- **THEN** cleanup MUST refuse with the mismatch and persist nothing

#### Scenario: Origin metadata is non-staged or malformed
- **WHEN** a change declares an ad-hoc, unsupported, or malformed origin
- **THEN** cleanup MUST NOT reinterpret that change through the possibles-pick compatibility fallback
- **AND** ambiguity unrelated to the requested tile MUST NOT globally block exact evidence for the requested tile

#### Scenario: Cleanup is attempted on live or unattested work
- **WHEN** the session is live, a worktree remains attached, the branch is outside the tile's branch family, or no durable `abandon-session` proof names the ref
- **THEN** cleanup MUST refuse regardless of proposal or retention-release evidence

#### Scenario: Branch deletion fails after the cleanup record is prepared
- **WHEN** local branch deletion fails after the cleanup action prepared its main-resident record
- **THEN** the record MUST be unwound so no durable artifact claims a deletion that did not occur
- **AND** the branch and prior abandonment evidence MUST remain available for retry

#### Scenario: Concurrent cleanup attempts share a tile and timestamp
- **WHEN** cleanup attempts target different refs for the same tile during the same second, or two attempts race for the same ref
- **THEN** their records MUST NOT overwrite or unlink one another
- **AND** only a record whose exact ref deletion completed MAY enter completed state

#### Scenario: The branch changes during cleanup
- **WHEN** the ref advances after its head is inspected but before deletion
- **THEN** the expected-value deletion MUST fail atomically and preserve the advanced ref
- **AND** no cleanup record may claim that the advanced ref was deleted

#### Scenario: Cleanup services address different repositories
- **WHEN** the human gate output root and the Git service root do not resolve to the same checkout
- **THEN** cleanup MUST refuse before writing a record or touching a branch

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
The staging workbench's `lens` panel SHALL render the match-count bullseye — the same rings-by-match-count, sectored-by-matched-subset, dotted geometry the keyword lens renders (rings index how many checked keywords a document matches, innermost = all) — at TILE SCOPE, from the SAME scoped keyword-lens derivation the panel already performs. The bullseye MUST introduce no new analysis, no new score, and no new snapshot field: it renders the geometry the scoped derivation already returns, and each rail row's declared count stays the snapshot's corpus-wide number verbatim, labelled as such. The keyword rail, the bullseye, and the flat matrix SHALL each be a NAMED, ALWAYS-REACHABLE SECTION of ONE tablist on that panel, and no section SHALL be reachable only by dismissing another; that tablist SHALL carry full APG semantics — roving tabindex, arrow keys, Home and End — and the ordering relation the earlier `above` wording expressed SHALL be discharged by the tablist's declared section order rather than by simultaneous rendering. The flat matrix SHALL remain a first-class always-reachable section and MUST NOT be demoted to an opt-in alternate of the bullseye. This supersedes the earlier simultaneity clause, which the shipped three-subtab restructure contradicted: what that clause protected was ACCESS to the matrix, and a named section of a keyboard-driven tablist protects access without spending a third of the panel on a second drawing. There SHALL be exactly ONE bullseye renderer serving both the keyword-lens view and the workbench panel, so the two surfaces cannot drift. The human's checked-keyword selection SHALL persist across tab switches within one workbench session, and SHALL reset to the scope's seed when a different scope is opened or the workbench is closed.

#### Scenario: The workbench lens panel renders the bullseye
- **WHEN** a human opens the workbench's `lens` tab on any topic-bearing tile
- **THEN** the match-count bullseye MUST be a named, always-reachable section of that panel's tablist, rendered at that tile's scope
- **AND** the flat matrix MUST be an equally named, always-reachable section of the same tablist
- **AND** neither MUST be reachable only by toggling the other off

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

#### Scenario: The lens sections are driven from the keyboard
- **WHEN** a human moves through the lens panel's section tablist with arrow keys, Home, and End
- **THEN** every section MUST be reachable without a pointer
- **AND** exactly one tab MUST be in the tab order at a time

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
The dashboard SHALL provide doxBench as the named evolution of the staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — with three coordinated regions over that scope. A context region SHALL retain `docs` and `lens`: `docs` SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them; `lens` SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `docs` context's expanded tile SHALL offer this capability's three document verbs — read, load-for-editing, and save — as specified by their own requirement. An authoring canvas SHALL present exactly ONE buffer at a time — the SELECTED buffer of the loaded set — and the SELECTION SHALL be made outside the canvas rather than by the canvas: the context region's `outline` selection tab SHALL select the `outline` buffer, loading a document SHALL select that document, and the chat rail's loaded-document selector SHALL select among the loaded documents. The `outline` buffer SHALL load the topic's declared outline material when one exists — for a staged topic, the fragment's outline material — and a document buffer SHALL load the exact document the human loaded; the canvas SHALL provide browser-local editing plus live rendered Markdown preview of the SELECTED buffer on the local human console, presented as this capability's Editor/Preview view-tab pair rather than as a side-by-side split pane, while an absent outline remains an explicit empty/create state rather than fabricated content. The canvas MUST NOT render a second buffer-selection tablist beside the selection surfaces the context region and the chat rail own, because two controls answering one question is how the two come to disagree. A chat region SHALL contain Working subject, the loaded-document selector, transcript, server-declared model selection, and composer, and SHALL ground turns on the current canvas buffers and this capability's bounded context packet as specified by this capability. doxBench's corpus write authority SHALL remain the human-only gate verbs `create-document`, `edit-document`, `open-pr`, session share, and session abandon: buffer edits, chat turns, thread writes, and AI Apply MUST write no corpus document, register entry, workbench manifest, snapshot, or gate artifact; Save MAY materialize/join a branch session and invoke only create/edit as specified; no verb MAY delete a document; and no session write may touch the served checkout. With the gate/model capabilities absent or on the hosted plane, the context SHALL remain usable and doxBench SHALL render read-only outline/document content without reachable editing, chat, threads, or write controls. The `docs` context SHALL present its document set as a VERTICAL SPLIT: a per-document ABSTRACT REGION above, and a single-reel DOCUMENT WHEEL below that places this scope's documents — every separately labelled section of them flattened into one ordered reel — in the surface's own drum projection with its own established click and spin gestures. Selecting a wheel tile SHALL make that document the abstract region's SUBJECT, and the abstract region SHALL RE-PRESENT ONLY what the snapshot already carries for that document — its own `Summary:` header, its declared topics, its stage and kind, its declared destinations, and its completeness score beside the five named signals — and MUST NOT compute, adjust, or re-weight any of it, exactly as the docs rows are already held to. The `lens` context SHALL present its three sections as named, always-reachable sections of one tablist as that panel's own requirement specifies. Neither presentation SHALL introduce a new score or a new snapshot field. The no-new-ANALYSIS clause in this requirement, and in the workbench bullseye requirement it restates, SHALL be read as governing THE BULLSEYE'S OWN GEOMETRY and the completeness signals — the derivations those clauses were written about — and SHALL NOT be read as forbidding a separately captioned, explicitly non-authoritative MODEL-DERIVED artifact that this capability's own requirements govern, feeds no score, no aggregate, no readiness tier and no gate, and never replaces or adjusts anything the snapshot carries. A model-derived artifact admitted this way SHALL be presented BESIDE the snapshot-derived material and never merged into it, so a reader can always tell which claim is the document's own and which a model made.

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
- **AND** the `outline` buffer MUST load that fragment's outline material from the active repository/ref

#### Scenario: A document is loaded for editing
- **WHEN** a human uses the load verb on a `docs` tile
- **THEN** the canvas MUST load that exact document as a buffer of the loaded set and select it
- **AND** docs/lens context, every other loaded buffer, and chat state MUST remain available

#### Scenario: The outline selection tab becomes the working context
- **WHEN** a human focuses the context region's `outline` selection tab
- **THEN** the `outline` buffer MUST become the selected buffer and the canvas MUST show that buffer's working content, including unsaved edits
- **AND** the context region's own outline pane MUST keep rendering the material as it stands in the source, so "what is stored" and "what I have unsaved" remain separately readable

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
- **THEN** the canvas MUST render an explicit empty state for the `outline` buffer rather than fabricating or drafting one
- **AND** only a capable local human console MAY offer a create-backed outline buffer

#### Scenario: A human edits before a session exists
- **WHEN** a capable local human edits any buffer with no active branch session
- **THEN** the edit MUST remain browser-local and available to the next chat turn
- **AND** the served checkout and every shared surface MUST remain unchanged

#### Scenario: An existing document is saved
- **WHEN** a human saves an existing eligible buffer from doxBench
- **THEN** `edit-document` MUST persist it on the tile's branch session as that action's single commit
- **AND** the served checkout MUST remain untouched

#### Scenario: doxBench renders without gate or model capability
- **WHEN** doxBench runs on a surface where gate and model capabilities are absent
- **THEN** docs/lens and available source content MUST remain readable
- **AND** no editing, chat, Apply, Save, Cancel, load, share, or other write-implying control MUST be reachable

#### Scenario: doxBench is used on a narrow viewport
- **WHEN** the three desktop regions cannot remain usable side by side
- **THEN** the same context, authoring canvas, and chat regions MUST stack without losing state, labels, keyboard reachability, or focus order

#### Scenario: The docs context presents its documents as a split
- **WHEN** a human opens doxBench's `docs` context on any topic-bearing tile
- **THEN** the pane MUST render a per-document abstract region above and a single-reel document wheel below
- **AND** selecting a wheel tile MUST make that document the abstract region's subject

#### Scenario: The abstract region re-presents and never recomputes
- **WHEN** the abstract region renders a document the snapshot scores
- **THEN** its score and named signals MUST be the snapshot's `completeness` object verbatim
- **AND** doxBench MUST NOT compute, adjust, or re-weight any signal

#### Scenario: The lens context is presented in three sections
- **WHEN** a human opens the `lens` context on a topic-bearing tile
- **THEN** the keyword rail, the bullseye, and the flat matrix MUST each be a named, always-reachable section of one tablist

#### Scenario: A model-derived artifact is admitted beside the snapshot's own
- **WHEN** the docs context renders a model-derived abstract for a document
- **THEN** it MUST be presented beside the snapshot-derived material with its own caption, never merged into it
- **AND** it MUST feed no completeness score, no staged-topic aggregate, no readiness tier, and no gate

#### Scenario: The no-new-analysis clause is read against the bullseye
- **WHEN** the no-new-analysis clause is applied to a derivation
- **THEN** it MUST govern the bullseye's geometry and the completeness signals
- **AND** it MUST NOT be read as forbidding an artifact this capability's own requirements govern

### Requirement: doxBench surface identity
The dashboard SHALL name the integrated staging-workbench authoring surface **doxBench**, using that exact casing wherever the surface names itself — visible product copy, navigation, heading text where a heading exists, ACCESSIBLE NAMES, documentation, tests, and realization evidence. A region whose accessible name already carries the product name SHALL NOT be required to restate it as visible heading text: an accessible `region` is announced by its name on entry, so a heading duplicating that name adds nothing an assistive technology did not already receive while costing visible space, and a surface MAY therefore carry its name in the accessible name alone. Where a surface renders a heading at all, that heading MUST use the exact casing. doxBench SHALL remain the named human-facing evolution of the existing `ideation-dashboard` staging workbench rather than a second capability. Existing technical identifiers — including `workbench-*` schemas, routes, module names, the `workbench-chat-turn` kind, `WorkbenchModelPort`, branch-session records, and persisted dashboard artifacts — MUST remain compatible and MUST NOT be renamed or rewritten solely to adopt the doxBench name.

#### Scenario: The integrated authoring surface is presented
- **WHEN** the dashboard exposes the integrated authoring surface
- **THEN** its accessible surface name MUST use the exact name `doxBench`, and any heading it does render MUST use that exact name too
- **AND** generic controls MAY retain descriptive workbench terminology where that terminology names an inherited technical concept

#### Scenario: A named region would restate its own name visibly
- **WHEN** a doxBench region already carries the product name as its accessible name
- **THEN** a visible heading repeating that same name MUST NOT be required, because it is announced twice and occupies space the surface needs for material
- **AND** the accessible name MUST NOT be dropped in exchange — removing the heading is only permitted while the region stays named

#### Scenario: Existing workbench artifacts are loaded
- **WHEN** doxBench consumes a pre-name snapshot, branch-session record, route, schema, or other `workbench-*` artifact
- **THEN** that artifact MUST remain valid and usable without migration
- **AND** no persisted identifier or artifact kind MUST be rewritten merely to carry the doxBench name

### Requirement: doxBench editor buffer contract
The local doxBench surface SHALL maintain a KEYED BUFFER SET for its canvas — the permanently reserved `outline` key plus one key per LOADED document — and each buffer SHALL carry its kind, repository-relative path or `null` for a not-yet-created artifact, repository, base ref, base source revision, base content hash, current content hash, current text, and dirty state. A document buffer's key SHALL be its repository-relative path, so a document can be loaded at most once and no two buffers can claim the same file; at most ONE unbacked document buffer MAY exist, under the reserved key `document`, which is the not-yet-created artifact of the existing create flow and SHALL be re-keyed to its path when its first Save gives it one. The outline buffer SHALL be seeded from the opened scope's declared outline material when one exists and MUST NOT be fabricated from any document's headings; a document buffer SHALL be seeded from the document the human loaded or from the existing create-document flow. Editing any buffer MUST be a browser-local, reversible action that writes no corpus document, snapshot, register, workbench manifest, gate artifact, or branch until the human invokes Save. Save SHALL compare current and base hashes, persist a new path through `create-document` and an existing path through `edit-document`, preserve each verb's existing validation and authority boundary, and refresh/rebase each successfully saved buffer from the resulting session ref and source revision. Save ordering SHALL be an explicit rule rather than a fixed list: the `outline` buffer SHALL be persisted FIRST when it is dirty, because its commit establishes the session ancestry the document commits descend from; every dirty document buffer SHALL then be persisted in a DETERMINISTIC order the realization declares, each through its own existing gate action as one commit; and a dirty outline that did not land SHALL stop every document with a stated `not_attempted` verdict. One document's refusal SHALL NOT stop another document, because documents carry no ancestry dependency on each other and reporting one refusal as the cause of untried work is a false statement about both. Save MUST NOT invent a multi-document write verb, rewrite history, or hide partial success, and every buffer it acted on SHALL report its own verdict. Discard SHALL restore the last loaded/saved base content of the buffer it names and MUST persist nothing. A document that is the `docs` context's ABSTRACT SUBJECT SHALL NOT thereby become a buffer: the abstract subject is a READING selection over the scope's documents, independent of the keyed buffer set, so making a document the abstract's subject MUST NOT load it, key it, seed it, mark it dirty, or place it in the loaded set. Only the load-for-editing verb creates a document buffer.

#### Scenario: A human edits the outline before chatting
- **WHEN** a human changes the outline buffer without invoking Save
- **THEN** the canvas MUST show the outline as dirty
- **AND** no corpus file, branch, snapshot, register, manifest, or gate record MUST change

#### Scenario: A second document is loaded
- **WHEN** a human loads a second document while the first is still loaded and dirty
- **THEN** both document buffers MUST exist under their own path keys with their own dirty state and their own base identity
- **AND** loading the second MUST NOT replace, discard, or flush the first

#### Scenario: A document already loaded is loaded again
- **WHEN** a human invokes the load verb on a document the loaded set already holds
- **THEN** that existing buffer MUST become the selected one and MUST NOT be reloaded from source, because reloading would silently discard its unsaved text

#### Scenario: A scope has no outline
- **WHEN** the opened scope declares no outline material
- **THEN** the outline buffer MUST show an explicit empty state
- **AND** it MAY offer a new outline buffer whose first persistence uses `create-document`, but it MUST NOT fabricate or persist an outline merely by being opened

#### Scenario: Several dirty documents are saved
- **WHEN** the human invokes Save with a dirty outline and three dirty documents
- **THEN** the outline action MUST run first and each changed document MUST then produce its own existing gate-action commit in the declared deterministic order
- **AND** no combined or hidden write verb MUST be introduced

#### Scenario: One document's save refuses
- **WHEN** the outline commits, the first document commits, and the second document's save refuses
- **THEN** the third document MUST still be attempted, because it descends from the same ancestry and the refusal was not about it
- **AND** the report MUST name the committed, refused, and remaining buffers separately

#### Scenario: The outline's save refuses
- **WHEN** the outline is dirty and its save refuses
- **THEN** every dirty document MUST be reported `not_attempted` with the missing-ancestry reason and MUST NOT be sent
- **AND** every buffer's text, base, and dirty state MUST be preserved exactly

#### Scenario: An unbacked document buffer is first saved
- **WHEN** the reserved unbacked document buffer is persisted through `create-document` and the server reports the path it created
- **THEN** that buffer MUST be re-keyed from the reserved key to its path
- **AND** the reserved key MUST become available for a later create without carrying anything from the buffer that left it

#### Scenario: A human discards local edits
- **WHEN** the human invokes Discard on a dirty buffer
- **THEN** that buffer MUST return to its last loaded or saved base content and no other buffer MUST change
- **AND** no gate action or provider call MUST occur

#### Scenario: A document is pointed at but not loaded
- **WHEN** a human makes a document the docs context's abstract subject without invoking load-for-editing
- **THEN** no buffer MUST be created or keyed for that document
- **AND** the keyed buffer set MUST be unchanged

### Requirement: Grounded doxBench chat turn
The local human-console doxBench surface SHALL offer a chat rail containing a `Working subject` field, the loaded-document selector, transcript, server-declared model selection, and message composer. Each submitted turn SHALL use a versioned `workbench-chat-turn` request containing the repository/ref and tile scope, the BOUND BUFFER's key, `working_subject`, the new user message, the bounded prior transcript, the selected model id, a client-generated turn id, and the complete current descriptors and text of the outline buffer and of every loaded document buffer including their hashes. The server MUST independently resolve and confine the repository/ref, the tile, and every supplied buffer path before a provider call; MUST verify every declared content hash; MUST refuse a request whose bound-buffer key names no supplied buffer; and MUST record in the response the exact per-buffer hashes, the bound buffer's key, the model id, and the turn id used. The turn RECORD SHALL name the buffer the turn was bound to, so a transcript read later says which material the conversation was working on — Phase A deferred this because the released envelope had no room for it, and this capability's contract release discharges that obligation rather than substituting a server-side-only field no reader can consult. The response SHALL echo the model that answered together with the selected-model metadata the contract release carries, so a transcript states which model produced which turn rather than leaving it to be inferred. Unsaved buffer text SHALL be eligible turn input and MUST be labelled as working state rather than governed or committed content. Per-turn context SHALL be assembled as this capability's bounded context packet and MUST NOT be assembled by concatenating whatever the browser happened to send. The next turn SHALL use the buffer contents and thread state that exist when that next turn is submitted, including intervening human edits and locally applied AI proposals, rather than reusing a previous turn's text. The request/response schemas SHALL impose explicit byte, buffer-count, transcript-turn, and output bounds; an over-bound turn MUST refuse with the applicable measured limit and MUST NOT silently truncate, summarize, or omit any buffer. Exactly one turn MAY be in flight per browser conversation key. Within one server process the client turn id SHALL be idempotent: a repeated completed id with identical input hashes SHALL return the recorded result without another provider dispatch, an in-flight repeat SHALL attach to or report that turn, and reuse with different content or hashes MUST refuse. A provider or response-validation failure MUST return a fixed redacted error, preserve every buffer, append no assistant proposal, and disclose no credential, raw provider response, prompt, document content, thread content, or unsaved text in logs or error details.

#### Scenario: A turn is bound to one of several loaded documents
- **WHEN** four documents are loaded and the human sends a message with the third selected
- **THEN** the request MUST name that buffer's key as the bound buffer and MUST carry the outline and all four documents with their hashes
- **AND** the completed turn's durable record MUST name that same bound buffer

#### Scenario: A turn names a bound buffer it did not supply
- **WHEN** a request's bound-buffer key names no buffer in its own buffer set
- **THEN** the route MUST refuse before any provider call, exactly as the existing active-path revalidation does

#### Scenario: A human edit feeds the next turn
- **WHEN** a human edits any loaded buffer after one assistant response and submits another message
- **THEN** the new request MUST carry that buffer's edited current text and hash
- **AND** the response MUST identify that hash as the content the model saw

#### Scenario: Unsaved edits are discussed
- **WHEN** a dirty buffer is included in a chat turn
- **THEN** the model MAY use that exact unsaved text
- **AND** neither the request nor the response MUST represent the text as committed, governed, or present on `main`

#### Scenario: The route receives a mismatched path or hash
- **WHEN** a turn names a path outside the opened tile's allowed scope, a repository/ref other than the active binding, or a hash that does not match the supplied text
- **THEN** the route MUST refuse before any provider call
- **AND** no browser conversation state or corpus state MUST be persisted by the server

#### Scenario: A turn exceeds a declared limit
- **WHEN** the combined buffers, transcript, assembled packet, message, or requested output exceed the selected catalog entry's or route's limit
- **THEN** the route MUST refuse and name the exceeded dimension and limit
- **AND** it MUST NOT silently truncate or send a partial document to the provider

#### Scenario: A turn completes
- **WHEN** the provider returns a valid response for the exact request
- **THEN** the chat rail MUST append assistant prose and any typed proposals under one turn id, into the SELECTED document's thread
- **AND** focus, the selected document, the active view tab, editor selection, scroll position, and every buffer's dirty state MUST remain usable

#### Scenario: A completed turn is retried
- **WHEN** the same client turn id is submitted again in the same server process with identical content and hashes
- **THEN** the recorded result MUST be returned without a second provider dispatch

#### Scenario: A turn id is reused for different content
- **WHEN** a client turn id is repeated with different buffer text, hashes, bound buffer, subject, message, or model
- **THEN** the server MUST refuse the idempotency conflict before any additional provider call

#### Scenario: A provider or response validation fails
- **WHEN** the provider call fails or its response violates the typed response schema
- **THEN** every editor buffer MUST remain byte-identical and no assistant proposal MUST be appended
- **AND** the UI MUST receive a fixed actionable failure while logs and response details reveal no credential, raw provider payload, prompt, document content, thread content, or unsaved text

### Requirement: doxBench model catalog and provider boundary
The dashboard backend SHALL expose a same-origin workbench model catalog whose entries carry a stable opaque model id, human label, provider class, input/output limits, availability, and a human-readable data-handling badge. The catalog MUST NOT expose a provider credential, raw secret, raw endpoint, secret environment-variable name, or provider request template, and the browser MUST NOT call any model provider directly. EVERY MODEL CONSUMER on this surface — a chat turn, and any further consumer such as a per-document derivation — SHALL accept only a model id present and available in the current catalog and SHALL resolve that id through a server-side injected model-provider port whose member surface SHALL remain exactly the three declared members — the adapter-declared timeout, the catalog, and the single opaque dispatch — so that per-turn model selection, harness session handling, and any adapter-internal routing are performed INSIDE an adapter and MUST NOT be added as a fourth provider verb. A catalog entry MAY name a ROUTING RULE this capability owns rather than a single provider model — an `auto` entry that maps a turn to a model by declared role — and such an entry SHALL declare itself as a routing rule with the data-handling badge of the models it may route to, because an entry that hid a routing decision behind a model-shaped id would report a handling posture it does not control. Provider credentials MUST come only from the deployment's approved server-side credential mechanism and MUST NOT enter browser storage, a request body, response body, dashboard snapshot, chat transcript, thread file, log, gate record, git artifact, or exception detail; an adapter that reaches a hosted provider SHALL obtain its credential through the ratified broker lane and MUST NOT hold or read a raw secret of its own. A hosted fallback MAY be offered only when the deployment explicitly enables it and its configured data-handling policy meets the catalog badge; otherwise the model MUST be unavailable. The model catalog and EVERY model-consuming route SHALL be offered only on a loopback human console with a real checkout, resolved actor, and demonstrated console presence; the hosted/read-only plane MUST offer NONE of them. A NEW model consumer SHALL reach the provider through this same seam and MUST NOT be added as a fourth provider verb, MUST NOT open a second provider path, and MUST NOT be smuggled through the chat-turn envelope: a consumer whose request is not a conversation SHALL carry its own request shape and its own declared purpose. The port MUST also be DECLARED AT AN ENTRYPOINT for any consumer to reach a provider at all; where no entrypoint declares one, every consumer's honest posture is an absent capability rather than an error. Where the declared adapter is STATEFUL — a supervised harness child holding per-thread sessions — the declaration SHALL resolve to ONE instance for the life of the served process, and the per-request accessor SHALL return that same instance rather than constructing a new one, because an adapter rebuilt per request cannot hold the one-session-per-document-thread correspondence this capability requires elsewhere and would restart a child on every call.

#### Scenario: The browser loads model choices
- **WHEN** local doxBench opens with one or more allowed providers configured
- **THEN** the selector MUST show exactly the available catalog entries and their data-handling badges
- **AND** no credential or raw provider endpoint MUST be present in the page or catalog response

#### Scenario: The menu offers a routing rule
- **WHEN** the catalog offers an `auto` entry that this capability resolves to a model by role
- **THEN** the entry MUST declare itself a routing rule and carry the handling badge of every model it may route to
- **AND** the resolved model MUST be recorded on the turn, so a transcript names the model that actually answered

#### Scenario: No model is configured
- **WHEN** the model catalog is empty
- **THEN** the chat rail MUST explain that no allowed model is configured
- **AND** every loaded editor MUST remain usable

#### Scenario: An unknown model id is submitted
- **WHEN** a chat request names a model id absent from or unavailable in the current catalog
- **THEN** the server MUST refuse before any provider call

#### Scenario: A fourth provider verb is proposed
- **WHEN** any realization would add a port member beyond the declared three to carry model switching, session handling, or harness control
- **THEN** it MUST be rejected — that behavior belongs inside an adapter, and a fourth member is a second provider verb by another name

#### Scenario: A browser attempts a direct provider call
- **WHEN** the dashboard bundle or runtime would contact a model endpoint other than the same-origin workbench routes
- **THEN** the renderer boundary MUST fail validation and the call MUST NOT ship

#### Scenario: Hosted doxBench is opened
- **WHEN** doxBench runs on the hosted plane
- **THEN** the model catalog and turn capabilities MUST be absent
- **AND** no chat or editor control implying unavailable authority MUST be reachable

#### Scenario: A second model consumer is added
- **WHEN** a capability adds a model consumer that is not a chat turn
- **THEN** it MUST resolve its model through the same server-side injected port under the same loopback-console gate
- **AND** the port's member surface MUST remain exactly the three declared members

#### Scenario: A non-conversation request is offered as a chat turn
- **WHEN** a model consumer whose request carries no human message, transcript, or buffer set would ride the chat-turn envelope
- **THEN** it MUST be rejected and MUST carry its own request shape and declared purpose

#### Scenario: No entrypoint declares a model port
- **WHEN** a served process is started by an entrypoint that declares no model-provider port
- **THEN** every model consumer MUST report an absent capability and MUST NOT fail as an error

#### Scenario: A stateful adapter is resolved twice in one process
- **WHEN** two requests in one served process each resolve the model port
- **THEN** both MUST receive the SAME adapter instance
- **AND** no adapter child process MUST be started a second time by the act of resolving

### Requirement: Typed AI proposals and stale-application protection
A workbench chat response MAY contain ordinary assistant prose and zero or more typed edit proposals, and each proposal SHALL name exactly one target BUFFER KEY drawn from the request's own supplied buffer set, carry complete proposed content, identify that buffer's input `base_hash`, and include a human-readable summary. A proposal naming a key the request did not supply MUST be refused as unroutable rather than guessed at, and two proposals MUST NOT name the same key in one response. The number of proposals in one response SHALL be bounded by the contract, and the bound SHALL be expressed over the request's buffer count rather than a fixed pair, so widening the loaded set does not silently widen what one response may rewrite beyond what it was grounded on. A provider response MUST NOT write, save, commit, create, delete, or apply any document by itself. The browser SHALL render Apply only for schema-valid typed proposals. Applying a proposal SHALL replace only the named browser buffer, mark it dirty, remain locally reversible, and MUST NOT invoke Save or any gate action. Immediately before Apply, the browser MUST recompute the target buffer hash and compare it with the proposal's `base_hash`; a mismatch MUST refuse as stale and offer inspection of current versus proposed content or a new turn, but MUST NOT silently merge or expose an authority-bypassing force-apply action. Chat prose without a typed proposal MUST NOT be inferred as replacement content.

#### Scenario: An AI proposes a revision to the selected document
- **WHEN** a valid response proposes content for the bound document's key against that buffer's current hash
- **THEN** the human MAY apply it to that buffer
- **AND** the buffer MUST become dirty while the corpus and branch remain unchanged until Save

#### Scenario: A proposal targets a buffer that was not sent
- **WHEN** a response names a buffer key absent from the request's buffer set
- **THEN** that proposal MUST be refused as unroutable and MUST NOT be rendered with an Apply control

#### Scenario: Two proposals name one buffer
- **WHEN** one response returns two proposals against the same buffer key
- **THEN** the response MUST be refused rather than applied in an arbitrary order

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
The dashboard header SHALL brand as "Opensoft openDox" and SHALL organize repository navigation around the CURRENT PROJECT: a project dropdown whose first line is "New Project" (opening the create-project commission form) followed by the register's projects, defaulting to the viewer's last-used project when the register projection still names it and to the first register project otherwise — the viewer is always in a project. Repository selection SHALL be a filter scoped to the current project: a popover listing the project's member repositories. Where the project can be composed, that popover SHALL be a VISIBILITY control — each member row's indicator ticks its repository into or out of the view, one toggle chooses union or shared over the visible set, `all` and `none` are offered as the two bulk moves, and the member name is the shortcut that makes that repository the only visible one — and the filter's own label SHALL state the visible count against the total. Where no member snapshot is published, and therefore nothing can be composed, the popover SHALL degrade to naming the merged view unavailable with the rows selecting one repository at a time.

#### Scenario: The header renders project-first
- WHEN the dashboard loads with a register projection available
- THEN the brand reads "Opensoft openDox", the project dropdown shows "New Project" first and the register's projects after it
- AND the current project is the stored last-used project, else the first register project

#### Scenario: The filter ticks repositories into the view
- WHEN a human toggles a member repository in the current project's filter popover
- THEN that repository enters or leaves the visible set, the view re-renders over the new set, and the filter label restates the visible count

#### Scenario: A member name selects that repository alone
- WHEN a human clicks a member repository's name in the filter popover
- THEN that repository becomes the only visible one and its own snapshot is served, exactly as the repository selector contract already specifies

#### Scenario: All-repositories awaits the merged view
- WHEN no member snapshot is published, so the project has no derived aggregate
- THEN the filter names the merged view as unavailable and the rows select one repository at a time

#### Scenario: The header degrades without a projection
- WHEN no register projection is served (a static image or no reachable register)
- THEN the project dropdown and filter do not render and the dashboard degrades exactly as the selector contract already specifies

### Requirement: Project membership editing is a recorded commission
The dashboard SHALL offer an `edit-project` verb on the human gate console — the filter popover's add line offering the known-repository candidates, and each member row a two-click removal control — that records a `project-register-edit` workflow-job descriptor carrying the added and removed member lists plus an `edit-project` gate-action record, and SHALL NOT write the register itself. Membership edits QUEUE: a project MAY carry several dispatched, undelivered edit commissions at once, each validated at commission time against the register with that project's pending commissions applied oldest-first — a dispatched create-project commission counting as the project existing, so a just-created project can be populated before its fulfilment lands — and same-second commissions MUST land as distinct descriptors. The commission SHALL be refused when the project exists neither in the register projection nor as a pending creation, when an addition is outside the roster-or-register repository universe, when an addition is already an effective member (register or pending), or when a removal is not an effective member. Removing the last member is legal, because a project MAY be empty (created first, populated later); pending membership changes SHALL render as clearly-marked overlay, netted across the queue, until the fulfilment lands the register edit.

#### Scenario: A repository is added and another removed
- WHEN a human commissions an addition from the filter's add line or a removal from a member row's armed removal control
- THEN one `edit-project` descriptor records the diff and one gate-action record names the human
- AND the register is unchanged until the commission's fulfilment applies the edit

#### Scenario: An empty project is legal
- WHEN a project is created with no member repositories, or an edit removes its last member
- THEN the commission is accepted — the project exists awaiting its next additions, and the register schema admits the empty set

#### Scenario: Successive edits queue instead of refusing
- WHEN a human commissions a second membership edit while the project's earlier edit commission is dispatched and undelivered
- THEN the second commission records as its own descriptor, validated against the register with the pending commissions applied oldest-first
- AND a duplicate addition against that pending-applied state is still refused
- AND the fulfilment delivers the queued commissions oldest-first

#### Scenario: Pending membership renders as overlay
- WHEN edit-project commissions are dispatched and undelivered
- THEN the affected repositories badge as pending in the popover, netted across the queue, and the register projection's truth plane is unchanged

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

### Requirement: The merged view spans the visible member set
The composed view SHALL render exactly the member repositories the human has made VISIBLE in the project's filter, under one of two set modes: UNION (every item belonging to a visible repository) or SHARED (only items whose identity — the composed id's tail, or the unnamespaced key a collection uses instead — is carried by TWO OR MORE of the visible repositories). The shared threshold is two rather than every visible repository, because convergence between any pair of a project's members is the finding, and requiring all of them keeps almost nothing on a real multi-member project; with two repositories visible the two readings coincide. Shared SHALL filter and never merge, so each repository's own copy stays a separately badged, separately openable row and two repositories' takes on one document can be read side by side. The narrowing SHALL be applied BEFORE the cluster union, so merged tallies count the visible contributions rather than the whole project, and `generation.composed_from` SHALL be trimmed to the visible members so the freshness header names the repositories actually rendered. Exactly one visible repository SHALL serve that repository's own snapshot with every capability it normally carries; any other count SHALL serve the project's composed, read-only aggregate, and an empty visible set SHALL render honestly empty rather than refusing. The visible set and mode are viewer state stored per project and resolved against current membership: a repository that leaves the project drops out of the stored set, a stored set that membership has outlived falls back to every member rather than rendering nothing, and nothing stored means every member under union — the composition's own answer.

#### Scenario: The union narrows to the ticked repositories
- WHEN a human hides a member repository in the project's filter
- THEN the composed view drops that repository's items, merged cluster tallies fall to the visible contributions, and the freshness header counts only the visible members

#### Scenario: The shared mode shows what two or more visible repositories carry
- WHEN the view mode is shared over two or more visible repositories
- THEN only items whose identity is carried by at least two visible repositories render, each repository's copy as its own badged row
- AND an identity only one of them carries does not render
- AND an identity two of three carry DOES render, because the threshold is two rather than all

#### Scenario: One visible repository is the interactive single view
- WHEN exactly one repository is visible
- THEN that repository's own snapshot is served with its full capabilities, exactly as selecting it directly always did

#### Scenario: The stored set survives a membership change
- WHEN a repository leaves the project after the human ticked a set
- THEN it drops out of the visible set, and a stored set that membership has outlived falls back to every member rather than rendering nothing

### Requirement: The lens serves a repository vocabulary
The lens SHALL offer a REPOSITORY vocabulary alongside its keyword vocabulary wherever the rendered snapshot is composed, presenting the project's member repositories as the rail, one dot per cross-repository document IDENTITY, and rings by CARRIER COUNT — how many visible repositories carry that identity, the centre being every one of them. The two vocabularies SHALL be served by the same derivation, geometry, and renderer: the repository plane is supplied by re-expressing the composed snapshot in the shape the lens already reads, so no vocabulary-specific engine exists. Where the snapshot is not composed the switch SHALL NOT render and the keyword lens SHALL behave exactly as before. The repository rail's ticks ARE the view's visible member set: the lens SHALL open on the current set, write changes back so the project filter and the lens never disagree, and redraw from the aggregate it already holds rather than reloading.

#### Scenario: The repository lens draws carrier rings
- WHEN a human switches the lens to the repository vocabulary on a composed view
- THEN the rail lists the member repositories with their identity counts, and each document identity is a dot on the ring for the number of visible repositories carrying it
- AND the centre holds the identities every visible repository carries

#### Scenario: A tick moves both controls
- WHEN a human unticks a repository in the lens rail
- THEN the visible set records that change and the project filter reflects it
- AND the lens redraws over the remaining set without reloading the shell

#### Scenario: A single-repository view offers no repository vocabulary
- WHEN the rendered snapshot is not composed
- THEN no vocabulary switch renders and the keyword lens is unchanged

### Requirement: Drill-in scopes the dashboard to a region's documents
Activating a region of the repository bullseye — its centre, or a sector naming an exact repository combination — SHALL scope the whole dashboard to the documents behind that region, and the activation SHALL be reachable both from the region itself and from a labelled control beside it, because a hit region alone is undiscoverable. The scope is a DOCUMENT SET: every other plane SHALL keep only what references it — a cluster with an edge into the set, a change or staged topic with a file path in it, a keyword a kept document still declares — and planes with no document relationship SHALL be left alone rather than silently emptied. A scope SHALL be stated on screen with the count of documents, the count of identities behind them, and the repository combination, and SHALL be clearable from that statement.

#### Scenario: A sector scopes the shell to its documents
- WHEN a human activates a sector naming a repository combination
- THEN every view renders only the documents whose identity is carried by exactly that combination, one document per carrying repository
- AND clusters, changes and staged topics narrow to those that reference the kept documents

#### Scenario: The scope states itself and clears
- WHEN a drill-in scope is active
- THEN the shell states the document count, the identity count, and the combination scoped to
- AND clearing it restores the full visible-set view

### Requirement: doxBench resolves its released contract from the checkout it runs in
The dashboard runtime SHALL resolve the pinned doxBench wire schemas from the repository it is running in whenever that repository is itself a publisher release, and MUST NOT reach a sibling checkout in preference to its own tree. Resolution precedence SHALL be, highest first: an explicitly supplied checkout; the `OPENXFACTORY_ROOT` operator override; the hosting repository when it carries the publisher markers; then the existing walk up to an aggregation-relative `openxFactory/`; and a refusal when none of those yields a checkout. Only the third rung is new, and no rung above or below it moves.

A serve MUST verify contracts against the tree it was launched from. The path this replaces searched one level below where it stood, so from inside the publisher it walked past itself every time and landed on the aggregation's submodule checkout — a shared tree that sessions move between branches — which meant a serve started from one worktree could verify its wire shapes against another session's working state. That this has so far been harmless is a property of two files not having changed, not a guarantee anything makes.

The runtime's pinned release SHALL name the release the repository currently publishes, and a repin MUST carry the digests that release's own manifest records. Where the schema bytes are unchanged across the releases spanned, the repin SHALL be digest-neutral: it re-declares which release is read and changes no verified byte, so no conformance question reopens.

The two model routes SHALL keep their current refusal shape and their current gate order. A route that cannot read the contract MUST still refuse before consulting any port, MUST still emit only the fixed catalog code, and MUST NOT let a pin diagnostic — which names checkout paths and digests — reach the wire. Recovery comes from the resolution beneath the routes succeeding, never from a route relaxing what it refuses.

The honest empty-catalog posture SHALL remain distinct from a contract failure. A plane with no configured model provider MUST receive a conformant empty catalog as a SUCCESS, and MUST NOT be served the refusal that means the contract could not be read — the two say different things to an operator and MUST NOT be collapsed.

#### Scenario: The model routes are served from a publisher checkout
- **WHEN** the dashboard serves from an openxFactory checkout carrying the publisher markers
- **THEN** the released schema validators MUST resolve from that same checkout
- **AND** the model catalog and chat-turn routes MUST NOT refuse for want of a declared consumption pin

#### Scenario: A sibling checkout is not preferred over the running tree
- **WHEN** the hosting repository is a publisher release and an aggregation-relative `openxFactory/` checkout also exists
- **THEN** the hosting repository MUST be resolved
- **AND** the sibling checkout's branch or working state MUST NOT affect the verdict

#### Scenario: An operator names a checkout explicitly
- **WHEN** a checkout is supplied directly or through `OPENXFACTORY_ROOT`
- **THEN** that checkout MUST be used in preference to the hosting repository

#### Scenario: The pinned bytes have drifted
- **WHEN** a pinned schema in the resolved checkout no longer matches its digest or its manifest entry
- **THEN** both model routes MUST refuse with the fixed catalog code
- **AND** the refusal MUST NOT disclose the checkout path or digest

#### Scenario: No model provider is configured
- **WHEN** the contract resolves and no provider port is available
- **THEN** the catalog route MUST return a conformant empty catalog as a success
- **AND** it MUST NOT return the contract-unavailable refusal

#### Scenario: The released rung runs without an environment override
- **WHEN** the dashboard test suite runs from a publisher checkout with no `OPENXFACTORY_ROOT` set
- **THEN** the released-contract probes MUST execute rather than skip
- **AND** a pin that a serve would refuse on MUST surface as a test failure

### Requirement: A session notebook is retirable after its session has already ended
A session notebook SHALL have a governed retirement route that does not require its session to still be live, because the two governed endings are not the only ways a session ends: a worktree and its branch can be removed directly — by a probe, or by clearing crash residue — and neither runs the abandon path, so neither retires the notebook.

The targeted retirement route SHALL CONTINUE to refuse a branch with no live session. That refusal is what prevents a caller inventing a session and retiring a notebook belonging to a live one, and it SHALL NOT be relaxed to admit dead sessions. The route for a session that has already ended SHALL instead be RECONCILIATION over the session namespace, which establishes death from the absence of any live session claiming the notebook rather than from a caller's assertion about one branch.

A retirement performed by reconciliation SHALL be reported as a reconciliation, distinguishable from a retirement performed by a governed ending, so the record does not claim an abandon that never happened.

#### Scenario: A hand-removed session's notebook is retired
- **WHEN** a session's worktree and branch have been removed without an abandon, leaving its notebook alive
- **THEN** the reconciliation route establishes that no live session claims that notebook and retires it
- **AND** the targeted `--session-ref` route still refuses that branch, because no live session bears it

#### Scenario: The targeted route keeps refusing a dead branch
- **WHEN** a caller names a branch with no live session for targeted retirement
- **THEN** the request is refused naming the joint liveness signal, unchanged by this capability's new route

### Requirement: Demote refreshes a staged topic's outline and never silently replaces it
The reverse transition SHALL leave the demoted topic's primary fragment carrying the ACTUAL text of the last attempted `proposal.md` and the demoted change's own provenance, and MUST NOT reset that fragment to the pre-proposal aspirational snapshot the change folder holds. The primary fragment is the file the existing deterministic, path-only selection already names; this requirement adds no second candidate file and MUST NOT change that selection.

A returning file whose destination is the topic's declared primary fragment SHALL keep `Status: staged`. It MUST NOT be flipped to `Status: draft`: the same selection rule still calls that file the staged topic's outline, so a draft status there makes the document disagree with every reader of it. The `Status: draft` flip remains correct and unchanged for the proposal documents returning to the topic's `openspec/` workspace.

The reverse transition SHALL fill the fragment's round-trip provenance slots from values it holds when it executes — the change id, the date demoted, the demote reason, the date the change was raised, and the change's state at demote. The state-at-demote slot SHALL carry the change's status TOGETHER WITH its task progress where the change records tasks, because the status alone is a constant: the reverse transition refuses any change that is not active, so a status-only slot can never distinguish one demote from another. Where the change records no tasks, the slot SHALL carry the status alone rather than a fabricated count. A value that is genuinely unavailable SHALL be recorded as unavailable and MUST NOT be fabricated or left reading as an unused placeholder.

The fragment's proposal-element sections — the sections wrapped in the ratified `xspec:candidate` marker grammar — SHALL be refreshed from the corresponding sections of the returned `proposal.md`. Only sections present in BOTH the fragment and the returned proposal SHALL be rewritten; the refresh MUST NOT invent a section the proposal does not carry, and MUST NOT delete a section the proposal omits. Where the demoted change carries no `proposal.md`, the provenance slots SHALL still be filled and the sections left untouched.

**The snapshot is a fallback SOURCE, never the authority.** Where the destination fragment already exists and differs from the change folder's snapshot of it, the reverse transition MUST NOT replace the destination's bytes. The refresh SHALL apply INTO the existing fragment, bounded to the provenance slots and the marked proposal-element sections, leaving every other byte of that file unchanged; and the snapshot copy SHALL be preserved in the topic beside it under a non-colliding name and named in the transition's own record, so that nothing is discarded either. Only where no fragment exists at the destination SHALL the snapshot be restored first and then refreshed. No live human work is ever silently replaced by a demote.

EXACTLY ONE addition is carved out of that byte bound, and it is not part of the refresh. Where the destination fragment carries no lifecycle status header at all, the reverse transition SHALL add one — the `staged` status the primary-fragment rule above already requires — and SHALL name that addition in its execution record. Without it the reverse transition leaves behind a fragment the forward transition refuses, making the cycle one-way for the very topic it has just returned material to; a live fragment can reach that state because it is the human's own working document and never had to pass the forward gate to acquire a header. It is an ADDITION and never a rewrite: a header the fragment already carries is the human's statement about their own document and MUST NOT be changed. No other byte outside the provenance slots and the marked proposal-element sections may be written.

The refresh SHALL be idempotent: applying it twice with the same inputs SHALL produce the same bytes. It SHALL preserve the destination document's own line-ending flavor rather than translating it.

#### Scenario: The state-at-demote slot carries progress beside the status
- **WHEN** a change recording tasks is demoted
- **THEN** the state-at-demote slot MUST carry the change's status and its task progress together
- **AND** the progress MUST come from the change's own recorded tasks rather than being counted a second way

#### Scenario: A demoted change records no tasks
- **WHEN** a change with no recorded tasks is demoted
- **THEN** the state-at-demote slot MUST carry the status alone
- **AND** a task count MUST NOT be fabricated

#### Scenario: The returning outline keeps its staged status
- **WHEN** a demote returns a file whose destination is the topic's declared primary fragment
- **THEN** that file MUST keep `Status: staged`
- **AND** the proposal documents returning to the topic's `openspec/` workspace MUST still continue as `Status: draft`

#### Scenario: The proposal-element sections carry the real prior text
- **WHEN** a topic that reached proposal is demoted and the change carries a `proposal.md`
- **THEN** the fragment's `xspec:candidate` proposal-element sections MUST carry that proposal's actual text
- **AND** they MUST NOT carry the pre-proposal aspirational text the change folder snapshotted

#### Scenario: The destination fragment already exists and differs
- **WHEN** a demote's primary-fragment destination exists and differs from the change folder's snapshot of it
- **THEN** the destination's bytes MUST NOT be replaced by the snapshot
- **AND** the provenance slots and the marked proposal-element sections MUST be refreshed in place, leaving every other byte of that file unchanged
- **AND** the snapshot MUST be preserved in the topic under a non-colliding name and named in the transition's record

#### Scenario: The live fragment carries no lifecycle status header
- **WHEN** a demote's primary-fragment destination exists, differs from the snapshot, and carries no lifecycle status header
- **THEN** a `staged` header MUST be added and named in the execution record
- **AND** every other byte outside the provenance slots and the marked proposal-element sections MUST still be unchanged
- **AND** a header the fragment already carries MUST NOT be changed

#### Scenario: The refresh runs twice
- **WHEN** the reverse transition's fragment refresh is applied twice with the same inputs
- **THEN** the resulting bytes MUST be identical
- **AND** the document's own line-ending flavor MUST be preserved rather than translated

### Requirement: The reverse transition resolves its origin staging topic from a declared order
The reverse transition SHALL resolve the staging topic it returns material to through a DECLARED PRECEDENCE ORDER rather than a single source: an explicitly supplied topic first, then the change's own recorded origin where that origin declares a staged kind, then a possibles-register pick edge naming the change. The first source that answers SHALL win, and an explicitly supplied topic SHALL always win, because a human naming the destination is the most direct statement of intent available.

A change whose recorded origin is not staged — an ad-hoc origin, or none — SHALL NOT have a staging topic inferred for it. The reverse transition SHALL refuse with a stated reason and name the explicit option instead, because a change that never came from staging has no topic to return to and inventing one would move material somewhere nobody chose.

The resolution MUST NOT depend solely on register state the forward transition destroys. A pick edge points at a staging folder, the forward transition removes that folder, and a resolution reading only pick edges therefore fails for exactly the changes that actually reached proposal — which is the condition a demote exists to reverse.

#### Scenario: A change that reached proposal is demoted with no pick edge present
- **WHEN** a change whose recorded origin declares a staged kind is demoted, and no possibles pick edge names it
- **THEN** the origin staging topic MUST be resolved from the change's own recorded origin
- **AND** the demote MUST NOT refuse for want of a topic

#### Scenario: An explicitly supplied topic is offered alongside a resolvable origin
- **WHEN** a human supplies a staging topic explicitly and the change's recorded origin also names one
- **THEN** the explicitly supplied topic MUST be used

#### Scenario: A change with no staged origin is demoted
- **WHEN** a change whose recorded origin is ad-hoc or absent is demoted with no explicit topic
- **THEN** the reverse transition MUST refuse with a stated reason
- **AND** it MUST NOT infer a staging topic
- **AND** the refusal MUST name the explicit option

### Requirement: The reverse transition's own artifacts do not block the topic's next transition
Every artifact the reverse transition writes into a staging topic SHALL satisfy the same governed-document rules the forward transition enforces on that topic, so that a topic which has received returned material can be transitioned again without an operator working around an artifact the reverse transition itself left behind. In particular a governed markdown artifact it writes SHALL carry a valid lifecycle status header.

This is a round-trip obligation rather than a formatting preference: the reverse transition is one half of a cycle whose other half refuses governed markdown without a status header, so an artifact that fails that rule makes the cycle one-way for the topic it was applied to.

#### Scenario: A returned topic is transitioned again
- **WHEN** a topic that has received returned material through the reverse transition is transitioned forward again over its whole folder
- **THEN** the forward transition MUST NOT refuse because of an artifact the reverse transition wrote
- **AND** every governed markdown artifact the reverse transition wrote MUST carry a valid lifecycle status header

### Requirement: The doxBench canvas presents Editor and Preview view tabs
The doxBench authoring canvas SHALL present the active buffer as exactly two VIEW TABS — `Editor`, the buffer's raw Markdown text, and `Preview`, its large rendered Markdown — and MUST NOT render the raw text and its rendering side by side in one pane. `Preview` SHALL be the tab selected when the canvas mounts, because most opens are to read or resume rather than to immediately type. Switching INTO `Preview` SHALL render the active buffer's current content before that tab becomes visible, so a switch never displays a rendering the debounce had not yet applied; switching into `Editor` SHALL require no such flush, because the raw text is never debounced. The view tabs SHALL reuse the capability's existing single Markdown rendering path and its existing debounce, and MUST NOT introduce a second rendering path, a second sanitizer, or a raw-markup sink. The view tabs answer WHICH VIEW of one buffer is shown and MUST NOT be used to answer which buffer is active — that choice belongs to the context region.

#### Scenario: The canvas mounts
- **WHEN** doxBench mounts its authoring canvas on a capable local human console
- **THEN** exactly two view tabs MUST be present, `Editor` and `Preview`
- **AND** `Preview` MUST be the selected tab
- **AND** the raw text and its rendering MUST NOT both be visible in one pane

#### Scenario: A human types and then switches to Preview
- **WHEN** a human edits the active buffer in `Editor` and switches to `Preview` before the debounce has elapsed
- **THEN** the rendering MUST be brought up to the buffer's current content as part of the switch
- **AND** the human MUST NOT see the pre-edit rendering

#### Scenario: A human switches back to Editor
- **WHEN** a human switches from `Preview` to `Editor`
- **THEN** the raw Markdown MUST be shown as it stands, with no re-render required and no content transformation

#### Scenario: A view tab is asked to select a buffer
- **WHEN** any realization would let the view tabs choose which buffer the canvas shows
- **THEN** it MUST be rejected — the context region selects the buffer and the view tabs select the view of it

### Requirement: One Save and one Cancel govern the doxBench canvas
The doxBench authoring canvas SHALL carry exactly ONE control slot placed outside both view tabs so that the slot and its answer are on screen whichever view the human is standing on, and what that slot renders SHALL be conditional on whether the loaded set holds unsaved work: while ANY buffer of the loaded set is dirty the slot SHALL render exactly ONE Save control and exactly ONE Cancel control, and while NO buffer is dirty it SHALL render exactly ONE Unload control in their place; the canvas MUST NOT render a duplicate Save, Cancel, or Unload per view tab or per buffer WITHIN THE CANVAS, and MUST NOT render Save or Cancel beside Unload, because the slot's own content is what tells a human whether this canvas is holding unsaved work. The dirty condition SHALL be read from the SAME per-buffer dirty flag Save and Cancel already derive their reachability from, and a realization that introduces a second source of dirtiness for the swap MUST be rejected. The condition SHALL be ANY-buffer-dirty rather than selected-buffer-dirty: Save answers for the whole canvas, so a rule that withdrew it whenever the SELECTED buffer happened to be clean would hide the only Save from a human whose other buffer still holds unsaved text — the precise hazard this capability's discard rules exist to prevent. The Unload control SHALL perform the loaded set's one way out for the SELECTED buffer, SHALL NAME that buffer where it can act, SHALL be reachable only where that buffer is a document the loaded set holds under a key that is not the reserved `outline` AND that names a document, and SHALL otherwise render as visibly inert while STATING the reason it cannot act as VISIBLE TEXT beside it rather than only in a hover title — the same standard this requirement already sets for an unreachable Save, and for the same reason doubled: a disabled control cannot take focus, so a title alone is reachable by neither a keyboard nor a screen reader. Amendment 2 (2026-08-21, Brett, ruled via browser annotation, verbatim: "if I do the workflow to edit a document, and then cancel instead of save, then try to unload, the unload button is stippled. It should allow the document to unload. only the outline can never unload. we always want that to be loaded. If saved or canceled so the document is in neutral position, then we can unload it."): the reserved set narrows to the outline alone; a backed reserved-slot document in the neutral position unloads like any other document; the unbacked slot remains inert for want of anything to unload. The `outline` key SHALL therefore be the ONLY key this control permanently withholds, and a document held under the reserved `document` key SHALL be as unloadable as one held under its own path once no buffer of the loaded set is dirty — the amendment narrows WHICH KEYS the control acts on and changes the dirty rule not at all. The UNBACKED `document` slot SHALL remain inert, and the realization MUST state that as a want of SUBJECT rather than as a reservation: the slot is held but names no document, so it has no loaded-set membership for the act to end, and the control's stated reason MUST NOT claim a reservation it no longer carries. Emptying the loaded set of every document SHALL NOT be prevented by withholding this act: where the turn contract's one-document floor makes such a session unable to build a turn, the surface SHALL refuse AT SEND with the composer preserved and the selector's honest empty state rendered, because a stated refusal a human can act on is a better discharge of a wire bound than a control that can never be reached. Where the gate capability is absent the slot SHALL keep its Save and Cancel posture unchanged and MUST NOT swap to Unload, because a surface that cannot save must go on saying so. A per-document Save on the context region's `docs` tile is NOT such a duplicate and SHALL be permitted: it lives on a different surface, is scoped to the document whose tile carries it, and reaches the same governed pipeline — one save mechanism with a second entry point, which is the opposite of a second save path. The canvas Save SHALL keep the semantics the editor buffer contract gives it — it persists every dirty backed buffer through the existing `create-document`/`edit-document` gate actions under that contract's ordering rule, as commit-per-gate-action on the tile's branch session, with `open-pr` remaining the separate promotion act. Save's verdict SHALL continue to be reported PER BUFFER, so a partial success across several documents remains separately readable. Cancel SHALL discard the SELECTED buffer back to its last loaded or saved base content and MUST NOT touch any other buffer, because discard destroys unsaved human work, has no cross-buffer dependency, and a single control that silently reverted a buffer the human is not looking at would be this surface's one irreversible surprise — a hazard that grows, not shrinks, as the loaded set grows. Neither control SHALL grant any authority the surface did not already hold: no force-save, no force-discard, no bypass of a refusal, and no second write route. Where the gate capability is absent, both controls SHALL state that absence as visible text beside them rather than only in a hover title, and MUST NOT be reachable.

#### Scenario: The canvas offers its controls while a buffer is dirty
- **WHEN** doxBench renders its authoring canvas with any buffer of the loaded set dirty
- **THEN** exactly one Save control and exactly one Cancel control MUST be rendered on the canvas, outside both view tabs
- **AND** no Unload control MUST be rendered beside them
- **AND** no per-view-tab or per-buffer duplicate of any of them MUST be rendered inside the canvas

#### Scenario: The canvas offers its controls while nothing is dirty
- **WHEN** doxBench renders its authoring canvas with no buffer of the loaded set dirty and a loaded document selected
- **THEN** exactly one Unload control MUST be rendered in the same slot, outside both view tabs
- **AND** no Save control and no Cancel control MUST be rendered beside it
- **AND** the Unload control MUST be reachable and MUST name the selected document it would unload

#### Scenario: Nothing is dirty and the selected buffer is the reserved outline
- **WHEN** doxBench renders its authoring canvas with nothing dirty and the reserved `outline` buffer selected
- **THEN** the Unload control MUST be rendered and MUST be visibly inert rather than absent
- **AND** it MUST state that the outline is reserved and is never unloaded as VISIBLE TEXT beside it, not only in a hover title, because the inert control cannot take focus to reveal one
- **AND** the `outline` key MUST be the ONLY key this control withholds by reservation (Amendment 2)

#### Scenario: The tile's own document is edited, cancelled, and unloaded
- **WHEN** a human edits the document held under the reserved `document` key, invokes Cancel rather than Save, and then invokes Unload
- **THEN** the Unload control MUST be reachable and MUST name that document, because the buffer is clean and its key is not the outline
- **AND** the document MUST leave the loaded set
- **AND** the selector MUST render its honest empty state where it was the only loaded document
- **AND** the same MUST hold where the buffer was returned to a clean state by Save instead of Cancel

#### Scenario: The selected buffer is the unbacked create slot
- **WHEN** doxBench renders its authoring canvas with nothing dirty and the reserved `document` key holding the not-yet-created artifact, which has no path
- **THEN** the Unload control MUST be rendered and MUST be visibly inert rather than absent
- **AND** its stated reason MUST name the absence of anything to unload, and MUST NOT claim the slot is reserved against unloading

#### Scenario: The slot renders where the gate capability is absent
- **WHEN** the authoring canvas is mounted with no gate save capability and no buffer is dirty
- **THEN** the slot MUST keep rendering its Save and Cancel controls with Save unreachable and its absence stated as visible text
- **AND** an Unload control MUST NOT be rendered in their place, because the swap would replace the one statement that a surface cannot save with a control that never says so

#### Scenario: The swap is asked for a second source of dirtiness
- **WHEN** any realization would drive the Save/Cancel-versus-Unload swap from a dirtiness signal other than the per-buffer dirty flag Save and Cancel already read
- **THEN** it MUST be rejected — two answers to "is this canvas holding unsaved work" is how the two come to disagree

#### Scenario: The canvas Save is invoked with several buffers dirty
- **WHEN** a human invokes the canvas Save with the outline and two documents dirty
- **THEN** each changed document MUST persist through its existing gate action under the buffer contract's ordering rule
- **AND** the verdict MUST be reported per buffer, so a committed buffer and a refused buffer are separately readable

#### Scenario: Cancel is invoked with several documents loaded
- **WHEN** a human invokes Cancel while one of four loaded buffers is selected and dirty
- **THEN** only the selected buffer MUST return to its base content, and the other three MUST be untouched
- **AND** nothing MUST be persisted, committed, or dispatched

#### Scenario: A control is asked for authority it does not have
- **WHEN** any realization would add a force-save, a force-discard, a refusal bypass, or a second write route to either control or to the tile's Save
- **THEN** it MUST be rejected — an additional entry point MUST NOT widen what the act may do

#### Scenario: The gate capability is absent
- **WHEN** the canvas renders on a surface with no gate capability
- **THEN** Save MUST be unreachable and MUST state that absence as visible text beside it, not only in a hover title

### Requirement: The doxBench chat binds to the active buffer selection
The doxBench chat SHALL take its working context from the SELECTED BUFFER of the loaded set and MUST NOT maintain a second, separately-chosen context beside it. Changing the selection SHALL change the chat's working context IMMEDIATELY, with no confirmation step, because changing which buffer is selected replaces no content and destroys nothing; the existing unsaved-edit guard SHALL be unchanged by this rule where it still applies, and it SHALL NOT be extended to selection, since a selection change no longer replaces any buffer's content once documents are held side by side rather than in one slot. Focusing the context region's `outline` selection tab SHALL put the chat in outline-editing context; selecting a loaded document in the chat rail's selector SHALL put the chat in that document's context. The chat SHALL STATE its current binding on the chat surface itself and SHALL make it SELECTABLE there, so which material a conversation is working on is both read and chosen where the conversation happens. Naming the bound buffer inside a turn's durable RECORD SHALL now be CARRIED rather than deferred: Phase A recorded the obligation against the buffer-set widening that next releases the chat-turn contract, this capability performs that release, and the record SHALL therefore name the bound buffer's key. A server-side-only field that no reader can consult MUST NOT be accepted as a substitute for it, and the record MUST derive the bound buffer from the request's DECLARED binding rather than inferring it from which document happened to be supplied. This SHALL generalize the existing active-path revalidation rather than replace it: a turn whose declared binding does not match a supplied buffer MUST still refuse before any provider call. Binding SHALL govern what the chat is working ON and MUST NOT narrow what the turn may be grounded on — the turn continues to carry the outline and every loaded document the grounded-turn contract requires, plus the assembled context packet.

#### Scenario: The selection changes mid-conversation
- **WHEN** a human with an open conversation selects a different loaded document
- **THEN** the chat's working context MUST follow immediately and the chat MUST show that document's own thread
- **AND** no confirmation step MUST be required, because no content is replaced by the change

#### Scenario: The outline is selected
- **WHEN** the context region's `outline` selection tab is focused
- **THEN** a turn submitted next MUST be bound to the `outline` buffer
- **AND** the chat surface MUST state that binding, so the human can see which material the conversation is working on before they send

#### Scenario: A turn record is consulted for its bound buffer
- **WHEN** a reader consults a completed turn's durable record to learn which buffer that turn was bound to
- **THEN** the record MUST name it, carried on the released envelope this capability's contract release provides
- **AND** the named buffer MUST be the one the request DECLARED as bound, never one inferred from the supplied paths

#### Scenario: A turn's declared binding does not match its buffers
- **WHEN** a turn declares a binding that matches no buffer supplied under it
- **THEN** the route MUST refuse before any provider call, exactly as the existing active-path revalidation does

#### Scenario: Binding is mistaken for grounding
- **WHEN** any realization would use the binding to drop a buffer or a packet section the grounded-turn contract requires the request to carry
- **THEN** it MUST be rejected — binding names what the chat works on, not what it may see

### Requirement: The canvas controls stay inside the per-buffer staleness guard
Every doxBench canvas control SHALL remain subject to the existing per-buffer content-identity guard, and consolidating controls onto the panel MUST NOT create a path around it. A Save attempted against a buffer whose settled content identity has moved since the acting request last observed it MUST refuse that buffer, exactly as it does today; an AI proposal applied against a moved identity MUST refuse as stale; a turn whose declared buffer hash does not match the supplied text MUST refuse before any provider call. The guard SHALL be applied PER BUFFER rather than per panel, because it describes one buffer's identity and nothing about it depends on how many buffers exist. Cancel MOVES a buffer's identity back to its base and SHALL therefore emit the same settled-identity notification an edit or a discard already emits, so no proposal card continues to offer Apply against text the buffer no longer holds. While a Save is in flight the canvas SHALL state that fact, withdraw the controls it would otherwise offer, and REFUSE rather than queue a second Save or a concurrent edit, because the bytes handed over are the bytes the verdict describes.

#### Scenario: Save meets a moved identity
- **WHEN** a buffer's settled content identity has moved since the request that is now being saved observed it
- **THEN** that buffer's save MUST refuse, and its text, base, and dirty state MUST be preserved exactly

#### Scenario: Cancel moves an identity
- **WHEN** Cancel restores the active buffer to its base content
- **THEN** the settled-identity notification MUST fire, exactly as it does for an edit or a discard
- **AND** any proposal card whose base no longer matches MUST stop offering Apply

#### Scenario: A second Save is attempted
- **WHEN** a human invokes Save while a Save is already in flight for this canvas
- **THEN** it MUST refuse and say so, and MUST NOT be queued

#### Scenario: An edit is attempted mid-save
- **WHEN** a human edits a buffer whose bytes are currently in flight to the save seam
- **THEN** the edit MUST refuse visibly rather than silently vanish or land underneath the verdict

### Requirement: The canvas view surface is expressed over the buffer set, not over two names
The view tabs, the canvas Save, the canvas Cancel, and the chat binding SHALL each be expressed over the capability's declared buffer set and its selected-buffer key, and MUST NOT hard-code any literal buffer name into their own structure. The view tabs render whichever buffer is selected and MUST NOT enumerate buffers; the canvas Save operates over the declared buffer set; Cancel operates on the selected-buffer key; the chat binds to the selected-buffer key. Phase A held this requirement WITHOUT widening the buffer set and required a realization that widened it to be rejected; that clause is now DISCHARGED, because the widening is exactly what this capability performs — in the buffer contract, the turn contract, and the save ordering rule, which are the three places that ever enumerated `outline` and `document`. The purpose of this requirement is unchanged and is now proven: widening the buffer set required changing those contracts and NOTHING on the view surface, and any FURTHER widening — a third buffer kind, a per-buffer view mode, a second selection surface — SHALL likewise be a change to the buffer contract alone. A realization that re-introduces a literal buffer name into the view tabs, the controls, or the binding MUST be rejected. A surface that selects a SUBJECT TO DESCRIBE rather than a buffer to edit — the `docs` context's document wheel, whose selection drives the abstract region's subject — SHALL NOT be a second selection surface within the meaning of this requirement and SHALL therefore require no change to the buffer contract. The test is whether the surface can make a buffer the canvas's SELECTED BUFFER: the wheel cannot, and a surface that could would be a second selection surface however it is labelled.

#### Scenario: A view surface names a buffer literally
- **WHEN** a realization builds the view tabs, Save, Cancel, or the chat binding around a literal buffer name
- **THEN** it MUST be rejected — these surfaces read the buffer set and the selected key

#### Scenario: The buffer set widens
- **WHEN** the buffer set grows from two buffers to the outline plus several loaded documents
- **THEN** the view tabs, the canvas Save, Cancel, and the chat binding MUST require no structural change to carry it
- **AND** the change MUST be confined to the buffer contract, the turn contract, and the save ordering rule

#### Scenario: A surface selects a subject rather than a buffer
- **WHEN** the docs context's wheel selection changes which document the abstract region describes
- **THEN** it MUST NOT change the canvas's selected buffer and MUST require no change to the buffer contract
- **AND** the view tabs, the canvas Save, Cancel, and the chat binding MUST be unaffected

### Requirement: The outline tab renders the staged-topic template
The doxBench outline tab SHALL render a conforming staged topic's primary fragment as its templated sections rather than as undifferentiated prose, so the surface a human iterates a topic in shows the same structure the template contract requires. Section identity SHALL come from the fragment's own headings and its `xspec:` marker fences — the addressing grammar the template already uses — and the tab MUST NOT infer sections by content-sniffing or by fabricating headings the fragment does not carry.

The tab SHALL offer an add-section affordance. A section added through it SHALL be written by the existing `edit-document` path on the topic's branch session, scoped by the section it targets — the heading, or the `xspec:candidate` fence where the section is a proposal-element block — as the patch's addressing key. It MUST NOT introduce a second write verb: section-scoped patching is a patch-TARGETING detail, not a different kind of action, and `edit-document` already supplies the branch-scoped, committed, reviewable machinery.

(AMENDED 2026-08-15, Brett: "amend to edit-document". As ratified this named `edit-apply`, carried from the topic's Q4. `edit-apply` is the gate console's MAIN-RESIDENT redline verb — it requires a `change_id` and applies to change documents — so it cannot write a staged topic's fragment on a session branch, and the two states are mutually exclusive besides: a fragment whose topic has an owning change has already moved out of staging. `edit-document` is the session content verb the buffer contract already uses. Q4's intent is unchanged; only the verb name was wrong.) Every section added this way SHALL carry its `Added-by:` provenance, whether the author is the human or an agent.

The tab SHALL degrade rather than refuse on a NON-CONFORMING fragment. Topics staged before the template ratifies are conformant only opt-in, so the tab MUST render what is present, MUST NOT report a pre-existing topic as broken, and MUST NOT rewrite a fragment into conformance as a side effect of opening it. Conformance is earned when a human next works the topic, never by the act of viewing it.

Rendering the template MUST NOT change the outline buffer's existing seeding, hashing, dirty-state, or Save semantics. The buffer contract governs how the outline is loaded and written; this requirement governs only how its content is presented and how a new section is addressed.

#### Scenario: A conforming topic is opened in the outline tab
- **WHEN** the outline tab opens a primary fragment carrying the template
- **THEN** its required sections MUST be rendered as identified sections
- **AND** section identity MUST come from headings and `xspec:` fences, never from content-sniffing

#### Scenario: A human adds a section
- **WHEN** the add-section affordance is used
- **THEN** the write MUST go through `edit-document` scoped to the targeted section
- **AND** the added section MUST carry `Added-by:` provenance
- **AND** no second write verb MUST be introduced

#### Scenario: A pre-template topic is opened
- **WHEN** the outline tab opens a fragment staged before ratification that carries none of the required sections
- **THEN** it MUST render what is present without reporting the topic as broken
- **AND** it MUST NOT rewrite the fragment into conformance on open

#### Scenario: The gate capability is absent
- **WHEN** the outline tab renders on a plane with no gate capability
- **THEN** the add-section affordance MUST NOT be offered as a live control
- **AND** no write path MUST be reachable from the page

### Requirement: Hosted actor surfaced additively on capabilities
The serving side SHALL include a `hosted_actor` field on the `/capabilities` response, resolved PER REQUEST from the gateway-stamped `X-Auth-Request-User` header, and `null` when that header is absent. The field is additive to the existing unversioned `/capabilities` shape — the same additive pattern the prior `model` and `repository` fields followed — so it introduces no version bump and existing consumers are unaffected. The field is DISPLAY-ONLY: the dox-auth gateway remains the identity authority, the dashboard's trust in the header rests on the NetworkPolicy boundary that lets only the gateway reach it, and the dashboard reads the header to present a name and never to authorize.

#### Scenario: The stamped header is present
- WHEN a request carrying `X-Auth-Request-User: alice` reaches the `/capabilities` route
- THEN the response's `hosted_actor` MUST be `alice`
- AND the value is resolved per request, beside the existing per-request `repository` field

#### Scenario: The header is absent
- WHEN `/capabilities` is requested on a local or loopback serve, or by an unauthenticated path that still reached the probe, with no `X-Auth-Request-User` header
- THEN `hosted_actor` MUST be `null`

#### Scenario: A client-supplied header on a direct request is not trusted differently
- WHEN a direct (non-gateway) request carries a client-supplied `X-Auth-Request-User`
- THEN the dashboard MUST treat it exactly as any other value of that header — as DISPLAY data only — and MUST NOT authorize any action on it, because trust rests on the NetworkPolicy boundary and the gateway, which strips client values before stamping its own, remains the identity authority

### Requirement: The dashboard authorizes nothing on the hosted actor
The dashboard SHALL treat `hosted_actor` as presentation data only and MUST NOT use it to grant, gate, or unlock any action. All existing write, gate, and edit gating stays exactly as-is — a loopback bind, a real checkout, a resolved local actor, and the per-serve console token — none of which consults `hosted_actor`. Recording the design-D16 boundary nuance explicitly: the credential-free dashboard now READS a stamped identity header for display, which does not make it a credential holder or an authorization authority.

#### Scenario: A hosted request with an actor still cannot write or gate
- WHEN a request is hosted (not loopback) and carries a stamped `hosted_actor`
- THEN every write, gate, and edit affordance MUST remain unavailable exactly as it is today
- AND the presence of `hosted_actor` MUST NOT change any capability verdict, because those capabilities are keyed on the loopback console verdict and never on identity presence

### Requirement: The user-account menu
The dashboard SHALL render a user-account control in the top-right corner header controls, beside the theme and settings buttons, that opens a dropdown showing the signed-in username, the session's access level, and a logout control. The username SHALL be `hosted_actor`. The access level SHALL be DERIVED from the existing `/capabilities.actions` map plus loopback state — read-only when no write, gate, or edit action is available, otherwise naming the granted capabilities — reusing existing capability flags and inventing no new authorization. The menu SHALL follow the established header-popover interaction contract: anchored under its button, closed on Escape and on outside click, keyboard-focusable, and DOM-safe with every dynamic value bound via `textContent` and never `innerHTML`.

#### Scenario: A hosted session opens the menu
- WHEN a viewer with a present `hosted_actor` opens the account menu
- THEN it MUST show that username, the derived access level, and an enabled logout control
- AND it MUST anchor under its button, close on Escape and outside click, and bind every dynamic value via `textContent`

#### Scenario: A local session opens the menu
- WHEN the menu opens with `hosted_actor` absent (local mode)
- THEN it MUST show the local actor if the serve resolved one, or a generic "local session" label otherwise
- AND it MUST show NO logout control, because there is no gateway session to end

#### Scenario: The access level reflects the capability verdict
- WHEN the menu renders its access level
- THEN it MUST read the level from the existing `/capabilities.actions` map plus loopback state, showing read-only when no write, gate, or edit action is available and otherwise naming the granted capabilities
- AND it MUST NOT introduce any new authorization flag

### Requirement: Logout delegates to the gateway
The logout control SHALL navigate the browser to the gateway-owned `/logout` route, which clears the session cookie and redirects to `/login`. The dashboard SHALL NOT implement session termination itself.

#### Scenario: Activating logout leaves for the gateway
- WHEN a viewer activates the logout control
- THEN the browser MUST navigate to `/logout`
- AND the dashboard MUST NOT clear any session or perform any termination of its own

### Requirement: The doxBench loaded set is the outline plus the documents the human loaded
The loaded set SHALL be exactly the `outline` buffer plus every document a human has LOADED through the `docs` tile's load verb, and no other route SHALL add a document to it — not a chat proposal, not a retrieval result, not the snapshot, and not an inherited edge. A document SHALL leave the loaded set only by an explicit human act, and that act MUST refuse or require an explicit discard while the buffer is dirty, because unloading a dirty buffer destroys unsaved work exactly as Cancel does. Membership SHALL be session-local working state: it MUST NOT be written into the snapshot, the register, the workbench manifest, or any generated projection, because "a human has this open right now" is a fact about a browser the generator cannot observe. A document the tile offers as READ-ONLY CONTEXT — an inherited, cluster-neighbourhood, cited, or inbound-context document that is not the tile's own editable material — MAY be loaded for grounding and for conversation, and its buffer SHALL carry that non-owned status so the governed Save withholds it with the stated context-only reason exactly as it does today; such a buffer MUST NOT be offered a reachable Save on its tile and MUST NOT be marked as needing one. The loaded set SHALL be bounded, and reaching the bound SHALL refuse the load with the measured bound stated rather than silently evicting a buffer that may hold unsaved work.

#### Scenario: A retrieval result is not a loaded document
- **WHEN** the knowledge service returns a document as evidence for a turn
- **THEN** that document MUST NOT join the loaded set, MUST NOT appear in the selector, and MUST NOT become an editable buffer
- **AND** the human MUST use the load verb if they want to edit it

#### Scenario: A dirty document is unloaded
- **WHEN** a human unloads a document whose buffer has unsaved edits
- **THEN** the unload MUST refuse or require an explicit discard, and MUST NOT silently drop the text
- **AND** WITHHOLDING the unload affordance entirely while anything is dirty MUST satisfy this rule, because an act that cannot be reached is refused in the strongest available form
- **AND** the state-level unload MUST keep refusing a dirty buffer that names no explicit discard, whether or not any surface can currently reach it

#### Scenario: A context-only document is loaded
- **WHEN** a human loads an inherited or cited document that is not this tile's own editable material
- **THEN** it MAY be loaded for grounding and conversation with its non-owned status carried on the buffer
- **AND** its tile MUST NOT offer a reachable Save and MUST NOT be marked as needing one

#### Scenario: The loaded-set bound is reached
- **WHEN** a human loads one document past the declared bound
- **THEN** the load MUST refuse and state the measured bound
- **AND** no already-loaded buffer MUST be evicted to make room

#### Scenario: Membership is asked to persist
- **WHEN** any realization would record which documents are loaded into the snapshot, register, manifest, or a published projection
- **THEN** it MUST be rejected — membership is session-local, and a generator cannot observe a live browser

### Requirement: The loaded-document selector names the working document
The chat rail SHALL carry a SELECTOR listing every loaded document, and its selected entry SHALL BE the selected buffer that the canvas presents and the chat binds to. The selector SHALL be a scrolling list rather than a fixed-width row of chips, so a session that accumulates many loaded documents needs no folding, overflow, or least-recently-used eviction policy — the control is the overflow mechanism. An entry whose filename does not fit on one line SHALL reveal its full name on hover and to assistive technology, and MUST NOT be silently truncated or ellipsized into ambiguity with another entry. Every entry SHALL be distinguishable when two loaded documents share a basename, because a selector that cannot tell two files apart is worse than one that shows a longer name. The selector SHALL be keyboard-reachable and operable with the surface's established selection semantics, and MUST NOT introduce a second spelling of selection beside the one the surface already uses. Selecting an entry SHALL be immediate, SHALL switch the transcript to that document's thread, and MUST NOT be the surface's only route to selection: loading a document and focusing the `outline` selection tab SHALL both continue to select, and every route SHALL leave the selector, the canvas, and the chat agreeing about which buffer is selected. Where no document is loaded, the selector SHALL render its empty state honestly rather than hiding, and the `outline` buffer SHALL remain selectable and workable on its own.

#### Scenario: Several documents are loaded
- **WHEN** a human has loaded five documents
- **THEN** the selector MUST list all five and MUST name which one is selected
- **AND** no entry MUST be folded away, dropped, or evicted to fit

#### Scenario: A long filename does not fit
- **WHEN** a loaded document's name is longer than one line of the selector
- **THEN** hovering the entry MUST reveal the full name, and the full name MUST be available to assistive technology
- **AND** the entry MUST remain distinguishable from every other entry

#### Scenario: Two loaded documents share a basename
- **WHEN** two loaded documents have the same file name in different folders
- **THEN** the selector MUST distinguish them

#### Scenario: Selection is changed from another route
- **WHEN** a human selects the `outline` tab or loads a new document
- **THEN** the selector, the canvas, and the chat MUST all agree about which buffer is selected

#### Scenario: Nothing is loaded yet
- **WHEN** no document has been loaded
- **THEN** the selector MUST render an honest empty state rather than hiding
- **AND** the `outline` buffer MUST remain selectable and workable

### Requirement: A docs tile carries read, load-for-editing, and save
The `docs` context's expanded tile SHALL offer exactly three verbs — READ, which opens the immersive full-window read-only reader unchanged; LOAD-FOR-EDITING, which loads the document into the chat context as a member of the loaded set and selects it; and SAVE, which persists that document through the same governed pipeline the canvas Save uses. These are the CONTRACT names other requirements refer to; the visible control labels SHALL follow the surface's own copy, and load-for-editing MAY be labelled `edit` or `load` — the annotation that ruled this verb used both words — provided the label does not reclaim the bare word "edit" for an act that happens outside the app. The SAVE verb SHALL be reachable only while that document's buffer is dirty and SHALL be visibly inert otherwise, so the control's own state answers "does this need saving" without a sentence of standing text. The tile SAVE SHALL run the SAME pipeline as the canvas Save, restricted to that document plus the outline-ancestry step the buffer contract requires when the outline is dirty, and it MUST NOT persist another loaded document the human is not looking at; every buffer it acted on — including the outline when the ancestry step ran — SHALL report its own verdict on the same surfaces the canvas Save reports on. A tile whose document is LOADED SHALL be visibly marked as loaded and, where that buffer is dirty, as needing a save; the marking SHALL be driven from live session-local buffer state and MUST NOT be written into the snapshot, the register, or any generated projection. The three verbs SHALL be offered only where the surface already holds the authority each needs: READ requires no gate capability, and LOAD and SAVE MUST be unreachable wherever editing is unreachable, stating that absence rather than failing on activation. A document that is not this tile's own editable material MUST NOT offer a reachable SAVE. Where the `docs` context presents its document set as a WHEEL rather than as a list, these three verbs SHALL attach to the WHEEL'S EXPANDED TILE, and their contract names, their authority conditions, their dirty-state gating, and their per-buffer reporting obligations SHALL be unchanged: how the document set is PRESENTED is not a change to the verbs a document carries, and a change of presentation MUST NOT introduce a fourth verb.

#### Scenario: A tile is expanded
- **WHEN** a human expands a `docs` tile on a capable local console
- **THEN** the action row MUST offer read, load-for-editing, and save
- **AND** save MUST be inert unless that document's buffer is dirty

#### Scenario: Read is unchanged
- **WHEN** a human activates read
- **THEN** the immersive full-window read-only reader MUST open exactly as it does today, and no buffer MUST be created or loaded

#### Scenario: A loaded document's tile is marked
- **WHEN** a document is loaded and its buffer becomes dirty
- **THEN** the tile MUST be visibly marked as loaded and as needing a save
- **AND** the marking MUST come from live buffer state and MUST NOT be recorded in the snapshot or any projection

#### Scenario: The tile save runs with a dirty outline
- **WHEN** a human invokes a tile's save while the outline is also dirty
- **THEN** the outline MUST be persisted first as the ancestry step and that document MUST then be persisted, each reporting its own verdict
- **AND** no other loaded document MUST be persisted by that act

#### Scenario: Editing is unavailable
- **WHEN** the tile renders on a surface where editing is unreachable
- **THEN** load and save MUST be unreachable and MUST state that absence rather than failing when activated
- **AND** read MUST remain available, because it needs no gate capability

#### Scenario: The docs context presents a wheel
- **WHEN** the `docs` context renders its document set as a wheel rather than as a list
- **THEN** the three verbs MUST attach to the expanded wheel tile with their authority conditions unchanged
- **AND** no fourth verb MUST be introduced by the change of presentation

### Requirement: Each loaded document carries a session thread with a structured state header
Every loaded document SHALL carry its own persisted chat THREAD, and switching the selected document SHALL switch which thread the chat shows and appends to. A thread SHALL persist as a SIDECAR FILE on the session's own branch, written only inside the session worktree and never into the served checkout, and it SHALL carry a STRUCTURED THREAD-STATE HEADER above its transcript declaring at least: the active goal, the accepted facts, the open questions, the decisions made in the thread, the refs of evidence the thread retrieved, and the pending actions. Thread state SHALL be NON-AUTHORITATIVE by construction and REGENERABLE from the transcript it summarizes: it MUST NOT be cited as governed truth, and it MUST NOT become truth by being compacted, promoted in place, or carried into a record that claims authority. COMPACTION SHALL preserve those commitments rather than the narrative that produced them: a compaction that drops an open question, a decision, an accepted fact, or a pending action SHALL be a defect, while dropping prose that restates them is the point. Threads SHALL commit with the document's Save, riding the existing one-commit-per-gate-action substrate so a thread and the document text it discusses cannot land through separate paths. Threads are WORKING MEMORY: they SHALL be excluded by default from the promotion a session's pull request performs, and a finding SHALL leave a thread only through the lifecycle verbs that already exist — an idea note, a fragment, or a disposition on the topic, with provenance — so no parallel decision store is created. Raw chat SHALL NOT become durable truth automatically by any path. Threads SHALL exist only where branch sessions exist, and MUST be absent on the hosted plane and wherever the gate capability is unavailable.

#### Scenario: The selected document changes
- **WHEN** a human selects a different loaded document
- **THEN** the chat MUST show that document's own thread and append to it
- **AND** the previous document's thread MUST be preserved unchanged

#### Scenario: A thread is compacted
- **WHEN** a thread is compacted to stay inside its bounds
- **THEN** every open question, decision, accepted fact, evidence ref, and pending action in the state header MUST survive the compaction
- **AND** the compacted result MUST remain non-authoritative and regenerable

#### Scenario: A document is saved
- **WHEN** a human saves a document whose thread has new turns
- **THEN** the thread MUST commit with that document's save inside the session worktree
- **AND** the served checkout MUST remain untouched

#### Scenario: A thread finding should become durable
- **WHEN** something decided in a thread should become part of the corpus
- **THEN** it MUST be promoted through an existing lifecycle verb with provenance
- **AND** the thread itself MUST NOT be promoted as truth and MUST NOT be published by default with the session's pull request

#### Scenario: Threads are asked for on a surface without sessions
- **WHEN** doxBench runs on the hosted plane or without the gate capability
- **THEN** no thread MUST be created, written, or offered

### Requirement: Share-session hands a live session to a colleague
The workbench SHALL offer an explicit human-only SHARE-SESSION verb that commits the session's threads, PUSHES the session branch, and returns the pushed ref, so a colleague can resume the same session from the fetched branch. Threads and every other session artifact SHALL be LOCAL until this verb runs: no thread, buffer, or session artifact SHALL be pushed as a side effect of a Save, a turn, a compaction, or a periodic task, because a working note that leaves the machine without an explicit act is a disclosure nobody chose. The verb SHALL open no pull request, request no review, and hold NO approval or merge authority; it SHALL reuse the existing remote-write path rather than introducing a second one, and it MUST NOT bypass any branch protection. Invoking it when nothing has changed since the last share SHALL report that honestly rather than pushing again. The verb SHALL be recorded as a human gate action naming the branch and the pushed ref, and it MUST be loopback-only, MUST fail closed on an unresolved actor, and MUST reject any invocation that cannot demonstrate it originates from the human console this serve started, exactly like every other gate action on this surface. The push identity SHALL follow the PLANE under the same rule the session save verb already carries: on the local plane the invoking engineer's own credential, never a stored service identity. Share-session SHALL be a local-plane capability, absent on the hosted plane, and where the gate capability is absent it SHALL render as a copyable descriptor rather than a live control.

#### Scenario: A session is shared
- **WHEN** a human invokes share-session on an active session with uncommitted threads
- **THEN** the threads MUST commit, the branch MUST be pushed, and the pushed ref MUST be returned and recorded
- **AND** no pull request MUST be opened and no review MUST be requested

#### Scenario: A colleague resumes the session
- **WHEN** a colleague fetches the shared branch and opens the same tile
- **THEN** they MUST be able to resume that session — its documents and its threads — from the fetched branch under the existing session-join rules

#### Scenario: Nothing has changed since the last share
- **WHEN** share-session is invoked with nothing new to push
- **THEN** it MUST report that honestly and MUST NOT push again

#### Scenario: A thread leaves the machine without the verb
- **WHEN** any realization would push a thread, a buffer, or a session artifact as a side effect of a Save, a turn, a compaction, or a scheduled task
- **THEN** it MUST be rejected — sharing is an explicit act

#### Scenario: Share-session is asked for approval authority
- **WHEN** any path would have share-session merge, approve, request review, or bypass protection
- **THEN** it MUST be refused

### Requirement: The staged-set knowledge service assembles a bounded context packet
Per-turn context SHALL be assembled as a BOUNDED CONTEXT PACKET by a Staged-Set Knowledge Service, and the packet SHALL contain the SELECTED document's thread in full, the THREAD-STATE HEADERS of the other loaded documents' threads, and SELECTED corpus evidence from the tile's staged set plus promoted findings only — never an unrestricted corpus, never another tile's material, and never a thread the session does not hold. The packet SHALL declare its purpose, the exact sources it carries with their refs, its bound scope, and its expiry, and it SHALL be invalid as input to any other purpose, scope, or expired turn; a consuming surface presented with such a packet MUST reject it and request a new one. Assembly SHALL run as a RAIL BEFORE any retrieval provider or model provider is reached: selection, the lifecycle-status exemption below, and the compression policy are decided first, and a refusal at that stage MUST disclose no packet content. The service SHALL be exposed behind exactly ONE tool boundary declaring a small tool contract — search, get_source, promote_finding, and reindex, with a graph query name RESERVED and unimplemented — and behind that boundary an INTERNAL ASSEMBLY PORT SHALL be the product-neutral surface a retrieval backend implements as a declared PROVIDER PROFILE. The v1 profile SHALL be local and GRAPH-LESS: lexical retrieval plus small embedded vectors plus the structured thread-states, with NO graph engine, on the recorded caution that a graph memory layer measured worse on recall, latency, and token cost than the retrieval it replaced. A graph provider SHALL be admitted only when a concrete GRADUATION TRIGGER is recorded — a recurring need for dependency traversal, contradiction detection, or change-impact analysis — and admitting one SHALL require the semantic-plane bounds to hold at that time: its index stays a derived projection, its inferred relations stay advisory, and no inference MAY create or widen authority, establish approval, or authorize an action. The retrieval backend SHALL be an INSTALL-TIME DECLARATION under the ratified two-case principle — local-embedded for a self-hosted install, a hosted backend only where a tenant install declares one — and a backend MUST NOT be selected at runtime by a turn, a prompt, or a heuristic. Content whose lifecycle status is APPROVED or RATIFIED SHALL be EXEMPT from aggressive compression, and the exemption SHALL be applied BY THE ASSEMBLER keyed on the content's own lifecycle status header; it MUST NOT be delegated to any component that cannot read that status. The source-ranking hierarchy SHALL be stated in the harness system prompt in this order — ratified or standard canon, then accepted or staged facts, then promoted findings, then active thread state, then harness-local memory last and explicitly non-authoritative — and MUST NOT be left to the model to infer. Where the knowledge service is unavailable the turn SHALL degrade to a declared reduced packet — the selected thread and the loaded buffers, with the reduced posture STATED — and MUST NOT bypass a rail to reach a provider, MUST NOT silently substitute an unbounded context, and MUST NOT fail an editor that does not need it.

#### Scenario: A turn is assembled
- **WHEN** a turn is submitted with four documents loaded
- **THEN** the packet MUST carry the selected document's thread in full, the other three threads' state headers, and the evidence the service selected
- **AND** the packet MUST declare its purpose, sources, scope, and expiry

#### Scenario: A packet is reused for another purpose
- **WHEN** a packet issued for one turn's purpose or scope is presented for another, or after it has expired
- **THEN** the consuming surface MUST reject it and request a new packet

#### Scenario: Evidence outside the staged set is requested
- **WHEN** retrieval would return material outside the tile's staged set and the promoted findings
- **THEN** it MUST be excluded from the packet

#### Scenario: A graph engine is proposed for v1
- **WHEN** any realization would add a graph engine, graph store, or graph index before a graduation trigger is recorded
- **THEN** it MUST be rejected, and the reserved graph query name MUST remain unimplemented

#### Scenario: A graph provider is graduated in
- **WHEN** a recorded graduation trigger admits a graph provider behind the assembly port
- **THEN** its index MUST remain a derived projection and its inferred relations MUST remain advisory
- **AND** no inference MUST create authority, establish approval, or authorize an action

#### Scenario: Ratified content meets the compressor
- **WHEN** the packet carries content whose lifecycle status is approved or ratified
- **THEN** the assembler MUST exempt it from aggressive compression before any provider is reached
- **AND** the exemption MUST NOT be delegated to a component that cannot read a lifecycle status

#### Scenario: The backend is chosen at runtime
- **WHEN** a turn, a prompt, or a heuristic would select the retrieval backend
- **THEN** it MUST be rejected — the backend is an install-time declaration

#### Scenario: The knowledge service is unavailable
- **WHEN** the knowledge service cannot answer
- **THEN** the turn MUST degrade to the declared reduced packet with the reduced posture stated
- **AND** it MUST NOT substitute an unbounded context, bypass a rail, or make the editors unusable

### Requirement: Context compression is a three-layer stack with declared fidelity
Compression SHALL be organized as THREE layers, each with a declared fidelity contract, and no layer SHALL be described as doing another's work. Layer one is SELECTION, performed by the knowledge service: it is LOSSLESS BY REFERENCE, because material left out of a packet remains one retrieval call away and the packet names what it carries. Layer two is SEMANTIC COMPACTION into the thread-state header: it is LOSSY BY DESIGN, human-reviewable, promotion-gated, non-authoritative, and regenerable — it preserves commitments and discards narrative. Layer three is MECHANICAL REVERSIBLE COMPRESSION at the model boundary: heavy material offloads to session artifacts behind recoverable placeholders, and it SHALL be REVERSIBLE — an offloaded item MUST be retrievable in full by the same session — and SHALL run INSIDE this surface's own trust boundary, with no third-party proxy in the path and no new network dependency. Every artifact any layer produces SHALL be non-authoritative and regenerable, and MUST NOT become truth by being compressed, cached, or offloaded. The lifecycle-status exemption SHALL live UPSTREAM of layer three, in the assembler, and MUST NOT be delegated into any component that cannot read a lifecycle status — a compressor with no caller-metadata surface is disqualified from carrying it by construction, not by preference. A candidate component for any layer SHALL be recorded with its adoption gates rather than adopted provisionally, and this capability MUST NOT depend on a watch-listed candidate: a candidate is admitted only when every recorded gate holds, including a sandboxed trial measuring net benefit on this surface's own workload rather than a published headline. Every external claim about a candidate SHALL be verified against the upstream source before it enters contract text. A LAYER-2-CLASS SIBLING ARTIFACT MAY be declared: a derived artifact that carries layer two's FIDELITY WORD — lossy by design — without being layer two's own work, without writing the thread-state header, and without claiming layer two's commitment-preservation rule, which is shaped for a transcript and not for a document. A sibling SHALL declare its own verifier and its own refusal rule, and MUST NOT be recorded as a second OWNER of any layer: the declared owner of each layer stays exactly one component, because a fidelity contract with two owners in a one-owner field is a comment rather than a checker. A sibling is bound by every clause of this requirement that speaks of what ANY layer produces — non-authoritative, regenerable, never truth by being compressed, cached, or offloaded — and by the promotion rule, which stays a human creating a new object through review. Layer two's HUMAN-REVIEWABLE adjective SHALL be inherited by a sibling as a STATED OPEN OBLIGATION rather than claimed as discharged where the realization provides only presentation, because rendering an artifact in a pane is not a human reviewing it.

#### Scenario: A layer claims another's fidelity
- **WHEN** a realization describes selection as lossy, semantic compaction as lossless, or mechanical offload as a semantic summary
- **THEN** it MUST be rejected — the three fidelity contracts are what make the stack readable

#### Scenario: An offloaded item is needed again
- **WHEN** material offloaded at layer three is required in full later in the same session
- **THEN** it MUST be retrievable in full

#### Scenario: A third-party compressor is proposed
- **WHEN** a proposal would route model traffic through a third-party compressor or proxy
- **THEN** it MUST be rejected unless every recorded adoption gate holds, including a sandboxed trial on this surface's own workload
- **AND** the lifecycle-status exemption MUST NOT be moved into a component that cannot read a lifecycle status

#### Scenario: A compressed artifact is cited as truth
- **WHEN** any path would treat a summary, a thread-state header, an offloaded artifact, or a derived index as authoritative
- **THEN** it MUST be rejected — promotion happens only by creating a new object through review

#### Scenario: A sibling artifact is declared at a layer's fidelity class
- **WHEN** a derived artifact is declared as a layer-2-class sibling
- **THEN** it MUST carry the lossy-by-design fidelity word, declare its own verifier and refusal rule, and remain non-authoritative and regenerable
- **AND** the declared owner of layer two MUST remain exactly one component

#### Scenario: A sibling claims layer two's own obligations
- **WHEN** a sibling artifact is described as preserving commitments or as writing the thread-state header
- **THEN** it MUST be rejected — those are layer two's own work, and a sibling borrows the fidelity class and not the job

#### Scenario: Presentation is offered as human review
- **WHEN** a realization claims a sibling artifact is human-reviewable because it is rendered on a surface
- **THEN** the claim MUST be rejected and the adjective MUST stand as a stated open obligation

### Requirement: The chat harness runs behind the existing model port through a local bridge
The chat harness SHALL be reached as an ADAPTER for the existing three-member model port, through a THIN LOCAL BRIDGE that translates the server's call into the harness's own process protocol, and the bridge SHALL be the only component that knows the harness's protocol. The bridge SHALL be a local child process of the console's own server, MUST NOT be reachable from the browser or from any non-loopback surface, and MUST NOT hold, read, or log a provider credential — where a menu entry reaches a hosted provider, its credential comes from the deployment's approved credential mechanism through the ratified broker lane. The bridge's process lifecycle SHALL be declared: it is started on demand, supervised, and restarted on failure, and a bridge that cannot start or has died SHALL surface as the honest model-unavailable posture — the editors and the loaded set stay usable and the chat states why it is not — rather than as a crash, a hang, or a silent empty answer. ONE harness session SHALL correspond to one document thread, so switching the selected document switches the harness session, and the harness's own session identity MUST NOT be shared across two documents' threads. The SIDECAR THREAD FILES SHALL REMAIN THE RECORD: doxBench mirrors each turn into the sidecar, and the harness's native memory backends MUST NOT hold the threads. Where a harness-native memory backend is enabled at all it SHALL hold only non-authoritative material, SHALL be ranked last by the source hierarchy, and MUST NOT be consulted as a source of governed truth — two stores claiming to be the same thread is a split brain, and the sidecar wins by contract, not by convention. Per-turn model choice SHALL be applied inside the adapter before the prompt is dispatched, and MUST NOT be expressed as an additional port member.

#### Scenario: The bridge is not running
- **WHEN** a turn is submitted and the bridge cannot start or has died
- **THEN** the surface MUST show the honest model-unavailable posture and state why
- **AND** the editors and the loaded set MUST remain fully usable

#### Scenario: The selected document changes mid-session
- **WHEN** the human switches to another loaded document and sends a turn
- **THEN** the harness session MUST switch with the thread
- **AND** one harness session MUST NOT serve two documents' threads

#### Scenario: The harness offers to remember the thread
- **WHEN** the harness's native memory would store the thread, or a turn would be reconstructed from it
- **THEN** it MUST be rejected — the sidecar is the record
- **AND** any harness-local memory that is enabled MUST be treated as non-authoritative and ranked last

#### Scenario: The bridge is reached from outside
- **WHEN** anything other than this server's own process would reach the bridge
- **THEN** it MUST be refused — the bridge is loopback-local and holds no credential of its own

### Requirement: The chat-turn contract release carries the bound buffer and the model
This capability's widened turn SHALL be carried by a RELEASED chat-turn contract, and the release SHALL be additive: the currently released envelopes SHALL remain valid and byte-identical, and the widened shape SHALL be introduced as a co-resident envelope family rather than by mutating a closed envelope, so nothing that validates today stops validating. The released widened family SHALL carry, at minimum: the outline plus every loaded document buffer, the BOUND BUFFER's key on both the request and the durable record, the per-buffer observed hashes keyed by buffer, a proposal target expressed as a buffer key, and the SELECTED-MODEL metadata that lets a record state which model answered. The release version SHALL be ALLOCATED AT REALIZATION under the repository's contract-versioning policy and MUST NOT be reserved by this proposal, because a reserved number is a claim about a merge order nobody knows yet. The release SHALL record its change class, its migration note, and the removal target for anything it deprecates, and the older family SHALL keep working for at least one full published release after it is deprecated. The runtime SHALL keep resolving its pinned wire schemas from the checkout it runs in and MUST keep refusing before consulting any provider when a pinned contract cannot be read; a release MUST NOT relax that refusal. A field the released envelope has no room for MUST NOT be carried as a server-side-only value that no reader can consult, and MUST NOT be inferred from an adjacent field that answers a different question — the record either names the thing or the gap stays stated.

#### Scenario: An older client sends a released v1 turn
- **WHEN** a client submits a turn in the previously released envelope shape
- **THEN** it MUST still validate and MUST still be served
- **AND** the older shape's bytes MUST be unchanged by this release

#### Scenario: The release version is reserved early
- **WHEN** a proposal would reserve the release's version number before merge order is known
- **THEN** it MUST be rejected — the version is allocated at realization

#### Scenario: A record is asked which model answered
- **WHEN** a reader consults a turn record for the model that produced it
- **THEN** the record MUST name it from the released envelope's own metadata

#### Scenario: A field has no room in the envelope
- **WHEN** a needed field does not fit the released envelope
- **THEN** it MUST NOT be carried as an unreadable server-side-only value or inferred from a field that answers a different question
- **AND** the obligation MUST be recorded against the release that will carry it

### Requirement: The deterministic document abstract is never captioned as a distillation and states its absences
The `docs` context's abstract region MUST NOT caption, label, or announce the deterministic abstract as a distillation, as a summary the surface produced, or as any analysis nobody ran — it re-presents fields the snapshot already carries, and claiming more would be the surface asserting work nobody did. Where the snapshot carries no derived material at all for the subject document, the region SHALL STATE that absence in words rather than rendering an empty box. Where a single named field is absent, the region SHALL OMIT that field rather than rendering a placeholder that reads as a value.

#### Scenario: A document carries no derived material
- **WHEN** the abstract region's subject is a document the snapshot references but does not catalogue
- **THEN** the region MUST state in words that there is nothing derived to show
- **AND** it MUST NOT render an empty abstract that reads as the document having no content

#### Scenario: A named field is absent for the subject
- **WHEN** the snapshot carries no summary for the subject document, or the document declares no topics
- **THEN** the region MUST omit that field rather than rendering a placeholder that reads as a value

#### Scenario: The deterministic abstract would be called a distillation
- **WHEN** any caption, label, or accessible name would describe the deterministic abstract as a distillation or as an analysis the surface performed
- **THEN** it MUST be rejected

### Requirement: The model-derived distilled document abstract
The `docs` context SHALL offer a MODEL-DERIVED distilled abstract of ONE subject document, declared as a layer-2-class sibling artifact — lossy by design, non-authoritative, and regenerable from the document — and it MUST NOT become authoritative by being cached, rendered, copied, or projected. The abstract's SUBJECT SHALL be the document the docs wheel has selected, which is a reading selection and never a buffer, and the bytes described SHALL be the SAVED file's content: where the subject is also a loaded buffer with unsaved edits, the abstract SHALL be captioned as describing the saved version, and unsaved buffer text MUST NOT be sent to any provider. The subject SHALL be drawn from the scope projection's EDITABLE path set, honouring the surface's standing rule that disclosure requires edit authority; where a pointed-at document is readable but not editable, the region SHALL state honestly that no distillation is available for it rather than generating one, and a realization MUST NOT widen the disclosure set to reach a subject. The deterministic snapshot-derived abstract SHALL remain present, separately captioned, and SHALL be the region's default, because it is the one that exists before any model runs. The model-derived abstract SHALL feed no completeness score, no staged-topic health aggregate, no readiness tier and no gate, and SHALL NOT be promotable except by a human creating a new document through an existing gate verb.

#### Scenario: A subject is readable but not editable
- **WHEN** the wheel's selected document is in the scope's context paths but not its editable paths
- **THEN** the region MUST state that no distillation is available for that document
- **AND** no provider MUST be reached and the disclosure set MUST NOT be widened

#### Scenario: The subject is a dirty loaded buffer
- **WHEN** the subject document is loaded and its buffer carries unsaved edits
- **THEN** the abstract MUST describe the SAVED content and MUST be captioned as describing the saved version
- **AND** the unsaved buffer text MUST NOT be sent to any provider

#### Scenario: A reader wants the document's own account
- **WHEN** the abstract region opens on any subject
- **THEN** the deterministic snapshot-derived abstract MUST be the default view
- **AND** the model-derived abstract MUST be separately captioned wherever it is shown

### Requirement: Abstract generation is explicitly invoked and never a side effect of selection
Generation of a model-derived abstract SHALL be invoked EXPLICITLY by a human control acting on the currently selected subject, and MUST NOT be triggered by a selection change, a mount-time seed, a scope opening, or any other side effect — the docs wheel notifies its consumer on every notch and at mount, so a selection-triggered design would dispatch a model call for every document a reader spins past. An in-flight generation SHALL be cancellable and SHALL state the expected wait with THE ADAPTER'S OWN DECLARED TIMEOUT as its visible bound — the value the adapter reports, not the contract's maximum, which is a validated ceiling and not a prediction. A RE-GENERATE control SHALL be offered against the subject's current content digest, and invoking it SHALL carry an EXPLICIT REFRESH INTENT that bypasses the abstract cache's completed-entry replay as that cache's own requirement specifies — without it the control would be inert whenever content and model are unchanged, which is the ordinary case a reader invokes it in. Every generation SHALL carry the subject path, the content digest, and the RESOLVED MODEL ID it was generated for, and WHEN a SUCCESSFUL generation resolves against a subject the pane no longer has selected, the result MUST be discarded unrendered and uncached and the not-yet-generated caption MUST show for the current subject; a REFUSAL or an ERROR answering the subject the request was DISPATCHED for SHALL be recorded against THAT subject and rendered on it when it is next shown — a refusal carries no prose, so it is the one answer that cannot paint a wrong document, and dropping it left an invoked control looking like one that did nothing — and MUST NOT be rendered against any other subject, while any answer NAMING A DIFFERENT subject than the one dispatched MUST be discarded whole and recorded against neither. Where the subject's content has moved past the digest an abstract was generated from, the abstract SHALL BE SHOWN AND LABELLED STALE with its source digest stated, and MUST NOT be silently discarded, silently refreshed, or presented as current; a regeneration in flight SHALL show the in-flight state over it. The SOURCE DIGEST for an unloaded subject SHALL be the digest of the SERVED SAVED CONTENT, and the per-buffer settled-content-identity guard SHALL be escalated to only where the subject is also a loaded buffer — most wheel subjects have no buffer, and a per-buffer rule applied to them would have nothing to compare. An abstract already generated in the session SHALL survive leaving and re-entering the tile, keyed by subject path, content digest and resolved model id, so returning to a document does not spend a second call on an answered question — and a re-entry SHALL carry NO refresh intent, because a reader coming back to a document has asked for nothing. Where the gate capability is absent on the local console, the generation control SHALL be ABSENT rather than present-and-refusing, and any already-generated abstract SHALL remain readable with its normal caption.

#### Scenario: A human spins the docs wheel
- **WHEN** a human moves the docs wheel across N documents
- **THEN** no model dispatch MUST occur

#### Scenario: A slow generation resolves after the subject changed
- **WHEN** a generation resolves and the pane's selected subject is no longer the subject it was dispatched for
- **THEN** a SUCCESSFUL result MUST be discarded unrendered and MUST NOT be cached
- **AND** the region MUST show the not-yet-generated caption for the current subject
- **AND** a REFUSAL or ERROR answering the DISPATCHED subject MUST be recorded against that subject and rendered on it when it is next shown, and MUST NOT be rendered against any other subject
- **AND** a result NAMING A DIFFERENT subject than the one dispatched MUST be discarded whole, recorded against neither subject

#### Scenario: A generation is in flight
- **WHEN** a generation has been invoked and has not resolved
- **THEN** the region MUST show a cancellable in-flight state stating the expected wait bounded by the adapter's OWN declared timeout
- **AND** the stated bound MUST NOT be the contract's validated maximum where the adapter declares something shorter

#### Scenario: The subject has moved past the abstract's digest
- **WHEN** the subject document's content no longer matches the digest its abstract was generated from
- **THEN** the abstract MUST be shown, labelled stale, with its source digest stated
- **AND** it MUST NOT be silently discarded or presented as current

#### Scenario: An unloaded subject's digest is taken
- **WHEN** the subject is a document that is not a loaded buffer
- **THEN** the source digest MUST be the digest of the served saved content
- **AND** the per-buffer settled-content-identity guard MUST NOT be required of it

#### Scenario: The RE-GENERATE control is invoked on an already-generated abstract
- **WHEN** a human invokes RE-GENERATE on a subject whose abstract is already completed for the current content digest and resolved model
- **THEN** the request MUST carry refresh intent and a second dispatch MUST occur
- **AND** the completed entry MUST NOT be replayed as the answer

#### Scenario: The gate capability is absent
- **WHEN** the docs context renders on a local console without the gate capability
- **THEN** the generation control MUST be absent rather than present-and-refusing
- **AND** any already-generated abstract MUST remain readable

### Requirement: The abstract request carries exactly one subject document
An abstract request SHALL carry EXACTLY ONE subject document's content and MUST NOT carry the layer-one context packet, another buffer, another document, a transcript, or a human message — with no human message in the prompt, the subject document's own content is the entire instruction-bearing text, and every additional document is both an injection surface and a disclosure the request has no reason to make. The request SHALL be assembled by its own non-chat assembler and MUST NOT be expressed as a chat turn: the chat assembler requires an outline buffer, one or more document buffers, a non-blank human message, a working subject and a transcript, none of which an abstract request has. The assembled prompt SHALL be BYTE-IDENTICAL for identical construction input, so a prompt is reviewable and a dispatch is reproducible. The response bound SHALL be tighter than the chat surface's assistant-prose ceiling, because the region that renders it is a fixed-height pane and an abstract that overflows it is not an abstract. Provider-bound content MUST NOT include a credential, a raw endpoint, a secret name, or unsaved buffer text.

#### Scenario: A request would carry the context packet
- **WHEN** a bounded context packet of ANY declared purpose, or any second document, is handed to the abstract assembler
- **THEN** the assembler MUST refuse it before any provider is reached
- **AND** the refusal MUST NOT depend on the packet's declared purpose, because an abstract request carries no packet at all

#### Scenario: The same subject is assembled twice
- **WHEN** the same subject document, content digest and model are assembled twice
- **THEN** the rendered prompt bytes MUST be identical

#### Scenario: An abstract request is offered as a chat turn
- **WHEN** an abstract request would be dispatched through the chat-turn assembler
- **THEN** it MUST be rejected — the request carries its own assembler and its own declared shape

### Requirement: The distilled abstract is verified against the document's own declared fields
A returned abstract SHALL be verified before it is rendered, and the verification base SHALL be the SNAPSHOT'S OWN declared fields for the subject document — its declared topics and its declared destinations — so the rule fires on the FIRST generation and not only on a regeneration; a previously generated abstract, where one exists, SHALL be an ADDITIONAL base and never the only one. The declared-field check SHALL be described as SUBJECT-MENTION COVERAGE and MUST NOT be described as a fidelity or faithfulness check, because a provider returns assistant prose as one opaque string and nothing downstream can establish that a mentioned subject was treated faithfully; a realization that claims otherwise MUST be rejected. The abstract SHALL name the subject document's path or title, and MUST NOT name any repository path absent from its own request — this is the one structural clause the response bytes can decide, and it refuses both a wrong-document answer and a leaked-neighbour answer. A verification failure SHALL be a stated refusal that renders no abstract, and MUST NOT be silently downgraded to rendering the unverified text. The verified artifact SHALL be structurally non-authoritative and SHALL record what it is regenerable from, in the manner of this surface's existing compacted-artifact type, and it MUST NOT reuse that type where that type's own commitment classes do not apply. The artifact SHALL also record the SUBJECT PATH, the SUBJECT CONTENT DIGEST and the RESOLVED MODEL ID it was produced from, and the recorded model id MUST be the model that actually answered — which is why those three are also the cache key, since a store that replayed one model's prose under another model's recorded id would make the artifact lie about its own provenance.

#### Scenario: An abstract mentions none of the declared subjects
- **WHEN** a returned abstract mentions no declared topic and no declared destination of its subject document
- **THEN** it MUST be refused and no abstract MUST be rendered

#### Scenario: An abstract names a foreign path
- **WHEN** a returned abstract names a repository path that its own request did not carry
- **THEN** it MUST be refused as a wrong-document or leaked answer

#### Scenario: Coverage is described as fidelity
- **WHEN** a realization or its documentation describes the declared-field check as verifying faithfulness
- **THEN** it MUST be rejected — the check is subject-mention coverage over one opaque string

#### Scenario: The first generation is verified
- **WHEN** the first abstract for a document is returned and no previous abstract exists
- **THEN** it MUST still be verified against the snapshot's declared topics and destinations

### Requirement: A model-derived abstract is session-local and never a snapshot field
A model-derived abstract SHALL be session-local and MUST NOT be written into the dashboard snapshot for as long as the snapshot's byte-identical guarantee stands, because keying a model value by content digest makes a CACHE stable and does not make a TREE reproducible — a cold cache, a substituted adapter, or a provider revision all change the bytes while the working tree does not. The observable SHALL hold in BOTH directions: an emitted snapshot MUST be byte-identical whether or not any abstract was generated, and no snapshot field MUST carry a model-derived value. Generation MUST NOT block, delay, or fail a snapshot, a publication lane, or a gate action; where the port raises, times out, or is absent, the snapshot MUST be unaffected and the region MUST state the not-yet-generated caption. On the hosted read-only plane, where no model-consuming route is offered, the region SHALL render the deterministic abstract and state that no distillation is available ON THAT PLANE — a statement about the plane and never about the document. Projecting an abstract into the snapshot in future SHALL require its own change amending the byte-identical scenario first, and MUST NOT be treated as an additive growth this requirement already permits.

#### Scenario: The generator runs on a tree with and without generation
- **WHEN** the generator runs over an unchanged working tree, once with abstracts generated in the session and once without
- **THEN** both snapshots MUST be byte-identical
- **AND** no snapshot field MUST carry a model-derived value

#### Scenario: The provider is absent or fails
- **WHEN** the model port is absent, raises, or exceeds its timeout
- **THEN** the snapshot MUST be unaffected and no lane or gate action MUST fail
- **AND** the region MUST state the not-yet-generated caption

#### Scenario: The hosted plane renders the docs context
- **WHEN** a viewer opens the docs context on the hosted read-only plane
- **THEN** the deterministic abstract MUST render and the region MUST state that no distillation is available on that plane

### Requirement: The abstract cache is a separate bounded store keyed by path, digest and model, and an explicit refresh bypasses it
An abstract cache SHALL be a SEPARATE, separately bounded store and MUST NOT share the chat surface's turn-idempotency ledger, whose per-process instance is bounded by entry count and total bytes and would evict chat records under abstract churn — a scope larger than that bound is the ordinary case, not an edge case. The cache key SHALL be composed of the subject's PATH, its CONTENT DIGEST, and the RESOLVED MODEL ID the request dispatched against, QUALIFIED BY the request's SCOPE — its REPOSITORY and REF — so no key is ever shared across scopes. The digest MUST be in the key so a regeneration after an edit is a NEW key rather than a same-key conflict; a store that refused a changed digest under an unchanged key would refuse every regeneration after every edit. The RESOLVED MODEL ID MUST be in the key because this surface lets a human change the selected model while the document stands still: on a path-and-digest key that second request is identical, so the first model's answer would replay while the artifact records the newly selected model — a claim the artifact's own recorded model id makes false on its face, and one the provider boundary's rule that every consumer resolves a catalog model id forbids. Where the selected entry is a ROUTING RULE rather than a single provider model, the key SHALL carry the RESOLVED model id and not the rule's id, for the same reason a turn records the model that actually answered. The cache SHALL admit at most ONE in-flight generation per key, with a concurrent request for the same key attaching to it rather than dispatching a second time. A request carrying NO REFRESH INTENT SHALL replay a completed result for an identical key without a second dispatch — this is the path that makes an abstract survive leaving and re-entering the tile. A request carrying an EXPLICIT REFRESH INTENT — which is what the RE-GENERATE control issues — SHALL BYPASS completed replay: it SHALL invalidate the completed entry for its key, dispatch again, and its result SHALL replace that entry. Without that bypass the RE-GENERATE control would be INERT for the ordinary case it exists for, because a regeneration against unchanged content and an unchanged model has an identical key. A refresh intent MUST NOT open a second in-flight generation where one is already in flight for the same key: a second invocation attaches to the first, so an impatient double-click spends one model call and not two, and refresh intent MUST NOT be inferred from a selection change, a mount, a re-entry, or any other event that is not the human control being invoked. Eviction SHALL be deterministic and MUST NOT be ordered by wall-clock time, and a re-dispatch after eviction SHALL be stated expected behaviour rather than an error. Nothing in the cache SHALL be authoritative, and its contents MUST NOT outlive the session or be written to any corpus, snapshot, register, or gate artifact.

#### Scenario: Abstract churn over a large scope
- **WHEN** abstracts are generated across a scope holding more documents than the cache bound
- **THEN** eviction MUST be deterministic and re-dispatch after eviction MUST be expected behaviour
- **AND** the chat surface's turn-idempotency records MUST NOT be evicted by abstract activity

#### Scenario: The subject is edited and regenerated
- **WHEN** a subject document changes and an abstract is requested again
- **THEN** the request MUST be treated as a new key rather than refused as a conflict

#### Scenario: Two requests race for one subject
- **WHEN** a second request arrives for a key whose generation is in flight
- **THEN** it MUST attach to the in-flight generation rather than dispatching a second time

#### Scenario: RE-GENERATE is invoked on an unchanged document with an unchanged model
- **WHEN** a human invokes the RE-GENERATE control and neither the subject's content digest nor the resolved model has changed since the completed entry
- **THEN** the completed entry MUST be invalidated and a second dispatch MUST occur
- **AND** the new result MUST replace that entry rather than being discarded as a duplicate

#### Scenario: RE-GENERATE is invoked twice before the first resolves
- **WHEN** the RE-GENERATE control is invoked a second time while its own generation is still in flight for the same key
- **THEN** the second invocation MUST attach to the in-flight generation rather than dispatching a third time

#### Scenario: The selected model changes while the document stands still
- **WHEN** an abstract is requested for a subject whose content digest is unchanged but whose resolved model id differs from the completed entry's
- **THEN** it MUST be treated as a DIFFERENT key and MUST dispatch against the newly resolved model
- **AND** the first model's result MUST NOT be replayed under the new model's identity

#### Scenario: Re-entering the tile is not a refresh
- **WHEN** a reader leaves the tile and returns to a subject whose abstract is already generated, with no control invoked
- **THEN** the completed result MUST replay with no second dispatch
- **AND** refresh intent MUST NOT be inferred from the re-entry

### Requirement: One abstract region, named for its subject and its provenance
The `docs` context SHALL carry EXACTLY ONE abstract region, presenting ONE abstract at a time — switched by an explicit control, opening on the DETERMINISTIC one — because the upper half of the docs split carries a measured fixed height that two regions cannot share and the deterministic abstract is the only one that always exists. That region's ACCESSIBLE NAME SHALL be composed of the SUBJECT's title or path together with the provenance caption of the state currently shown, so a reader using assistive technology can tell WHICH DOCUMENT and WHICH PROVENANCE they have landed on from the name alone, and the deterministic and model-derived states are distinguishable without reading the body. The region MUST NOT be named `selected document` or otherwise announced as the selected buffer: that name belongs to the loaded-document selector, and two surfaces claiming one name is how the two come to disagree. Each state SHALL carry its own caption declaring who derived it and what it is not — the model-derived abstract as model-derived, non-authoritative and regenerable; the deterministic abstract as derived from the document's own headers, and NEVER as a distillation; a stale abstract as describing an earlier version, with the source digest stated; an ungenerated abstract as not yet generated; and, on the hosted plane, as unavailable on that plane. The model-derived and deterministic captions SHALL be BOTH visible text and part of the region's accessible name; the stale, ungenerated and hosted-plane captions SHALL be visible text inside the already-named region. The region SHALL follow this surface's established idiom — a named `role=region` carrying no heading of its own, in the surface's exact casing. No caption SHALL describe the model-derived abstract in terms that imply it may be cited.

#### Scenario: Both abstracts exist for one subject
- **WHEN** a subject has both a deterministic and a model-derived abstract
- **THEN** exactly ONE abstract region MUST exist and exactly one abstract MUST render at a time, switched by an explicit control
- **AND** the deterministic abstract MUST be the opening view

#### Scenario: A reader lands on the region with assistive technology
- **WHEN** a reader enters the abstract region with assistive technology
- **THEN** the region's accessible name MUST carry both the subject's identity and the provenance of the state shown
- **AND** it MUST NOT be announced as the selected document

#### Scenario: The provenance state changes
- **WHEN** the region switches between the deterministic and the model-derived abstract for one subject
- **THEN** the accessible name MUST change with it, so the two states are distinguishable by name

#### Scenario: A caption implies citability
- **WHEN** a caption describes the model-derived abstract as a summary of record, an authoritative account, or otherwise citable
- **THEN** it MUST be rejected

