# Tasks: amend-worker-input-budget-dispatch-wording

Status: ratified
Ratified by: amend-worker-input-budget-dispatch-wording — 2026-10-07, Brett Heap, "ratify 1262 when ready", RULED 2026-10-07T09:58:32Z (record `review/ratification-2026-10-07.md`)
Kind: tasks

## 0. Ratification

- [x] 0.1 Brett Heap's word ratifying the amended sentence, which is
  `#1262`'s replacement text verbatim. A different normative wording is his
  choice to make, not the authoring lane's. **RATIFIED AS DRAFTED
  2026-10-07** — Brett Heap's word in session to lane `openxfactory-1`,
  verbatim *"ratify 1262 when ready"*; RULED on the estate's lane register
  at 2026-10-07T09:58:32Z (`opensoft/brett-wip` commit `f6964352`,
  `lanes/log/openxfactory-1.md`). The delta stands without amendment, in
  blob `eead8960`. The word archives nothing. Record:
  `review/ratification-2026-10-07.md`.
- [x] 0.2 On the word: `Status: ratified` plus a `Ratified:` line in
  `proposal.md`; the `approved_by`/`approved_on` pair in `.openspec.yaml`
  (the `proposal-origin` family reports an ERROR the moment the status claims
  approval without it, `scripts/doc_health/proposal_origin.py`:352-363); a
  record under `review/`; and the README *Active changes* entry moved with it.
  Done in one commit with the word, so the ratifying commit carries the
  approval pair: `Status: ratified` and `Ratified:` in `proposal.md`,
  `Status: ratified` and `Ratified by:` here, the pair in `.openspec.yaml`,
  `review/ratification-2026-10-07.md`, and the README entry.

## 1. Verification before ratifying (`#1262` acceptance 1)

- [x] 1.1 The realization never dispatches a unit it has measured over the
  budget. **CONFIRMED, read-only, 2026-10-07.** If it did, that would be a
  code defect for its own issue and not part of this wording change; it does
  not.
  - `opensoft/openxFactory#1137`, merged `9da52e31`, in
    `scripts/doc_health/catalog_dispatch.py`:
    - `catalog_dispatch.py:513-515` measures each shard's assembled analysis
      input in bytes (`shard_analysis_input(...)`, the child's own assembly
      reproduced so the parent can measure it);
    - `catalog_dispatch.py:516-517` appends the shard to the dispatch list
      ONLY when that measure is `<= input_budget_bytes`;
    - `catalog_dispatch.py:518-526` is the comment *"A SHARD MEASURED OVER
      THE BUDGET IS NEVER DISPATCHED"*;
    - `catalog_dispatch.py:527-528` writes `shards.json` from that list and
      nothing else;
    - `catalog_dispatch.py:535-543` records the shards over the budget in
      `meta.json` as `shards_over_budget`.
  - The same file on `main` `16779816` is unchanged in substance: the gate is
    at `catalog_dispatch.py:521-522` and the `shards.json` write at
    `catalog_dispatch.py:532-533`.
  - The worker reads only that list. `opensoft/xFactory`
    `.github/workflows/doc-health-cataloger-worker.yml`:171-175 takes `ids[0]`
    of `shards.json` and exits 0 with *"no shards selected this run; nothing
    to classify"* when the list is empty. The file is identical at `b2479b6e`
    (the merge of `opensoft/xFactory#481`, the paired realization) and at
    `main` as read on 2026-10-07.
  - The tests: `tests/doc-health/test_semantic_input_budget.py`:503
    `test_a_shard_measured_over_the_budget_is_never_dispatched` builds two
    shards, one over a 20,000-byte budget, and asserts that exactly one is
    dispatched and that it is not in `shards_over_budget`; :559
    `test_the_bundle_reports_what_will_be_dispatched_not_what_was_sharded`.
    The line numbers are the same at `9da52e31` and on `main`.
  - The other assembly shape, where the orchestrator assembles the prompt,
    packs and defers rather than dispatching units: :205
    `test_a_scaffold_larger_than_the_budget_refuses_rather_than_overshoots`.

## 2. The delta

- [x] 2.1 `specs/doc-health/spec.md`: ONE `## MODIFIED` requirement,
  *Bounded worker input budget*, copied from canon (`main` `16779816`,
  `openspec/specs/doc-health/spec.md`:4070 to the end of the file, 52 lines,
  3,596 bytes) with only the second paragraph's last sentence replaced by
  `#1262`'s text. Measured: the title and first paragraph are identical; the
  second paragraph is identical through *"SHALL NOT dispatch a unit it has /
  measured over the budget"*; the third paragraph and all six scenarios (16
  bullets) are identical. `diff` of canon's block against the delta's block
  reports one hunk, `17,18c17,21`: canon's two lines ending *"... letting the
  worker refuse is / conformant but useless, because the same unit is selected
  again next run."* become five lines carrying the new text. The block is 55
  lines and 3,772 bytes.
- [x] 2.2 The replacement is `#1262`'s text verbatim. Measured with
  whitespace normalized: the new sentence is in the block and the old one is
  not, and *"conformant but useless"* appears nowhere in it.
- [x] 2.3 Nothing else is edited. No other requirement of `doc-health` is
  reached, and the archived delta at
  `openspec/changes/archive/2026-10-06-add-worker-input-budget/specs/doc-health/spec.md`
  (line 48) is not touched: it is the historical record.

## 3. Gate

- [x] 3.1 `python3 scripts/validate-openspec-cli-pin.py --all --strict`, and
  `--change amend-worker-input-budget-dispatch-wording` (`#1262`
  acceptance 2).
- [x] 3.2 `python3 scripts/proposal-support.py . verify
  amend-worker-input-budget-dispatch-wording`, `validate-code-surface.py`,
  `validate-target-release.py`, `validate-scope-globs.py`, and
  `validate-sequenced-after.py`, plain and `--ledger-diff`.
- [x] 3.3 doc-health, run from the tree it measures. The
  `modified-block-currency` family reports this block ONCE, at INFO: it does
  not carry 1 of the 25 body units and scenario bullets canon states, and that
  unit is the amended sentence. The family cannot tell a deliberate rewording
  from drift and does not claim to. The finding is named by a row in
  `tests/doc-health/test_modified_block_currency_self_gate.py`
  `_LEDGER_SUBJECTS`, which retires when this packet archives. A
  `**Removed from canon by**` marker was NOT used, because the marker is
  promoted with the block and would carry the removed sentence into canon,
  which `#1262` acceptance 3 forbids.
- [x] 3.4 The sweep-ledger row in `tests/sequenced_after/corpus-ledger.yaml`,
  seeded by the sanctioned seeder with `--moved-by '#1264'`: `active`,
  `co-modifier`, `declares [add-worker-input-budget]`, `depth: 1`. One row
  moved.
- [ ] 3.5 Required checks green at the head, Copilot's review at the exact
  head read, every thread resolved.

## 4. Archive

- [ ] 4.1 After the ratified packet lands, and on its own word: archive with
  `python3 scripts/proposal-support.py . archive
  amend-worker-input-budget-dispatch-wording` (never a bare `openspec
  archive`), landed as a merge commit and never a squash; retire this
  packet's `_LEDGER_SUBJECTS` row; move the README entry to the archive
  record. Then confirm `#1262` acceptance 3 on canon: no sentence calls an
  over-budget dispatch conformant, and the six scenarios are byte-identical to
  those on `main` `16779816`.

**3.5 AND 4.1 KEEP A LITERAL `- [ ]` DELIBERATELY.**
`scripts/proposal-support.py`:4632-4633 refuses an archive while any
`^- \[ \]` remains. Those two boxes are for acts that have not happened yet
(a green head with every thread resolved at landing, and the archive
itself), so the acts tick them and nothing ticks them in advance. § 0's boxes
were ticked by the ratifying word. Every box for work this packet will never
do carries `[~]`, in § 5.

## 5. Registered, not taken

- [~] 5.1 A CODE COMMENT ECHOES THE OLD CLAUSE.
  `scripts/doc_health/catalog_dispatch.py`:527-528 on `main` reads
  *"Dispatching it and letting the child refuse would be conformant and
  useless"*. It describes code that already obeys the SHALL NOT, so it is
  non-normative and misleads no implementation. It is left because editing it
  would give a wording packet a code surface. Owed to the next change that
  opens that file with a code surface declared.
- [~] 5.2 A TEST DOCSTRING ECHOES IT TOO.
  `tests/doc-health/test_semantic_input_budget.py`:506-508 reads
  *"Dispatching it and letting the child refuse is conformant and useless"*.
  Same reason, same owner.
- [~] 5.3 COPILOT'S COMMENT 4202036546 ALSO ASKED FOR THE ARCHIVED DELTA TO BE
  AMENDED. `#1262` declines that part, and so does this packet: an archive is
  the record of what was ratified and promoted, and it is never rewritten.
