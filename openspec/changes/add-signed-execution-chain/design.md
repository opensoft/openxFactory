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

## D5 — Tier 1 narrowed to RATIFYING authority — RAISED HERE, RULED BY BRETT HEAP

**Status: RULED 2026-08-29 by Brett Heap, in session.** This decision was
authored as a flagged narrowing and is no longer one. He ruled that **tier 1 is
RATIFYING authority**: agent-held REVIEW wallets stay lawful, and what a chain
refuses is an agent-held wallet performing the RATIFYING act. The requirement's
grounding cites his ruling; this design note keeps the reasoning that was put to
him, so the ruling can be read against what it decided.

**The sitting did not reach it.** The 2026-08-29 clarify sitting took the seven
questions and nothing else — `#499` touches neither the tier model nor either
narrowing — so this went to him separately and was ruled separately. Recording
that distinction matters: a reader who saw "ruled 2026-08-29" beside the seven
dispositions would otherwise conclude the sitting covered it.

**Decision.** Requirement 8 governs the authority that INCEPTS a chain, not
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

**Why it needed a ruling anyway, given that the custody rule already settles
it.** Because the custody rule settles what the wallet CAN carry, not what the
topic's sentence SAYS. The sentence as written refuses the artifact, and a
packet that narrows a topic's text on its own authority — even correctly — is
doing the quiet-narrowing thing this family refuses. So it was raised rather
than assumed, and it stands now on his word rather than on this document's.

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
first one is the strongest possible way to honour it.

**The reading is now the RULING's, and the flag is gone.** Q1 was ruled AS
RECOMMENDED on 2026-08-29 and its disposition says in terms that "no new
artifact is created for it" — which is this reading in the ruling's own words.
Narrowing B therefore needed no separate act and got none. The flag came out of
the requirement at the same commit that encoded the ruling: a flag left standing
after its question is ruled is a stale contested marker, and doc-health's
contested-finding rule is what makes that a defect rather than untidiness.

## D7 — Five corrections the review rounds forced, recorded as corrections

All five came from the bot bench on this packet's own pull request (PR #495,
`chatgpt-codex-connector`, all rated P1, all real). They are recorded here
rather than silently patched, because each one is a case of a rule naming
something it could not actually do — the family's most-repeated defect shape.

**AND THE SECOND ROUND FALSIFIED THE FIRST ROUND'S FIX, TWICE.** D7.1 and D7.2
below each carry a second correction on top of the first, because the repairs
reached for machinery that does not exist: one equated an enum selector with a
digest value, the other gave a signing duty to a link the authoritative table
gives no signer. That is the same defect shape recurring INSIDE its own repair,
which is worth naming — a fix authored against the vocabulary one remembers
rather than the vocabulary one re-reads will reproduce the defect it is fixing.

**D7.1 — A reference is not a binding.** Requirement 1 originally had the
ratification record REFERENCE the exercise by identifier. The shipped
`xfactory_wallet_grant_exercise` records `signed_over` as `request` or
`request_digest`, makes `object_ref` OPTIONAL, and carries no required digest of
the thing approved — so **a previously successful exercise could be REPLAYED as
the proof for a different ratification** and satisfy every check as written. The
human would have signed something else. **The requirement binds in the shape
D7.1b arrives at, and this sentence states THAT shape rather than the first
repair's**: `object_ref` CARRIES the ratification's content digest — a value, in
the shipped identifier grammar, so the comparison is recomputable — and
`proof_of_possession.signed_over` is the SELECTOR `request_digest`, naming what
the signature covered without holding it. Written the other way round, as this
note first was, it equates an enum selector with a digest value and describes a
comparison no validator can run; the correction is D7.1b's and is stated here so
a reader of D7.1 alone is not handed the defect the section exists to record.
**This is a scope restriction by the
consuming capability, not a schema change** — the same move S2 made when it
required `issued_by` for review-class grants while leaving the shared grant
schema untouched, which is why it costs no bundle edit in openXwallet.

**D7.1b — and the first repair was itself unenforceable.** It said
`proof_of_possession.signed_over` "SHALL be the request digest, which SHALL
equal the ratification's content digest". But `signed_over` is an **enum
selector** whose only values are `request` and `request_digest`; it names WHAT
was signed and holds no digest, and the pinned schema carries no field that does.
A validator had nothing to compare. The repair equated a selector with a value —
the identical defect one level down. The requirement now puts the digest where a
digest can actually live: **`object_ref` carries the ratification's content
digest** in the shipped identifier grammar, which admits it, so the comparison is
recomputable. The step from "the record NAMES this ratification" to "the
SIGNATURE COVERS this ratification" is not closable from the record alone, and
that residual is **raised as an explicit gap** with the durable repair named as
an `opensoft/openXwallet` successor (an additive optional signed-subject-digest
field). Defining that field HERE would be minting the second proof vocabulary
this whole requirement exists to avoid. The staged topic sanctions exactly this:
every link resolves to an existing family OR is raised as an explicit gap.

**D7.2 — The chain identity could not be signed by the act that mints it.** The
binding rule said "every link from inception onward signs over the chain
identity". But the chain identity IS the digest of the signed ratification, and
inception is that same signed act — so the signature input would depend on the
completed signature and **no implementation could construct link 2 at all**. The
rule now starts AFTER inception: inception mints the identity and carries it,
bound to the ratification by BEING it. **The first repair then named the
traveling contract as the next link to sign over a predecessor, and D7.2b below
shows that was wrong too** — link 3 has no signer. The correction is stated
here rather than only below, so a reader who skims headings does not carry away
the intermediate answer as the final one: at tranche one **no** link after
inception signs, and the hash-linked signing rule takes effect at tranche two's
first signed link.

**D7.2b — and "the traveling contract signs" was wrong too, for a reason the
authoritative table states outright.** Link 3 has NO SIGNER: the staged topic's
own table records it as `— (carried)`. Requiring it to sign over inception's
digest invents a signing act and a signer nothing defines, and the ratification's
signature cannot cover an inception record created from it. So at tranche one
there is no link after inception with a signer at all, and **continuity is
established by DERIVATION AND COMPARISON rather than by a third signature**: the
ratification's signature verifies, **the digest of the SIGNED ratification —
recomputed, and taken over the signed bytes rather than over the ratified
subject — equals the chain identity**, the inception leaf commits to that
identity, and the traveling contract's carried identity and carried leaf digest
equal both. The bare phrase "its digest" stood here until the round below caught
what the same looseness had already done in the delta; a note about which digest
is which cannot itself leave the referent to context. That is a complete continuity check over links
1–3 built only from artifacts that exist, and it defeats mix-and-match exactly as
a signature chain would, because artifacts from different executions carry
different chain identities. **The hash-linked SIGNING rule takes effect at the
first link that has a signer of its own — the controller setup attestation, in
tranche two** — and the spec now says so, which is the honest place for a rule
whose machinery arrives with a later tranche. The staged topic's "every link
from enrollment onward" carries BOTH defects and is corrected on both counts, on
exactly the footing its own review round corrected "link 8 walks all ten".

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

## D7.6 — The harvested digest rule falsified a sentence in the gate, and I did not sweep for it

**Found by Codex as a P1 on `61ab5d84`, and it is the packet's own lesson used
against the packet.** Requirement 4 — harvested from #494 — was extended in this
session with the rule that the ratification's CONTENT digest (over the subject
ratified) and the CHAIN IDENTITY (over the SIGNED ratification) are different
values and MUST NOT be equated. The gate requirement already contained the
sentence *"the ratification's signature verifies and its content digest EQUALS
the chain identity"*, written before that distinction existed. Adding the
distinction **falsified a sentence elsewhere in the same delta**, and the
addition shipped without the sweep.

**The consequence was not cosmetic.** As written the gate rule *"rejects every
conforming chain"* — Codex's words, and correct: the signed bytes are a strict
SUPERSET of the ratified subject, since they also carry the exercise reference
and the per-act value, so the two digests can never be equal for a conforming
record. A realization building to that sentence would have produced a gate that
refuses everything, and the delta would have contained both the rule and its
contradiction with no test able to see the conflict.

**The rule is now stated as five ordered checks over NAMED digest subjects**,
with the identity check recomputing the digest of the SIGNED ratification and
the `object_ref` comparison kept separate as the REPLAY check over the CONTENT
digest — two comparisons over two subjects, and a sentence forbidding their
collapse in either direction. A scenario refuses a gate that implements the
identity check with the content digest.

**The lesson is one this family already wrote down and this session still
missed:** *when a definition gains a conjunct, sweep every one-conjunct sentence
immediately.* Requirement 4's distinction WAS the new conjunct. The sweep is now
done and recorded — every "content digest" occurrence in the packet was checked,
and one further ambiguity was repaired in D7.2b, where a bare "its digest"
left the referent to context in the very note explaining which digest is which.

**Copilot's finding in the same round was the same shape one level up.** D7.2
said the traveling contract *"is the first link with a predecessor to sign
over"* while D7.2b immediately below establishes that link 3 has no signer — so
a reader skimming headings carried away the intermediate repair as the final
answer. D7.2 now names its own supersession in place.

## D7.7 — The gate enumerated its checks "exactly" and left the harvested actor binding out of the list

**Found by Codex as a P1 on `a576f774`, one round after D7.6, and it is the SAME
failure a second time.** D7.6's fix rewrote the gate rule as five ordered checks
over named digest subjects. Requirement 2 — the actor-to-wallet binding
harvested from #494 — was not among them, and the rewritten rule says the gate
validates **exactly** those checks.

**So the harvested requirement was inert at the only place that runs.** Codex's
case is airtight: Alice signs a ratification whose actor field names Bob, and
all five checks pass — the signature verifies, both digests agree, the inception
leaf commits, the traveling contract matches — because every one of them tests
whether ONE CHAIN IS INTERNALLY CONSISTENT, and none tests WHOSE IT IS. The
chain would carry authority its signer never exercised, through the terminal
act, with the requirement forbidding exactly that sitting four requirements
above and never consulted.

The gate now walks **six** checks, with the sixth stated as non-optional and its
independence argued rather than asserted: structural consistency and correct
attribution are different properties, and no amount of the first establishes the
second. A scenario refuses a chain that passes all five structural checks and
fails the binding.

**The lesson is D7.6's, and the repetition is the finding.** D7.6 recorded that
adding a rule without sweeping for what it falsifies is more dangerous than not
having the rule, because the packet then *reads* as though it is covered. D7.7
is the mirror image: **writing an EXHAUSTIVE list is itself a definition gaining
a conjunct** — the word "exactly" converts every requirement absent from the
list into a requirement the gate does not enforce. The sweep owed after
enumerating a closed list is a pass over every requirement asking *is this one
in the list, and should it be?* That pass was not run. It has been now, and
requirement 9's named-reader rule is the reason it matters: a requirement no
reader walks confers nothing, which this capability states about itself.

**The P2 in the same round is a smaller instance of the same class.** `tasks.md`
still claimed 40 scenarios after README and `proposal.md` moved to 41, because
the count claim is LINE-WRAPPED there and a single-line `sed` could not see it.
A count restated in three places is one invariant; a check that assumes one
spelling verifies two of the three and reports success. The count is now
verified with a whitespace-normalizing pass over all three files rather than a
literal match, which is why this round's move to 42 landed in all three.

## D8 — Four hardenings HARVESTED from the closed #494, cited to their source

**Decision.** Four requirements or requirement-parts in this delta did not
originate here. They come from **pull request #494**, the parallel tranche-one
packet that Brett Heap closed on 2026-08-29 when he ruled the collapse, and they
are cited rather than absorbed so that four Codex rounds of adversarial work are
provably carried rather than quietly re-derived.

**Why cite at all.** A harvested rule with no provenance reads as this session's
insight, and the next author who wants to weaken it has no idea what it cost to
find. Each of these four was a **live defect in a packet that had already passed
several review rounds** — which is the argument for keeping them, stated better
than any reasoning this document could supply.

| # | What #494's bench found | Where it lands here |
| --- | --- | --- |
| 1 | **The actor a chain records was unbound to the wallet that signed.** A link could reference Alice's valid exercise and record Bob's well-formed opaque subject with every enumerated check passing — the exercise proves who SIGNED, and nothing tied that to whom the act is RECORDED AS | Requirement 2, four scenarios |
| 2 | **Naming a per-act value does not make it unique.** #494's own earlier fix named the exercise identifier as the value that makes re-ratification produce a new chain; the round after it showed the pinned schema constrains no reuse, so a producer reusing one reproduces identical bytes and the collision returns | Requirement 3, two scenarios |
| 3 | **A second digest with no construction rule.** #494 declared one construction for the chain identity and left the predecessor digest with none — the same defect twice — and unified rather than adding a second rule | Requirement 4 |
| 4 | **A validator in no required check enforces nothing.** `review-authority-intake` already ratifies that a grant with no reader in a required check confers nothing; #494 carried it explicitly because a rule relied on by implication is a rule nobody checks | Requirement 9 |

**The binding DIRECTION in item 1 is taken from the pinned contract, not from
the finding's wording, and that is worth recording.** #494's Codex round asked
that the actor "resolve through the wallet subject attestation to the exercise
holder". The pinned `openxwallet-subject-attestation` closes
`resolution.resolved_by` to `subject_ref` **precisely so that a record cannot
declare it resolves a subject through a wallet** — the ratified rule that a
wallet identifier never becomes a subject identifier. So the finding named a real
defect and its suggested repair would have inverted the direction the consumed
contract allows. Requirement 2 checks the wallet reference as an ATTESTATION and
never uses it to resolve who the actor is. **A finding can be right about the
hole and wrong about the patch**, and the consumed contract is what decides.

**One #494 requirement was deliberately NOT harvested.** Its rule that every link
after genesis signs the chain identity and its predecessor's digest cannot be
performed on any link this tranche defines: D7.2 establishes that inception
cannot sign over an identity derived from its own signature, and that link 3 has
no signer at all. Importing it would have put a rule in force that no tranche-one
link can satisfy — the "a rule that names a link it cannot apply to" defect this
packet corrected once already. The hash-linked SIGNING rule stays declared at
tranche two's first signed link, and tranche one's continuity is derivation and
comparison.

## What tranche one DELIBERATELY DEFERS, and where each lands

Recorded so that nothing here is mistaken for silence.

| Deferred | Why it cannot land here | Where it lands |
| --- | --- | --- |
| **Q7 — where an attestation signature physically happens** | It decides what an attestation PROVES about a runner, and this tranche mints no attestation identity at all | Tranche two's contract text. **RULED 2026-08-29** — remote signing served by the harness controller, the runner's signing request recorded beside the signature, the controller corroborating against its own link-4 setup attestation. The gate is OPEN; the mechanism is drafted there and is named nowhere here |
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
