# Staged: every governed act carries a signature, and the chain is the permission to merge

Status: staged
Kind: capability-proposal
Summary: A ratification signed with a presented wallet begins a CHAIN that travels
with the work — enrollment, harness setup, each runner's attestation, the decision
to open a pull request, the council's review, and the merge gate that validates the
whole chain before it lets anything land. A broken link is not a warning; it is a
fraud signal and there is no merge. The omnigent layer REFUSES to build an
unverified chain, so the chain is a precondition of execution rather than a record
of it. Brett ruled 2026-08-27 that the anchoring layer goes ON CHAIN — definitively
for financial and medical records — with patients anchoring commitments and consent
checkpoints and working with hospitals and insurers through verifiable presentations.
The same chain shape serves MedxFactory through HealthLinc and LedgerxFactory
through LedgerLinc, which is what proves the family belongs in the neutral layer.
A chain-selection study is vendored beside this file and answers Q3: the signed
transparency log is the record, Bitcoin is the primary anchor with Kaspa an
optional secondary, consent logic stays in a governed permissioned layer, and
nothing anchored is ever an unsalted hash.

## Pre-document idea notes

Unstructured, kept because the reasoning is younger than the vocabulary.

- The family already signs the *decision*. `add-wallet-carried-review-authority`
  makes review authority a wallet-carried grant with a root issuer anchored to a
  named operator. What it does not yet do is carry that signature FORWARD: the
  ratification is signed, and then the work happens in a lane that cannot prove
  it descended from that ratification.
- The interesting inversion: this is not an audit trail. An audit trail is
  written after the fact and can be forged after the fact. A chain that the
  merge gate VALIDATES is a permission — you cannot merge what you cannot prove.
  The record and the control are the same object.
- "Broken chain = fraud signal" is deliberately stronger than "broken chain =
  needs review". A missing link means either the act did not happen or something
  is misrepresenting that it did. Both are refusals.
- The tier split fell out of a constitutional fact rather than a design
  preference: omnigent workers carry `access_secrets: false`. A worker therefore
  CANNOT hold an authority credential. So authority stays human-held, and
  runner attestations carry an ephemeral per-task identity issued — and signed
  — at the harness controller, whose key never enters the worker (the PR's own
  review round caught the first draft handing the runner the key; Q7 records
  the correction and asks for the mechanism). The worker proves *this task ran
  as declared*; it never proves *someone authorized this*.
- On-chain arrived from the medical side first, and the honest constraint arrived
  with it: PHI cannot go on a public chain, and a design that hand-waves that is
  worse than no design. What goes on chain is the commitment, not the record.
- That note originally read "the commitment and the consent". The chain-selection
  study corrected it twice over — consent *state* stays in the permissioned layer
  because on-chain consent rows are publicly linkable to a person, and the
  commitment must be salted and keyed because a plain hash of personal data is
  itself personal data. Both corrections are kept visible here rather than
  silently patched, because the wrong version is the intuitive one and a later
  reader will arrive holding it.
- HealthLinc and LedgerLinc are the same shape twice. That is the argument for a
  neutral family: if the chain only made sense for one domain it would belong in
  that domain's repository.

## The chain

Ten links. Each names what is signed, by whom, and what refuses when it is absent.

| # | Link | Signed by | Absent ⇒ |
| --- | --- | --- | --- |
| 1 | **Ratify with the wallet presented** — the ratifying human presents a wallet-carried authority; the ratification records the presentation | human authority credential | no ratification; nothing downstream can begin |
| 2 | **Ratified ⇒ enrolled, atomically, inside the signed handshake** — enrollment is not a second act that could diverge | same signature as link 1 | a ratified-but-unenrolled state, which is the divergence this link exists to make impossible |
| 3 | **The traveling contract** — the signed ratification becomes an artifact that accompanies the work rather than a row in a table it must be looked up in | — (carried) | the chain cannot be checked at the point of use |
| 4 | **Harness-controller setup attestation** — the controller attests the environment it prepared | controller certificate | runner attestations have no issuer to chain to |
| 5 | **Runner attestations** — each runner attests its model, its version, and its local harness | per-task identity (key held at the controller; signature produced there) | the work cannot say what produced it |
| 6 | **Signed PR-open decision** — opening a pull request is itself a decision and is signed as one | per-task identity + carried contract | the PR is an orphan act |
| 7 | **Council review with the signed proposal as the brief** — the council reviews the chain-carrying artifact, not a summary of it | council seats | review is of a restatement, which is the fidelity defect this family keeps finding |
| 8 | **Chain-validating merge gate** — the gate walks the chain before it permits a merge | gate (verifier) | **no merge** |
| 9 | **Broken chain = fraud signal** — a gap is refused and reported as a fraud signal, never downgraded to a warning | — | (this IS the refusal) |
| 10 | **Governed post-merge test** — consumes the proposal AND the review notes, so what was promised is what is tested | per-task identity | the test is disconnected from the claim it should verify |

**Link 8 is the load-bearing one.** Links 1–7 could be recorded by a
well-behaved lane and forged by a badly-behaved one. Link 8 is what makes the
chain a permission instead of a story: nothing merges unless the chain validates.

## The tier model

Two credential classes, and the boundary between them is constitutional rather
than conventional.

**Tier 1 — authority credentials, HUMAN-HELD.** The wallet-carried grants that
say *this person may ratify, may approve, may delegate*. These are never held by
an agent, a runner, or a lane. `add-wallet-carried-review-authority` already
anchors the root issuer to a named operator, which is the shape this tier
extends.

**Tier 2 — attestation identities, EPHEMERAL and PER TASK.** Issued by the
harness controller under its own certificate, valid for one task, and capable of
exactly one thing: signing an attestation that *this ran, as this model, at this
version, under this harness*.

**Why the split is forced, not chosen.** The omnigent contract family holds
`access_secrets: false` as a constitutional constraint on every worker archetype.
A worker that cannot access secrets cannot hold an authority credential — so any
design in which a runner signs *authority* contradicts a ratified constraint. The
tier split is what that constraint looks like when you still want signed
execution.

**And the per-task key never enters the worker.** The same constraint reaches
the attestation key too: `access_secrets: false` is written to hold in *every*
configuration, and a short lifetime does not stop a private key being a secret.
So tier 2's issuing controller is also its SIGNER — the runner submits the
payload it wants attested and receives a signature over it, and no key bytes
cross into the worker at any point. Links 5, 6 and 10 read that way: signed at
the controller boundary, *about* the runner, never *by* a key the runner holds.
"Ephemeral" describes the identity's lifetime, not a relaxation of custody, and
a design that hands a worker a key for one task has already breached the
constraint it claims to honour.

The two tiers answer different questions, and conflating them is the failure to
avoid: tier 1 answers **"who permitted this?"**, tier 2 answers **"what actually
ran?"**. A chain needs both and must never let one stand in for the other.

## The omnigent enforcement claim

**The layer refuses to build an unverified chain.** This is the claim that makes
the topic worth raising, and it is a claim about a PRECONDITION, not about
record-keeping.

The weak version — omnigent records what it did, and something later checks —
gives an audit trail that a compromised or careless lane can write falsely. The
strong version is that the omnigent layer will not execute a step whose inbound
chain does not verify. Verification moves from *after* to *before*, and the
record becomes a by-product of a control rather than a substitute for one.

This is the same doctrine the family already applies elsewhere: a gate that
cannot evaluate its condition REFUSES rather than proceeding, and an unevaluable
answer never reads as permission.

## The on-chain layer, as ruled

Brett ruled 2026-08-27 that the anchoring and consent layer goes **on chain**,
definitively, and **especially for financial and medical records**. The ruling
is recorded as it was given; what the study refines is *which* chain each part
lands on — public commitments for the anchoring layer, a governed permissioned
ledger whose state roots are anchored for consent, and raw records on neither.

A chain-selection study ran in parallel and is vendored beside this file as
[`chain-selection-study.md`](chain-selection-study.md) — research input, dated
2026-08-27, sourced and date-checked. This section cites its recommendation; it
does not re-argue it, and Q3 defers to it rather than restating the analysis.

### The recommended architecture, from the study

Three layers, and the load-bearing point is that **the blockchain is not the
record**:

- **Evidence plane (off-chain).** An append-only signed transparency log
  (RFC-6962 / Certificate-Transparency and Sigstore-Rekor pattern) inside the
  factory's governed store. Every ratification, attestation, verdict and merge
  decision is a signed leaf. *This* is the primary chain of custody — the ten
  links of §"The chain" live here. Chains only make it externally undeniable.
- **Public anchoring (commitments only).** **Bitcoin as the primary anchor**,
  via OpenTimestamps-style aggregation; **Kaspa as an optional low-latency
  secondary anchor**, honouring the named candidate and adding an independent
  proof-of-work witness under different governance. Receipts in a
  **chain-agnostic multi-anchor format** (digest → aggregation Merkle path →
  per-chain {anchor transaction, its transaction-to-block or DAG inclusion
  proof, block header} list). The transaction and its inclusion proof are part
  of the receipt, not a lookup deferred to verification time: a block header
  commits only to a transaction root, so a header plus a bare transaction
  reference proves nothing once the transaction itself is unavailable — which
  on Kaspa is a certainty within days, and on any chain is the ten-year
  assumption.
- **Consent and execution logic: NOT on the anchoring chain.** Consent,
  enrollment and access policy are authority questions and belong in the
  governed policy plane, and — where several external covered entities must
  share state — a permissioned consortium ledger whose **state roots are
  anchored** by the layer above. Explicitly **not** smart contracts on the
  anchoring chain, and **not** Kasplex or Igra in 2026.

**The Kaspa conditions are not optional.** Kaspa L1 **prunes transaction data
after roughly three days**, which cuts directly against a ten-year evidentiary
claim. Adopting it as a secondary anchor therefore requires running an archival
node, **capturing and retaining full inclusion proofs at anchor time**, and
treating Kaspa anchors as **corroborating evidence, never sole** evidence. A
design that anchors to Kaspa and expects to re-derive the proof later has
already lost it.

**The multi-anchor receipt is the ten-year exit path**, and it is why chain
selection is not a one-way door: anchor targets can be added or dropped without
touching the evidence plane. If Kaspa matures, promote it; if it fades, drop it
and lose nothing.

### The three priors, tested

The named candidate came with three stated priors. The study tested each; the
verdicts are recorded as they came back, including the one that did not hold.

| Prior | Verdict | What the study found |
| --- | --- | --- |
| "Kaspa is one of the only non-captured chains besides Bitcoin" | **QUALIFIED** | Launch fairness and absence of foundation control check out. Operational capture does not support the absolute: mining-pool concentration roughly as bad as Bitcoin's, one public miner targeting ~16% of hashrate, VC-funded L2 companies absorbing core devs — and the set of credibly neutral chains is larger than {Bitcoin, Kaspa}. |
| "Bitcoin is just too expensive" | **REFUTED for anchoring** | Merkle aggregation (OpenTimestamps) makes Bitcoin anchoring ~$0 marginal per record; even naive hourly self-anchoring is ≈$2.1k/yr. The objection holds *only* for per-record individual transactions and for contract execution, which Bitcoin cannot do anyway. This refutation is what puts Bitcoin in the primary-anchor seat. |
| "KAS is fractions of a penny per transaction" | **CONFIRMED**, and understated | Typical fees are fractions of a *thousandth* of a penny (~$0.000001–0.000003). Caveat carried honestly: this is partly a symptom of low demand and a security budget the fee market does not yet fund. |

Recording the refuted prior is the point of the exercise. The cost objection was
the reason to look past Bitcoin, and it did not survive aggregation — so the
architecture changed rather than the evidence being read to fit.

### What goes on chain, and what must not

**Raw PHI never touches a public chain.** A public chain is append-only,
world-readable and permanent — three properties that are individually
incompatible with HIPAA's treatment of protected health information. A design
that puts PHI on chain "encrypted" is still wrong: it publishes a permanent
ciphertext whose key management becomes the only thing standing between a
patient and irreversible disclosure, forever, against future cryptanalysis.

**And a plain hash is not enough either.** This topic first drafted the split
with "commitments (hashes)" on chain. The vendored study refutes that: EDPB
**Guidelines 02/2025 (v2.0, adopted 2026-07-07)** hold that a hash of personal
data *is itself personal data*, and a bare record hash is not HIPAA Safe-Harbor
de-identified either. So the anchored value must be a **salted, keyed
commitment** (HMAC over content under a per-record secret salt held in the
governed layer), which buys the property a public chain otherwise cannot offer:
**erasure by salt destruction** — destroy the salt and the on-chain residue is
effectively anonymous, satisfying erasure by design against a ledger that
cannot forget.

So the split is:

| Layer | Holds | Property relied on |
| --- | --- | --- |
| **Off-chain, encrypted custody** | the record itself — PHI, financial detail | revocable, deletable, access-controlled |
| **Governed permissioned layer** | consent state, and the salts | shareable between covered entities, erasable |
| **On chain** | **salted keyed commitments** to records — never plain hashes | tamper-evidence, ordering, erasure-by-salt-destruction |
| **On chain** | commitments to consent-log **checkpoints**, not per-patient consent rows | non-repudiation without public linkability to a person |
| **On chain** | the chain anchors of §"The chain" | the merge gate can verify without the payload |
| **Patient-held** | the access-granting keys | patient control is the point |

**A commitment proves a record existed and has not changed. It does not reveal
the record.** That is the whole trick, and the design must not drift off it.

Two rows above were corrected by the study rather than authored against it, and
both corrections narrow the vision: consent *state* does not go on chain (it
would be publicly linkable to a person), and no anchored value is ever an
unsalted hash.

### Patients, hospitals, insurers

The expansion vision: a patient anchors record-commitments and consent
checkpoints, and works with hospitals and insurers **through** that layer —
presenting verifiable presentations rather than surrendering records. A hospital
verifies that a consent is current and that a record's commitment matches what it
holds; an insurer verifies that a claim references a real, unaltered, consented
record. None of that requires either party to read PHI they were not granted.

**Where the ruling and the research pull against each other, stated plainly.**
The ruling includes patients "putting PHI portions on chain". Taken literally
that is refused by the research: raw PHI, encrypted PHI, and plain hashes of PHI
are all out (§6 of the study). What survives, and what this topic proposes as
the faithful reading, is that the patient puts *a verifiable handle to a PHI
portion* on chain — a salted keyed commitment — and discloses the portion itself
off-chain under a consent whose checkpoint is anchored. The patient-facing
behaviour the ruling asks for is preserved: they choose what to share, with
whom, provably. What changes is where the bytes live. **This reading needs
Brett's confirmation** (Q6) rather than being assumed, because it narrows a
ruling and a topic should never quietly narrow one.

A second reality check from the study, worth carrying now so tranche three is
not designed in a vacuum: US hospital and insurer interoperability runs on
FHIR/TEFCA rails, not chains. A chain layer earns its place as the **neutral
integrity witness** those rails lack — who consented to what, when, and which
record version was exchanged — not as a replacement for them.

Revocation is the sharp question and is deliberately raised here rather than
assumed: an on-chain consent record can be superseded by an on-chain revocation,
but **nothing on a chain can be un-published**, and no revocation reaches a copy
already disclosed. The design must state that limit rather than let "patient
controlled" imply more than it delivers — the same honesty the credential-custody
work applied to bearer secrets.

## Claims — the domain mapping

Settled enough to state; each is a claim this topic asserts and a later change
must carry or refute.

1. **The chain family is NEUTRAL and lives in openxFactory.** It composes with
   `openxwallet` (the authority instrument), `trust-anchor` (certificates and
   chain custody), `identity-brokering` (who a signer is), and
   `roles-authority-model` (what authority means).
2. **MedxFactory → HealthLinc, the patient app.** A treatment plan is ratified,
   simulated, reviewed, and "merged" — where merge means *pushed to the patient
   app, or printed as signed orders*. The chain is what makes a printed order
   verifiable rather than merely printed.
3. **LedgerxFactory → LedgerLinc, financial analysis and reviews.** An analysis
   or review plan runs the same chain; "merge" means *published to the ledger
   app*.
4. **The two mappings are the same shape.** That is the neutral-layer proof: a
   family that only fit one domain would belong in that domain's repository.
   HealthLinc and LedgerLinc differ in payload and regulator, not in chain.
5. **"Merge" is domain-interpreted.** In codexFactory it is a git merge; in
   HealthLinc a push to the patient app; in LedgerLinc a publication. The gate is
   the same act — *validate the chain, then permit the terminal step*.
6. **The evidence plane is OFF chain, and it is the record.** The signed
   transparency log inside the governed store is the primary chain of custody;
   public anchoring only makes it externally undeniable. A design in which the
   blockchain *is* the record has confused the witness for the evidence — and
   would also be the design that cannot satisfy erasure.
7. **Anchoring is multi-target and reversible by construction.** Receipts use a
   chain-agnostic format (digest → aggregation Merkle path → per-chain {anchor
   transaction, inclusion proof, block header}), captured whole at anchor time,
   so anchor targets are added or dropped without touching the evidence plane.
   This is the claim that makes a ten-year commitment survivable, and it is why
   Q3's answer is a starting configuration rather than a permanent one.

## Conflicts

Where this topic touches live work, and how it must sequence. **Four active
OpenSpec changes** occupy adjacent ground — note these are ACTIVE CHANGES, not
staged topics, which raises the bar: their ratified text governs, and this topic
composes with it rather than proposing alternatives.

| Live work | State | How this topic sequences |
| --- | --- | --- |
| `add-wallet-carried-review-authority` | 31 done / 18 open; **S2 issuer anchor REALIZED** | **The direct predecessor.** Its wallet-carried grant with a root issuer IS link 1's instrument. This topic must NOT re-invent a signing primitive; tranche one consumes it. If the two disagree, that change's ratified text wins. |
| `add-trust-anchor` | ratified 2026-08-21, realized at `contract-v1.37`; 24 done / 9 open | Owns certificate records and declared chain custody. The harness controller's certificate (link 4) and the per-task issuance (link 5) are `trust-anchor` shapes — this topic must express them in that vocabulary, not a parallel one. |
| `add-identity-brokering` | 20 done / 10 open | Owns persona assertion and actor-subject reference. **Who a signer is** belongs there; this topic owns **what the signature attests**. The seam is the `actor_subject` its impact map already names as a successor. |
| `implement-openxpki-install-repo` | 22 done / 8 open | The runtime CA that would issue the controller certificate. This topic depends on it for tranche two and must not assume it before it exists. |

**The collision risk this topic must actively avoid** is inventing a second
identity or certificate vocabulary. Three of the four changes above already own
one. Every link in §"The chain" should resolve to an existing family or be
raised as an explicit gap — a new schema here would be the "two records of one
decision" defect at contract scale.

**A conflict inside the vision itself**, stated rather than smoothed: link 9
says a broken chain is a fraud signal, and the on-chain layer says nothing can be
un-published. A false attestation that reaches the chain is therefore permanent.
That argues for anchoring LATE (commit only what has been validated) and is a
real design constraint on tranche three, not a detail. The vendored study
sharpens it: because anchoring is aggregated and batched anyway, anchoring late
costs latency measured in an aggregation interval, not in architecture — the
constraint is cheap to honour and expensive to ignore.

**A second conflict, between the ruling and the research**, and the more
consequential one. The 2026-08-27 ruling has patients putting PHI portions on
chain; the research refuses raw PHI, encrypted PHI and plain hashes alike. This
topic reads the ruling as *commitments*, preserves every patient-facing
behaviour it asked for, and raises the narrowing as **Q6** rather than adopting
it silently. Until Q6 is ruled, tranche three cannot be drafted without either
guessing at a ruling or building something the regulators named. Neither is
acceptable, so the question gates the tranche.

## Open questions

None blocking; all seven are for the eventual clarify round. Q3 and Q5 now carry
the vendored study's recommendation rather than open analysis; Q6 is the one
that needs a ruling before tranche three can be drafted honestly; Q7 came out of
the review round on this topic's own pull request and asks for a mechanism, not
a ruling.

### Q1 — What are the wallet-presentation mechanics?

Context: Link 1 says the ratifier "presents a wallet". The shipped
  `openxwallet-grant` vocabulary expresses the authority, and
  `add-wallet-carried-review-authority` anchors its issuer — but the act of
  PRESENTING one at ratification time, and what the ratification records as proof
  of that presentation, is unspecified.
Recommended answer: Express presentation in the existing grant vocabulary
  plus a proof-of-possession step; record the presentation in the ratification
  record rather than a new artifact.
Explanation: The family already refuses a wallet address as identity proof;
  possession must be demonstrated, not asserted. Reusing the grant vocabulary
  keeps one instrument rather than two.
Disposition status: open

### Q2 — Where exactly is the on-chain boundary?

Context: The ruling is that anchoring goes on chain. The boundary between
  what is anchored and what stays in encrypted off-chain custody needs to be
  drawn precisely enough that an implementer cannot drift PHI across it.
Recommended answer: On chain: salted keyed commitments, commitments to
  consent-log checkpoints, and chain anchors. Off chain: every payload without
  exception, plus consent state and the salts. Draw the line in contract text,
  with a validator that refuses a record shaped like a payload AND refuses an
  unsalted commitment.
Explanation: "Don't put PHI on chain" as prose will erode; as a refusal it
  holds. This mirrors how the hosting record refuses secret-shaped fields by name.
  The unsalted-commitment refusal is the new half, and it is the one an
  implementer is most likely to get wrong, because a plain SHA-256 of a record
  looks like exactly the right thing to anchor until you read EDPB 02/2025 v2.0.
Disposition status: open — boundary corrected by the vendored study; the
  refusing-validator shape still to be specified

### Q3 — Which chain?

Context: Chain selection was undecided when this topic opened, with **Kaspa
  as the named candidate**. The parallel research fan-out has since COMPLETED and
  is vendored beside this file as
  [`chain-selection-study.md`](chain-selection-study.md) — Kaspa reviewed in
  depth against a comparison set (Bitcoin, Ethereum+L2, Algorand, Hedera,
  Cardano, Ergo, permissioned), with a capture scorecard, a cost model at
  2026-08-27 prices, and an honest §9 of what could not be established.
Recommended answer: Adopt the study's recommendation rather than re-deriving
  it — transparency log as the evidence plane, **Bitcoin (OpenTimestamps
  aggregation) as the primary anchor**, **Kaspa as an optional low-latency
  secondary anchor** under its three conditions (archival node, inclusion proofs
  retained at anchor time, corroborating-only status), consent logic in the
  governed permissioned layer with anchored state roots, and a chain-agnostic
  multi-anchor receipt so the choice stays reversible. Not smart contracts on the
  anchoring chain; not Kasplex or Igra in 2026.
Explanation: The question is answered on evidence, and the answer changed the
  architecture: the cost objection that pointed away from Bitcoin did not survive
  aggregation, and Kaspa's ~3-day L1 pruning disqualifies it as a sole ten-year
  anchor while leaving it useful as a second witness. Deferring further would be
  deferring past the evidence. What keeps this OPEN rather than settled is that a
  chain selection is a governance decision for a change to carry and Brett to
  rule, not one a staging topic closes on its own.
Disposition status: open — research COMPLETE with a recommendation on the
  table; awaiting a ruling, not awaiting more analysis

### Q4 — Where do the tranche boundaries fall?

Context: The exit path proposes three tranches. Whether tranche one is
  genuinely composable today, and whether attestation and anchoring can be split
  as cleanly as §"Exit path" assumes, needs testing against the four live changes.
Recommended answer: Tranche one = links 1–3 only, because they need nothing
  that does not exist. Re-derive the later boundaries once the omnigent layer and
  chain selection are real.
Explanation: A tranche that depends on an unbuilt layer is a plan, not a
  tranche. The family's own release-realization discipline is the precedent.
Disposition status: open

### Q5 — Are smart contracts or an L2 in scope?

Context: Anchoring needs only commitment storage. Consent verification,
  revocation checking and presentation validation COULD be enforced on chain by
  contract code, or could stay off chain with the chain used purely as evidence.
Recommended answer: Evidence-only on the anchoring chain — no contract code
  there, ever, per the study. Consent logic goes to the governed permissioned
  layer with anchored state roots. IF a genuinely public programmable layer is
  later forced (patient-facing consent verifiability across organizations sharing
  no consortium), the study's answer is an **Ethereum L2 with EAS** — mature,
  audited, $0.001–0.05 per action — and explicitly **not** Kasplex or Igra in
  2026, whose stacks are weeks-to-months old and unaudited. Re-evaluate those, and
  Kaspa's L1 covenants and ZK precompile, in 12–24 months.
Explanation: This question was drafted as a judgement call and came back
  answered by evidence, in the same direction but for a firmer reason: contract
  code is an irrevocable deployment with its own vulnerability class, and putting
  regulated logic on an unaudited stack compounds that with a maturity risk. The
  permissioned layer is also the only posture EDPB and HIPAA guidance cleanly
  supports, so the split is regulatory as much as architectural.
Disposition status: open — direction confirmed by the study; the trigger
  condition for a public programmable layer still needs stating

### Q6 — Does "patients put PHI portions on chain" mean commitments?

Context: The 2026-08-27 expansion ruling includes patients placing PHI
  portions on chain. Read literally that is refused by the research: raw PHI,
  encrypted PHI, and plain hashes of PHI are all excluded, the last of these by
  EDPB Guidelines 02/2025 v2.0. This topic has read it as *a verifiable handle to
  a PHI portion* — a salted keyed commitment anchored publicly, with the portion
  itself disclosed off-chain under an anchored consent checkpoint.
Recommended answer: Confirm the commitment reading, and record it as the
  ruling's operative form so no later change re-litigates it. The patient-facing
  behaviour is preserved in full — they choose what to share, with whom,
  provably; only the location of the bytes changes.
Explanation: A topic must not quietly narrow a ruling, and this reading does
  narrow it. Raising it as a question is the honest move: the alternative is an
  implementer discovering the gap at contract time, or worse, building to the
  literal reading and putting PHI-derived data on a public ledger that cannot
  forget. The erasure-by-salt-destruction property is what makes the narrowed
  reading genuinely serve the patient rather than merely comply.
Disposition status: open — needs Brett's confirmation; this is the one
  question where the topic has interpreted a ruling rather than applied it

### Q7 — Where does an attestation signature physically happen?

Context: Tier 2 forbids the runner holding the per-task key, which forces
  signing to the controller boundary but does not name a mechanism. A remote
  signing call the controller serves, a co-process holding the key behind an
  attested boundary, and a hardware-backed signer are all consistent with
  `access_secrets: false`, and they differ in exactly what an attacker who owns
  a runner for one task can obtain.
Recommended answer: Remote signing served by the harness controller, with the
  runner's signing REQUEST recorded alongside the signature it received, so the
  chain shows both what was attested and who asked for the attestation.
Explanation: Raised by the review round on this topic's PR, which read the
  original tier-2 wording — a key "issued" to the runner — as key custody, and
  was right to: shortening a credential's life does not make it non-secret, so
  the wording contradicted the very constraint the tier split exists to honour.
  The boundary is now stated in the tier model; the mechanism has to be named
  before tranche two drafts contract text, because it decides what the
  attestation actually proves about the runner.
Disposition status: open — for the clarify round; the boundary is forced by
  ratified text, the mechanism is a design choice

## Exit path

OpenSpec change(s), in three tranches, each gated on what actually exists.

**Tranche 1 — signed ratification + atomic enrollment. Composable TODAY.**
Links 1–3. Consumes `add-wallet-carried-review-authority`'s realized issuer
anchor and the shipped grant vocabulary; needs no omnigent layer and no chain.
This is the tranche that can become a change as soon as the topic is ruled.

**Tranche 2 — harness and runner attestation.** Links 4–6 and 10. Needs the
omnigent layer to enforce the precondition, and `implement-openxpki-install-repo`
to issue the controller certificate. Expresses its certificates in
`trust-anchor` vocabulary and its signer identity in `identity-brokering`.

**Tranche 3 — on-chain anchoring.** The commitment and anchor layer, plus the
permissioned consent plane whose state roots it anchors. The chain-selection
research is COMPLETE and its recommendation is on the table (Q3), so what this
tranche now waits on is a ruling — Q3's configuration and Q6's reading of the PHI
boundary — and the PKI plane being real. It carries the Q2 boundary as contract
text with a validator that refuses both payload-shaped records and unsalted
commitments, and it builds the multi-anchor receipt format first, because the
receipt is what makes the anchor choice reversible; anchoring to a single chain
with a bespoke receipt would be the one-way door this design exists to avoid.

Sequencing note: the evidence plane of claim 6 — the signed transparency log —
is a **tranche 1** artifact, not a tranche 3 one. The log is the record; the
anchors are late additions to it. Building the log last would mean tranches 1
and 2 had nowhere to write their signed leaves.

Links 7–9 — council review of the signed brief, the chain-validating merge gate,
and the fraud-signal refusal — span tranches: each tranche extends what the gate
validates. **The gate should exist from tranche one validating a short chain,
rather than arriving at the end validating a long one**, so the refusal path is
exercised from the start rather than first tested when it matters most.
