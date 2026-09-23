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
`converged_with:` members, which are the read plan's workflow members, and the
aggregation's constant that holds them identical, `MIGRATION_PIN`, — and where they DISAGREE the check SHALL report INCONSISTENT, name
each surface by a digest of the commit it carried, and conclude NEITHER `converged` NOR
`diverged`. A check permitted to pick one surface would be choosing its own
answer, and an aggregation whose own surfaces disagree is a fact about that
repository that this measurement is the first thing positioned to see. WHEN IT
RUNS is at least every proposed advance of `core_commit` and the pull request
that carries it, so a declaration an advance falsifies is reported in the SAME
pull request that falsifies it rather than whenever a human next happens to read
the field. THE ONE EXCEPTION IS THE HOST'S OWN: where the host does not start a
path-filtered workflow because it cannot see the whole diff — GitHub does not for
a pull request of more than 3,000 changed files whose matching file is not among
the first 3,000 — the check does not run on that pull request, and the gap is
stated here so that this clause is never read as closing it. WHAT IT OBSERVES IS
THIS REPOSITORY'S SIDE OF THE PAIR: a move the
aggregation makes alone, its `MIGRATION_PIN` re-pointed at a ceremony, can
falsify the declaration with no pull request here, and the check reports that at
the next pull request that changes the pin; the ceremony's own pull request here,
the one that moves `lockstep.status`, is such a pull request. Observing the
aggregation's side as it moves would take an act in the aggregation or a
schedule, and this requirement takes neither. IT JUDGES EVERY SUCH PULL REQUEST ALIKE: no condition of the check SHALL
branch on the pull request's author, its branch or its automated origin, because
this capability's *An automated pin advance is judged by the freshness checks that
already exist, with no exemption* forbids exactly that to every check that judges
a pin advance, and a hand-authored advance leaves the declaration as false as an
automated one.

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

WHERE THE AGGREGATION'S SURFACES CANNOT BE READ, for a reason outside the check's
own access, the check SHALL report the state as UNDETERMINED and name what it
could not read; it SHALL NOT resolve to either
state, and it SHALL NOT read its own silence as confirmation of the declared one.
An unaskable question is never an implicit pass. A SURFACE IS READ ONLY AS A
COMMIT: each surface's value SHALL be forty lowercase hexadecimal characters, the
grammar the pin's own `core_commit` obeys, and a surface whose value is not SHALL
count as UNREADABLE, named by a CLASSIFICATION of what its fixed location held —
absent, empty, or not a commit — and NEVER by that value or the file around it,
in the verdict or in the run log: the aggregation is private while both of those
are public, and a value that is not a commit is exactly the one nobody has vetted
for publication. AND NO SURFACE'S VALUE IS PUBLISHED AS IT IS, a commit's grammar
included, because the grammar proves forty hexadecimal characters and not a
commit: a surface that has it is named by its relation to `core_commit`, equal or not, and a digest of its value; only the
commit the check resolves the aggregation's branch to, which the API returns as a
commit, is named as it is. A reviewer with access to the aggregation reproduces
every value with the same call. So surfaces that AGREE on
something that names no commit, an empty string among them, conclude nothing,
rather than reaching a comparison that a declared `diverged` would pass merely
because two strings differ.

THE SURFACES ARE READ AT ONE RESOLVED COMMIT OF THE AGGREGATION AND NOT
INDEPENDENTLY FROM A MOVING REF. The check SHALL resolve the aggregation's
DEFAULT BRANCH at run time, from the repository itself and never from an event
payload, a pull-request head, a tag or any reference a caller supplies; SHALL
resolve that branch to a single commit first; SHALL read every surface AT THAT
COMMIT; and SHALL name the branch and the commit with its verdict. Reading the surfaces one at a time from
a branch lets a re-point land between the reads and returns a MIXED set — which
the check would then report as INCONSISTENT, a state that never existed in the
repository it was reading. A measurement taken across a moving ref measures READ
TIMING, not the aggregation.

THE DECLARED STATE IS A CLOSED VOCABULARY AND AN UNREADABLE DECLARATION IS THE
REPOSITORY'S OWN DEFECT. The declared lockstep state SHALL be one of the two
words the field carries; where it is ABSENT, or carries any other value, the
check SHALL FAIL naming the value it found, in the same class as a declaration
the measurement contradicts, the value named inert and length-bounded — because
both are this repository's own file failing to say something true, and the remedy for both is one edit to the field. Without
that clause the ordering below has an input it does not reach. SO IS THE SET OF
SURFACES THE PIN DECLARES: where the candidate's `converged_with:` names any set
other than the WORKFLOW MEMBERS of the check's own read plan, the check SHALL FAIL
naming the set it found and those members, in that same class, because a pin
declaring surfaces the check does not read is the same file failing to say
something true. AND SO IS THE COMMIT THE CANDIDATE PROPOSES: a candidate
`core_commit` that is not forty lowercase hexadecimal characters SHALL FAIL in
that same class, naming the value found, inert and length-bounded — otherwise an
inequality against the aggregation's commit would report a declared `diverged`
as agreeing with a value that names no commit. A candidate that
cannot be parsed declares nothing, and SHALL count as ABSENT, the parse error
named as the value found, inert and length-bounded. A base's defect reaches the
verdict through every candidate that inherits it, and a candidate that repairs it
is judged on what it proposes.

THE PIN THE CHECK READS IS THE ONE THE ACT PROPOSES, NOT THE ONE ALREADY IN
PLACE, AND IT IS PARSED STRICTLY. The check SHALL parse a pin only under a byte
ceiling fixed in its own code, as ONE document with no duplicate key, alias,
merge key or tag, so that the check and a reviewer reading the same bytes cannot
see different values; a pin the strict parse refuses cannot be parsed, and counts
as ABSENT. Where the check runs over a proposed advance, it SHALL take
`core_commit` from the CANDIDATE state of the pin at the head that advance
proposes — read as INERT BYTES at a verified head commit, never by executing
anything from that head — and SHALL re-verify that commit after the read so a
ref moved underneath it is refused rather than reported. A check that read the
pin from the base it runs on would compare the commit ALREADY in place against
the aggregation, pass, and never see the advance it exists to judge.

WHAT IS READ IN THE AGGREGATION IS DECIDED BY THE CHECK'S OWN CODE, NEVER BY THE
PIN FILE. The candidate's bytes are data to be JUDGED and never an instruction
about what to READ, and so are the base's, because the base's pin file is only a
candidate an earlier pull request proposed: the check SHALL take from the pin
only the values under judgment — `core_commit`, the declared state and the
surfaces `converged_with:` declares — and SHALL take the aggregation and the path
of every surface in it from a READ PLAN FIXED IN ITS OWN CODE — its WORKFLOW
MEMBERS, the aggregation's judging workflows, each read at the `ref:` of its step
that checks out the decision core's repository, `codeXfactory/codexFactory`,
parsed as YAML and never matched as text, and one ADDITIONAL fixed read, the
aggregation's constant at its `MIGRATION_PIN` assignment in
`tests/test_merge_master_workflows.py`, which is never a `converged_with:`
member — never resolving a path
from the pin file, at the candidate head or at the base. A check that could be
told what to read, by the pull request it judges or by one merged before it,
could turn the credential for a private repository on any file in it, and have
that file's contents named back as the value a surface carried.

THE OUTCOMES ARE ORDERED AND EXACTLY ONE HOLDS FOR ANY INPUT: the DECLARATION
OUTSIDE ITS VOCABULARY first — a declared state absent or not one of its two
words, an unparseable candidate among the absent, a candidate `core_commit` that
is not a commit, or a `converged_with:` naming other than the read plan's
workflow members: this
repository's own file, readable without touching anything else, and a defect that
makes every later question moot; then the check's own ACCESS FAILING; then
the aggregation UNREADABLE, a surface whose value is not a commit included; then
its surfaces DISAGREEING with each other; then the comparison of the agreed commit
against `core_commit` and the declared state against that comparison. A later
outcome is reached only where every earlier one does not hold, so no input can
require two conclusions and no implementation has to arbitrate between them. THE
VOCABULARY IS VALIDATED BEFORE THE AGGREGATION IS READ, which is both the ordering
the scenarios require and the honest engineering order: a check does not go
asking another repository a question in order to report a defect in its own file.

UNDETERMINED SHALL NOT BE A STANDING STATE, AND THE CHECK'S OWN ACCESS IS NEVER
UNDETERMINED. An ACCESS failure — its binding unresolved, its mint refused, or the aggregation repository itself refused to the token it minted (a 401, or a 403 or 404 that is not a rate-limit response) — is the check's own defect on
the run where it happens, and SHALL conclude FAIL, naming it; only a failure
outside that access — a surface missing at the resolved commit, a server error,
a timeout or a rate limit — is UNDETERMINED. A check that answered UNDETERMINED
for its own access would answer it on every run, indistinguishable from one that
is working, which is the failure this requirement exists to end rather than to
reproduce.

EACH OUTCOME SHALL CARRY A CONCLUSION AND NOT ONLY A NAME, because a state a
check computes and does not publish is a state nobody acts on. A declaration the
measurement CONTRADICTS SHALL fail the check and name `core_commit`, the declared
state and the digest of the commit the surfaces agree on: that is this
repository's own contract file stating something false about another repository,
and the remedy is one edit to the field. An ACCESS failure SHALL fail it too,
naming the failure, because that is this repository's own configuration and the
remedy is to repair it, not to wait. UNDETERMINED and INCONSISTENT SHALL
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
- **WHEN** an automated pin advance moves `core_commit` to a commit that the aggregation's surfaces — read, and agreeing with each other on one commit of forty lowercase hexadecimal characters — do not name, and the declared lockstep state still reads `converged`
- **THEN** the check reports the contradiction on the advance's own pull request, naming `core_commit`, the digest of the commit the surfaces agree on, and the surfaces it read
- **AND** the report does not depend on the advancing lane having remembered to write the field, because the check reads the other repository rather than the lane's intent

#### Scenario: The declaration is absent or outside its vocabulary
- **WHEN** the pin's declared lockstep state is absent, or carries a value that is neither of the two words the field admits, or the candidate's `core_commit` is not forty lowercase hexadecimal characters, or its `converged_with:` names a set other than the workflow members of the check's own read plan, or the candidate cannot be parsed at all
- **THEN** the check FAILS and names the value, set or parse error it found, inert and length-bounded, and for `converged_with:` the plan's workflow members beside it, in the same class as a declaration the measurement contradicts
- **AND** it reads nothing in the aggregation and does not fall through to a comparison, because there is nothing to compare

#### Scenario: The advance lands on the commit the aggregation already pins
- **WHEN** an advance moves `core_commit` to exactly the commit the aggregation's surfaces — read, and agreeing with each other on one commit of forty lowercase hexadecimal characters — already name, and the declared state reads `diverged`
- **THEN** the check reports that contradiction too, because the obligation is that the declaration be TRUE and not that it be pessimistic

#### Scenario: The aggregation's own surfaces disagree with each other
- **WHEN** the aggregation's surfaces, read at ONE resolved commit of it and each carrying a commit of forty lowercase hexadecimal characters, do not all carry the same commit
- **THEN** the check reports INCONSISTENT and names each surface by a digest of the commit it carried
- **AND** it concludes neither `converged` nor `diverged`, because a check permitted to pick one surface would be choosing its own answer
- **AND** the disagreement is the aggregation's own at that commit, not an artefact of reading its surfaces one at a time while a re-point landed between the reads

#### Scenario: The check's own access fails
- **WHEN** the check's access to the aggregation fails — its binding unresolved, its mint refused, or the aggregation repository itself refused to the token it minted (a 401, or a 403 or 404 that is not a rate-limit response)
- **THEN** the check FAILS and names the access failure, rather than reporting UNDETERMINED
- **AND** it reads no surface and concludes neither `converged` nor `diverged`, because the defect is this repository's own configuration, and an UNDETERMINED for it would stand on every run

#### Scenario: The aggregation's surfaces cannot be read
- **WHEN** the check cannot obtain the aggregation's judging surfaces for a reason outside its own access — a surface missing at the resolved commit, a server error, a timeout or a rate limit — or a surface it obtains carries a value that is not forty lowercase hexadecimal characters
- **THEN** it reports the lockstep state as UNDETERMINED and names each surface it could not read, with the classification of what it carried — absent, empty or not a commit — and never that value itself
- **AND** it concludes neither `converged` nor `diverged`, and does not report the declared value as confirmed
- **AND** the check's own conclusion is NEUTRAL and visible rather than failing, because another repository's availability is not this repository's build, and rather than passing, because silence is not a measurement

#### Scenario: The verdict is reproduced without firing the lane
- **WHEN** a reviewer is given the commit the pin declares, the commits the aggregation's surfaces name and the declared state
- **THEN** the same verdict follows from those values alone, because the comparison is a function over them and reaches no network
- **AND** each refusal and each report is exercised by a unit test with a fixture rather than by dispatching the workflow
