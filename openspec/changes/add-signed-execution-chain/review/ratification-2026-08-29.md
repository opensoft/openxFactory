# Proposal Ratification: add-signed-execution-chain (tranche one)

Status: ratified
Decision date: 2026-08-29
Ratifier: Brett Heap (repository owner) — in-session via question prompts
Ratified: 2026-08-29 by Brett Heap (repository owner) — in-session via question prompts
Ratified baseline: this change as committed in the ratification commit carrying
this record (`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`,
`specs/signed-execution-chain/spec.md` — NINE ADDED requirements over 45
scenarios, no `## MODIFIED Requirements` block anywhere), validated `--strict`
and `--all --strict`.

## Decision

**RATIFY tranche one of the staged topic `signed-execution-chain`** — links 1–3,
plus the signed transparency log, plus the short-chain gate. The capability is
neutral, additive, and authorizes ONE Speckit contract feature plus its gate. It
creates no certificate authority, no attestation identity, no anchor, no chain
and no runtime beyond the validator and the pull-request check named in
`code_surface`.

**This record is not a realization.** `target_release` names `contract-v2.3`,
fresh-counted at the ratification tip, and the number is **allocated at
realization by merge order** per `docs/contract-versioning-policy.md`. The
realization is a later commission and is NOT performed by this ratification.

## Four rulings reached this packet, and they are four acts, not one

They are recorded separately because merging them would misstate what each
authorized. Three preceded ratification and are its input; the fourth is the
ratification.

### 1. The seven clarify questions — ruled 2026-08-29, provenance `#499`

All seven of the staged topic's open questions were ruled by Brett Heap in a
clarify sitting, landed as openxFactory pull request **#499**, squash
**`9c501df6`**. **Q1, Q2, Q4 and Q7 as recommended; Q6 CONFIRMED as
recommended; Q3 and Q5 DIVERGE** and are labelled where they land.

| Q | Ruling | Bearing on this packet |
| --- | --- | --- |
| Q1 wallet presentation | AS RECOMMENDED — shipped grant vocabulary plus a proof-of-possession step, recorded in the ratification record itself, no new artifact | **Encoded as ruled** in requirement 1; the flag was struck |
| Q2 on-chain boundary | AS RECOMMENDED | Tranche three — pre-encoded nowhere here |
| Q3 which chain | **DIVERGES, in two rounds** — Kaspa FIRST as operational witness, Bitcoin-via-OpenTimestamps on EVERY anchored item as durability witness; no selectivity, no third chain | Tranche three — **this delta names no chain, witness, anchor or receipt** |
| Q4 tranche boundaries | AS RECOMMENDED — tranche one is links 1–3 ONLY; the signed transparency log is a TRANCHE-1 artifact; the chain-validating gate exists FROM TRANCHE ONE | **Governs this packet directly.** It already conformed; the scope section now cites the ruling |
| Q5 contract code or an L2 | **OVERRIDES the recommendation** — "allow contract code later"; MUST NOT constitutionalize a never, MUST NOT gate a future adoption on a pre-written trigger | **Complied with positively**: no posture, no never, **no trigger condition** |
| Q6 PHI portions on chain | CONFIRMED — salted keyed commitments; the ruling's OPERATIVE FORM | Tranche three — no commitment format here |
| Q7 attestation signing | AS RECOMMENDED — remote signing served by the harness controller | Tranche two — no attestation link exists here |

**The sitting did NOT green-light the drafting**, and said so in terms: *"the
next act is his."* That distinction is preserved in the staged fragment rather
than smoothed away by the later word.

### 2. The drafting green-light — ruled 2026-08-29, in session

The authorization the sitting withheld. It authorized this packet's EXISTENCE
and no word of its text. The `.openspec.yaml` `approved_by` field was corrected
to name it: as first filed the packet cited the 2026-08-28 session-handoff
board, which is an orchestrating session's record of direction and **not his
word** — an authorization the sitting's own record said was still outstanding.

### 3. The collapse — ruled 2026-08-29, in session

Two sessions raised tranche one into the **same change directory three minutes
apart** — **#494** (08:55:44Z) and **#495** (08:58:21Z) — neither able to see
the other, both authored before the rulings landed. **He ruled #495 the
surviving base; #494 is closed.**

The deciding ground was **Q4**, and it was a ruling rather than a preference.
#494 deliberately shipped **no gate** — *"the packet creates no merge gate"*,
with a requirement scenario normatively against the claim — while Q4 ruled that
the chain-validating gate exists FROM TRANCHE ONE. Conforming #494 would have
meant reversing its thesis, three recorded design decisions and a normative
scenario. #495 already carried the gate, argued from the same convening record,
and kept apart what #494 collapsed: **an out-of-pipeline INCEPTION and a
required-check GATE are different objects**, and only the first is what the
2026-08-28 seats refused. Brett's own §8.2 continuation names the other path as
one that *"needs no class and no flip."*

**Four of #494's hardenings are carried by harvest, cited to it in `design.md`
D8**, so four Codex rounds are provably kept rather than lost with the branch:

| Harvested from #494 | Landed as |
| --- | --- |
| The actor-to-wallet attestation binding, with its DIRECTION taken from the pinned `openxwallet-subject-attestation` (`resolution.resolved_by` closed to `subject_ref`, so a wallet is checked as an attestation and never resolves a subject) | Requirement 2 |
| Per-ratification uniqueness ENFORCED, not merely named — the pinned schema constrains no reuse | Requirement 3 |
| ONE digest construction governing every digest, declared once | Requirement 4 |
| The named-reader required-check rule | Requirement 9 |

One #494 requirement was deliberately **not** harvested: its every-link-signs
rule cannot be performed on any link this tranche defines.

### 4. Narrowing A — ruled 2026-08-29, in session

**Tier 1 is RATIFYING authority.** Agent-held **REVIEW** wallets stay lawful, so
the realized `wal-agent-mrc-0001` is untouched; what a chain refuses is an
agent-held wallet performing the **ratifying** act.

**The clarify sitting did not reach this narrowing** — `#499` touches neither
the tier model nor either narrowing — so it was put to him separately and ruled
separately, and `design.md` D5 records which act is which. The ruling costs
nothing in strictness: `holder_readable` custody evidences that the HOST acted,
which under `add-trust-anchor`'s ratified declared-custody rule is precisely
what a ratification may not stand on. **It removes a false refusal without
creating a real permission.**

**Narrowing B** — Q1's *"rather than a new artifact"* read as *invent no new
artifact* — needed no separate act: Q1's own disposition says no new artifact is
created for the presentation.

## What was corrected before ratification, and by whom

Recorded because this packet's own doctrine is that corrective text earns the
same scrutiny as original text. **Five adversarial rounds ran on #495 after the
rulings landed; eleven findings, all real, all taken** — three Codex P1s among
them, each one a defect in text this session had just written.

| Round | Finding | Class |
| --- | --- | --- |
| 1 | `target_release` carried Markdown emphasis into YAML front matter — the only proposal in the repository not starting with a plain token, and the field IS parsed into the dashboard | Data, not style |
| 1 | D7.1 and D7.2 restated superseded repairs, handing a skimming reader the defect the section records | Corrective text |
| 2 | **P1** — the newly added digest-subject distinction FALSIFIED the gate's own sentence; as written it *"rejects every conforming chain"* | Sweep failure |
| 3 | **P1** — the rewritten gate said it validates EXACTLY five checks and omitted the actor binding just harvested, leaving it inert at the only place that runs | Sweep failure, mirrored |
| 4 | **P1 ×2** — the same closed list still omitted the REVOCATION check and the HOLDER-CLASS check, so a valid signature over a revoked grant, or an honestly self-attesting agent wallet, would pass every enumerated check | Third appearance |
| 5 | **The ratification commit itself** left four sites still asserting "not ratified" — this document's own front matter said ratified while `proposal.md`'s body, `tasks.md`'s boxes, `.openspec.yaml` and `INDEX.md` said otherwise | Fourth appearance |

**Round 5's findings were caused BY the ratification commit** and were repaired
in the same pull request before merge, which is why this record describes them:
a ratification record that omitted the defects its own commit introduced would
be the least trustworthy document in the packet.

**The third appearance was unified rather than patched again**, on this
estate's own rule. The gate now walks **eight** checks and carries a
**requirement-to-enforcement map** stating, for every requirement of this
capability, whether it is walked at the gate or enforced elsewhere — with the
two inception-time refusals named as deliberate omissions rather than left to
look overlooked. The defect class was that a closed list silently converts every
absent requirement into an unenforced one; the map is what closes it, because a
future requirement added without a row is visibly missing.

**The fourth appearance is what made the class legible**, because a state flip
is neither a rule gaining a conjunct nor a closed list, and it failed
identically: *any edit that changes what the packet asserts about itself is a
definition change, and owes a sweep of every site asserting the same thing.* The
method changed with it — a grep-first sweep over the status vocabulary,
re-running the same grep and requiring it empty, which is what found the two
sites no reviewer had named.

Recorded in `design.md` as **D7.6**, **D7.7**, **D7.8** and **D7.9**.

## What this ratification does NOT authorize

- **No realization.** Contract bytes, validator, fixtures and the required-check
  wiring are a later commission, tracked in `tasks.md` §4.
- **No bundle number.** `contract-v2.3` is fresh-counted at this tip and
  re-counted at realization against the manifest at ITS tip.
- **No tranche two and no tranche three.** Both are named successors. Their
  question-gates are open, but what holds them is machinery — the omnigent layer
  and the PKI plane.
- **No envelope and no candidate class.** `specs/025-openxfactory-review-lane-caller/spec.md`
  FR-008 stays gated exactly where the 2026-08-28 convening left it, and
  `add-substantive-review-lane` task 3.2 stays open.
- **No enforcement claim.** Requirement 9 governs this capability's own
  standing: until a named validator runs as a REQUIRED check, every record it
  defines confers and refuses nothing, and the capability says so about itself
  rather than asserting its properties in the present tense.
