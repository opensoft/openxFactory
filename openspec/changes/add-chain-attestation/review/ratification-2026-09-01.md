# Proposal Ratification: add-chain-attestation (tranche two)

Status: ratified
Decision date: 2026-09-01
Ratifier: Brett Heap (repository owner) — in-session, on the recorded word
Ratified: 2026-09-01 by Brett Heap (repository owner) — in-session; record: this
file.
Ratified baseline: this change as committed at `dd847e44`, the head this ruling
names (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`specs/signed-execution-chain/spec.md` — **NINE ADDED requirements over 104
scenarios, plus TWO scenario-complete `## MODIFIED Requirements` over 17
scenarios**), validated `--strict` and `--all --strict`, doc-health zero-new,
and verified by the archive construction the council itself prescribed.

## Decision

**RATIFY.** The requirement set stands as it is at this record's commit.

This change is **TRANCHE TWO of the `signed-execution-chain` family — links 4–6
and 10**: the harness-controller setup attestation, the per-task runner
attestations, the signed pull-request-open decision, and the governed post-merge
test that CLOSES a chain. It realizes the declaration tranche one could only
make — that the signed hash-link rule takes effect at the first link with a
signer of its own — and extends the running gate from links 1–3 to links 1–6.

**This ratification authorizes realization; it does not perform it.** The change
carries a code surface and `target_release: the next additive minor`, so it
archives only on merged code with green realization evidence. **No contract byte
moves with this ratification**, no number is spent, and `contracts/` is untouched
by the ratified diff.

---

## 1. THE RULING SEQUENCE, COMPLETE AND VERBATIM

**Eight rulings bear on this packet's basis question. Two were superseded before
they could operate, and BOTH ARE RECORDED HERE WITH THE REASON** — because a
ratification record that showed only the ruling that succeeded would misrepresent
how this decision was actually reached.

| # | Date | Verbatim | Effect |
|---|---|---|---|
| 1 | 2026-08-30 | *"accept all fifteen as recommended, 14 folds into the fix rounds."* | The combined §7.4 sitting's ballot. #510's blocking set became THIRTEEN — eleven, plus LS-A10 and LQ-A13 elevated by decision 13. |
| 2 | 2026-08-30 | *"1 yes, 2 yes with note, 3 merge, 4a, 5 bless, 6a."* | The six-item closing queue. Item 1 is this packet's ratification; item 4a is the frozen-bundle header normalization, performed 2026-08-30. |
| 3 | 2026-08-30 | *"if clean, ratify and merge the batch."* | The condition that governed every basis after it. |
| 4 | 2026-08-31 | *"proceed on the silence basis, ratify and merge."* | **MOOTED.** A Codex verdict on the then-head surfaced in the gap between the ruling and its execution. The basis was an ABSENCE of review; the absence ended before the act. |
| 5 | 2026-08-31 | *"if clean, ratify and merge on the positive verdict."* | **THE POSITIVE-VERDICT RULE**, set after the silence basis failed. Ratification re-presents only against a review whose `Reviewed commit` names the head, with its comments enumerated. |
| 6 | 2026-08-31 | *"3 — merge #509 and #513 now, #510 waits for its verdict."* | **THE BATCH SPLIT.** Both siblings merged — #509 at `698a5fc9`, #513 at `f8f4cb5f` — and this packet was held back for its own verdict. |
| 7 | 2026-08-31 | *"proceed on the prescribed-fix basis, ratify and merge #510."* | **MOOTED.** Its stated premise — that the head was bot-unreviewed — was false at the moment of execution: Codex had reviewed that head and returned FOUR P1s, including a forgeable tier-2 identity. |
| 8 | **2026-09-01** | **"proceed on the prescribed-fix basis, ratify and merge #510."** | **THIS RULING.** The second issuance of the basis, given with the full history before him and against a disclosed state. |

**RULINGS 4 AND 7 ARE THE REASON THIS RECORD IS SHAPED AS IT IS.** Twice a basis
resting on an absence of review was overtaken by a verdict arriving in the
interval, and on both occasions the packet's author STOPPED rather than write a
ratification record whose stated premise had become false. **Those stops are part
of this ratification's provenance**, not a preamble to it: a record asserting a
clean head at the one link with no gate behind it is the exact defect this whole
capability exists to refuse.

---

## 2. THE BASIS, AND WHAT MAKES THIS HEAD DIFFERENT

### 2.1 The prescribed-fix principle, at its cleanest fit since #125

**`dd847e44`'s diff implements THE REVIEWER'S OWN REMEDY**, in substance and
close to verbatim. The round-eighteen finding closed with:

> *"add the ratification fields and their amendment-record shape to the owned
> schema and realization surface."*

That is precisely what the head does, by **ROUTE A** — a second scenario-complete
`## MODIFIED` requirement on tranche one's ratification/chain-inception record,
adding the three amendment-lineage fields — **and the route was justified against
four preconditions verified in the artifacts rather than assumed:**

1. **~~Tranche one is RATIFIED-NOT-REALIZED~~ — THIS GROUND WAS TRUE AT
   `dd847e44` AND IS SUPERSEDED. SEE §7.** It was verified in the artifacts at
   the head this ruling named; PR #524 (`9af98c4d`) had by then realized tranche
   one at `contract-v2.5`, which the merge-up surfaced. **Brett re-grounded Route
   A on 2026-09-01 ("route A"):** the MODIFIED on tranche one's REQUIREMENT TEXT is
   lawful canon amendment, and its schema consequence is an **ADDITIVE EXTENSION
   of the shipped `chain-inception.schema.yaml` at this packet's own cut**, on the
   #497 precedent.
2. **This packet already held the instrument by the council's own prescription** —
   LA-A1's scenario-complete MODIFIED on tranche one's gate requirement. Precedent
   applied, not set. All SIX scenarios of the ratification requirement restated
   verbatim (PR #331's rule), plus two for the lineage.
3. **No sibling delta collides.** Only tranche one and this packet write to
   `signed-execution-chain`.
4. **The archive-order dependency is the one already carried**, not widened.

The alternative — an eighth record kind owned here — is recorded as **considered
and ruled against** at `design.md` D12, on the ground that it would put the
lineage in a record the ratifying signature does not cover.

**This is the prescribed-fix principle's cleanest fit since it was first applied
at #125**: the change under ratification is the change the reviewer asked for.

### 2.2 The review state, stated exactly

**The head is bot-unreviewed by Codex after the full procedure.** Verified by
paginated read as the last act before this record was written:

```
paginated Codex reviews on #510        21
last review's Reviewed commit          416fed22
reviews naming dd847e44                 0
```

Three request forms were used across 4+ hours — the summary comment's embedded
`@codex review`, and two subsequent bare requests. **No response and no refusal
message.**

### 2.3 THE ONE CORRECTION TO THE RULING'S PREMISE, MADE ON THE RECORD

**The ruling was put with the premise "ZERO reviews or comments on `dd847e44`".
The reviews half is exact. The comments half is not: FOUR COPILOT COMMENTS were
filed against this head at 2026-08-31T21:15Z.** They are recorded here rather
than passed over, because this record does not repeat the failure that mooted
rulings 4 and 7.

**They are one finding repeated at four sites, and it is REFUTED ON THE FACTS:**

| Copilot's claim | Measured |
|---|---|
| *"104 scenarios is the **combined promoted canon** after archiving tranche one + this packet (18 requirements / 104 scenarios)"* | **FALSE.** The promoted canon is **151 scenarios**. **104 is the ADDED delta count**, exactly as the announcement sites say. |
| *"tranche two is described as '9 ADDED / 59 scenarios'"*, citing `review/council-review-2026-08-30.md:39-40` | **59 was the ADDED count AT THE SITTING**, before eighteen bot rounds. That record is **frozen by the disposition's §3.7** and must not be updated; its figure is history, not a competing current count. |
| *"reads as though the 9 ADDED requirements themselves have 104 scenarios"* | **They do.** That is what the sentence means and it is true. |

**No byte is owed.** The live text already names both halves distinctly — *"NINE
ADDED requirements over 104 scenarios, plus TWO `## MODIFIED Requirements` — 2
requirements over 17 scenarios"* — and the only live mention of "59" is inside
`tasks.md` 1.23's own history entry, which labels it **PRE-COUNCIL state**.

**This is the second time Copilot's count advice has been directionally wrong on
this packet** — it earlier asked that a *measured* 89 be reconciled down to a
*stale* 85 — and the packet's standing answer is recorded at `tasks.md` 1.22:
**a majority of stale sites is not a measurement.**

**Ratification therefore proceeds on the head the ruling names, unedited.**
Correcting phrasing first would have produced a different head than the one Brett
ruled on, for a finding that is wrong.

### 2.4 What this basis does not claim

**A later bot finding on the ratified text routes to the AMENDMENT LANE**, not to
doubt about this act's validity. That is the same disposition every ratification
in this family carries, and it is the honest reading of a prescribed-fix basis:
the act is sound on what was known and disclosed, and the text stays open to
improvement.

---

## 3. THE PACKET'S STATE AT RATIFICATION

### 3.1 What was answered

* **THIRTEEN COUNCIL AMENDMENTS**, all discharged — LA-A1, LA-A2, LA-A3, LA-A5 ·
  LS-A1, LS-A2, LS-A3 · LQ-A1, LQ-A2, LQ-A3, LQ-A4 · **LS-A10** and **LQ-A13**,
  both filed SHOULD-FIX by their seats and **ELEVATED TO BLOCKING** by decision 13.
  The bench was **UNANIMOUS 4/4** that the drafted text was not ratifiable.
* **EIGHTEEN BOT ROUNDS**, all answered from the record with citations.
* **RULING 4a PERFORMED** — the record owner's deterministic normalization of the
  frozen bundle headers, after which doc-health reports **zero new findings
  overall**, not zero-with-a-known-exception.

### 3.2 What the artifacts measure

| Measure | Value |
|---|---|
| ADDED delta | **9 requirements / 104 scenarios** |
| MODIFIED delta | **2 requirements / 17 scenarios**, each scenario-complete |
| Promoted canon (archive construction) | **18 requirements / 151 scenarios** |
| Canon contradiction check | **contradiction-free** |
| Permitting antecedents in canon | **5, each read against every rival and disjoint from all** |
| Fixture-equality screen | 91 of 92 behaviour-naming scenarios matched; the remainder a hand-verified synonym |
| Both-axis equality (5.4 ↔ `code_surface`) | record kinds **7/7/7**, field disciplines **3/3/3** — **HOLDS** |
| `openspec validate --strict` / `--all --strict` | valid / **79 passed, 0 failed** |
| doc-health vs `origin/main` (matched basename) | **0 new findings** |

**THE FIVE PERMITS ARE REPORTED HONESTLY RATHER THAN DRIVEN TO ZERO.** Each is a
genuine permitting scenario — the not-yet-in-force link, the named-reader rule,
the runner-claimed measurement, the unamended-review closure, and the zero-length
lineage — and each was read against every rival refusal and found to share an
antecedent with none.

### 3.3 The methods the rounds paid for

**Six standing sweep rules are recorded at `tasks.md` 1.22**, each because its
absence cost a round: the announcement-family sweep firing on any count-moving
commit; the two-field sweep (assertions AND commissions); the guard walk over
every permitting conjunct set **including sets a previous walk touched**; the
set-read after amending a requirement; **one rule, not slots**; equality checks
covering **every declared axis**; and the retire rule — **subject-keyed, never
phrase-keyed**, because grepping the old phrase is itself the defect.

**The D-series carries the reasoning**: D1–D10 (the packet's own decisions and the
first bot round), D11 · D11a · D11b · D11c (the constructibility family, the
subject split, bind-before-sign's last limb, and the split's own residue), and
**D12** (the lineage fields' home, with Route B recorded as ruled against).

---

## 4. RATIFIED-NOT-REALIZED

**Ratification authorizes ONE contract feature plus the extension of an existing
gate. It performs no realization**, creates no certificate authority, mints no
attestation identity, deploys nothing, and moves no contract byte.

**§5's gates stand and are not discharged by this act:**

* **THE RAISING-TIME RE-DERIVATION IS PERFORMED** (`design.md` D7a, dated
  2026-08-30) and confirms links 4–6 and 10 with no link moved. **The
  REALIZATION-time re-derivation at `tasks.md` 5.1 is a SECOND obligation** and is
  made decidable there — both observables named, and the artifact it must produce.
* **THE OMNIGENT LAYER must be real enough to enforce a precondition**, and
  **`implement-openxpki-install-repo` real enough to issue a controller
  certificate.** Neither is today. Requirement 9 is UNMET rather than partially
  met until a running layer refuses.
* **THE CROSS-TRANCHE COMMISSIONING NOTE STANDS.** `tasks.md` 5.4 commissions the
  three amendment-lineage fields on **tranche one's** ratification record, because
  that family's contract surface has not been cut. **Whichever tranche's
  realization lands first must author them**, and the task says so, so neither can
  assume the other did.

---

## 5. WHAT THIS RATIFICATION DOES NOT COVER

* **It does not ratify the realization.** `tasks.md` §4–§6 are authorized, not
  performed. The change stays ACTIVE until merged code, green evidence and the
  contract cut exist.
* **It does not merge this pull request.** That is the orchestrator's act on
  ruling 3.
* **It does not settle the should-fix schedule**, which the disposition left
  UNDISPOSED (§6) and which `tasks.md` 2.8 keeps open by name — including LA-A6,
  now load-bearing because the MODIFIED blocks depend on tranche one archiving
  first.
* **It does not correct the frozen sitting artifacts.** The seat-returns
  appendix's *"Sixteen blocking amendments"* over a breakdown summing to
  seventeen is a **PRESERVED ERROR**, recorded at `tasks.md` 1.17 on the
  disposition's §3.7 ground, and is the record owner's alone to normalize.
* **It does not close codexFactory #131**, the charter obligation decision 8 made
  a standing condition on the convening pattern.

---

## 7. WHAT ARRIVED AFTER THIS RATIFICATION, AND WHAT IT CHANGED

**THIS RECORD TRUTHFULLY RATIFIED `f54cb5bc`. IT IS KEPT AS WRITTEN AND EXTENDED
HERE, BECAUSE TWO THINGS ARRIVED AFTER THE ACT AND A RECORD THAT ABSORBED THEM
SILENTLY WOULD BE THE DEFECT THIS CAPABILITY EXISTS TO REFUSE.**

### 7.1 The verdict on the ratified head — Codex review 22

**A Codex review naming `f54cb5bc` arrived after the ratification**, the sixth
time in this arc a verdict landed in a gap. It carried **THREE P1s and a P2**:

| id | finding | discharged |
|---|---|---|
| `3899739417` | **A rival authority-proven review of the same bytes could close the chain** — limb 1 compared SUBJECTS, not review IDENTITY; and the committed fields named no review record, so **limb 2 was not constructible as written** | the ratifying bytes now commit to **THE CONSUMED REVIEW RECORD'S OWN DIGEST** (a fourth lineage field), and limb 1 compares identity twice — against that digest AND against the review the amendment record names |
| `3899739435` | **Link 6 bound to no pull request** — a decision reused after a branch move, a retarget, or attached to another PR on the same chain permitted a merge of work the controller never signed as proposed | the signed decision now carries the **PR identifier and head revision**, and the gate refuses unless both EQUAL the merge |
| `3899739441` | **A no-op test could close the chain** — rounds four and seven hardened the OUTCOME and never checked the test was the RIGHT test; *"governed"* constrained nothing checkable | the **ratified subject names the governed test**, the controller dispatches THAT test, and the closure record's test identity must EQUAL it |
| `3899739426` | `proposal.md`'s section heading still said ONE MODIFIED block | corrected to TWO |

Plus a Copilot finding that the **pull-request description** still described the
packet as a draft — the announcement family's outermost member — now corrected.

### 7.2 The ground correction

The merge-up against `main` surfaced that **PR #524 (`9af98c4d`) had realized
tranche one at `contract-v2.5`**, falsifying Route A's first precondition as
stated at §2.1. The merge was **aborted rather than pushed**, because pushing it
would have landed a ratification record the same tree disproves. Brett was given
the correction in full and ruled:

> **"route A"** — Brett Heap, 2026-09-01

**The route stands; its ground moves.** The lineage fields land as an **additive
extension of the realized tranche-one schema at this packet's own release cut**,
per the #497 precedent — `add-binding-consumer-identity`, ratified extending a
SHIPPED schema with an additive optional block. `design.md` D12 carries the
superseded ground **marked and dated** rather than rewritten, and records that
**Route B's refusal ground is unaffected**, having never depended on tranche one
being uncut.

### 7.3 The standing of this record

**THE RATIFICATION OF `f54cb5bc` STANDS AS THE ACT IT WAS** — given at a head
whose disclosed state Brett ruled against, and truthfully recorded here.
**RE-RATIFICATION IS PENDING FOR THE AMENDED HEAD.** The packet's status is
therefore **RATIFIED-THEN-AMENDED**: not a draft, and not currently-ratified
text. `approved_on` stands as the history of the act it records, not as a claim
about the amended text.

## 6. NEXT

Realization per `tasks.md` §5, gated on both planes being real. The mirror of the
2026-08-30 sitting to codexFactory `hermes/domain/review-councils/` remains owed
(disposition §8). Tranche three, `add-chain-anchoring`, merged 2026-08-31 at
`f8f4cb5f` and carries its own realization.
