# Tasks: add-unclassified-finding-class

Status: ratified
Ratified by: add-unclassified-finding-class

Nothing below group 3 has been done. Group 2 is the realization plan and every
box in it is open; group 3 records what the authoring session measured before
writing the proposal, which is evidence rather than implementation.

Build with Speckit, not `/opsx:apply`. OpenSpec ratifies; Spec Kit builds. This
change is ONE Spec Kit feature — group 2 — because the module edit and the tests
that hold it are a single vertical slice over one module and one test file, and
splitting them would produce two features neither of which is green alone.
Group 4 is recorded-not-fixed and group 5 is the archive act, last and open
until the merge it follows exists.

## 1. Ratification

- [x] 1.1 COMMISSIONED AND RATIFIED 2026-08-27 by Brett, in session, verbatim
      "Amend now", on the question put to him as a choice: leave the F4 report
      block's `unclassified` residual as a text row with no severity, no
      ranked-plan reach and no `--fail-on` reach, or make a nonzero count emit
      one `warning` — which adds a FIFTH finding class. He chose the amendment.
      The citation covers the DECISION TO BUILD and nothing else.
- [ ] 1.2 THE THREE ORCHESTRATOR DECISIONS ARE FLAGGED FOR VETO and this box
      stays OPEN until they are vetoed or affirmatively ruled — not-vetoed being
      neither. Each is independently reversible: D1 (ADDED-only, no MODIFIED
      block on the currency requirement), D2 (a fifth `FindingClass` with an
      anchored pattern, rather than an unplaced finding or a severity on the
      report block), D3 (one finding per run, carrying the first unplaced
      finding's repo and path, rather than one per repository).
- [ ] 1.3 IF D1 IS VETOED, this packet grows a `## MODIFIED Requirements` block
      restating "Currency of an active change's MODIFIED requirement blocks" in
      full — 14 scenarios and roughly 90 body lines, byte-for-byte — and the
      carriage ledger will then report this packet's own delta for every unit the
      restatement rewords. The predicted movement in the proposal stops being
      zero at that moment, and the number must be re-measured before the packet
      is put up again. Recorded so the cost of that veto is visible before it is
      taken.

## 2. Speckit F1 — the fifth class and its emit

One feature. RED first on every box that asserts behaviour: the test is written
against the delta's words, run, and seen to fail for the stated reason before
the module moves.

- [ ] 2.1 `scripts/doc_health/modified_block_currency.py`: add the fifth
      `FindingClass` to `CLASSES` — a class id of its own, the `warning` band,
      and this change's action line, "extend the class map, or fix the rule text
      drift". The existing four keep their order and their bands; the ordering
      comment's "gate-bearing arm reads FIRST" contract is unchanged, and the
      new entry goes LAST because it is not an arm.
- [ ] 2.2 Add the pattern that places it to `_CLASS_PATTERNS`, ANCHORED at the
      start of the rule text past the count, in the shape `_BLOCK_HEAD`
      established. RED FIRST, and the red case is the one that matters: an
      unplaced rule text that ITSELF begins `active MODIFIED block for '…' omits
      …`, so that an unanchored or substring probe files the drift finding under
      `scenario-titles` and the test says so.
- [ ] 2.3 `fam_modified_block_currency`: after the arms have run and before the
      family's own sort returns, count the findings `classify` places as
      `UNCLASSIFIED`. Where the count is nonzero, append EXACTLY ONE `warning`
      finding carrying that count, the first unplaced finding's rule text
      VERBATIM, its repo and its delta path, and the new action line. "First" is
      in the family's own report order, so the emit is deterministic: sort, read
      the first unplaced finding, append, sort again.
- [ ] 2.4 `classify`, `class_counts` and `class_summary` keep their signatures
      and their no-context discipline —
      `test_the_summary_reads_the_findings_and_nothing_else` asserts both
      structurally and must stay green untouched. The residual row keeps
      rendering on a nonzero count; it is not replaced, moved or reworded.
- [ ] 2.5 The four scenarios of the delta arrive as four tests in
      `tests/doc-health/test_modified_block_currency_reporting.py`, RED first:
      (1) every finding placed → no additional finding, and the counts still sum;
      (2) one unplaced rule text → exactly one `warning` naming the count and
      that rule text verbatim, carrying its repo and path and the action line,
      AND itself placed into the fifth class so the residual never counts it;
      (3) the finding renders in the ranked plan with severity, repo, path and
      action, and the residual row still renders in the family's block;
      (4) the map extended with a pattern that places the rule text → the finding
      is gone, the residual row is gone, and nothing is reported as an uncited
      resolution.
- [ ] 2.6 Move the three standing pins that count classes, deliberately and by
      name rather than by re-running until green:
      `test_the_class_registry_is_closed_ordered_and_states_a_band_per_class`,
      `test_each_of_the_five_rule_shapes_classifies_into_its_own_class` (five
      shapes and four classes become six and five), and the block-length pin in
      `test_the_block_is_not_a_finding_and_cannot_become_one` (`len(block) == 5`
      becomes 6). That last test's SUBJECT — that the block never re-enters
      `report.parse_previous` — must not weaken by one assertion.
- [ ] 2.7 SELF-GATE. `python3 scripts/doc-health.py --single-repo . --family
      modified-block-currency` on the realization branch reports the SAME eight
      findings as § 3.1, with the class block carrying a fifth row reading `0`
      and no residual row. Zero movement in every band, recorded in the feature's
      evidence as a before/after pair rather than asserted.
- [ ] 2.8 MUTATION ROUND. At minimum: (a) delete the fifth class's pattern from
      `_CLASS_PATTERNS` — 2.5's scenario (2) must fail on the drift finding
      counting itself; (b) change the emit from `> 0` to unconditional — 2.5's
      scenario (1) must fail; (c) emit per repository instead of per run — a test
      over a two-repository fixture must fail; (d) make the pattern unanchored —
      2.2's red case must fail. Each mutation reverted, each failure recorded.
- [ ] 2.9 NOTHING ELSE MOVES, proved mechanically: `git diff --stat
      <merge-base> -- .github/ scripts/ tests/` names only
      `scripts/doc_health/modified_block_currency.py` and
      `tests/doc-health/test_modified_block_currency_reporting.py`. No workflow
      file, no `families.py`, no `report.py`, no `Finding`, no other family.

## 3. Evidence recorded at proposal time

- [x] 3.1 Baseline, `python3 scripts/doc-health.py --single-repo . --family
      modified-block-currency` at `b5fb03f3`: **1 `warning`, 7 `info`**; class
      counts scenario-title completeness **1**, carriage ledger **7**, title
      resolution and ordering **0**, marker defects **0**; `unclassified` **0**,
      the residual row absent. This is the state § 2.7 must reproduce.
- [x] 3.2 THE MEASUREMENT D1 TURNS ON. `openspec/specs/doc-health/spec.md`
      contains `class map`, `finding classes`, `residual` and `class summary` at
      exactly ONE line between them — 1530, the three-arms sentence — and
      `unclassified` only at 1001 and 1153, both describing OTHER families'
      resolution classification. Canon enumerates ARMS, never CLASSES; the
      four-classes-to-three-arms gap is stated in the module and nowhere in the
      promoted specification. No MODIFIED block is therefore owed.
- [x] 3.3 The non-arm precedent that keeps the advisory paragraph true: canon
      requires marker defects reported and states no band for them; the module
      gives them `info`. The sentence "Every finding carries `warning` severity
      for the scenario-completeness and title-resolution arms and `info` for the
      carriage ledger" is therefore already an ARM-to-band map rather than an
      exhaustive one, and a second non-arm finding at `warning` leaves it true
      word for word.
- [x] 3.4 This packet's own delta, measured with the packet present: the family
      reads `## MODIFIED Requirements` blocks only, this packet carries an ADDED
      block and no MODIFIED block, and the run is byte-identical to § 3.1 with no
      finding naming any path under
      `openspec/changes/add-unclassified-finding-class/`.

## 4. Open — recorded, not fixed

- [ ] 4.1 THE FLIP IS UNTOUCHED. `add-modified-block-currency-check` § 7.2 — the
      scenario-title arm to `error` plus the `contested` classification, taken
      together by ruling on the discharge of the standing population — is neither
      advanced nor blocked by this change. The fifth class's band is NOT part of
      that flip and must not be folded into it silently: this finding is designed
      to disappear when somebody extends the map, and `contested` would turn that
      disappearance into an `error` under the uncited-resolution rule.
- [ ] 4.2 THE POPULATION IS EMPTY ON THIS TREE AND UNMEASURED EVERYWHERE ELSE.
      No aggregation run has been taken with this emit present, so the class this
      change reports has never been observed in the wild. Recorded rather than
      predicted; the first nightly after realization is the measurement.
- [ ] 4.3 THE OTHER FAMILIES HAVE NO CLASS MAP AND THEREFORE NO RESIDUAL. This
      change adds nothing to them and does not propose that they grow one. If
      per-class report blocks spread, this becomes a shared mechanism question
      rather than a per-family one — named here, not opened.

## 5. Archive

- [ ] 5.1 ARCHIVE AFTER REALIZATION AND AFTER THE MERGE. This change ships active
      and archives only once the realization is merged to `main` and green:
      `python3 -m pytest tests/doc-health`, `OPENSPEC_TELEMETRY=0 openspec
      validate --all --strict`, and a doc-health single-repo run moving by exactly
      § 2.7's prediction — zero in every band. The archive act is a separate later
      commit titled for the merge it follows, per `add-modified-block-currency-check`
      and `add-promotion-fidelity-check` (`01ff3434`).
