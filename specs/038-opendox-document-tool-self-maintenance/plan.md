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

**RULED.** Brett Heap ruled this plan at `6847e99e`, by interactive
multi-choice, every item as recommended (`#656` `6013547504`, 2026-10-06). §
"Ruled answers, the plan ruling" quotes his words, and § "Design decisions,
RULED with the plan" marks each item with the option taken. Implementation
starts on this word (T004, this revision, encodes it).

**Revision: review round 1 folded** (2026-10-05). Two independent read-only
reviews of `6d6911e1`, an Opus analyze and adversarial pass and lane
openXfactory-3's PLANCHECK, are committed verbatim with their disposition tables
in `evidence/analyze-round-1.md` and `evidence/plancheck-lane3-round-1.md`. The
holder's rulings on how to resolve each item conform the plan to ratified text
wherever possible, so Brett's list is shorter: six RULINGS, six readings to
CONFIRM, and the rest as proposed defaults ruled together.

**Revision: the ruling encoded** (T004, 2026-10-06). Brett's answers are
quoted in § "Ruled answers, the plan ruling (`6013547504`)". Three items moved
tier to match the ruling's record: N-7b is now a tier-1 ruling, and OQ-12-12's
and OQ-12-16's readings are tier 2's CF-7 and CF-8. `spec.md` carries I-2 (a)'s
amendment. The two reviewers' re-check of round 1 (every CRITICAL, HIGH and FIX
item landed as worded) left five small fixes, applied here: packs always see the
committed export (data-model.md § Health run), the capability keys' presence
and value kept apart (contracts/cli-http-submit-land.md § `/capabilities`), the
phase-4 `src/` exceptions named (§ Project Structure), finding-id collisions
(contracts/health-finding.md § The id rule), and the single-writer table's rule
for files only one task writes.

**Revision: Copilot's reviews of the ruled revision folded** (2026-10-06).
Copilot's reviews of `2a4a73d1` to `abd28ba2` found gaps the ruled options left
open. Each fix refines a ruled item without taking another option, and all are
listed here so the holder can judge whether any needs Brett's word:
- the run's pack inventory, a newly added pack's first findings as
  `pack-upgrade`, and the baseline scoped to the same corpus (spec FR-010;
  data-model.md § the baseline);
- only a complete, full default-tip run becomes a baseline or measures a
  disappearance, and an accepted id is never a disappearance (FR-010;
  contracts/health-exceptions.md); the once-only re-raise of an uncited
  disappearance is an engine-authored `uncited-disappearance` finding with its
  own id, never itself measured as a disappearance (data-model.md § Baseline
  classes);
- a finding's `identity` is engine-internal, never stored or emitted
  (contracts/health-finding.md), and engine-authored findings carry
  engine-owned identity keys;
- `actions.land` is true for a bound lander or a governed instrument; the
  `land` act's two success shapes (`Landed`, or the instrument's
  `Submission`); and `land`'s remote check reads the chosen remote's PUSH URL,
  refusing several (contracts/cli-http-submit-land.md; R2Q6 (a)'s check);
- `list`, `fix` and `accept` read only the resolved corpus's runs
  (contracts/cli-http-health.md); every repair commit carries a `Finding:`
  trailer, so a landing's citation is read from git between the baseline's
  commit and the run's (data-model.md § Fix draft);
- a run records each pack's exact pin (`pack_pins`) and the commit its packs
  read (`export_commit`), and `fix` re-runs a producer only there, refusing by
  name otherwise (OQ-H15-20's re-obtained patch, data-model.md § Finding); every
  emitted finding carries `evidence`, `{}` when empty;
- a run is `partial` when any selected pack was not evaluated (failed, refused,
  unfetchable, or no live sandbox), so such a run never becomes a baseline;
  `fix` acts only on findings of runs over a commit, a working-state finding
  refused with the commit-and-re-run remedy; and an open batch draft grows only
  at its base (data-model.md § Fix draft);
- a pack's digest tree is defined per source (OQ-H15-12's reading); the pids
  bound is an accepted limit where no cgroup is delegated (OQ-H15-5); no pack
  stderr is stored (OQ-H15-11, refined);
- 9.5 is ticked at T084, after the cut's sync and the publish (ARC-5 (a)'s
  wording; SC-004, FR-025, § Phases); and the F12.1 composition is
  permanent in User Story 3's independent test too, as FR-005 and CF-5 have it;
- stale text brought to the ruling: spec § Assumptions lets #1144 archive with
  F9.2 open (ARC-5 (a)); the checklist records the direction arc as ruled; and
  T003, if dispatched, dispositions its own round before the first realization
  PR, since T004 is done;
- one exceptions entry per finding id: a repeated `accept` and a hand-repeated
  id are refused by name (contracts/health-exceptions.md).

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
  and the deadline confirmed (ARC-Q4 (a)). Tasks T070–T077 schedule it. Its
  composed-CI half, T073, is #1144's requirement-9 work and runs as #1144's
  (lane openXfactory-3's split condition 3).
- **The schemas come first in phase 5.** Three openDox-spec schemas, then the
  openDox root's spec pin and one more `dox-v1.y` minor bundle on Brett's cut
  word (T060), then the copies in openDox-code at the pinned commit (R2Q22 (a);
  release 1's order, research R7).
- **The close.** AT-R2, HTTP half in CI and browser half on the host
  (R2Q24 (a)); the ticks of the 37 release-2 boxes and of 11.0, 11.1 and F11.1
  (T082); the cut's pin sync through the aggregation (T083); and LAST,
  `opendox` 0.2.0 on PyPI on Brett's publish word (R2Q23 (a)), followed by 9.5's
  tick (T084).

**The first act** is T005: ONE bookkeeping batch (batch Q) in plan 034's T007
form, under a Rule 6 window, whose contents are tier 2's confirmation CF-2. It
lands before phase 4's first checkpoint.

**What Brett ruled** (§ "Design decisions, RULED with the plan"; `6013547504`),
every item as recommended:
- **Tier 1, seven RULINGS**: R-1 (with W-1), W-1, ARC-5 (with OQ-038-2), I-2,
  N-6, ARC-1 and N-7b.
- **Tier 2, eight readings CONFIRMED**: I-1, batch Q's contents (I-3, N-5 and
  N-12 merged), H-1, H-2, F12.1's permanent composition, "optionally on
  commit", the remote `submit` chooses, and `gh` hidden from PATH.
- **Tier 3, 52 defaults**, ruled together: the rest of the 34 deferred items,
  the smaller repair questions, the arc's other items, and this plan's own,
  each conformed to ratified text by review round 1.
- **The two-lane split** (§ "Two lanes").

§ "Conflicts found" reports where the answers, #1144 and the code disagree, and
where each was ruled.

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
The store holds no document and no patch text, and stays disposable (14.3; R2Q25 (a)). Exceptions live in
git, in `health/dispositions.yaml`; the pack manifest in `health/packs.yaml`;
the governance declaration in `.opendox/governance.yaml`, read from `main`'s
tip (R2Q7 (a)).

**Testing**: pytest in openDox-code (`tests/`, `tests_runtime/`, the whole
suite in the required `validate` job, `EXPECT_SKIPPED` 11); 12.5's 16 governed
suites run composed in openXdox-code against a pinned openxFactory (R2Q8 (a),
ARC-Q2 (a)); #1144's falsifiers F12.1, F12.2, F6.1, F14.1, F15.1 and F11.1,
each as amended, quoted in evidence, F15.1's shell block in the required job
(T067); AT-R2 (R2Q24 (a)).

**Target Platform**: the local plane on Linux, macOS and any platform openDox
already serves. Packs run only where the reference sandbox is proved live:
Linux with `bwrap` and unprivileged user namespaces. macOS gets health with
no packs and one finding that says why (R2Q16 (a)). Hosted installs refuse the
health verbs and view by name (R2Q15 (a)).

**Project Type**: a CLI and loopback web application with library seams,
spread over a two-leg product (openDox root, openDox-code, openDox-spec) and
its governed descendant (openXdox root, openXdox-code), consumed by
openxFactory and the xFactory aggregation.

**Performance Goals**: none beyond #1144's. A pack has a per-pack budget (60 seconds by default,
capped at 600) and engine-declared resource bounds; a bound hit is a finding
against that pack (15.6, OQ-H15-5).

**Constraints**: no landing merges automatically (SC-007); `land` pushes
nothing; evidence carries locators, never document text (R2Q25 (a)); packs
see only the exported tree and are model-free (R2Q19 (a), R2Q20 (a)); 12.5's
16 suites are edited only through the allow-list (R2Q8 (a)); openxFactory's
arc edits stay on 11.1's surfaces; `EXPECT_SKIPPED` stays 11 (R2Q17 (a)).

**Scale/Scope**: 37 release-2 boxes (Group 6: 4; Group 12: 11; Group 14: 10;
Group 15: 12), the four arc-close boxes, and F9.2 through the direction arc.
Seven product repositories, one codexFactory spec amendment (R2Q6 (a)), one
new OpenSpec change (ARC-Q3 (a)), and the aggregation's pin syncs. 79 tasks.

No item of the Technical Context is NEEDS CLARIFICATION: every behavioural
question is answered (R2Q1–R2Q25, ARC-Q1–ARC-Q4), and every design question
was ruled with the plan (`6013547504`).

## Constitution Check

*GATE: checked before planning, and re-checked after the design (Phase 1
below). This revision is the first plan of feature 038. Re-checked at T004, the
revision that encodes Brett's ruling (`6013547504`): no row changes.*

| principle | status | how this feature meets it |
|---|---|---|
| I. Contract-first, domain-neutral core | PASS | openxFactory gains only host wiring, pin pairs, `edits[].note` annotations and the named composition tests 11.1 admits. Neutral contracts land in openDox-spec (R2Q22 (a)'s three schemas, T040), never in openxFactory. No domain vocabulary enters openDox: the health families, classes and labels are neutral, and a domain pack's labels arrive through the display facet (15.3). |
| II. OpenSpec before implementation | PASS | Everything here realizes the RATIFIED #1144 (`5815412869`). The answers' changes to #1144's falsifiers and task lines land as bookkeeping in plan 034's T007 form (T005, batch Q; T082 at the close). The `doc_health` direction arc's realization gets its OWN OpenSpec change (ARC-Q3 (a); T070), ratified on Brett's word (T071) before any of its realization slices start. Feature 007's four exceptions are amended in codexFactory's own spec on R2Q6 (a)'s word (T008) before the guard moves (T013). |
| III. Document lifecycle | PASS | Every file of this feature carries `Status: draft`; evidence files will carry `Status: record`, as feature 034's do. #1144 is `Status: ratified`. The arc's change is authored `Status: draft` and ratified on Brett's word. |
| IV. Schema and artifact discipline | PASS | No committed file names a host path: commands resolve scratch space with `W=$(mktemp -d)`, and lane 3's inventories are cited by their workspace-relative path (`lane-coord-034/r2/…`). No credential is stored: a credential-bearing remote is pushed with every report and message redacted (12.1a; OQ-12-11), and nothing about it is stored. Every YAML file the product reads carries `schema_version` and `kind` (contracts/). **The README document index** entry for feature 038 (`README.md:87`) links the plan, research, data model, AT-R2 quickstart, tasks, contracts and both review-round evidence files, from this revision (D1, ADV-28, ADV-34). Every evidence task keeps it current. The entry sits outside the OpenSpec Records block, so it needs no Rule 6 window. |
| V. Validation gates | PASS for this PR | This PR touches no `openspec/` path (`git diff --name-only` against `origin/main` lists none under `openspec/`; research R0). It touches `README.md`'s Documentation entry, outside the OpenSpec Records block. The pinned `scripts/validate-openspec-cli-pin.py --all` gate is run before each push (the PR body quotes it). Batch Q (T005), T070, T071, T076, T077 and T082 do touch `openspec/changes/`; each records its own gates against the `main` it lands on. Implementation evidence is falsifier output, quoted. |
| VI. Versioned releases | PASS | R2Q22 (a) adds three openDox-spec schemas, so the openDox root moves its spec pin and cuts ONE more `dox-v1.y` minor bundle, `dox-v1.2`, on Brett's cut word (T060, straight after T040, as release 1's `dox-v1.1` was cut, RULED `5894235642`), under a batch-G style addendum at 9.5 (batch Q); the copies follow the pin (research R7). R2Q23 (a) publishes `opendox` 0.2.0, tagged `v0.2.0`, under a batch-O style addendum, on Brett's publish word (T084). The arc's change cuts no bundle unless its openXdox-spec delta needs one (ARC-3). |
| VII. Fail-closed authority | PASS | No merge without a human act: `land` needs a confirmation capability bound to the branch and its head, single-use (12.6a). `governed` with no instrument refuses `land` by name; `unknown` refuses. Packs run only in a sandbox proved live by a per-run canary; with no sandbox, packs do not run and one finding says why (R2Q16 (a)). A hosted install refuses the health surface by name (R2Q15 (a)). A dirty served checkout holding `main` is never moved (ADV-08). A git-URL pack source is fetched over https or ssh only, never with a credential (OQ-H15-14). Evidence and messages carry locators only, and the store holds no patch text (R2Q25 (a)). |
| Workflow: *"material ambiguities MUST be resolved before planning"* | **PASS** | Brett answered all 25 round-1 questions (`6003486656`) and the four arc questions (`6003918488`). Round 2 was empty (`clarify-questions.md` § "Round 2"). Brett ruled the plan's design decisions in three tiers, every item as recommended (`6013547504`), and T004 records the ruling (FR-025). |
| Workflow: *"`/speckit.analyze` MUST report no critical findings before implementation"* | Round 1's CRITICALs applied and re-checked; a fresh analyze (T003) is the holder's call | Round 1's analyze (`evidence/analyze-round-1.md`) found one CRITICAL under the skill's rubric (D1, the README index) and three under its brief's (ADV-01 to ADV-03); all four were applied at `6847e99e`, as its disposition table shows. Both reviewers re-checked that revision before Brett ruled: every CRITICAL, HIGH and FIX item landed as worded (`6013547504`); their five small remaining fixes are applied at T004. That re-check is not a fresh `/speckit-analyze` run. Brett's ruling starts implementation on his word (`6013547504`); whether a fresh analyze of the ruled revision runs before the first realization PR lands is the holder's call, recorded at T003. |
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
├── research.md             # R0–R13: measurements, the inventories and reviews credited, the ruled arc
├── data-model.md           # entities, fields, state transitions
├── contracts/
│   ├── health-finding.md            # the finding's neutral shape (openDox-spec schema 1)
│   ├── health-packs-manifest.md     # health/packs.yaml (openDox-spec schema 2)
│   ├── health-exceptions.md         # health/dispositions.yaml (openDox-spec schema 3)
│   ├── cli-http-submit-land.md      # submit, land: CLI verbs, routes, /capabilities
│   └── cli-http-health.md           # health run|list|fix|accept: CLI verbs, routes
├── quickstart.md           # AT-R2: the HTTP half (CI) and the browser half (host)
├── tasks.md                # 79 tasks, T001–T093
└── evidence/               # Status: record
    ├── analyze-round-1.md          # the Opus review of 6d6911e1, verbatim, with its dispositions
    └── plancheck-lane3-round-1.md  # lane openXfactory-3's PLANCHECK, verbatim, with its dispositions
```

### Source code: the repositories release 2 lands in

| tag | repository | what release 2 changes there | merge method |
|---|---|---|---|
| `[oDc]` | opensoft/openDox-code | Group 12's ports, verbs, routes and view controls; the feature-007 guard (R2Q6 (a)); the health package (store migration, families, engine, fix loop, exceptions, view); the check-pack contract, manifest, sandbox, patch validator and engine integration; the three digest-checked copies in `src/opendox/contracts/`; `validate.yml` (R2Q17 (a), and F15.1's shell block); the `0.2.0` bump; the arc's re-authored `lines` slice (T072) | squash or merge, never rebase |
| `[oXc]` | opensoft/openXdox-code | U-1 to U-5 and U-7 (the repair of 12.5's reds, no protected edit outside an entry; nothing vendored into its copy record); U-8's pin; U-9's composed workflow, permanent and required (ARC-Q2 (a), N-7b); requirement 9's composed declarations (T073); the arc's seams and retargets (T074) | squash or merge, never rebase |
| `[oD]` | opensoft/openDox (root) | the code pin per phase; the spec pin and the `dox-v1.2` bundle on Brett's cut word (R2Q22 (a); T060, early in phase 5); README: the governance declaration, `submit`, `land`, the push routes, `health`, and the 0.2.0 install line | squash or merge, never rebase |
| `[oX]` | opensoft/openXdox (root) | the code pin and `contracts/opendox-pin.yaml` per phase | squash or merge, never rebase |
| `[oDs]` | opensoft/openDox-spec | the three health schemas (R2Q22 (a)) | squash or merge, never rebase |
| `[oxF]` | opensoft/openxFactory | pin pairs, host wiring (11.1 surfaces), `edits[].note`s, evidence and bookkeeping (no `Arc:` trailer), batch Q, the arc's OpenSpec change | squash or merge, never rebase |
| `[cxF]` | codeXfactory/codexFactory | feature 007's spec: the four named exceptions (R2Q6 (a)); required checks `validate` and `lane-line`, one approving review (research R13) | **merge commits only** |
| `[xF]` | opensoft/xFactory (aggregation) | the routine pin-syncs after openxFactory landings, and the cut's sync with the three-way parity | as its owner lands pin-syncs |

openDox-code's new files (the planned paths; each is owned by exactly one slice,
tasks.md § "Writer slices"):

```text
src/opendox/
├── session_pr.py              # + SubmissionPort, Submission, LocalGitSubmissions, NoSubmissionTarget (T011)
├── submission_push.py         # the push helper factored from runtime/repository_act.py (T011, CF-7)
├── landing.py                 # LandingPort, Landed, MergeConflict, repository_governance, the lander (T012)
├── landing_confirm.py         # the confirmation capability and its two issuers (T012)
├── cli_branch_actions.py      # the submit and land verbs, default-profile contributions (T015, T016)
├── serve_branch_actions.py    # the submit, land-nonce and land routes, contributed through the default profile (T015, T016)
├── contracts/copies.yaml, schemas/   # + the three health copies at the root's pinned spec commit (T041 → T047 → T054)
├── health/
│   ├── __init__.py
│   ├── families.py            # the neutral families (T044)
│   ├── engine.py, baseline.py # the engine, the baseline classes (T046)
│   ├── cli.py                 # health run|list|fix|accept (T046 → T053 → T054)
│   ├── applier.py             # the fix loop (T053)
│   ├── exceptions.py          # health/dispositions.yaml (T054)
│   └── routes.py              # the Health view's routes, contributed through the default profile (T057)
├── runtime/health_store.py    # the store (T042)
├── health_contract.py         # THE contract module (N-3): U-0's finding vocabulary (T041), then G15-A's pack protocol (T045)
├── check_pack_manifest.py     # health/packs.yaml, the pin (T047)
├── check_pack_sandbox.py      # bwrap, the probe and canary, the mount set (T048); bounds measured in T056
├── check_pack_shim.py         # the in-sandbox shim (T048)
├── check_pack_patch.py        # the patch validator (T049)
├── check_pack_engine.py       # the engine integration (T056)
└── web/views/
    ├── branch-actions.js      # the submit control and the land confirm control (T015, T016)
    └── health.js, health-model.js   # the Health view (T057)
migrations/0003_health.sql     # runs and findings, with 15.7's provenance columns; no patch column (T042)
tests/fixtures/health-corpus/  # 14.9 (T043)
tests/fixtures/pack-corpus/    # 15.6a (T055)
```

**Structure Decision**: release 2 adds no repository (R2Q22 (a): "No
repository joins"). Product code lands in openDox-code under new modules beside
the existing seams, never inside the `doxbench-*.js` files FR-037's sentinels
guard (OQ-12-14), and never in the three pinned `session_pr.py` classes
(`test_session_snapshot.py:893-916`). The verbs `submit`, `land` and `health`
are contributions of openDox's DEFAULT profile, and so are their routes and
the `/capabilities` keys derived from those routes, so a host profile that
replaces it carries none of them: the hosts' help goldens and `/capabilities`
payloads do not move (R2Q3 (a); decision N-2; ADV-14). In phase 4,
openXdox-code changes its tests, its pin and its workflows (no protected edit
outside an allow-list entry), and two `src/` files: T021's
`src/openxdox/gate_console.py` (the schema-source seam) and T023's
`src/openxdox/web/views/swb-session.js` (two one-off nodes). Its `src/` otherwise
changes only in the arc's realization (T074). openxFactory changes only on
11.1's surfaces.

## Phases, and where every release-2 box closes

The box census at this branch's base, `ce64afc9` (research R0), reads 125
boxes in #1144's `tasks.md`: 74 `[x]`, 42 `[ ]` and 9 `[~]`. The 42 open boxes
are the 37 release-2 boxes, the four arc-close boxes, and F9.2.

| phase | boxes that CLOSE in it | exit (all quoted in the phase checkpoint task) |
|---|---|---|
| 0 | none | the plan ruled (T004); batch Q landed (T005), before phase 4's checkpoint; feature 007 amended (T008) before T013 |
| 4 | 12.1, 12.1a, 12.2, 12.3, 12.4, 12.4a, 12.5, F12.1, 12.6, 12.6a, F12.2 (11) | F12.2 exits 0 alone with `gh` absent (20 named nodes); F12.1 exits 0 composed with 174 reds repaired and the oracle printing `ok: … each entered and holding`; interim F11.1 `requirement 1 holds` (T033; SC-001, SC-003) |
| 5 | 6.1, 6.1a, 6.2, F6.1 (4); 14.1–14.9, F14.1 (10); 15.1, 15.1a, 15.1b, 15.2, 15.2a, 15.3, 15.4, 15.5, 15.6, 15.6a, 15.7, F15.1 (12) | F6.1, F14.1 and F15.1 exit 0 as batch Q amends them; F15.1's shell block and its 24 nodes run in the required `validate` job with the sandbox proved live (T067, T058); 12.5 still green composed at phase 5's pin; interim F11.1 (T066; SC-002, SC-003) |
| close | the ticks of all 37 (T082), after AT-R2 (T080, T081; SC-008) | AT-R2 both halves; bookkeeping under Rule 6; the cut's pin syncs (T083); then the 0.2.0 publish, LAST (T084) |
| every phase, ticked at the ARC's close (T082) | 11.0, 11.1, F11.1 | interim F11.1 after each phase (T032, T065); final F11.1 at T082 (tier 1's ARC-5) |
| every phase, ticked LAST, after the cut's sync (T083) and the publish (T084) | 9.5 | ticked at T084, never at T082 (ARC-5 (a), as worded at T004) |
| beside phase 5, the arc's own change | F9.2 (outside the 37) | F9.2 re-run after the arc's realization lands (T076), recorded as tier 1's ARC-5 (a) ruled |

Phase 4's boxes tick at T082 with every other release-2 box, as release 1's
did at plan 034's T097. Each checkpoint quotes its falsifiers; the tick is
bookkeeping.

## Dependency graph

```text
T001–T009 (holder: claims, base, analyze, the plan ruling, batch Q, the arc ask [done], the arc encoding [done], feature 007, the lane split)
                          │
DAY ONE (the plan ruled)  T010 [oDc] R2Q17's required-check change (CI owner)        T070 [oxF] author the arc's change
                          T020–T024 [oXc] U-1..U-5 (T021 after T020; T022 after T021)
                          T025 [oDc] U-6 (W-1 ruled)    T040 [oDs] the three schemas → T060 [oD] spec pin + dox-v1.2 (Brett's cut word)
                          T011 [oDc] P4-A → T012 + T013 [oDc] P4-D1 (T012 after T011 on repository_act.py; T013 after T008)
 PHASE 4  [oDc]  T011 → T014 (P4-B) → T015 (P4-C; also after T025) → T016 (P4-D2; also after T012, T013)
                 T017 (floors; after T010–T016, T025)
          [oD]   T018 (README) after T016;  T027 root pin after T017, T018
          [oXc]  T026 (U-7) after T020, T005 (H-2, R-1);  T028 (U-8a pin) after T027;  T029 (U-9) after T020–T026, T028
          [oX]→[oxF]  T030 (U-8b consumer pins, host wiring incl. the receipt schema source, T019's proof) after T029
          [oxF]  T031 (F12.2) after T027, T005;  T032 (F12.1 composed, interim F11.1) after T029, T030
                 → checkpoint T033 (after T005)
 PHASE 5  (openDox-code from T027: tier 1's N-6 (a), ruled)
          W1  T041 (U-0; after T060)  T042 (HA-1)  T043 (HA-3)
          W2  T044 (HA-2)  T045 (G15-A; after T041)
          W3  T046 (HA-5)  T047 (G15-B; after T041's copy)  T048 (G15-C)  T049 (G15-D)  T050 (G15-H; after T045)   T051 floors per wave (CI owner)
          W4  T052 (HA-4)  T053 (HA-6)  T054 (HA-7; after T047's copy and T053)  T055 (G15-G; after T048)  T056 (G15-E; bounds measured)   T059 [oxF] facet follow-on, if measured
          W5  T057 (HA-8; after T052)  T058 (G15-I2)
          W6  T067 (F15.1's shell block in the required job; CI owner)  →  T061 [oDc] 0.2.0 bump  →  T062 [oD] root code pin  →  T063 [oXc] pin, composed re-run
              →  T064 [oX][oxF] consumer pins + host wiring (then composed_host_pin advances)  →  T065 [oxF] evidence (F6.1, F14.1, F15.1, interim F11.1)  →  checkpoint T066
              (T063 also after T028, and T064 after T030: phase 4's pins land first, N-6 (a))
          T068 [oDc] the 26.04 runner measurement (R2Q17), non-gating
 REQUIREMENT 9 FOR openXdox-code (ARC-Q2 (a); #1144's work, lane openXfactory-3, NOT gated on T071)
          T073 [oXc] composed declarations, after T029 and T005; re-runs after each composed_host_pin advance (T030, T064, T075)
 BESIDE PHASE 5: the arc's own change (ARC-Q3 (a); gates neither release 2's close nor #1144's archive)
          T070 [oxF] author → T071 ratify word → T072 [oDc] lines slice (opportunistic: rides T061 only if already landed; T061 never waits)
          T074 [oXc] seams, retargets, respellings (after T071, T072's pin, T021, T073)
          T074 → T075 [oxF] host registers the seams, with its pin pairs → T076 [oxF] F9.2 re-run (ARC-5 (a)) → T077 archive + topic exit (Rule 6)
 CLOSE    T080 [oDc] AT-R2 HTTP (CI; after T066) → T081 [oxF] AT-R2 browser (host) → T082 [oxF] ticks + arc close (Rule 6)
          → T083 [xF] the cut's pin sync (three-way parity) → T084 [oDc][oD] 0.2.0 publish, on Brett's word: LAST
 EVERY PHASE  T090 pins · T091 trailer · T092 notes · T093 interim F11.1 (run as T032, T065, and finally at T082)
```

## Parallel slices, and the files only one writer may touch at a time

Writers run in parallel when they share no file. The surfaces below are
SINGLE-WRITER: at most one open slice edits each, and a slice that needs one
rebases onto the previous slice's landing before it opens. Every order below is
also encoded in the later task's `After:` line (ADV-23). A change to an order is
the holder's act, recorded in the PR that changes it.

**A file that only one task ever writes needs no row:** that task's Files line
is its record (T021's new `tests/test_gate_console_schema_source.py`, for one,
and every other new file named in a single task). A row marked "alone" is kept
only where another task reads, runs or relies on the file, so its one writer is
a constraint other slices must respect (re-check of review round 1, lane
openXfactory-3).

| single-writer file | slices, in order |
|---|---|
| openDox-code `.github/workflows/validate.yml` | T010 (R2Q17: `ubuntu-24.04`, bubblewrap, the AppArmor sysctl, the live proof, fail-not-skip under `CI`; `EXPECT_SKIPPED` stays 11) → T017 (phase 4's floors) → T051 (phase 5's floors, once per wave) → T067 (F15.1's shell block as a step) → T080 (AT-R2's `acceptance` job). One CI-owner slice across release 2 (decision N-4) |
| openDox-code `src/opendox/session_pr.py` | T011 (new names only; the three pinned classes untouched) → T012 (the re-exports 12.6a requires: `LandingPort`, `repository_governance`) |
| openDox-code `src/opendox/runtime/repository_act.py` | T011 (the push core factored out; the call site) → T012 (only if its repository-creation audit edits `:982`'s `init --bare`) |
| openDox-code `src/opendox/session_git.py`, `tests/test_session_git.py` | T013 alone (R2Q6 (a)) |
| openDox-code `src/opendox/serve.py` | T014 (`submission_factory`) → T015 (the submit route's capability derivation) → T016 (`landing_factory`, `actions.land`) → T052 (HA-4's registration lines) → T057 (the `health` block's derivation) |
| openDox-code `src/opendox/cli.py` | T014 (`_submission_port`) → T016 (`_landing_port`) → T046 (HA-5: the `health` group's local wiring) → T052 (HA-4's registration lines) |
| openDox-code `src/opendox/default_profile.py` | T015 (`submit`; the submit route in `ROUTE_EXTENSIONS`, its mixin in `HANDLER_CONTRIBUTIONS`) → T016 (`land` and its routes) → T046 (`health` verbs) → T057 (the health routes) |
| openDox-code `src/opendox/health_contract.py` (THE contract module, N-3) | T041 (U-0, lane 4) → T045 (G15-A, lane 3: the pack protocol, appended). A cross-lane hand-off at T041's landing |
| openDox-code `src/opendox/contracts/copies.yaml`, `src/opendox/contracts/schemas/`, `src/opendox/contracts/__init__.py`, `tests/test_validator_input_set.py` | T041 (the finding shape; the record's `commit` moves to the spec commit T060 pins) → T047 (the packs manifest, lane 3) → T054 (the exceptions file). All three copy at T060's pinned commit, in this FIXED order (lane 3's split condition 2) |
| openDox-code `src/opendox/health/cli.py` | T046 (the parser, frozen to 14.5's shapes plus `--local` and `--class`) → T053 (`fix`'s dispatch) → T054 (`accept`'s dispatch) |
| openDox-code `src/opendox/workbench.py` | T052 alone |
| openDox-code `src/opendox/branch_session.py` | T016 alone (R2Q5 (a)) |
| openDox-code `src/opendox/web/app.js`, `web/index.html` | T015 → T016 → T057 |
| openDox-code `src/opendox/web/views/staging-workbench.js`, `staging-workbench-model.js` | T025 alone (U-6; the model too, W-1 (A), ruled) |
| openDox-code `src/opendox/display_profile.py`, `web/views/display.js` | T050 alone (G15-H), with a guard that the model's inlined tables equal `display.js`'s (W-1 (A), ruled) |
| openDox-code `tests/fixtures/web_boundary_census.yaml`, `tests/test_web_boundary.py` | T025 → T015 → T016 → T057 |
| openDox-code `migrations/0003_*.sql` and the five `tests_runtime/` suites it moves | T042 alone |
| openDox-code `tests/fixtures/health-corpus/**` | T043 → (read-only copy by T055; a later change re-runs T055's digest test) |
| openDox-code `tests/test_check_packs.py` | T058 alone (the 24 named nodes) |
| openDox-code `pyproject.toml` | T048 (if the sandbox needs package data) → T055 (fixture package data, if any; After T048) → T061 (the 0.2.0 bump, the LAST package-changing landing before T062) |
| openDox root `README.md` | T018 (the declaration, `submit`, `land`, the two push routes) → T062 (the `health` section and its hook line) → T084 (the 0.2.0 install line) |
| openDox root spec pin, `contracts/manifest.yaml`, `CHANGELOG.md`, the `dox-v1.2` tag | T060 alone (early in phase 5) |
| openDox root `code` gitlink, `contracts/code-pin.yaml` | T027 (phase 4) → T062 (phase 5); then, only if the arc's `lines` module lands after the 0.2.0 bump, the arc's own root commit (ARC-6) |
| openXdox-code `tests/conftest.py`, `tests/test_host_plane.py` | T020 (U-1) → T021 (the gate console's schema-source registration line) → T073 (the rail registration) → T074 (the arc's governed implementations, until T075) |
| openXdox-code `src/openxdox/gate_console.py` | T021 (U-2: the packaged read and the schema-source seam) → T074 (the arc's retarget) |
| openXdox-code `src/openxdox/contracts/copies.yaml` | NO writer in release 2 (ADV-10; `test_packaged_validator.py:81-92`) |
| openXdox-code `.gitignore`, `scripts/composed_placements.py` | T022 alone |
| openXdox-code `scripts/ideation_dashboard/session_git.py` | T024 alone (no `__init__.py`; ADV-39) |
| openXdox-code `src/openxdox/generator.py`, `corpus_root.py`, `cli_gate.py`, `gate_routes.py`, `snapshot_registry.py`, `completeness.py`, `round_trip.py` | T074 alone |
| openXdox-code `tests/protected_suite_respellings.yaml`, `scripts/protected_suites.py` and the five protected files U-7 enters | T026 alone in phase 4 (entries chain by blob); a later edit to a protected suite adds its entry in its own PR |
| openXdox-code `tests/declared_exclusion.yaml` | T073 (entries become declared composed integration tests, with count and reason) → T074 (the `doc_health` reason empties) |
| openXdox-code `tests/test_dependency_direction.py` | T074 alone |
| openXdox-code `pyproject.toml` | T028 (phase 4's `opendox @` pin) → T063 (phase 5's) → T074 (only if T072 lands after T061: the arc's own pin, ARC-6) |
| openXdox-code `.github/workflows/composed.yml` | T029 (U-9: the workflow, recursive submodules) → T073 (the rail, contracts and governed-behaviour files) → T074 (F9.2's code removals) |
| openXdox-code `tests/composed_host_pin.yaml` | T029 (created) → the openXdox-code PR after T030 (advance) → the PR after T064 (advance) → the PR after T075 (advance). T073 re-runs after each advance |
| openxFactory pin pairs and host wiring (`scripts/opendox_host.py`, `tests/domain_profile/`) | T030 (phase 4, with the receipt schema source) → T064 (phase 5) → T075 (the arc's seams) |
| openxFactory `README.md` (feature 038's Documentation entry) | this revision → T004 → each evidence task in landing order (T002, T031–T033, T065, T066, T076, T081, T082); T070 and T077 touch only the OpenSpec Records block, under Rule 6. One open edit at a time, by the holder |
| openxFactory `openspec/changes/add-neutral-product-standalone-operability/` | T005 (batch Q) first; then T082 (the release-2 ticks and the arc-close boxes but 9.5) and T076 (only while #1144 is active, as ARC-5 (a) ruled), in either order but never both open at once; then T084's tick of 9.5, last; each under its own Rule 6 window |
| the arc's own change directory (`openspec/changes/<ARC-2>/`) | T070 → T071 → T077 |
| codexFactory `specs/007-workbench-branch-sessions/spec.md` | T008 alone |

## Two lanes: the split (RULED on `6013547504`; T009)

Lane openxfactory-4 is the coordinator. It claims for itself, writes its own
slices, and LANDS EVERY PR, its peer's included (the landing kit, Rule 6
windows, the register). Lane openXfactory-3 is the peer, with its own writers;
it claims its slices on `#656` (T001) and hands each PR to the coordinator
when it is READY. Neither lane opens a PR on a file the other lane's open slice
owns (the single-writer table above).

Lane openXfactory-3 ACCEPTED this split in its PLANCHECK (2026-10-05T22:42:30Z),
on three conditions, each applied here: (1) T021 before T022; (2) T054 After
T047, with openDox-code's copy record in the single-writer table; (3) T073 moves
out of the arc's section and is #1144's requirement-9 work, with #1144's `Arc:`
value, staying lane 3's and not gated on T071.

| lane | slices (tasks) | why this lane |
|---|---|---|
| **openXfactory-3 (peer)** | **Phase 4's repair, P4-F:** U-1 (T020), U-2 (T021), U-3 (T022), U-4 (T023), U-5 (T024), U-6 (T025), U-7 (T026), U-9 (T029). **Requirement 9 for openXdox-code:** T073 (ARC-Q2 (a)'s composed declarations). **Phase 5's pack track:** G15-A (T045), G15-B (T047), G15-C (T048), G15-D (T049), G15-G (T055), G15-E (T056), G15-I2 (T058). **Re-measures on request** (T002's composed re-run). | Lane 3 wrote R2-INV-P4F (every red node mapped, its slice outline) and Part B of R2-INV-HEALTH (Group 15, the sandbox survey). Its slices are openXdox-code tests and workflows and the self-contained `check_pack_*` modules, which share no file with lane 4's open slices except in the fixed orders above. |
| **openxfactory-4 (coordinator)** | **Phase 0:** T001–T009. **Phase 4's product:** T010 (the CI owner, all five of its edits: T010, T017, T051, T067, T080), P4-A (T011), P4-D1 (T012, T013), P4-B (T014), P4-C (T015), P4-D2 (T016), README (T018), the host-unchanged proof (T019). **Pins and evidence:** T027, T028, T030, T031, T032, T033; T060–T066, T068. **Phase 5's health track:** T040, U-0 (T041), HA-1 (T042), HA-3 (T043), HA-2 (T044), HA-5 (T046), G15-H (T050), HA-4 (T052), HA-6 (T053), HA-7 (T054), HA-8 (T057), T059 if needed. **The arc's change (ARC-Q3 (a), owned here):** T070–T072, T074–T077. **The close:** T080–T084. **Every phase:** T090–T093. | The coordinator holds every surface that more than one phase touches (`serve.py`, `cli.py`, `default_profile.py`, `validate.yml`, the pins, the README entry, `openspec/changes/`), so no cross-lane hand-off happens on a single-writer file mid-phase. ARC-Q3 (a) names lane openxfactory-4 the arc's owner. |

**Cross-lane hand-offs, each at a landing, never mid-slice:** the census
fixture (T025, lane 3 → T015, lane 4); openXdox-code's `tests/conftest.py`
(T020, T021 and T073, lane 3 → T074, lane 4); `gate_console.py` (T021, lane 3 →
T074, lane 4); openXdox-code's `composed.yml` (T029 and T073, lane 3 → T074,
lane 4); `health_contract.py` (T041, lane 4 → T045, lane 3); openDox-code's copy
record (T041, lane 4 → T047, lane 3 → T054, lane 4); openDox-code
`pyproject.toml` (T048 and T055, lane 3 → T061, lane 4).

## The critical path

Inferred from the task graph and lane 3's sizing, not measured (ADV-33 corrected
phase 5's path).

```text
T004 (ruling: R-1, W-1, H-2 among it) → T020 (U-1) → T026 (U-7) ─┐
T011 → T014 → T015 → T016 → T017 → T027 → T028 ───────────────────┴→ T029 (U-9) → T030 → T032 → T033
PHASE 5, two poles that join at T061 (every package-changing openDox-code landing precedes it):
  health:  T040 → T060 (Brett's cut word) → T041 → T044 → T046 → T053 (also after T016) → T057 ─┐
  packs:   T041 → T045 → T047 → T048 → T056 → T058 → T067 (F15.1's shell block, live sandbox) ┴→ T061 → T062 → T063 → T064 → T065 → T066
CLOSE:   T066 → T080 → T081 → T082 → T083 → T084 (the publish, last)
```

- **Phase 4's long pole is P4-F (U-1 → U-7 → U-9)**, as lane 3's inventory says
  (R2-INV-12 § "Proposed phase-4 task outline"; R2-INV-P4F § "Slice
  outline"). It starts the day the plan is ruled. U-7 also waits on H-2 and,
  for its admitted part, on R-1; so R-1 and H-2 are on the critical path, and
  W-1 and H-1 gate U-6 and U-5 off it. Whether P4-F is longer than the product
  chain is unmeasured.
- **Phase 5 has two poles.** The health track ends in the view (T057); the
  pack track runs through the sandbox (T048), which this plan calls the
  riskiest slice, to F15.1's shell block in the required job (T067). Brett's cut
  word (T060) is on both, because every copy waits for the root's spec pin.
  R2Q17's CI provisioning (T010) moves to DAY ONE so its failure modes surface
  before T048 is written.
- **The overlap (tier 1's N-6, ruled (a)).** Phase 5's openDox-code slices land
  once T027 has pinned phase 4's openDox-code commit, without waiting for T033.
  That shortens the path by T028–T033.

**What starts on the ruling (`6013547504`):** T005 (batch Q), T008
(codexFactory), T009 (claims), T010 (CI), T011 (P4-A), T013 (after T008),
T020–T024 (U-1 to U-5; T021 after T020 and T022 after T021, lane 3's condition
1; T024, H-1 confirmed as CF-3), T025 (U-6, W-1 ruled for its model part), T040
(the three schemas, from `contracts/`), T060 as soon as T040 lands, and T070
(authoring the arc's change). T012 starts beside T011 and lands after it.

## Scheduled acts the brief names, and where each sits

| # | act | task(s) | when |
|---|---|---|---|
| 1 | R2Q9 (a)'s seven amendments, ONE batch in plan 034's T007 form, under Rule 6 | T005 (batch Q; its full contents are tier 2's CF-2) | the FIRST act; lands before T033 and before any task whose falsifier reads an amended line (T026, T031, T032, T052, T058, T065, T067, T073) |
| 2 | R2Q6 (a)'s four feature-007 exceptions | T008 (codexFactory spec, merge commit only; required checks `validate` and `lane-line`) → T013 (openDox-code guard and pins) | T008 day one; T013 lands with T012, after T008 |
| 3 | R1Q6 (d): the `doc_health` direction arc decided before F12.1 needs the 16 suites | T006 (DONE: ruled on `6003918488`); T007 (DONE: encoded here) | The latest point it could have been asked was the claim of U-9 (T029), whose composed run is F12.1. It was asked and ruled before this plan was ruled, so phase 4's checkpoint waits on nothing |
| 4 | R2Q17 (a)'s required-check change in openDox-code's `validate.yml` | T010, the CI owner; F15.1's shell block in the same required job (T067) | T010 day one, before any phase-4 or phase-5 slice adds a test |
| 5 | R2Q22 (a): three openDox-spec schemas, one more `dox-v1.y` minor, digest-checked copies | T040 (schemas) → T060 (the root's spec pin, manifest and the `dox-v1.2` cut, on Brett's cut word) → T041 → T047 → T054 (copies at the pinned commit) | T040 day one; T060 straight after it, early in phase 5 (release 1's order: 034's T053 then T057); batch Q carries the 9.5 and 7.1 addenda |
| 6 | R2Q23 (a): `opendox` 0.2.0, tag `v0.2.0`, LAST | T061 (the bump; never waits for the arc) → T084 (the publish, on Brett's word after AT-R2) | T084 is the last task of the release |
| 7 | R2Q24 (a): AT-R2, HTTP half in CI, browser half on the host | T080, T081; quickstart.md | after T066 |
| 8 | The pin sync across openxFactory and the aggregation, with the three-way openDox/openXdox parity | T030, T064 (openxFactory per phase), the routine aggregation syncs after each openxFactory landing, and T083 at the cut | T083 after T082 |
| 9 | The arc-close boxes 9.5, 11.0, 11.1, F11.1, and plan 034's T090–T093 | T090–T093 (every phase); ticked by T082, except 9.5, ticked by T084 after the sync and the publish; 034's four close by reference in T082 | at the close (tier 1's ARC-5 (a) ruled what happens to F9.2) |
| 10 | The direction arc's realization (ARC-Q1–ARC-Q4) | T070–T072, T074–T077; its composed half T073 is #1144's | beside phase 5; T073 after T029 |
| 11 | R2Q17 (a)'s 26.04 measurement | T068 (lane 4, non-gating) | when GitHub's 26.04 image is available to the org; the move itself is a required-check change, not release 2's |

## Pins and landing order (9.5): one openDox-code commit per phase, everywhere

Release 1's seven steps hold unchanged (plan 034 § "Pins and landing order";
the runbook `docs/openxdox-pin-resync-runbook.md`, #1154). Each step's PR opens
only after the step before it has landed.

| step | phase 4 | phase 5 | the arc (ARC-6) |
|---|---|---|---|
| 0. openDox root: the spec pin, the manifest and the bundle | none | T060, straight after T040 (Brett's cut word) | none |
| 1. openDox-code lands | T010–T017, T025 | T041–T058, T067, T061 (the bump last) | T072 (rides T061 only if already landed) |
| 2. openDox root: `code` gitlink, `contracts/code-pin.yaml`, workflow `@sha`s, ONE commit (`make pins`) | T027 | T062 | the arc's own root commit, only if T072 lands after T061 |
| 3. openXdox-code `pyproject.toml` `opendox @` to the SAME commit | T028 | T063 | rides T063, or the arc's own |
| 4. openXdox-code lands | T020–T024, T026, T029 | T073 (requirement 9; any time after T029) | T074 |
| 5. openXdox root: `code` gitlink and `code-pin.yaml`; `opendox-pin.yaml` to step 2's commit | T030 | T064 | T075 |
| 6. openxFactory: both pin pairs, one commit each, in ONE PR with the host wiring | T030 (+ T019; the receipt schema source) | T064 (+ HA-4's host-wiring test) | T075 (the seams' registration) |
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
  openXdox-code names ONE openxFactory commit, by full sha, in
  `tests/composed_host_pin.yaml` (decision N-7a). It advances after T030, T064
  and T075, each in an openXdox-code PR of its own, so the composed run always
  tests the host that openxFactory's `main` carries; T073 re-runs after each.
- **Merge method.** Squash or merge commit, never rebase, in every product
  repository, so each landing is ONE first-parent commit for 5.4a's, 12.5's
  and 11.1's guards. codexFactory allows merge commits ONLY (T008).

## The trailer, the guard and Rule 6

- **Realization landings** carry `Arc: neutral-product-standalone-operability`
  and their lane's `Lane:` line (`Lane: openxfactory-4`, or `Lane:
  openXfactory-3` for the peer's), in every repository the arc touches,
  openDox-spec included (T040, T060). T073 is one of them: it is #1144's
  requirement-9 work, so it carries #1144's value, not the direction arc's.
- **Bookkeeping** carries NO `Arc:` trailer (R1Q20 (a)): this feature's files,
  batch Q, #1144's ticks, evidence notes, interim guard output, and the
  codexFactory spec amendment (T008; decision N-8).
- **The direction arc's change** (T070–T072, T074–T077) carries its own trailer
  value (decision ARC-4), so #1144's guards neither count nor miss its
  landings. Because that also takes T075's openxFactory edits out of F11.1's
  selection, the arc's change runs an equivalent surfaces check over its own
  landings (F11.1's guard logic, selected by its own trailer), quoted in T075's PR
  and in T077's archive evidence (ADV-37).
- **Non-arc acts in plan 034's T066 form** (both pins, no `Arc:` trailer): T059,
  only if G15-H's display-facet schema bump moves an openxFactory facet test.
- **F11.1's guard is closed** (HOST, HOST_TESTS, PIN_PAIRS, COMPOSITION_TESTS,
  ADMITTED_ARC_EDITS). It grows only by a further ruling (`5890601202`). No
  task here needs it to grow: T019, T030's schema-source registration and T064's
  host-wiring test sit in host wiring and under `tests/domain_profile/`, HOST and
  HOST_TESTS surfaces (inferred from the guard's constants as R2-INV-12
  § "Proposed phase-4 task outline" reads them; T032's interim run proves it).
- **Rule 6.** Every PR touching `openspec/changes/` lands under a `LANDING` /
  `LANDED` window: T005, T070, T071, T076 (while #1144 is active), T077 and
  T082. Realization PRs never touch it. No closing keyword appears in a commit
  message or PR body.

## Ruled answers, round 1 (`6003486656`)

Brett Heap answered all 25 by interactive multi-choice, verbatim *"Accept all
25 recommended (Recommended)"* (`#656` `6003486656`). Every question took (a).
`spec.md` § Clarifications holds each answer; this table names where the plan
carries it out. "No task" means the answer constrains tasks without being a
task.

| question | answer | what it fixes in this plan |
|---|---|---|
| R2Q1 | (a) | One user-facing interface; three ports stay split. T015/T016 put `submit`/`land` in every governance mode under openDox's own profile; batch Q (T005) records the map's phrase as a non-normative reading. CF-1 (I-1) confirmed the reading. |
| R2Q2 | (a) | `pull_request_factory` keeps `GhPullRequests`; the new pair defaults to `LocalGitSubmissions` (T014). Batch Q's repoint-sentences note (T005). Ruling `5783934499`'s third bullet and 12.5's "host's implementation registered" go unrealized (Conflicts C-3). |
| R2Q3 | (a) | No governed host carries `submit`, `land` or `health` in release 2: the verbs, routes and route-derived flags are default-profile contributions (decision N-2; ADV-14); T019 and T064 prove the hosts' trees, goldens and `/capabilities` unchanged; F12.2's host side runs against a registered test host (T012, T016, T031). |
| R2Q4 | (a) | The instrument is a contributed `SubmissionPort` in the host profile; under `governed` no lander is bound; `land` submits through it (T012, T016). |
| R2Q5 | (a) | Any local branch but `main`; a landed live session ends by the existing merge observation (T016, `branch_session.py`). No standalone session opener (no task). |
| R2Q6 | (a) | The lander's own landing worktree, `--no-ff`; ff-only of a clean served checkout on `main`, and a refusal when the served checkout holds `main` and is not clean (ADV-08); `land` pushes nothing, `ls-remote` check first. Feature 007's four exceptions: T008 (codexFactory) and T013 (the guard and pins). The README's two push routes: T018. |
| R2Q7 | (a) | Default branch `main` for landing; no `main` → `unknown`, refused naming it; no declaration → `land` refuses naming the file and content (T012, each a named test node); the root README documents it (T018). The health baseline's branch is `main`, else the branch HEAD names (tier 1's I-2 (a), ruled). |
| R2Q8 | (a) | F12.1 runs composed (batch Q's line, T005; with ARC-Q2 (a), tier 2's CF-5 reading); the repair slice U-1 to U-9 (T020–T029); R1Q6 (d)'s decision first (T006, done). |
| R2Q9 | (a) | Batch Q (T005), the first act: F6.1's entry point, its struck "Today" text and 6.2's superseded description; F14.1/F15.1 start the document server; F15.1's sandbox precondition; the forking pack's child carries its pack id; the export cannot be steered by `export-subst`/`export-ignore`; the escaping pack's restore is a write; `--local` on the verb shapes of 12.4a, 12.6a and 14.5 (F14.1 and F15.1 stand as written). Realized by T015, T016, T046, T048 (items 3, 5), T052 (item 1), T055 (items 4, 6), T058, T067 (item 3). |
| R2Q10 | (a) | The finding id rule (T041), hashing a position-independent identity key the family supplies (ADV-07, a conforming refinement); `health list --json` carries `kind` (T046); F14.1/F15.1 select planted findings by fixture document, every literal-id use enumerated (batch Q item 4; ADV-24). |
| R2Q11 | (a) | `stage-location-mismatch` reads the six role keys' top-level directories; `auto-fix` edits `stage:` only (T044, T053). |
| R2Q12 | (a) | Baseline = the previous default-tip run in the store; exactly three classes (new, pack-upgrade, persistent; I-2 (a) ruled, so no `unclassed` fourth); runs at the tip, on a branch or over the working state (N-10, as corrected); disappearance only between default-tip runs; citations; the uncited re-raise (T046). Conflict C-2 records the narrowed reading. |
| R2Q13 | (a) | DOMAIN: `identity.TABLES`, and the closure test reads `0001` with `0003_`, in one change (T042). |
| R2Q14 | (a) | 6.1a satisfied vacuously; no family moves, no shared module (T052 records it at the tick). |
| R2Q15 | (a) | Hosted plane: the health view, routes and verbs refuse by name and record nothing; the schema still migrates (T046, T057, T042). |
| R2Q16 | (a) | Trusted installed code in process; only manifest-listed packs sandboxed; no sandbox → no packs and one finding; no Seatbelt (T048, T056, T052). A host's registered check replaces openDox's own at the scoped seam (ADV-18). Batch Q records the full reading (item 9). |
| R2Q17 | (a) | The required-check change, by this word (T010); F15.1's shell block in the same required job (T067); the 26.04 measurement has an owner (T068), and the move itself is not release 2's. |
| R2Q18 | (a) | Packs import the standard library and `opendox.health_contract` only (N-3); the sandbox binds the interpreter, its standard library and that module, never `site-packages` (T048); digest plus version pin everything (T045, T047). |
| R2Q19 | (a) | Kept as ratified: packs see only the exported tree (T048). No amendment task. |
| R2Q20 | (a) | Kept as ratified: pack checks are model-free (T045). No amendment task. |
| R2Q21 | (a) | `health/packs.yaml` is authoritative; the `stack.yaml` lockstep check is F2's (T047). No release-2 task for F2. |
| R2Q22 | (a) | Three openDox-spec schemas (T040); the root's spec pin and one `dox-v1.2` minor on Brett's cut word (T060, straight after T040); digest-checked copies at the pinned commit (T041 → T047 → T054); batch Q's 9.5 addendum and 7.1's addendum (four kinds become seven copies). |
| R2Q23 | (a) | 0.2.0 bump (T061), publish LAST on Brett's word (T084), under batch Q's batch-O style addendum. |
| R2Q24 | (a) | AT-R2 (T080, T081; quickstart.md). |
| R2Q25 | (a) | Evidence holds locators only, and `message` is bounded the same way (ADV-27); the store holds no patch text (lane 3's MISLABEL row 31); the view reads the passage from git (T041's shape, T042's store test, T057). |

## Ruled answers, the `doc_health` direction arc (`6003918488`)

Lane openXfactory-3 prepared the ask read-only (`lane-coord-034/r2/R2-ARC-ASK.md`,
CLAIMED on `#656` `6003715712`). Brett Heap answered all four by interactive
multi-choice; `6003918488` records his words verbatim.

| question | answer | what it fixes in this plan |
|---|---|---|
| ARC-Q1 | (a) *"Retarget all eight (Recommended)"* | The generic `lines` slice re-authored in openDox-code (T072); the governed names reached through seams openXdox-code declares (T074) and openxFactory's host wiring registers (T075, the pattern of `scripts/opendox_host.py:518-533`); the 7 test files that import `doc_health` respelled, none of them protected (T074); `DOC_HEALTH_SURFACE` empty; no `corpus-adapter-seam` change. |
| ARC-Q2 | (a) *"Composed CI in openXdox-code (Recommended)"* | U-9's composed workflow, pinned to openxFactory, is PERMANENT (T029); it gains R1Q24's 3 rail files and 5 contracts files and the governed-behaviour tests, declared as integration tests with count and reason (T073, #1144's requirement-9 work, lane openXfactory-3, not gated on T071); requirement 9 closes for openXdox-code by declaration; F9.1's declaration is amended in batch B's form, in batch Q (T005). |
| ARC-Q3 | (a) *"Own change, beside phase 5 (Recommended)"* | Its own OpenSpec change, `code_surface:` naming openXdox-code, openDox-code and openxFactory host wiring (T070); Brett's ratify word (T071); realization slices (T072, T074, T075); archive on merged, green evidence (T077); owned by lane openxfactory-4; gates neither release 2's close nor #1144's archive, so T061 never waits for T072 (ARC-6) and #1144 may archive with F9.2 open (tier 1's ARC-5, ruled). `target_release: implemented` (tier 1's ARC-1, ruled). |
| ARC-Q4 | (a) *"Confirm (Recommended)"* | The decision is discharged before F12.1; the realization is not on 12.5's path. T006 is done. |

Measured in the ask (fact 3): 0 of the 174 composed reds are `doc_health`-caused,
so U-1 to U-9 and R-1, W-1, H-1 and H-2 do not change.


## Ruled answers, the plan ruling (`6013547504`)

Brett Heap ruled this plan at `6847e99e` on 2026-10-06, by interactive
multi-choice; `#656` comment `6013547504` records his words verbatim. Before he
ruled, the plan had passed an independent Opus `speckit-analyze` and
adversarial review, lane openXfactory-3's plan check, one fix round folding in
both, and both reviewers' re-check of that round (every CRITICAL, HIGH and FIX
item landed as worded). T004, this revision, encodes the ruling.

| item | Brett's answer, verbatim | what it fixes in this plan |
|---|---|---|
| R-1 | *"Admitted edit kind (Recommended)"* | (a): a new `edit: admitted` kind reaches named module-level spans; `scripts/protected_suites.py`'s `_inside_the_test` rule is amended to accept it; each such edit is reviewed in U-7's PR (T026). With W-1, all 26 nodes close. |
| W-1 | *"Model import-free again (Recommended)"* | (A): openDox-code inlines what `staging-workbench-model.js` takes from `./display.js` (T025); a guard keeps the inlined tables equal to `display.js` (T050). This word reverses carve slice S7's model import. |
| ARC-5 | *"Archive with F9.2 open (Recommended)"* | (a): #1144 may archive with F9.2 open, reported in R1Q6 (d)'s form; F9.2's later closure goes into the arc change's own evidence (T076); the archived `tasks.md` is never edited. It reconciles F9.2's ruled notes (`5859927858`, `5870594693`) with ARC-Q3 (a). |
| I-2 | *"main, else HEAD's branch (Recommended)"* | (a): the baseline branch is `main`, else the branch HEAD names; R2Q7 (a)'s `main` still governs landing alone. `spec.md` FR-010 and its other "`main`'s tip" lines are amended in this revision; batch Q notes the reading at 14.4 (T005 item 12). |
| N-6 | *"Allow the overlap (Recommended)"* | (a): phase 5's openDox-code slices may land once T027 pins phase 4's openDox-code commit, without waiting for T033; batch Q records the reading beside the release map (T005 item 12). |
| ARC-1 | *"implemented (Recommended)"* | (a): the arc change's `target_release:` is `implemented` (T070). |
| N-7b | *"Make it required (Recommended)"* | (a): the holder adds `composed` to openXdox-code's required checks after T029's first green run on `main`, recorded in T029's evidence. This word is the required-check change. |
| tiers 2 and 3, and the lane split | *"Accept all as recommended (Recommended)"* | CF-1 to CF-8 confirmed; the 52 tier-3 defaults ruled as recommended; the two-lane split confirmed (T009): lane openXfactory-3 takes T020–T026, T029, T073 and the pack track (T045, T047, T048, T049, T055, T056, T058), and lane openxfactory-4 the rest, landing every PR. |

**Still Brett's word, at the act** (named in the ruling): the `dox-v1.2` cut at
T060, the arc change's ratification at T071, and the 0.2.0 publish at T084.

## Design decisions, RULED with the plan (`6013547504`)

**Every item below is RULED.** Brett Heap ruled them at `6847e99e`, by
interactive multi-choice, every item as recommended (`#656` `6013547504`;
§ "Ruled answers, the plan ruling" quotes his words). Each item is marked with
the option taken; the options not taken stay as the record of what he was
shown. Review round 1 put them in three tiers, on the holder's rulings,
conforming to ratified text wherever possible. T004 moved three items to match
the ruling's record: N-7b, ruled on its own question, is in tier 1, and
OQ-12-12's and OQ-12-16's readings are tier 2's CF-7 and CF-8. "Was row N" maps
each item to the 63-row table of `6d6911e1`, which the two review evidence files
cite. Row 59 (N-9, the batch letters) is a record, not a decision: release 2's
amendment batches continue #1144's letters after release 1's A–P, so batch Q is
next.

### Tier 1: RULINGS (seven), each ruled as recommended

Each lists the option Brett took first, its alternatives, and a one-line
consequence.

**R-1. The staging suite's 26 `PROTECTED-CONFLICT` nodes** (was row 38;
R2-INV-P4F § "Items needing a ruling", corrected by lane 3's row 38 FIX).
`tests/test_staging_workbench.py` is one of 12.5's 16 protected suites. 21 of
the 26 run the suite's Node harness, whose text sits in the module constants
`_CREATE_HARNESS` (`:492-553`) and `_SESSION_HARNESS` (`:1008-1094`), outside
any test, so no in-test allow-list entry reaches them; 3 are one-off S3 nodes
(`:802` and `:1286` import-free pins, `:1291` and `:1333` route claims); 2 are not
harness text at all: `test_staged_scope_adds_cluster_neighbourhood_section`
expects 'group' where S7's neutral word is 'cluster', inside the test, and
`test_the_hostile_descriptors_still_parse_into_the_real_cli` fails `SystemExit: 2`,
untraced.

**RULED (a)**, verbatim *"Admitted edit kind (Recommended)"* (`6013547504`).
- **(a) (Recommended; RULED)** A new `edit: admitted` kind, of R1Q26 (a)'s sort, that
  reaches named module-level spans: `scripts/protected_suites.py`'s
  `_inside_the_test` rule is amended to accept them, and each admitted edit is
  entered and reviewed in U-7's PR (T026); batch Q notes it at 12.5's falsifier.
  It closes the 21 harness nodes and the `:1291`/`:1333` claims ONLY TOGETHER
  WITH W-1, because those nodes first fail on the `./display.js` import at the
  helper copy sites (`:98`, `:565`, `:1242`, `:2000`, `:2507`), outside the
  spans. The 'cluster' node takes an ordinary in-test entry (H-2's form); the
  `SystemExit: 2` node is traced first in T026, and returns to Brett only if its
  trace finds no admissible repair.
  *Consequence:* all 26 close and the suite stays in 12.5's proof.
- **(b)** W-1's route for the import-free pins only (`:802`, `:1286`).
  *Consequence:* 21 harness nodes and the two route claims stay red, so F12.1
  cannot exit 0 and phase 4 does not close.
- **(c)** Re-scope 12.5's governed set to drop `test_staging_workbench.py`.
  *Consequence:* F12.1 runs over 15 suites; the proof shrinks, and 12.5's
  falsifier text changes (a batch Q amendment on this word).

**W-1. The `display.js` route for 32 nodes (and the `:802`/`:1286` pins)** (was
row 39; R2-INV-P4F § display-js). Both routes were proved equivalent by
simulation: 32 clear.

**RULED (A)**, verbatim *"Model import-free again (Recommended)"* (`6013547504`).
- **(A) (Recommended; RULED)** openDox-code makes `staging-workbench-model.js`
  import-free again (U-6, T025), inlining what it takes from `./display.js`; T050
  adds a guard that the inlined tables equal `display.js`'s.
  *Consequence:* reverses the S7 amendment the model's header records (`:36-40`;
  openDox-code `1e46971`), a ruled carve slice, so it needs this word; the
  protected proof passes on the bytes the product serves.
- **(A′)** `tests/opendox_bundle.py`'s `composed()` (not protected) flattens the
  `./display.js` import into its composed copy (T026).
  *Consequence:* S7 stands, but the proof by proxy then passes on bytes the
  product does not serve.

**ARC-5. #1144's archive and F9.2** (was rows 34 and 49; lane 3's MISLABEL row 49;
ADV-20). F9.2's ruled notes keep it open until the direction arc LANDS
(`5859927858`: "It runs again once the doc_health direction arc (T008) lands.
F9.2 is unchanged."; `5870594693`: "T008 removes it together with the workflow
deselect"). ARC-Q3 (a), the later ruling, says the arc "gates neither release 2's
close nor #1144's archive" (`6003918488`). OQ-038-2's default clause ("blocked
until F9.2 closes") predates the arc ruling.

**RULED (a)**, verbatim *"Archive with F9.2 open (Recommended)"* (`6013547504`).
- **(a) (Recommended; RULED)** #1144 MAY archive with F9.2 open, reported as part of
  requirement 9's open extraction for openXdox-code in R1Q6 (d)'s reporting form.
  F9.2's later closure is recorded in the arc change's own evidence (T076); the
  archived `tasks.md` is never edited. If #1144 is still active when T076 runs,
  T076 ticks F9.2 there under Rule 6. Batch Q adds this note at F9.2. This
  feature ticks 11.0, 11.1 and F11.1 at T082, and 9.5 last, at T084, after the
  cut's sync and the publish that still realize it; plan 034's T090–T093 close
  by reference; the archive act itself stays the holder's. (Sequencing fix
  after the ruling, from Copilot's review: the option as Brett was shown it
  named T082 for all four boxes.)
  *Consequence:* the two rulings read together; the arc gates nothing.
- **(b)** #1144's archive waits for T076 (F9.2's ruled notes read literally).
  *Consequence:* the arc gates #1144's archive, against ARC-Q3 (a)'s words.
- **(c)** Amend F9.2 in batch Q to run in the composed workflow, so it can close
  in release 2. *Consequence:* changes F9.2's environment ("openDox arriving ONLY
  through the pin"), a falsifier-text change on this word.

**I-2. The health baseline in a repository with no `main`** (was row 36; lane
3's MISLABEL row 36). R2Q7 (a) makes `main` the default branch and a repository
without one `unknown`; R2Q12 (a) makes the baseline the previous run at "the
default branch's tip". F14.1 and F15.1 create their repositories with `git init
-q`, so on an unconfigured runner they have `master`, not `main` (C-14).

**RULED (a)**, verbatim *"main, else HEAD's branch (Recommended)"* (`6013547504`).
- **(a) (Recommended; RULED)** The baseline branch is `main`, else the branch HEAD
  names (a detached HEAD in a repository with no `main` has none). R2Q7 (a)'s
  `main` still governs LANDING alone.
  *Consequence:* requirement 6's "BASELINE-RELATIVE" holds in every repository,
  F14.1's included; spec FR-010's "`main`'s tip" reads "the baseline branch's
  tip", amended at T004, and batch Q notes the reading at 14.4.
- **(b)** In a repository with no `main`, every finding is `unclassed` and one
  install-level `no-default-branch` finding names the absent branch; no
  disappearance is measured.
  *Consequence:* suspends requirement 6's baseline where there is no `main`,
  F14.1's own repository possibly among them (F14.1 still passes; it asserts no
  class).

**N-6. Phase 5's openDox-code work overlapping phase 4's tail** (was row 56;
ADV-25). The RULED release map says "The ORDER they are built in is the release
map" (`5799646419`).

**RULED (a)**, verbatim *"Allow the overlap (Recommended)"* (`6013547504`).
- **(a) (Recommended; RULED)** Allow it: phase 5's openDox-code slices land once T027
  has pinned phase 4's openDox-code commit, without waiting for T033. Batch Q
  records the reading beside the map.
  *Consequence:* the path shortens by T028–T033; a P4-F repair that needs a
  further openDox-code change then rides phase 5's pin.
- **(b)** Release 1's strict order: every phase-5 task after T033.
  *Consequence:* the map's order holds literally; phase 5 starts later.

**ARC-1. The arc change's `target_release:`** (was row 45; Brett's to name).
The vocabulary admits `implemented`, a release this estate defines, or
`deferred-allocation` (#1144's own front matter).

**RULED (a)**, verbatim *"implemented (Recommended)"* (`6013547504`).
- **(a) (Recommended; RULED)** `implemented`: the affected repositories' main lines
  (openDox-code, openXdox-code, openxFactory). No bundle is cut; it archives only
  on merged, green realization evidence because its `code_surface:` is non-empty.
- **(b)** `deferred-allocation`, if Brett wants the change to hold a release slot
  open (for an openXdox-spec delta that might need a bundle).
- **(c)** A release this estate defines, named by Brett (for example the
  `opendox` version its `lines` module first ships in).

**N-7b. The required-check act for the composed workflow** (was row 57's
second half; moved from tier 3 at T004, because Brett ruled it on its own
question). U-9's composed workflow (T029) is permanent (ARC-Q2 (a)).

**RULED (a)**, verbatim *"Make it required (Recommended)"* (`6013547504`); this
word is the required-check change.
- **(a) (Recommended; RULED)** The holder (lane openxfactory-4) adds `composed`
  to openXdox-code's required checks after T029's first green run on `main`,
  recorded in T029's evidence.
  *Consequence:* a permanent check cannot rot unseen; every openXdox-code PR
  waits on it.
- **(b)** Leave it not required. *Consequence:* a red composed run blocks
  nothing, and 12.5's proof can regress between checkpoints.

### Tier 2: readings CONFIRMED (eight)

Brett confirmed all eight, verbatim *"Accept all as recommended
(Recommended)"* (`6013547504`). One line each, the confirmed reading first.

| id | reading (CONFIRMED) | alternative (not taken) |
|---|---|---|
| **CF-1. I-1** (was row 35) | "The same in every mode" (R2Q1 (a)) means every GOVERNANCE mode (`standalone`, `governed`, `unknown`) under openDox's own profile; a host profile that replaces the default carries none of `submit`, `land` or `health` in release 2 (R2Q3 (a)); a `governed` repository with no instrument refuses `land` by name ("governed-without-an-instrument", 12.6a). FR-004 states both. | "Every mode" includes host profiles, which contradicts R2Q3 (a). |
| **CF-2. Batch Q's contents** (was rows 37, 55, 62: I-3, N-5, N-12) | ONE batch, one Rule 6 window, before phase 4's checkpoint, carrying: (1) R2Q9 (a)'s seven, with item 1's note that 6.2's description is superseded; (2) R2Q2 (a)'s repoint note; (3) F12.1's composed line, worded as CF-5; (4) R2Q10 (a)'s selection lines, every literal-id use in F14.1 and F15.1 enumerated; (5) R2Q1 (a)'s non-normative reading; (6) ARC-Q2 (a)'s F9.1 declaration, batch B's form; (7) ARC-5's F9.2 note as ruled; (8) H-2's and R-1's notes at 12.5's falsifier as ruled; (9) R2Q16 (a)'s full reading at requirement 16 and 15.1b; (10) 9.5's two addenda (the `dox-v1.2` bundle; 0.2.0); (11) 7.1's addendum (four kinds become seven copies, R2Q22 (a)); (12) I-2's and N-6's readings, as ruled. | A batch per phase, as each falsifier is reached: more Rule 6 windows, and phase 4's checkpoint would wait on more than one. |
| **CF-3. H-1** (was row 40) | Confirm the shim, openXdox-code `scripts/ideation_dashboard/session_git.py` (`import sys; from opendox import session_git as _m; sys.modules[__name__] = _m`), with NO `__init__.py` (ADV-39), restoring the spelling `LOCK_HOLDER` imports (`test_session_transaction.py:296`). | Respell `:296` under R-1 (a)'s kind, with no shim. |
| **CF-4. H-2** (was row 41) | Admit the 17 AL entries (`cmd_gate_*` 7, `hosted_index` 3, share paths 2, Group W 1, Group S2 4), which respell names the split-opendox CARVE moved in commits with no `Arc:` trailer, under batch C, on `5962785556` item 1's precedent. **Two views:** the Opus review reads batch C's ratified text (#1144 `tasks.md:922-936`) as admitting any pure respelling, so no widening is needed; lane openXfactory-3 reads R1Q7 (a)'s "a reference to a moved seam" in its release-1 context as the arc's moves, so this stretches batch C. Either way batch Q records it. | Treat the 17 as RULING-class, or exclude their nodes from F12.1. |
| **CF-5. F12.1's composition** (ADV-15; lane 3's T005 item 3 FIX) | R2Q8 (a) says F12.1 runs composed "until the direction arc's realization lands"; ARC-Q2 (a), the later ruling, makes the composed workflow permanent, and the governed-behaviour tests stay composed after the arc. Read together: F12.1 runs composed, and ARC-Q2 (a) makes the composition its permanent home. Batch Q words item 3 so. | Read R2Q8 (a)'s limit literally, so F12.1's line expires into a standalone form that cannot pass once T074 lands. |
| **CF-6. "Optionally on commit"** (was row 17, OQ-H-18; lane 3's low-confidence MISLABEL) | It means a documented hook line, `opendox health run --repo-root .`, which the user may add to their own hook; the product writes nothing under `.git/`. | An opt-in `health hook` verb that writes `.git/hooks/pre-commit` (a 14.5 surface change, and a write under `.git/`). |
| **CF-7. The remote `submit` chooses** (was OQ-12-12, row 3; ADV-26; lane 3's T011 FIX) | The remote is `origin`, else the sole remote; several remotes and none named `origin` raise `NoSubmissionTarget` by name, which narrows requirement 11's "a remote attached" to a remote the product can choose without guessing; several push URLs raise `SubmissionRefused`. The push core is `_push_to_remote_with` (`repository_act.py:1742`) factored into `submission_push.py`, keeping the command-config refusal (`:1335`, `:1372`). | `origin` only, or the first remote listed. |
| **CF-8. F12.2's "`gh` NOT installed"** (was OQ-12-16, row 6) | F12.2 runs under a PATH that hides `gh`, asserted (`command -v gh` fails) and recorded; that meets F12.2's asserted precondition (#1144 `tasks.md:2824-2825`), a reading of its prose "`gh` NOT installed" (`:2817`). | A container image without `gh` (GitHub runners ship it, inferred). |

### Tier 3: DEFAULTS, RULED together (52)

Brett ruled all 52 as recommended, verbatim *"Accept all as recommended
(Recommended)"* (`6013547504`). Each conforms to ratified text, as review round
1 corrected it. "Adopt" keeps `clarify-questions.md`'s proposed default;
"refine" or "conform" says what moved. The decision column is what was ruled.

| id | was row | decision (RULED) | alternative (not taken) | why |
|---|---|---|---|---|
| OQ-12-9 | 1 | Adopt. The CLI `submit` is not under the console-presence and `--actor` gate; the route stays gated (12.4a). | Gate the CLI. | F12.2 runs it with no actor. |
| OQ-12-11 | 2 | CONFORM (ADV-09). A credential-bearing remote is PUSHED; the `Submission`'s `url` and every message are redacted (12.1a). | Refuse it (the first plan's default, which narrowed 12.1a). | 12.1a designs exactly this case, and F12.2's redaction test expects the report to name the host and path. |
| OQ-12-13 | 4 | Adopt. `land-nonce` then `land`, both gated with the console token. | One two-step route. | Single use is testable. |
| OQ-12-14 | 5 | Refine (ADV-14). The routes and their flags are default-profile contributions; `actions.submit` and `actions.land` are PRESENT only under openDox's own profile, their VALUES derived from the route bindings as `gate`'s is (core `_DEFAULT_CAPABILITIES` always carries `gate` and gains nothing); controls in `web/views/branch-actions.js`. | `submit` keys on `session` (the first default). | A host profile's payload stays byte-identical, and no control is offered where no route answers (plan 034 T084's rule). |
| OQ-12-17 | 7 | Adopt. `land(branch)` serves fix drafts, the batch draft included. | A batch-land API. | One signature. |
| OQ-H-2 | 8 | Adopt. The registered check's default families answer a call that names none. | Callers always name families. | Today's callers keep working. |
| OQ-H-3 | 9 | Refine (ADV-18). One neutral check, the built-in families, registered at the scoped seam ONLY when it is empty; a host's check replaces it; both registration orders tested. A scoped run is not stored. | Register unconditionally. | The seam holds one check and refuses a different second one (`workbench.py:1622-1651`); R2Q16 (a) keeps the host's running. |
| OQ-H-8 | 10 | Refine (ADV-17, ADV-40). Orphans, stale stubs, an unmovable broken link and non-derivable front matter are `human-only`; an EMPTY stub is `assisted` (14.6), with a deterministic proposal; the stub criteria are declared (data-model.md § Families). | Stale stubs `assisted` too. | 14.6 and requirement 14's third scenario fix empty stubs as `assisted`. |
| OQ-H-10 | 11 | Adopt. A unique basename elsewhere is a moved target; ambiguous or absent is `human-only`. | Git rename detection. | Deterministic, no history. |
| OQ-H-11 | 12 | Refine. Deterministic proposals for near-duplicates (a note naming the other document; `path` the later-committed one) AND empty stubs. | A model-written proposal. | No model-assisted family in release 2. |
| OQ-H-13 | 13 | Adopt. `kind: opendox-health-dispositions`, keyed by finding id, suppress not downgrade, another kind refused. | Downgrade. | F14.1 asserts absence. |
| OQ-H-14 | 14 | Adopt. `accept` writes the working tree, or a draft branch where there is none. | Refuse on a bare repository. | One landing path. |
| OQ-H-15 | 15 | Adopt. The engine's files join the settings exclusion. | Lint them. | They are configuration. |
| OQ-H-16 | 16 | Adopt. README and index documents are exempt from "nothing links to it". | No exemption. | Entry documents have no inbound link. |
| OQ-H-20 | 18 | Adopt. No model-assisted family in release 2. | Model near-duplicates. | F14.1 stays deterministic. |
| OQ-H-21 | 19 | Refine. `doxbench_knowledge` cosine only if it runs with no binding (T044 measures), else Jaccard shingles; the threshold is measured and recorded. | Always Jaccard. | Every install gets health (SC-006). |
| OQ-H-22 | 20 | CONFORM (lane 3's MISLABEL row 31). Runs and findings tables, no foreign key to `projects`, provenance NOT NULL, and NO patch column. | A patch column. | 14.3 and R2Q25 (a) keep document text out of the store. |
| OQ-H15-1 | 21 | Adopt. A Python package run through the engine's shim. | Any executable. | One runtime to sandbox. |
| OQ-H15-5 | 22 | Refine (lane 3's bwrap-facts FIXes; ADV-22, ADV-40). Budget and bounds are the ENGINE's: `--timeout` defaults to 60 seconds per pack, capped at 600; address space, CPU, file size, tmpfs and stdout through rlimits and `bwrap`; the process count through `pids.max` where a cgroup is delegated, never `RLIMIT_NPROC` (per user, not per sandbox), and NOT bounded where no cgroup is delegated (an accepted limit the run records, contracts/health-packs-manifest.md); no per-entry budget or bounds in the manifest; T056 measures the defaults against `pack-corpus`. | Per-entry budgets; `RLIMIT_NPROC`. | 15.6 puts the budget in the engine; setrlimit(2) counts NPROC per real user. |
| OQ-H15-9 | 23 | Adopt. The canary is per-run product behaviour, and now plants both a CANARY variable and a CANARY descriptor (15.6a). | A test hook. | F15.1 stands. |
| OQ-H15-10 | 24 | Adopt. A static `opendox-pack.yaml`; forbidden keys refused. | Runtime output. | No pack code before its check. |
| OQ-H15-11 | 25 | Adopt, with the stderr half refined after the ruling (Copilot's review of `b7137d5e`, under R2Q25 (a)). One JSON document on stdout; stderr is never stored, and a failure finding carries only engine-authored metadata (category, exit status or signal, stderr's byte count and SHA-256). | JSON lines; a stored stderr tail (the ruled default's first wording, which could store document text). | One bounded parse; R2Q25 (a) keeps document text out of the store. |
| OQ-H15-12 | 26 | Adopt, with its reading stated: `sorted-ls-tree-r-v1` (defined over a commit) applied to `<corpus-commit>:<source>` for a corpus-relative source, and to the declared `commit`'s root tree for a git-URL source; gitlinks refused; HEAD's tree in a working-state run. | Whole tree only. | A corpus-relative pack needs a subtree digest. |
| OQ-H15-14 | 27 | Refine (ADV-21). The engine fetches over `https://` or `ssh://` only; `file://`, `ext::`, local paths and credential URLs refused; the runtime's hardened transport rules reused. | Any URL git accepts. | A cloned corpus must not choose a transport. |
| OQ-H15-15 | 28 | Adopt. A health role family under a schema-version bump; host labels win. | Raw labels. | 15.3. |
| OQ-H15-18 | 29 | Adopt. `opendox`'s version is the installed one; a family's own in evidence. | Per-family. | 15.7. |
| OQ-H15-19 | 30 | Adopt. Pack ids `[a-z0-9-]`; install-level findings `opendox`, empty path, `human-only`. | Dots and underscores. | Ref-name safe. |
| OQ-H15-20 | 31 | CONFORM (lane 3's MISLABEL row 31). A patch is validated at `run` (a refusal is stored as a finding, no text) and RE-OBTAINED at `fix` by re-running that one pinned pack in the sandbox, then validated again. | Stored at `run` (the first default). | The store holds no document (14.3; R2Q25 (a)). |
| OQ-H15-21 | 32 | Adopt. A fixed `bwrap` path; a version floor set by `--json-status-fd`, `--disable-userns`, `--size`; T010 records the runner's version. | A PATH lookup. | PATH can be steered. |
| OQ-038-1 | 33 | Adopt. The refusal names the remedy; no conflict verb. | `land --rebase`. | #1144 declares none. |
| P4F-3 | 42 | CONFORM (ADV-10; lane 3's T022 FIX). The runbook is PLACED from the composed tree (`openDox/spec/docs/…` at the root's pinned spec commit) by T022's script, git-ignored; nothing vendored. | A digest-checked copy in openXdox-code (two copies of an openDox-spec document). | openXdox-code's copy record is single-source (`copies.yaml:1-33`). |
| P4F-4 | 43 | CONFORM (ADV-10; lane 3's T021 FIX). `gate-action-record` is read from openXdox-code's own package; `demotion-execution-receipt` from a schema source the HOST registers (the composed conftest, then host wiring at T030); a lone checkout refuses by name. Nothing vendored. | Vendor the receipt schema (conflicts with `test_packaged_validator.py:81-92`, `neutral-product-pin` and R1Q27 (a)). | No conforming text is bent. |
| P4F-5 | 44 | Adopt. A governed-suite list with its own guard; the composite registered only in the composed run. | Gate column on every host-plane suite. | Smaller blast radius. |
| ARC-2 | 46 | Adopt. The change id `realize-doc-health-direction-arc`. | `retarget-openxdox-doc-health-imports`. | It names the topic it exits. |
| ARC-3 | 47 | Refine (lane 3's row 47 FIX). `skip_specs: true`, no `corpus-adapter-seam` delta. If the seams need contract text, an openXdox-spec delta is written into the change T070 authors, and Brett's ratify word (T071) is the word for it; the ruling itself said nothing of one. | An ADDED requirement in a new capability. | Requirement 1 is met, not changed. |
| ARC-4 | 48 | Refine (ADV-37). Its own `Arc: realize-doc-health-direction-arc` value; plus an equivalent surfaces check over its own landings, quoted in T075 and T077. | #1144's value. | Its evidence is its own, and its openxFactory edits stay checked. |
| ARC-6 | 50 | CONFORM (ADV-06; lane 3's T072 and row 50 FIXes). T072 is opportunistic: it rides T061's pin only if already landed; T061 NEVER waits for T071 or T072; a late T072 rides the arc's own pin. | T061 after T072 (the first default, which put the arc on release 2's cut). | ARC-Q3 (a): the arc gates nothing. |
| N-1 | 51 | Adopt. `.opendox/governance.yaml`'s shape, no fourth schema. | A fourth schema. | R2Q22 names three. |
| N-2 | 52 | Refine (ADV-14). The verbs, their routes and their route-derived flags are default-profile contributions. | Core verbs and routes. | R2Q3 (a): hosts' goldens and payloads unchanged. |
| N-3 | 53 | Adopt. ONE stdlib-only `health_contract.py`. | Two modules. | R2Q18 names one. |
| N-4 | 54 | Refine (ADV-13). One CI owner: T010 → T017 → T051 → T067 (F15.1's shell block) → T080. | The inventory's W3 placement. | Fail-not-skip from the first sandbox test. |
| N-7a | 57 | The composed workflow is its own file, `.github/workflows/composed.yml`, with ONE openxFactory commit in `tests/composed_host_pin.yaml` (`schema_version`, `kind`), checked out with recursive submodules. | A job inside `validate.yml`. | Its own lifecycle and pin. |
| N-8 | 58 | Adopt, with ADV-41. T008 is bookkeeping (no `Arc:`), lands by merge commit, and passes codexFactory's required `validate` and `lane-line` and its one-approval rules. | Carry `Arc:`. | It realizes no code. |
| N-10 | 60 | CONFORM (ADV-16, F9). Runs at the tip, on a branch, or over the working state, as R2Q12 (a) names them; only default-tip runs form the baseline or measure disappearance. | Committed tree only (the first default, which narrowed R2Q12 (a)). | The answer names three run kinds. |
| N-11 | 61 | Adopt. No non-interactive bypass for `land`. | A `--confirm` flag. | 12.6a: refuses when there is none. |
| N-13 | 63 | Refine (ADV-07). The id hashes a POSITION-INDEPENDENT identity key in canonical sorted-key JSON with `pack_id`, `kind` and `path`; line ranges are display-only. A conforming refinement of R2Q10 (a)'s "a locator the family supplies". | Hash a line-bearing locator (the first default). | An edit above a finding must not change its id or orphan its exception. |
| N-14 | new (C4) | An uncommitted exception suppresses only in a working-state run; commit runs read the committed file. | Suppress everywhere at once. | A run reads what it reads (N-10). |
| N-15 | new | The finding schema is a copy the engine reads, not a validator kind; openDox-code's set test reads "the validator's kinds plus the finding shape"; 7.1's count becomes seven (batch Q's addendum). | Make the finding a validator kind. | The finding's `kind` field is its family, so no `kind` const can name the schema. |
| N-16 | new (C6) | `land`'s remote check reads `refs/heads/main` on the chosen remote; an absent remote branch, or no remote, passes. | Refuse when the remote has no `main`. | A first landing must be possible. |
| N-17 | new (ADV-04) | The CLI `submit` does not read the install mode; only `--local` disagreeing with `OPENDOX_INSTALL_MODE=hosted` refuses. `land`'s `standalone` still needs the explicit local install (FR-007). | Refuse the CLI `submit` on the hosted default. | F12.2 runs it with neither selection, and must pass. |
| N-18 | new (lane 3's R2Q17 FIX) | T068 measures bubblewrap and user namespaces on a 26.04 runner when available; release 2 stays on `ubuntu-24.04`, and the move is a separate required-check change. | No measurement task. | R2Q17 (a) makes the move wait for a measurement. |
| N-19 | new (ADV-11) | `health fix --finding ID [--batch]` exactly as 14.5 declares: `--batch` adds the repair to the open batch draft `health-fix-batch`; drafts branch at HEAD in the applier's own worktree. | A repeatable `--finding` (the first contract). | 14.5 closes Groups 14 and 15 on an exact surface. |

**Count:** 7 rulings, 8 readings confirmed and 52 defaults: 67 items, every one
RULED on `6013547504`. They come from the 63 rows of `6d6911e1` (row 59 became a
record; row 57 split in two; rows 34 and 49, and rows 37, 55 and 62, merged),
plus C-5 and six new defaults found in review round 1 (N-14 to N-19). T004 moved
N-7b to tier 1, and OQ-12-12 and OQ-12-16 to tier 2 as CF-7 and CF-8.

## Conflicts found, and where each was ruled

Each is a place where the 25 answers, the arc ruling, #1144's ratified text, the
inventories or the code disagree. This plan resolves none by itself: where a
decision is the way through, the row names it, and Brett ruled every such
decision as recommended (`6013547504`). Review round 1 confirmed C-1 to C-17
(the Opus review's § 4.4) and added C-18 to C-21.

| # | conflict | between | where it was ruled or fixed |
|---|---|---|---|
| C-1 | `spec.md`'s Assumptions said the 174 reds lie "across 10 files"; R2-INV-P4F § "Errata for R2-INV-12" measures **11** files and **5** green suites (210 cases). | the spec's text, lane 3's later measurement | FIXED at `6847e99e`: `spec.md` reads 11 files and 5 suites (ADV-32; lane 3's spec FIX) |
| C-2 | R2Q12 (a) holds the baseline in the store, so a reset forgets pending disappearances; #1144's "recomputable from git" is narrowed for them. Brett took that reading on `6003486656`. | R2Q12 (a), 14.3/14.4's text | accepted by the answer; recorded at T046's tick |
| C-3 | R2Q2 (a) with R2Q3 (a) leaves ruling `5783934499`'s third bullet ("contributed by the governed host") and 12.5's "With the host's implementation registered" unrealized, and 12.4's repoint sentences (`tasks.md:2513-2519`; `design.md:476-478`, `:1059-1061`) still say `GhPullRequests` is repointed. | the answers, a ruling's text, #1144's box | CF-2 item 2 (the note); the tension remains in ratified text |
| C-4 | 15.1b says "RUN EVERY PACK IN AN OS-ENFORCED SANDBOX"; R2Q16 (a) runs a host's registered check in process. They agree only if a registered check is not a "pack". | R2Q16 (a), requirement 16 | CF-2 item 9 (R2Q16 (a)'s full reading) |
| C-5 | Feature 007's FR-004 and SC-002 forbid moving the served checkout; 12.6a's landing merges and R2Q6 (a)'s fast-forward moves it. Until T008 lands, codexFactory's spec and openDox-code's guard disagree with the answer. | feature 007 (codexFactory), R2Q6 (a), `session_git.py:93`, `:99` | scheduled: T008 → T013; ADV-08's refusal keeps a dirty `main` checkout unmoved |
| C-6 | F9.2's ruled notes (`5859927858`, `5870594693`) keep F9.2 open until the arc LANDS, and #1144 cannot archive with a box open; ARC-Q3 (a) says the arc gates neither release 2's close nor #1144's archive; OQ-038-2's default said the archive "is blocked until F9.2 closes". | ARC-Q3 (a), F9.2's notes, OQ-038-2's default | tier 1's ARC-5 |
| C-7 | 14.8 says exceptions follow "openxFactory's `health/dispositions.yaml`", citing `scripts/doc_health/families.py:370`. That file is the aggregation's (`opensoft/xFactory`: `gh api …/contents/health/dispositions.yaml` returns it; for `opensoft/openxFactory` it returns 404), and the quoted words sit at `families.py:371-372`. openDox's file of the same path but another `kind` is refused by name (OQ-H-13), so `opendox health` over the aggregation's tree refuses that file. | #1144's citation, the trees | OQ-H-13; no amendment proposed |
| C-8 | F14.1 and F15.1 select findings by literal ids (`x["id"]`, `health-fix-$f`, `--finding patch-*`, `refused_patch` values); R2Q10 (a) makes ids pack-qualified keys. | R2Q10 (a), the falsifiers' text | CF-2 item 4, every use enumerated (ADV-24) |
| C-9 | 6.1 says 37 modules with `lines.py` alone generic; at `0f2a87f6` there are 38, with `lines.py` and `fs_probe.py` generic. 6.2 cites `workbench.py:1389`; `run_scoped_doc_health` is at `:1666` (`:1542-1557` is `DEFAULT_SCOPED_FAMILIES`). | #1144's text, the trees | T052's tick records the re-measure; CF-2 item 1 notes 6.2's superseded description |
| C-10 | W-1 (A) reverses ruled carve slice S7 (openDox-code `1e46971`); W-1 (A′) tests bytes the product does not serve. | W-1, the carve's ruling | tier 1's W-1 |
| C-11 | R-1: no allow-list entry can reach module-level text under the ruled `_inside_the_test` rule, yet 21 harness nodes need it, and they close only with W-1. | R2Q8 (a), R1Q26 (a)'s rule | tier 1's R-1 |
| C-12 | H-2: whether batch C admits respellings of the CARVE's moves. The Opus review reads batch C's text as admitting them; lane 3 reads R1Q7 (a) as the arc's moves. | batch C's words, R1Q7 (a)'s context, the 17 nodes | tier 2's CF-4 |
| C-13 | F12.2 requires `gh` absent; GitHub-hosted runners ship `gh` (inferred). | F12.2, the CI environment | tier 2's CF-8 |
| C-14 | F14.1 and F15.1 run `git init -q` with no branch name, so on a runner whose `init.defaultBranch` is unset their repositories have no `main`. F14.1 asserts no class, so it passes under either I-2 option; #1144's own falsifiers then never exercise the baseline on `main`, so T046's tests must. AT-R2 creates its repository with `-b main`. | F14.1's text, R2Q7 (a), R2Q12 (a) | tier 1's I-2 |
| C-15 | R2-INV-HEALTH's HA-5 adds a core `health` subcommand, and its HA-9 moves openxFactory's help golden; core routes and `/capabilities` keys would change every host's payload. R2Q3 (a) keeps both hosts unchanged. | the inventory's design, `serve.py:528-650`, R2Q3 (a) | N-2, OQ-12-14 (ADV-14) |
| C-16 | R2Q18 (a) lets a pack import "the engine runner's neutral contract module", one module; the inventory's outline has two. | R2Q18 (a), the inventory's outline | N-3 |
| C-17 | The constitution's Principle IV requires the plan's documents in the README index; the first planning PR's brief wrote only the feature directory. | the constitution, the first brief | FIXED at `6847e99e`: `README.md:87` links them (D1) |
| C-18 | 7.1, as batch G amends it, says openDox's validator validates its spec leg's FOUR kinds, and `tests/test_validator_input_set.py` holds exactly four copies; R2Q22 (a) adds three schemas to that spec leg. | 7.1's ratified count, R2Q22 (a), the test | CF-2 item 11 (7.1's addendum); N-15 |
| C-19 | R2-INV-P4F § schema proposed vendoring the receipt schema into openXdox-code's `copies.yaml`; that record is single-source (openXdox-spec, one commit) and `test_packaged_validator.py:81-92` admits only the validator's three kinds; the promoted `neutral-product-pin` admits one vendored openxFactory contract on other terms. | lane 3's inventory, openXdox-code's record and test, a promoted capability | P4F-3, P4F-4 (nothing vendored) |
| C-20 | 15.6 says the per-pack budget's default is "declared by this box", and declares no number. | 15.6's text | OQ-H15-5 (60 seconds, capped at 600) |
| C-21 | openDox-code's install mode defaults to HOSTED (`runtime/config.py:1954-1996`, `install_mode`); F12.2 runs `opendox submit` with neither `--local` nor `OPENDOX_INSTALL_MODE`. | 13.4's safe default, F12.2's command | N-17 |

## Complexity Tracking

| deviation | why it is needed | the simpler alternative, and why it was rejected |
|---|---|---|
| A permanent, REQUIRED composed workflow in openXdox-code against a pinned openxFactory (N-7a; N-7b, ruled) | 12.5's 16 suites cannot run in a lone openXdox-code checkout (15 of them fail to collect on `doc_health`, R2-INV-P4F § "Passing composed today"), and ARC-Q2 (a) makes the composition their permanent home. | Running F12.1 only by hand at each checkpoint: nothing would stop a regression between checkpoints. |
| A pin of openxFactory inside openXdox-code's CI, while openxFactory pins the openXdox root | The composed run needs a host; the pin names a commit that already exists, so no cycle of gitlinks forms (only a CI reference). | Testing against openxFactory's moving `main`: the run would not be reproducible. |
| A host-registered schema source for the gate console (P4F-4) | The receipt schema is openxFactory's, and no conforming route vendors it into the code leg (C-19). | Vendoring it, which conflicts with a promoted capability and a test. |
| The `doc_health` direction arc as a second OpenSpec change inside this plan (T070–T077, less T073) | ARC-Q3 (a) rules it. | Folding it into #1144 (ARC-Q3 (c)), rejected by the ruling. |
| A new admitted-edit kind in the protected-suite oracle (R-1 (a), ruled) | 21 nodes need module-level text that no in-test entry reaches. | Re-scoping 12.5's set (R-1 (c)) shrinks the proof. |
| Running this feature's lifecycle commands from the lane's own clone and worktree, not the git extension's sibling worktree of the shared root | Several sessions share the root checkout; each writer works in a clone of its own (plan 034 § Complexity Tracking, the same deviation). | A sibling worktree shares the root's refs, stash and branch locks with every other session. |
