# shared-contract-ownership

## ADDED Requirements

### Requirement: A content resolution reduced to presence or identity names the condition it observed
Release verification SHALL reduce a content resolution to a presence answer or a
blob identity ONLY where the resolution established that answer, and where it
did not, it SHALL fail closed as an unavailable dependency naming the condition
observed — never returning the same value for "there is nothing at this path"
and for "the question could not be asked".

THIS IS THE SAME DEFECT AS THE ONE THE REACHABILITY REQUIREMENTS ALREADY CLOSE,
ONE LAYER DOWN, and it is stated separately because those requirements do not
reach it. They govern the ANCESTRY question and its three outcomes; this governs
the CONTENT question — what is at this path in this commit, and is anything
there at all. The reasoning transfers exactly: a candidate not being on
published `main` is a verdict about the RELEASE, an object that could not be
made available is a fact about the ENVIRONMENT, and a store that cannot answer
is neither. Reducing the second to the first is how a verification reports
something it did not read.

A FLATTENED FAILURE IS WORSE THAN A LOUD ONE IN BOTH DIRECTIONS, and the
direction that matters most is the quiet one. Where two resolutions are compared
and each fails, the two identical non-answers compare EQUAL, and the
verification reports the surface as undrifted having read neither side of it — a
PASS manufactured out of two failures. Where one fails and one succeeds, the
mismatch produces a drift finding about a release surface that may not have
drifted at all. A verification that can pass on an unread surface has lost the
property it exists for, and it loses it without emitting anything a reader could
notice.

ONE CONDITION IS THE DATA ANSWER AND THE REST ARE NOT. That the path does not
exist in that commit's tree is a fact ABOUT THE RELEASE, established by a
resolution that ran: the tree was read and the path was not in it. Everything
else — the commit is absent from the store, the repository cannot be opened, the
tool cannot be run, the read timed out, the argument was malformed — establishes
nothing about the release, and MUST NOT be spelled the same way. The
verification SHALL therefore distinguish the one condition it can act on from
every condition it cannot, rather than distinguishing none of them.

THE SAFETY REFUSALS STAY REFUSALS AND ARE NOT DEMOTED TO ABSENCE. A path that
resolves to something other than a supported regular file — a directory, a
symbolic link, a nested repository link — and a tree entry the resolver refuses
as malformed or inexact are DELIBERATE refusals of an unsafe read, not
statements that nothing is there. Reporting them as absence converts a safety
refusal into release data, which is the one conversion a fail-closed resolver
must never make, and it is reachable from committed state rather than only from
a broken environment: a release-surface path replaced at one commit by a
directory or a nested repository link takes that branch on ordinary data.

THE DISTINCTION SHALL BE CARRIED BY A DECLARED SIGNAL, NOT BY MATCHING PROSE.
Which condition a resolution failure names SHALL be determined from something
the resolver declares for that purpose. A verification that recovers the
distinction by matching the text of an error message re-creates the failure it
is closing: a message is prose, prose is edited for clarity, and a near-miss
match then silently reclassifies a refusal as data. This is the same rule the
sentinel vocabulary states for a near-miss spelling, applied to the resolver's
own vocabulary.

FAIL-CLOSED IS PRESERVED IN FULL AND NOTHING ABOUT A SUCCESSFUL RESOLUTION
MOVES. A resolution that succeeds returns exactly what it returns today, the
comparison it feeds runs exactly as it runs today, and the finding codes, their
severities and their meanings are untouched. This requirement changes only what
happens when a resolution does NOT succeed, and it never converts a refusal into
a pass.

#### Scenario: The path is absent at the commit
- **WHEN** the resolution runs to completion and establishes that the path is not present in that commit's tree
- **THEN** the verification MUST take that as the release fact it is and proceed with the comparison or the membership decision it feeds
- **AND** no other condition MUST be able to produce that same answer

#### Scenario: The store cannot answer the content question
- **WHEN** a content resolution fails for any reason other than the path being absent from the tree — the commit is not in the store, the repository cannot be opened, the tool cannot be run, the read times out, or the request is malformed
- **THEN** the verification MUST fail closed as an unavailable dependency whose reason names the condition observed
- **AND** it MUST NOT be reported as a drifted release surface, as an undrifted one, or as a missing release member

#### Scenario: Both sides of a comparison fail
- **WHEN** a release-surface comparison resolves neither side, each failing for a reason other than absence
- **THEN** the verification MUST fail closed rather than report the surface as undrifted, because two non-answers that happen to be spelled alike are not a comparison
- **AND** a verdict MUST NOT be reached by comparing one unavailable result against another

#### Scenario: An unsafe or inexact resolution is offered as absence
- **WHEN** the path at that commit resolves to a directory, a symbolic link, a nested repository link, or a tree entry the resolver refuses as malformed or inexact
- **THEN** the verification MUST fail closed naming that condition rather than treating the path as absent
- **AND** the refusal MUST NOT be softened because the same path resolves cleanly at the other commit under comparison

### Requirement: Each distinguished content-resolution condition is pinned by an executable proof
Release verification SHALL carry an executable proof for each content-resolution
condition this requirement family distinguishes, and each proof SHALL be pinned
to the condition it exists to separate rather than to the shape of the code that
separates them.

THE SIBLING FAMILY ESTABLISHED WHY, ON EVIDENCE THIS ONE INHERITS. The reachability
defect it closed was not caught by any test — it was caught by a continuous-
integration run failing twice and passing once over one unchanged tree — and the
conclusion drawn there applies unchanged here: a requirement about mechanics that
carries no proof of those mechanics leaves the next reader unable to tell whether
the mechanics still hold. This defect is in the same position today. It was found
by reading, not by a failing test, and the suite that covers this file passes with
the conflation in place.

THE ABSENCE PROOF AND THE UNAVAILABILITY PROOF ARE DIFFERENT PROOFS AND BOTH ARE
OWED. A proof that the absent path still yields the release answer establishes
that the fix did not break the ordinary case; a proof that an unavailable store
refuses establishes that the fix does what it exists for. Only the pair
distinguishes the two, and a family whose whole subject is a distinction cannot
be pinned by a proof of one side.

THE QUIET DIRECTION SHALL BE PROVEN EXPLICITLY. A proof SHALL exist for the case
in which BOTH sides of a comparison fail, asserting a refusal rather than a clean
result, because that is the direction in which the defect produces no output at
all and is therefore the direction a suite is least likely to have covered by
accident.

A PROOF MUST BE ABLE TO FAIL FOR THE RIGHT REASON. Each proof SHALL be
demonstrated to fail when the distinction alone is removed — the resolver's
declared signal ignored, or the failure flattened back to a single value — so
that it is pinned to the conflation and cannot pass merely because the
surrounding verification happens to succeed. And no proof SHALL be written that
asserts a clean or undrifted result reached from a failed resolution, because a
test that permits the quiet direction is how this defect would return.

#### Scenario: The proof for a path that is genuinely absent
- **WHEN** a fixture presents a commit whose tree does not contain a release-surface path
- **THEN** the proof MUST assert the release answer the verification reaches today, unchanged
- **AND** it MUST NOT reach that answer through any path that a failed resolution could also reach

#### Scenario: The proof for a store that cannot answer
- **WHEN** a fixture makes the content resolution fail for a reason other than the path being absent
- **THEN** the proof MUST assert a fail-closed refusal rather than a finding or a clean result
- **AND** it MUST assert that the refusal's reason names the condition observed rather than the release

#### Scenario: A proof is checked against the defect it claims to prevent
- **WHEN** the distinction is removed and the proofs are run
- **THEN** the refusal proofs MUST fail, reproducing the flattened value the defect produces
- **AND** a proof that still passes MUST be treated as unpinned and rewritten rather than accepted
