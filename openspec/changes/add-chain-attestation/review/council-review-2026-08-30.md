# Council Review Record (§7.4 sitting), 2026-08-30: openxFactory PR #510 `add-chain-attestation`

Status: record
Record scope: **VALID.** All three operator slots are FILLED, by Brett Heap's
  ruling of **2026-08-30**. Slot 1 acknowledged in the ruling; slot 2 filled as
  liaison — **`lead-security`'s park (LS-C4) is DISPOSED**; slot 3 filled by the
  disposition. **This record carries NO disposition of its own: the SOLE
  disposition of record is `disposition-2026-08-30.md`, cited at §8, and where
  this record and that file differ, THAT FILE GOVERNS.**
  **Read §7 and the disposition's §6 before treating any silence as settled** —
  a valid record is one whose operator slots are filled, not one with nothing
  left owed.

> **THIS RECORD LANDED `NOT VALID` AND WAS FLIPPED BY THE RULING. The history is
> kept, because the flip is the protocol working rather than a correction.** As
> first written it read **DRAFT. NOT VALID**, with all three slots open and slot 2
> engaged by LS-C4's park, and it stated plainly that it carried no disposition.
> All three are now filled. **Nothing else in this record has been rewritten to
> agree with the ruling** — the bench's verdicts, findings and the convening's own
> errors stand exactly as filed.
Council: `gate_rules_council` (codexFactory
  `hermes/domain/review-councils/gate-rules.yaml`), sitting in the **§7.4
  no-class shape** — a seating the charter does not reach, sanctioned as a
  convener act pending a charter amendment (codexFactory issue **#131**) and put
  to this bench again as **T-0(a)**.
Convened: 2026-08-30
Packet: `openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md`
  — **ONE packet, THREE subjects.** Its placement under this change's `review/`
  is a convener act, explained at §5.
Seat returns (verbatim, evidence appendix):
  `openspec/changes/add-chain-attestation/review/seat-returns-2026-08-30/`
  **This record condenses; the appendix does not. Where a summary here and a
  return there diverge, THE RETURN GOVERNS.**
Ballot (the schedule the seats produced, and the INPUT to any ruling — **not a
  disposition**): `openspec/changes/add-chain-attestation/review/ballot-2026-08-30.md`
Sibling record (#513): `openspec/changes/add-chain-anchoring/review/council-review-2026-08-30.md`
Subject: openxFactory pull request **#510**, `add-chain-attestation` — the
  tranche-TWO OpenSpec proposal packet of the `signed-execution-chain` family:
  links 4–6 and 10, **nine ADDED requirements over 59 scenarios** (verified by
  three seats), with **no `## MODIFIED Requirements` block anywhere**.
  `proposal.md:4` `Status: draft`; 7 files, +1741/−0; `contracts/` untouched.
  **The PR is `isDraft: false` on GitHub notwithstanding its text** — ballot §X.9.
Also judged in the same sitting: **#513** (`add-chain-anchoring`) and **#509**
  (the MedxChain brainstorm vendoring). #509 is carried in the ballot and here,
  because `ideation/` holds no `review/` directory anywhere (§5).
Judged at:

```
openxFactory origin/main       afe29561a317853eb22f1e6b248f7029fa2fb2a7
shared merge-base (all three)  b710976b4a4fef277cdd292a407942369e9b9efa
PR #510 head                   e7f6ae0e400719894fbaa0d14be274ba86b2e3b3
PR #513 head                   cf5a24b89870a87663c595550210ee4deb0ac28e
PR #509 head                   26c7e778682089789795befad4c28af509ff2706
codexFactory (read-only)       3c71ddc910b8e0b119d0e1ee40a5523dfa294f07
contracts/manifest.yaml:3      contract_bundle_version: contract-v2.2
```

Precedents: codexFactory
  `records/2026-08-29-council-review-add-binding-consumer-identity.md`, its ballot
  and its seat-return appendix — **the PRIMARY precedent** (same repository, same
  §7.4 path, ruled by Brett);
  `records/2026-08-28-gate-rules-openxfactory-substantive-classes.md` and its
  ballot — the packet/return/ballot shape and the independence discipline;
  `records/2026-08-26-gate-rules-classification-intent.md` §7.4 — the no-class
  path this sitting executes.

---

## 0. THE SCHEDULE IS THE BALLOT, AND THIS RECORD DOES NOT RESTATE IT

The 2026-08-26 round shipped a schedule carrying one fabrication and six
omissions against its own seat returns and had to be rebuilt; the structural
cause was a record that *condensed* a schedule which then *competed* with the
returns it condensed. **This record therefore holds no schedule.** Every
amendment, condition, ballot position and open decision lives in the ballot,
where each item cites the return it derives from. There is one schedule, in one
place, and it can be checked line by line against the appendix.

---

## 1. VERDICT

# **UNANIMOUS 4/4 — ACCEPT AS AMENDED. ELEVEN BLOCKING AMENDMENTS ACROSS THREE SEATS.**

| Seat | Verdict on #510 | Blocking |
|---|---|---|
| lead-architect | **ACCEPT AS AMENDED** | LA-A1, LA-A2, LA-A3, LA-A5 |
| lead-security | **ACCEPT AS AMENDED** | LS-A1, LS-A2, LS-A3 |
| lead-quality | **ACCEPT AS AMENDED** *(recording that the text as drafted is **not ratifiable**)* | LQ-A1, LQ-A2, LQ-A3, LQ-A4 |
| company-policy-lead | **ACCEPT AS AMENDED** *(charter limb; conditional on T-1)* | **none, and the seat says so** |
| ~~client-security-compliance-officer~~ | **NOT SEATED** — §4.2. **`lead-security` PARKS the question** | — |
| ~~intent-owner role slot~~ | vacant-symbolic, `binding: symbolic_until_project_roster` — not missing | — |

**`split_vote: park_for_liaison` is NOT engaged on the verdict** — the first §7.4
sitting since that procedure was defined at which it is not.
`missing_required_seat: refused` is **satisfied**. **Slot 2 is nonetheless engaged
by LS-C4's seat-level park** (§6.1).

**No seat refused. No seat refused the packet's purpose.** LQ: *"The packet is
genuinely well-built — every count it makes about itself is correct, every
requirement carries SHALL on line one, doc-health is zero-new, and it does not
outrun its machinery anywhere I could find, including under a live ruleset
read."* **And the same seat records, in the 2026-08-29 formula, that the text as
drafted is not ratifiable.**

---

## 2. THE THRESHOLD, RULED FIRST — **#510 IS NOT PREMATURE. THE ROUND DID NOT END.**

`tasks.md:88-92` required this and required it first: *"A ruling that the packet
is premature ends the round; nothing below it survives."*

**Three seats reach T-1; `company-policy-lead` returns NOT MY SEAT and names
`lead-architect`, as the packet's own obligations table assigned it.**

* **lead-architect — (c) NOT PREMATURE BUT NARROWED.**
* **lead-security — (a) NOT PREMATURE** on the security limb, caveat LS-F1.
* **lead-quality — (a) NOT PREMATURE** on the testability limb, caveat LQ-F17.

**LA's ground is a distinction of OBJECTS, and it is what reconciles three ruled
texts that otherwise collide:**

> The estate contains three texts and they are consistent **only if their objects
> are kept distinct** … Q4's object is the **boundary**; the Exit path's object is
> the **contract text** (*"may now NAME the mechanism"*). Drafting is permitted.
> But tranche one's ratified `tasks.md:5.3` fixes the trigger at "**when each is
> raised**" — #510 IS the raising, relocates it to realization, and never cites
> it.

**LA verified D7's supporting precedent rather than accepting it** —
`add-trust-anchor` did stay conformant against a certificate authority the family
does not operate — *"which is why (c) not (b)."*

**The narrowing is LA-A5 and it is BLOCKING**: perform the raising-time
re-derivation now, cite `add-signed-execution-chain/tasks.md:5.3` by path and
text, state what exists today, state the boundary derived from it, and keep
`tasks.md:5.1` as the SECOND, realization-time re-derivation rather than a
substitute for the first. **LA is explicit that this is an act of authorship, not
a re-ruling: *"Q4 stays exactly as Brett ruled it."***

**T-2 — a ruling on #510 does NOT bind #513.** Unanimous among the three seats
reaching it. LA verified the independence architecturally; LQ read #513's entire
`spec.md` and confirmed it cites **no requirement of #510**; LS: *"None of my
#513 findings depends on #510's fate."*

---

## 3. THE FINDING

**#510's gate extension is drafted as an ADDED requirement composing with tranche
one's by a prose reading. Built into the canon it would actually promote, the two
requirements hold TWO CONTRADICTORY SCENARIOS ON ONE ANTECEDENT — and every
validator in the estate passes.**

`lead-architect` did not read this; it constructed it. It copied
`invmain/openspec`, dropped #510's delta beside tranche one's, and ran
`openspec archive` **twice**:

```
promoted canon, 18 requirements / 104 scenarios, `openspec` reports `~ 0` modified

  :552    a chain carrying no attestation link
          -> "validates links 1–3 … the absent later link is not reported as a break"
  :1141   the same chain, after this tranche
          -> REFUSES
```

**Both normative. Both promoted.** #510's prose — that tranche one's scope note is
*"SELF-LIMITING and SPENT HERE"* — **cannot repeal a scenario living inside a
different requirement.** LA's answer to its own assigned obligation: *"the gate
self-limits its scope note and NOT its closed-list claim."*

### 3.1 What else the same construction produced

* **An orphaned closed-list obligation.** Tranche one's *"**THE LIST IS CLOSED** …
  every requirement of **this capability** is either walked here or has its
  enforcement point named below"* is scoped to the CAPABILITY, not the tranche.
  Its mapping table carries **9 rows against 18 promoted requirements**, so canon
  would assert that #510's own nine requirements are ones *"this capability does
  not enforce."* **#510 never touches that clause** — grep returns zero. **LA-A2.**
* **A silent archive-order hazard.** Archiving #510 FIRST yields
  `signed-execution-chain: create` carrying only tranche two's nine requirements.
  **Both orders succeed silently.** LA-A6 (should-fix).

### 3.2 The minted vocabulary — the family's own first-named risk

The staged topic names it (`:465-469`): *"inventing a second identity or
certificate vocabulary … a new schema here would be the 'two records of one
decision' defect at contract scale."*

**LA resolved every one of the six cited authorities. Five are genuinely
CONSUMED** — the omnigent citation verifies byte-exact against the schema (six
booleans, `additionalProperties: false`, `execute_final_action` and
`access_secrets` both `const: false`, exactly five archetypes), a precision LS
independently confirmed by walking the same schema.

**The sixth is MINTED**: an evidence class whose member **`hardware_attested` is
precisely the `excluded_models: asserted_hardware_backing` entry that the ratified
`contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml` rules out** —
*"hardware … belongs in `notes`, never a tier."* **Zero references to that registry
anywhere in #510.** The class carries strength semantics with no ranks and no
`composes_with`. **LA-A3.**

### 3.3 What does NOT hold under subtraction — three fail-closed defects

`lead-security` drove each rule by removing conditions one at a time.

* **LS-A1 — the strongest.** The P1-3 fix binds link-10 closure — the link **#510
  itself calls *"the one with no gate behind it"*** — to revocation standing
  *"current at exercise"*, drawn from `governance/review-authority/register.yaml`,
  **whose own ratified header declares a file-based register cannot satisfy
  revocation-at-exercise and *"must not be pretended into a revocation
  surface"***. Zero hits in #510 for register / revocation surface / live lookup /
  S5. LS: *"a bot-prescribed fix applied without running it against its
  instrument."*
* **LS-A2.** P1-1's mandatory refusal is undone 19 lines later by a
  declared-shortfall escape; `grep "per-task attribution"` returns **two hits,
  both inside the escape itself**. **The disqualified set has no members.** *"The
  fix repairs the record, not the control: the exact shape D10 says all three P1s
  had."*
* **LS-A3.** Every enumerated tier-2 condition genuinely refuses when the others
  are removed — *"the depth is real"* — but
  `grep -E "co-locat|isolat|trust boundary|same host"` returns **zero** across all
  seven files. *"In every configuration"* enumerates **hand-overs**, never
  **reachability**: a controller co-resident with a self-hosted runner hands
  nothing across and is **conformant as drafted**.

### 3.4 What is not testable as drafted

* **LQ-A2** — two scenarios (`:159`, `:177`) give **opposite consequents on the
  same antecedent** with no distinguisher in the requirement body. **The same
  defect family as §3, found independently in a different requirement.**
* **LQ-A3** — nothing orders link-5 leaves before link-6's, so *"a lane that
  defers an unwanted leaf past its successor passes the gate with an EQUAL
  enumeration. The P1-2 fix moved the attack rather than closing it."*
* **LQ-A4** — **D6, routed to this council at `tasks.md:2.5`, has zero scenarios
  and no SHALL.** The bench cannot rule a decision with no requirement text.

### 3.5 A PRESERVED CONFLICT BETWEEN TWO SEATS, NOT RECONCILED

**LA judged P1-2's repair *"the sitting's best engineering (log-derived set,
EQUALITY both directions) — I could not break it."* LQ broke it**, by a route LA
did not take (LQ-A3). **Both returns stand.** This record does not pick between
them, because it is a disagreement of judgement resting on different attacks
rather than a disagreement of measurement — and the rule that a numeric conflict
must be reconciled does not reach a conflict of attack.

### 3.6 What the finding does NOT defeat

**Every count #510 makes about itself is correct** (LQ, by script): 9 ADDED / 59
scenarios consistent at four sites; **SHALL on the first body line of all nine**;
≥1 scenario each; no MODIFIED or REMOVED block; `--strict` green; `--all --strict`
**79 passed** against 78 at main; doc-health zero-new with matched basenames per
issue #342.

**And on the estate's most-recorded defect family — claims outrunning the
machinery — LQ found NOTHING BLOCKING.** The one ASSERTED live claim survives a
**live ruleset read**: ruleset `21538893`, enforcement active, `~DEFAULT_BRANCH`,
`required_status_checks: wallet-validation, pytest-suite`. *"Everything else is
DECLARED with a cite."*

**The amendments are of the text as drafted, not of the tranche.**

---

## 4. THE BENCH, RESOLVED HONESTLY

| Seat | Layer | Basis | Model |
|---|---|---|---|
| lead-architect | domain | `members.domain` | inherited (`opus`) |
| lead-security | domain | `members.domain` | inherited (`opus`) |
| lead-quality | domain | `members.domain` | inherited (`opus`) |
| company-policy-lead | client | `members.client.seat`; `missing_required_seat: refused` | **`sonnet`**, per codexFactory `hermes/client/role-overrides.yaml` `seat_representation` — **the TENANT's declaration**, which R4 fixed as the authority the domain lane consumes |
| ~~client-security-compliance-officer~~ | client | conjunction pull-in — **NOT SEATED**, §4.2 | — |
| ~~intent-owner role slot~~ | project | `binding: symbolic_until_project_roster` — vacant-symbolic, not missing | — |

### 4.1 The shipped resolver still cannot read this council's document — FIFTH consecutive convening

Executed at codexFactory `3c71ddc9` rather than cited:

```
ConditionError: council.members must be a non-empty list — the unconditional domain roster
```

`gate-rules.yaml`'s `members` is a mapping; the evaluator requires a list. **The
bench above was HAND-ASSEMBLED, and this record says so rather than presenting a
hand roster as a tool output.** codexFactory task 5.9a stays open. **The ordinal
was verified against the estate's own headings** — 2026-08-28 "third",
2026-08-29 "FOURTH" — rather than inherited; the ballot records that it was
inherited when first written (§Y.6).

### 4.2 The CSC seat was NOT seated, and `lead-security` PARKS rather than dissents

Fed the subjects' real reach the conjunction predicate does not hold: all three
PRs touch only `openspec/changes/**`, `ideation/**` and `README.md`, and none
touches `scripts/merge_master/**`, `.github/workflows/**`,
`hermes/domain/review-councils/**` or `schemas/**`.

**LS executed `seat_resolution.py` and rules the ground WRONG — for the second
consecutive sitting.** This sitting sets no rule, so the predicate's declared
input `rule_touched_paths` **does not exist**; feeding it pull-request paths is
the exact substitution the module's input contract forbids. **The honest ground is
`ConditionUnevaluable`, not `False`**, and the module's own words are *"the caller
refuses the rule or parks the convening"* — with no rule here to refuse.

**LA agrees the outcome was right and offers the repair Brett's 2026-08-29 ruling
left undecided**: the honest ground is ***inapplicable***, not *false*, because
the predicate's input contract is definition-time and no rule is being defined.
**LQ returns NOT MY SEAT. CPL supports the dissent at policy level without ruling
the technical ground.**

**This escalated from a dissent to a PARK — §6.1.**

### 4.3 The S5 seat-model target is NOT in force, and the divergence is disclosed

Brett's R1–R4 of 2026-08-29 name a target composition including `lead-quality` →
`claude-sonnet-5`. **The ruling's own text holds it back**: the enrolled roster
keeps the mutable `opus`/`sonnet` selectors until the Gate-Rules Council's
selection act and the Lead's `lead_accepted_recorded` both land. **Neither has.**
Further, `hermes/domain/agent-mixes.yaml`'s `model_assignments` covers the
**merge-readiness** council only, names no model for `lead-architect`, and the
gate-rules council carries no such block at all.

**This sitting therefore follows the enrolled roster and the 2026-08-29 §7.4
precedent, not an unapplied target** — and records that under the target,
`lead-quality` would have sat at sonnet rather than opus. **What R4 DID fix was
applied**: `company-policy-lead`'s model is read from the tenant declaration in
`hermes/client/role-overrides.yaml`, never from a domain file.

---

## 5. PLACEMENT — a convener act, measured and explained

The 2026-08-29 precedent split its artifacts across two repositories: packet,
seat returns, ballot and council record in codexFactory
`hermes/domain/review-councils/`; only the RATIFICATION record in openxFactory
under the change's own `review/`.

**This sitting could not follow that split** — it holds no write authority over
codexFactory in this act and pushed nothing anywhere. The deviation is declared
rather than glossed:

* **The combined packet, the seat-return appendix and the ballot** live under
  **this** change's `review/`. One sitting produces one packet and one ballot;
  duplicating them across two change directories would create two objects where
  there is one act, and the family's most-repeated defect is two records of one
  decision. **#510 is the physical home because its council had to rule FIRST and
  its threshold ruling could have ended its own round** — the sitting's ordering
  is anchored on it. **That is a reason, not a neutrality claim.**
* **A per-change council review record** lands in each change's `review/`, which
  is exactly what each packet asked for — #510 `tasks.md:2.6` and #513
  `tasks.md:2.3`, both naming `add-binding-consumer-identity`'s pattern.
* **#509 gets NO `review/` directory, on measurement rather than preference.**
  `find ideation -type d -name review` returns **0** at `origin/main`; every
  review record in this estate lives under `openspec/changes/<change>/review/`;
  and no brainstorm vendoring here has ever carried one. **Creating one would
  invent a convention this sitting has no authority to invent.** `lead-architect`
  independently ruled a council **the wrong instrument** for #509 (ballot §7.1).
* **A MIRROR TO codexFactory `hermes/domain/review-councils/` IS OWED**, so the
  council's records stay in one place across sittings. Named here as an obligation
  rather than left to memory.

---

## 6. THE THREE OPERATOR SLOTS — ALL THREE FILLED 2026-08-30. THIS RECORD IS VALID.

| Slot | Act | State |
|---|---|---|
| 1 | `human_step: acknowledgement_of_notice` | **FILLED** — surfaced in the ballot and acknowledged in the ruling. A non-blocking notice the human registers — **never a sign-off** |
| 2 | Liaison disposition | **FILLED by Brett Heap as liaison.** `split_vote` never fired — there was no split — but **LS-C4's park engaged the slot, and it is DISPOSED** by route (ii): the ground is ruled *inapplicable*, and **the three-sitting dissent is discharged**. Disposition §3.2 |
| 3 | `output_disposition: convener_accepts_or_rejects_on_record` | **FILLED** — `disposition-2026-08-30.md`, §8 |

### 6.1 Slot 2 — `lead-security`'s park, recorded in full **(NOW DISPOSED — disposition §3.2)**

LS parks under its charter's standing `security_ambiguity → park_for_liaison`
must-not. **It parks the client-layer exposure verdict the unseated CSC seat would
have carried**, having carried and discharged the DOMAIN-layer reading as the
packet assigned:

> I cannot supply a client-layer voice, and I will not wave one through by
> treating my own reading as covering both. **What would resolve it:** either
> (i) Brett seats the CSC for a supplementary reading limited to LS-F1, LS-F3,
> LS-F7 and LS-F8, or (ii) Brett rules on the record that no client-layer exposure
> voice is required for a §7.4 proposal review that sets no rule — which would
> also discharge the 2026-08-29 dissent that has now stood unresolved through two
> sittings. **Either is a real answer; the present state, where the ground is
> recorded as *false* and the code says *unevaluable*, is not.**

---

## 7. WHAT THIS CONVENING DOES NOT DO

* **It does not ratify.** `Status: draft` stands; `tasks.md` §3's ratification
  gate has not occurred; **LQ records that the text as drafted is not
  ratifiable.**
* **It does not merge, and it pushed nothing to any remote.**
* **It moves no schema byte, cuts no bundle, allocates no minor**, and touches
  nothing under `contracts/`.
* **It defines no candidate class, no envelope entry, no enrollment and no flip.**
  The 2026-08-28 unanimous ruling that proposals are never-convenable through the
  clearance pipeline is UNDISTURBED; **this sitting exists because of it.**
* **It re-opens none of the seven Q-dispositions**, all ruled by Brett Heap on
  2026-08-29. Seats found that a packet MISREADS a ruling; **no seat ruled a
  ruling wrong.**
* **It does not decide #502 or #504**, and neither packet was delayed for them.
* **It does not break any split** — there is none. ~~and it does not dispose LS's
  park~~ **— THE PARK IS NOW DISPOSED**, not by the convening but by Brett as
  liaison on 2026-08-30 (disposition §3.2). Struck rather than deleted because it
  was true of the CONVENING and its closing is the sequence working.

**All of the above remains true OF THE SITTING and is not amended by the ruling.**
The ruling is a separate, later act by Brett; §8 records it.

---

## 8. THE DISPOSITION — Brett Heap, 2026-08-30

**THE SOLE DISPOSITION OF RECORD IS
[`disposition-2026-08-30.md`](disposition-2026-08-30.md)**, in this directory and
carried byte-identically in #513's bundle. **This section is a pointer, not a
restatement**, so that one act cannot drift into two records — the defect the
2026-08-26 round paid for. **Where this record and that file differ, THAT FILE
GOVERNS.**

**The ruling, verbatim:**

> **"accept all fifteen as recommended, 14 folds into the fix rounds."**

**What it means for #510, in one paragraph.** All fifteen ballot §12 decisions are
adopted as the convening recommended them. **T-1 is ruled (c) NOT PREMATURE BUT
NARROWED, so this packet's round did not end** and LA-A5 — the raising-time
re-derivation citing tranche one's ratified `tasks.md:5.3` — is blocking. **All
eleven blocking amendments are accepted**, and **item 13 ELEVATES LS-A10 and
LQ-A13 from should-fix to blocking**, so **#510's fix round carries THIRTEEN**.
Item 11 carries R12 as a named should-fix in LA-A9's shape. Item 12 leaves the
short id standing and **owes the back-citation #513 already made**. One fix round;
**the ratification read comes after, and this ruling ratifies nothing.**

**Read the disposition's §6 before treating any silence as settled.** The
should-fix schedule item by item, the LA/LQ conflict at §3.5, B-8, and every
convening finding at ballot §X except the two ruled by items 14 and 15 are
**UNDISPOSED and stay open** — including **§X.8**, that Codex never re-read this
packet's fix round.

---

## 9. FOR THE NEXT SITTING

* **LA-F1 is the argument for construction over reading, in its strongest form
  yet.** The defect is invisible to `openspec` (it reports `~ 0` modified), to
  both deltas' independent `--strict` runs, to two bot rounds and to three other
  seats. **It appeared only when someone built the artifact the changes would
  actually produce and diffed the result.**
* **LA states the cost, and it bears on T-0(c):** *"I would not have found LA-F1
  had I paced all three equally — it cost a build, two archives and a diff."*
  **The bench is unanimous that combining three subjects degraded every seat's
  reading.**
* **The 2026-08-29 lesson recurred one packet later, by a different route.** There
  Codex was PROVIDER-REFUSED and the packet disclosed it. **Here Codex was simply
  not re-invoked** — it reviewed `bf021888` and never saw the fix round
  `e7f6ae0e` — and neither the packet nor `tasks.md:1.9` discloses that the
  prescriber never re-read the repairs. *"A prescribed fix applied without a
  verifier is an unverified change, whatever its provenance."*
* **LS-A10 names a structural gap larger than its SHOULD-FIX label:** the
  declared-shortfall pattern is load-bearing at **five sites with no floor
  anywhere**, and it is what LS-A1 and LS-A2 both turn on.
* **LQ-C3 names a defect class no checker in this estate reads:** a prose appendix
  asserting facts about ruled dispositions and about what a document "calls"
  something. **Three such claims in #509 survived authoring, a bot round and the
  convening.**
* **The CSC ground has now been disputed at three consecutive sittings** and has
  escalated from a dissent to a park. **LA has offered wording that fixes it at no
  cost.**
