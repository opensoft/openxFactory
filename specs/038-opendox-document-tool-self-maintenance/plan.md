# Implementation Plan: openDox, the document tool and self-maintenance (release 2)

Status: draft

**Branch**: `038-opendox-document-tool-self-maintenance` | **Date**: 2026-10-05 | **Spec**: [`spec.md`](./spec.md)
**Input**: the clarified feature specification; #1144's ratified packet
(`openspec/changes/add-neutral-product-standalone-operability/`); Brett Heap's
answers to clarify round 1, R2Q1–R2Q25 all (a) (`#656` `6003486656`); his
ruling of the `doc_health` direction arc, ARC-Q1–ARC-Q4 all (a) (`#656`
`6003918488`); lane openXfactory-3's read-only inventories; and measurements
of the live trees ([`research.md`](./research.md)).
**Lane**: `openxfactory-4` (coordinator; lands every PR), with lane
`openXfactory-3` as the peer that runs its own writers (§ "Two lanes").

**NO CODE UNTIL BRETT RULES THIS PLAN.** Every row of § "Design decisions for
Brett to rule with this plan" is a PROPOSAL. No realization task starts before
T004 records his ruling of them.

## Summary

Release 2 makes openDox a document tool that maintains itself, in the two
phases #1144's RULED release map gives it (`5799646419`, `5800995035`):

- **Phase 4, Group 12: the submission step and the landing seam.** openDox
  gains its own neutral submission (`SubmissionPort`, `Submission`,
  `LocalGitSubmissions`, `NoSubmissionTarget`), its own `submit` act (CLI verb
  and route), and a landing seam (`LandingPort.land(branch, *, confirmation)`,
  `repository_governance()`, the `land` act). A standalone owner lands a
  branch on `main` by ONE confirmed act, as a `--no-ff` merge commit that ONE
  `git revert -m 1` undoes. `land` pushes nothing. The governed path
  (`PullRequestPort`, `GhPullRequests`, `gate open-pr`) is unchanged
  (R2Q1–R2Q8). Beside it, phase 4 repairs the 174 composed reds of 12.5's 16
  governed suites WITHOUT editing those proofs, through lane openXfactory-3's
  repair map (U-1 to U-9, R2Q8 (a)), so that F12.1 runs green, composed.
- **Phase 5, Groups 6, 14 and 15: health.** A health store (`0003_`, a DOMAIN
  table), the neutral families, the engine with a baseline, the Health view
  with CLI parity, the fix loop whose drafts land only through phase 4's
  `land`, exceptions in git (`health/dispositions.yaml`), and the check-pack
  interface: a committed, digest-pinned manifest (`health/packs.yaml`) and an
  OS-enforced sandbox (`bwrap` on Linux; no packs where no sandbox exists).
  Group 6's scoped check is the engine's built-in families, registered at
  openDox's existing seam (R2Q9–R2Q22). It follows lane openXfactory-3's
  21-slice, seven-wave outline.
- **Beside phase 5: the `doc_health` direction arc's realization.** Brett
  ruled the arc on `6003918488`: retarget all eight openXdox-code modules
  (ARC-Q1 (a)), composed CI in openXdox-code made permanent (ARC-Q2 (a)), its
  OWN OpenSpec change owned by lane openxfactory-4 under this plan, beside
  phase 5, gating neither release 2's close nor #1144's archive (ARC-Q3 (a)),
  and the deadline confirmed (ARC-Q4 (a)). Tasks T070–T077 schedule it.
- **The close.** Three openDox-spec schemas and one more `dox-v1.y` minor
  bundle (R2Q22 (a)); AT-R2, HTTP half in CI and browser half on the host
  (R2Q24 (a)); the ticks of the 37 release-2 boxes and the arc-close boxes
  (9.5, 11.0, 11.1, F11.1); the pin syncs through openxFactory and the
  aggregation; and LAST, `opendox` 0.2.0 on PyPI on Brett's publish word
  (R2Q23 (a)).

**The first act** is T005: ONE bookkeeping batch (batch Q) in plan 034's T007 form,
under a Rule 6 window, carrying R2Q9 (a)'s seven amendments, the three further
lines R2Q2 (a), R2Q8 (a) and R2Q10 (a) owe, R2Q1 (a)'s non-normative reading,
ARC-Q2 (a)'s F9.1 amendment, and (as decisions I-3, N-5 and N-12 propose) the R2Q22
and R2Q23 addenda at 9.5. It lands before phase 4's first checkpoint.

**What this plan leaves to Brett.** 63 design decisions, each with a
recommended option and its alternative (§ "Design decisions for Brett to rule
with this plan"): the 34 items `clarify-questions.md` deferred to the plan, the
four phase-4 repair items R-1, W-1, H-1 and H-2, the three interplays the spec
writer reported, the arc ruling's open items, and the items this plan found.
§ "Conflicts found" reports the places where the answers, #1144 and the code
disagree. They are reported there, not resolved.

## Technical Context

**Language/Version**: Python, at the version openDox-code's `pyproject.toml`
declares (not re-measured here); browser JavaScript modules under
`src/opendox/web/`, exercised by the suites' Node harness; SQL migrations for
the runtime's PostgreSQL store.

**Primary Dependencies**: openDox-code's existing dependencies only. `git` (the
CLI) for every submission, landing and corpus export. `bubblewrap` (`bwrap`)
as the Linux reference sandbox (R2Q16 (a), R2Q17 (a)). No `gh` anywhere on
openDox's own path (12.4, F12.2). A pack may depend on the standard library
and the engine runner's neutral contract module only (R2Q18 (a)).

**Storage**: the runtime's store, through a new `0003_` migration that adds a
health runs table and a health findings table, both DOMAIN tables (R2Q13 (a)).
The store holds no document and stays disposable (14.3). Exceptions live in
git, in `health/dispositions.yaml`; the pack manifest in `health/packs.yaml`;
the governance declaration in `.opendox/governance.yaml`, read from `main`'s
tip (R2Q7 (a)).

**Testing**: pytest in openDox-code (`tests/`, `tests_runtime/`, the whole
suite in the required `validate` job, `EXPECT_SKIPPED` 11); 12.5's 16 governed
suites run composed in openXdox-code against a pinned openxFactory (R2Q8 (a),
ARC-Q2 (a)); #1144's falsifiers F12.1, F12.2, F6.1, F14.1, F15.1 and F11.1,
each as amended, quoted in evidence; AT-R2 (R2Q24 (a)).

**Target Platform**: the local plane on Linux, macOS and any platform openDox
already serves. Packs run only where the reference sandbox is proved live:
Linux with `bwrap` and unprivileged user namespaces. macOS gets health with
no packs and one finding that says why (R2Q16 (a)). Hosted installs refuse the
health verbs and view by name (R2Q15 (a)).

**Project Type**: a CLI and loopback web application with library seams,
spread over a two-leg product (openDox root, openDox-code, openDox-spec) and
its governed descendant (openXdox root, openXdox-code), consumed by
openxFactory and the xFactory aggregation.

**Performance Goals**: none beyond #1144's. A pack has a timeout and declared
resource bounds; a bound hit is a finding against that pack (15.6, OQ-H15-5).

**Constraints**: no landing merges automatically (SC-007); `land` pushes
nothing; evidence carries locators, never document text (R2Q25 (a)); packs
see only the exported tree and are model-free (R2Q19 (a), R2Q20 (a)); 12.5's
16 suites are edited only through the allow-list (R2Q8 (a)); openxFactory's
arc edits stay on 11.1's surfaces; `EXPECT_SKIPPED` stays 11 (R2Q17 (a)).

**Scale/Scope**: 37 release-2 boxes (Group 6: 4; Group 12: 11; Group 14: 10;
Group 15: 12), the four arc-close boxes, and F9.2 through the direction arc.
Seven product repositories, one codexFactory spec amendment (R2Q6 (a)), one
new OpenSpec change (ARC-Q3 (a)), and the aggregation's pin syncs. 77 tasks.

No item of the Technical Context is NEEDS CLARIFICATION: every behavioural
question is answered (R2Q1–R2Q25, ARC-Q1–ARC-Q4), and every design question
carries a proposal in the decisions table, which Brett rules with the plan.

## Constitution Check

*GATE: checked before planning, and re-checked after the design (Phase 1
below). This revision is the first plan of feature 038. It is re-checked at
T004, when Brett rules the decisions table, and again after the independent
analyze (T003).*

| principle | status | how this feature meets it |
|---|---|---|
| I. Contract-first, domain-neutral core | PASS | openxFactory gains only host wiring, pin pairs, `edits[].note` annotations and the named composition tests 11.1 admits. Neutral contracts land in openDox-spec (R2Q22 (a)'s three schemas, T040), never in openxFactory. No domain vocabulary enters openDox: the health families, classes and labels are neutral, and a domain pack's labels arrive through the display facet (15.3). |
| II. OpenSpec before implementation | PASS | Everything here realizes the RATIFIED #1144 (`5815412869`). The answers' changes to #1144's falsifiers and task lines land as bookkeeping in plan 034's T007 form (T005, batch Q; T082 at the close). The `doc_health` direction arc's realization gets its OWN OpenSpec change (ARC-Q3 (a); T070), ratified on Brett's word (T071) before any of its realization slices start. Feature 007's four exceptions are amended in codexFactory's own spec on R2Q6 (a)'s word (T008) before the guard moves (T013). |
| III. Document lifecycle | PASS | Every file of this feature carries `Status: draft`; evidence files will carry `Status: record`, as feature 034's do. #1144 is `Status: ratified`. The arc's change is authored `Status: draft` and ratified on Brett's word. |
| IV. Schema and artifact discipline | PASS, with one item owed | No committed file names a host path: commands resolve scratch space with `W=$(mktemp -d)`, and lane 3's inventories are cited by their workspace-relative path (`lane-coord-034/r2/…`). No credential is stored: a credential-bearing remote is refused and redacted (OQ-12-11). Every YAML file the product reads carries `schema_version` and `kind` (contracts/). **Owed:** the README document index entry for feature 038 (`README.md:87`) links only `spec.md`, `clarify-questions.md` and the checklist. The plan's six documents must join it. This planning PR writes only the feature directory, by its brief, so the holder adds the links before the PR leaves draft (T004). The entry sits outside the OpenSpec Records block, so it needs no Rule 6 window. |
| V. Validation gates | PASS for this PR | This PR touches no `openspec/` path (`git diff --stat origin/main -- openspec/` is empty at this branch's head; research R0). No `scripts/validate-*.py` reads `specs/`. Batch Q (T005), T070, T071, T076, T077 and T082 do touch `openspec/changes/`; each records its own gates, including the pinned `scripts/validate-openspec-cli-pin.py --all`, against the `main` it lands on. Implementation evidence is falsifier output, quoted. |
| VI. Versioned releases | PASS | R2Q22 (a) adds three openDox-spec schemas, so the openDox root cuts ONE more `dox-v1.y` minor bundle (T060) under a batch-G style addendum at 9.5 (batch Q). R2Q23 (a) publishes `opendox` 0.2.0, tagged `v0.2.0`, under a batch-O style addendum, on Brett's publish word (T084). The arc's change cuts no bundle unless its openXdox-spec delta needs one (ARC-3). |
| VII. Fail-closed authority | PASS | No merge without a human act: `land` needs a confirmation capability bound to the branch and its head, single-use (12.6a). `governed` with no instrument refuses `land` by name; `unknown` refuses. Packs run only in a sandbox proved live by a per-run canary; with no sandbox, packs do not run and one finding says why (R2Q16 (a)). A hosted install refuses the health surface by name (R2Q15 (a)). A credential-bearing remote is refused (OQ-12-11). Evidence carries locators only (R2Q25 (a)). |
| Workflow: *"material ambiguities MUST be resolved before planning"* | **PASS** | Brett answered all 25 round-1 questions (`6003486656`) and the four arc questions (`6003918488`). Round 2 was empty (`clarify-questions.md` § "Round 2"). What remains is design-level, not material to WHAT the spec requires, and is put to Brett as proposals in the decisions table. No task starts before T004 records his ruling of them (FR-025). |
| Workflow: *"`/speckit.analyze` MUST report no critical findings before implementation"* | PENDING (T003) | An independent reviewer runs the analyze after this revision; the plan writer does not. Its findings are dispositioned at T004. |
| Repository Constraints | PASS, with one deviation (Complexity Tracking) | **Shared tree**: every writer works in its own clone or worktree, stages explicit paths and commits with pathspecs. **Worktree mode**: this feature's planning runs from the lane's own worktree of its own openxFactory clone. **The aggregation pin**: each openxFactory landing is followed by the aggregation's ordinary pin-sync in `opensoft/xFactory`, a separate commit that is not an arc landing (034's practice). At the cut, T083 runs it with the openDox/openXdox three-way gitlink parity (the aggregation's `CLAUDE.md` working rule 2). |

**Post-design re-check (after data-model.md, contracts/ and quickstart.md).**
No row changes. The design adds three product file kinds, each carrying
`schema_version` and `kind` (Principle IV): `.opendox/governance.yaml`
(`kind: opendox-governance`, decision N-1), `health/dispositions.yaml` (`kind:
opendox-health-dispositions`) and `health/packs.yaml` (`kind:
opendox-health-packs`). The finding shape is a contract in openDox-spec, not a
file kind. No design element moves anything out of openxFactory (FR-022).

## Project Structure

### Documentation (this feature)

```text
specs/038-opendox-document-tool-self-maintenance/
├── spec.md                 # the clarified specification (ce64afc9)
├── clarify-questions.md    # R2Q1–R2Q25, answered (6003486656); 34 deferred items
├── checklists/
│   └── requirements.md     # the quality checklist
├── plan.md                 # this file
├── research.md             # R0–R12: measurements, the inventories credited, the ruled arc
├── data-model.md           # entities, fields, state transitions
├── contracts/
│   ├── health-finding.md            # the finding's neutral shape (openDox-spec schema 1)
│   ├── health-packs-manifest.md     # health/packs.yaml (openDox-spec schema 2)
│   ├── health-exceptions.md         # health/dispositions.yaml (openDox-spec schema 3)
│   ├── cli-http-submit-land.md      # submit, land: CLI verbs, routes, /capabilities
│   └── cli-http-health.md           # health run|list|fix|accept: CLI verbs, routes
├── quickstart.md           # AT-R2: the HTTP half (CI) and the browser half (host)
├── tasks.md                # T001–T093
└── evidence/               # created by the tasks; Status: record
```

### Source code: the repositories release 2 lands in

| tag | repository | what release 2 changes there | merge method |
|---|---|---|---|
| `[oDc]` | opensoft/openDox-code | Group 12's ports, verbs, routes and view controls; the feature-007 guard (R2Q6 (a)); the health package (store migration, families, engine, fix loop, exceptions, view); the check-pack contract, manifest, sandbox, patch validator and engine integration; `validate.yml` (R2Q17 (a)); the `0.2.0` bump; the arc's re-authored `lines` slice (T072) | squash or merge, never rebase |
| `[oXc]` | opensoft/openXdox-code | U-1 to U-5 and U-7 (the repair of 12.5's reds, no protected edit outside an entry); U-8's pin; U-9's composed workflow, permanent (ARC-Q2 (a)); the arc's seams and retargets (T074) | squash or merge, never rebase |
| `[oD]` | opensoft/openDox (root) | the code pin per phase; the spec pin and the `dox-v1.y` bundle (R2Q22 (a)); README: the governance declaration, `submit`, `land`, `health`, and the 0.2.0 install line | squash or merge, never rebase |
| `[oX]` | opensoft/openXdox (root) | the code pin and `contracts/opendox-pin.yaml` per phase | squash or merge, never rebase |
| `[oDs]` | opensoft/openDox-spec | the three health schemas (R2Q22 (a)) | squash or merge, never rebase |
| `[oxF]` | opensoft/openxFactory | pin pairs, host wiring (11.1 surfaces), `edits[].note`s, evidence and bookkeeping (no `Arc:` trailer), batch Q, the arc's OpenSpec change | squash or merge, never rebase |
| `[cxF]` | codeXfactory/codexFactory | feature 007's spec: the four named exceptions (R2Q6 (a)) | **merge commits only** |
| `[xF]` | opensoft/xFactory (aggregation) | the routine pin-syncs after openxFactory landings, and the cut's sync with the three-way parity | as its owner lands pin-syncs |

openDox-code's new files (proposed paths; each is owned by exactly one slice,
tasks.md § "Writer slices"):

```text
src/opendox/
├── session_pr.py              # + SubmissionPort, Submission, LocalGitSubmissions, NoSubmissionTarget (T011)
├── submission_push.py         # the push helper factored from runtime/repository_act.py (T011, OQ-12-12)
├── landing.py                 # LandingPort, Landed, MergeConflict, repository_governance, the lander (T012)
├── landing_confirm.py         # the confirmation capability and its two issuers (T012)
├── cli_branch_actions.py      # the submit and land verbs, default-profile contributions (T015, T016)
├── serve_branch_actions.py    # the submit, land-nonce and land routes (T015, T016)
├── health/
│   ├── __init__.py
│   ├── families.py            # the neutral families (T044)
│   ├── engine.py, baseline.py # the engine, the baseline classes (T046)
│   ├── cli.py                 # health run|list|fix|accept (T046 → T053 → T054)
│   ├── applier.py             # the fix loop (T053)
│   ├── exceptions.py          # health/dispositions.yaml (T054)
│   └── routes.py              # the Health view's routes (T057)
├── runtime/health_store.py    # the store (T042)
├── health_contract.py         # THE contract module (N-3): U-0's finding vocabulary (T041), then G15-A's pack protocol (T045)
├── check_pack_manifest.py     # health/packs.yaml, the pin (T047)
├── check_pack_sandbox.py      # bwrap, the canary, bounds (T048)
├── check_pack_shim.py         # the in-sandbox shim (T048)
├── check_pack_patch.py        # the patch validator (T049)
├── check_pack_engine.py       # the engine integration (T056)
└── web/views/
    ├── branch-actions.js      # the submit control and the land confirm control (T015, T016)
    └── health.js, health-model.js   # the Health view (T057)
migrations/0003_health.sql     # runs and findings, with 15.7's provenance columns (T042)
tests/fixtures/health-corpus/  # 14.9 (T043)
tests/fixtures/pack-corpus/    # 15.6a (T055)
```

**Structure Decision**: release 2 adds no repository (R2Q22 (a): "No
repository joins"). Product code lands in openDox-code under new modules beside
the existing seams, never inside the `doxbench-*.js` files FR-037's sentinels
guard (OQ-12-14), and never in the three pinned `session_pr.py` classes
(`test_session_snapshot.py:893-916`). The verbs `submit`, `land` and `health`
are contributions of openDox's DEFAULT profile, so a host profile that replaces
it carries none of them and the hosts' help goldens do not move (R2Q3 (a);
decision N-2). openXdox-code changes only tests, its pin and its workflows in phase 4
(no protected edit outside an allow-list entry), and its `src/` only in the
arc's realization (T074). openxFactory changes only on 11.1's surfaces.

## Phases, and where every release-2 box closes

The box census at this branch's head, `ce64afc9` (research R0), reads 125
boxes in #1144's `tasks.md`: 74 `[x]`, 42 `[ ]` and 9 `[~]`. The 42 open boxes
are the 37 release-2 boxes, the four arc-close boxes, and F9.2.

| phase | boxes that CLOSE in it | exit (all quoted in the phase checkpoint task) |
|---|---|---|
| 0 | none | the plan ruled (T004); batch Q landed (T005), before phase 4's checkpoint; feature 007 amended (T008) before T013 |
| 4 | 12.1, 12.1a, 12.2, 12.3, 12.4, 12.4a, 12.5, F12.1, 12.6, 12.6a, F12.2 (11) | F12.2 exits 0 alone with `gh` absent (20 named nodes); F12.1 exits 0 composed with 174 reds repaired and the oracle printing `ok: … each entered and holding`; interim F11.1 `requirement 1 holds` (T033; SC-001, SC-003) |
| 5 | 6.1, 6.1a, 6.2, F6.1 (4); 14.1–14.9, F14.1 (10); 15.1, 15.1a, 15.1b, 15.2, 15.2a, 15.3, 15.4, 15.5, 15.6, 15.6a, 15.7, F15.1 (12) | F6.1, F14.1 and F15.1 exit 0 as batch Q amends them, F15.1 inside the required `validate` job with the sandbox proved live; 12.5 still green composed at phase 5's pin; interim F11.1 (T066; SC-002, SC-003) |
| close | the ticks of all 37 (T082), after AT-R2 (T080, T081; SC-008) | AT-R2 both halves; bookkeeping under Rule 6; the cut's pin syncs (T083); then the 0.2.0 publish, LAST (T084) |
| every phase, ticked at the ARC's close | 9.5, 11.0, 11.1, F11.1 | interim F11.1 after each phase (T032, T065); final F11.1 at T082 (OQ-038-2) |
| beside phase 5, its own change | F9.2 (outside the 37) | F9.2 re-run after the arc's realization lands (T076); see ARC-5 |

Phase 4's boxes tick at T082 with every other release-2 box, as release 1's
did at plan 034's T097. Each checkpoint quotes its falsifiers; the tick is bookkeeping.

## Dependency graph

```text
T001–T009 (holder: claims, base, analyze, the plan ruling, batch Q, the arc ask [done], the arc encoding [done], feature 007, the lane split)
                          │
DAY ONE (the plan ruled)  T010 [oDc] R2Q17's required-check change (CI owner)        T070 [oxF] author the arc's change
                          T020–T024 [oXc] U-1..U-5   T025 [oDc] U-6 (after W-1)      T040 [oDs] the three schemas
                          T011 [oDc] P4-A            T012 + T013 [oDc] P4-D1 (T013 after T008)
 PHASE 4  [oDc]  T011 → T014 (P4-B) → T015 (P4-C) → T016 (P4-D2; also after T012, T013)
                 T017 (floors; after T011–T016, T025)
          [oD]   T018 (README) after T016;  T027 root pin after T017, T018
          [oXc]  T026 (U-7) after T020, H-2, R-1;  T028 (U-8a pin) after T027;  T029 (U-9) after T020–T026, T028
          [oX]→[oxF]  T030 (U-8b consumer pins + T019 host-unchanged proof) after T029
          [oxF]  T031 (F12.2) after T027;  T032 (F12.1 composed, interim F11.1) after T029, T030
                 → checkpoint T033 (after T005)
 PHASE 5  W1  T041 (U-0)  T042 (HA-1)  T043 (HA-3)      [T040's schemas before T041's, T047's and T054's copies]
          W2  T044 (HA-2)  T045 (G15-A)
          W3  T046 (HA-5)  T047 (G15-B)  T048 (G15-C)  T049 (G15-D)  T050 (G15-H)   T051 floors per wave (CI owner)
          W4  T052 (HA-4)  T053 (HA-6)  T054 (HA-7)  T055 (G15-G)  T056 (G15-E)   T059 [oxF] facet follow-on, if measured
          W5  T057 (HA-8)  T058 (G15-I2)
          W6  T060 [oDs][oD] spec pin + dox-v1.y  →  T061 [oDc] 0.2.0 bump  →  T062 [oD] root pin  →  T063 [oXc] pin, composed re-run
              →  T064 [oX][oxF] consumer pins + host wiring  →  T065 [oxF] evidence (F6.1, F14.1, F15.1, interim F11.1)  →  checkpoint T066
 BESIDE PHASE 5 (ARC-Q3 (a); gates neither release 2's close nor #1144's archive)
          T070 [oxF] author → T071 ratify word → T072 [oDc] lines slice → T074 [oXc] seams, retargets, respellings
          T073 [oXc] composed declarations (ARC-Q2 (a); after T029; not gated on T071) → T074
          T074 → T075 [oxF] host registers the seams, with its pin pairs → T076 [oxF] F9.2 re-run (Rule 6) → T077 archive + topic exit (Rule 6)
 CLOSE    T080 [oDc] AT-R2 HTTP (CI; after T066) → T081 [oxF] AT-R2 browser (host) → T082 [oxF] ticks + arc close (Rule 6)
          → T083 [xF] the cut's pin sync (three-way parity) → T084 [oDc][oD] 0.2.0 publish, on Brett's word: LAST
 EVERY PHASE  T090 pins · T091 trailer · T092 notes · T093 interim F11.1 (run as T032, T065, and finally at T082)
```

## Parallel slices, and the files only one writer may touch at a time

Writers run in parallel when they share no file. The surfaces below are
SINGLE-WRITER: at most one open slice edits each, and a slice that needs one
rebases onto the previous slice's landing before it opens. The order is fixed
here; a change to it is the holder's act, recorded in the PR that changes it.

| single-writer file | slices, in order |
|---|---|
| openDox-code `.github/workflows/validate.yml` | T010 (R2Q17: `ubuntu-24.04`, bubblewrap, the AppArmor sysctl, the live proof, fail-not-skip under `CI`; `EXPECT_SKIPPED` stays 11) → T017 (phase 4's floors) → T051 (phase 5's floors, once per wave) → T080 (AT-R2's `acceptance` job). The CI owner is ONE slice across release 2 (decision N-4) |
| openDox-code `src/opendox/health_contract.py` (THE contract module, N-3) | T041 (U-0: the finding vocabulary) → T045 (G15-A: the pack protocol, appended) |
| openDox-code `src/opendox/session_pr.py` | T011 (new names only; the three pinned classes untouched) → T012 (re-exports, if any) |
| openDox-code `src/opendox/session_git.py`, `tests/test_session_git.py` | T013 alone (R2Q6 (a): `:93`'s rule, the guard's argument check; `:523` still refusing `("merge", "other-branch")`, `:563-564`'s pin moving) |
| openDox-code `src/opendox/serve.py` | T014 (`submission_factory`) → T015 (submit route dispatch, capabilities) → T016 (`landing_factory`, nonce and land routes, `actions.land`) → T052 (HA-4's registration lines) → T057 (HA-8's routes and the `/capabilities` health block) |
| openDox-code `src/opendox/cli.py` | T014 (`_submission_port`) → T016 (`_landing_port`) → T046 (HA-5: the `health` group's local wiring) → T052 (HA-4's registration lines) |
| openDox-code `src/opendox/default_profile.py` | T015 (`submit`) → T016 (`land`) → T046 (`health`) |
| openDox-code `src/opendox/health/cli.py` | T046 (the parser, frozen with `--pack`, `--timeout`, `--local`, `--json`) → T053 (`fix`'s dispatch line) → T054 (`accept`'s dispatch line) |
| openDox-code `src/opendox/workbench.py` | T052 alone |
| openDox-code `src/opendox/branch_session.py` | T016 alone (R2Q5 (a): a landed live session ends by the existing merge observation) |
| openDox-code `src/opendox/web/app.js`, `web/index.html` | T015 → T016 → T057 |
| openDox-code `src/opendox/web/views/staging-workbench.js`, `staging-workbench-model.js` | T025 alone (U-6; the model only if W-1 rules (A)) |
| openDox-code `src/opendox/display_profile.py`, `web/views/display.js` | T050 alone (G15-H) |
| openDox-code `tests/fixtures/web_boundary_census.yaml`, `tests/test_web_boundary.py` | T025 → T015 → T016 → T057 |
| openDox-code `migrations/0003_*.sql` and the `tests_runtime/` schema suites | T042 alone (HA-1, with 15.7's provenance columns from its first landing) |
| openDox-code `tests/fixtures/health-corpus/**` | T043 → (read-only copy by T055; a later change re-runs T055's digest test) |
| openDox-code `tests/test_check_packs.py` | T058 alone (the 24 named nodes) |
| openDox-code `pyproject.toml` | T048 (if the sandbox needs package data) → T055 (fixture package data, if any) → T061 (the 0.2.0 bump: the LAST package-changing landing before T062) |
| openDox root `README.md` | T018 (the declaration, `submit`, `land`) → T046's README line (the `health` hook line, OQ-H-18; it rides in T062) → T084 (the 0.2.0 install line) |
| openDox root `code` gitlink, `contracts/code-pin.yaml` | T027 (phase 4) → T060's spec pin and bundle (spec side only) → T062 (phase 5) |
| openXdox-code `tests/conftest.py`, `tests/test_host_plane.py` | T020 (U-1) → T073 (the rail registration, ARC-Q2 (a)) → T074 (the stand-in host registers the arc's seams, if its tests need them) |
| openXdox-code `src/openxdox/gate_console.py` | T021 (U-2, the schema read) → T074 (the arc's retarget) |
| openXdox-code `src/openxdox/generator.py`, `corpus_root.py`, `cli_gate.py`, `gate_routes.py`, `snapshot_registry.py`, `completeness.py`, `round_trip.py` | T074 alone (no phase-4 or phase-5 slice edits them; T029's run reads them) |
| openXdox-code `tests/protected_suite_respellings.yaml` and the five protected files U-7 enters | T026 alone in phase 4 (entries chain by blob); a later edit to a protected suite adds its entry in its own PR |
| openXdox-code `tests/declared_exclusion.yaml` | T073 (entries become declared composed integration tests, with count and reason) → T074 (the `doc_health` reason empties) |
| openXdox-code `tests/test_dependency_direction.py` | T074 alone (`DOC_HEALTH_SURFACE` to empty) |
| openXdox-code `pyproject.toml` | T028 (phase 4's `opendox @` pin) → T063 (phase 5's) → T074 (only if T072 lands after T063's pin: the arc's own pin, ARC-6) |
| openXdox-code `.github/workflows/` (`validate.yml`, the new composed workflow) | T029 (U-9: the composed workflow, permanent) → T073 (the rail, contracts and governed-behaviour files) → T074 (the help-tree `--deselect` and its guard leave, F9.2's two code removals) |
| openxFactory pin pairs and host wiring | T030 (phase 4) → T064 (phase 5) → T075 (the arc's seams, with its own pin pairs, unless they ride T064) |
| openxFactory `openspec/changes/add-neutral-product-standalone-operability/` | T005 (batch Q) → T076 (F9.1's `--deselect` line, F9.2's tick) → T082 (the release-2 ticks and the arc-close boxes), each under its own Rule 6 window; T076 and T082 may land in either order |
| the arc's own change directory (`openspec/changes/<ARC-2>/`) | T070 → T071 → T077 |
| codexFactory `specs/007-workbench-branch-sessions/spec.md` | T008 alone |

## Two lanes: the proposed split (Brett and the holder confirm it at T009)

Lane openxfactory-4 is the coordinator. It claims for itself, writes its own
slices, and LANDS EVERY PR, its peer's included (the landing kit, Rule 6
windows, the register). Lane openXfactory-3 is the peer, with its own writers;
it claims its slices on `#656` (T001) and hands each PR to the coordinator
when it is READY. Neither lane opens a PR on a file the other lane's open slice
owns (the single-writer table above).

| lane | slices (tasks) | why this lane |
|---|---|---|
| **openXfactory-3 (peer)** | **Phase 4's repair, P4-F:** U-1 (T020), U-2 (T021), U-3 (T022), U-4 (T023), U-5 (T024), U-6 (T025), U-7 (T026), U-9 (T029). **Beside phase 5:** T073 (ARC-Q2 (a)'s composed declarations, U-9's continuation). **Phase 5's pack track:** G15-A (T045), G15-B (T047), G15-C (T048), G15-D (T049), G15-G (T055), G15-E (T056), G15-I2 (T058). **Re-measures on request** (T002's composed re-run). | Lane 3 wrote R2-INV-P4F (every red node mapped, its slice outline) and Part B of R2-INV-HEALTH (Group 15, the sandbox survey). Its slices are mostly openXdox-code tests and the self-contained `check_pack_*` modules, which share no file with lane 4's open slices except in the fixed orders above. |
| **openxfactory-4 (coordinator)** | **Phase 0:** T001–T009. **Phase 4's product:** T010 (the CI owner, all four of its edits: T010, T017, T051, T080), P4-A (T011), P4-D1 (T012, T013), P4-B (T014), P4-C (T015), P4-D2 (T016), README (T018), the host-unchanged proof (T019). **Pins and evidence:** T027, T028, T030, T031, T032, T033; T060–T066. **Phase 5's health track:** U-0 (T041), HA-1 (T042), HA-3 (T043), HA-2 (T044), HA-5 (T046), G15-H (T050), HA-4 (T052), HA-6 (T053), HA-7 (T054), HA-8 (T057), T059 if needed. **The arc's change (ARC-Q3 (a), owned here):** T070–T072, T074–T077. **The close:** T080–T084. **Every phase:** T090–T093. | The coordinator holds every surface that more than one phase touches (`serve.py`, `cli.py`, `default_profile.py`, `validate.yml`, the pins, `openspec/changes/`), so no cross-lane hand-off happens on a single-writer file mid-phase. ARC-Q3 (a) names lane openxfactory-4 the arc's owner. |

**Cross-lane hand-offs, each at a landing, never mid-slice:** the census
fixture (T025, lane 3 → T015, lane 4); openXdox-code's `tests/conftest.py`
(T020 and T073, lane 3 → T074, lane 4); `gate_console.py` (T021, lane 3 →
T074, lane 4); openXdox-code's workflows (T029 and T073, lane 3 → T074,
lane 4); openDox-code `pyproject.toml` (T048 and T055, lane 3 → T061, lane 4).

## The critical path

Inferred from the task graph and lane 3's sizing, not measured.

```text
T004 (ruling, incl. R-1, W-1, H-1, H-2) → T020 (U-1) → T026 (U-7) ─┐
T011 → T014 → T015 → T016 → T017 → T027 → T028 ─────────────────────┴→ T029 (U-9) → T030 → T032 → T033
  → [phase 5] T041 → T044 → T046 → T053 (also after T016) → T057 → T060 → T061 → T062 → T063 → T064 → T065 → T066
  → T080 → T081 → T082 → T083 → T084 (the publish, last)
```

- **The long pole is P4-F (U-1 → U-7 → U-9)**, as lane 3's inventory says
  (R2-INV-12 § "Proposed phase-4 task outline"; R2-INV-P4F § "Slice
  outline"). It starts the day the plan is ruled. U-7 also waits on H-2 and,
  for its admitted part, on R-1; so R-1 and H-2 are on the critical path, and
  W-1 and H-1 gate U-6 and U-5 off it.
- **Phase 5's own pole** is the health track, U-0 → HA-2 → HA-5 → HA-6 → HA-8
  (HA-6 also needs phase 4's `land`). The sandbox (G15-C, T048) is the
  riskiest slice; R2Q17's CI provisioning (T010) moves to DAY ONE so that its
  failure modes surface before G15-C is written.
- **The overlap proposal (decision N-6).** Phase 5's openDox-code slices may land
  once T027 has pinned phase 4's openDox-code commit, without waiting for
  T033, because P4-F's tail is openXdox-code work that shares no file with
  them. This shortens the path by the length of T028–T033. The alternative is
  release 1's strict order: every phase-5 task after T033.

**What starts the day the plan is ruled (T004):** T005 (batch Q), T008
(codexFactory), T009 (claims), T010 (CI), T011 (P4-A), T012 (P4-D1), T013
(after T008), T020–T023 (U-1 to U-4), T024 (U-5, H-1 ruled), T025 (U-6, W-1
ruled for its model part), T040 (the three schemas in openDox-spec, from
`contracts/`) and T070 (authoring the arc's change).

## Scheduled acts the brief names, and where each sits

| # | act | task(s) | when |
|---|---|---|---|
| 1 | R2Q9 (a)'s seven amendments, ONE batch in plan 034's T007 form, under Rule 6 | T005 (batch Q) | the FIRST act; lands before T033 and before any task whose falsifier reads an amended line (T031, T032, T052, T065) |
| 2 | R2Q6 (a)'s four feature-007 exceptions | T008 (codexFactory spec, merge commit only) → T013 (openDox-code guard and pins) | T008 day one; T013 lands with T012, after T008 |
| 3 | R1Q6 (d): the `doc_health` direction arc decided before F12.1 needs the 16 suites | T006 (DONE: ruled on `6003918488`); T007 (DONE: encoded here) | The latest point it could have been asked was the claim of U-9 (T029), whose composed run is F12.1. It was asked and ruled before this plan was ruled, so phase 4's checkpoint waits on nothing |
| 4 | R2Q17 (a)'s required-check change in openDox-code's `validate.yml` | T010, the CI owner | day one, before any phase-4 or phase-5 slice adds a test |
| 5 | R2Q22 (a): three openDox-spec schemas, digest-checked copies, one more `dox-v1.y` minor | T040 (schemas) → T041, T047, T054 (copies) → T060 (spec pin, bundle cut) | T040 day one; T060 at phase 5's W6, before T062's code pin; batch Q carries the addendum (decision N-5) |
| 6 | R2Q23 (a): `opendox` 0.2.0, tag `v0.2.0`, LAST | T061 (the bump) → T084 (the publish, on Brett's word after AT-R2) | T084 is the last task of the release |
| 7 | R2Q24 (a): AT-R2, HTTP half in CI, browser half on the host | T080, T081; quickstart.md | after T066 |
| 8 | The pin sync across openxFactory and the aggregation, with the three-way openDox/openXdox parity | T030, T064 (openxFactory per phase), the routine aggregation syncs after each openxFactory landing, and T083 at the cut | T083 after T082 |
| 9 | The arc-close boxes 9.5, 11.0, 11.1, F11.1, and plan 034's T090–T093 | T090–T093 (every phase); ticked by T082; 034's four close by reference in T082 | at the close (OQ-038-2, as refined) |
| 10 | The direction arc's realization (ARC-Q1–ARC-Q4) | T070–T077 | beside phase 5; T073 after T029 |

## Pins and landing order (9.5): one openDox-code commit per phase, everywhere

Release 1's seven steps hold unchanged (plan 034 § "Pins and landing order";
the runbook `docs/openxdox-pin-resync-runbook.md`, #1154). Each step's PR opens
only after the step before it has landed.

| step | phase 4 | phase 5 | the arc (ARC-6) |
|---|---|---|---|
| 1. openDox-code lands | T010–T017, T025 | T041–T058, T061 (the bump last) | T072 |
| 2. openDox root: `code` gitlink, `contracts/code-pin.yaml`, workflow `@sha`s, ONE commit (`make pins`) | T027 | T060 (spec pin and bundle first) → T062 | rides T062 if T072 landed before T061; else its own root commit |
| 3. openXdox-code `pyproject.toml` `opendox @` to the SAME commit | T028 | T063 | rides T063, or its own |
| 4. openXdox-code lands | T020–T024, T026, T029 | none (T063 re-runs 12.5 composed) | T073, T074 |
| 5. openXdox root: `code` gitlink and `code-pin.yaml`; `opendox-pin.yaml` to step 2's commit | T030 | T064 | T075 |
| 6. openxFactory: both pin pairs, one commit each, in ONE PR with the host wiring | T030 (+ T019) | T064 (+ HA-4's host-wiring test) | T075 (the seams' registration) |
| 7. the aggregation: routine pin-sync after each openxFactory landing | after T030 | after T064 | after T075 |

- **The aggregation's rules** (its `CLAUDE.md` working rule 2): an openxFactory
  pin-sync moves the gitlink AND `.github/clearing/openxfactory/PIN.yaml` in
  ONE commit; a sync touching `openDox` or `openXdox` keeps the aggregation's
  root gitlink EQUAL to openxFactory's nested gitlink AND to the `commit:` in
  openxFactory's `contracts/opendox-pin.yaml` / `contracts/openxdox-pin.yaml`,
  in the SAME commit. `tests/test_opendox_openxdox_gitlink_parity.py` and
  `tests/test_clearing_contract_pin.py` SKIP in `validate` (no submodules), so
  each sync runs `python3 -m pytest tests/ -q` with `openxFactory` initialized
  before it is pushed (T083 quotes it).
- **The composed workflow's openxFactory pin** (U-9, permanent by ARC-Q2 (a)).
  openXdox-code names ONE openxFactory commit, by full sha, in one place the
  workflow reads (decision N-7). It advances after T030 and after T064, each in
  an openXdox-code PR of its own, so the composed run always tests the host
  that openxFactory's `main` carries.
- **Merge method.** Squash or merge commit, never rebase, in every product
  repository, so each landing is ONE first-parent commit for 5.4a's, 12.5's
  and 11.1's guards. codexFactory allows merge commits ONLY (T008).

## The trailer, the guard and Rule 6

- **Realization landings** carry `Arc: neutral-product-standalone-operability`
  and `Lane: openxfactory-4` (or `Lane: openXfactory-3` for the peer's), in
  every repository the arc touches, openDox-spec included (T040, T060).
- **Bookkeeping** carries NO `Arc:` trailer (R1Q20 (a)): this feature's files,
  batch Q, #1144's ticks, evidence notes, interim guard output, and the
  codexFactory spec amendment (T008; decision N-8).
- **The arc's change** (T070–T077) is not #1144's arc: its realization landings
  carry their own trailer value (decision ARC-4), so #1144's guards neither count nor
  miss them.
- **Non-arc acts in plan 034's T066 form** (both pins, no `Arc:` trailer): T059, only if
  G15-H's display-facet schema bump moves an openxFactory facet test.
- **F11.1's guard is closed** (HOST, HOST_TESTS, PIN_PAIRS, COMPOSITION_TESTS,
  ADMITTED_ARC_EDITS). It grows only by a further ruling (`5890601202`). No
  task here needs it to grow: T019 and T064's host-wiring tests sit under
  `tests/domain_profile/`, a HOST_TESTS surface (inferred from the guard's
  constants as R2-INV-12 § "Proposed phase-4 task outline" reads them; T032's
  interim run proves it).
- **Rule 6.** Every PR touching `openspec/changes/` lands under a `LANDING` /
  `LANDED` window: T005, T070, T071, T076, T077 and T082. Realization PRs never
  touch it. No closing keyword appears in a commit message or PR body.

## Ruled answers, round 1 (`6003486656`)

Brett Heap answered all 25 by interactive multi-choice, verbatim *"Accept all
25 recommended (Recommended)"* (`#656` `6003486656`). Every question took (a).
`spec.md` § Clarifications holds each answer; this table names where the plan
carries it out. "No task" means the answer constrains tasks without being a
task.

| question | answer | what it fixes in this plan |
|---|---|---|
| R2Q1 | (a) | One user-facing interface; three ports stay split. T015/T016 put `submit`/`land` in every governance mode under openDox's own profile; batch Q (T005) records the map's phrase as a non-normative reading. Interplay I-1 confirms the reading. |
| R2Q2 | (a) | `pull_request_factory` keeps `GhPullRequests`; the new pair defaults to `LocalGitSubmissions` (T014). Batch Q's repoint-sentences note (T005). Ruling `5783934499`'s third bullet and 12.5's "host's implementation registered" go unrealized (Conflicts C-3). |
| R2Q3 | (a) | No governed host carries `submit`, `land` or `health` in release 2: the verbs are default-profile contributions (decision N-2); T019 and T064 prove the hosts unchanged; F12.2's host side runs against a registered test host (T012, T016, T031). |
| R2Q4 | (a) | The instrument is a contributed `SubmissionPort` in the host profile; under `governed` no lander is bound; `land` submits through it (T012, T016). |
| R2Q5 | (a) | Any local branch but `main`; a landed live session ends by the existing merge observation (T016, `branch_session.py`). No standalone session opener (no task). |
| R2Q6 | (a) | The lander's own landing worktree, `--no-ff`; ff-only of a clean served checkout on `main`; `land` pushes nothing, `ls-remote` check first. Feature 007's four exceptions: T008 (codexFactory) and T013 (the guard and pins). |
| R2Q7 | (a) | Default branch `main`; no `main` → `unknown`, refused naming it; no declaration → `land` refuses naming the file and content (T012); the root README documents it (T018). Interplay I-2. |
| R2Q8 | (a) | F12.1 runs composed (batch Q's line, T005); the repair slice U-1 to U-9 (T020–T029); R1Q6 (d)'s decision first (T006, done). |
| R2Q9 | (a) | Batch Q (T005), the first act: F6.1's entry point and struck "Today" text; F14.1/F15.1 start the document server; F15.1's sandbox precondition; the forking pack's child carries its pack id; the export cannot be steered by `export-subst`/`export-ignore`; the escaping pack's restore is a write; `--local` on `submit`, `land`, `health`. Realized by T015, T016, T046, T048, T052, T058. |
| R2Q10 | (a) | The finding id rule (T041); `health list --json` carries `kind` (T046); F14.1/F15.1 select planted findings by fixture document (batch Q). |
| R2Q11 | (a) | `stage-location-mismatch` reads the six role keys' top-level directories; `auto-fix` edits `stage:` only (T044, T053). |
| R2Q12 | (a) | Baseline = the previous default-tip run in the store; three classes; disappearance only between default-tip runs; citations; the uncited re-raise (T046). Interplay I-2. Conflicts C-2 records the narrowed reading. |
| R2Q13 | (a) | DOMAIN: `identity.TABLES`, and the closure test reads `0001` with `0003_`, in one change (T042). |
| R2Q14 | (a) | 6.1a satisfied vacuously; no family moves, no shared module (T052 records it at the tick). |
| R2Q15 | (a) | Hosted plane: the health view, routes and verbs refuse by name and record nothing; the schema still migrates (T046, T057, T042). |
| R2Q16 | (a) | Trusted installed code in process; only manifest-listed packs sandboxed; no sandbox → no packs and one finding; no Seatbelt (T048, T056, T052). |
| R2Q17 | (a) | The required-check change, by this word (T010). |
| R2Q18 | (a) | Packs import the standard library and `opendox.health_contract` only (N-3); digest plus version pin everything (T045, T047, T048). |
| R2Q19 | (a) | Kept as ratified: packs see only the exported tree (T048). No amendment task. |
| R2Q20 | (a) | Kept as ratified: pack checks are model-free (T045). No amendment task. |
| R2Q21 | (a) | `health/packs.yaml` is authoritative; the `stack.yaml` lockstep check is F2's (T047). No release-2 task for F2. |
| R2Q22 | (a) | Three openDox-spec schemas (T040), digest-checked copies (T041, T047, T054), one `dox-v1.y` minor (T060) under batch Q's 9.5 addendum. |
| R2Q23 | (a) | 0.2.0 bump (T061), publish LAST on Brett's word (T084), under batch Q's batch-O style addendum. |
| R2Q24 | (a) | AT-R2 (T080, T081; quickstart.md). |
| R2Q25 | (a) | Evidence holds locators only; the view reads the passage from git (T041's shape, T042's store test, T057). |

## Ruled answers, the `doc_health` direction arc (`6003918488`)

Lane openXfactory-3 prepared the ask read-only (`lane-coord-034/r2/R2-ARC-ASK.md`,
CLAIMED on `#656` `6003715712`). Brett Heap answered all four by interactive
multi-choice; `6003918488` records his words verbatim.

| question | answer | what it fixes in this plan |
|---|---|---|
| ARC-Q1 | (a) *"Retarget all eight (Recommended)"* | The generic `lines` slice re-authored in openDox-code (T072); the governed names reached through seams openXdox-code declares (T074) and openxFactory's host wiring registers (T075, the pattern of `scripts/opendox_host.py:518-533`); the 7 test files that import `doc_health` respelled, none of them protected (T074); `DOC_HEALTH_SURFACE` empty; no `corpus-adapter-seam` change. |
| ARC-Q2 | (a) *"Composed CI in openXdox-code (Recommended)"* | U-9's composed workflow, pinned to openxFactory, is PERMANENT (T029); it gains R1Q24's 3 rail files and 5 contracts files and the governed-behaviour tests, declared as integration tests with count and reason (T073); requirement 9 closes for openXdox-code by declaration; F9.1's declaration is amended in batch B's form, in batch Q (T005). |
| ARC-Q3 | (a) *"Own change, beside phase 5 (Recommended)"* | Its own OpenSpec change, `code_surface:` naming openXdox-code, openDox-code and openxFactory host wiring (T070); Brett's ratify word (T071); realization slices (T072–T075); archive on merged, green evidence (T077); owned by lane openxfactory-4; gates neither release 2's close nor #1144's archive; F12.1 stays composed until it lands. `target_release:` is Brett's (ARC-1). |
| ARC-Q4 | (a) *"Confirm (Recommended)"* | The decision is discharged before F12.1; the realization is not on 12.5's path. T006 is done. |

Measured in the ask (fact 3): 0 of the 174 composed reds are `doc_health`-caused,
so U-1 to U-9 and R-1, W-1, H-1 and H-2 do not change.

## Design decisions for Brett to rule with this plan

**Every row is a PROPOSAL.** Brett rules them when he rules the plan (T004);
any row can be raised to a ruling question on request. "Rec." is the
recommended option; "Alt." is the alternative put beside it. Rows 1–34 are the
items `clarify-questions.md` deferred to the plan ("Deferred to the plan, with
proposed defaults"); each says whether it ADOPTS that default or REFINES it.
Then come the three interplays, the phase-4 repair items, the arc ruling's open
items, and the items this plan found.

### A. The 34 deferred items

| # | id | decision (Rec.) | Alt. | why (one line) |
|---|---|---|---|---|
| 1 | OQ-12-9 | ADOPT. The CLI `submit` is NOT under the console-presence and `--actor` gate; it runs as the invoking user. The route stays gated (12.4a). | Gate the CLI as `gate open-pr` is (`cli.py:1253`). | F12.2 runs `submit` non-interactively with no actor and expects success, so #1144 already decides it. |
| 2 | OQ-12-11 | ADOPT. A credential-bearing remote (userinfo in the push URL) is refused by name before any push, as `attach_remote` refuses one (`repository_act.py:203`); the refusal text is redacted (12.1a). | Push through it and redact the message. | No secret ever reaches a message that must then be redacted. |
| 3 | OQ-12-12 | REFINE. Factor the runtime's hardened push (`repository_act.py:1335-1372`) into a new `submission_push.py` that takes a named branch; `repository_act.py` calls it, and `LocalGitSubmissions` calls it. The remote is `origin` only; several push URLs are refused by name. | Mirror `GhPullRequests.push`'s plain argv. | One hardened push path, already tested, instead of two; the factoring is named so T011 owns `repository_act.py`'s edit. |
| 4 | OQ-12-13 | ADOPT, with names. Two routes: `POST /actions/session/land-nonce` mints a nonce bound to the branch and its head; `POST /actions/session/land` consumes it once. Both sit behind 12.4a's three-clause gate and the console token. | One route with a two-step body. | 12.6a's nonce is "issued for that branch" by the server; separating issue from use makes single-use testable. |
| 5 | OQ-12-14 | ADOPT. `submit` reuses the `session` capability; a new `actions.land` is true only where a lander is bound (plan 034's T084 honesty rule). The controls live in a new `web/views/branch-actions.js`, never in the `doxbench-*.js` files FR-037's sentinels guard. | A new `actions.submit` key as well. | The flags stay honest, and no sentinel-guarded file moves. |
| 6 | OQ-12-16 | REFINE. F12.2's evidence runs under a PATH that hides `gh` (a `W=$(mktemp -d)/bin` holding links to `git` and `python` only), with `command -v gh` asserted empty and recorded, both locally and in CI. | A container image without `gh`. | GitHub-hosted runners ship `gh` (inferred from R2-INV-12 OQ-12-16), so PATH-hiding is the form that works in both places. |
| 7 | OQ-12-17 | ADOPT. `LandingPort.land(branch)` serves the fix loop's batches unchanged: a batch is one draft branch. | A batch-land API. | One signature, one confirmation per branch. |
| 8 | OQ-H-2 | ADOPT. The registered check names its own default scoped families, which the scoped action asks for when a caller names none. openxFactory's host-wiring test adapts at T064's pin, under `tests/domain_profile/`. | Callers must always name families. | Today's callers keep working. |
| 9 | OQ-H-3 (plan half) | ADOPT. One neutral check: the engine's built-in families, attributed `opendox`, are what openDox registers at the scoped seam (T052). A scoped run is not stored. | Two checks, the seam's and the engine's. | One implementation; Group 6 and Group 14 cannot drift apart. |
| 10 | OQ-H-8 | ADOPT. Orphans, stale stubs, an unmovable broken link and non-derivable front matter are all `human-only`. | `assisted` for stale stubs. | `auto-fix` and `assisted` stay exactly the ruled lists. |
| 11 | OQ-H-10 | ADOPT. A moved link target is detected structurally: a unique basename elsewhere in the tree is the target; an ambiguous or absent one makes the finding `human-only`. | Rename detection from git history. | Deterministic from one tree; packs and the baseline never need history. |
| 12 | OQ-H-11 | ADOPT. An `assisted` proposal with no model is deterministic: a front-matter note naming the other document, which the human edits. A near-duplicate's `path` is the later-committed document of the pair. | A model-written merge proposal. | Release 2 ships no model-assisted family (row 18). |
| 13 | OQ-H-13 | ADOPT, with the kind named. `health/dispositions.yaml` carries `schema_version: 1` and `kind: opendox-health-dispositions`; entries are keyed by finding id (R2Q10) with a `reason`. An accepted finding is suppressed, not downgraded. A file of another kind at that path is refused by name (it is the aggregation's own file kind in `opensoft/xFactory`, Conflicts C-7). | Downgrade an accepted finding's severity. | F14.1 asserts the accepted finding ABSENT. |
| 14 | OQ-H-14 | ADOPT. `accept` in a checkout writes the working tree (F14.1). With no working tree, it writes a draft on a branch that lands through `land`. | Refuse `accept` on a bare repository. | One path to the default branch, the landing rule. |
| 15 | OQ-H-15 | ADOPT. `health/dispositions.yaml` and `health/packs.yaml` join the settings-document exclusion. | Lint them as documents. | They are configuration, not documents. |
| 16 | OQ-H-16 | ADOPT. Root `README` and index documents are exempt from "nothing links to it"; T043 measures the `plain-documents` fixture and declares the rule in the module. | No exemptions. | Entry documents have no inbound link by design. |
| 17 | OQ-H-18 | ADOPT. "Optionally on commit" means on demand, plus a documented hook line, `opendox health run --repo-root .`, which the user may add. The product writes nothing under `.git/`. | An `install-hook` verb. | The product never writes under `.git/`. |
| 18 | OQ-H-20 | ADOPT. No built-in family is model-assisted in release 2; an `assisted` proposal that ever needs a model goes through Group 16's trusted binding, through `doxbench_provider.py` alone. | Near-duplicate proposals by the bound model. | F14.1 stays deterministic and model-free in CI. |
| 19 | OQ-H-21 | REFINE. Near-duplicates use openDox's own `doxbench_knowledge` embedding with cosine, IF T044 measures that it runs with no model binding; its threshold is set by T044 so that the fixture's planted pair is above it and every other fixture pair below, and recorded in the module and the evidence. If it needs a binding, a lexical shingle (Jaccard) similarity replaces it. | Always the lexical shingle. | Health must run on every local install, model or none (SC-006); whether the embedding needs a binding is not measured (inferred risk). |
| 20 | OQ-H-22 | REFINE. A runs table and a findings table, keyed by the corpus's resolved root, with no foreign key to `projects`; the findings table carries 15.7's `pack_id`/`pack_version` NOT NULL and a `patch` column (row 31). | A foreign key to `projects`. | F14.1 creates no project; one migration carries every column (HA-1's single ownership). |
| 21 | OQ-H15-1 | ADOPT. A pack is a Python package that an engine-provided shim imports inside the sandbox, calling 15.1's protocol. Python is the only pack runtime in release 2. | Any executable speaking a JSON protocol. | One runtime to sandbox and to pin. |
| 22 | OQ-H15-5 | ADOPT, with names. rlimits always (address space, CPU seconds, processes, file size), cgroups only where delegated, `bwrap --size` for the tmpfs, a stdout byte cap; defaults declared in `health-packs-manifest.md`. A bound hit is a finding against the pack. | Require cgroups. | cgroup delegation is absent on many hosts (inferred); rlimits are always there. |
| 23 | OQ-H15-9 | ADOPT. The canary is a per-run self-check of the sandbox: product behaviour, so F15.1 stands. | A test hook (F15.1's text then changes, a ruling). | No falsifier text moves. |
| 24 | OQ-H15-10 | ADOPT. A pack's declaration is a static file inside the pack (`opendox-pack.yaml`), read before any pack code runs; forbidden keys (baseline, landing, classes) are refused by name. | Runtime output of the pack. | No pack code runs before its declaration is checked. |
| 25 | OQ-H15-11 | ADOPT. One JSON document on stdout; stderr dropped, except a bounded tail in a failure finding. | JSON lines. | One bounded parse. |
| 26 | OQ-H15-12 | ADOPT. The subtree form of `sorted-ls-tree-r-v1` for a corpus-relative source is `<commit>:<source>` with relative paths; gitlinks inside a pack are refused. Fixed in T047 before T055 commits any fixture digest. | The whole-tree form only. | A corpus-relative pack needs a subtree digest that cannot drift. |
| 27 | OQ-H15-14 | ADOPT. The engine, never the pack, fetches a git-URL source at `health run`, into a cache under `OPENDOX_STATE_DIR`; offline, the entry gets a finding against it. | Fetch only on an explicit verb. | No new verb, and offline is visible as a finding. |
| 28 | OQ-H15-15 | ADOPT. Pack labels enter the display facet as a health role family keyed by pack and family id, under a schema-version bump; a host profile's labels win. | Render the pack's raw labels. | 15.3 routes labels through the facet; T059 covers any openxFactory facet test the bump moves. |
| 29 | OQ-H15-18 | ADOPT. The product's own `pack_version` is the installed version (15.7); each family's own version rides in the finding's evidence. | A `pack_version` per family. | 15.7 fixes it. |
| 30 | OQ-H15-19 | ADOPT. Pack ids are `[a-z0-9-]`, unique per manifest. An install-level or pre-run finding has `pack_id` `opendox` (or the entry's id), an empty `path`, and `human-only`. | Dots and underscores too. | Ids map to valid ref names (R2Q10). |
| 31 | OQ-H15-20 | ADOPT. A pack's patch is stored with its finding at `run`, validated at `run` and again at `fix`. | Re-obtain it at `fix`. | `fix` needs no second sandbox run, and re-validation catches drift. |
| 32 | OQ-H15-21 | ADOPT. `bwrap` at a fixed system path, verified by the probe; the minimum version is one that has `--json-status-fd`, `--disable-userns` and `--size`. T010 records `bwrap --version` on the runner. | A PATH lookup. | PATH can be steered; the version floor is the flags the sandbox uses. |
| 33 | OQ-038-1 | ADOPT. A shown conflict's refusal names the remedy: bring `main` into the branch and resolve there. No conflict verb or editor. | A `land --rebase` helper. | #1144 declares none. |
| 34 | OQ-038-2 | REFINE, after `6003918488`. This feature performs 9.5, 11.0, 11.1 and F11.1 in phases 4–5 and ticks them at the close (T082); plan 034's T090–T093 close by reference there. #1144's archive is the holder's. The proposed default's last clause ("blocked until F9.2 closes on the direction arc's landing") is withdrawn as written, because ARC-Q3 (a) rules that the arc gates neither release 2's close nor #1144's archive; ARC-5 puts the F9.2 consequence to Brett. | Keep the default's clause and read ARC-Q3 (a) as "not scheduled to gate". | The ruling post-dates the default. |

### B. The three interplays the spec writer reported at `ce64afc9`

| # | id | decision (Rec.) | Alt. | why (one line) |
|---|---|---|---|---|
| 35 | I-1 (R2Q1 (a) with R2Q3 (a)) | CONFIRM THE READING. "The same in every mode" means every GOVERNANCE mode of a repository (`standalone`, `governed`, `unknown`) under openDox's own profile. A host profile that replaces the default carries none of `submit`, `land` or `health` in release 2. Under openDox's own profile, a `governed` repository with no host instrument refuses `land` by name ("governed-without-an-instrument", 12.6a). FR-004 states both answers side by side. | Read "every mode" as including host profiles, so hosts carry the verbs. | That reading contradicts R2Q3 (a); this one is the only one under which both answers hold. |
| 36 | I-2 (R2Q7 (a) with R2Q12 (a)) | A run in a repository with no `main` records ONE install-level finding (`pack_id` `opendox`, empty `path`, `human-only`, kind `no-default-branch`) that names the absent default branch, and lists every other finding UNCLASSED: no new, upgrade or persistent class, and no disappearance is measured. `land` there refuses (`unknown`). Every repository openDox itself creates is created on `main` (T012 audits the creation sites, and pins `-b main` where git's `init.defaultBranch` would otherwise decide). | Classify every finding `new` on every run, with no note. | "New, every run" is noise that hides what is new; one finding tells the user why and what fixes it. |
| 37 | I-3 (bookkeeping beyond R2Q9) | R2Q2 (a)'s repoint-sentences note, R2Q8 (a)'s F12.1 "runs composed" line and R2Q10 (a)'s selection lines in F14.1 and F15.1 ride in R2Q9 (a)'s ONE batch (batch Q, T005), in one Rule 6 window, before phase 4's first checkpoint. | A batch per phase, as each falsifier is reached. | All three are ruled now, and one window costs the other lanes one hold. |

### C. Phase 4's repair items (R2-INV-P4F § "Items needing a ruling or a holder's word"; § "Open questions")

| # | id | decision (Rec.) | Alt. | why (one line) |
|---|---|---|---|---|
| 38 | **R-1** (a RULING) | (a) A new `edit: admitted` kind, of the R1Q26 (a) sort, that reaches module-level text: `protected_suites.py`'s `_inside_the_test` rule is amended to accept a named module-level span (`_CREATE_HARNESS` `:492-553`, `_SESSION_HARNESS` `:1008-1094`, and `:1291`/`:1333`), each admitted edit entered and reviewed in U-7's PR; 12.5's falsifier note rides in batch Q. All 26 `test_staging_workbench.py` nodes then close with the suite still in 12.5's set. | (c) Re-scope 12.5's governed set to drop `test_staging_workbench.py`; or (b) DJ for the import-free pins only (`:802`, `:1286`), which leaves 21 harness nodes red. | (a) keeps the whole proof and names every edit; (b) does not finish, and (c) shrinks the proof. `:1291` and `:1333` move a claim about where routes are defined, a relocation, which only an admitted-edit kind can carry. |
| 39 | **W-1** (a RULING) | (A) openDox-code makes `staging-workbench-model.js` import-free again (U-6, T025), inlining what it takes from `./display.js`. This reverses the S7 amendment the model's header records (`:36-40`; openDox-code `1e46971`). | (A′) `tests/opendox_bundle.py`'s `composed()` flattens the `./display.js` import into its composed copy. | The protected suite asserts the model is import-free (`:802`, `:1286`); (A′) would make that proof pass on bytes the product does not serve. Both clear the same 32 nodes (proved by simulation, R2-INV-P4F § display-js). |
| 40 | **H-1** (holder proposal; Brett confirms) | CONFIRM the shim: a new openXdox-code `scripts/ideation_dashboard/session_git.py` (`import sys; from opendox import session_git as _m; sys.modules[__name__] = _m`) restores the retired spelling `LOCK_HOLDER` imports (`test_session_transaction.py:296`); `test_dependency_direction.py` does not scan `scripts/` (R2-INV-P4F-part-oneoffs § Group L). | Respell the module constant `:296` under R-1 (a)'s kind, with no shim. | U-5 starts on day one without waiting on R-1; if R-1 (a) is ruled, the respelling can replace the shim later. |
| 41 | **H-2** (holder proposal; Brett confirms) | CONFIRM: batch C admits the 17 AL entries (`cmd_gate_*` 7, `hosted_index` 3, share paths 2, Group W 1, Group S2 4), which respell names the split-opendox CARVE moved in commits with no `Arc:` trailer; batch Q records batch C's widened scope at 12.5's falsifier, on the precedent of `5962785556` item 1. | Treat them as RULING-class, or exclude the nodes from F12.1. | They are pure respellings, and the precedent for F5.2's suites already exists. |
| 42 | P4F-3 (runbook placement) | A digest-checked copy in openXdox-code under its `copies.yaml` pattern, so a lone checkout and an offline run have it (U-3). | A CI-time placement from openDox-spec at a named commit. | The copy guard already catches drift, with no network at test time. |
| 43 | P4F-4 (receipt schema source) | openXdox-code vendors it from openxFactory's `contracts/schemas/` with a digest, under `copies.yaml` (U-2); no openXdox-spec change in release 2. | openXdox-spec gains the schema first, and openXdox-code copies from it. | U-2 does not wait on an openXdox-spec PR; the schema's owner today is openxFactory. |
| 44 | P4F-5 (conftest scope and direction) | A governed-suite list beside `HOST_PLANE_SUITES` with its own guard; openxFactory's composite is registered only in the composed run, guarded as `tests/conftest.py:413-421`'s composed-only registration already is. | The gate column on `StandInHost` for every host-plane suite. | The 13 non-governed host-plane suites were never run with the gate column (R2-INV-P4F § Open questions). |

### D. The `doc_health` direction arc's open items (`6003918488`)

| # | id | decision (Rec.) | Alt. | why (one line) |
|---|---|---|---|---|
| 45 | ARC-1 (`target_release:`, Brett's to name) | `target_release: implemented` — the affected repositories' main lines (openDox-code, openXdox-code, openxFactory); no contract bundle is cut; it archives only on merged, green realization evidence because its `code_surface:` is non-empty. | `deferred-allocation`, if the openXdox-spec delta (ARC-3) turns out to need a bundle. | The vocabulary admits `implemented`, a release this estate defines, or `deferred-allocation` (#1144's proposal front matter), and nothing here cuts a bundle. |
| 46 | ARC-2 (the change's id) | `realize-doc-health-direction-arc`. | `retarget-openxdox-doc-health-imports`. | It names the staged topic it exits. |
| 47 | ARC-3 (its spec deltas) | `skip_specs: true` (the pinned CLI accepts it), with no `corpus-adapter-seam` delta, as ruled. If the seams need contract text, an openXdox-spec delta rides along, as the ruling allows. | An ADDED requirement in a new openxFactory capability that records the seams. | Requirement 1 is met, not changed, so there is no requirement to add. |
| 48 | ARC-4 (its trailer) | Its realization landings carry their own `Arc: realize-doc-health-direction-arc` line and `Lane: openxfactory-4`, never #1144's value. | Carry #1144's `Arc:` line, bringing them under F11.1's and 12.5's selection. | Its evidence is its own; #1144's guards close with release 2. |
| 49 | ARC-5 (F9.2 against "gates neither … #1144's archive") | Batch Q adds a note at F9.2: F9.2 is re-run and ticked by the arc's change (T076); if #1144 archives first, F9.2 is reported OPEN at the archive, in R1Q6 (d)'s reporting form, and ticks when T076 lands. | #1144's archive waits for T076 (F9.2's ruled note, `5859927858` and T008's record, read literally). | Only the first honours ARC-Q3 (a)'s words; the second honours F9.2's earlier note. Conflicts C-6. |
| 50 | ARC-6 (its pins) | T072 lands inside phase 5's openDox-code window (before T061), so phase 5's pin chain carries it; T074 and T075 then bring their own openXdox pin pairs after T064. | All of the arc's pins after release 2's cut. | One fewer openDox-code pin chain. |

### E. Items this plan found

| # | id | decision (Rec.) | Alt. | why (one line) |
|---|---|---|---|---|
| 51 | N-1 (`.opendox/governance.yaml`) | Its shape is `schema_version: 1`, `kind: opendox-governance`, `governance: standalone \| governed`, read from `main`'s tip. Any other key, kind or value, or an unreadable file, makes the repository `unknown` (fail closed). It gets no openDox-spec schema in release 2; data-model.md and `contracts/cli-http-submit-land.md` state it. | A fourth openDox-spec schema beside R2Q22's three. | R2Q22 (a) names exactly three schemas (R2-INV-12 OQ-12-15). |
| 52 | N-2 (where the verbs live) | `submit`, `land` and `health` are contributions of openDox's DEFAULT profile (the holder note at `default_profile.py:41`), not core `cli.py` verbs. Inventory slice HA-9 (a moved openxFactory help golden) therefore shrinks to a proof that the golden does NOT move (T019, T064). | Core verbs, which move both hosts' help goldens and need a ruling (`test_extension_point_parity.py:280-286`). | R2Q3 (a) keeps both hosts' trees and help goldens unchanged. Conflicts C-15. |
| 53 | N-3 (the contract module) | ONE stdlib-only contract module, `src/opendox/health_contract.py`: U-0 (T041) writes the finding vocabulary (classes, severities, the shape with `pack_id`/`pack_version`, the id rule), and G15-A (T045) extends the SAME file with the pack protocol (declaration, patch type). The engine, the families and packs all import it; the sandbox exposes it alone. | Two modules (`health/findings.py` and `check_pack.py`), both exposed in the sandbox. | R2Q18 (a) names ONE "neutral contract module" a pack may import. Conflicts C-16. |
| 54 | N-4 (the CI owner) | openDox-code's `validate.yml` has ONE owner slice across release 2 (T010 → T017 → T051 → T080), and R2Q17 (a)'s change is its FIRST edit, on day one, before any slice adds a test. | The inventory's W3 placement (G15-I1 beside G15-C). | The sandbox tests must fail, not skip, under `CI` from their first landing, and phase 4 moves the floors too. |
| 55 | N-5 (when the two cut addenda land) | R2Q22 (a)'s batch-G style addendum and R2Q23 (a)'s batch-O style addendum at 9.5 ride in batch Q, stating the policy (one more `dox-v1.y` minor; 0.2.0, tag `v0.2.0`, on Brett's word) without a number the cut has not allocated. | A second batch at the cut, naming the bundle's number. | One Rule 6 window instead of two; batch G and batch O also stated policy before their cuts. |
| 56 | N-6 (phase overlap) | Phase 5's openDox-code slices may land once T027 has pinned phase 4's openDox-code commit, without waiting for T033. | Release 1's strict order: every phase-5 task after T033. | P4-F's tail is openXdox-code work that shares no file with them; this shortens the critical path. Risk: a P4-F repair that needs another openDox-code change then rides phase 5's pin. |
| 57 | N-7 (the composed workflow) | U-9 adds `.github/workflows/composed.yml` to openXdox-code (not a job in `validate.yml`), REQUIRED on `main` from T029's landing, pinning ONE openxFactory commit by full sha in `tests/composed_host_pin.yaml` (`schema_version`, `kind`), advanced after T030 and T064. | A job inside `validate.yml`; or a composed workflow that is not required. | ARC-Q2 (a) makes it permanent, and a non-required permanent check can rot unseen. Making it required is a required-check change, so it needs this word. |
| 58 | N-8 (feature 007's amendment) | T008 is bookkeeping: no `Arc:` trailer (R1Q20 (a)), `Lane: openxfactory-4`, landed by a merge commit (codexFactory allows merge commits only). | Carry `Arc:` (11.0's "every repository it touches"). | It amends a specification; it realizes no code. |
| 59 | N-9 (batch letters) | Release 2's amendment batches continue #1144's letters after release 1's A–P: batch Q (T005), and any later batch R, S…, so every `AMENDED — … Batch <letter>` label in #1144's `tasks.md` stays unique. | Restart at A with a release prefix. | Release 1's sixteen labels are already in #1144's text. |
| 60 | N-10 (what a run reads) | `health run` reads the committed tree of `HEAD` (a git export), for the built-in families and packs alike; a dirty working tree is noted on the run, not scanned. | Built-in families read the working tree. | Runs and baselines are per commit (R2Q12 (a)), packs already read the export (15.1b), and F14.1 commits before each run. |
| 61 | N-11 (no confirmation bypass) | `land` has no non-interactive bypass: with no `/dev/tty` it refuses, naming the missing terminal; the view's nonce is the other issuer. | A typed `--confirm <branch>` argument for scripts. | SC-007: every landing traces to a human confirmation. |
| 62 | N-12 (what else batch Q carries) | Batch Q also carries: R-1 (a)'s and H-2's notes at 12.5's falsifier (conditional on their ruling), ARC-Q2 (a)'s F9.1 amendment, ARC-5's F9.2 note, R2Q1 (a)'s non-normative reading of the map's phrase, and a non-normative note at 15.1b that a host's registered check is trusted code run in process, not a pack (R2Q16 (a)). | Separate batches for the conditional notes. | Phase 4 then needs ONE Rule 6 window for its amendments. |
| 63 | N-13 (the finding id's form) | `<pack_id>.<family>.<h16>`, `<h16>` the first 16 hex digits of SHA-256 over the pack id, family, document path and the family-supplied locator joined by NUL; a collision within a run is refused, never truncated further. The draft branch is `health-fix-<id>`. | A readable `<pack_id>:<family>:<path>:<locator>` key with a separate ref-name mapping. | R2Q10 (a) needs a key that is stable, unique and maps to a valid ref name; `:` and many path characters are not allowed in ref names. |

**Count:** 63 decisions (34 deferred, 3 interplays, 4 repair items and 3 smaller
repair questions, 6 arc items, 13 found here).

## Conflicts found: reported, NOT resolved

Each is a place where the 25 answers, the arc ruling, #1144's ratified text, the
inventories or the code disagree. None is resolved here; where a decision row
proposes a way through, it names that row.

| # | conflict | between | where a proposal sits |
|---|---|---|---|
| C-1 | `spec.md` § Assumptions (`:1193`) says the 174 reds lie "across 10 files"; R2-INV-P4F § "Errata for R2-INV-12" and R2-INV-12's erratum 2 measure **11** files, and **5** green suites (210 cases), not six. | the spec's text, lane 3's later measurement | none; `spec.md` is not this plan's to edit. T002 re-measures. |
| C-2 | R2Q12 (a) holds the baseline in the store, so a reset forgets pending disappearances; #1144's "recomputable from git" is narrowed for them. Brett took that reading on `6003486656`. | R2Q12 (a), 14.3/14.4's text | accepted by the answer; recorded at T046's tick |
| C-3 | R2Q2 (a) with R2Q3 (a) leaves ruling `5783934499`'s third bullet ("contributed by the governed host") and 12.5's "With the host's implementation registered" unrealized, and 12.4's repoint sentences (`tasks.md:2513-2519`; `design.md:476-478`, `:1059-1061`) still say `GhPullRequests` is repointed. Batch Q records a note; the ratified text stays. | the answers, a ruling's text, #1144's box | I-3 (the note); the tension remains in ratified text |
| C-4 | 15.1b says "RUN EVERY PACK IN AN OS-ENFORCED SANDBOX"; R2Q16 (a) runs a host's registered check in process. They agree only if a registered check is not a "pack". | R2Q16 (a), requirement 16 | N-12 (a non-normative note at 15.1b) |
| C-5 | Feature 007's FR-004 and SC-002 forbid moving the served checkout; 12.6a's landing merges and R2Q6 (a)'s fast-forward moves it. R2Q6 (a) names four exceptions, but until T008 lands codexFactory's spec and openDox-code's guard disagree with the answer. | feature 007 (codexFactory), R2Q6 (a), `session_git.py:93`, `:99` | scheduled: T008 → T013 |
| C-6 | F9.2's ruled note (`5859927858`; 034's T008 record) keeps F9.2 open until the arc LANDS, and #1144 cannot archive with a box open; ARC-Q3 (a) says the arc gates neither release 2's close nor #1144's archive; and OQ-038-2's proposed default says the archive "is blocked until F9.2 closes on the direction arc's landing". | ARC-Q3 (a), F9.2's note, OQ-038-2's default | ARC-5; row 34 |
| C-7 | 14.8 says exceptions follow "openxFactory's `health/dispositions.yaml`", citing `scripts/doc_health/families.py:370`. That file is the aggregation's (`opensoft/xFactory`: `gh api …/contents/health/dispositions.yaml` returns it; for `opensoft/openxFactory` it returns 404), and the quoted words sit at `families.py:371-372` at `0f2a87f6`. openDox's file of the same path but another `kind` is refused by name (row 13), so `opendox health` over the aggregation's tree refuses that file. | #1144's citation, the trees | row 13; no amendment proposed |
| C-8 | F14.1 and F15.1 select findings by literal ids (`x["id"]`, `health-fix-$f`); R2Q10 (a) makes ids pack-qualified keys. | R2Q10 (a), the falsifiers' text | batch Q (R2Q10's selection lines) |
| C-9 | 6.1 says 37 modules with `lines.py` alone generic; at `0f2a87f6` there are 38, with `lines.py` and `fs_probe.py` generic (`fs_probe.py` landed in #1201 after #1144). 6.2 cites `workbench.py:1389`; R2-INV-HEALTH places the seam at `:1542-1557`. | #1144's text, the trees | none; T052's tick records the re-measure |
| C-10 | W-1 (A) reverses ruled carve slice S7 (openDox-code `1e46971`); W-1 (A′) tests bytes the product does not serve. | W-1, the carve's ruling | row 39 |
| C-11 | R-1: no allow-list entry can reach module-level text under the ruled `_inside_the_test` rule, yet 26 nodes need it. | R2Q8 (a) ("editing none of the 16 suites" except through the allow-list), R1Q26 (a)'s rule | row 38 |
| C-12 | H-2: batch C admits "a respelling of a reference to a seam the ARC moved"; the 17 entries respell the CARVE's moves. | batch C's words, the 17 nodes | row 41 |
| C-13 | F12.2 requires `gh` absent; GitHub-hosted runners ship `gh` (inferred). | F12.2, the CI environment | row 6 |
| C-14 | F14.1 runs `git init -q` with no branch name, so on a machine whose `init.defaultBranch` is unset its repository has no `main`; under R2Q7 (a) it is `unknown` and under R2Q12 (a) it has no baseline. F14.1 asserts no class, so it still passes (inferred); AT-R2's "new first" needs `main`, so quickstart.md creates its repository with `-b main`. | F14.1's text, R2Q7 (a), R2Q12 (a) | I-2 (row 36) |
| C-15 | R2-INV-HEALTH's HA-5 adds a core `health` subcommand to `cli.py`, and its HA-9 moves openxFactory's help golden; R2Q3 (a) keeps both hosts' help goldens unchanged. | the inventory's design, R2Q3 (a) | N-2 (row 52) |
| C-16 | R2Q18 (a) lets a pack import "the engine runner's neutral contract module", one module; the inventory's outline has two (`health/findings.py` or `health_findings.py`, and `check_pack.py`). | R2Q18 (a), the inventory's outline | N-3 (row 53) |
| C-17 | The constitution's Principle IV requires the plan's documents in the README index; this PR's brief writes only the feature directory. | the constitution, the brief | Constitution Check row IV: the holder adds the links (T004) |

## Complexity Tracking

| deviation | why it is needed | the simpler alternative, and why it was rejected |
|---|---|---|
| A permanent, REQUIRED composed workflow in openXdox-code against a pinned openxFactory (N-7) | 12.5's 16 suites cannot run in a lone openXdox-code checkout (15 of them fail to collect on `doc_health`, R2-INV-P4F § "Passing composed today"), and ARC-Q2 (a) makes the composition their permanent home. | Running F12.1 only by hand at each checkpoint: nothing would stop a regression between checkpoints. |
| A pin of openxFactory inside openXdox-code's CI, while openxFactory pins the openXdox root | The composed run needs a host; the pin names a commit that already exists, so no cycle of gitlinks forms (only a CI reference). | Testing against openxFactory's moving `main`: the run would not be reproducible. |
| The `doc_health` direction arc as a second OpenSpec change inside this plan (T070–T077) | ARC-Q3 (a) rules it. | Folding it into #1144 (ARC-Q3 (c)), rejected by the ruling. |
| A new admitted-edit kind in the protected-suite oracle (R-1 (a), if ruled) | 26 nodes need module-level text that no in-test entry reaches. | Re-scoping 12.5's set (R-1 (c)) shrinks the proof. |
| Running this feature's lifecycle commands from the lane's own clone and worktree, not the git extension's sibling worktree of the shared root | Several sessions share the root checkout; each writer works in a clone of its own (plan 034 § Complexity Tracking, the same deviation). | A sibling worktree shares the root's refs, stash and branch locks with every other session. |
