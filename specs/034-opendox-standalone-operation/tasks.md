# Tasks: openDox standalone operation (release 1)

Status: draft

**Input**: [`spec.md`](./spec.md), [`plan.md`](./plan.md), [`research.md`](./research.md),
[`clarify-questions.md`](./clarify-questions.md), and #1144's ratified
`openspec/changes/add-neutral-product-standalone-operability/tasks.md`, which
holds the boxes and every falsifier.
**Lane**: `openxfactory-4`

## Format

`- [ ] T### [P?] [US#] [repo] Title`, followed by up to seven lines:

- **Realizes**: the #1144 boxes the task closes, or advances when marked
  "(part)".
- **Falsifier**: the #1144 falsifier or named test the task must pass, quoted
  in its PR.
- **Blocked by**: the open `R1Q` questions, if any. No task starts while one
  of these is open (FR-012). None is open, so no task carries this line.
- **Ruled**: the answered `R1Q` questions whose answers the task carries out.
  A ruled question no longer blocks. Brett Heap answered them on `#656`, in
  three rounds:
  - round 1a, comment `5817152735` (2026-09-24T15:31:46Z), verbatim *"(a) on
    all eleven, (d) on R1Q6"*: R1Q1–R1Q9, R1Q20 and R1Q22;
  - round 2, comment `5850003126` (2026-09-26T21:23:03Z), verbatim *"go with
    recommendations on all the open questions"*: fourteen more, each answered
    with the option `clarify-questions.md` recommended;
  - round 3, comment `5851950767` (2026-09-27T02:25:29Z), verbatim *"(a) Admit
    the two edits (Recommended)"* and *"(a) Own three, others by tree
    (Recommended)"*: R1Q26 and R1Q27, which round 2's analyze raised. Brett
    kept R1Q26 (a) on comment `5852513402` (2026-09-27T04:08:46Z), verbatim
    *"Keep (a) as ruled (Recommended)"*, once shown the unlisted route W2-10.
- **Ruling needed**: a change to #1144's requirement or scenario TEXT that an
  answer implies. It goes back to Brett Heap (plan.md § "Ruling needed"), and
  it holds only the part of the task it names. RN-1, the one so far, was
  ruled (a) in `5850003126`.
- **After**: tasks that must land first.
- **Lands with**: a task whose change rides in the same PR. Neither task waits
  for the other, so neither names the other on its `After:` line.

An `After:` entry such as `T007 (batches C and F)` waits for those batches of
T007 alone, and a bare `T007` waits for every batch. T007's `After, by batch`
field gives each batch its own line. The plan-consistency tools read each
batch as a node of its own, so the graph they check is
the one this file states. There are twelve batches, `T007.A` to `T007.L`. A
task that waits on some of T007's batches may still run beside a task that
another batch waits for (T006).

A task with no `[P]` either shares a file with a neighbour or depends on one.

- **Stories**: US1 (it runs), US2 (useful alone), US3 (installs) and US4 (the
  governed host unchanged). Holder tasks carry no story tag.
- **Repositories**:
  - `[oDc]` opensoft/openDox-code
  - `[oXc]` opensoft/openXdox-code
  - `[oD]` opensoft/openDox (root)
  - `[oX]` opensoft/openXdox (root)
  - `[oxF]` opensoft/openxFactory
  - `[oDs]` opensoft/openDox-spec (T053, since R1Q11 is answered (a))

  No task touches opensoft/openXdox-spec, because R1Q12 is answered (a). T003
  recorded its base all the same.
- **Falsifier labels**: `F<g>.<n>` is the n-th `FALSIFIED BY` box of #1144's
  Group g, in document order. `research.md` § Appendix `box_census.py` prints
  every label.

Every realization task lands through its repository's own PR, with the `Arc:`
and `Lane:` trailers (T091). T066 is the one openxFactory act that is not an
arc landing, and it carries no `Arc:` trailer (plan.md § "The trailer, the
guard and Rule 6"). Only the holder lands. Every writer works in its
OWN clone, runs `cd <clone> || exit 1` in every call, and names the repository
with `-R` in every `gh` call.

## What can start

Brett Heap has answered all 27 questions on `#656`. The eleven that
phase 1 needed were answered on comment `5817152735` (verbatim *"(a) on all
eleven, (d) on R1Q6"*), and T004 encoded them. Fourteen more were answered on
comment `5850003126` (verbatim *"go with recommendations on all the open
questions"*), which also ruled RN-1 (a). T019, T009 and T069 encode that
second round in this revision, for phase 1's openXdox-code tail, phase 2 and
phase 3. Round 2's analyze raised R1Q26 and R1Q27
(`evidence/analyze-round-2.md`), which Brett answered (a) on comment
`5851950767`, and T067 encodes them in a bookkeeping PR of its own. T001 and
T003–T006 are done, and their evidence is in `evidence/`. Every phase is
planned on answers.

- **The holder's own tasks**: T002 is a standing act, one claim per slice.
  T008 was raised as a staged topic (#1173), and the arc it raised is still
  open. T007's batches A to L have landed, from A (#1171) to L (#1212, on
  Brett Heap's second word of 2026-09-30, `5920216845`), and T007 lists each.
  Brett Heap's `5962785556`, item 2, rules a batch M, which this plan does
  not list yet.
- **Each phase-1 task** starts once its slice has been claimed (T002).
  **T020** and **T030** never needed an answer. **T030** lands with T011,
  because it fails until 2.1 lands. **T043** also waits for T007's batches C
  and F.
- **R1Q25 (b) returned T061 (7.3) to phase 2**, beside openDox's own validator
  (T057, T058). Until T061 lands, phase 1's openXdox-code check declares
  `tests/test_snapshot.py` in its exclusion with its own reason (T043).
- **Phase 1's CLOSE** (T049) waits on T007's batches A, B, D, F and J, among
  the tasks its `After:` line names.
- **Phases 2 and 3** each start once the phase before them has closed: every
  phase-2 task comes after T049, and every phase-3 task after T063, through
  its own `After:` line. In phase 2, T059, T060 and T061 also wait on T007's
  batch I. Each phase's writer slices are below its phase-1 counterpart, in
  § "Phase 2 writer slices" and § "Phase 3 writer slices".

---

## Phase 0: preconditions (holder)

- [x] T001 [oxF] **Ratification record, and 3.0.** DONE: #1151 landed as
  `cd494e4c` (2026-09-24T14:54:27Z), under its own Rule 6 window. It ticks 1.8
  and 3.0, citing `5815412869` (*"ratify #1144"*, which struck nothing) and
  `review/ratification-2026-09-24.md` § 2.
  - **Realizes**: 3.0.
- [ ] T002 **Claims, per slice.** Post a `CLAIMED` on `#656` before each slice's
  PR (Rule 1), naming its task ids. Do the three sibling reads first:
  - the claims on `#656`;
  - `gh pr list -R <repo> --state all --search <slug>`;
  - `git ls-remote --heads origin | grep <slug>`.

  Lane 4's C3 and C4 have landed, so a slice starts from them and duplicates
  neither (plan.md § "In-flight overlaps").
- [x] T003 **ARC_BASE.** DONE: `evidence/arc-base.md` (2026-09-25). No
  repository holds an arc landing yet, so each base is that repository's `main`
  at the time. Record, per repository, a `main` commit before the
  arc's first landing there: openDox-code, openXdox-code, openDox, openXdox,
  openxFactory, openDox-spec and openXdox-spec. The two spec legs' bases are
  recorded unconditionally, so they were in place when T009 selected T053
  (R1Q11 (a)). R1Q12 was answered (a), so openXdox-spec, whose base is
  recorded too, is touched by no task. Any commit before a repository's first arc landing serves:
  `$ARC_BASE..HEAD` leaves ARC_BASE itself out, and the guards read only
  trailered landings. So it is recorded now, before phase 1 starts. For
  openxFactory's guard,
  `PACKET_MERGE` is `94b6f7f1` (11.1). Record them in `evidence/arc-base.md`,
  with no `Arc:` trailer.
  - **Ruled**: R1Q20 (a), `5817152735`.
- [x] T004 **Round 1a: encode the eleven phase-1 answers.** DONE in #1155.
  The answers of `5817152735` (R1Q1–R1Q9, R1Q20, R1Q22) are in
  `spec.md` § Clarifications, in `clarify-questions.md`, and in this file as
  `Ruled:` lines.
  - Every answer that amends a #1144 falsifier or task line is handed to T007.
  - The one scenario text an answer touches is RULING NEEDED RN-1 (plan.md
    § "Ruling needed").
  - Phase 1 is re-planned on the answers.

  The later rounds are T009 (phase 2) and T069 (phase 3).
- [x] T005 **Re-measure.** DONE: `evidence/remeasure-2026-09-25.md`. Re-run
  research R1–R15 at the then-current `main`s,
  using the persisted tools. Record the drift from the 2026-09-24 figures in
  `evidence/remeasure-<date>.md`, with no `Arc:` trailer (R13 already shows
  one pin drifting). A figure that moved re-plans the slice it feeds, before T006.
  - It runs openXdox-code's WHOLE suite at the then-current tip, not only the
    22 protected suites research ran under the shim, and records whether
    `tests/test_snapshot.py`'s three failures (research R11) cleared once C3's
    PR 2 landed (T043).
  - **What it found.** openDox-code, openDox-spec, openXdox-spec and the openDox
    root are unchanged, and so is every figure the openDox-code slices use.
    - `tests/test_snapshot.py` still fails two of the three cases that
      research R11 recorded. The validator lookup is fixed, but the schemas
      are not: they are found only through `CONTRACTS_DIR`. So T061 came
      into phase 1, until R1Q25 (b) returned it to phase 2 (T019).
    - 5.4a's glob now selects seven suites, which bears on R1Q14.
    - The whole suite shows six causes that no task named. T040 takes the four
      that are carve residue, and R1Q24 asks about the two that reach
      openxFactory.
    - T019 is the round that applies the new answers.
- [x] T006 **Analyze round 1a.** DONE: `evidence/analyze-round-1a.md`
  (2026-09-25), CRITICAL 0. Its findings are dispositioned there, and this
  revision carries them. Run `/speckit-analyze` over spec, plan and
  tasks. No CRITICAL finding may stand before any phase-1 task starts (the
  constitution's workflow gate).
  - First set the feature context. `.specify/feature.json` is gitignored, so
    a fresh openxFactory clone has no feature pointer, and the prerequisite
    resolver refuses without one. Run from that clone, with this feature's
    files at the branch's head or on `main` once #1155 lands:

        export SPECIFY_FEATURE_DIRECTORY=specs/034-opendox-standalone-operation
        bash .specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks

    The check must print this feature's `FEATURE_DIR` before analyze runs.
  - Record that output, analyze's verdict and every finding with its
    disposition in `evidence/analyze-round-1a.md`, with no `Arc:` trailer.
  - T003, T005 and T006 can land their evidence together, in one bookkeeping
    PR. It touches only this feature's directory, and this feature's README
    entry, which sits outside the OpenSpec Records block. So it needs no Rule
    6 window.
  - **After**: T003, T004, T005.
- [ ] T007 [oxF] **Record the ruled amendments in #1144's `tasks.md`, and one
  addendum in its `design.md`.** The answers of `5817152735` and `5850003126`
  amend falsifiers, task lines, addenda and one design note (§ D4). They amend
  no requirement and no scenario, except RN-1's, which batch D carries on its
  own ruling. Batch K adds a dated note to requirement 17 on its own ruling
  (`5916000030`, item 1), and rewrites no requirement or scenario text. The
  full list is in § "Ruled amendments" below. Each batch is its own
  bookkeeping PR. T007 was ticked when batch J landed, and was reopened for
  batches K and L, both of which have landed.
  - Every PR touches `openspec/changes/`, so it lands under a Rule 6
    `LANDING`/`LANDED` window.
  - It carries no `Arc:` trailer (R1Q20 (a)), so 11.1's guard never reads it.
  - It carries no closing keyword. Each amended line cites the ruling it
    carries out: `5817152735` for batches A, B, C and E, and `5850003126` for
    batches D, F, G and H, `5851950767` for batch I, `5870594693` for
    batch J, `5916000030` for batch K, and `5920216845` for batch L.

  - **Batch A** holds the F3.1, 2.2, 3.2, 4.3, 10.1, 11.0, 11.1 and F11.1
    amendments. It lands before T047, whose openxFactory landing edits the
    parity test that batch A names in F11.1, and so before T049.
  - **Batch B** holds F9.1 for openXdox-code, 9.2 and 9.4. It lands once T041
    names its exclusion file, and before T049.
  - **Batch C** holds F5.2 and 12.5's falsifier. It lands before the first
    respelling edit to a protected suite, and before T059, whose falsifier
    reads the allow-list.
  - **Batch D**, on RN-1 (a), ruled in `5850003126`: requirement 3's fourth
    scenario as ruled, and the added after-build refusal scenario, in #1144's
    spec delta. It is the amendment the ruling's own words send through the
    change. LANDED as #1170 → `79a720a2`, before T049 as it must.
  - **Batch E** adds to F11.1's named set each openxFactory composition test
    that phase 1 moves or finds: `test_session_harness.py` or
    `test_outline_model.py`'s `doc_health` case if T035 or T034 moves one, and
    any test that fails at T047's new pin, as P1-K's writer finds it. It
    lands before T047.
  - **Batch F** holds the amendments that T019's answers imply. F5.2 admits
    T061's two edits to protected suites (R1Q14 (a)). F9.1 and 9.2 admit three
    more exclusion reasons (R1Q24 (a), R1Q25 (b)), and 9.2 gains its
    phase-3 close as an addendum to the release map (R1Q25 (b)). F7.1 is
    unchanged. It lands before T043 and T061.
    - Two of its lines extend what another batch adds: F5.2's allow-list is
      batch C's, and F9.1's exclusion is batch B's. Each names what it extends
      by the ruling behind it, R1Q7 (a) or R1Q6 (d) (`5817152735`), so it
      reads the same whichever batch lands first. Of two batches that amend
      one line, the later rebases onto the earlier.
  - **Batch G** holds the amendments that T009's answers imply: the 4.3
    addendum (R1Q10 (a)), 5.3 (R1Q11 (a)), 7.0 and 7.1 (R1Q11 (a), R1Q12
    (a)), the 9.5 addendum (R1Q11 (a)) and F5.2's environment line (R1Q23
    (a)). It lands before T053, phase 2's first landing, and so before every
    phase-2 task that follows T053. 5.3a's `values` block, which R1Q11 (a)
    also implies, is batch I's, because R1Q26 (a) decided how the block
    lands.
  - **Batch H** holds the amendments that T069's answers imply: F10.1 and 10.3
    (R1Q15 (b), R1Q16 (iii)), the 13.4 addendum (R1Q15 (b)), the 13.1
    addendum and F13.1 (R1Q16), and the 16.3 addendum (R1Q17 (b), R1Q18 (a)).
    It lands before T070, T075 and T080, and so before every phase-3 task
    that runs an amended line.
  - **Batch I** holds the amendments that T067's answers imply: 5.3a admits
    the facet's `values` block beside its one stage (R1Q26 (a), with R1Q11
    (a)); 12.5's falsifier admits `tests/test_gate_loop_views.py`'s two facet
    edits, each with its reason (R1Q26 (a)); and 7.3 and F7.1 read the second
    named test as every schema that install validates (R1Q27 (a)). It lands
    before T059, T060, T061 and T063.
  - **Batch J** holds the one amendment that `5870594693` implies, which
    Brett Heap ruled *"(b) Amend F9.1 to deselect it (Recommended)"* after
    `5859927858`. F9.1's openXdox-code exclusion takes a fourth entry, the
    31-entry help-tree test, deselected for the reason `5859927858` gives
    (`cli_gate` imports `doc_health` at load time) until T008. T043 carries
    it out, and T008 removes it. It lands before T049, whose F9.1 run needs
    it. LANDED as #1193 → `6b97c601`.
  - **Batch K** holds the two amendments that Brett Heap's multi-choice word
    of 2026-09-30 implies (`5916000030`):
    - Item 1, *"Yes, amendment batch K (Recommended)"*: a dated note in
      requirement 17's body in #1144's spec delta, after its SHALL paragraph
      and above its scenarios, in batch D's form, with a pointer after batch
      H's 16.3 addendum. The note records how two rulings narrow requirement
      17's and scenario 17.1's "any endpoint". The loopback rule
      (`5880893901`) covers a credential the built-in resolver resolves, and
      the broker-path ruling (`5890601202`) covers a token a broker mints.
      Each is sent only over `https://`, or over `http://` to `127.0.0.1`,
      `[::1]` or `localhost`. The note rewrites no ratified text.
    - Item 4, *"Reword as reviewed entries (Recommended)"*: F5.2 admits
      T061's ten edits to protected suites as R1Q7 (a) entries, each keeping
      its real assertions and changing only the walk premise to 7.3's
      answer. One landing's several entries for one suite chain in the order
      listed. F5.2's call passes `--chains`, and 12.5's call does not.

    It lands before T061 (openXdox-code#36), and so before T063, whose F5.2
    run needs it, and before T080 (openDox-code#63) and openDox-code#64.
    LANDED as #1210 → `39f19145`.
  - **Batch L** holds the one #1144 amendment that Brett Heap's multi-choice
    word of 2026-09-30 (`5920216845`) implies. Item 1, *"Fix in T084 + #1144
    note (Recommended)"*, is an addendum at 4.3, after batch G's. It records
    that a flag in the served `/capabilities` payload's `actions` map whose
    affordance is a route this server serves is true only where such a route
    answers. So `gate` and `refresh` read false standalone, and a composed
    host reads as today. `notebook`, `edit`, `session` and `intent` keep
    their conditions, and the three late reaches that drop a connection
    answer through their seams or refuse cleanly, as 4.2 requires. Items 2
    and 3 amend nothing in #1144:
    T085 and T084 carry them. It lands before T084.
    LANDED as #1212 → `2140f5a7`.

  A realization PR that lands before its batch still quotes the falsifier as
  the answer records it, citing the ruling.
  - **Realizes**: none of the 69 boxes. It records the word the realization
    carries out.
  - **Ruled**: R1Q1, R1Q2, R1Q3, R1Q5, R1Q6, R1Q7, R1Q9, R1Q20 and R1Q22,
    `5817152735`; R1Q10, R1Q11, R1Q12, R1Q14, R1Q15, R1Q16, R1Q17, R1Q18,
    R1Q23, R1Q24 and R1Q25, `5850003126`; R1Q26 and R1Q27, `5851950767`;
    the help-tree deselect (no question), `5870594693`, citing
    `5859927858`; items 1 and 4 of `5916000030`, with the loopback rule
    `5880893901` and the broker-path ruling `5890601202`; item 1 of
    `5920216845`.
  - **After**, by batch:
    - **A**: nothing.
    - **B**: T041, which names the exclusion file.
    - **C**: nothing.
    - **D**: nothing. RN-1 was ruled (a) in `5850003126`, and the batch has
      landed (#1170 → `79a720a2`).
    - **E**: T034 and T035, whose PR bodies list what they move, and T039 and
      T044. P1-K's writer names the red tests at the pins of those two
      commits, before its openxFactory PR opens. Batch E cannot wait on that
      PR's landing, which needs it.
    - **F**: T019.
    - **G**: T009.
    - **H**: T069.
    - **I**: T067.
    - **J**: nothing.
    - **K**: nothing, since `5916000030` is given. K lands before 7.3's
      landing (openXdox-code#36), and before 16.3's (openDox-code#63) and
      openDox-code#64's. This line names those landings by pull request,
      because a task id here would read as one K waits for.
    - **L**: nothing, since `5920216845` is given. L lands before the landing
      that routes 4.3's last reaches (P3-R's). This line names that landing
      by its slice, for the same reason as K's.
  - **Landed**: batches A to L, each an openxFactory PR with no `Arc:` trailer.
    A #1171 → `bca4a260`; B #1194 → `e369cb25`; C #1172 → `4663e9e8`; D #1170 →
    `79a720a2`; E #1183 → `b9742534`; F #1178 → `295abd8d`; G #1205 →
    `91e4685f`; H #1206 → `f99a2097`; I #1180 → `8421603a`; J #1193 →
    `6b97c601`; K #1210 → `39f19145`; L #1212 → `2140f5a7`. T063's checkpoint
    PR records batch L's landing here, and does not tick T007: Brett Heap's
    `5962785556`, item 2 (*"Trust per machine (Recommended)"*), rules a
    batch M, which T007 records, and a new phase-3 task, T100. This plan
    lists neither yet.
  - #1144's `tasks.md` was also edited outside the batches. #1202 → `e81eed62`
    (T018's PR) added F11.1's `ADMITTED_ARC_EDITS` (RULED `5890601202`) and
    corrected batch E's held-case count from "6 to 7" to "5 to 6". #1204 →
    `9d2e5bc3` (T049's PR) made two one-sentence record corrections in batch E.
- [x] T008 **Raise the `doc_health` direction arc (R1Q6 (d)).** R1Q6 (d)
  makes the direction question its own arc: openXdox-code's modules import
  openxFactory's `doc_health`, and openxFactory packages nothing (research
  R10). The arc must be decided before 12.5 (release 2) needs the 16 governed
  suites to run. R1Q23 is answered (a), so phase 2 does not wait for it. The
  holder files it as a staging topic or a proposal, which cites `5817152735`
  and names that deadline.
  - Under R1Q24 (a), the arc also takes the two other classes in the declared
    exclusion: the files that reach openxFactory's status-exemption rail, and
    those that reach its contracts (T043). Its record cites `5850003126` for
    them.
  - T061's PR body, in phase 2, lists the excluded files that validate a kind
    the narrowed validator gives up. The holder then adds that list to the
    arc's record, as bookkeeping, so the arc knows which validator each file
    will need once it runs.
  - **Ruled**: R1Q6 (d), `5817152735`; R1Q24 (a), `5850003126`.
  - **Raised**: openxFactory#1173 → `0d48231b`. The arc's record is the staged
    topic
    `ideation/staging/doc-health-direction-arc/doc-health-direction-arc.md`,
    with its row in `ideation/staging/INDEX.md`. It cites `5817152735` and names
    the deadline.
  - **Record completed**: openxFactory#1214, a bookkeeping PR with no `Arc:`
    trailer. It edits the staged topic, its row and detail section in
    `ideation/staging/INDEX.md`, and this file. The record had been captured
    before round 2's answers, and now:
    - takes the rail class (3 files) and the contracts class (5 files) of the
      declared exclusion, each file listed as openXdox-code's
      `tests/declared_exclusion.yaml` holds it at `6a3b93b9` (the same lists as
      at T043's landing, openXdox-code#32 → `4610bca5`), and cites `5850003126`
      for them (R1Q24 (a));
    - reads R1Q23 as answered (a), and R1Q25's consumer-schemas class as
      cleared by T061 (openXdox-code#36 → `6a3b93b9`), so neither is open in it
      any more (its claim 6 and Q5);
    - carries T061's list of the seven excluded files that validate a kind the
      narrowed validator gives up (openXdox-code#36's body, § "For T008");
    - names F9.2, and what the arc's landing removes (the bullet below).
  - **What the tick means.** T008's box is the raise and the record. The arc
    itself is not done: the topic's Q1 to Q4 and Q6 stay open (Q5 is answered
    by R1Q23 (a)), so it still needs Brett Heap's ruling among its options,
    and an owner or a task list for the realization (Q6). "After T008" and
    "until T008", elsewhere in this file, mean that arc's LANDING, so F9.2's
    box stays open until then.
  - **F9.2's re-run belongs to this arc.** Where this file says F9.2 closes
    "after T008" or stays red "until T008", it means that arc's landing. The
    landing removes, together, the help-tree test's `--deselect` in
    openXdox-code's required check (openXdox-code#31, folded into the
    whole-suite step by #32), the guard test beside it, and the same
    `--deselect` in F9.1's pytest line (T007 batch J) (RULED `5859927858`,
    `5870594693`). F9.2 is then re-run, and its box closes. The staged topic
    now names F9.2 and these three removals (openxFactory#1214).
    - `5870594693` itself says *"T008 removes it together with the workflow
      deselect"*, which names F9.1's `--deselect` and the workflow's. The
      guard test beside the workflow's is openXdox-code#32's own
      (`tests/integration/test_assembled_surface.py::test_the_help_tree_is_left_out_only_while_its_stated_reason_holds`),
      and its docstring says the pull request that clears the reason takes the
      exclusion and the guard out together.
- [x] T009 **Phase 2's round.** DONE in this revision, on `5850003126`. No
  task of phase 2 starts before it is done.
  - The answers to R1Q10, R1Q11, R1Q12, R1Q13 and R1Q23 are encoded in
    `spec.md` § Clarifications and `clarify-questions.md`.
  - The #1144 lines they amend are T007's batch G (§ "Ruled amendments"). None
    changes a requirement or a scenario, so no RULING NEEDED is raised.
  - Phase 2 is re-planned below, in `plan.md`, and in § "Phase 2 writer
    slices", and its PROVISIONAL marker is lifted.
  - `/speckit-analyze` ran with T006's feature context over the whole
    revision, T019's and T069's parts included, and found nothing CRITICAL.
    Every finding is recorded with its disposition in
    `evidence/analyze-round-2.md`, which is linked from this feature's README
    entry. That one record serves T009, T019 and T069. It also raised R1Q26
    and R1Q27, which T067 encodes.
  - **Ruled**: R1Q10 (a), R1Q11 (a), R1Q12 (a), R1Q13 (a) with (c), R1Q23 (a),
    `5850003126`.
  - **After**: T004.
- [x] T019 **Phase 1's openXdox-code round.** DONE in this revision, on
  `5850003126`. T005's re-measure had put two tasks of phase 1's openXdox-code
  tail on open questions: T061 (7.3), which its contingency brought into phase
  1, and T043, which met the two classes R1Q24 asks about. T006's analyze
  added R1Q25, on 7.3's phase.
  - The answers to R1Q14, R1Q24 and R1Q25 are encoded in `spec.md`
    § Clarifications and `clarify-questions.md`.
  - The #1144 lines they amend are T007's batch F. F5.2 admits T061's two edits
    to protected suites (R1Q14 (a)). F9.1 and 9.2 admit three more exclusion
    reasons (R1Q24 (a), R1Q25 (b)), and 9.2's phase-3 close is recorded beside
    the release map (R1Q25 (b)). F7.1 is unchanged, because under R1Q24 (a)
    its second test still runs by node id. None of them changes a requirement
    or a scenario.
  - Re-planned:
    - T061 returns to phase 2, with an `After:` line of its own, and F7.1 goes
      back to T063 (R1Q25 (b)). P1-M leaves phase 1's slices.
    - T041's exclusion takes four reasons. T043 declares in it the two classes
      R1Q24 (a) names and `tests/test_snapshot.py`, each with its own reason.
    - T008, T040, T047, T049, T063, T064 and P1-J follow.
    - T027, T046 and T085 are unchanged, because R1Q24 (a) needs no default in
      phase 1.
  - How openxFactory's readers of openXdox's validator keep working, and what
    the ten-to-three narrowing means for each caller, are in T061 and T066, as
    T067 re-planned them on R1Q27 (a).
    T061 now lands in phase 2, so the pin at which they must keep working is
    T064's, not T047's.
  - The reviewed allow-list (R1Q7 (a)) has its owner. The first task that
    makes an admitted edit to a protected suite creates the file in its own
    PR: T043, if its triage respells one, and otherwise T061, with R1Q14 (a)'s
    two edits. An entry names its landing by that PR's number, since the
    landing's commit is not known inside it. T067: under R1Q26 (a), T060's
    edit lands before T061's, so T060 creates the file if T043 has not.
  - `/speckit-analyze` ran over the whole revision, this tail included, and
    found nothing CRITICAL (`evidence/analyze-round-2.md`, T009).
  - **Ruled**: R1Q14 (a), R1Q24 (a), R1Q25 (b), `5850003126`.
  - **After**: T006.
- [x] T067 **Round 3: R1Q26 and R1Q27.** Round 2's analyze raised both
  (`evidence/analyze-round-2.md`, V2-1 and V2-2), and Brett Heap answered both
  (a) on `#656`, comment `5851950767`. This task, in a bookkeeping PR of its
  own:
  - encoded the answers in `spec.md` § Clarifications and
    `clarify-questions.md`, and handed T007's batch I the three #1144 lines
    they amend (§ "Ruled amendments");
  - re-planned T059, T060, T061, T063, T064 and T066 on them. T066's re-plan
    says how each kind reaches a validator (V2-12): under R1Q27 (a) the
    consumer's validator keeps validating every kind the tree it runs from
    supplies, so openxFactory's callers are not moved;
  - re-ran `/speckit-analyze` over the result, and recorded it in
    `evidence/analyze-round-3.md`, linked from this feature's README entry.
  - **Ruled**: R1Q26 (a), R1Q27 (a), `5851950767`.
  - **After**: T009.

---

## Phase 1: it runs (US1 and US4)

**Goal**: openDox-code imports, builds its parser on its own default profile,
registers its own default adapter, and runs its whole suite green. openXdox-code
runs its whole suite green less its declared exclusion, which is reported with
its count and each entry's reason as an open extraction. It lists the files
that need `doc_health` (R1Q6 (d)), the files that reach openxFactory's
status-exemption rail or its contracts (R1Q24 (a)), and `tests/test_snapshot.py`
until 7.3 lands in phase 2 (R1Q25 (b)). The `opendox` console script exists.
openxFactory is unchanged in behaviour.

**Independent test**: T049.

**Until T011 lands, `opendox.serve` and `opendox.cli` do not import** in a
lone openDox-code checkout: both raise `ModuleNotFoundError: No module named
'ideation_dashboard'` (measured at `1e4a57fb` for T006). Any run with the root
conftest in play fails with them, because the autouse `declared_human_console`
fixture imports `opendox.cli` (`tests/session_fixtures.py:397`).
- So a test from a task that can land before T011 (T010, T015, T020, T025,
  T026 and T027) imports neither module.
- Its PR quotes its run under `--noconftest`, as `validate.yml`'s file list
  runs today.
- A module the test must check but cannot import, it may read with `ast`, as
  `tests/test_profile_registration.py` reads `serve.py` and `cli.py`.
- No slice edits openDox-code's `validate.yml` before T036, which removes its
  file lists. A new test first runs in the required check there.

### Lane A: the route seam (`src/opendox/serve.py`, `src/route_extension.py`; single writer)

- [x] T010 [US1] [oDc] **Declare the handler-contribution facet (R1Q1 (a)).**
  A profile or an extension declares the mixin classes that hold the methods
  its bindings name. `build_server` composes them into
  `BoundDashboardHandler`'s bases. `resolve_handlers` is unchanged, so every
  binding is still checked against the class that will dispatch it, and no
  core module names a contributor. Tests:
  - a binding naming a method that only a contributed mixin has resolves;
  - a binding naming a method no class has is refused at wiring time.

  `opendox.serve` does not import until T011 lands (above). So the test drives
  the facet where plan.md places it, in `src/route_extension.py`, over a
  stand-in base class. T011's PR adds a case through `build_server`, with a
  stand-in profile registered and a snapshot source injected (plan.md's
  "Phase-1 limit" note).
  - **Realizes**: 2.2 (the mechanism).
  - **Falsifier**: a new `tests/test_route_handler_contribution.py`.
  - **Ruled**: R1Q1 (a), R1Q22 (a), `5817152735`. The edits to carved files
    need no declared-edit act.
  - **After**: T006.
  - **Landed**: openDox-code#40 → `0f10b1f5`.
- [x] T011 [US1] [oDc] **Remove the two import-time reaches.**
  - Delete `serve.py:199` and the `:206` re-export block (2.1).
  - Take `serve_openxfactory_lanes.LaneRoutes` off `DashboardHandler`'s bases.
  - Move every openDox-side reader of the five names to the lanes column's own
    spelling, or to a neutral one (2.2).
  - Do NOT vendor the module (2.1a).
  - Land T030 in the same PR.
  - Add T010's `build_server` case, now that `opendox.serve` imports.
  - Move `opendox.cli` and `opendox.serve` from `tests/test_consumer_reach.py`'s
    `STILL_REACHING` into its `NEUTRAL_MODULES`, in this PR. The required
    `validate` job runs that file by name (`validate.yml:394`), and its
    `test_the_reaching_modules_are_recorded_as_reaching` fails the moment the
    two modules import, asking for exactly this move *"in the same act"*
    (T006). T034 re-derives the rest of the file.
  - **Realizes**: 2.1, 2.1a, 2.2 (openDox half).
  - **Falsifier**: F2.1's generated sweep; `tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling`;
    `tests/test_route_handler_contribution.py` with its `build_server` case;
    `tests/test_consumer_reach.py`, which the required check runs.
  - **Ruled**: R1Q1 (a), R1Q22 (a).
  - **After**: T010.
  - **Landed**: openDox-code#46 → `0e88454a`, with T030 in the same PR.
- [x] T012 [US1] [oDc] **`serve.py:713`** (`doc_health.corpus.RealGit` in
  `_head_of`). Replace it with openDox's own HEAD reader. It must keep
  degrading to `None`.
  - **Realizes**: 4.3 (1 of the 8 reaches into openxFactory).
  - **Falsifier**: F4.1's scan no longer lists `serve.py:713`.
  - **Ruled**: R1Q22 (a).
  - **After**: T011.
  - **Landed**: openDox-code#47 → `27683028`.

### Lane B: the default profile

- [x] T015 [P] [US1] [oDc] **Ship openDox's default profile for its own domain**
  (documents and ideas).
  - It carries none of openxFactory's `Status:` taxonomy, change/spec/delta
    nouns or act verbs, and its display words are `NEUTRAL_DISPLAY`'s,
    unchanged. It declares no `DISPLAY` facet, so the absent facet renders
    them (holder reading, `#656` `5851560764`).
  - It contributes openDox's OWN verbs and routes (R1Q4 (a)). For now that
    means the runtime verbs: `RuntimeSubcommand` is in its
    `SUBCOMMAND_EXTENSIONS` from this first landing (R1Q5 (a)), so no build
    ever meets an empty default (design.md § D5). `opendox.runtime.cli`
    imports with the `test` extra alone (checked for T006). T038 gives the
    verbs the `opendox` console script. Release 2 adds `submit`, `land` and
    `health`.
  - A test holds the vocabulary out (requirement 3, second scenario).
  - **Realizes**: 3.1.
  - **Falsifier**: the new vocabulary test, and a test that
    `RuntimeSubcommand` is in the default's `SUBCOMMAND_EXTENSIONS`. F3.1
    needs T016's registration, so T016 quotes it. That the default imports
    with no extra installed is shown by T038's plain-install runs.
  - **Ruled**: R1Q4 (a), R1Q5 (a).
  - **After**: T006.
  - **Landed**: openDox-code#38 → `a435aecf`.
  - As landed, the default declares no `DISPLAY` facet, because assigning
    `NEUTRAL_DISPLAY` literally would pin light-theme colours on `:root` and
    override dark mode. `ProjectSubcommand` stays out of the default. Both are
    holder readings within existing rulings, recorded on `#656`,
    `5851560764`.
- [x] T016 [US1] [oDc] **Registration semantics (R1Q3 (a)).**
  - `build_parser()`, `build_server()` and `main()` REGISTER the default where
    nothing is registered, so `is_registered()` then answers True. The default
    is an entry-point registration and never a fallback inside `current()`.
  - A bare process that builds nothing still meets `ProfileNotRegistered`,
    which is the library caller's case. `profile_proxy`'s nothing-registered
    refusal is kept, and never weakened into `()`. That is the case the file
    was written for (R1Q3 (i)).
  - A host registration made before anything is built replaces the default.
    After a parser or server was built from the default, a host registration
    meets today's `AlreadyRegistered` refusal (R1Q3 (ii)), which T016 leaves
    in place.
  - `tests/test_profile_registration.py` asserts the bare-process refusal, the
    replacement before a build, and the refusal after one.
  - The one-line entry-point calls in `serve.py` and `cli.py` rebase onto Lane
    A.
  - **Realizes**: 3.2.
  - **Falsifier**: F3.1 with line 2 as amended (T007 batch A); `tests/test_profile_registration.py`.
  - **Ruled**: R1Q3 (a), with (i) and (ii); R1Q22 (a); RN-1 (a),
    `5850003126`. RN-1 (a) aligns requirement 3's fourth scenario with (ii)
    and adds a scenario for the refusal after a build, through T007's batch D.
    The refusal after a build is today's `AlreadyRegistered`, which (a) keeps,
    so T016 lands as planned. Batch D landed as #1170 → `79a720a2`, so
    requirement 3's text now says what T016 does (T049).
  - **After**: T015, T012 (Lane A's last `serve.py` edit).
  - **Landed**: openDox-code#42 → `19370adc`.
- [x] T017 [US4] [oxF] **3.3, read-only.** At every openxFactory arc
  landing, confirm that the carve manifest's `deleted_at_carve` row for
  `scripts/ideation_dashboard/profile_openxfactory.py` is byte-identical. F11.1's
  content check already refuses any row change, so the interim F11.1 runs are
  the evidence: T018, T065 and T098. The first is phase 1's, after T047.
  Phases 2 and 3 repeat the check through T065 and T098, after their own
  consumer pins, and T097 ticks 3.3 on all three.
  - **Realizes**: 3.3.
  - **Falsifier**: F11.1 (interim: T018, T065, T098).
  - **After**: T047, which is phase 1's openxFactory landing.

### Lane C: the home-corpus seam

- [x] T020 [P] [US1] [oDc] **`corpus_adapter.register_home(factory)` and
  `corpus_adapter.home()`.**
  - `factory` has `home_corpus`'s shape: `adapter, ref = factory(root)`.
  - With nothing registered, `home()` raises `CorpusRefused` of the NEW kind
    `ADAPTER_NOT_REGISTERED` (added to `REFUSAL_KINDS`, `:135`). Its `subject`
    is `opendox.corpus_adapter` and its `detail` names `register_home(...)`.
  - With a stand-in factory registered, `home()` returns it.
  - **Realizes**: 4.1 (the seam), 4.2.
  - **Falsifier**: those two cases, as seam tests in a new
    `tests/test_authoring_seam.py`. F4.1's first block and its first named
    test call `required_header_fields()`, which reaches the seam only once
    `authoring.py:318` is routed, so they are T021's.
  - **After**: T006. It never needed an answer.
  - **Landed**: openDox-code#37 → `e295b1a9`.
- [x] T021 [US1] [oDc] **`authoring.py:318`** resolves the home corpus through
  `corpus_adapter.home()`.
  - **Realizes**: 4.1, 4.3 (1 of 8).
  - **Falsifier**: F4.1's first block (nothing registered: exactly one
    outcome); `tests/test_authoring_seam.py::test_required_header_fields_come_from_the_registered_adapter`,
    which this task adds. The named test runs with the root conftest in play,
    so it needs T011.
  - **Ruled**: R1Q22 (a).
  - **After**: T020, T011.
  - **Landed**: openDox-code#44 → `9d13bd16`.
- [x] T022 [US1] [oDc] **4.1a: openDox's own default adapter.** Where no host
  called `register_home`, the entry points register a `home_corpus`-shaped
  factory over `LocalGitCorpus`. Like the default profile, it is an
  entry-point registration (R1Q3 (a)). It starts at `LocalGitCorpus()`'s
  defaults (`required_fields=()`), and phase 2's T054 sets the small neutral
  field set that R1Q13 (a) rules (`title` and `summary`, in the answer's own
  example). A bare process still refuses.
  - **Realizes**: 4.1a.
  - **Falsifier**: `tests/test_authoring_seam.py::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has`.
  - **Ruled**: R1Q3 (a), R1Q22 (a).
  - **After**: T020, T021, T016.
  - **Landed**: openDox-code#45 → `255514df`.
  - The default reads the working tree, uncommitted edits included, and not the
    session branch's HEAD, as the hosted adapter does (RULED `#656`,
    `5851560764`, *"Working tree (Recommended)"*).

### Lane D: the other openxFactory reaches (`workbench.py`, `serve_wire.py`, `doxbench_packet.py`)

- [x] T025 [US1] [oDc] **`workbench.py:746`** (`session_documents`), in
  phase 1 (R1Q9 (a)). It resolves through the registered adapter's
  `list_documents`: openDox's `LocalGitCorpus` standalone, and openxFactory's
  adapter when hosted. With nothing registered it refuses, as 4.2 does. The
  hosted membership rule (the governed roots plus a `Status:` header) is
  proved unchanged by T046.
  - **Which scope it lists matters (measured for T006).** At openxFactory
    `c415c3d1`, the host's adapter lists 794 documents under `all`, and
    exactly the session notebook's 398 under its declared `documents` scope,
    which equals today's `doc_health.corpus.load_docs` set with a `Status:`
    header. `LocalGitCorpus` declares `all` alone. So listing `all` would
    change the hosted set. T025 declares where the scope to list is
    registered, with `all` as openDox's default. T046 registers `documents`.
    openDox's core names no host scope.
  - **Realizes**: 4.3 (1 of 8).
  - **Falsifier**: F4.1's scan; a session-notebook membership test, which
    lists `all` with nothing but the default registered, and the registered
    scope when one is.
  - **Ruled**: R1Q9 (a), R1Q22 (a).
  - **After**: T020, T026 (both edit `workbench.py`).
  - **Landed**: openDox-code#43 → `c46430fb`.
- [x] T026 [US1] [oDc] **`workbench.py:1407-1409`** (`run_scoped_doc_health`).
  Route it through a declared health-check seam that, with nothing registered,
  returns `status = not-available`, naming the seam and its remedy (the
  registration call), which is 4.2's discipline. It stays that way until Group
  6 (release 2) registers openDox's own check.
  - **Realizes**: 4.3 (3 of 8).
  - **Falsifier**: F4.1's scan; a seam test.
  - **Ruled**: R1Q22 (a).
  - **After**: T006.
  - **Landed**: openDox-code#39 → `582ed073`.
- [x] T027 [P] [US1] [oDc] **`serve_wire.py:1369` and `doxbench_packet.py:177`.**
  - The doxBench schema validators and the status-exemption rail become seams.
    Each fails closed, naming itself, when nothing is registered.
  - openxFactory registers its own (T046).
  - The standalone defaults are T085's (phase 3).
  - **Realizes**: 4.3 (2 of 8).
  - **Falsifier**: F4.1's scan; seam tests.
  - **Ruled**: R1Q22 (a).
  - The phase-1 seam fails closed exactly as 4.2 does. The standalone defaults
    are T085's, as R1Q10 (a) rules: openDox's own validators over its spec
    leg's two chat schemas, and no status exemption.
  - **After**: T006.
  - **Landed**: openDox-code#41 → `8017cd52`.

### Lane E: the instrument and the README

- [x] T030 [P] [US1] [oDc] **2.4: the import-every-module test.**
  `tests/test_imports_standalone.py::test_every_module_imports_with_no_sibling`
  walks the package with `pkgutil`. It fails naming the first module that needs
  a sibling, and it first asserts the siblings are absent.
  - **Realizes**: 2.4; 9.2a (the instrument; T036 makes a required check run
    it).
  - **Falsifier**: F2.1's last line.
  - **After**: T006.
  - **Lands with**: T011, in T011's PR, because it fails until 2.1 lands.
  - **Landed**: openDox-code#46 → `0e88454a`, in T011's PR as planned.
- [x] T031 [US1] [oDc] **2.6: `README.md:39-42`.** State the live cause
  (`ideation_dashboard`, not the openDox → openXdox inversion). Once the
  narrowing ends, rewrite the paragraph.
  - **Realizes**: 2.6.
  - **Falsifier**: review.
  - **After**: T035.
  - **Lands with**: T036, in T036's PR.
  - **Landed**: openDox-code#52 → `55194335`, in T036's PR as planned.

### Join: the sweep, the suite, the console script

- [x] T032 [US1] [oDc] **2.3: the sweep.** Grep `src/` for `ideation_dashboard`,
  `corpus_adapter_openxfactory`, `doc_health` and `openxdox` in import
  position. Record, for each hit, whether it is closed or deferred, with its
  reason, in the PR body. The expected state is: no import-time reach, and 19
  deferred reaches, all into `openxdox`.
  - **Realizes**: 2.3.
  - **Falsifier**: F4.1's scan, which lists only `openxdox` targets.
  - **After**: T011, T012, T016, T021, T022, T025–T027 (every lane joins
    here).
  - **Landed**: openDox-code#49 → `68be484a`.
- [x] T034 [US1] [oDc] **Repair the nine files that go red once 2.1 lands**
  (research R3; 86 failures and errors). Update the Node harnesses to the
  views; replace carve-residue paths and module literals; re-derive
  `test_consumer_reach.py`'s `STILL_REACHING` beyond the two modules T011
  moved; re-pin `test_boundary.py`'s census.
  - `test_provider_boundary.py` is repaired for 16.6's three reasons (*"the file
    is repaired in phase 1"*).
  - `test_outline_model.py`'s `doc_health` case is either rewritten against
    openDox's own contract, or becomes a NAMED openxFactory composition test
    (R1Q2 (a)). In the second case, it takes the same route as T035's
    `test_session_harness.py`. This PR removes the case and lists it, with its
    destination, in its body. A T007 batch adds its openxFactory path to
    F11.1's named set. T047's openxFactory PR lands it, and T049 checks that
    it arrived.
  - **Realizes**: 9.1 (part), 16.6 (the phase-1 repair).
  - **Falsifier**: `python -m pytest -q` over the nine files.
  - **Ruled**: R1Q2 (a); R1Q22 (a). Eight of the nine are carved
    `moved_with_declared_edit` rows (research R12). The ninth,
    `test_consumer_reach.py`, was created at the destination and has no row.
    None needs a declared-edit act.
  - **After**: T032, whose sweep fixes the import inventory that the
    re-derived censuses must match.
  - **Landed**: openDox-code#50 → `71b631bc`.
  - It moved four cases to openxFactory: the outline case, and three
    memory-gateway cases. The holder accepted the memory-gateway move under R1Q2
    (a), because the spec those cases read exists only in openxFactory
    (openDox-code#50's body). All four landed under `tests/domain_profile/`,
    which is in `HOST_TESTS`, and not in F11.1's named set (see T047).
- [x] T035 [US1] [oDc] **Empty the root `conftest.py`'s `collect_ignore`**
  (seven modules; research R4).
  - The six that import `openxdox` each leave `collect_ignore` in one of two
    ways:
    - rewritten in place as a neutral openDox test that imports no sibling;
    - or removed from openDox-code in this PR, and re-landed by T042 in
      openXdox-code's `tests/integration/`. A module whose imports reach
      `doc_health` cannot run there in release 1, because F9.2 runs every file
      in `tests/integration/`. It goes into T041's declared exclusion, with its
      reason, instead (R1Q6 (d)).
  - `test_session_harness.py` runs a script only openxFactory has. It is
    either rewritten, or removed here and moved to openxFactory as a NAMED
    composition test (R1Q2 (a)). In the second case, a T007 batch adds its
    path to F11.1's named set first, and it lands in T047's openxFactory PR.
  - This PR's body lists each removed module with its destination:
    openXdox-code's `tests/integration/` (T042), openXdox-code's declared
    exclusion (T041), or openxFactory (T047). Each destination task lands
    exactly its part of that list, and T049 checks that every listed module
    arrived where the list sends it, so none is dropped from both suites
    (requirement 9, second scenario).
  - **Realizes**: 9.1 (part), 9.3 (part).
  - **Falsifier**: `python -m pytest -q tests/`, with the root conftest in
    play and its `collect_ignore` empty. F9.1 whole needs T036's
    `validate.yml` and `testpaths`, so T036 quotes it.
  - **Ruled**: R1Q2 (a), R1Q6 (d), R1Q22 (a). All seven are carved rows.
  - **After**: T034.
  - **Landed**: openDox-code#51 → `80acead1`.
  - One case, `test_worktree_container_is_gitignored_in_the_aggregation_repo`,
    was held out of the move, and landed on its own as openxFactory#1203 →
    `08e97c27` (`EXPECT_SKIPPED` 5 → 6), because T049's arrival check found it
    in no suite. The cases it did move to openxFactory landed under
    `tests/domain_profile/`, not in F11.1's named set (see T047).
- [x] T036 [US1] [oDc] **The required check runs the whole suite.**
  - Remove `validate.yml`'s three `--noconftest` steps and their file lists.
    Also remove the 15 comment lines that name the flag, because F9.1's
    `grep -c` counts comments.
  - Set `testpaths = ["tests", "tests_runtime"]`, and give the required
    `validate` job the PostgreSQL service and the `.[runtime,test]` install
    that the `runtime` job has today (R1Q8 (a)). The separate `runtime` job may
    then be folded in.
  - F9.1 is unchanged, and it installs `.[test]` alone. So the `test` extra
    gains the `runtime` extra's packages. Without them,
    `tests_runtime/conftest.py` fails every runtime case under `CI` and skips
    it elsewhere, and a skipped case does not make a whole suite. Keeping
    `test` lean would instead need F9.1's install line changed, which R1Q8 (a)
    left alone, so that route goes to Brett.
  - F9.1's runs (here, and in T049) export the database's DSN the way the job
    does, and quote the variables they set.
  - T095's clean-machine harness is not a test module, so it stays out of this
    job: it runs in its own job, with no database service.
  - Re-pin the floors to the measured whole-suite counts.
  - T031 lands in the same PR.
  - **Realizes**: 2.5, 9.1, 9.2a (a required check now runs T030).
  - **Falsifier**: F9.1 (openDox-code), both of its assertions.
  - **Ruled**: R1Q8 (a).
  - **After**: T035, T038 (both edit `pyproject.toml`, and T038's
    `[project.scripts]` lands first).
  - **Landed**: openDox-code#52 → `55194335`, with T031.
- [x] T037 [US1] [oDc] **9.4, openDox's half.** Restore the margin over the
  floors. The two skips that mirror openXdox's gap leave this leg, because
  they need both legs. Their both-legs halves assert for real in openXdox-code's
  `tests/integration/` (T042), and the half this leg can prove alone asserts
  here (holder decision, 2026-09-27; openDox-code#55).
  - **Realizes**: 9.4 (part).
  - **Falsifier**: the triple in `validate.yml`.
  - **Ruled**: R1Q22 (a). The two skips sit in
    `tests/test_binding_stylesheets.py`, a created file with no
    carve-manifest row (RULED OQ-C), so R1Q22 (a) is not needed for them
    (openDox-code#55, question 4).
  - **After**: T036.
  - **Landed**: openDox-code#55 → `2d116415`.
  - **As landed, on the holder's decisions of 2026-09-27**:
    - The floors sit three below CI's reading, on the rule of openxFactory's
      `pytest-suite`, *"three below the lower of the two greens"*. So "restore
      the margin" reads that way in this leg. The holder accepted it, and it
      reverses the choice that openDox-code#31 recorded in `validate.yml`: *"a
      floor with slack in it is a floor that stops catching the regression it
      was set to catch"* (openDox-code#55, question 1). openXdox-code's floors
      stay on CI's reading (T044).
    - The two skips that mirrored openXdox's gap left this leg, as the task
      sentence above now says. Their both-legs halves went to the composition,
      and T042 took them (see T042). The half this leg can prove alone stays,
      and asserts on every run. The gap until T042 landed was accepted. Both
      cases are in openXdox-code's `tests/integration/test_assembled_bundle.py`
      at `6158151e`.
- [x] T038 [US1] [oDc] **10.1: `[project.scripts] opendox = "opendox.cli:main"`**,
  with Q-R4's runtime verbs reached through the default profile's
  `SUBCOMMAND_EXTENSIONS`, where T015 put `RuntimeSubcommand` (R1Q5 (a)).
  - `opendox runtime …` works standalone, and `opendox-runtime` stays as an
    alias.
  - A host that registers its own profile keeps its 31-entry `--help` tree, so
    neither golden is regenerated.
  - The same landing corrects two comments in `src/opendox/runtime/cli.py`.
    The `:17-19` claim, that a line added to `cli.py` needs a declared edit
    first, is retired by R1Q22 (a). The `:39-42` record of Q-R4 now says
    where the verbs were wired.
  - **Realizes**: 10.1.
  - **Falsifier**: `opendox --help` exits 0 (F10.1's first assertion, which is
    phase 1's proof); `opendox runtime --help` exits 0. Both run after a plain
    `pip install .` into a fresh venv, so no extra is present, and so they also
    show that the default profile imports with no extra. They keep that plain
    install even after batch H makes F10.1 install `.[local]` (R1Q16 (iii)).
    `opendox.runtime.cli` imports under a plain install (measured for T006:
    PyYAML is its only dependency there).
  - **Ruled**: R1Q4 (a), R1Q5 (a), R1Q22 (a).
  - **After**: T016, T022 (`cli.py`'s single-writer order).
  - **Landed**: openDox-code#48 → `796838e8`.

### The openDox root pin (9.5, steps 1–2)

- [x] T039 [US4] [oD] **Phase 1's openDox root pin** (T090 steps 1–2). ONE
  commit in opensoft/openDox moves the `code` gitlink, `contracts/code-pin.yaml`
  and every workflow `@<sha>` to the openDox-code commit carrying phase 1.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openDox root.
  - **After**: T022, T032, T037, T038 (every phase-1 openDox-code landing).
  - **Landed**: openDox#13 → `663ac683`.

### openXdox-code: green alone, less the declared exclusion

- [x] T040 [US1] [oXc] **Move the pin; clear the residue.**
  - Move `pyproject.toml`'s `opendox @` to the phase-1 openDox-code commit
    (plan.md § Pins, step 3). The ratchet is unchanged, since phase 1 closes no
    openXdox reach.
  - Give `test_create_project.py`, `test_edit_project.py` and
    `test_register_edit_lane.py` a helper of their own, in place of the
    openxFactory-only `test_gate_routes` module (research R10).
  - Do the same for the importers of two more openxFactory-only helpers
    (T005, classes C and D). `test_doxbench_routes` is imported by
    `test_doxbench_knowledge_service.py`, `test_doxbench_thread_wiring.py` and
    `test_doxbench_blank_reason.py`. `test_doxbench_model` is imported by
    `test_doxbench_bridge.py`. Each helper carries only the names its importers
    use, because openxFactory's own copies import further openxFactory helpers.
  - Declare `rfc3339-validator` in the `test` extra.
  - Add two fixtures (T005, classes F and E):
    - `tests/fixtures/base-repo` (research R11), which `test_register.py` reads
      as well;
    - `tests/fixtures/fake_omp_child.py`, the bridge suite's stand-in child,
      which only openDox-code has.
  - Respell the pre-carve source paths, `scripts/ideation_dashboard/<module>.py`,
    in `test_doxbench_packet.py`, `test_scope_column_split.py`,
    `test_doxbench_blank_reason.py` and `test_doxbench_bridge.py` (T005, class
    G). Those modules now live in the installed `opendox` package.
    `test_scope_column_split.py`'s import parser must also recognise an
    `opendox.` import.
  - No protected suite is edited. The four contract-family files, whose `ROOT`
    is `parents[2]`, are left as they are, because T043 declares them in the
    exclusion (R1Q24 (a); T005, class I).
  - **Realizes**: 9.2 (part), 9.5 (step 3).
  - **Falsifier**: collection no longer fails on `test_gate_routes`,
    `test_doxbench_routes` or `test_doxbench_model`. No test reads a source
    path under `scripts/ideation_dashboard/`. `test_register.py` and
    `test_snapshot_validation_launch.py` find their fixture, and the bridge
    suite finds its child.
  - **Ruled**: R1Q22 (a). The edited test files are carved rows.
  - **After**: T039.
  - **Landed**: openXdox-code#29 → `d84b5048`, which also moved the `opendox @`
    pin to openDox-code `2d116415`.
- [x] T041 [US1] [oXc] **The declared exclusion (R1Q6 (d), R1Q24 (a), R1Q25
  (b)).** Requirement 9's first scenario applies.
  - A committed exclusion file lists each test file that cannot run in a lone
    checkout, each entry with its reason, and the total count. T041 names the
    file, and T007 batch B records that name in F9.1.
  - The file admits four reasons, and each is reported as an open extraction:
    - `doc_health` reachability, pending the direction arc (T008), from R1Q6
      (d);
    - openxFactory's status-exemption rail, and openxFactory's contracts, both
      pending T008, from R1Q24 (a);
    - the consumer's schemas until 7.3 lands, for `tests/test_snapshot.py`
      alone, from R1Q25 (b). T061 clears that entry in phase 2.

    T007's batch F admits the last three in F9.1 and 9.2.
  - T041 writes the entries for all four reasons, on the holder's decision at
    its landing, because a file with two reasons cannot be split between two
    tasks. T043's triage is then a re-run at T040's pin. T005 measured the
    `doc_health` set at openXdox-code `e28930bf`, with Group 2 simulated: 50
    files fail at collection on it, and `test_doxbench_packet.py` has 3
    `doc_health` cases as well, among failures of other classes
    (`evidence/remeasure-2026-09-25.md`, class A). The file is written from the
    run at T040's pin, not from that list.
  - The root `conftest.py` derives its `collect_ignore` from that file. So
    once T043 removes `validate.yml`'s file list and its `--noconftest` lines,
    the whole suite collects less the exclusion, with no list to keep.
  - A run that loads the root conftest PRINTS the exclusion as an open
    extraction, with its count and each entry's reason. From T043 on, the
    required check is such a run.
  - A test asserts that each listed file fails, alone, for exactly its entry's
    reason. The list therefore cannot hide any other failure, and a file that
    stops failing for its reason leaves the list, in the PR that clears it
    (T061's, for `tests/test_snapshot.py`). An entry may name two reasons, as
    `test_doxbench_packet.py`'s does once T040 has cleared its residue
    (`doc_health` and the rail), and the test then checks both.
  - **Realizes**: 9.2 (part).
  - **Falsifier**: the test above, and batch B's three assertions on the
    exclusion (T007): its count equals its entries, every entry carries its
    reason, and the run prints it. Batch F admits the three further reasons.
    F9.1 whole, with its two `validate.yml` assertions, needs T043's edit to
    `validate.yml`, so T043 quotes it.
  - **Ruled**: R1Q6 (d), `5817152735`; R1Q24 (a), R1Q25 (b), `5850003126`.
  - **After**: T040.
  - **Landed**: openXdox-code#30 → `5fbd188e`: 66 files under all four reasons,
    68 reasons in all.
  - **As landed, on the holder's decisions at T041's landing**:
    - T041 wrote the entries for all four reasons, not only the `doc_health`
      ones, because a file with two reasons cannot be split between two tasks
      (openXdox-code#30). The plan's earlier split, T041 writing the
      `doc_health` entries and T043 the other three reasons', was not
      followed. T043's triage became a re-run at T040's pin, and the pin
      moved no entry.
    - The layer-2 hermeticity commits stay in T041, and T043 re-runs them at the
      pin.
    - The protected `tests/test_snapshot_validation_launch.py` joins the
      exclusion under `doc_health`, and is not edited (R1Q6 (d)). T016's default
      registration does clear the `ProfileNotRegistered` that T043's text
      expected it to clear, and the suite then fails 9 cases on `doc_health`
      (openXdox-code#30).
- [x] T042 [US1] [oXc] **9.3: `tests/integration/`.**
  - Add the 31-entry assembled `--help` tree:
    `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records`.
  - Add those of T035's relocated modules that run without `doc_health`,
    exactly as T035's PR body lists them. The others are in T041's declared
    exclusion (R1Q6 (d)).
  - Each test names the pin it composes at.
  - The tree stays at 31 entries because a host that registers its own
    profile does not get the default's runtime verbs (R1Q5 (a)).
  - **Realizes**: 9.3.
  - **Falsifier**: F9.2, quoted red on the 31-entry help-tree test, and
    closing after T008, as T049's does. RULED `5859927858` leaves F9.2
    unchanged and takes that test out of the required check until the arc
    that T008 raised lands, and `5870594693` deselects it in F9.1. F9.2
    fails on nothing else (openXdox-code#31).
  - **Ruled**: R1Q5 (a), R1Q6 (d).
  - **After**: T040, T041 (whose exclusion decides which relocated modules
    belong here).
  - **Landed**: openXdox-code#31 → `4e16db95`.
  - It also took T037's two relocated cases, on the holder's decision of
    2026-09-27: the two-leg re-derivation,
    `test_the_gate_exclusive_set_is_re_derived_where_the_modules_are_present`,
    and the partial-assembly rule,
    `test_a_partial_assembly_is_a_failure_and_not_a_skip`, with the scan of an
    assembled bundle's stylesheets. They keep their names. T035 sent nothing
    here (openXdox-code#31).
- [x] T043 [US1] [oXc] **9.2: the required check runs the whole suite, less
  the declared exclusion.** Remove the file list and all 8 `--noconftest`
  lines. Re-pin `MIN_SELECTED`/`MIN_PASSED` (564/558 when this was written,
  574/568 once T042 landed) and
  `EXPECT_SKIPPED` to the triple measured over the whole suite less T041's
  exclusion.
  - **First, the whole suite at T040's pin.** T043 runs openXdox-code's whole
    suite there, as T005 did at `e28930bf`, and its PR body names each red
    file with its class:
    - `doc_health` goes into T041's exclusion;
    - carve residue that the new pin exposes is cleared in this PR, as T040
      cleared the rest. T005's experiment found layers behind what T040
      names, and only the pin shows them. For example, once its fixture is
      present, `test_snapshot_validation_launch.py` fails on
      `ProfileNotRegistered`. That depends on T016's default registration at
      the pin, and it is not an edit this protected suite may take. The suite
      builds its parser through `build_parser()` (`:98`), which T016 makes
      register the default, so T016 should clear it. That was read for T006,
      and is not yet run at the pin;
    - a protected suite is respelled only under R1Q7 (a)'s allow-list;
    - the files that reach openxFactory's status-exemption rail or its
      contracts (T005's classes H and I) go into T041's exclusion, each with
      its reason (R1Q24 (a)). At `e28930bf` the rail's were
      `test_doxbench_packet.py`, `test_doxbench_turns.py` and
      `test_doxbench_abstract_envelope.py`. The contracts' were
      `test_validate_ideation_dashboard_contracts.py`,
      `test_wheel_action_contracts.py`, `test_project_schema_election.py` and
      `test_project_action_contracts.py`, and `test_doxbench_blank_reason.py`
      joins them if the triage finds it there (T005's experiment);
    - a protected suite that stays red for a cause none of these takes stops
      this task, and the holder raises that cause with Brett as a question.
  - `test_branch_session.py` fails on `doc_health` (research R11), so in
    release 1 it sits in the exclusion. Its stale `getsource` assertion is
    respelled when it becomes runnable.
  - Any respelling edit that release 1 makes to a protected suite is entered
    in R1Q7 (a)'s reviewed allow-list (T007 batch C).
  - `tests/test_snapshot.py` needs no `doc_health`, so this check runs it, and
    as one of 5.4a's protected suites it cannot be edited to pass. At
    `626f2c8d` three of its cases failed on the validator lookup and the
    schema path (research R11). C3's PR 2 (openXdox-code#28, landed as
    `e28930bf`) moved that lookup into the product's own tree. T005 found that
    one case now passes and two still fail: no `contracts/` and no
    `CONTRACTS_DIR` supply the schemas. Under R1Q25 (b), 7.3 lands in phase 2
    (T061), so this task declares `tests/test_snapshot.py` in T041's exclusion,
    with its own reason: the consumer's schemas, until 7.3 lands. T007's batch
    F admits that reason, and T061 clears the entry.
    `tests/test_snapshot_validator_home.py`, which 5.4a's glob now selects as
    well, passes all 12 of its cases at `e28930bf`.
  - **Realizes**: 9.2.
  - **Falsifier**: F9.1 (openXdox-code), as amended by T007's batches B and F,
    and by batch J's one `--deselect`, which T008 removes.
  - **Ruled**: R1Q6 (d), R1Q7 (a), R1Q22 (a), `5817152735`; R1Q24 (a), R1Q25
    (b), `5850003126`.
  - **After**: T019, T041, T042, T007 (batches C and F), and C3's
    openXdox-code PR 2 (openXdox-code#28, landed as `e28930bf`).
  - **Landed**: openXdox-code#32 → `4610bca5`. F9.1, with the one `--deselect`
    that batch J records, exits 0 there. It landed before batch J did, and
    quoted the falsifier as `5870594693` amends it, as T007 allows.
  - The floors were re-pinned to 890/880/10, at CI's reading with no margin
    (openXdox-code#31, #32). T041's layer-2 hermeticity commits were re-run at
    the pin (openXdox-code#32).
- [x] T044 [US1] [oXc] **9.4, openXdox's half.** Restore the margin over the
  floors T043 re-pinned. Each of the six skips defers *"`doc_health`
  reachability"*. Each one either asserts for real, or its file joins T041's
  declared exclusion with that reason (R1Q6 (d)). No skip is left carrying the
  gap. A file that joins the exclusion here lowers the collected counts, so
  T044 first re-pins T043's floors over the new whole suite less the
  exclusion, and then restores the margin.
  - **Realizes**: 9.4 (part).
  - **Falsifier**: the triple.
  - **Ruled**: R1Q6 (d), R1Q22 (a). The six skips sat in three § 4.5 seam
    suites, which are created files with no carve-manifest row.
    `docs/opendox-carve-admissions.yaml` admits them under
    `openxdox_code`, so R1Q22 (a) is not needed for them (openXdox-code#33,
    note 1).
  - **After**: T043.
  - **Landed**: openXdox-code#33 → `6158151e`.
  - **As landed**: the six skips assert for real, in a new file,
    `tests/test_seam_assembly_beside_gate_and_projection.py`, which joins the
    exclusion under `doc_health`, so the declaration holds 67 files. The triple
    is 885/881/4, and the four skips left are the aggregation-register suite's.
  - **How "restore the margin" is read here.** What is restored is that no
    skip carries the gap: the six skips assert for real, so `EXPECT_SKIPPED`
    falls from 10 to 4, and none of the four left waits for `doc_health`. The
    floors sit on CI's reading, so the margin the step prints stays 0. That is
    the form openXdox-code's #25 set, and the holder chose it for this leg
    (2026-09-28). openDox-code's T037 took the three-below form (see T037).
    The task's falsifier is the triple, and it passes (openXdox-code#33).

### openxFactory: the host keeps working (US4)

- [x] T045 [US4] [oxF] **The lanes column, through the handler-contribution
  facet (R1Q1 (a)).** `scripts/profile_openxfactory.py` declares `LaneRoutes`,
  with tests under `tests/domain_profile/`.
  - `tests/ideation-dashboard/test_extension_point_parity.py`'s MRO assertion
    (`:404-425`) is updated. It is the first NAMED composition test that R1Q2
    (a) admits to 11.1's surfaces, and T007 batch A widens F11.1 to name it.
  - `tests/ideation-dashboard/test_serve_column_split.py`'s
    `test_every_moved_handler_still_resolves_on_the_request_handler` resolves
    six `LaneRoutes` methods on `DashboardHandler` (`:97-110`, `:189-195`).
    Once T011 lands they no longer resolve there, so the test is updated to
    resolve them where the facet binds them. It is the second NAMED
    composition test, and T007 batch A names it too.
  - Any other openxFactory test that pins openDox internals and fails at
    T047's pin joins F11.1's named set through T007's batch E before T047
    lands (R1Q2 (a)). So T045 starts by running openxFactory's whole
    `pytest-suite` at T047's new openDox and openXdox pins, before T047's PR
    opens, and names every red test. `tests/ideation-dashboard/test_route_extension.py` and
    `test_intent_plane_boundary.py`'s serve-surface walk (`:572-588`) are the
    likely ones (T006). T047's own `pytest-suite` run confirms the set.
  - This lands in T047's PR.
  - **Realizes**: 2.2 (openxFactory half), 11.1 (surface).
  - **Falsifier**: openxFactory's `pytest-suite`; the five lane routes are
    served.
  - **Ruled**: R1Q1 (a), R1Q2 (a).
  - **After**: T011.
  - **Lands with**: T047, in T047's PR.
  - **Landed**: openxFactory#1181 → `f56c87c6`, in T047's PR as planned.
- [x] T046 [US4] [oxF] **The other host wiring.** The host registers
  `corpus_adapter_openxfactory.home_corpus` via `register_home` (4.1). It
  registers its `doc_health` check with T026's seam, and its doxBench
  validators and status-exemption rail with T027's seams.
  - Its session-notebook membership rule (the governed roots plus a `Status:`
    header) stays exactly as today (R1Q9 (a)). The host gets it by registering
    its adapter's `documents` scope with T025's registration, which lists the
    same 398 documents at `c415c3d1` (T006). The session notebook needs no
    other implementation of its own.
  - Its own start, in `scripts/opendox_host.py`, asserts that its profile is
    the registered one (R1Q4 (a)).
  - Tests go under `tests/domain_profile/`. This lands in T047's PR.
  - **Realizes**: 4.1 (host half), 4.3 (host half).
  - **Falsifier**: `pytest-suite`; the hosted session notebook is unchanged.
  - **Ruled**: R1Q2 (a), R1Q4 (a), R1Q9 (a).
  - **After**: T020–T022 and T025–T027.
  - **Lands with**: T047, in T047's PR.
  - **Landed**: openxFactory#1181 → `f56c87c6`, in T047's PR as planned.
- [x] T047 [US4] [oX] [oxF] **Phase 1's consumer pins and host wiring** (T090
  steps 5–6). The openXdox root moves to T044's commit and to T039's root
  commit. openxFactory then moves both pin pairs in ONE PR, which also carries
  T045 and T046. It also carries, as named composition tests,
  `test_session_harness.py` if T035 moved it here and `test_outline_model.py`'s
  `doc_health` case if T034 did. C3's openXdox pin bump landed as #1157 →
  `1edbb3dd`, so T047 starts from that pin.
  - It carries nothing for openxFactory's readers of openXdox's validator.
    R1Q25 (b) returned T061 to phase 2, so the openXdox pin this PR moves to
    predates 7.3, and those readers keep working unchanged. Their phase-2
    change is T066, which lands before T064.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openXdox root; `verify-opendox-pin.py` and
    `verify-openxdox-pin.py`; `pytest-suite`.
  - **After**: T039, T044, T007 (batches A and E).
  - **Lands with**: T045, T046.
  - **Landed**: openXdox#20 → `57e2b8f2` (the openXdox root: code `6158151e`,
    openDox `663ac683`), then openxFactory#1181 → `f56c87c6` with T045 and T046.
    The pins are openDox `663ac683` (code `2d116415`, T039) and openXdox
    `57e2b8f2`.
  - Both pin pairs moved in ONE commit, which departs from T090 step 6's "one
    commit each", on the holder's decision of 2026-09-28. The runbook's § 4
    comparison printed DIFFERENT, so its § 3 step 8 moves the openDox pair in
    the same commit (openxFactory#1181).
  - The cases that T034 and T035 moved landed under `tests/domain_profile/`,
    which is in `HOST_TESTS`, and not in F11.1's `COMPOSITION_TESTS`.
    `validate-carve-manifest.py` refuses a new file under
    `tests/ideation-dashboard/` (`carve-file-undeclared`), and batch E records
    the change (openxFactory#1183 → `b9742534`). Seven paths that no F11.1
    surface covers are admitted as arc edits. F11.1 names them in
    `ADMITTED_ARC_EDITS` (RULED `5890601202`), which openxFactory#1202 →
    `e81eed62` carried.
- [x] T018 [US4] [oxF] **Phase 1's interim F11.1**, by T093's procedure, with
  `ARC_TIP` at T047's landing. Record the output in
  `evidence/f11.1-phase1.txt`, with no `Arc:` trailer, and link it from
  this feature's README entry (Principle IV).
  - **Falsifier**: F11.1, as widened by T007 batch A, prints `requirement 1
    holds`.
  - **After**: T047.
- [x] T048 **The F4 re-measure (holder).** After phase 1 lands, re-measure
  openxFactory's direct `opendox` imports and bring Brett the direct-arrow
  question (F4, outside both releases; `5799494355`).
  - **After**: T049.
  - **Done**: measured at openxFactory `main` `91e4685f`, after phase 1. There
    are 107 direct `opendox` import statements in 43 files: 13 statements in 9
    non-test modules, and 94 in 34 test files. The baseline at `9f357e95`
    (design.md D13, `5800995035`) was 9 statements in 8 modules and 80 in 30
    files. Phase 1 removed none: the 4 added non-test statements are T046's host
    wiring (#1181) and the refresh lane (#1166).
  - **Ruled**: F4's direct-arrow question, Brett Heap, 2026-09-30: *"Keep direct
    arrow; close F4 (Recommended)"* (`#656`, `5901316180`). openxFactory keeps
    pinning openDox directly (the `openDox` gitlink,
    `contracts/opendox-pin.yaml` and `verify-opendox-pin.py`), and F4 closes as
    answered. T064 and T094 move both pin pairs as planned. #1144's own F4 box
    is not edited here.
- [x] T049 **Phase 1 checkpoint.** Run and quote:
  - F2.1, and F3.1 with line 2 as amended (T007 batch A);
  - F9.1 in each leg (openXdox-code's as amended by batches B and F, with
    batch J's one `--deselect`, openDox-code's with the database DSN
    exported), and F9.2;
  - `opendox --help`;
  - F4.1's scan, which must list only `openxdox` targets;
  - every module or case T034 or T035 removed, found where its PR's list
    sends it: openXdox-code's `tests/integration/` or its declared exclusion,
    or openxFactory, with its path in F11.1's named set;
  - every file T043 classed under R1Q24 (a), and `tests/test_snapshot.py`
    (R1Q25 (b)), found in the declared exclusion with its reason;
  - T018's interim F11.1 output.

  F7.1 is not run here. 7.3 closes in phase 2 (R1Q25 (b)), and T063 runs it.
  Tick nothing; T097 ticks.

  F9.2 is quoted red, as ruled. RULED `5859927858` keeps F9.2 unchanged, so it
  stays red on the 31-entry help-tree test until T008, and phase 1 closes with
  it quoted so: its box closes after T008, not here (holder decision,
  2026-09-29, at T049). The run is recorded in `evidence/checkpoint-phase1.md`.
  Its arrival check first found one of T035's cases in no suite. That case
  landed first (#1203 → `08e97c27`), so the check finds all 19.
  - **Ruled**: RN-1 (a), `5850003126`. Batch D landed as #1170 → `79a720a2`,
    so requirement 3 is reported as realized once T016 matches it.
  - **After**: T047, T017, T018, T007 (batches A, B, D, F and J).

---

## Phase 2: useful alone (US2 and US4)

Planned on answers since T009 (`5850003126`): R1Q10 (a), R1Q11 (a), R1Q12
(a), R1Q13 (a) with (c), and R1Q23 (a). R1Q25 (b) returned T061 (7.3) here
from phase 1. Every phase-2 task comes after T049 and T009. Round 2's
analyze raised R1Q26 and R1Q27, and T067 (`5851950767`) re-planned T059,
T060, T061, T064 and T066 on their answers.

**Goal**: with no consumer installed, openDox generates its own neutral
snapshot from a plain repository, serves it standalone, and validates it
against schemas that are on disk. The snapshot's contract is openDox-spec's own
neutral schema (R1Q11 (a)). openXdox's validator finds its own three schemas
through its installed distribution (7.3). The governed projection is
unchanged.

**Independent test**: T063.

- [x] T053 [P] [US2] [oDs] [oD] **The neutral snapshot contract (R1Q11 (a),
  R1Q12 (a)).** openDox-spec owns a new schema for the snapshot openDox's
  generator writes. Its stage values are the six role keys, and it requires
  only the sections the neutral projection writes (T054). The schema lands in
  openDox-spec. Then the openDox root's spec pin moves, and then the root cuts
  a `dox-v1.x` minor bundle under its four-value rule (9.5, as batch G amends
  it).
  - openDox-spec becomes a sixth repository of the arc. Its landings carry the
    `Arc:` and `Lane:` trailers and land by squash or merge, like every
    realization landing (T091). It allows all three methods and requires only
    `validate`. T003 recorded its ARC_BASE.
  - openXdox-spec does not change. Its `ideation-dashboard-snapshot` stays the
    governed generator's contract (R1Q12 (a)).
  - One schema is planned. If T055's neutral registry needs an index kind of
    its own, that is a finding raised with the holder before this lands,
    because 7.1's count would change again.
  - **Realizes**: 5.1 and 7.1 (their contract).
  - **Falsifier**: the openDox root's `make validate`, and openDox-spec's own
    `validate`.
  - **Ruled**: R1Q11 (a), R1Q12 (a), `5850003126`.
  - **After**: T049, T009, T007 (batch G).
  - **Landed**: openDox-spec#16 → `f7ee3c76` (the schema). At the openDox root,
    openDox#14 → `52005213` moved the spec pin and the manifest from `dox-v1.0`
    to `dox-v1.1`, with the `opendox-snapshot` entry and the CHANGELOG entry
    kept `Status: draft`. The annotated tag `dox-v1.1` (tag object `851a28e9`)
    is on that commit, cut by Brett Heap (RULED `#656`, `5894235642`; evidence
    `5896493558`, with `make validate` and `make pins` exiting 0 at the target).
    openDox#15 → `66758438` then moved the CHANGELOG entry from `Status: draft`
    to `standard`, the tag existing.
- [x] T050 [P] [US2] [oDc] **5.0: `tests/fixtures/plain-documents`.**
  - A handful of `.md` documents, spread across the six stations (R1Q13 (a)
    with (c)). A document names its station with a neutral front-matter key,
    `stage: <role>` in the answer's own example. A document that declares
    nothing is a source, and groups derive from the topics that sources
    share. At least one group forms, so that AT-R1 can open the chat pane from
    a grouping tile.
  - It carries none of the declared vocabulary: the eight `Status:` words and
    the change/spec/delta nouns.
  - A test keeps the fixture free of those words.
  - **Realizes**: 5.0.
  - **Falsifier**: the vocabulary test; used by F5.3, F7.2, F10.1 and F13.1.
  - **Ruled**: R1Q11 (a), R1Q13 (a) with (c), `5850003126`.
  - **After**: T049, T009.
  - **Landed**: openDox-code#53 → `dc3765dd`.
- [x] T051 [US2] [oDc] **7.0: `tests/fixtures/malformed`.** Exactly one
  violation of a rule of the neutral snapshot schema (T053, R1Q12 (a)), and an
  `EXPECTED_RULE` file holding that rule's identifier.
  - **Realizes**: 7.0.
  - **Falsifier**: used by F7.2.
  - **Ruled**: R1Q12 (a), `5850003126`.
  - **After**: T050, T053.
  - **Landed**: openDox-code#56 → `86647320`. The one violation is the schema's
    rule `title-and-summary-are-text`, an empty title, and `EXPECTED_RULE` holds
    that identifier.
- [x] T052 [US2] [oDc] **5.4: declare the generator seam.** Declare the
  operation handed over, the registration point beside
  `domain_profile.register()`, and the conformance a contributed generator
  must meet.
  - The conformance clause names T053's neutral snapshot kind for openDox's
    own generator. A contributor declares the contract it writes, as
    openXdox's governed generator writes `ideation-dashboard-snapshot`.
  - The entry points register openDox's own generator where no host has (R1Q10
    (a), in R1Q3 (a)'s pattern).
  - `CorpusAdapter` stays closed at six members.
  - **Realizes**: 5.4.
  - **Falsifier**: seam tests; F5.2 through T059 and T061.
  - **Ruled**: R1Q10 (a), R1Q11 (a), `5850003126`.
  - **After**: T049, T009, T053.
  - **Landed**: openDox-code#54 → `fa8862cc`. F5.2 is quoted in T059's and
    T061's PRs, as the falsifier line says, not in this one.
- [x] T054 [US2] [oDc] **5.1–5.3: openDox's small neutral projection** over
  `CorpusAdapter`. It is new code, not a copy of openXdox's.
  - It is bound to `LocalGitCorpus` (5.2) and renders the six words only
    (5.3).
  - It writes T053's neutral snapshot. A document lands in the station its
    neutral `stage:` key names, a document that declares nothing is a source,
    and groups derive from the topics sources share (R1Q13 (a) with (c)).
  - It copies a document's declared `title` and `summary` verbatim. It never
    coerces an empty declared value to `null`, and never excludes the
    document because of it, so T051's one violation, the schema rule
    `title-and-summary-are-text`, is a defect the projection carries through
    (holder decision, 2026-09-27; openDox-code#56).
  - The topic rule must work on documents with no front matter at all. AT-R1's
    repository (b) has none, and it must still yield a grouping tile
    (quickstart.md § 2). The PR names the rule, and a test runs it over a copy
    of that repository, which must yield at least one group.
  - A `stage:` value that is not one of the six role keys is not a
    declaration. The generate verb reports it, naming the document, the value
    and the six keys, and reads the document as a source. The neutral schema
    admits only the six (T053), and a closed set rejects a value it does not
    know (Principle VII), so no other value reaches the snapshot.
  - `display_profile.py` changes in one place, as batch G amends 5.3:
    `SNAPSHOT_VALUES`' defaults become the neutral snapshot's values, so the
    product's own views match its own snapshot (R1Q11 (a)). The governed
    values move to openXdox's facet in T060. No word is re-authored.
  - It sets the small neutral field set on openDox's default adapter (T022),
    so `required_header_fields()` answers it (R1Q13 (a)). A document without
    those fields is still read, as a source.
  - **Realizes**: 5.1, 5.2, 5.3.
  - **Falsifier**: an in-process test that the projection over T050's
    fixture, with neither sibling importable, validates against T053's schema
    and carries none of F5.3's declared words; the topic-rule test over a copy
    of repository (b); and a test that a `stage:` value outside the six is
    reported and read as a source. F5.3 itself runs `python -m opendox.cli
    generate`, whose generate verb reaches the consumer's generator until T055
    routes it (`cli.py:90`), so T056 and T063 quote it, and T056 tests the
    verb's own report of a `stage:` value outside the six.
  - **Ruled**: R1Q11 (a), R1Q13 (a) with (c), `5850003126`.
  - **After**: T050, T052, T053.
  - **Landed**: openDox-code#57 → `a691e4e4`.
  - It carries these holder decisions, each recorded in its body: `organized`
    maps to `grouping`; an entry the adapter cannot classify is left out unread;
    the wheel's grouping tile counts a group's edges where no tally exists, and
    the schema is not widened; content comes from the working tree (T022's
    ruling, `5851560764`), and `source_revision` is the caller's pin, else the
    corpus HEAD; and, from 2026-09-28, `render_scaffold()` gained `lead_fields`,
    so that a scaffold reads as having its `title` and `summary`.
- [x] T057 [US2] [oDc] **7.1, 7.1a, 7.1b, 7.2: the validator's input set.**
  - Narrow it to openDox's own kinds: its spec leg's four, which are 7.1's
    three and T053's neutral snapshot schema (7.1 as batch G amends it).
  - Ship the four as package data. A test checks each copy's digest against
    the spec-leg commit the openDox root pins (R1Q12 (a)). The same copies
    serve T085's doxBench validators.
  - Record why the old script cannot be reused (7.1a).
  - A test asserts that `gate-intent` and `ideation-possibles-register` are
    NOT in the set (7.1b).
  - The validator is new surface at the code leg (7.2).
  - **Realizes**: 7.1, 7.1a, 7.1b, 7.2.
  - **Falsifier**: the packaged-copy digest test and the 7.1b test. F7.2 runs
    the generate verbs, so T058 and T063 quote it.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q12 (a), `5850003126`.
  - **After**: T049, T009, T053.
  - **Landed**: openDox-code#58 → `8ec08e91`. Its `pyproject.toml` package-data
    key is its own line, on the holder's decision that openDox-code's phase-1
    work on `pyproject.toml` was finished.
- [x] T055 [US2] [oDc] **Serve and generate standalone; route 4.3's
  generator-facing reaches.**
  - Give the snapshot source and registry, the corpus-root predicate, and the
    writer and validator lookup seams an openDox default each. The entry
    points register the defaults where no host has (R1Q10 (a), in R1Q3 (a)'s
    pattern), as batch G's 4.3 addendum reads. Their uses are `serve.py:1647`,
    `:629`, `:1687` and `:1993`, `cli.py:610` and `branch_session.py:1568`,
    `:2105`, `:2151`, `:2228` and `:3573`.
  - The validator lookup's default is openDox's own validator (T057), wired in
    by T058. T055 keeps a stand-in as the default until then, on the holder's
    decision of 2026-09-28: T057's PR (openDox-code#58) is NOT merged into
    T055's (#59), and T055 takes T057's code only through `main`. T057 has
    landed (openDox-code#58 → `8ec08e91`). The stand-in names T057 and never
    answers `validated`, and T058 swaps in `opendox.validator`. Either way
    `workbench.py:442`'s `validate_manifest` stops reaching
    `consumer_reach.find_validator` for the `ideation-workbench` manifest,
    which is the first of T061's callers.
  - Retire the `consumer_reach` names `snapshot_registry` (22 uses),
    `snapshot` (6), `generate_snapshot` (2), `is_rfc3339_datetime` (1),
    `corpus_root_refusal` (1), `scanned_roots` (1) and `find_validator` (1),
    plus the core `/snapshot.json` arm's `LateProjectionRoutes` forwarding.
  - An empty `--project-register` or `--possibles` path is REFUSED, failing
    closed. It is never dropped, and never read as `Path("")` (holder
    decision, 2026-09-28; taken in openDox-code#59 at `d7aa9d8c`).
  - **Realizes**: 5.5, 4.3 (part).
  - **Falsifier**: F4.1's scan, down by these reaches.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q10 (a), `5850003126`.
  - **After**: T054, T057, T022 and T038 (`serve.py`'s and `cli.py`'s
    single-writer order).
  - **Landed**: openDox-code#59 → `fa140875`, then its follow-up
    openDox-code#70 → `75bd8703`.
    - #70 confines `serve_project._resolved_listed_edit_entry` to the one entry
      it resolved, with no second lookup by `(repository, ref)`. It takes the
      finding that Copilot's review of #59 at `0c946f4e` raised after the last
      push that could take it, and it landed before T062 (openDox#16).
    - The validator lookup's stand-in, above, is gone: T058
      (openDox-code#68 → `047bb4fa`) wired `opendox.validator` in.
- [x] T056 [US2] [oDc] **The standalone generate path, end to end.**
  `python -m opendox.cli generate` and `generate-and-open --no-open` run on
  the fixture with neither sibling importable, and the server STARTS (the limit
  measured in research R7 is lifted).
  - **Realizes**: 5.1 (part).
  - **Falsifier**: F5.3; F10.1's `generate-and-open` run through
    `python -m opendox.cli`, with a plain install and no `--local`, which
    arrives in phase 3 (T070); and the verb's half of spec.md's `stage:` edge
    case. `python -m opendox.cli generate`, over a copy of T050's fixture in
    which one document declares a `stage:` value outside the six role keys,
    reports it, naming the document, the value and the six keys, and the
    snapshot it writes reads that document as a source. T054 tests the
    projection's half in process. F10.1 as batch H amends it is T077's.
  - **Ruled**: R1Q22 (a), `5817152735`.
  - **After**: T055.
  - **Landed**: openDox-code#66 → `a23e4224`.
    - The verbs already ran standalone at T055's head, and the server started.
      T056 found one defect: the URL line of `generate-and-open` and of `serve`
      was block-buffered on a pipe, so a wrapper never saw where the server had
      started. It is fixed with `flush=True` on those lines in `cli.py` and
      `serve.py`.
    - `tests/test_standalone_generate_path.py` (new) runs real child processes
      with `openxdox`, `ideation_dashboard`, `doc_health` and
      `corpus_adapter_openxfactory` refused, and each case asserts that no
      refused import was swallowed.
    - F5.3 exits 1 at openDox-code `fa8862cc` and 0 at the PR's head. F10.1's
      plain-install run stays T077's.
    - The squash message cites three shas with a wrong 8th character; the
      record correction is openDox-code#66's comment `5917853351`.
- [x] T058 [US2] [oDc] **The post-render validator in the generate verbs.** It
  validates the neutral snapshot against T053's schema, read from T057's
  packaged copy. `--strict` makes a validator that cannot run fatal, and
  `--no-validate` skips validation.
  - **Realizes**: 7.2 (part).
  - **Falsifier**: F7.2. The good fixture exits 0; the malformed one exits
    non-zero, naming `EXPECTED_RULE`, with no `No such file or directory`.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q11 (a), R1Q12 (a), `5850003126`.
  - **After**: T051, T056, T057.
  - **Landed**: openDox-code#68 → `047bb4fa`.
    - `opendox.validator` takes the stand-in's place as openDox's default
      validator, one adapter per own kind (`opendox-snapshot` and
      `ideation-workbench`), over the packaged copies T057 shipped. A validator
      that cannot run reports `validator-unavailable`, which `--strict` makes
      fatal.
    - F7.2 exits 1 at the branch's base (with the stand-in) and 0 after, and
      the malformed fixture's report names `title-and-summary-are-text`, with
      no `No such file or directory`.
    - T062 pins this commit as phase 2's openDox code leg.
- [x] T060 [US4] [oXc] **5.3a: openXdox's facet carries the governed snapshot
  values, and F5.1 is re-run against the realized openDox.** R1Q11 (a) moves
  `SNAPSHOT_VALUES`' defaults to the neutral snapshot's values (T054). So the
  governed values move into openXdox's `DISPLAY` facet, in its `values` block,
  which `display_profile.py` already lets a host override. Batch I amends
  5.3a to admit that block beside the facet's one stage (R1Q26 (a)). The
  block is inert at the old pin, where the defaults are still the governed
  values, so it lands before T059 moves the pin.
  - **The first protected edit (R1Q26 (a)).** `tests/test_gate_loop_views.py`,
    one of 12.5's governed suites, pins the facet as it is today (analyze
    round 2, V2-1). This landing edits its
    `test_the_display_facet_declares_one_stage_entry_and_nothing_else` to
    admit the `values` block beside the one stage, and no other assertion.
    The edit is entered in the reviewed allow-list with its reason, as batch I
    amends 12.5's falsifier. If no earlier task has created the reviewed
    allow-list, this PR creates it. T059 makes the second edit.
  - **Realizes**: 5.3a, F5.1.
  - **Falsifier**: F5.1, whose assertions read only the facet's stages; a
    test that the facet's `values` block holds the governed snapshot's values,
    so the governed views place every card as they do today; and
    `tests/test_gate_loop_views.py` green, with its one entered edit.
  - **Ruled**: R1Q11 (a), `5850003126`; R1Q26 (a), `5851950767`.
  - **After**: T054, T067, T007 (batch I).
  - **Landed**: openXdox-code#34 → `c41063d6`. It created the reviewed
    allow-list, `tests/protected_suite_respellings.yaml`, and entered this
    task's one edit to `tests/test_gate_loop_views.py` (suite blob `7321b04d` →
    `a56906c6`).
  - For T064: the allow-list needs a `created:` admission under `openxdox_code`
    in `docs/opendox-carve-admissions.yaml`, with `since:` set to this landing
    commit (openXdox-code#34).
- [x] T062 [US4] [oD] **Phase 2's openDox root pin** (T090 steps 1–2). T053's
  spec pin and bundle come first in this root, so this commit follows them.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openDox root.
  - **After**: T054–T058 (every phase-2 openDox-code landing), T039 (the root
    pin's single-writer order).
  - **Landed**: openDox#16 → `d5098297`.
    - One commit moves the root's code gitlink, and `contracts/code-pin.yaml`'s
      `commit:` and `digests.tree_sha256`, from `2d116415` to `047bb4fa`
      (`047bb4fa394f3e1bf42466062a67ef18e99f8d6a`, T058's landing). No
      workflow file moves.
    - The falsifier, `make pins` in the openDox root at the PR's head, reads
      `pins ok`: both gitlinks equal their pin files, and both tree digests
      recompute (the code leg's is `97536dbe7454…`).
- [x] T059 [US4] [oXc] **5.4a: openXdox contributes its governed generator,
  registry and source through the seams**, the governed half of R1Q10 (a).
  - It keeps `generator.py`, `snapshot.py`, `snapshot_registry.py`,
    `completeness.py` and `corpus_root.py`.
  - **The registration path (holder decision, 2026-09-27, at T052).** The
    generator seam needs one explicit registration in openxFactory's
    process, and the seam does not read the profile. T059 makes it from
    openXdox's own profile-registration path, the hook openxFactory already
    calls, so that T064 would need no host line (openDox-code#54). That
    reading was revised at T059's landing (below): T064 owed one host line,
    and openxFactory#1215 → `fcb45380` carries it.
  - It moves `pyproject.toml`'s `opendox @` pin to the phase-2 openDox-code
    commit (step 3). The ratchet is lowered for T055's closed reaches in the
    same landing.
  - T060 has landed first, so openXdox's own views keep matching the governed
    snapshot once the pin carries openDox's neutral `SNAPSHOT_VALUES`.
    openxFactory's served views do not, until its profile composes the
    facet's `values` block (T066, R1Q26 (a)).
  - **The second protected edit (R1Q26 (a)).** At this pin the facet's
    `values` block changes the `values.*` leaves of the served display as
    well, so this landing edits
    `tests/test_gate_loop_views.py::test_the_overlay_changes_four_words_and_the_named_absence_and_nothing_else`
    to expect them, and no other assertion. The edit is entered in the
    reviewed allow-list with its reason, as batch I amends 12.5's falsifier.
  - **Realizes**: 5.4a, 9.5 (step 3, part).
  - **Falsifier**: seam tests that show openXdox's contributions are the
    registered ones; and 5.4a's generator suites, run in F5.2's environment as
    batch G amends it, with openxFactory's `scripts/` composed at a named
    commit (R1Q23 (a)). `tests/test_snapshot.py` runs with its two schema
    cases deselected, since they wait for T061 (R1Q25 (b)):
    `--deselect tests/test_snapshot.py::test_minimal_snapshot_validates_against_pinned_validator`
    and
    `--deselect tests/test_snapshot.py::test_referentially_broken_snapshot_is_rejected`.
    Every other suite runs whole. So F5.2 whole is T061's, and T063 runs it
    again. No arc landing edited the suites except through R1Q7 (a)'s
    allow-list (T007 batch C). F5.2 takes them by glob: six in research, seven
    at openXdox-code `e28930bf` (T005). The whole-suite check (9.2) also runs
    `tests/test_gate_loop_views.py`, green with its two entered edits.
  - **Ruled**: R1Q6 (d), R1Q7 (a), `5817152735`; R1Q10 (a), R1Q23 (a),
    `5850003126`; R1Q26 (a), `5851950767`.
  - **After**: T052, T055, T060, T062, T067, T007 (batches C and I), T040 (the
    ratchet's single-writer order).
  - **Landed**: openXdox-code#35 → `839492d9`. It pins openDox-code `047bb4fa`,
    T062's commit. Its body records these holder rulings:
    - **The registration path is REVISED** (holder, 2026-09-29), and the
      decision of 2026-09-27 above rested on a misread. openxFactory's
      `register_openxfactory()` calls `openxdox.domain_profile.load()` and
      registers the composite with openDox alone, and never calls
      `openxdox.domain_profile.register()`. So the contributions register
      through an explicit `openxdox.projection_contributions.register()`
      (idempotent, all or none), which `openxdox.domain_profile.register()`
      also calls, and `load()` stays free of side effects. **T064 therefore
      owes one host line**, that call in `register_openxfactory()`, on
      F11.1's `HOST` surface. T064's own text was corrected in
      openxFactory#1213 → `80217a92` (T066's non-arc PR).
    - `tests/conftest.py` registers openxFactory's
      `corpus_adapter_openxfactory.home_corpus` where F5.2's environment puts
      `scripts/` on `PYTHONPATH`, and registers nothing in a lone checkout, so
      4.1a's refusal stands there.
    - The respelled call in `tests/test_session_snapshot.py` is an R1Q7 (a)
      allow-list entry. Seven consumer-schema reds that fail at both pins are
      deselected in T059's F5.2 run with R1Q25 (b)'s reason. Three pre-arc reds
      in `tests/test_session_snapshot.py` are deselected with the reason "red at
      both pins; pre-arc carve residue; not the arc's", and stay open for F5.2
      whole (T061, T063).
    - `tests/test_seam_assembly_beside_gate_and_projection.py` left the
      declared exclusion (67 → 66), and T059 joined that file's single-writer
      chain, T044 → T059 → T061.
- [x] T061 [US4] [oXc] **7.3: the consumer's validator lookup through the
  installed distribution**, with no parent walk (R1Q14 (a)). The lookup
  ignores its start and resolves the installed distribution's own validator.
  C3's `test_a_start_outside_the_product_is_refused_not_walked` is revised in
  the same landing.
  - **In phase 2, beside openDox's own validator (R1Q25 (b)).** The RULED
    release map puts Group 7 here. This task follows T059, whose pin brings
    openDox's validator (T057, T058), so each of openDox's kinds that the
    consumer's validator gives up in a lone install already has a validator
    of its own. openxFactory's four kinds keep this one wherever openxFactory's
    tree supplies their schemas (R1Q27 (a)). Until this task lands, phase 1's
    check declares `tests/test_snapshot.py` in the exclusion (T043). This PR
    removes that entry, since the file then passes and T041's test would
    refuse it.
  - 7.3's falsifier names two tests, and neither exists yet:
    `tests/test_snapshot.py::test_the_validator_is_the_installed_consumers_own`
    and
    `tests/test_validate_ideation_dashboard_contracts.py::test_every_schema_the_consumer_validates_is_on_disk`.
    - The first is added to one of 5.4a's protected suites. C3's test is
      revised in another, `tests/test_snapshot_validator_home.py`, which 5.4a's
      glob selects since T005. T007's batch F admits both edits to the
      reviewed allow-list, each entered with its reason (R1Q14 (a)). If no
      earlier task has created the reviewed allow-list, this PR creates it.
    - The second goes into a contract-family file that T043 declared in the
      exclusion (R1Q24 (a)). F7.1 still runs it by node id, because pytest
      collects a file named on its command line even when `collect_ignore`
      lists it (pytest 8.4.2, T006). The file's module level only computes
      paths, so it imports in a lone checkout (read at `e28930bf` for T019).
      Those paths are the carve's: its `ROOT` is `parents[2]`, above the
      checkout (`:28`). So the new test resolves the validator and its schemas
      through the installed distribution, and never through the module's own
      paths (V2-10).
  - **The ten walk-premise cases (RULED `5916000030`, item 4, *"Reword as
    reviewed entries (Recommended)"*).** Ten existing tests assume a
    validator is found by walking up from a start. Nine are in
    `tests/test_snapshot_validation_launch.py`, and one,
    `test_a_missing_validator_is_unavailable_not_a_verdict`, is in
    `tests/test_snapshot.py`. Each keeps its real assertions, and only its
    premise changes to 7.3's answer: its stub is planted as the
    distribution's own validator, or the distribution carries none. Each
    is its own R1Q7 (a) entry in the reviewed allow-list, which T007's
    batch K admits. One case,
    `test_a_run_dir_beside_a_checkout_still_uses_that_one_first`, inverts
    its expected answer and keeps its name. This landing's several entries
    for one suite chain in the order listed, and F5.2's call passes
    `--chains` to `scripts/protected_suites.py`, which this task extends.
    12.5's call does not.
  - **What the validator validates (R1Q27 (a)).** 7.3 locates *"its three
    schemas (7.1's openXdox-spec three)"*, `ideation-dashboard-snapshot`, its
    `-index` and `gate-action-record`, through the installed distribution, and
    the validator validates those three wherever it runs. It reads them from
    the installed distribution, unless the tree it runs from carries its own
    `contracts/schemas/`, which is read first, as the answered option has it
    (*"a tree's own `contracts/` read first"*). openxFactory's farm is such a
    tree, and it relies on the rule: it runs a copy of the script from a
    scratch directory, outside any installed distribution
    (`doxbench_contracts._composed_validator`). The validator validates the
    family's other seven kinds only where their schemas are supplied: by that
    tree's own `contracts/schemas/`, or by the directory `CONTRACTS_DIR`
    names, the assembly's declared channel for a contract the code reads but
    does not own, which never supplies the three. So a lone install validates the
    three from its distribution, and openxFactory's farm, which supplies the
    whole family, still validates all ten, as today. The second named test
    reads *"every schema this install validates is on disk"* (batch I): each
    kind the running install will validate has its schema on disk, and in a
    lone install the three come from the distribution. Where the other seven
    kinds are validated:
    - openDox-code's `workbench.py:442` (`validate_manifest`, the
      `ideation-workbench` manifest) reaches openDox's own validator from
      T055 on.
    - openxFactory's `doxbench_contracts.delegated_semantic_validation` (the
      doxBench wire kinds) and `tests/ideation-dashboard/conftest.py`'s
      `find_openxfactory_validator` (workbench manifests, besides the
      consumer's own kinds) run this validator in openxFactory's farm, which
      supplies the whole family's schemas, so it keeps validating their kinds
      there (R1Q27 (a)). T066 moves neither.
    - openXdox-code's own test files that run this validator are listed in
      this PR's body, each with the kinds it validates and where it runs. A
      search at `e28930bf` for T019 found three groups. The snapshot suites and
      `test_validator_schema_home.py` validate the consumer's own kinds or its
      lookup. The declared exclusion holds the rest in release 1, for
      `doc_health` or as contract-family files, with
      `test_doxbench_blank_reason.py` among the latter if T043's triage puts
      it there. `test_aggregation_register_instance.py` skips in a lone
      checkout, where no aggregation register exists. A file that runs in the
      whole suite and validates one of the seven moves to openDox's validator
      in this PR, which T059's pin makes available. The holder adds the list
      to T008's direction-arc record.
    - **openxFactory's four kinds (R1Q27 (a)).** No code caller validates
      them through this script (a search of openxFactory at `a65230f6` for
      T019), but openxFactory's `contracts/manifest.yaml` names it as their
      validator. Three retained rows name it, two as the enforcer of their
      rules and one as the script consumers run. The cross-reference
      validator delegates the register's rules to it, and
      `contracts/README.md` documents its `--transition`. openxFactory's farm
      (`doxbench_contracts._composed_validator`) runs it with openxFactory's
      own schemas beside it, which it reads first
      (`validate-ideation-dashboard-contracts.py:119-121`), so it keeps
      checking what those rows say it checks, and no contract row changes.
  - **openxFactory's lanes read this lookup (R1Q14's T006 paragraph).** The
    nightly lane calls `find_validator()` with no start and `product_root()`
    (`nightly_lane.py`, `_pinned_validator` and `_pinned_validator_missing`).
    The refresh lane's seal holds `VALIDATOR_SCRIPT_PATH` equal to
    `VALIDATOR_RELPATH` (`dashboard_refresh_lane.py`). Both validate
    snapshots, which stay the consumer's kind. This task keeps those three
    answers for a source checkout, which is how openxFactory composes the leg,
    so neither script needs an edit. The farm and the seal also rely on a
    fourth: a tree's own `contracts/schemas/` is read first, and this task
    keeps it too (R1Q27 (a); V2-8). The seal test's assertion that a start
    outside the product answers `None` does change under R1Q14 (a), and T066
    revises it. If this task cannot keep the four answers, the script edits
    ride in T066 too.
  - The package data edits openXdox-code's `pyproject.toml` after T059's pin
    move (plan.md's single-writer table). `test_validator_schema_home.py`,
    which C3's PR 2 added, is revised with the schemas' new home. It is not a
    protected suite.
  - **Realizes**: 7.3.
  - **Falsifier**: F7.1, including its two named tests, the second as batch I
    reads it; and F5.2 whole, as T007's batches C, F, G and K amend it, which
    this landing makes reachable.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q14 (a), R1Q24 (a), R1Q25 (b),
    `5850003126`; R1Q27 (a), `5851950767`; the ten cases, `5916000030`,
    item 4.
  - **After**: T059, T067, T007 (batches C, F, I and K), and C3's
    openXdox-code PR 2 (openXdox-code#28, landed as `e28930bf`).
  - **Landed**: openXdox-code#36 → `6a3b93b9`.
    - The validator and its own three schemas ship as package data
      (`openxdox.contracts`, each copy checked against a recorded digest before
      it is read), and `find_validator` ignores its start.
      `referencing>=0.28.4` and `rfc3339-validator>=0.1.4` are runtime
      dependencies (Brett Heap, `5916000030`, *"Keep as runtime deps"*).
    - `tests/test_snapshot.py` and its `consumer-schemas` reason left the
      declared exclusion (66 → 65). Twelve allow-list entries were made
      (R1Q7 (a)): batch F's two (`tests/test_snapshot.py` and
      `tests/test_snapshot_validator_home.py`), and batch K's ten, one more
      for `tests/test_snapshot.py`, chained with batch F's, and nine for
      `tests/test_snapshot_validation_launch.py`, chained.
    - F7.1, as #1144 writes it, exits 1 at #35's head and 0 after (`2 passed`).
      F5.2 whole, in batch G's environment, passes every suite but
      `tests/test_session_snapshot.py` (20 passed, 3 failed): the three failures
      are T059's ruled pre-arc reds, which T063 still owns.
    - The list this task owes the direction arc's record, of the excluded
      files that validate a kind the narrowed validator gives up, is in the
      PR's body and, as bookkeeping, in that record (T008 above).
- [x] T066 [US4] [oxF] **openxFactory at both pins, ahead of T064 (a non-arc
  act).** T064 composes T060's facet and T061's lookup into openxFactory.
  Before T064, this act makes openxFactory hold at both pins. It carries no
  `Arc:` trailer, because it is openxFactory's own change and correct with or
  without the arc's commits, like F3's overlays (plan.md § "The trailer, the
  guard and Rule 6"). R1Q14's T006 paragraph names this route, and T019 chose
  it (R1Q14 (a), R1Q25 (b)).
  - **The validator callers are not moved (R1Q27 (a)).**
    `scripts/ideation_dashboard/doxbench_contracts.py`'s
    `delegated_semantic_validation` and `tests/ideation-dashboard/conftest.py`'s
    `find_openxfactory_validator` run the consumer's validator in
    openxFactory's farm, which supplies the family's schemas beside
    openxFactory's own. Under R1Q27 (a) the validator keeps validating every
    kind the tree it runs from supplies, so both keep working at T064's pins,
    and neither is edited. Round 2 had this act send openDox's kinds to
    openDox's validator, because T061 then narrowed the consumer's validator
    to three kinds everywhere. R1Q27 (a) narrows it only where a tree supplies
    nothing else, so that reason is gone, and so is V2-12's question of how
    each kind would be dispatched (`evidence/analyze-round-3.md`).
  - **The facet's `values` block (R1Q26 (a)).** This act composes the block
    into openxFactory's profile (`scripts/profile_openxfactory.py`, which
    composes only `stages` today), so openxFactory's served views match the
    governed snapshot at T064's pins, and it updates
    `tests/test_engineering_profile_display_facet.py` (`:272`, `:566`) to
    match. At the current pins openXdox's facet has no block, so nothing
    changes there (V2-5).
  - `tests/ideation-dashboard/test_dashboard_source_seal.py`'s
    `test_the_confined_locator_never_adopts_the_sealed_validator` asserts
    `find_validator(start) is None` for starts inside the seal. Under R1Q14
    (a) the lookup ignores its start, so the assertion becomes what the test
    is for: the answer is never the sealed copy. That holds at both pins.
  - `nightly_lane.py` and `dashboard_refresh_lane.py` need no edit if T061
    keeps the four answers they read. If it does not, their edits ride here,
    in the same both-pins form.
  - Before its PR opens, its writer runs openxFactory's whole `pytest-suite`,
    and the `openxdox-consumer-gate` suite at its floors (`MIN_PASSED` 1137
    and `EXPECT_SKIPPED` 0 at `79a720a2`), since `pytest-suite` alone passes
    on skips (V2-25). It runs them with the two roots at T064's candidate
    commits: the openDox root at T062's, and the openXdox root with its code
    at T061's. Every red test is named in the PR body. Each is fixed here, or
    raised with the holder if no both-pins form exists.
  - **Realizes**: none of the 69 boxes. It keeps requirement 1 at T064's pins
    (SC-007).
  - **Falsifier**: openxFactory's `pytest-suite` and the consumer gate's
    suite at its floors, green on this PR at the current pins and at T064's
    candidate pins, all quoted.
  - **Ruled**: R1Q14 (a), R1Q25 (b), `5850003126`; R1Q26 (a), R1Q27 (a),
    `5851950767`.
  - **After**: T061, T062, T067.
  - **Landed**: openxFactory#1213 → `80217a92`, a squash whose tree equals the
    PR head `2cc8e926`'s.
    - **A non-arc landing**, as T091 and plan.md § "The trailer, the guard and
      Rule 6" have it: the squash message carries no `Arc:` trailer, and the
      PR touches nothing under `openspec/`.
    - openxFactory holds at both pin sets. The current pins are openDox
      `663ac683` and openXdox `57e2b8f2`. T064's candidates are the openDox
      root at T062's `d5098297` and the openXdox root with its code at T061's
      `6a3b93b9`.
    - CI at the PR head passes all 12 checks. `pytest-suite` reads
      `selected=9335 passed=9329 skipped=6`, and the consumer gate reads
      105/105/0 for the pin suites and 1480/1480/0 for
      `tests/ideation-dashboard`.
    - At the candidate pins, 187 reds need T064's host line and cannot be
      answered in openxFactory. With the host line, three remain, none with a
      both-pins form: the pin verifier's snapshot literal, and
      `RENDER_LEG_MODULES` and `RENDER_UNIT_IMPORTS` gaining
      `projection_contributions.py`. All three go into T064's arc commit, on
      declared F11.1 surfaces (the holder's decision, recorded in #1213's
      body).
    - It also carried T064's plan-text correction, the one host line, as the
      holder decided (a plan edit in T064's own arc PR sits on no F11.1
      surface).
- [x] T064 [US4] [oX] [oxF] **Phase 2's consumer pins** (T090 steps 5–6). The
  openXdox root moves to T061's commit, the phase's last openXdox-code
  landing, and to T062's root commit. Host wiring is needed only if
  openxFactory's composite has to register a generator contribution, and it
  does, so T064 owes one host line (below); confirm it by `pytest-suite`.
  The facet's `values` block reaches openxFactory's served views only through
  T066's composition (R1Q26 (a)).
  - **The one host line (holder decision, 2026-09-29, at T059, which REVISES
    the decision of 2026-09-27 at T052).** `scripts/opendox_host.register_openxfactory()`
    calls `openxdox.projection_contributions.register()`, which T059 added
    (openXdox-code#35 → `839492d9`), and a test under `tests/domain_profile/`
    pins it. `scripts/opendox_host.py` is on F11.1's `HOST` surface, so the
    guard admits the line.
    - The revised decision read: *"T059 registers openXdox's generator from
      openXdox's own profile-registration path, the hook openxFactory already
      calls (`register_openxfactory()` makes the profile registration today).
      So the line above, that this composes openXdox's profile and so needs
      none, stays true (openDox-code#54)."* That misread the host.
      `register_openxfactory()` calls `openxdox.domain_profile.load()` and
      registers the composite with openDox alone
      (`opendox.domain_profile.register(composite)`). It never calls
      `openxdox.domain_profile.register()`, the hook that registers the
      governed projection too since T059.
    - The revision is recorded in the lane's later-slice notes (2026-09-29
      ~23:55Z) and in openXdox-code#35's body.
    - This correction rides in T066's non-arc PR, not in T064's (holder
      decision, 2026-09-30). A plan edit in T064's arc PR sits on no F11.1
      surface, so the guard would refuse it: a dry run on a simulated T064
      commit refused `specs/034-opendox-standalone-operation/tasks.md` and
      nothing else.
  - T066 has landed first, so openxFactory's profile composes the block and
    its seal test holds at these pins. Its validator callers need no move:
    under R1Q27 (a) the consumer's validator keeps validating every kind
    openxFactory's farm supplies.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: as T047's, with the consumer gate's suite at its floors.
  - **Ruled**: R1Q26 (a), R1Q27 (a), `5851950767`.
  - **After**: T059, T060, T061, T062, T066, T047 (the pin pairs'
    single-writer order).
  - **Landed**: openXdox#21 → `f257e021` (the openXdox root: code
    `6a3b93b9`, openDox pin `d5098297`), then openxFactory#1215 →
    `fcb45380`, an arc landing whose squash carries the `Arc:` trailer.
    - Both pin pairs move in ONE commit (#1215's `59866105`), departing from
      T090 step 6 on the holder's decision of 2026-09-28: #21 moves the openDox
      pin that `verify-opendox-pin.py` check 5 reads through the openXdox
      gitlink. openDox is `d5098297` (`2815ca23…`, 28 records), and openXdox
      is `f257e021` (`52f0598e…`, 29 records, recomputed three ways).
    - The host line calls `openxdox.projection_contributions.register()` once
      openDox answers the profile and before `register_seams()`, so a refused
      profile writes no seam (Copilot's finding at `d6c47f4f`, answered in
      `5663b4ed`). `tests/domain_profile/test_host_registers_openxdox_projection.py`
      pins it in 9 cases.
    - #1213's three no-both-pins-form reds are answered on admitted F11.1
      surfaces (holder decision (c)): `RENDER_LEG_MODULES` and
      `RENDER_UNIT_IMPORTS` gain `projection_contributions.py`, and the q7
      literal moves to `d5098297`. 129 carve admissions are added and pinned in
      `tests/carve_arrival`.
    - CI at the PR head passes all 12 checks. `pytest-suite` reads
      `selected=9345 passed=9339 skipped=6`, and the consumer gate reads
      105/105/0 and 1481/1481/0.
- [x] T065 [US4] [oxF] **Phase 2's interim F11.1**, by T093's procedure, with
  `ARC_TIP` at T064's landing. Record the output in
  `evidence/f11.1-phase2.txt`, with no `Arc:` trailer, and link it from
  this feature's README entry.
  - **Falsifier**: F11.1, as widened by T007 batch A, prints `requirement 1
    holds`.
  - **After**: T064.
  - **Landed**: [`evidence/f11.1-phase2.txt`](evidence/f11.1-phase2.txt),
    with `PACKET_MERGE=94b6f7f1` and `ARC_TIP=fcb45380` (#1215). It prints
    `requirement 1 holds: 0 note(s) annotated, every other path a declared
    surface (11.1)` (exit 0) over the arc's two landings, `f56c87c6` (T047)
    and `fcb45380` (T064). A planted path on no surface is refused. The
    admitted list did not grow.
- [x] T063 **Phase 2 checkpoint.** Run and quote F5.1, F5.2 (as amended by
  T007's batches C, F, G and K, its last step passing `--chains`), F5.3,
  F7.1 (T061, back in this phase by R1Q25
  (b), and read as batch I records R1Q27 (a)) and F7.2. Then run a standalone
  `generate-and-open` serving the fixture, and quote T065's interim F11.1
  output.
  - **Ruled**: R1Q23 (a), R1Q25 (b), `5850003126`; R1Q27 (a), `5851950767`;
    `5916000030`, item 4; F5.2's close, `5962785556`, item 1.
  - **After**: T064, T065, T007 (batches C, F, G, I and K).
  - **Run** (2026-10-02; `evidence/checkpoint-phase2.md`): at openDox-code
    `047bb4fa`, openXdox-code `6a3b93b9` and, for F5.2's composition,
    openxFactory at T064's landing `fcb45380`.
    - F5.1, F5.3, F7.1 and F7.2 pass, and a standalone `generate-and-open`
      serves the fixture.
    - F5.2, as batches C, F, G and K amend it, exits 1 on
      `tests/test_session_snapshot.py` alone (20 passed, 3 failed), the same
      at openxFactory `2656e8c2`. The three are the pre-arc reds the holder
      ruled (a) at T059 (openXdox-code#35's body, item 6), which T061 left to
      this task. The six other suites pass whole, and the `--chains` step
      admits all four protected suites the arc touched.
    - **F5.2 is quoted red, as ruled, and phase 2 closes.** RULED
      `5962785556` (Brett Heap, 2026-10-02, item 1, *"Fix in T086, close at
      phase 3 (Recommended)"*): T063 quotes F5.2 red, names the three tests
      (`test_a_new_serve_process_re_registers_the_session_at_startup`,
      `test_a_session_key_is_validated_against_the_roster_before_url_composition`
      and `test_the_hosted_session_arrival_path_is_recorded_and_not_built`),
      and is ticked. T086 repairs them under R1Q7 (a)'s allow-list, and
      F5.2's box closes at T089, so the pins move only once more, at T094.
      #1144's F5.2 text is unchanged.
    - T065's interim F11.1 output (openxFactory#1217 → `1f670bc3`) is quoted
      there, and it was re-run with the same line, `requirement 1 holds`.

---

## Phase 3: it installs (US3 and US4)

Planned on answers since T069 (`5850003126`): R1Q15 (b), R1Q16 (i)–(iv) as
recommended, R1Q17 (b), R1Q18 (a) and R1Q19 (a), with R1Q10 (a) and R1Q12 (a)
for chat standalone. Every phase-3 task comes after T063 and T069.

**Goal**: one documented command installs and starts the whole product, with
its bundled datastore, the local mode, the served bundle, and chat with a clear
no-model state. The install is `pip install "opendox[local]"`, and the command
is `opendox generate-and-open --local …` (R1Q15 (b), R1Q16 (iii)). T099
publishes the package to PyPI at the cut, so that the install line works as
written (`5962754358`). `consumer_reach.py` is gone.

**Independent test**: T089, then T095 and T096.

- [x] T069 **Phase 3's round.** DONE in this revision, on `5850003126`. No
  task of phase 3 starts before it is done.
  - The answers to R1Q15, R1Q16, R1Q17, R1Q18 and R1Q19 are encoded in
    `spec.md` § Clarifications and `clarify-questions.md`, with R1Q21's.
  - The #1144 lines they amend are T007's batch H (§ "Ruled amendments"). None
    changes a requirement or a scenario. One line follows from two answers
    together: F10.1 passes `--local` (R1Q15 (b)), and the local mode's server
    arrives only with the `local` extra (R1Q16 (iii)), so F10.1 installs
    `.[local]` as F13.1 does. `evidence/analyze-round-2.md` records it.
  - Phase 3 is re-planned below, in `plan.md`, and in § "Phase 3 writer
    slices", and its PROVISIONAL marker is lifted.
  - `/speckit-analyze` found nothing CRITICAL (`evidence/analyze-round-2.md`,
    T009).
  - **Ruled**: R1Q10 (a), R1Q12 (a), R1Q15 (b), R1Q16 (i)–(iv), R1Q17 (b),
    R1Q18 (a), R1Q19 (a), `5850003126`.
  - **After**: T009.

### Group 13: the install's shape (`runtime/`)

- [ ] T071 [US3] [oDc] **13.2 and 13.3.** `load_settings` refuses a
  non-PostgreSQL DSN, naming the one dialect kept. It refuses the same
  credential in both settings, naming `OPENDOX_MIGRATION_DATABASE_URL`. The
  migration DSN is required on the migrate path only, which is `migrate` and
  `reset`. `serve` and `status` keep it optional, and it is never defaulted
  from `OPENDOX_DATABASE_URL`. The collapse refusal and the non-PostgreSQL
  refusal stand. This corrects the earlier wording, "stops being
  optional" (RULED `5880893901`, Brett Heap, 2026-09-28: *"Required only
  for migrate (Recommended)"*). #1144's 13.3 text is unchanged.
  - **Realizes**: 13.2, 13.3.
  - **Falsifier**: F13.1's `load_settings` block.
  - **After**: T063, T069.
- [ ] T070 [US3] [oDc] **13.4, 13.5 and 13.6: `OPENDOX_INSTALL_MODE`, and the
  `--local` flag.**
  - `local` or `hosted`, defaulting to `hosted`, and read beside
    `OPENDOX_OIDC_ISSUER`.
  - `generate-and-open --local` selects local exactly as
    `OPENDOX_INSTALL_MODE=local` does (R1Q15 (b), as batch H's 13.4 addendum
    reads). With neither, the install is hosted (13.5).
  - A flag and a setting that disagree, such as `--local` with
    `OPENDOX_INSTALL_MODE=hosted`, are refused, naming both, so no explicit
    selection is silently overridden. No answer rules this case. The refusal
    is the plan's fail-closed reading (Principle VII), which
    `evidence/analyze-round-2.md` records for Brett. Batch H does not write it
    into #1144.
  - `local` needs no broker, binds loopback only, and refuses a non-loopback
    `--host` with no opt-in.
  - `hosted`, or unset, with no issuer refuses, naming the setting.
  - Hosted mode is otherwise unchanged.
  - **Realizes**: 13.4, 13.5, 13.6.
  - **Falsifier**: F13.1's refusals, and a test of the disagreeing pair.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q15 (b), `5850003126`.
  - **After**: T071, T007 (batch H).
- [ ] T072 [US3] [oDc] **13.1: the bundled PostgreSQL server** (R1Q16).
  - The document server starts it as its own child process and reports it
    (i). Starting and migrating the store is all release 1 asks of it, since
    the document surface reads nothing from it yet (ii). It stops with the
    entry point (iv).
  - It ships as the `opendox[local]` extra, which carries the `runtime`
    extra's packages and the server's own (iii). The `test` extra gains them
    too, as T036 gave it the `runtime` extra's, so F9.1's `.[test]` install
    still runs every case.
  - Its data and socket directories live under `OPENDOX_STATE_DIR`, with NO TCP
    listener, and both DSNs are supplied.
  - `runtime status` reports `database_bundle` (`data_dir`, `socket_dir`,
    `pid`).
  - **Realizes**: 13.1.
  - **Falsifier**: F13.1's TCP-listener block, which reads the kernel's socket
    table at run time, and its `runtime status` block.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q16 (i)–(iv), `5850003126`.
  - **After**: T070.
- [ ] T073 [US3] [oDc] **13.4a: `/capabilities` gains an `install` block**,
  read from the serving process's own settings, which is the process that owns
  the bundled server (R1Q16 (i)). `serve.py` is a single-writer file.
  - **Realizes**: 13.4a.
  - **Falsifier**: F13.1's `caps.json` block.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q16 (i), `5850003126`.
  - **After**: T072, T055 (`serve.py`'s single-writer order).
- [ ] T074 [US3] [oDc] **Run F13.1**, as batch H amends it: it installs
  `.[local]`, and its local probe's `OPENDOX_INSTALL_MODE=local` is the same
  selection as `--local`.
  - **Realizes**: F13.1.
  - **Falsifier**: F13.1 itself, as amended. This task is that run, quoted in
    its PR.
  - **Ruled**: R1Q15 (b), R1Q16 (iii), `5850003126`.
  - **After**: T073.

### Group 10: the door

- [ ] T075 [US3] [oDc] **10.2 and 10.2a.** The entry point serves the 42-file
  bundle, reachable in a browser from an openDox-only install. `intent-feed.js`
  is not owed (10.2a is a declaration, recorded in the PR).
  - **Realizes**: 10.2, 10.2a.
  - **Falsifier**: F10.1's fetch, as batch H amends it: a `.[local]` install
    and `--local`, which start the bundled server, so it follows T072.
  - **Ruled**: R1Q22 (a), `5817152735`.
  - **After**: T056, T038, T063, T069, T072, T007 (batch H).
- [ ] T076 [US3] [oD] **10.3: the openDox root's `README.md` documents the one
  command.** It is `pip install "opendox[local]"`, then
  `opendox generate-and-open --local …` (R1Q15 (b), R1Q16 (iii), as batch H's
  10.3 addendum reads). No `Makefile` target is added, since it has a
  shape-pin row.
  - **Realizes**: 10.3.
  - **Falsifier**: review, and AT-R1 step 4 follows it literally.
  - **Ruled**: R1Q15 (b), R1Q16 (iii), `5850003126`.
  - **After**: T074, T075, T087 (the README documents the command the root
    pins).
- [ ] T099 [US3] [oDc] **Publish to PyPI (10.3's install line).** openDox-code's
  sdist and wheel go to PyPI as `opendox`, by trusted publishing (OIDC), so
  10.3's `pip install "opendox[local]"` works as written. No token or secret is
  stored anywhere. Today `pypi.org/pypi/opendox/json` answers 404 (RULED
  `5962754358`, item 1, *"Publish to PyPI at the cut (Recommended)"*). This task
  is the publish alone. The workflow it dispatches and the version bump it
  publishes are T101's.
  - **The release commit, and the order (RULED `5963162921`, *"0.1.0
    (Recommended)"*).** Release 1's version is 0.1.0.
    - T101 lands last among the phase-3 openDox-code landings that change the
      shipped package, and its last landing is the version bump.
    - T087 pins that commit in the openDox root.
    - The workflow publishes only the commit that the root's
      `contracts/code-pin.yaml` names, and that is on openDox-code's `main`,
      never requiring `main`'s head. T095 lands after T089, so `main` may have
      moved on by the cut.
  - **At the cut, on Brett Heap's publish word**: the holder creates the tag
    `v0.1.0` at the pinned commit and dispatches the workflow with `version`
    0.1.0, on that tag or on `main`. A dispatch on a tag must name
    `v<version>`. Brett Heap approves the `testpypi` environment's deployment,
    and, once the TestPyPI install has passed, the `pypi` environment's.
  - **Brett Heap's one-time setup**, before the first dispatch:
    - on pypi.org, a pending trusted publisher for `opendox` (owner `opensoft`,
      repository `openDox-code`, workflow `release.yml`, environment `pypi`);
    - the same on test.pypi.org, with environment `testpypi`;
    - in openDox-code's GitHub settings, the two environments, each with a
      required reviewer. The build job refuses until both name one.
  - **Realizes**: 10.3.
  - **Falsifier**: the release workflow's verify job, then a TestPyPI dry run
    installed with `pip install --index-url https://test.pypi.org/simple/
    --extra-index-url https://pypi.org/simple/ "opendox[local]"` in a fresh
    venv, then the PyPI publish at the cut.
  - **Ruled**: `5962754358`, item 1; the version and the release commit,
    `5963162921`. The split into T101 and this task is the holder's decision
    of 2026-10-03, after Copilot's review of openxFactory#1220.
  - **After**: T101, T087, T089 (the publish happens at the cut, after phase
    3's checkpoint).
- [ ] T101 [US3] [oDc] **T099's release step: the release workflow, and the
  version bump to 0.1.0.** Two openDox-code landings, which T087 pins and
  T099 publishes.
  - **The release workflow** (openDox-code#78) is `.github/workflows/release.yml`,
    with its hash-locked tools and `tests/test_release_workflow.py`. It runs
    only when dispatched by hand, with a `version` input that must equal
    `pyproject.toml`'s. Its build job refuses a commit the openDox root does
    not pin, and an environment with no reviewer. Then it verifies the files
    before any upload:
    - the requirements, against `pyproject.toml`'s, with the `local` extra
      (T072);
    - the `opendox` console script;
    - every tracked file of the web bundle (T075) and of `src/`, and the
      migrations;
    - and, from the built wheel in a fresh venv, the whole requirement
      closure of `opendox[local]`, the bundled server's binaries, and
      `opendox --help`.

    It publishes to TestPyPI first, in a `testpypi` environment, and then to
    PyPI, in a `pypi` environment. Its artifact checks pass only once T072 and
    T075 have landed. The same PR adds `readme` to openDox-code's
    `pyproject.toml`, so that file's single-writer order runs T072 → T075 →
    T101.
  - **The version bump** (openDox-code#79) sets `version = "0.1.0"` (RULED
    `5963162921`). It is the last of the landings below, right before T087.
  - **Realizes**: 10.3 (part, with T099).
  - **Falsifier**: `tests/test_release_workflow.py`, in the required check.
    The workflow's build job, over the pinned commit, is T099's.
  - **Ruled**: `5962754358`, item 1; `5963162921`. The split is the holder's
    decision of 2026-10-03.
  - **After**: T070–T075, T077, T078–T085, T088, T100 (every phase-3
    openDox-code landing that changes the shipped package, with the T074,
    T077 and T083 runs).
  - That line also stands for openDox-code#64, the broker-path hardening,
    which is no task of this plan. T095's `acceptance/` harness ships nothing,
    so T101 does not wait for it.
- [ ] T077 [US3] [oDc] **Run F10.1**, as batch H amends it: it installs
  `".[local]"`, and it runs `opendox generate-and-open --local …`. The local
  mode starts the bundled server, so this run follows T072.
  - **Realizes**: F10.1.
  - **Falsifier**: F10.1 itself, as amended. This task is that run, quoted in
    its PR.
  - **Ruled**: R1Q15 (b), R1Q16 (iii), `5850003126`.
  - **After**: T075, T072.

### Group 16: chat's model configuration (`doxbench_binding.py`, then `doxbench_provider.py`)

- [ ] T078 [US3] [oDc] **16.1: `openai-chat-v1`.** A second `DIALECTS` member.
  The chat-completions request (`model`, `messages`) and its answer
  (`choices[0].message.content`) are spoken by an arm in
  `doxbench_provider.py` alone. An unknown dialect is still refused.
  - **Realizes**: 16.1.
  - **Falsifier**: F16.1's dialect assertion.
  - **Ruled**: R1Q22 (a), `5817152735`. `doxbench_binding.py` is a
    `moved_verbatim` row, and editing it needs no declared-edit act.
  - **After**: T063, T069.
- [ ] T079 [US3] [oDc] **16.2: a `model` field**, sent as the request's model
  and set by `model-binding add|edit --model`. The record grows from nine
  fields to ten, and none of them can hold a secret.
  - **Realizes**: 16.2.
  - **Falsifier**: F16.1's `BINDING_FIELDS` assertion.
  - **Ruled**: R1Q22 (a), `5817152735`.
  - **After**: T078.
- [ ] T080 [US3] [oDc] **16.3: refuse a raw key when it is declared.**
  - Keys in the URL and in extra fields are refused, via `carries_a_credential`.
  - A reference is resolved by a built-in resolver for `env:NAME` and the OS
    keyring, at call time and inside `doxbench_provider.py` only (R1Q17 (b)).
    A record whose reference the built-in resolver takes needs no broker, so
    `broker_argv` is not required for it. One given beside such a reference is
    refused, so each record has one resolver. No answer rules that refusal:
    it is the plan's fail-closed reading, which `evidence/analyze-round-2.md`
    records, and batch H does not write it into #1144. A test holds both.
  - An endpoint that takes no credential declares the auth kind `none`, under
    which `broker_argv` and `credential_ref` are forbidden (R1Q18 (a)). `none`
    joins `AUTH_KINDS` after the two kinds that exist, so F16.1's
    `AUTH_KINDS[0]` still names a kind that takes a credential.
  - A credential that the built-in resolver resolves travels only over
    `https://`, or over `http://` to `127.0.0.1`, `::1` or `localhost`. Any
    other endpoint is refused before the credential is resolved
    (`ENDPOINT_NOT_PRIVATE`). RULED `5880893901`, Brett Heap, 2026-09-28:
    *"Refuse unless loopback (Recommended)"*. The rule narrows where a
    resolved credential travels. An `https://` endpoint, a loopback one and
    one that takes no credential (auth kind `none`) are reached as before,
    and only a credential sent over `http://` beyond loopback is refused.
    The request that presents the credential keeps that route: it follows no
    redirect, and over plain `http://` it takes no proxy (openDox-code#63;
    batch K's note records both).
    Brett Heap answered openxFactory#1207's question, whether that needs a
    batch in #1144, with `5916000030`, item 1: *"Yes, amendment batch K
    (Recommended)"*. T007's batch K adds a dated note to #1144's requirement
    17 and scenario 17.1 ("any endpoint"), and a pointer after 16.3's batch H
    addendum. It rewrites no ratified text, and `spec.md`'s FR-009 follows
    it. The broker path is unchanged in this task.
  - **The broker path follows in a separate phase-3 draft**, openDox-code#64,
    stacked after #63 (T080's PR). It is no task of this plan, and T080's
    scope does not grow. It gives a minted token the protections above:
    `https://` or loopback only, no redirect or environment proxy, no
    chained cause or context, and a printable-ASCII check (RULED
    `5890601202`, Brett Heap, 2026-09-29: *"Yes, separate phase-3 draft
    (Recommended)"*). Batch K's note to requirement 17 records this rule for
    the broker path too. The shared broker runner's refusals carry no
    broker output, no cause and no context (RULED `5901112350`, item 2:
    *"Yes, add to #64 (Recommended)"*). An operator's own credential input
    is left unbounded by the broker's timeout (RULED `5916000030`, item 5:
    *"Leave unbounded (Recommended)"*). Neither of those two bears on the
    route.
  - **Realizes**: 16.3.
  - **Falsifier**: F16.1's three refusals, and tests of the resolver and of
    `none`.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q17 (b), R1Q18 (a), `5850003126`;
    the loopback rule, `5880893901`; batch K's note, `5916000030`, item 1.
  - **After**: T079, T007 (batches H and K).
- [ ] T081 [US3] [oDc] **16.4: "no model configured" is a state.**
  - With no binding and no harness, the catalog offers no available entry.
  - The chat rail shows "no model configured" AND how to configure one, before
    any turn. Today's copy (research R15) does not name how.
  - A turn is refused `model_capability_unavailable` before any spawn or
    contact.
  - The harness route stays, for an install where it is present.
  - The SERVED catalog route answers standalone. That needs T085's
    validators, so T081 lands after T085.
  - **Realizes**: 16.4.
  - **Falsifier**: F16.1's catalog block; `tests/test_chat_model_configuration.py`.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q10 (a), R1Q12 (a), `5850003126`.
  - **After**: T063, T085.
- [ ] T082 [US3] [oDc] **16.5: every other surface works with no model.** The
  named test covers documents, generation, the views, sessions and saving,
  which answer through R1Q10 (a)'s defaults (T084) exactly as they do with a
  model configured.
  - **Realizes**: 16.5.
  - **Falsifier**: `tests/test_chat_model_configuration.py`.
  - **Ruled**: R1Q10 (a), `5850003126`.
  - **After**: T081, T084, T085.
- [ ] T083 [US3] [oDc] **16.6, then F16.1.** `tests/test_provider_boundary.py`
  stays green as 16.1 joins the one module. Then run F16.1 whole.
  - **Realizes**: 16.6, F16.1.
  - **Falsifier**: `tests/test_provider_boundary.py` for 16.6, then F16.1 whole.
  - **After**: T080, T081, T082.

### 4.3's last reaches, and the consumer's columns

- [ ] T084 [US3] [oDc] **Route everything left, and retire `consumer_reach.py`.**
  - Route `serve_workbench.py`'s seven (`:347`, `:407`, `:408`, `:544`,
    `:1215`, `:1665`, `:2607`), `serve_project.py:246/:247`, and
    `branch_session.py:1587/:2005`.
  - Route the `gate_console` names (27 uses), `hosted_ref_refused` (2), and the
    `LateGateRoutes` and `LateProjectionRoutes` bases, through declared seams.
  - Give each seam an openDox default that the entry points register where no
    host has (R1Q10 (a)): the doxBench scope, the gate primitives behind chat's
    Save, model approval, sessions and the project register, and kickoff and
    the register. Each default is small and neutral. openXdox contributes its
    governed ones in T086.
  - Hand the gate and projection columns to the handler-contribution facet
    (R1Q1 (a)).
  - **Capability honesty (RULED `5920216845`, item 1, *"Fix in T084 + #1144
    note (Recommended)"*).** Measured at openDox-code `047bb4fa`, a
    standalone `/capabilities` answers `actions.gate` and `actions.refresh`
    true, while every `POST /actions/gate/<verb>` and `POST /actions/refresh`
    answers `404 unknown_action`. The gate flag follows the checkout's git
    identity alone (`serve.py:529` and `:533`, in `compute_capabilities` at
    `:464`).
    - Pass the route bindings the assembly collects (`serve.py:1900`) into
      `compute_capabilities` (called at `:1957`). Each `actions` flag whose
      affordance is a route this server serves is then true only where such
      a route answers. `gate` and `refresh` are true only when the bindings
      carry a route they govern.
    - Standalone, both read false. So the workbench's session controls,
      which read `actions.gate` (`sessionActionsLive`,
      `web/views/staging-workbench-model.js:1068`), are hidden too.
    - A composed host that contributes the routes reads as today.
      `notebook`, `edit` and `session` keep their conditions. `intent`
      governs a POST to another plane's intent API, a route that plane
      answers, so its condition stands too.
    - The three reaches that drop a connection standalone answer cleanly
      instead. At `047bb4fa`:
      - The document abstract's `openxdox` import (`serve_workbench.py:2611`)
        sits above its step-one check, which reads `session` and `gate`
        (`:2625`). It moves below that check, so once `gate` reads false a
        standalone request is refused `model_capability_unavailable`.
      - Model approval (`:1219`) passes its only check standalone, because
        `_intake_console_refusal` (`:875`) reads `session` alone. The project
        register (`serve_project.py:271`) has no check at all: `GET
        /project-register.json` calls `_serve_project_register` directly. Both
        are among this task's reaches, and this task routes each through its
        seam. openDox's default answers where one serves the request (R1Q10
        (a)), and otherwise the seam refuses by name (4.2).
      - None of the three ends a request with a dropped connection.
    - T007's batch L records the rule at #1144's 4.3.
  - **Every broken rule, once (RULED `5920216845`, item 3, *"Show every
    rule, grouped (Recommended)"*).** `cli._report_non_conformance`
    (`cli.py:481`) prints each broken rule id once, with its count, instead
    of the last 20 lines of the validator's output (`:490`). This task
    already ends `cli.py`'s single-writer order. No #1144 line changes,
    because F7.2 asserts only that the fixture's rule id is printed, which
    stays true.
  - **Realizes**: 4.3.
  - **Falsifier**: F4.1 whole: `consumer_reach.py` is absent, and the scan
    prints `no deferred reach names the consumer or the publisher`. Also:
    - `tests/test_capability_honesty.py` (new), over T056's standalone
      child (`tests/standalone_child.py`) and over composed hosts whose
      other conditions hold. It asserts `gate` and `refresh`
      false standalone and true on the composed host. With a gate-only host
      and a refresh-only host, it asserts each flag independently: only the
      flag whose routes are contributed reads true. Then, on each, it
      asserts that for every `actions` key that reads true, a route it
      governs does not answer `unknown_action`, so a plane that switched
      every flag off fails it. In the same module, over the same standalone
      child, a request to each of the three sites gets a structured answer
      or refusal, never `RemoteDisconnected`.
    - `tests/test_rejection_report.py` (new): a rejected snapshot that
      breaks one rule several times and a second rule once prints each rule
      id once, with its exact count. So an implementation that always
      prints `1`, or never groups a repeated id, fails it. It is a module of
      its own, clear of `tests/test_post_render_validator.py`, which T085
      edits.
  - **Ruled**: R1Q1 (a), R1Q22 (a), `5817152735`; R1Q10 (a), `5850003126`;
    items 1 and 3 of `5920216845`.
  - **After**: T055, T073 (`serve.py`'s single-writer order), T007 (batch L).
- [ ] T085 [US3] [oDc] **The standalone doxBench defaults for T027's seams**
  (R1Q10 (a)). openDox's own validators run over the packaged copies of
  openDox-spec's `xfactory-workbench-chat-turn` and
  `xfactory-workbench-model-catalog` (T057, R1Q12 (a)). There is no status
  exemption by default.
  - **T058's two workbench-manifest rules move into openDox's validator
    (RULED `5920216845`, item 2, *"Move into openDox's validator
    (Recommended)"*).** `workbench-pinned-not-checked` (every pinned keyword
    is a checked one) and `workbench-candidate-overlap` (no new candidate is
    a member or excluded) leave `default_projection`'s `WORKBENCH_RULES`
    (`default_projection.py:134` at `047bb4fa`) for `opendox.validator`. They
    take ids openDox's validator owns, in place of the identifiers the
    consumer's script gave them. Like its other rules (`ids-are-unique`,
    `candidate-names-a-group`), each states what must hold, under the
    `ideation-workbench` kind: `pinned-keywords-are-checked` and
    `new-candidates-are-disjoint`. T085 carries the old adapter ids only as
    its tests' before-state, and keeps neither as an alias. No #1144
    falsifier names either old id, so no #1144 line moves.
  - **Realizes**: 4.3 (part), 16.4 (part).
  - **Falsifier**: the served catalog route answers, with no available
    entry. Also `opendox.validator` reports the two rules as
    `pinned-keywords-are-checked` and `new-candidates-are-disjoint`, and
    `default_projection` checks neither.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q10 (a), R1Q12 (a), `5850003126`;
    item 2 of `5920216845`.
  - **After**: T057, T063, T069.
- [ ] T088 [US3] [oDc] **The lens's two seed actions** are offered only where a
  binding answers them (R1Q19 (a)). Standalone, no binding answers
  `/actions/dtn-seed` or `/actions/staging-seed`, so neither control is
  offered. `lens.js` stays the web census's one declared `?` row. Moving the
  two controls into a view extension that openxFactory contributes, which
  retires the row, is R1Q19's (b), for later and outside release 1.
  - **Realizes**: none of the 69; this is the precondition for AT-R1 step 6.
  - **Falsifier**: AT-R1 step 6.
  - **Ruled**: R1Q22 (a), `5817152735`; R1Q19 (a), `5850003126`.
  - **After**: T063, T069.
- [ ] T087 [US4] [oD] **Phase 3's openDox root pin** (T090 steps 1–2).
  - It pins the commit that carries release 1's version bump to 0.1.0 (T101,
    T099's release step, openDox-code#79), the last phase-3 openDox-code
    landing that changes the shipped package, because T099 publishes only the
    commit this root pins (RULED `5963162921`).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins` in the openDox root.
  - **After**: T074, T077, T083, T084, T085, T088, T101 (every phase-3
    openDox-code landing), T062 (the root pin's single-writer order).
- [ ] T086 [US4] [oXc] **openXdox contributes its columns.** It contributes the
  gate and projection mixins, `doxbench_scope` and its gate primitives through
  the seams, as the governed half of R1Q10 (a). `OPENDOX_BACK_IMPORTS` becomes
  `(0, 0)` in the SAME landing that moves the pin to the openDox-code commit
  T087 pins, which carries T084 (4.3's wording). That is also where 9.2's box
  closes, as batch F's addendum records (R1Q25 (b)).
  - It contributes the columns through the handler-contribution facet (R1Q1
    (a)). A protected suite that names a moved seam is respelled only under
    R1Q7 (a)'s allow-list.
  - **F5.2's three pre-arc reds (RULED `5962785556`, item 1, *"Fix in T086,
    close at phase 3 (Recommended)"*).** This landing repairs three tests of
    `tests/test_session_snapshot.py`: `test_a_new_serve_process_re_registers_the_session_at_startup`,
    `test_a_session_key_is_validated_against_the_roster_before_url_composition`
    and `test_the_hosted_session_arrival_path_is_recorded_and_not_built`.
    They are red at both phase-2 pins, as pre-arc carve residue
    (openXdox-code#35's body, item 6; T063 quotes them). The suite is one of
    F5.2's protected suites, so each repair is its own entry in R1Q7 (a)'s
    reviewed allow-list (`tests/protected_suite_respellings.yaml`), which
    F5.2's `--chains` step reads. F5.2 whole then passes, and its box closes
    at T089.
  - **Realizes**: 4.3 (consumer half), 9.2 (the ratchet), 9.5 (step 3, part);
    F5.2 (its three repairs, with T089).
  - **Falsifier**: `tests/test_dependency_direction.py`; F9.1 (openXdox-code,
    as amended by T007's batches B and F, and by batch J's `--deselect` unless
    T008 has removed it); and F5.2 whole, as T007's batches C, F, G and K
    amend it, with `tests/test_session_snapshot.py` green.
  - **Ruled**: R1Q1 (a), R1Q7 (a), R1Q22 (a), `5817152735`; R1Q10 (a), R1Q25
    (b), `5850003126`; F5.2's three repairs, `5962785556`, item 1.
  - **After**: T084, T087, T061 (the `pyproject.toml` pin's single-writer
    order), T059 (the ratchet's).
- [ ] T094 [US4] [oX] [oxF] **Phase 3's consumer pins and host wiring** (T090
  steps 5–6). openxFactory's PR carries whatever host wiring the retired
  columns need. That includes the parity test's MRO assertion and
  `test_serve_column_split.py`'s gate and projection rows, updated again once
  `consumer_reach.py` is gone. Both are named composition tests under R1Q2
  (a).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: as T047's.
  - **Ruled**: R1Q2 (a), `5817152735`.
  - **After**: T086, T087, T064 (the pin pairs' single-writer order).
- [ ] T098 [US4] [oxF] **Phase 3's interim F11.1**, by T093's procedure, with
  `ARC_TIP` at T094's landing. Record the output in
  `evidence/f11.1-phase3.txt`, with no `Arc:` trailer, and link it from
  this feature's README entry.
  - **Falsifier**: F11.1, as widened by T007 batch A, prints `requirement 1
    holds`.
  - **After**: T094.
- [ ] T089 **Phase 3 checkpoint.** Run and quote F4.1, F10.1 and F13.1 (both
  as batch H amends them), F16.1, and F5.2 whole (as T007's batches C, F, G and
  K amend it, after T086's repair), then T098's interim F11.1 output.
  - **Ruled**: F5.2's close here, `5962785556`, item 1.
  - **After**: T094, T098, T076 (so every phase-3 task but the PyPI publish is
    done).
  - The publish follows this checkpoint by design, at the cut
    (`5962754358`, `5963162921`).

---

## Every phase

- [ ] T090 [US4] [oD] [oXc] [oX] [oxF] **The pin procedure (9.5)**, run once
  per phase: T039 then T047 (phase 1), T062 then T064 (phase 2), T087 then T094
  (phase 3). The openDox-root step always precedes the consumer's. The order
  is:
  1. openDox-code lands.
  2. The openDox root moves its gitlink, `contracts/code-pin.yaml` and every
     workflow `@<sha>` in ONE commit (`make pins`).
  3. openXdox-code's `pyproject.toml` pin moves to the SAME openDox-code
     commit, and the ratchet is lowered.
  4. openXdox-code lands.
  5. The openXdox root moves its `code` gitlink and `code-pin.yaml`, and moves
     `contracts/opendox-pin.yaml` to step 2's root commit.
  6. openxFactory moves both pin pairs, one commit each, in ONE PR together
     with that phase's host wiring.

  Follow C4's runbook, `docs/openxdox-pin-resync-runbook.md` (landed as
  #1154). Phase 1's PR moved both pairs in ONE commit, which departs from
  step 6 (T047). Every one of these is an ancestor move. The one bundle release 1
  cuts is phase 2's `dox-v1.x` minor at the openDox root, which T053 cuts
  after its spec pin (R1Q11 (a), batch G's 9.5 addendum).
  - **Realizes**: 9.5, which is ticked at ARC close.
  - **Falsifier**: `make pins` in the openDox root (step 2) and in the openXdox
    root (step 5), and openxFactory's `scripts/verify-opendox-pin.py` and
    `scripts/verify-openxdox-pin.py` (step 6).
- [ ] T091 [oDc] [oXc] [oD] [oX] [oxF] [oDs] **The trailer (11.0).** Every
  realization commit and every landing carries `Arc:
  neutral-product-standalone-operability` as well as `Lane: openxfactory-4`.
  That holds in every repository the arc touches: the five, and openDox-spec
  (T053). No task touches openXdox-spec (R1Q12 (a)). 11.0's own words are
  *"in EVERY repository it touches"*. A merge landing writes the trailer into
  the merge message. Land by squash or merge, never rebase. Bookkeeping
  carries NO `Arc:` trailer: this feature's files, #1144's ticks, evidence
  notes and amendments (T007), and interim guard output (R1Q20 (a)). T066 is
  not an arc landing either, and carries none.
  - **How the landings are found, and the one that lost its line.** F5.2,
    F11.1 and 12.5's falsifier select the arc's landings with `git log
    --first-parent --grep='^Arc: neutral-product-standalone-operability$'`,
    which matches that line anywhere in the message, not only in git's parsed
    trailer block (measured with git 2.43). The holder's landing kit first
    built each squash message from the PR body with the `Lane:` and
    `Co-Authored-By:` lines after it, so in openDox-code #38, #39, #40, #41,
    #43, #46 and #47 the `Arc:` line sits in the body, and the grep finds all
    seven. openDox-code#37 (`e295b1a9`, T020) and #44 (`9d13bd16`, T021) carry
    no `Arc:` line at all: their PR bodies had none. The kit was fixed on
    2026-09-27, and it now falls back to the PR's commit trailers, so every
    later landing carries its `Arc:` line in the block `git interpret-trailers
    --parse` reads, as openDox-code#42 (`19370adc`, T016), the first landing
    after the fix, does. No `main` is rewritten.
  - 11.0's record at the arc's close lists each repository's landing set, as
    the grep finds it, cross-checked against the arc's merged PRs, and names
    openDox-code#37 and #44 as the two landings whose message lacks the line.
    No falsifier of #1144 reads openDox-code's landings, so none changes.
  - **Realizes**: 11.0, which is ticked at ARC close.
  - **Falsifier**: each PR's review, as for the `Lane:` line (11.0). F11.1
    finds the arc's landings by the trailer, and the falsifiers of 5.4a and
    12.5 assert that the set is non-empty in openXdox-code.
  - **Ruled**: R1Q20 (a).
- [ ] T092 [oxF] **11.1's notes.** One `edits[].note` per closed reach, added
  where an existing `edits[]` entry has none, or extended, and never rewritten.
  The note is the only field that changes: with every `edits[].note` removed,
  the manifest is unchanged, so no row, other field or digest moves. The
  manifest records the carve as it arrived, so an arc edit to a carved file
  needs nothing more (R1Q22 (a)). Each phase's notes ride in that phase's
  openxFactory PR (T047, T064, T094), for the reaches the phase closed.
  Phase 1's rode in T049's checkpoint PR instead, on the holder's decision of
  2026-09-28: six notes on five rows, for the ten reaches phase 1 closed. That
  PR carries no `Arc:` trailer, so F11.1's count of annotated notes never
  includes them. Their PR ran F11.1's content rule over them instead.
  Phase 2's rode in T063's checkpoint PR in the same way, on the holder's
  decision (b) recorded in T064's PR (openxFactory#1215): three notes on three
  rows (two added, one extended), for the eight reaches into openXdox that
  T055 closed (openDox-code#59 → `fa140875`). That PR ran the same content rule
  over them.
  - **Realizes**: 11.1, which is ticked at ARC close.
  - **Falsifier**: F11.1's manifest check. With every `edits[].note` removed,
    the two documents must be equal, and a note that already existed may only
    be extended. Each interim run (T018, T065, T098) applies it.
  - **Ruled**: R1Q22 (a).
- [ ] T093 [oxF] **The interim F11.1 procedure, and F11.1 at the arc's
  close.** Run F11.1 with `PACKET_MERGE=94b6f7f1` and `ARC_TIP` set to the last
  arc landing measured. Use the guard as widened by T007 batch A (R1Q2 (a)'s
  named composition tests). Record the output in this feature's `evidence/`,
  with no `Arc:` trailer. It runs once per phase, as T018 (phase 1), T065
  (phase 2) and T098 (phase 3), each with its own `After:` line. It runs once
  more at the arc's close, after release 2, where the box is ticked.
  - **Realizes**: F11.1, which is ticked at ARC close.
  - **Falsifier**: F11.1 itself, which must print `requirement 1 holds`.
  - **Ruled**: R1Q2 (a), R1Q20 (a).

---

## Acceptance: AT-R1

- [ ] T095 [US3] [oDc] **AT-R1, the HTTP half, in CI.** An acceptance harness,
  `acceptance/at_r1_http.py`, run by its own `acceptance` job in openDox-code's
  `validate.yml`.
  - That job has NO database service, because the harness asserts a clean
    machine. The `validate` job's PostgreSQL service (T036) would break that
    precondition.
  - The harness is not a pytest module, and it sits outside `tests/` and
    `tests_runtime/`. Like the browser half (T096), it installs the product and
    drives it from outside. So the harness changes neither `testpaths`, which
    T036 sets in phase 1, nor F9.1, and FR-006's "no exclusion" for
    openDox-code still holds.
  - Making `acceptance` a required check is a ruleset change for the
    repository's owner.

  It does the following:
  - installs openDox alone into a fresh venv, as `opendox[local]` (R1Q16
    (iii));
  - ASSERTS that the four siblings, `omp`, an identity broker, a database and
    a binding are all absent, in a fresh `OPENDOX_STATE_DIR`;
  - copies both plain repositories into fresh `git init`s (spec.md AT-R1
    step 3), and gives each a git identity (`git config user.name` and
    `user.email`), which the served actor is read from;
  - runs the documented command, `opendox generate-and-open --local …`
    (R1Q15 (b)), on loopback;
  - fetches `/` (it must be HTML), `/snapshot.json` (non-empty, neutral per
    F5.3) and `/capabilities` (`install.mode == local`);
  - fetches the model-catalog route, presenting `/capabilities`'
    `console_token` in `X-XF-Console-Token`, and it must answer with no
    available entry;
  - fetches every route the wheel, the lens and the chat rail request on load,
    none of which may answer 5xx;
  - stops the server, and asserts that no bundled PostgreSQL process is left
    running (R1Q16 (iv)).
  - **Realizes**: FR-011 (HTTP half).
  - **Falsifier**: the harness itself, which exits non-zero on the first failed
    assertion.
  - **Ruled**: R1Q10 (a), R1Q12 (a) (the catalog's validators, T085), R1Q15
    (b), R1Q16 (iii) and (iv), `5850003126`.
  - **After**: T089, T076 (the root README's one documented command, which the
    harness runs).
- [ ] T096 [US3] [oxF] **AT-R1, the browser half, on the host.** Drive the
  same install with Playwright (quickstart.md § 4, against the server § 3
  starts). The verdict comes from
  openDox-code's `tests/smoke_signals.py` oracle:
  - the wheel renders the fixture's tiles;
  - the lens renders the radar with the documents as dots, and offers neither
    seed action (R1Q19 (a));
  - opening the workbench from a grouping tile shows the chat rail's "no model
    configured" state, with how to configure one, before any turn;
  - a turn is refused `model_capability_unavailable`, and both editors stay
    usable;
  - there is zero `pageerror`, and nothing undeclared.

  Record the evidence in openxFactory, in this feature's `evidence/at-r1/`, with
  no `Arc:` trailer, and link it from this feature's README entry: this run's oracle
  verdict, and the URL and verdict of T095's `acceptance` job at the same
  openDox-code commit. Together they are SC-004's
  evidence for both halves.
  - **Realizes**: FR-011 (browser half).
  - **Falsifier**: the oracle's verdict, which must pass: zero `pageerror`, and
    nothing undeclared.
  - **Ruled**: R1Q20 (a), `5817152735`; R1Q13 (a) with (c), R1Q19 (a),
    `5850003126`.
  - **After**: T095.
- [ ] T097 [oxF] **Bookkeeping.**
  - Tick #1144's release-1 boxes, each with its evidence note: the 62 in the
    table below. 3.0 is already ticked (#1151).
  - Leave 9.5, 11.0, 11.1 and F11.1 open for the arc's close, and F9.2 open
    until T008 (RULED `5859927858`; holder decision, 2026-09-29, at T049).
  - The PR touches `openspec/changes/`, so it lands under a Rule 6
    `LANDING`/`LANDED` window. It carries no `Arc:` trailer (R1Q20 (a)) and no
    closing keyword.
  - Record the non-normative corrections from research R16 in the evidence
    notes.
  - **Ruled**: R1Q20 (a).
  - **After**: T096, T099 (10.3 closes on the publish), T007 (every batch).

---

## Box accounting (#1144 `tasks.md`: 124 boxes)

`python3 "$W/tools/box_census.py" openspec/changes/add-neutral-product-standalone-operability/tasks.md`,
run from an openxFactory checkout (research.md § Appendix writes the tool),
printed `total 124`: 104 `[ ]`, 11 `[x]` and 9 `[~]`
at `cd494e4c`. At `dd2466ad` the counts were 106, 9 and 9, before #1151 ticked
1.8 and 3.0.

| scope | groups | boxes |
|---|---|---|
| **release 1 (this feature)** | 2, 3, 4, 5, 7, 9, 10, 11, 13, 16 | **69** |
| release 2 (its own Speckit feature, R1Q21 (a)) | 6 (4), 12 (11), 14 (10), 15 (12) | 37 |
| outside both releases | 1 (9, all `[x]` since #1151), 8 (5 `[~]`), F1–F4 (4 `[~]`) | 18 |
| **total** | | **124** |

Release 1's 69 boxes, by class:

| class | count | boxes |
|---|---|---|
| closed by a realization task in release 1 | 62 | every other box below |
| closes after T008, outside release 1's tasks | 1 | F9.2: RULED `5859927858` keeps it unchanged and red on the 31-entry help-tree test until T008 (holder decision, 2026-09-29, at T049) |
| discharged by the ratification | 1 | 3.0 (ticked by #1151, T001) |
| already `[x]` | 1 | 5.6 (openDox-code#35 → `3c3a9e31`) |
| performed in every phase, ticked at ARC close | 4 | 9.5 (T090), 11.0 (T091), 11.1 (T092), F11.1 (T093) |
| **total** | **69** | |

Every release-1 box, with the task that closes it:

| group | box → task |
|---|---|
| 2 (8) | 2.1 → T011 · 2.1a → T011 · 2.2 → T010, T011, T045 · 2.3 → T032 · 2.4 → T030 · 2.5 → T036 · 2.6 → T031 · F2.1 → T049 |
| 3 (5) | 3.0 → T001 · 3.1 → T015 · 3.2 → T016 · 3.3 → T017 · F3.1 → T049 |
| 4 (5) | 4.1 → T020, T021, T046 · 4.1a → T022 · 4.2 → T020 · 4.3 → T012, T021, T025–T027, T046, T055, T084–T086 · F4.1 → T089 |
| 5 (12) | 5.0 → T050 · 5.1 → T053, T054, T056 · 5.2 → T054 · 5.3 → T054 · 5.3a → T060 · F5.1 → T060 · 5.4 → T052 · 5.4a → T059 · F5.2 → T086, T089 (T063 quotes it red; RULED `5962785556` moves its close to phase 3) · 5.5 → T055 · 5.6 `[x]` · F5.3 → T063 |
| 7 (8) | 7.0 → T051 · 7.1 → T053, T057 · 7.1b → T057 · 7.1a → T057 · 7.2 → T057, T058 · 7.3 → T061 · F7.1 → T061 · F7.2 → T058, T063 |
| 9 (8) | 9.1 → T034–T036 · 9.2 → T040, T041, T043, T086 · 9.2a → T030, T036 · 9.3 → T035, T042 · 9.4 → T037, T044 · 9.5 → T039, T040, T047, T059, T062, T064, T086, T087, T094 (T090's steps; arc close) · F9.1 → T049 · F9.2 → after T008 (T049 quotes it red, as RULED `5859927858` keeps it) |
| 10 (5) | 10.1 → T038 · 10.2 → T075 · 10.2a → T075 · 10.3 → T076, T101, T099 · F10.1 → T077 |
| 11 (3) | 11.0 → T091 · 11.1 → T045, T092 · F11.1 → T093 (all at arc close) |
| 13 (8) | 13.1 → T072 · 13.2 → T071 · 13.3 → T071 · 13.4 → T070 · 13.4a → T073 · 13.5 → T070 · 13.6 → T070 · F13.1 → T074 |
| 16 (7) | 16.1 → T078 · 16.2 → T079 · 16.3 → T080 · 16.4 → T081, T085 · 16.5 → T082 · 16.6 → T034, T083 · F16.1 → T083 |

8 + 5 + 5 + 12 + 8 + 8 + 5 + 3 + 8 + 7 = **69**.

## Dependencies and execution order

- **Phase 0** gates phase 1. T003, T004 and T005 came before T006, and T006's
  round-1a analyze came before every phase-1 task. T019, T009 and T069 came
  after it, in this revision. All of them are done. T007's batches land
  before the landings and checkpoints that need them: batch A before T047,
  both A and B before T049, C before T059, T061 and T043, D before T049, E
  before T047, F before T043 and T061, G before T053, H before T070, T075 and
  T080, I before T059, T060, T061 and T063, J before T049, whose F9.1
  run needs J's `--deselect`, K before T061, T063 and T080 (and
  openDox-code#64, which is no task of this plan), and L before T084. T016 may land before batch A, T041 and T043
  before batch B, and T043 before batch J, each quoting its falsifier as the
  answer records it (T007).
- **The round tasks.** T019 encoded phase 1's openXdox-code tail, T009 phase
  2 and T069 phase 3, each on `5850003126`, and one analyze ran over the
  result (`evidence/analyze-round-2.md`). That analyze raised R1Q26 and R1Q27,
  and T067, the third round, encoded their answers (`5851950767`), with an
  analyze of its own (`evidence/analyze-round-3.md`).
- **Phase 1**: lanes A–E run in parallel, subject to plan.md's single-writer
  table (`serve.py`, `cli.py`, `workbench.py`, `pyproject.toml`,
  `tests/test_authoring_seam.py`, `tests/test_consumer_reach.py` and
  openDox-code's `validate.yml` in phase 1). They join at T032 and then run
  T034 → T035 → T036 → T037. T031 co-lands in T036's PR. T039 then pins
  openDox's phase-1 commit in the openDox root, after T022, T032, T037 and
  T038. openXdox-code follows: T040 → T041 → T042 → T043 → T044, with
  T007's batches C and F before T043. T047 moves the consumer pins after T039,
  T044 and T007's batches A and E, and openxFactory's host wiring (T045,
  T046) lands inside T047's openxFactory PR. T017 and T018 run after T047.
  T049 closes the phase after T007's batches A, B, D, F and J.
- **Phase 2**: T053 and T050 first, in parallel: T053 after T049, T009 and
  T007's batch G, and T050 after T049 and T009. Then T051, after both, and
  T053 → T052 and T053 → T057, in parallel. Then T054 → T055 → T056 → T058,
  with T055 also after T057. T062 (the phase-2 openDox root pin) follows
  T054–T058, and T060 follows T054 and T007's batch I. openXdox-code runs
  T059 → T061 (T059 after T052, T055, T060, T062 and T007's batches C and I;
  T061 after T007's batches C, F, I and K). Then T061 → T066 → T064, and T064 →
  T065 → T063.
- **Phase 3**: T069 is done. Group 13 runs T071 → T070 → T072 → T073 → T074,
  with T084 after T073 for `serve.py`. In parallel: Group 16's binding slice
  (T078 → T079 → T080), T085 → T081, and T088. T075 and T077 run F10.1 as
  batch H amends it, so both follow T072: T072 → T075 → T077. Then T082,
  which comes after T081, T084 and T085, and T083. Then T087 (the phase-3
  openDox root pin) → T086 → T094 → T098 → T089, and T087 → T076 → T089.
  The PyPI publish comes last. T101, T099's release step (the release
  workflow, and then the bump to 0.1.0), lands after every other phase-3
  openDox-code landing that changes the shipped package, and T087 pins it:
  T101 → T087. The publish follows the checkpoint, at the cut: T089 → T099.
- **Acceptance**: T095 (after T089 and T076) → T096 → T097, and T099 → T097.

### Parallel slices, summarised

| phase | runs in parallel | is serialized |
|---|---|---|
| 1 | T010–T012 ∥ T015–T016 ∥ T020–T022 ∥ T025–T027 ∥ T030 | `serve.py` and `cli.py` writers; `pyproject.toml` (T038 → T036); `tests/test_authoring_seam.py` (T020 → T021 → T022); openDox-code's `validate.yml` (T036 → T037); T020 → T025 and T026 → T025; T032 → T037; T039 (root pin) → openXdox (T040, then T041 → T042 → T043 → T044) → T047 → T017, T018 |
| 2 | T053 ∥ T050, then T052 ∥ T057 ∥ T051 | T053 → T054 → T055 → T056 → T058; T062 → T059 → T061 → T066 → T064; openXdox-code `pyproject.toml` (T059 → T061); ratchet writers; T007 batch I before T059, T060 and T061; batch K before T061 |
| 3 | Group 13 ∥ 16.1–16.3 ∥ T085 → 16.4 (T081) ∥ T088, then T075 → T077 after T072 | `serve.py` and `cli.py` (T070, T072 and T073 before T084); openDox-code `pyproject.toml` (T072 → T075 → T101); `doxbench_binding.py` (T078 → T080); T085 → T081; T087 → T086 → T094; T101 → T087; T089 → T099 (the publish, at the cut) |

## Phase 1 writer slices (for the fan-out)

Each slice is one writer and one claim (T002) in one repository. Its tasks land
in their `After:` order, one PR each unless a `Lands with:` line joins them, and
each PR quotes its task's falsifier. "Opus" marks a slice that designs a seam or
makes a judgement the packet does not settle. "Sonnet" marks a slice that is
fully specified. T006's round-1a analyze is done. Every question the slices
need is answered (`5817152735`, `5850003126`), so a slice waits only on its
claim and the slices in its "depends on" column. The **group** column is the
parallel group: slices in one
group run at the same time, and a group starts once the one before it has
landed, except where a row says otherwise.

The task headings' lanes A–E are not these slices. Lane A is P1-A. Lane B is
P1-B, less T017, which is P1-L's. Lane C is P1-C and P1-D. Lane D, the other
openxFactory reaches, is P1-E. Lane E rides in P1-A (T030) and P1-G (T031).

| slice | group | tasks | repo | files | depends on | falsifier it must pass | size |
|---|---|---|---|---|---|---|---|
| P1-A route seam | G1 | T010, T011 (with T030), T012 | oDc | `src/route_extension.py`; `src/opendox/serve.py`; readers of the five lane names; new `tests/test_route_handler_contribution.py` and `tests/test_imports_standalone.py`; `tests/test_consumer_reach.py` (T011 moves two modules into `NEUTRAL_MODULES`) | T006 | F2.1 (sweep and named test); the new seam tests | Opus |
| P1-B default profile | G1 | T015, T016 | oDc | `src/opendox/domain_profile.py`, `profile_proxy.py`, a new default-profile module; one-line entry calls in `cli.py`/`serve.py`; `tests/test_profile_registration.py` and a vocabulary test | T006; T016 lands after P1-A (T012 is its last `serve.py` edit) | the vocabulary test and the `RuntimeSubcommand` test (T015); F3.1 with line 2 as amended (T007 batch A), and `tests/test_profile_registration.py` (T016) | Opus |
| P1-C home-corpus seam | G1 | T020 | oDc | `src/opendox/corpus_adapter.py`; `tests/test_authoring_seam.py` (new) | T006 (it never needed an answer) | the seam tests: with nothing registered, `home()` refuses `ADAPTER_NOT_REGISTERED`, naming the seam and `register_home(...)`; a registered factory is what `home()` returns | Sonnet |
| P1-E openxFactory reaches | G1; T025 after P1-C | T026, T027, then T025 | oDc | `src/opendox/workbench.py`, `serve_wire.py`, `doxbench_packet.py`, with seam tests | T006; P1-C for T025 | F4.1's scan without `workbench.py:746/1407-1409`, `serve_wire.py:1369` or `doxbench_packet.py:177`; a session-notebook membership test | Opus |
| P1-D authoring and the default adapter | G2 | T021, T022 | oDc | `src/opendox/authoring.py`; entry registration in `cli.py`/`serve.py`; `tests/test_authoring_seam.py` | P1-C, P1-B | F4.1's first block; `…::test_required_header_fields_come_from_the_registered_adapter` (T021); `…::test_an_entry_point_registers_the_local_git_corpus_when_no_host_has` (T022) | Sonnet |
| P1-H console script | G2; rebases onto P1-D for `cli.py` | T038 | oDc | `pyproject.toml` `[project.scripts]`; `cli.py`; two comments in `src/opendox/runtime/cli.py` | P1-B; P1-D for `cli.py` | `opendox --help` and `opendox runtime --help` exit 0 | Sonnet |
| P1-F sweep and nine-file repair | G3; it need not wait for P1-H | T032, T034 | oDc | the nine files in research R3 and their Node harnesses | P1-A–P1-E landed | the nine files green; F4.1's scan lists only `openxdox` targets | Opus (the `test_consumer_reach`/`test_boundary` re-pins alone would be Sonnet) |
| P1-G whole suite in CI | G3, after P1-F | T035, T036, T037, T031 | oDc | `conftest.py`; `pyproject.toml` (`testpaths`); `.github/workflows/validate.yml` (a PostgreSQL service and the `.[runtime,test]` install in `validate`); `README.md`; the seven ignored modules | P1-F; P1-H, since both edit `pyproject.toml` | `python -m pytest -q tests/` (T035); F9.1 (openDox-code), both assertions, with the database DSN exported (T036) | Opus |
| P1-R openDox root pin | G4 | T039 | oD | the `code` gitlink, `contracts/code-pin.yaml` and every workflow `@sha`, in ONE commit | every phase-1 openDox-code slice landed (T022, T032, T037, T038) | `make pins` | Sonnet |
| P1-I openXdox pin and residue | G5 | T040 | oXc | `pyproject.toml` (the `opendox @` pin, `rfc3339-validator`); local helpers for the importers of `test_gate_routes`, `test_doxbench_routes` and `test_doxbench_model`; `tests/fixtures/base-repo` and `tests/fixtures/fake_omp_child.py`; the source paths in `test_doxbench_packet.py`, `test_scope_column_split.py`, `test_doxbench_blank_reason.py` and `test_doxbench_bridge.py` (T005's classes B–G) | P1-R | no collection error on the three helpers; no source path under `scripts/ideation_dashboard/`; `test_register` and `test_snapshot_validation_launch` find their fixture, and the bridge suite its child | Opus (T005 found the residue layered: what shows behind it depends on the pin) |
| P1-J openXdox green alone, less the declared exclusion | G5, after P1-I | T041, T042, T043, T044 | oXc | the declared exclusion file, with its four reasons, and `conftest.py`; `tests/integration/` (new, with `test_assembled_surface.py` and P1-G's relocated modules); `.github/workflows/validate.yml`; the residue T043 finds at T040's pin | P1-I, P1-G; T007 batches C and F for T043; T007 batch B lands once T041 names its file | the exclusion test and batch B's three exclusion assertions (T041); F9.2 (T042, quoted red until T008); F9.1 (openXdox-code, as amended by batches B, F and J) (T043) | Opus |
| P1-K pins and host wiring | G6 | T045, T046, T047 | oX, oxF | openXdox root: `code`, `contracts/code-pin.yaml`, `contracts/opendox-pin.yaml`. openxFactory: both pin pairs, plus `scripts/opendox_host.py`, `scripts/profile_openxfactory.py`, `tests/domain_profile/`, `tests/ideation-dashboard/test_extension_point_parity.py` and `tests/ideation-dashboard/test_serve_column_split.py` (and, as named composition tests, `test_session_harness.py` or `test_outline_model.py`'s `doc_health` case if T035 or T034 moves one here). openxFactory's readers of openXdox's validator need nothing here, because T061 lands in phase 2 and T066 takes their change | P1-R, P1-J; T007 batches A and E (F11.1 names the composition tests) | `make pins` in the openXdox root; `verify-opendox-pin.py`, `verify-openxdox-pin.py`; openxFactory `pytest-suite` | Opus |
| P1-L read-only checks | G6, after P1-K | T017, T018 | oxF | `evidence/` only | P1-K | interim F11.1 (T018, by T093's procedure), as widened by batch A, prints `requirement 1 holds` | Sonnet |
| checkpoint | G6, last | T049 | — | none (a verifier) | P1-K, P1-L; T007 batches A, B, D, F and J | F2.1; F3.1 as amended; F9.1 in both legs; F9.2; `opendox --help`; F4.1's scan | Opus (verifier) |

**Fan-out order.** Before any slice: T006's round-1a analyze, and the slice's
claim (T002).

1. **G1**: P1-A, P1-B, P1-C and P1-E in parallel. P1-B's T016 lands after
   P1-A, because both write `serve.py`, and P1-E's T025 waits for P1-C.
2. **G2**: P1-D and P1-H in parallel. P1-H rebases onto P1-D for `cli.py`.
3. **G3**: P1-F, then P1-G.
4. **G4**: P1-R, the openDox root pin.
5. **G5**: P1-I, then P1-J.
6. **G6**: P1-K, then P1-L, then T049.

P1-K's host wiring (T045, T046) could be authored once P1-A and P1-C–P1-E had
landed, and it landed inside T047's PR. The holder worked beside the slices
on T007's batches A to J, all of which have landed, and on T008, which was
raised (#1173) and whose arc is open.

## Phase 2 writer slices (for the fan-out)

The rules are phase 1's: one writer and one claim (T002) per slice, landing in
`After:` order, each PR quoting its task's falsifier. Every phase-2 slice
starts after T049 and T009, and T007's batch G lands before P2-S opens.
Batch I lands before P2-X, P2-K and P2-C, and batch K before P2-C.

| slice | group | tasks | repo | files | depends on | falsifier it must pass | size |
|---|---|---|---|---|---|---|---|
| P2-S neutral snapshot contract | G1 | T053 | oDs, oD | openDox-spec: the new schema and its fixtures. openDox root: the spec pin, then the `dox-v1.x` bundle | T049, T009; T007 batch G | the root's `make validate`; openDox-spec's `validate` | Opus (a new contract, whose sections are what T054 writes) |
| P2-F fixtures | G1 (T050); T051 after P2-S | T050, T051 | oDc | `tests/fixtures/plain-documents/` and its vocabulary test; `tests/fixtures/malformed/` with `EXPECTED_RULE` | T049, T009; P2-S for T051 | the vocabulary test (T050); the one violation, named by `EXPECTED_RULE` (T051) | Sonnet |
| P2-G generator seam | G2 | T052 | oDc | the generator seam, beside `domain_profile.register()`, and its seam tests; the entry points' one-line registration calls in `src/opendox/cli.py` and `src/opendox/serve.py` (single-writer, after T038) | P2-S | the seam tests | Opus |
| P2-V validator input set | G2 | T057 | oDc | the validator, the four packaged schemas and their digest test; openDox-code's `pyproject.toml` (package data) | P2-S | the packaged-copy digest test; the 7.1b test | Opus |
| P2-P neutral projection | G3 | T054 | oDc | the projection's new modules; `src/opendox/display_profile.py` (`SNAPSHOT_VALUES`' defaults, batch G's 5.3); the default adapter's field set | P2-F (T050), P2-G, P2-S | the in-process projection test, the topic-rule test and the `stage:` test (F5.3 runs at T056) | Opus |
| P2-X openXdox's facet | G4 | T060 | oXc | `src/openxdox/view_extensions.py` (the `values` block); `tests/test_gate_loop_views.py`'s facet-declaration test, one edit entered in the reviewed allow-list (R1Q26 (a)) | P2-P; T007 batch I | F5.1, the `values` test, and `tests/test_gate_loop_views.py` green | Sonnet |
| P2-R serve and generate standalone | G4 | T055, T056, T058 | oDc | `src/opendox/serve.py`, `src/opendox/cli.py`, `src/opendox/branch_session.py`, `src/opendox/workbench.py` and `src/opendox/serve_workbench.py` (T055); the seams' default modules | P2-P, P2-V, P2-F (T051, for T058) | F4.1's scan, down by these reaches (T055); F5.3, F10.1's `generate-and-open` with a plain install and no `--local`, and the verb's `stage:` test (T056); F7.2 (T058) | Opus |
| P2-D openDox root pin | G5 | T062 | oD | the `code` gitlink, `contracts/code-pin.yaml` and every workflow `@sha`, in ONE commit | every phase-2 openDox-code slice landed (T054–T058) | `make pins` | Sonnet |
| P2-K openXdox contributes | G6 | T059 | oXc | the contributions through the seams; `pyproject.toml` (the `opendox @` pin); `tests/test_dependency_direction.py` (the ratchet); `tests/test_gate_loop_views.py`'s overlay test, one edit entered in the reviewed allow-list (R1Q26 (a)) | P2-D, P2-X; T007 batches C and I | seam tests, and 5.4a's suites in F5.2's environment, all but `tests/test_snapshot.py`'s two schema cases | Opus |
| P2-C the consumer's validator (7.3) | G7 | T061 | oXc | `src/openxdox/snapshot.py`; `scripts/validate-ideation-dashboard-contracts.py`; the package data and `pyproject.toml`; `tests/test_snapshot.py` and `tests/test_snapshot_validator_home.py` (protected, admitted by batch F; `tests/test_snapshot.py`'s tenth case by batch K); `tests/test_snapshot_validation_launch.py` (protected, nine cases admitted by batch K); `scripts/protected_suites.py` (F5.2's `--chains`); `tests/test_validate_ideation_dashboard_contracts.py`; `tests/test_validator_schema_home.py`; the exclusion file (`tests/test_snapshot.py`'s entry leaves) | P2-K; T007 batches C, F, I and K | F7.1, with both of its named tests; F5.2 whole | Opus |
| P2-H openxFactory at both pins (non-arc) | G8 | T066 | oxF | `tests/ideation-dashboard/test_dashboard_source_seal.py`; `scripts/profile_openxfactory.py` and `tests/test_engineering_profile_display_facet.py` (R1Q26 (a)); whatever the candidate pins' runs name | P2-C, P2-D | openxFactory's `pytest-suite`, and the consumer gate's suite at its floors, at the current pins and at T064's candidate pins | Opus |
| P2-L consumer pins | G9 | T064 | oX, oxF | openXdox root: `code`, `contracts/code-pin.yaml`, `contracts/opendox-pin.yaml`. openxFactory: both pin pairs | P2-H, P2-K, P2-C, P2-X, P2-D | `make pins` in the openXdox root; `verify-opendox-pin.py`, `verify-openxdox-pin.py`; `pytest-suite`, and the consumer gate's suite at its floors (`MIN_PASSED` 1137, `EXPECT_SKIPPED` 0) | Sonnet |
| P2-M read-only checks | G9, after P2-L | T065 | oxF | `evidence/` only | P2-L | interim F11.1 prints `requirement 1 holds` | Sonnet |
| checkpoint | G9, last | T063 | — | none (a verifier) | P2-L, P2-M; T007 batches C, F, G, I and K | F5.1, F5.2 (quoted red, as RULED `5962785556`), F5.3, F7.1, F7.2; a standalone `generate-and-open` | Opus (verifier) |

## Phase 3 writer slices (for the fan-out)

Every phase-3 slice starts after T063 and T069, and T007's batch H lands
before P3-I's T070, P3-E's T075 and P3-B's T080. Batch K also lands before
P3-B's T080, and batch L before P3-R's T084.

| slice | group | tasks | repo | files | depends on | falsifier it must pass | size |
|---|---|---|---|---|---|---|---|
| P3-I install mode and the bundle | G1 | T071, T070, T072, T073 | oDc | `src/opendox/runtime/config.py`; `src/opendox/cli.py` (`--local`); the bundle module; `src/opendox/serve.py` (the child, and the `install` block); openDox-code's `pyproject.toml` (the `local` extra, which the `test` extra joins) | T063, T069; T007 batch H for T070 | F13.1's `load_settings` block (T071), its refusals (T070), its TCP-listener and `runtime status` blocks (T072), its `caps.json` block (T073) | Opus |
| P3-J F13.1 | G2, after P3-I | T074 | oDc | none (a run) | P3-I | F13.1, as batch H amends it | Sonnet |
| P3-B binding and provider | G1 | T078, T079, T080 | oDc | `src/opendox/doxbench_binding.py`; `src/opendox/doxbench_provider.py` (the dialect arm, and the resolver); `src/opendox/cli_model_binding.py` (`--model`) | T063, T069; T007 batches H and K for T080 | F16.1's dialect, field and refusal assertions; the resolver's and `none`'s tests | Opus |
| P3-D doxBench defaults and the no-model state | G1 (T085); T081 after it | T085, T081 | oDc | the default registrations for T027's seams; `src/opendox/doxbench_install.py`; `src/opendox/web/views/doxbench-chat.js`; `tests/test_chat_model_configuration.py` (new); `src/opendox/validator.py`, `src/opendox/default_projection.py` and `tests/test_post_render_validator.py` (T058's two workbench-manifest rules and their assertions, T085) | T063, T069 | the served catalog route answers with no available entry, and the two rules report as `pinned-keywords-are-checked` and `new-candidates-are-disjoint` (T085); F16.1's catalog block and the named test (T081) | Opus |
| P3-L lens seed actions | G1 | T088 | oDc | `src/opendox/web/views/lens.js`, and the capability that says a binding answers | T063, T069 | AT-R1 step 6 | Sonnet |
| P3-E the door | G2, after P3-I | T075, T077 | oDc | none, unless T075's run finds a gap in how the bundle is served. An edit to the server module then joins its single-writer order between T073 and T084 before the PR opens | P3-I (T072); T007 batch H | F10.1's fetch, as batch H amends it (T075); F10.1, as batch H amends it (T077) | Sonnet |
| P3-R 4.3's last reaches | G2, after P3-I | T084 | oDc | `src/opendox/serve.py`, `src/opendox/cli.py`, `src/opendox/serve_workbench.py`, `src/opendox/serve_project.py` and `src/opendox/branch_session.py`; the defaults' modules; `src/opendox/consumer_reach.py` (deleted); `tests/test_capability_honesty.py` (new, the capability and crash-site assertions); `tests/test_rejection_report.py` (new, the grouped rejection output) | P3-I; T007 batch L | F4.1 whole; the capability-honesty test, over a standalone child and a composed host; the rejection-output test | Opus |
| P3-N no model, everywhere | G3 | T082, T083 | oDc | `tests/test_chat_model_configuration.py`; `tests/test_provider_boundary.py` | P3-D, P3-R, P3-B | the named test (T082); `tests/test_provider_boundary.py`, then F16.1 whole (T083) | Sonnet |
| P3-P openDox root pin | G4 | T087 | oD | the `code` gitlink, `contracts/code-pin.yaml` and every workflow `@sha`, in ONE commit | every phase-3 openDox-code slice landed | `make pins` | Sonnet |
| P3-O the root README | G5 | T076 | oD | `README.md` | P3-P, P3-J, P3-E | review; AT-R1 step 4 follows it | Sonnet |
| P3-X openXdox's columns | G5 | T086 | oXc | the gate and projection contributions; `pyproject.toml` (the `opendox @` pin); `tests/test_dependency_direction.py` (the ratchet at `(0, 0)`); `tests/test_session_snapshot.py` and `tests/protected_suite_respellings.yaml` (F5.2's three repairs, RULED `5962785556`) | P3-P, P3-R; P2-C | `tests/test_dependency_direction.py`; F9.1 as batches B and F amend it, and batch J's `--deselect` unless T008 has removed it; F5.2 whole | Opus |
| P3-K pins and host wiring | G6 | T094 | oX, oxF | as P1-K's pin files; `tests/ideation-dashboard/test_extension_point_parity.py` and `tests/ideation-dashboard/test_serve_column_split.py` (named composition tests) | P3-X, P3-P | as T047's | Opus |
| P3-M read-only checks | G6, after P3-K | T098 | oxF | `evidence/` only | P3-K | interim F11.1 prints `requirement 1 holds` | Sonnet |
| checkpoint | G6, last | T089 | — | none (a verifier) | P3-K, P3-M, P3-O | F4.1, F5.2, F10.1, F13.1, F16.1 | Opus (verifier) |
| acceptance | after T089 | T095, T096 | oDc, oxF | `acceptance/at_r1_http.py` and its `acceptance` job; `evidence/at-r1/` | the checkpoint, P3-O | the harness; the oracle's verdict | Opus |
| P3-W publish to PyPI | T101 last among the package-changing openDox-code landings, before P3-P; T099 after the checkpoint, at the cut | T101, T099 | oDc | `.github/workflows/release.yml`, `.github/release-tools-cpython312-linux.txt` and `tests/test_release_workflow.py` (new); `pyproject.toml` (`readme`, after T072 and T075; then the version bump to 0.1.0, its own PR and the last of T101's landings) | every package-changing phase-3 openDox-code slice (T101); P3-P and the checkpoint (T099) | `tests/test_release_workflow.py` (T101); the release workflow's verify job, a TestPyPI dry run installed in a fresh venv, and the PyPI publish at the cut (T099) | Opus |
| bookkeeping | last | T097 | oxF | #1144's `tasks.md` ticks, under a Rule 6 window | the acceptance, P3-W; T007 every batch | none (a record) | Sonnet |

## Ruled amendments (`5817152735`, `5850003126`, `5851950767`, `5870594693`, `5916000030`, `5920216845`)

Brett Heap's answers amend #1144's falsifiers, task lines, addenda and one
design note. Batches A, B and C carry `5817152735`'s answers, and batches F,
G and H carry `5850003126`'s, batch I carries `5851950767`'s, batch J
carries `5870594693`'s, batch K carries `5916000030`'s, and batch L
carries `5920216845`'s. They amend
no requirement and no scenario, except that batch K's first row adds a
dated note to requirement 17 on its own ruling and rewrites none of its
text. T007 records each amendment in #1144's `tasks.md` (and the D4
addendum in `design.md`, and batch K's note in the spec delta) as
bookkeeping, and the realization tasks beside it carry it out.
The one scenario text an answer touches is not listed here. It is RN-1
(plan.md § "Ruling needed"), ruled (a) in `5850003126`. T007's batch D
landed it in #1144's spec delta, as #1170 → `79a720a2`.

| batch | #1144 line | the amendment | from | carried out by |
|---|---|---|---|---|
| A | F3.1, line 2 | The line asks after `build_parser()`: `python -c "from opendox.cli import build_parser; from opendox import domain_profile as d; build_parser(); print('OK', d.name_of(d.current()))"`. The prose under it adds that a bare process that builds nothing still meets `ProfileNotRegistered`, which `tests/test_profile_registration.py` asserts. | R1Q3 (a) | T016, T049 |
| A | 3.2 | "fall back to it" becomes "register it", because the default is a registration the entry point makes. The refusal `profile_proxy.py` keeps is the one it was written for, NOTHING REGISTERED (`profile_proxy.py:42-46`). It is not "an ambiguous registration": that case is `AlreadyRegistered`. A host registration made before a build replaces the default. (ii)'s after-build refusal joins 3.2 only with RN-1. | R1Q3 (a), (i), (ii) | T016 |
| A | 2.2; `design.md` § D4 | An addendum. The routes still travel through the `RouteBinding` seam. The methods they name travel through a handler-contribution facet that openDox declares, which D4's "no new mechanism" did not foresee. openxFactory's half gains the `LaneRoutes` declaration. | R1Q1 (a) | T010, T011, T045 |
| A | 4.3 | Of `workbench.py`'s four reaches, only three (`:1407-1409`) are the ones `run_scoped_doc_health` makes. The fourth, `session_documents` (`:746`), resolves through the registered adapter's `list_documents` in phase 1, and the hosted membership rule is unchanged. | R1Q9 (a) | T025, T026, T046 |
| A | 10.1 | An addendum. Q-R4's condition is discharged through the default profile's `SUBCOMMAND_EXTENSIONS` (`RuntimeSubcommand`). `opendox-runtime` stays as an alias, and a host's own profile keeps the 31-entry tree. | R1Q5 (a) | T038, T042 |
| A | 11.0 | An addendum. Bookkeeping is not an arc landing and carries no `Arc:` trailer: the Speckit feature files, #1144's ticks, evidence notes and amendments, and interim guard output. | R1Q20 (a) | T091 |
| A | 11.1; F11.1 | A fourth declared surface: NAMED openxFactory composition tests, which may be edited or added and are never removed. The guard gains `COMPOSITION_TESTS = {"tests/ideation-dashboard/test_extension_point_parity.py", "tests/ideation-dashboard/test_serve_column_split.py"}` beside `HOST`. Batch E adds a path before the landing that adds it (T034, T035), or that T047's `pytest-suite` run finds. Also an addendum to 11.1: the manifest records the carve as it arrived, so an arc edit to a carved file needs no declared-edit act. | R1Q2 (a); R1Q22 (a) | T045, T093, T094 |
| B | F9.1 (openXdox-code) | `python -m pytest -q` collects the whole suite less the files in T041's declared exclusion file. The falsifier asserts three things: the file's count equals its entries, every entry carries its reason, and the run prints the exclusion as an open extraction. The two `validate.yml` assertions stay. openDox-code's F9.1 is unchanged (R1Q8 (a)). | R1Q6 (d) | T041, T043, T049 |
| B | 9.4 | An addendum: each of openXdox's six skips either asserts, or its file joins the declared exclusion. | R1Q6 (d) | T044 |
| B | 9.2 | An addendum (T006): for release 1, openXdox-code's whole suite runs less T041's declared exclusion, which is reported as an open extraction with its count and each entry's reason. T097 ticks 9.2 with that note, and requirement 9 stays open for openXdox-code until the direction arc (T008) lands. | R1Q6 (d) | T041, T043, T097 |
| C | F5.2; 12.5's falsifier | The "unedited by the arc" check subtracts the edits entered in a reviewed allow-list in openXdox-code, such as `tests/protected_suite_respellings.yaml`. Each entry names the suite, the landing, the reference it respelled, and its review. No edit that weakens an assertion is entered. | R1Q7 (a) | T043, T059, T086 |
| F | F5.2 | The reviewed allow-list, R1Q7 (a)'s, also admits the two edits F7.1 requires, each entered with its reason and neither as a respelling: the added `tests/test_snapshot.py::test_the_validator_is_the_installed_consumers_own`, and the revised `tests/test_snapshot_validator_home.py::test_a_start_outside_the_product_is_refused_not_walked`, whose answer 7.3 governs. | R1Q14 (a) | T061, T063 |
| F | F9.1 (openXdox-code); 9.2 | The declared exclusion, R1Q6 (d)'s, admits three more reasons, each entry naming its own: openxFactory's status-exemption rail and openxFactory's contracts, both pending the direction arc (T008), and the consumer's schemas until 7.3 lands, for `tests/test_snapshot.py` alone. Each is reported as an open extraction, as the `doc_health` entries are. | R1Q24 (a), R1Q25 (b) | T041, T043, T049, T061 |
| F | 9.2, beside the release map | An addendum. The RULED map puts Group 9 in phase 1, and 9.2's whole-suite check lands there (T043). The box closes in phase 3, where its ratchet reaches `(0, 0)` (T086), because 9.2 lowers the ratchet *"as each deferred reach closes"*. 7.3 stays in phase 2, as the map has it. | R1Q25 (b) | T043, T086, T097 |
| G | 4.3 | An addendum. Every consumer mechanism on release 1's path gets an openDox-owned neutral default, which the entry points register where no host has (R1Q3 (a)'s pattern), and openXdox contributes its governed one through the same seam (R-G3's pattern). For openxFactory's two reaches, openDox's default validators run over its spec leg's two chat schemas, and there is no status exemption by default. A bare process still refuses, naming the seam (4.2). | R1Q10 (a) | T052, T055, T059, T084, T085, T086 |
| G | 5.3 | `display_profile.py` changes in one place, where `SNAPSHOT_VALUES`' defaults become the neutral snapshot's values. No word is re-authored. 5.3a's `values` block, which R1Q11 (a) also implies, is batch I's (R1Q26 (a)). | R1Q11 (a) | T054 |
| G | 7.0; 7.1 | openDox's validator validates its spec leg's FOUR kinds: 7.1's three, and the neutral snapshot schema T053 adds to openDox-spec. The code leg carries digest-checked copies of the four, which a test holds to the spec-leg commit the openDox root pins. The malformed fixture breaks one of the neutral schema's rules. | R1Q11 (a), R1Q12 (a) | T051, T053, T057, T058 |
| G | 9.5 | An addendum. Phase 2 cuts one contract bundle, a `dox-v1.x` minor at the openDox root under its four-value rule, because T053 adds an openDox-spec contract. openDox-spec joins the arc's repositories, and its landings carry the trailer (11.0). | R1Q11 (a) | T053, T062, T090 |
| G | F5.2 | Its environment also composes openxFactory at a NAMED commit. After the two installs it requires `OPENXFACTORY`, puts `"$OPENXFACTORY/scripts"` on `PYTHONPATH`, and quotes that checkout's commit. Only the environment changes. | R1Q23 (a) | T059, T061, T063 |
| H | F10.1; 10.3 | F10.1 installs `".[local]"` and runs `opendox generate-and-open --local …`, and `opendox --help` stays its first assertion. 10.3's README documents that command. The install line follows from R1Q15 (b) together with R1Q16 (iii), because the local mode's server arrives only with the extra. | R1Q15 (b), R1Q16 (iii) | T070, T076, T077 |
| H | 13.4 | An addendum. `generate-and-open --local` selects the local mode explicitly, as `OPENDOX_INSTALL_MODE=local` does. With neither, the install is hosted, as 13.5 requires. | R1Q15 (b) | T070 |
| H | 13.1; F13.1 | 13.1 leaves the packaging to the realization, and an addendum names it. The document server starts the bundled server as its own child and reports it. Starting and migrating the store is all release 1 asks of it. It ships as the `opendox[local]` extra, and it stops with the entry point. F13.1 installs `".[local]"`. | R1Q16 (i)–(iv) | T072, T073, T074 |
| H | 16.3 | 16.3 leaves two choices to the realization, and an addendum names them. A built-in resolver takes `env:NAME` and OS-keyring references, at call time and inside `doxbench_provider.py` only, and such a record needs no broker. A third auth kind, `none`, forbids `broker_argv` and `credential_ref`. It joins after the two kinds that exist, so F16.1's `AUTH_KINDS[0]` is unchanged. | R1Q17 (b), R1Q18 (a) | T080 |
| I | 5.3a | An addendum. openXdox's facet also carries a `values` block beside its one stage, holding the governed snapshot's values, because 5.3's defaults become the neutral snapshot's values (batch G). `display_profile.py` already lets a host override those values. The facet stays partial in its stages, so the falsifier, which reads only the stages, is unchanged. openxFactory composes the block in a non-arc act. | R1Q26 (a), with R1Q11 (a) | T060, T059, T066 |
| I | 12.5's falsifier | The reviewed allow-list (batch C) also admits the two edits to `tests/test_gate_loop_views.py` that 5.3a's `values` block requires, each entered with its reason and neither as a respelling: `test_the_display_facet_declares_one_stage_entry_and_nothing_else`, which then admits the block beside the one stage, and `test_the_overlay_changes_four_words_and_the_named_absence_and_nothing_else`, whose changed leaves then include the block's `values.*` leaves. No other assertion changes. | R1Q26 (a) | T060, T059 |
| I | 7.3; F7.1 | The consumer's validator validates its own three kinds from its installed distribution wherever it runs, and the other kinds only where the tree it runs from supplies their schemas, its own `contracts/` read first, as openxFactory's composed validator does today. F7.1's second test reads: every schema this install validates is on disk. No contract changes. | R1Q27 (a) | T061, T063 |
| J | F9.1 (openXdox-code) | The declared exclusion takes a fourth entry: `tests/integration/test_assembled_surface.py::test_the_assembled_help_tree_is_the_31_entry_tree_the_manifest_records`, deselected for T042's own reason (`cli_gate` imports openxFactory's `doc_health` at load time), pending the direction arc (T008). It is reported as an open extraction like the other three. T008 removes the entry together with the workflow's own deselect. openDox-code's run is unchanged. | `5870594693`, citing `5859927858` | T043, T049, T008 |
| K | requirement 17 and scenario 17.1 (spec delta); 16.3 | A dated note in requirement 17's body, after its SHALL paragraph and above its scenarios, in batch D's form, with a pointer after batch H's 16.3 addendum. No ratified text is rewritten. A credential the built-in resolver resolves (`5880893901`) and a token a broker mints (`5890601202`) are each sent only over `https://`, or over `http://` to `127.0.0.1`, `[::1]` or `localhost`. Any other `http://` endpoint that would receive one is refused when it is declared (`ENDPOINT_NOT_PRIVATE`), before anything is resolved or minted. The request follows no redirect, and over plain `http://` it takes no proxy. The auth kind `none` keeps its route. F16.1 is unchanged. | `5916000030`, item 1 | T080, and openDox-code#64 (no task of this plan) |
| K | F5.2 | The reviewed allow-list, R1Q7 (a)'s, also admits T061's ten walk-premise edits, each entered with its reason and none as a respelling: nine in `tests/test_snapshot_validation_launch.py`, and `tests/test_snapshot.py::test_a_missing_validator_is_unavailable_not_a_verdict`. `test_a_run_dir_beside_a_checkout_still_uses_that_one_first` inverts its answer and keeps its name. For F5.2, batch C's "the entry's recorded text" reads as several entries' texts together: one landing's entries for one suite, applied in the order listed, chain by git blob, and the call passes `--chains`. 12.5's falsifier is not amended, and its call refuses a chain. | `5916000030`, item 4 | T061, T063 |
| L | 4.3 | An addendum after batch G's. A flag in the served `/capabilities` payload's `actions` map whose affordance is a route this server serves is true only where such a route answers. `gate` and `refresh`, whose routes a host contributes through the route bindings, are true only when the assembled bindings carry a route they govern, so standalone both read false (and the workbench's session controls, which read `actions.gate`, are hidden), and a composed host reads as today. `notebook`, `edit` and `session` keep their conditions, and `intent` governs a POST to another plane's intent API, a route that plane answers, so its condition stands. The three reaches that drop a connection standalone (`serve_workbench.py:1219` and `:2611`, `serve_project.py:271` at `047bb4fa`) answer through their seams, from openDox's default where one serves the request, or else with a structured refusal, never a dropped connection, as 4.2 requires. | `5920216845`, item 1 | T084 |

R1Q4 (a) and R1Q8 (a) amend nothing in #1144. They shape T015, T038, T046 and
T036 only. Nor do three of round 2's answers. R1Q13 (a) with (c) shapes T050,
T054 and T096, R1Q19 (a) shapes T088 and T096, and R1Q21 (a) is a process
answer, recorded in plan.md. Nor do items 2 and 3 of `5920216845`. T085
moves T058's two workbench-manifest rules into openDox's validator, and T084
prints every broken rule once, because no #1144 falsifier names those rule
ids or fixes the CLI's rejection output: F7.2 asserts only that the
fixture's rule id is printed.
