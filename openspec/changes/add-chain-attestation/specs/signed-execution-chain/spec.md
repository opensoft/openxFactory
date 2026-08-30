# signed-execution-chain Specification (delta)

## ADDED Requirements

### Requirement: The harness controller attests the environment it prepared

openxFactory SHALL require a HARNESS-CONTROLLER SETUP ATTESTATION — link 4 —
recording the environment the controller PREPARED before any runner executes:
the model surface, the harness and its version, the toolchain, and the
workspace provenance it provisioned. The attestation is signed under a
CONTROLLER CERTIFICATE and is the CORROBORATION SOURCE for link 5. It is the
first link in this family with a signer of its own, and the hash-linking rule
below takes effect at it.

**THE CERTIFICATE IS EXPRESSED IN `add-trust-anchor`'s VOCABULARY AND THIS
CAPABILITY DEFINES NO SECOND ONE.** That change's ratified text governs, and
four of its obligations bind here by composition rather than by restatement:
the controller certificate is trusted THROUGH AN ANCHOR RECORD the evaluating
gate already holds and never on its own strength, so a chain terminating in no
held anchor is refused with the missing anchor named; it issues only under a
RECORDED AUTHORITY with an ISSUANCE EVIDENCE record establishing which anchor
issued, under which authority, on whose request and when; its DECLARED CUSTODY
bounds what its signature evidences, so a host-readable key evidences that the
HOST acted and may not be presented for an assurance requiring hardware-bound
custody; and REVOCATION IS CHECKED AT USE rather than trusted from issuance,
propagating transitively from a revoked anchor to the authority its
subordinates supported.

**THE ISSUING AUTHORITY IS A REALIZATION DEPENDENCY AND IS NOT ASSUMED HERE.**
The runtime certificate authority is the one `implement-openxpki-install-repo`
creates at `opensoft/OpenXPKI-Install`, which openxFactory does not operate:
that change's ratified boundary keeps openxFactory the canonical owner of the
neutral `trust-anchor` contract while the install repository realizes it and
owns neither. This capability therefore creates NO certificate authority, NO
issuance pipeline and NO key service. Where the operated authority exposes less
than an obligation above requires, the realization DECLARES the shortfall under
`add-trust-anchor`'s conformance-declaration rule rather than recording evidence
it does not have — an undeclared shortfall is non-conformance, and the identical
shortfall declared is conformant.

**REVOCATION AFTER SIGNING IS TREATED ON THE FAMILY'S TWO-HORIZON DOCTRINE, AND
THIS IS A DESIGN DECISION RATHER THAN A RULING.** The attestation carries the
controller's revocation standing AS CHECKED AT SIGNING; a certificate already
revoked at signing makes the attestation refused outright. A certificate revoked
AFTER a signature was made does not retroactively unmake an act the gate already
permitted — it refuses everything the chain has not yet been permitted for, which
is the same horizon rule link 10's closure requirement states below.

#### Scenario: a controller certificate chains to no anchor the gate holds

- WHEN a setup attestation is presented under a certificate whose chain terminates in no anchor record the evaluating gate holds
- THEN it is REFUSED and the missing anchor is named
- AND the certificate's well-formedness is not accepted in place of an anchor

#### Scenario: a host-held controller key is offered for a hardware-bound assurance

- WHEN a controller certificate declaring host-readable custody is offered for an authority requiring hardware-bound custody
- THEN the request is REFUSED with the custody ceiling named
- AND what the signature evidences is derived from the declared custody, never from the certificate's contents

#### Scenario: the operated authority cannot evidence issuance provenance

- WHEN the realization cannot extract per-certificate request provenance from the certificate authority it does not operate
- THEN it DECLARES the shortfall and records only what it can establish
- AND asserting unestablished provenance is a validation failure, while the declared gap leaves it conformant

#### Scenario: link 4 is absent and runner attestations are offered anyway

- WHEN runner attestations are presented for a chain carrying no setup attestation
- THEN they are REFUSED, because they have no issuer to chain to and nothing to be corroborated against
- AND the absence is reported as a broken link, never as a controller that had nothing to say

#### Scenario: a setup attestation records nothing the controller provisioned

- WHEN a setup attestation is well-formed and records no provisioned fact
- THEN it is REFUSED, because link 5's corroboration would have nothing to read
- AND an empty attestation is never accepted as a link that merely says little

### Requirement: A runner attestation is produced at the controller, on a recorded request

openxFactory SHALL require every RUNNER ATTESTATION — link 5 — to be signed AT
THE HARNESS CONTROLLER under a PER-TASK TIER-2 ATTESTATION IDENTITY, by REMOTE
SIGNING SERVED BY THE CONTROLLER, and SHALL require the runner's SIGNING REQUEST
to be RECORDED ALONGSIDE the signature it received. The attestation says what
ran — this model, at this version, under this harness — and nothing about who
permitted it.

**THIS IS Q7 AS RULED**, by Brett Heap on 2026-08-29, AS RECOMMENDED: attestation
signatures happen by remote signing served by the harness controller, with the
runner's request recorded beside the signature and the controller corroborating
the payload against its own link-4 setup attestation. The mechanism is named in
contract text because that ruling opened the gate; until it was ruled, tranche
two could not name one. An HSM is a LATER HARDENING OF THE SAME SHAPE — it moves
where the key sits and changes nothing the chain carries — so adopting one
requires no change to this requirement.

**THE REQUEST IS RECORDED BECAUSE A BARE SIGNATURE ANSWERS HALF THE QUESTION.**
A signature shows WHAT was attested; the recorded request shows WHO ASKED for
the attestation. An attestation carrying no recorded request is REFUSED rather
than accepted as an attestation with a detail missing. The identity is valid for
ONE TASK and capable of exactly one thing — signing an attestation about that
task.

**RECORDING THE REQUEST IS NECESSARY AND NOT SUFFICIENT, AND THIS REQUIREMENT
SAYS SO RATHER THAN LETTING THE RECORD IMPLY MORE THAN IT SHOWS.** A recorded
request establishes that SOMETHING asked; it does not establish WHAT. An
opportunistic caller that can reach the signing service can submit a payload
that corroborates against link 4 and satisfy every refusal above, and the
signature it receives is then indistinguishable from the provisioned task's. So
the controller SHALL **ATTRIBUTE** every signing request TO THE TASK IT
PROVISIONED IN LINK 4, SHALL REFUSE a request it cannot so attribute, and SHALL
cover the attribution — requester, chain identity, and the digest of the payload
— INSIDE THE BYTES IT SIGNS, because an attribution attachable afterwards is an
attribution anyone can attach.

**THE ATTRIBUTION COMES FROM THE CONTROLLER'S OWN PROVISIONING AND NEVER FROM
WHAT THE RUNNER SAYS ABOUT ITSELF** — a requester identity the runner supplies
is self-report, and self-report is precisely what the corroboration requirement
below refuses. What must be ESTABLISHED is stated here; the mechanism that
establishes it is not, on the same footing `add-trust-anchor` uses for issuance
evidence it cannot mandate a mechanism for.

**AND THE RESIDUAL IS RAISED AS AN EXPLICIT GAP RATHER THAN CLAIMED AS CLOSED.**
The obvious mechanism — a per-task request credential held by the runner — is
UNAVAILABLE HERE: `access_secrets: false` forbids placing one in a worker, which
is the same constraint that forces remote signing in the first place. A
realization SHALL therefore DECLARE, under `add-trust-anchor`'s
conformance-declaration rule, exactly what its platform lets the controller
establish about a requester, and SHALL NOT assert an attribution stronger than
that. Where a platform cannot distinguish two tasks the same controller
provisioned, the realization DECLARES it and the affected attestations are
refused for uses requiring per-task attribution — an undeclared shortfall is
non-conformance, and the identical shortfall declared is conformant.

**SIGNER IDENTITY IS EXPRESSED IN `add-identity-brokering`'s VOCABULARY, AND
WHAT THAT VOCABULARY CONTRIBUTES HERE IS A REFUSAL.** Its ratified text keeps
non-human identity out of the persona population: a workload, agent, job or
service SHALL NOT be represented as a persona, its authority comes from
`credential-contracts` grants and `openxwallet` holders rather than from
anything the broker holds, and such an identity NEVER APPEARS AS THE ACTOR of a
governed act. A per-task attestation identity is a workload by that definition.
The HUMAN actor a chain records remains link 1's stable opaque subject, bound to
the wallet that signed, exactly as tranche one's actor-binding requirement
fixes it. Tier 2 answers *what ran*; tier 1 answers *who permitted*; neither
stands in for the other.

#### Scenario: a runner presents a signature it produced itself

- WHEN an attestation carries a signature not produced at the controller
- THEN it is REFUSED, and the refusal names the custody breach rather than the signature's validity
- AND a valid signature made in the wrong place is not a conforming attestation

#### Scenario: an attestation arrives with no recorded signing request

- WHEN an attestation is presented with a signature and no record of the request that asked for it
- THEN it is REFUSED
- AND the missing request is never treated as an omitted detail on an otherwise complete record

#### Scenario: an opportunistic caller submits a payload that corroborates

- WHEN a caller the controller cannot attribute to a task it provisioned in link 4 submits a payload that matches the setup attestation
- THEN the request is REFUSED and no signature is produced
- AND the payload's corroborating cleanly is never accepted in place of attributing the asker

#### Scenario: the attribution falls outside the signed bytes

- WHEN the requester attribution is present on the record but outside the bytes the controller's signature covers
- THEN it is REFUSED, because an attribution attachable afterwards is an attribution anyone can attach
- AND its mere presence on the record is not accepted

#### Scenario: the runner supplies its own requester identity

- WHEN a signing request carries a requester identity the runner asserts about itself
- THEN it is not accepted as the attribution, which comes from the controller's own provisioning
- AND a self-reported asker is refused on the same ground as a self-reported measurement

#### Scenario: the platform cannot distinguish two tasks the same controller provisioned

- WHEN a realization's platform cannot attribute a request to one provisioned task rather than another
- THEN it DECLARES that shortfall under the conformance-declaration rule and does not assert the attribution
- AND the affected attestations are refused for uses requiring per-task attribution, the declaration leaving the realization conformant

#### Scenario: the attestation identity is offered as the actor of a governed act

- WHEN a governed record names a per-task attestation identity as the actor of the act
- THEN validation FAILS, because a workload is not a persona and never appears as an actor
- AND the act's actor remains link 1's stable opaque subject bound to the wallet that signed

#### Scenario: a persona is proposed for a runner

- WHEN a realization proposes issuing a broker persona to a runner so its attestations can name an actor
- THEN it is REFUSED, and the runner's authority stays a `credential-contracts` / `openxwallet` grant
- AND no persona is created for a workload

#### Scenario: one attestation identity is reused across two tasks

- WHEN an attestation identity signs for a second task
- THEN the second attestation is REFUSED, because the identity is valid for one task
- AND reuse is never accepted on the strength of the identity still being unexpired

#### Scenario: a hardware-backed signer is adopted

- WHEN the controller moves its signing key into an HSM
- THEN every record the chain carries is unchanged and this requirement is satisfied as written
- AND the adoption is recorded as a hardening of the same shape rather than a different mechanism

### Requirement: The controller corroborates what it signs and never notarizes self-report

openxFactory SHALL require the harness controller to CORROBORATE a submitted
attestation payload against its OWN link-4 setup attestation BEFORE signing it,
and SHALL REFUSE TO SIGN a claim about something it provisioned that it cannot
match. **BIND BEFORE SIGN.** The controller is a SIGNER, never a notary of
whatever it is handed.

**A SIGNATURE AT THE CONTROLLER BOUNDARY PROVES ONLY THAT THE CONTROLLER SIGNED
THE BYTES IT WAS GIVEN.** A compromised runner could submit a false
model/version/harness payload and links 5, 6 and 10 would still chain — the
fabricated-but-valid-looking record this family exists to refuse. The model,
version and harness of link 5 are facts the controller PROVISIONED in link 4, so
they are corroborated against its own setup attestation rather than accepted
from the runner. Q7's ruling settles WHERE THE KEY LIVES; it never settles
whether the claims are checked, and this requirement is the half the mechanism
does not discharge.

**MEASUREMENTS ONLY THE RUNNER CAN SEE ARE LABELLED, NEVER LAUNDERED.** Such a
measurement is either INDEPENDENTLY OBSERVED — hardware-attested where the
platform offers it — or carried EXPLICITLY AS RUNNER-CLAIMED. To make the
labelling survive reading as well as writing, EVERY ATTESTED FACT SHALL CARRY
ITS EVIDENCE CLASS — `controller_corroborated`, `hardware_attested`, or
`runner_claimed` — and A FACT CARRYING NO CLASS IS REFUSED, on the same footing
as tranche one's untagged digest: a class that can be omitted is a class that
will be, and an unclassed fact is read at the strength of the strongest fact
beside it.

#### Scenario: a submitted payload disagrees with the setup attestation

- WHEN a runner submits a model, version or harness value that does not match what link 4 records as provisioned
- THEN the controller REFUSES TO SIGN and records the disagreement
- AND a signature is never produced and then flagged, because a signed record with a warning beside it still chains

#### Scenario: a measurement only the runner can see, on a platform offering no hardware attestation

- WHEN a fact cannot be corroborated against link 4 and cannot be independently observed
- THEN it is carried as `runner_claimed`
- AND it is never laundered into controller-attested fact by being signed alongside facts that were corroborated

#### Scenario: an attested fact carries no evidence class

- WHEN an attestation carries a fact with no evidence class
- THEN it is REFUSED
- AND the omission is never resolved in favour of the strongest class present on the record

#### Scenario: a consumer reads a runner-claimed fact as attested

- WHEN a downstream consumer quotes or aggregates a `runner_claimed` fact as though it were corroborated
- THEN the use is REFUSED, because the class travels with the fact
- AND the controller's signature over the record is not evidence for the claims the record itself labels unverified

#### Scenario: the controller is asked to sign a payload it provisioned nothing for

- WHEN a signing request names a subject that appears nowhere in the controller's own setup attestation
- THEN the request is REFUSED
- AND being asked is never accepted as authority to sign

### Requirement: A tier-2 attestation key never enters a worker, in every configuration

openxFactory SHALL KEEP TIER-2 ATTESTATION KEY MATERIAL OUT of every worker,
every runner and every lane — in EVERY configuration and for EVERY lifetime —
and SHALL realize tier 2 as a SIGNING ORACLE AT THE CONTROLLER: the runner
submits a payload and receives a signature over it, and nothing else crosses the
boundary. Key bytes do not cross it; neither does a handle that dereferences to
key bytes, nor a delegation that would let the runner sign again without asking.

**THE GROUND IS CONSTITUTIONAL AND ALREADY SHIPPED.** The neutral omnigent
overlay contract at `contracts/omnigent/omnigent-domain-overlay.schema.yaml`
holds a CLOSED six-boolean permission matrix on every worker class —
`additionalProperties: false`, with `execute_final_action` and `access_secrets`
declared `const: false` — over exactly five archetypes (`frame`, `generate`,
`verify`, `challenge`, `assemble_for_admission`). **`access_secrets: false`
FORBIDS CUSTODY, NOT MERELY LONG-LIVED CUSTODY.** A private key is a secret, and
shortening a credential's lifetime does not make it non-secret. "Ephemeral"
describes the identity's LIFETIME and never a relaxation of custody; a design
that hands a worker a key for one task has already breached the constraint it
claims to honour.

#### Scenario: a runner requests custody of the per-task key

- WHEN a worker, runner or lane requests custody of tier-2 key material
- THEN the request is REFUSED and no key bytes cross into it
- AND the request is recorded as a custody breach attempt rather than as an unmet configuration need

#### Scenario: a one-task lifetime is offered as making a key non-secret

- WHEN a design argues that a key valid for one task is not a secret
- THEN it is REFUSED, because `access_secrets: false` binds custody rather than duration
- AND the key's short life is not accepted as a substitute for the boundary

#### Scenario: a key is issued into the worker and destroyed after the task

- WHEN a design proposes issuing key material into a worker and destroying it when the task ends
- THEN it is REFUSED
- AND its own destruction step is not accepted as a defence, because the breach is the crossing and not the retention

#### Scenario: the runner is handed a reusable signing delegation

- WHEN a runner receives a token, handle or delegation that lets it obtain further signatures without a fresh corroborated request
- THEN it is REFUSED, because a credential that signs again without asking is custody by another name

#### Scenario: an HSM is adopted

- WHEN the controller's key moves into hardware-backed custody
- THEN the design remains conforming, because the key has moved further from the worker and never closer
- AND no record the chain carries changes

### Requirement: Opening a pull request is a signed decision, bound to the chain

openxFactory SHALL treat the OPENING of a pull request — link 6 — as a DECISION
and SHALL require it to be SIGNED AS ONE: under the same per-task tier-2 identity
at the controller, over the carried traveling contract, corroborated and
hash-linked like every link from link 4 onward. The signed decision records which
chain it descends from, which link-5 attestations produced the work it proposes,
and what it proposes.

**ABSENT, THE PULL REQUEST IS AN ORPHAN ACT — AND THIS IS WHERE THE ABSENCE OF
THE ATTESTATION LINKS BECOMES DETECTABLE RATHER THAN MERELY UNRECORDED.** A pull
request EXISTS, so something opened it, so a signed decision is owed. A pull
request reaching the gate with no signed open decision is REFUSED — not as a
missing optional record, but because an unsigned open is an act with no signer,
and a chain that cannot name who opened cannot tell provisioned work from work
that arrived from outside the chain entirely.

**SIGNING AN OPEN IS NOT PERMITTING A MERGE.** Link 6 is the decision to
PROPOSE; the terminal act is permitted by the gate and by nothing else. Nothing
in this requirement weakens the constitutional `execute_final_action: false`, and
a lane offering its own signed open decision as permission has confused proposing
with permitting.

#### Scenario: a pull request reaches the gate with no signed open decision

- WHEN work is presented for the terminal act and no link-6 record exists
- THEN it is REFUSED as an orphan act
- AND the absence is never read as an unremarkable omission, because the pull request's existence proves the act occurred

#### Scenario: the open decision names a chain the traveling contract does not carry

- WHEN a signed open decision names a chain identity other than the one the traveling contract carries
- THEN it is refused as a fraud signal
- AND the mismatch is never resolved in favour of either copy

#### Scenario: the open decision commits to only some of the runner attestations

- WHEN a signed open decision commits to a proper subset of the link-5 attestations for the work it proposes
- THEN it is REFUSED under the completeness rule below
- AND the omitted attestation is treated as a dropped link rather than as work that produced nothing

#### Scenario: a signed open decision is offered as permission to merge

- WHEN a lane offers link 6 as evidence that the terminal act is permitted
- THEN it is REFUSED, because proposing is not permitting
- AND the permission remains the gate's verdict and nothing else

#### Scenario: the open decision is signed by a key the runner holds

- WHEN link 6 is signed anywhere other than at the controller
- THEN it is REFUSED under the tier-2 custody requirement
- AND the decision's correctness is not accepted as a defence of where it was signed

### Requirement: The signed hash-link rule takes effect at link 4, and the gate walks the extended chain

openxFactory SHALL bring the SIGNED HASH-LINKING RULE INTO EFFECT AT LINK 4 —
the first link in this family with a signer of its own — and SHALL require every
signature from link 4 onward to cover, besides its own content, (a) THE CHAIN
IDENTITY minted at inception and (b) THE DIGEST OF ITS PREDECESSOR, each computed
under the ONE digest construction already in force and each NAMING THE SUBJECT it
was taken over.

**THIS REALIZES TRANCHE ONE'S DECLARATION RATHER THAN AMENDING IT.**
`add-signed-execution-chain`'s gate requirement states that the hash-linked
signing rule "takes effect at the first link that has a signer of its own, which
is the harness-controller setup attestation — tranche two". Tranche one could not
perform it: inception cannot sign over an identity derived from its own
signature, and the traveling contract has no signer at all, so continuity there
is established by derivation and comparison. From link 4 the signature exists,
so the rule can be executed rather than asserted.

**NO SECOND DIGEST CONSTRUCTION IS DECLARED HERE.** Tranche one puts exactly one
construction in force for every digest this capability computes, including any a
later tranche adds, and says so in its own scenario. Declaring one beside it
would be the defect that requirement exists to prevent, and this delta declares
none.

**WHERE A LINK ADMITS SEVERAL RECORDS, ITS SUCCESSOR COMMITS TO ALL OF THEM.**
Link 5 is PLURAL — each runner attests — so "the digest of the predecessor" is
not one value, and a rule that leaves it singular lets a lane DROP THE
ATTESTATION IT DISLIKES and still present a continuous chain. A successor SHALL
therefore commit to an ORDERED, DEDUPLICATED ENUMERATION of every predecessor
record under the one construction. **A dropped attestation is a BREAK, never a
shorter chain.**

**AND THE COMPLETE SET IS DERIVED FROM THE LOG, NOT FROM WHAT THE SUBMISSION
HAPPENS TO CONTAIN — WITHOUT WHICH "A PROPER SUBSET" NAMES NOTHING.** An
enumeration can only be judged incomplete against an AUTHORITATIVE SET, and a
gate reading only the artifacts it was handed has none: a lane that omits an
unwanted link-5 record before presenting link 6 leaves behind an enumeration
that is ordered, deduplicated and complete over everything the gate can see. The
authoritative set SHALL therefore be DERIVED BY THE GATE from the append-only
signed transparency log tranche one makes THE RECORD, by a DEFINED QUERY —
**every leaf of the link-5 record kind committing to this chain identity, at or
before the successor's own leaf** — and the gate SHALL REFUSE a successor whose
enumeration is not EQUAL to that set. Not a subset and not a superset: a record
enumerated but never written as a leaf is UNPROVEN under tranche one's own rule
that an act writing no leaf is refused by every consumer requiring the chain.

**THE RESIDUAL HERE IS TRANCHE ONE'S DECLARED ONE AND IS NOT RE-DECLARED AS
NEW.** A store that truncates its newest unobserved leaves could hide a link-5
leaf and make an incomplete enumeration look equal. That is exactly the suffix
truncation tranche one's transparency-log requirement DECLARES it cannot detect
and names tranche-three anchoring as closing. This requirement inherits that gap
rather than papering over it, and claims detection only within a prefix some
party has observed.

**THE GATE'S SCOPE GROWS WITH THE TRANCHE, AND IT STILL VALIDATES A CHAIN RATHER
THAN A BAG OF SIGNATURES.** From this tranche the gate walks LINKS 1–6 and
validates CONTINUITY: one chain identity carried unbroken, each signed link
committing to its predecessor. Individually valid setup, runner and PR-open
artifacts drawn from DIFFERENT EXECUTIONS MUST NOT ASSEMBLE, because with
concurrent or repeated work a signature bag is exactly what a badly-behaved lane
would submit. A broken or missing link is a FRAUD SIGNAL AND A REFUSAL, never a
warning and never a finding downgraded for convenience; and a chain the gate
CANNOT EVALUATE is REFUSED on the family's fail-closed doctrine, because an
unevaluable answer never reads as permission.

**HOW THIS COMPOSES WITH TRANCHE ONE'S SCOPE NOTE — STATED, NOT LEFT TO A
READER.** Tranche one bounds its gate to links 1–3 and says it "SHALL NOT report
the absence of a later tranche's link as a break, because a gate cannot walk a
link that does not exist yet", with a scenario conditioned in terms on "a
tranche-two link does not exist yet". That sentence is SELF-LIMITING and it is
SPENT HERE: on this tranche's realization links 4–6 STOP BEING "a later
tranche's link", and the scenario's condition no longer obtains. No requirement
of tranche one is restated or replaced and none needs to be — but the composition
is written down, because a scope note read as a standing permission is exactly
how an absence becomes a hole.

#### Scenario: a signature from link 4 onward omits the chain identity

- WHEN a link-4, link-5, link-6 or link-10 signature covers its own content and not the chain identity
- THEN it is REFUSED
- AND the signature's validity over its own content is never accepted in place of the binding

#### Scenario: valid artifacts from different executions are submitted together

- WHEN the gate receives setup, runner and PR-open artifacts that individually verify but do not share one chain identity and predecessor sequence
- THEN it REFUSES, naming the broken continuity
- AND per-link validity is never accepted in place of continuity

#### Scenario: a successor commits to three of four runner attestations

- WHEN a link-6 or link-10 record's enumeration is not EQUAL to the set the gate derives from the log for this chain identity
- THEN the gate REFUSES
- AND the omission is reported as a dropped link rather than accepted as a shorter chain

#### Scenario: a lane omits an attestation before presenting its successor

- WHEN a lane withholds a link-5 record so that the successor's enumeration is complete over everything submitted
- THEN the gate REFUSES, because it derives the complete set from the log rather than from the submission
- AND an enumeration complete over what was handed in is never accepted as complete

#### Scenario: an enumerated record was never written as a leaf

- WHEN a successor enumerates a predecessor record for which the log holds no leaf
- THEN it is REFUSED as UNPROVEN
- AND the record's own well-formedness is not accepted, because an act that writes no leaf is refused by every consumer requiring the chain

#### Scenario: a realization declares a second digest construction for the predecessor digest

- WHEN a realization declares an algorithm or serialization for the predecessor digest beside the one already in force
- THEN it is REFUSED, because one construction governs every digest this capability computes including those a later tranche adds
- AND the second rule is removed rather than reconciled

#### Scenario: a predecessor digest names no subject

- WHEN a link carries a correctly constructed, algorithm-tagged predecessor digest that does not name what it was taken over
- THEN it is REFUSED, because readers that agree on how to hash can still disagree on what was hashed

#### Scenario: the gate cannot evaluate the extended chain

- WHEN the controller's anchor is unresolvable, the log is unreachable, or the chain cannot otherwise be evaluated
- THEN the gate REFUSES rather than proceeding
- AND an unevaluable condition is never reported as a pass

#### Scenario: a chain carrying links 1–3 only reaches the gate after this tranche is in force

- WHEN a chain presents the ratification, the inception and the traveling contract and no attestation links at all
- THEN the gate REFUSES to permit the terminal act, because links 4–6 are in scope from this tranche and are no longer "a later tranche's link"
- AND tranche one's scope note is not available as a permission, having been written for the period before this tranche existed

### Requirement: The chain completes at CLOSURE, and the governed post-merge test is what closes it

openxFactory SHALL treat a chain as COMPLETE ONLY AT CLOSURE — link 10, the
GOVERNED POST-MERGE TEST — and SHALL require that test to consume BOTH the
ratified proposal AND the review notes, so that what was promised is what is
tested. Link 10 is signed under the same per-task identity at the controller,
corroborated and hash-linked exactly as links 5 and 6 are.

**IT CONSUMES TWO ARTIFACTS AND NOT ONE.** The proposal is referenced by the
RATIFICATION'S CONTENT DIGEST that tranche one already fixes — the digest taken
over the subject ratified, never the chain identity taken over the signed
ratification. The review notes are the record of the council review link 7
carries on the §7.4 path. A test consuming only the proposal tests what was
promised and not what was reviewed; one consuming only the review notes tests the
amendments and not the commitment. Both, or the record is not this link.

**BINDING TO THE REVIEW RECORD'S BYTES IS NOT ENOUGH, AND CLOSURE SHALL
ESTABLISH THE REVIEW'S AUTHORITY.** A digest over a review record proves only
that the bytes did not change after the controller signed them; it establishes
nothing about whether a council produced them, so a SUPPLIED OR FABRICATED
review record would otherwise be consumed by a passing test and CLOSE THE CHAIN
— the fabricated-but-valid-looking record arriving at the one link that has no
gate behind it. Link 10 SHALL therefore establish that the review record it
consumes was produced under REVIEW AUTHORITY PROVEN BY POSSESSION, expressed in
the ALREADY SHIPPED vocabulary of `add-wallet-carried-review-authority` — a
wallet-carried review grant, exercised, with the exercise's proof of possession
supplied and VERIFIED, its standing current at exercise, and its `object_ref`
bound to that review record — and SHALL REFUSE a review record it cannot so
establish. No second review-authority, proof or grant vocabulary is defined
here; the instrument is the one this repository already reads inside a required
check.

**WHAT THAT ESTABLISHES, AND WHAT IT DOES NOT — DECLARED RATHER THAN IMPLIED.**
It establishes that the review record was produced under PROVEN review
authority. It does NOT establish that every seat signed, because link 7's seat
signatures are outside this tranche's gate scope and this requirement does not
pretend to walk them. That residual SHALL be DECLARED under the
realization-conformance obligation, with a walked link-7 check named as what
closes it — an undeclared shortfall is non-conformance, and the identical
shortfall declared is conformant.

**THE TWO ENFORCEMENT HORIZONS ARE DIFFERENT AND THE DIFFERENCE IS THE POINT.**
Links 1–6 enforce AT THE GATE, before the merge. Links 9 and 10 enforce AT
CLOSURE, after it. **A MERGE THAT ALREADY HAPPENED IS NOT RETROACTIVELY
REFUSED** — that is not a concession but what an honest control says about a
state it cannot reach. What an unclosed chain forfeits is EVERYTHING DOWNSTREAM
OF IT: a MERGED-BUT-UNCLOSED chain — link 10 missing, failed, or unsigned — is a
REFUSING STATE for whatever consumes the merge (promotion, release, the next
chain that builds on it) and FIRES link 9's FRAUD SIGNAL. It is not a pending
state, not an advisory, and not a warning.

**MISSING, FAILED AND UNSIGNED ARE THREE OUTCOMES AND ARE RECORDED AS THREE.** A
failed test is a stronger signal than an absent one and an unsigned pass is
stronger than an absent record, on the same footing as tranche one's rule that a
failed proof of possession is never the weaker reading of a missing one.
Collapsing them loses the distinction a responder needs first.

#### Scenario: the post-merge test consumes the proposal only

- WHEN a post-merge test binds to the ratified proposal and to no review record
- THEN it is not link 10 and the chain does not close on it
- AND its own passing is not evidence that what was reviewed was tested

#### Scenario: a fabricated review record is supplied to the post-merge test

- WHEN a review record is consumed that is well-formed and bound by digest, and no verified review-authority exercise establishes it
- THEN the chain does NOT close and the record is REFUSED
- AND the test's own passing is never accepted as evidence that a council produced what it read

#### Scenario: the review authority was revoked before its exercise

- WHEN the review grant behind a consumed review record records a revoked grant, ancestor or holder at exercise
- THEN closure is REFUSED, because a valid signature is not current authority
- AND the review record's integrity is not accepted in place of standing at exercise

#### Scenario: a reader asks whether closure proves every seat signed

- WHEN a reader takes closure as evidence that each council seat signed the review
- THEN it is corrected: closure establishes PROVEN REVIEW AUTHORITY and not per-seat signatures
- AND the residual is DECLARED, naming a walked link-7 check as what would close it

#### Scenario: the test runs, passes, and is unsigned

- WHEN a governed post-merge test completes successfully with no signature
- THEN the chain does not close, and the outcome is recorded as UNSIGNED rather than as absent
- AND the pass is not evidence that the act it reports was permitted

#### Scenario: a merge landed and link 10 never ran

- WHEN a merge is complete and no post-merge test exists for its chain
- THEN every consumer of that merge REFUSES and the fraud signal fires
- AND the merge itself is not un-made, because the horizon that could have refused it has passed

#### Scenario: a release is attempted over an unclosed chain

- WHEN promotion or release is attempted for work whose chain has not closed
- THEN it is REFUSED
- AND the merge having succeeded is never accepted as evidence that the chain closed

#### Scenario: a reader treats an unclosed chain as pending

- WHEN an unclosed chain is reported as awaiting completion
- THEN it is corrected to a REFUSING state
- AND the distinction is kept, because a pending state invites waiting where a refusing state requires acting

### Requirement: A remediation chain is the one admitted consumer of an unclosed chain

openxFactory SHALL admit EXACTLY ONE consumer of an unclosed chain — a
REMEDIATION CHAIN whose DECLARED, SIGNED SUBJECT IS THAT FAILURE — and SHALL
refuse every other consumer until a chain closes over the merge.

**WITHOUT THE EXEMPTION THE INVARIANT DEADLOCKS.** When link 10 fails on an
ordinary defect, the corrective or revert change is itself a NEXT CHAIN that
builds on the merge; refuse that too and the repository can never repair what it
cannot retroactively unmerge. FAIL-CLOSED MEANS THE FAILURE CAN BE REPAIRED, NOT
THAT IT IS TRAPPED.

**THE EXEMPTION'S CONDITIONS ARE WHAT KEEP IT FROM BEING A HOLE, AND EACH IS
ENFORCED RATHER THAN ASSUMED:**

1. A remediation chain is A FULL CHAIN — ratified and signed like any other, its
   links 1–6 walked at the gate exactly as for any work. It is an exempt
   CONSUMER, never an exempt CHAIN.
2. Its SUBJECT IS DECLARED, names the unclosed chain BY CHAIN IDENTITY, and falls
   INSIDE THE BYTES THE RATIFYING SIGNATURE COVERS. A declaration attachable
   afterwards is a declaration anyone can attach, and the exemption would then be
   claimable by relabelling.
3. PROMOTION AND RELEASE STAY REFUSED until a chain closes over the merge. The
   exemption admits the REPAIR, never the thing the repair is for.
4. THE EXEMPTION IS NOT INHERITABLE. A chain that builds on a remediation chain
   is an ordinary consumer and stays refused while the original is unclosed — an
   exemption that descends is an exemption that launders, which this family has
   already met once as an exemption inheritable by identifier collision.
5. A remediation chain OWES ITS OWN CLOSURE. One that does not close is itself
   unclosed, refuses its own downstream, and is repairable by this same route
   rather than exempt from it.

#### Scenario: link 10 fails on an ordinary defect and a corrective change is raised

- WHEN a corrective or revert change declares the failed closure as its signed subject
- THEN it is ADMITTED as a consumer of the unclosed chain
- AND the repository can repair what it cannot retroactively unmerge

#### Scenario: a chain merely mentions the failure

- WHEN a chain references the unclosed chain in its text without declaring it as the subject covered by the ratifying signature
- THEN the exemption is REFUSED
- AND mentioning is never accepted as declaring

#### Scenario: a release is attempted on the strength of an admitted remediation chain

- WHEN promotion or release is attempted because a remediation chain was admitted
- THEN it is REFUSED
- AND admission of the repair is never read as closure of the chain being repaired

#### Scenario: a third chain builds on the remediation chain

- WHEN a further chain consumes the remediation chain's merge while the original chain is still unclosed
- THEN it is REFUSED as an ordinary consumer
- AND the exemption does not descend to it

#### Scenario: a remediation chain skips the gate because it is a remediation

- WHEN a remediation chain is offered with links 4–6 absent, on the ground that it exists to repair a failure
- THEN it is REFUSED, because it is exempt as a consumer and never as a chain
- AND its purpose is not accepted as a substitute for its own links

#### Scenario: a remediation chain's own closure fails

- WHEN a remediation chain merges and its own link 10 fails
- THEN it is itself unclosed and refuses its own downstream
- AND its remediation status does not exempt it from the invariant it was raised under

### Requirement: The executing layer refuses a step whose inbound chain does not verify

openxFactory SHALL require the OMNIGENT EXECUTION LAYER to REFUSE TO EXECUTE a
step whose INBOUND CHAIN DOES NOT VERIFY, as a PRECONDITION OF EXECUTION rather
than as a record written afterwards. The weak version — the layer records what it
did and something later checks — yields an audit trail a compromised or careless
lane can write falsely. The strong version moves verification from AFTER to
BEFORE, and the record becomes a BY-PRODUCT OF A CONTROL rather than a SUBSTITUTE
FOR ONE.

**THIS COMPOSES WITH THE OMNIGENT PERMISSION MATRIX AND IS NOT A NEW AUTHORITY.**
It adds NO sixth archetype, NO seventh permission boolean, and NO change to
`contracts/omnigent/omnigent-domain-overlay.schema.yaml`, whose `permissions`
block is closed (`additionalProperties: false`) over exactly six booleans with
`execute_final_action` and `access_secrets` fixed `const: false`. **A REFUSAL IS
NOT A PERMISSION**: withholding execution requires no capability a worker does
not already have, and this requirement grants none.

**AND VERIFYING A CHAIN NEEDS NO SECRET**, which is why the precondition sits
comfortably beside `access_secrets: false` rather than in tension with it.
Continuity, digests, certificates and anchor records are public material. A
design that required a worker to hold key material in order to verify would have
re-created the very breach the tier split exists to prevent, and is refused for
that reason rather than on preference.

**FAIL-CLOSED, ON THE FAMILY'S STANDING DOCTRINE.** A layer that CANNOT EVALUATE
the inbound chain REFUSES rather than proceeding, and an unevaluable answer never
reads as permission. The refusal is recorded as A REFUSAL TO EXECUTE and not as a
failed execution — a step that never ran did not fail, and recording it as a
failure attributes a defect to the work instead of to its missing permission.

#### Scenario: a step arrives with an inbound chain that does not verify

- WHEN the executing layer evaluates a step whose inbound chain fails verification
- THEN it REFUSES TO EXECUTE and nothing runs
- AND no record of the step's outcome is produced, because there is no outcome

#### Scenario: the inbound chain cannot be evaluated

- WHEN an anchor is unresolvable or the chain cannot otherwise be evaluated
- THEN the layer REFUSES
- AND an unevaluable answer never reads as permission

#### Scenario: a seventh permission boolean is proposed to express the precondition

- WHEN a realization proposes adding a permission to the omnigent matrix to carry this refusal
- THEN it is REFUSED, because the matrix is closed and a refusal is not a permission
- AND the precondition is expressed without widening what any archetype may do

#### Scenario: a worker is offered key material so that it can verify

- WHEN a design proposes giving a worker key material in order to verify an inbound chain
- THEN it is REFUSED, because verification uses public material only
- AND the proposal is recorded as re-creating the breach the tier split exists to prevent

#### Scenario: an unpermitted step is recorded as a failed execution

- WHEN a refusal to execute is reported as an execution that failed
- THEN it is corrected to a refusal
- AND the distinction is kept, because a step that never ran did not fail

#### Scenario: the chain is checked after the step runs

- WHEN a layer executes first and verifies the inbound chain afterwards
- THEN it is REFUSED as the weak version of this requirement
- AND a record written after the fact is never accepted as a precondition
