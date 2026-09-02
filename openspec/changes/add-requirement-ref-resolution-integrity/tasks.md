# Tasks: add-requirement-ref-resolution-integrity

Governance-level and dependency-ordered. **This change is RATIFIED** (2026-09-01,
Brett Heap, by direct ruling — `review/ratification-2026-09-01.md`). § 1 was
authored in this pull request; **§ 2 CARRIES THE RATIFICATION and its dispositions,
two of its four boxes disposed rather than closed**; § 3 onward are for the
implementer and belong to a separate realization pull request, on the pattern this
packet's own subject set established (proposal PR #497, realization PR #516).

**NOTHING ELSE HAS MOVED.** § 3 – § 6 are the unbuilt realization slice, § 7's
verification gates are untouched, § 8's archive gate is untouched, and § 9 records
what this change deliberately does not close. Ratification authorizes realization
and performs none of it.

**ONE POST-RATIFICATION AMENDMENT HAS SINCE LANDED, BY THE RATIFYING OWNER'S OWN
CONSENT — 2026-09-01, and it is the ONLY movement of normative text after
ratification.** Brett Heap ruled the third Codex round's P2 in session
`openxfactory-f5`, by an explicit multi-choice put with the contradiction before
him: **SCOPE TO PER-DOCUMENT.** The delta's ambiguity requirement and scenario
NARROW to the ambiguity the frozen resolver can actually see — more than one
record carrying the id INSIDE THE ONE REQUIREMENTS DOCUMENT the reference names —
and the CROSS-DOCUMENT arm is FILED AS THE NAMED SUCCESSOR, **openxFactory issue
#553**. So § 9.4 is RULED rather than routed-open, § 3.4's freeze now AGREES with
the scenario instead of contradicting it, and § 2.5 records the act. **The
scenario count is UNCHANGED at TWELVE** — the ambiguity scenario was NARROWED and
retitled, never struck — **and AD-1's two-code ruling is untouched.** What moved
is SCOPE and nothing else.

Evidence convention, unchanged from the family's standard: a box closes on a
FACT that survives the session — a merged commit, a green run named by id, a
file path, a command and its output — never on an intention.

## 1. The packet (THIS PULL REQUEST)

- [x] 1.1 `credential-contracts` — **TWO ADDED requirements over TWELVE
      SCENARIOS**: the per-binding reporting duty (six scenarios, one of them the
      falsifiable reproduction), and the own-code-family phasing rule (six
      scenarios). **THE COUNT SURVIVES THE 2026-09-01 AMENDMENT** (§ 2.5): the
      ambiguity scenario was NARROWED to per-document and RETITLED, not struck,
      so TWELVE still holds and no site asserting it has to move.
- [x] 1.2 **NO `## MODIFIED Requirements` block anywhere in this packet**, and
      the choice is MEASURED rather than preferred. The two requirements a
      reconciling MODIFIED block would have named — *"A credential binding
      declares the consuming system that holds it and the identity it fetches
      with"* and *"Two bindings on one secret are refused unless every pair
      declares distinct consumers…"* — are carried by NO promoted specification
      (`openspec/specs/credential-contracts/spec.md` holds seven titles, neither
      of them these) and are ADDED by the then-ACTIVE, ratified, unarchived
      `add-binding-consumer-identity`. A MODIFIED block over either would then
      have been exactly the shape `govern-sibling-added-modified-deltas` governs:
      a ``**Modified over `<basis>`'s addition by <change-id> (<date>):**``
      marker plus an ARCHIVE-ORDER HOLD behind the sibling. A pure ADDED
      requirement serves, so this packet takes it, carries no marker and imposes
      no hold.
      **RE-MEASURED 2026-09-01, AFTER THE CATCH-UP MERGE OF `origin/main`
      `1c1dcbbe`, AND THE BOX STILL TICKS.** PR #541 ARCHIVED
      `add-binding-consumer-identity` on 2026-08-31 (basis-first, with
      `add-notebook-hosting-credential-custody`), so the promoted spec now carries
      TWELVE titles and BOTH of the two named above ARE among them (`:278` and
      `:440`). A MODIFIED block over either would now be an ORDINARY block over
      promoted canon — no marker, no hold, the basis having archived. **The
      CHOICE is unchanged and only its REASON moved**: an all-ADDED delta served
      before because it avoided a marker and a hold, and serves now because the
      reporting duty is still a duty this capability states nowhere. Neither
      ADDED title collides with the twelve promoted ones — checked, not assumed.
      Both measurements are recorded in proposal.md § The sibling rule, measured
      and in `review/ratification-2026-09-01.md` § The catch-up merge.
- [x] 1.3 The reproduction is IN the packet as a falsifiable scenario
      (*"The shipped check is silent on both of them today"*), not only as
      prose in § What was measured — so a later reader can re-run it against
      whatever the validator has become.
- [x] 1.4 `.openspec.yaml` — `kind: ad_hoc`, origin id
      `openxFactory:adhoc:2026-08-31-add-requirement-ref-resolution-integrity`,
      `reason` naming issue #523 and the PR #516 review thread, `approved_by`
      recording Brett Heap's 2026-08-30 ruling AS A DECISION TO FILE and
      explicitly NOT as a ratification of content, `approved_on: 2026-08-30`.
- [x] 1.5 README "OpenSpec Records" active entry, stating the defect, the
      reproduction, the code-versus-narrowing choice as the ruling recorded it,
      the all-ADDED shape and the draft posture.
- [x] 1.6 `OPENSPEC_TELEMETRY=0 openspec validate
      add-requirement-ref-resolution-integrity --strict` and `--all --strict`
      both green.
- [x] 1.7 `python3 -m pytest tests/doc-health -q` green, and a same-clock
      doc-health run against an `origin/main` baseline in an identically named
      directory shows ZERO NEW FINDINGS. Docs-only, so the suite's pinned skip
      count MUST NOT move.
- [x] 1.8 § Authoring decisions AD-1 … AD-6 and § Open questions OQ-1 … OQ-4
      are stated as the AUTHORING SESSION'S and are flagged for veto. None is
      presented as ruled.
- [x] 1.9 **The Codex round on PR #542, both findings repaired in the packet.**
      (a) The reproduction's Control A claimed a ONE-BYTE edit over
      `example-secret-one` -> `example-secret-two`, which is THREE bytes. The
      reproduction was REBUILT on `example-secret-a` / `example-secret-b` and
      RE-RUN against `scripts/validate-credential-contracts.py` at this branch's
      merge-base; the templates are now the same length and differ at one offset,
      the recorded outputs are that run's, and the delta scenario *"The shipped
      check is silent on both of them today"* states the single-byte spacing in
      its WHEN so the claim is checkable rather than asserted; § What was
      measured § 6 now carries BOTH REPRODUCTION FILES IN FULL, so the run is
      re-executable from this packet alone rather than from a description of a
      tree nobody kept. (b) AD-1 offered a one-code branch that struck ONE
      scenario while the delta still obliged "NAMED APART" and the tasks and
      `code_surface` still bought two codes — a packet that would have ratified a
      permission and a prohibition together. AD-1 now carries the COMPLETE
      twelve-item AD-1/ONE-CODE AMENDMENT SET, and § 2.2 and § 3.3 point at it.
      The recommendation stands UNCHANGED at TWO codes.

## 2. Ratification — DONE 2026-09-01, BY DIRECT RULING

**RATIFIED 2026-09-01 BY DIRECT RULING** — Brett Heap (repository owner), in
session via an explicit multi-choice put, session `openxfactory-f5`; record
`review/ratification-2026-09-01.md`. **AD-1 IS RULED TWO CODES, AS DRAFTED**, and
the twelve-item AD-1/ONE-CODE AMENDMENT SET is DECLINED — none of its items
executed, and it is left standing in the proposal rather than struck. **NO §7.4
SITTING WAS CONVENED**, § 2.3 having left that question to Brett rather than
prescribing one. Each box below therefore carries its MEASURED disposition, and
TWO OF THE FOUR DO NOT TICK: a box that routes every open question to a ruling
cannot be ticked by a ruling that reached the decisions and not the questions, and
a box that puts a live question cannot be ticked by the act that answered it.

- [x] 2.1 **DONE.** Brett Heap read the packet and ruled: RATIFY, by direct
      ruling of the repository owner, over tip `deb72c8e`. Ratification authorizes
      REALIZATION and performs none of it; `proposal.md` now carries
      `Status: ratified` with the record-citing `Ratified:` line, and § 3 onward
      may start in a SEPARATE pull request.
- [ ] 2.2 **PARTLY ANSWERED, AND THEREFORE NOT TICKED.** This box asks for TWO
      things and got one. **THE AD SIDE IS DISCHARGED IN FULL**: AD-1 is RULED
      TWO CODES — the decision the box names as "the one that changes the spec
      text" — and AD-2 … AD-6 stand ACCEPTED AS DRAFTED. The box's own prediction
      held exactly: the ruling took ONE SENTENCE and executed as ZERO EDITS,
      because the one-code branch was enumerated as a mechanical amendment set,
      so no delta requiring two codes was ever left standing beside a ruling
      permitting one. **THE OQ SIDE IS NOT**: OQ-1 … OQ-4 received neither a
      ruling nor an explicit defer. They REMAIN OPEN exactly as
      `proposal.md` § Open questions leaves them, each with its recommendation
      and no decision, and they travel with § 4, § 9.1 and § 9.2. Ticking this
      box would assert four dispositions that were never taken.
- [ ] 2.3 **ANSWERED, NOT PERFORMED — AND THEREFORE NOT TICKED.** This box put a
      QUESTION rather than an obligation: whether to convene a §7.4-shaped sitting
      was Brett's call and was not assumed. **HE TOOK THE DIRECT PATH.** No
      sitting was convened, no seat sat, no ballot was cast, and nothing in this
      packet may be cited as a council disposition. The box named the
      `govern-sibling-added-modified-deltas` precedent as the nearer one and it
      was: that packet was ratified 2026-08-31 by direct ruling with the sitting
      it had PRESCRIBED for itself declined, and this one never prescribed a
      sitting at all. The box's `review/` condition is honoured in its own terms —
      the directory was created only when there was a record to put in it, and
      what it holds is a RATIFICATION record, not a sitting record. A box asking
      "shall we convene?" cannot be ticked by the answer "no".
- [x] 2.4 **DONE in the ratification commit.** `proposal.md` carries
      `Status: ratified` plus the RECORD-CITING `Ratified:` spelling — the branch
      of this box that applies, there being no approving OpenSpec change to name,
      so `Ratified by:` would mean naming a change that does not exist; the
      citation names an approver, a date AND a resolvable record path, all three
      of the three-way floor rather than the one it needs. The record is
      `review/ratification-2026-09-01.md`. Swept in the SAME commit, on the rule
      that any edit changing what a packet asserts about itself owes a sweep of
      every site asserting the same thing: `proposal.md`'s new § Standing, its
      § Authoring decisions preamble, AD-1's heading and its amendment-set
      heading, § The sibling rule measured, § Impact's sibling states,
      `.openspec.yaml`'s `approved_by` and three `related:` rows, this file's
      header and § 1.2, and the README active-changes entry.
- [x] 2.5 **THE POST-RATIFICATION CONSENTED AMENDMENT — DONE 2026-09-01. Same
      day, same ratifier, SEPARATE ACT.** The third Codex round's P2 was ROUTED
      OPEN by the ratification (§ 9.4 as first written). Brett Heap then ruled it
      in session `openxfactory-f5` by an explicit multi-choice put, with the
      contradiction stated in full rather than summarised: the packet was already
      `Status: ratified`, and its ambiguity scenario AS RATIFIED reached ACROSS
      requirements documents while `resolve_requirement` — frozen by § 3.4 —
      matches only inside the ONE document a reference names, so that arm was
      UNMEETABLE by this packet's own realization. **RULED: SCOPE TO
      PER-DOCUMENT; the cross-document arm FILED AS A NAMED SUCCESSOR,
      openxFactory issue #553.** Because the packet was ratified, this is a
      **CONSENTED AMENDMENT BY THE RATIFYING OWNER HIMSELF**, not an edit to
      ratified text by anybody else, and the consent is recorded AT EVERY TOUCHED
      SITE: two dated `**AMENDED 2026-09-01**` notes in
      `specs/credential-contracts/spec.md`, a dated addendum in
      `review/ratification-2026-09-01.md`, this file's header and § 1.1, § 3.4,
      § 9.4, `proposal.md`'s `code_surface`, § Standing, § What was measured § 4,
      § What this changes, § The sibling rule measured's neighbour § What this
      deliberately does not change, AD-1 and § Impact, and the README active
      entry. **WHAT DID NOT MOVE, stated so a reader need not diff for it**:
      AD-1's TWO-CODE ruling, AD-2 … AD-6, OQ-1 … OQ-4 (all four still OPEN), the
      TWELVE-scenario count, the two codes and their split, the phasing, the
      removal target contract-v3.0, the packaged corpus, and every realization row
      but § 3.4's pointer.

## 3. Realization — the validator arm (SEPARATE PULL REQUEST)

**REALIZED 2026-09-01**, on branch
`change/realize-requirement-ref-resolution-integrity` off `origin/main`
`6856f502`. Every box below closes on a fact measured on that branch — a path, a
count, a command and its output — never on an intention, and a box that did NOT
close stays OPEN WITH THE MEASUREMENT written in rather than ticked with an
excuse. **THREE SETS OF BOXES DO NOT TICK, EACH FOR A STATED AND CHECKABLE
REASON**: **§ 6**, because the cut allocates a bundle number and another lane's
`contract-v2.6` cut (PR #565) is in flight on the same file; **§ 7.2**, because
the full suite carries ONE failure — pre-existing on `origin/main`, reproduced
identically on an untouched baseline clone, and already PR #568's; and **§ 8**,
because this realization opens a pull request and merges nothing.

- [x] 3.1 **DONE — RE-MEASURED BEFORE ANY EDIT, AND THE DEFECT REPRODUCES
      EXACTLY AS RECORDED.** The two files of § What was measured § 6 were
      written out verbatim under a `credentials/` directory and run against
      `scripts/validate-credential-contracts.py` at `origin/main` `6856f502`,
      BEFORE the first line of this realization was written:

      ```text
      self-test: 6 positive + 16 negative + 10 warning example(s) confirmed, 8 deprecation code(s) probed

      repro: 2 contract(s) checked, 0 skipped, 0 warning(s), 0 error(s) -> PASS
      ```

      **Zero warnings. Zero errors. PASS** — the same three numbers the packet
      recorded at merge-base `3a6a16e9`, so the defect has not moved and this is
      not an implementation against a defect that has. Control A was rebuilt and
      re-verified with it: `wc -c` gives **1318 bytes for BOTH** templates and
      `cmp -l` reports **exactly ONE differing offset — byte 981 1-based, i.e.
      offset 980**, the number the packet states; the control still refuses with
      `shared-secret-identity` naming the FOURTH lift condition, resolution never
      being reached.
      **ONE MEASUREMENT NOTE, RECORDED BECAUSE THE NEXT READER WILL HIT IT.** The
      reproduction's binding template names BOTH secret spellings in its comment
      header, so a global `sed s/example-secret-b/example-secret-a/` over that
      file produces a TWO-byte control (offsets 183 and 980) rather than the
      one-byte control the packet describes. Control A is the `secret_ref:` LINE
      alone. `tests/credential_contracts/test_requirement_ref_resolution.py`
      now builds it by replacing that whole line and ASSERTS the one-offset
      spacing (`test_the_control_is_ONE_BYTE_and_the_templates_are_the_SAME_LENGTH`),
      so the claim cannot drift again.
- [x] 3.2 **DONE.** `_requirement_resolution_warnings(bindings, index)` in
      `scripts/validate-credential-contracts.py`, reached from
      `_deprecation_warnings` — which gains an OPTIONAL `index` parameter
      defaulting to `None` — beside the eight `consumer-*` arms and NOT from
      `_lift_refusal_detail`. It is handed EVERY binding of the document, and the
      comment at the call site says so: the list is not filtered by `by_secret`,
      which is the whole of the act.
      **ONE FAULT KEEPS ONE FINDING.** The `malformed` and `ungrammatical`
      statuses — the two shapes `consumer-member-grammar` and
      `consumer-requirement-ref-grammar` already report — are SKIPPED rather than
      named twice, and so is a `requirement_id` outside the identifier grammar,
      which that same arm reports.
      `test_a_shape_the_GRAMMAR_arms_already_report_is_not_reported_TWICE` drives
      all FIVE such shapes (bare id, one member, extra member, absolute document,
      ungrammatical id) and asserts no `requirement-ref-*` code accompanies any of
      them.
      **AN ABSENT INDEX SKIPS THE PASS ALONE**, rather than reporting `not-found`
      against an index nobody built: an empty index would invent a finding about
      every record in a repository the caller never scanned, and the twenty-odd
      existing one-argument callers in `tests/credential_contracts/` would all
      start warning. `test_no_index_means_no_resolution_finding`.
- [x] 3.3 **DONE, AT THE PROPOSED SPELLINGS.** `requirement-ref-unresolved` and
      `requirement-ref-ambiguous`, reported apart, one per status. Both join
      `DEPRECATION_CODES` — **8 -> 10, asserted by
      `test_the_two_codes_are_DECLARED_and_are_not_a_widening_of_the_consumer_block_set`** —
      and both join `WARNING_EXPECTATIONS` against a packaged probe apiece, which
      the self-test's unprobed/stray checks enforce in both directions.
      **AD-1's TWO-CODE RULING IS WHAT WAS BUILT**; the one-code amendment set is
      DECLINED and not one of its twelve items is applied, so this row's
      *"Subject to AD-1"* cross-reference is DISCHARGED rather than deleted. Its
      item 9 — the `report-the-wrong-status` mutant — is nevertheless carried in
      the mutation round below, because it costs nothing and it proves the two
      codes are ROUTED differently rather than merely spelled differently.
- [x] 3.4 **DONE — `resolve_requirement` IS CALLED AND ITS BODY IS BYTE-UNTOUCHED.**
      `git diff origin/main -- scripts/validate-credential-contracts.py` moves no
      line of that function: same four statuses, same index, same grammar, same
      never-open-a-path rule. The new arm adds no read, no path and no input; it
      reports a resolution the validator already performed and discarded on every
      code path but the lift's.
      **THE NAMING THIS ROW OWES IS PERFORMED, AND IN FOUR PLACES A READER
      ACTUALLY REACHES.** openxFactory issue **#553** is cited (a) in the
      `requirement-ref-ambiguous` FINDING ITSELF, where the reader who hits the
      per-document boundary is standing —
      `test_the_ambiguity_message_cites_the_successor_that_owns_the_wider_arm`;
      (b) in the new `docs/contract-versioning-policy.md` entry; (c) in the
      validator's module docstring and the arm's own docstring; and (d) in
      `examples/credential-contracts/warning/requirement-ref-ambiguous.yaml`'s
      header. **THE PROMOTED SCENARIO AT
      `openspec/specs/credential-contracts/spec.md:565` IS LEFT TO THAT
      SUCCESSOR**, and this realization does not read as having satisfied it: the
      boundary is PINNED by a named test,
      `test_the_same_id_in_ANOTHER_document_draws_nothing_at_this_minor`, which
      declares one id in TWO schema-valid documents and asserts the arm stays
      SILENT — so #553 can see exactly which assertion it is changing.
- [x] 3.5 **DONE.** The lift path is untouched and a sharing pair keeps BOTH
      duties. `test_the_sharing_pair_keeps_BOTH_duties_and_neither_replaced_the_other`
      asserts, on ONE record: exactly ONE semantic finding, and it is
      `shared-secret-identity` carrying *"resolves to no requirement in the
      repository under validation"*; AND exactly one deprecation code, and it is
      `requirement-ref-unresolved`. Neither replaced the other.
      **THE CONTROL IS BUILT WITH IT**, because a refusal test that never had a
      lift to lose proves nothing:
      `test_the_lift_path_is_UNTOUCHED_and_a_conforming_pair_still_lifts` drives
      the packaged two-consumer shape and asserts BOTH lists empty, and
      `test_the_pair_that_lifts_stops_lifting_when_one_reference_stops_resolving`
      moves ONE `requirement_id` between them and watches both verdicts move at
      once. The end-to-end proof is § 7.6's control run, where the one-byte tree
      carries the `shared-secret-identity` ERROR and both new WARNINGS together.
- [x] 3.6 **DONE, and it is FOUR named tests rather than two**, the silent
      direction being what distinguishes a working check from one that fires on
      everything. A reference resolving to exactly one requirement:
      `test_a_reference_that_RESOLVES_draws_nothing`. A binding declaring no
      `requirement_ref`: `test_a_binding_that_declares_NO_reference_draws_nothing`
      — the member is OPTIONAL at this release and an omission is a different
      question from a wrong answer. Beside them,
      `test_a_stub_block_declaring_no_reference_draws_nothing` reaches the record
      kind written before any install exists, and
      `test_the_report_does_not_depend_on_ANY_other_binding_in_the_document`
      proves the delta's second bullet by driving the SAME defective binding
      alone and beside a conformant one and asserting the codes are equal. The
      packaged half is § 4.3's positive.
- [x] 3.7 **DONE — FIVE MUTANTS, EACH WITH BOTH HALVES RECORDED.** The four this
      row enumerates — `drop-the-per-binding-call`, `merge-the-two-codes`,
      `report-on-an-undeclared-member`, `scope-back-to-by_secret` — plus
      `report-the-wrong-status` (the AD-1 item-9 mutant, carried though the
      branch was declined). Each records the ANCHOR (`the named check PASSES
      against unmutated code`) as well as the death, on the sibling module's
      rule that a named test failing for want of a fixture is ANCHOR-MISSING and
      not a kill: `test_the_named_test_PASSES_against_unmutated_code[5]` and
      `test_each_mutant_DIES[5]`, with
      `test_the_mutant_population_is_an_explicit_count` pinning the count at 5.
      **`merge-the-two-codes` IS DRIVEN ON A DOCUMENT CARRYING ONE OF EACH
      FAULT**, because with a single defective binding a merged code is
      indistinguishable from a correctly split one — the anchor would have
      passed and the mutant would have died for the wrong reason.

## 4. Realization — the packaged corpus

- [x] 4.1 **DONE.** `examples/credential-contracts/warning/requirement-ref-unresolved.yaml`
      — ONE binding, sharing its `secret_ref` with NOBODY, naming
      `projection_archive_sweeper` in
      `two-consumer-operated-identity.requirements.example.yaml`, a document that
      SHIPS and is INDEXED and declares no such id. Pointing at a real document
      makes the fault unambiguously the ID rather than a missing file.
      Schema-VALID and drawing no ERROR, which the self-test enforces in both
      directions (`a fixture that is refused belongs in negative/`).
      `test_each_packaged_probe_shares_its_secret_with_NOBODY` asserts the
      no-shared-secret property, because a probe that shared one would pass
      against the SHIPPED validator too and would evidence nothing.
- [x] 4.2 **DONE, RE-USING THE SHIPPED SUPPORT RECORD PER OQ-1.**
      `examples/credential-contracts/warning/requirement-ref-ambiguous.yaml`
      resolves `projection_sync_lane` against
      `support/ambiguous-requirement-ids.requirements.yaml`, which declares that
      id TWICE with DIFFERENT access modes. **THE RE-USE IS RECORDED AT BOTH
      ENDS, not just in the fixture header**: the support record's own header now
      names BOTH probes that depend on its duplication — this file and
      `negative/consumer-requirement-ref-ambiguous.yaml` — and says that
      de-duplicating those ids would leave both passing VACUOUSLY rather than
      failing. A one-ended note is exactly the silent defanging the row warns
      about, since the edit happens in the support record and not in the fixtures.
- [x] 4.3 **DONE, AS ITS OWN FILE PER OQ-4.**
      `examples/credential-contracts/resolving-requirement-ref.binding-template.example.yaml`
      — two bindings, DISTINCT secret references, each reference resolving to
      EXACTLY ONE requirement. It draws no error and no warning of any code,
      which the positive channel's self-test enforces (`positive … unexpectedly
      invalid` lists semantic findings AND deprecation warnings), and the
      positive loop now runs WITH the index so the new arm is actually exercised
      against it rather than skipped. A regression in the silent direction names
      this file. `test_the_positive_proves_the_SILENT_direction_and_shares_no_secret`.
- [x] 4.4 **DONE, IN THE SAME COMMIT AS THE FIXTURES.** All three join the
      by-name inventory tuples in
      `tests/credential_contracts/test_dispatch_credential_contract.py`:
      `POSITIVES` 6 -> 7, `WARNINGS` 10 -> 12, `NEGATIVES` unmoved at 16.
      `test_the_inventory_is_the_whole_corpus_and_not_a_sample` holds all four
      tuples EXHAUSTIVE against the glob, and the count string in
      `test_selftest_passes_on_the_packaged_examples` is DERIVED from the tuples
      (`f"...{len(POSITIVES)}...{len(NEGATIVES)}...{len(WARNINGS)}..."`), so it
      moved with them and no hand-written number was touched. **MEASURED
      BEFORE -> AFTER**: `self-test: 6 positive + 16 negative + 10 warning
      example(s) confirmed, 8 deprecation code(s) probed` becomes
      `self-test: 7 positive + 16 negative + 12 warning example(s) confirmed,
      10 deprecation code(s) probed`.

## 5. Realization — the declared deprecation

- [x] 5.1 **DONE, AND THE COMPLETENESS CLAIM IS RECONCILED IN THE SAME COMMIT.**
      `docs/contract-versioning-policy.md` § Deprecations Currently In Force
      gains an entry for this act: the two codes in a table written from the
      REFUSAL LIST, a migration path PER CODE (repair the REFERENCE for
      `requirement-ref-unresolved`; repair the REQUIREMENTS DOCUMENT THE
      REFERENCE NAMES for `requirement-ref-ambiguous`), the per-binding scope,
      the sharing pair's two duties, the PER-DOCUMENT boundary with #553 named,
      the measurement that nothing narrows at this minor, and the removal target
      **contract-v3.0**.
      **THE SIBLING ENTRY IS RECONCILED RATHER THAN LEFT TO CONTRADICT IT.** Its
      *"THIS ENTRY NAMES EVERY ACT THAT LANDS AT THAT MAJOR"* paragraph now
      carries a **RECONCILED, NOT RESTATED** paragraph naming the NINTH act and
      pointing at the entry that declares it, on the delta's own terms: an entry
      that carries the new act OR names the entry that does. The claim is scoped
      to the consumer block's SEVEN SHAPE acts and stays true.
      **ONE THING THE ENTRY DELIBERATELY DOES NOT SAY**, stated in the entry
      itself rather than left as an omission: it carries NO `Warned since
      contract-vX.Y` line, because the bundle number is § 6.1's to allocate at
      the cut and a number written in advance is a number another packet is
      already spending. An entry naming a warning release that was never cut
      would be the same defect as an entry claiming a completeness it does not
      have.
      **THE SWEEP IS RECORDED IN BOTH DIRECTIONS, because the house rule is that
      an edit changing what a packet asserts about itself owes a sweep of every
      site asserting the same thing — and two of the five sites are deliberately
      NOT edited.** `grep -rniE 'EIGHT warning|eight .consumer-|seven acts'` over
      `docs/ contracts/ scripts/ tests/ README.md openspec/specs/` returns FIVE
      live sites. **RECONCILED:** (1) `docs/contract-versioning-policy.md`
      (§ 5.1); (2) `contracts/manifest.yaml`'s row (§ 5.2); (3)
      `contracts/README.md:109`, the schema-registry table, which repeats the
      same "ONE deprecation window and EIGHT warning codes" sentence and points
      readers AT the policy section — a live registry doc, not digest-pinned, so
      it is swept in the same commit and its change list gains this change.
      **DELIBERATELY LEFT, EACH WITH ITS REASON:** (4)
      `contracts/schemas/xfactory-credential-contracts.schema.yaml:205` — *"the
      eight warning codes the canonical validator emits for the whole of this
      minor"*, inside the block's own `description`. Editing it moves the SCHEMA
      BYTES, which moves the manifest digest § 5.2 pins as unmoved and which
      `proposal.md` § What this deliberately does not change declares out of this
      packet's surface; the sentence is scoped by its own paragraph to the seven
      block narrowings it is describing, and it does not claim to name every code
      the validator will ever emit. (5) `contracts/CHANGELOG.md:270-288` — the
      `contract-v2.4` release entry, which is a RECORD of what that release
      shipped and was TRUE at it. Retroactively editing a shipped release entry
      would falsify the record; § 6.3 gives the CHANGELOG to the cut, which adds
      its OWN entry rather than rewriting an old one.
- [x] 5.2 **DONE, AND THE UNCHANGED DIGEST IS STATED RATHER THAN INFERRED.**
      `contracts/manifest.yaml`'s `credential-contracts` `consumption_rule` moves
      with § 5.1: the *"All seven acts … EIGHT warning codes"* sentence is now
      followed by a paragraph naming the NINTH act, the SECOND code family, the
      EIGHT -> TEN growth, the per-binding scope, the both-duties rule and the
      PER-DOCUMENT boundary with #553. **THE ROW'S `sha256` DOES NOT MOVE, AND
      THE ROW ITSELF NOW SAYS SO**: the digest is the SCHEMA FILE's, resolution
      is not a shape JSON Schema can check — it is a lookup INTO ANOTHER
      DOCUMENT — and the schema is not edited. Verified rather than asserted:
      `python3 scripts/validate-manifest-digests.py` -> `OK contracts/manifest.yaml:
      163 per-file digest(s) verify`, and
      `tests/credential_contracts/test_manifest_row_digest.py` green.
      `contract_bundle_version` stays `contract-v2.5` — the cut is § 6's.
- [x] 5.3 **CHECKED, NONE FOUND — and the sweep is recorded rather than the
      conclusion alone.** `docs/credential-access-model.md` carries THREE sites
      that could have said the reference is resolved only in a pair, and not one
      of them does: `:180` *"resolves binding and issues short-lived grant"* (a
      broker sequence step, about the SECRET); `:231` *"The binding says where
      the credential can be resolved after approval"* (also the secret, not the
      requirement reference); and `:246-250`, the only paragraph in the file
      mentioning `requirement_ref` at all, which describes the SHARING case
      without claiming resolution happens only there. Those are every occurrence
      of `resolv` and every occurrence of `requirement_ref` in the file, by
      `grep`. **NO EDIT MADE, and none is invented**: this row asks for a repair
      if a wrong sentence exists, and adding a right one is a different act than
      the one it authorizes.

## 6. Realization — the contract cut

**NOT THIS SLICE, AND THE FOUR BOXES BELOW STAY OPEN ON PURPOSE.** § 6 allocates
and spends a contract bundle number, and at the time of this realization ANOTHER
LANE'S CUT IS IN FLIGHT ON THE SAME FILE — `contracts/manifest.yaml:3` reads
`contract_bundle_version: contract-v2.5` and openxFactory PR **#565** is an open
`contract-v2.6` cut. Allocating a second number against that file here is exactly
the collision § 6.1 was written to prevent. **REGISTRATION RIDES WHICHEVER CUT
COMES NEXT**: this realization ships the codes, the probes, the policy entry and
the manifest prose, and performs NO cut. The un-ticked boxes are the honest
record of that, not an oversight — untick-with-reason over tick-with-excuse.

- [ ] 6.1 **OPEN — DELIBERATELY.** Re-read `contracts/manifest.yaml:3` at cut
      time. Read at this branch's tip and recorded rather than remembered:
      `contract-v2.5`, with PR #565 open on `contract-v2.6`.
- [ ] 6.2 **OPEN.** `contract_bundle_version` is UNMOVED by this realization —
      verified, not assumed: `grep -n '^contract_bundle_version'
      contracts/manifest.yaml` -> `3:contract_bundle_version: contract-v2.5`,
      the same value `origin/main` carries.
- [ ] 6.3 **OPEN.** `contracts/CHANGELOG.md` is untouched by this realization.
      The class is **DEPRECATING (MINOR)** on the policy's own bullet, which OWES
      the removal version (contract-v3.0) and the migration path in the CHANGELOG
      rather than leaving them optional; both are already written into
      `docs/contract-versioning-policy.md` by § 5.1, so the cut copies rather
      than composes.
- [ ] 6.4 **OPEN.** Release build, digest inventory, tag and `verify-commit` are
      the cut's ritual and none of them ran here.

## 7. Verification gates

All run on branch `change/realize-requirement-ref-resolution-integrity` at its
tip, 2026-09-01. **FIVE OF THE SIX TICK. § 7.2 DOES NOT**, because the full
suite carries ONE failure — a failure that is PRE-EXISTING on `origin/main`,
reproduces identically on an untouched baseline clone, and is already another
lane's open pull request (#568). The box asks for zero failures; it gets one, so
it stays open with the measurement written in. Diagnosing a failure is not the
same act as passing a gate, and only one of those two things happened here.

- [x] 7.1 **GREEN.** `set -o pipefail; python3 -m pytest tests/credential_contracts -q`
      -> **219 passed**, up from **175** on `origin/main` `6856f502` (measured on
      the baseline clone, not remembered). Zero skips added — the new module
      contains none.
      **THE +44 IS 41 + 3, AND THE THREE ARE WORTH NAMING** because they are
      proofs this realization did not write. `comm` over the two collected id
      lists shows 41 from
      `tests/credential_contracts/test_requirement_ref_resolution.py` and THREE
      that the EXISTING corpus-driven parametrisations picked up on their own:
      `test_every_packaged_WARNING_fixture_stays_schema_valid_at_the_minor` for
      each of the two new probes, and
      `test_every_packaged_POSITIVE_validates_at_the_major_too` for the new
      positive — which drives it against `major_projection.py`, the prescription
      for contract-v3.0 made executable. So the three new fixtures are checked
      against BOTH releases without a line being added to say so, which is what
      those parametrisations were built for.
- [ ] 7.2 **NOT TICKED — ONE FAILURE, AND IT IS NOT THIS CHANGE'S.** The box asks
      for ZERO failures, and there is one, so the box does not tick. It is
      un-ticked WITH THE REASON rather than ticked with an excuse.
      `python3 -m pytest tests/ -q -m "not postgres"` ->
      **`1 failed, 8620 passed, 21 skipped, 338 deselected, 9 warnings,
      46 subtests passed in 1293.65s`**.
      **THE PINS AND FLOORS ARE ALL MET.** SKIPPED is **21**, EXACTLY the
      `EXPECT_SKIPPED: "21"` that `.github/workflows/pytest-suite.yml` pins — so
      no directory silently turned into skips, and this realization adds none.
      PASSED 8620 and SELECTED 8642 clear the `MIN_PASSED: "7070"` and
      `MIN_SELECTED: "7090"` floors with margin; neither is lowered.
      **THE FAILURE IS PRE-EXISTING ON `origin/main` AND IS ANOTHER LANE'S OPEN
      PULL REQUEST.** In `tests/sequenced_after/test_sweep.py`, the test
      `test_the_live_sweep_reproduces_the_AUTHORING_measurement` fails
      `assert 18 == 19` on `active_co_modified`. **ISOLATED ON BOTH TREES, WHICH IS WHAT MAKES THIS
      A DIAGNOSIS RATHER THAN A HOPE**: running that file alone gives
      `1 failed, 13 passed` on THIS branch AND on the untouched `origin/main`
      `6856f502` baseline clone, and the `Sweep(...)` tuple the failure prints is
      BYTE-IDENTICAL between them —
      `change_ids=153, active=30, archived=123, co_modified=104,
      sole_modifiers=49, active_co_modified=18`. This realization adds no
      OpenSpec change directory and moves no requirement title, so it cannot move
      any of those counts, and measurement confirms it does not.
      **THE REPAIR IS ALREADY FILED BY ITS OWN LANE: openxFactory PR #568**,
      *"Move the sequenced-after live pin: active_co_modified 19->18 since #563
      archived add-release-tag-publication-check"* — the same number, the same
      test, the same cause. Nothing is owed to this packet by it and nothing is
      owed to it by this packet; this box ticks when that PR lands and the suite
      is re-run.
- [x] 7.3 **GREEN, WITH THE GROWN COUNTS REPORTED.**
      `python3 scripts/validate-credential-contracts.py .` ->
      `self-test: 7 positive + 16 negative + 12 warning example(s) confirmed,
      10 deprecation code(s) probed` and
      `openxFactory: 0 contract(s) checked, 0 skipped, 0 warning(s), 0 error(s)
      -> PASS`. **THE REPO SCAN IS EMPTY BECAUSE openxFactory CARRIES NO
      `credentials/` TREE**, which is stated rather than left to look like a
      pass: the scan target of this validator is a DOMAIN repo, and the tree
      under validation here is the neutral one. The scan-side evidence is § 7.6's
      reproduction and control, which are real two-file repositories.
- [x] 7.4 **GREEN.** `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` ->
      `Totals: 83 passed, 0 failed (83 items)`.
- [x] 7.5 **ZERO NEW FINDINGS.** Same-clock `--as-of` doc-health, this branch
      against an `origin/main` `6856f502` baseline in an identically named
      `openxFactory/` directory, run TWICE — once mid-realization and once over
      the final tree. **THE FINDINGS LINE IS IDENTICAL IN EVERY PAIRING:**
      `Findings: 6 critical, 7 error, 39 warning, 14 info. New regressions vs
      previous report: 0.` The two reports differ in exactly two places, and
      neither is a finding:
      (a) the canon-share metric moves 33.3% -> 33.4% (+1027 canon words,
      +1198 governance words) — the § 5.1 policy prose landing in a ratified
      document and the § 5.1 sweep's sentence landing in a draft one, both of
      which the metric is supposed to move;
      (b) the head's FULL runs each recorded `release-tag-publication` as
      **Skipped**, which the report distinguishes from a finding by its own
      section heading.
      **THAT SKIP WAS CHASED RATHER THAN EXCUSED, AND FOUR CONTROLS SAY IT IS
      ENVIRONMENTAL.** (1) The two head runs gave DIFFERENT reasons — *"the
      published refs for contract-v1.23 could not be consulted"* and *"contracts/
      manifest.yaml could not be read at the published tip `d308c012c`"* — so it
      is not determined by tree content. (2) `git cat-file -t d308c012c` and
      `git cat-file -p d308c012c:contracts/manifest.yaml` BOTH succeed in BOTH
      clones, so the object the second reason names is present and readable. (3)
      Re-running the family ALONE against the final head tree returns
      `release-tag-publication — No findings` and `Findings: 0 critical, 0 error,
      0 warning, 0 info`. (4) Re-running the FULL baseline with its `origin`
      repointed at the same SSH URL the head carries reproduces NOTHING,
      eliminating the remote URL as the cause. The likeliest cause is
      contention: this box was running three other sessions' full test suites
      and the head clone reads through a `--reference-if-able` alternate object
      store those sessions are writing to.
      **NOTHING IS SUPPRESSED AND NOTHING IS OWED TO THE CUT.** No registered
      document moved, so `release-inventory-drift` reports nothing — there is no
      #516-§6.3-shaped drift for a cut to discharge here.
- [x] 7.6 **THE REPRODUCTION NOW REPORTS, AND THE CONTROL STILL REFUSES.**
      Both pasted, and both are also carried as tests so they survive this
      session (`test_the_reproduction_now_REPORTS_and_the_record_stays_VALID`,
      `test_the_one_byte_control_still_reports_its_own_shared_secret_ERROR`).
      The reproduction, on the realized tree:

      ```text
      WARN  [requirement-ref-unresolved] credentials/example.binding-template.yaml: binding 'zero_resolving_lane''s consumer.requirement_ref names requirement 'no_such_requirement' in 'credentials/example.requirements.yaml', and NO requirement of that document carries that id — the reference resolves to NOTHING and is not treated as resolved. THE REPAIR IS AT THE REFERENCE: the id is misspelled, the document moved, or the requirement was never written. Reported on this binding whatever it shares — a dangling reference is a defect OF THE REFERENCE and not of a pair. ERROR at contract-v3.0
      WARN  [requirement-ref-ambiguous] credentials/example.binding-template.yaml: binding 'multi_resolving_lane''s consumer.requirement_ref names requirement 'dup_lane' in 'credentials/example.requirements.yaml', and MORE THAN ONE requirement OF THAT ONE DOCUMENT carries that id; the matches are free to differ in access_mode, so picking one would be a traversal order with an opinion. THE REPAIR IS IN THE REQUIREMENTS DOCUMENT THE REFERENCE NAMES: make the ids that document declares unique. Resolution here is PER-DOCUMENT, which is what the resolver can see; the same id in a DIFFERENT requirements document draws nothing at this release (openxFactory issue #553). ERROR at contract-v3.0

      repro: 2 contract(s) checked, 0 skipped, 2 warning(s), 0 error(s) -> PASS
      ```

      **BOTH DEFECTS NAMED, THE VERDICT STILL `PASS`** — a warning is not a
      refusal and nothing narrows at this minor. Control A (the ONE BYTE) on the
      same tree:

      ```text
      ERROR credentials/example.binding-template.yaml: shared-secret-identity: bindings 'zero_resolving_lane' and 'multi_resolving_lane' share secret_ref 'example-secret-a'; … binding 'zero_resolving_lane' does not declare shared_credential_acknowledged: true — a one-sided declaration exempts a pair on one party's word

      control: 2 contract(s) checked, 0 skipped, 2 warning(s), 1 error(s) -> FAIL
      ```

      The lift path's refusal is byte-identical to the pre-change run and the two
      new warnings sit BESIDE it — the sharing pair keeping both duties, end to
      end.
      **THE TREE IS NOT A SILENT ONE, AND THAT IS CHECKED TOO.** Giving the
      reproduction's `dispatch_only` record a content scope
      (`actions:read` -> `projection:write`) produces
      `ERROR … dispatch-scope-ceiling: requirement 'dup_lane' is dispatch_only
      but requests non-trigger scope(s) ['projection:write']`, so the silence of
      the original run was the gap and not a validator that had stopped looking.

## 8. Archive gate

**ALL FOUR OPEN — this realization opens a pull request and merges nothing.**

- [ ] 8.1 **OPEN.** Not merged. The realization PR is open on
      `change/realize-requirement-ref-resolution-integrity`; required checks and
      the merge commit are owed to it.
- [ ] 8.2 **OPEN.** The cut is § 6 and is deliberately not this slice — see § 6's
      preamble.
- [ ] 8.3 **RE-VERIFIED BY `grep` AT THIS TIP AND STILL TRUE, BUT THE BOX BELONGS
      TO ARCHIVE TIME.** `grep -rn '## MODIFIED Requirements'
      openspec/changes/add-requirement-ref-resolution-integrity/` returns
      NOTHING, so no archive-order hold applies. The row asks for the check AT
      ARCHIVE TIME rather than at realization time, and this realization is not
      that moment; the measurement is recorded so the archiver re-runs it against
      a shorter list of possibilities, not so they skip it.
- [ ] 8.4 **OPEN.** § 9's four items carry dispositions rather than blank boxes
      already; the box closes with the archive.

## 9. Open — deliberately not closed by this change

- [ ] 9.1 **The identity-brokering `requirements_document_ref`**, per OQ-3. The
      packet that introduced that pointer recorded that "no script and no test
      resolves" it. The same class of gap, a different family; a successor issue,
      not a fold-in.
- [ ] 9.2 **The other two conditions of the general SHALL**, per OQ-2 —
      ungrammatical and foreign-repository. Both ARE reported per-binding today
      by `consumer-requirement-ref-grammar`; the finding is that this was checked
      rather than assumed, and the check should be written down where the next
      reader looks.
- [ ] 9.3 **Whether the major should refuse an UNDECLARED `requirement_ref`**
      — i.e. whether the reference becomes required alongside the two
      identifiers. Out of scope: that is a requiredness act on the block, which
      is the sibling's territory and its degraded-mode gate.
- [ ] 9.4 **CROSS-DOCUMENT AMBIGUITY — RULED OUT OF SCOPE AT THIS MINOR
      2026-09-01, AND FILED AS openxFactory ISSUE #553.** No longer routed-open:
      this box carries a RULING. **IT STAYS UNTICKED ON PURPOSE, and on § 9's own
      terms** — this section records what the change DELIBERATELY DOES NOT CLOSE,
      and a ruling that DEFERS a subject to a named successor is not a closing of
      it. The box's disposition, which is what § 8.4 asks of it, is below and is
      complete; § 9.1 sits in exactly this shape for exactly this reason.
      **THE FINDING, as the bench raised it.** Codex, round 3 on PR #542,
      2026-08-31 23:54 UTC, against `deb72c8e` — the tip that was ratified:
      *"Resolve ambiguity across all indexed requirement documents."*
      `resolve_requirement` matches
      `[r for r in index.get(doc_ref, []) if r.get("id") == rid]`
      (`scripts/validate-credential-contracts.py:344`) over an index keyed BY
      DOCUMENT PATH (`requirements_index`, `:294-309`) — scoped to the ONE
      document the reference names — so where the same requirement id sits in TWO
      schema-valid documents a binding pointing at either resolves `ok`, and the
      per-binding arm § 3.2 buys would stay SILENT on that case.
      **WHAT WAS PUT TO BRETT, AND WHAT HE RULED.** The packet was already
      `Status: ratified`, so the contradiction went to him in full rather than in
      summary: this delta's ambiguity scenario AS RATIFIED said *"matching more
      than one requirement record"* — naming no document, so reading as reaching
      ACROSS documents — while § 3.4 freezes a resolver that cannot look past one,
      which made that arm UNMEETABLE by this packet's own realization. **HE RULED
      2026-09-01, in session `openxfactory-f5`, by an explicit multi-choice put:
      SCOPE TO PER-DOCUMENT.** The requirement now states the resolution scope
      plainly, the ambiguity scenario's WHEN is narrowed to the document the
      reference names, and the cross-document arm is DEFERRED. Because the packet
      was ratified, that narrowing is a POST-RATIFICATION CONSENTED AMENDMENT BY
      THE RATIFYING OWNER HIMSELF and is recorded as one at every touched site —
      § 2.5.
      **THE SUCCESSOR IS FILED, NOT PROMISED: openxFactory issue #553**, carrying
      the finding, the resolver mechanics by file and line, the ruling, and the
      choice that arm owes — BROADEN the lookup across indexed documents, or AMEND
      the promoted scenario at
      `openspec/specs/credential-contracts/spec.md:565`. Deciding which is #553's
      work and is deliberately NOT decided here.
      **THE INHERITED GAP IS NAMED, NOT CLOSED.** That promoted scenario — *"a
      named requirement reference matches requirement records in MORE THAN ONE
      DOCUMENT, or more than one record in a document"*, canon since PR #541
      archived `add-binding-consumer-identity` on 2026-08-31 — is ALREADY unmet by
      the SHIPPED resolver. This packet neither created that gap nor closes it.
      What the ruling changes is that the packet no longer CLAIMS to close it, and
      #553 now carries it where the next reader looks.
      **THE BENCH HAS NOT SEEN THIS ANSWER.** No review round has read the packet
      since the finding was raised; the four hourly retries after it were all
      provider-refused on org usage limits. Recorded in
      `review/ratification-2026-09-01.md` § "The review evidence", § "The provider
      refusal, recorded honestly" and § "Addendum, 2026-09-01".
