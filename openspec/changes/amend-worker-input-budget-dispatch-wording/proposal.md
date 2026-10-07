---
code_surface: none — MEASURED on `main` `16779816`, not assumed. The delta rewords ONE sentence of one promoted requirement, and the realization ALREADY BEHAVES THE WAY THE AMENDED TEXT READS — it never dispatches a unit it has measured over the budget (`tasks.md` 1.1 cites the gate, the dispatch list the worker reads, and the test, each by file and line). THIS PACKET'S WHOLE DIFF IS CORPUS TEXT AND BOOKKEEPING: its own five files (`.openspec.yaml`, `proposal.md`, `tasks.md`, `review/ratification-2026-10-07.md`, the ratification record, and `specs/doc-health/spec.md`, the one `## MODIFIED` delta), one README *Active changes* bullet, the machine-seeded per-change row in `tests/sequenced_after/corpus-ledger.yaml` that every filing owes, and the one `_LEDGER_SUBJECTS` row `tests/doc-health/test_modified_block_currency_self_gate.py` requires for every packet its carriage ledger names (a data row; no check changes). NOT ONE CHARACTER OF RUNTIME CODE MOVES — no validator, no script under `scripts/`, no test logic, no contract, no workflow. Two non-normative echoes of the old clause sit in code, a comment at `scripts/doc_health/catalog_dispatch.py`:527-528 and a test docstring at `tests/doc-health/test_semantic_input_budget.py`:506-508; they are registered in `tasks.md` § 5 and left, because editing them would give a wording packet a code surface. Under `release-realization` an empty code surface archives ON LANDING plus this task list, rather than on merged-plus-green realization evidence; the archive is its own act, taken on its own word.
target_release: implemented — the value `release-realization` names for a doc-only change. No contract bundle is cut, nothing under `contracts/` is edited, no `contracts/manifest.yaml` row moves and no consumer's pin has to advance to receive this. The realization of a wording amendment IS its promotion at archive.
sequenced_after: [add-worker-input-budget]
---

# Proposal: amend-worker-input-budget-dispatch-wording

Status: ratified
Ratified: 2026-10-07 by Brett Heap (openxFactory repository owner) — in session to lane `openxfactory-1`, verbatim *"ratify 1262 when ready"*; RULED on the estate's lane register at 2026-10-07T09:58:32Z (`opensoft/brett-wip` commit `f6964352bbd463815c4d2f66a732d40b01d1e83a`, `lanes/log/openxfactory-1.md`). RATIFIED AS DRAFTED, with no amendment: the MODIFIED requirement *Bounded worker input budget*, whose one reworded sentence is #1262's text verbatim, in the delta blob `eead8960` unmoved since this packet's first commit. The word archives nothing; record at review/ratification-2026-10-07.md
Kind: proposal
Proposed: 2026-10-07, in lane `openxfactory-1`, on Brett Heap's word, verbatim
in session that day: *"draft the amendment change for 1262"*.
Origin: Copilot review comment
[`4202036546`](https://github.com/opensoft/openxFactory/pull/1258#discussion_r4202036546)
on `opensoft/openxFactory`
[#1258](https://github.com/opensoft/openxFactory/pull/1258), the archive of
`add-worker-input-budget`, merged `16779816`; encoded as
[#1262](https://github.com/opensoft/openxFactory/issues/1262).
Governing issue: `opensoft/openxFactory#1262` (Refs #1262).

**NOTHING HERE WAS RATIFIED BY THE AUTHORING LANE.** The packet rewords
requirement text Brett Heap ratified on 2026-10-06, and requirement text is
amended on his word, not folded in as an addendum. The lane drafted this
packet as the instrument for that word, and he gave it on 2026-10-07,
verbatim *"ratify 1262 when ready"*, as the `Ratified:` line above records.
Landing it and archiving it each take their own word.

## Why

The promoted requirement **"Bounded worker input budget"**
(`openspec/specs/doc-health/spec.md`, lines 4083-4087 on `main` `16779816`)
contradicts itself inside one sentence of its second paragraph. The sentence
first says the orchestrator *"SHALL NOT dispatch a unit it has measured over the
budget"*, then says that *"dispatching one and letting the worker refuse is
conformant but useless"*. The SHALL NOT makes an over-budget dispatch
non-conformant. The clause after the dash calls the same dispatch conformant. An
orchestrator reading the paragraph is given two incompatible rules.

Copilot found it on the archive pull request, at
`openspec/specs/doc-health/spec.md:4087`, verbatim: *"The promoted requirement
contradicts itself: `SHALL NOT dispatch` (and the scenario at lines 4105–4108)
makes an over-budget dispatch non-conformant, but this sentence calls that same
dispatch “conformant.” This leaves orchestrators with two incompatible rules."*

Brett Heap ruled on that thread, verbatim in session 2026-10-07: *"(a) land as
ratified, amend later"*. The ruling is recorded as a RULED line on the estate's
lane register at 2026-10-07T09:42:21Z (`opensoft/brett-wip` commit `98b8b3d4`,
`lanes/log/openxfactory-1.md`). `#1258` landed with the text exactly as
ratified. On his next words, *"log the issue to change this"*, the lane filed
`#1262`, which states the defect, the exact replacement sentence and the
acceptance. This packet is that change.

**The scenarios were never wrong.** Two of the requirement's six scenarios
already say what the amended sentence says, and neither moves:

- *"A dispatchable unit measures over the budget"* (canon line 4105): the unit
  MUST NOT be dispatched.
- *"A worker receives an input over the budget"* (canon line 4110): the worker
  refuses before invoking the model. That is the backstop.

Only the rationale clause is defective, so only the rationale clause changes.

## What Changes

- **MODIFIED** `doc-health` requirement **"Bounded worker input budget"**: ONE
  sentence of the SECOND paragraph is replaced. The first and third paragraphs
  and all six scenarios are carried byte-for-byte. The requirement's title does
  not change.

The sentence as promoted (canon, `main` `16779816`, lines 4083-4087), exactly:

> Where the WORKER assembles the prompt from a dispatchable unit the orchestrator prepared, the orchestrator SHALL measure each unit's assembled size, record it, and SHALL NOT dispatch a unit it has measured over the budget — dispatching one and letting the worker refuse is conformant but useless, because the same unit is selected again next run.

The sentence as amended (`#1262`'s text, verbatim), exactly:

> Where the WORKER assembles the prompt from a dispatchable unit the orchestrator prepared, the orchestrator SHALL measure each unit's assembled size, record it, and SHALL NOT dispatch a unit it has measured over the budget. The worker's refusal of an over-budget input (scenario "A worker receives an input over the budget") is a backstop that keeps such an input from reaching the model. It does not make an over-budget dispatch conformant, and relying on it wastes the run, because the same unit is selected again next run.

The obligation does not move. The SHALL NOT was already the rule and both
scenarios already enforced it. The amendment removes the clause that
contradicted it, and states what the worker's refusal is for: a backstop that
keeps an over-budget input from the model, not a licence to dispatch one.

The delta block is canon's block with only that sentence's tail re-wrapped:
every line of the requirement up to *"each unit's assembled size, record it, and
SHALL NOT dispatch a unit it has"* is identical, and so is every line from the
paragraph's end to the block's last scenario. `tasks.md` 2.1 records the diff.

## Impact

- Affected spec: `doc-health` (promoted, `openspec/specs/doc-health/spec.md`),
  one requirement, one sentence. No other requirement in the spec is touched.
- Affected code: none. Measured, not assumed: the realization
  (`opensoft/openxFactory#1137`, merged `9da52e31`) does not dispatch a unit it
  has measured over the budget, so the amended sentence describes behaviour that
  already holds (`tasks.md` 1.1).
- Affected gates: canon doc-health only. The carriage ledger of the
  `modified-block-currency` family reads a `## MODIFIED` block that rewords a
  promoted body unit as an uncarried unit. That is expected for an amendment,
  and the self-gate's subject list names this packet for as long as it is
  active (`tasks.md` 3.3).
- Not edited: the archived delta at
  `openspec/changes/archive/2026-10-06-add-worker-input-budget/specs/doc-health/spec.md`
  (line 48). It is the historical record of what was ratified and promoted, and
  an archive is never rewritten. Copilot's comment also suggested amending the
  archived delta; `#1262` declines that part, and so does this packet.
- After the archive, canon carries no sentence that calls an over-budget
  dispatch conformant, and the six scenarios are unchanged (`#1262`
  acceptance 3).
