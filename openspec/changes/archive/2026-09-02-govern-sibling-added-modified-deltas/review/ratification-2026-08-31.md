# Proposal Ratification: govern-sibling-added-modified-deltas

Status: ratified
Decision date: 2026-08-31
Ratifier: Brett Heap (repository owner) — in-session, via an explicit
multi-choice put
Ratified: 2026-08-31 by Brett Heap (repository owner) — in-session via an
explicit multi-choice put, session `openxfactory-f5`; record: this file.
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `tasks.md`, `.openspec.yaml` and the three spec
deltas `specs/release-realization/spec.md`, `specs/document-lifecycle/spec.md`,
`specs/doc-health/spec.md`. **The three deltas are BYTE-UNCHANGED from branch tip
`3d776c67`**, the ninth review round's head and what was put to him; the
ratification commit moves only the sites that assert the packet's own standing.
Gates at the ratification commit, which are the COMMIT'S gates and not
`tasks.md` § 8's archive gate: `openspec validate --strict` valid and
`--all --strict` 81 passed / 0 failed; `pytest tests/doc-health` 1339 passed;
the full suite `pytest tests/ -m "not postgres"` 8343 passed / 21 skipped /
0 failed; doc-health single-repo against the merge-base `9af98c4d`, ZERO new
findings and identical totals (5 critical, 4 error, 38 warning, 12 info).

## Decision

**RATIFY, BY DIRECT RULING OF THE REPOSITORY OWNER.** The requirement set stands
as it is at tip `3d776c67`. All five orchestrator decisions flagged for veto in
`proposal.md` § Orchestrator Decisions are **ACCEPTED AS DRAFTED**. His selection,
verbatim: *"Direct — accept D1–D5 (Recommended)"*.

**Ratification authorizes realization and performs none of it.** `tasks.md` § 2
and § 3 are the two Speckit features and are not built by this act; § 6's marker
sweep, which D4 sequences BEFORE § 2, is a post-ratification act on four ratified
packets and is not performed here.

## The path taken, and the path declined

**The packet prescribed a §7.4 council sitting for itself and did not get one,
because the ratifying authority chose otherwise.** `tasks.md` § 1.1 as authored
said *"Put the packet to a §7.4 council sitting"*, and § 1.2 routed the five open
questions to that sitting. The choice between convening it and ratifying the
converged packet directly was put to Brett Heap in session as an explicit
multi-choice, and he took the direct path. **The sitting was DECLINED by the
ratifying authority's own explicit choice — it was not skipped, not deferred, and
not overtaken by events.** That is recorded plainly here because a packet whose
own task list prescribes a sitting, and which then ratifies without one, owes the
reader the reason on the face of the record rather than a silently ticked box.

**What stood in for the sitting, and what did not.** Nine adversarial machine
review rounds converged the text (below), and that is an adversarial bench, not a
seated council: it found defects, it cast no ballot, and it holds no seat's
authority. The direct path is therefore the OWNER'S act carrying the whole
verdict, with the bench as its input — the estate's ordinary ratification shape,
which `add-notebook-projection-identity` (2026-08-23) and
`add-standing-policy-compliance-contract` (2026-08-26) each took, and which is
distinct from the seated §7.4 path `add-binding-consumer-identity` (2026-08-29)
and `add-chain-anchoring` (2026-08-30) took. What is particular here is not the
direct path but that **this packet had asked for the other one and was answered
by a choice between them**.

**The convergence pre-ruling.** Earlier the same day, before round 9 returned, he
ruled the sequence *"keep going as planned"* — that round 9's verdict decides
whether ratification proceeds clean or carries routed residue. Round 9 came back
CLEAN (Codex on `3d776c67`: *"Didn't find any major issues"*; Copilot: no new
comments), so ratification proceeds with **NO residual routed items**.

## The five decisions, ACCEPTED AS DRAFTED

Accepted as they stand at `3d776c67` — that is, as the nine rounds left them, not
as they were first authored. Each was flagged with the cost of its own veto, and
none of those costs was incurred.

| # | The decision, as drafted and now accepted |
| --- | --- |
| **D1** | **`release-realization` owns the RULE, by EXTENDED ANTECEDENT; `document-lifecycle` owns the DECLARATION.** #502's alternative — state plainly that no rule governs the shape — is refused. The split follows what each capability already owns: ordering between changes, and what a delta must carry. |
| **D2** | **NO `## MODIFIED` block on either currency requirement**, measured rather than preferred, against canon's own *"MUST NOT be reported **as unresolved**"* qualifier. Its second half stands too: **ONE MODIFIED block IS opened**, on a third requirement, superseding the `FAMILY_RESOLUTION` absence rule (`spec.md:2088`) and the bullet resting on it (`:2126`) that `7f656980` (PR #529) falsified without amending any specification. **AND `:1726` IS LEFT STANDING** — answered, not stepped over: it sits under an *"advisory AT LAUNCH"* paragraph that RESERVES its own reversal, `7f656980` is that reserved act, and a launch state whose own requirement provides for leaving it is SPENT rather than contradicted. `:2088` alone is superseded, being an unconditional SHALL with a MUST resting on it. |
| **D3** | **A THIRD RESERVED MARKER FORM** — not a proposal cross-reference (per-change where the fact is per-requirement, and in a document that does not promote) and not a fourth delta-header key. Per-requirement, inside the block making the claim, read by the parser that already exists. |
| **D4** | **The resolution-classification posture as reconciled with #529.** Advisory in the half the packet still owns — both new classes carry `warning` on their own severity constants, and **NO band flip is proposed here**; it follows the discharge of § 6 and is one later ruling. The other half is no longer available: the family joined `FAMILY_RESOLUTION` at `7f656980`, so both classes are `contested` from their first emit, and `add-modified-block-currency-check` § 7.2 is SPENT rather than owed. The forced discharge path is accepted with it, IN ORDER — § 6 sequenced BEFORE § 2 so the class launches at population zero, with the disposition citation as a bounded EXCEPTION (bounded in availability, in grain, and in time) and never a second equal route. |
| **D5** | **THE COLLISION CLASS IS IN SCOPE** — the decision the proposal itself names as most worth vetoing. It reports an active `## ADDED` block, or an active `## RENAMED` block's `TO:` title, for a title canon already carries: the surviving evidence of the unsafe archive order, which nothing in the estate reads today. Population zero on this tree, so it is in place before its first instance — which for a shape whose damage is an archive act that cannot be taken back is the whole argument. |

**The two decisions the proposal predicted a seat would most want re-argued —
D1's capability split and D5 — are accepted unchanged.** Recording that is the
point of having flagged them: the flags were answered, not withdrawn.

## The five open questions — OPEN, and routed where the proposal routes them

**This ruling settles none of OQ-1..OQ-5.** `tasks.md` § 1.2 routed them to a
sitting that did not sit, so the routing they carry is the proposal's own, which
is unchanged by this act.

| OQ | Standing after this ruling |
| --- | --- |
| **OQ-1** — the post-archive detector for the MODIFIED writer's own delta | **OPEN.** `tasks.md` § 7.1: owner unassigned, trigger is the first observed unsafe archive order or a ruling. On this corpus's precedent, a different document pair and therefore a different family. |
| **OQ-2** — whether a `Modified over` marker survives promotion | **OPEN.** The packet KEEPS it, on consistency with the two existing forms; § 7.2 carries the question. Accepting D3 as drafted accepts that default and does not close the question. |
| **OQ-3** — two or more active changes writing one title, by addition or rename | **OPEN**, population zero in both forms by the packet's own disposition rather than by luck (§ 4.3, § 7.3). |
| **OQ-4** — the four standing pairs repaired by their own authors, or by one sweep | **OPEN, and it is the one this ruling most visibly leaves open.** `tasks.md` § 6 stages a sweep with per-packet consent and § 6.1 is explicitly *"Subject to OQ-4's routing"*; a per-owner routing was the alternative a council could have settled in one line. No sitting sat, so § 6 stands as staged and the routing question travels with it. |
| **OQ-5** — the aggregation population across the fourteen submodules carrying `openspec/changes/` | **OPEN.** § 5 makes the measurement a task; a large population elsewhere is a reason to revisit D4's band before the flip, not after. |

## How the ratified text was arrived at — nine rounds, twelve findings, none repeated

**The packet was ADOPTED by this lane on 2026-08-31 after two days orphaned**, on
Brett Heap's word — *"take it, clean it up, resolve our a/b issues too"* — and the
(a)/(b) archive-fork disposition of the live
`add-notebook-hosting-credential-custody` / `add-binding-consumer-identity` pair
was encoded into the packet as part of that adoption (`proposal.md` § The one live
pair this rule already disposes).

**NINE adversarial Codex rounds ran over the tips
`a3dc59ec → 7ba87817 → 2db20313 → 727a14f6 → b926e7f5 → 04c432a3 → 9f25e09d →
3d776c67`. Twelve findings; every one fixed; none repeated.** No finding class
returned after its repair, which is the property worth recording — the
signed-execution-chain arc's four appearances of one class is the counter-example
this arc does not reproduce. **CI was green at every reviewed tip.** Two catch-up
merges of `main` landed across the arc — `355a2efd` (main-side parent `7f656980`,
after the first reviewed tip) and `5287f6c0` (main-side parent `9af98c4d`,
between rounds) — and the packet's population figures were re-read UNCHANGED at
both: 20 active MODIFIED blocks, 16 `canon`, 4 `pending`, zero markers, all four
adding siblings `ratified`.

| # | Finding | Repair landed at |
| --- | --- | --- |
| 1 | **P1 — disposition suppression.** A disposition entry recorded for a pairing finding is consulted BEFORE the block resolves, at family/repo/path grain with no finding-class grain, so it would go on silencing the three comparison arms AFTER the basis archived and the block became comparable for the first time — the exact defect family those arms exist for. Bounded in grain and RETIRED with the basis. | `2db20313` |
| 2 | **P2 — the canon/#529 contradiction the packet was building on.** `7f656980` added the `FAMILY_RESOLUTION` row and amended no specification, so promoted canon still asserted the family's absence while this packet's whole discharge design rested on the row being real. Canon caught up rather than the row being reverted. | `2db20313` |
| 3 | **The unratified basis discloses, or is reported.** The disclosure became a FORM — the word `unratified` in the reason clause — rather than a wish, so it has a reader. | `727a14f6` |
| 4 | **State exclusivity.** Four reported states made MUTUALLY EXCLUSIVE and examined in order, each a predicate over the block's WHOLE marker set, so every block gets EXACTLY ONE and iteration order decides nothing. | `b926e7f5` |
| 5 | **`by`-identifier validation.** The marker's `by` identifier is VALIDATED as the change carrying the block, not merely resolved — so a right basis under an unrelated author is reported instead of promoting as false provenance. | `b926e7f5` |
| 6 | **P1 — the map-extension disposition PROHIBITION.** An earlier draft required a citation for the map-extending act. Measured against the mechanism, it would have fired on no reachable state (`report.uncited_resolutions` keys on `(family, repository, path)`; the unplaced-class finding survives the extension at the same key) and obeying it would itself have been the defect. The block now records the measurement and FORBIDS the disposition, with a falsifying scenario. | `95f8a6d1` |
| 7 | **Own-rename precedence.** One's own rename to the title is the supported rename-and-amend shape promoted canon already resolves against the OLD name one step earlier; the packet leaves that precedence exactly where it found it, and one's own rename is not a collision with oneself. | `04c432a3` |
| 8 | **Rename-basis extension — a rename is a basis everywhere or nowhere.** An ordering rule reaching additions alone would govern the identical hazard in one capability and leave it ungoverned in the next. | `04c432a3` |
| 9 | **Marker multiplicity.** AT MOST ONE pairing marker to a block — one pairing, one declaration; a block resting on two bases rests on neither. The two existing forms keep no such bound because they NAME UNITS and accumulate. | `b39ba549` |
| 10 | **The concurrent-ordering availability bound.** The citation route is refused outright while any OTHER `ratified` change writes a MODIFIED block for the same capability and requirement title, so *"it suppresses nothing"* is true BY CONSTRUCTION rather than asserted. Population zero on this tree. | `b39ba549` |
| 11 | **P1 — the hold keys on the UNPROMOTED TITLE, not on the basis's standing.** Disclosure warns the reader; it does not open the gate. A pairing may be perfectly declared and still be unarchivable. | `9f25e09d` |
| 12 | **Reason-required validation.** The marker's ` — <reason>` tail is REQUIRED and NONEMPTY: a paragraph carrying the prefix alone is a marker whose declaration is DEFECTIVE, not a non-marker, and is reported for the tail it lacks rather than promoting as a complete declaration. | `3d776c67` |

**Round 9 returned clean on `3d776c67`** — Codex *"Didn't find any major issues"*,
Copilot no new comments — which is the condition the pre-ruling made decisive.

## The merge authorization, recorded for provenance and NOT exercised here

Brett Heap's standing word on this packet is **"Merge on clear"**, given before
the convergence closed. It is recorded here because a ratification record is where
the provenance of the acts around it belongs, and because a reader finding the
merge already taken should be able to see what authorized it. **The merge is not
this record's act**, this record does not perform it, and nothing here is
conditioned on it.

## What this ratification does NOT do

- **It settles no open question.** OQ-1..OQ-5 stand exactly as the proposal
  leaves them, including OQ-4's routing of the § 6 sweep. A direct ruling that
  quietly disposed of five questions routed to a sitting that never sat would be
  the worse record.
- **It performs no archive.** `tasks.md` § 8 is unchanged: the archive gate is
  merged-and-green realization evidence, with the doc-health movement matching the
  figure for THE ORDER ACTUALLY TAKEN, and § 8.3's re-read of both of this
  packet's own MODIFIED blocks against canon.
- **It does not close #502.** § 8.2's `Closes #502` remains an archive-time
  option stated as intent. An unratified proposal closing a governance issue was
  the shape § Standing refused; a ratified-but-unarchived one closing it is the
  same shape one step later.
- **It authorizes no code realization beyond what the packet's tasks state.**
  § 2 (F1 — the `Modified over` marker and the pairing class) and § 3 (F2 — the
  ADDED-over-canon collision class) are the two Speckit features, and their scope
  is `proposal.md`'s `code_surface:` and nothing wider. No band flip is
  authorized (§ 7.4), no fourth comparison arm is added, and the 2026-08-27
  ruling against synthesising a basis from a sibling's ADDED text is NOT
  reopened — nothing here compares requirement text.
- **It performs none of § 6.** The four standing pairs are not marked by this
  act. Each marker is an amendment to a ratified proposal, taken with that
  packet's owner consenting, and `add-notebook-hosting-credential-custody`'s
  falsified-scenario amendment (§ 6.6) is obliged by the packet and performed by
  its owner, not here.
- **It convenes nothing retroactively.** No seat sat, no ballot was cast, and no
  part of this record may be cited as a council disposition.
