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
refusal shape (what is a "failed opening"?). **`inception`** appeared nowhere in
this repository BEFORE this change — grepped 2026-08-29 against `origin/main` at
`3ffd6a8f`, zero hits — it names the beginning of a chain rather than an
administrative entry, and it composes with the chain identity it mints. (The
tense is exact because the first draft's "appears nowhere … outside this packet"
was already false of this change's own README and `INDEX.md` edits, which a
review round caught. The evidence is kept rather than deleted: it is the reason
the word was chosen, and deleting evidence to repair a tense would be the wrong
repair.)

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

**The measurement is not the whole ground, and the requirement says so.** The
984/984/0 figure covers the surface this repository's ratifications actually land
on. If it were the ONLY ground, a later implementer could argue that inception
of a chain over some other surface may route through the pipeline once a class
exists there. It may not, for a reason independent of any floor: **a pipeline
that CLEARS candidates cannot also be what CONFERS the authority those
candidates are cleared against.** A chain whose first link is minted by the
mechanism it exists to permit is circular on any surface. The measurement makes
the rule unarguable here; the circularity makes it correct everywhere.

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

## D7 — Three corrections the first review round forced, recorded as corrections

All three came from the bot bench on this packet's own pull request (PR #495,
`chatgpt-codex-connector`, all rated P1, all real). They are recorded here
rather than silently patched, because each one is a case of a rule naming
something it could not actually do — the family's most-repeated defect shape.

**D7.1 — A reference is not a binding.** Requirement 1 originally had the
ratification record REFERENCE the exercise by identifier. The shipped
`xfactory_wallet_grant_exercise` records `signed_over` as `request` or
`request_digest`, makes `object_ref` OPTIONAL, and carries no required digest of
the thing approved — so **a previously successful exercise could be REPLAYED as
the proof for a different ratification** and satisfy every check as written. The
human would have signed something else. The requirement now binds: `object_ref`
names this ratification, `signed_over` is the request digest, and that digest
EQUALS the ratification's content digest. **This is a scope restriction by the
consuming capability, not a schema change** — the same move S2 made when it
required `issued_by` for review-class grants while leaving the shared grant
schema untouched, which is why it costs no bundle edit in openXwallet.

**D7.2 — The chain identity could not be signed by the act that mints it.** The
binding rule said "every link from inception onward signs over the chain
identity". But the chain identity IS the digest of the signed ratification, and
inception is that same signed act — so the signature input would depend on the
completed signature and **no implementation could construct link 2 at all**. The
rule now starts AFTER inception: inception mints the identity and carries it,
bound to the ratification by BEING it; the traveling contract is the first link
with a predecessor to sign over. The staged topic's "every link from enrollment
onward" carries the same defect and is corrected in the spec text, on exactly
the footing its own review round corrected "link 8 walks all ten".

**D7.3 — Deletion detection was promised at a strength the tranche cannot
deliver.** "The log's hash structure is what makes an alteration detectable" is
true for a prefix someone has observed and FALSE for suffix truncation nobody
has: a store that drops its newest leaves and presents an earlier valid signed
tree head shows a shorter log that verifies perfectly to a fresh reader. With
anchors deferred to tranche three, the unconditional guarantee was not
implementable — and an unimplementable guarantee on the PRIMARY RECORD is the
worst place in this design to have one. The requirement now states the guarantee
at its real strength, names the two things that do reach at this tranche
(consistency proofs against an observed head, and the traveling contract's
carried leaf digest catching truncation at the point of use), and DECLARES the
residual under the realization-conformance obligation. That is `add-trust-anchor`'s
ratified rule applied to ourselves: an undeclared shortfall is non-conformance,
the identical shortfall declared is conformant.

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
