# review-lane-floor-mirror

## MODIFIED Requirements

### Requirement: An automated pin advance only ever proposes

An automated lane that advances this repository's pinned decision core MUST propose the advance as a pull request and MUST NOT dispose of it by its own act: it SHALL NOT merge by its own act and SHALL NOT approve; it MAY arm the platform's auto-merge on that same pull request, so that the merge completes only when (a) the merge-master envelope approval for that exact head stands and (b) every required check has succeeded; and it SHALL NOT push to this repository's default branch, and SHALL NOT hold any authority over the pin that the equivalent hand act does not already have.

The pull request SHALL move the pin and nothing else: no unrelated file, no documentation line, no formatting change, and no edit to the checks that judge it. This requirement composes with, and does not restate, the requirement "The mirror is inert until the pin carries the rule, and the pin moves as one act": that requirement governs WHAT one advance must contain, and this one governs who may author it and what else it may not contain.

The arming is a request to the platform and never a merge. The lane SHALL arm nothing but the platform's own auto-merge, on its OWN pull request, at a merge method this repository already permits, and it SHALL NOT reach the merge by any other path: no administrative override, no direct call to a merge endpoint, no merge queue this repository has not declared, no dismissal or solicitation of a review, no closing or reopening of the pull request, and no second act after the arming. The default-branch bar is a bar on the LANE'S OWN WRITES and is unchanged by this rule: a merge the platform completes under this repository's own rules is not a push by the lane, and the lane SHALL still make no direct write to the default branch.

Where a rule the pull request must satisfy is unsatisfied, the armed auto-merge SHALL simply not complete: the lane SHALL NOT widen a rule, add itself or any other actor to a bypass list, remove any path from the never-clearable floor, enrol itself in any approval envelope, or re-arm with a stronger act; and an armed pull request that cannot complete SHALL remain a proposal awaiting the same hand a hand-authored advance would need. An arming that can never complete under the machinery in force is a CONFORMING state of this requirement and SHALL be reported as such rather than treated as a failure or as progress.

The approval that releases the merge SHALL be another party's and SHALL bind to the head it was given for. The lane SHALL NOT approve its own pull request under any identity; where the pull request's head moves after an approval, the merge SHALL NOT complete until an approval naming the new head stands. A lane that has armed auto-merge SHALL report that it armed, naming the pull request and the head it armed at, so that an armed proposal is never distinguishable from an unarmed one only by consulting the platform.

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
