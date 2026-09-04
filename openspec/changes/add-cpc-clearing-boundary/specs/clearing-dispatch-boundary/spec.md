# clearing-dispatch-boundary — Spec Delta

## MODIFIED Requirements

### Requirement: Work crosses the boundary only as a sealed bounded request
Cross-repository work SHALL reach a governed execution host only as a SEALED
BOUNDED REQUEST, and the sealed request SHALL carry all TEN declared fields:
(1) the originating repository and workflow; (2) the source commit; (3) a
unique job id and an expiration; (4) the selected-file manifest with a hash
per file; (5) the permitted operation; (6) the required worker profile; (7)
the exact runner group and the unique dispatch label; (8) the output schema;
(9) the data-handling classification; and (10) a signature or trusted
hosted-workflow provenance.

The sealed request SHALL be a SHORT-LIVED SEALED JOB OBJECT and SHALL NOT be
a committed path of copied data in any repository: an expiring object is a
REQUEST, while a committed copy is a MIRROR that outlives the work, carries
the source's handling class into a second repository's permanent history, and
cannot distinguish two dispatches of the same content. A request whose
expiration has passed is refused rather than served, and a bundle carrying
selected files without their hashes, or hashes that do not match the files
carried, is refused.

Hashes and any bundle digest SHALL be computed with the ONE digest
construction `signed-execution-chain` already puts in force, and the sealed
request SHALL NOT define a second job-envelope, handling-classification, or
digest vocabulary; it seals a job expressed in existing vocabulary.


**Modified by `add-cpc-clearing-boundary`:** FIELD (10) SHALL NOT REMAIN A FREE
DISJUNCTION WHERE THE ORIGINATING REPOSITORY HOLDS A REGISTERED ORIGIN
IDENTITY. Where an active origin identity is registered for the originating
repository in the neutral factory-identity register, field (10) SHALL be an
ORIGIN SIGNATURE made by that identity over the manifest, and trusted
hosted-workflow provenance alone SHALL NOT satisfy it. Where no origin identity
is registered, field (10) is satisfied by trusted hosted-workflow provenance
exactly as the basis states, so registering an identity TIGHTENS a producer and
never loosens one, and the boundary stays usable by a producer that has not yet
been issued a key.

The signature SHALL cover ALL TEN DECLARED FIELDS, the per-file hashes
included, so that no field can be altered after signing without detection. NO
ELEVENTH FIELD IS ADDED AND NO SECOND VOCABULARY IS INTRODUCED: the signature is
computed over the ten fields the basis already declares, using the ONE digest
construction `signed-execution-chain` already puts in force, and this
modification defines no job-envelope, handling-classification, or digest rule of
its own.

TWO CONSTRUCTIONS ARE IN PLAY, AND NAMING BOTH IS WHAT KEEPS THIS FROM BEING A
SECOND VOCABULARY. The manifest is a JSON value: its digest, and the origin
signature computed over it, SHALL use the estate's canonical JSON construction
`xfc-jcs-sha256-1`, which requires the manifest to be admitted as a SUBJECT of
that construction's closed `digest_subject` enumeration — a tranche widening of
SUBJECTS, never a second construction, which is the one way that enumeration is
meant to move. Until that subject exists, this requirement is UNREALIZABLE as
written and SHALL NOT be reported as satisfied. PER-FILE CONTENT HASHES ARE NOT
JSON VALUES: they SHALL be plain algorithm-tagged SHA-256 over the file's BYTES.
A canonical-JSON construction has nothing to canonicalize in a byte stream, so
applying it to file content would be a category error rather than a stricter
rule. One construction for JSON values and one byte hash for file content —
both already in use, neither invented here.

**Modified over `add-clearing-dispatch-boundary`'s addition by add-cpc-clearing-boundary (2026-09-01):** — the basis ADDS this requirement and is ratified but unmerged; the ruling's same-day extension on codexFactory issue #156 closes field (10)'s disjunction for an originating repository that holds a registered origin identity. The ratified text is carried verbatim and every original scenario retained; the addition is additive and introduces no eleventh field and no second digest vocabulary.

#### Scenario: A conformant sealed request is presented
- **WHEN** a producer presents a sealed bounded request at the boundary
- **THEN** all ten declared fields MUST be present
- **AND** every selected file MUST carry a hash matching its bytes
- **AND** a missing or empty declared field MUST refuse the request with the field named

#### Scenario: A request is presented as committed data
- **WHEN** work is offered to the boundary as a committed folder, branch, or path of copied source rather than as a sealed job object
- **THEN** the offer MUST be refused
- **AND** the refusal MUST NOT be worked around by committing the bundle into the clearing repository

#### Scenario: An expired handle is replayed
- **WHEN** a sealed request whose declared expiration has passed is dispatched
- **THEN** the boundary MUST refuse it
- **AND** the refusal MUST be recorded as an expiry refusal rather than a transient failure

#### Scenario: A second digest rule is proposed
- **WHEN** a manifest hash or bundle digest is specified for the sealed request
- **THEN** it MUST use the digest construction already in force for the estate
- **AND** a new construction MUST NOT be defined by this capability


#### Scenario: A registered producer presents hosted provenance alone
- **WHEN** a sealed request's originating repository holds an active registered origin identity and its field (10) carries only trusted hosted-workflow provenance
- **THEN** the request MUST be refused
- **AND** the refusal MUST name the missing origin signature rather than report field (10) as present

#### Scenario: An unregistered producer presents hosted provenance
- **WHEN** a sealed request's originating repository holds no registered origin identity and its field (10) carries trusted hosted-workflow provenance
- **THEN** field (10) MUST be satisfied exactly as the basis states
- **AND** the absence of a registered identity MUST NOT by itself refuse the request

#### Scenario: The manifest has no admitted digest subject
- **WHEN** an origin signature over the manifest is required and the canonical JSON construction's `digest_subject` enumeration admits no manifest subject
- **THEN** the requirement MUST be reported as unrealizable rather than satisfied
- **AND** the remedy MUST be a tranche widening of subjects, never a second construction

#### Scenario: A canonical-JSON construction is applied to file bytes
- **WHEN** a per-file content hash is specified using the canonical JSON construction
- **THEN** it MUST be refused as a category error
- **AND** per-file content hashes MUST be algorithm-tagged SHA-256 over the file's bytes

#### Scenario: A signature covers less than the declared fields
- **WHEN** an origin signature covers some of the ten declared fields but not all of them, or does not cover the per-file hashes
- **THEN** the request MUST be refused
- **AND** a partial signature MUST NOT be reported as a signed manifest

### Requirement: Every verifiable field is verified against the provider's authoritative API
The clearing workflow SHALL verify each sealed-request field that has an
authoritative provider-side answer by resolving that answer from the
provider's API and comparing it, and SHALL NEVER accept a field as true
because the bundle asserts it. A bundle is a set of CLAIMS by its packager;
its internal consistency evidences only the packager's consistency.

The fields with an authoritative answer — the originating repository, the
originating workflow path, the source commit, the dispatching identity, and
the existence of the sealed object together with the run that produced it —
SHALL be resolved and compared before any dispatch. The fields with NO
authoritative provider answer — permitted operation, required worker profile,
output schema, and data-handling classification — SHALL be validated against
the closed permitted-operations register and against policy, and SHALL NOT
be reported as VERIFIED, because "verified" applied to a field nothing could
verify is precisely the false assurance this boundary exists to prevent.

A verification that cannot be performed SHALL refuse: an unreadable or
erroring provider API is not a verification that passed. The claimed value
SHALL be retained beside the resolved value in the dispatch record, because a
discarded claim makes a disagreement undetectable after the fact.


**Modified by `add-cpc-clearing-boundary`:** Two additions, neither widening the
field set the basis declares.

FIRST, THE ORIGIN SIGNATURE IS A THIRD VERIFICATION CLASS, distinct from the
provider-verifiable fields and from the policy-checked ones. Where the
originating repository holds an active registered origin identity, the clearing
workflow SHALL verify field (10)'s origin signature against the PUBLIC KEY
registered for that repository in the neutral factory-identity register — or
against a projection of that register whose staleness is bounded and declared —
and SHALL do so CONJUNCTIVELY with the provider-side resolution above. A
verifying signature over provenance the provider contradicts SHALL refuse, and
provider-confirmed provenance carrying no verifying signature SHALL refuse,
because each answers a question the other cannot: the provider says WHICH RUN
produced the object, and the signature says the originating repository's hosted
environment INTENDED THIS MANIFEST. The signature outcome SHALL be recorded as
its own outcome in the dispatch record and SHALL NOT be folded into the
provider-verified set, for the same reason the basis refuses to report a
policy-checked field as verified.

SECOND, THE POLICY-CHECKED FIELDS SHALL BE RESOLVED FROM THE REGISTER RATHER
THAN READ FROM THE BUNDLE. The permitted operation's class constraints, its
required worker profile, the lanes it may be dispatched to, and its declared
output schema SHALL be taken from the PERMITTED-OPERATIONS REGISTER ENTRY that
the operation id names, and the bundle's copies of those values SHALL be treated
as CLAIMS compared against the resolved entry rather than as the values the
dispatch runs on. Where a bundle's copy disagrees with the register entry, THE
REGISTER GOVERNS: the request SHALL be refused and the disagreement recorded,
rather than the dispatch proceeding on either value. Validating a claim against
the register and executing on the register's own answer are different acts, and
only the second denies a producer the ability to choose its own worker profile,
lane, or output schema by writing them into a bundle it controls.

**Modified over `add-clearing-dispatch-boundary`'s addition by add-cpc-clearing-boundary (2026-09-01):** — the basis ADDS this requirement and is ratified but unmerged; the same extension makes the origin signature a THIRD verification class, conjunctive with the provider resolution, and requires the policy-checked fields to be RESOLVED FROM the closed permitted-operations register rather than read from the bundle. The ratified text is carried verbatim and every original scenario retained; both additions tighten and neither loosens.

#### Scenario: The bundle names a workflow the provider contradicts
- **WHEN** the bundle's declared originating workflow path differs from the path the provider reports for the run that produced the sealed object
- **THEN** the dispatch MUST be refused before any runner is selected
- **AND** both the claimed and the resolved value MUST be recorded

#### Scenario: The claimed source commit does not match the run
- **WHEN** the bundle's declared source commit differs from the head commit the provider reports for the originating run
- **THEN** the dispatch MUST be refused

#### Scenario: The provider API cannot be read
- **WHEN** a required provider-side resolution fails, times out, or returns an error
- **THEN** the boundary MUST refuse the dispatch
- **AND** it MUST NOT proceed on the bundle's own assertion of the same fact

#### Scenario: A policy-checked field is reported
- **WHEN** the dispatch record reports on the permitted operation, worker profile, output schema, or data-handling classification
- **THEN** those fields MUST be reported as policy-checked against the register
- **AND** they MUST NOT be reported as provider-verified


#### Scenario: A valid signature over provenance the provider contradicts
- **WHEN** an origin signature verifies against the registered public key but the provider's API contradicts the originating repository, workflow path, source commit, or the run that produced the sealed object
- **THEN** the request MUST be refused
- **AND** the verifying signature MUST NOT be treated as curing the provider disagreement

#### Scenario: Provider-confirmed provenance with no verifying signature
- **WHEN** the provider's API confirms every field it can answer, the originating repository holds an active registered origin identity, and the origin signature is absent, malformed, or does not verify against the registered key
- **THEN** the request MUST be refused
- **AND** provider confirmation MUST NOT be treated as satisfying the origin check

#### Scenario: The bundle's worker profile disagrees with the register
- **WHEN** a sealed request carries a required worker profile, lane, or output schema differing from the permitted-operations register entry its operation id names
- **THEN** the request MUST be refused and the disagreement recorded
- **AND** the dispatch MUST NOT proceed on the register's value while ignoring the disagreement, nor on the bundle's value at all

#### Scenario: The register is the source of the operation's constraints
- **WHEN** a dispatch is prepared for a registered operation
- **THEN** the class constraints, worker profile, lane, and output schema it runs under MUST be those resolved from the register entry
- **AND** no value read from the bundle MUST determine what the operation is permitted to do

#### Scenario: The origin signature outcome is reported
- **WHEN** the dispatch record reports its verification outcomes
- **THEN** the origin-signature check MUST appear as its own outcome naming the register row and the key it resolved
- **AND** it MUST NOT be reported inside the provider-verified set

### Requirement: Every dispatch is recorded, and the single door is attested rather than assumed
The clearing workflow SHALL RECORD every dispatch it clears and every
request it refuses, and each record SHALL carry the verified provenance —
the resolved originating repository and workflow, the resolved source commit,
the job id, the operation, the runner group and dispatch label, the
data-handling classification, and the outcome — together with the CLAIMED
values where they differed from the resolved ones. A refusal SHALL be
recorded with its ground named FROM A CLOSED, NAMED ENUMERATION of refusal
grounds rather than as free text, because a boundary that logs only
successes cannot evidence what it stopped, and one that logs prose cannot be
counted.

AN OPERATION THAT CARRIES NO BUNDLE IS RECORDED FROM DECLARATIONS, and the
record SHALL say which values those are. Where a registered operation is
dispatched without a sealed bundle — as the first read-only operation is —
the record carries the REGISTER ENTRY'S DECLARED data-handling
classification, and, for each selected lane, that lane's DECLARED runner
group and DECLARED dispatch label. Those are declarations of the dispatch,
not observations of the host: OBSERVED group membership is established by the
periodic single-door attestation reading the provider's API, and SHALL NOT
be taken from the runner's own report of itself. A record that presented a
declared lane as an observed one would be asserting exactly the
self-corroboration this capability refuses everywhere else.

Because the door is single, that record IS the complete audit of everything
that ever reached the governed host. That completeness claim is TRUE ONLY
WHILE THE DOOR IS SINGLE, so the estate SHALL ATTEST the door periodically
rather than assume it: an attestation reads each governed runner group's
admitted repositories and workflow allowlist from the provider's API and
compares them against an expected set.

THE EXPECTED ALLOWLIST SHALL BE COMPUTED PER GROUP, not once for the estate.
For each governed runner group, the expected set is: THE CLEARING WORKFLOW'S
PATH, UNION the grandfather members ENUMERATED FOR THAT GROUP whose declared
allowlist-entry status is `present`. Computing one estate-wide expected set
instead would report every group as diverging from every other group's
members, which is a definition that cannot be green while more than one
group exists.

THE TWO DIVERGENCE DIRECTIONS ARE DISTINCT FINDINGS AND SHALL NOT BE
CONFLATED:

- AN OBSERVED ALLOWLIST ENTRY NOT DERIVABLE from that group's expected set
  is a WIDENING — a SINGLE-DOOR BREACH — and SHALL be a finding naming the
  group, the unexpected entry, and the expected set. An admitted repository
  other than the clearing repository is a widening of the same class.
- AN ENUMERATED MEMBER WITH NO OBSERVED ALLOWLIST ENTRY is NOT a breach: it
  is ALREADY FAILING CLOSED, nothing reaches the host through it, and it
  SHALL be raised as a DARK-LANE DISPOSITION ITEM — retire it into an
  operation, or remove the reference — rather than as a divergence of the
  door. Treating an unreachable lane as a breach would make the attestation
  red for a condition that is strictly safer than the expectation.

Likewise, THE CLEARING WORKFLOW'S PATH BEING ABSENT before the operator has
admitted it is the NOT-YET-CONVERGED state of requirement 1 and SHALL NOT be
reported as a widening; it is reported as convergence not yet reached.

The RESIDUAL SHALL be declared rather than implied: runner-group membership
and workflow allowlists are provider-side configuration outside the
repository's version control, changeable by an administrator with no pull
request. This contract does not make that configuration versioned, and it
SHALL NOT be read as claiming to; it makes a change to it OBSERVABLE within
one attestation cycle.

THE LEDGER'S COMPLETENESS CLAIM SHALL BE STATED AT THE STRENGTH THE CURRENT
ATTESTATION SUPPORTS, and that strength CHANGES at the operator acts, so the
two states SHALL be distinguished. BEFORE the clearing workflow's path is
admitted to every governed group and every non-clearing admitted repository
is removed, a green attestation attests the NARROWER claim: that no allowlist
entry outside each group's expected set exists, so nothing reaches the host
by a path the enumeration does not account for — while the ledger itself is
complete only for dispatches that came THROUGH THE DOOR, because the door is
not yet the only way in and is not yet open. AFTER those acts, a green
attestation supports the FULL claim: the door is single, so the ledger is the
complete record of everything that reached the host. A presentation of the
ledger as the complete audit SHALL cite a current, green attestation AND
SHALL NOT overstate which of those two claims that attestation carries.

The dispatch record SHALL NOT restate vocabulary another capability owns: it
REFERENCES a signed execution chain where one governs the work rather than
defining a second log, and it is distinct from the enrollment audit record,
whose subject is which hosts may BE runners rather than what was CLEARED to
one.

**Modified by `add-cpc-clearing-boundary`:** THE ATTESTATION ALSO READS THE
DISPATCH RECORD'S WORKSPACE-DISPOSAL FIELD. Because this packet makes disposal
evidence a field of the very record this requirement already governs, the
periodic attestation SHALL additionally report a dispatch record whose disposal
field is absent or empty as an UNATTESTED DISPOSAL, and SHALL NOT count such a
dispatch as clean. This adds a field to what the attestation reads and adds
nothing to what it authorizes: the completeness claim, the expected-set
comparison, and every refusal ground above are untouched.

**Modified over `add-clearing-dispatch-boundary`'s addition by add-cpc-clearing-boundary (2026-09-01):** — the basis ADDS this requirement and is ratified but unmerged; this packet's ADDED workspace-disposal requirement makes disposal evidence a field of the dispatch record THIS requirement governs, so the periodic attestation's read set grows by one field. Declared here rather than left as an implicit extension of a ratified requirement from outside it. The ratified text is carried verbatim, every original scenario retained, and nothing the attestation authorizes changes.

#### Scenario: A dispatch clears
- **WHEN** the clearing workflow admits a sealed request and dispatches it
- **THEN** a record MUST be written carrying the resolved provenance, the operation, the lane, the handling classification, and the outcome
- **AND** any claimed value that differed from the resolved value MUST be recorded beside it

#### Scenario: A request is refused
- **WHEN** the clearing workflow refuses a request for any ground in this capability
- **THEN** the refusal MUST be recorded with its ground named from the closed enumeration of refusal grounds
- **AND** a ground absent from that enumeration MUST be added by a governed change rather than recorded as free text

#### Scenario: An operation carrying no bundle is dispatched
- **WHEN** a registered operation is dispatched without a sealed bundle
- **THEN** the record MUST carry the register entry's DECLARED data-handling classification and each selected lane's DECLARED runner group and dispatch label
- **AND** those values MUST NOT be recorded as observed group membership, which only the single-door attestation establishes

#### Scenario: The attestation finds an extra allowlist entry
- **WHEN** a governed runner group's workflow allowlist contains a path that group's expected set does not derive — neither the clearing workflow nor a grandfather member enumerated for that group with allowlist status `present`
- **THEN** the attestation MUST report a WIDENING finding naming the group, the unexpected path, and the expected set

#### Scenario: The attestation finds an extra admitted repository
- **WHEN** a governed runner group admits a repository other than the clearing repository
- **THEN** the attestation MUST report a finding naming that repository

#### Scenario: An enumerated member holds no allowlist entry
- **WHEN** a grandfather member enumerated for a governed group holds no allowlist entry on that group
- **THEN** the attestation MUST NOT report it as a single-door breach
- **AND** it MUST be raised as a dark-lane disposition item, because that member is already failing closed

#### Scenario: The clearing path is not yet admitted
- **WHEN** the attestation runs before the operator has admitted the clearing workflow's path to a governed group
- **THEN** the absent clearing path MUST be reported as convergence not yet reached
- **AND** it MUST NOT be reported as a widening

#### Scenario: The completeness of the audit is claimed
- **WHEN** the dispatch record is presented as the complete audit of what reached the governed host
- **THEN** the claim MUST cite a current, green single-door attestation
- **AND** the claim MUST be stated at the strength that attestation supports, distinguishing the pre-admission narrower claim from the post-admission full claim
- **AND** without a green attestation the record MUST be presented as complete only for dispatches that came through the door

#### Scenario: A dispatch record carries no disposal evidence
- **WHEN** the periodic attestation reads a dispatch record whose workspace-disposal field is absent or empty
- **THEN** it MUST report an unattested disposal
- **AND** it MUST NOT count that dispatch as clean

## ADDED Requirements

### Requirement: Result attestation is produced on the originating repository's hosted infrastructure after the return verifies
Result attestation by an originating repository SHALL be produced on THAT
REPOSITORY'S OWN HOSTED INFRASTRUCTURE, after the sealed return's provenance and
digest have been verified, and SHALL NOT be produced on a governed execution
host. A governed execution host SHALL return
UNSIGNED results inside the sealed return, and no attestation private key —
seat, review, verdict-signing, or any other — SHALL be delivered to, stored on,
or reachable from a governed execution host, whatever the operation.

Verification SHALL PRECEDE SIGNING and not merely accompany it: the hosted
signer SHALL verify the return's digest and its provenance against the dispatch
record BEFORE producing any attestation, so that the signer cannot be turned
into an oracle that attests whatever a host returned. A return that fails either
check SHALL be refused unsigned.

#### Scenario: A key is proposed for the host so results are signed where produced
- **WHEN** a design would deliver an attestation private key to a governed execution host
- **THEN** it MUST be refused
- **AND** the host MUST return unsigned results instead

#### Scenario: A verified return is attested
- **WHEN** a sealed return's digest and provenance verify against the dispatch record on the originating repository's hosted infrastructure
- **THEN** the attestation is produced there, by keys that never left that infrastructure
- **AND** the attested result proceeds through the originating repository's normal completion path

#### Scenario: An unverified return reaches the signing step
- **WHEN** the sealed return's digest or provenance does not verify
- **THEN** nothing MUST be signed
- **AND** the return MUST be refused rather than attested with a caveat

### Requirement: Returned output is re-served to the originator from the clearing side's own sealed object
The clearing side SHALL RE-SEAL THE RETURN: output produced by a governed
execution host SHALL be admitted by the clearing side, verified, and then served
to the originating repository from the CLEARING SIDE'S OWN sealed object. The
originating repository SHALL NOT fetch, download, or otherwise read an artifact
belonging to the execution host's run, and SHALL NOT hold any credential scoped
to that run or to the execution estate.

This is the INBOUND half of the re-seal the basis states outbound, and it is
stated rather than left to symmetry. A sealed object belongs to the run that
produced it, so an originator reading the host's artifact directly would need a
credential into the execution estate — reintroducing, on the return path, exactly
the cross-boundary reach the outbound rule removes. The return SHALL therefore
cross the same way the request did: admitted, verified, re-sealed, re-served.

#### Scenario: The originator fetches the host's artifact
- **WHEN** an originating repository reads, downloads, or is granted access to an artifact belonging to a governed execution host's run
- **THEN** it MUST be refused
- **AND** the return MUST be served from the clearing side's own sealed object instead

#### Scenario: A return is re-served
- **WHEN** a governed execution host's output is admitted and verified by the clearing side
- **THEN** the clearing side seals its own object and serves the originator from it
- **AND** the originator holds no credential scoped to the execution estate

#### Scenario: A credential into the estate is proposed for the originator
- **WHEN** a design would give an originating repository a credential scoped to the execution estate so it can collect its own results
- **THEN** it MUST be refused as reintroducing the reach the boundary exists to remove

### Requirement: Workspace disposal evidence is a recorded field of the dispatch record
A dispatch SHALL leave no residue on a governed execution host: the staged
bundle, every artifact derived from it, and the workspace itself SHALL be
disposed of when the dispatch reaches a terminal state, INCLUDING on failure,
refusal, and timeout.

The evidence of that disposal SHALL be a FIELD OF THE DISPATCH RECORD the
basis already requires for every dispatch, so that it is carried by a record
that already exists, is already written for admissions and refusals alike, and
whose completeness the basis already attests rather than assumes. A dispatch
record whose disposal field is absent or empty SHALL NOT be read as evidence of
a clean host, and the periodic attestation that reads those records SHALL
report it as an unattested disposal rather than passing it.

#### Scenario: A dispatch fails mid-execution
- **WHEN** execution fails, is refused, or times out
- **THEN** the workspace MUST be disposed of exactly as on success
- **AND** the disposal evidence MUST be written to the dispatch record for that dispatch

#### Scenario: A dispatch record carries no disposal evidence
- **WHEN** a dispatch record's disposal field is absent or empty
- **THEN** the attestation MUST report it as an unattested disposal
- **AND** it MUST NOT be counted as a clean dispatch

#### Scenario: A disposal claim is made outside the record
- **WHEN** disposal is asserted only in job logs or a workflow summary
- **THEN** it MUST NOT satisfy this requirement
- **AND** the dispatch record's own field MUST be the evidence read
