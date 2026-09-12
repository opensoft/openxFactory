# Tasks: amend-register-act-5b-projection-proof

Status: ratified
Ratified by: Brett Heap, 2026-09-11T13:09:12Z — verbatim "accept all A on 960" (record `review/ratification-2026-09-11.md`)
Kind: tasks
Lane: hermes-wallet-exercise

`code_surface: none`, `target_release: implemented` — so under
`release-realization` this packet archives on LANDING plus this task list,
and not on merged-plus-green realization evidence. **The runbook edit is IN
this list (§3), so "archives on landing plus its task list" still means the
runbook edit has to have happened.**

**§ 1 BELOW IS NOW TICKED, AGAINST BRETT HEAP'S RATIFICATION WORD; NOTHING
ELSE IS, AND THIS PULL REQUEST STILL PERFORMS NO OTHER ACT.** No requirement
is promoted, no runbook byte moves, no register file is touched, no record is
appended, and no box in any other packet is ticked by it. Every box names the
act that ticks it and the word that authorizes that act.

**Groups, in order:** §1 ratify → §2 encode → §3 realize → §4 cite back →
§5 archive → §6 residue.

---

## 1. Ratification — Brett Heap's, and nobody else's

- [x] 1.1 **Rule OQ-1 through OQ-7** (`proposal.md` § Open questions;
      `design.md` D-1 through D-7). Multiple choice, each with a RECOMMENDED
      option and its reason. **Taking every recommendation moves no byte**;
      any other answer on OQ-1, OQ-2, OQ-4 or OQ-5 rewrites the requirement it
      names before ratification, and any other answer on OQ-3, OQ-6 or OQ-7
      moves the packet rather than the wording. Ticks on the ruling, recorded
      verbatim with its UTC instant. **RULED: Brett Heap, 2026-09-11T13:09:12Z,
      verbatim "accept all A on 960"** — all seven OQs at their RECOMMENDED
      option (`proposal.md` § Rulings; `review/ratification-2026-09-11.md`).
- [x] 1.2 **Ratify the packet.** `Status: draft` → `ratified` on
      `proposal.md`, `design.md`, `tasks.md` and the delta, with a `Ratified:`
      line naming the human, the instant and the verbatim word, plus
      `review/ratification-<date>.md`. `.openspec.yaml` gains `approved_by` +
      `approved_on` **ADDED BESIDE** the drafting pair, with `kind`, `id`,
      `reason`, `proposed_by` and `proposed_on` unmoved — the
      addition-not-rewrite shape `add-drafted-proposal-origin` defined, which
      is also what keeps doc-health's `proposal-origin` class 7 quiet. **DONE**
      in this same commit: all three documents plus `review/ratification-
      2026-09-11.md` (`Status: ratified`) and `review/verification-2026-09-11.md`
      (`Status: record`, the gate-run capture).
- [x] 1.3 **Record the ruling where the disposition can see it**: a comment on
      the pull request carrying this packet, quoted verbatim, so the walk
      record's disposition section can be cited back to an act rather than to
      a session. **DONE**: recorded in full, in this same commit, at
      `review/ratification-2026-09-11.md`; a comment quoting it verbatim
      follows on openxFactory PR #960.

## 2. Encode — only if a ruling moves the wording

- [ ] 2.1 **Apply any non-recommended OQ ruling to the delta** before the
      ratified head is fixed, one commit per requirement touched, and re-run
      §6.1's validators on the result. **Skipped, with the skip recorded, if
      every OQ is ruled at its recommendation** — in which case the encoded
      wording IS the ratified wording and this box ticks empty with that
      sentence as its reason.
- [ ] 2.2 **Re-measure the claims the ruling touches.** If OQ-4 is ruled B or
      C, the §5.2 step 2 correction in §3.2 drops and this file says so. If
      OQ-2 is ruled B, the fourth requirement gains the preserving sentence
      for the 2026-09-11 precedent named in `design.md` D-2.

## 3. Realize — the two runbook sentences (three if OQ-4 = A)

**One document, `docs/governed-reissuance-runbook.md`, whose `Status: draft`
does NOT move: its own header rules why it is draft, and this packet does not
reach that ruling.**

- [x] 3.1 **§5.2 step 3 — replace the exit condition.** Today:
      *"**VERIFY ONE CONVENING ADMITS.** The park is not lifted by a green
      validator — it is lifted when a real convening is admitted against the
      new grant. Until you have seen that, you have evidence that the files are
      consistent and no evidence that the lane recovered. Record which
      convening you watched."* **KEEP the true half** (a green validator does
      not lift the park) and **replace the false half** with the observed-
      projection test as ruled at OQ-1, naming the concrete artifact per OQ-3:
      ConfigMap `hermes-register-projection`, annotation
      `hermes.opensoft.one/source-revision`, at or after the register act's
      landed commit. Cite the requirement by title, and cite the walk record
      §13.2/§14.1 as the evidence. **DONE**: replaced in openxFactory PR
      [#1008](https://github.com/opensoft/openxFactory/pull/1008) →
      `0446dece9886f60daf052741b3b3e00f51b24583`, citing this requirement's
      title and walk record §§13.2/14.1 inline, and naming PR #960 →
      `ac688c40` as the ratifying act.
- [x] 3.2 **§5.2 step 2 — correct the stale clause** *"it is loose on purpose
      because nothing refreshes the projection automatically"*, which
      contradicts the refresher this packet's precondition depends on.
      **ONLY IF OQ-4 is ruled A**; dropped otherwise, with the drop recorded
      here. **DONE** (OQ-4 confirmed ruled A at `design.md` D-4): corrected in
      the same commit, openxFactory PR
      [#1008](https://github.com/opensoft/openxFactory/pull/1008) →
      `0446dece9886f60daf052741b3b3e00f51b24583`, **and CORRECTED AGAIN at
      `08eb0aa3e691d02064af661c21d95dadd1bc18ea`** on the #1008 REVIEW seat's BLOCKING finding
      ([comment 5648024201](https://github.com/opensoft/openxFactory/pull/1008#issuecomment-5648024201)):
      the first correction deleted the stale clause and put a DIFFERENT false
      one in its place — *"loose on purpose to cover the interval before the
      projection refresher's next completed cycle"* — which inverts the
      register's own declared rationale
      (`governance/review-authority/register.yaml` § *"WHY P7D AND NOT
      SOMETHING TIGHT"*: the bound is the window a revocation may go
      unhonoured, and automated refresh is the reason to move it to `P1D` or
      tighter, never the reason it is loose). The clause now quotes the
      register verbatim and carries ratified requirement 3's own evidence
      phrase, *"evidenced by the refresher's own success record"*.
- [x] 3.3 **§ "Contents" of the walk record — the `step-5b` evidence bullet.**
      Today it requires *"which convening was watched admitting"*; it becomes
      the observation's values, its comparison and its stated limit, per OQ-2.
      **DONE**: corrected in the same commit, openxFactory PR
      [#1008](https://github.com/opensoft/openxFactory/pull/1008) →
      `0446dece9886f60daf052741b3b3e00f51b24583`; the bullet now names the
      `source-revision` value read, the comparison against the act's landed
      commit, and the unread fields, named as OWED with an owner.
      **OPEN REVIEW FINDING, RECORDED AND NOT FIXED** (#1008 REVIEW seat,
      [comment 5648024201](https://github.com/opensoft/openxFactory/pull/1008#issuecomment-5648024201)):
      the bullet's surviving first half still requires, as step-5b evidence,
      *"that the staleness bound travelled verbatim"* — which is one of the
      THREE fields D-2 and §6.3 of this file record as OWED and UNREAD under a
      provenance-only observation, and which the bullet's new second half
      simultaneously permits to be named as unread. As written a walker must
      either overclaim (the failure ratified requirement 4 exists to refuse) or
      fail the bullet. This row's own text names only the *"which convening was
      watched admitting"* clause, so moving the staleness-bound clause into the
      OWED half is a judgement about what the evidence list requires rather
      than a transcription of this row — **left to Brett Heap.**
- [x] 3.4 **Do NOT touch §"Before you start" (the step-5b prerequisite) or §4's
      *"The only exit is step 5 and step 5b together"***. Both are true as
      written and this packet makes them truer; recorded as a deliberate
      non-edit so a reviewer does not read the omission as an oversight.
      **DONE**: confirmed untouched in openxFactory PR
      [#1008](https://github.com/opensoft/openxFactory/pull/1008) →
      `0446dece9886f60daf052741b3b3e00f51b24583` (`git diff` shows no hunk
      near either sentence). Citation correction while checking: the "only
      exit is step 5 and step 5b together" sentence is in the runbook's own
      §3 ("Step 3 — the in-flight behavior (R9), verbatim"), not §4 as this
      row's text says — unchanged either way.
- [x] 3.5 **Prove the edit did not widen.** Diff the runbook and state the
      insertion/deletion counts in the realization pull request body; any hunk
      outside §5.2 and the Contents list is a finding against the edit.
      **DONE**: `git diff --stat` for the runbook = 1 file changed, 46
      insertions(+), 7 deletions(-) at review-fix `08eb0aa3e691d02064af661c21d95dadd1bc18ea`
      (39/7 at the first pass, `0446dece`), stated in openxFactory PR
      [#1008](https://github.com/opensoft/openxFactory/pull/1008)'s body.
      **THE FINDING THIS ROW DEFINES IS RAISED, NOT WAIVED.** The diff carries
      a THIRD hunk beyond §5.2 and the Contents list — a new `Amended by:`
      line in the document's own header — so by this row's own words it **is a
      finding against the edit**, and it is recorded here as one rather than
      explained away. It is raised rather than dropped because the line is this
      repository's standing convention for citing a realizing change
      (`docs/lifecycle-notebook-projection.md:8,11,13` — same shape, same
      header position) and because `docs/document-lifecycle.md` reaches neither
      for nor against it on a `Status: draft` document. **Its disposition is
      Brett Heap's at merge — keep the hunk, or drop it and re-diff — and this
      row does not clear it.**

## 4. Cite back — close the disposition's loop

- [ ] 4.1 **Name this change in the disposition's own record**, openxFactory
      `openspec/changes/register-gate-rules-council-seats/walk-2026-09-11-register-act.md`
      § `## Disposition — design § D4 step 5b`. The record is `Status: record`:
      the citation is a **DATED APPEND**, never an edit of the section, and it
      states which of the four "WHAT THE QUEUED CHANGE SHOULD SETTLE" items
      each ruling settled and which it did not.
- [ ] 4.2 **Answer the disposition's four items explicitly**, by number:
      (1) what the real exit condition is; (2) whether the runbook's *"a green
      validator does not lift the hold"* framing survives — it does, and only
      the convening half goes; (3) whether the step names the source-revision
      test and whether it requires the row-level fields; (4) who may perform
      it.
- [ ] 4.3 **Do NOT amend codexFactory.** `clarify-gate-rules-decline-position`
      § D4 step 5b keeps its ratified text and its 2026-09-11 pointer
      annotation; if that packet has archived by then, the archived copy is
      likewise untouched. Ticks on the recording of the non-act.

## 5. Archive — and not before the parents

- [ ] 5.1 **Hold the archive behind `add-wallet-carried-review-authority`**
      per OQ-6 option A, so that the promoted
      `openspec/specs/review-authority-intake/spec.md` is created by the
      capability's author and not by this amendment. `sequenced_after:`
      declares both parents; this box records which parent archived and when.
- [ ] 5.2 **Archive on Brett Heap's separate word**, after §1–§4 are ticked:
      `openspec archive amend-register-act-5b-projection-proof --yes` through
      the pinned CLI entrypoint, promoting the four requirements into
      `review-authority-intake`, with the README OpenSpec Records row moved
      from Active to Archived.
- [ ] 5.3 **Re-run the corpus validators on the archived tree** and compare
      the failure set with the pre-archive baseline, quoting both.

## 6. Residue, measurements and what is deliberately not taken

- [ ] 6.1 **The validator runs this packet is landed on**, recorded with
      commands and exit codes: `OPENSPEC_TELEMETRY=0 openspec validate
      amend-register-act-5b-projection-proof --strict`;
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` compared against
      an origin/main baseline; `python3 scripts/validate-openspec-cli-pin.py
      --all` (the pinned 1.12.0 entrypoint, which is the gate);
      `python3 scripts/validate-sequenced-after.py .`;
      `python3 scripts/doc-health.py --single-repo . --fail-on error` compared
      against the same baseline.
- [ ] 6.2 **The gate-side check (OQ-1 option B) is NAMED AS THE SUCCESSOR and
      not proposed here.** No owner is assigned and no issue is filed by this
      packet; filing one is a separate act. Recorded so that "we decided
      against a gate" is never read off this packet's silence.
- [ ] 6.3 **The three owed row-level fields** — `row-grc-0001`'s `grant_ref`,
      its `expires_at`, and `projected_from.staleness_bound` verbatim — stay
      OWED to whoever next has operator cause to read that ConfigMap, exactly
      as walk record §14.1 recorded them. This packet requires that they be
      NAMED as owed; it does not read them.
- [ ] 6.4 **hermes-install #89 (FR-021 first-parent merge-commit reach) is
      NOT this packet's subject.** It was surfaced by the same ceremony and is
      a separate defect in a separate repository; named so the two are not
      conflated by a later reader.
- [ ] 6.5 **Rule 1 claim and Rule 6 landing window are owed at landing, not at
      draft.** The lane-collision protocol's CLAIMED comment and the
      `LANDING`/`LANDED` posts fire when this packet's pull request is taken
      out of draft and merged (it touches `openspec/changes/` and the README
      OpenSpec Records block); nothing is posted by the draft.
