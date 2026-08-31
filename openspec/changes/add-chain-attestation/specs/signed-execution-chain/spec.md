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

**AND IT COMMITS TO THE EXPECTED ATTESTATION SET — THE TASKS IT DISPATCHED —
BECAUSE A COMPLETENESS RULE WITH NO INDEPENDENT EXPECTATION CANNOT DETECT AN
ATTESTATION THAT WAS NEVER WRITTEN.** The setup attestation SHALL therefore
record, besides the environment, the EXPECTED ATTESTATION SET: the tasks the
controller DISPATCHED under this chain identity, each named by a stable
per-task reference the corresponding link-5 attestation carries back. **This
falls inside the bytes the controller's signature covers**, on the same ground
every other binding in this capability does — an expectation attachable
afterwards is an expectation anyone can attach, and one a lane could edit is one
a lane will edit down.

**THE COMMITMENT ORIGINATES WHERE THE FACT DOES, WHICH IS WHAT MAKES IT WORTH
ANYTHING.** The controller is the party that PROVISIONS and DISPATCHES; the
runner is the party whose record is at stake. A completeness rule derived only
from what the runners' side later wrote can be satisfied by writing less, so the
expectation has to come from the side that cannot benefit from shrinking it.
**This is BIND BEFORE SIGN's sibling one link earlier:** there the controller
refuses to sign a claim it cannot corroborate; here it states, before any runner
executes, what claims are owed.

**A DYNAMIC FAN-OUT IS SERVED BY EXTENSION AND NEVER BY SILENCE, WHICH IS THE
OBJECTION THIS RULE HAD TO ANSWER TO BE BUILDABLE.** Where the full task set is
not knowable when link 4 is signed — the ordinary case for work that fans out as
it runs — the controller SHALL EXTEND the commitment by a further
CONTROLLER-SIGNED EXTENSION RECORD under the same chain identity, hash-linked
like every link from link 4 onward, **WRITTEN AS A LEAF BEFORE, OR AT, THE
DISPATCH OF THE TASK IT ADDS — NEVER LATER.** The expected set is then link 4 AS
EXTENDED.

**THE DEADLINE IS DISPATCH AND NOT FIRST-ATTESTATION, AND THE DIFFERENCE IS THE
WHOLE CONTROL.** An earlier form of this rule set the deadline at *"before the
attestation it covers is produced"*, which fails twice. It lets the controller
commit **AFTER OBSERVING THE EXECUTION**, so the record stops being an
INDEPENDENT EXPECTATION and becomes a description of what happened. And worse: a
realization that mints extensions when SIGNING REQUESTS ARRIVE never commits a
task whose attestation the runner SUPPRESSES ENTIRELY — no request, no extension,
no expectation — so link 6's enumeration equals the reduced committed set and
**the dropped-attestation attack passes again**, through the very instrument
raised to close it. Dispatch is the moment the controller acts and the only
moment before the runner can influence anything, which is what makes the
expectation independent. It is also what the paragraph below can then truthfully
say: that the commitment named the task BEFORE ANY RUNNER EXECUTED.

Four refusals keep the extension from becoming the hole it exists to close:

1. **AN EXTENSION WRITTEN AFTER THE DISPATCH OF THE TASK IT ADDS IS REFUSED**,
   because an expectation recorded after the controller has acted is a
   description and not an expectation — and one recorded after the task has RUN
   is not even that.
2. **A TASK DISPATCHED UNDER NO COMMITMENT IS A BREACH AT DISPATCH**, not merely
   at attestation: the obligation binds the controller's own act, so a
   realization cannot defer it to a request that may never arrive.
3. **A LINK-5 ATTESTATION FOR A TASK NO COMMITMENT COVERS IS REFUSED**, so
   extension cannot be skipped by simply attesting anyway.
4. **AN EXTENSION SIGNED ANYWHERE OTHER THAN AT THE CONTROLLER IS REFUSED**,
   under the tier-2 custody requirement, so a runner cannot enlarge or shrink
   the expectation it is measured against.

**WHAT THIS DOES NOT REACH IS DECLARED RATHER THAN IMPLIED.** A controller that
is itself the attacker can under-commit — dispatch a task and never name it — and
no comparison against its own commitment will show that. This requirement claims
detection against A LANE, A RUNNER OR A STORE and not against a compromised
controller, whose own signature is the root of every fact link 5 carries in any
case. **THE RESIDUAL IS THEREFORE NOT A GAP THIS RULE OPENS BUT THE TRUST BOUNDARY
THE TIER SPLIT ALREADY DRAWS**, and it is the same boundary requirement 4 exists
to keep the runner outside of.

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

**AND EVERY CERTIFICATE THIS CAPABILITY CONSUMES SHALL BIND TO A KEY, BY ONE RULE
OVER THE WHOLE SET RATHER THAN A CLAUSE PER TIER.** The canonical
`certificate-record` carries an OPTIONAL `subject.public_key_fingerprint` and NO
PUBLIC KEY AT ALL, and `issuance-evidence` carries neither — so *"the signature
verifies under the certified key"* is unrunnable from those records as they
stand, and where the fingerprint is absent even an out-of-band key cannot be
bound. **THE CONSUMED-CERTIFICATE SET OF THIS CAPABILITY IS: THE CONTROLLER
CERTIFICATE OF THIS REQUIREMENT, AND THE TIER-2 CERTIFICATES OF REQUIREMENT 2 AT
BOTH SUBJECT SCOPES.** Two obligations bind across ALL of them, and **neither
moves a canonical byte**:

1. **EVERY CERTIFICATE THIS CAPABILITY CONSUMES SHALL CARRY
   `subject.public_key_fingerprint`.** This is THIS CAPABILITY'S CONSUMPTION
   REQUIREMENT and not a schema change — the field is already in the canonical
   shape and already constrained there; a consumer may REQUIRE what the canonical
   shape leaves OPTIONAL, on the estate's own precedent
   (`add-wallet-carried-review-authority`'s S2, where `issued_by` is optional in
   the canonical wallet shape and the register's reader refuses a record without
   it). A consumed certificate lacking the fingerprint is REFUSED with the
   FORGED-IDENTITY force, because it is a certificate that cannot be tied to any
   key.
2. **EVERY SIGNED RECORD THIS CAPABILITY DEFINES SHALL CARRY THE SIGNER'S PUBLIC
   KEY ALONGSIDE ITS SIGNATURE** — link 4 and the commitment extensions under the
   controller certificate exactly as links 5, 6 and 10 under tier-2 ones. This is
   a discipline on THIS capability's own record surface, which is ours to set;
   the canonical shapes are untouched.

**RESOLVE, COMPARE, THEN VERIFY — IN THAT ORDER, FOR EVERY CERTIFICATE IN THE
SET.** The verification input supplies the purported key from the signed record
itself; verification COMPUTES ITS FINGERPRINT under the ONE digest construction
already in force and REQUIRES EQUALITY with the consumed certificate's
`subject.public_key_fingerprint`; only then is the signature verified under that
key. **A MISMATCH IS THE FORGED-IDENTITY REFUSAL** — it is precisely a key that is
not the certified one — and so is an ABSENT FINGERPRINT, the same condition
reached by omission rather than by substitution.

**THE RULE IS WRITTEN OVER THE SET BECAUSE A PER-TIER CLAUSE WAS THE DEFECT.** An
earlier form required the fingerprint of TIER-2 certificates only. Link 4 and the
commitment extensions are signed under the CONTROLLER certificate, so a canonical
controller certificate omitting its optional fingerprint left both forgeable by
exactly the supplied-key trick the tier-2 clause had closed: the record supplies a
key, the signature verifies under it, and no required equality check binds it to
certified material. **A rule that enumerates the slots it covers will be outrun by
the next slot** — the same lesson the predecessor order learned when extensions
were given a placement of their own — so this one is stated over the SET, and any
certificate a later tranche adds to that set is covered on the day it is added.

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

**AND A DECLARED SHORTFALL IS A BOUNDED ADMISSION AND NEVER A CONVERSION. THIS
PARAGRAPH IS THE FLOOR UNDER EVERY DECLARATION THIS CAPABILITY ADMITS, AND THE
LATER SITES CITE IT RATHER THAN RESTATING IT.** A declaration records honestly
that a control CANNOT BE MET; it never makes the unmeetable control MET, and it
never supplies the evidence that control would have produced. **A DECLARED
SHORTFALL SHALL THEREFORE DISQUALIFY THE CHAIN FROM EVERY USE THAT DEPENDS ON
WHAT THE DECLARED CONTROL WOULD HAVE ESTABLISHED**, and a realization SHALL NOT
offer a declaration as satisfaction of the obligation it declares against. A
declaration that disqualifies nothing is not a declaration but an exemption, and
this capability admits none: where a declaration's disqualified set would be
EMPTY, the shortfall is NON-CONFORMANCE and not a declaration. What conformance
under a declaration establishes is that the REALIZATION is conformant; it is
never that the CHAIN is admissible for a use the declaration removes.

**REVOCATION AFTER SIGNING IS TREATED ON THE FAMILY'S TWO-HORIZON DOCTRINE, AND
THIS IS A DESIGN DECISION RATHER THAN A RULING.** The attestation SHALL CARRY
the controller's revocation standing AS CHECKED AT SIGNING, and a certificate
ALREADY REVOKED AT SIGNING SHALL make the attestation REFUSED OUTRIGHT. A
certificate revoked AFTER a signature was made SHALL NOT retroactively unmake an
act the gate already permitted — it SHALL REFUSE everything the chain has not yet
been permitted for, which is the same horizon rule link 10's closure requirement
states below. The two cases are DISTINCT OUTCOMES and are recorded as two: a
revoked-at-signing certificate produces NO admissible attestation at all, while a
revoked-after-signing certificate leaves the already-permitted act standing and
refuses the remainder.

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

#### Scenario: a setup attestation commits to no expected attestation set

- WHEN a setup attestation records the environment and names no expected attestation set for the chain identity
- THEN it is REFUSED, because the completeness rule the gate applies at link 6 would then have nothing independent to compare an enumeration against
- AND a chain whose expectation is inferred from the attestations that happen to arrive is never accepted, since that is the rule being satisfied by writing less

#### Scenario: the expectation is carried outside the bytes the controller signed

- WHEN the expected attestation set is present on the link-4 record but outside the bytes the controller's signature covers
- THEN it is REFUSED, because an expectation attachable afterwards is an expectation anyone can attach
- AND its presence on the record is not accepted, on the same footing as an attribution outside the signed bytes

#### Scenario: a commitment extension is written after the task it adds was dispatched

- WHEN a controller-signed extension naming a task is written to the log AFTER that task was dispatched — whether before its attestation, after it, or never followed by one
- THEN it is REFUSED, because an expectation recorded after the controller has acted is a description and not an expectation
- AND the extension's correct content and valid signature are not accepted in place of its being written at or before dispatch

#### Scenario: a realization mints extensions when signing requests arrive

- WHEN a realization creates commitment extensions on the arrival of a signing request, and a runner suppresses its attestation entirely so no request is ever made
- THEN the design is REFUSED, because that task was dispatched under no commitment and the expectation the gate compares against would silently shrink to exclude it
- AND link 6's enumeration equalling that reduced set is exactly the dropped-attestation attack this commitment exists to refuse, so a deadline the runner can influence is no deadline

#### Scenario: a runner attestation arrives for a task no commitment covers

- WHEN a link-5 attestation is presented for a task named neither in link 4 nor in any extension written before it
- THEN it is REFUSED, so that extension cannot be skipped by attesting anyway
- AND the attestation's corroborating cleanly against link 4's environment is not accepted in place of the task having been committed

#### Scenario: an extension is signed somewhere other than at the controller

- WHEN a commitment extension carries a signature not produced at the controller
- THEN it is REFUSED under the tier-2 custody requirement
- AND a runner is never permitted to enlarge or shrink the expectation its own completeness is measured against

#### Scenario: the controller certificate was already revoked when the attestation was signed

- WHEN a setup attestation is presented whose controller certificate records a revoked standing AT SIGNING
- THEN the attestation is REFUSED OUTRIGHT and nothing downstream of it is permitted
- AND the signature's cryptographic validity is never accepted in place of standing at signing, because revocation does not invalidate a signature

#### Scenario: the controller certificate is revoked after a signature was already made

- WHEN a controller certificate is revoked after an attestation it signed was already permitted by the gate
- THEN the permitted act is not retroactively unmade, and EVERYTHING THE CHAIN HAS NOT YET BEEN PERMITTED FOR is REFUSED from that point
- AND the two cases are recorded as two outcomes, because a revoked-at-signing certificate produces no admissible attestation while this one leaves an act standing and refuses the remainder

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
than accepted as an attestation with a detail missing.

**TIER 2 HAS TWO SUBJECT SCOPES, AND EACH CARRIES ITS OWN CLOSED ENUMERATION OF
AUTHORIZED RECORD KINDS.** The controller SHALL issue, alongside the per-task
identities, exactly ONE **CHAIN-SCOPED TIER-2 IDENTITY** per chain identity. Both
scopes are tier 2 and both are bound by every custody rule below without
exception — the key lives at the controller's signing boundary, the identity is
EPHEMERAL, and `access_secrets: false` is untouched, because adding a SUBJECT
SCOPE moves no key and widens no permission:

| Scope | Valid for | Authorized record kinds — CLOSED |
| --- | --- | --- |
| **PER-TASK** | ONE task | the **TASK ATTESTATION** — link 5, what ran |
| **CHAIN-SCOPED** | ONE chain identity | the **PR-OPEN DECISION RECORD** — link 6; and the **POST-MERGE TEST RECORD** — link 10 |

**AND EVERY TIER-2 IDENTITY IS ISSUED UNDER CONTROLLER-SIGNED ISSUANCE EVIDENCE,
WITHOUT WHICH THE WORD "ISSUES" ABOVE ESTABLISHES NOTHING A VERIFIER CAN CHECK.**
Saying the controller ISSUES these identities does not let anyone TELL that it
did. A lane can generate its own keypair, label it with the scope a verifier
expects, and then forge BOTH the record and the request attribution under that
same untrusted key — and every attribution rule in this capability is satisfied
by the forgery, because they all check the record against the key rather than the
key against an issuer. **The staged topic already requires the fix and this
delta owes it**: tier 2 is *"issued by the harness controller UNDER ITS OWN
CERTIFICATE"*, and *"the harness controller's certificate (link 4) and the
per-task issuance (link 5) are `trust-anchor` SHAPES — this topic must express
them in that vocabulary, not a parallel one."*

**THE CONTROLLER SHALL THEREFORE ISSUE EVERY TIER-2 IDENTITY — PER-TASK AND
CHAIN-SCOPED ALIKE — UNDER THREE RECORDS THAT COMPOSE**, two of them
`add-trust-anchor`'s own CANONICAL shapes consumed UNMODIFIED, and one this
capability's own:

1. **THE CERTIFICATE RECORD** — `add-trust-anchor`'s canonical
   `certificate-record`, carrying the identity's **PUBLIC-KEY FINGERPRINT**
   (`subject.public_key_fingerprint`) and its **VALIDITY BOUNDS**
   (`validity.not_before` / `not_after`), an ephemeral identity being one whose
   bounds say so. **It carries a FINGERPRINT AND NOT A KEY** — the canonical shape
   holds no public key at all, which is why the verification key is SUPPLIED by
   the signed record and matched against this fingerprint rather than read from
   here. **Canonical and unmodified.**
2. **THE ISSUANCE EVIDENCE** — `add-trust-anchor`'s canonical
   `issuance-evidence`, carrying the CONTROLLER'S ISSUANCE ACT: which authority
   issued, under what establishment level, on whose request, and when.
   **Canonical and unmodified.**
3. **THE SIGNED CHAIN BINDING — A RECORD KIND THIS CAPABILITY DEFINES**,
   controller-signed, carrying exactly what neither canonical shape admits —
   **the identity's SUBJECT SCOPE** (the one task, or the one chain), **its
   CLOSED RECORD-KIND ENUMERATION**, and **THE CHAIN IDENTITY IT SERVES** — and
   REFERENCING (1) and (2) by their `certificate_id` and `issuance_evidence_id`.

**THE COMPOSITION IS FORCED BY THE CANONICAL SHAPES AND IS NOT A PREFERENCE.**
Both trust-anchor schemas are `additionalProperties: false` at every level:
`certificate-record` holds the key and the bounds and no scope, enumeration or
chain identity; `issuance-evidence` describes the ISSUANCE ACT — authority,
request provenance, issuing authority — and admits none of the three either. An
earlier form of this requirement asked for all five bindings in "issuance
evidence expressed in `add-trust-anchor` vocabulary", **which no realization
could build**: it would have had to invent the parallel certificate-like record
this requirement forbids, or drop the bindings and re-open the forged-identity
gap. **Composition is what lets the canonical shapes stay canonical.**

**AND THE CHAIN BINDING IS NOT A CERTIFICATE SHAPE, WHICH IS WHY THE
NO-SECOND-VOCABULARY RULE SURVIVES INTACT.** It asserts no key, no validity, no
issuing authority and no trust; it establishes nothing about WHO A SIGNER IS —
that is entirely (1) and (2)'s work, in `add-trust-anchor`'s vocabulary and no
other. What it carries is what THIS capability means by a tier-2 identity: which
chain it serves, which subject scope it holds, and which record kinds it may
sign. Those are `signed-execution-chain` facts about a `signed-execution-chain`
identity, so the record belongs to **this capability's own code surface** and is
counted there.

**VERIFICATION COMPOSES ALL THREE, AND THE FORGED-IDENTITY REFUSAL FIRES ON ANY
ONE MISSING**: the certificate valid and current; the issuance evidenced; and the
chain binding naming THIS chain and the scope the record's kind requires.

**AND THE VERIFICATION KEY IS RESOLVED BY REQUIREMENT 1'S RULE, WHICH GOVERNS
EVERY CERTIFICATE THIS CAPABILITY CONSUMES AND IS NOT RESTATED HERE.** A tier-2
certificate carries `subject.public_key_fingerprint` because it is IN THAT SET,
not because tier 2 is special; the signed record carries the signer's public key
beside its signature; and verification RESOLVES, COMPARES, THEN VERIFIES — the
supplied key's fingerprint computed under the one digest construction and
required EQUAL to the certificate's, before any signature is checked. **A
mismatch or an absent fingerprint is the FORGED-IDENTITY refusal**, at the same
force for a tier-2 certificate as for the controller's.

**EVERY VERIFICATION OF A TIER-2 SIGNATURE VERIFIES THE COMPOSED ISSUANCE
FIRST.** A signature under an identity missing ANY OF THE THREE records is a
**FORGED IDENTITY** — refused with the FRAUD-SIGNAL force a broken link carries,
never as an unrecognised key or a record with a detail missing. A signature whose
record kind falls outside the enumeration ITS OWN CHAIN BINDING carries is
refused on the same footing, so the closed enumerations above
are enforced against the issuer's statement rather than against a reader's
memory. **The gate's continuity walk includes issuance verification at every link
it walks**, which is what makes links 4–6 a chain of ESTABLISHED signers rather
than of plausible ones.

**THIS IS THE GROUND EVERY ATTRIBUTION RULE IN THIS CAPABILITY STANDS ON**, and
it is stated here rather than assumed: attributing a request to a provisioned
task, or to the party a chain's inception record binds, establishes something
only once the KEY THAT SIGNED is known to be the controller's own issue. Without
issuance evidence those rules bind a forger to its own forgery.

**THE SPLIT IS BY SUBJECT, BECAUSE THAT IS WHAT THE RECORDS ACTUALLY DIFFER IN.**
A link-5 attestation is a record about ONE TASK. **Link 6 is ONE DECISION that
commits to EVERY link-5 attestation for the work it proposes, and link 10 is ONE
TEST OUTCOME over that same whole** — they are records about the CHAIN. A signer
valid for one task and authorized only for records about THAT task therefore
cannot produce either of them the moment a chain fans out to more than one task:
whichever task's identity signed, the record would necessarily cover work from
the others. **AN EARLIER DRAFT MADE EXACTLY THAT MISTAKE**, enumerating links 5,
6 and 10 under the per-task identity — which fixed the records' FORM and left
their SUBJECT unfixed, so the ordinary multi-task fan-out still had no conforming
link 6. The enumeration is split rather than widened, because widening the
per-task identity to cover work it was not minted for would have destroyed the
one property that identity exists to carry.

**EACH ENUMERATION IS CLOSED, AND A RECORD SIGNED UNDER THE WRONG SCOPE IS
REFUSED AS FIRMLY AS ONE SIGNED UNDER NO TIER-2 IDENTITY AT ALL.** A per-task
identity presented for a link-6 or link-10 record is REFUSED; the chain-scoped
identity presented for a link-5 attestation is REFUSED. Neither is a lesser
defect than the other, and a realization that collapses the two scopes into one
identity has re-created the conflict this split exists to resolve.

**AUTHORITY RECORDS STAY OUTSIDE BOTH ENUMERATIONS FOREVER, AND THAT IS THE
POINT OF CLOSING THEM.** A ratification, an approval, a review grant or any
other record that CONFERS PERMISSION is never signable under a tier-2 identity of
EITHER scope — not by widening, not by realization convenience, and not by a
later tranche adding a further kind. **The chain-scoped identity is broader in
SUBJECT and not in AUTHORITY**: it says things about a whole chain and it permits
nothing, exactly as the per-task identity says things about one task and permits
nothing. Tier 2 answers *what ran*; tier 1 answers *who permitted*; the
enumerations are closed precisely so that widening either cannot quietly move an
act from the second question into the first.

**THIS FILLS A GAP IN THE STAGED TOPIC RATHER THAN OVERTURNING A RULING, AND IT
IS FLAGGED SO A REVIEWER CAN DISAGREE.** The topic's link table gives links 6 and
10 a *"per-task identity (controller-signed)"* while its own row 6 calls the
PR-open a single decision — the same shape as its SINGULAR hash-link rule beside
its PLURAL link 5, which this delta already resolves by addition. Tranche one's
ratified text characterizes tier 2 as *"ephemeral per-task attestation
identities"* and in the same sentence says tier 2 *"is the named tranche-two
boundary and is NOT defined here"*, creating no attestation identity of any kind.
**Defining it is this tranche's act**, and the two operative constraints that
ratified sentence does impose — EPHEMERAL, and keys that never enter a worker —
bind the chain-scoped identity exactly as they bind the per-task ones.

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

**AND THE SAME OBLIGATION REACHES THE CHAIN-SCOPED IDENTITY, BECAUSE THE
ATTRIBUTION ABOVE IS TASK-SCOPED AND WOULD OTHERWISE COVER NOTHING IT SIGNS.**
The rule above attributes a request to THE TASK THE CONTROLLER PROVISIONED IN
LINK 4. The chain-scoped identity signs no record about a task, so that rule
reaches none of its requests — and an opportunistic caller able to reach the
controller could submit a link-6 payload naming a valid chain, the complete
link-5 set and plausible proposed work, satisfy every refusal in requirement 5,
and receive a chain-scoped signature the controller never established anyone was
authorized to ask for. **THE SPLIT THAT MADE LINK 6 CONSTRUCTIBLE IS WHAT OPENED
THIS**, and it is closed by extending the mechanism rather than by inventing a
second one:

1. **THE REQUEST IS RECORDED**, beside the signature it received, exactly as a
   task-scoped request is. A chain-scoped record carrying no recorded request is
   REFUSED.
2. **THE CONTROLLER SHALL ATTRIBUTE every chain-scoped signing request TO THE
   PARTY THE CHAIN'S OWN INCEPTION RECORD BINDS** — the ACTOR bound to the wallet
   that signed the ratification, carried with the work by the traveling contract
   — **and SHALL REFUSE a chain-scoped signing request from any party that
   binding does not name.**
3. **THE ATTRIBUTION FALLS INSIDE THE BYTES IT SIGNS** — requester, chain
   identity, and the digest of the payload — because an attribution attachable
   afterwards is an attribution anyone can attach.

**NO AUTHORITY IS MINTED HERE, AND THAT IS THE POINT OF DERIVING IT.** The
authorized-requester set is not a new grant, a new role or a new credential: it
is READ OFF WHAT THE CHAIN ALREADY CARRIES. Tranche one's actor-binding
requirement already fixes that the actor's subject carries a wallet attestation
naming the wallet whose key made the exercise, and that the binding falls inside
the signed bytes; the gate already walks exactly that. **This requirement adds no
vocabulary and no second source of truth — it obliges the controller to ASK the
question the chain already answers**, before it signs on that chain's behalf. A
chain whose inception record binds nobody can obtain no chain-scoped signature,
which is the correct fail-closed outcome rather than a gap.

**THE REQUEST BRANCH AND THE PLATFORM BRANCH ARE DIFFERENT OBLIGATIONS AT
DIFFERENT MOMENTS, AND THE DISTINGUISHER IS STATED HERE RATHER THAN LEFT TO BE
INFERRED.** A **REQUEST** the controller cannot attribute — one request, on a
platform that can attribute requests — is REFUSED AT SIGNING and no signature is
produced; that is the refusal above and it is not dischargeable by any
declaration. A **PLATFORM** that cannot attribute ANY request is a property of
the realization rather than of a request: it is DECLARED under the shortfall rule
below, and what the declaration costs is stated there. **WHERE BOTH HOLD, THE
PLATFORM BRANCH GOVERNS AND IT GOVERNS DOWNWARD, NEVER UPWARD** — a declared
platform shortfall does not convert the sign-time refusal into a conformant pass
for the individual request; it disqualifies every attestation the platform
produces, so there is nothing left for the request branch to permit.

**AND THE RESIDUAL IS RAISED AS AN EXPLICIT GAP RATHER THAN CLAIMED AS CLOSED,
WITH THE FLOOR REQUIREMENT 1 STATES BINDING IT.** The obvious mechanism — a
per-task request credential held by the runner — is UNAVAILABLE HERE:
`access_secrets: false` forbids placing one in a worker, which is the same
constraint that forces remote signing in the first place. A realization SHALL
therefore DECLARE, under `add-trust-anchor`'s conformance-declaration rule,
exactly what its platform lets the controller establish about a requester, and
SHALL NOT assert an attribution stronger than that. Where a platform cannot
distinguish two tasks the same controller provisioned, the realization DECLARES
it and the affected attestations are refused for uses requiring per-task
attribution — an undeclared shortfall is non-conformance, and the identical
shortfall declared is conformant AS A REALIZATION while the chain it produces is
not.

**WHAT THAT DECLARATION DISQUALIFIES IS NAMED, BECAUSE A DISQUALIFIED SET WITH NO
MEMBERS IS AN EXEMPTION.** Per-task attribution is REQUIRED BY THE TERMINAL ACT
ITSELF: **A CHAIN WHOSE REALIZATION HAS DECLARED THAT IT CANNOT ATTRIBUTE A
SIGNING REQUEST TO THE TASK IT PROVISIONED IN LINK 4 SHALL NOT SATISFY THE LINKS
1–6 GATE FOR THE TERMINAL ACT**, and its link-5 records SHALL NOT be presented
for any use that reads them as establishing WHICH provisioned task ran. The
declaration keeps the realization honest and conformant; it never buys the gate's
permission. Without this the mandatory refusal above would be fully dischargeable
by declaration and the disqualified set would have no members, which is exactly
the shape requirement 1's declared-shortfall floor refuses.

**SIGNER IDENTITY IS EXPRESSED IN `add-identity-brokering`'s VOCABULARY, AND
WHAT THAT VOCABULARY CONTRIBUTES HERE IS A REFUSAL.** Its ratified text keeps
non-human identity out of the persona population: a workload, agent, job or
service SHALL NOT be represented as a persona, its authority comes from
`credential-contracts` grants and `openxwallet` holders rather than from
anything the broker holds, and such an identity NEVER APPEARS AS THE ACTOR of a
governed act. A tier-2 attestation identity is a workload by that definition — a
per-task one and the chain-scoped one alike, since widening a SUBJECT does not
make a workload a persona.
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
- AND the affected attestations are refused for uses requiring per-task attribution, the declaration leaving the REALIZATION conformant and the CHAIN disqualified

#### Scenario: a chain from a platform that declared it cannot attribute reaches the gate

- WHEN a chain whose realization has declared it cannot attribute a signing request to the task provisioned in link 4 is presented for the terminal act
- THEN the links 1–6 gate REFUSES, because the terminal act is itself a use requiring per-task attribution
- AND the declaration is never accepted as the gate's permission, because a declaration that disqualifies nothing is an exemption and this capability admits none

#### Scenario: an unattributable request arrives on a platform that has declared it cannot attribute at all

- WHEN both branches hold — this request cannot be attributed AND the realization has declared its platform can attribute none
- THEN the PLATFORM branch governs: the request is still REFUSED at signing, and the realization's declaration does not convert that refusal into a conformant pass
- AND the declaration governs DOWNWARD by disqualifying every attestation the platform produces, never UPWARD by permitting the individual request

#### Scenario: the attestation identity is offered as the actor of a governed act

- WHEN a governed record names a tier-2 attestation identity of either scope as the actor of the act
- THEN validation FAILS, because a workload is not a persona and never appears as an actor
- AND the act's actor remains link 1's stable opaque subject bound to the wallet that signed

#### Scenario: a persona is proposed for a runner

- WHEN a realization proposes issuing a broker persona to a runner so its attestations can name an actor
- THEN it is REFUSED, and the runner's authority stays a `credential-contracts` / `openxwallet` grant
- AND no persona is created for a workload

#### Scenario: a controller-signed record supplies its own key against a fingerprintless certificate

- WHEN a lane supplies an arbitrary public key and a matching signature for a link-4 setup attestation or a commitment extension, and the controller certificate those records name omits `subject.public_key_fingerprint`
- THEN it is REFUSED with the FORGED-IDENTITY force, because a consumed certificate carrying no fingerprint is one no supplied key can be bound to
- AND the signature's verifying under the supplied key is not accepted, since that is the trick the rule exists to refuse and it does not become sound at the controller tier

#### Scenario: records under a compliant controller certificate verify

- WHEN a link-4 attestation and its commitment extensions each carry the signer's public key beside the signature, the controller certificate carries `subject.public_key_fingerprint`, and each supplied key's computed fingerprint EQUALS it
- THEN the keys RESOLVE, the signatures verify under them, and the records are admitted for the checks their links require
- AND the same rule ran here as at tier 2, because it is written over the consumed-certificate set and not per tier

#### Scenario: a tier-2 certificate record carries no public key fingerprint

- WHEN a tier-2 identity's certificate record omits `subject.public_key_fingerprint`, the canonical schema leaving it optional
- THEN it is REFUSED with the forged-identity force, because a certificate that cannot be tied to any key certifies nothing this capability can verify a signature against
- AND the field's being optional in the canonical shape is not accepted as making it optional HERE, a consumer being free to require what the canonical shape leaves open

#### Scenario: the signing key's fingerprint does not match the certificate's

- WHEN the public key a signed record carries alongside its signature has a fingerprint, computed under the one digest construction in force, that does not EQUAL the certificate record's `subject.public_key_fingerprint`
- THEN it is REFUSED as a FORGED IDENTITY, because a key that is not the certified key is exactly what that refusal names
- AND the signature's verifying under the supplied key is never accepted, since it is the binding to the certificate that was in question and not the arithmetic

#### Scenario: the verification key resolves against the certificate

- WHEN a signed record carries the signer's public key beside its signature, that key's computed fingerprint EQUALS the certificate record's `subject.public_key_fingerprint`, and the signature verifies under it
- THEN the key is RESOLVED and the signature is admitted for the composition's remaining checks
- AND resolution happens before verification, because verifying under an unbound key establishes only that someone signed

#### Scenario: a lane mints its own keypair and labels it with the expected scope

- WHEN a lane generates a keypair, labels it with the scope a verifier expects, and signs a link-5, link-6 or link-10 record and its request attribution under that same key
- THEN verification REFUSES AT ISSUANCE, because that key has no canonical certificate record, no canonical issuance evidence, and no controller-signed chain binding naming a scope, an enumeration and this chain
- AND the refusal carries the FRAUD-SIGNAL force of a broken link, never the weaker reading of an unrecognised key
- AND the record's internally consistent attribution is not accepted, because an attribution verified against the forger's own key establishes nothing

#### Scenario: a genuine tier-2 identity's records verify end to end

- WHEN a record is signed under an identity whose CERTIFICATE RECORD carries its PUBLIC-KEY FINGERPRINT with the signing moment inside its validity bounds, the record SUPPLYING the public key beside its signature and that key's computed fingerprint EQUALLING the certificate's, whose ISSUANCE EVIDENCE records the controller's issuance act and references that certificate, and whose SIGNED CHAIN BINDING names THIS chain, the identity's subject scope and a closed record-kind enumeration the record's kind falls inside — the binding referencing both by identifier
- THEN all three verify, the supplied key RESOLVES against the certificate's fingerprint, the signature verifies under that resolved key, and the record is admitted for the checks its link requires
- AND an identity whose bounds had EXPIRED at signing, whose binding names a different chain, or which is MISSING ANY OF THE THREE RECORDS, is REFUSED, because bounds that are merely PRESENT are not bounds that are MET and a composition is not composed until every part is there
- AND the attribution rules that follow now establish something, because the key that signed is known to be the controller's own issue

#### Scenario: a tier-2 signature covers a record kind outside its own issuance evidence

- WHEN an identity signs a record whose kind is not in the closed enumeration the identity's SIGNED CHAIN BINDING carries
- THEN it is REFUSED, because the enumeration is enforced against the controller's signed statement rather than against a reader's memory
- AND the identity's being genuinely controller-issued is not accepted, since issuance bounds what an identity may sign and not merely that it exists

#### Scenario: an opportunistic caller asks for a chain-scoped signature

- WHEN a caller the chain's inception record does not bind submits a link-6 payload naming a valid chain identity, the complete link-5 set and plausible proposed work
- THEN the controller REFUSES the request and no chain-scoped signature is produced
- AND the payload's satisfying every other refusal is never accepted in place of attributing the asker, because the task-scoped attribution reaches no record about a chain

#### Scenario: the bound requester asks for a chain-scoped signature

- WHEN the party the chain's inception record binds — the actor bound to the wallet that signed the ratification, carried by the traveling contract — requests the link-6 signature from an identity whose CERTIFICATE, ISSUANCE EVIDENCE and SIGNED CHAIN BINDING all verify
- THEN the request is ATTRIBUTED to that party, RECORDED beside the signature it receives, and the attribution falls inside the bytes the controller signs
- AND no authority is minted for it, the authorized requester being read off what the chain already carries rather than granted here

#### Scenario: a chain-scoped record arrives with no recorded signing request

- WHEN a link-6 or link-10 record is presented with a chain-scoped signature and no record of the request that asked for it
- THEN it is REFUSED, on the same footing as a task attestation carrying no recorded request
- AND the missing request is never treated as an omitted detail on an otherwise complete record

#### Scenario: a chain fans out to several tasks and one link-6 decision is signed

- WHEN a chain dispatches several tasks and the chain-scoped tier-2 identity — whose CERTIFICATE, ISSUANCE EVIDENCE and SIGNED CHAIN BINDING verify for this chain and this record kind — signs the single link-6 PR-open decision record committing to every one of their link-5 attestations, at the controller, ON A REQUEST THE CONTROLLER ATTRIBUTED TO THE PARTY THE CHAIN'S INCEPTION RECORD BINDS, RECORDED BESIDE THE SIGNATURE, WITH THAT ATTRIBUTION INSIDE THE CONTROLLER-SIGNED BYTES
- THEN it is CONFORMING, because the decision is a record about the CHAIN, the chain-scoped identity's closed enumeration names that record kind, and the asker was established rather than merely reachable
- AND no per-task identity is asked to sign for work it was not minted for, which is the case the ordinary multi-task fan-out makes unavoidable

#### Scenario: a per-task identity is offered for the PR-open decision

- WHEN a link-6 or link-10 record is signed under an identity valid for one task
- THEN it is REFUSED, because that identity's closed enumeration names the task attestation and nothing else
- AND a single-task chain is not accepted as making the scope immaterial, since a rule that holds only where the fan-out happens to be one is not the rule

#### Scenario: the chain-scoped identity is offered for a runner attestation

- WHEN a link-5 attestation is signed under the chain-scoped tier-2 identity rather than under the identity minted for that task
- THEN it is REFUSED, because a record about ONE TASK is outside the chain-scoped identity's closed enumeration
- AND the refusal has the same force as one for a record signed under no tier-2 identity at all, so the two scopes cannot be collapsed into one

#### Scenario: a tier-2 identity of either scope is offered for an authority record

- WHEN a per-task or chain-scoped tier-2 identity is used to sign a ratification, an approval, a review grant, or any other record that confers permission
- THEN it is REFUSED, because both enumerations are CLOSED and an authority record is never in either
- AND the chain-scoped identity's wider SUBJECT is not accepted as wider AUTHORITY, because tier 2 answers what ran and never who permitted

#### Scenario: one per-task attestation identity is reused across two tasks

- WHEN a PER-TASK attestation identity signs a link-5 attestation for a second task
- THEN the second attestation is REFUSED, because a per-task identity is valid for one task
- AND reuse is never accepted on the strength of the identity still being unexpired
- AND this refusal does not reach the CHAIN-SCOPED identity, whose one chain spans every task the chain dispatched and whose records are about that whole

#### Scenario: a hardware-backed signer is adopted

- WHEN the controller moves its signing key into an HSM that remains outside every host, process and credential scope a worker, runner or lane executes within
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
measurement is either INDEPENDENTLY OBSERVED — by a party that is neither the
runner making the claim nor the controller signing it, which is what a platform
attestation service supplies where one exists — or carried EXPLICITLY AS
RUNNER-CLAIMED. To make the labelling survive reading as well as writing, EVERY
ATTESTED FACT SHALL CARRY ITS EVIDENCE CLASS — `controller_corroborated`,
`independently_observed`, or `runner_claimed` — and A FACT CARRYING NO CLASS IS
REFUSED, on the same footing as tranche one's untagged digest: a class that can
be omitted is a class that will be, and an unclassed fact is read at the strength
of the strongest fact beside it.

**THE CLASS IS ORDERED, AND THE ORDER IS DECLARED HERE RATHER THAN LEFT TO THE
WORDS' CONNOTATIONS**, because the paragraph above reads facts at "the strength
of the strongest fact beside it" and a strength rule over an undeclared order is
not a rule. **`runner_claimed` < `controller_corroborated` <
`independently_observed`**, on ONE discriminator: HOW MANY PARTIES INDEPENDENT OF
THE CLAIMANT ESTABLISHED THE FACT — none, the provisioning controller, or a party
independent of both. A comparison between classes SHALL use this order and no
other, and a realization SHALL NOT introduce a second ordering.

**AND THIS SET COMPOSES WITH THE RATIFIED CUSTODY LADDER RATHER THAN BECOMING A
SECOND ONE.** `add-trust-anchor`'s ratified, CLOSED registry
`contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml` — realized at
`contract-v1.37` — already ranks what a CERTIFICATE'S CUSTODY evidences
(`channel_authentication` / `host_attributed_act` / `holder_attributed_act`).
**THAT IS A DIFFERENT AXIS AND THE DIFFERENCE IS STATED IN TERMS:** the registry
classes WHOSE ACT a signature evidences; this set classes WHERE A FACT INSIDE
THE SIGNED PAYLOAD CAME FROM. The two are read TOGETHER AND IN THAT ORDER — the
custody ceiling of the signing certificate BOUNDS what any fact under it can be
read as evidencing, and no evidence class raises a fact above the custody
ceiling of the certificate that signed it. Neither set may be substituted for
the other, and this capability declares no member of the registry's axis.

**THE THIRD CLASS IS NAMED FOR THE PROPERTY IT ASSERTS AND NOT FOR THE HARDWARE
THAT OFTEN SUPPLIES IT**, because that registry excludes
`asserted_hardware_backing` by name and gives the reason: *"the family's own live
canary runs certificates whose keys are hardware-resident and usable by the host
without limit, and those evidence the HOST … where the key physically lives is a
fact about blast radius that belongs in `notes`, never a tier."* A class called
`hardware_attested` would have re-opened on this axis exactly the hole that
ruling closed on the other. **The property that earns the class is INDEPENDENT
OBSERVATION**; hardware attestation is one mechanism that supplies it, and a
hardware mechanism that observes nothing independent of the claimant earns
nothing.

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

**"IN EVERY CONFIGURATION" REACHES REACHABILITY AND NOT ONLY HAND-OVER, AND THIS
CONDITION IS STATED BECAUSE AN ENUMERATION OF CROSSINGS DOES NOT IMPLY IT.**
Every refusal above is framed on something CROSSING the boundary, and a key that
never crosses can still be READ: a controller process co-resident with the runner
on a self-hosted host, holding a host-readable key, hands nothing across and
would otherwise be conformant as drafted. So, WITH THE SAME FORCE AS THE CROSSING
REFUSALS: **THE TIER-2 SIGNING KEY SHALL NOT BE READABLE FROM ANY HOST, PROCESS
OR CREDENTIAL SCOPE THAT A WORKER, RUNNER OR LANE EXECUTES WITHIN**, and **A
DESIGN THAT PLACES THE CONTROLLER INSIDE THE RUNNER'S TRUST BOUNDARY — the same
host, the same process, the same credential scope, or any boundary the runner can
read across — IS REFUSED.** The signing oracle is an oracle only where the thing
asking cannot reach behind it; a boundary the requester can read across is a
boundary in name.

#### Scenario: the signing key is readable from the scope the runner executes within

- WHEN the tier-2 signing key is readable from a host, process or credential scope that a worker, runner or lane executes within
- THEN the design is REFUSED with the same force as a key crossing the boundary
- AND the key's never having been handed over is not accepted as a defence, because reachability and hand-over are the same breach reached two ways

#### Scenario: the controller is co-located inside the runner's trust boundary

- WHEN a design places the harness controller on the same host, in the same process, or inside the same credential scope as the runner it signs for
- THEN it is REFUSED, because a boundary the requester can read across is a boundary in name
- AND the design's handing nothing across the boundary is never accepted as evidence that the boundary exists

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

- WHEN the controller's key moves into hardware-backed custody that is not readable from, and not co-located inside, any scope a worker, runner or lane executes within
- THEN the design remains conforming, because the key has moved further from the worker and never closer
- AND hardware custody REACHABLE from the runner's scope is NOT this scenario and does not conform, because where a key lives is not the discriminator
- AND no record the chain carries changes

### Requirement: Opening a pull request is a signed decision, bound to the chain

openxFactory SHALL treat the OPENING of a pull request — link 6 — as a DECISION
and SHALL require it to be SIGNED AS ONE: **under the CHAIN-SCOPED tier-2
identity** at the controller, **as the PR-OPEN DECISION RECORD, which that
identity's closed enumeration authorizes**, over the carried traveling contract,
corroborated and hash-linked like every link from link 4 onward. The signed
decision records which chain it descends from, which link-5 attestations produced
the work it proposes, and what it proposes.

**ONE PULL REQUEST IS ONE DECISION, AND ITS SIGNER IS SCOPED TO WHAT IT DECIDES
OVER.** Link 6 commits to EVERY link-5 attestation for the work it proposes, so
its subject is the CHAIN and not any one task. Two earlier drafts of this
capability got this wrong in sequence, and both are recorded rather than
smoothed: the first let the per-task identity sign only *"an attestation about
that task"*, so **no conforming link 6 was constructible at all**; the second
enumerated this record kind under the per-task identity, which fixed the record's
FORM and left its SUBJECT unfixed — so **the ordinary multi-task fan-out still
had none**, since whichever task's identity signed would be covering work from
the others. **The decision is NOT composed from N per-task decisions**: the
authoritative link table gives link 6 one signed decision, and a rule assembling
one link from several signatures would be inventing a link the family does not
have.

**AND THE SIGNING REQUEST FOR THIS RECORD IS ITSELF ATTRIBUTED, NOT MERELY
CORROBORATED.** A controller that checked only the payload would sign for
whoever reached it: the link-5 attribution is TASK-SCOPED and reaches no record
about a chain, so this record's request is attributed to **the party the chain's
own inception record binds**, refused from any other, and recorded beside the
signature — the same mechanism one link over, extended rather than duplicated.
Corroborating what a record SAYS is not establishing who was entitled to ASK for
it, and this link's whole subject is a decision somebody made.

**Signing it still confers nothing**, and the scope split does not change that.
The chain-scoped identity is broader in SUBJECT and not in AUTHORITY: its
enumeration excludes every authority record exactly as the per-task one does, so
nothing here may be read as widening what tier 2 may permit.

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

**"ITS PREDECESSOR" IS DEFINED OVER RECORDS THAT EXIST, BECAUSE THE LINK TABLE'S
NUMBERING IS NOT A CHAIN OF RECORDS.** Read against the authoritative ten-link
table alone, link 10's predecessor is LINK 9 — which is a REFUSING STATE and not
a record: the table gives it no signer at all, and this capability defines no
record kind for it. A realization could not know whether to hash a nonexistent
link-9 artifact, skip to link 6, or use the review record, and the three choices
produce mutually unverifiable chains. **THE PREDECESSOR OF A SIGNED LINK IS
THEREFORE THE NEAREST PRIOR LINK POSSESSING A RECORD KIND IN FORCE AT THE
TRANCHE THAT ACTS**, and its digest is taken over that record. **At this tranche
the signed order is 4 → 5 → 6 → 10**, link 5 being plural and governed by the
enumeration rule below, **so LINK 10'S PREDECESSOR IS LINK 6'S PR-OPEN DECISION
RECORD.**

**THE RULE GOVERNS EVERY SIGNED RECORD KIND THIS CAPABILITY DEFINES, FULL STOP —
NOT THE NUMBERED LINKS, AND NOT A LIST OF KINDS.** Any record this capability
defines that is SIGNED and written under the chain identity is an in-force record,
and "nearest prior" reaches it: **its predecessor is THE ACTUAL NEAREST PRIOR
IN-FORCE SIGNED RECORD OF THIS CHAIN**, whatever kind that record happens to be —
the setup attestation, a commitment extension, **a SIGNED CHAIN BINDING minted
when a late-dispatched task's identity is issued**, or a link-5 attestation
already written. **A record's KIND never determines its place; its POSITION IN
THE LOG does.**

**THIS IS STATED OVER THE SET BECAUSE ENUMERATING KINDS HAS NOW BEEN OUTRUN
TWICE.** A rule naming only numbered links left every dynamic fan-out
unverifiable, so extensions were folded in — and folding in a NAMED KIND rather
than stating the rule over the SET left the SIGNED CHAIN BINDING outside the walk
the moment the ninth round created it, since a late dispatch mints one after the
hash-link rule is in force. **The packet had already recorded this lesson at
`tasks.md` 1.22 — "ONE RULE, NOT SLOTS: a rule that enumerates the slots it
covers will be outrun by the next slot" — and THIS SECTION DID NOT FOLLOW IT.**
It is stated over the set now, so a signed record kind a later tranche adds takes
its place by the rule on the day it is defined, with no amendment here.

**WHERE FAN-OUT COMPLETES BEFORE ANY RUNNER ATTESTS AND EVERY IDENTITY IS ISSUED
UP FRONT, THAT ORDER READS 4 → x₁ → … → xₙ → 5 → 6 → 10. THAT ENUMERATION IS
PURELY ILLUSTRATIVE OF THE NO-INTERLEAVING CASE — IT IS NOT THE RULE, IT BINDS
NOTHING, AND IT OMITS EVERY KIND THAT HAPPENS NOT TO OCCUR IN THAT CASE (a chain
binding minted up front sits in it too).** Fan-out is discovered as work runs, so a chain may lawfully dispatch a
further task AFTER an earlier task has already emitted its link-5 attestation.
The extension that commits that later task is then owed at THAT dispatch, and the
nearest prior in-force record at that moment is the link-5 record already
written — so the extension descends from it, and the later task's own attestation
descends from the extension. **The gate walks the interleaved order as it stands,
because the order is a property of the records that exist rather than of their
kinds.** An extension forced to descend only from link 4 or another extension
could satisfy neither its own placement rule nor the general one, and the
ordinary dynamic fan-out would have been unbuildable.

**WHAT THE DISPATCH DEADLINE ACTUALLY CONSTRAINS, RESTATED PRECISELY BECAUSE THE
LOOSE READING IS WHAT COLLIDED.** An extension SHALL precede — and therefore be
written before — **THE DISPATCH OF THE TASKS IT COMMITS**. It is NOT required to
precede every link-5 attestation of the chain, and never was: an expectation must
be independent of the runners it measures, which is a fact about **the tasks that
extension names** and says nothing about tasks committed earlier and already
attested. The deadline binds per-task, and so does the order.

**THE RULE IS WRITTEN TO BE EXTENDED, NOT REPLACED.** It names no fixed number,
so a later tranche that puts a record kind in force at links 7, 8 or 9 changes
what "nearest prior" resolves to WITHOUT contradicting this text or invalidating
chains built under it — the successor states the new order for chains from ITS
realization, exactly as this tranche does. A rule naming "link 6" literally would
have had to be amended by every such tranche.

**AND THE OMITTED LINKS ARE NAMED RATHER THAN LEFT AS A HOLE, since the whole
defect was a reader having to guess:** **LINK 7** — the council review — carries
seat signatures that tranche one placed on the §7.4 path and left outside the
gate's scope, and it is OUTSIDE THIS CAPABILITY'S CODE SURFACE; its record is
reached by link 10's separate REVIEW-AUTHORITY binding rather than by the
hash-link, which is why closure consumes it without hashing it as a predecessor.
**LINK 8** is the GATE ITSELF, a verifier and not a record, so it can have no
digest. **LINK 9** is the FRAUD SIGNAL — a refusing STATE the chain enters, not
an act that writes an artifact. None of the three is a signed record at this
tranche, and that is why the order steps over them.

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

**AND THE AUTHORITATIVE SET IS LINK 4'S COMMITTED EXPECTATION, NOT THE LEAVES
THAT HAPPEN TO BE PRESENT — WITHOUT WHICH "A PROPER SUBSET" NAMES NOTHING.** An
enumeration can only be judged incomplete against an AUTHORITATIVE SET, and a
gate reading only the artifacts it was handed has none: a lane that omits an
unwanted link-5 record before presenting link 6 leaves behind an enumeration
that is ordered, deduplicated and complete over everything the gate can see.
**THE AUTHORITATIVE SET SHALL THEREFORE BE THE EXPECTED ATTESTATION SET LINK 4
COMMITTED TO, AS EXTENDED BEFORE EACH ATTESTATION IT COVERS**, and the gate SHALL
REFUSE a successor whose enumeration is not EQUAL to it. Not a subset and not a
superset.

**A SET DERIVED FROM THE LOG ALONE CANNOT DETECT THE ATTACK IT WAS WRITTEN FOR,
AND THAT IS WHY THE AUTHORITY MOVED.** An earlier form of this rule derived the
complete set by querying *"every leaf of the link-5 record kind committing to
this chain identity, at or before the successor's own leaf"*. **A leaf that is
NEVER WRITTEN is not in that query's answer**, so a lane that simply never writes
an unwanted attestation — or defers it until after the gate has passed — produces
an enumeration EQUAL to the derived set, and the terminal act is PERMITTED. The
ordering obligation below cannot repair it either: refusing the late leaf when it
finally appears comes after a merge that this capability's own two-horizon
doctrine says is not retroactively refused. **A completeness rule whose
expectation is inferred from the side that benefits from shrinking it is
satisfiable by writing less**, which is the same defect one link over that
"a proper subset" had with nothing to be a subset OF.

**THE LOG COMPARISON SURVIVES AS A SECOND CHECK AND NOT AS THE AUTHORITY.**
Against the committed expectation the gate SHALL ALSO require that **every
committed task has a link-5 leaf** in the append-only signed transparency log
tranche one makes THE RECORD, and that **every link-5 leaf for this chain
identity is covered by the commitment** — the first catching an owed attestation
that was never produced, the second catching one produced outside the
expectation. A record enumerated but never written as a leaf remains UNPROVEN
under tranche one's own rule that an act writing no leaf is refused by every
consumer requiring the chain.

**AND THE WRITING ORDER REMAINS AN OBLIGATION, NOW AS DEFENCE IN DEPTH RATHER
THAN AS THE LOAD-BEARING RULE.** **EVERY LINK-5 LEAF FOR A CHAIN IDENTITY SHALL
BE WRITTEN BEFORE THAT CHAIN'S LINK-6 LEAF**, and **A LINK-5 LEAF SEQUENCED AFTER
ITS SUCCESSOR'S LEAF IS REFUSED** — refused as a DROPPED LINK, and never accepted
as a late-arriving record on an otherwise complete chain. A rule that is
satisfiable by waiting is not a rule. What this obligation no longer has to carry
alone is COMPLETENESS: the committed expectation detects the deferred leaf and
the never-written one at the GATE horizon, where the ordering rule by itself
detected only the deferred one and only once it arrived.

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
committing to its predecessor AS THIS REQUIREMENT DEFINES ONE — the nearest prior
link possessing a record kind in force, which inside the gate's scope is 4 → 5 →
6. Individually valid setup, runner and PR-open
artifacts drawn from DIFFERENT EXECUTIONS MUST NOT ASSEMBLE, because with
concurrent or repeated work a signature bag is exactly what a badly-behaved lane
would submit. A broken or missing link is a FRAUD SIGNAL AND A REFUSAL, never a
warning and never a finding downgraded for convenience; and a chain the gate
CANNOT EVALUATE is REFUSED on the family's fail-closed doctrine, because an
unevaluable answer never reads as permission.

**HOW THIS COMPOSES WITH TRANCHE ONE'S SCOPE NOTE — AMENDED IN THE `## MODIFIED
Requirements` BLOCK BELOW, NOT LEFT TO A READING.** Tranche one bounds its gate
to links 1–3 and says it "SHALL NOT report the absence of a later tranche's link
as a break, because a gate cannot walk a link that does not exist yet", with a
scenario conditioned in terms on "a tranche-two link does not exist yet". **PROSE
CANNOT REPEAL A SCENARIO LIVING IN ANOTHER REQUIREMENT**, and an earlier draft of
this delta tried: it argued the sentence was self-limiting and spent, and left
the scenario standing, so promoted canon would have carried this requirement's
refusal and that scenario's permission on ONE antecedent, both normative, with
every validator reporting clean. **The scope note is therefore AMENDED WHERE IT
LIVES**, in the scenario-complete MODIFIED restatement at the end of this delta,
which re-scopes the gate to the links the ratified tranches have put in force and
re-conditions the scenario on a link NO tranche has yet put in force. The
composition is still written down here, because a scope note read as a standing
permission is exactly how an absence becomes a hole.

#### Scenario: a signature from link 4 onward omits the chain identity

- WHEN a link-4, link-5, link-6 or link-10 signature covers its own content and not the chain identity
- THEN it is REFUSED
- AND the signature's validity over its own content is never accepted in place of the binding

#### Scenario: valid artifacts from different executions are submitted together

- WHEN the gate receives setup, runner and PR-open artifacts that individually verify but do not share one chain identity and predecessor sequence
- THEN it REFUSES, naming the broken continuity
- AND per-link validity is never accepted in place of continuity

#### Scenario: a successor commits to three of four runner attestations

- WHEN a link-6 or link-10 record's enumeration is not EQUAL to the expected attestation set link 4 committed to for this chain identity, as extended
- THEN the gate REFUSES
- AND the omission is reported as a dropped link rather than accepted as a shorter chain

#### Scenario: a lane omits an attestation before presenting its successor

- WHEN a lane withholds a link-5 record so that the successor's enumeration is complete over everything submitted
- THEN the gate REFUSES, because it compares the enumeration against link 4's committed expectation rather than against the submission
- AND an enumeration complete over what was handed in is never accepted as complete

#### Scenario: a lane never writes a dispatched runner's leaf at all

- WHEN a task named in link 4's committed expectation produces no link-5 attestation and no leaf, and link 6's enumeration omits it so that it EQUALS the set a log query would return
- THEN the gate REFUSES, because the enumeration is compared against the COMMITTED EXPECTATION and an owed attestation that was never written is missing from it
- AND the leaf's never having existed is not accepted as the task's never having been dispatched, because the controller committed to it before any runner executed

#### Scenario: an attestation is produced for a task outside the committed expectation

- WHEN a link-5 leaf exists for this chain identity whose task is covered by no commitment, and the successor enumerates it
- THEN the gate REFUSES, because the enumeration must EQUAL the committed expectation and this is a superset of it
- AND the attestation's own validity is not accepted, because work the controller never committed to dispatching is work the chain cannot account for

#### Scenario: a lane defers an unwanted link-5 leaf until after link 6

- WHEN a link-5 leaf for a chain identity is written to the log AFTER that chain's link-6 leaf, so that a query bounded at the successor's leaf would have excluded it
- THEN it is REFUSED as a DROPPED LINK, because every link-5 leaf for a chain identity is owed before its successor's leaf
- AND the deferral is caught at the GATE in any case by the committed expectation, which named the task before any runner executed and does not shrink when a leaf is withheld

#### Scenario: an enumerated record was never written as a leaf

- WHEN a successor enumerates a predecessor record for which the log holds no leaf
- THEN it is REFUSED as UNPROVEN
- AND the record's own well-formedness is not accepted, because an act that writes no leaf is refused by every consumer requiring the chain

#### Scenario: a realization declares a second digest construction for the predecessor digest

- WHEN a realization declares an algorithm or serialization for the predecessor digest beside the one already in force
- THEN it is REFUSED, because one construction governs every digest this capability computes including those a later tranche adds
- AND the second rule is removed rather than reconciled

#### Scenario: a late-dispatched task's identity is issued after an earlier attestation

- WHEN fan-out dispatches a task after an earlier task's link-5 attestation is written, and issuing that task's tier-2 identity mints a SIGNED CHAIN BINDING at that moment
- THEN the chain binding descends from THE ACTUAL NEAREST PRIOR IN-FORCE SIGNED RECORD — that earlier link-5 record, or the commitment extension if that was written later — and the records written after it descend from the binding in turn
- AND the gate walks it, because a signed record this capability defines takes its place by the rule and never by its kind
- AND no realization-specific choice arises, since the predecessor is the log's own latest signed record and not a preference

#### Scenario: a later task is dispatched after an earlier task has attested

- WHEN fan-out discovers a further task after an earlier task's link-5 attestation is already written, and the extension committing the later task is written at that dispatch
- THEN the extension descends from THAT LINK-5 RECORD, being the actual nearest prior in-force signed record, and the later task's own attestation descends from the extension
- AND the gate walks the interleaved order as it stands, because the order is a property of the records that exist rather than of their kinds
- AND the dispatch deadline is satisfied, because it binds an extension to precede the dispatch of THE TASKS IT COMMITS and never every attestation of the chain

#### Scenario: fan-out completes before any runner attests

- WHEN a COMPLETE chain is walked whose every extension was written at dispatch while fan-out ran ahead of the runners, so that each extension's actual nearest prior in-force record is the setup attestation or the prior extension
- THEN the gate walks 4 → x₁ → … → xₙ → 5 → 6 → 10 and CONTINUITY holds over that order — this being the NO-INTERLEAVING case of the general rule and not a placement rule of its own
- AND this says nothing about a chain PRESENTED with links missing, which the completeness and scope rules refuse; what holds here is the hash-link ORDER of a chain whose links are all present
- AND continuity establishes ORDER and never COMPLETENESS, the committed expectation being what decides whether every dispatched task is accounted for
- AND a record chaining from anything other than its actual nearest prior in-force record is REFUSED as a break, in this order and in any interleaved one

#### Scenario: link 10's signature hashes a link-9 artifact

- WHEN a realization computes link 10's predecessor digest over a link-9 artifact, link 9 being the fraud signal for which this capability defines no record kind
- THEN it is REFUSED, because the predecessor of a signed link is the nearest prior link possessing a RECORD KIND IN FORCE, and link 9 is a refusing STATE rather than a record
- AND at this tranche that predecessor is LINK 6's PR-OPEN DECISION RECORD, the signed order being 4 → 5 → 6 → 10

#### Scenario: two realizations pick different predecessors for link 10

- WHEN one realization hashes link 6's record as link 10's predecessor and another skips to the review record or to a link-9 placeholder
- THEN the second is REFUSED, because the order is fixed by this requirement rather than chosen per realization
- AND chains that disagree about what a signature covers cannot be verified against one another, which is the outcome the rule exists to prevent

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
tested. Link 10 is signed **under the same CHAIN-SCOPED tier-2 identity that
signed link 6**, at the controller, **as the POST-MERGE TEST RECORD — the second
and last of the record kinds that identity's closed enumeration authorizes** —
corroborated and hash-linked exactly as links 5 and 6 are. A test outcome is no
more an attestation than a decision is, and its SUBJECT is the same whole: the
governed post-merge test runs over the work the chain produced, not over one
task's share of it, so a task-scoped signer could no more produce a conforming
link 10 than a conforming link 6.

**IT CONSUMES TWO ARTIFACTS AND NOT ONE.** The proposal is referenced by the
RATIFICATION'S CONTENT DIGEST that tranche one already fixes — the digest taken
over the subject ratified, never the chain identity taken over the signed
ratification. The review notes are the record of the council review link 7
carries on the §7.4 path. A test consuming only the proposal tests what was
promised and not what was reviewed; one consuming only the review notes tests the
amendments and not the commitment. Both, or the record is not this link.

**AND THE OUTCOME ITSELF SHALL BE ESTABLISHED AND NEVER NOTARIZED — THIS IS BIND
BEFORE SIGN'S LAST UNCOVERED LIMB.** Every other link moved its CLAIMS to the
controller and this one had left its RESULT with the lane: the corroboration rule
binds a submitted attestation's fields against link 4, and nothing in it
establishes that the post-merge test RAN, or that it PASSED, or that it ran
against the merged work. **A lane supplying a fabricated passing outcome on an
otherwise valid chain would therefore obtain a controller signature over it, with
correct proposal and review bindings, and CLOSE THE CHAIN — unblocking promotion
and release.** That is the fabricated-but-valid-looking record this family exists
to refuse, arriving at the one link with no gate behind it. Link 10 SHALL
therefore BIND, INSIDE THE CONTROLLER-SIGNED BYTES, all three of:

1. **AN AUTHENTICATED TEST EXECUTION** — one the controller ITSELF DISPATCHED OR
   OBSERVED, on exactly the footing its link-4 corroboration already stands on.
   The controller signs what it can ESTABLISH and never notarizes an outcome it
   was handed.
2. **THE EXACT TESTED REVISION**, which SHALL EQUAL the merge commit the chain
   closed over. **A REVISION MISMATCH IS A REFUSAL**, because a test that passed
   against other bytes is evidence about other bytes.
3. **THE RESULT** — the outcome that execution produced, covered by the same
   signature, so a result attachable afterwards is not a result anyone can
   attach.

**AND ESTABLISHING THE RESULT IS NOT THE SAME AS THE RESULT BEING A PASS. A CHAIN
CLOSES ONLY ON AN ESTABLISHED *PASSING* RESULT.** The three bindings above make
the outcome TRUSTWORTHY; they do not make it FAVOURABLE, and a rule that stopped
at "established" would close a chain on a genuine, honestly-reported, correctly
signed TEST FAILURE — permitting promotion and release over work whose own
governed test says it is broken. **AN ESTABLISHED FAILING RESULT SHALL REFUSE
CLOSURE**, and the chain is then in the LINK-10-FAILED refusing state this
requirement already defines below: merged-but-unclosed, refusing everything
downstream, firing link 9's fraud signal, with a REMEDIATION CHAIN as its one
admitted consumer. **A failure honestly established is the control WORKING**, and
it is recorded as FAILED — never as UNESTABLISHED, which is a different fact, and
never as a pass.

**AN OUTCOME THAT IS MERELY RUNNER-CLAIMED OR LANE-CLAIMED IS REFUSED AS CLOSURE
GROUNDS**, fail-closed, on this capability's standing doctrine: the chain stays
MERGED-BUT-UNCLOSED and every consumer of that merge refuses, exactly as the two
enforcement horizons below already provide. Nothing here reaches back through the
merge; what it refuses is the CLOSURE, which was always the thing this link
controls.

**AND NO DECLARED-SHORTFALL PATH EXISTS FOR THE OUTCOME, WHICH THIS REQUIREMENT
STATES RATHER THAN LEAVING TO BE INFERRED.** Requirement 1's declared-shortfall
floor governs: a declaration records honestly that a control CANNOT BE MET and
**never converts an unmeetable control into a met one**, and a declaration whose
disqualified set is empty is not a declaration but an exemption. A realization
that cannot establish its test's execution, revision or result therefore cannot
DECLARE its way to a closed chain — **the declaration would disqualify the chain
from closure, which is the only thing closure does**, leaving nothing for the
declaration to permit. This is precisely the class the floor exists for, and it
is named here so that the two shortfalls this requirement DOES declare — the
per-seat residual below, and the revocation-at-exercise one after it — are not
read as a pattern extending to the outcome.

**AND THE REVIEW RECORD SHALL NAME THE PROPOSAL IT REVIEWED, OR A GENUINE REVIEW
OF OTHER WORK CLOSES THIS CHAIN.** Link 10 references the ratified proposal and
the review record INDEPENDENTLY, and the review-authority exercise below binds
only to the review record — so a caller supplying a REAL, authority-proven review
record **produced for a different proposal** would satisfy every other condition
here and close this chain. Nothing in a valid old review says which work it
reviewed.

**THE BINDING CANNOT BE TO THE CHAIN IDENTITY, AND AN EARLIER FORM OF THIS
PARAGRAPH ASKED FOR EXACTLY THAT.** The §7.4 flow this capability requires puts
the COUNCIL REVIEW BEFORE THE RATIFICATION, and tranche one mints the CHAIN
IDENTITY as *"the digest of the signed ratification"* IN the ratification act
itself. The review record therefore exists BEFORE the value exists, cannot be
amended afterwards without falsifying the record it is, and **no genuine review
could ever have satisfied the positive closure path.** A binding that requires an
artifact to name a value minted after it was written is not a strict binding but
an unsatisfiable one.

**SO THE BINDING IS TO WHAT EXISTS AT REVIEW TIME, AND THE CHAIN IS REACHED
THROUGH THE RATIFICATION'S OWN BYTES.** The consumed review record SHALL NAME
**THE CONTENT DIGEST OF THE PROPOSAL IT REVIEWED** — a value available when the
review is written, taken under the ONE digest construction already in force — and
**CLOSURE SHALL VERIFY THE EQUALITY CHAIN**:

1. the review record's named proposal digest **EQUALS** the RATIFICATION'S
   CONTENT DIGEST, which tranche one fixes as the digest taken over THE SUBJECT
   RATIFIED — the same proposal, digested the same way; and
2. that ratification's SIGNED BYTES, which cover that subject, recompute under
   the same construction to **THE CHAIN IDENTITY** the traveling contract
   carries — which is tranche one's own chain-identity check, already walked.

**The chain is therefore bound to the review TRANSITIVELY, through the
ratification that sits between them**, and nothing is asked to name the future.
**REPLAY IS STILL REFUSED**: a review of another proposal names another proposal
digest, which cannot equal this ratification's content digest, so the first limb
fails and closure is refused. The two digests are the two tranche one already
distinguishes — the CONTENT digest over the ratified subject and the CHAIN
IDENTITY over the signed ratification — and this rule uses each for the comparison
it was defined for rather than collapsing them, which is the error the gate's own
checks 2 and 3 exist to prevent.

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

**AND THE SECOND RESIDUAL IS THE ONE THIS REQUIREMENT'S OWN INSTRUMENT DECLARES
AGAINST ITSELF: REVOCATION-AT-EXERCISE IS NOT SERVED BY A FILE.** *"Standing
current at exercise"* above is demanded of the shipped intake register
`governance/review-authority/register.yaml`, whose ratified header
(`:19-25`) says in terms that **a file-based register CANNOT satisfy
revocation-at-exercise** — *"every distribution path is digest-pinned and
lagging, so this file is an issuance-time snapshot … it must not be pretended
into a revocation surface"* — and whose `revocation_staleness_bound` declares the
window a revocation may go unhonoured. **THIS CAPABILITY THEREFORE DECLARES THE
SHORTFALL RATHER THAN DEMANDING WHAT THE INSTRUMENT SAYS IT CANNOT GIVE**: what a
realization reading that register establishes is standing current AS OF A
PROJECTION NO OLDER THAN THE DECLARED BOUND, and not standing at the instant of
exercise. **WHAT THE SHORTFALL DISQUALIFIES, per this capability's
declared-shortfall floor:** closure SHALL BE REFUSED where the projection the
standing was read from is older than the register's own declared bound, and a
closed chain SHALL NOT be presented as evidence that no revocation occurred
inside that window. **WHAT WOULD CLOSE IT** is the conforming home the register
itself names — a LIVE LOOKUP ON THE HERMES RUNTIME, the S5 successor — at which
point this declaration is withdrawn rather than inherited. Demanding
revocation-at-exercise from the file while declaring nothing would have made this
requirement non-conformant to its own undeclared-shortfall doctrine, at the one
link with no gate behind it.

**THE TWO ENFORCEMENT HORIZONS ARE DIFFERENT AND THE DIFFERENCE IS THE POINT.**
Links 1–6 enforce AT THE GATE, before the merge. Links 9 and 10 enforce AT
CLOSURE, after it. **A MERGE THAT ALREADY HAPPENED IS NOT RETROACTIVELY
REFUSED** — that is not a concession but what an honest control says about a
state it cannot reach. What an unclosed chain forfeits is EVERYTHING DOWNSTREAM
OF IT: a MERGED-BUT-UNCLOSED chain — link 10 missing, failed, or unsigned — is a
REFUSING STATE for whatever consumes the merge (promotion, release, the next
chain that builds on it) and FIRES link 9's FRAUD SIGNAL. It is not a pending
state, not an advisory, and not a warning.

**MISSING, FAILED, UNSIGNED AND UNESTABLISHED ARE FOUR OUTCOMES AND ARE RECORDED
AS FOUR.** A failed test is a stronger signal than an absent one and an unsigned
pass is stronger than an absent record, on the same footing as tranche one's rule
that a failed proof of possession is never the weaker reading of a missing one.
Collapsing them loses the distinction a responder needs first. **THE FOURTH IS
ADDED HERE DELIBERATELY AND IS NAMED AS AN ADDITION**: an UNESTABLISHED outcome —
one whose execution, tested revision or result the controller could not establish
— is a DIFFERENT FACT from a test that ran and FAILED, and a responder who
conflates them will go looking for a defect in the work when what is missing is
evidence about the test. All four are REFUSING states for whatever consumes the
merge; they differ in what they tell the responder to do next, which is the whole
reason this paragraph enumerates rather than summarizes.

#### Scenario: the post-merge test consumes the proposal only

- WHEN a post-merge test binds to the ratified proposal and to no review record
- THEN it is not link 10 and the chain does not close on it
- AND its own passing is not evidence that what was reviewed was tested

#### Scenario: a lane supplies a fabricated passing outcome

- WHEN a lane hands the controller a passing post-merge test outcome the controller neither dispatched nor observed, on a chain whose proposal and review bindings are correct
- THEN the chain does NOT close and the outcome is REFUSED as closure grounds, recorded as UNESTABLISHED rather than as a pass
- AND the controller's willingness to sign the bytes is never accepted in place of establishing that the test ran, because a signer is not a notary of an outcome it was handed

#### Scenario: the tested revision is not the merge commit the chain closed over

- WHEN a link-10 record binds an authenticated execution and a result whose tested revision does not EQUAL the merge commit the chain closed over
- THEN closure is REFUSED
- AND the execution's being genuine and its result passing are not accepted, because a test that passed against other bytes is evidence about other bytes

#### Scenario: the controller dispatches the post-merge test and binds a PASSING result

- WHEN the controller dispatches the governed post-merge test on a request it ATTRIBUTED to the party the chain's inception record binds, RECORDED beside the signature, with that attribution INSIDE THE CONTROLLER-SIGNED BYTES and the signing identity's CERTIFICATE, ISSUANCE EVIDENCE and SIGNED CHAIN BINDING all verifying; the consumed review record NAMES THIS CHAIN'S IDENTITY; the tested revision EQUALS the merge commit the chain closed over; the result is a PASS; and the execution, the revision and the result all fall inside the bytes the controller signs
- THEN the outcome is established AS A PASS and the chain CLOSES on it, the proposal and review-record bindings being satisfied and the review authority's standing established within the register's declared bound
- AND nothing about the result is taken from the lane, which is what makes this record closure grounds rather than a report

#### Scenario: the established post-merge result is a FAILURE

- WHEN the controller dispatches the governed post-merge test against the merge commit the chain closed over, and the established, correctly signed result is a FAILURE
- THEN closure is REFUSED, and the chain is in the LINK-10-FAILED refusing state — merged-but-unclosed, refusing everything downstream, firing link 9's fraud signal
- AND the outcome is recorded as FAILED rather than as UNESTABLISHED or as a pass, because a failure honestly established is this control WORKING
- AND a REMEDIATION CHAIN declaring that failed closure as its signed subject is the one admitted consumer, which is the route out

#### Scenario: a realization declares it cannot establish the test outcome

- WHEN a realization declares, under the conformance-declaration rule, that its platform cannot establish the post-merge test's execution, revision or result
- THEN the declaration does NOT admit closure, because a declared shortfall never converts an unmeetable control into a met one and closure is the only thing this link confers
- AND the chain stays MERGED-BUT-UNCLOSED, its downstream refusing, because a declaration that disqualified nothing here would be an exemption and this capability admits none

#### Scenario: a genuine review record from another proposal is replayed

- WHEN a caller supplies a REAL, authority-proven review record produced for a DIFFERENT proposal, and every other closure condition is satisfied
- THEN closure is REFUSED, because the proposal digest that review names does not EQUAL this ratification's content digest, so the first limb of the equality chain fails
- AND the record's genuine authority and verified proof of possession are not accepted, since they establish that a council reviewed something and never that it reviewed THIS work

#### Scenario: a review written before ratification closes its own chain

- WHEN a council review record written BEFORE ratification names the content digest of the proposal it reviewed, that digest EQUALS the ratification's content digest taken over the subject ratified, and the signed ratification recomputes to the chain identity the traveling contract carries
- THEN the equality chain holds, the review is established as a review OF THIS WORK, and closure proceeds on it
- AND the review record is never asked to name the chain identity, which is minted in the ratification act that comes after it — the chain is reached THROUGH the ratification's own bytes

#### Scenario: a fabricated review record is supplied to the post-merge test

- WHEN a review record is consumed that is well-formed and bound by digest, and no verified review-authority exercise establishes it
- THEN the chain does NOT close and the record is REFUSED
- AND the test's own passing is never accepted as evidence that a council produced what it read

#### Scenario: the review authority was revoked before its exercise

- WHEN the review grant behind a consumed review record records a revoked grant, ancestor or holder at exercise
- THEN closure is REFUSED, because a valid signature is not current authority
- AND the review record's integrity is not accepted in place of standing at exercise

#### Scenario: the review authority's standing is read from a projection older than the declared bound

- WHEN closure resolves the review grant's standing against a projection of the intake register older than that register's own declared revocation staleness bound
- THEN closure is REFUSED and is never proceeded with on the stale copy
- AND the shortfall's being declared does not admit the closure, because a declaration bounds what may be claimed and never supplies the evidence the control asked for

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

- WHEN a corrective or revert change that is ITSELF A FULL CHAIN, its own links 1–6 walked at the gate, declares the failed closure BY CHAIN IDENTITY as a subject falling inside the bytes its ratifying signature covers
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

## MODIFIED Requirements

### Requirement: A gate validates the short chain as a hash-linked chain

openxFactory SHALL operate a gate that validates EVERY LINK THE RATIFIED
TRANCHES OF THIS CAPABILITY HAVE PUT IN FORCE — **links 1–3 at tranche one, and
LINKS 1–6 from tranche two** — before permitting the terminal act, and SHALL
validate them as A CHAIN rather than as a bag of signatures — CONTINUITY, never
merely the presence of the required signatures. Continuity means one chain
identity carried unbroken from the ratification that minted it through every link
the gate walks; how each link binds to it depends on whether that link has a
signer, which the two paragraphs below settle for tranche one and for tranche two
respectively.

**INCEPTION ITSELF DOES NOT SIGN OVER THE CHAIN IDENTITY, AND CANNOT.** The
chain identity is the digest of the signed ratification, and inception is that
same signed act, so requiring inception to sign over the identity would make the
signature input depend on the completed signature — an implementation could not
construct the link at all. Inception is the act that MINTS the identity and the
first record that CARRIES it; it is bound to the ratification by BEING it, not
by signing over it.

**AND THE TRAVELING CONTRACT CANNOT SIGN EITHER, BECAUSE IT HAS NO SIGNER.** The
authoritative link table gives link 3 no signature of its own — it is CARRIED —
so requiring it to sign over inception's digest would invent a signing act and a
signer that nothing in this capability defines, and the ratification's own
signature cannot cover an inception record created from it. **ACROSS LINKS 1–3
continuity is therefore established BY DERIVATION AND COMPARISON, not by a third
signature** — the eight checks below are that half of the walk, and from link 4
onward the signatures exist, so the hash-link rule is performed instead. The gate
SHALL validate exactly that, over the digest subjects this capability's digest
requirement fixes:

1. the ratification's signature VERIFIES;
2. the digest of the SIGNED RATIFICATION, RECOMPUTED by the gate under the one
   construction in force, EQUALS the carried chain identity — this is the
   chain-identity check, and it is taken over the signed bytes, never over the
   ratified subject;
3. the exercise that proved link 1 carries an `object_ref` equal to the
   ratification's CONTENT digest, taken over the subject ratified — a DIFFERENT
   comparison over a DIFFERENT subject, which is the replay check and not the
   identity check;
4. the inception leaf commits to that same chain identity;
5. the traveling contract's carried chain identity and carried leaf digest EQUAL
   the values established above;
6. the ACTOR the chain records is bound to the wallet that signed, per this
   capability's actor-binding requirement — the actor's subject carries a wallet
   attestation, that attestation names the wallet whose key made the exercise,
   and the binding falls inside the signed bytes;
7. the exercise's PROOF OF POSSESSION was supplied AND verified, and its outcome
   is the authenticated one — never a `verification_failure` and never an
   `unauthenticated_request`; and finally
8. the STANDING of the authority was current AT EXERCISE — the exercise's
   revocation check returns not-revoked for the grant, for every ancestor of it,
   and for the holder — and the HOLDER CLASS is one this capability admits for a
   RATIFYING act, which per the human-held requirement means a named human and
   never an agent, runner, lane or workflow identity.

**THE LIST IS CLOSED, AND CLOSING IT IS ITSELF AN OBLIGATION.** Because the gate
validates EXACTLY these checks over links 1–3 — **together with the links 4–6
legs the extended-walk requirement fixes, which are part of the same one walk and
not a second gate** — before the terminal act, **every requirement of
this capability is either walked here or has its enforcement point named
below** — a requirement absent from both is a requirement this capability does
not enforce, however firmly its own text is written. **THE CLAUSE IS SCOPED TO
THE CAPABILITY AND NOT TO A TRANCHE, SO THE TABLE GROWS WITH THE CAPABILITY**:
it covers ALL EIGHTEEN requirements this capability now holds — tranche one's
nine above the rule, tranche two's nine below it — because a table that stopped
at nine would have this capability asserting, in its own words, that tranche
two's requirements are ones it does not enforce. The mapping is stated rather
than left to a reader to reconstruct:

| Requirement | Where it is enforced |
| --- | --- |
| Presentation proven by possession, bound to this ratification, standing current at exercise | Checks 1, 3, 7, 8 |
| The actor is bound to the wallet that signed | Check 6 |
| Ratification and inception are one signed act | Check 4; the atomicity itself is an INCEPTION-TIME refusal, not a gate check, because a gate sees only chains that were incepted |
| Per-ratification uniqueness of the per-act value | INCEPTION-TIME refusal — the gate cannot see the set of all chains from one presented chain, and this is named so the omission is deliberate rather than overlooked |
| One digest construction, subjects named | Checks 2 and 3 recompute under it; a digest naming no subject fails them |
| The traveling contract | Check 5 |
| The transparency log is the record | Check 4 reads the leaf; the log's append-only property is a STORE obligation, not a per-chain check |
| Ratifying authority is human-held | Check 8's holder-class half |
| A named reader runs as a required check | This gate IS that reader; until it is REQUIRED, every check above confers nothing |
| The harness controller attests the environment it prepared | THE EXTENDED WALK's link-4 leg, under this capability's requirement *The signed hash-link rule takes effect at link 4, and the gate walks the extended chain*. The certificate's anchor, recorded-issuance, declared-custody and revocation obligations are `add-trust-anchor`'s and are checked AT USE; the revoked-at-signing refusal is a SIGNING-TIME refusal the gate reads from the attestation's carried standing |
| A runner attestation is produced at the controller, on a recorded request | The extended walk's link-5 leg, for what a presented chain shows: the signature's place of production, the recorded request's presence, and the attribution's falling inside the signed bytes. The refusal of an unattributable REQUEST is a CONTROLLER-TIME refusal at signing, which a gate reading a completed chain cannot observe and which is named here so the split is deliberate; the PLATFORM branch's declared shortfall is enforced at the gate, which REFUSES the terminal act for a chain from a realization that declared it |
| The controller corroborates what it signs and never notarizes self-report | CONTROLLER-TIME refusal BEFORE signing — the gate cannot re-run a corroboration whose inputs it does not hold — plus the gate's own per-fact EVIDENCE-CLASS check on the presented attestations, which refuses an unclassed fact and a class read above its order |
| A tier-2 attestation key never enters a worker, in every configuration | NOT a per-chain check and named as such: a DESIGN and REALIZATION-CONFORMANCE obligation, refused at review and at realization, because a gate sees signatures and never where a key lived or what could read it |
| Opening a pull request is a signed decision, bound to the chain | The extended walk's link-6 leg, including the orphan-act refusal for a pull request reaching the gate with no signed open decision |
| The signed hash-link rule takes effect at link 4, and the gate walks the extended chain | THIS GATE, extended: it IS the enforcement point the link-4, link-5 and link-6 rows name, and it carries the plural-predecessor enumeration, the EQUALITY COMPARISON AGAINST LINK 4'S COMMITTED EXPECTED ATTESTATION SET — which is THE AUTHORITY, the bidirectional transparency-log comparison being a SECONDARY check and never the source of the set — and the leaf-ordering refusal |
| The chain completes at CLOSURE, and the governed post-merge test is what closes it | THE SECOND HORIZON — enforced AFTER the merge, by every consumer of it, and never at this gate. Named here rather than omitted, because the omission is the point: this gate cannot refuse a merge that already happened |
| A remediation chain is the one admitted consumer of an unclosed chain | CONSUMER-TIME, at that same closure horizon. Its own links 1–6 are walked HERE like any chain's — it is an exempt CONSUMER and never an exempt CHAIN |
| The executing layer refuses a step whose inbound chain does not verify | EXECUTION-TIME, in the omnigent layer, BEFORE this gate is ever reached. Until a running layer refuses, the requirement is UNMET rather than partially met, on this capability's named-reader rule |

**WHY CHECKS 6, 7 AND 8 ARE NOT COVERED BY THE STRUCTURAL ONES.** Checks 1–5
establish that ONE CHAIN IS INTERNALLY CONSISTENT. None of them establishes
WHOSE it is, whether the holder actually demonstrated possession, whether the
authority still stood, or whether the holder was ever eligible to ratify. Three
chains pass every structural check and must still be refused: one whose actor
names a different holder than the signer; one whose signature is cryptographically
valid over an exercise recording a REVOKED grant, since revocation does not
invalidate a signature; and one signed by an AGENT-HELD wallet that correctly
attests itself, where the attribution is honest and the holder class is refused.
A gate that enumerates exhaustively and omits any of them authorizes work under
misattributed, revoked, or machine-held authority at the terminal act.

**Checks 2 and 3 SHALL NOT be collapsed into one comparison.** Equating the
content digest with the chain identity would reject every conforming chain,
because the signed bytes are a strict superset of the ratified subject — they
also carry the exercise reference and the per-act value. It is also unbuildable
in the other direction, since an exercise's `object_ref` would then have to
commit to a signature not yet made. That is a complete continuity check over
links 1–3 using only artifacts that exist, and it defeats assembly just as a
signature chain would, because artifacts from different executions carry
different chain identities. **It is complete over links 1–3 and over nothing
further**: links 4–6 carry signatures of their own and are walked by the
extended-walk requirement, which is why the scope sentence below states the
gate's reach and this paragraph does not.

**THE HASH-LINKED SIGNING RULE TAKES EFFECT AT THE FIRST LINK THAT HAS A SIGNER
OF ITS OWN**, which is the harness-controller setup attestation — tranche two.
It is stated here so the rule is declared where it applies rather than asserted
where it cannot be performed. The staged topic's "every link from enrollment
onward" is corrected on both counts, on the same footing its own review round
corrected "link 8 walks all ten": a rule that names a link it cannot apply to is
a rule that has not been executed in the head.

Individually valid artifacts drawn from DIFFERENT executions MUST
NOT assemble into a chain, because with concurrent or repeated work a signature
bag is exactly what a badly-behaved lane would submit. A BROKEN OR MISSING LINK
IS A FRAUD SIGNAL AND A REFUSAL, never a warning and never a finding downgraded
for convenience: a missing link means either the act did not happen or something
is misrepresenting that it did, and both are refusals. A chain the gate cannot
EVALUATE is refused on the family's fail-closed doctrine — an unevaluable answer
never reads as permission.

**THE GATE'S SCOPE IS EXACTLY THE LINKS THE RATIFIED TRANCHES OF THIS CAPABILITY
HAVE PUT IN FORCE, AND IT GROWS WITH THEM.** That is links 1–3 at tranche one and
LINKS 1–6 FROM TRANCHE TWO, whose requirements stand in this same capability. The
gate SHALL NOT report the absence of a link **NO RATIFIED TRANCHE HAS YET PUT IN
FORCE** as a break, because a gate cannot walk a link that does not exist yet —
**and that sentence is available for such a link and for no other.** It is a
SCOPE NOTE AND NEVER A STANDING PERMISSION: once a tranche puts a link in force,
the link's absence is a BREAK and a REFUSAL on the rule above, and no scope note
written before that tranche existed may be read as permitting it. **This
paragraph and the scenario below are AMENDED BY TRANCHE TWO** — they were written
at tranche one in terms of "a later tranche's link" and of "links 1–3", which,
left standing beside tranche two's extended walk, would have put a permission and
a refusal on ONE antecedent in one promoted capability.

#### Scenario: valid artifacts from different executions are submitted together

- WHEN the gate receives links that individually verify but do not share one chain identity and predecessor sequence
- THEN it REFUSES, naming the broken continuity
- AND per-link validity is never accepted in place of continuity

#### Scenario: a link is missing

- WHEN any link a ratified tranche has put in force is absent — links 1–3 at tranche one, and any of links 1–6 from tranche two
- THEN the gate REFUSES and reports a fraud signal
- AND the outcome is never downgraded to a warning, an advisory, or a finding to be triaged

#### Scenario: the grant was revoked before the exercise

- WHEN a chain is offered whose ratifying signature is cryptographically valid, but whose exercise records a revoked grant, a revoked ancestor, or a revoked holder
- THEN the gate REFUSES, because a valid signature is not current authority and revocation does not invalidate a signature
- AND the structural checks passing is never accepted in place of standing at exercise

#### Scenario: a machine-held wallet signs and attests itself honestly

- WHEN an agent-held wallet signs a ratification and the recorded actor correctly attests that same wallet
- THEN the gate REFUSES on HOLDER CLASS, because ratifying authority is human-held
- AND correct attribution is never accepted as evidence that the attributed holder was eligible to ratify

#### Scenario: the proof of possession was never verified

- WHEN a chain is offered whose exercise records the proof as presented but carries a verification failure, or records an unauthenticated request
- THEN the gate REFUSES
- AND the presence of an exercise record is never accepted in place of a verified proof

#### Scenario: the signer and the recorded actor differ

- WHEN a chain is offered whose signature, digests, inception leaf and traveling contract are all internally consistent, but whose recorded actor attests a different wallet than the one whose key signed
- THEN the gate REFUSES, because internal consistency establishes that one chain is whole and not whose it is
- AND the five structural checks passing is never accepted in place of the actor binding

#### Scenario: the gate compares the content digest against the chain identity

- WHEN a gate implements the chain-identity check by comparing the ratification's content digest to the carried chain identity
- THEN it is REFUSED as an incorrect gate, because that comparison rejects every conforming chain
- AND the conforming check recomputes the digest of the SIGNED ratification, the content digest belonging to the separate replay check

#### Scenario: the gate cannot evaluate the chain

- WHEN the log is unreachable, a key is unresolvable, or the chain cannot otherwise be evaluated
- THEN the gate REFUSES rather than proceeding
- AND an unevaluable condition is never reported as a pass

#### Scenario: a link no ratified tranche has yet put in force is absent

- WHEN the gate walks a chain that carries no link from a tranche later than the tranches whose requirements are in force
- THEN it validates the links in force and returns a verdict scoped to them
- AND the absent not-yet-in-force link is not reported as a break, while the absence of a link a ratified tranche HAS put in force is a break and a refusal
