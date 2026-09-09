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

- [x] T011 [US3] Create `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md`
      with a header naming the head, the branch, the lane and what the file is
      NOT: not a ruling, not a ratification, not a promotion; LOCAL evidence at a
      named head rather than a CI result (FR-023); and a record of edits to an
      ACTIVE packet, which the ratified archived-record requirement does not yet
      bind (FR-022). (FR-013, FR-022, FR-023)
      **Done 2026-09-08** — created `openspec/changes/govern-archived-record-edits/evidence/realization-2026-09-08.md` with a header naming head
      `645e88ec`, branch, lane `opsXfactory-1`, and the three disclaimers (not a ruling, not
      a ratification, not a promotion), plus § *What this file is*: LOCAL evidence at a named
      head rather than CI (FR-023), and a record of edits to an ACTIVE packet which the
      ratified archived-record requirement does not yet bind (FR-022), with FR-033's
      after-the-archive statement beside it. The two evidence homes and their different jobs
      are stated (FR-013b).

- [x] T012 [US3] Take the pinned-target measurement at this head and record it,
      worded exactly: no IN-REPO `sha256` pin names `docs/document-lifecycle.md`,
      measured at base `68712924`; the only pairings are illustrative fixtures
      under `examples/document-cataloging/`. (FR-008)
      **Done 2026-09-08** — recorded in the packet evidence file § *Measurement 1*, worded
      as FR-008 requires: no IN-REPO `sha256` pin names `docs/document-lifecycle.md`, measured
      at base `68712924`. Method named (FR-008a): the two greps, and `contracts/manifest.yaml`
      PARSED as YAML rather than grepped -> 0 `docs/`-prefixed path values. FIVE files name the
      path and each was RESOLVED rather than dismissed; the fixture criterion is PROVEN, not
      asserted — `validate-document-catalog.py` schema-validates shape and never hashes a file
      on disk, doc-health's catalog families read `health/document-catalog/` WHICH DOES NOT
      EXIST in this repository, and the fixtures' own README calls them "static reference
      material, not runtime state". Re-taken at the final head by T029.

- [x] T013 [US3] Take the MODIFIED-block currency measurement at this head
      (canon characters, delta characters, canon lines removed) and record it as
      a measurement with its command. (FR-012, task 4.2 — measured, NOT ticked)
      **Done 2026-09-08** — packet evidence file § *Measurement 2*, with its command:
      canon **5,815** chars, delta **7,209** (the quickstart script's own bound) / **7,186**
      (bounded at `## ADDED Requirements`), **0 canon lines removed**, 17 lines added. The two
      delta figures are RECONCILED rather than one reported: the 23-character gap is exactly
      `len("\n## ADDED Requirements\n")`, the discrepancy sits in this feature's own quickstart
      expectation (corrected forward in the same commit, the superseded sentence quoted), and
      the load-bearing result — 0 canon lines removed — is identical under both bounds. Box 4.2
      is MEASURED, NOT TICKED.

- [x] T012a [US3] Re-check the CROSS-CITATIONS on BOTH `main` lines — this
      packet's citations of the twin and the twin's citations of this packet —
      from a read-only clone of OpsxFactory, and record: the two heads, each
      citation, whether it resolves, and the twin's merge sha
      `bbbef015cd394e2de31586b9718356586c413884`. A citation that does not
      resolve STOPS the branch (FR-025), it is not a note. (FR-007a, SC-010)
      **Done 2026-09-08** — packet evidence file § *Measurement 3*. Read-only clone
      `<scratchpad>/opsx-citation-archive`, `git fetch origin main` taken first; nothing in
      OpsxFactory was written. Two heads: openxFactory `origin/main` `6cc06288`, OpsxFactory
      `origin/main` `bbbef015cd394e2de31586b9718356586c413884` (the twin merge itself, PR #279,
      2026-09-08T15:28:23Z, `merge-base --is-ancestor` confirms). EVERY CROSS-CITATION RESOLVES
      IN BOTH DIRECTIONS — seven of this packet's, six of the twin's, each tabulated with its
      result. Two were worth resolving rather than assuming: `add-content-address-integrity-gate`
      is ABSENT from OpsxFactory `main` and resolves as PROPOSED on branch
      `change/add-content-address-integrity-gate` (`cbbe5b48`), which is exactly what the packet
      asserts; and `add-pre-archive-citation-gate` HAS since archived, so the archive path the
      packet named as conditional is now present and the live path is gone — the packet named
      BOTH on purpose, so the citation resolves and only its tense is stale. No citation failed,
      so FR-025's stop was not triggered on this ground.

- [x] T012b [US3] CONTINGENCY, and it is a task rather than a hope: if T012's
      measurement finds a pin naming any file this feature edits, or a candidate
      pin that cannot be resolved, STOP — record the finding, do not tick, do not
      land the edit, and report at STOP (B). (FR-008c, FR-025)
      **NOT TRIGGERED, and checked rather than assumed 2026-09-08** — T012's measurement
      found no pin naming any file this feature edits, and no candidate pin was left
      unresolved. The one candidate that needed resolving (`content_hash` beside the path in
      two `examples/document-cataloging/` fixtures) was resolved against the code that would
      read it: nothing does. The contingency stands available for the T029 re-take.

- [x] T014 [US3] Run task 4.1's two pinned-CLI gates THROUGH
      `scripts/validate-openspec-cli-pin.py` with the pinned 1.12.0 on `PATH`
      (never PATH's 1.2.0), capture rc and the summary lines to files under the
      feature's `evidence/`, and record in the packet evidence file: the EXACT
      command text with its environment, the counts, and the pinned CLI's version
      and verified provenance. Compare the dispositioned-exception count in BOTH
      DIRECTIONS against the ratification record's baseline (99 passed / 2 failed,
      0 undispositioned) and explain any movement either way.
      (FR-013a, FR-024, SC-002, panel P7)
      **Done 2026-09-08** — both runs through `scripts/validate-openspec-cli-pin.py` with
      the pinned 1.12.0 on `PATH`; PATH's 1.2.0 was never used. `--change
      govern-archived-record-edits --strict`: **rc 0**, `Totals: 1 passed, 0 failed (1 items)`.
      `--all --strict`: **rc 0**, `Totals: 99 passed, 2 failed (101 items)`, 0 UNDISPOSITIONED.
      Pinned CLI provenance recorded: `@fission-ai/openspec@1.12.0` at content address
      `c844543999f673cdd72445879b86a4abea4c07ef`, integrity `sha512-oFE2Lj7WVSc87nSi…`
      verified on every run. SC-002 COMPARED IN BOTH DIRECTIONS against the ratification
      record's 99/2/0 baseline: the count moved in NEITHER direction — not up (a new
      undispositioned finding this branch could not clear, `contracts/**` being frozen) and not
      down (a difference too, not a bonus). Captures `evidence/gate-4.1-change-strict.txt` and
      `evidence/gate-4.1-all-strict.txt`; both carried the pinned CLI's host-absolute banner
      paths, substituted to `<pinned-cli-cache>`/`<scratchpad>` under the estate rule against
      host-absolute paths in committed files, with the substitution declared in the evidence
      file and nothing else altered.

- [x] T015 [US3] Run task 4.3's four validators, capture rc and summary lines,
      record them.
      **Done 2026-09-08** — all four exit **rc 0**, capture
      `evidence/gate-4.3-validators.txt`: `sequenced_after validation passed (41 active
      changes, 8 declaring the field).`; `per-change sweep ledger consistent with the corpus
      (185 rows).`; `scope_globs validation passed (all active changes conform).`; `OK
      contracts/manifest.yaml: 188 per-file digest(s) verify`.

- [x] T016 [US3] Run doc-health on the branch with `--report-out` and diff its
      FINDING SET against T004's `main` report, using the identity-safe recipe
      T004 proved: TWO INDEPENDENT RUNS from identically-named checkouts, or a
      normalization of all THREE stamped places (`repo=\S+`, the
      `Repo-Identity:` header, the "scope limited to single repo" line), plus the
      run date. NEVER `--previous-report` — it refuses on identity mismatch by
      design (`REFUSE previous-report-identity-mismatch`). Record the diff
      verbatim, including "empty" if it is empty, and state separately any COUNT
      that moved only because the document grew (word totals, canon share), which
      is not a finding. A non-empty finding-set diff is a BLOCKER (FR-020).
      **Done 2026-09-08; FINDING SET IDENTICAL** — the identity-safe recipe T004 proved,
      with both baseline checkouts named `oxf-realize-f3`; `--previous-report` never used.
      A FIRST comparison was taken across the 2026-09-09T00:00Z rollover and is STRUCK, not
      deleted: every aging finding embeds a day count, so all of them moved and two topics
      crossed the 30-day threshold (55 -> 57 warnings) for reasons that have nothing to do with
      this diff. The comparison OF RECORD pins the aging clock on both sides with `--as-of
      2026-09-09` and RE-PROVES main-vs-main at that same `--as-of` (zero differences) before
      comparing. Result: `diff` of the `- severity=` finding lines returns **ZERO differences**;
      headline identical at 10 critical / 9 error / 55 warning / 16 info. The full-report diff
      is not empty and the two differing lines are NAMED rather than smoothed away — canon and
      governance word totals +199 each (share unchanged at 38.9%) and the `standard` stage word
      count +199 (document count unchanged at 6) — counts that moved only because the document
      GREW, which is not a finding. Both runs exit rc 1 on PRE-EXISTING findings identical on
      `main` (FR-037). Superseded interim kept at
      `evidence/doc-health-diff-INTERIM-superseded-clock-rollover.txt`.

- [x] T017 [US3] Run task 4.5's pytest paths, capture rc and the `N passed` line
      to a file, record them.
      **Done 2026-09-08** — `python3 -m pytest tests/sequenced_after tests/proposal-support
      tests/scope_globs -q`: **rc 0** captured as a return code rather than inferred from a
      pipeline, summary `330 passed, 2 subtests passed in 26.32s`. Capture
      `evidence/gate-4.5-pytest.txt`.

- [x] T018 [US3] Commit S2+S3 (the evidence file and the captured outputs) with
      explicit paths and the three trailers.
      **Done 2026-09-08** — `git diff --cached --stat` read before committing and named no
      foreign path: the packet evidence file, the eleven captures under the feature's
      `evidence/`, the forward correction to `quickstart.md` § 5, and this file. Three trailers
      on this commit. No box in the PACKET's `tasks.md` is ticked yet — that is T027's single
      commit, and FR-018 is the reason this evidence lands first.


**Checkpoint**: every claim US2 will tick against is now recorded at a named head.

---

## Phase 5: User Story 2 — the truthful task record (Priority: P2)

**Goal**: `openspec/changes/govern-archived-record-edits/tasks.md` says, box by
box, what was done, by whom, and what is owed elsewhere.

**Independent test**: read that file alone and name the responsible repository
and actor for each of the 28 boxes.

- [x] T019 [US2] Amend, in the packet's `tasks.md` and in commit `3b530009`'s
      FORM — a BLOCK QUOTE of the superseded sentence plus the neighbouring clause
      NAMED as not superseded, dated and attributed to this change: the preamble
      (line 7), § 0.1's "THE BOX STAYS UNTICKED" paragraph (lines 58–66), § 1's
      "GIVEN 2026-09-08, AND THE BOXES BELOW STAY UNTICKED" (line 70) and its
      re-assertion (lines 74–78). Same commit as the ticks. (FR-017, FR-017a)
      **Done 2026-09-08 in commit `0e7a67f3`** (ticked here in the following commit, so no
      tick precedes its evidence). Four passages amended in commit `3b530009`'s form — block
      quote of the superseded sentence plus the neighbouring clause NAMED as not superseded,
      dated and attributed to this change: the preamble, § 0.1's "THE BOX STAYS UNTICKED"
      paragraph, § 1's "GIVEN 2026-09-08, AND THE BOXES BELOW STAY UNTICKED" and its
      re-assertion. Same commit as the ticks. Nothing rewritten in place: the packet
      `tasks.md` diff deletes exactly 21 lines — the 19 tick markers and the 2 headings — and
      nothing else.

- [x] T019a [US2] Amend the TWO HEADINGS with whole-token markers, each naming the
      ratified clause it supersedes: § 1 "Ratification — OWED, NOT GIVEN" (line
      68), whose own line 73 says the heading is left as written on purpose, and
      § 3 "Composition — named here; 3.4 alone is this packet's own act" (line
      161), which 3.1's tick falsifies. (FR-017b; veto point 5)
      **Done 2026-09-08 in commit `0e7a67f3`.** § 1 now reads `## 1. Ratification — OWED,
      NOT GIVEN — AMENDED 2026-09-08` and § 3 `## 3. Composition — named here;
      3.4 alone is this packet's own act — AMENDED 2026-09-08` — the pair's
      CLOSED marker vocabulary `AMENDED <UTC date>` as a whole token, adopted
      from the twin in place of the `[SUPERSEDED …]` form first written —
      whole-token markers, not bare parentheticals, with the original words kept in front of
      each. § 1's amendment NAMES the ratified clause it supersedes ("The heading is left as
      written because it names what the section was raised to hold") and says that superseding
      a deliberate decision is why that clause is named; it is VETO POINT 5. § 3's names the
      superseded clause "3.4 alone is this packet's own act" and keeps "Composition — named
      here" as not superseded.

- [x] T019b [US2] Write the dated CORRECTED block for § 0.1's PERFORMED note,
      QUOTING its stale words "this packet is `Status: draft` awaiting
      ratification at task 1.1" (line 60) — true when written, false now — and
      never rewriting them in place. (FR-017c)
      **Done 2026-09-08 in commit `0e7a67f3`.** A dated CORRECTED block under § 0.1 quotes
      the stale words "this packet is `Status: draft` awaiting ratification at task 1.1" and
      says they were TRUE WHEN WRITTEN and are false now, citing the file's own `Status:
      ratified` header and the ratification record. Never rewritten in place. The neighbouring
      corpus-precedent sentence about `add-consent-custody-rederivation-record` is explicitly
      NOT corrected, because re-measurement (46 unticked / 0 ticked at `main` `6cc06288`,
      2026-09-09 UTC) shows it still true as written.

- [x] T020 [US2] Tick § 0.1 with a dated note: the row on `main` reads
      `moved_by: "#788"` (`corpus-ledger.yaml:214`); the file is not rewritten
      here.
      **Done 2026-09-08 in commit `0e7a67f3`.** § 0.1 ticked with a dated note: the row on
      `main` reads `moved_by: "#788", moved_on: "2026-09-08"` at
      `tests/sequenced_after/corpus-ledger.yaml:214`, and `--ledger-diff` reports the corpus
      consistent at this head. The ledger file is READ and NOT rewritten by this branch.

- [x] T021 [US2] Tick § 1.1–1.5 with dated notes citing the record as the record
      does — GitHub review `5141756427`, APPROVED `2026-09-08T12:38:36Z`, record
      `review/ratification-2026-09-08.md` — and NO quotation: the approval body
      is empty. 1.2a/1.2b/1.2c note that the veto was not exercised and the
      default stands; 1.3 and 1.4 note the same. (FR-006)
      **Done 2026-09-08 in commit `0e7a67f3`.** § 1.1-1.5 ticked, every note citing the
      record as the record does — GitHub review `5141756427`, APPROVED `2026-09-08T12:38:36Z`,
      record `review/ratification-2026-09-08.md` — and NO WORD QUOTED anywhere, because the
      approval body is EMPTY. 1.2a/1.2b/1.2c each note that the veto was NOT exercised and name
      the default that therefore stands (wide pin scope; report-then-refuse; TWO `## ADDED`
      requirements); 1.3 and 1.4 note the same for D-3 and the strict read-only reading. 1.5 is
      ticked on the record EXISTING, with the box's "the word verbatim" phrase addressed
      head-on: the record states there are no words to quote, and inventing one to satisfy the
      box would be the defect this packet exists to refuse.

- [x] T022 [US2] Tick § 2.1–2.3 with dated notes naming the ratified baseline
      `8cc76e1b` and the delta's shape (1 MODIFIED + 2 ADDED, 18 scenarios).
      **Done 2026-09-08 in commit `0e7a67f3`.** § 2.1-2.3 ticked, each naming the ratified
      baseline `8cc76e1b` and the delta's measured shape — 1 `## MODIFIED` + 2 `## ADDED`
      blocks, 18 scenarios. 2.3's note also carries the one figure this realization corrects
      (the 7,186/7,209 block-bound reconciliation) and states that ticking 2.3 is NOT ticking
      4.2.

- [x] T023 [US2] Tick § 3.4 with a dated note naming the doc commit and the
      bullet's location. TICK § 3.1 TOO, on T012a's performed cross-citation
      check: the twin LANDED as OpsxFactory `main`
      `bbbef015cd394e2de31586b9718356586c413884` (PR #279, 2026-09-08T15:28:23Z),
      and the note cites the sha, the two heads checked, and the evidence file.
      Leave § 3.2, 3.3 and 3.5 UNTICKED, each with ONE dated NOT-OWED line — 3.3
      naming `add-consent-custody-rederivation-record` (merged `543d47a9`, 46
      boxes unticked). (FR-007, FR-007a, panel P2)
      **Done 2026-09-08 in commit `0e7a67f3`.** 3.4 ticked, naming commit `645e88ec` and the
      bullet's location (end of § *Status Claim Rules*, line 138, two sub-bullets). 3.1 ticked
      on T012a's PERFORMED cross-citation check, not on the merge alone, citing the sha
      `bbbef015cd394e2de31586b9718356586c413884`, PR #279, both heads checked and the evidence
      file. 3.2, 3.5 and 3.3 left UNTICKED, each with ONE dated NOT-OWED line; 3.3 names
      `add-consent-custody-rederivation-record` (merged `543d47a9`, 46 boxes unticked measured
      2026-09-09 UTC); 3.2 names OpsxFactory's `add-content-address-integrity-gate` and the
      register file `models/content-address-families.yaml` it proposes; 3.5 names every other
      DomainxFactory as a CLASS and states that no survey was performed and none is implied.

- [x] T024 [US2] Tick § 4.1, 4.3, 4.4, 4.5 with dated notes citing the evidence
      file's recorded results; leave § 4.2 UNTICKED with a dated note saying the
      measurement was taken and the box is deliberately open for the archive
      act. (FR-012)
      **Done 2026-09-08 in commit `0e7a67f3`.** 4.1, 4.3, 4.4 and 4.5 ticked, each citing
      the evidence file's recorded result rather than restating it. 4.2 left UNTICKED with a
      dated note saying the measurement was taken, recording where it lives, and stating why
      the box is deliberately open — a realization tick would retire the clearance signal the
      archive act is meant to re-take.

- [x] T025 [US2] Add the § 4 pinned-target note (FR-008 wording) beside the § 4
      boxes.
      **Done 2026-09-08 in commit `0e7a67f3`.** The pinned-target note sits at the head of
      § 4, beside the § 4 boxes, in FR-008's wording: no IN-REPO `sha256` pin names
      `docs/document-lifecycle.md`, measured at base `68712924`, with "in-repo" flagged as
      load-bearing and the full working referred to the evidence file.

- [x] T026 [US2] Tick § 5.1 (README row on `main` since #788); leave § 5.2 and
      5.3 UNTICKED with dated NOT-OWED lines naming the lane; leave § 6.1, 6.2
      and 6.3 UNTICKED with dated lines naming the archive act and, for 6.1, the
      fact that its gating box 3.4 is now ticked.
      **Done 2026-09-08 in commit `0e7a67f3`.** 5.1 ticked (README row on `main` since
      #788, not re-authored here, with the Rule 7 union re-derivation named as the lane's).
      5.2 and 5.3 left UNTICKED with dated NOT-OWED lines naming lane `opsXfactory-1`. 6.1,
      6.2 and 6.3 left UNTICKED with dated lines naming the archive act; 6.1's records that
      its gating box 3.4 IS NOW TICKED, so the condition it waits on is met.

- [x] T026a [US2] AUDIT THE NOTE CLASSES before committing: every one of the 28
      boxes carries exactly one of ticked-with-evidence / NOT-OWED /
      RUN-RECORDED-LEFT-OPEN, the three counts SUM TO 28, and every § 4 note cites
      the evidence file rather than restating a result. Record the three numbers.
      (FR-026, SC-006)
      **Done 2026-09-08, audited mechanically before the commit.** Every one of the 28
      boxes carries EXACTLY ONE class; no box carries two or none; every note carries its UTC
      date; the tick state matches the class on every box; and all five § 4 notes CITE the
      evidence file rather than restating a result. **THE THREE NUMBERS:
      ticked-with-evidence 19, NOT-OWED 8, RUN-RECORDED-LEFT-OPEN 1 — sum 28.** Recorded in
      the packet evidence file § *The note classes, and they sum to 28*, with the boxes
      enumerated per class.

- [x] T027 [US2] Commit T019–T026a as ONE commit — ticks and their notes together,
      never a tick ahead of its evidence; evidence without a tick is permitted and
      box 4.2 is that case. (FR-018)
      **Done 2026-09-08 as commit `0e7a67f3`** — ONE commit carrying T019-T026a together:
      the ticks, their notes, the NOT-OWED lines, the § 4 pinned-target note, the four sentence
      amendments, the two heading amendments and the CORRECTED block. No tick landed ahead of
      its evidence: every gate result it cites was recorded in `31704f0a`, the commit before.
      Evidence without a tick is permitted and box 4.2 is that case. Quotation check run before
      committing: 7 block quotes and 4 inline quotations, all 11 verbatim in the pre-edit
      bytes, 0 invented.

- [x] T028 [US2] Add the ONE additive dated realization note to the packet's
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
      **Done 2026-09-08 as commit `1b9b66c7`, committed SEPARATELY** so the veto reverts as
      one named act. The note sits immediately after the `Lane: opsXfactory-1` line and nothing
      is inserted above `Status:`; the YAML front matter is BYTE-IDENTICAL either side
      (sha256 of lines 1-5 unchanged) and the folded `code_surface:` scalar is untouched. The
      repository's own `corpus.parse_status` returns `ratified` for the file both before and
      after. It QUOTES the front-matter enumeration sentence and names the three ways
      realization makes it incomplete, and it also quotes the two sentences at lines 17 and 44
      that assert every box stays unticked, each as a whole sentence with the neighbouring
      unsuperseded clause named. The superseded-enumeration reason is stated in the commit
      message.

- [x] T028a Append ONE dated superseding sentence at the END of this change's
      README "OpenSpec Records" row, which asserts "all 28 boxes in `tasks.md`
      stay unticked" (README.md line 671). At the row's END, never near the block
      anchor, so a concurrent lane's row edit collides on a different line.
      (FR-010c; veto point 4; mirror ruling M-A1)
      **Done 2026-09-08 as commit `539edd28`, committed SEPARATELY** so this veto too
      reverts as one named act. ONE dated superseding amendment appended at the END of this
      change's README "OpenSpec Records" row — at line 643, the row's last line, 128 lines
      BELOW the "Active changes:" block anchor, so a concurrent lane's row edit collides on a
      different line. It block-quotes the superseded clause "all 28 boxes in `tasks.md` stay
      unticked, § 1's ratification boxes included" and names what is NOT superseded, including
      the one assertion realization did perform rather than dropping it silently.


**Checkpoint**: the packet reads truthfully and the branch is archive-ready.

---

## Phase 6: Gates and polish

- [x] T029 Re-run the FULL § 4 gate set at the final head (T027/T028 touched
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
      **Done 2026-09-08 at final head `539edd282dd3e16c0cba6c0e5395d3b2882a618f`.** The FULL
      § 4 set was re-run — none carried forward — and the evidence file gained a FINAL-HEAD
      RESULTS section; the earlier section is STRUCK by name as INTERIM (taken at `645e88ec`)
      and kept rather than deleted. Results at the final head: 4.1a rc 0 (1/0); 4.1b rc 0
      (99 passed / 2 failed / **0 UNDISPOSITIONED** — the ratified baseline exactly, moved in
      neither direction); all four 4.3 validators rc 0; 4.5 rc 0 `330 passed, 2 subtests
      passed`; 4.4 finding set **IDENTICAL** to `main`'s, same two non-finding word-count
      lines and no others. **NO GATE FAILED, so no tick is struck.** RE-TAKEN at this head as
      required: the pinned-target measurement (still no in-repo pin; `health/document-catalog/`
      still absent) and T002's ancestry check (`3504287a` still an ancestor; the log against
      `main` still EMPTY), both recorded BESIDE their earlier readings rather than over them.
      Idempotence demonstrated rather than assumed: a third baseline run at the same head and
      `--as-of` was BYTE-IDENTICAL. NO forward merge was taken, so this run is not stale on
      that ground; a veto exercised after it re-opens it for the paths it touches, and the two
      veto-bearing commits are isolated for exactly that.

- [x] T030 [P] Verify SC-007: `git diff main...HEAD --name-only` contains only
      the SIX allowed paths — the feature directory, `docs/document-lifecycle.md`,
      the packet's `tasks.md`, its new `evidence/` file, its `proposal.md`, and
      `README.md` — and nothing under any `archive/` path, nothing in `design.md`,
      `.openspec.yaml` or the spec delta.
      **Done 2026-09-08, verified at final head `be643e55`.** `git diff
      main...HEAD --name-only` names exactly the SIX allowed paths and nothing
      else: the feature directory `specs/032-govern-archived-record-edits/`,
      `docs/document-lifecycle.md`, the packet's `tasks.md`, its new
      `evidence/realization-2026-09-08.md`, its `proposal.md`, and `README.md`.
      The forbidden-path scan returns NOTHING for any `archive/` path, the
      packet's `design.md`, `.openspec.yaml` or
      `specs/document-lifecycle/spec.md`, or anything under `scripts/`,
      `.github/`, `contracts/` or `tests/`. Three-dot, so the comparison runs
      against the merge base `68712924`; no forward merge was taken, so the base
      did not move.

- [x] T030a [P] Verify SC-001 as the FULL LINE FORM, and WORD-DIFF the two
      explanatory sentences against FR-005's wording so a paraphrase cannot drift
      in unnoticed: the document contains
      `Edited (bookkeeping): <UTC date> by <change-id> — <edit class>`
      byte-for-byte, em dash and placeholders included, and the citation is the
      last clause of the bullet's parent prose. Substring presence is not the
      check. (Panel P8)
      **Done 2026-09-08.** SC-001 verified as the FULL LINE FORM, not substring
      presence: `docs/document-lifecycle.md` line 143 is exactly the two-space
      indent + the ratified form + the sentence's terminating period OUTSIDE the
      closing backtick, and the form matches the delta's line 122 byte-for-byte
      (em dash U+2014 and both placeholders). Exactly ONE occurrence. The
      citation is the LAST CLAUSE of the bullet's parent prose ("… Ratified by
      `govern-archived-record-edits` (2026-09-08)."), there is no colon after
      the change name, and the archive-act statement sits EARLIER in that prose.
      WORD-DIFF against FR-005's wording: both explanatory sentences contain
      every FR keyword in order, and the SequenceMatcher opcodes are INSERTIONS
      ONLY — no deletion and no substitution, so no paraphrase drifted in. The
      insertions are "authorizing the class of edit" (the ratified requirement's
      own phrase) and "so it is not the authorization for the edit" (required by
      FR-002). Exactly two explanatory sentences found.

- [x] T030b [P] Verify SC-009: every superseding amendment carries a block quote
      and names the clause that is NOT superseded — counted across `tasks.md`,
      the two headings, `proposal.md` and the README row.
      **Done 2026-09-08.** SC-009 counted across all EIGHT superseding
      amendments, every one carrying a block quote of what it supersedes AND
      naming the neighbouring clause that is not: in the packet `tasks.md` — the
      preamble, § 0.1's STAYS-UNTICKED paragraph, § 0.1's CORRECTED stale-text
      block, § 1's sentence plus its re-assertion, the § 1 heading marker and
      the § 3 heading marker; in `proposal.md` — the enumeration note covering
      the front-matter sentence and both unticked-state sentences; and in
      `README.md` — the row sentence. Totals: 25 block-quote lines and 7
      explicit not-superseded namings across the three files.

- [x] T031 [P] Verify FR-014 on every AUTHORED commit: `git log main..HEAD`
      shows `Lane: opsXfactory-1`, `Co-Authored-By: Claude Fable 5.1` and
      `Claude-Session:` on each; a forward-merge commit is exempt and is named as
      such. VERIFY FR-018 POST HOC in the same pass: for every tick, the commit
      that added it also added or cited its evidence — no tick appears in a commit
      earlier than the evidence it rests on.
      ~~**Done 2026-09-08.** FR-014 verified on ALL 11 authored commits in `git
      log main..HEAD`~~ — **STRUCK 2026-09-08 after the refutation panel: that
      count was true when written and stale when read.** Eleven was the range at
      the moment of the check; two commits followed it (`be643e55`, `5dccfad1`)
      and the panel measured 13. RE-VERIFIED by counting rather than recalling —
      13 of 13 authored commits carry `Lane: opsXfactory-1`, `Co-Authored-By:
      Claude Fable 5.1` and `Claude-Session:`, ZERO merge commits in that range
      — and RE-VERIFIED AGAIN after the forward merge, where the merge commit is
      the one entry FR-014 exempts and is named as such rather than counted as a
      violation. The number is struck, not deleted, and the same correction is
      owed to commit `5dccfad1`'s message, which carries the stale figure and
      cannot be rewritten; this line is that correction. FR-018 verified POST HOC by walking
      the range in order: all 19 packet ticks land in ONE commit, `0e7a67f3`,
      which itself touches the evidence file, and the evidence they cite was
      recorded in `31704f0a`, the commit BEFORE it. No tick appears in a commit
      earlier than the evidence it rests on.

- [x] T032 [P] Verify the three requirements no other task carries: FR-016 (no
      checker, workflow, pin or repair is authored — `git diff main...HEAD
      --name-only` names no file under `scripts/`, `.github/`, `contracts/` or
      `tests/`), FR-019 (the full Speckit tree is committed, `checklists/` and
      `analysis.md` included), and SC-006 (COUNT the packet's boxes: 28 total,
      each either `- [x]` with a dated note or `- [ ]` with a dated NOT-OWED
      line, no box left in its pre-realization state).
      **Done 2026-09-08.** FR-016: `git diff main...HEAD --name-only` names
      **0** files under `scripts/`, `.github/`, `contracts/` or `tests/` — no
      checker written, no pin edited, no pin repaired. FR-019: the full Speckit
      tree is committed — `spec.md`, `clarify-questions.md`, `plan.md`,
      `research.md`, `quickstart.md`, `tasks.md`, `analysis.md` and all EIGHT
      files under `checklists/`, 15 tracked files. SC-006: the packet's boxes
      COUNTED at HEAD — **19 `- [x]` + 9 `- [ ]` = 28**, each ticked box
      carrying a dated note and each unticked box a dated NOT-OWED or
      run-recorded line, and no box left in its pre-realization state.

- [x] T033 Commit the Speckit tree — `checklists/` and `analysis.md` — with
      explicit paths and the three trailers. (FR-019)
      **Done 2026-09-08 as this commit.** The Speckit tree was already committed
      by the specify/plan/checklist commits and is verified complete at T032;
      this commit carries the feature's own `tasks.md` ticks and the packet
      evidence file's final section, with explicit paths and the three trailers.
      It touches only `specs/032-govern-archived-record-edits/` and the packet's
      `evidence/` directory — neither gate-scanned (root `specs/` is outside
      doc-health's `GOVERNED_ROOTS` and outside the pinned CLI's change scan;
      `evidence/` is excluded from the lifecycle scan by `EVIDENCE_PARTS` and is
      not part of the spec delta) — and the full gate set was re-run afterwards
      to CHECK that rather than assert it.

- [x] T033a VERIFY THE STOP CONDITION AGAINST REPOSITORY STATE, not intention:
      no pull request exists for this branch that this feature opened, no comment
      was posted by it anywhere, no merge or `openspec archive` was run, and the
      working tree is clean. (FR-015, FR-038)
      **Done 2026-09-08, verified AGAINST REPOSITORY STATE rather than
      intention.** `gh api
      repos/opensoft/openxFactory/pulls?head=opensoft:032-govern-archived-record-edits&state=all`
      returns **0** — no pull request exists for this branch, open or closed.
      `git merge-base --is-ancestor HEAD origin/main` fails: NOT MERGED. The
      change directory is still `openspec/changes/govern-archived-record-edits/`
      with NO entry under `openspec/changes/archive/`, so `openspec archive` was
      never run. No GitHub comment was posted on any surface in any repository,
      and no such act was routed to another agent, session or person. The only
      `gh` invocation this realization made is the read-only PR query in this
      line, which the task itself directs. Working tree clean at the stop.

      **CORRECTED 2026-09-09 by `archive-govern-archived-record-edits` (lane
      `opsXfactory-1`) — stale-but-TRUE-WHEN-WRITTEN text, quoted and never
      rewritten in place.** The record above states:

      > The change directory is still `openspec/changes/govern-archived-record-edits/`
      > with NO entry under `openspec/changes/archive/`, so `openspec archive` was
      > never run.

      That was TRUE on 2026-09-08 and is FALSE NOW. `openspec archive` WAS run,
      on 2026-09-09 through the pinned CLI 1.12.0, and the packet is at
      `openspec/changes/archive/2026-09-09-govern-archived-record-edits/`.
      **THE RECORD IS NOT WEAKENED BY THE CORRECTION AND IS THE STRONGER FOR
      IT**: T033's claim was about what THE REALIZATION did, and the realization
      still ran no archive — a SEPARATE act, in a separate change on a separate
      branch, did, which is exactly the separation T033 exists to prove.
      **EVERY OTHER SENTENCE OF THE RECORD STILL HOLDS UNQUALIFIED**, the
      0-pull-requests query and the NOT-MERGED merge-base included, both being
      statements about the realization branch at its own stop.

- [x] T034 Copy the checklists' results and the final gate summary into the
      report for STOP (B), then STOP: no `gh`, no PR, no comment, no merge, no
      `openspec archive`. (FR-015)
      **Done 2026-09-08.** The checklist results (327 passed / 4 dispositioned /
      0 open) and the final gate summary are carried into the STOP (B) report.
      STOPPING HERE: no `gh` write, no PR, no comment, no merge, no `openspec
      archive`. Claiming, the pull request, the LANDING/LANDED notices, the
      claim discharge on issue #630 and the archive act are lane
      `opsXfactory-1`'s.


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
