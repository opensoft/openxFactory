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
      quickstart? [Completeness, Spec Key Entities, Openspec tasks §4] **— OPEN:** spec.md's Key Entities "gate set" enumeration lists the pinned CLI, the sequenced-after/scope/manifest validators, doc-health and the pytest paths, but omits the §4.2 MODIFIED-block currency measurement that FR-012 and the packet's own §4 both treat as one of the five gates. **FIX:** Add "4.2's MODIFIED-block currency measurement" to spec.md's Key Entities gate-set bullet so it is closed against the packet's full §4.1--4.5.
- [x] CHK002 Is each gate's pass condition stated as a measurable predicate — an
      exit code, a count, a diff being empty — rather than as a general
      expectation such as "clean" or "green"? [Measurability, Spec SC-002,
      SC-004, SC-005]
- [x] CHK003 Is "zero undispositioned findings" for `--all --strict` defined, or
      at least distinguished from "zero findings", so "undispositioned" is not
      left as an unexplained term of art? [Ambiguity, Spec SC-002]
- [x] CHK004 Is the `--change` invocation's pass condition (passes outright)
      kept distinct from the `--all` invocation's pass condition (a specific
      finding count), so task 4.1's two runs are not conflated into one
      requirement? [Ambiguity, Quickstart §1, Openspec tasks §4.1]
- [x] CHK005 Is `--ledger-diff`'s expected output string ("per-change sweep
      ledger consistent with the corpus") specified as part of its pass
      condition, rather than only "exits 0"? [Measurability, Quickstart §2]
- [x] CHK006 Are the four validators of task 4.3 each given an independently
      statable pass condition, so satisfying the requirement cannot be done by
      running one and inferring the rest? [Coverage, Tasks T015]
- [x] CHK007 Is the pytest gate's pass condition specified as the captured
      summary line plus return code 0, rather than as "green" left undefined?
      [Measurability, Spec SC-005]

## Pinned CLI Discipline

- [ ] CHK008 Is "the pinned OpenSpec CLI 1.12.0, reached only through
      `scripts/validate-openspec-cli-pin.py`" stated as a MUST-level
      requirement, rather than as background describing the tooling in use?
      [Ambiguity, Plan Primary Dependencies, Assumptions] **— OPEN:** "The pinned OpenSpec CLI 1.12.0, reached only through validate-openspec-cli-pin.py" is stated only in Plan's Technical Context and the Assumptions section, never as a MUST-level FR in spec.md's Functional Requirements. **FIX:** Add a new FR requiring every gate invocation to use the pinned CLI via the PIN prefix and forbidding resolution of PATH's 1.2.0 (same fix as requirements.md CHK058).
- [x] CHK009 Is "PATH's 1.2.0 is never used" stated as a prohibition WITH a
      detection method (e.g., the `PATH="$PIN/bin:$PATH"` prefix present in
      every recorded invocation), rather than as an instruction with no way to
      check compliance after the fact? [Measurability, Quickstart §1,
      Assumptions]
- [x] CHK010 Is the environment needed to select the pinned CLI (the `PIN`
      prefix variable, `OPENSPEC_TELEMETRY=0`) specified as part of each gate's
      own definition, so "run the gate" is unambiguous about which binary
      answers? [Completeness, Quickstart §1]
- [ ] CHK011 Is a response specified for the case where
      `validate-openspec-cli-pin.py` itself is unavailable or resolves the
      wrong CLI version — is that a gate failure, or a setup precondition
      outside any gate's stated scope? [Gap, Quickstart §1] **— OPEN:** No requirement states the disposition if validate-openspec-cli-pin.py itself is unavailable or resolves the wrong CLI version, as distinct from the tool running and finding a violation. **FIX:** Add a clause to FR-020 (or the Risks table) naming "gate cannot be run at all" as its own blocker class, reported separately from a substantive finding.

## Baseline Timing for doc-health

- [x] CHK012 Is the doc-health comparison baseline specified as a `main`
      checkout, rather than left ambiguous between "main" and "the branch's own
      parent commit"? [Ambiguity, Spec SC-003, Quickstart §3]
- [x] CHK013 Is WHEN the baseline must be captured specified — before the
      `docs/document-lifecycle.md` edit lands on the branch — rather than left
      to be taken at whatever point the gate happens to run? [Measurability,
      Tasks T004]
- [ ] CHK014 Is the consequence of capturing the baseline AFTER the edit (rather
      than before) stated anywhere, so a reader understands why T004's ordering
      is load-bearing rather than a convenience? [Gap, Tasks T004] **— OPEN:** T004's rationale for capturing the doc-health baseline BEFORE the docs edit ("a fixed comparand") doesn't establish that capturing it after would actually differ, since the main baseline comes from an independent worktree/checkout unaffected by this branch's edits. **FIX:** Strengthen T004's rationale to state the real risk -- that `main` itself may advance during the feature's work, so capturing early anchors SC-003 to one fixed reference throughout -- or reclassify the ordering as a workflow convenience rather than a correctness requirement.
- [ ] CHK015 Is the baseline's own currency addressed — if `main` advances
      between when the baseline is captured and when the final-head diff is
      taken, is the baseline re-captured or is the original retained? [Gap,
      Tasks T004, Spec Edge Cases] **— OPEN:** Nothing states whether the doc-health baseline is re-captured if `main` advances between T004's capture and T029's final-head diff, or whether the original T004 snapshot is retained as the fixed comparand. **FIX:** Add a sentence to T004/T029 or the Edge Cases stating which -- retain the original snapshot, or re-capture a fresh `main` baseline at T029 -- and why.
- [ ] CHK016 Is the mechanism for obtaining the `main` checkout specified
      precisely enough that two readers would compare the branch against the
      same bytes (a named worktree or second checkout), rather than "whatever
      main looked like when I checked"? [Consistency, Quickstart §3] **— OPEN:** Quickstart §3 offers "a named worktree ... or a second clone" without pinning the reproduction to one exact `main` commit sha, so two readers running the recipe at different times would compare the branch against different bytes. **FIX:** Name the exact `main` commit sha the baseline must be taken at (recorded in the evidence file) rather than leaving "main" as a moving ref in the reproduction recipe.

## Idempotency and Re-Run Expectations

- [ ] CHK017 Is "running a gate twice at the same head yields the same result"
      stated as a general expectation of every gate in the set, or only
      demonstrated for the ledger seeder? [Coverage, Openspec tasks §0.1] **— OPEN:** No spec, plan or task states a general idempotency expectation ("every §4 gate, run twice at the same head, produces the same result") -- the only measured idempotency demonstration is for the ledger seeder (§0.1), a mutating tool rather than a gate. **FIX:** Add a sentence (to FR-011 or a new clause) stating every §4 gate is expected to produce identical output on repeated runs at the same head, since SC-002 through SC-005 rest on that assumption.
- [x] CHK018 Is the ledger seeder's no-op behavior for a provenance-only
      correction specified with its own measured evidence (the "184 rows, 0
      moved by #999" / zero-line-diff result), rather than asserted as a
      general property of the tool? [Measurability, Openspec tasks §0.1]
- [x] CHK019 Is it specified that this feature does NOT re-run the seeder —
      because the row's derived keys are already correct — as a rule
      distinguishing "a no-op if run" from "must not be run"? [Ambiguity,
      Openspec tasks §0.1, Spec FR-016]
- [ ] CHK020 Are idempotency expectations stated for the doc-health
      finding-set diff specifically — that running it twice at the same two
      heads (branch, main) produces the same diff — or is this left to be
      assumed from the tool's general behavior? [Gap, Tasks T016] **— OPEN:** No requirement states that the doc-health finding-set diff specifically is idempotent across repeated runs at the same two heads (branch, main) -- a specific instance of CHK017's general gap. **FIX:** Extend the CHK017 fix to name the doc-health diff explicitly as one gate requiring demonstrated same-head reproducibility.
- [x] CHK021 Is re-running the § 4 gate set at a NEW final head (task T029)
      kept distinct from re-running it AGAIN at the SAME head — i.e., is
      idempotency (same head, same result) kept separate from currency (new
      head, possibly different result)? [Ambiguity, Tasks T029]

## Gate Ordering Relative to Commits

- [x] CHK022 Is the rule that the FINAL gate run must cover every commit
      touching `openspec/changes/**` stated as a precondition for that run
      counting as valid evidence, rather than as a scheduling preference?
      [Measurability, Plan S6, Tasks T029]
- [x] CHK023 Is the dependency chain (doc edit → gate run → task ticks → final
      gate re-run) stated with the REASON for each ordering constraint, rather
      than only the bare sequence? [Traceability, Tasks Dependencies, Plan
      Implementation sequence]
- [x] CHK024 Is it specified which exact commits (T027, T028) trigger the
      requirement for a final re-run, so a reader can determine from `git log`
      alone whether previously-recorded evidence is now stale? [Measurability,
      Tasks T029]
- [x] CHK025 Is a disposition specified for a gate run captured at a head that
      is NEITHER the pre-edit baseline NOR the true final head — is that result
      labeled interim, discarded, or left ambiguous? [Gap, Tasks T029]

## Gate Failure Handling

- [x] CHK026 Is a failing gate's consequence specified as a BLOCKER — halting
      the feature's progress — rather than as a finding to be noted and carried
      forward? [Ambiguity, Plan Risks table, Constitution Principle V]
- [x] CHK027 Is the doc-health finding-set diff, specifically, called out as a
      case where ANY non-empty diff is a blocker, rather than a judgment call
      about whether the new findings are individually acceptable?
      [Measurability, Plan Risks table, Spec Edge Cases]
- [ ] CHK028 Is what "the feature stops" means operationally specified for a
      mid-sequence gate failure — does already-committed work get reverted, or
      does the branch simply not proceed past that point? [Gap, Plan Risks
      table] **— OPEN:** FR-020 states a failing gate halts forward progress ("no dependent task proceeds") but never says whether already-committed, prior-passing work is reverted or left standing. **FIX:** Add a sentence to FR-020 or FR-021 stating explicitly that already-committed work is NOT reverted on a later gate failure -- only forward progress halts, and the branch is handed to STOP (B) in its committed state.
- [ ] CHK029 Is a gate that FAILS distinguished, in the requirements, from a
      gate that CANNOT BE RUN at all (missing tool, wrong CLI resolved), or are
      both collapsed into the same undifferentiated "blocker" language?
      [Ambiguity, Tasks T002] **— OPEN:** No requirement distinguishes a gate that FAILS (ran, found a violation) from a gate that CANNOT BE RUN AT ALL (missing tool, wrong CLI resolved) -- both collapse into the same "blocker" language. **FIX:** Add a clause naming "gate cannot be run" as its own blocker class, distinct from and reported separately from a substantive failing result (same fix as CHK011).

## Pre-Existing vs New Findings

- [x] CHK030 Are pre-existing dispositioned exceptions distinguished from
      newly-introduced findings by a NUMBER — a count carried from the ratified
      baseline — rather than by a qualitative claim that "nothing new
      appeared"? [Measurability, Quickstart §1]
- [x] CHK031 Is the ratified baseline's dispositioned-exception count itself
      named as a fixed reference value the branch's count must be compared
      against, so "unchanged" has a number on both sides of the comparison?
      [Traceability, Quickstart §1]
- [x] CHK032 Is a disposition specified for the case where the branch's
      dispositioned-exception count is LOWER than the baseline (an exception
      resolved) versus HIGHER (a new one introduced) — are both, either, or
      neither treated as noteworthy? [Gap, Quickstart §1]
- [x] CHK033 Is the doc-health "count that moved only because the document
      grew" rule (word totals, canon share) kept distinct from the
      dispositioned-exception count, so the two different "explain away a
      number" mechanisms are not conflated in the evidence record?
      [Consistency, Tasks T016, Quickstart §1]

## Environment Closure and Portability

- [x] CHK034 Is it specified whether these gate results are expected to be
      captured and recorded ANYWHERE other than the dedicated scratchpad clone
      — i.e., is a gate result's validity scoped to the environment it was
      captured in? [Gap, Assumptions]
- [x] CHK035 Is a requirement stated for the case where a gate is green in this
      local clone but would fail in a different environment (a CI runner, a
      fresh checkout without the pinned-CLI prefix set up) — is that
      possibility addressed anywhere, or is local-clone success treated as
      unconditionally sufficient evidence? [Gap, Assumptions]
- [ ] CHK036 Is the pinned CLI's own installation and availability (the
      `<scratchpad>/cli-pin-prefix` tree) treated as part of each gate's
      specified environment, so a result recorded without noting that prefix's
      provenance is an incomplete record? [Completeness, Assumptions, Quickstart
      §1] **— OPEN:** Nothing requires the evidence file to record the pinned CLI's own installation/version provenance (e.g. `openspec --version` output) as part of each gate result; the pin-prefix's identity is assumed rather than captured. **FIX:** Add a clause to FR-011 or FR-013 requiring the evidence file to record the pinned CLI's resolved version/provenance alongside each gate's output.

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

## Evaluation — 2026-09-08

**Tally**: 25 passed / 11 open / 0 deferred (total 36).

### Open items
- CHK001 — spec.md's Key Entities "gate set" enumeration lists the pinned CLI, the sequenced-after/scope/manifest validators, doc-health and the pytest paths, but omits the §4.2 MODIFIED-block currency measurement that FR-012 and the packet's own §4 both treat as one of the five gates. → Add "4.2's MODIFIED-block currency measurement" to spec.md's Key Entities gate-set bullet so it is closed against the packet's full §4.1--4.5.
- CHK008 — "The pinned OpenSpec CLI 1.12.0, reached only through validate-openspec-cli-pin.py" is stated only in Plan's Technical Context and the Assumptions section, never as a MUST-level FR in spec.md's Functional Requirements. → Add a new FR requiring every gate invocation to use the pinned CLI via the PIN prefix and forbidding resolution of PATH's 1.2.0 (same fix as requirements.md CHK058).
- CHK011 — No requirement states the disposition if validate-openspec-cli-pin.py itself is unavailable or resolves the wrong CLI version, as distinct from the tool running and finding a violation. → Add a clause to FR-020 (or the Risks table) naming "gate cannot be run at all" as its own blocker class, reported separately from a substantive finding.
- CHK014 — T004's rationale for capturing the doc-health baseline BEFORE the docs edit ("a fixed comparand") doesn't establish that capturing it after would actually differ, since the main baseline comes from an independent worktree/checkout unaffected by this branch's edits. → Strengthen T004's rationale to state the real risk -- that `main` itself may advance during the feature's work, so capturing early anchors SC-003 to one fixed reference throughout -- or reclassify the ordering as a workflow convenience rather than a correctness requirement.
- CHK015 — Nothing states whether the doc-health baseline is re-captured if `main` advances between T004's capture and T029's final-head diff, or whether the original T004 snapshot is retained as the fixed comparand. → Add a sentence to T004/T029 or the Edge Cases stating which -- retain the original snapshot, or re-capture a fresh `main` baseline at T029 -- and why.
- CHK016 — Quickstart §3 offers "a named worktree ... or a second clone" without pinning the reproduction to one exact `main` commit sha, so two readers running the recipe at different times would compare the branch against different bytes. → Name the exact `main` commit sha the baseline must be taken at (recorded in the evidence file) rather than leaving "main" as a moving ref in the reproduction recipe.
- CHK017 — No spec, plan or task states a general idempotency expectation ("every §4 gate, run twice at the same head, produces the same result") -- the only measured idempotency demonstration is for the ledger seeder (§0.1), a mutating tool rather than a gate. → Add a sentence (to FR-011 or a new clause) stating every §4 gate is expected to produce identical output on repeated runs at the same head, since SC-002 through SC-005 rest on that assumption.
- CHK020 — No requirement states that the doc-health finding-set diff specifically is idempotent across repeated runs at the same two heads (branch, main) -- a specific instance of CHK017's general gap. → Extend the CHK017 fix to name the doc-health diff explicitly as one gate requiring demonstrated same-head reproducibility.
- CHK028 — FR-020 states a failing gate halts forward progress ("no dependent task proceeds") but never says whether already-committed, prior-passing work is reverted or left standing. → Add a sentence to FR-020 or FR-021 stating explicitly that already-committed work is NOT reverted on a later gate failure -- only forward progress halts, and the branch is handed to STOP (B) in its committed state.
- CHK029 — No requirement distinguishes a gate that FAILS (ran, found a violation) from a gate that CANNOT BE RUN AT ALL (missing tool, wrong CLI resolved) -- both collapse into the same "blocker" language. → Add a clause naming "gate cannot be run" as its own blocker class, distinct from and reported separately from a substantive failing result (same fix as CHK011).
- CHK036 — Nothing requires the evidence file to record the pinned CLI's own installation/version provenance (e.g. `openspec --version` output) as part of each gate result; the pin-prefix's identity is assumed rather than captured. → Add a clause to FR-011 or FR-013 requiring the evidence file to record the pinned CLI's resolved version/provenance alongside each gate's output.
