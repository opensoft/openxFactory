# Council Convening Packet (§7.4 sitting), 2026-08-30: openxFactory PRs #510, #513 and #509

Status: record
Record scope: convening packet
Council: `gate_rules_council` (codexFactory
  `hermes/domain/review-councils/gate-rules.yaml`), sitting in the **§7.4
  no-class shape**, exactly as the 2026-08-29 sitting on PR #497 did. That
  seating is a **convener act SANCTIONED PENDING A CHARTER AMENDMENT** (record
  `2026-08-29-council-review-add-binding-consumer-identity.md` §8.3; the
  amendment rides codexFactory issue **#131**). It is disclosed here rather
  than assumed, and it is put to the bench again as **T-0**.
Convened: 2026-08-30
Convener: orchestrating session, on Brett Heap's instruction. **The convening
  pushes nothing, merges nothing and ratifies nothing.** Its whole output is a
  ballot for Brett Heap to rule on.

Subjects — THREE, in one sitting:

| # | PR | Branch | Head | Kind |
|---|---|---|---|---|
| 1 | **#510** | `change/add-chain-attestation` | `e7f6ae0e400719894fbaa0d14be274ba86b2e3b3` | OpenSpec proposal packet — tranche TWO, links 4–6 + 10 |
| 2 | **#513** | `change/add-chain-anchoring` | `cf5a24b89870a87663c595550210ee4deb0ac28e` | OpenSpec proposal packet — tranche THREE, a NEW capability |
| 3 | **#509** | `change/vendor-medxchain-brainstorm` | `26c7e778682089789795befad4c28af509ff2706` | A vendoring of Brett Heap's MedxChain notes into `ideation/brainstorm/` |

Judged at:

```
openxFactory origin/main                afe29561a317853eb22f1e6b248f7029fa2fb2a7
shared merge-base of all three PRs      b710976b4a4fef277cdd292a407942369e9b9efa
PR #510 head                            e7f6ae0e400719894fbaa0d14be274ba86b2e3b3
PR #513 head                            cf5a24b89870a87663c595550210ee4deb0ac28e
PR #509 head                            26c7e778682089789795befad4c28af509ff2706
codexFactory (the council's own contract, read-only)
                                        3c71ddc910b8e0b119d0e1ee40a5523dfa294f07
contracts/manifest.yaml:3 on main       contract_bundle_version: contract-v2.2
```

Precedents this packet mirrors:

* codexFactory `records/2026-08-29-council-review-add-binding-consumer-identity.md`
  and its ballot and seat-return appendix — **the PRIMARY precedent**: same
  repository, same §7.4 path, ruled by Brett on 2026-08-29.
* codexFactory `records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`
  and its ballot — the packet/return/ballot SHAPE and the independence
  discipline.
* codexFactory `records/2026-08-26-gate-rules-classification-intent.md` §7.4 —
  the *"council-reviewed-but-human-approved path, which needs no class and no
  flip"* this sitting executes.

---

## 0. WHAT THE CONVENER MUST KNOW BEFORE READING ANYTHING ELSE

### 0.1 THIS COUNCIL'S CHARTERED SCOPE DOES NOT LITERALLY COVER THESE SUBJECTS

`gate-rules.yaml` declares `scope: per_repository_rule_setting` and
`purpose: "what are the merge/gate rules for this repo?"`. **This sitting sets
no rule.** It reviews three pull requests.

The identical mismatch was disclosed at the 2026-08-29 sitting, put to that
bench as its Decision 4, and ruled: the seating is **SANCTIONED as a convener
act, pending a charter amendment** which "rides the next codexFactory council
change" and is tracked as codexFactory issue **#131**. That amendment has not
landed. **So this sitting stands on a sanction, not on a charter**, and the
sanction was given for a sitting over ONE proposal — not three subjects at once.
**T-0 puts that squarely to the bench.**

### 0.2 THE THRESHOLD STRUCTURE — #510's Q4 QUESTION IS DECIDED FIRST, AND A RULING THERE CAN END #510's ROUND

This is not the convening's ordering. **It is #510's own text**, at
`tasks.md:88-92`:

> 2.2 The sitting rules FIRST on **Q4's re-derivation instruction versus
> drafting tranche two before the omnigent layer and the PKI plane are real**
> (`design.md` D7; `proposal.md`, first substantive section). **A ruling that the
> packet is premature ends the round; nothing below it survives.**

The instruction it is measured against is a **ruled disposition of Brett
Heap's**, 2026-08-29, at
`ideation/staging/signed-execution-chain/signed-execution-chain.md:673-681`:

> Disposition (2026-08-29, RULED BY BRETT HEAP): as recommended. **Tranche one is
> links 1–3 ONLY.** The later boundaries are RE-DERIVED when the omnigent layer
> and the PKI plane are real, not fixed now — **a boundary drawn against an
> unbuilt layer is a guess wearing a tranche number.**

**Neither the omnigent layer nor the PKI plane is real.** #510 says so itself and
carries the obligation forward as a realization gate rather than discharging it
(`tasks.md:127-131`):

> 5.1 **[GATE] Re-derive the tranche boundary against what actually exists** when
> the omnigent layer and the PKI plane are real, per Q4's ruling. **This
> obligation survives ratification deliberately: a packet cannot discharge it,
> because it is an obligation about a state the packet cannot observe.**

**The counter-text is in the same ruled topic**, at its `## Exit path`
(`:829-837`), and it is why this is a genuine question rather than a formality:

> **Tranche 2 — harness and runner attestation. Its question-gate is OPEN (Q7).**
> Links 4–6 and 10. **Its contract text may now NAME the mechanism** … What
> remains is **machinery rather than a ruling** — the omnigent layer to enforce
> the precondition, and `implement-openxpki-install-repo` to issue the controller
> certificate.

So the ruled record contains BOTH: an instruction to re-derive boundaries when
the machinery is real, AND an exit path saying tranche two's contract text may
now be written and what remains is machinery. **The bench is asked which of those
governs the act of DRAFTING tranche two's requirement text today.** T-1 states
the options.

**T-1 is ruled before anything else about #510.** It does **not** bind #509 or
#513: a premature ruling on #510 ends #510's round *without prejudice to the
other two subjects*.

### 0.3 THREE SUBJECTS IN ONE SITTING, AND WHAT THAT RISKS — DISCLOSED

Every §7.4 precedent sat over ONE object. This sitting sits over three, of which
two are 1,700–1,900-line proposal packets and one is a 223-line brainstorm
vendoring. **The convening states the hazard against its own interest:**

1. **Attention is not divisible without loss.** A seat that reads three subjects
   in one pass reads each of them less well than a seat that reads one. The
   2026-08-29 sitting's decisive finding was reached by BUILDING a schema; that
   depth is what a three-subject load threatens.
2. **The two chain packets are sequential in substance.** #513 composes on #510,
   which is neither merged nor ratified. Reading them together risks a seat
   treating #510's text as settled while judging #513.
3. **#509 is a different kind of object entirely** and its review questions
   (provenance fidelity, no invented claims) share nothing with the other two.
   It is included because it is small, not because it belongs.

**Mitigation, and it is only partial:** the return format demands PER-SUBJECT
verdicts, each with its own grounds; a seat may return **PARK** on any single
subject for want of capacity and say so, and that is a legitimate return, not a
failure. **A seat that cannot read all three properly should say so rather than
thin its reading across them.** T-0 asks the bench whether the combination was
lawful at all.

### 0.4 THE CONVENING'S OWN FINDING, REPRODUCED BEFORE IT WAS RECORDED: #510 SAYS "TWELVE SCENARIOS"; THERE ARE NINE

**This is the convening's finding, not a seat's, and it is labelled as such.** It
is put in §0 because it bears directly on ballot item **B-2**, where a seat is
asked to weigh ADDED against a MODIFIED restatement, and the packet quantifies
the cost of the alternative.

#510 asserts at **four sites** that a scenario-complete MODIFIED restatement of
tranche one's gate requirement would carry **twelve** scenarios:

```
design.md:114   "Restating it would also cost twelve scenarios of verbatim carry"
design.md:124   "all twelve scenarios, not the two that change"
tasks.md:99     "all twelve scenarios, not the two that change"
proposal.md:243 "all twelve scenarios, not the two that change"
```

Measured at `origin/main` `afe29561`, and again at PR #510's own head
`e7f6ae0e` (the two copies of the file are byte-identical — `git diff` over
`openspec/changes/add-signed-execution-chain/` between the two returns empty):

```
$ python3 - # count '#### Scenario:' per '### Requirement:' block
  openspec/changes/add-signed-execution-chain/specs/signed-execution-chain/spec.md

    5  scenarios= 6   Ratification presents wallet-carried authority, proven by possession
  103  scenarios= 4   The actor a chain records is bound to the wallet that signed
  151  scenarios= 6   Ratification and chain inception are one signed act
  241  scenarios= 5   One digest construction governs every digest this capability computes
  305  scenarios= 3   The signed ratification travels with the work
  337  scenarios= 4   The signed transparency log is the record
  391  scenarios= 9   A gate validates the short chain as a hash-linked chain   <-- THE SUBJECT
  557  scenarios= 4   Ratifying authority is human-held
  613  scenarios= 4   The capability confers and refuses nothing until a named reader runs as a required check
TOTAL requirements: 9   TOTAL scenarios: 45
```

**The gate requirement carries NINE scenarios. No requirement in tranche one
carries twelve, and the whole delta carries forty-five.**

Stated precisely, and against the convening's own temptation to overstate it:
the number does not decide B-2, and D3's *quotations* from tranche one were
checked and are **accurate** (`"at this tranche"`, `"a later tranche"`, `"does
not exist yet"` and `"is not reported as a break"` all resolve, and the scenario
headed *"a tranche-two link does not exist yet"* exists at
`spec.md:161`). What the number does is **inflate by a third the cost of the
alternative the packet is arguing against**, in the one paragraph where that cost
is the argument. A seat weighing ADDED-versus-MODIFIED is entitled to the real
figure. **Seats should verify this themselves rather than take it from here.**

### 0.5 ALL THREE BRANCHES ARE BEHIND MAIN, AND WHAT MAIN GAINED ROUTES A RULED QUESTION INTO THIS VERY FAMILY

All three PRs share merge-base `b710976b`. `origin/main` is `afe29561`. The three
commits between them are one thing:

```
$ git diff --stat b710976b origin/main
 .../add-wallet-carried-review-authority/AGENTS.md   |   4 +-
 .../research/README.md                              |   6 +-
 .../rulings-2026-08-29.md                           | 228 +++++++++++++++++++++
 .../add-wallet-carried-review-authority/tasks.md    |  29 +++
```

That new file records **Brett Heap's S5 rulings R1–R12 of 2026-08-29**, and
**R12 routes an attestation question into the signed-execution-chain family**
(`openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-29.md:191-199`):

> 12. **R12 — Attestation-envelope SIGNER: DEFERRED to the
>     signed-execution-chain change** (staged; PR #452). Composition digests MAY
>     be recorded UNSIGNED in the register in the meantime … **The per-seat
>     Ed25519 keys minted 2026-08-28 are NOT to be used for self-attestation: a
>     holder signing its own composition attests nothing an independent party can
>     rely on.** Report §5's remaining envelope questions — **standard, key
>     distribution, signature algorithm, evidence-retention location** — travel
>     with that change.

**Neither #510 nor #513 cites R12, the rulings file, or the S5 envelope
questions.** Verified by grep over both packets' `proposal.md`, `design.md`,
`tasks.md` and `.openspec.yaml`: `#510` cites
`add-wallet-carried-review-authority` five times, always for its *review-authority
vocabulary* and its *required-check evidence standard*, never for R12; `#513`
cites it not at all.

**This is chronology, not negligence** — R12 landed on main after both branches
cut. It is put to the bench because #510 **is** the attestation tranche, R12's
four deferred envelope questions are attestation-envelope questions, and R12
names a rule (*no self-attestation*) that bears directly on #510's own
corroborate-versus-notarize decision. **Which tranche carries R12 is genuinely
open**: R12 says "the signed-execution-chain change (staged; PR #452)", which at
the time of the ruling meant tranche ONE — and tranche one is ratified without
it. **B-6 puts this to the bench.**

### 0.6 #513 DISCLOSES ITS LARGEST NARROWING AND DOES NOT ROUTE IT TO THE COUNCIL

`#513 tasks.md:2.2` routes **six** authoring decisions to the seats — D-A…D-F,
mapping to `design.md` D2, D3, D4, D6, D5 and D7. **`design.md` D8 is not among
them**, and D8 is where the packet narrows the staged topic's anchor-late
constraint:

> **AND THE NARROWING IS RECORDED RATHER THAN APPLIED SILENTLY.** The staged
> topic's constraint reads *"anchoring LATE (commit only what has been
> validated)"*. Taken literally that is unachievable against an append-only log,
> and this packet narrows it … **A topic's constraint is not a packet's to
> quietly reinterpret**, so the narrowing is in the requirement text, here, and in
> the pull-request record.
> — `#513 design.md` D8

**THE CONSTRAINT'S STATUS, CORRECTED AGAINST THIS PACKET'S OWN FIRST DRAFT.** An
earlier draft of this section called the anchor-late sentence a **ruled**
constraint. **It is not, and the distinction matters to how a seat should weigh
C-1.** The sentence lives at `signed-execution-chain.md:471-478`, inside the
topic's **`## Conflicts`** section — which holds three conflicts, of which the
second carries *"RESOLVED 2026-08-29"* and the third is *"left OPEN by design"*.
**The anchor-late conflict carries no ruling stamp, no date and no
disposition-by line**, and none of the seven Q-dispositions addresses it.
Repository-wide, the phrase *"only what has been validated"* resolves to exactly
two hits — this sentence and its INDEX mirror.

So the topic is **fully ruled as to its seven questions** and **unruled as to
this constraint**. #513 states the same thing in its own requirement text
(`spec.md:316`): *"THIS IS RECORDED AS A TENSION THE STAGED TOPIC DID NOT
RESOLVE, NOT AS A RESTATEMENT OF IT."*

**That cuts both ways and the bench should have both edges.** It weakens any
claim that #513 overrode a ruling — there was none to override. It does **not**
dissolve C-1: the staged topic calls the constraint *"a real design constraint on
tranche three, not a detail"*, the packet narrows it, and **recorded is not
ruled**. The convening therefore ADDS it to the ballot as **C-1**, and discloses
that as a convener act: the bench is being asked something its subject did not
ask.

`design.md` D1 and D9 are likewise unrouted. C-7 asks whether either needs to be.

### 0.7 TRANCHE ONE'S RATIFIED TASK LIST SAYS THE RE-DERIVATION IS OWED **WHEN EACH IS RAISED** — AND NEITHER PACKET CITES IT

**This is the convening's own finding and it bears directly on T-1.** The
threshold argument at §0.2 turns on WHEN Q4's re-derivation binds. #510 reads the
trigger as **realization** and carries it to `tasks.md:5.1`. **Tranche one's
own ratified `tasks.md` reads it as the raising**
(`openspec/changes/add-signed-execution-chain/tasks.md:187-190`, on main,
verbatim):

> - [ ] 5.3 Neither successor's content enters this packet. **Re-derive the
>   tranche two/three boundary against what actually exists when each is
>   raised**, per the topic's Q4 — a tranche that depends on an unbuilt layer is a
>   plan, not a tranche.

**#510 IS the raising of tranche two. #513 IS the raising of tranche three.**
Neither packet cites this task, and neither performs a re-derivation "against
what actually exists" — verified by grep for *"when each is raised"* and *"task
5.3"* across both packets' `proposal.md`, `design.md`, `tasks.md` and
`.openspec.yaml`: **zero hits in all eight files.**

**Stated with its limits, because it does not settle T-1 by itself.** Tranche
one's `tasks.md` is a task list, not a requirement; Q4's own disposition says
only *"not fixed now"* and names no binding moment; and the staged topic's Exit
path still says tranche two's *"contract text may now NAME the mechanism"*. **But
it is the only text in the estate that fixes a trigger, it is in a RATIFIED
packet, and it says "when each is raised" rather than "at realization."** A seat
ruling T-1 should read it. **Seats should verify this themselves.**

### 0.8 NEITHER PACKET CLAIMS A DRAFTING AUTHORIZATION, AND ONLY TRANCHE ONE'S IS RECORDED

Both packets decline to claim an approver, and both say so in terms. #510's
`.openspec.yaml:40-49`: *"**NOBODY YET, AND THE FIELD SAYS SO RATHER THAN
IMPLYING OTHERWISE.**"* #513's `.openspec.yaml:43-49` goes further and names the
reason:

> **NO APPROVAL FIELD IS CLAIMED HERE, DELIBERATELY.** … this packet does not
> record one it cannot cite: **the drafting was commissioned by an orchestrating
> session, which is not Brett Heap's word.** Tranche one's own origin record was
> corrected for exactly that overstatement — it first cited a session-handoff
> board as the drafting authorization and had to name his separate in-session
> green-light instead — and the lesson is carried rather than repeated.

**The honesty is exemplary and is recorded in the packets' favour.** What it
leaves open is the question itself. The only drafting green-light on the record
is tranche ONE's (`signed-execution-chain.md:873`: *"Brett Heap authorized the
**tranche-one** drafting in session"*). **Nothing at `origin/main` records an
authorization to draft tranche two or tranche three.**

The convening does not treat that as fatal — a draft filed FOR REVIEW is a
different act from a ratification, and Brett may authorize retrospectively in
ruling on this ballot. **It is put to the bench as T-3** because the family's own
recorded lesson is that an orchestrating session's direction is not the owner's
word, and #513 cites that lesson against itself.

### 0.9 #513's REQUIREMENT TEXT CITES A FILE THAT ONLY PR #509 CREATES

**The three subjects are not as independent as a combined sitting assumes.**
#513's `specs/chain-anchoring/spec.md` cites
`ideation/brainstorm/medxchain-blockchain-medical-records.md` in **NORMATIVE
requirement text at three sites** (`:541-542`, `:604`, `:657`). **That file does
not exist at `origin/main`. It is created by PR #509 — the third subject of this
sitting.**

Copilot found the dead reference and #513's commit `cf5a24b8` took it, adding the
in-flight status to each citation inside the requirement rather than only in the
proposal, plus (`spec.md:549-553`) *"**The obligation does not depend on the
citation**: it is normative on its own ground … and the citation is
PROVENANCE."*

**Consequences the bench should weigh, and they run in both directions:** #509
stops being a trivial subject — three of #513's requirements name it as their
provenance, so **A-1's provenance-fidelity question is load-bearing for #513
too**; and a seat judging #513 cannot verify those three citations without
reading #509. **This is stated in §0.3's terms: it is an argument FOR having
combined the sitting, and it is the only one the convening found.**

---

## 1. THE THREE SUBJECTS

### 1.1 SUBJECT 1 — PR #510, `add-chain-attestation` (tranche two)

**What it is.** An OpenSpec proposal packet, `Status: draft`, adding **NINE ADDED
requirements over a claimed 59 scenarios** to the `signed-execution-chain`
capability: the harness-controller setup attestation, runner attestations signed
AT the controller on a recorded request, corroboration rather than notarization
of self-report, a tier-2 key that never enters a worker, the pull-request open as
a signed chain-bound decision, the signed hash-link rule taking effect at link 4
with the gate's walk extended to links 1–6, CLOSURE as the point a chain
completes, the remediation chain as the one admitted consumer, and the executing
layer refusing an unverified inbound chain.

7 files, +1741/−0. **`contracts/` is untouched by the diff.** The packet declares
**no `## MODIFIED Requirements` block anywhere** (`tasks.md:1.2`).

**Its authority stack — the ruled dispositions it consumes.**

| Authority | Where ruled | What it gives #510 |
|---|---|---|
| **Q4** — tranche boundaries | staged topic `:672-683`, ruled 2026-08-29 by Brett Heap | Tranche one is links 1–3 ONLY; later boundaries RE-DERIVED when the omnigent layer and PKI plane are real; the log is a tranche-1 artifact; the gate exists FROM tranche one. **This is the threshold question — §0.2.** |
| **Q7** — where a signature physically happens | staged topic `:773-…`, ruled 2026-08-29 AS RECOMMENDED | Remote signing served by the harness controller; the runner's signing REQUEST recorded beside the signature; the controller corroborating against its own link-4 attestation. **This is the gate that held tranche two, and it is OPEN.** |
| **Narrowing A** | staged topic `:886-896`, ruled 2026-08-29 | Tier 1 is RATIFYING authority; agent-held REVIEW wallets stay lawful |
| **Tranche one**, ratified 2026-08-29 | `openspec/changes/add-signed-execution-chain/review/ratification-2026-08-29.md` | The chain identity, the ONE digest construction, the transparency log, the short-chain gate this packet extends |
| `add-trust-anchor` (realized, `contract-v1.37`) | | The certificate vocabulary the controller cert must be expressed in |
| `add-identity-brokering` (ACTIVE) | | Who a signer is; the persona-population refusal |
| `implement-openxpki-install-repo` (ACTIVE) | | The CA that would issue the controller certificate — **a realization gate, `tasks.md:5.2`** |
| `contracts/omnigent/` | | `access_secrets: false`, the constitutional ground of the tier split |

**Its own pre-flagged council questions**, from `tasks.md` §2:

* **2.2 — the threshold**, §0.2 above. Ruled first; a premature ruling ends the round.
* **2.3 — the ADDED-not-MODIFIED gate composition** (`design.md` D3). Named
  repair if the composition is ruled insufficient: a scenario-complete MODIFIED
  restatement of tranche one's gate requirement. **See §0.4 for the convening's
  measurement of what that costs.**
* **2.4 — the plural-predecessor enumeration** (`design.md` D4) — the packet's own
  resolution of a gap in the ruled topic, not a ruling encoded.
* **2.5 — the revocation-after-signing horizon** (`design.md` D6) — likewise the
  packet's own decision.

**Self-declared contested pulls** (`tasks.md:1.8`), which the family's
contested-finding rule requires be recorded rather than smoothed: Q4's
re-derivation instruction versus drafting now (**routed to this council,
unresolved in the packet**); tranche one's gate scope note versus the extended
walk (read as self-limiting); and the topic's SINGULAR hash-link rule versus its
PLURAL link 5 (resolved by addition, flagged as the packet's own resolution).

**A first bot round has already run** and its three P1s are recorded as closed
(`tasks.md:1.9`; `design.md` D10). All three were one shape — *a record that NAMED
something standing where a record that ESTABLISHES it belonged*. **A seat that
records only that they were "taken" has not discharged its obligation; attack
them.**

### 1.2 SUBJECT 2 — PR #513, `add-chain-anchoring` (tranche three)

**What it is.** An OpenSpec proposal packet adding **NINE ADDED requirements over
a claimed 52 scenarios** in a **NEW capability directory**,
`specs/chain-anchoring/`. 7 files, +1884/−0. Five commits, of which four are fix
rounds against bot findings.

**Confirmed by the convening:** `openspec/specs/chain-anchoring/` does **not**
exist at `origin/main` — this is a genuinely new capability, not a delta over an
unpromoted one.

**Its authority stack.**

| Authority | Where ruled | What it gives #513 |
|---|---|---|
| **Q3** — which chain | staged topic `:579-661`, ruled 2026-08-29, **DIVERGING from the vendored study, in two rounds** | BOTH witnesses on EVERY anchored item; **Kaspa FIRST** as the operational witness under three unchanged conditions; **Bitcoin batched via OpenTimestamps as the DURABILITY witness — ten-year claims cite Bitcoin**; no selectivity, no third chain; receipts chain-agnostic multi-anchor carrying BOTH proofs. *"Primary" is order of arrival, never evidentiary weight.* |
| **Q6** — what "PHI portions on chain" means | staged topic `:735-…`, **CONFIRMED** 2026-08-29 | SALTED KEYED COMMITMENTS; erasure by salt destruction; raw/encrypted/plain-hashed PHI on chain stays REFUSED and **no later change re-litigates it** |
| **Q5** — smart contracts / L2 | staged topic `:685-…`, **RULED AGAINST THE RECOMMENDATION** | Evidence-only today, but the change **MUST NOT constitutionalize "no contract code ever"** nor gate a future adoption on the study's trigger; the study's caution is ADVISORY CONTEXT, not a bar |
| **Q2** — the on-chain boundary | staged topic `:553-…` | Carried as contract text with a validator refusing payload-shaped records and unsalted commitments |
| **The anchor-late constraint** | staged topic `:471-478` | *"That argues for anchoring LATE (commit only what has been validated) and is a real design constraint on tranche three, not a detail."* **NARROWED by this packet — §0.6, ballot C-1** |
| The vendored study | `ideation/staging/signed-execution-chain/chain-selection-study.md` | Research input, **NOT to be edited** — *"a research record rewritten to agree with a later ruling stops being evidence"* |
| Tranche one; tranche two (**#510, UNMERGED and UNRATIFIED**) | | The chain this layer anchors |

**Its own pre-flagged council questions**, `tasks.md:2.2` — six authoring
decisions, **D-A read first**: D-A missing-witness semantics (`design.md` D2, *"THE
PACKET'S LARGEST DECISION"*); D-B the structural payload refusal (D3); D-C the
declared-construction commitment refusal and its residual (D4); D-D the change id
and capability name (D6); D-E deferring the permissioned-ledger selection to
realization (D5); D-F the per-plane key correction to a vendored source (D7).

**The convening ADDS two**, disclosed as convener acts: **C-1**, the D8 anchor-late
narrowing (§0.6); and **C-3**, how a packet expresses a dependency on an
unratified sibling.

**Three pre-flagged items carried from the convening instruction**, stated as the
bench will find them:

1. **The TWO-ANCHOR narrowing** — D8. §0.6 and ballot C-1.
2. **MISSING-WITNESS semantics** — D2 / D-A. The claim must fail closed, never
   the factory. Commit `455bbdaa` ("A pending witness contributes no receipt
   entry, so the two rules stop colliding") is a fix round on exactly this;
   **seats should read the commit, not only the current text.** Ballot C-2.
3. **NAMING** — D6 / D-D. Ballot C-4, and it is shared with #510 as **B-7**;
   §1.4 below states the measured fact.

### 1.3 SUBJECT 3 — PR #509, `vendor-medxchain-brainstorm`

**What it is.** ONE new file,
`ideation/brainstorm/medxchain-blockchain-medical-records.md`, 223 lines,
+223/−0. A vendoring of Brett Heap's MedxChain notes into the brainstorm stage —
the one stage of the document lifecycle where, per
`docs/document-lifecycle.md`, contradiction is legal.

**Why it is nonetheless a council subject.** A vendoring makes a claim of
PROVENANCE. `ideation/brainstorm/` is projected into NotebookLM and is read by
later authors as a record of what someone actually said. **The risk is not that
the ideas are wrong — a brainstorm may be wrong. The risk is that the vendoring
author's own framing enters the record wearing Brett's voice, or that a mapping
appendix asserts things about the estate that are not true.**

**The review questions proper to its kind**, and they are the only ones:

* **Provenance fidelity.** Does the document say where the notes came from, who
  authored them, and when? Is Brett's original text distinguishable from the
  vendoring author's framing, headers and appendices?
* **No invented claims.** Every assertion the document makes *about the estate*
  — as opposed to Brett's own speculation — must be true at `origin/main`.
  Brett's speculative content is legitimate and is **not** to be judged for
  correctness.
* **Mapping accuracy.** If the document carries a mapping appendix onto ruled
  dispositions or existing artifacts, **every target must exist and every
  characterization must be accurate.** This is the one part of a brainstorm
  document that is not free-form.
* **Lifecycle conformance.** The controlled `Status:` header and whatever
  `docs/document-lifecycle.md` requires of a `brainstorm` document.

**The governing header contract** is `ideation/README.md` "## Ideation Header
Format", enforced in code at `scripts/ideation_dashboard/authoring.py`
(`REQUIRED_HEADER_FIELDS` = Status, Kind, Summary, Topics, Repository context,
Captured; `BRAINSTORM_SUFFIX = " — Brainstorm"`). It also carries a provision
specific to **imported** evidence — material not authored in-session — which
these notes are. **Seats should read that contract themselves and rule whether it
is met.**

**A seat whose charter does not reach this subject should say so and name the
seat it belongs to**, exactly as the 2026-08-28 returns did. The convening's
reading is that **company-policy-lead** and **lead-quality** reach it squarely,
**lead-architect** reaches the mapping-accuracy question, and **lead-security**
reaches it only if the document discloses something it should not.

**PLACEMENT, MEASURED — and it decides where this sitting's own #509 record can
live.** `ideation/` contains **no `review/` directory anywhere**;
`ideation/brainstorm/` has exactly three subdirectories (`cross-domain/`,
`inbox/`, `notebooklm-import-test/`). Every review record in this estate lives
under `openspec/changes/<change>/review/`, and **no brainstorm vendoring in this
repository has ever carried a review record.** Brainstorm material has landed by
ordinary pull request, with review carried by the PR itself and — for routed
intake — by `routing.yaml`. **So this sitting does not create one**, and #509's
outcome is carried in the combined ballot and in the shared record. **A-5 asks the
bench whether a council was the right instrument here at all.**

### 1.4 THE NAMING FACT, MEASURED — it is common to #510 and #513

Tranche one, **ratified**, names both successors
(`openspec/changes/add-signed-execution-chain/proposal.md:82-100`):

> - **Tranche two — `add-signed-execution-chain-attestation`** (working id): links
>   4–6 and 10 …
> - **Tranche three — `add-signed-execution-chain-anchoring`** (working id): the
>   commitment and anchor layer …

The changes as raised are **`add-chain-attestation`** and
**`add-chain-anchoring`**.

**Both sides are stated exactly.** Tranche one marks each name *"(working id)"*
on its face, so the shortening is not a breach of a fixed identifier. What it
costs is **resolvability**: a reader who greps the ratified packet for its named
successor finds no such change. Whether that matters, and whether the ratified
text should be corrected or the ids adopted, is **B-7 / C-4**. #513's `design.md`
D6 addresses the id question directly; **#510's does not** — verified by grep.

---

## 2. WHAT THIS CONVENING IS FOR, AND WHAT IT IS NOT

### 2.1 The output is a ballot; every act after it is Brett's

This sitting produces **per-subject, per-seat verdicts with return citations**, a
**convener's tally**, and an **enumerated item list for Brett Heap's ruling**.

### 2.2 What this convening does NOT do

* **It does not ratify.** All three PRs stay exactly as they are.
* **It does not merge, and it does not push.** Nothing is pushed to any remote by
  this sitting.
* **It moves no schema byte, cuts no bundle, allocates no minor**, and touches
  nothing under `contracts/`.
* **It defines no candidate class, no envelope entry, no enrollment and no flip.**
  The 2026-08-28 unanimous ruling that proposals are **never-convenable** through
  the clearance pipeline is UNDISTURBED; **this sitting exists because of it.**
* **It does not re-open any of the seven Q-dispositions.** All seven were ruled by
  Brett Heap on 2026-08-29. A seat may find that a packet MISREADS a ruling; no
  seat may rule the ruling wrong.
* **It does not decide #504** (`govern-sibling-added-modified-deltas`, open) or
  **#502**, and neither packet may be delayed for them.

### 2.3 Convener acts this packet cannot perform

Per `gate-rules.yaml` `failure_semantics`:

```yaml
failure_semantics:
  split_vote: park_for_liaison
  missing_required_seat: refused
  output_disposition: convener_accepts_or_rejects_on_record
```

1. `human_step: acknowledgement_of_notice` — the non-blocking notice. **Never a
   sign-off.**
2. The liaison disposition, for anything this council parks. **A 2–2 split on a
   proposal review PARKS FOR BRETT'S LIAISON RULING** — the procedure defined at
   the 2026-08-29 sitting (record §8.4).
3. `output_disposition: convener_accepts_or_rejects_on_record`.
4. **T-0** — whether a §7.4 sitting, and a three-subject one, is within this
   council's reach at all. The council recommends; only Brett rules.
5. The ratification act, and the merge.

**NOTHING IN THIS CONVENING IS RATIFIED. Every output is a recommendation carried
to Brett Heap.**

---

## 3. THE BENCH, AND HOW IT WAS RESOLVED

### 3.1 The shipped resolver still cannot read this council's document — FIFTH consecutive convening

R26 (LA-F7, 2026-08-26; reproduced 2026-08-28 and 2026-08-29) is unrepaired.
Executed at codexFactory `3c71ddc9` rather than cited:

```
$ sr.resolve_required_seats(yaml.safe_load(open("hermes/domain/review-councils/gate-rules.yaml"))["council"], None, {})
ConditionError: council.members must be a non-empty list — the unconditional domain roster
```

`gate-rules.yaml`'s `members` is a mapping; the evaluator requires a list. **The
bench below was HAND-ASSEMBLED, and this packet says so rather than presenting a
hand roster as a tool output.** codexFactory task 5.9a stays open.

### 3.2 The CSC seat is NOT seated

`gate-rules.yaml`'s `conjunction_pull_in` seats the
`client-security-compliance-officer` when the predicate
`rule_touches_security_posture` holds over `scripts/merge_master/**`,
`.github/workflows/**`, `hermes/domain/review-councils/**` and `schemas/**`.

**Fed the subjects' real reach it does not hold.** All three PRs touch only
openxFactory `openspec/changes/**`, `ideation/**` and `README.md`. None touches
any listed surface — and, as the 2026-08-29 sitting established, `schemas/**`
does not reach `contracts/schemas/…` in any case. The only supply that returns
`True` for any gate-rules convening is the convening's **own paperwork**, which
CSC itself proved is a tautology and which Brett adopted a finding against on
2026-08-28.

**Recorded against this convening's own interest, exactly as its predecessor
did:** the predicate's input contract asks a **definition-time** question about
*"the rule being SET"*, and **no rule is being set here** — so the honest ground
is arguably *inapplicable* rather than *false*, which is the repair
`lead-architect` offered on 2026-08-29 and which Brett's ruling **did not adopt**
(record §8.5 leaves the ground undecided). `lead-security` ruled that sitting's
identical decline **WRONG** on `seat_resolution.py:40-44` (*"Unevaluable NEVER
means absent … The caller refuses the rule or parks the convening"*), and that
dissent is preserved and unresolved. **`lead-security`'s obligation below
explicitly includes the exposure reading a CSC seat would have carried**, so the
question is not dropped along with the seat. **T-0(b) carries the decline to the
bench again.**

### 3.3 The bench

| Seat | Layer | Basis | Model |
|---|---|---|---|
| **lead-architect** | domain | `members.domain` | **`opus`** — inherited |
| **lead-security** | domain | `members.domain` | **`opus`** — inherited |
| **lead-quality** | domain | `members.domain` | **`opus`** — inherited |
| **company-policy-lead** | client | `members.client.seat`; `missing_required_seat: refused` | **`sonnet`** — `hermes/client/role-overrides.yaml` `seat_representation.model`, declared by this council 2026-08-26 (Slot 2, R23) |
| ~~client-security-compliance-officer~~ | client | conjunction pull-in — **NOT SEATED**, §3.2 | — |
| ~~intent-owner role slot~~ | project | `binding: symbolic_until_project_roster` — **vacant-symbolic**, not missing | — |

**Four seats**, identical to the 2026-08-29 sitting.
`missing_required_seat: refused` is satisfied: the unconditional domain roster is
complete and the required client seat sits.

**THE SEAT-MODEL MAPPING, AND THE S5 TARGET THAT IS NOT YET APPLIED — stated
precisely because it changed on main two days ago.** Brett's S5 rulings R1–R4 of
2026-08-29 (`add-wallet-carried-review-authority/rulings-2026-08-29.md`) name a
**target** composition: `lead-quality` → `claude-sonnet-5`, `lead-security` and
`lead-integration` → `claude-opus-5`, `company-policy-lead` → `claude-sonnet-5`
declared by the tenant. **That target is NOT in force**, on the ruling's own
words:

> **What makes R1–R4 enforceable:** the Gate-Rules Council's selection record (with
> the soak evidence §2 requires, its diversity finding, and the convener's recorded
> acceptance), followed by the roster-change Lead's `lead_accepted_recorded`
> acceptance … **Until both land, the enrolled roster keeps the mutable `opus` /
> `sonnet` selectors** and task 7.5's model half stays UNTICKED.

Neither owed act has landed. Further, `hermes/domain/agent-mixes.yaml`'s
`model_assignments` block covers the **merge-readiness** council's four seats
(`lead-quality`, `lead-security`, `lead-integration`, `company-policy-lead`) —
**it does not cover `lead-architect`, and the gate-rules council has no
`model_assignments` block at all.** So the bench above follows the 2026-08-29
§7.4 precedent verbatim, which recorded `lead-architect`, `lead-security` and
`lead-quality` as *"inherited (opus)"* and `company-policy-lead` as `sonnet`.

**What R4 fixed, and what this sitting applied:** R4 establishes that **the TENANT
declares the CPL's model and the domain lane is a consumer bound to that
declaration**. This sitting reads `company-policy-lead`'s model from
`hermes/client/role-overrides.yaml` — the tenant declaration — and not from any
domain file. That is the mapping R4 fixed, and it is followed.

**The divergence, disclosed:** under the S5 *target*, `lead-quality` would sit at
sonnet; here it sits at opus. **The convening follows the enrolled roster and the
direct precedent rather than an unapplied target**, and says so rather than
letting a reader infer that R2 was ignored.

### 3.4 Mode

**Agent-seat deliberation**, per the 2026-08-22, 2026-08-26, 2026-08-28 and
2026-08-29 precedents: **one independent agent per seat**, each loaded with only
this packet, its own persona and seat declaration, and the council contract.
**No seat sees another seat's return. No seat sees the convener's opinions. No
seat writes to any checkout.**

**FINDINGS ARE TO BE REACHED BY EXECUTION**, not by reading prose. The
2026-08-29 sitting's decisive finding was reached by building a schema and
driving a record through it after the same defect had survived two Copilot
reviews, three author self-catches and a full seat round that read the
prescription instead of running it. **The standing method rule, offered as
precedent by that sitting's `lead-quality` seat and worth repeating here:**

> a prescribed fix applied without a verifier is an unverified change, whatever
> its provenance.

**RETURN CITATION IS MANDATORY.** Every claim in a return cites `file:line` in
this packet, in a pull request's own files, or in governing text. The standing
rule applies unchanged: **where a ballot and a return diverge, THE RETURN
GOVERNS.**

**THIS PACKET IS AN INPUT, NOT A LIMIT — AND THE CONVENING IS HOLDING FINDINGS
BACK ON PURPOSE.** The convening has executed work of its own on all three
subjects and has deliberately **withheld** most of it, because injecting a
convener-found fact into a seat round makes the convener a participant and
contaminates the independence that is the only reason to convene a bench at all.
Those findings go to the ballot, where Brett sees them **beside** your returns
rather than through them.

**Two mechanical facts were carried in anyway** — §0.4 and §0.7 — on a narrow and
stated ground: each bears directly on a question **the subject itself asks the
council**, and the 2026-08-29 sitting recorded as its own fourth error that it
*"asked B12 and did not itself execute the fix it asked about."* **Both are
labelled as the convening's, and both are to be re-verified by you rather than
taken.** If your measurement disagrees with the convening's, **your measurement
governs and you should say so plainly.**

**The absence of a finding in this packet is not evidence that there is none.**

### 3.5 The checkouts

Read-only for every seat.

```
sitting     opensoft/openxFactory   origin/main @ afe29561a317853eb22f1e6b248f7029fa2fb2a7
              PR #510 head          e7f6ae0e400719894fbaa0d14be274ba86b2e3b3   (origin/change/add-chain-attestation)
              PR #513 head          cf5a24b89870a87663c595550210ee4deb0ac28e   (origin/change/add-chain-anchoring)
              PR #509 head          26c7e778682089789795befad4c28af509ff2706   (origin/change/vendor-medxchain-brainstorm)
              shared merge-base     b710976b4a4fef277cdd292a407942369e9b9efa
sittingref  opensoft/codexFactory   3c71ddc910b8e0b119d0e1ee40a5523dfa294f07   (READ-ONLY precedent reference)
```

A seat needing a checked-out tree **creates its own worktree** and never modifies
another's. Confirm `git status --porcelain` empty before and after your work.

---

## 4. PER-SEAT VERIFICATION OBLIGATIONS

**Every obligation below is to be discharged BY EXECUTION.** Where you cannot
execute, say so and say what you tried.

| Seat | Verify |
|---|---|
| **lead-architect** | **The threshold, the composition, and whether the vocabulary is consumed or reinvented.** (a) **T-1 is yours first.** Read Q4's ruled disposition and the staged topic's `## Exit path` **in the topic itself**, not in either packet's summary of them, and rule whether drafting tranche two's requirement text today is what Q4 permits or what it forbids. (b) **D3, by construction**: does tranche one's gate requirement actually self-limit? Read it at `spec.md:391-556`, count its scenarios yourself, and rule whether an ADDED requirement that extends the walk composes cleanly or leaves promoted canon holding two gate requirements a reader must reconcile. Note that **both changes write ADDED into the same unpromoted capability** and that `#504` is open on exactly the sibling-delta class. (c) **The collision risk the staged topic names as its FIRST risk** (`:465-469`): *"inventing a second identity or certificate vocabulary … a new schema here would be the 'two records of one decision' defect at contract scale."* For each of `add-trust-anchor`, `add-identity-brokering`, `contracts/omnigent/`, `add-wallet-carried-review-authority` and tranche one — does the packet CONSUME the existing vocabulary at the cited path, or does it mint a parallel one? Resolve every citation. (d) **#513's D8** (C-1): is the two-anchor split a faithful narrowing of a ruled constraint, or a reinterpretation the packet was not entitled to make? (e) **#509's mapping appendix**: does every artifact it names exist, and is each characterization accurate? |
| **lead-security** | **Fail-closed behaviour under subtraction, and the exposure reading the unseated CSC seat would have carried (§3.2).** (a) **#513's D2/D-A — MISSING WITNESS (C-2), and it is the largest security question in this sitting.** Drive it: when a witness is unavailable, unreachable, or pending, does the CLAIM fail closed while the FACTORY keeps running — or can a missing witness stop the factory, or a claim pass with one witness where two are required? Read commit `455bbdaa` and say whether it fixed the collision or moved it. Q3 ruled BOTH witnesses on EVERY anchored item with **ten-year claims citing Bitcoin**: what does a receipt assert when the Bitcoin half is absent? (b) **#510's tier-2 key rule**, *"in every configuration"* — subtract each condition in turn and report which still refuse. `access_secrets: false` is constitutional; does the drafted text actually hold it, or does it hold it only in the configuration the packet imagined? (c) **Corroborate-versus-notarize**, and **R12's no-self-attestation rule** (§0.5): does #510's corroboration requirement satisfy *"a holder signing its own composition attests nothing an independent party can rely on"*, or is there a configuration in which the controller effectively notarizes itself? (d) **Q6's commitment reading is CONFIRMED and no later change may re-litigate it.** Does #513's text hold salted keyed commitments everywhere, refuse unsalted commitments and payload-shaped records by a check a validator can actually run, and is the salt-destruction erasure claim honest in BOTH directions? (e) Does anything in either packet, or its declared realization, create, move or read live key material? (f) **#509**: does the vendored document disclose anything that should not be in a repository read by NotebookLM? |
| **lead-quality** | **Is it TESTABLE, is the delta what it claims, and does any claim outrun the machinery?** (a) **Run and report real counts**: `OPENSPEC_TELEMETRY=0 openspec validate add-chain-attestation --strict`, the same for `add-chain-anchoring`, and `--all --strict` on each branch. (b) **VERIFY THE PACKETS' OWN NUMBERS BY COUNTING.** #510 claims 9 ADDED / 59 scenarios; #513 claims 9 ADDED / 52. **The convening has already found one count wrong** (§0.4) and states plainly that it may have found only one of several. Count every requirement and every scenario in both, and check that **every requirement's FIRST body line carries SHALL/MUST** — the parser reads only line one. (c) **THE CLAIM-OUTRUNNING-THE-MACHINERY FAMILY — this estate's most-recorded defect.** Enumerate every place either packet asserts a gate, check, refusal or enforcement, and classify each: DECLARED as not-yet-existing with a cite, or ASSERTED as fact. A workflow file is not evidence; a live ruleset state is. (d) **Do the scenarios test what the requirement STATES?** Sample hard: for at least three requirements per packet, read the requirement text and then read its scenarios, and report any scenario that tests something adjacent to, weaker than, or different from what its requirement says. (e) Are the tasks executable as written, and does either `tasks.md` state anything a checker cannot decide? (f) **#509**: does the vendored document conform to `docs/document-lifecycle.md`, and does it carry any claim about the estate that is false? |
| **company-policy-lead (tenant)** | **THE TENANT VOICE — and note that BOTH chain packets edit `README.md`, which your `role-overrides.yaml` specialization names verbatim as a surface that "speaks for the company to a reader outside the engineering conversation".** (a) Do the README entries state what is true about a DRAFT — that nothing is ratified, that no schema byte moved, that no number is spent — to a reader who reads **only** that entry? (b) Does any sentence in either packet read as though Brett has already agreed to its CONTENT, as opposed to having authorized its authoring? The 2026-08-29 sitting's CPL seat swept exactly this and found it clean; sweep it again, because tranche one's ratification and Brett's drafting green-light are now real acts that a packet could over-read. (c) **#509 is squarely yours.** A vendoring of the owner's own notes into a company repository is the tenant-voice question in its purest form: is Brett's voice preserved and attributed, is the vendoring author's framing distinguishable from it, and would a reader outside this conversation be misled about who said what? (d) **Volume.** Two packets totalling 3,625 lines and a 223-line vendoring, in one sitting. Does the volume itself do persuasive work the record should not let it do — and was combining three subjects into one sitting the right instrument (**T-0(c)**)? |
| **EVERY SEAT** | **(i) T-1, the threshold** — answer it even if your charter reaches it only partly, and say which limb is yours. **(ii) THE INHERITED BOT SURFACE.** #510's three P1s (`design.md` D10) and #513's four fix-round commits (`455bbdaa`, `e1bd201d`, `2e539779`, `cf5a24b8`) were prescribed by readers who may not have re-read their own fixes. **Attack the fixes, not the fact that they were taken.** Read the commits. **(iii)** Record what you found in each packet's **FAVOUR**. A record that lists only defects misreports what the bench read. |

---

## 5. BALLOT QUESTIONS

Answer every question your charter reaches. **Where a question is not your
seat's, say so and name the seat it belongs to.** Where you decline for want of
grounds, say that instead of guessing — but note that a seat WITH grounds rules.

### T — THRESHOLD AND SITTING

**T-0 — Was this sitting lawful, and in this shape?** Three limbs, and they are
separable. **(a)** Is a §7.4 proposal review within `gate_rules_council`'s reach
at all (§0.1)? Options: (i) this council extends to it; (ii) it needs a chartered
third body; (iii) it is not a council act. The 2026-08-29 bench split LA+CPL →
(ii), LS+LQ → (i); **Brett sanctioned the act pending the amendment and did not
choose between the roads.** **(b)** Was declining the CSC seat right (§3.2), and
is the honest ground *false* or *inapplicable*? `lead-security` ruled the
identical decline WRONG on 2026-08-29 and that dissent stands unresolved.
**(c)** Was combining THREE subjects into one sitting lawful, and did it degrade
your reading (§0.3)? **Answer (c) honestly even if it embarrasses the convening.**

**T-1 — THE THRESHOLD. Is #510 PREMATURE?** *(Ruled before anything else about
#510. A ruling of premature ENDS #510's round and touches neither #509 nor
#513.)* §0.2 states both texts in full. Options as the convening sees them:

* **(a) NOT PREMATURE.** Q4's re-derivation instruction governs the **boundary
  re-derivation at realization**, which #510 carries as an undischargeable gate
  at `tasks.md:5.1`; the staged topic's Exit path says tranche two's *"contract
  text may now NAME the mechanism"* and that what remains is *"machinery rather
  than a ruling"*. Drafting proceeds; the gate holds realization.
* **(b) PREMATURE.** Q4 says the later boundaries are *"RE-DERIVED when the
  omnigent layer and the PKI plane are real, NOT FIXED NOW"*, and a packet that
  fixes links 4–6+10 as tranche two's content **fixes a boundary now**. *"A
  boundary drawn against an unbuilt layer is a guess wearing a tranche number"*
  is a statement about the drafting act, not only about its realization.
* **(c) NOT PREMATURE BUT NARROWED** — the packet may stand as drafted only if
  some named subset is struck or explicitly re-opened at the re-derivation. **Name
  the subset.**

**T-2 — Does a ruling on #510 bind #513?** #513 composes on a sibling that is
neither merged nor ratified. If #510 is ruled premature, is #513 premature *a
fortiori*, or does it stand on its own ruled gates (Q3 and Q6, both OPEN)? Note
that #513 declares the relation as **"Sequencing, not blocking"** at four sites
and names only tranche one and the PKI plane as hard prerequisites.

**T-3 — WAS THE DRAFTING AUTHORIZED?** (§0.8.) The only recorded drafting
green-light is tranche ONE's. Both packets decline to claim an approver and say
why. Is a draft filed FOR REVIEW without a recorded drafting authorization a
lawful object to put before this council — and if it is not, is the defect cured
by Brett ruling on this ballot, or must the authorization precede the sitting?
**Answer within your charter and say plainly if it is not yours.**

### A — SUBJECT #509 (the vendoring)

**A-1 — PROVENANCE FIDELITY.** Does the document establish where the notes came
from, who authored them and when, and is Brett's text distinguishable from the
vendoring author's framing? **Read the `Source:` block closely.** Blocking if the
answer is no. Note §0.9: **three of #513's requirements cite this file as their
provenance**, so this question is load-bearing beyond #509.

**A-2 — INVENTED CLAIMS.** Does the document assert anything **about the estate**
that is not true at `origin/main`? **Enumerate exhaustively, and verify each by
executing a search rather than by reading.** *(Brett's own speculative content is
legitimate in a brainstorm and is NOT judged for correctness — say which is
which.)* Pay particular attention to any phrase presented as **what the staged
topic "calls"** something, and to any **disposition label** attached to a Q.

**A-3 — MAPPING ACCURACY.** For every target the mapping appendix names — a
ruled Q-disposition, a section heading, a claim number, a document path: does it
exist, and is the characterization accurate? **A table, please**, with a cite per
row. Quotations presented inside quotation marks should be checked as
quotations.

**A-4 — LIFECYCLE CONFORMANCE.** The mandatory header fields, the H1 suffix rule,
and the **imported-evidence** provisions of `ideation/README.md`. Does it conform?
Compare against at least one existing **imported** brainstorm document, not only
against in-session ones.

**A-5 — Is a council the right instrument for a brainstorm vendoring at all?**
No brainstorm vendoring has ever carried a review record (§1.3). **Answer against
the convening's interest if that is where the evidence points.**

### B — SUBJECT #510 (tranche two)

**B-1 — The packet as a whole**, conditional on T-1 not ending the round.

**B-2 — D3: the ADDED-not-MODIFIED gate composition** (`tasks.md:2.3`). Accept, or
rule the composition insufficient and take the named repair (a scenario-complete
MODIFIED restatement)? **§0.4 gives you the measured scenario count; verify it
yourself.** Note that tranche one is an ACTIVE change whose gate requirement is
**not** in `openspec/specs/`, and that #504 is open on this class.

**B-3 — D4: the plural-predecessor enumeration** — the packet's own resolution of
a gap in the ruled topic. Sound? Is *"a dropped attestation is a break, never a
shorter chain"* actually enforced by the drafted text?

**B-4 — D6: the revocation-after-signing horizon** — the packet's own decision.

**B-5 — The three closed P1s** (`design.md` D10). Do the repairs hold *as
applied*? Name any that does not, and say what you executed.

**B-6 — R12 (§0.5).** Does #510 need to consume Brett's R12 ruling and the four
S5 envelope questions — standard, key distribution, signature algorithm,
evidence-retention location — before ratification? Or do they belong to tranche
one (which is ratified without them), to tranche three, or to a successor?

**B-7 — NAMING** (§1.4). Should the change id be `add-chain-attestation`, or the
working id tranche one names? If the short id stands, is a back-citation owed in
the ratified tranche-one text?

**B-8 — Does landing a draft governance packet on `main` commit anything?** Both
chain packets add README "OpenSpec Records" entries. Is a draft-status packet on
`main` a safe object?

### C — SUBJECT #513 (tranche three)

**C-1 — D8: THE TWO-ANCHOR NARROWING OF A RULED CONSTRAINT** *(added by the
convening, §0.6 — the packet did not route it)*. The staged topic's constraint
is *"anchoring LATE (commit only what has been validated) … a real design
constraint on tranche three, not a detail"*. #513 narrows it to govern ITEM
anchors only, on the ground that an append-only log's checkpoints commit to the
whole prefix by construction and so cannot satisfy the constraint literally.
**Is the narrowing (i) correct and faithfully recorded; (ii) correct but owed a
ruling before it lands; or (iii) a reinterpretation of a ruled constraint that
the packet was not entitled to make?** The packet's own rejected alternative — a
second validated-only tree — is stated in D8; weigh it.

**C-2 — D2 / D-A: MISSING-WITNESS SEMANTICS** *(the packet's own largest
decision)*. Does the CLAIM fail closed while the FACTORY keeps running? Can a
missing or pending witness halt the factory? Can a claim pass carrying one
witness where Q3 requires both? **What does a ten-year claim assert when the
Bitcoin durability witness is absent?** Read `455bbdaa`.

**C-3 — Dependency on an unratified sibling** *(added by the convening)*. #513
composes on #510, which is neither merged nor ratified and may be ruled premature
in this very sitting. How does the packet express that, and is the expression
honest and safe?

**C-4 — D6 / D-D: the change id and capability name** (§1.4), plus the
sibling-delta shape. Note that #513 creates a **new** capability while #510 adds
to an **unpromoted** one — is that asymmetry right?

**C-5 — D-B, D-C, D-E, D-F**, the packet's four remaining routed decisions:
the structural payload refusal; the declared-construction commitment refusal and
its declared residual; deferring the permissioned-ledger selection to
realization; and the per-plane key correction to a vendored source. **On D-F note
the standing rule that the vendored study is NOT to be edited** — a research
record rewritten to agree with a later ruling stops being evidence. Does the
correction respect that?

**C-6 — Q5's standing tension.** Brett ruled AGAINST the recommendation's
permanence: the change **must not constitutionalize "no contract code ever"** nor
gate a future adoption on the study's trigger. Does #513's text hold today's
evidence-only posture **without** constitutionalizing it?

**C-7 — D1 and D9 are unrouted** (§0.6). Does either need a ruling?

### X — CROSS-CUTTING

**X-1 — CLAIMS OUTRUNNING THE MACHINERY.** The estate's most-recorded defect
family. Across both chain packets: what is asserted that does not exist, and is
each such place DECLARED or ASSERTED? Blocking wherever a packet asserts an
enforcement it cannot name a running check for.

**X-2 — VOCABULARY: consumed or reinvented?** The staged topic names this as the
family's FIRST risk. Per packet, per named authority.

**X-3 — Two ADDED deltas into one unpromoted capability.** #510 and tranche one
both add to `signed-execution-chain`, which is not in `openspec/specs/`. Is that
safe on promotion, and does it interact with #502 / #504?

---

## 6. VERDICT VOCABULARY, AND THE RETURN FORMAT

**Verdicts are the 2026-08-28 set, unchanged, and you give ONE PER SUBJECT:**

> **ACCEPT** · **ACCEPT AS AMENDED** · **REFUSE AS DEFINED** · **REFUSE** ·
> **PARK** (for want of grounds only — a seat with grounds rules)

A subject outside your charter returns **NOT MY SEAT**, naming the seat it
belongs to. That is not a PARK and is not counted as one.

The return format is the 2026-08-29 shape, and it is not optional:

```
Seat: <id> (<layer> seat) · Convening: gate_rules_council (§7.4 sitting), 2026-08-30
Packet: openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md
Judged at: openxFactory main afe29561 / #510 e7f6ae0e / #513 cf5a24b8 / #509 26c7e778

# SEAT RETURN — `<id>` (<CODE>), <layer> seat

## 0. Persona declaration      — charter quoted, seat basis, assigned obligation,
                                 and any boundary reading you take, stated openly
## 1. What I verified BY EXECUTION — commands and their REAL output, verbatim
## 2. Findings                 — <CODE>-F1…, each BLOCKING | SHOULD-FIX | OBSERVATION,
                                 each with a return citation, each tagged [509|510|513|X]
## 3. Positions on the ballot questions   — T-0, T-1, T-2, A-1…, B-1…, C-1…, X-1…
## 4. VERDICTS — ONE PER SUBJECT
### #509 — <word>, then the grounds in one sentence
### #510 — <word>, then the grounds in one sentence
### #513 — <word>, then the grounds in one sentence
### Amendments             — <CODE>-A1…, each BLOCKING | SHOULD-FIX, each tagged with its subject
### Conditions attached to the record — <CODE>-C1…
## 5. In the packets' and the changes' FAVOUR
```

**Amendment numbering is per seat and continuous across subjects** (LA-A1, LA-A2,
…), with each amendment tagged `[509]`, `[510]`, `[513]` or `[X]`. **A blocking
amendment must name what would discharge it.**

---

## Appendix A — governing text, by path, at the judged commits

Read these rather than this packet's summary of them.

**The ruled authority — read the topic itself, not a packet's account of it**
* `ideation/staging/signed-execution-chain/signed-execution-chain.md` (main) —
  `:471-478` the anchor-late constraint; `:501-…` all seven Q-dispositions;
  `:579-661` Q3; `:662-683` Q4; `:685-…` Q5; `:735-…` Q6; `:773-…` Q7;
  `:810-901` the Exit path, the tranche gate states, and Narrowing A.
* `ideation/staging/signed-execution-chain/chain-selection-study.md` — the
  vendored research record. **NOT to be edited.**
* `ideation/staging/INDEX.md` — the topic's row and detail section.

**Tranche one, ratified — the base both packets build on**
* `openspec/changes/add-signed-execution-chain/proposal.md` — `:82-103` the named
  successors; `:385-…` the rulings table.
* `openspec/changes/add-signed-execution-chain/specs/signed-execution-chain/spec.md`
  — `:391-556` the gate requirement (**nine** scenarios; §0.4).
* `openspec/changes/add-signed-execution-chain/review/ratification-2026-08-29.md`.

**The S5 rulings, landed on main after both branches cut**
* `openspec/changes/add-wallet-carried-review-authority/rulings-2026-08-29.md` —
  R1–R4 the seat-model target; **R12 the attestation-envelope signer deferral**.

**The composed families**
* `openspec/changes/add-trust-anchor/`, `openspec/changes/add-identity-brokering/`,
  `openspec/changes/implement-openxpki-install-repo/`, `contracts/omnigent/`,
  `openspec/changes/add-wallet-carried-review-authority/`,
  `governance/review-authority/`.

**Governance and lifecycle**
* `docs/document-lifecycle.md` — the controlled `Status:` vocabulary and the
  contested-finding rule (**#509 and both packets' §1.8-style disclosures**).
* `docs/contract-versioning-policy.md`; `contracts/manifest.yaml:3`
  (`contract-v2.2`).
* `openspec/specs/release-realization/spec.md`;
  `openspec/specs/release-surface-integrity/spec.md`.
* openxFactory issues **#502** and **#504** (`govern-sibling-added-modified-deltas`,
  OPEN) — the sibling-delta class.

**The council's own contract (codexFactory `3c71ddc9`, read-only)**
* `hermes/domain/review-councils/gate-rules.yaml`.
* `hermes/domain/roles/{lead-architect,lead-security,lead-quality}.yaml`.
* `hermes/client/role-overrides.yaml` — the CPL specialization and
  `seat_representation` (**the tenant declaration R4 fixed**).
* `hermes/domain/agent-mixes.yaml` — `model_assignments` (merge-readiness only).
* `scripts/merge_master/seat_resolution.py` — the CSC predicate and the
  `ConditionUnevaluable` contract.
* `records/2026-08-29-council-review-add-binding-consumer-identity.md`, its ballot
  and its `records/2026-08-29-seat-returns/` appendix — **the primary precedent**.
* `records/2026-08-28-gate-rules-openxfactory-substantive-classes.md` and ballot.
* `records/2026-08-26-gate-rules-classification-intent.md` §7.4.
* openxFactory neutral persona `templates/client-layer/roles/company-policy-lead.yaml`.
