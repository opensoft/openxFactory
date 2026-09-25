# Implementation Plan: openDox standalone operation (release 1)

Status: draft

**Branch**: `034-opendox-standalone-operation` | **Date**: 2026-09-24 | **Spec**: [`spec.md`](./spec.md)
**Input**: the feature specification, #1144's ratified packet
(`openspec/changes/add-neutral-product-standalone-operability/`), and
measurements of the live trees ([`research.md`](./research.md)).
**Lane**: `openxfactory-4`

## Summary

Release 1 makes openDox run, be useful, and install with nothing else present.
It is built in three phases, following #1144's RULED release map:

- **Phase 1** cuts the reach-back and makes both legs' suites green alone:
  Groups 2, 3 and 9 (except 9.5, and 9.2's ratchet, which reaches `(0, 0)` in
  phase 3), boxes 4.1, 4.1a and 4.2, 4.3's eight reaches into openxFactory,
  and 10.1. It also takes 7.3, which T005's re-measure brought in, because
  openXdox-code's whole suite needs its validator's schemas. openDox-code's
  suite runs whole. openXdox-code's runs whole less the declared `doc_health`
  exclusion (R1Q6 (d)), which stays an open extraction. R1Q24 decides where
  its files that reach openxFactory's contracts or rail run.
- **Phase 2** gives openDox its own neutral generator and its own validator:
  Groups 5 and 7 (except 7.3), and 4.3's generator and snapshot-registry
  reaches.
- **Phase 3** makes it install: Group 13, boxes 10.2, 10.3 and F10.1, Group 16,
  and the rest of 4.3, which retires `consumer_reach.py`.
- **Every phase** includes Group 11 (the trailer and the guard) and 9.5 (the
  pins).

#1144 contains contradictions, both internal and with the live code. They
were put to Brett as `R1Q1`–`R1Q22`. One answer raised `R1Q23`, and T005's
re-measure raised `R1Q24`.

- **Phase 1 is planned on answers.** Brett ruled all eleven questions it
  needed (`#656`, `5817152735`: *"(a) on all eleven, (d) on R1Q6"*). See
  § "Ruled answers". It also records the one scenario text they touch, RN-1,
  which holds phase 1's close but none of its work.
  - **Except two tasks, since T005.** T061 (7.3) came in through its
    contingency, and it waits on R1Q14 and on R1Q12 as far as (b) goes. T043
    met the two classes R1Q24 asks about. Both tasks are PROVISIONAL, as the
    later phases are. Their round, T019, encodes the answers, re-plans them
    and re-runs analyze before either starts. The rest of phase 1 is
    unaffected.
- **Phases 2 and 3 are PROVISIONAL, and they authorize no implementation.**
  They are an outline, kept for sequencing, for the release-wide box
  accounting, and for the questions that planning them raised. The phase
  questions still open (R1Q10–R1Q13, R1Q15–R1Q19 and R1Q23) belong to them,
  and they are drafted on the recommended options, each conditional step
  naming its question. R1Q12 also bears on T061 in phase 1. R1Q21, also open,
  is a process question that no release-1 task waits on.
  Each phase opens with its own round task, T009 for phase 2 and T069 for
  phase 3. No other task of the phase starts before that task has done three
  things:
  1. encoded that phase's answers;
  2. re-planned the phase, in this plan and in `tasks.md`;
  3. re-run `/speckit-analyze`, finding nothing CRITICAL.

So the constitution's workflow gate, *"material ambiguities MUST be resolved
before planning"*, holds for everything this plan authorizes. That is phase 1,
less T061 and T043 until T019 has run.

## Technical Context

**Language/Version**: Python 3.12, which is what the CI of every leg runs and
what the measurements used. JavaScript ES modules for the web bundle, with
Node harnesses in the tests.
**Primary Dependencies**: PyYAML; for the runtime extra, FastAPI, uvicorn,
psycopg 3, PyJWT and httpx; for the tests, pytest 8. The bundled PostgreSQL
packaging is decided by R1Q16.
**Storage**: the corpus is a plain git repository, read through
`LocalGitCorpus`. A bundled PostgreSQL server holds the runtime's datastore
(13.1), packaged as R1Q16 decides. No document is stored in the database
(RULING Q1).
**Testing**: each leg's own pytest suite, run whole (Group 9), less
openXdox-code's declared `doc_health` exclusion (R1Q6 (d)), and as R1Q24
decides for its files that reach openxFactory's contracts or rail; openXdox-code's
`tests/integration/` (9.3); openxFactory's `pytest-suite` at every pin advance;
#1144's falsifiers, re-run and quoted; and AT-R1. Its HTTP half is a harness in
openDox-code's own `acceptance` job, which has no database service (T095). Its
Playwright half runs on the host with `tests/smoke_signals.py`'s oracle (T096).
Neither half is a member of a leg's pytest suite: each installs the product and
drives it from outside. So neither half changes openDox-code's `testpaths`,
which T036 sets in phase 1, or F9.1.
**Target Platform**: a single-user Linux machine for the local install, and the
existing AKS hosted mode, which must be unchanged. Linux is where #1144's
falsifiers run. 13.1 checks the "no TCP port" invariant at the operating
system, in the Linux kernel's socket table, and F13.1 reads it there. macOS is
not a release-1 target, because no ratified falsifier covers it. Adding it
would need a Darwin leg for 13.1's check and F13.1, which is an amendment to
#1144 and so needs a ruling.
**Project Type**: a split product across five repositories: two code legs, two
assembly roots, and the governing aggregation child. openDox-spec becomes a
sixth only if T053 applies (R1Q11 (a) or R1Q12 (b)). Under R1Q12 (b), re-homing
the snapshot schema also touches openXdox-spec, and T003 records its base too.
**Performance Goals**: none are new. The readiness loops in F10.1 and F13.1
allow 30 seconds.
**Constraints**:
- No host-absolute path in any committed file (Principle IV).
- No raw credential anywhere.
- Nothing moves out of openxFactory (requirement 1).
- Only `doxbench_provider.py` contacts a provider.
- Local mode binds to loopback only.
**Scale/Scope**: release 1 has 69 of #1144's 124 boxes (tasks.md § "Box
accounting"). About 12 carved openDox-code files are edited (research R12), and
27 deferred reaches plus 65 `consumer_reach` uses are routed (research R5, R6).

## Constitution Check

*GATE: checked before planning, and re-checked after each round of answers.
Round 1a was #1155. This revision is T005's re-plan, before T006's analyze.*

| principle | status | how this feature meets it |
|---|---|---|
| I. Contract-first, domain-neutral core | PASS | openxFactory gains only host wiring, pin pairs, notes, and the named composition tests that R1Q2 (a) admits (11.1). No domain vocabulary enters openDox; the default profile's words are `NEUTRAL_DISPLAY`'s (requirement 3, third scenario). |
| II. OpenSpec before implementation | PASS | Everything here realizes the RATIFIED #1144 (`5815412869`). An answer that amends a #1144 falsifier or task line is recorded there on Brett's word (T007). One that would change requirement or scenario text goes back to him first (RN-1). Speckit owns the tasks; #1144's `tasks.md` is ticked, and never duplicated (T097). |
| III. Document lifecycle | PASS | Every feature file carries a controlled `Status: draft` header, in the form feature 029's files use. #1144 is `Status: ratified`, with its record landed as #1151 → `cd494e4c`. |
| IV. Schema and artifact discipline | PASS | No committed file names a host path: every command resolves its scratch space with `W=$(mktemp -d)`. No credential is stored: 16.3 refuses raw keys. **The README document index** links all seven of this feature's documents, and its evidence records, in one entry in its Documentation section, beside the openDox carve documents. The entry sits outside the OpenSpec Records block, so it needs no Rule 6 window. None of the 31 earlier feature directories under `specs/` on `main` (`138a4722`) is indexed there, so this entry is the first of its kind. |
| V. Validation gates | PASS for this PR, against `main`'s recorded baseline | This PR touches no `openspec/` path: `git diff --stat main -- openspec/` is empty. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` gives `111 passed, 1 failed (112 items)` at this branch's head, run on 2026-09-25, and so `main` at `c415c3d1` gives the same. #1155 measured `110 passed, 1 failed` on 2026-09-24. The one item gained since is `admit-code-leg-under-pinned-root`, filed on `main` as #1156 (`daca0b89`). research.md's `dd2466ad` is a different thing: the baseline the plan's measurements were taken at, not this PR's gate. The one failure is `add-chain-attestation`'s "omits scenario(s)" finding. It is an accepted disposition in `contracts/openspec-cli-pin.yaml` (`ratified_by: 'Brett Heap, 2026-09-05, "take exit 2"'`), and it retires when that change archives. This PR cannot move it. The gate the repository enforces, `scripts/validate-openspec-cli-pin.py --all` (the `openspec-cli-pin` check), exits 0 with `0 UNDISPOSITIONED failures`. No other `scripts/validate-*.py` reads `specs/`, and every check on the PR is green. Implementation evidence will be falsifier output, quoted. |
| VI. Versioned releases | WATCH | 9.5 says *"none cuts a contract bundle"*. R1Q11 (a) or R1Q12 (b) would add an openDox-spec schema (T053), which is probably a `dox-v1.1` minor at the openDox root; if so, that release follows the root's own four-value rule. |
| VII. Fail-closed authority | PASS | Every seam refuses naming itself when nothing is registered (4.2's discipline). The hosted mode refuses without an issuer. An unknown dialect is refused. |
| Workflow: *"material ambiguities MUST be resolved before planning"* | **PASS for phase 1 less T061 and T043; those two, and phases 2–3, PROVISIONAL** | This plan authorizes only phase 1 for implementation. Every material ambiguity in it is resolved (`5817152735`), except the three that T005's re-measure put on its openXdox-code tail: R1Q14 and R1Q12's part (T061) and R1Q24 (T043). Those two tasks are provisional, as phases 2–3 are, and authorize nothing yet. Each provisional part is planned for implementation only by its round task (T019, T009, T069), which encodes its answers, re-plans it and re-runs analyze. A task blocked by an open R1Q never starts (FR-012). See Complexity Tracking. |

## Project Structure

### Documentation (this feature)

```text
specs/034-opendox-standalone-operation/
├── spec.md                 # user stories, FRs mapped to #1144, AT-R1
├── plan.md                 # this file
├── research.md             # every measurement, with its command
├── clarify-questions.md    # R1Q1–R1Q24: 11 answered (5817152735), 13 open
├── quickstart.md           # AT-R1's procedure
├── tasks.md                # 88 tasks, T001–T098 (some ids unused), box accounting (69 of 124)
├── checklists/
│   └── requirements.md     # the spec-quality checklist
└── evidence/               # bookkeeping records, with no trailer (R1Q20 (a))
    ├── arc-base.md         # T003: ARC_BASE for all seven repositories; PACKET_MERGE
    ├── remeasure-2026-09-25.md   # T005: R1–R15 again, and openXdox-code's whole suite
    └── analyze-round-1a.md # T006: the prerequisites check and analyze's verdict
```

Later tasks add their own records to `evidence/`: T018, T065 and T098 add the
interim F11.1 runs, and T096 adds AT-R1.

### Source code: the five repositories release 1 lands in (six if T053 applies, seven under R1Q12 (b))

```text
opensoft/openDox-code            [oDc]   the product; most of the work
  src/route_extension.py                  the handler-contribution facet, R1Q1 (a) (T010)
  src/opendox/serve.py                    2.1/2.2, 4.3, 13.4a — ONE WRITER AT A TIME
  src/opendox/cli.py                      3.2, 4.1a, 4.3, 10.1 — ONE WRITER AT A TIME
  src/opendox/domain_profile.py, profile_proxy.py, <default profile module>   Group 3
  src/opendox/corpus_adapter.py, authoring.py                                  4.1, 4.1a, 4.2
  src/opendox/workbench.py, serve_wire.py, doxbench_packet.py                  4.3 (phase 1)
  src/opendox/<generator seam + neutral projection modules>                    5.1–5.5
  src/opendox/<validator + packaged schemas>                                   7.1–7.2
  src/opendox/serve_workbench.py, serve_project.py, branch_session.py          4.3 (phases 2–3)
  src/opendox/consumer_reach.py                                                retired (4.3)
  src/opendox/runtime/config.py, runtime/cli.py, <bundle module>               Group 13
  src/opendox/doxbench_binding.py, doxbench_provider.py, doxbench_install.py   Group 16
  src/opendox/web/views/doxbench-chat.js, lens.js                              16.4, R1Q19
  tests/fixtures/plain-documents/, tests/fixtures/malformed/                   5.0, 7.0
  tests/test_imports_standalone.py, test_authoring_seam.py,
    test_profile_registration.py, test_chat_model_configuration.py             named by the falsifiers
  acceptance/at_r1_http.py                                                     T095: a harness in its own job, no database
  conftest.py, pyproject.toml, .github/workflows/validate.yml, README.md       9.1, 10.1, 2.6
opensoft/openXdox-code           [oXc]   the consumer
  pyproject.toml (opendox pin), tests/test_dependency_direction.py (ratchet)   9.5, 4.3
  src/openxdox/<contributions through the seams>                               5.4a, 4.3
  <declared doc_health exclusion file>, conftest.py                            9.2, R1Q6 (d)
  src/openxdox/snapshot.py, scripts/validate-ideation-dashboard-contracts.py   7.3 (after C3)
  tests/integration/                                                           9.3
  .github/workflows/validate.yml                                               9.2
opensoft/openDox                 [oD]    assembly root: code pin; README (10.3)
opensoft/openXdox                [oX]    assembly root: code pin; contracts/opendox-pin.yaml
opensoft/openxFactory            [oxF]   host wiring + pin pairs + notes (11.1), and this feature
  scripts/opendox_host.py, scripts/profile_openxfactory.py, tests/domain_profile/
  tests/ideation-dashboard/test_extension_point_parity.py (a named composition test, R1Q2 (a))
  tests/ideation-dashboard/test_serve_column_split.py     (a named composition test, R1Q2 (a))
  openDox + contracts/opendox-pin.yaml; openXdox + contracts/openxdox-pin.yaml
  docs/opendox-carve-manifest.yaml (edits[].note only)
opensoft/openDox-spec            [oDs]   ONLY if R1Q11 (a) or R1Q12 (b): the neutral snapshot schema
opensoft/openXdox-spec           [oXs]   ONLY under R1Q12 (b): retires its copy of the re-homed snapshot schemas
```

**Structure Decision.** ONE Speckit feature for release 1, with release 2 as
its own feature later (R1Q21, recommended (a)). The feature lives in
openxFactory, beside its governing change. Implementation happens in each
repository's own clone or worktree, on a branch named for the slice, and each
slice lands through that repository's own pull request. None of it happens in
this worktree, which holds the plan only.

## Phases, and where every release-1 box closes

| phase | boxes that CLOSE in it | exit (all quoted in the phase checkpoint task) |
|---|---|---|
| 0 | 3.0 (ratification) | answers applied; analyze clean |
| 1 | 2.1, 2.1a, 2.2, 2.3, 2.4, 2.5, 2.6, F2.1; 3.1, 3.2, 3.3 (first run; T065 and T098 repeat it before T097 ticks it), F3.1; 4.1, 4.1a, 4.2; 7.3, F7.1 (T061, moved in by T005); 9.1, 9.2a, 9.3, 9.4, F9.1, F9.2; 10.1 | F2.1, F3.1, F7.1, F9.1 (both legs), F9.2, `opendox --help` |
| 2 | 5.0, 5.1, 5.2, 5.3, 5.3a, F5.1, 5.4, 5.4a, F5.2, 5.5, F5.3; 7.0, 7.1, 7.1a, 7.1b, 7.2, F7.2 | F5.1, F5.2, F5.3, F7.2; standalone `generate-and-open` serves |
| 3 | 4.3, F4.1; 9.2 (its whole-suite check lands in phase 1, and its ratchet reaches `(0, 0)` at T086); 10.2, 10.2a, 10.3, F10.1; 13.1–13.6, 13.4a, F13.1; 16.1–16.6, F16.1 | F4.1, F10.1, F13.1, F16.1; AT-R1 follows the checkpoint (T095, T096) |
| every phase, ticked at ARC close | 9.5, 11.0, 11.1, F11.1 | interim F11.1 after each phase |
| already `[x]` | 5.6 | — |

**Phase-1 limit (measured, research R7).** A standalone `build_server` is
refused at `serve.py:1647` until the snapshot-source default lands in phase 2.
If that line were cleared, `serve.py:1687` (`_checkout_real`, which reaches
`openxdox.corpus_root`) would fail next. Phase 1's server-side proofs therefore
inject a snapshot source, and a standalone server START is phase 2's exit. By
the release map's own rule (*"no later than the phase whose surface calls
it"*), `serve.py:629` is routed in phase 2 along with the snapshot source.

## Dependency graph

```text
T001–T008 (holder: claims, ARC_BASE, round 1a, re-measure, analyze, #1144 amendments, the direction arc); T019 (the openXdox-code tail's round)
                              │
 PHASE 1  [oDc]  A: T010→T011→T012 (serve.py)     B: T015→T016 (profile)
                 C: T020→T021→T022 (adapter)      D: T026→T025, T027 (seams; T025 also after T020)
                 E: T030 (the import test; lands with T011)
                        └───────── join ─────────┘
                 T032 (2.3 sweep) → T034 (repair 9 files) → T035 → T036 (+ T031) → T037
                 T038 (10.1, Q-R4)  after B and T022
          [oD]   T039 root pin (T090 steps 1–2)  after T022, T032, T037, T038
          [oXc]  T040 (pin, residue) → T041 (declared exclusion) → T042 (9.3) → T043 → T044
                 T040 → T061 (7.3, moved in by T005) → T043; T019 before T061 and T043
          [oX]→[oxF]  T047 consumer pins (steps 5–6) after T039, T044, T007 batch A; carries T045 + T046
          T047 → T017 (3.3) and T018 (interim F11.1) → checkpoint T049 (after T007 batches A, B, RN-1, and T019 through T043);  holder T048
 PHASE 2 (PROVISIONAL)  T009 (phase 2's round: answers, re-plan, analyze) first
          [oDc]  T050 → T051  ∥  T052  ∥  T057   (∥ T053 [oDs] if R1Q11 (a) or R1Q12 (b))
                 T054 (projection) → T055 (sources, 4.3 part) → T056 → T058 (validator)
          [oD]   T062 root pin  after T054–T058
          [oXc]  T059 (5.4a) after T052, T055, T062, T007 batch C;  T060 (5.3a re-run) after T054
          [oX]→[oxF]  T064 consumer pins → T065 (interim F11.1) → checkpoint T063 (after T007 batch C)
 PHASE 3 (PROVISIONAL)  T069 (phase 3's round: answers, re-plan, analyze) first
          [oDc]  G13: T071→T070→T072→T073→T074      G16: T078→T079→T080;  T085 → T081
                 4.3 end: T084 (after T073)          T075 → T077;  T082, T083, T088
          [oD]   T087 root pin → T076 (README), once the command has its final form (R1Q15)
          [oXc]  T086 (columns, ratchet (0,0)) at the pin T087 carries
          [oX]→[oxF]  T094 consumer pins + host wiring → T098 (interim F11.1) → checkpoint T089 (after T076)
 ACCEPTANCE      T095 (HTTP, CI; after T089 and T076)  →  T096 (browser)  →  T097 (bookkeeping, Rule 6)
 EVERY PHASE     T090 pins · T091 trailer · T092 notes · T093 interim F11.1 (run as T018, T065, T098)
```

## Parallel slices, and the files only one writer may touch at a time

Writers run in parallel when they share no file. The surfaces below are
SINGLE-WRITER: at most one open slice may edit each, and a slice that needs one
rebases onto the previous slice's landing before it opens. The phase-2 and
phase-3 entries are provisional: T009 and T069 re-derive them from the file
lists of the re-planned tasks.

| single-writer file | slices, in order |
|---|---|
| `src/opendox/serve.py` | T010 (`build_server`'s bases) → T011 → T012 → (T016, T022 one-line entry-point calls) → T055 → T073 → T084 |
| `src/opendox/cli.py` | T016/T022 entry-point registration → T038 → T055 → T084 |
| `src/opendox/workbench.py` | T026 → T025 (both in P1-E) |
| openDox-code `pyproject.toml` | T038 (`[project.scripts]`) → T036 (`testpaths`, and the `test` extra); T069 re-derives phase 3's packaging edits (R1Q16) |
| openDox-code `tests/test_authoring_seam.py` | T020 → T022 |
| openXdox-code `tests/test_dependency_direction.py` (the ratchet) | T040 (it moves the pin and leaves the ratchet unchanged) → T059 → T086 |
| openXdox-code `pyproject.toml` | T040 (the `opendox @` pin and `rfc3339-validator`) → T061 (the validator's package data) |
| openDox root `code` gitlink, `contracts/code-pin.yaml`, workflow `@sha` | one commit per phase (T039, T062, T087), each after that phase's last openDox-code landing |
| openxFactory pin pairs | one openxFactory PR per phase (T047, T064, T094), each also carrying that phase's host wiring |

- **Phase 1 parallel lanes**: A (serve seam), B (profile), C (adapter), D
  (workbench, serve_wire and doxbench_packet seams) and E (the import test,
  which lands with T011; the README fix, T031, lands with T036). R1Q6 is
  answered (d), so openXdox-code's T041 waits only on T006 and T040. T061
  (7.3) runs beside T041 and T042 once T019 has its answers, and T043 waits
  for all three.
- **Phase 2 parallel lanes**: the fixtures (T050, then T051), the generator seam
  (T052), the validator input set (T057) and the neutral schema (T053), if
  R1Q11 (a) or R1Q12 (b) is chosen.
- **Phase 3 parallel lanes**: Group 13 (T070–T074), the Group 16 binding
  (T078–T080), the doxBench defaults and then the no-model state (T085 →
  T081), the retirement of the late reaches (T084, after T073; then T086), and
  entry-point serving (T075).

## Pins and landing order (9.5): one openDox-code commit per phase, everywhere

Each phase advances the pins in this order. Every step is its owner's ordinary
pin-sync act, and each step's PR is opened only after the step before it has
landed. Steps 1–2 are T039, T062 and T087; steps 5–6 are T047, T064 and T094.
Each of these is a separate task from its phase's openXdox-code work, so no
task waits on a later step of itself:

1. **openDox-code** lands the phase's slices.
2. **openDox root**: ONE commit moves the `code` gitlink,
   `contracts/code-pin.yaml` (its `commit:` and `digests.tree_sha256`), and
   every `.github/workflows/*.yml` `@<sha>` that names the leg, if any does;
   none does at `36ded1cd`. `make pins` checks this (AGENTS-shape: "Advancing a
   leg is ONE commit here").
3. **openXdox-code**: `pyproject.toml`'s `opendox @ …@<sha>` moves to THE SAME
   openDox-code commit, and the `OPENDOX_BACK_IMPORTS` ratchet is lowered for
   every reach that commit closed (9.2).
4. **openXdox-code** lands its phase's contributions.
5. **openXdox root**: the `code` gitlink and `contracts/code-pin.yaml` move, in
   one commit, to step 4's commit, and `contracts/opendox-pin.yaml` moves to
   step 2's root commit.
6. **openxFactory**, in ONE PR: the `openDox` gitlink and
   `contracts/opendox-pin.yaml` in one commit, and the `openXdox` gitlink and
   `contracts/openxdox-pin.yaml` in one commit. `verify-opendox-pin.py` holds
   openxFactory's openDox pin EQUAL to openXdox's derived one. The same PR
   carries the phase's host wiring (step 7).
7. **openxFactory host wiring** (the phase's T045/T046-class tasks). It lands in
   the same PR as step 6, so `main` never holds a pin without its wiring.

**One openDox-code commit per phase, in all three places.** The openDox root's
code pin, openXdox-code's `pyproject.toml` pin, and (through the roots)
openxFactory's view all name one commit. They disagree today (`d816cf06`
against `5c137a90`, research R13). Step 3 ends that.

**The runbook C4 is writing** (lane 4's openXdox-pin resync runbook) is the
procedure for steps 5 and 6 once it lands. Until then, #1146 and #1148 are the
shape to follow.

**Merge method.** Every one of these repositories allows merge, squash and
rebase, and so does openDox-spec; the product repositories each require only
`validate` on `main`. Land by **squash or merge commit, never rebase**. That
way each landing is ONE first-parent commit, which is what 5.4a's, 12.5's and
11.1's guards diff against its parent. A merge landing writes the `Arc:`
trailer into the merge message (11.0).

## The trailer, the guard and Rule 6

- **Realization landings** carry `Arc: neutral-product-standalone-operability`
  in every repository, alongside `Lane: openxfactory-4`. Reviews check both
  (11.0).
- **Bookkeeping** carries NO `Arc:` trailer: this feature's files, #1144's
  ticks, evidence notes and amendments (T007), and interim guard output. That
  is R1Q20 (a), ruled in `5817152735`, and this planning PR follows it.
- **The manifest.** An openxFactory arc landing may only add or extend an
  existing `edits[].note` (11.1). The manifest records the carve as it arrived,
  so no arc edit to a carved file needs a declared-edit act first (R1Q22 (a),
  ruled).
- **The named composition tests.** R1Q2 (a) admits an arc landing's edit to a
  NAMED openxFactory composition test. That covers
  `tests/ideation-dashboard/test_extension_point_parity.py` and
  `tests/ideation-dashboard/test_serve_column_split.py` first, and any path
  T034, T035 or T047's `pytest-suite` run finds once a T007 batch names it.
  F11.1 checks this after T007 batch A has widened it.
- **Rule 6.** Realization PRs never touch `openspec/changes/`. Only T007's
  amendments (batch D among them, if RN-1 is ruled (a)), T008's proposal if it
  files one, and T097's ticks do, and each lands under a `LANDING` / `LANDED`
  window. Closing keywords never appear in a commit message or PR body.

## Ruled answers (`5817152735`)

Brett Heap answered the eleven phase-1 questions on `#656`, comment
`5817152735` (2026-09-24T15:31:46Z), verbatim: *"(a) on all eleven, (d) on
R1Q6"*. Phase 1 is therefore planned on its answers, not on recommendations.

| question | answer | what it fixes in this plan |
|---|---|---|
| R1Q22 | (a) | No declared-edit act precedes an arc edit to a carved file. T038 corrects `runtime/cli.py:17-19`, which said otherwise. |
| R1Q1 | (a) | The handler-contribution facet (T010). T011 and T045 use it now, and T084 and T086 in phase 3. |
| R1Q2 | (a) | 11.1's surfaces gain named composition tests, starting with the parity test and the column-split test (T045, T094). T007 batch A widens F11.1. |
| R1Q3 | (a), (i), (ii) | Both defaults are entry-point registrations (T016, T022). T007 batch A amends F3.1 line 2 and 3.2. (ii) touches a scenario's text: RN-1. |
| R1Q4 | (a) | The default contributes openDox's own verbs (T015), and the host asserts its own registration (T046). |
| R1Q5 | (a) | `RuntimeSubcommand` arrives through `SUBCOMMAND_EXTENSIONS`, with the `opendox-runtime` alias (T038). The 31-entry goldens stand (T042). |
| R1Q6 | (d) | openXdox-code's declared `doc_health` exclusion (T041, T043, T044). T007 batch B amends F9.1. T008 raises the direction arc. The answer raises R1Q23. |
| R1Q7 | (a) | The reviewed respelling allow-list (T007 batch C; T043, T059, T086). |
| R1Q8 | (a) | `tests_runtime/` is part of the whole suite, with a PostgreSQL service in the required job (T036). F9.1 is unchanged. |
| R1Q9 | (a) | `session_documents` resolves through `list_documents` in phase 1 (T025, T046). |
| R1Q20 | (a) | Bookkeeping carries no trailer (T091). T007 batch A adds 11.0's addendum. |

**Where the amendments go.** Brett's comment says: *"Where an answer amends a
ratified falsifier (F3.1, F9.1) or widens the 11.1 guard, that change rides in
the realization as the answer records it."*

- The planning PR (#1155) edits no file of #1144.
- T007 records each amendment in #1144's `tasks.md`, in three bookkeeping
  batches (A, B and C).
- Each batch lands under a Rule 6 window, with no `Arc:` trailer, before the
  checkpoint that runs the amended falsifier.
- `tasks.md` § "Ruled amendments" lists every amended line, the text it takes,
  and the task that carries it out.

### Ruling needed

Brett's comment keeps the post-word rule: *"any change to requirement or
scenario TEXT still comes back to Brett as RULING NEEDED."* One answer implies
such a change.

**RN-1 — requirement 3's fourth scenario, against R1Q3 (ii).** The scenario
reads: *"WHEN a host, consumer layer or domain descendant registers a profile —
THEN the registered profile replaces the default for that process, so the
default is a fallback and never a privileged path."* As ruled, R1Q3 (ii) lets
a host registration replace the default only until a parser or server is
built from it. A later one is refused as `AlreadyRegistered`, which is RULED
ASK-4 Q5's reason. For that later registration, the scenario's THEN does not
hold as written.

- (a) Amend the scenario's WHEN to *"…registers a profile before the
  product's parser or server has been built from the default in that
  process"*. Add a scenario for the refusal after a build. **Recommended.**
- (b) Keep the scenario as written, and let a registration after a build
  replace the default too. The parser already built would then keep the old
  profile, which is the hazard ASK-4 Q5 refused.
- (c) Read a refused registration as never having happened, so the scenario
  never fires. No text changes, but the default is then privileged after a
  build, against the scenario's own words.

RN-1 holds phase 1's CLOSE, not its work. T016 lands on the ruled (ii),
because after a build it leaves today's `AlreadyRegistered` refusal in place,
and that refusal is (ii). The checkpoint T049 does not report requirement 3 as
realized until RN-1 is ruled and T016 matches the ruling. Only (b) would make
T016 do more.

**Not a ruling: a watch item for the archive.** Under R1Q6 (d), requirement 9
is met for openXdox-code by its first scenario: a declared exclusion, with its
count and its reason. That exclusion stays an OPEN EXTRACTION until T008's
direction arc lands. The archive act must report it as open, and must not
read it as closed.

**Raised by an answer: R1Q23.** R1Q6 (d) leaves four of 5.4a's generator
suites needing `doc_health`. F5.2 closes in phase 2, and it installs nothing
that provides `doc_health`. R1Q23 asks how F5.2 runs. It blocks T059 and T063,
not phase 1. At openXdox-code `e28930bf` the glob selects seven suites, and the
seventh passes (T005).

**Raised by the re-measure: R1Q24, and T061 in phase 1.** T005 ran
openXdox-code's whole suite for the first time
([`evidence/remeasure-2026-09-25.md`](./evidence/remeasure-2026-09-25.md)).

- Most of what it found is carve residue, which T040 now clears.
- Two classes reach openxFactory without going through `doc_health`, so
  R1Q6 (d)'s exclusion cannot hold them. They are the status-exemption rail
  (three files) and the contract family (four files). R1Q24 asks where they
  run. It blocks T043.
- `tests/test_snapshot.py` still fails two cases on its schemas, so T061's
  contingency applies. T061 is in phase 1 and blocked by R1Q14. It is blocked
  by R1Q12 as well, because (b) would re-home two of the three schemas that
  T061 packages.

All three questions go through T019. Phase 1 therefore closes only once
Brett has answered them, as well as RN-1. Only T061, T043 and the tasks after
them wait for these answers.

## In-flight overlaps (lane 4's own acts, all landed by 2026-09-24T18:34Z)

| act | touches | release-1 overlap | rule |
|---|---|---|---|
| 1.8 ratification record | #1144's three lifecycle docs and `.openspec.yaml` | LANDED as #1151 → `cd494e4c`, ticking 1.8 and 3.0 | T007's amendments build on it |
| C1 (`5815604830`) | an openxFactory count fix | none; LANDED as #1152 → `9afea8d7` | — |
| C3 (`5815613524`) | openXdox-code `src/openxdox/snapshot.py` and the validator script; openxFactory manifest rows; the openXdox pin | 7.3's files (T061); 9.5's openXdox pin pair (T047). PR 1, the manifest window, LANDED as #1153 → `1d14fee6`; PR 2 LANDED as openXdox-code#28 → `e28930bf`; the openxFactory openXdox pin bump LANDED as #1157 → `1edbb3dd` | T061 revisits PR 2's confinement per R1Q14. T005 found `tests/test_snapshot.py` still red after PR 2, so T061 is in phase 1. T043 and T047 start from these landings |
| C4 (`5815620605`) | the openXdox-pin resync runbook | 9.5 steps 5 and 6; LANDED as #1154 → `138a4722` | T090 follows it |

## Persisted tools

The four measurement scripts in [`research.md`](./research.md) § Appendix are
also persisted to the lane's workspace repository (`opensoft/brett-wip`) under
the lane's tool directory, so that T005's re-measure does not depend on any
session's scratch space. That persistence is recorded in the PR body.

## Complexity Tracking

| deviation | why it is needed | the simpler alternative, and why it was rejected |
|---|---|---|
| Keeping phases 2–3 in this feature as a PROVISIONAL outline while their questions are open. The constitution's workflow asks that material ambiguities be *"resolved before planning"* | The box accounting, the pin chain and the single-writer order span all three phases, and planning them is what found the questions. The outline authorizes no implementation, so the gate holds for everything the plan authorizes (phase 1, less the two tasks in the next row). | Dropping phases 2–3 from this feature now would lose the release-wide accounting. They can still move to their own feature when they are re-planned, which is R1Q21's pattern. |
| Keeping T061 and T043 in phase 1 as PROVISIONAL tasks while R1Q14, R1Q24 and R1Q12's part are open (T005) | T061 is where its own contingency sends it: phase 1's openXdox-code suite cannot go green without 7.3's schemas. T043 is the task that makes that suite a required check. Both stay in place with their dependencies. Their round, T019, re-plans and re-analyzes them before either starts, as T009 and T069 do for their phases. | Holding all of phase 1 until the answers arrive would stop the openDox-code slices, which no open question touches. Moving 7.3 and 9.2 out of phase 1 would leave phase 1's checkpoint unable to run F9.1 for openXdox-code. |
| A handler-contribution mechanism (R1Q1 (a), ruled), which is new mechanism against design.md § D4 | The existing seam provably cannot carry a mixin's methods (`route_extension.py:60`). T007 batch A records D4's addendum. | Keeping a forwarding stand-in (R1Q1 (c)) is the pattern 4.3 retires. |
| A second pin chain step inside each phase (openXdox-code's pyproject pin brought to the root's commit) | Without it, openxFactory and openXdox-code test different openDox bytes (research R13). | Leaving the pins divergent means 9.3's integration run measures a composition nobody ships. |
