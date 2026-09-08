# doc-health Specification Delta

## ADDED Requirements

### Requirement: The readiness derivation proof resolves the repository under test
The readiness derivation proof SHALL resolve the repository under test before
any other checkout, and SHALL NEVER read a different checkout in its place
without saying so in the run's own output.

The proof is the verification that the readiness lane's cluster derivation
still reproduces the landed `ideation-cross-reference` index. It needs two
things from a checkout — the index and the corpus the index pins — and today
it finds them by walking UP from its own location to the first ancestor
holding a `openxFactory/ideation/cross-reference.yaml`. In the aggregation
workspace that walk always terminates on the one shared checkout beneath the
aggregation root, whatever repository the run was actually launched against.
Resolution order is therefore reversed here: the repository under test first,
any other checkout only as a declared fallback, and never silently.

An ancestor search or an environment override MAY serve as that fallback. When
one is used, the run MUST name the checkout it resolved and the reason the
fallback was taken, so that a proof about repository A is never reported as
though it were a proof about repository B. The same resolution order SHALL
govern every checkout the readiness surface reaches for — the index, the
corpus, and the pinned index validator the checker spawns — because a proof
that reads its subject from one checkout and its validator from another has
proved nothing about either.

#### Scenario: The proof runs from a worktree of the repository under test
- **WHEN** the proof runs from any working tree of a repository that itself carries `ideation/cross-reference.yaml`
- **THEN** it MUST read that repository's own index, corpus, and validator
- **AND** it MUST NOT resolve to a sibling checkout that happens to sit above it on the filesystem

#### Scenario: The repository under test cannot serve the proof
- **WHEN** the repository under test does not carry the index and a declared fallback checkout does
- **THEN** the run MUST record which checkout it resolved and why the fallback was taken
- **AND** the fallback MUST be reached only after the repository under test has been tried and found wanting

#### Scenario: No checkout can serve the proof
- **WHEN** neither the repository under test nor any declared fallback carries the index
- **THEN** the run MUST report the proof as not performed, naming that reason
- **AND** it MUST NOT report a pass

### Requirement: The derivation comparison reads committed index state
The derivation comparison SHALL read the landed index from committed state
rather than from a working tree, so that an uncommitted edit — in the
repository under test or in any other checkout on the machine — can neither
red nor green the verdict.

Both sides of the comparison are already revision-addressed on the corpus
side: the derived clusters are built from the corpus reconstructed at the
index's own `generation.source_revision`. The index side is not, and the
asymmetry is the defect. An index read from a working tree is whatever
somebody happens to be editing at that moment, which makes the verdict a
function of a concurrent session rather than of the repository's committed
content.

The comparison SHALL therefore name the committed revision it read the index
at, and SHALL read the corpus at the revision that index pins. A consequence
is stated rather than left implicit: an index edit under review is proved when
it is committed, not while it sits in a working tree. That is the intended
trade — a proof that changes its answer depending on who else is editing is
not a proof.

#### Scenario: Another session holds an uncommitted index edit
- **WHEN** a checkout on the machine carries an uncommitted change to `ideation/cross-reference.yaml`
- **THEN** the verdict MUST equal the verdict the same revision yields on a clean tree
- **AND** the run MUST NOT read that edit as the index under test

#### Scenario: The comparison assembles its two sides
- **WHEN** the comparison reads the index and the corpus
- **THEN** the index MUST be read at a named committed revision of the repository under test
- **AND** the corpus MUST be read at the revision that index itself pins

#### Scenario: The change under review edits the index
- **WHEN** a working tree carries an index edit that has not been committed
- **THEN** the proof MUST state that it read committed state and name the revision it read
- **AND** the edit MUST become subject to the proof once committed, rather than being proved from the working tree

### Requirement: An unreachable pinned revision fails the proof
An unreachable pinned `source_revision` SHALL fail the readiness derivation
proof whenever the repository under test is a complete clone, and SHALL be
reported as skipped only where the repository's history is genuinely truncated.

A pin the repository cannot resolve is not an environment inconvenience: it
means the index names a corpus state that no reader can reconstruct, so the
index's own provenance claim is unverifiable. Reporting that as a skip
converts a defect in the index into a silent absence of verification, and the
absence is invisible precisely because a skip looks like a healthy run.

The two conditions SHALL be distinguished by observation rather than by
supposition, and the reported reason SHALL name the condition observed. A
complete clone missing the object is a finding about the index; a truncated
history missing the object is a finding about the clone; and a reason that
guesses at the second while standing in the first is worse than no reason,
because it sends the reader to the wrong repair.

This obligation is on the verification, not on the nightly lane's findings:
the readiness lane's own output remains report-only under its owning
requirement, and nothing here makes a lane finding block a merge.

#### Scenario: The pin is unreachable in a complete clone
- **WHEN** the index pins a revision the repository under test cannot resolve, and that repository's history is not truncated
- **THEN** the proof MUST fail, naming the pinned revision and the index that carries it
- **AND** it MUST NOT be reported as a skip

#### Scenario: The clone is truncated
- **WHEN** the repository under test is shallow or its history is otherwise truncated, and the pinned revision lies outside the fetched history
- **THEN** the proof MAY be reported as skipped
- **AND** the reason MUST name the truncation actually observed rather than offering it as a conjecture

#### Scenario: The pin resolves
- **WHEN** the pinned revision resolves in the repository under test
- **THEN** the comparison MUST run and its result MUST be the verdict
- **AND** no resolution branch may return a skip in place of a comparison that could have been performed
