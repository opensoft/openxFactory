# Tasks: amend-merged-into-empty-tail-standing

Status: draft
Kind: tasks

`code_surface: none`, `target_release: none`. Under `release-realization` an
empty code surface archives ON LANDING plus its own task list rather than on
merged-plus-green realization evidence — **and that archive is still a separate
act on a separate word, and it is NOT performed here** (§ 5).

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body.
**§ 1 (RATIFICATION) IS ENTIRELY OPEN**: Brett Heap's ruling of 2026-09-11,
verbatim *"Rule the silence correct in canon"*, settles `design.md` D1's
DIRECTION and commissions this authoring — it was given before a sentence
existed and it approves no wording. **§ 5 (ARCHIVE) IS ENTIRELY OPEN**: the
promotion of the block into `openspec/specs/doc-health/spec.md` and the closing
line for openxFactory #914 belong to the archive pull request and to nothing
here. **§ 6 STAYS UNTICKED**: residue, measured and deliberately not taken.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RATIFICATION IS A SEPARATE WORD AND IT HAS NOT BEEN GIVEN.** The
      word this packet was AUTHORED on — Brett Heap's *"Rule the silence
      correct in canon"* of 2026-09-11, given in session by multiple choice
      (~01:3xZ) and recorded on openxFactory
      [#914](https://github.com/opensoft/openxFactory/issues/914#issuecomment-5628349929)
      at 2026-09-11T02:06:38Z — is the ORIGIN of the AUTHORING and is not read
      as an approval: it chose between #914's two options and decided no
      wording, no scenario and no marker. Every document in this packet carries
      `Status: draft`; `.openspec.yaml` carries drafting provenance with **no**
      `approved_by` and **no** `approved_on`, which is the lawful unapproved
      shape `add-drafted-proposal-origin` (issue #318) defined. At
      ratification the status flip and the approval pair move in ONE commit,
      the pair ADDED beside a fixed `kind` and `id`.
- [ ] 1.2 **`design.md` D1 IS THE VETO POINT — THE WORDING.** The direction is
      ruled; the sentence is not. **THE OPTIONS AS THEY ARE PUT:** Option **A**
      (RECOMMENDED, and what the delta encodes): one sentence in the grounds
      paragraph stating that a `Merged into` marker declares its DESTINATION in
      its PREFIX and owes no tail, so a tail naming no superseded title is
      SILENT BY RULE — not reported on the fifth ground, which is read on the
      `Removed from canon` form alone, and, where the tail carries no code span
      at all, reaching none of the other four either, each of those being read
      through a name or a quoted span such a tail does not carry; with a final
      clause keeping a code span the reason DOES quote subject to the second
      ground, so the silence is scoped at the SHAPE and never at the FORM.
      Option **B** (#914's own second option, and the one the ruling declined):
      report it as a SIXTH GROUND at `info` on the `Merged into` form alone —
      one predicate, one WHY clause, a flipped test and a code surface, which
      would report a marker that declared everything its form requires and
      would change this packet's archive rule. **A VETO OF THE WORDING** costs
      the added sentence, the added scenario and the marker's one name, and
      restores the retired clause verbatim; a veto of the DIRECTION reverses
      the ruling of 2026-09-11 and is not treated as available to this lane.
- [ ] 1.3 **`design.md` D2 IS THE SECOND VETO POINT — THE MARKER, AND IT IS
      DECIDED BY MEASUREMENT RATHER THAN BY THE RULING.** A pure addition would
      owe no `Removed from canon` marker; the measurement refuses a pure
      addition, because the clause the ruling contradicts is not a unit —
      `derive_units` reads the whole fifth-ground sentence as ONE body unit of
      478 characters and this corpus has no instrument for retiring a CLAUSE.
      So the sentence is RETIRED AND REPLACED IN PLACE, one canon unit goes
      uncarried, and a marker is owed. The alternative — leave the sentence
      standing and add a second sentence beside it — is written out in
      `design.md` D2 with its cost: canon would say the requirement does not
      decide the question and then decide it, two sentences apart.
- [ ] 1.4 **`design.md` D0 AND D3 THROUGH D6 ARE CARRIED BESIDE THEM.** D0 the
      measurement — 27 markers, ZERO `Merged into` markers with a tail carrying
      no code span, 29 active MODIFIED blocks of which TWO carry a unit-naming
      marker — together with the correction it forces to #914's own figure (the
      issue's "9 pairing-form markers" counts a THIRD form, not the form this
      packet rules on). D3 why an OpenSpec change and not a patch. D4 why
      `code_surface: none` archives on landing and why the archive is still a
      separate act. D5 the sibling search, pasted. D6 what is measured and
      deliberately not taken.

## 2. The measurement, taken before the design

- [x] 2.1 **EVERY MARKER IN THE CORPUS, COUNTED BY FORM AND BY TAIL** —
      `openspec/specs/*/spec.md` and every active
      `openspec/changes/*/specs/*/spec.md`, read through `derive_units` so that
      fenced example markers are never offered, exactly as they are never
      offered to a run. Taken 2026-09-11 on the clone of `main` @ `96b4835b`:
      **27 markers — 15 of `Removed from canon` form, 3 of `Merged into` form
      and 9 of the pairing form; ZERO `Merged into` markers whose tail carries
      no code span, ZERO `Removed from canon` markers with an empty tail, and
      ZERO pairing-form markers carrying no reason at all.** The table is in
      `proposal.md` and in `design.md` D0. **THE SCOPE IS THE CORPUS AS IT
      STOOD BEFORE THIS PACKET**, said so wherever the figure appears: this
      block carries a marker of its own, excluded so that a reader re-deriving
      the figure on `main` @ `96b4835b` gets exactly 27.
- [x] 2.2 **THE RULED SHAPE HAS A POPULATION OF ZERO TODAY.** The family reads
      markers only inside active `## MODIFIED Requirements` blocks; there are
      **29** such blocks on this tree and exactly **TWO** carry a unit-naming
      marker — `add-chain-attestation` and `add-composed-view-authoring`, both
      `Merged into`, each naming exactly one superseded title that matches its
      resolved basis. Measured, not assumed: the branch's `doc-health` finding
      set is identical to `origin/main`'s LINE FOR LINE, and **the
      marker-defect class raises NOTHING on either tree** (§ 4.6).
- [x] 2.3 **THE ZERO IS ALREADY ASSERTED AS A TEST, WHICH IS WHY THIS PACKET
      ADDS NONE.** `tests/doc-health/test_modified_block_currency.py::test_a_MERGED_marker_whose_tail_names_nothing_stays_SILENT`
      constructs exactly this marker, asserts `m.form == "merged"`,
      `m.destination`, `m.names == []` and `m.quoted == []`, and asserts the
      defect list is EMPTY. `amend-marker-declaring-nothing` wrote it so the
      silence would be *"a decision a later act can overturn rather than a gap
      it has to rediscover"*. This is that later act and it CONFIRMS the
      assertion rather than flipping it, so a second test would assert one fact
      twice.
- [x] 2.4 **THE SENTENCE IS PROMOTED IN ONE PLACE, CHECKED IN BOTH
      DIRECTIONS.** `document-lifecycle`'s marker grammar says how a deleted
      unit is NAMED and carries no reporting rule at all, so it needs no
      amendment and none is made. `doc-health` is where the reporting rule
      lives, and the retired sentence occurs ONCE in it: read with the
      whitespace normalization this requirement itself defines, both the whole
      sentence and the clause the ruling contradicts occur exactly 1 time in
      `openspec/specs/doc-health/spec.md`.
- [x] 2.5 **NO ACTIVE CHANGE CARRIES A `## MODIFIED` BLOCK FOR THIS
      REQUIREMENT.** Measured rather than recited (`design.md` D5): of the
      three active changes carrying a `doc-health` delta at all, one is this
      packet, `add-nightly-dashboard-refresh` is seven `## ADDED` requirements
      of the refresh lane, and `settle-aging-staging-topics` modifies *Aging
      threshold defaults*. The three other active changes that name this
      requirement mention it in prose only
      (`prepare-openspec-1-12-readiness/tasks.md`,
      `disposition-codexfactory-floor-relocation-retitle/design.md`,
      `disposition-codexfactory-declared-renames/design.md`). No two-writers
      ordering is owed; `sequenced_after: []` is declared as an explicit root
      claim.
- [x] 2.6 **`kind: ad_hoc` IS CHECKED RATHER THAN ASSUMED.**
      `ideation/staging/` was enumerated and `INDEX.md` read on 2026-09-11: its
      30 topic folders carry no marker grammar, no marker-defect reporting and
      no doc-health carriage arm. The `INDEX.md` lines matching "marker" are
      the `xspec:candidate`/`xspec:supersedes` PROSE-TAGGING grammar, the
      doxBench dirty-tile UI marker and a compression-marker note — three
      different things in three different capabilities. `kind: staged` would
      claim a staging source that does not resolve. The organized source is
      openxFactory #914 and the archived § 7.1 that scoped it.

## 3. The delta

- [x] 3.1 **ONE `## MODIFIED` REQUIREMENT, WRITTEN OVER CANON**, byte-faithful
      by CONSTRUCTION rather than by transcription: the block was GENERATED by
      slicing `openspec/specs/doc-health/spec.md` lines **1588–2037** and
      **2063–2168** and applying ONE replacement as an exact single-occurrence
      substitution inside the ONE paragraph it touches (the generator REFUSES
      on any other count), then re-wrapping ONLY that paragraph — which canon
      itself makes unit-identical, *"a re-wrapped paragraph compares equal to
      the same paragraph wrapped differently"*. The gap between the slices is
      the promoted marker paragraph a block must not restate (§ 3.4). Verified
      after the fact by the family's own derivation (`carried()` and
      `suppression()`, the two callables the shipping path uses): **165 canon
      units, 1 uncarried, that one named by the marker and suppressed, 0
      uncarried-and-unsuppressed, 0 marker defects, 21 of 21 promoted scenario
      titles carried, 0 missing.**
- [x] 3.2 **ONE UNIT RETIRED AND REPLACED IN PLACE, ONE SENTENCE ADDED BESIDE
      IT.** The retired unit is the fifth-ground sentence; it is REPLACED, not
      dropped, by a sentence carrying its removal-form scoping and its ENTIRE
      pairing-form exclusion word for word, with only the clause calling the
      merge form's empty tail undecided removed. The added sentence states the
      ruling, and it is written so that it cannot be read as a sixth ground: a
      prohibition (*SHALL NOT be reported*) in a paragraph of obligations, the
      count of grounds left at FIVE in the sentence above it, and a final
      clause keeping a quoted code span subject to the second ground.
- [x] 3.3 **ONE `Removed from canon` MARKER, ONE NAME, NO CODE SPAN IN ITS
      REASON — AND THE MARKER IS ASSEMBLED FROM `derive_units`' OWN OUTPUT
      RATHER THAN RETYPED**, so it cannot name a fragment or a unit as its
      author remembers it. The name contains backticks (`` `Removed from
      canon` ``, `` `Merged into` ``) and is fenced with a LONGER run, exactly
      as canon's own rule requires. The assembled marker is re-parsed by
      `parse_marker` and asserted to yield exactly one name, an EMPTY `quoted`
      and a reason with no code span in it — which is why ground two has
      nothing to resolve over it, and why the marker survives all five grounds
      (`design.md` D2).
- [x] 3.4 **THE SELF-REFERENCE HAZARD IS DISCHARGED.**
      `amend-marker-declaring-nothing`'s promoted `Removed from canon` marker
      is **deliberately NOT restated**, on this requirement's own rule that a
      marker is not a carriage unit in either direction: its two named units
      are sentences canon no longer carries, so restating it would make this
      block report ITSELF under ground three. The `AMENDED BY` note says so in
      terms.
- [x] 3.5 An `**AMENDED BY …**` note in the precedents' style records the whole
      accounting: that every paragraph and every scenario above it stands
      exactly as promoted, that the only promoted text changed is ONE sentence
      of one paragraph, that one sentence and one scenario are added, that NO
      ground is added and none withdrawn, that no severity, threshold, arm,
      parse, grammar or resolution row moves, that NO CODE MOVES and the two
      artifacts that already implement the rule are cited rather than edited,
      the measured population, and why the predecessor's marker is absent.
- [x] 3.6 **ONE SCENARIO IS ADDED AT THE END OF THE BLOCK** — *A merge marker's
      tail names no superseded title* — because a rule no scenario exercises is
      a rule the next author re-deriving this class has nothing to test
      against, and because pinning it only by a test would be running code
      standing in for canon. No promoted scenario moves, is retitled or loses a
      bullet. The block ADDS one scenario title, so `suppression`'s
      `adds_new_title` gate withholds the scenario-title bullet cascade — which
      has nothing to withhold here, this packet's marker naming a BODY unit.
- [x] 3.7 **README `## OpenSpec Records` CARRIES THE ACTIVE ROW**, in house
      style, naming the origin issue, the ruling and its recording, the veto
      points, the zero population and the DRAFT standing. **AUTHORED AT THE
      DRAFT STANDING**: the row says `Status: draft` in terms and says that
      ratification, promotion and the archive are three later acts.
- [ ] 3.8 **THE PER-CHANGE SWEEP LEDGER ROW IS SEEDED BY THE SANCTIONED TOOL**,
      never hand-written: `python3 scripts/validate-sequenced-after.py .
      --seed-ledger --moved-by '#<this pull request>'`, run AFTER the draft
      pull request exists because the tool stamps `moved_by` with its number.
      The diff must be ONE line — this change's own row — and no other row's
      provenance may move.

## 4. Verification — IN THIS PULL REQUEST

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate
      amend-merged-into-empty-tail-standing --strict`
- [ ] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`, with the
      failure set measured against `origin/main`'s and required to be
      IDENTICAL.
- [ ] 4.3 `python3 scripts/proposal-support.py . verify
      amend-merged-into-empty-tail-standing`
- [ ] 4.4 `python3 scripts/validate-sequenced-after.py .` and `--ledger-diff`
- [ ] 4.5 `python3 scripts/validate-scope-globs.py .`
- [ ] 4.6 `python3 scripts/doc-health.py --single-repo .`, with the finding set
      measured against `origin/main`'s line for line.
- [ ] 4.7 `python3 -m pytest tests/doc-health tests/sequenced_after
      tests/scope_globs tests/proposal-support -q`
- [ ] 4.8 **EVERY GATE RE-RUN IN FULL ON THE FROZEN TREE**, after the ledger
      seed of § 3.8.

## 5. Archive — OWED, NOT GIVEN

**THE PROMOTION IS NOT PERFORMED HERE AND NOTHING UNDER `openspec/specs/` IS
EDITED BY THIS PULL REQUEST.** `code_surface: none` means this packet archives
ON LANDING plus its own task list under `release-realization` rather than on
merged-plus-green realization evidence — but landing is a merge, and the
archive is the act that moves the packet into
`openspec/changes/archive/<date>-amend-merged-into-empty-tail-standing/` and
writes the block into `openspec/specs/doc-health/spec.md`. That act needs
Brett Heap's word, it follows ratification, and openxFactory #914 closes THERE.

- [ ] 5.1 **RATIFY, THEN ARCHIVE.** § 1 first: the status flip and the approval
      pair in one commit. Then the archive act, on its own word.
- [ ] 5.2 **THE CLOSING LINE FOR openxFactory #914 STANDS IN THE ARCHIVE PULL
      REQUEST'S BODY AND NOWHERE ELSE.** This pull request's body carries
      `refs` and no closing keyword, and `closingIssuesReferences` is verified
      EMPTY on it (recorded in the pull request body).
- [ ] 5.3 **AND THE SANCTIONED ARCHIVE PATH REFUSES AN OPEN BOX**, with no
      bypass flag: `scripts/proposal-support.py` refuses any change whose
      `tasks.md` still matches `^- \[ \]` (*"change has incomplete tasks"*), so
      every box above is ticked in the commit BEFORE the move rather than after
      it.

## 6. Measured, and deliberately NOT taken here

- [ ] 6.1 **`scripts/doc_health/modified_block_currency.py` IS NOT EDITED, AND
      TWO PIECES OF ITS PROSE GO STALE AT THE PROMOTION.** `suppression`'s
      docstring at `:1432` and the comment beside the fifth-ground predicate at
      `:1535` each say that a `Merged into` marker whose tail names no
      superseded title is *"a question nobody has ruled"*. After the archive
      that sentence is false, while the PREDICATE it sits beside stays exactly
      right and no behaviour moves — so this is a comment-currency debt, not a
      defect, and taking it here would give this packet a code surface and
      change its archive rule (`design.md` D4). A successor is NAMED at the
      archive act, on the tick-on-the-recording ruling of 2026-09-06.
- [ ] 6.2 **`specs/019-modified-block-currency-family/` IS NOT EDITED.** Its
      FR-018 states the ONE reporting ground a marker had before
      `amend-marker-defect-reporting` made it three, and the restatement is
      already owed by openxFactory
      [#915](https://github.com/opensoft/openxFactory/issues/915), filed at the
      predecessor's archive and OPEN. This packet adds no ground, so it neither
      widens that scope nor discharges it; and the build record says nothing at
      all about the merge form's empty tail — checked, not assumed.
- [ ] 6.3 **THE ESTATE-WIDE RUN IS NOT OWED.** The predecessor owed one because
      it ADDED two reporting grounds and a sibling repository's marker could
      have surfaced new advisory rows there. Both directions of THIS amendment
      are silence — no finding starts being emitted, none stops, no severity
      moves and no suppression changes — so no governed repository can gain or
      lose a row and the uncited-resolution rule has nothing to fire on. The
      direction is bounded by construction and measured on this repository
      (§ 4.6).
- [ ] 6.4 **THE PER-CLASS GRAIN OF THE UNCITED-RESOLUTION RULE IS NOT WIDENED.**
      `report.uncited_resolutions` keys on `(family, repository, path)`; that is
      the shipped behaviour and promoted canon states it. Whether the checker
      SHOULD track disappearance at finding-class grain is openxFactory
      [#893](https://github.com/opensoft/openxFactory/issues/893), filed by
      `amend-modified-block-currency-standing` at its own archive, and it is
      that issue's work rather than this packet's.
