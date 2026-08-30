# chain-anchoring Specification (delta)

## ADDED Requirements

### Requirement: The multi-anchor receipt format is defined FIRST and is chain-agnostic

openxFactory SHALL define the anchor receipt as a CHAIN-AGNOSTIC MULTI-ANCHOR
record before it defines any anchor target, and SHALL express every anchor this
capability ever mints in that one format. The receipt is: the anchored DIGEST,
then the AGGREGATION MERKLE PATH from that digest to the aggregated root, then a
PER-CHAIN LIST whose every entry carries — for that chain — the ANCHOR
TRANSACTION BYTES, the TRANSACTION-TO-BLOCK OR DAG INCLUSION PROOF, and the
BLOCK HEADER. All three per-chain elements are CAPTURED WHOLE AT ANCHOR TIME and
stored in the receipt; none of them is a lookup deferred to verification time.

**A TRANSACTION REFERENCE PLUS A HEADER IS NOT A PROOF, AND THIS FORMAT REFUSES
TO PRETEND IT IS.** A block header commits only to a transaction root, so a
header beside a bare transaction identifier proves nothing once the transaction
itself is unavailable — which on a pruning chain is a certainty within days and
on any chain is the ten-year assumption. A receipt that omits the transaction
bytes or the inclusion proof for any chain in its list SHALL BE REFUSED AT
CAPTURE TIME, not accepted and flagged, because a receipt is only ever captured
once and the missing material cannot be recovered afterwards.

**THE RECEIPT IS WHY ANCHOR SELECTION IS REVERSIBLE, AND THAT IS ITS PURPOSE
RATHER THAN A SIDE EFFECT.** Anchor targets SHALL be addable and droppable by
changing the per-chain LIST, never the FORMAT, and never anything in the
evidence plane: adding a target appends an entry to receipts minted afterwards,
dropping a target stops new entries and invalidates no receipt already captured.
A bespoke receipt shaped around one chain's proof structure SHALL BE REFUSED —
it is the one-way door this capability exists to avoid, and the staged topic's
exit path names building the receipt first for exactly this reason.

#### Scenario: a receipt carries a transaction reference and a header but no inclusion proof

- WHEN a receipt is offered whose per-chain entry names a transaction and a block header and carries no transaction-to-block or DAG inclusion proof
- THEN the receipt is REFUSED AT CAPTURE TIME
- AND the refusal names the missing inclusion proof rather than reporting the receipt as incomplete-but-stored

#### Scenario: a receipt defers the transaction bytes to verification time

- WHEN a receipt records a transaction identifier and expects the transaction to be re-fetched when the anchor is later verified
- THEN it is REFUSED, because a chain that prunes will not have the transaction to return
- AND the refusal holds even where the chain in question does not prune today, because the format is one format and a ten-year claim is made against all of them

#### Scenario: an anchor target is dropped from the configuration

- WHEN an anchor target is removed
- THEN receipts already captured continue to verify from the material they carry, and no receipt is re-minted
- AND nothing in the evidence plane is touched, because the evidence plane never referenced the target

#### Scenario: an anchor target is added to the configuration

- WHEN a new anchor target is adopted by a ruling
- THEN the per-chain list of receipts minted afterwards gains an entry and the receipt FORMAT is unchanged
- AND no earlier receipt is rewritten to claim a witness it never had

#### Scenario: a receipt is verified after its operational chain has pruned

- WHEN an anchor is verified long after the anchoring chain has discarded the transaction
- THEN verification succeeds from the transaction bytes, inclusion proof and header the receipt itself carries
- AND no request to the chain is required for the receipt to prove what it proves

#### Scenario: a single-chain receipt shape is proposed for convenience

- WHEN a realization proposes a receipt shaped around one chain's proof structure because only one chain is configured at that moment
- THEN it is REFUSED as a one-way door, and the chain-agnostic format is used with a one-entry list
- AND the refusal is recorded against this requirement rather than treated as a style preference

### Requirement: Both ruled witnesses anchor every anchored item, with no selectivity

openxFactory SHALL anchor every anchored item to BOTH configured witnesses, and
SHALL NOT make a per-item choice about which witness an item receives. The
configuration is Brett Heap's Q3 ruling of 2026-08-29, round two, and it is
carried here as ruled rather than re-derived: the OPERATIONAL witness is Kaspa,
FIRST in order of arrival, answering in seconds when something needs to know now
that a leaf was anchored; the DURABILITY witness is Bitcoin, anchored via
OpenTimestamps AGGREGATION, on EVERY anchored item. **"Primary" is order of
arrival and never evidentiary weight**, and **every ten-year claim SHALL cite
the durability witness**, never the operational one.

**THE OPERATIONAL WITNESS IS ADOPTED UNDER THREE CONDITIONS AND NONE OF THEM IS
OPTIONAL.** The realization SHALL run an ARCHIVAL NODE for it; it SHALL CAPTURE
AND RETAIN full inclusion proofs AT ANCHOR TIME; and its anchors SHALL be
treated as CORROBORATING EVIDENCE, NEVER SOLE evidence. The ground is the
vendored study's finding that this chain's L1 prunes transaction data after
roughly three days, and the ruling carries all three conditions forward
unchanged into the primary seat — the promotion in ordering does not soften the
pruning finding, which is why a ten-year claim still rests on the other witness.

**NO SELECTIVITY, STATED AS A REFUSAL RATHER THAN A PREFERENCE.** A rule that
decides per item which witness that item is worth SHALL BE REFUSED, on the
ruling's own ground: a rule that decides per item is a rule that will eventually
decide wrong about the item that matters. There is likewise no aggregate
`anchored` boolean anywhere in this capability — the receipt records PER-WITNESS
status, so no single true value can stand where a witness is missing.

**THE CONFIGURATION NAMES EXACTLY TWO ANCHOR CHAINS, AND A THIRD IS A RULING AND
NOT AN IMPLEMENTATION CHOICE.** Q3 ruled no third chain. This requirement
therefore refuses a third anchor target adopted by a realization, an operator or
a later author acting alone; it does not forbid one forever, and it writes no
condition under which one would become admissible, because the receipt format of
the requirement above is precisely what makes such an adoption a configuration
change rather than a rebuild.

#### Scenario: an item is anchored to the operational witness only

- WHEN an item reaches the operational witness and the durability witness is skipped for it
- THEN the item is NOT anchored-complete, and no surface reports it as anchored
- AND the omission is a refusal against this requirement, never a latency note

#### Scenario: a rule selects which items get the durability witness

- WHEN a realization proposes anchoring only high-value items to the durability witness, on cost or volume grounds
- THEN it is REFUSED as selectivity, and the cost ground is answered by aggregation rather than by selection
- AND the refusal cites the ruling's own reasoning, that a per-item rule will eventually decide wrong about the item that matters

#### Scenario: a ten-year claim cites the operational witness

- WHEN a claim about an item's integrity over a decade is made against the operational witness's anchor
- THEN the claim is REFUSED, and the same claim against the durability witness is admitted
- AND the operational witness's anchor remains valid corroboration of the same fact at a shorter horizon

#### Scenario: an operational-witness anchor is captured without retaining its inclusion proof

- WHEN an anchor is written to the operational witness and the inclusion proof is not captured at anchor time
- THEN the anchor is REFUSED and the item is not credited with that witness
- AND a plan to re-derive the proof later is not accepted, because the chain will have pruned the material the derivation needs

#### Scenario: an operational-witness anchor is offered as the sole evidence for a claim

- WHEN a verification is asked to stand on the operational witness alone
- THEN it is REFUSED, because that witness is corroborating and never sole
- AND the refusal names the durability witness as what the claim actually requires

#### Scenario: a third anchor chain is added by a realization

- WHEN a realization, operator or later author adds a third anchor target without a ruling
- THEN it is REFUSED, because the configuration is ruled and not an implementation choice
- AND no condition is written here under which a third target would become admissible, since a later ruling answers to its own evidence

### Requirement: A missing witness is a declared, fail-closed state and never silently fine

openxFactory SHALL treat an item carrying fewer witnesses than the configuration
demands as `anchor_incomplete` — a DECLARED state with its missing witnesses
NAMED — and SHALL NOT report, present or verify it as anchored. Anchoring is a
two-phase, deadline-bounded obligation rather than an instantaneous act: an item
enters `anchor_pending` when validated material is submitted, and each witness
carries its own declared COMPLETION HORIZON, because the durability witness's
aggregation is deferred by hours even when everything is healthy and a rule that
demanded both witnesses instantly would refuse every item in the healthy path.

**WHAT FAILS CLOSED IS THE CLAIM, NOT THE FACTORY.** The transparency log is the
evidence plane and a leaf's standing has never depended on an anchor, so a
witness outage SHALL NOT block ratification, execution, review or any gate. What
it blocks is the CLAIM: while an item is `anchor_incomplete`, any verification of
it SHALL return `anchor_incomplete` naming the missing witnesses — never a bare
pass, and never a bare fail, because both of those are answers the record cannot
support. A ten-year claim over such an item is REFUSED outright while the
durability witness is missing.

**THE TWO OUTAGES ARE NOT SYMMETRIC AND THE SEMANTICS SAY SO.** Where the
OPERATIONAL witness is unreachable, the durability witness still completes on its
own horizon: the item reaches durability-only completeness, which is NOT the
configured completeness, so it stays `anchor_incomplete` and is not presented as
anchored — while the ten-year claim over it IS available, because that claim
rests on the witness that landed. Where the DURABILITY witness's aggregation
calendar is unreachable, the operational witness completes and ten-year claims
are REFUSED until the durability anchor lands; and because an aggregation proof
completes by UPGRADE, the pending receipt SHALL be completed in place when the
calendar returns and the item SHALL NOT be re-anchored — re-anchoring would mint
a second transaction for the same digest and leave two proofs to keep where one
was owed.

**THE INCOMPLETENESS IS ITSELF EVIDENCE, SO A SILENT GAP IS IMPOSSIBLE.** Entry
into `anchor_pending`, every horizon breach, and the eventual completion SHALL
each be written as a leaf in the evidence plane. Past its horizon an item stays
`anchor_incomplete` and an operator obligation is raised; the anchoring
subsystem SHALL NOT mark an item complete by any path other than a CAPTURED
RECEIPT meeting the receipt requirement above. An outage is exactly the
circumstance that would otherwise become selectivity by accident — "this one
only got the one witness, and that was fine" — and naming the state is what
stops it becoming a habit.

#### Scenario: the operational witness is unreachable at anchor time

- WHEN the operational chain cannot be reached and the durability anchor completes on its horizon
- THEN the item is `anchor_incomplete` with the operational witness named as missing, and is not presented as anchored
- AND a ten-year claim over it IS admitted, because that claim rests on the witness that landed

#### Scenario: the durability witness's aggregation calendar is unreachable

- WHEN the aggregation calendar cannot be reached and only the operational anchor completes
- THEN the item is `anchor_incomplete`, and every ten-year claim over it is REFUSED until the durability anchor lands
- AND the pending receipt is COMPLETED IN PLACE when the calendar returns, rather than the item being anchored a second time

#### Scenario: a verification runs against an incomplete item

- WHEN an external party verifies an item that is `anchor_incomplete`
- THEN the verification returns `anchor_incomplete` naming the missing witnesses
- AND it returns neither a bare pass nor a bare fail, because the record supports neither answer

#### Scenario: a witness outage is proposed as a reason to hold the gate

- WHEN a realization proposes blocking ratification or merge until both anchors complete
- THEN it is REFUSED, because the evidence plane is the record and an anchor is a late addition to it
- AND the fail-closed obligation is discharged against the CLAIM instead, which is where the missing witness actually bites

#### Scenario: an item passes its completion horizon still missing a witness

- WHEN a horizon elapses and a configured witness has not landed
- THEN the breach is written as a leaf, the item stays `anchor_incomplete`, and an operator obligation is raised
- AND no path other than a captured receipt is permitted to move the item to complete

#### Scenario: an aggregate anchored flag is proposed

- WHEN a realization proposes a single `anchored: true` field summarizing an item's anchors
- THEN it is REFUSED, because such a field can read true while a configured witness is missing
- AND per-witness status in the receipt is what every surface reads instead

### Requirement: Only validated, gate-passed material is anchored

openxFactory SHALL anchor only material that has already passed its governing
gate, and SHALL NOT provide any path by which unvalidated material reaches a
chain. The ground is stated in the staged topic as a design constraint on this
tranche and not as a detail: a broken chain is a fraud signal, nothing on a
chain can be un-published, and a false attestation that reaches a chain is
therefore PERMANENT. Anchoring late is what keeps that from happening, and
because anchoring is aggregated and batched in any case, the cost of lateness is
one aggregation interval rather than an architectural concession.

**THE EVIDENCE PLANE HOLDS EVERYTHING; THE CHAINS WITNESS CHECKPOINTS OF IT.**
The transparency log SHALL NOT be held back waiting for validation — a leaf is
written when the event happens, including a leaf recording a refusal — and only
the ANCHORING of a checkpoint waits. The two are different acts against
different stores, and conflating them would either delay the record or publish
the unvalidated.

**A RETRACTION IS A NEW LEAF AND A NEW ANCHOR, NEVER AN ERASURE.** Where
anchored material is later found wrong, the correction SHALL be recorded and
anchored forward; this capability SHALL NOT claim that any anchored value can be
withdrawn, because it cannot. The only erasure property this capability offers is
the salt destruction of the commitment requirement below, and it is a property of
the COMMITMENT rather than of the anchor.

#### Scenario: material is submitted for anchoring before its gate has passed

- WHEN unvalidated material is submitted to the anchoring path
- THEN it is REFUSED, and the refusal is recorded as a leaf
- AND no configuration, operator flag or urgency argument admits it, because the resulting anchor would be permanent

#### Scenario: a leaf is written for an event that then fails validation

- WHEN an event is written to the transparency log and its validation subsequently fails
- THEN the leaf stands, the failure is written as a further leaf, and neither is anchored as validated material
- AND the log is never held back waiting for a validation outcome

#### Scenario: anchored material is later found wrong

- WHEN an item that has been anchored is found to be false
- THEN the correction is recorded and anchored FORWARD as new material
- AND no claim is made that the original anchor is withdrawn, because nothing on a chain can be un-published

#### Scenario: a low-latency anchoring path is proposed that bypasses the gate

- WHEN a realization proposes anchoring on submission to shorten time-to-witness
- THEN it is REFUSED, because the latency saved is one aggregation interval and the risk taken is permanent
- AND the refusal cites this requirement rather than being argued case by case

### Requirement: The on-chain boundary is contract text carrying a refusing validator

openxFactory SHALL draw the boundary between what is anchored and what stays in
governed custody as CONTRACT TEXT carrying a VALIDATOR THAT REFUSES, not as
guidance to be interpreted. Brett Heap ruled Q2 on 2026-08-29 as recommended and
the boundary is his: ON CHAIN, and nothing else — SALTED KEYED COMMITMENTS,
commitments to consent-log CHECKPOINTS, and the chain anchors; OFF CHAIN — EVERY
PAYLOAD WITHOUT EXCEPTION, plus consent STATE and the SALTS. Prose about where
regulated content may not go erodes; a refusal holds. This mirrors how the
hosting record refuses secret-shaped fields by name.

**THE PAYLOAD REFUSAL IS STRUCTURAL, NOT SEMANTIC, AND THAT MAKES IT BOTH
NEUTRAL AND STRICTER.** The validator SHALL refuse any anchor-bound record
carrying a field that holds record content — cleartext, ciphertext, or any
content-bearing blob — by the SHAPE of the field rather than by recognizing what
the content is about. A neutral validator that refused protected health
information by name would need domain semantics to do it, which this capability
is forbidden to carry; a validator that refuses EVERY payload needs none, and
refuses the regulated ones without having to detect them. Raw regulated content,
ENCRYPTED regulated content and PLAIN-HASHED regulated content are all outside
the boundary, and the structural refusal reaches all three.

**THE UNSALTED-COMMITMENT REFUSAL IS BY DECLARED CONSTRUCTION, BECAUSE THE BYTES
CANNOT TELL YOU.** A salted keyed commitment and a plain digest of the same
record are INDISTINGUISHABLE BY INSPECTION — both are opaque values of the same
width — so this capability SHALL require every anchor-bound commitment to
DECLARE its construction: the algorithm, that it is KEYED and SALTED, and a SALT
CUSTODY REFERENCE resolving into the governed layer. The validator REFUSES a
record declaring no construction, a construction that is not keyed and salted,
and a record whose salt custody reference resolves onto a chain or into the
anchored record itself. This is the half an implementer is most likely to get
wrong, because a plain digest of a record looks like exactly the right thing to
anchor.

**AND THE RESIDUAL IS RAISED AS AN EXPLICIT GAP RATHER THAN CLAIMED AS CLOSED.**
A record that DECLARES a salted keyed construction while anchoring a plain digest
is not detectable from the record, and this requirement does not pretend
otherwise. The declaration and the custody reference are enforceable today; the
step from "the record declares a salted keyed commitment" to "the anchored value
IS one" rests on the realization making the commitment path the ONLY path that
can mint an anchor-bound value, so an undeclared construction is UNREACHABLE
rather than merely refused. A realization that cannot establish that SHALL
DECLARE the shortfall on `add-trust-anchor`'s ratified declared-shortfall
pattern rather than assert a property it cannot show.

**SALT DESTRUCTION IS THE ERASURE MECHANISM, AND ITS CONSEQUENCE IS STATED
RATHER THAN SOFTENED.** Destroying a record's salt renders the anchored residue
effectively anonymous — which is the erasure — and the same act makes the handle
PERMANENTLY UNVERIFIABLE: no later party, including the record's own subject,
can ever again prove that a held copy matches the anchored value. That is not a
defect of the mechanism, it IS the mechanism, and any surface offering erasure
SHALL state the loss before performing it. The ground is the vendored study's
§6: EDPB Guidelines 02/2025 (v2.0, adopted 2026-07-07) hold that a hash of
personal data is itself personal data, and a bare record hash is not HIPAA
Safe-Harbor de-identified either.

#### Scenario: a record carrying a content-bearing field is offered for anchoring

- WHEN an anchor-bound record carries a field holding record content in any form
- THEN it is REFUSED by a named structural check on the field's shape
- AND the refusal does not depend on the validator recognizing what the content is about

#### Scenario: encrypted content is offered on the ground that it is unreadable

- WHEN ciphertext is offered for anchoring because it discloses nothing today
- THEN it is REFUSED, because a public chain is permanent and key management would become the only thing standing between a subject and irreversible disclosure
- AND the refusal is the same structural payload check, reached without classifying the plaintext

#### Scenario: a commitment declares no construction

- WHEN an anchor-bound commitment is offered with no declared algorithm, keying, salting or salt custody reference
- THEN it is REFUSED, because the value alone cannot show what it is
- AND the refusal names the missing declaration rather than reporting an unverifiable value

#### Scenario: a plain digest is declared honestly as a plain digest

- WHEN a record declares an unkeyed, unsalted digest construction
- THEN it is REFUSED as an unsalted commitment
- AND the honesty of the declaration is not accepted as a defence, because the boundary refuses the construction and not the disclosure

#### Scenario: a salt is placed where the anchor can reach it

- WHEN a record's salt custody reference resolves onto a chain or into the anchored record itself
- THEN it is REFUSED, because a salt reachable from the anchor destroys the erasure property the salting exists to provide
- AND salts remain in the governed layer, which is where the ruled boundary puts them

#### Scenario: a realization cannot establish that the declared construction is the minted one

- WHEN a realization cannot show that the commitment path is the only path that mints an anchor-bound value
- THEN it DECLARES the shortfall on the declared-shortfall pattern and does not assert the property
- AND the declaration names what would close it, so the gap is visible rather than implied

#### Scenario: a subject requests erasure of an anchored handle

- WHEN a salt is destroyed to erase the subject's connection to an anchored commitment
- THEN the anchored residue becomes effectively anonymous AND the handle becomes permanently unverifiable, and both are stated before the act
- AND no later party, the subject included, can afterwards prove a held copy matches the anchored value

### Requirement: Consent state lives in the permissioned plane and only checkpoints are anchored

openxFactory SHALL hold consent state, access-control lists, subject-to-record
linkage and the commitment salts in a GOVERNED PERMISSIONED PLANE, and SHALL
anchor only that plane's STATE ROOTS and its consent-log CHECKPOINTS through the
anchoring configuration above. A public chain SHALL never see a per-subject
consent row: a row is publicly linkable to a person, a checkpoint is not, and the
distinction is the whole reason consent is split from its own anchor. The
permissioned plane is a consortium ledger of the Fabric or Besu class where
several external covered entities must share state, and the governed policy plane
otherwise; its selection is a REALIZATION decision and is not fixed here.

**CONSENT AND EXECUTION LOGIC ARE NOT ON THE ANCHORING CHAIN.** Consent,
enrollment and access policy are authority questions, and this capability places
none of them on any anchoring chain and deploys no contract code on one. That is
this configuration's posture, stated positively; this capability writes NO
permanent prohibition and NO condition under which a different posture would
become admissible, because a later change answers to its own evidence rather than
to a condition written here in advance.

**AN UNEVALUABLE CONSENT REFUSES, ON THE FAMILY'S FAIL-CLOSED DOCTRINE.** Where
the permissioned plane cannot be reached, a consent-dependent act SHALL BE
REFUSED rather than proceeding: an unevaluable answer never reads as permission,
and this is the same doctrine the family applies to an unevaluable gate. The
refusal is distinct from the anchoring semantics above — a missing WITNESS
degrades a CLAIM about the past, while a missing CONSENT ANSWER refuses an ACT in
the present.

**REVOCATION'S LIMIT IS STATED RATHER THAN LET TO IMPLY MORE THAN IT DELIVERS.**
A revocation supersedes forward from the moment it is recorded and anchored; it
does not reach a copy already disclosed, and nothing on a chain can be
un-published. Any surface presenting subject control SHALL carry that limit, on
the same honesty the credential-custody work applied to bearer secrets.

#### Scenario: a per-subject consent row is offered for anchoring

- WHEN a consent record naming a subject is submitted to the anchoring path
- THEN it is REFUSED, because it would be publicly linkable to a person
- AND the checkpoint commitment covering that row's log is what is anchored instead

#### Scenario: the permissioned plane's state root is anchored

- WHEN a state root of the permissioned plane is anchored
- THEN it passes through the ruled configuration unchanged, receiving both witnesses and one multi-anchor receipt
- AND the anchoring path treats it as an ordinary anchored item with no consent-specific handling

#### Scenario: the permissioned plane cannot be reached

- WHEN a consent-dependent act runs and the permissioned plane is unreachable
- THEN the act is REFUSED, because an unevaluable consent never reads as permission
- AND the refusal is not conflated with an incomplete anchor, which degrades a claim about the past rather than an act in the present

#### Scenario: a consent is revoked after a disclosure

- WHEN a revocation is recorded and anchored after a record copy has already been disclosed
- THEN the revocation supersedes forward and does not reach the disclosed copy, and the surface says so
- AND no claim of recall or un-publication is made anywhere in the record

#### Scenario: consent enforcement is proposed as on-chain contract code

- WHEN a realization proposes enforcing consent by contract code on an anchoring chain
- THEN it is REFUSED under this configuration, which places consent logic in the permissioned plane
- AND the refusal states no permanent bar and names no trigger condition, because a later change adopting a different posture answers to its own evidence

### Requirement: Verification attempts and refused access are logged leaves

openxFactory SHALL write VERIFY events, FAILED verifications and REFUSED ACCESS
ATTEMPTS as signed leaves in the evidence plane, on the same footing as the
events that produce material. An evidence plane that records only what was
written answers what happened and cannot answer who tried — and for a capability
whose whole purpose is external verifiability, an unrecorded verification attempt
is a hole in exactly the surface the design exposes. Checkpoints over these
leaves are anchored through the configuration above like any other checkpoint.

**THIS OBLIGATION IS CARRIED FROM A NAMED SOURCE.** The vendored MedxChain notes
(`ideation/brainstorm/medxchain-blockchain-medical-records.md`) log views, edits,
FAILED ATTEMPTS and administrative actions, and their appendix names
verification-attempt auditing as an addition the neutral family's ten links do
not yet carry, since those links are framed around what was signed and produced.
This requirement carries it.

**AND THESE LEAVES ARE BOUND BY THE BOUNDARY LIKE EVERYTHING ELSE.** An attempt
leaf SHALL carry no payload and no unsalted commitment, and the checkpoint over
attempt leaves is what a chain sees — never an attempt row, which would publish a
who-looked-at-what trail to a permanent public ledger and leak by metadata what
the payload rules keep off it.

#### Scenario: a verification succeeds

- WHEN an external party successfully verifies an anchored item
- THEN the verification is written as a leaf naming what was verified and the outcome
- AND the leaf is covered by an anchored checkpoint like any other leaf

#### Scenario: a verification fails

- WHEN a verification is attempted and does not verify
- THEN the failure is written as a leaf recorded as a failure, never as an absent event
- AND a log that shows no leaf for the attempt is non-conformant with this requirement

#### Scenario: an access attempt is refused

- WHEN an access request is refused by the permissioned plane
- THEN the refused attempt is written as a leaf
- AND the leaf records the refusal without recording the material that was not disclosed

#### Scenario: a realization logs only successful writes

- WHEN an evidence plane records produced material and no verification or attempt events
- THEN it is REFUSED as non-conformant, naming this requirement
- AND the absence is not read as an implementation detail, because the missing events are the ones an attacker generates

#### Scenario: attempt rows are proposed for direct anchoring

- WHEN a realization proposes anchoring each attempt event directly to a public chain
- THEN it is REFUSED, because a per-attempt public trail leaks by metadata what the payload rules keep off chain
- AND batched checkpoints over the attempt leaves are anchored instead

### Requirement: The record and demographic planes are analyzable without the identity plane

openxFactory SHALL separate the planes so that analysis across the RECORD plane
and the DEMOGRAPHIC plane is possible WITHOUT the IDENTITY plane, BY
CONSTRUCTION rather than by policy. A record-plane entry and a demographic-plane
entry SHALL carry no identifier that resolves a person, and the linkage that
joins either to a person SHALL exist only inside the governed permissioned
identity plane. Analysis over the first two planes therefore exposes no personal
identifiers because there are none to expose, not because a query was written
carefully.

**THE CROSS-PLANE JOIN KEY IS THE DEFECT THIS REQUIREMENT CLOSES, AND IT IS A
CORRECTION TO THE SOURCE SKETCH RATHER THAN A RESTATEMENT OF IT.** The vendored
MedxChain notes segregate three databases but carry ONE shared record digest
across all three, which makes that digest a join key: anyone holding a
demographic row and an identity row can link them without either plane's
permission. So the per-plane key SHALL be derived under that plane's OWN salt,
and the anchored commitment — derived under the record's salt, held in the
governed layer — SHALL NOT function as a cross-plane join key. The segregation is
only structural if the keys are.

**AND THE LANE IS A NAMED CONSUMER RATHER THAN AN EMERGENT PROPERTY.**
Meta-analysis across the record and demographic planes is a first-class use case
of this capability, carried from the MedxChain notes' appendix, which observes
that the neutral family's tranche-three text does not yet name this consumer
though the anchored, segregated design already supports it.

#### Scenario: an analysis runs across the record and demographic planes

- WHEN an analysis queries the record and demographic planes without the identity plane
- THEN it runs, and no personal identifier is exposed because neither plane carries one
- AND the result is unaffected by whether the identity plane was reachable

#### Scenario: a demographic-plane entry carries a direct identifier

- WHEN an entry in the demographic plane carries an identifier that resolves a person
- THEN it is REFUSED by a named check
- AND the refusal is structural, on the identifier's declared resolution rather than on its apparent content

#### Scenario: one key is shared across planes for convenience

- WHEN a realization uses one derived key across the record, demographic and identity planes so the planes can be joined easily
- THEN it is REFUSED, because a shared key makes the segregation nominal
- AND per-plane keys derived under per-plane salts are used instead

#### Scenario: re-identification is attempted through the anchored commitment

- WHEN a holder of an anchored commitment attempts to use it to join a demographic entry to an identity entry
- THEN the join fails, because the anchored commitment is derived under the record's own salt held in the governed layer
- AND no plane's key is derivable from the anchored value

### Requirement: This capability is neutral and names no domain semantics

openxFactory SHALL keep this capability DOMAIN-NEUTRAL, and SHALL NOT define,
name or encode any domain's record kinds, regulators, clinical or financial
semantics, or product surfaces in its contracts, schemas, field names or finding
codes. Domain products instantiate the capability through DIGEST-PINNED domain
overlays owned by their own repositories, on the pattern the estate already runs
for the omnigent family. A capability that fit one domain would belong in that
domain's repository, which is the staged topic's own neutrality argument and the
reason the two domain mappings are stated as a proof rather than as consumers
under obligation.

**THE MAPPING IS NAMED HERE AND AUTHORED ELSEWHERE.** MedxChain and HealthLinc
are MedxFactory's instantiations of this capability; LedgerLinc is
LedgerxFactory's. The vendored MedxChain notes read as an early, domain-specific
sketch of this same shape, predating the neutral family by eighteen months. This
capability names those instantiations to show the shape occurs twice; it authors
no content for any of them, and no domain is obliged to adopt a chain.

**THE STRUCTURAL REFUSALS ARE WHAT MAKES NEUTRALITY AFFORDABLE.** Because the
payload refusal and the identifier refusal above are shape-based rather than
semantic, this capability enforces the regulated-content boundary without
carrying a single domain term in its checks. A domain overlay MAY add stricter
domain-specific refusals on top; it SHALL NOT relax a refusal made here.

#### Scenario: a domain record kind is proposed for this capability

- WHEN a domain-specific record kind is proposed as a contract of this capability
- THEN it is REFUSED, and it lands in that domain's digest-pinned overlay instead
- AND the neutral capability gains no field, code or vocabulary naming the domain

#### Scenario: a domain overlay adopts the capability

- WHEN a domain repository pins this capability by commit and per-file digest and adds its own record kinds on top
- THEN the overlay is conformant, and the neutral contracts are unchanged by the adoption
- AND the domain's own regulator and semantics live entirely in the overlay

#### Scenario: an overlay relaxes a neutral refusal

- WHEN a domain overlay admits a record the neutral validator refuses
- THEN the overlay is non-conformant, because an overlay may add refusals and never remove them
- AND the neutral refusal is what the pin is for

#### Scenario: a domain is asked to adopt the chain

- WHEN a domain repository declines to instantiate this capability
- THEN nothing in this capability obliges it, and no existing capability of that domain is made non-conformant
- AND the two named mappings remain a neutrality proof rather than an obligation
