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
like every link from link 4 onward, **WRITTEN AS A LEAF BEFORE THE ATTESTATION
IT COVERS IS PRODUCED**. The expected set is then link 4 AS EXTENDED. Three
refusals keep the extension from becoming the hole it exists to close:

1. **AN EXTENSION WRITTEN AFTER THE ATTESTATION IT COVERS IS REFUSED**, because
   an expectation recorded after the fact is a description and not an
   expectation.
2. **A LINK-5 ATTESTATION FOR A TASK NO COMMITMENT COVERS IS REFUSED**, so
   extension cannot be skipped by simply attesting anyway.
3. **AN EXTENSION SIGNED ANYWHERE OTHER THAN AT THE CONTROLLER IS REFUSED**,
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

#### Scenario: a commitment extension is written after the attestation it covers

- WHEN a controller-signed extension naming a dispatched task is written to the log after that task's link-5 attestation leaf
- THEN it is REFUSED, because an expectation recorded after the fact is a description and not an expectation
- AND the extension's correct content and valid signature are not accepted in place of its being written first

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

#### Scenario: a chain fans out to several tasks and one link-6 decision is signed

- WHEN a chain dispatches several tasks and the chain-scoped tier-2 identity signs the single link-6 PR-open decision record committing to every one of their link-5 attestations, at the controller
- THEN it is CONFORMING, because the decision is a record about the CHAIN and the chain-scoped identity's closed enumeration names that record kind
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

- WHEN the controller's key moves into hardware-backed custody
- THEN the design remains conforming, because the key has moved further from the worker and never closer
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
committing to its predecessor. Individually valid setup, runner and PR-open
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

## MODIFIED Requirements

### Requirement: A gate validates the short chain as a hash-linked chain

openxFactory SHALL operate, FROM THIS TRANCHE, a gate that validates links 1–3
before permitting the terminal act, and SHALL validate them as A CHAIN rather
than as a bag of signatures — CONTINUITY, never merely the presence of the
required signatures. Continuity means one chain identity carried unbroken from
the ratification that minted it through every link the gate walks; how each link
binds to it depends on whether that link has a signer, which the two paragraphs
below settle for tranche one and for tranche two respectively.

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
signature cannot cover an inception record created from it. **At this tranche
continuity is therefore established BY DERIVATION AND COMPARISON, not by a third
signature**, and the gate SHALL validate exactly that, over the digest subjects
this capability's digest requirement fixes:

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
validates EXACTLY these checks before the terminal act, **every requirement of
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
different chain identities.

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

- WHEN any of links 1–3 is absent
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
