# Tasks: add-modified-block-currency-check

Status: ratified
Ratified by: add-modified-block-currency-check

Nothing below group 6 has been done. Groups 1-5 are the realization plan and
every box in them is open; group 6 records what the authoring session measured
before writing the proposal, which is evidence rather than implementation.

Build with Speckit, not `/opsx:apply`. OpenSpec ratifies; Spec Kit builds.
Groups 2, 3, 4 and 5 map one-to-one onto four Spec Kit features and are ordered
by dependency: F1 blocks F2, F2 blocks F3, F3 blocks F4. Group 7 is
recorded-not-fixed and group 8 is the archive act, last and open until the
merge it follows exists.

**THE TWO PARAGRAPHS ABOVE ARE THE AUTHORING STATE AND ARE LEFT AS WRITTEN;
THIS IS THE STATE AT THE ARCHIVE ACT OF 2026-08-27.** Groups 2, 3, 4 and 5 are
DISCHARGED and ticked, each group header naming its Spec Kit feature, pull
request and squash commit; six of their boxes carry a `RECONCILED` clause
because they were not discharged as written, and each names the feature decision
that disposed it. Group 8 is done. STILL OPEN, deliberately: § 1.2 (the five
orchestrator decisions were not vetoed, which is not the same as affirmatively
ruled), § 1.3 (the conditional cost of a D1 veto), § 7.1 (#330), § 7.2 (the
flip) and § 7.4 (the domain factories are unmeasured).

## 1. Ratification

- [x] 1.1 RATIFIED 2026-08-27 by Brett, in session, verbatim "Ratify as-is", on
      the packet as written at `06c7475a`. What follows is the original task text
      and it is left standing rather than rewritten, because it records what was
      put to him. No ruling covers any part of this. Issues
      #357, #329 and #330 establish the defect class and #357 proposes a check;
      the packet's `.openspec.yaml` records queue admission by the orchestrating
      session on those filed issues, and says in its own words that it is not an
      approval. Ratification is a separate act.
- [ ] 1.2 THE FIVE ORCHESTRATOR DECISIONS WERE NOT VETOED at the ratification of
      2026-08-27, and this box stays OPEN because not-vetoed is not the same as
      affirmatively ruled. Reverting any one of them remains an edit to this
      change rather than a new one. Each is independently
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

Discharged 2026-08-27 by Speckit F1 = specs/019-modified-block-currency-family
(PR #420, squash `19e3f6b5`); per-task evidence, RED-first records and the
mutation round live in that feature's tasks.md and evidence.

- [x] 2.1 FIRST, AND IN THE SAME COMMIT AS THE REGISTRATION: the `doc-health`
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
      **RECONCILED AS WRITTEN-STALE**: the basis clause "relative to
      `add-family-enumeration-check`'s outcome" could not apply, that change
      having archived at `f027d3b3` before F1 registered the family, so F1's T052
      wrote the block relative to CANON — F1 plan O10 (what a declared sibling's
      outcome is computed as) and F3 plan D2. Everything else in this box landed
      as specified, and § 8.2 records the 8 → 8 count and the six differences.
- [x] 2.2 `scripts/doc_health/modified_block_currency.py`. The active-change
      delta reader (`openspec/changes/*/specs/*/spec.md`, `archive/` excluded,
      every active change regardless of lifecycle standing), the
      promoted-requirement reader, the `## MODIFIED Requirements` section parser,
      and whitespace normalization.
- [x] 2.3 THE UNIT DERIVATION, IMPLEMENTED EXACTLY AS THE DELTA STATES IT: mask
      backticked spans before any sentence split; split on a period, question
      mark or exclamation mark followed by whitespace or end of paragraph; each
      body bullet line is one unit with its list marker stripped; each dated bold
      note is ONE undivided unit; each `#### Scenario:` heading is one title unit
      and each scenario bullet one bullet unit. Matching is same-kind and exact.
      CONTAINMENT AND SIMILARITY ARE BOTH FORBIDDEN — a test asserts that a block
      bullet CONTAINING canon's bullet still fires (§ 3.4).
- [x] 2.4 The three arms as three finding classes: scenario-title completeness
      (`warning`), the carriage ledger (`info`, one finding per requirement
      listing its uncarried units), and title resolution / two-writers
      (`warning`). Scenario bullets compare against ALL bullets of the block,
      never scenario by scenario. `_LAUNCH_SEVERITY` is a module constant so the
      flip in § 7.2 is one line beside one `FAMILY_RESOLUTION` row.
- [x] 2.5 The reserved-marker parser, two forms, recognized by form and never by
      prose: `**Removed from canon by <change-id> (<YYYY-MM-DD>):**` followed by
      the deleted units and a ` — <reason>`; and
      ``**Merged into `<destination scenario title>` by <change-id> (<YYYY-MM-DD>):**``
      followed by the superseded titles. Named units are CommonMark code spans,
      extracted in order per CommonMark — never by splitting on punctuation — and
      a unit containing backticks carries a longer fence. The merge DESTINATION
      is not a named unit. A marker is one PARAGRAPH and whitespace normalization
      applies to it, so a wrapped marker parses. A marker suppresses only units it
      names AND that are absent; a marker naming a present unit is itself
      reported; naming a scenario title also declares that scenario's canon
      bullets removed unless they appear elsewhere in the block. Marker paragraphs
      are excluded from the ledger in both directions, so a promoted marker never
      becomes text a later block must restate. No fuzzy matching on the marker.
- [x] 2.6 Title resolution, in order: the change's OWN `## RENAMED Requirements`
      block first — where it renames a promoted requirement to the modified title,
      the arms run against canon under the OLD name — then active sibling changes'
      ADDED and RENAMED blocks; a title resolving to none of those is reported.
- [x] 2.7 The two-writers resolution, ORDERING BY DECLARATION (ruled 2026-08-27,
      Brett, verbatim "By declaration" — § 7.3 is closed and this task is
      unblocked). The change whose own `proposal.md` names a sibling as a whole
      token IS the later writer; its block is measured against that sibling's
      outcome and must carry the sibling's additions. Verify exactly two things
      and infer nothing else: that exactly one of two active RATIFIED writers
      declares, and that the declaring block carries the other's additions.
      Neither declaring is a finding against both blocks; both declaring is a
      finding too. No `created:` date, folder name or commit timestamp is read —
      a second authority for an ordering one rule already owns is the defect
      "Explicit delta rule" names.
- [x] 2.8 The disposition read: `health/dispositions.yaml` in the aggregation
      checkout, entries naming this family with a `cite`, optionally narrowed by
      `requirement:`, in the shape `promotion_fidelity.py` already implements.
      Reuse that reader; do not write a second one.
- [x] 2.9 Registration: one import and one `FAMILIES` line in `families.py`, one
      `FAMILY_IDS` entry in `__init__.py`, one comment recording why the family
      is deliberately absent from `FAMILY_RESOLUTION`, and the `families.py`
      module docstring's owner list extended.
- [x] 2.10 `tests/doc-health/test_lifecycle_scan_set.py`: the twenty-second family
      classified as a non-reader of the lifecycle scan set. That test exists to
      fail loudly when a new family is added without classifying it.

## 3. Speckit F2 — fixtures and tests

Discharged 2026-08-27 by Speckit F2 = specs/020-modified-block-currency-fixtures
(PR #426, squash `76a2ad27`); per-task evidence, RED-first records and the
mutation round live in that feature's tasks.md and evidence.

- [x] 3.1 Regression fixture A — the #351 true positive, reconstructed.
      `add-doxchat-model-intake`'s pre-repair block against the canon of
      2026-08-25: six body clauses, two scenarios (`The menu offers a routing
      rule`, `A fourth provider verb is proposed`) and one reverted scenario line
      ("every loaded editor" → "the Outline and Document editors"). ACCEPTANCE:
      the scenario arm fires on the two scenarios by title; the ledger lists the
      six clauses AND the reverted line; assertions are on the rule text and the
      named units, never on a count.
- [x] 3.2 Regression fixture B — the #329 one-of-eight case. A MODIFIED block
      restating 1 of a promoted requirement's 8 scenarios, with the change's own
      ADDED requirement bringing 7 so the file-level scenario count stays flat.
      ACCEPTANCE: the family fires naming all seven omitted titles, and a second
      assertion pins that the flat file-level count is not what the family reads.
      **RECONCILED AS WRITTEN-STALE**: there is no revert in that history and no
      ratified document claimed one — the "reverted first archive attempt"
      phrasing came from a session brief (F2 review finding B4). The truncated
      block was caught pre-commit and rewritten scenario-complete inside the
      archive commit `38b548d4` itself (merged to main as squash `b03b9992`,
      PR #331 — `38b548d4` is branch-only and is NOT reachable from `main`, while
      the recovery point `d5f447e8` is), so the fixture is byte-faithful from that
      commit's PARENT `d5f447e8`, reconstructed from git with its SHAs in the
      fixture README (F2 plan D2).
- [x] 3.3 Red test — retitle and gut. Rename a scenario, declare the rename with
      a `Merged into` marker, and drop two of the superseded scenario's four
      bullets. ACCEPTANCE: the scenario arm is quiet (the marker is valid) AND
      the ledger reports the two dropped bullets — a `Merged into` marker names
      titles only, so bullets a merge makes redundant must be carried or named in
      a `Removed from canon` marker of their own. A companion case names them
      there and asserts the ledger goes quiet.
- [x] 3.3a Red test — the COMBINATION, which is where the two marker rules could
      contradict each other. A `Removed from canon` marker naming the old
      scenario title, AND a replacement scenario the promoted requirement does
      not carry, carrying two of the old scenario's four bullets. ACCEPTANCE: the
      two uncarried bullets are reported. Suppressing them would let a retitle
      relabelled as a removal drop obligations with nothing reported — B5 through
      the permissive marker — so this fixture covers the COMBINATION rather than
      each branch alone, and the genuine-removal case (marker, no new scenario
      title, nothing reported) is asserted beside it. This test fails under any
      scenario-paired bullet comparison and is the reason the delta compares
      bullets across the whole block.
- [x] 3.4 Red test — containment is not carriage. A block bullet that CONTAINS
      canon's bullet verbatim as a substring, widened at either end. ACCEPTANCE:
      the ledger reports canon's bullet as uncarried. This is #351's widening
      mechanism and the case the first draft of the delta would have missed.
- [x] 3.5 Tokenization fixture — a requirement body carrying backticked tokens
      with internal periods (`.openspec.yaml`, `promotion_fidelity.py`,
      `contract-v1.45`), a body bullet list, and a dated bold note spanning
      several sentences. ACCEPTANCE: no unit boundary falls inside a backticked
      span; each bullet is one unit; the note is ONE unit; and an edit to the
      note's third sentence reports the note once, not three times.
- [x] 3.6 Negative — a scenario-complete block stays quiet, including one that
      re-wraps every paragraph it carries. The case line-level matching fails.
- [x] 3.7 Marker tests. A valid `Removed from canon by` marker suppresses exactly
      the units it names and leaves an unnamed sibling reported. A marker naming a
      unit the block still carries is itself reported. A marker wrapped across
      several lines parses as one. A named unit that itself contains backticks —
      a clause citing `openxFactory` — is fenced with a longer run and is
      extracted whole, not truncated at its first inner backtick. A paragraph
      that merely quotes or templates a marker — as this change's own two deltas
      both do, in prose that promotes into canon — is NOT of marker form and
      stays an ordinary carriage unit; the form test anchors on the complete
      prefix, change-id and ISO date included. A named
      SCENARIO TITLE suppresses that scenario's canon bullets too, and this is
      asserted directly: a four-bullet scenario named in a `Removed from canon`
      marker reports NOTHING at `info`, while the same scenario with one of its
      bullets surviving elsewhere in the block reports nothing either, because
      the survivor is carried — and this holds ONLY where the block adds no new
      scenario title; § 3.3a pins the other branch. A `Merged into` marker's
      DESTINATION title, which
      is present in the block, is not read as a named unit — the pin that stops
      every valid merge marker reporting itself. A prose dated bold note that is
      not one of the two reserved forms suppresses nothing: the guard on the
      finding that canon's own restoration notes must never be read as
      declarations of deletion. And a marker paragraph is not a carriage unit —
      a block whose canon requirement already carries a promoted marker is not
      required to restate it.
- [x] 3.8 Negative — a MODIFIED title resolving to an active sibling's ADDED
      stays quiet (pending, not absent). Positive — the same title with no
      sibling and no canon requirement fires.
- [x] 3.9 Own-rename — a change carrying both `## RENAMED Requirements` and a
      MODIFIED block under the new title resolves against its own rename first,
      and the three arms compare it to canon under the OLD name. Without this the
      family would report every rename-and-amend change as unresolved, and would
      compare nothing where it should compare everything.
- [x] 3.10 Two-writers, by declaration. The DECLARING block missing the
      sibling's addition fires; carrying it stays quiet. Neither of two active
      ratified writers declaring fires against both blocks; both declaring fires
      too. A declaration naming a change id INSIDE a longer id buys nothing
      (whole-token match). Pin that an unratified sibling creates NO reference
      obligation, so the `ratified` scoping of `release-realization`'s rule is
      not silently widened. And pin that NO date, folder name or commit
      timestamp is consulted — a test that would pass under date ordering and
      fail under declaration ordering, so the withdrawn reading cannot creep
      back.
- [x] 3.11 Structural pins on the advisory launch, both halves, so a half-flip in
      either direction fails: `_LAUNCH_SEVERITY` is not `error`, and
      `"modified-block-currency"` is absent from `FAMILY_RESOLUTION`.
- [x] 3.12 A scope with no `openspec/changes/` directory reports SKIPPED with its
      reason; a scope WITH active changes but no MODIFIED block reports nothing
      and is NOT skipped. The two are different states and canon's skip rule is
      "cannot run", not "found nothing".
- [x] 3.13 Determinism: two runs over one fixture tree produce byte-identical
      findings, including ordering.

## 4. Speckit F3 — the self-gate against this repository

Discharged 2026-08-27 by Speckit F3 = specs/021-modified-block-currency-self-gate
(PR #427, squash `f728d57f`); per-task evidence, RED-first records and the
mutation round live in that feature's tasks.md and evidence.

- [x] 4.1 The family runs against this repository's own tree, through the family
      itself rather than by inspection, and the result is asserted. Expected with
      § 2.1's block present, from § 6: 1 scenario-arm finding, 11
      carriage-ledger findings, 0 title-resolution findings. Assert the
      scenario-arm finding by its named subject (`add-composed-view-authoring` /
      `Gate verbs hide on a composed view`) so the test cannot pass vacuously.
      **RECONCILED AS WRITTEN-STALE**: the `11 carriage-ledger findings` figure
      was taken at `9be81a40` over 23 MODIFIED blocks and this tree carried 22,
      so the gate asserts the re-measured truth — +1 `warning`, +9 `info` at
      `76a2ad27`, then +8 after merging `origin/main` — and names the packet's
      numbers as history rather than asserting a count the tree no longer
      produces (F3 plan D1).
- [x] 4.2 The family reads its own packet. Assert that this change's own § 2.1
      delta is among the blocks examined and that it is measured against
      `add-family-enumeration-check`'s outcome, so § 4.1 cannot pass because
      discovery quietly stopped working.
      **RECONCILED AS WRITTEN-STALE**: there is no sibling outcome in this tree
      to measure against, so the gate asserts this box's PURPOSE — that discovery
      reached the packet's own delta — plus the basis that does exist and the
      sibling's absence (F3 plan D2). This group then fell due at the archive act
      itself and was disposed there: see § 8.1, two assertions re-aimed at the
      archived path and one retired with its dated record.
- [x] 4.3 The whole suite: `python3 -m pytest tests/doc-health` green, count
      recorded before and after so the added tests are visible as a delta.
- [x] 4.4 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, count
      recorded.
- [x] 4.5 The report moves by exactly the prediction and in no other line.
      `python3 scripts/doc-health.py` single-repo, diffed against the same run on
      `main`: +1 `warning`, +11 `info`, 0 `error`, 0 `critical`, headline
      unchanged, census / inventory / catalog untouched. Movement anywhere else
      is a defect in this change.
      **RECONCILED AS WRITTEN-STALE, SAME CAUSE AS § 4.1** (F3 plan D1): the
      invariant asserted is that the movement EQUALS the family's own
      per-severity counts and that `error`/`critical` do not move — held at
      +1/+9, at +1/+8 (F4's gate) and at +1/+7 (after this archive act), with
      the movement confined to 3 of the report's 30 headings.

## 5. Speckit F4 — reporting and workflow

Discharged 2026-08-27 by Speckit F4 = specs/022-modified-block-currency-reporting
(PR #433, squash `4def2274`); per-task evidence, RED-first records and the
mutation round live in that feature's tasks.md and evidence.

- [x] 5.1 The family renders its own report section with the three arms
      distinguishable rather than summed — a reader must see one scenario-arm
      warning next to eleven editorial rows without counting.
- [x] 5.2 The action line: "restate the requirement as canon currently states it,
      or declare the deletion with a `Removed from canon by` marker". No existing
      family's action line says this, which is part of D1's argument.
      **RECONCILED AS ALREADY-LANDED**: F1 had already shipped the action line,
      so F4 realized this box as a PIN rather than an addition — and F4's Phase 0
      recorded the second imprecision beside it, that the singular is wrong
      because the family has TWO action lines. Both findings were carried to
      review rather than worked around (F4 research/plan Phase 0, pr-body
      § Two imprecisions in § 5).
- [x] 5.3 NO workflow change is expected. `.github/workflows/doc-health-reusable.yml`
      passes no per-family option to this family and must not: the live-`main`
      basis belongs to `promotion-fidelity` alone, and this family measures the
      checkout by contract. Pin the boundary by a NEW test of this family's own —
      `test_workflow_contract.py` pins that boundary for `promotion-fidelity` in a
      shape written for that family, and this is a new assertion rather than a
      reuse of that pin.

## 6. Evidence recorded at proposal time

- [x] 6.1 The spike, run under the matching rule exactly as the delta writes it:
      same-kind exact units, backtick-masked sentence split, bullets compared
      across the whole block. Every active change under
      `openspec/changes/*/specs/*/spec.md` (`archive/` excluded) against
      `openspec/specs/*/spec.md`, at `9be81a40`. Not committed.
- [x] 6.2 The three arms, measured separately over 23 MODIFIED requirements at
      the branch point: scenario-title losses **1**; ledger **14 units** (10
      body, 4 scenario-bullet) across **10 requirements**; title-resolution
      **0**. Reported as **+1 warning, +10 info**.
- [x] 6.3 The single scenario-arm finding: `add-composed-view-authoring` /
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
- [x] 6.5 The D5 experiment. The enumeration MODIFIED block was written
      (twenty-one → twenty-two, 8 of 8 scenarios) and `fam_family_enumeration`
      run against the resulting tree: 3 findings, and
      `test_the_real_corpus_reads_zero_on_both_halves` FAILED. Withdrawn to
      § 2.1; with it removed the same call reads 0.
- [x] 6.6 The realization prediction, measured with § 2.1's block present.
      Measured against `add-family-enumeration-check`'s outcome, § 2.1's block
      does not carry two body sentences — the enumeration sentence and the "Four
      of the twenty-one" sentence — so it adds ONE ledger finding: **16 units
      across 11 requirements, +1 warning and +11 info**. It also creates the
      corpus's first two-writers instance between two ACTIVE changes. The spike
      first resolved "later" by `.openspec.yaml` `created:`; that reading is
      WITHDRAWN by the ruling of 2026-08-27 (§ 7.3, "By declaration"). The figure
      does not move, because this change's proposal declares itself relative to
      `add-family-enumeration-check` and that change names nothing, so the
      declaration selects the same basis the date reading had guessed.
- [x] 6.7 The two-writers arm measured zero, and RE-MEASURED zero under the
      ruled by-declaration rule. Seven `(capability, requirement)` pairs are
      written by two active changes; all seven are
      MODIFIED-over-a-sibling's-ADDED, so seven MODIFIED titles are pending on a
      sibling's addition and zero resolve to nothing. Pairs where two active
      changes both MODIFY one requirement: **0** at the branch point, **1** with
      § 2.1 present — `add-family-enumeration-check` and this change on
      "Deterministic check families", both `ratified`, with exactly one declaring
      (this one). **0 findings either way.** Compliance was 7 of 7 on the
      reference under the pre-ruling reading and is not an obligation on the
      MODIFIED-over-ADDED shape under the ruled one, which scopes the declaration
      to two writers who both MODIFY.
- [x] 6.8 Canon's state confirmed, not assumed: `openspec/specs/doc-health/spec.md`
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
- [x] 7.3 **RULED 2026-08-27 — BY DECLARATION.** Brett, in session, verbatim
      "By declaration": the change that writes "relative to <sibling>" IS the
      later writer; the check only verifies that the declaration exists and that
      the declaring block carries the sibling's additions; no date arithmetic.
      This matches `release-realization`'s existing spelling rather than adding a
      second authority, which is why the `.openspec.yaml` `created:` reading the
      spike used is WITHDRAWN. Written into the doc-health delta's
      title-resolution bullet and two scenarios, the document-lifecycle delta's
      two-writers paragraph and scenario, design D4, and § 2.7 — which is
      unblocked. Re-measured under the ruled rule: 0 two-MODIFIED pairs at the
      branch point, 1 with § 2.1 present, 0 findings either way.
- [ ] 7.4 THE DOMAIN FACTORIES ARE UNMEASURED. This change's evidence is
      openxFactory's active changes and a fixture corpus; what the pinned
      domains' active changes will say is unknown, and is why the launch is
      advisory.
- [x] 7.5 **RULED 2026-08-27 — ADMISSION RECORDED.** Brett, in session,
      verbatim "Record your admission now": `.openspec.yaml` names him as
      approver on 2026-08-27, in the same shape
      `create-medxchart-overlay-boundary` uses, and the packet is
      `Status: ratified` with a record-citing citation. **ISSUE #318 ITSELF
      STAYS OPEN**, and this ruling does not close it: the taxonomy still has no
      origin kind that expresses "proposed, not approved", so the next packet
      drafted before approval sits in the same gap this one sat in from
      2026-08-27's authoring until the ratification later the same day. That is
      another capability's rule to fix.

## 8. Archive

- [x] 8.1 ARCHIVE AFTER REALIZATION AND AFTER THE MERGE. This change ships active
      and archives only once the realization is merged to `main` and green:
      `pytest tests/doc-health`, `openspec validate --all --strict`, and a
      doc-health run moving by exactly § 4.5's prediction. The archive act is a
      separate later commit titled for the merge it follows, per
      `add-promotion-fidelity-check` (`01ff3434`) and
      `add-family-enumeration-check`.
      **DONE — ARCHIVED 2026-08-27, on the merge-plus-green rule this box
      declared.**
      **REALIZATION RE-VERIFIED FROM `main` AT THIS GATE, not read out of a PR
      body.** All four Speckit merges were re-confirmed ancestors of
      `origin/main` with `git merge-base --is-ancestor` (exit 0 on each):
      1. **PR #420 → `19e3f6b5`** — F1, `019-modified-block-currency-family`:
         the family module and its three registrations, and § 2.1's own
         MODIFIED block written in the same commit as the registration.
      2. **PR #426 → `76a2ad27`** — F2, `020-modified-block-currency-fixtures`:
         the regression catalogue, #351 and #329 reconstructed from history.
      3. **PR #427 → `f728d57f`** — F3, `021-modified-block-currency-self-gate`:
         the self-gate against this repository, by named subject.
      4. **PR #433 → `4def2274`** — F4, `022-modified-block-currency-reporting`:
         the report section counting the finding classes apart, the action-line
         pin, and the workflow-boundary pin.
      The live tree carries the ADVISORY launch in both halves, re-read here
      rather than assumed: `modified-block-currency` is registered in `FAMILIES`
      (22 entries), present in `FAMILY_IDS`, and ABSENT from
      `FAMILY_RESOLUTION` — so § 7.2's flip is still owed and still unticked.
      **THE GATE NUMBERS, all measured in this worktree at base `4def2274`.**
      Before the archive act: `python3 -m pytest tests/doc-health -q` → **1209
      passed, 0 failed**; `OPENSPEC_TELEMETRY=0 openspec validate --all
      --strict` → **76 passed, 0 failed (76 items)** = 24 active + 52 promoted
      specs; `python3 scripts/doc-health.py --single-repo .` → **5 critical, 7
      error, 41 warning, 12 info. New regressions vs previous report: 0**, and
      the same run with `--skip-family modified-block-currency` → **5 critical,
      7 error, 40 warning, 4 info** — movement **+1 `warning`, +8 `info`, 0
      `error`, 0 `critical`**, equal to the family's own per-severity counts
      (`--family modified-block-currency` → 1 warning, 8 info) and to F4's
      re-measured figure. After the archive act: pytest **1209 passed, 0
      failed**; validate **75 passed, 0 failed (75 items)** = 23 active + 52
      specs, −1 exactly as promotion of one change predicts; the single-repo run
      **5 critical, 7 error, 41 warning, 11 info, 0 new regressions** against
      **5 critical, 7 error, 40 warning, 4 info** skipped — movement **+1
      `warning`, +7 `info`**. The gated bands do not move in either
      measurement, so a run configured `--fail-on error` is unaffected by
      construction, which is what D3's advisory launch claimed.
      **§ 4.5'S AUTHORED PREDICTION IS HISTORY AND IS NOT WHAT THIS GATE
      MEASURED.** It said `+1 warning, +11 info`, measured at `9be81a40` over 23
      MODIFIED blocks; F3 re-measured 9 then 8 as `add-hermes-customer-subject-
      runtime-contract` and `add-shared-identity-seeds` archived and as PR #424
      renamed a repository in canon and in the active delta quoting it, in one
      commit. The invariant that must hold, and does at every one of those
      figures, is that the movement EQUALS the family's own counts and that
      `error`/`critical` do not move. The ledger arm is advisory precisely
      because its population moves.
      **THE ONE INFO THE ACT ITSELF REMOVED IS THE SELF-FINDING, and its
      departure is the promotion working.** Before the act the family drew 8
      `info`, one of them against this packet's own § 2.1 block naming the two
      canon sentences it did not carry. The act promoted that block, so those
      two sentences ARE canon now, the packet left the active set, and the
      family — which excludes `openspec/changes/archive/` in its reader — draws
      7. Active MODIFIED blocks examined: **22 → 21**.
      **GROUPS 2–5 ARE TICKED, AND EACH GROUP HEADER NAMES THE EVIDENCE — RULED
      AT THIS GATE.** The four features above discharged them, but each was built
      as a Spec Kit feature with its own `tasks.md` and no session ticked this
      packet's boxes as it went. This session's first instinct was to leave them
      open and record why; that was OVERRULED on the ground that an archived
      change carrying thirty-two open build boxes reads as
      archived-UNREALIZED to a cold reader, which is a worse record than a tick
      that names its evidence. So every box in groups 2, 3, 4 and 5 is ticked and
      each group header carries ONE dated discharge line naming its feature, its
      pull request and its squash commit — `specs/019-modified-block-currency-family`
      (#420, `19e3f6b5`), `specs/020-modified-block-currency-fixtures` (#426,
      `76a2ad27`), `specs/021-modified-block-currency-self-gate` (#427,
      `f728d57f`), `specs/022-modified-block-currency-reporting` (#433,
      `4def2274`) — with the per-task evidence, the RED-first records and the
      mutation rounds staying where they were written rather than being copied
      here. The last of the four carries `evidence/f4-gates.md`, whose
      archive-readiness numbers this gate re-measured rather than trusted.
      **SIX BOXES WERE NOT DISCHARGED AS WRITTEN AND SAY SO WHERE THEY STAND**,
      each ticked with a `RECONCILED` clause naming the feature decision that
      disposed it rather than being ticked silently: § 2.1's sibling-outcome
      basis (F1 O10, F3 D2 — the sibling had archived, so the block was written
      relative to canon), § 3.2's revert (F2 B4/D2 — no revert exists; the
      fixture is byte-faithful from the archive commit's parent), § 4.1 and
      § 4.5's `+11 info` (F3 D1 — a figure taken over 23 blocks against a tree
      carrying 22, re-measured rather than asserted), § 4.2's sibling basis
      (F3 D2, and disposed again by this act), and § 5.2's action line (F4
      Phase 0 — already landed by F1, so realized as a pin, with the singular's
      imprecision recorded beside it). § 7 and § 1.2 are untouched.
      **THE WHOLE REPORT DIFF IS SEVEN LINES AND ONLY TWO OF THEM ARE A
      FINDING.** Canon words 208551 → 213280 (+4729) and governance words
      664611 → 669340 (the SAME +4729, those words moving from active-change
      prose into promoted prose), canon share 31.4% → 31.9%, the promoted-specs
      row of the per-source table (148998 → 153727), the headline's `info`
      12 → 11, the family's own class subtotal `carriage ledger: 8` → `7`, and
      the two lines — the finding row and its ranked-plan row — of the departed
      self-finding. Nothing new is reported anywhere, by any family.
      **FIVE TESTS FELL DUE AT THIS ACT — FOUR PREDICTED BY F3 AND A FIFTH ITS
      LIST DID NOT CARRY. NONE WAS DELETED AND NO MODULE CHANGED.** F3's
      `quickstart.md` § WHEN THE GATE FAILS named this exact day FIRST among the
      movements it expected, and recorded the disposition: re-aim to the ARCHIVED
      path where the family's reader can be pointed there without a module change
      — a change of SUBJECT, the family excluding `archive/` — else retire with a
      dated record, never delete silently. Applied, in
      `tests/doc-health/test_modified_block_currency_self_gate.py`:
      1. `_LEDGER_SUBJECTS` drops the `add-modified-block-currency-check` /
         `doc-health` / `Deterministic check families` triple, **8 → 7**, with
         the dated comment recording why, in the shape the row PR #424 removed
         already used.
      2. `_own_block()` → `_archived_block()`, RE-AIMED: the block is read at
         `openspec/changes/archive/2026-08-27-add-modified-block-currency-check/specs/doc-health/spec.md`
         through `mbc.parse_delta` and `mbc.derive_units` — the two calls
         `active_blocks` itself makes on every block it returns — so the gate
         still reaches the corpus only through the family and owns no second
         parser. `active_blocks` itself cannot be pointed there: it excludes
         `openspec/changes/archive/` in its reader by construction.
      3. `test_this_change_s_own_delta_is_among_the_blocks_the_family_examined`
         → `test_the_packet_s_own_block_sits_at_its_archived_path_and_out_of_reach`,
         RE-AIMED. The discovery claim one document over, in BOTH directions: the
         block is readable at the archived path, AND no active block comes from
         this change or from any archived path at all — which pins that reader's
         own exclusion against the REAL tree for the first time, F2's fixtures
         having been the only cover for it until now.
      4. `test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists`
         → `test_the_archived_block_still_resolves_to_canon_and_no_active_writer_holds_it`,
         RE-AIMED. All three original claims asserted about the tree as it now
         stands: `resolve()` on the archived block returns basis
         `openspec/specs/doc-health/spec.md` with status `canon`; this packet and
         `add-family-enumeration-check` are each archived exactly once and neither
         is active; and the ordering arm applies no basis override, the
         active-writer count on the requirement moving 1 → **0** because the last
         one promoted. Deliberately NOT coupled to canon's TEXT — canon's wording
         moves with every family that lands, and what it says is
         `family-enumeration`'s business, pinned in that family's own suite.
      5. `test_the_self_finding_quotes_this_change_s_two_stale_numeral_sentences`
         → `test_the_self_finding_is_retired_by_the_archive_act`, **RETIRED with
         its dated record in its own docstring** — the one member of the group
         that could not be re-aimed, and the reason is stated rather than
         implied: the other two are about DOCUMENTS and a document can be read at
         another path, while this one is about a FINDING, and the family draws
         findings against ACTIVE deltas only. Manufacturing an archived
         counterpart would widen the family's scope inside a test instead of
         inside its module. The docstring records what it proved and until when;
         two residual assertions replace it, each carrying a claim of its own
         rather than standing in for the retired one — no finding
         names either path this packet ever had (the check that made the ledger
         row above safe to remove), and the FROZEN archived block carries
         `twenty-two check families` and `Four of the twenty-two` and NOT the
         `twenty-one` forms, which preserves the DIRECTION claim the original
         existed for: the finding named what CANON stated, so `twenty-one` was
         the correct thing to find there.
      6. THE FIFTH TEST, IN F2's FILE, WHICH F3's LIST DID NOT NAME:
         `test_modified_block_currency_fixtures.py::test_the_packets_own_marker_templates_are_not_marker_form`
         read the packet's own ACTIVE delta to prove its two marker TEMPLATE
         bullets are ordinary carriage units rather than marker form. RE-AIMED to
         `openspec/specs/doc-health/spec.md` — and the re-aim is that test's own
         claim arriving, because its docstring argued the strict anchor matters
         "precisely because these paragraphs promote into canon", and now they
         have. The subject it reads is now the promoted text rather than a
         prediction about it, and its count floor of two is untouched.
      UNTOUCHED BY THE ACT, and it matters which: the resolver guard, the
      discovery floor, the scenario-arm subject, the three zero-read classes, the
      structural pins on the advisory launch, the movement pin — stated as a
      DIFFERENCE against the family's own per-severity counts, so `+1 / +7`
      needed no edit at all — and the two-attribute context pin. The gate's regex
      set is unchanged: three names joined the `mbc.*` allowlist (`ActiveBlock`,
      `derive_units`, `parse_delta`) and not one pattern.
      **`fam_family_enumeration` NOW READS CANON ALONE, AND READS ZERO.** With no
      active change restating "Deterministic check families",
      `_delta_statements` returns nothing and its own re-aimed
      `test_canon_is_the_statement_under_test` measures canon instead:
      `twenty-two`, **22 names, 22 registered, 0 unresolved, 0 findings** — the
      count chain this packet moved, closing against the live registry.
- [x] 8.2 AT THE ARCHIVE GATE, VERIFY THIS CHANGE'S OWN PROMOTION BYTE-FOR-BYTE,
      per requirement, in both capabilities, and resolve the § 2.1 ordering
      against `add-family-enumeration-check` explicitly rather than by whichever
      archives first. A change whose subject is lossy promotion that promoted
      lossily would be the worst possible entry in this record. Record the
      per-requirement scenario counts before and after.
      **DONE 2026-08-27, BEFORE THE ACT, IN BOTH CAPABILITIES.**
      **THE § 2.1 ORDERING, RESOLVED BY THE RECORDED D5 SEQUENCING AND NOT BY
      WHICHEVER ARCHIVED FIRST.** `add-family-enumeration-check` archived FIRST,
      at `f027d3b3` (PR #419), which is the precondition D5 priced and that
      packet's own § 2.5 records paying: a proposal that registers no family
      cannot lawfully restate the requirement at twenty-two, so the sibling had
      to promote its twenty-one first. Its enumeration was therefore already
      CANON when F1 wrote § 2.1's block, so the block was written relative to
      canon — `release-realization`'s "declare relative to that change's
      outcome" discharged by the outcome having become canon, not by a
      two-writers basis substitution. Proven at this gate rather than reasoned:
      canon's "Deterministic check families" requirement is byte-IDENTICAL
      between `f027d3b3` and this base `4def2274` — extracted from both trees
      and diffed, **0 hunks** — so canon did not move under this packet and the
      block reverts nothing. The one commit touching the promoted spec since
      (`49f0c18c`, `govern-derived-pin-reachability`'s archive) appended a
      requirement at the end of the file and left this one alone. Measured
      through the family's own ordering arm as well: ZERO two-MODIFIED pairs on
      this requirement, so `_arm_ordering` applied no basis override and emitted
      nothing, which is what § 6.6's re-measurement under the ruled
      by-declaration rule predicted.
      **TABLE 1 — `doc-health`, per requirement.**
      | requirement | canon before | delta | canon after | verdict |
      | --- | --- | --- | --- | --- |
      | `Deterministic check families` (MODIFIED) | 8 scenarios; 12 body units + 27 scenario bullets = 39 units | 8 scenarios restated; 13 body units + 28 bullets | 8 scenarios | **8 → 8**; titles an identical SET in identical ORDER; 7 of 8 byte-identical bullet for bullet; all 3 dated bold notes byte-identical; exactly SIX differences |
      | `Currency of an active change's MODIFIED requirement blocks` (ADDED) | absent | 14 scenarios | 14 scenarios | pure append; the title collides with NONE of canon's 34 |
      | the other 33 requirements | — | untouched | unchanged | bytes identical, per requirement, and the file order of all 34 pre-existing titles preserved |
      | FILE | 34 requirements, 145 scenarios | — | 35 requirements, 159 scenarios | +1 requirement, +14 scenarios |
      **THE SIX DIFFERENCES, NAMED RATHER THAN GLOSSED.** (1) the total numeral,
      canon `SHALL implement twenty-one check families` → block `twenty-two`;
      (2) the enumeration gains one name, canon `… duplicate packet, and family
      enumeration.` → block `… duplicate packet, family enumeration, and
      modified-block currency.`; (3) `Four of the twenty-one` → `Four of the
      twenty-two`; (4) `the other seventeen families` → `the other eighteen
      families`; (5) ONE new body sentence, the measurement-basis declaration
      beginning "The modified-block currency family reads ACTIVE CHANGE
      DELTAS…"; (6) ONE new `AND` bullet in `A run executes the check families`,
      12 → 13 bullets, reading "**AND** modified-block currency MUST compare
      each active change's `## MODIFIED Requirements` blocks against the
      promoted requirements they replace as its owning requirement below
      defines". Differences 1–2 are ONE canon sentence and 3–4 are ANOTHER, so
      exactly TWO canon body units are not carried.
      **AND THAT IS EXACTLY WHAT THE FAMILY ITSELF REPORTED AGAINST THIS BLOCK —
      THE CHECK VERIFIED ITS OWN BLOCK.** Run over this tree before the act, the
      family drew ONE `info` against
      `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`
      reading "does not carry 2 of the 39 body units and scenario bullets", and
      the two units it quoted are canon's `twenty-one check families` sentence
      and canon's `Four of the twenty-one` sentence — canon's wording, not the
      block's, which is the correct direction. This gate's independent
      derivation of the same unit set agreed with it unit for unit, 39 for 39,
      which is the dogfooding § 6.6 predicted and F1's O2 recorded as evidence
      never to be dispositioned.
      **SCENARIO-BY-SCENARIO, 8 → 8.** `A run executes the check families`
      12 → 13 bullets (difference 6, the other twelve byte-identical);
      `Lifecycle conformance checks fire` 2/2, `A register carries staged
      status` 2/2, `Drift checks fire` 2/2, `Catalog conformance checks fire`
      2/2, `Routing conformance checks fire` 2/2, `Origin conformance checks
      fire` 2/2, `Roster composition is checked across domains` 3/3 — all seven
      IDENTICAL.
      **TABLE 2 — `document-lifecycle`, per requirement.**
      | requirement | canon before | delta | canon after | verdict |
      | --- | --- | --- | --- | --- |
      | `A MODIFIED requirement block restates the requirement as canon currently states it` (ADDED) | absent | 5 scenarios | 5 scenarios | pure append; the title collides with NONE of canon's 16 |
      | the 16 pre-existing requirements | — | untouched | unchanged | bytes identical, per requirement, order preserved |
      | FILE | 16 requirements, 72 scenarios | — | 17 requirements, 77 scenarios | +1 requirement, +5 scenarios |
      The delta carries ONLY an `## ADDED Requirements` section — no MODIFIED,
      no REMOVED, no RENAMED — so there is no promotion direction in which it
      could delete anything.
      **CANON AFTER THE ACT IS WHAT THE TWO DELTAS IMPLY AND NOTHING ELSE.**
      `git diff openspec/specs/` → **2 files changed, 404 insertions(+), 5
      deletions(-)**. All five deletions are in `doc-health` and all five are
      re-wrapped lines of the two numeral sentences plus the one continuation
      line the new basis sentence extends; `document-lifecycle` has **ZERO**
      deletions. Proven per requirement and then as a BYTE DIFF OF THE
      REMAINDER — the remainder being the whole document minus the one MODIFIED
      requirement and the one appended requirement, each requirement running from
      its `### Requirement:` line to the next one or to EOF. Byte-identical
      before and after, RAW and again after trailing-newline normalization:
      `doc-health` **88197 vs 88197** raw, 88196 vs 88196 normalized;
      `document-lifecycle` **48653 vs 48653** raw, 48652 vs 48652 normalized.
      Preambles identical, no title removed, every pre-existing title still in
      its original position, and both files still ending in a blank line before
      and after, so no appended requirement consumed an EOF newline.
      **RESOLVED 2026-08-27** by `record/rederive-mbc-archive-remainder`: re-
      derived byte-for-byte from `4def2274`/`8997e00b`. **doc-health 88343 ==
      88343 raw (88341 normalized); document-lifecycle 48731 == 48731 raw
      (48729 normalized)** — equality holds, as both readings agreed; neither
      pair matches this exactly. **N2 EXPLAINED**: `split('\n### ')` + drop +
      `'\n'.join` reproduces 88343/88342 and 48731/48730 verbatim — lossless
      except when the dropped chunk is the file's LAST heading, true only of
      the appended requirement, costing one join newline on `after` alone; no
      EOF blank line is truly consumed. The session's own 88197/48653 pair
      could not be reproduced by any construction tried and stays unexplained,
      though self-consistent like the true figure. N2 is discharged by this
      derivation.
