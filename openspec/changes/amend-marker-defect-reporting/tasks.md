# Tasks: amend-marker-defect-reporting

Status: draft
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body.
**§ 1 IS NOT TICKED AND NAMES WHY**: ratification has not happened.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFICATION IS OWED AND NOTHING HERE PERFORMS IT.** Brett Heap's
      *"author the 729 packet"* (2026-09-09, recorded on openxFactory issue
      **#729**) instructs a lane to AUTHOR the remedy. It decides no wording,
      takes no design decision, and is recorded as the ORIGIN in `proposal.md`
      front matter and in `.openspec.yaml` — which carries drafting provenance
      ONLY, with no `approved_by` and no `approved_on`, the lawful unapproved
      shape `add-drafted-proposal-origin` defined. Every document in this packet
      carries `Status: draft`. When a word is given, this box is ticked with the
      verbatim utterance, ONE citation line is added to each document's front
      matter, the approval pair is ADDED beside the drafting provenance (`kind`
      and `id` never move), and the record is written to
      `review/ratification-<date>.md`.
- [ ] 1.2 **THE VETO POINT IS `design.md` D1** — option **A** (report a marker
      only where a code span inside its reason EXACTLY MATCHES a unit of the
      basis the block does not carry) against option **B** (report any code span
      inside any reason, which is issue #729's own wording). A is designed and
      encoded; B is written out beside it with four costs, the first being that
      it fires on canon's own blessed form in **EIGHT of this corpus's SIXTEEN**
      unit-naming markers, every one of them promoted, and grows with the corpus.
      **A veto of A is a veto of the delta's second ground**; the third ground
      survives either ruling, and `design.md` D1 records ground 3 alone as the
      strictly smaller packet if that is what is wanted.
- [ ] 1.3 **THE OWN-CHANGE SCOPE IS A SECOND DECISION AND IT IS PUT, NOT
      ASSUMED** (`design.md` D2). Grounds 2 and 3 are read only against a marker
      the block's own change declares. It is not offered as a veto point because
      without it this packet's OWN block reports itself — measured — but it is a
      designed limit with a stated prospective cost, and a ruling may widen it.

## 2. The measurement, taken before the design

- [x] 2.1 **EVERY UNIT-NAMING MARKER IN THE CORPUS, RE-DERIVED ON THIS BRANCH**
      at `main` `245ee85a` on 2026-09-09 — `openspec/specs/*/spec.md` and every
      active `openspec/changes/*/specs/*/spec.md`, read through `derive_units` so
      that fenced example markers are never offered, exactly as they are never
      offered to a run. **115 files, 18,394 derived units; SIXTEEN unit-naming
      markers; EIGHT quoting a code span inside their reason; ZERO reason-quoted
      spans that are a derived unit of the document carrying them.** The eight
      are tabled by marker in `proposal.md` and `design.md` D0. This re-derives
      the STOP measurement recorded on issue #729 exactly (16 / 8 / 0) on a tree
      that has since moved.
- [x] 2.2 **THE WORDING ISSUE #729 PROPOSED IS THE PREDICATE FOR CANON'S BLESSED
      FORM, AND THE MEASUREMENT IS WHAT SAYS SO.** *"Carries a code span INSIDE
      its reason"* describes 8 of 16 markers today, every one promoted, five of
      them written by one archived change; the share was 2 of 7 on 2026-09-06.
      The narrow predicate replaces it and is silent on all eight, measured.
- [x] 2.3 **THE SHIPPING PATH: 31 ACTIVE MODIFIED BLOCKS (23 resolved, 8
      pending, 0 unresolved) CARRY EXACTLY TWO UNIT-NAMING MARKERS**, both
      `Merged into`, both naming one unit that matches their resolved basis,
      neither with a reason quoting a code span. **Both new grounds report ZERO
      today** — pinned as a test (§ 3.5), not only measured.
- [x] 2.4 **THE COUNTERFACTUAL FOR THE OWN-CHANGE SCOPE, MEASURED ON THIS
      PACKET'S OWN BLOCK.** With the scope removed, ground 3 reports THIS block:
      it carries `amend-marker-reason-boundary`'s promoted marker verbatim, whose
      named unit left canon when that marker was promoted. One finding, naming
      the sentence #719 retired. That is why `design.md` D2 exists and why it is
      canon in the delta rather than a code comment.
- [x] 2.5 **NO ACTIVE CHANGE CARRIES A `## MODIFIED` BLOCK FOR THIS
      REQUIREMENT.** Grepped over `openspec/changes/` on the tree this packet is
      authored on. No two-writers ordering is owed and `sequenced_after` is
      elective, undeclared — `python3 scripts/validate-sequenced-after.py .`
      passes with 43 active changes, 10 declaring.
- [x] 2.6 **THE REPORTING RULE IS PROMOTED IN ONE PLACE, CHECKED.**
      `document-lifecycle`'s marker grammar names each deleted unit as a code
      span and says nothing about when a marker is reported, so it needs no
      amendment and none is made.

## 3. The realization — one added reading, in this pull request

- [x] 3.1 `scripts/doc_health/modified_block_currency.py`: `Marker` gains a
      `quoted` field — the code spans standing AFTER the reason boundary,
      normalized, in order — populated by `parse_marker`, which derived them and
      DISCARDED them. `names` and `reason` are unchanged; a LAST parameter with a
      default, on the rule `Marker.basis` was added under, so every existing
      positional construction still reads. Empty for the pairing form, whose
      WHOLE tail is reason, with the reason stated in the field's own comment.
- [x] 3.2 `_declares_nothing` added as a module-level helper: the block's OWN
      unit-naming markers, read against the basis, returning `(marker, why)` for
      a reason-quoted span matching a unit the block does not carry and for a
      name matching no unit of the basis and none of the block's own. **PRIVATE
      ON PURPOSE** — `test_this_feature_touches_no_production_module` snapshots
      the module's public callables, and a reading that adds no public callable
      keeps that guard meaningful for the next name that does. It carries the
      two carves (a span the marker also names; a span matching a unit the block
      DOES carry) and the own-change scope, each with its measurement.
- [x] 3.3 `suppression` IS NOT TOUCHED — same signature, same return, same
      behaviour, nothing new suppressed and nothing newly unsuppressed. Only its
      docstring's account of the third resolution moves, because *"deliberately
      NOT a finding … Recorded as a plausible later ruling"* becomes false the
      moment the ruling is taken. A comment describing a retired rule is a
      comment that will mislead the next reader.
- [x] 3.4 ONE new arm template `TEMPLATE_MARKER_VOID` (`_ARM_TEMPLATES` 8 → 9),
      reusing `TEMPLATE_MARKERS`' opening so `CLASS_MARKERS`' existing class
      pattern places both grounds and the seventh class (`unplaced-finding
      drift`) stays silent — verified, `_shape` returns
      `template:marker-declares-nothing` and `classify` returns
      `marker-defects` for both. `_arm_marker_defects` gains a LAST parameter
      with a default and renders them. **NO CLASS, NO BAND AND NO ACTION MOVES**:
      `_LEDGER_SEVERITY` (`info`) and `_MARKER_ACTION`, which is a per-CLASS
      constant a standing test compares against, so the predicate lives in the
      rule text and nowhere else (`design.md` D3).
- [x] 3.5 `tests/doc-health/test_modified_block_currency.py`: **TEN TESTS ADDED**
      (128 → 138) — the spans are kept and the names unchanged (all three marker
      forms); ground 2 fires and suppresses nothing; ground 3 fires and the sound
      name still suppresses; a well-formed marker is silent and so is the eight
      promoted markers' shape; a reason quoting a unit the block DOES carry is
      silent WITH its positive control; a span the marker also names is not
      reported twice; the own-change scope with its counterfactual in the same
      test; one class, one band, one action, one template over the whole
      registry; **and D0 AS A TEST** — both grounds report nothing over every
      resolved block in this repository, non-vacuous in both directions (at
      least two blocks with an own marker, at least one with an inherited one).
- [x] 3.6 **ONE NEW FIXTURE TREE** `tests/doc-health/fixtures/modified-block-currency-void/`
      — five requirements, one per case, with a `README.md` on the corpus's own
      `SYNTHESIZED`-on-line-3 convention: the two grounds fire (3 findings, the
      third being the carriage row that stands BESIDE the ground-2 report), and
      the three negative controls are silent, each one fact away from a positive.
      A tree is needed because `test_every_finding_matches_exactly_one_arm_template`
      requires every REGISTERED template to be exercised over the corpus and the
      real tree raises zero; `ALL_TREES` is derived by glob, so the tree joins the
      catalogue-wide partition, determinism and band sweeps by being there.
- [x] 3.7 **FOUR EXISTING ASSERTIONS EDITED, EACH BECAUSE IT BECAME LITERALLY
      FALSE, EACH NAMED HERE AND IN THE PULL REQUEST BODY.** Three are
      bookkeeping a ninth template forces, in
      `tests/doc-health/test_modified_block_currency_reporting.py`:
      (a) `len(_ARM_TEMPLATES) == 8` → `9`, twice, with the pairing class's
      one-template-per-remedy argument extended rather than replaced;
      (b) the INDEPENDENT probe table's `markers` key, `" marker by "` →
      `", which the block still restates"`, because two templates now share that
      opening BY DESIGN and a probe matching two makes
      `_independent_template_of` assert against itself; a `void` key is added
      beside it; (c) the label map in the exclusivity sweep gains its row.
      **THE FOURTH IS A DELIBERATE BEHAVIOUR CHANGE AND IS NOT BOOKKEEPING**:
      `test_the_inner_backtick_does_not_truncate_the_named_unit`
      (`…_fixtures.py`) asserted that a marker naming a FRAGMENT — the
      `-fence` tree's single-backtick mis-fence — emits NO marker defect, which
      was ground 3's silence pinned as a fact. It now emits one, naming both
      fragments. **The assertion is INVERTED rather than deleted**, its docstring
      records the change and the ruling that made it, and the tree's `README.md`
      is corrected with it. **This is the amendment working on a case the corpus
      already had**: an author who mis-fences a backtick-carrying unit is now
      told, instead of being handed a carriage row naming the clause and nothing
      naming the declaration. No other existing test is edited.
- [x] 3.8 **THE WHOLE SUITE, GREEN.** `python3 -m pytest tests/doc-health -q`
      **1635 → 1645** passed, 0 failed (the ten of § 3.5 plus § 3.6's tree test).

## 4. The delta

- [x] 4.1 `specs/doc-health/spec.md` restates *Currency of an active change's
      MODIFIED requirement blocks* IN FULL — **122 canon units: 59 body units,
      16 scenario titles, 47 scenario bullets**, byte-faithful, including the
      fenced block that writes the two marker forms out, the `AMENDED BY` note
      **#719** promoted and the `Removed from canon by
      amend-marker-reason-boundary (2026-09-06)` marker promoted with it — with
      ONE body sentence replaced. Measured through the family's own readers: 121
      carried, ONE uncarried, and that one named by the marker below.
- [x] 4.2 The retired unit is declared by the reserved marker
      `**Removed from canon by amend-marker-defect-reporting (2026-09-09):**`,
      naming it verbatim as a single-backtick code span — the sentence contains
      no backtick, so canon's longer-fence rule does not apply, which
      `design.md` D5 says out loud because the sibling amendment needed a
      DOUBLED run.
- [x] 4.3 **THE SELF-REFERENCE HAZARD IS DISCHARGED TWICE** (`design.md` D4).
      The marker's reason quotes NO code span anywhere, so it derives exactly one
      name and no quoted span under the grammar on `main` and under this
      branch's alike (verified: `names=1`, `quoted=[]`, reason non-empty) — a
      constraint this packet's own ground 2 now makes MANDATORY for every
      amendment marker. And the block carries a PREDECESSOR'S marker, which is
      § 2.4's counterfactual.
- [x] 4.4 An `**AMENDED BY …**` note in the precedents' style records that every
      paragraph, note, marker and scenario above it stands exactly as promoted,
      that the only change to promoted text is the one sentence, that the
      promoted scenario *A marker's reason quotes a code span* is carried WHOLE —
      its third `AND` included, so the units a reason-quoted span would have
      named stay subject to the carriage arms and the report is added BESIDE that
      carriage — and that two scenarios are added.
- [x] 4.5 **TWO SCENARIOS ARE ADDED AT THE END OF THE BLOCK, ONE PER GROUND** —
      *A marker's reason quotes a unit the block does not carry* and *A marker
      names something no unit matches*. Without them the new normative rules
      would promote with no scenario exercising them and be pinned only by this
      packet's tests — running code standing in for canon, the exact shape
      `proposal.md` § *Why this is NOT a plain fix* refuses, and the shape the
      origin packet's own § 5.1 named ("with its own scenarios to write"). Each
      carries its carves and the own-change scope as bullets, so the limits are
      canon and not commentary. No promoted scenario moves, is retitled or loses
      a bullet.
- [x] 4.6 **THE BLOCK RAISES ZERO FINDINGS FROM ITS OWN FAMILY, MEASURED, AND
      THE MEASUREMENT IS FALSIFIABLE.** `--family modified-block-currency` is
      byte-identical between an OUTSIDE `main` worktree and this branch once the
      repository-identity line is normalized (9 `info`, 0 new, the report never
      names this change), and so is the full `--single-repo .` run. Two mutation
      probes prove the run is looking: remove the marker and the dropped unit is
      reported (`info`, 1 of 106); retitle one promoted scenario and the
      gate-bearing arm reports `error` (omits 1 of the 16 scenarios). Both
      restored byte-identical.
- [x] 4.7 **OPENSPEC STRICT, THROUGH THE PINNED CLI.**
      `python3 scripts/validate-openspec-cli-pin.py --change
      amend-marker-defect-reporting --strict --no-cache` → 1 passed, 0 failed;
      `--all --no-cache` → exit 0 with **0 undispositioned failures** (the two
      accepted exceptions belong to `add-chain-attestation` and
      `add-composed-view-authoring` and are unchanged by this packet).
      `validate-scope-globs.py .` passes.

## 5. Owed, and deliberately not taken here

- [ ] 5.1 **A MARKER A BLOCK CARRIES BUT DID NOT WRITE IS NOT REPORTED ON EITHER
      NEW GROUND**, and the limit is designed (`design.md` D2) rather than
      overlooked. Its prospective cost is stated: a block carrying a
      predecessor's marker whose reason quotes a unit the block dropped is
      silent, and the unit is reported by the carriage arms instead. Widening it
      would need a rule for distinguishing an inherited marker's stale name from
      a defective one, which needs history the family does not read. Recorded as
      available to a later ruling and not proposed.
- [ ] 5.2 **NO PROMOTED MARKER IS EDITED, AND NEITHER ARE THE ARCHIVED DELTAS
      THAT CARRY THEM.** They are records of ratified removals. Nothing is owed
      here; it is recorded so a later reader does not read the omission as an
      oversight.
- [ ] 5.3 **`specs/019-modified-block-currency-family/spec.md` STILL DESCRIBES
      ONE REPORTING CASE FOR A MARKER, AND IS DELIBERATELY NOT EDITED.** It is a
      BUILD RECORD of what `add-modified-block-currency-check` specified and was
      implemented against — not promoted canon, pinned by no test and by no gate
      — and precedents `amend-unreadable-read-sibling-scenarios` (#688) and
      `amend-marker-reason-boundary` (#719 § 5.3) likewise edited no feature spec
      when they amended the canon those specs describe. Recorded as residue; a
      superseding note there is available to a later act and is not this
      packet's.
- [ ] 5.4 **THE ESTATE-WIDE RUN IS OWED AT LANDING, NOT TAKEN HERE.**
      `active_blocks()` takes a repository root and the aggregation's nightly run
      reads every submodule, so a sibling repository whose block carries a marker
      naming something no unit matches would surface as new advisory findings
      there. The measurement in this packet covers openxFactory only, this lane
      being confined to its own clone. The direction is safe by construction —
      nothing new is SUPPRESSED, so no unit can become less visible, and both
      grounds are `info`, so no `--fail-on error` run can red on them. What is
      owed is the estate-wide run recorded on the pull request or here, so the
      first nightly does not hand another lane findings nobody attributes.
- [ ] 5.5 **ARCHIVE.** `code_surface` is non-empty, so under
      `release-realization` this packet archives on merged-plus-green realization
      evidence rather than on landing, and on a separate word.
