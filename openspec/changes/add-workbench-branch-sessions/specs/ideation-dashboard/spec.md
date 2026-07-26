# ideation-dashboard Delta: Branch Sessions, Commit-Per-Gate-Action, PR-As-Save

## ADDED Requirements

### Requirement: Branch session lifecycle
The workbench SHALL open a BRANCH SESSION on a topic-bearing tile the first time a gate write is performed against that tile, and the session's working state SHALL live on a git branch materialized as a git WORKTREE rather than in the served checkout. The session branch name SHALL be derived deterministically from the TILE's scope identity — `draft/<staging-id>` for a staged topic, and the scope's kind and id for a cluster or a possible — never from the actor, so two humans working the same tile join the SAME session rather than forking two. The served checkout MUST NEVER be switched, reset, stashed, or otherwise moved by any session operation: session writes reach the branch only through its own worktree, which dissolves the shared-checkout hazard by construction rather than by discipline. A branch session SHALL end in exactly one of two ways — its pull request MERGES, or a human explicitly ABANDONS it — and on either ending the worktree, the session's snapshot registry entry, and the session notebook SHALL be torn down and the main view refreshed. On a MERGE the session BRANCH SHALL ALSO be deleted: the work is saved on `main`, so the branch holds nothing the merge did not preserve, and a surviving branch would only contend for its own deterministic name when the tile is worked again. An abandon SHALL be a recorded human gate action carrying a reason, MUST end only the SESSION, and MUST NOT delete history that has already been pushed or close a pull request on the human's behalf — a pushed branch and its PR remain reviewable evidence, and an abandoned session is RESOLVED even though its branch may survive. A BRANCH session is distinct from the workbench's UI-lifetime "workbench session" that scopes the checked-keyword selection: a branch session outlives page loads, spans actors, and is ended only by a merge or an abandon.

#### Scenario: The first gate write on a tile opens a session
- **WHEN** a human performs the first gate write against a topic-bearing tile that has no active branch session
- **THEN** a session branch named from that tile's scope identity MUST be created and materialized as a git worktree
- **AND** the write MUST land in that worktree, not in the served checkout

#### Scenario: A second human opens the same tile
- **WHEN** another human performs a gate write against a tile that already has an active branch session
- **THEN** they MUST join the EXISTING session on the same branch rather than opening a second session
- **AND** the branch name MUST NOT encode either actor

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
The gate console SHALL offer a human-only `edit-document` verb that is valid ONLY inside an active branch session, and it MUST refuse any invocation that names no session branch, targets a document outside that session's worktree, or is reached with no active session at all. The verb SHALL rewrite an EXISTING document in the session worktree and commit the rewrite as that action's single commit, MUST NOT create a document (that stays `create-document`) and MUST NOT delete one by any path. No per-edit redline ceremony SHALL be required of an on-branch edit, because THE PULL REQUEST REVIEW IS THE GOVERNANCE — the ratified gates-happen-on-main rule already holds that an unmerged transition is exploration and not status, which makes an unmerged branch precisely the place where ordinary editing is legal. The gate console's `edit-apply` redline path SHALL REMAIN UNCHANGED as the path for editing a MAIN-RESIDENT document outside a session: that is a different act with a different risk profile and it keeps its ceremony. The `create-document` verb SHALL keep its create-only semantics unchanged and, inside a branch session, SHALL write into the session worktree instead of the served checkout. The verb MUST be loopback-only, MUST fail closed on an unresolved actor, and MUST reject and report any agent or automated invocation, like every gate action.

#### Scenario: A document is edited inside a session
- **WHEN** a human invokes `edit-document` on a document in an active session's worktree
- **THEN** the document MUST be rewritten in that worktree and committed as that action's single commit with its gate-action record
- **AND** no redline artifact MUST be required before the edit lands

#### Scenario: Editing is attempted outside a session
- **WHEN** `edit-document` is invoked with no active branch session, or against the served checkout's `main`
- **THEN** it MUST refuse and persist nothing — main-resident editing stays the `edit-apply` redline path

#### Scenario: An edit targets a path outside the worktree
- **WHEN** `edit-document` names a path that does not resolve inside the active session's worktree root
- **THEN** it MUST refuse and persist nothing

#### Scenario: A session edit is asked to delete
- **WHEN** `edit-document` is invoked in a way that would remove a document
- **THEN** it MUST refuse — the verb rewrites, and no session verb grants delete authority

#### Scenario: Creating inside a session
- **WHEN** `create-document` is invoked while a branch session is active on the tile
- **THEN** the document MUST be created in the session worktree with the create-only semantics unchanged, and committed as that action's single commit

#### Scenario: An agent invokes the edit verb
- **WHEN** any agent or automated path calls `edit-document`
- **THEN** the call MUST be rejected and reported

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
The gate console SHALL offer a human-only `open-pr` verb that SAVES a branch session by pushing the session branch and opening a pull request into the EXISTING Merge-Master review ritual, recording the dispatch as a gate-action record that names the session branch and references the pull request as a `pull-request`-kind artifact. The verb SHALL create NO new approval path and grant NO authority: it MUST NOT merge, approve, self-review, or bypass any branch protection, and the merge remains the Merge Master's action under the existing ritual. The verb MUST NOT require the topic's readiness recommendation gate to have fired: a session pull request is exploration offered for review, and the readiness gate guards PROPOSE, not SAVE. Invoking the verb on a session that already has an open pull request SHALL update and report that pull request rather than opening a second one for the same branch. On merge the documents become governed content on `main`, the publication lane reflects them on its own schedule, and the session tears down as its lifecycle requires. The verb MUST be loopback-only, MUST fail closed on an unresolved actor, and MUST reject and report any agent invocation.

#### Scenario: A session is saved
- **WHEN** a human invokes `open-pr` on an active branch session
- **THEN** the branch MUST be pushed, a pull request MUST be opened into the existing review ritual, and a gate-action record MUST name the branch and reference the pull request as a `pull-request`-kind artifact

#### Scenario: The save verb is asked to merge
- **WHEN** any path would have `open-pr` merge, approve, or bypass protection on its own pull request
- **THEN** it MUST be refused — saving hands work to the Merge-Master ritual and holds no approval authority

#### Scenario: A session without a passing readiness gate is saved
- **WHEN** a human invokes `open-pr` on a session whose topic carries no fired readiness recommendation
- **THEN** the save MUST proceed — a session pull request is exploration, and the readiness gate is a precondition of proposing, not of saving

#### Scenario: The verb is invoked twice
- **WHEN** `open-pr` is invoked on a session that already has an open pull request
- **THEN** it MUST update and report the existing pull request and MUST NOT open a second one for the same branch

#### Scenario: A saved session merges
- **WHEN** the session's pull request merges
- **THEN** the documents MUST be governed content on `main`, the session MUST tear down, and the main view MUST refresh

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

## MODIFIED Requirements

### Requirement: Staging workbench scoped view
The dashboard SHALL provide a staging workbench: a full-screen view scoped to exactly ONE topic-bearing tile — a cluster, a possible, or a staged topic — presenting three tabbed panels over that one scope. The `docs` panel SHALL list the tile's document set derived strictly from the snapshot's own edges (a cluster's `document_edges`; a possible's `supporting_evidence` documents, with any claiming-cluster member documents shown as a separately labelled inherited section, never conflated with cited evidence; a staged topic's files that are corpus documents plus every document whose `destinations.staged_topics` names it, plus — Brett's 2026-07-25 dogfood ruling — the member documents of the topic's linked clusters as a THIRD, separately labelled cluster-neighbourhood section, inherited via clusters, never conflated with the topic's own material, and never an input to the topic's health or the readiness gate, which stay folder-scoped) and SHALL render each row's completeness bar and named signals verbatim from the snapshot, never recomputing them. The `lens` panel SHALL render interconnectedness scoped to that tile's keywords and documents by RE-SCOPING the existing keyword-lens and edge-degree derivation — the same `keyword_index` seed and the same edge/degree computation the funnel and wheel already use, filtered to the tile's scope — and MUST NOT introduce a new analysis, a new score, or a new snapshot field. The `outline` panel SHALL render the topic's outline when one exists — for a staged topic, the fragment's outline material — read through the same read-only `/source` pass-through the document viewer uses, and MUST show an explicit empty state when the scope carries no outline. The workbench's write authority SHALL be the human-only gate verbs `create-document`, `edit-document`, `open-pr`, and the session abandon, and OUTSIDE an active branch session it SHALL be `create-document` alone: it MUST write no register entry, no workbench manifest, and no gate artifact beyond those verbs' own gate-action records; outside a branch session it MUST NOT modify or delete any existing document, in any panel, by any path; INSIDE a branch session `edit-document` MAY rewrite an existing document in the SESSION WORKTREE while no verb MAY delete one, and no session write ever touches the served checkout; and an in-panel outline EDITOR remains out of scope — the `outline` panel stays a read-only rendering, and a session edit reaches the underlying document through `edit-document` like any other document. With the gate capability absent the workbench SHALL be read-only in every panel, as it is on the served static image.

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

#### Scenario: An existing document is modified outside a session
- **WHEN** any workbench panel would edit or delete an existing corpus document with no active branch session, or write a register entry, a workbench manifest, or any gate artifact other than the session verbs' own gate-action records
- **THEN** the write MUST be rejected and reported — outside a session the workbench's only write is the create-only gated document creation

#### Scenario: An existing document is edited inside a session
- **WHEN** a human edits an existing document through `edit-document` inside an active branch session
- **THEN** the rewrite MUST land in the session worktree as that action's single commit
- **AND** the served checkout MUST remain untouched

#### Scenario: The workbench renders without the gate capability
- **WHEN** the workbench runs on a surface where the gate capability is absent
- **THEN** every panel MUST be read-only and no write MUST be reachable from the page

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

#### Scenario: Propose is invoked with a live branch session on the tile
- **WHEN** propose is invoked for a topic whose tile holds a live branch session
- **THEN** the console MUST refuse and persist nothing, naming the session branch and offering both resolutions — merge the session's pull request, or abandon the session
- **AND** the refusal MUST clear once the session ends by either route, with no further action required of the human

#### Scenario: A previously abandoned session leaves a branch behind
- **WHEN** propose is invoked for a topic whose session was abandoned but whose pushed branch still exists
- **THEN** propose MUST proceed — the session is resolved, and the surviving branch is reviewable evidence rather than unresolved working state
