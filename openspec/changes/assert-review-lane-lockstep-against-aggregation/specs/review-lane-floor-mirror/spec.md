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
the commit the aggregation's judging surfaces name, `converged` meaning equal and
`diverged` meaning unequal. WHEN IT RUNS is at least every proposed advance of
`core_commit` and the pull request that carries it, so a declaration an advance
falsifies is reported in the SAME pull request that falsifies it rather than
whenever a human next happens to read the field.

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

THE DECLARATION IS NOT REMOVED BY THIS RULE. The pin file stays the place the
state is declared and the place its dated reasoning is kept; what changes is that
the declaration becomes the SUBJECT of a measurement rather than its only
evidence. A check that could be satisfied by reading the pin file alone would
satisfy nothing: the fact being asserted is about another repository, and a value
compared only to itself is a tautology.

#### Scenario: A routine advance leaves the declared state behind
- **WHEN** an automated pin advance moves `core_commit` to a commit the aggregation's judging surfaces do not name, and the declared lockstep state still reads `converged`
- **THEN** the check reports the contradiction on the advance's own pull request, naming both values and the surfaces it read them from
- **AND** the report does not depend on the advancing lane having remembered to write the field, because the check reads the other repository rather than the lane's intent

#### Scenario: The advance lands on the commit the aggregation already pins
- **WHEN** an advance moves `core_commit` to exactly the commit the aggregation's judging surfaces already name, and the declared state reads `diverged`
- **THEN** the check reports that contradiction too, because the obligation is that the declaration be TRUE and not that it be pessimistic

#### Scenario: The aggregation's surfaces cannot be read
- **WHEN** the check cannot obtain the aggregation's judging surfaces
- **THEN** it reports the lockstep state as UNDETERMINED and names each surface it could not read
- **AND** it concludes neither `converged` nor `diverged`, and does not report the declared value as confirmed

#### Scenario: The verdict is reproduced without firing the lane
- **WHEN** a reviewer is given the commit the pin declares, the commits the aggregation's surfaces name and the declared state
- **THEN** the same verdict follows from those values alone, because the comparison is a function over them and reaches no network
- **AND** each refusal and each report is exercised by a unit test with a fixture rather than by dispatching the workflow
