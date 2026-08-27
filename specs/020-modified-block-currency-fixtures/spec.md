# Feature Specification: The modified-block-currency regression-fixture catalogue

**Feature Branch**: `020-modified-block-currency-fixtures`

**Created**: 2026-08-27

**Status**: Draft

**Input**: Speckit F2 of `add-modified-block-currency-check`: the
regression-fixture catalogue for the modified-block-currency family — the #351
true positive reconstructed from history, the #329 one-of-eight flat-count
case, the retitle/merge/removal marker cases, containment-is-not-carriage,
tokenization, re-wrap quiet, SKIPPED-vs-quiet, determinism — as an audit of
F1's existing 97 tests plus RED-first tests for every gap, adding no behaviour
to the module.

## What this feature is, and what it deliberately is not

This is **F2 of four** Speckit features realizing the ratified OpenSpec change
`add-modified-block-currency-check`. Its scope is that packet's
**§ 3 "Speckit F2 — fixtures and tests", items 3.1 through 3.13**, and nothing
else. F1 (`specs/019-modified-block-currency-family/`, PR #420, squashed to
`19e3f6b5`) is on `main`: the family module is registered as the twenty-second
family, with 97 tests and six fixture trees.

**F1's implementation review found that F1 already realizes every scenario of
the ratified delta with a test.** F2 is therefore two things, in this order:

1. **An AUDIT.** Every one of § 3's thirteen numbered items — fourteen rows,
   3.3a included — is mapped to the F1 test or
   tests that already discharge it, by test name, with a verdict of
   `satisfied` or `gapped` and — where gapped — a statement of exactly what is
   missing. An item F1 already covers gets a row in the audit and NO second
   copy of the test. F1's own hand-off note names this trap: "§ 3.11 has
   nothing left to add and should say so rather than write a second copy."
2. **The GAPS, closed RED-first.** Six items are gapped, wholly or in part.
   The two that carry this feature are the HISTORICAL reconstructions — F1
   froze the SHAPES of #351 and #329 in synthesized text; F2 freezes the real
   text, recovered from this repository's git history at recorded commits.

**F2 adds no behaviour to `scripts/doc_health/modified_block_currency.py`.**
If a fixture exposes a real defect in F1's implementation, the fix is a
separate, minimally-scoped task with its own RED test, named as a defect in
the PR body — never folded silently into a fixture commit.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The two real instances that motivated the change can never regress silently (Priority: P1)

The packet exists because of two caught defects. Issue #351:
`add-doxchat-model-intake`'s MODIFIED block, written 2026-08-21 against a
pre-`02a71d6e` canon, was on 2026-08-25 holding the deletion of six body
clauses, two whole scenarios and one reverted scenario line — caught by a
human, repaired by PR #358. Issue #329: `add-release-inventory-drift-check`'s
MODIFIED block restated ONE of `doc-health`'s eight "Deterministic check
families" scenarios while its own ADDED requirement brought seven, so the
file-level scenario count stayed flat at eight and nothing counted the loss —
caught by a byte-for-byte promotion verification run by hand at the archive
gate.

Both texts still exist in this repository's history. This story recovers them
verbatim, freezes them as fixture trees with their commit SHAs recorded, and
asserts what the family says about them. A future refactor of the matching
rule that reintroduces containment, line-level comparison, or per-scenario
bullet pairing fails on the real defect rather than on a proxy for it.

**Why this priority**: F1's fixtures carry the SHAPES; F1's own spec assigns
the byte-faithful reconstructions to F2 (SC-001, SC-002: "F2's § 3.2 owns the
full reconstruction"). These two fixtures are the irreducible content of this
feature — everything else is either already covered or a small extension.

**Independent Test**: Build the two fixture trees from the recorded commits
and run the family over each; assert the named titles and the named units.
Delivers the regression protection on its own, with no other item of § 3
present.

**Acceptance Scenarios**:

1. **Given** the pre-repair `add-doxchat-model-intake` block and the canon of
   2026-08-25, both recovered at `bcfc26a0` (the parent of the repair commit
   `f68261f7`, merged as `87d0b95a` / PR #358), **When** the family runs over
   that tree, **Then** the scenario-title arm emits one `warning` naming
   exactly `The menu offers a routing rule` and
   `A fourth provider verb is proposed`, and naming the promoted spec path it
   read them from.
2. **Given** the same tree, **When** the family runs, **Then** the carriage
   ledger emits one `info` finding for that requirement whose reported units
   carry the text of every clause the repair commit named — the three-member
   port-surface enumeration, "MUST NOT be added as a fourth provider verb",
   the `auto` routing-rule clause, the broker-lane credential clause, and
   `thread file` in the credential-leak list — plus the reverted scenario line
   `**AND** every loaded editor MUST remain usable` and the drifted
   `**WHEN** doxBench runs on the hosted plane` line.
3. **Given** the same tree, **When** the family runs, **Then** canon's bullet
   `**THEN** the selector MUST show exactly the available catalog entries and
   their data-handling badges` is reported as uncarried, even though the
   block's replacement contains it verbatim as a strict prefix — the real
   instance of the widening mechanism, and the single-bullet residue PR #358's
   manual verification found.
4. **Given** the pre-archive `add-release-inventory-drift-check` delta and the
   canon of 2026-08-25, both recovered at `d5f447e8` (the parent of the
   archive commit `38b548d4`, merged as `b03b9992` / PR #331), **When** the
   family runs over that tree, **Then** the scenario-title arm names all SEVEN
   omitted titles: `Lifecycle conformance checks fire`,
   `A register carries staged status`, `Drift checks fire`,
   `Catalog conformance checks fire`, `Routing conformance checks fire`,
   `Origin conformance checks fire`, and
   `Roster composition is checked across domains`.
5. **Given** the same tree, **When** the file-level `#### Scenario:` count is
   taken on both sides, **Then** canon states eight for the requirement and
   the delta FILE carries eight — one restated plus seven brought by the
   change's own ADDED requirement — and the family fires anyway, which is the
   assertion that pins the flat count as not what the family reads.

---

### User Story 2 - A reader can see which of the packet's § 3 items were already discharged and which this feature added (Priority: P1)

Packet § 3 was written before F1 existed. F1 then wrote 97 tests that
discharge most of it, and F1's hand-off says so in prose. Prose is not an
audit: the next reader cannot tell, item by item, whether § 3.7's nine
sub-clauses are covered or whether someone stopped reading at clause four.

This story produces the audit as a committed artefact — one row per § 3 item,
naming the F1 test functions that satisfy it, with a verdict and, where
gapped, the specific missing assertion. It is the artefact that makes "F2 adds
no second copy" checkable rather than claimed.

**Why this priority**: without it, every later reader either re-derives the
mapping (and derives it differently) or writes the duplicate tests F1's
hand-off warns against. It is also the only place the F1 residue this audit
found gets recorded.

**Independent Test**: Read the audit against § 3 and against
`tests/doc-health/test_modified_block_currency.py`; every item has a verdict
and every named test exists and asserts what the row claims.

**Acceptance Scenarios**:

1. **Given** packet § 3 items 3.1 through 3.13 (fourteen rows, counting 3.3a),
   **When** the audit is read, **Then** every item has exactly one row, a
   verdict of `satisfied` or `gapped`, and — for `satisfied` — at least one
   F1 test function name that exists in the F1 test file.
2. **Given** a row whose verdict is `gapped`, **When** it is read, **Then** it
   names the specific assertion § 3 asks for that no F1 test makes, and the
   F2 task that closes it.
3. **Given** § 3.11 and § 3.12, **When** the audit is read, **Then** both are
   `satisfied` and no F2 task duplicates them.

---

### User Story 3 - The marker case § 3 names and F1 did not write is pinned (Priority: P2)

§ 3.3 asks for a specific shape: rename a scenario, declare the rename with a
`Merged into` marker, and drop two of the superseded scenario's four bullets.
The scenario arm must be quiet, because the marker is valid; the ledger must
report the two dropped bullets, because a `Merged into` marker names TITLES
only. A companion case names those two bullets in a `Removed from canon`
marker of their own and the ledger goes quiet.

F1's `Merged into` fixture case is a merge whose source scenario carries ONE
bullet, and that bullet is carried, so the case is quiet in both arms and the
"bullets a merge makes redundant must be declared one at a time" rule is
tested nowhere end to end. F1 covers the adjacent `Removed from canon` +
replacement COMBINATION (§ 3.3a) and the destination exemption; neither
exercises this rule.

**Why this priority**: it is the one marker rule the delta states in its own
paragraph ("A `Merged into` marker names titles only, so a bullet a merge
makes redundant is a declared removal, not a permanent editorial row — but it
has to be declared as a bullet, one at a time") that has no end-to-end pin.

**Independent Test**: One fixture tree with two requirements — the merge-and-gut
and its companion — run through the family.

**Acceptance Scenarios**:

1. **Given** a block whose `Merged into` marker names a four-bullet scenario
   as superseded and whose replacement scenario carries two of those four
   bullets, **When** the family runs, **Then** the scenario-title arm is quiet
   and the ledger reports exactly the two uncarried bullets by their text.
2. **Given** the same block with those two bullets additionally named as code
   spans in a `Removed from canon by <change-id> (<date>):` marker, **When**
   the family runs, **Then** the ledger reports nothing for that requirement
   and no marker-defect finding is emitted.

---

### User Story 4 - The derivation cases are pinned at the granularity the packet phrases them (Priority: P2)

Three items of § 3 are covered by F1 in a narrower form than § 3 asks for, and
the difference is the part that would survive a refactor:

- **§ 3.5 tokenization.** § 3 asks for `.openspec.yaml`,
  `promotion_fidelity.py` AND `contract-v1.45` — a version token whose period
  sits between digits, which is the token shape a naive `\d\.\d` guard would
  let through — plus a body bullet list and a dated bold note spanning
  SEVERAL sentences, with an EDIT TO THE NOTE'S THIRD SENTENCE reporting the
  note ONCE. F1's fixture carries two tokens, a two-sentence note, and the
  note DROPPED rather than edited. Dropped and edited take the same code path
  only if the note is one undivided unit — which is the property under test.
- **§ 3.4 containment.** § 3 asks for a block bullet containing canon's
  bullet "widened at either end". F1's unit test widens at the END only, and
  its end-to-end fixture case is not a strict-containment case at all (canon's
  sentence terminator becomes a comma), so no F1 test exercises containment
  through the family. F1's own SC-003 claims "widened at either end".
- **§ 3.6 re-wrap quiet.** § 3 asks that a scenario-complete block stays
  quiet, "including one that re-wraps every paragraph it carries". F1 asserts
  this at `carried()` — on units it synthesizes in the test body — and its
  `-quiet` fixture tree carries no MODIFIED block at all. A wiring regression
  between `derive_units` and the arms would leave both F1 tests green.

**Why this priority**: each is a small extension of an already-covered rule
rather than a new rule, but each closes the gap between "the helper is right"
and "the family is right".

**Independent Test**: Two fixture trees (tokenization, re-wrap) plus
assertions added to the containment coverage; each runs through
`fam_modified_block_currency`, not through a helper.

**Acceptance Scenarios**:

1. **Given** a requirement body carrying `.openspec.yaml`,
   `promotion_fidelity.py` and `contract-v1.45` in backticked spans, a body
   bullet list, and a dated bold note of at least three sentences, **When**
   the family runs, **Then** no reported unit is a fragment of a backticked
   span, each bullet is reported as its own unit, and the note appears as at
   most one reported row.
2. **Given** the same tree where the block restates that note with its THIRD
   SENTENCE edited, **When** the family runs, **Then** the note is reported
   ONCE and not once per sentence.
3. **Given** a block bullet that contains canon's bullet verbatim with text
   added BEFORE it, and another with text added at both ends, **When** the
   comparison runs, **Then** canon's bullet is reported as uncarried in both
   cases.
4. **Given** a fixture tree whose MODIFIED block restates its promoted
   requirement completely but re-wraps every paragraph, bullet and scenario
   line it carries, **When** the family runs over that tree, **Then** it
   returns no findings and is NOT reported skipped.

---

### User Story 5 - Every fixture in the catalogue says where it came from, and the catalogue is deterministic (Priority: P3)

A fixture that reproduces a real defect is evidence; a fixture that looks like
it reproduces a real defect and was invented is a liability, because the next
reader trusts it. This story requires each new fixture tree to carry its own
provenance note — the commit SHAs the text was recovered from, or an explicit
statement that the text is synthesized and why — and requires determinism to
hold over every tree this family owns, including the new ones.

**Why this priority**: it costs one file per tree and it is what lets a later
session tell a reconstruction from an illustration. F1's determinism test
covers one tree.

**Independent Test**: Each new fixture directory carries a provenance note;
the determinism assertion enumerates every fixture tree.

**Acceptance Scenarios**:

1. **Given** a fixture tree reconstructed from git, **When** its provenance
   note is read, **Then** it names the commit the text was recovered from, the
   repair or archive commit, the merge commit, the issue number, and the exact
   `git show` invocations that reproduce each file.
2. **Given** a fixture tree whose text is synthesized, **When** its provenance
   note is read, **Then** it says so explicitly and says what rule it
   illustrates.
3. **Given** every fixture tree this family owns, **When** the family runs
   twice over each, **Then** the two finding lists are byte-identical
   including ordering.

### Edge Cases

- **A recovered file is not self-contained.** `openspec/specs/ideation-dashboard/spec.md`
  is 279 KB and carries dozens of unrelated requirements. The fixture freezes
  the REQUIREMENT under test verbatim inside a minimal spec file rather than
  the whole document, because the family reads per requirement and a whole-file
  copy would freeze canon nobody is testing. The verbatim guarantee is scoped
  to the requirement, and the provenance note says so.
- **The human's clause count is not the family's unit count.** The repair
  commit for #351 names SIX body clauses; the normative derivation splits the
  body into SENTENCES, and those six clauses lie inside THREE sentence units.
  Assertions therefore name the clause TEXT found inside the reported units,
  never a row count — which is what orchestrator decision 3 requires anyway.
- **The rendered finding truncates each unit.** The ledger quotes each unit to
  a fixed width, so a clause late in a long sentence is not present in the
  rendered rule string. Assertions on full clause text run against the
  uncarried UNIT texts; assertions on the rendered finding run against the
  quoted prefixes. A test that asserted a late clause against the rendered
  rule would fail for a reason that has nothing to do with the rule.
- **A fixture provenance note is not a governed document.** It lives under
  `tests/`, which the corpus reader excludes by name and which no
  `GOVERNED_ROOTS` entry covers, so it carries no `Status:` header and draws no
  lifecycle finding.
- **A fixture could exercise a defect rather than a rule.** If a § 3 fixture
  reports something the delta says it should not, that is a defect in F1's
  implementation and not a fixture to be adjusted until it agrees. It becomes
  its own task with its own RED test and its own line in the PR body.
- **A `Merged into` companion could be quiet for the wrong reason.** The
  companion case must be shown to go quiet BECAUSE of the marker, not because
  the bullets were carried — asserted by removing the marker in the same test
  and observing the report return.

## Requirements *(mandatory)*

### Functional Requirements

Each requirement is a reading of packet § 3, of the ratified `doc-health`
delta, or of an orchestrator decision. The § 3 item is named in every case.

**The audit**

- **FR-001**: The feature MUST produce a committed coverage audit mapping each
  packet § 3 item — 3.1, 3.2, 3.3, 3.3a, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10,
  3.11, 3.12, 3.13 — to the F1 test functions that discharge it, with a
  verdict of `satisfied` or `gapped` and, for every `gapped` row, the specific
  assertion § 3 asks for that no F1 test makes and the F2 task that closes it.
- **FR-002**: An item the audit marks `satisfied` MUST NOT gain a duplicate F2
  test. Where § 3 names an item F1 fully covers, the audit row IS the
  deliverable.
- **FR-003**: Every F1 test function named in the audit MUST exist in
  `tests/doc-health/test_modified_block_currency.py`, and the audit MUST be
  checked against the file rather than against F1's plan.

**Fixture A — the #351 true positive, reconstructed (§ 3.1)**

- **FR-004**: A fixture tree MUST carry `add-doxchat-model-intake`'s MODIFIED
  block for `doxBench model catalog and provider boundary` as it stood before
  the repair, and the promoted `ideation-dashboard` requirement as canon
  stated it on 2026-08-25, both recovered from git at recorded commits.
- **FR-005**: The scenario-title arm MUST emit one `warning` on that tree
  naming exactly `The menu offers a routing rule` and
  `A fourth provider verb is proposed`, and naming the promoted spec path.
- **FR-006**: The carriage ledger MUST emit one `info` finding for that
  requirement, and the test MUST assert that the reported units carry the text
  of each clause the repair commit named, the reverted scenario line
  `**AND** every loaded editor MUST remain usable`, and the hosted-plane
  scenario line the block drifted.
- **FR-007**: A test MUST assert that canon's bullet
  `**THEN** the selector MUST show exactly the available catalog entries and
  their data-handling badges` is reported as uncarried on this tree, and MUST
  state in its docstring that the block's replacement contains it verbatim as
  a strict prefix — the REAL instance of § 3.4's mechanism.
- **FR-008**: Every assertion on this tree MUST be on rule text and named
  units and MUST NOT be on a finding count, a unit count, or a scenario count
  (orchestrator decision 3).

**Fixture B — the #329 one-of-eight case, reconstructed (§ 3.2)**

- **FR-009**: A fixture tree MUST carry `add-release-inventory-drift-check`'s
  MODIFIED block for `Deterministic check families` as it stood before its
  archive — restating ONE of canon's eight scenarios — together with its own
  ADDED requirement bringing SEVEN, and the promoted `doc-health` requirement
  as canon then stated it, both recovered from git at recorded commits.
- **FR-010**: The scenario-title arm MUST emit one `warning` on that tree
  naming all SEVEN omitted titles, asserted title by title.
- **FR-011**: A second assertion MUST pin that the flat file-level count is
  not what the family reads: canon states eight scenarios for the requirement,
  the delta FILE carries eight, and the family fires regardless.

**The gapped marker case (§ 3.3)**

- **FR-012**: A fixture MUST carry a block whose `Merged into` marker names a
  four-bullet scenario as superseded and whose replacement scenario carries
  two of those four bullets. The scenario-title arm MUST be quiet and the
  ledger MUST report exactly the two uncarried bullets by text.
- **FR-013**: A companion fixture requirement MUST name those two bullets as
  code spans in a `Removed from canon by <change-id> (<YYYY-MM-DD>):` marker,
  and the ledger MUST report nothing for it and emit no marker defect. The
  test MUST show the silence is caused by the marker.

**The derivation gaps (§ 3.4, § 3.5, § 3.6, § 3.7)**

- **FR-014**: Containment MUST be pinned for a block unit widened BEFORE
  canon's unit and for one widened at BOTH ends, not only after it (§ 3.4,
  and F1's own SC-003 wording).
- **FR-015**: A tokenization fixture MUST carry backticked tokens with
  internal periods including `.openspec.yaml`, `promotion_fidelity.py` and
  `contract-v1.45`, a body bullet list, and a dated bold note spanning at
  least three sentences (§ 3.5).
- **FR-016**: On that fixture, run through the family: no reported unit may be
  a fragment of a backticked span; each body bullet MUST be reported as its
  own unit; and the note MUST be reported as at most one row.
- **FR-017**: On that fixture the block MUST restate the note with its THIRD
  SENTENCE edited, and the note MUST be reported ONCE rather than once per
  sentence (§ 3.5's last clause, which the dropped-note case does not reach).
- **FR-018**: A fixture tree MUST carry a MODIFIED block that restates its
  promoted requirement completely while re-wrapping every paragraph, bullet
  and scenario line, and the family MUST return no findings over that tree and
  MUST NOT report itself skipped (§ 3.6, end to end).
- **FR-019**: A marker naming a unit that itself contains backticks — a clause
  citing `openxFactory` — fenced with a longer run, MUST be pinned END TO END
  through the family, suppressing the whole unit rather than a fragment
  (§ 3.7's longer-fence clause, which F1 pins only at `extract_code_spans`).

**Determinism and provenance (§ 3.13, orchestrator decision 2)**

- **FR-020**: Determinism MUST be asserted over EVERY fixture tree this family
  owns, including each tree this feature adds: two runs produce byte-identical
  findings including ordering (§ 3.13).
- **FR-021**: Each fixture tree this feature adds MUST carry a provenance note
  naming, for a reconstruction, the commit the text was recovered from, the
  repair or archive commit, the merge commit, the issue number, and the exact
  `git show` invocations that reproduce each file; and, for a synthesis, an
  explicit statement that the text is synthesized and what rule it
  illustrates.

**No behaviour, and the scope guard**

- **FR-022**: This feature MUST NOT change the behaviour of
  `scripts/doc_health/modified_block_currency.py`, of any other family, or of
  `families.py`, `__init__.py`, `report.py`, `runner.py`, the thresholds, or
  `.github/workflows/`.
- **FR-023**: Where a § 3 fixture exposes a real defect in F1's
  implementation, the fix MUST be a separate task with its own RED test,
  minimal in scope, and MUST be named as a defect in the PR body — never
  folded into a fixture task (orchestrator decision 1).
- **FR-024**: This feature MUST NOT edit the packet's delta text, its § 2.1
  MODIFIED block, any promoted spec, or any other change's delta
  (orchestrator decision 4). A scope-guard test MUST pin the boundary, in the
  shape F1's T059 established.
- **FR-025**: Every test this feature adds MUST be shown to have failed before
  the fixture or assertion it covers existed — RED first, recorded per task.
- **FR-026**: Suite evidence MUST be `python3 -m pytest tests/doc-health -q`
  from this worktree, never a whole-tree `pytest tests` run, which requires a
  live Postgres this worktree does not have. The baseline is **1077 passed**,
  measured at this branch point (orchestrator decision 5).
- **FR-027**: A mutation round MUST be run over the assertions this feature
  adds — each new assertion inverted or weakened in turn — and every surviving
  mutant MUST be either killed by a new assertion or recorded with the reason
  it is accepted.
- **FR-028**: An adversarial review pass MUST run over the fixtures and the
  audit, with its findings and dispositions recorded in `plan.md`.

### Key Entities

- **Fixture tree**: a directory under `tests/doc-health/fixtures/` named
  `modified-block-currency-<case>` containing one or more miniature repository
  directories, each with `openspec/specs/<capability>/spec.md` and
  `openspec/changes/<change-id>/{proposal.md,specs/<capability>/spec.md}`. The
  directory name is the argument `make_ctx` takes.
- **Provenance note**: a `README.md` beside a fixture tree's repository
  directories recording where its text came from. New to this suite — no
  fixture carries one today; `test_promotion_fidelity.py` records provenance
  in its module docstring instead, and F2 keeps that habit as well as adding
  the note.
- **Coverage audit**: `contracts/coverage-audit.md` — one row per packet § 3
  item, with F1 test names, verdict, and gap description.
- **Reported unit**: a `(kind, text)` pair the family names in a finding —
  `body`, `scenario-title` or `scenario-bullet`. Assertions name these, not
  their number.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The #351 instance, in its real text recovered at a recorded
  commit, is reported by the family: two scenario titles named on the
  scenario arm, and the repair commit's named clauses, the reverted scenario
  line and the widened bullet all present among the ledger's reported units.
- **SC-002**: The #329 instance, in its real text recovered at a recorded
  commit, is reported with all seven omitted titles named, and the flat
  file-level count of eight on both sides is shown not to buy silence.
- **SC-003**: The `Merged into` retitle-and-gut reports exactly the two
  uncarried bullets of four, and the companion case that declares them goes
  quiet — with the silence shown to be caused by the marker.
- **SC-004**: Canon's unit, widened BEFORE it and at BOTH ends, is reported as
  uncarried.
- **SC-005**: A dated bold note of three or more sentences, restated with its
  third sentence edited, is reported once.
- **SC-006**: A scenario-complete block that re-wraps every line it carries
  produces no findings when run through the family over a fixture tree, and is
  not reported skipped.
- **SC-007**: Every one of packet § 3's fourteen items carries an audit row
  with a verdict; zero items are unaccounted for; and every F1 test name the
  audit cites exists.
- **SC-008**: `python3 -m pytest tests/doc-health -q` is green, and the count
  rises from **1077** by exactly the number of tests this feature adds.
- **SC-009**: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` is
  green, with its count recorded before and after and unchanged.
- **SC-010**: `git diff --stat origin/main` shows no change under `scripts/`
  unless a defect task under FR-023 exists and names it; and no change to any
  `openspec/` path.
- **SC-011**: Two runs over every fixture tree this family owns produce
  byte-identical findings including ordering.
- **SC-012**: The mutation round over the added assertions leaves no surviving
  mutant unrecorded.

## Assumptions

Each is a reading of the packet, of the ratified delta, or of measured
evidence, with what settles it.

- **A1 — § 3.1's "six body clauses" are six human-named clauses inside THREE
  normative body units.** The delta's derivation splits a body paragraph into
  SENTENCES (`specs/doc-health/spec.md`, "every other paragraph SHALL be split
  into sentences"), and the six clauses the repair commit enumerates lie
  inside three of canon's sentences. MEASURED on the reconstruction: the
  ledger reports 3 body units, 8 scenario bullets and — on the title arm — 2
  scenario titles. Assertions therefore name the clause TEXT inside the
  reported units. Orchestrator decision 3 requires exactly this.
- **A2 — full-clause assertions run against the uncarried unit texts, not the
  rendered rule string.** The ledger quotes each unit to a fixed width, so a
  clause late in a long sentence is absent from the rendered finding.
  Assertions split accordingly: the rendered finding is asserted on its quoted
  prefixes and on the arm's own wording; full clause text is asserted on the
  units the comparison returns.
- **A3 — a reconstructed fixture freezes the REQUIREMENT verbatim, not the
  whole source file.** Canon for #351 is a 279 KB document of unrelated
  requirements; the family reads per requirement. The requirement is copied
  byte-for-byte into a minimal spec file with a synthetic `# … Specification`
  header and `## Requirements` heading, and the provenance note records that
  the verbatim guarantee is scoped to the requirement.
- **A4 — the two histories are recoverable, and were recovered.** VERIFIED
  before this spec was written. #351: the pre-repair block and the canon of
  2026-08-25 both read at `bcfc26a0d2f182c652ed9054b82210ccbee8124a`, the
  parent of the repair commit `f68261f775eb74455a16f7d4d67b576fd76618f0`
  (merged as `87d0b95ae2970733f273cbac15beb847a5b562c5`, PR #358). #329: the
  pre-archive delta and canon both read at
  `d5f447e89cf619fd12113bcf03525468ece4470d`, the parent of the archive commit
  `38b548d46153e5e39c855aa105aa77cbb550894a` (merged as
  `b03b9992d519dbfab78fa63a00c5c6e2413ae0e0`, PR #331). Nothing in § 3 needs
  to be synthesized, so orchestrator decision 2's synthesis branch does not
  fire for 3.1 or 3.2.
- **A5 — F1's hand-off note governs where it and F1's spec disagree.** F1's
  `spec.md` § Out of Scope assigns to F2 "the full marker matrix, the
  determinism pin and the structural launch pins"; F1's `tasks.md` hand-off,
  written after the implementation review, says F1 already carries all three
  and that F2 should say so rather than write a second copy. The hand-off is
  the later statement and is the one consistent with orchestrator decision 4
  (minimal scope). The audit records the disagreement in the affected rows.
- **A6 — § 3.11 and § 3.12 are fully satisfied by F1.** § 3.11 by
  `test_the_three_launch_severities_are_named_apart` and
  `test_the_family_is_absent_from_family_resolution_at_launch`; § 3.12 by
  `test_a_scope_with_no_changes_directory_skips_with_its_reason` and
  `test_a_scope_with_active_changes_but_no_modified_block_is_not_skipped`,
  which match § 3.12's phrasing clause for clause.
- **A7 — a fixture provenance note draws no lifecycle finding.**
  `corpus.EXCLUDED_PARTS` contains `tests` and `GOVERNED_ROOTS` does not, so
  a `README.md` under `tests/doc-health/fixtures/` is outside the governed
  corpus and outside the lifecycle scan set and needs no `Status:` header.
- **A8 — new fixture trees are separate directories, not additions to F1's.**
  `make_ctx` takes the fixture directory name and loads every repository
  directory under it, so adding a repository to an existing tree changes what
  every existing test over that tree sees. Each new case gets its own tree.
- **A9 — the two-writers, resolution, disposition and skip families of cases
  are closed by F1** (§ 3.8, § 3.9, § 3.10, § 3.12), each with named tests in
  the audit. F2 adds nothing to them beyond the determinism sweep.

## Dependencies

- **F1, on `main`**: `scripts/doc_health/modified_block_currency.py`, its 97
  tests, and its six fixture trees — consumed, never modified. Base commit
  `19e3f6b5`.
- The ratified packet `openspec/changes/add-modified-block-currency-check`
  (§ 3 is this feature's scope; § 6 is its evidence) and the two spec deltas —
  binding inputs, read-only.
- This repository's own git history, for the two reconstructions. If a future
  history rewrite loses `bcfc26a0` or `d5f447e8`, the fixtures remain but
  their provenance notes become unverifiable, which is the risk the notes
  exist to make visible.
- `tests/doc-health/conftest.py` — `make_ctx`, `FakeGit`, `FIXTURES`.
- `tests/doc-health/test_promotion_fidelity.py` — the precedent for a
  historical reconstruction declared as one.

## Out of Scope

- Any behaviour change to the family, to any other family, or to the report,
  runner, thresholds or workflows (FR-022) — except a defect fix admitted
  under FR-023, which is named as a defect and carries its own RED test.
- The self-gate against this repository (packet § 4) — F3. This feature
  asserts nothing about the live corpus figures, and does not restate F1's
  `plan.md` § Predicted movement.
- Report rendering, the action line, and the workflow-boundary test (packet
  § 5) — F4.
- Any severity flip or `FAMILY_RESOLUTION` change (packet § 7.2).
- #330's shape 1, the post-archive safety net (packet § 7.1). This feature
  does not close #330.
- The archive act (packet § 8) and the § 2.1 sequencing gate, both discharged
  or owned elsewhere.
- Re-testing anything the audit marks `satisfied` (FR-002).
