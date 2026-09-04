# Proposal Ratification: add-per-change-sweep-ledger

Status: record
Kind: report
Decision date: 2026-09-04
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-04 by Brett Heap (openxFactory operator authority) —
in-session, verbatim: *"ratify 623"*, given after a presentation that offered
ratify-then-land and that carried `design.md` D1 as the reading most worth a
veto. **D1 was not vetoed.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/release-realization/spec.md` (**ONE ADDED requirement**, "A pinned corpus
measurement is carried per subject, never as a shared total") — together with
its realization in `scripts/sequenced_after.py`,
`scripts/validate-sequenced-after.py`, `tests/sequenced_after/test_sweep.py`,
`tests/sequenced_after/corpus-ledger.yaml`, `README.md` and
`docs/sequenced-after-trust-root-floor.md`, with `openspec validate --strict`
and `--all --strict` green (88/88) and the verification run captured beside this
file at `verification-2026-09-04.md`.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-04.md` was
re-derived on the tree this record sits in, after the branch's fourth merge from
`main` — see that file § 7.

## 1. What was ratified, and what it says

The corpus-sweep measurement that discharges `add-sequenced-after-substrate`'s
"Chain-walk policy belongs to the consumer, and its bound SHALL be measured" is
**unchanged**. What changes is how it is PINNED.

`tests/sequenced_after/test_sweep.py` asserted five corpus-wide TOTALS as
literals. A total is a shared mutable that every change-dir pull request writes
to — authoring, adopting, ratifying or archiving a change each move at least one
— so two pull requests that look disjoint collide on the same assertion lines,
git cannot auto-merge them, and the loser owes a merge-from-main, a re-derived
pin, a narrative entry and re-derived record files, one continuous-integration
window per round.

The ADDED requirement replaces the mechanism, not the obligation: **a pinned
corpus measurement is carried as one row per measured subject, and every total a
check asserts is DERIVED from those rows.** Failures name the subject; the
derivation is cross-checked against the measurement by an independent
computation; records cite their own subject's row rather than a total; and a
dated hand-written narrative is kept in exactly one place, appended only where a
move is NOT explained by the row diff.

## 2. THE DEPARTURE FROM ISSUE #618, RATIFIED KNOWINGLY

Issue **#618**'s "Shape of the packet" paragraph specified the opposite of what
was delivered, in as many words: *"`sequenced_after:
[add-sequenced-after-substrate]` (it MODIFIES that change's still-active '…bound
SHALL be measured' requirement, so both are co-modifiers and the declaration is
owed)"*.

**This packet delivers ALL-ADDED.** Both rows read `class: sole`, and the
`sequenced_after:` declaration is ELECTIVE rather than owed. The reading is
`design.md` D1: the requirement's normative sentences bind that a measurement
exists, is recorded, and that the first post-adoption sweep records the deepest
chain — **none of them binds the mechanism by which the recorded measurement is
pinned in a test.** The scalar pin was a realization choice made in that
change's tasks 5.4/5.5 and in `test_sweep.py`'s own prose. A `## MODIFIED`
block would have restated the requirement UNCHANGED, which is what would have
made it dishonest rather than merely redundant.

The departure was recorded in D1 **before** ratification, precisely so that
ratifying the packet would ratify it knowingly rather than by omission, and the
coordinator posted the same reconciliation on #618. It is ratified.

The declaration is made anyway — `sequenced_after: [add-sequenced-after-substrate]`
— on the substrate's own doctrine that *declaring must never be worth less than
omitting*, and because the relation is real. That takes the deepest declared
chain from 1 hop to 2.

## 3. Review before ratification

**An independent adversarial review** verified the mechanics and raised eleven
items; all eleven were taken. It merge-tested two branches adding
adjacent-free change dirs (clean), confirmed every ledger mutation fails naming
id + key + both values, confirmed `corpus_sweep` byte-identical, confirmed the
MOVEMENT LOG retained verbatim, and judged the D1 ALL-ADDED reading **SOUND**
against `spec.md:327-355` and the substrate's tasks 5.4/5.5. It **re-verified at
`d0c50eea`** after the fixes.

**Copilot ran twelve rounds and raised fifteen findings; all fifteen were
taken**, each with a fixture or a corrected claim, and each recorded as this
packet's own defect (thirteen), inherited from `main` (one — `--archive-gate`
resolving `CHANGE_DIR` against the current directory, verified byte-identical on
`origin/main` before the claim was made), or a house-rule breach (two —
host-absolute placeholders, with the constitution's Principle IV read and quoted
rather than taken on the reviewer's word). Rounds 8, 10 and 12 returned zero
findings.

**Codex was ABSENT for all three requests**, each answered with a usage-limit
refusal. That is recorded as ABSENCE and was never counted as clearance: this
packet has had no Codex round at all, and the ratifier was told so.

## 4. Live evidence the ratified mechanism already produced

The branch took **four merges from `main`** while open, and each is a
measurement of the thing the packet argues:

| merge | what landed | rows moved | narrative entry owed |
| --- | --- | --- | --- |
| `19d00872` (#616) | contract-v3.1 cut; `add-project-repo-schema` archived | **1** (`state` flip) | no — the diff says it |
| `c271caa2` (#615) | `update-standards-body-current-publications` archived | **1** (`state` flip) | no — the diff says it |
| `6a39d2ab` (#617) | `amend-owner-layer-severity` ratified and archived | **2** (new row + a PARTNER FLIP) | **yes** |
| `95c2cf6a` (#622) | `add-consumer-identity-namespace` authored | **1** (new row, no flip) | no — the diff says it |

The third is the rule earning its keep: `promote-workflow-gate-contract` flipped
`sole` → `co-modifier` **without anything about that change moving** — archived
2026-07-09 and untouched since — because the newcomer's MODIFIED block shares
"Owner layer constraint" with it. The two rows alone cannot show WHICH key they
share or that this newcomer caused it, so an entry was owed and written. The
other three merges moved rows the diff explains in full and owed nothing.

Under the old pin, every one of those four merges would have moved several
shared totals and required a re-derivation.

## 5. What ratification does NOT settle

- **Archive** is not authorized here. `code_surface` is non-empty and
  `target_release: implemented`, so under `release-realization`'s realization
  archive gate this packet archives on MERGED-PLUS-GREEN, measured after
  landing and never assumed (`tasks.md` Group 7).
- **The two residual serialization points** — the README "OpenSpec Records"
  block and the rare narrative append — remain with the landing window
  (#618 item 1), as `design.md` D9 states.
- **One OPEN inherited defect**, diagnosed during this packet's review and
  deliberately NOT fixed in it: `tests/doc-health/`
  `test_modified_block_currency_self_gate.py` charges to the
  `modified-block-currency` family an info row that only appears in the FIRST
  render of a cold checkout — the same defect shape #614 already fixed once in
  that file ("ONE CLOCK, NOT TWO"), with the object store in place of the clock.
  It is not this packet's and is filed separately.

## 6. Citations

- Issue **#618** — the problem statement, the 2026-09-03 ruling *"do 1 and 3,
  keep the log in one place"*, and the shape paragraph this packet departs from;
  the coordinator's reconciliation comment records the departure there.
- Pull request **#623** — this packet, its twelve review rounds and the
  adversarial review.
- `design.md` **D1** (the ALL-ADDED reading), **D2** (the elective declaration),
  **D8** (records cite rows, and the cited sha is not `seeded_from`), **D9**
  (what is not solved).
