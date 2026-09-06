# Tasks: amend-marker-reason-boundary

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
      *"do 3 and 4"* admits openxFactory issue **#692** to work and instructs a
      lane to author a remedy. It decides no wording, takes no design decision,
      and is recorded as the ORIGIN in `proposal.md` front matter and in
      `.openspec.yaml` — which carries drafting provenance ONLY, with no
      `approved_by` and no `approved_on`, the lawful unapproved shape
      `add-drafted-proposal-origin` defined. Every document in this packet
      carries `Status: draft`. When a word is given, this box is ticked with the
      verbatim utterance, ONE citation line is added to each document's front
      matter, the approval pair is ADDED beside the drafting provenance
      (`kind` and `id` never move), and the record is written to
      `review/ratification-<date>.md`.
- [ ] 1.2 **THE VETO POINT IS `design.md` D1** — option **A** (the reason begins
      at the first separator standing outside every code span) against option
      **B** (require the removed units in a fenced list). A is designed and
      encoded; B is written out beside it with four costs, the first being that
      it rewrites every existing marker including those inside
      `openspec/changes/archive/`, which are records of ratified acts. **A veto
      of A is a veto of this delta's one sentence**, and the packet does not
      land on it.

## 2. The measurement, taken before the design

- [x] 2.1 **EVERY UNIT-NAMING MARKER IN THE CORPUS, PARSED UNDER BOTH RULES** —
      `openspec/specs/*/spec.md` and every active
      `openspec/changes/*/specs/*/spec.md`, read through `derive_units` so that
      fenced example markers are never offered, exactly as they are never
      offered to a run. **SEVEN markers; TWO change (3 names → 1, reason `None`
      → the author's text); FIVE are unaffected.** The table is in
      `proposal.md` and in `design.md` D0. **THE SCOPE IS THE CORPUS AS IT STOOD
      BEFORE THIS PACKET**, said so wherever the figure appears: this packet's
      own delta carries an EIGHTH unit-naming marker, so the same walk over the
      branch returns eight. The eighth is § 4.3's self-reference case, identical
      under both rules by construction, and it is excluded from the figures so
      that a reader re-deriving them on the tree the design was taken on gets
      exactly seven.
- [x] 2.2 **WHY IT IS INERT: 17,566 derived units, NONE literally `WHEN` or
      `AND`.** `suppression`'s third resolution — a name matching no canon unit
      suppresses nothing and reports nothing — has been absorbing the defect by
      luck. Same scope as § 2.1 — 108 files, the corpus BEFORE this packet; with
      this packet's delta the walk is 109 files and more units, and NONE of
      those is literally `WHEN` or `AND` either, so the claim holds on both
      readings and only the figure is scoped.
- [x] 2.3 **NO MARKER IN THIS CORPUS SEPARATES ITS NAMES WITH ` — `.** All
      seven separate names with `; ` and use ` — ` once, to open the reason. This
      is what makes option A's conservative failure direction EMPTY on the
      present corpus rather than merely tolerable, and it is asserted as a test
      (§ 3.4) rather than only measured.
- [x] 2.4 **THE SENTENCE IS PROMOTED IN ONE PLACE, CHECKED IN BOTH DIRECTIONS.**
      `document-lifecycle`'s marker grammar names each deleted unit as a code
      span and says nothing about the reason boundary, so it needs no amendment
      and none is made. TWO THINGS ARE NAMED RATHER THAN LEFT IMPLIED. FIRST,
      what `document-lifecycle` DOES say — *"naming each deleted unit as a
      CommonMark code span"* — was true of every span under the retired rule and
      is true only of the spans before the boundary under the amended one; that
      narrowing is disclosed in `proposal.md` and its reporting is scoped into
      § 5.1. SECOND, the sentence also appears in a NON-GOVERNING feature record
      (§ 5.3), which is a build artifact rather than promoted canon and is
      deliberately not edited.
- [x] 2.5 **NO ACTIVE CHANGE CARRIES A `## MODIFIED` BLOCK FOR THIS
      REQUIREMENT.** Grepped over `openspec/changes/`: the two active changes
      that name it at all mention it in prose
      (`disposition-codexfactory-declared-renames/design.md`,
      `prepare-openspec-1.12-readiness/tasks.md`) and carry no delta over it. No
      two-writers ordering is owed and `sequenced_after` is elective, undeclared.

## 3. The realization — one split, in this pull request

- [x] 3.1 `scripts/doc_health/modified_block_currency.py`: `_reason_boundary`
      added as a module-level helper — the offset of the first ` — ` standing
      outside every code span, or `None` — with the amended requirement quoted
      above it and the retired rule named, so the next reader knows which
      sentence the code conforms to. **PRIVATE ON PURPOSE**: the module's public
      callables are snapshotted by
      `test_modified_block_currency_fixtures.py::test_this_feature_touches_no_production_module`,
      and a helper that is one split inside `parse_marker` adds no public
      reading, so that guard stays meaningful for the next name that does and is
      NOT edited by this packet.
- [x] 3.2 `parse_marker`: the unit-naming tail is split at that boundary. Names
      are the spans that close at or before the cut; the reason is what follows
      it; where no boundary stands, every span names a unit and the reason is
      `None` — the `Merged into` example's form, unchanged.
- [x] 3.3 The pairing branch's comment, which justified taking the WHOLE tail by
      contrast with the retired *"after the LAST code span"* rule, is corrected
      to the amended rule, and the branch's separator literal and its hardcoded
      `[3:]` are replaced by `_REASON_SEP` and `len(_REASON_SEP)` so one grammar
      token has ONE spelling in the function. The BEHAVIOUR of that branch is
      untouched, which the file's existing pairing tests hold.
- [x] 3.4 `tests/doc-health/test_modified_block_currency.py`: **121 → 128**,
      seven tests added and none edited — a reason quoting code spans names only
      the spans before the separator; a separator inside a code span is a unit's
      own bytes; a marker with no separator still names every span; names
      separated by ` — ` fail in the CONSERVATIVE direction and suppress nothing;
      **A REASON QUOTING A REAL CANON UNIT IS SUPPRESSED UNDER THE RETIRED RULE
      AND NOT UNDER THE AMENDED ONE**, asserted at `suppression` level because
      that is where the defect's harm lands rather than at parse level where it
      merely shows; the whole corpus loses no name any author meant to declare;
      and the two promoted markers, located BY CONTENT rather than by line
      number, parse to exactly one name each with a non-`None` reason. The
      corpus test's unit set is a PROXY for the promoted requirement's units and
      its docstring says so.

## 4. The delta

- [x] 4.1 `specs/doc-health/spec.md` restates *Currency of an active change's
      MODIFIED requirement blocks* IN FULL — 50 body units, 14 scenario titles,
      40 scenario bullets, byte-faithful, including the fenced block that writes
      the two marker forms out — with ONE body sentence replaced.
- [x] 4.2 The retired unit is declared by the reserved marker
      `**Removed from canon by amend-marker-reason-boundary (2026-09-06):**`,
      naming it verbatim as a code span fenced with a DOUBLED backtick run,
      because the unit cites ` — ` and so contains backticks (`design.md` D5).
- [x] 4.3 **THE SELF-REFERENCE HAZARD IS DISCHARGED** (`design.md` D4): this
      marker is read by the RETIRED grammar on `main` and by the AMENDED grammar
      here, so its reason is written with NO code span anywhere in it and both
      grammars derive exactly one name and the same reason. Verified under both
      parsers, and the verification is in the pull request body.
- [x] 4.4 An `**AMENDED BY …**` note in the precedents' style records that every
      paragraph and every scenario above it stands exactly as promoted, that the
      only change to promoted text is the one sentence, and that two scenarios
      are added.
- [x] 4.5 **TWO SCENARIOS ARE ADDED AT THE END OF THE BLOCK, PINNING THE
      AMENDED SENTENCE IN CANON.** *A marker's reason quotes a code span* and
      *A marker's tail carries no separator outside a code span*. Without them
      the new normative rule would promote with no scenario exercising it and
      would be pinned only by this packet's tests — running code standing in for
      canon, which is the exact shape `proposal.md` § *Why this is NOT a plain
      fix* refuses. No promoted scenario moves, is retitled or loses a bullet;
      the marker names a BODY unit, so `suppression`'s `adds_new_title` gate —
      which withholds the scenario-title bullet cascade from a block that adds a
      title — has nothing to withhold here. Measured on the branch: the block
      still raises ZERO findings from its own family.

## 5. Owed, and deliberately not taken here

- [ ] 5.1 **A MARKER NAMING SOMETHING THAT IS NOT A UNIT IS STILL SILENT.**
      `suppression`'s third resolution is fail-closed by design and this packet
      does not touch it — but it is what absorbed this defect. A family that
      reported *"this marker names something no unit of the requirement
      matches"* would have surfaced `WHEN` and `AND` the day they were written.
      The family's own author recorded that as a plausible later ruling; it is an
      OWED SUCCESSOR with its own scenarios to write, and it is not this packet.
      **AND THIS AMENDMENT ADDS A SECOND CASE TO THAT SILENCE, NAMED HERE AS ITS
      OWN CONSEQUENCE RATHER THAN AS PRE-EXISTING GAP.** An author who separates
      two names with ` — ` — which `document-lifecycle`'s *"naming each deleted
      unit as a CommonMark code span"* reads as legitimate — now declares only
      the first, and the second is REPORTED (the conservative direction) with
      this family's fixed action string telling them to declare a deletion with a
      marker they already wrote. The successor is therefore scoped to report
      *"this marker carries a code span INSIDE its reason"* as well as *"this
      marker names something no unit matches"*; the first is mechanically
      detectable and points at the real cause.
- [ ] 5.2 **THE TWO PROMOTED MARKERS ARE NOT EDITED, AND NEITHER ARE THE
      ARCHIVED DELTAS THAT CARRY THEM.** They are records of ratified removals.
      Nothing is owed here; it is recorded so that a later reader does not read
      the omission as an oversight.
- [ ] 5.3 **`specs/019-modified-block-currency-family/spec.md` FR-016 AND
      RATIFIED-READING A1 STILL STATE THE RETIRED SENTENCE, AND ARE DELIBERATELY
      NOT EDITED.** The Speckit feature spec for this module carries the retired
      rule as an `FR-` MUST and repeats it in reading A1. It is a BUILD RECORD of
      what `add-modified-block-currency-check` specified and was implemented
      against — not promoted canon, pinned by no test and by no gate — and
      precedent `amend-unreadable-read-sibling-scenarios` (PR #688) likewise
      edited no feature spec when it amended the canon those specs describe.
      Recorded as residue so a later reader does not read the omission as an
      oversight; a superseding note in `specs/019` is available to a later act
      and is not this packet's.
- [ ] 5.4 **THE ESTATE-WIDE RUN IS OWED AT LANDING, NOT TAKEN HERE.**
      `active_blocks()` takes a repository root and the aggregation's nightly run
      reads every submodule, so a marker in a sibling repository that separates
      its names with ` — ` would surface as new advisory findings there. The
      measurement in this packet covers openxFactory only, this lane being
      confined to its own clone. The direction is safe by construction — the
      amended names are always a subset of the retired ones, so suppression can
      only shrink and a unit can only become MORE visible — and both affected
      arms are `info`/`warning`, so no `--fail-on error` run can red on it. What
      is owed is the estate-wide run recorded on the pull request or here, so the
      first nightly does not hand another lane findings nobody attributes.
- [ ] 5.5 **ARCHIVE.** `code_surface` is non-empty, so under `release-realization`
      this packet archives on merged-plus-green realization evidence rather than
      on landing, and on a separate word.
