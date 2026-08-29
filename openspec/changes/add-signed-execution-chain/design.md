# Design: add-signed-execution-chain (tranche one)

Companion to `proposal.md`. The proposal argues the doctrine and names the
build; this document records the DECISIONS, the mechanism the atomicity claim
actually rests on, the failure semantics both ways, what is deliberately
deferred, and the check that tranche one does not depend on Q6 or Q7.

## Context

Three facts set this design's shape.

**One.** The staged topic's doctrine was hardened across five Codex bench rounds
on pull request #452 and is treated here as settled, not reopened: per-task keys
never enter workers; bind-before-sign; two enforcement horizons (link 8 walks
links 1–7 pre-merge, links 9–10 enforce at closure); a chain is hash-linked
rather than a bag of signatures; and the remediation chain is the one exempt
consumer of an unclosed chain. Only the second and fourth of those five bear on
tranche one. The other three are tranche-two-and-later doctrine, carried forward
unchanged and not restated as requirements here.

**Two.** Three of the four neighbouring changes already own an identity,
certificate or custody vocabulary, and the staged topic names inventing a second
one as this family's live collision risk. That risk is answered structurally
(R8) rather than by good intentions.

**Three.** This family's recurring defect — measured repeatedly across the
corpus, most sharply in `add-wallet-carried-review-authority`'s own design — is
text that outruns its machinery: a control described as though the description
were the enforcement. R10 exists so this packet cannot commit it.

## Decisions

### D1 — Tranche one is links 1–3, plus exactly the two rules those links need to be statable

**Decision.** In: links 1 (ratify with a wallet-carried authority), 2 (ratified
⇒ chain-enrolled, atomically, inside the one signed handshake) and 3 (the
traveling contract). Plus the hash-linking rule (R4) and the evidence plane
(R7). Out: everything else.

**Why R4 is in, stated exactly rather than flatteringly.** R4 governs no link
that tranche one alone creates: links 1 and 2 share ONE signature (the topic's
own table says link 2 is signed by "same signature as link 1"), so the genesis
link is links 1-and-2 together, and link 3 is CARRIED rather than signed. **R4
first bites in tranche two.** It is in scope anyway for two reasons. First, R3's
chain identity is otherwise an identifier that nothing consumes — a value defined
with no rule about what may be done with it, which is how identifiers acquire
incompatible uses. Second, the topic's binding rule is a property of the chain's
SHAPE, not of any one link: "every link from enrollment onward signs over … the
chain identity … and the digest of the link that precedes it". Fixing the shape
at the root is what lets tranche two extend a chain rather than renegotiate one,
and the topic's own mix-and-match finding — individually valid artifacts from
DIFFERENT executions assembling into one apparent chain — is what happens when
the binding is designed after the links exist.

**Why R7 is in.** The staged topic's own sequencing note settles it: the signed
transparency log is a tranche-1 artifact, "not a tranche 3 one … Building the log
last would mean tranches 1 and 2 had nowhere to write their signed leaves."
Enrollment is a write; a write needs a target.

**Why the merge gate is out**, despite the topic's argument that the gate should
exist from tranche one validating a short chain. Two independent reasons, and
either alone is sufficient. (a) A gate over `openspec/changes/**` is the
never-convenable object the 2026-08-28 council record refuses at §2 and Brett
ruled refused at §8.2 — the packet must not create the exact vehicle that was
just refused. (b) R10 forbids stating an enforcement point that does not exist.
What the topic's intent DOES get is R6: the refusal semantics are specified from
the start, so the refusal path is defined before it is first needed rather than
first designed when it matters most.

### D2 — The act is always spelled CHAIN ENROLLMENT, never bare "enrollment"

**Decision.** Every occurrence in requirement text is "chain enrollment" or
"enrolled in a signed execution chain". Bare "enrollment" is not used.

**Why.** The active change `add-worker-enrollment-broker` owns "enrollment" for a
WORKER joining a fleet — enrollment requests, enrollment grants, leases, an
enrollment policy and an enrollment audit record, with a whole
`contracts/worker-enrollment/` family behind it. Two different acts over two
different subjects sharing one unqualified noun is the "two records of one
decision" defect arriving as vocabulary. Qualifying the term costs one word per
occurrence; the alternative is a reader who has to guess which enrollment a
sentence means. This is also why the packet does not name its change id or its
capability after the word.

### D3 — Link 1 is an EXERCISE of a grant, not a presentation of a wallet

**Decision.** R1 requires the ratification to be recorded as an exercise whose
proof of possession was presented AND verified, whose `event_class` is
`authenticated`, and whose attribution mode is `key_attributed`.

**Why, and this is a correction to the staged topic's own shorthand.** The topic
says the ratifier "presents a wallet". openXwallet's ratified requirement is
titled *"Use requires proof of possession, not presentation"* and rules that "no
authority is conferred by presentation alone", with the refusal naming the
missing PROOF rather than the missing grant, because the grant was supplied and
is not what was lacking. A requirement written on the topic's shorthand would
have contradicted pinned ratified text on its first line. The topic's own Q1
anticipates this and recommends exactly this resolution — express presentation in
the existing grant vocabulary plus a proof-of-possession step, recorded in the
ratification record rather than in a new artifact.

**The three-way distinction is carried whole, not collapsed.** The ratified text
distinguishes `authenticated`, `verification_failure` (a signature was presented
and did not verify) and `unauthenticated_request` (none was presented), and says
in as many words that the two failures "describe different events". R1's
scenarios keep all three apart. Collapsing them into "unsigned" would be a
one-conjunct restatement of a two-conjunct rule.

### D4 — The chain link is a NEW record that REFERENCES an exercise; the wallet schema is not extended

**Decision.** One new record kind, `xfactory_execution_chain_link`, in a new
`contracts/signed-execution-chain/` family. It names the exercise it descends
from by `exercise_id`. No field is added to any openXwallet schema.

**Why it could not be otherwise, verified rather than assumed.**
`contracts/openxwallet/openxwallet-grant-exercise.schema.yaml` declares
`additionalProperties: false` and carries no field capable of naming a chain, and
that file is not openxFactory's to edit: the wallet family was carved out at
`contract-v2.0` and is consumed here at `wallet-v1.3` through
`contracts/openxwallet-pin.yaml`, which pins the schema by commit AND sha256. An
"additive optional field" on it is a change in `opensoft/openXwallet` followed by
a pin bump here, under the `neutral-product-pin` seam — not something a tranche of
this packet can perform.

**Why that is the right answer and not merely the available one.** The two
records answer different questions and have different owners. The exercise record
answers *was this act authorized and by whom*; the chain link answers *what does
this act begin, and what descends from it*. Putting the second inside the first
would make the wallet family a prerequisite for reconstructing a chain, which the
ratified requirement *"The capability is an authority control, never an identity
substrate"* refuses in its own domain and which would be the same mistake here.

**Recorded as a dependency, not a gap being smoothed:** if a later tranche needs
an exercise record to name its own chain, that is a publisher-side change plus a
pin bump, and this packet says so rather than minting a second exercise record.

### D5 — The unwalleted root ratifier, which is a live collision and is resolved by declaration

**The collision.** The staged topic's link 1 has "the ratifying human presents a
wallet-carried authority". But `review-authority-intake`'s ratified requirement
*"Every review-authority grant names its issuer, and a root grant's issuer is
anchored outside the register"* rules that the root issuer of review authority in
this family is the responsible operator, "whose authority is standing under the
Human Escalation Contract … and therefore **requires no wallet and no grant of
its own**." Today's ratifier IS that operator. A requirement demanding a wallet
signature from him would contradict ratified text on day one — and the topic's
own conflicts section says that where the two disagree, the ratified text wins.

**Decision, and it is the SECOND answer to this collision — the first was wrong
and Codex caught it.** That ratifier begins NO signed execution chain. The case
is recorded as a DECLARED GAP naming the instrument it lacks, and this capability
defines no origin, tier, mode or exemption under which a chain begins without a
verified signature.

**What the first answer was, and why it could not stand.** The packet as first
pushed had a chain DECLARE its origin — `wallet_exercise` or
`standing_authority` — and forbade a standing-authority chain being accepted for
a signature-rooted assurance. That was modelled on `add-trust-anchor`'s ratified
custody rule, where an undeclared custody evidences "the weakest member of the
defined set". **The analogy does not carry, and the reason is structural rather
than stylistic.** A host-held key is still a key: it produces a signature, and
the custody declaration bounds what that signature EVIDENCES. A standing
authority with no wallet produces no signature at all — so there are no signed
bytes for R3's chain identity to be the digest of, and no predecessor for R4's
successor binding to cover. The branch was therefore admitting an object that
could not satisfy R2, R3 or R4: a permitted origin whose chains are unconformant
by construction. Codex raised exactly that on PR #494 and it is right.

**Why the gap and not a weaker chain.** An object called a chain that carries no
signature would be accepted wherever a chain is required — the substitution this
whole capability exists to prevent. A declared gap is visible and has a named
remedy; a weaker chain sitting beside the real one is neither. This is the shape
`add-trust-anchor` ratified for obligations rather than for custody: *"A
realization declares the obligations it cannot meet."*

**The consequence, accepted plainly.** Until the root issuer holds a wallet,
this capability governs that ratifier's acts NOT AT ALL rather than governing
them weakly, and realization owes the wallet. That dependency is real and already
booked: `add-wallet-carried-review-authority`'s own build plan carries "the first
wallet: one holder, `holder_readable`, with its custody attestation row" as
openxFactory S-work.

**One lesson recorded, because it is the second appearance of a pattern this
corpus has met before.** This session's own first-pass correction had patched the
branch by forbidding a SELF-ASSERTED standing-authority origin — a real hole,
patched at the point it showed. The right move was to remove the branch, which
dissolves the self-assertion hole along with it. Unify on a defect's second
appearance rather than patching it again.

### D6 — The atomicity mechanism: ONE signed object, TWO views — bind before sign

This is the crux, so it is stated mechanically rather than as an aspiration.

**The problem with the naive reading.** "Ratification and chain enrollment are
atomic" cannot mean a distributed transaction across two writes. Two records
written by one process are two writes, and a claim of atomicity over them is a
claim the machinery cannot keep.

**The mechanism.** The handshake produces ONE signed object. The ratifier signs
ONE byte-string that already contains both halves: the ratification's subject and
the declaration that signing it enrolls that subject in a signed execution chain.
Because the enrollment declaration is INSIDE the signed bytes, there is no second
act to keep in step — this is bind-before-sign, applied at the root. The exercise
record and the genesis chain link are two VIEWS of that one signed object, not
two independently produced facts.

**No circularity, stated because a careless reading finds one.** The chain
identity is the digest OF the signed bytes, computed after signing. The signed
bytes contain the enrollment DECLARATION, never the identity derived from them. A
successor link then signs over that identity plus its predecessor's digest, which
is why R4 can bind successors without R3 having to bind itself.

**One ratification therefore yields at most one chain**, and the recording of the
genesis link is idempotent on the chain identity: a second genesis link presented
under an existing chain identity is refused rather than appended, so a retry after
a failed write cannot mint a rival chain.

### D7 — No MODIFIED delta on any existing capability

**Decision.** The packet is ADDED-only.

**The obvious alternative, and why it is rejected.** The natural MODIFIED target
is `document-lifecycle`'s *"Proposal packets carry the lifecycle header"* — bind
every ratified openxFactory proposal to carry a chain. Rejected on three grounds.

1. **It would describe a control that does not exist.** Zero chain links exist,
   zero live wallets exist, and no validator reads either. A MODIFIED requirement
   asserting that every ratified packet carries a chain would be false in the
   present tense the day it promoted — the precise defect `review-authority-intake`
   ratified two requirements to refuse.
2. **It would make a neutral family's rule an openxFactory-shaped rule.** The
   capability has to serve HealthLinc and LedgerLinc, where the ratified object is
   a treatment plan or an analysis plan and there is no `proposal.md` at all. The
   topic's own claim 4 — the two mappings are the same shape — is the argument for
   the neutral home, and writing the rule against one consumer's document format
   would undercut it. A claim true of one caller is a bug in shared text.
3. **The binding has a defined arrival point already.** R10 makes the family
   confer and refuse nothing until a named reader runs as a required check. The
   openxFactory-lifecycle binding is a realization task in this packet's
   `tasks.md`, performed when that reader exists — which is when the statement
   becomes true rather than aspirational.

**Consequence accepted honestly:** until that realization task lands, this packet
adds a capability that governs nothing in this repository's day-to-day flow. That
is the same shape `add-worker-enrollment-broker` and `add-trust-anchor` both took
— neutral contract first, consumers named as successors — and it is preferable to
a promoted requirement that is untrue on its promotion day.

### D8 — The evidence plane is in; anchoring is not, and the log's standing does not depend on any anchor

**Decision.** R7 puts the append-only signed log inside the governed store and
makes it THE record. It says nothing about any external chain, and it states
positively that the log's evidentiary standing does not depend on any anchor.

**Why the positive statement matters rather than mere silence.** The topic's
claim 6 is that a design in which the blockchain IS the record "has confused the
witness for the evidence". Silence would leave a later tranche free to invert
that by adding anchoring and quietly demoting the log. Saying it as a property of
the log makes tranche three additive to it rather than a reinterpretation of it —
and it is also what makes R7 provably independent of Q3 and Q6 (see below).

### D9 — R6 states refusal semantics without creating an enforcement point

**Decision.** R6 binds any consumer that VALIDATES a chain: it validates every
link that exists at that point, refuses on a gap, refuses when it cannot evaluate,
and names which link failed and why. It does not create, name, or require any
particular gate.

**Why both halves.** Without the first half, tranche two would arrive with the
refusal semantics unspecified and would design them under pressure. Without the
second half, the packet would assert an enforcement point over the exact surface
the council record refuses. The distinction is the one the corpus already draws
between what a rule REQUIRES OF a check and where the check runs.

**Fraud signal, not warning, and why the strength is deliberate.** A missing link
means either the act did not happen or something is misrepresenting that it did.
Both are refusals. Downgrading either to a warning would make the record an audit
trail again — writable falsely by the very lane it is supposed to constrain.

### D10 — The out-of-pipeline placement is a requirement, not a rationale

**Decision.** R9 states normatively that the handshake is performed outside the
clearance pipeline and that its record is never presented as a clearance.

**Why it is not left in the "Why" section.** A rationale can be forgotten by the
next author, who will reasonably ask why this is not simply gated — and will find,
as the council did, that the surface can never be classified. Writing it down as a
requirement, with the record cited, means the finding is carried by the corpus
rather than rediscovered. It also states the converse, which is the part that
protects the ratified lane: an out-of-pipeline handshake confers no clearance and
MUST NOT be recorded as one, so this packet cannot become a route around the
substantive review lane.

## Failure semantics — atomic means neither half stands alone

Four cases, stated in both directions, because "atomic" is worth nothing if the
failure paths are unstated.

### Case A — the signature verifies, the chain link cannot be recorded

**The ratification does not stand.** A signed statement whose genesis link is not
in the evidence plane is an unrecorded intent, not a ratification: the
ratification's standing is DERIVED from the link, never stored beside it. An
implementation that writes a "ratified" marker before the link lands has
reintroduced the divergence link 2 exists to make impossible, and R2's scenarios
say so.

**Recovery is re-RECORDING, never re-signing.** The same signed bytes are
presented again; the write is idempotent on the chain identity, so a retry
produces the same chain rather than a second one. If the record cannot be written
at all, the act is refused as a whole and nothing is presented as ratified.

### Case B — a chain link exists whose ratification does not verify, or cannot be resolved

**The chain is broken at its root and is refused.** This is not a repairable half
and is not healed by producing the missing ratification afterwards: a signature
made after the fact, over an object that already claimed to descend from it, is
precisely the fabricated-but-valid-looking record this family exists to refuse.
The remedy is a NEW handshake producing a NEW chain, and the broken one stays
broken on the record.

**The asymmetry between A and B is deliberate and is the design's load-bearing
choice.** A is recoverable because nothing has yet claimed to descend from an
unrecorded root. B is not, because something already has.

### Case C — a link asserting a chain identity its own bytes do not produce

Refused. **The earlier drafting of this case was wrong and is corrected here
rather than quietly replaced.** It said "two genesis links under one chain
identity are refused, not appended" — which cannot happen: the identity IS the
digest of the signed bytes, so different bytes are a different identity, and the
refusal described an impossible input while the reachable attack went unnamed.
The reachable attack is a link that CLAIMS an identity, and the answer is that
every reader COMPUTES the identity and never accepts an asserted one (R3).
One-ratification-one-chain then holds by construction, and R3 says so instead of
posing it as a separate refusal a validator would be expected to enforce
independently. D6's idempotency still does its own job: re-recording the same
signed bytes after a failed write yields the same chain rather than a rival.

### Case D — a successor link that verifies but does not bind

A link whose own signature verifies but that does not cover the chain identity
and its predecessor's digest is refused under R4 even though nothing about it is
cryptographically wrong. This is the mix-and-match case: individually valid
artifacts from different executions must not assemble into one chain. A verifier
that checks signatures without checking binding has verified a bag.

## Proving tranche one is Q6/Q7-independent

Not asserted — checked, and the check is repeatable.

**The claim.** No requirement in this packet changes its meaning under either
answer to Q6 (does "patients put PHI portions on chain" mean commitments?) or Q7
(where does an attestation signature physically happen?).

**Q6.** Q6 is a question about what may be placed on a public chain. Tranche one
places nothing on any chain: it defines no anchor, no commitment, no salt, no
receipt, no consent checkpoint and no payload of any kind. R7 states positively
that the log is the record and that its standing does not depend on any anchor,
so both answers to Q6 land entirely inside tranche three's additive surface. The
strongest form of the check: if Q6 were ruled tomorrow in either direction, not
one word of `specs/signed-execution-chain/spec.md` would need to change.

**Q7.** Q7 is a question about tier 2 — where a per-task ATTESTATION signature is
produced. Tranche one contains no attestation link. Its only signer is a human
holder of a tier-1 authority credential, whose custody is already governed by
openXwallet's ratified *"Custody is declared and bounds what a signature
evidences"*, a tier-1 rule Q7 does not touch. Links 4, 5, 6 and 10 — every link
where a per-task identity appears — are explicitly out of scope.

**The mechanical check, so a reviewer can repeat it.** The tranche-two and
tranche-three vocabulary appears in this packet ONLY inside prose that declares it
out of scope — `proposal.md` § Scope, this document's deferrals, and `tasks.md`'s
reserved rows. None of it appears in the delta itself. Run:

```sh
grep -c -i -E '\b(attestation|runner|harness|controller|per-task|hsm|anchoring|anchored|commitment|salt|salted|phi|receipt)\b' \
  openspec/changes/add-signed-execution-chain/specs/signed-execution-chain/spec.md
# → 0
```

**Two near-misses a looser grep produces, named so a reviewer repeating the check
is not misled by them.** Searching for the bare substrings `on-chain` and `anchor`
DOES match the delta, and both matches are innocent: `on-chain` occurs inside the
capability's own name — "executi**on chain**" — and `anchor` occurs once, inside
the cited capability name `add-trust-anchor` in R8. Neither is a use of the
tranche-three concept. The word-boundary form above is the check that discriminates,
which is why it is the one written down.

## Deliberately deferred

**To tranche two** (`extend-signed-execution-chain-attestation`): links 4, 5, 6
and 10 — the harness-controller setup attestation, the runner attestations, the
signed PR-open decision, and the governed post-merge test that closes a chain.
With them: the two-horizon enforcement model (link 8 walking links 1–7 pre-merge;
links 9–10 enforcing at closure), the unclosed-chain refusal and its ONE exempt
consumer — the remediation chain, without which the invariant deadlocks because a
corrective change is itself a consumer of the merge it repairs — and the
controller's obligation to BIND submitted claims against its own setup attestation
rather than notarize self-report. Gated on Q7, on the omnigent layer enforcing the
precondition, and on `implement-openxpki-install-repo` issuing the controller
certificate.

**To tranche three** (`extend-signed-execution-chain-anchoring`): the public
anchoring layer, the salted keyed commitments, the consent-log checkpoints, the
permissioned consent plane whose state roots are anchored, the chain-agnostic
multi-anchor receipt, and the refusing validator that Q2 recommends for the
boundary. Gated on Q3 and Q6.

**To realization of this packet:** the openxFactory-lifecycle binding (D7), the
validator, and the required check (R10).

**To the domain repositories:** codexFactory's lane, MedxFactory's HealthLinc and
LedgerxFactory's LedgerLinc. "Merge" is domain-interpreted — a git merge, a push
to a patient app or printed signed orders, a publication to a ledger app — and the
neutral family deliberately says nothing about which.

## The topic's other open questions, as the topic leaves them

Carried unchanged. None is decided here.

- **Q1 — wallet-presentation mechanics. OPEN.** Its recommended answer is adopted
  in substance by D3, which is why tranche one specifies WHAT a ratification must
  evidence (a verified proof of possession, key-attributed, revocation checked at
  exercise) and not the ceremony by which a holder presents. The mechanics remain
  the topic's question.
- **Q2 — where exactly is the on-chain boundary. OPEN**, tranche three. Its
  recommended refusing-validator shape is unbuilt and unspecified.
- **Q3 — which chain. OPEN**, research COMPLETE and vendored, awaiting a ruling
  rather than more analysis. Tranche three.
- **Q4 — where do the tranche boundaries fall. OPEN**, and this packet is the
  first evidence on it: its recommended answer is "tranche one = links 1–3 only,
  because they need nothing that does not exist", and D1 records that authoring it
  additionally required R4 and R7 — a refinement of the recommendation, offered to
  the question rather than closing it.
- **Q5 — smart contracts or an L2. OPEN**, direction confirmed by the study, the
  trigger condition for a public programmable layer still unstated. Tranche three.
- **Q6 and Q7 — HELD for Brett's clarify sitting**, per `proposal.md` and the
  independence proof above.

## Self-review pass, recorded rather than folded in silently

Five corrections were made to the delta by this session's own re-reading after
the packet was first pushed. They are listed because corrective text earns the
same scrutiny as original text, and a reader of the diff deserves to know which
parts were second thoughts.

1. **R1 — a standing-authority origin could be self-asserted.** As first drafted,
   any actor could declare the origin that excuses a missing signature, which
   turns a declared gap into a bypass. Patched by requiring the origin be anchored
   outside the record it writes into — and then **SUPERSEDED ENTIRELY** by the
   Codex round, which showed the branch itself could not conform to R2, R3 or R4.
   The branch is gone; see D5. Kept in this list because the patch-then-unify
   sequence is the lesson, not the patch.
2. **R2 — "recovery SHALL NOT be a fresh signature" was too absolute.** A fresh
   signature is lawful; it simply produces a DIFFERENT chain. Corrected to say
   that, rather than forbidding an act the corpus permits.
3. **R3 — the one-ratification-one-chain refusal was vacuous.** See Case C.
4. **R6 — "validate every link that EXISTS" made completeness unfalsifiable.** A
   chain judged against the links it supplied is complete by definition, so a
   lane that simply omitted a link would pass. Corrected: the required set comes
   from the consumer's own DECLARED EXPECTATION, and a consumer holding none
   refuses.
5. **R9 — "by a human authority acting under standing authority" was true of one
   caller only.** R1 admits a wallet-carried holder who is not the root issuer,
   and R9 as drafted would have excluded them. Corrected to bind on the SURFACE
   the handshake writes rather than on the instrument the authority holds.

## The Codex round, and how each finding was taken

Three P1 findings on `a367eaa7`, all real, all taken — one of them narrowed, with
the narrowing argued rather than asserted.

1. **"Define how standing authority signs the handshake." TAKEN IN FULL**, and it
   is the most consequential correction in the packet. See D5: the branch is
   removed and replaced by a declared gap.
2. **"Test enrollment declarations attached after signing." TAKEN IN FULL.** The
   fixture list in tasks 2.2 omitted R2's central case — a chain-enrollment
   declaration recorded outside the signed bytes — and the ratification/genesis
   mismatch beside it. Because task 2.3 requires the validator to reject exactly
   what 2.2 packages, realization could have completed with a validator that
   accepts an unsigned enrollment declaration while every other fixture passed.
   The list is now organized per requirement, the bind-before-sign pair is called
   out as the silent-failure case, and 2.3 gains a test asserting one-to-one
   correspondence between the fixture set and the validator's refusal codes so a
   later-added refusal cannot ship with neither.
3. **"Move selected tranche material into supporting-docs." TAKEN IN A NARROWED
   FORM, and the narrowing is the honest part.** The ratified proposal-gate
   requirement binds "the SELECTED source documents", and nothing here is
   selected: both staged documents are load-bearing for tranches two and three,
   and moving them would strand those tranches. That reading is not this
   packet's invention — three sibling ACTIVE staged-origin changes
   (`add-ideation-intent-plane`, `add-model-capability-vocabulary`,
   `add-notebook-projection-identity`) carry no supporting folder at all. **But
   the finding's second half is right and was not answered by that.**
   `release-realization`'s "Origin retention at archive" scenario expects a
   staged-origin change's READABLE SUPPORT MANIFEST to carry the identical origin
   id and path, and a packet with no manifest gives that gate nothing to read. So
   the manifest lands — zero selected files, both remaining staged paths, the
   source revision, the repeated origin — and the documents stay where the later
   tranches need them. `proposal-support.py verify add-signed-execution-chain`
   passes, and doc-health's `location-conformance` support arm is satisfied by a
   manifest whose `files` list is empty.

## The second Codex round

Three P1 findings on `d3ff87c6`. Two taken, one judged SUPERSEDED — recorded as
superseded rather than silently skipped.

4. **"Reject forks after a predecessor." TAKEN IN FULL, and it is a real hole in
   the constitution R4 exists to be.** Two successor links binding the same
   predecessor under the same chain identity each satisfied R4 independently, so
   an authorized signer could produce two conflicting histories that both
   validate and a consumer shown either would see a well-formed chain. R4 now
   requires successor UNIQUENESS and states plainly that this capability defines
   no fork, branch or resolution semantics — a consumer offered two candidate
   successors REFUSES rather than preferring the longer, the earlier, or the one
   it was handed. **The lesson generalizes:** the mix-and-match attack the topic
   found was framed as coming from OUTSIDE the chain, and R4 as first drafted
   defeated only that framing; the same attack from a signer INSIDE the chain
   walked through. A binding rule has to close both directions or it closes one.
5. **"Test omission of a required chain link." TAKEN.** R6's fixture line now
   names the truncated-but-correctly-signed chain and the no-declared-expectation
   consumer as two separate fixtures, with the reason spelled out: neither is a
   malformed link, so a validator built only against malformed-link fixtures
   passes both.
6. **"Test self-asserted standing authority." SUPERSEDED, not declined.** The
   finding is correct against the commit it reviewed, but the round-1 correction
   to the same requirement removed the branch it tests: there is no
   `standing_authority` origin any more, so there is nothing to self-assert. The
   replacement fixture — a ratification offered under standing authority with no
   wallet, which begins NO chain — is already in tasks 2.2's R1 list. This is the
   patch-then-unify sequence of D5 seen from the fixture side: had the branch
   been patched rather than removed, this fixture would have been owed.

## Risks that survive

1. **A capability that governs nothing until its reader ships.** Accepted under
   D7 and made visible by R10 rather than hidden. The mitigation is that R10 makes
   the gap a stated property of the family instead of something a reader discovers.
2. **The family may govern nothing for its only current ratifier.** After D5's
   correction there is no weaker branch to fall back to: until the root issuer
   holds a wallet, ratifications by that authority begin no chain. This is the
   honest state and it is deliberately uncomfortable — it converts "we have a
   chain of a lesser kind" into "we have no chain yet, and here is the missing
   instrument". Named as a residual risk because the remedy is another change's
   S-work, not this packet's.
3. **Tranche two could find R4's binding rule insufficient** once four more link
   types exist. Tranche two extends it; the shape it extends is fixed here
   deliberately, because the topic's mix-and-match finding shows what happens when
   the binding is designed after the links.
4. **The evidence plane's implementation is unspecified.** R7 states the
   properties (append-only, signed leaves, inside the governed store, the record);
   it names no log implementation. That is deliberate at the neutral layer, and it
   means realization owes the choice.
