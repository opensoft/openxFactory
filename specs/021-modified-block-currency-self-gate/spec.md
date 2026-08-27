# Feature Specification: The modified-block-currency self-gate

**Feature Branch**: `021-modified-block-currency-self-gate`

**Created**: 2026-08-27

**Status**: Draft

**Input**: Speckit F3 of `add-modified-block-currency-check` — packet
`openspec/changes/add-modified-block-currency-check/tasks.md` § 4 (4.1–4.5).
F1 (`019-modified-block-currency-family`, `19e3f6b5`) built the family and
registered it; F2 (`020-modified-block-currency-fixtures`, `76a2ad27`) built the
regression catalogue. Both are on `main`. F4 owns reporting and the workflow
boundary and is not started.

## Why this feature exists

`add-modified-block-currency-check` polices a defect class: an active
`## MODIFIED Requirements` block that silently drops obligations canon still
states. The family that detects it now exists and is registered. **Nothing yet
asserts what it says about the repository that ships it.**

**Fixtures prove the rules. Nothing proved the verdict.** F1's tests are
behavioural over fixture trees; F2's are historical reconstructions over fixture
trees. Both are the right shape for what they assert, and neither says a word
about what the family reports over the corpus the steward actually reads.

The distinction is not academic, and the first draft of this paragraph
overstated it — worth recording, because the overstatement is the kind this
feature exists to catch. It claimed that "if `active_blocks` returned an empty
list, every fixture test would still pass". That is FALSE: the fixture trees
carry `openspec/changes/`, an `archive/` directory and a `proposal.md` each, so
they route through the same discovery and a total break reds them.

What fixture tests genuinely cannot reach is narrower and worse:

- **The verdict.** Whether this repository's twenty-two MODIFIED blocks are
  currently lossy, and which ones, is a fact about this corpus. No fixture
  asserts it, so nobody could read the report and know whether its rows were the
  expected rows.
- **Real prose.** Fixture units are short synthetic sentences. A normalization or
  masking change that made real canon's long, backticked, wrapped units match
  loosely would leave every fixture green and quietly empty the ledger.
- **Any future guard that empties a real-tree read without touching a fixture
  shape** — a repository-name condition, a scale cutoff, a `.git`-presence
  assumption, a path depth that happens to hold for a fixture root and not for
  this one.
- **The rendered report.** Fixtures never render one, so nothing bounded what
  registering a twenty-second family did to the other twenty-one sections.

This feature is the measurement that cannot be satisfied vacuously: the family
runs over **this checkout**, through the family's own entry point, and its
findings are asserted **by named subject** — which change, which requirement,
which unit — rather than by count. It also asserts that the family reads its
own packet, which is the one block in the tree whose content this change
controls.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The corpus verdict is a named claim, not a number (Priority: P1)

A doc-health steward reads the nightly report and sees the
`modified-block-currency` section carrying one `warning` and nine `info` rows.
They need to know that those rows are the rows the repository's own tests expect
— that the section is not empty because discovery broke, and not populated by
some accident of a refactor. Every row the family draws over this checkout is
named in a test: the change, the capability, the requirement title, and for the
gate-bearing `warning`, the omitted scenario title itself.

**Why this priority**: this is the acceptance measurement the packet's § 4.1
asks for, and the anti-vacuity rule it states in the same breath. Without it the
family ships unmeasured against the only corpus anybody has run it on.

**Independent Test**: run the family over this checkout through
`fam_modified_block_currency` and assert the full named-subject set. Delete any
one name from the expected set and the test fails naming it.

**Acceptance Scenarios**:

1. **Given** this checkout, **When** the family runs over it through its own
   entry point, **Then** it returns a finding list (never a `Skip`) and the
   `warning` band holds exactly one finding, which names
   `add-composed-view-authoring` and quotes the omitted scenario title
   `Gate verbs hide on a composed view`.
2. **Given** the same run, **When** the `info` band is enumerated, **Then** each
   finding's `(change, capability, requirement title)` triple is one of a named
   set written out in the test, and the set matches exactly — an extra finding
   fails naming it, a missing finding fails naming it.
3. **Given** the same run, **When** the resolution, ordering and marker-defect
   classes are counted, **Then** each is empty, asserted by the rule text that
   identifies the class rather than by a total.

---

### User Story 2 - The gate cannot pass on an empty read (Priority: P1)

A future refactor breaks `active_blocks` — a glob typo, a path assumption, a
premature `continue`. Every fixture test still passes because fixtures reach the
parser directly. The self-gate must fail, and it must fail saying that discovery
found nothing rather than that a count moved.

**Why this priority**: it is the whole reason § 4.1 forbids a bare count. A
count assertion over a broken read fails with `0 != 10`, which reads as a corpus
change. A floor plus named subjects fails with "discovery examined 0 MODIFIED
blocks over <root>".

**Independent Test**: the floor is separately assertable — the population of
MODIFIED blocks the family discovers over this checkout is non-empty and is the
same population the entry point consumes.

**Acceptance Scenarios**:

1. **Given** this checkout, **When** the block population is enumerated,
   **Then** it is non-empty, and the failure message on an empty read names the
   resolved root and the glob that found nothing.
2. **Given** a run whose named-subject assertion is removed, **When** discovery
   returns nothing, **Then** the remaining floor assertion still fails — the two
   guards are independent, not one guard written twice. *This scenario is
   discharged by the MUTATION ROUND rather than by a test, because a test that
   deleted its own sibling's assertion would be a test of the test file.*

---

### User Story 3 - The family reads its own packet, against canon (Priority: P1)

`add-modified-block-currency-check` carries its own
`## MODIFIED Requirements` block on "Deterministic check families" (packet
§ 2.1). That block is the one document in the tree this change authored, and the
family draws exactly one `info` finding against it — the two stale numeral
sentences the block does not carry. That finding is **evidence, not a
regression**: it is how a reader knows the family reads the packet that
introduced it.

**Why this priority**: § 4.2 exists so § 4.1 cannot pass because discovery
quietly stopped at the packet's own delta. It also settles which document the
block is measured against, and the packet's own answer to that is now stale.

**Independent Test**: assert the own-delta path is among the discovered blocks,
assert its resolved basis is canon (`openspec/specs/doc-health/spec.md`), and
assert the self-finding quotes both stale numeral sentences.

**Acceptance Scenarios**:

1. **Given** this checkout, **When** the discovered blocks are enumerated,
   **Then**
   `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`
   is among them, carrying the title "Deterministic check families".
2. **Given** that block, **When** its measurement basis is resolved, **Then**
   the basis is the promoted `doc-health` spec and the resolution status is
   canon — not an active sibling's addition and not a two-writers override.
3. **Given** the packet's § 4.2 claim that the block is measured against
   `add-family-enumeration-check`'s outcome, **When** that change is looked for
   among active changes, **Then** it is absent (archived at `f027d3b3`), so no
   sibling basis exists to measure against and the packet's claim is history.
4. **Given** the self-finding, **When** its quoted units are read, **Then** they
   are the two body sentences carrying `twenty-one check families` and
   `Four of the twenty-one`, and the finding is neither suppressed nor
   dispositioned.

---

### User Story 4 - The report moves in this family's lines and nowhere else (Priority: P2)

The steward needs to know that registering a twenty-second family changed the
report only where that family renders. If the `error` or `critical` bands moved,
a run configured `--fail-on error` would newly fail for reasons unrelated to
this change. If the per-stage counts or the catalog sections moved, some shared
reader was disturbed.

**Why this priority**: it bounds the blast radius of F1's landing, and it is the
one place a count assertion earns its keep — stated as a **difference between
two runs of this tree**, never as a hard-coded total.

**Independent Test**: run the single-repo report twice over this checkout, once
with the family and once with `--skip-family modified-block-currency`, and
compare.

**Acceptance Scenarios**:

1. **Given** the two runs, **When** their headline bands are compared, **Then**
   `critical` and `error` are identical and `warning` and `info` differ by
   exactly the family's own warning count and info count.
2. **Given** the two runs, **When** every differing line is classified, **Then**
   each falls in one of four places: the headline line, the skipped-family
   notice, this family's own report section, or the ranked-plan rows for this
   family's own findings.
3. **Given** the two runs, **When** the per-stage counts, the preflight section
   and every other family's section are compared, **Then** they are
   byte-identical.

---

### User Story 5 - The gate says what to do when the corpus moves (Priority: P2)

`add-composed-view-authoring` will eventually declare its rename with a
`Removed from canon by` marker, or archive. On that day the named `warning`
disappears and this feature's test fails. The engineer who sees that failure
must be told it is expected corpus movement and what to do, not left to
reverse-engineer whether the family broke.

**Why this priority**: a self-gate against a live corpus is a maintenance
obligation. A failure message that does not name the obligation converts the
gate into an obstacle and gets it deleted.

**Independent Test**: read the failure messages. Each names the measured tree,
the subject that moved, and the two legitimate responses (re-measure and update
the named set; or, if the family reads zero, assert zero by the same mechanism
because that is the desired end state).

**Acceptance Scenarios**:

1. **Given** a named subject that no longer appears, **When** the assertion
   fails, **Then** the message names the subject, states that corpus movement is
   the expected cause, and says to re-measure and update the named set.
2. **Given** a corpus where the family reads zero findings, **When** the gate is
   updated, **Then** the desired end state is zero asserted by the same
   named-subject mechanism, with the floor assertion still proving discovery ran.

---

### Edge Cases

- **The family returns `Skip`.** A checkout with no `openspec/changes/`
  directory skips by contract. This checkout has one, so a `Skip` here is a
  defect and is asserted apart from an empty finding list — they are different
  states and the family's own delta says so.
- **The resolved root is not this checkout.** A resolver that walks up the
  directory tree lands on the aggregation checkout or another session's
  worktree, and the verdict then describes a tree nobody asked about. The gate
  resolves the repository under test and fails with a named reason rather than
  walking up.
- **A disposition hides the self-finding.** `health/dispositions.yaml` lives at
  the aggregation root and a single-repo run has none, so no disposition can
  apply in this scope. Asserted, so the silence is understood rather than
  discovered — and so a future entry naming the packet's own delta is visibly a
  change of behaviour.
- **The corpus is measured through a different code path than the report.** A
  gate that reimplements discovery proves something about the gate. Every
  assertion routes through the family's own public functions.
- **Two report runs disagree for a reason other than the family.** Wall-clock
  enters the report only through `--as-of`; both runs take the default on the
  same day. A cross-day run is the one condition under which the diff comparison
  is not meaningful, and the diff itself surfaces it as movement in another
  section.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The self-gate MUST run the family over this repository through
  `fam_modified_block_currency`, not through any reimplementation of its
  discovery, parsing or comparison — and MUST assert that structurally rather
  than by authoring discipline: the gate module's own source carries no
  requirement or markdown parser of its own and reaches the corpus only through
  the family's public functions.
- **FR-002**: The self-gate MUST resolve the repository under test as the
  checkout containing the test file itself, MUST confirm it by the markers a
  measurable openxFactory checkout carries (`openspec/changes/` and
  `openspec/specs/doc-health/spec.md`), and MUST fail with a reason naming what
  was searched rather than walking up to an ancestor.
- **FR-003**: The self-gate MUST NOT resolve to the aggregation checkout or to
  any other worktree, and MUST assert that the resolved root is the same tree
  the test file lives in.
- **FR-004**: The self-gate MUST assert that the family returns a finding list
  and not a `Skip`, and MUST assert those two states apart.
- **FR-005**: The self-gate MUST carry a discovery floor independent of any
  finding assertion: the population of MODIFIED blocks the family discovers over
  this checkout is non-empty, so no assertion in this feature can pass on an
  empty read.
- **FR-006**: The self-gate MUST assert the scenario-title arm's finding by its
  NAMED SUBJECT — the change `add-composed-view-authoring`, the requirement
  title `Composed views are read-only with a repository jump`, and the omitted
  scenario title `Gate verbs hide on a composed view` — and MUST assert that the
  `warning` band holds exactly that one finding.
- **FR-007**: The self-gate MUST assert every carriage-ledger finding by its
  named subject as a `(change, capability, requirement title)` triple, compared
  as an exact set so both an extra and a missing finding fail by name.
- **FR-008**: The self-gate MUST assert that the resolution class (a block
  resolving to no promoted requirement), the ordering class (an undecided
  two-writers group) and the marker-defect class are each empty over this
  checkout, identified by the rule text that distinguishes the class rather than
  by a total.
- **FR-009**: The self-gate MUST assert that this change's own doc-health delta
  is among the blocks the family examined, by its path and its requirement
  title.
- **FR-010**: The self-gate MUST assert that the own delta's measurement basis
  is the promoted `doc-health` spec — canon — and that the resolution status is
  the canon status rather than a pending-on-sibling status or a two-writers
  override.
- **FR-011**: The self-gate MUST assert that `add-family-enumeration-check` is
  not among this tree's active changes, which is why no sibling basis exists and
  why the packet's § 4.2 wording is history rather than a live claim.
- **FR-012**: The self-gate MUST assert that the self-drawn ledger finding
  quotes the two stale numeral sentences (`twenty-one check families` and
  `Four of the twenty-one`) and MUST record that this finding is expected
  evidence rather than a regression.
- **FR-013**: The self-gate MUST assert that no disposition applies in
  single-repo scope, so the self-finding cannot be silently suppressed.
- **FR-014**: The self-gate MUST pin the report movement as a DIFFERENCE between
  two runs of this checkout — one with the family, one with
  `--skip-family modified-block-currency` — and MUST NOT assert a hard-coded
  report total.
- **FR-015**: The movement pin MUST assert that `critical` and `error` do not
  move, that `warning` and `info` move by exactly the family's own per-severity
  finding counts, and that every other differing line falls in the headline, the
  skipped-family notice, this family's section, or this family's ranked-plan
  rows.
- **FR-016**: Every assertion whose subject is live corpus content MUST fail
  with a message that names the subject, states that corpus movement is the
  expected cause, and names the two legitimate responses (re-measure and update
  the named set; or assert zero by the same mechanism once the family reads
  zero).
- **FR-017**: The self-gate MUST record its numbers as evidence with the exact
  commands that produced them: the `tests/doc-health` suite count before and
  after, the `openspec validate --all --strict` count, and the two-run report
  diff.
- **FR-018**: The self-gate MUST pin the family's run-context surface at both
  levels at which it exists, so a lightweight context in the test is provably
  faithful to the one the report builds: the family's own module reads exactly
  ONE context attribute (the repository paths), and it hands the context to
  exactly ONE collaborator (the disposition reader), which reads exactly one
  more (the aggregation root). A newly read attribute at either level MUST red
  the pin.
- **FR-019**: This feature MUST add no production-code change. The diff against
  the merge base over `scripts/`, `openspec/` and `.github/` MUST be empty; a
  defect found in the module is recorded as its own named task, not fixed here.
- **FR-020**: Every test this feature adds MUST have been shown failing before
  it passed, and the RED evidence MUST be recorded — for a corpus assertion, by
  asserting a wrong named subject; for the movement pin, by running it with the
  family skipped.

### Key Entities

- **Repository under test**: the checkout the gate measures. Resolved from the
  test file's own location, confirmed by markers, never inherited from an
  ancestor walk.
- **Named subject**: the identity of a finding as a reader states it — change
  id, capability, requirement title, and for the scenario arm the omitted
  scenario title. The unit of assertion in this feature.
- **Discovery floor**: the non-empty population of active MODIFIED blocks,
  asserted independently of any finding, so no other assertion can pass
  vacuously.
- **Movement pin**: the per-severity difference between two report runs of this
  checkout differing only by `--skip-family`. The one place a count is asserted.
- **Self-finding**: the single carriage-ledger `info` the family draws against
  this change's own § 2.1 block. Expected evidence; never dispositioned.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader of the failing gate learns, without opening the module,
  which named subject moved and what to do about it.
- **SC-002**: Breaking the family's discovery over a real tree fails the gate,
  and the failure names an empty read rather than a moved count.
- **SC-003**: Removing the named-subject assertion leaves the discovery floor
  still failing on a vacuous read — the two guards are independent.
- **SC-004**: Pointing the resolver at any checkout other than the one holding
  the test file fails the gate.
- **SC-005**: Running the movement pin against a tree with the family skipped
  fails it.
- **SC-006**: The `tests/doc-health` suite is green before and after, and the
  added tests appear as a count delta against the recorded baseline.
- **SC-007**: `openspec validate --all --strict` is green with its count
  recorded at the measured revision.
- **SC-008**: The two-run report diff touches only the four line classes
  FR-015 names; every other section is byte-identical.
- **SC-009**: The diff over `scripts/`, `openspec/` and `.github/` against the
  merge base is empty.

## Assumptions

- The corpus figures in this spec are the ones measured at `76a2ad27` with the
  family registered and § 2.1's block present: one `warning`, nine `info`, zero
  `error`, zero `critical`, over twenty-two active MODIFIED blocks. The packet's
  § 4.1 figure (eleven carriage-ledger findings) and § 4.2 basis
  (`add-family-enumeration-check`'s outcome) are STALE and are treated as
  history — see `plan.md` for the reconciliation and the orchestrator decisions
  it rests on.
- `tests/doc-health` is the suite of record. The whole-tree `pytest tests` run
  drives live Postgres and is never run from a worktree (F1's ruling N12).
- The report gate runs single-repo (`--single-repo .`), which is the mode a PR
  self-gate uses and the mode in which no aggregation disposition applies.
- Both report runs are taken on the same day, so `--as-of` defaults agree.
- F1's own-packet hook (task T057,
  `test_the_family_reads_its_own_packet_s_delta`) is recorded `[x]` in F1's
  `tasks.md` but **does not exist** anywhere under `tests/`. This feature writes
  the assertion rather than reusing it, and records the discrepancy as F1
  residue. Nothing is duplicated.

## Out of Scope

- Any change to `scripts/doc_health/`. FR-019 pins the empty diff.
- The report section rendering, the action-line wording and the workflow
  boundary pin — packet § 5, owned by F4.
- The advisory-to-enforcing flip of the scenario-title arm — packet § 7.2, a
  later ruling.
- The eighteen-repository aggregation pass — packet § 7.4, unmeasured by design
  and F4's first instruction.
- Dispositioning any finding this gate asserts, the self-finding above all.
- Issue #330's post-archive safety net (packet § 7.1).
