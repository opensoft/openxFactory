# Tasks: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Input**: [`spec.md`](./spec.md), [`plan.md`](./plan.md), [`research.md`](./research.md),
[`data-model.md`](./data-model.md), [`contracts/`](./contracts/),
[`quickstart.md`](./quickstart.md), [`clarify-questions.md`](./clarify-questions.md),
and #1144's ratified `openspec/changes/add-neutral-product-standalone-operability/tasks.md`,
which holds the boxes and every falsifier.
**Lane**: `openxfactory-4` (coordinator), with lane `openXfactory-3` (peer).
**Revision**: review round 1 folded (`evidence/analyze-round-1.md`,
`evidence/plancheck-lane3-round-1.md`); each changed task cites its finding.
T004 encodes Brett's ruling of the plan.

**Revision: T002's bookkeeping** (2026-10-06). The rulings posted on `#656` since
the plan was ruled are encoded as worded, each cited by comment id, with no new
decision:
- the Files of T022 (`6016356225`), T023 (`6016676145`), T026 (`6016648451`),
  T029 (`6017860539`) and T073 (`6020698021`), and T026's three more in-test
  respellings, 17 to 20 (`6020859092`);
- R-1 (a)'s six spans and F12.1's `--chains` (`6016648451`);
- T073's After set, T094, T095+ and its `open_until` wording (`6016982816`);
- T076's F9.2 disposition (ARC-5 (a), `6013547504`);
- T003's close on the re-check (`6017901451`);
- T074's Files (the arc change's `design.md` § 10);
- the finding's `identity`, stored and emitted (`6018624750`);
- the ticks of T002, T003, T005, T008, T010, T020, T024, T040 and T070, each with
  its pull request and merge commit.

**RULED.** Brett Heap ruled the plan at `6847e99e`, every item as recommended
(`#656` `6013547504`, 2026-10-06; plan.md § "Ruled answers, the plan ruling").
Implementation starts on this word. Still his word, at the act: the `dox-v1.2`
cut (T060), the arc change's ratification (T071) and the 0.2.0 publish (T084).
The constitution's analyze gate stands as plan.md § Constitution Check records
it: round 1's CRITICALs are applied and re-checked, and a fresh analyze of the
ruled revision (T003) was the holder's call before the first realization PR
lands, closed on the re-check (`6017901451`): no round-2 analyze is dispatched.

## Format

`- [ ] T### [P?] [US#] [repo] Title`, followed by up to ten lines:

- **Realizes**: the #1144 boxes the task closes, or advances when marked
  "(part)". A box is TICKED only by T082 (bookkeeping, after AT-R2, SC-008),
  except 9.5, which T084 ticks last, after the cut's sync and the publish.
- **Falsifier**: the #1144 falsifier or named test the task must pass, quoted
  in its PR (FR-025).
- **Ruled**: the answers the task carries out. Round 1, R2Q1–R2Q25, all (a):
  `#656` `6003486656` (2026-10-05), verbatim *"Accept all 25 recommended
  (Recommended)"*. The direction arc, ARC-Q1–ARC-Q4, all (a): `#656`
  `6003918488` (2026-10-05T21:59:43Z).
- **Decisions**: the plan.md items the task carries out (tier 1 rulings, tier 2
  readings, tier 3 defaults), every one RULED as recommended (`#656`
  `6013547504`).
- **Blocked by**: none. Every behavioural question is answered (FR-025).
- **After**: tasks that must land first. `T005` means batch Q. Every
  single-writer order of plan.md is encoded here (ADV-23).
- **Lands with**: a task whose change rides in the same PR.
- **Files**: the files the task owns, as plan.md § "Parallel slices" orders
  them. A file another open slice owns is never edited.
- **README**: an evidence task links its evidence file in the feature's entry of
  openxFactory's `README.md` in the same PR (Principle IV; D1, ADV-34).
- **Lane**: `4` (openxfactory-4) or `3` (openXfactory-3), as plan.md § "Two
  lanes" sets out, lane 3 accepted and Brett ruled (T009).

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
  neutral-product-standalone-operability` and their lane's `Lane:` line (T073
  included, as #1144's requirement-9 work); bookkeeping carries no `Arc:`
  (R1Q20 (a)); the direction arc's change carries its own value (decision
  ARC-4). No closing keyword in any commit message or PR body. Land by squash
  or merge, never rebase.
- **Evidence** goes to this feature's `evidence/`, `Status: record`, with no
  `Arc:` trailer.

## What can start

Brett Heap answered all 25 round-1 questions (`6003486656`) and the four
direction-arc questions (`6003918488`), and ruled the plan's 67 items, every one
as recommended (`#656` `6013547504`): seven rulings, eight readings confirmed,
52 defaults. On that word:

- **Day one** (plan.md § "The critical path"): T005 (batch Q, the first act),
  T008, T009, T010, T011 (and T012 beside it, landing after it), T013 (after
  T008), T020–T024 (T021 after T020, T022 after T021; H-1 confirmed as CF-3 for
  T024), T025 (W-1 (A) ruled), T040, then T060 as soon as T040 lands, and T070.
- **The long pole** of phase 4 is P4-F: T020 → T026 → T029 (lane 3).
- **Phase 5's openDox-code slices** start once T027 has pinned phase 4's
  openDox-code commit (tier 1's N-6 (a), ruled); they do not wait for T033. The
  copies (T041, T047, T054) also wait for T060's pinned spec commit.
- **Requirement 9 for openXdox-code** (T073, lane 3) starts after T029; it is
  #1144's work, not the direction arc's, and is not gated on T071. Its PR stays a
  DRAFT until the repair slices T095+ land, which T094's read-only map cuts
  (`6016982816`).
- **The direction arc** (T070–T072, T074–T077) runs beside phase 5 and gates
  neither release 2's close nor #1144's archive (ARC-Q3 (a)); T061 never waits
  for it.
- **The publish** (T084) is LAST, on Brett's publish word after AT-R2.

---

## Phase 0: preconditions (holder)

- [ ] T001 **Claims, per slice.** Before each slice opens, its lane posts a
  `CLAIMED` on `#656` after a sibling search, naming the task ids, the files it
  owns (plan.md § "Parallel slices") and `lane X's PR #N` once it exists. Lane
  3 claims its own slices; lane 4 lands every PR. A standing act.
  - **Lane**: 4 and 3.
- [x] T002 **Release-2 base, and the re-measure at the ruling.** DONE:
  `evidence/r2-base.md` (2026-10-06). Every repository's `main` is recorded with
  its date; the box census reads 125 boxes and 42 open, as at `ce64afc9` (delta
  0); `PACKET_MERGE=94b6f7f1`; and lane openXfactory-3's composed re-run reads
  174 red against R2-INV-P4F's 174, with no node moved. Record in
  `evidence/r2-base.md`: every repository's `main` (the R0 command of
  research.md), the box census, and `PACKET_MERGE=94b6f7f1` for F11.1. Lane 3
  re-runs 12.5's composed suites at the then-current tips and quotes the red
  count against R2-INV-P4F's 174 (research.md R2), naming any node that moved.
  - **README**: links `evidence/r2-base.md`.
  - **After**: T004 (the base is recorded at the ruling).
  - **Lane**: 4 (lane 3 for the composed run).
- [x] T003 **The independent analyze, round 2.** DONE, CLOSED ON THE RE-CHECK:
  the holder's call, which this task's own text grants (`#656` `6017901451`).
  Two reviewers re-checked round 1 at `6847e99e`, and every CRITICAL, HIGH and
  FIX item landed as worded (`6013547504`). #1245 then converged through its
  Copilot rounds. No round-2 analyze is dispatched. The task's text, as
  written: an independent reviewer runs
  `/speckit-analyze` over this revision (the plan writer does not). Round 1's
  findings are dispositioned in `evidence/analyze-round-1.md` and
  `evidence/plancheck-lane3-round-1.md`. If the holder dispatches round 2, its
  findings are dispositioned in this task's own revision of the plan, committed
  with its verbatim report under `evidence/`, before the first realization PR
  lands, not ignored (constitution, Development Workflow); T004 is done and
  encodes only the ruling and round 1's re-check. Both reviewers re-checked
  round 1 at `6847e99e` before Brett ruled: every CRITICAL, HIGH and FIX item
  landed as worded (`#656` `6013547504`). The re-check's five remaining fixes
  are applied at T004. Whether that re-check closes this task is the holder's
  call.
  - **Lane**: 4 (holder dispatches).
- [x] T004 [oxF] **Brett's ruling of the plan, encoded.** DONE. Brett Heap ruled
  plan.md's three tiers at `6847e99e` by interactive multi-choice, every item as
  recommended (`#656` `6013547504`, 2026-10-06). This revision encodes it:
  plan.md § "Ruled answers, the plan ruling" quotes his words; § "Design
  decisions, RULED with the plan" marks every item with the option taken, with
  N-7b moved to tier 1 and OQ-12-12 and OQ-12-16 to tier 2 as CF-7 and CF-8
  (seven rulings, eight readings, 52 defaults); `spec.md` carries I-2 (a)
  (FR-010's and the other "`main`'s tip" lines now read "the baseline branch's
  tip"); and the re-check's five remaining fixes are applied (T003). No new
  evidence file; the README entry's wording says the plan is ruled.
  - **Files**: this feature's documents; `README.md` (the entry's wording only).
  - **After**: the two reviewers' re-check of round 1 at `6847e99e` (recorded in
    `6013547504`); T003's fresh analyze was the holder's call, closed on the
    re-check (`6017901451`).
  - **Lane**: 4.
- [x] T005 [oxF] **Batch Q: record the answers' amendments in #1144, in plan
  034's T007 form, ONE PR, under a Rule 6 window. THE FIRST ACT.** Its contents
  are tier 2's CF-2, as Brett confirmed them (`6013547504`). Each amended line
  cites its ruling.
  It amends no requirement and no scenario. It holds:
  1. **R2Q9 (a)'s seven** (`6003486656`): F6.1 builds an entry point first, its
     stale "Today" text (`tasks.md:1163-1165`) is struck, and 6.2's matching
     description (`:1138-1142`) is noted as superseded (lane 3's T005 FIX); F14.1
     and F15.1 first start the document server, as F13.1 does; F15.1 asserts
     its sandbox precondition; the forking pack's child carries its own pack id
     in argv; the corpus export cannot be steered by `export-subst` or
     `export-ignore`; the escaping pack's restore attempt counts as a write; the
     verb shapes of 12.4a (`submit`), 12.6a (`land`) and 14.5 (`health`) gain
     `--local`, which selects local exactly as `OPENDOX_INSTALL_MODE=local` does
     (F14.1 and F15.1, which export the setting, stand as written; F12.2 is not
     amended, ADV-04/F10).
  2. **R2Q2 (a)'s note** at 12.4: the repoint sentences (`tasks.md:2513-2519`;
     `design.md:476-478`, `:1059-1061`) are the withdrawn draft's residue.
  3. **F12.1's composed line** at 12.5's falsifier, worded as tier 2's CF-5:
     "F12.1 runs composed, as F5.2 does under R1Q23 (a); ARC-Q2 (a)
     (`6003918488`) makes the composition its permanent home" (ADV-15; lane 3's
     T005 item 3 FIX).
  4. **R2Q10 (a)'s selection lines**, every literal-id use enumerated (ADV-24):
     F14.1's `grep -q 'broken-link'` (`:3320`, `:3364`), the `want` map and
     `x["id"]` (`:3326-3329`), the `for f in broken-link …` loop with
     `health-fix-$f` (`:3336-3340`), `--finding human-only-finding` and
     `health-fix-human-only-finding` (`:3347-3349`), `--finding accepted-finding`
     (`:3351`), and `grep 'accepted-finding'` (`:3357`, `:3365`); F15.1's `grep -q
     'broken-link'` (`:3575`), `x['id'] == 'broken-link'` (`:3590`), the
     `--finding "$f"` loop over the five `patch-*` ids with `health-fix-$f`
     (`:3595-3599`), `--finding patch-ok` and `refs/heads/health-fix-patch-ok`
     (`:3601-3602`), and the `refused_patch` values (`:3608-3612`). Each becomes
     a selection by the planted finding's fixture document (its `path`, and
     `kind`), with the fixture documents named after the old literal ids.
  5. **R2Q1 (a)'s non-normative reading** of the release map's "one interface
     for both" (`tasks.md:108`; `design.md:799-800`), as tier 2's CF-1 confirms it.
  6. **ARC-Q2 (a)'s F9.1 amendment**, in batch B's form (`6003918488`):
     openXdox-code's composed files are declared integration tests with count
     and reason, and requirement 9 closes for openXdox-code by declaration.
  7. **F9.2's note**, as tier 1's ARC-5 (a) ruled it (`6013547504`).
  8. **12.5's falsifier notes**, as ruled (`6013547504`): H-2's (tier 2's CF-4)
     batch-C scope for pre-arc carve residue (`5962785556` item 1's precedent),
     and R-1 (a)'s admitted module-level kind.
  9. **R2Q16 (a)'s full reading** at requirement 16's sandbox and attribution
     clauses and at 15.1b (lane 3's R2Q16 FIX): the product's own checks run in
     process and are attributed `opendox`; a host's check registered through
     `register_health_check` runs in process at the scoped seam ONLY and is NEVER
     STORED; the sandbox clause governs manifest-listed packs; the attribution
     clause is attribution only.
  10. **9.5's two addenda**: R2Q22 (a)'s batch-G style addendum (one more
      `dox-v1.y` minor, `dox-v1.2`, carrying the three schemas, cut on Brett's
      word at T060), and R2Q23 (a)'s batch-O style addendum (`opendox` 0.2.0 at
      the cut, tag `v0.2.0`, on Brett's publish word).
  11. **7.1's addendum** (C-18; N-15): R2Q22 (a) adds three schemas to openDox's
      spec leg, so its packaged copies become seven; the two file kinds join the
      validator's kinds, and the finding shape is a copy the engine reads.
  12. **The readings tier 1 ruled** (`6013547504`): I-2 (a)'s baseline branch
      at 14.4 (`main`, else the branch HEAD names), and N-6 (a)'s overlap
      beside the release map.
  - **Realizes**: none (bookkeeping; FR-025).
  - **Falsifier**: the PR's gates against the `main` it lands on, the pinned
    `scripts/validate-openspec-cli-pin.py --all` among them.
  - **Ruled**: R2Q1, R2Q2, R2Q8, R2Q9, R2Q10, R2Q16, R2Q22, R2Q23; ARC-Q2, ARC-Q3.
  - **Decisions**: CF-1, CF-2, CF-4, CF-5; R-1, ARC-5, I-2, N-6; N-15.
  - **After**: T004.
  - **Files**: `openspec/changes/add-neutral-product-standalone-operability/tasks.md`
    (and `design.md` for item 5's addendum, if the reading needs one there).
  - **Lane**: 4.
  - **Landed**: DONE, openxFactory#1248 → `91e961a0` (2026-10-06T14:33:54Z). It
    also records Brett's `6016648451` under item 8 (F12.1 with `--chains`, and
    R-1 (a)'s six spans), folded in at `2198edda`. Its two notes name T020,
    T025 and T026 (the spans) and T026 and T029 (`--chains`) as their carriers.
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
- [x] T008 [cxF] **Feature 007's four exceptions (R2Q6 (a)).** Amend codexFactory's
  `specs/007-workbench-branch-sessions/spec.md` with four named exceptions, citing
  `6003486656`: the guard's argument check (`tests/test_session_git.py:523` still
  refusing `("merge", "other-branch")`, `:563-564`'s pin moving);
  `session_git.py:93`'s stated rule; SC-002's `HEAD` clause; SC-002's
  working-tree clause. Each names the only admitted moves: the lander's
  `--no-ff` merge in its own landing worktree under `<repo>-worktrees/` (where
  `merge` is already allowed, `session_git.py:250-263`), and `git merge
  --ff-only <commit>` of a CLEAN served checkout that holds `main`; a dirty one
  is refused (ADV-08, ADV-36).
  - **Ruled**: R2Q6. **Decisions**: N-8 (bookkeeping, no `Arc:`).
  - **Gates** (ADV-41; measured with `gh api repos/codeXfactory/codexFactory/rules/branches/main`,
    research R13): required status checks `validate` and `lane-line`; one
    approving review under its pull-request rules (last-push approval in one
    ruleset, code-owner review in another); Copilot review on push. Landed by a
    MERGE COMMIT (the repository allows no other).
  - **After**: T004.
  - **Files**: codexFactory `specs/007-workbench-branch-sessions/spec.md`.
  - **Lane**: 4.
  - **Landed**: DONE, codeXfactory/codexFactory#515 → `f1b019fe` (2026-10-06T11:14:26Z,
    a merge commit).
- [x] T009 **The lane split, confirmed.** DONE: Brett confirmed plan.md § "Two
  lanes" in the plan ruling, verbatim *"Accept all as recommended
  (Recommended)"* (`#656` `6013547504`). Lane openXfactory-3 had accepted it on
  three conditions, all applied (T021 before T022; T054 After T047 with the copy
  record in the single-writer table; T073 as #1144's work). Each lane records
  its slices in its handoff and the workspace's `LANES.md` as it claims them;
  lane 3 posts its claims (T001).
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

- [x] T010 [oDc] **R2Q17 (a)'s required-check change.** In openDox-code's
  `.github/workflows/validate.yml`, the required `validate` job: pins
  `runs-on: ubuntu-24.04` (`:47` reads `ubuntu-latest` today); installs
  bubblewrap; sets `kernel.apparmor_restrict_unprivileged_userns=0`; proves the
  sandbox LIVE in a step before the suite (a `bwrap` invocation that must
  succeed, and one that must be refused a write outside its tmpfs); records
  `bwrap --version` (OQ-H15-21); and exports the switch under which the sandbox
  tests FAIL rather than skip when `CI` is set. `EXPECT_SKIPPED` stays "11"
  (`:306`). No macOS job. The 26.04 move waits for T068's measurement.
  - **Realizes**: 15.1b (part), 15.5 (part, the platform).
  - **Falsifier**: the job's own run on the PR, quoted: the live proof step
    green, the suite's selected/passed/skipped counts unchanged.
  - **Ruled**: R2Q17. **Decisions**: N-4, OQ-H15-21.
  - **After**: T004.
  - **Files**: `.github/workflows/validate.yml` (first of five edits: T010 →
    T017 → T051 → T067 → T080).
  - **Lane**: 4.
  - **Landed**: DONE, openDox-code#89 → `34c20641` (2026-10-06T14:34:29Z).

### P4-A: the submission protocol and its neutral default

- [ ] T011 [P] [US1] [oDc] **`SubmissionPort`, `Submission`, `LocalGitSubmissions`,
  `NoSubmissionTarget`.** Add the protocol (`submit(branch) -> Submission`) and
  the report to `session_pr.py` as NEW names, never touching the three classes
  `test_session_snapshot.py:893-916` pins. `Submission` carries `remote`, `ref`
  and `url` (the credential redacted), with `branch` and `commit` (12.1a;
  data-model.md; ADV-02). `submit` RETURNS only on success; every failure
  RAISES a named, redacted error: `NoSubmissionTarget` (no remote; or several
  remotes and none named `origin`, 12.3) and `SubmissionRefused` (a rejected
  push, several push URLs, a transport failure). The remote is the one named
  `origin`, else the sole remote (ADV-26). `LocalGitSubmissions(Path(checkout_root))`
  pushes through `submission_push.py`, which factors the runtime's push core,
  `_push_to_remote_with` (`runtime/repository_act.py:1742`, with
  `_bound_local_destination` `:1613` and `_receive_pack_for` `:1720`), to take a
  named branch, keeping the repository-local command-config refusal
  (`_EXECUTED_LOCAL_KEYS` `:1335`, `_refuse_repository_local_command_config`
  `:1372`; lane 3's T011 FIX). A credential-bearing remote is PUSHED, and the
  report and every message are redacted (12.1a; ADV-09). `BRANCH` = `main` is
  refused. Tests use a local bare repository as `origin`, never the network.
  - **Realizes**: 12.1, 12.1a, 12.2, 12.3.
  - **Falsifier**: F12.2's two `tests/test_submission_default.py` nodes (the
    credential node here; the server node lands with T014); the new
    `tests/test_submission_port.py`.
  - **Ruled**: R2Q1, R2Q2, R2Q5. **Decisions**: OQ-12-11, CF-7 (was OQ-12-12).
  - **After**: T004.
  - **Files**: `src/opendox/session_pr.py` (first: T011 → T012), new
    `src/opendox/submission_push.py`, `src/opendox/runtime/repository_act.py`
    (first: T011 → T012), new `tests/test_submission_port.py`, new
    `tests/test_submission_default.py`.
  - **Lane**: 4.

### P4-D1: governance, confirmation and the lander (pure)

- [ ] T012 [US2] [oDc] **The landing seam.** New `landing.py`: `LandingPort`,
  `Landed`, `MergeConflict` (data-model.md), `repository_governance(checkout_root)`
  returning `standalone`, `governed` or `unknown`, fail closed; `session_pr.py`
  re-exports `LandingPort` and `repository_governance`, as FR-007 declares them
  there (ADV-23). The declaration reader reads `.opendox/governance.yaml` at
  `main`'s tip (decision N-1); `standalone` needs the explicit local install
  (`OPENDOX_INSTALL_MODE=local` or `--local`, FR-007; ADV-38); a registered host
  profile's instrument outranks a declaration (R2Q4 (a)). New `landing_confirm.py`:
  the confirmation capability, bound to the branch and its head, single-use,
  with exactly two issuers (the `/dev/tty` prompt; the server's per-branch nonce)
  and a static check that no other exists. The neutral lander: `--no-ff` merge in
  a landing worktree of its own under `<repo>-worktrees/`; the `ls-remote
  refs/heads/main` check first, at the chosen remote's PUSH URL (`git remote
  get-url --push`), with several push URLs refused (a remote with no `main`
  passes, N-16; Copilot's review of `cbe2adfb`), the URL passed to git only as
  a transient remote in the child's environment (`GIT_CONFIG_COUNT=1`,
  `GIT_CONFIG_KEY_0=remote.<transient>.url`, `GIT_CONFIG_VALUE_0=<push URL>`,
  then `git ls-remote <transient> refs/heads/main`; git 2.31 or later), never in
  its argv (data-model.md § Landed; Copilot's review of `74dfe79c`); then
  ff-only of the served checkout when it holds `main` and is clean, a REFUSAL
  naming the remedy when it holds `main` and is not clean (ADV-08), and `left`
  when it holds another branch; pushes nothing (R2Q6 (a)); `MergeConflict`
  names the remedy (OQ-038-1). A registered TEST host profile in the tests
  declares an instrument, so F12.2's host-side nodes run here (R2Q3 (a)). Audit
  every place openDox creates a repository, and pin `-b main` where git's
  `init.defaultBranch` would decide.
  - **Realizes**: 12.6a (part: the seam, the query, the capability, the lander),
    12.6 (part).
  - **Falsifier**: F12.2's thirteen `tests/test_landing_guardrails.py` nodes,
    including the static issuer check; and named nodes beside them for R2Q7 (a)'s
    two refusals (`test_a_repository_with_no_main_is_unknown_and_refused_naming_it`,
    `test_no_declaration_refuses_naming_the_file_and_its_content`; lane 3's R2Q7
    FIX), ADV-08's (`test_a_dirty_served_checkout_on_main_is_refused_before_merging`),
    and the push URL's (`test_the_remote_check_reads_the_push_url_not_the_fetch_url`,
    a remote whose `pushurl` names a repository ahead of local `main`, refused;
    and a remote with two push URLs, refused; and
    `test_the_push_url_never_reaches_git_argv`, a credential-bearing push URL
    absent from every recorded git argv).
  - **Ruled**: R2Q1, R2Q3, R2Q4, R2Q5, R2Q6, R2Q7. **Decisions**: CF-1, N-1,
    N-11, N-16, OQ-12-17, OQ-038-1.
  - **After**: T004; T011 (`session_pr.py`, and `repository_act.py` if the audit
    edits `:982`'s `init --bare`).
  - **Lands with**: T013.
  - **Files**: new `src/opendox/landing.py`, new `src/opendox/landing_confirm.py`,
    `src/opendox/session_pr.py` (second: the re-exports), new
    `tests/test_landing_guardrails.py`; the repository-creation call sites the
    audit finds (named in the PR).
  - **Lane**: 4.
- [ ] T013 [US2] [oDc] **Feature 007's guard, by R2Q6 (a)'s four exceptions.** The
  lander's `merge --no-ff` runs in its landing worktree under `<repo>-worktrees/`,
  where `merge` is already allowed (`session_git.py:250-263`), so only `git merge
  --ff-only <commit>` AT THE SERVED ROOT needs the new argument check (ADV-36):
  `session_git.py:93`'s stated rule admits it for a clean checkout on `main` and
  nothing else; `tests/test_session_git.py:523` still refuses `("merge",
  "other-branch")`; `:563-564`'s pin moves to the admitted form; `:99`'s set is
  restated.
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
  `cli_branch_actions.py` holds `submit --repo-root PATH --branch BRANCH [--local]
  [--json]` (12.4a's ratified shape; ADV-01), contributed through
  `default_profile.py`'s `SUBCOMMAND_EXTENSIONS` (decision N-2), with no actor gate
  (OQ-12-9). The CLI verb does not read the install mode: only `--local`
  disagreeing with `OPENDOX_INSTALL_MODE=hosted` refuses, naming both (N-17;
  ADV-04). New `serve_branch_actions.py` holds `POST /actions/session/submit`
  behind 12.4a's three-clause gate and the console token, contributed through the
  default profile's `ROUTE_EXTENSIONS` and `HANDLER_CONTRIBUTIONS`. The
  `actions.submit` key is PRESENT only under openDox's own profile, which
  contributes it; its VALUE is derived from the route bindings as `gate`'s is
  (`answers_a_gate_verb`, `:509-521`). Core `_DEFAULT_CAPABILITIES` (`:528`)
  gains nothing (it always carries `gate`) (ADV-14; OQ-12-14). The hosted
  plane's refusal is the ROUTE's. New
  `web/views/branch-actions.js` holds the submit control, keyed on
  `actions.submit`; `web/app.js` and `web/index.html` wire it; the census
  fixture gains its rows. Under `governed`, `submit` goes through the host's
  contributed `SubmissionPort` and reports where the work went (R2Q4 (a)).
  `contracts/cli-http-submit-land.md` is the surface.
  - **Realizes**: 12.4a.
  - **Falsifier**: F12.2's five `tests/test_submit_route.py` nodes; CLI tests
    in `tests/test_cli_branch_actions.py`; a test that a host profile replacing
    the default sees no `actions.submit` key.
  - **Ruled**: R2Q1, R2Q3, R2Q4, R2Q5, R2Q9 (item 7). **Decisions**: CF-1, N-2,
    N-17, OQ-12-9, OQ-12-14.
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
  `landing_factory` in `serve.py` and `_landing_port` in `cli.py`; `land
  --repo-root PATH --branch BRANCH [--local] [--json]` (12.6a's shape; ADV-01) in
  `cli_branch_actions.py` (prompt over `/dev/tty`, no bypass, N-11), contributed
  through `default_profile.py`; `POST /actions/session/land-nonce` and `POST
  /actions/session/land` in `serve_branch_actions.py` (OQ-12-13), contributed
  through the default profile's route facets; `actions.land` present only under
  openDox's own profile, its value derived from those bindings and true where
  `land` can act: a lander is bound, or the repository is `governed` with a
  contributed instrument (Copilot review); the confirm control in
  `branch-actions.js`. Under `governed` no lander is bound and `land` submits
  through the instrument; with none it refuses "governed-without-an-instrument".
  A live session whose branch lands ends by the existing merge observation
  (`branch_session.py`, R2Q5 (a)).
  - **Realizes**: 12.6a (part: the bindings and the surface), 12.6.
  - **Falsifier**: F12.2's guardrail nodes that drive the surface; T012's suite
    re-run green; a test that a host profile sees no `actions.land` key; a
    capability test that `actions.land` is true for `standalone` with a lander
    and for `governed` with an instrument, and false otherwise.
  - **Ruled**: R2Q1, R2Q3, R2Q4, R2Q5, R2Q6, R2Q7, R2Q9 (item 7). **Decisions**:
    CF-1, N-2, N-11, OQ-12-13, OQ-12-14, OQ-12-17.
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
  - **After**: T010, T011–T016, T025.
  - **Files**: `.github/workflows/validate.yml` (second edit).
  - **Lane**: 4.
- [ ] T018 [US2] [oD] **The openDox root README: the declaration, `submit`,
  `land`, and the two push routes.** Document `.opendox/governance.yaml` (the
  exact file and content the refusal names), `submit`, and `land` (the
  confirmation, the merge commit, the `git revert -m 1` that undoes it, that
  `land` pushes nothing, and the dirty-checkout refusal). Add R2Q6 (a)'s two push
  routes (ADV-30; E3): a plain repository's landed `main` reaches its remote by
  the user's own `git push`; a clone of a project repository pushes to it, and
  `project push` then carries the work on.
  - **Ruled**: R2Q6, R2Q7. **Decisions**: N-1.
  - **After**: T016.
  - **Files**: openDox root `README.md` (first of three edits).
  - **Lane**: 4.
- [ ] T019 [US3] [oxF] **The governed host is unchanged, proved.** A host-wiring
  test under `tests/domain_profile/` with the real host registered: no lander
  bound; the host outranks a declaration; openxFactory's help golden unchanged
  (no `submit`, `land` or `health`); `/capabilities` unchanged, key for key,
  because the new keys are derived from routes only openDox's default profile
  contributes (ADV-14; no openxFactory test pins the key set, research R13);
  `_session_pull_requests()` still `GhPullRequests`.
  - **Realizes**: 12.5 (part, rows 10 and 11), 12.4 (part).
  - **Falsifier**: the new test, and `tests/ideation-dashboard/test_extension_point_parity.py`
    unchanged and green, at T030's pins.
  - **Ruled**: R2Q2, R2Q3. **Decisions**: N-2, OQ-12-14.
  - **Lands with**: T030.
  - **Files**: a new test under openxFactory `tests/domain_profile/` (a HOST_TESTS
    surface of 11.1).
  - **Lane**: 4.

### P4-F: the governed set runnable and green (12.5), lane openXfactory-3's repair map

R2Q8 (a): F12.1 runs composed; the 174 reds are repaired WITHOUT editing the 16
suites except through allow-list entries. Every node is mapped in R2-INV-P4F
§ "The map" and part-oneoffs; the slices are its § "Slice outline", with lane
3's PLANCHECK corrections. Every landing that edits one of the 16 adds its entry
in the same PR; at the end the oracle (`scripts/protected_suites.py`) prints
`ok: … each entered and holding`. Nothing is vendored into openXdox-code's copy
record (`src/openxdox/contracts/copies.yaml`), which is single-source and pinned
to the validator's three kinds by `tests/test_packaged_validator.py:81-92`
(ADV-10; lane 3's T021/T022 FIXes).

- [x] T020 [P] [US3] [oXc] **U-1, host registration (HR).** A governed-suite list
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
  - **Files**: openXdox-code `tests/conftest.py` (first: T020 → T021 and T026, in
    landing order → T073 → T074), `tests/test_host_plane.py` (first: T020 → T021
    and T026 → T073 → T074).
  - **Lane**: 3.
  - **Landed**: DONE, openXdox-code#39 → `c6d15b27` (2026-10-06T16:10:45Z).
- [ ] T021 [US3] [oXc] **U-2, the gate console's schemas (GA), resolved without
  vendoring.** `gate_console._validate_contract_document` reads
  `parents[2] / "contracts" / "schemas"` (`gate_console.py:642-643`), which in the
  code leg is the checkout root. Make it read `gate-action-record.schema.yaml`
  (openXdox-spec's, `:665`) from openXdox-code's OWN packaged copy, which the copy
  record already holds, and `demotion-execution-receipt.schema.yaml`
  (openxFactory's, `:711`) from a schema source the HOST registers through a new
  `gate_console.register_contract_schema_source(...)` seam; with none registered,
  validating a receipt refuses by name (R1Q27 (a)). The composed run's conftest
  registers openxFactory's `contracts/schemas/` from the composed tree (one line
  after U-1's registration); openxFactory's host wiring registers the same at
  T030. Finishes schema 16 (including
  `test_execution_receipt_releases_cleanup_for_the_exact_destination`).
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 16 schema nodes (R2-INV-P4F § schema), composed, quoted; a
    lone-checkout test that the receipt refuses by name; `test_packaged_validator.py`
    unchanged and green.
  - **Ruled**: R2Q8. **Decisions**: P4F-4.
  - **After**: T020 (the conftest).
  - **Files**: openXdox-code `src/openxdox/gate_console.py` (first: T021 → T074),
    `tests/conftest.py` (after T020: T020 → T021 and T026, in landing order →
    T073 → T074), a new `tests/test_gate_console_schema_source.py`.
  - **Lane**: 3.
- [ ] T022 [US3] [oXc] **U-3, the runbook placed from the composed tree (RP).**
  `test_session_runbook.py:54` and `test_session_notebook.py:1075` read
  `REPO_ROOT / "docs" / "ideation-dashboard-session-runbook.md"`, with `REPO_ROOT`
  the openXdox-code root (`tests/conftest.py:25`). A new
  `scripts/composed_placements.py` links the runbook from the composed tree
  (`openDox/spec/docs/ideation-dashboard-session-runbook.md` under the
  openxFactory checkout, at the openDox root's pinned spec commit) to `docs/`
  for the run; `.gitignore` names the placed path, so the tree stays clean. The
  composed workflow (T029) and the documented local composed run both call it.
  Finishes moved-name runbook 10.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 10 nodes, composed, quoted.
  - **Ruled**: R2Q8. **Decisions**: P4F-3.
  - **After**: T021 (lane 3's split condition 1).
  - **Files**: openXdox-code new `scripts/composed_placements.py`, new
    `tests/test_composed_placements.py`, `.gitignore`. The ten-scenario harness
    becomes that new test in openXdox-code#41, because the script mutates the
    filesystem and CI should hold its guards; only T022 writes it, so it creates
    no single-writer conflict (holder, `6016356225`, option (a)).
  - **Lane**: 3.
- [ ] T023 [P] [US3] [oXc] **U-4, `swb-session.js` (SF).** Fix the two one-off
  Group J nodes (`test_session_confinement.py`) in the view module the carve's S5
  respelled; no protected edit.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 2 nodes, composed, quoted.
  - **Ruled**: R2Q8.
  - **After**: T004.
  - **Files**: openXdox-code `src/openxdox/web/views/swb-session.js`, and a new
    `tests/test_swb_session_transport.py`, the bound and unbound probes in one
    committed test file, so that CI kills the two behaviour mutants (always the
    module pair; a miswired wrapper) which the existing suites do not (holder,
    `6016676145`, following `6016356225`). Only T023 writes it, so it creates no
    single-writer conflict.
  - **Lane**: 3.
- [x] T024 [P] [US3] [oXc] **U-5, the shim (SF; H-1 confirmed as CF-3).** New
  `scripts/ideation_dashboard/session_git.py` (`import sys; from opendox import
  session_git as _m; sys.modules[__name__] = _m`), with NO `__init__.py` in its
  directory, so it merges with openxFactory's `scripts/ideation_dashboard/` (which
  has none) as one namespace package in the composed run instead of shadowing it
  (ADV-39; inferred from Python's namespace-package rule). `LOCK_HOLDER`
  (`test_session_transaction.py:296`) then resolves. Finishes one-off Group L 3
  and Group T's first cause.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the 4 nodes, composed, quoted; `test_dependency_direction.py`
    green (it does not scan `scripts/`).
  - **Ruled**: R2Q8. **Decisions**: CF-3 (H-1).
  - **After**: T004.
  - **Files**: openXdox-code new `scripts/ideation_dashboard/session_git.py`.
  - **Lane**: 3.
  - **Landed**: DONE, openXdox-code#38 → `8b64fae0` (2026-10-06T16:32:39Z).
- [ ] T025 [P] [US3] [oDc] **U-6, openDox web (SF; DJ by W-1 (A), ruled).**
  S1's two nodes (plan 034's T102 follow-on in `staging-workbench.js` and the
  census); and, under W-1 (A) (`6013547504`, *"Model import-free again
  (Recommended)"*), `staging-workbench-model.js` made import-free again by
  inlining what it takes from `./display.js`, which clears the 32 DJ nodes and
  the import-free pins `:802` and `:1286`. This word reverses carve slice S7's
  model import; the PR says so.
  - **Realizes**: 12.5 (part).
  - **Falsifier**: openDox-code's whole suite; the 34 nodes, composed, quoted
    at T029.
  - **Ruled**: R2Q8. **Decisions**: W-1.
  - **After**: T004.
  - **Files**: openDox-code `src/opendox/web/views/staging-workbench.js`,
    `src/opendox/web/views/staging-workbench-model.js`,
    `tests/fixtures/web_boundary_census.yaml` and `tests/test_web_boundary.py`
    (first: T025 → T015 → T016 → T057).
  - **Lane**: 3.
- [ ] T026 [US3] [oXc] **U-7, the allow-list (AL; R-1's admitted part).** One
  entry per admitted test in `tests/protected_suite_respellings.yaml`, chained by
  blob, each in the same PR as its protected edit: `cmd_gate_*` 7, `hosted_index`
  3, share paths 2, Group W 1, Group S2 4 (17, under H-2, tier 2's CF-4), and
  three more in-test respellings the holder admitted under the same CF-4 scope
  (`6020859092`; 20 in all): `test_gate_off_descriptor_is_the_real_cli_invocation`
  (`cli.cmd_gate_create_document` → `cli_gate.cmd_gate_create_document`),
  `test_gate_off_session_affordances_are_the_real_cli_invocations` (the three
  `cmd_gate_*` names → `cli_gate.…`) and
  `test_the_notebook_refresh_is_a_descriptor_in_BOTH_gate_postures` (the script
  is read from its one home on the import path, and a run fails if it finds none
  or more than one). Each is a carve-moved name or path, weakens no assertion,
  and is entered as a `respelling` naming its history, under the oracle's
  `--chains` form. Under
  R-1 (a), ruled (`6013547504`) and widened by Brett's *"Widen the spans, served
  display (Recommended)"* (`6016648451`): the admitted module-level edits reach
  SIX named spans of `tests/test_staging_workbench.py`, the harness constants
  `_CREATE_HARNESS` (`:492-553`), `_SESSION_HARNESS` (`:1008-1094`) and
  `_HOSTILE_HARNESS` (`:1950-1981`), and the three copy helpers `_run_create`
  (`:562-574`), `_run_session` (`:1239-1257`) and `_hostile_descriptors`
  (`:1997-2008`), with `scripts/protected_suites.py`'s `_inside_the_test` rule
  (`:294`) amended to admit the new kind (lane 3's T026 FIX: the path is
  `scripts/`). The helpers copy the model's siblings and hand each harness the
  SERVED governed display. T020's host registration covers this suite, through
  T020's `tests/conftest.py` and the scan in `tests/test_host_plane.py`, which
  T026 edits after T020 lands (#39). That the served display is reachable in the
  test process is INFERRED, and T026 measures it. The spans close the harness
  nodes only together with W-1's fix of the `./display.js` import at the helper
  copy sites (`:98`, `:565`, `:1242`, `:2000`, `:2507`); the widened spans close
  the last nine of them and the traced `SystemExit: 2` node. The two route claims
  (`:1291`, `:1333`) lie inside their own named tests (`:1262-1300`,
  `:1305-1343`), so in-test entries reach them and they need no span. The line
  numbers are as measured at openXdox-code `56e1c238`, where batch Q records them.
  The two non-harness nodes of R-1's 26 (lane 3's row 38 FIX):
  `test_staged_scope_adds_cluster_neighbourhood_section` takes an in-test entry
  that respells its expected label to 'group neighbourhood', S7's neutral word,
  as measured (the holder's ruling recorded with `6016648451`);
  `test_the_hostile_descriptors_still_parse_into_the_real_cli` (`SystemExit: 2`)
  is closed by the widened spans, as ruled.
  **F12.1 carries `--chains`** (Brett's *"Amend F12.1 with --chains
  (Recommended)"*, `6016648451`; batch Q adds it to 12.5's falsifier in #1144,
  T005): several entries for one suite land in ONE landing, applied in the order
  they are listed and chained by git blob. Each entry is still exactly one edit
  inside its own named test or, under R-1 (a), its named span; the landing's diff
  for each suite is exactly the chain's recorded texts, and nothing wider is
  admitted. T026 lands as ONE PR (openXdox-code#43).
  - **Realizes**: 12.5 (part).
  - **Falsifier**: the oracle, run with `--chains`, prints `ok: … each entered
    and holding`; the nodes, composed, quoted; the new
    `tests/test_protected_suite_check.py`.
  - **Ruled**: R2Q8; Brett's `6016648451` (F12.1 with `--chains`; R-1 (a)'s six
    spans). **Decisions**: CF-4 (H-2), R-1, W-1.
  - **After**: T020 (it unmasks 3; and T020's `tests/conftest.py` and
    `tests/test_host_plane.py`, which T026 edits only after #39 lands), T005
    (batch Q's 12.5 notes, `--chains` among them).
  - **Files**: openXdox-code `tests/protected_suite_respellings.yaml` (its only
    phase-4 writer), `tests/test_session_gates.py`, `tests/test_session_verbs.py`,
    `tests/test_session_confinement.py`, `tests/test_doxbench_share.py`,
    `tests/test_staging_workbench.py`, `scripts/protected_suites.py` (R-1 (a));
    a new `tests/test_protected_suite_check.py`, for the span kind's cases, as
    T022's new test holds its script's (holder, `6016648451`); and, after T020
    lands, T020's `tests/conftest.py` and `tests/test_host_plane.py` (T020 →
    T021 and T026, in landing order → T073 → T074; Brett, `6016648451`).
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
  the commit `tests/composed_host_pin.yaml` names (`schema_version`, `kind`) and
  initializes its submodules RECURSIVELY, `openDox`, `openXdox` and `openXwallet`
  included, without which `corpus_adapter_openxfactory` refuses at import (lane 3's
  T029 FIX); runs T022's placement script; installs openDox at the pin; and runs
  12.5's 16 suites with `PYTHONPATH="$OPENXFACTORY/scripts"`, then the oracle,
  with `--chains` (F12.1 as batch Q amends it; Brett's *"Amend F12.1 with
  --chains (Recommended)"*, `6016648451`). openXdox-code's help-tree goldens are
  asserted unchanged in the same run (R2Q3 (a)). After its first green run on
  `main`, the holder makes `composed` a REQUIRED check of openXdox-code,
  recorded in the evidence (N-7b (a), ruled
  `6013547504`: *"Make it required (Recommended)"*, the word for that change).
  T029 also raises the two floor lines of openXdox-code's
  `.github/workflows/validate.yml`, `MIN_SELECTED` and `MIN_PASSED`, ONCE: at its
  final head, after merging `main`, to the selected and passed counts measured
  there, with the CI-form run quoted in its body (holder, `6017860539`). No other
  PR raises them: T020 to T026 leave them unchanged, and later test-adding PRs
  (T073, T074 and T095 onward) leave them too, unless their own task names them.
  - **Realizes**: 12.5, F12.1 (both ticked at T082).
  - **Falsifier**: F12.1 (12.5's falsifier, as batch Q's line words it): 16
    suites, 0 red; the oracle, run with `--chains`, prints `ok: … each entered and
    holding`, quoted.
  - **Ruled**: R2Q8; ARC-Q2 (permanent); Brett's `6016648451` (F12.1 with
    `--chains`) and the holder's `6017860539` (the floors). **Decisions**: CF-5,
    N-7a, N-7b, R-1.
  - **After**: T020–T026, T028.
  - **Files**: openXdox-code new `.github/workflows/composed.yml` (first: T029 →
    T073 → T074), new `tests/composed_host_pin.yaml` (first; advances after T030,
    T064 and T075), and `.github/workflows/validate.yml`, its two floor lines
    `MIN_SELECTED` and `MIN_PASSED` only (T029 → T074's `LEFT_OUT`; the
    single-writer table).
  - **Lane**: 3.
- [ ] T030 [US3] [oX] [oxF] **U-8, steps 5–6: phase 4's consumer pins and host
  wiring.** The openXdox root moves its `code` gitlink and `code-pin.yaml` to
  openXdox-code's tip, and `contracts/opendox-pin.yaml` to T027's root commit.
  Then ONE openxFactory PR: the `openDox` gitlink with `contracts/opendox-pin.yaml`
  in one commit, the `openXdox` gitlink with `contracts/openxdox-pin.yaml` in
  another, the host wiring that registers openxFactory's `contracts/schemas/` as
  the gate console's schema source (P4F-4), T019's test, and the phase's
  `edits[].note`s (T092). Then `tests/composed_host_pin.yaml` advances to this
  landing, in an openXdox-code PR of its own, and T073 re-runs after it. The
  aggregation's routine pin-sync follows (T090 step 7).
  - **Realizes**: 9.5 (part), 11.1 (part).
  - **Falsifier**: `make pins` (openXdox root); `scripts/verify-opendox-pin.py`
    and `scripts/verify-openxdox-pin.py`; openxFactory's required checks green
    (SC-005).
  - **After**: T029.
  - **Lands with**: T019.
  - **Files**: openXdox root pins; openxFactory gitlinks, pin files and
    `scripts/opendox_host.py` (first: T030 → T064 → T075); openXdox-code
    `tests/composed_host_pin.yaml` (after).
  - **Lane**: 4.
- [ ] T031 [US1] [US2] [oxF] **F12.2's evidence.** Run F12.2 as ratified (batch Q
  does not amend it) in an openDox-code checkout alone at T027's pinned commit,
  under a PATH that hides `gh` (`command -v gh` empty, recorded), and quote all
  twenty named nodes, plus T012's three added nodes. `evidence/f12.2-run.md`.
  - **Realizes**: F12.2 (ticked at T082).
  - **Falsifier**: F12.2, exit 0.
  - **Decisions**: CF-8 (was OQ-12-16), N-17.
  - **After**: T027.
  - **README**: links `evidence/f12.2-run.md`.
  - **Lane**: 4.
- [ ] T032 [US3] [oxF] **F12.1's evidence, and phase 4's interim F11.1.** Quote
  T029's composed run at the pins T030 landed, and run F11.1 by T093's procedure
  (`PACKET_MERGE=94b6f7f1`). `evidence/f12.1-run.md`, `evidence/f11.1-phase4.txt`.
  - **Realizes**: F12.1 (ticked at T082); F11.1 (interim).
  - **Falsifier**: F12.1 exit 0; F11.1 prints `requirement 1 holds`.
  - **After**: T029, T030, T005.
  - **README**: links both files.
  - **Lane**: 4.
- [ ] T033 [oxF] **Phase 4 checkpoint.** `evidence/checkpoint-phase4.md` quotes
  F12.2, F12.1, the oracle and the interim F11.1 (SC-001, SC-003), names every
  phase-4 landing by repository, and records any node that moved since T002.
  - **After**: T031, T032, T005.
  - **README**: links `evidence/checkpoint-phase4.md`.
  - **Lane**: 4.

---

## Phase 5: health (US4, US5, US6), Groups 6, 14 and 15

**Goal**: every local install gets health over its own documents; repairs are
drafts on branches that land only through `land`; exceptions live in git;
packs are pinned and run only in a live sandbox.
**Independent test**: F6.1, F14.1 and F15.1 exit 0 as batch Q amends them; F15.1's
shell block and its 24 nodes run inside the required `validate` job with the
sandbox proved live (T067, T058; SC-002).

Lane openXfactory-3's outline (R2-INV-HEALTH Part 12) in seven waves, with review
round 1's corrections. Its W0 (R-0, the rulings) is T004; its G15-I1 is the CI
owner's T010, T051 and T067; its HA-9 shrinks to a proof inside T064 (decision
N-2). Phase-5 openDox-code slices start after T027 under tier 1's N-6 (a), else
after T033. The schemas come first: T040, then T060's pin and cut, then the
copies (research R7; ADV-05).

### W1: the schemas, the cut, and the first slices

- [x] T040 [P] [oDs] **The three health schemas (R2Q22 (a)).** Author in
  openDox-spec, from this feature's `contracts/`: the finding's neutral shape
  (`health-finding.md`), `health/packs.yaml` (`health-packs-manifest.md`) and the
  exceptions file (`health-exceptions.md`), in that repository's schema layout.
  - **Realizes**: 15.1, 15.1a, 14.8 (part: the contracts).
  - **Falsifier**: openDox-spec's own validation, quoted.
  - **Ruled**: R2Q10, R2Q22, R2Q25. **Decisions**: N-3, N-13, N-15, OQ-H-13,
    OQ-H15-5, -10, -12, -19.
  - **After**: T004.
  - **Lane**: 4.
  - **Landed**: DONE, openDox-spec#17 → `7db9438b` (2026-10-06T14:37:29Z). Its
    finding schema holds `identity`, which the plan now stores and emits (the
    holder, `6018624750`: the plan moved, T040 did not).
- [ ] T060 [oD] **The openDox root's spec pin and the `dox-v1.2` minor, on Brett's
  cut word (R2Q22 (a)).** Straight after T040 (moved here from W6 by review round
  1, ADV-05; release 1's order, plan 034's T053): ONE root commit moves the spec
  pin to the openDox-spec commit holding T040's three schemas and adds their
  entries to `contracts/manifest.yaml`, with the CHANGELOG entry `Status: draft`;
  then the holder ASKS BRETT FOR THE CUT WORD, as release 1's `dox-v1.1` was cut
  by him (RULED `#656` `5894235642`); on it, the annotated tag `dox-v1.2` goes on
  that commit, and a second PR moves the CHANGELOG entry to `standard`, the tag
  existing. `make validate` and `make pins` exit 0 at the target.
  - **Realizes**: 9.5 (part).
  - **Falsifier**: the root's `make validate` and `make pins`, quoted; openDox-spec's
    own `validate`.
  - **Ruled**: R2Q22; Brett's cut word, recorded on `#656`. **Decisions**: CF-2
    (batch Q item 10's addendum).
  - **After**: T040, T005.
  - **Files**: openDox root spec gitlink, `contracts/spec-pin.yaml`,
    `contracts/manifest.yaml`, `CHANGELOG.md`; the tag.
  - **Lane**: 4.
- [ ] T041 [US4] [oDc] **U-0, the contract module's finding vocabulary, and the
  first copy.** New stdlib-only `src/opendox/health_contract.py`: the classes
  `auto-fix`, `assisted`, `human-only`; the severities; the finding shape with
  `pack_id` and `pack_version`; the id rule (position-independent identity key,
  canonical sorted-key JSON, N-13; ADV-07), `pack_id` and `kind` each 1 to 40
  characters so a fix branch's name stays bounded (a 40- and a 41-character
  value tested at the boundary), the identity being hashed into the id AND
  stored and emitted with the finding (the holder, `6018624750`, which reverses
  the engine-internal refinement of Copilot's review of `2076f24b`), bounded as
  openDox-spec's finding schema (T040, landed) bounds it (no `excerpt`, `text`,
  `content` or `quote` key, no number, every string at most 200 characters; a
  pathless finding's identity is `{category, entry}` and a collision's is
  `{collided_id}`), under an engine cap on its serialized size, stricter than the
  schema's, as for `pack_id` and `kind` (the cap's value is T041's and T042's to
  set, and T041 tests it at its boundary, as it tests theirs); the bounds on `message` and
  `evidence` (R2Q25 (a); ADV-27); a closure test that the module imports only the
  standard library. Copy T040's finding schema at the spec commit T060 pins into
  openDox-code's EXISTING copy record: `copies.yaml`'s `commit:` moves to that
  commit (the four existing copies' digests unchanged), `schemas/` gains the file,
  `contracts/__init__.py`'s `COPY_IDS` gains its id, and
  `tests/test_validator_input_set.py`'s `SPEC_COMMIT`, `PINNED_BY_THE_ROOT` and set
  test move with it; the set test reads "the validator's kinds plus the finding
  shape" (N-15).
  - **Realizes**: 14.6 (part: spellings), 15.2 (part: shape), 7.1's addendum (part).
  - **Falsifier**: new `tests/test_health_contract.py`; `tests/test_validator_input_set.py`
    green at the new commit.
  - **Ruled**: R2Q10, R2Q18, R2Q22, R2Q25; the holder's `6018624750`.
    **Decisions**: N-3, N-13, N-15, OQ-H15-19.
  - **After**: T060, T027 (N-6 (a), ruled).
  - **Files**: new `src/opendox/health_contract.py` (first: T041 → T045),
    `src/opendox/contracts/copies.yaml`, `schemas/`, `__init__.py` and
    `tests/test_validator_input_set.py` (first: T041 → T047 → T054), new
    `tests/test_health_contract.py`.
  - **Lane**: 4.
- [ ] T042 [P] [US4] [oDc] **HA-1, the store (`0003_`), one owner.** New
  `migrations/0003_health.sql`: `health_runs` (with the run's kind, the
  baseline branch, the run's pack inventory with each pack's exact pin,
  `pack_pins`, the `export_commit` its packs read, whether it was
  `full`, and the probe's `sandbox` record; Copilot review) and
  `health_findings` (data-model.md, with an `identity` column: canonical
  sorted-key JSON, its serialized size capped by the engine, stricter than the
  schema's; the holder, `6018624750`), with 15.7's
  `pack_id`/`pack_version` NOT NULL from the first landing, and NO patch column
  (14.3; R2Q25 (a); lane 3's MISLABEL row 31). DOMAIN tables in
  `runtime/identity.py`'s `TABLES` (R2Q13 (a)); `runtime/cli.py`'s `DROP_ORDER` and
  reset wording; the role-init scripts (`deploy/compose/init-runtime-role.sh`,
  `deploy/kubernetes/base/init-runtime-role.sh`, and any other R2-INV-HEALTH Part
  6 C names); new `runtime/health_store.py` (no document stored, 14.3); the
  hosted plane migrates the schema (R2Q15 (a)). The five `tests_runtime/` suites
  `0003_` moves, each for its reason (lane 3's T042 FIX, re-checked by grep at
  `a9ac96f9`): `test_migrations_apply.py`, `test_runtime_cli.py` (`:277`) and
  `test_bundled_postgres.py` (`:540`, `:924`) hard-code the migration list;
  `test_schema_shape.py`'s closure reads `0001` only (`:32`, `:36-59`) and must
  read `0001` with `0003_` (R2Q13 (a)); `test_deploy_shape.py` derives its lists
  from `identity.TABLES` (`:1850`, `:2222`), so it moves with this task's
  `TABLES` edit and is re-run, not edited.
  - **Realizes**: 14.1, 14.2, 14.3, 15.7 (part: the columns).
  - **Falsifier**: new `tests_runtime/test_health_store.py`, carrying
    `test_the_store_refuses_a_finding_without_provenance` and a test that an
    install-level finding (`pack_id` `opendox`, empty `path`) is admitted; the
    five suites above.
  - **Ruled**: R2Q13, R2Q15, R2Q25; the holder's `6018624750`. **Decisions**:
    OQ-H-22, OQ-H15-18, -19, -20.
  - **After**: T027 (N-6 (a), ruled).
  - **Files**: as listed (single owner of `0003_` and of the five suites).
  - **Lane**: 4.
- [ ] T043 [P] [US4] [oDc] **HA-3, `tests/fixtures/health-corpus`.** 14.9's corpus:
  ONE planted instance per kind requirement 14 names (`broken-link`,
  `derivable-front-matter`, `stage-location-mismatch`, `near-duplicate`, a
  `human-only` finding, the accepted finding), plus ONE EMPTY STUB, which
  requirement 14's third scenario names as `assisted` (ADV-17). Each planted
  finding's document is named after its old literal id, so batch Q's selection
  lines find it by `path`. Measure the `plain-documents` fixture and declare the
  inbound-link exemption (OQ-H-16).
  - **Realizes**: 14.9.
  - **Falsifier**: new `tests/test_health_corpus_fixture.py`.
  - **Decisions**: OQ-H-8, OQ-H-16.
  - **After**: T027 (N-6 (a), ruled).
  - **Files**: `tests/fixtures/health-corpus/**` (single owner), the test.
  - **Lane**: 4.

### W2

- [ ] T044 [US4] [oDc] **HA-2, the neutral families (detection).** New
  `src/opendox/health/families.py`: broken links (moved targets detected
  structurally, OQ-H-10), orphans (README and index exempt, OQ-H-16), empty stubs
  (`assisted`) and stale stubs (`human-only`) by the criteria data-model.md
  § Families declares (ADV-17, ADV-40), derivable front matter,
  `stage-location-mismatch` by the six role keys' top-level directories (R2Q11
  (a)), near-duplicates (OQ-H-21: measure whether `doxbench_knowledge` runs with
  no binding; set and record the threshold); each family supplies a
  position-independent identity key (N-13); the engine files excluded (OQ-H-15).
  Model-free (OQ-H-20).
  - **Realizes**: 14.4 (part: detection), 6.2 (part: the check's body).
  - **Falsifier**: new `tests/test_health_families.py`, over T043's corpus,
    including the empty stub's class and an id that survives an edit above its
    finding.
  - **Ruled**: R2Q10, R2Q11, R2Q14. **Decisions**: OQ-H-8, -10, -11, -15, -16,
    -20, -21; N-13.
  - **After**: T041, T043.
  - **Files**: new `src/opendox/health/__init__.py`, `src/opendox/health/families.py`,
    the test.
  - **Lane**: 4.
- [ ] T045 [US6] [oDc] **G15-A, the pack contract.** Extend `health_contract.py`
  (handed over at T041's landing) with the pack protocol: the static declaration
  `opendox-pack.yaml` (read before any pack code runs; no version, or forbidden
  keys, refused; each family declaring its `kind`, its own `version` and its
  `applies_to` globs, data-model.md § Pack declaration, with a finding of an
  undeclared kind or outside its family's globs refused), the one-JSON-document stdout format, and the patch type, a
  unified diff and nothing else (15.2; ADV-12). Python is the only pack runtime.
  - **Realizes**: 15.1, 15.2.
  - **Falsifier**: new `tests/test_check_pack_contract.py`, including a family
    missing its version or its `applies_to`, refused; a finding of an
    undeclared kind, and one outside its family's globs, each refused as a
    finding against the pack.
  - **Ruled**: R2Q18, R2Q20. **Decisions**: N-3, OQ-H15-1, -10, -11.
  - **After**: T041.
  - **Files**: `src/opendox/health_contract.py` (second, appended), the test.
  - **Lane**: 3.

### W3

- [ ] T046 [US4] [oDc] **HA-5, the engine, the baseline and `health run|list`.**
  New `health/engine.py` and `health/baseline.py`: the three run kinds R2Q12 (a)
  names (default-tip, branch, working-state; N-10, as ADV-16 corrected it); in a
  working-state run only the built-in families read the working copy, while
  every pack still gets the committed export of HEAD (`git archive`, 15.1b) and
  no untracked file reaches a pack; the built-in families in process, attributed
  `opendox`; the baseline classes and disappearance rules of R2Q12 (a), with the
  baseline branch `main`, else the branch HEAD names (I-2 (a), ruled), each run's
  pack inventory recorded and read for a pack's previous pin (a newly added
  pack's findings, and those of a pack whose digest or commit moved under an
  unchanged version, are `pack-upgrade`; data-model.md § Baseline classes); only a
  complete, full default-tip run becomes a baseline or measures a
  disappearance, and an id it suppresses as accepted is never one (Copilot's
  review of `2076f24b`); each run
  reads the dispositions file in what it reads (N-14); the engine hook G15-E
  calls; the per-pack budget, `--timeout`, default 60 seconds, capped at 600,
  a whole number of seconds of at least 1 (OQ-H15-5); id-collision detection
  over the whole run, families and packs alike, before anything is stored
  (contracts/health-finding.md § The id rule). New `health/cli.py`: the `health` group with 14.5's exact shapes
  (`run`, `list`, `fix --finding ID [--batch]`, `accept`), plus `--local` and
  `list --class`, frozen, `fix` and `accept` dispatching to T053's and T054's
  modules; contributed through `default_profile.py` (N-2); `--json` carries
  `kind` and `identity` (the holder, `6018624750`). The hosted plane refuses by name (R2Q15 (a)). Record the hook line for
  the root README (CF-6).
  - **Realizes**: 14.4 (part: on demand, the baseline), 14.5 (part: CLI run/list).
  - **Falsifier**: new `tests/test_health_cli.py`, `tests_runtime/test_health_engine.py`
    (including a repository on `main`, since #1144's falsifiers never exercise
    the baseline there, C-14; a repository on another branch, I-2 (a); a pack
    with zero findings in the baseline, then upgraded; a newly added pack; a
    pack whose digest changes under an unchanged `version`, its new findings
    `pack-upgrade`;
    interleaved runs of two corpora in one store, each classed against its own
    baseline, with `list`, `fix` and `accept` reading only their own corpus's
    runs; a `--pack` run, a run where a pack failed, a run with no live sandbox
    and a run whose manifest entry is refused, each at the tip between two
    complete runs, after which the restored full run is classed against the
    earlier complete baseline and reports no disappearance from the partial run; a finding accepted after
    a baseline, which the next tip run neither lists nor reports as
    disappeared; three consecutive default-tip runs where a finding vanishes
    uncited, the second carrying one `uncited-disappearance` re-raise and the
    third raising nothing for either id; two findings with one identity key from
    one family, and a forced 16-digit hash collision at two paths through the id
    function's test seam, each run storing ONE `identity-collision` finding,
    path as the contract rules, and neither colliding finding; and `--timeout`
    `0`, `-5`, `1.5` and `abc` refused before any pack runs, `900` run at 600).
  - **Ruled**: R2Q9 (items 2, 7), R2Q10, R2Q12, R2Q15. **Decisions**: I-2, CF-6,
    N-2, N-10, N-14, N-19, OQ-H15-5.
  - **After**: T042, T044.
  - **Files**: new `src/opendox/health/engine.py`, `baseline.py`, `cli.py` (first:
    T046 → T053 → T054); `src/opendox/cli.py` (third); `src/opendox/default_profile.py`
    (third); the tests.
  - **Lane**: 4.
- [ ] T047 [US6] [oDc] **G15-B, the manifest, the pin and the second copy.** New
  `check_pack_manifest.py` reads `health/packs.yaml` (`contracts/health-packs-manifest.md`):
  exactly 15.1a's fields; the id `opendox` reserved, and every id 1 to 40
  characters of `[a-z0-9-]` (a 41-character id refused); a corpus-relative entry that
  carries `commit` REFUSED (15.1a, `#1144 tasks.md:3414-3421`; lane 3's T047 FIX);
  `sorted-ls-tree-r-v1` over `<corpus-commit>:<source>` for a corpus-relative
  source and over the declared `commit`'s root tree for a git-URL source (the
  contract's digest rule; fixed before any fixture digest is committed); the
  contract's CONTAINMENT rule: a symlinked `source` component or any symlink in
  the pack's pinned tree refused, the tree materialized into a directory the
  engine owns, and every host-resolved pack path checked beneath it after
  `realpath` before it is read or bound; git sources fetched by the engine into `OPENDOX_STATE_DIR` over
  `https://` or `ssh://` only, with `file://`, `ext::`, local paths and credential
  URLs refused and the runtime's hardened transport rules reused (ADV-21); no
  budget or bound keys. Copy T040's manifest schema at T060's pinned commit into
  the copy record after T041 (the validator gains the `opendox-health-packs` kind).
  - **Realizes**: 15.1a, 15.7 (part: the reserved id).
  - **Falsifier**: new `tests/test_check_pack_manifest.py`, including hostile
    sources: a `source` that is a symlink to a directory outside the pinned
    tree, a pack whose `opendox-pack.yaml` is a symlink to a file outside it,
    and a pack holding a symlinked module, each refused as a finding against
    the entry with no file of the target read and no pack code run;
    `tests/test_validator_input_set.py`.
  - **Ruled**: R2Q18, R2Q21, R2Q22. **Decisions**: OQ-H15-12, -14, -19; N-15.
  - **After**: T045, T041 (the copy record; lane 3's split condition 2).
  - **Files**: new `src/opendox/check_pack_manifest.py`, the test;
    `src/opendox/contracts/copies.yaml`, `schemas/`, `__init__.py`,
    `tests/test_validator_input_set.py` (second), and the validator's kind map.
  - **Lane**: 3.
- [ ] T048 [P] [US6] [oDc] **G15-C, the sandbox runner.** New
  `check_pack_sandbox.py` and `check_pack_shim.py`: `bwrap` at a fixed path with
  the version floor; the probe; the per-run canary (product behaviour,
  OQ-H15-9), planting a CANARY variable and a CANARY descriptor before spawning
  (15.6a); the export (`git archive <commit>` of the commit the run reads,
  HEAD's in a working-state run, never the working copy; unsteerable by
  `export-subst`/`export-ignore`, R2Q9 (a) item 5); the read-only mount set
  R2Q18 (a) fixes: the install's interpreter, its standard library and
  `opendox.health_contract` alone, never `site-packages`, `$HOME` or the
  checkout (lane 3's T048 FIX); 15.1b's COMPLETE invocation (Copilot's review
  of `55cc1334`): `--unshare-all` (network, PID, IPC, UTS and user namespaces),
  `--die-with-parent`, `--new-session`, `--ro-bind <copy> /corpus`, `--ro-bind
  <pack> /pack`, the read-only interpreter binds above, a private `--tmpfs
  /tmp`, its own `--proc /proc`, a minimal `--dev /dev`, and `--clearenv` then
  `--setenv` of 15.1b's allowlist alone; spawned with `close_fds=True`, stdin
  from `/dev/null` and the two output pipes only; the PID namespace means ending
  the sandbox's init ends the whole tree; with no
  live sandbox, no pack runs and one install-level finding says why. The probe
  also records whether a delegated cgroup's `pids.max` bounds the process
  count; where none is delegated the count is unbounded, an accepted limit the
  run records (`health_runs.sandbox`). F15.1's platform precondition is asserted
  (R2Q9 (a) item 3). The fail-not-skip helper
  the tests use under `CI` lives in its own test module,
  `tests/sandbox_required.py`, never a shared conftest.
  - **Realizes**: 15.1b, 15.6 (part: enforcement), 15.5 (part).
  - **Falsifier**: new `tests/test_check_pack_sandbox.py`, run in the required
    job with the sandbox live, including the engine's process killed mid-pack
    with no pack process left alive (`--die-with-parent`), the pack in a new
    session that cannot reach the engine's terminal (`--new-session`), writes
    to `/corpus` and `/pack` refused, a private `/tmp`, and the sandbox's own
    `/proc` showing only the pack's descriptors; `EXPECT_SKIPPED` still 11.
  - **Ruled**: R2Q9 (items 3, 5), R2Q16, R2Q17, R2Q18, R2Q19. **Decisions**:
    OQ-H15-5, -9, -21.
  - **After**: T045, T010.
  - **Files**: new `src/opendox/check_pack_sandbox.py`, `check_pack_shim.py`,
    `tests/test_check_pack_sandbox.py`, `tests/sandbox_required.py`;
    `pyproject.toml` only if package data is needed (first: T048 → T055 → T061).
  - **Lane**: 3.
- [ ] T049 [P] [US6] [oDc] **G15-D, the patch validator.** New
  `check_pack_patch.py` checks each patch, a unified diff and nothing else
  (ADV-12), BEFORE any branch exists, refusing (lane 3's T049 FIX, `#1144
  tasks.md:3461-3479`): an edit of any path other than its own finding's `path`
  (a finding with no document carries no patch); an absolute path, a `..`
  component, or a `.git` component in any letter case; a target that is a
  symbolic link in the corpus or lies below one; a create, delete, rename, copy,
  re-mode or binary patch (`new file mode`, `deleted file mode`, `rename from`,
  `copy from`, `old mode`, `GIT binary patch`); and a patch over 65,536 bytes,
  the engine's bound, never read from the pack. Each refusal is a finding against
  the pack naming `refused_patch` and `reason`. A passing patch reaches `git apply
  --check` against the draft's base. The patch is validated at `run` and again at
  `fix`, after T056 re-obtains it (OQ-H15-20).
  - **Realizes**: 15.2a.
  - **Falsifier**: new `tests/test_check_pack_patch.py`, one case per refusal.
  - **Decisions**: OQ-H15-20.
  - **After**: T045.
  - **Files**: new `src/opendox/check_pack_patch.py`, the test.
  - **Lane**: 3.
- [ ] T050 [US6] [oDc] **G15-H, the display facet's health roles.** A health
  role family keyed by pack and family id (the label keys T045's declaration
  defines), under a schema-version bump; a host profile's labels win; labels
  render as text. A guard test that the tables T025 inlined into
  `staging-workbench-model.js` equal `display.js`'s, so the two copies cannot
  drift (W-1 (A), ruled; lane 3's T050 FIX).
  - **Realizes**: 15.3.
  - **Falsifier**: the display-facet tests, extended; the inline-parity guard.
  - **Decisions**: OQ-H15-15, W-1.
  - **After**: T045 (lane 3's T050 FIX), T027 (N-6 (a), ruled).
  - **Files**: `src/opendox/display_profile.py`, `src/opendox/web/views/display.js`,
    their facet tests (single owner), new `tests/test_display_tables_inline_parity.py`.
  - **Lane**: 4.
- [ ] T051 [oDc] **Phase 5's CI floors, once per wave.** Re-pin `MIN_SELECTED`
  and `MIN_PASSED` after each wave's landings; `EXPECT_SKIPPED` stays 11.
  - **After**: T017; then each wave's last openDox-code landing.
  - **Files**: `.github/workflows/validate.yml` (third edit).
  - **Lane**: 4.

### W4

- [ ] T052 [US4] [oDc] [oxF] **HA-4, Group 6 at the seam (and F6.1).** The entry
  point registers openDox's own check, the engine's built-in families attributed
  `opendox`, at the scoped seam (`register_health_check`, `workbench.py:1622`;
  `run_scoped_doc_health`, `:1666`; ADV-29 corrected the cite) ONLY when the seam
  is empty; a host's check, registered through the same call, REPLACES it, in
  process and unstored (R2Q16 (a); ADV-18), so openxFactory's
  `scripts/opendox_host.py:524` registration keeps working at T064's pin. Both
  registration orders are tested. The registered check's default scoped families
  answer a call that names none (OQ-H-2); a scoped run is not stored (OQ-H-3).
  Registration lines in `cli.py` and `serve.py`. openxFactory's
  `tests/domain_profile/test_openxfactory_host_wiring.py` adapts at T064's pin (an
  arc landing on 11.1's surface). At the tick, record 6.1's re-measure (38 modules;
  `lines.py` and `fs_probe.py`, research.md R4) and 6.1a's vacuous satisfaction
  (R2Q14 (a)).
  - **Realizes**: 6.1, 6.1a, 6.2, F6.1.
  - **Falsifier**: F6.1 as batch Q amends it (an entry point built first);
    new `tests/test_health_check_seam_registration.py` (both orders).
  - **Ruled**: R2Q9 (item 1), R2Q14, R2Q16. **Decisions**: OQ-H-2, OQ-H-3.
  - **After**: T044, T046, T005.
  - **Files**: `src/opendox/workbench.py` (single owner), `src/opendox/cli.py`
    (fourth), `src/opendox/serve.py` (fourth), the test; openxFactory's host-wiring
    test rides T064.
  - **Lane**: 4.
- [ ] T053 [US5] [oDc] **HA-6, the fix loop.** New `health/applier.py`: `fix
  --finding ID` writes `health-fix-<id>`, and `--batch` adds the repair to the
  open batch draft `health-fix-batch` (14.5's shape; N-19), each branched at HEAD in
  the applier's own worktree, so HEAD and the working tree never move, and never
  `main`; `auto-fix` applies the family's repair or the pack's patch, which T056
  re-obtains and T049 re-validates before any branch exists; `assisted` writes
  the deterministic proposal (near-duplicates and empty stubs, OQ-H-11);
  `human-only` is refused with no branch, and so is a working-state run's
  finding (commit, run again, fix the fresh finding); `--batch` grows the open
  batch only at its base, refusing by name when HEAD has moved past it
  (data-model.md § Fix draft); every repair commit carries a
  `Finding: <id>` trailer for the finding it repairs, so a landing cites by git
  alone (data-model.md § Fix draft); the draft lands only through `land`
  (T016; OQ-12-17). `fix`'s dispatch line in `health/cli.py`.
  - **Realizes**: 14.6, 14.7.
  - **Falsifier**: new `tests/test_health_fix.py` (F14.1's fix loop, by fixture
    document, R2Q10 (a); the empty stub's proposal; a two-repair batch, each
    commit carrying its `Finding:` trailer, landed and its branch deleted, after
    which the next tip run counts both disappearances cited; a working-state
    run's finding refused with no branch, naming commit and re-run; and a stale
    batch, HEAD advanced after its first repair, whose second `--batch`
    repair is refused with no commit made).
  - **Ruled**: R2Q5, R2Q10, R2Q11. **Decisions**: OQ-H-8, -10, -11, OQ-12-17,
    OQ-H15-20, N-19.
  - **After**: T046, T049, T016.
  - **Files**: new `src/opendox/health/applier.py`, `src/opendox/health/cli.py`
    (second), the test.
  - **Lane**: 4.
- [ ] T054 [US5] [oDc] **HA-7, exceptions in git, and the third copy.** New
  `health/exceptions.py` reads and writes `health/dispositions.yaml`
  (`contracts/health-exceptions.md`); suppresses, never downgrades; refuses another
  `kind` by name, and a repeated `finding` id; `accept` refuses an id already
  accepted (contracts/health-exceptions.md); `accept` writes the working tree in a checkout and a draft
  branch with none (OQ-H-14); a run reads the file in what it reads (N-14); the
  engine files join the settings-document exclusion (OQ-H-15). Copy T040's
  exceptions schema at T060's pinned commit into the copy record after T047 (the
  validator gains the `opendox-health-dispositions` kind). `accept`'s dispatch
  line in `health/cli.py`.
  - **Realizes**: 14.8.
  - **Falsifier**: new `tests/test_health_accept.py`, including a second
    `accept` of one id, refused with the file unchanged; a hand-written file
    with a repeated id, refused as a whole; an id accepted
    after a baseline run that held it, which the next tip run suppresses and
    never re-raises as an uncited disappearance; a reset-survival test in
    `tests_runtime/` (an exception survives `runtime reset`); `tests/test_validator_input_set.py`.
  - **Ruled**: R2Q10, R2Q22. **Decisions**: OQ-H-13, -14, -15; N-14, N-15.
  - **After**: T046, T053 (`health/cli.py`), T047 (the copy record; lane 3's split
    condition 2).
  - **Files**: new `src/opendox/health/exceptions.py`, `src/opendox/health/cli.py`
    (third), `src/opendox/contracts/copies.yaml`, `schemas/`, `__init__.py`,
    `tests/test_validator_input_set.py` (third), the tests.
  - **Lane**: 4.
- [ ] T055 [US6] [oDc] **G15-G, `tests/fixtures/pack-corpus`: 15.6a's EIGHT packs,
  by their exact names** (ADV-03; lane 3's two T055 FIXes). T043's `health-corpus`,
  plus `packs/` and a `health/packs.yaml` registering all eight by corpus-relative
  `source`, pinned by digest, with NO `commit` (15.1a):
  - `fixture-crashing-pack`: raises on its first family;
  - `fixture-slow-pack`: sleeps past any timeout;
  - `fixture-writing-pack`: tries to write, commit and merge in the tree it is
    given, and lets the operating system's refusal PROPAGATE;
  - `fixture-escaping-pack`: tries each escape in turn, and reports which
    succeeded: restores write permission and WRITES (the write, never the chmod,
    counts as success; R2Q9 (a) item 6), follows a symlink planted to point out of
    its copy, opens a network connection, reads `$HOME`, looks for the engine's
    CANARY environment variable, and walks `/proc/self/fd` for the engine's CANARY
    descriptor;
  - `fixture-forking-pack`: forks a child that sleeps past the budget, the child
    carrying its own pack id in argv (R2Q9 (a) item 4), so F15.1's `ps` check
    cannot pass vacuously;
  - `fixture-garbage-pack`: writes bytes that are not the neutral shape to stdout,
    and exits 0;
  - `fixture-anonymous-pack`: declares no version, while its manifest entry names
    one;
  - `fixture-patching-pack`: returns six findings, each naming its own document
    and carrying a patch: `patch-ok`, a valid edit, and one of each kind 15.2a
    refuses, `patch-other-document`, `patch-traversal`, `patch-git-metadata`,
    `patch-rename` and `patch-oversized`.
  A test keeps the fixture digests current.
  - **Realizes**: 15.6a.
  - **Falsifier**: new `tests/test_pack_corpus_digests.py`.
  - **Ruled**: R2Q9 (items 4, 6). **Decisions**: OQ-H15-12.
  - **After**: T043, T045, T047, T048 (`pyproject.toml`).
  - **Files**: `tests/fixtures/pack-corpus/**`, the test; `pyproject.toml` only if
    package data is needed (second).
  - **Lane**: 3.
- [ ] T056 [US6] [oDc] **G15-E, the engine integration, and the bounds measured.**
  New `check_pack_engine.py`, called from T046's hook: runs each manifest entry
  in the sandbox under the engine's budget; stamps `pack_id`/`pack_version` from
  the manifest entry; validates each returned patch through T049 and stores only
  the finding (a refusal names `refused_patch` and `reason`; no patch text);
  re-obtains one finding's patch at `fix` by re-running that one pinned pack
  (OQ-H15-20) only at the run's recorded `pack_pins` entry and `export_commit`,
  refusing by name, with no branch, when the current pin or HEAD differs or the
  re-run does not reproduce the finding's id (data-model.md § Finding; Copilot's
  review of `3f807204`); records each run's `pack_pins` and `export_commit`; turns a crash, timeout, bound hit, bad stdout or refused output
  into a finding against that pack, storing none of its output and no stderr
  (only the failure's category, exit status, and stderr's byte count and
  SHA-256; OQ-H15-11, refined), each such finding with its engine-owned identity
  key (`category`, `entry`; contracts/health-finding.md) and one id across runs,
  and keeps the view, the classes, the baseline and the landing rule the
  engine's (15.4). Measure the bounds' defaults against T055's `pack-corpus`
  before fixing them (ADV-22): address space, CPU, file size, tmpfs and stdout
  through rlimits and `bwrap`, the process count through `pids.max` where a
  cgroup is delegated, never `RLIMIT_NPROC`, which setrlimit(2) counts per real
  user (lane 3's bwrap-facts FIX). Owns nothing of Group 14's.
  - **Realizes**: 15.4, 15.5 (part), 15.6, 15.7 (part: stamping).
  - **Falsifier**: new `tests/test_check_pack_engine.py`, including a `fix`
    refused with no branch after the manifest's digest changes under an
    unchanged `version`, and after HEAD moves past the run's `export_commit`;
    the measurement quoted in its PR.
  - **Ruled**: R2Q16, R2Q18, R2Q21, R2Q25. **Decisions**: OQ-H15-5, -11, -18, -19,
    -20.
  - **After**: T046, T042, T047, T048, T049, T055.
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
  from git at render time, labels and messages as text; every action the CLI has.
  New `health/routes.py` (`contracts/cli-http-health.md`), contributed through
  the default profile's `ROUTE_EXTENSIONS` and `HANDLER_CONTRIBUTIONS`; the
  `/capabilities` `health` block is present only under openDox's own profile,
  with values derived from those bindings, listing every resolution action the
  view offers (14.5), so a host profile sees no `health` key (ADV-14); the
  hosted plane refuses by name. Wiring in `web/app.js` and
  `web/index.html`; census rows.
  - **Realizes**: 14.5.
  - **Falsifier**: `tests/test_health_parity.py`'s three named tests
    (`test_the_health_view_is_served`, `test_every_view_action_has_a_cli_verb`,
    `test_every_cli_verb_is_offered_by_the_view`); a test that pack labels
    render as text.
  - **Ruled**: R2Q15, R2Q25. **Decisions**: N-2, OQ-H15-15.
  - **After**: T046, T052 (`serve.py`; lane 3's T057 FIX), T053, T054, T050, T056.
  - **Files**: new `src/opendox/web/views/health.js`, `health-model.js`, new
    `src/opendox/health/routes.py`, `src/opendox/default_profile.py` (fourth),
    `src/opendox/serve.py` (fifth), `src/opendox/web/app.js`,
    `src/opendox/web/index.html`, `tests/fixtures/web_boundary_census.yaml`,
    `tests/test_web_boundary.py`, new `tests/test_health_parity.py`.
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

### W6: F15.1 live in CI, the cut's openDox-code and pins, evidence, checkpoint

- [ ] T067 [oDc] **F15.1's shell block in the required job (the CI owner;
  ADV-13).** Add F15.1's command, as batch Q amends it, as a step of the required
  `validate` job (pinned `ubuntu-24.04`, bubblewrap installed and the sandbox
  proved live by T010's step): the `pack-corpus` run under `timeout 120`, the
  `ps` check, the tamper re-run and the patch loop. A sandbox that is not live
  FAILS the step under `CI`; it never skips.
  - **Realizes**: F15.1 (part: its shell block where a sandbox is live).
  - **Falsifier**: the step green in the job's own run, quoted.
  - **Ruled**: R2Q9 (item 3), R2Q17. **Decisions**: N-4.
  - **After**: T058, T051, T005.
  - **Files**: `.github/workflows/validate.yml` (fourth edit).
  - **Lane**: 4.
- [ ] T068 [oDc] **R2Q17 (a)'s 26.04 measurement (non-gating).** When GitHub's
  `ubuntu-26.04` image is available to the organization, run T010's live sandbox
  proof and the sandbox tests on it in a non-required workflow run, and record the
  result in `evidence/runner-26.04.md`. Release 2 stays on `ubuntu-24.04`; moving
  the required job is a separate required-check change on Brett's word (N-18;
  lane 3's R2Q17 FIX).
  - **Ruled**: R2Q17. **Decisions**: N-18.
  - **After**: T048.
  - **README**: links `evidence/runner-26.04.md`.
  - **Lane**: 4.
- [ ] T061 [oDc] **The release step: 0.2.0.** Bump openDox-code's version to
  0.2.0, the LAST package-changing openDox-code landing before T062 (plan 034's
  T101 form). It NEVER waits for the direction arc: T072 rides it only if T072 has
  already landed; a late T072 rides the arc's own pin (ARC-6; ARC-Q3 (a); ADV-06;
  lane 3's T072 FIX).
  - **Ruled**: R2Q23; ARC-Q3. **Decisions**: ARC-6.
  - **After**: every package-changing phase-5 openDox-code landing (T041–T058,
    T067).
  - **Files**: `pyproject.toml` (third, last).
  - **Lane**: 4.
- [ ] T062 [oD] **Phase 5's openDox root code pin (steps 1–2).** As T027, to
  T061's commit (P), in ONE commit; the root README gains the `health` section and
  its hook line (CF-6).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: `make pins`.
  - **After**: T061, T060.
  - **Files**: openDox root `code` gitlink, `contracts/code-pin.yaml`; `README.md`
    (second edit).
  - **Lane**: 4.
- [ ] T063 [oXc] **Step 3, and 12.5 still green.** openXdox-code's `opendox @`
  pin to P; the composed workflow re-runs 12.5's 16 suites green (US3: every
  phase).
  - **Realizes**: 9.5 (part).
  - **Falsifier**: F12.1, composed, at P.
  - **After**: T062; T028 (phase 4's pin first; under N-6 (a) phase 5 no longer
    waits for T033, so the pin order is named here).
  - **Files**: openXdox-code `pyproject.toml` (second).
  - **Lane**: 4.
- [ ] T064 [US3] [oX] [oxF] **Steps 5–6: phase 5's consumer pins and host
  wiring.** As T030, carrying T052's host-wiring test adaptation, phase 5's
  `edits[].note`s, and the proof that openxFactory's help golden and
  `/capabilities` are unchanged, key for key (inventory HA-9's place; N-2;
  ADV-14). Then `tests/composed_host_pin.yaml` advances, and T073 re-runs after
  it (lane 3's composed_host_pin FIX).
  - **Realizes**: 9.5 (part), 11.1 (part).
  - **Falsifier**: the pin verifiers; openxFactory's required checks green (SC-005).
  - **After**: T063, T059; T030 (phase 4's consumer pins and host wiring first;
    N-6 (a)).
  - **Files**: openXdox root pins; openxFactory gitlinks, pin files and host wiring
    (second); openXdox-code `tests/composed_host_pin.yaml` (after).
  - **Lane**: 4.
- [ ] T065 [US4] [US5] [US6] [oxF] **Phase 5's evidence.** Run F6.1, F14.1 and
  F15.1 as batch Q amends them, at P, and quote them; F15.1 from T067's step in
  the required job with the sandbox live, and its 24 nodes from T058; the interim
  F11.1 (T093). `evidence/f6.1-run.md`, `f14.1-run.md`, `f15.1-run.md`,
  `f11.1-phase5.txt`.
  - **Realizes**: F6.1, F14.1, F15.1 (ticked at T082); F11.1 (interim).
  - **After**: T064, T067, T005.
  - **README**: links the four files.
  - **Lane**: 4.
- [ ] T066 [oxF] **Phase 5 checkpoint.** `evidence/checkpoint-phase5.md` quotes
  T065's runs and T063's composed run (SC-002, SC-003).
  - **After**: T065.
  - **README**: links `evidence/checkpoint-phase5.md`.
  - **Lane**: 4.

---

## Requirement 9 for openXdox-code (ARC-Q2 (a)): #1144's work, lane openXfactory-3

Moved here from the arc's section by review round 1 (lane 3's T073 FIX and split
condition 3): T073 realizes #1144's requirement 9 for openXdox-code, by
declaration, as batch Q's F9.1 amendment states it, so it carries #1144's `Arc:`
value, stays lane 3's, and is NOT gated on the arc's ratify word (T071).

- [ ] T073 [US3] [oXc] **The composed declarations (ARC-Q2 (a)).** U-9's workflow
  gains R1Q24's 3 rail files (the rail registered in `tests/conftest.py`, as U-1
  registers the host), its 5 contracts files and the governed-behaviour files a
  lone checkout cannot run; `tests/declared_exclusion.yaml`'s entries become
  declared composed integration tests with count and reason, matching batch Q's
  F9.1 amendment. It re-runs after each `tests/composed_host_pin.yaml` advance
  (after T030, T064 and T075), because each moves the openxFactory commit its
  composed run checks out (lane 3's composed_host_pin FIX).
  T073 lands what its own files can (the holder's option (a), `6016982816`,
  answering lane openXfactory-3's question `6016925160`): the declaration, every
  entry a declared integration test with its count and each reason unchanged; the
  rail registration, as measured; and the `composed.yml` step that runs every
  entry outside 12.5's set, composed and each file alone, so that none is dropped
  from both suites. The step goes green only when the repair slices land (T094's
  map, T095+), so T073's PR stays a DRAFT until they do. Options (b) and (c) of
  that question are not taken.
  **The `open_until` wording** (the holder, `6016982816`): `id`, `reason` and
  `ruled` stay byte-identical, and no commit id appears outside the pin file.
  - The `doc_health` reason's `open_until` keeps its words and gains lane 3's
    clause, *"; run composed, as a declared integration test, by
    .github/workflows/composed.yml at the openxFactory commit
    tests/composed_host_pin.yaml names (ARC-Q2 (a), openxFactory#656 comment
    6003918488)"*.
  - The `status-exemption-rail` and `openxfactory-contracts` reasons drop "the
    doc_health direction arc (plan 034 T008)", because under ARC-Q2 (a) the arc
    does not clear them. Each reads instead: *"never in a lone checkout: a
    declared integration test, run composed by .github/workflows/composed.yml at
    the openxFactory commit tests/composed_host_pin.yaml names (ARC-Q2 (a),
    openxFactory#656 comment 6003918488)"*.
  - **Realizes**: requirement 9 for openXdox-code, by declaration (F9.1 as
    amended; F9.1 is already `[x]`, so the re-run is quoted, not ticked).
  - **Falsifier**: F9.1 as batch Q amends it; the composed workflow green. It
    stands as written (`6016982816`).
  - **Ruled**: ARC-Q2; the holder's `6016982816`.
  - **After**: T029, T005, and T095+ (the repair slices cut from T094's map). Its
    PR stays a DRAFT until they land.
  - **Files**: openXdox-code `tests/conftest.py` (after T021 and T026: T020 →
    T021 and T026, in landing order → T073 → T074), `tests/declared_exclusion.yaml`
    (first), `.github/workflows/composed.yml` (second), and a new
    `tests/test_declared_rail_registration.py`, the committed test of the
    conftest rail block: 5 lone cases with stand-in rails, so that the committed
    tests in CI kill all seven mutants of the block (C1 to C7; C5 to C7 died only
    to uncommitted probes before it). Only T073 writes it, so it creates no
    single-writer conflict (the holder's ruling `6020698021`, answering lane
    openXfactory-3's question `6020683941`: fix-now, as T022 and T023 were ruled).
  - **Lane**: 3.
- [ ] T094 [oXc] **R2-INV-R9: the map of every composed red outside 12.5's set.**
  READ-ONLY, in lane 3 (claimed on `#656`, `6017801219`; the holder's ruling
  `6016982816`). It maps, as R2-INV-P4F mapped 12.5's 174 reds, every composed
  red outside 12.5's set in openXdox-code's declared exclusion: the 5
  `openxfactory-contracts` files, the 33 red `doc_health` files, and the rail node
  `tests/test_doxbench_packet.py::test_the_status_read_agrees_with_the_repositorys_own_corpus_reader`.
  For each file the map names:
  - its cause class and the means that finish it;
  - any overlap with T074's 7 respelled tests, and with the files of T023 to T028;
  - whether it is a protected suite. If it is, F12.1's allow-list applies, with
    `--chains`.

  It ends with a slice outline for T095+, one owner per file. Output:
  `lane-coord-034/r2/R2-INV-R9.md`, beside R2-INV-P4F, and one line in
  `lane3-to-lane4.log`. No pull request, no edit to any repository, no push.
  - **Ruled**: ARC-Q2; the holder's `6016982816`.
  - **After**: none (read-only; T073's measurement, `6016925160`, is its
    starting point).
  - **Lane**: 3.
- [ ] T095+ [oXc] **The repair slices cut from T094's map.** New tasks, numbered
  from T095 as the map cuts them, in lane 3 (the holder, `6016982816`): one
  repair slice per owner of the files the map names, each with its own Files
  line, falsifier and After. They make T073's `composed.yml` step green, and
  requirement 9 closes for openXdox-code when that step is green. A slice that
  edits a protected suite adds its allow-list entry in its own PR, chained as
  F12.1's `--chains` allows. T073's After set gains every slice, and T073's PR
  stays a DRAFT until they land.
  - **Ruled**: ARC-Q2; the holder's `6016982816`.
  - **After**: T094.
  - **Files**: as the map names them, one owner per file; a file another open
    slice owns is never edited.
  - **Lane**: 3.

---

## Beside phase 5: the `doc_health` direction arc's realization (ARC-Q1–ARC-Q4)

Ruled on `#656` `6003918488`. Its OWN OpenSpec change, owned by lane
openxfactory-4 under this plan; it gates neither release 2's close nor #1144's
archive (ARC-Q3 (a)), so T061 never waits for it (ARC-6) and #1144 may archive
with F9.2 open (tier 1's ARC-5); F12.1 stays composed, and the composition is
permanent (tier 2's CF-5). Its realization landings carry the change's own
trailer value (decision ARC-4), not #1144's, and its change runs an equivalent
surfaces check over them (ADV-37).

- [x] T070 [oxF] **Author the change.** `openspec/changes/<ARC-2>/`: `proposal.md`
  with `code_surface:` naming openXdox-code, openDox-code and openxFactory host
  wiring, and `target_release: implemented` (tier 1's ARC-1, ruled); `design.md`
  (the eight modules, fact 1 of R2-ARC-ASK; the seams; the re-authored `lines`
  slice; the 7 respelled tests; F9.2's three removals; the surfaces check over its
  own landings, ADV-37); `tasks.md`; `.openspec.yaml` (`skip_specs: true`; if the
  seams need contract text, an openXdox-spec delta written into this change, which
  T071's ratify word then covers, ARC-3); the README "OpenSpec Records" bullet;
  the corpus-ledger row. Validated through the pinned CLI entrypoint. Under a
  Rule 6 window.
  - **Ruled**: ARC-Q1, ARC-Q3. **Decisions**: ARC-1, ARC-2, ARC-3, ARC-4.
  - **After**: T004.
  - **Lane**: 4.
  - **Landed**: DONE, openxFactory#1247 → `51456835` (2026-10-06T14:38:36Z), the
    change `realize-doc-health-direction-arc`. T071's ratify word is still to come.
- [ ] T071 [oxF] **Brett's ratify word, and its record.** Put the change to
  Brett; record his word on `#656` and the change's ratification record, under a
  Rule 6 window. No realization slice starts before it.
  - **After**: T070.
  - **Lane**: 4.
- [ ] T072 [oDc] **Re-author the generic `lines` slice in openDox-code.** A small
  stdlib module carrying `split_keepends`, `join_rows` and the few git reads
  `RealGit` gives the generator; nothing is relocated out of openxFactory
  (R2Q14 (a), 11.1). OPPORTUNISTIC (ARC-6; ADV-06): it rides T061's pin only if it
  has already landed; T061 never waits for it, and a late T072 rides the arc's own
  pin chain.
  - **Falsifier**: the module's own tests; openDox-code's whole suite.
  - **Ruled**: ARC-Q1, ARC-Q3. **Decisions**: ARC-6.
  - **After**: T071.
  - **Lane**: 4.
- [ ] T074 [oXc] **Declare the seams, retarget the eight modules, respell the
  seven tests.** openXdox-code declares seams for corpus loading and status
  reading (generator, `corpus_root`, `gate_console`), `derive_possibles`' index
  and disposition (`gate_console`, `cli_gate`, `gate_routes`), the readiness
  renderer and the pin sentinel (`snapshot_registry`); `completeness.py`,
  `round_trip.py` and `generator.py`'s generic half import T072's module; the 7
  test files that import `doc_health` directly are respelled (none protected);
  `DOC_HEALTH_SURFACE` falls to empty; the `doc_health` exclusion reason empties;
  the help-tree test's `--deselect` in the required check and its guard test
  leave together (F9.2's two code removals). Until T075 moves the registration
  into openxFactory's host wiring, the composed conftest registers the governed
  implementations from the composed tree's `scripts/`, so the 12.5 suites never
  meet an unregistered seam (ADV-19; inferred from T075's order).
  - **Falsifier**: `tests/test_dependency_direction.py` with
    `DOC_HEALTH_SURFACE` empty; a lone openXdox-code checkout imports cleanly; the
    composed workflow green; the help-tree test green.
  - **Ruled**: ARC-Q1. **Decisions**: ARC-4, ARC-6.
  - **After**: T071, T072's pin (T063's, or the arc's own), T021, T073.
  - **Files**: openXdox-code `src/openxdox/{generator,corpus_root,gate_console,cli_gate,gate_routes,snapshot_registry,completeness,round_trip}.py`,
    the seam declarations, the 7 tests, `tests/test_dependency_direction.py`,
    `tests/declared_exclusion.yaml` (second), `tests/conftest.py` (last: T020 →
    T021 and T026 → T073 → T074), `.github/workflows/composed.yml` (third),
    `pyproject.toml` (if ARC-6 needs it); and the six openXdox-code files that
    the arc change's `design.md` § 10 lists, measured at `56e1c238`, which this
    line did not name:
    - `.github/workflows/validate.yml`, the `LEFT_OUT` help-tree `--deselect` and
      its notes (after T029's two floor lines: T029 → T074);
    - `tests/integration/test_assembled_surface.py`;
    - `src/openxdox/column_contributions.py` and `tests/test_column_contributions.py`;
    - `src/openxdox/projection_contributions.py`;
    - `tests/test_declared_exclusion.py`.
  - **Lane**: 4.
- [ ] T075 [oX] [oxF] **The host registers the seams, with its pin pairs.**
  openxFactory's `scripts/opendox_host.py` registers the governed implementations
  at T074's seams at startup (the pattern of `:518-533`), with a host-wiring test
  under `tests/domain_profile/`, in the PR that moves the openXdox pin pair to
  T074's commit; the composed conftest's interim registration (T074) leaves in the
  openXdox-code PR that next advances `tests/composed_host_pin.yaml`. The arc's
  surfaces check runs over its own landings and is quoted (ADV-37).
  - **Falsifier**: the pin verifiers; the host-wiring test; openxFactory's
    required checks green; the surfaces check.
  - **Ruled**: ARC-Q1. **Decisions**: ARC-4.
  - **After**: T074, T064.
  - **Lane**: 4.
- [ ] T076 [oxF] **F9.2's re-run and its record.** Re-run F9.2 and quote it in
  the arc change's own evidence. As tier 1's ARC-5 (a) ruled (`6013547504`): if
  #1144 is still active, remove the `--deselect` from F9.1's pytest line (batch
  J's) and tick F9.2 there, under a Rule 6 window; if #1144 has archived, its
  archived `tasks.md` is never edited, and the closure lives in the arc change's
  evidence alone (ADV-20). #1144's archive tool refuses unticked lines, so if
  #1144 archives before T076 runs, its archive ticks F9.2 with a WRITTEN
  DISPOSITION that names the arc change `realize-doc-health-direction-arc` as
  F9.2's carrier (ARC-5 (a), "Archive with F9.2 open", `6013547504`; the
  mechanism is batch Q's F9.2 note, T005), and T076 records the real closure in
  the arc change's evidence. That tick is a disposition, not a performance.
  - **Falsifier**: F9.2, exit 0, quoted.
  - **Decisions**: ARC-5.
  - **After**: T074, T075.
  - **README**: links the arc's evidence file if this feature's entry cites it.
  - **Lane**: 4.
- [ ] T077 [oxF] **Archive the change; exit the staged topic.** Archive on merged,
  green realization evidence (release-realization), with the surfaces check quoted
  (ADV-37); move `ideation/staging/doc-health-direction-arc/` out through the change
  and update its `ideation/staging/INDEX.md` row. Under a Rule 6 window, landed by
  merge commit (never squash) so the archive date holds.
  - **After**: T076.
  - **Lane**: 4.

---

## Close: acceptance, ticks, the cut

- [ ] T080 [US4] [US5] [US1] [US2] [oDc] **AT-R2, the HTTP half, in CI.** A
  harness in openDox-code's `acceptance` job (the CI owner's last edit to
  `validate.yml`), running quickstart.md §§ 1–3 at the landing commit X
  (`RELEASE2_TIP`): the four outcomes of FR-024, with `gh` absent. It records
  `caps.health.packs` and asserts no value for it: FR-024's outcomes need no
  pack, and the `acceptance` job is not a provisioned sandbox host (ADV-31).
  - **Falsifier**: the `acceptance` job green, quoted.
  - **Ruled**: R2Q24.
  - **After**: T066, T067.
  - **Files**: `.github/workflows/validate.yml` (fifth), the harness.
  - **Lane**: 4.
- [ ] T081 [oxF] **AT-R2, the browser half, on the host.** quickstart.md § 4 at
  `RELEASE2_TIP`; `evidence/at-r2/` with each step's outcome and screenshot.
  - **Ruled**: R2Q24.
  - **After**: T080.
  - **README**: links `evidence/at-r2/`.
  - **Lane**: 4.
- [ ] T082 [oxF] **Bookkeeping: the release-2 ticks and the arc's close.** Under a
  Rule 6 window, no `Arc:` trailer: tick the 37 release-2 boxes, each with its
  evidence path (SC-004); run F11.1 at the arc's close (T093) and tick 11.0,
  11.1 and F11.1 (tier 1's ARC-5); close plan 034's T090–T093 by reference to this
  task; record 11.0's landing set per repository, lane 3's landings (T073 among
  them) included. 9.5 is NOT ticked here: the cut's pin sync (T083) and the
  0.2.0 publish (T084) still realize it, so T084 ticks it last (Copilot review
  of `6847e99e`).
  - **Realizes**: the 37; 11.0, 11.1, F11.1.
  - **Falsifier**: F11.1 prints `requirement 1 holds`; the box census reads every
    release-2 box `[x]`.
  - **After**: T081 (SC-008), T033, T066.
  - **README**: links the close's evidence.
  - **Lane**: 4.
- [ ] T083 [xF] **The cut's pin sync, with the three-way parity.** The aggregation
  moves its `openxFactory` gitlink with `.github/clearing/openxfactory/PIN.yaml`,
  and its root `openDox` and `openXdox` gitlinks equal to openxFactory's nested
  gitlinks and to `contracts/opendox-pin.yaml` / `contracts/openxdox-pin.yaml`'s
  `commit:`, in ONE commit (the aggregation's `CLAUDE.md` working rule 2);
  `python3 -m pytest tests/ -q` with `openxFactory` initialized, quoted
  (`test_opendox_openxdox_gitlink_parity.py`, `test_clearing_contract_pin.py`).
  - **Realizes**: 9.5 (part; ticked by T084, after this sync and the publish).
  - **After**: T082.
  - **Lane**: 4.
- [ ] T084 [US1] [US4] [oDc] [oD] [oxF] **Publish `opendox` 0.2.0, and tick 9.5. LAST,
  on Brett's publish word.** After AT-R2 passes and Brett gives the word: assert P (T062's
  pinned commit) and X (T080's) have identical build inputs (`git diff --quiet P
  X -- src/ pyproject.toml migrations/ README.md LICENSE`), else re-run both AT-R2
  halves at P; tag `v0.2.0` on P; dispatch the existing trusted-publishing
  workflow (OIDC, no stored token); confirm `pypi.org/pypi/opendox/0.2.0/json`;
  then the openDox root README's install line names 0.2.0 (batch Q's batch-O
  style addendum). Then, as the very last act, tick 9.5 in #1144's `tasks.md`
  under its own Rule 6 window (bookkeeping, no `Arc:`), citing T083's sync and
  this publish as its last realizations.
  **#1144's archive and F9.2.** No task of this feature archives #1144: the
  archive act stays the holder's (ARC-5 (a)). After this tick F9.2 is the only
  box of #1144 left unticked, unless T076 has already ticked it. #1144's archive
  tool refuses unticked lines, so under ARC-5 (a) ("Archive with F9.2 open",
  `6013547504`) #1144's archive ticks F9.2 with a WRITTEN DISPOSITION that names
  the arc change `realize-doc-health-direction-arc` as F9.2's carrier, and T076
  records the real closure in the arc change's evidence (batch Q's F9.2 note,
  T005). That tick is a disposition, not a performance.
  - **Realizes**: 9.5 (the tick).
  - **Ruled**: R2Q23.
  - **After**: T081, T082, T083, and Brett's publish word.
  - **Files**: the tag; openDox root `README.md` (third, last); #1144's
    `tasks.md` (9.5's tick only).
  - **Lane**: 4.

---

## Every phase

- [ ] T090 [oD] [oXc] [oX] [oxF] [xF] **The pin procedure (9.5)**, once per phase
  (T027 → T028 → T030; T060 early in phase 5, then T062 → T063 → T064) and for the
  arc (ARC-6): the steps of plan.md § "Pins and landing order", C4's runbook
  (`docs/openxdox-pin-resync-runbook.md`), and step 7, the aggregation's routine
  pin-sync after each openxFactory landing.
  - **Realizes**: 9.5 (ticked last, at T084, after the cut's sync and the
    publish).
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
| 14.8 | T054 (T040's schema, T060's pin) | T065 | T082 |
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
| F15.1 | T058 (its 24 nodes), T067 (its shell block, sandbox live) | T065 | T082 |
| 9.5 | T027, T028, T030, T060, T062–T064, T083, T084 (T090) | T090's runs; T083; the publish | T084 (last, after the sync and the publish) |
| 11.0 | T091 | T082's landing set | T082 (arc close) |
| 11.1 | T092 (T030, T064) | F11.1 | T082 (arc close) |
| F11.1 | T093 (T032, T065, T082) | `evidence/f11.1-*` | T082 (arc close) |
| F9.2 (outside the 37) | T073, T074, T075 | T076 | T076 while #1144 is active; else #1144's archive ticks it with a WRITTEN DISPOSITION naming `realize-doc-health-direction-arc` as the carrier, and T076 records the real closure in the arc change's evidence (tier 1's ARC-5 (a), `6013547504`; batch Q's F9.2 note) |

**Count:** Group 12's 11, Group 6's 4, Group 14's 10 and Group 15's 12 make
the 37; with the four arc-close boxes and F9.2, all 42 open boxes have a task.

## Falsifier mapping (the falsifiers of Groups 6, 11, 12, 14 and 15 that release 2 owns)

| falsifier (#1144 `tasks.md`) | amended by | run by | quoted in |
|---|---|---|---|
| F6.1 (`:1143`, openDox-code, no sibling) | batch Q item 1 (an entry point first; "Today" struck; 6.2's description noted superseded) | T052 (in its PR), T065 | `evidence/f6.1-run.md` |
| F11.1 (`:2007`, openxFactory, at the arc's close) | none (the guard is closed, `5890601202`) | T093 as T032, T065, T082 | `evidence/f11.1-phase4.txt`, `f11.1-phase5.txt`, T082's record |
| F12.1 (`:2670`, 12.5's, openXdox-code with openDox installed) | batch Q item 3 (composed, permanently, CF-5); item 8 (H-2, R-1 notes, as ruled) | T029 (required workflow), T032, T063 | `evidence/f12.1-run.md` |
| F12.2 (`:2816`, openDox-code, no sibling, `gh` absent) | NONE: it runs as ratified (review round 1 removed a false "`--local`" claim, F10); batch Q item 1 amends 12.4a's and 12.6a's verb shapes, not F12.2 | T031 | `evidence/f12.2-run.md` |
| F14.1 (`:3302`, openDox-code over `health-corpus`) | batch Q item 1 (the document server first); item 4 (every literal-id use, selected by fixture document) | T065 (its nodes by T053, T054, T057) | `evidence/f14.1-run.md` |
| F15.1 (`:3548`, openDox-code over `pack-corpus`, 24 nodes and a shell block) | batch Q item 1 (server first; sandbox precondition; forking child's pack id; export not steerable; restore is a write); item 4 | T058 (the nodes), T067 (the shell block in `validate`, sandbox live), T065 | `evidence/f15.1-run.md` |

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
| FR-012 (14.6; R2Q11) | T041, T044, T053 |
| FR-013 (14.7) | T053 |
| FR-014 (14.8) | T054, T040, T060 |
| FR-015 (14.9, F14.1; R2Q10) | T043, T065, T005 (item 4) |
| FR-016 (15.1, 15.1a; R2Q18, R2Q21, R2Q22) | T040, T060, T045, T047 |
| FR-017 (15.1b; R2Q15, R2Q16, R2Q17) | T010, T048, T067, T068 |
| FR-018 (15.2, 15.2a; R2Q25) | T041, T045, T049 |
| FR-019 (15.3, 15.4; R2Q12) | T050, T056 |
| FR-020 (15.5, 15.6, 15.6a; R2Q17) | T010, T048, T055, T056, T058, T067 |
| FR-021 (15.7) | T042, T047, T056 |
| FR-022 (11.0, 11.1, F11.1) | T091, T092, T093, T082 |
| FR-023 (9.5; R2Q22, R2Q23) | T060, T061, T084, T090, T083 |
| FR-024 (AT-R2) | T080, T081 |
| FR-025 (process) | T004, T005 (and every task's Falsifier line) |
| SC-001 | T031, T032, T033 |
| SC-002 | T058, T065, T066, T067 |
| SC-003 | T032, T065, T093 |
| SC-004 | T082 |
| SC-005 | T010, T017, T051, T067, T030, T064, T075 |
| SC-006 | T011, T016, T057, T042, T054, T048 (outcomes; AT-R2 in T080, T081) |
| SC-007 | T012, T013, T016 (no automatic merge; every landing confirmed or instrumented) |
| SC-008 | T080, T081, before T082 |

### Every ruling

| ruling | realized by | | ruling | realized by |
|---|---|---|---|---|
| R2Q1 | T015, T016, T005 (5) | | R2Q14 | T052 (recorded at the tick) |
| R2Q2 | T014, T005 (2) | | R2Q15 | T042, T046, T057 |
| R2Q3 | T015, T016, T019, T064 | | R2Q16 | T048, T052, T056, T005 (9) |
| R2Q4 | T012, T015, T016 | | R2Q17 | T010, T048, T067, T068 |
| R2Q5 | T011, T016 | | R2Q18 | T041, T045, T047, T048 |
| R2Q6 | T008, T012, T013, T018 | | R2Q19 | no task: kept as ratified (T048 honours it) |
| R2Q7 | T012, T018 | | R2Q20 | no task: kept as ratified (T045 honours it) |
| R2Q8 | T020–T029, T005 (3) | | R2Q21 | T047; the `stack.yaml` lockstep is F2's, no release-2 task |
| R2Q9 | T005 (1), T015, T016, T046, T048 (3, 5), T052 (1), T055 (4, 6), T058, T067 | | R2Q22 | T040, T060, T041, T047, T054, T005 (10, 11) |
| R2Q10 | T041, T044, T046, T053, T005 (4) | | R2Q23 | T061, T084, T005 (10) |
| R2Q11 | T044, T053 | | R2Q24 | T080, T081 |
| R2Q12 | T046 | | R2Q25 | T041, T042, T056, T057 |
| R2Q13 | T042 | | ARC-Q1–ARC-Q4 | T070–T072, T074–T077; ARC-Q2 also T029, T073, T094, T095+, T005 (6); ARC-Q4 T006 |

## Phase 4 writer slices (for the fan-out)

| slice | tasks | repo | lane | files (single owner while open) | depends on | falsifier | size |
|---|---|---|---|---|---|---|---|
| CI | T010, T017 | oDc | 4 | `.github/workflows/validate.yml` | T004 | the job's own run | Opus (T010, the live proof); Sonnet (T017) |
| P4-A | T011 | oDc | 4 | `session_pr.py` (new names), `submission_push.py`, `runtime/repository_act.py`, two new tests | T004 | F12.2 (2 nodes), `test_submission_port.py` | Opus |
| P4-D1 | T012 + T013 | oDc | 4 | `landing.py`, `landing_confirm.py`, `session_pr.py` (re-exports), `session_git.py`, `tests/test_session_git.py`, `tests/test_landing_guardrails.py` | T004, T008, T011 | F12.2 (13 nodes, plus 3) | Opus |
| P4-B | T014 | oDc | 4 | `serve.py`, `cli.py` | T011 | F12.2 (server node) | Sonnet |
| P4-C | T015 | oDc | 4 | `cli_branch_actions.py`, `serve_branch_actions.py`, `default_profile.py`, `serve.py`, `branch-actions.js`, `app.js`, `index.html`, census | T014, T025 | F12.2 (5 nodes) | Opus |
| P4-D2 | T016 | oDc | 4 | as P4-C, plus `branch_session.py` | T015, T012, T013 | F12.2 (surface) | Opus |
| README | T018 | oD | 4 | root `README.md` | T016 | — | Sonnet |
| P4-E | T019 | oxF | 4 | a new `tests/domain_profile/` test | lands with T030 | the test; parity test green | Sonnet |
| U-1 | T020 | oXc | 3 | `tests/conftest.py`, `tests/test_host_plane.py` | T004 | host-reg nodes | Opus |
| U-2 | T021 | oXc | 3 | `gate_console.py`, `tests/conftest.py` (one line), a new test | T020 | schema nodes | Opus |
| U-3 | T022 | oXc | 3 | `scripts/composed_placements.py`, `tests/test_composed_placements.py` (new), `.gitignore` | T021 | runbook nodes | Sonnet |
| U-4 | T023 | oXc | 3 | `swb-session.js`, `tests/test_swb_session_transport.py` (new) | T004 | Group J | Sonnet |
| U-5 | T024 | oXc | 3 | the shim | T004 (CF-3) | Group L, T | Sonnet |
| U-6 | T025 | oDc | 3 | `staging-workbench.js`, `staging-workbench-model.js`, census, `test_web_boundary.py` | T004 (W-1) | S1 + DJ | Opus |
| U-7 | T026 | oXc | 3 | `protected_suite_respellings.yaml` and the five protected files; `scripts/protected_suites.py` (R-1 (a)); `tests/test_protected_suite_check.py` (new); `tests/conftest.py` and `tests/test_host_plane.py` after T020 | T020, T005 | the oracle, with `--chains` | Opus |
| U-8 | T027, T028, T030 | oD, oXc, oX, oxF | 4 | the pins; the host's schema source | T017, T025; T029 | the pin verifiers | Sonnet |
| U-9 | T029 | oXc | 3 | `composed.yml`, `composed_host_pin.yaml`, `validate.yml`'s two floor lines (`MIN_SELECTED`, `MIN_PASSED`) | T020–T026, T028 | F12.1, with `--chains` | Opus |
| P4-G | T031, T032, T033 | oxF | 4 | `evidence/`, the README entry | T027, T029, T030, T005 | F12.2, F12.1, F11.1 | Sonnet |

**Parallel on day one:** CI (T010) ∥ P4-A (T011, with T012 beside it) ∥ U-1 ∥ U-4 ∥ U-5 ∥ U-6; U-2 and U-3 follow U-1 in lane 3.

## Phase 5 writer slices (for the fan-out)

| wave | slice | tasks | lane | depends on | size |
|---|---|---|---|---|---|
| W1 | schemas | T040 | 4 | T004 | Sonnet |
| W1 | the cut | T060 | 4 | T040, T005, Brett's cut word | Sonnet |
| W1 | U-0 | T041 | 4 | T060 | Opus |
| W1 | HA-1 | T042 | 4 | T027 / T033 | Opus |
| W1 | HA-3 | T043 | 4 | T027 / T033 | Sonnet |
| W2 | HA-2 | T044 | 4 | T041, T043 | Opus |
| W2 | G15-A | T045 | 3 | T041 | Sonnet |
| W3 | HA-5 | T046 | 4 | T042, T044 | Opus |
| W3 | G15-B | T047 | 3 | T045, T041 | Opus |
| W3 | G15-C | T048 | 3 | T045, T010 | Opus |
| W3 | G15-D | T049 | 3 | T045 | Opus |
| W3 | G15-H | T050 | 4 | T045, T027 / T033 | Sonnet |
| every wave | CI | T051 | 4 | the wave | Sonnet |
| W4 | HA-4 | T052 | 4 | T044, T046, T005 | Opus |
| W4 | HA-6 | T053 | 4 | T046, T049, T016 | Opus |
| W4 | HA-7 | T054 | 4 | T046, T053, T047 | Sonnet |
| W4 | G15-G | T055 | 3 | T043, T045, T047, T048 | Sonnet |
| W4 | G15-E | T056 | 3 | T046, T042, T047, T048, T049, T055 | Opus |
| W4 | facet follow-on | T059 | 4 | T050 | Sonnet |
| W5 | HA-8 | T057 | 4 | T046, T052, T053, T054, T050, T056 | Opus |
| W5 | G15-I2 | T058 | 3 | T047, T048, T049, T055, T056, T005 | Opus |
| W6 | F15.1 live | T067 | 4 | T058, T051, T005 | Sonnet |
| W6 | cut and pins | T061–T064 | 4 | T067, every package-changing landing | Sonnet |
| W6 | HA-10 | T065, T066 | 4 | T064, T067 | Sonnet |
| — | 26.04 | T068 | 4 | T048 | Sonnet |

## Requirement 9 and the direction arc's slices

| slice | tasks | lane | depends on | size |
|---|---|---|---|---|
| requirement 9 declarations (#1144's) | T073 | 3 | T029, T005, T095+ (its PR stays a DRAFT until they land) | Sonnet |
| the map of every composed red outside 12.5's set (read-only) | T094 | 3 | none | lane 3's call |
| the repair slices cut from the map | T095+ | 3 | T094 | lane 3's call, as the map slices |
| the change | T070, T071 | 4 | T004 | Opus |
| lines | T072 | 4 | T071 | Sonnet |
| seams and retargets | T074 | 4 | T071, T072's pin, T021, T073 | Opus |
| host registration | T075 | 4 | T074, T064 | Sonnet |
| F9.2 and archive | T076, T077 | 4 | T075 | Sonnet |

## Dependencies and execution order

1. **Phase 0**: T004 (DONE, after round 1's re-check) gates everything except
   T001–T003, T006, T007; T003 closed on the re-check (`6017901451`), so no
   round-2 analyze lands before the first realization PR. T005 lands before T015, T026, T032, T033, T052, T058,
   T060, T065, T067 and T073. T008 before T013.
2. **Phase 4**: the product chain T011 → T014 → T015 → T016 (with T012 + T013)
   → T017 → T027 → T028; the repair chain T020 → T021 → T022 and T020 → T026; both
   join at T029 → T030 → T032 → T033.
3. **Phase 5**: T040 → T060 → T041 → (W2 … W5) → T067 → T061 → T062 → T063 →
   T064 → T065 → T066; openDox-code slices from T027 (tier 1's N-6 (a)) or T033.
4. **Requirement 9**: T073 after T029, re-run after each composed-pin advance;
   T094 (the read-only map) → T095+ (the repair slices), and T073's PR stays a
   DRAFT until they land (`6016982816`).
5. **Beside phase 5**: T070 → T071 → T072 → T074 → T075 → T076 → T077; T061 never
   waits for any of them.
6. **Close**: T066 → T080 → T081 → T082 → T083 → T084 (LAST).

## Implementation strategy

- **MVP: phase 4** (US1 + US2, with US3 held): a plain repository submits and
  lands. It is shippable on its own pins (T027–T030), but release 2 publishes
  once, at the close (R2Q23 (a)).
- **Increment: phase 5** (US4, US5, US6), wave by wave, each wave green in
  `validate` before the next opens its PRs; the schemas and their cut first.
- **Beside it**: the direction arc, which never blocks the release, and
  requirement 9's declarations, which are #1144's.
- Every slice's PR names its task ids, the boxes it realizes and its falsifier's
  quoted output (FR-025).

## Ruled amendments (`6003486656`, `6003918488`, `6013547504` and `6016648451`)

| batch | item | #1144 location | ruling |
|---|---|---|---|
| Q | R2Q9's seven: F6.1's entry point, struck "Today" and 6.2's superseded description; F14.1/F15.1 start the server; F15.1's sandbox precondition; the forking child's pack id; the unsteerable export; the restore is a write; `--local` on three verb shapes | F6.1 (`:1143`), 6.2 (`:1136-1142`), F14.1 (`:3302`), F15.1 (`:3548`), 15.1b, 15.6a, 12.4a, 12.6a, 14.5 | `6003486656` |
| Q | R2Q2's repoint-sentences note | 12.4 (`:2513-2519`); `design.md:476-478`, `:1059-1061` | `6003486656` |
| Q | F12.1's composed line, permanent (CF-5) | 12.5's falsifier (`:2670`) | `6003486656`, `6003918488`, `6013547504` |
| Q | R2Q10's selection lines, every literal-id use | F14.1, F15.1 | `6003486656` |
| Q | R2Q1's non-normative reading (CF-1) | the release map (`:108`); `design.md:799-800` | `6003486656`, `6013547504` |
| Q | ARC-Q2's F9.1 declaration, batch B's form | F9.1 | `6003918488` |
| Q | F12.1 with `--chains`: several entries per suite in one landing, chained by git blob (carried out by T026, T029) | 12.5's falsifier (`:3047`); a dated note beside batch K's sentence at F5.2 (`:1065`) | `6016648451` |
| Q | ARC-5's F9.2 note | F9.2 (`:1718`) | `6013547504` (tier 1) |
| Q | H-2's batch C scope (CF-4); R-1 (a)'s admitted kind, widened to six spans (served display) | 12.5's falsifier | `6013547504`, `6016648451` |
| Q | R2Q16's full reading | requirement 16; 15.1b (`:3426`) | `6003486656` |
| Q | 9.5's two addenda (`dox-v1.2`; 0.2.0) | 9.5 (`:1553`) | `6003486656` |
| Q | 7.1's addendum: four kinds become seven copies (C-18) | 7.1 | `6003486656` (R2Q22) |
| Q | I-2 (a)'s baseline branch at 14.4; N-6 (a)'s overlap beside the map | 14.4; the release map | `6013547504` (tier 1) |
| — | F9.1's `--deselect` removed | F9.1 (batch J's line) | `5859927858`, at T076 while #1144 is active |

**Task count:** 81 rows: Phase 0 9 (T001–T009; eight done, T002–T009, and T001 is a
standing act), Phase 4 24 (T010–T033; T010, T020 and T024 done), Phase 5 29 (T040–T068, T059,
T067 and T068 among them; T040 done), requirement 9 3 (T073, T094 and the one
placeholder row T095+, which T094's map replaces with the concrete repair-slice
tasks, T095 onward), the
direction arc 7 (T070–T072, T074–T077; T070 done), Close 5 (T080–T084), Every
phase 4 (T090–T093).
