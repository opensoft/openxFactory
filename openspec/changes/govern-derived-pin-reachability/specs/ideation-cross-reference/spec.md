# ideation-cross-reference Specification Delta

## ADDED Requirements

### Requirement: A committed derivation pin stays resolvable
A committed artifact SHALL pin, as its derivation source, only a repository
commit reachable from `main` — or from a retained ref the artifact or its
owning contract itself declares — at all times that the artifact stands on
`main`.

An unreachable pin is a DEFECT IN THE ARTIFACT, not staleness in it, and the
distinction is the whole of this requirement. A pin naming an older commit that
`main` still reaches is legal and expected: the artifact says "I was derived
from the corpus as it stood at X", a reader reconstructs the corpus at X, and
the provenance claim is verifiable even when the corpus has since moved. That
is the ordinary condition of every generated projection between regenerations,
and nothing here makes it a finding. A pin naming a commit no ref reaches makes
the same sentence unverifiable BY ANYONE: there is no state to reconstruct, so
the artifact's central claim about itself cannot be checked, confirmed, or
refuted. Reporting that as staleness understates it by a category.

The pinned commit's reachability SHALL be judged against refs, not against a
particular clone's object store. A commit an ancestor walk from `main` reaches
is conforming even in a clone that has not fetched it; a commit no ref reaches
is non-conforming even while it survives in some working clone's object store,
because that survival is an accident of local garbage collection rather than a
property of the repository.

The class this requirement reaches is REPO-LOCAL COMMIT PINS: a commit of the
same repository the artifact is committed to, recorded by that repository's own
generators as the state the artifact was derived from. `generation.source_revision`
on the cross-reference index and `source_revision` on this capability's
derivation and readiness evidence records are the members this capability owns.
Cross-repository pins are OUT and are governed elsewhere: an aggregation
gitlink, a `pinned_contract_manifest` entry, a release digest, and a container
image digest all name state in a repository other than the one recording them,
and their reachability question is answered against a different remote by a
different authority.

#### Scenario: The pin names an older commit that main still reaches
- **WHEN** a committed artifact pins a commit that is an ancestor of `main` but is no longer its tip
- **THEN** no finding is emitted under this requirement, because the pinned state is still reconstructible and staleness between regenerations is legal
- **AND** the artifact's provenance claim MUST be treated as verifiable rather than as merely old

#### Scenario: The pin names a commit no ref reaches
- **WHEN** a committed artifact standing on `main` pins a commit that is reachable from no ref, local or remote
- **THEN** it MUST be reported as a defect in that artifact, naming the artifact and the pinned commit
- **AND** it MUST NOT be reported as staleness, deferred to a regeneration schedule, or excused as an environment condition

#### Scenario: The pin resolves only through a retained ref
- **WHEN** a committed artifact pins a commit that `main` does not reach, and a retained ref declared by the artifact or its owning contract does reach it
- **THEN** the artifact is conforming, because the pinned state remains reconstructible by a reader who follows the declared ref
- **AND** the declaration MUST name the retained ref, so that reachability is verifiable without guessing which ref was meant

#### Scenario: A truncated clone cannot resolve a conforming pin
- **WHEN** a clone's history is shallow or otherwise truncated and cannot resolve a pin that `main` reaches
- **THEN** the condition MUST be reported against the clone rather than against the artifact
- **AND** the artifact MUST NOT be recorded as carrying an unreachable pin on the strength of a local absence

### Requirement: An orphaned pin on an immutable record is repaired by retention, never by editing the record
An orphaned derivation pin on an artifact whose status is `record` SHALL be
repaired by making the pinned commit reachable again, and MUST NOT be repaired
by editing the pin the record carries.

Two rules meet here and only one ordering of them is coherent. This
capability's derivation evidence is persisted as IMMUTABLE evidence, and
`document-lifecycle` makes a content edit to a `record` after capture a
finding in its own right. So the repair that works for a generated projection
— re-derive the body, re-pin, commit — is unavailable for a record: rewriting
the pin would replace one defect with another and would additionally falsify
the record, which exists to say what a run actually read. The pinned commit is
therefore what moves, not the record.

Retention SHALL be a published ref rather than a local one, because a pin whose
reachability depends on one machine's object store is unreachable by every
other reader and the requirement above is not satisfied by it. Retention is
also TIME-BOUND in a way no other repair in this repository is: an orphaned
commit survives only until garbage collection reaches it in the last clone
holding it, so a retention that is possible today may be impossible next week.
A packet that observes an orphaned pin on a record SHALL therefore establish
whether the object is still recoverable BEFORE proposing a route, and SHALL
record the answer it measured.

Where the pinned object is no longer recoverable anywhere, the record's bytes
still stand. The resolution SHALL be a SUPERSEDING record that names the loss
and what can and cannot now be verified, plus a disposition for the finding the
unrecoverable pin will keep producing. Silently rewriting the pin, deleting the
record, or leaving the finding unresolved and uncited are all refused: the
first falsifies the record, the second destroys the evidence the record is,
and the third converts a known defect into background noise.

#### Scenario: A record's pin is orphaned and the object is still recoverable
- **WHEN** an artifact with `status: record` carries a derivation pin no ref reaches, and the pinned object is still present in at least one clone
- **THEN** the repair MUST publish a ref that reaches that commit, leaving the record's own bytes unchanged
- **AND** the record MUST NOT be edited to name a different commit

#### Scenario: A record's pin is orphaned and the object is unrecoverable
- **WHEN** the pinned object is present in no clone and cannot be published
- **THEN** the resolution MUST be a superseding record naming the loss and what is no longer verifiable, together with a disposition for the standing finding
- **AND** the original record MUST NOT be edited or deleted to make the finding disappear

#### Scenario: A generated projection's pin is orphaned
- **WHEN** the orphaned pin is carried by a generated artifact that is not a `record` — the cross-reference index and its rendered twin among them
- **THEN** re-deriving the body and re-pinning it is the available repair, under the reproduction obligation the landing rule states
- **AND** the record-retention route is not owed for it, because nothing about a regenerable projection is immutable evidence

#### Scenario: A record's pin is edited in place
- **WHEN** a change edits the `source_revision` a captured record carries, for any reason including repairing an orphaned pin
- **THEN** the edit MUST be reported as a content edit to a `record` after capture
- **AND** the edit MUST NOT be accepted as the repair for the orphaned pin, because it makes the record state something the run did not read
