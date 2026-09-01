# Tasks — govern-sibling-added-modified-deltas

**This change is RATIFIED** (2026-08-31, Brett Heap, by direct ruling —
`review/ratification-2026-08-31.md`). §1 carries the ratification and its two
non-ticking boxes, disposed there rather than closed. **Nothing else has moved**:
§2 and §3 are the two unbuilt Speckit features, §6 is a post-ratification sweep
across four ratified packets that this act does not perform, §7 records five open
questions the ruling did not reach, and §8's archive gate is untouched.

**UPDATED 2026-08-31 — §6 HAS SINCE BEEN PERFORMED, by a separate
post-ratification act and not by the ratification described above, whose account
of itself is left exactly as written.** Brett Heap routed the proposal's OQ-4 as
(a), ONE SWEEP, in session on 2026-08-31 and consented to all five ratified-packet
edits
that sweep makes; it wrote the four `Modified over` markers, fixed the §6.3
mis-citation, struck the falsified scenario §6.6 names, and re-measured the
carriage claim that strike made stale. §6 is now ticked box by box with its
evidence. §2, §3, §7 and §8 are unmoved.

House rule: **OpenSpec ratifies, Speckit builds.** Each `## Speckit F<n>` group
below maps to exactly ONE Speckit feature and is the handoff unit; nothing in
this file is an executable task list for a session to work directly. Groups 1,
4, 5, 6, 7 and 8 are governance bookkeeping and belong to this packet.

## 1. Ratification

**RATIFIED 2026-08-31 BY DIRECT RULING** — Brett Heap, in session via an explicit
multi-choice put, verbatim *"Direct — accept D1–D5 (Recommended)"*; record
`review/ratification-2026-08-31.md`. **The §7.4 sitting this section prescribed
DID NOT SIT.** Each box below therefore carries its MEASURED disposition, and two
of the four do not tick: a box that says "put it to a sitting" cannot be ticked by
a ratification that declined one, and ticking it would put a sitting in the record
that never happened.

- [ ] 1.1 **DECLINED BY THE RATIFYING AUTHORITY, NOT SKIPPED — and therefore
      NOT TICKED as written.** The choice between convening a §7.4 sitting and
      ratifying the converged packet directly was put to Brett Heap in session as
      an explicit multi-choice, and he took the direct path; the sitting was never
      convened and no seat sat. **What this box asked for was nonetheless
      ANSWERED**: all five decisions in § Orchestrator Decisions were accepted AS
      DRAFTED at tip `3d776c67`, D5 and D1 included — the two the box named as
      most likely to be re-argued. See `review/ratification-2026-08-31.md`
      § "The path taken, and the path declined".
- [ ] 1.2 **NOTHING TO ROUTE, AND THEREFORE NOT TICKED.** OQ-1..OQ-5 REMAIN OPEN.
      They were routed to the sitting of 1.1, which did not sit, and the direct
      ruling reached the five DECISIONS without reaching the five QUESTIONS — so
      they stand exactly as `proposal.md` § Open questions leaves them and travel
      with § 7 below. OQ-4's one-line routing of the § 6 sweep is unruled, so § 6
      stands as staged (per-packet consent) rather than re-routed per owner.
      **UPDATED 2026-08-31, AND STILL NOT TICKED.** OQ-4 HAS SINCE BEEN RULED,
      separately from the ratification this box describes: Brett Heap routed it in
      session on 2026-08-31 as **(a), ONE SWEEP**, and the sweep has run. OQ-1,
      OQ-2, OQ-3 and OQ-5 remain open and travel with §7 and §5 exactly as this
      box leaves them. THE BOX STILL DOES NOT TICK, because what it says did not
      happen — the sitting that would have routed all five — still did not
      happen; one question later answered by a different act does not make the
      sentence about the sitting true.
- [x] 1.3 **DONE in the ratification commit.** `proposal.md` front matter carries
      `Status: ratified` plus the `Ratified:` line in the sanctioned
      record-citing spelling — approver, date and a resolvable record path, all
      three of `sanction-ratified-record-spelling`'s floor rather than the one it
      needs — there being no approving OpenSpec change to name. § Standing,
      § Orchestrator Decisions' preamble, § Open questions' preamble,
      `.openspec.yaml`'s `approved_by` and the README active-changes row were
      swept in the same act, on the rule that any edit changing what the packet
      asserts about itself owes a sweep of every site asserting the same thing.
- [x] 1.4 **DONE — `review/ratification-2026-08-31.md`**, carrying
      `Status: ratified` plus a citation, which is the branch of this box that
      applies: the record IS the ratification, so `Status: record` would understate
      the claim it makes, and `document-lifecycle`'s "A review record records a
      ratification" scenario requires the ratified spelling with a citation. It
      records the ruling and its channel, the declining of the sitting, the D1–D5
      acceptance, the OQ dispositions, the nine-round convergence evidence, the
      pre-given merge word, and what the ratification does NOT do.

## 2. Speckit F1 — the `Modified over` marker and the pairing class

One feature: the parser change and the emit are one mechanism and cannot land
apart, because a marker form the parser does not recognize is a body unit and a
pairing class that cannot read a marker reports every declared pair.

- [x] 2.1 Extend the marker parser with the third reserved form. Recognized only
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
      **AND RECOGNITION ENDS AT THE CLOSING COLON — THE ` — <reason>` TAIL IS NO
      PART OF IT**, on that same split and for that same consequence.
      `document-lifecycle` REQUIRES the tail and 2.5's FOURTH misdeclared ground
      VALIDATES it; recognition tests it nowhere. A paragraph carrying the
      complete prefix and nothing after it is a MARKER OF THIS FORM whose
      declaration is defective, and reading it as a non-marker would return it to
      the body units and report the block UNDECLARED — again the absent-marker
      remedy for a block that carries one, and again the wrong paragraph named
      for repair.
- [x] 2.2 Make the form name NO units. It suppresses nothing, is never a
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
      **HARVEST ALWAYS AND VALIDATE — NEVER HARVEST OPTIONALLY.** The tail is
      read off EVERY recognized marker of this form, and where there is no ` — `
      separator, or one with nothing but whitespace after it, the harvest yields
      NO REASON rather than declining: an absent reason is a VALUE 2.5 reports on
      its fourth misdeclared ground, not a parse outcome and not a silence. The
      other two forms may carry a reason or not, their declarations being
      complete in the UNITS THEY NAME; this one names none, so a marker without a
      reason declares a bare pairing — and, the disclosure living in that same
      tail, discloses nothing and can disclose nothing.
- [x] 2.3 Widen `sibling_titles` to carry the BASIS CHANGE ID, ITS DECLARED
      STANDING, and WHICH BLOCK PUT THE TITLE THERE — an `## ADDED Requirements`
      block or a `## RENAMED Requirements` block's `TO:` half — beside each
      `(capability, title)`. The bare title set it returns
      today cannot name a pairing in a finding and cannot see the
      self-referential state, because it does not exclude the reading change from
      its own sources; and it cannot see the UNDISCLOSED state, because the
      basis change's standing is never read at all — `active_blocks` skips a
      change that carries no MODIFIED block, which a pure adder or a pure renamer
      is. Read it
      through `_standing`, the module's existing `corpus.parse_status` ->
      `promotion_fidelity.declared_standing` path, never a private regex.
      **THE ADDED/RENAMED DISCRIMINATOR IS NOT DECORATION**: 2.5's
      self-referential state is the carrier's own ADDITION alone, so the set has
      to be able to say whether the carrier's own entry came from an addition or
      from a rename's `TO:` half. The set's TITLE CONTENT is unchanged — both
      forms still make a title `pending`, exactly as the promoted rule reads "a
      requirement an active sibling change ADDS or RENAMES".
- [x] 2.4 Replace the `if status == "pending": continue` drop with the pairing
      emit. THE THREE COMPARISON ARMS STILL DO NOT RUN against a pending block;
      the 2026-08-27 ruling is untouched and the change is that the block is no
      longer dropped before anything looks at it. **`resolve()` IS NOT TOUCHED,
      AND ITS SECOND STEP IS WHY.** Its order is canon's
      (`openspec/specs/doc-health/spec.md:1568-1574`): canon, then the carrying
      change's OWN `## RENAMED Requirements` block — which returns `own-rename`
      with a real basis so the three arms RUN against canon under the OLD name
      (`:1783-1786`) — and only THEN `pending`. The emit replaces the `pending`
      branch alone, so the rename-and-amend shape never reaches the new class and
      the precedence survives without being restated in the classifier.
- [x] 2.5 Report exactly four states — self-referential, undeclared,
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
      **CLASSIFY FROM THE BLOCK'S WHOLE MARKER SET AND READ ITS COUNT FIRST.**
      `derive_units` preserves every recognized marker in `block.markers`, so the
      classifier is handed a LIST and must never reason about "the marker": a
      block carrying one valid pairing marker and one naming a change that adds
      nothing satisfies MISDECLARED and the silent state at once, and which one a
      run reported would be decided by iteration order. `document-lifecycle`
      bounds the set at AT MOST ONE marker of this form per block, so the checks
      run self-addition, then COUNT, then the single marker's basis, its `by`,
      ITS REASON and
      its disclosure — the silent state and UNDISCLOSED reached only where
      EXACTLY ONE pairing marker stands and passes every check above, every other
      block placed by the FIRST check it fails.
      **READ THE CONDITION FROM THE CARRIER'S OWN `## ADDED Requirements` BLOCK
      AND FROM NOTHING ELSE** — this is what 2.3's discriminator is for. A
      carrier's own RENAME to the title is NOT this state: it is the
      rename-and-amend shape promoted canon resolves against the OLD name one
      step before `pending` (2.4), so reading it here would either report the
      supported shape or, where `resolve()` had already claimed it, sit as a
      branch no input can reach.
      MISDECLARED CARRIES FOUR GROUNDS AND ONE ACTION: the block carries MORE
      THAN ONE pairing marker — read FIRST, so a block carrying a good marker and
      a bad one is placed by a fact about the block rather than by which marker
      the loop reached; OR the named basis is not an
      active change OTHER THAN THE CARRIER that ADDS or RENAMES to the title —
      it names a change that does neither, or it names the carrier itself — OR the
      `by` identifier is not the change carrying
      the block — read by comparing the identifier the parser already
      recognized (2.1) against the block's own change id, which is why a right
      basis under a wrong author cannot pass as DECLARED AND RESOLVING — OR the
      marker CARRIES NO REASON, the required ` — <reason>` tail absent or empty,
      which without this ground reaches DECLARED AND RESOLVING and promotes a
      declaration `document-lifecycle` calls incomplete as a complete one.
      **THE THREE SINGLE-MARKER GROUNDS ARE READ basis, then `by`, THEN REASON,
      AND THE REASON MUST PRECEDE THE DISCLOSURE.** The disclosure is a WORD
      LOOKED FOR IN THE REASON CLAUSE, so a marker with no clause offers it
      nothing to look in: read the other way an unratified basis under a
      prefix-only marker would be reported UNDISCLOSED and told to add a word to
      a sentence that does not exist, while the identical marker over a RATIFIED
      basis passed in silence — the same defect named two ways at two titles and
      unnamed at one of them. Reading both would emit two findings for one
      missing tail, which the exactly-one-state rule forbids. **THE
      BASIS GROUND IS WRITTEN AS THE EXACT NEGATION of the silent state's basis
      clause**, so that narrowing self-reference to the carrier's own addition
      leaves no block outside all five states and the exhaustiveness claim stays
      true by construction rather than by inspection. The
      finding SHALL say which ground it names.
      UNDISCLOSED NARROWS THE SILENT STATE — its antecedent is that state's plus
      two conditions, so it reaches only a block otherwise in good order (basis
      real, `by` equal to the carrier) and restates no defect the other three
      name. It reads the reason clause for the word `document-lifecycle`
      reserves, and it is why that capability's disclosure obligation has an
      enforcer at all.
- [x] 2.6 Register ONE `_ArmTemplate` for the class, carrying all four states —
      and MISDECLARED's four grounds inside its own — in one interpolated `why`
      clause on the `TEMPLATE_UNRESOLVED` precedent, and append it to
      `_ARM_TEMPLATES`. One template is one shape is one map
      entry; a rule text not rendered from a registered template has no shape the
      unplaced-drift mask can compute and is reported as drift on every run. The
      four grounds differ only in that interpolated clause, so they stay ONE shape
      and add no entry — the `by`-mismatch wording goes in the `why`, never in
      the fixed prose the mask reads, and so do the marker COUNT, the basis
      ground's THIRD reading,
      a marker naming the carrier itself, and the ABSENT REASON, each being the
      same state under the same
      action and none to be given fixed prose of its own. The count belongs in an
      INTERPOLATED field for the same reason every other number this family
      reports does: fixed prose carrying a numeral is a shape the mask cannot
      strip, and a two-marker block and a three-marker one would then read as two
      remedies.
- [x] 2.7 Register the `FindingClass` in `CLASSES`, with its own severity and
      action constants named apart from `_LAUNCH_SEVERITY`, and insert it BEFORE
      the `unplaced` class so both standing ordering claims stay true: the
      gate-bearing arm reads first, the drift class reads last.
- [x] 2.8 Add the anchored `_CLASS_PATTERNS` entry. Verify the negative first:
      with the template registered and the pattern absent, the fifth class fires
      and names the new rule text — that is the fifth class working, and it is a
      test worth keeping rather than a step to skip.
- [x] 2.9 Fixtures, one per reported state plus BOTH silent ones — a `ratified`
      basis, and an unratified basis whose marker discloses it — and the
      regression fixture reconstructing the corpus's own four-pair shape.
      MISDECLARED NEEDS ALL THREE OF ITS GROUNDS: a marker naming a basis that adds
      nothing; a marker whose basis is right and whose `by` names another
      change — the false-provenance case, which without the
      comparison passes as DECLARED AND RESOLVING and is the one fixture that
      fails on the pre-fix classifier; and a block carrying TWO pairing markers,
      ONE OF THEM VALID and the other naming a change that adds nothing, asserted
      to emit exactly ONE finding on the count ground — the fixture that fails a
      classifier reasoning about a singular marker, which would report it or clear
      it according to which marker it reached, and whose PAIR is an otherwise
      identical block carrying the valid marker alone, asserted silent; and, on
      the FOURTH ground, a marker whose basis and `by` are both right over a
      RATIFIED basis and which carries the complete prefix and NO ` — ` separator
      at all, asserted MISDECLARED on the reason ground and NOT silent — the
      fixture that fails a classifier recognizing the prefix and validating no
      tail — with an EMPTY-REASON TWIN carrying the separator and nothing but
      whitespace after it, asserted identically, an empty reason declaring what an
      absent one does. **AND THE ORDER NEEDS ITS OWN**: the same prefix-only
      marker over an UNRATIFIED basis, asserted to emit exactly ONE finding, in
      the misdeclared state on the reason ground and NOT undisclosed — the fixture
      that fails a classifier reading the disclosure before the reason, which
      would name a missing word where the tail is what is missing.
      EXCLUSIVITY NEEDS ITS OWN: a
      self-referential block carrying NO marker, asserted to emit ONE finding in
      that state and no undeclared one beside it. **THE OWN-RENAME CARVE NEEDS
      TWO**: a rename-and-amend fixture — a change whose `## RENAMED
      Requirements` block renames a PROMOTED requirement to the title it also
      MODIFIES — asserted to emit NOTHING of this class and to have the three
      arms compare it against canon under the OLD name, which is the promoted
      behaviour this round refuses to displace; and a marker naming the CARRIER
      ITSELF as basis over a block that is not self-referential, asserted
      MISDECLARED rather than silent, which is the exhaustiveness hole the
      narrowing would otherwise open. The
      unratified pair needs its own adding-change fixture carrying a non-ratified
      `Status:`, the standing being read from the adder's proposal header.
- [x] 2.10 Move the standing pins by name, one at a time: the class-registry
      pin, the rule-shapes pin, the verbatim class-row list, the
      last-row assertions, the `len(block)` pin, and the FR-023 severity
      snapshot. Nothing else.
- [x] 2.11 Self-gate. `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree`
      no longer covers the new class; add a NAMED EXACT SET for its standing
      subjects under `_LEDGER_SUBJECTS`'s movement discipline, each row carrying
      its own retirement condition — the row retires when its declaring block
      carries a marker or its adding sibling archives. A row discharged by a
      DISPOSITION rather than by a marker is not a retirement: the entry is the
      exception § 6.4 bounds, and it carries its own availability bound and its own
      retirement (recordable only where no second ratified change writes the
      title, requirement grain, retired when the basis archives) rather than
      resolving the row.
      **UNDER D4's SEQUENCING THE SET LAUNCHES EMPTY**, § 6 having discharged all four before this
      feature lands, and an empty exact set with a positive control is the same
      shape § 3.3 asks of the collision class. Where the order taken was the
      other one, the set launches with the four.
- [x] 2.12 Amend `specs/022-modified-block-currency-reporting/contracts/report-section.md`.
      It is byte-level and enumerates the classes four times over; a class that
      landed without touching it would leave a false contract in the corpus.
- [x] 2.13 Amend `docs/doc-health.md`'s family paragraph, which today names
      three arms, a marker-defect class and a fifth `unplaced` class.

## 3. Speckit F2 — the ADDED-over-canon collision class

Separate feature because D5 is separately vetoable and this is the whole of what
a veto would strike.

- [x] 3.1 Read active `## ADDED Requirements` blocks AND the `TO:` titles of
      active `## RENAMED Requirements` blocks against the promoted index
      the family already builds, and report a title canon already carries. **READ
      THE `TO:` HALF AND NEVER THE `FROM:` HALF**: a rename's source is a title
      canon is expected to carry, so reading it would report every lawful rename
      in the corpus, while its target is the collision shape — the same surviving
      evidence an unpromoted addition leaves, reached through the other basis
      form. `promotion_fidelity.parse_delta` already returns the `(FROM, TO)`
      pairs the family reads for `resolve()`, so this is a second use of one
      parse rather than a second parser.
- [x] 3.2 Its own template, its own `FindingClass`, its own anchored pattern,
      its own action line naming both remedies. Same registration discipline as
      2.6-2.8.
- [x] 3.3 A zero assertion on the real tree WITH A POSITIVE CONTROL. A class
      whose population is zero and whose only test asserts zero is a class no
      test proves exists.
- [x] 3.4 Fixture: the unsafe archive order, reconstructed — the modifying
      change archived, the requirement in canon, the basis change still active
      and still holding its ADDED block. **AND ITS RENAME TWIN**: the same
      reconstruction with the basis change holding a `## RENAMED Requirements`
      block whose `TO:` title canon now carries, asserted to report in the same
      class, plus a NEGATIVE control — a lawful rename whose `FROM:` title canon
      carries and whose `TO:` title it does not — asserted silent.

## 4. Evidence recorded at proposal time

- [x] 4.1 The population, RE-STATED AT THE CATCH-UP MERGE of 2026-08-31 whose
      `main`-side parent is `7f656980` and RE-READ UNCHANGED at the SECOND
      catch-up merge of the same day, whose `main`-side parent is `9af98c4d`
      (the `main` tip after #530, #509, #513 and #524): 20 active MODIFIED
      blocks, 16 `canon`,
      4 `pending`; all four adding siblings `ratified`; zero markers; the
      proposal cross-reference present in 4 of 4 and over-broad by two to three
      unrelated active change ids in each. **AND THE REASON GROUND'S LAUNCH
      POPULATION IS ZERO BY AN EMPTY SET**: the
      same read finds ZERO markers of this form anywhere on the tree, § 6's sweep
      not having run, so no marker can be missing its tail and the ground reaches
      nothing at launch. It moves neither figure § 8.1 reads, and the four markers
      § 6.1 writes are authored under the rule rather than measured against it.
      **THE UNDISCLOSED STATE'S LAUNCH
      POPULATION IS ZERO BY THAT SAME READ**: all four bases are `ratified`, so
      no marker the § 6 sweep writes owes the disclosure and the fourth state
      moves neither figure § 8.1 reads. **AND THE ARCHIVE HOLD'S WIDENING TO
      UNRATIFIED BASES HOLDS NOTHING TODAY, BY THAT SAME READ**: the four bases
      resolve `ratified` through the family's own `_standing`, so ZERO live
      pending pair is held by the widening and the case it reaches is
      prospective. Re-measure the four standings at every catch-up merge — a base
      whose standing MOVES puts its pair inside the widened hold, which is the
      one input this measurement exists to catch. The PENDING SET IS UNCHANGED
      from the 19/15/4 read at `91cf0a46` — the twentieth block is
      `add-structured-scope-substrate`'s over `release-realization`'s
      "Realization axis declaration", a different requirement of the same spec,
      resolving `canon`. Recorded in `proposal.md` § Why.
      **RE-MEASURED AT THE F1+F2 BUILD, 2026-09-01, over `main` at `1c1dcbbe`,
      AND THE FIGURES ABOVE ARE HISTORY.** 20 active MODIFIED blocks, **17
      `canon` and 3 `pending`** — not 16/4 — and BOTH movements are acts this
      packet's own § 6 and a peer lane took after the measurement above was
      written. (i) `add-binding-consumer-identity` over
      `add-notebook-hosting-credential-custody` LEFT the pending set: PR #541
      archived both on 2026-08-31 in the SAFE order, so the requirement is
      promoted and the block resolves `canon`. (ii) The remaining THREE —
      `add-wallet-carried-review-authority`,
      `implement-keycloak-install-repo` and `implement-openxpki-install-repo` —
      each now carry ONE `Modified over` marker, written by § 6's sweep at
      `3a6a16e9` (PR #538, 2026-08-31), each naming a basis that adds the title,
      each carrying the carrying change's own id as its `by` identifier and a
      nonempty reason, over a `ratified` basis. **SO THE PAIRING CLASS LAUNCHES
      AT A POPULATION OF ZERO — D4's ROUTE 1, PERFORMED — AND ITS EXACT SET IN
      THE SELF-GATE LAUNCHES EMPTY WITH A POSITIVE CONTROL** (§ 2.11's
      D4-sequencing branch, not its fallback). The three declarations are read
      back through the family's own parser, which is what makes the sweep's
      markers evidence that the form as authored is the form as recognized
      rather than two spellings that happen to coexist. Zero markers of this
      form remain anywhere on the tree that the check would report.
- [x] 4.2 BOTH of this packet's own MODIFIED blocks read ZERO. The
      `release-realization` block resolves `canon`, and the title arm and the
      carriage ledger report nothing against it — both promoted body sentences
      and both promoted scenarios restated byte-identical, everything added new.
      **RE-DERIVED AFTER THE ROUND-5 WIDENING TO RENAMES**, which moved this
      block's text and no other's: canon still 8 units (2 body sentences, 2
      scenario titles, 4 scenario bullets); the block's own units 40 -> 52 (body
      17 -> 23, scenario titles 6 -> 7, scenario bullets 17 -> 22); ZERO
      uncarried canon units, ZERO suppressed, ZERO markers, ZERO defective — all
      three arms still read zero, the widening having touched only text canon
      does not carry. The `doc-health` MODIFIED block was NOT touched by that
      round (the round's `doc-health` edits are all inside the two ADDED
      requirements), and its measurement below is re-confirmed unchanged at 56
      block units and the same two suppressed.
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
      RE-CONFIRMED AFTER THE ROUND-6 EDITS, which are again ALL inside the two
      `doc-health` ADDED requirements and `document-lifecycle`'s ADDED one —
      neither MODIFIED block was touched, and both re-read at exactly the figures
      above: `release-realization` 8 canon units, 52 block units, 0 markers, 0
      suppressed, 0 defective; `doc-health` 35 canon units, 56 block units, 1
      marker, the SAME 2 suppressed, 0 defective; 0 title, 0 ledger and 0
      marker-defect findings against either path.
      **RE-DERIVED AFTER THE ROUND-7 WIDENING OF THE ARCHIVE HOLD**, which again
      moved the `release-realization` block's text and no other's: canon still 8
      units (2 body sentences, 2 scenario titles, 4 scenario bullets); the
      block's own units 52 -> 64 (body 23 -> 30, scenario titles 7 -> 8, scenario
      bullets 22 -> 26); ZERO uncarried canon units, ZERO suppressed, ZERO
      markers, ZERO defective — all three arms still read zero, the widening
      having touched only text canon does not carry. The `doc-health` block was
      NOT touched by that round either (its edits are inside the two ADDED
      requirements), and it re-reads at exactly 56 block units, 1 marker, the
      SAME 2 suppressed and 0 defective.
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
      **RE-RUN AT THE F1+F2 BUILD, 2026-09-01, WITH BOTH NEW CLASSES LIVE.**
      Over `main` at `1c1dcbbe` the family emits 8 findings, all
      `carriage-ledger`, and NONE of them names either of this packet's delta
      paths; both blocks still resolve `canon`. The count moved from 7 to 8 for
      a reason that has nothing to do with this packet — `add-chain-attestation`
      landed a new MODIFIED block on `main` — and neither new class touches
      either figure: the pairing class reads 0 and the collision class reads 0.
- [x] 4.3 The collision class's population is zero on this tree ACROSS BOTH
      BASIS FORMS, re-measured after the class was widened to renames: of 159
      active `## ADDED Requirements` blocks, NONE names a capability and
      requirement title the promoted specification already carries; and this
      repository carries ZERO active `## RENAMED Requirements` pairs, so the
      `TO:` half's population is zero by an empty set rather than by a passing
      comparison. Measured with `promotion_fidelity.parse_delta` and the family's
      own `promoted()` index over the branch tree. Re-run at every catch-up
      merge: a rename landing in some other active packet is exactly the input
      this widening exists for.
      **RE-RUN AT THE F1+F2 BUILD, 2026-09-01, THROUGH THE BUILT CLASS ITSELF
      RATHER THAN THROUGH A SPIKE.** Over `main` at `1c1dcbbe` the collision
      class emits ZERO, across both basis forms, and the self-gate asserts that
      zero WITH A POSITIVE CONTROL (§ 3.3): the control feeds the corpus's own
      active additions to the family's own emit against a promoted index that
      DOES carry one of their titles, and the class fires — so the zero is a
      zero the class could have moved off.
- [x] 4.4 The `family-enumeration` gate stays green: no family is registered, so
      the "Deterministic check families" enumeration and its numerals are
      untouched and unrestated.
      **CONFIRMED AT THE F1+F2 BUILD**: `tests/doc-health/test_family_enumeration.py`
      is green and `scripts/doc_health/families.py` is untouched — the two new
      classes are classes of an EXISTING family, so `FAMILIES`,
      `FAMILY_SUMMARIES`, `FAMILY_NOTES` and `FAMILY_RESOLUTION` all read
      exactly what they read on `main`.
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

- [x] 6.1 Subject to OQ-4's routing: add ONE `Modified over` marker — one, and
      never a second — to each of
      the four live pairs — `add-binding-consumer-identity`,
      `add-wallet-carried-review-authority`, `implement-keycloak-install-repo`,
      `implement-openxpki-install-repo`. NONE of the four owes the unratified
      disclosure: every one of the four bases is `ratified` (§ 4.1). Re-read the
      four standings at the moment the sweep is written rather than trusting this
      line — a base whose standing has moved owes the word AND puts that pair's
      modifying change under the archive hold until the base ratifies and
      archives, and the sweep is the cheapest place to notice.
      **DONE 2026-08-31 — OQ-4 ROUTED AS (a), ONE SWEEP, BY THE OWNER'S RULING.**
      Brett Heap ruled the routing in session on 2026-08-31 and his consent covers
      all five ratified-packet edits this sweep makes; the routing and the consent
      are recorded in the carrying commit, in the pull request body, and in each
      tick of this section. FOUR MARKERS WRITTEN, one per pair, each one paragraph
      inside its MODIFIED block after the body and before the first
      `#### Scenario:`, each naming its basis as a code span and its own carrying
      change bare after `by`, each carrying a nonempty ` — ` tail free of code
      spans:
      `openspec/changes/add-binding-consumer-identity/specs/credential-contracts/spec.md`
      (basis `add-notebook-hosting-credential-custody`),
      `openspec/changes/add-wallet-carried-review-authority/specs/roles-authority-model/spec.md`
      (basis `add-substantive-review-lane`),
      `openspec/changes/implement-keycloak-install-repo/specs/repo-boundary-governance/spec.md`
      (basis `add-identity-brokering`),
      `openspec/changes/implement-openxpki-install-repo/specs/repo-boundary-governance/spec.md`
      (basis `add-trust-anchor`).
      **THE FOUR STANDINGS WERE RE-READ AT THE TIP THE SWEEP WAS WRITTEN AGAINST**,
      as this box orders, rather than trusted from § 4.1 — `main` at `8f986c39`:
      `add-notebook-hosting-credential-custody` `Status: ratified`
      (`proposal.md:8`), `add-substantive-review-lane` `Status: ratified`
      (`proposal.md:8`), `add-identity-brokering` `Status: ratified`
      (`proposal.md:4`), `add-trust-anchor` `Status: ratified`
      (`proposal.md:4`). ALL FOUR STILL `ratified`, NONE MOVED, so no marker owes
      the unratified disclosure, none carries the word, and no pair enters the
      widened archive hold. Writing the word into any of the four would have been
      a defect rather than caution.
- [x] 6.2 Each is a RATIFIED packet, so each marker is an amendment to a
      ratified proposal and takes that route, with the packet's owner consenting
      to the edit. A marker is not a carriage unit, so adding one changes what no
      later block must restate. `add-binding-consumer-identity`'s own § 7.4
      obliges its carriage diff to be RE-RUN whenever its MODIFIED block is
      touched; a marker does not move that diff's answer, and the re-run is its
      packet's discipline rather than this one's exemption.
      **ROUTE TAKEN 2026-08-31: THE IN-PLACE DATED AMENDMENT WITH THE OWNER
      CONSENTING**, the route this corpus already uses for a ratified document
      (precedent `openspec/specs/ideation-dashboard/spec.md:1870`, "(AMENDED
      2026-08-15, Brett: …)"). Brett Heap, the ratifying owner of all five edited
      packets, consented in session on 2026-08-31 in the same ruling that routed
      OQ-4 as one sweep. NO SECOND NOTE IS WRITTEN BESIDE ANY OF THE FOUR MARKERS:
      a marker of this form IS a dated declaring paragraph, so a companion
      amendment note would be a second paragraph declaring what the first already
      declares. The three NON-MARKER edits (§ 6.3, § 6.6, and the re-measurement
      the § 6.6 strike forces on `add-binding-consumer-identity`'s preamble) each
      carry their own dated note naming the consenting owner.
      `add-binding-consumer-identity`'s § 7.4 carriage re-run IS OWED AT ITS OWN
      ARCHIVE GATE and is NOT discharged here — this act records the
      re-measurement its edit occasioned (five basis scenarios, all five restated
      byte-identical, the sixth now an addition), which is evidence for that
      re-run and not a substitute for it.
- [x] 6.3 `add-wallet-carried-review-authority` additionally carries a
      MIS-CITATION in its delta preamble — it quotes the already-modified
      antecedent and calls the scenario a MUST. Correct it to cite the extended
      antecedent this change adds, once ratified.
      **FIXED 2026-08-31, in place and dated, with the owner consenting.**
      BEFORE, at `openspec/changes/add-wallet-carried-review-authority/specs/roles-authority-model/spec.md:3-12`:
      the preamble declared its deltas relative to `add-substantive-review-lane`
      "per `openspec/specs/release-realization/spec.md:64-74`" — quoting the
      ALREADY-MODIFIED antecedent verbatim — "with the scenario 'Two changes touch
      one requirement' making it a MUST". BOTH halves mis-cited: that antecedent
      names a requirement canon CARRIES, its scenario is written for a proposal
      modifying a requirement an active ratified change ALREADY MODIFIES, and
      `add-substantive-review-lane` ADDS this requirement to a title the promoted
      specification does not carry at all. AFTER: the same paragraph with that
      citation removed, followed by a dated `**CORRECTED 2026-08-31**` note that
      names the mis-citation in both halves and cites the EXTENDED antecedent —
      the paragraph "THE ANTECEDENT REACHES A REQUIREMENT AN ACTIVE RATIFIED
      CHANGE ADDS OR RENAMES TO, AND NOT ONLY ONE IT MODIFIES" and its scenario
      "A proposal modifies a requirement an active ratified change adds or renames
      to" — at
      `openspec/changes/govern-sibling-added-modified-deltas/specs/release-realization/spec.md`,
      **stated in the note as RATIFIED (2026-08-31, direct ruling) AND NOT YET
      CANON** and cited at that change-directory path precisely because these
      deltas promote only at this packet's own archive. `openspec/specs/` is not
      cited for it and MUST NOT be until this packet archives.
      `add-binding-consumer-identity`'s preamble is NOT touched on this ground: it
      already carries the corrected reading at its LA-A3 sentence.
- [x] 6.4 Do NOT disposition any of the four IN PLACE OF a marker. The remedy is
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
      is the first moment those arms can read it at all — AND, where the
      two-writers ordering arm has a subject at that title, the ordering finding
      over that same block, that arm running BEFORE resolution and filtered
      through the same read. So: record the entry ONLY where no active change
      other than the block's own carrier, whose standing is `ratified`, writes a
      MODIFIED block for that same capability and requirement title — the arm
      being armed by a COUNT of ratified writers and returning nothing below two
      of them, so that an admissible state is one in which it has nothing it
      could emit; at REQUIREMENT grain; and RETIRE it when the basis archives. The
      retirement is
      the ARCHIVING change's act, evidenced at its own archive gate, and the
      MODIFYING change's archive gate confirms that no such entry stands over its
      block. The population of the availability bound is ZERO on this tree: no
      capability-and-requirement title carries more than one active MODIFIED block
      at all. See D4.
      **OBSERVED 2026-08-31, AND THIS BOX IS A PROHIBITION THE ACT COMPLIED WITH
      rather than a unit of work it performed.** NO DISPOSITION WAS RECORDED FOR
      ANY OF THE FOUR — not in `health/dispositions.yaml`, not anywhere else — and
      the remedy taken for each of the four was the one paragraph this section
      names. THE CITATION LIMB IS MOOT ON THIS TREE AND NOT WAIVED: § 6 ran BEFORE
      § 2, F1 is unbuilt, so no finding of the new class has ever been emitted for
      these four and no uncited-resolution citation is owed for any of them. The
      availability bound is untested for the same reason and its measured
      population stays ZERO: no capability-and-requirement title on this tree
      carries more than one active MODIFIED block, so no entry could have been
      recorded even had the exception been taken.
- [x] 6.5 SEQUENCE THIS SECTION BEFORE § 2. § 6 is a PRECONDITION of the F1
      feature, not a follow-up to it: the class must launch at a population of
      zero, on the discipline every predecessor family in this group observed
      before joining `FAMILY_RESOLUTION`. **THIS IS THE ROUTE AND THE CITATION IS
      THE EXCEPTION**, in that order and not as two equal options — the delta
      states them ordered, because the exception costs a disposition that
      suppresses more than the finding it answers (6.4), is UNAVAILABLE OUTRIGHT
      wherever a second ratified change writes the same title, and this route
      costs nothing at all and is available everywhere.
      Adding a marker before the parser recognizes the form is
      mechanically safe — an unrecognized `Modified over` paragraph reads as one
      dated bold note, an extra body unit, and the carriage arms report only
      units canon carries that a block LACKS.
      **THE ROUTE WAS TAKEN, NOT THE EXCEPTION — 2026-08-31.** § 6 is discharged
      by this act and § 2 IS UNBUILT: F1 does not exist, no parser recognizes the
      `Modified over` form yet, and the class therefore launches, whenever it
      launches, at a population of ZERO standing undeclared pairs. The four
      markers were written under the rule rather than measured against it, exactly
      as § 4.1 anticipates. **§ 8.1's FIGURE NOTE, recorded here because this run
      is an input that box reads**: the order actually taken is § 6 FIRST, which is
      the `0 warning` figure — and this run moves NEITHER figure, because F1 is
      unbuilt and no check of either new class exists to emit anything. The
      `+4 warning` figure is now unreachable for these four pairs by construction.
- [x] 6.6 `add-notebook-hosting-credential-custody` owes an amendment its
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
      **PERFORMED 2026-08-31 BY THE POST-RATIFICATION SWEEP THIS SECTION
      DESCRIBES, AS A STRIKE AND NOT A RE-SCOPE.** The scenario was REMOVED from
      `openspec/changes/add-notebook-hosting-credential-custody/specs/credential-contracts/spec.md`
      and a dated in-place amendment note stands in its place, carrying its
      AUTHORITY (Brett Heap, ratifying owner, consenting per § 6.2, ruled
      2026-08-31), its GROUND (the falsified-scenario clause of this packet's
      `release-realization` delta, cited at the change-directory path and stated
      to be ratified-but-unpromoted), its EVIDENCE
      (`contracts/schemas/xfactory-credential-contracts.schema.yaml:185-229`;
      `contracts/CHANGELOG.md` § `contract-v2.4 — 2026-08-31`), the SUCCESSOR that
      discharged the gap (`add-binding-consumer-identity`, PR #516 squash
      `5e8a33cf`, cut `contract-v2.4` PR #526 `afdf0e88`, tag published), and the
      statement that THE ARCHIVE ORDER IS UNCHANGED. Re-scoping was refused
      deliberately: every clause of the scenario is falsified by the release, so a
      narrowing would leave a smaller false statement, and the surviving truth is
      already carried by the successor's replacement scenario. NOTHING ELSE IN THE
      BLOCK WAS TOUCHED — verified by measurement rather than asserted: the block's
      four body paragraphs are byte-unchanged, and its five surviving scenarios
      are byte-identical to the five `add-binding-consumer-identity` restates, so
      that packet's byte-identity claim survives the strike with its COUNT
      corrected from six to five. The amendment note begins `**AMENDED 2026-08-31`
      and carries NO reserved prefix — not `Modified over`, not `Removed from
      canon by`, not `Merged into` — so it cannot be read as a carriage marker.

## 7. Open — recorded, not fixed

- [ ] 7.1 OQ-1, the post-archive detector for the MODIFIED writer's own delta.
      Owner: unassigned. Trigger: the first observed unsafe archive order, or a
      ruling. On this corpus's precedent it is a different document pair and
      therefore a different family.
- [ ] 7.2 OQ-2, whether a `Modified over` marker survives promotion.
- [ ] 7.3 OQ-3, two or more active changes writing one title, by addition or
      by rename. Population zero in both forms (§ 4.3).
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
      `ratified` — for the REASON GROUND, which adds a ground to an existing
      state rather than a class and whose launch population is zero by an empty
      marker set (§ 4.1) — and for the archive hold's widening to unratified
      bases, which
      adds no class and no check and so contributes to no band. Record which
      order was taken; a run whose movement matches NEITHER figure is the
      finding, not the gate.
- [ ] 8.2 On archive, the change MAY state `Closes #502`. It does not close it
      before then, and the proposal says so in § Standing.
- [ ] 8.3 Confirm at the archive gate that BOTH of this packet's own MODIFIED
      blocks still read zero against canon (§ 4.2), each having been live for as
      long as the packet was. The `doc-health` block is the one to read twice:
      its subject requirement is in the same specification this change also ADDS
      to, so a hand-edit anywhere in that file is the likeliest way its carriage
      goes stale.
