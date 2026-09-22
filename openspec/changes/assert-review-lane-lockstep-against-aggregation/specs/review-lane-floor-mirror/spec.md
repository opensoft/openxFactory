# review-lane-floor-mirror Specification

ONE `## ADDED` requirement. **No `## MODIFIED` block, and that is a decision
rather than an omission** (`design.md` D3): three active changes carry deltas on
this capability — `amend-mirror-floor-regeneration-merge-authority` (a
`## MODIFIED` block on *An automated pin advance only ever proposes*),
`admit-review-lane-repin-to-merge-approval-envelope` and
`extend-merge-master-envelope-to-floor-bot-lanes` (four and three `## ADDED`
requirements) — and none of them names the requirement below or is named by it.
The hazard this closes is not in any promoted requirement's text; it is in the
GAP between the pin advance this capability automates and a field of the pin
file that no requirement has ever obliged anyone to measure. Adding the
obligation collides with nothing and rewords nothing.

## ADDED Requirements

### Requirement: The pin's cross-repository lockstep state is measured against the aggregation's own surfaces, never declared alone
The pin's declared CROSS-REPOSITORY LOCKSTEP STATE SHALL be MEASURED against the
aggregation's own pin surfaces rather than standing on a declaration alone: a
check SHALL compare the declared state to the commit those surfaces name, and
SHALL REPORT a declared state the comparison contradicts.

WHAT IS COMPARED is values and not authorship: the pin's `core_commit` against
the commit the aggregation's surfaces name, `converged` meaning equal and
`diverged` meaning unequal. THE AGGREGATION'S SURFACES ARE READ AS A SET AND
SHALL AGREE WITH EACH OTHER BEFORE EITHER STATE IS CONCLUDED — the pin's own
`converged_with:` members and the aggregation's constant that holds them
identical — and where they DISAGREE the check SHALL report INCONSISTENT, name
each surface with the value it carried, and conclude NEITHER `converged` NOR
`diverged`. A check permitted to pick one surface would be choosing its own
answer, and an aggregation whose own surfaces disagree is a fact about that
repository that this measurement is the first thing positioned to see. WHEN IT
RUNS is at least every proposed advance of `core_commit` and the pull request
that carries it, so a declaration an advance falsifies is reported in the SAME
pull request that falsifies it rather than whenever a human next happens to read
the field.

WHERE THE READ LIVES AND WHERE THE JUDGMENT LIVES follows this capability's own
split and SHALL NOT be drawn elsewhere: the cross-repository read is performed
where this capability already performs cross-repository reads — the workflow,
which resolves the other repository over the API, visible in the run log and
re-runnable by a reviewer with the same call — and the COMPARISON is a function
over supplied values that touches no network, so every verdict is a unit test
with a fixture rather than a workflow that has to be fired to be believed.

THE CHECK IS SYMMETRIC. A declared `converged` the measurement contradicts and a
declared `diverged` the measurement contradicts SHALL be reported alike, because
the field is a point-in-time claim about a mutable pair and either value can be
the false one.

WHERE THE AGGREGATION'S SURFACES CANNOT BE READ the check SHALL report the state
as UNDETERMINED and name what it could not read; it SHALL NOT resolve to either
state, and it SHALL NOT read its own silence as confirmation of the declared one.
An unaskable question is never an implicit pass.

THE SURFACES ARE READ AT ONE RESOLVED COMMIT OF THE AGGREGATION AND NOT
INDEPENDENTLY FROM A MOVING REF. The check SHALL resolve the aggregation's
branch to a single commit first and read every surface AT THAT COMMIT, and
SHALL name that commit with its verdict. Reading the surfaces one at a time from
a branch lets a re-point land between the reads and returns a MIXED set — which
the check would then report as INCONSISTENT, a state that never existed in the
repository it was reading. A measurement taken across a moving ref measures READ
TIMING, not the aggregation.

THE DECLARED STATE IS A CLOSED VOCABULARY AND AN UNREADABLE DECLARATION IS THE
REPOSITORY'S OWN DEFECT. The declared lockstep state SHALL be one of the two
words the field carries; where it is ABSENT, or carries any other value, the
check SHALL FAIL naming the value it found, in the same class as a declaration
the measurement contradicts — because both are this repository's own file failing
to say something true, and the remedy for both is one edit to the field. Without
that clause the ordering below has an input it does not reach.

THE OUTCOMES ARE ORDERED AND EXACTLY ONE HOLDS FOR ANY INPUT: the aggregation
UNREADABLE first; then its surfaces DISAGREEING with each other; then the
comparison of the agreed commit against `core_commit`; then the declared state
against that comparison. A later outcome is reached only where every earlier one
does not hold, so no input can require two conclusions and no implementation has
to arbitrate between them.

UNDETERMINED SHALL NOT BE A STANDING STATE. Where the check cannot read the
aggregation on EVERY run, the defect is the check's own access and SHALL be
reported as that rather than as a property of the measurement — a check that
answers UNDETERMINED forever is indistinguishable from one that is working, which
is the failure this requirement exists to end rather than to reproduce.

EACH OUTCOME SHALL CARRY A CONCLUSION AND NOT ONLY A NAME, because a state a
check computes and does not publish is a state nobody acts on. A declaration the
measurement CONTRADICTS SHALL fail the check and name both values: that is this
repository's own contract file stating something false about another repository,
and the remedy is one edit to the field. UNDETERMINED and INCONSISTENT SHALL
each conclude NEUTRAL — visible, naming the state and what was read, and NOT
failing — because neither is this repository's claim to answer: an unreachable
aggregation is another repository's availability and an aggregation whose own
surfaces disagree is another repository's defect, and turning either into this
repository's red build would make the check a liability its owners would route
around. A NEUTRAL conclusion SHALL NOT be reported as a pass, and silence SHALL
NOT stand in for it.

THE DECLARATION IS NOT REMOVED BY THIS RULE. The pin file stays the place the
state is declared and the place its dated reasoning is kept; what changes is that
the declaration becomes the SUBJECT of a measurement rather than its only
evidence. A check that could be satisfied by reading the pin file alone would
satisfy nothing: the fact being asserted is about another repository, and a value
compared only to itself is a tautology.

#### Scenario: A routine advance leaves the declared state behind
- **WHEN** an automated pin advance moves `core_commit` to a commit that the aggregation's surfaces — agreeing with each other, and read — do not name, and the declared lockstep state still reads `converged`
- **THEN** the check reports the contradiction on the advance's own pull request, naming both values and the surfaces it read them from
- **AND** the report does not depend on the advancing lane having remembered to write the field, because the check reads the other repository rather than the lane's intent

#### Scenario: The declared state is absent or outside its vocabulary
- **WHEN** the pin's declared lockstep state is absent, or carries a value that is neither of the two words the field admits
- **THEN** the check FAILS and names the value it found, in the same class as a declaration the measurement contradicts
- **AND** it does not fall through to a comparison, because there is nothing to compare

#### Scenario: The advance lands on the commit the aggregation already pins
- **WHEN** an advance moves `core_commit` to exactly the commit the aggregation's surfaces — agreeing with each other, and read — already name, and the declared state reads `diverged`
- **THEN** the check reports that contradiction too, because the obligation is that the declaration be TRUE and not that it be pessimistic

#### Scenario: The aggregation's own surfaces disagree with each other
- **WHEN** the aggregation's surfaces, read at ONE resolved commit of it, do not all carry the same commit
- **THEN** the check reports INCONSISTENT and names each surface with the value it carried
- **AND** it concludes neither `converged` nor `diverged`, because a check permitted to pick one surface would be choosing its own answer
- **AND** the disagreement is the aggregation's own at that commit, not an artefact of reading its surfaces one at a time while a re-point landed between the reads

#### Scenario: The aggregation's surfaces cannot be read
- **WHEN** the check cannot obtain the aggregation's judging surfaces
- **THEN** it reports the lockstep state as UNDETERMINED and names each surface it could not read
- **AND** it concludes neither `converged` nor `diverged`, and does not report the declared value as confirmed
- **AND** the check's own conclusion is NEUTRAL and visible rather than failing, because another repository's availability is not this repository's build, and rather than passing, because silence is not a measurement

#### Scenario: The verdict is reproduced without firing the lane
- **WHEN** a reviewer is given the commit the pin declares, the commits the aggregation's surfaces name and the declared state
- **THEN** the same verdict follows from those values alone, because the comparison is a function over them and reaches no network
- **AND** each refusal and each report is exercised by a unit test with a fixture rather than by dispatching the workflow
