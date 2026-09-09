# Tasks: amend-marker-defect-reporting

Status: ratified
Ratified by: amend-marker-defect-reporting — 2026-09-09, Brett Heap, "merge 842 and 846 when green, then ratify the 729 packet" (record `review/ratification-2026-09-09.md`)
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is IN THIS PULL REQUEST: the tasks are individually
executable, so under `release-realization`'s decomposition rule this packet
realizes through its own task list rather than through a feature DAG.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in the pull request body.
**§ 5 STAYS UNTICKED AND NAMES WHY**: residue and owed successors, not work this
packet performs.

**AMENDED AT THE ARCHIVE, 2026-09-09 — EXACTLY ONE SENTENCE ABOVE IS SUPERSEDED,
IT IS NAMED, AND IT IS QUOTED IN PLACE RATHER THAN DELETED.** The superseded
sentence is this one and no other:

> **§ 5 STAYS UNTICKED AND NAMES WHY**: residue and owed successors, not work
> this packet performs.

Every box in § 5 is now ticked. **THE SENTENCE BEFORE IT — *"NOTHING IS TICKED
THAT DID NOT LAND"* — IS NOT SUPERSEDED**: it still holds, and these ticks are
what make it hold, because each one records the NAMING of a successor and not the
doing of the work that successor carries. Five successors were filed **UNCLAIMED**
at this archive — **#856** (§ 5.2), **#857** (§ 5.3), **#858** (§ 5.4), **#859**
(§ 5.5) and **#860** (§ 5.7) — and § 5.6 is the archive box itself, ticked on the
act this pull request performs. The full disposition is at the head of § 5, and
the ratified text of every box is carried there verbatim beneath its tick clause.

## 1. Ratification — GIVEN 2026-09-09

- [x] 1.1 **RATIFIED 2026-09-09 by Brett Heap** (openxFactory operator
      authority), in session, verbatim *"merge 842 and 846 when green, then
      ratify the 729 packet"* (2026-09-09T13:13:41Z, recorded on openxFactory
      issue **#729**). **THE WORD IS ONE UTTERANCE OF THREE CLAUSES IN ORDER,
      AND THE ORDER WAS KEPT**: PR **#842** merged `4cdadd56` (16:11:57Z) and PR
      **#846** merged `183d1b43` (16:12:40Z), both green, and this encode is the
      third clause. The earlier *"author the 729 packet"*
      (2026-09-09T12:32:46Z) remains recorded as the ORIGIN of the authoring —
      it instructed a lane to write a remedy and decided no wording.
      `proposal.md`, `design.md` and this file now carry `Status: ratified` with
      **ONE** citation line each — `Ratified:` in `proposal.md`'s front matter,
      `Ratified by:` here and in `design.md` — which is what
      `ratified-provenance` counts. `.openspec.yaml` gains the approval pair
      (`approved_by`, `approved_on`) **BESIDE** the drafting provenance it was
      authored with, `kind` and `id` unmoved, which is the addition-not-rewrite
      shape `add-drafted-proposal-origin` defined for this transition and the
      shape the archive gate's origin-retention arm reads. Record:
      `review/ratification-2026-09-09.md`, with the verification run captured
      beside it at `review/verification-2026-09-09.md`.
- [x] 1.2 **THE VETO POINT WAS `design.md` D1 AND IT WAS NOT VETOED** — option
      **A** (a reason-quoted span is reported only where it matches EXACTLY a
      unit of the requirement's basis the block does not carry and no marker
      declares removed) against option **B** (any code span inside a reason,
      the remedy shape issue #729's own body proposes). It was carried as the
      veto point in the pull request body, in this file, in the README row and
      on issue #729, with B written out beside A and its four costs, the first
      being that it fires on canon's own blessed form and makes EIGHT correct
      promoted markers reportable — a share that grew from 2 of 7 to 8 of 16 in
      three days. **A is RATIFIED AS DESIGNED**, ground two included. **A veto
      of A would have been a veto of GROUND TWO ONLY**: ground three rests on no
      predicate choice and stood either way. The narrowing `design.md` D5 adds
      to the ruling's literal wording — *"and that no marker declares removed"*,
      narrower in the SILENT direction — was disclosed on issue #729 at 14:22Z,
      before the act this word authorized, and is ratified with A.

## 2. The measurement, taken before the design

- [x] 2.1 **EVERY UNIT-NAMING MARKER IN THE CORPUS, WITH ITS REASON-QUOTED
      SPANS RESOLVED AGAINST THE UNITS OF ITS OWN DOCUMENT** —
      `openspec/specs/*/spec.md` and every active
      `openspec/changes/*/specs/*/spec.md`, read through `derive_units` so that
      fenced example markers are never offered, exactly as they are never
      offered to a run. **SIXTEEN markers; EIGHT quote a code span INSIDE their
      reason, every one of them PROMOTED; and of the 34 spans those eight
      reasons quote, ZERO is a derived unit of the document that carries the
      marker.** The tables are in `proposal.md` and in `design.md` D0. **THE
      SCOPE IS THE CORPUS AS IT STOOD BEFORE THIS PACKET**, said so wherever the
      figure appears: this block carries a seventeenth marker of its own, § 4.3's
      self-reference case, excluded so that a reader re-deriving the figure on
      `main` @ `6df21737` gets exactly sixteen.
- [x] 2.2 **BOTH NEW GROUNDS HAVE A POPULATION OF ZERO TODAY.** The family reads
      markers only inside active `## MODIFIED Requirements` blocks, and exactly
      TWO of those carry a unit-naming marker — `add-chain-attestation` and
      `add-composed-view-authoring`, both `Merged into`, one name each matching
      its resolved basis, neither quoting a code span in a reason. Measured, not
      assumed: `--family modified-block-currency` returns output identical to
      `origin/main`'s, line for line, apart from the repository identity label.
- [x] 2.3 **THAT MEASUREMENT IS WHAT MAKES GROUND TWO NARROW.** Half this
      corpus's unit-naming markers quote a code span in their reason and canon
      blesses precisely that shape, so the position predicate is the predicate
      for the NORMAL FORM rather than for a defect. The exact-match predicate is
      silent on all eight and fires on the shape
      `amend-marker-reason-boundary` created; it is asserted as a test
      (§ 3.6) rather than only measured.
- [x] 2.4 **THE SENTENCE IS PROMOTED IN ONE PLACE, CHECKED IN BOTH
      DIRECTIONS.** `document-lifecycle`'s marker grammar says how a deleted
      unit is NAMED and carries no reporting rule at all, so it needs no
      amendment and none is made. `doc-health` is where the reporting rule
      lives, and the retired sentence occurs once in it.
- [x] 2.5 **NO ACTIVE CHANGE CARRIES A `## MODIFIED` BLOCK FOR THIS
      REQUIREMENT.** Grepped over `openspec/changes/`: the two active changes
      that name it at all mention it in prose
      (`prepare-openspec-1-12-readiness/tasks.md`,
      `disposition-codexfactory-declared-renames/design.md`) and carry no delta
      over it. No two-writers ordering is owed and `sequenced_after` is
      elective, undeclared.

## 3. The realization — two grounds, in this pull request

- [x] 3.1 `scripts/doc_health/modified_block_currency.py`: `Marker` gains
      `quoted`, the post-boundary code spans in order, normalized — A LAST
      PARAMETER WITH A DEFAULT, on the `basis` precedent, so every existing
      positional construction of a `Marker` still reads. `parse_marker` fills it
      from the spans it already computed and discarded. **NO PARSE MOVES**:
      `names` and `reason` are exactly what the amended boundary derived, and
      the field is EMPTY for the pairing form (whose whole tail is a reason and
      which names no units) and for a marker whose tail carries no boundary
      (where every span IS a name).
- [x] 3.2 `suppression` gains the two resolutions and returns
      `list[_MarkerDefect]` in place of `list[Marker]` — a PRIVATE record of one
      marker and one ground, on `_reason_boundary`'s rule, so the module's
      public surface is unchanged and
      `test_this_feature_touches_no_production_module` is NOT edited. Every
      existing assertion over `defective` compares it to `[]`, so the change of
      element type reds nothing.
- [x] 3.3 **GROUND TWO RUNS IN A SECOND PASS AND IT HAS TO** (`design.md` D5):
      its predicate asks about a unit NO marker accounts for, which cannot be
      decided until every name in the block is resolved. A span the marker also
      NAMES is skipped — its author declared it — and that one line is what
      keeps the retired-rule half of
      `test_a_reason_quoting_a_REAL_canon_unit_suppresses_it_under_the_retired_rule`
      true.
- [x] 3.4 `TEMPLATE_MARKERS` gains ONE interpolated `{why}` field and keeps its
      fixed opening and its fixed trailing prose — ONE TEMPLATE FOR THREE
      GROUNDS, on the `TEMPLATE_PAIRING` precedent and Brett's shape amendment
      of 2026-08-28 (`design.md` D2). `_ARM_TEMPLATES` stays at EIGHT, the
      existing `CLASS_MARKERS` probe places every new finding so the seventh
      class stays silent, and **ground one's rendered text is byte-identical to
      the one this class shipped with**.
- [x] 3.5 `_arm_marker_defects` renders one finding per record at
      `_LEDGER_SEVERITY` with the class's existing `_MARKER_ACTION` —
      unchanged, because it already names the remedy for all three grounds and a
      per-ground action would break
      `test_every_finding_carries_its_class_s_band_and_action` for no reader's
      benefit.
- [x] 3.6 `tests/doc-health/test_modified_block_currency.py`: **128 → 139**,
      eleven tests ADDED — the quoted spans are carried rather than discarded;
      ground two fires on an uncarried promoted unit; a reason quoting something
      that is no unit at all stays SILENT (the shape all eight promoted markers
      are written in); a unit a sibling marker declares removed stays silent;
      ground three fires and names only the names that matched nothing; a name
      matching a unit the BLOCK adds stays silent (D3); a well-formed marker is
      silent on all three grounds; ground one's finding is byte-identical to the
      shipped one, asserted against a typed-out literal rather than the
      template; a marker defective twice reports TWO findings in a fixed order;
      each new ground matches exactly ONE arm template and classifies as
      `marker-defects`; and no marker in the corpus raises either new ground
      today.
- [x] 3.7 **THREE EXISTING ASSERTIONS ARE FLIPPED RATHER THAN LOOSENED, AND
      NAMED HERE RATHER THAN LEFT IN THE DIFF.** All three sit in tests that
      BUILD the shapes these grounds exist for and all three asserted the
      silence this packet retires:
      `test_names_separated_by_the_separator_fail_in_the_CONSERVATIVE_direction`
      and `test_a_reason_quoting_a_REAL_canon_unit_suppresses_it_under_the_retired_rule`
      (both `defective == []`), and
      `test_the_inner_backtick_does_not_truncate_the_named_unit` in
      `test_modified_block_currency_fixtures.py` — **the REAL fixture instance**,
      a marker whose single-backtick fence truncates its name to a fragment
      matching no unit, whose author previously saw only the ledger row for a
      clause they thought they had declared. Each edit states the reason where
      the assertion stands. **No other existing test is edited.**
- [x] 3.8 Two comments describing the retired rule are corrected, on
      `amend-marker-reason-boundary` § 3.3's own rule that a comment describing
      a retired rule will mislead the next reader: the module header's
      fail-closed bullet and the arm list's marker-defect entry, plus
      `suppression`'s docstring.

## 4. The delta

- [x] 4.1 `specs/doc-health/spec.md` restates *Currency of an active change's
      MODIFIED requirement blocks* IN FULL — every body unit, every scenario
      title and every scenario bullet, byte-faithful, including the fenced block
      that writes the two marker forms out and including
      `amend-marker-reason-boundary`'s own `AMENDED BY` note and its narrative
      paragraph — with ONE body sentence replaced.
- [x] 4.2 The retired unit is declared by the reserved marker
      `**Removed from canon by amend-marker-defect-reporting (2026-09-09):**`,
      naming it verbatim as a code span. The unit contains no backtick, so a
      single-backtick fence names it whole and canon's longer-fence rule has
      nothing to do here.
- [x] 4.3 **THE SELF-REFERENCE HAZARD IS DISCHARGED** (`design.md` D4). This
      packet's own marker names one canon unit the block does not carry and
      carries **NO CODE SPAN IN ITS REASON**, so ground two has nothing to
      resolve over it and it parses to exactly one name. And
      `amend-marker-reason-boundary`'s promoted `Removed from canon` marker is
      **deliberately NOT restated**, on this requirement's own rule that a
      marker is not a carriage unit in either direction: its named unit is a
      sentence canon no longer carries, so restating it would make this block
      report ITSELF under its own new ground three. The `AMENDED BY` note says
      so in terms, and the general consequence — copying a predecessor's
      declaration forward is now reportable — is disclosed in `proposal.md`
      § Impact.
- [x] 4.4 An `**AMENDED BY …**` note in the precedents' style records that every
      paragraph and every scenario above it stands exactly as promoted, that the
      only change to promoted text is the one sentence, that two scenarios are
      added, and that the reason-quotes scenario's third `AND` — the carriage
      the new report is added BESIDE — is carried word for word.
- [x] 4.5 **TWO SCENARIOS ARE ADDED AT THE END OF THE BLOCK, ONE PER GROUND.**
      *A marker's reason quotes a unit the block does not carry* and *A marker
      names something no unit matches*. Without them the two grounds would
      promote with nothing exercising them and would be pinned only by this
      packet's tests — running code standing in for canon, the exact shape
      `proposal.md` § *Why this is NOT a plain fix* refuses. No promoted scenario
      moves, is retitled or loses a bullet. The block ADDS two scenario titles,
      so `suppression`'s `adds_new_title` gate withholds the scenario-title
      bullet cascade — which has nothing to withhold here, this packet's marker
      naming a BODY unit. Measured on the branch: the block raises ZERO findings
      from its own family.

## 5. Owed, and deliberately not taken here

**DISPOSITION 2026-09-09 — WHY EVERY BOX BELOW IS TICKED WHEN THE RATIFICATION
RECORD SAYS SIX OF THEM ARE NOT.** `review/ratification-2026-09-09.md` describes
§ 5.2, § 5.3, § 5.4, § 5.5, § 5.6 and § 5.7 as **UNTICKED**. That document is
`Status: record`: it is immutable, it is **NOT edited by this archive**, and it
stands exactly as written. Nothing below contradicts it — it named this act in
advance.

**FIRST, THE RECORD ITSELF FORESAW THIS ACT AND NAMED WHEN THE ISSUES WOULD BE
FILED.** `review/ratification-2026-09-09.md`, disposition 2, verbatim: *"§ 5.2,
§ 5.3, § 5.4, § 5.5 and § 5.6 are open and three of them name no successor;
`proposal-support` refuses the ARCHIVE act until each names a filed issue. That
is not a ratification defect — the predecessor `amend-marker-reason-boundary` was
ratified in exactly this shape with § 5.1–§ 5.5 open — and **the issues are filed
at the archive word**. § 5.7, added by the fix, is open on the same footing."*
This is the archive word, and these are those issues. § 5.7's own ratified text
says the same thing in its last clause: *"the issue is filed at the archive word
rather than here."*

**SECOND, THE SHAPE IS A RULING AND NOT A WORKAROUND.** Brett Heap,
**2026-09-06T23:10Z**, in session, by multiple choice, recorded on openxFactory
[#692](https://github.com/opensoft/openxFactory/issues/692), chose the option
labelled verbatim **"Tick on the recording"** — *an owed successor's task box
ticks once the successor is NAMED (issue filed), the box text saying the tick
records the naming, not the doing.* The predecessor
`amend-marker-reason-boundary` was the first packet ticked under it as a rule;
this is the second, and its own § 5.1 above was ticked on that same rule at
ratification.

**THIRD, THE SANCTIONED ARCHIVE PATH REFUSES AN OPEN BOX.**
`scripts/proposal-support.py` refuses any change whose `tasks.md` still matches
`^- \[ \]` — *"change has incomplete tasks"* — and there is no bypass flag, so
the archive act this packet's non-empty `code_surface` requires cannot be taken
while a box here is open.

**THE WORK IN § 5.2, § 5.3, § 5.4, § 5.5 AND § 5.7 IS NOT DONE, AND NO TICK BELOW
SAYS IT IS.** Each names a **filed, UNCLAIMED** GitHub issue — **#856**, **#857**,
**#858**, **#859**, **#860** — and the tick is on that naming. Every ratified
sentence of § 5.2 through § 5.7 is carried below **verbatim**, beneath the tick
clause; nothing of the ratified reading is deleted. § 5.6 is the archive box
itself: it restates its own ratified sentence beside the evidence for the act it
records.

**AND ONE OWED RUN IS FILED SEPARATELY RATHER THAN FOLDED INTO ITS SIBLING.**
§ 5.5's estate-wide measurement was checked against the predecessor's still-open
[#731](https://github.com/opensoft/openxFactory/issues/731) before a new issue was
filed. #731 owes the estate-wide measurement of `amend-marker-reason-boundary`'s
NARROWING — which markers change their NAME SET under the amended boundary versus
the retired last-code-span rule. This packet's § 5.5 owes a DIFFERENT measurement
over the same marker population: which markers REPORT under grounds two and
three. Same `active_blocks()` sweep, different predicates, different findings — so
#859 was filed for this one and names #731 as its sibling, and whoever claims
either should claim both. Citing #731 alone would have recorded this measurement
as taken care of by an issue whose declared scope does not include it.

- [x] 5.1 **THE SUCCESSOR `amend-marker-reason-boundary` § 5.1 OWED IS NAMED AND
      IS THIS PACKET.** That box ticks on the recording, which is what this
      packet is: openxFactory issue **#729** names it, this change id realizes
      it, and both silences § 5.1 scoped — a name matching no unit, and a code
      span inside a reason — are grounds three and two above. The archived
      packet's own text is NOT edited; an archived delta is a record of what was
      ratified.
- [x] 5.2 **TICKED ON THE RECORDING — THE SUCCESSOR IS NAMED AS openxFactory
      [#856](https://github.com/opensoft/openxFactory/issues/856), IT IS
      UNCLAIMED, AND THE WORK IS NOT DONE HERE.** Per the ruling of
      2026-09-06T23:10Z, verbatim *"Tick on the recording"*: the box ticks once
      the successor is NAMED, and this sentence is the box text saying the tick
      records the naming, not the doing. **NO FOURTH GROUND IS INVENTED BY THIS
      ARCHIVE AND THIS BOX DOES NOT SAY ONE IS** — the silence stands exactly as
      ratified, `suppression`'s `if name not in block_texts:` guard unmoved and
      `test_a_name_matching_a_unit_the_BLOCK_adds_stays_SILENT` still pinning it.
      The ratified text follows unchanged:
      **A NAME MATCHING A UNIT THE BLOCK ADDS AND CANON DOES NOT IS STILL
      SILENT** (`design.md` D3). Whether a block may declare its own additions
      removed, and against what, is a rule nobody has written, and inventing a
      fourth ground here would repeat on the same afternoon the fault this
      packet corrects. Pinned by a test so the silence is a decision a later act
      can overturn rather than a gap it has to rediscover.
- [x] 5.3 **TICKED ON THE RECORDING — THE RESIDUE IS NAMED AS openxFactory
      [#857](https://github.com/opensoft/openxFactory/issues/857), IT IS
      UNCLAIMED, AND THE CORRECTION IS NOT MADE HERE.** Per the ruling of
      2026-09-06T23:10Z, verbatim *"Tick on the recording"*: the tick records
      that the residue is on the queue with a resolvable name, **not** that canon
      has been corrected — it has not, and at this commit the *advisory at
      launch* paragraph still states `warning` severities and still says the
      family is *"deliberately absent from `FAMILY_RESOLUTION`"* while
      `_LAUNCH_SEVERITY` is `ERROR` and `families.FAMILY_RESOLUTION` carries the
      family `CONTESTED`. `review/ratification-2026-09-09.md` names this same
      residue in its own disposition 3 and is not edited. The ratified text
      follows unchanged:
      **CANON'S *ADVISORY AT LAUNCH* PARAGRAPH STILL DESCRIBES THE PRE-FLIP
      STATE, AND IS DELIBERATELY NOT CORRECTED HERE.** It states `warning`
      severities for the scenario-completeness and title-resolution arms and
      says the family "is deliberately absent from `FAMILY_RESOLUTION`" — both
      true at launch and neither true since the flip of 2026-08-31 (issue #357),
      which took `_LAUNCH_SEVERITY` to `error` and added the family's
      `contested` row. It is a PROMOTED UNIT, it is carried here byte-faithfully
      because this packet replaces exactly ONE sentence, and correcting it is its
      own amendment with its own ruling. Recorded as residue so a later reader
      does not read the omission as an oversight — and so that nothing in this
      packet is read as claiming an exemption from the `contested` row, which
      `design.md` D7 states plainly instead.
- [x] 5.4 **TICKED ON THE RECORDING — THE RESIDUE IS NAMED AS openxFactory
      [#858](https://github.com/opensoft/openxFactory/issues/858), IT IS
      UNCLAIMED, AND THE EDIT IS NOT MADE HERE.** Per the ruling of
      2026-09-06T23:10Z, verbatim *"Tick on the recording"*: the tick records
      the naming, **not** that `specs/019` has been corrected — at this commit
      FR-018 still states the ONE-ground rule. The remedy shape is already
      precedented in the same file: the predecessor's identical residue (#730)
      was taken at PR #827, which restated FR-016 and left a dated amendment
      note beside it, and #858 asks for exactly that form over FR-018. The
      ratified text follows unchanged:
      **`specs/019-modified-block-currency-family/` STILL STATES THE
      ONE-GROUND RULE AND IS DELIBERATELY NOT EDITED.** The Speckit feature spec
      for this module is a BUILD RECORD of what
      `add-modified-block-currency-check` specified and was implemented against
      — not promoted canon, pinned by no test and by no gate — and both
      precedents (`amend-unreadable-read-sibling-scenarios` PR #688,
      `amend-marker-reason-boundary` PR #719) likewise edited no feature spec
      when they amended the canon those specs describe. Recorded as residue; a
      superseding note there is available to a later act and is not this
      packet's.
- [x] 5.5 **TICKED ON THE RECORDING — THE OWED RUN IS NAMED AS openxFactory
      [#859](https://github.com/opensoft/openxFactory/issues/859), IT IS
      UNCLAIMED, AND THE RUN IS NOT TAKEN HERE.** Per the ruling of
      2026-09-06T23:10Z, verbatim *"Tick on the recording"*: the tick records
      the naming. **NO ESTATE-WIDE MEASUREMENT HAS BEEN TAKEN** — this lane is
      confined to its own openxFactory clone, exactly as the ratified text says,
      and the box says so rather than implying the run happened at the archive.
      #859 names the predecessor's still-open
      [#731](https://github.com/opensoft/openxFactory/issues/731) as its sibling
      sweep and is deliberately NOT folded into it: #731's declared scope is the
      NAME-SET narrowing of `amend-marker-reason-boundary`, and this one is the
      population of grounds two and three. The ratified text follows unchanged:
      **THE ESTATE-WIDE RUN IS OWED AT LANDING, NOT TAKEN HERE.**
      `active_blocks()` takes a repository root and the aggregation's nightly run
      reads every submodule, so a marker in a sibling repository whose name
      matches nothing, or whose reason quotes an uncarried unit of ITS
      requirement, would surface as new advisory findings there. The measurement
      in this packet covers openxFactory only, this lane being confined to its
      own clone. The direction is bounded by construction — both grounds REPORT
      and suppress nothing, so no suppression changes and no unit becomes less
      visible — and both are `info`, so no `--fail-on error` run can red on
      them. What is owed is the estate-wide run recorded on the pull request or
      here, so the first nightly does not hand another lane findings nobody
      attributes.
- [x] 5.6 **ARCHIVE — TAKEN, ON THE EVIDENCE BELOW AND ON A SEPARATE WORD.**
      `code_surface` is non-empty, so under `release-realization` this packet
      archives on **merged-plus-green realization evidence rather than on
      landing**. Both halves exist and are cited rather than asserted:
      - **RATIFIED AND REALIZED IN ONE PULL REQUEST** — **PR
        [#850](https://github.com/opensoft/openxFactory/pull/850) → merge
        `250d93d7`**, 2026-09-09T17:39:11Z, ratifying commit `4e3c2e26`, records
        `review/ratification-2026-09-09.md` and
        `review/verification-2026-09-09.md`, both `Status: record` and both
        untouched here.
      - **GREEN ON MAIN** — `pytest-suite` run
        **[34384218837](https://github.com/opensoft/openxFactory/actions/runs/34384218837)**,
        conclusion `success`, `headSha` **`250d93d79a`** — that is `250d93d7`
        **itself**, the merge commit: the green run is ON the commit that carries
        the realization, not merely on a descendant of it.
      **THE SEPARATE WORD IS BRETT HEAP'S**, 2026-09-09, in session, verbatim
      **"do 1, then 2"** — item 1 being the archive of this change and the
      closure of openxFactory #729. **ON THE RECORDING: THIS ARCHIVE PR
      [#862](https://github.com/opensoft/openxFactory/pull/862)** is the act the
      box records — the move to
      `openspec/changes/archive/2026-09-09-amend-marker-defect-reporting/`, the
      write-back of the delta into `openspec/specs/doc-health/spec.md`, the
      README row moving from the active list to the archived list, and the
      corpus-ledger row going `active` → `archived` with `moved_by: "#862"`.
      Its `closingIssuesReferences` is exactly `[729]`, verified through
      GraphQL, so #729 closes with this merge and with nothing else. Neither half of the evidence is a local
      assertion: both are references an outside reader resolves — a merge commit
      on `main` and a workflow run id. The ratified text follows unchanged:
      **ARCHIVE.** `code_surface` is non-empty, so under
      `release-realization` this packet archives on merged-plus-green
      realization evidence rather than on landing, and on a separate word.
- [x] 5.7 **TICKED ON THE RECORDING — THE SUCCESSOR IS NAMED AS openxFactory
      [#860](https://github.com/opensoft/openxFactory/issues/860), IT IS
      UNCLAIMED, AND THE GRAMMAR QUESTION IS NOT OPENED HERE.** Per the ruling
      of 2026-09-06T23:10Z, verbatim *"Tick on the recording"*: the box ticks
      once the successor is NAMED. **THE TICK IS THE ONE THIS BOX'S OWN RATIFIED
      TEXT ASKED FOR**: its last clause says the issue *"is filed at the archive
      word rather than here"*, and this is the archive word. No fourth ground is
      invented and no grammar rule is written; the case remains silent and
      unruled exactly as ratified. The ratified text follows unchanged:
      **A MARKER THAT NAMES NOTHING AT ALL IS STILL SILENT** — the FOURTH
      case of a marker that declares nothing about the block, and nobody has
      ruled it. A `Removed from canon` marker whose tail carries no code span
      parses to `names = []` and `quoted = []`, so `suppression`'s per-name loop
      never runs and the second pass has nothing to resolve: it reaches none of
      the three grounds and no finding is emitted. Found by this packet's
      adversarial pass, which is why the delta's sentence claims what the three
      grounds REPORT rather than claiming that every marker declaring nothing is
      reported (`design.md` D3, `proposal.md` § *What this proposal does NOT
      claim*). What such a paragraph even is — a marker form carrying no
      declaration, or prose that merely looks like one — is a grammar question
      this packet does not open, so no ground is invented here and no successor
      is named yet — the issue is filed at the archive word rather than here.
