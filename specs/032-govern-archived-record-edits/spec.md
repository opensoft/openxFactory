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

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/document-lifecycle.md` MUST state the neutral bookkeeping-note
  minimum as a form the lifecycle header block accepts, quoting
  `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` exactly as the
  ratified requirement states it, including the em dash and the placeholder
  spellings.
- **FR-002**: That passage MUST say the note is recorded in the EDITED FILE'S OWN
  lifecycle-header block, and MUST say the note is not the authorization for the
  edit.
- **FR-003**: That passage MUST carry a ratification citation for
  `govern-archived-record-edits` in a spelling this document's § *Status Claim
  Rules* sanctions. [NEEDS CLARIFICATION: Q3 — `Ratified by:`-style inline
  citation now, while the delta is ratified but not yet promoted, or a form that
  waits for promotion at the archive act?]
- **FR-004**: The passage's placement MUST be beside the `Status:` / `Ratified
  by:` header rules, per task 3.4. [NEEDS CLARIFICATION: Q2 — a bullet inside
  § *Status Claim Rules*, a `###` subsection under it, or a new top-level
  section?]
- **FR-005**: The passage MUST NOT state more of the route than the ratified
  requirement states, and MUST NOT introduce a rule the delta does not carry.
  [NEEDS CLARIFICATION: Q2b — note form only, or note form plus the
  recorded-ruling and bookkeeping-class sentences?]
- **FR-006**: `tasks.md` boxes whose acts this feature performs MUST be ticked
  with a dated note naming the evidence. [NEEDS CLARIFICATION: Q1 — which of the
  28 boxes this realization ticks, and in particular whether the already-performed
  § 0.1 re-stamp, the § 1 `[OPERATOR]` ratification boxes, the § 2 authoring
  boxes and § 5.1 are ticked on the record the packet already cites.]
- **FR-007**: `tasks.md` boxes belonging to the OpsxFactory twin, another
  DomainxFactory or another openxFactory packet MUST be left UNTICKED and MUST
  carry a dated note naming the owing repository or packet.
- **FR-008**: The re-derivation obligation of the second ADDED requirement MUST
  be discharged as a MEASUREMENT for every file this feature edits: each edited
  path is checked against the repository's content-address pins and the result
  recorded. [NEEDS CLARIFICATION: Q8 — where that measurement is recorded: the
  feature's evidence artifact, the packet, or the PR body only?]
- **FR-009**: No file under `openspec/changes/archive/` may be edited by this
  feature, and no ratified requirement text may be reworded.
- **FR-010**: The ratified packet files other than `tasks.md` MUST NOT be edited
  unless the architect rules otherwise. [NEEDS CLARIFICATION: Q10 — may this
  feature touch `proposal.md`/`design.md` at all (for example to resolve the
  twin's cross-citations at task 3.1), or is `tasks.md` the only packet file
  this branch may write?]
- **FR-011**: Every § 4 gate MUST be run at the final head and its output
  recorded verbatim, including the doc-health finding-set diff against `main`.
- **FR-012**: The § 4.2 MODIFIED-block currency check MUST be re-run at the final
  head and recorded as a measurement. [NEEDS CLARIFICATION: Q6 — ticked here, or
  left for the archive act which is where "before archive" lands?]
- **FR-013**: Gate evidence MUST live in a named artifact a later reader can
  re-run. [NEEDS CLARIFICATION: Q4 — the Speckit feature directory only, or also
  an `evidence/` file inside the change packet?]
- **FR-014**: Every commit on this branch MUST carry the `Lane: opsXfactory-1`
  trailer, the `Co-Authored-By` trailer and the session link, and MUST stage
  explicit paths.
- **FR-015**: This feature MUST stop at a branch ready for the archive act. It
  MUST NOT run `openspec archive`, open a pull request, post a GitHub comment,
  or merge.
- **FR-016**: This feature MUST write no checker, edit no pin, and repair no
  broken pin — the packet's own § *What This Change Does NOT Do*.

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
  the final head.
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
  `specs/032-govern-archived-record-edits/`, `docs/document-lifecycle.md`, and
  `openspec/changes/govern-archived-record-edits/tasks.md` (plus whatever Q4/Q10
  add), and nothing under any `archive/` path.
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
