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
- **Decision: transport** (OQ-12-12, plan row 3). Factor the runtime's hardened
  push (`repository_act.py:1335-1372`, `:1742` onward, as R2-INV-12 cites them)
  into a helper that takes a named branch. *Alternatives:* the plain argv of
  `GhPullRequests.push`. *Rationale:* the hardening already exists.
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
  `workbench.py:1389` and R2-INV-HEALTH § HA-4 places at `:1542-1557` at
  `a9ac96f9` (line drift). **Decision:** the engine's built-in families are
  what openDox registers there (OQ-H-3, plan row 9).

## R5. Group 14's store (phase 5)

Source: R2-INV-HEALTH Part 4 (14.1–14.3), Part 6; R2Q13 (a), R2Q15 (a).

- **Decision:** one migration, `0003_`, adds a runs table and a findings table
  (OQ-H-22), DOMAIN tables in `identity.TABLES` (R2Q13 (a)), with 15.7's
  `pack_id`/`pack_version` columns and the patch column (OQ-H15-20) from its
  first landing. *Rationale:* Part 6 C measured that `0003_` moves about twenty
  assertions (`["0001","0002"]` hard-coded ten times; `DROP_ORDER`; the role-init
  scripts), so the table is migrated once, by one owner (HA-1). *Alternative:*
  separate migrations for Group 14 and Group 15's columns, which doubles those
  moves.
- **A hosted install** migrates the schema but refuses the health surface by
  name and records nothing (R2Q15 (a)).

## R6. Group 14's engine, view, fix loop and exceptions (phase 5)

Source: R2-INV-HEALTH Part 4 (14.4–14.9), Part 9; R2Q10–R2Q12, R2Q25.

- **The finding id** (R2Q10 (a)): `<pack_id>.<family>.<h16>`, where `<h16>` is
  the first 16 hex digits of a SHA-256 over the pack id, family, document path
  and the family-supplied locator. It is derived by the engine, survives a
  reset, is unique within a run (a collision is refused, never truncated
  further), and is itself a valid ref-name component, so the draft branch is
  `health-fix-<id>` (data-model.md § Finding). A raw `path:locator` form was
  rejected: `:` is not allowed in a git ref name.
- **The baseline** (R2Q12 (a)): the previous default-tip run in the store; three
  classes (new, arrived with a pack upgrade, persistent); disappearance measured
  only between default-tip runs; a citation is a landing of the fix loop's draft
  or a commit with a `Finding:` trailer; an uncited disappearance re-raised once
  as `human-only`. With no `main`, plan I-2 applies.
- **What a run reads** (plan N-10): the committed tree of `HEAD`. F14.1 commits
  before each run (#1144 `tasks.md:3302` onward), so it is compatible.
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
| 6.2 (`tasks.md:1136-1142`) | the seam at `workbench.py:1389` | `:1542-1557` (R2-INV-HEALTH § HA-4) | T052's tick |
| 14.8 (`tasks.md:3289-3294`) | "openxFactory's `health/dispositions.yaml`", `families.py:370` | the aggregation's file; `:371-372` | T054's tick |
| 12.4 (`tasks.md:2513-2519`), design § D9 | `GhPullRequests` repointed and contributed by the host | unrealized in release 2 (R2Q2 (a), R2Q3 (a)) | batch Q's note (T005) |
| 12.5's falsifier | composition unnamed | runs composed until the arc lands (R2Q8 (a)) | batch Q's line (T005) |
