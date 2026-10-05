# Tasks: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Input**: [`spec.md`](./spec.md), [`plan.md`](./plan.md), [`research.md`](./research.md),
[`data-model.md`](./data-model.md), [`contracts/`](./contracts/),
[`quickstart.md`](./quickstart.md), [`clarify-questions.md`](./clarify-questions.md),
and #1144's ratified `openspec/changes/add-neutral-product-standalone-operability/tasks.md`,
which holds the boxes and every falsifier.
**Lane**: `openxfactory-4` (coordinator), with lane `openXfactory-3` (peer).

**NO CODE UNTIL BRETT RULES THIS PLAN.** No task below except T001–T004 and
T006–T007 starts before T004 records his ruling of plan.md § "Design decisions
for Brett to rule with this plan".

## Format

`- [ ] T### [P?] [US#] [repo] Title`, followed by up to nine lines:

- **Realizes**: the #1144 boxes the task closes, or advances when marked
  "(part)". A box is TICKED only by T082 (bookkeeping, after AT-R2, SC-008).
- **Falsifier**: the #1144 falsifier or named test the task must pass, quoted
  in its PR (FR-025).
- **Ruled**: the answers the task carries out. Round 1, R2Q1–R2Q25, all (a):
  `#656` `6003486656` (2026-10-05), verbatim *"Accept all 25 recommended
  (Recommended)"*. The direction arc, ARC-Q1–ARC-Q4, all (a): `#656`
  `6003918488` (2026-10-05T21:59:43Z).
- **Decisions**: the plan.md decision rows the task depends on. Until T004
  records Brett's ruling of them, they are proposals, and the task does not
  start.
- **Blocked by**: none. Every behavioural question is answered (FR-025).
- **After**: tasks that must land first. `T005` means batch Q.
- **Lands with**: a task whose change rides in the same PR.
- **Files**: the files the task owns, as plan.md § "Parallel slices" orders
  them. A file another open slice owns is never edited.
- **Lane**: `4` (openxfactory-4) or `3` (openXfactory-3), as plan.md § "Two
  lanes" proposes; T009 confirms the split.

A task with no `[P]` either shares a file with a neighbour or depends on one.

- **Stories** (spec.md): US1 submit (phase 4), US2 land (phase 4), US3 the
  governed host unchanged (every phase), US4 health of one's own documents
  (phase 5), US5 the fix loop and exceptions in git (phase 5), US6 pinned,
  sandboxed packs (phase 5). Holder tasks carry no story tag.
- **Repositories**:
  - `[oDc]` opensoft/openDox-code
  - `[oXc]` opensoft/openXdox-code
  - `[oD]` opensoft/openDox (root)
  - `[oX]` opensoft/openXdox (root)
  - `[oDs]` opensoft/openDox-spec
  - `[oxF]` opensoft/openxFactory
  - `[cxF]` codeXfactory/codexFactory (merge commits only)
  - `[xF]` opensoft/xFactory (the aggregation)
- **Trailers**: realization landings carry `Arc:
  neutral-product-standalone-operability` and their lane's `Lane:` line;
  bookkeeping carries no `Arc:` (R1Q20 (a)); the direction arc's change
  carries its own value (decision ARC-4). No closing keyword in any commit
  message or PR body. Land by squash or merge, never rebase.
- **Evidence** goes to this feature's `evidence/`, `Status: record`, with no
  `Arc:` trailer.

## What can start

Brett Heap answered all 25 round-1 questions (`6003486656`) and the four
direction-arc questions (`6003918488`). This plan holds 63 design decisions
for him to rule (plan.md). Once T004 records that ruling:

- **Day one** (plan.md § "The critical path"): T005 (batch Q, the first act),
  T008, T009, T010, T011, T012 with T013 (after T008), T020–T023, T024 (H-1
  ruled), T025 (W-1 ruled for its model part), T040 and T070.
- **The long pole** is P4-F: T020 → T026 → T029 (lane 3).
- **Phase 5's openDox-code slices** start once T027 has pinned phase 4's
  openDox-code commit, if decision N-6 is ruled (a); otherwise after T033.
- **The direction arc** (T070–T077) runs beside phase 5 and gates neither
  release 2's close nor #1144's archive (ARC-Q3 (a)).
- **The publish** (T084) is LAST, on Brett's publish word after AT-R2.

---

## Phase 0: preconditions (holder)

- [ ] T001 **Claims, per slice.** Before each slice opens, its lane posts a
  `CLAIMED` on `#656` after a sibling search, naming the task ids, the files it
  owns (plan.md § "Parallel slices") and `lane X's PR #N` once it exists. Lane
  3 claims its own slices; lane 4 lands every PR. A standing act.
  - **Lane**: 4 and 3.
- [ ] T002 **Release-2 base, and the re-measure at the ruling.** Record in
  `evidence/r2-base.md`: every repository's `main` (the R0 command of
  research.md), the box census, and `PACKET_MERGE=94b6f7f1` for F11.1. Lane 3
  re-runs 12.5's composed suites at the then-current tips and quotes the red
  count against R2-INV-P4F's 174 (research.md R2), naming any node that moved.
  - **Lane**: 4 (lane 3 for the composed run).
- [ ] T003 **The independent analyze.** An independent reviewer runs
  `/speckit-analyze` over this revision (the plan writer does not). Its
  findings are dispositioned at T004, not ignored (constitution, Development
  Workflow).
  - **Lane**: 4 (holder dispatches).
- [ ] T004 [oxF] **Brett's ruling of the plan, encoded.** Put plan.md's 63
  decision rows to Brett as one block (R-1 and W-1 as the two RULINGS, H-1 and
  H-2 for confirmation, ARC-1 for him to name, the rest as proposals). Record
  his words on `#656`, then encode them in this feature's documents in one
  bookkeeping PR on this branch, which also adds the six planning documents to
  the README document index entry at `README.md:87` (Principle IV, plan.md
  Constitution Check) and dispositions T003's findings.
  - **Files**: this feature's documents; `README.md` (the entry's links only).
  - **After**: T003.
  - **Lane**: 4.
- [ ] T005 [oxF] **Batch Q: record the answers' amendments in #1144, in plan 034's T007
  form, ONE PR, under a Rule 6 window. THE FIRST ACT.** Each amended line cites
  its ruling. It amends no requirement and no scenario. It holds:
  1. **R2Q9 (a)'s seven** (`6003486656`): F6.1 builds an entry point first and
     its stale "Today" text is struck; F14.1 and F15.1 first start the document
     server, as F13.1 does; F15.1 asserts its sandbox precondition; the forking
     pack's child carries its own pack id; the corpus export cannot be steered
     by `export-subst` or `export-ignore`; the escaping pack's restore attempt
     is a write; `submit`, `land` and `health` take `--local`.
  2. **R2Q2 (a)'s note** at 12.4: the repoint sentences (`tasks.md:2513-2519`;
     `design.md:476-478`, `:1059-1061`) are the withdrawn draft's residue.
  3. **R2Q8 (a)'s line** at 12.5's falsifier: F12.1 runs composed, as F5.2 does
     under R1Q23 (a), until the direction arc's realization lands.
  4. **R2Q10 (a)'s selection lines** in F14.1 and F15.1: planted findings are
     selected by their fixture document, and `health list --json` carries `kind`.
  5. **R2Q1 (a)'s non-normative reading** of the release map's "one interface
     for both" (`tasks.md:108`; `design.md:799-800`).
  6. **ARC-Q2 (a)'s F9.1 amendment**, in batch B's form (`6003918488`):
     openXdox-code's composed files are declared integration tests with count
     and reason, and requirement 9 closes for openXdox-code by declaration.
  7. **ARC-5's note at F9.2**, in whichever form Brett rules.
  8. **12.5's falsifier notes**, if ruled: H-2's widening of batch C to pre-arc
     carve residue (`5962785556` item 1's precedent), and R-1 (a)'s admitted
     module-level kind.
  9. **A non-normative note at 15.1b** (decision N-12): a host's registered
     check is trusted code run in process, not a pack (R2Q16 (a)).
  10. **9.5's two addenda** (decision N-5): R2Q22 (a)'s batch-G style addendum
      (one more `dox-v1.y` minor carrying the three schemas), and R2Q23 (a)'s
      batch-O style addendum (`opendox` 0.2.0 at the cut, tag `v0.2.0`, on
      Brett's publish word).
  - **Realizes**: none (bookkeeping; FR-025).
  - **Falsifier**: the PR's gates against the `main` it lands on, the pinned
    `scripts/validate-openspec-cli-pin.py --all` among them.
  - **Ruled**: R2Q1, R2Q2, R2Q8, R2Q9, R2Q10, R2Q16, R2Q22, R2Q23; ARC-Q2.
  - **Decisions**: I-3, N-5, N-9, N-12, R-1, H-2, ARC-5.
  - **After**: T004.
  - **Files**: `openspec/changes/add-neutral-product-standalone-operability/tasks.md`
    (and `design.md` for item 5's addendum, if the reading needs one there).
  - **Lane**: 4.
- [x] T006 **Ask Brett the `doc_health` direction arc (R1Q6 (d)).** DONE.
  Lane openXfactory-3 prepared the ask read-only (`lane-coord-034/r2/R2-ARC-ASK.md`,
  CLAIMED on `#656` `6003715712`); Brett answered ARC-Q1–ARC-Q4 all (a),
  recorded on `#656` `6003918488` (2026-10-05T21:59:43Z). The latest point it
  could have been asked without making phase 4's checkpoint wait was the claim
  of U-9 (T029), whose composed run is F12.1; it was asked before this plan was
  ruled. Plan 034's T008 (the arc's raising) is discharged by it.
- [x] T007 **Encode the arc ruling in this plan.** DONE in this revision: plan.md
  § "Ruled answers, the `doc_health` direction arc", decisions ARC-1 to ARC-6,
  and tasks T070–T077.
- [ ] T008 [cxF] **Feature 007's four exceptions (R2Q6 (a)).** Amend codexFactory's
  `specs/007-workbench-branch-sessions/spec.md` with four named exceptions, citing
  `6003486656`: the guard's argument check (`tests/test_session_git.py:523` still
  refusing `("merge", "other-branch")`, `:563-564`'s pin moving);
  `session_git.py:93`'s stated rule; SC-002's `HEAD` clause; SC-002's
  working-tree clause. Each names the lander's own landing worktree and the
  ff-only of a clean served checkout as the only admitted moves.
  - **Ruled**: R2Q6. **Decisions**: N-8 (bookkeeping, no `Arc:`).
  - **After**: T004. Landed by a MERGE COMMIT (the repository allows no other).
  - **Files**: codexFactory `specs/007-workbench-branch-sessions/spec.md`.
  - **Lane**: 4.
- [ ] T009 **The lane split, confirmed.** Brett and the holder confirm plan.md
  § "Two lanes"; each lane records its slices in its handoff and the
  workspace's `LANES.md`; lane 3 posts its claims (T001).
  - **After**: T004.
  - **Lane**: 4 and 3.

---

## Phase 4: submission and landing (US1, US2, US3), Group 12

**Goal**: a plain repository's owner submits a branch to an attached remote and
lands a branch on `main` by ONE confirmed act; the governed flow is unchanged,
and 12.5's 16 suites run green composed.
**Independent test**: F12.2 exits 0 in an openDox-code checkout alone with `gh`
hidden; F12.1 exits 0 composed (SC-001).

### The CI owner, day one

- [ ] T010 [oDc] **R2Q17 (a)'s required-check change.** In openDox-code's
  `.github/workflows/validate.yml`, the required `validate` job: pins
  `runs-on: ubuntu-24.04`; installs bubblewrap; sets
  `kernel.apparmor_restrict_unprivileged_userns=0`; proves the sandbox LIVE in
  a step before the suite (a `bwrap` invocation that must succeed, and one
  that must be refused a write outside its tmpfs); records `bwrap --version`
  (OQ-H15-21); and exports the switch under which the future sandbox tests FAIL
  rather than skip when `CI` is set. `EXPECT_SKIPPED` stays "11" (`:306`). No
  macOS job. The move to 26.04 waits for a measurement on a runner.
  - **Realizes**: 15.1b (part), 15.5 (part, the platform).
  - **Falsifier**: the job's own run on the PR, quoted: the live proof step
    green, the suite's selected/passed/skipped counts unchanged.
  - **Ruled**: R2Q17. **Decisions**: N-4, OQ-H15-21.
  - **After**: T004.
  - **Files**: `.github/workflows/validate.yml` (first of four edits: T010 →
    T017 → T051 → T080).
  - **Lane**: 4.

### P4-A: the submission protocol and its neutral default

- [ ] T011 [P] [US1] [oDc] **`SubmissionPort`, `Submission`, `LocalGitSubmissions`,
  `NoSubmissionTarget`.** Add the protocol (`submit(branch) -> Submission`) and
  the report (data-model.md § Submission) to `session_pr.py` as NEW names,
  never touching the three classes `test_session_snapshot.py:893-916` pins.
  `LocalGitSubmissions(Path(checkout_root))` pushes to `origin` through a push
  helper factored out of `runtime/repository_act.py:1335-1372` into
  `submission_push.py`, which takes a named branch; `repository_act.py` calls
  the helper. Refuse by name: `main`; no `origin` (`NoSubmissionTarget`, 12.3);
  several push URLs; a credential-bearing URL, redacted (12.1a). Tests use a
  local bare repository as `origin`, never the network.
  - **Realizes**: 12.1, 12.1a, 12.2, 12.3.
  - **Falsifier**: F12.2's two `tests/test_submission_default.py` nodes (the
    credential node here; the server node lands with T014); the new
    `tests/test_submission_port.py`.
  - **Ruled**: R2Q1, R2Q2, R2Q5. **Decisions**: OQ-12-11, OQ-12-12.
  - **After**: T004.
  - **Files**: `src/opendox/session_pr.py` (new names only), new
    `src/opendox/submission_push.py`, `src/opendox/runtime/repository_act.py`
    (the call site only), new `tests/test_submission_port.py`, new
    `tests/test_submission_default.py`.
  - **Lane**: 4.

### P4-D1: governance, confirmation and the lander (pure)

- [ ] T012 [P] [US2] [oDc] **The landing seam.** New `landing.py`: `LandingPort`,
  `Landed`, `MergeConflict` (data-model.md), `repository_governance()` returning
  `standalone`, `governed` or `unknown`, fail closed; the declaration reader for
  `.opendox/governance.yaml` at `main`'s tip (decision N-1); a registered host
  profile's instrument outranks a declaration (R2Q4 (a)). New
  `landing_confirm.py`: the confirmation capability, bound to the branch and its
  head, single-use, with exactly two issuers (the `/dev/tty` prompt; the
  server's per-branch nonce) and a static check that no other exists. The
  neutral lander: `--no-ff` merge in a landing worktree of its own; ff-only of a
  clean served checkout on `main`; `ls-remote` check first; pushes nothing
  (R2Q6 (a)); `MergeConflict` names the remedy (OQ-038-1). A registered TEST
  host profile in the tests declares an instrument, so F12.2's host-side nodes
  run here (R2Q3 (a)). Audit every place openDox creates a repository, and pin
  `-b main` where git's `init.defaultBranch` would decide (interplay I-2).
  - **Realizes**: 12.6a (part: the seam, the query, the capability, the lander),
    12.6 (part).
  - **Falsifier**: F12.2's thirteen `tests/test_landing_guardrails.py` nodes,
    including the static issuer check.
  - **Ruled**: R2Q1, R2Q3, R2Q4, R2Q5, R2Q6, R2Q7. **Decisions**: I-1, I-2,
    N-1, N-11, OQ-12-17, OQ-038-1.
  - **After**: T004.
  - **Lands with**: T013.
  - **Files**: new `src/opendox/landing.py`, new `src/opendox/landing_confirm.py`,
    new `tests/test_landing_guardrails.py`; the repository-creation call sites
    the audit finds (named in the PR).
  - **Lane**: 4.
- [ ] T013 [US2] [oDc] **Feature 007's guard, by R2Q6 (a)'s four exceptions.**
  `session_git.py:93`'s stated rule and the guard's argument check admit the
  lander's `merge --no-ff` in its own landing worktree and the ff-only of the
  served checkout, and nothing else: `tests/test_session_git.py:523` still
  refuses `("merge", "other-branch")`; `:563-564`'s pin moves to the admitted
  forms; `:99`'s rule is restated.
  - **Realizes**: 12.6a (part).
  - **Falsifier**: `tests/test_session_git.py` whole, quoted.
  - **Ruled**: R2Q6.
  - **After**: T008.
  - **Lands with**: T012.
  - **Files**: `src/opendox/session_git.py`, `tests/test_session_git.py`.
  - **Lane**: 4.

### P4-B: the two bindings

- [ ] T014 [US1] [oDc] **`submission_factory` and `_submission_port`.** In
  `serve.py`, `submission_factory` (with its accessor and compose entry)
  defaulting to `LocalGitSubmissions`; in `cli.py`, `_submission_port`, the
  same. `pull_request_factory` and `_pull_request_port` keep `GhPullRequests`,
  serving `gate open-pr` unchanged.
  - **Realizes**: 12.4.
  - **Falsifier**: F12.2's server node in `tests/test_submission_default.py`;
    `test_session_snapshot.py:893-916` unchanged and green.
  - **Ruled**: R2Q2.
  - **After**: T011.
  - **Files**: `src/opendox/serve.py` (first phase-4 edit), `src/opendox/cli.py`
    (first), `tests/test_submission_default.py` (the server node).
  - **Lane**: 4.

### P4-C: openDox's own submit act

- [ ] T015 [US1] [oDc] **The `submit` verb, route and control.** New
  `cli_branch_actions.py` holds `submit`, contributed through `default_profile.py`
  (decision N-2) with `--local` (R2Q9 (a) item 7) and no actor gate (OQ-12-9).
  New `serve_branch_actions.py` holds `POST /actions/session/submit` behind
  12.4a's three-clause gate and the console token; `serve.py` dispatches it and
  `/capabilities` reuses `session` (OQ-12-14). New
  `web/views/branch-actions.js` holds the submit control; `web/app.js` and
  `web/index.html` wire it; the census fixture gains its rows. The hosted plane
  refuses by name. Under `governed`, `submit` goes through the host's
  contributed `SubmissionPort` and reports where the work went (R2Q4 (a)).
  `contracts/cli-http-submit-land.md` is the surface.
  - **Realizes**: 12.4a.
  - **Falsifier**: F12.2's five `tests/test_submit_route.py` nodes; CLI tests
    in `tests/test_cli_branch_actions.py`.
  - **Ruled**: R2Q1, R2Q3, R2Q4, R2Q5, R2Q9 (item 7). **Decisions**: I-1, N-2,
    OQ-12-9, OQ-12-14.
  - **After**: T014, T025 (the census fixture), T005 (the `--local` line).
  - **Files**: new `src/opendox/cli_branch_actions.py`, new
    `src/opendox/serve_branch_actions.py`, `src/opendox/default_profile.py`
    (first), `src/opendox/serve.py`, new `src/opendox/web/views/branch-actions.js`,
    `src/opendox/web/app.js`, `src/opendox/web/index.html`,
    `tests/fixtures/web_boundary_census.yaml`, `tests/test_web_boundary.py`,
    new `tests/test_submit_route.py`, new `tests/test_cli_branch_actions.py`.
  - **Lane**: 4.

### P4-D2: the landing bindings and surface

- [ ] T016 [US2] [oDc] **The `land` verb, routes and confirm control.**
  `landing_factory` in `serve.py` and `_landing_port` in `cli.py`; the `land`
  verb in `cli_branch_actions.py` (prompt over `/dev/tty`, `--local`, no bypass,
  decision N-11), contributed through `default_profile.py`; `POST
  /actions/session/land-nonce` and `POST /actions/session/land` in
  `serve_branch_actions.py` (OQ-12-13); `actions.land` in `/capabilities`, true
  only where a lander is bound; the confirm control in `branch-actions.js`. Under
  `governed` no lander is bound and `land` submits through the instrument; with
  none it refuses "governed-without-an-instrument". A live session whose branch
  lands ends by the existing merge observation (`branch_session.py`, R2Q5 (a)).
  - **Realizes**: 12.6a (part: the bindings and the surface), 12.6.
  - **Falsifier**: F12.2's guardrail nodes that drive the surface; T012's suite
    re-run green.
  - **Ruled**: R2Q1, R2Q3, R2Q4, R2Q5, R2Q6, R2Q7, R2Q9 (item 7). **Decisions**:
    I-1, N-2, N-11, OQ-12-13, OQ-12-14, OQ-12-17.
  - **After**: T015, T012, T013.
  - **Files**: `src/opendox/serve.py`, `src/opendox/cli.py`,
    `src/opendox/default_profile.py`, `src/opendox/cli_branch_actions.py`,
    `src/opendox/serve_branch_actions.py`, `src/opendox/branch_session.py`,
    `src/opendox/web/views/branch-actions.js`, `src/opendox/web/app.js`,
    `src/opendox/web/index.html`, `tests/fixtures/web_boundary_census.yaml`,
    `tests/test_web_boundary.py`, `tests/test_landing_guardrails.py` (the
    surface nodes).
  - **Lane**: 4.
- [ ] T017 [oDc] **Phase 4's CI floors.** Re-pin `MIN_SELECTED` (`:272`) and
  `MIN_PASSED` (`:273`) to the counts the phase-4 tip measures; `EXPECT_SKIPPED`
  stays 11.
  - **Falsifier**: the job's own run, quoting the three counts.
  - **After**: T011–T016, T025.
  - **Files**: `.github/workflows/validate.yml` (second edit).
  - **Lane**: 4.
- [ ] T018 [US2] [oD] **The openDox root README: the declaration, `submit` and
  `land`.** Document `.opendox/governance.yaml` (the exact file and content the
  refusal names), `submit`, and `land` (the confirmation, the merge commit, the
  `git revert -m 1` that undoes it, and that `land` pushes nothing).
  - **Ruled**: R2Q6, R2Q7. **Decisions**: N-1.
  - **After**: T016.
  - **Files**: openDox root `README.md` (first of three edits).
  - **Lane**: 4.
- [ ] T019 [US3] [oxF] **The governed host is unchanged, proved.** A host-wiring
  test under `tests/domain_profile/` with the real host registered: no lander
  bound; the host outranks a declaration; openxFactory's help golden unchanged
  (no `submit`, `land` or `health`); `/capabilities` unchanged; `_session_pull_requests()`
  still `GhPullRequests`.
  - **Realizes**: 12.5 (part, rows 10 and 11), 12.4 (part).
  - **Falsifier**: the new test, and `tests/ideation-dashboard/test_extension_point_parity.py`
    unchanged and green, at T030's pins.
  - **Ruled**: R2Q2, R2Q3. **Decisions**: N-2.
  - **Lands with**: T030.
  - **Files**: a new test under openxFactory `tests/domain_profile/` (a HOST_TESTS
    surface of 11.1).
  - **Lane**: 4.

### P4-F: the governed set runnable and green (12.5), lane openXfactory-3's repair map

R2Q8 (a): F12.1 runs composed; the 174 reds are repaired WITHOUT editing the 16
suites except through allow-list entries. Every node is mapped in R2-INV-P4F
§ "The map" and part-oneoffs; the slices are its § "Slice outline". Every
landing that edits one of the 16 adds its entry in the same PR; at the end the
oracle (`protected_suites.py`, T059 of plan 034) prints `ok: … each entered and
holding`.

- [ ] T020 [P] [US3] [oXc] **U-1, host registration (HR).** A governed-suite list
  beside `HOST_PLANE_SUITES` with its own guard (`tests/conftest.py:533-578`'s
  pattern) registers the governed host for the suites that need it; openxFactory's
  composite is registered only in the composed run, guarded as `:413-421`'s
  composed-only registration is. Finishes host-reg 62 (59 alone), one-off Group
  H 7 and Group T's second cause, and the host half of the 4 `cmd_gate_*` nodes.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the composed run of the named nodes (R2-INV-P4F § host-reg;
    part-oneoffs § Group H), quoted.
  - **Ruled**: R2Q8. **Decisions**: P4F-5.
  - **After**: T004.
  - **Files**: openXdox-code `tests/conftest.py` (first: T020 → T073 → T074),
    `tests/test_host_plane.py`.
  - **Lane**: 3.
- [ ] T021 [P] [US3] [oXc] **U-2, gate-contract schemas (GA).** Place the
  schema `gate_console` reads where it reads it: the receipt schema vendored from
  openxFactory's `contracts/schemas/` with its digest under `copies.yaml`.
  Finishes schema 16 (including `test_execution_receipt_releases_cleanup_for_the_exact_destination`).
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 16 schema nodes, composed, quoted.
  - **Ruled**: R2Q8. **Decisions**: P4F-4.
  - **After**: T004.
  - **Files**: openXdox-code `src/openxdox/gate_console.py` (first: T021 → T074),
    `src/openxdox/contracts/schemas/`, `src/openxdox/contracts/copies.yaml`.
  - **Lane**: 3.
- [ ] T022 [P] [US3] [oXc] **U-3, runbook placement (RP).** A digest-checked copy
  of the session runbook where the suites read it. Finishes moved-name runbook 10.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 10 nodes, composed, quoted.
  - **Ruled**: R2Q8. **Decisions**: P4F-3.
  - **After**: T004.
  - **Files**: openXdox-code `docs/ideation-dashboard-session-runbook.md` and its
    `copies.yaml` row.
  - **Lane**: 3.
- [ ] T023 [P] [US3] [oXc] **U-4, `swb-session.js` (SF).** Fix the two one-off
  Group J nodes (`test_session_confinement.py`) in the view module the carve's S5
  respelled; no protected edit.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 2 nodes, composed, quoted.
  - **Ruled**: R2Q8.
  - **After**: T004.
  - **Files**: openXdox-code `src/openxdox/web/views/swb-session.js`.
  - **Lane**: 3.
- [ ] T024 [P] [US3] [oXc] **U-5, the shim (SF), if H-1 is confirmed.** New
  `scripts/ideation_dashboard/session_git.py` (`import sys; from opendox import
  session_git as _m; sys.modules[__name__] = _m`), so `LOCK_HOLDER`
  (`test_session_transaction.py:296`) resolves. Finishes one-off Group L 3 and
  Group T's first cause.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 4 nodes, composed, quoted; `test_dependency_direction.py`
    green (it does not scan `scripts/`).
  - **Ruled**: R2Q8. **Decisions**: H-1.
  - **After**: T004.
  - **Files**: openXdox-code new `scripts/ideation_dashboard/session_git.py`.
  - **Lane**: 3.
- [ ] T025 [P] [US3] [oDc] **U-6, openDox web (SF; DJ (A) if W-1 rules it).**
  S1's two nodes (plan 034's T102 follow-on in `staging-workbench.js` and the census);
  and, under W-1 (A), `staging-workbench-model.js` made import-free again by
  inlining what it takes from `./display.js`, which clears the 32 DJ nodes and
  the import-free pins `:802` and `:1286`. Under W-1 (A′), the model is untouched
  and T026 owns `tests/opendox_bundle.py` instead.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: openDox-code's whole suite; the 34 nodes, composed, quoted
    at T029.
  - **Ruled**: R2Q8. **Decisions**: W-1.
  - **After**: T004.
  - **Files**: openDox-code `src/opendox/web/views/staging-workbench.js`,
    `src/opendox/web/views/staging-workbench-model.js`,
    `tests/fixtures/web_boundary_census.yaml` (first: T025 → T015 → T016 → T057).
  - **Lane**: 3.
- [ ] T026 [US3] [oXc] **U-7, the allow-list (AL; R-1's admitted part).** One
  entry per admitted test in `tests/protected_suite_respellings.yaml`, chained by
  blob, each in the same PR as its protected edit: `cmd_gate_*` 7, `hosted_index`
  3, share paths 2, Group W 1, Group S2 4 (17, under H-2); and, if R-1 (a) is
  ruled, the admitted module-level edits to `_CREATE_HARNESS` (`:492-553`),
  `_SESSION_HARNESS` (`:1008-1094`), `:1291` and `:1333`, with
  `protected_suites.py`'s `_inside_the_test` rule amended to admit the new kind.
  Under W-1 (A′), `tests/opendox_bundle.py` flattens the `./display.js` import.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the oracle prints `ok: … each entered and holding`; the
    nodes, composed, quoted.
  - **Ruled**: R2Q8. **Decisions**: H-2, R-1, W-1.
  - **After**: T020 (it unmasks 3), T005 (batch C's widened scope).
  - **Files**: openXdox-code `tests/protected_suite_respellings.yaml` (its only
    phase-4 writer), `tests/test_session_gates.py`, `tests/test_session_verbs.py`,
    `tests/test_session_confinement.py`, `tests/test_doxbench_share.py`,
    `tests/test_staging_workbench.py`, `tests/protected_suites.py` (R-1 (a)
    only), `tests/opendox_bundle.py` (W-1 (A′) only).
  - **Lane**: 3.

### Phase 4's pins (9.5) and the composed run

- [ ] T027 [oD] **Phase 4's openDox root pin (steps 1–2).** ONE commit moves the
  `code` gitlink, `contracts/code-pin.yaml` (`commit:`, `digests.tree_sha256`) and
  any workflow `@sha` naming the leg, to openDox-code's phase-4 tip; `make pins`.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins`, quoted.
  - **After**: T010–T017, T025; T018 rides in the same PR or lands first.
  - **Files**: openDox root `code` gitlink, `contracts/code-pin.yaml`.
  - **Lane**: 4.
- [ ] T028 [oXc] **U-8, step 3: openXdox-code's `opendox` pin.** `pyproject.toml`'s
  `opendox @ …@<sha>` moves to THE SAME openDox-code commit T027 pins.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: F9.2's pin assertion block (the installed `direct_url.json`
    commit equals the pin), quoted.
  - **After**: T027.
  - **Files**: openXdox-code `pyproject.toml` (first: T028 → T063 → T074 if ARC-6
    needs it).
  - **Lane**: 4.
- [ ] T029 [US3] [oXc] **U-9, the composed run, permanent (F12.1).** Add
  `.github/workflows/composed.yml` to openXdox-code: it checks out openxFactory at
  the commit `tests/composed_host_pin.yaml` names (`schema_version`, `kind`),
  installs openDox at the pin, and runs 12.5's 16 suites with
  `PYTHONPATH="$OPENXFACTORY/scripts"`, then the oracle. It is required on
  `main` from this landing (decision N-7). openXdox-code's help-tree goldens are
  asserted unchanged in the same run (R2Q3 (a)).
  - **Realizes**: 12.5, F12.1 (both ticked at T082).
  - **Falsifier**: F12.1 (12.5's falsifier, as batch Q's line amends it): 16
    suites, 0 red; the oracle's `ok: … each entered and holding`, quoted.
  - **Ruled**: R2Q8; ARC-Q2 (permanent). **Decisions**: N-7, R-1.
  - **After**: T020–T026, T028.
  - **Files**: openXdox-code new `.github/workflows/composed.yml` (first: T029 →
    T073 → T074), new `tests/composed_host_pin.yaml`.
  - **Lane**: 3.
- [ ] T030 [US3] [oX] [oxF] **U-8, steps 5–6: phase 4's consumer pins.** The
  openXdox root moves its `code` gitlink and `code-pin.yaml` to openXdox-code's
  tip, and `contracts/opendox-pin.yaml` to T027's root commit. Then ONE
  openxFactory PR: the `openDox` gitlink with `contracts/opendox-pin.yaml` in one
  commit, the `openXdox` gitlink with `contracts/openxdox-pin.yaml` in another,
  T019's test, and the phase's `edits[].note`s (T092). Then
  `tests/composed_host_pin.yaml` advances to this landing, in an openXdox-code
  PR of its own. The aggregation's routine pin-sync follows (T090 step 7).
  - **Realizes**: 9.5 (part), 11.1 (part).
  - **Falsifier**: `make pins` (openXdox root); `scripts/verify-opendox-pin.py`
    and `scripts/verify-openxdox-pin.py`; openxFactory's required checks green
    (SC-005).
  - **After**: T029.
  - **Lands with**: T019.
  - **Files**: openXdox root pins; openxFactory gitlinks and pin files;
    openXdox-code `tests/composed_host_pin.yaml` (after).
  - **Lane**: 4.
- [ ] T031 [US1] [US2] [oxF] **F12.2's evidence.** Run F12.2 (as batch Q
  amends it) in an openDox-code checkout alone at T027's pinned commit, under a
  PATH that hides `gh` (`command -v gh` empty, recorded), and quote all twenty
  named nodes. `evidence/f12.2-run.md`.
  - **Realizes**: F12.2 (ticked at T082).
  - **Falsifier**: F12.2, exit 0.
  - **Decisions**: OQ-12-16.
  - **After**: T027, T005.
  - **Lane**: 4.
- [ ] T032 [US3] [oxF] **F12.1's evidence, and phase 4's interim F11.1.** Quote
  T029's composed run at the pins T030 landed, and run F11.1 by T093's procedure
  (`PACKET_MERGE=94b6f7f1`). `evidence/f12.1-run.md`, `evidence/f11.1-phase4.txt`.
  - **Realizes**: F12.1 (ticked at T082); F11.1 (interim).
  - **Falsifier**: F12.1 exit 0; F11.1 prints `requirement 1 holds`.
  - **After**: T029, T030.
  - **Lane**: 4.
- [ ] T033 [oxF] **Phase 4 checkpoint.** `evidence/checkpoint-phase4.md` quotes
  F12.2, F12.1, the oracle and the interim F11.1 (SC-001, SC-003), names every
  phase-4 landing by repository, and records any node that moved since T002.
  - **After**: T031, T032, T005.
  - **Lane**: 4.

---

## Phase 5: health (US4, US5, US6), Groups 6, 14 and 15

**Goal**: every local install gets health over its own documents; repairs are
drafts on branches that land only through `land`; exceptions live in git;
packs are pinned and run only in a live sandbox.
**Independent test**: F6.1, F14.1 and F15.1 exit 0 as batch Q amends them, F15.1
inside the required `validate` job with the sandbox proved live (SC-002).

Lane openXfactory-3's outline (R2-INV-HEALTH Part 12) in seven waves. Its W0
(R-0, the rulings) is T004; its G15-I1 is split between T010 (day one) and
T051; its HA-9 shrinks to a proof inside T064 (decision N-2). Phase-5
openDox-code slices start after T027 under decision N-6 (a), else after T033.

### W1

- [ ] T040 [P] [oDs] **The three health schemas (R2Q22 (a)).** Author in
  openDox-spec, from this feature's `contracts/`: the finding's neutral shape
  (`health-finding.md`), `health/packs.yaml` (`health-packs-manifest.md`) and the
  exceptions file (`health-exceptions.md`), in that repository's schema layout.
  - **Realizes**: 15.1, 15.1a, 14.8 (part: the contracts).
  - **Falsifier**: openDox-spec's own validation, quoted.
  - **Ruled**: R2Q10, R2Q22, R2Q25. **Decisions**: N-3, N-13, OQ-H-13, OQ-H15-5, -10, -12, -19.
  - **After**: T004.
  - **Lane**: 4.
- [ ] T041 [P] [US4] [oDc] **U-0, the contract module's finding vocabulary.**
  New stdlib-only `src/opendox/health_contract.py`: the classes `auto-fix`,
  `assisted`, `human-only`; the severities; the finding shape with `pack_id`
  and `pack_version`; the id rule (decision N-13); the locator-only evidence
  rule (R2Q25 (a)); a digest-checked copy of T040's finding schema; a closure
  test that the module imports only the standard library.
  - **Realizes**: 14.6 (part: spellings), 15.2 (part: shape).
  - **Falsifier**: new `tests/test_health_contract.py`.
  - **Ruled**: R2Q10, R2Q18, R2Q25. **Decisions**: N-3, N-13, OQ-H15-19.
  - **After**: T040 (the schema), T027 or T033 (N-6).
  - **Files**: new `src/opendox/health_contract.py` (first: T041 → T045), its
    schema copy, new `tests/test_health_contract.py`.
  - **Lane**: 4.
- [ ] T042 [P] [US4] [oDc] **HA-1, the store (`0003_`), one owner.** New
  `migrations/0003_health.sql`: `health_runs` and `health_findings`
  (data-model.md), with 15.7's `pack_id`/`pack_version` NOT NULL and the `patch`
  column from the first landing; DOMAIN tables in `runtime/identity.py`'s
  `TABLES`, and the closure test reads `0001` with `0003_`, in the same change
  (R2Q13 (a)); `runtime/cli.py`'s `DROP_ORDER` and reset wording; the three
  role-init files; the `tests_runtime/` suites that hard-code `["0001","0002"]`
  (`test_schema_shape.py`, `test_migrations_apply.py`, `test_bundled_postgres.py`,
  `test_runtime_cli.py`, `test_deploy_shape.py`); new `runtime/health_store.py`
  (no document stored, 14.3); the hosted plane migrates the schema (R2Q15 (a)).
  - **Realizes**: 14.1, 14.2, 14.3, 15.7 (part: the columns).
  - **Falsifier**: new `tests_runtime/test_health_store.py`, carrying
    `test_the_store_refuses_a_finding_without_provenance`; the five suites above.
  - **Ruled**: R2Q13, R2Q15, R2Q25. **Decisions**: OQ-H-22, OQ-H15-18, -20.
  - **After**: T027 or T033 (N-6).
  - **Files**: as listed (single owner of `0003_` and of the five `tests_runtime/` suites).
  - **Lane**: 4.
- [ ] T043 [P] [US4] [oDc] **HA-3, `tests/fixtures/health-corpus`.** A small
  corpus with ONE planted instance per family and class F14.1 names
  (`broken-link`, `derivable-front-matter`, `stage-location-mismatch`,
  `near-duplicate`, a `human-only` finding, an accepted finding); measure the
  `plain-documents` fixture and declare the inbound-link exemption (OQ-H-16).
  - **Realizes**: 14.9.
  - **Falsifier**: new `tests/test_health_corpus_fixture.py`.
  - **Decisions**: OQ-H-8, OQ-H-16.
  - **After**: T027 or T033 (N-6).
  - **Files**: `tests/fixtures/health-corpus/**` (single owner), the test.
  - **Lane**: 4.

### W2

- [ ] T044 [US4] [oDc] **HA-2, the neutral families (detection).** New
  `src/opendox/health/families.py`: broken links (moved targets detected
  structurally, OQ-H-10), orphans (README and index exempt, OQ-H-16), stale
  stubs, derivable front matter, `stage-location-mismatch` by the six role keys'
  top-level directories (R2Q11 (a)), near-duplicates (OQ-H-21: measure whether
  `doxbench_knowledge` runs with no binding; set and record the threshold); the
  classes per OQ-H-8; the engine files excluded (OQ-H-15). Model-free (OQ-H-20).
  - **Realizes**: 14.4 (part: detection), 6.2 (part: the check's body).
  - **Falsifier**: new `tests/test_health_families.py`, over T043's corpus.
  - **Ruled**: R2Q11, R2Q14. **Decisions**: OQ-H-8, -10, -11, -15, -16, -20, -21.
  - **After**: T041, T043.
  - **Files**: new `src/opendox/health/__init__.py`, `src/opendox/health/families.py`,
    the test.
  - **Lane**: 4.
- [ ] T045 [P] [US6] [oDc] **G15-A, the pack contract.** Extend
  `health_contract.py` with the pack protocol: the static declaration
  `opendox-pack.yaml` (read before any pack code runs; forbidden keys refused),
  the one-JSON-document stdout format, and the patch type. Python is the only
  pack runtime.
  - **Realizes**: 15.1, 15.2.
  - **Falsifier**: new `tests/test_check_pack_contract.py`.
  - **Ruled**: R2Q18, R2Q20. **Decisions**: N-3, OQ-H15-1, -10, -11.
  - **After**: T041.
  - **Files**: `src/opendox/health_contract.py` (second, appended), the test.
  - **Lane**: 3.

### W3

- [ ] T046 [US4] [oDc] **HA-5, the engine, the baseline and `health run|list`.**
  New `health/engine.py` and `health/baseline.py`: runs read the committed tree
  of `HEAD` (decision N-10); the built-in families in process, attributed
  `opendox`; the baseline classes and disappearance rules of R2Q12 (a), with
  interplay I-2's no-`main` behaviour; the engine hook G15-E calls. New
  `health/cli.py`: the `health` group with `run`, `list`, `fix`, `accept` parsed
  and frozen (`--pack`, `--timeout`, `--local`, `--json`, `--class`), `fix` and
  `accept` dispatching to T053's and T054's modules; contributed through
  `default_profile.py` (decision N-2); `--json` carries `kind`. The hosted plane
  refuses by name (R2Q15 (a)). Record the hook line for the root README (OQ-H-18).
  - **Realizes**: 14.4 (part: on demand, the baseline), 14.5 (part: CLI run/list).
  - **Falsifier**: new `tests/test_health_cli.py`, `tests_runtime/test_health_engine.py`.
  - **Ruled**: R2Q9 (items 2, 7), R2Q10, R2Q12, R2Q15. **Decisions**: I-2, N-2,
    N-10, OQ-H-18.
  - **After**: T042, T044.
  - **Files**: new `src/opendox/health/engine.py`, `baseline.py`, `cli.py` (first:
    T046 → T053 → T054); `src/opendox/cli.py` (third phase-4/5 edit);
    `src/opendox/default_profile.py` (third); the tests.
  - **Lane**: 4.
- [ ] T047 [P] [US6] [oDc] **G15-B, the manifest and the pin.** New
  `check_pack_manifest.py` reads `health/packs.yaml` (`contracts/health-packs-manifest.md`),
  reserves the id `opendox`, computes `sorted-ls-tree-r-v1` over
  `<commit>:<source>` (fixed before any fixture digest is committed), fetches
  git sources into `OPENDOX_STATE_DIR` at `health run`, and refuses by name.
  Digest-checked copy of T040's manifest schema.
  - **Realizes**: 15.1a, 15.7 (part: the reserved id).
  - **Falsifier**: new `tests/test_check_pack_manifest.py`.
  - **Ruled**: R2Q18, R2Q21, R2Q22. **Decisions**: OQ-H15-12, -14, -19.
  - **After**: T045, T040.
  - **Files**: new `src/opendox/check_pack_manifest.py`, its schema copy, the test.
  - **Lane**: 3.
- [ ] T048 [P] [US6] [oDc] **G15-C, the sandbox runner.** New
  `check_pack_sandbox.py` and `check_pack_shim.py`: `bwrap` at a fixed path with
  the version floor; the probe; the per-run canary (product behaviour,
  OQ-H15-9); the exported tree only (R2Q19 (a)); no network; rlimits always,
  cgroups where delegated, `--size` tmpfs, the stdout cap; the bounds' defaults
  fixed after running the pack corpus under them (OQ-H15-5); a forking pack's
  child carries its own pack id; the export cannot be steered by
  `export-subst`/`export-ignore`; a restore attempt is a write (R2Q9 (a)). With
  no live sandbox, no pack runs and one install-level finding says why. Under
  `CI` the sandbox tests FAIL rather than skip (T010's switch).
  - **Realizes**: 15.1b, 15.6 (part: enforcement), 15.5 (part).
  - **Falsifier**: new `tests/test_check_pack_sandbox.py`, run in the required
    job with the sandbox live; `EXPECT_SKIPPED` still 11.
  - **Ruled**: R2Q9 (items 3–6), R2Q16, R2Q17, R2Q19. **Decisions**: OQ-H15-5,
    -9, -21.
  - **After**: T045, T010.
  - **Files**: new `src/opendox/check_pack_sandbox.py`, `check_pack_shim.py`, the
    test; `pyproject.toml` only if package data is needed (first: T048 → T055 → T061).
  - **Lane**: 3.
- [ ] T049 [P] [US6] [oDc] **G15-D, the patch validator.** New `check_pack_patch.py`:
  a patch touches only its finding's own document, applies to its `base_blob`,
  and is validated at `run` and again at `fix`, BEFORE any branch exists.
  - **Realizes**: 15.2a.
  - **Falsifier**: new `tests/test_check_pack_patch.py`.
  - **Decisions**: OQ-H15-20.
  - **After**: T045.
  - **Files**: new `src/opendox/check_pack_patch.py`, the test.
  - **Lane**: 3.
- [ ] T050 [P] [US6] [oDc] **G15-H, the display facet's health roles.** A health
  role family keyed by pack and family id, under a schema-version bump; a host
  profile's labels win; labels render as text.
  - **Realizes**: 15.3.
  - **Falsifier**: the display-facet tests, extended.
  - **Decisions**: OQ-H15-15.
  - **After**: T027 or T033 (N-6).
  - **Files**: `src/opendox/display_profile.py`, `src/opendox/web/views/display.js`,
    their facet tests (single owner).
  - **Lane**: 4.
- [ ] T051 [oDc] **Phase 5's CI floors, once per wave.** Re-pin `MIN_SELECTED`
  and `MIN_PASSED` after each wave's landings; `EXPECT_SKIPPED` stays 11.
  - **After**: each wave's last openDox-code landing.
  - **Files**: `.github/workflows/validate.yml` (third edit).
  - **Lane**: 4.

### W4

- [ ] T052 [US4] [oDc] [oxF] **HA-4, Group 6 at the seam (and F6.1).** Register
  the engine's built-in families, attributed `opendox`, at
  `run_scoped_doc_health` (`workbench.py:1542-1557`), with the registered
  check's default scoped families asked for when a caller names none; a scoped
  run is not stored; a host's check registered through `register_health_check`
  runs in process there only. Registration lines in `cli.py` and `serve.py`.
  openxFactory's `tests/domain_profile/test_openxfactory_host_wiring.py` adapts
  at T064's pin (an arc landing on 11.1's surface). At the tick, record 6.1's
  re-measure (38 modules; `lines.py` and `fs_probe.py`, research.md R4) and
  6.1a's vacuous satisfaction (R2Q14 (a)).
  - **Realizes**: 6.1, 6.1a, 6.2, F6.1.
  - **Falsifier**: F6.1 as batch Q amends it (an entry point built first);
    new `tests/test_health_check_seam.py`.
  - **Ruled**: R2Q9 (item 1), R2Q14, R2Q16. **Decisions**: OQ-H-2, OQ-H-3.
  - **After**: T044, T046, T005.
  - **Files**: `src/opendox/workbench.py` (single owner), `src/opendox/cli.py`
    (fourth), `src/opendox/serve.py` (fourth), the test; openxFactory's host-wiring
    test rides T064.
  - **Lane**: 4.
- [ ] T053 [US5] [oDc] **HA-6, the fix loop.** New `health/applier.py`: `fix`
  writes `health-fix-<id>` (or one batch branch) and never `main`; `auto-fix`
  applies the family's or the validated pack patch; `assisted` writes the
  deterministic proposal (OQ-H-11); `human-only` is refused with no branch; the
  draft lands only through `land` (T016; OQ-12-17). `fix`'s dispatch line in
  `health/cli.py`.
  - **Realizes**: 14.6, 14.7.
  - **Falsifier**: new `tests/test_health_fix.py` (F14.1's fix loop, by fixture
    document, R2Q10 (a)).
  - **Ruled**: R2Q5, R2Q10, R2Q11. **Decisions**: OQ-H-8, -10, -11, OQ-12-17.
  - **After**: T046, T049, T016.
  - **Files**: new `src/opendox/health/applier.py`, `src/opendox/health/cli.py`
    (second), the test.
  - **Lane**: 4.
- [ ] T054 [US5] [oDc] **HA-7, exceptions in git.** New `health/exceptions.py`
  reads and writes `health/dispositions.yaml` (`contracts/health-exceptions.md`;
  digest-checked copy of T040's schema); suppresses, never downgrades; refuses
  another `kind` by name; `accept` writes the working tree in a checkout and a
  draft branch with none (OQ-H-14); the engine files join the settings-document
  exclusion (OQ-H-15). `accept`'s dispatch line in `health/cli.py`.
  - **Realizes**: 14.8.
  - **Falsifier**: new `tests/test_health_accept.py`; a reset-survival test in
    `tests_runtime/` (an exception survives `runtime reset`).
  - **Ruled**: R2Q10, R2Q22. **Decisions**: OQ-H-13, -14, -15.
  - **After**: T046, T040; T053 (the shared `health/cli.py`).
  - **Files**: new `src/opendox/health/exceptions.py`, its schema copy,
    `src/opendox/health/cli.py` (third), the tests.
  - **Lane**: 4.
- [ ] T055 [P] [US6] [oDc] **G15-G, `tests/fixtures/pack-corpus`.** T043's
  `health-corpus`, plus `packs/` (a well-behaved pack, and one each that writes,
  connects, reads outside the export, forks, hangs, babbles, crashes and tries a
  restore) and `health/packs.yaml` with their digests.
  - **Realizes**: 15.6a.
  - **Falsifier**: new `tests/test_pack_corpus_digests.py`.
  - **Decisions**: OQ-H15-12.
  - **After**: T043, T045, T047.
  - **Files**: `tests/fixtures/pack-corpus/**`, the test; `pyproject.toml` only if
    package data is needed (second).
  - **Lane**: 3.
- [ ] T056 [US6] [oDc] **G15-E, the engine integration.** New
  `check_pack_engine.py`, called from T046's hook: runs each manifest entry in the
  sandbox, stamps `pack_id`/`pack_version`, stores the patch, turns a crash,
  timeout, bound hit, bad stdout or refused output into a finding against that
  pack, and keeps the view, the classes, the baseline and the landing rule the
  engine's (15.4). Owns nothing of Group 14's.
  - **Realizes**: 15.4, 15.5 (part), 15.6, 15.7 (part: stamping).
  - **Falsifier**: new `tests/test_check_pack_engine.py`.
  - **Ruled**: R2Q16, R2Q18, R2Q21. **Decisions**: OQ-H15-11, -18, -19, -20.
  - **After**: T046, T042, T047, T048, T049.
  - **Files**: new `src/opendox/check_pack_engine.py`, the test.
  - **Lane**: 3.
- [ ] T059 [oxF] **A display-facet follow-on, only if measured.** If T050's
  schema-version bump moves an openxFactory facet test at T064's pin, land a
  non-arc act in plan 034's T066 both-pins form (no `Arc:` trailer) before T064.
  Otherwise record "not needed" with the measurement.
  - **After**: T050.
  - **Lane**: 4.

### W5

- [ ] T057 [US4] [US5] [oDc] **HA-8, the Health view and parity.** New
  `web/views/health.js` and `health-model.js`: findings new first, passages read
  from git at render time, labels as text; every action the CLI has. New
  `health/routes.py` (`contracts/cli-http-health.md`); `serve.py` dispatches them
  and `/capabilities` gains the `health` block; the hosted plane refuses by
  name. Wiring in `web/app.js` and `web/index.html`; census rows.
  - **Realizes**: 14.5.
  - **Falsifier**: `tests/test_health_parity.py`'s three named tests
    (`test_the_health_view_is_served`, `test_every_view_action_has_a_cli_verb`,
    `test_every_cli_verb_is_offered_by_the_view`); a test that pack labels
    render as text.
  - **Ruled**: R2Q15, R2Q25. **Decisions**: OQ-H15-15.
  - **After**: T046, T053, T054, T050, T056.
  - **Files**: new `src/opendox/web/views/health.js`, `health-model.js`, new
    `src/opendox/health/routes.py`, `src/opendox/serve.py` (fifth),
    `src/opendox/web/app.js`, `src/opendox/web/index.html`,
    `tests/fixtures/web_boundary_census.yaml`, `tests/test_web_boundary.py`,
    new `tests/test_health_parity.py`.
  - **Lane**: 4.
- [ ] T058 [US6] [oDc] **G15-I2, F15.1's 24 named nodes.** New
  `tests/test_check_packs.py` holding the falsifier's 24 nodes as batch Q amends
  them (the document server started first, the sandbox precondition asserted,
  selection by fixture document), run in the required job.
  - **Realizes**: 15.5, F15.1 (part: the nodes).
  - **Falsifier**: F15.1's pytest line, inside `validate`, sandbox live.
  - **Ruled**: R2Q9, R2Q10, R2Q17.
  - **After**: T047, T048, T049, T055, T056, T005.
  - **Files**: `tests/test_check_packs.py` (single owner).
  - **Lane**: 3.

### W6: the cut's openDox-code and pins, evidence, checkpoint

- [ ] T060 [oDs] [oD] **The spec pin and the `dox-v1.y` minor (R2Q22 (a)).** The
  openDox root's spec pin moves to the openDox-spec commit holding T040's three
  schemas (as T041, T047 and T054 copied them, unchanged since), then the root
  cuts ONE more `dox-v1.y` minor bundle under batch Q's batch-G style addendum.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: the root's own bundle checks, quoted; the three copies'
    digests equal the bundle's.
  - **Ruled**: R2Q22. **Decisions**: N-5.
  - **After**: T041, T047, T054 (the three copies), T005.
  - **Lane**: 4.
- [ ] T061 [oDc] **The release step: 0.2.0.** Bump openDox-code's version to
  0.2.0, the LAST package-changing openDox-code landing before T062 (plan
  034's T101 form).
  - **Ruled**: R2Q23.
  - **After**: every package-changing phase-5 openDox-code landing (T041–T058),
    and T072 if decision ARC-6 (a) holds.
  - **Files**: `pyproject.toml` (third, last).
  - **Lane**: 4.
- [ ] T062 [oD] **Phase 5's openDox root pin (steps 1–2).** As T027, to T061's
  commit (P), in ONE commit; the root README gains the `health` section and its
  hook line (OQ-H-18).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins`.
  - **After**: T060, T061.
  - **Files**: openDox root pins; `README.md` (second edit).
  - **Lane**: 4.
- [ ] T063 [oXc] **Step 3, and 12.5 still green.** openXdox-code's `opendox @`
  pin to P; the composed workflow re-runs 12.5's 16 suites green (US3: every
  phase).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: F12.1, composed, at P.
  - **After**: T062.
  - **Files**: openXdox-code `pyproject.toml` (second).
  - **Lane**: 4.
- [ ] T064 [US3] [oX] [oxF] **Steps 5–6: phase 5's consumer pins and host
  wiring.** As T030, carrying T052's host-wiring test adaptation, phase 5's
  `edits[].note`s, and the proof that openxFactory's help golden and
  `/capabilities` are unchanged (inventory HA-9's place; decision N-2). Then
  `tests/composed_host_pin.yaml` advances.
  - **Realizes**: 9.5 (part), 11.1 (part).
  - **Falsifier**: the pin verifiers; openxFactory's required checks green (SC-005).
  - **After**: T063, T059.
  - **Lane**: 4.
- [ ] T065 [US4] [US5] [US6] [oxF] **Phase 5's evidence.** Run F6.1, F14.1 and
  F15.1 as batch Q amends them, at P, and quote them; F15.1 in the required job
  with the sandbox live; the interim F11.1 (T093). `evidence/f6.1-run.md`,
  `f14.1-run.md`, `f15.1-run.md`, `f11.1-phase5.txt`.
  - **Realizes**: F6.1, F14.1, F15.1 (ticked at T082); F11.1 (interim).
  - **After**: T064, T005.
  - **Lane**: 4.
- [ ] T066 [oxF] **Phase 5 checkpoint.** `evidence/checkpoint-phase5.md` quotes
  T065's runs and T063's composed run (SC-002, SC-003).
  - **After**: T065.
  - **Lane**: 4.

---

## Beside phase 5: the `doc_health` direction arc's realization (ARC-Q1–ARC-Q4)

Ruled on `#656` `6003918488`. Its OWN OpenSpec change, owned by lane
openxfactory-4 under this plan; it gates neither release 2's close nor #1144's
archive (ARC-Q3 (a)); F12.1 stays composed until it lands. Its realization
landings carry the change's own trailer value (decision ARC-4), not #1144's.

- [ ] T070 [oxF] **Author the change.** `openspec/changes/<ARC-2>/`: `proposal.md`
  with `code_surface:` naming openXdox-code, openDox-code and openxFactory host
  wiring and `target_release:` as Brett names it (ARC-1); `design.md` (the eight
  modules, fact 1 of R2-ARC-ASK; the seams; the re-authored `lines` slice; the 7
  respelled tests; F9.2's three removals); `tasks.md`; `.openspec.yaml`
  (`skip_specs: true`, or an openXdox-spec delta if the seams need contract
  text, ARC-3); the README "OpenSpec Records" bullet; the corpus-ledger row.
  Validated through the pinned CLI entrypoint. Under a Rule 6 window.
  - **Ruled**: ARC-Q1, ARC-Q3. **Decisions**: ARC-1, ARC-2, ARC-3, ARC-4.
  - **After**: T004.
  - **Lane**: 4.
- [ ] T071 [oxF] **Brett's ratify word, and its record.** Put the change to
  Brett; record his word on `#656` and the change's ratification record, under a
  Rule 6 window. No realization slice starts before it.
  - **After**: T070.
  - **Lane**: 4.
- [ ] T072 [oDc] **Re-author the generic `lines` slice in openDox-code.** A small
  stdlib module carrying `split_keepends`, `join_rows` and the few git reads
  `RealGit` gives the generator; nothing is relocated out of openxFactory
  (R2Q14 (a), 11.1).
  - **Falsifier**: the module's own tests; openDox-code's whole suite.
  - **Ruled**: ARC-Q1. **Decisions**: ARC-6.
  - **After**: T071.
  - **Order**: under ARC-6 (a) it lands before T061, so phase 5's pin chain carries it.
  - **Lane**: 4.
- [ ] T073 [US3] [oXc] **The composed declarations (ARC-Q2 (a)).** U-9's
  workflow gains R1Q24's 3 rail files (the rail registered in `tests/conftest.py`,
  as U-1 registers the host), its 5 contracts files and the governed-behaviour
  files the lone checkout cannot run; `tests/declared_exclusion.yaml`'s entries
  become declared composed integration tests with count and reason, matching
  batch Q's F9.1 amendment. Not gated on T071.
  - **Realizes**: requirement 9 for openXdox-code, by declaration (F9.1 as
    amended).
  - **Falsifier**: F9.1 as batch Q amends it; the composed workflow green.
  - **Ruled**: ARC-Q2.
  - **After**: T029, T005.
  - **Files**: openXdox-code `tests/conftest.py` (second), `tests/declared_exclusion.yaml`
    (first), `.github/workflows/composed.yml` (second).
  - **Lane**: 3.
- [ ] T074 [oXc] **Declare the seams, retarget the eight modules, respell the
  seven tests.** openXdox-code declares seams for corpus loading and status
  reading (generator, `corpus_root`, `gate_console`), `derive_possibles`' index
  and disposition (`gate_console`, `cli_gate`, `gate_routes`), the readiness
  renderer and the pin sentinel (`snapshot_registry`); `completeness.py`,
  `round_trip.py` and `generator.py`'s generic half import T072's module; the 7
  test files that import `doc_health` directly are respelled (none protected);
  `DOC_HEALTH_SURFACE` falls to empty; the `doc_health` exclusion reason empties;
  the help-tree test's `--deselect` in the required check and its guard test
  leave together (F9.2's two code removals).
  - **Falsifier**: `tests/test_dependency_direction.py` with
    `DOC_HEALTH_SURFACE` empty; a lone openXdox-code checkout imports cleanly; the
    composed workflow green; the help-tree test green.
  - **Ruled**: ARC-Q1. **Decisions**: ARC-4, ARC-6.
  - **After**: T071, T072's pin (T063, or the arc's own), T021, T073.
  - **Files**: openXdox-code `src/openxdox/{generator,corpus_root,gate_console,cli_gate,gate_routes,snapshot_registry,completeness,round_trip}.py`,
    the seam declarations, the 7 tests, `tests/test_dependency_direction.py`,
    `tests/declared_exclusion.yaml` (second), `tests/conftest.py` (third, if
    needed), `.github/workflows/` (third), `pyproject.toml` (if ARC-6 needs it).
  - **Lane**: 4.
- [ ] T075 [oX] [oxF] **The host registers the seams, with its pin pairs.**
  openxFactory's `scripts/opendox_host.py` registers the governed implementations
  at T074's seams at startup (the pattern of `:518-533`), with a host-wiring test
  under `tests/domain_profile/`, in the PR that moves the openXdox pin pair to
  T074's commit.
  - **Falsifier**: the pin verifiers; the host-wiring test; openxFactory's
    required checks green.
  - **Ruled**: ARC-Q1.
  - **After**: T074, T064.
  - **Lane**: 4.
- [ ] T076 [oxF] **F9.2's re-run and its tick.** Re-run F9.2; remove the
  `--deselect` from F9.1's pytest line (batch J's), under a Rule 6 window, as
  F9.2's ruled note (`5859927858`) requires; tick F9.2.
  - **Falsifier**: F9.2, exit 0, quoted.
  - **Decisions**: ARC-5.
  - **After**: T074, T075.
  - **Lane**: 4.
- [ ] T077 [oxF] **Archive the change; exit the staged topic.** Archive on merged,
  green realization evidence (release-realization); move
  `ideation/staging/doc-health-direction-arc/` out through the change and update
  its `ideation/staging/INDEX.md` row. Under a Rule 6 window, landed by merge
  commit (never squash) so the archive date holds.
  - **After**: T076.
  - **Lane**: 4.

---

## Close: acceptance, ticks, the cut

- [ ] T080 [US4] [US5] [US1] [US2] [oDc] **AT-R2, the HTTP half, in CI.** A
  harness in openDox-code's `acceptance` job (the CI owner's last edit to
  `validate.yml`), running quickstart.md §§ 1–3 at the landing commit X
  (`RELEASE2_TIP`): the four outcomes of FR-024, with `gh` absent.
  - **Falsifier**: the `acceptance` job green, quoted.
  - **Ruled**: R2Q24.
  - **After**: T066.
  - **Files**: `.github/workflows/validate.yml` (fourth), the harness.
  - **Lane**: 4.
- [ ] T081 [oxF] **AT-R2, the browser half, on the host.** quickstart.md § 4 at
  `RELEASE2_TIP`; `evidence/at-r2/` with each step's outcome and screenshot.
  - **Ruled**: R2Q24.
  - **After**: T080.
  - **Lane**: 4.
- [ ] T082 [oxF] **Bookkeeping: the release-2 ticks and the arc's close.** Under a
  Rule 6 window, no `Arc:` trailer: tick the 37 release-2 boxes, each with its
  evidence path (SC-004); run F11.1 at the arc's close (T093) and tick 9.5, 11.0,
  11.1 and F11.1 (OQ-038-2); close plan 034's T090–T093 by reference to this
  task; record 11.0's landing set per repository.
  - **Realizes**: the 37; 9.5, 11.0, 11.1, F11.1.
  - **Falsifier**: F11.1 prints `requirement 1 holds`; the box census reads every
    release-2 box `[x]`.
  - **After**: T081 (SC-008), T033, T066.
  - **Lane**: 4.
- [ ] T083 [xF] **The cut's pin sync, with the three-way parity.** The aggregation
  moves its `openxFactory` gitlink with `.github/clearing/openxfactory/PIN.yaml`,
  and its root `openDox` and `openXdox` gitlinks equal to openxFactory's nested
  gitlinks and to `contracts/opendox-pin.yaml` / `contracts/openxdox-pin.yaml`'s
  `commit:`, in ONE commit (the aggregation's `CLAUDE.md` working rule 2);
  `python3 -m pytest tests/ -q` with `openxFactory` initialized, quoted
  (`test_opendox_openxdox_gitlink_parity.py`, `test_clearing_contract_pin.py`).
  - **Realizes**: 9.5 (part; recorded in T082's tick if it lands first, else in
    an evidence note).
  - **After**: T082.
  - **Lane**: 4.
- [ ] T084 [US1] [US4] [oDc] [oD] **Publish `opendox` 0.2.0. LAST, on Brett's
  publish word.** After AT-R2 passes and Brett gives the word: assert P (T062's
  pinned commit) and X (T080's) have identical build inputs (`git diff --quiet P
  X -- src/ pyproject.toml migrations/ README.md LICENSE`), else re-run both AT-R2
  halves at P; tag `v0.2.0` on P; dispatch the existing trusted-publishing
  workflow (OIDC, no stored token); confirm `pypi.org/pypi/opendox/0.2.0/json`;
  then the openDox root README's install line names 0.2.0 (batch Q's batch-O
  style addendum).
  - **Ruled**: R2Q23.
  - **After**: T081, T082, T083, and Brett's publish word.
  - **Files**: the tag; openDox root `README.md` (third, last).
  - **Lane**: 4.

---

## Every phase

- [ ] T090 [oD] [oXc] [oX] [oxF] [xF] **The pin procedure (9.5)**, once per phase
  (T027 → T028 → T030; T060 → T062 → T063 → T064) and for the arc (ARC-6): the
  seven steps of plan.md § "Pins and landing order", C4's runbook
  (`docs/openxdox-pin-resync-runbook.md`), and step 7, the aggregation's routine
  pin-sync after each openxFactory landing.
  - **Realizes**: 9.5 (ticked at T082).
  - **Falsifier**: `make pins` (both roots); `verify-opendox-pin.py`,
    `verify-openxdox-pin.py`; the aggregation's parity tests, run locally.
- [ ] T091 [oDc] [oXc] [oD] [oX] [oDs] [oxF] **The trailer (11.0).** Every
  realization landing carries `Arc: neutral-product-standalone-operability` with
  its `Lane:` line, found by `git log --first-parent --grep='^Arc:
  neutral-product-standalone-operability$'`; bookkeeping (T004, T005, T008,
  T082, evidence) carries none; the direction arc's change carries its own.
  - **Realizes**: 11.0 (ticked at T082).
  - **Ruled**: R1Q20 (a).
- [ ] T092 [oxF] **11.1's notes.** One `edits[].note` per closed reach, added or
  extended and never rewritten, riding in T030 and T064.
  - **Realizes**: 11.1 (ticked at T082).
  - **Falsifier**: F11.1's manifest check.
- [ ] T093 [oxF] **The interim F11.1, and F11.1 at the arc's close.**
  `PACKET_MERGE=94b6f7f1`, `ARC_TIP` the last arc landing measured; the closed
  guard (HOST, HOST_TESTS, PIN_PAIRS, COMPOSITION_TESTS, ADMITTED_ARC_EDITS),
  which grows only by a ruling (`5890601202`). Run as T032 (phase 4), T065 (phase
  5) and in T082 (the close).
  - **Realizes**: F11.1 (ticked at T082).
  - **Falsifier**: F11.1 prints `requirement 1 holds` (SC-003).

---

## Box accounting (#1144 `tasks.md`: 125 boxes; 42 open at `ce64afc9`)

| box | realized by | evidence | ticked by |
|---|---|---|---|
| 12.1, 12.1a, 12.2, 12.3 | T011 | T031 | T082 |
| 12.4 | T014 (T019 for the host half) | T031, T019 | T082 |
| 12.4a | T015 | T031 | T082 |
| 12.5 | T020–T026, T029 (T019 rows 10–11) | T032 | T082 |
| F12.1 | T029 | T032 | T082 |
| 12.6 | T012, T016 | T031 | T082 |
| 12.6a | T012, T013, T016 | T031 | T082 |
| F12.2 | T011–T016 | T031 | T082 |
| 6.1, 6.1a, 6.2, F6.1 | T052 (6.2's body: T044) | T065 | T082 |
| 14.1, 14.2, 14.3 | T042 | T065 | T082 |
| 14.4 | T044, T046 | T065 | T082 |
| 14.5 | T046, T057 | T065 | T082 |
| 14.6 | T041, T053 | T065 | T082 |
| 14.7 | T053 | T065 | T082 |
| 14.8 | T054 (T040's schema) | T065 | T082 |
| 14.9 | T043 | T065 | T082 |
| F14.1 | T042–T054, T057 | T065 | T082 |
| 15.1 | T040, T045 | T065 | T082 |
| 15.1a | T040, T047 | T065 | T082 |
| 15.1b | T048 (T010's CI) | T065 | T082 |
| 15.2 | T041, T045 | T065 | T082 |
| 15.2a | T049 | T065 | T082 |
| 15.3 | T050 | T065 | T082 |
| 15.4 | T056 | T065 | T082 |
| 15.5 | T058 (T010, T048, T056) | T065 | T082 |
| 15.6 | T048, T056 | T065 | T082 |
| 15.6a | T055 | T065 | T082 |
| 15.7 | T042, T047, T056 | T065 | T082 |
| F15.1 | T058 (T048 live) | T065 | T082 |
| 9.5 | T027, T028, T030, T060, T062–T064, T083 (T090) | T090's runs | T082 (arc close) |
| 11.0 | T091 | T082's landing set | T082 (arc close) |
| 11.1 | T092 (T030, T064) | F11.1 | T082 (arc close) |
| F11.1 | T093 (T032, T065, T082) | `evidence/f11.1-*` | T082 (arc close) |
| F9.2 (outside the 37) | T073–T075 | T076 | T076 (ARC-5) |

**Count:** Group 12's 11, Group 6's 4, Group 14's 10 and Group 15's 12 make
the 37; with the four arc-close boxes and F9.2, all 42 open boxes have a task.

## Falsifier mapping (the falsifiers of Groups 6, 11, 12, 14 and 15 that release 2 owns)

| falsifier (#1144 `tasks.md`) | amended by | run by | quoted in |
|---|---|---|---|
| F6.1 (`:1143`, openDox-code, no sibling) | batch Q item 1 (an entry point first; "Today" struck) | T052 (in its PR), T065 | `evidence/f6.1-run.md` |
| F11.1 (`:2007`, openxFactory, at the arc's close) | none (the guard is closed, `5890601202`) | T093 as T032, T065, T082 | `evidence/f11.1-phase4.txt`, `f11.1-phase5.txt`, T082's record |
| F12.1 (`:2670`, 12.5's, openXdox-code with openDox installed) | batch Q item 3 (composed); item 8 (H-2, R-1 notes, if ruled) | T029 (required workflow), T032, T063 | `evidence/f12.1-run.md` |
| F12.2 (`:2816`, openDox-code, no sibling, `gh` absent) | batch Q item 1 (`--local`) | T031 | `evidence/f12.2-run.md` |
| F14.1 (`:3302`, openDox-code over `health-corpus`) | batch Q item 1 (the document server first; `--local`); item 4 (selection by fixture document) | T065 (its nodes by T053, T054, T057) | `evidence/f14.1-run.md` |
| F15.1 (`:3548`, openDox-code over `pack-corpus`, 24 nodes) | batch Q item 1 (server first; sandbox precondition; forking child's pack id; export not steerable; restore is a write); item 4 | T058 (in `validate`), T065 | `evidence/f15.1-run.md` |

F9.1 (amended by batch Q item 6, ARC-Q2 (a)) is re-run by T073; F9.2 by T076.

## Coverage self-check

### Every FR and SC of spec.md

| requirement | tasks |
|---|---|
| FR-001 (12.1, 12.1a) | T011 |
| FR-002 (12.2, 12.3) | T011 |
| FR-003 (12.4; R2Q2) | T014, T019, T005 (item 2) |
| FR-004 (12.4a; R2Q1, R2Q3) | T015, T016, T019 |
| FR-005 (12.5, F12.1; R2Q2, R2Q8) | T020–T029, T032, T063, T005 (item 3) |
| FR-006 (12.6) | T012, T016 |
| FR-007 (12.6a, F12.2; R2Q3–R2Q7) | T008, T012, T013, T016, T018, T031 |
| FR-008 (6.1, 6.1a, 6.2, F6.1; R2Q14) | T044, T052, T065 |
| FR-009 (14.1–14.3; R2Q13, R2Q15) | T042 |
| FR-010 (14.4; R2Q11, R2Q12) | T044, T046 |
| FR-011 (14.5) | T046, T057 |
| FR-012 (14.6; R2Q11) | T041, T053 |
| FR-013 (14.7) | T053 |
| FR-014 (14.8) | T054, T040 |
| FR-015 (14.9, F14.1; R2Q10) | T043, T065, T005 (item 4) |
| FR-016 (15.1, 15.1a; R2Q18, R2Q21, R2Q22) | T040, T045, T047 |
| FR-017 (15.1b; R2Q15, R2Q16, R2Q17) | T010, T048 |
| FR-018 (15.2, 15.2a; R2Q25) | T041, T045, T049 |
| FR-019 (15.3, 15.4; R2Q12) | T050, T056 |
| FR-020 (15.5, 15.6, 15.6a; R2Q17) | T010, T048, T055, T056, T058 |
| FR-021 (15.7) | T042, T047, T056 |
| FR-022 (11.0, 11.1, F11.1) | T091, T092, T093, T082 |
| FR-023 (9.5; R2Q22, R2Q23) | T060, T061, T084, T090, T083 |
| FR-024 (AT-R2) | T080, T081 |
| FR-025 (process) | T004, T005 (and every task's Falsifier line) |
| SC-001 | T031, T032, T033 |
| SC-002 | T065, T066 |
| SC-003 | T032, T065, T093 |
| SC-004 | T082 |
| SC-005 | T010, T017, T051, T030, T064, T075 |
| SC-006 | T011, T016, T057, T042, T054, T048 (outcomes; AT-R2 in T080, T081) |
| SC-007 | T012, T013, T016 (no automatic merge; every landing confirmed or instrumented) |
| SC-008 | T080, T081, before T082 |

### Every ruling

| ruling | realized by | | ruling | realized by |
|---|---|---|---|---|
| R2Q1 | T015, T016, T005 (5) | | R2Q14 | T052 (recorded at the tick) |
| R2Q2 | T014, T005 (2) | | R2Q15 | T042, T046, T057 |
| R2Q3 | T015, T016, T019, T064 | | R2Q16 | T048, T052, T056, T005 (9) |
| R2Q4 | T012, T015, T016 | | R2Q17 | T010, T048 |
| R2Q5 | T011, T016 | | R2Q18 | T041, T045, T047 |
| R2Q6 | T008, T012, T013 | | R2Q19 | no task: kept as ratified (T048 honours it) |
| R2Q7 | T012, T018 | | R2Q20 | no task: kept as ratified (T045 honours it) |
| R2Q8 | T020–T029, T005 (3) | | R2Q21 | T047; the `stack.yaml` lockstep is F2's, no release-2 task |
| R2Q9 | T005 (1), T015, T016, T046, T048, T052, T058 | | R2Q22 | T040, T041, T047, T054, T060 |
| R2Q10 | T041, T046, T053, T005 (4) | | R2Q23 | T061, T084, T005 (10) |
| R2Q11 | T044, T053 | | R2Q24 | T080, T081 |
| R2Q12 | T046 | | R2Q25 | T041, T042, T057 |
| R2Q13 | T042 | | ARC-Q1–ARC-Q4 | T070–T077; ARC-Q2 also T029, T005 (6); ARC-Q4 T006 |

## Phase 4 writer slices (for the fan-out)

| slice | tasks | repo | lane | files (single owner while open) | depends on | falsifier | size |
|---|---|---|---|---|---|---|---|
| CI | T010, T017 | oDc | 4 | `.github/workflows/validate.yml` | T004 | the job's own run | Sonnet (T017); Opus (T010, the live proof) |
| P4-A | T011 | oDc | 4 | `session_pr.py` (new names), `submission_push.py`, `runtime/repository_act.py` (call site), two new tests | T004 | F12.2 (2 nodes), `test_submission_port.py` | Opus |
| P4-D1 | T012 + T013 | oDc | 4 | `landing.py`, `landing_confirm.py`, `session_git.py`, `tests/test_session_git.py`, `tests/test_landing_guardrails.py` | T004, T008 | F12.2 (13 nodes) | Opus |
| P4-B | T014 | oDc | 4 | `serve.py`, `cli.py` | T011 | F12.2 (server node) | Sonnet |
| P4-C | T015 | oDc | 4 | `cli_branch_actions.py`, `serve_branch_actions.py`, `default_profile.py`, `serve.py`, `branch-actions.js`, `app.js`, `index.html`, census | T014, T025 | F12.2 (5 nodes) | Opus |
| P4-D2 | T016 | oDc | 4 | as P4-C, plus `branch_session.py` | T015, T012, T013 | F12.2 (surface) | Opus |
| README | T018 | oD | 4 | root `README.md` | T016 | — | Sonnet |
| P4-E | T019 | oxF | 4 | a new `tests/domain_profile/` test | lands with T030 | the test; parity test green | Sonnet |
| U-1 | T020 | oXc | 3 | `tests/conftest.py`, `tests/test_host_plane.py` | T004 | host-reg nodes | Opus |
| U-2 | T021 | oXc | 3 | `gate_console.py`, `contracts/schemas/`, `copies.yaml` | T004 | schema nodes | Sonnet |
| U-3 | T022 | oXc | 3 | the runbook copy | T004 | runbook nodes | Sonnet |
| U-4 | T023 | oXc | 3 | `swb-session.js` | T004 | Group J | Sonnet |
| U-5 | T024 | oXc | 3 | the shim | T004 (H-1) | Group L, T | Sonnet |
| U-6 | T025 | oDc | 3 | `staging-workbench.js`, `staging-workbench-model.js`, census | T004 (W-1) | S1 + DJ | Opus |
| U-7 | T026 | oXc | 3 | `protected_suite_respellings.yaml` and the five protected files; `protected_suites.py` (R-1 (a)); `opendox_bundle.py` (W-1 (A′)) | T020, T005 | the oracle | Opus |
| U-8 | T027, T028, T030 | oD, oXc, oX, oxF | 4 | the pins | T017, T025; T029 | the pin verifiers | Sonnet |
| U-9 | T029 | oXc | 3 | `composed.yml`, `composed_host_pin.yaml` | T020–T026, T028 | F12.1 | Opus |
| P4-G | T031, T032, T033 | oxF | 4 | `evidence/` | T027, T029, T030, T005 | F12.2, F12.1, F11.1 | Sonnet |

**Parallel on day one:** CI (T010) ∥ P4-A ∥ P4-D1 ∥ U-1 ∥ U-2 ∥ U-3 ∥ U-4 ∥ U-5 ∥ U-6.

## Phase 5 writer slices (for the fan-out)

| wave | slice | tasks | lane | depends on | size |
|---|---|---|---|---|---|
| W1 | schemas | T040 | 4 | T004 | Sonnet |
| W1 | U-0 | T041 | 4 | T040 | Sonnet |
| W1 | HA-1 | T042 | 4 | T027 / T033 | Opus |
| W1 | HA-3 | T043 | 4 | T027 / T033 | Sonnet |
| W2 | HA-2 | T044 | 4 | T041, T043 | Opus |
| W2 | G15-A | T045 | 3 | T041 | Sonnet |
| W3 | HA-5 | T046 | 4 | T042, T044 | Opus |
| W3 | G15-B | T047 | 3 | T045, T040 | Opus |
| W3 | G15-C | T048 | 3 | T045, T010 | Opus |
| W3 | G15-D | T049 | 3 | T045 | Sonnet |
| W3 | G15-H | T050 | 4 | T027 / T033 | Sonnet |
| every wave | CI | T051 | 4 | the wave | Sonnet |
| W4 | HA-4 | T052 | 4 | T044, T046, T005 | Opus |
| W4 | HA-6 | T053 | 4 | T046, T049, T016 | Opus |
| W4 | HA-7 | T054 | 4 | T046, T040, T053 (`health/cli.py`) | Sonnet |
| W4 | G15-G | T055 | 3 | T043, T045, T047 | Sonnet |
| W4 | G15-E | T056 | 3 | T046, T042, T047, T048, T049 | Opus |
| W4 | facet follow-on | T059 | 4 | T050 | Sonnet |
| W5 | HA-8 | T057 | 4 | T046, T053, T054, T050, T056 | Opus |
| W5 | G15-I2 | T058 | 3 | T047, T048, T049, T055, T056, T005 | Opus |
| W6 | cut and pins | T060–T064 | 4 | T058, T057 | Sonnet |
| W6 | HA-10 | T065, T066 | 4 | T064 | Sonnet |

## The direction arc's slices

| slice | tasks | lane | depends on | size |
|---|---|---|---|---|
| the change | T070, T071 | 4 | T004 | Opus |
| lines | T072 | 4 | T071 | Sonnet |
| declarations | T073 | 3 | T029, T005 | Sonnet |
| seams and retargets | T074 | 4 | T071, T072's pin, T021, T073 | Opus |
| host registration | T075 | 4 | T074, T064 | Sonnet |
| F9.2 and archive | T076, T077 | 4 | T075 | Sonnet |

## Dependencies and execution order

1. **Phase 0**: T004 (after T003) gates everything except T001–T003, T006,
   T007. T005 lands before T026, T031, T033, T052, T058, T060, T065 and T073.
   T008 before T013.
2. **Phase 4**: the product chain T011 → T014 → T015 → T016 (with T012 + T013)
   → T017 → T027 → T028; the repair chain T020 → T026; both join at T029 → T030
   → T032 → T033.
3. **Phase 5**: W1 → W6 as the table gives; openDox-code slices from T027
   (N-6 (a)) or T033.
4. **Beside phase 5**: T070 → T071 → T072 → T074 → T075 → T076 → T077; T073
   after T029.
5. **Close**: T066 → T080 → T081 → T082 → T083 → T084 (LAST).

## Implementation strategy

- **MVP: phase 4** (US1 + US2, with US3 held): a plain repository submits and
  lands. It is shippable on its own pins (T027–T030), but release 2 publishes
  once, at the close (R2Q23 (a)).
- **Increment: phase 5** (US4, US5, US6), wave by wave, each wave green in
  `validate` before the next opens its PRs.
- **Beside it**: the direction arc, which never blocks the release.
- Every slice's PR names its task ids, the boxes it realizes and its falsifier's
  quoted output (FR-025).

## Ruled amendments (`6003486656`, `6003918488`, and T004's ruling)

| batch | item | #1144 location | ruling |
|---|---|---|---|
| Q | R2Q9's seven: F6.1's entry point and struck "Today"; F14.1/F15.1 start the server; F15.1's sandbox precondition; the forking child's pack id; the unsteerable export; the restore is a write; `--local` on three verbs | F6.1 (`:1143`), F14.1 (`:3302`), F15.1 (`:3548`), 12.4a, 12.6a, 14.5 | `6003486656` |
| Q | R2Q2's repoint-sentences note | 12.4 (`:2513-2519`); `design.md:476-478`, `:1059-1061` | `6003486656` |
| Q | R2Q8's composed line | 12.5's falsifier (`:2670`) | `6003486656` |
| Q | R2Q10's selection lines | F14.1, F15.1 | `6003486656` |
| Q | R2Q1's non-normative reading | the release map (`:108`); `design.md:799-800` | `6003486656` |
| Q | ARC-Q2's F9.1 declaration, batch B's form | F9.1 | `6003918488` |
| Q | ARC-5's F9.2 note | F9.2 (`:1718`) | T004 |
| Q | H-2's batch C scope; R-1 (a)'s admitted kind | 12.5's falsifier | T004 |
| Q | R2Q16's reading at 15.1b | 15.1b (`:3426`) | `6003486656`, T004 (N-12) |
| Q | 9.5's two addenda (bundle, 0.2.0) | 9.5 (`:1553`) | `6003486656`, T004 (N-5) |
| — | F9.1's `--deselect` removed | F9.1 (batch J's line) | `5859927858`, at T076 |

**Task count:** 77: Phase 0 9 (T001–T009, two done), Phase 4 24 (T010–T033),
Phase 5 27 (T040–T066), the direction arc 8 (T070–T077), Close 5 (T080–T084),
Every phase 4 (T090–T093).
