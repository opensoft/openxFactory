# shared-contract-ownership Specification

## Purpose
Defines how `openxFactory` owns shared factory contracts, how install repos pin
contract compatibility, how submodules are sequenced, and how evidence is
preserved from proposal through merge readiness.
## Requirements
### Requirement: Canonical contract home
`openxFactory` SHALL define the canonical home for shared factory contracts that
govern behavior between factory subsystems or across DomainxFactories. Migrated
contracts SHALL preserve source provenance and consumer compatibility
expectations. Domain-specific artifact schemas and workflow gate contracts MAY
live in the owning DomainxFactory when they preserve upstream `openxFactory`
references.

#### Scenario: Shared schema is introduced
- **WHEN** a schema or contract governs behavior between two or more factory subsystems or DomainxFactories
- **THEN** the canonical contract MUST be defined or referenced from `openxFactory/contracts/`

#### Scenario: Domain artifact schema is introduced
- **WHEN** a schema defines a domain-specific artifact such as a software PR admission packet, clinical review package, operations runbook result, ledger close packet, or campaign workflow artifact
- **THEN** the canonical implementation schema MUST live in the owning DomainxFactory
- **AND** the artifact MUST retain required upstream `openxFactory` scope, gate, and traceability references

#### Scenario: Subsystem adapter needs a contract
- **WHEN** an install repo needs a runtime adapter, generated client, smoke fixture, or pinned schema copy
- **THEN** the install repo MAY keep an implementation copy but MUST identify the corresponding `openxFactory` contract version or owning DomainxFactory contract version

#### Scenario: Existing schema is migrated
- **WHEN** a shared schema is copied from an install repo into `openxFactory/contracts/`
- **THEN** the canonical copy MUST identify the source path, intended consumers, compatibility reference, and adapter ownership rule

### Requirement: Contract version pinning
Install repositories SHALL pin compatible contract bundles from `openxFactory` before runtime adapters are treated as compatible. A governed bundle pin SHALL include the canonical repository, published bundle tag, exact repository commit, canonical manifest path/digest, release-inventory path/digest, and unique required contract entries containing contract ID, repository-relative path, schema version, and SHA-256 digest. Its own compatibility-manifest digest SHALL be bound from an external runtime manifest or realization record rather than self-recorded. Online Gate verification SHALL prove the annotated tag on the canonical remote; offline runtime verification SHALL resolve exact commit/tree/blob objects already present locally. Both modes SHALL fail closed for branch refs, tag-only refs, duplicate IDs or paths, missing bundle members, traversal, symlink escape, version mismatch, or digest drift. For this Gate G0 handoff, the consumer receipt SHALL require `opensoft/xFactory-Hermes-Install` and SHALL reject `FarHeap/Hermes-Install` before resolving downstream objects.

#### Scenario: Install repo consumes a contract
- **WHEN** `Hermes-Install` or `Omnigent-Install` consumes a shared contract
- **THEN** it MUST document and verify the exact published `openxFactory` bundle tag and commit
- **AND** it MUST pin the required contract paths, schema versions, and per-file digests

#### Scenario: Published tag is verified
- **WHEN** an install repository verifies a bundle pin
- **THEN** the tag MUST be annotated, published remotely, and dereference to the exact pinned commit
- **AND** the canonical manifest and changelog MUST declare the same bundle version

#### Scenario: Pinned file drifts
- **WHEN** bytes read from a pinned contract path at the exact commit do not match the recorded digest
- **THEN** compatibility validation MUST fail before runtime realization

#### Scenario: Runtime verifies without a network connection
- **WHEN** the exact pinned commit, trees, blobs, manifest, and release inventory are already present locally
- **THEN** offline verification MUST reproduce every required digest without consulting a mutable working tree

#### Scenario: Compatibility manifest is modified
- **WHEN** the compatibility manifest bytes do not match the digest bound by runtime or realization evidence
- **THEN** compatibility validation MUST fail

#### Scenario: Contract changes incompatibly
- **WHEN** a shared contract change would break an install repo adapter or smoke test
- **THEN** the change MUST be split from adapter migration or explicitly approved as a breaking change

#### Scenario: Existing consumer retains an older pin
- **WHEN** a consumer remains on an older valid bundle pin during an additive release
- **THEN** that consumer remains conformant to its pinned contract until it deliberately upgrades

### Requirement: Submodule sequencing
`openxFactory` SHALL document submodule intent and update procedures before
adding install repositories as submodules.

#### Scenario: Submodule is proposed
- **WHEN** a change proposes adding `Hermes-Install` or `Omnigent-Install` as a submodule
- **THEN** a decision record MUST document the remote, path, pinned commit, update process, and rollback process

#### Scenario: Hermes-Install remote is unresolved
- **WHEN** `Hermes-Install` still points to a non-Opensoft remote and the target umbrella repo is `opensoft/openxFactory`
- **THEN** the Hermes submodule MUST NOT be added until the move, fork, mirror, or external remote decision is approved

### Requirement: Evidence preservation
Each repo-boundary feature SHALL preserve traceability evidence from proposal
through merge readiness. Content migration features SHALL also preserve source
inventory and post-merge install repo link/update evidence where applicable.

#### Scenario: Feature proceeds to PR admission
- **WHEN** a repo-boundary feature is ready for PR
- **THEN** the feature MUST have a proposal or change record, acceptance criteria, implementation diff, local check result, branch review result, and PR admission packet

#### Scenario: Feature proceeds to merge
- **WHEN** a repo-boundary feature is considered for merge
- **THEN** merge council MUST have a merge readiness report that references the relevant OpenSpec change, feature slice, and evidence artifacts

#### Scenario: Content migration feature proceeds to merge
- **WHEN** a dogfood content migration feature is considered for merge
- **THEN** merge readiness MUST include source provenance, copy-first compliance, and evidence that source repos were not destructively changed in the same PR

### Requirement: Avatar-client contract ownership and consumer pinning
openxFactory SHALL own the canonical avatar-client contract kernel — the AVC
schemas, shared definitions, session-outcome, event, command, and
consent-purpose registries, fixtures, compatibility rules, and the
schema/fixture validator — under
`contracts/avatar-client/`, authored as YAML-serialized JSON Schema (draft
2020-12) and registered in `contracts/manifest.yaml` under the repository
contract changelog policy.

Each published bundle SHALL have one matching manifest version, changelog
entry, annotated tag, exact release commit, and per-file digests. Consumer
repositories SHALL own their language bindings and local adapters and SHALL
record the compatible bundle tag while pinning the exact openxFactory commit
and per-file digests. Bindings MAY be hand-written or generated; either way the consumer
SHALL prove conformance by executing the canonical valid, invalid,
compatibility, and redaction fixtures of the pinned contract release in its
CI. Provider DTOs, generated bindings, copied schemas, and client models
MUST NOT become canonical neutral semantics.

#### Scenario: Avatar runtime contract is introduced
- **WHEN** a schema governs shared session requests, results, events, confirmations, retention, personas, commands, or snapshots
- **THEN** its canonical schema, registry entries, and conformance fixtures MUST live under `openxFactory/contracts/avatar-client/`

#### Scenario: Contract bundle release identifiers disagree
- **WHEN** the manifest version, changelog release, annotated tag, release commit, or registered file digests do not identify the same realized bundle
- **THEN** release validation MUST fail and consumers MUST NOT be instructed to upgrade

#### Scenario: Consumer records only a contract tag
- **WHEN** a consumer records a bundle tag without the exact compatible commit and required file digests
- **THEN** consumer conformance MUST fail because the tag alone is not a content-addressed pin

#### Scenario: Client models drift from the pinned contract
- **WHEN** a consumer's models fail the canonical fixture suite of its pinned contract release
- **THEN** the consumer's release validation MUST fail

#### Scenario: Provider event is added
- **WHEN** a provider adds or changes an event or field
- **THEN** it MUST remain in the owning provider adapter unless a reviewed cross-provider semantic requirement justifies a neutral contract evolution

### Requirement: Avatar runtime reference ownership
openxFactory SHALL own the deterministic broker/control reference modules,
the fail-closed authority stub, the contract validator, and the server-side
provider adapter shape needed to prove the neutral contracts, all as
non-deployable reference code under `xfactory/avatar_runtime/`. Production
deployment, hosting, and operations SHALL be defined by the
live-qualification successor change consistent with repo-boundary
governance. The client repository SHALL own only distributable client
concerns.

DomainxFactories SHALL specialize through the avatar-first UI profile (the
domain overlay carrier), a mapping from neutral avatar purpose IDs to the
owning consent authority, and optional stricter domain purpose IDs, each
pinned to a compatible contract release. The memory-gateway consent profile
MAY be adapted by a domain but SHALL NOT become the neutral media-consent
contract. A domain overlay MUST NOT copy or fork the broker protocol,
authority rules, or canonical event and command vocabulary.

#### Scenario: Server-side provider integration is implemented
- **WHEN** code creates provider calls, holds a provider key, attaches sideband control, or configures tools and prompts
- **THEN** that code MUST live in the openxFactory reference runtime or a separately approved server trust boundary and MUST NOT live in the distributable client

#### Scenario: Domain overlay adopts the runtime
- **WHEN** a DomainxFactory publishes persona, speech-gate, consent-purpose, retention, or handoff specialization
- **THEN** it MUST identify its immutable overlay version, consent-authority mapping, and compatible contract release without redefining neutral authority or transport semantics

### Requirement: Tooling hosted in the publisher verifies released bytes, not a declared pin
Neutral tooling hosted inside `openxFactory` SHALL verify the shared contract it consumes by the released BYTES it reads — digest equality against its pinned value, and parity against the consumed checkout's own `contracts/manifest.yaml` — and SHALL NOT require the hosting repository to declare a consumption pin, because the publisher declares no pin on itself. A declared-pin check exists so that a consumer can never read one release while its repository declares another; that gap is real for a domain repo reading a submodule pin and structurally absent for tooling shipping inside the release it reads, and a question the publisher cannot honestly be asked MUST NOT be able to refuse it.

A checkout SHALL be treated as a publisher release only when it carries all of `contracts/manifest.yaml`, `contracts/schemas/`, and the contract family's own validator. Requiring every marker together is what separates a coherent release from a directory that merely contains a file with the right name — the same distinction manifest parity draws for a single schema, applied to the checkout as a whole. A tree missing any marker is NOT a publisher and SHALL take the consumer path with its declared pin intact.

Dropping the declared-pin question MUST NOT weaken any other link. The byte chain SHALL run unchanged and per request, and SHALL refuse on the request that first sees a drifted digest or a manifest disagreeing with its own bytes. Verification remains fail-closed throughout: an unreachable checkout, an absent schema, a digest mismatch, and a manifest disagreement each mean nothing may be treated as contract-conformant, and none of them may resolve to an implicit pass.

Nothing here changes how a consuming repository pins. A domain or install repo SHALL continue to declare the openxFactory release it consumes in its own `stack.yaml`, and tooling reading a contract from a checkout other than its own host SHALL continue to require that declaration.

#### Scenario: Tooling runs from a publisher checkout
- **WHEN** relocated neutral tooling loads a shared contract from the openxFactory checkout it is hosted in
- **THEN** the released bytes MUST be verified by digest and manifest parity
- **AND** the absence of a `stack.yaml` in that checkout MUST NOT refuse the load

#### Scenario: A consuming repository reads the same contract
- **WHEN** a domain or install repo consumes a shared contract from a pinned openxFactory checkout
- **THEN** its own declared `stack.yaml` consumption pin MUST still be required and MUST still be checked against the pinned release

#### Scenario: A release byte has drifted
- **WHEN** a consumed schema's bytes no longer hash to the pinned digest, or the checkout's manifest records a different digest than its own bytes
- **THEN** the load MUST refuse on the request that sees it
- **AND** publisher mode MUST NOT exempt it

#### Scenario: A tree only looks like a release
- **WHEN** the hosting repository carries some but not all of the publisher markers
- **THEN** it MUST NOT be treated as a publisher release
- **AND** the declared-pin requirement MUST apply to it unchanged

#### Scenario: A refusal reason cannot be established
- **WHEN** the consumed checkout cannot be resolved at all
- **THEN** verification MUST fail closed rather than treat the unanswered question as a pass

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

A TRUNCATED HISTORY IS A FOURTH WAY THE QUESTION CAN GO UNANSWERED, and it is
the one that hides behind a definite answer. Making an object locally resolvable
does not make the ANCESTRY between it and another object resolvable: a clone
whose history has been truncated carries a boundary that declares its oldest
commits parentless, so an ancestry query returns a definite NEGATIVE for a
commit that is reachable on the real history. Release verification SHALL NOT
report such a negative as a candidate or a tag being unreachable. A POSITIVE
answer needs no such care and SHALL be honoured wherever it is obtained, because
a path that was found is a path that exists; the obligation falls on the
negative alone, which is also what keeps the check off the ordinary path. Where
the store cannot bear the weight of its own negative, the outcome SHALL be the
fail-closed dependency refusal of this requirement, with a reason naming the
truncated history — and it SHALL be that refusal even when the negative happens
to be correct, because a verification that cannot tell an earned negative from
an artefact of its own store has not established which one it holds.

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

#### Scenario: A truncated history returns a negative it cannot earn
- **WHEN** the reachability comparison runs in a clone whose history is truncated and returns a negative answer
- **THEN** the verification MUST fail closed as an unavailable dependency naming the truncated history, not report the candidate or the tag as unreachable
- **AND** a positive answer in the same clone MUST still be honoured, because a path that was found is a path that exists

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

