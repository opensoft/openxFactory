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
  and 10.1. openDox-code's suite runs whole. openXdox-code's runs whole less
  a declared exclusion, which stays an open extraction: the `doc_health` files
  (R1Q6 (d)), the files that reach openxFactory's contracts or rail (R1Q24
  (a)), and `tests/test_snapshot.py` until 7.3 lands (R1Q25 (b)).
- **Phase 2** gives openDox its own neutral generator and its own validator:
  Groups 5 and 7, and 4.3's generator and snapshot-registry reaches. Its
  snapshot's contract is a new openDox-spec schema (R1Q11 (a)). 7.3 is here,
  beside openDox's own validator, as the map has it (R1Q25 (b)).
- **Phase 3** makes it install: Group 13, boxes 10.2, 10.3 and F10.1, Group 16,
  and the rest of 4.3, which retires `consumer_reach.py`. The one documented
  command is `pip install "opendox[local]"`, then
  `opendox generate-and-open --local …` (R1Q15 (b), R1Q16 (iii)). T099
  publishes the package to PyPI at the cut, so that the install line works as
  written (`5962754358`, `5963162921`).
- **Every phase** includes Group 11 (the trailer and the guard) and 9.5 (the
  pins).

#1144 contains contradictions, both internal and with the live code. They
were put to Brett as `R1Q1`–`R1Q22`. One answer raised `R1Q23`, T005's
re-measure raised `R1Q24`, and T006's analyze raised `R1Q25`, and round 2's
analyze raised `R1Q26` and `R1Q27`. **All 27 are answered.**

- **Round 1a**, the eleven questions phase 1 needed: `#656`, `5817152735`,
  *"(a) on all eleven, (d) on R1Q6"*. See § "Ruled answers".
- **Round 2**, the other fourteen and RN-1: `#656`, `5850003126`, *"go with
  recommendations on all the open questions"*. Each is answered with the
  option `clarify-questions.md` recommended, and RN-1 (a) with them. This
  revision encodes them. T019 does so for phase 1's openXdox-code tail, T009
  for phase 2 and T069 for phase 3, and each re-plans its part. One
  `/speckit-analyze` run over the result, in two verifier passes, found
  nothing CRITICAL (`evidence/analyze-round-2.md`). See § "Ruled answers,
  round 2".
- **Round 3**, the two that analyze raised: `#656`, `5851950767`, *"(a) Admit
  the two edits (Recommended)"* and *"(a) Own three, others by tree
  (Recommended)"*, and `5852513402`, which kept R1Q26 (a) once Brett was
  shown the unlisted route W2-10. They are about openXdox's facet `values`
  block and 12.5's protected suite, and about what validates openxFactory's
  own four kinds once 7.3 moves the consumer's validator lookup. T067 encodes
  them and re-plans T059, T060, T061, T063, T064 and T066, and its analyze
  found nothing CRITICAL (`evidence/analyze-round-3.md`). See § "Ruled
  answers, round 3".

So the constitution's workflow gate, *"material ambiguities MUST be resolved
before planning"*, holds for the whole plan, and no phase is provisional.

## Technical Context

**Language/Version**: Python 3.12, which is what the CI of every leg runs and
what the measurements used. JavaScript ES modules for the web bundle, with
Node harnesses in the tests.
**Primary Dependencies**: PyYAML; for the runtime extra, FastAPI, uvicorn,
psycopg 3, PyJWT and httpx; for the tests, pytest 8. The bundled PostgreSQL
server ships in a `local` extra, beside the runtime extra's packages (R1Q16
(iii)).
**Storage**: the corpus is a plain git repository, read through
`LocalGitCorpus`. A bundled PostgreSQL server holds the runtime's datastore
(13.1). The document server starts it as its child and it stops with the
entry point (R1Q16 (i), (iv)). No document is stored in the database (RULING
Q1).
**Testing**: each leg's own pytest suite, run whole (Group 9), less
openXdox-code's declared exclusion (R1Q6 (d), R1Q24 (a), R1Q25 (b)); openXdox-code's
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
sixth through T053 (R1Q11 (a)). openXdox-spec is not touched (R1Q12 (a)),
though T003 recorded its base.
**Performance Goals**: none are new. The readiness loops in F10.1 and F13.1
allow 30 seconds.
**Constraints**:
- No host-absolute path in any committed file (Principle IV).
- No raw credential anywhere.
- Nothing moves out of openxFactory (requirement 1).
- Only `doxbench_provider.py` contacts a provider.
- Local mode binds to loopback only.
**Scale/Scope**: release 1 has 70 of #1144's 125 boxes (tasks.md § "Box
accounting"). About 12 carved openDox-code files are edited (research R12), and
27 deferred reaches plus 65 `consumer_reach` uses are routed (research R5, R6).

## Constitution Check

*GATE: checked before planning, and re-checked after each round of answers.
Round 1a was #1155, and #1167 carried T005's re-plan and T006's analyze
(`evidence/analyze-round-1a.md`). This revision carries round 2
(`5850003126`) and its analyze (`evidence/analyze-round-2.md`).*

| principle | status | how this feature meets it |
|---|---|---|
| I. Contract-first, domain-neutral core | PASS | openxFactory gains only host wiring, pin pairs, notes, and the named composition tests that R1Q2 (a) admits (11.1). No domain vocabulary enters openDox; the default profile's words are `NEUTRAL_DISPLAY`'s (requirement 3, third scenario). |
| II. OpenSpec before implementation | PASS | Everything here realizes the RATIFIED #1144 (`5815412869`). An answer that amends a #1144 falsifier or task line is recorded there on Brett's word (T007). One that would change requirement or scenario text goes back to him first (RN-1, ruled (a) in `5850003126` and landed by T007's batch D as #1170). Speckit owns the tasks; #1144's `tasks.md` is ticked, and never duplicated (T097). |
| III. Document lifecycle | PASS | Every feature file carries a controlled `Status:` header, in the form feature 029's files use: `draft` for the plan's documents, and `record` for `evidence/`. #1144 is `Status: ratified`, with its record landed as #1151 → `cd494e4c`. |
| IV. Schema and artifact discipline | PASS | No committed file names a host path: every command resolves its scratch space with `W=$(mktemp -d)`. No credential is stored: 16.3 refuses raw keys. **The README document index** links all seven of this feature's documents, and its evidence records, in one entry in its Documentation section, beside the openDox carve documents. The entry sits outside the OpenSpec Records block, so it needs no Rule 6 window. None of the 31 earlier feature directories under `specs/` on `main` (`138a4722`) is indexed there, so this entry is the first of its kind. |
| V. Validation gates | PASS for this PR, against `main`'s recorded baseline | T007's batch PRs (A to N) do touch #1144's files under `openspec/changes/`. Each records its own gates against the `main` it lands on. Batch N's (#1222) measured the pinned `--all` gate at rc 0, with `0 UNDISPOSITIONED failures` and the one accepted exception `add-chain-attestation`, identical apart from the clone path at `main` `ec9308c8` and at its head, both in clones whose `remote.origin.url` is opensoft/openxFactory. The pin reads its dispositions' scope from that URL. The rest of this row is the planning PR's record. That PR touches no `openspec/` path: `git diff --stat main -- openspec/` is empty. `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` gives `110 passed, 1 failed (111 items)` at this branch's head, run on 2026-09-27 over `main` at `b060d400` with this revision's files, and `main` gives the same, since this PR adds no `openspec/` path. #1155 measured `110 passed, 1 failed` on 2026-09-24. Since then `admit-code-leg-under-pinned-root` was filed on `main` as #1156 (`daca0b89`) and archived by #1174 (`b060d400`), so the count is where #1155 left it. research.md's `dd2466ad` is a different thing: the baseline the plan's measurements were taken at, not this PR's gate. The one failure is `add-chain-attestation`'s "omits scenario(s)" finding. It is an accepted disposition in `contracts/openspec-cli-pin.yaml` (`ratified_by: 'Brett Heap, 2026-09-05, "take exit 2"'`), and it retires when that change archives. This PR cannot move it. The gate the repository enforces, `scripts/validate-openspec-cli-pin.py --all` (the `openspec-cli-pin` check), exits 0 with `0 UNDISPOSITIONED failures`. No other `scripts/validate-*.py` reads `specs/`. The PR that lands this revision is green on every check before it lands, and its READY comment quotes them. Implementation evidence will be falsifier output, quoted. |
| VI. Versioned releases | PASS | R1Q11 (a) adds an openDox-spec schema (T053), so phase 2 cuts a `dox-v1.x` minor bundle at the openDox root, under the root's own four-value rule. 9.5 says *"none cuts a contract bundle"*, so T007's batch G records 9.5's addendum before T053 lands. |
| VII. Fail-closed authority | PASS | Every seam refuses naming itself when nothing is registered (4.2's discipline). The hosted mode refuses without an issuer. An unknown dialect is refused. |
| Workflow: *"material ambiguities MUST be resolved before planning"* | **PASS** | Every material ambiguity is resolved. Round 1a (`5817152735`), round 2 (`5850003126`) and round 3 (`5851950767`) answer all 27 questions, and RN-1 is ruled (a) and landed (#1170). No task carries a `Blocked by:` line (FR-012), and no phase is provisional. Each round's analyze found nothing CRITICAL (`evidence/analyze-round-1a.md`, `evidence/analyze-round-2.md`, `evidence/analyze-round-3.md`). |
| Repository Constraints | PASS, with one deviation | **Shared tree**: every writer works in its own clone, stages explicit paths and commits with pathspecs, so none touches the shared root checkout. **Worktree mode**: the git extension's sibling worktree under `../openxFactory-worktrees/` is not used. This feature's PRs run from the lane's own clone of openxFactory, as the lane protocol and each brief require; the rule's purpose, that no lifecycle command runs in the root checkout, holds. See Complexity Tracking. **The aggregation pin**: each openxFactory landing (this feature's bookkeeping PRs, T007's batches, T066, and T047, T064 and T094) is followed by the aggregation's ordinary pin-sync in `opensoft/xFactory`, a separate commit that is not an arc landing and carries no `Arc:` trailer. The holder has it done after each landing, as this Repository Constraints rule requires. |

## Project Structure

### Documentation (this feature)

```text
specs/034-opendox-standalone-operation/
├── spec.md                 # user stories, FRs mapped to #1144, AT-R1
├── plan.md                 # this file
├── research.md             # every measurement, with its command
├── clarify-questions.md    # R1Q1–R1Q27, all answered (5817152735, 5850003126, 5851950767)
├── quickstart.md           # AT-R1's procedure
├── tasks.md                # 96 tasks, T001–T104 (some ids unused), box accounting (70 of 125)
├── checklists/
│   └── requirements.md     # the spec-quality checklist
└── evidence/               # bookkeeping records, with no `Arc:` trailer (R1Q20 (a))
    ├── arc-base.md         # T003: ARC_BASE for all seven repositories; PACKET_MERGE
    ├── remeasure-2026-09-25.md   # T005: R1–R15 again, and openXdox-code's whole suite
    ├── analyze-round-1a.md # T006: the prerequisites check and analyze's verdict
    ├── analyze-round-2.md  # T019, T009, T069: round 2's analyze, one run over the result
    ├── analyze-round-3.md  # T067: round 3's analyze
    ├── f11.1-phase1.txt    # T017, T018: phase 1's interim F11.1
    ├── checkpoint-phase1.md # T049: phase 1's checkpoint, quoted
    ├── f11.1-phase2.txt    # T065: phase 2's interim F11.1
    ├── checkpoint-phase2.md # T063: phase 2's checkpoint, quoted
    ├── f10.1-run.md        # T077: F10.1, run as batch H amends it, quoted
    └── f13.1-run.md        # T074: F13.1, run as batch H amends it, quoted
```

T018 added phase 1's interim F11.1 run, and T049 its checkpoint. T065 added
phase 2's interim F11.1 run, and T063 its checkpoint. T077 added its F10.1
run, quoted in the checkpoints' form on the holder's ruling of 2026-10-03,
and T074 its F13.1 run in the same form.
Later tasks add their own records to `evidence/`:
T098 adds the interim F11.1 run for phase 3, and T096 AT-R1. T009, T019 and T069 share one analyze record,
`analyze-round-2.md`. Each is linked from this feature's README entry.

### Source code: the six repositories release 1 lands in

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
  src/opendox/web/views/doxbench-chat.js, lens.js                              16.4, R1Q19 (a)
  src/opendox/web/views/staging-workbench.js, staging-workbench-model.js       T102: the editors and the rail by scope
  src/opendox/web/views/lens.js, web/index.html                                T102: the display text (lens.js after T088)
  src/opendox/web/app.js, web/views/edit.js, staging-workbench-model.js        T104: the console token from the opened URL (after T102)
  tests/fixtures/plain-documents/, tests/fixtures/malformed/                   5.0, 7.0
  tests/test_imports_standalone.py, test_authoring_seam.py,
    test_profile_registration.py, test_chat_model_configuration.py             named by the falsifiers
  acceptance/at_r1_http.py                                                     T095: a harness in its own job, no database
  .github/workflows/release.yml, .github/release-tools-cpython312-linux.txt    T101: the release workflow, by trusted publishing; T099 publishes with it at the cut
  conftest.py, pyproject.toml, .github/workflows/validate.yml, README.md       9.1, 10.1, 2.6
opensoft/openXdox-code           [oXc]   the consumer
  pyproject.toml (opendox pin), tests/test_dependency_direction.py (ratchet)   9.5, 4.3
  src/openxdox/<contributions through the seams>                               5.4a, 4.3
  <declared doc_health exclusion file>, conftest.py                            9.2, R1Q6 (d)
  src/openxdox/view_extensions.py (DISPLAY's values block)                     5.3a, R1Q11 (a)
  src/openxdox/snapshot.py, scripts/validate-ideation-dashboard-contracts.py   7.3 (phase 2, after C3)
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
  tests/ideation-dashboard/test_dashboard_source_seal.py, scripts/profile_openxfactory.py,
    tests/test_engineering_profile_display_facet.py   T066, a non-arc act before T064
opensoft/openDox-spec            [oDs]   the neutral snapshot schema (T053, R1Q11 (a))
```

No task touches opensoft/openXdox-spec, since R1Q12 is answered (a).

**Structure Decision.** ONE Speckit feature for release 1, with release 2 as
its own feature, planned once release 1 lands (R1Q21 (a), ruled in
`5850003126`). The feature lives in
openxFactory, beside its governing change. Implementation happens in each
repository's own clone or worktree, on a branch named for the slice, and each
slice lands through that repository's own pull request. None of it happens in
this worktree, which holds the plan only.

## Phases, and where every release-1 box closes

| phase | boxes that CLOSE in it | exit (all quoted in the phase checkpoint task) |
|---|---|---|
| 0 | 3.0 (ratification) | answers applied; analyze clean |
| 1 | 2.1, 2.1a, 2.2, 2.3, 2.4, 2.5, 2.6, F2.1; 3.1, 3.2, 3.3 (first run; T065 and T098 repeat it before T097 ticks it), F3.1; 4.1, 4.1a, 4.2; 9.1, 9.2a, 9.3, 9.4, F9.1; 10.1 | F2.1, F3.1, F9.1 (both legs), F9.2 (quoted red, as RULED `5859927858` keeps it), `opendox --help` |
| 2 | 5.0, 5.1, 5.2, 5.3, 5.3a, F5.1, 5.4, 5.4a, 5.5, F5.3; 7.0, 7.1, 7.1a, 7.1b, 7.2, 7.3, F7.1, F7.2 | F5.1, F5.2 (quoted red on three pre-arc tests; RULED `5962785556` closes it in phase 3), F5.3, F7.1, F7.2; standalone `generate-and-open` serves |
| 3 | 4.3, F4.1; F5.2 (T086 repairs its three pre-arc reds; RULED `5962785556`, at T063); 9.2 (its whole-suite check lands in phase 1, and its ratchet reaches `(0, 0)` at T086, as T007's batch F records beside the map, R1Q25 (b)); 10.2, 10.2a, 10.3 (at the cut, on T099's publish), F10.1; 13.1–13.6, 13.4a, F13.1; 16.1–16.6, 16.3a (T007's batch M), F16.1 | F4.1, F5.2, F10.1, F13.1, F16.1 (as batch M amends it); AT-R1 follows the checkpoint (T095, T096); 10.3 closes only at the cut, on T099's publish |
| every phase, ticked at ARC close | 9.5, 11.0, 11.1, F11.1 | interim F11.1 after each phase |
| after T008, outside release 1's tasks | F9.2 (RULED `5859927858` keeps it unchanged and red on the assembled help-tree test until T008; holder decision, 2026-09-29, at T049. The test reads 31 entries through phase 2 and 32 from phase 3's pin, RULED `5970917267`; T086 moves it) | F9.2, after the `doc_health` direction arc |
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
T001–T009, T019, T067 (holder: claims, ARC_BASE, rounds 1a, 2 and 3, re-measure, analyze, #1144 amendments in batches A–N, the direction arc)
                              │
 PHASE 1  [oDc]  A: T010→T011→T012 (serve.py)     B: T015→T016 (profile)
                 C: T020→T021→T022 (adapter)      D: T026→T025, T027 (seams; T025 also after T020)
                 E: T030 (the import test; lands with T011)
                        └───────── join ─────────┘
                 T032 (2.3 sweep) → T034 (repair 9 files) → T035 → T036 (+ T031) → T037
                 T038 (10.1, Q-R4)  after B and T022
          [oD]   T039 root pin (T090 steps 1–2)  after T022, T032, T037, T038
          [oXc]  T040 (pin, residue) → T041 (declared exclusion, four reasons) → T042 (9.3) → T043 → T044
                 T007 batches C and F before T043
          [oX]→[oxF]  T047 consumer pins (steps 5–6) after T039, T044, T007 batches A and E; carries T045 + T046
          T047 → T017 (3.3) and T018 (interim F11.1) → checkpoint T049 (after T007 batches A, B, D, F and J);  holder T048
 PHASE 2  T053 [oDs][oD] first: the neutral schema, the spec pin, the dox-v1.x bundle (after T007 batch G)
          [oDc]  T050 → T051;  T053 → T052;  T053 → T057
                 T054 (projection) → T055 (sources, 4.3 part; also after T057) → T056 → T058 (validator)
          [oD]   T062 root pin  after T054–T058
          [oXc]  T060 (the facet's values) after T054, T007 batch I;  T059 (5.4a, the pin) after T052, T055, T060, T062, T007 batches C and I
                 T059 → T061 (7.3, after T007 batches C, F, I and K)
          [oxF]  T061 → T066 (a non-arc act: the seal test and the facet's values, at both pins)
          [oX]→[oxF]  T066 → T064 consumer pins → T065 (interim F11.1) → checkpoint T063 (after T007 batches C, F, G, I and K)
 PHASE 3  T069 is done; T007 batch H lands before T070, T075 and T080, batch K before T080, batch M before T100, and batch N before T095
          [oDc]  G13: T071→T070→T072→T073→T074      G16: T078→T079→T080;  T085 → T081
                 4.3 end: T084 (after T073, T007 batch L)          T072 → T075 → T077 (F10.1 as batch H amends it);  T082, T083, T088
                 16.3a: T100 (after T080, openDox-code#64, T081, T072, T084, T007 batch M) → T083 (F16.1 as batch M amends it)
          [oD]   T087 root pin → T076 (README: the opendox[local] install and the --local command)
          [oXc]  T086 (columns, ratchet (0,0)) at the pin T087 carries
          [oX]→[oxF]  T094 consumer pins + host wiring (after its non-arc ahead PR, the phase-3 help golden) → T098 (interim F11.1) → checkpoint T089 (after T076)
          [oDc]  T084 → T102 (the workbench by scope; also after T081, T088) and T084 → T103 (the loopback Host check)
          [oDc]  T103 → T104 (the console token in the opened URL, not /capabilities; also after T102)
          [oDc]  T101 → T087 (T099's release step: the release workflow, then the 0.1.0 bump, after every package-changing phase-3 openDox-code landing)
          [oDc]  T089 → T099 and T096 → T099 (the PyPI publish at the cut, of the commit T087 pins, after the acceptance)
          [oD]   T099's last step: the root README's "Where opendox comes from" becomes the PyPI install line (after T076)
 ACCEPTANCE      T095 (HTTP, CI; after T089, T076, T104 and T007 batch N)  →  T096 (browser)  →  T099 (the publish)  →  T097 (bookkeeping, Rule 6)
 EVERY PHASE     T090 pins · T091 trailer · T092 notes · T093 interim F11.1 (run as T018, T065, T098)
```

## Parallel slices, and the files only one writer may touch at a time

Writers run in parallel when they share no file. The surfaces below are
SINGLE-WRITER: at most one open slice may edit each, and a slice that needs one
rebases onto the previous slice's landing before it opens. T009 and T069
re-derived the phase-2 and phase-3 entries from the re-planned tasks' file
lists.

| single-writer file | slices, in order |
|---|---|
| `src/opendox/serve.py` | T010 (`build_server`'s bases) → T011 → T012 → (T016, T022 one-line entry-point calls) → T052 (the generator's registration call) → T055 → T072 (the bundled server, the document server's child) → T073 → T084 → T103 (every loopback route checks `Host`) → T104 (`/capabilities` stops carrying the console token) |
| `src/opendox/cli.py` | T016/T022 entry-point registration → T038 → T052 (the generator's registration call) → T055 → T058 (the generate verbs' post-render validator) → T070 (`--local`) → T084 → T104 (`generate-and-open` opens the page with the console token in the URL fragment, and keeps its private copy) |
| `src/opendox/workbench.py` | T026 → T025 (both in P1-E) → T055 (the validator lookup's default) |
| openDox-code `pyproject.toml` | T038 (`[project.scripts]`) → T036 (`testpaths`, and the `test` extra) → T057 (the validator's package data) → T072 (the `local` extra, which the `test` extra joins) → T075 (the bundle's `web/**/.*`) → T101 (`readme`; then the version bump to 0.1.0, the last package-changing phase-3 openDox-code landing) |
| openDox-code `tests/test_authoring_seam.py` | T020 (the seam tests) → T021 → T022 |
| openDox-code `tests/test_consumer_reach.py` | T011 (`opendox.cli` and `opendox.serve` into `NEUTRAL_MODULES`) → T034 (the rest of `STILL_REACHING`) |
| openDox-code `.github/workflows/validate.yml` | T036 → T037; no earlier phase-1 slice edits it (tasks.md § Phase 1), and T095 adds phase 3's `acceptance` job |
| openDox-code `src/opendox/doxbench_binding.py` | T078 (the second dialect) → T079 (the `model` field) → T080 (the raw-key refusal and the auth kind `none`), all in P3-B, then the broker-path follow-on, a PR of no task (openDox-code#64, LANDED → `8e377823`), then T100 wherever it edits the record (16.3a) |
| openDox-code `src/opendox/cli_model_binding.py` | T079 (`--model`) → T080 (the resolver's and `none`'s arguments) → T100 (`add` and `edit` record trust, the `trust` verb, `set-credential`'s gate and re-trust) |
| openDox-code `src/opendox/doxbench_install.py` | T081 (16.4's catalog, in P3-D after T085) → T100 (16.3a's gate where the bindings are read) |
| openDox-code `src/opendox/serve_workbench.py` (phase 3) | T084 (4.3's last reaches, openDox-code#77) → T100 (16.3a: the console intake's broker hand-off) |
| openDox-code `src/opendox/web/views/lens.js` | T088 (the seed actions offered only where a binding answers) → T102 (the display text) |
| openDox-code `src/opendox/web/views/staging-workbench-model.js` | T102 (the editors and the rail by scope) → T104 (the console token's reader) |
| openDox root `README.md` | T076 (the one documented command, with the dated "Where `opendox` comes from" paragraph) → T099 (that paragraph becomes the PyPI install line, after the publish) |
| openXdox-code `tests/test_dependency_direction.py` (the ratchet) | T040 (it moves the pin and leaves the ratchet unchanged) → T059 → T086 |
| openXdox-code `tests/test_gate_loop_views.py` (one of 12.5's protected suites) | T060 (the facet-declaration test's entered edit) → T059 (the overlay test's entered edit), both under R1Q26 (a) |
| openXdox-code `pyproject.toml` | T040 (the `opendox @` pin and `rfc3339-validator`) → T059 (the phase-2 pin) → T061 (the validator's package data) → T086 (the phase-3 pin) |
| openXdox-code's declared exclusion file | T041 (the file, its four reasons and every entry, on the holder's decision at T041's landing) → T043 (a re-run at T040's pin, which moved no entry) → T044 (any file whose skip joins it) → T061 (`tests/test_snapshot.py`'s entry leaves) |
| openDox root `code` gitlink, `contracts/code-pin.yaml`, workflow `@sha` | one commit per phase (T039, T062, T087), each after that phase's last openDox-code landing. In phase 2, T053's spec pin and bundle come first in this root |
| openxFactory pin pairs | one openxFactory PR per phase (T047, T064, T094), each also carrying that phase's host wiring |

- **Phase 1 parallel lanes**: A (serve seam), B (profile), C (adapter), D
  (workbench, serve_wire and doxbench_packet seams) and E (the import test,
  which lands with T011; the README fix, T031, lands with T036). R1Q6 is
  answered (d), so openXdox-code's T041 waits only on T006 and T040. T043
  waits for T041, T042 and T007's batches C and F.
- **Phase 2 parallel lanes**: the neutral schema (T053) first, beside the plain
  fixture (T050). Then the malformed fixture (T051), the generator seam (T052)
  and the validator input set (T057) run in parallel. tasks.md § "Phase 2
  writer slices" gives the fan-out.
- **Phase 3 parallel lanes**: Group 13 (T070–T074), the Group 16 binding
  (T078–T080), the doxBench defaults and then the no-model state (T085 →
  T081), the retirement of the late reaches (T084, after T073; then T086), and
  entry-point serving (T075, after T072). Per-machine binding trust (T100,
  16.3a) follows the binding slice, the no-model state and T084, and comes
  before F16.1's whole run (T083). The workbench by scope (T102) and the
  loopback Host check (T103) follow T084, and the console token's move to
  the opened URL (T104) follows both. The release step (T101) lands last
  among the package-changing openDox-code landings, before T087, and the
  PyPI publish (T099) follows the checkpoint and the acceptance, at the
  cut. tasks.md § "Phase 3 writer slices" gives the fan-out.

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

**The runbook C4 wrote** (lane 4's openXdox-pin resync runbook,
`docs/openxdox-pin-resync-runbook.md`, landed as #1154 → `138a4722`) is the
procedure for steps 5 and 6. #1146 and #1148 are the shape it records.

**Phase 2's extra root commits.** T053 moves the openDox root's spec pin to the
openDox-spec commit carrying the neutral snapshot schema, and then cuts the
`dox-v1.x` minor bundle (R1Q11 (a), batch G's 9.5 addendum). Both come before
T062's code-pin commit in that root.

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
- **T066 is not an arc landing.** It is openxFactory's own change to its
  seal test and its facet composition, correct at the current pins and at
  T064's, like F3's overlays. So it carries no `Arc:` trailer, and 11.1's
  guard never reads it. R1Q14's T006 paragraph names this route, T019 chose
  it, and T067 narrowed it on R1Q27 (a) (tasks.md T066).
- **How the guards find the arc's landings.** F5.2, F11.1 and 12.5's
  falsifier select them with `git log --first-parent --grep='^Arc:
  neutral-product-standalone-operability$'`, which matches that line anywhere
  in a commit's message, not only in git's parsed trailer block. So the seven
  openDox-code landings whose squash message carries the line in its body
  count as written. openDox-code#37 (`e295b1a9`, T020) and #44 (`9d13bd16`,
  T021) carry no `Arc:` line, and T091's record at the arc's close names both
  (tasks.md T091).
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
  amendments (batch D among them, landed as #1170), T008's proposal if it
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
| R1Q5 | (a) | `RuntimeSubcommand` arrives through `SUBCOMMAND_EXTENSIONS`, with the `opendox-runtime` alias (T038). The 31-entry goldens stand (T042). From phase 3's pin they hold 32, because T100 adds `model-binding trust` (RULED `5970917267`; T086, and T094's non-arc ahead PR). |
| R1Q6 | (d) | openXdox-code's declared `doc_health` exclusion (T041, T043, T044). T007 batch B amends F9.1. T008 raises the direction arc. The answer raises R1Q23. |
| R1Q7 | (a) | The reviewed respelling allow-list (T007 batch C; T043, T059, T086). |
| R1Q8 | (a) | `tests_runtime/` is part of the whole suite, with a PostgreSQL service in the required job (T036). F9.1 is unchanged. |
| R1Q9 | (a) | `session_documents` resolves through `list_documents` in phase 1 (T025, T046). |
| R1Q20 | (a) | Bookkeeping carries no `Arc:` trailer (T091). T007 batch A adds 11.0's addendum. |

**Where the amendments go.** Brett's comment says: *"Where an answer amends a
ratified falsifier (F3.1, F9.1) or widens the 11.1 guard, that change rides in
the realization as the answer records it."*

- The planning PR (#1155) edits no file of #1144.
- T007 records each amendment in #1144's `tasks.md`, in bookkeeping batches:
  A, B and C for the answers of `5817152735`, D for RN-1 (a) (landed as
  #1170), E for the composition tests phase 1 finds, F, G and H for round
  2's answers, which T019, T009 and T069 encode, I for round 3's, which
  T067 encodes: 5.3a's `values` block, 12.5's two admitted edits and F7.1's
  reading, J for the help-tree deselect (`5870594693`), and K for Brett
  Heap's word of 2026-09-30 (`5916000030`): a dated note to requirement 17
  on the loopback and broker-path rulings (`5880893901`, `5890601202`), and
  F5.2's admission of T061's ten walk-premise edits, and L for Brett Heap's
  second word of 2026-09-30 (`5920216845`): 4.3's addendum on what the
  served `/capabilities` payload's `actions` map claims, and M for Brett
  Heap's word of 2026-10-02 (`5962785556`, item 2): box 16.3a, a second
  dated note to requirement 17 and F16.1's added line, for per-machine
  trust of a served repository's model bindings, and N for Brett Heap's
  word of 2026-10-03 (`5963851934`): 12.4a's addendum on how a standalone
  plane's console token reaches the page, through the opened URL and never
  `/capabilities`.
- Each batch lands under a Rule 6 window, with no `Arc:` trailer, before the
  task that needs it. A batch that amends a falsifier lands before the
  checkpoint that runs it. Batch N amends none, and lands before T095,
  AT-R1's HTTP half, whose harness reads the private copy it records.
- `tasks.md` § "Ruled amendments" lists every amended line, the text it takes,
  and the task that carries it out.

## Ruled answers, round 2 (`5850003126`)

Brett Heap answered the other fourteen questions, and RN-1, on `#656`, comment
`5850003126` (2026-09-26T21:23:03Z), verbatim: *"go with recommendations on
all the open questions"*. Each answer is the option `clarify-questions.md`
recommended.

| question | answer | what it fixes in this plan |
|---|---|---|
| R1Q14 | (a) | 7.3 governs the lookup (T061). F5.2 admits T061's two edits (batch F), and T066 holds openxFactory at both pins. Under R1Q27 (a), T066 moves none of openxFactory's validator callers. |
| R1Q24 | (a) | The declared exclusion takes the rail and contracts classes, each file with its reason (T041, T043), and T008's arc takes them. |
| R1Q25 | (b) | 7.3 stays in phase 2 (T061, after T059). Phase 1 declares `tests/test_snapshot.py` in the exclusion (T043), and 9.2's phase-3 close is batch F's addendum. |
| R1Q10 | (a) | An openDox default for each consumer mechanism, registered by the entry points (T052, T055, T084, T085), and openXdox's governed ones through the same seams (T059, T086). Batch G's 4.3 addendum. |
| R1Q11 | (a) | A neutral snapshot schema in openDox-spec, a sixth repository (T053). `SNAPSHOT_VALUES`' defaults move, and the governed values go to openXdox's facet (T054, T060). A `dox-v1.x` bundle. Batch G: 5.3, 7.0, 7.1 and 9.5. 5.3a's `values` block is batch I's (R1Q26 (a)). |
| R1Q12 | (a) | openDox's validator takes its spec leg's four kinds as digest-checked package data (T057), and the malformed fixture breaks the neutral schema (T051). openXdox-spec is untouched. Batch G: 7.0 and 7.1. |
| R1Q13 | (a) with (c) | A neutral `stage:` key, a small default field set, and sources with derived groups (T050, T054, T096). |
| R1Q23 | (a) | F5.2 composes openxFactory's `scripts/` at a named commit (batch G; T059, T063). |
| R1Q15 | (b) | `--local` on the documented command (T070, T076, T077). Batch H: F10.1, 10.3 and 13.4. |
| R1Q16 | (i)–(iv) | The bundled server is the document server's child, ships as `opendox[local]`, and stops with the entry point (T072, T073, T095). Batch H: 13.1, F13.1, and F10.1's install line. |
| R1Q17 | (b) | A built-in `env:` and keyring resolver in `doxbench_provider.py` (T080). Batch H: 16.3. |
| R1Q18 | (a) | The auth kind `none` (T080). Batch H: 16.3. |
| R1Q19 | (a) now, (b) later | The seed actions are capability-gated (T088, T096). |
| R1Q21 | (a) | Release 2 is its own Speckit feature (§ Structure Decision). |
| RN-1 | (a) | Requirement 3's two scenarios, landed by batch D as #1170 → `79a720a2`. T016 is unchanged. |

### Ruled answers, round 3 (`5851950767`)

Round 2's analyze (`evidence/analyze-round-2.md`) found two places where the
answers did not settle what the realization must do, and put them to Brett
Heap in `clarify-questions.md`. He answered both (a) on `#656`, comment
`5851950767`, 2026-09-27T02:25:29Z. T067 encodes them. Shown a route R1Q26
had not listed (W2-10), he kept (a), on `5852513402`.

| question | answer | what it fixes in this plan |
|---|---|---|
| R1Q26 | (a) | Batch I amends 5.3a to admit the facet's `values` block, and 12.5's falsifier to admit the two edits to `tests/test_gate_loop_views.py`, each entered with its reason. T060 makes the first edit and T059 the second. T066 composes `values` into openxFactory's profile at both pins. |
| R1Q27 | (a) | The consumer's validator validates its own three kinds from its installed distribution, and the other kinds only where the tree it runs from supplies their schemas, its own `contracts/` read first (T061). F7.1's second test reads every schema that install validates (batch I; T061, T063). No contract row changes, and T066 moves none of openxFactory's validator callers. |

What each question was:

- **R1Q26.** R1Q11 (a) puts the governed snapshot values in openXdox's
  `DISPLAY` facet (T060). `tests/test_gate_loop_views.py`, one of the sixteen
  suites 12.5's falsifier protects, pins that facet as a value and pins the
  five leaves it changes, so T060's landing and T059's pin turn two of its
  tests red, and R1Q7 (a)'s allow-list admits only respellings. openxFactory's
  profile composes only the facet's `stages`, and its own test asserts it. The
  recommendation is (a): 12.5's falsifier admits the two edits, each with its
  reason, as batch F does for F7.1, and T066 composes `values` in
  openxFactory at both pins.
- **R1Q27.** 7.3 narrows the consumer's validator to its three schemas (T061).
  openxFactory's `contracts/manifest.yaml`, its cross-reference validator and
  its contracts README name that validator as the one that checks
  openxFactory's own four kinds, which openxFactory's farm composes beside it.
  The recommendation is (a): the validator checks its own three from its
  installed distribution, and the other kinds only where the tree it runs from
  supplies their schemas, so no contract row changes.

No task carries a `Blocked by:` line for them now. T007's batch I lands
before T059, T060, T061 and T063.

### Ruling needed

Brett's comment keeps the post-word rule: *"any change to requirement or
scenario TEXT still comes back to Brett as RULING NEEDED."* One answer implies
such a change.

**RN-1 — requirement 3's fourth scenario, against R1Q3 (ii). RULED (a)** in
`5850003126`, and T007's batch D landed it as #1170 → `79a720a2`. The scenario
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

RN-1 held phase 1's CLOSE, not its work. It is ruled (a), so T016 does what
it planned: after a build it leaves today's `AlreadyRegistered` refusal in
place, and that refusal is (ii). The checkpoint T049 reports requirement 3 as
realized once T016 matches the amended text.

**Not a ruling: a watch item for the archive.** Under R1Q6 (d), requirement 9
is met for openXdox-code by its first scenario: a declared exclusion, with its
count and its reason. That exclusion stays an OPEN EXTRACTION until T008's
direction arc lands. The archive act must report it as open, and must not
read it as closed.

**Raised by an answer: R1Q23.** R1Q6 (d) leaves four of 5.4a's generator
suites needing `doc_health`. F5.2 runs in phase 2 (its box closes in phase 3,
at T089, RULED `5962785556`), and it installs nothing
that provides `doc_health`. R1Q23 asked how F5.2 runs, and Brett answered (a):
F5.2's environment composes openxFactory's `scripts/` at a named commit (batch
G). At openXdox-code `e28930bf` the glob selects seven suites, and the seventh
passes (T005).

**Raised by the re-measure: R1Q24, and T061 in phase 1.** T005 ran
openXdox-code's whole suite for the first time
([`evidence/remeasure-2026-09-25.md`](./evidence/remeasure-2026-09-25.md)).

- Most of what it found is carve residue, which T040 now clears.
- Two classes reach openxFactory without going through `doc_health`, so
  R1Q6 (d)'s exclusion cannot hold them. They are the status-exemption rail
  (three files) and the contract family (four files). R1Q24 asked where they
  run, and Brett answered (a): in the declared exclusion, each with its reason.
- `tests/test_snapshot.py` still fails two cases on its schemas, so T061's
  contingency applied, and T061 came into phase 1 until R1Q25 (b) returned it
  to phase 2. F7.1's second named test goes into one of the contract-family
  files, and still runs by node id (R1Q24 (a)).

**Raised by T006's analyze: R1Q25, and R1Q12 off the tail.** The RULED
release map puts Group 7 in phase 2, and the contingency that moved 7.3 into
phase 1 is the plan's, so R1Q25 put the move to Brett, with 9.2's phase-3
close beside it. R1Q12 stopped holding T061, since T061 packages the three
schemas where they stand, and R1Q12 is now answered (a), so they stay at
openXdox-spec. The analyze also found that openxFactory's nightly and refresh lanes
read the lookup T061 changes, and that R1Q14's options weigh differently for
them (R1Q14's T006 paragraph). Its second pass found phase-1 callers that
validate other kinds through the validator T061 would narrow to its three
schemas: two today, and a third once T061's lookup reaches it. So R1Q25
recommended (b), which keeps 7.3 in phase 2, beside openDox's own validator
(T057, T058). Brett answered (b).

T019 applied all three answers, R1Q14 (a), R1Q24 (a) and R1Q25 (b), in this
revision. T061 is phase 2's, after T059, and T043 declares
`tests/test_snapshot.py` in the exclusion until it lands.

## In-flight overlaps (lane 4's own acts, all landed by 2026-09-24T18:34Z)

| act | touches | release-1 overlap | rule |
|---|---|---|---|
| 1.8 ratification record | #1144's three lifecycle docs and `.openspec.yaml` | LANDED as #1151 → `cd494e4c`, ticking 1.8 and 3.0 | T007's amendments build on it |
| C1 (`5815604830`) | an openxFactory count fix | none; LANDED as #1152 → `9afea8d7` | — |
| C3 (`5815613524`) | openXdox-code `src/openxdox/snapshot.py` and the validator script; openxFactory manifest rows; the openXdox pin | 7.3's files (T061); 9.5's openXdox pin pair (T047). PR 1, the manifest window, LANDED as #1153 → `1d14fee6`; PR 2 LANDED as openXdox-code#28 → `e28930bf`; the openxFactory openXdox pin bump LANDED as #1157 → `1edbb3dd` | T061 revisits PR 2's confinement under R1Q14 (a), in phase 2 (R1Q25 (b)). T043 and T047 start from these landings |
| C4 (`5815620605`) | the openXdox-pin resync runbook | 9.5 steps 5 and 6; LANDED as #1154 → `138a4722` | T090 follows it |

## Persisted tools

The four measurement scripts in [`research.md`](./research.md) § Appendix are
also persisted to the lane's workspace repository (`opensoft/brett-wip`) under
the lane's tool directory, so that T005's re-measure does not depend on any
session's scratch space. T005's fifth script, `classify_whole_suite.py`
(`evidence/remeasure-2026-09-25.md` § Appendix), sits beside them, with the
plan-consistency checks that T006 ran and that T009, T019 and T069 run again.
The checks read each of T007's batches as a node of its own (tasks.md
§ Format), and check for cycles with each Lands-with group merged too. Round 2
widened them to batches G, H and I, to the phase-2 and phase-3 slice tables,
to R1Q26 and R1Q27, and to every answer form in `clarify-questions.md`'s
headers. Each persistence is recorded in its PR's body.

## Complexity Tracking

| deviation | why it is needed | the simpler alternative, and why it was rejected |
|---|---|---|
| T066, a non-arc openxFactory act inside the arc's sequence | 11.1's guard admits no arc edit to `tests/test_engineering_profile_display_facet.py` or the seal test, and R1Q2 (a)'s named set holds neither, so their edits cannot ride in T064. A form that holds at both pins lands first, so `main` stays green at every pin. R1Q14's T006 paragraph names the route. | Widening 11.1's surfaces to these tests would need a ruling. Holding T061's narrowing until release 2 would leave F7.1 open, against R1Q25 (b). |
| A handler-contribution mechanism (R1Q1 (a), ruled), which is new mechanism against design.md § D4 | The existing seam provably cannot carry a mixin's methods (`route_extension.py:60`). T007 batch A records D4's addendum. | Keeping a forwarding stand-in (R1Q1 (c)) is the pattern 4.3 retires. |
| A second pin chain step inside each phase (openXdox-code's pyproject pin brought to the root's commit) | Without it, openxFactory and openXdox-code test different openDox bytes (research R13). | Leaving the pins divergent means 9.3's integration run measures a composition nobody ships. |
| Running this feature's lifecycle commands from the lane's own clone of openxFactory, not from the git extension's sibling worktree (Repository Constraints) | Several sessions work beside the root checkout. The lane protocol, and every brief for this feature, put each writer in its own clone, which shares no refs, stash, hooks or branch locks with any other session. | A sibling worktree shares the root repository's refs, stash and hooks with every other session's worktree, and a branch checked out in one worktree cannot be checked out in another. A private clone keeps each writer's state its own. |
