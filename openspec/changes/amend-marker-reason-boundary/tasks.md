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
      `proposal.md` and in `design.md` D0.
- [x] 2.2 **WHY IT IS INERT: 17,566 derived units, NONE literally `WHEN` or
      `AND`.** `suppression`'s third resolution — a name matching no canon unit
      suppresses nothing and reports nothing — has been absorbing the defect by
      luck.
- [x] 2.3 **NO MARKER IN THIS CORPUS SEPARATES ITS NAMES WITH ` — `.** All
      seven separate names with `; ` and use ` — ` once, to open the reason. This
      is what makes option A's conservative failure direction EMPTY on the
      present corpus rather than merely tolerable, and it is asserted as a test
      (§ 3.4) rather than only measured.
- [x] 2.4 **THE SENTENCE IS PROMOTED IN ONE PLACE, CHECKED IN BOTH DIRECTIONS.**
      `document-lifecycle`'s marker grammar names each deleted unit as a code
      span and says nothing about the reason boundary, so it needs no amendment
      and none is made.
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
      to the amended rule. The BEHAVIOUR of that branch is untouched.
- [x] 3.4 `tests/doc-health/test_modified_block_currency.py`: **121 → 127**, six
      tests added and none edited — a reason quoting code spans names only the
      spans before the separator; a separator inside a code span is a unit's own
      bytes; a marker with no separator still names every span; names separated
      by ` — ` fail in the CONSERVATIVE direction and suppress nothing; the whole
      corpus loses no name any author meant to declare; and the two promoted
      markers, located BY CONTENT rather than by line number, parse to exactly
      one name each with a non-`None` reason.

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
      paragraph and every scenario above it stands exactly as promoted and that
      the only change is the one sentence.

## 5. Owed, and deliberately not taken here

- [ ] 5.1 **A MARKER NAMING SOMETHING THAT IS NOT A UNIT IS STILL SILENT.**
      `suppression`'s third resolution is fail-closed by design and this packet
      does not touch it — but it is what absorbed this defect. A family that
      reported *"this marker names something no unit of the requirement
      matches"* would have surfaced `WHEN` and `AND` the day they were written.
      The family's own author recorded that as a plausible later ruling; it is an
      OWED SUCCESSOR with its own scenarios to write, and it is not this packet.
- [ ] 5.2 **THE TWO PROMOTED MARKERS ARE NOT EDITED, AND NEITHER ARE THE
      ARCHIVED DELTAS THAT CARRY THEM.** They are records of ratified removals.
      Nothing is owed here; it is recorded so that a later reader does not read
      the omission as an oversight.
- [ ] 5.3 **ARCHIVE.** `code_surface` is non-empty, so under `release-realization`
      this packet archives on merged-plus-green realization evidence rather than
      on landing, and on a separate word.
