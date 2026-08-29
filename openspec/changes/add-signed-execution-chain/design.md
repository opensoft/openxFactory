# Design: add-signed-execution-chain (tranche one)

Only decisions that are REAL decisions are recorded here — where a reader would
otherwise reasonably choose differently, or where this change deliberately
departs from the staged topic's own wording. Everything the topic already
settles is consumed by reference rather than re-argued; the topic is the design
authority and this document does not restate it.

## D1 — The act is `chain inception`, not "enrollment"

**Decision.** This capability's link-2 act is named **chain inception**. The
staged topic calls it "ratified ⇒ enrolled"; the rename is deliberate and is
recorded here so the topic's wording and the spec's wording are never read as
two different acts.

**Why the topic's word could not survive contact with this repository.**
`specs/025-openxfactory-review-lane-caller/spec.md` FR-008 already owns
"enrollment" here — *"The caller MUST declare no enrolled candidate class"* —
and its sense is the entry of a candidate class into a `merge-approval-envelope`
for the codexFactory decision core. That is not a nearby sense; it is a
different act with a different owner, a different artifact and a different
refusal. The two would sit on the same pull requests in the same repository one
week apart. `add-worker-enrollment-broker` carries a THIRD sense already, which
is the evidence that the word is loaded rather than free.

**Why not "chain enrollment".** A qualifier does not survive conversation. Six
weeks after ratification a reviewer says "is this change enrolled?" and there is
no way to know which act was meant. The 2026-08-28 seats named second-vocabulary
invention as the live risk precisely because qualified duplicates read as
synonyms in practice.

**Rejected alternatives.** *"Chain registration"* — collides with the
review-authority **register** and its reader, which is a live artifact in the
same tree. *"Chain minting"* — reads as key material. *"Chain opening"* — no
refusal shape (what is a "failed opening"?). **`inception`** appears nowhere in
this repository (grepped 2026-08-29, zero hits outside this packet), it names
the beginning of a chain rather than an administrative entry, and it composes
with the chain identity it mints.

**Where the non-collision is stated.** In requirement text, not only here: the
inception requirement's body carries the bolded distinction and its fourth
scenario exercises it, so a reader who arrives at the promoted spec without this
packet still finds it.

## D2 — Out-of-pipeline is a NECESSITY, not a preference, and it is recorded as such

**Decision.** The chain-inception act is performed OUTSIDE the codexFactory
clearance-envelope pipeline, and the requirement cites the ground rather than
merely asserting the posture.

**The ground.** `opensoft/codexFactory`
`hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`
— unanimous 5/5 refusal, convener disposition §8 (Brett Heap, 2026-08-28). A
class over `openspec/changes/**` **can never commission a council**: the surface
is inside the canonical `GATE_INTEGRITY_FLOOR`, the PR-time floor is evaluated
before any clearable classification, every candidate parks
`parked_never_clearable`, and the convening lane bails on exactly that outcome.
Measured on openxFactory's real tree: **984 admitted, 984 floored, 0 remaining**.
Reproduced **code-level**: `gate_integrity` declared, `gate_integrity` absent,
and no rule document at all all park identically, reasons byte-identical.

**Why the citation is load-bearing rather than decorative.** Without it, a later
implementer reads "out-of-pipeline" as a temporary posture and tries to route
inception through the envelope once a class exists. It would fail for a reason
no rule document can fix — and the failure mode is a control that is described
and does not run, which is LS-A3, the failure this family has now named three
times. The requirement carries the measurement so the impossibility is on the
face of the spec.

**What this does NOT do.** It does not amend FR-008, define a candidate class,
create an envelope, touch a ruleset, or discharge `add-substantive-review-lane`
task 3.2 — all of which the convening left exactly where they are.

## D3 — Link 7 lands on the §7.4 path, in short-chain form

**Decision.** Council review of the signed brief (link 7) is expressed at this
tranche as a signed review OF THE TRAVELING CONTRACT on the
council-reviewed-but-human-approved path, and NOT as a clearance-envelope
entry.

**Why.** The convener's ruled continuation is that path, which *"per the
2026-08-26 record §7.4 needs no class and no flip"* and *"reaches this
repository without an envelope and without amending FR-008"*. Composing link 7
with the envelope would require the very thing constraint D2 proves cannot
exist here.

**Scope honesty.** Link 7's FULL form — the council reviewing the chain-carrying
artifact rather than a summary of it, with seat signatures as a link the gate
walks — is not realized by this tranche. What tranche one owes is that the
traveling contract is the reviewable artifact, and that the gate's scope is
links 1–3. Adding seat signatures to the walked chain is tranche-two work and is
named as such.

## D4 — The log comes BEFORE the anchors, and the topic says so

**Decision.** The signed transparency log is a tranche-ONE artifact.

**Why, in the topic's own words.** *"The evidence plane of claim 6 — the signed
transparency log — is a **tranche 1** artifact, not a tranche 3 one. The log is
the record; the anchors are late additions to it. Building the log last would
mean tranches 1 and 2 had nowhere to write their signed leaves."* The exit path
lists tranche one as "links 1–3", and read alone that would exclude the log; the
sequencing note is the same document correcting the same document, and the
correction governs. This is recorded rather than assumed because a reader who
stops at the tranche list will think the log was smuggled in.

**The consequence stated in requirement text.** Because the log ships without
anchors, the spec says the absence of an anchor is NOT a defect. Otherwise the
first honest implementer reads "the log makes the record undeniable" and
concludes something is missing — or worse, invents an anchor format that tranche
three then has to displace, which is the one-way door the topic's multi-anchor
receipt exists to avoid.

## D5 — Tier 1 narrowed to RATIFYING authority, against a realized artifact

**Decision.** Requirement 6 governs the authority that INCEPTS a chain, not
every authority credential in the family.

**Why the narrowing is forced.** The topic says tier-1 authority credentials are
"never held by an agent, a runner, or a lane". `wal-agent-mrc-0001` is a
realized wallet whose holder is `agent:merge-readiness-council`, backing an
active `review`-act grant that the required `wallet-validation` check reads on
every pull request. Read literally, the topic refuses an artifact this
repository runs today. A staged topic does not override a realized one.

**Why the narrowing is principled rather than convenient.** The wallet's custody
model is `holder_readable`, and `add-trust-anchor`'s ratified rule is that
declared custody bounds what a signature EVIDENCES: a key readable by the host
that uses it evidences that the HOST acted. A ratification must evidence that a
named human acted, so `holder_readable` custody cannot carry a ratifying grant —
by the custody rule, before any tier vocabulary is invoked. The tier boundary
and the custody boundary agree; the narrowing just says which one is doing the
work.

**Flagged.** The narrowing is a reading of the topic against a ratified
artifact, so it goes to the clarify round with Q1 rather than standing on this
document's own authority.

## D6 — Q1's "no new artifact" is read as "invent no new artifact"

**Decision.** The presentation is recorded by REFERENCE to an
`xfactory_wallet_grant_exercise`, which the ratification record names by
identifier.

**Why.** Q1's recommended answer says to record the presentation "in the
ratification record rather than a new artifact". Taken at the letter, that
forbids using a record kind the family already ships — and the shipped kind is
purpose-built for exactly this: `proof_of_possession` with `presented`,
`verified`, `signed_over` and `presenting_key_ref`; `event_class` separating
`verification_failure` from `unauthenticated_request`; and a closed refusal
enumeration that already distinguishes `missing_proof_of_possession` from
`missing_grant` because *"the grant was supplied and is not what was lacking"*.
Q1's intent is plainly to prevent a SECOND proof vocabulary, and referencing the
first one is the strongest possible way to honour it. **The reading is flagged
in the requirement**, because a reading of an unruled recommendation is not a
ruling.

## What tranche one DELIBERATELY DEFERS, and where each lands

Recorded so that nothing here is mistaken for silence.

| Deferred | Why it cannot land here | Where it lands |
| --- | --- | --- |
| **Q7 — where an attestation signature physically happens** | It decides what an attestation PROVES about a runner, and this tranche mints no attestation identity at all | Tranche two's contract text; the question is answered in the clarify round, the mechanism is drafted there |
| **The remediation exemption's full form** | It is an exemption on link 10's CLOSURE invariant — an unclosed chain refuses every consumer except a chain whose declared, signed subject is that failure. Link 10 does not exist at this tranche, so the exemption has nothing to except and drafting it here would be drafting a rule against a state the system cannot enter | Tranche two, alongside link 10; the shape is already argued in the staged topic and is carried, not re-derived |
| **The controller-does-not-notarize-self-report rule** | It binds link 5's claims against link 4's setup attestation; both are tranche two | Tranche two |
| **The on-chain boundary, the salted keyed commitment, the multi-anchor receipt** | Gated on rulings for Q3 and Q6, and on the PKI plane being real | Tranche three |
| **Link 7's seat signatures as a walked link** | The gate's scope at this tranche is links 1–3 by the topic's own instruction | Tranche two |
| **Domain realizations (HealthLinc, LedgerLinc)** | They are MedxFactory's and LedgerxFactory's, not openxFactory's; the neutral family is what this change owns | Domain repositories, consuming the released bundle |

## What this design does NOT decide

- **No storage mechanism for the log** beyond append-only and signed. The
  register precedent (a repository-tracked file whose READER is the shape) is
  available to the realization and is not mandated here.
- **No signature algorithm.** The shipped exercise vocabulary already
  enumerates `ed25519`, `ecdsa-p256` and `ecdsa-secp256k1`; picking one is
  realization work bounded by that enumeration.
- **No ruleset change.** Making the gate a REQUIRED check is an operator act
  with its own evidence obligation, on the shape `wallet-validation` already
  proved — a merged workflow file is not evidence.
