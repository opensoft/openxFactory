# Tasks — scope-pinned-arm-root-naming

Status: ratified
Ratified by: scope-pinned-arm-root-naming — Brett Heap (openxFactory
repository owner), first-hand, in session, lane `openxfactory-2` (display
`openXfactory-2`), verbatim ***"ratify 1052 when green, then 1050"*** — the
"1052" half of that word. THE ONE CITATION: openxFactory #1047, comment
https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379.
Record: `review/ratification-2026-09-16.md`.
Amended by: Brett Heap, the same ratifier, 2026-09-17, first-hand, in session —
an interactive multiple-choice selection, verbatim ***"Apply the narrowing"*** —
narrowing ONE scenario WHEN and nothing else. THE ONE CITATION: openxFactory
#1047, comment
https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5714432684.
Record: `review/ratification-2026-09-16.md` § Addendum, 2026-09-17. NO BOX OF
§ 1 MOVES BY IT.
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
and transcribed rather than decided by this lane. **§ 3 STAYED ENTIRELY OPEN
THROUGH THE FILING AND THE RATIFICATION** — the promotion of the block into
`openspec/specs/document-lifecycle/spec.md` and the closing of openxFactory
#1047 belong to the archive pull request — **AND IS DISCHARGED THERE,
2026-09-17, ON BRETT HEAP'S SEPARATE ARCHIVE WORD** (§ 3.1, § 3.2). Every § 3
tick below is likewise a diff in that pull request or a measurement recorded
verbatim in its body.

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
      no approval pair claimed — **THE AT-AUTHORING STATE OF 2026-09-15, WHICH
      THIS BOX RECORDS AND WHICH IS NO LONGER THE FILE'S STATE**: the
      ratification of 2026-09-16 ADDED `approved_by`/`approved_on` BESIDE the
      unmoved drafting pair, approval being a pure addition), and one spec
      delta under `specs/document-lifecycle/`.
- [x] 2.2 **THE `## MODIFIED` BLOCK IS GENERATED FROM CANON, NEVER
      TRANSCRIBED.** A script slices the promoted requirement *Prose tagging
      marker hygiene* whole (`openspec/specs/document-lifecycle/spec.md:218`
      through the next `### Requirement:`), asserts the target sentence occurs
      EXACTLY ONCE and replaces it, and appends ONE scenario — **THOSE TWO
      ACTS, AND ONLY THOSE TWO, ARE THE FILING GENERATION.** The script's
      SECOND single-occurrence replacement was added at FIX ROUND 1, not at
      filing: it asserts the sibling scenario *A pinned target names a pin no
      resolution root carries*'s WHEN occurs EXACTLY ONCE and narrows it by
      one clause (round 1, R2: "…and at least one resolution root was selected
      for the run", so the empty-root-set case the new scenario covers keeps
      one outcome, not two). Verified two ways at every round and recorded in
      the pull request body — a unified diff of the generated block against
      canon's, and a `derive_units` comparison through the
      modified-block-currency family's own derivation.
      **THE FIGURES, LABELLED BY ROUND RATHER THAN CONFLATED** (canon 209
      units and block 215 units throughout — canon is never edited and no
      round added or removed a bullet):
      **AT FILING** — TWO hunks (the sentence and the appended scenario),
      17 added / 4 removed, ONE uncarried unit, SEVEN new.
      **AFTER FIX ROUND 1's WHEN clause** — THREE hunks, 18 added / 5 removed,
      TWO uncarried, EIGHT new.
      **FROM FIX ROUND 5 ONWARD, AND CURRENTLY** — FOUR hunks, 21 added /
      8 removed, THREE uncarried, NINE new.
      ROUND HISTORY, IN ONE SENTENCE: fix round 5 refreshed one stale
      source-citation pointer canon itself carries (KEPT) and briefly narrowed
      the same WHEN clause FURTHER on a real Copilot finding, which fix round 6
      REVERTED because ratified normative text is the ratifier's to amend and
      not the lane's (`review/ratification-2026-09-16.md` § Addendum, 2026-09-16;
      RULING NEEDED posted to openxFactory #1047) — **AND BRETT HEAP ANSWERED
      THAT RULING ON 2026-09-17, verbatim *"Apply the narrowing"*
      (openxFactory #1047 comment 5714432684), so the WHEN promoted at the
      archive is round 5's text applied by the RATIFIER**
      (`review/ratification-2026-09-16.md` § Addendum, 2026-09-17). The
      figures do not move with it: the WHEN clause is one physical line under
      either wording.
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

## 3. Archive — ARCHIVED (Brett Heap's separate archive word)

- [x] 3.1 **(OPERATOR)** Promote the `## MODIFIED` block onto
      `openspec/specs/document-lifecycle/spec.md` byte-identically and archive
      the packet to `openspec/changes/archive/<date>-scope-pinned-arm-root-naming/`
      through `scripts/proposal-support.py . archive`, on the word that
      authorizes it. `code_surface: none` archives ON LANDING plus this task
      list, so nothing is held behind realization evidence — but nothing
      archives on this pull request's landing alone either.
      **ARCHIVED 2026-09-17 ON BRETT HEAP'S SEPARATE ARCHIVE WORD** — verbatim
      ***"merge 1051 when green, then archive 1047"***, 2026-09-17, first-hand,
      in session to lane `openxfactory-2` (display `openXfactory-2`, session
      c0d09b6d). THE ONE CITATION: openxFactory #1047, comment
      https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5714241892.
      Performed by `python3 scripts/proposal-support.py . archive
      scope-pinned-arm-root-naming --yes` — NEVER bare `openspec` — which
      printed **`ORIGIN RETAINED scope-pinned-arm-root-naming (declaration
      unchanged since the ratifying commit f8eba3455c0a)`**; independently,
      `git diff f8eba345 HEAD -- .../.openspec.yaml` is EMPTY and no commit
      touched this packet between that merge and this act. Packet moved to
      `openspec/changes/archive/2026-09-17-scope-pinned-arm-root-naming/`.
      **PROMOTION MEASURED BYTE-IDENTICAL, not asserted:** the promoted
      requirement *Prose tagging marker hygiene* in
      `openspec/specs/document-lifecycle/spec.md` and this packet's `##
      MODIFIED` block are both **41,984 bytes, sha256
      `c009f5cc3e4aa5aa…`** (the requirement text from its `### Requirement:`
      line, canon's trailing blank separator before the next `### Requirement:`
      excluded on both sides, which is the convention PR #1042's archive used);
      canon's `git diff --numstat` reads **21 added,
      8 removed** — exactly the block's own measured canon-diff. The text
      promoted carries the RATIFIER'S 2026-09-17 AMENDMENT of the sibling
      scenario's WHEN (§ 2.2; `review/ratification-2026-09-16.md` § Addendum,
      2026-09-17), and no other post-ratification movement.
- [x] 3.2 **(OPERATOR)** Retire this packet's `_LEDGER_SUBJECTS` row in the
      archive act, its condition ("retires when the block is promoted") being
      discharged there, and close openxFactory #1047 in that pull request.
      **DONE, AND MEASURED FIRST.** A row for this packet DID exist —
      `("scope-pinned-arm-root-naming", "document-lifecycle", "Prose tagging
      marker hygiene")` in `_LEDGER_SUBJECTS`,
      `tests/doc-health/test_modified_block_currency_self_gate.py` — opened by
      § 2.7 at filing under the condition this box discharges. It is RETIRED in
      the archive commit with a note in its place, and the gate's population
      narrative and docstring say which subject moved and why (fifteen →
      fourteen), as the gate's own failure message directs. Measured over the
      archived tree: `--family modified-block-currency` reports 14 `info` rows,
      none naming this packet, none unnamed.
      **THE ISSUE CLOSES BY THE LANE'S HAND, NOT BY A KEYWORD.** This pull
      request's body carries `refs #1047` and NO closing keyword, so the merge
      does not close it; the lane closes openxFactory #1047 itself immediately
      after posting the ARCHIVED record there, which is the record order the
      lane-collision protocol requires and the same discharge this box names.
