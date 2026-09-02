# clearing-dispatch-boundary — Spec Delta

## MODIFIED Requirements

**Modified over `add-clearing-dispatch-boundary`'s addition by add-cpc-clearing-boundary (2026-09-01):** — that packet, ratified 2026-09-01, ADDS this capability and its ten requirements from the same operator ruling; this packet carries the ruling's SAME-DAY EXTENSION on `opensoft/codexFactory` issue #156, which the basis does not reach: per-factory ORIGIN KEYS registered in openxFactory and verified at clearing, and sign-on-return attestation. Only the two requirements the extension actually touches are modified, each carried VERBATIM from the ratified text with its additions marked in place and every original scenario retained; the eight requirements the extension does not touch are left to the basis and cited rather than restated. No eleventh manifest field, no second digest vocabulary, and no re-authoring of the basis's re-seal, dispatch-credential scoping, closed permitted-operations register, grandfather enumeration, or single-door attestation.

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
