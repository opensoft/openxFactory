# review-lane-floor-mirror

## MODIFIED Requirements

### Requirement: An automated pin advance only ever proposes

An automated lane that advances this repository's pinned decision core MUST propose the advance as a pull request and MUST NOT dispose of it by its own act: it SHALL NOT merge by its own act and SHALL NOT approve; it MAY arm the platform's auto-merge on that same pull request, so that the merge completes only when (a) the merge-master envelope approval for that exact head stands and (b) every required check has succeeded; and it SHALL NOT push to this repository's default branch, and SHALL NOT hold any authority over the pin that the equivalent hand act does not already have.

The pull request SHALL move the pin and nothing else: no unrelated file, no documentation line, no formatting change, and no edit to the checks that judge it. This requirement composes with, and does not restate, the requirement "The mirror is inert until the pin carries the rule, and the pin moves as one act": that requirement governs WHAT one advance must contain, and this one governs who may author it and what else it may not contain.

The arming is a request to the platform and never a merge. The lane SHALL arm nothing but the platform's own auto-merge, on its OWN pull request, at a merge method this repository already permits, and it SHALL NOT reach the merge by any other path: no administrative override, no direct call to a merge endpoint, no merge queue this repository has not declared, no dismissal or solicitation of a review, no closing or reopening of the pull request, and no second act TOWARD THE MERGE after the arming. The default-branch bar is a bar on the LANE'S OWN WRITES and is unchanged by this rule: a merge the platform completes under this repository's own rules is not a push by the lane, and the lane SHALL still make no direct write to the default branch.

WHAT IS FORBIDDEN AFTER THE ARMING IS DISPOSAL, NEVER DELIVERY, and this requirement SHALL NOT be read as closing the update path its own capability requires. The requirement "The automated advance lane is triggered by the pinned core's own movement and every firing is idempotent" obliges the lane to keep at most one advance pull request open and to bring an open one up to date rather than open a second; where a further advance is owed while an ARMED pull request is still open, the lane SHALL take that same update path and SHALL re-arm the platform's auto-merge on that pull request idempotently. An update is the lane's ordinary delivery act, is bounded by everything this requirement already says about what an advance may carry, and does not become a disposal act by arriving after an arming. What may not follow the arming is a SECOND ROUTE TO THE MERGE, and a re-arming is the same one route restated.

WHAT BECOMES OF THE ARMED STATE ON AN UPDATE IS THE PLATFORM'S ANSWER, NOT THIS LANE'S, and the lane SHALL make it true rather than assume it. GitHub disables an armed auto-merge when new changes are pushed to the head branch by an actor WITHOUT write permission to the repository; an actor that holds write permission does not disable it by pushing. The lane's declared credential binding SHALL therefore state the permission its arming relies on, and the re-arming SHALL be performed on every delivery regardless of what the previous state was, so that an armed intent the platform dropped is restored on the next firing and an intent still standing is left exactly as it is. THE APPROVAL IS A SEPARATE QUESTION AND MOVES THE OTHER WAY: an update moves the head, and this repository's rules dismiss a review on push and require the last push to be approved, so the merge SHALL wait for an approval naming the new head — the scenario "A head that moves after an approval is not merged on that approval", which an update reaches by design rather than by defect.

Where a rule the pull request must satisfy is unsatisfied, the armed auto-merge SHALL simply not complete: the lane SHALL NOT widen a rule, add itself or any other actor to a bypass list, remove any path from the never-clearable floor, enrol itself in any approval envelope, or re-arm with a stronger act; and an armed pull request that cannot complete SHALL remain a proposal awaiting the same hand a hand-authored advance would need. An arming that can never complete under the machinery in force is a CONFORMING state of this requirement and SHALL be reported as such rather than treated as a failure or as progress.

The approval that releases the merge SHALL be another party's and SHALL bind to the head it was given for. The lane SHALL NOT approve its own pull request under any identity; where the pull request's head moves after an approval, the merge SHALL NOT complete until an approval naming the new head stands. A lane that has armed auto-merge SHALL report that it armed, naming the pull request and the head it armed at, so that an armed proposal is never distinguishable from an unarmed one only by consulting the platform.

**Modified over `mirror-floor-regeneration-automation`'s addition by amend-mirror-floor-regeneration-merge-authority (2026-09-08):** — the requirement this block restates is not in canon: it is ADDED by the ACTIVE change `mirror-floor-regeneration-automation`, which is ratified (2026-09-06, PR #708) but not yet archived, so the basis is a sibling's addition rather than a promoted specification. The pairing is declared here per requirement, as `govern-sibling-added-modified-deltas` requires, and the archive order follows from it: this packet SHALL NOT archive until that change promotes, which `.openspec.yaml`'s `related` entry and the `sequenced_after` front matter already record.

#### Scenario: The lane opens a pull request and stops there
- **WHEN** the automated lane has a pin advance to deliver
- **THEN** it opens a pull request carrying that advance and takes no further action on it beyond arming the platform's auto-merge on that same pull request
- **AND** it neither merges by its own act nor approves that pull request

#### Scenario: An envelope-approved, fully green pin advance merges with no human act
- **WHEN** the lane has armed the platform's auto-merge on its pull request, the merge-master envelope approval stands for that exact head, and every required check has succeeded
- **THEN** the platform completes the merge with no human review and no human click
- **AND** the lane performs no act at merge time, its last act having been the arming

#### Scenario: A parked pin advance is not merged
- **WHEN** the merge-master envelope parks the lane's pull request rather than approving it
- **THEN** the armed auto-merge does not fire and the pull request stays open, waiting exactly as an unarmed one would
- **AND** the lane takes no further act to move it

#### Scenario: A further advance owed while the armed pull request is parked updates it and re-arms
- **WHEN** a further pin advance is owed while the lane's armed pull request is still open and unmerged
- **THEN** the lane brings that same pull request up to date rather than opening a second one, and re-arms the platform's auto-merge on it
- **AND** the update and the re-arming are the only acts it takes, and any approval that named the superseded head no longer releases the merge

#### Scenario: A head that moves after an approval is not merged on that approval
- **WHEN** the pull request's head moves after an approval was given for the previous head
- **THEN** the armed auto-merge does not complete
- **AND** the merge waits for an approval that names the new head

#### Scenario: The lane never posts an approval
- **WHEN** the lane's pull request needs an approving review to satisfy this repository's rules
- **THEN** that approval comes from another party and never from the lane
- **AND** the lane submits no review of any kind on its own pull request

#### Scenario: No mechanism can release the arming, and the lane says so
- **WHEN** no candidate class admits the lane, or a never-clearable path the advance writes is composed over the approval envelope, or the reviewer a rule names is an identity the approving party cannot be
- **THEN** the armed auto-merge stays armed and never completes, and the pull request waits for the same hand a hand-authored advance would need
- **AND** the run states that the arming cannot complete and why, and the lane neither widens the rule nor grants itself or the approving identity a bypass of it

#### Scenario: The arming is reported where the run is read
- **WHEN** the lane arms the platform's auto-merge on its pull request
- **THEN** the run states that it armed, naming the pull request and the head it armed at
- **AND** a reader of the run can tell an armed proposal from an unarmed one without consulting the platform

#### Scenario: The lane never writes to the default branch
- **WHEN** the automated lane has a pin advance to deliver
- **THEN** it delivers it on a branch and through a pull request
- **AND** it makes no direct write to this repository's default branch

#### Scenario: The advance carries nothing but the advance
- **WHEN** the automated lane's pull request is read
- **THEN** every changed file is one of the sites that name the pinned core commit
- **AND** no other file in the repository is changed by it
