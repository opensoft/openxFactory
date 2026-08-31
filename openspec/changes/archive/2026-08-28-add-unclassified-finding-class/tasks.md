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
      rewritten at packet review 2026-08-27, previously one per run; its SHAPE
      IDENTITY was then widened by Brett's amendment of 2026-08-28, § 1.4, and
      the veto flag on D3 as amended stays open with the other two).
- [ ] 1.3 IF D1 IS VETOED, this packet grows a `## MODIFIED Requirements` block
      restating "Currency of an active change's MODIFIED requirement blocks" in
      full — 14 scenarios and roughly 90 body lines, byte-for-byte — and the
      carriage ledger will then report this packet's own delta for every unit the
      restatement rewords. The predicted movement in the proposal stops being
      zero at that moment, and the number must be re-measured before the packet
      is put up again. Recorded so the cost of that veto is visible before it is
      taken.
- [x] 1.4 AMENDED 2026-08-28 by Brett, in session, verbatim: "Amend: shape = arm
      template, all interpolations masked". Put to him as a multiple choice by
      the Speckit 026 review, which had measured that the ratified mask (quoted
      spans and digit runs only) leaves the promoted spec's path, the
      `[body]`/`[bullet]` unit-kind list, change-id lists and an unresolved
      block's `why` clause standing — so ONE dropped class-map entry yields
      SEVEN unplaced findings in SIX shapes on the 2026-08-28 openxFactory tree,
      six `warning` rows in the ranked plan for ONE map entry to write. He chose
      to amend the delta rather than ship the narrower grain. The delta's
      identity paragraph and its third scenario are reworded accordingly, the
      family now deriving the mask FROM ITS OWN ARM TEMPLATES; § 2.4 and § 2.6
      below carry the build. The measured table is in
      `specs/026-unplaced-finding-drift/plan.md` § OPEN-1. **The predicted
      severity movement is unchanged — ZERO in every band** — the mask being
      read only where the residual count is nonzero, which is nowhere today.

## 2. Speckit F1 — the fifth class and its emit

One feature. RED first on every box that asserts behaviour: the test is written
against the delta's words, run, and seen to fail for the stated reason before
the module moves. Every line reference below was read at `69c4a218` and must be
re-resolved by name if the file has moved under the feature.

**Speckit feature `026-unplaced-finding-drift` is that feature, and it is IN
FLIGHT.** It carries the group in full, including the shape grammar as AMENDED
on 2026-08-28 (§ 1.4): the review that raised the amendment is that feature's
own (`specs/026-unplaced-finding-drift/plan.md` § OPEN-1), and its
`test_the_drift_grain_is_one_finding_per_masked_arm_text_not_one_per_remedy`
already MEASURES the grain on the real tree — under the amended mask that
measurement reads ONE where it read six, and the test, its docstring and the
claims struck alongside it move with the rule.

**DISCHARGED 2026-08-28 by Speckit `026-unplaced-finding-drift` (PR #466, squash
`db2442ce`); per-task evidence in that feature's `tasks.md` and `evidence/`.**
That feature is no longer in flight: all 44 of its boxes are done, each of its
tasks cites the box of this group it realizes, and the RED-first log, the
mutation round and the self-gate before/after pair stay where they were written
rather than being copied here. Every box below is ticked against it. EIGHT carry
a `RECONCILED` clause rather than being ticked silently, because they were not
discharged exactly as authored — § 2.4, § 2.6 and § 2.14 by Brett's amendment of
2026-08-28 (PR #461, `6d100e51`, § 1.4), and § 2.3, § 2.7, § 2.8, § 2.10 and
§ 2.15 by defects in THIS PACKET that realization found, recorded as that
feature's plan decisions O3–O8 and its completion record. A box ticked without a
clause was discharged as written.

- [x] 2.1 `scripts/doc_health/modified_block_currency.py`: a FOURTH severity
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
- [x] 2.2 The FIFTH `FindingClass` in `CLASSES`: id `unplaced`, label
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
- [x] 2.3 The pattern that places it, in `_CLASS_PATTERNS`, ANCHORED at the start
      of the rule text in the shape `_BLOCK_HEAD` established. RED FIRST, and the
      red case is the one that matters: an unplaced rule text that ITSELF begins
      `active MODIFIED block for '…' omits …`, quoted inside the drift finding,
      so that an unanchored or substring probe files the drift finding under
      `scenario-titles` and the test says so. This is the delta's fourth
      scenario.
      **RECONCILED — plan § O3.** The fifth class's opening phrase is
      `this family's own class map has no pattern for `, DELIBERATELY not the
      residual row's "its own class map does not place": reusing the row's
      wording would leave § 2.10's positive control unable to tell the finding
      from the row, and it would pass on the wrong constant. Two readings of one
      fact, two spellings.
- [x] 2.4 `fam_modified_block_currency`: after the arms have run, group the
      findings `classify` places as `UNCLASSIFIED` BY SHAPE — **rule texts equal
      after EVERY FIELD THE ARM'S TEMPLATE INTERPOLATES is replaced by a fixed
      placeholder** (§ 1.4's amendment). Quoted spans and digit runs are the
      grammar `_CLASS_PATTERNS` is already written in (`_TITLE_REPR` and
      `\d+`), and they are NOT SUFFICIENT: the arms also interpolate
      `basis.spec_rel` (a repository-relative path), the `[body]`/`[bullet]`
      unit-kind list a ledger finding quotes, the ordering arm's change-id list,
      and the unresolved arm's `why` clause. **The mask is DERIVED FROM THE ARM
      TEMPLATES, not hand-listed** — the fixed prose of each of the five rule
      shapes (module `:825`, `:881`, `:992`, `:1165`, `:1267`) is the shape and
      every interpolation is masked — so the rule cannot drift from the arms the
      way an enumerated mask would, which is the same failure this whole class
      exists to report. Per shape, append EXACTLY ONE `warning` carrying that
      shape's count, the FIRST instance's rule text VERBATIM, its repo and its
      delta path, and `_DRIFT_ACTION`. "First" is in the family's own report
      order, so the emit is deterministic: sort, group, append, sort again.
      MEASURED TARGET, from `specs/026-unplaced-finding-drift/plan.md` § OPEN-1:
      with `carriage-ledger` dropped from the map, the real tree's 7 unplaced
      findings collapse to **ONE** drift finding, not six.
      **RECONCILED — the AMENDMENT (PR #461, `6d100e51`, § 1.4), and plan § O4.**
      As FIRST ratified this box asked for the lexical mask alone — quoted spans
      and digit runs — and that mask is now the fail-closed FALLBACK only: each
      arm renders through one registered `_ArmTemplate` so the fixed prose has a
      single definition, and `_shape` masks the `repr` spans with a
      left-to-right consumer before matching the templates first-match-wins, the
      shape BEING the matched template's id. And the quoted rule text is carried
      PLAIN rather than `repr`-wrapped, so the delta's "verbatim" stays literally
      true and `first.rule in drift.rule` holds. No field was added to
      `Finding`.
- [x] 2.5 `classify`, `class_counts` and `class_summary` keep their signatures
      and their no-context discipline —
      `test_the_summary_reads_the_findings_and_nothing_else` asserts both
      structurally and must stay green untouched. The residual row keeps
      rendering on a nonzero count; it is not replaced, moved or reworded.
- [x] 2.6 The FIVE scenarios of the delta arrive as tests in
      `tests/doc-health/test_modified_block_currency_reporting.py`, RED first:
      (1) every finding placed → no additional finding, and the counts still sum;
      (2) an unplaced rule text → one `warning` per distinct shape naming that
      shape's count and the first instance's rule text verbatim, carrying its
      repo and path and the action line, AND itself placed into the fifth class
      so the residual never counts it; (3) two unplaced findings FROM THE SAME
      ARM TEMPLATE differing only in the values it interpolates — a different
      quoted title, a different `basis.spec_rel`, a different unit-kind list,
      different change ids → ONE finding naming the count two; and two unplaced
      findings from DIFFERENT arm templates, differing in the fixed prose the
      mask leaves standing → TWO findings. **Both halves are written against the
      AMENDED rule (§ 1.4); a test that passes under the quoted-spans-and-digits
      mask alone does not discharge this box** — the path-differing and
      kind-list-differing pairs are exactly the cases the narrow mask split and
      the amendment joins. (4) the anchored pattern, per § 2.3; (5) the map
      extended → the finding and the residual row are both gone, and nothing is
      reported as an uncited resolution.
      **RECONCILED — the AMENDMENT (PR #461, `6d100e51`, § 1.4).** Scenario 3's
      two halves were reworded by the amendment and are discharged against the
      AMENDED rule, joined by
      `test_two_findings_of_one_template_differing_in_an_unquoted_field_are_one_shape`
      and `test_two_findings_of_different_templates_are_two_shapes` — the
      path-differing and unit-kind-list-differing pairs the narrow mask split
      and the wide mask joins.
- [x] 2.7 THE STANDING PINS THAT RED ON REALIZATION, moved by name rather than by
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
      **RECONCILED — plan § O8 and the completion record, on two counts.** The
      roster moves `test_each_of_the_five_rule_shapes_classifies_into_its_own_class`
      to six-and-five without saying its FUNCTION NAME must move; it did, to
      `test_each_of_the_six_rule_shapes_classifies_into_its_own_class`, a
      function name stating a count the code contradicts being the same defect
      § 2.12 sweeps out of the prose. And § 3.6 predicted EIGHT reddening pin
      sites; **FIVE** actually reddened, all in `..._reporting.py` — the
      five-rule-shapes pin's assertions survive a fifth class (only its name and
      docstring were false), the self-gate needed a probe ADDED rather than
      corrected, and the FR-023 snapshot is a POSITIVE list that a new PRIVATE
      constant cannot red.
- [x] 2.8 THE FIXTURE TREE, ruled at packet review 2026-08-27 and BEHAVIOURAL
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
      **RECONCILED — plan § O5.** This box names F2's provenance checker as
      though it would cover the new tree, and it would not: that checker
      iterates `NEW_TREES` — "the trees F2 adds" — and additionally requires each
      README to cite an F2 audit row and an
      `add-modified-block-currency-check § 3.<n>` section, neither of which this
      tree can honestly claim. Fabricating an audit row to satisfy a checker
      would be exactly the false-documentation defect this family exists to
      catch. So the tree joins `ALL_TREES` by glob as written, carries its
      `SYNTHESIZED` README to F2's convention, and this feature pins that README
      from its OWN test rather than by widening F2's list.
- [x] 2.9 AMEND `specs/022-modified-block-currency-reporting/contracts/report-section.md`,
      which is byte-level ("everything here is asserted by a test; nothing is a
      suggestion") and enumerates the four classes four times: `:17-24` the
      per-class bullets, `:33-45` the worked example, `:98-109` the class-map
      grammar, `:116-123` the action-line table. All four gain the fifth class;
      the residual bullet at `:26-31` is unchanged and stays. A fifth class that
      landed without this leaves the corpus carrying a byte-level contract that
      is false about the code it describes.
- [x] 2.10 `tests/doc-health/test_modified_block_currency_self_gate.py`: add a
      FOURTH probe to
      `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
      (`:661-702`), WITH its positive control — the probe string is first
      asserted to be the module's own wording, exactly as the three existing
      probes are, so a misspelled probe fails on the probe rather than reading a
      vacuous zero against the corpus. The probe asserts the drift class reads
      zero over the real tree, and the test's docstring numerals move from three
      classes to four.
      **RECONCILED — completion record 6, an UNFORESEEN pin.** The self-gate's
      `test_the_gate_reaches_the_corpus_only_through_the_family` allowlist moved
      too: the fourth probe's positive control has to reach BOTH `_DRIFT_RULE`
      and `_UNCLASSIFIED_LINE`, because the module source carries both constants
      and a probe matching only the ROW would pass that control and then read a
      vacuous zero. Two names declared with their reason in the allowlist's own
      convention; not one regex pattern changed.
- [x] 2.11 `tests/doc-health/test_modified_block_currency_fixtures.py`: the
      FR-023 snapshot (`:1127-1146`) gains `_DRIFT_SEVERITY` in its severity
      tuple, so the snapshot stays complete over the module's severity constants.
      **The public-callable list is UNCHANGED** — the emit adds no public
      callable, the new class being a `FindingClass` instance and the new
      constants private — and the box is discharged by asserting that, not by
      editing the list. Correct the stale numeral at `:1117` ("its four finding
      classes").
- [x] 2.12 THE NUMERAL SWEEP, as one task so none is left behind. Module: `:40`
      ("THREE ARMS, FOUR FINDING CLASSES"), `:137` (§ 2.1), `:1299` ("this
      family's four finding classes"), `:1315` (the gloss sentence, § 2.2),
      `:1349` ("FOUR ENTRIES FOR FIVE RULE SHAPES"). Tests:
      `test_modified_block_currency.py:16`; `…_reporting.py` `:5`, `:39`,
      `:116-117`, `:151`, `:429`; `…_fixtures.py:1117` (§ 2.11). Each is prose
      stating a count that this change makes false, and a count only a human
      re-reads is the drift class `family_enumeration` exists for.
- [x] 2.13 SELF-GATE. `python3 scripts/doc-health.py --single-repo . --family
      modified-block-currency` on the realization branch reports the SAME
      findings as the run taken at that branch point — seven at `45ba637a`, per
      § 3.1 — with the class block carrying a fifth row reading `0` and no
      residual row. **Take the before figure at the branch point rather than
      reading § 3.1's**: the arms' population moves as active changes land, and
      it has already moved once under this packet. Zero movement in every band,
      recorded in the feature's evidence as a before/after pair rather than
      asserted.
- [x] 2.14 MUTATION ROUND. At minimum: (a) delete the fifth class's pattern from
      `_CLASS_PATTERNS` — § 2.6's scenario (2) must fail on the drift finding
      counting itself; (b) change the emit from `> 0` to unconditional —
      scenario (1) must fail; (c) collapse the per-shape grouping to one finding
      per run — scenario (3)'s two-shapes half must fail; (d) make the pattern
      unanchored — § 2.3's red case must fail; (e) point `_DRIFT_SEVERITY` at
      `_LAUNCH_SEVERITY` — § 2.1's reasoning must be caught by a pin, and if it
      is not, that pin is missing and is owed here; (f) NARROW THE MASK BACK to
      quoted spans and digit runs only — § 2.6's scenario (3) must fail on the
      pair that differs by an interpolated path or unit-kind list, and the
      real-tree grain measurement must read six rather than one. Each mutation
      reverted, each failure recorded.
      **RECONCILED — plan § O6, and mutant (f) is the AMENDMENT's (PR #461,
      `6d100e51`).** Mutation (e) cannot be killed by ANY value comparison:
      `_DRIFT_SEVERITY = WARNING` and `_DRIFT_SEVERITY = _LAUNCH_SEVERITY` are
      value-identical until § 7.2 flips one, so every assertion about the
      constants' VALUES passes under both and the separately-assignable pin
      passes too. This box says the pin is owed here if it is missing, and it
      was: a SIMULATED FLIP that executes the module's own source with
      `_LAUNCH_SEVERITY` textually replaced by the package's `error` constant
      and asserts the scenario-title class moved while the drift class did not.
      Round as run: **9 mutants applied, 9 killed, 0 survivors** — the
      unanchored-pattern mutant survived its first attempt and exposed a
      near-miss adversarial title, since fixed.
- [x] 2.15 NOTHING ELSE MOVES, proved mechanically: `git diff --stat
      <merge-base> -- .github/ scripts/ tests/ specs/022-modified-block-currency-reporting/contracts/`
      names only `scripts/doc_health/modified_block_currency.py`, the three
      `tests/doc-health/test_modified_block_currency*.py` files touched above,
      the new fixture tree, and `contracts/report-section.md`. No workflow file,
      no `families.py`, no `report.py`, no `Finding`, no other family.
      **RECONCILED — plan § O7.** This box says "the three
      `tests/doc-health/test_modified_block_currency*.py` files"; **FOUR** move.
      `test_modified_block_currency.py` is named by § 2.12 for its `:16` numeral
      and carries O6's simulated-flip pin beside the family's other severity
      pins, so the packet already names all four between § 2.6 and § 2.12. A
      mechanical inaccuracy in this box rather than a scope change: the proof
      itself held, `.github/` and `openspec/` both diffing EMPTY.

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
      rule — mask every field this family's own arm templates interpolate, then
      compare the fixed prose that remains (as amended 2026-08-28, § 1.4) — is
      derived from THIS family's five rule shapes and is meaningful only against
      them. A family with different templates would derive a different mask. It
      is not proposed as a general finding-identity rule and nothing else may
      import it as one without its own change.

## 5. Archive

- [x] 5.1 ARCHIVE AFTER REALIZATION AND AFTER THE MERGE. This change ships active
      and archives only once the realization is merged to `main` and green:
      `python3 -m pytest tests/doc-health`, `OPENSPEC_TELEMETRY=0 openspec
      validate --all --strict`, and a doc-health single-repo run moving by exactly
      § 2.13's prediction — zero in every band. The archive act is a separate later
      commit titled for the merge it follows, per `add-modified-block-currency-check`
      and `add-promotion-fidelity-check` (`01ff3434`).
      **DONE — ARCHIVED 2026-08-28, on the merge-plus-green rule this box
      declared.**
      **REALIZATION AND AMENDMENT RE-VERIFIED FROM `main` AT THIS GATE, not read
      out of a pull-request body.** Both are confirmed ancestors of `origin/main`
      with `git merge-base --is-ancestor` (exit 0 on each):
      1. **PR #461 → `6d100e51`** — the DELTA AMENDMENT, "a drift shape is the
         arm's template with every interpolated field masked". It lands FIRST by
         construction: the realization's spec cites the amended text, so the
         feature waited on it.
      2. **PR #466 → `db2442ce`** — the realization, Speckit
         `026-unplaced-finding-drift`: the fifth class, its anchored pattern, the
         per-shape emit through registered `_ArmTemplate`s, the four test files,
         the behavioural fixture tree and the amended byte-level report contract.
      The live tree carries the advisory launch, re-read here rather than
      assumed: `modified-block-currency` is registered in `FAMILIES` and in
      `FAMILY_IDS` and is ABSENT from `FAMILY_RESOLUTION`, so § 7.2's flip is
      still owed and still unticked, and § 4.1 stands as authored.
      **THE GATE NUMBERS, all measured in this worktree at base `db2442ce`.**
      Before the archive act: `python3 -m pytest tests/doc-health -q` → **1270
      passed, 0 failed**; `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`
      → **76 passed, 0 failed (76 items)** = 24 active + 52 promoted specs;
      `python3 scripts/doc-health.py --single-repo .` → **5 critical, 11 error,
      41 warning, 11 info. New regressions vs previous report: 0**, and the same
      run with `--skip-family modified-block-currency` → **5 critical, 11 error,
      41 warning, 4 info** — movement **+0 `warning`, +7 `info`, 0 `error`, 0
      `critical`**, equal to the family's own per-severity counts
      (`--family modified-block-currency` → **0 critical, 0 error, 0 warning, 7
      info**). After the archive act: pytest **1270 passed, 0 failed**; validate
      **75 passed, 0 failed (75 items)** = 23 active + 52 specs, **−1** exactly
      as promotion of one change predicts; the single-repo run's severity
      headline **byte-identical — 5 critical, 11 error, 41 warning, 11 info, 0
      new regressions** — against **5 critical, 11 error, 41 warning, 4 info**
      skipped, the same **+0 / +7** movement.
      **THE FIFTH CLASS MOVED NOTHING, WHICH IS WHAT THE PACKET PREDICTED AND IS
      THE WHOLE OF ITS EVIDENCE.** The family's report block reads
      `scenario-title completeness: 0` / `carriage ledger: 7` / `title resolution
      and ordering: 0` / `marker defects: 0` / **`unplaced-finding drift: 0`**,
      and the residual row does NOT render — `- unclassified: ` occurs zero times
      in the report. The realization's own before/after evidence pair
      (`specs/026-unplaced-finding-drift/evidence/`) differs by **exactly one
      line**, the fifth class row reading `0`, over a FULL report covering all
      twenty-two families; this gate reproduced the same state independently at
      `db2442ce`. § 3.4's claim also re-measured and holds: **ZERO** findings name
      any path under `openspec/changes/add-unclassified-finding-class/`, this
      packet carrying an `## ADDED` block and the family reading
      `## MODIFIED Requirements` blocks only.
      **THE WHOLE REPORT DIFF ACROSS THE ACT IS THREE LINES AND NONE OF THEM IS A
      FINDING.** Canon words 218169 → 219088 (**+919**) and governance words
      690954 → 691873 (the SAME +919, those words moving from active-change prose
      into promoted prose), canon share 31.6% → 31.7%, and the promoted-specs row
      of the per-source table (160586 → 161505). Nothing new is reported
      anywhere, by any family, and — unlike this capability's sibling archives —
      **no finding DEPARTED either**, because an ADDED-only packet drew none to
      begin with.
      **NO TEST FELL DUE AT THIS ACT, AND THAT IS A CONSEQUENCE OF D1 RATHER THAN
      LUCK.** `add-modified-block-currency-check`'s archive re-aimed five tests
      and retired one, because that packet's own MODIFIED block was a live
      subject the act moved out of the active set. This packet has no MODIFIED
      block, drew no self-finding, and its delta is named by no self-gate
      subject, so the F3 self-gate and F5's own tests read the same corpus after
      the act as before: **1270 → 1270 passed, no re-aim, no retirement, no
      module changed.**
      **GROUP 2 IS TICKED AGAINST PR #466 AND EIGHT OF ITS BOXES CARRY A
      `RECONCILED` CLAUSE**, on the rule this capability's sibling archive ruled:
      an archived change carrying fifteen open build boxes reads as
      archived-UNREALIZED to a cold reader, which is a worse record than a tick
      that names its evidence. § 1.2 and § 1.3 are UNTOUCHED — the three
      orchestrator decisions were never vetoed and never affirmatively ruled, and
      not-vetoed is neither, so the veto flag stays open exactly as § 1.2
      demands; D1 was not vetoed, so § 1.3's conditional never fired. § 4 is left
      open as authored: § 4.2's first-nightly measurement is the one thing this
      act cannot supply, the population being empty on this tree and unmeasured
      everywhere else.
      **THE PROMOTION WAS VERIFIED PER REQUIREMENT BEFORE THE ACT, not after
      it.** A change whose subject is a family that polices lossy promotion, and
      that promoted lossily, would be the worst possible entry in this record.
      The delta is **ADDED-ONLY** — grepped, not recalled:
      `openspec/changes/add-unclassified-finding-class/specs/doc-health/spec.md`
      carries exactly ONE `## ` section header, `## ADDED Requirements`, and no
      `## MODIFIED`, `## REMOVED` or `## RENAMED` block anywhere. Its one
      requirement title, "A modified-block-currency finding its own class map
      cannot place is itself a finding", collides with **none** of canon's 38
      pre-existing titles, so promotion is a pure append and no restatement is at
      risk.
      **TABLE — `doc-health`, per requirement.**
      | requirement | canon before | delta | canon after | verdict |
      | --- | --- | --- | --- | --- |
      | `A modified-block-currency finding its own class map cannot place is itself a finding` (ADDED) | absent | 6 scenarios | 6 scenarios | pure append; the title collides with NONE of canon's 38 |
      | the other 38 requirements | — | untouched | unchanged | bytes identical, per requirement, and the file order of all 38 pre-existing titles preserved |
      | FILE | 38 requirements, 173 scenarios | — | 39 requirements, 179 scenarios | **+1 requirement, +6 scenarios** |
      **CANON AFTER THE ACT IS WHAT THE DELTA IMPLIES AND NOTHING ELSE.**
      `git diff --stat openspec/specs/doc-health/spec.md` → **1 file changed, 73
      insertions(+), 0 deletions(-)** — ZERO deletions, there being no promotion
      direction in which an ADDED-only delta could remove anything. The
      requirement lands LAST in the file, at line 2036, the three preceding
      headings unmoved.
      **AND PROVEN AS A BYTE DIFF OF THE REMAINDER, per the resolved precedent in
      `2026-08-27-add-modified-block-currency-check` § 8.2.** The REMAINDER is the
      whole document minus the appended requirement, each requirement running
      from its `### Requirement:` line to the next such line or to EOF; every
      `### ` heading in this file is a requirement heading (38 before, 39 after,
      0 non-requirement), so the definition is exact. Measured two ways, because
      the precedent's own construction carries a known artifact:
      • **slice construction** (cut the chunk out by its heading offsets) —
      **139505 == 139505 raw**, 139503 == 139503 after trailing-newline
      normalization;
      • **`split('\n### ')` + drop + `'\n### '.join`, the mbc construction** —
      **139505 vs 139504 raw**, 139503 == 139503 normalized. The one-byte gap is
      the precedent's own N2 artifact reproducing exactly: that construction is
      lossless EXCEPT when the dropped chunk is the file's LAST heading, which is
      true only of an appended requirement, and it costs one join newline on
      `after` alone. No EOF blank line is truly consumed — both files still end
      in a blank line.
      **THE STRONGEST READING, WHICH THIS SHAPE ALLOWS AND A MODIFIED BLOCK NEVER
      WOULD**: canon before is a strict byte PREFIX of canon after
      (`after.startswith(before)` → True), 139505 → 144975 bytes, the whole
      difference being the 5470-byte appended chunk. Nothing before that offset
      moved by one byte.
      **THE FAMILY VERIFIED ITS OWN PACKET, AND READ ZERO.** Run over this tree
      before the act, `--family modified-block-currency` drew **0 warning, 7
      info**, and not one of the seven names a path under this packet — the
      dogfooding D1's measurement predicted, and the reason § 3.4's figure needed
      no revision.
