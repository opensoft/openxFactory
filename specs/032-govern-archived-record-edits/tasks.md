# Tasks: 032-govern-archived-record-edits

**Input**: `spec.md`, `plan.md`, `research.md`, `quickstart.md` in this directory

**Prerequisites**: the ratified packet at `openspec/changes/govern-archived-record-edits/`
(openxFactory `main` `3504287a`, PR #788), branch base `main` `68712924`.

**Tests**: this feature has no code, so its tests ARE the repository's gates —
Phase 5. They are mandatory, not optional (constitution Principle V).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: may run in parallel (different files, no dependency)
- **[Story]**: US1 (the doc adoption), US2 (the truthful task record), US3 (the
  evidence the archive act reads)

## Path conventions

Repository root is the openxFactory checkout. `PIN` is the pinned CLI prefix.
Two files named `tasks.md` are in play: THIS one (the feature's) and the
PACKET's at `openspec/changes/govern-archived-record-edits/tasks.md`. Every task
below names its path in full.

---

## Phase 1: Setup

- [x] T001 Confirm the working tree: branch `032-govern-archived-record-edits`,
      clean status, base `main` `68712924`, and the dedicated clone (never
      `~/projects/xFactory/...`). Confirm the LANE IDENTITY too — this work is
      lane `opsXfactory-1`'s, the trailers say so, and a commit authored under
      another lane's name would misattribute the act. Record the head and the
      lane in the evidence file's header.
      **Done 2026-09-08** — head `aafdbf01f276a0a2bd1e4b3051f321a6d32fa694`, branch
      `032-govern-archived-record-edits`, `git status --porcelain` empty, base `main`
      `68712924` (also the merge-base with `origin/main`), clone
      `<scratchpad>/oxf-realize-f3`, never a shared checkout. LANE IDENTITY: this work is
      lane `opsXfactory-1`'s and every commit carries the `Lane: opsXfactory-1` trailer.
      MEASURED AND REPORTED, NOT ACTED ON: `origin/main` has moved to `6cc06288` since the
      branch was cut; no merge is taken here (no task asks for one), so `main` `68712924`
      remains the comparand for SC-007 and for the doc-health baseline. Carried into the
      evidence file header at T011.

- [x] T002 Re-take M1 at the current head: `git log --oneline 3504287a..HEAD --
      openspec/changes/govern-archived-record-edits openspec/specs/document-lifecycle
      docs/document-lifecycle.md`. If it is NOT empty, STOP and report — the
      MODIFIED block or the § 3.4 target moved and the plan's premises need
      re-reading.
      **Done 2026-09-08** — `git log --oneline 3504287a..HEAD -- openspec/changes/govern-archived-record-edits
      openspec/specs/document-lifecycle docs/document-lifecycle.md` printed NOTHING, and
      `git merge-base --is-ancestor 3504287a HEAD` succeeded. The MODIFIED block and the
      § 3.4 target have not moved since ratification; the plan's premises hold. Re-taken at
      the final head by T029.


---

## Phase 2: Foundational (blocking)

**⚠️ Nothing in Phase 3+ may start until these hold.**

- [x] T003 Verify the frozen set is untouched and stays so. The set is
      enumerated ONCE, in `spec.md` FR-009a, and is NOT re-listed here — the one
      thing worth repeating is its exception: `README.md` is frozen EXCEPT the
      single sentence T028a appends to this change's own Records row. This is a
      standing constraint, re-checked at T030 (the SC-007 path-set check), not a
      one-time act.
      **Standing constraint, verified at this commit 2026-09-08** — `git diff main...HEAD
      --name-only` names nothing under `openspec/changes/archive/`, nothing in the packet's
      `design.md`, `.openspec.yaml` or `specs/document-lifecycle/spec.md`, nothing in
      `tests/`, `contracts/`, `scripts/` or `.github/`, and no part of `README.md`. Re-checked
      at T030 as the SC-007 path-set check.

- [x] T004 [P] Capture the doc-health BASELINE from `main` before any edit, into
      the feature's `evidence/` directory, so the 4.4 diff has a fixed comparand
      rather than a re-derived one, and NAME the `main` sha it was taken at
      (FR-029). The baseline checkout MUST carry the SAME directory basename as
      this one — doc-health stamps the basename into `repo=<basename>` on every
      finding line, into the `Repo-Identity:` header and into the "scope limited
      to single repo" line — so check `main` out at
      `<scratchpad>/dh-base/oxf-realize-f3`. PROVE the recipe main-vs-main first:
      two runs over the SAME commit in the two directories must differ in ZERO
      finding lines. Only then is a branch-vs-main diff evidence of anything.
      (FR-028, panel P1)
      **Done 2026-09-08** — baseline taken at `main` **`68712924732849fd146c3a1969b79879b44fae7c`**
      (FR-029), the commit this branch was cut from and has not merged past. Two checkouts of
      that same sha, BOTH named `oxf-realize-f3`, at `<scratchpad>/dh-base/oxf-realize-f3` and
      `<scratchpad>/dh-proof/oxf-realize-f3`. RECIPE PROVEN MAIN-VS-MAIN FIRST: `diff` of the
      two reports returned ZERO differences (rc 0), so the basename stamp is neutralised and a
      branch-vs-main diff is evidence. Reports: `evidence/doc-health-main-68712924-A.md`
      (the baseline T016 diffs against) and `evidence/doc-health-main-68712924-B.md` (the
      proof twin); both runs exited rc 1 on PRE-EXISTING error-level findings that predate this
      branch (FR-037). Headline at baseline: 10 critical, 9 error, 55 warning, 16 info.


---

## Phase 3: User Story 1 — the doc adoption (Priority: P1) 🎯 MVP

**Goal**: `docs/document-lifecycle.md` states the neutral bookkeeping-note
minimum, so the repository promoting the rule stops being the one repository
with no note obligation written down.

**Independent test**: read that document alone and recover the note's exact
form, its placement, and the change that ratified it.

- [x] T005 [US1] Write ONE top-level bullet at the END of § *Status Claim Rules*
      in `docs/document-lifecycle.md` (after the byte-exact-evidence bullet),
      with sub-bullets, in the `govern-openspec-corpus-membership` bullet's
      shape. The bullet is BODY PROSE in that section — it is NOT placed in this
      document's own lifecycle-header block, and nothing is inserted near the top
      of the file. (FR-004, FR-002)
      **Done 2026-09-08** — one top-level bullet appended at the END of § *Status Claim
      Rules*, immediately after the byte-exact-evidence sub-bullet, at
      `docs/document-lifecycle.md` line 138, with two sub-bullets, in the
      `govern-openspec-corpus-membership` bullet's shape. It is BODY PROSE: nothing was
      inserted near the top of the file and the document's own lifecycle-header block is
      untouched.

- [x] T006 [US1] In that bullet, quote the note form BYTE-EXACT from the ratified
      requirement: `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>`,
      em dash and placeholders included, and say it belongs in the EDITED FILE'S
      OWN lifecycle-header block. (FR-001, FR-002)
      **Done 2026-09-08** — the form was EXTRACTED PROGRAMMATICALLY from line 122 of
      `openspec/changes/govern-archived-record-edits/specs/document-lifecycle/spec.md` rather
      than retyped, so the em dash (U+2014, bytes `e2 80 94`) and the placeholder spellings are
      the ratified bytes. It sits on ONE line, unreflowed (FR-040), as a code span (FR-005a),
      with the sentence's period OUTSIDE the closing backtick. The bullet says the line belongs
      in the EDITED FILE'S OWN lifecycle-header block.

- [x] T007 [US1] Add exactly TWO explanatory sentences — the ruling is recorded
      BEFORE the edit; the note records WHAT changed and never THAT IT MAY —
      written as explanation, not as requirement text. No third sentence of
      route. (FR-005)
      **Done 2026-09-08** — exactly two explanatory sentences: "The ruling authorizing the
      class of edit is recorded BEFORE the edit." and "The note records WHAT changed and never
      THAT IT MAY, so it is not the authorization for the edit." Plain prose, not requirement
      text, and no third sentence of route.

- [x] T008 [US1] Add the inline citation "Ratified by `govern-archived-record-edits`
      (2026-09-08)" in the precedent form (no colon after the change name), and
      put "reaches promoted canon at the archive act" in a FOLLOWING sentence,
      never inside the citation clause. (FR-003)
      **Done 2026-09-08** — the bullet's parent prose ENDS "Ratified by
      `govern-archived-record-edits` (2026-09-08)." — the precedent form, no colon after the
      change name, the last clause before the sub-bullets. The archive-act statement sits in
      the PRECEDING sentence ("the requirement reaches promoted canon at the archive act, and
      this document does not assert that canon carries it today"), never inside or after the
      citation clause.

- [x] T009 [US1] Verify locally before committing: the bullet sits below line 15
      (outside the status-header scan window), the document's own `Status:
      standard` header is untouched, and the added text states no rule the
      ratified requirement does not carry.
      **Done 2026-09-08** — verified before committing: the bullet begins at line 138, far
      below the 15-real-line status-header scan window; `Status: standard` and the rest of the
      header block are byte-identical (`git diff` shows +18 lines and no deletion); no trailing
      whitespace and no CR anywhere in the file; and every clause traces to the ratified
      requirement — the neutral minimum and its form, the recorded-ruling precedence, the
      note-is-not-the-authorization reading, the stricter-may-not-absent rule, and the reason
      the note sits in the lifecycle header. PRE-CHECK (diagnostic, not the gate): doc-health
      over the working tree against the T004 baseline moved ZERO finding lines; the only
      differences were the canon/governance word totals and the `standard` stage word count,
      each +199 because the document grew.

- [x] T010 [US1] Commit S1 with explicit paths and the three trailers. Before
      EVERY commit on this branch, read `git diff --cached --stat` and confirm no
      foreign path is staged — the clone is this feature's alone, and the check
      costs nothing.
      **Done 2026-09-08** — `git diff --cached --stat` was read before committing and named
      no foreign path: `docs/document-lifecycle.md`, the four T004 baseline captures under
      `specs/032-govern-archived-record-edits/evidence/`, and this file. The three trailers
      (`Lane: opsXfactory-1`, `Co-Authored-By: Claude Fable 5.1`, `Claude-Session:`) are on
      this commit.


**Checkpoint**: US1 is independently landable — the packet's § 6.1 gate reads
box 3.4, and this is the act behind it.

---

## Phase 4: User Story 3 — the evidence (Priority: P3, sequenced before US2)

**Goal**: every § 4 gate result and both measurements are captured at a named
head, because US2's ticks may not land ahead of the evidence they cite (FR-018).

**Independent test**: from the evidence file alone, re-run each command and
reproduce each result.

- [ ] T011 [US3] Create `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`
      with a header naming the head, the branch, the lane and what the file is
      NOT: not a ruling, not a ratification, not a promotion; LOCAL evidence at a
      named head rather than a CI result (FR-023); and a record of edits to an
      ACTIVE packet, which the ratified archived-record requirement does not yet
      bind (FR-022). (FR-013, FR-022, FR-023)
- [ ] T012 [US3] Take the pinned-target measurement at this head and record it,
      worded exactly: no IN-REPO `sha256` pin names `docs/document-lifecycle.md`,
      measured at base `68712924`; the only pairings are illustrative fixtures
      under `examples/document-cataloging/`. (FR-008)
- [ ] T013 [US3] Take the MODIFIED-block currency measurement at this head
      (canon characters, delta characters, canon lines removed) and record it as
      a measurement with its command. (FR-012, task 4.2 — measured, NOT ticked)
- [ ] T012a [US3] Re-check the CROSS-CITATIONS on BOTH `main` lines — this
      packet's citations of the twin and the twin's citations of this packet —
      from a read-only clone of OpsxFactory, and record: the two heads, each
      citation, whether it resolves, and the twin's merge sha
      `bbbef015cd394e2de31586b9718356586c413884`. A citation that does not
      resolve STOPS the branch (FR-025), it is not a note. (FR-007a, SC-010)
- [ ] T012b [US3] CONTINGENCY, and it is a task rather than a hope: if T012's
      measurement finds a pin naming any file this feature edits, or a candidate
      pin that cannot be resolved, STOP — record the finding, do not tick, do not
      land the edit, and report at STOP (B). (FR-008c, FR-025)
- [ ] T014 [US3] Run task 4.1's two pinned-CLI gates THROUGH
      `scripts/validate-openspec-cli-pin.py` with the pinned 1.12.0 on `PATH`
      (never PATH's 1.2.0), capture rc and the summary lines to files under the
      feature's `evidence/`, and record in the packet evidence file: the EXACT
      command text with its environment, the counts, and the pinned CLI's version
      and verified provenance. Compare the dispositioned-exception count in BOTH
      DIRECTIONS against the ratification record's baseline (99 passed / 2 failed,
      0 undispositioned) and explain any movement either way.
      (FR-013a, FR-024, SC-002, panel P7)
- [ ] T015 [US3] Run task 4.3's four validators, capture rc and summary lines,
      record them.
- [ ] T016 [US3] Run doc-health on the branch with `--report-out` and diff its
      FINDING SET against T004's `main` report, using the identity-safe recipe
      T004 proved: TWO INDEPENDENT RUNS from identically-named checkouts, or a
      normalization of all THREE stamped places (`repo=\S+`, the
      `Repo-Identity:` header, the "scope limited to single repo" line), plus the
      run date. NEVER `--previous-report` — it refuses on identity mismatch by
      design (`REFUSE previous-report-identity-mismatch`). Record the diff
      verbatim, including "empty" if it is empty, and state separately any COUNT
      that moved only because the document grew (word totals, canon share), which
      is not a finding. A non-empty finding-set diff is a BLOCKER (FR-020).
- [ ] T017 [US3] Run task 4.5's pytest paths, capture rc and the `N passed` line
      to a file, record them.
- [ ] T018 [US3] Commit S2+S3 (the evidence file and the captured outputs) with
      explicit paths and the three trailers.

**Checkpoint**: every claim US2 will tick against is now recorded at a named head.

---

## Phase 5: User Story 2 — the truthful task record (Priority: P2)

**Goal**: `openspec/changes/govern-archived-record-edits/tasks.md` says, box by
box, what was done, by whom, and what is owed elsewhere.

**Independent test**: read that file alone and name the responsible repository
and actor for each of the 28 boxes.

- [ ] T019 [US2] Amend, in the packet's `tasks.md` and in commit `3b530009`'s
      FORM — a BLOCK QUOTE of the superseded sentence plus the neighbouring clause
      NAMED as not superseded, dated and attributed to this change: the preamble
      (line 7), § 0.1's "THE BOX STAYS UNTICKED" paragraph (lines 58–66), § 1's
      "GIVEN 2026-09-08, AND THE BOXES BELOW STAY UNTICKED" (line 70) and its
      re-assertion (lines 74–78). Same commit as the ticks. (FR-017, FR-017a)
- [ ] T019a [US2] Amend the TWO HEADINGS with whole-token markers, each naming the
      ratified clause it supersedes: § 1 "Ratification — OWED, NOT GIVEN" (line
      68), whose own line 73 says the heading is left as written on purpose, and
      § 3 "Composition — named here; 3.4 alone is this packet's own act" (line
      161), which 3.1's tick falsifies. (FR-017b; veto point 5)
- [ ] T019b [US2] Write the dated CORRECTED block for § 0.1's PERFORMED note,
      QUOTING its stale words "this packet is `Status: draft` awaiting
      ratification at task 1.1" (line 60) — true when written, false now — and
      never rewriting them in place. (FR-017c)
- [ ] T020 [US2] Tick § 0.1 with a dated note: the row on `main` reads
      `moved_by: "#788"` (`corpus-ledger.yaml:214`); the file is not rewritten
      here.
- [ ] T021 [US2] Tick § 1.1–1.5 with dated notes citing the record as the record
      does — GitHub review `5141756427`, APPROVED `2026-09-08T12:38:36Z`, record
      `review/ratification-2026-09-08.md` — and NO quotation: the approval body
      is empty. 1.2a/1.2b/1.2c note that the veto was not exercised and the
      default stands; 1.3 and 1.4 note the same. (FR-006)
- [ ] T022 [US2] Tick § 2.1–2.3 with dated notes naming the ratified baseline
      `8cc76e1b` and the delta's shape (1 MODIFIED + 2 ADDED, 18 scenarios).
- [ ] T023 [US2] Tick § 3.4 with a dated note naming the doc commit and the
      bullet's location. TICK § 3.1 TOO, on T012a's performed cross-citation
      check: the twin LANDED as OpsxFactory `main`
      `bbbef015cd394e2de31586b9718356586c413884` (PR #279, 2026-09-08T15:28:23Z),
      and the note cites the sha, the two heads checked, and the evidence file.
      Leave § 3.2, 3.3 and 3.5 UNTICKED, each with ONE dated NOT-OWED line — 3.3
      naming `add-consent-custody-rederivation-record` (merged `543d47a9`, 46
      boxes unticked). (FR-007, FR-007a, panel P2)
- [ ] T024 [US2] Tick § 4.1, 4.3, 4.4, 4.5 with dated notes citing the evidence
      file's recorded results; leave § 4.2 UNTICKED with a dated note saying the
      measurement was taken and the box is deliberately open for the archive
      act. (FR-012)
- [ ] T025 [US2] Add the § 4 pinned-target note (FR-008 wording) beside the § 4
      boxes.
- [ ] T026 [US2] Tick § 5.1 (README row on `main` since #788); leave § 5.2 and
      5.3 UNTICKED with dated NOT-OWED lines naming the lane; leave § 6.1, 6.2
      and 6.3 UNTICKED with dated lines naming the archive act and, for 6.1, the
      fact that its gating box 3.4 is now ticked.
- [ ] T026a [US2] AUDIT THE NOTE CLASSES before committing: every one of the 28
      boxes carries exactly one of ticked-with-evidence / NOT-OWED /
      RUN-RECORDED-LEFT-OPEN, the three counts SUM TO 28, and every § 4 note cites
      the evidence file rather than restating a result. Record the three numbers.
      (FR-026, SC-006)
- [ ] T027 [US2] Commit T019–T026a as ONE commit — ticks and their notes together,
      never a tick ahead of its evidence; evidence without a tick is permitted and
      box 4.2 is that case. (FR-018)
- [ ] T028 [US2] Add the ONE additive dated realization note to the packet's
      `proposal.md`, placed immediately AFTER the `Lane: opsXfactory-1` line and
      NOWHERE ABOVE `Status:`, recording that realization adds the evidence file
      and the `docs/document-lifecycle.md` edit task 3.4 names, and QUOTING the
      front-matter enumeration sentence it corrects rather than rewriting it. The
      YAML front matter and the `code_surface:` value stay byte-identical —
      measured reason: `Status: ratified` sits at real-line index 8 of a 15-line
      header window and the folded `code_surface` scalar counts as ONE real line,
      so an insertion above `Status:` moves the header toward the window's edge.
      Commit separately with the superseded-enumeration reason stated. The note
      MUST also quote the two sentences at lines 17 and 44 that assert every box
      stays unticked. (FR-010, FR-010a, FR-010b, panel P5)
- [ ] T028a Append ONE dated superseding sentence at the END of this change's
      README "OpenSpec Records" row, which asserts "all 28 boxes in `tasks.md`
      stay unticked" (README.md line 527). At the row's END, never near the block
      anchor, so a concurrent lane's row edit collides on a different line.
      (FR-010c; veto point 4; mirror ruling M-A1)

**Checkpoint**: the packet reads truthfully and the branch is archive-ready.

---

## Phase 6: Gates and polish

- [ ] T029 Re-run the FULL § 4 gate set at the final head (T027/T028 touched
      `openspec/changes/**`, which the pinned CLI scans) and update the evidence
      file with the final-head results, marking clearly which results are
      final-head and which were interim. A superseded interim result is STRUCK
      with a dated line naming the head that replaced it, never deleted. (FR-021)
      IF ANY GATE FAILS AT THE FINAL HEAD, the tick it supported is STRUCK — a
      dated line in `tasks.md` saying the gate that supported it failed at this
      head — never deleted and never quietly left standing. (FR-020, panel P3)
      A veto exercised after this run re-opens it for the paths it touches.
      RE-TAKE at this head, because a forward merge can move either: the
      pinned-target measurement (FR-008a) and the ancestry check of T002. Record
      both results beside their earlier ones rather than over them.
- [ ] T030 [P] Verify SC-007: `git diff main...HEAD --name-only` contains only
      the SIX allowed paths — the feature directory, `docs/document-lifecycle.md`,
      the packet's `tasks.md`, its new `evidence/` file, its `proposal.md`, and
      `README.md` — and nothing under any `archive/` path, nothing in `design.md`,
      `.openspec.yaml` or the spec delta.
- [ ] T030a [P] Verify SC-001 as the FULL LINE FORM, and WORD-DIFF the two
      explanatory sentences against FR-005's wording so a paraphrase cannot drift
      in unnoticed: the document contains
      `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>`
      byte-for-byte, em dash and placeholders included, and the citation is the
      last clause of the bullet's parent prose. Substring presence is not the
      check. (Panel P8)
- [ ] T030b [P] Verify SC-009: every superseding amendment carries a block quote
      and names the clause that is NOT superseded — counted across `tasks.md`,
      the two headings, `proposal.md` and the README row.
- [ ] T031 [P] Verify FR-014 on every AUTHORED commit: `git log main..HEAD`
      shows `Lane: opsXfactory-1`, `Co-Authored-By: Claude Fable 5.1` and
      `Claude-Session:` on each; a forward-merge commit is exempt and is named as
      such. VERIFY FR-018 POST HOC in the same pass: for every tick, the commit
      that added it also added or cited its evidence — no tick appears in a commit
      earlier than the evidence it rests on.
- [ ] T032 [P] Verify the three requirements no other task carries: FR-016 (no
      checker, workflow, pin or repair is authored — `git diff main...HEAD
      --name-only` names no file under `scripts/`, `.github/`, `contracts/` or
      `tests/`), FR-019 (the full Speckit tree is committed, `checklists/` and
      `analysis.md` included), and SC-006 (COUNT the packet's boxes: 28 total,
      each either `- [x]` with a dated note or `- [ ]` with a dated NOT-OWED
      line, no box left in its pre-realization state).
- [ ] T033 Commit the Speckit tree — `checklists/` and `analysis.md` — with
      explicit paths and the three trailers. (FR-019)
- [ ] T033a VERIFY THE STOP CONDITION AGAINST REPOSITORY STATE, not intention:
      no pull request exists for this branch that this feature opened, no comment
      was posted by it anywhere, no merge or `openspec archive` was run, and the
      working tree is clean. (FR-015, FR-038)
- [ ] T034 Copy the checklists' results and the final gate summary into the
      report for STOP (B), then STOP: no `gh`, no PR, no comment, no merge, no
      `openspec archive`. (FR-015)

---

## Failure handling (applies to every task)

A failing gate is a BLOCKER: the dependent task does not proceed, no box is
ticked against it, the output is recorded as produced, and the failure goes into
the STOP (B) report (FR-020). A defect found after a commit is repaired by a NEW
commit naming what it supersedes — never a force-push, never a rewritten history,
and a superseded evidence entry is struck with a dated line rather than deleted
(FR-021).

## Dependencies

- T001, T002 → everything.
- T004 (main baseline) → T016 (the diff needs a comparand taken before the edit).
- Phase 3 (US1) → Phase 4 (US3): the gates must run at a head that carries the
  doc edit.
- Phase 4 (US3) → Phase 5 (US2): FR-018 — a tick may not land ahead of its
  evidence.
- T027, T028, T028a → T029: the final gate run must cover the packet and README
  edits.
- T012a (the cross-citation check) → T023's tick of 3.1.
- T029 → T030, T030a, T030b, T031, T032 → T033 → T034.
- A forward merge from `main` taken after T029 re-opens T029 (FR-011).

## Parallel opportunities

- T004 runs alongside T005–T009 (different tree).
- T030, T031 and T032 run together after T029.
- Within Phase 5, T019–T026 are one file and are NOT parallel.

## Implementation strategy

MVP is US1 alone: the § 3.4 adoption is the box that holds the packet open.
US3 then makes the gates re-runnable, and US2 makes the record true. Stop at (B)
with the gate report; the lane claims, opens the PR, lands, and archives.

## Requirement → task map

Every requirement and success criterion in `spec.md`, and the task that carries
it. A requirement with no row would be a requirement nobody executes; a task
appearing in no row would be work nobody asked for.

| Requirement | Task(s) |
| --- | --- |
| FR-001 | T006 |
| FR-002 | T005, T006 |
| FR-003 | T008 |
| FR-004 | T005 |
| FR-005 | T007 |
| FR-005a | T007, T030a |
| FR-005b | T007, T009 |
| FR-006 | T020–T024, T026 (T022 is § 2's authoring boxes) |
| FR-006a | T020–T026 |
| FR-006b | T020–T026 |
| FR-007 | T023 |
| FR-007a | T012a, T023 |
| FR-007b | T023 |
| FR-008 | T012, T025 |
| FR-008a | T012, T029 |
| FR-008b | T012, T025 |
| FR-008c | T012b |
| FR-009 | T003, T030 |
| FR-009a | T003, T030 |
| FR-010 | T028 |
| FR-010a | T028 |
| FR-010b | T028 |
| FR-010c | T028a |
| FR-011 | T014–T017, T029 |
| FR-012 | T013, T024 |
| FR-013 | T011 |
| FR-013a | T014, T015, T017 |
| FR-013b | T011, T029 |
| FR-013c | T011 |
| FR-014 | T010, T018, T027, T031 |
| FR-015 | T033a, T034 |
| FR-016 | T032 |
| FR-017 | T019 |
| FR-017a | T019, T030b |
| FR-017b | T019a |
| FR-017c | T019b |
| FR-018 | T027, T031 |
| FR-019 | T032, T033 |
| FR-020 | T016, T029 |
| FR-021 | T029 |
| FR-022 | T011 |
| FR-023 | T011 |
| FR-024 | T014 |
| FR-024a | T029 |
| FR-025 | T002, T012b |
| FR-026 | T026a |
| FR-027 | T021, T026a |
| FR-028 | T004, T016 |
| FR-029 | T004, T016 |
| FR-030 | T031 |
| FR-031 | T034 |
| FR-032 | T012a, T023 |
| FR-033 | T011 |
| FR-034 | T029 |
| FR-035 | T012, T025 |
| FR-036 | T034 |
| FR-037 | T016, T029 |
| FR-038 | T033a, T034 |
| FR-039 | T001 |
| FR-040 | T006, T030a |
| SC-001 | T030a |
| SC-002 | T014 |
| SC-003 | T016 |
| SC-004 | T015 |
| SC-005 | T017 |
| SC-006 | T026a, T032 |
| SC-007 | T030 |
| SC-008 | T013 |
| SC-009 | T030b |
| SC-010 | T012a |
