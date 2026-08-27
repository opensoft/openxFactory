# Tasks: add-modified-block-currency-check

Status: draft
Proposed: 2026-08-27

**Nothing below group 6 has been done.** This packet is a PROPOSAL; groups 1-5
are the realization plan and every box in them is open. Group 6 records what the
authoring session measured before writing the proposal, which is evidence rather
than implementation.

**Build with Speckit, not `/opsx:apply`.** OpenSpec ratifies; Spec Kit builds.
Groups 2, 3, 4 and 5 map one-to-one onto four Spec Kit features and are ordered
by dependency: F1 blocks F2, F2 blocks F3, F3 blocks F4. Group 7 is
recorded-not-fixed and group 8 is the archive act, which is last and stays open
until the merge it follows exists.

## 1. Ratification

- [ ] 1.1 BRETT RULES ON THE PROPOSAL. No ruling covers any part of this. Issues
      #357, #329 and #330 establish the defect class and #357 proposes a check;
      the packet's `.openspec.yaml` records that filing as ADMISSION OF THE CLASS
      INTO THE QUEUE and nothing more. Ratification is a separate act.
- [ ] 1.2 BRETT RULES ON THE FIVE ORCHESTRATOR DECISIONS, each of which is
      independently reversible: D1 (one new family, `promotion-fidelity` not
      extended, #330 shape 1 deferred), D2 (verbatim-after-whitespace matching,
      three arms, in-delta deletion note), D3 (advisory launch, flip requested
      for the scenario-title arm only, never for the carriage ledger), D4 (reuse
      `release-realization`'s "relative to that change's outcome", add only the
      currency consequence), D5 (no MODIFIED block in this packet; it is owed at
      realization). A veto on D1 re-scopes the whole change; a veto on D2, D3 or
      D4 is a rewrite of one requirement paragraph; a veto on D5 requires
      `add-family-enumeration-check` to archive first.
- [ ] 1.3 IF D1 IS VETOED IN FAVOUR OF #330's SHAPE 1, this packet becomes a
      `promotion-fidelity` extension and the measurement-basis requirement must
      be amended in the same change to declare a third basis. Recorded so the
      cost of that veto is visible before it is taken, not after.

## 2. Speckit F1 — the family module and its registrations

- [ ] 2.1 **FIRST, AND IN THE SAME COMMIT AS THE REGISTRATION: the `doc-health`
      delta gains its `## MODIFIED Requirements` block on "Deterministic check
      families".** Owed and deliberately absent from the proposal (D5): a
      proposal-only tree registers no family, so the restatement would name a
      family the registry does not carry and would red
      `test_the_real_corpus_reads_zero_on_both_halves`, which was demonstrated
      rather than assumed (§ 6.4). The block is written RELATIVE TO
      `add-family-enumeration-check`'s outcome per `release-realization`'s
      "Ordered deltas and branch vocabulary" — twenty-one → twenty-two, the
      enumeration gaining `modified-block currency`, `Four of the twenty-two`,
      `the other eighteen families`, one new sentence declaring that this family
      reads ACTIVE change deltas and promoted specs and therefore takes neither
      the governed corpus nor the lifecycle scan set, and one new `AND` bullet in
      `A run executes the check families`. ACCEPTANCE: all EIGHT scenarios
      restated, per-requirement count recorded as **8 → 8**, seven byte-identical
      to `add-family-enumeration-check`'s outcome and the eighth differing by
      exactly one bullet; and `fam_family_enumeration` reads 0 against the tree.
- [ ] 2.2 `scripts/doc_health/modified_block_currency.py`. The ACTIVE-change
      delta reader (`openspec/changes/*/specs/*/spec.md`, `archive/` excluded),
      the promoted-requirement reader, the `## MODIFIED Requirements` section
      parser, the whitespace normalization, and the unit split into body
      sentences, scenario titles and scenario bullets.
- [ ] 2.3 The three arms as three finding classes: scenario-title completeness
      (`warning`), the carriage ledger (`info`, ONE finding per requirement
      listing its uncarried units), and title resolution / two-writers
      (`warning`). `_LAUNCH_SEVERITY` is a module constant so the flip in § 7.2
      is one line beside one `FAMILY_RESOLUTION` row.
- [ ] 2.4 The in-delta deletion-declaration parser: a dated bold note inside the
      MODIFIED block, naming deleted scenarios by exact title in backticks and
      quoting deleted body units. Suppresses exactly what it names. NO fuzzy
      matching on the note either — an unparseable note suppresses nothing and
      says so.
- [ ] 2.5 The two-writers resolution: where a second active change carries a
      MODIFIED block for one `(capability, title)`, the later block is measured
      against the earlier change's outcome, and the earlier change's additions
      must be present in it. "Later" is resolved the way this corpus already
      resolves it and NOT by inventing a second ordering rule — see § 7.3 for the
      open question this leaves.
- [ ] 2.6 The disposition read: `health/dispositions.yaml` entries naming this
      family with a `cite`, optionally narrowed by `requirement:`, in the shape
      `promotion_fidelity.py` already implements. Reuse that reader; do not write
      a second one.
- [ ] 2.7 Registration: one import and one `FAMILIES` line in `families.py`, one
      `FAMILY_IDS` entry in `__init__.py` so the family gets its own report
      section, one `FAMILY_NOTES`-style comment recording why the family is
      deliberately ABSENT from `FAMILY_RESOLUTION`, and the `families.py` module
      docstring's owner list extended.
- [ ] 2.8 `tests/doc-health/test_lifecycle_scan_set.py`: the twenty-second family
      classified as a non-reader of the lifecycle scan set. That test exists to
      fail loudly when a new family is added without classifying it.

## 3. Speckit F2 — fixtures and tests

- [ ] 3.1 **REGRESSION FIXTURE A — the #351 true positive, reconstructed.**
      `add-doxchat-model-intake`'s pre-repair block against the canon of
      2026-08-25: six body clauses, two scenarios (`The menu offers a routing
      rule`, `A fourth provider verb is proposed`) and one reverted scenario line
      ("every loaded editor" → "the Outline and Document editors"). ACCEPTANCE:
      the scenario arm fires on the two scenarios BY TITLE; the carriage ledger
      lists the six clauses AND the reverted line; and the assertion is on the
      rule text and the named units, never on a count.
- [ ] 3.2 **REGRESSION FIXTURE B — the #329 one-of-eight case.** A MODIFIED block
      restating 1 of a promoted requirement's 8 scenarios, with the change's own
      ADDED requirement bringing 7 so the FILE-LEVEL scenario count stays flat.
      ACCEPTANCE: the family fires naming all seven omitted titles, and a second
      assertion pins that the flat file-level count is NOT what the family reads —
      the defect that made this class nearly escape.
- [ ] 3.3 NEGATIVE — a scenario-complete block stays quiet, including one that
      re-wraps every paragraph it carries. This is the case line-level matching
      would have failed and is why D2 normalizes whitespace.
- [ ] 3.4 NEGATIVE — a declared deletion stays quiet, and suppresses EXACTLY the
      units the note names: a note naming one of two dropped scenarios leaves the
      other reported.
- [ ] 3.5 NEGATIVE — a MODIFIED title resolving to an active sibling's ADDED,
      with the sibling referenced, stays quiet (pending, not absent). POSITIVE —
      the same title with no sibling and no canon requirement fires.
- [ ] 3.6 TWO-WRITERS — two active changes on one canon requirement: the later
      block missing the earlier's addition fires; carrying it stays quiet.
- [ ] 3.7 STRUCTURAL PINS ON THE ADVISORY LAUNCH, both halves, so a half-flip in
      either direction fails: `_LAUNCH_SEVERITY` is not `error`, and
      `"modified-block-currency"` is absent from `FAMILY_RESOLUTION`.
- [ ] 3.8 A scope with no active change carrying a MODIFIED block reports SKIPPED
      with its reason, never silently omitted.
- [ ] 3.9 Determinism: two runs over one fixture tree produce byte-identical
      findings, including ordering.

## 4. Speckit F3 — the self-gate against this repository

- [ ] 4.1 THE FAMILY RUNS AGAINST THIS REPOSITORY'S OWN TREE, through the family
      itself rather than by inspection, and the result is asserted. Expected at
      the branch point, from § 6: **1 scenario-arm finding, 10 carriage-ledger
      findings, 0 title-resolution findings.** Assert the scenario-arm finding by
      its NAMED subject (`add-composed-view-authoring` /
      `Gate verbs hide on a composed view`) so the test cannot pass vacuously on
      a different finding.
- [ ] 4.2 THE FAMILY READS ITS OWN PACKET. Assert that this change's own delta is
      among the statements examined once § 2.1's MODIFIED block exists, so § 4.1
      cannot pass because discovery quietly stopped working.
- [ ] 4.3 THE WHOLE SUITE: `python3 -m pytest tests/doc-health` green, and the
      count recorded before and after so the added tests are visible as a
      delta rather than asserted.
- [ ] 4.4 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, count
      recorded.
- [ ] 4.5 THE REPORT MOVES BY EXACTLY THE PREDICTION AND IN NO OTHER LINE.
      `python3 scripts/doc-health.py` single-repo, diffed against the same run on
      `main`: +1 `warning`, +10 `info`, 0 `error`, 0 `critical`, headline
      unchanged, census / inventory / catalog untouched. A movement anywhere else
      is a defect in this change, not a surprise to be explained in prose.

## 5. Speckit F4 — reporting and workflow

- [ ] 5.1 The family renders its own report section, with the three arms
      distinguishable in the section rather than summed — a reader must be able
      to see one scenario-arm warning next to ten editorial rows without
      counting.
- [ ] 5.2 The action line: "restate the requirement as canon currently states it,
      or declare the deletion in the block". No existing family's action line
      says this, which is part of D1's argument for a family.
- [ ] 5.3 NO workflow change is expected. `.github/workflows/doc-health-reusable.yml`
      passes no per-family option to this family and MUST NOT: the live-`main`
      basis belongs to `promotion-fidelity` alone, and this family measures the
      checkout by contract. Verify by test that no other module can name a basis
      option for it, the way `test_workflow_contract.py` already pins that
      boundary.

## 6. Evidence recorded at proposal time

- [x] 6.1 THE SPIKE. A throwaway implementation of the proposed matching rule,
      run across every active change under `openspec/changes/*/specs/*/spec.md`
      (`archive/` excluded) against `openspec/specs/*/spec.md`, at `9be81a40`.
      Not committed. Results in § 6.2-6.4.
- [x] 6.2 THE THREE ARMS, MEASURED SEPARATELY over 23 MODIFIED requirements in
      the active corpus: scenario-title losses **1**, body-sentence losses
      **10**, scenario-bullet losses **3**; **10 requirements** fire on at least
      one arm. Reported as **1 warning + 10 info**. The single scenario-arm
      finding is `add-composed-view-authoring` / `ideation-dashboard` /
      "Composed views are read-only with a repository jump", omitting canon's
      `Gate verbs hide on a composed view` — which on inspection is a deliberate
      RENAME to `Tile-bound gate verbs hide on a composed view`, i.e. the exact
      case the in-delta declaration exists for. All 13 ledger units are
      deliberate in-place edits.
- [x] 6.3 THE LEDGER REPRODUCED A HUMAN VERIFICATION. Against
      `add-doxchat-model-intake` the bullet arm isolates exactly ONE unit — the
      widened `browser loads model choices` line — which is the single-line
      residue PR #358's manual `canon ⊆ intake ⊆ B` check reported after the
      repair. Independent agreement between the mechanical rule and the human
      procedure it replaces, on the case that produced #351.
- [x] 6.4 THE TWO-WRITERS ARM MEASURED ZERO, AND COMPLIANCE MEASURED 7 OF 7.
      Seven `(capability, requirement)` pairs are written by two active changes;
      in all seven the modifying change's proposal already names the sibling; all
      seven are MODIFIED-over-a-sibling's-ADDED; **zero** titles resolve to
      neither canon nor a sibling.
- [x] 6.5 THE D5 EXPERIMENT. The enumeration MODIFIED block was written
      (twenty-one → twenty-two, 8 of 8 scenarios) and
      `fam_family_enumeration` run against the resulting tree: **3 findings**,
      and `test_the_real_corpus_reads_zero_on_both_halves` FAILED. The block was
      withdrawn to § 2.1; with it removed the same call reads **0**. This is why
      the packet carries no MODIFIED block.
- [x] 6.6 CANON'S STATE CONFIRMED, not assumed: `openspec/specs/doc-health/spec.md`
      still reads "twenty check families" in prose with three numerals;
      `add-family-enumeration-check` is ACTIVE with its code landed and its delta
      unpromoted; `families.FAMILIES` registers 21.

## 7. Open — recorded, not fixed

- [ ] 7.1 #330's SHAPE 1, the post-archive safety net. Diff a promoted spec
      against its own prior state across the archive commit and report any
      requirement that lost scenarios. NOT built here (D1): it needs the spec's
      state at the archive commit's parent, which is a third measurement basis
      inside a family whose promoted requirement obliges it to declare which of
      TWO it measured. It is the second net, not the first, and #330 itself calls
      the pre-archive gate "where it is cheap". A separate change, or a ruling
      that this family should own a history-reading arm.
- [ ] 7.2 RULE on raising the SCENARIO-TITLE arm from advisory to enforcing —
      `error` severity AND the `contested` classification, moved together in one
      commit, never apart. The standing population to discharge first is ONE
      finding (§ 6.2). No flip is proposed for the carriage ledger, by D3.
- [ ] 7.3 THE "LATER" QUESTION IN THE TWO-WRITERS ARM. `promotion-fidelity`
      orders ARCHIVED packets by folder date with an archive-commit tie-break.
      Active changes have no such ordering — there is no archive folder and no
      archive act yet. The arm therefore reports the ASYMMETRY (which block
      carries which additions) rather than deciding who is later, and PR #358's
      conclusion for intake and B — "archive safety is asymmetric ... the
      constraint is intake archives before B" — is the shape a reader must still
      reason to. Whether the family should also require an explicit archive-order
      declaration in the later packet is unruled.
- [ ] 7.4 THE DOMAIN FACTORIES ARE UNMEASURED. This change's evidence is
      openxFactory's active changes and a fixture corpus. What the pinned
      domains' active changes will say is unknown, and is the reason the launch
      is advisory rather than a claim.
- [ ] 7.5 ISSUE #318 REMAINS OPEN AND THIS PACKET SITS IN IT. A drafted,
      unapproved packet still has no origin kind that expresses "proposed, not
      approved"; this one uses `Status: draft` plus an origin recording admission
      into the queue, which is the shape `create-medxchart-overlay-boundary` and
      `qualify-avatar-live-voice` use. Named here so the workaround is visible,
      not fixed here — it is another capability's rule.

## 8. Archive

- [ ] 8.1 ARCHIVE AFTER REALIZATION AND AFTER THE MERGE. This change ships ACTIVE
      and archives only once the realization is merged to `main` and green:
      `pytest tests/doc-health`, `openspec validate --all --strict`, and a
      doc-health run moving by exactly § 4.5's prediction. The archive act is a
      separate later commit titled for the merge it follows, per
      `add-promotion-fidelity-check` (`01ff3434`) and
      `add-family-enumeration-check`.
- [ ] 8.2 AT THE ARCHIVE GATE, VERIFY THIS CHANGE'S OWN PROMOTION BYTE-FOR-BYTE,
      per requirement, in both capabilities. A change whose subject is lossy
      promotion that promoted lossily would be the worst possible entry in this
      record. Record the per-requirement scenario counts before and after.
