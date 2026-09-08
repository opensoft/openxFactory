# Feature Specification: The promoting repository performs its own acts under the archived-record-edit rule

**Feature Branch**: `032-govern-archived-record-edits`
**Created**: 2026-09-08
**Status**: Draft
**Realizes**: openxFactory OpenSpec change `govern-archived-record-edits`
(ratified 2026-09-08 by Brett Heap, CLI approval `gh pr review 788 --approve`,
GitHub review 5141756427, APPROVED 2026-09-08T12:38:36Z, empty body; landed as
PR #788 → main `3504287a`; record
`openspec/changes/govern-archived-record-edits/review/ratification-2026-09-08.md`)
**Lane**: opsXfactory-1

**THE RATIFIED PACKET IS THE AUTHORITY, NOT THIS FILE.** Every requirement below
is a REALIZATION act. Nothing here restates, narrows or widens the three
ratified requirement blocks in
`openspec/changes/govern-archived-record-edits/specs/document-lifecycle/spec.md`,
and no act in this feature edits them. Where this file and the packet appear to
differ, the packet governs and this file is the defect.

**Input**: Realize the openxFactory half of the matched pair — this
repository's OWN acts: the § 3.4 adoption of the neutral bookkeeping-note
minimum in `docs/document-lifecycle.md`, the truthful task record for the 28
boxes, and the § 4 gate evidence the archive act reads — through to a branch
ready for the archive act, which the lane performs.

## Measured baseline

- Branch cut from `main` at **`68712924`** (Merge PR #811). The ratification
  merge `3504287a` (PR #788) IS an ancestor of that head, measured with
  `git merge-base --is-ancestor`.
- **The packet has not moved since ratification.**
  `git log 3504287a..68712924 -- openspec/changes/govern-archived-record-edits
  openspec/specs/document-lifecycle docs/document-lifecycle.md` is EMPTY, so
  the ratified bytes, promoted canon and the target document are all unchanged
  at this base. Task 4.2's currency check therefore starts from an unmoved
  canon and is re-measured rather than assumed.
- **The § 0 and § 5.1 bookkeeping already landed with #788.**
  `tests/sequenced_after/corpus-ledger.yaml:214` carries
  `moved_by: "#788", moved_on: "2026-09-08"`, and `README.md:515` carries the
  packet's "OpenSpec Records" row. Neither is authored again here.
- **No in-repo content-address pin names `docs/document-lifecycle.md`**, so the
  § 3.4 edit is not a pinned-target edit. Measured two ways: `contracts/manifest.yaml`
  contains ZERO `docs/`-prefixed path values (parsed, not grepped), and no
  `*.yaml|*.yml|*.json` file in the repository pairs a `sha256` with that path.
  The only occurrences of the path beside a digest are in `examples/document-cataloging/`,
  which are illustrative fixtures rather than live pins.
- **doc-health does not scan the Speckit tree.** `GOVERNED_ROOTS` is
  `("contracts", "docs", "examples", "ideation", "templates")`, so
  `specs/032-*` adds no finding; `docs/document-lifecycle.md` IS scanned, so the
  § 3.4 edit is the only act in this feature that can move the finding set.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The repository promoting the rule states the note the rule demands (Priority: P1)

An engineer or agent about to repair a lifecycle header on a file under
openxFactory's `openspec/changes/archive/` opens this repository's own lifecycle
document and finds the form of the bookkeeping note that the edit must carry —
without having to read a change packet or another repository's convention. Today
that document says nothing about archived-record edits at all, which is the gap
the ratified requirement's neutral minimum exists to close (proposal § *Impact*:
"openxFactory — THIS repository — owes one too, and it was missed for two
drafts").

**Why this priority**: it is the ONLY task in the packet's § 3 that is this
packet's own act in this repository, and § 6.1 makes it the single box that
holds the packet open. Everything else in this feature is bookkeeping or
evidence about it.

**Independent Test**: read `docs/document-lifecycle.md` alone at this branch's
head and recover the note's exact form, its placement (the edited file's own
lifecycle-header block) and the change that ratified it, with no other file
open.

**Acceptance Scenarios**:

1. **Given** `docs/document-lifecycle.md` at this branch's head, **When** a
   reader looks for the form a bookkeeping note takes, **Then** the document
   states the dated line `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>`
   byte-for-byte as the ratified requirement states it, and says it belongs in
   the edited file's own lifecycle-header block.
2. **Given** the same document, **When** a reader asks what authorizes the
   edit, **Then** the document says the note is NOT the authorization and names
   the recorded-ruling requirement, so the note-alone reading the measured
   breach relied on is closed here too.
3. **Given** the same document, **When** a reader asks by what authority this
   text stands, **Then** the passage carries a ratification citation naming
   `govern-archived-record-edits`, in the spelling this document's own § *Status
   Claim Rules* sanctions.
4. **Given** doc-health run over the branch and over `main`, **When** the two
   finding sets are diffed, **Then** they are identical (task 4.4).

---

### User Story 2 - The task record says who did what, and does not claim another repository's work (Priority: P2)

A reader of `openspec/changes/govern-archived-record-edits/tasks.md` after this
feature lands can tell, box by box, what was performed in openxFactory, what was
performed by Brett Heap, what belongs to the OpsxFactory twin or a further
DomainxFactory, and what belongs to another openxFactory packet — without
inferring any of it.

**Why this priority**: the packet's own preamble made "every box unticked" a
claim that the packet had not begun. It has now begun, so leaving the list
untouched would be as false as ticking a box on someone else's behalf. The
corpus practice is that an archived change's boxes are ticked (six most recent
archived changes: 28/0, 28/1, 21/0, 39/0, 40/0, 26/0 ticked/unticked), and the
one unticked box in that sample carries an explicit "NOT OWED HERE" note.

**Independent Test**: read `tasks.md` alone and, for every one of the 28 boxes,
name the repository and the actor responsible, and for every unticked box read a
dated note saying why it is not this feature's to tick.

**Acceptance Scenarios**:

1. **Given** a box whose act this feature performed, **When** the box is read,
   **Then** it is ticked and carries a dated note naming the evidence.
2. **Given** a box tagged `[OpsxFactory]` or belonging to another openxFactory
   packet, **When** the box is read, **Then** it is UNTICKED and carries a dated
   note naming the repository or packet that owes it.
3. **Given** the whole file, **When** it is read against this feature's diff,
   **Then** no box is ticked whose act happened outside this branch and outside
   the record the packet already cites.

---

### User Story 3 - The archive act finds its evidence already measured (Priority: P3)

The lane performing the archive act reads one place and finds every § 4 gate
result at a named head, including the MODIFIED-block currency re-check that
`A MODIFIED requirement block restates the requirement as canon currently states
it` demands continuously until archive.

**Why this priority**: the gates are the archive act's precondition, not this
feature's product; but an archive act that has to re-derive them is an archive
act that will skip one.

**Independent Test**: from the feature's evidence artifact alone, re-run each
named command at the named head and reproduce each stated result.

**Acceptance Scenarios**:

1. **Given** the branch head, **When** the pinned-CLI entrypoint runs
   `--change govern-archived-record-edits --strict` and `--all --strict`,
   **Then** both are recorded with their pass/fail counts and zero
   undispositioned findings.
2. **Given** the branch head, **When** the MODIFIED block is compared with
   promoted canon, **Then** the comparison is recorded as a measurement (canon
   bytes carried, lines removed) rather than asserted.
3. **Given** the branch head, **When** `validate-sequenced-after.py .`,
   `--ledger-diff`, `validate-scope-globs.py .`, `validate-manifest-digests.py .`
   and `pytest tests/sequenced_after tests/proposal-support tests/scope_globs -q`
   run, **Then** each result is recorded verbatim.

### Edge Cases

- **Canon moves under the MODIFIED block while this feature is open.** The block
  must be brought forward before archive (task 4.2). Measured at this base canon
  has not moved; the check is re-run at the final head rather than trusted.
- **Another lane lands a substrate change first.** The README Records row and
  the ledger row are already on `main` from #788; if `main` moves under this
  branch, the branch merges forward and never rebases pushed commits.
- **The § 3.4 text drifts from the ratified requirement.** Any wording that
  states MORE than the requirement states would be this repository restating
  promoted-adjacent policy in different words — the § *Explicit Delta Rule*
  defect — so the adopted text is quoted from the requirement and cited to it.
- **A box's act is performed after this branch is cut** (for example the twin's
  landing). This feature does not re-open to tick it; it leaves the dated note
  naming where the act lives.
- **doc-health's finding set moves for a reason unrelated to this diff** (word
  counts, canon share). The diff is taken over the FINDING SET, and any residual
  difference is explained or the edit is reworked.

## Clarifications

### Session 2026-09-08 (architect seat, lane `opsXfactory-1`, after cross-model adversarial review)

Ten questions asked and answered; the full block with reasoning is
`clarify-questions.md` in this directory.

- **Q1 → (b)** tick every box whose act is verifiably DONE, `[OPERATOR]` boxes
  included (act-done, not actor-class), with no invented quotation, with the
  three ratified "stays unticked" sentences amended in the same commit, and with
  3.1 and 4.2 excepted.
- **Q2 → (a) + (ii)** a top-level bullet at the end of § *Status Claim Rules*;
  note form plus two explanatory sentences, minimal prose.
- **Q3 → (b)** the precedent citation form, with the archive-act phrase in a
  following sentence.
- **Q4 → (b)** evidence in the packet's `evidence/` directory as well as here.
- **Q5 → (c)** per-box notes, one NOT-OWED-HERE line per unticked box, tick and
  evidence in the same commit.
- **Q6 → (b)** 4.2 measured but left UNTICKED for the archive act.
- **Q7 → (b)** twin notes cite repository, change id and PR #279; no merge sha.
- **Q8 → (b)** the pinned-target measurement recorded in both places, worded
  "no IN-REPO sha256 pin … measured at base `68712924`".
- **Q9 → (a)** the full Speckit tree is committed.
- **Q10 → (b)** `tasks.md`, the evidence file, and one additive dated note in
  `proposal.md`; everything else in the packet frozen.

## Architect rulings open to veto

Three rulings above go beyond what the ratified packet strictly prescribes. They
proceed unless Brett Heap says otherwise, and they are named here so the
realization PR body can cite them rather than bury them:

1. **The enumeration note in `proposal.md`** (Q10) — additive dated prose inside
   text ratified as written. Declining it leaves the ratified enumeration of the
   packet's whole diff false from the moment realization lands.
2. **Ticking § 1's `[OPERATOR]` boxes** (Q1) — an agent ticking boxes that record
   Brett Heap's own acts, together with the amendment of the three ratified
   "stays unticked" sentences. Declining it leaves five boxes for him to tick
   before archive.
3. **Q2b's two explanatory sentences** — arguably more than task 3.4's "record
   the minimum". Declining them leaves the note recorded with no statement that
   it is not the authorization.

**EACH IS REVERSIBLE BY ONE NAMED ACT, and the branch does not wait on the
word.** (1) revert the `proposal.md` note commit; (2) untick the § 1 boxes and
restore the three sentences, each by a dated line naming the reversal; (3) delete
the two explanatory sentences from the bullet. All three are forward-only
corrections under FR-021 — no history is rewritten — and each is small enough
that carrying the ruling now costs less than waiting.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/document-lifecycle.md` MUST state the neutral bookkeeping-note
  minimum as a form the lifecycle header block accepts, quoting
  `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` exactly as the
  ratified requirement states it, including the em dash and the placeholder
  spellings.
- **FR-002**: That passage MUST say the note is recorded in the EDITED FILE'S OWN
  lifecycle-header block, and MUST say the note is not the authorization for the
  edit. "The edited file's own lifecycle-header block" describes where a FUTURE
  archived-record edit records ITS note; it does NOT describe where this bullet
  sits in `docs/document-lifecycle.md`, which is body prose in § *Status Claim
  Rules* and deliberately outside that document's own header window.
- **FR-003**: That passage MUST carry the inline citation "Ratified by
  `govern-archived-record-edits` (2026-09-08)" — the precedent form, WITHOUT a
  colon after the change name — and MUST state that the requirement reaches
  promoted canon at the archive act in a FOLLOWING sentence, never inside the
  citation clause. (Q3 = b.)
- **FR-004**: The passage MUST be a new TOP-LEVEL BULLET at the end of
  § *Status Claim Rules*, with sub-bullets, in the shape the
  `govern-openspec-corpus-membership` bullet already uses in that section.
  (Q2a = a.)
- **FR-005**: The passage MUST carry the note form PLUS exactly two further
  sentences — one saying the ruling is recorded before the edit, one saying the
  note records WHAT changed and never THAT IT MAY — written as EXPLANATION of
  why the note is not self-authorizing rather than as requirement text, the
  requirement text being the packet's and reaching canon at archive. The prose
  MUST stay minimal: `docs/` is a doc-health governed root and gate 4.4 diffs the
  finding set. It MUST NOT introduce a rule the delta does not carry, and MUST
  NOT claim `standard` authority the corpus does not back (the document's own
  line 57) — the inline citation of FR-003 is what backs it. (Q2b = ii.)
- **FR-006**: EVERY `tasks.md` box whose act is verifiably DONE MUST be ticked
  with a dated note naming the evidence — the § 0.1 re-stamp, the § 1
  `[OPERATOR]` ratification boxes, the § 2 authoring boxes and § 5.1 included.
  The test is ACT-DONE, not actor-class (precedent: archived
  `2026-09-04-create-medxchart-overlay-boundary` § 5.3 and
  `2026-09-05-add-release-tag-gate` § 4.1 are both ticked `[OPERATOR]` boxes).
  A § 1 note MUST cite the record as the record does — GitHub review
  `5141756427`, APPROVED `2026-09-08T12:38:36Z`, and
  `review/ratification-2026-09-08.md` — and MUST NOT quote a word: the approval
  body is EMPTY and no verbatim word exists. A note MAY restate a fact the record
  states and MUST NOT attribute words to the ratifier — restating what a record
  says is citation; putting a sentence in his mouth is invention. Boxes 3.1 and 4.2 are NOT ticked
  (FR-007, FR-012). (Q1 = b.)
- **FR-007**: `tasks.md` boxes belonging to the OpsxFactory twin, another
  DomainxFactory or another openxFactory packet MUST be left UNTICKED, each
  carrying ONE dated "NOT OWED HERE" line in the
  `2026-09-05-mirror-floor-addition-grace` § 6.3 shape. A twin note MUST name
  the repository, the change id and **PR #279** as the landing vehicle at this
  date, and MUST NOT cite a merge sha — the twin is not on OpsxFactory `main`
  and no such sha exists. Task 3.1 stays unticked with a NOT-OWED-YET note that
  ALSO records that the cross-citation re-check it names remains OWED and is not
  attempted here — the packet's own text gives that re-check no actor and no
  trigger, and this feature invents neither. (Q5 = c, Q7 = b.)
- **FR-008**: The re-derivation obligation of the second ADDED requirement MUST
  be discharged as a MEASUREMENT for every file this feature edits, recorded BOTH
  in the packet's evidence file AND as a dated note in `tasks.md` beside § 4. The
  note MUST read that **no IN-REPO `sha256` pin names `docs/document-lifecycle.md`,
  measured at base `68712924`** — "in-repo" is load-bearing, 1.2a's ratified scope
  being in-repo pointers to in-repo targets, and a broader claim would overstate
  the measurement. (Q8 = b.)
- **FR-009**: No file under `openspec/changes/archive/` may be edited by this
  feature, and no REQUIREMENT OR SCENARIO TEXT in the ratified delta may be
  reworded. The scope is stated this narrowly on purpose: the three `tasks.md`
  process sentences amended under FR-017 are neither archived bytes nor
  requirement text, and FR-009 and FR-017 do not conflict once that boundary is
  named.
- **FR-010**: This branch MUST write exactly three packet files: `tasks.md`, the
  new `evidence/realization-2026-09-08.md`, and ONE purely additive dated
  realization note in `proposal.md`'s HEADER AREA — placed immediately AFTER the
  `Lane: opsXfactory-1` line and NOWHERE ABOVE `Status:` — recording that realization
  adds the evidence file and the `docs/document-lifecycle.md` edit task 3.4 names
  — without it the ratified enumeration of the packet's whole diff becomes false
  on landing (precedent: `align-status-reader-to-real-lines`, Brett Heap's
  2026-08-19 correction of a narrow enumeration). `design.md`, `.openspec.yaml`
  and the spec delta stay FROZEN. (Q10 = b.)
- **FR-010a**: The note MUST NOT be written INSIDE the YAML front matter and MUST
  NOT alter the ratified `code_surface:` value, and the reason is measured:
  `parse_status` finds `Status: ratified` at REAL-LINE INDEX 8 of a 15-line header
  window (`STATUS_SCAN_LINES = 15`), where the whole folded `code_surface` scalar
  counts as ONE real line. Anything inserted above `Status:` moves that header
  toward the edge of the window, and editing the folded scalar would change a
  ratified front-matter value the archive gate reads. The note therefore QUOTES
  the enumeration sentence it corrects rather than rewriting it.
- **FR-011**: Every § 4 gate MUST be run at the final head and its output
  recorded verbatim, including the doc-health finding-set diff against `main`.
- **FR-012**: The § 4.2 MODIFIED-block currency check MUST be re-run at the final
  head and recorded as a measurement, and box 4.2 MUST be left **UNTICKED** for
  the archive act, with a dated note saying it is deliberately open: the rule
  demands currency CONTINUOUSLY until archive, and a realization tick would retire
  the clearance signal the `modified-block-currency` family exists to keep live.
  (Q6 = b, reversed on review.)
- **FR-013**: Gate evidence MUST live in
  `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`
  as well as in this feature directory. The `evidence/` segment is excluded from
  doc-health's lifecycle scan set (`EVIDENCE_PARTS`), so that file owes no
  lifecycle header and cannot move gate 4.4's finding set; a `review/` record
  would owe one. (Q4 = b.)
- **FR-014**: Every commit on this branch MUST carry the `Lane: opsXfactory-1`
  trailer, the `Co-Authored-By` trailer and the session link, and MUST stage
  explicit paths.
- **FR-015**: This feature MUST stop at a branch ready for the archive act. It
  MUST NOT run `openspec archive`, MUST NOT run `gh` in any form (no `gh pr
  create`, no `gh pr review`, no `gh api` write), MUST NOT post a GitHub comment,
  and MUST NOT merge. Claiming, the pull request, the LANDING/LANDED notices, the
  claim discharge and the archive act are the lane's.
- **FR-016**: This feature MUST write no checker, edit no pin, and repair no
  broken pin — the packet's own § *What This Change Does NOT Do*.
- **FR-017**: The three ratified `tasks.md` sentences that hold the boxes
  unticked — the preamble "EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE
  PACKET", § 0.1's "THE BOX STAYS UNTICKED", and § 1's "AND THE BOXES BELOW STAY
  UNTICKED" — MUST be amended in the SAME COMMIT that ticks the boxes, each
  amendment NAMING the superseded sentence and the reason, on the precedent of
  commit `3b530009`. The ratification record's "28 boxes, NONE ticked" baseline
  is a historical fact about the ratified head and MUST NOT be touched.
- **FR-018**: A box MUST be ticked in the same commit that records its evidence,
  or neither happens — a tick landing ahead of its evidence is the failure this
  packet exists to refuse.
- **FR-019**: The feature's Speckit tree MUST be committed in full — `spec.md`,
  `clarify-questions.md`, `plan.md`, `research.md`, `quickstart.md`, `tasks.md`,
  `analysis.md` and every file under `checklists/` — as features 030 and 031
  commit theirs. (Q9 = a.)
- **FR-020**: A FAILING GATE IS A BLOCKER. Where any § 4 gate fails, no dependent
  task proceeds, no box is ticked against it, the failure output is recorded in
  the evidence file as it was produced, and the failure is reported at STOP (B).
  A gate result is never reported as passing on the strength of a re-run that
  changed the conditions.
- **FR-021**: CORRECTIONS ARE FORWARD-ONLY. A defect found on this branch is
  repaired by a NEW commit that names what it supersedes; history is never
  rewritten and nothing is force-pushed. A superseded evidence entry is struck
  with a dated line saying which head replaced it, never deleted — an evidence
  file that quietly loses an earlier result is the failure mode this packet's own
  motivating commit demonstrates.
- **FR-022**: The packet is ACTIVE, not archived, so the ratified archived-record
  requirement does not bind this feature's edits to the packet's own files. The
  feature MUST say so where it could be misread, and MUST follow the discipline
  anyway — dated notes, superseded sentences named, nothing deleted — because the
  packet's credibility rests on it.
- **FR-023**: The gate results this branch records are LOCAL evidence at a named
  head. CI on the lane's pull request is a SEPARATE confirmation that this feature
  neither performs nor claims, and the evidence file MUST say which it is.

### Key Entities

- **The ratified packet** — `openspec/changes/govern-archived-record-edits/`:
  five files, 28 boxes, one MODIFIED and two ADDED requirements, 18 scenarios.
  Its `tasks.md` is the only member this feature expects to write.
- **The lifecycle document** — `docs/document-lifecycle.md`, `Status: standard`,
  backed by the promoted `document-lifecycle` spec. The § 3.4 target.
- **The sweep-ledger row** — `tests/sequenced_after/corpus-ledger.yaml:214`.
  Already correct; read, never rewritten.
- **The README Records row** — `README.md:515`. Already landed; read, never
  rewritten.
- **The gate set** — the pinned CLI entrypoint, the sequenced-after validators,
  scope globs, manifest digests, doc-health, and the three pytest paths.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader of `docs/document-lifecycle.md` alone can state the
  bookkeeping note's exact form and where it goes, and the string
  `Edited (bookkeeping):` appears in that document at least once.
- **SC-002**: `validate-openspec-cli-pin.py --change govern-archived-record-edits
  --strict` passes and `--all --strict` reports ZERO undispositioned findings at
  the final head, with the dispositioned-exception COUNT stated as a number and
  compared with the ratified baseline's (99 passed / 2 failed, 0 undispositioned).
  A count that moved in EITHER direction is explained; a lower count is a
  difference too, not a bonus.
- **SC-003**: The doc-health finding set at the final head is diff-identical to
  `main`'s.
- **SC-004**: `validate-sequenced-after.py .` and `--ledger-diff`,
  `validate-scope-globs.py .` and `validate-manifest-digests.py .` all exit 0.
- **SC-005**: `pytest tests/sequenced_after tests/proposal-support
  tests/scope_globs -q` is green, with the `Ran N tests` line captured to a file
  rather than inferred from a pipeline's exit code.
- **SC-006**: Every one of the 28 boxes in `tasks.md` is either ticked with a
  dated evidence note or unticked with a dated note naming its owner; no box is
  left in the pre-realization state.
- **SC-007**: `git diff main...HEAD --stat` shows changes ONLY under
  `specs/032-govern-archived-record-edits/`, `docs/document-lifecycle.md`,
  `openspec/changes/govern-archived-record-edits/tasks.md`,
  `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`
  and `openspec/changes/govern-archived-record-edits/proposal.md` — and nothing
  under any `archive/` path, nothing in `design.md`, `.openspec.yaml` or the spec
  delta.
- **SC-008**: The MODIFIED block's currency against promoted canon is recorded
  with a number (canon bytes carried, canon lines removed) at the final head.

## Assumptions

- The packet is ratified AS WRITTEN and the three veto points were not
  exercised: every declared family, report-then-refuse, two ADDED requirements.
  This feature does not reopen them.
- `main` moves frequently in this repository; the branch merges forward from
  `main` and never rebases pushed commits.
- The lane — not this feature — claims, opens the PR, posts LANDING/LANDED,
  discharges the claims on issue #630, and performs the archive act.
- Work happens only in the dedicated clone at
  `<scratchpad>/oxf-realize-f3`; the shared checkouts are never touched.
- The pinned OpenSpec CLI 1.12.0 at `<scratchpad>/cli-pin-prefix/bin/openspec`
  is the only CLI used; PATH's 1.2.0 is never used.

## Out of scope

- **Task 3.3** — `add-consent-custody-rederivation-record`'s contract cut. Another
  openxFactory packet's act, named in the record and not performed here.
- **Tasks 3.1, 3.2, 3.5 and every `[OpsxFactory]` box** — the domain twin
  (OpsxFactory PR #279, ratified, realized by a sibling orchestrator), its
  content-address family register, and every other DomainxFactory's convention.
- **The archive act (§ 6) and the landing acts (§ 5.2, § 5.3)** — the lane's.
- **Any checker, gate or workflow** — the packet declares `code_surface: none`
  and builds no checker by design (D-6).
- **Any edit to a file under `openspec/changes/archive/`** — including under the
  rule this packet states.
- **Any re-derivation of the README "OpenSpec Records" row at a union with
  another lane's row** (task 5.1, lane-protocol Rule 7): the row is already on
  `main` from #788, and a union re-derivation, if one becomes necessary, is the
  lane's act at landing.
- **CI**: no workflow run is triggered, awaited or claimed here (FR-023).
