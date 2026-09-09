# Checklist: Evidence and Traceability — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate audit of the evidentiary chain this feature plans
to produce and the chain it has already produced in the Speckit tree —
whether evidence lands in BOTH trees, whether a box is ticked in the same
commit as its evidence or in neither, whether every gate transcript is
present and named, whether the doc-health two-report comparison is
correctly specified, whether every measured figure in `spec.md`/`research.md`
carries the command that produced it, whether every claim in any artifact is
backed by a measurement or a citation, and whether each of the ratified
delta's 22 scenarios traces to a `T###` task. This interrogates the WRITTEN
plan for evidence and the CURRENT truth of every figure already asserted —
no gate transcript yet exists (§§ 2–5 are unrealized), so items about future
transcripts are requirements-quality checks; items about figures already
stated in `spec.md`/`research.md` are re-measured against the live tree.

**Artifacts under review**: `spec.md`, `plan.md`, `tasks.md`, `research.md`
(Speckit tree); the ratified delta
(`openspec/changes/add-consent-custody-rederivation-record/specs/consent-instrument/spec.md`);
the packet's `tasks.md`; `contracts/manifest.yaml`; `contracts/releases/`;
`examples/consent-instrument/`; `docs/contract-versioning-policy.md`.

**Date**: 2026-09-09. No-argument invocation — maximum coverage, no item cap.

## Dual-Tree Evidence Homing

- [x] CHK001 Is the evidence home specified as BOTH
      `specs/033-add-consent-custody-rederivation-record/evidence/` AND
      `openspec/changes/add-consent-custody-rederivation-record/evidence/realization-2026-09-09.md`,
      rather than either alone? MEASURED: FR-042 names both paths explicitly,
      and `plan.md`'s Project Structure and Repository-files lists repeat
      both. [Completeness, spec.md FR-042, plan.md]
- [x] CHK002 Is the packet-side evidence file's exact name specified
      (`realization-2026-09-09.md`, matching the branch's creation date), not
      left as an open-ended "an evidence file"? [Precision, spec.md FR-042,
      plan.md Repository files list]
- [x] CHK003 Is it stated which tree is the WORKING evidence home for
      per-task transcripts (`specs/.../evidence/`) versus which is the
      SUMMARY home for the packet's own record (`openspec/.../evidence/realization-2026-09-09.md`),
      or could an implementer write everything into only one and technically
      satisfy a loose reading of FR-042? [Ambiguity, spec.md FR-042]
- [x] CHK004 Is task T079 traceable to FR-042 by explicit architect-ruling
      citation (Q4), so a reader of `tasks.md` alone knows WHY dual-homing is
      required rather than treating it as an arbitrary duplication?
      [Traceability, tasks.md T079]

## Commit/Tick Coupling — Same Commit as Its Evidence, or Neither

- [x] CHK005 Is "a box MUST be ticked in the same commit as its evidence, or
      in neither" (FR-041) stated as a rule about COMMIT boundaries rather
      than about ordering within a working tree? [Ambiguity, spec.md FR-041]
- [ ] CHK006 Is a verification method named for FR-041 — inspectable from
      `git log`/`git show` after the fact — rather than left to depend on the
      author's own account of the order events happened in? MEASURED: no
      task explicitly names a post-hoc `git log` verification step for
      FR-041 the way the sibling feature's checklist required one (compare
      `specs/032-govern-archived-record-edits/checklists/evidence-and-traceability.md`
      CHK015's closure). — **FINDING:** neither `tasks.md` nor `plan.md`
      names a post-hoc commit-history check that verifies, after all ticks
      land, that no tick's commit precedes the commit that recorded its
      evidence; the discipline relies on author care at commit time only.
      [Gap, spec.md FR-041]
- [x] CHK007 Is FR-041 read consistently with FR-042 (evidence is a WRITTEN
      artifact created at tick time) so that ticking box 0.1 or 1.1–1.3 in a
      commit later than the underlying act's own historical commit
      (`6cfe9ba6`, or the ratification record's commit) does not itself
      violate FR-041? [Consistency, spec.md FR-041/FR-042]
- [x] CHK008 Does FR-041's rule apply uniformly to EVERY box in §§ 2–5
      (schema, validator, fixtures, cut), or only to the bookkeeping boxes of
      §§ 0–1 — and is that scope stated rather than assumed? [Clarity,
      spec.md FR-041, tasks.md Phase B-H structure]

## Gate Transcript Completeness and Naming

- [x] CHK009 Are the FIVE gates FR-034 requires against the exact unchanged
      candidate (`release-tag-gate`/`validate-release-tag-gate.py`; the
      pytest set CI runs; `validate-manifest-digests.py`;
      `validate-contract-release.py`; `validate-consent-instruments.py`)
      named identically in `tasks.md` T064? MEASURED: T064 lists the same
      five, verbatim command names. [Consistency, spec.md FR-034, tasks.md
      T064]
- [x] CHK010 Is each of the five gates' transcript required to be a
      SEPARATELY named file under `evidence/`, so no gate's result can be
      inferred from another's absence of complaint? [Coverage, tasks.md T064]
- [ ] CHK011 Does the FINAL branch-head gate sweep (T081 — pinned CLI,
      `validate-consent-instruments.py --strict`,
      `validate-sequenced-after.py`/`--ledger-diff`, `validate-scope-globs.py`,
      `validate-manifest-digests.py`, `pytest`) include EVERY gate T064 ran
      against the candidate, or does it silently drop `release-tag-gate`/
      `validate-release-tag-gate.py` and `validate-contract-release.py
      verify-commit`? MEASURED: T081's list omits both. — **FINDING:**
      Phase H (T070–T082) lands strictly after Phase G (the cut) per the
      Dependencies graph, so "the branch head" T081 sweeps is a LATER commit
      than "the exact unchanged candidate" T064 validated; T081's omission of
      `validate-release-tag-gate.py` and `validate-contract-release.py
      verify-commit` is plausible (Phase H does not touch `contracts/`) but
      that premise — that no Phase H commit touches any path either gate
      inspects — is nowhere stated as the reason for the narrower final
      sweep, so a reader cannot tell an intentional narrowing from an
      oversight. [Gap, tasks.md T064 vs T081]
- [x] CHK012 Is the pinned CLI's own gate command required as PART of the
      reproducible transcript (`@fission-ai/openspec@1.12.0`,
      `OPENSPEC_TELEMETRY=0`), rather than left to be inferred from the
      phrase "the pinned CLI"? MEASURED: `plan.md`'s Technical Context names
      the exact package and the telemetry flag. [Ambiguity, plan.md
      Technical Context]
- [x] CHK013 Is § 5.4's tick condition (T064, Q11) explicit that a LOCAL run
      of all five gates is sufficient evidence, with the GitHub workflow's
      own green treated as the lane's later PR-open observation and not this
      feature's tick condition — closing the gap the architect flagged in
      clarify Q11? [Gap-closure, spec.md FR-034/Clarifications Q11, tasks.md
      T064]

## Doc-Health Two-Report Comparison

- [x] CHK014 Is "two reports with identical basenames and a pinned `--as-of`"
      (FR-045) specified precisely enough that an implementer could not
      satisfy it with two reports of DIFFERENT basenames taken on the SAME
      date, or the SAME basename taken on two DIFFERENT dates? [Precision,
      spec.md FR-045]
- [x] CHK015 Does T080 name BOTH heads the comparison runs against (`main`
      and this branch) explicitly, rather than leaving "the two reports" to
      be inferred? MEASURED: T080 reads "identical basenames, `--as-of`
      pinned to one date on both, main and this branch, finding sets
      diff-identical at every severity." [Completeness, tasks.md T080]
- [x] CHK016 Is the required OUTCOME of the comparison (diff-identical at
      EVERY severity) distinguished from a weaker outcome (no NEW findings,
      or no findings above a threshold), so a partial match could not be
      read as satisfying SC-008? [Precision, spec.md SC-008, tasks.md T080]
- [ ] CHK017 Is a rule stated for distinguishing, in the comparison, a
      finding-count change that occurred only because the corpus grew
      (new fixtures, a new schema property) from a genuine new or resolved
      doc-health finding — analogous to the sibling feature's CHK025 concern?
      — **FINDING:** neither `spec.md` nor `tasks.md` states such a rule;
      T080 and SC-008 require the finding SET to be diff-identical, which by
      construction would already surface a spurious new finding caused by
      corpus growth as a diff, but nothing tells the implementer how to
      DISPOSITION such a diff if the growth itself trips a doc-health rule
      (e.g., a lifecycle-header scan over the new `withheld/` directory).
      [Gap, spec.md SC-008, tasks.md T080]

## Measured-Figure-to-Command Traceability

- [x] CHK018 Do R1, R2, R6, R7, R12 and R13 each name the EXACT command that
      produced the stated figure, rather than describing the command in
      prose? MEASURED: `ls specs/`, `git branch -r | grep`, `git diff
      --name-status contract-v3.4 HEAD -- contracts/`, `ls
      examples/consent-instrument/*.example.yaml`, `gh api
      repos/opensoft/openxFactory/pulls/774/reviews`, and the per-gate
      command lines are each given verbatim. [Measurability, research.md
      R1/R2/R6/R7/R12/R13]
- [ ] CHK019 Do R3 (the `contract-v3.4` squash-merge precedent), R9 (no
      caller reads the validator's exit code) and R10 (test-package naming
      survey) each name a literal, re-runnable command the way R1/R2/R6/R7/
      R12 do? MEASURED: R3 states "landed as `807a4f47` — ONE parent,
      committer `GitHub`, subject ending `(#653)`" with no shown command
      (e.g. `git show -s --format='%P %cn %s' contract-v3.4`); R9 states
      "Grepped across `.github/workflows/*.yml` (twelve files), `tests/`,
      and the OpsxFactory consumption path" with no literal grep invocation;
      R10 states "No `tests/consent*` directory exists" with no shown `ls`/
      `find` command. — **FINDING:** R3, R9 and R10 report measured
      conclusions without the literal command line the file's own
      convention (R1, R2, R6, R7, R12, R13) otherwise uses throughout,
      so a reader cannot re-run "the command" for these three without
      first reconstructing what it must have been. [Measurability,
      research.md R3/R9/R10]
- [x] CHK020 Is R5's claim that the manifest digest is CURRENT today backed
      by a command AND its exact returned value? MEASURED: `sha256sum
      contracts/schemas/consent-instrument.schema.yaml` returns
      `13b0fe46fdb8791020b426dcd763aced2a3280a82923b32d3a0d0877ab6ad441`,
      matching the pin at `contracts/manifest.yaml:2042`; re-run and
      confirmed identical on this pass. [Measurability, research.md R5]
- [x] CHK021 Is the "5 valid + 5 invalid + purpose probes" manifest comment's
      falseness (R7) independently reproducible by counting files, not only
      asserted? MEASURED: `ls examples/consent-instrument/*.example.yaml`
      returns 6, `ls examples/consent-instrument/negative/*.yaml` returns 7,
      confirming R7's "6/7" figure and the comment's staleness, both
      re-verified on this pass. [Measurability, research.md R7]
- [x] CHK022 Does `spec.md`'s Measured baseline table cite the SAME figures
      as `research.md`, with no table row silently diverging from the
      research it is supposed to summarize (e.g., contract_bundle_version,
      corpus counts, digest, highest tag)? MEASURED: every row in `spec.md`'s
      table (lines 61–82) matches its corresponding R-section. [Consistency,
      spec.md Measured baseline / research.md]

## No Unbacked Claims

- [x] CHK023 Is the claim that `contract-v3.5` is "free on all three
      surfaces" backed by re-checking all three surfaces independently
      (manifest, `contracts/releases/`, tags), not inferred from only one?
      MEASURED: `contracts/manifest.yaml:3` reads `contract-v3.4`;
      `contracts/releases/` highest is `contract-v3.4.digests.yaml`; `git
      tag -l 'contract-v*' | sort -V | tail` tops at `contract-v3.4` — all
      three re-confirmed on this pass. [Measurability, research.md R2]
- [x] CHK024 Is the claim that "`contract-v2.6` is the SPENT number, not this
      one" (R2) traceable to the exact policy section that defines the SPENT
      state, rather than asserted with no citation? MEASURED:
      `docs/contract-versioning-policy.md` § *The SPENT State* names
      `contract-v2.6` as "the estate's first instance." [Traceability,
      research.md R2, docs/contract-versioning-policy.md]
- [x] CHK025 Is every claim in the Edge Cases section of `spec.md` backed by
      a citation to a ruled answer or a measurement (the version-number
      re-measurement rule to Q1/task 5.1; the squash-merge rule to policy
      step 4; the exit-code-caller claim to clarify round 1's measurement),
      rather than asserted as the author's own judgment with no anchor?
      [Traceability, spec.md Edge Cases]
- [x] CHK026 Is the A2 cross-repo consequence's premise — `README.md:2993`'s
      exact sentence — quoted rather than paraphrased in `research.md` R14,
      so a reader can verify the falsification claim word-for-word? MEASURED:
      R14 quotes "NO family anywhere has a declared re-derivation rule
      today — the consent family's is PROPOSED only (`contract_schema_version:
      2`, no `custody_rederivations` property, `contract-v3.4`, 46/46 boxes
      unticked)" and this matches `README.md:2991-2993` verbatim. [Precision,
      research.md R14, README.md:2991-2993]

## Scenario-to-Task Traceability

- [ ] CHK027 Does any document in the Speckit tree provide an explicit
      scenario-by-scenario mapping from the ratified delta's 22 `#### Scenario:`
      blocks (7 in the `## MODIFIED` requirement, 15 in the `## ADDED`
      requirement) to the `T###` task(s) that realize or deliberately do not
      realize each one? MEASURED: no such table exists in `spec.md`,
      `plan.md`, `tasks.md` or `research.md` — `spec.md`'s own "User
      Scenarios & Testing" section defines four NEW User Stories with their
      own Acceptance criteria, none titled after or cross-referencing the
      ratified delta's 22 scenario titles verbatim. — **FINDING:** there is
      no scenario-to-task traceability matrix; the mapping from (for example)
      the delta's "A chain that does not anchor to the pin is refused" to
      task T020/T037 must be reconstructed by a reader rather than read off
      a table, and nothing distinguishes, scenario-by-scenario, which of the
      22 are THIS feature's to satisfy versus which are inherently
      git-dependent and therefore F.2/OpsxFactory's (§7.1, NOT-OWED) even
      though the ratified delta states all 22 as one requirement's scenarios.
      [Gap, spec.md/tasks.md, ratified delta]
- [x] CHK028 Is the SPLIT between validator-internal scenarios (checkable
      from the record's own bytes) and git-dependent scenarios (requiring
      repository resolution — e.g. "A header_only claim contradicted by the
      diff is refused," "A locator pair that resolves at neither path is
      refused," "A chain on a commit that is not an ancestor of HEAD is
      refused," "A HEAD digest matching no terminus is refused," "A chain
      that cannot be re-derived is refused, never admitted," "A consumer
      gate propagates a withheld verdict and never upgrades it," "A direct
      pin verifies with no chain") stated as a GENERAL PRINCIPLE anywhere
      (the ratified delta's own closing paragraph, "The obligation is
      SPLIT... SHALL NOT attempt the git re-derivation"), so a reader knows
      WHY roughly a third of the 22 scenarios have no `T###` counterpart in
      this feature, even without CHK027's table? [Traceability, ratified
      delta closing paragraph, proposal.md C-7, design.md C-7]
- [x] CHK029 Is the one scenario most likely to be mistaken for
      fully-owned-here — "A re-derivation does not amend the instrument"
      (the C-10 no-`amendments`-entry rule) — correctly recognized as a
      CONSUMER-authored-instrument behavior (§6.2, OpsxFactory's own
      instruments taking entries) rather than something this feature's
      fixtures independently prove, given this feature's own fixtures
      (T030–T033) merely DEMONSTRATE the pattern is schema-legal without any
      validator check that an instrument's status did not change "for that
      reason alone"? [Ambiguity, ratified delta "A re-derivation does not
      amend the instrument" scenario, proposal.md § *Consumers*, packet
      tasks.md § 6.2]
- [x] CHK030 For each git-dependent scenario correctly deferred to F.2, is
      the deferral traceable to a NAMED packet box (§ 7.1) rather than
      merely implied by the absence of a matching `T###`? MEASURED: packet
      `tasks.md` § 7.1 states "F.2's custody-digest gate is NOT built here...
      This packet supplies only the consent-custody family's re-derivation
      rule, which that gate consumes," and Speckit `tasks.md` T075 records a
      dated NOT-OWED line against § 7.1. [Traceability, packet tasks.md
      § 7.1, Speckit tasks.md T075]

## False-Record / Transcript-Authenticity Class

- [ ] CHK031 Is it required anywhere that a gate transcript filed to
      `evidence/` be the RAW, unedited command output (return code plus the
      summary line, captured to a file) rather than a hand-composed
      description of what the command reportedly showed — the discipline
      the sibling feature's evidence checklist required (its CHK021/CHK023,
      "capture the return code AND the summary line," "recorded verbatim")?
      — **FINDING:** `spec.md` and `tasks.md` require transcripts to exist
      and be named (T064, T081) but neither states that a transcript must be
      the literal captured output rather than a paraphrase, and neither
      names the piped-`tail`-masks-`make`'s-exit-code failure mode the
      sibling feature's evidence checklist calls out by name; a
      hand-composed "gate X passed" line would satisfy the letter of T064/
      T081 as written. [Gap, tasks.md T064/T081, cf.
      specs/032-govern-archived-record-edits/checklists/evidence-and-traceability.md
      CHK021-023]
- [x] CHK032 Is the box-arithmetic assertion (CHK041 of the governance
      checklist) itself required to be evidence-backed in the SAME file the
      note classes are counted in, rather than trusted as a planning-time
      claim never re-verified against the actual `- [x]` state of the
      packet's `tasks.md`? MEASURED: T076 requires the arithmetic to be
      asserted IN the evidence file, which by construction is written after
      the ticks exist, so it is a post-hoc re-verification rather than a
      forward-looking guess. [Measurability, tasks.md T076]
- [x] CHK033 Is a note permitted to cite a gate result from an INTERIM run
      (before the final candidate commit) as though it were the FINAL-HEAD
      result, or is the distinction between interim and final-head evidence
      drawn explicitly the way the sibling feature's checklist required
      (its CHK016-020)? MEASURED: FR-034/T064 require the five gates to run
      "against the exact unchanged candidate," and FR-036/the Landing
      Contract require a RE-RUN if the landed commit differs — there is no
      path by which an interim pre-candidate run could be filed as the
      candidate's own evidence without contradicting FR-034's own wording.
      [Consistency, spec.md FR-034/FR-036]
- [x] CHK034 Could the "digest inventory drifts from the tree" risk (plan.md
      Risks table) be realized as a FALSE RECORD — an inventory file that
      claims to have been BUILT by the tool but was in fact hand-edited —
      and is the refusal to that risk (built by `validate-contract-release.py
      build`, never hand-edited, re-derived by `verify-commit`) independently
      checkable rather than a promise with no gate behind it? MEASURED:
      SC-005 names `validate-contract-release.py verify-commit --commit
      <candidate>` as the independent check, and T063 requires the BUILD
      command's exact invocation. [Completeness, plan.md Risks table,
      spec.md SC-005, tasks.md T063]
