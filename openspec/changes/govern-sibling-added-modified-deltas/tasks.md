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
- [ ] 2.2 Make the form name NO units. It suppresses nothing, is never a
      candidate for the marker-defect check, and — like the other two forms — is
      excluded from unit derivation in canon and in the block, so it is not a
      carriage unit in either direction.
- [ ] 2.3 Widen `sibling_titles` to carry the ADDING CHANGE ID beside each
      `(capability, title)`. The bare title set it returns today cannot name a
      pairing in a finding and cannot see the self-referential state, because it
      does not exclude the reading change from its own sources.
- [ ] 2.4 Replace the `if status == "pending": continue` drop with the pairing
      emit. THE THREE COMPARISON ARMS STILL DO NOT RUN against a pending block;
      the 2026-08-27 ruling is untouched and the change is that the block is no
      longer dropped before anything looks at it.
- [ ] 2.5 Report exactly three states — undeclared, misdeclared,
      self-referential — and emit NOTHING for a declared, resolving pair.
- [ ] 2.6 Register ONE `_ArmTemplate` for the class, carrying all three states
      in one interpolated `why` clause on the `TEMPLATE_UNRESOLVED` precedent,
      and append it to `_ARM_TEMPLATES`. One template is one shape is one map
      entry; a rule text not rendered from a registered template has no shape the
      unplaced-drift mask can compute and is reported as drift on every run.
- [ ] 2.7 Register the `FindingClass` in `CLASSES`, with its own severity and
      action constants named apart from `_LAUNCH_SEVERITY`, and insert it BEFORE
      the `unplaced` class so both standing ordering claims stay true: the
      gate-bearing arm reads first, the drift class reads last.
- [ ] 2.8 Add the anchored `_CLASS_PATTERNS` entry. Verify the negative first:
      with the template registered and the pattern absent, the fifth class fires
      and names the new rule text — that is the fifth class working, and it is a
      test worth keeping rather than a step to skip.
- [ ] 2.9 Fixtures, one per reported state plus the silent one, and the
      regression fixture reconstructing the corpus's own four-pair shape.
- [ ] 2.10 Move the standing pins by name, one at a time: the class-registry
      pin, the rule-shapes pin, the verbatim class-row list, the
      last-row assertions, the `len(block)` pin, and the FR-023 severity
      snapshot. Nothing else.
- [ ] 2.11 Self-gate. `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
      no longer covers the new class; add a NAMED EXACT SET for its standing
      subjects under `_LEDGER_SUBJECTS`'s movement discipline, each row carrying
      its own retirement condition — the row retires when its declaring block
      carries a marker or its adding sibling archives. **UNDER D4's SEQUENCING
      THE SET LAUNCHES EMPTY**, § 6 having discharged all four before this
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
      `main`-side parent is `7f656980`: 20 active MODIFIED blocks, 16 `canon`,
      4 `pending`; all four adding siblings `ratified`; zero markers; the
      proposal cross-reference present in 4 of 4 and over-broad by two to three
      unrelated active change ids in each. The PENDING SET IS UNCHANGED from the
      19/15/4 read at `91cf0a46` — the twentieth block is
      `add-structured-scope-substrate`'s over `release-realization`'s
      "Realization axis declaration", a different requirement of the same spec,
      resolving `canon`. Recorded in `proposal.md` § Why.
- [ ] 4.2 This packet's own delta reads ZERO. Its `release-realization` block
      resolves `canon`, and the title arm and the carriage ledger report nothing
      against it — both promoted body sentences and both promoted scenarios
      restated byte-identical, everything added new. Re-run this at every
      catch-up merge; canon moving under this block is exactly the defect the
      family exists to catch and this packet is not exempt from it.
      RE-RUN AT THE 2026-08-31 CATCH-UP MERGE: canon still carries the requirement
      at `openspec/specs/release-realization/spec.md:64-78` unmoved, the block
      still resolves `canon`, and a `--single-repo --family
      modified-block-currency` run over the branch tree emits 8 findings, none of
      them against this packet's delta path.
- [ ] 4.3 The collision class's population is zero on this tree: no active ADDED
      block names a title the promoted specification carries.
- [ ] 4.4 The `family-enumeration` gate stays green: no family is registered, so
      the "Deterministic check families" enumeration and its numerals are
      untouched and unrestated.

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
      `implement-openxpki-install-repo`.
- [ ] 6.2 Each is a RATIFIED packet, so each marker is an amendment to a
      ratified proposal and takes that route, with the packet's owner consenting
      to the edit. A marker is not a carriage unit, so adding one changes what no
      later block must restate.
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
      than a way around it. See D4.
- [ ] 6.5 SEQUENCE THIS SECTION BEFORE § 2. § 6 is a PRECONDITION of the F1
      feature, not a follow-up to it: the class must launch at a population of
      zero, on the discipline every predecessor family in this group observed
      before joining `FAMILY_RESOLUTION`. Adding a marker before the parser
      recognizes the form is mechanically safe — an unrecognized `Modified over`
      paragraph reads as one dated bold note, an extra body unit, and the
      carriage arms report only units canon carries that a block LACKS.

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
      row. It is untouched by this packet, and its second half is what § 7.4 and
      D4 now have to reckon with rather than reserve.
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
      against the population undischarged. Record which order was taken; a run
      whose movement matches NEITHER figure is the finding, not the gate.
- [ ] 8.2 On archive, the change MAY state `Closes #502`. It does not close it
      before then, and the proposal says so in § Standing.
- [ ] 8.3 Confirm at the archive gate that this packet's own MODIFIED block
      still reads zero against canon (§ 4.2), the block having been live for as
      long as the packet was.
