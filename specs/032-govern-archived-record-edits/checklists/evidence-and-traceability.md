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

- [x] CHK001 Is every claim recorded in the evidence file paired with the exact
      command that produced it, rather than a description of the command?
      [Traceability, Spec US3-AS1]
- [x] CHK002 Is the head (a commit sha, not "current" or "now") required beside
      every recorded result, so a later reader knows what state produced it?
      [Traceability, Spec FR-011]
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
- [x] CHK013 Is "or neither happens" specified so the rule reads as asymmetric —
      evidence may be recorded with no corresponding tick (box 4.2), but a tick
      may never precede its evidence — rather than as a strict two-way pairing?
      [Ambiguity, Spec FR-018, FR-012]
- [x] CHK014 Is the one deliberate exception to synchronous tick+evidence (box
      4.2, measured but left unticked) reconciled against FR-018's general
      rule, so the two requirements do not read as contradictory? [Conflict,
      Spec FR-012, FR-018]
- [x] CHK015 Is a verification method for FR-018 specified — by commit
      contents after the fact — rather than left to depend on the author's own
      account of the order events happened in? [Measurability, Spec FR-018,
      Tasks T027]

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

- [x] CHK026 Is "no invented quotation" stated as a requirement of every note
      that cites a record, rather than as guidance or an aside? [Ambiguity,
      Spec FR-006, Clarifications Q1/Q5]
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

- [x] CHK031 Is the response specified for the case where the re-check of M1
      (task T002) finds the packet or canon HAS moved since the plan was
      written — is "STOP and report" defined precisely enough to be followed
      without further judgment? [Exception, Tasks T002]
- [x] CHK032 Is the disposition of already-captured evidence specified for a
      STOP-and-restart — discarded, re-validated, or left untouched pending a
      new plan? [Gap, Spec FR-018]
- [x] CHK033 Is the scenario where `main` moves under the branch (merge
      forward, never rebase) reconciled with the evidence file's head-naming
      requirement — does a merge commit require its own gate re-run and
      evidence entry? [Consistency, Spec Edge Cases, Assumptions]

## Non-Functional — Reproducibility and Independence

- [x] CHK034 Can the evidence file be used to reproduce every stated result by
      a reader who has NOT read `research.md` or `quickstart.md`, or does a
      claim depend on context only those files supply? [Completeness, Spec US3
      Independent Test]
- [x] CHK035 Is the evidence file required to be self-contained with respect to
      command invocation — full paths, `OPENSPEC_TELEMETRY=0`, `PATH`
      prefixing — rather than assuming the reader already has the pinned CLI on
      their own PATH? [Measurability, Quickstart §1]
- [x] CHK036 Is a mechanism specified for keeping the evidence file's claims
      from drifting out of sync with `tasks.md`'s citations of it, once both
      exist? [Consistency, Spec FR-006, Tasks T024]
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

**Evaluator's note on the two items above (2026-09-08, updated after the
amendment pass):** both notes predate the amendments. CHK017 is PASSED — FR-021
plus Tasks T029 specify the disposition (struck with a dated line naming the
replacing head, never deleted) for the interim/final-head case this note
describes. CHK032 is NOW ALSO PASSED, on re-evaluation: FR-025 explicitly
routes a T002-style STOP into the STOP (B) report path, and FR-021's
unqualified "corrections are forward-only... never deleted" rule reaches any
evidence invalidated on this branch, a STOP-and-restart included, not only the
interim/final-head case. CHK029 is PASSED — FR-006's "a note MAY restate a
fact... and MUST NOT attribute words to the ratifier" gives the operative
boundary (restatement is citation, attribution is invention), even though the
word "paraphrase" itself is not separately defined.

## Evaluation — 2026-09-08 (round 3, re-evaluated after amendments)

**Tally**: 37 passed / 0 open / 0 dispositioned (total 37).

The last previously-open item, CHK015, flipped to PASS this round: Tasks T031
now adds "VERIFY FR-018 POST HOC in the same pass: for every tick, the commit
that added it also added or cited its evidence — no tick appears in a commit
earlier than the evidence it rests on" — a dedicated post-hoc commit-history
check, not just author discipline at commit time. Combined with round 2's
closures (FR-013a's exact-command-plus-environment-plus-head requirement,
FR-018's explicit non-biconditional statement, FR-027's blanket
no-invented-quotation rule, FR-025's STOP-AND-REPORT routing, the forward-merge
Edge Case, and T026a's cite-don't-restate anti-drift rule), every item in this
checklist now passes.

### Open items
(none)

### Dispositioned items
(none)

### Deferred items
(none — every item concerned the written requirements, which exist now and were judged against the current text)

