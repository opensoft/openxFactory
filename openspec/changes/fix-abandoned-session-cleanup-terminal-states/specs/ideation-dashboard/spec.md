## MODIFIED Requirements

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
