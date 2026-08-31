# Tasks — govern-sibling-added-modified-deltas

House rule: **OpenSpec ratifies, Speckit builds.** Each `## Speckit F<n>` group
below maps to exactly ONE Speckit feature and is the handoff unit; nothing in
this file is an executable task list for a session to work directly. Groups 1,
4, 5, 6, 7 and 8 are governance bookkeeping and belong to this packet.

## 1. Ratification

- [ ] 1.1 Put the packet to a §7.4 council sitting. The five decisions in
      § Orchestrator Decisions are flagged for veto; D5 (the collision check) is
      the one the proposal itself names as most worth vetoing, and D1's
      capability split is the one a seat is most likely to want re-argued.
- [ ] 1.2 Route the five open questions OQ-1..OQ-5. OQ-4 in particular is a
      routing question the council can settle in one line: one sweep with
      per-packet consent, or one task per owning packet.
- [ ] 1.3 Brett ratifies or reverses. On ratification, amend `proposal.md`'s
      `Status:` to `ratified` and add the `Ratified:` line in the sanctioned
      record-citing spelling, there being no approving OpenSpec change to name.
- [ ] 1.4 Record the sitting under `review/` with `Status: record` (or
      `Status: ratified` plus a citation where the record IS the ratification),
      per `document-lifecycle`'s "Proposal packets carry the lifecycle header".

## 2. Speckit F1 — the `Modified over` marker and the pairing class

One feature: the parser change and the emit are one mechanism and cannot land
apart, because a marker form the parser does not recognize is a body unit and a
pairing class that cannot read a marker reports every declared pair.

- [ ] 2.1 Extend the marker parser with the third reserved form. Recognized only
      where, after the family's normalization, the paragraph BEGINS with the
      prefix COMPLETE: the bold run, a code-spanned resolvable change id, the
      fixed `'s addition by`, a resolvable change id, an ISO date in
      parentheses, and the closing colon. The anchor is load-bearing for the
      same reason it is on the other two forms: this packet's own delta text and
      `document-lifecycle`'s both set the template out in prose and both promote.
      **THE `by` IDENTIFIER IS RECOGNIZED AS RESOLVABLE AND VALIDATED AS EQUAL TO
      THE CARRIER, and the two steps stay apart on purpose.** `document-lifecycle`
      requires that identifier to BE the change whose delta carries the block, so
      RECOGNITION keeps the resolvability test above — a marker whose `by` names
      another change is still a marker of this form — and 2.5 REPORTS the
      inequality as the misdeclared state. Folding the equality into recognition
      would drop such a paragraph back to a body unit and report the block as
      UNDECLARED, naming the absent-marker remedy for a block that carries one.
- [ ] 2.2 Make the form name NO units. It suppresses nothing, is never a
      candidate for the marker-defect check, and — like the other two forms — is
      excluded from unit derivation in canon and in the block, so it is not a
      carriage unit in either direction. **AND ITS REASON IS THE WHOLE TAIL
      AFTER ` — `**, harvested without extracting code spans as names: the
      `Removed from canon`/`Merged into` path takes the reason from after the
      LAST code span, and reusing it here would read a code span an author wrote
      INSIDE the reason as a named unit and shorten the reason to nothing. The
      disclosure 2.5's fourth state reads lives in that reason, so the two are
      one mechanism and this note is a precondition of that state working at
      all.
- [ ] 2.3 Widen `sibling_titles` to carry the ADDING CHANGE ID and ITS DECLARED
      STANDING beside each `(capability, title)`. The bare title set it returns
      today cannot name a pairing in a finding and cannot see the
      self-referential state, because it does not exclude the reading change from
      its own sources; and it cannot see the UNDISCLOSED state, because the
      adding change's standing is never read at all — `active_blocks` skips a
      change that carries no MODIFIED block, which every pure adder is. Read it
      through `_standing`, the module's existing `corpus.parse_status` ->
      `promotion_fidelity.declared_standing` path, never a private regex.
- [ ] 2.4 Replace the `if status == "pending": continue` drop with the pairing
      emit. THE THREE COMPARISON ARMS STILL DO NOT RUN against a pending block;
      the 2026-08-27 ruling is untouched and the change is that the block is no
      longer dropped before anything looks at it.
- [ ] 2.5 Report exactly four states — self-referential, undeclared,
      misdeclared, undisclosed — and emit NOTHING for a declared, resolving
      pair whose `by` identifier is the carrying change and whose basis is
      `ratified` OR whose marker discloses that it is not.
      **CLASSIFY IN THAT ORDER AND EMIT EXACTLY ONE STATE PER BLOCK.** The
      self-addition condition is examined FIRST and EXCLUDES the block from every
      state below it, because it is a fact about the delta rather than about the
      marker: without the order a self-referential block carrying no marker
      satisfies UNDECLARED as well, and the run emits two findings with two
      remedies for one defect. Each state's own antecedent carries the exclusion
      the order performs, so the branch and the delta text say the same thing.
      MISDECLARED CARRIES TWO HALVES AND ONE ACTION: the named basis neither ADDS
      nor RENAMES to the title, OR the `by` identifier is not the change carrying
      the block — the second read by comparing the identifier the parser already
      recognized (2.1) against the block's own change id, which is why a right
      basis under a wrong author cannot pass as DECLARED AND RESOLVING. The
      finding SHALL say which half it names.
      UNDISCLOSED NARROWS THE SILENT STATE — its antecedent is that state's plus
      two conditions, so it reaches only a block otherwise in good order (basis
      real, `by` equal to the carrier) and restates no defect the other three
      name. It reads the reason clause for the word `document-lifecycle`
      reserves, and it is why that capability's disclosure obligation has an
      enforcer at all.
- [ ] 2.6 Register ONE `_ArmTemplate` for the class, carrying all four states —
      and MISDECLARED's two halves inside its own — in one interpolated `why`
      clause on the `TEMPLATE_UNRESOLVED` precedent, and append it to
      `_ARM_TEMPLATES`. One template is one shape is one map
      entry; a rule text not rendered from a registered template has no shape the
      unplaced-drift mask can compute and is reported as drift on every run. The
      two halves differ only in that interpolated clause, so they stay ONE shape
      and add no entry — the `by`-mismatch wording goes in the `why`, never in
      the fixed prose the mask reads.
- [ ] 2.7 Register the `FindingClass` in `CLASSES`, with its own severity and
      action constants named apart from `_LAUNCH_SEVERITY`, and insert it BEFORE
      the `unplaced` class so both standing ordering claims stay true: the
      gate-bearing arm reads first, the drift class reads last.
- [ ] 2.8 Add the anchored `_CLASS_PATTERNS` entry. Verify the negative first:
      with the template registered and the pattern absent, the fifth class fires
      and names the new rule text — that is the fifth class working, and it is a
      test worth keeping rather than a step to skip.
- [ ] 2.9 Fixtures, one per reported state plus BOTH silent ones — a `ratified`
      basis, and an unratified basis whose marker discloses it — and the
      regression fixture reconstructing the corpus's own four-pair shape.
      MISDECLARED NEEDS BOTH ITS HALVES: a marker naming a basis that adds
      nothing, and a marker whose basis is right and whose `by` names another
      change — the second being the false-provenance case, which without the
      comparison passes as DECLARED AND RESOLVING and is the one fixture that
      fails on the pre-fix classifier. EXCLUSIVITY NEEDS ITS OWN: a
      self-referential block carrying NO marker, asserted to emit ONE finding in
      that state and no undeclared one beside it. The
      unratified pair needs its own adding-change fixture carrying a non-ratified
      `Status:`, the standing being read from the adder's proposal header.
- [ ] 2.10 Move the standing pins by name, one at a time: the class-registry
      pin, the rule-shapes pin, the verbatim class-row list, the
      last-row assertions, the `len(block)` pin, and the FR-023 severity
      snapshot. Nothing else.
- [ ] 2.11 Self-gate. `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
      no longer covers the new class; add a NAMED EXACT SET for its standing
      subjects under `_LEDGER_SUBJECTS`'s movement discipline, each row carrying
      its own retirement condition — the row retires when its declaring block
      carries a marker or its adding sibling archives. A row discharged by a
      DISPOSITION rather than by a marker is not a retirement: the entry is the
      exception § 6.4 bounds, and it carries its own retirement (requirement
      grain, retired when the basis archives) rather than resolving the row.
      **UNDER D4's SEQUENCING THE SET LAUNCHES EMPTY**, § 6 having discharged all four before this
      feature lands, and an empty exact set with a positive control is the same
      shape § 3.3 asks of the collision class. Where the order taken was the
      other one, the set launches with the four.
- [ ] 2.12 Amend `specs/022-modified-block-currency-reporting/contracts/report-section.md`.
      It is byte-level and enumerates the classes four times over; a class that
      landed without touching it would leave a false contract in the corpus.
- [ ] 2.13 Amend `docs/doc-health.md`'s family paragraph, which today names
      three arms, a marker-defect class and a fifth `unplaced` class.

## 3. Speckit F2 — the ADDED-over-canon collision class

Separate feature because D5 is separately vetoable and this is the whole of what
a veto would strike.

- [ ] 3.1 Read active `## ADDED Requirements` blocks against the promoted index
      the family already builds, and report a title canon already carries.
- [ ] 3.2 Its own template, its own `FindingClass`, its own anchored pattern,
      its own action line naming both remedies. Same registration discipline as
      2.6-2.8.
- [ ] 3.3 A zero assertion on the real tree WITH A POSITIVE CONTROL. A class
      whose population is zero and whose only test asserts zero is a class no
      test proves exists.
- [ ] 3.4 Fixture: the unsafe archive order, reconstructed — the modifying
      change archived, the requirement in canon, the adding change still active
      and still holding its ADDED block.

## 4. Evidence recorded at proposal time

- [ ] 4.1 The population, RE-STATED AT THE CATCH-UP MERGE of 2026-08-31 whose
      `main`-side parent is `7f656980` and RE-READ UNCHANGED at the SECOND
      catch-up merge of the same day, whose `main`-side parent is `9af98c4d`
      (the `main` tip after #530, #509, #513 and #524): 20 active MODIFIED
      blocks, 16 `canon`,
      4 `pending`; all four adding siblings `ratified`; zero markers; the
      proposal cross-reference present in 4 of 4 and over-broad by two to three
      unrelated active change ids in each. **THE UNDISCLOSED STATE'S LAUNCH
      POPULATION IS ZERO BY THAT SAME READ**: all four bases are `ratified`, so
      no marker the § 6 sweep writes owes the disclosure and the fourth state
      moves neither figure § 8.1 reads. The PENDING SET IS UNCHANGED from the
      19/15/4 read at `91cf0a46` — the twentieth block is
      `add-structured-scope-substrate`'s over `release-realization`'s
      "Realization axis declaration", a different requirement of the same spec,
      resolving `canon`. Recorded in `proposal.md` § Why.
- [ ] 4.2 BOTH of this packet's own MODIFIED blocks read ZERO. The
      `release-realization` block resolves `canon`, and the title arm and the
      carriage ledger report nothing against it — both promoted body sentences
      and both promoted scenarios restated byte-identical, everything added new.
      The `doc-health` block over "A modified-block-currency finding its own
      class map cannot place is itself a finding" also resolves `canon`: of that
      requirement's 35 promoted units (10 body sentences, 6 scenario titles, 19
      scenario bullets) THIRTY-THREE are restated byte-identical and TWO are
      declared by one `Removed from canon by` marker naming each as a code span
      — the `FAMILY_RESOLUTION`-absence sentence and the last bullet of "The
      class map grows the pattern the drift named". Measured with the family's
      own `suppression`: 2 units suppressed, 0 defective markers, 0 title and 0
      ledger findings — RE-DERIVED after the round-4 rewrite of the block's
      operative text (the map-extension citation removed, the prohibition and
      its scenario added): canon still 35 units, the block's own units 45 -> 56
      (body 16 -> 23, scenario titles 7 -> 8, scenario bullets 22 -> 25), the
      SAME two units missing and the SAME two suppressed by the SAME single
      marker, 0 defective. All three arms still read zero, the rewrite having
      touched only text canon does not carry. Re-run BOTH at every catch-up
      merge; canon moving under either block is exactly the defect the family
      exists to catch and this packet is not exempt from it.
      RE-RUN AT BOTH 2026-08-31 CATCH-UP MERGES, the second against `9af98c4d`:
      that merge moved nothing under either block — `openspec/specs/` is
      byte-identical between `7f656980` and `9af98c4d` — and canon still carries the
      `release-realization` requirement at
      `openspec/specs/release-realization/spec.md:64-78` and the `doc-health`
      one at `openspec/specs/doc-health/spec.md:2055-2126`, both unmoved, both
      blocks still resolve `canon`, and a `--single-repo --family
      modified-block-currency` run over the branch tree emits 8 findings, none of
      them against either of this packet's delta paths — the same 8, re-measured
      after the second merge.
- [ ] 4.3 The collision class's population is zero on this tree: no active ADDED
      block names a title the promoted specification carries.
- [ ] 4.4 The `family-enumeration` gate stays green: no family is registered, so
      the "Deterministic check families" enumeration and its numerals are
      untouched and unrestated.
- [ ] 4.5 THE CANON/CODE CONTRADICTION IS CLOSED BY THIS PACKET RATHER THAN
      NAMED BY IT. `scripts/doc_health/families.py:117` carries
      `"modified-block-currency": CONTESTED` since `7f656980` (PR #529,
      2026-08-31); that landing amended no specification, so promoted canon read
      "The family SHALL remain absent from `FAMILY_RESOLUTION`"
      (`openspec/specs/doc-health/spec.md:2088`) with a MUST resting on the
      absence at `:2126`. The `doc-health` MODIFIED block supersedes both units,
      cites the landing, and answers their protective intent BY MEASUREMENT
      rather than by re-seating it: `report.uncited_resolutions` keys on
      `(family, repository, path)` and `_drift_findings` builds the
      unplaced-class finding from the repo and path of the finding it NAMES,
      which survives a map extension under that same key — so the map extension
      endangers the protection not at all and owes no citation. The block
      instead FORBIDS the extending act to record a disposition, which
      `promotion_fidelity.disposed` would apply before the block resolves and
      which would hide the surviving finding. **NOT the pairing case**: a
      pairing finding sits on a `pending` block whose arms do not run, so its
      key vanishes outright when the marker lands (§ 6.4's grain and retirement
      stand unchanged). No code moves: the row and `_LAUNCH_SEVERITY` stay where
      #529 put them.
- [ ] 4.6 THE THIRD `FAMILY_RESOLUTION` MENTION IS LEFT STANDING ON PURPOSE.
      Canon names the table three times. `:2088` and `:2126` are superseded
      (4.5); `:1726` is not, and the reason is in the promoted text: it sits
      under "This family SHALL be advisory AT LAUNCH" in a paragraph that
      RESERVES its own reversal as "ONE later decision taken together by ruling",
      which is exactly what `7f656980` took, together and on a measured
      population of zero. A launch state a requirement provides for leaving is
      SPENT rather than contradicted. Superseding it anyway would mean restating
      a ~290-line requirement with 14 scenarios — the cost D2 measured and
      declined. A seat may reverse this and ask for that block.

## 5. Population measurement — the aggregation read

- [ ] 5.1 After F1 lands, read the next NIGHTLY AGGREGATION report and record
      the pairing class's count PER REPOSITORY across the submodules that carry
      `openspec/changes/`. This packet measures openxFactory and predicts
      nothing about the rest.
- [ ] 5.2 Record the count in this packet before archive. A large population
      elsewhere is a reason to revisit D4's band BEFORE the flip is proposed,
      not after — and a reason to route the discharge to owners rather than to
      one sweep.
- [ ] 5.3 Do not open per-repository issues from that read without a ruling. The
      remedy is one marker paragraph per block and the owners are the packets'
      authors, not this change.

## 6. Discharging the standing population

- [ ] 6.1 Subject to OQ-4's routing: add one `Modified over` marker to each of
      the four live pairs — `add-binding-consumer-identity`,
      `add-wallet-carried-review-authority`, `implement-keycloak-install-repo`,
      `implement-openxpki-install-repo`. NONE of the four owes the unratified
      disclosure: every one of the four bases is `ratified` (§ 4.1). Re-read the
      four standings at the moment the sweep is written rather than trusting this
      line — a base whose standing has moved owes the word, and the sweep is the
      cheapest place to notice.
- [ ] 6.2 Each is a RATIFIED packet, so each marker is an amendment to a
      ratified proposal and takes that route, with the packet's owner consenting
      to the edit. A marker is not a carriage unit, so adding one changes what no
      later block must restate. `add-binding-consumer-identity`'s own § 7.4
      obliges its carriage diff to be RE-RUN whenever its MODIFIED block is
      touched; a marker does not move that diff's answer, and the re-run is its
      packet's discipline rather than this one's exemption.
- [ ] 6.3 `add-wallet-carried-review-authority` additionally carries a
      MIS-CITATION in its delta preamble — it quotes the already-modified
      antecedent and calls the scenario a MUST. Correct it to cite the extended
      antecedent this change adds, once ratified.
- [ ] 6.4 Do NOT disposition any of the four IN PLACE OF a marker. The remedy is
      one paragraph, and a disposition standing in for it is the shape D4 exists
      to avoid. **NARROWED, NOT LIFTED, by the `FAMILY_RESOLUTION` row that
      landed on 2026-08-31**: because this family is now `contested`, a finding
      of the new class that VANISHES owes a citation under the
      uncited-resolution rule. Sequencing § 6 ahead of § 2 means no finding is
      ever emitted for these four and no citation is owed for them; where that
      sequencing is unavailable elsewhere, the act that adds the marker records
      the citation in the same act, and that is the rule's requirement rather
      than a way around it. **AND THE ENTRY IS BOUNDED, in grain and in time.**
      `promotion_fidelity.disposed` runs BEFORE the block is resolved and matches
      family/repo/path with an optional REQUIREMENT narrowing and no finding-class
      grain, so an entry recorded for a pairing finding also silences the three
      comparison arms over that block — after the basis archives included, which
      is the first moment those arms can read it at all. So: record the entry at
      REQUIREMENT grain, and RETIRE it when the basis archives. The retirement is
      the ARCHIVING change's act, evidenced at its own archive gate, and the
      MODIFYING change's archive gate confirms that no such entry stands over its
      block. See D4.
- [ ] 6.5 SEQUENCE THIS SECTION BEFORE § 2. § 6 is a PRECONDITION of the F1
      feature, not a follow-up to it: the class must launch at a population of
      zero, on the discipline every predecessor family in this group observed
      before joining `FAMILY_RESOLUTION`. **THIS IS THE ROUTE AND THE CITATION IS
      THE EXCEPTION**, in that order and not as two equal options — the delta
      states them ordered, because the exception costs a disposition that
      suppresses more than the finding it answers (6.4) and this route costs
      nothing at all. Adding a marker before the parser recognizes the form is
      mechanically safe — an unrecognized `Modified over` paragraph reads as one
      dated bold note, an extra body unit, and the carriage arms report only
      units canon carries that a block LACKS.
- [ ] 6.6 `add-notebook-hosting-credential-custody` owes an amendment its
      MARKER SWEEP PARTNER cannot make for it: its fifth ADDED scenario, "The
      published binding shape cannot yet express the access identity", was
      FALSIFIED by `contract-v2.4` — the published schema now carries
      `consumer:` with `holder_ref` and `fetch_identity`
      (`contracts/schemas/xfactory-credential-contracts.schema.yaml:185-229`;
      `contracts/CHANGELOG.md` § `contract-v2.4 — 2026-08-31`). Under the
      falsified-scenario clause the ADDING change amends it BEFORE it archives,
      with its owner consenting per 6.2. Archiving it unamended in the chain
      order would promote a scenario the repository's own published schema
      contradicts. THIS PACKET OBLIGES THE AMENDMENT AND DOES NOT PERFORM IT;
      it is a post-ratification act on a ratified packet.

## 7. Open — recorded, not fixed

- [ ] 7.1 OQ-1, the post-archive detector for the MODIFIED writer's own delta.
      Owner: unassigned. Trigger: the first observed unsafe archive order, or a
      ruling. On this corpus's precedent it is a different document pair and
      therefore a different family.
- [ ] 7.2 OQ-2, whether a `Modified over` marker survives promotion.
- [ ] 7.3 OQ-3, two or more active changes adding one title. Population zero.
- [ ] 7.4 The band flip for both new classes is RESERVED and not proposed here;
      it follows the discharge of § 6 and is one ruling. It is NO LONGER paired
      with "whether the family joins `FAMILY_RESOLUTION`" — the family joined on
      2026-08-31 (§ 7.5), the table has no per-class grain, and both new classes
      are `contested` from their first emit whatever band they carry. What the
      flip still decides is the band alone.
- [ ] 7.5 `add-modified-block-currency-check` § 7.2 — the scenario-title arm's
      own reserved flip — is SPENT, not owed: it landed at `7f656980` (PR #529,
      2026-08-31) on a measured population of zero everywhere, moving
      `_LAUNCH_SEVERITY` to `error` AND adding the family's `FAMILY_RESOLUTION`
      row. Its second half is what § 7.4 and D4 have to reckon with rather than
      reserve. **THE CODE IS UNTOUCHED BY THIS PACKET AND THE CANON IS NOT**:
      #529 amended no specification, so promoted `doc-health` still asserted the
      family's ABSENCE from that table at
      `openspec/specs/doc-health/spec.md:2088` with a scenario resting a MUST on
      it at `:2126`. This packet's `doc-health` MODIFIED block supersedes both
      and cites `7f656980` as the landing — canon catching up with a row the code
      already carries (§ 4.5). Nothing further is owed to #529 by this packet:
      its row, its severity move and its tests stay exactly as it landed them.
- [ ] 7.6 #318 stays open. This packet is once again the shape it describes:
      an `ad_hoc` origin whose approval covers the decision to file and not the
      content, recorded as such in `.openspec.yaml`.

## 8. Archive

- [ ] 8.1 Archive only on merged-and-green realization evidence:
      `python3 -m pytest tests/doc-health` green,
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a
      doc-health single-repo run whose severity counts move in the `warning`
      line ALONE and by the amount THE ORDER ACTUALLY TAKEN predicts:
      `0 warning` where § 6 was sequenced first as D4 asks and the standing pairs
      are declared before the class runs, `+4 warning` where the class landed
      against the population undischarged. Both figures already account for the
      UNDISCLOSED state, which contributes zero either way, all four bases being
      `ratified`. Record which order was taken; a run whose movement matches
      NEITHER figure is the finding, not the gate.
- [ ] 8.2 On archive, the change MAY state `Closes #502`. It does not close it
      before then, and the proposal says so in § Standing.
- [ ] 8.3 Confirm at the archive gate that BOTH of this packet's own MODIFIED
      blocks still read zero against canon (§ 4.2), each having been live for as
      long as the packet was. The `doc-health` block is the one to read twice:
      its subject requirement is in the same specification this change also ADDS
      to, so a hand-edit anywhere in that file is the likeliest way its carriage
      goes stale.
