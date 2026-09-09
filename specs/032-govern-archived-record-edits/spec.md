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

**ARCHIVE NOTE, DATED 2026-09-09 AND ADDED BY `archive-govern-archived-record-edits`
(lane `opsXfactory-1`).** The packet this feature realizes was ARCHIVED on
2026-09-09, on Brett Heap's separate archive word of `2026-09-09T12:15:01Z` (in
session, first-hand to the lane, verbatim *"archive both"*), and now lives at
`openspec/changes/archive/2026-09-09-govern-archived-record-edits/`. **THE
LIVE-PATH CITATIONS THROUGHOUT THIS FEATURE DIRECTORY ARE LEFT AS AUTHORED, AND
THAT IS A MEASURED DECISION RATHER THAN AN OMISSION.** Read
`openspec/changes/govern-archived-record-edits/<file>` anywhere below as
`openspec/changes/archive/2026-09-09-govern-archived-record-edits/<file>`. Three
reasons, in order of weight:

1. **THE CORPUS'S CONVENTION IS MEASURED, NOT ASSUMED.** Twelve Speckit feature
   directories in this repository realize packets that have since archived —
   `002`, `003`, `004`, `007`, `016`, `018`, `019`, `020`, `022`, `023`, `024`
   and `026` — and they carry **98 live-path occurrences of their own packet's
   id and ZERO archive-path occurrences** between them, counted by regular
   expression over every file in each tree. Not one was repointed at its
   packet's archive. The one repoint in the tree's history (`3d7b8f3b`,
   `specs/029`) moved a SINGLE pointer to a ratification record, in a file whose
   only other citation was already authored in archive form; it is a pointer
   fix, not a sweep.
2. **MOST OF THESE CITATIONS ARE NOT POINTERS AT ALL.** Several sit inside git
   commands whose PATHSPEC is evaluated over a commit range that PREDATES the
   move (`git log 3504287a..68712924 -- openspec/changes/govern-archived-record-edits`),
   where the live path is the CORRECT one and the archive path matches nothing.
   Others sit inside dated `**Done 2026-09-08**` records of acts performed at
   that path on that day. Rewriting either would turn a true record false —
   which is the same test the requirement this feature realizes applies to an
   archived record, applied here to a living one.
3. **openxFactory HAS NO CITATION GATE.** OpsxFactory's pre-archive citation
   gate, which would refuse a live-path citation of an archived packet, is that
   repository's and is not in force here — so no gate is being worked around,
   and this note records the reasoning a gate would otherwise have forced.

One assertion in `tasks.md` (T033) DID become false at the move and carries its
own dated correction there rather than being covered by this note.

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
  `moved_by: "#788", moved_on: "2026-09-08"`, and `README.md:659` carries the
  packet's "OpenSpec Records" row. Neither is authored again here.
- **No in-repo content-address pin names `docs/document-lifecycle.md`**, so the
  § 3.4 edit is not a pinned-target edit. **CORRECTED 2026-09-08 during
  realization — the method as originally stated would have missed a real
  candidate.** This bullet said the measurement was "no `*.yaml|*.yml|*.json`
  file in the repository pairs a `sha256` with that path". A `sha256`-keyed
  search alone MISSES the fixtures' `content_hash:` key — for example
  `examples/document-cataloging/document-catalog-reference-invalidation.example.yaml`
  pairs the path with `content_hash:` and never with `sha256:` — so a re-runner
  following the old wording would get a different (and falsely clean) result.
  **THE METHOD AS RUN, which a re-runner should follow**: (1) parse
  `contracts/manifest.yaml` as YAML and walk every string value — ZERO
  `docs/`-prefixed path values; (2) `grep` the repository's `*.yaml|*.yml|*.json`
  for the PATH itself, not for a digest key — FIVE files name it; (3) resolve
  each of the five by reading what sits beside the path, `content_hash:` and
  `passage_sha256:` as well as `sha256:`. The conclusion is unchanged and is now
  reached by a method that would have found the candidate: the only pairings live
  in `examples/document-cataloging/` (plus one comment in a contracts schema and
  one prose mention in an archived `.openspec.yaml`), and they are illustrative
  fixtures rather than live pins — PROVEN, not asserted, because
  `scripts/validate-document-catalog.py` validates their SHAPE and never hashes a
  file on disk, and doc-health's catalog families read `health/document-catalog/`,
  which does not exist in this repository.
- **THE OPSXFACTORY TWIN HAS LANDED.** `govern-archived-record-edits` merged into
  OpsxFactory `main` as **`bbbef015cd394e2de31586b9718356586c413884`** (PR #279,
  committed 2026-09-08T11:28:23-04:00 = **2026-09-08T15:28:23Z**), verified in a
  read-only clone: `git merge-base --is-ancestor bbbef015… origin/main` succeeds.
  Every statement in this feature that the twin had not landed is superseded by
  this measurement.
- **The packet holds SIX files AT THE RATIFIED HEAD, and SEVEN after
  realization — each count names its head, because the two are both true and
  neither supersedes the other.** At `main` `3504287a` / base `68712924`: SIX,
  counted rather than carried forward from the ratification record's five-file
  baseline (which predates its own `review/` record) — `.openspec.yaml`,
  `design.md`, `proposal.md`, `tasks.md`, `review/ratification-2026-09-08.md`,
  `specs/document-lifecycle/spec.md`. At this branch's head, SEVEN: realization
  adds `evidence/realization-2026-09-08.md`, which is exactly what the
  `proposal.md` realization note records. A statement of the count is therefore
  incomplete without its head.
- **doc-health stamps the CHECKOUT'S DIRECTORY BASENAME into every finding** —
  `repo=<basename>`, the `Repo-Identity:` header, and the "scope limited to
  single repo <name>" line — so a baseline taken in a differently-named directory
  differs on EVERY line. The comparison therefore uses an identically-named
  baseline checkout or normalizes those three places, and the recipe is proven
  main-vs-main first.
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
   states the dated line `Edited (bookkeeping): <UTC date> by <change-id> —
   <edit class>`
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
5. **Given** another lane has landed its own bullet or row into a file this branch
   also writes, **When** this branch merges `main` forward, **Then** the adopted
   bullet still sits at the END of § *Status Claim Rules*, the appended README
   sentence still sits at the END of this change's own row, and the § 4 gate set
   is re-run at the merged head before anything is ticked against it.

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

## Primary flow, in one ordered narrative

A reader who wants the shape of this feature without reading the task graph gets
it here. The branch (1) adopts the neutral minimum in `docs/document-lifecycle.md`;
(2) opens the packet's evidence file and takes the two measurements — the
pinned-target check and the MODIFIED-block currency — at a named head; (3) runs
the § 4 gate set and records every command, return code and summary line; (4)
re-checks the cross-citations against the landed twin on both `main` lines; (5)
writes the packet's `tasks.md` in ONE commit — the ticks, their evidence notes,
the NOT-OWED lines, the § 4 pinned-target note, the amendment of the three
"stays unticked" sentences, and the two heading amendments; (6) appends the
additive realization note to `proposal.md` and the superseding sentence to the
README row; (7) re-runs the whole gate set at the final head; (8) verifies the
diff's path set, the trailers, the note-class sum and the Speckit tree; and (9)
STOPS with the report. Nothing merges, nothing archives, and no `gh` runs at any
step.

### Edge Cases

**EVERY EDGE CASE BELOW CARRIES THE SAME RECORD OBLIGATION**, stated once rather
than repeated in each: when one occurs, the evidence file records WHAT happened,
the head it happened at, what was re-run or re-taken, and what — if anything —
was struck. An edge case handled and unrecorded is indistinguishable from one
that never happened.


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
  difference is explained or the edit is reworked — where "reworked" means the
  added prose is narrowed until the finding disappears, never that the finding is
  dispositioned away by this feature.
- **A forward merge is taken after the final gate run.** The run is stale: either
  the gates are re-run at the new head, or the merge waits (FR-011).
- **`main` moves between the doc-health baseline and the final comparison.** The
  baseline is re-taken at the commit last merged from, and both shas are recorded
  (FR-029).
- **A gate cannot be RUN at all** — a missing dependency, an unavailable baseline
  checkout. That is not a failure result; it is recorded as "could not run", named
  as such, and the branch stops (FR-025).
- **PR #279 is renumbered, closed or superseded.** The twin's identity in every
  note rests on the MERGE SHA `bbbef015…` and the repository, with the PR number
  as a convenience pointer; a moved number does not invalidate the citation.
- **A sibling lane lands a bullet in § *Status Claim Rules* first.** The adopted
  bullet is appended at the section's end, so the collision is a merge of two
  appends; the branch merges forward and re-runs the gates (FR-011).
- **An invented quotation is discovered after a commit lands.** It is corrected
  under FR-021 with the invented words quoted in the correction, never silently
  edited out (FR-027).

## Clarifications

### Session 2026-09-08 — consistency panel (gates-only fan-out), applied

The panel read the branch at `2de9cca7` against the ratified packet and the ten
rulings, and returned PROCEED AFTER FIXES. Applied here: **P1** the doc-health
recipe was identity-unsafe (FR-028); **P2** the twin HAS LANDED, so the
"no merge sha" reading is struck and 3.1 is ticked on a performed cross-citation
check (FR-007, FR-007a, SC-010); **P3** a failed final-head gate strikes the
affected tick forward-only (FR-020/FR-021, task T029); **P4** the amendment form
is commit `3b530009`'s — block quote plus the neighbouring clause named — and
reaches every measured passage (FR-017a); **P5** `proposal.md` lines 17 and 44
also assert the unticked state (FR-010b); **P6** the packet holds SIX files, not
five; **P7** SC-002's two-direction comparison is a task; **P8** SC-001 is
verified as the full line form; **P9** the citation is the bullet's last clause
(FR-003). Mirror rulings from the OpsxFactory half: **M-A1** the README row
sentence (FR-010c, veto point 4); **M-A7** the § 1 heading amendment (FR-017b,
veto point 5); **M-A3** the § 3 heading amendment (FR-017b); **M-A6** dated
CORRECTED blocks for stale-but-true-when-written text, and the three note classes
that must sum to 28 (FR-017c, FR-026).

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

FIVE rulings go beyond what the ratified packet strictly prescribes. They proceed
unless Brett Heap says otherwise, they each name the requirements they produced so
a veto identifies exactly what is reverted (FR-031), and they are listed here so
the realization PR body can cite them rather than bury them:

1. **The enumeration note in `proposal.md`** (Q10 → FR-010, FR-010a, FR-010b) —
   additive dated prose inside text ratified as written. Declining it leaves the
   ratified enumeration of the packet's whole diff false from the moment
   realization lands.
2. **Ticking § 1's `[OPERATOR]` boxes** (Q1 → FR-006, FR-017, FR-017a) — an agent
   ticking boxes that record Brett Heap's own acts, together with the amendment of
   the three ratified "stays unticked" sentences. Declining it leaves five boxes
   for him to tick before archive.
3. **Q2b's two explanatory sentences** (Q2b → FR-005) — arguably more than task
   3.4's "record the minimum". Declining them leaves the note recorded with no
   statement that it is not the authorization.
4. **The README Records row sentence** (mirror ruling M-A1 → FR-010c) — this
   branch writes `README.md`, which the earlier scope froze. **The row makes the
   now-false claim TWICE, not once** — at `README.md:671` ("**all 28 boxes in
   `tasks.md` stay unticked**, § 1's ratification boxes included") and again at
   `README.md:689-692` ("**NOTHING IS REALIZED** — … and **all 28 boxes in
   `tasks.md` stay unticked**"), where BOTH halves fail: 19 boxes are ticked, and
   `docs/document-lifecycle.md` IS amended, so "NOTHING IS REALIZED" is false in
   its own right. ONE amendment block-quotes both. Declining leaves two false
   sentences in the repository's own index of records.
5. **Amending the § 1 heading "Ratification — OWED, NOT GIVEN"** (mirror ruling
   M-A7 → FR-017b) — the packet's own ratified text says the heading is left as
   written ON PURPOSE, so amending it supersedes a deliberate decision, which is
   why the amendment must NAME that clause. Declining leaves a section heading
   that says a thing is owed which was given on the day the packet was ratified.

**EACH IS REVERSIBLE BY ONE NAMED ACT, and the branch does not wait on the
word.** (1) revert the `proposal.md` note commit; (2) untick the § 1 boxes and
restore the three sentences, each by a dated line naming the reversal; (3) delete
the two explanatory sentences from the bullet; (4) revert the README row's
appended sentence; (5) restore the § 1 heading and strike its amendment, by a
dated line naming this reversal. All FIVE are forward-only corrections
under FR-021 — no history is rewritten — and each is small enough that carrying
the ruling now costs less than waiting. **The veto arrives as an architect ruling
relayed to this orchestrator, or as Brett Heap's own word on the realization PR;
there is no waiting period** — the branch proceeds, and a veto exercised later is
performed as the named reversal act.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001** (origin: task 3.4 of the ratified packet): `docs/document-lifecycle.md` MUST state the neutral bookkeeping-note
  minimum as a form the lifecycle header block accepts, quoting
  `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` exactly as the
  ratified requirement states it, including the em dash and the placeholder
  spellings.
- **FR-002** (origin: the first ADDED requirement's neutral minimum): That passage MUST say the note is recorded in the EDITED FILE'S OWN
  lifecycle-header block, and MUST say the note is not the authorization for the
  edit. "The edited file's own lifecycle-header block" describes where a FUTURE
  archived-record edit records ITS note; it does NOT describe where this bullet
  sits in `docs/document-lifecycle.md`, which is body prose in § *Status Claim
  Rules* and deliberately outside that document's own header window — the
  status-header scan reads the first 15 REAL lines (`STATUS_SCAN_LINES = 15`) and
  the bullet sits far below them. The passage MUST NAME the requirement it
  records — *An archived record is edited only as a bookkeeping correction under
  a recorded ruling* — so a reader can reach the rule from the note.
- **FR-003**: That passage MUST carry the inline citation "Ratified by
  `govern-archived-record-edits` (2026-09-08)" — the precedent form, WITHOUT a
  colon after the change name — as the LAST CLAUSE of the bullet's parent prose,
  which is where the precedent bullet puts its own
  (`docs/document-lifecycle.md`, "…exists to make checkable. Ratified by
  `govern-openspec-corpus-membership` (2026-08-23)."). The statement that the
  requirement reaches promoted canon at the archive act MUST sit EARLIER in that
  prose, never inside or after the citation clause; sub-bullets follow the
  citation, as they do in the precedent. (Q3 = b, panel P9.)
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
- **FR-005a**: THE QUOTED FORM IS TYPOGRAPHICALLY DISTINCT FROM THE EXPLANATION.
  The note form is written as a code span (`Edited (bookkeeping): …`); the two
  explanatory sentences are plain prose. A reader, and a later diff, can tell
  which bytes are the ratified form and which are this document's gloss.
- **FR-005b**: THE RATIFIED-BUT-NOT-PROMOTED POSITION IS STATED, NOT LEFT TO
  INFERENCE. The document is `standard` and line 57 forbids claiming authority the
  corpus does not back; this requirement is ratified and reaches promoted canon
  only at the archive act. The passage records the minimum ON THE AUTHORITY OF THE
  NAMED CHANGE, says so in its own words, and does not assert that canon already
  carries it.
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
  says is citation; putting a sentence in his mouth is invention.
- **FR-006a**: ACT-DONE RESTS ON AN INDEPENDENT DURABLE RECORD — a commit sha, a
  merge sha, a GitHub review id, or a path in this repository. A box is never
  ticked on this session's recollection, and a reader six months later must reach
  the same record from the note alone.
- **FR-006b**: EVERY TICKED NOTE CARRIES THREE THINGS: the act performed, the UTC
  date, and the pointer to its evidence. That minimum reaches § 2's authoring
  boxes and § 5.1's bookkeeping box as much as § 1's ratification boxes; a class
  label (FR-026) is not a substitute for the content. Boxes 3.1 and 4.2 are NOT ticked
  (FR-007, FR-012). (Q1 = b.)
- **FR-007**: `tasks.md` boxes belonging to the OpsxFactory twin, another
  DomainxFactory or another openxFactory packet MUST be left UNTICKED, each
  carrying ONE dated "NOT OWED HERE" line in the
  `2026-09-05-mirror-floor-addition-grace` § 6.3 shape. A twin note MUST name
  the repository, the change id, **PR #279** and the merge sha
  **`bbbef015cd394e2de31586b9718356586c413884`** — the twin LANDED on OpsxFactory
  `main` at 2026-09-08T15:28:23Z, so the earlier "no such sha exists" reading is
  superseded by measurement. (Q5 = c, Q7 = b as amended by panel P2.)
- **FR-007a**: Because the twin has landed, task 3.1's act is DONE and the box is
  TICKED. The tick MUST rest on a performed check, not on the merge alone: the
  cross-citations MUST be re-checked on BOTH `main` lines — this packet's
  citations of the twin, and the twin's citations of this packet — each MUST
  resolve, and the check MUST be recorded in the evidence file with the two heads
  it was taken at and the sha `bbbef015…`. A citation that does not resolve is a
  BLOCKER under FR-020, never a note.
- **FR-007b**: THE 3.2 AND 3.5 NOTES SAY WHAT IS OWED AND BY WHOM: 3.2 names
  OpsxFactory's `add-content-address-integrity-gate` and the register file it
  proposes; 3.5 names "every other DomainxFactory" as a class, states that no
  survey was performed here, and does not imply one.
- **FR-008**: The re-derivation obligation of the second ADDED requirement MUST
  be discharged as a MEASUREMENT for every file this feature edits, recorded BOTH
  in the packet's evidence file AND as a dated note in `tasks.md` beside § 4. The
  note MUST read that **no IN-REPO `sha256` pin names `docs/document-lifecycle.md`,
  measured at base `68712924`** — "in-repo" is load-bearing, 1.2a's ratified scope
  being in-repo pointers to in-repo targets, and a broader claim would overstate
  the measurement. (Q8 = b.)
- **FR-008a**: THE MEASUREMENT NAMES ITS METHOD, NOT ONLY ITS CONCLUSION: the
  commands in `quickstart.md` § 6, the PARSE of `contracts/manifest.yaml` (parsed
  as YAML rather than grepped — a grep over a folded scalar reports prose that is
  not a path value), and the head. It is RE-TAKEN at the final head (T029): a pin
  arriving with a forward merge is a pin.
- **FR-008b**: TWO FACTS ARE KEPT APART. "No in-repo pin names this file" is a
  statement about POINTERS; "this family has declared no re-derivation rule" is a
  statement about OBLIGATIONS. This feature measures the first and asserts nothing
  about the second. The Explicit Delta Rule is NOT engaged by the adopted passage,
  and the reason is named rather than assumed: that rule refuses UNMARKED
  restatement of promoted policy, and this passage marks its source in the same
  breath as it states the minimum. A path appearing beside a digest under
  `examples/` is an
  ILLUSTRATIVE FIXTURE — the criterion is that no gate reads it as a pin and
  nothing verifies it — and the note names those files rather than leaving
  "fixture" undefined.
- **FR-008c**: CONTINGENCY, BECAUSE A NEGATIVE MEASUREMENT NEEDS ONE. If a pin IS
  found naming a file this feature edits, or a candidate pin cannot be resolved,
  the branch STOPS and reports (FR-025): re-deriving a pin is a contract act this
  feature is not scoped to perform, and landing with the question open is the
  exact failure the packet exists to refuse.
- **FR-009**: No file under `openspec/changes/archive/` may be edited by this
  feature, and no REQUIREMENT OR SCENARIO TEXT in the ratified delta may be
  reworded. The scope is stated this narrowly on purpose: the three `tasks.md`
  process sentences amended under FR-017 are neither archived bytes nor
  requirement text, and FR-009 and FR-017 do not conflict once that boundary is
  named.
- **FR-009a**: THE FROZEN SET, ENUMERATED ONCE AND IN ONE PLACE, so no reader has
  to assemble it from three artifacts: everything under `openspec/changes/archive/`;
  the packet's `design.md`, `.openspec.yaml` and `specs/document-lifecycle/spec.md`;
  `tests/sequenced_after/corpus-ledger.yaml`; `contracts/**` (the CLI pin and its
  `dispositions:` block included); every part of `README.md` EXCEPT the single
  appended sentence FR-010c authorizes; and everything under `scripts/`,
  `.github/` and `tests/`. `plan.md` and `tasks.md` restate this list BY REFERENCE,
  never by re-enumeration. **THE FREEZE IS CONTINUOUS, NOT A ONE-TIME CHECK**: it
  holds at every commit on this branch and is re-verified at the final head
  (SC-007), because a path can enter the diff at any commit and a freeze checked
  once is a freeze that stops holding the moment work resumes.
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
- **FR-010b**: The note MUST cover EVERY sentence in `proposal.md` that the
  realization falsifies, not only the front-matter enumeration: line 17
  ("…and every box in `tasks.md` stays unticked") and line 44 ("…and every box in
  `tasks.md` stays unticked") each assert the unticked state, and each MUST be
  quoted in the note as superseded. (Panel P5.)
- **FR-010c**: This branch ALSO writes `README.md`: ONE dated superseding
  amendment appended at the END of this change's "OpenSpec Records" row. **THE
  ROW ASSERTS THE NOW-FALSE FACT IN TWO PLACES AND THE AMENDMENT MUST QUOTE
  BOTH**: `README.md:671` "**all 28 boxes in `tasks.md` stay unticked**, § 1's
  ratification boxes included", and `README.md:689-692` "**NOTHING IS
  REALIZED** — no archived byte is edited, no pin is re-derived, no checker is
  written, no repository's convention is amended, and **all 28 boxes in
  `tasks.md` stay unticked**." The second is superseded in BOTH halves — 19
  boxes are ticked AND `docs/document-lifecycle.md` is amended — while its three
  other clauses (no archived byte, no pin, no checker; and no convention amended)
  still hold and are named as not superseded. Each quotation is BYTE-EXACT,
  emphasis markers included. The amendment goes at the row's END and NEVER near
  the block anchor, so a concurrent lane's row edit collides on a different line.
  (Mirror ruling M-A1; VETO POINT 4.)
- **FR-011** (origin: the packet's § 4 gate list): Every § 4 gate MUST be run at the final head and its output
  recorded verbatim, including the doc-health finding-set diff against `main`.
  A FORWARD MERGE from `main` taken after that run makes the run stale: the gate
  set MUST be re-run at the new head, or the merge MUST NOT be taken on this
  branch before the stop.
- **FR-012**: The § 4.2 MODIFIED-block currency check MUST be re-run at the final
  head and recorded as a measurement, and box 4.2 MUST be left **UNTICKED** for
  the archive act — and re-taken after any forward merge, since a merge can move
  canon under the block — with a dated note saying it is deliberately open: the rule
  demands currency CONTINUOUSLY until archive, and a realization tick would retire
  the clearance signal the `modified-block-currency` family exists to keep live.
  (Q6 = b, reversed on review.) Where the check finds the block NOT current, the
  branch STOPS and reports (FR-025): bringing the block forward edits the ratified
  delta, which FR-009 freezes, so it is the architect's ruling to make and not
  this feature's act.
- **FR-013**: Gate evidence MUST live in
  `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`
  as well as in this feature directory. The `evidence/` segment is excluded from
  doc-health's lifecycle scan set (`EVIDENCE_PARTS`), so that file owes no
  lifecycle header and cannot move gate 4.4's finding set; a `review/` record
  would owe one. (Q4 = b.)
- **FR-013a**: The evidence file MUST record, for every gate, the EXACT COMMAND
  TEXT as run — including the environment the run needed (`OPENSPEC_TELEMETRY=0`,
  the `PATH` carrying the pinned CLI) — the return code, the summary line, and the
  head. It MUST also record the pinned CLI's own version and the provenance the
  pin verifies. "Re-runnable from the evidence file alone" is the test, and a
  result without its command does not meet it.
- **FR-013b**: THE TWO EVIDENCE HOMES HAVE DIFFERENT JOBS, AND THE RELATIONSHIP IS
  STATED: the packet's `evidence/realization-2026-09-08.md` is AUTHORITATIVE — it
  is what the archive act reads — and the files under this feature's `evidence/`
  are the RAW CAPTURES it cites (full gate output, the two doc-health reports).
  The packet file names each capture by path; where the two would disagree the
  capture is right and the packet file is corrected under FR-021.
- **FR-013c**: THE EVIDENCE FILE'S OWN HEADER carries, before any result: the
  branch, the lane, the head it was opened at, and the three disclaimers — it is
  not a ruling, not a ratification, not a promotion — plus the statement that its
  results are LOCAL evidence rather than CI (FR-023) and that they record edits to
  an ACTIVE packet (FR-022).
- **FR-014** (origin: lane-collision protocol amendment 1, and this session's attribution rules): Every commit this feature AUTHORS MUST carry three trailers, by
  name — `Lane: opsXfactory-1`, `Co-Authored-By: Claude Fable 5.1
  <noreply@anthropic.com>`, and `Claude-Session: <session URL>` — and MUST stage
  explicit paths. The verification is `git log main..HEAD` read for the three keys
  (T031). A MERGE COMMIT taken from `main` is not an authored commit: it stages by
  merge rather than by pathspec, and that is stated here so the audit does not
  read a forward merge as a violation.
- **FR-015** (origin: this orchestrator's scope, and lane-protocol Rule 6): This feature MUST stop at a branch ready for the archive act. It
  MUST NOT run `openspec archive`, MUST NOT run `gh` in any form (no `gh pr
  create`, no `gh pr review`, no `gh api` write), MUST NOT post a GitHub comment,
  and MUST NOT merge. Claiming, the pull request, the LANDING/LANDED notices, the
  claim discharge and the archive act are the lane's. The comment prohibition
  reaches EVERY GitHub surface in EVERY repository — issues, pull requests,
  reviews, discussions — by any means, API or CLI; and this feature does not route
  a prohibited act around itself by asking another agent, session or person to
  perform one on its behalf.
- **FR-016**: This feature MUST write no checker, edit no pin, and repair no
  broken pin — the packet's own § *What This Change Does NOT Do*. That is not a
  refusal to enforce the rule: the ratified requirement's refusal scenarios are
  discharged by gates that already run or are proposed elsewhere (design D-6), and
  a checker built here would state only what its own shape could see.
- **FR-017**: The three ratified `tasks.md` sentences that hold the boxes
  unticked — the preamble "EVERY BOX IS UNTICKED, AND THAT IS THE STATE OF THE
  PACKET", § 0.1's "THE BOX STAYS UNTICKED", and § 1's "AND THE BOXES BELOW STAY
  UNTICKED" — MUST be amended in the SAME COMMIT that ticks the boxes, each
  amendment NAMING the superseded sentence and the reason, on the precedent of
  commit `3b530009` ("Name the superseded sentence in the archive-time header
  amendment"). The ratification record's "28 boxes, NONE ticked" baseline is a
  historical fact about the ratified head and MUST NOT be touched.
- **FR-017a**: THE AMENDMENT FORM IS FIXED. Every superseding amendment MUST
  BLOCK-QUOTE the sentence it supersedes, MUST NAME the neighbouring clause that
  is NOT superseded, and MUST carry its date and this change id. Nothing is
  rewritten in place. The passages it reaches are measured, not guessed:
  `tasks.md` line 7 (the preamble), line 58 with the paragraph at lines 58–66,
  line 70 (§ 1's "GIVEN 2026-09-08, AND THE BOXES BELOW STAY UNTICKED"), the
  § 1 clause at line 73 ("The heading is left as written because it names what
  the section was raised to hold"), and the re-assertion at lines 74–78.
  (Panel P4.)
- **FR-017b**: TWO HEADINGS ARE AMENDED, each with a WHOLE-TOKEN marker rather
  than a bare parenthetical, and each amendment NAMES the ratified clause it
  supersedes: § 1 "Ratification — OWED, NOT GIVEN" (line 68), whose own text says
  the heading is left as written, and § 3 "Composition — named here; 3.4 alone is
  this packet's own act" (line 161), which stops being true when 3.1 is ticked.
  (Mirror rulings M-A7 and M-A3; § 1's amendment is VETO POINT 5.)
- **FR-017c**: STALE IN-RECORD TEXT THAT WAS TRUE WHEN WRITTEN is corrected by a
  dated CORRECTED block that QUOTES the stale words — never rewritten in place.
  The measured instance is § 0.1's PERFORMED note, which says "this packet is
  `Status: draft` awaiting ratification at task 1.1" (line 60) and was true when
  written. (Mirror ruling M-A6.)
- **FR-018** (origin: architect answer Q5, the mirror-floor discipline): A box MUST be ticked in the same commit that records its evidence,
  or neither happens — a tick landing ahead of its evidence is the failure this
  packet exists to refuse. The rule is NOT a biconditional: evidence MAY be
  recorded without a tick, and box 4.2 is exactly that case (FR-012). What is
  forbidden is the tick without the evidence.
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
- **FR-024**: EVERY OpenSpec CLI invocation MUST go through
  `scripts/validate-openspec-cli-pin.py` with the pinned `@fission-ai/openspec@1.12.0`
  on `PATH`. PATH's 1.2.0 MUST NOT be used for validation, archiving, or any
  reading whose result is recorded. This is a MUST, not a convention: the pin is
  the whole of the claim about which tool validated this corpus.
- **FR-024a**: EVERY § 4 GATE IS EXPECTED TO BE IDEMPOTENT AT A FIXED HEAD: run
  twice over the same commit with the same inputs, each MUST report the same
  result. Where one does not, the non-determinism IS the finding — recorded and
  reported (FR-025), never averaged away by re-running until green.
- **FR-025**: STOP-AND-REPORT. Where a precondition measurement returns other than
  expected — the packet or canon moved (T002), a gate CANNOT be run at all
  (missing dependency, unavailable checkout), `main` moved under a comparison, or
  a cross-citation does not resolve — the branch STOPS, records the measurement,
  and reports at STOP (B). A gate that cannot be RUN is a different fact from a
  gate that FAILED, and the evidence file MUST distinguish them by name. The
  trigger list includes a CONFLICT DISCOVERED between this feature's artifacts and
  the ratified packet: the packet governs, this feature's text is the defect, and
  resolving it is a ruling rather than an edit made in passing. A stop is a STOP,
  not an abandonment: committed work stays, the evidence file records the stop and
  its measurement, and the branch RESUMES from the same head when the ruling
  arrives — it does not restart.
- **FR-026**: NOTE CLASSES, AND THEY SUM TO 28. Every box in the packet's
  `tasks.md` MUST carry exactly one of three classes: **ticked-with-evidence**
  (the act is done here or is done and cited), **NOT-OWED** (another repository,
  another packet, or the lane owes it), or **RUN-RECORDED-LEFT-OPEN** (the check
  was run and recorded and the box is deliberately open — box 4.2 alone today).
  The CLASS is not the note: every note also carries FR-006b's three things.
  The three counts MUST sum to 28, and the evidence file MUST state the three
  numbers. "NOT OWED HERE" and "NOT-OWED-YET" are the same class with different
  reasons — permanently another's, versus not yet due — and each note says which.
- **FR-027**: NO INVENTED QUOTATION ANYWHERE. The rule reaches every note this
  feature writes, not only the § 1 ratification notes: a note may restate what a
  record states and may never attribute words to a person. An invented quotation
  is a BLOCKING DEFECT — the commit does not land, and if one is discovered after
  landing it is corrected under FR-021 with the invented words quoted in the
  correction.
- **FR-028**: THE DOC-HEALTH COMPARISON IS IDENTITY-SAFE. The baseline checkout
  MUST carry the SAME directory basename as the branch checkout, or the comparison
  MUST normalize all three places the basename is stamped (`repo=<basename>` on
  every finding line, the `Repo-Identity:` header, the "scope limited to single
  repo" line). The comparison MUST be keyed on (family, repository, path, message)
  rather than on line numbers — a finding that moved down the file is the same
  finding. The recipe MUST be PROVEN main-vs-main before it is trusted:
  two runs over the same commit in the two directories, expected zero differences.
  `--previous-report` MUST NOT be used; it refuses on identity mismatch by design.
  (Panel P1.)
- **FR-029**: BASELINE AUTHORITY. The doc-health baseline MUST name the `main`
  COMMIT SHA it was taken at. If `main` moves between the baseline and the final
  comparison, the baseline is RE-TAKEN at the commit the branch was last merged
  from, and the evidence records both shas — a comparison against a moved baseline
  is not a comparison.
- **FR-030**: TRAILER REMEDIATION WITHOUT REWRITING. A commit that lands missing a
  trailer is NOT rewritten (FR-021 forbids it). The omission is recorded in the
  evidence file and the next commit carries a dated line naming the commit and the
  missing trailer.
- **FR-031**: THE VETO POINTS NAME THEIR REQUIREMENTS. Each ruling open to Brett
  Heap's veto MUST name the FR(s) it produced, so exercising a veto identifies
  exactly what is reverted.
- **FR-032**: EVERY CROSS-REPOSITORY CLAIM NAMES WHEN IT WAS CHECKED. A statement
  about another repository's state — the twin's landing, another packet's tick
  count, a register that does not exist — carries the head or sha and the UTC date
  at which it was measured. A claim without one is not made, because the other
  repository moves under this branch and an undated claim silently becomes false.
  This reaches task 3.3's citation of `add-consent-custody-rederivation-record`
  (merged `543d47a9`, 46 boxes unticked as measured 2026-09-08) as much as the
  twin's.
- **FR-033**: AFTER THE ARCHIVE ACT, THE SAME EDITS WOULD TAKE THE ARCHIVED-RECORD
  ROUTE. FR-022's exemption is a statement about TODAY: once the packet sits under
  `openspec/changes/archive/`, an edit to any of these same files needs a ruling
  recorded before it, the neutral minimum note, and the bookkeeping class — which
  is the whole reason realization happens before the archive rather than after.
- **FR-034**: THE ARCHIVE ACT'S OWN CHECKS ARE THE LANE'S, AND THE HANDOFF IS
  NAMED. If the archive act re-runs the pinned-target measurement or the
  MODIFIED-block currency check and finds this feature's result stale, that is the
  ARCHIVE ACT's finding to record and correct; this feature's obligation is that
  its results carry the head they were taken at (FR-008a, FR-032), so staleness is
  detectable rather than invisible.
- **FR-035**: CROSS-BOUNDARY PINS, AND THE WORD "INSTRUMENT". The ratified
  scenario *A dependent pin lives in another repository* obliges an editing change
  to record the owed consumer re-pin by NAME, REPOSITORY and INSTRUMENT — where an
  INSTRUMENT is the named artifact that holds the pin (a consent instrument, an
  evidence manifest, a digest inventory, a contract release's digest file). This
  feature's measurement is IN-REPO by ruling (1.2a) and asserts nothing about
  consuming repositories; were a consumer pin naming one of these files ever
  found, the owed act would be recorded in those three terms and performed in that
  repository's own change.
- **FR-036**: A LATER DISCOVERY IS A FORWARD CORRECTION. If a file this feature
  edited is later found to have been a pinned target after all, the correction is
  a NEW change recording the owed re-derivation — never a rewrite of this branch's
  history and never a re-run of its measurement under a different answer.
- **FR-037**: PRE-EXISTING FAILURES ARE NAMED AS SUCH. A gate finding also present
  on `main` at the comparison head is PRE-EXISTING: it is recorded with the
  evidence that it predates this branch, is never attributed to this feature's
  diff, and is not cleared here — most such findings live in files FR-009a freezes.
- **FR-038**: THE STOP CONDITION HAS ONE NORMATIVE HOME. FR-015 states it; the
  Primary flow, the Assumptions, the Out-of-scope list and `tasks.md` T034 POINT
  AT IT and add nothing. Where they appear to differ, FR-015 governs and the other
  text is the defect.
- **FR-039**: THE CLAIM IS THE LANE'S AND IT COVERS THIS AUTHORING. "Claim before
  author" targets the governing issue — openxFactory #630, claimed by the lane
  before this branch existed — not the working tree, so authoring inside a
  dedicated clone under that claim is what it authorizes. If another lane posts a
  LANDING notice touching #630 or a shared substrate while this branch is open,
  this feature does nothing: it holds no landing of its own, and the lane decides
  the order.
- **FR-040**: TYPOGRAPHY AND WHITESPACE OF THE ADOPTED TEXT. LF line endings, no
  trailing whitespace, and the quoted note form is never reflowed or line-broken —
  a wrapped quotation of a byte-exact form is no longer byte-exact. Quoting a
  FRAGMENT of a ratified sentence is permitted only where the omission cannot
  change its meaning; where it could, the whole sentence is quoted.

### Key Entities

- **The ratified packet** — `openspec/changes/govern-archived-record-edits/`:
  five files, 28 boxes, one MODIFIED and two ADDED requirements, 18 scenarios.
  Its `tasks.md` is the only member this feature expects to write.
- **The lifecycle document** — `docs/document-lifecycle.md`, `Status: standard`,
  backed by the promoted `document-lifecycle` spec. The § 3.4 target.
- **The sweep-ledger row** — `tests/sequenced_after/corpus-ledger.yaml:214`.
  Already correct; read, never rewritten.
- **The README Records row** — `README.md:659`, whose body asserts "all 28 boxes
  in `tasks.md` stay unticked" (line 671). The row itself stays; ONE dated
  superseding sentence is appended at its END (FR-010c).
- **The twin** — OpsxFactory's `govern-archived-record-edits`, LANDED on that
  repository's `main` as `bbbef015cd394e2de31586b9718356586c413884` (PR #279,
  2026-09-08T15:28:23Z).
- **Glossary, because three terms carry weight**: "the lane" is `opsXfactory-1`,
  the main session that claims, opens the PR, lands and archives; "the feature" is
  this branch and its acts; "STOP (B)" is the arrangement's second mandatory stop —
  after the analyze loop first reads clean, before implementation — at which this
  orchestrator ends its turn with a report and waits. "The archive act" is the
  later, separate act that runs `openspec archive` and promotes the delta into
  `openspec/specs/document-lifecycle/spec.md`; "a sibling orchestrator" is the
  agent realizing the OpsxFactory twin, which shares the lane and the rulings and
  writes in the other repository. **THE AGENT/OPERATOR BOUNDARY, stated once**: an
  agent authors prose, runs gates, records evidence, and ticks boxes whose act is
  DONE and independently recorded; only Brett Heap rules, ratifies, vetoes and
  gives the archive word; only the lane claims, opens the PR, comments, merges and
  archives.
- **The gate set** — the pinned CLI entrypoint (4.1), the § 4.2 MODIFIED-block
  currency measurement (run and recorded, box left open), the sequenced-after
  validators, scope globs and manifest digests (4.3), doc-health (4.4), and the
  three pytest paths (4.5).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader of `docs/document-lifecycle.md` alone can state the
  bookkeeping note's exact form and where it goes. The check is the FULL LINE
  FORM, not substring presence: the document contains
  `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>` byte-for-byte
  as the ratified requirement states it, em dash and placeholders included, and
  the citation is the last clause of the bullet's parent prose.
- **SC-002**: `validate-openspec-cli-pin.py --change govern-archived-record-edits
  --strict` passes and `--all --strict` reports ZERO undispositioned findings at
  the final head, with the dispositioned-exception COUNT stated as a number and
  compared with the ratified baseline's (99 passed / 2 failed, 0 undispositioned).
  A count that moved in EITHER direction is explained; a lower count is a
  difference too, not a bonus. Dispositions live in
  `contracts/openspec-cli-pin.yaml`'s `dispositions:` list, each carrying its
  citation — and `contracts/**` is frozen here (FR-009a), so a NEW undispositioned
  finding is a BLOCKER this feature cannot clear itself: it stops and reports.
- **SC-003**: The doc-health finding set at the final head is diff-identical to
  `main`'s.
- **SC-004**: `validate-sequenced-after.py .` and `--ledger-diff`,
  `validate-scope-globs.py .` and `validate-manifest-digests.py .` all exit 0.
- **SC-005**: `pytest tests/sequenced_after tests/proposal-support
  tests/scope_globs -q` is green, with the `Ran N tests` line captured to a file
  rather than inferred from a pipeline's exit code.
- **SC-006**: Every one of the 28 boxes in `tasks.md` carries exactly one FR-026
  note class, the three class counts SUM TO 28, no box is left in the
  pre-realization state, and every § 4 note CITES the evidence file rather than
  restating a result.
- **SC-007** (three-dot: the comparison runs against the MERGE BASE, so a forward
  merge moves the base and the check is re-run after one): `git diff main...HEAD
  --stat` shows changes ONLY under
  `specs/032-govern-archived-record-edits/`, `docs/document-lifecycle.md`,
  `openspec/changes/govern-archived-record-edits/tasks.md`,
  `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`,
  `openspec/changes/govern-archived-record-edits/proposal.md` and `README.md`
  (the one appended row sentence, FR-010c) — and nothing under any `archive/`
  path, nothing in `design.md`, `.openspec.yaml` or the spec delta.
- **SC-008**: The MODIFIED block's currency against promoted canon is recorded
  with a number (canon bytes carried, canon lines removed) at the final head.
- **SC-009**: Every superseding amendment this branch writes carries a BLOCK QUOTE
  of the superseded sentence and names the neighbouring clause that is not
  superseded — counted: the `tasks.md` passages FR-017a names, the two headings
  FR-017b names, the `proposal.md` sentences FR-010b names, and the README row
  sentence FR-010c names.
- **SC-010**: The cross-citations between this packet and the OpsxFactory twin
  RESOLVE on both `main` lines, checked at named heads and recorded with the twin's
  merge sha `bbbef015cd394e2de31586b9718356586c413884`.

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
