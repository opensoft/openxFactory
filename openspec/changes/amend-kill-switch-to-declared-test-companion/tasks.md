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

## 2. The filing — what this pull request contains

- [ ] **2.1** `specs/roles-authority-model/spec.md` carries a single
      `## MODIFIED Requirements` block whose header is **EXACTLY** the parent's,
      `### Requirement: An enrolled autonomous lane carries a one-edit kill
      switch`, whose first body line carries **SHALL**, and which keeps every
      parent scenario's intent — the amended "Withdrawing an enrolment", the
      unchanged "A kill switch outside the diff", and two added scenarios — with
      nothing silently dropped.
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
      `openspec validate --all --strict` is clean.

## 3. Realization — NOT PERFORMED BY THIS PULL REQUEST; a codexFactory companion change, authored by that repository's lane after ratification

**No byte below is written by this lane or by this pull request.** openxFactory's
half of this packet is text. The realization is a **companion change in
codexFactory**, authored there, exactly as
`extend-merge-master-envelope-to-floor-bot-lanes` split its own halves.

- [ ] **3.1 The banner correction and the companion declaration.** In
      codexFactory `.github/merge-approval-envelope.yml`, in the BANNER/COMMENT
      block beside the `openxfactory-floor-regeneration` candidate: correct the
      sentence that repeats N-4's false "one edit" claim, and DECLARE that
      candidate's test companion — naming the exact files and the assertion(s)
      each carries. A comment-only edit: **no schema member is added**, no
      `active:` boolean, no repository variable, and the candidate MAPPING
      itself does not move.
- [ ] **3.2 The conformance test.** ONE codexFactory test asserting that the
      DECLARED companion equals the set of assertions that actually pin the
      enrolment, so a stale declaration is a failing check rather than a
      discovery made when the switch is thrown.
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
      (d) Brett Heap's word. No contract bundle is cut, no
      `contract_bundle_version` is spent and no release tag is owed.
