# Checklist: Tooling and Gates — 032-govern-archived-record-edits

**State**: written 2026-09-08, NOT YET RUN — this file is the gate instrument for the architect's refutation panel. The findings its authoring raised were resolved in the analyze loop and are recorded in [`../analysis.md`](../analysis.md).

**Purpose**: Release-gate validation that the gate SET, the pinned-CLI
configuration, the doc-health comparison baseline, re-run/idempotency
expectations and failure handling are stated precisely enough to be run the
same way by two different readers — this checklist interrogates the WRITTEN
REQUIREMENTS for the gates, not whether any gate currently passes.
**Created**: 2026-09-08
**Feature**: [spec.md](../spec.md)

## Gate Set Enumeration and Pass Conditions

- [ ] CHK001 Is the complete set of gates this feature must run enumerated in
      one place, closed against the packet's § 4 (4.1 through 4.5), rather than
      left to be assembled from scattered references across spec, plan and
      quickstart? [Completeness, Spec Key Entities, Openspec tasks §4]
- [ ] CHK002 Is each gate's pass condition stated as a measurable predicate — an
      exit code, a count, a diff being empty — rather than as a general
      expectation such as "clean" or "green"? [Measurability, Spec SC-002,
      SC-004, SC-005]
- [ ] CHK003 Is "zero undispositioned findings" for `--all --strict` defined, or
      at least distinguished from "zero findings", so "undispositioned" is not
      left as an unexplained term of art? [Ambiguity, Spec SC-002]
- [ ] CHK004 Is the `--change` invocation's pass condition (passes outright)
      kept distinct from the `--all` invocation's pass condition (a specific
      finding count), so task 4.1's two runs are not conflated into one
      requirement? [Ambiguity, Quickstart §1, Openspec tasks §4.1]
- [ ] CHK005 Is `--ledger-diff`'s expected output string ("per-change sweep
      ledger consistent with the corpus") specified as part of its pass
      condition, rather than only "exits 0"? [Measurability, Quickstart §2]
- [ ] CHK006 Are the four validators of task 4.3 each given an independently
      statable pass condition, so satisfying the requirement cannot be done by
      running one and inferring the rest? [Coverage, Tasks T015]
- [ ] CHK007 Is the pytest gate's pass condition specified as the captured
      summary line plus return code 0, rather than as "green" left undefined?
      [Measurability, Spec SC-005]

## Pinned CLI Discipline

- [ ] CHK008 Is "the pinned OpenSpec CLI 1.12.0, reached only through
      `scripts/validate-openspec-cli-pin.py`" stated as a MUST-level
      requirement, rather than as background describing the tooling in use?
      [Ambiguity, Plan Primary Dependencies, Assumptions]
- [ ] CHK009 Is "PATH's 1.2.0 is never used" stated as a prohibition WITH a
      detection method (e.g., the `PATH="$PIN/bin:$PATH"` prefix present in
      every recorded invocation), rather than as an instruction with no way to
      check compliance after the fact? [Measurability, Quickstart §1,
      Assumptions]
- [ ] CHK010 Is the environment needed to select the pinned CLI (the `PIN`
      prefix variable, `OPENSPEC_TELEMETRY=0`) specified as part of each gate's
      own definition, so "run the gate" is unambiguous about which binary
      answers? [Completeness, Quickstart §1]
- [ ] CHK011 Is a response specified for the case where
      `validate-openspec-cli-pin.py` itself is unavailable or resolves the
      wrong CLI version — is that a gate failure, or a setup precondition
      outside any gate's stated scope? [Gap, Quickstart §1]

## Baseline Timing for doc-health

- [ ] CHK012 Is the doc-health comparison baseline specified as a `main`
      checkout, rather than left ambiguous between "main" and "the branch's own
      parent commit"? [Ambiguity, Spec SC-003, Quickstart §3]
- [ ] CHK013 Is WHEN the baseline must be captured specified — before the
      `docs/document-lifecycle.md` edit lands on the branch — rather than left
      to be taken at whatever point the gate happens to run? [Measurability,
      Tasks T004]
- [ ] CHK014 Is the consequence of capturing the baseline AFTER the edit (rather
      than before) stated anywhere, so a reader understands why T004's ordering
      is load-bearing rather than a convenience? [Gap, Tasks T004]
- [ ] CHK015 Is the baseline's own currency addressed — if `main` advances
      between when the baseline is captured and when the final-head diff is
      taken, is the baseline re-captured or is the original retained? [Gap,
      Tasks T004, Spec Edge Cases]
- [ ] CHK016 Is the mechanism for obtaining the `main` checkout specified
      precisely enough that two readers would compare the branch against the
      same bytes (a named worktree or second checkout), rather than "whatever
      main looked like when I checked"? [Consistency, Quickstart §3]

## Idempotency and Re-Run Expectations

- [ ] CHK017 Is "running a gate twice at the same head yields the same result"
      stated as a general expectation of every gate in the set, or only
      demonstrated for the ledger seeder? [Coverage, Openspec tasks §0.1]
- [ ] CHK018 Is the ledger seeder's no-op behavior for a provenance-only
      correction specified with its own measured evidence (the "184 rows, 0
      moved by #999" / zero-line-diff result), rather than asserted as a
      general property of the tool? [Measurability, Openspec tasks §0.1]
- [ ] CHK019 Is it specified that this feature does NOT re-run the seeder —
      because the row's derived keys are already correct — as a rule
      distinguishing "a no-op if run" from "must not be run"? [Ambiguity,
      Openspec tasks §0.1, Spec FR-016]
- [ ] CHK020 Are idempotency expectations stated for the doc-health
      finding-set diff specifically — that running it twice at the same two
      heads (branch, main) produces the same diff — or is this left to be
      assumed from the tool's general behavior? [Gap, Tasks T016]
- [ ] CHK021 Is re-running the § 4 gate set at a NEW final head (task T029)
      kept distinct from re-running it AGAIN at the SAME head — i.e., is
      idempotency (same head, same result) kept separate from currency (new
      head, possibly different result)? [Ambiguity, Tasks T029]

## Gate Ordering Relative to Commits

- [ ] CHK022 Is the rule that the FINAL gate run must cover every commit
      touching `openspec/changes/**` stated as a precondition for that run
      counting as valid evidence, rather than as a scheduling preference?
      [Measurability, Plan S6, Tasks T029]
- [ ] CHK023 Is the dependency chain (doc edit → gate run → task ticks → final
      gate re-run) stated with the REASON for each ordering constraint, rather
      than only the bare sequence? [Traceability, Tasks Dependencies, Plan
      Implementation sequence]
- [ ] CHK024 Is it specified which exact commits (T027, T028) trigger the
      requirement for a final re-run, so a reader can determine from `git log`
      alone whether previously-recorded evidence is now stale? [Measurability,
      Tasks T029]
- [ ] CHK025 Is a disposition specified for a gate run captured at a head that
      is NEITHER the pre-edit baseline NOR the true final head — is that result
      labeled interim, discarded, or left ambiguous? [Gap, Tasks T029]

## Gate Failure Handling

- [ ] CHK026 Is a failing gate's consequence specified as a BLOCKER — halting
      the feature's progress — rather than as a finding to be noted and carried
      forward? [Ambiguity, Plan Risks table, Constitution Principle V]
- [ ] CHK027 Is the doc-health finding-set diff, specifically, called out as a
      case where ANY non-empty diff is a blocker, rather than a judgment call
      about whether the new findings are individually acceptable?
      [Measurability, Plan Risks table, Spec Edge Cases]
- [ ] CHK028 Is what "the feature stops" means operationally specified for a
      mid-sequence gate failure — does already-committed work get reverted, or
      does the branch simply not proceed past that point? [Gap, Plan Risks
      table]
- [ ] CHK029 Is a gate that FAILS distinguished, in the requirements, from a
      gate that CANNOT BE RUN at all (missing tool, wrong CLI resolved), or are
      both collapsed into the same undifferentiated "blocker" language?
      [Ambiguity, Tasks T002]

## Pre-Existing vs New Findings

- [ ] CHK030 Are pre-existing dispositioned exceptions distinguished from
      newly-introduced findings by a NUMBER — a count carried from the ratified
      baseline — rather than by a qualitative claim that "nothing new
      appeared"? [Measurability, Quickstart §1]
- [ ] CHK031 Is the ratified baseline's dispositioned-exception count itself
      named as a fixed reference value the branch's count must be compared
      against, so "unchanged" has a number on both sides of the comparison?
      [Traceability, Quickstart §1]
- [ ] CHK032 Is a disposition specified for the case where the branch's
      dispositioned-exception count is LOWER than the baseline (an exception
      resolved) versus HIGHER (a new one introduced) — are both, either, or
      neither treated as noteworthy? [Gap, Quickstart §1]
- [ ] CHK033 Is the doc-health "count that moved only because the document
      grew" rule (word totals, canon share) kept distinct from the
      dispositioned-exception count, so the two different "explain away a
      number" mechanisms are not conflated in the evidence record?
      [Consistency, Tasks T016, Quickstart §1]

## Environment Closure and Portability

- [ ] CHK034 Is it specified whether these gate results are expected to be
      captured and recorded ANYWHERE other than the dedicated scratchpad clone
      — i.e., is a gate result's validity scoped to the environment it was
      captured in? [Gap, Assumptions]
- [ ] CHK035 Is a requirement stated for the case where a gate is green in this
      local clone but would fail in a different environment (a CI runner, a
      fresh checkout without the pinned-CLI prefix set up) — is that
      possibility addressed anywhere, or is local-clone success treated as
      unconditionally sufficient evidence? [Gap, Assumptions]
- [ ] CHK036 Is the pinned CLI's own installation and availability (the
      `<scratchpad>/cli-pin-prefix` tree) treated as part of each gate's
      specified environment, so a result recorded without noting that prefix's
      provenance is an incomplete record? [Completeness, Assumptions, Quickstart
      §1]

## Notes

- **CHK034/CHK035** name a genuine, un-addressed gap: nothing in spec, plan,
  research or quickstart says whether a gate result captured only in this
  dedicated scratchpad clone is meant to be re-proven anywhere else (a CI
  runner, the lane's own checkout) before the archive act relies on it. The
  packet declares `code_surface: none`, so no CI workflow is implicated by
  this feature's own diff — but the requirements never say that explicitly,
  so the silence reads as an omission rather than a reasoned "not applicable."
- **CHK028** and **CHK025** are related gaps: the plan's risk table says a
  non-empty doc-health diff "is a blocker, not a note," but nothing in spec,
  plan or tasks says what a blocker DOES to work already committed on the
  branch, or how to label a gate run caught at an odd, non-final head.
