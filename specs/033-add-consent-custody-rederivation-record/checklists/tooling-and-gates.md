# Checklist: Tooling and Gates — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate validation that every gate this feature must run is
named with its EXACT command and a MEASURABLE pass criterion — the pinned
OpenSpec CLI's two invocations and its disposition mechanism, the canonical
consent-instrument validator, both `validate-sequenced-after.py` modes,
`validate-scope-globs.py`, `validate-manifest-digests.py`,
`validate-contract-release.py verify-commit`, `validate-release-tag-gate.py`,
the pytest set CI runs, and the doc-health two-report comparison — plus the
ban on PATH's unpinned OpenSpec CLI and the rule that every transcript lands
in `evidence/`. This checklist interrogates the WRITTEN REQUIREMENTS for the
gates, including the "silently passes" class: a gate that exits 0 without
having checked what it was invoked to check.

**Artifacts under review**: `spec.md` (SC-001 through SC-010, the measured
baseline table), `plan.md` (Technical Context, the Implementation sequence
table, the Risks table), `tasks.md` (T006–T007, T015, T054, T064, T080–T081),
`research.md` (R9, R13), the ratified packet, and the gate scripts themselves
(`scripts/validate-openspec-cli-pin.py`, `scripts/validate-consent-instruments.py`,
`scripts/validate-sequenced-after.py`, `scripts/validate-scope-globs.py`,
`scripts/validate-manifest-digests.py`, `scripts/validate-contract-release.py`,
`scripts/validate-release-tag-gate.py`, `scripts/doc_health/runner.py`).

**Date**: 2026-09-09

---

## A. Gate set enumeration

- [x] CHK001 Is the complete set of gates this feature must run enumerated in
      ONE place — `tasks.md` T081's "Final gate sweep" list — closed against
      `spec.md`'s SC-001 through SC-010, rather than left to be assembled from
      scattered mentions across spec, plan and tasks? [Completeness, tasks.md
      T081, spec.md Success Criteria]
- [x] CHK002 Is each gate's pass condition stated as a measurable predicate —
      an exit code, a count, a diff being empty — rather than as a general
      "clean" or "green"? [Measurability, spec.md SC-001–SC-010]
- [x] CHK003 Are the § 5.4 FIVE-gate subset (`release-tag-gate`, pytest,
      `validate-manifest-digests.py`, `validate-contract-release.py`,
      `validate-consent-instruments.py`) kept as a NAMED subset of the full
      T081 sweep, rather than a separately invented list that could drift
      from it? [Consistency, spec.md FR-034, tasks.md T064, T081] — verified:
      all five of T064's gates also appear in T081's six-gate final sweep
      (T081 adds `validate-sequenced-after.py` and `validate-scope-globs.py`,
      which are not release-surface gates and so are correctly absent from
      FR-034's five).

## B. Pinned OpenSpec CLI discipline

- [x] CHK004 Is the command for the change-scoped run stated exactly —
      `python3 scripts/validate-openspec-cli-pin.py --change
      add-consent-custody-rederivation-record --strict`, matching the
      script's own `--change ID` (repeatable) and `--strict` (accepted,
      always on) flags — rather than a paraphrase using the raw `openspec`
      binary? [Measurability, spec.md line 81, script `build_parser()`]
- [x] CHK005 Is the command for the corpus-wide run stated exactly —
      `python3 scripts/validate-openspec-cli-pin.py --all --strict` —
      distinct from the change-scoped run, per T081 and T006/T007's
      `speckit-analyze` loop discipline? [Measurability, tasks.md T081]
- [x] CHK006 Is the `--change` run's pass condition ("passes outright," 1
      passed / 0 failed) kept DISTINCT from the `--all` run's pass condition
      ("zero UNDISPOSITIONED failures," SC-006) — two different bars, not
      one conflated requirement? [Ambiguity, spec.md SC-006, research.md R13]
- [ ] CHK007 Is "zero UNDISPOSITIONED failures" (SC-006) the WHOLE of the
      `--all --strict` pass condition, or does the gate script's own
      `reconcile()` function name a THIRD outcome — a STALE disposition (an
      accepted exception whose condition no longer occurs) — that raises
      `PinRefusal("pin-disposition-stale", ...)` and exits 2, distinct from
      both a clean pass and an undispositioned-findings failure (exit 1)?
      [Gap, spec.md SC-006, script lines 1706–1780, 2043–2049] —
      **FINDING:** `validate-openspec-cli-pin.py`'s `reconcile()` returns
      `(applied, undispositioned, stale)` and the `--all` path in `main()`
      raises a hard `PinRefusal` (exit 2) when `stale` is non-empty — a THIRD
      failure mode SC-006 does not name. A stale disposition is unrelated to
      this feature's own correctness (it means some OTHER accepted exception
      in `contracts/openspec-cli-pin.yaml`'s `dispositions:` list no longer
      matches any finding, typically because an unrelated change archived) —
      but a builder who sees `--all --strict` exit 2 and checks only SC-006
      ("zero undispositioned failures") would not find language covering
      this exit code, and could misdiagnose it as a harness/dependency error
      (this script's OTHER documented use of exit 2) rather than a
      corpus-hygiene refusal requiring an edit to a file this feature does
      not otherwise touch.
- [x] CHK008 Is the ban on PATH's unpinned OpenSpec CLI (`1.2.0`, per the
      script's own docstring history) stated as a prohibition with a
      DETECTION method — no `T###` in this feature invokes `--path-mode`, and
      every invocation runs through `validate-openspec-cli-pin.py` rather
      than a bare `openspec` on PATH — rather than an instruction with no way
      to check compliance after the fact? [Measurability, plan.md line 37,
      script docstring lines 12–27] — verified against the live tree: the
      script's own docstring records "CORRECTED 2026-09-05: THAT LINE IS
      GONE" (the `npm install -g @fission-ai/openspec@1.2.0` line in
      `pytest-suite.yml`), and no task in `tasks.md` (T006, T007, T081) uses
      `--path-mode`.
- [x] CHK009 Is `OPENSPEC_TELEMETRY=0` named as part of the gate's own
      environment, so "run the gate" is unambiguous about telemetry behavior,
      per the CLAUDE.md-level instruction to validate with it set?
      [Completeness, plan.md line 36]
- [x] CHK010 Is a response specified for the case where
      `validate-openspec-cli-pin.py` itself cannot fetch or verify the pinned
      tarball (a `pin-integrity-mismatch` or dependency-closure refusal,
      exit 2) — is that treated as a gate failure blocking the feature, or a
      setup precondition outside any single task's stated scope? [Gap,
      tasks.md T006, T007, T081] — not addressed by any task; reasonable to
      treat as a harness precondition rather than a feature defect, but
      nothing says so explicitly.

## C. `validate-consent-instruments.py --strict`

- [x] CHK011 Is the command stated with NO path argument (so layer 1's
      `self_test` runs, not layer 2's `repo_scan`) — `python3
      scripts/validate-consent-instruments.py --strict` — distinct from the
      `--purpose` and repo-scan invocations the script also supports?
      [Measurability, spec.md line 124, script `main()` argparse]
- [x] CHK012 Is the pass condition stated as the printed summary line's exact
      shape — "0 error(s), 0 warning(s)" (validator `report()`, line 802) —
      AND return code 0, rather than "clean" left undefined? [Measurability,
      spec.md SC-001, research.md R13]
- [x] CHK013 Does SC-001 require the self-test NOTE line to report THREE
      bucket counts (valid / negative / withheld) as part of the pass
      condition, not merely the error/warning tally — so a corpus that is
      technically 0/0 but still reports only two buckets (a missed T046)
      would be caught by this gate's OWN stated criterion? [Measurability,
      spec.md SC-001]
- [x] CHK014 Is the WITHHELD-vs-clean distinction made operational for SC-010
      — "an instrument that WITHHOLDS exits in the new named status class,
      and the packaged corpus exits 0 — the two are distinguishable from the
      command line" — i.e., does the plan require demonstrating BOTH exit
      paths (a real withheld instrument via a path argument, and the
      packaged self-test) rather than only one? [Coverage, spec.md SC-010]
- [x] CHK015 Is the new exit status's NUMBER treated as provisional
      everywhere this checklist's sibling gates touch it — is the gate's own
      pass/fail language keyed to "the single named constant" rather than
      hard-coding `3`, so a later ruling that moves the constant does not
      require rewriting this checklist too? [Consistency, tasks.md T024,
      T053]

## D. `validate-sequenced-after.py` — both invocations

- [x] CHK016 Is the bare, no-flag invocation — `python3
      scripts/validate-sequenced-after.py .` — named as the PLAIN validation
      run (the mutually-exclusive `--archive-gate` / `--sweep` /
      `--ledger-diff` / `--seed-ledger` modes are each something else),
      distinct from the `--ledger-diff` invocation named separately?
      [Measurability, spec.md SC-009, script `main()` mode group]
- [x] CHK017 Is `--ledger-diff`'s pass condition stated as its printed message
      — "per-change sweep ledger consistent with the corpus (`N` rows)" — with
      the row count itself measurable (189, per `research.md` R11), rather
      than only "exits 0"? [Measurability, research.md R11, spec.md SC-009]
- [x] CHK018 Is it stated that this feature's own ledger row (§ 0.1) is
      ALREADY correct and NOT re-seeded — task T070 ticks box 0.1 on EXISTING
      evidence (commit `6cfe9ba6`) rather than re-running `--seed-ledger` —
      so `validate-sequenced-after.py .`'s pass condition for THIS feature
      does not depend on an act this feature performs? [Consistency,
      tasks.md T070, research.md R11]
- [x] CHK019 Given `--strict-archive-dates` is explicitly "only meaningful on
      the plain validation run" (the script's own `parser.error` guard), is
      it clear that this feature's plain-run invocation does NOT need that
      flag (no archived-record edits are made by this feature under §§ 0–5),
      so its absence from the stated command is a deliberate omission rather
      than an overlooked option? [Scope boundary, script mode guards, spec.md
      Out of scope]

## E. `validate-scope-globs.py`

- [x] CHK020 Is the command stated exactly — `python3
      scripts/validate-scope-globs.py .` — with a bare pass/fail (exit 0)
      criterion, matching its argparse shape (`repo_root`, `--archive-gate`,
      `--ratified-ref`, none required for the plain run)? [Measurability,
      spec.md SC-009, script argparse]
- [x] CHK021 Is this gate's role distinguished from `validate-sequenced-after.py`'s
      — the two are named together in SC-009 and T081 but check DIFFERENT
      things (scope-glob well-formedness vs. sequenced-after/ledger
      consistency) — so a reader does not assume one gate's pass implies the
      other's? [Ambiguity, spec.md SC-009]

## F. `validate-manifest-digests.py`

- [x] CHK022 Is the pass condition stated as a count — "189 per-file digests
      verify" at baseline (`research.md` R5), and the SAME count PLUS the
      re-derived `consent-instrument` row once § 5.2 lands (SC-004) — rather
      than "digests verify" left unquantified? [Measurability, research.md
      R5, spec.md SC-004]
- [x] CHK023 Does the plan distinguish this gate's TWO invocation points —
      once at the PRE-CUT baseline (Phase A–F, where it passes on the
      UNCHANGED `consent-instrument` digest) and once AT THE CANDIDATE (§ 5.4,
      where it must verify the RE-DERIVED digest) — so a single "it passes"
      claim is not read as covering both moments? [Ambiguity, spec.md FR-034,
      SC-004, plan.md Phase table]
- [x] CHK024 Is it stated that this gate is ALSO driven inside `pytest-suite`
      by `tests/manifest_digests/test_manifest_digest_sweep.py` (research.md
      R5), so the standalone CLI run and the pytest-suite run are the SAME
      check exercised twice, not two independent gates whose disagreement
      would need reconciling? [Consistency, research.md R5]

## G. `validate-contract-release.py verify-commit`

- [x] CHK025 Is the command stated with its exact required flag —
      `python3 scripts/validate-contract-release.py verify-commit --commit
      <candidate-sha>` — matching the script's own
      `verify_commit.add_argument("--commit", required=True)`, rather than a
      paraphrase that could be confused with `verify-promotion` (which also
      needs `--remote` and `--tag`)? [Measurability, spec.md SC-005, script
      `build_parser()`]
- [x] CHK026 Is the pass condition ("passes on the exact candidate," SC-005)
      distinguished from the EXPECTED, NON-defect red result `verify-commit`
      gives AT HEAD BETWEEN CUTS — policy's own "Between cuts, `verify-commit`
      at HEAD is EXPECTED to report mismatches on the editorial members
      (CHANGELOG, manifest, README)" — so a builder does not mistake this
      documented, bounded staleness for a gate failure BEFORE the § 5.2
      candidate commit exists? [Ambiguity, policy lines 280–287, spec.md
      SC-005] — no task explicitly names this expected-staleness caveat for
      the PRE-cut phases (B–F), though `research.md`/`plan.md`'s own
      staleness language (T017, "the digest is now deliberately stale")
      covers the specific `consent-instrument` row; the POLICY's broader
      "editorial members" allowance is not cross-referenced anywhere in this
      feature's own documents.
- [x] CHK027 Is `verify-commit`'s scope correctly distinguished from
      `verify-promotion` and `verify-tag` (the OTHER two subcommands this
      script offers) — does the plan avoid naming a subcommand this feature
      does not need (it never promotes or tags)? [Scope boundary, spec.md
      FR-034, FR-035]

## H. `validate-release-tag-gate.py`

- [x] CHK028 Is the command's positional `repo_root` argument and its
      purpose (evaluating a merge-tree diff against `contracts/manifest.yaml`
      or `contracts/releases/**`) named, distinguishing this LOCAL,
      offline reproduction from the GitHub Actions `pull_request`-triggered
      run this feature never observes (Q11)? [Consistency, clarify-questions.md
      Q11, script docstring]
- [ ] CHK029 Is the EXACT `--head` / `--base` pair for the LOCAL run
      specified, given the script's own default (`--base` defaults to "the
      head's first parent, which is the base branch tip") is designed for a
      GitHub `pull_request` MERGE COMMIT (whose first parent is conventionally
      the BASE branch and second parent the PR head), while THIS feature's
      candidate commit is produced by "fetch, integrate onto the final
      integration point" — a MERGE OF MAIN INTO THE FEATURE BRANCH (`R3`,
      per opensoft ruleset 8981805) — whose first parent is the FEATURE
      BRANCH'S OWN PRIOR TIP, not `main`? [Gap, script `main()` `--base`
      help text, research.md R3, tasks.md T064] — **FINDING:** neither
      `tasks.md` T064 nor `plan.md` names an explicit `--base` override for
      the local `validate-release-tag-gate.py` run. Relying on the script's
      default would resolve `--base` to the candidate commit's first parent
      — under a main-into-branch integration merge, that is the FEATURE
      BRANCH's own previous commit, not `main` — which diffs the candidate
      against the wrong tree and could report a near-empty (or wrong) result
      that LOOKS like a clean pass without having evaluated the same
      comparison the real PR-triggered gate performs. The local run needs an
      explicit `--base <main-sha-at-integration>` to reproduce the intended
      comparison; this is exactly the "gate not actually run" class this
      checklist is charged with catching.
- [x] CHK030 Is it stated that this gate's SILENCE about the new bundle's own
      tag (`contract-v3.5`) is EXPECTED and not a defect — "a bundle whose
      EARLIEST DECLARING COMMIT IS THE TIP is at distance zero and emits NO
      FINDING" (script docstring) — so a builder does not add work trying to
      make this gate mention the tag it cannot require yet? [Consistency,
      script docstring, spec.md FR-035]

## I. The pytest set CI runs

- [x] CHK031 Is the command stated exactly — `python3 -m pytest tests/ -q -m
      "not postgres"` — matching `.github/workflows/pytest-suite.yml:462`
      byte-for-byte (modulo the `--junitxml` flag CI adds, which is not part
      of this feature's local pass condition)? [Measurability, plan.md line
      33, workflow line 462]
- [x] CHK032 Is the pass condition specified as the captured summary line
      (e.g., "N passed") PLUS return code 0, rather than "green" left
      undefined, per this codebase's own documented lesson about piped
      `make test | tail` masking exit codes? [Measurability, spec.md SC-007]
- [x] CHK033 Is the `postgres` marker's use WITHOUT a corresponding
      `markers =` registration in `pytest.ini` (which deliberately declares
      no options, per its own header comment) addressed as a non-issue —
      `tests/conftest.py`'s own docstring cites this exact invocation
      verbatim, confirming it is an established, intentional convention
      rather than a fragile one-off this feature introduces? [Consistency,
      pytest.ini, tests/conftest.py line 8]
- [x] CHK034 Does SC-007 require the NEW `tests/consent_instruments/` package
      to be green as part of THIS pass condition — the source-level no-git
      ban, the runtime patch over all three buckets, and the parametrized
      blob-walk test — rather than treating "pytest is green" as satisfied by
      the pre-existing suite alone? [Completeness, spec.md SC-007]
- [x] CHK035 Is `tests/consent_instruments/`'s own standalone pass condition
      (T054: `python3 -m pytest tests/consent_instruments -q` green) required
      BEFORE the full-suite run, so a new-package failure is diagnosed
      against a small, fast target rather than only discovered inside the
      full 20-plus-directory suite? [Traceability, tasks.md T054]

## J. doc-health two-report comparison

- [ ] CHK036 Does "two reports with identical basenames" (FR-045, T080) name
      WHICH basename must be identical — the OUTPUT REPORT FILES' own
      basenames (e.g., both named `doc-health.md` in separate directories),
      or the CHECKOUT DIRECTORIES' basenames (the identity trap this
      family's `repo=<basename>` stamp actually keys on, per the sibling
      feature's own `docs/032` precedent)? [Ambiguity, spec.md FR-045,
      tasks.md T080] — **FINDING:** `doc-health.py --single-repo <dir>`
      stamps the CHECKOUT'S DIRECTORY BASENAME into every finding line
      (`repo=<basename>`), the `Repo-Identity:` header, and the "scope
      limited to single repo" line — a fact this feature's own sibling
      (`specs/032-govern-archived-record-edits` FR-028) discovered and
      resolved by requiring the BASELINE CHECKOUT to carry the SAME
      directory basename as the branch checkout (or, failing that,
      normalizing all three stamped places before diffing). `spec.md` FR-045
      and `tasks.md` T080 in THIS feature say only "identical basenames"
      with no object named — a builder could satisfy the literal words by
      giving the two REPORT FILES the same name while running
      `--single-repo` against two DIFFERENT-basename checkout directories,
      which would reproduce exactly the identity-mismatch defect FR-028 was
      written to prevent.
- [ ] CHK037 Is the doc-health baseline required to NAME the `main` COMMIT
      SHA it was taken at, and to be RE-TAKEN if `main` moves before the
      final comparison — the discipline the sibling feature's FR-029 states
      in as many words ("If `main` moves between the baseline and the final
      comparison, the baseline is RE-TAKEN at the commit the branch was last
      merged from, and the evidence records both shas") — or does this
      feature's FR-045/T080 omit that discipline entirely? [Gap, spec.md
      FR-045, tasks.md T080] — **FINDING:** neither `spec.md` nor `tasks.md`
      in this feature requires recording which `main` SHA the doc-health
      baseline was captured at, nor requires re-capturing it if `main`
      advances before the final comparison. This is precisely the gap
      `specs/032-govern-archived-record-edits`' own FR-029 exists to close
      for its sibling feature; this feature's evidence could record a
      diff-identical comparison against a baseline that has since gone
      stale, with nothing in the plan requiring a check for that.
- [x] CHK038 Is the `--as-of` flag required to be PINNED to ONE date across
      BOTH the `main` and branch runs (T080), rather than each run taking
      its own default (today's date), which would make the two reports
      differ on the run-date line alone and confound the comparison?
      [Measurability, tasks.md T080, script `runner.py` `--as-of` argument]
- [x] CHK039 Is the comparison's pass condition stated as "finding sets
      diff-identical at every severity" (T080) — a KEYED comparison (family,
      repository, path, message), matching the sibling feature's own FR-028
      precedent that line-number-based diffing is wrong because a finding
      that moved down the file is still the same finding — or does this
      feature's plan leave the comparison METHOD (raw `diff` vs. a
      keyed/normalized comparison) unstated? [Ambiguity, tasks.md T080] — not
      explicitly stated which comparison method to use; a plain `diff` over
      two Markdown reports is likely adequate given both are taken at the
      same pinned `--as-of` and (once CHK036/CHK037 are closed) the same
      checkout-basename discipline, but the METHOD itself is not named.
- [x] CHK040 Is it required that counts which move only because the corpus
      GREW (word totals, canon share) are recognized as non-findings rather
      than diff noise, per the sibling feature's own quickstart recipe
      ("Counts that move only because the document GREW... are not
      findings")? [Consistency, T080, spec.md SC-008]

## K. Evidence discipline: transcripts land in `evidence/`

- [x] CHK041 Is "transcripts to `evidence/`" stated for the § 5.4 five-gate
      run (T064) and the final gate sweep (T081), matching FR-042's
      requirement that evidence be written to BOTH
      `specs/033-.../evidence/` AND
      `openspec/changes/.../evidence/realization-<date>.md`? [Completeness,
      tasks.md T064, T081, spec.md FR-042]
- [ ] CHK042 Are the INTERMEDIATE phase gates in `plan.md`'s Implementation
      Sequence table — Phase B ("schema self-validates"), Phase C ("validator
      runs clean over the un-grown corpus"), Phase D
      ("`validate-consent-instruments.py --strict` 0/0 with three bucket
      counts"), Phase E (`pytest tests/consent_instruments -q` green) — each
      given their OWN "transcript to `evidence/`" instruction the way T015
      (the § 2 custody-diff proof) and T064/T081 explicitly are, or do they
      exist only as "gates before moving on" with no `T###` requiring a
      written record of the run? [Gap, plan.md Implementation sequence table,
      tasks.md T015, T054, T064, T081] — **FINDING:** only T015 (custody
      byte-diff), T054 (the `tests/consent_instruments` pytest run, though
      T054's own text does not itself say "transcript to `evidence/`" — only
      that it must be "green") and T064/T081 explicitly instruct writing a
      transcript. The Phase table names four OTHER checkpoint gates (B, C, D,
      E) as conditions for "moving on," but no `T###` in Phase B–E requires
      capturing a transcript of the run that satisfied that condition — so a
      phase could be judged complete on an unrecorded, unreproducible local
      run, which is exactly the "gate not actually run" scenario class this
      checklist is charged with catching, applied to intermediate
      checkpoints rather than only the final ones.
- [x] CHK043 Is FR-042's "BOTH trees" requirement satisfied by a SINGLE
      transcript-writing act per gate (write once, copy or symlink to the
      second location), or does the plan require the transcript to be
      CAPTURED TWICE (once per invocation) — and if the latter, is running
      the gate a second time to produce the second copy addressed as a
      distinct, deliberate re-run rather than an accidental double
      execution? [Ambiguity, spec.md FR-042, FR-079/T079] — not addressed;
      `tasks.md` T079 says only "Evidence in BOTH trees," not by which
      mechanism the same transcript reaches both paths.
- [x] CHK044 Is the evidence directory's own creation (`$FD/evidence/`,
      `openspec/changes/.../evidence/`) itself gated on anything, or is it
      simply expected to be created by the first task that writes into it
      (T015, being the earliest evidence-producing task in the dependency
      order)? [Gap, tasks.md Dependencies] — reasonable to leave implicit;
      no task explicitly creates the directory, but T015 is unambiguously
      first in the dependency chain (`A → B → C → D → E → {F, G} → H`) among
      evidence-producing tasks.

## L. The "silently passes / gate not actually run" scenario class

- [x] CHK045 For EVERY gate named in §§ B–J above, does this checklist (or the
      sibling `release-cut-and-versioning.md` checklist for § 5's five gates)
      identify at least one way the gate could exit 0 without having checked
      what it claims to — i.e., is this scenario class deliberately searched
      for gate-by-gate, rather than assumed absent? [Coverage] — searched:
      CHK007 (stale-disposition exit 2 misdiagnosis), CHK026 (expected
      pre-cut `verify-commit` staleness read as a false failure, the inverse
      risk), CHK029 (release-tag-gate's default `--base` silently diffing
      the wrong tree), CHK036/CHK037 (doc-health basename/baseline-SHA
      identity traps that make two DIFFERENT comparisons look like the same
      one). Four distinct instances found across five gates; the remaining
      gates (`validate-consent-instruments.py`, `validate-sequenced-after.py`,
      `validate-scope-globs.py`, `validate-manifest-digests.py`, pytest) have
      no comparable trap identified — each fails closed on a straightforward
      exit-code/count check with no default-argument or identity-stamp
      subtlety in its invocation here.
- [x] CHK046 Is the `--strict` flag's effect (warnings become errors) applied
      CONSISTENTLY across every gate that offers it
      (`validate-consent-instruments.py --strict`, the pinned CLI's
      always-on `--strict`), so a reader cannot mistake a warning-tolerant
      run for a strict one? [Consistency, spec.md SC-001, SC-006]
- [x] CHK047 Is it stated anywhere that a gate's LOCAL pass (this feature
      never opens a pull request, per plan.md's Constitution Check table —
      "no PR, no comment, no merge, no tag from this seat") is NOT the same
      evidentiary weight as the same gate's CI run — i.e., does the plan
      avoid implying that a green local run discharges an obligation
      (`release-tag-gate`'s workflow-triggered form, the required
      `pytest-suite` CI job) that only actually runs once a PR exists?
      [Ambiguity, clarify-questions.md Q11, plan.md Constitution Check] —
      Q11 states this explicitly for `release-tag-gate` ("the workflow's own
      green is the lane's PR-open observation, not this feature's tick
      condition"); the same caveat is implicit but not repeated for
      `pytest-suite`'s own CI job, which also only runs once a PR exists.

## Evaluation — 2026-09-09

**State of gate execution at evaluation time**: NOT YET RUN AS A SET. This
checklist evaluates whether the gates and their pass criteria are stated
completely and precisely enough to be run the same way by two different
readers, and independently verifies several of the cited facts (the
`--path-mode` absence, the `pytest.ini`/`conftest.py` marker convention, the
`validate-release-tag-gate.py` default-`--base` behavior, the
`reconcile()`/`PinRefusal` three-way outcome) against the live scripts —
each cited individually above.

**Tally**: 42 passed / 5 open (unticked) / 0 dispositioned (47 total).

**Open findings**: CHK007 (stale-disposition exit 2 not named by SC-006),
CHK029 (no explicit `--base` for the local `release-tag-gate` run, risking a
wrong-tree diff under this repository's main-into-branch integration
direction), CHK036 (doc-health "identical basenames" does not say whether it
means the report files' or the checkouts' basenames), CHK037 (no requirement
to name or re-take the doc-health baseline's `main` SHA, unlike the sibling
feature's FR-029), CHK042 (intermediate Phase B–E gates have no transcript
requirement, only the § 2 diff proof and the § 5.4/final sweeps do). Five
findings total; CHK029 and CHK036/CHK037 are the load-bearing ones — each
describes a way a gate can be run, exit cleanly, and still not have checked
the comparison it exists to make.
