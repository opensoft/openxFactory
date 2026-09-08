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

- [ ] T001 Confirm the working tree: branch `032-govern-archived-record-edits`,
      clean status, base `main` `68712924`, and the dedicated clone (never
      `~/projects/xFactory/...`). Record the head in the evidence file's header.
- [ ] T002 Re-take M1 at the current head: `git log --oneline 3504287a..HEAD --
      openspec/changes/govern-archived-record-edits openspec/specs/document-lifecycle
      docs/document-lifecycle.md`. If it is NOT empty, STOP and report — the
      MODIFIED block or the § 3.4 target moved and the plan's premises need
      re-reading.

---

## Phase 2: Foundational (blocking)

**⚠️ Nothing in Phase 3+ may start until these hold.**

- [ ] T003 Verify the frozen set is untouched and stays so:
      `openspec/changes/govern-archived-record-edits/design.md`,
      `.openspec.yaml`, `specs/document-lifecycle/spec.md`, everything under
      `openspec/changes/archive/`, `tests/sequenced_after/corpus-ledger.yaml`,
      `README.md`, `contracts/**`. This is a standing constraint, re-checked at
      T030 (the SC-007 path-set check), not a one-time act.
- [ ] T004 [P] Capture the doc-health BASELINE from `main` before any edit, to
      the feature's `evidence/` directory, so the 4.4 diff has a fixed
      comparand rather than a re-derived one.

---

## Phase 3: User Story 1 — the doc adoption (Priority: P1) 🎯 MVP

**Goal**: `docs/document-lifecycle.md` states the neutral bookkeeping-note
minimum, so the repository promoting the rule stops being the one repository
with no note obligation written down.

**Independent test**: read that document alone and recover the note's exact
form, its placement, and the change that ratified it.

- [ ] T005 [US1] Write ONE top-level bullet at the END of § *Status Claim Rules*
      in `docs/document-lifecycle.md` (after the byte-exact-evidence bullet),
      with sub-bullets, in the `govern-openspec-corpus-membership` bullet's
      shape. The bullet is BODY PROSE in that section — it is NOT placed in this
      document's own lifecycle-header block, and nothing is inserted near the top
      of the file. (FR-004, FR-002)
- [ ] T006 [US1] In that bullet, quote the note form BYTE-EXACT from the ratified
      requirement: `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>`,
      em dash and placeholders included, and say it belongs in the EDITED FILE'S
      OWN lifecycle-header block. (FR-001, FR-002)
- [ ] T007 [US1] Add exactly TWO explanatory sentences — the ruling is recorded
      BEFORE the edit; the note records WHAT changed and never THAT IT MAY —
      written as explanation, not as requirement text. No third sentence of
      route. (FR-005)
- [ ] T008 [US1] Add the inline citation "Ratified by `govern-archived-record-edits`
      (2026-09-08)" in the precedent form (no colon after the change name), and
      put "reaches promoted canon at the archive act" in a FOLLOWING sentence,
      never inside the citation clause. (FR-003)
- [ ] T009 [US1] Verify locally before committing: the bullet sits below line 15
      (outside the status-header scan window), the document's own `Status:
      standard` header is untouched, and the added text states no rule the
      ratified requirement does not carry.
- [ ] T010 [US1] Commit S1 with explicit paths and the three trailers.

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
- [ ] T014 [US3] Run task 4.1's two pinned-CLI gates, capture rc and the summary
      lines to files under the feature's `evidence/`, and record both in the
      packet evidence file with their counts.
- [ ] T015 [US3] Run task 4.3's four validators, capture rc and summary lines,
      record them.
- [ ] T016 [US3] Run doc-health on the branch with `--report-out`, and diff its
      FINDING SET against T004's `main` report. Use TWO INDEPENDENT RUNS plus a
      normalized textual diff, NOT `--previous-report`: that flag refuses on a
      repo-identity mismatch (`REFUSE previous-report-identity-mismatch`) because
      the stamped identity is the checkout's slug, and a `main` checkout with a
      different basename is a foreign identity by construction. Normalize away
      the repo-identity stamp and any run date before diffing. Record the diff
      verbatim — including "empty" if it is empty — and state separately any
      COUNT that moved only because the document grew (word totals, canon share),
      which is not a finding. A non-empty finding-set diff is a BLOCKER (FR-020).
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

- [ ] T019 [US2] Amend the THREE ratified "stays unticked" sentences in the
      packet's `tasks.md` — the preamble "EVERY BOX IS UNTICKED…", § 0.1's "THE
      BOX STAYS UNTICKED…", § 1's "AND THE BOXES BELOW STAY UNTICKED" — each
      amendment NAMING the superseded sentence and the reason, on commit
      `3b530009`'s precedent. Same commit as the ticks. (FR-017)
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
      bullet's location; leave § 3.1, 3.2, 3.3 and 3.5 UNTICKED, each with ONE
      dated NOT-OWED line — 3.1 naming OpsxFactory `govern-archived-record-edits`
      and PR #279 as the landing vehicle at this date and NO merge sha; 3.3
      naming `add-consent-custody-rederivation-record` (merged `543d47a9`, 46
      boxes unticked). (FR-007)
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
- [ ] T027 [US2] Commit T019–T026 as ONE commit — ticks and their notes together,
      never a tick ahead of its evidence. (FR-018)
- [ ] T028 [US2] Add the ONE additive dated realization note to the packet's
      `proposal.md`, placed immediately AFTER the `Lane: opsXfactory-1` line and
      NOWHERE ABOVE `Status:`, recording that realization adds the evidence file
      and the `docs/document-lifecycle.md` edit task 3.4 names, and QUOTING the
      front-matter enumeration sentence it corrects rather than rewriting it. The
      YAML front matter and the `code_surface:` value stay byte-identical —
      measured reason: `Status: ratified` sits at real-line index 8 of a 15-line
      header window and the folded `code_surface` scalar counts as ONE real line,
      so an insertion above `Status:` moves the header toward the window's edge.
      Commit separately with the superseded-enumeration reason stated.
      (FR-010, FR-010a)

**Checkpoint**: the packet reads truthfully and the branch is archive-ready.

---

## Phase 6: Gates and polish

- [ ] T029 Re-run the FULL § 4 gate set at the final head (T027/T028 touched
      `openspec/changes/**`, which the pinned CLI scans) and update the evidence
      file with the final-head results, marking clearly which results are
      final-head and which were interim. A superseded interim result is STRUCK
      with a dated line naming the head that replaced it, never deleted. (FR-021)
- [ ] T030 [P] Verify SC-007: `git diff main...HEAD --name-only` contains only
      the five allowed path prefixes and nothing under any `archive/` path.
- [ ] T031 [P] Verify FR-014 on every commit: `git log main..HEAD --format='%h %(trailers:key=Lane)'`
      shows `Lane: opsXfactory-1` on each, with the Co-Authored-By and
      Claude-Session trailers present.
- [ ] T032 [P] Verify the three requirements no other task carries: FR-016 (no
      checker, workflow, pin or repair is authored — `git diff main...HEAD
      --name-only` names no file under `scripts/`, `.github/`, `contracts/` or
      `tests/`), FR-019 (the full Speckit tree is committed, `checklists/` and
      `analysis.md` included), and SC-006 (COUNT the packet's boxes: 28 total,
      each either `- [x]` with a dated note or `- [ ]` with a dated NOT-OWED
      line, no box left in its pre-realization state).
- [ ] T033 Commit the Speckit tree — `checklists/` and `analysis.md` — with
      explicit paths and the three trailers. (FR-019)
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
- T027, T028 → T029: the final gate run must cover the packet edits.
- T029 → T030, T031, T032 → T033 → T034.

## Parallel opportunities

- T004 runs alongside T005–T009 (different tree).
- T030, T031 and T032 run together after T029.
- Within Phase 5, T019–T026 are one file and are NOT parallel.

## Implementation strategy

MVP is US1 alone: the § 3.4 adoption is the box that holds the packet open.
US3 then makes the gates re-runnable, and US2 makes the record true. Stop at (B)
with the gate report; the lane claims, opens the PR, lands, and archives.
