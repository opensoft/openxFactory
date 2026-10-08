# Proposal Ratification: amend-worker-input-budget-dispatch-wording

Status: ratified
Kind: report
Decision date: 2026-10-07
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-10-07 by Brett Heap (openxFactory repository owner) — in
session to lane `openxfactory-1`, verbatim *"ratify 1262 when ready"*,
recorded as a RULED line on the estate's lane register at
**2026-10-07T09:58:32Z** (`opensoft/brett-wip` commit
`f6964352bbd463815c4d2f66a732d40b01d1e83a`, `lanes/log/openxfactory-1.md`).
Ratified baseline: the delta `specs/doc-health/spec.md` at blob
`eead896054ff21de62650014a275815171b8edf4`, the same blob at every commit of
pull request #1264 from its first, `24b7862b`.

## Decision

**RATIFIED AS DRAFTED.** The one `## MODIFIED` requirement in
`specs/doc-health/spec.md`, *Bounded worker input budget*, is ratified with no
amendment. No requirement or scenario text moves in the ratifying commit.

The ratified change to canon is ONE sentence, the last of the requirement's
second paragraph. As promoted on 2026-10-06:

> Where the WORKER assembles the prompt from a dispatchable unit the orchestrator prepared, the orchestrator SHALL measure each unit's assembled size, record it, and SHALL NOT dispatch a unit it has measured over the budget — dispatching one and letting the worker refuse is conformant but useless, because the same unit is selected again next run.

As ratified, `#1262`'s text verbatim:

> Where the WORKER assembles the prompt from a dispatchable unit the orchestrator prepared, the orchestrator SHALL measure each unit's assembled size, record it, and SHALL NOT dispatch a unit it has measured over the budget. The worker's refusal of an over-budget input (scenario "A worker receives an input over the budget") is a backstop that keeps such an input from reaching the model. It does not make an over-budget dispatch conformant, and relying on it wastes the run, because the same unit is selected again next run.

The title, the first and third paragraphs, and all six scenarios are carried
byte-for-byte from canon.

## 1. The word, and the words before it

> ratify 1262 when ready

Brett Heap gave this word on 2026-10-07, in session to lane `openxfactory-1`.
The lane recorded it as a RULED line on the estate's lane register at
2026-10-07T09:58:32Z, object `opensoft/openxFactory#1262` (`opensoft/brett-wip`
commit `f6964352`). The register line states its condition: once the draft is
green and Copilot is clean at its head, the ratification is encoded in the same
pull request. This record is that encoding.

Three earlier words, the same day, led here:

1. *"(a) land as ratified, amend later"*, his ruling on Copilot's comment
   `4202036546` at `#1258`, the archive of `add-worker-input-budget`. RULED at
   2026-10-07T09:42:21Z (`opensoft/brett-wip` commit `98b8b3d4`).
2. *"log the issue to change this"*. The lane filed `#1262`, which states the
   defect, the exact replacement sentence and the acceptance.
3. *"draft the amendment change for 1262"*. The lane drafted this packet as
   pull request #1264.

## 2. What the word does not decide

- **No archive.** `code_surface: none`, so under `release-realization` the
  archive follows landing plus the task list. The archive is still its own
  act, taken on its own word, and this record promotes nothing into
  `openspec/specs/`. Canon keeps the old sentence until that act.
- **No code moves.** The realization (`#1137` → `9da52e31`, with
  `opensoft/xFactory#481` → `b2479b6e`) already never dispatches a unit it has
  measured over the budget (`tasks.md` 1.1). The code comment and the test
  docstring that still echo the old clause stay as registered in `tasks.md`
  § 5.
- **The archived delta is not edited.**
  `openspec/changes/archive/2026-10-06-add-worker-input-budget/specs/doc-health/spec.md`
  is the record of what was ratified on 2026-10-06 and promoted.

## 3. What the ratifying commit changes

None of these changes is requirement or scenario text.

- **`proposal.md`:** `Status: draft` becomes `Status: ratified`, with one
  `Ratified:` citation line beside it.
- **`tasks.md`:** `Status: ratified` with a `Ratified by:` line; boxes 0.1 and
  0.2 are ticked with the word and this record.
- **`.openspec.yaml`:** the approval pair is ADDED to the origin, after the
  drafting pair: `approved_by`, Brett Heap and the word verbatim, and
  `approved_on: 2026-10-07`. Every field the declaration already carried is
  unchanged, so the approval is an addition and not a re-minting. The
  `proposal-origin` family requires the pair the moment the status claims
  approval.
- **`README.md`:** the *Active changes* entry's status, and its closing
  sentence.
- **This record.**

Three files do not move, and each has a reason:

- **`specs/doc-health/spec.md`:** the word ratifies the delta as drafted.
- **`tests/sequenced_after/corpus-ledger.yaml`:** the row records the change's
  state (`active`), class and declaration, and ratification moves none of
  them.
- **`tests/doc-health/test_modified_block_currency_self_gate.py`:** the
  `_LEDGER_SUBJECTS` row names the block, which does not change. It retires at
  the archive.

## 4. What was measured

Every run used full clones of the same kind, each named `openxFactory`,
against `main` `16779816`:

1. **The full set**, at `24b7862b`, the draft. `validate-openspec-cli-pin.py
   --change` for this packet passed, which `main` cannot run because the
   packet does not exist there. Every other gate matched `main` but two, both
   expected: `--ledger-diff` asked for this packet's row, and the four
   `tests/sequenced_after` ledger tests failed for the same reason.
   doc-health reported one more INFO, the carriage-ledger finding this block
   owes, named by the self-gate row.
2. **The gates and doc-health, plus `tests/sequenced_after`, the self-gate
   module and `test_semantic_input_budget.py`**, at `5b3edf14`, with the row
   seeded. Every gate exited 0, `--ledger-diff` read 233 rows, and the three
   test modules passed (337 tests).

Copilot's review `5441182701` at `5b3edf14` recommended approval with one
low-severity finding, a malformed citation in `tasks.md` 1.1, fixed in
`5d236d7d` before this commit. The gates and doc-health run again on the
ratifying tree, and pull request #1264 reports them.

**This pull request lands by SQUASH,** on Brett Heap's word *"yes, land it
when green"*, RULED at 2026-10-07T10:04:03Z (`opensoft/brett-wip` commit
`43e9a5c2`). The squash commit is then the first commit on `main` whose
`proposal.md` declares `Status: ratified`, and it carries the approval pair,
so the archive's origin-retention walk has its baseline in one commit. The
ratifying commit on this branch also carries the pair, so the record holds
either way.
