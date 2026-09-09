# Checklist: Failure Recovery and Landing — 033-add-consent-custody-rederivation-record

**Purpose**: Release-gate audit of what happens when things go wrong — whether
each risk in `plan.md`'s risk table has a stated refusal that actually fires,
whether the landing contract's steps are complete and in order, whether the
"repeat the integration if `main` moved under `contracts/`" rule is stated,
whether force-push and PR/comment/merge/tag acts are banned from this seat,
whether recovery is specified for the version number being taken by a
sibling lane, for the substrate note never arriving, and for a gate reddening
after the candidate commit is formed. This interrogates the WRITTEN recovery
plan — no failure has yet occurred, since §§ 2–5 are unrealized.

**Artifacts under review**: `plan.md` (Risks table, THE LANDING CONTRACT,
Implementation sequence table), `spec.md` (Edge Cases, Out of scope, FR-036),
`tasks.md` (Dependencies graph, Phase F/G, T082),
`docs/contract-versioning-policy.md` § *Bundle Realization Order*, § *The
SPENT State*.

**Date**: 2026-09-09. No-argument invocation — maximum coverage, no item cap.

## Risk-Table Coverage — Every Risk Has a Stated, Firing Refusal

- [x] CHK001 **Risk: a sibling lane takes `contract-v3.5`.** Is the refusal
      ("the number is a measurement re-taken at every merge-from-main and
      CLAIMED by the lane at the last one; nothing on this branch reserves
      it") consistent with FR-030's "re-measures at every merge-from-main and
      reports" and with the Edge Cases bullet "The version number is taken
      while this branch is open... The allocation step re-measures... and the
      branch re-numbers rather than landing a stale one"? [Consistency,
      plan.md Risks / spec.md FR-030/Edge Cases]
- [x] CHK002 **Risk: the digest inventory drifts from the tree.** Is the
      refusal ("BUILT by `validate-contract-release.py build`, never
      hand-edited, and `verify-commit` re-derives it against the exact
      candidate") independently gated by a Success Criterion, not merely
      asserted? MEASURED: SC-005 names `verify-commit --commit <candidate>`
      as the check. [Measurability, plan.md Risks / spec.md SC-005]
- [x] CHK003 **Risk: the stale manifest digest between § 2 and § 5.2 is read
      as a defect.** Is the refusal (§ 2's commit message states the
      staleness and names T060 as the commit that closes it) traceable to a
      SPECIFIC task requiring that commit-message content, not left to an
      implementer's discretion whether to mention it? MEASURED: T017 reads
      "Commit message STATES that `contracts/manifest.yaml`'s
      `consent-instrument` digest is now deliberately stale and names T060
      as the commit that closes it." [Traceability, plan.md Risks / tasks.md
      T017]
- [x] CHK004 **Risk: the withheld fixture reddens a caller.** Is the refusal
      ("Measured: no caller reads this exit code. The packaged fixture is
      exempt in any case.") backed by BOTH the R9 measurement AND an
      independent design safeguard (the exemption), so the refusal does not
      rest on the measurement alone becoming false later? MEASURED: T024
      names the packaged-fixture exemption as a SEPARATE guarantee from the
      R9 measurement. [Completeness, plan.md Risks / research.md R9 / tasks.md
      T024]
- [x] CHK005 **Risk: the exit-code number is wrong.** Is the refusal ("single
      named constant, Q2 records the number is Brett's ruling") backed by a
      dedicated TEST pinning the constant (T053), so a later re-ruling is a
      one-line test edit rather than a silent drift? [Measurability, plan.md
      Risks / tasks.md T024/T053]
- [x] CHK006 **Risk: a tick claims an act nobody performed.** Is the refusal
      ("every tick's note cites a commit, a record or a transcript, and
      rides the same commit as its evidence") the SAME rule as FR-040/FR-041,
      or does the risk table describe a DIFFERENT, weaker standard than the
      Functional Requirements actually impose? MEASURED: the risk-table
      language and FR-040/FR-041 are consistent restatements of the same
      rule. [Consistency, plan.md Risks / spec.md FR-040/FR-041]
- [x] CHK007 **Risk: a README amendment lands without its substrate claim.**
      Is the stated refusal ("Phase G is BLOCKED until the lane posts the
      note") the CORRECT phase under the SAME lettering scheme the rest of
      `plan.md` uses in this same table — or does it name a phase letter
      that means something else elsewhere in the Speckit tree? See CHK024
      below for the load-bearing finding this surfaces. [Consistency,
      plan.md Risks table row 7]
- [x] CHK008 **Risk: landing arms a cross-repo refusal nobody scheduled.** Is
      the refusal ("A2 is recorded as a dated note in two places and built
      nowhere") the SAME two places FR-047/T078 name, so the risk table and
      the Functional Requirements do not silently diverge on where the note
      lives? [Consistency, plan.md Risks table row 8 / spec.md FR-047]
- [x] CHK009 Does EVERY row in the risk table correspond to a named task or
      requirement an implementer can point to as the refusal's actual
      mechanism, rather than any row being a bare assurance with no
      enforcing task behind it? MEASURED: rows 1-8 each trace to
      FR-030/Edge-Cases, SC-005, T017, T024/R9, T024/T053, FR-040/FR-041,
      T055 (see CHK024), and FR-047/T078 respectively — none is unmechanized.
      [Completeness, plan.md Risks table]

## The Landing Contract — Steps In Order

- [x] CHK010 Is THE LANDING CONTRACT's numbered sequence (1. one PR carries
      §§2-5; 2. the version is a measured candidate, re-measured at every
      merge-from-main; 3. the lane claims the number at the LAST
      merge-from-main before merge; 4. landing is a merge commit; 5. the
      merge commit IS "a different commit," so gates re-run against it
      before merging; 6. if `main` advanced under `contracts/`, the
      integration repeats; 7. the annotated tag targets the landed merge
      commit; 8. § 5.5 is the lane's tick in a follow-up commit) internally
      ordered so that a later step never depends on a step that comes after
      it? MEASURED: steps 1-8 form a strict causal chain with no forward
      reference. [Consistency, plan.md THE LANDING CONTRACT]
- [x] CHK011 Is step 3's "at the LAST merge-from-main before the merge — at
      cut time and not before" traceable to a specific citation (the
      ratification record lines 109-111, and task 5.1) rather than asserted
      as the plan author's own preference? MEASURED: plan.md line 137-140
      cites both. [Traceability, plan.md THE LANDING CONTRACT step 3]
- [x] CHK012 Is step 5's claim that "the merge commit IS 'a different
      commit'" traced to the EXACT policy clause it applies (§ *Bundle
      Realization Order* step 4), and does the policy's own wording support
      reading a merge commit (as opposed to only a squash) as "a different
      commit"? MEASURED: `docs/contract-versioning-policy.md` line 311-313
      reads "Land the exact reviewed commit... If promotion creates a
      different commit, that commit becomes the new candidate and every gate
      and review reruns before tagging" — worded generally enough to cover
      a merge commit, not only a squash. [Precision, plan.md step 5 / policy
      § Bundle Realization Order]
- [x] CHK013 Is FR-036 (spec.md's own statement of the landing contract)
      IDENTICAL in substance to `plan.md`'s THE LANDING CONTRACT, so an
      implementer reading only `spec.md` would not receive a materially
      different landing procedure than one reading only `plan.md`? MEASURED:
      FR-036's five clauses (merge commit; RE-RUNS gates; repeats
      integration if `main` advanced) match plan.md steps 4-6 in substance.
      [Consistency, spec.md FR-036 / plan.md THE LANDING CONTRACT]
- [x] CHK014 Is step 7 (the annotated tag targets the LANDED MERGE COMMIT)
      consistent with FR-035's "the annotated tag MUST be left OWED. This
      feature does not tag," so the landing contract's mention of the tag is
      informational (for the OPERATOR's later act) and not itself a task
      this feature performs? [Consistency, plan.md step 7 / spec.md FR-035]
- [x] CHK015 Is step 8 (§ 5.5 is the lane's tick, in a follow-up bookkeeping
      commit "while the packet is still live") reconciled with T065's
      NOT-OWED-HERE disposition for § 5.5 in THIS feature, so the reader
      understands the follow-up tick is a SEPARATE later act by the same
      lane rather than something T065 itself performs? [Consistency, plan.md
      step 8 / tasks.md T065]

## "Repeat the Integration if `main` Moved Under `contracts/`"

- [x] CHK016 Is the repeat-the-integration rule stated in BOTH `plan.md`
      (step 6: "If `main` advanced under `contracts/` between integration
      and merge, the lane REPEATS the integration. A bundle measured against
      a tree that has since moved is not a measurement.") and `spec.md`
      (FR-036: "If `main` advanced under `contracts/` between integration
      and merge, the lane REPEATS the integration.")? MEASURED: both present,
      word-for-word consistent. [Consistency, plan.md step 6 / spec.md
      FR-036]
- [x] CHK017 Is the SCOPE of "advanced" bounded precisely (specifically
      under `contracts/`, not any path in the repository), so a move under
      an unrelated path (e.g. `docs/`) does not trigger an unnecessary
      re-integration, and a move under `contracts/releases/` or
      `contracts/manifest.yaml` specifically is not missed by a narrower
      reading limited only to `contracts/schemas/`? [Ambiguity, plan.md step
      6 / spec.md FR-036 — both say "under `contracts/`" without narrowing
      to a subpath, so the broader reading governs]
- [x] CHK018 Is it stated what happens to evidence ALREADY GATHERED against
      the pre-repeat candidate when the integration repeats? **RE-VERIFIED,
      RESOLVED.** Landing Contract step 7 now reads "A repeat-integration
      RETAINS the superseded gate transcripts, struck with a dated line
      naming the head that replaced them; the evidence shows every attempt,
      not only the last." A matching new risk-table row: "A repeat-integration
      orphans the evidence already gathered | The superseded transcripts are
      RETAINED and STRUCK with a dated line naming the head that replaced
      them — never deleted and never silently overwritten." This is the same
      discipline the sibling feature's checklist required, now stated
      in-feature. [Gap-closure, plan.md THE LANDING CONTRACT step 7, Risks
      table]

## Force-Push Ban

- [x] CHK019 Is a ban on force-pushing this branch stated anywhere in this
      feature's own `spec.md`, `plan.md` or `tasks.md`? **RE-VERIFIED,
      RESOLVED.** `spec.md` Edge Cases now carries: "THE BRANCH MERGES
      FORWARD AND NEVER REBASES PUSHED COMMITS. No `--force`, no
      `--force-with-lease`, no rebase of anything already pushed, and no
      amend of a commit another party may have read. Integration with `main`
      is always a MERGE — opensoft org ruleset 8981805 forbids
      non-fast-forward updates... This is stated here, in this feature's own
      documents, rather than left to the global harness rule." `tasks.md`
      T082 restates the identical discipline with the same ruleset citation.
      [Gap-closure, spec.md Edge Cases, tasks.md T082]
- [x] CHK020 Is the CONSEQUENCE of the missing in-document statement actually
      material, given the Landing Contract's own step 6 ("repeats the
      integration" via a forward merge, never a rebase) already implies the
      merge-forward discipline operationally, even without a standalone
      prohibition sentence? [Ambiguity, plan.md THE LANDING CONTRACT step 6]

## PR / Comment / Merge / Tag Ban From This Seat

- [x] CHK021 Is "no PR, no comment, no merge, no tag from this seat" stated
      in `plan.md`'s Constitution Check table AS WELL AS in `spec.md`'s Out
      of scope section ("Opening the pull request, posting any GitHub
      comment... merging, tagging, or archiving the OpenSpec change") AND in
      `tasks.md` T082 ("Push the branch. No pull request, no comment, no
      merge, no tag")? MEASURED: all three present and consistent.
      [Consistency, plan.md Constitution Check / spec.md Out of scope /
      tasks.md T082]
- [x] CHK022 Is the ONE apparent exception — the row-3 substrate note Phase F
      needs, attributed to "the LANE" rather than "this feature" — reconciled
      with the blanket "no comment from this seat" rule by the SAME pattern
      used for § 5.1's version-number claim (also explicitly "the LANE's,"
      posted separately from this feature's own task execution), so the two
      statements are not read as contradicting each other? [Consistency,
      spec.md FR-030/FR-046/Out of scope]
- [x] CHK023 Is T082 the LAST task in the Speckit `tasks.md`'s Phase H, so
      pushing the branch is unambiguously the final act this feature
      performs, with nothing after it that could be misread as an implicit
      license to also open the PR? MEASURED: T082 is the final numbered task
      in the file. [Precision, tasks.md T082]

## Phase-Lettering and Ordering Consistency Between `plan.md` and `tasks.md`

- [x] CHK024 Does `plan.md`'s "Implementation sequence" table use the SAME
      phase-letter assignments as `tasks.md`'s own `## Phase X` headers and
      Dependencies graph? **RE-VERIFIED, RESOLVED — this was the LOAD-BEARING
      finding.** `plan.md`'s table now opens with an explicit self-correction:
      "THE PHASE LETTERS HERE ARE `tasks.md`'s LETTERS, EXACTLY. An earlier
      draft of this table used its own scheme, in which corpus counts were a
      separate phase and every letter after it was offset by one — so this
      table's 'Phase G' named the cut while `tasks.md`'s Phase G named the
      README amendments, and the risk row below pointed at the wrong phase.
      One scheme, and it is the executable file's." The table itself now
      reads A–H (8 phases) with corpus counts (T047–T049) folded into Phase
      D, matching `tasks.md` exactly row for row, and the risk-table row now
      reads "**Phase F** is BLOCKED until the lane posts the note" — the
      correct letter under the now-shared scheme. [Consistency, plan.md
      Implementation sequence table / tasks.md `## Phase` headers — now
      identical]
- [x] CHK025 Does `plan.md`'s Implementation sequence table order corpus
      counts consistently with `tasks.md`? **RE-VERIFIED, RESOLVED by the same
      fix as CHK024.** `plan.md`'s Phase D content now explicitly reads "§ 4
      fixtures — positives, negatives, the withheld bucket, `self_test`'s
      third bucket, **and the three corpus-count surfaces (T047–T049)**,"
      placing corpus-count re-measurement inside Phase D, strictly before
      Phase E (`tests/consent_instruments/`, T050–T054) — matching
      `tasks.md`'s own task numbering and phase structure exactly. The
      cross-document sequencing disagreement no longer exists. [Consistency,
      plan.md Implementation sequence table Phase D / tasks.md Phase D
      "Corpus counts" subsection / Phase E — now aligned]
- [x] CHK026 Despite CHK024/CHK025's lettering and ordering divergence, is
      the SUBSTANTIVE recovery rule the task prompt asks after — "Phase F
      blocked, Phase G must not wait on it" — actually TRUE under
      `tasks.md`'s own (executable) lettering? MEASURED: `tasks.md`'s
      Dependencies graph reads `E -> {F (BLOCKED on the lane's substrate
      note), G (LAST; must not wait on F)} -> H`, which is exactly this
      rule, correctly stated under `tasks.md`'s own scheme. The defect
      identified in CHK024/CHK025 is a CROSS-DOCUMENT lettering/ordering
      mismatch, not a defect in the underlying recovery rule itself once a
      reader commits to `tasks.md` (the "EXECUTABLE list," per its own
      header) as authoritative. [Consistency, tasks.md Dependencies graph]

## Recovery — Version Number Taken by a Sibling Lane

- [x] CHK027 Is the recovery ("re-measure at every merge-from-main; the
      branch re-numbers rather than landing a stale one") stated as an
      explicit EDGE CASE in `spec.md`, not only inferred from FR-030's
      forward-looking obligation? MEASURED: `spec.md` Edge Cases bullet 1
      states it directly. [Completeness, spec.md Edge Cases]
- [x] CHK028 Is it explicit that NOTHING on this branch RESERVES
      `contract-v3.5` before cut time, so a sibling lane taking it is not a
      "collision" in the lane-collision-protocol sense but an ordinary,
      anticipated re-measurement? MEASURED: `spec.md` Assumptions:
      "`contract-v3.5` is free at the integration point unless a sibling
      lane takes it first; the allocation step re-measures rather than
      trusting this document." [Clarity, spec.md Assumptions]
- [x] CHK029 Is the SPENT-number failure mode (a number cut but never
      publishable, per `docs/contract-versioning-policy.md` § *The SPENT
      State*, `contract-v2.6`'s precedent) distinguished from the ordinary
      "taken by a sibling, re-measure and take the next" case, so an
      implementer does not conflate "someone else already used 3.5" with
      "3.5 became permanently unusable"? [Edge Case, docs/contract-versioning-policy.md
      § The SPENT State, research.md R2]

## Recovery — the Substrate Note Never Arrives

- [x] CHK030 Is it explicit that Phase F's (tasks.md lettering) non-arrival
      leaves T057/T058 open WITHOUT blocking Phase G (the cut) or Phase H
      (bookkeeping/push)? MEASURED: Dependencies graph shows F and G as
      siblings off E, with G annotated "must not wait on F." [Consistency,
      tasks.md Dependencies graph]
- [x] CHK031 Is it explicit that Phase F's non-arrival does not prevent the
      feature from being reported as meeting its "Definition of done"?
      MEASURED: the Definition of done list (35 boxes ticked, 11 NOT-OWED/
      NOT-OWED-HERE lines, SC-001..010, zero `speckit-analyze` findings, the
      branch pushed) contains no item that depends on T055-T059, since the
      README sites are additional realization acts (FR-046/A1) outside the
      packet's 46-box count. [Consistency, tasks.md Definition of done]
- [x] CHK032 Is a TERMINAL disposition stated for T057/T058 if the note never
      arrives before the branch is pushed (T082)? **RE-VERIFIED, RESOLVED.**
      T055 now carries "TERMINAL DISPOSITION if it never arrives. T056 is
      taken regardless. If the branch reaches T082 with Phase F still
      blocked, **T057 and T058 take a dated `REPORTED, NOT PERFORMED` line**
      naming the block and the note they wait on — the same register as
      §§ 6–7's NOT-OWED lines. They are neither left dangling nor silently
      dropped, and the two README sentences stay false-on-main with that
      fact RECORDED rather than hidden." `plan.md`'s matching risk row states
      the identical disposition. [Gap-closure, tasks.md T055, plan.md Risks
      table]

## Recovery — a Gate Reds After the Candidate Commit Is Formed

- [x] CHK033 Is it stated anywhere that a gate failure discovered AFTER the
      § 5.2 candidate commit is formed requires FORMING A NEW CANDIDATE
      COMMIT (remaking it) rather than amending/patching the existing one in
      place? **RE-VERIFIED, RESOLVED.** New FR-034a states it explicitly:
      "a gate that reds after the § 5.2 candidate commit is formed MUST be
      repaired by producing a FRESH single candidate commit and re-running
      EVERY gate against it. The reviewed commit is never amended in place:
      FR-031 makes the candidate one atomic commit and FR-034 certifies 'the
      exact unchanged candidate', so a candidate edited after a gate ran is
      no longer the thing that gate certified." A matching risk-table row
      ("A gate reds after the candidate commit is formed | The candidate is
      REMADE, never patched (FR-034a)...") and a traceability-table row
      ("FR-034a | T061–T064 (the rule the phase follows)") both carry it
      forward. What was previously only an inference is now a named rule.
      [Gap-closure, spec.md FR-034a, plan.md Risks table, tasks.md
      traceability table]
- [x] CHK034 Is the ONE narrow exception to "remake, don't patch" — the
      squash/merge-produced "different commit" the Landing Contract already
      contemplates (step 5/FR-036) — correctly distinguished from an
      in-place amend of the SAME commit object, so CHK033's inferred rule
      and FR-036's explicit rule do not conflict? MEASURED: FR-036 describes
      a NEW commit object (the merge commit) superseding the reviewed one
      with a full gate re-run, which is consistent with "remake, don't
      patch" rather than an exception to it. [Consistency, spec.md FR-036]
- [x] CHK035 If a gate reds on the candidate and the fix touches
      `contracts/schemas/consent-instrument.schema.yaml` (§ 2) rather than
      the release surface itself, is it clear that the SAME "no split, one
      atomic candidate" discipline (FR-031) applies to the REMADE candidate,
      requiring the digest inventory to be rebuilt (not hand-patched) again
      via T063's exact command? [Consistency, spec.md FR-031/FR-033, tasks.md
      T061-T063]

## False-Record Class

- [x] CHK036 Could the Landing Contract, as specified, be satisfied by
      recording "gates green" against the PRE-merge candidate while actually
      merging a commit the gates never ran against — i.e., does FR-036 leave
      any path by which the post-merge re-run could be SKIPPED and the
      pre-merge evidence cited in its place? MEASURED: FR-036 and Landing
      Contract step 5 both make the re-run MANDATORY whenever the merge
      commit differs from the reviewed candidate, with no stated exception.
      [Completeness, spec.md FR-036, plan.md step 5]
- [x] CHK037 Does the annotated-tag prohibition (FR-035, "This feature does
      not tag") foreclose any path by which this feature's own evidence
      could misrepresent a tag as already published, given the tag is the
      one release-surface element this feature explicitly never touches?
      [Completeness, spec.md FR-035]
