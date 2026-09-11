# Tasks: amend-kill-switch-to-declared-test-companion

Status: draft

**THE AUTHORITY FOR THIS PACKET'S EXISTENCE, AND ITS LIMIT.** Brett Heap,
2026-09-11 at approximately 03:40Z, in session to lane `openxfactory-2`
(display `openXfactory-2`), presented with the lane's MULTI-CHOICE question,
selected the option **"Accept the finding; file a successor"** — a SELECTION,
not a typed sentence. Recorded on openxFactory #745 comment 5632569506
(2026-09-11T09:42:11Z,
https://github.com/opensoft/openxFactory/issues/745#issuecomment-5632569506)
and on codexFactory #232 (2026-09-11T09:42:12Z). The ruling's consequence (3),
verbatim: ***"a SUCCESSOR change is to be filed in openxFactory amending N-4 to
state the switch as it truly is — one reviewed edit plus its declared test
companion (or, alternatively, making the pinning suite kill-switch-aware) — so
that a later throw is landable and the box can be observed"***. Consequence
(4), verbatim: ***"3.6's observation resumes only after that successor lands and
a real bot cycle exists."***

**THAT WORD AUTHORIZED THE FILING AND NOTHING FURTHER. FILING ≠ RATIFYING.**
This pull request is a PROPOSAL: it admits no text to canon, ratifies no design
decision, moves no byte in either repository, throws no switch, and **ticks no
box anywhere — including the parent's box 3.6**, which is an OBSERVATION box and
does not tick on a successor being named. Every box below is `- [ ]`.

## 1. Pre-ratification asks — Brett Heap's acts, and no agent may take them

- [ ] **1.1 Ratify or refuse this packet's TEXT.** The ask is over the
      `## MODIFIED` requirement delta at
      `specs/roles-authority-model/spec.md` and the account of decision **N-4**
      that `proposal.md` § *THIS FILING AMENDS A RATIFIED DECISION (N-4) BY
      SUPERSESSION* sets out: that the kill switch is **one reviewed edit PLUS
      ITS DECLARED TEST COMPANION**, and that an enrolment whose withdrawal
      (companion applied, nothing else) is not landable against the required
      checks is non-conformant. Ratification admits the TEXT only. It performs
      no realization in either repository, throws no switch, and does not by
      itself tick the parent's box 3.6.
- [ ] **1.2 Veto or let stand D-1 … D-6** (`design.md` § 2). Each is one edit
      away and none is separately ruled by a ratification of 1.1 unless the
      owner says so. The two most worth a veto: **D-1**, the choice of
      alternative (A) over alternative (B) "make the pinning suite
      kill-switch-aware" — rejected because a suite that adapts to the entry
      leaving no longer notices it leaving; and **D-3**, that the golden
      behaviour digest IS part of the declared companion, with the throw and the
      restore each recorded as a movement.
- [ ] **1.3** On Brett Heap's ratifying word (1.1), and in ONE commit: ADD
      `approved_by`/`approved_on` beside the drafting pair in `.openspec.yaml`
      (`kind` and `id` unmoved; `document-lifecycle` § Proposal origin
      declaration), flip every `Status: draft` header in this packet to
      `Status: ratified` + `Ratified by:` with the citation, write
      `review/ratification-<date>.md` carrying `Status: ratified` and ONE
      citation of the word, and move the README row's status. The lane
      encodes; the word is his.

## 2. The filing — what this pull request contains

- [ ] **2.1** `specs/roles-authority-model/spec.md` carries a single
      `## MODIFIED Requirements` block whose header is **EXACTLY** the parent's,
      `### Requirement: An enrolled autonomous lane carries a one-edit kill
      switch`, whose first body line carries **SHALL**, and which keeps every
      parent scenario's intent — the amended "Withdrawing an enrolment", the
      restated and BROADENED "A kill switch outside the diff" (the parent's
      "repository or environment setting" widened to name secrets and any
      other value that does not appear in a reviewable diff), and THREE added
      scenarios ("The companion is declared beside the declaration", "An
      undeclared companion is a finding against the enrolment" and "An enrolment
      nobody would notice leaving is refused") — with nothing silently dropped.
- [ ] **2.2** `proposal.md`'s SECOND heading states the supersession in its own
      words: **THIS FILING AMENDS A RATIFIED DECISION (N-4) BY SUPERSESSION, AND
      SAYS SO HERE**, quoting N-4 verbatim and naming the clause that is
      measured false.
- [ ] **2.3** `.openspec.yaml` carries the provenance: the finding with its
      figures, the two records, the authorizing SELECTION verbatim with its time
      and place, that the parent's box 3.6 stays open and is an observation box,
      and that filing ≠ ratifying.
- [ ] **2.4** `README.md` carries ONE new row at the HEAD of the `Active
      changes:` list under `## OpenSpec Records`, naming the status, the lane,
      the authority and **FILING ≠ RATIFYING**.
- [ ] **2.5** `sequenced_after: [extend-merge-master-envelope-to-floor-bot-lanes]`
      resolves, `OPENSPEC_TELEMETRY=0 openspec validate
      amend-kill-switch-to-declared-test-companion --strict` is clean, and
      `openspec validate --all --strict` has its failure set UNCHANGED from
      `main` — requiring `--all --strict` clean outright is unsatisfiable: the
      repository's gate is per-change strict-clean plus `--all --strict` with
      the failure set unchanged from `main`. Measured 2026-09-11 against
      `main` at `54c166cf` and re-measured at `78d2c6f5` after this branch
      merged main: 3 pre-existing failures, stable across both
      (`change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle`,
      `spec/repo-boundary-governance`), none of them this packet's own; this
      branch measured the same 3 and no others. RE-MEASURED 2026-09-11 against
      `main` at `38c076d1`: 2 pre-existing failures
      (`change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle` —
      `spec/repo-boundary-governance` has since been fixed on `main`), and this
      branch measures the same 2 and no others. This pull request also moves
      two bookkeeping rows in `tests/sequenced_after/corpus-ledger.yaml` —
      its own row and the parent's `sole` → `co-modifier` flip — seeded by
      `scripts/validate-sequenced-after.py --seed-ledger --moved-by '#959'`;
      they carry no requirement and no grant.

## 3. Realization — NOT PERFORMED BY THIS PULL REQUEST; a codexFactory companion change, authored by that repository's lane after ratification

**No byte below is written by this lane or by this pull request.** openxFactory's
half of this packet is text. The realization is a **companion change in
codexFactory**, authored there, exactly as
`extend-merge-master-envelope-to-floor-bot-lanes` split its own halves.

- [ ] **3.1 The banner correction and the companion declarations — FOR EVERY
      ENROLLED CANDIDATE CLASS, WITH NOTHING GRANDFATHERED.** The requirement
      binds every enrolled candidate class and this packet grandfathers none.
      In codexFactory: correct the banner sentence that repeats N-4's false
      "one edit" claim, and DECLARE a test companion for **EVERY candidate
      class enrolled in `.github/merge-approval-envelope.yml` at realization
      time — today TWO, `codexfactory-routine-code` and
      `openxfactory-floor-regeneration`** — each MEASURED BY **THE FIVE-STEP
      PROCEDURE OF 3.2 BELOW, IN THAT ORDER**, which is this packet's single
      statement of it and is not restated here: capture the declarations from
      the pre-withdrawal envelope, commit the withdrawal as the baseline,
      measure the assertions over the whole pinning suite with the conformance
      module excluded by its own path, regenerate every allowlisted artefact and
      diff against the baseline commit, record. Each companion is declared using
      design.md D-2c's grammar, **IN the envelope beside the candidate it
      belongs to**,
      as comment lines: `# companion: <pytest node id>` for every assertion
      that pins that enrolment, and `# companion-artefact: <repo-relative path>
      regenerate: <identifier>` for every golden/snapshot file whose recorded
      value moves with it — **the `regenerate:` FIELD IS AN ALLOWLISTED
      IDENTIFIER AND NEVER A COMMAND**. The envelope is a pull-request-editable
      file and 3.2 runs inside a REQUIRED check, so the declaration carries a
      BARE TOKEN and nothing executable. This task therefore also adds, IN THE
      TRUSTED CONFORMANCE TEST MODULE under codexFactory's `tests/merge-master/`
      (code-owner-reviewed test code — a module EXCLUDED BY ITS OWN PATH from
      every measurement and never itself measured, 3.2 steps 1 and 3), the fixed
      `identifier -> argv` TABLE that resolves each declared identifier — an
      argv list, no shell, a fixed cwd of
      the repository root — so that an identifier ABSENT FROM THE TABLE fails the
      check and an edit to a declaration can never introduce execution. Adding an
      identifier is a reviewed test-code change, not a declaration edit. **An
      artefact with no declared, resolvable identifier cannot be declared**, so
      where a declared artefact has none this task SUPPLIES ONE (a
      recording/regeneration entry point in codexFactory, plus its table row)
      before the artefact may be named. In the ENVELOPE the edit stays
      comment-only: **no schema member is added** to any candidate mapping, no
      `active:` boolean, no repository variable, and no candidate MAPPING moves.
      **AND THIS REALIZATION MOVES NOTHING IN THE PINNING SUITE.** It adds the
      declarations and the trusted conformance module and nothing else: no
      pinning assertion is re-targeted, deleted, skipped, weakened or rewritten,
      and no golden artefact moves — **3.3 below stands, unqualified**. The
      conformance test of 3.2 is a MEASUREMENT taken in a throwaway scratch tree
      and it EDITS NOTHING in the repository; what it proves is that each
      class's declaration is COMPLETE AND EXACT (declared equals measured, and
      the measured set is not empty). Its value is that the THROW's author knows,
      BEFORE opening that pull request, exactly which assertions and which
      artefacts the withdrawal will move. APPLYING the companion is a LATER and
      SEPARATE act, in a later pull request, defined once at **3.6** below.
- [ ] **3.2 The conformance test — ONE PROCEDURE, FIVE NUMBERED STEPS, IN THIS
      ORDER, RUN PER ENROLLED CLASS.** ONE codexFactory test that, per D-2c's
      grammar and for **EACH enrolled candidate class**, performs exactly the
      sequence below. **THE ORDER IS PART OF THE RULE**: every later step
      consumes what an earlier step captured or committed, so a step taken out of
      order cannot hold. This list is the packet's SINGLE statement of the
      procedure; 3.1 above, `design.md` D-2b, the `## MODIFIED` scenarios and
      `proposal.md` point AT IT rather than restate it.
      **STEP 1 — CAPTURE THE DECLARATIONS, BEFORE ANYTHING IS EDITED.** Parse the
      envelope AS IT STANDS PRE-WITHDRAWAL and retain, for that class and by
      D-2c's discovery rule, (a) the declared `# companion:` PINNING NODE-ID SET
      and (b) the declared `# companion-artefact:` SET as (path,
      regeneration-identifier) pairs; and RESOLVE every declared identifier
      against the allowlist table in the trusted test module in this same step —
      an identifier absent from that table FAILS HERE, before a byte is edited,
      rather than being looked up elsewhere or executed, and a declared node id
      naming the conformance module itself is REFUSED HERE: that module is
      EXCLUDED BY ITS OWN PATH from the step-3 run, so such a node id could never
      enter the measured set and would break the equality by construction.
      The captured sets are the expected values every later step compares
      against: step 2 removes those very comment lines from the tree being
      measured, so a test that has not captured them first has no declaration
      left to compare against.
      **STEP 2 — WITHDRAW THAT CLASS ALONE AND COMMIT THE BASELINE.** In the
      scratch tree remove THAT class's candidate mapping and its companion
      comment lines and **nothing else**, and `git commit` that withdrawal as the
      **BASELINE COMMIT**. EVERY measurement below is taken in that committed
      tree and against that commit. Without the baseline the measuring tree
      already carries the withdrawal edit, so a whole-tree diff would report
      `.github/merge-approval-envelope.yml` itself and the artefact equality
      could never hold however correct the regeneration was.
      **STEP 3 — MEASURE THE ASSERTIONS OVER AN INDEPENDENT, COMPLETE PINNING
      INVENTORY, WITH THE CONFORMANCE MODULE EXCLUDED BY ITS OWN PATH.** Run the
      WHOLE pinning suite — `tests/merge-master/` in the committed baseline tree —
      with the conformance module itself EXCLUDED BY PATH (`pytest
      --ignore=<conformance module path>`), and let the set of FAILING node ids be
      the MEASURED SET. **WHAT IS RUN IS NOT TAKEN FROM THE DECLARATION**: the
      captured `# companion:` set is the EXPECTED value and nothing else, so a
      pinning assertion the declaration OMITS is still run, still fails, and still
      enters the measured set — which is exactly how an INCOMPLETE declaration is
      detected, and why the measured set may not be drawn from the declared one.
      Self-invocation is prevented by THE EXPLICIT EXCLUSION — the conformance
      module's own path, a CONSTANT IN TRUSTED TEST CODE and never a value read
      from any declaration — and NOT by narrowing the run: narrowing makes the
      equality circular, because a test that is never run can never enter the
      measured set. Assert that the MEASURED set EQUALS that class's captured
      `# companion:` set exactly, both directions, order-free, **and that the set
      is NOT EMPTY**: an enrolment whose withdrawal fails no assertion is exactly
      the one that could leave unnoticed, so an empty measured set is a FAILING
      check and the enrolment is recorded as non-conformant for lacking a pinning
      assertion — never a vacuous pass on two empty sets. An UNDECLARED pinning
      assertion that fails on this withdrawal is therefore IN the measured set and
      ABSENT from the declared one, the equality breaks, and the finding is
      recorded against THE ENROLMENT AND ITS DECLARATION — never against the suite
      that caught it (the `## MODIFIED` scenario "An undeclared companion is a
      finding against the enrolment").
      **STEP 4 — REGENERATE EVERY ALLOWLISTED ARTEFACT, AND DIFF AGAINST THE
      BASELINE COMMIT.** THEN run **EVERY REGENERATION IN THE TRUSTED MODULE'S
      ALLOWLIST TABLE — THE WHOLE TABLE, not only the identifiers this class
      declared** — each resolved to fixed argv by that table (argv list, no shell,
      fixed cwd of the repository root; a DECLARED identifier absent from the
      table has already failed at step 1 rather than being executed), and assert
      that the set of paths **`git diff --name-only <baseline-commit>`** reports
      changed EQUALS that class's captured `# companion-artefact:` PATH set
      exactly — **no more, no less** — both directions, order-free. **The
      INVENTORY IS INDEPENDENT OF THE DECLARATION on this half too**: an artefact
      that MOVES on this withdrawal but which no `# companion-artefact:` line
      names is regenerated anyway, appears in the changed-path set, is absent from
      the declared set, and breaks the equality — the same finding against the
      same enrolment, rather than an omission hiding inside its own measurement.
      Because the withdrawal is already IN the baseline, that delta holds ONLY
      what the regenerations wrote, and an allowlisted regeneration with nothing
      to do with this withdrawal writes nothing and so adds nothing to it. **The
      diff is NOT path-scoped to the declared set**, precisely so that a
      regeneration writing a path NOBODY DECLARED still fails the check.
      **STEP 5 — RECORD THE RESULT.** Report, per class, BOTH equalities and the
      non-emptiness result, and NAME THE CLASS AND THE STEP in any failure (step
      1 an unresolvable identifier or a self-naming node id, step 3 an
      assertion-set inequality or an empty measured set, step 4 an artefact-set
      inequality), so a red check says WHICH enrolment failed and WHERE rather
      than only that the conformance test failed.
      The artefact's movement is therefore MEASURED BY THAT REGENERATION DIFF
      and is NOT inferred: an existence check does not prove the declared path
      is the file whose recorded value moves, a node id does not identify the
      path its run rewrites, a recording test can fail for an unrelated reason,
      and a shared snapshot can change with no declared node id naming it.
      Existence remains necessary and is no longer the check. A stale
      declaration in EITHER half is a failing check rather than a discovery made
      when the switch is thrown.
- [ ] **3.3 Nothing else moves.** No candidate mapping, no ruleset, no bypass
      actor, no schema, no workflow logic, no `scripts/`, no `contracts/`, no
      relaxation of any existing assertion, and no rewrite of the pinning suite
      to read the enrolment from the envelope. **This binds the REALIZATION
      (3.1 and 3.2), which is the only act this section authorizes; it is not a
      description of the throw.** The throw is a later, separate pull request,
      and what applying the companion means there is defined once at **3.6** —
      re-targeting a declared assertion's expectation to the post-withdrawal
      tree is not a relaxation of it, and this task's bar on relaxation holds
      over the throw exactly as it holds here.
- [ ] **3.4 The suite is green.** codexFactory's required `validate` check
      passes, `tests/merge-master/` included, on the companion's pull request.
- [ ] **3.6 THE THROW, DEFINED — what "THE DECLARED COMPANION APPLIED" IS AS AN
      ACT.** Numbered for the parent's box 3.6, whose throw it defines; this
      section carries no 3.5. **This is the packet's SINGLE definition of
      applying the companion**; 3.1 and 3.3 above, 4.1 below and the `##
      MODIFIED` requirement POINT AT IT rather than restate it. The throw is not
      performed by the realization: it is a LATER codexFactory pull request,
      taken on a real bot cycle, carrying exactly three kinds of change and
      nothing else.
      **(i) THE WITHDRAWAL.** That class's candidate mapping AND its companion
      comment lines are removed from `.github/merge-approval-envelope.yml`.
      **(ii) THE DECLARED ASSERTIONS, RE-TARGETED — NEVER RELAXED.** For EACH
      declared `# companion:` node id, the MINIMAL REVIEWED EDIT to THAT
      ASSERTION'S EXPECTATION so that it holds in the POST-WITHDRAWAL tree: an
      enrolled-id list loses the withdrawn id; a helper asserting
      `len(matches) == 1` asserts the post-withdrawal count. The assertion is
      RE-TARGETED — never deleted, never skipped, never weakened — and it keeps
      NOTICING THE REMAINING ENROLMENTS exactly as it noticed this one.
      **(iii) THE DECLARED ARTEFACTS, REGENERATED.** For EACH declared
      `# companion-artefact:`, the file AS PRODUCED BY ITS OWN ALLOWLISTED
      REGENERATION (3.1's identifier table), with the golden digest's movement
      recorded in its movement log AS THE THROW (`design.md` D-3).
      **"AND NOTHING ELSE" IS A MEASURABLE BOUND, not an assurance:** the paths
      `git diff --name-only` reports for the throw pull request lie WITHIN the
      union of the envelope, the files holding the declared `# companion:` node
      ids, and the declared `# companion-artefact:` paths — and NO ASSERTION
      OUTSIDE THE DECLARED SET CHANGES.
      **LANDABILITY IS THEN A CONSEQUENCE, not a further hope:** every assertion
      that would fail is one this pull request re-targets, and every artefact
      that would move is one it regenerates, so codexFactory's required
      `validate` check passes ON THE THROW'S OWN TREE.
      **THE RESTORE IS A FORWARD CHANGE PRODUCED BY THIS SAME PROCEDURE — NEVER
      A REVERT** (4.3). It is ONE pull request carrying exactly the same three
      kinds of change IN THE OPPOSITE DIRECTION and nothing else: (i) the
      candidate mapping AND its companion comment lines RE-ADDED BYTE-IDENTICAL
      to the pre-throw declaration; (ii) each declared `# companion:` assertion's
      EXPECTATION re-targeted BACK to the enrolled tree, by the same minimal
      reviewed edit and never by deletion, skipping or weakening; (iii) each
      declared `# companion-artefact:` REGENERATED BY ITS OWN ALLOWLISTED TOOL in
      the RESTORED tree — which is what APPENDS THE RESTORE MOVEMENT to the golden
      digest's history (`design.md` D-3's second movement), exactly as the throw
      appended the first. The "AND NOTHING ELSE" measurable bound and the
      landability consequence are IDENTICAL to the throw's, because the act is the
      same act pointed the other way. **A `git revert` of the throw is REFUSED as
      the restore**: it DELETES the throw's recorded movement instead of RECORDING
      a restore, leaving the behaviour history with no trace that the switch was
      ever thrown — the opposite of the ledger this observation exists to produce.
      **The figures this makes declared rather than hidden.** At today's head the
      companion for `openxfactory-floor-regeneration` measures 29 assertions
      across FIVE test files plus the golden digest — the RESULT posted on
      openxFactory #745 at 2026-09-11T03:08Z — so the throw carries a SIX-FILE
      companion beside the envelope edit, which is exactly what N-4's "one edit"
      hid and what this packet makes declared, bounded and reviewable rather
      than pretending away.

## 4. The observation this unblocks — parent box 3.6

**THE PARENT'S BOX 3.6 IS TICKED ON THE PARENT'S OWN PACKET, NOT HERE, AND NOT BY
THIS PULL REQUEST.** It is an OBSERVATION box: it owes a throw, an observation
and a restore on a real bot cycle. None of those is performed by naming a
successor.

- [ ] **4.1 The throw is ONE pull request.** In codexFactory: the
      `openxfactory-floor-regeneration` candidate entry's removal **together
      with exactly the declared companion, APPLIED AS 3.6 DEFINES IT**, and
      nothing else — 3.6 is the single definition of that act and states the
      measurable bound that "nothing else" carries — landable against the
      repository's required checks, and taken on a real bot cycle rather than on
      a manufactured one.
- [ ] **4.2 Observe the withdrawal.** The next real `floor/bot-regeneration` pull
      request reaches **no envelope decision** — `is_candidate: false`, exit 11
      (`_EXIT_NOT_CANDIDATE`), `decision=skip`, **no sticky comment** (the
      "Explain park or block" step is gated on `decision == 'park'`) — and stays
      at the human merge gate.
- [ ] **4.3 Restore — a FORWARD change by the same procedure as the throw, NEVER
      a revert**, as **3.6** defines it: ONE pull request re-adding that class's
      candidate mapping and its companion comment lines byte-identical to the
      pre-throw declaration, re-targeting each declared assertion's expectation
      back to the enrolled tree, and REGENERATING each declared artefact by its
      allowlisted tool — so the entry and the companion assertions return in one
      act AND the golden digest records the RESTORE as its own movement beside the
      throw's, rather than losing the throw's movement to a reverted patch.
- [ ] **4.4 Observe approval resume** on the following real bot cycle.
- [ ] **4.5 Record it** on openxFactory #745 and codexFactory #232, and tick the
      parent's box 3.6 **THERE, on the parent's packet** — never here.

**A real bot cycle is required and does not exist today.** Hourly
floor-regeneration has reported "nothing owed" since 2026-09-10T17:22Z, and an
APPROVE cannot be constructed by hand because the class pins `expected_author:
openxfactory[bot]`. Consequence (4) of the ruling says exactly this: the
observation resumes only after this successor lands **and** a real bot cycle
exists.

## 5. Archive

- [ ] **5.1** Archive through **`proposal-support`**, never bare `openspec`, on
      (a) this pull request merged, (b) green realization evidence from the
      codexFactory companion (3.4), (c) the parent
      `extend-merge-master-envelope-to-floor-bot-lanes` PROMOTED — because this
      packet's `## MODIFIED` targets that change's own unarchived addition — and
      (d) Brett Heap's word. **THIS PACKET IS NOT ARCHIVABLE WHILE ANY ENROLLED
      CANDIDATE CLASS LACKS A DECLARED COMPANION AND A PASSING CONFORMANCE TEST
      OVER BOTH EQUALITIES.**
      The condition is PER CLASS, not per packet: green evidence for
      `openxfactory-floor-regeneration` alone does not satisfy (b) while
      `codexfactory-routine-code` is enrolled and undeclared, and a class
      enrolled later by another change carries the same block. No contract
      bundle is cut, no `contract_bundle_version` is spent and no release tag
      is owed.
