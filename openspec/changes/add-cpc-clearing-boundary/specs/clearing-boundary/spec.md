# clearing-boundary — Spec Delta

## ADDED Requirements

### Requirement: Cross-boundary work reaches an execution estate only as a sealed bounded request
Work that an ORIGINATING FACTORY wants executed inside an EXECUTION ESTATE it does not own SHALL reach that estate only as a SEALED BOUNDED REQUEST admitted by a CLEARING BOUNDARY, and an originating factory MUST NOT be broadly authorized to originate execution in that estate directly. The clearing boundary is the single admission point: it is the only party the estate's execution surface accepts work from, and it decides admission per request rather than per repository. Broad standing authorization for an originating factory — repository-wide access to the estate's execution surface — SHALL be REFUSED; where a direct path is later granted at all, it MUST be a single exact named workflow path on a protected branch, never a repository.

#### Scenario: A factory attempts to originate execution directly
- **WHEN** an originating factory dispatches work at an execution estate's execution surface without passing the clearing boundary
- **THEN** the work MUST be unclaimable by design — the estate's execution surface does not accept it
- **AND** the refusal is a contract outcome, not an incident

#### Scenario: A factory originates work lawfully
- **WHEN** an originating factory needs work executed in an estate it does not own
- **THEN** it packages a sealed bounded request and submits it to the clearing boundary
- **AND** the clearing boundary, not the factory, selects the execution target

#### Scenario: Repository-wide authorization is requested
- **WHEN** a proposal would authorize an originating factory's repository at an execution estate's execution surface
- **THEN** it MUST be refused, and any narrower grant MUST name one exact workflow path on a protected branch

### Requirement: The sealed bounded request carries a complete, enumerated manifest
A sealed bounded request SHALL carry a signed MANIFEST enumerating, at minimum and by name: the originating repository and the originating workflow; the source commit revision the request was built from; a unique job identifier and an EXPIRATION; the selected-file manifest with a per-file content hash for every member; the digest of the bundle as a whole; the PERMITTED OPERATION; the required worker profile; the exact execution group and a UNIQUE DISPATCH LABEL; the declared OUTPUT SCHEMA; the data-handling classification; and an ORIGIN SIGNATURE (or an equivalent attestation of trusted hosted-workflow provenance). A manifest missing any enumerated field SHALL be refused; the bundle SHALL carry only the selected files and MUST NOT carry any credential, token, or key material as a member.

#### Scenario: An incomplete manifest is submitted
- **WHEN** a sealed bounded request omits any enumerated manifest field, or carries a file with no declared hash
- **THEN** clearing refuses it and records the refusal naming the missing field
- **AND** nothing is dispatched

#### Scenario: A credential is packaged as a bundle member
- **WHEN** a bundle carries a token, key, or credential as a member — declared or undeclared
- **THEN** clearing refuses the request
- **AND** no credential is ever a bundle member, whatever the permitted operation

#### Scenario: A complete manifest is submitted
- **WHEN** every enumerated field is present, every selected file carries a hash, and the bundle digest covers the whole bundle
- **THEN** the request is eligible for verification

### Requirement: Clearing verifies every manifest claim against the platform's authoritative API
The clearing boundary SHALL verify the manifest's provenance claims — originating repository, originating workflow, source revision, and the hosted run that produced the bundle — against the hosting PLATFORM's authoritative API, and MUST NOT accept those claims because the bundle asserts them. Fields inside the bundle are UNTRUSTED INPUT to be checked, never evidence. Verification SHALL be conjunctive: platform provenance and origin-signature verification are both required, and neither substitutes for the other.

#### Scenario: A bundle asserts a provenance it does not have
- **WHEN** a manifest names an originating repository, workflow, or source revision that the platform API does not confirm for the run that produced the bundle
- **THEN** clearing refuses the request and records the mismatch
- **AND** the assertion inside the bundle is given no weight

#### Scenario: A valid origin signature over false provenance
- **WHEN** a manifest carries a correctly verifying origin signature but its platform provenance check fails
- **THEN** clearing refuses — a valid signature does not substitute for platform provenance

#### Scenario: Correct provenance with no valid origin signature
- **WHEN** the platform API confirms the run, repository, workflow, and revision, but the origin signature is absent, malformed, or does not verify against the registered origin key
- **THEN** clearing refuses — platform provenance does not substitute for origin attestation

### Requirement: A cleared dispatch is single-use, expiring, and bound to its unique label
Clearing SHALL admit a sealed bounded request at most ONCE: the unique job identifier MUST NOT clear twice, a request presented after its declared expiration SHALL be refused, and the dispatch SHALL be bound to the unique dispatch label named in the manifest so that exactly one execution target can claim it. Replaying a previously cleared bundle, re-presenting an expired one, or claiming a dispatch under any other label SHALL be refused.

#### Scenario: A cleared bundle is replayed
- **WHEN** a sealed bounded request bearing a job identifier that has already cleared is submitted again
- **THEN** clearing refuses the replay and records it

#### Scenario: An expired request arrives
- **WHEN** a request is presented after the expiration its own manifest declares
- **THEN** clearing refuses it regardless of the validity of every other field

#### Scenario: A dispatch is claimed under the wrong label
- **WHEN** an execution target attempts to claim a cleared dispatch under a label other than the unique dispatch label the clearing decision bound
- **THEN** the claim MUST NOT succeed

### Requirement: The clearing surface is a short-lived sealed job object, never a committed folder
The surface a sealed bundle travels on SHALL be a SHORT-LIVED sealed job object — a build artifact or equivalent expiring object — and MUST NOT be a committed folder of copied data in any repository. The bundle SHALL NOT be retained past the dispatch it serves; the durable record of the transaction is the clearing AUDIT RECORD and the manifest digests it names, not the bundle payload.

#### Scenario: A packaging step commits the bundle
- **WHEN** a realization would carry the selected files into a repository as committed content in order to move them
- **THEN** it violates this contract and MUST be refused in review
- **AND** the sealed short-lived job object is the only sanctioned carrier

#### Scenario: The dispatch completes
- **WHEN** a cleared dispatch reaches a terminal state
- **THEN** the sealed job object expires or is deleted
- **AND** the audit record and the digests it names survive as the durable evidence

### Requirement: The execution target receives only the sealed bundle
The execution target SHALL receive ONLY the sealed bundle and its declared permitted operation. It MUST NOT clone, check out, or otherwise fetch the originating factory's repository, and it MUST NOT be handed any repository credential, registry credential, or attestation key. Before executing, the target SHALL RECOMPUTE the bundle digest and every per-file hash and compare them to the manifest, and SHALL refuse to execute on any mismatch. Execution SHALL be confined to the permitted operation the manifest declares.

#### Scenario: A staged bundle does not match its manifest
- **WHEN** the recomputed bundle digest or any per-file hash differs from the manifest value
- **THEN** the target refuses to execute and reports the mismatch
- **AND** nothing from the bundle is run

#### Scenario: The target attempts an operation outside the permitted one
- **WHEN** work staged from the bundle attempts an operation the manifest did not permit
- **THEN** the attempt is refused and the dispatch fails closed

#### Scenario: A compromised originating workflow
- **WHEN** an originating factory's workflow is compromised and packages hostile content
- **THEN** the blast radius is bounded by the permitted operation, the absent credentials, and the absent repository access — a compromised originating workflow MUST NOT be able to execute arbitrary commands in the execution estate

### Requirement: Returned results validate on hosted infrastructure before affecting any repository
A returned result SHALL be a SEALED RETURN — the declared outputs and a structured result, carrying its own digest — and it SHALL be validated against the manifest's declared OUTPUT SCHEMA on HOSTED infrastructure, together with whatever tests the permitted operation requires, BEFORE it is allowed to affect any repository. A result that fails schema validation, digest verification, or the required tests SHALL be refused, and no repository state SHALL change on the strength of anything the execution target returned unvalidated.

#### Scenario: A result violates its declared output schema
- **WHEN** the sealed return does not validate against the output schema the manifest declared
- **THEN** it is refused on hosted infrastructure and no repository is touched

#### Scenario: A result arrives with an unverifiable digest
- **WHEN** the sealed return's digest does not verify, or names a job identifier that was never cleared
- **THEN** it is refused before any validation of its content is attempted

#### Scenario: A valid result is admitted
- **WHEN** the sealed return verifies, validates against the declared output schema, and passes the required tests on hosted infrastructure
- **THEN** it becomes eligible to affect a repository through the normal governed path

### Requirement: The execution workspace is wiped and the wipe is proven
An execution target SHALL leave no residue of a dispatch: the staged bundle, every derived artifact, and the workspace itself SHALL be wiped when the dispatch reaches a terminal state — including on failure, refusal, and timeout — and the wipe SHALL be PROVEN by evidence carried in the dispatch record, not merely attempted. A dispatch whose wipe cannot be proven SHALL be reported as a governance finding.

#### Scenario: A dispatch fails mid-execution
- **WHEN** execution fails, is refused, or times out
- **THEN** the workspace is wiped exactly as on success
- **AND** the wipe evidence is recorded

#### Scenario: Wipe evidence is missing
- **WHEN** a dispatch record carries no wipe proof
- **THEN** the dispatch is reported as a finding rather than treated as clean

### Requirement: Result attestation is signed on hosted infrastructure after the return is verified
Where a returned result must be ATTESTED by the originating factory, that attestation SHALL be produced on the originating factory's HOSTED infrastructure, AFTER the sealed return's provenance and digest have been verified, and never inside the execution estate. Attestation private keys — including seat, review, and any verdict-signing keys — MUST NOT be placed in, delivered to, or reachable from any execution target; the execution target SHALL produce UNSIGNED results inside the sealed return. Sign-on-return SHALL NOT require re-minting or relocating any existing attestation key.

#### Scenario: The estate is asked to sign
- **WHEN** a design would deliver an attestation private key to an execution target so results can be signed where they are produced
- **THEN** it MUST be refused — attestation keys never enter the execution estate

#### Scenario: A verified return is attested
- **WHEN** a sealed return's provenance and digest verify on the originating factory's hosted infrastructure
- **THEN** the hosted workflow signs the results there, using keys that never left it
- **AND** the attested result proceeds through the originating factory's normal completion path

#### Scenario: An unverified return reaches the signing step
- **WHEN** the sealed return's provenance or digest does not verify
- **THEN** nothing is signed and the return is refused

### Requirement: Every clearing decision is recorded, and the boundary is the throttle and shutdown point
The clearing boundary SHALL record an AUDIT RECORD for every decision it takes — admissions and REFUSALS alike — naming the originating factory, the job identifier, the manifest digests, the verification outcomes, and the selected execution target. Because it is the single admission point, the clearing boundary SHALL also be the one place where rate limiting, policy, and EMERGENCY SHUTDOWN for the estate are exercised: halting the clearing boundary SHALL halt all cross-boundary execution in that estate. No audit record SHALL contain credential or key material.

#### Scenario: A request is refused
- **WHEN** clearing refuses a sealed bounded request for any reason
- **THEN** an audit record is written naming the reason, exactly as for an admission

#### Scenario: The estate must be stopped
- **WHEN** an operator needs to stop all cross-boundary execution in an execution estate
- **THEN** halting the clearing boundary is sufficient — there is no second admission path to close

#### Scenario: An audit record is inspected
- **WHEN** any clearing audit record is read
- **THEN** it names the decision, the factory, the job, the digests, and the outcome
- **AND** it contains no credential, token, or key material

### Requirement: Estate readiness is the clearing lane's first operation
Verifying that an execution estate can actually claim and run a cleared dispatch SHALL be expressed as the clearing lane's FIRST OPERATION — a permitted operation of the clearing boundary — and MUST NOT be added as a separate per-path authorization at the estate's execution surface. The estate's authorization surface SHALL therefore converge to ONE permanent entry per execution group: the clearing boundary itself. Standalone readiness or diagnostic paths that hold their own authorization SHALL be retired into the clearing operation.

#### Scenario: A new readiness path is proposed
- **WHEN** a proposal would add a per-path authorization entry so a readiness or diagnostic workflow can reach an execution group
- **THEN** it MUST be refused, and readiness MUST be expressed as a clearing-lane operation instead

#### Scenario: The authorization surface is audited
- **WHEN** an execution group's authorization entries are inspected after this contract is realized
- **THEN** exactly one permanent entry — the clearing boundary — is present per group

#### Scenario: An existing standalone diagnostic exists
- **WHEN** a standalone readiness workflow already holds its own authorization at an execution group
- **THEN** it is retired into the clearing operation as part of realization, not kept alongside it
