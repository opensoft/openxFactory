# signed-execution-chain Specification (delta)

## ADDED Requirements

### Requirement: Ratification presents wallet-carried authority, proven by possession

openxFactory SHALL admit a ratifying act only where the ratifying human has
PRESENTED a wallet-carried grant and that presentation has been PROVEN BY
POSSESSION, and SHALL express both the grant and the proof in the already
shipped `openxwallet` vocabulary rather than in any vocabulary this capability
defines. The grant is an `xfactory_wallet_grant`; the presentation is an
`xfactory_wallet_grant_exercise` whose `proof_of_possession` records what was
presented, whether it verified, what the signature covered, and which key
presented it. The ratification record REFERENCES that exercise by identifier and
carries no second proof, key, identity or grant vocabulary of its own — a
possession claim that is asserted rather than demonstrated is not a
presentation, and a second vocabulary for the same act would be the two-records-
of-one-decision defect at contract scale.

**THE EXERCISE SHALL BE BOUND TO THE EXACT RATIFICATION, AND A REFERENCE IS NOT
A BINDING.** An identifier alone would let a previously successful exercise be
REPLAYED as the proof for a different ratification, satisfying every other check
while the human signed something else — so this capability requires two things
the shipped schema leaves optional, as a SCOPE RESTRICTION BY THE CONSUMING
CAPABILITY rather than as a schema change (the S2 precedent, which made
`issued_by` required for review-class grants without editing the shared grant
schema): the exercise SHALL carry `object_ref` holding THE RATIFICATION'S
CONTENT DIGEST, spelled in the shipped identifier grammar so the value is
recomputable and comparable rather than merely nominal; and its
`proof_of_possession.signed_over` SHALL be `request_digest`. An exercise whose
`object_ref` digest is not this ratification's digest is REFUSED AS A REPLAY,
and its own validity is not a defence.

**AND THE RESIDUAL IS RAISED AS AN EXPLICIT GAP RATHER THAN CLAIMED AS CLOSED.**
`signed_over` is an ENUM SELECTOR — it names WHAT the signature covers, and the
pinned schema carries NO field holding the signed digest VALUE. So the record
alone cannot prove the signed request included `object_ref`, and this
requirement does not pretend otherwise: the digest comparison above is
enforceable today, the step from "the record names this ratification" to "the
signature covers this ratification" rests on the realization ESTABLISHING that
the signed request includes `object_ref`, and a realization that cannot
establish it SHALL DECLARE the shortfall rather than assert the binding. The
durable repair is an additive optional field on the exercise record carrying the
signed subject digest, and it belongs to `opensoft/openXwallet` as a NAMED
SUCCESSOR — not to this capability, which would otherwise be defining a second
proof vocabulary to escape a gap in the first. The staged topic's own
instruction governs: every link resolves to an existing family OR is raised as
an explicit gap.

**THIS REQUIREMENT IS Q1 AS RULED.** Brett Heap ruled Q1 on 2026-08-29 AS
RECOMMENDED: presentation is expressed in the SHIPPED grant vocabulary plus a
PROOF-OF-POSSESSION step, and the presentation is recorded in the RATIFICATION
RECORD ITSELF, with no new artifact created for it. This requirement is written
to that ruling and no longer flags it as open. Q1's "rather than a new artifact"
is read as *invent no new artifact* — Narrowing B as it was raised — and the
ruling settles that reading directly, since it says in terms that no new
artifact is created for the presentation; the shipped exercise record is
therefore REFERENCED and nothing is minted beside it.

**WHAT THIS REQUIREMENT ADDS BEYOND THE RULING IS THE BINDING, AND IT IS ADDITIVE
RATHER THAN INTERPRETIVE.** Q1 settles WHERE the presentation is recorded; it
does not say that recording a valid exercise makes it this ratification's
exercise. The `object_ref` and `signed_over` obligations above close the replay
hole that silence would leave open, and they narrow the consuming capability
without touching the ruled answer or the pinned schema.

#### Scenario: a grant is presented with no proof of possession

- WHEN a ratification presents a wallet-carried grant and no proof of possession
- THEN the ratification is REFUSED naming the missing proof, never the missing grant
- AND the refusal is recorded with the closed code `missing_proof_of_possession`

#### Scenario: a proof is presented and does not verify

- WHEN a presented signature is evaluated and does not verify
- THEN the event is recorded as a verification failure and NOT as an absent proof
- AND the ratification is REFUSED, because a failed proof is a stronger signal than a missing one, never a weaker one

#### Scenario: a presentation verifies

- WHEN the presented proof verifies against the presenting key
- THEN the ratification record names the exercise record, the grant, and the presenting key
- AND no new proof artifact, key record, or grant kind is created by this capability

#### Scenario: a valid exercise from an earlier ratification is presented

- WHEN an exercise that verified for one ratification is offered as the proof for a different one
- THEN the ratification is REFUSED as a replay, because its `object_ref` digest is not this ratification's digest
- AND the exercise's own validity is not accepted as a defence

#### Scenario: the realization cannot establish what the signature covered

- WHEN a realization cannot establish that the signed request included `object_ref`
- THEN it DECLARES that shortfall and does not assert the binding it cannot prove
- AND the declaration names the openXwallet successor field as what closes it, so the gap is visible rather than implied

#### Scenario: the grant was valid at issuance and is revoked now

- WHEN a grant is presented whose revocation check at exercise returns revoked
- THEN the ratification is REFUSED
- AND validity recorded at issuance is not accepted as evidence of validity at presentation

### Requirement: The actor a chain records is bound to the wallet that signed

openxFactory SHALL bind the ACTOR a chain link records to the WALLET whose key
made the exercise that link descends from, and SHALL NOT accept a valid exercise
as evidence of WHOM the act is recorded as. The chain records its actor as
`identity-brokering`'s stable opaque subject; that subject SHALL carry a wallet
attestation naming the wallet whose key made the exercise; the chain SHALL check
that the two agree; and the binding SHALL be covered by the signed bytes so it
cannot be attached after the signature. Without this, a link may reference one
holder's valid exercise while recording a different, well-formed opaque subject,
and every other check in this capability still passes — the exercise proves who
SIGNED, and nothing else in the delta ties that to whom the act is ATTRIBUTED.

**THE DIRECTION OF THE BINDING IS FIXED BY THE PINNED CONTRACT AND THIS
CAPABILITY DOES NOT REVERSE IT.** `openxwallet-subject-attestation`, consumed at
the `wallet-v1.3` pin (`contracts/openxwallet-pin.yaml`), closes
`resolution.resolved_by` to `subject_ref` precisely so that a record cannot
declare it resolves a subject THROUGH a wallet — the ratified rule that a wallet
identifier never becomes a subject identifier. A subject is therefore resolved by
its own identifier and never through a wallet, and the wallet reference is checked
as an ATTESTATION only. Stating the obligation without its direction would invite
a realization to satisfy it by resolving the actor from the wallet, which the
pinned contract refuses.

#### Scenario: the recorded actor is not the holder that signed

- WHEN a link names a well-formed opaque subject and references a valid exercise, but that subject attests a different wallet than the one whose key made the exercise
- THEN the link is REFUSED
- AND the validity of the exercise does not admit it, because the exercise proves who signed and not whom the act is recorded as

#### Scenario: the recorded actor attests no wallet at all

- WHEN a link's actor subject carries no wallet attestation
- THEN the link is REFUSED rather than accepted on the strength of the exercise alone
- AND the absence is never read as an attestation that happens to be omitted

#### Scenario: the binding is attached after the signature

- WHEN the actor-to-wallet binding is present but falls outside the bytes the ratifying signature covers
- THEN it is REFUSED, because a binding attachable afterwards is a binding anyone can attach
- AND the link is not accepted on the strength of the binding's mere presence

#### Scenario: a realization resolves the actor through the wallet

- WHEN a realization resolves the actor subject by looking up the wallet that signed
- THEN it is REFUSED, because the pinned subject-attestation contract closes `resolution.resolved_by` to `subject_ref`
- AND the wallet reference is checked as an attestation and never used to resolve identity

### Requirement: Ratification and chain inception are one signed act

openxFactory SHALL perform CHAIN INCEPTION — the registration of a ratification
into the signed-execution-chain registry, minting the CHAIN IDENTITY as the
digest of the signed ratification — in the SAME signed act as the ratification
it registers, so that a ratified-but-uninscribed state is constructively
impossible rather than merely discouraged. Either both stand or neither does: an
inception that fails leaves no standing ratification, and a chain identity that
exists with no ratification behind it is a fraud signal under this capability's
refusal requirement. The act SHALL be performed OUT-OF-PIPELINE — outside the
codexFactory clearance-envelope pipeline — and the record SHALL cite the ground:
the `gate_rules_council` convening of 2026-08-28 established, code-level and
unanimously, that a class over `openspec/changes/**` can never commission a
council, because that surface lies wholly inside the canonical
`GATE_INTEGRITY_FLOOR`, which is evaluated before any clearable classification
(984 admitted paths, 984 floored, 0 remaining; `gate_integrity` declared, absent,
and no rule document at all all park identically). Routing inception through the
pipeline would describe a control that provably cannot run. **That measurement
is the ground for the surface this repository's ratifications actually land on;
the rule itself is not surface-dependent**, because a pipeline that CLEARS
candidates cannot also be what CONFERS the authority those candidates are
cleared against — a chain whose first link is minted by the mechanism it exists
to permit is circular, and would be circular on any surface, floored or not.

**RE-RATIFYING AN UNCHANGED SUBJECT SHALL PRODUCE A DIFFERENT CHAIN, AND THE
SIGNED BYTES ARE WHAT MAKE THAT TRUE.** The chain identity is the digest of the
signed ratification, so re-ratifying an unchanged subject would otherwise produce
identical bytes, an identical digest and — under a deterministic signature
scheme — an identical signature: the "new" chain would silently BE the old one,
and no refusal in this capability would catch it, because nothing would look
wrong. The bytes covered by the ratifying signature SHALL therefore carry a value
UNIQUE TO THE RATIFYING ACT, and this capability NAMES that value rather than
minting one: the identifier of the grant exercise that proved link 1, since one
exercise is one act and the pinned exercise record already carries it.

**NAMING THE VALUE IS NECESSARY AND NOT SUFFICIENT — UNIQUENESS IS ENFORCED
HERE.** The pinned schema validates the exercise identifier as a generic
identifier and constrains nothing about its reuse, so a producer that reuses one
while re-ratifying an unchanged subject reproduces the identical bytes and the
collision returns by the back door. This capability SHALL therefore REFUSE an
inception whose named per-act value has already been consumed by an existing
chain. The rule is stated rather than assumed because an obligation a consumed
contract does not carry is this capability's to enforce or to declare as a
dependency, never to take on trust.

**CHAIN INCEPTION IS NOT ENROLLMENT.** `specs/025-openxfactory-review-lane-caller/spec.md`
FR-008 owns the word "enrollment" in this repository for a different act — the
entry of a candidate class into a `merge-approval-envelope` for the codexFactory
decision core to classify. Chain inception creates no envelope, names no
candidate class, touches no ruleset and produces no verdict; candidate-class
enrollment mints no chain identity and is not a link in any chain. FR-008 stays
gated exactly as the convening left it, and nothing in this capability
discharges, amends or relies on it.

#### Scenario: inception fails after a ratification is signed

- WHEN the inception half of the act cannot complete
- THEN the ratification does not stand and is not recorded as ratified
- AND no partial state is retained that a later reader could mistake for a ratification

#### Scenario: a chain identity is found with no ratification behind it

- WHEN a chain identity resolves to no signed ratification
- THEN it is refused as a fraud signal
- AND it is never treated as an incomplete record awaiting completion

#### Scenario: inception is attempted through the clearance pipeline

- WHEN chain inception is routed through the codexFactory clearance-envelope pipeline
- THEN it parks never-clearable before classification and produces no verdict
- AND the conforming path is the out-of-pipeline act, whose record cites the 2026-08-28 convening

#### Scenario: a reader asks whether inception is 025's enrollment

- WHEN a reader or an implementer treats chain inception as an enrolled candidate class
- THEN the two acts are distinguished by name and neither substitutes for the other
- AND no `merge-approval-envelope` instance is created by this capability

#### Scenario: an identical subject is ratified twice

- WHEN the same unchanged subject is ratified on two separate occasions
- THEN the two ratifications mint TWO DISTINCT chain identities, because each signs a different per-act value
- AND neither is accepted as a continuation or a re-issue of the other

#### Scenario: a per-act value is reused across inceptions

- WHEN an inception names a per-act value already consumed by an existing chain
- THEN it is REFUSED
- AND the refusal does not depend on the pinned schema having constrained reuse, which it does not

### Requirement: One digest construction governs every digest this capability computes

openxFactory SHALL put exactly ONE digest construction in force for this
capability — a named algorithm and an exact, order-fixed byte serialization —
and that construction SHALL govern EVERY digest the capability computes: the
chain identity, the digest of any predecessor a later tranche's link binds to,
the transparency-log leaf digests, and any digest a later tranche adds. The
construction SHALL be declared in the contract rather than restated in this
specification, so that one fact lives in one place, and every digest a record
carries SHALL be algorithm-tagged so a later migration is a readable change
rather than a silent reinterpretation.

**ONE CONSTRUCTION, DISTINCT SUBJECTS — AND THE DISTINCTION IS LOAD-BEARING.**
The construction is shared; what each digest is taken OVER is not, and this
capability computes three that a reader can conflate. The **ratification's
content digest** is taken over the subject being ratified, and it is what an
exercise's `object_ref` carries. The **chain identity** is taken over the SIGNED
ratification — a superset of that content, since the signed bytes also carry the
reference to the exercise and its per-act value. A **leaf digest** is taken over
a transparency-log leaf. Each record SHALL name which subject its digest is
taken over, because a construction rule that fixes the algorithm while leaving
the subject implicit produces readers that agree on how to hash and disagree on
what. The content digest and the chain identity in particular MUST NOT be
equated: doing so would make the exercise's `object_ref` depend on the signature
that has not been made yet, and no implementation could construct the record.

**THE RULE IS STATED ONCE, DELIBERATELY, AND NOT PER DIGEST.** A requirement that
mandates agreement between readers while naming neither algorithm nor encoding
makes agreement impossible: two readers serializing the same record differently
derive different digests, and neither can verify the other. Declaring the
construction beside each digest that needs it would repair one site and invite a
third rule beside the second — which is exactly how this defect appeared twice in
this packet's ancestry, once for the chain identity and once for the predecessor
digest. A capability that computes digests SHALL NOT carry a second construction
rule anywhere.

#### Scenario: a reader derives a digest under its own serialization

- WHEN a reader computes a chain identity or a leaf digest under a serialization other than the one in force
- THEN the value it derives does not match and the record is REFUSED
- AND the disagreement is reported as a construction mismatch rather than as a broken chain

#### Scenario: a later tranche adds a digest

- WHEN a later tranche introduces a digest this capability did not previously compute
- THEN it is computed under the SAME construction already in force
- AND no second construction rule is declared beside the first

#### Scenario: a digest is carried untagged

- WHEN a record carries a digest with no algorithm tag
- THEN it is REFUSED, because an untagged digest cannot be migrated without silently changing meaning

#### Scenario: the content digest is equated with the chain identity

- WHEN a realization treats the ratification's content digest and the chain identity as the same value
- THEN it is REFUSED, because the chain identity is taken over the SIGNED ratification and the content digest over the subject ratified
- AND the equation is unbuildable in any case, since it would make an exercise's `object_ref` depend on a signature not yet made

#### Scenario: a digest names no subject

- WHEN a record carries a correctly constructed, algorithm-tagged digest that does not name what it was taken over
- THEN it is REFUSED, because readers that agree on how to hash can still disagree on what was hashed

### Requirement: The signed ratification travels with the work

openxFactory SHALL require the signed ratification to be carried WITH the work
as a TRAVELING CONTRACT — a self-contained artifact checkable at the point of
use — rather than as a row in a table the checker must go and look up. The
traveling contract carries the chain identity, the reference to the presentation
that proved link 1, and the digest of the transparency-log leaf that recorded
inception, so that a checker can establish what permits this work without
resolving a live service. Work that arrives with no traveling contract is
UNPERMITTED at the point of use, not merely unattributed; and a traveling
contract whose chain identity does not match the record it claims is a fraud
signal under this capability's refusal requirement rather than a stale copy.

#### Scenario: work arrives with no traveling contract

- WHEN a consuming step evaluates work carrying no traveling contract
- THEN the step REFUSES, because nothing establishes what permits the work
- AND the absence is never read as an unremarkable omission

#### Scenario: the carried digest disagrees with the record

- WHEN a traveling contract's chain identity does not match the ratification it names
- THEN it is refused as a fraud signal
- AND the mismatch is never resolved in favour of the carried copy

#### Scenario: the checker cannot reach the registry

- WHEN a checker at the point of use cannot resolve the registry or any live service
- THEN it can still establish the traveling contract's internal consistency from the artifact alone
- AND that establishes consistency ONLY — a check whose question requires the log still refuses while the log is unreachable, per this capability's gate requirement
- AND an unresolvable external lookup never converts into permission

### Requirement: The signed transparency log is the record

openxFactory SHALL maintain an APPEND-ONLY SIGNED TRANSPARENCY LOG in the
governed store as the primary chain of custody, and SHALL record every act this
capability governs as a SIGNED LEAF on the RFC-6962 / Certificate-Transparency
and Sigstore-Rekor pattern: the wallet-presented ratification, the chain
inception, the issuance of a traveling contract, and every verdict the
short-chain gate returns. Leaves are appended and never edited or removed.

**THE DETECTION GUARANTEE IS STATED AT THE STRENGTH IT ACTUALLY HAS**, because
an overstated guarantee is worse than a declared gap. The log's hash structure —
not an access control and not a convention — detects any alteration WITHIN A
PREFIX SOME PARTY HAS ALREADY OBSERVED: a consistency proof against a previously
observed signed tree head fails, and every traveling contract carries the digest
of the leaf that recorded its inception, so a truncation dropping an observed
leaf is caught AT THE POINT OF USE. **What the log ALONE cannot detect is suffix
truncation no party has yet observed** — a store that deletes its newest leaves
and rolls back to an earlier valid signed tree head presents a shorter log that
still verifies to a fresh reader. That residual SHALL be DECLARED under the
realization-conformance obligation rather than covered by a promise this tranche
cannot keep, and it is exactly what the tranche-three anchor closes, by making a
tree head externally witnessed. An undeclared shortfall is non-conformance; the
identical shortfall, declared, is conformant.

THE LOG IS THE RECORD. Public anchoring is
a LATER ADDITION that makes the record externally undeniable and belongs to the
named tranche-three successor; the absence of an anchor at this tranche is
therefore NOT a defect, and no requirement here may be read as claiming external
undeniability the log alone does not provide.

#### Scenario: a governed act occurs and writes no leaf

- WHEN an act this capability governs completes with no corresponding signed leaf
- THEN the act is UNPROVEN and every consumer that requires the chain refuses it
- AND the act's own success is not evidence that it was permitted

#### Scenario: a leaf inside an observed prefix is altered or removed

- WHEN a leaf's bytes change, or a leaf is dropped, within a prefix some party has already observed
- THEN the consistency proof against that observed signed tree head fails and the alteration is detected
- AND it is reported as a fraud signal rather than as a corrupted file

#### Scenario: the newest leaves are truncated before anyone observes them

- WHEN a store deletes its newest leaves and presents an earlier valid signed tree head
- THEN the log alone cannot detect it, and the realization DECLARES that residual rather than claiming coverage
- AND the declaration names tranche-three anchoring as what closes it, so the gap is visible instead of implied

#### Scenario: an external anchor is expected at this tranche

- WHEN a reader asks the log for an external anchor or an inclusion receipt
- THEN the log states that anchoring is a named tranche-three successor and claims none
- AND the missing anchor is not counted as a broken link

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
4. the inception leaf commits to that same chain identity; and
5. the traveling contract's carried chain identity and carried leaf digest EQUAL
   the values established above; and
6. the ACTOR the chain records is bound to the wallet that signed, per this
   capability's actor-binding requirement — the actor's subject carries a wallet
   attestation, that attestation names the wallet whose key made the exercise,
   and the binding falls inside the signed bytes.

**CHECK 6 IS NOT OPTIONAL AND ITS ABSENCE IS NOT COVERED BY THE OTHERS.** Checks
1–5 establish that ONE chain is internally consistent; none of them establishes
WHOSE it is. A ratification signed by one holder whose actor field names another
passes every one of them — the signature verifies, the digests agree, the
inception leaf commits, the traveling contract matches — while the chain records
authority that its signer never exercised. A gate that enumerates its checks
exhaustively and omits this one permits misattributed authority at the terminal
act, which is the precise harm the actor-binding requirement exists to prevent.
Stating the requirement without walking it at the gate would leave it inert.

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
never reads as permission. The gate's scope at this tranche is links 1–3 and it
SHALL NOT report the absence of a later tranche's link as a break, because a
gate cannot walk a link that does not exist yet.

#### Scenario: valid artifacts from different executions are submitted together

- WHEN the gate receives links that individually verify but do not share one chain identity and predecessor sequence
- THEN it REFUSES, naming the broken continuity
- AND per-link validity is never accepted in place of continuity

#### Scenario: a link is missing

- WHEN any of links 1–3 is absent
- THEN the gate REFUSES and reports a fraud signal
- AND the outcome is never downgraded to a warning, an advisory, or a finding to be triaged

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

#### Scenario: a tranche-two link does not exist yet

- WHEN the gate walks a chain that carries no attestation link
- THEN it validates links 1–3 and returns a verdict scoped to them
- AND the absent later link is not reported as a break

### Requirement: Ratifying authority is human-held

openxFactory SHALL require the authority that INCEPTS a chain — the tier-1
ratifying credential — to be held by a NAMED HUMAN, and SHALL refuse it to an
agent, a runner, a lane, a workflow identity, or any other machine holder. The
ground is constitutional rather than conventional: every omnigent worker
archetype carries `access_secrets: false`, so a worker cannot hold an authority
credential, and a design in which a runner signs AUTHORITY contradicts ratified
text. Tier 2 — ephemeral per-task attestation identities, whose keys never enter
a worker — is the named tranche-two boundary and is NOT defined here; no
attestation identity of any kind is created by this capability.

**THE SCOPE OF "AUTHORITY" HERE IS NARROWING A, RULED BY BRETT HEAP ON
2026-08-29 IN SESSION.** The staged topic's tier model says tier-1 credentials
are "never held by an agent, a runner, or a lane". Read literally that refuses
`wal-agent-mrc-0001` — a REALIZED agent-held wallet backing an active `review`
grant that this repository runs today — so the literal reading would make a
shipped artifact nonconformant on this capability's first day. He ruled that
**tier 1 is RATIFYING authority**: the human-held constraint binds the RATIFYING
act, agent-held REVIEW wallets stay lawful, and what this requirement refuses is
an agent-held wallet performing a RATIFICATION. This is a ruling of record, not
a reading this capability adopted on its own authority; it was raised as a
narrowing, it was not reached by the 2026-08-29 clarify sitting, and it was ruled
separately in the same session.

The ruling is also independently supported by ratified text, which is why it
narrows nothing that matters: an agent-held wallet's custody is
`holder_readable`, and under `add-trust-anchor`'s ratified declared-custody rule
that evidences the HOST acted — precisely what a ratification may not stand on.
So the review wallet could never have carried a ratifying grant regardless, and
the ruling removes a false refusal without creating a real permission.

#### Scenario: a machine holder is named as ratifying authority

- WHEN a grant naming an agent, runner, lane, or workflow identity as holder is presented to incept a chain
- THEN the ratification is REFUSED
- AND the refusal names the holder class rather than the missing signature

#### Scenario: a runner asks for the ratifying key

- WHEN any worker, runner, or lane requests custody of a tier-1 credential
- THEN the request is REFUSED and no key material crosses into it
- AND a short credential lifetime is not accepted as making a key non-secret

#### Scenario: an attestation is offered as authority

- WHEN a record attesting what ran is presented in place of a record of who permitted
- THEN it is REFUSED as answering a different question
- AND neither tier is ever accepted as standing in for the other

#### Scenario: an agent-held review grant is presented for review, not ratification

- WHEN an agent-held wallet exercises a `review`-act grant
- THEN this requirement does not refuse it, because reviewing is not incepting a chain
- AND the same holder remains refused for any ratifying act

### Requirement: The capability confers and refuses nothing until a named reader runs as a required check

This capability SHALL confer and refuse nothing until a NAMED validator that
reads its records runs as a REQUIRED check on the repository that holds them,
and until that check is required its records SHALL be treated as documentation
that governs nothing. No statement of this capability SHALL describe a rule
inside a validator as though the description were the enforcement, and any
statement of what the chain enforces SHALL NAME the check that enforces it;
where no such check exists, the requirement is UNMET rather than partially met.

The rule is carried HERE rather than inherited by implication from
`review-authority-intake`'s ratified *"A grant with no reader in a required
check confers nothing"*, because a rule relied on by implication is a rule
nobody checks. It is also what keeps the gate requirement above honest: a
workflow file that validates chains is not evidence that chains are validated —
the ruleset state is, which is the same distinction
`add-wallet-carried-review-authority` tasks 2.5/2.6 already drew for
`wallet-validation` in this repository.

#### Scenario: the validator exists in no required check

- WHEN the chain validator is present in the repository but appears in no workflow that is a required check
- THEN every chain record confers nothing, and the capability states so rather than asserting the chain's properties in the present tense

#### Scenario: a described control is offered as an existing one

- WHEN a requirement of this capability is stated as satisfied by a rule inside a validator
- THEN the statement MUST name the required check under which that validator executes
- AND where no such check exists the requirement is UNMET, not partially met

#### Scenario: the capability is promoted before any reader exists

- WHEN this capability's requirements reach the promoted specification and no reader is yet required anywhere
- THEN the capability is recorded as conferring nothing yet, with the reader named as the outstanding realization obligation

#### Scenario: a merged workflow file is offered as the required check

- WHEN a merged workflow that runs the validator is offered as evidence that the check is required
- THEN it is REFUSED as evidence, because merging a workflow does not make it required
- AND the ruleset state naming the check is what discharges the obligation
