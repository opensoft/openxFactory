# Council Review Record (§7.4 sitting), 2026-08-30: openxFactory PR #513 `add-chain-anchoring`

Status: record
Record scope: **VALID.** All three operator slots are FILLED, by Brett Heap's
  ruling of **2026-08-30**. Slot 1 acknowledged in the ruling; slot 2 filled as
  liaison — **`lead-security`'s park (LS-C4) is DISPOSED**; slot 3 filled by the
  disposition. **This record carries NO disposition of its own: the SOLE
  disposition of record is `disposition-2026-08-30.md`, cited at §8, and where
  this record and that file differ, THAT FILE GOVERNS.**
  **Read §7 and the disposition's §6 before treating any silence as settled.**

> **THIS RECORD LANDED `NOT VALID` AND WAS FLIPPED BY THE RULING. The history is
> kept, because the flip is the protocol working rather than a correction.**
> **Nothing else in this record has been rewritten to agree with the ruling** —
> the bench's verdicts and findings stand exactly as filed.
Council: `gate_rules_council` (codexFactory
  `hermes/domain/review-councils/gate-rules.yaml`), sitting in the **§7.4
  no-class shape** — sanctioned as a convener act pending a charter amendment
  (codexFactory issue **#131**) and put to this bench again as **T-0(a)**.
Convened: 2026-08-30
Packet: `openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md`
  — **ONE packet, THREE subjects.** Placement explained at §5 of the sibling
  record.
Seat returns (verbatim, evidence appendix):
  `openspec/changes/add-chain-attestation/review/seat-returns-2026-08-30/`
  **This record condenses; the appendix does not. Where a summary here and a
  return there diverge, THE RETURN GOVERNS.**
Ballot (the schedule the seats produced, and the INPUT to any ruling — **not a
  disposition**): `openspec/changes/add-chain-attestation/review/ballot-2026-08-30.md`
Sibling record (#510, the threshold subject):
  `openspec/changes/add-chain-attestation/review/council-review-2026-08-30.md`
Subject: openxFactory pull request **#513**, `add-chain-anchoring` — the
  tranche-THREE OpenSpec proposal packet: **nine ADDED requirements over 52
  scenarios** (verified) in a **NEW capability directory** `specs/chain-anchoring/`,
  with no `## MODIFIED` and no `## REMOVED` block. `proposal.md:8` `Status: draft`;
  7 files, +1884/−0; five commits, four of them fix rounds against bot findings.
  **`openspec/specs/chain-anchoring/` does not exist at `origin/main` and no other
  change or branch writes it** — a genuinely new capability, not a delta over an
  unpromoted one, which is the shape #510 does have.
Also judged in the same sitting: **#510** and **#509**.
Judged at:

```
openxFactory origin/main       afe29561a317853eb22f1e6b248f7029fa2fb2a7
shared merge-base (all three)  b710976b4a4fef277cdd292a407942369e9b9efa
PR #513 head                   cf5a24b89870a87663c595550210ee4deb0ac28e
PR #510 head                   e7f6ae0e400719894fbaa0d14be274ba86b2e3b3
PR #509 head                   26c7e778682089789795befad4c28af509ff2706
codexFactory (read-only)       3c71ddc910b8e0b119d0e1ee40a5523dfa294f07
contracts/manifest.yaml:3      contract_bundle_version: contract-v2.2
```

Precedents: codexFactory
  `records/2026-08-29-council-review-add-binding-consumer-identity.md` and its
  ballot and seat-return appendix — **the PRIMARY precedent**, and the pattern
  `tasks.md:2.3` names by name;
  `records/2026-08-28-gate-rules-openxfactory-substantive-classes.md`;
  `records/2026-08-26-gate-rules-classification-intent.md` §7.4.

---

## 0. THE SCHEDULE IS THE BALLOT, AND THIS RECORD DOES NOT RESTATE IT

The 2026-08-26 round shipped a schedule carrying one fabrication and six
omissions against its own returns and had to be rebuilt; the cause was a record
that *condensed* a schedule which then *competed* with the returns it condensed.
**This record therefore holds no schedule.** Every amendment, condition and
position lives in the ballot, each citing its return.

---

## 1. VERDICT

# **NO REFUSAL. THREE ACCEPT AS AMENDED, ONE ACCEPT. THREE BLOCKING AMENDMENTS.**

| Seat | Verdict on #513 | Blocking |
|---|---|---|
| lead-architect | **ACCEPT** | **none** |
| lead-security | **ACCEPT AS AMENDED** | LS-A5, LS-A6 |
| lead-quality | **ACCEPT AS AMENDED** | LQ-A5 *(its #513 limb)* |
| company-policy-lead | **ACCEPT AS AMENDED** *(charter limb)* | **none** |
| ~~client-security-compliance-officer~~ | **NOT SEATED**. **`lead-security` PARKS the question** | — |
| ~~intent-owner role slot~~ | vacant-symbolic, `binding: symbolic_until_project_roster` | — |

**`split_vote: park_for_liaison` is NOT engaged on the verdict.**
`missing_required_seat: refused` is **satisfied**. **Slot 2 is engaged by LS-C4's
seat-level park** — a park about the SITTING, not about this packet.

**#513 drew the sitting's only unqualified ACCEPT.** LA: *"Its largest decision
(D8) is a faithful, well-recorded narrowing of an UNRULED design observation that
the mechanics make literally unachievable; it consumes the estate's vocabulary and
mints none; its four inherited fixes hold on inspection; and its dependency on an
unratified sibling is expressed honestly and is architecturally true."*

**LQ: *"the strongest-drafted of the three on my measures"*** — 52 scenarios that
all test system behaviour with **no assertions-as-scenarios**, where #510 has
three.

---

## 2. THE THRESHOLD DID NOT REACH THIS PACKET

**T-2 — a ruling on #510 does NOT bind #513.** Unanimous among the three seats
reaching it (CPL: NOT MY SEAT).

**The seats verified the independence rather than accepting the packet's word.**

* **LA:** #513's gates are **Q3 and Q6, both OPEN**, neither dependent on tranche
  two; its subject is reachable from tranche one's transparency log alone, and
  **anchoring a checkpoint of that log requires no link 4**. *"I verified that this
  is architecturally true, not a convenience."*
* **LQ** read #513's entire `spec.md` and confirmed it cites the staged topic, the
  vendored study, #509, `add-trust-anchor` and tranche one — and **no requirement
  of #510**. Its hard prerequisites are declared as tranche one and the PKI plane.
* **LS:** *"None of my #513 findings depends on #510's fate."* **LS-C3** attaches
  that as a condition: LS-F7 and LS-F8 *"are findings about #513's own text and
  stand whatever is ruled on #510; they must not be swept up in a T-1 ruling."*

**#510's threshold was in any case ruled NOT PREMATURE**, so no question of a
consequential ruling arises. **#513 also creates a NEW capability directory**,
confirmed absent at main, so it shares no delta surface with tranche one — the
shape that produced #510's decisive defect.

---

## 3. THE PRE-FLAGGED ITEMS, ANSWERED

### 3.1 D8 — the TWO-ANCHOR narrowing. **The bench holds it CORRECT.**

**And the convening's own characterisation had to be corrected first, against its
own interest.** An earlier draft of the packet called the anchor-late sentence a
**ruled** constraint. It is not. It sits in the staged topic's `## Conflicts`
section — whose second conflict is stamped *"RESOLVED 2026-08-29"* and whose third
is *"left OPEN by design"* — and **carries no ruling stamp, no date and no
disposition-by line**. None of the seven Q-dispositions reaches it; repo-wide the
phrase *"only what has been validated"* resolves to exactly two hits, this
sentence and its INDEX mirror. **The topic is fully ruled as to its seven
questions and unruled as to this constraint.**

**#513 says exactly that in its own requirement text** (`spec.md:316`): *"THIS IS
RECORDED AS A TENSION THE STAGED TOPIC DID NOT RESOLVE, NOT AS A RESTATEMENT OF
IT."*

**LA — whose obligation it was — rules the narrowing faithful**, and it is the
first ground of its ACCEPT. **LS — correct and faithfully recorded on my limb.**
**No seat asked for the narrowing to be undone.**

**The one residual is procedural and it is why the item was on the ballot at
all**: the packet **recorded** the narrowing and did **not route it** among the six
authoring decisions `tasks.md:2.2` puts to the seats. **Recorded is not ruled** —
and the packet's own sentence, *"a topic's constraint is not a packet's to quietly
reinterpret"*, is the argument for routing it. The convening added it as ballot
**C-1** and disclosed that as a convener act.

### 3.2 D2 / D-A — MISSING-WITNESS SEMANTICS. **Right in design; one blocking gap.**

**LS's answer, from driving it:** commit `455bbdaa` **genuinely fixed** the
collision it names — *"by the receipt's own rule, not an exception"* — and the
asymmetry with requirement 6 (**a missing WITNESS degrades a CLAIM about the past;
a missing CONSENT ANSWER refuses an ACT in the present**) is **deliberate and
correct**. **The claim fails closed; the factory does not.** The requirement says
so in terms, and the scenario at `spec.md:253-257` refuses a realization that
would block ratification or merge on anchor completion.

**LS-A5 — BLOCKING.** The fix makes the receipt **stateless**, so *"a one-entry
receipt handed to an independent verifier — the flow requirement 1 exists to
enable — is byte-indistinguishable from a one-witness configuration. **The
fail-closed disclosure cannot travel with the artifact the design exists to make
independently checkable.**"* *Discharged by* requiring the receipt (or a companion
it commits to) to carry the **CONFIGURED witness set at mint time**. **LS notes
this is configuration, not "what has not happened yet", so it does not disturb the
receipt/state split.**

**LS-A6 — BLOCKING.** #513 holds Q6 faithfully and by checks a validator could
really run, **but `grep -E "entropy|random|unguessable"` returns zero**, and the
**KEY** of the keyed commitment has **no custody rule** where the salt has both a
reference and a reachability refusal. *"Q6's erasure property — the authority for
the whole narrowing — rests on two parameters the contract never fixes, against
precisely the attack its own EDPB citation names."*

### 3.3 D6 / D-D — NAMING. **No seat asked for a rename.**

Tranche one names both successors *"(working id)"* on their face. **#513 records
the divergence in a dedicated section** (`proposal.md:96-106`) — *"a reader
arriving from the ratified packet will look for the longer name and should find
out in one place why it is not there"* — **where #510 does not**; grep for the long
id returns zero in #510. LA holds only a back-citation obligation, at **SHOULD-FIX**
(LA-A10). **No seat treats the short ids as a breach.**

---

## 4. WHAT ELSE THE BENCH FOUND

* **LQ-A5 [509][513] — BLOCKING, and it is the one place an error has already
  propagated from brainstorm colour into proposed contract text.** *"Eighteen
  months"* is wrong — 2024-11-10 → 2026-08-29 is **657 days** — and **#513 carries
  it into its own requirement text at `spec.md:658-659`**. **CPL found this
  independently and traced the same propagation.** *Discharged by* correcting it in
  both packets, or striking the interval from #513's requirement text, which does
  not depend on it.
* **LA-A7 — SHOULD-FIX.** Take the *"IN FLIGHT at this revision"* status out of
  **normative** text at `spec.md:546`, `:604` and `:658` — *"promotion carries it
  verbatim"*. The commit's stronger half stays: *"the obligation does not depend on
  the citation … the citation is PROVENANCE."* **This is the one inherited fix LA
  found defective** (`cf5a24b8`); the other three hold on inspection.
* **LS-A7, A8, A9 — SHOULD-FIX.** Bound capture by a declared confirmation depth
  or finality condition (a captured receipt is the only path to complete); make the
  anchor-state record **derivable from and EQUAL to** its evidence-plane leaves —
  *"the same repair #510's P1-2 applied to enumerations"*; and resolve
  `anchor_pending`/`anchor_incomplete` in the healthy path.
* **LQ-A10, A11, A12, A14 — SHOULD-FIX.** A scenario for the **archival-node**
  condition (the one of Q3's three with none); extend requirement 1's capture-time
  refusal to all **four** per-chain elements; give the **aggregation Merkle path** a
  scenario and a negative example; and re-measure the **984** figure, which is
  stale (today **1032**).
* **CPL-A5 — SHOULD-FIX, tenant-facing.** Hedge mid-entry present-tense operative
  language (*"BECOME CONTRACT TEXT"*) in the 83-line README entry, whose own
  opening and closing sentences are already correctly draft-qualified.

---

## 5. WHAT VERIFIED CLEAN — recorded because a record listing only defects misreports the bench

* **The headline counts are right**: 9 ADDED / 52 scenarios, consistent at four
  sites; **SHALL on the first body line of all nine**; ≥1 scenario each; no
  MODIFIED or REMOVED block. `--strict` green; `--all --strict` **79 passed**
  against 78 at main; **doc-health zero-new** with matched basenames per issue
  **#342**.
* **#513 MINTS NO VOCABULARY** (LA) — the one risk the staged topic names first,
  and the one #510 did not clear.
* **#513 edits nothing in the staged topic directory, study included** (LQ, empty
  diff). The standing rule — *a research record rewritten to agree with a later
  ruling stops being evidence* — is **respected**, which answers D-F.
* **Q5's standing tension is held correctly** (LQ, verified positively): today's
  evidence-only posture without constitutionalizing it, **no "never" and no
  trigger**.
* **Zero assertions-dressed-as-scenarios**, where #510 has three (LQ).
* **The declared residual is correctly declared** on `add-trust-anchor`'s ratified
  declared-shortfall pattern rather than asserted closed.
* **The self-correction discipline is real, not performative** (CPL):
  `455bbdaa`'s own message opens *"Self-caught before the bot round"* and shows its
  reasoning rather than asserting a fix.
* **The authorization posture is exemplary** (CPL swept all 28 "Brett" citations
  across both packets): `.openspec.yaml` declines to claim an approver it cannot
  cite **and names the exact prior overreach — tranche one's own corrected origin
  record — that it is deliberately not repeating**.
* **No contract number spent, no schema byte moved**, and `target_release` states
  plainly why no number is written.

---

## 6. THE THREE OPERATOR SLOTS — ALL THREE FILLED 2026-08-30. THIS RECORD IS VALID.

| Slot | Act | State |
|---|---|---|
| 1 | `human_step: acknowledgement_of_notice` | **FILLED** — surfaced in the ballot and acknowledged in the ruling; a non-blocking notice, never a sign-off |
| 2 | Liaison disposition | **FILLED by Brett Heap as liaison.** **LS-C4's park is DISPOSED** by route (ii) — the CSC ground is ruled *inapplicable*, and **a dissent standing through three sittings is discharged**. Full park text at the sibling record §6.1; disposition §3.2 |
| 3 | `output_disposition: convener_accepts_or_rejects_on_record` | **FILLED** — `disposition-2026-08-30.md`, §8 |

**The bench, the resolver failure, the S5 model-target divergence and the
placement decision are identical across both records and are stated once, at the
sibling record §4 and §5.**

---

## 7. WHAT THIS CONVENING DOES NOT DO

* **It does not ratify.** `Status: draft` stands and `tasks.md` §3 has not
  occurred. `tasks.md:2.3`'s obligation — *"Record the sitting in `review/`, on
  `add-binding-consumer-identity`'s pattern: seats, verdicts, blocking amendments,
  and the convener disposition"* — **is discharged as to the first three; the
  convener disposition is slot 3 and is OPEN.**
* **It does not merge, and it pushed nothing to any remote.**
* **It moves no schema byte, cuts no bundle, allocates no minor**, and touches
  nothing under `contracts/`.
* **It re-opens none of the seven Q-dispositions.** Q3, Q6, Q2 and Q5 were read as
  ruled and were applied, never revisited.
* **It does not narrow, widen or ratify D8's narrowing** — it records that the
  bench holds it correct and that a ruling on it is Brett's (ballot C-1).
* **It does not decide #502 or #504**, and this packet was not delayed for them.

**All of the above remains true OF THE SITTING and is not amended by the ruling.**
The ruling is a separate, later act by Brett; §8 records it.

---

## 8. THE DISPOSITION — Brett Heap, 2026-08-30

**THE SOLE DISPOSITION OF RECORD IS
[`disposition-2026-08-30.md`](disposition-2026-08-30.md)**, carried
byte-identically here and in #510's bundle. **This section is a pointer, not a
restatement**, so that one act cannot drift into two records. **Where this record
and that file differ, THAT FILE GOVERNS.**

**The ruling, verbatim:**

> **"accept all fifteen as recommended, 14 folds into the fix rounds."**

**What it means for #513, in one paragraph.** All fifteen ballot §12 decisions are
adopted as recommended. **Item 6 rules the D8 narrowing CORRECT AND FAITHFULLY
RECORDED — the narrowing stands** — and pairs it with a process rule for future
packets, §8.1. **All three blocking amendments are accepted** (LS-A5, LS-A6, and
LQ-A5's #513 limb), and **item 5 requires LQ-A5 be carried into this packet's
REQUIREMENT TEXT at `spec.md:658-659`, not only into #509's appendix**. **Item 14
folds one further finding in**: Codex's *"Require de-identification before
treating metadata as reusable"*, raised on #509, is assigned **to this packet's
fix round for its REQUIREMENT-8 limb** as well as to #509's own text (disposition
§4). **T-2 stood — #510's threshold ruling did not reach this packet** — and item
12 leaves `add-chain-anchoring` standing as the change id, this packet having
already made the back-citation #510 owes.

**`tasks.md:2.3`'s obligation is now DISCHARGED IN FULL** — *"Record the sitting
in `review/` … seats, verdicts, blocking amendments, and the convener
disposition."* The first three are this record; **the convener disposition is
§8.**

### 8.1 The routing rule this packet's own decision produced

**Item 6 is adopted in both halves.** The D8 narrowing is ruled correct; **and it
is now on the record that a packet which NARROWS a constraint carried in a staged
topic SHALL ROUTE the narrowing to its council as an explicit decision, not
merely RECORD it in its own text.**

**This is a process obligation on future packets and NOT a defect finding against
#513**, whose narrowing is ruled correct. The rule is this packet's own sentence,
now binding: *"a topic's constraint is not a packet's to quietly reinterpret."*
The companion fact travels with it — **a constraint sitting inside a fully-ruled
topic is not thereby ruled**, and `## Conflicts` sections carry unruled material
by design.

**Read the disposition's §6 before treating any silence as settled**: the
should-fix schedule item by item, B-8, and every convening finding at ballot §X
except those ruled by items 14 and 15 are **UNDISPOSED**.

---

## 9. FOR THE NEXT SITTING

* **A packet that narrows a topic constraint should ROUTE the narrowing, not only
  record it.** #513 did the hard half — the narrowing is in requirement text, in
  design, and in the PR record — and then left it out of the six decisions it put
  to the council. **The convening had to add it.** #513's own sentence is the rule:
  *"a topic's constraint is not a packet's to quietly reinterpret."*
* **A constraint inside a fully-ruled topic is not thereby ruled.** The convening
  itself got this wrong in a first draft and corrected it before the seats read the
  packet. **`## Conflicts` sections carry unruled material by design**, and two of
  this topic's three conflicts carry disposition stamps while the third does not.
* **An error can propagate from a brainstorm into requirement text in one hop.**
  *"Eighteen months"* travelled from #509's appendix into #513's `spec.md:658`
  before either landed. **LQ-C1 and CPL-C1 both flag the moment it stops being
  free brainstorm content and becomes governed text carrying a false claim.**
* **LS-A5 is the sharpest general lesson here:** a fail-closed state that a
  verifier cannot see **in the artifact** is not fail-closed for that verifier.
  The receipt/state split is right; what it cost was the incompleteness's ability
  to travel.
