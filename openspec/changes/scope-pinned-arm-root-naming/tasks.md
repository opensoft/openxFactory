# Tasks — scope-pinned-arm-root-naming

Status: ratified
Ratified by: scope-pinned-arm-root-naming — Brett Heap (openxFactory
repository owner), first-hand, in session, lane `openxfactory-2` (display
`openXfactory-2`), verbatim ***"ratify 1052 when green, then 1050"*** — the
"1052" half of that word. THE ONE CITATION: openxFactory #1047, comment
https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379.
Record: `review/ratification-2026-09-16.md`.
Kind: tasks

`code_surface: none`, `target_release: implemented`. Under
`release-realization` an EMPTY code surface archives ON LANDING plus its own
task list rather than on merged-plus-green realization evidence — **and that
archive is a separate act on a separate word, not performed here** (§ 3).

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in its body, save 1.1's
RATIFIED annotation. **§ 1 IS BRETT HEAP'S ACT, TICKED HERE ONLY ON HIS
WORD** — recorded at openxFactory #1047, comment
https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379,
and transcribed rather than decided by this lane. **§ 3 STAYS ENTIRELY OPEN**:
the promotion of the block into `openspec/specs/document-lifecycle/spec.md`
and the closing line for openxFactory #1047 belong to the archive pull
request.

## 1. Ratification — RATIFIED (Brett Heap's word)

- [x] 1.1 **(OPERATOR)** Ratify or refuse `design.md` D-1 (the reading, as
      encoded), D-2 (widen the arm instead — not taken) and D-3 (delete the
      sentence — rejected), put as one multiple choice at `proposal.md` § *The
      decision, put for a veto* (OQ-1) with the recommendation first. Ratifying
      option (a) moves no byte of the delta; the packet's documents then take
      `Status: ratified` with one citation line each, `.openspec.yaml` gains
      `approved_by`/`approved_on` ADDED BESIDE the unmoved drafting pair, and a
      `review/ratification-<date>.md` record is written.
      RATIFIED 2026-09-16T13:43:18Z by Brett Heap, verbatim "ratify 1052
      when green, then 1050" — citation openxFactory #1047, comment
      https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379.

## 2. Filing — this pull request

- [x] 2.1 Packet authored at `openspec/changes/scope-pinned-arm-root-naming/`
      — `proposal.md` (front matter `code_surface: none`,
      `target_release: implemented`, `sequenced_after: []`), `design.md`,
      `tasks.md`, `.openspec.yaml` (ad-hoc origin declared through
      `scripts/proposal-support.py . declare-adhoc`, drafting provenance only,
      no approval pair claimed), and one spec delta under
      `specs/document-lifecycle/`.
- [x] 2.2 **THE `## MODIFIED` BLOCK IS GENERATED FROM CANON, NEVER
      TRANSCRIBED.** A script slices the promoted requirement *Prose tagging
      marker hygiene* whole (`openspec/specs/document-lifecycle/spec.md:218`
      through the next `### Requirement:`), asserts the target sentence occurs
      EXACTLY ONCE and replaces it, asserts the sibling scenario *A pinned
      target names a pin no resolution root carries*'s WHEN occurs EXACTLY
      ONCE and narrows it by one clause (round 1, R2: "…and at least one
      resolution root was selected for the run", so the empty-root-set case
      the new scenario covers keeps one outcome, not two), and appends ONE
      scenario. Verified two ways and both recorded in the pull request
      body — a unified diff of the generated block against canon's (THREE
      hunks: the sentence, the one WHEN clause, and the scenario, nothing
      else), and a `derive_units` comparison through the modified-block-currency
      family's own derivation (canon 209 units, block 215, TWO uncarried
      units, eight new).
- [x] 2.3 Sibling search for a co-writer of this requirement, taken at
      authoring on `8944758c` (before this packet's own delta existed): no
      OTHER active change holds a `## MODIFIED` block over *Prose tagging
      marker hygiene* — read in the indexed tree this packet is itself the one
      active change that now does, so the qualifier is load-bearing; the only
      OTHER active `document-lifecycle` delta is `prepare-openspec-1-12-readiness`,
      an `## ADDED` requirement touching nothing this packet writes.
      `sequenced_after: []` is therefore a
      CORROBORATED root claim rather than an assumed one.
- [x] 2.4 README "OpenSpec Records → Active changes" bullet added.
- [x] 2.5 Validation recorded in the pull request body —
      `OPENSPEC_TELEMETRY=0 openspec validate scope-pinned-arm-root-naming
      --strict` and `--all --strict`, `python3 scripts/proposal-support.py .
      verify`, `python3 scripts/validate-sequenced-after.py . --ledger-diff`,
      `python3 scripts/doc-health.py --single-repo . --as-of <date> --family
      modified-block-currency`, and `pytest -q tests/doc-health`, each with its
      result and with the pre-existing failures of `origin/main` named as such.
- [x] 2.6 Per-change sweep-ledger row seeded from the live corpus in a SECOND
      commit after the pull request existed
      (`python3 scripts/validate-sequenced-after.py . --seed-ledger --moved-by
      '#<PR>'`), the PR number being unknowable in the first.
- [x] 2.7 Carriage-ledger self-gate reconciled: this packet's active
      `## MODIFIED` block opens ONE `info` row in the
      modified-block-currency family, and
      `tests/doc-health/test_modified_block_currency_self_gate.py` asserts that
      population with `==` and never `<=`, so an unnamed row would red the
      required `pytest-suite` check for every open pull request in this
      repository. The row is added with its narrative and its count, as the
      gate's own failure message directs; NO ASSERTION, PREDICATE OR THRESHOLD
      IN THAT MODULE MOVED. It retires when this packet archives and its block
      is promoted.

## 3. Archive — OPEN (a separate act on a separate word)

- [ ] 3.1 **(OPERATOR)** Promote the `## MODIFIED` block onto
      `openspec/specs/document-lifecycle/spec.md` byte-identically and archive
      the packet to `openspec/changes/archive/<date>-scope-pinned-arm-root-naming/`
      through `scripts/proposal-support.py . archive`, on the word that
      authorizes it. `code_surface: none` archives ON LANDING plus this task
      list, so nothing is held behind realization evidence — but nothing
      archives on this pull request's landing alone either.
- [ ] 3.2 **(OPERATOR)** Retire this packet's `_LEDGER_SUBJECTS` row in the
      archive act, its condition ("retires when the block is promoted") being
      discharged there, and close openxFactory #1047 in that pull request.
