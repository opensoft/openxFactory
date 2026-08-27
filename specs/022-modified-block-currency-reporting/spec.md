# Feature Specification: modified-block currency — reporting and workflow

**Feature Branch**: `022-modified-block-currency-reporting`

**Created**: 2026-08-27

**Status**: Draft

**Input**: Speckit F4 of `add-modified-block-currency-check`: the family's report
section renders its four finding classes distinguishably (per-arm subtotals under
the family heading, other families byte-identical), carries its action line —
restate the requirement as canon currently states it, or declare the deletion
with a `Removed from canon by` marker — and pins that no workflow option reaches
the family, with no workflow change.

## Provenance and scope boundary

This is **F4, the last of four Speckit features** realizing the ratified OpenSpec
change `add-modified-block-currency-check`. Its scope is that packet's
`tasks.md` **§ 5 "Speckit F4 — reporting and workflow" (5.1–5.3)** and nothing
else.

| feature | packet § | landed |
| --- | --- | --- |
| F1 `019-modified-block-currency-family` | § 2 the family module + registrations | `19e3f6b5` |
| F2 `020-modified-block-currency-fixtures` | § 3 fixtures and tests | `76a2ad27` |
| F3 `021-modified-block-currency-self-gate` | § 4 the self-gate | `f728d57f` |
| **F4 (this feature)** | **§ 5 reporting and workflow** | — |

**What F4 does NOT do.** It does not change what the family measures, which
documents it reads, its severities, its resolution-class absence, its rule texts,
or the finding/ranked-plan grammars. It does not tick or perform the packet's
§ 8 archive act — F4 is that act's precondition and leaves the tree
archive-ready. It does not decide F3's open question (below). It does not touch
`.github/` or `openspec/`.

**One question stays OPEN and is carried forward, not answered here.** F3's
hand-off records the blast radius of an exact-set corpus gate inside a REQUIRED
check (`_LEDGER_SUBJECTS` in `test_modified_block_currency_self_gate.py`, against
`pytest-suite` on `main`, org ruleset 21538893). It is Brett's call. This feature
ships F3's § 4 intent unchanged and repeats the question in its own hand-off and
PR body.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The reader sees the arms apart, without counting (Priority: P1)

A reviewer opens the nightly doc-health report at
`### modified-block-currency`. The family emits one gate-bearing `warning` and a
standing population of editorial `info` rows, all of them long — each row quotes
the requirement title, the promoted spec path, and up to two elided units. Today
the only way to learn "one scenario was dropped, and eight blocks diverge
editorially" is to read every row and tally it.

After this feature, the split is stated once, under the family's own heading,
before the rows: each of the family's four finding classes named, with its count
and its severity band.

**Why this priority**: § 5.1 is the packet's requirement and the reason the delta
split the arms in the first place — "so that a precise signal is never buried in
an editorial one" (`doc-health` delta, "three comparison arms"). The split exists
in the finding classes already; F4 is where it reaches the reader.

**Independent Test**: render a report from a known finding set and assert the
subtotal block appears under the family's heading with the per-class counts, and
that the counts equal the rows below them.

**Acceptance Scenarios**:

1. **Given** a run in which the family reports 1 scenario-title finding and 8
   carriage-ledger findings, **When** the report renders, **Then**
   `### modified-block-currency` carries a subtotal block naming all four
   classes, reading 1 / 8 / 0 / 0, before the first finding row.
2. **Given** a run in which the family reports nothing, **When** the report
   renders, **Then** the subtotal block still appears, all four classes reading
   0, above `No findings.` — a clean run states which classes were measured
   rather than leaving "No findings." to be read as a verdict about classes
   nobody named.
3. **Given** a run configured `--skip-family modified-block-currency`, **When**
   the report renders, **Then** the family's section carries its skip reason and
   NO subtotal block — a skip is the absence of a measurement, and a subtotal of
   zeros beside it would claim one.
4. **Given** a scope with no `openspec/changes/` directory, so the family
   returns its own `Skip`, **When** the report renders, **Then** the section
   carries that skip reason and no subtotal block, exactly as in scenario 3.
5. **Given** a finding this family emitted that its own class map does not
   place, **When** the report renders, **Then** the subtotal block carries a
   named residual line rather than dropping the finding from the tally — the
   counts always sum to the rows.

---

### User Story 2 - Every finding names the remedy, and nothing else moves (Priority: P1)

A session working the ranked plan reads a `modified-block-currency` row and needs
to know what to do about it. The remedy is not "edit the block until the check
goes quiet": it is to restate the requirement as canon currently states it, or to
declare the deletion with a `Removed from canon by` marker — the two acts the
family's own delta admits, and a line no other family's action says.

**Why this priority**: § 5.2, and part of decision D1's argument that this had to
be a new family rather than a wider reading of `promotion-fidelity`. The action
text landed with F1; F4 is where the rendered report is asserted to carry it, and
where "no other family's action line changed" becomes a test rather than a claim.

**Independent Test**: render a report carrying this family's findings alongside
other families' findings; assert this family's ranked-plan rows carry the action
verbatim, and that every other family's section and plan row is byte-identical to
a render of the same findings without this family's rendering path involved.

**Acceptance Scenarios**:

1. **Given** any finding from the family's three comparison arms, **When** the
   report renders, **Then** its ranked-plan row carries
   `action="restate the requirement as canon currently states it, or declare the deletion with a `Removed from canon by` marker"`
   verbatim.
2. **Given** a marker-defect finding — the fourth class, which is a defect in a
   DECLARATION rather than a comparison — **When** the report renders, **Then**
   its row carries the marker action ("name a unit the block does not restate,
   or drop the declaration …") and not the arms' action, the two remedies being
   different acts.
3. **Given** a finding set spanning several families, **When** the report
   renders with this feature's rendering path active, **Then** every line
   outside `### modified-block-currency`, the headline counts line, and this
   family's own ranked-plan rows is byte-identical to the render without it.
4. **Given** the subtotal block, **When** the report renders, **Then** no line
   of it appears in `## Ranked Plan` and no severity count in `## Headline`
   moves — it is a rendering of findings, never a finding.

---

### User Story 3 - No workflow option reaches this family (Priority: P1)

The nightly workflow passes exactly one per-family option:
`--promotion-fidelity-basis live-main`, ruled for that family alone. This family
measures the checked-out tree by contract — an active change lives on a branch,
so a family reading `main` would measure a delta `main` does not carry against
canon the branch may have moved. Nothing in the workflow may hand this family a
basis, a scope, or any other per-family switch, and no such switch may exist to
be handed.

**Why this priority**: § 5.3. The boundary is currently true by accident of
nobody having added anything; a pin makes it true on purpose. The packet asks for
a NEW assertion of this family's own rather than a reuse of
`test_workflow_contract.py`'s promotion-fidelity pin, which is written in that
family's shape.

**Independent Test**: read `.github/workflows/doc-health-reusable.yml` and the
checker's own command-line surface; assert the family is named by neither. Prove
non-vacuity by asserting the workflow DOES carry the one per-family option that
exists.

**Acceptance Scenarios**:

1. **Given** the workflow file, **When** every job's every step is read, **Then**
   no `run`, `env`, or `with` value names this family in any spelling
   (`modified-block-currency`, `modified_block_currency`).
2. **Given** the same read, **When** the one existing per-family option is
   looked for, **Then** `--promotion-fidelity-basis live-main` IS found — so the
   absence asserted above is measured against a file that really does carry
   per-family options.
3. **Given** the checker's command-line surface, **When** its options are
   enumerated, **Then** none names this family, while the generic
   `--family` / `--skip-family` options still accept it — a generic option that
   takes every family's id is not a per-family option.
4. **Given** a scratch copy of the workflow with a per-family option for this
   family added, **When** the pin runs against it, **Then** it fails.
5. **Given** this feature's whole diff, **When** `.github/` and `openspec/` are
   diffed against the merge base, **Then** the diff is empty.

---

### User Story 4 - The archive gate has its numbers (Priority: P3)

The packet's § 8.1 archives only on merged-and-green evidence: `pytest
tests/doc-health`, `openspec validate --all --strict`, and a doc-health run whose
movement equals the prediction. F4 is the last feature before that act, so F4 is
where those three numbers are recorded with the commands that produced them.

**Why this priority**: it is evidence, not behaviour — but the archive act cannot
proceed without it, and recording it after the fact is how a figure gets
re-derived differently.

**Independent Test**: the evidence file exists, carries all three gates with
their commands and outputs, and its report-movement figure matches the family's
own measured per-severity counts.

**Acceptance Scenarios**:

1. **Given** F4 complete, **When** `specs/022-modified-block-currency-reporting/evidence/`
   is read, **Then** it records the pytest result with its count, the
   `openspec validate --all --strict` result with its count, and the report
   movement, each with the command that produced it.
2. **Given** the recorded movement, **When** it is compared with the family's own
   per-severity finding counts on the same tree, **Then** they agree.

### Edge Cases

- **Skipped by run configuration** vs **skipped by the family's own scope
  guard**: both are skips, both suppress the subtotal, and the two reasons are
  different text. Canon's skip rule is "cannot run", not "found nothing".
- **A single-family run** (`--family modified-block-currency`): the subtotal
  renders, and the headline's non-default-configuration lines are untouched.
- **Zero findings**: all four classes read 0 and the block still renders.
- **An unclassifiable finding**: counted in a named residual line, never
  silently dropped. The counts sum to the rows or the report says why.
- **Dispositions**: a disposed finding is not reported, so it is not counted —
  the subtotal describes what the report says, not what the family measured
  before suppression.
- **Several repositories in scope** (an aggregation run): ONE subtotal block for
  the family, family-wide, not one per repository — the section it heads is
  family-wide and every row already names its repo.
- **Another family gains a subtotal later**: the mechanism is registry-keyed, so
  a family with no entry renders exactly as it does today.
- **The family's rule texts drift**: the class map is pinned against the arms'
  real output, so drift reds a test instead of silently emptying a class.

## Requirements *(mandatory)*

### Functional Requirements

**The subtotal (§ 5.1)**

- **FR-001**: The report section for `modified-block-currency` MUST carry, under
  its own heading and BEFORE its finding rows, a subtotal block naming each of
  the family's four finding classes with the count of findings in it.
- **FR-002**: Each class MUST be named in the subtotal with its severity band,
  so a reader sees the gate-bearing `warning` class beside the editorial `info`
  classes without reading a row.
- **FR-003**: The subtotal MUST render for a run in which the family produced
  findings AND for a run in which it produced none.
- **FR-004**: The subtotal MUST NOT render for a run in which the family is
  skipped, whether by run configuration or by its own scope guard.
- **FR-005**: Every finding the family emits MUST classify into exactly one of
  its four classes; the class map MUST be pinned against the arms' real output
  so that a rule-text change reds a test rather than emptying a class.
- **FR-006**: A finding the class map does not place MUST be counted in a named
  residual line rendered only when nonzero; the counts MUST always sum to the
  family's findings in the report.
- **FR-007**: The subtotal MUST be produced from the findings the report renders
  for that family, and from nothing else — no second read of the corpus, no
  re-run of the family, no context access.

**The action line (§ 5.2)**

- **FR-008**: Every finding of the family's three comparison arms MUST carry, as
  its suggested action, verbatim: "restate the requirement as canon currently
  states it, or declare the deletion with a `Removed from canon by` marker"; and
  the rendered report's ranked plan MUST carry it for each such finding.
- **FR-009**: The marker-defect class MUST keep its own distinct action, the
  remedy for a defective declaration not being the remedy for an uncarried unit.
  § 5.2 names one action line; the family has two, and this requirement records
  which findings carry which.
- **FR-010**: No other family's action line, section content, or ranked-plan row
  may change. Proven by a rendered-report comparison, not by inspection.

**The mechanism**

- **FR-011**: The subtotal MUST reach the report through an additive,
  registry-keyed mechanism keyed by family id, in the shape of the existing
  per-family notes registry; a family with no entry MUST render byte-identically
  to today.
- **FR-012**: The subtotal MUST NOT be a finding: it MUST NOT appear in
  `## Ranked Plan`, MUST NOT move any `## Headline` severity count, and MUST NOT
  reach the regression diff, the uncited-resolution rule, or the new-findings
  JSON.
- **FR-013**: The finding grammar and the ranked-plan grammar MUST NOT change,
  and the family's rule texts MUST remain byte-identical.

**The workflow boundary (§ 5.3)**

- **FR-014**: `.github/workflows/doc-health-reusable.yml` MUST NOT name this
  family in any step's `run`, `env`, or `with`, in either spelling; asserted by a
  NEW test of this family's own, which reads the workflow file and does not edit
  it.
- **FR-015**: The checker's command-line surface MUST expose no option naming
  this family; the generic `--family` / `--skip-family` options MUST continue to
  accept its id, a generic option taking every family's id not being a per-family
  option.
- **FR-016**: The § 5.3 pin MUST be non-vacuous: it MUST assert that the
  workflow does carry the one per-family option that exists
  (`--promotion-fidelity-basis live-main`), and it MUST fail against a scratch
  copy of the workflow carrying a per-family option for this family.
- **FR-017**: The pin MUST cite F1's and F3's existing structural pins on "the
  family accepts no basis" rather than duplicating them.
- **FR-018**: `git diff` from the merge base over `.github/` and `openspec/`
  MUST be empty.

**Archive readiness (§ 8 precondition, not the archive act)**

- **FR-019**: `python3 -m pytest tests/doc-health -q` green, with its count
  recorded before and after this feature.
- **FR-020**: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green,
  with its count recorded.
- **FR-021**: A doc-health single-repo run whose movement equals the family's own
  per-severity finding counts, recorded with the commands that produced it.
- **FR-022**: The packet's § 8 boxes MUST NOT be ticked and the change MUST NOT
  be archived by this feature.
- **FR-023**: F3's open question on the blast radius of an exact-set corpus gate
  in a required check MUST be carried forward undecided, in this feature's
  hand-off and its PR body.

### Key Entities

- **Finding class**: one of the family's four — scenario-title completeness
  (`warning`, the arm carrying the gate), the carriage ledger (`info`,
  editorial), title resolution and ordering (`warning`), and marker defects
  (`info`, a defect in a declaration rather than a comparison). Three arms, four
  classes; the module's own docstring already says so.
- **The subtotal block**: report lines under the family's heading, before its
  rows, stating each class's count and band. A rendering of findings, never a
  finding.
- **The family-summary registry**: `family id -> (that family's findings) ->
  [note lines]`, a sibling of the existing per-family notes registry, which is
  keyed the same way and rendered in the same position.
- **The action line**: a finding's suggested action, rendered in the ranked plan.
  This family has two — the arms' and the marker class's.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader learns the per-class split of the family's findings from
  ONE block of at most six lines, and the counts in it equal the rows beneath
  them on every run measured.
- **SC-002**: Zero lines outside `### modified-block-currency`, the headline
  counts line, and this family's own ranked-plan rows differ between a report
  rendered with this feature and one rendered without it, over the same findings.
- **SC-003**: Zero changed lines under `.github/` and `openspec/` in this
  feature's diff.
- **SC-004**: Every one of the family's findings, over the F2 fixture corpus and
  over this repository's real tree, classifies into exactly one class; the
  residual count is 0.
- **SC-005**: Three mutations each red exactly the intended test and nothing
  else: dropping the subtotal, changing another family's action line, and adding
  a per-family option for this family to a scratch workflow copy.
- **SC-006**: The three archive-gate numbers are recorded with their commands,
  and the recorded movement agrees with the family's measured counts.
- **SC-007**: `tests/doc-health` is green, and the added tests are visible as a
  count delta against the branch-point baseline. That baseline figure has ONE
  home — `research.md` § "The measurements this feature starts from" — and is
  deliberately not restated here: F3's hand-off records what a figure with four
  homes costs.

## Assumptions

- **The action text already lands.** F1 implemented `_ACTION` with § 5.2's exact
  wording. F4 asserts the rendered report carries it; it does not introduce it.
  Were § 5.2 read as "add the action line", the work would be zero and the
  requirement vacuous, so it is read as "pin it".
- **§ 5.1's "three arms" is read as the family's four finding classes**, because
  the fourth (marker defects) is a class the reader sees rows for and would
  otherwise be uncounted. The module's own docstring already states "THREE ARMS,
  FOUR FINDING CLASSES".
- **§ 5.1's "eleven editorial rows"** is a figure from the packet's § 6.6
  prediction, measured at `9be81a40`. The real tree reads 8 today (F3's plan
  § THE FIGURES re-measured it, and one row was correctly repaired by PR #424).
  F4 asserts no absolute count; the subtotal is measured, and the count
  assertions stay in F3 where they live.
- **`report.render` is the only renderer of a family section.** The lanes that
  fold sections into an already-rendered report (readiness, possibles,
  neutrality) insert their own sections before `## Findings By Family` and do
  not touch a family section.
- **F3's report-movement gate permits this feature's new lines.** Its permitted
  set is `## Headline`, `### modified-block-currency`, `## Ranked Plan`, and the
  subtotal lands inside the second.
- **The subtotal is family-wide**, not per-repository, matching the section it
  heads.
- **No `[NEEDS CLARIFICATION]` remains.** R1's preference order is ruled in this
  feature's brief; the one genuinely open question (F3's blast radius) is ruled
  to be carried forward rather than answered.
