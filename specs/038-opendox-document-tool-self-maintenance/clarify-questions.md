# Clarify questions — 038-opendox-document-tool-self-maintenance (round 1)

Status: draft

**Feature**: `038-opendox-document-tool-self-maintenance`, release 2 ("the
document tool and self-maintenance", phases 4–5) of the ratified OpenSpec
change `add-neutral-product-standalone-operability` (#1144).
**Lane**: `openxfactory-4`. **Raised**: 2026-10-05, at `/speckit.specify`,
before any plan or code. **Answer state**: OPEN. All 25 round-1 questions
await Brett Heap. Nothing here is decided by this feature. Each question puts
its recommended option first, marked **(Recommended)**, and that is a
recommendation only.

**Naming.** Round 1's questions are `R2Q1`…`R2Q25`. A bare `Q<n>` names one of
#1144's own rulings (RULING Q1, RULING Q2, Q-R4, DIRECTION Q5), and `R1Q<n>`
names plan 034's, so this round uses neither. The inventory ids (`OQ-12-n`,
`OQ-H-n`, `OQ-H15-n`) are kept beside each question, so that every candidate
can be traced to where it went.

**Inputs.** Three read-only inventories by lane openXfactory-3, delegated by
this lane (#656 `6001723339`, claimed on `6001723764`):

- R2-INV-12, for Group 12 (17 open questions, `OQ-12-1` to `OQ-12-17`);
- R2-INV-HEALTH part A, for Groups 6 and 14 (22, `OQ-H-1` to `OQ-H-22`);
- R2-INV-HEALTH part B, for Group 15 (22, `OQ-H15-1` to `OQ-H15-22`).

These add to this feature's own reading of #1144 and its four release-2
rulings. All three inventories pin the same trees this feature measured:
openDox-code `a9ac96f9`, openXdox-code `56e1c238` and openxFactory `0f2a87f6`,
all `main` on 2026-10-05.

**Revision.** Lane openXfactory-3 checked round 1 read-only at `43ddf275` and
found 14 questions to fix and two candidates missing. Every fix is folded in
below, and each was verified against the trees before it was written in. The
two candidates are now asked: OQ-H-3 within R2Q16, and OQ-H-19 as R2Q25.

**How the 61 candidates were sorted.**

- **Round 1 (this file's first section) holds only what Brett must decide.** A
  candidate is here if its answer changes WHAT the spec requires, and neither
  #1144 nor the four rulings (`5783934499`, `5784155201`, `5784247356`,
  `5784295745`) already decide it. Pairs that one answer settles are merged.
- **"Deferred to the plan, with proposed defaults"** holds the design-level
  questions. The plan writer proposes each default, and Brett rules them when
  he rules the plan.
- **"Round 2"** is empty: 25 questions fill round 1's budget of 25.
- **"Where every candidate went"** maps all 61 inventory ids and this feature's
  own. Nothing is dropped silently.

Box numbers (`12.6a`, `14.5`, …) are #1144 `tasks.md`'s, and `tasks.md:N`,
`spec.md:N` and `design.md:N` are lines in #1144's change directory. Falsifier
labels are plan 034's: `F<group>.<n>` is the n-th FALSIFIED BY box of that
group, so F12.1 is 12.5's governed-flow proof and F12.2 is the submission and
landing acceptance.

**How to answer.** One line per question is enough, for example `R2Q1 a`.
Each answer is written inline under its question, and encoded into `spec.md`
in the same commit. An answer that changes a falsifier or a task line of
#1144's `tasks.md` lands there as a bookkeeping amendment on your word, in plan
034's T007 form, under a Rule 6 window. An answer that would change a
requirement's text or a scenario is put to you as a ruling first.

**Six are contradictions, not gaps**: R2Q1, R2Q2, R2Q6, R2Q8, R2Q9 and R2Q10.
**Two ask only whether to amend ratified text, and recommend keeping it**:
R2Q19 and R2Q20.

**What each phase waits on.**

| phase | cannot be planned without |
|---|---|
| 4 (Group 12) | R2Q1–R2Q8 |
| 5 (Groups 6, 14, 15) | R2Q9–R2Q21, R2Q25 |
| release 2's close | R2Q22–R2Q24 |

---

## Round 1: questions for Brett Heap

### R2Q1 — What does "one interface for both" bind? *(phase 4; FR-004)* — CONTRADICTION

**Open because** the release map's phase-4 cell reads *"local merge and the
governed pull-request path, the neutral submission step, one interface for
both"* (`tasks.md:108`; `design.md:800`, *"submission behind one
interface"*). That cannot be one protocol. 12.1 says *"SPLIT THE PROTOCOL"*
(`tasks.md:2464`), and 12.6a makes landing *"a SEPARATE protocol,
`session_pr.LandingPort`"* (`tasks.md:2767-2773`). The phrase is elaborated
nowhere (OQ-12-3). `design.md:1061-1063`'s *"not one interface serving both"*
is about the submission seam and the generator seam, so it does not decide
this.

- **(a) (Recommended)** One USER-FACING interface. The `submit` and `land` verbs
  and routes, and the Health view's land action, are the same in every mode.
  Behind them, the three protocols stay split as 12.1 and 12.6a require, and
  each is bound the way #1144 already says:
  - `submit`'s port comes from injection, through `submission_factory` and
    `_submission_port`, and is `LocalGitSubmissions` when nothing is injected
    (12.4, `tasks.md:2500-2505`);
  - the governance query binds the lander alone: `landing_factory` under
    `standalone`, the host's own instrument under `governed`, and nothing
    under `unknown` (12.6a, `tasks.md:2773`, `:2793-2796`).

  *Consequence:* no box text moves, and the map's phrase is recorded as a
  non-normative reading.
- **(b)** One PROTOCOL for submission and landing. *Consequence:* this reverses
  12.1 and 12.6a, which `design.md` § D9 argued against, and needs a ruling.
- **(c)** Strike the phrase as an editorial slip. *Consequence:* a bookkeeping
  amendment to the map's cell and to § D13's line.

**ANSWER:** _awaiting Brett Heap_

### R2Q2 — Does `pull_request_factory`'s unset default stay `GhPullRequests`? *(phase 4; FR-003)* — CONTRADICTION

**Open because** 12.4 says both things (OQ-12-1). `tasks.md:2500-2511` declares
a NEW pair of bindings and keeps the `PullRequestPort` ones *"serving the
governed verb they serve today"*. `tasks.md:2513-2519` then says *"The unset
default becomes the neutral implementation; `GhPullRequests` becomes ONE
contributed implementation … this box repoints its UNSET DEFAULT"*. The same
leftover appears twice in `design.md`: at `:476-478` and at `:1059-1061`
(*"requirement 11 repoints its unset DEFAULT"*). Ruling `5783934499`'s third
bullet, which predates the split, says the same.

**Measured:** openXdox-code's `tests/test_session_snapshot.py:893-916` asserts
that the server's unset port IS `GhPullRequests` (the assertion is at `:910`).
F5.2 protects that suite (`tasks.md:896`). openxFactory's host injects no
`pull_request_factory`, so the governed flow runs on that unset default today.

- **(a) (Recommended)** The NEW pair (`submission_factory`, `_submission_port`)
  is the product's own binding, and its unset default is `LocalGitSubmissions`.
  `pull_request_factory` and `_pull_request_port` keep `GhPullRequests` as their
  unset default, and serve `gate open-pr` unchanged. The repoint sentences
  (`tasks.md:2513-2519`, `design.md:476-478` and `:1059-1061`) are read as the
  residue of the withdrawn draft that 12.4's own parenthesis records, and a
  bookkeeping note says so. *Consequence:* the protected test stands, and the
  governed flow is untouched (12.5). **But with R2Q3 (a) as well, no governed
  host contributes `GhPullRequests` in release 2.** Two texts then go
  unrealized in release 2:
  - ruling `5783934499`'s third bullet, *"contributed by the governed host"*;
  - 12.5's *"With the host's implementation registered"*
    (`tasks.md:2659-2660`).

  A bookkeeping note cannot accept that. Choosing (a) with R2Q3 (a) is your
  acceptance of it.
- **(b)** Repoint the `PullRequestPort` default away from `GhPullRequests`. A
  push-only class cannot serve that protocol, so an unset port refuses, and
  openxFactory's host injects `GhPullRequests` explicitly. *Consequence:* the
  ruling's bullet and 12.5's clause are realized. The protected test needs an
  allow-list entry, and the host wiring changes in phase 4.
- **(c)** Move `GhPullRequests` into openXdox, contributed by the governed host.
  *Consequence:* the largest. It touches openXdox-code's `src/` and every
  governed suite that patches `cli._pull_request_port`.

**ANSWER:** _awaiting Brett Heap_

### R2Q3 — Does any governed host carry `submit`, `land` or `health` in release 2? *(phases 4–5; FR-004, FR-007)*

**Open because** R1Q4 (a) already rules that openDox's default profile
contributes these verbs, and that a host's own profile replaces it. The ruled
option's text reads *"release 2's `submit`/`land`/`health` later"*
(`specs/034-opendox-standalone-operation/clarify-questions.md:226`). The ruling
comment, `5817152735`, summarizes it as *"The default profile contributes
openDox's own verbs (runtime now) and `NEUTRAL_DISPLAY`"*. openDox-code's
`src/opendox/default_profile.py:41` says the same.

Yet 12.4 (`tasks.md:2504-2505`) lets a governed host contribute its own
`SubmissionPort`, and 12.6a (`tasks.md:2784-2786`) lets it declare an
instrument. Both serve verbs that a host's tree carries only if the host
contributes them. This question does not reopen R1Q4 (a). It asks whether any
host contributes the verbs now (OQ-12-2).

**Measured:**
- openxFactory's host tree is held by the help golden
  `tests/domain_profile/fixtures/cli-help-tree.phase3.golden.txt`. Its test
  says to regenerate it *"ONLY with a ruling"*
  (`tests/ideation-dashboard/test_extension_point_parity.py:284`).
- openXdox-code holds the assembled tree at 32 entries
  (`tests/integration/test_assembled_surface.py:217`, docstring `:36-42`).

- **(a) (Recommended)** No host contributes them in release 2. Both hosts'
  trees, goldens and governed flows are unchanged: `gate open-pr`, and
  openxFactory's own doc-health. F12.2 proves the host-side behaviour against a
  registered test host. *Consequence:* the smallest governed-side change, and a
  host opting in is a later act. See R2Q2 (a) for what this leaves unrealized.
- **(b)** openXdox contributes `submit` (with a `GhPullRequests`-backed
  `SubmissionPort`) and `land`, routed to its instrument. *Consequence:* the
  32-entry tree and the goldens move by a batch-O style amendment.
- **(c)** Both hosts contribute all three, `health` included, running openDox's
  neutral checks over openxFactory's corpus. *Consequence:* broadest. A composed
  host has no store today (R2Q15).

**ANSWER:** _awaiting Brett Heap_

### R2Q4 — What is the governed host's "instrument", and what does routing a landing to it do? *(phase 4; FR-007, US2 scenario 4)*

**Open because** 12.6a says only *"a registered host profile that declares an
instrument"* and *"routed to the host's own instrument"* (`tasks.md:2784-2796`).
It names neither the instrument's form, nor who declares it, nor what `land`
or the fix loop's land action DOES under `governed` (OQ-12-10). Ruling
`5784247356` adds *"A governed repository gets a pull request instead"*.

- **(a) (Recommended)** The instrument is the host's contributed
  `SubmissionPort` (12.4), declared in the host profile. Under `governed`, no
  lander is bound. `land`, and the fix loop's land action, SUBMIT through the
  host's port (for openXdox, a push followed by opening or updating the pull
  request) and report where the work went. The merge stays the governance's
  act. *Consequence:* one contribution serves both acts, the fix loop's "pull
  request instead" needs no second step, and `gate open-pr` is untouched.
- **(b)** Under `governed`, `land` refuses, naming the host's declared
  instrument (for openxFactory, `gate open-pr` and the Merge Master ritual).
  *Consequence:* simplest. A governed user takes two acts.
- **(c)** The host declares a separate instrument callable, a sixth facet beside
  `opendox_host.FACETS`. *Consequence:* a fourth seam to declare and test.

**ANSWER:** _awaiting Brett Heap_

### R2Q5 — What may a standalone install submit and land? *(phase 4; FR-004, FR-007)*

**Open because** 12.4a and 12.6a write `--branch <session-branch>`
(`tasks.md:2536-2537`, `:2814-2815`), while F12.2 submits a plain branch,
`sess-1` (`tasks.md:2828-2834`).

**Measured** (OQ-12-8): openDox has no session opener of its own on a
standalone plane:
- every session-opening verb is a gate verb;
- openDox's default `GATE` refuses governed records;
- release 1 RULED Save refused by name on standalone (`5971834845`).

So a standalone user today cannot make a session branch in openDox at all.

- **(a) (Recommended)** `submit` and `land` take any local branch except the
  default branch, as F12.2's `sess-1` does. That covers branches the user made
  with git, and the fix loop's own `health-fix-*` drafts. A live session whose
  branch is landed ends by the existing merge observation
  (`reconcile_merged_session`). A standalone session opener and Save are a
  follow-on outside release 2. *Consequence:* release 2 ships as specified.
  Until the follow-on, a standalone user edits with git or through the fix
  loop.
- **(b)** Release 2 also gives standalone openDox a session opener and Save (a
  neutral default behind the gate seam). *Consequence:* new scope that no box of
  #1144 names, and it needs a ruling and an amendment.
- **(c)** Only branches in openDox's session namespace may be submitted or
  landed. *Consequence:* F12.2's `sess-1` needs an amendment, and nothing on a
  standalone plane could be submitted until (b) exists.

**ANSWER:** _awaiting Brett Heap_

### R2Q6 — Where does a standalone `land` merge, and how does a landed default branch reach a remote? *(phase 4; FR-007)* — CONTRADICTION

**Open because** 12.6a makes a landing a `--no-ff` merge commit that `git
revert -m 1` undoes (`tasks.md:2812-2814`). F12.2's third node expects *"the
tree restored"* (`tasks.md:2910`). Feature 007's served-checkout rule pins the
opposite (OQ-12-6, OQ-12-7), and 12.6a says nothing about a remote.

**Measured:**
- **Feature 007** is codexFactory's `specs/007-workbench-branch-sessions/spec.md`,
  read at `main` `1a32f399`.
  - FR-004 (`:517-519`) refuses any session operation that would switch,
    reset or stash the served checkout.
  - SC-002 (`:811-816`) holds the served checkout's branch and `HEAD`
    unchanged across every session operation. Its working tree may change only
    inside the gate-records path.
- **Feature 007's realization** is openDox-code's
  `src/opendox/session_git.py`.
  - Every subcommand that moves a working tree, an index or `HEAD` is absent
    from `SERVED_ALLOWED_SUBCOMMANDS` (`:99`). That includes `merge`, `revert`
    and `update-ref`, which `:93-97` name.
  - `tests/test_session_git.py:563-564` pins `merge` and `update-ref` by name.
  - `fetch` and `pull` are refused at every cwd (`:125`).
- **The promoted scenario** *"The served checkout is asked to move"* forbids
  only a switch, a reset or a stash.
  - It was promoted into openxFactory's
    `openspec/specs/ideation-dashboard/spec.md` by `a0ea7666` (2026-07-31).
  - It left that file with the carve's archive, `5851bd7c` (2026-09-22), for
    openDox-spec to re-promote (Group 8, outside both releases).
  - Its text now lives only in openxFactory's
    `openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/specs/ideation-dashboard/spec.md:28-30`.

- **(a) (Recommended)** Land in a worktree, then fast-forward the served
  checkout.
  - The lander makes the `--no-ff` merge commit in a landing worktree of its
    own, outside the served checkout, under a valid confirmation.
  - **Served checkout on another branch:** the lander advances the default
    branch there, and nothing of feature 007 moves.
  - **Served checkout on the default branch** (the common standalone case,
    `main`): the lander then fast-forwards the served checkout to the merge
    commit with `git merge --ff-only`, only when that checkout is clean. A
    fast-forward that no longer applies refuses, which serves as the
    compare-and-swap. It never switches, resets or stashes, so FR-004 and the
    promoted scenario hold.
  - **Feature 007 gains THREE named exceptions**, each scoped to a confirmed
    landing onto the branch the served checkout holds:
    1. `SERVED_ALLOWED_SUBCOMMANDS` admits `merge`, in its `--ff-only` form
       alone, and `tests/test_session_git.py:563-564`'s pin of `merge` moves.
    2. SC-002's "`HEAD` unchanged" admits that fast-forward.
    3. SC-002's "working tree changes only inside the gate-records path" admits
       the files the fast-forward brings.
  - `land` pushes nothing. Before landing, where a remote is attached, it reads
    the remote's default-branch tip with `ls-remote` (already allowed). It
    refuses if the local default branch does not contain that tip, and names the
    remedy.
  - A landed default branch reaches the remote only by the user's own
    `git push`, which the openDox root's README documents. `submit` cannot carry
    it, because R2Q5 (a) refuses the default branch.

  *Consequence:* the student lands from the view or the CLI. Feature 007's three
  pins move by your word. Landing and publishing stay separate acts.
- **(b)** Land only when the default branch is NOT checked out in the served
  checkout, and refuse otherwise. *Consequence:* feature 007 is unchanged, but
  the common standalone case (served checkout on `main`) cannot land from the
  view.
- **(c)** Land only from the CLI, in the user's own checkout outside the served
  process, and drop the view's confirm issuer. *Consequence:* feature 007 is
  unchanged, but 12.6a's two-issuer text needs a ruling.
- **(d)** As (a), and `land` then pushes the landed default branch to the
  attached remote, with `submit`'s redaction. *Consequence:* one act lands and
  publishes. But pushing the default branch is an act no box of #1144 names, and
  ruling `5783934499` pushes only *"the session branch"*, so this needs a
  ruling.

**ANSWER:** _awaiting Brett Heap_

### R2Q7 — Which branch is "the default branch", and how does a standalone owner's first declaration reach it? *(phase 4; FR-007)*

**Open because** 12.6a reads `.opendox/governance.yaml` *"from the tip of the
DEFAULT BRANCH"* (`tasks.md:2779`), and never defines that branch. It also
refuses a branch that adds its own declaration, so the product cannot land the
first one (OQ-12-15).

**Measured:** the code points two ways.
- The session layer fixes `DEFAULT_BASE = "main"` (`branch_session.py:149`,
  `session_pr.py:55`). A plain repository with no remote has no `origin/HEAD`.
- The runtime deliberately pushes the branch HEAD names, *"not an assumed
  `main`"* (`runtime/repository_act.py:1266-1270`).
  - `create_repository` and `initialize_repository` take a `branch` argument
    (`:604`, `:659`), whose default is `main`
    (`runtime/local_git_adapter.py:146`).
  - The same docstring says the adapter serves a repository whose HEAD is
    `master` without complaint.

- **(a) (Recommended)** The default branch is openDox's existing session base,
  `main`. A repository with no `main` is `unknown`, and is refused naming it.
  The product never writes the default branch outside `land`. With no
  declaration, `land` refuses, naming the exact file and content, which the
  owner commits with git. The openDox root's README documents this.
  *Consequence:* one rule the session code already uses, and one documented git
  step for a new owner. **But a repository the product itself created on
  another branch, or serves on `master`, reads `unknown` and can never land,
  until its owner creates or renames `main`.**
- **(b)** The default branch is `origin/HEAD` where a remote is attached, and
  `main` otherwise. The first declaration is handled as in (a). *Consequence:*
  repositories cloned from a `master` remote work, the answer changes when a
  remote is attached, and a local-only `master` repository still reads
  `unknown`.
- **(c)** The default branch is whatever HEAD names in the main worktree at
  landing time, and `project create-repository` seeds the declaration.
  *Consequence:* a checked-out session branch would read as the default, so a
  branch could decide its own landing, which 12.6a forbids.

**ANSWER:** _awaiting Brett Heap_

### R2Q8 — Where does 12.5 run, and who repairs the governed suites' reds? *(phase 4; FR-005, US3)* — CONTRADICTION

**Open because** 12.5 (`tasks.md:2659-2669`) names Group 9 as its only
prerequisite, and F12.1 (`tasks.md:2674-2699`) runs the 16 governed suites with
plain `pytest` in an openXdox-code checkout. That cannot pass today (OQ-12-4,
OQ-12-5).

**Measured at `56e1c238`** (R2-INV-12, re-measured by this feature on
2026-10-05):
- Fifteen of the 16 suites are entries of `tests/declared_exclusion.yaml`, each
  with the reason `doc_health`, and they fail to import alone.
- Composed with openxFactory's `scripts/` (R1Q23 (a)'s form for F5.2), the 16
  read 668 passed, 170 failed and 4 errors: 174 red across 10 files.
  - This feature's run installed openDox-code `a9ac96f9`, put openxFactory
    `0f2a87f6`'s `scripts/` on `PYTHONPATH`, and initialized its `openDox`
    and `openXdox` submodules.
  - Plan 034's T086 recorded the same 174.
- Classed by each red's first cause:
  - 62 need a registered governed host (41 find no `gate` subcommand, and 21
    meet `unknown_action`);
  - 55 are the `display.js` harness copy, 4 of them setup errors;
  - 16 read names the carve moved (4 `cmd_gate_*`) or old in-tree paths (12);
  - 16 cannot load the gate-action record schema;
  - 3 reach a moved `hosted_index`;
  - 22 are singletons.

  R2-INV-12 classed 50, 15 and 28 of the same 93 differently. Both readings
  agree on the 62, the 16 and the 3.

R1Q6 (d) already requires the `doc_health` direction arc to be DECIDED before
12.5 needs these suites. That ruling (the staged topic's Q1–Q4 and Q6) is owed
first, whatever is answered here.

- **(a) (Recommended)** F12.1 runs composed, as F5.2 does under R1Q23 (a), until
  the direction arc's realization lands. The amendment is a bookkeeping line.
  The 174 reds are repaired in phase 4 without editing the proofs:
  - a host-registering conftest outside the 16 files, as T104's
    `HOST_PLANE_SUITES` already does;
  - the harness copy fixed, and the schema placed where the suites read it;
  - an allow-list entry for each pure respelling (batch C);
  - each singleton traced, and repaired by one of these means or by an entry.

  *Consequence:* phase 4 owns a sizeable repair slice, which can start the day
  the plan is ruled. The exclusion stays an open extraction.
- **(b)** 12.5 waits for the direction arc's REALIZATION, and runs standalone as
  written. *Consequence:* phase 4's close is gated on an arc that has no owner
  yet (its Q6).
- **(c)** Re-scope 12.5's governed set, by amendment, to the suites that pass
  composed today. *Consequence:* requirement 11's tenth scenario rests on 6 of
  the 16 suites.

**ANSWER:** _awaiting Brett Heap_

### R2Q9 — Approve the falsifier amendments that release 1's rules force? *(phase 5, and the verb shapes of phases 4–5; FR-004, FR-008, FR-011, FR-015, FR-017, FR-020)* — CONTRADICTION

**Open because** each item below changes #1144's falsifier or box text after
ratification, which by the estate's practice goes to you (the T007 batches).
Items 1 and 2 are conflicts with release-1 rulings (OQ-H-1, OQ-H-6), and items
3 to 6 are part B's (OQ-H15-22 (a)–(d)).

1. **F6.1** (`tasks.md:1143-1165`).
   - It runs a bare `python3` and asserts `completed`. But batch G
     (`tasks.md:560-562`) says *"a bare process still refuses, naming the
     seam"*, and openDox-code's `test_health_check_seam.py` pins that.
     **Measured:** at `a9ac96f9`, the call answers `not-available`.
   - The amendment: F6.1 builds an entry point, which registers openDox's own
     check, before the call, as F3.1 line 2 was amended.
   - It also strikes F6.1's out-of-date "Today" sentence (`tasks.md:1163-1165`),
     and notes 6.2's matching description (`:1138-1142`) as superseded. Both
     say the call fails with *"No module named 'doc_health'"*. At `a9ac96f9`
     the detail is the seam's `HEALTH_CHECK_NOT_REGISTERED`
     (`workbench.py:1594`), and `test_health_check_seam.py:143-144` asserts
     that `doc_health` and `No module named` are both absent from it.
2. **F14.1 and F15.1** (`tasks.md:3302-3366`, `:3548-3651`).
   - Both run `opendox health …` in local mode with no document server running.
     F14.1 also runs `runtime reset` and `runtime migrate` (`:3360-3361`);
     F15.1 runs only `health` verbs (`:3567-3618`).
   - R1Q16 (i) and (iv) give the bundled server to the document server, and the
     local runtime verbs refuse `local-bundle-unverified` without it.
   - The amendment: each block first starts the document server in the
     background, the way F13.1 does (`tasks.md:3085-3087`):
     `opendox generate-and-open --repo-root $C --repository fixture --no-open
     --port <port> &`. It waits for readiness, and kills the server on exit.
     Both blocks already export `OPENDOX_INSTALL_MODE=local` (`:3310`,
     `:3556`), so no flag is needed. The `health` verbs, like the runtime
     verbs, then reach the running bundle, and refuse by name without one.
     For F15.1, this is needed for the `health` verbs alone.
3. **F15.1 asserts its platform precondition**, a working kernel sandbox, and
   exits 1 naming it otherwise, as F12.2 does for `gh`.
4. **15.6a's forking pack** gives its child its own pack id in argv, so that
   F15.1's `ps` check cannot pass vacuously.
5. **15.1b's corpus export** cannot be steered by `export-subst` or
   `export-ignore`: either the export is not a plain `git archive`, or those
   attributes are refused.
6. **15.6a's escaping pack** counts a WRITE as its "restores write permission"
   success, never a chmod.
7. **The verb shapes** of 12.4a (`submit`), 12.6a (`land`) and 14.5 (`health`)
   gain the same `--local` flag as `generate-and-open` (batch H). A flag and a
   setting that disagree are refused, naming both. F14.1 and F15.1, which
   export the setting, stand as written.

- **(a) (Recommended)** Approve all seven as listed. They land as ONE
  bookkeeping batch, in T007's form, under a Rule 6 window, before phase 4's
  first checkpoint, the earliest point any of them is needed. *Consequence:*
  the falsifiers can pass against the release-1 code without reversing R1Q16 or
  batch G.
- **(b)** Rule them one by one in round 2. *Consequence:* phase 5 waits a round.
  For item 2, the alternative is to amend R1Q16 instead, so that each `health`
  verb attaches to, or starts, a transient bundle of its own.

**ANSWER:** _awaiting Brett Heap_

### R2Q10 — What is a finding's `id`? *(phase 5; FR-011, FR-015, US5, US6)* — CONTRADICTION

**Open because** F14.1 and F15.1 use `id` both as the per-finding handle
(`--finding ID`, `refs/heads/health-fix-<id>`) and as a kind name.
- **F14.1** names `broken-link` and the other kinds, plus two non-kinds,
  `human-only-finding` and `accepted-finding` (`tasks.md:3295-3301`,
  `:3326-3345`).
- **F15.1** names `patch-ok` and similar labels.

Requirement 15 needs an exception that *"SHALL cite what it is accepting"*
(`spec.md:509`) across store resets. 14.5 declares the field but no identity
rule (`tasks.md:3259-3262`), and two packs can return the same label (OQ-H-7,
OQ-H15-17).

- **(a) (Recommended)** A finding's `id` is a STABLE, pack-qualified key.
  - The engine derives it from the pack's id, the family, the document's path
    and a locator the family supplies. That is the shape openxFactory's
    uncited-resolution rule keys on, `(family, repository, path)`.
  - It survives a reset, is unique, and is mapped into a valid ref name for
    `health-fix-*`. `health list --json` also carries `kind`.
  - F14.1 and F15.1 are amended, by bookkeeping, to find each planted finding
    by its fixture document, not by a literal id.

  *Consequence:* exceptions cite something durable, and two falsifiers'
  selection lines change.
- **(b)** The `id` is the kind name. *Consequence:* the falsifiers stand
  verbatim, but two findings of one family, or of two packs, share an id, which
  fails requirement 15.
- **(c)** The `id` is the kind name with a numeric suffix. *Consequence:* the
  falsifiers stand, but ids shift when an earlier finding disappears, so an
  exception can attach to the wrong finding.

**ANSWER:** _awaiting Brett Heap_

### R2Q11 — What is a document's "location" for `stage-location-mismatch`, and which way does the repair go? *(phase 5; FR-010, FR-012)*

**Open because** D10.5 and 14.4 name the family, *"a declared stage that
disagrees with the document's location among the six ruled words"*
(`tasks.md:3236-3241`; `spec.md:187`), but give no rule (OQ-H-9).

**Measured:**
- openDox reads a station from the `stage:` header alone (R1Q13 (a) with
  (c)), and nothing maps a path to a station.
- 15.2a refuses renames in pack patches.
- F14.1's `git diff --name-only` check sees only a renamed file's new path.

- **(a) (Recommended)** The location is a top-level directory whose name is one
  of the six role keys or their declared words. A document outside such a
  directory has no location, and is never flagged. The `auto-fix` repair edits
  the `stage:` header to match the directory, and never moves the file.
  *Consequence:* deterministic, and it passes F14.1. A corpus without stage
  directories draws no finding of this kind.
- **(b)** As (a), but the repair moves the file into the directory its header
  names. *Consequence:* the header stays authoritative, the rename conflicts
  with 15.2a's patch rule for packs, and F14.1's path check needs an amendment.
- **(c)** A corpus-declared map from paths to stations, committed in the corpus.
  *Consequence:* the most flexible, and one more committed configuration file to
  define.

**ANSWER:** _awaiting Brett Heap_

### R2Q12 — How does the baseline work in a disposable store? *(phase 5; FR-010, FR-019)*

**Open because** requirement 6 keeps doc-health's pattern, *"new findings get
attention while persistent ones stay quiet and an uncited disappearance is
re-raised"* (`spec.md:188-190`; ruling `5784155201`). Nothing says how, in a
store that a reset may discard (OQ-H-12, OQ-H15-16). openxFactory's citations
are governance acts that a neutral corpus lacks.

**Already decided, so not asked:** across a pack upgrade, the baseline must
*"tell a genuinely new finding from one that merely arrived with a new pack
version"*, so that an upgrade does not look like a regression. D12 decides
this (`design.md:688-690`), and requirement 16 says the same
(`spec.md:584-586`). Both options below honour it: a finding whose id persists
across a pack-version bump stays persistent.

**Common to both options:**
- A finding is **new** when it is absent from the previous run at the default
  branch's tip.
- It is **persistent** when that run had it.
- It has **disappeared** when that run had it and this run does not.
- A disappearance is **cited** by a landing of the fix loop's draft for it, or
  by a commit that names its id in a `Finding:` trailer. An uncited one is
  re-raised once, as a `human-only` finding naming the original.

So a finding committed straight to the default branch is new the first time a
run sees it.

- **(a) (Recommended)** The previous default-tip run lives in the store, and a
  store reset forgets it.
  - The first run after a reset, like the first run ever, has no previous run,
    so it sees every finding once as new.
  - Pending uncited disappearances are forgotten with the store.

  *Consequence:* simple, and within RULING Q1: losing the store costs a
  recomputation. Requirement 15's survival rule covers decisions the documents
  do not contain (`spec.md:505-508`), which a pending disappearance is not. A
  reset re-alerts once, and can drop a re-raise that was still pending.
- **(b)** Disappearances are derived from git.
  - When the store holds no previous run, the engine recomputes one from git,
    over the default tip's first parent.
  - Citations are found by walking the commits between the two.

  *Consequence:* a reset loses no disappearance that the latest default-branch
  commit made, at the cost of a second check pass and a history walk. Pending
  disappearances older than that commit are still lost, because the store held
  the only record of which commit was last measured.

**ANSWER:** _awaiting Brett Heap_

### R2Q13 — Does the health table join RULING Q1's closed list? *(phase 5; FR-009, US4 scenario 2)*

**Open because** ruling `5784155201` item 4 reads *"health results become a
seventh table … with the closure test moved in the SAME change"*, the DOMAIN
reading. But 14.2 and D10.4 leave the declaration to the realization
(`tasks.md:3225-3232`; `design.md:524-557`) (OQ-H-4, with OQ-H-22's ownership
half).

**Measured:**
- About twenty assertions move whichever way this is answered, because
  `["0001", "0002"]` is hard-coded ten times.
- The ledger precedent does not cover a table that the served role must write.

- **(a) (Recommended)** DOMAIN. The results table joins Q1's list in
  `identity.TABLES`, and the closure test reads `0001` together with `0003_`, in
  the same change, as the ruling's words have it. Q1's principle stands: no
  document, and a disposable store. *Consequence:* the boundary is re-drawn in
  the open, and `0001`'s digest is untouched. The served role's access is
  verified like the other six tables'.
- **(b)** INSTALL-OWNED, beside the ledger. *Consequence:* no closure text moves.
  But `verify_runtime_access` stays blind to the table unless `SERVED_TABLES`
  grows, and the ruling's "seventh table" reads as not joining the list.

**ANSWER:** _awaiting Brett Heap_

### R2Q14 — How does 6.1a's "relocate the generic part" square with 11.1's guard and the unruled direction arc? *(phase 5; FR-008)*

**Open because** 6.1a (`tasks.md:1133-1135`) predates 11.1's narrowed surfaces
(`tasks.md:1982-1994`) and the `doc_health` direction arc (plan 034 T008). 6.1
says requirement 6 is met *"not by relocating families"* (OQ-H-17).
**Measured:** two of `scripts/doc_health/`'s 38 modules are generic, `lines.py`
and `fs_probe.py`.

- **(a) (Recommended)** 6.1a is satisfied vacuously in release 2. No family
  moves, openDox writes its own check, and no module both sides depend on is
  created. Any relocation inside `doc_health` belongs to the direction arc's own
  answer (its Q4). *Consequence:* 11.1's guard is untouched, and the box closes
  on a recorded finding.
- **(b)** 6.1a is carried out as a non-arc openxFactory act, outside 11.1's
  surfaces, in T066's form. *Consequence:* openxFactory edits `doc_health` in
  release 2.
- **(c)** 6.1a is folded into the direction arc's Q4 and waits for it.
  *Consequence:* Group 6's close is gated on an unruled arc.

**ANSWER:** _awaiting Brett Heap_

### R2Q15 — What does a HOSTED install do with the health engine and with packs? *(phase 5; FR-009, FR-017)*

**Open because** 14.5 serves the view from the entry point, the local case
(`tasks.md:3242-3269`), and 12.4a refuses `submit` on the hosted plane
(`tasks.md:2557-2562`). Nothing says whether `run`, `fix` and `accept` exist
there, which credential writes the store, or whether packs run in a pod (OQ-H-5,
OQ-H15-6).

**Measured:**
- The document server imports no database driver.
- The hosted runtime API serves six table routers, and no health.
- bwrap is refused in containers ("No permissions to create new namespace" in
  this lane's container), and a pod's masked `/proc` defeats `--proc`
  (inferred).

- **(a) (Recommended)** Release 2 serves the health engine on the LOCAL plane,
  and from the CLI. On the hosted plane, the Health view, its routes and the
  `health` verbs REFUSE BY NAME before anything runs, as `submit` does
  (12.4a). The refusal says that the health engine and its packs run only on a
  local install. Nothing runs there, so no finding is recorded. The schema
  still migrates, because there is one migration set. *Consequence:* no
  per-tenant design in release 2, and the governance pack (F1) cannot run
  hosted until a later act.
- **(b)** The hosted plane runs and lists the built-in checks per project,
  read-only, and refuses `fix`, `accept`, `land` and packs. *Consequence:* the
  plan must design a project key, membership checks and the served role's
  writes.
- **(c)** Release 2 owes a second sandbox realization for hosted pods (Landlock,
  seccomp and rlimits, or a sidecar). *Consequence:* Landlock alone cannot meet
  requirement 16's own `/proc` and whole-tree clauses, so this needs a ruling on
  what "kernel-enforced" admits.

**ANSWER:** _awaiting Brett Heap_

### R2Q16 — What runs in the sandbox, and does macOS get packs? *(phase 5; FR-008, FR-017)*

**Open because** requirement 16, read literally, puts the product's own checks
inside the sandbox. Two of its texts combine:
- *"A pack SHALL RUN IN A SEPARATE PROCESS INSIDE AN OPERATING-SYSTEM-ENFORCED
  SANDBOX"* (`spec.md:544-545`);
- the product's own checks are attributed *"as the one pack no manifest
  lists"* (`spec.md:584-587`).

Where the platform *"offers no such sandbox, packs SHALL NOT RUN"*
(`spec.md:557`). Yet requirement 6's second scenario calls a document product
that cannot report on its own documents undelivered.

Release 1 also left a host's check registered IN PROCESS at the scoped seam:
openxFactory's `scripts/opendox_host.py:524` registers `scoped_doc_health`
through `register_health_check`. Ruling `5784295745` and 15.1b say nothing of
it, and 15.1b defers *"other platforms"* (`tasks.md:3453-3454`). (OQ-H-3's
ruling half, OQ-H15-7, and this feature's own reading.)

**Measured:** bwrap is unavailable by default on every target the estate runs
today:
- this lane's container;
- GitHub's `ubuntu-24.04`, which restricts unprivileged user namespaces through
  AppArmor;
- the hosted pod (inferred).

macOS Seatbelt cannot give an own `/proc` or a PID namespace. Landlock, which
enforces in this lane's container, cannot meet requirement 16's own-`/proc`
and whole-tree clauses (`spec.md:550-553`).

- **(a) (Recommended)** TRUSTED INSTALLED CODE runs IN PROCESS, on every
  platform. That means the product's own checks (attributed `opendox`) and a
  host's check registered through `register_health_check`. Only
  manifest-listed packs run in the sandbox. Where a probe finds none (macOS, a
  restricted Linux, a container), packs do not run, and one finding against
  the install says why. There is no Seatbelt realization in release 2. The
  sandbox clause is recorded as governing manifest-listed packs, and the
  attribution clause as attribution only. *Consequence:* every install gets
  health over its own documents, and openxFactory's scoped check keeps running
  as release 1 left it. Packs run only on a capable Linux host.
- **(b)** As (a), plus a Seatbelt realization on macOS that denies fork.
  *Consequence:* macOS users get packs. It also needs a ruling that deprecated
  `sandbox-exec` counts as kernel-enforced, with fork denied standing for the
  whole tree.
- **(c)** The product's own checks, and any host's registered check, also run
  in the sandbox. *Consequence:* uniform. But no target the estate runs today
  would have any health check, and openxFactory's scoped check would stop
  running.

**ANSWER:** _awaiting Brett Heap_

### R2Q17 — Does openDox-code's required check run the sandbox suite? *(phase 5; FR-017, FR-020)*

**Open because** F15.1 names nine sandbox tests (`tasks.md:3628-3636`, within
its 24-test command at `:3627-3651`). 9.4 lets no skip carry a gap, and R1Q8
(a) shows that a change to the required check is a ruled act (OQ-H15-8).

**Measured:**
- `validate.yml`'s `validate` and `acceptance` jobs run on `ubuntu-latest`, and
  no workflow installs `bubblewrap`.
- The `validate` job pins its skip count exactly: `EXPECT_SKIPPED: "11"`
  (`validate.yml:306`), enforced at `:344`.
- On `ubuntu-24.04`, unprivileged user namespaces need
  `sysctl kernel.apparmor_restrict_unprivileged_userns=0`
  (runner-images#10443).
- `ubuntu-latest` moves to 26.04 between 2026-10-19 and 2026-11-19. Its
  shipped bwrap AppArmor profile reportedly permits bwrap, on a secondary
  source (anthropics/claude-code#87680) that nobody has measured on a runner.

- **(a) (Recommended)** The required `validate` job pins `ubuntu-24.04`,
  installs `bubblewrap`, sets the AppArmor sysctl, and proves the sandbox live
  before the suite. Under `CI`, the sandbox tests FAIL rather than skip,
  mirroring `tests_runtime/conftest.py:130-147` (`_skip_or_fail`), so
  `EXPECT_SKIPPED` stays at 11. A move to 26.04 waits until its bwrap profile is
  measured on a runner. There is no macOS job in release 2. *Consequence:* the
  guarantee is measured on every PR, and the required check changes by your
  word.
- **(b)** The sandbox tests run in their own declared job, reported by name and
  never skipped silently, like AT-R1's `acceptance` job. In `validate`, the nine
  are deselected by name, so `EXPECT_SKIPPED` stays at 11. *Consequence:*
  `validate` changes by one deselection, and the sandbox is still proved on
  every PR.
- **(c)** The sandbox tests skip in CI with a declared reason, and run on a
  capable host. *Consequence:* against 9.4, and `EXPECT_SKIPPED` moves from 11
  to 20 by your word.

**ANSWER:** _awaiting Brett Heap_

### R2Q18 — What may a pack depend on? *(phase 5; FR-016, FR-017)*

**Open because** the digest covers only the pack's own source tree
(`tasks.md:3412-3413`). Requirement 16's *"the libraries its runtime reads"*
(`spec.md:549`) names no owner and no pin. An unpinned library *"silently
changes what a corpus is judged against"*, 15.1a's own stated hazard
(OQ-H15-2). openXdox's governance pack (F1) would need PyYAML, and openxFactory's
`doc_health`.

- **(a) (Recommended)** In release 2, a pack is Python source using only the
  standard library, and the neutral contract module the engine's runner
  provides. The install's own interpreter and standard library are mounted
  read-only. *Consequence:* the pack's digest plus the install's version
  (`importlib.metadata.version("opendox")`, `tasks.md:3546`) pin everything that
  runs. F1 must vendor what it needs, or wait for a later act.
- **(b)** A pack declares third-party dependencies, which the engine installs
  into a per-pack environment pinned by hash. *Consequence:* richer packs, and a
  dependency installer in the engine.
- **(c)** The install's own site-packages are mounted read-only.
  *Consequence:* simple, but what a pack runs then depends on what the user
  installed, which is the very hazard 15.1a names.

**ANSWER:** _awaiting Brett Heap_

### R2Q19 — Amend requirement 16 and 15.1b so that a pack may see git history? *(phase 5; FR-017)*

**Open because** #1144 as ratified already decides this: a pack sees no
history.
- 15.1b exports `git archive <commit> | tar -x` (`tasks.md:3427-3428`), a tree
  that carries no `.git`.
- Requirement 16 lets the pack see, beside that copy, *"only"* its own code,
  the interpreter and libraries, a private scratch space, and its own process
  and device filesystems (`spec.md:546-551`).

The question is whether to amend it. openxFactory's families read history:
`scripts/doc_health/corpus.py:420` opens `class RealGit`, with `log` at
`:434-470` and `rev-list` at `:683`. So the follow-on F1 port could not run
those families unchanged (OQ-H15-3).

- **(a) (Recommended)** Keep requirement 16 and 15.1b as ratified: the exported
  tree only. *Consequence:* the smallest surface to contain. F1 ports its
  history-reading families only after a later act gives them a history seam.
- **(b)** Amend requirement 16 and 15.1b to mount a read-only history bundle of
  the corpus beside the copy. **This changes ratified text, so you rule it as an
  amendment.** *Consequence:* F1 can port those families unchanged, and the
  sandbox exposes the corpus's whole history, which is more of the user's data.

**ANSWER:** _awaiting Brett Heap_

### R2Q20 — Amend requirement 16 and 15.1b so that a pack's check may be model-assisted? *(phase 5; FR-017)*

**Open because** #1144 as ratified already decides this: no model channel can
reach a pack.
- 15.1b *"passes exactly stdin from `/dev/null` and the two output pipes"*
  (`tasks.md:3445-3447`).
- A pack *"has NO NETWORK"* (`spec.md:552`).
- 14.4 allows model-assisted checks *"only where a model is configured"*
  (`tasks.md:3240-3241`) for the product's own families. Group 16 keeps model
  access to one provider module, `doxbench_provider.py`
  (`tasks.md:4046-4050`).

The question is whether to amend it. openxFactory's semantic and neutrality
families dispatch to models (OQ-H15-4).

- **(a) (Recommended)** Keep requirement 16 and 15.1b as ratified: pack checks
  are model-free. *Consequence:* the sandbox stays network-free. F1 ports
  openxFactory's model-dispatching families only after a later act.
- **(b)** Amend requirement 16 and 15.1b so that the engine brokers a model
  channel, through Group 16's one provider module, to packs that declare the
  need. **This changes ratified text, so you rule it as an amendment.**
  *Consequence:* F1 can port those families, but a new boundary runs through
  the sandbox, with its own containment tests.

**ANSWER:** _awaiting Brett Heap_

### R2Q21 — Is a domain's pack pinned in its `stack.yaml` or in the corpus's `health/packs.yaml`? *(phase 5; FR-016)*

**Open because** ruling `5784295745` says each DomainxFactory's pack is *"pinned
in its `stack.yaml`"*, while 15.1a says the engine loads ONLY from the corpus's
`health/packs.yaml` (`tasks.md:3404`) (OQ-H15-13). F2 is outside both releases,
but the interface fixes the shape F2 must fit.

- **(a) (Recommended)** `health/packs.yaml` is authoritative for what the engine
  runs. A domain's `stack.yaml` records the same pin for that domain's own
  governance. A lockstep check, like `scripts/verify-opendox-pin.py`, is owed by
  F2, not by release 2. *Consequence:* release 2 builds one loader, and F2 adds
  its check later.
- **(b)** The engine also reads a domain's `stack.yaml` when present.
  *Consequence:* two sources of truth for one corpus, inside the neutral
  product.

**ANSWER:** _awaiting Brett Heap_

### R2Q22 — Does openDox-spec own the health contract's schemas, with a bundle cut? *(release 2; FR-016, FR-023)*

**Open because** requirement 16's contract is one *"the product itself owns"*.
Release 2 adds three serialized artifacts, and 15.1 names only a protocol
(`tasks.md:3398-3402`):
- the exceptions file;
- `health/packs.yaml`;
- the finding's neutral shape.

Release 1's precedent put a contract in openDox-spec and cut a bundle: R1Q11
(a) and R1Q12 (a) (ruled at `tasks.md:1176`), and batch G at 9.5
(`tasks.md:1578-1596`). Batch G also made openDox-spec the arc's sixth
repository (`tasks.md:1594-1595`). This is this feature's own question.

- **(a) (Recommended)** openDox-spec owns a schema for each of the three, and the
  code leg carries digest-checked copies. Release 2 cuts ONE `dox-v1.y` minor at
  the openDox root, under a batch-G style addendum at 9.5. *Consequence:* the
  same shape as release 1, and no repository joins. openDox-spec gains three
  schemas, and the openDox root owes a second `dox-v1.y` tag.
- **(b)** The contract is the code leg's protocol and constants alone: no schema,
  and no bundle. *Consequence:* fewer acts, but a pack author reads Python, not
  a schema.

**ANSWER:** _awaiting Brett Heap_

### R2Q23 — Is release 2 published to PyPI? *(release 2's close; FR-023)*

**Open because** batch O at 9.5 (`tasks.md:1598-1615`; `5962754358`,
`5963162921`) published 0.1.0 at release 1's cut, as an exception to *"owes no
tag"*. Nothing says what release 2 owes. **Measured:** `pyproject.toml` reads
`version = "0.1.0"` at `a9ac96f9`. This is this feature's own question.

- **(a) (Recommended)** Publish `opendox` 0.2.0 at release 2's cut, under a
  batch-O style addendum.
  - It goes through the existing trusted-publishing workflow, with one tag,
    `v0.2.0`.
  - It is published on your publish word, after release 2's acceptance passes.

  *Consequence:* `pip install "opendox[local]"` brings release 2.
- **(b)** No publish. *Consequence:* PyPI users stay on 0.1.0.
- **(c)** A publish per phase (0.2.0 and 0.3.0). *Consequence:* two cuts, two
  tags and two publish words.

**ANSWER:** _awaiting Brett Heap_

### R2Q24 — Does release 2 carry an end-to-end acceptance, AT-R2? *(release 2's close; FR-024)*

**Open because** #1144's release-2 falsifiers are command-line acceptances and
named tests. 14.5's three parity tests (`tasks.md:3242-3269`) prove that the view
is served and that its action list matches the CLI's. They do not prove that a
human can complete a repair from the view. Release 1 closed on AT-R1. This is
this feature's own question.

- **(a) (Recommended)** Define AT-R2 in AT-R1's form, on a clean machine with
  only `opendox[local]`, and a plain repository:
  - the Health view lists findings, new first;
  - a mechanical repair is drafted from the view, and landed through the view's
    confirm control as a revertible merge commit;
  - an exception survives `runtime reset`;
  - a branch is submitted to a bare remote with `gh` absent.

  It runs as an HTTP half in CI and a browser half on the host. *Consequence:*
  the release is proved as a user meets it, and the plan carries two more tasks.
- **(b)** Close on #1144's falsifiers and the named tests alone. *Consequence:*
  faster, but the view's flows are proved only by parity.

**ANSWER:** _awaiting Brett Heap_

### R2Q25 — May a finding's `evidence` hold document excerpts? *(phase 5; FR-009, FR-018)*

**Open because** 14.3 says the store holds *"NO DOCUMENT"* and stays
disposable (`tasks.md:3233-3235`, RULING Q1's principle), but sets no bound on
a finding's `evidence`. 14.5 and 15.2 put `evidence` on every finding
(`tasks.md:3259-3262`, `:3459`). openxFactory's checker allows excerpts of up
to 240 characters (`scripts/doc_health/families.py:367`,
`_CITE_EXCERPT_CHARS`). So the answer is a reading of RULING Q1's boundary
(OQ-H-19).

- **(a) (Recommended)** Locators only: a path, a line, a link-target string or a
  family-defined key, and no text of a document. *Consequence:* the store
  provably holds no document (Q1, 14.3). The view shows the passage by reading
  the document from git when it renders. openXdox's follow-on governance pack
  (F1) must keep its 240-character excerpts out of `evidence`.
- **(b)** Bounded excerpts, up to a declared length such as openxFactory's 240
  characters. *Consequence:* findings read well without a second read, and F1
  ports its evidence unchanged. But the store then holds fragments of
  documents, so Q1's "no document" needs a stated bound, which is yours to
  rule.

**ANSWER:** _awaiting Brett Heap_

---

## Deferred to the plan, with proposed defaults

Design-level questions that #1144 and the rulings leave open, but whose answer
does not change WHAT the spec requires. The plan writer proposes each default
below. Brett rules them when he rules the plan, and any of them can be raised
to a ruling question on request.

| id | question | proposed default |
|---|---|---|
| OQ-12-9 | Is the CLI `submit` under the console-presence and `--actor` gate? | No. F12.2 runs it non-interactively with no actor and expects success, so #1144 already decides it. The route stays gated (12.4a). |
| OQ-12-11 | Is a credential-bearing remote pushed or refused? | Refused by name, as `attach_remote` refuses one, and the refusal is redacted (12.1a). |
| OQ-12-12 | `LocalGitSubmissions`' transport, and which remote counts | Reuse the runtime's hardened push (`repository_act.py`), factored to take a named branch. The remote is `origin`, as both existing pushes fix it. Several push URLs are refused. |
| OQ-12-13 | `land`'s HTTP surface | Two routes, one that mints the per-branch nonce and one that lands. Both sit behind 12.4a's three-clause gate and the console token. |
| OQ-12-14 | Capability flags, and where the view's controls live | `submit` reuses `session`. A new `actions.land` is true only where a lander is bound (T084's honesty rule). The controls go in a new view module, never in the `doxbench-*.js` files that FR-037's sentinels guard. |
| OQ-12-16 | Where F12.2's evidence runs, given that it needs `gh` absent | In a container, or under a PATH that hides `gh`, recorded in the evidence. |
| OQ-12-17 | Does `LandingPort` serve the fix loop's batches? | Yes. A batch is one draft branch, so `land(branch)` serves it unchanged. |
| OQ-H-2 | Which families the scoped action asks for, once openDox's check exists | The registered check names its own default scoped families, and the action asks for those when a caller names none. openxFactory's host-wiring test adapts at the pin, under `tests/domain_profile/`. |
| OQ-H-3 (plan half) | Are the scoped seam's check (Group 6) and the engine's built-in families (14) one check, and is a scoped run stored? | One neutral check: the engine's built-in families, attributed `opendox`, are what openDox registers at the scoped seam. A scoped run is not stored. Whether a host's in-process check runs beside sandboxed packs is R2Q16. |
| OQ-H-8 | The class of orphans, stale stubs, an unmovable broken link and non-derivable front matter | `human-only` for all four, so that `auto-fix` and `assisted` stay exactly the ruled lists. |
| OQ-H-10 | How a moved link target is detected | Structurally: a unique basename elsewhere in the tree is the target. An ambiguous or absent one makes the finding `human-only`. |
| OQ-H-11 | An `assisted` proposal with no model, and a near-duplicate's `path` | A deterministic proposal, a front-matter note naming the other document, which the human edits. The finding's `path` is the later-committed document of the pair. |
| OQ-H-13 | The exceptions file's schema, key, effect and path | `health/dispositions.yaml` carries `schema_version` and a product `kind`, and its entries are keyed by finding id (R2Q10) with a reason. An accepted finding is suppressed, not downgraded. A file of another kind at that path is refused by name. |
| OQ-H-14 | `accept` on a bare repository openDox created | In a checkout, it writes the working tree, as F14.1 expects. With no working tree, it writes a draft on a branch that lands through the landing rule. |
| OQ-H-15 | Whether the engine's own files are excluded from its families | Yes: `health/dispositions.yaml` and `health/packs.yaml` join the settings-document exclusion. |
| OQ-H-16 | Which documents are exempt from "nothing links to it" | Root `README` and index documents. The plan measures the `plain-documents` fixture and declares the rule. |
| OQ-H-18 | What "optionally on commit" means | On demand only, plus a documented hook line, `opendox health run --repo-root .`, which the user may add. The product writes nothing under `.git/`. |
| OQ-H-20 | Which model-assisted checks exist, and through which configuration | No built-in family is model-assisted in release 2. An `assisted` proposal uses Group 16's trusted binding, through `doxbench_provider.py` alone. |
| OQ-H-21 | Which "existing engine" finds near-duplicates | openDox's own `doxbench_knowledge` embedding with cosine. Its threshold is declared by the plan. |
| OQ-H-22 | `0003_`'s table shape (its ownership half is R2Q13) | A runs table and a findings table, keyed by the corpus's resolved root, with no foreign key to `projects` (F14.1 creates no project). |
| OQ-H15-1 | What a pack IS, and how it is invoked | A Python package that an engine-provided shim imports inside the sandbox, calling 15.1's protocol. Python is the only pack runtime in release 2. |
| OQ-H15-5 | Memory, CPU, process, tmpfs and stdout bounds | rlimits always, cgroups only where delegated, and declared defaults. A bound hit is a finding against the pack, as a timeout is. |
| OQ-H15-9 | Is the canary product behaviour, or a test hook? | A per-run self-check of the sandbox, which is product behaviour, so F15.1 stands. If Brett prefers a test hook, this becomes a ruling question, because F15.1's text changes. |
| OQ-H15-10 | A pack's declaration: a static file, or runtime output? | A static file inside the pack, read before any pack code runs. Forbidden keys (baseline, landing, classes) are refused. |
| OQ-H15-11 | stdout's wire format, and stderr | One JSON document on stdout. stderr is dropped, except a bounded tail in a failure finding. |
| OQ-H15-12 | The subtree form of `sorted-ls-tree-r-v1` for a corpus-relative source | `<commit>:<source>` with relative paths, and gitlinks inside a pack refused. Fixed before any fixture digest is committed. |
| OQ-H15-14 | Fetching a git-URL source | The engine fetches, never the pack, at `health run`, into a cache under `OPENDOX_STATE_DIR`. Offline, the entry gets a finding against it. |
| OQ-H15-15 | How pack labels enter the display facet | A health role family keyed by pack and family id, under a schema-version bump. A host profile's labels win. |
| OQ-H15-18 | The product's own `pack_version` | The installed version, as 15.7 fixes it. Each family's own version rides in the finding's evidence. |
| OQ-H15-19 | The pack-id charset, and the install-level finding's fields | `[a-z0-9-]`, unique per manifest. An install-level or pre-run finding has `pack_id` `opendox` (or the entry's id), an empty `path`, and `human-only`. |
| OQ-H15-20 | Is a pack's patch stored at `run`, or re-obtained at `fix`? | Stored with its finding at `run`, validated at `run` and again at `fix`. |
| OQ-H15-21 | Which `bwrap` binary, and which minimum version | A fixed system path, verified by the probe. The minimum version has `--json-status-fd`, `--disable-userns` and `--size`. |
| OQ-038-1 | What remedy a shown conflict names | The refusal names it: bring the default branch into the branch and resolve there. Release 2 adds no conflict verb or editor (#1144 declares none). |
| OQ-038-2 | Who ticks the arc-close boxes (9.5, 11.0, 11.1, F11.1) | This feature performs them in phases 4–5 and ticks them at the arc's close. Plan 034's T090–T093 close by reference. The archive is the holder's, and is blocked until F9.2 closes on the direction arc's landing. |

## Round 2 (after round 1's answers)

None. Every question that needs Brett fits round 1's budget, with 25 of 25
slots used.

## Where every candidate went

| candidate | went to |
|---|---|
| OQ-12-1 | R2Q2 |
| OQ-12-2 | R2Q3 (R1Q4 (a) already rules the verbs' placement) |
| OQ-12-3 | R2Q1 |
| OQ-12-4, OQ-12-5 | R2Q8 |
| OQ-12-6, OQ-12-7 | R2Q6 |
| OQ-12-8 | R2Q5 |
| OQ-12-9, -11, -12, -13, -14, -16, -17 | plan defaults |
| OQ-12-10 | R2Q4 |
| OQ-12-15 | R2Q7 |
| OQ-H-1 | R2Q9, item 1 |
| OQ-H-2, -8, -10, -11, -13, -14, -15, -16, -18, -20, -21 | plan defaults |
| OQ-H-3 | R2Q16 (the host's in-process check beside sandboxed packs); plan default (one neutral check; a scoped run is not stored) |
| OQ-H-4 | R2Q13 (with OQ-H-22's ownership half) |
| OQ-H-5 | R2Q15 |
| OQ-H-6 | R2Q9, item 2 |
| OQ-H-7 | R2Q10 |
| OQ-H-9 | R2Q11 |
| OQ-H-12 | R2Q12 |
| OQ-H-17 | R2Q14 |
| OQ-H-19 | R2Q25 |
| OQ-H-22 | plan default (shape); R2Q13 (ownership) |
| OQ-H15-2 | R2Q18 |
| OQ-H15-3 | R2Q19 |
| OQ-H15-4 | R2Q20 |
| OQ-H15-6 | R2Q15 |
| OQ-H15-7 | R2Q16 |
| OQ-H15-8 | R2Q17 |
| OQ-H15-9 | plan default (a ruling only if a test hook is preferred) |
| OQ-H15-13 | R2Q21 |
| OQ-H15-16 | R2Q12 |
| OQ-H15-17 | R2Q10 |
| OQ-H15-22 (a)–(d) | R2Q9, items 3–6 |
| OQ-H15-1, -5, -10, -11, -12, -14, -15, -18, -19, -20, -21 | plan defaults |
| this feature's own: the verb shapes' `--local` | R2Q9, item 7 |
| this feature's own: the product's checks without a sandbox | R2Q16 |
| this feature's own: openDox-spec's schemas and bundle | R2Q22 |
| this feature's own: PyPI | R2Q23 |
| this feature's own: AT-R2 | R2Q24 |
| this feature's own: the conflict remedy; the arc's close | plan defaults OQ-038-1, OQ-038-2 |
