# Tasks: add-unclassified-finding-class

Status: ratified
Ratified by: add-unclassified-finding-class

Nothing below group 3 has been done. Group 2 is the realization plan and every
box in it is open; group 3 records what the authoring session and the packet
review measured before the packet was put up, which is evidence rather than
implementation.

Build with Speckit, not `/opsx:apply`. OpenSpec ratifies; Spec Kit builds. This
change is ONE Spec Kit feature — group 2 — because the module edit, the pins it
moves and the tests that hold it are a single vertical slice over one module and
one test file, and splitting them would produce two features neither of which is
green alone. Group 4 is recorded-not-fixed and group 5 is the archive act, last
and open until the merge it follows exists.

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
      report block), D3 (one finding per DISTINCT UNPLACED RULE SHAPE per run —
      rewritten at packet review 2026-08-27, previously one per run).
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
the module moves. Every line reference below was read at `69c4a218` and must be
re-resolved by name if the file has moved under the feature.

- [ ] 2.1 `scripts/doc_health/modified_block_currency.py`: a FOURTH severity
      constant, `_DRIFT_SEVERITY = WARNING`, NOT a reuse of `_LAUNCH_SEVERITY`.
      The module states the reason for its existing split at `:137` — "The other
      two are separate constants precisely so that flip cannot drag them" — and
      it applies here exactly: § 7.2 of `add-modified-block-currency-check` flips
      `_LAUNCH_SEVERITY` to `error`, and this class must not ride that flip (see
      § 4.1). The drag would also be INVISIBLE: `FindingClass.band` reads the
      constant and the registry pin reads the band off the class, so a shared
      constant moves the caption and the finding together and no pin notices.
      Update `:137`'s "THREE OF THEM" to four. Add `_DRIFT_ACTION`, verbatim:
      "extend the class map in `scripts/doc_health/modified_block_currency.py`,
      or fix the drifted rule text the finding names". It carries NO interpolated
      delta path, because `test_every_finding_carries_its_class_s_band_and_action`
      (`:538-547`) asserts `f.action == klass.action` against a class constant —
      the path is already the finding's own `path` field and is quoted in its
      rule text.
- [ ] 2.2 The FIFTH `FindingClass` in `CLASSES`: id `unplaced`, label
      `unplaced-finding drift`, band `_DRIFT_SEVERITY`, action `_DRIFT_ACTION`,
      NO gloss, appended LAST. **Neither the id nor the label may contain the
      substring `unclassified`** — `test_a_finding_the_map_cannot_place_is_counted_and_named`
      (`:334`) asserts that string's ABSENCE from a fully-classified summary, and
      a class label renders even at a count of zero, so the obvious name reddens
      a standing pin for a real reason. The class goes last because it is not an
      arm and the ordering comment's "the gate-bearing arm reads FIRST" contract
      is unchanged. No gloss, on the module's own stated rule at `:1315` — a
      gloss "would pad a line whose whole value is being short enough to read at
      a glance"; update that sentence's numerals (two of FIVE carry one, three
      do not).
- [ ] 2.3 The pattern that places it, in `_CLASS_PATTERNS`, ANCHORED at the start
      of the rule text in the shape `_BLOCK_HEAD` established. RED FIRST, and the
      red case is the one that matters: an unplaced rule text that ITSELF begins
      `active MODIFIED block for '…' omits …`, quoted inside the drift finding,
      so that an unanchored or substring probe files the drift finding under
      `scenario-titles` and the test says so. This is the delta's fourth
      scenario.
- [ ] 2.4 `fam_modified_block_currency`: after the arms have run, group the
      findings `classify` places as `UNCLASSIFIED` BY SHAPE — rule texts equal
      after every single-quoted span, every double-quoted span and every run of
      digits is replaced by a fixed placeholder, which is the same grammar
      `_CLASS_PATTERNS` is written in (`_TITLE_REPR` and `\d+`). Per shape,
      append EXACTLY ONE `warning` carrying that shape's count, the FIRST
      instance's rule text VERBATIM, its repo and its delta path, and
      `_DRIFT_ACTION`. "First" is in the family's own report order, so the emit
      is deterministic: sort, group, append, sort again.
- [ ] 2.5 `classify`, `class_counts` and `class_summary` keep their signatures
      and their no-context discipline —
      `test_the_summary_reads_the_findings_and_nothing_else` asserts both
      structurally and must stay green untouched. The residual row keeps
      rendering on a nonzero count; it is not replaced, moved or reworded.
- [ ] 2.6 The FIVE scenarios of the delta arrive as tests in
      `tests/doc-health/test_modified_block_currency_reporting.py`, RED first:
      (1) every finding placed → no additional finding, and the counts still sum;
      (2) an unplaced rule text → one `warning` per distinct shape naming that
      shape's count and the first instance's rule text verbatim, carrying its
      repo and path and the action line, AND itself placed into the fifth class
      so the residual never counts it; (3) two unplaced findings differing only
      in a quoted span and a digit run → ONE finding naming the count two, and
      two findings differing outside those → TWO findings; (4) the anchored
      pattern, per § 2.3; (5) the map extended → the finding and the residual row
      are both gone, and nothing is reported as an uncited resolution.
- [ ] 2.7 THE STANDING PINS THAT RED ON REALIZATION, moved by name rather than by
      re-running until green. In
      `tests/doc-health/test_modified_block_currency_reporting.py`:
      `test_the_class_registry_is_closed_ordered_and_states_a_band_per_class`
      (`:115`); `test_each_of_the_five_rule_shapes_classifies_into_its_own_class`
      (`:150` — five shapes and four classes become six and five);
      `test_the_summary_states_every_class_with_its_count_and_band`
      (`:287-294`, the VERBATIM four-row list);
      `test_the_block_renders_under_the_heading_before_the_first_row` (`:422`,
      which pins the `marker defects` bullet as the LAST row and asserts the
      blank line after it — the new class is appended last, so both assertions
      move to it); `test_every_finding_carries_its_class_s_band_and_action`
      (`:538-547`); and the `len(block) == 5` pin inside
      `test_the_block_is_not_a_finding_and_cannot_become_one` (`:707` → 6). That
      last test's SUBJECT — that the block never re-enters
      `report.parse_previous` — must not weaken by one assertion.
      NOT in this roster, deliberately:
      `test_the_block_renders_on_a_run_that_found_nothing` (`:429`) carries "All
      four counts read 0" in its DOCSTRING only — its assertions survive the
      fifth class untouched, so it is a numeral fix and belongs to § 2.12, not
      here. A pin roster that lists prose is a roster a reader stops trusting.
- [ ] 2.8 THE FIXTURE TREE, ruled at packet review 2026-08-27 and BEHAVIOURAL
      rather than an exemption: `tests/doc-health/fixtures/modified-block-currency-unplaced/`.
      `ALL_TREES` globs `modified-block-currency*`, so the tree joins the
      corpus-wide pins that iterate it — but **its presence in `ALL_TREES` does
      NOT by itself exercise the fifth class.** `_fixture_findings` calls
      `fam_modified_block_currency` with no seam, so over the unmodified map this
      tree contributes only PLACED findings and `:538-547`'s
      `all(checked.values())` still fails on `unplaced: 0`. **`:538-547`
      therefore gains a MONKEYPATCHED PASS over this tree — one pattern removed
      from `_CLASS_PATTERNS` — and that pass is what exercises the class.**
      **RED EXPECTATION**: with the tree present and the fifth class absent, the
      amended `:538-547` fails on `unplaced: 0`; with the class present and the
      emit wired, the monkeypatched pass drives one drift finding through
      `fam_modified_block_currency`, `classify`, `class_summary` and
      `report.render`, and the pin passes on a measured row rather than a
      constructed `Finding`.
      **THE AMENDED PASS MUST NOT INDEX `by_id` WITH `UNCLASSIFIED`.** `:542` is
      `by_id[mbc.classify(f)]`, and `UNCLASSIFIED` is deliberately not a class id,
      so the induced-unplaced arm findings raise `KeyError` there — a red that is
      a crash rather than the assertion this pin exists to make. The pass asserts
      explicitly over the induced-unplaced findings, or skips them into the drift
      count, and the drift finding itself goes through `by_id` like any other.
      **THE TREE'S REQUIREMENT TITLES MUST BE PLAIN** — no title may contain
      another class's phrase (`omits`, `does not carry`, `carries a … marker by`,
      `resolves to no promoted requirement`, `the ordering of MODIFIED blocks`).
      F2's `CLASSIFIERS` (`test_modified_block_currency_fixtures.py:139-145`) are
      UNANCHORED substring probes, and
      `test_every_finding_falls_into_exactly_one_class` asserts `len(hits) == 1`
      over `ALL_TREES`, so a corpus-supplied phrase in a title would fail that
      pin from the new tree — the trap that narrowed F1's own `_ledger` helper.
      **THE TREE CARRIES A PROVENANCE README**, per F2's convention and its
      checker `test_every_fixture_tree_this_feature_adds_carries_a_provenance_note`:
      line 3 is the machine-readable provenance line and this tree is
      `SYNTHESIZED` (case-sensitive, whole-word), being constructed for this
      class rather than reconstructed from history.
      **THE TRIGGER IS A REMOVED PATTERN, NOT A CRAFTED TITLE, AND THAT IS
      MEASURED** — see § 3.5. No corpus can produce an unplaced rule text while
      the map is complete, because every arm's rule text is a fixed prefix plus
      `{title!r}` and `_TITLE_REPR` admits every `repr` Python can emit. So the
      tree supplies REAL arm findings and the test induces the drift the class
      exists to report — one pattern removed from `_CLASS_PATTERNS`, which is
      precisely the live condition "the map has drifted behind the arms". The
      family, the classifier, the summary and the renderer all run unmodified.
      Recorded as a decision of this feature: reversible, and if the review lane
      prefers a different seam it is a one-test change rather than a re-scope.
- [ ] 2.9 AMEND `specs/022-modified-block-currency-reporting/contracts/report-section.md`,
      which is byte-level ("everything here is asserted by a test; nothing is a
      suggestion") and enumerates the four classes four times: `:17-24` the
      per-class bullets, `:33-45` the worked example, `:98-109` the class-map
      grammar, `:116-123` the action-line table. All four gain the fifth class;
      the residual bullet at `:26-31` is unchanged and stays. A fifth class that
      landed without this leaves the corpus carrying a byte-level contract that
      is false about the code it describes.
- [ ] 2.10 `tests/doc-health/test_modified_block_currency_self_gate.py`: add a
      FOURTH probe to
      `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
      (`:661-702`), WITH its positive control — the probe string is first
      asserted to be the module's own wording, exactly as the three existing
      probes are, so a misspelled probe fails on the probe rather than reading a
      vacuous zero against the corpus. The probe asserts the drift class reads
      zero over the real tree, and the test's docstring numerals move from three
      classes to four.
- [ ] 2.11 `tests/doc-health/test_modified_block_currency_fixtures.py`: the
      FR-023 snapshot (`:1127-1146`) gains `_DRIFT_SEVERITY` in its severity
      tuple, so the snapshot stays complete over the module's severity constants.
      **The public-callable list is UNCHANGED** — the emit adds no public
      callable, the new class being a `FindingClass` instance and the new
      constants private — and the box is discharged by asserting that, not by
      editing the list. Correct the stale numeral at `:1117` ("its four finding
      classes").
- [ ] 2.12 THE NUMERAL SWEEP, as one task so none is left behind. Module: `:40`
      ("THREE ARMS, FOUR FINDING CLASSES"), `:137` (§ 2.1), `:1299` ("this
      family's four finding classes"), `:1315` (the gloss sentence, § 2.2),
      `:1349` ("FOUR ENTRIES FOR FIVE RULE SHAPES"). Tests:
      `test_modified_block_currency.py:16`; `…_reporting.py` `:5`, `:39`,
      `:116-117`, `:151`, `:429`; `…_fixtures.py:1117` (§ 2.11). Each is prose
      stating a count that this change makes false, and a count only a human
      re-reads is the drift class `family_enumeration` exists for.
- [ ] 2.13 SELF-GATE. `python3 scripts/doc-health.py --single-repo . --family
      modified-block-currency` on the realization branch reports the SAME
      findings as the run taken at that branch point — seven at `45ba637a`, per
      § 3.1 — with the class block carrying a fifth row reading `0` and no
      residual row. **Take the before figure at the branch point rather than
      reading § 3.1's**: the arms' population moves as active changes land, and
      it has already moved once under this packet. Zero movement in every band,
      recorded in the feature's evidence as a before/after pair rather than
      asserted.
- [ ] 2.14 MUTATION ROUND. At minimum: (a) delete the fifth class's pattern from
      `_CLASS_PATTERNS` — § 2.6's scenario (2) must fail on the drift finding
      counting itself; (b) change the emit from `> 0` to unconditional —
      scenario (1) must fail; (c) collapse the per-shape grouping to one finding
      per run — scenario (3)'s two-shapes half must fail; (d) make the pattern
      unanchored — § 2.3's red case must fail; (e) point `_DRIFT_SEVERITY` at
      `_LAUNCH_SEVERITY` — § 2.1's reasoning must be caught by a pin, and if it
      is not, that pin is missing and is owed here. Each mutation reverted, each
      failure recorded.
- [ ] 2.15 NOTHING ELSE MOVES, proved mechanically: `git diff --stat
      <merge-base> -- .github/ scripts/ tests/ specs/022-modified-block-currency-reporting/contracts/`
      names only `scripts/doc_health/modified_block_currency.py`, the three
      `tests/doc-health/test_modified_block_currency*.py` files touched above,
      the new fixture tree, and `contracts/report-section.md`. No workflow file,
      no `families.py`, no `report.py`, no `Finding`, no other family.

## 3. Evidence recorded at proposal time

- [x] 3.1 Baseline, `python3 scripts/doc-health.py --single-repo . --family
      modified-block-currency`. **AT THE CURRENT BASE `45ba637a`: 0 `warning`,
      7 `info`**; class counts scenario-title completeness **0**, carriage ledger
      **7**, title resolution and ordering **0**, marker defects **0**;
      `unclassified` **0**, the residual row absent. **This is the state § 2.13
      must reproduce**, and it must be RE-TAKEN at the realization branch point
      rather than copied from here — this figure has already moved once under
      this packet. History, so the movement is legible: at `b5fb03f3` and at the
      first catch-up merge `d808974d` the same run read **1 `warning`, 7 `info`**
      with the scenario arm at 1, against
      `add-composed-view-authoring` / "Composed views are read-only with a
      repository jump"; PR #444 declared that rename with a `Merged into` marker
      and the arm's standing population reached zero. The arm discharging its
      own finding is that arm working, and it says nothing about this change:
      the residual read `0` before and after.
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
- [x] 3.5 WHY § 2.8's TRIGGER IS A REMOVED PATTERN. Every rule text this family
      constructs is one of FIVE fixed prefixes plus `{title!r}` (module `:825`,
      `:881`, `:992`, `:1165`, `:1267`), and `_TITLE_REPR` admits both `repr`
      quotings and the `\\.` escape, so no corpus-supplied title can fall outside
      it. Fuzzed at packet review: 13 adversarial titles (empty, both quote
      kinds together, trailing backslash, tab, `\x7f`, and titles that themselves
      read `omits 1 of the 2 scenarios` and `carries a 'removed' marker by`) plus
      4000 random titles over an alphabet of quotes, backslashes, control
      characters and class phrases, times the five rule shapes = **20,065 rule
      texts, 0 unplaceable**. A crafted fixture title therefore cannot exercise
      the fifth class, and the honest behavioural trigger is the drift itself.
- [x] 3.6 THE PINS THAT WILL RED, enumerated before the feature starts so none is
      discovered as a surprise: `…_reporting.py` `:115`, `:150`, `:287-294`,
      `:422`, `:538-547`, `:707`; `…_self_gate.py:661-702`;
      `…_fixtures.py:1127-1146`. Read at `69c4a218`. `:429` is NOT among them —
      its "All four counts read 0" is a docstring numeral and its assertions
      survive; it is § 2.12's, not § 2.7's.

## 4. Open — recorded, not fixed

- [ ] 4.1 THE FLIP IS UNTOUCHED. `add-modified-block-currency-check` § 7.2 — the
      scenario-title arm to `error` plus the `contested` classification, taken
      together by ruling on the discharge of the standing population — is neither
      advanced nor blocked by this change. The fifth class's band is NOT part of
      that flip and must not be folded into it silently: this finding is designed
      to disappear when somebody extends the map, and `contested` would turn that
      disappearance into an `error` under the uncited-resolution rule. `_DRIFT_SEVERITY`
      exists so the flip cannot take this class with it by accident (§ 2.1).
- [ ] 4.2 THE POPULATION IS EMPTY ON THIS TREE AND UNMEASURED EVERYWHERE ELSE.
      No aggregation run has been taken with this emit present, so the class this
      change reports has never been observed in the wild. Recorded rather than
      predicted; the first nightly after realization is the measurement.
- [ ] 4.3 THE OTHER FAMILIES HAVE NO CLASS MAP AND THEREFORE NO RESIDUAL. This
      change adds nothing to them and does not propose that they grow one. If
      per-class report blocks spread, this becomes a shared mechanism question
      rather than a per-family one — named here, not opened.
- [ ] 4.4 THE SHAPE MASK IS THIS FAMILY'S, NOT THE PACKAGE'S. § 2.4's grouping
      rule (mask quoted spans and digit runs, compare) is written for this
      family's rule-text grammar. It is not proposed as a general finding-identity
      rule and nothing else may import it as one without its own change.

## 5. Archive

- [ ] 5.1 ARCHIVE AFTER REALIZATION AND AFTER THE MERGE. This change ships active
      and archives only once the realization is merged to `main` and green:
      `python3 -m pytest tests/doc-health`, `OPENSPEC_TELEMETRY=0 openspec
      validate --all --strict`, and a doc-health single-repo run moving by exactly
      § 2.13's prediction — zero in every band. The archive act is a separate later
      commit titled for the merge it follows, per `add-modified-block-currency-check`
      and `add-promotion-fidelity-check` (`01ff3434`).
