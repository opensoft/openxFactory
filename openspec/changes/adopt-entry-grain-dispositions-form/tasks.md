# Tasks: adopt-entry-grain-dispositions-form

Status: draft

**NOTHING IN § 1 IS TICKED, AND THAT IS THE STATE OF THE WORK RATHER THAN AN
OVERSIGHT.** This pull request FILES a proposal. § 1 is Brett Heap's ratify or
refuse and this lane ticks no box in it; § 2 is the filing itself and is the
only section this pull request performs; § 3 is the realization, a SEPARATE
later pull request on a separate word; § 4 is the archive, held behind
merged-plus-green realization evidence and a further word. No byte of
`scripts/doc_health/pin_shapes.py`, of `tests/doc-health/test_pin_shape_adapter.py`,
of any pin verifier, of any record under `contracts/` or of any file under
`openspec/specs/` moves anywhere in this pull request.

## 1. Ratification — BRETT HEAP'S WORD, NOT THIS LANE'S

- [ ] 1.1 **RULE `design.md` D-2 — the entry-grain reading is the OPTIONAL
      member's FORM and not a new required member.** Recommended: (a), change
      `_is_disposition_list` only; `dispositions:` stays optional, stays out of
      the shape-guard-required set, and the measured `(29, 27, 2)` table split
      does not move. The alternative (b) — make `dispositions:` REQUIRED — is
      priced in D-2: WIDER than the guard, two canon passages rewritten, a
      carriage-ledger row owed, and a guard leg asserting a refusal the verifier
      does not make.
- [ ] 1.2 **RULE `design.md` D-3 — act at all, rather than leave it as it
      stands.** Recommended: adopt. (a) LEAVE AS IS is the round-8 ruling's own
      position and is priced there, including what it costs: the adapter stays
      NARROWER than the guard on exactly the trees it exists for, and the
      asymmetry with `pinned_by_commit_only:` stays unexplained. (c) restating
      the verifier's entry rules as PROSE in canon and (d) having the adapter
      CALL the verifier are both refused in D-3 on canon's own words; a veto
      there re-opens the requirement rather than this scenario.
- [ ] 1.3 **CONFIRM the `## MODIFIED` delta is the whole normative act** — ONE
      scenario added to *Prose tagging marker hygiene*, every other promoted
      unit of that requirement carried VERBATIM (`diff` against
      `openspec/specs/document-lifecycle/spec.md:218-688` shows exactly the
      eight inserted lines), and no second capability touched. A veto here is a
      veto of the scenario's wording and costs one block.
- [ ] 1.4 **CONFIRM that ratifying § 1 authorizes NO REALIZATION.** Ratification
      admits the scenario to the packet and nothing more: § 3 stays open, the
      adapter and its tests stay untouched, and the realization is a later pull
      request on a separate word.

## 2. The filing — THIS PULL REQUEST, AND THE WHOLE OF IT

- [x] 2.1 **MEASURE the verifier's pure entry-grain guard before writing
      anything**, by importing `scripts/validate-openspec-cli-pin.py` at its
      fixed authored path and CALLING `pinned_dispositions` on in-memory records
      — no file, no `git`, no network. Recorded as `design.md` D-1: seven
      readings, each with its condition line, the line the `PinRefusal` was
      raised from, and the input that reached it.
- [x] 2.2 **MEASURE the adapter's verdict on the same records**
      (`judge(record, "openspec-cli")` over `contracts/openspec-cli-pin.yaml`
      with each value substituted): EIGHT accepted that the guard refuses, ZERO
      refused that the guard admits.
- [x] 2.3 **MEASURE the other optional member for comparison** —
      `pinned_by_commit_only:`, whose verifiers refuse a non-string entry
      (`scripts/verify-openxwallet-pin.py:449-454`,
      `scripts/validate-openreposhape-pin.py:493-498`) and whose adapter form
      `_is_path_only_list` ALREADY refuses `[{}]`. Recorded as D-1's second
      table.
- [x] 2.4 **AUTHOR the packet** — `proposal.md`, `design.md`, `tasks.md`,
      `.openspec.yaml` (drafting provenance only, `kind: ad_hoc`, declared
      through `scripts/proposal-support.py . declare-adhoc`), and ONE
      `## MODIFIED Requirements` delta over `document-lifecycle`.
- [x] 2.5 **LIST the change in the README "OpenSpec Records → Active changes"
      block.**
- [ ] 2.6 **SEED the per-change sweep-ledger row** in
      `tests/sequenced_after/corpus-ledger.yaml` with
      `scripts/validate-sequenced-after.py . --seed-ledger --moved-by '#<PR>'`,
      in a second commit once the pull request number exists.
- [x] 2.7 **VALIDATE** — `OPENSPEC_TELEMETRY=0 openspec validate
      adopt-entry-grain-dispositions-form --strict` and `--all --strict`,
      `python3 scripts/proposal-support.py . verify`,
      `python3 scripts/validate-sequenced-after.py . --ledger-diff`, the
      `tests/doc-health` suite, and `doc-health.py` over the families this
      packet touches. Results in the pull request body.

## 3. Realization — ONE LATER PULL REQUEST, ON A SEPARATE WORD

- [ ] 3.1 **`scripts/doc_health/pin_shapes.py`: extend `_is_disposition_list`
      to the entry grain**, transcribing D-1 rows 2-6 and NOTHING ELSE. Keep
      `value is None or ...` and the empty list accepted; keep the member in
      `SHAPE_C.optional` and out of `SHAPE_C.required`. Transcribe the two
      corrected readings exactly: the falsey-not-absent test for the six
      required keys (so `cited_to: []` is reported as the MISSING key, matching
      `:818-827`), and the `is not None` + case-folded test for `level` (so
      `"error"` is admitted and `""` refused, matching `:837-848`).
- [ ] 3.2 **Carry the constants BY TRANSCRIPTION, beside the existing ones**
      (`pin_shapes.py:65-93`), each with its measured citation:
      `DISPOSITION_REQUIRED` (`:353-354`), `DISPOSITION_AUTHORITY` (`:361`),
      `BLOCKING_LEVELS` (`:366`). A transcription, never an import: the adapter
      imports no verifier.
- [ ] 3.3 **Move the member's guard-leg citation with it.** The entry today
      carries `Citation(_OPENSPEC_CLI, 801)` (`pin_shapes.py:421-422`) — the
      absent-is-empty line. Give the entry-grain reading its own measured
      citation(s) at the lines D-1 names, and note in code why the optional
      entry's citation now CAN name an importable guard
      (`pinned_dispositions`) where the absent-is-empty line could not.
      `test_guard_leg_every_cited_line_still_reads_the_member_it_was_measured_from`
      asserts `pin.get("<spelling>")` appears on a CITED line and ranges over
      the REQUIRED table only (`_tracked_table`, `test_pin_shape_adapter.py:99`),
      so the realization decides — and states — whether the optional arm gets a
      route of its own or a parallel helper; either way `:813` onwards does not
      read `pin.get("dispositions")` and MUST NOT be cited as though it did.
- [ ] 3.4 **`tests/doc-health/test_pin_shape_adapter.py`: the optional arm's
      ENTRY case, as a CALL.** Import `scripts/validate-openspec-cli-pin.py` at
      its fixed authored path (the way the guard leg already imports verifiers),
      call `pinned_dispositions` on `contracts/openspec-cli-pin.yaml` carrying
      each malformed entry, assert it raises `PinRefusal`, and assert
      `ps.judge(record, "openspec-cli")` refuses the SAME record naming
      `dispositions`. One case per D-1 row 2-6.
- [ ] 3.5 **Regressions named in the finding, explicitly:** `[{}]`, `[null]`,
      and an entry missing `cited_to`. Plus the two boundary cases the
      measurement turned up: `cited_to: []` (reported as the missing key) and
      `level: "error"` (ADMITTED, case-folded).
- [ ] 3.6 **The negative side, so the form does not drift WIDER:**
      `dispositions:` absent, `null` and `[]` all still ACCEPTED, and
      `contracts/openspec-cli-pin.yaml` as it stands — six entries, all
      admitted by the guard today — still ACCEPTED by `judge`, which is the
      record leg's own assertion for this member.
- [ ] 3.7 **Leave `test_the_table_ranges_over_twenty_nine_member_entries_split_twenty_seven_two`
      at `(29, 27, 2)`** and
      `test_the_adapter_is_necessary_and_not_sufficient_and_the_boundary_is_named`
      passing unchanged: the member is still absent-is-empty, so
      `judge(_without(RECORDS["openspec-cli"], "dispositions"), "openspec-cli")`
      is still ACCEPTED. A realization that moved either has changed the shape
      table and is outside this packet.
- [ ] 3.8 **Update the adapter's own docstrings** — `_is_disposition_list`
      (`:217-223`) and the `SHAPE_C.optional` comment (`:418-419`) — so the code
      states the entry grain and its citations, as `_is_path_only_list` already
      does for the other optional member.
- [ ] 3.9 **Run the realization's evidence:** `pytest -q tests/doc-health`,
      `pytest -q tests/openspec_cli_pin`, and
      `python3 scripts/doc-health.py --single-repo . --family tag-hygiene`,
      with no new finding on `contracts/`.

## 4. Archive — ON MERGED-PLUS-GREEN REALIZATION EVIDENCE

- [ ] 4.1 **Archive on the realization pull request being MERGED and GREEN**,
      not on this filing landing: `code_surface:` is non-empty, and under
      *Realization archive gate* a non-empty code surface archives on
      merged-plus-green realization evidence rather than on landing.
- [ ] 4.2 **Promote the `## MODIFIED` block into
      `openspec/specs/document-lifecycle/spec.md`** at the archive, and confirm
      the promotion is byte-identical for every carried unit.
- [ ] 4.3 **Re-seed the sweep-ledger row** for the archived state
      (`--seed-ledger --moved-by '#<archive PR>'`), and check the
      carriage-ledger self-gate again: a block promoted byte-identically opens
      no row and retires any this packet held.
