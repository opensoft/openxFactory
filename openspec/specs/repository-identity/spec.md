# repository-identity Specification

## Purpose

Govern the repository name itself as a NORMATIVE VALUE, not a label, for the
case where a governed repository changes organizations. A repository address
appears in governed content in four incompatible roles at once — as a key in a
regression denominator that gates bundle publication, as the pinned identity of
a decision core another repository checks out, as the holder and object
narrowing of a signing grant, and as prose in dated records — and a transfer
cannot treat those alike. So this capability states which occurrences MUST be
respelled, which are frozen by construction because a signature or a dated
record covers them, how a disposition is published as a rule with a recorded
sweep instead of being decided occurrence by occurrence, and why a reference
across organizations is an identity that must be re-established rather than a
redirect that can be ridden.

The transfer mapping this capability's requirements read — the published
`former` → `current` record itself — is authored by
`adopt-medxsoft-repository-identity` and is not restated here.

## Requirements

### Requirement: A cryptographically covered former identity is frozen by construction
A former repository identity carried inside bytes covered by a signature or a digest the repository cannot reproduce SHALL NOT be respelled, and MUST be resolved through the published transfer mapping instead.
This is a SECOND and INDEPENDENT freeze arm, and it binds even where the
records-and-assertions test would have ordered a rename. Where a validator
recomputes a digest over a named subject, or verifies a signature over that
subject's canonical bytes, a one-character edit inside the subject changes the
canonical serialization and invalidates both. Where the signing key's private
half is deliberately absent — as it is for a packaged fixture corpus whose whole
value is that it is self-checking — there is no repair: the rename does not
produce a stale example, it produces a broken one with no path back. The
disposition is therefore arithmetic rather than policy, and a ruling that the
string "asserts what is" cannot override it.

#### Scenario: A transferred repository is named inside a signed block
- **WHEN** a former identity appears inside a block covered by a verified signature or by a digest the validator recomputes
- **THEN** the bytes MUST NOT change
- **AND** the transfer mapping MUST supply the current identity to any reader who needs it

#### Scenario: The signing key is unavailable by design
- **WHEN** re-signing would be the only way to respell such a surface and the private key exists nowhere in the repository
- **THEN** the surface MUST be recorded as frozen by construction rather than left as outstanding rename work
- **AND** the change MUST NOT count that surface toward the release-surface arithmetic, no byte of it having moved

#### Scenario: A rename proposal reaches a covered surface
- **WHEN** a sweep classifies occurrences for rename
- **THEN** it MUST test coverage by signature or digest BEFORE applying the records-and-assertions test
- **AND** an occurrence that fails the coverage test MUST be dispositioned frozen whatever the second test would have said

### Requirement: A repository identity that is an authorization scope is re-issued with the transfer
Where a governed grant, register row, or wallet record names a repository as its holder or as the object its authority is narrowed to, the transfer SHALL re-issue those records in the same governed act that renames the live surfaces.
A repository identity used this way is not a label: it is the scope a signature
evidences. After a transfer the record evidences origination or authority for an
address that no longer exists, and a consumer comparing a request's declared
repository against the register REFUSES rather than degrading. The transfer
therefore revokes the authority until the records are re-issued, and the
re-issuance is not optional follow-on work. Where a transfer moves the OWNER
SEGMENT ONLY, re-issuance means respelling the existing records: the key
material, its custody, its identifier and its fingerprint are unchanged by a
transfer, so a new wallet, a new grant, a new register row or a re-mint asserts a
change that did not happen and may collide with a reader that refuses concurrent
active rows for one repository.

#### Scenario: An origin grant narrows to the transferred repository
- **WHEN** a grant's object narrowing or holder reference names the former identity
- **THEN** the change that renames live surfaces MUST also re-issue that grant, its backing register row and its wallet record
- **AND** it MUST NOT widen the narrowing to carry both identities

#### Scenario: The re-issuance surface is human-only
- **WHEN** the records being re-issued sit on a surface declared never-clearable by any autonomous or council path
- **THEN** the realizing pull request MUST be merged on a human word
- **AND** the change MUST state that constraint rather than leave it to be discovered by a fail-closed gate

#### Scenario: Only the owner segment moved
- **WHEN** re-issuance is performed for an owner-segment transfer
- **THEN** the key material, key identifier, fingerprint and custody attestation MUST be carried unchanged
- **AND** any expiry ceiling MUST NOT be extended by the identity respell, renewal being a separate governed act

### Requirement: A transfer disposition is a published rule with a recorded sweep
A transfer whose live occurrences exceed reliable hand enumeration SHALL declare its disposition as a rule over path classes and MUST record a reproducible sweep whose output is the evidence.
Per-occurrence enumeration is the correct instrument at small scale and fails at
large scale in three measurable ways: the list goes stale while review is still
running, it invites a reviewer to verify the list rather than the tree, and it
inflates the front-matter surface a strict loader must accept. The replacement
carries the same obligations and no fewer: every occurrence is accounted for,
each path class carries one stated disposition, and the counts close exactly
across rename, frozen and not-swept. A NOT-SWEPT class is a distinct disposition
from a FROZEN one and MUST be recorded separately, because a surface left to
another owner is not a surface protected from edits.

#### Scenario: The disposition is declared by class
- **WHEN** a transfer change declares its code surface
- **THEN** it MUST state one disposition for each path class it touches
- **AND** the per-class counts MUST sum to the measured total for both occurrences and files

#### Scenario: Occurrences belong to another lane's unmerged work
- **WHEN** a former identity appears in a change packet that is neither archived nor owned by the transferring change
- **THEN** those occurrences MUST be recorded as NOT SWEPT with the owner named, rather than as frozen or as remaining rename work
- **AND** the mapping MUST resolve them whether the owning lane respells them or archives them as written

#### Scenario: The sweep is re-run at realization
- **WHEN** the rename work is performed
- **THEN** the recorded sweep MUST be re-run and its output filed as the change's evidence
- **AND** any occurrence appearing since the proposal MUST be classified by the published rule rather than by a fresh judgment

### Requirement: A cross-organization governed reference is an identity, not a redirect
A governed reference that resolves a repository across an organization boundary SHALL be repointed at the transfer, and its reachability MUST be established before the transfer rather than assumed from a provider redirect.
Host redirects do not cover every reference shape. A workflow-to-workflow
reference resolved by the provider's own runner, a container package namespace,
and a federated-credential subject string are each scoped to the owning
organization and are broken or unreachable the moment the owner changes,
independently of whether a clone still redirects. Where such a reference is
pinned by a governed artifact, the pin and every artifact that asserts the pin
move in ONE act, so that no window exists in which the governed artifacts
disagree about where the referenced repository is.

#### Scenario: A pinned reference names the repository across organizations
- **WHEN** a governed pin dispatches or checks out a repository under a former owner
- **THEN** the pin, every workflow that carries it, and every test that asserts it MUST move in one commit
- **AND** the change MUST NOT rely on a provider redirect to keep the reference resolving

#### Scenario: Reachability is not yet established
- **WHEN** the destination organization cannot yet be reached by the calling organization under the reference's access rules
- **THEN** establishing that reachability MUST precede the transfer
- **AND** the transfer MUST NOT proceed on the expectation that the reference will be repaired afterwards

#### Scenario: A package namespace is organization-scoped
- **WHEN** an artifact is published under a namespace derived from the owning organization
- **THEN** the new namespace MUST be published and resolvable BEFORE any consumer allowlist or pinned record is flipped to it
- **AND** the allowlist, the pinned record and every test asserting either MUST flip together, the consumer being fail-closed in between
