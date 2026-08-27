# Tasks: add-modified-block-currency-check

Status: draft
Proposed: 2026-08-27

Nothing below group 6 has been done. Groups 1-5 are the realization plan and
every box in them is open; group 6 records what the authoring session measured
before writing the proposal, which is evidence rather than implementation.

Build with Speckit, not `/opsx:apply`. OpenSpec ratifies; Spec Kit builds.
Groups 2, 3, 4 and 5 map one-to-one onto four Spec Kit features and are ordered
by dependency: F1 blocks F2, F2 blocks F3, F3 blocks F4. Group 7 is
recorded-not-fixed and group 8 is the archive act, last and open until the
merge it follows exists.

## 1. Ratification

- [ ] 1.1 Brett rules on the proposal. No ruling covers any part of this. Issues
      #357, #329 and #330 establish the defect class and #357 proposes a check;
      the packet's `.openspec.yaml` records queue admission by the orchestrating
      session on those filed issues, and says in its own words that it is not an
      approval. Ratification is a separate act.
- [ ] 1.2 Brett rules on the five orchestrator decisions, each independently
      reversible: D1 (one new family, `promotion-fidelity` not extended, #330
      shape 1 deferred), D2 (same-kind exact units, containment and similarity
      both forbidden, normative unit derivation, a new reserved marker), D3
      (advisory launch, flip requested for the scenario-title arm, none proposed
      for the ledger in this packet), D4 (reuse `release-realization` with
      `ratified` verbatim; reading scope stated separately), D5 (no MODIFIED
      block in this packet; owed at realization). A veto on D1 re-scopes the
      change; a veto on D2, D3 or D4 rewrites one requirement paragraph; a veto
      on D5 requires `add-family-enumeration-check` to archive first.
- [ ] 1.3 If D1 is vetoed in favour of #330's shape 1, this packet becomes a
      `promotion-fidelity` extension and "The promotion fidelity measurement
      basis is declared" must be amended in the same change to declare a third
      basis. Recorded so the cost of that veto is visible before it is taken.

## 2. Speckit F1 — the family module and its registrations

- [ ] 2.1 FIRST, AND IN THE SAME COMMIT AS THE REGISTRATION: the `doc-health`
      delta gains its `## MODIFIED Requirements` block on "Deterministic check
      families". Owed and deliberately absent from the proposal (D5): a
      proposal-only tree registers no family, so the restatement would name a
      family the registry does not carry and would red
      `test_the_real_corpus_reads_zero_on_both_halves`, demonstrated rather than
      assumed (§ 6.5). The block is written relative to
      `add-family-enumeration-check`'s outcome per `release-realization`'s
      "Ordered deltas and branch vocabulary" — twenty-one → twenty-two, the
      enumeration gaining `modified-block currency`, `Four of the twenty-two`,
      `the other eighteen families`, one new sentence declaring that this family
      reads active change deltas and promoted specs and therefore takes neither
      the governed corpus nor the lifecycle scan set, and one new `AND` bullet in
      `A run executes the check families`. ACCEPTANCE: all eight scenarios
      restated, per-requirement count recorded as 8 → 8, seven byte-identical to
      `add-family-enumeration-check`'s outcome and the eighth differing by
      exactly one bullet; `fam_family_enumeration` reads 0 against the tree; and
      the one carriage-ledger finding this block draws against itself (§ 6.6) is
      present and expected rather than treated as a regression.
- [ ] 2.2 `scripts/doc_health/modified_block_currency.py`. The active-change
      delta reader (`openspec/changes/*/specs/*/spec.md`, `archive/` excluded,
      every active change regardless of lifecycle standing), the
      promoted-requirement reader, the `## MODIFIED Requirements` section parser,
      and whitespace normalization.
- [ ] 2.3 THE UNIT DERIVATION, IMPLEMENTED EXACTLY AS THE DELTA STATES IT: mask
      backticked spans before any sentence split; split on a period, question
      mark or exclamation mark followed by whitespace or end of paragraph; each
      body bullet line is one unit with its list marker stripped; each dated bold
      note is ONE undivided unit; each `#### Scenario:` heading is one title unit
      and each scenario bullet one bullet unit. Matching is same-kind and exact.
      CONTAINMENT AND SIMILARITY ARE BOTH FORBIDDEN — a test asserts that a block
      bullet CONTAINING canon's bullet still fires (§ 3.4).
- [ ] 2.4 The three arms as three finding classes: scenario-title completeness
      (`warning`), the carriage ledger (`info`, one finding per requirement
      listing its uncarried units), and title resolution / two-writers
      (`warning`). Scenario bullets compare against ALL bullets of the block,
      never scenario by scenario. `_LAUNCH_SEVERITY` is a module constant so the
      flip in § 7.2 is one line beside one `FAMILY_RESOLUTION` row.
- [ ] 2.5 The reserved-marker parser, two forms, recognized by form and never by
      prose: `**Removed from canon by <change-id> (<YYYY-MM-DD>):** ` followed by
      backticked unit names separated by semicolons and a ` — <reason>`; and
      `**Merged into <new scenario title> by <change-id> (<YYYY-MM-DD>):** `
      followed by backticked superseded titles. Whitespace normalization applies
      to the marker, so a wrapped marker parses. A marker suppresses only units
      it names AND that are absent from the block; a marker naming a present unit
      is itself reported. NO fuzzy matching on the marker either.
- [ ] 2.6 The two-writers resolution: where a second active change carries a
      MODIFIED block for one `(capability, title)`, the later block is measured
      against the earlier change's outcome, and the earlier change's additions
      must be present in it. Where the earlier change is an active RATIFIED
      change, the reference is checked as that change's id occurring as a whole
      token in the later change's own `proposal.md`. "Later" is UNRULED for two
      active changes — see § 7.3; implement whatever § 7.3's ruling settles, and
      until it is settled do not silently pick one.
- [ ] 2.7 The disposition read: `health/dispositions.yaml` in the aggregation
      checkout, entries naming this family with a `cite`, optionally narrowed by
      `requirement:`, in the shape `promotion_fidelity.py` already implements.
      Reuse that reader; do not write a second one.
- [ ] 2.8 Registration: one import and one `FAMILIES` line in `families.py`, one
      `FAMILY_IDS` entry in `__init__.py`, one comment recording why the family
      is deliberately absent from `FAMILY_RESOLUTION`, and the `families.py`
      module docstring's owner list extended.
- [ ] 2.9 `tests/doc-health/test_lifecycle_scan_set.py`: the twenty-second family
      classified as a non-reader of the lifecycle scan set. That test exists to
      fail loudly when a new family is added without classifying it.

## 3. Speckit F2 — fixtures and tests

- [ ] 3.1 REGRESSION FIXTURE A — the #351 true positive, reconstructed.
      `add-doxchat-model-intake`'s pre-repair block against the canon of
      2026-08-25: six body clauses, two scenarios (`The menu offers a routing
      rule`, `A fourth provider verb is proposed`) and one reverted scenario line
      ("every loaded editor" → "the Outline and Document editors"). ACCEPTANCE:
      the scenario arm fires on the two scenarios by title; the ledger lists the
      six clauses AND the reverted line; assertions are on the rule text and the
      named units, never on a count.
- [ ] 3.2 REGRESSION FIXTURE B — the #329 one-of-eight case. A MODIFIED block
      restating 1 of a promoted requirement's 8 scenarios, with the change's own
      ADDED requirement bringing 7 so the file-level scenario count stays flat.
      ACCEPTANCE: the family fires naming all seven omitted titles, and a second
      assertion pins that the flat file-level count is not what the family reads.
- [ ] 3.3 RED TEST — RETITLE AND GUT. Rename a scenario, declare the rename with
      a `Merged into` marker, and drop two of the superseded scenario's four
      bullets. ACCEPTANCE: the scenario arm is quiet (the marker is valid) AND
      the ledger reports the two dropped bullets. This test fails under any
      scenario-paired bullet comparison and is the reason the delta compares
      bullets across the whole block.
- [ ] 3.4 RED TEST — CONTAINMENT IS NOT CARRIAGE. A block bullet that CONTAINS
      canon's bullet verbatim as a substring, widened at either end. ACCEPTANCE:
      the ledger reports canon's bullet as uncarried. This is #351's widening
      mechanism and the case the first draft of the delta would have missed.
- [ ] 3.5 TOKENIZATION FIXTURE — a requirement body carrying backticked tokens
      with internal periods (`.openspec.yaml`, `promotion_fidelity.py`,
      `contract-v1.45`), a body bullet list, and a dated bold note spanning
      several sentences. ACCEPTANCE: no unit boundary falls inside a backticked
      span; each bullet is one unit; the note is ONE unit; and an edit to the
      note's third sentence reports the note once, not three times.
- [ ] 3.6 NEGATIVE — a scenario-complete block stays quiet, including one that
      re-wraps every paragraph it carries. The case line-level matching fails.
- [ ] 3.7 MARKER TESTS — a valid `Removed from canon by` marker suppresses
      exactly the units it names and leaves an unnamed sibling reported; a marker
      naming a unit the block still carries is itself reported; a marker wrapped
      across two lines parses; a prose dated bold note that is NOT one of the two
      reserved forms suppresses nothing. The last is the guard on the review's
      finding that canon's own restoration notes must never be read as
      declarations of deletion.
- [ ] 3.8 NEGATIVE — a MODIFIED title resolving to an active sibling's ADDED
      stays quiet (pending, not absent). POSITIVE — the same title with no
      sibling and no canon requirement fires.
- [ ] 3.9 TWO-WRITERS — two active changes on one canon requirement: the later
      block missing the earlier's addition fires; carrying it stays quiet. Pin
      that an unratified earlier writer creates NO reference obligation, so the
      `ratified` scoping of `release-realization`'s rule is not silently widened.
- [ ] 3.10 STRUCTURAL PINS ON THE ADVISORY LAUNCH, both halves, so a half-flip in
      either direction fails: `_LAUNCH_SEVERITY` is not `error`, and
      `"modified-block-currency"` is absent from `FAMILY_RESOLUTION`.
- [ ] 3.11 A scope with no `openspec/changes/` directory reports SKIPPED with its
      reason; a scope WITH active changes but no MODIFIED block reports nothing
      and is NOT skipped. The two are different states and canon's skip rule is
      "cannot run", not "found nothing".
- [ ] 3.12 Determinism: two runs over one fixture tree produce byte-identical
      findings, including ordering.

## 4. Speckit F3 — the self-gate against this repository

- [ ] 4.1 The family runs against this repository's own tree, through the family
      itself rather than by inspection, and the result is asserted. Expected with
      § 2.1's block present, from § 6: 1 scenario-arm finding, 11
      carriage-ledger findings, 0 title-resolution findings. Assert the
      scenario-arm finding by its named subject (`add-composed-view-authoring` /
      `Gate verbs hide on a composed view`) so the test cannot pass vacuously.
- [ ] 4.2 The family reads its own packet. Assert that this change's own § 2.1
      delta is among the blocks examined and that it is measured against
      `add-family-enumeration-check`'s outcome, so § 4.1 cannot pass because
      discovery quietly stopped working.
- [ ] 4.3 The whole suite: `python3 -m pytest tests/doc-health` green, count
      recorded before and after so the added tests are visible as a delta.
- [ ] 4.4 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, count
      recorded.
- [ ] 4.5 The report moves by exactly the prediction and in no other line.
      `python3 scripts/doc-health.py` single-repo, diffed against the same run on
      `main`: +1 `warning`, +11 `info`, 0 `error`, 0 `critical`, headline
      unchanged, census / inventory / catalog untouched. Movement anywhere else
      is a defect in this change.

## 5. Speckit F4 — reporting and workflow

- [ ] 5.1 The family renders its own report section with the three arms
      distinguishable rather than summed — a reader must see one scenario-arm
      warning next to eleven editorial rows without counting.
- [ ] 5.2 The action line: "restate the requirement as canon currently states it,
      or declare the deletion with a `Removed from canon by` marker". No existing
      family's action line says this, which is part of D1's argument.
- [ ] 5.3 NO workflow change is expected. `.github/workflows/doc-health-reusable.yml`
      passes no per-family option to this family and must not: the live-`main`
      basis belongs to `promotion-fidelity` alone, and this family measures the
      checkout by contract. Pin the boundary by a NEW test of this family's own —
      `test_workflow_contract.py` pins that boundary for `promotion-fidelity` in a
      shape written for that family, and this is a new assertion rather than a
      reuse of that pin.

## 6. Evidence recorded at proposal time

- [x] 6.1 THE SPIKE, run under the matching rule exactly as the delta writes it:
      same-kind exact units, backtick-masked sentence split, bullets compared
      across the whole block. Every active change under
      `openspec/changes/*/specs/*/spec.md` (`archive/` excluded) against
      `openspec/specs/*/spec.md`, at `9be81a40`. Not committed.
- [x] 6.2 THE THREE ARMS, MEASURED SEPARATELY over 23 MODIFIED requirements at
      the branch point: scenario-title losses **1**; ledger **14 units** (10
      body, 4 scenario-bullet) across **10 requirements**; title-resolution
      **0**. Reported as **+1 warning, +10 info**.
- [x] 6.3 THE SINGLE SCENARIO-ARM FINDING: `add-composed-view-authoring` /
      `ideation-dashboard` / "Composed views are read-only with a repository
      jump", omitting canon's `Gate verbs hide on a composed view` — on
      inspection a deliberate rename to `Tile-bound gate verbs hide on a composed
      view`, the case the marker exists for, and NOT claimed as a defect. The
      same block also drops one of that scenario's two bullets, which the ledger
      reports separately; the rename and the bullet loss are different facts.
- [x] 6.4 THE LEDGER REPRODUCED A HUMAN VERIFICATION, AND ONLY BECAUSE MATCHING
      IS EXACT. Against `add-doxchat-model-intake` the bullet arm isolates
      exactly one unit — canon's `**THEN** the selector MUST show exactly the
      available catalog entries and their data-handling badges` — which is the
      single-bullet residue PR #358's manual `canon ⊆ intake ⊆ B` verification
      reported. Canon's bullet is a SUBSTRING of the widened replacement, so the
      first draft's containment reading yielded zero here; the finding exists
      only under the exact-unit rule now written into the delta.
- [x] 6.5 THE D5 EXPERIMENT. The enumeration MODIFIED block was written
      (twenty-one → twenty-two, 8 of 8 scenarios) and `fam_family_enumeration`
      run against the resulting tree: 3 findings, and
      `test_the_real_corpus_reads_zero_on_both_halves` FAILED. Withdrawn to
      § 2.1; with it removed the same call reads 0.
- [x] 6.6 THE REALIZATION PREDICTION, MEASURED WITH § 2.1's BLOCK PRESENT.
      Measured against `add-family-enumeration-check`'s outcome, § 2.1's block
      does not carry two body sentences — the enumeration sentence and the "Four
      of the twenty-one" sentence — so it adds ONE ledger finding: **16 units
      across 11 requirements, +1 warning and +11 info**. It also creates the
      corpus's first two-writers instance between two ACTIVE changes; the spike
      resolved "later" by `.openspec.yaml` `created:` (2026-08-27 against
      2026-08-25), which is a reading and not a ruling — § 7.3.
- [x] 6.7 THE TWO-WRITERS ARM MEASURED ZERO, COMPLIANCE 7 OF 7. Seven
      `(capability, requirement)` pairs are written by two active changes; in all
      seven the modifying proposal names the sibling; all seven are
      MODIFIED-over-a-sibling's-ADDED; zero titles resolve to neither.
- [x] 6.8 CANON'S STATE CONFIRMED, not assumed: `openspec/specs/doc-health/spec.md`
      still reads "twenty check families" with three numerals;
      `add-family-enumeration-check` is active with code landed and delta
      unpromoted; `families.FAMILIES` registers 21. Three families carry a
      `_LAUNCH_SEVERITY` and launched advisory; two have flipped;
      `family_enumeration._LAUNCH_SEVERITY` is still `WARNING`;
      `release-inventory-drift` never had an advisory launch to flip.

## 7. Open — recorded, not fixed

- [ ] 7.1 **#330 STAYS OPEN.** Its shape 1 — the post-archive safety net,
      diffing a promoted spec against its own prior state across the archive
      commit — is not built here (D1): it needs the spec's state at the archive
      commit's parent, a third measurement basis inside a family whose promoted
      requirement obliges it to declare which of TWO it measured. OWNER: the
      doc-health steward, at the next family change touching
      `promotion_fidelity.py`, who either builds the arm with the basis
      amendment or records that the pre-archive gate is accepted as sufficient.
      This change MUST NOT be read as closing #330, and its PR says so.
- [ ] 7.2 RULE on raising the SCENARIO-TITLE arm from advisory to enforcing —
      `error` severity AND the `contested` classification, moved together in one
      commit, never apart. The standing population to discharge first is one
      finding (§ 6.3). No flip is proposed for the carriage ledger in this
      packet; a later flip for it is a separate ruling and is not foreclosed —
      seven of #351's nine items are reported rather than gated until one is
      taken.
- [ ] 7.3 **THE "LATER" QUESTION BETWEEN TWO ACTIVE WRITERS — RULING OWED.**
      `promotion-fidelity` orders ARCHIVED packets by folder date with an
      archive-commit tie-break; active changes have neither a folder date nor an
      archive act. This change's own § 2.1 creates the corpus's first instance
      (§ 6.6), so the question is live rather than hypothetical. Candidates:
      `.openspec.yaml` `created:` (what the spike used), the packet's first
      commit timestamp, or an explicit archive-order declaration required in the
      later packet. OWNER: Brett, before § 2.6 is implemented — § 2.6 is blocked
      on this ruling and must not default silently. Until it is ruled, the delta
      states the CONSEQUENCE (the later block is measured against the earlier
      outcome) without stating how "later" is decided.
- [ ] 7.4 THE DOMAIN FACTORIES ARE UNMEASURED. This change's evidence is
      openxFactory's active changes and a fixture corpus; what the pinned
      domains' active changes will say is unknown, and is why the launch is
      advisory.
- [ ] 7.5 ISSUE #318 REMAINS OPEN AND THIS PACKET SITS IN IT. A drafted,
      unapproved packet still has no origin kind expressing "proposed, not
      approved"; this one uses `Status: draft` plus an origin recording queue
      admission by the orchestrating session, the shape
      `create-medxchart-overlay-boundary` uses. Named so the workaround is
      visible; it is another capability's rule to fix.

## 8. Archive

- [ ] 8.1 ARCHIVE AFTER REALIZATION AND AFTER THE MERGE. This change ships active
      and archives only once the realization is merged to `main` and green:
      `pytest tests/doc-health`, `openspec validate --all --strict`, and a
      doc-health run moving by exactly § 4.5's prediction. The archive act is a
      separate later commit titled for the merge it follows, per
      `add-promotion-fidelity-check` (`01ff3434`) and
      `add-family-enumeration-check`.
- [ ] 8.2 AT THE ARCHIVE GATE, VERIFY THIS CHANGE'S OWN PROMOTION BYTE-FOR-BYTE,
      per requirement, in both capabilities, and resolve the § 2.1 ordering
      against `add-family-enumeration-check` explicitly rather than by whichever
      archives first. A change whose subject is lossy promotion that promoted
      lossily would be the worst possible entry in this record. Record the
      per-requirement scenario counts before and after.
