# shared-contract-ownership Specification Delta

## ADDED Requirements

### Requirement: Release reachability resolves its remote operand before it compares
Release verification SHALL make every remote-derived object locally resolvable
before it compares against that object, and SHALL NOT report a comparison it
could not perform as a fact about the candidate.

The online mode of release verification asks the canonical remote what its
`main` and its tags point at, and then answers questions about those object ids
inside a local clone. The two halves have different ages. A clone is fixed at
the moment it was taken; the remote's refs are not. When the remote's `main`
advances after the clone, the object the online read named is simply absent
locally, and every local operation over it fails for that reason alone —
`git merge-base --is-ancestor` exits 128 rather than 0 or 1, a tree read fails
outright, and a blob read resolves to nothing.

THE OBLIGATION IS ON THE OPERAND, NOT ON THE COMPARISON. Every remote-derived
object id the verification will read locally SHALL be resolved before it is
read: the remote's `main` tip, the object a published tag peels to, and any
further object a verification derives from them. Placing the obligation at the
comparison would repair one reader and leave every other reader of the same
absent object to fail in its own words — the release-surface comparison, the
tag's tree walk, and the per-member blob reads are all readers of the same
operand, and a repair that covers only the ancestor check merely moves which of
them reports the absence.

Making an object available MAY be a fetch from the remote that named it. This
requirement does not prescribe the incantation, only that the verification not
answer from a store it has not brought up to date with respect to the operand it
was handed.

THE MEANING OF REACHABILITY IS UNCHANGED AND MUST NOT BE WEAKENED. A candidate
SHALL still be required to be reachable from the canonical remote's `main`, and
a published tag's commit from published `main`. A verification MUST NOT satisfy
this requirement by relaxing what counts as reachable, by answering from a
remote-tracking ref in place of the remote, or by treating an unresolvable
comparison as a negative answer. The set of candidates the existing refusals
fire on is exactly the set they fire on today.

#### Scenario: The remote advances while the verification is running
- **WHEN** the canonical remote's `main` moves to a commit the local clone does not hold, between the clone being taken and the reachability comparison being made
- **THEN** the verification MUST make that object locally resolvable and complete the comparison
- **AND** it MUST report no finding attributable to the movement, because nothing about the candidate changed

#### Scenario: The candidate is genuinely not on published main
- **WHEN** the compared objects both resolve and the candidate is not an ancestor of the remote's `main`
- **THEN** the existing refusal MUST fire unchanged, naming the candidate as unreachable from remote `main`
- **AND** resolving the operand MUST NOT convert this answer into a pass

#### Scenario: A later reader of the same remote object runs
- **WHEN** a verification derives further reads from a remote-supplied object id — the release-surface comparison against the remote's `main`, or the tree and blobs of the commit a published tag peels to
- **THEN** those reads MUST also find the object resolvable, because the operand was resolved on entry rather than at one comparison
- **AND** an absent object MUST NOT surface as a drift finding, a missing member, or a generic tool failure

### Requirement: The reachability outcome names which condition was observed
Release verification SHALL distinguish three reachability outcomes and SHALL
name the one it observed: the candidate is not reachable, the comparison could
not be performed because an object could not be made available, or the objects
were reconciled and the comparison ran.

The three are different facts and today two of them arrive as one message. A
candidate that is not on published `main` is a verdict about the RELEASE, and it
belongs in the findings list under its existing code. An object that cannot be
made locally available — no network, no permission, a remote that declines to
serve it — is a fact about the ENVIRONMENT, and it belongs where unavailable
dependencies already go: a fail-closed refusal, distinct from a findings-bearing
result, whose reason names the retrieval that failed rather than announcing that
reachability could not be determined. Transient skew is the third, and it is
neither: it is resolved by the reconciliation and produces no finding and no
refusal at all.

FAIL-CLOSED IS PRESERVED IN FULL. An unanswerable reachability question SHALL
NOT resolve to a pass, and SHALL NOT resolve to a refusal finding either — a
verdict invented from an absence is wrong in both directions, and reporting an
unresolved operand as "not reachable" would fire the refusal on candidates that
are perfectly reachable. The refusal for an unanswerable question stays a
dependency refusal.

A REASON THAT GUESSES IS WORSE THAN A REASON THAT NAMES. The reported reason
SHALL name the condition actually observed, because the reader's next action
differs completely between the three: check the candidate, check the network or
the credential, or do nothing at all. A message asserting that reachability
"could not be determined" points at the verification's own uncertainty and sends
the reader to look at the candidate, which is the one place the answer is not.

#### Scenario: The object cannot be made available
- **WHEN** the remote named an object the clone does not hold and it cannot be retrieved — the remote is unreachable, the credential is refused, or the remote declines to serve it
- **THEN** the verification MUST fail closed as an unavailable dependency, not as a finding about the release
- **AND** the reason MUST name the retrieval that failed rather than reporting that reachability could not be determined

#### Scenario: The skew is reconciled
- **WHEN** the absent object is retrieved and the comparison then runs to a definite answer
- **THEN** the verification MUST report that answer and nothing else
- **AND** no finding, refusal, or warning MUST be attributed to the reconciliation

#### Scenario: An unresolved comparison is reported as a verdict
- **WHEN** a reachability comparison cannot be performed for any reason
- **THEN** the outcome MUST NOT be reported as the candidate being unreachable
- **AND** it MUST NOT be reported as the candidate being reachable

### Requirement: The skew and unavailable-object paths are pinned by executable proofs
Release verification SHALL carry executable proofs for both paths this
requirement family adds — a remote that has advanced beyond the clone, and an
object that cannot be made available — and each proof SHALL be pinned to the
defect it exists to prevent rather than to the shape of its fix.

The defect these requirements close was not caught by any test. It was caught by
a continuous-integration run failing twice and passing once over one unchanged
tree, which means the behaviour was outside everything the suite exercised. A
requirement about mechanics that carries no proof of those mechanics leaves the
next reader unable to tell whether the mechanics still hold, so the proofs are
part of the obligation rather than a consequence of it.

THE SKEW PROOF SHALL DRIVE THE CONDITION, NOT DESCRIBE IT: a fixture whose
declared remote holds a `main` the verifying clone does not, so that the
verification meets a genuinely absent object and must complete anyway. THE
UNAVAILABLE-OBJECT PROOF SHALL ESTABLISH THE REFUSAL AND ITS REASON: a fixture
where the object cannot be retrieved, asserting both that the verification
refuses and that the refusal names the retrieval rather than the candidate.

A PROOF MUST BE ABLE TO FAIL FOR THE RIGHT REASON. Each proof SHALL be
demonstrated to fail when the resolution step alone is removed, so that it is
pinned to the absent-object condition and cannot pass merely because the
surrounding verification happens to succeed. And no proof SHALL be written that
asserts a pass on a candidate genuinely absent from the remote's `main`, because
a test that permits the refusal to be lost is how the semantics this family
protects would quietly be traded away.

#### Scenario: The proof for a remote that advanced
- **WHEN** a fixture's declared remote carries a `main` commit the verifying clone does not hold
- **THEN** the proof MUST assert that the verification completes and returns the same result it returns against a current clone
- **AND** it MUST NOT reach that result by relaxing what reachability means

#### Scenario: The proof for an object that cannot be retrieved
- **WHEN** a fixture makes retrieval of the absent object impossible while the remote's refs are still readable
- **THEN** the proof MUST assert a fail-closed refusal rather than a finding
- **AND** it MUST assert that the refusal's reason names the failed retrieval

#### Scenario: A proof is checked against the defect it claims to prevent
- **WHEN** the resolution step is removed and the proofs are run
- **THEN** the skew proof MUST fail, reproducing the original refusal on an absent object
- **AND** a proof that still passes MUST be treated as unpinned and rewritten rather than accepted
