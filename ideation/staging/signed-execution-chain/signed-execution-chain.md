# Staged: every governed act carries a signature, and the chain is the permission to merge

Status: staged
Kind: capability-proposal
Summary: A ratification signed with a presented wallet begins a CHAIN that
travels with the work — enrollment, harness setup, each runner's attestation,
the decision to open a pull request, the council's review, and the merge gate
that validates links 1–7 — everything that exists pre-merge — before it lets
anything land; links 9–10 enforce at closure. A broken link is not a warning;
it is a fraud signal: no merge if it breaks before the gate, no closure and
nothing downstream — remediation of the failure itself excepted — if it breaks
after. The omnigent layer REFUSES to build an unverified chain, so the chain is
a precondition of execution rather than a record of it. Brett ruled 2026-08-27
that the anchoring layer goes ON CHAIN — definitively for financial and medical
records — with patients anchoring commitments and consent checkpoints and
working with hospitals and insurers through verifiable presentations. The same
chain shape serves MedxFactory through HealthLinc and LedgerxFactory through
LedgerLinc, which is what proves the family belongs in the neutral layer. A
chain-selection study is vendored beside this file as Q3's research input: the
signed transparency log is the record, consent logic stays in a governed
permissioned layer, and nothing anchored is ever an unsalted hash. ALL SEVEN
OPEN QUESTIONS WERE RULED 2026-08-29 by Brett Heap in a clarify sitting, and two
rulings diverge from what was recommended — Q3 seats KASPA as the primary,
operational witness and BITCOIN-VIA-OPENTIMESTAMPS ON EVERY ANCHORED ITEM as the
durability witness, inverting the study's ordering and dropping its optionality;
Q5 keeps the door open for on-chain contract code in a future change instead of
refusing it forever. The topic is fully ruled, and tranche one is DRAFTED,
RATIFIED and RAISED: the sitting answered the questions and did NOT green-light
the drafting — "draftable" was a readiness state and not an authorization — and
THAT WORD CAME 2026-08-29 in a separate in-session act, which also collapsed the
two parallel tranche-one packets onto pull request #495 and adopted Narrowing A
(tier 1 is RATIFYING authority; agent-held REVIEW wallets stay lawful). Brett
Heap RATIFIED that packet the same day.
Staging ID: openxFactory:staging:signed-execution-chain

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
  review round caught the first draft handing the runner the key; Q7 recorded
  the correction and asked for the mechanism, and 2026-08-29 ruled it: REMOTE
  SIGNING SERVED BY THE CONTROLLER, with the runner's request recorded beside
  the signature). The worker proves *this task ran as declared*; it never proves
  *someone authorized this*.
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

Ten links. Each names what is signed, by whom, and what refuses when it is absent; every signature also covers the chain identity and its predecessor, per the binding rule below the table.

| # | Link | Signed by | Absent ⇒ |
| --- | --- | --- | --- |
| 1 | **Ratify with the wallet presented** — the ratifying human presents a wallet-carried authority; the ratification records the presentation | human authority credential | no ratification; nothing downstream can begin |
| 2 | **Ratified ⇒ enrolled, atomically, inside the signed handshake** — enrollment is not a second act that could diverge | same signature as link 1 | a ratified-but-unenrolled state, which is the divergence this link exists to make impossible |
| 3 | **The traveling contract** — the signed ratification becomes an artifact that accompanies the work rather than a row in a table it must be looked up in | — (carried) | the chain cannot be checked at the point of use |
| 4 | **Harness-controller setup attestation** — the controller attests the environment it prepared | controller certificate | runner attestations have no issuer to chain to |
| 5 | **Runner attestations** — each runner attests its model, its version, and its local harness | per-task identity (key held at the controller; signature produced there) | the work cannot say what produced it |
| 6 | **Signed PR-open decision** — opening a pull request is itself a decision and is signed as one | per-task identity (controller-signed) + carried contract | the PR is an orphan act |
| 7 | **Council review with the signed proposal as the brief** — the council reviews the chain-carrying artifact, not a summary of it | council seats | review is of a restatement, which is the fidelity defect this family keeps finding |
| 8 | **Chain-validating merge gate** — the gate walks links 1–7 before it permits a merge | gate (verifier) | **no merge** |
| 9 | **Broken chain = fraud signal** — a gap is refused and reported as a fraud signal, never downgraded to a warning | — | (this IS the refusal) |
| 10 | **Governed post-merge test** — consumes the proposal AND the review notes, so what was promised is what is tested | per-task identity (controller-signed) | the chain never closes: anything that consumes the merge refuses (remediation excepted), and link 9 fires |

**A chain is hash-linked, not a bag of signatures.** Every link from
enrollment onward signs over two things besides its own content: the chain
identity — the digest of the signed ratification that link 3 carries — and
the digest of the link that precedes it. Link 8 validates that continuity,
not merely the presence of the required signatures: individually valid
setup, runner, PR-open and review artifacts from DIFFERENT executions must
not assemble into a chain, because with concurrent or repeated tasks a
signature bag is exactly what a badly-behaved lane would submit. The review
round supplied this as the mix-and-match attack; the binding is what makes
"the chain travels with the work" cryptographic rather than narrative.

**Link 8 is the load-bearing one, and it walks links 1–7** — everything that
exists before a merge can. Links 1–7 could be recorded by a well-behaved lane
and forged by a badly-behaved one; link 8 is what makes that part of the chain
a permission instead of a story: nothing merges unless links 1–7 validate.
Links 9 and 10 sit on the other side of the merge and are enforced at the NEXT
gate, not this one: the chain is not complete at merge, it is complete at
CLOSURE, and a merged-but-unclosed chain — link 10 missing, failed, or
unsigned — is a refusing state for whatever consumes the merge (promotion,
release, the next chain that builds on it) and fires link 9's fraud signal. A
merge that already happened cannot be retroactively refused; what an unclosed
chain forfeits is everything downstream of it. One consumer is exempt by
design, or the invariant deadlocks: the remediation chain. When link 10 fails
on an ordinary defect, the corrective or revert change is itself a next chain
that builds on the merge — refuse it too and the repository can never repair
what it cannot retroactively unmerge. So an unclosed chain refuses every
consumer EXCEPT a chain whose declared, signed subject is that failure; a
remediation chain is still a full chain, ratified and signed like any other,
and promotion and release stay refused until a chain closes over the merge.
Fail-closed means the failure can be repaired, not that it is trapped. The
review round caught the first draft implying link 8 walks all ten — a gate
cannot walk a link that does not exist yet.

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

**And the controller must not notarize self-report.** A signature at the
controller boundary proves the controller signed the bytes it was handed —
nothing more. A compromised runner could submit a false model/version/harness
payload and links 5, 6 and 10 would still chain, which is exactly the
fabricated-but-valid-looking record this topic exists to refuse. So the
controller signs an attestation only where it can BIND the claims: the model,
version and harness of link 5 are facts the controller *provisioned* in link 4,
and it corroborates them against its own setup attestation rather than
accepting them from the runner; measurements only the runner can see are either
independently observed — hardware-attested where the platform offers it — or
carried explicitly as runner-claimed, never laundered into controller-attested
fact. The review round raised this as the second custody-adjacent defect: first
the key, now the claims — the controller is a signer, not a notary of whatever
it is told.

**The mechanism is now named: remote signing served by the controller.** Brett
ruled Q7 on 2026-08-29 as recommended. The runner submits the payload it wants
attested to a signing service that the HARNESS CONTROLLER serves, and the runner's
signing REQUEST is recorded alongside the signature it received — so the chain
shows both what was attested and who asked for the attestation, which a bare
signature does not. A hardware-backed signer (HSM) is a later HARDENING of that
same shape rather than a different answer, so adopting one changes where the key
sits and nothing about what the chain carries. Tranche two's contract text may
now name the mechanism; until this ruling it could not.

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
is recorded as it was given; what the study refined, and what his 2026-08-29 Q3
ruling then configured, is *which* chain each part lands on — public commitments
for the anchoring layer, a governed permissioned ledger whose state roots are
anchored for consent, and raw records on neither.

A chain-selection study ran in parallel and is vendored beside this file as
[`chain-selection-study.md`](chain-selection-study.md) — research input, dated
2026-08-27, sourced and date-checked. This section cites its recommendation; it
does not re-argue it. **Brett ruled Q3 on 2026-08-29 and his configuration
DIVERGES from the study's anchor ordering**, so both are recorded below, in
order: the study's recommendation as it came back, then the ruled configuration
that governs. The study itself is NOT edited — it is a dated research record,
and a record rewritten to agree with a later ruling stops being evidence.

### The recommended architecture, from the study

Three layers, and the load-bearing point is that **the blockchain is not the
record**. Its anchor ORDERING is superseded by the 2026-08-29 ruling in the next
subsection; everything else here — the evidence plane, the Kaspa conditions, the
consent split, the receipt format — still governs:

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
claim. Anchoring to it therefore requires running an archival node, **capturing
and retaining full inclusion proofs at anchor time**, and treating Kaspa anchors
as **corroborating evidence, never sole** evidence. A design that anchors to
Kaspa and expects to re-derive the proof later has already lost it. The three
conditions are stated without reference to which seat Kaspa holds, and the
2026-08-29 ruling carries all three forward unchanged.

**The multi-anchor receipt is the ten-year exit path**, and it is why chain
selection is not a one-way door: anchor targets can be added or dropped without
touching the evidence plane. That reversibility is what makes a ruling on
ordering a configuration rather than a commitment.

### The ruled configuration (Q3, ruled 2026-08-29 by Brett Heap)

**Both witnesses on every anchored item — Kaspa first, Bitcoin on everything.**
This is Brett's configuration of the study, not the study's own ordering, and it
is what governs.

- **Kaspa FIRST — the primary, OPERATIONAL witness.** Seconds, not hours. It is
  what answers when something needs to know now that a leaf was anchored. It is
  adopted under the study's three conditions, unchanged: an archival node,
  inclusion proofs captured AND retained at anchor time, and corroborating
  status. "Primary" here is order of arrival, never evidentiary weight — the
  pruning finding is not softened by the promotion.
- **Bitcoin batched via OpenTimestamps aggregation — the DURABILITY witness, on
  EVERY anchored item.** Hours, not seconds. **Ten-year claims cite Bitcoin.**
  There is no selectivity: no per-item judgement about which items are worth a
  Bitcoin anchor, because a rule that decides per item is a rule that will
  eventually decide wrong about the item that matters.
- **No third chain**, and nothing here reopens Kasplex or Igra in 2026.
- **Receipts stay chain-agnostic and multi-anchor and carry BOTH proofs** —
  digest → aggregation Merkle path → a per-chain list of {chain, block header,
  transaction reference}. The topic's standing correction over the study's
  identical shorthand still governs and does not contest it: each per-chain
  entry ALSO carries the transaction-to-block or DAG inclusion proof, captured
  whole at anchor time. His own Kaspa condition demands exactly that
  independently, and without it a header plus a bare transaction reference
  proves nothing once the transaction is pruned.
- **The transparency log remains the evidence plane**, and **consent logic stays
  in the governed permissioned layer** with anchored state roots. Neither half
  of the ruling moves anything onto a chain that the study kept off one.

**What the divergence actually is.** The study seated Bitcoin as the primary
anchor and Kaspa as an OPTIONAL secondary; the ruling keeps both chains, reverses
which one is called primary, and makes neither optional. The reasoning it was
ruled on is recorded because a two-round ruling is only honest with both rounds
in it, and the cost facts are what turned round one into round two — see Q3.
Every substantive finding of the study survives: its Kaspa conditions, its
pruning finding, its refuted cost prior, its refusal of contract code on the
anchoring chain. What changed is ordering and optionality.

### The three priors, tested

The named candidate came with three stated priors. The study tested each; the
verdicts are recorded as they came back, including the one that did not hold.

| Prior | Verdict | What the study found |
| --- | --- | --- |
| "Kaspa is one of the only non-captured chains besides Bitcoin" | **QUALIFIED** | Launch fairness and absence of foundation control check out. Operational capture does not support the absolute: mining-pool concentration roughly as bad as Bitcoin's, one public miner targeting ~16% of hashrate, VC-funded L2 companies absorbing core devs — and the set of credibly neutral chains is larger than {Bitcoin, Kaspa}. |
| "Bitcoin is just too expensive" | **REFUTED for anchoring** | Merkle aggregation (OpenTimestamps) makes Bitcoin anchoring ~$0 marginal per record; even naive hourly self-anchoring is ≈$2.1k/yr. The objection holds *only* for per-record individual transactions and for contract execution, which Bitcoin cannot do anyway. This refutation is what put Bitcoin in an anchor seat at all — the study's primary one, and, after the 2026-08-29 ruling, the durability witness on every anchored item. |
| "KAS is fractions of a penny per transaction" | **CONFIRMED**, and understated | Typical fees are fractions of a *thousandth* of a penny (~$0.000001–0.000003). Caveat carried honestly: this is partly a symptom of low demand and a security budget the fee market does not yet fund. |

Recording the refuted prior is the point of the exercise. The cost objection was
the reason to look past Bitcoin, and it did not survive aggregation — so the
architecture changed rather than the evidence being read to fit. The same fact
did the same work a second time in the clarify sitting: round one inverted the
ordering, the cost facts were put, and round two put Bitcoin on **everything**
(Q3). A refuted prior that only changes a document is decoration; this one
changed a ruling.

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

**Q2 ruled this boundary exactly as drawn, 2026-08-29 (Brett Heap).** The split
above is not guidance to be interpreted: it becomes CONTRACT TEXT carrying a
validator that refuses a payload-shaped record AND refuses an unsalted
commitment. Prose about not putting PHI on a chain erodes; a refusal holds. The
unsalted half is the one an implementer is most likely to get wrong, because a
plain SHA-256 of a record looks like exactly the right thing to anchor.

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
whom, provably. What changes is where the bytes live. The topic raised this as
**Q6** rather than assuming it, because it narrows a ruling and a topic should
never quietly narrow one.

**Confirmed 2026-08-29 by Brett Heap, and it is now the ruling's OPERATIVE
FORM.** "Patients put PHI portions on chain" means SALTED KEYED COMMITMENTS: a
verifiable public handle, the portion itself disclosed off-chain under an
anchored consent checkpoint, and salt destruction as the erasure mechanism.
Literal raw PHI, encrypted PHI and plain-hashed PHI on chain stay refused. No
later change re-litigates this — the commitment reading is no longer an
interpretation a later author may revisit, it is what the ruling says.

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
   the configuration Q3 was ruled to on 2026-08-29 — Kaspa first, Bitcoin via
   OpenTimestamps on everything — is a starting configuration rather than a
   permanent one. The receipt carries BOTH witnesses' proofs; adding or dropping
   a target changes the list, not the format.

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

**A second conflict, between the ruling and the research** — the more
consequential one, and **RESOLVED 2026-08-29**. The 2026-08-27 ruling has
patients putting PHI portions on chain; the research refuses raw PHI, encrypted
PHI and plain hashes alike. This topic read the ruling as *commitments*,
preserved every patient-facing behaviour it asked for, and raised the narrowing
as **Q6** rather than adopting it silently — because until Q6 was ruled, tranche
three could only be drafted by guessing at a ruling or by building something the
regulators named. Brett CONFIRMED the commitment reading on 2026-08-29 and it is
now the ruling's operative form, so the conflict is closed rather than managed:
there is one reading, and it is his.

**A third conflict, between a ruling and a recommendation, and it is left
OPEN by design.** Q5's recommendation was that contract code never runs on the
anchoring chain. Brett ruled against the permanence of that — "allow contract
code later" — while leaving today's evidence-only posture exactly as
recommended. So this topic carries a standing tension it must not resolve on its
own: the regulatory and maturity caution the study documented is real and is
recorded, and it is ADVISORY to a future change rather than a bar on one. A
later author who reads the caution as a refusal has misread the ruling; a later
author who ignores it has misread the record.

## Open questions — all seven SETTLED 2026-08-29

**ALL SEVEN ARE RULED.** The clarify sitting was held **2026-08-29** and Brett
Heap ruled every question in it; each disposition below carries its date and its
ruling authority. The section keeps every question and its structure — the
heading gains a closure stamp, nothing is removed — because a question and its
recommendation are the record a disposition is read against, and deleting the
question would leave the ruling answering nothing.

*The heading declares the closure because that is where the readiness gate reads
it.* `completeness._open_question_items` closes a question section either by a
resolution word in the HEADING or by an uppercase closure token
(`RESOLVED`/`ANSWERED`/`CLOSED`/`DECIDED`/`SETTLED`) in the body — and `RULED`
is not one of them, so a section full of rulings would still have counted as one
standing open item and refused proposal commissioning for a topic that is
actually decided. **A later author who adds a Q8 must strike `SETTLED` from this
heading**, or the gate will count the new question as already closed. The
declaration is in the heading rather than buried in prose for exactly that
reason: it is where someone adding a question cannot miss it.

Four were ruled AS RECOMMENDED (Q1, Q2, Q4, Q7) and one CONFIRMED as recommended
(Q6). **Two diverge, and both are labelled where they land**: **Q3** was ruled in
TWO ROUNDS to Brett's own configuration of the study rather than to the study's
ordering, and **Q5** OVERRIDES its recommendation.

The gates these questions held are now open. **Q3 and Q6 were tranche-three
blockers**; **Q7 gated tranche two's contract text**; tranche one was gated by
none of them and never was.

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
Disposition status: ruled 2026-08-29 — Brett Heap, in session; AS RECOMMENDED
Disposition (2026-08-29, RULED BY BRETT HEAP): as recommended. Presentation is
  expressed in the SHIPPED grant vocabulary plus a PROOF-OF-POSSESSION step, and
  the presentation is recorded in the RATIFICATION RECORD ITSELF. No new
  artifact is created for it. Tranche one therefore consumes
  `add-wallet-carried-review-authority`'s realized instrument rather than
  extending it, which is the whole reason link 1 is composable today.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's clarify ruling)
  · 2026-08-29

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
Disposition status: ruled 2026-08-29 — Brett Heap, in session; AS RECOMMENDED
Disposition (2026-08-29, RULED BY BRETT HEAP): as recommended. ON CHAIN, and
  nothing else: salted keyed commitments, commitments to consent-log
  CHECKPOINTS, and the chain anchors. OFF CHAIN: every payload without
  exception, plus consent STATE and the SALTS. The line is drawn as CONTRACT
  TEXT carrying a validator that refuses a payload-shaped record AND refuses an
  unsalted commitment — the refusal is the durable form because prose about
  where PHI may not go erodes and a validator does not.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's clarify ruling)
  · 2026-08-29

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
  deferring past the evidence. What kept this open rather than settled was that a
  chain selection is a governance decision for a change to carry and Brett to
  rule, not one a staging topic closes on its own — which is exactly how it went:
  he ruled it on 2026-08-29, and to a different configuration than the one
  recommended here. One correction governs over
  the study's compact receipt sketch: receipts carry the anchor transaction and
  its transaction-to-block or DAG inclusion proof, as the architecture section
  and claim 7 state — the study's own Kaspa conditions demand the same
  retention.
Disposition status: ruled 2026-08-29 in TWO ROUNDS — Brett Heap, in session;
  **DIVERGES from the recommendation above**
Disposition, ROUND 1 (2026-08-29, RULED BY BRETT HEAP — his text verbatim):
  "lets [sic] use Kaspa as primary and bitcoin as secondary". That INVERTS the
  study's ordering. It is recorded verbatim, before the cost facts were put to
  him, because a two-round ruling is only honest if the first round survives
  inside it — a record that shows only the final answer hides what the answer
  was reached against. The bracketed [sic] marks his spelling, and the lowercase
  "bitcoin" is his too: both are preserved because a verbatim record that tidies
  its subject's typing has stopped being verbatim, and the brackets are what
  keep the tidying visible instead of silent.
Cost facts put to him between the rounds (2026-08-27 prices, from the vendored
  study): Kaspa ~$0.000001 per transaction; Bitcoin via OpenTimestamps $0
  marginal per item on public calendars, or ~$2.1k/yr for a self-run hourly
  calendar; a raw Bitcoin transaction $0.12–0.36 with a spike history; and a
  cheaper sidechain adds federation trust and saves nothing.
Disposition, ROUND 2 (2026-08-29, RULED BY BRETT HEAP — the OPERATIVE
  configuration): **"Bitcoin-via-OTS on everything."** BOTH witnesses on EVERY
  anchored item. **Kaspa FIRST** — seconds; the primary, OPERATIONAL witness,
  adopted under the study's three conditions unchanged (archival node;
  inclusion proofs captured AND retained at anchor time; corroborating
  evidence, never sole). **Bitcoin batched via OpenTimestamps aggregation** —
  hours; the DURABILITY witness, and **ten-year claims cite Bitcoin**. Receipts
  stay chain-agnostic and multi-anchor and carry BOTH proofs: digest →
  aggregation Merkle path → a per-chain list of {chain, block header,
  transaction reference}. **No selectivity** — no per-item choice of which
  witness an item gets — and **no third chain**. The transparency log remains
  the evidence plane and consent logic stays in the governed permissioned layer
  with anchored state roots.
How this diverges, stated plainly: the study seated **Bitcoin as PRIMARY** with
  **Kaspa an OPTIONAL secondary**. The ruling keeps both chains, REVERSES which
  is called primary, and makes NEITHER optional. "Primary" in the ruling is
  order of arrival, not evidentiary weight — Kaspa's ~3-day L1 pruning finding
  is carried forward untouched, which is why its corroborating-only condition
  still holds even in the primary seat, and why the ten-year claim rests on
  Bitcoin. Every substantive finding of the study survives; ordering and
  optionality are what changed.
One shorthand, reconciled rather than smoothed: the round-2 receipt sketch names
  {chain, header, transaction reference}, the same compact form this question's
  Explanation already corrected in the study. The correction still governs and
  does not contest the ruling — each per-chain entry ALSO carries the
  transaction-to-block or DAG inclusion proof, captured whole at anchor time,
  which his own Kaspa condition demands independently and without which a
  header plus a bare transaction reference proves nothing once the transaction
  is pruned.
The vendored study is NOT edited. It is a dated research record; a record
  rewritten to agree with a later ruling stops being evidence, so the divergence
  is carried here and the study stands as it came back.
Gate: this was one of two TRANCHE-THREE blockers. With Q6 confirmed in the same
  sitting, **tranche three is OPEN**.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's clarify ruling)
  · 2026-08-29

### Q4 — Where do the tranche boundaries fall?

Context: The exit path proposes three tranches. Whether tranche one is
  genuinely composable today, and whether attestation and anchoring can be split
  as cleanly as §"Exit path" assumes, needs testing against the four live changes.
Recommended answer: Tranche one = links 1–3 only, because they need nothing
  that does not exist. Re-derive the later boundaries once the omnigent layer and
  chain selection are real.
Explanation: A tranche that depends on an unbuilt layer is a plan, not a
  tranche. The family's own release-realization discipline is the precedent.
Disposition status: ruled 2026-08-29 — Brett Heap, in session; AS RECOMMENDED
Disposition (2026-08-29, RULED BY BRETT HEAP): as recommended. **Tranche one is
  links 1–3 ONLY.** The later boundaries are RE-DERIVED when the omnigent layer
  and the PKI plane are real, not fixed now — a boundary drawn against an
  unbuilt layer is a guess wearing a tranche number. Two sequencing facts are
  ruled with it: the **signed transparency log is a TRANCHE-1 artifact**,
  because tranches 1–2 need somewhere to write their signed leaves; and the
  **chain-validating gate exists FROM TRANCHE ONE**, validating a short chain,
  so the refusal path is exercised from the start rather than first tested when
  it matters most.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's clarify ruling)
  · 2026-08-29

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
Disposition status: ruled 2026-08-29 — Brett Heap, in session; **RULED AGAINST
  THE RECOMMENDATION — his OVERRIDE of the study's answer**
Disposition (2026-08-29, RULED BY BRETT HEAP, OVERRIDING THE RECOMMENDATION —
  his words): **"Allow contract code later."** What the ruling PRESERVES is the
  posture: the anchoring chains stay EVIDENCE-ONLY today, and **no tranche now
  planned puts contract code on any of them**. What it REFUSES is the permanence
  the recommendation asked for. This change **MUST NOT constitutionalize "no
  contract code ever"**, and **MUST NOT gate a future adoption on the
  recommendation's stated trigger** — patient-facing verifiability across
  organizations sharing no consortium. The door stays open by his ruling: a
  future change MAY adopt on-chain contract code **on its own merits**, and it
  answers to its own evidence rather than to a condition written here in
  advance.
What becomes of the study's caution: it is RECORDED as ADVISORY CONTEXT for that
  future change, not as a gate on it — the EDPB/HIPAA posture that cleanly
  supports only the off-chain split; the unaudited-stack risk that made Kasplex
  and Igra a refusal in 2026; and the irrevocable-deployment vulnerability class
  that contract code carries. A later author must ANSWER these; a later author
  does not need this topic's permission to answer them differently. The study's
  IF-forced answer — an Ethereum L2 with EAS, explicitly not Kasplex or Igra in
  2026 — likewise survives as advice, not as the only door.
Why the divergence is recorded rather than smoothed: the recommendation asked
  for a "never", and a staging topic that converts a "not now" into a "never"
  has legislated past its own authority. The ruling differs from the
  recommendation in exactly one dimension — DURATION, where it is the LESS
  absolute of the two — and every other word of the recommendation is adopted.
  Encoding a "not now" as a "never" would be the quiet-narrowing defect this
  topic already refused once at Q6, run in the opposite direction.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's clarify ruling)
  · 2026-08-29

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
Disposition status: CONFIRMED 2026-08-29 — Brett Heap, in session; AS
  RECOMMENDED, and this is the ruling's OPERATIVE FORM
Disposition (2026-08-29, CONFIRMED BY BRETT HEAP): the commitment reading is
  confirmed and becomes the 2026-08-27 ruling's OPERATIVE FORM. "Patients put
  PHI portions on chain" means **SALTED KEYED COMMITMENTS** — a verifiable
  public handle to a PHI portion, with the portion itself disclosed OFF-CHAIN
  under an anchored consent checkpoint, and **salt destruction as the erasure
  mechanism**. Literal raw PHI, encrypted PHI and plain-hashed PHI on chain stay
  REFUSED. **No later change re-litigates this**: the reading is no longer an
  interpretation a later author may revisit, it is what the ruling says.
Why the confirmation mattered: this was the one place the topic INTERPRETED a
  ruling rather than applying it, and it narrowed one. The narrowing is now
  authorized at the source, so the patient-facing behaviour the 2026-08-27
  ruling asked for stands whole — patients choose what to share, with whom,
  provably — and only the location of the bytes was ever in question.
Gate: this was one of two TRANCHE-THREE blockers. With Q3 ruled in the same
  sitting, **tranche three is OPEN**.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's clarify ruling)
  · 2026-08-29

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
  attestation actually proves about the runner. The second review round added
  the binding requirement on top: whichever mechanism is chosen, the
  controller corroborates the submitted payload against its own link-4 setup
  attestation rather than notarizing self-report, so the mechanism question is
  about WHERE the key lives, never about whether the claims are checked.
Disposition status: ruled 2026-08-29 — Brett Heap, in session; AS RECOMMENDED
Disposition (2026-08-29, RULED BY BRETT HEAP): as recommended. Attestation
  signatures happen by **REMOTE SIGNING SERVED BY THE HARNESS CONTROLLER**. The
  runner's signing **REQUEST is recorded alongside the signature it received**,
  so the chain shows both what was attested and who asked for the attestation —
  a bare signature shows only the first. The controller **corroborates the
  submitted payload against its own link-4 setup attestation**: it signs, it
  does not notarize self-report. An **HSM remains a later HARDENING of the same
  shape**, not a different answer, so adopting one moves where the key sits and
  changes nothing about what the chain carries.
Gate: this gated **TRANCHE TWO's contract text**, which may now name the
  mechanism. The gate is OPEN.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's clarify ruling)
  · 2026-08-29

## Exit path

OpenSpec change(s), in three tranches, each gated on what actually exists.

**Gate state after the 2026-08-29 clarify sitting.** Tranche 1 was **never
gated** by an open question. Tranche 2 was gated by **Q7**, and that gate is now
**OPEN**. Tranche 3 was gated by **Q3 and Q6**, and both gates are now **OPEN**.
No tranche is held by a question any more. What still holds tranches 2 and 3 is
unbuilt machinery — a different kind of wait, and stated per tranche below so
the two are never confused.

**Tranche 1 — signed ratification + atomic enrollment. Composable TODAY, and
UNGATED.** Links 1–3. Consumes `add-wallet-carried-review-authority`'s realized
issuer anchor and the shipped grant vocabulary — Q1 ruled the presentation INTO
that vocabulary plus a proof-of-possession step, rather than into a new artifact
— and needs no omnigent layer and no chain. Q4 fixed the boundary at links 1–3
and put the signed transparency log inside it. This tranche waits on nothing but
the word to draft it.

**Tranche 2 — harness and runner attestation. Its question-gate is OPEN (Q7).**
Links 4–6 and 10. Its contract text may now NAME the mechanism: remote signing
served by the harness controller, the runner's signing request recorded beside
the signature it received, the controller corroborating the payload against its
own link-4 setup attestation. What remains is machinery rather than a ruling —
the omnigent layer to enforce the precondition, and
`implement-openxpki-install-repo` to issue the controller certificate. Expresses
its certificates in `trust-anchor` vocabulary and its signer identity in
`identity-brokering`.

**Tranche 3 — on-chain anchoring. Both question-gates are OPEN (Q3 and Q6).**
The commitment and anchor layer, plus the permissioned consent plane whose state
roots it anchors. It builds to the RULED configuration rather than to the
study's: **Kaspa first** as the operational witness under its three unchanged
conditions, **Bitcoin via OpenTimestamps aggregation on every anchored item** as
the durability witness, no selectivity and no third chain. It carries the Q2
boundary as contract text with a validator that refuses both payload-shaped
records and unsalted commitments, and Q6's commitment reading as its operative
form. It builds the multi-anchor receipt format FIRST — the receipt is what
makes the anchor choice reversible, and it must carry BOTH witnesses' proofs
from the start; anchoring to a single chain with a bespoke receipt would be the
one-way door this design exists to avoid. What still holds this tranche is the
PKI plane being real, not a ruling.

Sequencing note: the evidence plane of claim 6 — the signed transparency log —
is a **tranche 1** artifact, not a tranche 3 one. The log is the record; the
anchors are late additions to it. Building the log last would mean tranches 1
and 2 had nowhere to write their signed leaves.

Links 7–9 — council review of the signed brief, the chain-validating merge gate,
and the fraud-signal refusal — span tranches: each tranche extends what the gate
validates. **The gate should exist from tranche one validating a short chain,
rather than arriving at the end validating a long one**, so the refusal path is
exercised from the start rather than first tested when it matters most. Q4 ruled
that sequencing on 2026-08-29, so it is settled rather than proposed.

**Closing note — the topic is FULLY RULED.** All seven open questions were ruled
by Brett Heap on 2026-08-29; no tranche is waiting on a clarification any more,
and every disposition above carries its date and its ruling authority.
**Tranche one is draftable on Brett's word.** Its drafting was NOT green-lit in
that sitting, and this fragment does not read "ruled" as "authorized to draft" —
the questions being answered is what makes the drafting possible, not what
authorizes it. The next act is his.

**The word came, 2026-08-29, in a separate act — DRAFTING IS GREEN-LIT.** Brett
Heap authorized the tranche-one drafting in session, after the sitting, and the
two acts are kept apart here rather than merged into one because the sitting's
own record says it did not authorize drafting. Rewriting that sentence to agree
with the later word would delete the distinction the sitting was careful to
draw; recording the authorization beneath it keeps both true. The same ruling
did two further things, and both are recorded where they bind rather than only
here: it COLLAPSED the two parallel tranche-one packets — pull requests #494 and
#495, raised into the same change directory three minutes apart by two sessions
that could not see each other — onto **#495** as the surviving base, with #494's
four hardenings carried across by harvest rather than discarded; and it ADOPTED
**Narrowing A**, which the sitting did not reach.

**Narrowing A, RULED BY BRETT HEAP 2026-08-29 in session: tier 1 is RATIFYING
authority.** The tier model above says tier-1 authority credentials are
"never held by an agent, a runner, or a lane". Read literally that refuses
`wal-agent-mrc-0001` — a REALIZED agent-held wallet backing an active `review`
grant, which this repository runs today — so the literal reading would have made
a shipped artifact nonconformant on the capability's first day. The ruling
narrows the TIER, not the artifact: the human-held constraint binds the
**ratifying** act, agent-held **review** wallets stay lawful, and what a chain
refuses is an agent-held wallet performing a **ratification**. The tier-model
paragraph above is left as written, because it states the constitutional ground
(`access_secrets: false`) correctly and it is the scope of the word "authority"
that was ruled, not the ground. **Narrowing B** — Q1's "rather than a new
artifact" read as *invent no new artifact* — needed no separate ruling: Q1 as
ruled already says no new artifact is created for the presentation.
Dispositioned-by: Claude Opus 5 (session, encoding Brett Heap's in-session
ruling) · 2026-08-29
