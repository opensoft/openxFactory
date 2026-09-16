# openxfactory-engineering-adapter Specification

This delta is the RE-PROMOTION half of `split-opendox-two-layer-product` § 5.2a: the
FIFTEEN engineering-vocabulary requirements that leave the capability
`ideation-dashboard` and STAY IN THIS REPOSITORY under **RULING DQ-1**
(`opensoft/openxFactory` issue #656, 2026-09-04T22:14Z, comment `5547049745`) land here,
under the successor capability of the adapter § 2.2a stood up — one conformant
implementation of openDox's corpus-adapter seam over this repository's own corpus,
`scripts/corpus_adapter_openxfactory/`, landed by #725 → `ea4e6ff2`.

**THE FIFTEEN ARE NOT AUTHORED HERE; THEY ARE CARRIED.** Each requirement below was
lifted from `openspec/specs/ideation-dashboard/spec.md` BY TITLE rather than by line or
by hand, and carries every byte of its promoted text except at the SIX sites
`design.md` § D2 discloses, where a path literal becomes the seam operation that answers
for it. Titles are therefore character-for-character identical to the promoted spec — the
same discipline the packet's own removal block states for the same reason:
`scripts/doc_health/promotion_fidelity.py` keys on (capability, normalized title), so
the successor is a DISTINCT key, this re-promotion masks nothing, and the packet's
`## REMOVED` delta stays visible to the checker.

**THIS DELTA REMOVES NOTHING.** The departure from `ideation-dashboard` is the packet's
own ratified per-requirement map — 71 openDox / 16 openXdox / 15 openxFactory, ratified
2026-09-05T01:38Z — and that map is the single writer of the removal. See `design.md`
§ D3 for why a second `## REMOVED` block over the same fifteen titles is refused here.

## ADDED Requirements

### Requirement: Staged-topic proposal commissioning
The gate console SHALL offer a human-only `propose` action on a staging topic that commissions proposal authoring as a recorded dispatch — a `workflow-job` descriptor naming the proposal-authoring workflow and targeting the topic's staging id, plus a gate-action record — without authoring anything itself; the commissioned authoring runs externally and lands as an ordinary OpenSpec change subject to the existing review and ratify gates. The console SHALL refuse a topic absent from the pinned checkout's staging area and SHALL refuse a duplicate commission while a dispatched `propose` job for the same topic remains undelivered. The console SHALL ALSO refuse `propose` while the topic's tile carries an UNRESOLVED branch session, and the refusal MUST name the session and the two resolutions available — merge its pull request, or abandon the session to discard it. Proposal is the end of the staging pipeline: commissioning it from a tile whose drafts are still scattered across an unmerged branch would propose from a state no reviewer can see, so the human SHALL clear the session first. A session is UNRESOLVED while its snapshot registry entry is live; a merged session and an abandoned session are both resolved, and a branch surviving an abandon MUST NOT block propose, because the abandon already recorded the human's decision to discard.

An abandoned branch SHALL remain reviewable evidence until a human invokes cleanup with a durable RETENTION-RELEASE basis. The console SHALL accept an exact-tile active proposal, an archived change carrying that exact staged origin, or an executed demotion returning the proposal to that exact tile as machine-resolved preservation evidence. A demotion plan, proposal dispatch, missing change, missing worktree, missing tile, or non-live session state MUST NOT itself release retention. Demotion execution SHALL be proved by a durable execution receipt for new demotions; a pre-receipt demotion MAY be accepted only when the exact transition manifest and an exact returned-topic artifact jointly prove execution.

Where no machine-resolved preservation evidence exists, cleanup MAY proceed only through an explicit human retention release carrying a nonblank reason. This lane SHALL support staged-topic, cluster, possible, missing, renamed, and otherwise orphaned tile identities without inferring that absence is disposition. Every successful cleanup SHALL remain human-invoked, local-only, and non-automatic; SHALL verify the branch belongs to the supplied tile, the session is not live, no worktree is attached, and a durable `abandon-session` proof names the ref; and SHALL write a main-resident cleanup record naming the exact tile scope, pre-delete head, abandonment proof, retention-release evidence, and reason where explicitly supplied. A failed deletion MUST NOT leave a record claiming success.

#### Scenario: A staged tile is taken toward proposal
- **WHEN** a human runs the propose action on a staging topic
- **THEN** a `workflow-job` descriptor (workflow `proposal-authoring`, target `topic_id`) and a `propose` gate-action record are written through the human gate
- **AND** no proposal artifact is authored by the console itself

#### Scenario: A missing topic is refused
- **WHEN** propose is invoked for a topic id the corpus adapter's `list_documents` returns nothing for in the pinned checkout's staging area
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
The gate console SHALL offer a human-only `promote-to-staging` action on a possible that commissions the organization of that possible into a staging topic of the corpus the adapter resolves, as a fragment — a `workflow-job` descriptor naming the staging-fragment authoring workflow and targeting the possible's register id (optionally carrying a proposed topic slug), plus a `promote-to-staging` gate-action record — and the console MUST NOT author the fragment or mutate the possibles register: the possible's `latent → picked` pick edge is recorded only when the commissioned fragment is delivered, never at commission time. Promotion SHALL presuppose an accepted disposition — the console MUST refuse a derived possible still `pending_review` (it must be disposed first), a `rejected` or `superseded` possible, an already-`picked` possible, and a register id absent from the pinned checkout — and MUST refuse a duplicate commission while a dispatched `promote-to-staging` job for the same possible remains undelivered.

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

### Requirement: doxBench resolves its released contract from the checkout it runs in
The dashboard runtime SHALL resolve the pinned doxBench wire schemas from the repository it is running in whenever that repository is itself a publisher release, and MUST NOT reach a sibling checkout in preference to its own tree. Resolution precedence SHALL be, highest first: an explicitly supplied checkout; the `OPENXFACTORY_ROOT` operator override; the hosting repository when it carries the publisher markers; then the corpus adapter's `resolve` of the aggregation-relative home corpus; and a refusal when none of those yields a checkout. Only the third rung is new, and no rung above or below it moves.

A serve MUST verify contracts against the tree it was launched from. The path this replaces searched one level below where it stood, so from inside the publisher it walked past itself every time and landed on the aggregation's submodule checkout — a shared tree that sessions move between branches — which meant a serve started from one worktree could verify its wire shapes against another session's working state. That this has so far been harmless is a property of two files not having changed, not a guarantee anything makes.

The runtime's pinned release SHALL name the release the repository currently publishes, and a repin MUST carry the digests that release's own manifest records. Where the schema bytes are unchanged across the releases spanned, the repin SHALL be digest-neutral: it re-declares which release is read and changes no verified byte, so no conformance question reopens.

The two model routes SHALL keep their current refusal shape and their current gate order. A route that cannot read the contract MUST still refuse before consulting any port, MUST still emit only the fixed catalog code, and MUST NOT let a pin diagnostic — which names checkout paths and digests — reach the wire. Recovery comes from the resolution beneath the routes succeeding, never from a route relaxing what it refuses.

The honest empty-catalog posture SHALL remain distinct from a contract failure. A plane with no configured model provider MUST receive a conformant empty catalog as a SUCCESS, and MUST NOT be served the refusal that means the contract could not be read — the two say different things to an operator and MUST NOT be collapsed.

#### Scenario: The model routes are served from a publisher checkout
- **WHEN** the dashboard serves from an openxFactory checkout carrying the publisher markers
- **THEN** the released schema validators MUST resolve from that same checkout
- **AND** the model catalog and chat-turn routes MUST NOT refuse for want of a declared consumption pin

#### Scenario: A sibling checkout is not preferred over the running tree
- **WHEN** the hosting repository is a publisher release and an aggregation-relative home corpus the adapter could resolve also exists
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

### Requirement: Demote refreshes a staged topic's outline and never silently replaces it
The reverse transition SHALL leave the demoted topic's primary fragment carrying the ACTUAL text of the last attempted `proposal.md` and the demoted change's own provenance, and MUST NOT reset that fragment to the pre-proposal aspirational snapshot the change folder holds. The primary fragment is the file the existing deterministic, path-only selection already names; this requirement adds no second candidate file and MUST NOT change that selection.

A returning file whose destination is the topic's declared primary fragment SHALL keep `Status: staged`. It MUST NOT be flipped to `Status: draft`: the same selection rule still calls that file the staged topic's outline, so a draft status there makes the document disagree with every reader of it. The `Status: draft` flip remains correct and unchanged for the proposal documents returning to the topic's OpenSpec workspace.

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
- **AND** the proposal documents returning to the topic's OpenSpec workspace MUST still continue as `Status: draft`

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

### Requirement: Convergent lens regions draft candidate-register seeds
The dashboard SHALL draft a domain-neutralization candidate-register seed from a repository-lens region carrying two or more repositories, because such a region is the promotion process's first candidate rule — two or more domain repositories carrying the same structure — computed rather than eyeballed. A region with a single carrier SHALL NOT be draftable and SHALL say why. The draft SHALL be produced in the register's own format: a Candidate List row and a `### DTN-NNN:` detail section, numbered past every identifier the register mentions so a drafted-but-unmerged seed never collides, quoting the rule it satisfies and listing each identity with its carriers as the evidence — the carrier set IS the evidence for this rule, so the draft SHALL be deterministic and involve no model judgment.

The drafting SHALL write nothing. The register is never opened for writing and a candidate enters the register lifecycle only when a human merges the seed, which is the same seed-first discipline the machine-drafted intake path already records; because nothing is written, the affordance SHALL remain available on a composed read-only view and SHALL NOT claim a gate capability. The evidence SHALL be recomputed by the serving side from its own composed view — the client names the project, the visible member set, and the region's carrier combination, never the identities — and a seed SHALL cover exactly the region it was drafted from rather than everything the wider visible set happens to share.

#### Scenario: A convergent region drafts a seed
- WHEN a human drafts from a lens region whose identities two or more repositories carry
- THEN the response is a register-format row and detail section naming those identities and their carriers, numbered from the register's own numbering
- AND the register file is unchanged

#### Scenario: A seed covers exactly its region
- WHEN the region is a sector naming an exact repository combination
- THEN the drafted seed covers the identities whose carriers are exactly that combination, and no others

#### Scenario: A single-carrier region cannot be drafted
- WHEN a region's identities are carried by only one repository
- THEN the draft affordance is unavailable and states that a candidate needs two or more carriers

#### Scenario: A plane that cannot compose has no candidates
- WHEN the drafting route is asked about a project with no composed view
- THEN it refuses and names the project, rather than drafting from a single repository's documents
