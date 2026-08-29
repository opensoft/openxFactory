---
code_surface: openxFactory — A NEW NEUTRAL CONTRACT FAMILY PLUS ITS RUNNING GATE, declared honestly because this tranche is not doctrine-only. `contracts/signed-execution-chain/` gains the chain-inception record (the ratification's signed registration, carrying the chain identity and the reference to the `openxwallet` exercise record that proved presentation), the traveling-contract artifact (the carried form of the signed ratification), the transparency-log leaf record (append-only, signed, hash-linked), and the realization conformance declaration on `trust-anchor`'s declared-shortfall pattern — plus packaged positive AND negative examples for every named refusal, and the canonical `scripts/validate-signed-execution-chain.py`. The GATE is a running check, not a described one: a short-chain verifier over links 1–3 wired as a pull-request check, on the shape `wallet-validation` already proved in this repository (`add-wallet-carried-review-authority` tasks 2.5/2.6 — a workflow file is not evidence; the ruleset state is). Registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut. NO attestation record of any kind, NO controller certificate, NO per-task identity, NO certificate authority, NO key service, NO anchor, NO chain, NO commitment format, NO consent plane — links 4–6 and 10 are the named tranche-two successor and the anchoring layer is the named tranche-three successor, each carrying its OWN code surface. NO second identity, grant, proof-of-possession or certificate vocabulary is defined: link 1's instrument is the SHIPPED `xfactory_wallet_grant` / `xfactory_wallet_grant_exercise` pair consumed at the digest pin, and a new one here would be the collision the staged topic names as its first risk.
target_release: contract-v2.3 — the next additive contract bundle, FRESH-COUNTED at this branch's tip rather than remembered: `contracts/manifest.yaml:3` declares `contract_bundle_version: contract-v2.2` AND `contracts/releases/contract-v2.2.digests.yaml` is a cut inventory in the tree, so v2.2 is spent and v2.3 is next. The number is named because the count was taken here and not carried from an earlier reading — the packet as first filed reasoned from `contract-v2.1`, which #498 had already superseded on the same day, and a `target_release` reasoned from a stale manifest is the defect this line exists to avoid. **It remains ALLOCATED AT REALIZATION BY MERGE ORDER** per `docs/contract-versioning-policy.md`: several changes ride one additive cut, so a sibling reaching the cut first does not renumber this one, and the realization confirms the number against the manifest at ITS tip. THE CLASS IS ADDITIVE and nothing narrows — a new contract family is the versioning policy's "new contracts" case verbatim, no existing schema changes, no consumer pinned at `contract-v2.2` is made non-conformant, and no domain is obliged to adopt a chain.
Status: draft
Proposed: 2026-08-29
Origin: `openxFactory:staging:signed-execution-chain`, EXIT 1 OF THREE — the tranche the staged topic's own `## Exit path` marks "Composable TODAY", and Q4 ruled that boundary on 2026-08-29. The topic was registered 2026-08-27 from Brett Heap's expansion ruling and hardened by five adversarial review rounds on its own pull request (PR #452, squash `6612d323`). Tranches two and three are named successors in this document and NOT drafted here. **THE DRAFTING AUTHORIZATION IS BRETT HEAP'S IN-SESSION RULING OF 2026-08-29**, and it is named precisely because the earlier claim was weaker than the fact required: this packet as first filed cited the 2026-08-28 session-handoff board, which is an orchestrating session's record of direction and not his word, and the clarify sitting's own closing note says in terms that the sitting did NOT green-light the drafting. He gave the green-light separately, in session, on 2026-08-29, in the same ruling that collapsed pull requests #494 and #495 onto this one and adopted Narrowing A. Nothing else is authorized by it — not the requirement text, not the vocabulary act, not `target_release`, and above all not ratification.
---

# Proposal: add-signed-execution-chain

**THIS DOCUMENT IS NOT RATIFIED. THE CLARIFY ROUND IT USED TO WAIT ON HAS
HAPPENED.** Brett Heap ruled all seven of the staged topic's open questions on
**2026-08-29** in a clarify sitting, landed as pull request **#499** (squash
`9c501df6`), and this packet is amended to those rulings rather than flagging
them. Q1 — the only one this tranche's own text depended on — was ruled AS
RECOMMENDED and is encoded as ruled in requirement 1. Q4 ruled tranche one's
boundary and its two sequencing facts, which this packet already met. Q2, Q3,
Q6 and Q7 govern the later tranches: they are RECORDED here and **pre-encoded
nowhere** — this packet names no chain, no anchor, no commitment format and no
contract-code posture.

**Ratification is a separate act and is Brett Heap's.** `tasks.md` §2 carries it
as an open box. What he HAS given, on 2026-08-29 in session, is the DRAFTING
GREEN-LIGHT the sitting deliberately withheld, together with the ruling that
collapsed two parallel packets onto this one and the ruling that adopted
Narrowing A. Those three acts are recorded in this document where each binds.

## Why

**The family already signs the decision, and then loses the signature.**
`add-wallet-carried-review-authority` made review authority a wallet-carried
grant with a root issuer anchored to a named operator, and S2 realized it: the
validator refuses a review-class grant that names no `issued_by`, refuses a root
grant naming an agent as issuer, and the first live root grant
`governance/review-authority/grants/grant-mrc-0001.yaml` roots in the anchored
operator under the Human Escalation Contract. That is a signed ratification.
What happens next is unsigned. The work runs in a lane that cannot prove it
descended from that ratification, and the merge gate that lets it land cannot
ask.

**The inversion that makes this worth doing is that a validated chain is not an
audit trail — it is a permission.** An audit trail is written after the fact and
can be forged after the fact. A chain the gate WALKS before it permits the
terminal act cannot be forged after the fact, because the act does not happen
without it. The record and the control become the same object, which is the
property this repository keeps discovering it needs and keeps having to add
afterwards.

**The forcing fact is not hypothetical.** openxFactory issue **#351** landed a
reversion of ratified canon that passed `openspec validate --strict`, passed CI,
and passed a three-bot review lane; **#357** generalizes it into an open
validator gap. Every one of those gates asked *is this well-formed?* None of
them could ask *whose ratification is this work descended from, and does that
ratification permit it?* — because nothing carried the answer.

**And the neutral-layer argument is that the same shape occurs twice in two
domains.** MedxFactory's HealthLinc ratifies, simulates, reviews and "merges" a
treatment plan, where merge means pushed to the patient app or printed as signed
orders; LedgerxFactory's LedgerLinc runs the same chain over an analysis and
publishes. They differ in payload and regulator, not in chain. A family that fit
one domain would belong in that domain's repository.

## What this change is — TRANCHE ONE, and its boundary is the point

Tranche one's scope is **RULED**, not proposed. Brett Heap ruled **Q4** on
2026-08-29 AS RECOMMENDED — *"Tranche one is links 1–3 ONLY"* — and ruled two
sequencing facts with it, both of which this packet already met and now cites as
rulings rather than as the topic's instruction:

- **Links 1–3** — the wallet-presented ratification, the atomic
  ratified⇒chain-incepted act, and the traveling contract.
- **PLUS the signed transparency log, a TRANCHE-1 artifact BY RULING.** Q4's
  disposition: *"the **signed transparency log is a TRANCHE-1 artifact**, because
  tranches 1–2 need somewhere to write their signed leaves."* The log is the
  record; the anchors are late additions to it, and building the log last would
  leave tranches one and two nowhere to write.
- **PLUS the gate, existing FROM TRANCHE ONE and validating a SHORT chain, BY
  RULING.** Q4's disposition: *"the **chain-validating gate exists FROM TRANCHE
  ONE**, validating a short chain, so the refusal path is exercised from the
  start rather than first tested when it matters most."* This is why the packet
  ships a running gate rather than refusal semantics alone — the difference is
  now a ruling and not a judgement call.

**Named successors, NOT drafted here:**

- **Tranche two — `add-signed-execution-chain-attestation`** (working id): links
  4–6 and 10, the harness-controller setup attestation, per-task attestation
  identities, the signed PR-open decision and the governed post-merge test. It
  needs the omnigent layer to enforce the precondition and
  `implement-openxpki-install-repo` to issue the controller certificate. **Its
  Q7 gate is OPEN** — ruled 2026-08-29 as remote signing served by the harness
  controller, with the runner's signing request recorded beside the signature it
  received and the controller corroborating the payload against its own link-4
  setup attestation — so what remains for tranche two is MACHINERY, not a
  ruling. None of that mechanism is named in this packet's delta.
- **Tranche three — `add-signed-execution-chain-anchoring`** (working id): the
  commitment and anchor layer plus the permissioned consent plane whose state
  roots it anchors. **Both its question-gates are OPEN** — Q3 and Q6 were ruled
  on 2026-08-29 — so what holds tranche three is the PKI plane being real, not a
  ruling. The ruled configuration is recorded in the staged topic and is
  **deliberately absent from this packet's delta**: tranche one places nothing on
  any chain, so it names no chain, no witness ordering and no receipt format.

**Neither successor's content appears in this change**, and no requirement here
may be read as authorizing it.

## The two convening-derived constraints

Both come from the `gate_rules_council` convening record
`opensoft/codexFactory` →
`hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`
(unanimous 5/5; convener disposition §8, Brett Heap, 2026-08-28). They are not
background: each one bounds a requirement in this change's delta.

### Constraint A — the chain-inception act is OUT-OF-PIPELINE, by proven necessity

**A class over `openspec/changes/**` can never commission a council.** That
surface is a member of the canonical `GATE_INTEGRITY_FLOOR`, the PR-time floor
is evaluated **before** any clearable classification, so every candidate returns
`parked_never_clearable` and `council-convening-lane.yml:1022-1026` bails on
exactly that outcome. **Measured on openxFactory's real tree: 984 admitted
paths, 984 floored, 0 remaining.** And it is **code-level, not
document-level** — the record's own reproduction shows `gate_integrity`
declared, `gate_integrity` absent, and **no rule document at all** all parking
identically, with reasons byte-identical. CPL's sentence is the sharpest form:
*"No edit to this rule document — none — can make this class ever reach
classification."*

**This change's own ratification and chain inception land on
`openspec/changes/**`.** So the enrollment mechanism cannot be the clearance
pipeline — not by preference, but because the pipeline provably cannot reach it.
The inception act is therefore performed OUT-OF-PIPELINE and the delta says so
in requirement text, citing this record. A design that routed inception through
the envelope would be describing a control that cannot run, which is the LS-A3
failure this family has now named three times.

**And the measurement is not the whole ground.** 984/984/0 covers the surface
this repository's ratifications land on; the rule itself is not
surface-dependent, because **a pipeline that CLEARS candidates cannot also be
what CONFERS the authority those candidates are cleared against.** A chain whose
first link is minted by the mechanism it exists to permit is circular on any
surface, floored or not. The measurement makes the rule unarguable here; the
circularity makes it correct everywhere, and both are in the requirement.

### Constraint B — link 7 composes with the §7.4 path, not with the clearance envelope

The convener's ruled continuation is *"the council-reviewed-but-human-approved
path, which per the 2026-08-26 record §7.4 needs no class and no flip"* — and
that path *"reaches this repository without an envelope and without amending
FR-008"*. Link 7 (council review with the signed proposal as the brief) is
therefore expressed, in its short-chain tranche-one form, as **a signed review
of the traveling contract on the §7.4 path**, and NOT as an envelope entry, a
candidate class, a flip, or a soak threshold. **This change creates no
`merge-approval-envelope` instance and defines no candidate class**, and
`specs/025-openxfactory-review-lane-caller/spec.md`'s FR-008 is left exactly
where the convening left it: gated, task 3.2 open, undischarged.

## The vocabulary act — `chain inception`, and why it is not `enrollment`

**025 already owns "enrollment" in this repository**, for a different act: FR-008
reads *"The caller MUST declare no enrolled candidate class"*, and the word there
means **the entry of a candidate class into a `merge-approval-envelope`** so the
codexFactory decision core may classify and possibly clear it. A second, adjacent
sense of "enrollment" landing in a neighbouring capability is precisely the
second-vocabulary invention the 2026-08-28 seats named as the live risk — and it
would be worse than a normal collision here, because both words would sit on the
same pull requests, in the same repository, one week apart. The family already
carries a THIRD sense in `add-worker-enrollment-broker`, which is the proof the
word is loaded rather than free.

So this capability does not take the word at all. **The pair, stated once and
carried in requirement text:**

| This capability's act | 025's act |
| --- | --- |
| **`chain inception`** — the ratification's registration into the signed-execution-chain registry, performed in the SAME signed act as the ratification, minting the **chain identity** (the digest of the signed ratification) that every later link binds to | **candidate-class enrollment** — 025 FR-008's *"enrolled candidate class"*: the entry of a class into a `merge-approval-envelope` for the codexFactory decision core to classify |

**The non-collision, stated explicitly rather than left to inference:** chain
inception creates no envelope, names no candidate class, touches no ruleset,
produces no verdict, and changes nothing FR-008 governs; and 025's enrollment
mints no chain identity, signs nothing, and is not a link in any chain. **The
two appear together ONLY where they are being told apart** — here, in the
inception requirement's body, and in that requirement's fourth scenario — and
never as alternatives to one another, which is the property that matters. (This
sentence first read "the two never appear in the same sentence except this one",
which the packet's own spec text falsified the moment it stated the distinction
in requirement form; a review round caught it. The claim was rhetoric standing
where a precise one belonged.) The delta states the
non-collision in the requirement that owns the act, so a reader who arrives at
the spec without this proposal still finds it (`## ADDED Requirements`, the
inception requirement's body and its fourth scenario). The staged topic's own
prose calls link 2 "ratified ⇒ enrolled"; **this change renames that act on
purpose**, and the rename is recorded in `design.md` D1 so the topic's wording
and this spec's wording are never read as two different acts.

## Capabilities

### New Capabilities

- `signed-execution-chain`: the neutral tranche-one chain, **NINE ADDED
  requirements over 41 scenarios**, no `## MODIFIED Requirements` block anywhere
  — a ratification admitted only on wallet-carried authority PROVEN BY POSSESSION
  in the shipped `openxwallet` vocabulary and BOUND to the exact ratification;
  the recorded ACTOR bound to the wallet that signed, in the direction the pinned
  subject-attestation contract fixes; ratification and chain inception as one
  signed act, performed out-of-pipeline, so a ratified-but-uninscribed state is
  constructively impossible and re-ratifying an unchanged subject cannot silently
  reproduce an existing chain; ONE digest construction governing every digest the
  capability computes; the signed ratification as a TRAVELING CONTRACT checkable
  at the point of use; an append-only signed transparency log as THE RECORD, with
  its one uncovered residual declared rather than papered over; a gate that
  validates links 1–3 as a HASH-LINKED chain and refuses a break as a fraud
  signal rather than reporting it as a warning; tier-1 RATIFYING authority held
  by a human, never by an agent, runner or lane, per Brett Heap's Narrowing A
  ruling of 2026-08-29; and the rule that none of it confers or refuses anything
  until a named reader runs as a REQUIRED check.

### Modified Capabilities

**None.** No promoted requirement is restated or replaced, and this change
carries no `## MODIFIED Requirements` block anywhere. That is deliberate: every
adjacent capability this composes with is either still an ACTIVE change whose
ratified text governs (`add-wallet-carried-review-authority`, `add-trust-anchor`,
`add-identity-brokering`) or a promoted spec this change has no cause to move
(`roles-authority-model`, `credential-contracts`, `workflow-gate-contract`).
Composing by reference is the staged topic's own instruction and the condition
under which its Conflicts table admits this tranche at all.

## Impact

- **New code (this change authorizes; realization is a later commission)**: one
  contract family, packaged positive and negative examples, one canonical
  validator, the append-only log store, one required pull-request check, and
  manifest / CHANGELOG registration at the next additive bundle.
- **Consumes, and does not re-invent** — the composition target, cited at the
  artifacts that actually shipped rather than at the change that promised them:
  - `contracts/openxwallet-pin.yaml` pins `opensoft/openXwallet` at
    `6b248d4050e1f88b3ca75c1290ad2c81f465300c` (`wallet-v1.3`), digest
    `fde433c5…` for `contracts/openxwallet/openxwallet-grant.schema.yaml` and
    `f16ad312…` for `contracts/openxwallet/openxwallet-grant-exercise.schema.yaml`.
    **The exercise record is link 1's instrument and it already exists**: it
    requires `proof_of_possession`, distinguishes `verification_failure` from
    `unauthenticated_request` by `event_class`, and its closed refusal
    enumeration already names `missing_proof_of_possession` separately from
    `missing_grant`, because *"the grant was supplied and is not what was
    lacking"*.
  - `governance/review-authority/grants/grant-mrc-0001.yaml`,
    `.../register.yaml`, `.../wallets/wal-agent-mrc-0001.yaml` and
    `.../attestations/custody-attest-wal-agent-mrc-0001.yaml` — the realized S2
    issuer anchor, the register and its reader, and the first wallet, all read
    inside the REQUIRED `wallet-validation` check (org ruleset **21538893**).
  - `add-trust-anchor`'s ratified declared-custody rule — custody bounds what a
    signature evidences — which is what makes requirement 8's ruled narrowing
    exact rather than assertive.
- **Composes with, and is bounded by**: `specs/025-openxfactory-review-lane-caller/spec.md`
  FR-008 (untouched, still gated), the 2026-08-28 convening record (both
  constraints above), and `omnigent-domain-overlay`'s constitutional
  `access_secrets: false`.
- **Obliges no domain.** No domain must adopt a chain, and no existing
  capability is modified in a way that requires action from a domain that has
  none. MedxFactory/HealthLinc and LedgerxFactory/LedgerLinc are named as the
  neutrality proof, not as consumers under obligation.

## Where the staged topic and a ratified artifact pulled against each other — BOTH SETTLED

Recorded rather than smoothed, on this family's contested-finding rule. Both
were raised as narrowings; **both are now settled, and neither is settled by
this packet's own authority.**

**1. NARROWING A — "Tier 1 … never held by an agent" versus a realized
agent-held wallet. RULED BY BRETT HEAP, 2026-08-29, IN SESSION.** The topic's
tier model says authority credentials are never held by an agent. But
`wal-agent-mrc-0001` is a REALIZED wallet whose holder is
`agent:merge-readiness-council`, custody model `holder_readable`, backing an
active `review`-act grant — shipped, validated, and register-backed. Read
literally the topic refuses an artifact this repository already runs.
**He ruled that tier 1 is RATIFYING authority**: agent-held REVIEW wallets stay
lawful, and what a chain refuses is an agent-held wallet performing the
RATIFYING act. Requirement 8 is written to that ruling.

*The 2026-08-29 clarify sitting did not reach this narrowing* — it took the
seven questions and nothing else, and `#499` touches neither the tier model nor
either narrowing. So it was put to him separately and ruled separately, and this
document says so rather than letting a reader infer that the sitting covered it.
The ruling also costs nothing in strictness: `holder_readable` custody evidences
that the HOST acted, which under `add-trust-anchor`'s ratified custody rule is
exactly what a ratification may not stand on, so the review wallet could never
have carried a ratifying grant anyway. **The ruling removes a false refusal
without creating a real permission.**

**2. NARROWING B — Q1's "rather than a new artifact" versus a shipped record kind
for exactly this act. SETTLED BY Q1'S OWN RULING, 2026-08-29.** Q1's recommended
answer said to record the presentation *"in the ratification record rather than a
new artifact"*, while the family already HAS an artifact for it —
`xfactory_wallet_grant_exercise`, shipped at `wallet-v1.3`. This packet read that
as **invent no new artifact**, honoured by REFERENCING the shipped exercise
record. **Q1 was ruled AS RECOMMENDED and its disposition says in terms that "no
new artifact is created for it"**, which is that reading in the ruling's own
words — so Narrowing B needed no separate act and gets none. The reading is no
longer flagged on requirement 1.

## The collapse of two parallel packets, and what was carried across

**Two sessions raised this same tranche into the same change directory three
minutes apart** — pull request **#494** (`change/add-signed-execution-chain`,
08:55:44Z) and this one, **#495** (08:58:21Z) — neither able to see the other.
Both were authored before the seven rulings landed. **Brett Heap ruled the
collapse on 2026-08-29 in session: #495 is the surviving base and #494 is
closed.**

The deciding ground was **Q4**, and it is worth stating because it is a ruling
and not a preference. #494 deliberately shipped **no gate** — its proposal says
*"the packet creates no merge gate"*, and one of its requirement scenarios is
normatively against the claim, requiring that any statement that a gate validates
chains "is corrected". Q4 then ruled that **the chain-validating gate exists FROM
TRANCHE ONE**. Conforming #494 would have meant reversing its thesis, three
recorded design decisions and a normative scenario; this packet already carried
the gate, argued from the same convening record, and drew the line #494 collapsed
— **out-of-pipeline INCEPTION and a required-check GATE are different objects**,
and only the first is what the 2026-08-28 seats refused.

**#494 was ahead on hardening, and none of it is discarded.** Four Codex rounds
and five Copilot rounds ran on it and closed thirteen findings. **Four are
harvested into this packet's delta**, cited here so the work is provably carried
rather than lost with the branch:

| Harvested from #494 | Lands as |
| --- | --- |
| **The actor↔wallet attestation binding** — a link could reference one holder's valid exercise and record a different well-formed subject, with every other check passing. The binding direction is taken from the pinned contract: `openxwallet-subject-attestation` closes `resolution.resolved_by` to `subject_ref`, so a wallet is checked as an ATTESTATION and never resolves a subject | Requirement 2 (new) |
| **Per-ratification uniqueness, ENFORCED and not merely named** — the identity is the digest of the signed bytes, so re-ratifying an unchanged subject reproduces them; naming the exercise identifier as the per-act value is necessary and not sufficient, because the pinned schema constrains no reuse | Requirement 3, two new scenarios |
| **ONE digest construction governing EVERY digest** — identity, predecessor, leaves, and any a later tranche adds; declared once in the contract. #494 met this defect twice, once per digest, and unified rather than adding a second rule | Requirement 4 (new) |
| **The named-reader required-check rule** — the capability confers nothing until a named validator runs as a REQUIRED check, and a merged workflow file is not that. Carried explicitly rather than inherited by implication from `review-authority-intake` | Requirement 9 (new) |

**What was NOT harvested, and why.** #494's requirement that every link sign the
chain identity and its predecessor's digest is not carried as written: this
packet's gate requirement establishes that inception cannot sign over an identity
derived from its own signature, and that link 3 has no signer at all, so at
tranche one continuity is established by derivation and comparison and the
hash-linked SIGNING rule takes effect at tranche two's first signed link. Taking
#494's formulation would have imported a rule that cannot be performed on any
link this tranche defines.

## What the review rounds corrected, before ratification

Five P1 findings across two bot rounds on this proposal's own pull request, all
real, all of the same shape — a rule naming something it could not actually do.
Recorded here rather than silently patched; the full reasoning is `design.md`
D7. **The second round falsified the first round's fix twice**, which is the
finding worth carrying forward on its own: a repair authored against the
vocabulary one REMEMBERS rather than the vocabulary one RE-READS reproduces the
defect it is repairing. Both relapses were exactly that — one equated an enum
selector with a digest value, the other handed a signing duty to a link the
authoritative table gives no signer.

1. **A reference is not a binding.** Requirement 1 had the ratification record
   merely REFERENCE the exercise. The shipped schema makes `object_ref` optional
   and carries no digest of the thing approved, so **a previously successful
   exercise could be REPLAYED as the proof for a different ratification** and
   pass every stated check. **The first repair was itself unenforceable** — it
   equated `signed_over`, an enum selector holding no digest, with a digest
   value the pinned schema cannot represent. The digest now lives where a digest
   can live: `object_ref` carries the ratification's content digest in the
   shipped identifier grammar, so the comparison is recomputable. The step from
   "the record names this ratification" to "the signature covers it" is **raised
   as an explicit gap**, with the durable repair named as an openXwallet
   successor field — defining it here would mint the second proof vocabulary the
   requirement exists to avoid.
2. **The chain identity could not be signed by the act that mints it** — and
   then **the traveling contract could not sign either, because link 3 has no
   signer** (`— (carried)` in the authoritative table). At tranche one there is
   no link after inception with a signer at all, so continuity is established by
   **derivation and comparison** rather than a third signature, and the
   hash-linked SIGNING rule is declared to take effect at tranche two's first
   signed link. The staged topic's "from enrollment onward" carries both defects
   and is corrected on both counts.
3. **Deletion detection was promised at a strength this tranche cannot
   deliver.** A store that drops its newest leaves and presents an earlier valid
   signed tree head shows a shorter log that verifies perfectly. The guarantee
   is now stated at its real strength, and the residual is DECLARED under the
   realization-conformance obligation — `add-trust-anchor`'s ratified rule
   applied to ourselves — with tranche-three anchoring named as what closes it.

## The seven questions — ALL RULED 2026-08-29, and what each means here

Brett Heap ruled all seven in a clarify sitting on 2026-08-29, landed as **#499**
(squash `9c501df6`). This packet carries no clarify round of its own; the table
records what each ruling means for THIS tranche. **Four of the seven govern later
tranches and are pre-encoded nowhere in this delta** — recording a ruling is not
building to it.

| Q | Ruling (2026-08-29) | Bearing on THIS change |
| --- | --- | --- |
| **Q1** wallet presentation | **AS RECOMMENDED** — the shipped grant vocabulary plus a proof-of-possession step, recorded in the ratification record itself; no new artifact | **Encoded as ruled** in requirement 1; the flag is struck. Narrowing B is settled by this ruling's own words |
| **Q2** on-chain boundary | AS RECOMMENDED — salted keyed commitments, consent-checkpoint commitments and anchors on chain; every payload, consent state and the salts off chain; a validator refusing payload-shaped records AND unsalted commitments | **Tranche three.** Nothing here places anything on any chain, so no boundary is drawn and none is pre-empted |
| **Q3** which chain | **DIVERGES from the recommendation, in two rounds** — Kaspa FIRST as the operational witness, Bitcoin-via-OpenTimestamps on EVERY anchored item as the durability witness; no selectivity, no third chain | **Tranche three, and NOT pre-encoded.** This delta names no chain, no witness, no ordering and no receipt format. Its transparency-log requirement states positively that the log's standing does not depend on any external witness, which is the shape the ruling assumes |
| **Q4** tranche boundaries | AS RECOMMENDED — **tranche one is links 1–3 ONLY**, with the **signed transparency log a TRANCHE-1 artifact** and the **chain-validating gate existing FROM TRANCHE ONE** validating a short chain | **Directly governs this packet, and it already conformed.** Links 1–3, the log (requirement 6) and the short-chain gate (requirement 7). The scope section now cites the ruling rather than the topic's instruction |
| **Q5** contract code or an L2 | **OVERRIDES the recommendation** — *"allow contract code later."* Evidence-only stays today's posture; the change **MUST NOT constitutionalize "no contract code ever"** and **MUST NOT gate a future adoption on any trigger condition written in advance** | **Complied with by silence, deliberately.** This delta contains no contract-code posture, no "never", and **no trigger condition** — see below |
| **Q6** PHI portions on chain | **CONFIRMED as recommended, and it is the ruling's OPERATIVE FORM** — salted keyed commitments, the portion disclosed off-chain under an anchored consent checkpoint, salt destruction as erasure; no later change re-litigates it | **Tranche three.** This packet defines no commitment format and touches no PHI |
| **Q7** where an attestation signature happens | AS RECOMMENDED — remote signing served by the harness controller, the runner's signing request recorded beside the signature, the controller corroborating against its own link-4 setup attestation | **Tranche two.** This packet contains no attestation link at all |

### Q5 needs a positive statement, not just an absence

Q5's ruling has a REFUSAL in it that a packet can breach by writing too much, so
this one states its compliance rather than leaving it to be inferred. What Q5
preserved is the posture — the anchoring chains stay evidence-only today, and no
tranche now planned puts contract code on any of them. What it REFUSED is the
permanence the recommendation asked for.

**This change therefore does three things and no more.** It puts no contract
code anywhere, because tranche one touches no chain. It writes **no "never"** —
there is no requirement, scenario or design note in this packet forbidding
on-chain contract code in a future change. And it writes **NO TRIGGER
CONDITION**: the recommendation would have gated any future adoption on
patient-facing verifiability across organizations sharing no consortium, and the
ruling refuses that gate, so this packet names no condition under which contract
code would become admissible. **A later change may adopt on-chain contract code
on its own merits and answers to its own evidence, not to anything written
here.** The study's cautions — the EDPB/HIPAA posture, the unaudited-stack risk,
the irrevocable-deployment vulnerability class — survive as ADVISORY CONTEXT that
a later author must answer, never as this packet's permission to withhold.

*Recorded because the earlier draft of this section got it wrong in the ruling's
own direction:* it described Q5 as open with "the trigger condition still to be
stated", which is exactly the sentence the ruling forbids. The correction is left
visible rather than smoothed, on the same footing as the review-round corrections
above.

## Ratification

**Not ratified.** Ratification is Brett Heap's act; `tasks.md` §2 carries it as
an open box, and this pull request asks for review of the packet rather than for
ratification.

**What he HAS ruled, 2026-08-29, all in session and all recorded above:** the
seven clarify questions (#499); the DRAFTING GREEN-LIGHT, which the sitting
deliberately withheld and which is the authority this packet now cites for its
own existence; the COLLAPSE of #494 and #495 onto this packet; and NARROWING A.
None of those four is a ratification, and this document does not read any of them
as one.

Ratification would authorize exactly one Speckit contract feature plus its gate,
and would create no certificate authority, no attestation identity, no anchor, no
chain, and no runtime beyond the validator and the pull-request check named in
`code_surface`.
