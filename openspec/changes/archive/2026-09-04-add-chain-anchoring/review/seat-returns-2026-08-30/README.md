# Seat returns — combined §7.4 council review sitting, 2026-08-30

Status: record (evidence appendix)
Convening: council review of openxFactory pull requests **#510**
  (`add-chain-attestation`, tranche two), **#513** (`add-chain-anchoring`,
  tranche three) and **#509** (`vendor-medxchain-brainstorm`) — commissioned
  OUTSIDE the clearance pipeline BY DESIGN (proposals are never-convenable
  through it, unanimously, 2026-08-28), on the §7.4
  council-reviewed-but-human-approved path.
Packet: `openspec/changes/add-chain-attestation/review/convening-packet-2026-08-30.md`
Ballot: `openspec/changes/add-chain-attestation/review/ballot-2026-08-30.md`
Judged at:

```
openxFactory origin/main       afe29561a317853eb22f1e6b248f7029fa2fb2a7
shared merge-base (all three)  b710976b4a4fef277cdd292a407942369e9b9efa
PR #510 head                   e7f6ae0e400719894fbaa0d14be274ba86b2e3b3
PR #513 head                   cf5a24b89870a87663c595550210ee4deb0ac28e
PR #509 head                   26c7e778682089789795befad4c28af509ff2706
codexFactory (read-only)       3c71ddc910b8e0b119d0e1ee40a5523dfa294f07
```

Mode: **agent-seat deliberation** — one independent agent per seat, each loaded
with only the convening packet, its own persona and seat declaration, and the
council contract. **No seat saw another seat's return. No seat saw the
convener's opinions beyond the packet. No seat wrote to any checkout.** Matches
the 2026-08-22, 2026-08-26, 2026-08-28 and 2026-08-29 precedents, including the
requirement that findings be reached **BY EXECUTION** rather than by reading
prose.

Files here are the seats' returns **VERBATIM**, preserved as evidence.
**The records condense; this appendix does not. Where a summary in a record and a
return here diverge, THE RETURN GOVERNS.**

**Nothing in these files has been edited**, including where a return cites the
convening's local checkout path rather than a repository-relative one. Verbatim
is the stronger discipline and it wins over tidiness. The five read-only
checkouts the returns name resolve as follows:

```
invmain     openxFactory origin/main @ afe29561    inv510  PR #510 head @ e7f6ae0e
inv513      PR #513 head @ cf5a24b8                inv509  PR #509 head @ 26c7e778
sittingref  codexFactory @ 3c71ddc9
```

| Seat | Layer | Model | File | #509 | #510 | #513 |
| --- | --- | --- | --- | --- | --- | --- |
| lead-architect (LA) | domain | `opus` | `lead-architect.md` | ACCEPT AS AMENDED | **ACCEPT AS AMENDED** | **ACCEPT** |
| lead-security (LS) | domain | `opus` | `lead-security.md` | **ACCEPT** *(disclosure limb only, LS-C2)* | **ACCEPT AS AMENDED** | ACCEPT AS AMENDED |
| lead-quality (LQ) | domain | `opus` | `lead-quality.md` | ACCEPT AS AMENDED | **ACCEPT AS AMENDED** *(text as drafted **not ratifiable**)* | ACCEPT AS AMENDED |
| company-policy-lead (CPL) | client | `sonnet` | `company-policy-lead.md` | ACCEPT AS AMENDED | ACCEPT AS AMENDED *(charter limb)* | ACCEPT AS AMENDED *(charter limb)* |
| ~~client-security-compliance-officer~~ | client | — | — | **NOT SEATED — and LS PARKS the question (LS-C4)** | | |
| ~~intent-owner role slot~~ | project | — | — | vacant-symbolic, `binding: symbolic_until_project_roster` | | |

**FINAL TALLY: NO REFUSALS ON ANY SUBJECT. #510 IS UNANIMOUS 4/4 ACCEPT AS
AMENDED.** `split_vote: park_for_liaison` is **NOT engaged on any verdict** — the
first §7.4 sitting since the procedure was defined at which it is not.
`missing_required_seat: refused` is **satisfied**. **Slot 2 is nonetheless engaged
by LS-C4's seat-level park.**

**Sixteen blocking amendments**: eleven on #510 (LA-A1/A2/A3/A5 · LS-A1/A2/A3 ·
LQ-A1/A2/A3/A4), three on #513 (LS-A5/A6 · LQ-A5's #513 limb), three on #509
(LQ-A5's #509 limb · LQ-A6 · LQ-A7). **CPL holds none and says so.**

## The threshold, ruled first

**#510 IS NOT PREMATURE and its round did NOT end.** Three seats reach T-1; CPL
returns NOT MY SEAT and names `lead-architect`. LA rules **(c) NOT PREMATURE BUT
NARROWED**; LS and LQ each rule **(a) NOT PREMATURE** on their own limb, each with
a caveat that became a blocking amendment. **T-2 is unanimous among the three
seats reaching it: a ruling on #510 does not bind #513.**

## The decisive finding — reached by construction, by one seat

**LA built the canon these two changes would actually promote** — copied
`invmain/openspec`, dropped #510 beside tranche one, ran `openspec archive`
twice — and found **18 requirements / 104 scenarios, mechanically clean, holding
two contradictory scenarios on one antecedent**: promoted canon `:552` validates
a chain carrying no attestation link and does not report the absence as a break;
promoted canon `:1141` **REFUSES** the same chain. `openspec` reports `~ 0`
modified, because each delta is independently valid.

**A second defect fell out of the same construction**: tranche one's *"THE LIST IS
CLOSED … every requirement of **this capability**"* is scoped to the capability,
not the tranche, and its table carries **9 rows against 18 promoted
requirements**. #510 never touches that clause.

**And a third**: #510 **MINTS** an evidence class whose member `hardware_attested`
is precisely the `excluded_models: asserted_hardware_backing` entry that the
ratified `contracts/trust-anchor/trust-anchor-chain-custody.registry.yaml` rules
out — the one vocabulary the staged topic names as the family's **first** risk.
LA resolved all six cited authorities: five are genuinely consumed.

## Findings reached independently by more than one seat

* **The three closed Codex P1 fixes do not all hold as applied.** LS: P1-1
  *"repairs the record, not the control"*; P1-3 binds closure to an instrument
  whose own ratified header says it cannot serve the requirement. LQ: P1-2
  *"moved the attack rather than closing it."* **LA disagrees on P1-2** — *"the
  sitting's best engineering … I could not break it."* **The conflict is preserved,
  not reconciled.**
* **#509's mapping appendix carries checkable falsehoods.** LA checked 16 rows
  (13 true, 3 false); LQ checked 17 targets (15 verify); CPL found four. **All
  three independently found the same core three**: Q6's disposition label
  transplanted onto Q2, two phrases attributed to the staged topic that return
  **zero hits repo-wide**, and *"eighteen months"* where the interval is 657 days.
  **CPL additionally traced the date error into #513's own requirement text at
  `spec.md:658`.**
* **The convening's two carried facts were re-verified, not adopted.** All three
  domain seats measured tranche one's gate scenarios independently and all three
  returned **nine**; all three reproduced the zero-hit grep for *"when each is
  raised"*.

## Unique execution-proven findings

* **LS-F3** — subtraction on #510's tier-2 key rule: every enumerated condition
  genuinely refuses when the others are removed, *"the depth is real"* — but
  `grep -E "co-locat|isolat|trust boundary|same host"` returns **zero** across all
  seven files. *"In every configuration"* enumerates hand-overs, never
  **reachability**; a controller co-resident with a self-hosted runner is
  conformant as drafted.
* **LS-F7** — `455bbdaa` genuinely fixed the collision it names, and the
  asymmetry with requirement 6 is deliberate and correct; but the fix makes the
  receipt stateless, so *"a one-entry receipt handed to an independent verifier …
  is byte-indistinguishable from a one-witness configuration."*
* **LS-F8** — `grep -E "entropy|random|unguessable"` returns **zero**, and the KEY
  of the keyed commitment has no custody rule where the salt has two. **Q6's
  erasure property rests on two parameters the contract never fixes.**
* **LQ-F9 / LQ-F10** — two scenarios giving **opposite consequents on one
  antecedent** in #510's requirement 2; and a deferred-leaf path that passes the
  gate with an EQUAL enumeration.
* **LQ-F22** — D6, routed to this council at `tasks.md:2.5`, has **zero scenarios
  and no SHALL**. There is nothing to rule on.
* **LA-F6** — archiving #510 first yields a nine-requirement canon holding only
  tranche two. **Both orders succeed silently.**

## Recorded in the packets' and the changes' FAVOUR

Every seat filed a favour section unprompted; a record that lists only defects
misreports what the bench read.

* **LQ found NOTHING BLOCKING on the claim-outrunning-the-machinery family** —
  the estate's most-recorded defect. The one ASSERTED live claim survives a **live
  ruleset read**: ruleset `21538893`, enforcement active, `~DEFAULT_BRANCH`,
  `required_status_checks: wallet-validation, pytest-suite`. Everything else is
  DECLARED with a cite.
* **Both packets' headline counts are right** — 9/59 and 9/52, consistent at four
  sites each; **SHALL on the first body line of all eighteen requirements**; ≥1
  scenario each; no MODIFIED/REMOVED block anywhere; `--strict` green on both and
  `--all --strict` **79 passed** in each branch against 78 at main;
  **doc-health zero-new on all three** with matched basenames per issue #342.
* **#510's constitutional citation verifies byte-exact against the schema** (LS
  walked it): six booleans, `additionalProperties: false`, `execute_final_action`
  and `access_secrets` both `const: false`, exactly five archetypes.
* **#513 mints no vocabulary** (LA), **edits nothing in the staged topic
  directory, study included** (LQ, empty diff — the standing
  do-not-edit-the-study rule respected), complies with Q5 positively, and has
  **zero assertions-dressed-as-scenarios** where #510 has three.
* **The authorization discipline is exemplary** (CPL swept all 28 "Brett"
  citations): *"No sentence reads as though Brett agreed to either packet's
  drafted content."* Both `.openspec.yaml` files decline to claim an approver they
  cannot cite, and #513 names the exact prior overreach it is not repeating.
* **#509 on LS's limb: ACCEPT** — no credential, secret, key, PHI or identifier
  disclosed, and the unsafe 2024 architecture is corrected in its own appendix so
  it cannot be read as endorsed. **CPL:** its dated section boundary is *"a clean,
  reusable pattern for future vendorings."*
* **All four seats confirmed all five checkouts UNMODIFIED** — `git status
  --porcelain` empty before and after their work.

## What the seats said about the sitting itself

**T-0(c) is unanimous against the convening: combining three subjects cost every
seat.** LA: *"I would not have found LA-F1 had I paced all three equally."* LS:
*"I did not drive #510's requirements 6–9 by subtraction as I drove requirement
4."* LQ: *"It did compress the judgement half."* CPL: *"Yes, measurably, and I
disclose it against my own return."*

**LQ also caught the convening in two unmeasured figures** (LQ-F2, LQ-A15) —
*"It found one and made two."* The packet is deliberately **not** edited to fix
them, because it is the evidence of what the seats read; the correction is in the
ballot at §Y.3.
