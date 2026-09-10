# Tasks: amend-marker-declaring-nothing

Status: draft
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body.
**§ 1 (RATIFICATION) AND § 6 (ARCHIVE) STAY OPEN AND NAME WHY**: Brett Heap's
word of 2026-09-10, verbatim *"do the 860 856 batch, land each when green"*,
commissions this authoring and ratifies no wording — ratification, promotion and
archive are three later acts on three later words. **§ 7 STAYS UNTICKED**:
residue, measured and deliberately not taken.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFY THE TEXT.** No approval pair is declared in `.openspec.yaml`
      and none is implied. The word this packet is authored on —
      *"do the 860 856 batch, land each when green"* (2026-09-10, in session,
      recorded on openxFactory #856 and #860) — names a batch and a landing
      condition and decides no wording. On ratification: `proposal.md`,
      `design.md` and this file take `Status: ratified` with ONE citation line
      each (`Ratified:` in the proposal's front matter, `Ratified by:` here and
      in `design.md`), which is what `ratified-provenance` counts;
      `.openspec.yaml` gains `approved_by` and `approved_on` **BESIDE** the
      drafting provenance, `kind` and `id` unmoved, which is the
      addition-not-rewrite shape `add-drafted-proposal-origin` defined; and a
      `review/ratification-<date>.md` record is written carrying
      `Status: ratified` and one citation.
- [ ] 1.2 **RULE `design.md` D1 — openxFactory #860.** Option **A**
      (RECOMMENDED, and what the delta encodes): a `Removed from canon` marker
      whose tail carries no code span stays a MARKER and is REPORTED, as a fifth
      ground of the marker-defect class at `info`. Option **B** (the issue's own
      second option): a `document-lifecycle` GRAMMAR rule that such a paragraph
      is NOT of marker form — cheaper to encode and the LARGER semantic change,
      because the paragraph then becomes prose, becomes a carriage UNIT of the
      block and of canon after promotion, is read by the carriage arms, points
      its author at the block's completeness rather than at the empty
      declaration, and moves the rule to a capability that carries no reporting
      rule at all. **A VETO OF A IS A VETO OF GROUND FIVE ALONE** — ground four,
      its scenario, its test and its measurement are untouched, D1 and D2
      sharing no predicate, no field and no branch.
- [ ] 1.3 **RULE `design.md` D2 — openxFactory #856.** Option **A**
      (RECOMMENDED, and what the delta encodes): a name matching no unit of the
      requirement's basis and matching a unit THE BLOCK ITSELF ADDS is REPORTED,
      as a fourth ground at `info` — a block cannot declare removed from canon a
      unit canon never carried. Option **B** (the issue's own second option):
      rule the silence CORRECT and say so in canon in one sentence, so the next
      reader finds a decision rather than a gap — which ratifies a shape nobody
      has given a reading, is silent in the direction that hides (no row for the
      marker, none for the addition), costs the same amendment, and is the
      harder rule to retire. **A VETO OF A IS A VETO OF GROUND FOUR ALONE**, and
      the flipped test flips back to its ratified silence.
- [ ] 1.4 **NOTE `design.md` D3 AND AFTER, WHICH ARE NOT VETO POINTS BUT ARE
      DECISIONS.** D3 the band (`info`, the class's existing one; `warning`
      refused on this family's own "MEASURE FIRST, THEN FLIP" ruling of
      2026-08-27) and the `contested` row this packet claims no exemption from.
      D4 one template for five grounds, `TEMPLATE_MARKERS`' text UNMOVED so the
      `CLASS_MARKERS` probe places every new finding and `_ARM_TEMPLATES` stays
      at eight. D5 the self-reference hazard and this block's own marker. D6 the
      two exclusions ground five is written around — the PAIRING form (silence
      ruled correct 2026-09-09) and the `Merged into` form with an empty tail
      (residue, § 7.1). D7 why ONE packet for two issues. D8 why the realization
      rides this pull request.

## 2. The measurement, taken before the design

- [x] 2.1 **EVERY MARKER IN THE CORPUS, COUNTED BY FORM AND BY TAIL** —
      `openspec/specs/*/spec.md` and every active
      `openspec/changes/*/specs/*/spec.md`, read through `derive_units` so that
      fenced example markers are never offered, exactly as they are never
      offered to a run. Taken 2026-09-10 on `main` @ `e0638f11`: **26 markers,
      17 of the two unit-naming forms and 9 of the pairing form; ZERO of
      `Removed from canon` form with an empty tail, and ZERO of EITHER
      unit-naming form with an empty tail.** The tables are in `proposal.md`
      and in `design.md` D0. **THE SCOPE IS THE CORPUS AS IT STOOD BEFORE THIS
      PACKET**, said so wherever the figure appears: this block carries a marker
      of its own, excluded so that a reader re-deriving the figure on `main` @
      `e0638f11` gets exactly 26.
- [x] 2.2 **BOTH NEW GROUNDS HAVE A POPULATION OF ZERO TODAY.** The family reads
      markers only inside active `## MODIFIED Requirements` blocks; there are
      **THIRTY** such blocks on this tree and exactly **TWO** carry a
      unit-naming marker — `add-chain-attestation` and
      `add-composed-view-authoring`, both `Merged into`, one name each matching
      its resolved basis, neither quoting a code span in a reason and neither
      naming a unit its own block adds. Measured, not assumed: the branch's
      `doc-health` finding set is identical to `origin/main`'s apart from this
      packet's own rows, and **the marker-defect class raises NOTHING on either
      tree**.
- [x] 2.3 **THE ZEROS ARE ASSERTED AS A TEST, NOT ONLY AS A FIGURE** (§ 3.6):
      `test_no_marker_in_this_corpus_raises_either_ground_ADDED_HERE_today`,
      written as two CEILINGS rather than two exact counts so that an unrelated
      marker landing later is not read as a regression of these grounds, and
      saying of its ground-four half that it is STRICTLY WIDER than the ground
      (it does not resolve names against the promoted requirement).
- [x] 2.4 **THE SENTENCE IS PROMOTED IN ONE PLACE, CHECKED IN BOTH
      DIRECTIONS.** `document-lifecycle`'s marker grammar says how a deleted
      unit is NAMED and carries no reporting rule at all, so it needs no
      amendment and none is made — and amending it is exactly `design.md` D1's
      rejected alternative. `doc-health` is where the reporting rule lives, and
      the two retired sentences occur once each in it.
- [x] 2.5 **NO ACTIVE CHANGE CARRIES A `## MODIFIED` BLOCK FOR THIS
      REQUIREMENT.** Grepped over `openspec/changes/`: the three active changes
      that name it at all mention it in prose
      (`prepare-openspec-1-12-readiness/tasks.md`,
      `disposition-codexfactory-floor-relocation-retitle/design.md`,
      `disposition-codexfactory-declared-renames/design.md`) and carry no delta
      over it. Measured on the archive rather than recited: the requirement was
      PROMOTED by `add-modified-block-currency-check` (an `## ADDED` block) and
      exactly THREE archived changes carry a `## MODIFIED` block for it —
      `amend-marker-reason-boundary`, `amend-marker-defect-reporting` and
      `amend-modified-block-currency-standing`. No two-writers ordering is owed;
      `sequenced_after: []` is declared as an explicit root claim.
- [x] 2.6 **`kind: ad_hoc` IS CHECKED RATHER THAN ASSUMED.**
      `ideation/staging/` was enumerated and `INDEX.md` read on 2026-09-10: its
      33 topics carry no marker grammar, no marker-defect reporting and no
      doc-health carriage arm. The one `INDEX.md` line matching "marker" is the
      `xspec:candidate`/`xspec:supersedes` PROSE-TAGGING grammar — a different
      form in a different capability. `kind: staged` would claim a staging
      source that does not resolve.

## 3. The realization — two grounds, in this pull request

- [x] 3.1 `scripts/doc_health/modified_block_currency.py`: **GROUND FOUR IS THE
      `else` HALF OF A GUARD THAT ALREADY REPORTS.** `suppression`'s
      `if name not in block_texts:` becomes an if/else — the `if` still feeds
      `unmatched` (ground three) and the `else` feeds a new `block_added` list.
      The two are DISJOINT BY CONSTRUCTION, so a marker cannot be
      double-reported, and each names only the names that reached it, because
      those are the ones an author edits. **NO PARSE MOVES AND NO `Marker` FIELD
      IS ADDED.**
- [x] 3.2 **GROUND FIVE IS ONE PREDICATE OVER THREE FIELDS THE PARSER ALREADY
      DERIVES** — `marker.form == "removed" and not marker.names and not
      marker.quoted`. It is EXCLUSIVE of the other four by construction (every
      one of them is reached through `names` or `quoted`, and both are empty
      here), so a marker reported on it is reported ONCE, which the test asserts
      rather than the comment merely claiming.
- [x] 3.3 **THE ORDER IS FIXED AND WRITTEN DOWN**: ground one, then three, then
      four, then five, per marker, with ground two following in the second pass
      it has needed since `amend-marker-defect-reporting` — so a marker
      defective more than one way reports the same rows in the same sequence
      every run.
- [x] 3.4 **`TEMPLATE_MARKERS`' TEXT IS NOT EDITED AT ALL.** Both new clauses go
      into the `{why}` field the predecessor added, so `_ARM_TEMPLATES` stays at
      EIGHT, the existing `CLASS_MARKERS` probe places every new finding, the
      seventh class (`unplaced-finding drift`) stays silent, and ground one's
      rendered text is still byte-identical to the one this class shipped with.
      Ground five's clause is the module's first WHY with NO interpolation,
      which is correct rather than an omission: there is no name and no span to
      name.
- [x] 3.5 `_arm_marker_defects` and `_MARKER_ACTION` are UNCHANGED —
      the action already names the remedy for all five grounds, and a per-ground
      action would break `test_every_finding_carries_its_class_s_band_and_action`
      for no reader's benefit. `_LEDGER_SEVERITY` (`info`) is unchanged.
- [x] 3.6 `tests/doc-health/test_modified_block_currency.py`: **139 → 144**,
      five tests ADDED — a `Removed from canon` marker with no code span reports
      the marker and reports it ONCE; the PAIRING form with no code span stays
      SILENT; a `Merged into` marker whose tail names nothing stays SILENT
      (§ 7.1's pin); each ground added here matches exactly ONE arm template and
      classifies as `marker-defects`, with `_ARM_TEMPLATES` still at eight; and
      no marker in this corpus raises either ground today, as two ceilings.
- [x] 3.7 **ONE EXISTING ASSERTION IS FLIPPED RATHER THAN LOOSENED, AND NAMED
      HERE RATHER THAN LEFT IN THE DIFF.**
      `test_a_name_matching_a_unit_the_BLOCK_adds_stays_SILENT` asserted
      `findings == []` and was the pin `design.md` D3 of the predecessor put on
      the silence #856 reports. **ITS FIXTURE IS UNCHANGED** — the same canon
      unit, the same block addition, the same marker — and only the assertion
      and the name move, to
      `test_a_name_matching_a_unit_the_BLOCK_adds_reports_the_marker`, with the
      reason written where the assertion stands and a second half asserting that
      grounds three and four are disjoint rows. **ONE further existing test is
      RENAMED AND NOT OTHERWISE EDITED**:
      `test_a_well_formed_marker_is_silent_on_all_three_grounds` →
      `…_on_all_five_grounds`, no assertion and no fixture moved, because a
      title claiming three grounds would tell the next reader the class had
      three. **No other existing test is edited.**
- [x] 3.8 **EVERY COMMENT DESCRIBING THE RETIRED RULE IS CORRECTED**, on
      `amend-marker-reason-boundary` § 3.3's own rule that a comment describing a
      retired rule will mislead the next reader: the module header's arm-list
      item 4 (THREE GROUNDS → FIVE, each spelled out), `TEMPLATE_MARKERS`' own
      comment, the `_WHY_*` block's heading comment, `_MarkerDefect`'s docstring,
      `suppression`'s docstring (both the third resolution's retired silence and
      a new paragraph for ground five), the per-marker order comment, and
      `_arm_marker_defects`' docstring.

## 4. The delta

- [x] 4.1 **ONE `## MODIFIED` REQUIREMENT, WRITTEN OVER CANON**, byte-faithful
      by CONSTRUCTION rather than by transcription: the block was GENERATED by
      slicing `openspec/specs/doc-health/spec.md` lines **1588–1985** and
      **2018–2113** and applying each replacement as an exact single-occurrence
      substitution (the script REFUSES on any other count), then re-wrapping ONLY
      the one paragraph the substitutions touched — which canon itself makes
      unit-identical, *"a re-wrapped paragraph compares equal to the same
      paragraph wrapped differently"*. Verified after the fact by the family's
      own derivation: **154 canon units, 2 uncarried, both named by the marker
      and suppressed, 0 marker defects, 19 of 19 promoted scenario titles
      carried, 0 missing.**
- [x] 4.2 **TWO UNITS RETIRED AND REPLACED IN PLACE**: the sentence stating
      THREE grounds and enumerating them, and the sentence counting them. Each
      is REPLACED, neither is dropped. **TWO SENTENCES ARE ADDED BESIDE THEM** in
      the same paragraph, one scoping each new ground — ground four changes no
      suppression and does not report the block's own addition; ground five is
      read on the `Removed from canon` form ALONE, the pairing form's silence
      staying ruled correct and the `Merged into` empty tail staying undecided.
- [x] 4.3 **ONE `Removed from canon` MARKER, TWO NAMES, NO CODE SPAN IN ITS
      REASON — AND THE MARKER IS ASSEMBLED FROM `derive_units`' OWN OUTPUT
      RATHER THAN RETYPED**, so it cannot name a fragment or a unit as its
      author remembers it. The first name contains a backtick (`` `info` ``) and
      is fenced with a LONGER run, exactly as canon's own rule requires; the
      second contains none. The assembled marker is then re-parsed by
      `parse_marker` and asserted to yield exactly those two names and an empty
      `quoted`, which is why ground two has nothing to resolve over it.
- [x] 4.4 **THE SELF-REFERENCE HAZARD IS DISCHARGED** (`design.md` D5).
      `amend-modified-block-currency-standing`'s promoted `Removed from canon`
      marker is **deliberately NOT restated**, on this requirement's own rule
      that a marker is not a carriage unit in either direction: its five named
      units are sentences canon no longer carries, so restating it would make
      this block report ITSELF under ground three. The `AMENDED BY` note says so
      in terms.
- [x] 4.5 An `**AMENDED BY …**` note in the precedents' style records the whole
      accounting: that every paragraph and every scenario above it stands
      exactly as promoted, that the only promoted text changed is two sentences
      of one paragraph, that two sentences and two scenarios are added, that no
      severity, threshold, arm, parse, grammar or resolution row moves, the
      measured population of both grounds, and why the predecessor's marker is
      absent.
- [x] 4.6 **TWO SCENARIOS ARE ADDED AT THE END OF THE BLOCK, ONE PER GROUND.**
      *A marker names a unit the block itself adds* and *A marker of removal
      form declares nothing at all*, the second carrying the pairing-form
      exclusion in its own bullet. Without them the two grounds would promote
      with nothing exercising them and would be pinned only by this packet's
      tests — running code standing in for canon, the exact shape `proposal.md`
      § *Why this is NOT a plain fix* refuses. No promoted scenario moves, is
      retitled or loses a bullet. The block ADDS two scenario titles, so
      `suppression`'s `adds_new_title` gate withholds the scenario-title bullet
      cascade — which has nothing to withhold here, this packet's marker naming
      BODY units only.
- [x] 4.7 **README `## OpenSpec Records` CARRIES THE ACTIVE ROW**, in house
      style, naming the draft standing, both origin issues, both veto points and
      the zero population.
- [ ] 4.8 **THE PER-CHANGE SWEEP LEDGER ROW IS SEEDED BY THE SANCTIONED TOOL**,
      never hand-written — and it is OWED UNTIL THE PULL REQUEST EXISTS, the
      tool stamping `moved_by` with a number this commit cannot know:
      `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#<PR>'`, in the commit that follows the opening
      of the draft pull request. ONE row is added,
      `amend-marker-declaring-nothing: {state: active, class: co-modifier,
      declares: [], depth: 0, prose: false}`, and NO other row's provenance
      moves: the change classes `co-modifier` on ARCHIVED partners only (the
      three archived changes carrying a `## MODIFIED` block for this
      requirement), so no partner flips and no MOVEMENT LOG entry is owed.

## 5. Verification — DONE IN THIS PULL REQUEST

- [x] 5.1 `OPENSPEC_TELEMETRY=0 openspec validate amend-marker-declaring-nothing
      --strict` — **exit 0**, *"Change 'amend-marker-declaring-nothing' is
      valid"*.
- [x] 5.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **exit 1**,
      `Totals: 97 passed, 4 failed (101 items)`, and **the failure set is
      byte-identical to `origin/main`'s** (`e0638f11`: `Totals: 96 passed, 4
      failed (100 items)`): `change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle`,
      `spec/neutral-product-pin`, `spec/repo-boundary-governance`. This change
      appears in NEITHER set; the item count moves by exactly one, which is this
      change passing.
- [x] 5.3 **THROUGH THE PINNED CLI, WHICH IS THE ONE THE GATE RUNS.** The
      `openspec` on PATH is **1.2.0** and the pin is **1.12.0**, so both were
      run: `python3 scripts/validate-openspec-cli-pin.py --change
      amend-marker-declaring-nothing --no-cache` — **exit 0**, `Totals: 1
      passed, 0 failed (1 items)`, artifact integrity verified; and the gate's
      literal `python3 scripts/validate-openspec-cli-pin.py --all --no-cache` —
      **exit 0**, *"every target validated --strict with 0 UNDISPOSITIONED
      failures"*, with the two PRE-EXISTING accepted exceptions
      (`add-chain-attestation`, `add-composed-view-authoring`) named in the
      output and neither of them this change. **THIS BLOCK OMITS NO SCENARIO AND
      RETITLES NONE**, so it adds no 1.12 finding of its own.
- [x] 5.4 `python3 scripts/proposal-support.py . verify
      amend-marker-declaring-nothing` — **exit 0**, *"proposal support
      verification ok"*.
- [x] 5.5 `python3 scripts/validate-sequenced-after.py .` — **exit 0**,
      *"sequenced_after validation passed (39 active changes, 9 declaring the
      field)"*, both archive-date arms passing. `--ledger-diff` reports the
      ledger STALE by exactly ONE missing row — this change's own — until § 4.8
      seeds it, which is the tool's own instruction and not a defect; the run
      after the seed is recorded here.
- [x] 5.6 `python3 scripts/validate-scope-globs.py .` — **exit 0**,
      *"scope_globs validation passed (all active changes conform)"*.
- [x] 5.7 `python3 scripts/doc-health.py --single-repo .` — **exit 0**. The
      finding set is IDENTICAL to `origin/main`'s except for this packet's own
      rows, and **the modified-block-currency family reports NOTHING on this
      block**: the arm that would catch a stale restatement is the one this
      packet is written under, and it is silent because the block carries canon
      and declares its two removals. The marker-defect class — including both
      grounds this packet adds — raises ZERO findings on the whole corpus, before
      and after.
- [x] 5.8 `python3 -m pytest tests/doc-health tests/sequenced_after
      tests/scope_globs tests/proposal-support -q` — **2173 collected**;
      `tests/doc-health` goes **1684 → 1689** (collected on this tree and on
      `origin/main` in the same shell) and
      `tests/doc-health/test_modified_block_currency.py` **139 → 144**. Before
      the ledger seed of § 4.8 the run is `4 failed, 2169 passed`, and ALL FOUR
      are the same fact stated four ways —
      `tests/sequenced_after/test_sweep.py`'s row-by-row, one-row-per-change and
      two totals assertions, each reporting the ONE row this change has not yet
      added. The seed is what turns them green, and the run after it is recorded
      here.

## 6. Archive — OWED, NOT GIVEN

- [ ] 6.1 **ARCHIVE ON REALIZATION EVIDENCE, ON A SEPARATE WORD.**
      `code_surface` is non-empty, so under `release-realization` this packet
      archives on **merged-plus-green realization evidence rather than on
      landing**: this pull request merged into `main`, and a green `pytest-suite`
      run ON that merge commit. Performed with
      `python3 scripts/proposal-support.py . archive
      amend-marker-declaring-nothing --date <YYYY-MM-DD> --yes` through the
      pinned CLI, never a bare `openspec archive`, which moves the packet to
      `openspec/changes/archive/<date>-amend-marker-declaring-nothing/` and
      writes the `## MODIFIED` block back into
      `openspec/specs/doc-health/spec.md`.
- [ ] 6.2 **CLOSE openxFactory #856 AND #860 AT THE ARCHIVE**, not at this
      landing. This pull request's body carries `refs #856` and `refs #860` and
      **no closing keyword**, and its `closingIssuesReferences` is verified
      through GraphQL to be exactly `[]` for exactly that reason. The archive
      pull request is where `Closes #856` and `Closes #860` belong.

## 7. Measured, and deliberately NOT taken here

- [ ] 7.1 **A `Merged into` MARKER WHOSE TAIL NAMES NO SUPERSEDED TITLE IS
      STILL SILENT** (`design.md` D6). Such a marker parses with `names = []`
      and `quoted = []` exactly as ground five's shape does, but its
      DESTINATION stands in the prefix, where that form's declaration has always
      been read — so whether it declares nothing, or declares a destination that
      absorbed nothing named here, is a question nobody has ruled. openxFactory
      #860 scopes itself to the `Removed from canon` form, and inventing a sixth
      ground here would repeat, on the day after, the fault the predecessor
      packet exists to correct. Population ZERO, measured with the rest. Pinned
      by `test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT` so the
      silence is a decision a later act can overturn rather than a gap it has to
      rediscover, and a successor is named at the archive word.
- [ ] 7.2 **THE ESTATE-WIDE RUN IS OWED AT LANDING, NOT TAKEN HERE.**
      `active_blocks()` takes a repository root and the aggregation's nightly run
      reads every submodule, so a marker in a sibling repository naming a unit
      its own block adds, or of removal form with an empty tail, would surface as
      new advisory findings there. The measurement in this packet covers
      openxFactory only, this lane being confined to its own clone. The direction
      is bounded by construction — both grounds REPORT and suppress nothing, so
      no suppression changes and no unit becomes less visible — and both are
      `info`, so no `--fail-on error` run can red on them. What is owed is the
      estate-wide run recorded on the pull request or here, so the first nightly
      does not hand another lane findings nobody attributes. Its two sibling
      sweeps — openxFactory
      [#731](https://github.com/opensoft/openxFactory/issues/731) (the
      `amend-marker-reason-boundary` narrowing) and
      [#859](https://github.com/opensoft/openxFactory/issues/859) (the two
      grounds `amend-marker-defect-reporting` added) — are BOTH CLOSED, checked
      rather than assumed at this authoring, so this run has no open sibling to
      be folded into and is owed on its own.
- [ ] 7.3 **`specs/019-modified-block-currency-family/` IS NOT EDITED BY THIS
      PACKET.** FR-018 was restated to canon's THREE grounds by PR #887 (issue
      #858) this morning and now describes a rule this packet amends. The Speckit
      feature spec for this module is a BUILD RECORD pinned by no test and by no
      gate, both precedents edited no feature spec when they amended the canon
      those specs describe, and the remedy shape — a restatement with a dated
      amendment note beside it, as PR #827 and PR #887 both used — is available
      to a later act. Recorded as residue so a later reader does not read the
      omission as an oversight; a successor is named at the archive word.
- [ ] 7.4 **THE PER-CLASS GRAIN OF THE UNCITED-RESOLUTION RULE IS NOT WIDENED.**
      `report.uncited_resolutions` keys on `(family, repository, path)` and skips
      a prior contested key whenever ANY current finding carries it, so a
      marker-defect finding that stops being reported while another finding of
      this family is still emitted at that path owes no citation. That is the
      shipped behaviour, promoted canon states it, and the two grounds added here
      inherit it unchanged. Whether the checker SHOULD track disappearance at
      finding-class grain is openxFactory
      [#893](https://github.com/opensoft/openxFactory/issues/893), filed by
      `amend-modified-block-currency-standing` at its own archive, and it is that
      issue's work rather than this packet's.
