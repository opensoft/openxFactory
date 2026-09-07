# roles-authority-model — delta

## ADDED Requirements

### Requirement: Autonomous approval is enrolled per lane and per surface
The model SHALL make autonomous merge approval a property of an ENROLLED CANDIDATE CLASS — a named lane together with the exact author identity, head reference, base reference and writable path set it is admitted for — and never a property of an author identity alone, so that a machine identity trusted on one surface is refused on every other surface by default.

An enrolment declaration SHALL be readable from the base branch of the repository it governs and SHALL be routed to a human code owner, so that a pull request can neither author nor widen the class that approves it.

#### Scenario: A trusted machine identity outside its enrolled surface
- **WHEN** a pull request is authored by the machine identity an enrolled candidate class names, but changes a path outside that class's declared writable set
- **THEN** the approval parks and the pull request falls back to the human merge gate
- **AND** no fact about the pull request is treated as approving it

#### Scenario: Widening the enrolment
- **WHEN** a pull request would add a candidate class to the enrolment declaration, or widen an existing class's writable path set
- **THEN** that pull request is itself outside every declared writable path set
- **AND** it is never autonomously approved by the mechanism it edits

### Requirement: A never-clearable floor member is never autonomously approvable
The model SHALL compose the never-clearable governance floor OVER the autonomous approval envelope, so that a candidate touching any floor member is refused BEFORE the envelope is consulted and regardless of what the envelope declares, and SHALL treat an unavailable or unevaluable floor measurement as a refusal rather than as an absence of floor members.

Where an owner rules that one enrolled candidate may be approved despite touching a named floor member, that permission SHALL be expressed as a CARVE naming the candidate and the exact member set it may touch — never as the removal of the member from the floor — so the path stays never-clearable for every other candidate and every other author, and floor-drift detection continues to see it.

#### Scenario: An enrolled candidate touches the floor
- **WHEN** an enrolled candidate satisfies every envelope condition but its changed paths include a never-clearable floor member
- **THEN** the approval parks, naming the floor member it touched
- **AND** the envelope's own verdict does not override the refusal

#### Scenario: The floor measurement is unavailable
- **WHEN** the floor evaluation is skipped, fails, or yields no measured count
- **THEN** the approval parks as though the floor were touched
- **AND** absence of a measurement is never read as zero matches

#### Scenario: A ruled carve for one candidate
- **WHEN** an owner admits one named candidate over one named floor member
- **THEN** the floor member remains declared on the floor
- **AND** any other candidate touching that member is refused exactly as before

### Requirement: A lane writing its own repository's judge is enrolled only behind named safeguards
The model SHALL refuse to enrol a lane whose writable surface includes the artifact selecting which decision core, verifier or gate judges that repository's subsequent pull requests, unless the enrolment records a named safeguard set that bounds what the lane can propose — at minimum that the lane cannot select an arbitrary value, that the proposed judge is exercised against the candidate before approval, and that the residual risk is stated rather than argued away.

#### Scenario: A judge-selecting lane proposed for enrolment
- **WHEN** an enrolment is proposed for a lane that writes the artifact naming the repository's judge
- **THEN** the enrolment records the safeguards bounding the values the lane can propose, and the residual risk that remains after them
- **AND** an enrolment recording no safeguard set is refused

#### Scenario: The proposed judge is exercised on the candidate
- **WHEN** such a lane's pull request proposes a new judge
- **THEN** the required checks that decide the pull request run against the proposed judge, not against the superseded one
- **AND** those checks are inside the conditions the approval quantifies over

### Requirement: An enrolled autonomous lane carries a one-edit kill switch
The model SHALL ensure that every enrolled candidate class can be returned to the human merge gate by a single reviewed edit to the enrolment declaration, taking effect on the next evaluation without redeploying or reconfiguring any lane, and SHALL NOT accept a kill switch held in a value that does not appear in a reviewable diff.

#### Scenario: Withdrawing an enrolment
- **WHEN** an owner removes a candidate class from the enrolment declaration and that removal lands on the base branch
- **THEN** the next evaluation of a pull request of that class reaches no envelope decision and parks for a human
- **AND** the withdrawal is visible in the declaration's history

#### Scenario: A kill switch outside the diff
- **WHEN** a proposed enrolment would hold its on/off state in a repository or environment setting rather than in the reviewed declaration
- **THEN** that enrolment is refused
- **AND** the reason recorded is that the state is not reviewable

### Requirement: An autonomous approval is not a merge
The model SHALL keep autonomous approval and merge as distinct acts, so that an approving lane submits a review and performs no merge, and SHALL require any enrolment that intends unattended landing to name the separate mechanism that merges the approved pull request.

#### Scenario: An approved candidate with no merge mechanism named
- **WHEN** a candidate class is enrolled for unattended landing but no merging mechanism is named for it
- **THEN** the enrolment is incomplete and the pull request still waits for a human
- **AND** the gap is recorded rather than discovered when the first candidate does not land
