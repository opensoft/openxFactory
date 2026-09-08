# Checklist: Evidence and Traceability — 032-govern-archived-record-edits

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

**Purpose**: Release-gate validation that every evidentiary claim this feature
makes is tied to a re-runnable command and a named head, honestly separated
into interim and final-head results, correctly scoped as non-authoritative,
and free of invented quotation — this checklist interrogates the WRITTEN
REQUIREMENTS for the evidence, not whether any gate currently passes.
**Created**: 2026-09-08
**Feature**: [spec.md](../spec.md)

## Claim-to-Command Traceability

- [ ] CHK001 Is every claim recorded in the evidence file paired with the exact
      command that produced it, rather than a description of the command?
      [Traceability, Spec US3-AS1] **— OPEN:** FR-011 requires gate output to be "recorded verbatim" but never requires the exact command text itself to be recorded beside each claim, only the output. **FIX:** Add a clause to FR-011 requiring every recorded result to be paired with the exact command text that produced it, not merely a task reference.
- [ ] CHK002 Is the head (a commit sha, not "current" or "now") required beside
      every recorded result, so a later reader knows what state produced it?
      [Traceability, Spec FR-011] **— OPEN:** FR-011 and Tasks T001/T029 record one session-level head plus interim/final labels, but no requirement pairs an actual commit sha with every individual recorded result. **FIX:** Add a clause requiring each recorded result in the evidence file to carry the commit sha it was taken at, not only a categorical "interim/final" label.
- [x] CHK003 Is "re-run each named command at the named head and reproduce each
      stated result" stated as the acceptance test for the evidence file,
      rather than left implicit in the file merely existing? [Measurability,
      Spec US3 Independent Test]
- [x] CHK004 Are the four § 4 gate families (4.1, 4.3, 4.4, 4.5) each mapped to
      a distinct, separately-labeled evidence entry, so no gate's result can be
      inferred from another's? [Coverage, Tasks T014-T017]
- [x] CHK005 Is the pinned CLI's prefix path required as part of the
      reproducible command text itself, rather than left to be inferred from
      the phrase "the pinned CLI"? [Ambiguity, Plan Technical Context]

## Evidence Artifact Identity, Home and Non-Authority

- [x] CHK006 Is the evidence file's exact path specified, including that a copy
      lives inside the packet's own `evidence/` directory as well as this
      feature's? [Traceability, Spec FR-013]
- [x] CHK007 Is the evidence file's non-authority stated explicitly — that it is
      not a ruling, not a ratification and not a promotion — rather than left
      to be inferred from its filename or directory? [Ambiguity, Tasks T011]
- [x] CHK008 Is the mechanism by which the evidence file owes no lifecycle
      header specified (its directory segment is excluded from doc-health's
      lifecycle scan set), rather than asserted with no stated mechanism?
      [Measurability, Spec FR-013, Research M4]
- [x] CHK009 Is a `review/`-homed record distinguished from an
      `evidence/`-homed one by the obligation each carries, so a future author
      could not relocate the file without changing what it owes? [Consistency,
      Spec FR-013, Research M4]
- [x] CHK010 Is the evidence file's required header content specified as a
      closed, checkable set (head, branch, lane, and what the file is not)
      rather than an open-ended description? [Completeness, Tasks T011]

## Commit/Evidence Coupling (FR-018)

- [x] CHK011 Is "a box is ticked in the same commit that records its evidence"
      stated as a rule about COMMIT boundaries, rather than about ordering
      within a working tree? [Ambiguity, Spec FR-018]
- [x] CHK012 Is the failure mode FR-018 exists to refuse — a tick landing ahead
      of its evidence — defined precisely enough that a reviewer could detect
      it from `git log` alone? [Measurability, Spec FR-018]
- [ ] CHK013 Is "or neither happens" specified so the rule reads as asymmetric —
      evidence may be recorded with no corresponding tick (box 4.2), but a tick
      may never precede its evidence — rather than as a strict two-way pairing?
      [Ambiguity, Spec FR-018, FR-012] **— OPEN:** FR-018's "or neither happens" reads as a strict biconditional (tick and evidence always co-occur), which literally conflicts with FR-012's exception letting box 4.2 be measured and recorded with no tick. **FIX:** Amend FR-018 to state the rule is asymmetric — evidence may be recorded without a tick (per FR-012's box 4.2), but a tick may never precede its evidence.
- [ ] CHK014 Is the one deliberate exception to synchronous tick+evidence (box
      4.2, measured but left unticked) reconciled against FR-018's general
      rule, so the two requirements do not read as contradictory? [Conflict,
      Spec FR-012, FR-018] **— OPEN:** No sentence in spec.md cross-references FR-012 and FR-018 to reconcile box 4.2's measured-but-unticked state with FR-018's "or neither happens" wording. **FIX:** Add a cross-reference in FR-018 (or FR-012) explicitly naming box 4.2 as the sanctioned exception to the general tick/evidence pairing rule.
- [ ] CHK015 Is a verification method for FR-018 specified — by commit
      contents after the fact — rather than left to depend on the author's own
      account of the order events happened in? [Measurability, Spec FR-018,
      Tasks T027] **— OPEN:** FR-018 is enforced only by author discipline at commit time (Tasks T027); no task performs a post-hoc `git log`/`git show` check that a tick never precedes its evidence. **FIX:** Add a verification task alongside T030-T032 that inspects commit history to confirm no box's tick commit lands before its cited evidence exists.

## Alternate Flow — Interim vs Final-Head Currency

- [x] CHK016 Is the distinction between an INTERIM gate result and a
      FINAL-HEAD result specified as a labeled property of each recorded
      result, rather than left to be inferred from its position in the file?
      [Ambiguity, Tasks T029]
- [x] CHK017 Is the disposition of an interim result specified once a
      final-head result exists for the same gate — superseded-but-retained, or
      removed — rather than left unstated? [Gap, Tasks T029]
- [x] CHK018 Is the trigger for re-running a gate at a new head specified
      (commits touching `openspec/changes/**`) rather than left to judgment
      about which commits "matter"? [Measurability, Plan S6, Tasks T029]
- [x] CHK019 Is the MODIFIED-block currency measurement (task 4.2) required to
      be RE-TAKEN at the final head rather than carried forward from an earlier
      measurement, even when canon is believed not to have moved? [Consistency,
      Spec Edge Cases, FR-012]
- [x] CHK020 Is a way specified for a reader to tell "this measurement is
      current as of the final head" apart from "this measurement was true when
      captured but the head has since moved"? [Ambiguity, Tasks T029]

## Measurement Discipline

- [x] CHK021 Is "capture the return code AND the summary line to a file"
      required for every gate run, not only demonstrated for the pytest step it
      is illustrated with? [Consistency, Quickstart §4, Spec SC-005]
- [x] CHK022 Is the failure mode of a piped `tail` — reporting the pipeline's
      exit status rather than the command's — named as the reason for the
      file-capture rule, so the rule does not read as an arbitrary style
      preference? [Ambiguity, Quickstart §4]
- [x] CHK023 Is "recorded verbatim" (FR-011) quantified as the literal captured
      text, rather than a paraphrase or a summary composed after reading the
      output? [Measurability, Spec FR-011]
- [x] CHK024 Is the doc-health finding-set diff required to be recorded as the
      diff itself (or the word "empty"), rather than as a conclusion such as
      "no new findings" that could paper over an unexamined change?
      [Measurability, Tasks T016, Spec SC-003]
- [x] CHK025 Is a rule stated for distinguishing, in the record, a count that
      moved only because the document grew (word totals, canon share) from a
      genuine new or resolved finding? [Ambiguity, Spec Edge Cases, Tasks T016]

## Exception Handling — Citation Fidelity and Quotation Discipline

- [ ] CHK026 Is "no invented quotation" stated as a requirement of every note
      that cites a record, rather than as guidance or an aside? [Ambiguity,
      Spec FR-006, Clarifications Q1/Q5] **— OPEN:** "No invented quotation" is stated only for the § 1 ratification note in FR-006; no requirement generalizes it to every other dated note in `tasks.md` that cites a record (twin notes, ledger notes, etc.). **FIX:** Generalize FR-006's citation-not-invention rule into a standalone requirement covering every dated note in `tasks.md`, not only the § 1 note.
- [x] CHK027 Is the specific fact that licenses this rule — the approval's
      GitHub review body is EMPTY — stated as the reason no verbatim
      ratification word exists to quote, so a future author cannot assume a
      quotable word was merely omitted from the note? [Gap, Spec FR-006]
- [x] CHK028 Are the exact fields a citation-only note must carry specified
      (review id, timestamp, record path) as a closed set, so two authors
      would not produce differently-shaped citations for the same fact?
      [Consistency, Spec FR-006]
- [x] CHK029 Is "cite records rather than paraphrase them" distinguished from
      summarizing a record's conclusion in the note-writer's own words — i.e.,
      is paraphrase itself defined anywhere, or only its prohibited instances
      named? [Ambiguity, Spec FR-006]
- [x] CHK030 Is the pinned-target measurement's required wording specified
      byte-for-byte ("no IN-REPO sha256 pin names … measured at base
      `68712924`") so two independent authors recording the same measurement
      would produce identical prose? [Measurability, Spec FR-008]

## Recovery — Re-Measurement When Canon or Base Moves

- [ ] CHK031 Is the response specified for the case where the re-check of M1
      (task T002) finds the packet or canon HAS moved since the plan was
      written — is "STOP and report" defined precisely enough to be followed
      without further judgment? [Exception, Tasks T002] **— OPEN:** T002's "STOP and report" names no report format, audience or channel, unlike the later "STOP (B)" convention which at least specifies checklist results plus gate summary. **FIX:** Amend T002 to route its STOP into the same STOP (B) architect-report path, or state its own minimal report content explicitly.
- [ ] CHK032 Is the disposition of already-captured evidence specified for a
      STOP-and-restart — discarded, re-validated, or left untouched pending a
      new plan? [Gap, Spec FR-018] **— OPEN:** No requirement states what happens to evidence already captured if a STOP-and-restart is triggered by a moved packet or canon (as opposed to the interim/final-head case FR-021/T029 already cover). **FIX:** Add a sentence extending FR-021's struck-not-deleted discipline explicitly to a T002-style STOP-and-restart, so already-captured evidence's disposition is stated.
- [ ] CHK033 Is the scenario where `main` moves under the branch (merge
      forward, never rebase) reconciled with the evidence file's head-naming
      requirement — does a merge commit require its own gate re-run and
      evidence entry? [Consistency, Spec Edge Cases, Assumptions] **— OPEN:** Nothing states whether a forward-merge commit from `main` that touches an in-scope path triggers its own gate re-run and evidence entry, though T029 states this trigger for the branch's own commits. **FIX:** Add a sentence to Edge Cases or FR-011 stating a forward-merge commit touching `openspec/changes/**` or `docs/document-lifecycle.md` triggers the same re-run and evidence-entry requirement as S6.

## Non-Functional — Reproducibility and Independence

- [ ] CHK034 Can the evidence file be used to reproduce every stated result by
      a reader who has NOT read `research.md` or `quickstart.md`, or does a
      claim depend on context only those files supply? [Completeness, Spec US3
      Independent Test] **— OPEN:** Because no requirement mandates embedding the exact command text in the evidence file itself (only the verbatim output), a reader without `quickstart.md` may not know what command produced a given result. **FIX:** Same fix as CHK001 — require the evidence file to carry the exact command text beside each result, making it self-sufficient without `quickstart.md`.
- [ ] CHK035 Is the evidence file required to be self-contained with respect to
      command invocation — full paths, `OPENSPEC_TELEMETRY=0`, `PATH`
      prefixing — rather than assuming the reader already has the pinned CLI on
      their own PATH? [Measurability, Quickstart §1] **— OPEN:** No requirement states the evidence file must itself carry full command invocation detail (PATH prefixing, `OPENSPEC_TELEMETRY=0`); that detail exists only in `quickstart.md`, a separate document. **FIX:** Require the evidence file to reproduce each command's full invocation (env vars, PATH prefix) rather than relying on the reader consulting `quickstart.md`.
- [ ] CHK036 Is a mechanism specified for keeping the evidence file's claims
      from drifting out of sync with `tasks.md`'s citations of it, once both
      exist? [Consistency, Spec FR-006, Tasks T024] **— OPEN:** No task or requirement re-checks or updates `tasks.md`'s § 4 citations of the evidence file when T029 updates that file with final-head results. **FIX:** Add a step to T029 (or a new task) confirming `tasks.md`'s § 4 notes still match the evidence file's final-head content after the update.
- [x] CHK037 Is the § 4.2 measurement's own reproduction script (the Python
      block computing canon/delta character counts and removed lines) treated
      as part of the specified command, so "the command" for that measurement
      is unambiguous rather than described only in prose? [Measurability,
      Quickstart §5]

## Notes

- **CHK017** and **CHK032** name the same underlying gap from two directions:
  neither the spec nor the tasks say what becomes of a superseded or
  since-invalidated evidence entry. This feature never hits the STOP path
  (M1's re-check is expected to come back empty), so the gap is latent rather
  than blocking — but a later reader following this checklist against a
  different STOP-triggering run would find nothing written to follow.
- **CHK029** is a genuine definitional gap: "cite, don't paraphrase" is easy to
  state and hard to bound. The spec gives one worked example (no invented
  ratification quote) but never says where description of a record's contents
  crosses into disallowed paraphrase.

**Evaluator's note on the two items above (2026-09-08):** both notes predate
the amendment pass. CHK017 is now PASSED — FR-021 plus Tasks T029 specify the
disposition (struck with a dated line naming the replacing head, never
deleted) for the interim/final-head case this note describes. CHK032 remains
OPEN because it names a distinct scenario (a T002-style STOP triggered by a
moved packet/canon, not a moved head) that FR-021/T029 do not explicitly
cover. CHK029 is now PASSED — FR-006's "a note MAY restate a fact... and MUST
NOT attribute words to the ratifier" gives the operative boundary (restatement
is citation, attribution is invention), even though the word "paraphrase"
itself is not separately defined.

## Evaluation — 2026-09-08

**Tally**: 25 passed / 12 open / 0 deferred (total 37).

### Open items
- CHK001 — FR-011 requires verbatim output but not the exact command text beside each claim → add a clause requiring the command text itself to be recorded
- CHK002 — no commit sha required beside every individual recorded result, only a session head + interim/final label → require a sha per recorded result
- CHK013 — FR-018's "or neither happens" reads as a strict biconditional, conflicting with FR-012's evidence-without-tick exception for box 4.2 → amend FR-018 to state the rule is asymmetric
- CHK014 — FR-012 and FR-018 are not cross-referenced to reconcile box 4.2's exception → add an explicit cross-reference naming the exception
- CHK015 — FR-018 has no post-hoc git-log verification task, only author discipline at commit time → add a verification task alongside T030-T032
- CHK026 — "no invented quotation" is scoped to the § 1 note only, not generalized to every citing note in tasks.md → generalize FR-006's rule into a standalone requirement
- CHK031 — T002's "STOP and report" names no report format, audience or channel → route it into the STOP (B) path or state its own report content
- CHK032 — no stated disposition for evidence already captured before a T002-style STOP-and-restart → extend FR-021's struck-not-deleted discipline to this case
- CHK033 — no trigger stated for whether a forward-merge commit from main requires its own gate re-run/evidence entry → add a trigger sentence to Edge Cases/FR-011
- CHK034 — evidence file isn't required to embed command text, so it may not be reproducible without quickstart.md → same fix as CHK001
- CHK035 — evidence file isn't required to carry full command invocation detail (env vars, PATH prefix) → require full invocation text in the evidence file
- CHK036 — no mechanism keeps tasks.md's § 4 citations in sync when T029 updates the evidence file at the final head → add a sync-check step to T029

### Deferred items
(none — every item concerned the written requirements, which exist now and were judged against the current text)
