# release-realization Specification Delta

This delta is ALL-ADDED, and that is a MEASURED CHOICE rather than a style. The
obligation it states has no promoted home today: `openspec/specs/` carries no
requirement about how this capability's own tooling behaves when a path it is
asked to judge cannot be resolved at all. Read at `c6997f12`, the whole promoted
corpus mentions a symlink in exactly one place, `document-lifecycle`'s pin-record
containment rule (`openspec/specs/document-lifecycle/spec.md:484-493`, with its
two scenarios at `:637-643`), which governs a DIFFERENT reader (the pin resolver)
over a DIFFERENT tree (a resolution root's `contracts/` directory) and says
nothing about what either reader does when resolution RAISES. So there is no
current text to restate and nothing to modify.

**THE ALTERNATIVE WAS A `## MODIFIED` BLOCK AND IT WAS DECLINED FOR A MEASURED
REASON, NOT A STYLISTIC ONE.** The nearest promoted titles are *Realization axis
vocabulary is gated* (the `target_release:` gate, whose validator carries two of
the four sites) and *Realization axis declaration*. Both are ALREADY written by
an active ratified change: `add-target-release-deferred-allocation` holds a
`## MODIFIED` block over each. A second block over either would owe
`sequenced_after: [add-target-release-deferred-allocation]`, would have to write
its pre-text from THAT change's outcome rather than from canon under *Ordered
deltas and branch vocabulary*, and would inherit that requirement's archive-order
hold. It would also add a third active writer to a requirement whose two existing
writers are the collision this repository's modified-block-currency self-gate is
red on today. An ADDED requirement over a NOVEL title owes none of it, restates
no promoted text, drops none, and therefore owes no `Modified over`,
`Removed from canon by` or `Merged into` marker.

**NOTHING PROMOTED IS CHANGED.** *Realization axis declaration*, *Realization
axis vocabulary is gated*, *Realization archive gate*, *Proposal support archive
gate*, *Origin retention at archive*, *A moved packet declares the identity it
was ratified under* and *An undeclared rename arrival is refused at its landing*
all stand exactly as ratified. What this delta adds is a property of the READERS
those requirements are enforced by, which none of them states: that a reader
asked to judge a path it cannot resolve answers, rather than ending the run.

**THE TWO TITLES BELOW WERE CHECKED AGAINST THE WHOLE CORPUS AND APPEAR
NOWHERE ELSE**, in `openspec/specs/`, in any active change's delta, or in the
archive.

## ADDED Requirements

### Requirement: A containment guard answers every resolution failure and raises none
A PATH-CONTAINMENT GUARD in this capability's own tooling SHALL ANSWER ITS CALLER
FOR EVERY FAILURE OF THE PATH RESOLUTION IT PERFORMS, AND SHALL RAISE NONE: a
resolution that fails SHALL produce the guard's own negative answer (the dropped
candidate, the absent registry, the uncontained path) rather than an exception
its caller cannot tell apart from a defect in the tool. A guard that answers some
resolution failures and raises on others does not have the contract its callers
were written against; it has that contract for the failures its author happened
to enumerate.

A PATH-CONTAINMENT GUARD IS ANY FUNCTION THIS CAPABILITY'S TOOLING USES TO DECIDE
WHETHER A CANDIDATE PATH IS REALLY INSIDE THE SCANNED TREE, and the decision is
taken by RESOLVING the candidate and the root and comparing them. The definition
is by ROLE and not by name: it reaches a guard called `_unescaped`, one called
`_contained`, one called `_registry_present`, and any later one, because what
makes the obligation apply is that a caller is relying on an answer.

THE SET OF FAILURES THE GUARD MUST ABSORB IS THE INTERPRETER'S, NOT THE SET ITS
AUTHOR NAMED. A guard SHALL be written against what the resolution it calls can
actually raise on the interpreter the gates run on, and that set SHALL be
MEASURED rather than assumed from the operation's name. On the interpreter this
repository's required test suite pins, `Path.resolve(strict=True)` signals a
symlink loop as a `RuntimeError` and NOT as an `OSError`; `RuntimeError` is a
subclass of neither `OSError` nor `ValueError`, so a clause naming only those is
open at exactly that failure. The loop may stand at the candidate's LEAF or at
ANY PARENT COMPONENT of it, including the scanned root itself, and the obligation
reaches every position equally, because the caller's need for an answer does not
depend on which component failed.

A CATCH ALREADY WIDER THAN THIS OBLIGATION SHALL BE RETAINED AND NEVER NARROWED
TO MATCH IT. Where a guard also absorbs a failure of a DIFFERENT operation it
performs (the relative-path computation that decides containment raises a
`ValueError` of its own when the candidate lies outside the root), that catch
answers a different question and stands. This requirement widens a guard's
failure set and never trims it.

A CROSS-MODULE CLAIM OF IDENTITY BETWEEN TWO GUARDS IS PART OF THE OBLIGATION AND
SHALL BE KEPT TRUE BY THE SAME ACT THAT WIDENS EITHER. Where one guard's own
documentation names another as the shape it mirrors, or as the test it
generalizes, the two SHALL be widened together in ONE act. Widening one alone
leaves a documented claim of identity that is false, which misleads the next
reader more than no claim would: the claim is what tells that reader they need
only understand one of the two.

A GUARD'S DOCUMENTATION SHALL NAME THE FAILURES IT ABSORBS. Prose that promises a
candidate is DROPPED, or that a registry is ABSENT, without naming what makes
that answer possible, is the prose that produced this defect: every reviewer read
the promise and none read the clause. Naming the set costs one line and is what
makes a narrowing visible in a diff.

THE OBLIGATION IS ABOUT THE ANSWER AND NOT ABOUT ANY PARTICULAR SPELLING OF THE
GUARD. An exception clause listing the measured set is the shape this estate's
guards use today; a resolution that cannot raise at all would satisfy this
requirement equally. What is forbidden is a guard whose caller can be handed an
exception where the guard's own contract promised an answer.

#### Scenario: A symlink loop stands at a candidate's leaf
- **WHEN** a containment guard is asked about a candidate whose final component is a symlink that resolves back into its own chain
- **THEN** the guard MUST return its negative answer, the candidate being dropped, absent or uncontained as that guard's contract states
- **AND** it MUST NOT raise, whatever exception type the interpreter uses to signal the loop

#### Scenario: A symlink loop stands in a parent component
- **WHEN** the candidate's own final component is an ordinary name but a DIRECTORY above it, at any depth between it and the scanned root, is a symlink that resolves back into its own chain
- **THEN** the guard MUST return its negative answer exactly as it does for the leaf case
- **AND** the position of the failing component MUST NOT change the answer, ordinariness being a property of the one component it is asserted of

#### Scenario: The scanned root is itself reached through a loop
- **WHEN** the root the guard resolves the candidate against is itself behind a symlink loop, so resolving the root fails rather than resolving the candidate
- **THEN** the guard MUST still answer, because a caller that cannot resolve its own root has a tree it cannot judge and not a defect to report

#### Scenario: A guard absorbs a second failure of its own
- **WHEN** a guard additionally computes a path relative to the root, and that computation raises for a candidate that lies outside it
- **THEN** that catch MUST be retained beside the resolution failures, this obligation widening a guard's failure set and never trimming it

#### Scenario: One guard is widened and the guard it names as its mirror is not
- **WHEN** a guard whose documentation names a second guard as the exact shape it mirrors, or as the test it generalizes, is corrected alone
- **THEN** that act MUST be refused as incomplete, because it leaves a documented claim of identity false
- **AND** the correction MUST reach every guard the claim binds together, in one act

#### Scenario: A guard promises a drop its clause does not deliver
- **WHEN** a guard's documentation states that a failing path is dropped rather than reported, and its clause absorbs only part of the failure set the measured interpreter produces
- **THEN** the documentation MUST be read as stating the obligation and the clause as failing it, the remedy being to widen the clause and to name the set in the prose

### Requirement: A symlink-loop proof is built at test time and never committed
A TEST PROVING A CONTAINMENT GUARD'S ANSWER FOR A SYMLINK LOOP SHALL BUILD THAT
LOOP AT TEST TIME, under the test's own temporary directory, and this repository
SHALL NOT carry a committed symlink loop anywhere in its tree. The fixture is
evidence for ONE guard; a committed one is a hazard to every reader of the tree.

A COMMITTED LOOP IS TRACKED AS ORDINARY GIT OBJECTS AND REACHES EVERY RECURSIVE
READER THIS ESTATE RUNS, not only the guard under test: the corpus scans, the
document-health families, the archive gate, the notebook projection and the
packaging tools all walk this tree, and each would meet a path that cannot be
resolved. A fixture that reds tools unrelated to the defect it proves is not
evidence; it is a second defect, introduced to demonstrate the first.

THE PROOF SHALL FAIL AGAINST THE UNFIXED GUARD AND PASS AGAINST THE FIXED ONE,
and that pair SHALL be recorded rather than asserted. A test written after a fix,
which passes on both sides of it, proves that the fixed code works and says
nothing about whether the defect was real; this estate's standard for a
correction is the pair of runs.

WHERE A GUARD CANNOT BE REACHED BY ANY TREE STATE, ITS PROOF SHALL SAY SO AND
SHALL PROVE THE CLAUSE INSTEAD. A guard fronted by a pre-check that absorbs the
same failure earlier may be unreachable through a real tree while its own clause
is still narrower than the measured failure set. Such a guard SHALL still be
widened, both because a pre-check and a resolution are two separate reads of a
tree that can change between them and because a reader of the module sees the
clause and not the pre-check; and its proof SHALL be declared for what it is, a
test of the clause and not of a reachable tree state, rather than dressed as a
tree the estate cannot actually build.

#### Scenario: A guard's answer for a symlink loop is proved
- **WHEN** a test asserts that a containment guard returns its negative answer for a loop
- **THEN** it MUST build the loop under its own temporary directory at test time
- **AND** no symlink participating in that loop may be added to this repository's tracked tree

#### Scenario: A loop is offered as a committed fixture
- **WHEN** a change proposes to commit a symlink loop as a test fixture
- **THEN** it MUST be refused, the loop reaching every recursive reader of the tree and not only the guard it was written for

#### Scenario: A proof passes against the unfixed guard
- **WHEN** a test written to prove a widened guard also passes against that guard before the widening
- **THEN** it MUST NOT be accepted as the proof, and the failing run against the unfixed guard MUST be recorded beside the passing one

#### Scenario: A guard is unreachable through any tree state
- **WHEN** a guard's own pre-check absorbs the failure before the resolution it guards is reached, so no buildable tree drives it to its clause
- **THEN** the guard MUST still be widened, the pre-check and the resolution being two reads of a tree that can change between them
- **AND** its proof MUST be declared as a test of the clause rather than presented as a reachable tree state
