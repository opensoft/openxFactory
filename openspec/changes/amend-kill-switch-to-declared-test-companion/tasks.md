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
      branch measures the same 3 and no others. This pull request also moves
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
      `openxfactory-floor-regeneration`** — each MEASURED the same way:
      withdraw THAT CLASS ALONE in a scratch tree, run the pinning suite and
      collect the failing node ids, then COMMIT that withdrawal as the baseline
      and regenerate each golden/snapshot artefact by its own allowlisted
      regeneration, reading the paths `git diff --name-only <baseline-commit>`
      reports changed. Each companion is declared using design.md
      D-2c's grammar, **IN the envelope beside the candidate it belongs to**,
      as comment lines: `# companion: <pytest node id>` for every assertion
      that pins that enrolment, and `# companion-artefact: <repo-relative path>
      regenerate: <identifier>` for every golden/snapshot file whose recorded
      value moves with it — **the `regenerate:` FIELD IS AN ALLOWLISTED
      IDENTIFIER AND NEVER A COMMAND**. The envelope is a pull-request-editable
      file and 3.2 runs inside a REQUIRED check, so the declaration carries a
      BARE TOKEN and nothing executable. This task therefore also adds, IN THE
      TRUSTED CONFORMANCE TEST MODULE under codexFactory's `tests/merge-master/`
      (code-owner-reviewed test code), the fixed `identifier -> argv` TABLE that
      resolves each declared identifier — an argv list, no shell, a fixed cwd of
      the repository root — so that an identifier ABSENT FROM THE TABLE fails the
      check and an edit to a declaration can never introduce execution. Adding an
      identifier is a reviewed test-code change, not a declaration edit. **An
      artefact with no declared, resolvable identifier cannot be declared**, so
      where a declared artefact has none this task SUPPLIES ONE (a
      recording/regeneration entry point in codexFactory, plus its table row)
      before the artefact may be named. In the ENVELOPE the edit stays
      comment-only: **no schema member is added** to any candidate mapping, no
      `active:` boolean, no repository variable, and no candidate MAPPING moves.
- [ ] **3.2 The conformance test — RUN PER CLASS, OVER A COMMITTED
      POST-WITHDRAWAL BASELINE, AND IT IS TWO EQUALITIES PLUS A NON-EMPTINESS
      CHECK.** ONE codexFactory test that, per D-2c's grammar and for **EACH
      enrolled candidate class**, does this IN ORDER:
      **(0) THE BASELINE** — in a scratch tree, withdraw THAT class alone (its
      candidate mapping and its companion comment lines removed, nothing else)
      and **COMMIT that withdrawal as the BASELINE COMMIT**. Every measurement
      below is taken against it. Without the baseline the measuring tree already
      carries the withdrawal edit, so a whole-tree diff would report
      `.github/merge-approval-envelope.yml` itself and the artefact equality
      could never hold however correct the regeneration was.
      **(i) ASSERTIONS** — run the pinning suite on that tree and assert that the
      set of failing node ids EQUALS that class's declared `# companion:` set
      exactly, both directions, order-free, **and that the set is NOT EMPTY**: an
      enrolment whose withdrawal fails no assertion is exactly the one that could
      leave unnoticed, so an empty measured set is a FAILING check and the
      enrolment is recorded as non-conformant for lacking a pinning assertion —
      never a vacuous pass on two empty sets.
      **(ii) ARTEFACTS** — THEN regenerate each declared artefact by ITS OWN
      declared `regenerate:` IDENTIFIER, resolved to fixed argv by the trusted
      module's table (argv list, no shell, fixed cwd; an unknown identifier fails
      the check rather than being executed), and assert that the set of paths
      **`git diff --name-only <baseline-commit>`** reports changed EQUALS that
      class's declared `# companion-artefact:` set exactly — **no more, no
      less** — both directions, order-free. Because the withdrawal is already IN
      the baseline, that delta holds ONLY what the regeneration wrote. **The diff
      is NOT path-scoped to the declared set**, precisely so that a regeneration
      writing a path NOBODY DECLARED still fails the check.
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
      to read the enrolment from the envelope.
- [ ] **3.4 The suite is green.** codexFactory's required `validate` check
      passes, `tests/merge-master/` included, on the companion's pull request.

## 4. The observation this unblocks — parent box 3.6

**THE PARENT'S BOX 3.6 IS TICKED ON THE PARENT'S OWN PACKET, NOT HERE, AND NOT BY
THIS PULL REQUEST.** It is an OBSERVATION box: it owes a throw, an observation
and a restore on a real bot cycle. None of those is performed by naming a
successor.

- [ ] **4.1 The throw is ONE pull request.** In codexFactory: the
      `openxfactory-floor-regeneration` candidate entry's removal **together
      with exactly the declared companion**, and nothing else — landable against
      the repository's required checks, and taken on a real bot cycle rather
      than on a manufactured one.
- [ ] **4.2 Observe the withdrawal.** The next real `floor/bot-regeneration` pull
      request reaches **no envelope decision** — `is_candidate: false`, exit 11
      (`_EXIT_NOT_CANDIDATE`), `decision=skip`, **no sticky comment** (the
      "Explain park or block" step is gated on `decision == 'park'`) — and stays
      at the human merge gate.
- [ ] **4.3 Restore by revert** of that same pull request, so the entry and the
      companion assertions return in one act.
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
