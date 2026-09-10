# review-lane-floor-mirror — delta

## ADDED Requirements

### Requirement: The re-pin lane is enrolled as one named candidate class over its four writable files
An autonomous approval envelope that admits this repository's automated pin advance SHALL admit it as ONE named candidate class whose author identity, head reference, base reference and writable path set are the values that lane's already-observed pull requests carried, and SHALL name each writable path EXACTLY rather than by a directory-wide pattern, so that a pull request differing from the lane in any of those respects matches no class and waits for a human merge word.

The class SHALL require every non-excluded check on the head to be green, excluding at minimum the approval workflow's own check-run, so that the lane's own judges of the advance — including the freshness verifier that runs against the core the pull request PROPOSES — are conditions of the approval rather than facts about it. The declaration SHALL be readable from the base branch alone and SHALL be routed to a human code owner, so that a pull request can neither author nor widen the class that approves it. Admitting a second class SHALL be a NEW GRANT with its own recorded word, and SHALL NOT be treated as a configuration change.

#### Scenario: The admitted surface is exactly the sites the driver writes
- **WHEN** the re-pin lane is enrolled as a candidate class
- **THEN** its writable path set names exactly the files the pin driver writes, each by name
- **AND** no directory-wide pattern stands in for any of them

#### Scenario: A fifth path parks the candidate
- **WHEN** a pull request on the lane's head reference changes any path the class does not name
- **THEN** the approval parks and the pull request waits for a human merge word
- **AND** no other satisfied condition of the class overrides that park

#### Scenario: The enrolment cannot be widened by the pull request it approves
- **WHEN** a pull request would add a candidate class to the declaration or widen an existing class's writable path set
- **THEN** that pull request is itself outside every declared writable path set
- **AND** the declaration governing its approval is read from the base branch rather than from its head

### Requirement: The re-pin enrolment names the safeguard set that keeps the judge chosen by the source floor
An enrolment of the lane that writes this repository's decision-core pin SHALL record the safeguard set that bounds what the lane can propose, and SHALL state the residual risk that remains after those safeguards rather than arguing it away, so that the enrolment is judged on what the lane structurally cannot do rather than on trust in its author.

The recorded safeguards SHALL include, at minimum: that the lane's proposals are confined to one measured author identity and one measured head reference; that the diff is produced by the pin driver, which moves every declared site or opens nothing and writes nothing outside them; that the value proposed is the source repository's default-branch head resolved AT RUN TIME, with any commit, branch, tag or reference named by the trigger payload refused; and that the proposed decision core is EXERCISED against the candidate by a required check before any approval can stand. The residual risk SHALL be recorded as what it is — that an autonomous approval of such a delivery is the envelope approving a change to its own next judge — together with the bounds that remain: a human may close the pull request, the required checks still gate the merge, and the enrolment carries a one-edit kill switch.

#### Scenario: An enrolment recording no safeguard set
- **WHEN** an enrolment is proposed for the lane that writes this repository's decision-core pin and records no safeguard set
- **THEN** the enrolment is refused
- **AND** the reason recorded is that the safeguards were not named

#### Scenario: The value proposed is the source default-branch head and nothing else
- **WHEN** the enrolled lane delivers a pin advance
- **THEN** the commit it proposes is the source repository's default branch head resolved at run time
- **AND** a commit named by a trigger payload, a tag, a branch or a pull-request head is refused rather than proposed

#### Scenario: The proposed core judges the candidate before the approval
- **WHEN** an enrolled re-pin pull request is evaluated for autonomous approval
- **THEN** the required checks that decide it have run against the decision core the pull request proposes
- **AND** those checks are inside the all-green condition the approval quantifies over

### Requirement: The re-pin enrolment is inert until a carve for its named candidate lands, and never reaches for a removal or a bypass
An enrolment whose candidate touches a never-clearable floor member SHALL approve nothing until a CARVE naming that candidate and that exact member set lands in the decision core that composes the floor, and that inert state SHALL be a CONFORMING state of the enrolment reported as such rather than treated as a failure or as progress.

The enrolment SHALL NOT reach the completion it wants by any other route: it SHALL NOT remove the member from the floor, SHALL NOT widen the floor's grace for any class of candidate, SHALL NOT propose or take any ruleset act including the addition of a bypass actor, and SHALL NOT admit a second identity, an administrative merge or an undeclared merge queue. Where the carve lands, the member SHALL remain declared on the floor so that every other candidate and every other author is refused over it exactly as before, and floor-drift detection SHALL continue to see it.

#### Scenario: The enrolment lands before the carve
- **WHEN** the candidate class is enrolled and the floor composition still parks the candidate over the never-clearable member
- **THEN** the candidate parks, naming the floor member it touched, and the pull request waits for a human merge word
- **AND** the park is recorded as a conforming state of the enrolment rather than as a defect in it

#### Scenario: A removal offered in place of a carve
- **WHEN** a change would take the never-clearable member off the floor so that the enrolled candidate stops being refused
- **THEN** it is refused, and the carve naming the candidate and the member is what is asked for instead
- **AND** the member stays visible to floor-drift detection

#### Scenario: A bypass actor offered in place of a carve
- **WHEN** a change would add a bypass actor to a ruleset so that the enrolled candidate's merge stops being refused
- **THEN** it is refused, and the reason recorded is that the grant is per actor and per ruleset rather than per candidate
- **AND** no agent takes a ruleset act on account of the enrolment

### Requirement: The armed witness drops its inertness clause only when a class actually admits the lane
The witness the automated pin advance writes when it arms the platform's auto-merge SHALL state whether a candidate class admits the lane at the time it is written, and that statement SHALL be dropped or added only in the change that makes it false or true, so that a reader of the run log is never told the lane is autonomous when nothing can release the arming, nor told the arming is inert once an enrolment and its carve both stand.

#### Scenario: The enrolment lands and the carve does not
- **WHEN** a candidate class admits the lane but the floor composition still parks it
- **THEN** the witness states that the arming cannot yet complete and names what is missing
- **AND** it does not claim that no class admits the lane

#### Scenario: The enrolment is withdrawn
- **WHEN** the candidate class is removed from the enrolment declaration
- **THEN** the witness states again that no class admits the lane
- **AND** the lane returns to the human merge gate on the next evaluation
