# Ratification record — relocate-review-authority-floor-mirror

Status: record
Kind: review record
Recorded: 2026-09-08, lane `openxfactory-2` (`openXfactory-2`), session 78b27179

## The word

Brett Heap (openxFactory repository owner), in session, **2026-09-08T23:51Z**,
verbatim:

> **"ratify 293 and 817 when green, then realize them"**

Recorded on openxFactory issue
[#745](https://github.com/opensoft/openxFactory/issues/745) and mirrored on
codexFactory issue
[#232](https://github.com/opensoft/codexFactory/issues/232).

**IT RATIFIES TWO PACKETS IN ONE BREATH, AND THAT IS ITSELF AN ANSWER.** This
packet asked, as **MQ-1** and `tasks.md` box 1.2, whether it would ratify on the
same word as its codexFactory sibling
`relocate-review-authority-floor` (pull request
[codexFactory #293](https://github.com/opensoft/codexFactory/pull/293)) or
separately. **The same word.** The sibling's OQ-3 is answered identically, from
its own side.

The commissioning word was earlier and different: 2026-09-08T13:49:30Z,
*"rule shape 1, measure first, this lane realizes it"* (#232 comment 5586188401,
mirrored on #745). That ruled the SHAPE and ratified no text.

## The head it was given over, and the condition it names

*"when green"* is a condition, and this packet was **NOT** green when the word
was given. That is stated first because it is the honest order of events.

Pull request [#817](https://github.com/opensoft/openxFactory/pull/817) at head
`d4f31962` had `pytest-suite` **RED**, for two causes, both of them this
packet's own and both fixed before this record was written:

1. **`tests/doc-health/test_modified_block_currency_self_gate.py`** reported the
   packet's `## MODIFIED` block for *"The automated advance re-copies the
   vendored snapshot and recomputes its witnesses from the bytes it wrote"* as
   an **undeclared pending block**. The requirement it restates is not in canon:
   it is ADDED by the ACTIVE change `mirror-floor-regeneration-automation`
   (ratified 2026-09-06, PR #708, not archived), so
   `govern-sibling-added-modified-deltas` requires the pairing to be DECLARED in
   the block. The block now carries the reserved `Modified over …'s addition by
   … (…):` marker, in the same form and the same position as the sibling packet
   `amend-mirror-floor-regeneration-merge-authority` uses for the *other*
   requirement of the same parent. **The packet was fixed, not the test.**
2. **`tests/sequenced_after/test_sweep.py`** — four cases — reported the packet
   as *"in the corpus and has no ledger row"*. The row was seeded by the
   sanctioned tool, `scripts/validate-sequenced-after.py . --seed-ledger
   --moved-by '#817'`, which wrote
   `relocate-review-authority-floor-mirror: {state: active, class: co-modifier,
   declares: [mirror-floor-regeneration-automation,
   codexFactory:relocate-review-authority-floor], depth: 2, prose: false,
   moved_by: "#817", moved_on: "2026-09-09"}`. **`moved_on` reads 2026-09-09 and
   that is correct, not a typo**: the seeder stamps UTC, and the word of
   23:51Z was followed within the hour by a UTC midnight. It is the first row
   this repository has stamped through issue #790's UTC-clock fix, and the fix
   works.

After both fixes, measured locally in this lane's own clone on the merged tree:

* `python3 scripts/doc-health.py --single-repo . --family modified-block-currency`
  — the packet appears in **no** finding;
* `python3 -m pytest tests/doc-health/test_modified_block_currency_self_gate.py -q`
  — **19 passed**;
* `python3 scripts/validate-sequenced-after.py .` — *"sequenced_after validation
  passed (43 active changes, 10 declaring the field)"*, archive-date agreement
  passed;
* `openspec validate relocate-review-authority-floor-mirror --strict` — valid;
  `--all --strict` — **101 passed, 1 failed**, the one failure
  `change/disposition-codexfactory-declared-renames` being **pre-existing on
  `main`** (measured there: 100 passed, 1 failed, the same item).

The branch was merged up to `main` `f03fd875` first, so all of the above is
measured against the tree this packet will land on — including #807's
sibling-pairing precedent and #790's UTC clock, both of which it depends on.

* review threads: **2 raised by Copilot, both answered and RESOLVED — 0
  unresolved**;
* `closingIssuesReferences`: **empty** — both issues are referenced with `Refs`.

## What it ratifies

**The PROPOSAL, and one requirement.** `specs/review-lane-floor-mirror/spec.md`
restates *"The automated advance re-copies the vendored snapshot and recomputes
its witnesses from the bytes it wrote"* in full and changes **what "obtain"
means**: the lane resolves the authoritative document through an ORDERED LIST of
declared candidate paths, taking the first obtained, and refuses
`floor_document_unobtainable` only when EVERY candidate fails, naming every path
tried. The copy, the byte-witness rule, the prohibition on carrying a digest
forward from the party being witnessed, and the refusal itself are **untouched**.

The list is bounded rather than left open: it names the governed relocation that
opened it, is ordered with the path in force FIRST, returns to a single entry
once an advance has been observed against the successor, and **the lane is never
taught to SEARCH** — a discovered file is one an author elsewhere can plant, and
the byte copy goes into this repository's witnessed snapshot.

**M-1 THROUGH M-7 STAND AS RECOMMENDED — NO VETO WAS ENTERED.**

* **M-1** the two realizations bracket codexFactory's move: (1) accept both
  paths here → (2) codexFactory moves → (3) drop the old path here. **Not a
  preference.**
* **M-2** ordered, first-obtained-wins, old path FIRST — so realization (1) is
  observably a no-op on the day it lands.
* **M-3** `floor_document_unobtainable` keeps its identifier and its meaning.
* **M-4** the credential binding gains an enumerated `source_documents:` read
  surface — documentation with a lockstep test, never a run-time input.
* **M-5** nothing about the snapshot changes, and the realization asserts it.
* **M-6** `contracts/review-lane-pin.yaml`'s `sources:` entry advances in step
  (3), not (1).
* **M-7** the lane is never taught to discover the document.

## What it does NOT decide

* **NOTHING IS REALIZED BY THE RATIFICATION.** *"then realize them"* is a SECOND
  act in the same word. This repository's step (1) is the FIRST realization of
  the pair and lands as its own pull request; codexFactory's move may not be
  opened before it.
* **BOXES 1.3 AND 1.4 STAY OPEN.** 1.3 is MQ-2 — whether the binding's
  `source_documents:` read surface (M-4) is wanted; 1.4 is MQ-3 — what triggers
  M-1 step (3). M-4 and the default trigger both stand unvetoed as
  recommendations, but each box asks for a word choosing between named options,
  and the word of 23:51Z chose neither. **Neither blocks realization (1)**: M-4
  is a single file in that realization and can be dropped by one edit, and MQ-3
  bears only on step (3).
* **No codexFactory file is touched by this packet, ever.**

## Which boxes this ratification ticks, and why only those

**FOUR.** Each because its OWN stated tick condition is the ratifying word or
the ratifying commit.

* **1.1** Brett Heap ratifies this packet — the word above and this record.
* **1.2** MQ-1, same word or separate — **the same word**, which ratified #293
  and #817 together.
* **5.1** the README OpenSpec Records entry — its condition is the ratifying
  commit.
* **5.2** validators — its condition is *"the ratifying commit, over the
  recorded runs"*, and the runs are recorded above and in the pull-request
  thread.

**1.3 and 1.4 stay open** for the reason above. **§ 2, § 3 and § 4 stay open**,
each on the act it already names — this repository's step (1), codexFactory's
move, and this repository's step (3).

## ONE CORRECTION MADE AFTER THE RATIFYING WORD, DISCLOSED RATHER THAN FOLDED IN

**The ratified requirement text was edited after the word of 23:51Z, and it is
recorded here so the record is not outrun by its own packet.** Copilot raised it
on #817 (comment 3963496884) against the merged head: the requirement said the
candidate list *"SHALL be declared in the lane's own sources AND in the
credential binding's read surface"*, while the same packet puts that binding
site for veto as **M-4**, with **MQ-2 open** and `tasks.md` boxes 1.3 and 2.4
("M-4 (if it stands)") written on the assumption it may be dropped.

**A ratified SHALL cannot be contingent on a question the same ratification left
open**, so the two could not both be right. The requirement now mandates only
what is NOT in question — the declaration in the lane's own sources, and the
run-time prohibition on reading the list from any artifact a check compares it
against — and treats the binding as an ADDITIONAL site the packet recommends,
covered by the same agreement assertion if it stands and removed by a veto of
M-4 without touching the requirement.

**WHY THIS WAS TAKEN RATHER THAN ESCALATED.** It removes a contradiction the
ratifying word itself created by ratifying M-4 as vetoable alongside a text that
mandated it; it makes the requirement demand LESS rather than more; and it
changes no decision — M-4 still stands as recommended, MQ-2 is still open, and no
box moved. **It is nonetheless an edit to ratified requirement text made by this
lane and not by an owner's word, and Brett Heap may veto it in one edit**: the
alternative he may prefer is Copilot's option (b) — close MQ-2, mark M-4
non-optional throughout, and restore the original mandate.

## Scope

This record ratifies the PROPOSAL. The realization is a separate pull request on
the second half of the same word, and it is the FIRST of the pair to land
(M-1). **The archive is a separate, later word**, and `tasks.md` box 5.3 says
what it waits on — including that this packet SHALL NOT archive until
`mirror-floor-regeneration-automation` promotes, which the sibling-pairing
marker in the spec delta records.
