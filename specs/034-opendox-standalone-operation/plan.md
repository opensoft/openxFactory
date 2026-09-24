# Implementation Plan: openDox standalone operation (release 1)

**Branch**: `034-opendox-standalone-operation` | **Date**: 2026-09-24 | **Spec**: [`spec.md`](./spec.md)
**Input**: the feature specification, #1144's ratified packet
(`openspec/changes/add-neutral-product-standalone-operability/`), and
measurements of the live trees ([`research.md`](./research.md)).
**Lane**: `openxfactory-4`

## Summary

Release 1 makes openDox run, be useful, and install with nothing else present.
It is built in three phases, following #1144's RULED release map:

- **Phase 1** cuts the reach-back and makes both legs' suites green alone:
  Groups 2, 3 and 9 (except 9.5), boxes 4.1, 4.1a and 4.2, 4.3's eight reaches
  into openxFactory, and 10.1.
- **Phase 2** gives openDox its own neutral generator and its own validator:
  Groups 5 and 7, and 4.3's generator and snapshot-registry reaches.
- **Phase 3** makes it install: Group 13, boxes 10.2, 10.3 and F10.1, Group 16,
  and the rest of 4.3, which retires `consumer_reach.py`.
- **Every phase** includes Group 11 (the trailer and the guard) and 9.5 (the
  pins).

The plan is CONDITIONAL. #1144 contains contradictions, both internal and with
the live code, and they are put to Brett as `R1Q1`–`R1Q22`. Each is planned
here on its recommended option, and each conditional step names its question.
T004 re-plans on the answers, and T006 (`/speckit-analyze`) gates
implementation.

## Technical Context

**Language/Version**: Python 3.12, which is what the CI of every leg runs and
what the measurements used. JavaScript ES modules for the web bundle, with
Node harnesses in the tests.
**Primary Dependencies**: PyYAML; for the runtime extra, FastAPI, uvicorn,
psycopg 3, PyJWT and httpx; for the tests, pytest 8. The bundled PostgreSQL
packaging is decided by R1Q16.
**Storage**: the corpus is a plain git repository, read through
`LocalGitCorpus`. A bundled PostgreSQL 16 holds the runtime's datastore
(13.1). No document is stored in the database (RULING Q1).
**Testing**: each leg's own pytest suite, run whole (Group 9); openXdox-code's
`tests/integration/` (9.3); openxFactory's `pytest-suite` at every pin advance;
#1144's falsifiers, re-run and quoted; and AT-R1's Playwright half, run on the
host with `tests/smoke_signals.py`'s oracle.
**Target Platform**: a single-user Linux or macOS machine for the local install,
and the existing AKS hosted mode, which must be unchanged.
**Project Type**: a split product across five repositories: two code legs, two
assembly roots, and the governing aggregation child.
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

*GATE: checked before planning, and re-checked after T004 applies the answers.*

| principle | status | how this feature meets it |
|---|---|---|
| I. Contract-first, domain-neutral core | PASS | openxFactory gains only host wiring, pin pairs and notes (11.1). No domain vocabulary enters openDox; the default profile's words are `NEUTRAL_DISPLAY`'s (requirement 3, third scenario). |
| II. OpenSpec before implementation | PASS | Everything here realizes the RATIFIED #1144 (`5815412869`). Any answer that changes #1144's text lands there first, on Brett's word (T004). Speckit owns the tasks; #1144's `tasks.md` is ticked, and never duplicated (T097). |
| III. Document lifecycle | PASS | The feature files carry Speckit's own `Status: Draft`. #1144 is `Status: ratified`, with its record landed as #1151 → `cd494e4c`. |
| IV. Schema and artifact discipline | PASS | No committed file names a host path: every command resolves its scratch space with `W=$(mktemp -d)`. No credential is stored: 16.3 refuses raw keys. |
| V. Validation gates | PASS for this PR | `openspec validate --all --strict` is run from the worktree root before the push (this feature adds no OpenSpec change). Implementation evidence is falsifier output, quoted. |
| VI. Versioned releases | WATCH | 9.5 says *"none cuts a contract bundle"*. R1Q11 (a) would add an openDox-spec schema, which is probably a `dox-v1.1` minor at the openDox root; if so, that release follows the root's own four-value rule. |
| VII. Fail-closed authority | PASS | Every seam refuses naming itself when nothing is registered (4.2's discipline). The hosted mode refuses without an issuer. An unknown dialect is refused. |
| Workflow: *"material ambiguities MUST be resolved before planning"* | **DEVIATION, recorded** | The brief asks for the plan now and forbids resolving ambiguities by assumption. So the plan is conditional: tasks blocked by an open R1Q may not start, T004 re-plans on the answers, and T006 gates implementation. See Complexity Tracking. |

## Project Structure

### Documentation (this feature)

```text
specs/034-opendox-standalone-operation/
├── spec.md                 # user stories, FRs mapped to #1144, AT-R1
├── plan.md                 # this file
├── research.md             # every measurement, with its command
├── clarify-questions.md    # R1Q1–R1Q22, awaiting Brett Heap
├── quickstart.md           # AT-R1's procedure
├── tasks.md                # T001–T097, box accounting (69 of 124)
└── checklists/
    └── requirements.md     # the spec-quality checklist
```

`evidence/` is created by the first task that records evidence (T003). It is
not created empty.

### Source code: the five repositories release 1 lands in

```text
opensoft/openDox-code            [oDc]   the product; most of the work
  src/route_extension.py                  R1Q1's handler contribution (T010)
  src/opendox/serve.py                    2.1/2.2, 4.3, 13.4a — ONE WRITER AT A TIME
  src/opendox/cli.py                      3.2, 4.1a, 4.3 — ONE WRITER AT A TIME
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
    test_profile_registration.py, test_chat_model_configuration.py,
    test_release1_acceptance.py                                                named by the falsifiers
  conftest.py, pyproject.toml, .github/workflows/validate.yml, README.md       9.1, 10.1, 2.6
opensoft/openXdox-code           [oXc]   the consumer
  pyproject.toml (opendox pin), tests/test_dependency_direction.py (ratchet)   9.5, 4.3
  src/openxdox/<contributions through the seams>                               5.4a, 4.3
  src/openxdox/snapshot.py, scripts/validate-ideation-dashboard-contracts.py   7.3 (after C3)
  tests/integration/                                                           9.3
  .github/workflows/validate.yml                                               9.2
opensoft/openDox                 [oD]    assembly root: code pin; README (10.3)
opensoft/openXdox                [oX]    assembly root: code pin; contracts/opendox-pin.yaml
opensoft/openxFactory            [oxF]   host wiring + pin pairs + notes (11.1), and this feature
  scripts/opendox_host.py, scripts/profile_openxfactory.py, tests/domain_profile/
  openDox + contracts/opendox-pin.yaml; openXdox + contracts/openxdox-pin.yaml
  docs/opendox-carve-manifest.yaml (edits[].note only)
opensoft/openDox-spec            [oDs]   ONLY if R1Q11 (a) or R1Q12 (b): the neutral snapshot schema
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
| 1 | 2.1, 2.1a, 2.2, 2.3, 2.4, 2.5, 2.6, F2.1; 3.1, 3.2, 3.3, F3.1; 4.1, 4.1a, 4.2; 9.1, 9.2, 9.2a, 9.3, 9.4, F9.1, F9.2; 10.1 | F2.1, F3.1, F9.1 (both legs), F9.2, `opendox --help` |
| 2 | 5.0, 5.1, 5.2, 5.3, 5.3a, F5.1, 5.4, 5.4a, F5.2, 5.5, F5.3; 7.0, 7.1, 7.1a, 7.1b, 7.2, 7.3, F7.1, F7.2 | F5.1, F5.2, F5.3, F7.1, F7.2; standalone `generate-and-open` serves |
| 3 | 4.3, F4.1; 10.2, 10.2a, 10.3, F10.1; 13.1–13.6, 13.4a, F13.1; 16.1–16.6, F16.1 | F4.1, F10.1, F13.1, F16.1, AT-R1 |
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
T001–T006 (holder; answers) ──┬──────────────────────────────────────────────┐
                              │                                              │
 PHASE 1  [oDc]  A: T010→T011→T012 (serve.py)     B: T015→T016 (profile)      │
                 C: T020→T021→T022 (adapter)      D: T025, T026, T027 (seams) │
                 E: T030, T031 (import test, README)                         │
                        └───────── join ─────────┘                           │
                 T032 (2.3 sweep) → T034 (repair 9 files) → T035 → T036 → T037
                 T038 (10.1, Q-R4)  after B
          [oXc]  T040 (pin, residue) → T041 (doc_health, R1Q6) → T042 (9.3) → T043 → T044
          [oD]→[oX]→[oxF]  T047 = T090 pin advance, carrying T045 + T046 host wiring
          checkpoint T049;  holder T048 (F4 re-measure)
 PHASE 2  [oDc]  T050 ∥ T051 ∥ T052 ∥ T057   (∥ T053 [oDs] if R1Q11 (a))
                 T054 (projection) → T055 (sources, 4.3 part) → T056 → T058 (validator)
          [oXc]  T059 (5.4a) after T052 + a pin;  T060 (5.3a re-run) after T054
                 T061 (7.3) after C3's PR 2 lands
          pins T062;  checkpoint T063
 PHASE 3  [oDc]  G13: T071→T070→T072→T073→T074      G16: T078→T079→T080 ∥ T081
                 4.3 end: T084 → T085                T075 → T077;  T082, T083, T088
          [oXc]  T086 (columns, ratchet (0,0)) with the pin that retires consumer_reach
          [oD]   T076 (README)  after the command's final form (R1Q15)
          pins T087;  checkpoint T089
 ACCEPTANCE      T095 (HTTP, CI) ∥ T096 (browser)  →  T097 (bookkeeping, Rule 6)
 EVERY PHASE     T090 pins · T091 trailer · T092 notes · T093 interim F11.1
```

## Parallel slices, and the files only one writer may touch at a time

Writers run in parallel when they share no file. Four files are SINGLE-WRITER:
at most one open slice may edit each, and a slice that needs one rebases onto
the previous slice's landing before it opens.

| single-writer file | slices, in order |
|---|---|
| `src/opendox/serve.py` | T011 → T012 → (T016, T022 one-line entry-point calls) → T055 → T073 → T084 |
| `src/opendox/cli.py` | T016/T022 entry-point registration → T038 → T055 → T084 |
| openXdox-code `tests/test_dependency_direction.py` (the ratchet) | T040 → T059 → T086 |
| openxFactory pin pairs | one openxFactory PR per phase (T047, T062, T087), each also carrying that phase's host wiring |

- **Phase 1 parallel lanes**: A (serve seam), B (profile), C (adapter), D
  (workbench, serve_wire and doxbench_packet seams) and E (import test and
  README). openXdox-code's T041 can start as soon as R1Q6 is answered.
- **Phase 2 parallel lanes**: the fixtures (T050, T051), the generator seam
  (T052), the validator input set (T057) and the neutral schema (T053), if
  R1Q11 (a) is chosen.
- **Phase 3 parallel lanes**: Group 13 (T070–T074), the Group 16 binding
  (T078–T080), the no-model state (T081), the retirement of the late reaches
  (T084–T086), and entry-point serving (T075).

## Pins and landing order (9.5): one openDox-code commit per phase, everywhere

Each phase advances the pins in this order. Every step is its owner's ordinary
pin-sync act, and each step's PR is opened only after the step before it has
landed:

1. **openDox-code** lands the phase's slices.
2. **openDox root**: ONE commit moves the `code` gitlink, `contracts/code-pin.yaml`
   `commit:` and every `.github/workflows/*.yml` `@<sha>` that names the leg
   (`make pins` checks this; AGENTS-shape "Advancing a leg is ONE commit here").
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
rebase. Land by **squash or merge commit, never rebase**. That way each landing
is ONE first-parent commit, which is what 5.4a's, 12.5's and 11.1's guards
diff against its parent. A merge landing writes the `Arc:` trailer into the
merge message (11.0).

## The trailer, the guard and Rule 6

- **Realization landings** carry `Arc: neutral-product-standalone-operability`
  in every repository, alongside `Lane: openxfactory-4`. Reviews check both
  (11.0).
- **Bookkeeping** carries NO `Arc:` trailer: this feature's files, #1144's
  ticks and evidence notes, and interim guard output. That follows R1Q20 (a),
  which is recommended, and this planning PR already does so. If Brett answers
  (b), 11.1's surfaces must widen first.
- **The manifest.** An openxFactory arc landing may only add or extend an
  existing `edits[].note` (11.1). Whether arc edits to carved files need
  declared-edit windows first is R1Q22. The recommendation is (a): they do not.
- **Rule 6.** Realization PRs never touch `openspec/changes/`. Only T004's
  amendments and T097's ticks do, and each lands under a `LANDING` / `LANDED`
  window. Closing keywords never appear in a commit message or PR body.

## In-flight overlaps (lane 4's own acts, 2026-09-24)

| act | touches | release-1 overlap | rule |
|---|---|---|---|
| 1.8 ratification record | #1144's three lifecycle docs and `.openspec.yaml` | LANDED as #1151 → `cd494e4c`, ticking 1.8 and 3.0 | T004's amendments build on it |
| C1 (`5815604830`) | an openxFactory count fix | none | — |
| C3 (`5815613524`) | openXdox-code `src/openxdox/snapshot.py` and the validator script; openxFactory manifest rows; the openXdox pin | 7.3's files (T061); 9.5's openXdox pin pair (T047) | T061 starts after C3's PR 2 lands and revisits its confinement per R1Q14; T047 rebases onto C3's pin bump |
| C4 (`5815620605`) | the openXdox-pin resync runbook | 9.5 steps 5 and 6 | follow it once landed |

## Persisted tools

The four measurement scripts in [`research.md`](./research.md) § Appendix are
also persisted to the lane's workspace repository (`opensoft/brett-wip`) under
the lane's tool directory, so that T005's re-measure does not depend on any
session's scratch space. That persistence is recorded in the PR body.

## Complexity Tracking

| deviation | why it is needed | the simpler alternative, and why it was rejected |
|---|---|---|
| Planning with 22 material ambiguities open (constitution workflow: *"resolved before planning"*) | The brief asks for the plan now, and forbids resolving by assumption. Implementation cannot begin anyway until the ratification record lands and the answers come back. | Waiting for the answers before planning would serialize a day of the holder's time behind the questions. The conditional plan names every assumption, T004 re-plans, and T006 gates implementation. |
| A handler-contribution mechanism (R1Q1 (a)), which is new mechanism against design.md § D4 | The existing seam provably cannot carry a mixin's methods (`route_extension.py:60`). | Keeping a forwarding stand-in (R1Q1 (c)) is the pattern 4.3 retires. |
| A second pin chain step inside each phase (openXdox-code's pyproject pin brought to the root's commit) | Without it, openxFactory and openXdox-code test different openDox bytes (research R13). | Leaving the pins divergent means 9.3's integration run measures a composition nobody ships. |
