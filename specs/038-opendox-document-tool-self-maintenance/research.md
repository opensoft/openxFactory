# Research: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Feature**: [`spec.md`](./spec.md) · **Plan**: [`plan.md`](./plan.md)
**Lane**: `openxfactory-4`

This file records what the plan rests on: the trees as measured, what lane
openXfactory-3's inventories found, and each design question's decision with
its rationale and the alternatives considered. Every figure is either a
command quoted with its output, or a measurement credited to the inventory that
made it. Anything inferred says so.

## Credit: lane openXfactory-3's inventories

Release 2's plan stands on four read-only inventories that lane
openXfactory-3 wrote for lane openxfactory-4 on 2026-10-05, in the lane
workspace under `lane-coord-034/r2/`. Nothing in them was modified, pushed or
posted by their writers; this plan cites them by file and section.

| inventory | what it gives the plan | sections this plan cites |
|---|---|---|
| `R2-INV-12.md` (394 lines) | Group 12 box by box, the governed path today, OQ-12-1 to OQ-12-17, and the phase-4 outline P4-A to P4-G with file ownership | § "Today: the governed path and the merge authority"; § "Per box"; § "Open questions"; § "Proposed phase-4 task outline"; § "Erratum" and "Erratum 2" (the 174 reds split 62/55/16/16/3/22, over 11 files) |
| `R2-INV-HEALTH.md` (1512 lines; parts A and B merged) | Groups 6, 14 and 15 box by box; the migrations; `doc_health` check by check; the sandbox survey; the fixture corpora; OQ-H-* and OQ-H15-*; the 21-slice, seven-wave phase-5 outline | Part 3 (Group 6); Part 4 (Group 14); Part 5 (Group 15); Part 6 (migrations); Part 7 (`doc_health`); Part 8 (sandbox); Part 9 (fixtures); Part 11 (open questions); Part 12 A (single owners), B (slices), C (parallelism) |
| `R2-INV-P4F.md` (355 lines) with `R2-INV-P4F-part-oneoffs.md` (306 lines) | Every one of the 174 composed reds mapped to a repair means; R-1, W-1, H-1, H-2; the five suites green composed (210 cases); the slice outline U-1 to U-9 | § "Repair means"; § "Counts across all 174"; § "Items needing a ruling or a holder's word"; § "Passing composed today"; § "Errata for R2-INV-12"; § "Protected-file check"; § "Open questions"; § "Slice outline"; part-oneoffs §§ Groups H, J, L, T, W, S |
| `R2-ARC-ASK.md` (203 lines) | The `doc_health` direction arc put to Brett as ARC-Q1 to ARC-Q4, with six measured facts; CLAIMED on `#656` `6003715712`; ruled on `6003918488` | § "Measured facts every question rests on" (facts 1–6); §§ ARC-Q1 to ARC-Q4; § "Addendum" (none of the 7 directly-importing test files is protected) |

Lane openXfactory-3 also checked the clarify block twice before Brett saw it
(`spec.md` § Clarifications). The plan's lane split (plan.md § "Two lanes")
gives lane 3 the slices its inventories mapped.

## R0. The trees, measured for this plan

Run from this feature's worktree on 2026-10-05:

```text
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-05T22:19:52Z
$ for r in <the nine repositories>; do git ls-remote https://github.com/$r refs/heads/main | cut -c1-8; done
opensoft/openDox-code      a9ac96f9
opensoft/openXdox-code     56e1c238
opensoft/openDox           d77f8cbf
opensoft/openXdox          9564d5d9
opensoft/openDox-spec      f7ee3c76
opensoft/openXdox-spec     f088b097
opensoft/openxFactory      0f2a87f6
opensoft/xFactory          ce47bbc0
codeXfactory/codexFactory  972bb6f6
```

The first seven are the commits the spec and lane 3's inventories measured at
(`spec.md` § Clarifications: openDox-code `a9ac96f9`, openXdox-code
`56e1c238`, openDox root `d77f8cbf`, openxFactory `0f2a87f6`), so nothing the
plan cites has moved under it. An earlier run at 21:50:59Z gave the same eight
opensoft values.

```text
$ git fetch origin main; git rev-parse FETCH_HEAD | cut -c1-8; git rev-parse HEAD | cut -c1-8
0f2a87f6
ce64afc9
$ git merge-base --is-ancestor FETCH_HEAD HEAD && echo "main is ancestor of HEAD"
main is ancestor of HEAD
$ git diff --name-only FETCH_HEAD...HEAD -- openspec/ | wc -l
0
```

**The box census** (plan 034's `box_census.py`, verbatim, over #1144's
`tasks.md` at this branch's head):

```text
$ python3 box_census.py openspec/changes/add-neutral-product-standalone-operability/tasks.md | tail -8
11 3 11.0[ ] 11.1[ ] F11.1[ ]
12 11 12.1[ ] 12.1a[ ] 12.2[ ] 12.3[ ] 12.4[ ] 12.4a[ ] 12.5[ ] F12.1[ ] 12.6[ ] 12.6a[ ] F12.2[ ]
13 8 13.1[x] 13.2[x] 13.3[x] 13.4[x] 13.4a[x] 13.5[x] 13.6[x] F13.1[x]
14 10 14.1[ ] 14.2[ ] 14.3[ ] 14.4[ ] 14.5[ ] 14.6[ ] 14.7[ ] 14.8[ ] 14.9[ ] F14.1[ ]
15 12 15.1[ ] 15.1a[ ] 15.1b[ ] 15.2[ ] 15.2a[ ] 15.3[ ] 15.4[ ] 15.5[ ] 15.6[ ] 15.6a[ ] 15.7[ ] F15.1[ ]
16 8 16.1[x] 16.2[x] 16.3[x] 16.3a[x] 16.4[x] 16.5[x] 16.6[x] F16.1[x]
F 4 F1[~] F2[~] F3[~] F4[~]
total 125 Counter({'x': 74, ' ': 42, '~': 9})
```

The 42 open boxes are: Group 6's four (6.1, 6.1a, 6.2, F6.1), Group 12's
eleven, Group 14's ten and Group 15's twelve (37, release 2's); 9.5, 11.0,
11.1 and F11.1 (the arc-close boxes); and F9.2 (the direction arc's). The
release-2 boxes sit at #1144 `tasks.md:1124-1165` (Group 6), `:2464` onward
(Group 12, falsifier blocks at `:2670` and `:2816`), `:3220-3390` (Group 14,
falsifier at `:3302`) and `:3398-3671` (Group 15, falsifier at `:3548`).

**Where 14.8's citation points.** 14.8 cites "openxFactory's
`health/dispositions.yaml`" and `scripts/doc_health/families.py:370`:

```text
$ gh api repos/opensoft/xFactory/contents/health/dispositions.yaml --jq '.path + " " + .sha'
health/dispositions.yaml 1ef89c064bf65fe91a048c3ff861fe650435a2dd
$ gh api repos/opensoft/openxFactory/contents/health/dispositions.yaml --jq '.path'
gh: Not Found (HTTP 404)
$ grep -n 'dispositions.yaml' scripts/doc_health/families.py | head -5
344:#: `health/dispositions.yaml` entry must carry to reach these findings, and the
372:    "and immutable, and removing its health/dispositions.yaml entry re-opens "
385:_DISPOSITIONS_REL = "health/dispositions.yaml"
422:    `health/dispositions.yaml` — promotion fidelity, duplicate packet and
466:    dispositions = Path(ctx.agg_root) / "health" / "dispositions.yaml"
```

The file is the aggregation's (`ctx.agg_root`), and the quoted words sit at
`:371-372` (plan.md § Conflicts, C-7).

## R1. Group 12: the submission step and the landing seam (phase 4)

Source: R2-INV-12 §§ "Today", "Per box", "Open questions"; the answers R2Q1–R2Q7.

- **Today.** openDox's only submission is the governed one: `PullRequestPort`
  with `GhPullRequests` (it shells out to `gh`), behind `gate open-pr`. The
  three classes in `session_pr.py` are pinned by the protected
  `test_session_snapshot.py:893-916`. openDox has no `submit` verb, no landing
  seam, and no merge of its own; `session_git.py:93`'s guard refuses a merge
  argument, as feature 007's FR-004 and SC-002 require (R2-INV-12 OQ-12-6).
- **Decision: split, do not bend** (12.1, R2Q1 (a)). `SubmissionPort.submit(branch)
  -> Submission` is a new protocol beside `PullRequestPort`; `LandingPort.land(branch,
  *, confirmation) -> Landed` a third. One user-facing interface sits over
  them: the same `submit` and `land` verbs, routes and view controls in every
  governance mode. *Rationale:* 12.1 forbids one protocol for both. *Alternative
  considered:* one port with a mode switch, which 12.1 rules out.
- **Decision: the neutral default is `LocalGitSubmissions`, the governed default
  stays `GhPullRequests`** (R2Q2 (a)). A new pair, `submission_factory` (serve) and
  `_submission_port` (CLI), defaults to `LocalGitSubmissions`; `pull_request_factory`
  and `_pull_request_port` keep `GhPullRequests` for `gate open-pr`.
  *Alternative considered:* repointing `pull_request_factory` (12.4's later
  sentences), which would break the protected pin.
- **Decision: transport** (OQ-12-12, ruled as tier 2's CF-7). Factor the
  runtime's push core, `_push_to_remote_with` (`runtime/repository_act.py:1742`,
  with `_bound_local_destination` `:1613` and `_receive_pack_for` `:1720`), into
  a helper that takes a named branch; it keeps the repository-local
  command-config refusal (`_EXECUTED_LOCAL_KEYS` `:1335`,
  `_refuse_repository_local_command_config` `:1372`). Lane 3's T011 FIX
  corrected the cite: `:1335-1372` is that refusal, not the push. The remote is
  the one named `origin`, else the sole remote (ADV-26). *Alternatives:* the
  plain argv of `GhPullRequests.push`. *Rationale:* the hardening already
  exists.
- **Decision: a credential-bearing remote is pushed, and redacted** (12.1a;
  ADV-09). 12.1a designs exactly that case (`https://user:<token>@host/…`), and
  F12.2's `test_a_credential_in_the_remote_url_never_reaches_the_report`
  asserts the report "still names the remote's host and path" (#1144
  `tasks.md:2476-2484`, `:2880-2886`). The first plan refused such a remote,
  which narrowed ratified text; review round 1 withdrew it. (`attach_remote`'s
  own refusal, `refuse_credential_bearing_remote` at `repository_act.py:203`,
  stays the runtime's: it guards what is STORED, and `submit` stores nothing.)
- **Decision: the CLI `submit` does not read the install mode** (ADV-04).
  `runtime/config.py`'s `install_mode` (`:1954`) says "THE DEFAULT IS HOSTED"
  (`:1958`) and returns `raw or INSTALL_MODE_HOSTED` (`:1996`), and F12.2 runs
  `opendox submit` with neither `--local` nor `OPENDOX_INSTALL_MODE`. A
  CLI push of the user's own checkout with the user's own git is not a hosted
  act, so only a disagreement between `--local` and the setting refuses (FR-004).
  The ROUTE refuses on the hosted plane.
- **Decision: the landing mechanics** (R2Q6 (a)). The lander merges `--no-ff` in a
  landing worktree of its own; a clean served checkout on `main` is then
  fast-forwarded with `git merge --ff-only <commit>`; `land` pushes nothing and
  first checks, with `ls-remote`, that local `main` contains the remote's tip.
  *Alternatives considered* (R2-INV-12 OQ-12-6, inferred there): widening FR-004
  for `land` alone; a plumbing merge with a compare-and-swap ref update; landing
  only from the CLI in the user's checkout. R2Q6 (a) chose the first shape with
  four named exceptions to feature 007.
- **Decision: governance** (R2Q4 (a), R2Q7 (a)). `repository_governance()`
  returns `standalone`, `governed` or `unknown`, fail closed. The declaration is
  `.opendox/governance.yaml` at `main`'s tip; the default branch is `main`
  (`DEFAULT_BASE = "main"` at `branch_session.py:149` and `session_pr.py:55`,
  R2-INV-12 OQ-12-15). A registered host profile that declares an instrument
  (its contributed `SubmissionPort`) outranks a declaration; under `governed`
  no lander is bound and `land` submits through the instrument.
- **The verbs' home** (plan N-2). The holder note at `default_profile.py:41`
  (plan 034 `tasks.md:728-729`) puts `submit` and `land` in openDox's default
  profile; R2Q3 (a) needs the hosts' help goldens unchanged
  (`test_extension_point_parity.py:280-286` pins openxFactory's). So the verbs,
  and `health` with them, are default-profile contributions.

## R2. 12.5's 174 composed reds and their repair (phase 4)

Source: R2-INV-P4F (all sections); R2-INV-12 § "12.5" and its errata; R2Q8 (a).

- **Measured by lane 3** at openXdox-code `56e1c238` with openDox `a9ac96f9`
  installed and openxFactory's `scripts/` supplied (composed): 16 suites, 668
  passed, 170 failed plus 4 errors, so 174 red, over **11** files; split by
  root cause host-reg 62, display-js 55, moved-name 16, schema 16, hosted-index
  3, one-off 22. Five suites pass composed today, 210 cases: R2Q8 (c)'s set
  (`test_doxbench_mutation_boundary` 80, `test_gate_loop_views` 74,
  `test_hosted_actor` 5, `test_session_commits` 22, `test_session_records` 29).
- **By finishing means** (R2-INV-P4F § "Counts"): HR alone 66; GA 16; RP 10;
  AL alone 10; AL+HR 7; SF 6; SF+HR 1; DJ 32 (needs W-1); RULING 26 (needs
  R-1). 99 need no protected edit and no word; 17 are admitted entries (need
  H-2); 32 need W-1; 26 need R-1.
- **Decision:** phase 4's repair task group is U-1 to U-9 exactly as R2-INV-P4F
  § "Slice outline" assigns files (plan tasks T020–T029). *Alternative
  considered:* R2Q8's (b) (re-scope) and (c) (the five green suites only), both
  ruled out by R2Q8 (a).
- **`doc_health` is not a cause of any of the 174** (R2-ARC-ASK fact 3): the
  composed run supplies openxFactory's `scripts/`. So the arc ruling changes
  none of U-1 to U-9.

- **The gate console's schemas (U-2, T021), resolved without vendoring**
  (ADV-10; lane 3's T021 FIX). `gate_console._validate_contract_document` reads
  `Path(__file__).resolve().parents[2] / "contracts" / "schemas"`
  (openXdox-code `gate_console.py:642-643`): in the code leg that is the
  checkout root, which holds no `contracts/`. It asks for two schemas (`:665`,
  `:711`):
  - `gate-action-record.schema.yaml`, openXdox-spec's, ALREADY packaged in
    openXdox-code's copy record (`src/openxdox/contracts/copies.yaml`, which
    records ONE source, `spec_leg: opensoft/openXdox-spec`, `commit: f088b097`).
    The fix reads it from the package. Nothing is added to the record.
  - `demotion-execution-receipt.schema.yaml`, openxFactory's (openXdox-spec
    carries only its examples). It cannot join the record:
    `tests/test_packaged_validator.py:81-92` pins the copies to the validator's
    own three kinds ("no fourth kind rides in as a copy"), and the promoted
    `neutral-product-pin` admits ONE vendored openxFactory contract on terms the
    record cannot meet (ADV-10). So the reader takes it from a schema source the
    HOST registers: the composed run's conftest registers openxFactory's
    `contracts/schemas/` from the composed tree (U-1's mechanism), and
    openxFactory's host wiring registers the same at T030's pin (an 11.1
    host-wiring surface). A lone checkout refuses by name, which is R1Q27 (a)'s
    "validated only where the tree it runs from supplies their schemas".
  - The spec's "gate-action record schema" named one of the two; spec.md now
    names both (F8).
- **The runbook (U-3, T022), placed from the composed tree** (ADV-10; lane 3's
  T022 FIX). `test_session_runbook.py:54` and `test_session_notebook.py:1075`
  read `REPO_ROOT / "docs" / "ideation-dashboard-session-runbook.md"`, with
  `REPO_ROOT` from openXdox-code's non-protected `tests/conftest.py:25`
  (`HERE.parent`). The carve sent the runbook to openDox-spec
  (`f7ee3c76:docs/ideation-dashboard-session-runbook.md`, measured in a clone;
  the `test_session_notebook.py:1075` reader is R2-INV-P4F's measurement).
  An openDox-spec document cannot be a row in openXdox-spec's copy record. U-9's
  composed workflow checks openxFactory out with recursive submodules, so
  `openDox/spec/docs/ideation-dashboard-session-runbook.md` is in the composed
  tree at the openDox root's pinned spec commit. T022's placement script links it
  to `docs/` for the run (the path is git-ignored), and the composed workflow and
  the documented local composed run both call the script.
- **The composed checkout** (lane 3's T029 FIX). openxFactory's nested `openDox`
  and `openXdox` (and `openXwallet`) must be initialized recursively, or
  `corpus_adapter_openxfactory` refuses at import ("the pinned openDox
  corpus-adapter interface is not at …"), as R2-INV-12's first composed run
  measured.
- **The shim's package** (H-1; ADV-39). openxFactory's `scripts/ideation_dashboard/`
  has no `__init__.py` (measured: `ls` refuses it). The shim's directory must
  not add one either, so the two directories merge as one namespace package in
  the composed run instead of one shadowing the other (inferred from Python's
  namespace-package rule).

## R3. Feature 007's four exceptions (R2Q6 (a))

Feature 007 is codexFactory's `specs/007-workbench-branch-sessions/spec.md`
(repo `codeXfactory/codexFactory`, which allows merge commits only; its `main`
was `972bb6f6` at R0). R2Q6 (a) names, by this word, four exceptions: the
guard's argument check (`tests/test_session_git.py:523` still refusing
`("merge", "other-branch")`, and `:563-564`'s pin moving), `session_git.py:93`'s
stated rule, SC-002's `HEAD` clause and SC-002's working-tree clause.
**Decision:** the codexFactory amendment lands first (T008), as bookkeeping
with no `Arc:` trailer (plan N-8); the guard and its pins move in openDox-code
with the lander (T013, landing with T012). *Alternative:* moving the guard first
and amending the spec after, which would leave openDox-code contradicting a
live spec.

## R4. Group 6 (phase 5)

Source: R2-INV-HEALTH Part 3, Part 7 D; R2Q14 (a).

- **6.1 re-measured by lane 3:** 38 Python modules (not 37), 32,838 lines
  (24,952 executable), and two generic modules, `lines.py` (133) and
  `fs_probe.py` (103; first committed in #1201, `0d143582`, after #1144 landed).
  6.1's claim holds in substance; its numbers are stale by one module.
- **6.1a** is satisfied vacuously in release 2: no family moves, and no shared
  module is created (R2Q14 (a)). The arc's re-authoring of the `lines` slice in
  openDox-code (ARC-Q1 (a)) relocates nothing out of openxFactory, so it does not
  reopen 6.1a.
- **6.2's seam** is `run_scoped_doc_health`, which 6.2 cites at
  `workbench.py:1389`. At `a9ac96f9` it is at `:1666`, and
  `register_health_check` is at `:1622`; `:1542-1557` is the
  `DEFAULT_SCOPED_FAMILIES` block, which R2-INV-HEALTH Part 12's HA-4 row cited
  by mistake (ADV-29; lane 3's T052 FIX). The seam holds ONE check and refuses a
  different second one (`:1622-1651`, "a different one would replace it").
  **Decision:** the engine's built-in families are what openDox registers
  there, only when the seam is empty, and a host's check replaces it (OQ-H-3;
  ADV-18).

## R5. Group 14's store (phase 5)

Source: R2-INV-HEALTH Part 4 (14.1–14.3), Part 6; R2Q13 (a), R2Q15 (a).

- **Decision:** one migration, `0003_`, adds a runs table and a findings table
  (OQ-H-22), DOMAIN tables in `identity.TABLES` (R2Q13 (a)), with 15.7's
  `pack_id`/`pack_version` columns from its first landing. There is NO patch
  column: a patch is document text, and 14.3 and R2Q25 (a) keep every document
  out of the store, so a pack's patch is re-obtained at `fix` (lane 3's
  MISLABEL row 31). *Rationale:* Part 6 C measured that `0003_` moves about
  twenty assertions, so the table is migrated once, by one owner (HA-1).
  *Alternative:* separate migrations for Group 14 and Group 15's columns, which
  doubles those moves.
- **The five `tests_runtime/` suites `0003_` moves, each with its reason** (lane
  3's T042 FIX, re-checked here by grep at `a9ac96f9`):
  `test_migrations_apply.py` (21 lines name `0002`), `test_runtime_cli.py`
  (`:277`) and `test_bundled_postgres.py` (`:540`, `:924`) hard-code the
  migration list; `test_schema_shape.py`'s closure reads `0001` only (`:32`,
  `:36-59`) and must read `0001` with `0003_` (R2Q13 (a)); `test_deploy_shape.py`
  derives its lists from `identity.TABLES` (`:1850`, `:2222`), so it moves with
  T042's `TABLES` edit and is re-run, not edited. The role-init scripts are
  `deploy/compose/init-runtime-role.sh` and
  `deploy/kubernetes/base/init-runtime-role.sh` (and any third R2-INV-HEALTH
  Part 6 C names).
- **A hosted install** migrates the schema but refuses the health surface by
  name and records nothing (R2Q15 (a)).

## R6. Group 14's engine, view, fix loop and exceptions (phase 5)

Source: R2-INV-HEALTH Part 4 (14.4–14.9), Part 9; R2Q10–R2Q12, R2Q25.

- **The finding id** (R2Q10 (a); ADV-07): `<pack_id>.<kind>.<h16>`, where
  `<h16>` is the first 16 hex digits of a SHA-256 over the canonical JSON
  (sorted keys) of the pack id, kind, document path and a POSITION-INDEPENDENT
  identity key the family supplies (a link target as written, a pair of paths, a
  heading key). Line ranges are display-only locators, outside the hash. The
  first plan hashed a line-bearing locator, so any edit above a finding changed
  its id, made the baseline see a new finding plus an uncited disappearance, and
  silently ended an exception keyed by the old id (ADV-07). Reading R2Q10 (a)'s
  "a locator the family supplies" as such a key is a conforming refinement.
  It survives a reset, is unique within a run (a collision is a finding against
  its producer, never truncated further; contracts/health-finding.md), and is a
  valid ref-name component, so the draft branch is
  `health-fix-<id>`. A raw `path:locator` form was rejected: `:` is not allowed
  in a git ref name.
- **The baseline** (R2Q12 (a)): the previous default-tip run in the store; three
  classes (new, arrived with a pack upgrade, persistent); disappearance measured
  only between default-tip runs; a citation is a landing of the fix loop's draft
  or a commit with a `Finding:` trailer; an uncited disappearance re-raised once
  as `human-only`. With no `main`, tier 1's I-2 decides the baseline branch.
- **What a run reads** (N-10, as review round 1 corrected it; ADV-16, F9): R2Q12
  (a) names runs "at the tip, on a branch or over the working state"
  (`clarify-questions.md:591-593`), so all three kinds are supported. The first
  plan's "committed tree of HEAD only" narrowed the answer and was withdrawn.
  In a working-state run only the built-in checks read the working copy;
  packs always get the committed export of HEAD (`git archive`, 15.1b), and no
  untracked file is copied to a pack. Branch and working-state runs never raise
  a disappearance. F14.1 commits before each run (#1144 `tasks.md:3302` onward),
  so it reads commits.
- **An uncommitted exception** (the spec's deferred edge case, `spec.md:534-536`;
  C4): a run reads the dispositions file in what it reads, so an uncommitted
  `accept` suppresses in a working-state run and in no commit run until it is
  committed.
- **Empty and stale stubs** (ADV-17, ADV-40): 14.6 and requirement 14's third
  scenario put empty stubs in `assisted` (#1144 `tasks.md:3276-3277`;
  `specs/…/spec.md:480-482`). The first plan's row classed stale stubs and was
  silent on empty ones. Criteria and the deterministic proposal: data-model.md
  § Families.
- **Exceptions** (14.8, OQ-H-13): `health/dispositions.yaml` with its own `kind`;
  F14.1 commits it and asserts the finding absent before and after `runtime
  reset`.
- **Evidence** (R2Q25 (a)): locators only; the view reads the passage from git.
- **Fixture** (14.9): `tests/fixtures/health-corpus` does not exist; R2-INV-HEALTH
  Part 9 B records what does.

## R7. Group 15: the pack contract and the sandbox (phase 5)

Source: R2-INV-HEALTH Part 5, Part 8; R2Q16–R2Q22.

- **What runs where** (R2Q16 (a)): trusted installed code (openDox's own checks;
  a host's check registered through `register_health_check`, at the scoped seam
  only and never stored) runs in process on every platform; only manifest-listed
  packs are sandboxed; with no sandbox, packs do not run and one finding against
  the install says why. No Seatbelt realization.
- **The sandbox survey** (Part 8 B–D, lane 3's measurements and reading):
  `bwrap` is the Linux reference. It was refused inside the lane container;
  GitHub's `ubuntu-24.04` image restricts unprivileged user namespaces through
  AppArmor by default (`actions/runner-images#10443`), which
  `kernel.apparmor_restrict_unprivileged_userns=0` lifts; a hosted pod is
  inferred to refuse it too. `ubuntu-latest` moves to 26.04 in a window lane 3
  recorded as 2026-10-19 to 2026-11-19, which is why R2Q17 (a) pins
  `ubuntu-24.04` and leaves the move to a measurement.
- **Decision** (R2Q17 (a), plan N-4): the required `validate` job pins
  `ubuntu-24.04`, installs bubblewrap, sets the sysctl, proves the sandbox live
  before the suite, and makes the sandbox tests fail rather than skip under
  `CI`, so `EXPECT_SKIPPED` stays 11. It lands on day one (T010).
  *Alternative considered:* R2-INV-HEALTH's G15-I1 in wave W3, beside the
  sandbox slice; moved earlier so the provisioning's failure modes surface
  first.
- **Pack dependencies** (R2Q18 (a)): the standard library and ONE contract
  module (plan N-3: `opendox.health_contract`).
- **Kept as ratified:** packs see only the exported tree (R2Q19 (a)) and are
  model-free (R2Q20 (a)).
- **The manifest** (R2Q21 (a)): `health/packs.yaml` is authoritative; F2 owns the
  `stack.yaml` lockstep.
- **The schemas** (R2Q22 (a)): openDox-spec owns the exceptions file,
  `health/packs.yaml` and the finding's neutral shape; openDox-code carries
  digest-checked copies; the openDox root cuts one more `dox-v1.y` minor.
- **The copies follow the root's pin, never lead it** (ADV-05; lane 3's SHARED
  and T047 FIXes). openDox-code's copy record
  (`src/opendox/contracts/copies.yaml`) holds ONE `commit:`, the spec-leg commit
  the openDox root pins (`f7ee3c76` today). `tests/test_validator_input_set.py`
  asserts `record.commit == SPEC_COMMIT`, that each digest equals the root's
  (`PINNED_BY_THE_ROOT`), and that the record, the validator's kinds and the
  files on disk are the same set (`THE_FOUR`; measured in a clone at `a9ac96f9`,
  `:97-121`, `:148-160`). Release 1 therefore moved the root's spec pin and cut
  the bundle first (034 T053, `dox-v1.1`, cut by Brett, RULED `5894235642`) and
  copied after (T057). Release 2 does the same: T040 (schemas), then T060 (the
  root's spec pin, the manifest, and the `dox-v1.2` cut on Brett's cut word),
  then the copies T041 → T047 → T054 in that fixed order.
- **7.1's count moves from four to seven** (new in review round 1). 7.1, as batch
  G amends it, says openDox's validator validates its spec leg's FOUR kinds. R2Q22
  (a) adds three schemas to that spec leg. Two are file kinds the validator can
  validate (`opendox-health-dispositions`, `opendox-health-packs`); the finding
  shape is not (its `kind` field is the family, so no `kind` const can name the
  schema), so it is a copy the engine reads, and the set test reads "the
  validator's kinds plus the finding shape" (decision N-15). Batch Q carries 7.1's
  addendum, on R2Q22 (a)'s word.

## R8. openDox-code's CI floors

R2-INV-HEALTH Part 12 A records openDox-code `validate.yml` at `a9ac96f9`:
`MIN_SELECTED` "3977" (`:272`), `MIN_PASSED` "3966" (`:273`), `EXPECT_SKIPPED`
"11" (`:306`). Every phase-4 and phase-5 slice adds tests, and only the CI owner
re-pins the floors (T017, T051), so no two slices race on the file.

## R9. The `doc_health` direction arc, ruled (`6003918488`)

Source: R2-ARC-ASK (all); the staged topic
`ideation/staging/doc-health-direction-arc/doc-health-direction-arc.md` at
`0f2a87f6` (Q1 `:345-374` … Q6 `:459-470`; exit path `:472-553`).

- **The surface** (fact 1): 8 openXdox-code modules, 13 imports
  (`tests/test_dependency_direction.py:353-363`, `DOC_HEALTH_SURFACE`). Only
  `completeness.py` and `round_trip.py` are generic-only; `generator.py` is
  mixed; `corpus_root.py`, `gate_console.py`, `cli_gate.py`, `gate_routes.py`
  and `snapshot_registry.py` use governed names only.
- **The exclusion** (fact 2): 66 files in `tests/declared_exclusion.yaml`
  (`doc_health` 60, rail 3, contracts 5). 7 test files import `doc_health`
  themselves, and none is among 12.5's 16 protected suites (the ask's addendum).
- **The pattern** (fact 4): a host-registered seam, as
  `scripts/opendox_host.py:518-533` already registers openxFactory's scoped
  check and its status-exemption rail; host wiring is one of 11.1's surfaces.
- **The packs route is closed** (fact 5) by R2Q18 (a) and R2Q19 (a).
- **Ruled** (`6003918488`, verbatim *"Retarget all eight (Recommended)"*,
  *"Composed CI in openXdox-code (Recommended)"*, *"Own change, beside phase 5
  (Recommended)"*, *"Confirm (Recommended)"*). Plan tasks T070–T077 schedule it;
  plan decisions ARC-1 to ARC-6 are its open items.
- **R1Q6 (d)'s ask, scheduled and discharged.** R1Q6 (d) required the arc
  DECIDED before 12.5 needs the 16 governed suites. The latest point at which it
  could have been asked without delaying phase 4's checkpoint was the claim of
  U-9 (T029), whose composed run is F12.1. It was asked (lane 3's ask, at lane
  4's request) and ruled before this plan, so T006 is done.

## R10. Pins and the aggregation

- Release 1's seven-step pin procedure and C4's runbook
  (`docs/openxdox-pin-resync-runbook.md`, #1154) stand (plan 034 § "Pins and
  landing order").
- The aggregation's `CLAUDE.md` working rule 2: an openxFactory pin-sync moves the
  gitlink and `.github/clearing/openxfactory/PIN.yaml` together; a sync touching
  `openDox` or `openXdox` keeps the root gitlink equal to openxFactory's nested
  gitlink and to the `commit:` of `contracts/opendox-pin.yaml` /
  `contracts/openxdox-pin.yaml`, in the same commit
  (`tests/test_opendox_openxdox_gitlink_parity.py`); both parity tests skip in
  `validate` and bite locally, so each sync runs the aggregation's suite with
  `openxFactory` initialized.

## R11. Release mechanics: AT-R2 and 0.2.0

- **AT-R2** takes AT-R1's form (plan 034 `quickstart.md`; T095, T096): an HTTP
  half as a harness in openDox-code's `acceptance` CI job, and a browser half on
  the host. FR-024 names its four outcomes.
- **0.2.0** follows plan 034's T099/T101 cut kit: the version bump is the last
  package-changing openDox-code landing before the root pin; the workflow
  publishes only the commit the root's `contracts/code-pin.yaml` names; before
  the tag and the dispatch, the holder checks that the build inputs are
  identical between the pinned commit P and AT-R2's commit X (`git diff --quiet
  P X -- src/ pyproject.toml migrations/ README.md LICENSE`), and re-runs both
  halves at P if not. Trusted publishing (OIDC) only; no stored token.

## R12. Non-normative corrections to #1144 found while planning

None of these changes a requirement; each is recorded where its box ticks.

| where | what #1144 says | what the trees say | recorded by |
|---|---|---|---|
| 6.1 (`tasks.md:1124-1132`) | 37 modules; `lines.py` alone generic | 38; `lines.py` and `fs_probe.py` | T052's tick |
| 6.2 (`tasks.md:1136-1142`) | the seam at `workbench.py:1389`; the call fails on `No module named 'doc_health'` | `run_scoped_doc_health` at `:1666`, `register_health_check` at `:1622`; the detail is `HEALTH_CHECK_NOT_REGISTERED` (`:1594`) | batch Q item 1 (R2Q9 (a) item 1's superseded note); T052's tick |
| 7.1 (batch G's "four") | openDox validates its spec leg's four kinds | seven copies once R2Q22 (a)'s three land | batch Q (7.1's addendum) |
| 14.8 (`tasks.md:3289-3294`) | "openxFactory's `health/dispositions.yaml`", `families.py:370` | the aggregation's file; `:371-372` | T054's tick |
| 12.4 (`tasks.md:2513-2519`), design § D9 | `GhPullRequests` repointed and contributed by the host | unrealized in release 2 (R2Q2 (a), R2Q3 (a)) | batch Q's note (T005) |
| 12.5's falsifier | composition unnamed | runs composed (R2Q8 (a)); ARC-Q2 (a) makes the composition its permanent home | batch Q's line (T005; tier 2) |

## R13. Review round 1 (2026-10-05): what it found, and what was measured to check it

Two independent read-only reviews of this plan at `6d6911e1`:
- an Opus `speckit-analyze` and adversarial pass, ADV-01 to ADV-41 with the
  analyze table (D1, F1–F10, C1–C6, E1–E4, A1–A2, B1–B2), verdict "READY after
  the listed fixes": `evidence/analyze-round-1.md`, verbatim, with its
  disposition table;
- lane openXfactory-3's PLANCHECK, about 34 FIX lines and 4 MISLABEL, accepting
  the lane split on three conditions: `evidence/plancheck-lane3-round-1.md`,
  verbatim, with its disposition table.

Lane openXfactory-3 is credited for the PLANCHECK, which also corrected its own
inventory's copy-record proposal (R2-INV-P4F § schema).

**Re-measured by the plan writer before applying** (clones of openDox-code
`a9ac96f9`, openXdox-code `56e1c238`, openDox-spec `f7ee3c76`, openXdox-spec
`f088b097`, openDox `d77f8cbf`, all still `main`; and this worktree):
- #1144's ratified shapes: `submit --repo-root <repo> --branch
  <session-branch>` (`tasks.md:2536-2537`), `land --repo-root <repo> --branch
  <session-branch>` (`:2814-2815`), F12.2's `opendox submit --repo-root
  "$W/plain" --branch sess-1` (`:2834`) and `r.ref`, `r.url` (`:2848`);
  `health fix --repo-root <corpus> --finding ID [--batch]` (`:3253`); 15.6a's
  eight packs by name (`:3503-3525`); 15.2a's refusal list and the 65,536-byte
  bound (`:3461-3479`); 15.1a's `commit` rule (`:3414-3421`); every literal-id
  use in F14.1 (`:3320`, `:3326-3329`, `:3336-3340`, `:3347-3351`, `:3357`,
  `:3364-3365`) and F15.1 (`:3575`, `:3590`, `:3595-3602`, `:3608-3612`).
- `runtime/config.py:1954` opens `install_mode`; its docstring reads "THE DEFAULT
  IS HOSTED" at `:1958`, and `:1996` returns `raw or INSTALL_MODE_HOSTED` (the
  review cited `:1954` for the words; the function opens there).
- `serve.py:528-650` builds a fixed `actions` map; `gate` and `refresh` are
  derived from route bindings (`answers_a_gate_verb`, `answers_the_refresh`,
  `:509-526`). `default_profile.py` declares `ROUTE_EXTENSIONS` empty.
- No openxFactory test pins the `actions` key set: `grep -rn` over `tests/` finds
  only per-key reads (`tests/ideation-dashboard/test_intent_feed.py:533-589`,
  `test_gate_routes.py:192-212`, `test_intent_plane_boundary.py:532-536`).
- `workbench.py:1622-1651` refuses a second, different scoped check;
  `run_scoped_doc_health` is at `:1666`.
- `session_git.py:250-263`: session worktrees live in `<repo>-worktrees/`.
- `tests/test_session_git.py:563` opens the loop over `("add", "commit",
  "merge", …)` and `:564` holds its assertion (`sed -n 560,564p`). The review's
  item 3 placed them at `:564` and `:565`; the plan's `:563-564` stands.
- openXdox-code `scripts/protected_suites.py` (not `tests/`), with
  `_inside_the_test` at `:294`.
- codexFactory `main`'s rules (`gh api repos/codeXfactory/codexFactory/rules/branches/main`):
  required status checks `validate` and `lane-line`; pull-request rules with one
  approving review (one ruleset with last-push approval, one with code-owner
  review); Copilot code review; merge commits only (`allow_squash_merge` and
  `allow_rebase_merge` false).

**One finding was not applied as worded, and one was found beside it.** Both are
in the disposition tables: OQ-12-14's flags (ADV-14 asked for route-derived flags;
that also needs a new `actions.submit` key, since `session` alone would offer a
submit control where no submit route answers), and 7.1's count (above).
